#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dsh-api-probe.py —— 「当前 DSH 源码」核验 skill 依赖的易变 API 断言（纯 Python 版）。

为什么存在这个脚本：
    bash 版（dsh-api-probe.sh）依赖 coreutils（cat / grep / find / head）。
    在缺少 coreutils 的环境（例如某些 Windows 自带 bash）里，它会失效。
    * bash 版的 `$(cat <<EOF)` 一旦展开为空，会「断言表为空却回答全部成立」；
      该缺陷已修（内联字符串 + 空表哨兵 exit 3），但仍依赖 grep/find。
    * 「grep 缺失」会表现为大量假 STALE，同样不可信。
    本脚本用 Python 标准库完成全部匹配，**零外部命令依赖**，在 Windows 上最稳。
    两者断言表内容必须保持一致（见 references/api-claims.md）。

用法：
    python dsh-api-probe.py [DSH 仓库路径] [--quiet]

    不传路径时，依次尝试 ./deepseek-harness、../deepseek-harness、环境变量 DSH_REPO。

退出码：
    0 = 全部 HOLDS（或只有 SKIP）
    1 = 存在 STALE（有断言不成立 → 相关模板可能已过时，不要直接照抄）
    2 = 找不到仓库路径 / 不是 DSH 仓库
    3 = 断言表为空 → 未核验任何事实，结果无效

设计约束（与 bash 版一致）：
    * 断言只用「符号/字符串存在性」，绝不依赖行号 —— 行号必然漂移。
    * 只断言「一旦消失就会让本 skill 的指引失效」的事实；枚举类事实故意不断言。
    * 正向（S/M/L 级，模式 g/f/d）：命中 = HOLDS。
      反向（N 级，模式 nf/nd/nt/nl/na）：未命中 = HOLDS；命中 = 该否定论断被推翻（STALE）。
      `na:` 是 2026-09-16 新增的**内容**否定模式（前四个只能否定文件/目录/tag/提交信息），
      用于「旧名已被改名取代、且不提供兼容别名」这类结论。
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# 🔴 2026-10-10（1.4.0 轮实测）：本脚本会往 stdout 打印 ✅ / ⚠️ / ❌ 等符号，而 stdout 一旦是
#    **管道**（W8 真机核验、CI、`| grep` 都属于这种），Windows 上的 Python 会按 ANSI 代码页
#    （本机 cp936/GBK）编码，遇到 ✅（U+2705）直接抛 UnicodeEncodeError。外部表现是
#    「退出码 1 且没有 SUMMARY 行」—— 极易被误读成「有 STALE」（1 与「有 STALE」同码）。
#    这里强制 UTF-8，并把不可编码字符降级为替换字符，使重定向场景下的读数可信。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")   # Python 3.7+
    except Exception:                                            # pragma: no cover
        pass

BASELINE_COMMIT = "f3803c9697"
BASELINE_VER = "0.2.2-alpha.2"

# ── 断言表 ──────────────────────────────────────────────────────────────────
# 格式：ID,等级,说明,模式,作用域
#   等级：S 结构性公理 / M 接口名 / L 仓库布局 / N 否定性论断
#   模式：g:<正则> 文本检索 | f:<相对路径> 文件存在 | d:<相对路径> 目录存在
#         nf:<文件名> 文件不应存在 | nd:<目录名> 目录不应存在
#         nt:<正则> tag 不应匹配 | nl:<正则> 提交信息不应匹配
# 注意：说明字段里不要出现英文逗号以外的分隔歧义；字段数固定为 5。
CHECKS = r"""
S01,S,插件导出形态硬规则（函数式插件不得有 default export）,g:service packages default-export their service class,packages/AGENTS.md
S02,S,复盘 0001（default export 丢弃命名空间）仍在档,f:docs/postmortem/0001-acp-default-export-drops-inject.md,-
S03,S,服务类继承形态仍存在,g:extends Service,packages
S04,S,补丁行序无语义（激活由服务可用性驱动）,g:Row order carries no load semantics,packages
S05,S,纯配置组合包范式（src/index.ts 只导出空对象）,g:export \{\},packages/bundle/base/src/index.ts
S06,S,base 补丁含 !!js 内联表达式,g:!!js,packages/bundle/base
M01,M,defineTool 从 dsh-tools 导出,g:export (function|const) defineTool,packages
M02,M,DSH 参数 DSL：属性级 required,g:ParameterPropertySpec = ValueSchemaSpec & \{ required\?: true \},packages
M03,M,属性级 required 的校验报错文案,g:required must be true when present,packages
M04,M,对象级 required 必须是数组（裸 register 路径）,g:required must be an array of strings,packages
M05,M,DefineToolOptions 接口,g:interface DefineToolOptions,packages
M06,M,工具注册 API,g:tools\.register\(,packages
M07,M,命令注册 API,g:commands\.register\(,packages
M08,M,UI 插槽 API,g:slots\.(inject|register)\(,packages
M09,M,服务插件构造函数首参约定,g:super\(ctx[^)]*',packages
M10,M,dsh.bundle 声明缺失时的警告,g:declares no dsh\.bundle,packages
M11,M,loader 非事务化（补丁行应用失败只记日志、不回滚）,g:Wait until this tree has no pending import,vendor/loader
M12,M,子进程凭据清洗正则常量,g:SENSITIVE_ENV_PATTERN,packages
M13,M,补丁内相对路径锚定函数,g:anchorInsertedPluginNames,packages
M14,M,保留工具名 run_code,g:run_code,packages
M15,M,配置树导出开关,g:\-\-dump-config,packages
M16,M,插件安装 CLI,g:dsh plugin,apps
M17,M,事件 agent/pre-step,g:agent/pre-step,packages
M18,M,事件 agent/request,g:agent/request,packages
M19,M,事件 agent/turn-stopping,g:agent/turn-stopping,packages
M20,M,事件 llm/stream,g:llm/stream,packages
M21,M,事件 system-prompt/assemble,g:system-prompt/assemble,packages
M22,M,事件 approval/request,g:approval/request,packages
M23,M,插槽 settings.section,g:settings\.section,packages
M24,M,插槽 conversation.view,g:conversation\.view,packages
M25,M,插槽 tool.call.toolview,g:tool\.call\.toolview,packages
M26,M,DSH_HOME 路径辅助函数,g:dshHomePath,packages
M27,M,可选服务的拓扑无关取法,g:ctx\.get\(,packages
M28,M,副作用回收 API,g:ctx\.effect\(,packages
M29,M,waterfall 放行约定,g:await next\(\),packages
M30,M,timeoutMs 正值校验文案,g:timeoutMs must be a positive finite number,packages
M31,M,dsh.bundle 清单字段,g:dsh\.bundle,packages
M32,M,DSH_HOME 环境变量,g:DSH_HOME,packages
M33,M,服务 ctx.ptcRuntime（原 codeRuntime 改名，不提供别名）,g:ptcRuntime,packages/ptc-runtime
M34,M,服务 ctx.mcpResources,g:mcpResources,packages/mcp/mcp-resources
M35,M,PreToolDecision 新增 cancel 决策,g:kind: 'cancel',packages/core/tools
M36,M,base 补丁新增 image-offload 插件行,g:image-offload,packages/bundle/base/cordis.patch.yml
M37,M,base 补丁的 workflow 行改用 ptc 家族,g:workflow-ptc,packages/bundle/base/cordis.patch.yml
L01,L,官方插件工程约定入口,f:packages/AGENTS.md,-
L02,L,loader 配置校验实现,f:vendor/loader/src/config/group.ts,-
L03,L,CLI 插件安装实现,f:apps/cli/src/plugin.ts,-
L04,L,官方纯配置组合包补丁,f:packages/bundle/base/cordis.patch.yml,-
L05,L,顶层目录布局（packages/vendor/apps/docs）,d:vendor,-
N01,N,仓库没有 CHANGELOG 文件（变更史只在 git 与 .agents/notes）,nf:CHANGELOG*,-
N02,N,提交不使用 BREAKING CHANGE 页脚（只用 type(scope)!: 标题标记）,nl:BREAKING CHANGE,-
N03,N,不存在 packages/ui/（TUI 前端已归档）,nd:ui,packages
N04,N,版本号不连续：不存在 0.1.4,nt:0\.1\.4,-
N05,N,不采用 changesets 发布流程（无 .changeset/）,nf:.changeset,-
N06,N,旧服务名 codeRuntime 已无兼容别名,na:ctx\.codeRuntime,packages
N07,N,事件 agent/session-start 已被 serial 的 agent/created 取代,na:agent/session-start,packages
N08,N,E2B 执行后端已整体移除,na:deepseek-ai/dsh-e2b,packages
"""

# 扫描文本时应跳过的目录（体积大且无关）
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}
# 只在这些后缀的文件里做文本检索，避免扫二进制
TEXT_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".yaml", ".yml",
    ".md", ".txt", ".toml", ".py", ".sh", ".sql", ".css", ".html",
}


def log(msg=""):
    print(msg, flush=True)


def iter_files(root: Path, suffixes=None):
    """遍历 root 下的文本文件。

    root 既可以是目录，也可以直接是单个文件 —— 断言表的 scope 字段两种都在用
    （如 S05 的 scope 是 `packages/bundle/base/src/index.ts`，S03 是 `packages`）。
    早期版本只按目录处理，导致以文件为 scope 的断言永远 MISS（假 STALE）。
    """
    if root.is_file():
        if suffixes is None or root.suffix.lower() in suffixes:
            yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if suffixes is not None and p.suffix.lower() not in suffixes:
                continue
            yield p


def grep_first(root: Path, pattern: str):
    """在 root 下递归搜索正则，返回首个命中的 (文件, 行号, 行内容)。"""
    try:
        rx = re.compile(pattern)
    except re.error as exc:
        return None, f"正则编译失败: {exc}"
    for p in iter_files(root, TEXT_SUFFIXES):
        try:
            with p.open("r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if rx.search(line):
                        return (p, i, line.strip()[:160]), None
        except OSError:
            continue
    return None, None


def git(repo: Path, *args):
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="ignore",
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout if out.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("repo", nargs="?", default="")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    repo = args.repo
    if not repo:
        for cand in ("./deepseek-harness", "../deepseek-harness",
                     os.environ.get("DSH_REPO", "")):
            if cand and (Path(cand) / "packages" / "AGENTS.md").is_file():
                repo = cand
                break

    if not repo or not Path(repo).is_dir():
        log("ERROR: 找不到 DSH 仓库。请把仓库路径作为第一个参数传入。")
        log("       （判定标准：目录下存在 packages/AGENTS.md）")
        return 2

    repo_path = Path(repo).resolve()
    if not (repo_path / "packages").is_dir() or not (
        (repo_path / "vendor" / "loader").is_dir() or (repo_path / "apps" / "cli").is_dir()
    ):
        log(f"ERROR: {repo_path} 看起来不是 DSH 仓库。")
        log("       期望看到 packages/ 目录，以及 vendor/loader/ 或 apps/cli/ 之一。")
        log("       （防止对着错误目录跑出假的 STALE 结论）")
        return 2

    # 基线信息
    live_ver = "unknown"
    try:
        import json
        pkg = json.loads((repo_path / "package.json").read_text(encoding="utf-8"))
        live_ver = pkg.get("version") or "unknown"
    except Exception:
        pass

    live_commit = (git(repo_path, "rev-parse", "--short=10", "HEAD") or "unknown").strip()
    live_date = (git(repo_path, "log", "-1", "--format=%cs") or "unknown").strip()
    is_git = git(repo_path, "rev-parse", "--git-dir") is not None

    if not args.quiet:
        log("=" * 64)
        log(" DSH API 探针（Python 版，零 coreutils 依赖）")
        log("=" * 64)
        log(f" 仓库路径   : {repo_path}")
        log(f" 当前版本   : {live_ver}   (HEAD {live_commit}, {live_date})")
        log(f" skill 基线 : {BASELINE_VER}   ({BASELINE_COMMIT})")
        if live_commit == "unknown":
            log(" ⚠️  无法读取 git HEAD（不是 git 仓库或没有 git）——版本比对已跳过。")
        elif live_commit.startswith(BASELINE_COMMIT):
            log(" ✅  与基线同一 commit —— references 可直接使用。")
        else:
            log(" ⚠️  commit 与基线不同 —— references 仍需核验，不要无条件照抄。")
        log("")

    raw = [l for l in CHECKS.strip().splitlines() if l.strip()]
    if not raw:
        log("🔴 断言表为空 —— 探针未核验任何事实，结果无效。")
        return 3

    holds = stale = skipped = 0
    neg = 0
    parse_err = 0
    stale_rows, skip_rows = [], []

    for line in raw:
        parts = line.split(",")
        if len(parts) != 5:
            parse_err += 1
            stale_rows.append(
                f"  PARSE  断言表解析失败（字段数 {len(parts)} != 5，模式里可能混入了逗号）\n"
                f"        原文: {line}")
            continue
        cid, tier, desc, mode, scope = parts
        scope = "" if scope == "-" else scope
        target = repo_path / scope if scope else repo_path
        kind, _, payload = mode.partition(":")
        if tier == "N":
            neg += 1

        if kind == "g":
            if not target.exists():
                skipped += 1
                skip_rows.append(f"  {cid}  [{tier}] 作用域缺失: {scope}")
            else:
                hit, err = grep_first(target, payload)
                if err:
                    parse_err += 1
                    stale_rows.append(f"  {cid}  正则错误: {err}")
                elif hit:
                    holds += 1
                    if not args.quiet:
                        log(f"  HOLDS  {cid:<4} [{tier}] {desc}")
                else:
                    stale += 1
                    stale_rows.append(
                        f"  {cid}  [{tier}] {desc}\n"
                        f"        期望模式: {payload}\n"
                        f"        作用域  : {scope}")
                    if not args.quiet:
                        log(f"  STALE  {cid:<4} [{tier}] {desc}")

        elif kind == "f":
            if (target / payload).exists():
                holds += 1
                if not args.quiet:
                    log(f"  HOLDS  {cid:<4} [{tier}] {desc}")
            else:
                stale += 1
                stale_rows.append(
                    f"  {cid}  [{tier}] {desc}\n        缺失文件: {scope}/{payload}")
                if not args.quiet:
                    log(f"  STALE  {cid:<4} [{tier}] {desc}")

        elif kind == "d":
            if (target / payload).is_dir():
                holds += 1
                if not args.quiet:
                    log(f"  HOLDS  {cid:<4} [{tier}] {desc}")
            else:
                stale += 1
                stale_rows.append(
                    f"  {cid}  [{tier}] {desc}\n        缺失目录: {payload}")
                if not args.quiet:
                    log(f"  STALE  {cid:<4} [{tier}] {desc}")

        elif kind == "nf":
            # 断言「不存在该文件」；命中即否定被推翻
            found = None
            if target.exists():
                rx = re.compile("^" + re.escape(payload).replace(r"\*", ".*") + "$", re.I)
                for p in iter_files(target):
                    if rx.match(p.name):
                        found = p
                        break
            if found is None:
                holds += 1
                if not args.quiet:
                    log(f"  HOLDS  {cid:<4} [{tier}] {desc}")
            else:
                stale += 1
                stale_rows.append(
                    f"  {cid}  [{tier}] 否定论断已被推翻：{desc}\n"
                    f"        断言不存在，却找到: {found}")
                if not args.quiet:
                    log(f"  STALE  {cid:<4} [{tier}] {desc}（否定论断失效）")

        elif kind == "nd":
            if not (target / payload).is_dir():
                holds += 1
                if not args.quiet:
                    log(f"  HOLDS  {cid:<4} [{tier}] {desc}")
            else:
                stale += 1
                stale_rows.append(
                    f"  {cid}  [{tier}] 否定论断已被推翻：{desc}\n"
                    f"        断言不存在的目录已出现: {scope}/{payload}")
                if not args.quiet:
                    log(f"  STALE  {cid:<4} [{tier}] {desc}（否定论断失效）")

        elif kind == "nt":
            if not is_git:
                skipped += 1
                skip_rows.append(f"  {cid}  [{tier}] 非 git 仓库，无法核验 tag")
            else:
                tags = (git(repo_path, "tag") or "").splitlines()
                m = [t for t in tags if re.search(payload, t)]
                if m:
                    stale += 1
                    stale_rows.append(
                        f"  {cid}  [{tier}] 否定论断已被推翻：{desc}\n"
                        f"        匹配到的 tag: {' '.join(m[:3])}")
                    if not args.quiet:
                        log(f"  STALE  {cid:<4} [{tier}] {desc}（否定论断失效）")
                else:
                    holds += 1
                    if not args.quiet:
                        log(f"  HOLDS  {cid:<4} [{tier}] {desc}")

        elif kind == "nl":
            if not is_git:
                skipped += 1
                skip_rows.append(f"  {cid}  [{tier}] 非 git 仓库，无法核验提交历史")
            else:
                log_all = git(repo_path, "log", "--all", "--format=%s%n%b") or ""
                if re.search(payload, log_all):
                    stale += 1
                    stale_rows.append(
                        f"  {cid}  [{tier}] 否定论断已被推翻：{desc}\n"
                        f"        提交信息中匹配到: {payload}\n"
                        f"        复核: git -C <repo> log --all --grep='{payload}'")
                    if not args.quiet:
                        log(f"  STALE  {cid:<4} [{tier}] {desc}（否定论断失效）")
                else:
                    holds += 1
                    if not args.quiet:
                        log(f"  HOLDS  {cid:<4} [{tier}] {desc}")

        elif kind == "na":
            # 断言「该字符串不应再出现」（改名 / 移除类否定论断）；命中即否定被推翻。
            # 为什么需要这个模式：`nf:`/`nd:` 只能否定「文件 / 目录的存在」，而
            # 「旧服务名已无兼容别名」「旧事件名已被取代」这类结论的过时方向是
            # **内容里又冒出了旧字符串**，既有的五个模式在语义上抓不到。
            if not target.exists():
                skipped += 1
                skip_rows.append(f"  {cid}  [{tier}] 作用域缺失: {scope}")
            else:
                hit, err = grep_first(target, payload)
                if err:
                    parse_err += 1
                    stale_rows.append(f"  {cid}  正则错误: {err}")
                elif hit:
                    p, i, line = hit
                    stale += 1
                    stale_rows.append(
                        f"  {cid}  [{tier}] 否定论断已被推翻：{desc}\n"
                        f"        断言不应再出现，却在 {p}:{i} 命中：{line}")
                    if not args.quiet:
                        log(f"  STALE  {cid:<4} [{tier}] {desc}（否定论断失效）")
                else:
                    holds += 1
                    if not args.quiet:
                        log(f"  HOLDS  {cid:<4} [{tier}] {desc}")

        else:
            parse_err += 1
            stale_rows.append(f"  {cid}  未知的检查类型: {kind}")

    total = len(raw)
    log("")
    log("-" * 64)
    log(f"SUMMARY total={total} positive={total - neg} negative={neg} "
        f"holds={holds} stale={stale} skipped={skipped} parse_errors={parse_err}")

    if parse_err > 0:
        log("")
        log("🔴 断言表自身有解析错误 —— 探针结果不可信，先修断言表再判断是否过时。")
        log("\n".join(stale_rows))
        return 1

    if stale > 0:
        log("")
        log("🔴 有断言不成立 —— 相关模板/速查表可能已过时，**不要直接照抄**：")
        log("\n".join(stale_rows))
        log("")
        log("处理办法（见 references/00-version-gate.md）：")
        log("  1) 以源码为准，从当前源码重新推导该 API 的正确用法；")
        log("  2) 把结论写进 ~/.workbuddy/memory/ 并在交付物里注明「已对 <commit> 核验」；")
        log("  3) 更新 references/api-claims.md 与本脚本的断言表，然后重跑本探针。")
        log("")
        log("  ⚠️ 若 STALE 来自 N 级反向断言 —— 那不是「上游 API 过时」，而是")
        log("     **本 skill 的一条否定结论已被推翻**。必须修正 api-claims.md 该条，")
        log("     并 grep 全库找出所有引用该结论的文档一并改正 —— 不能只改一处。")
        return 1

    if skipped > 0:
        log(f"⚠️  有作用域缺失（可能是仓库不完整或布局变了）：")
        log("\n".join(skip_rows))
    log("✅ 全部断言成立 —— references 中 M 级事实对当前源码有效。")
    log("   注意：本结果只覆盖「探针断言过的事实」，不覆盖 V 级细节（默认值/枚举/文案）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
