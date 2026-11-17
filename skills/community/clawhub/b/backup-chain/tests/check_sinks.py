#!/usr/bin/env python3
"""Sink-inventory tripwire (v1.2.2).

WHAT THIS IS: a syntactic check that makes DRIFT in the tool's side effects
visible. It scans scripts/backup_chain.py with `ast` and compares, against a
registry a human or agent has to edit on purpose:

  1. every filesystem-write / process-spawn / archive-write call, keyed by
     (enclosing function, kind, count) — a new sink, a removed sink, or a
     changed count fails until the registry says what it is and why it is
     acceptable;
  2. BANNED kinds that are not registrable at all: pathname-reopening writers
     (shutil.copy*/move, open(...,'w'/'x'), os.open). v1.2.1 shipped exactly
     one of these (shutil.copy2 in stow_to_dir) beside a changelog saying
     every write was staged; it followed a planted symlink and then reported a
     verified copy. Staged fd-writes + os.replace are the only write path;
  3. the import set — so "no network code in this script" is a checked claim,
     not only a stated one: adding socket/urllib/ctypes/... fails until it is
     registered. (Operator-supplied commands run via consent-exec can still
     reach a network by design; this scans the script, not what it launches.)
  4. dynamic features that would hide a sink from this very scan (eval, exec,
     compile, __import__, importlib, setattr/globals/locals, getattr on a
     sink module);
  5. the file set of scripts/ — a second script is outside the scan's reach.

WHAT THIS IS NOT: proof that a registered sink is safe. It sees that the
inventory moved, not whether the move is sound. A registry row can be filled
in carelessly; `--print` therefore emits rows with class=TODO/why=TODO, which
the check rejects until a reader has written a real reason. It reads one
file's syntax: a sink reached through a helper in another module, or through a
construct this scan does not model, is invisible to it (see METHOD.md and
RESIDUAL_RISK item 14 for the standing list of what it leaves unseen).

Usage: check_sinks.py [--script PATH] [--registry PATH] [--print]
Exit 0 = inventory matches ("SINKS OK"); 1 = drift or violation.
"""
import argparse
import ast
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCRIPT = os.path.join(HERE, "..", "scripts", "backup_chain.py")
DEFAULT_REGISTRY = os.path.join(HERE, "sink_registry.txt")

CLASSES = {
    "staged-write":    "written through a secure_staging fd, moved in with os.replace",
    "staged-meta":     "metadata applied to our own staging file",
    "tar-into-staged": "tar members added to an archive whose file object is a staged fd",
    "append-gated":    "ledger append: realpath containment + consent for external paths",
    "consent-exec":    "subprocess behind per-invocation consent or CLI-only operator voice",
    "dir-create":      "directory creation at an operator-chosen or containment-checked path",
    "cleanup-own":     "removes only files/dirs this process created",
}
WRITE_MODE_CHARS = set("wax+")
OS_SINKS = {"replace", "rename", "remove", "unlink", "makedirs", "mkdir",
            "symlink", "link", "chmod", "fchmod", "utime", "truncate", "fdopen",
            "system", "popen", "rmdir", "removedirs", "open", "write",
            "mkfifo", "mknod"} | {"execv", "execve", "execvp", "execl", "execlp"}
SHUTIL_SINKS = {"copy", "copy2", "copyfile", "copyfileobj", "copytree", "move",
                "rmtree", "copymode", "copystat"}
SUBPROC_SINKS = {"run", "Popen", "call", "check_call", "check_output"}
TEMPFILE_SINKS = {"mkstemp", "mkdtemp", "NamedTemporaryFile", "TemporaryFile",
                  "TemporaryDirectory"}
TAR_METHODS = {"add", "addfile", "extractall", "extract"}
SINK_MODULES = {"os", "shutil", "subprocess", "tarfile", "tempfile", "sys", "io"}
# Registrable? No: these reopen a pathname for writing (follows symlinks).
BANNED_KINDS = {"shutil.copy", "shutil.copy2", "shutil.copyfile",
                "shutil.copytree", "shutil.move", "os.open", "os.system",
                "os.popen"}
BANNED_CALLS = {"eval", "exec", "compile", "__import__", "setattr", "globals",
                "locals"}


def _mode(call, pos):
    """Constant mode string, None if absent, '?' if present but not constant."""
    if len(call.args) > pos:
        a = call.args[pos]
        return a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else "?"
    for k in call.keywords:
        if k.arg == "mode":
            return k.value.value if isinstance(k.value, ast.Constant) and isinstance(k.value.value, str) else "?"
    return None


def _writes(mode):
    return mode == "?" or (isinstance(mode, str) and bool(set(mode) & WRITE_MODE_CHARS))


def _funcs_with_tarfile_open(tree):
    out = set()
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(fn):
                if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                        and n.func.attr == "open" and isinstance(n.func.value, ast.Name)
                        and n.func.value.id == "tarfile"):
                    out.add(fn.name)
    return out


def scan(path):
    """Return (sinks Counter[(func, kind)], imports set, violations list)."""
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    tar_funcs = _funcs_with_tarfile_open(tree)
    sinks = collections.Counter()
    violations = []
    imports = set()

    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            imports.add((n.module or "").split(".")[0])

    def visit(node, fn):
        for ch in ast.iter_child_nodes(node):
            nfn = ch.name if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            if isinstance(ch, ast.Call):
                f, kind = ch.func, None
                if isinstance(f, ast.Name):
                    if f.id == "open":
                        m = _mode(ch, 1)
                        if _writes(m):
                            kind = "open(dynamic)" if m == "?" else "open(%s)" % "".join(sorted(set(m) - set("tb")))
                    elif f.id in BANNED_CALLS:
                        violations.append(f"dynamic feature {f.id}() in {fn or '<module>'} — "
                                          "indirection that would hide a sink from this scan")
                    elif f.id in ("getattr", "setattr") and ch.args:
                        a0 = ch.args[0]
                        if isinstance(a0, ast.Name) and a0.id in SINK_MODULES:
                            violations.append(f"{f.id}({a0.id}, …) in {fn or '<module>'} — "
                                              "attribute indirection on a sink module")
                elif isinstance(f, ast.Attribute):
                    base = f.value.id if isinstance(f.value, ast.Name) else None
                    if base == "os" and f.attr in OS_SINKS:
                        kind = "os." + f.attr
                        if f.attr == "fdopen" and not _writes(_mode(ch, 1)):
                            kind = None
                    elif base == "shutil" and f.attr in SHUTIL_SINKS:
                        kind = "shutil." + f.attr
                    elif base == "subprocess" and f.attr in SUBPROC_SINKS:
                        kind = "subprocess." + f.attr
                    elif base == "tempfile" and f.attr in TEMPFILE_SINKS:
                        kind = "tempfile." + f.attr
                    elif base == "tarfile" and f.attr == "open":
                        m = _mode(ch, 1)
                        if m is None:
                            for k in ch.keywords:
                                if k.arg == "mode":
                                    m = k.value.value if isinstance(k.value, ast.Constant) else "?"
                        if m == "?" or (isinstance(m, str) and "w" in m):
                            kind = "tarfile.open(write)"
                    elif base == "io" and f.attr == "open" and _writes(_mode(ch, 1)):
                        kind = "io.open(write)"
                    elif f.attr in ("write_text", "write_bytes"):
                        kind = "pathlib.%s" % f.attr
                    elif f.attr in TAR_METHODS and fn in tar_funcs:
                        kind = "archive." + f.attr
                if kind:
                    sinks[(fn or "<module>", kind)] += 1
            visit(ch, nfn)

    visit(tree, None)
    for imp in ("importlib",):
        if imp in imports:
            violations.append("importlib imported — dynamic import would hide sinks from this scan")
    return sinks, imports, violations


def load_registry(path):
    rows, imps, files, problems = {}, set(), set(), []
    for ln, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # maxsplit=4: the free-text reason (5th field) may itself contain "|"
        parts = [p.strip() for p in line.split("|", 4)]
        if parts[0] == "import" and len(parts) == 2:
            imps.add(parts[1])
        elif parts[0] == "file" and len(parts) == 2:
            files.add(parts[1])
        elif len(parts) == 5:
            fn, kind, count, cls, why = parts
            if not count.isdigit():
                problems.append(f"registry line {ln}: count is not an integer: {count!r}")
                continue
            if (fn, kind) in rows:
                problems.append(f"registry line {ln}: duplicate row for {fn} | {kind}")
            if cls not in CLASSES:
                problems.append(f"registry line {ln}: class {cls!r} is not one of {sorted(CLASSES)}")
            if not why or why.upper() == "TODO" or len(why) < 12:
                problems.append(f"registry line {ln}: {fn} | {kind} needs a real reason (got {why!r})")
            if kind in BANNED_KINDS or (kind.startswith("open(") and kind != "open(a)"):
                problems.append(f"registry line {ln}: {kind} is a pathname-reopening writer and is not "
                                "registrable — stage through secure_staging and os.replace")
            rows[(fn, kind)] = int(count)
        else:
            problems.append(f"registry line {ln}: unrecognised row: {line[:60]!r}")
    return rows, imps, files, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--script", default=DEFAULT_SCRIPT)
    ap.add_argument("--registry", default=DEFAULT_REGISTRY)
    ap.add_argument("--print", action="store_true", dest="do_print",
                    help="print the current inventory as registry rows (class/why = TODO)")
    a = ap.parse_args(argv)

    sinks, imports, violations = scan(a.script)
    if a.do_print:
        for (fn, kind), n in sorted(sinks.items()):
            print(f"{fn} | {kind} | {n} | TODO | TODO")
        for m in sorted(imports):
            print(f"import | {m}")
        return 0

    rows, reg_imports, reg_files, problems = load_registry(a.registry)
    problems = list(violations) + problems

    for key, n in sorted(sinks.items()):
        fn, kind = key
        if kind in BANNED_KINDS or (kind.startswith("open(") and kind != "open(a)"):
            problems.append(f"BANNED sink {kind} in {fn} — pathname-reopening writers follow planted "
                            "symlinks (the v1.2.1 stow incident); use staged fd-writes + os.replace")
        elif key not in rows:
            problems.append(f"NEW sink {kind} x{n} in {fn} — classify it in the registry "
                            "(class + a real reason) before it ships")
        elif rows[key] != n:
            problems.append(f"CHANGED count for {fn} | {kind}: registry says {rows[key]}, code has {n}")
    for key in sorted(rows):
        if key not in sinks:
            problems.append(f"STALE registry row {key[0]} | {key[1]} — no such sink in the code; "
                            "remove it or the registry stops describing the program")
    for m in sorted(imports - reg_imports):
        problems.append(f"NEW import {m!r} — register it (and say why it is not network/FFI/dynamic)")
    for m in sorted(reg_imports - imports):
        problems.append(f"STALE import {m!r} in registry")
    present = {f for f in os.listdir(os.path.dirname(os.path.abspath(a.script))) if f.endswith(".py")}
    if reg_files != present:
        problems.append(f"scripts/ file set changed: registry {sorted(reg_files)}, on disk {sorted(present)} "
                        "— a script outside the registry is outside this scan")

    if problems:
        print("SINKS DRIFT")
        for p in problems:
            print("  - " + p)
        return 1
    print(f"SINKS OK ({sum(sinks.values())} sink calls in {len(sinks)} rows, {len(imports)} imports)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
