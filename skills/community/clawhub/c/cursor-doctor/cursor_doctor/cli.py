"""Cursor Doctor CLI - Cursor IDE 故障诊断与修复命令行工具"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box

from . import __version__
from .diagnose import CursorDoctor
from .fixes.apply import suggest_fixes, apply_fix
from .signatures.database import SIGNATURES, count_by_category, CATEGORY_NAMES

console = Console()


@click.group()
@click.version_option(version=__version__)
def main():
    """Cursor Doctor - Cursor IDE 故障诊断与修复工具

    一键诊断 Cursor 报错、崩溃、配置问题，并提供智能修复方案。
    """
    pass


@main.command()
def diagnose():
    """全面诊断 Cursor 环境健康状况"""
    doctor = CursorDoctor()
    report = doctor.diagnose()

    console.print(Panel.fit(
        "[bold cyan]🔍 Cursor Doctor 诊断报告[/]",
        border_style="cyan"
    ))

    # 基本信息
    console.print(f"\n[bold]Cursor 版本:[/] {report.cursor_version}")
    console.print(f"[bold]诊断分数:[/] ", end="")
    if report.score < 0.3:
        console.print(f"[green]{report.score:.0%} - 健康 ✅[/]")
    elif report.score < 0.7:
        console.print(f"[yellow]{report.score:.0%} - 需关注 ⚠️[/]")
    else:
        console.print(f"[red]{report.score:.0%} - 高危 🔴[/]")

    # 系统环境
    console.print("\n[bold underline]系统环境:[/]")
    sys_table = Table(show_header=False, box=box.SIMPLE)
    sys_table.add_column("项目", style="cyan")
    sys_table.add_column("值")
    for k, v in report.system_checks.items():
        if isinstance(v, bool):
            v = "[green]是[/]" if v else "[dim]否[/]"
        sys_table.add_row(k.replace("_", " "), str(v))
    console.print(sys_table)

    # 错误列表
    if report.errors_found:
        console.print(f"\n[bold underline]发现 [red]{len(report.errors_found)}[/] 条错误:[/]")
        err_table = Table(show_header=True, box=box.ROUNDED)
        err_table.add_column("严重度", style="bold")
        err_table.add_column("签名", style="cyan")
        err_table.add_column("错误名")
        err_table.add_column("来源")

        for err in report.errors_found:
            sev = err["severity"]
            sev_style = {"critical": "red", "high": "yellow", "medium": "blue", "low": "dim"}.get(sev, "white")
            err_table.add_row(
                Text(sev.upper(), style=sev_style),
                err["signature_id"],
                err["signature_name"],
                err["file"]
            )
        console.print(err_table)

        # 修复建议
        fixes = suggest_fixes(report.errors_found)
        if fixes:
            console.print("\n[bold underline]推荐修复:[/]")
            for f in fixes:
                sev_style = {"high": "yellow", "critical": "red"}.get(f["severity"], "blue")
                console.print(f"  [{sev_style}]■[/] {f['name']}: {f['description']}")
                console.print(f"     使用: [dim]cursor-doctor fix {f['category']}[/]")
    else:
        console.print("\n[green]✅ 未发现错误日志，Cursor 运行正常[/]")


@main.command()
@click.argument("category", required=False)
def fix(category: str | None):
    """自动修复 Cursor 问题

    CATEGORY: mcp_connection | crash | network_proxy | config_env
    
    不指定类别则自动诊断并推荐修复方案。
    """
    if category:
        doctor = CursorDoctor()
        report = doctor.diagnose()
        result = apply_fix(report.errors_found, category)
        console.print(result)
    else:
        # Auto-detect and fix all
        doctor = CursorDoctor()
        report = doctor.diagnose()
        
        if not report.errors_found:
            console.print("[green]✅ Cursor 运行正常，无需修复[/]")
            return
        
        fixes = suggest_fixes(report.errors_found)
        if not fixes:
            console.print("[yellow]⚠️ 未找到匹配的自动修复方案[/]")
            return
        
        console.print(f"[bold]发现 {len(fixes)} 类可修复问题:[/]\n")
        for i, f in enumerate(fixes, 1):
            sev_style = {"critical": "red", "high": "yellow"}.get(f["severity"], "blue")
            console.print(f"  {i}. [{sev_style}]■[/] [bold]{f['name']}[/]: {f['description']}")
        
        console.print("\n[dim]使用 'cursor-doctor fix <category>' 应用特定修复[/]")
        console.print("[dim]或 'cursor-doctor fix mcp_connection' 修复 MCP 连接问题[/]")


@main.command()
def signatures():
    """浏览已知的错误签名数据库"""
    console.print(Panel.fit(
        "[bold yellow]📋 Cursor Doctor 错误签名数据库[/]",
        border_style="yellow"
    ))

    # 分类统计
    counts = count_by_category()
    summary = Table(show_header=True, box=box.SIMPLE)
    summary.add_column("分类", style="cyan")
    summary.add_column("数量", justify="right")
    summary.add_column("严重级别", justify="center")

    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        cat_name = CATEGORY_NAMES.get(cat, cat)
        # Find worst severity in this category
        catsigs = [s for s in SIGNATURES if s.category == cat]
        worst = max(s.severity for s in catsigs)
        sev_style = {"critical": "red", "high": "yellow"}.get(worst, "blue")
        summary.add_row(cat_name, str(count), Text(worst.upper(), style=sev_style))
    console.print(summary)

    # 详细列表
    console.print("\n[bold underline]详细签名:[/]")
    sig_table = Table(show_header=True, box=box.ROUNDED)
    sig_table.add_column("ID", style="dim")
    sig_table.add_column("名称", style="cyan")
    sig_table.add_column("严重度", style="bold")
    sig_table.add_column("频率")
    sig_table.add_column("诊断摘要")

    for sig in SIGNATURES:
        sev_style = {"critical": "red", "high": "yellow", "medium": "blue", "low": "dim"}.get(sig.severity, "white")
        sig_table.add_row(
            sig.id,
            sig.name,
            Text(sig.severity.upper(), style=sev_style),
            f"{'🔥' * min(sig.frequency // 5 + 1, 5)} {sig.frequency}",
            sig.diagnosis[:50] + "..."
        )
    console.print(sig_table)

    console.print(f"\n[dim]共 {len(SIGNATURES)} 条签名，覆盖 {len(counts)} 个分类[/]")


@main.command()
@click.option("--text", "-t", help="输入错误文本进行匹配")
@click.option("--file", "-f", "file_path", help="从文件读取错误文本")
def match(text: str | None, file_path: str | None):
    """将错误文本与已知签名匹配"""
    if not text and not file_path:
        console.print("[yellow]请提供错误文本 (--text) 或错误日志文件 (--file)[/]")
        return
    
    if file_path:
        try:
            with open(file_path, "r") as f:
                text = f.read()
        except Exception as e:
            console.print(f"[red]无法读取文件: {e}[/]")
            return
    
    from .signatures.database import find_matching_signatures
    
    matches = find_matching_signatures(text)
    
    if not matches:
        console.print("[yellow]⚠️ 未找到匹配的已知错误签名[/]")
        console.print("[dim]这可能是新类型的错误，请将错误信息提交到 GitHub Issues[/]")
        return
    
    console.print(f"[bold green]✅ 找到 {len(matches)} 个匹配:[/]\n")
    
    for sig, pattern in matches:
        sev_style = {"critical": "red", "high": "yellow", "medium": "blue"}.get(sig.severity, "white")
        console.print(Panel(
            f"[bold]{sig.name}[/] [dim]({sig.id})[/]\n"
            f"严重度: [{sev_style}]{sig.severity.upper()}[/]\n"
            f"分类: {CATEGORY_NAMES.get(sig.category, sig.category)}\n\n"
            f"诊断: {sig.diagnosis}\n"
            f"修复: [cyan]{sig.fix_hint}[/]",
            title=f"匹配模式: {pattern}",
            border_style=sev_style
        ))
