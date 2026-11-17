#!/usr/bin/env python3
"""Fingerprint a repo, decide which audit lenses fire, and pre-locate candidate sites.

Usage:
  scan.py [root] [--since REF] [--lens a,b] [--budget N] [--max-sites N]   markdown report on stdout
  scan.py [root] --special                                                  special-case counts only
  scan.py [root] --check                                                    signals, tools <-> lenses consistency

Every pattern lives in signals.tsv beside this file, every analyzer in tools.tsv; a project adds its
own signal rows (same six columns) in docs/agents/audit-signals.tsv. Sites and tool warnings are
leads for hunters, never findings.
shortcut: invoked as python3; on Windows run `py scan.py` until someone needs a launcher.
"""
import argparse
import collections
import concurrent.futures
import dataclasses
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LENS_DIR = os.path.join(os.path.dirname(HERE), "lenses")
LOCAL_SIGNALS = os.path.join("docs", "agents", "audit-signals.tsv")
TOOLS = os.path.join(HERE, "tools.tsv")

ALWAYS = ("types", "state", "failure", "security", "performance", "tests", "design")
SEQUENTIAL_MAX_FILES = 150   # at or below this many source files, subagents cost more than they save
SHARD_SHARE = 0.15           # a package gets its own shard of a lens when it holds this share of its sites
MAX_SHARDS_PER_LENS = 4
MAX_BYTES = 1_000_000        # larger files are generated or vendored; skip them

CODE = {"swift", "m", "mm", "kt", "kts", "java", "ts", "tsx", "js", "jsx", "mjs", "cjs", "py", "go",
        "rs", "dart", "rb", "php", "cs", "vue", "svelte", "astro", "scala", "ex", "exs"}
MANIFESTS = {"package.json", "Package.swift", "Podfile", "build.gradle", "build.gradle.kts", "pubspec.yaml",
             "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "Gemfile", "composer.json", "pom.xml"}
TEST_PATH = re.compile(r"(^|/)(tests?|__tests__|spec|specs|[A-Za-z]*Tests|UITests)/|[._-](test|spec)\.\w+$"
                       r"|Tests?\.swift$|_test\.(go|py|dart)$|(^|/)test_\w+\.py$")
SKIP_PATH = re.compile(r"(^|/)(node_modules|vendor|Pods|build|dist|\.build|DerivedData|\.dart_tool|\.next"
                       r"|target|\.venv|venv|__pycache__|\.audit|\.git)/")
PROBE_LINE = re.compile(r"^- \*\*([a-z0-9-]+)\*\*( \(when [^)]+\))?:", re.MULTILINE)
FIRES_LINE = re.compile(r"^Fires: (always|when .+)$", re.MULTILINE)


def read_text(path):
    """A whole text file, closed after reading; undecodable bytes are dropped."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


# ---------- signals and lenses ----------

@dataclasses.dataclass(frozen=True)
class Row:
    kind: str          # stack | signal | seed | special
    id: str            # seed ids are <lens>.<probe>
    lenses: tuple      # lenses a stack or signal row fires
    scope: str         # path | dep | code | ext,ext | test:<scope>
    rx: re.Pattern
    tag: str | None    # special-case counter this row feeds
    origin: str        # file:line, for error messages

    @property
    def lens(self):
        return self.id.split(".")[0]


def load_rows(root=None):
    """Rows from signals.tsv, plus the audited project's own LOCAL_SIGNALS file when present."""
    paths = [os.path.join(HERE, "signals.tsv")]
    if root and os.path.isfile(os.path.join(root, LOCAL_SIGNALS)):
        paths.append(os.path.join(root, LOCAL_SIGNALS))
    return [row for path in paths for row in _parse_signals(path)]


def _parse_signals(path):
    for n, line in enumerate(read_text(path).splitlines(), 1):
        if line.startswith(("type\t", "#")) or not line.strip():
            continue
        cols = line.split("\t")
        origin = f"{os.path.basename(path)}:{n}"
        if len(cols) != 6:
            sys.exit(f"{origin}: expected 6 tab-separated columns, got {len(cols)}")
        kind, rid, lenses, scope, pattern, tag = cols
        try:
            rx = re.compile(pattern, re.MULTILINE)
        except re.error as e:
            sys.exit(f"{origin}: bad regex for {rid}: {e}")
        yield Row(kind, rid, () if lenses == "-" else tuple(lenses.split(",")), scope, rx,
                  None if tag == "-" else tag, origin)


@dataclasses.dataclass(frozen=True)
class Lens:
    name: str
    fires: str                  # "always" or "when <condition>", from the lens file's Fires: line
    probes: tuple               # probe ids in file order
    conditional: frozenset      # probe ids marked "(when ...)"


def load_lenses():
    """{name: Lens} parsed from lenses/*.md, the single source of probes and their conditions."""
    lenses = {}
    for name in sorted(os.listdir(LENS_DIR)):
        if name.endswith(".md"):
            text = read_text(os.path.join(LENS_DIR, name))
            fires = FIRES_LINE.search(text)
            found = PROBE_LINE.findall(text)
            lenses[name[:-3]] = Lens(name[:-3], fires.group(1) if fires else "",
                                     tuple(p for p, _ in found), frozenset(p for p, when in found if when))
    return lenses


@dataclasses.dataclass(frozen=True)
class Tool:
    name: str
    lens: str          # the lens whose hunters read this tool's output
    detect: re.Pattern # a file path matching this makes the tool relevant
    runs_in: str       # "root", or "package": the folder holding the matched file
    command: str
    origin: str


def load_tools():
    tools = []
    for n, line in enumerate(read_text(TOOLS).splitlines(), 1):
        if line.startswith(("tool\t", "#")) or not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) != 5 or cols[3] not in ("root", "package"):
            sys.exit(f"tools.tsv:{n}: expected tool, lens, detect, runs_in (root|package), command")
        tools.append(Tool(cols[0], cols[1], re.compile(cols[2]), cols[3], cols[4], f"tools.tsv:{n}"))
    return tools


def tool_available(cwd, command):
    """True when the command's binary is installed; for `npx --no-install X`, when X is in node_modules/.bin."""
    words = command.split()
    if words[:2] == ["npx", "--no-install"]:
        return os.path.exists(os.path.join(cwd, "node_modules", ".bin", words[2]))
    if words[0].startswith("./"):
        return os.path.exists(os.path.join(cwd, words[0]))
    return shutil.which(words[0]) is not None


def relevant_tools(root, files, fired):
    """[(tool, folder to run in, available)] per fired lens: root tools once, package tools once per package."""
    found = []
    for tool in load_tools():
        if tool.lens not in fired:
            continue
        matches = [f for f in files if tool.detect.search(f)]
        if tool.runs_in == "root":
            folders = ["."] if matches else []
        else:
            folders = outermost({os.path.dirname(f) or "." for f in matches})
        for folder in folders:
            match = next((f for f in matches if (os.path.dirname(f) or ".") == folder), matches[0])
            command = tool.command.replace("{file}", os.path.basename(match))
            found.append((dataclasses.replace(tool, command=command), folder,
                          tool_available(os.path.join(root, folder), command)))
    return found


# ---------- the repository ----------

def git(root, *args):
    try:
        return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def list_files(root):
    out = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if out is None:
        out = "\0".join(os.path.relpath(os.path.join(d, n), root) for d, _, names in os.walk(root) for n in names)
    return [f for f in out.split("\0")
            if f and not SKIP_PATH.search(f) and os.path.isfile(os.path.join(root, f))]


def changed_since(root, ref):
    committed = git(root, "diff", "--name-only", f"{ref}...HEAD")
    if committed is None:
        sys.exit(f"cannot diff against {ref}")
    return set(committed.split()) | set((git(root, "diff", "--name-only") or "").split())


def churn(root, since="12 months ago"):
    out = git(root, "log", f"--since={since}", "--no-merges", "--name-only", "--format=") or ""
    return collections.Counter(f for f in out.splitlines() if f and not SKIP_PATH.search(f))


def outermost(dirs):
    """Sorted folders with every folder nested inside another one dropped ("." contains everything)."""
    if "." in dirs:
        return ["."]
    return [d for d in sorted(dirs) if not any(d.startswith(other + "/") for other in dirs)]


def packages(files):
    """Top-level folders that carry their own manifest; nested packages fold into their parent."""
    return outermost({os.path.dirname(f) for f in files if os.path.basename(f) in MANIFESTS and os.path.dirname(f)})


def ext(path):
    name = os.path.basename(path)
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


def in_scope(scope, path):
    if scope.startswith("test:"):
        if not TEST_PATH.search(path):
            return False
        scope = scope[len("test:"):]
    allowed = set()
    for token in scope.split(","):
        allowed |= CODE if token == "code" else {token}
    return ext(path) in allowed


_texts = {}


def read(root, path):
    if path not in _texts:
        full = os.path.join(root, path)
        try:
            too_big = os.path.getsize(full) > MAX_BYTES
            _texts[path] = "" if too_big else read_text(full)
        except OSError:
            _texts[path] = ""
    return _texts[path]


# ---------- routing ----------

def detect(root, rows, files):
    """{row id: evidence path} for every stack and signal row that matches the repo."""
    manifests = [f for f in files if os.path.basename(f) in MANIFESTS or os.path.basename(f).startswith("requirements")]
    hits = {}
    for row in rows:
        if row.kind not in ("stack", "signal"):
            continue
        if row.scope == "path":
            evidence = next((f for f in files if row.rx.search(f)), None)
        else:
            pool = manifests if row.scope == "dep" else [f for f in files if in_scope(row.scope, f)]
            evidence = next((f for f in pool if row.rx.search(read(root, f))), None)
        if evidence:
            hits[row.id] = evidence
    return hits


def route(rows, hits, requested):
    """(fired lenses, {lens: reasons}) from ALWAYS plus matching signals, or exactly the requested lenses."""
    reasons = collections.defaultdict(list)
    for lens in ALWAYS:
        reasons[lens].append("always")
    for row in rows:
        if row.id in hits:
            for lens in row.lenses:
                reasons[lens].append(f"{row.id} ({hits[row.id]})")
    known = list(load_lenses())
    if requested:
        unknown = [l for l in requested if l not in known]
        if unknown:
            sys.exit(f"unknown lens: {', '.join(unknown)} (have: {', '.join(known)})")
        return list(requested), reasons
    return [l for l in known if l in reasons], reasons


def _seed_file(job):
    root, path, rows, lenses, max_sites = job
    text = read(root, path)
    sites, hits, counts = [], collections.Counter(), collections.Counter()
    for row in rows if text else ():
        if not in_scope(row.scope, path):
            continue
        wanted = row.kind == "seed" and row.lens in lenses
        for m in row.rx.finditer(text):
            if row.tag:
                counts[row.tag] += 1
            if wanted:
                hits[row.id] += 1
                if hits[row.id] <= max_sites:
                    line = text.count("\n", 0, m.start()) + 1
                    snippet = text[m.start():m.start() + 80].splitlines()[0].strip()
                    sites.append((row.id, f"{path}:{line}: {snippet}"))
    return sites, hits, counts


def seed(root, rows, files, lenses, max_sites):
    """Candidate sites per probe in file priority order, hit counts per probe and per file, special counts."""
    active = [r for r in rows if r.tag or (r.kind == "seed" and r.lens in lenses)]
    jobs = [(root, f, active, lenses, max_sites) for f in files if any(in_scope(r.scope, f) for r in active)]
    try:
        with concurrent.futures.ProcessPoolExecutor() as pool:
            results = list(pool.map(_seed_file, jobs, chunksize=64))
    except OSError:  # sandboxes that forbid spawning processes
        results = list(map(_seed_file, jobs))
    sites, hits, counts, per_file = collections.defaultdict(list), collections.Counter(), collections.Counter(), {}
    for job, (file_sites, file_hits, file_counts) in zip(jobs, results):
        per_file[job[1]] = file_hits
        hits.update(file_hits)
        counts.update(file_counts)
        for probe, site in file_sites:
            if len(sites[probe]) < max_sites:
                sites[probe].append(site)
    return sites, hits, counts, per_file


def lens_load(fired, probe_hits):
    return {l: sum(n for p, n in probe_hits.items() if p.startswith(l + ".")) for l in fired}


def plan(fired, load, per_file, pkgs, n_source, budget):
    """Execution plan text. Spare budget beyond one subagent per lens shards the heaviest lenses by package."""
    if n_source <= SEQUENTIAL_MAX_FILES:
        return "sequential: small scope, run every lens in the main context"
    shards, spare = {}, budget - len(fired)
    if len(pkgs) > 1:
        def package_of(f):
            return next((p for p in pkgs if f.startswith(p + "/")), "(root)")
        for lens in sorted(fired, key=lambda l: -load.get(l, 0)):
            by_pkg = collections.Counter()
            for f, file_hits in per_file.items():
                by_pkg[package_of(f)] += sum(n for probe, n in file_hits.items() if probe.startswith(lens + "."))
            total = sum(by_pkg.values())
            big = [p for p, n in by_pkg.most_common() if total and n / total >= SHARD_SHARE][:MAX_SHARDS_PER_LENS]
            parts = big + (["rest"] if total and sum(by_pkg[p] for p in big) < total else [])
            if 1 < len(parts) <= spare + 1:
                shards[lens], spare = parts, spare - (len(parts) - 1)
    count = len(fired) + sum(len(v) - 1 for v in shards.values())
    if count > budget:
        return f"parallel in waves: {count} lenses, at most {budget} subagents at once, heaviest lenses first"
    text = f"parallel: {count} subagents (budget {budget}), one per lens"
    if shards:
        text += "; shard " + "; ".join(f"{lens} into {', '.join(parts)}" for lens, parts in shards.items())
    return text


# ---------- commands ----------

def render(ctx):
    """The SCAN.md report. ctx carries every computed piece, so this function only formats."""
    source = [f for f in ctx["scoped"] if ext(f) in CODE]
    langs = collections.Counter(ext(f) for f in source).most_common(6)
    stacks = [f"{r.id} ({ctx['hits'][r.id]})" for r in ctx["rows"] if r.kind == "stack" and r.id in ctx["hits"]]
    since = f" (seeding only files changed since `{ctx['since']}`)" if ctx["since"] else ""
    out = ["# Scan", "",
           f"- root: `{ctx['root']}`{since}",
           f"- files: {len(ctx['files'])} tracked, {len(source)} source files in scope",
           f"- languages: {', '.join(f'{e} {n}' for e, n in langs) or 'none'}",
           f"- stacks: {', '.join(stacks) or 'none detected'}",
           f"- packages: {', '.join(ctx['pkgs']) or 'single package'}",
           f"- plan: {ctx['plan']}",
           "", "## Lenses", ""]
    for name, lens in load_lenses().items():
        if name in ctx["fired"]:
            why = "; ".join(ctx["reasons"][name]) or "requested"
            out.append(f"- **{name}** fires: {why} — {ctx['load'][name]} candidate sites")
        else:
            out.append(f"- {name} skipped: fires {lens.fires}, and no signal matched")
    out += ["", "## Tools", "", "Run each available one and save its output to `<out>/tools/<name>.txt`; its warnings are leads for the lens named.", ""]
    for tool, folder, available in ctx["tools"]:
        state = "available" if available else "not installed: note it, never install"
        run = tool.command if folder == "." else f"cd {folder} && {tool.command}"
        out.append(f"- **{tool.name}** → {tool.lens}: `{run}` ({state})")
    if not ctx["tools"]:
        out.append("- none relevant")
    out += ["", "## Hot spots (12 months)", ""]
    out += [f"- {n:4} {f}" for f, n in ctx["heat"].most_common(15)]
    out += ["", "## Candidate sites", "", "Leads only. Every probe is answered whether or not it has sites here.", ""]
    for lens in ctx["fired"]:
        probes = sorted(p for p in ctx["probe_hits"] if p.startswith(lens + "."))
        if probes:
            out += [f"### {lens}", ""]
            for probe in probes:
                out.append(f"- `{probe}` ({ctx['probe_hits'][probe]} hits)")
                out += [f"  - {s}" for s in ctx["sites"][probe]]
            out.append("")
    out += ["## Special cases", ""]
    out += [f"- {t}: {ctx['counts'][t]}" for t in sorted({r.tag for r in ctx["rows"] if r.tag})]
    return "\n".join(out)


def cmd_scan(a):
    root = os.path.abspath(a.root)
    rows = load_rows(root)
    files = list_files(root)
    heat = churn(root)
    scoped = files if not a.since else [f for f in files if f in changed_since(root, a.since)]
    scoped = sorted(scoped, key=lambda f: (bool(TEST_PATH.search(f)), -heat[f], f))  # hot source files first
    hits = detect(root, rows, files)
    fired, reasons = route(rows, hits, [l.strip() for l in a.lens.split(",")] if a.lens else None)
    sites, probe_hits, counts, per_file = seed(root, rows, scoped, set(fired), a.max_sites)
    load = lens_load(fired, probe_hits)
    pkgs = packages(files)
    print(render(dict(
        root=root, since=a.since, rows=rows, files=files, scoped=scoped, hits=hits, fired=fired,
        reasons=reasons, sites=sites, tools=relevant_tools(root, files, set(fired)), probe_hits=probe_hits, counts=counts, heat=heat, pkgs=pkgs, load=load,
        plan=plan(fired, load, per_file, pkgs, sum(ext(f) in CODE for f in scoped), a.budget))))
    return 0


def cmd_special(a):
    root = os.path.abspath(a.root)
    rows = load_rows(root)
    _, _, counts, _ = seed(root, rows, list_files(root), set(), 0)
    for tag in sorted({r.tag for r in rows if r.tag}):
        print(f"{tag:20} {counts[tag]}")
    return 0


def cmd_check(a):
    rows = load_rows(os.path.abspath(a.root))
    lenses = load_lenses()
    fired_by_signal = {l for r in rows for l in r.lenses}
    problems = []
    for name, lens in lenses.items():
        if not lens.probes:
            problems.append(f"lenses/{name}.md: no probes (expected lines like '- **probe-id**: question')")
        if not lens.fires:
            problems.append(f"lenses/{name}.md: no 'Fires: always' or 'Fires: when <condition>' line")
        elif (lens.fires == "always") != (name in ALWAYS):
            problems.append(f"lenses/{name}.md: says 'Fires: {lens.fires}' but scan.py ALWAYS "
                            f"{'includes' if name in ALWAYS else 'omits'} it")
        if name not in ALWAYS and name not in fired_by_signal:
            problems.append(f"lenses/{name}.md: nothing fires this lens")
    for row in rows:
        problems += [f"{row.origin}: lens '{l}' has no lenses/{l}.md" for l in row.lenses if l not in lenses]
        if row.kind == "seed" and row.id.partition(".")[2] not in getattr(lenses.get(row.lens), "probes", ()):
            problems.append(f"{row.origin}: seed {row.id} names no probe in lenses/{row.lens}.md")
    problems += [f"ALWAYS lens '{l}' has no lenses/{l}.md" for l in ALWAYS if l not in lenses]
    problems += [f"{t.origin}: tool {t.name} feeds unknown lens '{t.lens}'" for t in load_tools() if t.lens not in lenses]
    n_probes = sum(len(l.probes) for l in lenses.values())
    print("\n".join(problems) or f"ok: {len(rows)} rows, {len(lenses)} lenses, {n_probes} probes")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--since", help="seed only files changed since this git ref (diff or PR mode)")
    ap.add_argument("--lens", help="comma list of lenses to run, overriding detection")
    ap.add_argument("--budget", type=int, default=12, help="most subagents the plan may use (default 12)")
    ap.add_argument("--max-sites", type=int, default=12, help="candidate sites listed per probe (default 12)")
    ap.add_argument("--special", action="store_true", help="print special-case counts only")
    ap.add_argument("--check", action="store_true", help="check signals against lenses/*.md")
    a = ap.parse_args()
    return cmd_check(a) if a.check else cmd_special(a) if a.special else cmd_scan(a)


if __name__ == "__main__":
    sys.exit(main())
