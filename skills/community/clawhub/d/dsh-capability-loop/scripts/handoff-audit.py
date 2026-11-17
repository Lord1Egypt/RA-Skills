#!/usr/bin/env python3
"""交接包体检：材料可达性 / 证据对账 / 批次划分 / 设计依据。

为什么需要它：交接包交给 Trae 后，最常见的三类翻车都不是「写得不够细」，而是
  1) 引用的设计稿/规格在**另一个工作区**（实现者打开的不是那个目录 → 只能按文字猜）；
  2) 验收用例写的证据文件名与 evidence/ 实际采集的文件名对不上（验收时无图可看）；
  3) 一次交接 10+ 个任务（tasks.md 几十 KB）→ 上下文压缩后开发偏移。
以及一条纪律问题：系统已有设计体系时，必须先有 design-context（真实系统 token/组件/样本页），
否则设计会退化成「凭感觉做新设计」。

用法：
  python handoff-audit.py --workspace "D:\\repo\\app" --slug resource-demand [--out <报告.md>] [--json]
  python handoff-audit.py --workspace <工程根> --slug <slug> --batch-max-tasks 3 --task-max-files 3
退出码：0=无 FAIL 且无 WARN；1=有 FAIL；3=仅 WARN；2=参数/路径错误。
注意：默认只打印、不写文件（只读工具，不污染被体检的工程）；要留档请显式给 --out。
"""
import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DOC_FILES = ["brief.md", "tasks.md", "acceptance.md", "record.md"]
REF_EXT = (".md", ".html", ".htm", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
           ".json", ".csv", ".txt", ".har", ".log", ".pdf", ".yaml", ".yml")
EV_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".har", ".txt", ".md",
          ".csv", ".log", ".json")
IGNORE_DIRS = {"node_modules", ".git", "dist", ".tmp", "__pycache__", ".venv"}


def read(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def norm(p):
    return p.replace("\\", "/").strip()


def collect_refs(text):
    """收集引用：反引号内路径 + markdown 链接/图片目标（覆盖 ![]() 与 []()）。"""
    out = []
    for m in re.finditer(r"`([^`\n]+)`", text):
        s = norm(m.group(1))
        if not s or " " in s:
            continue
        head = s.split("#")[0]
        if head.lower().endswith(REF_EXT):
            out.append(head)
    for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", text):
        s = norm(m.group(1))
        head = s.split("#")[0]
        if head and head.lower().endswith(REF_EXT) and not head.lower().startswith("http"):
            out.append(head)
    return out


def collect_evidence_refs(text):
    """acceptance/record 里的 `evidence/<name>` 引用（含 * 通配）。"""
    found = set()
    alts = "|".join(e[1:] for e in EV_EXT)
    for m in re.finditer(r"evidence/([A-Za-z0-9._\-*]+\.(?:" + alts + "))", text):
        found.add(m.group(1))
    return found


def walk_files(root):
    for cur_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            yield os.path.join(cur_dir, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True, help="目标工程根（实现者打开的那个目录）")
    ap.add_argument("--slug", required=True, help="交接包 slug（docs/handoff/<slug>）")
    ap.add_argument("--out", default="", help="报告输出路径（可选；默认只打印不落盘）")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    ap.add_argument("--batch-max-tasks", type=int, default=3)
    ap.add_argument("--batch-max-files", type=int, default=8)
    ap.add_argument("--task-max-files", type=int, default=3)
    args = ap.parse_args()

    ws = os.path.abspath(args.workspace)
    pkg = os.path.join(ws, "docs", "handoff", args.slug)
    if not os.path.isdir(ws):
        print("[ERROR] workspace not found:", ws)
        sys.exit(2)
    if not os.path.isdir(pkg):
        print("[ERROR] handoff package not found:", pkg)
        sys.exit(2)

    fails, warns, oks = [], [], []

    def add(kind, code, msg):
        (fails if kind == "FAIL" else warns if kind == "WARN" else oks).append({"code": code, "msg": msg})

    # ---------- A. 包完整性 ----------
    for f in DOC_FILES:
        ok = os.path.isfile(os.path.join(pkg, f))
        add("OK" if ok else "FAIL", "A-" + f, ("存在 " + f) if ok else ("缺少必需文件 " + f))
    prompt = os.path.join(pkg, "PROMPT.md")
    add("OK" if os.path.isfile(prompt) else "WARN", "A-PROMPT",
        "存在 PROMPT.md（指针模式可直接贴给实现者）" if os.path.isfile(prompt)
        else "无 PROMPT.md：交接时要人工拼提示词，容易漏「禁止项」")

    ev = os.path.join(pkg, "evidence")
    ev_files = []
    if os.path.isdir(ev):
        ev_files = sorted(norm(os.path.relpath(fp, ev)) for fp in walk_files(ev))
    texts = {f: read(os.path.join(pkg, f)) for f in DOC_FILES}
    texts["PROMPT.md"] = read(prompt)
    tasks_md = texts["tasks.md"]

    # ---------- B. 材料可达性（实现者只能读工程内） ----------
    pkg_rel = norm(os.path.relpath(pkg, ws))
    materials = os.path.join(pkg, "materials")

    def abbrev_map(text):
        m = {}
        for line in text.splitlines():
            cells = [c.strip().strip("`") for c in line.split("|") if c.strip()]
            if len(cells) == 2 and cells[0] and len(cells[0]) <= 12 and "/" in cells[1]:
                m[cells[0]] = cells[1]
        return m

    abbrevs = {}
    for t in texts.values():
        abbrevs.update(abbrev_map(t))

    inside_names = {}
    for fp in walk_files(ws):
        inside_names.setdefault(os.path.basename(fp), fp)

    def resolve_ref(ref):
        cands = [ref]
        head = ref.split("/")[0]
        if head in abbrevs and abbrevs[head] != ref:
            cands.append(abbrevs[head] + ref[len(head):])
        for c in cands:
            for base in (ws, pkg, materials):
                if os.path.isfile(os.path.join(base, c.replace("/", os.sep))):
                    return True
        if os.path.basename(ref) in inside_names:
            return True
        return False

    outside, inside_missing, inside_ok, seen = [], [], 0, set()
    for f, t in texts.items():
        for ref in collect_refs(t):
            if ref.startswith("evidence/"):
                continue
            if ref.startswith(pkg_rel + "/") or ref.startswith("docs/handoff/"):
                continue
            if os.path.isfile(os.path.join(pkg, ref.replace("/", os.sep))):
                inside_ok += 1
                continue
            if (f, ref) in seen:
                continue
            seen.add((f, ref))
            if re.match(r"^[A-Za-z]:/", ref) or ref.startswith("/"):
                outside.append((f, ref))
                continue
            if resolve_ref(ref):
                inside_ok += 1
            else:
                inside_missing.append((f, ref))
    if outside:
        add("FAIL", "B-outside",
            f"{len(outside)} 处引用是工程外绝对路径（实现者打不开）："
            + "；".join(f"{f}→{r}" for f, r in outside[:6]) + ("…" if len(outside) > 6 else ""))
    if inside_missing:
        add("FAIL", "B-missing",
            f"{len(inside_missing)} 处引用在工程内找不到："
            + "；".join(f"{f}→{r}" for f, r in inside_missing[:6]) + ("…" if len(inside_missing) > 6 else ""))
    if inside_ok and not outside and not inside_missing:
        add("OK", "B", f"{inside_ok} 处引用全部在工程内且存在")
    if os.path.isdir(materials):
        add("OK", "B-materials", "存在 materials/ 副本目录（跨工作区材料已随行）")
    elif outside:
        add("WARN", "B-materials-hint", "未建 materials/：跨工作区材料应拷贝到 docs/handoff/<slug>/materials/ 再引用")

    # ---------- C. 证据对账 ----------
    refs = sorted(collect_evidence_refs(texts["acceptance.md"]) | collect_evidence_refs(texts["record.md"]))
    base_names = {os.path.basename(f) for f in ev_files}
    globby = [r for r in refs if "*" in r]
    literal = [r for r in refs if "*" not in r]
    missing = [r for r in literal if r not in ev_files and r not in base_names]

    def glob_match(pat):
        rx = re.compile("^" + re.escape(pat).replace(r"\*", ".*") + "$")
        return any(rx.match(f) for f in ev_files) or any(rx.match(os.path.basename(f)) for f in ev_files)

    missing_glob = [p for p in globby if not glob_match(p)]
    if not ev_files:
        add("FAIL", "C-empty", "evidence/ 为空：验收阶段无图/无日志可看（实现者未采集或未落位）")
    elif missing or missing_glob:
        add("FAIL", "C-missing",
            f"文档引用的证据 {len(missing) + len(missing_glob)} 个在 evidence/ 中不存在："
            + "；".join((missing + missing_glob)[:8]) + ("…" if len(missing) + len(missing_glob) > 8 else ""))
    else:
        add("OK", "C", f"{len(refs)} 个证据引用全部命中 evidence/（共 {len(ev_files)} 个文件）")

    def covered(f):
        if f in refs or os.path.basename(f) in refs:
            return True
        return any(glob_match(m) for m in globby if re.match(
            "^" + re.escape(m).replace(r"\*", ".*") + "$", f)) if globby else False

    unreferenced = [f for f in ev_files if f != "README.md" and not covered(f)]
    if unreferenced:
        add("WARN", "C-orphan",
            f"{len(unreferenced)} 个证据文件未被 acceptance/record 引用（验收时会被忽略）："
            + "；".join(unreferenced[:8]) + ("…" if len(unreferenced) > 8 else ""))

    # ---------- D. 批次划分与任务粒度 ----------
    task_ids = re.findall(r"^###\s+([A-Za-z]{0,2}-?\d+)", tasks_md, re.M)
    has_batch = bool(re.search(r"^##+\s*批次", tasks_md, re.M))
    prompt_batch = bool(re.search(r"本批次|批次\s*[0-9一二三]|batch", texts["PROMPT.md"], re.I))
    tasks_bytes = len(tasks_md.encode("utf-8"))
    per_task_files, cur = {}, None
    for line in tasks_md.splitlines():
        m = re.match(r"^###\s+([A-Za-z]{0,2}-?\d+)", line)
        if m:
            cur = m.group(1)
            per_task_files[cur] = 0
            continue
        if cur and line.startswith("- 涉及文件"):
            per_task_files[cur] += len(re.findall(r"`[^`]+`", line))

    batch_rows, covered_tasks = [], set()
    if has_batch:
        in_batch = False
        for line in tasks_md.splitlines():
            if re.match(r"^##+\s*批次", line):
                in_batch = True
                continue
            if in_batch and re.match(r"^#{2,}\s", line):
                break
            s = line.strip()
            if in_batch and s.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", s):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) < 2 or cells[0] in ("批次", "batch"):
                    continue
                ids = re.findall(r"([A-Za-z]{0,2}-?\d+)", cells[1]) if cells[1] not in ("任务",) else []
                files = 0
                for c in cells:
                    m2 = re.search(r"(\d+)\s*(?:个)?\s*文件", c)
                    if m2:
                        files = max(files, int(m2.group(1)))
                if ids:
                    batch_rows.append({"batch": cells[0], "tasks": ids, "files": files})
                    covered_tasks.update(ids)

    if not has_batch:
        add("FAIL", "D-nobatch",
            f"tasks.md 没有「批次」段，一次交给实现者 {len(task_ids)} 个任务"
            f"（约 {tasks_bytes // 1024} KB）→ 上下文会被压缩，容易开发偏移；应拆成每批 ≤{args.batch_max_tasks} 个任务")
    else:
        add("OK", "D-batch", f"tasks.md 有批次段（{len(batch_rows)} 批）")
        oversize = [b for b in batch_rows if len(b["tasks"]) > args.batch_max_tasks]
        if oversize:
            add("FAIL", "D-batch-size",
                f"{len(oversize)} 个批次任务数超上限（≤{args.batch_max_tasks}）："
                + "；".join(f"{b['batch']}={len(b['tasks'])}" for b in oversize))
        elif batch_rows:
            add("OK", "D-batch-size", f"每批任务数 ≤ {args.batch_max_tasks}")
        oversize_files = [b for b in batch_rows if b["files"] > args.batch_max_files]
        if oversize_files:
            add("WARN", "D-batch-files",
                f"{len(oversize_files)} 个批次文件数超上限（≤{args.batch_max_files}）："
                + "；".join(f"{b['batch']}={b['files']}" for b in oversize_files))
        uncovered = [t for t in task_ids if t not in covered_tasks]
        if uncovered:
            add("WARN", "D-batch-cover", f"{len(uncovered)} 个任务未归入任何批次：" + "；".join(uncovered[:8]))
    if not prompt_batch and len(task_ids) > args.batch_max_tasks:
        add("FAIL", "D-prompt-batch",
            f"PROMPT.md 未声明「本批次」范围，而任务有 {len(task_ids)} 个：实现者会按全量开工")
    fat = {t: n for t, n in per_task_files.items() if n > args.task_max_files}
    if fat:
        add("WARN", "D-fat-task",
            f"{len(fat)} 个任务的涉及文件 > {args.task_max_files}：" + "；".join(f"{t}={n}" for t, n in fat.items()))
    elif task_ids:
        add("OK", "D-granularity", f"{len(task_ids)} 个任务单任务涉及文件 ≤ {args.task_max_files}")

    # ---------- E. 设计依据（既有系统必须先读） ----------
    brief = texts["brief.md"]
    has_ctx = bool(re.search(r"design-context|设计上下文|设计依据|设计规范|真实系统|tokens?\.json", brief, re.I))
    ctx_files = []
    for root in (pkg, ws):
        for fp in walk_files(root):
            if re.match(r"^design-context.*\.md$", os.path.basename(fp), re.I):
                ctx_files.append(fp)
    tasks_design = len(re.findall(r"^- 设计依据[：:]", tasks_md, re.M))
    if not has_ctx:
        add("FAIL", "E-nodesign",
            "brief.md 无「设计依据/design-context」段：既有系统风格没有被固化成实现者可读的依据")
    elif not ctx_files:
        add("FAIL", "E-noctx-file",
            "brief 引用了设计依据，但工程/包内没有 design-context*.md：既有风格没有固化成单点依据（应先产出 design-context.md 再交接）")
    else:
        add("OK", "E-ctx", f"存在 design-context 文件 {len(ctx_files)} 个")
    if task_ids:
        if tasks_design == len(task_ids):
            add("OK", "E-per-task", f"{len(task_ids)}/{len(task_ids)} 个任务都写了「设计依据」")
        else:
            add("WARN", "E-per-task",
                f"{tasks_design}/{len(task_ids)} 个任务写了「设计依据」，其余任务实现者可自由发挥")

    # ---------- F. API 路径前缀一致性（网关前缀漏写会 404） ----------
    NON_API_SEGMENTS = {"docs", "apps", "src", "view", "views", "router", "assets", "public",
                        "tools", "scripts", "upgrade", "memory", "standards", "internal", "packages",
                        "node_modules", "dist", "build", "test", "tests", "spec", "fixtures", ".tmp"}

    def code_api_prefixes(root):
        """统计「网关前缀」：只取 API 目录（src/api，含 apps/<app>/src/api）里的字符串常量。
        规则：排除测试/mock 文件；排除 `api`（它是 baseURL 段，不是网关前缀）；出现 ≥2 次才算确定前缀，
        只出现 1 次的记入 weak（判定时降级为 WARN，避免「只出现 1 次就整项静默关闭」）。"""
        counts = {}
        targets = []
        for cur_dir, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            rel = os.path.relpath(cur_dir, root).replace("\\", "/").lower()
            if "/src/api" in rel or rel.endswith("src/api") or rel == "src/api":
                for f in files:
                    low = f.lower()
                    if not low.endswith((".ts", ".js", ".mjs", ".tsx", ".vue")):
                        continue
                    if re.search(r"\.(test|spec|mock|stub|fixture)\.[a-z]+$", low):
                        continue
                    rel_low = rel.replace("\\", "/")
                    if any(k in rel_low for k in ("/__tests__/", "/fixtures/", "/mocks/", "/stubs/")):
                        continue
                    targets.append(os.path.join(cur_dir, f))
        for fp in targets:
            txt = read(fp)
            for m in re.finditer(r"[\"'](/[A-Za-z0-9_\-/]+)[\"']", txt):
                seg = m.group(1).strip("/").split("/")[0]
                if not seg or seg[0].isdigit() or seg == "api":
                    continue
                counts[seg] = counts.get(seg, 0) + 1
        strong = {k for k, v in counts.items() if v >= 2}
        weak = {k for k, v in counts.items() if v == 1}
        return strong, weak

    def doc_api_paths(text):
        """按分句收集契约路径：否定子句（禁止/不新增/不要…）整句剔除，
        只认以 / 开头的整段反引号或 HTTP 动词后的路径，避免把 evidence/AC-007-before/after 当 API。"""
        found = set()
        NEG = re.compile(r"禁止|不新增|不要|不得|已废弃|deprecated|不复用|不写死")
        for line in text.splitlines():
            for seg in re.split(r"[，,、。；;]", line):
                if NEG.search(seg):
                    continue
                for m in re.finditer(r"`(/[^`\n]+)`", seg):
                    tok = m.group(1).strip().split("?")[0].split("#")[0]
                    if os.path.splitext(tok)[1]:
                        continue
                    if re.match(r"^/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-/]+$", tok):
                        found.add(tok)
                for m in re.finditer(r"(?:GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-/]+)", seg):
                    found.add(m.group(1))
        return found

    def route_paths(root):
        """收集页面路由（router/** 里的 path 常量），避免把 /resourceDemand/annual 这类前端路由当 API。"""
        out = set()
        for cur_dir, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            rel = os.path.relpath(cur_dir, root).replace("\\", "/").lower()
            if "/router" not in rel and not rel.endswith("router"):
                continue
            for f in files:
                if os.path.splitext(f)[1] not in (".ts", ".js", ".vue"):
                    continue
                for m in re.finditer(r"[\"'](/[A-Za-z0-9_\-/]+)[\"']", read(os.path.join(cur_dir, f))):
                    out.add(m.group(1).split("?")[0].rstrip("/"))
        return out

    page_routes = route_paths(os.path.join(ws, "apps")) or route_paths(ws)

    forbid = []
    NEG_WORDS = r"不需要写|不需要|不要|禁止|不写死|不含|不写|不得|严禁"
    HIST_WORDS = r"原写|原为|历史|已修|根因|事故|缺陷|修正|更正|变更记录|早期"
    CLAUSE_SPLIT = re.compile(r"[。；;\n]")   # 只按句号/分号切；逗号顿号都在句内，靠位置序判定
    PREFIX_PHRASE = re.compile(r"/png[^。；;\n]{0,24}?前缀|/png[^。；;\n]{0,12}?硬编码|/png[^。；;\n]{0,12}?硬写")
    PAREN = re.compile(r"（[^）]*）|\([^)]*\)")
    for fname, txt in texts.items():
        for line in txt.splitlines():
            clean = re.sub(r"[*_`]", "", line)

            def _paren(m):
                inner = m.group(0)[1:-1]
                return inner if "/png" in inner else " "

            clean = PAREN.sub(_paren, clean)
            for clause in CLAUSE_SPLIT.split(clean):
                m = PREFIX_PHRASE.search(clause)
                if not m:
                    continue
                if re.search(HIST_WORDS, clause):
                    continue
                if re.search(r"漏写", clause) and not re.search(r"不写死|不含", clause):
                    continue  # 「不得漏写 /png 前缀」= 正向要求
                if re.search(r"不是|而非|≠", clause):
                    continue  # 「/api 与 /png 不是同一前缀」= 解释性对比
                head = clause[: m.start()]
                if re.search(NEG_WORDS, head):  # 位置序：否定词在「/png…前缀」之前才算反向指令
                    forbid.append((fname, clause.strip()[:80]))
                    break
    if forbid:
        head = "文档里出现「不要/不写/不含 … `/png` 前缀」的反向指令（会让实现漏网关前缀 → 404）："
        add("FAIL", "F-forbid-prefix",
            head + "；".join(f"{f}: {l}" for f, l in forbid[:3]) + ("…" if len(forbid) > 3 else ""))

    api_prefixes, weak_prefixes = code_api_prefixes(ws)
    if not api_prefixes and not weak_prefixes:
        api_prefixes, weak_prefixes = code_api_prefixes(os.path.join(ws, "apps"))
    if api_prefixes or weak_prefixes:
        bad_paths, weak_paths, checked, page_hits = [], [], 0, 0
        for f, t in texts.items():
            for path in doc_api_paths(t):
                first = path.strip("/").split("/")[0]
                if first in NON_API_SEGMENTS:
                    continue
                if os.path.splitext(path)[1]:
                    continue
                checked += 1
                if path.rstrip("/") in page_routes:
                    page_hits += 1
                    continue  # 只豁免与页面路由完全相同的路径；子路径仍按 API 校验（父子同名时不能整支放过）
                if first in api_prefixes:
                    continue
                if first in weak_prefixes:
                    weak_paths.append((f, path))
                else:
                    bad_paths.append((f, path))
        # 反向指令：契约里明令「不要写 /xxx 前缀」
        pass
        uniq = sorted({p for _, p in bad_paths})
        if uniq:
            head = (str(len(uniq)) + " 个 API 路径的首段不在工程既有前缀集合 {"
                    + ", ".join(sorted(api_prefixes)[:6]) + "…} 内：")
            add("FAIL", "F-prefix",
                head + "；".join(uniq[:6]) + ("…" if len(uniq) > 6 else "")
                + "。多半是漏写网关前缀（例：`/annualResourceDemand/list` 应为 `/<网关前缀>/annualResourceDemand/list`）")
        elif checked:
            add("OK", "F-prefix", f"{checked - page_hits} 处 API 路径均与工程既有网关前缀一致（{', '.join(sorted(api_prefixes)[:6])}）")
        if weak_paths:
            add("WARN", "F-prefix-weak",
                f"{len({p for _, p in weak_paths})} 处路径的首段只在工程里出现过 1 次（无法确证是网关前缀，请人工确认）："
                + "；".join(sorted({p for _, p in weak_paths})[:5]))
    else:
        if weak_prefixes:
            add("WARN", "F-prefix-weak",
                "工程内 API 常量样本过少（每个前缀只出现 1 次），无法确定网关前缀；请人工核对接包里的路径前缀（"
                + ", ".join(sorted(weak_prefixes)[:6]) + "…）")
        else:
            add("OK", "F-skip", "工程内未找到既有 API 常量（无 src/api 或代码无字符串路径），本项不适用（已跳过）")

    # ---------- 汇总 ----------
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    report = {
        "workspace": ws, "package": pkg, "verdict": verdict,
        "counts": {"pass": len(oks), "warn": len(warns), "fail": len(fails)},
        "tasks": len(task_ids), "tasks_kb": max(1, tasks_bytes // 1024),
        "batches": len(batch_rows),
        "evidence_files": len(ev_files), "evidence_refs": len(refs),
        "fails": fails, "warns": warns, "oks": oks,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        lines = ["# 交接包体检报告", "",
                 f"- 工程：`{ws}`", f"- 包：`{pkg}`",
                 f"- 结论：**{verdict}**（PASS={len(oks)} / WARN={len(warns)} / FAIL={len(fails)}）",
                 f"- 任务数：{len(task_ids)}（tasks.md ≈ {tasks_bytes // 1024} KB）；批次 {len(batch_rows)} 个；"
                 f"evidence {len(ev_files)} 个，文档引用 {len(refs)} 个", ""]
        for title, items in (("FAIL（必须修）", fails), ("WARN（建议修）", warns), ("PASS", oks)):
            lines += ["## " + title, ""]
            if items:
                lines += [f"- `{it['code']}` {it['msg']}" for it in items]
            else:
                lines.append("- （无）")
            lines.append("")
        report_text = "\n".join(lines)
        print(report_text)
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(report_text)
            print("[INFO] report =", args.out)
    sys.exit(1 if fails else (3 if warns else 0))


if __name__ == "__main__":
    main()
