"""clam — CLI Agent for Mac。

扫描你的 Mac，发现可被 AI 操控的应用，一键生成 CLI 接口。
"""

from __future__ import annotations

import sys

import click

from clam.output import console, error, output, status, success
from clam.registry import registry
from clam.scanner.app_scanner import find_app, find_basic_app, scan_applications, suggest_app
from clam.scanner.sdef_parser import parse_sdef
from clam.generator.applescript_gen import (
    check_command_support,
    generate_basic_wrapper, generate_ui_wrapper, generate_wrapper,
    get_ui_wrapper_info, get_wrapper_info,
)
from clam.scanner.menu_scanner import scan_menus
from clam.generator.installer import install_wrapper, uninstall_wrapper


def _display_width(s: str) -> int:
    """计算字符串在终端中的显示宽度（处理中文、emoji 宽度差异）。"""
    import unicodedata
    w = 0
    for ch in s:
        cp = ord(ch)
        if ch == "\ufe0f":                         # 变体选择符，不占宽度
            continue
        eaw = unicodedata.east_asian_width(ch)
        if eaw in ("W", "F"):                      # 中日韩宽字符
            w += 2
        elif 0x1F000 <= cp <= 0x1FFFF:             # 补充 emoji 区
            w += 2
        elif 0x2600 <= cp <= 0x27BF:               # 杂项符号 & 丁巴特
            w += 2
        elif 0x2300 <= cp <= 0x23FF:               # 杂项技术符号 (⏱ 等)
            w += 2
        else:
            w += 1
    return w


def _pad_to(s: str, target: int) -> str:
    """将字符串用空格补齐到 target 个显示列宽。"""
    current = _display_width(s)
    return s + " " * max(0, target - current)


# ── 每个应用的人类可读能力描述 ──────────────────────────────────────────────
# app_id → (emoji, 类别, 核心能力)
_APP_DESCRIPTIONS: dict[str, tuple[str, str, str]] = {
    # 媒体
    "music":              ("🎵", "媒体", "控制播放、切歌、音量调节、曲目查询"),
    "tv":                 ("📺", "媒体", "视频播放、切集、音量调节、播放列表管理"),
    "quicktime-player":   ("🎬", "媒体", "视频播放、录屏、录音、导出裁剪"),
    "garageband":         ("🎸", "媒体", "音乐制作预览"),
    "photos":             ("📷", "媒体", "照片导入导出、相册管理、幻灯片放映"),
    # 浏览器
    "google-chrome":      ("🌐", "浏览器", "打开网页、管理标签页、页面导航"),
    "safari":             ("🌐", "浏览器", "打开网页、管理标签页、书签、阅读列表"),
    "arc":                ("🌐", "浏览器", "打开网页、管理标签页、页面导航"),
    "doubao":             ("🌐", "浏览器", "打开网页、管理标签页、书签操作"),
    # 办公
    "microsoft-word":     ("📝", "办公", "文档编辑、格式设置、表格、批量排版"),
    "microsoft-excel":    ("📊", "办公", "电子表格、图表、公式计算、数据处理"),
    "microsoft-powerpoint": ("📊", "办公", "幻灯片制作、动画设置、演示控制"),
    "microsoft-outlook":  ("📧", "办公", "邮件收发、日程管理、联系人"),
    "keynote":            ("📊", "办公", "幻灯片制作、导出、演示控制"),
    "pages":              ("📝", "办公", "文档编辑、排版、表格、导出"),
    "numbers":            ("📊", "办公", "电子表格、行列操作、排序、导出"),
    # 效率
    "mail":               ("📧", "效率", "发送邮件、搜索、管理邮箱"),
    "calendar":           ("📅", "效率", "创建/查询日程、视图切换"),
    "contacts":           ("👤", "效率", "联系人管理、搜索查询"),
    "messages":           ("💬", "效率", "发送消息"),
    "notes":              ("📝", "效率", "创建/搜索/编辑备忘录"),
    "reminders":          ("✅", "效率", "查看提醒事项、待办管理"),
    "ticktick":           ("✅", "效率", "任务查询、添加待办、番茄钟"),
    # 设计
    "figma":              ("🎨", "设计", "对象操作、文本排版、矢量编辑、图层管理"),
    # 开发/系统/工具
    "finder":             ("📂", "系统", "文件管理、窗口视图、前往目录、标签"),
    "xcode":              ("🔨", "开发", "项目构建、运行、测试、调试"),
    "terminal":           ("💻", "系统", "执行脚本、窗口设置"),
    "system-settings":    ("🔧", "系统", "系统设置查看与修改"),
    "shortcuts":          ("🔗", "系统", "运行快捷指令"),
    "amphetamine":        ("🔋", "工具", "防休眠控制、会话管理"),
    "flow":               ("🕐", "工具", "专注计时、番茄钟、阶段控制"),
    "the-unarchiver":     ("📦", "工具", "文件解压"),
    "bluetooth-file-exchange": ("📡", "工具", "蓝牙文件收发"),
    "screen-sharing":     ("🖥️", "工具", "远程屏幕共享"),
    "console":            ("🔍", "工具", "系统日志查看"),
}


def _auto_describe(cmd_names: list[str]) -> str:
    """根据命令名自动生成能力描述（用于未收录应用的兜底）。"""
    caps: list[str] = []
    names = {n.lower() for n in cmd_names}
    if names & {"play", "pause", "stop", "playpause", "resume"}:
        caps.append("播放控制")
    if names & {"next-track", "previous-track", "back-track"}:
        caps.append("切歌")
    if names & {"reload", "go-back", "go-forward"}:
        caps.append("页面导航")
    if names & {"send", "reply", "forward"}:
        caps.append("消息收发")
    if names & {"search", "find"}:
        caps.append("搜索")
    if names & {"export", "import"}:
        caps.append("导入导出")
    if names & {"build", "run", "test"}:
        caps.append("构建运行")
    if names & {"start", "stop", "reset"}:
        caps.append("启停控制")
    if not caps:
        caps.append("脚本化操作")
    return "、".join(caps[:4])


@click.group()
@click.option("--json", "use_json", is_flag=True, help="输出 JSON 格式，供 AI 工具解析")
@click.pass_context
def cli(ctx, use_json):
    """clam — CLI Agent for Mac

    扫描你的 Mac，发现可被 AI 操控的应用，一键生成 CLI 接口。
    """
    ctx.ensure_object(dict)
    ctx.obj["json"] = use_json


@cli.command()
@click.pass_context
def scan(ctx):
    """扫描本地可脚本化应用"""
    json_mode = ctx.obj["json"]

    if not json_mode:
        status("🔍 正在扫描本地应用…")

    apps = scan_applications()

    # 解析每个应用获取命令/属性数量
    results = []
    for app in apps:
        if app.sdef_path:
            # 完整模式：解析 sdef
            try:
                sdef_info = parse_sdef(app.sdef_path, app.name)
                wrapper_info = get_wrapper_info(sdef_info)
                results.append({
                    "name": app.name,
                    "app_id": app.app_id,
                    "sdef_path": app.sdef_path,
                    "commands": len(wrapper_info["commands"]),
                    "properties": len(wrapper_info["properties"]),
                    "nested_groups": len(wrapper_info["nested_groups"]),
                    "installed": app.installed,
                    "cmd_names": [c.cli_name for c in wrapper_info["commands"]],
                    "mode": "full",
                })
            except Exception:
                continue
        else:
            # UI Scripting / 基础模式：无 sdef，使用描述信息
            results.append({
                "name": app.name,
                "app_id": app.app_id,
                "sdef_path": "",
                "commands": 0,
                "properties": 0,
                "nested_groups": 0,
                "installed": app.installed,
                "cmd_names": [],
                "mode": "ui",
            })

    if json_mode:
        # JSON 模式不输出 cmd_names
        json_results = [{k: v for k, v in r.items() if k != "cmd_names"} for r in results]
        output(json_results, json_mode=True)
    else:
        if not results:
            console.print("未发现可脚本化应用")
            return

        console.print(
            f"\n🔍 [bold]扫描完成[/bold] — "
            f"发现 {len(results)} 个可脚本化应用"
        )

        # 按类别分组
        from collections import defaultdict

        grouped: dict[str, list[dict]] = defaultdict(list)
        for r in results:
            entry = _APP_DESCRIPTIONS.get(r["app_id"])
            cat = entry[1] if entry else "其他"
            grouped[cat].append(r)

        cat_order = ["办公", "设计", "媒体", "浏览器", "效率", "开发", "系统", "工具", "其他"]
        sorted_cats = sorted(grouped.keys(), key=lambda c: cat_order.index(c) if c in cat_order else 99)

        # 计算最长「emoji+名称」的显示宽度以对齐竖线
        def _label(r):
            entry = _APP_DESCRIPTIONS.get(r["app_id"])
            emoji = entry[0] if entry else "📎"
            return f"{emoji} {r['name']}"

        col_width = max(_display_width(_label(r)) for r in results) + 2

        idx = 1
        for cat in sorted_cats:
            console.rule(f"[bold]{cat}[/bold]", style="dim")
            for r in grouped[cat]:
                entry = _APP_DESCRIPTIONS.get(r["app_id"])
                desc = entry[2] if entry else _auto_describe(r["cmd_names"])
                label = _label(r)
                padded = _pad_to(label, col_width)
                mark = "  [green]✓[/green]" if r["installed"] else ""
                console.print(
                    f"  {idx:2d}.  {padded}[dim]|[/dim]  {desc}{mark}"
                )
                idx += 1
            console.print()

        console.print(
            "[dim]💡 安装: clam install <名称>  |  "
            "详情: clam info <名称>[/dim]"
        )


def _app_not_found(app_name: str) -> None:
    """输出未找到应用的错误信息。"""
    suggestions = suggest_app(app_name)
    if suggestions:
        error(f"未找到应用: {app_name}，你是不是想找: {', '.join(suggestions)}")
    else:
        error(f"未找到应用: {app_name}，运行 clam scan 查看可用应用")
    sys.exit(1)


@cli.command()
@click.argument("app_name")
@click.pass_context
def install(ctx, app_name):
    """安装应用的 CLI wrapper"""
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        app = find_basic_app(app_name)
    if not app:
        _app_not_found(app_name)

    mode = "full"  # "full", "ui", "basic"
    menu_scan = None
    if not app.sdef_path:
        # 无 sdef — 尝试 UI Scripting 模式：探测菜单
        if not json_mode:
            status(f"🔍 正在探测 {app.name} 的菜单结构…")
        menu_scan = scan_menus(app.name, app.process_name or None)
        if menu_scan and menu_scan.total_items > 0:
            mode = "ui"
        else:
            mode = "basic"

    mode_labels = {"full": "", "ui": "（UI Scripting 模式）", "basic": "（基础模式）"}
    if not json_mode:
        status(f"📦 正在为 {app.name} 生成 CLI wrapper{mode_labels[mode]}…")

    wrapper_dir = registry.REGISTRY_DIR / "wrappers" / app.app_id

    if mode == "basic":
        # 基础模式：仅标准套件命令
        try:
            generate_basic_wrapper(app.name, wrapper_dir)
        except Exception as e:
            error(f"生成 wrapper 失败: {e}")
            sys.exit(1)
        cmd_count = 3   # activate, quit-app, open-file
        prop_count = 3  # get-name, get-version, get-frontmost
    elif mode == "ui":
        # UI Scripting 模式：通过菜单点击控制
        try:
            generate_ui_wrapper(app.name, menu_scan.process_name, menu_scan, wrapper_dir)
        except Exception as e:
            error(f"生成 wrapper 失败: {e}")
            sys.exit(1)
        ui_info = get_ui_wrapper_info(menu_scan)
        cmd_count = ui_info["menu_cmd_count"] + 3  # menu commands + activate/quit/open
        prop_count = 3  # get-name, get-version, get-frontmost
    else:
        # 完整模式：解析 sdef
        try:
            sdef_info = parse_sdef(app.sdef_path, app.name)
        except Exception as e:
            error(f"解析 sdef 失败: {e}")
            sys.exit(1)
        try:
            generate_wrapper(sdef_info, wrapper_dir)
        except Exception as e:
            error(f"生成 wrapper 失败: {e}")
            sys.exit(1)
        wrapper_info = get_wrapper_info(sdef_info)
        cmd_count = len(wrapper_info["commands"])
        prop_count = len(wrapper_info["properties"])

    if not json_mode:
        status(f"📦 正在安装 clam-{app.app_id}…")

    # pip install
    if not install_wrapper(app.app_id, wrapper_dir):
        error("pip install 失败")
        sys.exit(1)

    # 注册
    registry.register(
        app_id=app.app_id,
        app_name=app.name,
        sdef_path=app.sdef_path,
        wrapper_dir=str(wrapper_dir),
        command_count=cmd_count,
        property_count=prop_count,
    )

    if json_mode:
        output({
            "app_id": app.app_id,
            "entry_point": f"clam-{app.app_id}",
            "commands": cmd_count,
            "properties": prop_count,
            "mode": mode,
        }, json_mode=True)
    else:
        ep = f"clam-{app.app_id}"
        if mode == "basic":
            success(f"{app.name} 已安装 → [bold]{ep}[/bold]  [dim]（基础模式）[/dim]")
            console.print(f"   命令: {cmd_count} 个  |  属性: {prop_count} 个")
            console.print(f"\n   [dim]快速上手:[/dim]")
            console.print(f"   [dim]  $ {ep} activate       前置窗口[/dim]")
            console.print(f"   [dim]  $ {ep} get-version    查看版本[/dim]")
            console.print(f"   [dim]  $ {ep} quit-app       退出应用[/dim]")
        elif mode == "ui":
            ui_info = get_ui_wrapper_info(menu_scan)
            success(f"{app.name} 已安装 → [bold]{ep}[/bold]  [dim]（UI Scripting 模式）[/dim]")
            console.print(f"   菜单命令: {ui_info['menu_cmd_count']} 个  |  基础命令: 6 个")
            console.print(f"\n   [dim]快速上手:[/dim]")
            for g in ui_info["menu_groups"][:2]:
                if g.items:
                    item = g.items[0]
                    console.print(f"   [dim]  $ {ep} {item.cli_name:<20}{item.name}[/dim]")
            console.print(f"   [dim]  $ {ep} activate            前置窗口[/dim]")
        else:
            nested_count = len(wrapper_info["nested_groups"])
            nested_str = f"  |  嵌套对象: {nested_count} 个" if nested_count else ""
            success(f"{app.name} 已安装 → [bold]{ep}[/bold]")
            console.print(f"   命令: {cmd_count} 个  |  属性: {prop_count} 个{nested_str}")

            example_cmds = []
            if wrapper_info["properties"]:
                first_prop = wrapper_info["properties"][0]
                example_cmds.append(f"{ep} get-{first_prop.cli_name}")
            if wrapper_info["commands"]:
                first_cmd = wrapper_info["commands"][0]
                example_cmds.append(f"{ep} {first_cmd.cli_name}")
            if wrapper_info["nested_groups"]:
                first_group = wrapper_info["nested_groups"][0]
                example_cmds.append(f"{ep} get-{first_group.cli_name}")

            console.print(f"\n   [dim]快速上手:[/dim]")
            for ex in example_cmds[:3]:
                console.print(f"   [dim]  $ {ex}[/dim]")

        console.print(f"   [dim]  $ {ep}         查看能力概括[/dim]")
        console.print(f"   [dim]  $ {ep} api     查看完整 API[/dim]")
        console.print()
        console.print("   [bold]AI 工具集成:[/bold]")
        console.print(f"   已配置完成，AI 可直接在终端调用 [cyan]{ep}[/cyan] 的所有命令。")
        console.print(f"   查看 AI 集成指南: [dim]clam --json info {app.app_id}[/dim]")


@cli.command(name="list")
@click.pass_context
def list_cmd(ctx):
    """查看已安装的 wrapper"""
    json_mode = ctx.obj["json"]
    wrappers = registry.list_all()

    if json_mode:
        output(list(wrappers.values()), json_mode=True)
        return

    if not wrappers:
        console.print(
            "尚未安装任何 wrapper，运行 [bold]clam scan[/bold] 查看可用应用"
        )
        return

    from rich.table import Table
    table = Table(
        title="已安装的 wrapper",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("应用", style="bold")
    table.add_column("入口命令")
    table.add_column("命令", justify="right")
    table.add_column("属性", justify="right")
    table.add_column("安装时间")

    for app_id, info in wrappers.items():
        table.add_row(
            info["app_name"],
            info["entry_point"],
            str(info["command_count"]),
            str(info["property_count"]),
            info["installed_at"][:10],
        )
    console.print(table)


@cli.command()
@click.argument("app_name")
@click.pass_context
def info(ctx, app_name):
    """查看应用的命令和属性清单

    对 AI agent 集成最关键 — agent 先 clam info <app> --json
    获取能力清单，再调 clam-<app> <command>。
    """
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        _app_not_found(app_name)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        error(f"解析 sdef 失败: {e}")
        sys.exit(1)

    wrapper_info = get_wrapper_info(sdef_info)
    commands = wrapper_info["commands"]
    properties = wrapper_info["properties"]

    nested_groups = wrapper_info["nested_groups"]

    # Build support map for JSON output
    support_results = check_command_support(sdef_info, app.app_id)
    support_map = {r["name"]: r["supported"] for r in support_results}

    if json_mode:
        output({
            "app_id": app.app_id,
            "app_name": app.name,
            "entry_point": f"clam-{app.app_id}",
            "commands": [
                {
                    "name": cmd.cli_name,
                    "description": cmd.description,
                    "has_direct_param": cmd.direct_param,
                    "supported": support_map.get(cmd.cli_name, True),
                    "params": [
                        {
                            "name": f"--{p.cli_name}",
                            "description": p.description,
                        }
                        for p in cmd.params
                    ],
                }
                for cmd in commands
            ],
            "properties": [
                {
                    "name": prop.cli_name,
                    "as_name": prop.as_name,
                    "access": prop.access,
                    "type": prop.value_type,
                    "get_command": f"get-{prop.cli_name}",
                    "set_command": (
                        f"set-{prop.cli_name}"
                        if prop.access == "rw" else None
                    ),
                }
                for prop in properties
            ],
            "nested_groups": [
                {
                    "name": group.cli_name,
                    "class": group.class_name,
                    "compound_command": f"get-{group.cli_name}",
                    "properties": [
                        {
                            "name": prop.cli_name,
                            "access": prop.access,
                            "type": prop.value_type,
                            "get_command": f"get-{group.cli_name}-{prop.cli_name}",
                            "set_command": (
                                f"set-{group.cli_name}-{prop.cli_name}"
                                if prop.access == "rw" else None
                            ),
                        }
                        for prop in group.properties
                    ],
                }
                for group in nested_groups
            ],
        }, json_mode=True)
    else:
        from rich.table import Table

        # 头部信息
        installed = registry.get(app.app_id)
        status_str = (
            "[green]已安装[/green]" if installed else "[dim]未安装[/dim]"
        )
        console.print(f"\n[bold]{app.name}[/bold]  {status_str}")
        console.print(f"  SDEF: [dim]{app.sdef_path}[/dim]")
        console.print(f"  入口: [bold]clam-{app.app_id}[/bold]")
        nested_info = (
            f"  |  嵌套对象: {len(nested_groups)} 个"
            if nested_groups else ""
        )
        console.print(
            f"  命令: {len(commands)} 个  |  属性: {len(properties)} 个"
            f"{nested_info}\n"
        )

        # 命令表格
        if commands:
            cmd_table = Table(
                title="命令",
                show_header=True,
                header_style="bold",
            )
            cmd_table.add_column("命令名", style="cyan")
            cmd_table.add_column("说明")
            cmd_table.add_column("参数")
            for cmd in commands:
                params_str = ""
                if cmd.direct_param:
                    params_str = (
                        "[ITEM] " if cmd.direct_optional else "ITEM "
                    )
                params_str += " ".join(
                    f"--{p.cli_name}" for p in cmd.params
                )
                cmd_table.add_row(
                    cmd.cli_name, cmd.description, params_str.strip(),
                )
            console.print(cmd_table)

        # 属性表格
        if properties:
            console.print()
            prop_table = Table(
                title="属性 (get/set)",
                show_header=True,
                header_style="bold",
            )
            prop_table.add_column("属性名", style="cyan")
            prop_table.add_column("访问", justify="center")
            prop_table.add_column("类型")
            prop_table.add_column("说明")
            for prop in properties:
                access_str = (
                    "[green]rw[/green]"
                    if prop.access == "rw" else "[dim]r[/dim]"
                )
                prop_table.add_row(
                    prop.cli_name, access_str,
                    prop.value_type, prop.description_short,
                )
            console.print(prop_table)

        # 嵌套对象表格
        for group in nested_groups:
            console.print()
            grp_table = Table(
                title=f"{group.as_name} ({group.class_name}) 属性",
                show_header=True,
                header_style="bold",
            )
            grp_table.add_column("命令", style="cyan")
            grp_table.add_column("访问", justify="center")
            grp_table.add_column("类型")
            for prop in group.properties:
                access_str = (
                    "[green]rw[/green]"
                    if prop.access == "rw" else "[dim]r[/dim]"
                )
                grp_table.add_row(
                    f"get-{group.cli_name}-{prop.cli_name}",
                    access_str,
                    prop.value_type,
                )
            console.print(grp_table)
            console.print(
                f"  [dim]复合命令: get-{group.cli_name} → JSON[/dim]"
            )


@cli.command()
@click.argument("app_name")
@click.pass_context
def doctor(ctx, app_name):
    """检查应用命令的可靠性（参数类型分析）"""
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        _app_not_found(app_name)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        error(f"解析 sdef 失败: {e}")
        sys.exit(1)

    results = check_command_support(sdef_info, app.app_id)
    supported = [r for r in results if r["supported"]]
    unsupported = [r for r in results if not r["supported"]]

    if json_mode:
        output({
            "app_id": app.app_id,
            "total": len(results),
            "supported": len(supported),
            "unsupported": len(unsupported),
            "commands": results,
        }, json_mode=True)
    else:
        console.print(f"\n[bold]{app.name}[/bold] 命令可靠性检查\n")
        console.print(
            f"  [green]✓ {len(supported)}[/green] / {len(results)} 个命令完全支持"
        )
        if unsupported:
            console.print(
                f"  [yellow]⚠ {len(unsupported)}[/yellow] 个命令含复杂参数类型（可能不可用）\n"
            )
            for r in unsupported:
                issues = "、".join(r["issues"])
                console.print(f"    [yellow]⚠[/yellow] {r['name']} — {issues}")
        console.print()


@cli.command()
@click.argument("app_name")
@click.pass_context
def remove(ctx, app_name):
    """卸载应用的 CLI wrapper"""
    json_mode = ctx.obj["json"]

    # 在已安装列表中查找
    needle = app_name.lower().strip()
    wrappers = registry.list_all()

    app_id = None
    for wid, winfo in wrappers.items():
        if wid == needle or winfo["app_name"].lower() == needle:
            app_id = wid
            break

    if not app_id:
        error(f"未找到已安装的 wrapper: {app_name}")
        sys.exit(1)

    if not json_mode:
        status(f"🗑  正在卸载 clam-{app_id}…")

    uninstall_wrapper(app_id)

    if json_mode:
        output({"removed": app_id}, json_mode=True)
    else:
        success(f"已卸载 clam-{app_id}")
