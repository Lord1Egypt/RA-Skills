#!/usr/bin/env python3
"""
clear_agent_rules.py — 一键清除所有 AI Agent 规则/技能文件

支持平台（50+）：
  # 主流 AI IDE
  Cursor · Windsurf(Codeium) · Cline · Trae IDE · Amazon Q · Continue.dev

  # Agent 框架 / CLI
  Claude Code · Codex CLI · GitHub Copilot · Gemini CLI · Aider · OpenCode

  # 新兴 AI 工具
  Amp · Goose · Kilo Code · Kiro (AWS) · Neovate · OpenHands · PI (pi-coding-agent) · Roo Code · Zencoder

  # OpenClaw 生态
  OpenClaw · QClaw · CoPaw · EasyClaw · ArkClaw · LobsterAI · HiClaw · AutoClaw · AntiClaw

  # 其他 AI Agent
  Manus · HappyCapy · QoderWork · Qoder · Droid (Factory)

  # WorkBuddy
  WorkBuddy/CodeBuddy

支持操作系统：Windows · macOS · Linux

用法：
  python clear_agent_rules.py [选项]

选项：
  --mode         project | global | all     清除范围（默认 all）
  --project      <路径>                      项目根目录（默认当前目录）
  --platforms    <p1,p2,...>                 指定平台，逗号分隔（默认 all）
  --no-backup                                不备份（危险，谨慎使用）
  --dry-run                                  预览模式，不实际删除
  --yes                                      跳过确认提示（非交互式执行）
  --include-self                             不保护本技能，也会清除 clear-agent-rules 本身

特性：
  - 自我保护：默认情况下不会删除 clear-agent-rules 技能本身
  - 智能扫描：只删除实际存在的文件/目录
  - 自动备份：删除前自动备份到桌面

示例：
  # 预览将被删除的内容（安全，不实际操作）
  python clear_agent_rules.py --dry-run

  # 清除当前项目 + 全局，自动备份（推荐，本技能受保护）
  python clear_agent_rules.py --mode all

  # 只清除指定平台
  python clear_agent_rules.py --platforms cursor,claude,copilot

  # 指定项目目录
  python clear_agent_rules.py --project /home/user/myproject

  # 非交互式（CI/脚本中使用）
  python clear_agent_rules.py --yes

  # 清除包括本技能在内的所有 WorkBuddy 技能（危险）
  python clear_agent_rules.py --mode global --include-self
"""

import argparse
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─── 终端颜色 ─────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
GRAY   = "\033[90m"

def c(text, color):
    """在支持颜色的终端输出彩色文本"""
    if sys.stdout.isatty() or platform.system() == "Windows":
        return f"{color}{text}{RESET}"
    return text

def section(title):
    print()
    print(c("━" * 52, CYAN))
    print(c(f"  {title}", CYAN))
    print(c("━" * 52, CYAN))

# ─── 系统路径解析 ──────────────────────────────────────────────────────────────

HOME = Path.home()
IS_WINDOWS = platform.system() == "Windows"

def home(*parts):
    return HOME.joinpath(*parts)

def docs_cline():
    """Cline 全局规则目录（跨平台）"""
    if IS_WINDOWS:
        docs = Path(os.environ.get("USERPROFILE", HOME)) / "Documents"
    else:
        docs = HOME / "Documents"
    candidates = [docs / "Cline" / "Rules", HOME / "Cline" / "Rules"]
    for c_ in candidates:
        if c_.exists():
            return c_
    return candidates[0]  # 返回主候选路径（不存在时也记录）

# ─── 规则目标定义 ──────────────────────────────────────────────────────────────
# 每条记录：
#   name     显示名称
#   platform 平台标识
#   scope    project | global
#   path     Path 对象（项目级为相对路径字符串，全局级为绝对 Path）

PROJECT_TARGETS = [
    # ===== 主流 AI IDE =====
    # Cursor
    {"name": "Cursor 旧版规则文件",            "platform": "cursor",   "path": ".cursorrules"},
    {"name": "Cursor 新版规则目录",             "platform": "cursor",   "path": ".cursor/rules"},
    # Windsurf
    {"name": "Windsurf 旧版规则文件",           "platform": "windsurf", "path": ".windsurfrules"},
    {"name": "Windsurf 新版规则目录",           "platform": "windsurf", "path": ".windsurf/rules"},
    # Cline
    {"name": "Cline 规则文件/目录",             "platform": "cline",    "path": ".clinerules"},
    # Trae IDE
    {"name": "Trae 项目规则文件",               "platform": "trae",     "path": ".trae/project_rules.md"},
    # Amazon Q
    {"name": "Amazon Q 规则目录",              "platform": "amazonq",  "path": ".amazonq/rules"},
    # Continue.dev
    {"name": "Continue 工作区配置",             "platform": "continue", "path": ".continuerc.json"},
    {"name": "Continue 规则目录",               "platform": "continue", "path": ".continue/rules"},

    # ===== Agent 框架 / CLI =====
    # Claude Code
    {"name": "Claude Code 项目指令文件",        "platform": "claude",   "path": "CLAUDE.md"},
    # Codex CLI
    {"name": "Codex CLI / 通用 AGENTS.md",     "platform": "codex",    "path": "AGENTS.md"},
    # GitHub Copilot
    {"name": "Copilot 主指令文件",              "platform": "copilot",  "path": ".github/copilot-instructions.md"},
    {"name": "Copilot 作用域规则目录",          "platform": "copilot",  "path": ".github/instructions"},
    # Gemini CLI
    {"name": "Gemini CLI 项目指令文件",         "platform": "gemini",   "path": "GEMINI.md"},
    # Aider
    {"name": "Aider 项目配置文件",              "platform": "aider",    "path": ".aider.conf.yml"},
    # OpenCode
    {"name": "OpenCode 项目规则文件",           "platform": "opencode", "path": "AGENTS.md"},
    {"name": "OpenCode CLAUDE.md 兼容文件",     "platform": "opencode", "path": "CLAUDE.md"},

    # ===== 新兴 AI 工具 =====
    # Amp
    {"name": "Amp 项目规则文件",              "platform": "amp",      "path": "AGENTS.md"},
    # Goose
    {"name": "Goose 提示文件",                "platform": "goose",    "path": ".goosehints"},
    {"name": "Goose 规则目录",                "platform": "goose",    "path": ".goose"},
    # Kilo Code
    {"name": "Kilo Code 规则目录",            "platform": "kilocode", "path": ".kilocode/rules"},
    # Kiro (AWS)
    {"name": "Kiro Steering 规则目录",         "platform": "kiro",     "path": ".kiro/steering"},
    {"name": "Kiro 配置目录",                 "platform": "kiro",     "path": ".kiro"},
    # Neovate
    {"name": "Neovate 项目规则文件",           "platform": "neovate",  "path": "AGENTS.md"},
    # OpenHands
    {"name": "OpenHands 配置文件",             "platform": "openhands", "path": "config.toml"},
    {"name": "OpenHands 项目目录",              "platform": "openhands", "path": ".openhands"},
    # PI (pi-coding-agent)
    {"name": "PI 编码代理配置文件",           "platform": "pi",       "path": ".pi/settings.json"},
    {"name": "PI 配置目录",                   "platform": "pi",       "path": ".pi"},
    # Qoder
    {"name": "Qoder 规则目录",                "platform": "qoder",    "path": ".qoder/rules"},
    # Roo Code
    {"name": "Roo Code 规则目录",             "platform": "roocode",   "path": ".roo/rules"},
    {"name": "Roo Code 规则文件",             "platform": "roocode",   "path": ".roorules"},
    # Zencoder
    {"name": "Zencoder 规则目录",             "platform": "zencoder", "path": ".zencoder/rules"},
    # Droid (Factory)
    {"name": "Factory Droid 配置目录",         "platform": "droid",    "path": ".droid"},
    {"name": "Factory Droid 规则文件",         "platform": "droid",    "path": "AGENTS.md"},

    # ===== Google Antigravity =====
    {"name": "Antigravity 规则目录",           "platform": "antigravity", "path": ".antigravity/rules.md"},

    # ===== OpenClaw 生态 =====
    # OpenClaw 项目级配置
    {"name": "OpenClaw 项目配置",              "platform": "openclaw", "path": ".openclaw/"},

    # ===== QoderWork =====
    {"name": "QoderWork 项目技能目录",         "platform": "qoderwork","path": ".qoderwork/skills"},

    # ===== WorkBuddy =====
    {"name": "WorkBuddy 项目技能目录",          "platform": "workbuddy","path": ".workbuddy/skills"},
]

GLOBAL_TARGETS = [
    # ===== 主流 AI IDE =====
    # Cursor
    {"name": "Cursor 全局规则目录",             "platform": "cursor",   "path": home(".cursor", "rules")},
    # Cline
    {"name": "Cline 全局规则目录",              "platform": "cline",    "path": docs_cline()},
    # Trae IDE
    {"name": "Trae 全局用户规则文件",           "platform": "trae",     "path": home(".trae", "user_rules.md")},
    # Continue.dev
    {"name": "Continue 全局配置目录",           "platform": "continue", "path": home(".continue")},

    # ===== Agent 框架 / CLI =====
    # Claude Code
    {"name": "Claude Code 全局指令文件",        "platform": "claude",   "path": home(".claude", "CLAUDE.md")},
    {"name": "Claude Code 全局配置目录",        "platform": "claude",   "path": home(".claude")},
    # Gemini CLI
    {"name": "Gemini CLI 全局指令文件",         "platform": "gemini",   "path": home(".gemini", "GEMINI.md")},
    # Aider
    {"name": "Aider 全局配置文件",              "platform": "aider",    "path": home(".aider.conf.yml")},
    # OpenCode
    {"name": "OpenCode 全局配置目录",           "platform": "opencode", "path": home(".config", "opencode")},
    {"name": "OpenCode 全局 AGENTS.md",        "platform": "opencode", "path": home(".config", "opencode", "AGENTS.md")},
    {"name": "OpenCode Claude 兼容目录",        "platform": "opencode", "path": home(".claude")},

    # ===== 新兴 AI 工具 =====
    # Amp
    {"name": "Amp 全局规则文件",              "platform": "amp",      "path": home(".factory", "AGENTS.md")},
    # Goose
    {"name": "Goose 配置目录",                "platform": "goose",    "path": home(".config", "goose")},
    # Kilo Code
    {"name": "Kilo Code 全局规则目录",          "platform": "kilocode", "path": home(".kilocode", "rules")},
    # Kiro (AWS)
    {"name": "Kiro 全局配置目录",             "platform": "kiro",     "path": home(".kiro")},
    {"name": "Kiro MCP 配置文件",              "platform": "kiro",     "path": home(".kiro", "mcp-config.json")},
    # Neovate
    {"name": "Neovate 全局规则文件",           "platform": "neovate",  "path": home(".neovate", "AGENTS.md")},
    # OpenHands
    {"name": "OpenHands 全局配置目录",           "platform": "openhands", "path": home(".openhands")},
    # PI (pi-coding-agent)
    {"name": "PI 编码代理全局配置",           "platform": "pi",       "path": home(".pi", "agent", "settings.json")},
    {"name": "PI 全局配置目录",               "platform": "pi",       "path": home(".pi")},
    # Roo Code
    {"name": "Roo Code 全局规则目录",          "platform": "roocode",   "path": home(".roo", "rules")},
    # Zencoder
    # （无全局配置目录，仅项目级）
    # Qoder
    # （无全局配置目录，仅项目级）

    # ===== OpenClaw 生态 =====
    # OpenClaw
    {"name": "OpenClaw 全局配置目录",           "platform": "openclaw", "path": home(".openclaw")},
    {"name": "OpenClaw 配置文件",               "platform": "openclaw", "path": home(".openclaw", "openclaw.json")},
    # QClaw (腾讯，基于 OpenClaw)
    {"name": "QClaw 配置目录",                  "platform": "qclaw",   "path": home(".openclaw")},  # 与 OpenClaw 共享
    # CoPaw (阿里)
    {"name": "CoPaw 全局配置目录",             "platform": "copaw",   "path": home(".copaw")},
    {"name": "CoPaw 配置文件",                 "platform": "copaw",   "path": home(".copaw", "config.json")},
    {"name": "CoPaw 工作区目录",               "platform": "copaw",   "path": home(".copaw", "workspaces")},
    # EasyClaw (基于 OpenClaw)
    {"name": "EasyClaw 配置目录",              "platform": "easyclaw", "path": home(".openclaw")},  # 共享
    # ArkClaw (火山引擎)
    {"name": "ArkClaw 配置目录",                "platform": "arkclaw", "path": home(".openclaw")},  # 可能共享
    # LobsterAI (网易)
    {"name": "LobsterAI 配置目录",              "platform": "lobsterai", "path": home(".openclaw")},  # 可能共享
    # HiClaw
    {"name": "HiClaw 配置目录",                 "platform": "hiclaw",  "path": home(".openclaw")},  # 可能共享
    # AutoClaw (智谱)
    {"name": "AutoClaw 配置目录",               "platform": "autoclaw", "path": home(".openclaw")},  # 可能共享
    # AntiClaw
    {"name": "AntiClaw 配置目录",               "platform": "anticlaw", "path": home(".openclaw")},  # 可能共享
    # Manus
    {"name": "Manus 配置目录",                  "platform": "manus",   "path": home(".manus")},
    # HappyCapy
    {"name": "HappyCapy 配置目录",              "platform": "happycapy", "path": home(".happycapy")},
    # Droid (Factory)
    {"name": "Factory Droid 全局配置",           "platform": "droid",    "path": home(".factory")},

    # ===== QoderWork =====
    {"name": "QoderWork 用户技能目录",         "platform": "qoderwork","path": home(".qoderwork", "skills")},

    # ===== WorkBuddy =====
    {"name": "WorkBuddy 用户技能目录",          "platform": "workbuddy","path": home(".workbuddy", "skills")},
]

ALL_PLATFORMS = [
    # 主流 AI IDE
    "cursor", "windsurf", "cline", "trae", "amazonq", "continue",
    # Agent 框架 / CLI
    "claude", "codex", "copilot", "gemini", "aider", "opencode",
    # 新兴 AI 工具
    "amp", "goose", "kilocode", "kiro", "neovate", "openhands", "pi",
    "qoder", "roocode", "zencoder", "droid",
    # OpenClaw 生态
    "openclaw", "qclaw", "copaw", "easyclaw", "arkclaw", "lobsterai",
    "hiclaw", "autoclaw", "anticlaw", "manus", "happycapy",
    # QoderWork
    "qoderwork",
    # WorkBuddy
    "workbuddy"
]

# ─── 解析参数 ──────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="一键清除所有 AI Agent 规则/技能文件",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--mode", choices=["project", "global", "all"],
                        default="all", help="清除范围（默认 all）")
    parser.add_argument("--project", default=os.getcwd(),
                        help="项目根目录路径（默认当前目录）")
    parser.add_argument("--platforms", default="all",
                        help="指定平台，逗号分隔，默认 all")
    parser.add_argument("--no-backup", action="store_true",
                        help="不备份（危险）")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式，不实际删除")
    parser.add_argument("--yes", action="store_true",
                        help="跳过确认提示（非交互式执行）")
    parser.add_argument("--include-self", action="store_true",
                        help="不保护本技能，也会清除 clear-agent-rules 本身（默认受保护）")
    return parser.parse_args()

# ─── 主逻辑 ───────────────────────────────────────────────────────────────────

def resolve_targets(mode, project_root, target_platforms, exclude_self=True):
    """收集所有符合条件的目标，返回 list of (name, platform, full_path)"""
    results = []

    # 获取当前技能的绝对路径，用于自我保护
    current_skill_path = None
    if exclude_self:
        try:
            # 获取脚本所在目录的父目录（技能根目录）
            script_dir = Path(__file__).parent.resolve()
            skill_root = script_dir.parent.resolve()
            current_skill_path = skill_root
        except Exception:
            pass

    if mode in ("project", "all"):
        for t in PROJECT_TARGETS:
            if t["platform"] not in target_platforms:
                continue
            full = project_root / t["path"]
            if full.exists():
                # 检查是否为当前技能路径
                if exclude_self and current_skill_path and full.resolve() == current_skill_path:
                    continue
                results.append({
                    "name":     t["name"],
                    "platform": t["platform"],
                    "scope":    "project",
                    "path":     full,
                })

    if mode in ("global", "all"):
        for t in GLOBAL_TARGETS:
            if t["platform"] not in target_platforms:
                continue
            full = Path(t["path"])
            if full.exists():
                # 检查是否包含当前技能路径
                if exclude_self and current_skill_path:
                    # 如果目标是目录且包含当前技能路径，则跳过
                    if full.is_dir():
                        try:
                            if current_skill_path.is_relative_to(full) or full.is_relative_to(current_skill_path):
                                continue
                        except ValueError:
                            pass
                    # 如果目标是文件且等于当前技能路径，则跳过
                    elif full == current_skill_path:
                        continue
                results.append({
                    "name":     t["name"],
                    "platform": t["platform"],
                    "scope":    "global",
                    "path":     full,
                })

    return results


def do_backup(targets, project_root):
    """将所有目标备份到桌面，返回备份目录路径"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    desktop = HOME / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    backup_root = desktop / f"agent-rules-backup-{ts}"
    backup_root.mkdir(parents=True, exist_ok=True)

    section("执行备份")
    for t in targets:
        try:
            rel = (f"project/{t['path'].relative_to(project_root)}"
                   if t["scope"] == "project"
                   else f"global/{t['path'].relative_to(HOME)}")
        except ValueError:
            rel = f"{t['scope']}/{t['path'].name}"

        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            if t["path"].is_dir():
                shutil.copytree(str(t["path"]), str(dest), dirs_exist_ok=True)
            else:
                shutil.copy2(str(t["path"]), str(dest))
            print(f"  {c('✔', GREEN)} 已备份: {t['name']}")
            print(f"      {c(str(t['path']), GRAY)}")
        except Exception as e:
            print(f"  {c('✘', RED)} 备份失败: {t['name']} — {e}")

    print()
    print(f"  {c('📦 备份保存在:', GREEN)} {backup_root}")
    return backup_root


def do_delete(targets):
    """执行删除，返回 (success_count, fail_count)"""
    section("执行清除")
    success, fail = 0, 0
    for t in targets:
        try:
            if t["path"].is_dir():
                shutil.rmtree(str(t["path"]))
            else:
                t["path"].unlink()
            print(f"  {c('✔', GREEN)} [{t['platform'].upper()}] {t['name']}")
            success += 1
        except Exception as e:
            print(f"  {c('✘', RED)} [{t['platform'].upper()}] {t['name']}")
            print(f"      {c(str(e), RED)}")
            fail += 1
    return success, fail


def main():
    args = parse_args()

    # 解析平台列表
    if args.platforms.strip().lower() == "all":
        target_platforms = ALL_PLATFORMS
    else:
        target_platforms = [p.strip().lower() for p in args.platforms.split(",")]
        invalid = [p for p in target_platforms if p not in ALL_PLATFORMS]
        if invalid:
            print(c(f"⚠ 未知平台: {', '.join(invalid)}", YELLOW))
            print(c(f"  可用平台: {', '.join(ALL_PLATFORMS)}", YELLOW))
            sys.exit(1)

    project_root = Path(args.project).resolve()

    # ── 打印摘要 ──
    section("AI Agent 规则清除工具")
    print(f"  操作系统   : {platform.system()} {platform.machine()}")
    print(f"  清除模式   : {args.mode}")
    print(f"  项目目录   : {project_root}")
    print(f"  平台数量   : {len(target_platforms)}")
    backup_flag = not args.no_backup
    print(f"  备份       : {c('是', GREEN) if backup_flag else c('否（危险！）', RED)}")
    if args.dry_run:
        print(c("  ⚡ 预览模式（--dry-run），不会实际删除任何文件", YELLOW))

    # ── 扫描 ──
    exclude_self = not args.include_self
    targets = resolve_targets(args.mode, project_root, target_platforms, exclude_self)

    # 检查是否自我保护生效
    current_skill_path = None
    try:
        script_dir = Path(__file__).parent.resolve()
        skill_root = script_dir.parent.resolve()
        current_skill_path = skill_root
    except Exception:
        pass

    section("扫描结果")
    if not targets:
        print(c("  ✅ 未发现任何 AI Agent 规则文件，已经很干净！", GREEN))
        sys.exit(0)

    # 提示自我保护
    if current_skill_path and args.mode in ("global", "all"):
        print(c(f"  🔒 已自动保护本技能: {current_skill_path}", CYAN))
        print(c("     不会被清除（可以安全使用本工具清理其他平台）", CYAN))
        print()

    print(c(f"  发现 {len(targets)} 个规则文件/目录：", YELLOW))
    for t in targets:
        icon = "📁" if t["path"].is_dir() else "📄"
        scope_tag = c(f"[{t['scope']}]", CYAN)
        plat_tag  = c(f"[{t['platform'].upper()}]", YELLOW)
        print(f"  {icon} {scope_tag} {plat_tag} {t['name']}")
        print(f"      {c(str(t['path']), GRAY)}")

    if args.dry_run:
        print()
        print(c("  ℹ️  预览模式结束，以上文件未被删除。", CYAN))
        print(c("     去掉 --dry-run 参数即可执行实际删除。", CYAN))
        sys.exit(0)

    # ── 确认 ──
    print()
    print(c(f"⚠️  即将删除以上 {len(targets)} 个文件/目录！", RED + BOLD))
    if backup_flag:
        print(c("   删除前将自动备份到桌面。", GREEN))

    if not args.yes:
        confirm = input("确认继续？输入 YES 继续，其他任意键取消：").strip()
        if confirm != "YES":
            print(c("已取消操作。", CYAN))
            sys.exit(0)

    # ── 备份 ──
    backup_root = None
    if backup_flag:
        backup_root = do_backup(targets, project_root)

    # ── 删除 ──
    success, fail = do_delete(targets)

    # ── 报告 ──
    section("清除完成")
    print(c(f"  ✅ 成功删除: {success} 个", GREEN))
    if fail:
        print(c(f"  ❌ 失败: {fail} 个", RED))
    if backup_root:
        print(c(f"  📦 备份位置: {backup_root}", CYAN))
    print()


if __name__ == "__main__":
    main()
