"""从解析后的 sdef 数据生成 Click CLI wrapper 包。"""

from __future__ import annotations

import keyword
import py_compile
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from clam.generator.specifier_defaults import get_specifier_default
from clam.scanner.menu_scanner import MenuGroup, MenuItem, MenuScanResult
from clam.scanner.sdef_parser import SdefCommand, SdefEnumeration, SdefInfo, SdefProperty

TEMPLATES_DIR = Path(__file__).parent / "templates"


@dataclass
class TemplateParam:
    cli_name: str
    func_name: str
    description: str
    is_flag: bool
    choices: str | None  # repr of list, e.g. "['off', 'one', 'all']"
    as_name: str         # AppleScript 参数名（如 "to", "for"）
    sdef_type: str       # 原始 sdef 类型，决定值的格式化方式


@dataclass
class TemplateCommand:
    name: str            # 原始 AppleScript 命令名（如 "switch view"）
    cli_name: str
    func_name: str
    description: str
    direct_param: bool
    direct_optional: bool
    direct_type: str     # 直接参数的 sdef 类型
    params: list[TemplateParam]
    specifier_default: str = ""  # 默认 AppleScript 对象引用（如 "active tab of window 1"）


@dataclass
class TemplateProperty:
    cli_name: str
    func_name: str
    as_name: str  # AppleScript property name (may have spaces)
    description_short: str
    access: str
    value_type: str  # "int", "float", "bool", "str", or "choice"
    choices: str | None  # repr of list for enums


@dataclass
class TemplateNestedGroup:
    """Represents a nested object accessible via an application property.

    E.g. "current track" in Music — the app property returns a track object,
    and we generate commands to access the track's individual properties.
    """
    cli_name: str        # "current-track"
    func_name: str       # "current_track"
    as_name: str         # "current track" (AppleScript name of the app property)
    class_name: str      # "track"
    properties: list[TemplateProperty]  # all non-hidden class properties

# Max properties per nested group compound command
MAX_COMPOUND_PROPS = 25


def _build_enum_map(enumerations: list[SdefEnumeration]) -> dict[str, list[str]]:
    """Map enumeration names to their value names."""
    return {e.name: [v[0] for v in e.values] for e in enumerations}


def _sdef_type_to_value_type(sdef_type: str, enum_map: dict[str, list[str]]) -> tuple[str, str | None]:
    """Convert sdef type to (value_type, choices_repr)."""
    if sdef_type == "integer":
        return "int", None
    if sdef_type == "real":
        return "float", None
    if sdef_type == "boolean":
        return "bool", None
    if sdef_type in enum_map:
        return "choice", repr(enum_map[sdef_type])
    return "str", None


def _safe_func_name(name: str) -> str:
    """将参数名转为合法 Python 标识符，避免关键字冲突。"""
    func_name = name.replace(" ", "_").replace("-", "_")
    if keyword.iskeyword(func_name):
        func_name += "_"
    return func_name


def _should_include_command(cmd: SdefCommand) -> bool:
    """只跳过 hidden 和 standard suite 命令，不再按类型过滤。"""
    return not cmd.is_standard_suite and not cmd.hidden


def _build_template_commands(
    commands: list[SdefCommand],
    enum_map: dict[str, list[str]],
    app_id: str = "",
) -> list[TemplateCommand]:
    result = []
    for cmd in commands:
        if not _should_include_command(cmd):
            continue

        params = []
        for p in cmd.parameters:
            sdef_type = p.type or ""
            cli_name = p.name.replace(" ", "-")
            func_name = _safe_func_name(p.name)
            if p.type == "boolean":
                params.append(TemplateParam(
                    cli_name=cli_name,
                    func_name=func_name,
                    description=p.description,
                    is_flag=True,
                    choices=None,
                    as_name=p.name,
                    sdef_type=sdef_type,
                ))
            elif p.type in enum_map:
                params.append(TemplateParam(
                    cli_name=cli_name,
                    func_name=func_name,
                    description=p.description,
                    is_flag=False,
                    choices=repr(enum_map[p.type]),
                    as_name=p.name,
                    sdef_type="enum",
                ))
            else:
                params.append(TemplateParam(
                    cli_name=cli_name,
                    func_name=func_name,
                    description=p.description,
                    is_flag=False,
                    choices=None,
                    as_name=p.name,
                    sdef_type=sdef_type,
                ))

        has_dp = cmd.direct_parameter is not None
        dp_optional = has_dp and cmd.direct_parameter.optional
        dp_type = cmd.direct_parameter.type if has_dp else ""

        # Look up specifier/document defaults for this app
        spec_default = ""
        if has_dp and not dp_optional and dp_type:
            spec_default = get_specifier_default(app_id, dp_type) or ""

        result.append(TemplateCommand(
            name=cmd.name,
            cli_name=cmd.cli_name,
            func_name=cmd.func_name,
            description=cmd.description,
            direct_param=has_dp,
            direct_optional=dp_optional,
            direct_type=dp_type,
            params=params,
            specifier_default=spec_default,
        ))
    return result


def _build_template_properties(
    properties: list[SdefProperty],
    enum_map: dict[str, list[str]],
) -> list[TemplateProperty]:
    """生成全量非 hidden 属性，不再使用 allowlist。"""
    result = []
    seen = set()
    for prop in properties:
        if prop.hidden:
            continue
        if prop.name in seen:
            continue
        seen.add(prop.name)

        value_type, choices = _sdef_type_to_value_type(prop.type, enum_map)
        result.append(TemplateProperty(
            cli_name=prop.cli_name,
            func_name=prop.func_name,
            as_name=prop.name,
            description_short=prop.description or prop.name,
            access=prop.access,
            value_type=value_type,
            choices=choices,
        ))
    return result


_PRIMITIVE_TYPES = frozenset({"text", "integer", "real", "boolean", "date", "double integer"})

# Types that _format_value can reliably handle in AppleScript
_SUPPORTED_TYPES = _PRIMITIVE_TYPES | frozenset({
    "Unicode text", "string", "number", "file", "alias",
})


def _build_nested_groups(
    app_properties: list[SdefProperty],
    all_properties: list[SdefProperty],
    enum_map: dict[str, list[str]],
) -> list[TemplateNestedGroup]:
    """Build nested groups for app properties whose type is a known class.

    E.g. Music's "current track" (type=track) → generates accessors for
    track properties like name, artist, album.
    """
    # Collect known class names
    class_names = {p.class_name for p in all_properties}

    # Find app properties that reference a class
    groups = []
    for app_prop in app_properties:
        if app_prop.hidden or app_prop.type not in class_names:
            continue

        # Get properties of the referenced class (non-hidden, primitive types)
        class_props = [
            p for p in all_properties
            if p.class_name == app_prop.type and not p.hidden
            and (p.type in _PRIMITIVE_TYPES or p.type in enum_map)
        ]
        if not class_props:
            continue

        template_props = _build_template_properties(class_props, enum_map)
        groups.append(TemplateNestedGroup(
            cli_name=app_prop.cli_name,
            func_name=app_prop.func_name,
            as_name=app_prop.name,
            class_name=app_prop.type,
            properties=template_props,
        ))

    return groups


def get_wrapper_info(sdef_info: SdefInfo, app_id: str = "") -> dict:
    """获取 wrapper 的命令和属性信息（不生成文件）。

    Returns dict with commands, properties, and nested_groups.
    """
    enum_map = _build_enum_map(sdef_info.enumerations)
    if not app_id:
        app_id = sdef_info.app_name.lower().replace(" ", "-")
    commands = _build_template_commands(sdef_info.commands, enum_map, app_id)
    app_props = [p for p in sdef_info.properties if p.class_name == "application"]

    # Separate simple properties from nested object references
    class_names = {p.class_name for p in sdef_info.properties}
    simple_props = [p for p in app_props if p.type not in class_names or p.hidden]
    properties = _build_template_properties(simple_props, enum_map)

    nested_groups = _build_nested_groups(app_props, sdef_info.properties, enum_map)

    return {
        "commands": commands,
        "properties": properties,
        "nested_groups": nested_groups,
    }


def check_command_support(sdef_info: SdefInfo, app_id: str = "") -> list[dict]:
    """Analyze each command's parameter types and report support level.

    Returns list of dicts with:
      - name: command cli_name
      - supported: True if all param types are handled
      - issues: list of strings describing unsupported params
    """
    enum_map = _build_enum_map(sdef_info.enumerations)
    results = []
    for cmd in sdef_info.commands:
        if not _should_include_command(cmd):
            continue
        issues = []
        # Check direct parameter (skip optional ones — user can just omit them)
        if cmd.direct_parameter and cmd.direct_parameter.type:
            dp_type = cmd.direct_parameter.type
            if not cmd.direct_parameter.optional:
                if dp_type not in _SUPPORTED_TYPES and dp_type not in enum_map:
                    # Check if we have a specifier default for this app+type
                    if not get_specifier_default(app_id, dp_type):
                        issues.append(f"direct param type '{dp_type}'")
        # Check named parameters
        for p in cmd.parameters:
            if p.type and p.type not in _SUPPORTED_TYPES and p.type not in enum_map:
                issues.append(f"param '{p.name}' type '{p.type}'")
        results.append({
            "name": cmd.cli_name,
            "supported": len(issues) == 0,
            "issues": issues,
        })
    return results


def generate_wrapper(sdef_info: SdefInfo, output_dir: Path) -> Path:
    """生成可 pip install 的 CLI wrapper 包。

    Args:
        sdef_info: 解析后的 sdef 数据。
        output_dir: 输出目录。

    Returns:
        输出目录路径。
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    enum_map = _build_enum_map(sdef_info.enumerations)
    app_id = sdef_info.app_name.lower().replace(" ", "-")

    app_props = [p for p in sdef_info.properties if p.class_name == "application"]

    # Separate simple properties from nested object references
    class_names = {p.class_name for p in sdef_info.properties}
    simple_props = [p for p in app_props if p.type not in class_names or p.hidden]

    commands = _build_template_commands(sdef_info.commands, enum_map, app_id)
    app_properties = _build_template_properties(simple_props, enum_map)
    nested_groups = _build_nested_groups(app_props, sdef_info.properties, enum_map)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )

    module_name = f"cli_{app_id.replace('-', '_')}"

    # 渲染 CLI 模块
    cli_template = env.get_template("applescript_cli.py.j2")
    cli_code = cli_template.render(
        app_name=sdef_info.app_name,
        app_id=app_id,
        commands=commands,
        app_properties=app_properties,
        nested_groups=nested_groups,
        max_compound_props=MAX_COMPOUND_PROPS,
    )
    cli_path = output_dir / f"{module_name}.py"
    cli_path.write_text(cli_code, encoding="utf-8")

    # 渲染 setup.py
    setup_template = env.get_template("setup.py.j2")
    setup_code = setup_template.render(app_id=app_id, module_name=module_name)
    setup_path = output_dir / "setup.py"
    setup_path.write_text(setup_code, encoding="utf-8")

    # 验证生成代码可编译
    try:
        py_compile.compile(str(cli_path), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"WARNING: Generated cli.py has syntax errors:\n{e}")
        print(f"Generated code saved at: {cli_path}")
        raise

    return output_dir


def generate_basic_wrapper(app_name: str, output_dir: Path) -> Path:
    """为无 .sdef 的应用生成基础模式 CLI wrapper（仅标准套件命令）。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    app_id = app_name.lower().replace(" ", "-")
    module_name = f"cli_{app_id.replace('-', '_')}"

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )

    # 渲染基础 CLI 模块
    cli_template = env.get_template("basic_cli.py.j2")
    cli_code = cli_template.render(app_name=app_name, app_id=app_id)
    cli_path = output_dir / f"{module_name}.py"
    cli_path.write_text(cli_code, encoding="utf-8")

    # 渲染 setup.py
    setup_template = env.get_template("setup.py.j2")
    setup_code = setup_template.render(app_id=app_id, module_name=module_name)
    setup_path = output_dir / "setup.py"
    setup_path.write_text(setup_code, encoding="utf-8")

    # 验证
    try:
        py_compile.compile(str(cli_path), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"WARNING: Generated cli.py has syntax errors:\n{e}")
        raise

    return output_dir


# ── UI Scripting mode ────────────────────────────────────────────────────────


@dataclass
class TemplateMenuItem:
    name: str           # original menu item name ("播放")
    cli_name: str       # CLI-safe name ("bo-fang")
    func_name: str      # Python-safe name ("menu_bo_fang")
    menu_bar_item: str  # parent menu bar item name
    submenu_of: str | None


@dataclass
class TemplateMenuGroup:
    name: str
    items: list[TemplateMenuItem]


def _to_ascii_slug(text: str) -> str:
    """Convert a string (possibly Chinese) to an ASCII slug for CLI/Python names.

    Uses pinyin-like mapping for common Chinese characters found in app menus.
    Falls back to stripping non-ASCII characters.
    """
    import re
    import unicodedata

    # Common Chinese menu item mappings (covers most app menus)
    _ZH_MAP = {
        "播放": "play", "暂停": "pause", "停止": "stop",
        "上一首": "prev", "下一首": "next",
        "音量加": "vol-up", "音量减": "vol-down",
        "喜欢": "like", "歌曲": "song", "歌词": "lyrics",
        "打开": "open", "关闭": "close", "切换": "toggle",
        "随机播放": "shuffle", "单曲循环": "repeat-one", "顺序播放": "sequential",
        "播放模式": "play-mode", "播放控制": "playback",
        "喜欢歌曲": "like-song",
        "静音": "mute", "全屏": "fullscreen",
        "新建": "new", "保存": "save", "另存为": "save-as",
        "设置": "settings", "偏好设置": "preferences",
        "搜索": "search", "刷新": "refresh",
        "登录": "login", "退出登录": "logout",
        "最小化": "minimize", "最大化": "maximize",
        "前进": "forward", "后退": "back",
    }

    # Try exact match first
    if text in _ZH_MAP:
        return _ZH_MAP[text]

    # Try compound: "打开/关闭歌词" → "toggle-lyrics"
    # Known verb pairs for toggle pattern
    _VERB_KEYS = {"打开", "关闭", "开启", "切换", "显示", "隐藏", "启用", "禁用"}
    if "/" in text:
        parts = text.split("/")
        verbs_en = []
        nouns = []
        for p in parts:
            remaining = p
            # Extract known verbs (shortest-tail = longest-verb first)
            sorted_items = sorted(_ZH_MAP.items(), key=lambda x: -len(x[0]))
            found_verb = False
            for zh, en in sorted_items:
                if zh in _VERB_KEYS and remaining.startswith(zh):
                    verbs_en.append(en)
                    remaining = remaining[len(zh):]
                    found_verb = True
                    break
            # Remaining is the noun
            if remaining:
                if remaining in _ZH_MAP:
                    nouns.append(_ZH_MAP[remaining])
                else:
                    nouns.append(remaining)
            elif not found_verb and p in _ZH_MAP:
                nouns.append(_ZH_MAP[p])
        if verbs_en:
            if "open" in verbs_en and "close" in verbs_en:
                verbs_en = ["toggle"]
            # Deduplicate nouns
            seen = set()
            unique_nouns = [n for n in nouns if n not in seen and not seen.add(n)]
            result_parts = verbs_en + unique_nouns
            result = "-".join(result_parts)
            result = re.sub(r"[^a-zA-Z0-9\-]", "", result)
            if result and result != "-":
                return result.strip("-")

    # Try partial matching
    result = text
    for zh, en in sorted(_ZH_MAP.items(), key=lambda x: -len(x[0])):
        result = result.replace(zh, en)

    # Replace separators
    result = result.replace("/", "-").replace(" ", "-").replace("…", "")

    # Strip non-ASCII
    result = re.sub(r"[^a-zA-Z0-9\-]", "", result)
    result = re.sub(r"-+", "-", result).strip("-")

    return result.lower() if result else "action"


def _menu_cli_name(item: MenuItem, group_name: str) -> str:
    """Generate a CLI-safe name for a menu item."""
    parts = []
    if item.submenu_of:
        parts.append(_to_ascii_slug(item.submenu_of))
    parts.append(_to_ascii_slug(item.name))
    return "-".join(parts).lower()


def _menu_func_name(cli_name: str) -> str:
    """Convert CLI name to Python function name."""
    func = cli_name.replace("-", "_")
    if keyword.iskeyword(func):
        func += "_"
    # Ensure it starts with a letter
    if func and not func[0].isalpha():
        func = "m_" + func
    return f"menu_{func}"


def _build_template_menu_groups(scan_result: MenuScanResult) -> list[TemplateMenuGroup]:
    """Convert MenuScanResult to template-ready menu groups."""
    seen_cli_names: set[str] = set()
    groups = []
    for group in scan_result.groups:
        t_items = []
        for item in group.items:
            cli_name = _menu_cli_name(item, group.name)
            if cli_name in seen_cli_names:
                continue
            seen_cli_names.add(cli_name)
            t_items.append(TemplateMenuItem(
                name=item.name,
                cli_name=cli_name,
                func_name=_menu_func_name(cli_name),
                menu_bar_item=group.name,
                submenu_of=item.submenu_of,
            ))
        if t_items:
            groups.append(TemplateMenuGroup(name=group.name, items=t_items))
    return groups


def generate_ui_wrapper(
    app_name: str,
    process_name: str,
    scan_result: MenuScanResult,
    output_dir: Path,
) -> Path:
    """生成基于 UI Scripting 的 CLI wrapper（通过菜单点击控制应用）。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    app_id = app_name.lower().replace(" ", "-")
    module_name = f"cli_{app_id.replace('-', '_')}"

    menu_groups = _build_template_menu_groups(scan_result)

    first_menu_cmd = ""
    first_menu_desc = ""
    if menu_groups and menu_groups[0].items:
        first_menu_cmd = menu_groups[0].items[0].cli_name
        first_menu_desc = menu_groups[0].items[0].name

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )

    cli_template = env.get_template("ui_scripting_cli.py.j2")
    cli_code = cli_template.render(
        app_name=app_name,
        app_id=app_id,
        process_name=process_name,
        menu_groups=menu_groups,
        first_menu_cmd=first_menu_cmd,
        first_menu_desc=first_menu_desc,
    )
    cli_path = output_dir / f"{module_name}.py"
    cli_path.write_text(cli_code, encoding="utf-8")

    setup_template = env.get_template("setup.py.j2")
    setup_code = setup_template.render(app_id=app_id, module_name=module_name)
    setup_path = output_dir / "setup.py"
    setup_path.write_text(setup_code, encoding="utf-8")

    try:
        py_compile.compile(str(cli_path), doraise=True)
    except py_compile.PyCompileError as e:
        print(f"WARNING: Generated cli.py has syntax errors:\n{e}")
        print(f"Generated code saved at: {cli_path}")
        raise

    return output_dir


def get_ui_wrapper_info(scan_result: MenuScanResult) -> dict:
    """获取 UI scripting wrapper 的命令信息。"""
    menu_groups = _build_template_menu_groups(scan_result)
    cmd_count = sum(len(g.items) for g in menu_groups)
    return {
        "menu_groups": menu_groups,
        "menu_cmd_count": cmd_count,
    }
