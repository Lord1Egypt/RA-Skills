#!/usr/bin/env python3
"""memory_index.py — change-index generator + environment discovery (ChangSheng 0.3).

Pure stdlib, zero dependencies. Two jobs:

1. DISCOVER (--discover / --list): locate the user's memory carriers for the
   semantic roles (rules / todos / journal) by scanning common file
   conventions. Discovery writes .changsheng/discovery.json so recovery can
   resolve roles -> real files. It only lists paths — it never reads content.

2. INDEX (default): hash the L2 tracked files listed in config.yaml and write
   memory_index.md (✅ new change / ⏸ unchanged) — where token savings live.

Mode (--mode):
  internal — for the maintainers' own fixed-layout vault (roles come straight
             from config; no discovery). Zero surprises.
  auto     — default for external users: roles auto-discovered, extras from
             config. Fresh install works with no config at all.
  manual   — roles come only from explicit config (0.2.x behaviour preserved).

Config shapes:
  New:  mode: auto|manual|internal
        roles: {rules: [...], todos: [...], journal: [...]}   # files or dirs
        must_read_extra: [...]    # extra L3 always-read files
        tracked_files_extra: [...] # extra L2 change-tracked files
        lang: en|zh               # display language for the generated index
                                  # (default en; zh = Chinese flags/labels)
  Old (0.2.x): must_read: [...] tracked_files: [...] -> migrated: must_read ->
        must_read_extra (keeps L3 meaning), tracked_files -> tracked_files_extra
        (keeps L2 meaning). Roles are NEVER guessed from old flat lists.

Usage:
  python memory_index.py --discover [root]     # scan + write discovery.json
  python memory_index.py --list [root]         # scan, print only, no write
  python memory_index.py --config config.yaml  # build index (auto/manual)
  python memory_index.py --config config.yaml --mode internal
  python memory_index.py --demo                # self-test

Single-source note (0.4.1): this file is the ONE source. The published
package copy at scripts/memory_index.py is byte-identical (cp); private
layouts/agent lists live in the maintainers' own private config, never here.
"""
import argparse, glob, hashlib, json, os, re, sys, tempfile
from datetime import datetime, timedelta

# ── Single source of truth for discovery candidates (community conventions) ──
# Order IS priority: first hit wins per role. Extend here only; the SKILL.md
# hand-list is a derived summary pointing back to this file.
RULES_CANDIDATES = [
    "CLAUDE.md", "AGENTS.md", "AGENTS.txt", ".cursor/rules/",  # dir
]
RULES_CANDIDATES_HOME = [
    ".claude/CLAUDE.md", ".config/agent/rules.md", ".claude/rules.md",
]
TODOS_CANDIDATES = ["TODO.md", "todo.md", "TODO.txt", "todo.txt", "tasks.md",
                    "docs/TODO.md", "docs/todo.md", "docs/todo.txt", "tasks/TODO.md"]
TODOS_CANDIDATES_HOME = ["todo.txt", ".todo/"]  # todo.txt-cli conventions
JOURNAL_DIRS = ["journal", "logs", "notes", "docs/journal", "journal/archive", "worklog"]
JOURNAL_GLOB = re.compile(r"^\d{4}-\d{2}-\d{2}\.(md|txt|markdown)$")
EXCLUDE_DIRS = {".git", ".obsidian", ".trash", ".venv", "node_modules",
                ".changsheng", "__pycache__", ".idea", ".vscode"}
DISCOVERY_FILE = "discovery.json"
TIP_SAAS = ("tip: ChangSheng targets local files. SaaS-only memory? "
            "Export it to a local folder first.")

# Display-language word table (template parametrisation). Public default is en
# (identical to 0.4.0 behaviour); `lang: zh` in the config selects Chinese row
# structure/flags. Zero private terms by design — titles, flags and row labels
# only, never role names, names or paths (those all come from config data).
_WORDS = {
    "en": {
        "title": "# memory index (auto-generated · %s)",
        "purpose1": ("> Purpose: change detection for the conditional layer (L2). "
                     "✅ new change -> read the file in full; "
                     "⏸ unchanged -> read only this index summary."),
        "purpose2": ("> The must-read layer (L3) is read every session; "
                     "the on-demand layer (L1) is read only when needed."),
        "heading": "## Conditional layer (L2) - read in full only on change",
        "flag_new": "✅ new change",
        "flag_unchanged": "⏸ unchanged",
        "summary_line": "{title}({n} lines/{kb}KB)",
        "read_failed": "read failed",
        "row_fail": "⚠️ read failed: {e} | read in full to confirm",
        "row": "- {name} | {summary} | {flag} | changed {t} | {desc}",
        "ok": "OK index written → {out} ({n} files, {c} new changes)",
    },
    "zh": {
        "title": "# 记忆索引(自动生成 · %s)",
        "purpose1": ("> 用途:条件读层(L2)变更检测。档案 ✅变更→读摘要行即可;"
                     "⏸ 未变更→只读本索引摘要。"),
        "purpose2": "> 必读层(L3)每会话必读;按需层(L1)用到才读。",
        "heading": "## 条件读层(L2)— 变更才读全文",
        "flag_new": "✅新变更",
        "flag_unchanged": "⏸未变更",
        "summary_line": "{title}({n}行/{kb}KB)",
        "read_failed": "读失败",
        "row_fail": "⚠️读取失败: {e} | 建议读全文确认",
        "row": "- {name} | {summary} | {flag} | 改于 {t} | {desc}",
        "ok": "OK 索引已生成 → {out}({n} 文件,新变更 {c} 个)",
    },
}


def _words(lang):
    return _WORDS.get(lang or "en", _WORDS["en"])


def expand(p):
    return os.path.abspath(os.path.expanduser(p))


def _unquote(v):
    """Strip one pair of matching ' or " quotes from a scalar (YAML-style).
    Applied everywhere the fallback parser reads a value so quoted configs
    parse identically to the yaml interpreter (never literal quotes in paths)."""
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def _parse_fallback(text):
    """Minimal yaml-subset parser. Supports the SHIPPED config.example shape:
    - mode: auto|manual|internal
    - nested roles block (indent-based), values are plain strings:
        roles:
          rules: [CLAUDE.md]          # inline list
          todos:                      # block list
            - docs/TODO.md
            - ~/todo.txt
    - flat role keys as an alternative: role_rules: a.md, b.md
    - list sections: must_read / tracked_files / must_read_extra / tracked_files_extra
      (dict items: path/name/desc)
    - top-level scalars: mode / memory_root / scan_root / output_dir / output_index /
      output_state / lang (en|zh display language for the generated index)
    Does NOT pre-seed empty lists — legacy keys appear only when present.
    """
    cfg = {"mode": "auto", "roles": {}}
    section = None          # "must_read" | "tracked_files" | ... | "roles" | None
    current = None          # dict item being collected (extra list sections)
    roles_key = None        # active role subkey inside roles block
    for raw in text.splitlines():
        line = raw.split("#")[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        # inside roles block: subkey (2sp) or list item (4sp)
        if section == "roles":
            if indent == 2 and not stripped.startswith("-") and ":" in stripped:
                sub_k, _, sub_v = stripped.partition(":")
                sub_k, sub_v = sub_k.strip(), sub_v.strip()
                roles_key = sub_k
                if sub_v.startswith("["):  # inline list: rules: ["a.md", "b.md"]
                    inner = sub_v[1:].rsplit("]", 1)[0]
                    cfg.setdefault("roles", {})[roles_key] = [_unquote(p) for p in inner.split(",") if p.strip()]
                else:
                    cfg.setdefault("roles", {})[roles_key] = []
                continue
            if indent == 4 and stripped.startswith("- ") and roles_key:
                cfg["roles"].setdefault(roles_key, []).append(_unquote(stripped[2:]))
                continue
            if indent == 0:
                section = None  # left roles block
        if not section and stripped.startswith("- "):
            continue  # stray list item outside a section
        if stripped.startswith("- "):
            if section is None or section == "roles":
                continue
            item = {"path": "", "name": "", "desc": ""}
            cfg.setdefault(section, []).append(item)
            current = item
            body = stripped[2:].strip()
            if ":" in body:
                k, _, v = body.partition(":")
                if k.strip() in item:
                    item[k.strip()] = _unquote(v)
            continue
        if ":" not in stripped:
            continue
        k, _, v = stripped.partition(":")
        k, v = k.strip(), v.strip()
        if k == "roles":
            section = "roles"
            roles_key = None
            current = None
        elif k in ("must_read", "tracked_files", "must_read_extra", "tracked_files_extra"):
            section = k
            current = None
        elif k == "mode":
            cfg["mode"] = _unquote(v)
            section = None
            current = None
        elif k == "lang":
            cfg["lang"] = _unquote(v)
            section = None
            current = None
        elif k.startswith("role_"):
            # flat roles alternative: role_rules: "a.md", b.md
            name = k[len("role_"):]
            cfg.setdefault("roles", {})[name] = [_unquote(p) for p in v.split(",") if p.strip()]
            section = None
            current = None
        elif k in ("memory_root", "scan_root", "output_dir", "output_index", "output_state"):
            cfg[k] = _unquote(v)
            section = None
            current = None
        elif current is not None and k in ("path", "name", "desc"):
            current[k] = _unquote(v)
    return cfg


def load_config(path):
    try:
        import yaml  # use yaml when available; degrade gracefully otherwise (see fallback)
    except ImportError:
        yaml = None
    if yaml is not None:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    with open(path, "r", encoding="utf-8") as f:
        return _parse_fallback(f.read())


def migrate_legacy(cfg):
    """0.2.x config -> 0.3: preserve semantics, never guess roles.
    Guards test CONTENT, because fallback parser never pre-seeds empty lists
    (pre-seeding made 'not in cfg' always False and silently dropped legacy files)."""
    if cfg.get("must_read") and not cfg.get("must_read_extra"):
        cfg["must_read_extra"] = cfg.pop("must_read")
    if cfg.get("tracked_files") and not cfg.get("tracked_files_extra"):
        cfg["tracked_files_extra"] = cfg.pop("tracked_files")
    if "memory_root" in cfg and "scan_root" not in cfg:
        cfg.setdefault("scan_root", cfg["memory_root"])
    return cfg


# ── discovery ────────────────────────────────────────────────────────────────

def _hit(path):
    p = expand(path)
    if not os.path.exists(p):
        return None
    if os.path.isfile(p):
        # case-insensitive fs: candidate "TODO.txt" may resolve to on-disk
        # "todo.txt" — return the real name so discovery stays honest
        d, n = os.path.split(p)
        try:
            for real in os.listdir(d):
                if real.lower() == n.lower() and os.path.isfile(os.path.join(d, real)):
                    return os.path.join(d, real)
        except OSError:
            pass
    return p


def _latest_dated_in(directory):
    """Newest YYYY-MM-DD.* file directly inside directory (1 level)."""
    d = expand(directory)
    if not os.path.isdir(d):
        return None
    best, best_m = None, None
    for name in os.listdir(d):
        if not JOURNAL_GLOB.match(name):
            continue
        p = os.path.join(d, name)
        if not os.path.isfile(p):
            continue
        m = os.path.getmtime(p)
        if best_m is None or m > best_m:
            best, best_m = p, m
    return best


def _walk_shallow(root, max_depth=2):
    """Yield dirs up to max_depth below root, skipping excludes. Never full-tree."""
    root = expand(root)
    seen = set()
    for dirpath, dirnames, _ in os.walk(root):
        depth = dirpath[len(root):].count(os.sep)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        if depth >= max_depth:
            dirnames[:] = []
            continue
        for d in list(dirnames):
            full = os.path.join(dirpath, d)
            if full not in seen:
                seen.add(full)
                yield full


def discover(scan_root, mode="auto"):
    """Locate role carriers. Returns {role: [paths...]} + missing list.
    Only paths — never reads file content."""
    root = expand(scan_root or ".")
    roles = {"rules": [], "identity": [], "todos": [], "journal": [], "profile": []}
    # identity: host-injected platforms handle identity at the SKILL layer;
    # for file-based hosts the rules file doubles as identity (top section).
    # We still probe CLAUDE.md/AGENTS.md as the identity carrier candidate.
    for cand in RULES_CANDIDATES:
        p = os.path.join(root, cand) if not os.path.isabs(cand) else cand
        h = _hit(p)
        if h:
            roles["rules"].append(h)
            roles["identity"].append(h)  # rules file doubles as identity carrier
            break
    else:
        for cand in RULES_CANDIDATES_HOME:
            h = _hit(os.path.expanduser("~/" + cand))
            if h:
                roles["rules"].append(h)
                roles["identity"].append(h)
                break
    for cand in TODOS_CANDIDATES:
        p = os.path.join(root, cand) if not os.path.isabs(cand) else cand
        h = _hit(p)
        if h:
            roles["todos"].append(h)
            break
    else:
        for cand in TODOS_CANDIDATES_HOME:
            if cand.endswith("/"):  # directory
                d = os.path.expanduser("~/" + cand.rstrip("/"))
                hit = _latest_dated_in(d) or (d if os.path.isdir(d) and os.listdir(d) else None)
                if hit:
                    roles["todos"].append(hit)
                    break
            else:
                h = _hit(os.path.expanduser("~/" + cand))
                if h:
                    roles["todos"].append(h)
                    break
    # journal: newest dated file under any conventional journal dir (shallow)
    for d in JOURNAL_DIRS:
        cand_dir = os.path.join(root, d)
        hit = _latest_dated_in(cand_dir)
        if hit:
            roles["journal"].append(hit)
            break
    missing = [r for r, v in roles.items() if not v and r != "profile"]
    return roles, missing


def discovery_path(scan_root):
    return os.path.join(expand(scan_root or "."), ".changsheng", DISCOVERY_FILE)


def load_discovery(scan_root):
    p = discovery_path(scan_root)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def discovery_still_valid(disc):
    """stat every stored path; any gone/unreadable -> re-discover (fixes V4)."""
    for role, paths in (disc or {}).get("roles", {}).items():
        for p in paths:
            if p == "injected":
                continue
            if not os.path.exists(expand(p)):
                return False
    return True


def write_discovery(scan_root, roles, missing):
    out = discovery_path(scan_root)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    payload = {"scan_root": expand(scan_root), "scanned_at": datetime.now().isoformat(timespec="minutes"),
               "roles": roles, "missing": missing}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    return payload


def print_discovery(roles, missing):
    print("ChangSheng discovery:")
    for role, paths in roles.items():
        if paths:
            joined = " · ".join(("injected" if p == "injected" else p) for p in paths)
            print(f"  {role} -> {joined}")
        else:
            print(f"  {role} -> (none)")
    if missing:
        print(f"  missing: {', '.join(missing)}")
    if all(not v for v in roles.values()):
        print("  " + TIP_SAAS)


# ── index ────────────────────────────────────────────────────────────────────

def summary(path, lang="en"):
    w = _words(lang)
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
        m = re.search(r"^#+\s+(.+)$", head, re.M) or re.search(r"^(【.+?】.+)$", head, re.M)
        title = m.group(1).strip()[:50] if m else os.path.basename(path)
        n = sum(1 for _ in open(path, "r", encoding="utf-8", errors="ignore"))
        size = os.path.getsize(path)
        return w["summary_line"].format(title=title, n=n, kb=max(1, size // 1024))
    except Exception:
        return w["read_failed"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:8]


def resolve(p, base):
    return p if os.path.isabs(p) else os.path.join(base, p)


def role_file_items(roles, base):
    """Flatten roles into L2 tracked items (path/name/desc) for indexing.
    Directories were already resolved to concrete files at discovery time."""
    items = []
    for role, paths in roles.items():
        for p in paths:
            if p == "injected" or not p:
                continue
            items.append({"path": resolve(p, base), "name": f"[{role}] {os.path.basename(p)}", "desc": role})
    return items


def expand_role_dirs(roles, base):
    """Resolve configured roles: FILE kept as-is; DIRECTORY -> newest dated file
    inside (same rule discovery uses). Applies to manual/internal modes, where
    roles come from config rather than discovery."""
    out = {}
    for role, paths in roles.items():
        resolved = []
        for p in (paths or []):
            if p == "injected":
                resolved.append(p)
                continue
            full = expand(resolve(p, base))
            if os.path.isdir(full):
                hit = _latest_dated_in(full)
                resolved.append(hit if hit else full)
            else:
                resolved.append(full)
        out[role] = resolved
    return out


def _atomic_write(path, text):
    """Write via temp file + os.replace: a crash mid-write can never leave a
    half-written index/state behind — readers keep the previous good copy.
    C34 P3#5 (parity with OpenClaw memory-builtin: build into a temp store,
    then publish atomically; on failure the old index stays intact)."""
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".mma_tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def build(out_path, state_path, files, lang="en"):
    w = _words(lang)
    prev = {}
    if os.path.exists(state_path):
        try:
            prev = json.load(open(state_path, encoding="utf-8"))
        except Exception:
            prev = {}
    now = datetime.now()
    cutoff = now - timedelta(hours=24)
    lines = [
        w["title"] % now.strftime("%Y-%m-%d %H:%M"),
        "",
        w["purpose1"],
        w["purpose2"],
        "",
        w["heading"],
        "",
    ]
    new_state = {}
    n_changed = 0
    for f in files:
        path = f.get("path", "")
        name = f.get("name") or os.path.basename(path)
        desc = f.get("desc", "")
        try:
            h = md5(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            changed = prev.get(path) != h or mtime > cutoff
            new_state[path] = h
            if changed:
                n_changed += 1
            flag = w["flag_new"] if changed else w["flag_unchanged"]
            lines.append(
                w["row"].format(name=name, summary=summary(path, lang), flag=flag,
                                t=mtime.strftime('%m-%d %H:%M'), desc=desc)
            )
        except Exception as e:
            lines.append(w["row_fail"].format(name=name, e=e))
    _atomic_write(out_path, "\n".join(lines) + "\n")
    _atomic_write(state_path, json.dumps(new_state, ensure_ascii=False, indent=1))
    print(w["ok"].format(out=out_path, n=len(files), c=n_changed))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--mode", choices=["internal", "auto", "manual"], default=None)
    ap.add_argument("--discover", nargs="?", const=".", default=None, metavar="ROOT",
                    help="scan ROOT (default .) and write .changsheng/discovery.json")
    ap.add_argument("--list", nargs="?", const=".", default=None, metavar="ROOT",
                    help="scan ROOT and print findings without writing")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        demo()
        return 0
    if args.discover is not None:
        roles, missing = discover(args.discover)
        write_discovery(args.discover, roles, missing)
        print_discovery(roles, missing)
        return 0
    if args.list is not None:
        roles, missing = discover(args.list)
        print_discovery(roles, missing)
        return 0

    # build index
    if not args.config and not os.path.exists("config.yaml"):
        # cold start with no config: discover and index what we find
        roles, missing = discover(".")
        write_discovery(".", roles, missing)
        print_discovery(roles, missing)
        files = role_file_items(roles, ".")
        out_dir = os.path.join(expand("."), ".changsheng")
        os.makedirs(out_dir, exist_ok=True)
        if not files:
            print("ERROR: nothing discovered to index. ChangSheng targets local files "
                  "(rules/todos/journal); SaaS-only memory? Export it to a local folder first.", file=sys.stderr)
            return 3
        build(os.path.join(out_dir, "memory_index.md"),
              os.path.join(out_dir, "memory_index_state.json"), files)
        return 0
    cfg = migrate_legacy(load_config(args.config or "config.yaml"))
    mode = args.mode or cfg.get("mode", "auto")
    lang = cfg.get("lang", "en")
    base = cfg.get("memory_root") or cfg.get("scan_root") or os.path.dirname(os.path.abspath(args.config or "config.yaml"))

    files = []
    roles = {}
    if mode == "auto":
        disc = load_discovery(base)
        if disc and discovery_still_valid(disc):
            roles = disc.get("roles", {})
        else:
            roles, missing = discover(base)
            write_discovery(base, roles, missing)  # missing propagated (fix 3b)
        files = role_file_items(roles, base)
    else:
        # manual / internal: roles come straight from config (fixed layout).
        # Directory roles resolve to the newest dated file inside.
        roles = expand_role_dirs(cfg.get("roles", {}) or {}, base)
        files = role_file_items(roles, base)
    for f in cfg.get("must_read_extra", []):
        f = dict(f)
        f["path"] = resolve(f["path"], base)
        files.append(f)
    for f in cfg.get("tracked_files_extra", []):
        f = dict(f)
        f["path"] = resolve(f["path"], base)
        files.append(f)

    if not files:
        # never produce a silent empty index: roles were declared but nothing resolved.
        # yaml-less manual configs: nested roles are parsed by the fallback parser;
        # flat role_* keys also work; installing PyYAML is the full-featured path.
        print("ERROR: 0 files to index — check mode/roles. In yaml-less environments the "
              "fallback parser supports nested roles (see config.example.yaml) and flat "
              "role_* keys; installing PyYAML enables the full config.", file=sys.stderr)
        return 3

    out_dir = cfg.get("output_dir") or os.path.dirname(os.path.abspath(args.config or "config.yaml"))
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(args.config or "config.yaml")), out_dir)
    os.makedirs(out_dir, exist_ok=True)
    build(os.path.join(out_dir, cfg.get("output_index", "memory_index.md")),
          os.path.join(out_dir, cfg.get("output_state", "memory_index_state.json")),
          files, lang)
    return 0


def demo():
    import shutil
    d = tempfile.mkdtemp()

    # A. discovery on three environment samples
    # A1 standard md layout
    env1 = os.path.join(d, "env1")
    os.makedirs(os.path.join(env1, "docs"))
    os.makedirs(os.path.join(env1, "journal"))
    open(os.path.join(env1, "CLAUDE.md"), "w", encoding="utf-8").write("# Rules\nbe nice\n")
    open(os.path.join(env1, "docs", "TODO.md"), "w", encoding="utf-8").write("# TODO\n- x\n")
    open(os.path.join(env1, "journal", "2026-09-04.md"), "w", encoding="utf-8").write("# 2026-09-04\nworked\n")
    r1, m1 = discover(env1)
    assert r1["rules"] and "CLAUDE.md" in r1["rules"][0], f"A1 rules failed: {r1['rules']}"
    assert r1["todos"] and "TODO.md" in r1["todos"][0], f"A1 todos failed: {r1['todos']}"
    assert r1["journal"] and "2026-09-04" in r1["journal"][0], f"A1 journal failed: {r1['journal']}"
    assert not m1 or m1 == ["profile"], f"A1 missing unexpected: {m1}"

    # A2 todo.txt layout (todo.txt-cli conventions in home are not mockable here;
    # verify project-level todo.txt + no journal)
    env2 = os.path.join(d, "env2")
    os.makedirs(env2)
    open(os.path.join(env2, "todo.txt"), "w", encoding="utf-8").write("x done\n")
    r2, m2 = discover(env2)
    assert r2["todos"] and "todo.txt" in r2["todos"][0], f"A2 todos failed: {r2['todos']}"
    assert "journal" in m2, f"A2 journal should be missing: {m2}"

    # A3 empty dir -> everything missing + SaaS tip readable
    env3 = os.path.join(d, "env3")
    os.makedirs(env3)
    r3, m3 = discover(env3)
    assert "rules" in m3 and "todos" in m3 and "journal" in m3, f"A3 missing wrong: {m3}"
    assert TIP_SAAS.startswith("tip:") and "SaaS" in TIP_SAAS, "A3 SaaS tip constant missing"

    # B. discovery.json lifecycle: valid -> reused; file deleted -> invalid
    roles, _ = discover(env1)
    write_discovery(env1, roles, [])
    assert discovery_still_valid(load_discovery(env1)), "B valid discovery should pass stat"
    os.remove(r1["journal"][0])
    assert not discovery_still_valid(load_discovery(env1)), "B deleted file must invalidate"

    # C. legacy config migration via the REAL yaml-less fallback parser
    # (regression for the silent-drop bug: fallback must not pre-seed extras,
    #  and migrate must move legacy lists by CONTENT)
    legacy_text = (
        "memory_root: .\n"
        "must_read:\n"
        "  - path: a.md\n"
        "    name: A file\n"
        "tracked_files:\n"
        "  - path: b.md\n"
        "    desc: B file\n"
    )
    lc = _parse_fallback(legacy_text)
    assert len(lc.get("must_read", [])) == 1 and len(lc.get("tracked_files", [])) == 1, \
        f"C fallback parse failed: {lc}"
    lc = migrate_legacy(lc)
    assert len(lc.get("must_read_extra", [])) == 1 and "must_read" not in lc, "C must_read migration failed"
    assert len(lc.get("tracked_files_extra", [])) == 1 and "tracked_files" not in lc, "C tracked migration failed"
    assert lc["must_read_extra"][0]["path"] == "a.md", "C content lost in migration"

    # C2. yaml-less flat roles: role_rules / role_todos -> cfg["roles"]
    flat = _parse_fallback("mode: manual\nrole_rules: CLAUDE.md, AGENTS.md\nrole_todos: docs/TODO.md\n")
    assert flat["mode"] == "manual" and flat["roles"]["rules"] == ["CLAUDE.md", "AGENTS.md"], \
        f"C2 flat roles failed: {flat}"

    # C3. yaml-less NESTED roles (the SHIPPED config.example shape) — regression
    # for the "nested roles silently lost without yaml" defect: inline + block lists
    nested = _parse_fallback(
        "mode: manual\n"
        "roles:\n"
        "  rules: [CLAUDE.md]\n"
        "  todos:\n"
        "    - docs/TODO.md\n"
        "    - ~/todo.txt\n"
        "  journal: []\n"
        "must_read_extra:\n"
        "  - path: README.md\n"
        "    name: Readme\n"
    )
    assert nested["mode"] == "manual", f"C3 mode failed: {nested}"
    assert nested["roles"]["rules"] == ["CLAUDE.md"], f"C3 inline list failed: {nested['roles']}"
    assert nested["roles"]["todos"] == ["docs/TODO.md", "~/todo.txt"], f"C3 block list failed: {nested['roles']}"
    assert nested["roles"]["journal"] == [], f"C3 empty subkey failed: {nested['roles']}"
    assert len(nested["must_read_extra"]) == 1 and nested["must_read_extra"][0]["path"] == "README.md", \
        f"C3 must_read_extra after roles failed: {nested}"

    # C4. quoted scalars parse identically to unquoted (regression: fallback
    # used to keep literal quotes -> paths like '\"CLAUDE.md\"' read-failed)
    quoted = _parse_fallback(
        'mode: "manual"\n'
        'roles:\n'
        '  rules: ["CLAUDE.md", \'AGENTS.md\']\n'
        '  todos:\n'
        '    - "docs/TODO.md"\n'
        "role_journal: 'journal'\n"
        'must_read_extra:\n'
        '  - path: "README.md"\n'
        "    name: 'Readme'\n"
    )
    assert quoted["mode"] == "manual", f"C4 mode unquote failed: {quoted['mode']!r}"
    assert quoted["roles"]["rules"] == ["CLAUDE.md", "AGENTS.md"], f"C4 inline unquote failed: {quoted['roles']}"
    assert quoted["roles"]["todos"] == ["docs/TODO.md"], f"C4 block unquote failed: {quoted['roles']}"
    assert quoted["roles"]["journal"] == ["journal"], f"C4 flat unquote failed: {quoted['roles']}"
    assert quoted["must_read_extra"][0]["path"] == "README.md" and quoted["must_read_extra"][0]["name"] == "Readme", \
        f"C4 dict unquote failed: {quoted['must_read_extra']}"

    # D. index build still works (3 scenarios from 0.2.x)
    p = os.path.join(d, "t.md")
    open(p, "w", encoding="utf-8").write("# Test doc\ncontent")
    files = [{"path": p, "name": "Test file", "desc": "demo"}]

    def file_flags(idx_path):
        txt = open(idx_path, encoding="utf-8").read()
        rows = [ln for ln in txt.splitlines() if ln.startswith("- ")]
        return (sum(1 for ln in rows if "✅ new change" in ln),
                sum(1 for ln in rows if "⏸ unchanged" in ln))

    build(os.path.join(d, "idx.md"), os.path.join(d, "st.json"), files)
    c1, u1 = file_flags(os.path.join(d, "idx.md"))
    assert c1 == 1 and u1 == 0, f"D1 got {c1} changed {u1} unchanged"
    old = datetime.now().timestamp() - 48 * 3600
    os.utime(p, (old, old))
    build(os.path.join(d, "idx.md"), os.path.join(d, "st.json"), files)
    c2, u2 = file_flags(os.path.join(d, "idx.md"))
    assert c2 == 0 and u2 == 1, f"D2 got {c2} changed {u2} unchanged"
    open(p, "w", encoding="utf-8").write("# Test doc\ncontent changed")
    build(os.path.join(d, "idx.md"), os.path.join(d, "st.json"), files)
    c3, u3 = file_flags(os.path.join(d, "idx.md"))
    assert c3 == 1 and u3 == 0, f"D3 got {c3} changed {u3} unchanged"

    # E. atomic write (C34 P3#5): a failed write must leave the old file intact
    #    and must not leak temp files; a good write must actually land.
    ap = os.path.join(d, "atomic.md")
    _atomic_write(ap, "v1\n")
    assert open(ap, encoding="utf-8").read() == "v1\n", "E1 first write failed"
    _atomic_write(ap, "v2\n")
    assert open(ap, encoding="utf-8").read() == "v2\n", "E2 overwrite failed"
    try:
        _atomic_write(ap, "bad \ud800\n")   # lone surrogate -> encode fails mid-write
    except UnicodeEncodeError:
        pass
    else:
        raise AssertionError("E3 unencodable text should have raised")
    assert open(ap, encoding="utf-8").read() == "v2\n", "E3 failed write clobbered the old file"
    assert not [n for n in os.listdir(d) if n.startswith(".mma_tmp_")], "E3 temp file leaked"

    shutil.rmtree(d, ignore_errors=True)
    print("demo OK: discover(3 envs: md/todo.txt/empty) + lifecycle stat + legacy migration + index 3 scenarios — all passed")


if __name__ == "__main__":
    sys.exit(main())
