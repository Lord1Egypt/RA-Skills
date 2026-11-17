"""提示词模板生成与段提取拼接。"""
import json, os, re, sys
from datetime import datetime

from config import _log, _resolve_generation_refs, get_agnes_default_model

# 将 script-optimizer 加入 import 路径（正常的 import，不用 importlib）
_PROMPT_BUILDER_DIR = os.path.join(
    os.path.dirname(__file__),  # modules/
    "..", "..", "..", "..",    # skills/
    "script-optimizer", "scripts"
)
_PROMPT_BUILDER_DIR = os.path.normpath(_PROMPT_BUILDER_DIR)
if os.path.isdir(_PROMPT_BUILDER_DIR) and _PROMPT_BUILDER_DIR not in sys.path:
    sys.path.insert(0, _PROMPT_BUILDER_DIR)

try:
    from prompt_builder import build_first_frame_prompt_template
except ImportError:
    # fallback：加载失败时使用本地内联版本（不应发生）
    def build_first_frame_prompt_template(model, ref_count, edit_instruction,
                                           target_style, lighting_desc,
                                           scene_info="", aspect="16:9",
                                           global_style=""):
        # 风格感知：global_style 够丰富则直接复用（LLM 生成的质量描述比 f-string 准）
        import re
        m = re.match(r'(.+?)(?:风|级|系|派)', global_style)
        prefix = m.group(1) if m else "电影"
        quality = global_style if len(global_style) >= 15 else f"{prefix}级画质，色彩鲜明，细节丰富"
        comp = f"{'竖屏' if '9:16' in aspect else '横屏'}{prefix}风构图"
        return (
            f"\n# 推荐模型: {model}\n将{ref_count}张参考图合成一张完整画面。\n\n"
            "## 提示词\n\n"
            f"{edit_instruction}\n\n"
            f"[保留元素] 以图1为基底，保持场景布局、空间关系、物体朝向、光线方向、色彩基调完全一致。\n\n"
            f"[目标风格/场景] {target_style}\n\n"
            f"[光照] {lighting_desc}{scene_info}\n\n"
            f"[构图] {comp}，角色在画面中的空间位置符合描述。\n\n"
            f"[画质要求] {quality}\n"
        )

def _generate_prompt_template(shot: dict, ff: dict, script_data: dict | None = None) -> str:
    """根据 shot 信息和脚本资产生成六段式提示词模板。"""
    desc = shot.get("description", "")
    refs = ff.get("ref_images", [])
    ref_count = len(refs)
    model = ff.get("model", "agnes-image-2.0-flash")
    # 如果是 agnes provider 且 model 是默认值，尝试从 script first_frame_model 获取
    if model == "agnes-image-2.0-flash" and script_data:
        sc = script_data.get("script", {})
        frm = sc.get("first_frame_model", "")
        if frm:
            model = frm
    is_v2_1 = "2.1" in model

    # === 自动从 character_cards 提取角色特征（确保跨 shot 一致性） ===
    # 根因：参考图（小段_front.png）有围巾，但 character_cards 的 distinctive_mark/armor 没写
    # 改法：从 character_cards 提取 distinctive_mark + style_keywords 注入到每个 shot 的 [目标风格/场景]
    # 保证每个 shot 都强制描述角色特征（避免 AI 忽视参考图的标志性特征）
    # 重要修复：只提取**当前 shot 涉及的角色**的特征，不是所有角色
    char_anchor = ""
    if script_data:
        ccards = script_data.get("character_cards", [])
        if ccards:
            # 从 shot.characters 列表获取本 shot 涉及的角色
            shot_chars = shot.get("characters", []) or []
            # 匹配规则：在 shot 描述/对话中出现的角色名也加入
            shot_text = (shot.get("description", "") + " " +
                         shot.get("prompt", "") + " " +
                         shot.get("dialogue", "") + " " +
                         " ".join(shot.get("video_prompts", [])) if isinstance(shot.get("video_prompts"), list) else "")
            parts = []
            for c in ccards:
                name = c.get("name", "")
                # 1) shot.characters 显式列出
                in_chars = name in shot_chars
                # 2) 名字出现在 shot 描述中
                in_desc = name and name in shot_text
                # 3) 别名匹配（如"天帝"对应"君无烬（天帝真身）"）
                alias = ""
                if "天帝" in name and "天帝" in shot_text:
                    alias = "天帝"
                if in_chars or in_desc or alias:
                    mark = c.get("distinctive_mark", "")
                    style = c.get("style_keywords", "")
                    if mark:
                        parts.append(mark)
                    if style:
                        parts.append(style)
            if parts:
                char_anchor = "，".join(parts)

    # 从 scene_cards 提取光照、氛围、色调，动态生成 [光照] 段
    matched_scene = None
    if script_data:
        scene_cards = script_data.get("scene_cards", [])
        for sc in scene_cards:
            for rp in refs:
                basename = os.path.basename(rp)
                if basename.startswith(sc.get("name", "").replace(" ", "_")):
                    matched_scene = sc
                    break
            if matched_scene:
                break

    if matched_scene:
        lighting = matched_scene.get("lighting", "")
        atmosphere = matched_scene.get("atmosphere", "")
        palette = matched_scene.get("color_palette", "")
        scene_name = matched_scene.get("name", "")
        parts_l = []
        if lighting:
            parts_l.append(lighting)
        if atmosphere:
            parts_l.append(atmosphere)
        if palette:
            parts_l.append(f"色调{palette}")
        if parts_l:
            lighting_desc = "，".join(parts_l) + "，电影级光影表现。"
        else:
            lighting_desc = "自然光照，电影级光影表现。"
        scene_info = (
            f"\n场景: {scene_name}\n"
            f"光照: {lighting}\n"
            f"氛围: {atmosphere}\n"
            f"色调: {palette}"
        )
    else:
        lighting_desc = "自然光照，电影级光影表现。"
        scene_info = ""

    model_note = f"\n# 推荐模型: {model}"

    # 为每张参考图描述角色
    edit_parts = []
    has_character_refs = False
    for i, rp in enumerate(refs):
        filename = os.path.splitext(os.path.basename(rp))[0]
        if i == 0:
            role = "场景基底"
        else:
            role = f"角色{i+1}样式（{filename}）"
            has_character_refs = True
        edit_parts.append(f"参考图{i+1}为{role}")

    # 2.0 Flash → 多图融合；2.1 Flash → 基底 + 添加
    # ⚠️ 单角色时用"该角色"避免 AI 脑补第二人
    # 修复：判断人类角色数量（"猫"等非人类不算），避免"1人+1猫"误判为多角色
    def _is_human_ref(filename: str) -> bool:
        """判断参考图是否为人类角色（否则视为动物/生物）。"""
        f = filename.lower()
        # 含动物/生物关键词 → 非人类
        non_human_kw = ["猫", "dog", "cat", "鸟", "鱼", "龙", "狐狸", "wolf", "animal", "creature"]
        if any(kw in f for kw in non_human_kw):
            return False
        return True
    human_ref_count = sum(1 for i, rp in enumerate(refs)
                          if i > 0 and _is_human_ref(os.path.splitext(os.path.basename(rp))[0]))
    char_ref_count = sum(1 for i, _ in enumerate(refs) if i > 0)
    if is_v2_1:
        if has_character_refs:
            if human_ref_count <= 1:
                # 有人类角色但≤1人时，强制约束为单人类（其他参考图为动物/生物）
                non_human_hint = ""
                if char_ref_count > 1:
                    non_human_hint = "非人类参考图是动物/生物形态，禁止将其画成人形或类人角色。"
                # 提取唯一人类角色的简名
                human_name = ""
                for i, rp in enumerate(refs):
                    if i == 0:
                        continue
                    fn = os.path.splitext(os.path.basename(rp))[0]
                    if _is_human_ref(fn):
                        # 取文件名中的人类角色名（_front/_face等后缀之前的部分）
                        for suffix in ["_front", "_face", "_side", "_back"]:
                            if suffix in fn:
                                human_name = fn.split(suffix)[0]
                                break
                        if not human_name:
                            human_name = fn
                        break
                hint_name = f"（{human_name}）" if human_name else ""
                edit_instruction = (
                    f"[编辑指令] {'。'.join(edit_parts)}。"
                    f"以图1为场景基底，{desc}。"
                    f"注意：只能出现一位人类角色{hint_name}，禁止出现第二个人。{non_human_hint}"
                )
            else:
                edit_instruction = (
                    f"[编辑指令] {'。'.join(edit_parts)}。"
                    f"以图1为基底，在图1中添加各角色，{desc}。注意角色间的空间关系和视线方向。"
                )
        else:
            edit_instruction = (
                f"[编辑指令] 参考图1为场景。以图1为基底，{desc}。"
            )
    else:
        if has_character_refs:
            if human_ref_count <= 1:
                non_human_hint = ""
                if char_ref_count > 1:
                    non_human_hint = "非人类参考图是动物/生物形态，禁止将其画成人形或类人角色。"
                human_name = ""
                for i, rp in enumerate(refs):
                    if i == 0: continue
                    fn = os.path.splitext(os.path.basename(rp))[0]
                    if _is_human_ref(fn):
                        for suffix in ["_front", "_face", "_side", "_back"]:
                            if suffix in fn:
                                human_name = fn.split(suffix)[0]; break
                        if not human_name: human_name = fn
                        break
                hint_name = f"（{human_name}）" if human_name else ""
                edit_instruction = (
                    f"[编辑指令] {'。'.join(edit_parts)}。"
                    f"以图1为场景基底，{desc}。"
                    f"只出现一位人类角色{hint_name}，禁止出现第二个人或倒影。{non_human_hint}"
                )
            else:
                edit_instruction = (
                    f"[编辑指令] {'。'.join(edit_parts)}。"
                    f"以图1为场景基底，在场景中加入各角色，{desc}。"
                    f"注意角色间的空间关系和视线方向，明确写出无交互无对视。"
                )
        else:
            edit_instruction = (
                f"[编辑指令] {'。'.join(edit_parts)}。"
                f"以图1为基础，{desc}。"
            )
    quality_text = "电影级写实，服装材质细节，光影层次丰富，氛围情绪饱满。\n"

    # === [目标风格/场景] 段：拼接 desc + char_anchor（确保角色特征不丢失） ===
    target_style = desc
    if char_anchor:
        target_style = f"{desc}，{char_anchor}" if desc else char_anchor

    # === 从 script_data 获取 aspect_ratio 和 global_style ===
    aspect = "16:9"
    global_style = ""
    if script_data:
        sc = script_data.get("script", {})
        aspect = sc.get("aspect_ratio", "16:9")
        global_style = sc.get("global_style", "")

    return build_first_frame_prompt_template(
        model=model,
        ref_count=ref_count,
        edit_instruction=edit_instruction,
        target_style=target_style,
        lighting_desc=lighting_desc,
        scene_info=scene_info,
        aspect=aspect,
        global_style=global_style,
    )



def _clean_prompt(text: str, segments: list[str] | None = None) -> str:
    """
    清理提示词：去掉 Markdown 标题行、文档说明、[xxx] 标签和历史迭代。

    当 segments 为 None 时，按原顺序保留 ## 提示词 之后的所有非标签内容（全量模式）。
    当 segments 指定时（如 ["目标风格/场景","光照","构图","画质要求"]），
    仅提取指定 [xxx] 段的内容，按 segments 顺序拼接。
    """
    import re
    lines = text.split("\n")
    in_frontmatter = False
    in_prompt_section = False

    if segments is not None:
        # 段模式：仅提取指定片段
        collected: dict[str, list[str]] = {}
        current_tag: str | None = None
        for line in lines:
            stripped = line.strip()
            if stripped == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter:
                continue
            if stripped == "## 提示词":
                in_prompt_section = True
                continue
            if not in_prompt_section:
                continue
            if stripped.startswith("## 历史"):
                break
            m = re.match(r'^\[(.+?)\]\s*', stripped)
            if m:
                current_tag = m.group(1)
                content_after = stripped[m.end():]
                if content_after:
                    collected.setdefault(current_tag, []).append(content_after)
            elif current_tag:
                collected.setdefault(current_tag, []).append(stripped)
        # 按 segments 顺序拼接
        result_parts = []
        for seg in segments:
            if seg in collected:
                result_parts.append("\n".join(collected[seg]))
        return "\n\n".join(result_parts).strip()

    # 全量模式（原有逻辑）
    cleaned: list[str] = []
    in_prompt_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if stripped == "## 提示词":
            in_prompt_section = True
            continue
        if stripped.startswith("## 历史"):
            break
        if not in_prompt_section:
            continue
        line_clean = re.sub(r'^\[.*?\]\s*', '', line)
        cleaned.append(line_clean)
    result = "\n".join(cleaned).strip()
    return result if result else text



def _resolve_single_shot_params(
    project: str, shot: dict, size: str | None = None
) -> dict:
    """从 shot 的 first_frame 块解析生成参数，返回统一参数字典。

    返回值（给 generate_image 用）：
      { "model", "ref_images" (绝对路径), "output_dir", "output_name", "prompt" }
    或抛出 SystemExit。
    """
    ff = shot.get("first_frame")
    if not ff or not isinstance(ff, dict):
        raise SystemExit(f"shot_{shot['id']:02d} 没有 first_frame 块")

    # model
    model = ff.get("model", get_agnes_default_model())

    # ref_images（绝对路径）
    ref_paths: list[str] = []
    for rp in ff.get("ref_images", []):
        if not isinstance(rp, str):
            continue
        abs_p = rp if os.path.isabs(rp) else os.path.join(project, rp)
        if os.path.isfile(abs_p):
            ref_paths.append(abs_p)
    if not ref_paths:
        raise SystemExit(f"shot_{shot['id']:02d} first_frame.ref_images 均为空或文件不存在")

    # final
    final = ff.get("final", "")
    if not final:
        raise SystemExit(f"shot_{shot['id']:02d} first_frame.final 为空")
    final_abs = final if os.path.isabs(final) else os.path.join(project, final)

    # prompt
    prompt_file = ff.get("prompt_file", "")
    if not prompt_file:
        raise SystemExit(f"shot_{shot['id']:02d} first_frame.prompt_file 为空")
    prompt_abs = prompt_file if os.path.isabs(prompt_file) else os.path.join(project, prompt_file)
    if not os.path.isfile(prompt_abs):
        raise SystemExit(
            f"提示词文件不存在: {prompt_abs}\n"
            f"请先运行 --build-first-frames 生成模板"
        )
    with open(prompt_abs, "r", encoding="utf-8") as f:
        prompt = _clean_prompt(f.read().strip(),
            segments=ff.get("segments",
                           ["编辑指令","目标风格/场景","光照","构图","画质要求"]))
    if not prompt:
        raise SystemExit(f"提示词文件 {prompt_abs} 内容为空")

    return {
        "model": model,
        "ref_images": ref_paths,
        "output_dir": os.path.dirname(final_abs),
        "output_name": os.path.basename(final_abs),
        "prompt": prompt,
    }



def _build_first_frame(project: str, shot: dict, script_data: dict | None = None) -> dict | None:
    """为一个 shot 自动生成 first_frame 块。返回 None 表示跳过。

    返回的 dict 会额外带 `_report` 键（参考图校验信息），不写入 script.json。
    """
    sid = shot["id"]

    # 跳过 multi-image 模式
    if shot.get("generation", {}).get("mode") == "multi-image":
        _log(f"  ↪ shot_{sid:02d}: multi-image 模式，跳过")
        return None

    # 从 generation.reference_images 解析参考图
    ref = shot.get("generation", {}).get("reference_images", {})
    if not ref:
        _log(f"  ⚠️ shot_{sid:02d}: 无 reference_images，跳过")
        return None

    ref_paths = _resolve_generation_refs(project, ref)
    if not ref_paths:
        _log(f"  ⚠️ shot_{sid:02d}: 参考图文件不存在，跳过。检查 images/scenes/ images/characters/")
        return None

    model = get_agnes_default_model()
    prompt_file = f"prompts/storyboard/shot{sid:02d}_image.md"
    final_path = f"images/storyboard/shot_{sid:02d}_first_frame.png"

    return {
        "model": model,
        "ref_images": ref_paths,
        "final": final_path,
        "prompt_file": prompt_file,
    }



