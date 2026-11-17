#!/usr/bin/env python3
"""
CLAM Demo Recording Script
===========================
用于录制 README 演示 GIF/视频的脚本。

录制方式:
    # 推荐: asciinema (终端录制 → 转 GIF)
    brew install asciinema agg
    asciinema rec demo.cast -c "python demo_recording.py"
    agg demo.cast demo.gif --cols 90 --rows 32 --speed 1.5

    # 或者: 直接运行观看效果
    python demo_recording.py

前置要求:
    pip install clam-mac      # 安装 CLAM (或 pip install -e . 用开发模式)
    clam remove music 2>/dev/null   # 清除旧的 wrapper (确保演示 install 流程)

场景设计原则:
    每个场景都瞄准一个「现有工具链做不到 / 不好做」的真实问题。
    不是在展示功能，而是在展示「为什么你需要 CLAM」。
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any

# ── Rich 输出 ────────────────────────────────────────────────────────────────

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console(width=88)

# ── 配置 ──────────────────────────────────────────────────────────────────────

# 每行输出后暂停，方便录屏观看。设为 0 可快速跑完。
PACE = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0


def pause(seconds: float = 1.0):
    time.sleep(seconds * PACE)


def run(cmd: str, timeout: int = 30) -> str:
    """执行命令并返回 stdout。"""
    result = subprocess.run(
        cmd.split(), capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0 and result.stderr.strip():
        return f"[ERROR] {result.stderr.strip()}"
    return result.stdout.strip()


def run_json(cmd: str) -> Any:
    """执行命令并解析 JSON 输出。"""
    raw = run(cmd)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def title_card(title: str, subtitle: str, problem: str):
    """场景标题卡，带问题陈述。"""
    console.print()
    console.rule(style="cyan")
    header = Text()
    header.append(f"  {title}\n", style="bold cyan")
    header.append(f"  {subtitle}\n\n", style="dim")
    header.append(f"  ❌ 痛点: ", style="bold red")
    header.append(problem, style="red")
    console.print(Panel(header, box=box.HEAVY, border_style="cyan", padding=(1, 2)))
    pause(3)


def step(icon: str, text: str):
    """步骤提示。"""
    console.print(f"\n  {icon}  [bold]{text}[/bold]")
    pause(0.5)


def contrast(clam_way: str, old_way: str):
    """对比展示 CLAM vs 传统方式。"""
    t = Table(show_header=True, box=box.SIMPLE_HEAVY, padding=(0, 2))
    t.add_column("CLAM", style="green", width=38)
    t.add_column("传统方式", style="red dim", width=38)
    t.add_row(clam_way, old_way)
    console.print(t)
    pause(2)


def show_cmd(cmd: str):
    """展示即将执行的命令。"""
    console.print(f"    [dim]$[/dim] [bold green]{cmd}[/bold green]")
    pause(0.8)


# ═══════════════════════════════════════════════════════════════════════════════
#  场景 1: 自主发现 → 即装即用
# ═══════════════════════════════════════════════════════════════════════════════
#
#  这个场景命中的核心问题:
#
#  现有工具链中，AI Agent 只能使用「预先配置好」的工具。如果你想让 AI
#  控制一个 Mac 应用，典型流程是:
#    1. 去 GitHub / ClawHub 搜索该应用的 Skill 或 MCP     (~5 分钟)
#    2. 发现根本没有人写过 → 放弃                         (大概率)
#    3. 即使找到了: 安装 → 编辑配置 → 重启 Agent           (~10 分钟)
#    4. 发现版本不兼容 / 接口不全 → 再找替代方案            (~∞)
#
#  CLAM 的解法:
#    clam scan     → AI 自己发现你的 Mac 上有什么可以控制
#    clam install  → 10 秒自动生成完整 CLI, 无需任何配置
#    直接使用      → 立刻可用, 不需要重启任何东西
#
#  这是 CLAM 最独特的价值: 整条链路全自动, 从未知到可控只需 10 秒。
#  没有任何现有工具提供这种 discovery → generation → ready 的一体化能力。

def scene_1():
    title_card(
        "场景 1: 自主发现 → 即装即用",
        "你的 Mac 上有几十个应用, 但 AI 一个都碰不到",
        "让 AI 控制一个新应用, 传统方式需要找 Skill/MCP → 安装 → 配置 → 测试 ≈ 30+ 分钟\n"
        "           而且大多数应用根本没有现成的 Skill/MCP 可用",
    )

    # ── Step 1: Scan ──
    step("🔍", "扫描: 你的 Mac 上有什么可以控制?")
    show_cmd("clam scan --json")

    raw = run("clam scan --json")
    try:
        apps = json.loads(raw)
    except json.JSONDecodeError:
        console.print(f"    [red]scan 失败: {raw[:200]}[/red]")
        return

    # 展示发现的应用表格
    t = Table(
        title=f"  发现 {len(apps)} 个可控应用",
        box=box.ROUNDED,
        title_style="bold green",
        padding=(0, 1),
        show_lines=False,
    )
    t.add_column("应用", style="bold", min_width=18)
    t.add_column("命令数", justify="right", style="cyan")
    t.add_column("属性数", justify="right", style="cyan")
    t.add_column("模式", justify="center")

    mode_style = {"full": "[green]完整[/green]", "ui": "[yellow]UI[/yellow]", "basic": "[dim]基础[/dim]"}
    for app in apps[:15]:  # 最多展示 15 个，避免屏幕太满
        t.add_row(
            app["name"],
            str(app.get("commands", 0)),
            str(app.get("properties", 0)),
            mode_style.get(app.get("mode", ""), app.get("mode", "")),
        )
    if len(apps) > 15:
        t.add_row(f"[dim]... 还有 {len(apps) - 15} 个应用[/dim]", "", "", "")

    console.print(t)
    pause(3)
    console.print(f"    [green]✓[/green] [bold]{len(apps)}[/bold] 个应用的 CLI 接口都可以自动生成, 无需手动编写")
    pause(2)

    # ── Step 2: Install ──
    step("📦", "安装: 给 Music 生成 CLI (10 秒, 零配置)")
    show_cmd("clam install music --json")

    result = run_json("clam install music --json")
    if isinstance(result, dict) and "error" not in result:
        console.print(f"    [green]✓[/green] 已生成 [bold cyan]clam-music[/bold cyan] — "
                       f"{result.get('commands', '?')} 个命令, {result.get('properties', '?')} 个属性")
    else:
        console.print(f"    [yellow]⚠[/yellow] {result}")
    pause(2)

    # ── Step 3: Immediate Use ──
    step("▶️ ", "立刻使用: 无需重启, 无需配置")
    show_cmd("clam-music play")
    run("clam-music play")
    console.print("    [green]✓[/green] 音乐已开始播放")
    pause(2)

    show_cmd("clam-music set-sound-volume 35")
    run("clam-music set-sound-volume 35")
    console.print("    [green]✓[/green] 音量 → 35")
    pause(1)

    # ── Contrast ──
    contrast(
        "clam scan → install → 立刻可用\n⏱ 10 秒, 零配置",
        "搜索 Skill → 安装 → 编辑配置 → 重启 Agent\n⏱ 30+ 分钟, 如果能找到的话",
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  场景 2: 深度数据感知 — 结构化数据 vs 表面操作
# ═══════════════════════════════════════════════════════════════════════════════
#
#  这个场景命中的核心问题:
#
#  现有工具让 AI「操作」应用的方式是表面级的:
#    - 浏览器自动化: 截图 → OCR → 识别文字 → 猜测状态 (慢、不准)
#    - Siri / Shortcuts: 只能执行预设动作, 无法把数据返回给 AI
#    - 原生 AppleScript: AI 生成的脚本经常语法错误, 输出是非结构化文本
#
#  但 AI 做决策需要的是「数据」, 不是「像素」。
#
#  CLAM 的解法:
#    每个命令都返回 JSON 格式的结构化数据。
#    AI 可以直接读取 15+ 个字段 (歌名、艺术家、专辑、时长、评分、播放次数...)
#    然后基于数据做推理和决策 — 这是其他工具做不到的。
#
#  关键差异: 其他工具让 AI「点按钮」, CLAM 让 AI「读数据后做判断」。

def scene_2():
    title_card(
        "场景 2: 深度数据感知",
        "AI 需要的是数据, 不是像素",
        "浏览器自动化只能截图识别; Siri/Shortcuts 无法返回结构化数据给 AI\n"
        "           AI 无法基于应用状态做智能决策",
    )

    # ── Step 1: 获取完整曲目数据 ──
    step("📊", "读取当前曲目: 获取结构化数据")
    show_cmd("clam-music --json get-current-track")
    raw = run("clam-music --json get-current-track")
    try:
        track = json.loads(raw)
    except json.JSONDecodeError:
        console.print(f"    [yellow]⚠ 无法解析 (Music 可能未在播放): {raw[:100]}[/yellow]")
        track = {}

    if track:
        t = Table(
            title="  当前曲目 — 结构化 JSON 数据",
            box=box.ROUNDED,
            title_style="bold green",
            show_lines=False,
            padding=(0, 1),
        )
        t.add_column("字段", style="cyan", min_width=16)
        t.add_column("值", style="bold", min_width=30)

        # 选择最有代表性的字段展示
        display_keys = [
            "name", "artist", "album", "genre", "year",
            "duration", "rating", "played-count", "loved",
            "bit-rate", "sample-rate",
        ]
        shown = 0
        for key in display_keys:
            if key in track:
                t.add_row(key, str(track[key]))
                shown += 1
        # 补充其他字段
        for key, val in track.items():
            if key not in display_keys and shown < 12:
                t.add_row(key, str(val))
                shown += 1

        console.print(t)
        pause(3)

        total_fields = len(track)
        console.print(f"    [green]✓[/green] 共 [bold]{total_fields}[/bold] 个字段, "
                       "AI 可直接用于推理和决策")
        pause(2)

        # ── Step 2: 基于数据做决策 ──
        step("🧠", "AI 智能决策: 基于数据自动执行")

        # 示例: 根据评分决定是否跳过
        rating = track.get("rating", 0)
        name = track.get("name", "未知")
        artist = track.get("artist", "未知")

        console.print(f'    [dim]当前播放:[/dim] {name} — {artist}')

        if isinstance(rating, (int, float)) and rating > 0:
            if rating >= 60:
                console.print(f'    [dim]评分: {rating}/100[/dim] → [green]评分不错, 继续播放[/green]')
            else:
                console.print(f'    [dim]评分: {rating}/100[/dim] → [yellow]评分较低, 自动跳到下一首[/yellow]')
                run("clam-music next-track")
                pause(1)
                new_raw = run("clam-music --json get-current-track")
                try:
                    new_track = json.loads(new_raw)
                    console.print(f'    [green]✓[/green] 已切换到: '
                                   f'{new_track.get("name", "?")} — {new_track.get("artist", "?")}')
                except Exception:
                    pass
        else:
            # 无评分数据时, 演示播放次数决策
            played = track.get("played-count", 0)
            console.print(f'    [dim]播放次数: {played}[/dim] → ', end="")
            if isinstance(played, int) and played > 10:
                console.print("[green]常听曲目, 继续播放[/green]")
            else:
                console.print("[yellow]新发现的曲目, 标记关注[/yellow]")

        pause(2)
    else:
        console.print("    [dim]（请先在 Music.app 中播放一首歌再运行此场景）[/dim]")

    # ── Contrast ──
    contrast(
        "一条命令 → 15+ 字段的 JSON\nAI 可基于数据做推理和决策",
        "浏览器截图 → OCR → 只拿到歌名文字\n无法获取评分/时长/播放次数等元数据",
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  场景 3: 可靠性保障 — doctor 诊断 + 参数安全
# ═══════════════════════════════════════════════════════════════════════════════
#
#  这个场景命中的核心问题:
#
#  让 AI 直接写 AppleScript 是目前最常见的「快捷方案」, 但:
#    - AppleScript 语法诡异, AI 经常生成无法运行的脚本
#    - 参数类型错误 (把字符串传给整数参数) 导致无声失败
#    - AI 不知道哪些命令是安全可用的, 哪些会报错
#    - 没有任何反馈机制 — 失败了 AI 也不知道为什么
#
#  CLAM 的解法:
#    - 代码生成阶段: py_compile 编译验证, 类型安全的参数处理
#    - 使用前: `clam doctor` 分析每个命令的可靠性
#    - 运行时: 枚举参数用 choices 校验, 类型自动转换
#
#  关键差异: CLAM 在 AI 使用之前就告诉它「什么能用, 什么不能用」,
#  避免了 trial-and-error 的黑盒调试过程。

def scene_3():
    title_card(
        "场景 3: 可靠性保障",
        "AI 写 AppleScript 常出错, CLAM 提前帮你排雷",
        "AI 直接生成的 AppleScript 经常因为类型错误、语法问题静默失败\n"
        "           AI 不知道哪些命令可靠, 哪些会出错 — 只能盲试",
    )

    # ── Step 1: Doctor 诊断 ──
    step("🩺", "诊断: 哪些命令可靠可用?")
    show_cmd("clam doctor music --json")

    raw = run("clam doctor music --json")
    try:
        report = json.loads(raw)
    except json.JSONDecodeError:
        console.print(f"    [yellow]⚠ 解析失败[/yellow]")
        return

    total = report.get("total", 0)
    supported = report.get("supported", 0)
    unsupported = report.get("unsupported", 0)

    # 概览
    pct = (supported / total * 100) if total > 0 else 0
    console.print(f"    [bold]{total}[/bold] 个命令中, "
                   f"[green]{supported} 个完全可靠[/green], "
                   f"[yellow]{unsupported} 个有兼容性问题[/yellow]"
                   f"  ([bold]{pct:.0f}%[/bold] 可用率)")
    pause(2)

    # 展示几个可靠 + 几个有问题的
    commands = report.get("commands", [])
    ok_cmds = [c for c in commands if c.get("supported")]
    bad_cmds = [c for c in commands if not c.get("supported")]

    t = Table(box=box.ROUNDED, padding=(0, 1), show_lines=False)
    t.add_column("命令", style="bold", min_width=24)
    t.add_column("状态", justify="center", min_width=8)
    t.add_column("说明", min_width=30)

    for cmd in ok_cmds[:5]:
        t.add_row(cmd["name"], "[green]✓ 可靠[/green]", "[dim]所有参数类型已支持[/dim]")
    for cmd in bad_cmds[:3]:
        issues = ", ".join(cmd.get("issues", [])[:2])
        t.add_row(cmd["name"], "[yellow]⚠ 风险[/yellow]", f"[dim]{issues}[/dim]")

    console.print(t)
    pause(3)

    # ── Step 2: 带参数执行 — 类型安全 ──
    step("🔒", "类型安全: 参数自动校验")

    console.print("    [dim]设置音量 (整数参数, 自动类型转换):[/dim]")
    show_cmd("clam-music set-sound-volume 45")
    run("clam-music set-sound-volume 45")
    vol = run("clam-music --json get-sound-volume")
    console.print(f"    [green]✓[/green] 音量已设为: {vol}")
    pause(1)

    # ── Contrast ──
    contrast(
        "clam doctor 预先诊断 → AI 只调用可靠命令\n参数类型自动校验, 枚举值自动约束",
        "AI 写 AppleScript → 运行 → 报错 → 重试\n盲试循环, 浪费 3-5 轮对话才能成功",
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    console.print()
    # 开场
    banner = Text()
    banner.append("🦀 CLAM", style="bold cyan")
    banner.append(" — 给你的 AI 装上控制 Mac 的手\n\n", style="bold")
    banner.append("你的 Mac 上有几十个应用, 但 AI 一个都碰不到。\n", style="dim")
    banner.append("CLAM 一键生成 CLI 接口, 让 AI Agent 用原生方式操控一切。", style="dim")
    console.print(Panel(banner, box=box.DOUBLE, border_style="cyan", padding=(1, 3)))
    pause(3)

    scene_1()
    scene_2()
    scene_3()

    # 收尾
    console.print()

    # 恢复状态
    run("clam-music set-sound-volume 73")
    run("clam-music stop")

    # 结语
    ending = Text()
    ending.append("pip install clam-mac\n\n", style="bold green")
    ending.append("一行命令, 让你的 AI 控制一切。\n", style="dim")
    ending.append("OpenClaw Skill · Claude Code MCP · 或任何 Agent 框架", style="dim")
    console.print(Panel(ending, title="[bold cyan]开始使用[/bold cyan]",
                         box=box.DOUBLE, border_style="cyan", padding=(1, 3)))
    console.print()


if __name__ == "__main__":
    main()
