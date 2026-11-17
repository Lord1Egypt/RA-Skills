#!/usr/bin/env python3
"""创建项目目录结构和 script.json 模板。

用法:
    python create_project.py --project /path/to/project [--template short_drama]
"""
import argparse, json, os, sys

# 从外部 JSON 文件加载模板
_TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "references", "templates.json")

# 加载类型注册表中的类型
try:
    _SKILL_MODULES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "skills", "project-generate", "scripts", "modules")
    if _SKILL_MODULES not in sys.path:
        sys.path.insert(0, _SKILL_MODULES)
    from type_registry import list_types as _list_types, get_type as _get_type
    _TYPE_NAMES = _list_types()
except Exception:
    _TYPE_NAMES = ["short_drama", "travelogue", "cinematic"]
if not os.path.isfile(_TEMPLATES_PATH):
    print(f"[ERROR] 模板文件未找到: {_TEMPLATES_PATH}")
    sys.exit(1)

try:
    with open(_TEMPLATES_PATH, "r", encoding="utf-8") as _f:
        TEMPLATES = json.load(_f)
except (json.JSONDecodeError, IOError) as _e:
    print(f"[ERROR] 模板文件格式错误: {_e}")
    sys.exit(1)

# 验证模板结构
_REQUIRED_TEMPLATE_KEYS = ["script.title", "shots"]
for _key, _data in list(TEMPLATES.items()):
    _missing = []
    if "shots" not in _data:
        _missing.append("shots[]")
    if not _missing:
        continue
    print(f"  [WARN] 模板 '{_key}' 缺少必要字段: {', '.join(_missing)}，创建的项目可能不完整")


def create_project(project: str, template_type: str = "short_drama",
                   feishu_doc_url: str | None = None) -> str:
    """创建项目目录结构和 script.json 模板，返回 script.json 路径。"""
    # 建目录
    dirs = [
        "images/characters", "images/scenes", "images/storyboard", "images/style",
        "images/props",
        "videos", "output", "sounds", "assets", "references", "scripts",
        "prompts", "tasks",
    ]
    for d in dirs:
        os.makedirs(os.path.join(project, d), exist_ok=True)
        print(f"  ✅ {d}")

    # 写 script.json
    script_path = os.path.join(project, "script.json")
    if os.path.isfile(script_path):
        print(f"  ⚠️ script.json 已存在，跳过")
        return script_path

    template_data = TEMPLATES.get(template_type, TEMPLATES["short_drama"])
    default_aspect = "16:9" if template_type in ("travelogue",) else "9:16"
    # 各类型的默认 global_style（≥15字，避免流水线卡在 optimize 阶段）
    _gs_defaults = {
        "short_drama": "短剧风格，剧情紧凑，画面清晰明亮，色彩饱满，叙事节奏明快",
        "travelogue": "文旅宣传风格，画面壮丽唯美，色彩鲜明，突出地域特色与文化底蕴",
        "cinematic": "电影叙事风格，画面质感细腻，光影层次丰富，构图考究，沉浸感强",
        "movie_length_drama": "电影级长剧风格，画面精良，细节丰富，色彩浓郁，沉浸感强",
    }
    script = {
        "script": {
            "title": os.path.basename(project),
            "duration_seconds": 30,
            "aspect_ratio": default_aspect,
            "type": template_type,
            "provider": "agnes",
            "global_style": _gs_defaults.get(template_type, "通用视频风格，画面明亮清晰，色彩丰富，细节层次生动"),
        },
        **template_data,
    }
    if feishu_doc_url:
        script["script"]["feishu_doc_url"] = feishu_doc_url
        # 自动提取 doc_id（wiki/doc 兼容），供飞书 Base 跟踪器使用
        if "/wiki/" in feishu_doc_url:
            doc_id = feishu_doc_url.rsplit("/wiki/", 1)[-1].split("?")[0].split("#")[0]
            script["script"]["feishu_doc_id"] = doc_id
        elif "/doc/" in feishu_doc_url:
            doc_id = feishu_doc_url.rsplit("/doc/", 1)[-1].split("?")[0].split("#")[0]
            script["script"]["feishu_doc_id"] = doc_id

    _safe_write_json(script_path, script)
    print(f"  ✅ script.json 已创建（{template_type} 模板）")

    print(f"\n=== 项目创建完成: {project} ===")
    print("接下来可运行 project-generate 完成后续步骤：")
    print("  project-generate --project . generate-characters   # 或 gc")
    print("  project-generate --project . generate-scenes       # 或 gs")
    print("  project-generate --project . build-first-frames    # 或 bff")

    return script_path


def _safe_write_json(path: str, data: dict) -> None:
    """JSON 安全写入：先写临时文件再 rename。"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main():
    parser = argparse.ArgumentParser(description="创建项目目录结构和 script.json 模板")
    parser.add_argument("--project", required=True, help="项目根目录路径")
    parser.add_argument("--template", default="short_drama",
                        choices=list(TEMPLATES.keys()) + _TYPE_NAMES,
                        help="项目模板类型")
    parser.add_argument("--feishu-doc-url", help="飞书需求文档 URL（可选）")
    parser.add_argument("--list-types", action="store_true", help="列出所有可用视频类型")
    args = parser.parse_args()

    if args.list_types:
        print("可用视频类型:")
        for t in sorted(set(list(TEMPLATES.keys()) + _TYPE_NAMES)):
            try:
                td = _get_type(t)
                print(f"  - {t}: {td.get('description', td.get('name', ''))}")
            except Exception:
                print(f"  - {t}")
        sys.exit(0)

    create_project(args.project, args.template, args.feishu_doc_url)

    # 创建后自动优化脚本（填充默认值、修复结构、补全字段）
    print("  📝 自动优化 script.json...")
    try:
        _opt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skills", "script-optimizer", "scripts")
        if os.path.isdir(_opt_dir) and _opt_dir not in sys.path:
            sys.path.insert(0, _opt_dir)
        from optimize import OptimizerV2
        opt = OptimizerV2(args.project, strict=True, gentle=True)
        result = opt.run()
        status = result.get("status", "unknown")
        print(f"     optimize: {status} (P0={result.get('p0','?')} P1={result.get('p1','?')})")
    except Exception as e:
        print(f"     ⚠️ optimize 跳过: {e}")


if __name__ == "__main__":
    main()
