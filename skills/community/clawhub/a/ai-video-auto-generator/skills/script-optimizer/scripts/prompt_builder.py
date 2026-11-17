#!/usr/bin/env python3
"""Build asset prompt files: read script.json → generate optimized prompts → save to prompts/"""

import json, os, sys, re
from datetime import datetime


def _extract_style_prefix(global_style: str) -> str:
    """从 global_style 中提取核心风格词，用于构造质量描述。
    
    提取规则：
    - 找到第一个「XX风」「XX级」「XX系」「XX派」模式，取 XX
    - 无匹配则取第一个逗号前的词整段
    - 仍无有效内容则回退 "电影"
    例: AI动漫风 → AI动漫 | 电影级写实风格 → 电影 | 水墨风 → 水墨
    """
    m = re.match(r'(.+?)(?:风|级|系|派)', global_style)
    if m:
        return m.group(1)
    parts = re.split(r'[，,、\s]+', global_style)
    prefix = parts[0].strip() if parts else ""
    return prefix[:8] if prefix else "电影"


def _style_terms(global_style: str) -> dict:
    """根据 global_style 动态生成风格感知的描述词。
    
    当 global_style 长度 ≥15 时（例"AI动漫风，画面明亮清晰，色彩饱和度高，细节丰富"），
    quality_body 和 scene_quality 直接复用 global_style，
    不再自作主张从前缀拼装——因为 LLM 生成的质量描述一定比 f-string 拼的更准。
    短描述时用前缀回退，保证空值时也有兜底。
    """
    prefix = _extract_style_prefix(global_style)
    # LLM 生成的 global_style 已含质量描述(≥15字)，直接使用；短值才自动拼装
    quality_from_style = global_style if len(global_style) >= 15 else f"{prefix}级画质，色彩鲜明，细节丰富"
    scene_quality_from_style = global_style if len(global_style) >= 15 else f"高细节渲染，{prefix}级色彩，视觉密度高"
    return {
        "quality_prefix": f"{prefix}级",
        "style_name": f"{prefix}风",
        "scene_environment": f"{prefix}场景环境",
        "lighting": f"{prefix}风格均匀光照",
        "feel": f"{prefix}感",
        "quality_body": quality_from_style,
        "scene_quality": scene_quality_from_style,
    }


def _comp_prefix(aspect: str, style_name: str) -> str:
    """根据画幅和风格返回构图前缀。"""
    orient = "竖屏" if "9:16" in aspect else "横屏"
    return f"{orient}{style_name}构图"


def build_asset_prompts(project: str, force: bool = False) -> list[str]:
    """为所有角色和场景生成 prompt 文件。返回生成的文件路径列表。"""
    script_path = os.path.join(project, "script.json")
    if not os.path.isfile(script_path):
        raise SystemExit(f"[ERROR] 未找到 {script_path}")

    with open(script_path, encoding="utf-8") as f:
        data = json.load(f)

    sc = data.get("script", {})
    global_style = sc.get("global_style", "电影级写实风格")
    terms = _style_terms(global_style)  # 风格感知的描述词，消除硬编码
    negative_prompt = sc.get("negative_prompt", "anime, illustration, cartoon, sketch, blurry")
    chars = data.get("character_cards", [])
    scenes = data.get("scene_cards", [])
    aspect = sc.get("aspect_ratio", "16:9")
    char_size = {"16:9": "1280x720", "9:16": "720x1280", "1:1": "1024x1024"}.get(aspect, "720x1280")
    # scene size always 16:9
    scene_size = sc.get("scene_size", "1280x720")
    scene_ar = sc.get("scene_aspect_ratio", "16:9")

    out_dir = os.path.join(project, "prompts")
    char_dir = os.path.join(out_dir, "characters")
    scene_pdir = os.path.join(out_dir, "scenes")
    video_dir = os.path.join(out_dir, "videos")
    os.makedirs(char_dir, exist_ok=True)
    os.makedirs(scene_pdir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    generated = []

    # ── 角色 prompt ──────────────────────────────────────────────
    for card in chars:
        name = card.get("name", "角色")
        slug = name.replace(" ", "_")
        gender = card.get("gender", "")
        gender_prefix = f"{gender}性角色" if gender in ("男", "女") else "角色"
        # 组合风格
        card_style = card.get("aesthetic_style", "")
        combined_style = f"{global_style}，{card_style}" if global_style and card_style else (global_style or card_style or "电影级写实风格")

        appearance = card.get("appearance", {})
        face = appearance.get("face", "")
        hair = appearance.get("hair", "")
        clothing = appearance.get("armor/clothing", "")
        aura = appearance.get("aura", "")
        # 特征
        dm = card.get("distinctive_mark", "")
        # 年龄
        age = card.get("age_range", "")
        age_part = f"，{age}" if age else ""

        # 基础描述（不含视角）
        base_char_desc = (
            f"角色描述：{aura} {face} {hair} {clothing}。"
            f"{dm}。"
        )

        # 定义各视角及其描述
        views = [
            ("front", "正面全身，面向镜头，展示全身形象和服装全貌"),
            ("face", "面部特写，展示五官细节和表情"),
            ("side", "侧面半身，展示侧面轮廓和发型"),
            ("back", "背面，展示背面形象和发型背面"),
        ]
        # 动作/姿态
        for w in card.get("weapons", []):
            views.append((f"action_{w}", f"手持{w}的战斗姿态，展示使用{w}的动作"))
        for a in card.get("actions", []):
            views.append((f"pose_{a}", f"展示{a}的动作姿态"))

        for view, view_desc in views:
            std_views = ("front", "face", "side", "back")

            if view == "front":
                # ── 文生图：[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求] ──
                subject = f"{gender_prefix}{age_part}，{aura}，{face}，{hair}，{clothing}，{dm}"
                scene = "白色纯色背景，无环境/无场景" if card.get("asset_background") in ("white", "纯白") else terms["scene_environment"]
                prompt = (
                    f"{subject}，{scene}，{combined_style}，"
                    f"{terms['lighting']}，无阴影，{view_desc}，"
                    f"全身完整展示，头部上方留白，脚部踩地完整在画面底部，{terms['feel']}，4K。"
                )
                # 白背景时追加纯色强调
                if card.get("asset_background") in ("white", "纯白"):
                    prompt += " 纯白背景，单一纯白色#FFFFFF，无武器，无道具，双手自然垂放。"
            else:
                # ── 图生图：[改变要求] + [新风格] + [添加/移除] + [保留元素] ──
                prompt = (
                    f"以参考图（front视角）为基础，改为{view_desc}视角。"
                )
                if view in std_views:
                    prompt += (
                        f"保持参考图中角色的面部结构、发型、服装、体型完全一致。"
                        f"纯白背景，无环境/无场景。"
                        f"{combined_style}，{terms['lighting']}，{terms['feel']}，4K。"
                    )
                else:
                    # action/pose 视图
                    prompt += (
                        f"角色保持参考图中的外观和服装，{view_desc}。"
                        f"{terms['quality_prefix']}{terms['style_name']}，动态姿态，全身完整展示，脚部踩地完整在画面底部，4K。"
                    )
                    # action/pose 视图也继承白背景
                    if card.get("asset_background") in ("white", "纯白"):
                        prompt += " 纯白背景，无环境/无场景。"
                prompt += (
                    f"\n注意：只出现一位角色，禁止出现第二个人或倒影。"
                )
            # 负面 prompt
            np = negative_prompt + ", 畸变, 变形, 模糊, 低质量, 丑陋, 多余肢体"
            if view in std_views:
                np += ", 武器, 刀, 剑, 枪, 道具"

            out_name = f"{slug}_{view}.md"
            out_path = os.path.join(char_dir, out_name)

            if os.path.isfile(out_path) and not force:
                continue

            # 写入 prompt 文件（YAML frontmatter + body）
            ref_path = f"../../images/characters/{name}_{view}.png"
            front_ref = f"../../images/characters/{name}_front.png"
            meta_ref = front_ref if view != "front" and os.path.isfile(os.path.join(project, "images", "characters", f"{name}_front.png")) else ""

            with open(out_path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"size: {char_size}\n")
                f.write(f"negative_prompt: \"{np}\"\n")
                f.write(f"type: character_view\n")
                f.write(f"view: {view}\n")
                if meta_ref:
                    f.write(f"ref_image: \"{meta_ref}\"\n")
                f.write(f"output: \"{ref_path}\"\n")
                f.write("---\n\n")
                f.write(prompt + "\n")

            generated.append(out_path)

    # ── 场景 prompt ──────────────────────────────────────────────
    for card in scenes:
        name = card.get("name", "场景")
        sid = card.get("id", name)
        slug = sid.replace(" ", "_")

        card_style = card.get("aesthetic_style", "")
        combined_style = f"{global_style}，{card_style}" if global_style and card_style else (global_style or card_style or "电影级写实风格")

        description = card.get("description", name)
        emotion = card.get("emotion", "")
        weather = card.get("weather", "")
        time_of_day = card.get("time_of_day", "day")
        time_str = {"day": "白天", "night": "夜晚", "dawn": "黎明", "dusk": "黄昏"}.get(time_of_day, time_of_day)
        mood_str = f"，{emotion}" if emotion else ""
        weather_str = f"，{weather}" if weather else ""

        # 场景图严格定义为"环境/物体特写"，从语义上避免"中景/特写"被模型理解为人脸特写
        # 中景/特写的描述从场景 card 的 description 动态派生，且必须与广角场景保持内容一致
        scene_views = [
            ("广角", "wide angle establishing shot of empty environment, no figures, no creatures"),
            ("中景", f"medium close view of {description}, no living beings, no figures"),
            ("特写", f"zoomed-in close-up of a specific visible element from the wide scene: {description}, extreme detail view, no humans no creatures"),
        ]

        for view, view_desc in scene_views:
            if view == "广角":
                # ── 文生图：广角独立生成 ──
                subject_part = f"{description}"
                scene_part = f"{time_str}场景{mood_str}{weather_str}，纯环境空镜，无人物无生物"
                style_part = combined_style
                lighting_part = card.get("lighting", "自然光照")
                composition_part = view_desc
                quality_part = terms["scene_quality"]
                hierarchy_part = (
                    f"视觉层次：前景为主体场景元素（建筑/瓦砾/地形/天空），中景为{description}，"
                    f"背景为{time_str}{weather_str}环境，"
                    f"光照来自{lighting_part}方向，"
                    f"色彩基调为自然饱和度。"
                )
                prompt = (
                    f"empty scene, {subject_part}，{scene_part}，{style_part}，{lighting_part}，"
                    f"{composition_part}，{quality_part}。"
                    f"{hierarchy_part}。"
                    f"ABSOLUTELY NO HUMANS, no figures, no silhouettes, no faces, no creatures, no living beings anywhere in the frame."
                )
            else:
                # ── 图生图：以广角为参考图 ──
                subject_part = f"{description}"
                style_part = combined_style
                lighting_part = card.get("lighting", "自然光照")
                prompt = (
                    f"[改变要求] 基于广角场景图，改为{view_desc}。构图聚焦环境/物体细节而非人物。\n"
                    f"[保留元素] 保持场景布局、空间关系、物体朝向、光线方向、色彩基调完全一致。\n"
                    f"[新风格/场景] {style_part}，{lighting_part}。\n"
                    f"ABSOLUTELY NO HUMANS, no figures, no silhouettes, no faces, no creatures, no living beings. Camera must focus on inanimate environment details only."
                )
            np = ("person, people, human, character, figure, silhouette, face, portrait, head, body, hand, "
                  "人物, 人, 行人, 角色, 人类, 人群, 人脸, 面部, 身体, 人体, "
                  "人物特写, 半身, 全身, 肖像, 人物剪影, 头部, 手部, 肩膀, "
                  "human presence, person, character, individual, creature, animal, "
                  "wolf, dog, cat, bird, any living being")

            out_path = os.path.join(scene_pdir, f"{slug}_{view}.md")
            if os.path.isfile(out_path) and not force:
                continue

            with open(out_path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"size: {scene_size}\n")
                f.write(f"type: scene_view\n")
                f.write(f"view: {view}\n")
                f.write(f"output: \"../../images/scenes/{slug}_{view}.png\"\n")
                if view != "广角":
                    f.write(f"ref_image: \"../../images/scenes/{slug}_广角.png\"\n")
                f.write(f"negative_prompt: \"{np}\"\n")
                f.write("---\n\n")
                f.write(prompt + "\n")

            generated.append(out_path)

    # ── 辅助资产 prompt（troop_cards） ────────────────────────────
    troops = data.get("troop_cards", [])
    troop_pdir = os.path.join(out_dir, "troops")
    os.makedirs(troop_pdir, exist_ok=True)
    troop_size = "768x768"

    for card in troops:
        name = card.get("name", "兵种")
        slug = name.replace(" ", "_")
        card_style = card.get("aesthetic_style", "")
        combined_style = f"{global_style}，{card_style}" if global_style and card_style else (global_style or card_style or "电影级写实风格")
        appearance = card.get("appearance", "")
        color_scheme = card.get("color_scheme", "")
        dm = card.get("distinctive_mark", "")

        troop_views = [
            ("front", "正面全身照，面向镜头，展示完整装束和形态"),
            ("side", "侧面全身照，展示侧面轮廓和装备"),
            ("back", "背面全身照，展示背面装束"),
        ]

        for view, view_desc in troop_views:
            prompt = (
                f"{combined_style}，"
                f"{appearance}，{color_scheme}，{dm}。"
                f"{view_desc}。完整全身从头到脚包括靴子，白色纯色背景。"
            )
            np = negative_prompt + ", 畸变, 变形, 模糊"

            out_path = os.path.join(troop_pdir, f"{slug}_{view}.md")
            if os.path.isfile(out_path) and not force:
                continue

            ref_path = f"../../images/troops/{slug}_{view}.png"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"size: {troop_size}\n")
                f.write(f"negative_prompt: \"{np}\"\n")
                f.write(f"type: troop_view\n")
                f.write(f"view: {view}\n")
                f.write(f"output: \"{ref_path}\"\n")
                f.write("---\n\n")
                f.write(prompt + "\n")

            generated.append(out_path)

    # ── 视频 prompt（图生视频格式） ─────────────────────────────
    shots = data.get("shots", [])
    aspect_for_video = sc.get("aspect_ratio", "16:9")
    # 通用的运动/稳定描述模板
    motion_templates = {
        "对话": "嘴唇轻微张合说话，面部表情细微变化，肩部有轻微的呼吸起伏，头发微动",
        "动作": "角色动作流畅进行，衣物飘动，肌肉运动自然，背景粒子或尘埃缓慢飘动",
        "静态": "极其轻微的自然呼吸起伏，眼神微微转动，发丝偶尔轻飘，整体画面稳定几乎静止",
    }

    for s in shots:
        sid = s["id"]
        desc = s.get("description", "")
        # 根据描述推断运动类型
        has_dialogue = bool(s.get("dialogue", ""))
        is_action = any(w in desc for w in [
            "战斗", "走", "跳跃", "跃下", "跑", "追逐",
            "转头", "回头", "扭头", "转身", "侧头", "回头", "转头",
            "看向", "望向", "抬头", "低头", "爆炸", "爆发",
            "震动", "晃动", "抖动", "挥舞", "挥动", "举起",
            "倒下", "跪倒", "起身", "站起", "坐下", "后退",
            "前进", "冲锋", "闪避", "跳跃", "腾空", "落下",
            "蹲下", "抚摸", "抱起", "拿起", "抓起", "掏",
            "擦", "裹", "抱", "摸", "张牙舞爪",
        ])
        motion_type = "对话" if has_dialogue else ("动作" if is_action else "静态")
        motion_desc = motion_templates.get(motion_type, motion_templates["静态"])
        
        # ── 对话镜头：指定说话角色 ──
        if motion_type == "对话":
            chars = s.get("characters", [])
            dialogue = s.get("dialogue", "")
            speaker = ""
            if len(chars) == 1:
                speaker = chars[0]
            elif len(chars) > 1:
                # 多角色时尝试从 description 尾段推断谁在说话
                shot_desc = s.get("description", "")
                # 优先: dialogue 开头自称（如"我君无烬"→君无烬、"我叫苏晚"→苏晚）
                for c in chars:
                    base = c.split("（")[0].split("(")[0].strip()
                    if base and f"我{base}" in dialogue:
                        speaker = c
                        break
                # 其次: description 末尾提到谁在做出"说"相关的动作
                if not speaker:
                    for c in chars:
                        base = c.split("（")[0].split("(")[0].strip()
                        if base and base == shot_desc.strip().split(" ")[-1].strip("，。、"):
                            speaker = c
                            break
                # 最后: 第一个非"君无烬"的角色（君无烬是猫或天帝，说话场景较少）
                if not speaker:
                    for c in chars:
                        base = c.split("（")[0].split("(")[0].strip()
                        if base != "君无烬":
                            speaker = c
                            break
                if not speaker:
                    speaker = chars[0]
            if speaker:
                speaker_short = speaker.split("（")[0].split("(")[0].strip()
                motion_desc = motion_desc.replace(
                    "嘴唇轻微张合说话",
                    f"{speaker_short}嘴唇轻微张合说话"
                )
        
        prompt_shot_dir = os.path.join(video_dir, f"video_shot{sid:02d}.md")
        # 图生视频格式：[动画内容] + [保持稳定] + [运镜] + [风格] + [场景描述]
        
        # ── 运镜描述：从 camera 字段（或 shot_type）生成 ──
        cam_field = s.get("camera", "")
        shot_type_field = s.get("shot_type", "")
        # 从 camera 字段提取关键词（如"广角俯拍"→"俯拍广角"）
        camera_desc = ""
        if cam_field:
            camera_desc = f"采用{cam_field}运镜"
        elif shot_type_field:
            # 内联运镜推断（避免循环导入 optimize）
            _CAMERA_DEFAULT = {
                "establishing": "广角远景，镜头缓慢推入",
                "reveal": "中景镜头，缓慢揭示主体",
                "emotional": "近景固定镜头",
                "dialogue": "中景双人或过肩镜头",
                "reaction": "近景特写",
                "flashback": "全景固定镜头，边缘柔光虚化",
                "action": "中景跟拍，轻微晃动",
                "comedy": "中景固定镜头",
                "cliffhanger": "近景推近",
                "slice_of_life": "中景固定镜头",
                "detail": "极端特写",
                "transition": "广角平移镜头",
            }
            cm = _CAMERA_DEFAULT.get(shot_type_field, "")
            if cm:
                camera_desc = f"采用{cm}运镜"
        
        # ── 场景描述：取 description 的最后一段叙事内容 ──
        # optimizer 在 description 前面注入了大量运镜词（"镜头XXX，同时XXX"）
        # 找到最后一个运镜句子的位置，取之后的全部内容作为叙事
        sentences = re.split(r'[，。！？、\s]+', desc)
        _CAMERA_KW = ['镜头', '推近', '拉远', '摇摄', '俯拍', '仰拍', '横移',
                      '平移', '跟拍', '跟随', '晃动', '抖动', '缓缓', '变焦',
                      '环绕', '旋转', '升降', '推入', '推进', '手持',
                      '同时', '随后', '突然']
        last_camera_idx = -1
        for i, s in enumerate(sentences):
            s = s.strip()
            if any(kw in s for kw in _CAMERA_KW):
                last_camera_idx = i
        if last_camera_idx >= 0 and last_camera_idx < len(sentences) - 1:
            clean_desc = '，'.join(sentences[last_camera_idx + 1:]).strip('，。、 ')  # space included for cleanup
            if len(clean_desc) < 10:
                clean_desc = desc
        else:
            clean_desc = desc
        
        style_section = f"整体风格：{global_style}。" if global_style else ""
        camera_section = f"[运镜] {camera_desc}\n" if camera_desc else ""
        prompt = (
            f"以首帧图为基底生成视频动画。\n"
            f"[动画内容] {motion_desc}。\n"
            f"[保持稳定] 保持角色的面部特征、发型、服装、体型完全一致不变，"
            f"场景中的建筑、地面、墙面等静态元素保持固定不动，"
            f"色彩基调、光照方向、构图不变。\n"
            f"{camera_section}"
            f"[风格] {style_section}\n"
            f"[场景描述] {clean_desc}"
        )

        _MANUAL_PROTECT = "手动精修，勿自动覆盖"
        if os.path.isfile(prompt_shot_dir):
            if not force:
                continue
            # --force 模式下仍检查保护标记
            try:
                with open(prompt_shot_dir, encoding="utf-8") as _pf:
                    _first = _pf.read(200)
                if _MANUAL_PROTECT in _first:
                    print(f"     🛡️ {fname}: 有精修保护标记，跳过覆盖")
                    continue
            except Exception:
                pass

        with open(prompt_shot_dir, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"aspect: {aspect_for_video}\n")
            f.write(f"type: video\n")
            f.write(f"shot_id: {sid}\n")
            f.write(f"motion_type: {motion_type}\n")
            f.write("---\n\n")
            f.write(prompt + "\n")
        generated.append(prompt_shot_dir)

    return generated


# ── 首帧图 prompt 模板组装（统一入口） ─────────────────────
# 被 agnes-ai/modules/prompt.py 调用，确保所有 prompt 生成都经过本模块

def build_first_frame_prompt_template(
    model: str,
    ref_count: int,
    edit_instruction: str,
    target_style: str,
    lighting_desc: str,
    scene_info: str = "",
    aspect: str = "16:9",
    global_style: str = "",
) -> str:
    """组装首帧图六段式提示词模板。
    prompt.py 负责提取上下文（角色锚定、场景匹配、编辑指令），
    本函数只做模板组装，确保格式统一。
    """
    terms = _style_terms(global_style) if global_style else {}
    quality_text = terms.get("quality_body", "电影级写实，服装材质细节，光影层次丰富，氛围情绪饱满")
    comp_text = _comp_prefix(aspect, terms.get("style_name", "电影"))
    return (
        f"\n# 推荐模型: {model}\n"
        f"将{ref_count}张参考图合成一张完整画面。\n"
        "\n"
        "## 提示词\n"
        "\n"
        f"{edit_instruction}\n"
        "\n"
        f"[保留元素] 以图1为基底，保持场景布局、空间关系、物体朝向、光线方向、色彩基调完全一致。\n"
        "\n"
        f"[目标风格/场景] {target_style}\n"
        "\n"
        f"[光照] {lighting_desc}{scene_info}\n"
        "\n"
        f"[构图] {comp_text}，角色在画面中的空间位置符合描述。\n"
        "\n"
        f"[画质要求] {quality_text}\n"
    )


# ── 文生图/图生图 结构验证关键词映射 ──
SECTIONS_MAP = {
    "主体": ["男性", "女性", "角色", "人物", "年龄", "岁"],
    "场景/环境": ["背景", "白色纯色背景", "场景", "环境", "废墟", "丛林", "室内", "室外"],
    "风格": ["写实", "电影", "cinematic", "风格", "realistic", "photorealistic"],
    "光照": ["光照", "光", "明", "暗", "阴影", "灯", "sunlight", "lighting"],
    "构图": ["全身", "半身", "特写", "正面", "侧面", "背面", "视角", "镜头", "广角"],
    "质量要求": ["4K", "8K", "电影感", "高清", "超高清", "细节", "质感", "高视觉密度"],
}


def validate_prompts(project: str) -> list[dict]:
    """验证所有已生成的 prompt 文件（角色/场景/辅助资产/首帧图/视频）。返回 issues 列表。"""
    issues = []
    issues += _validate_character_prompts(project)
    issues += _validate_scene_prompts(project)
    issues += _validate_troop_prompts(project)
    issues += _validate_first_frame_prompts(project)
    issues += _validate_video_prompts(project)
    return issues


def _validate_character_prompts(project: str) -> list[dict]:
    """验证角色 prompt 文件（文生图结构：主体+场景+风格+光照+构图+质量）。"""
    issues = []
    prompt_dir = os.path.join(project, "prompts", "characters")
    if not os.path.isdir(prompt_dir):
        return [{"priority": "P2", "msg": "角色 prompt 目录不存在（运行 build-prompts 后生成）", "location": "prompts/characters"}]

    for fname in os.listdir(prompt_dir):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(prompt_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()

        frontmatch = re.match(r'^---\n(.*?)\n---\n\n(.*)', content, re.DOTALL)
        if not frontmatch:
            issues.append({"priority": "P0", "msg": f"prompts/characters/{fname}: 缺少 YAML frontmatter", "location": fname})
            continue

        meta_text, body = frontmatch.groups()
        if "model:" not in meta_text:
            issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少 model 声明", "location": fname})
        if "size:" not in meta_text:
            issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少 size 声明", "location": fname})
        if "negative_prompt:" not in meta_text:
            issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少 negative_prompt", "location": fname})

        view = fname.rsplit("_", 1)[1].replace(".md", "") if "_" in fname else ""
        if view == "front":
            # front → 文生图验证
            SECTIONS = ["主体", "场景/环境", "风格", "光照", "构图", "质量要求"]
            missing = [s for s in SECTIONS if not any(kw in body for kw in SECTIONS_MAP[s])]
            for m in missing:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: front 文生图缺少{m}段", "location": fname})
            if "男性" not in body and "女性" not in body and "角色" not in body:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少性别声明", "location": fname})
            if "纯白背景" not in body and "#FFFFFF" not in body and "白色纯色" not in body:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 标准视图缺少白背景指令", "location": fname})
            if "无武器" not in body:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 标准视图缺少无武器指令", "location": fname})
        else:
            # face/side/back/action/pose → 图生图验证
            I2I_KWS = {
                "改变要求": ["参考图", "改为", "为基础", "改为"],
                "保留元素": ["保持", "保留", "一致", "相同"],
                "新风格": ["写实", "电影", "风格", "cinematic"],
            }
            for sec_name, kws in I2I_KWS.items():
                if not any(kw in body for kw in kws):
                    issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 图生图缺少{sec_name}", "location": fname})
            if view in ("face", "side", "back") and "参考图" not in body:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少参考图引用", "location": fname})
        if "电影感" not in body and "4K" not in body:
            issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 缺少质量关键词（4K/电影感）", "location": fname})
        # 文生图六段式结构验证
        SECTIONS = ["主体", "场景/环境", "风格", "光照", "构图", "质量要求"]
        missing = [s for s in SECTIONS if not any(kw in body for kw in SECTIONS_MAP[s])]
        if missing:
            for m in missing:
                issues.append({"priority": "P1", "msg": f"prompts/characters/{fname}: 文生图缺少{m}段", "location": fname})
    return issues


def _validate_scene_prompts(project: str) -> list[dict]:
    """验证场景 prompt 文件。"""
    issues = []
    scene_dir = os.path.join(project, "prompts", "scenes")
    if not os.path.isdir(scene_dir):
        return []  # 场景 prompt 可选
    count = len([f for f in os.listdir(scene_dir) if f.endswith(".md")])
    issues.append({"priority": "P2", "msg": f"场景 prompt 目录: {count} 个文件", "location": "prompts/scenes"})
    # 验证内容
    for fname in os.listdir(scene_dir):
        if not fname.endswith(".md"): continue
        path = os.path.join(scene_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        body_start = content.find("\n---\n\n")
        body = content[body_start + 5:] if body_start >= 0 else content
        body_upper = body.upper()
        if ("无任何人物" not in body and "禁止出现" not in body
            and "NO HUMANS" not in body_upper and "NO PEOPLE" not in body_upper
            and "NO FIGURES" not in body_upper):
            issues.append({"priority": "P1", "msg": f"prompts/scenes/{fname}: 缺少\"无人物\"指令", "location": fname})
    return issues


def _validate_first_frame_prompts(project: str) -> list[dict]:
    """验证首帧图 prompt 文件（prompts/storyboard/shot*.md）是否符合六段式格式。"""
    issues = []
    prompt_dir = os.path.join(project, "prompts", "storyboard")
    if not os.path.isdir(prompt_dir):
        return []

    # 加载 script.json 获取 shot 角色信息（用于语义检查）
    script_path = os.path.join(project, "script.json")
    script_data = None
    all_char_traits = {}
    shot_characters_map = {}
    if os.path.isfile(script_path):
        with open(script_path, encoding="utf-8") as f:
            script_data = json.load(f)
        for c in script_data.get("character_cards", []):
            name = c.get("name", "")
            # 收集每个角色的 distinctive_mark（如果无distinctive_mark，从appearance提取部分）
            mark = c.get("distinctive_mark", "")
            if not mark:
                app = c.get("appearance", {})
                if isinstance(app, dict):
                    face = app.get("face", "")
                    hair = app.get("hair", "")
                    clothing = app.get("armor/clothing", "")
                    mark = f"{hair}，{face}" if hair and face else ""
            all_char_traits[name] = c if mark else None  # 保留角色名即可
        for s in script_data.get("shots", []):
            shot_characters_map[s["id"]] = s.get("characters", [])
    # 预缓存每个 shot 的 description（供语义检查用）
    shot_text_cache = {}
    if script_data:
        for s in script_data.get("shots", []):
            shot_text_cache[s["id"]] = (s.get("description", "") + " " +
                                        s.get("prompt", "") + " " +
                                        s.get("dialogue", ""))

    shot_files = sorted([f for f in os.listdir(prompt_dir) if re.match(r'shot\d+_image\.md$', f)])
    if not shot_files:
        issues.append({"priority": "P2", "msg": "首帧图 prompt 文件不存在（运行 build-first-frames 后生成）",
                        "location": "prompts/storyboard/shot*_image.md"})
        return issues

    # 首帧图必须包含的六段格式
    REQUIRED_SECTIONS = [
        ("## 提示词", "缺少 ## 提示词 段"),
        ("[编辑指令]", "缺少 [编辑指令] 段"),
        ("[目标风格/场景]", "缺少 [目标风格/场景] 段"),
        ("[光照]", "缺少 [光照] 段"),
        ("[构图]", "缺少 [构图] 段"),
        ("[画质要求]", "缺少 [画质要求] 段"),
    ]
    # 推荐模型行
    MODEL_RE = re.compile(r'^# 推荐模型:\s*\S+', re.MULTILINE)

    for fname in shot_files:
        path = os.path.join(prompt_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()

        # 提取 body（frontmatter 之后）
        body_start = content.find("\n---\n\n")
        body = content[body_start + 5:] if body_start >= 0 else content

        shot_id = re.search(r'shot(\d+)_', fname).group(1) if re.search(r'shot(\d+)_', fname) else "?"
        loc = fname

        # 验证推荐模型行
        if not MODEL_RE.search(body):
            issues.append({"priority": "P1", "msg": f"{loc}: 缺少 '# 推荐模型:' 行", "location": loc})

        # 验证参考图数行
        if "张参考图合成" not in body and "参考图" not in body:
            issues.append({"priority": "P1", "msg": f"{loc}: 缺少参考图说明", "location": loc})

        # 验证六段格式
        for section_marker, error_msg in REQUIRED_SECTIONS:
            if section_marker not in body:
                issues.append({"priority": "P0", "msg": f"{loc}: {error_msg}", "location": loc})

        # 图生图结构验证：[改变要求] + [新风格/场景] + [添加/移除] + [保留]
        I2I_SECTIONS = {
            "改变要求": ["将", "改为", "变成", "以图1", "参考图"],
            "新风格/场景": ["编辑指令", "目标风格", "场景"],
            "添加或移除": ["添加", "加入", "移除", "删除", "增加"],
            "保留元素": ["保持", "保留", "不变", "原始"],
        }
        for sec_name, kws in I2I_SECTIONS.items():
            if not any(kw in body for kw in kws):
                issues.append({"priority": "P1", "msg": f"{loc}: 图生图缺少{sec_name}描述", "location": loc})

        # 验证构图格式
        comp_match = re.search(r'\[构图\](.*?)(?=\n\[|\Z)', body, re.DOTALL)
        if comp_match:
            comp_text = comp_match.group(1).strip()
            if "竖屏" not in comp_text and "横屏" not in comp_text and "电影" not in comp_text:
                issues.append({"priority": "P2", "msg": f"{loc}: [构图] 段缺少画幅说明（竖屏/横屏）", "location": loc})

        # 语义验证：检查 [目标风格/场景] 段是否混入了无关角色的特征词
        if script_data and int(shot_id) in shot_characters_map:
            expected_chars = shot_characters_map[int(shot_id)]
            # 收集画面上不应出现的角色特征关键词
            alien_traits = []
            for c_name, c_data in all_char_traits.items():
                if not c_name or c_name in expected_chars:
                    continue
                # 检查 c_name 是否在 shot 描述中显式提到
                desc = shot_text_cache.get(int(shot_id), "")
                name_in_desc = c_name and c_name in desc
                if name_in_desc:
                    continue  # 描述中提到了名字，角色的特征出现是合理的
                # 检查这个角色的 distinctive_mark 是否出现在 body 中
                mark = c_data.get("distinctive_mark", "") if c_data else ""
                if mark and mark in body:
                    alien_traits.append(f"「{c_name}」的特征: {mark[:20]}")
                # 检查 appearance 中的关键词
                app = c_data.get("appearance", {}) if c_data else {}
                if isinstance(app, dict):
                    for key in ("hair", "armor/clothing", "face"):
                        val = app.get(key, "")
                        for kw in val.split():
                            if len(kw) >= 3 and kw in body and kw not in desc:
                                alien_traits.append(f"「{c_name}」的{key}: {kw}")
                                break
            if alien_traits:
                issues.append({
                    "priority": "P1",
                    "msg": f"{loc}: [目标风格/场景] 段含无关角色特征 ({'; '.join(alien_traits[:3])})——应只包含当前 shot 角色 {expected_chars} 的特征",
                    "location": loc
                })

        # 语义验证：检查描述中提到的角色是否在 shot.characters 中缺失
        if script_data and int(shot_id) in shot_characters_map:
            expected_chars = shot_characters_map[int(shot_id)]
            desc = shot_text_cache.get(int(shot_id), "")
            # 检查每个角色的名称/别名是否出现在描述中但不在 character 列表中
            for c_name, c_data in all_char_traits.items():
                if not c_name or c_name in expected_chars:
                    continue
                # 提取角色的短名称/别名（括号前的部分）
                short_name = c_name.split("（")[0] if "（" in c_name else c_name
                # 提取括号内的特征描述
                bracket_content = c_name[c_name.find("（")+1:c_name.find("）")] if "（" in c_name else ""
                # 在 description 中搜索
                name_in_desc = (c_name in desc or short_name in desc or 
                               (bracket_content and bracket_content in desc))
                if name_in_desc:
                    issues.append({
                        "priority": "P1",
                        "msg": f"{loc}: 描述提到了「{c_name}」({short_name})但 shot.characters 未包含该角色——应添加至 characters 列表以确保参考图和特征正确",
                        "location": loc
                    })

    return issues


def _validate_video_prompts(project: str) -> list[dict]:
    """验证视频 prompt 文件（prompts/videos/video_shot*.md）。"""
    issues = []
    prompt_dir = os.path.join(project, "prompts", "videos")
    if not os.path.isdir(prompt_dir):
        return []

    video_files = sorted([f for f in os.listdir(prompt_dir)
                          if re.match(r'video_shot\d+\.md$', f)])
    if not video_files:
        issues.append({"priority": "P2", "msg": "视频 prompt 文件不存在（提交视频后生成）",
                        "location": "prompts/videos/video_shot*.md"})
        return issues

    for fname in video_files:
        path = os.path.join(prompt_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()

        body_start = content.find("\n---\n\n")
        body = content[body_start + 5:] if body_start >= 0 else content

        # 图生视频格式：[动画内容] + [保持稳定] + [场景描述]
        if "[动画内容]" not in body:
            issues.append({"priority": "P0", "msg": f"{fname}: 缺少 [动画内容] 段", "location": fname})
        if "[保持稳定]" not in body:
            issues.append({"priority": "P0", "msg": f"{fname}: 缺少 [保持稳定] 段", "location": fname})
        if "[场景描述]" not in body:
            issues.append({"priority": "P1", "msg": f"{fname}: 缺少 [场景描述] 段", "location": fname})
        # 检查稳定性关键词
        if "[保持稳定]" in body:
            s = body.split("[保持稳定]")[1]
            txt = s.split("\n[")[0] if "\n[" in s else s
            if not any(kw in txt for kw in ["保持", "一致", "固定", "不变"]):
                issues.append({"priority": "P1", "msg": f"{fname}: [保持稳定] 缺少保持关键词", "location": fname})
        # 检查动画描述长度
        if "[动画内容]" in body:
            s = body.split("[动画内容]")[1]
            txt = s.split("\n[")[0] if "\n[" in s else s
            if len(txt.strip()) < 5:
                issues.append({"priority": "P1", "msg": f"{fname}: [动画内容] 描述过短", "location": fname})
        if "model:" not in content[:200]:
            issues.append({"priority": "P1", "msg": f"{fname}: 缺少推荐模型声明", "location": fname})

        # 检查 motion_type 与描述是否匹配
        m = re.search(r'^motion_type:\s*(.+)$', content[:200], re.MULTILINE)
        if m:
            mt = m.group(1).strip()
            # 取 [场景描述] 中的内容来检测动作词
            desc_part = ""
            if "[场景描述]" in body:
                ds = body.split("[场景描述]")[1]
                desc_part = ds.split("\n")[0] if "\n" in ds else ds
            action_kw = ["转头","回头","扭头","转身","侧头","抬头","低头",
                         "战斗","跑","跳跃","追逐","爆炸","跃下","走",
                         "看向","望向","举起","倒下","震动","晃动","挥舞",
                         "挥动","冲锋","闪避","腾空","落下","蹲下","起身"]
            has_action_verb = any(kw in desc_part for kw in action_kw)
            if has_action_verb and mt == "静态":
                issues.append({"priority": "P1",
                    "msg": f"{fname}: motion_type=静态 但场景描述含动作词，可能应为动作或对话",
                    "location": fname})

        # ── 内容准确性检查（需 script.json 上下文） ──────────
        script_path = os.path.join(project, "script.json")
        if not os.path.isfile(script_path):
            continue
        try:
            with open(script_path, encoding="utf-8") as _sf:
                script_data = json.load(_sf)
        except Exception:
            continue

        # 提取 shot_id
        m_sid = re.match(r'video_shot(\d+)\.md$', fname)
        if not m_sid:
            continue
        shot_id = int(m_sid.group(1))
        shot = next((s for s in script_data.get("shots", []) if s.get("id") == shot_id), None)
        if not shot:
            continue
        shot_desc = shot.get("description", "")
        chars = shot.get("characters", []) or []
        dialogue = shot.get("dialogue", "")

        # 1. 角色覆盖检查：prompt 场景描述中的角色名 vs characters 字段
        char_names = [c.get("name", "") for c in script_data.get("character_cards", []) if c.get("name")]
        desc_part = ""
        if "[场景描述]" in body:
            ds = body.split("[场景描述]")[1]
            desc_part = ds.split("\n[")[0] if "\n[" in ds else ds
        anim_part = ""
        if "[动画内容]" in body:
            an = body.split("[动画内容]")[1]
            anim_part = an.split("\n[")[0] if "\n[" in an else an
        prompt_text = desc_part + " " + anim_part

        missing_chars = [cn for cn in chars if cn and cn not in prompt_text and
                         cn.split("（")[0].split("(")[0].strip() not in prompt_text]
        if missing_chars:
            issues.append({"priority": "P1",
                "msg": f"{fname}: 提示词未覆盖角色 {missing_chars}（characters={chars}）",
                "location": fname})

        # 2. 动作覆盖检查：description 的动作词 vs [动画内容]
        action_kw_all = ["转头","回头","扭头","转身","侧头","抬头","低头",
                         "战斗","跑","跳跃","追逐","爆炸","跃下","走",
                         "看向","望向","举起","倒下","震动","晃动","挥舞",
                         "挥动","冲锋","闪避","腾空","落下","蹲下","起身",
                         "凝视","注视","盯着","瞄准"]
        desc_actions = [kw for kw in action_kw_all if kw in shot_desc]
        prompt_actions = [kw for kw in desc_actions if kw in anim_part]
        missing_actions = [kw for kw in desc_actions if kw not in prompt_actions]
        if missing_actions:
            issues.append({"priority": "P1",
                "msg": f"{fname}: [动画内容] 缺少动作词 {missing_actions}",
                "location": fname})

        # 3. 场景一致性检查：description 的场景词 vs [场景描述]
        scene_kw_all = ["废墟","战场","丛林","森林","篝火","营地","夜空",
                        "硝烟","断壁","残垣","砖墙","弹孔","碎石","瓦砾",
                        "树木","环绕","空地","燃烧","火星","飞溅"]
        desc_scene = [kw for kw in scene_kw_all if kw in shot_desc]
        prompt_scene = [kw for kw in desc_scene if kw in desc_part]
        if len(desc_scene) > 0 and len(prompt_scene) < len(desc_scene) * 0.5:
            missing_scene = [kw for kw in desc_scene if kw not in prompt_scene]
            issues.append({"priority": "P1",
                "msg": f"{fname}: [场景描述] 与 description 场景词不一致，缺失 {missing_scene[:5]}",
                "location": fname})

        # 4. 台词存在检查
        if dialogue and "台词:" not in prompt_text and dialogue[:10] not in prompt_text:
            issues.append({"priority": "P1",
                "msg": f"{fname}: 缺少台词内容（{dialogue[:20]}）",
                "location": fname})

        # 5. 实名化检查：prompt 中有模糊计数词
        count_kw = ["一人","两人","二人","三人","四人","五人",
                    "一个人","两个人","三个人","四个人","五个人"]
        found_count = [kw for kw in count_kw if kw in prompt_text]
        if found_count and chars:
            issues.append({"priority": "P1",
                "msg": f"{fname}: 提示词使用模糊词「{found_count[0]}」应替换为角色名 {chars}",
                "location": fname})

    return issues


def _validate_troop_prompts(project: str) -> list[dict]:
    """验证辅助资产 prompt 文件（prompts/troops/*.md）。"""
    issues = []
    troop_dir = os.path.join(project, "prompts", "troops")
    if not os.path.isdir(troop_dir):
        # 无 troop 目录不是问题 — 可能项目不需要辅助资产
        # 但如果有 troops cards 却没有 prompt 文件，就是问题
        script_path = os.path.join(project, "script.json")
        if os.path.isfile(script_path):
            try:
                with open(script_path, encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("troop_cards"):
                    issues.append({"priority": "P1", "msg": "存在 troop_cards 但 prompts/troops/ 目录不存在",
                                    "location": "prompts/troops"})
            except Exception:
                pass
        return issues

    files = [f for f in os.listdir(troop_dir) if f.endswith(".md")]
    if not files:
        return issues

    issues.append({"priority": "P2", "msg": f"辅助资产 prompt 目录: {len(files)} 个文件", "location": "prompts/troops"})
    for fname in files:
        path = os.path.join(troop_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        body_start = content.find("\n---\n\n")
        body = content[body_start + 5:] if body_start >= 0 else content
        if "白色纯色背景" not in body and "纯白" not in body:
            issues.append({"priority": "P2", "msg": f"prompts/troops/{fname}: 缺少白色背景指令", "location": fname})
        if "完整全身" not in body and "从头到脚" not in body:
            issues.append({"priority": "P2", "msg": f"prompts/troops/{fname}: 缺少全身展示指令", "location": fname})

    return issues


# ── 自动修复 ──────────────────────────────────────────────────

def _fix_tag_in_body(body: str, tag: str, default_content: str) -> str:
    """如果 body 中缺少 [tag] 段，在 body 末尾追加。有则不改。"""
    if f"[{tag}]" not in body:
        body = body.rstrip() + f"\n[{tag}] {default_content}\n"
    return body


def _ensure_line(body: str, prefix: str, default: str) -> str:
    """如果 body 中没有指定前缀的行，追加。"""
    for line in body.split("\n"):
        if line.strip().startswith(prefix):
            return body
    return body.rstrip() + f"\n{prefix} {default}\n"


def _fix_first_frame_file(path: str, shot_desc: str = "", aspect: str = "16:9") -> int:
    """修复单个首帧图 prompt 文件，返回修复的项目数。"""
    fixes = 0
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 frontmatter 和 body
    m = re.match(r'^(---\n.*?\n---\n\n)(.*)', content, re.DOTALL)
    if not m:
        return 0
    frontmatter, body = m.groups()

    body = _fix_tag_in_body(body, "目标风格/场景", shot_desc or "场景描述")
    body = _fix_tag_in_body(body, "光照", "自然光照，电影级光影表现")
    body = _fix_tag_in_body(body, "构图", f"{'竖屏' if '9:16' in aspect else '横屏'}电影构图")
    body = _fix_tag_in_body(body, "画质要求", "电影级写实，服装材质细节，光影层次丰富，氛围情绪饱满")
    body = _fix_tag_in_body(body, "编辑指令", "参考图合成完整画面")

    if "## 提示词" not in body:
        body = "## 提示词\n\n" + body
        fixes += 1

    if "参考图" not in body:
        body = body.replace("## 提示词", "将参考图合成一张完整画面。\n\n## 提示词", 1)
        fixes += 1

    # 写回
    new_content = frontmatter + body
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixes += 1
    return fixes


def fix_first_frame_prompts(project: str, shot_issues: list[dict]) -> int:
    """根据验证结果自动修复首帧图 prompt 文件。返回修复的文件数。"""
    prompt_dir = os.path.join(project, "prompts", "storyboard")
    if not os.path.isdir(prompt_dir):
        return 0

    fixed = 0
    script_path = os.path.join(project, "script.json")
    script_data = {}
    if os.path.isfile(script_path):
        try:
            with open(script_path, encoding="utf-8") as f:
                script_data = json.load(f)
        except Exception:
            pass
    aspect = script_data.get("script", {}).get("aspect_ratio", "16:9")

    # 收集需要修复的文件
    affected = set()
    for issue in shot_issues:
        loc = issue.get("location", "")
        if loc.startswith("shot") and "_image" in loc:
            affected.add(os.path.join(prompt_dir, loc))

    for path in sorted(affected):
        if not os.path.isfile(path):
            continue
        # 从文件名提取 shot_id
        m = re.search(r'shot(\d+)_', os.path.basename(path))
        shot_desc = ""
        if m and script_data:
            sid = int(m.group(1))
            for s in script_data.get("shots", []):
                if s.get("id") == sid:
                    shot_desc = s.get("description", "")
                    break
        n = _fix_first_frame_file(path, shot_desc=shot_desc, aspect=aspect)
        if n:
            fixed += 1
            print(f"  ✅ 修复: {os.path.relpath(path, project)} ({n} 项)", flush=True)

    return fixed


def fix_video_prompts(project: str, video_issues: list[dict]) -> int:
    """根据验证结果自动修复视频 prompt 文件。返回修复的文件数。"""
    prompt_dir = os.path.join(project, "prompts", "videos")
    if not os.path.isdir(prompt_dir):
        return 0

    # 从 script.json 读取完整数据
    script_path = os.path.join(project, "script.json")
    aspect = "16:9"
    script_data = {}
    if os.path.isfile(script_path):
        try:
            with open(script_path, encoding="utf-8") as f:
                script_data = json.load(f)
            aspect = script_data.get("script", {}).get("aspect_ratio", "16:9")
        except Exception:
            pass

    fixed = 0
    affected = set()
    for issue in video_issues:
        loc = issue.get("location", "")
        if loc.startswith("video_shot") and loc.endswith(".md"):
            affected.add(os.path.join(prompt_dir, loc))

    char_names = [c.get("name", "") for c in script_data.get("character_cards", []) if c.get("name")]
    count_kw_rep = {"一人": 1, "两人": 2, "二人": 2, "三人": 3, "四人": 4, "五人": 5}
    action_kw_all = ["转头","回头","扭头","转身","侧头","抬头","低头",
                     "战斗","跑","跳跃","追逐","爆炸","跃下","走",
                     "看向","望向","举起","倒下","震动","晃动","挥舞",
                     "挥动","冲锋","闪避","腾空","落下","蹲下","起身",
                     "凝视","注视","盯着","瞄准"]

    for path in sorted(affected):
        if not os.path.isfile(path):
            continue
        # 提取 shot_id
        import re as _re_mod
        m = _re_mod.search(r'video_shot(\d+)\.md$', os.path.basename(path))
        if not m:
            continue
        shot_id = int(m.group(1))
        shot = next((s for s in script_data.get("shots", []) if s.get("id") == shot_id), None)
        if not shot:
            continue
        shot_desc = shot.get("description", "")
        chars = shot.get("characters", []) or []
        dialogue = shot.get("dialogue", "")

        with open(path, encoding="utf-8") as f:
            content = f.read()

        body_start = content.find("\n---\n\n")
        body = content[body_start + 5:] if body_start >= 0 else content

        fixes_local = 0

        # 1. 角色缺失：在 [场景描述] 补缺失角色名
        if chars:
            desc_part = ""
            if "[场景描述]" in body:
                ds = body.split("[场景描述]")[1]
                desc_part = ds.split("\n[")[0] if "\n[" in ds else ds
            anim_part = ""
            if "[动画内容]" in body:
                an = body.split("[动画内容]")[1]
                anim_part = an.split("\n[")[0] if "\n[" in an else an
            prompt_text = desc_part + " " + anim_part
            missing_chars = [cn for cn in chars if cn and cn not in prompt_text and
                             cn.split("（")[0].split("(")[0].strip() not in prompt_text]
            if missing_chars and "[场景描述]" in body:
                old = body.split("[场景描述]")[1].split("\n[")[0]
                add_names = "、".join(missing_chars)
                new_part = f"{old}，{add_names}"
                body = body.replace(old, new_part, 1)
                fixes_local += 1

        # 2. 动作缺失：在 [动画内容] 补缺失动作词
        if "[动画内容]" in body and shot_desc:
            an = body.split("[动画内容]")[1]
            anim_txt = an.split("\n[")[0] if "\n[" in an else an
            desc_actions = [kw for kw in action_kw_all if kw in shot_desc]
            missing_acts = [kw for kw in desc_actions if kw not in anim_txt]
            if missing_acts:
                old_anim = anim_txt
                new_anim = anim_txt.rstrip("。") + "，" + "、".join(missing_acts) + "。"
                body = body.replace("[动画内容]" + old_anim, "[动画内容]" + new_anim, 1)
                fixes_local += 1

        # 3. 台词缺失：在 [场景描述] 补台词
        if dialogue:
            if "台词:" not in body and dialogue[:10] not in body:
                if "[场景描述]" in body:
                    old = body.split("[场景描述]")[1].split("\n[")[0]
                    new_part = f"{old}，台词: {dialogue}"
                    body = body.replace(old, new_part, 1)
                    fixes_local += 1

        # 4. 模糊计数词替换
        if chars:
            prompt_text_full = body
            for ckw, cnum in count_kw_rep.items():
                if ckw not in prompt_text_full:
                    continue
                if len(chars) == cnum:
                    short_names = []
                    for cn in chars:
                        base = cn.split("（")[0].split("(")[0].strip()
                        short_names.append(base if base else cn)
                    if len(short_names) == 2:
                        replacement = f"{short_names[0]}和{short_names[1]}"
                    else:
                        replacement = "、".join(short_names[:-1]) + f"和{short_names[-1]}"
                    body = body.replace(ckw, replacement, 1)
                    fixes_local += 1
                    break

        if fixes_local > 0:
            frontmatter = content[:body_start + 5] if body_start >= 0 else ""
            new_content = frontmatter + body
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed += 1
            print(f"  ✅ 修复视频 prompt: {os.path.basename(path)} ({fixes_local} 项)", flush=True)

    return fixed


def fix_character_prompts(project: str, char_issues: list[dict]) -> int:
    """根据验证结果自动修复角色 prompt 文件。返回修复的文件数。"""
    prompt_dir = os.path.join(project, "prompts", "characters")
    if not os.path.isdir(prompt_dir):
        return 0
    fixed = 0
    affected = set()
    for issue in char_issues:
        loc = issue.get("location", "")
        if "characters/" in loc or loc.startswith("prompts/characters/"):
            fname = loc.split("/")[-1]
            affected.add(os.path.join(prompt_dir, fname))
    SECTIONS_FIX = {
        "主体": "[主体]\n",
        "场景/环境": "[场景/环境]\n",
        "风格": "[风格] 写实风格\n",
        "光照": "[光照] 自然光照\n",
        "构图": "[构图] 正面半身构图\n",
        "质量要求": "[质量要求] 4K 高清，电影感\n",
    }
    for path in sorted(affected):
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            content = f.read()
        body_start = content.find("\n---\n\n")
        if body_start < 0:
            continue
        body = content[body_start + 5:]
        additions = []
        for sec_name, template in SECTIONS_FIX.items():
            if not any(kw in body for kw in SECTIONS_MAP.get(sec_name, [sec_name])):
                additions.append(template)
        if additions:
            content += "\n" + "".join(additions)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            fixed += 1
            print(f"  ✅ 修复: prompts/characters/{os.path.basename(path)} ({len(additions)} 项)", flush=True)
    return fixed


def fix_scene_prompts(project: str, scene_issues: list[dict]) -> int:
    """根据验证结果自动修复场景 prompt 文件。"""
    prompt_dir = os.path.join(project, "prompts", "scenes")
    if not os.path.isdir(prompt_dir):
        return 0
    fixed = 0
    affected = set()
    for issue in scene_issues:
        loc = issue.get("location", "")
        if "scenes/" in loc or loc.startswith("prompts/scenes/"):
            fname = loc.split("/")[-1]
            affected.add(os.path.join(prompt_dir, fname))
    for path in sorted(affected):
        if not os.path.isfile(path):
            continue
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n[画质要求] 4K 高清，电影级画质\n")
        fixed += 1
        print(f"  ✅ 修复: prompts/scenes/{os.path.basename(path)} (1 项)", flush=True)
    return fixed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--force", action="store_true", help="覆盖已存在的 prompt 文件")
    parser.add_argument("--validate-only", action="store_true", help="仅验证不生成")
    parser.add_argument("--fix", action="store_true", help="根据验证结果自动修复 prompt 文件")
    parser.add_argument("--fix-type", default="first_frame", choices=["first_frame", "video"],
                        help="修复类型（default: first_frame）")
    parser.add_argument("--max-retries", type=int, default=3, help="最大修复轮数（default: 3）")
    args = parser.parse_args()

    if args.fix:
        # 多轮修复：验证 → 修复 → 再验证直到无 P0
        max_rounds = args.max_retries
        for r in range(1, max_rounds + 1):
            issues = validate_prompts(args.project)
            p0 = [i for i in issues if i["priority"] == "P0"]
            p1 = [i for i in issues if i["priority"] == "P1"]
            if not p0:
                print(f"  ✅ 第{r}轮: P0=0 P1={len(p1)} — 无需要修复项")
                break

            # 按类型选择修复
            if args.fix_type == "first_frame":
                fixed = fix_first_frame_prompts(args.project, p0 + p1)
            else:
                fixed = fix_video_prompts(args.project, p0 + p1)

            if not fixed:
                print(f"  ⚠️ 第{r}轮: 无法自动修复的 P0 ({len(p0)} 个)，跳过")
                for i in p0:
                    icon = {"P0": "🔴", "P1": "🟡", "P2": "💡"}.get(i["priority"], "❓")
                    print(f"    {icon} {i['msg']}")
                break

            if r == max_rounds:
                print(f"  ⚠️ 达最大轮数 {max_rounds}")
        sys.exit(0 if not any(i["priority"] == "P0" for i in validate_prompts(args.project)) else 1)

    if args.validate_only:
        issues = validate_prompts(args.project)
        for i in issues:
            icon = {"P0": "🔴", "P1": "🟡", "P2": "💡"}.get(i["priority"], "❓")
            print(f"  {icon} [{i['priority']}] {i['msg']}")
        p0 = sum(1 for i in issues if i["priority"] == "P0")
        p1 = sum(1 for i in issues if i["priority"] == "P1")
        print(f"  ── P0={p0} P1={p1} P2={len(issues)-p0-p1}")
        sys.exit(0 if p0 == 0 else 1)

    # 正常模式：构建 + 验证
    files = build_asset_prompts(args.project, force=args.force)
    print(f"  ✅ 生成 {len(files)} 个 prompt 文件:")
    for f in files:
        print(f"     {os.path.relpath(f, args.project)}")
