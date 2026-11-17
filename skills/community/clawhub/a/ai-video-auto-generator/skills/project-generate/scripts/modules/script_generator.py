"""脚本生成器 — 从来源（文本/文档/飞书）生成 script.json。

用法:
    # 从文本描述生成
    python script_generator.py --project /path --prompt "..."

    # 从本地文件生成（.txt / .md / .json）
    python script_generator.py --project /path --source story.txt

    # 从飞书文档生成
    python script_generator.py --project /path --source feishu://doc/<token>

不需要外部 API，通过模板引擎 + NLP 关键词提取生成结构完整的脚本。
"""
import json, os, re, random, sys, subprocess
from typing import Any
from type_registry import get_type, apply_type_rules as _apply_type, register_type, list_types, _TYPES_DIR
import json as _json

def read_source(source: str) -> str:
    """从各种来源读取文本内容。

    Args:
        source: 路径或 URL。支持:
          - 本地文件路径 (.txt/.md/.json)
          - feishu://doc/<token> — 飞书文档
          - http(s)://... — 网页 URL
          - 纯文本 — 原样返回

    Returns:
        文本内容（如果是 .json 会序列化为描述文本）
    """
    # 飞书文档
    if source.startswith("feishu://doc/"):
        token = source.split("feishu://doc/", 1)[-1].split("?")[0].split("#")[0]
        return _read_feishu_doc(token)

    # 飞书 Base 表格
    if source.startswith("feishu://base/"):
        parts = source.split("feishu://base/", 1)[-1].split("/")
        token = parts[0]
        table = parts[1] if len(parts) > 1 else ""
        return _read_feishu_base(token, table)

    # HTTP URL
    if source.startswith("http://") or source.startswith("https://"):
        return _read_url(source)

    # 本地文件
    if os.path.isfile(source):
        ext = os.path.splitext(source)[1].lower()
        if ext == ".json":
            # JSON 文件直接加载，转换为描述文本
            with open(source, "r", encoding="utf-8") as f:
                data = json.load(f)
            return _script_to_prompt(data)
        elif ext == ".docx":
            return _read_docx(source)
        else:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()

    # 纯文本
    return source


def _read_feishu_doc(token: str) -> str:
    """通过 lark-cli 读取飞书文档内容。"""
    try:
        r = subprocess.run(
            ["lark-cli", "docs", "+read", "--doc", token],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if r.returncode == 0:
            return r.stdout[:5000]  # 限制长度
        return f"[无法读取飞书文档: {r.stderr[:200]}]"
    except FileNotFoundError:
        return "[需要 lark-cli 才能读取飞书文档]"
    except Exception as e:
        return f"[读取飞书文档异常: {e}]"


def _read_feishu_base(token: str, table: str) -> str:
    """通过 lark-cli 读取飞书 Base 表格记录。"""
    try:
        cmd = ["lark-cli", "base", "+record-list", "--base-token", token]
        if table:
            cmd += ["--table-id", table]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            records = json.loads(r.stdout)
            lines = []
            for rec in records.get("items", [])[:50]:
                fields = rec.get("fields", {})
                desc = " | ".join(f"{k}: {v}" for k, v in fields.items()
                                  if v and not k.startswith("_"))
                lines.append(desc)
            return "\n".join(lines) if lines else "[Base 表格为空]"
        return f"[无法读取 Base: {r.stderr[:200]}]"
    except Exception as e:
        return f"[读取 Base 异常: {e}]"


def _read_url(url: str) -> str:
    """读取网页内容。"""
    try:
        from urllib.request import urlopen, Request
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        # 简单去 HTML 标签
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:5000]
    except Exception as e:
        return f"[读取 URL 异常: {e}]"


def _read_docx(path: str) -> str:
    """读取 .docx 文件。"""
    try:
        from docx import Document
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs[:100])  # 最多 100 段
    except ImportError:
        return "[需要 python-docx 才能读取 .docx 文件]"
    except Exception as e:
        return f"[读取 docx 异常: {e}]"


def _script_to_prompt(script: dict) -> str:
    """将已有的 script.json 转换为描述文本（用于重新生成）。"""
    lines = [script.get("script", {}).get("title", "短视频脚本")]
    for c in script.get("character_cards", []):
        lines.append(f"角色: {c.get('name', '?')}（{c.get('title', '')}）")
    for s in script.get("scene_cards", []):
        lines.append(f"场景: {s.get('name', '?')} - {s.get('description', '')}")
    for s in script.get("shots", []):
        lines.append(f"  shot_{s['id']:02d}: {s.get('description', '')}")
    return "\n".join(lines)
_STYLE_KW = {
    "电影": "电影级写实风格",
    "写实": "电影级写实风格",
    "真实": "电影级写实风格",
    "动漫": "二次元动漫风格",
    "二次元": "二次元动漫风格",
    "卡通": "卡通插画风格",
    "古风": "古风水墨风格",
    "水墨": "古风水墨风格",
    "暗黑": "暗黑哥特风格",
    "赛博": "赛博朋克风格",
    "科幻": "科幻未来风格",
}

_TONE_KW = {
    "紧张": "紧张激烈",
    "欢乐": "轻松欢快",
    "悲伤": "忧郁悲伤",
    "温馨": "温馨治愈",
    "悬疑": "悬疑神秘",
    "热血": "热血激昂",
    "平静": "平静恬淡",
    "搞笑": "幽默搞笑",
}

# ── 运镜模板 ──────────────────────────────────────────
_CAMERA_PATTERNS = [
    "镜头缓慢推进",
    "镜头平稳横移",
    "镜头固定，特写",
    "镜头缓缓上摇",
    "镜头环绕拍摄",
    "镜头拉远",
    "静态构图",
]

_EMOTION_TRANSITIONS = [
    ("平静", "温馨", "温馨开场"),
    ("温馨", "紧张", "气氛骤变"),
    ("紧张", "激烈", "冲突升级"),
    ("激烈", "紧张", "高潮回落"),
    ("紧张", "悲伤", "悲剧转折"),
    ("悲伤", "平静", "归于平静"),
    ("平静", "欢快", "情绪转好"),
    ("欢快", "温馨", "温馨收尾"),
]


def _detect_or_create_type(content: str, explicit_type: str = "") -> tuple[str, dict]:
    """从内容中检测视频类型，不存在时自动创建。

    策略:
      1. 如果用户指定了类型名且存在 → 直接使用
      2. 如果用户指定了类型名但不存在 → 用内容分析创建新类型
      3. 如果未指定 → 从内容关键词检测

    Returns: (type_name, type_def)
    """
    lower = content.lower()
    all_types = list_types()

    # 1. 用户明确指定了类型
    if explicit_type:
        if explicit_type in all_types:
            return explicit_type, get_type(explicit_type)
        # 不存在 → 自动创建
        return _auto_create_type(explicit_type, content)

    # 2. 从内容关键词检测
    # 先检查内置类型的匹配关键词
    for kw, vt in [("军事", "military"), ("战争", "military"), ("战术", "military"),
                   ("文旅", "travelogue"), ("旅游", "travelogue"), ("旅行", "travelogue"),
                   ("电影", "cinematic"), ("电影级", "cinematic"), ("长剧", "cinematic"),
                   ("短剧", "short_drama"), ("剧情", "short_drama")]:
        if kw in lower and vt in all_types:
            return vt, get_type(vt)

    # 3. 如果内容很长（文档），尝试从内容特征推断
    lines = content.strip().split("\n")
    if len(lines) > 20:
        # 文档内容 → 尝试检测类型特征
        scene_keywords = len(re.findall(r'(场景|镜头|幕|场)', content))
        char_count_content = len(re.findall(r'[\u4e00-\u9fff]{2,4}(?=[的。，：:、]|$)', content))
        if scene_keywords > 5 and char_count_content > 3:
            # 看起来像剧本/电影分镜 → cinematic
            if "cinematic" in all_types:
                return "cinematic", get_type("cinematic")

    # 4. 默认
    return "short_drama", get_type("short_drama")


def _auto_create_type(name: str, content: str) -> tuple[str, dict]:
    """自动创建新视频类型 — 从内容分析生成类型规则。"""
    lower = content.lower()
    
    # 提取关键特征
    has_16_9 = any(kw in lower for kw in ["横屏", "16:9", "宽屏", "电影"])
    has_9_16 = any(kw in lower for kw in ["竖屏", "9:16", "手机"])
    
    # 提取运镜关键词
    camera_kws_found = []
    for kw in ["推进", "拉远", "横移", "上摇", "下摇", "环绕", "航拍", "特写", "全景", "跟随"]:
        if kw in lower:
            camera_kws_found.append(kw)
    if not camera_kws_found:
        camera_kws_found = ["推进", "横移", "特写"]
    
    # 提取情绪关键词
    emotion_kws_found = []
    for kw in ["紧张", "激烈", "平静", "悲伤", "欢快", "温馨", "压抑", "悬疑", "热血"]:
        if kw in lower:
            emotion_kws_found.append(kw)
    if not emotion_kws_found:
        emotion_kws_found = ["平静", "温馨", "紧张"]
    
    # 提取风格
    aesthetic = "电影级写实风格"
    for kw, st in _STYLE_KW.items():
        if kw in lower:
            aesthetic = st
            break

    type_def = {
        "name": name,
        "description": f"从内容自动生成 — {content[:50]}...",
        "defaults": {
            "aspect_ratio": "16:9" if has_16_9 else "9:16",
            "max_shots": 25,
            "min_shots": 4,
        },
        "shot_rules": {
            "camera_patterns": [f"镜头{k}" for k in camera_kws_found[:5]],
            "emotion_arcs": emotion_kws_found[:7],
            "verify_style": "写实" if "写实" in aesthetic or "电影" in aesthetic else "动漫",
        },
    }

    # 写入选 type_defs/
    os.makedirs(_TYPES_DIR, exist_ok=True)
    tf = os.path.join(_TYPES_DIR, f"{name}.json")
    if not os.path.isfile(tf):
        try:
            with open(tf, "w", encoding="utf-8") as f:
                _json.dump(type_def, f, ensure_ascii=False, indent=2)
            print(f"  🆕 自动创建视频类型: {name} → {tf}")
        except Exception:
            pass

    register_type(name, type_def)
    return name, type_def


def generate_script(project: str, content: str, output: bool = True, type_name: str = "") -> dict:
    """从内容生成 script.json 并写入项目目录。

    Args:
        project: 项目根目录
        content: 用于生成脚本的文本内容（prompt / 文档全文等）
        output: 是否写回 script.json

    Returns:
        script dict
    """
    prompt = content
    prompt_lower = prompt.lower()

    # 1. 提取风格
    aesthetic = "电影级写实风格"
    for kw, style in _STYLE_KW.items():
        if kw in prompt_lower:
            aesthetic = style
            break

    # 2. 提取基调
    tone = "平静"
    for kw, t in _TONE_KW.items():
        if kw in prompt_lower:
            tone = t
            break

    # 3. 提取角色数量
    char_count = 1
    for kw, n in [("两人", 2), ("双人", 2), ("三个", 3), ("四人", 4), ("群像", 5)]:
        if kw in prompt_lower:
            char_count = n
            break

    # 4. 提取场景数量
    scene_count = 1
    for kw, n in [("两个场景", 2), ("三个场景", 3), ("多场景", 3)]:
        if kw in prompt_lower:
            scene_count = n
            break

    # 5. 估算镜头数
    shot_base = max(5, len(prompt) // 20)
    shot_count = min(15, max(5, shot_base))

    # 5.5 检测/创建视频类型
    video_type, type_def = _detect_or_create_type(prompt, explicit_type=type_name)
    type_rules = type_def.get("shot_rules", {})
    type_defaults = type_def.get("defaults", {})
    # 有转场需求增加镜头
    if any(kw in prompt_lower for kw in ["转场", "场景切换", "蒙太奇"]):
        shot_count += 3

    # 6. 生成角色卡
    chars: list[dict] = []
    for i in range(char_count):
        name = f"角色{i + 1}" if char_count > 1 else _extract_name(prompt)
        if not name or name == f"角色{i + 1}":
            name = f"角色{i + 1}"
        chars.append({
            "name": name,
            "title": f"角色{i + 1}" if char_count > 1 else "主角",
            "appearance": {"clothing": "未知", "hair": "未知", "physique": "匀称"},
            "views": ["front", "face", "side", "back"],
            "aesthetic_style": aesthetic,
            "asset_background": "white",
            "color_scheme": "中性",
            "gender": "未知",
            "age_range": "青年",
            "build": "匀称",
        })

    # 7. 生成场景卡
    scenes: list[dict] = []
    scene_names = _extract_scenes(prompt, scene_count)
    for i, sname in enumerate(scene_names):
        scenes.append({
            "name": sname,
            "id": f"scene_{i + 1}",
            "description": f"{sname}，氛围{tone}",
            "time": "白天",
            "color_palette": "自然色调",
        })

    # 8. 生成镜头列表
    shots: list[dict] = []
    # 根据类型选择运镜和情绪模板
    type_cameras = type_rules.get("camera_patterns", _CAMERA_PATTERNS)
    emotions = _build_emotion_arc(shot_count, tone)
    cameras = random.choices(type_cameras, k=shot_count)
    char_name = chars[0]["name"]

    for i in range(shot_count):
        sid = i + 1
        emo = emotions[i] if i < len(emotions) else "平静"
        cam = cameras[i]
        scene_idx = min(i // max(1, shot_count // scene_count), scene_count - 1)
        scene_id = scenes[scene_idx]["id"]

        # 为关键镜头生成描述
        if i == 0:
            desc = f"{char_name}出现在{scenes[scene_idx]['name']}，{cam}，{emo}"
        elif i == shot_count - 1:
            desc = f"{char_name}的结局镜头，{cam}，氛围{emo}"
        elif i == shot_count // 2:
            desc = f"关键转折：{char_name}面临抉择，{cam}，{emo}"
        else:
            action = random.choice(["行走", "注视", "说话", "思考", "动作"])
            desc = f"{char_name}{action}，{cam}，氛围{emo}"

        # 时长分布：开头短、中间长、结尾短
        if i < 2:
            dur = round(random.uniform(1.5, 3.0), 1)
        elif i == shot_count - 1:
            dur = round(random.uniform(3.0, 5.0), 1)
        else:
            dur = round(random.uniform(2.0, 4.0), 1)

        shots.append({
            "id": sid,
            "description": desc,
            "duration": dur,
            "location": scene_id,
        })

    # 9. 组装完整 script
    total_dur = sum(s["duration"] for s in shots)
    aspect = type_defaults.get("aspect_ratio", "9:16")
    script = {
        "script": {
            "title": prompt[:40] + ("..." if len(prompt) > 40 else ""),
            "type": video_type,
            "duration_seconds": round(total_dur, 1),
            "aspect_ratio": aspect,
            "aesthetic_style": aesthetic,
            "image_style": "cinematic photorealistic",
            "provider": "agnes",
            "video_provider": "agnes",
            "global_style": f"{aesthetic}，{tone}基调",
        },
        "character_cards": chars,
        "scene_cards": scenes,
        "shots": shots,
    }

    # 9.5 应用类型规则（运镜分配等）
    _apply_type(script)

    # 10. 写文件
    if output:
        os.makedirs(os.path.join(project, "images", "characters"), exist_ok=True)
        os.makedirs(os.path.join(project, "images", "scenes"), exist_ok=True)
        sp = os.path.join(project, "script.json")
        with open(sp, "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 脚本已生成: {sp}")
        print(f"     标题: {script['script']['title']}")
        print(f"     时长: {total_dur:.0f}s, {shot_count} 个镜头")
        print(f"     角色: {len(chars)} 个, 场景: {len(scenes)} 个")
        print(f"     风格: {aesthetic}")

    return script


# ── 辅助函数 ──────────────────────────────────────────

def _extract_name(prompt: str) -> str:
    """从 prompt 中提取可能的角色名。"""
    # 常见命名规则：中文名 2-4 字
    names = re.findall(r'[\u4e00-\u9fff]{2,4}(?=[的。，：:、]|$)', prompt)
    # 过滤掉场景/情绪等通用词
    skip = {"场景", "环境", "背景", "镜头", "画面", "短视频", "古代", "现代", "城市"}
    for n in names:
        if n not in skip:
            return n
    return "主角"


def _extract_scenes(prompt: str, count: int) -> list[str]:
    """从 prompt 中提取场景名，不够则用默认。"""
    scenes = re.findall(r'[\u4e00-\u9fff]{2,6}(?=(场景|地方|地点))', prompt)
    defaults = ["室内", "城市街头", "天台", "咖啡馆", "公园", "地下车库",
                "办公室", "海边", "森林", "废弃工厂", "屋顶", "走廊"]
    result = list(scenes) if scenes else []
    while len(result) < count:
        next_scene = defaults[len(result) % len(defaults)]
        if next_scene not in result:
            result.append(next_scene)
        else:
            result.append(f"{next_scene}{len(result) + 1}")
    return result[:count]


def _build_emotion_arc(count: int, tone: str) -> list[str]:
    """构建符合叙事逻辑的情绪弧线。"""
    if count <= 1:
        return [tone]

    # 根据 tone 选择弧线模板
    if any(k in tone for k in ("紧张", "悬疑")):
        template = ["平静", "平静", "紧张", "紧张", "激烈", "激烈", "紧张", "平静"]
    elif any(k in tone for k in ("悲伤", "忧郁")):
        template = ["平静", "悲伤", "悲伤", "悲伤", "压抑", "悲伤", "平静", "平静"]
    elif any(k in tone for k in ("欢乐", "搞笑")):
        template = ["欢快", "欢快", "温馨", "欢快", "欢快", "温馨", "温馨", "平静"]
    elif any(k in tone for k in ("热血", "激昂")):
        template = ["平静", "紧张", "激烈", "激烈", "紧张", "激烈", "紧张", "温馨"]
    else:
        template = ["平静", "温馨", "平静", "温馨", "紧张", "平静", "温馨", "平静"]

    # 循环/裁剪到目标长度
    result = []
    for i in range(count):
        result.append(template[i % len(template)])
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="从多种来源生成 script.json")
    parser.add_argument("--project", required=True, help="项目根目录")
    parser.add_argument("--prompt", default="", help="视频描述文本")
    parser.add_argument("--source", default="",
                        help="来源（本地文件/feishu://doc/<token>/URL）")
    args = parser.parse_args()

    if args.source:
        content = read_source(args.source)
        generate_script(args.project, content)
    elif args.prompt:
        generate_script(args.project, args.prompt)
    else:
        print("请提供 --prompt（文本描述）或 --source（文件/飞书链接）")
