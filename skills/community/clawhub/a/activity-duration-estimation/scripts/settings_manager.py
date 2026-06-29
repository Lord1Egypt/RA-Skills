"""
settings_manager — 活动历时估算技能全局设置

管理 5 项运行时设置，持久化到数据目录 JSON 文件。
提供加载/保存/校验/转HTML CLI接口。
"""

import json
import os
import sys
from datetime import datetime

# ═══════════════════════════════════════════════════════
# R-12 审计锚点
# ═══════════════════════════════════════════════════════
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"

SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_dir_abs = os.path.normpath(os.path.join(
    SKILL_DIR, "..", ".standardization", "activity-duration-estimation", "data"
))
SETTINGS_JSON = os.path.join(_data_dir_abs, "settings.json")

# ═══════════════════════════════════════════════════════
# 默认设置
# ═══════════════════════════════════════════════════════
DEFAULT_SETTINGS = {
    "version": "1",
    "updated_at": "",

    # 联网搜索：auto(自动执行) / manual(每次手动)
    "web_search_mode": "manual",

    # 知识库采集（执行后自动写入历史数据）：auto(自动执行) / manual(每次手动)
    "kb_collect_mode": "manual",

    # 知识库调用（估算前查询历史基准）：auto(自动执行) / manual(每次手动)
    "kb_query_mode": "manual",

    # 文档指定：null(留空, LLM 按当前实现做) / 模板名(选择现有模板库的文档)
    "doc_template": None,

    # 文档撰写：auto(自动执行) / manual(每次手动) / template(模板要求——混合模式)
    "doc_write_mode": "auto",
}

# 可选值约束
FIELD_OPTIONS = {
    "web_search_mode": ["auto", "manual"],
    "kb_collect_mode": ["auto", "manual"],
    "kb_query_mode": ["auto", "manual"],
    "doc_template": None,  # None = 自由文本或 null
    "doc_write_mode": ["auto", "manual", "template"],
}

# 字段中文名（用于 UI）
FIELD_LABELS = {
    "web_search_mode": "联网搜索",
    "kb_collect_mode": "知识库采集",
    "kb_query_mode": "知识库调用",
    "doc_template": "文档指定",
    "doc_write_mode": "文档撰写",
}

FIELD_DESCRIPTIONS = {
    "web_search_mode": "auto = 执行时自动联网搜索补充信息；manual = 每次搜索前询问用户",
    "kb_collect_mode": "auto = 每次估算完成自动写入知识库；manual = 写入前询问用户",
    "kb_query_mode": "auto = 估算前自动查询历史基准；manual = 查询前询问用户",
    "doc_template": "留空 = LLM 根据模板库或当前实现自动选择；选择模板 = 使用指定的自定义模板",
    "doc_write_mode": "auto = 按节自动生成；manual = 纯手动模式/部分自动混合；template = 按自定义模板要求执行混合模式",
}


# ═══════════════════════════════════════════════════════
# 核心接口
# ═══════════════════════════════════════════════════════

def get_defaults() -> dict:
    """返回默认设置深拷贝"""
    return json.loads(json.dumps(DEFAULT_SETTINGS))


def load() -> dict:
    """加载设置，不存在则创建默认并返回"""
    if not os.path.exists(SETTINGS_JSON):
        os.makedirs(os.path.dirname(SETTINGS_JSON), exist_ok=True)
        save(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 补缺失字段
        changed = False
        for key, value in DEFAULT_SETTINGS.items():
            if key not in data:
                data[key] = value
                changed = True
        # 移除多余字段
        for key in list(data.keys()):
            if key not in DEFAULT_SETTINGS:
                del data[key]
                changed = True
        if changed:
            save(data)
        return data
    except (json.JSONDecodeError, OSError):
        save(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)


def save(settings: dict) -> bool:
    """保存设置到文件"""
    os.makedirs(os.path.dirname(SETTINGS_JSON), exist_ok=True)
    s = dict(settings)
    s["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "version" not in s:
        s["version"] = "1"
    try:
        with open(SETTINGS_JSON, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def validate(settings: dict) -> list[str]:
    """校验设置合法性，返回错误列表"""
    errors = []

    # 枚举值检查
    for key, valid in FIELD_OPTIONS.items():
        if valid is not None:
            val = settings.get(key)
            if val not in valid:
                errors.append(f"{key} 值 '{val}' 不在可选范围 {valid} 内")

    # 合法性检查
    doc_template = settings.get("doc_template")
    doc_write = settings.get("doc_write_mode")

    if doc_template is None or doc_template == "" or doc_template == "null":
        # 文档指定为空时，文档撰写不能为 template
        if doc_write == "template":
            errors.append("文档指定为空时，文档撰写不能为「模板要求」，请先选择模板或修改文档撰写模式")
    else:
        # 文档指定非空时，文档撰写为 template 是合法的
        pass

    # 字段完整性
    for key in DEFAULT_SETTINGS:
        if key not in settings and key not in ("version", "updated_at"):
            errors.append(f"缺少设置项: {key}")

    return errors


def apply_to(settings: dict, key: str, value) -> dict:
    """应用单条设置变更，返回新字典"""
    s = dict(settings)
    s[key] = value
    return s


def get(key: str) -> object:
    """快速获取某条设置值"""
    return load().get(key)


# ═══════════════════════════════════════════════════════
# CLI 接口
# ═══════════════════════════════════════════════════════

def cli_show():
    """CLI: 显示当前设置"""
    s = load()
    print(f"设置文件: {SETTINGS_JSON}")
    print(f"上次更新: {s.get('updated_at', 'N/A')}")
    print()
    for key in DEFAULT_SETTINGS:
        label = FIELD_LABELS.get(key, key)
        val = s.get(key, "未设置")
        desc = FIELD_DESCRIPTIONS.get(key, "")
        print(f"  {label} ({key}): {val}")
        if desc:
            print(f"    {desc}")
    print()


def cli_set(key: str, value: str):
    """CLI: 设置单条"""
    # 解析 null
    if value.lower() in ("null", "none", ""):
        value = None
    s = load()
    if key not in DEFAULT_SETTINGS:
        print(f"错误: 未知设置项 '{key}'")
        print(f"可用项: {', '.join(DEFAULT_SETTINGS.keys())}")
        return

    # 类型转换：web_search_mode 等字符串字段
    if key in FIELD_OPTIONS and FIELD_OPTIONS[key] is not None:
        if value not in FIELD_OPTIONS[key]:
            print(f"错误: {key} 的值必须是 {FIELD_OPTIONS[key]} 之一，收到 '{value}'")
            return

    s = apply_to(s, key, value)
    errs = validate(s)
    if errs:
        print("校验失败:")
        for e in errs:
            print(f"  ❌ {e}")
        return

    save(s)
    print(f"已设置 {key} = {value}")


def cli_reset():
    """CLI: 恢复默认"""
    save(DEFAULT_SETTINGS)
    print("已恢复默认设置")
    cli_show()


def cli_export_html():
    """CLI: 输出当前设置的 HTML 片段（供前端渲染）"""
    s = load()
    out = []
    out.append('<div class="settings-panel">')
    out.append(f'<div class="settings-meta">上次更新: {s.get("updated_at", "N/A")}</div>')

    for key in DEFAULT_SETTINGS:
        label = FIELD_LABELS.get(key, key)
        val = s.get(key, "")
        desc = FIELD_DESCRIPTIONS.get(key, "")
        options = FIELD_OPTIONS.get(key)

        if options:
            out.append(f'<div class="setting-row" data-key="{key}">')
            out.append(f'  <label>{label}</label>')
            out.append(f'  <select data-key="{key}" class="setting-select">')
            for opt in options:
                sel = " selected" if str(val) == opt else ""
                out.append(f'    <option value="{opt}"{sel}>{opt}</option>')
            out.append(f'  </select>')
            out.append(f'  <span class="setting-desc">{desc}</span>')
            out.append(f'</div>')
        else:
            # 自由文本（doc_template）
            display_val = val if val else ""
            out.append(f'<div class="setting-row" data-key="{key}">')
            out.append(f'  <label>{label}</label>')
            out.append(f'  <input type="text" data-key="{key}" class="setting-input" value="{display_val}" placeholder="留空或输入模板名" />')
            out.append(f'  <span class="setting-desc">{desc}</span>')
            out.append(f'</div>')

    out.append('</div>')
    print("\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cli_show()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "show":
        cli_show()

    elif cmd == "set":
        if len(sys.argv) < 3:
            print("用法: python settings_manager.py set <key> [value]")
            print("      不传 value 则将该项设为 null（清空 doc_template）")
            print(f"可用键: {', '.join(FIELD_LABELS.keys())}")
            print(f"  web_search_mode  → {FIELD_OPTIONS['web_search_mode']}")
            print(f"  kb_collect_mode  → {FIELD_OPTIONS['kb_collect_mode']}")
            print(f"  kb_query_mode     → {FIELD_OPTIONS['kb_query_mode']}")
            print(f"  doc_template      → 自由文本，不传值或传入 '' / 'null' 清空")
            print(f"  doc_write_mode    → {FIELD_OPTIONS['doc_write_mode']}")
            sys.exit(1)
        key = sys.argv[2]
        value = sys.argv[3] if len(sys.argv) >= 4 else ""
        cli_set(key, value)

    elif cmd == "list":
        """列出所有设置项及其说明"""
        print("\n可用设置项:")
        print("─" * 50)
        for key in DEFAULT_SETTINGS:
            label = FIELD_LABELS.get(key, key)
            desc = FIELD_DESCRIPTIONS.get(key, "")
            opts = FIELD_OPTIONS.get(key)
            current = load().get(key)
            print(f"  {key:20s}  {label}")
            print(f"  {'':20s}  {desc}")
            if opts:
                print(f"  {'':20s}  可选: {opts}")
            print(f"  {'':20s}  当前: {current}")
            print()

    elif cmd == "reset":
        cli_reset()

    elif cmd == "html":
        cli_export_html()

    elif cmd == "validate":
        s = load()
        errs = validate(s)
        if errs:
            print("校验失败:")
            for e in errs:
                print(f"  ❌ {e}")
        else:
            print("✅ 设置校验通过")

    elif cmd == "import":
        """
        从 JSON 文件批量导入设置。
        用法: python settings_manager.py import settings.json
        JSON 格式示例:
        {
            "web_search_mode": "manual",
            "kb_collect_mode": "manual",
            "doc_template": "立项申请书",
            "doc_write_mode": "template"
        }
        只导入 JSON 中存在的字段，不存在的保持当前值。
        """
        if len(sys.argv) < 3:
            print("用法: python settings_manager.py import <settings.json>")
            sys.exit(1)
        import_path = sys.argv[2]
        if not os.path.exists(import_path):
            print(f"文件不存在: {import_path}")
            sys.exit(1)
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                imported = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"读取失败: {e}")
            sys.exit(1)

        current = load()
        changed = []
        skipped = []
        for key in DEFAULT_SETTINGS:
            if key in imported:
                val = imported[key]
                # null 字符串转 None
                if isinstance(val, str) and val.lower() in ("null", ""):
                    val = None
                current[key] = val
                changed.append(key)
            else:
                skipped.append(key)

        errs = validate(current)
        if errs:
            print("导入后校验失败:")
            for e in errs:
                print(f"  ❌ {e}")
            sys.exit(1)

        save(current)
        print(f"已导入 {len(changed)} 项: {', '.join(changed)}")
        if skipped:
            print(f"未变更 {len(skipped)} 项: {', '.join(skipped)}")
        cli_show()

    elif cmd == "export":
        """
        导出当前设置为 JSON 文件。
        用法: python settings_manager.py export [output.json]
        默认输出到 settings_export.json
        """
        default_out = "settings_export.json"
        out_path = sys.argv[2] if len(sys.argv) >= 3 else default_out
        s = load()
        # 去掉运行时字段
        export = {k: s[k] for k in DEFAULT_SETTINGS if k in s}
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(export, f, ensure_ascii=False, indent=2)
            print(f"已导出 {len(export)} 项设置到 {out_path}")
        except OSError as e:
            print(f"导出失败: {e}")

    elif cmd == "server":
        """
        启动可视化设置面板（HTML）。
        用法: python settings_manager.py server [port]
        """
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9099
        print("启动设置面板...")
        # 动态导入避免循环依赖
        from scripts.settings_server import main
        main()

    elif cmd == "help":
        print("""
╔══════════════════════════════════════════════╗
║  activity-duration-estimation 设置管理工具  ║
╚══════════════════════════════════════════════╝

无需 LLM 参与，纯 Python CLI 直接管理。

用法:
  python settings_manager.py show             查看当前设置
  python settings_manager.py list             列出所有可设项及说明
  python settings_manager.py set <key> <val>  修改单条设置
  python settings_manager.py reset            恢复默认设置
  python settings_manager.py validate         校验当前设置合法性
  python settings_manager.py import <file>    从 JSON 文件批量导入
  python settings_manager.py export [file]    导出设置为 JSON 文件
  python settings_manager.py html             输出 HTML 片段
  python settings_manager.py server [port]    启动可视化面板（需配合 settings_server.py）

快捷设置示例:
  python settings_manager.py set web_search_mode auto
  python settings_manager.py set kb_collect_mode manual
  python settings_manager.py set doc_template 立项申请书
  python settings_manager.py set doc_write_mode template
  python settings_manager.py set doc_template ''      # 清空文档指定
  python settings_manager.py import my_settings.json   # 批量导入
""")

    else:
        print(f"未知命令: {cmd}")
        print("用法: python settings_manager.py [show|list|set|reset|validate|import|export|html|server|help]")
        sys.exit(1)
