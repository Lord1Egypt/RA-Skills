#!/usr/bin/env python3
"""deploy_ghpages.py — 将生成的 AI 周报 HTML 部署到 gh-pages 分支（GitHub Pages）。

这是 ai-weekly 流水线最终的「分发」步骤：把单文件 HTML 周报推到 gh-pages 分支根目录，
飞书/钉钉卡片里的 view_url（https://<owner>.github.io/<repo>/AI_News_<date>.html）
即可被解析，解决先前 404 问题。

设计要点：
  * 用 git worktree 操作 gh-pages（不污染 main / 不进 SkillHub 包）。
  * 自动累加维护根 index.html（列出所有周报，最新高亮）。
  * 自动写入 .nojekyll（禁用 Jekyll 并强制 GitHub Pages 重新 build 分支）。
  * 默认仅本地提交/更新、不推送；--push 才推送 origin gh-pages。
  * --switch-pages 通过 GitHub API 一次性把 Pages 源切到 gh-pages(/root)。
  * MSYS 路径转换坑：所有 git 子进程注入 MSYS_NO_PATHCONV=1，路径用正斜杠。
  * 免交互推送凭据：优先 `gh auth token`（OAuth，gh 托管、不落盘），
    其次 $GITHUB_TOKEN/$GH_TOKEN 环境变量（短期令牌）；凭据经 GIT_CONFIG_*
    注入、不进 argv、不读磁盘 .github_token（P0-4/P0-5 修复）。

用法：
  python deploy_ghpages.py --html AI_News_2026-08-17.html
  python deploy_ghpages.py --html AI_News_2026-08-17.html  # 默认仅本地提交，不推送
  python deploy_ghpages.py --html AI_News_2026-08-17.html --switch-pages
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# 复用 deploy.py 的凭据脱敏（SEC-5）：失败分支会把 git 的 stderr 原样带进异常文本，
# 而 `url.<base>.insteadOf` 生效时 remote URL 内嵌 token，git 在部分认证失败场景会
# 把该 URL 回显进 stderr。脱敏实现只有一份（在 deploy.py 里），此处不重复造轮子。
# deploy.py 对本模块是**延迟导入**（函数体内的局部 import），故此处顶层导入不会
# 形成循环依赖：deploy -> deploy_ghpages 只在 deploy 的函数体内发生。
if __package__ in (None, "") and str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from deploy import _redact, _register_secrets  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_BRANCH = "gh-pages"

# 部署仓库白名单：逗号分隔的**绝对路径**。未配置时只允许仓库自身（安全默认）。
# 存在的理由：`--repo` 显式传入时若不受约束，本脚本会在该路径下 git init + commit +
# push，等于把 GitHub 凭据的推送能力开放给任意路径——一旦参数被注入内容影响，
# 凭据就会被用来向任意仓库推送内容（=「改动对外可见的基础设施」的真实形态）。
DEPLOY_REPO_ALLOWLIST_ENV = "AIWEEKLY_DEPLOY_REPO_ALLOWLIST"


def _allowlist_paths() -> list[Path]:
    """读取并解析白名单环境变量（逗号 / 分号 / 空白分隔均可）。"""
    raw = os.environ.get(DEPLOY_REPO_ALLOWLIST_ENV, "")
    out = []
    for chunk in re.split(r"[,;\s]+", raw.strip()):
        if not chunk:
            continue
        try:
            out.append(Path(chunk).expanduser().resolve())
        except OSError:
            # 单条路径解析失败不应让整份白名单失效，跳过即可（后续会因不匹配而拒绝）
            continue
    return out


def resolve_repo(explicit=None) -> Path:
    """解析部署目标仓库，并对其做白名单校验。

    安全边界（务必保留）：`--repo` 是本脚本唯一能改变「推送目标」的入口，
    因此**显式传入的路径必须同时满足**：
      1. 路径存在，且是一个 git 仓库（含 `.git`）；
      2. 路径 == 仓库自身，或路径在 `AIWEEKLY_DEPLOY_REPO_ALLOWLIST` 白名单内。

    白名单未配置时**只允许仓库自身**——即默认行为，把「显式放开」变成有意为之的动作。
    校验失败直接抛异常终止（绝不 warning 后继续），否则等于没有边界。
    """
    if not explicit:
        return REPO_ROOT

    try:
        repo = Path(explicit).expanduser().resolve()
    except OSError as exc:
        raise SystemExit(_repo_reject_message(explicit, f"路径无法解析：{exc}"))

    if not repo.is_dir():
        raise SystemExit(_repo_reject_message(explicit, "该路径不存在或不是一个目录"))
    if not (repo / ".git").exists():
        raise SystemExit(
            _repo_reject_message(explicit, "该目录不是一个 git 仓库（缺少 .git）")
        )

    if repo == REPO_ROOT:
        return repo

    allowed = _allowlist_paths()
    if repo in allowed:
        return repo

    raise SystemExit(_repo_reject_message(explicit, "未在部署白名单内"))


def _repo_reject_message(explicit: str, reason: str) -> str:
    """构造可操作的中文拒绝提示（含如何放开白名单）。"""
    env_name = DEPLOY_REPO_ALLOWLIST_ENV
    own = REPO_ROOT.as_posix()
    allow_raw = os.environ.get(env_name, "").strip()
    lines = [
        "",
        "❌ --repo 安全校验未通过：拒绝向该路径部署。",
        f"   目标路径：{explicit}",
        f"   原因：{reason}",
        "",
        "为什么这是硬边界：",
        "   本脚本会在目标路径下执行 git init / commit / push。--repo 若不受约束，",
        "   等于把 GitHub 推送凭据开放给任意路径；一旦该参数被注入内容影响，",
        "   凭据就会被用于向任意仓库推送内容（改动对外可见的基础设施）。",
        "",
        "如何处理（任选其一）：",
        f"   1) 不传 --repo，使用仓库自身（当前默认，安全）：{own}",
        f"   2) 确需部署到另一个仓库时，显式配置白名单（逗号分隔的绝对路径）：",
        f"      export {env_name}=\"/abs/path/to/repo1,/abs/path/to/repo2\"",
        "   3) 确认目标无误后，带上上面这行 export 重跑。",
    ]
    if allow_raw:
        lines += ["", f"   当前已配置的白名单：{allow_raw}"]
    else:
        lines += [
            "",
            f"   （{env_name} 未设置 → 只允许仓库自身，这是默认安全行为）",
        ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# git 封装（统一处理 MSYS 路径转换）
# ---------------------------------------------------------------------------
def _resolve_git_token() -> str | None:
    """解析用于免交互 push 的短期 GitHub 凭据（不落盘、不进 argv）。

    优先级：
      1) $GITHUB_TOKEN / $GH_TOKEN —— CI/托管环境注入的细粒度或 classic PAT（短生命周期）。
      2) `gh auth token` —— 复用已登录 gh 的 OAuth 设备流凭据（gh 托管、
         按会话刷新、40 字符，不落盘）。
      3) 不再回落读取磁盘 `.github_token`（长期 classic PAT 落盘，P0-5 已断根）。

    返回 token 明文（不含 scheme），或无法解析时返回 None。
    """
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok
    # 尝试 gh CLI（OAuth 设备流凭据，gh 托管，不落盘）
    try:
        res = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True, text=True, timeout=15,
        )
        if res.returncode == 0:
            t = res.stdout.strip()
            if t:
                return t
    except Exception:  # noqa: BLE001
        pass
    return None


def _git(args, cwd=None, check=True):
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"
    cmd = ["git"] + list(args)
    # 免交互推送：仅当命令为 push 且能解析到 token 时，通过 GIT_CONFIG_* 环境
    # 变量注入凭据（insteadOf 把 token 嵌进远端 URL，git 自动走 Basic 认证）。
    # 凭据在环境变量中传递，不进 argv（解决 `ps` 可见明文，P0-4 修复），不落盘。
    # 同时清空 credential.helper，避免 wincred 等助手干扰/覆盖。
    token = _resolve_git_token()
    if token and args and args[0] == "push":
        # 登记为字面量敏感值：`_redact` 的第一道防线靠它兜底，治「git 原样回显
        # token 且不带任何前缀」的形态（无前缀则形态正则定位不到）。
        # 登记名沿用 GITHUB_TOKEN（以 _TOKEN结尾，符合 deploy.py 的登记规则）。
        _register_secrets({"GITHUB_TOKEN": token})
        env["GIT_CONFIG_COUNT"] = "2"
        env["GIT_CONFIG_KEY_0"] = "url.https://github.com/.insteadOf"
        env["GIT_CONFIG_VALUE_0"] = f"https://x-access-token:{token}@github.com/"
        env["GIT_CONFIG_KEY_1"] = "credential.helper"
        env["GIT_CONFIG_VALUE_1"] = ""
    res = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
    )
    if check and res.returncode != 0:
        # SEC-5：stderr 原样进异常文本 = 理论泄漏通道。insteadOf 生效时 git 已解析出
        # 含 token 的 remote URL，认证失败场景下会把它回显在这里。统一过 _redact
        # （与 deploy.py 的 CLI 失败分支同一条防线），异常文本与终端输出一致脱敏。
        raise RuntimeError(
            f"git {' '.join(args)} 失败 (exit={res.returncode}):\n"
            f"{_redact(res.stderr.strip())}"
        )
    return res


# ---------------------------------------------------------------------------
# 文件名 / 标签工具
# ---------------------------------------------------------------------------
def report_label(name: str) -> str:
    """由文件名推导展示标签。"""
    stem = Path(name).stem
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", stem)
    if m:
        return f"AI News · {m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(\d{4})_W(\d+)", stem)
    if m:
        return f"AI Weekly · {m.group(1)} 第{m.group(2)}周"
    return stem


def report_sort_key(name: str) -> str:
    stem = Path(name).stem
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", stem)
    if m:
        return m.group(0)
    m = re.search(r"(\d{4})_W(\d+)", stem)
    if m:
        return f"{m.group(1)}-W{m.group(2)}"
    return stem


def build_index_html(reports: list[str], latest: str | None) -> str:
    if reports:
        items = []
        for r in reports:
            tag = "（最新）" if r == latest else ""
            items.append(
                '  <li><a href="' + r + '">' + report_label(r) +
                '</a> <span class="date">' + tag + "</span></li>"
            )
        body = "\n".join(items)
    else:
        body = '  <li><span class="date">暂无周报</span></li>'
    generated = datetime.now().replace(microsecond=0).isoformat()
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Weekly 周报存档</title>
<style>
  body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;max-width:720px;margin:48px auto;padding:0 20px;color:#222;line-height:1.6}
  h1{font-size:22px;margin-bottom:4px}
  .sub{color:#666;font-size:14px;margin-bottom:24px}
  a{color:#2b6cb0;text-decoration:none}
  a:hover{text-decoration:underline}
  li{margin:10px 0}
  .date{color:#999;font-size:13px}
</style>
</head>
<body>
<h1>AI Weekly 周报存档</h1>
<p class="sub">由 ai-weekly 技能生成的 AI 行业周报（单文件 HTML，可离线打开）。</p>
<ul>
__BODY__
</ul>
<p class="date">最近更新：__GENERATED__</p>
</body>
</html>
""".replace("__BODY__", body).replace("__GENERATED__", generated)


# ---------------------------------------------------------------------------
# worktree 准备 / 清理
# ---------------------------------------------------------------------------
def _unique_worktree_dir() -> Path:
    parent = Path(tempfile.gettempdir())
    return parent / f"aiw-ghp-{os.getpid()}-{int(time.time() * 1000)}"


def _prune_existing_worktree(repo: Path, branch: str) -> None:
    """若 gh-pages 已被其它（通常是上次异常残留的）worktree 占用，先强制移除。

    稳健做法：直接解析 `git worktree list` 文本输出，找出所有指向本仓库
    aiw-ghp-* 临时目录的工作树，强制移除 + prune。避免 --porcelain
    在 Windows 下按块分割解析失败导致残留越积越多、下次 deploy 直接报
    "already used by worktree" 而静默失败。
    """
    res = _git(["worktree", "list"], cwd=repo, check=False)
    if res.returncode != 0:
        return
    import tempfile
    tmp_root = Path(tempfile.gettempdir())
    seen: set[str] = set()
    for line in res.stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        wt = parts[0]
        if "aiw-ghp-" in wt and wt.startswith(str(tmp_root)):
            if wt in seen:
                continue
            seen.add(wt)
            try:
                _git(["worktree", "remove", "--force", wt], cwd=repo, check=False)
            except Exception:  # noqa: BLE001
                pass
    _git(["worktree", "prune"], cwd=repo, check=False)


# ---------------------------------------------------------------------------
# Pages 源切换（可选，一次性）
# ---------------------------------------------------------------------------
def _remote_api_url(repo: Path) -> str | None:
    res = _git(["remote", "get-url", "origin"], cwd=repo, check=False)
    if res.returncode != 0:
        return None
    url = res.stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?$", url)
    if not m:
        print(f"⚠️ 无法从 remote 解析 owner/repo：{url}")
        return None
    owner, name = m.group(1), m.group(2)
    return f"https://api.github.com/repos/{owner}/{name}/pages"


def switch_pages_source(repo: Path, branch: str = PAGES_BRANCH) -> bool:
    token = _resolve_git_token()
    if not token:
        print("⚠️ 未设置 GITHUB_TOKEN/GH_TOKEN，且 gh 未登录，无法自动切换 "
              "Pages 源。请到仓库 Settings → Pages → Source 选择 'Deploy from a "
              f"branch' → {branch} / /root。")
        return False
    url = _remote_api_url(repo)
    if not url:
        return False
    import urllib.request  # 延迟导入，避免无网络环境硬依赖

    payload = str(
        '{"source":{"branch":"' + branch + '","path":"/"},"build_type":"legacy"}'
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status in (200, 201, 204):
                return True
            print(f"⚠️ Pages 源切换返回 HTTP {resp.status}")
            return False
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️ Pages 源切换失败：{exc}")
        return False


# ---------------------------------------------------------------------------
# 主部署逻辑
# ---------------------------------------------------------------------------
def deploy(
    html_path,
    repo=None,
    branch: str = PAGES_BRANCH,
    no_push: bool = True,
    dry_run: bool = False,
    switch_pages: bool = False,
    commit_msg: str | None = None,
    verbose: bool = True,
    extra: list[str] | None = None,
) -> dict:
    repo = resolve_repo(repo)
    html_path = Path(html_path)
    if not html_path.exists():
        raise FileNotFoundError(f"HTML 报告不存在：{html_path}")
    html_name = html_path.name
    if not re.search(r"AI_News_.*\.html$|AI_Weekly_Report_.*\.html$", html_name):
        print(f"⚠️ 文件名 {html_name} 不像周报（期望 AI_News_*.html / "
              f"AI_Weekly_Report_*.html），仍继续。")

    if verbose:
        print(f"📦 准备部署：{html_name} → {repo} ({branch})")

    _prune_existing_worktree(repo, branch)

    site_dir = _unique_worktree_dir()
    branch_exists = (
        _git(["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
             cwd=repo, check=False).returncode == 0
    )
    if branch_exists:
        _git(["worktree", "add", str(site_dir), branch], cwd=repo)
    else:
        _git(["worktree", "add", "--orphan", str(site_dir), branch], cwd=repo)

    try:
        # 复制报告到 worktree 根
        shutil.copyfile(html_path, site_dir / html_name)
        if verbose:
            print(f"📄 已放入 {html_name}")

        # 附带文件（如 translations.json 译文源），与周报同批发布
        for f in (extra or []):
            p = Path(f)
            if p.is_file():
                shutil.copyfile(p, site_dir / p.name)
                if verbose:
                    print(f"📄 已放入附加文件 {p.name}")
            elif verbose:
                print(f"⚠️ 附加文件不存在，已跳过：{f}")

        # 收集所有报告并再生 index.html
        reports = sorted(
            [p.name for p in site_dir.glob("AI_News_*.html")]
            + [p.name for p in site_dir.glob("AI_Weekly_Report_*.html")],
            key=report_sort_key,
            reverse=True,
        )
        latest = reports[0] if reports else None
        (site_dir / "index.html").write_text(
            build_index_html(reports, latest), encoding="utf-8"
        )
        # 关键：加 .nojekyll 防止 GitHub Pages 走 Jekyll 处理，并确保重新 build
        (site_dir / ".nojekyll").write_text("", encoding="utf-8")
        if verbose:
            print(f"🗂️ 已更新 index.html（共 {len(reports)} 期，最新={latest}）+ .nojekyll")

        if dry_run:
            if verbose:
                print("🛑 dry-run：不提交/不推送。index.html 预览：")
                print((site_dir / "index.html").read_text(encoding="utf-8")[:900])
            return {"pushed": False, "dry_run": True, "reports": reports}

        # 提交
        _git(["add", "-A"], cwd=site_dir)
        status = _git(["status", "--porcelain"], cwd=site_dir, check=False).stdout.strip()
        if not status:
            if verbose:
                print("✅ 无变更，跳过提交。")
        else:
            msg = commit_msg or (
                f"docs: publish {html_name} to gh-pages ({datetime.now():%Y-%m-%d})"
            )
            _git(["commit", "-m", msg], cwd=site_dir)
            if verbose:
                print(f"✅ 已提交到本地 {branch}。")

        if no_push:
            if verbose:
                print("⏭️ 默认不推送：本地提交已就绪，需要时手动 "
                      "`git push origin gh-pages`（或加 --push）。")
            return {"pushed": False, "no_push": True, "reports": reports}

        pushed = False
        try:
            _git(["push", "origin", branch], cwd=site_dir)
            if verbose:
                print(f"🚀 已推送 {branch} → origin。")
            pushed = True
        except RuntimeError as exc:
            print(f"❌ 推送失败（本地 {branch} 已提交，待网络恢复重试）：{exc}")

        if switch_pages:
            if switch_pages_source(repo, branch):
                if verbose:
                    print(f"✅ 已将 GitHub Pages 源切到 {branch} / /root。")

        return {"pushed": pushed, "reports": reports}
    finally:
        # 清理 worktree（分支提交保留）
        try:
            _git(["worktree", "remove", "--force", str(site_dir)], cwd=repo, check=False)
        except Exception:  # noqa: BLE001
            pass


def main() -> int:
    ap = argparse.ArgumentParser(
        description="将 AI 周报 HTML 部署到 gh-pages 分支（GitHub Pages）"
    )
    ap.add_argument("--html", required=True, help="生成的周报 HTML 路径")
    ap.add_argument("--repo", default=None, help="仓库根目录（默认脚本上级目录）")
    ap.add_argument("--branch", default=PAGES_BRANCH, help="Pages 分支（默认 gh-pages）")
    ap.add_argument("--no-push", action="store_true", help="仅本地提交/更新，不推送（默认即如此，保留以兼容旧调用）")
    ap.add_argument("--push", action="store_true", help="推送（默认不推送，仅本地生成+提交）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只做 worktree+复制+index 预览，不提交不推送")
    ap.add_argument("--switch-pages", action="store_true",
                    help="部署后通过 API 把 Pages 源切到该分支（需 GITHUB_TOKEN）")
    ap.add_argument("--commit-msg", default=None, help="自定义提交信息")
    ap.add_argument("--extra", nargs="*", default=[],
                    help="随周报一并发布的附加文件（如 translations.json 译文源）")
    args = ap.parse_args()
    try:
        deploy(
            args.html,
            repo=args.repo,
            branch=args.branch,
            no_push=not args.push,
            dry_run=args.dry_run,
            switch_pages=args.switch_pages,
            commit_msg=args.commit_msg,
            extra=args.extra,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"❌ 部署失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
