#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能锻造炉 (SkillForge) — 自带发布器 forge-publish.py

让「技能锻造炉」锻造出的技能，能由创作者本人在本地一键发布到多个技能平台，
无需记住各平台繁杂的发布命令。本脚本随「技能锻造炉」技能包分发，纯标准库、
零第三方依赖，任何装了 Python 的机器都能跑。

支持平台:
    - skillhub  (现支持)   https://skillhub.cn
    - clawhub   (现支持)
    - github    (roadmap, 接口已预留)
    - gitee     (roadmap, 接口已预留)

首次使用:
    1. 进入你锻造好的技能目录（含 SKILL.md）
    2. 运行:  python forge-publish.py --check           # 本地校验
    3. 运行:  python forge-publish.py --platform both --changelog "你的更新说明"
    4. 若提示某平台 CLI 未安装/未登录，按脚本打印的引导完成一次性准备即可

零密钥云端（方案C）:
    本脚本沿用藏经阁·易筋单版本双模态模型。技能包分发时 cloud_config.json 仅含
    公网 URL（零密钥），终端用户零配置即可匿名回传（/ingest/anon）；创作者审核
    提案所需 token 存本地开发环境（.deploy/cloud_open.json），绝不进包。

安全策略:
    - 净化 config.json 中的 email 字段为 null（其余凭据原样保留）
    - 发布后自动从备份恢复本地技能目录（含 .gitignore）
    - 若技能无 config.json 但有 config.example.json，临时生成净化版用于发布，
      发布后删除，绝不在本地留痕
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Optional

# ============================================================
# 路径与常量
# ============================================================
SKILLS_BASE = Path.home() / ".workbuddy" / "skills"
# 本脚本所在目录（技能锻造炉 scripts/），用于指向同目录的 forge-register.py
FORGE_SCRIPTS = Path(__file__).resolve().parent
# 云端接入配置（方案C·零密钥）：cloud_config.json 仅含公网 URL，不含 token（SkillHub 拒绝点号隐藏文件）
CLOUD_CONFIG_FILE = "cloud_config.json"
# 端点全部来自 cloud_config.json（随包分发，仅公网 URL、零密钥）；此处不硬编码任何 URL。
DEFAULT_PROPOSAL_URL = None  # 部署 cjg-proposal 后由 --proposal-url 注入；旧包留空兼容
SKILLHUB_API_HOST = "https://api.skillhub.cn"
SKILLHUB_CREDENTIALS = Path.home() / ".skillhub" / "credentials.json"
SKILLHUB_PYTHON = "python"
# 发布包绝不可包含的运行时/密钥点文件（RC2/B2/#14 根治）。
# 与 forge-signal-kit.py 的 RUNTIME_POINT_FILES 同源（信号运行时点文件），本列表额外含
# .deploy（创作者 token 目录，零密钥模型下绝不进包）。两处须保持同步。
SKILLHUB_EXCLUDE_FILES = [".gitignore", ".cloud_token", ".cloud_config",
                          ".cloud_optin", ".optin", ".anon_id",
                          ".errored_ids.txt", ".upload_zero_rounds",
                          ".uploaded_ids.txt", "signals-log.jsonl",
                          ".skill_edit_baseline.json", ".capture.lock",
                          ".session_state.json", ".session_hook.lock",
                          ".apply-snapshots",
                          "cloud-enhancement",
                          ".deploy"]
EMAIL_FIELD_HINTS = ("email", "mail", "_email", "contact_email")
_GENERATED = "__GENERATED__"

# 跨 agent 适配（roadmap，接口预留，暂不实现转换）
# 未来 --format {workbuddy, claude, codex} 会把 SKILL.md 转成目标 agent 格式再发
SUPPORTED_FORMATS = ["workbuddy"]


# ============================================================
# 工具函数
# ============================================================
def _read_frontmatter(skill_md: Path) -> dict:
    """读取 SKILL.md frontmatter 为 dict（简单 YAML 解析，仅支持平铺 key: value）"""
    if not skill_md.exists():
        return {}
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            data[key] = val
    return data


def read_version(skill_dir: Path) -> Optional[str]:
    v = _read_frontmatter(skill_dir / "SKILL.md").get("version")
    if v and re.match(r"^\d+(\.\d+){0,2}$", v):
        return v
    return None


def read_field(skill_dir: Path, field: str) -> Optional[str]:
    return _read_frontmatter(skill_dir / "SKILL.md").get(field)


def to_semver(version: str) -> str:
    parts = version.split(".")
    if len(parts) == 2:
        return f"{version}.0"
    return version


def ensure_frontmatter(skill_dir: Path, slug: str, display_name: str) -> bool:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    content = skill_md.read_text(encoding="utf-8")
    modified = False
    if not re.search(r"^slug:\s*\S+", content, re.MULTILINE):
        content = re.sub(r"(^---\n)", f"\\1slug: {slug}\n", content, count=1,
                         flags=re.MULTILINE)
        modified = True
    if display_name and not re.search(r"^displayName:\s*\S+", content, re.MULTILINE):
        content = re.sub(r"(^slug:.*\n)", f"\\1displayName: {display_name}\n",
                         content, count=1, flags=re.MULTILINE)
        modified = True
    if modified:
        skill_md.write_text(content, encoding="utf-8")
    return modified


def _is_email_field(key: str) -> bool:
    kl = key.lower()
    return any(hint in kl for hint in EMAIL_FIELD_HINTS)


def generic_sanitize_config(skill_dir: Path) -> dict:
    """净化 config.json：email 字段置 null；无 config 但有 example 则临时生成。"""
    src = skill_dir / "config.json"
    example = skill_dir / "config.example.json"
    backup: dict = {}
    if src.exists():
        dst = Path(tempfile.gettempdir()) / f"_forgepub_{skill_dir.name}_config.json"
        shutil.copy2(src, dst)
        backup["config.json"] = dst
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        changed = False
        for k in list(data.keys()):
            if _is_email_field(k) and data.get(k) is not None:
                data[k] = None
                changed = True
        if changed:
            src.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return backup
    if example.exists():
        try:
            data = json.loads(example.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        for k in list(data.keys()):
            if _is_email_field(k):
                data[k] = None
        src.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        backup["config.json"] = _GENERATED
        return backup
    return backup


def backup_and_remove(skill_dir: Path, filenames: list) -> dict:
    """临时移走发布排除项（文件/目录都支持：目录用 copytree+rmtree），发布后 restore_files 还原。

    原子性：中途任何一项失败 → 立即还原已移走项再抛出异常（防止技能目录缺件、备份散落 /tmp）。
    """
    backups = {}
    try:
        for fname in filenames:
            src = skill_dir / fname
            if not src.exists():
                continue
            dst = Path(tempfile.gettempdir()) / f"_forgepub_{skill_dir.name}_{fname}"
            # 幂等：上次异常残留的同名备份先清，避免 copytree 目标已存在导致本次发布失败
            if dst.exists():
                if dst.is_dir():
                    shutil.rmtree(dst)
                else:
                    dst.unlink(missing_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst)
                shutil.rmtree(src)
            else:
                shutil.copy2(src, dst)
                src.unlink()
            backups[fname] = dst
    except Exception:
        restore_files(skill_dir, backups)
        raise
    return backups


def restore_files(skill_dir: Path, backups: dict):
    for fname, backup_path in backups.items():
        dst = skill_dir / fname
        if backup_path == _GENERATED:
            dst.unlink(missing_ok=True)
            continue
        if backup_path.is_dir():
            # 目标残留（如原目录删除失败）时先清，以备份为准还原，保证可重入
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(backup_path, dst)
            shutil.rmtree(backup_path)
        else:
            shutil.copy2(backup_path, dst)
            backup_path.unlink(missing_ok=True)


def _skillhub_ignore_match(skill_dir: Path, rel: str) -> bool:
    """解析 <skill_dir>/.skillhubignore（类 .gitignore，逐行相对路径/目录名），
    命中返回 True（应排除）。文件不存在/格式错 → 不命中。"""
    p = skill_dir / ".skillhubignore"
    if not p.exists():
        return False
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pat = line.rstrip("/")
            if rel == pat or rel.startswith(pat + "/") or os.path.basename(rel) == pat:
                return True
    except Exception:
        pass
    return False


def verify_pack_clean(skill_dir: Path) -> list:
    """打包干净验证（P0-1 硬闸门）：模拟平台 CLI 的打包方式（os.walk + 排除规则），
    返回「本会被打进包」的运行时点文件/目录清单（空=干净）。
    与 SKILLHUB_EXCLUDE_FILES + .skillhubignore 同源规则，确保 backup_and_remove
    之后目录里确实不再残留任何禁包文件。返回非空即阻断发布。"""
    leaked = []
    for root, dirs, files in os.walk(skill_dir):
        rel_root = Path(root).relative_to(skill_dir)
        # 目录级排除（如 .apply-snapshots / cloud-enhancement / .deploy）
        for d in list(dirs):
            rel_d = str(rel_root / d).replace("\\", "/")
            if d in SKILLHUB_EXCLUDE_FILES or _skillhub_ignore_match(skill_dir, rel_d):
                leaked.append(rel_d + "/")
                dirs.remove(d)
        for fn in files:
            full = Path(root) / fn
            rel = str(rel_root / fn).replace("\\", "/")
            if fn in SKILLHUB_EXCLUDE_FILES or _skillhub_ignore_match(skill_dir, rel):
                leaked.append(rel)
    return leaked


def get_skillhub_token() -> Optional[str]:
    try:
        creds = json.loads(SKILLHUB_CREDENTIALS.read_text(encoding="utf-8"))
        return creds.get("user", {}).get("token")
    except Exception:
        return None


# footer/coverage.md 是锻造炉产物的标记：发布时必须带信号套件闭环，缺则阻断（P0-3）
FORGE_FOOTER_RE = re.compile(r"由[「『]?技能锻造炉[」』]?")


def _is_forge_product(skill_dir: Path) -> bool:
    """识别「锻造炉产物」：SKILL.md 含 footer（『由技能锻造炉』）或存在 references/coverage.md。

    锻造炉产出的技能被当作自锻成品：能力再完整，发布时也必须带信号回传套件（闭环），
    否则终端用户拿到的是「无回传能力」的断链技能——与 A.0 同类病根（能力完整但默认不触发）。
    """
    try:
        md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    except Exception:
        md = ""
    if FORGE_FOOTER_RE.search(md):
        return True
    if (skill_dir / "references" / "coverage.md").exists():
        return True
    return False


def notice_registration(skill_dir: Path, slug: str):
    """发布前提示：若本技能 slug 尚未注册（无 .deploy/cloud_open.json 的创作者 token），
    跨用户真实反馈闭环（信号→蒸馏→提案→重发布）未激活，引导用 forge-register.py 注册。
    非阻塞——本地发布仍照常进行。"""
    open_path = skill_dir / ".deploy" / "cloud_open.json"
    token = None
    if open_path.exists():
        try:
            token = json.loads(open_path.read_text(encoding="utf-8")).get("signal_token")
        except Exception:
            token = None
    if not token:
        print(f"\n  ℹ️  云进化提示：slug「{slug}」尚未注册（缺 .deploy/cloud_open.json 的创作者 token）。")
        print(f"      跨用户真实反馈闭环（信号→蒸馏→提案→重发布）未激活。")
        print(f"      注册（需验证邮箱）：python {FORGE_SCRIPTS / 'forge-register.py'} register")
        print(f"      本机技能目录即：{skill_dir}")


# ============================================================
# 平台 CLI 定位
# ============================================================
def _find_skillhub_cli() -> Optional[Path]:
    p = shutil.which("skills_store_cli.py")
    if p:
        return Path(p)
    c = Path.home() / ".skillhub" / "skills_store_cli.py"
    return c if c.exists() else None


def _find_clawhub_cli() -> Optional[Path]:
    for cand in ("clawhub", "clawhub.cmd"):
        p = shutil.which(cand)
        if p:
            return Path(p)
    ws = Path.home() / ".workbuddy" / "binaries" / "node" / "workspace" / "node_modules" / ".bin" / "clawhub.cmd"
    if ws.exists():
        return ws
    base = Path.home() / ".workbuddy" / "binaries" / "node" / "versions"
    if base.exists():
        for d in sorted(base.iterdir(), reverse=True):
            c = d / "clawhub.cmd"
            if c.exists():
                return c
    return None


# ============================================================
# SkillHub 平台审核延迟规则（固化 2026-07-30）
# 发布成功即视为已发布；平台审核有延迟，latestVersion 不会立即变化。
# 严禁：① 发后立即重查 install/latestVersion（必显旧版）
#       ② 因 latest 未变而重发 / bump 版本号（触发 VERSION_EXISTS 孤儿版本）
# ============================================================
SKILLHUB_REVIEW_NOTE = (
    "    ── SkillHub 平台审核提示 ──\n"
    "    ① 已提交 v{}，平台需审核一段时间才会成为默认安装版本（latestVersion 不会立即变化，属正常）。\n"
    "    ② ⚠️ 切勿因 latest 未变而立即重查 install / latestVersion，或因此重发 / bump 版本号\n"
    "       —— 会触发 VERSION_EXISTS 孤儿版本，反而无法提升默认版本。\n"
    "    ③ 请稍后（建议隔数小时 / 隔天）到 SkillHub 创作者后台查看审核是否通过；通过后即成为默认版本。"
)


def yunding_audit_gate(skill_dir: Path) -> tuple:
    """纪律 17 云鼎实验室安全审计闸门（仅 SkillHub 发布路径前置）。
    返回 (block: bool, message: str)；block=True 时调用方须拒绝发布。"""
    sec = skill_dir / "references" / "security-audit.md"
    if not sec.exists():
        return (False, "⚠ 未检测到 references/security-audit.md（未跑云鼎 skills-security-check）。"
                        " 发 SkillHub 前建议先过审计；本次放行。")
    try:
        stext = sec.read_text(encoding="utf-8")
    except Exception:
        return (False, "⚠ security-audit.md 读取失败，跳过云鼎闸门（非阻断）。")
    # 判定用语义短语（仅在结论「使用建议」段出现），避免朴素子串误命中报告模板文字
    if "严禁使用" in stext:
        return (True, "✗ 云鼎审计结论为 Malicious（0-30分）——硬阻断，拒绝发布。"
                        " 请回退 S2/S6 重做并消除投毒风险后重试。")
    if "建议改进后使用" in stext:
        return (False, "⚠ 云鼎审计结论为 Suspicious（31-75分）——附整改说明经确认后可发；"
                         " 建议先修复（固定依赖版本/venv/checksum）再发 SkillHub。")
    if "可以安全使用" in stext:
        return (False, "✓ 云鼎审计结论为 Benign（76-100分），通过。")
    return (False, "⚠ security-audit.md 未检出明确结论，跳过云鼎闸门（非阻断）。")


def publish_skillhub(skill_dir: Path, slug: str, version: str,
                     changelog: str, dry_run: bool = False) -> bool:
    print(f"  [SkillHub] Publishing {skill_dir.name} v{version} ...")
    # 纪律 17 云鼎安全审计闸门（SkillHub 发布前置）
    block, msg = yunding_audit_gate(skill_dir)
    print(f"  [云鼎审计] {msg}")
    if block:
        return False
    ensure_frontmatter(skill_dir, slug, "")
    backups: dict = {}
    try:
        backups.update(backup_and_remove(skill_dir, SKILLHUB_EXCLUDE_FILES))
        backups.update(generic_sanitize_config(skill_dir))
        # P0-1 硬闸门：backup_and_remove 之后目录必须无任何禁包运行时点文件/目录
        leaked = verify_pack_clean(skill_dir)
        if leaked:
            print(f"    ✗ 打包干净校验失败（以下文件会泄漏进包，阻断发布）: {leaked}")
            print(f"       这些文件本应被 backup_and_remove 移走——请检查 SKILLHUB_EXCLUDE_FILES 与技能目录。")
            return False
        cmd = [
            SKILLHUB_PYTHON, str(_find_skillhub_cli()), "publish", str(skill_dir),
            "--version", version, "--changelog", changelog,
            "--host", SKILLHUB_API_HOST,
        ]
        if dry_run:
            cmd.append("--dry-run")
        token = get_skillhub_token()
        if token:
            cmd.extend(["--token", token])
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                timeout=120, env=env)
        if result.returncode == 0:
            out = (result.stdout or result.stderr).strip().lstrip("✓ ").lstrip("✗ ")
            print(f"    ✓ {out}")
            print(SKILLHUB_REVIEW_NOTE.format(version))
            return True
        else:
            stderr = result.stderr.strip() or result.stdout.strip()
            if "已被 clawhub 来源占用" in stderr:
                print(f"    ✗ slug 被 ClawHub 第三方占用（非本账号，无法覆盖）：{stderr}")
                print(f"       → 请换一个不冲突的 slug（默认从 SKILL.md frontmatter 读取）")
                return False
            elif "已存在" in stderr or "VERSION_EXISTS" in stderr:
                # 固化规则：版本已在平台（审核中/已存在），无需重发，请勿 bump 重复发布
                print(f"    ⚠️ 版本 {version} 已在平台（审核中或已存在），无需重发，请勿 bump 版本号重复发布。")
                print(f"       → 稍后到 SkillHub 创作者后台查看审核状态即可。")
                return True
            elif "频率过高" in stderr or "过于频繁" in stderr:
                print(f"    ⚠ 触发限流，请稍后重试")
                return False
            else:
                print(f"    ✗ {stderr}")
                return False
    finally:
        restore_files(skill_dir, backups)


def publish_clawhub(skill_dir: Path, slug: str, version: str,
                   changelog: str, dry_run: bool = False) -> bool:
    print(f"  [ClawHub] Publishing {slug} v{version} ...")
    ensure_frontmatter(skill_dir, slug, "")
    backups = generic_sanitize_config(skill_dir)
    backups.update(backup_and_remove(skill_dir, SKILLHUB_EXCLUDE_FILES))
    # P0-1 硬闸门：backup_and_remove 之后目录必须无任何禁包运行时点文件/目录
    leaked = verify_pack_clean(skill_dir)
    if leaked:
        print(f"    ✗ 打包干净校验失败（以下文件会泄漏进包，阻断发布）: {leaked}")
        print(f"       这些文件本应被 backup_and_remove 移走——请检查 SKILLHUB_EXCLUDE_FILES 与技能目录。")
        restore_files(skill_dir, backups)
        return False
    # ClawHub CLI v0.23.0+ 兼容：若技能目录含 .claude-plugin/plugin.json，会被误识别为
    # plugin 而强制走 `package publish`（需 openclaw.plugin.json），导致发布失败。
    # 这里临时挪开该文件，走 skill 发布路径（读 SKILL.md），发布后还原。
    plugin_json = skill_dir / ".claude-plugin" / "plugin.json"
    plugin_bak = skill_dir / ".claude-plugin" / "plugin.json.clawhub-bak"
    plugin_moved = False
    if plugin_json.exists():
        try:
            plugin_json.rename(plugin_bak)
            plugin_moved = True
        except Exception:
            pass
    try:
        # 新语法：clawhub publish <path> [--slug --name --version --changelog ...]
        cmd = [
            str(_find_clawhub_cli()), "publish", str(skill_dir),
            "--slug", slug, "--name", slug,
            "--version", version, "--changelog", changelog,
        ]
        if dry_run:
            print(f"    (dry-run) 将执行: {' '.join(cmd)}")
            return True
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                timeout=120, env=env)
        if result.returncode == 0:
            print(f"    ✓ {(result.stdout or result.stderr).strip()}")
            return True
        else:
            stderr = result.stderr.strip() or result.stdout.strip()
            if "已被" in stderr and "占用" in stderr:
                print(f"    ✗ slug 被占用：{stderr}")
                return False
            print(f"    ✗ {stderr}")
            return False
    finally:
        if plugin_moved and plugin_bak.exists():
            try:
                plugin_bak.rename(plugin_json)
            except Exception:
                pass
        restore_files(skill_dir, backups)


# ============================================================
# 平台注册表（可扩展：github/gitee 接口预留）
# ============================================================
PLATFORMS = {
    "skillhub": {
        "status": "ready",
        "cli_resolver": _find_skillhub_cli,
        "publish": publish_skillhub,
        "setup_help": (
            "  SkillHub 首次准备:\n"
            "    1. 安装 SkillHub CLI（见 https://skillhub.cn 文档，或从 WorkBuddy 技能市场获取）\n"
            "    2. 登录后凭证自动写入 ~/.skillhub/credentials.json（含 user.token）\n"
            "    3. 验证: python ~/.skillhub/skills_store_cli.py --help"
        ),
    },
    "clawhub": {
        "status": "ready",
        "cli_resolver": _find_clawhub_cli,
        "publish": publish_clawhub,
        "setup_help": (
            "  ClawHub 首次准备:\n"
            "    1. 安装 ClawHub CLI: npm i -g clawhub  (或 WorkBuddy 内置)\n"
            "    2. 登录: clawhub login   （clawhub whoami 验证登录状态）\n"
            "    3. 注意 slug 全局唯一，发布前先确认未被他人占用"
        ),
    },
    "github": {
        "status": "planned",
        "setup_help": (
            "  GitHub 发布 (roadmap): 计划把技能仓库推送到 GitHub 并自动生成 Release。\n"
            "  接口已预留，敬请期待。当前可用 clawhub/skillhub 分发后，在 GitHub 镜像仓库。"
        ),
    },
    "gitee": {
        "status": "planned",
        "setup_help": (
            "  Gitee 发布 (roadmap): 计划把技能仓库推送到 Gitee 并自动生成 Release。\n"
            "  接口已预留，敬请期待。"
        ),
    },
}


# ============================================================
# 首次准备引导
# ============================================================
def preflight_platform(name: str) -> list:
    """返回某平台的准备告警；空列表=就绪"""
    info = PLATFORMS.get(name, {})
    if info.get("status") != "ready":
        return [f"平台 {name} 尚未支持（roadmap）"]
    warns = []
    cli = info["cli_resolver"]()
    if not cli or not cli.exists():
        warns.append(f"{name} CLI 未找到")
    else:
        if name == "skillhub" and not SKILLHUB_CREDENTIALS.exists():
            warns.append(f"SkillHub 凭证缺失: {SKILLHUB_CREDENTIALS}")
    return warns


def print_setup_help(name: str):
    info = PLATFORMS.get(name, {})
    help_text = info.get("setup_help", f"  {name} 准备引导未提供")
    print(f"\n--- {name} 首次准备引导 ---")
    print(help_text)
    print()


# ============================================================
# 本地校验（--check，不触网）
# ============================================================
def check_only(skill_dir: Path, slug_hint: str, require_register: bool = False) -> int:
    print(f"\n{'='*60}")
    print(f"本地校验 (--check): {skill_dir}")
    print(f"{'='*60}")

    if not (skill_dir / "SKILL.md").exists():
        print(f"  ✗ 缺失 SKILL.md")
        return 1

    fm = _read_frontmatter(skill_dir / "SKILL.md")
    slug = fm.get("slug") or slug_hint
    display = fm.get("displayName") or "(无)"
    version = fm.get("version") or "(无)"

    print(f"  slug        : {slug}")
    print(f"  displayName : {display}")
    print(f"  version     : {version}")

    ok = True
    if not slug:
        print("  ✗ frontmatter 缺 slug（将无法通过 ClawHub --slug）")
        ok = False
    if version == "(无)" or not re.match(r"^\d+(\.\d+){0,2}$", str(version)):
        print("  ✗ frontmatter 缺合法 version")
        ok = False

    print(f"\n  双模态校验 (单版本双模态模型):")
    try:
        md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    except Exception:
        md = ""
    has_local = ("本地" in md) and ("记录" in md or "信号" in md)
    has_cloud = ("云端" in md) and ("上传" in md or "回传" in md)
    if has_local and has_cloud:
        print("    ✓ §零 含双模态说明（本地记录 + 云端上传）")
    elif has_local:
        print("    ℹ §零 仅本地记录（Tier 1 / 纯本地进化，无云端说明）")
    else:
        print("    ⚠ §零 未检出明确本地/云端信号说明")
    has_tier2 = ("🔄" in md) and ("⚙️" in md)
    if has_tier2:
        print("    ✓ footer Tier 2（⚙️ + 🔄 持续迭代）")
    else:
        print("    ℹ footer 未含 Tier 2 标记（⚙️+🔄），视为 Tier 1")
    if has_tier2:
        tok = skill_dir / CLOUD_CONFIG_FILE
        if not tok.exists():
            print("    ⚠ Tier 2 但 cloud_config.json 缺失 → 云端上传将降级失效（终端用户说『别传了』即纯本地）")
        else:
            try:
                cc = json.loads(tok.read_text(encoding="utf-8"))
            except Exception:
                cc = {}
            # 方案C 回归校验：零密钥包，cloud_config.json 不得含 token
            if "token" in cc:
                print("    ✗ cloud_config.json 含 token 字段（方案C 已禁止包内明文 token，包零密钥）")
                ok = False
            else:
                print("    ✓ cloud_config.json 存在且仅含公网 URL（零密钥，符合方案C）")

    src = skill_dir / "config.json"
    example = skill_dir / "config.example.json"
    print(f"  config.json : {'存在' if src.exists() else '缺失'}")
    if src.exists():
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
            emails = [k for k in data if _is_email_field(k) and data.get(k) is not None]
            print(f"    将清空 email 字段: {emails if emails else '无'}")
        except Exception as e:
            print(f"    ⚠ config.json 解析失败: {e}")
    elif example.exists():
        print("    将从 config.example.json 临时生成净化版（发布后删除）")
    else:
        print("    无 config 文件，跳过净化")

    print(f"\n  CLI 可用性:")
    any_warn = False
    for name in ("skillhub", "clawhub"):
        for w in preflight_platform(name):
            print(f"    ⚠ [{name}] {w}")
            any_warn = True
    if not any_warn:
        print("    ✓ SkillHub / ClawHub CLI 均可用")

    # ---- S8 可推广闸门校验（纪律 16，警告不阻塞）----
    print(f"\n  S8 可推广闸门校验 (纪律 16, 分发就绪):")
    refs = skill_dir / "references"
    disc = refs / "discovery.md"
    intro = refs / "intro.md"
    if not disc.exists():
        print("    ⚠ references/discovery.md 缺失（建议分类映射未落，发布后平台难正确归类）")
    else:
        dtext = disc.read_text(encoding="utf-8")
        if "needs_api_key" not in dtext:
            print("    ⚠ discovery.md 未声明 needs_api_key 系统标签")
        else:
            print("    ✓ discovery.md 存在且含 needs_api_key 标注")
    if not intro.exists():
        print("    ⚠ references/intro.md 缺失（跨平台 ≤1024 字符介绍未提供）")
    else:
        itext = intro.read_text(encoding="utf-8")
        n = len(itext)
        if n > 1024:
            print(f"    ✗ intro.md 字符数 {n} 超出 ≤1024 上限（UTF-8 计，含标点空格）")
            ok = False
        else:
            print(f"    ✓ intro.md 存在，字符数 {n}/1024（≤1024 跨平台介绍）")

    # ---- 纪律 17 云鼎安全审计状态（SkillHub 路径参考，警告不阻塞）----
    print(f"\n  纪律 17 云鼎安全审计状态:")
    sec = refs / "security-audit.md"
    if not sec.exists():
        print("    ⚠ references/security-audit.md 缺失（未跑云鼎 skills-security-check；发 SkillHub 前建议先过审计）")
    else:
        stext = sec.read_text(encoding="utf-8")
        if "严禁使用" in stext:
            print("    ✗ security-audit.md 结论为 Malicious —— SkillHub 发布将被硬阻断，须回退重做")
            ok = False
        elif "建议改进后使用" in stext:
            print("    ⚠ security-audit.md 结论为 Suspicious —— 附整改说明经确认后可发（SkillHub 路径建议先修）")
        elif "可以安全使用" in stext:
            print("    ✓ security-audit.md 结论为 Benign（云鼎审计通过）")
        else:
            print("    ⚠ security-audit.md 未检出明确结论（Benign/Suspicious/Malicious），请确认")

    # ---- 信号闭环完整性（P1-2 + P0-3：锻造炉产物 B 的信号套件必须闭环，缺则阻断发布）----
    if (skill_dir / "references" / "signals.md").exists():
        print(f"\n  信号闭环完整性 (forge-signal-kit --check):")
        try:
            r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                             "forge-signal-kit.py"),
                                "--check", str(skill_dir)], capture_output=True, text=True, timeout=60)
            loop_ok = r.returncode == 0
            if loop_ok:
                print("    ✓ 闭环完整（套件/引用/slug/状态/信号段）")
            else:
                last = [l for l in r.stdout.splitlines() if l.strip()][-1] if r.stdout else "未知"
                print(f"    ✗ 闭环断裂：{last}")
            ok = ok and loop_ok
        except Exception as e:
            print(f"    ⚠ 闭环校验执行异常: {e}")
    elif _is_forge_product(skill_dir):
        # P0-3：锻造炉产物但缺信号套件 → 硬阻断（防「能力完整但无回传」的断链技能流入终端用户）
        print(f"\n  信号闭环: ✗ 本技能是锻造炉产物（footer 含『由技能锻造炉』或存在 coverage.md），"
              f"但缺 references/signals.md")
        print(f"    → 锻造炉产物发布必须带信号回传套件（闭环），缺则阻断发布。")
        print(f"      修复: python {FORGE_SCRIPTS / 'forge-signal-kit.py'} inject {skill_dir}")
        ok = False
    else:
        print(f"\n  信号闭环: 本技能无 signals.md 且非锻造炉产物（第三方技能），跳过闭环校验")

    # ---- 注册状态检查（P1-3：跨会话持久化 · .deploy/cloud_open.json · S8 发布前闸门）----
    print(f"\n  注册状态（跨会话持久化 · .deploy/cloud_open.json）:")
    dep = skill_dir / ".deploy" / "cloud_open.json"
    reg_ok = False
    if not dep.exists():
        print("    ⚠ 未注册（.deploy/cloud_open.json 缺失）——该技能将无跨用户信号闭环")
        print("      注册: python scripts/forge-register.py register → verify")
    else:
        try:
            reg = json.loads(dep.read_text(encoding="utf-8"))
            rslug = reg.get("slug", "")
            rtoken = reg.get("token") or reg.get("signal_token") or ""
            reg_ok = bool(rslug and rtoken)
            if not reg_ok:
                print(f"    ⚠ 注册文件不完整（slug={rslug or '空'} token={'有' if rtoken else '空'}）")
            elif rslug != slug:
                print(f"    ✗ 注册 slug 不匹配：文件={rslug} 本技能={slug}（防错配——注册了 A 却发布 B）")
                reg_ok = False
            else:
                print(f"    ✓ 已注册（slug={rslug}）——跨用户信号闭环就绪")
        except Exception as e:
            print(f"    ⚠ 注册文件解析失败: {e}")
    if require_register and not reg_ok:
        print("    ✗ --require-register 已开启但技能未注册，阻断发布")
        ok = False

    # ---- 打包干净预检（P0-1，警告不阻断：发布时 backup_and_remove 自动移走）----
    leaked = verify_pack_clean(skill_dir)
    if leaked:
        print(f"\n  打包干净预检（P0-1）：以下运行时点文件/目录本会被打进包，"
              f"发布时 backup_and_remove 会自动移走（--check 不阻断）:")
        for lf in leaked:
            print(f"    - {lf}")
    else:
        print(f"\n  打包干净预检（P0-1）：✓ 无运行时点文件残留（发布即干净）")
    print(f"{'✅ 校验通过，可发布' if ok else '⚠️ 校验有缺失，请先补全 frontmatter'}")
    print(f"{'='*60}\n")
    return 0 if ok else 1


# ============================================================
# 主流程
# ============================================================
def resolve_skill_dir(args) -> Optional[Path]:
    if args.path:
        p = Path(args.path).expanduser().resolve()
        return p if p.exists() else None
    if args.skill:
        p = SKILLS_BASE / args.skill
        return p if p.exists() else None
    # 默认：当前工作目录（用户 cd 进自己锻造的技能目录后直接运行）
    cwd = Path.cwd()
    if (cwd / "SKILL.md").exists():
        return cwd
    return None


def main():
    parser = argparse.ArgumentParser(
        description="技能锻造炉自带发布器：一键发布到 SkillHub / ClawHub（GitHub/Gitee 规划中）")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--skill", help="技能 slug（从 ~/.workbuddy/skills/<slug> 读取）")
    g.add_argument("--path", help="技能目录绝对路径（默认：当前目录，需含 SKILL.md）")
    parser.add_argument("--platform", default="both",
                        choices=["skillhub", "clawhub", "both", "github", "gitee"],
                        help="目标平台 (default: both)")
    parser.add_argument("--changelog", default=None, help="发布 changelog（站用户侧：改了什么 + 价值，禁生产侧文案）")
    parser.add_argument("--version", default=None, help="覆盖版本号（默认读 frontmatter）")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不真正上线")
    parser.add_argument("--force", action="store_true",
                        help="changelog 含生产侧文案时仍发布（默认拒绝，防内部文案外泄）")
    parser.add_argument("--check", action="store_true",
                        help="仅本地校验（不调用网络/CLI）")
    parser.add_argument("--require-register", action="store_true",
                        help="强制要求技能已注册（.deploy/cloud_open.json 存在+slug 匹配+token 非空），否则阻断发布")
    parser.add_argument("--slug", default=None, help="覆盖 slug（默认读 frontmatter）")
    # 方案C：--token 已移除，发布工具不再向包内注入任何 token（包零密钥）
    parser.add_argument("--ingest-url", default=None,
                        help="signal-ingest 公网地址（默认内置藏经阁固定地址）")
    parser.add_argument("--proposal-url", default=None,
                        help="cjg-proposal 公网地址（查看/审核进化提案；默认不写，旧包兼容）")
    parser.add_argument("--format", default="workbuddy", choices=SUPPORTED_FORMATS,
                        help="目标 agent 格式 (default: workbuddy; claude/codex 规划中)")
    args = parser.parse_args()

    skill_dir = resolve_skill_dir(args)
    if not skill_dir:
        target = args.path or (args.skill and (SKILLS_BASE / args.skill)) or Path.cwd()
        print(f"✗ 技能目录不存在或不含 SKILL.md: {target}")
        print("  用法: cd 进你的技能目录后运行  python forge-publish.py --check")
        sys.exit(1)

    slug = args.slug or read_field(skill_dir, "slug") or (args.skill or "")
    version = args.version or read_version(skill_dir)
    # 云进化注册提示（非阻塞）
    notice_registration(skill_dir, slug)
    if not version and not args.check:
        print(f"✗ 无法解析版本号（frontmatter 无 version 且未用 --version 指定）")
        sys.exit(1)
    if version:
        version = to_semver(version)
    changelog = args.changelog or f"v{version}: 技能锻造炉自动化发布"

    if args.check:
        sys.exit(check_only(skill_dir, slug, require_register=args.require_register))

    # 发布版本说明用户侧校验（披露范围铁律 · references/skill-writing-guide.md 第 6 节）：
    # 复用同目录 writing_gate.py 的禁词表（单一真相源）；显式传 changelog 才阻断校验。
    if args.changelog:
        try:
            import writing_gate
        except ImportError:
            writing_gate = None
        if writing_gate is None:
            print("  ⚠ 未找到 writing_gate.py，跳过 changelog 禁词校验")
        else:
            hits, warns = writing_gate.check_changelog(changelog)
            for w in warns:
                print(f"  ⚠ {w}")
            if hits and not args.force:
                print("✗ changelog 含生产侧禁词，发布被拦（该文案会展示给终端用户，必须站用户侧）：")
                for h in hits[:6]:
                    print(f"    - {h}")
                print("  请改写为「改了什么 + 有什么价值」，简要 2–5 条；")
                print("  参考本技能 references/skill-writing-guide.md 第 6 节模板与正反对照。")
                print("  如确需发布，加 --force 明确接受。")
                sys.exit(1)

    # 方案C：cloud_config.json 由技能目录自带（仅 URL，无 token）；发布工具不注入任何凭据。

    # 解析目标平台列表
    if args.platform == "both":
        platforms = ["skillhub", "clawhub"]
    else:
        platforms = [args.platform]

    print(f"\n{'='*60}")
    print(f"技能锻造炉 · 自带发布器")
    print(f"  技能: {skill_dir.name}")
    print(f"  slug: {slug}")
    print(f"  平台: {', '.join(platforms)}")
    print(f"  模式: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"{'='*60}\n")

    # 准备引导：对就绪平台做 preflight，缺失则打印引导并跳过
    ready_platforms = []
    for name in platforms:
        info = PLATFORMS.get(name, {})
        if info.get("status") != "ready":
            print(f"  ℹ 平台 {name} 规划中，本次跳过（接口已预留）")
            print_setup_help(name)
            continue
        warns = preflight_platform(name)
        if warns:
            print(f"  ⚠ [{name}] 准备未完成，跳过本次发布：")
            for w in warns:
                print(f"      - {w}")
            print_setup_help(name)
            continue
        ready_platforms.append(name)

    if not ready_platforms:
        print("⚠️ 无就绪平台，未执行发布。请按上方引导完成首次准备后重试。")
        sys.exit(1)

    results = {}
    for name in ready_platforms:
        ok = PLATFORMS[name]["publish"](skill_dir, slug, version, changelog, args.dry_run)
        results[name] = ok

    print(f"{'='*60}")
    success = sum(results.values())
    total = len(results)
    status = "✅" if success == total else "⚠️"
    print(f"{status} {success}/{total} 平台发布完成")
    if args.dry_run:
        print("  (dry-run 模式，未真正上线)")
    print(f"{'='*60}\n")
    sys.exit(0 if success == total else 1)


if __name__ == "__main__":
    main()
