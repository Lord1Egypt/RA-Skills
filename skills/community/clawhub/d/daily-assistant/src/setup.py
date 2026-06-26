"""
日常小助手 MCP Server — 初始化脚本 v3

两种模式：
  --auto    全自动（零交互，默认路径，自动创建 venv，自动配置编辑器）
  无参数     交互式（询问路径，打印配置模板）

自动完成：
1. 创建 .venv 并安装 fastmcp（用户无需手动 pip install）
2. 创建数据目录（Daily/ + Dashboard.md）
3. 生成 config.json
4. 检测已安装的 AI 编辑器，自动写入 MCP 配置

支持的编辑器：Claude Code / Cursor / Kiro / Windsurf

用法（一条命令搞定）:
    macOS/Linux:  git clone ... && cd ... && python3 src/setup.py --auto
    Windows:      git clone ... && cd ... && py src/setup.py --auto
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
SERVER_PATH = SCRIPT_DIR / "server.py"
VENV_DIR = PROJECT_DIR / ".venv"


# ─── venv + fastmcp 安装 ─────────────────────────────────────

def get_venv_python() -> Path:
    """获取 .venv 中的 Python 可执行文件路径。"""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python3"


def ensure_venv() -> Path:
    """确保 .venv 存在并安装 fastmcp，返回 venv 的 python 路径。"""
    venv_python = get_venv_python()

    if venv_python.exists():
        print(f"   ⏭️  .venv 已存在: {VENV_DIR}")
    else:
        print(f"   📦 创建虚拟环境: {VENV_DIR}")
        venv.create(str(VENV_DIR), with_pip=True)
        print(f"   ✅ .venv 已创建")

    # 检查 fastmcp 是否已安装
    check = subprocess.run(
        [str(venv_python), "-c", "import fastmcp"],
        capture_output=True,
    )
    if check.returncode == 0:
        print(f"   ⏭️  fastmcp 已安装")
    else:
        print(f"   📦 安装 fastmcp...")
        result = subprocess.run(
            [str(venv_python), "-m", "pip", "install", "fastmcp"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"   ✅ fastmcp 安装成功")
        else:
            print(f"   ❌ fastmcp 安装失败:")
            print(f"      {result.stderr.strip()}")
            sys.exit(1)

    return venv_python


# ─── AI 编辑器 MCP 配置映射 ───────────────────────────────────

EDITORS = [
    {
        "name": "Claude Code",
        "config_path": Path.home() / ".claude.json",
        "detect_dir": Path.home() / ".claude",
        "detect_cmd": "claude",
        "create_parents": False,
    },
    {
        "name": "Cursor",
        "config_path": Path.home() / ".cursor" / "mcp.json",
        "detect_dir": Path.home() / ".cursor",
        "detect_cmd": None,
        "create_parents": True,
    },
    {
        "name": "Kiro",
        "config_path": Path.home() / ".kiro" / "settings" / "mcp.json",
        "detect_dir": Path.home() / ".kiro",
        "detect_cmd": None,
        "create_parents": True,
    },
    {
        "name": "Windsurf",
        "config_path": Path.home() / ".codeium" / "windsurf" / "mcp_config.json",
        "detect_dir": Path.home() / ".codeium" / "windsurf",
        "detect_cmd": None,
        "create_parents": True,
    },
]


# ─── 工具函数 ─────────────────────────────────────────────────

def detect_python_cmd() -> str:
    """检测当前 OS 的 Python 命令（用于非 venv 场景提示）。"""
    if platform.system() == "Windows":
        return "py"
    return "python3"


def build_mcp_entry(venv_python: Path | None = None) -> dict:
    """构建 daily-assistant 的 MCP Server 配置条目。

    如果提供了 venv_python，使用 venv 的 python；否则使用系统 python。
    """
    if venv_python and venv_python.exists():
        command = str(venv_python)
    else:
        command = detect_python_cmd()

    return {
        "command": command,
        "args": ["-X", "utf8", str(SERVER_PATH)],
    }


# ─── 编辑器检测与配置 ─────────────────────────────────────────

def detect_editor(editor: dict) -> bool:
    """检测某个 AI 编辑器是否已安装。"""
    if editor["config_path"].exists():
        return True
    if editor["detect_dir"] and editor["detect_dir"].is_dir():
        return True
    if editor["detect_cmd"] and shutil.which(editor["detect_cmd"]):
        return True
    return False


def merge_mcp_config(config_path: Path, entry: dict, create_parents: bool) -> None:
    """将 daily-assistant 合并写入编辑器的 MCP 配置文件。

    安全合并：读取现有 JSON → 添加/覆盖 daily-assistant → 写回。
    不会影响用户已有的其他 MCP Server 配置。
    """
    existing = {}
    if config_path.exists():
        try:
            text = config_path.read_text(encoding="utf-8").strip()
            if text:
                existing = json.loads(text)
        except (json.JSONDecodeError, OSError):
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    existing["mcpServers"]["daily-assistant"] = entry

    if create_parents:
        config_path.parent.mkdir(parents=True, exist_ok=True)

    config_path.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def configure_editors(venv_python: Path | None = None) -> tuple[list[str], list[str]]:
    """检测并配置所有已安装的 AI 编辑器。返回 (已配置列表, 跳过列表)。"""
    entry = build_mcp_entry(venv_python)
    configured = []
    skipped = []

    for editor in EDITORS:
        name = editor["name"]
        if detect_editor(editor):
            try:
                merge_mcp_config(
                    editor["config_path"], entry, editor["create_parents"]
                )
                print(f"   ✅ {name} 已配置 → {editor['config_path']}")
                configured.append(name)
            except OSError as e:
                print(f"   ⚠️ {name} 配置失败: {e}")
        else:
            print(f"   ⏭️  {name} 未检测到，跳过")
            skipped.append(name)

    return configured, skipped


# ─── 数据目录 & config.json ───────────────────────────────────

def prompt_data_dir() -> Path:
    """交互式询问数据目录位置。"""
    default = Path.home() / "Desktop" / "日常小助手"
    print(f"\n📁 数据目录将存放 Daily 文件、Dashboard 等。")
    print(f"   默认位置: {default}")
    user_input = input(f"\n   按 Enter 使用默认，或输入自定义路径: ").strip()

    if user_input:
        return Path(user_input).resolve()
    return default


def create_data_dir(data_dir: Path) -> None:
    """创建数据目录结构。"""
    daily_dir = data_dir / "Daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ 创建: {daily_dir}")

    dashboard = data_dir / "Dashboard.md"
    if not dashboard.exists():
        dashboard.write_text(
            "# 📊 日常小助手 Dashboard\n\n"
            "> 全局任务概览面板\n\n"
            "## 🔴 超期任务\n\n"
            "> 由 `check_overdue` 工具自动检测\n\n"
            "## 🟡 今日待办\n\n"
            "> 由 `get_today` 工具读取\n\n"
            "## 🟢 已完成\n\n"
            "> 由 `generate_review` 工具统计\n\n"
            "---\n\n"
            "*Dashboard 由日常小助手 MCP Server 提供数据支持*\n",
            encoding="utf-8",
        )
        print(f"   ✅ 创建: {dashboard}")
    else:
        print(f"   ⏭️  已存在: {dashboard}")


def create_config(data_dir: Path) -> None:
    """生成 config.json。"""
    config_path = SCRIPT_DIR / "config.json"
    config = {
        "daily_dir": str(data_dir / "Daily"),
        "dashboard_file": str(data_dir / "Dashboard.md"),
        "language": "zh",
    }

    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"   ✅ 生成: {config_path}")


# ─── 输出提示 ─────────────────────────────────────────────────

def print_manual_config(venv_python: Path | None = None) -> None:
    """打印手动配置模板（未检测到编辑器时使用）。"""
    entry = build_mcp_entry(venv_python)
    mcp_json = {"mcpServers": {"daily-assistant": entry}}

    print(f"\n📝 手动配置模板（复制到你的编辑器 MCP 配置文件）：")
    print(json.dumps(mcp_json, ensure_ascii=False, indent=2))
    print(f"\n   各编辑器配置文件位置：")
    for editor in EDITORS:
        print(f"   • {editor['name']}: {editor['config_path']}")


def print_next_steps_interactive(data_dir: Path) -> None:
    """交互模式的后续步骤提示。"""
    python_cmd = detect_python_cmd()

    mcp_json = {
        "mcpServers": {
            "daily-assistant": {
                "command": python_cmd,
                "args": ["-X", "utf8", str(SERVER_PATH)],
            }
        }
    }
    mcp_json_str = json.dumps(mcp_json, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"🎉 初始化完成！接下来：")
    print(f"{'='*50}")

    print(f"\n📦 步骤 1: 安装 fastmcp")
    print(f"   {python_cmd} -m pip install fastmcp")
    print(f"   或使用 --auto 模式自动创建 venv 并安装")

    print(f"\n📝 步骤 2: 配置你的 AI 编辑器")
    print(f"   将以下 JSON 合并到编辑器的 MCP 配置文件中：")
    print(f"\n{mcp_json_str}")
    print(f"\n   各编辑器配置文件位置：")
    for editor in EDITORS:
        print(f"   • {editor['name']}: {editor['config_path']}")

    print(f"\n🚀 步骤 3: 重启编辑器")
    print(f"   MCP Server 会自动加载")

    print(f"\n📅 步骤 4: 创建今日待办")
    print(f"   说: \"用 inherit_tasks 创建今天的待办\"")
    print(f"   或手动在 {data_dir / 'Daily'} 中创建 YYYY-MM-DD.md 文件")

    print(f"\n💡 任务格式:")
    print(f"   - [ ] 任务描述 ⏱️45min 📅 2026-03-30 ⏫")
    print(f"   标记: ⏱️=预估时间 📅=deadline ⏫=最高优先 🔼=高 🔽=低")


# ─── 主入口 ───────────────────────────────────────────────────

def main():
    auto_mode = "--auto" in sys.argv

    print("=" * 50)
    print("🛠️  日常小助手 MCP Server — 初始化向导")
    if auto_mode:
        print("   模式: 🚀 全自动 (--auto)")
    else:
        print("   模式: 💬 交互式")
    print("=" * 50)
    print(f"\n   系统: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   脚本目录: {SCRIPT_DIR}")

    venv_python = None

    if auto_mode:
        # ── 1. venv + fastmcp ──
        print(f"\n🐍 配置 Python 环境...")
        venv_python = ensure_venv()

        # ── 2. 数据目录 ──
        data_dir = Path.home() / "Desktop" / "日常小助手"
    else:
        data_dir = prompt_data_dir()

    print(f"\n📂 创建数据目录...")
    create_data_dir(data_dir)

    # ── 3. config.json ──
    print(f"\n⚙️  生成配置文件...")
    create_config(data_dir)

    # ── 4. 编辑器配置 ──
    if auto_mode:
        print(f"\n🔍 检测已安装的 AI 编辑器...")
        configured, skipped = configure_editors(venv_python)

        if not configured:
            print_manual_config(venv_python)

        print(f"\n{'='*50}")
        print(f"🎉 全部完成！")
        print(f"{'='*50}")

        if configured:
            print(f"\n   已配置: {', '.join(configured)}")
            print(f"   打开你的 AI 编辑器，说 \"今天做什么\" 即可开始使用。")
        else:
            print(f"\n   未检测到支持的编辑器，请手动复制上方配置模板。")

        print(f"\n💡 任务格式:")
        print(f"   - [ ] 任务描述 ⏱️45min 📅 2026-03-30 ⏫")
        print(f"   标记: ⏱️=预估时间 📅=deadline ⏫=最高优先 🔼=高 🔽=低")
    else:
        print_next_steps_interactive(data_dir)


if __name__ == "__main__":
    main()
