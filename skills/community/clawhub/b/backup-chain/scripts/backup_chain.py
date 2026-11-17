#!/usr/bin/env python3
"""backup-chain v1.3.2 — fenced, hash-chained workspace backups.

Protocol invariants (argued in references/PROTOCOL.md):
  1. Ordering is asserted, never inferred: a monotonic `generation` integer
     lives in a manifest INSIDE each archive; mtime and filename are claims.
  2. The chain is hash-linked: each manifest records `parent_sha256`.
     Parent resolution: ledger entry first, local manifest second, never filenames.
  3. The ledger lives outside the blast radius: an append-only record of
     `gen=N sha256=HEX parent=HEX built=ISO file=NAME entries=K` lines.
     Adapters: none | file | command. The command adapter runs ONLY the
     operator-configured commands from .vault/config.json, and only when the
     invocation carries --allow-cmd-ledger (argv vectors, never a shell).
     A file ledger whose destination resolves outside the workspace (absolute,
     traversing, or through a planted symlink) runs only when the invocation
     carries --allow-external-ledger: the config may propose, the operator
     disposes. This script itself contains no platform code and makes no
     network calls.
  4. A build is not done until a restore drill passed: extract to staging,
     hash-compare every member against the manifest's member map.
  5. Restore is per-member and verified: never bulk-extract (a failure class
     that exits 0 while writing nothing has been observed twice in production
     environments); stream each member and verify its sha256.
  6. Fencing failures are loud or refused, never silent: unreachable ledger is
     a marked SKIP, an archive older than the ledger head is a refused stale
     handoff.

Witness layer (v1.1) — witnesses, never gates:
  Each generation may carry a compressed decision trace (cot): trigger,
  belief, consciously-accepted risk, falsifier — written at decision time,
  bounded at build time (refusal, never truncation), stored in the manifest,
  and prefix-digested into its ledger line, so the why survives even when the
  archives do not. The ledger also carries witness entry types beyond build
  lines: `op=ack gen=N ts=… note=…` (a human saying "I have seen gen N and
  its drill receipt" — written when the operator actually looks, never on a
  schedule) and `event=restore|drill|evict|stow|ack-off|ack-on gen=N ts=… …`
  (the consequential custody acts — and the ack POLICY changes themselves:
  `ack-policy off` disables acks, and the decision is appended to the same
  ledger an ack would live in, because a no-ack chain must say WHY on the
  record — 'disabled by decision' and 'nobody watching' must never be
  indistinguishable to a later reader). None of these gate anything: a witness
  disagreement is an alarm, and a refusal is a gate; confusing the two
  teaches users to fix the alarm. The standing rule — every control addition
  must name the blind spot it creates, or be refused as control-inflation —
  lives in references/RESIDUAL_RISK.md.

Curation and custody hand-off (v1.2) — options, never defaults:
  Two operator decisions shaped this layer, both re-applying the founding
  constraint (an agent using this skill may have no storage beyond its own,
  and no two workspaces look alike):
  1. Exclusions are an OPTION. Per-member `--exclude PATTERN` (repeatable)
     and the pre-existing config-global `exclude` list are the whole surface;
     the only built-in patterns remain the self-exclusion class (*.tar.gz,
     receipts, .part — the chain must not swallow its own archives). An
     excluded directory prunes the walk: one pattern now stops the whole
     subtree.
  2. Off-site custody is an OPTION. `evict PATH --stow-to DIR|--stow-cmd CMD`
     removes a member from the chain only after its content landed somewhere
     (copy + hash roundtrip, or the user's own command fed the package on
     stdin); `build --stow-to/--stow-cmd` hands a FINISHED archive to the
     same destinations. Both record event=evict / event=stow witness lines.
     No upload code, no config-stored commands, no default behavior: with
     none of the flags passed, every command behaves exactly as v1.1.1.
  Detections (v1.2) — advisory failsafes, never gates: build-time warnings
  for archive growth vs the parent generation (the 30 MB creep class),
  duplicate content across members, and the largest members entering the
  chain; status shows raw member/archive totals. They see only what was
  collected, sized off raw bytes, and never change an exit code.

Staging discipline (v1.2.1) — unpredictable staging, exclusive
  creation, fd-written, atomically moved:
  Every temporary file this tool writes — config/marker/receipt/state
  writes, build and eviction .part archives, restore .restore-part
  members — is created by tempfile.mkstemp IN the destination directory:
  a random, O_CREAT|O_EXCL name nothing can pre-plant, written through
  its file descriptor (never by reopening the pathname), fsynced, then
  moved into place with os.replace. Until v1.2.0 the staging names were
  predictable (.<name>.tmp, <archive>.part, <member>.restore-part), so
  anyone who could write to a destination directory (an operator-set
  --output, an external ledger path, a restore --target) could pre-create
  the staging path as a symlink and have the write follow it outside the
  chosen boundary — audit T09 round 6 (v1.2.0 re-scan): "Predictable
  Temporary Files Permit Symlink-Based Writes Outside Authorized
  Boundaries". Staging keeps the *.part suffix family, so the
  self-exclusion class still shields crash leftovers from re-collection.
  Residual, stated plainly: an attacker who controls a destination
  directory still controls the files in it — this hardening removes the
  out-of-boundary write primitive, not the trustworthiness of a hostile
  directory.

Output containment (v1.3.2) — one gate for every writer of the
  configured output dir:
  Audit T09 round 8 (v1.3.1 re-scan): "Eviction Output Can Escape the
  Workspace Through a Symlinked Output Directory" — evict had inherited
  the pre-round-4 pattern and wrote the eviction package (often the
  credential-bearing member eviction exists to move) and its receipt
  wherever the workspace-controlled output_dir resolved, symlinked
  components included. Reproduced against shipped 1.3.1 bytes before the
  fix; closed by promoting build's round-4 realpath containment into ONE
  shared helper (contained_output_dir) that build and evict both call
  BEFORE makedirs or staging — a refusal leaves nothing behind, not even
  a directory. Escape hatches stay per-invocation and CLI-only: build
  --output, evict --stow-to/--stow-cmd.

Exit codes: 0 success · 1 failure (gate/verification/drill/mismatch) ·
2 refused (fencing refuse, overwrite without --overwrite, dangerous target,
evict without a custody destination). Detections never change an exit code.

Python 3.8+, standard library only. No network. Member bytes are hashed and
streamed, never parsed, logged, or transmitted.
"""
import argparse
import fnmatch
import hashlib
import io
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone

VERSION = "1.3.2"
DEFAULT_ARCHIVE_MODE = 0o600
VAULT = ".vault"
MANIFEST_NAME = "backup-manifest.json"
MARKER_NAME = "backup-chain-dir"
LAST_BUILD = "last_build.json"
LEDGER_FILE = "ledger.log"
GEN_RE = re.compile(r"^gen=(\d+)\b", re.M)
SHA_RE = re.compile(r"sha256=([0-9a-f]{64})")
COT_RE = re.compile(r"(?:^|\s)cot=(\S+)")
ACK_RE = re.compile(r"^op=ack\s+gen=(\d+)(?:\s+ts=([^\s]+))?(?:\s+note=(.*))?$")
# Witness-layer budgets. The caps are refusal boundaries, not truncation
# targets: truncation silently edits reasoning, and silent edits are what
# this skill exists to refuse.
COT_TRIGGERS = ("schedule", "pre-migration", "pre-risky-op", "post-heal",
                "manual", "anomaly")
COT_CAPS = {"b": 140, "r": 80, "f": 80}
COT_TOTAL_CAP = 320
COT_DIGEST_LEN = 96
ACK_NOTE_CAP = 120
SECRET_HINTS = ("credential", "creds", "secret", "token", "passwd", "password",
                "private_key", "id_rsa", "id_ed25519", "id_ecdsa", ".pem",
                ".p12", ".keystore", "apikey", "api_key", "auth_header")
DEFAULT_EXCLUDES = ["*.tar.gz", "*.tar.gz.sha256", "*.part"]
EVICT_MANIFEST_NAME = "evict-manifest.json"
STOW_CMD_TIMEOUT = 300  # seconds; uploads can be slow, reads stay at 120
EVICT_NOTE_CAP = 200
# Detections (v1.2) — advisory thresholds, all operator-tunable through the
# config `detect` object. Defaults are generous on purpose: a failsafe that
# cries wolf on small chains trains its reader to ignore it.
DETECT_DEFAULTS = {"enabled": True, "growth_pct": 50.0, "growth_mb": 4.0,
                   "archive_mb": 32.0}
OPS_RE = re.compile(
    r"^event=(evict|stow|ack-off|ack-on)\s+gen=(\d+)\s+ts=(\S+)(.*)$")


class GateError(Exception):
    """Exit 1 — a gate, verification, drill, or restore failure."""


class Refused(Exception):
    """Exit 2 — dangerous or fencing-refused operation."""


def now_iso():
    return datetime.now(timezone.utc).isoformat()[:19] + "Z"


# --- one definition of "a line break" for every ledger writer AND reader -----
# The ledger is line-oriented and its readers used str.splitlines(), which
# splits on far more than \n and \r: also \x0b \x0c \x1c \x1d \x1e \x85
# \u2028 \u2029. Validators that rejected only \n/\r/\x00 therefore let a
# note such as "x\u2028gen=1 sha256=<64 hex>" be WRITTEN as one physical line
# and READ BACK as two — the second being a forged build entry. v1.2.2 closes
# it three ways: writers refuse the whole class (has_line_break, enforced at
# the ledger_append chokepoint), filename-derived fields are escaped rather
# than refused (ledger_field), and readers split on "\n" only (ledger_lines),
# so a line poisoned by an older version is inert too.
_LINE_BREAK_CHARS = "\x00\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029"
_LINE_BREAK_RE = re.compile("[" + _LINE_BREAK_CHARS + "]")
_LEDGER_ESCAPE_RE = re.compile("[\x00-\x1f\x7f\x85\u2028\u2029]")


def has_line_break(s):
    """True if `s` contains anything a line-splitting reader could break on."""
    return bool(_LINE_BREAK_RE.search(s))


def ledger_field(v):
    """Make a filename-derived value safe to embed in a one-line ledger entry
    by escaping control and line-boundary characters as %XX (UTF-8 bytes).
    Legal-but-hostile names stay recordable — and faithful — instead of
    either forging a second entry or failing the act being witnessed."""
    def esc(m):
        return "".join("%%%02X" % b for b in m.group(0).encode("utf-8"))
    return _LEDGER_ESCAPE_RE.sub(esc, str(v))


def ledger_lines(text):
    """Split ledger text on "\n" ONLY (dropping the CR of a CRLF file) — never
    str.splitlines(), whose extra separators are exactly what a forged
    ledger line hides behind."""
    return [ln[:-1] if ln.endswith("\r") else ln for ln in (text or "").split("\n")]


_LEDGER_ANOMALY_WARNED = False


def warn_ledger_anomalies(text):
    """Alarm, never a gate: a ledger line holding a line-boundary or control
    character was written by an older version or by hand — a forgery attempt
    until shown otherwise. Reading it as ONE line already makes it inert; this
    makes the inertness visible, because a control that fails quietly is the
    kind this project refuses. Once per process."""
    global _LEDGER_ANOMALY_WARNED
    n = sum(1 for ln in ledger_lines(text) if has_line_break(ln))
    if n and not _LEDGER_ANOMALY_WARNED:
        _LEDGER_ANOMALY_WARNED = True
        print(f"LEDGER-ANOMALY: {n} ledger line(s) contain embedded line-break or "
              "control characters — written by an older version or by hand "
              "(possible forgery attempt). They are read as single lines and "
              "cannot create entries; inspect the ledger.", file=sys.stderr)


def safe_name_component(s, cap=80):
    """A member's basename as part of an output FILENAME: no separators or
    control characters (they would reach the ledger and the .sha256 sidecar),
    bounded length (an unbounded one made evict crash with ENAMETOOLONG)."""
    s = re.sub("[\x00-\x1f\x7f\x85\u2028\u2029/\\\\]", "_", s)
    return s[:cap] or "member"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def set_fd_mode(fd, mode=None):
    """Apply a permission mode through the fd of a file this process created
    (never by reopening a pathname — see tests/sink_registry.txt). mode=None
    keeps the pre-1.2.1 parity default for internal state files: 0666 & ~umask
    (best effort on platforms without fchmod — Windows keeps mkstemp's
    owner-only mode). An explicit mode — the v1.3.0 archive/receipt default
    is 0600 — is applied VERBATIM: the operator asked for that mode, so the
    ambient umask neither widens nor narrows it (--archive-mode 0644 means
    0644 whatever the umask is; the G7 receipt line prints what landed)."""
    if hasattr(os, "fchmod"):
        if mode is None:
            um = os.umask(0)
            os.umask(um)
            mode = 0o666 & ~um
        os.fchmod(fd, mode)


def parse_archive_mode(v, origin):
    """Validate an archive/receipt mode arriving from the CLI or config.json.
    Accepts 384, "384", "600", "0600" (octal digits). Refuses exec/setuid/
    setgid/sticky bits and anything above 0666 — archives are data files —
    loud (Refused, rc 2), naming where the value came from. Whether a value
    may WIDEN anything is resolve_archive_mode's decision, not this
    function's: since v1.3.1 (audit T09, round 7) only the operator's own
    --archive-mode flag can widen — a planted config value is never
    consulted for widening at all."""
    if isinstance(v, bool):
        raise Refused(f"{origin}: boolean is not an octal mode")
    if isinstance(v, int):
        m = v
    else:
        s = str(v).strip()
        if not re.fullmatch(r"[0-7]{1,4}", s):
            raise Refused(f"{origin}: not an octal mode: {v!r}")
        m = int(s, 8)
    if m < 0 or m & ~0o666:
        raise Refused(f"{origin}: mode {m:o} outside 0..0666 (no exec/setuid/"
                      "setgid/sticky bits on archives)")
    return m


def resolve_archive_mode(cli_val, cfg):
    """--archive-mode (the operator's own voice on the CLI) > the persistent
    config key archive_mode > DEFAULT_ARCHIVE_MODE (0600: archives, their
    receipts and stow copies are owner-only unless widened deliberately,
    v1.3.0). T09 (round 7, v1.3.1): the config key arrives from the
    workspace — adversarial input like the rest of config — so it may
    NARROW the artifacts (any mode with no group/other bits) but never
    widen them: a group/other bit is refused loudly, rc 2, naming the
    remedy. 1.3.0 let a planted config value reach 0666 "at most, visible
    on the G7 line" — but visibility is not consent, the same argument
    that closed 1.0.4's T09 on command execution; an operator who never
    runs stat never sees the G7 line either. Widening is the operator's
    own per-invocation act, echoed on the G7 line: --archive-mode 0644."""
    if cli_val is not None:
        return parse_archive_mode(cli_val, "--archive-mode")
    if isinstance(cfg, dict) and cfg.get("archive_mode") is not None:
        m = parse_archive_mode(cfg["archive_mode"], "config archive_mode")
        if m & 0o077:
            raise Refused(
                f"config archive_mode {m:04o} grants group/other access to "
                "archives, receipts and stow copies — workspace config may "
                "narrow artifact permissions but never widen them; widening "
                "is the operator's own per-invocation act: --archive-mode "
                "(config is code; see references/SECURITY.md)")
        return m
    return DEFAULT_ARCHIVE_MODE


def secure_staging(path, kind):
    """Create a securely-named staging file in the destination directory.

    T09 (round 6, v1.2.1): the old staging names were predictable
    (.<name>.tmp, <archive>.part, <member>.restore-part), so an attacker
    who could write to the destination directory could pre-create the
    staging path as a symlink and make the write follow it outside the
    boundary the operator chose. mkstemp creates a random name with
    O_CREAT|O_EXCL — nothing can be pre-planted at it — and the caller
    writes through the returned fd, never by reopening the pathname. The
    fstat assertion documents the guarantee: the fd is the regular file
    mkstemp just created. The *.part suffix keeps every staging leftover
    inside the self-exclusion class (*.part) even after a mid-write crash.
    """
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".%s.%s-" % (os.path.basename(path), kind),
                               suffix=".part", dir=d)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise GateError("staging file is not a regular file: %s" % tmp)
    return fd, tmp


def discard_staging(tmp):
    """Remove our own staging file; unlink operates on the link itself."""
    try:
        os.unlink(tmp)
    except OSError:
        pass


def atomic_write(path, data, binary=False, mode=None):
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = secure_staging(path, "atomic")
    fobj = None
    try:
        set_fd_mode(fd, mode)
        fobj = os.fdopen(fd, "wb" if binary else "w")
        fobj.write(data)
        fobj.flush()
        os.fsync(fobj.fileno())
        fobj.close()
        fobj = None
        os.replace(tmp, path)
    finally:
        if fobj is not None:
            try:
                fobj.close()
            except OSError:
                pass
        discard_staging(tmp)


def normalize_member(p):
    """Normalize a member path to a safe forward-slash relpath. Refuse escapes."""
    if p.startswith("~"):
        raise Refused(f"member path may not start with '~': {p}")
    parts = [x for x in re.split(r"[\\/]+", p) if x not in ("", ".")]
    if p.startswith("/") or (len(parts) > 0 and ":" in parts[0] and len(parts[0]) <= 2):
        raise Refused(f"member path must be relative to the project root: {p}")
    if any(x == ".." for x in parts):
        raise Refused(f"member path may not contain '..': {p}")
    if not parts:
        raise Refused("empty member path")
    return "/".join(parts)


def validate_archive_names(names):
    """Defence in depth: refuse any archive member that would escape the target.

    Rejects POSIX absolute paths, backslashes, '..' segments, NUL, and
    drive-letter paths (e.g. 'C:/x' or 'C:\\x'). The drive-letter case only
    bites on Windows hosts (os.path.join treats 'C:/x' as absolute there,
    silently dropping --target), but this script may run on one, and a
    restored archive is not necessarily one this script built.
    """
    bad = []
    for n in names:
        first = re.split(r"[\\/]+", n, maxsplit=1)[0]
        if (n.startswith("/") or n.startswith("\\") or "\\" in n
                or ".." in n.split("/") or "\x00" in n
                or (":" in first and len(first) <= 2)):
            bad.append(n)
    if bad:
        raise GateError("archive contains unsafe member paths: " + ", ".join(bad[:5]))


# ---------------------------------------------------------------- config ----

def vault_dir(root):
    return os.path.join(root, VAULT)


def config_path(root):
    return os.path.join(vault_dir(root), "config.json")


def validate_chain_name(name):
    """Audit T09 (round 4): chain_name becomes part of archive FILENAMES
    (<name>-g<N>.tar.gz), so a workspace-contributed config may not use it to
    traverse. Separator-free; spaces/unicode stay legal because init derives
    the default from the workspace basename."""
    if not isinstance(name, str) or not name:
        raise GateError("chain_name is empty — edit .vault/config.json or re-init")
    if len(name) > 128 or "\x00" in name:
        raise GateError(f"chain_name is not a usable filename component: "
                        f"{name[:24]!r}…")
    if "/" in name or "\\" in name or any(x == ".." for x in name.split()):
        raise GateError(f"chain_name may not contain path separators or '..': {name!r}")
    return name


def config_rel_inside(p, what):
    """Audit T09 (round 4): config-supplied filesystem paths (output_dir) must
    stay inside the workspace. Absolute, home-relative, traversing, and empty
    paths are refused; the per-invocation CLI (--output) remains the
    operator's escape hatch for external locations. Returns the normalized
    value, so downstream joins cannot reintroduce separators games."""
    if not isinstance(p, str) or not p.strip():
        raise GateError(f"{what} is empty — edit .vault/config.json or re-init")
    if p.startswith("~"):
        raise GateError(f"{what} may not start with '~': {p!r}")
    parts = [x for x in re.split(r"[\\/]+", p) if x not in ("", ".")]
    if p.startswith("/") or (parts and ":" in parts[0] and len(parts[0]) <= 2):
        raise GateError(f"{what} must be relative to the project root "
                        f"(pass --output for an external location): {p!r}")
    if any(x == ".." for x in parts) or "\x00" in p:
        raise GateError(f"{what} may not traverse outside the project root: {p!r}")
    if not parts:
        raise GateError(f"{what} may not be empty: {p!r}")
    return "/".join(parts)


def load_config(root):
    """Load and RE-VALIDATE .vault/config.json (audit T09, round 4).

    The config is workspace-contributed state — adversarial input, same trust
    class as the ledger command adapter: it may propose, the invocation root
    disposes. The stored root is pinned to the canonical invocation root, and
    every path the config controls (members, chain_name, output_dir) is
    re-validated HERE, not only at 'init'/'member add' time, so a hand-edited
    or planted config cannot redirect what gets read or where archives land.
    """
    p = config_path(root)
    if not os.path.exists(p):
        raise GateError(f"no backup-chain config at {p} — run 'init' first")
    with open(p) as f:
        cfg = json.load(f)
    if cfg.get("protocol") != "backup-chain/1":
        raise GateError(f"unsupported config protocol: {cfg.get('protocol')!r}")
    # Root pin: the stored root must BE this workspace (realpath equality, so
    # symlinked paths to the same workspace still pass). A config claiming a
    # different root would otherwise redirect member collection, output
    # resolution, and ledger paths — collecting files far outside the tree
    # the user selected. If the workspace MOVED, fix 'root' in the config or
    # re-init with --force; neither direction is taken silently.
    stored = cfg.get("root")
    if not isinstance(stored, str) or not stored:
        raise GateError("config has no root — re-init (init --force)")
    root_rp = os.path.realpath(root)
    if os.path.realpath(stored) != root_rp:
        raise GateError(
            "config root is not this workspace: initialized at "
            f"{stored!r}, invoked at {root!r} — a workspace config may not "
            "redirect the backup boundary. If the workspace moved, fix 'root' "
            "in .vault/config.json (or re-init with --force).")
    cfg["root"] = root_rp  # authoritative from here on
    cfg["chain_name"] = validate_chain_name(cfg.get("chain_name"))
    cfg["output_dir"] = config_rel_inside(cfg.get("output_dir"), "output_dir")
    members = cfg.get("members")
    if not isinstance(members, list):
        raise GateError("config members is not a list — edit .vault/config.json")
    for mem in members:
        if not isinstance(mem, dict) or not isinstance(mem.get("path"), str):
            raise GateError("config member without a string path — "
                            "edit .vault/config.json")
        try:
            mem["path"] = normalize_member(mem["path"])
        except Refused as e:
            raise GateError(f"config member rejected: {e}")
        # v1.2: per-member exclude patterns are config-contributed too — same
        # shape discipline as every other config-controlled list.
        mexp = mem.get("exclude", [])
        if not isinstance(mexp, list) or any(
                not isinstance(p, str) or not p.strip() or "\x00" in p
                for p in mexp):
            raise GateError(f"config member {mem['path']!r} exclude must be a "
                            "list of non-empty pattern strings — edit "
                            ".vault/config.json")
    # v1.2: the config-global exclude list existed since 1.0 but was never
    # shape-checked; tightened alongside per-member excludes (additive — any
    # previously-working config already holds valid patterns).
    exp = cfg.get("exclude", [])
    if not isinstance(exp, list) or any(
            not isinstance(p, str) or not p.strip() or "\x00" in p
            for p in exp):
        raise GateError("config exclude must be a list of non-empty pattern "
                        "strings — edit .vault/config.json")
    # v1.2: detection thresholds (advisory) are config-controlled; validate
    # the shape so a typo fails loudly here instead of silently never firing.
    det = cfg.get("detect")
    if det is not None:
        if not isinstance(det, dict):
            raise GateError("config detect is not an object — edit "
                            ".vault/config.json")
        if "enabled" in det and not isinstance(det["enabled"], bool):
            raise GateError("config detect.enabled must be a boolean")
        for k in ("growth_pct", "growth_mb", "archive_mb"):
            if k in det and (isinstance(det[k], bool)
                             or not isinstance(det[k], (int, float))
                             or det[k] < 0):
                raise GateError(f"config detect.{k} must be a non-negative "
                                "number")
    # v1.2: ack policy — operational state for a decision whose DURABLE record
    # is the ledger line (event=ack-off), not this key. Shape-checked so a
    # typo fails loudly instead of silently re-enabling or never refusing.
    pol = cfg.get("ack_policy")
    if pol is not None:
        if not isinstance(pol, dict) or pol.get("mode") != "off":
            raise GateError("config ack_policy must be an object with mode "
                            "'off' (absent means acks enabled) — edit "
                            ".vault/config.json")
        for k in ("ts", "note"):
            if k in pol and not isinstance(pol[k], str):
                raise GateError(f"config ack_policy.{k} must be a string")
        if "gen" in pol and (isinstance(pol["gen"], bool)
                             or not isinstance(pol["gen"], int)
                             or pol["gen"] < 0):
            raise GateError("config ack_policy.gen must be a non-negative "
                            "integer")
    # Audit T09 (round 5): ledger is the last config-controlled sink — validate
    # its SHAPE here (type/emptiness/NUL). Containment is decided at every USE
    # (ledger_state/ledger_append -> ledger_file_path), because the decision
    # depends on a per-invocation flag, not on the config alone.
    led = cfg.get("ledger")
    if led is not None:
        if not isinstance(led, dict):
            raise GateError("config ledger is not an object — edit "
                            ".vault/config.json or re-init")
        lf = led.get("file")
        if lf is not None and (not isinstance(lf, str) or not lf.strip()
                               or "\x00" in lf):
            raise GateError("ledger.file is not a usable path — edit "
                            ".vault/config.json or re-init")
    return cfg


def save_config(root, cfg):
    cfg["protocol"] = "backup-chain/1"
    atomic_write(config_path(root), json.dumps(cfg, indent=2, sort_keys=True) + "\n")
    atomic_write(os.path.join(vault_dir(root), MARKER_NAME),
                 "owned by backup-chain; commands refuse to touch unmarked vaults\n")


def default_config(root, name, output_dir, ledger, ledger_file, read_cmd, append_cmd):
    # init-time validation (audit T09, round 4): the operator's own arguments
    # face the same boundary checks that config re-validation applies later,
    # so an unsafe value can never get INTO the config in the first place.
    try:
        name = validate_chain_name(
            name or os.path.basename(os.path.realpath(root)) or "workspace")
        output_dir = config_rel_inside(output_dir or "download", "output_dir")
    except GateError as e:
        raise Refused(str(e))
    led = {"adapter": ledger or "file"}
    if (ledger or "file") == "file":
        led["file"] = ledger_file or os.path.join(VAULT, LEDGER_FILE)
        if ledger_file:
            cand = (ledger_file if os.path.isabs(ledger_file)
                    else os.path.join(root, ledger_file))
            root_rp = os.path.realpath(root)
            if not (os.path.realpath(cand).startswith(root_rp + os.sep)):
                print(f"WARN  init: ledger file resolves outside the workspace "
                      f"({os.path.realpath(cand)}) — every runtime invocation "
                      f"that touches the ledger will need "
                      f"--allow-external-ledger", file=sys.stderr)
    if (ledger or "file") == "command":
        if not read_cmd or not append_cmd:
            raise Refused("adapter 'command' needs both --read-cmd and --append-cmd")
        led["read_cmd"], led["append_cmd"] = read_cmd, append_cmd
    return {
        "protocol": "backup-chain/1",
        "version": VERSION,
        "chain_name": name,
        "root": os.path.realpath(root),
        "output_dir": output_dir,
        "members": [],
        "exclude": [],
        "ledger": led,
        "created_at": now_iso(),
    }


def output_abs(cfg):
    p = cfg["output_dir"]
    return p if os.path.isabs(p) else os.path.join(cfg["root"], p)


def contained_output_dir(cfg, escape):
    """Audit T09 (round 8): the configured output_dir is workspace-contributed
    state, so it is contained by REALPATH before anything is written — the
    same gate build has had since round 4, promoted into ONE shared helper
    for every command that writes the configured output dir (build, evict),
    so the two can never diverge again. A lexically-inside path with a
    planted symlinked component would otherwise carry archive bytes (build)
    or the credential-bearing eviction package and its receipt (evict)
    outside the workspace. The check runs before makedirs/staging: a
    refusal leaves nothing at the destination, not even a directory.
    External destinations remain a per-invocation CLI act, named verbatim
    in the refusal."""
    outdir = output_abs(cfg)
    out_rp = os.path.realpath(outdir)
    try:
        inside = os.path.commonpath([out_rp, cfg["root"]]) == cfg["root"]
    except ValueError:  # different drives (Windows)
        inside = False
    if not inside:
        raise GateError(f"output_dir resolves outside the project root "
                        f"({outdir} -> {out_rp}) — keep output_dir inside "
                        f"the workspace, or {escape}")
    return outdir


def archive_names_for(cfg):
    base = f"{cfg['chain_name']}-g"
    try:
        files = sorted(os.listdir(output_abs(cfg)))
    except OSError:
        return []
    return [f for f in files if f.startswith(base) and f.endswith(".tar.gz")]


def is_excluded(cfg, rel, member_pats=()):
    """Exclusion check (v1.2): the built-in self-exclusion class, the
    config-global patterns, and — new — the owning member's own patterns.
    Patterns match the path relative to the project root AND the basename
    (fnmatch). The built-in class exists to keep the chain from swallowing
    its own archives; it is the ONLY default. Everything else is opt-in,
    because no two workspaces look alike."""
    if rel == VAULT or rel.startswith(VAULT + "/") or rel.startswith(VAULT + "\\"):
        return True
    for pat in DEFAULT_EXCLUDES + list(cfg.get("exclude", [])) + list(member_pats):
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(os.path.basename(rel), pat):
            return True
    return False


# ---------------------------------------------------------------- ledger ----

def parse_entries(text):
    """Build entries (`gen=…` lines). op=ack and event= lines are witness
    traffic, not build entries: GEN_RE anchors at line start, so they are
    invisible here by construction (and by test)."""
    entries = []
    for line in ledger_lines(text):
        m = GEN_RE.search(line)
        if not m:
            continue
        e = {"gen": int(m.group(1)), "raw": line.strip()}
        s = SHA_RE.search(line)
        e["sha256"] = s.group(1) if s else None
        c = COT_RE.search(line)
        e["cot"] = c.group(1) if c else None
        entries.append(e)
    return entries


def parse_ops(text):
    """Custody-op and policy witness lines (`event=evict|stow|ack-off|ack-on
    gen=N ts=… …`). Same trust model as every ledger line: shaped text is
    witness traffic, invisible to the build-entry parser by construction."""
    ops = []
    for line in ledger_lines(text):
        m = OPS_RE.match(line.strip())
        if m:
            ops.append({"op": m.group(1), "gen": int(m.group(2)),
                        "ts": m.group(3), "rest": (m.group(4) or "").strip(),
                        "raw": line.strip()})
    return ops


def parse_acks(text):
    """Operator ack lines (`op=ack gen=N ts=… note=…`). The ledger parser
    trusts any line shaped like an entry — same honesty as build entries:
    an ack is a witness, and a forged ack is detectable only as any forged
    ledger text is, by its disagreement with everything else on record."""
    acks = []
    for line in ledger_lines(text):
        m = ACK_RE.match(line.strip())
        if m:
            acks.append({"gen": int(m.group(1)), "ts": m.group(2) or "",
                         "note": (m.group(3) or "").strip(),
                         "raw": line.strip()})
    return acks


# ----------------------------------------------------- decision traces ----
# The trace is written when the decision is made or it is worthless: a trace
# written later is a narrative with better formatting (doctor_memory's
# receipts-vs-identity argument; katarina_martinity's "the receipt is written
# at decision time"). The manifest copy lives inside the archive, where a
# rollback cannot edit it without breaking hashes; the ledger line carries a
# prefix digest, so the why survives even when the archives do not.

def validate_cot(args):
    """Compose + bound the decision trace from CLI flags. Refuses; never
    truncates. All four flags absent -> None (pre-v1.1 behavior, valid)."""
    t, b = getattr(args, "cot_trigger", None), getattr(args, "cot_belief", None)
    r, f = getattr(args, "cot_risk", None), getattr(args, "cot_falsifier", None)
    if t is None and b is None and r is None and f is None:
        return None
    if t is None:
        raise Refused("--cot-belief/--cot-risk/--cot-falsifier given without "
                      "--cot-trigger — a trace names its trigger")
    if t not in COT_TRIGGERS:
        raise Refused(f"cot trigger must be one of {', '.join(COT_TRIGGERS)}: {t!r}")
    cot = {"t": t, "b": b or "", "r": r or "", "f": f or ""}
    for k, cap in COT_CAPS.items():
        v = cot[k]
        if has_line_break(v):
            raise Refused(f"cot {k} must be a single line")
        if len(v) > cap:
            raise Refused(f"cot {k} exceeds {cap} chars ({len(v)}) — shorten the "
                          "trace or split the generation; traces are refused, "
                          "never truncated")
    total = len(cot["b"]) + len(cot["r"]) + len(cot["f"])
    if total > COT_TOTAL_CAP:
        raise Refused(f"cot exceeds {COT_TOTAL_CAP} chars total ({total}) — a trace "
                      "that cannot be read after a wipe is a narrative, not a trace")
    return cot


def cot_canonical(cot):
    """Single-line canonical form the ledger digest prefixes. Whitespace is
    collapsed so a digest survives ledger round-trips through channels that
    wrap or normalize spaces (gists, forum posts, mail)."""
    can = f"t={cot.get('t', '')}|b={cot.get('b', '')}|r={cot.get('r', '')}|f={cot.get('f', '')}"
    return re.sub(r"\s+", " ", can).strip()


def cot_digest(cot):
    """Space-free prefix digest for the ledger line: ledger fields are
    space-separated and every consumer (ours and foreign) keys fields by
    whitespace, so a digest carrying spaces would silently truncate on the
    first word. Whitespace becomes '_' here and in the comparison — the
    manifest keeps the true text; only the ledger copy is normalized."""
    return re.sub(r"\s+", "_", cot_canonical(cot))[:COT_DIGEST_LEN]


def cot_secret_scan(cot):
    blob = " ".join(str(v) for v in (cot or {}).values()).lower()
    return [h for h in SECRET_HINTS if h in blob]


# ------------------------------------------------- ledger command adapter ----
# The command adapter is deliberate, opt-in functionality — config-as-code of
# the git-hook trust class (SECURITY.md). Two audit rounds shaped it:
#   1.0.3 — every execution warns once per command per process, on stderr only
#           (stdout stays clean for JSON consumers and ledger parsing).
#   1.0.4 (audit T09, round 3) — a warning is not consent, and a
#           workspace-contributed config must not fire just because a routine
#           subcommand ran. Execution now requires an explicit per-invocation
#           --allow-cmd-ledger, and commands run as argv vectors (shlex-split,
#           shell=False) — never through a shell. Shell features exist only if
#           the config names `sh -c '…'` itself, in plain sight.
#   1.0.5 (audit T09, round 4) — the same trust boundary moves from WHAT RUNS
#           to WHAT IS READ: a workspace-contributed config could redefine the
#           backup root and collect files far outside the selected project,
#           with output_dir/chain_name steering where the archive lands.
#           load_config now pins the stored root to the canonical invocation
#           root (realpath equality, refuse on mismatch) and re-validates
#           every path the config controls (members, chain_name, output_dir).
#           Config proposes; the invocation root and the operator dispose.
#   1.0.6 (audit T09, round 5) — the boundary closes over the last unvalidated
#           config sink: ledger.file. An append-only ledger is still a write
#           primitive when its destination is attacker-chosen, and a path that
#           resolves outside the workspace (absolute, traversing, or through a
#           planted symlink) now requires the same per-invocation consent class
#           as the command adapter: --allow-external-ledger. In-root ledgers —
#           including symlinked in-root targets — are unaffected; the documented
#           wipe-safety setup (init --ledger-file /external/path) survives, with
#           the operator opting in once per invocation. Resolution is realpath-
#           based at every use, so a symlink swap after approval still fails
#           closed if it leaves the boundary.
#   1.2.1 (audit T09, round 6) — the boundary closes over the tool's own
#           temporaries: staging names were predictable (.<name>.tmp,
#           <archive>.part, <member>.restore-part) and the writes went
#           through path-reopening opens that follow symlinks, so an
#           attacker able to write to a destination directory (operator-set
#           --output, external ledger path, restore --target) could
#           pre-plant the staging path as a symlink and redirect the write
#           outside the chosen boundary. All staging is now mkstemp-random,
#           O_CREAT|O_EXCL, fd-written, fsynced, and moved with os.replace;
#           the *.part suffix keeps crash leftovers inside the
#           self-exclusion class. The consent-gate classes of rounds 3-5
#           are unchanged and remain the design.
_CMD_ADAPTER_WARNED = set()
CMD_LEDGER_ALLOWED = False
EXTERNAL_LEDGER_ALLOWED = False
_EXTERNAL_LEDGER_WARNED = False


def require_cmd_ledger_opt_in():
    """Audit T09 (round 3): refuse to execute config-supplied commands unless
    this process was explicitly launched with --allow-cmd-ledger."""
    if CMD_LEDGER_ALLOWED:
        return
    raise GateError("ledger adapter 'command' refuses to execute without "
                    "explicit per-invocation opt-in — inspect "
                    ".vault/config.json (config is code; see SECURITY.md) "
                    "and re-run with --allow-cmd-ledger")


def warn_cmd_adapter(action, cmd):
    if action in _CMD_ADAPTER_WARNED:
        return
    _CMD_ADAPTER_WARNED.add(action)
    preview = " ".join(str(cmd).split())
    if len(preview) > 100:
        preview = preview[:97] + "…"
    print(f"WARN  ledger command adapter: executing {action} — "
          f"\"{preview}\" (from .vault/config.json; config is code — "
          f"see SECURITY.md)", file=sys.stderr)


def require_external_ledger_opt_in():
    """Audit T09 (round 5): refuse a file-ledger destination that resolves
    outside the workspace unless this process was explicitly launched with
    --allow-external-ledger. Same consent class as the command adapter:
    a warning is not consent, and the config may propose, the operator
    disposes."""
    if EXTERNAL_LEDGER_ALLOWED:
        return
    raise GateError("file ledger resolves outside the workspace — a "
                    "workspace-contributed config may not point ledger "
                    "appends across the boundary; re-run with "
                    "--allow-external-ledger if this destination is "
                    "deliberate (config is code; see SECURITY.md)")


def ledger_file_path(cfg):
    """Resolve the file-ledger destination (audit T09, round 5).

    Returns (path, resolved_realpath, inside_root). The containment verdict
    is REALPATH-based at every use — not cached from load time — so a symlink
    planted (or swapped) after approval still fails closed if it leaves the
    workspace. A relative path is joined to the pinned config root; the
    default destination (<root>/.vault/ledger.log) is in-root by
    construction."""
    led = cfg.get("ledger") or {}
    p = led.get("file") or os.path.join(VAULT, LEDGER_FILE)
    if not isinstance(p, str) or not p.strip() or "\x00" in p:
        raise GateError("ledger.file is not a usable path — edit "
                        ".vault/config.json or re-init")
    p = p if os.path.isabs(p) else os.path.join(cfg.get("root") or ".", p)
    rp = os.path.realpath(p)
    root_rp = os.path.realpath(cfg.get("root") or ".")
    inside = (rp == root_rp or rp.startswith(root_rp + os.sep))
    return p, rp, inside


def warn_external_ledger(rp):
    """Opted-in external ledger use still warns once per process, on stderr
    only — same transparency rule as the command adapter (stdout stays clean
    for JSON consumers and ledger parsing)."""
    global _EXTERNAL_LEDGER_WARNED
    if _EXTERNAL_LEDGER_WARNED:
        return
    _EXTERNAL_LEDGER_WARNED = True
    print(f"WARN  file ledger: destination resolves outside the workspace "
          f"({rp}) — proceeding under --allow-external-ledger",
          file=sys.stderr)


def ledger_state(cfg):
    """Return {reachable, max_gen, entries, note}. Never raises."""
    led = (cfg or {}).get("ledger") or {"adapter": "none"}
    adapter = led.get("adapter", "none")
    note = ""
    try:
        if adapter == "none":
            return {"reachable": False, "max_gen": None, "entries": [],
                    "acks": [], "ops": [],
                    "note": "no ledger configured (adapter 'none') — local-chain fencing only"}
        if adapter == "file":
            p, rp, inside = ledger_file_path(cfg)
            if not inside:
                require_external_ledger_opt_in()
                warn_external_ledger(rp)
            if not os.path.exists(p):
                return {"reachable": True, "max_gen": 0, "entries": [],
                        "acks": [], "ops": [],
                        "note": f"file ledger empty at {p}"}
            with open(p, errors="replace") as f:
                text = f.read()
            warn_ledger_anomalies(text)
            entries = parse_entries(text)
            mx = max((e["gen"] for e in entries), default=0)
            return {"reachable": True, "max_gen": mx, "entries": entries,
                    "acks": parse_acks(text), "ops": parse_ops(text),
                    "note": f"file ledger at {p}"}
        if adapter == "command":
            require_cmd_ledger_opt_in()
            warn_cmd_adapter("read_cmd", led["read_cmd"])
            try:
                argv = shlex.split(str(led["read_cmd"]))
            except ValueError as e:
                raise GateError(f"read_cmd is not a valid command line "
                                f"(shlex parse failed): {e}")
            r = subprocess.run(argv, shell=False, capture_output=True,
                               text=True, timeout=120)
            if r.returncode != 0:
                note = f"ledger read command failed (rc={r.returncode}): {r.stderr.strip()[:200]}"
                return {"reachable": False, "max_gen": None, "entries": [],
                        "acks": [], "ops": [], "note": note}
            warn_ledger_anomalies(r.stdout)
            entries = parse_entries(r.stdout)
            mx = max((e["gen"] for e in entries), default=0)
            return {"reachable": True, "max_gen": mx, "entries": entries,
                    "acks": parse_acks(r.stdout), "ops": parse_ops(r.stdout),
                    "note": "command-adapter ledger"}
    except subprocess.TimeoutExpired:
        note = "ledger read command timed out"
    except Exception as e:  # adapter misconfig, shell missing, permissions…
        note = f"ledger unreachable: {e}"
    return {"reachable": False, "max_gen": None, "entries": [], "acks": [],
            "ops": [], "note": note}


def acks_disabled(cfg):
    """True when acks are disabled by a recorded decision (config state; the
    durable record of that decision is the event=ack-off ledger line)."""
    pol = (cfg or {}).get("ack_policy")
    return bool(isinstance(pol, dict) and pol.get("mode") == "off")


def ack_policy_desc(pol):
    """One-line human description of a recorded off decision."""
    if not isinstance(pol, dict):
        return ""
    g = pol.get("gen")
    gtxt = f" gen={g}" if isinstance(g, int) else ""
    return (f"event=ack-off{gtxt} ts={pol.get('ts') or 'unknown time'}"
            + (f" note={pol['note']}" if pol.get("note") else ""))


def chain_head(cfg, ls):
    """Best-known current head: max of ledger head and local archive head."""
    return max(local_max_gen(cfg) if cfg else 0, ls.get("max_gen") or 0, 0)


def ledger_append(cfg, line):
    led = cfg.get("ledger") or {"adapter": "none"}
    adapter = led.get("adapter", "none")
    if adapter == "none":
        raise GateError("cannot register: ledger adapter is 'none'")
    if has_line_break(line.rstrip("\n")):
        # Chokepoint for every ledger writer and both adapters: callers
        # validate earlier for friendlier messages, but this is the one
        # place a future caller that forgets cannot forge a second entry.
        raise GateError("refusing to append: the ledger line contains a "
                        "line-break or control character, which a reader "
                        "would split into a forged second entry")
    if adapter == "file":
        p, rp, inside = ledger_file_path(cfg)
        if not inside:
            require_external_ledger_opt_in()
            warn_external_ledger(rp)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a") as f:
            f.write(line.rstrip("\n") + "\n")
            f.flush()
            os.fsync(f.fileno())
        return p
    if adapter == "command":
        require_cmd_ledger_opt_in()
        warn_cmd_adapter("append_cmd", led["append_cmd"])
        try:
            argv = shlex.split(str(led["append_cmd"]))
        except ValueError as e:
            raise GateError(f"append_cmd is not a valid command line "
                            f"(shlex parse failed): {e}")
        r = subprocess.run(argv, shell=False, input=line.rstrip("\n") + "\n",
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise GateError(f"ledger append command failed (rc={r.returncode}): "
                            f"{r.stderr.strip()[:300]}")
        return led["append_cmd"]
    raise GateError(f"unknown ledger adapter: {adapter}")


def ledger_entry_for(lstate, gen):
    best = None
    for e in lstate.get("entries", []):
        if e["gen"] == gen:
            best = e  # last one wins in an append-only ledger
    return best


def ledger_event(cfg, kind, gen, extra=""):
    """Record a witness event line (`event=<kind> gen=N ts=… …`). Best-effort
    by design: a custody act that already succeeded must not be marked failed
    because its witness hiccuped — the heal-note build covers the gap. Returns
    True when recorded. Events are appended through the SAME adapter path as
    build registrations, so every audit consent boundary (rounds 3–5) applies
    unchanged: a command adapter still needs --allow-cmd-ledger, an external
    file ledger still needs --allow-external-ledger."""
    try:
        led = (cfg or {}).get("ledger") or {}
        if led.get("adapter", "none") == "none":
            return False
        line = f"event={kind} gen={gen} ts={now_iso()}"
        if extra:
            line += f" {extra}"
        ledger_append(cfg, line)
        return True
    except Exception as e:
        print(f"WARN  event not recorded ({kind} gen={gen}): {e}", file=sys.stderr)
        return False


# ------------------------------------------------- custody hand-off (stow) ----
# v1.2, operator decision on record: an agent using this skill may have no
# storage beyond its own, so everything in this section is opt-in per
# invocation and NOTHING happens by default. There is still no upload code
# here: --stow-to is a local directory copy with a hash roundtrip, and
# --stow-cmd is the OPERATOR'S OWN command, passed on the CLI in the
# operator's own voice, never stored in config (so the planted-config attack
# class the ledger adapter guards against cannot reach it), run as an argv
# vector with shell=False, announced on stderr every process that runs it.

_STOW_CMD_WARNED = False


def warn_stow_cmd(cmd):
    global _STOW_CMD_WARNED
    if _STOW_CMD_WARNED:
        return
    _STOW_CMD_WARNED = True
    preview = " ".join(str(cmd).split())
    if len(preview) > 100:
        preview = preview[:97] + "…"
    print(f"WARN  stow command adapter: piping archive bytes to stdin of "
          f"\"{preview}\" (per-invocation --stow-cmd, not config)", file=sys.stderr)


def run_stow_cmd(cmd, path):
    """Feed the file at `path` to the user's command on stdin. Returns None on
    success or a failure reason string. The command's opinion of success is
    its exit code — this skill cannot verify what the command did with the
    bytes, and says so wherever the result is reported."""
    try:
        argv = shlex.split(str(cmd))
    except ValueError as e:
        return f"stow-cmd is not a valid command line (shlex parse failed): {e}"
    if not argv:
        return "stow-cmd is empty"
    warn_stow_cmd(cmd)
    try:
        with open(path, "rb") as f:
            r = subprocess.run(argv, shell=False, stdin=f, capture_output=True,
                               timeout=STOW_CMD_TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"stow command timed out after {STOW_CMD_TIMEOUT}s"
    except OSError as e:
        return f"stow command could not run: {e}"
    if r.returncode != 0:
        err = (r.stderr or b"").decode("utf-8", "replace").strip()[:200]
        return f"stow command failed (rc={r.returncode}){': ' + err if err else ''}"
    return None


def _stage_copy(src, dst, expect_digest=None, mode=None):
    """Copy `src` to `dst` through an unpredictable O_EXCL staging file in
    dst's directory (the v1.2.1 staging discipline), verify the STAGED bytes
    by re-reading them from the destination medium when `expect_digest` is
    given, and only then os.replace onto the final name.

    Not shutil.copy2(src, dst): that reopens `dst` by pathname, so a symlink
    pre-planted at the predictable archive name (<chain>-g<N>.tar.gz) in an
    operator-chosen directory made the bytes land wherever it pointed — while
    the roundtrip hash, read back through the same link, still reported
    MATCH. os.replace swaps the directory entry itself: a planted link is
    replaced, never followed, and a failed or mismatching copy never exists
    under the final name. Raises OSError on I/O failure and ValueError on a
    hash mismatch; the staging file is always removed."""
    fd, tmp = secure_staging(dst, "stow")
    try:
        set_fd_mode(fd, mode)
        with os.fdopen(fd, "wb") as out, open(src, "rb") as inp:
            shutil.copyfileobj(inp, out, 1 << 20)
            out.flush()
            os.fsync(out.fileno())
        try:  # mtime parity with the copy2 this replaced
            st = os.stat(src)
            os.utime(tmp, ns=(st.st_atime_ns, st.st_mtime_ns))
        except (OSError, NotImplementedError):
            pass
        if expect_digest is not None and sha256_file(tmp) != expect_digest:
            raise ValueError("staged copy hash mismatch")
        os.replace(tmp, dst)
    finally:
        discard_staging(tmp)


def stow_to_dir(path, digest, dest, mode=None):
    """Copy `path` (+ its .sha256 sidecar, if any) into `dest`, re-hashing the
    copy at the destination before it takes its final name — the documented
    off-site roundtrip pattern (upload → fetch back → hash-compare), applied
    to a directory. Returns None on success, reason string on failure. A bad
    or partial copy is never left under the archive's name, so a silent bad
    copy cannot impersonate custody."""
    try:
        os.makedirs(dest, exist_ok=True)
        dst = os.path.join(dest, os.path.basename(path))
        try:
            _stage_copy(path, dst, expect_digest=digest, mode=mode)
        except ValueError:
            return (f"stow roundtrip hash MISMATCH at {dst} — bad copy removed; "
                    "destination medium is not trustworthy for this archive")
        side = path + ".sha256"
        if os.path.exists(side):
            _stage_copy(side, os.path.join(dest, os.path.basename(side)), mode=mode)
    except OSError as e:
        return f"stow copy failed: {e}"
    return None


def stow_archive(cfg, gen, path, digest, stow_to=None, stow_cmd=None,
                 archive_mode=None):
    """Hand a finished artifact to the opt-in destinations. Warn-only by
    doctrine: the artifact already exists and passed its gates, so a stow
    failure is a loud custody gap, never a gate failure. Returns the list of
    human-readable outcome lines."""
    lines = []
    if stow_to:
        dest = os.path.abspath(stow_to)
        why = stow_to_dir(path, digest, dest, mode=archive_mode)
        if why:
            print(f"WARN  {why}", file=sys.stderr)
            lines.append(f"stow:     FAILED ({why.split(' — ')[0]})")
        else:
            lines.append(f"stow:     MATCH ({dest}, hash roundtrip)")
            ledger_event(cfg, "stow", gen,
                         extra=f"file={ledger_field(os.path.basename(path))} sha={digest[:16]}… "
                               f"dest={ledger_field(os.path.basename(dest.rstrip(os.sep)) or dest)}")
    if stow_cmd:
        why = run_stow_cmd(stow_cmd, path)
        if why:
            print(f"WARN  {why} — continuing without side-bucket custody "
                  "(stow is custody-plus, never a gate)", file=sys.stderr)
            lines.append("stow:     FAILED (command refused the bytes)")
        else:
            lines.append("stow:     handed to command (claimed by the command, "
                        "not verified by this skill)")
            ledger_event(cfg, "stow", gen,
                         extra=f"file={ledger_field(os.path.basename(path))} sha={digest[:16]}… dest=cmd")
    return lines


# ----------------------------------------------------- detections (v1.2) ----
# Advisory failsafes born from a dead-weight audit that found a chain
# quietly creeping toward its size ceiling: the weight was visible in
# principle and invisible in practice. These warnings make it visible at
# every build and in status. They read only what was collected this build,
# they never gate, and they never change an exit code — a detector that
# blocks builds teaches users to disable detectors.

def detect_settings(cfg):
    d = dict(DETECT_DEFAULTS)
    d.update({k: v for k, v in (cfg.get("detect") or {}).items()
              if k in DETECT_DEFAULTS})
    return d


def fmt_mb(n):
    return f"{n / (1024 * 1024):.1f} MB"


def detect_block(cfg, files, member_map, gen, out_path):
    """Emit DETECT warnings for this build. stderr only; stdout stays clean
    for the ledger entry and anything that parses build output."""
    s = detect_settings(cfg)
    if not s.get("enabled", True):
        return
    try:
        sizes = {rel: os.path.getsize(ab) for rel, ab in files.items()}
    except OSError:
        sizes = {}
    total = sum(sizes.values())
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:3]
    if top and total:
        parts = [f"{rel} ({fmt_mb(sz)}, {100 * sz // total}%)"
                 for rel, sz in top if sz > 0]
        if parts:
            print("DETECT   largest members: " + " · ".join(parts)
                  + " (advisory, never gates)", file=sys.stderr)
    groups = {}
    for rel, sha in (member_map or {}).items():
        groups.setdefault(sha, []).append(rel)
    dups = sorted((g for g in groups.values() if len(g) > 1),
                  key=len, reverse=True)
    if dups:
        shown = "; ".join(
            ", ".join(g[:3]) + (f" (+{len(g) - 3} more)" if len(g) > 3 else "")
            for g in dups[:3])
        print(f"DETECT   duplicates: identical content under "
              f"{len(dups)} group(s): {shown} (advisory, curation candidates)",
              file=sys.stderr)
    new_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    if new_size > s["archive_mb"] * (1024 * 1024):
        print(f"DETECT   growth: archive {fmt_mb(new_size)} exceeds the "
              f"{s['archive_mb']:g} MB archive bound (advisory, never gates)",
              file=sys.stderr)
    else:
        parent = next((a for a in local_archives(cfg) if a["gen"] == gen - 1),
                      None)
        if parent is not None and new_size > 0:
            psize = os.path.getsize(parent["path"])
            if psize > 0:
                grew_pct = 100.0 * (new_size - psize) / psize
                if (grew_pct >= s["growth_pct"]
                        and (new_size - psize) >= s["growth_mb"] * (1024 * 1024)):
                    print(f"DETECT   growth: gen {gen} archive {fmt_mb(new_size)} "
                          f"vs parent {fmt_mb(psize)} (+{grew_pct:.0f}%) — chain "
                          "weight is creeping; consider curation (advisory, "
                          "never gates)", file=sys.stderr)


# ------------------------------------------------------------ chain scan ----

def read_manifest(tarball):
    """Read + validate the manifest inside a tarball. None if absent."""
    try:
        with tarfile.open(tarball, "r:gz") as tf:
            names = tf.getnames()
            validate_archive_names(names)
            if MANIFEST_NAME not in names:
                return None
            f = tf.extractfile(MANIFEST_NAME)
            if f is None:
                return None
            m = json.loads(f.read().decode("utf-8"))
    except GateError:
        raise
    except Exception as e:
        raise GateError(f"cannot read archive {tarball}: {e}")
    if not isinstance(m, dict) or not isinstance(m.get("generation"), int):
        raise GateError(f"manifest in {tarball} is malformed (no integer generation)")
    return m


def local_archives(cfg):
    out = []
    for fn in archive_names_for(cfg):
        p = os.path.join(output_abs(cfg), fn)
        try:
            m = read_manifest(p)
        except GateError:
            m = None
        out.append({"path": p, "name": fn, "gen": (m or {}).get("generation")})
    return out


def local_max_gen(cfg, exclude_path=None):
    gens = [a["gen"] for a in local_archives(cfg)
            if a["gen"] is not None
            and (exclude_path is None or os.path.abspath(a["path"]) != os.path.abspath(exclude_path))]
    return max(gens, default=0)


def next_generation(cfg):
    ls = ledger_state(cfg)
    base = local_max_gen(cfg)
    if ls["reachable"] and ls["max_gen"] is not None:
        base = max(base, ls["max_gen"])
        src = "ledger" if ls["max_gen"] >= local_max_gen(cfg) else "local chain"
    else:
        src = "local chain (no ledger)"
    return base + 1, src, ls


def resolve_parent(cfg, gen, lstate):
    """Parent sha for gen-1: ledger first, local manifest second, never filenames."""
    if lstate["reachable"]:
        e = ledger_entry_for(lstate, gen - 1)
        if e and e.get("sha256"):
            return e["sha256"], f"ledger gen={gen - 1} entry"
    for a in sorted(local_archives(cfg), key=lambda x: x["gen"] or -1, reverse=True):
        if a["gen"] == gen - 1:
            return sha256_file(a["path"]), f"local archive {a['name']} (embedded manifest)"
    return None, "NO PARENT RESOLVED (chain head broken — line will omit parent)"


# ---------------------------------------------------------------- members ----

def collect_members(cfg):
    """Expand configured members to {rel: abspath} files + dir list.

    Critical members missing on disk are fatal; non-critical missing members
    warn and are skipped (an archive should still be possible).
    """
    files, dirs, missing = {}, [], []
    # Read boundary (audit T05): nested symlinks are dereferenced ONLY when
    # their resolved target stays inside the project root. The root is
    # canonicalized once; containment is checked with commonpath, never with
    # string prefixes (sibling dirs like /ws vs /ws-alt must not pass).
    root_rp = os.path.realpath(cfg["root"])
    for mem in cfg["members"]:
        rel = mem["path"]
        ab = os.path.join(cfg["root"], rel)
        if not os.path.lexists(ab):
            missing.append(rel)
            if mem.get("critical"):
                raise GateError(f"CRITICAL member missing on disk: {rel} — refusing "
                                "to build an incomplete backup")
            continue
        if os.path.isfile(ab) and not os.path.islink(ab):
            if not is_excluded(cfg, rel):
                files[rel] = ab
            continue
        if os.path.islink(ab):
            print(f"WARN  skipping symlink member: {rel}", file=sys.stderr)
            continue
        mem_pats = mem.get("exclude", []) or []
        for dirpath, dirnames, filenames in os.walk(ab):
            dirnames.sort()
            # v1.2: an excluded directory prunes the walk. Before, only the
            # directory ENTRY was dropped and the descent continued, so a
            # single pattern ("node_modules") excluded the entry but not the
            # files under it — the documented two-pattern gotcha. Pruning
            # makes one pattern mean the whole subtree; configs that already
            # listed both forms behave identically (strictly less work).
            kept = []
            for d in dirnames:
                dfull = os.path.join(dirpath, d)
                drel = normalize_member(os.path.relpath(dfull, cfg["root"]))
                if is_excluded(cfg, drel, mem_pats):
                    continue  # pruned: not archived, not walked into
                # Same containment rule as symlinked files just below: os.walk
                # (followlinks=False) never recurses into a symlinked
                # subdirectory either way, so an out-of-root dir-symlink was
                # already contributing no file content — but leaving its NAME
                # as an empty directory placeholder in the archive still
                # contradicts "skipped ... never part of what you selected."
                # Applying the identical realpath+commonpath check here closes
                # that gap; in-root symlinked directories are unaffected.
                if os.path.islink(dfull):
                    rp = os.path.realpath(dfull)
                    try:
                        inside = os.path.commonpath([rp, root_rp]) == root_rp
                    except ValueError:  # different drive (Windows)
                        inside = False
                    if not inside:
                        print(f"WARN  skipping symlinked directory escaping "
                              f"project root: {drel} -> {rp}", file=sys.stderr)
                        continue
                dirs.append(drel)
                kept.append(d)
            dirnames[:] = kept
            for fn in sorted(filenames):
                full = os.path.join(dirpath, fn)
                frel = normalize_member(os.path.relpath(full, cfg["root"]))
                if is_excluded(cfg, frel, mem_pats):
                    continue
                if os.path.islink(full) and not os.path.exists(full):
                    print(f"WARN  skipping broken symlink: {frel}", file=sys.stderr)
                    continue
                # Non-regular files (FIFOs, sockets, devices — including
                # symlinks pointing at them) would hang or crash the hashing
                # step; skip with a warning like any other unrepresentable
                # member. os.path.isfile follows symlinks, so regular files
                # and valid file symlinks (dereferenced at build) pass.
                if not os.path.isfile(full):
                    print(f"WARN  skipping non-regular file: {frel}", file=sys.stderr)
                    continue
                # A nested symlink that resolves outside the project root must
                # not silently pull external bytes into the archive: whatever
                # is backing that link was not part of what the user selected,
                # and an innocuous link name (cache.txt, notes.txt) would carry
                # it past secret_warnings too. Skipped loudly, like any other
                # unrepresentable member. In-root links still dereference.
                if os.path.islink(full):
                    rp = os.path.realpath(full)
                    try:
                        inside = os.path.commonpath([rp, root_rp]) == root_rp
                    except ValueError:  # different drive (Windows)
                        inside = False
                    if not inside:
                        print(f"WARN  skipping symlink escaping project root: "
                              f"{frel} -> {rp}", file=sys.stderr)
                        continue
                files[frel] = full
    return files, dirs, missing


def secret_warnings(files):
    hits = []
    for rel in files:
        base = os.path.basename(rel).lower()
        if any(h in base for h in SECRET_HINTS):
            hits.append(rel)
    return hits


def ledger_line(gen, tarball, parent, member_count, cot_dig=None):
    return (f"gen={gen} sha256={sha256_file(tarball)} "
            f"{f'parent={parent} ' if parent else ''}"
            f"built={now_iso()} file={os.path.basename(tarball)} entries={member_count}"
            f"{f' cot={cot_dig}' if cot_dig else ''}")


# ------------------------------------------------------------------ drill ----

def run_drill(tarball, stage_dir=None):
    """Re-read every manifest member from the archive and verify its sha256.

    This is a READ-BACK, not a restore rehearsal: members are hashed from the
    decoded archive stream and NOTHING is written to disk. It sees a corrupt,
    truncated or incomplete archive; it cannot see a failure of the filesystem
    a real restore would write to (disk full, path limits, permissions) —
    restore itself verifies and reports those per member. (Through 1.2.1 this
    function also rmtree'd and recreated `stage_dir`, a directory it never
    wrote to, and the gate message claimed members were verified "in" it.
    `stage_dir` is accepted and ignored so existing callers keep working.)"""
    m = read_manifest(tarball)
    members = (m or {}).get("members") or {}
    if not members:
        raise GateError(f"{tarball}: manifest carries no member map — drill cannot verify")
    ok = True
    with tarfile.open(tarball, "r:gz") as tf:
        for rel in sorted(members):
            expected = members[rel]
            try:
                f = tf.extractfile(rel)
            except KeyError:
                f = None
            if f is None:
                print(f"FAIL  {rel}: missing from archive")
                ok = False
                continue
            h = hashlib.sha256()
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
            same = h.hexdigest() == expected
            print(f"{'PASS' if same else 'FAIL'}  {rel}: {h.hexdigest()[:16]}…")
            ok = ok and same
    if not ok:
        raise GateError(f"restore drill FAILED — {tarball} is NOT verified recoverable")
    return len(members)


# ------------------------------------------------------------------ build ----

def cmd_build(args, root):
    cfg = load_config(root)
    if not cfg["members"]:
        raise Refused("no members configured — add members before building "
                      "(a chain of empty archives is theatre, not backup)")
    cot = validate_cot(args)  # refuses overflow; never truncates

    # G1: member presence (critical fatal, others warn)
    files, dirs, missing = collect_members(cfg)
    for rel in missing:
        print(f"WARN  non-critical member missing, excluded from build: {rel}",
              file=sys.stderr)
    if not files and not dirs:
        raise GateError("no members resolved on disk — refusing to build an empty archive")

    # G2/G3: generation via fencing (ledger-aware)
    gen, gen_src, lstate = next_generation(cfg)
    parent, parent_src = resolve_parent(cfg, gen, lstate)
    print(f"generation: {gen} (from {gen_src})")
    print(f"parent:     {parent_src}")

    # G4: manifest inside the archive
    manifest = {
        "kind": "backup-chain workspace snapshot",
        "protocol": "backup-chain/1",
        "chain_name": cfg["chain_name"],
        "generation": gen,
        "built_at": now_iso(),
        "parent_sha256": parent,
        "parent_source": parent_src,
        "carries": args.carries or "",
        "member_count": len(files),
        "dir_count": len(dirs),
        "members": {rel: sha256_file(files[rel]) for rel in sorted(files)},
    }
    if cot:
        manifest["cot"] = cot  # decision trace, written at decision time
    if args.output:
        out = args.output
    else:
        # Audit T09 (rounds 4+8): ONE shared realpath containment for the
        # configured output_dir, checked BEFORE makedirs so a refusal leaves
        # nothing behind, not even a directory (see contained_output_dir).
        # --output stays the operator's per-invocation escape hatch and
        # touches no configured path.
        outdir = contained_output_dir(
            cfg, escape="pass --output <path> for this invocation")
        os.makedirs(outdir, exist_ok=True)
        label = args.label or ""
        if label and not re.fullmatch(r"[A-Za-z0-9._-]+", label):
            raise Refused(f"label may only contain [A-Za-z0-9._-]: {label!r}")
        fname = f"{cfg['chain_name']}-g{gen}" + (f"-{label}" if label else "") + ".tar.gz"
        out = os.path.join(outdir, fname)
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # v1.3.0: archive + receipt + stow copies land owner-only (0600) unless
    # widened here, per invocation or per config — resolved BEFORE anything
    # is written, so a bad value refuses the build, rc 2, nothing on disk.
    mode = resolve_archive_mode(getattr(args, "archive_mode", None), cfg)

    # T09 (round 6): staging name is mkstemp-random in the output directory
    # (formerly the predictable out + ".part", a symlink pre-plant target);
    # bytes go through the fd — tarfile receives a fileobj, never a pathname.
    fd, tmp_out = secure_staging(out, "build")
    # dereference=True: nested symlinked files WITHIN the project root are
    # hashed by resolved content (see collect_members / SECURITY.md); the
    # archive must store that same resolved content, not a bare symlink
    # entry, or the manifest hash and the archived bytes would refer to two
    # different things and the G8 restore drill would fail on every such
    # member. Out-of-root links never reach this point (containment gate in
    # collect_members).
    try:
        set_fd_mode(fd, mode)
        with os.fdopen(fd, "wb") as fh, \
                tarfile.open(fileobj=fh, mode="w:gz",
                             format=tarfile.GNU_FORMAT, dereference=True) as tf:
            mb = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8")
            ti = tarfile.TarInfo(MANIFEST_NAME)
            ti.size = len(mb)
            ti.mode = 0o644
            ti.mtime = int(time.time())
            tf.addfile(ti, io.BytesIO(mb))
            for d in sorted(dirs):
                ti = tarfile.TarInfo(d)
                ti.type = tarfile.DIRTYPE
                ti.mode = 0o755
                ti.mtime = int(time.time())
                tf.addfile(ti)
            for rel in sorted(files):
                tf.add(files[rel], arcname=rel, recursive=False)
        os.replace(tmp_out, out)
    finally:
        discard_staging(tmp_out)

    # G5/G6: listing + manifest roundtrip
    with tarfile.open(out, "r:gz") as tf:
        names = tf.getnames()
    validate_archive_names(names)
    if MANIFEST_NAME not in names:
        raise GateError("G5 FAIL: manifest missing from archive listing")
    absent = [rel for rel in manifest["members"] if rel not in set(names)]
    if absent:
        raise GateError(f"G5 FAIL: {len(absent)} members missing from archive "
                        f"(first: {absent[0]})")
    rt = read_manifest(out)
    if rt["generation"] != gen or set(rt.get("members") or {}) != set(manifest["members"]):
        raise GateError("G6 FAIL: manifest roundtrip mismatch")
    print(f"G5/G6    listing + manifest roundtrip: OK ({len(names)} entries)")

    # G7: sha256 receipt
    digest = sha256_file(out)
    atomic_write(out + ".sha256", f"{digest}  {os.path.basename(out)}\n", mode=mode)
    print(f"G7       receipt: {digest[:16]}…  ({os.path.basename(out)}.sha256)  "
          f"mode {mode:04o} (--archive-mode to widen)")

    # G8: restore drill
    n = run_drill(out)
    print(f"G8       restore drill: PASS ({n} members re-read from the archive "
          "and hash-verified; nothing written to disk)")

    atomic_write(os.path.join(vault_dir(cfg["root"]), LAST_BUILD),
                 json.dumps({"generation": gen, "sha256": digest, "path": out,
                             "built_at": manifest["built_at"], "carries": manifest["carries"],
                             "cot": cot, "members": n, "drill": "PASS", "gates": "G1-G8"},
                            indent=2, sort_keys=True) + "\n")

    for rel in secret_warnings(files):
        print(f"SECRET-WARN member looks credential-like: {rel} — archive "
              "distribution is your responsibility (see references/SECURITY.md)",
              file=sys.stderr)
    for hint in cot_secret_scan(cot):
        print(f"SECRET-WARN decision trace mentions {hint!r} — traces are "
              "hashed into manifests and digested into ledgers; keep secrets "
              "out of the trace (see references/SECURITY.md)", file=sys.stderr)

    # v1.2 detections (advisory failsafes) — never gate, never change rc.
    detect_block(cfg, files, manifest["members"], gen, out)

    # v1.2 custody hand-off (opt-in, warn-only) — silence when not requested:
    # an option must not advertise itself on every run.
    if getattr(args, "stow_to", None) or getattr(args, "stow_cmd", None):
        for ln in stow_archive(cfg, gen, out, digest,
                               stow_to=getattr(args, "stow_to", None),
                               stow_cmd=getattr(args, "stow_cmd", None),
                               archive_mode=mode):
            print(ln)

    line = ledger_line(gen, out, parent, len(files),
                       cot_digest(cot) if cot else None)
    print("\n--- LEDGER ENTRY ---")
    print(line)
    if args.register:
        where = ledger_append(cfg, line)
        print(f"registered: {where}")
    else:
        print("(not registered — pass --register or append manually)")
    print(f"\nOK: gen {gen} built and verified recoverable: {out}")
    return 0


# ----------------------------------------------------------------- verify ----

def cmd_verify(args, root):
    cfg = load_config(root)
    tb = os.path.abspath(args.tarball)
    if not os.path.exists(tb):
        raise GateError(f"no such archive: {tb}")
    digest = sha256_file(tb)
    fail = False
    print(f"archive: {os.path.basename(tb)}  sha256={digest[:16]}…")

    rcpt = tb + ".sha256"
    if os.path.exists(rcpt):
        with open(rcpt) as f:
            want = f.read().split()[0]
        same = want == digest
        print(f"receipt: {'MATCH' if same else 'MISMATCH'} ({os.path.basename(rcpt)})")
        fail = fail or not same
    else:
        print("receipt: UNKNOWN (no .sha256 sidecar)")

    m = read_manifest(tb)
    if m is None:
        print("manifest: ABSENT (unversioned archive — legacy or foreign)")
    else:
        print(f"manifest: gen={m['generation']} parent="
              f"{(m.get('parent_sha256') or 'none')[:16]}… members={m.get('member_count')}")
        cot = m.get("cot")
        if cot:
            print(f"trace:   {cot_canonical(cot)}")
        else:
            print("trace:   none recorded (pre-v1.1 generation)")

    ls = ledger_state(cfg)
    print(f"ledger:  {ls['note']}")
    if ls["reachable"] and m is not None:
        e = ledger_entry_for(ls, m["generation"])
        if e is None:
            print(f"ledger:  UNKNOWN (gen {m['generation']} not registered)")
        elif e.get("sha256") is None:
            print("ledger:  UNKNOWN (entry carries no sha256)")
        else:
            same = e["sha256"] == digest
            print(f"ledger:  {'MATCH' if same else 'MISMATCH'} "
                  f"(gen {m['generation']} entry)")
            fail = fail or not same
        # --- witness layer (v1.1): agreement between the two trace copies is
        # evidence; disagreement is an ALARM, not a gate. Refusing here would
        # teach users to fix the alarm instead of investigating it.
        cot = m.get("cot")
        if e is not None and e.get("cot"):
            can_norm = re.sub(r"\s+", "_", cot_canonical(cot)) if cot else ""
            if can_norm.startswith(e["cot"]):
                print("trace:   ledger digest MATCH")
            else:
                print("trace:   ledger digest MISMATCH — manifest trace and "
                      "ledger digest disagree (witness disagreement is an "
                      "alarm; investigate, do not explain away)")
                print("WARN  trace digest mismatch between archive manifest and "
                      "ledger entry — one of them was rewritten", file=sys.stderr)
        acks = [a for a in (ls.get("acks") or []) if a.get("gen") == m["generation"]]
        if acks:
            for a in acks[-3:]:
                print(f"witness:  op=ack ts={a.get('ts', '')}"
                      f"{f' note={a["note"]}' if a.get('note') else ''}")
        elif acks_disabled(cfg):
            print(f"witness:  acks disabled by recorded decision "
                  f"({ack_policy_desc(cfg.get('ack_policy'))}) — absence is "
                  "policy, not neglect")
        else:
            print("witness:  no operator ack on record for this generation")
    elif not ls["reachable"]:
        print("ledger:  SKIPPED (unreachable) — verification is INCOMPLETE, marked")
    if fail:
        raise GateError("verification FAILED — do not trust this archive")
    print("verify: OK (see per-source lines above)")
    return 0


# ------------------------------------------------------------ fencing gates ----

def fencing_check(cfg, tb, lstate=None):
    """The pre-restore gate. Returns the decision dict; never raises for
    decision outcomes (only for unreadable archives).

    lstate may be passed in by a caller that already has a fresh ledger_state
    (e.g. cmd_restore), so a 'command' ledger adapter's read command is not
    invoked twice per restore."""
    try:
        m = read_manifest(tb)
    except GateError:
        raise
    agen = m.get("generation") if m else None
    if lstate is None:
        lstate = ledger_state(cfg) if cfg else {
            "reachable": False, "max_gen": None, "entries": [],
            "note": "no config available (vault absent?) — fencing degraded to local heuristic"}
    lmax = lstate["max_gen"]
    local_head = local_max_gen(cfg) if cfg else 0

    if agen is None:
        if lstate["reachable"]:
            return {"decision": "refuse", "archive_gen": None, "ledger_gen": lmax,
                    "reason": "unversioned archive (no manifest) while the ledger is live "
                              "— provenance unknown"}
        return {"decision": "restore", "archive_gen": None, "ledger_gen": lmax,
                "marked": True,
                "reason": "unversioned archive and no live ledger — mtime heuristic, "
                          "marked (last of the old protocol)"}
    if not lstate["reachable"]:
        if local_head and agen < local_head:
            return {"decision": "refuse", "archive_gen": agen, "ledger_gen": None,
                    "local_head": local_head,
                    "reason": f"stale vs local chain: archive gen {agen} < local head "
                              f"{local_head}; ledger unavailable so this refusal is "
                              "assertable locally"}
        return {"decision": "skip", "archive_gen": agen, "ledger_gen": None,
                "marked": True, "reason": f"ledger unreachable ({lstate['note']}) — "
                f"fencing SKIPPED (marked); archive gen {agen} vs local head {local_head}"}
    if lmax and agen < lmax:
        return {"decision": "refuse", "archive_gen": agen, "ledger_gen": lmax,
                "reason": f"stale handoff: archive gen {agen} < ledger head {lmax}; "
                          "a newer backup existed — heroic retry refused"}
    if agen < local_head:
        return {"decision": "refuse", "archive_gen": agen, "ledger_gen": lmax,
                "local_head": local_head,
                "reason": f"stale vs local chain: archive gen {agen} < local head "
                          f"{local_head} — a newer archive exists locally; refusing "
                          "regardless of ledger state"}
    note = ""
    if lmax and agen > lmax:
        note = " (archive is AHEAD of ledger head — unregistered build?)"
    return {"decision": "restore", "archive_gen": agen, "ledger_gen": lmax,
            "reason": "archive generation is current (>= ledger head)" + note}


def cmd_check(args, root):
    cfg = load_config(root) if os.path.exists(config_path(root)) else None
    tb = os.path.abspath(args.tarball)
    if not os.path.exists(tb):
        raise GateError(f"no such archive: {tb}")
    lstate = ledger_state(cfg) if cfg else None
    d = fencing_check(cfg, tb, lstate)
    print(json.dumps(d, indent=2))
    return 0 if d["decision"] != "refuse" else 2


def cmd_recheck(args, root):
    cfg = load_config(root) if os.path.exists(config_path(root)) else None
    try:
        gen = int(args.gen)
    except ValueError:
        raise Refused(f"GEN must be an integer, got: {args.gen!r}")
    lstate = ledger_state(cfg) if cfg else {"reachable": False, "max_gen": None,
                                            "entries": [], "note": "no config"}
    local_head = local_max_gen(cfg) if cfg else 0
    if lstate["reachable"]:
        if lstate["max_gen"] and gen < lstate["max_gen"]:
            d = {"decision": "stale", "restored_gen": gen, "ledger_gen": lstate["max_gen"],
                 "reason": f"CLEAN-COMPLETING STALE RESTORE: workspace restored to gen "
                           f"{gen} but the ledger remembers {lstate['max_gen']} — bytes "
                           "landed, precondition did not hold"}
        else:
            d = {"decision": "ok", "restored_gen": gen, "ledger_gen": lstate["max_gen"],
                 "reason": "precondition held after apply"}
    else:
        if local_head and gen < local_head:
            d = {"decision": "stale", "restored_gen": gen, "ledger_gen": None,
                 "local_head": local_head,
                 "reason": f"stale vs local chain ({gen} < {local_head})"}
        else:
            d = {"decision": "ok", "restored_gen": gen, "ledger_gen": None,
                 "marked": True,
                 "reason": f"no live ledger ({lstate['note']}) — local-chain check only"}
    print(json.dumps(d, indent=2))
    return 0 if d["decision"] == "ok" else 1


# ----------------------------------------------------------------- restore ----

def cmd_restore(args, root):
    cfg = load_config(root) if os.path.exists(config_path(root)) else None
    tb = os.path.abspath(args.tarball)
    if not os.path.exists(tb):
        raise GateError(f"no such archive: {tb}")
    target = os.path.abspath(args.target)
    if target in ("/", os.path.expanduser("~"), os.path.expanduser("~/")):
        raise Refused(f"refusing dangerous restore target: {target}")
    m = read_manifest(tb)
    members = (m or {}).get("members") or {}
    if not members:
        raise GateError(f"{tb}: no member map in manifest — nothing verifiable to restore")

    # --- fencing gate (skip = loud; refuse = honored unless --force)
    # ledger_state is fetched once here and reused below for the authenticity
    # check, so a 'command' ledger adapter's read command runs only once per
    # restore instead of twice.
    ls = ledger_state(cfg) if cfg else None
    d = fencing_check(cfg, tb, ls)
    print(json.dumps(d, indent=2))
    if d["decision"] == "refuse" and not args.force:
        raise Refused("fencing refused this restore — pass --force only if you have "
                      "independently established that refusing is wrong")
    if d["decision"] == "skip":
        print("!! FENCING SKIPPED (unverified precondition) — proceeding, loudly marked !!",
              file=sys.stderr)
    if d["decision"] == "refuse" and args.force:
        print("!! FENCING OVERRIDE — gate said refuse, proceeding on explicit --force !!",
              file=sys.stderr)

    # --- archive authenticity vs ledger (when the ledger knows this gen)
    if cfg and m is not None and ls is not None:
        e = ledger_entry_for(ls, m["generation"]) if ls["reachable"] else None
        if e and e.get("sha256"):
            same = e["sha256"] == sha256_file(tb)
            print(f"ledger authenticity: {'MATCH' if same else 'MISMATCH'}")
            if not same and not args.force:
                raise Refused("archive sha256 does not match its ledger entry — "
                              "do not restore unauthenticated bytes")

    # --- witness narrative (v1.1): the 3 a.m. operator reads why before
    # healing with it. Context, never a gate — a stale trace is a thing to
    # know, not a thing that blocks a heal.
    if m is not None:
        cot = m.get("cot")
        if cot:
            print(f"trace:    built as: t={cot.get('t')} b={cot.get('b')}")
            if cot.get("r"):
                print(f"trace:    risk consciously accepted: {cot['r']}")
            if cot.get("f"):
                print(f"trace:    falsifier: {cot['f']}")
        else:
            print("trace:    none recorded for this generation (pre-v1.1 archive)")
        if ls is not None and ls.get("reachable"):
            acks = [a for a in (ls.get("acks") or [])
                    if a.get("gen") == m.get("generation")]
            if acks:
                for a in acks[-3:]:
                    print(f"witness:   op=ack ts={a.get('ts', '')}"
                          f"{f' note={a["note"]}' if a.get('note') else ''}")
            else:
                print("witness:   no operator ack on record for this generation")

    # --- target boundary (audit T09): a pre-existing symlinked directory
    # component beneath --target would redirect restore writes outside the
    # selected target (open/os.replace follow directory symlinks). Member
    # name validation cannot see this — the names are clean, the FILESYSTEM
    # is not. Refused unconditionally, like the dangerous-target gate above:
    # --force is a fencing override, not a target-safety override. The fix is
    # manual and deliberate: remove or replace the symlink, or pick another
    # target. The target path itself may be a symlink — the user chose it.
    def _link_component(tpath):
        top = os.path.abspath(target)
        cur = os.path.dirname(os.path.abspath(tpath))
        while cur.startswith(top + os.sep):
            if os.path.islink(cur):
                return cur
            cur = os.path.dirname(cur)
        return None

    checked, escapes = {}, []
    for rel in sorted(members):
        dest = os.path.join(target, rel)
        parent = os.path.dirname(dest)
        if parent not in checked:
            # _link_component examines every component BELOW target and above
            # the final one — i.e. exactly the directories that would carry
            # the write. Passing the parent itself would skip it (dirname
            # strips it first), which is why this takes dest, not parent.
            checked[parent] = _link_component(dest)
        if checked[parent] and checked[parent] not in escapes:
            escapes.append(checked[parent])
    if escapes:
        if args.dry_run:
            for e in escapes[:5]:
                print(f"  WOULD REFUSE: symlinked path component beneath target: {e}")
            print("dry-run: no changes made")
            return 0
        raise Refused(
            f"refusing restore: {len(escapes)} symlinked path component(s) "
            f"beneath --target would redirect writes outside it "
            f"(first: {escapes[0]}) — remove or replace the symlink(s), "
            "or choose another target")

    # --- plan
    restore, already, conflicts = [], [], []
    for rel in sorted(members):
        tpath = os.path.join(target, rel)
        if os.path.islink(tpath):
            # An existing symlink at the final component counts as differing
            # no matter what it currently points at: restore never follows it
            # and never silently replaces it. With --overwrite, os.replace
            # swaps the link itself, not the link target.
            conflicts.append(rel)
        elif os.path.exists(tpath):
            cur = sha256_file(tpath)
            if cur == members[rel]:
                already.append(rel)
            else:
                conflicts.append(rel)
        else:
            restore.append(rel)
    print(f"plan: restore={len(restore)} already-current={len(already)} "
          f"conflicts={len(conflicts)}")
    if args.dry_run:
        # A dry run previews the plan, including conflicts that would need
        # --overwrite for a real restore — it must never itself require
        # --overwrite, or there is no way to preview conflicts before opting in.
        for rel in restore[:20]:
            print(f"  would restore: {rel}")
        if len(restore) > 20:
            print(f"  … and {len(restore) - 20} more")
        for rel in conflicts[:20]:
            print(f"  would need --overwrite (differs locally): {rel}")
        if len(conflicts) > 20:
            print(f"  … and {len(conflicts) - 20} more conflicts")
        print("dry-run: no changes made")
        return 0
    if conflicts and not args.overwrite:
        raise Refused(f"{len(conflicts)} existing files differ from the archive "
                      f"(first: {conflicts[0]}) — pass --overwrite to replace them")
    if conflicts and args.overwrite:
        restore = sorted(set(restore) | set(conflicts))

    # --- per-member, verified (NEVER bulk extraction)
    ok = failed = 0
    with tarfile.open(tb, "r:gz") as tf:
        for rel in restore:
            tpath = os.path.join(target, rel)
            os.makedirs(os.path.dirname(tpath) or target, exist_ok=True)
            try:
                f = tf.extractfile(rel)
            except KeyError:
                f = None
            if f is None:
                print(f"FAIL  {rel}: missing from archive")
                failed += 1
                continue
            fd, tmp = secure_staging(tpath, "restore")
            h = hashlib.sha256()
            try:
                with os.fdopen(fd, "wb") as w:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        h.update(chunk)
                        w.write(chunk)
                    w.flush()
                    os.fsync(w.fileno())
                if h.hexdigest() != members[rel]:
                    print(f"FAIL  {rel}: sha256 mismatch after extraction")
                    failed += 1
                    continue
                os.replace(tmp, tpath)
            finally:
                discard_staging(tmp)
            ok += 1
    for rel in already:
        print(f"SKIP  {rel}: already current")
    if conflicts:
        print(f"OVERWRITE: {len(conflicts)} conflicting files replaced")
    print(f"restored: {ok} verified · {failed} failed · {len(already)} already-current")
    if failed:
        raise GateError(f"restore INCOMPLETE: {failed} members failed verification — "
                        "workspace is NOT fully healed; investigate before proceeding")

    gen = m["generation"] if m else None
    if gen is not None:
        if cfg is not None and ledger_event(
                cfg, "restore", gen,
                extra=f"target={ledger_field(os.path.basename(os.path.normpath(target)))}"):
            print("event:    restore recorded in ledger")
        rc = cmd_recheck(argparse.Namespace(gen=str(gen)), root)
        return rc
    print("recheck: SKIPPED (unversioned archive)")
    return 0


def cmd_drill(args, root):
    """Standalone drill + witness event. (The build-time G8 drill does not
    append an event: the build's own ledger line and last_build receipt are
    already witnesses of it, and a second line would be ceremony.)"""
    tb = os.path.abspath(args.tarball)
    m = read_manifest(tb)
    gen = m.get("generation") if m else None
    n = run_drill(tb)
    cfg = load_config(root)
    if gen is not None and ledger_event(cfg, "drill", gen):
        print(f"event:    drill recorded in ledger (gen {gen})")
    return 0


# ------------------------------------------------------------------ status ----

def cmd_status(args, root):
    cfg = load_config(root)
    print(f"chain:    {cfg['chain_name']}  (root: {cfg['root']})")
    print(f"output:   {output_abs(cfg)}")
    ls = ledger_state(cfg)
    print(f"ledger:   {ls['note']}"
          + (f"  head={ls['max_gen']}" if ls["reachable"] and ls["max_gen"] else ""))
    if acks_disabled(cfg):
        print(f"ack policy: DISABLED by recorded decision "
              f"({ack_policy_desc(cfg.get('ack_policy'))}) — new acks refuse")
    acks = ls.get("acks") or []
    if acks:
        print(f"acks:     {len(acks)} operator acknowledgment(s) on record")
        for a in acks[-5:]:
            print(f"  op=ack gen={a['gen']} ts={a.get('ts', '')}"
                  f"{f' note={a["note"]}' if a.get('note') else ''}")
    ops = ls.get("ops") or []
    if ops:
        print(f"ops:      {len(ops)} custody op(s) on record")
        for o in ops[-3:]:
            rest = f" {o['rest']}" if o["rest"] else ""
            print(f"  event={o['op']} gen={o['gen']} ts={o['ts']}{rest}")
    print(f"members:  {len(cfg['members'])} configured")
    for mem in cfg["members"]:
        exists = os.path.exists(os.path.join(cfg["root"], mem["path"]))
        print(f"  {'x' if not exists else ' '} {'[critical]' if mem.get('critical') else '          '} {mem['path']}")
    files, _, _ = collect_members(cfg)
    for rel in secret_warnings(files):
        print(f"  SECRET-WARN {rel}")
    # v1.2: raw weight on the record — the audit found the weight visible in
    # principle and invisible in practice; status makes it visible.
    try:
        total = sum(os.path.getsize(ab) for ab in files.values())
        print(f"sizes:    {len(files)} member file(s), {fmt_mb(total)} raw")
    except OSError:
        pass
    archs = local_archives(cfg)
    if archs:
        print("local chain (embedded manifest gens; filename is a label):")
        for a in sorted(archs, key=lambda x: x["gen"] if x["gen"] is not None else -1):
            print(f"  gen={a['gen'] if a['gen'] is not None else '??':>4}  {a['name']}")
        head = max((a["gen"] for a in archs if a["gen"] is not None), default=None)
        print(f"local head: gen {head}")
        try:
            atot = sum(os.path.getsize(a["path"]) for a in archs)
            print(f"archives: {len(archs)} local, {fmt_mb(atot)} total")
        except OSError:
            pass
    else:
        print("local chain: empty")
    lb = os.path.join(vault_dir(root), LAST_BUILD)
    if os.path.exists(lb):
        with open(lb) as f:
            b = json.load(f)
        print(f"last build: gen {b.get('generation')} drill={b.get('drill')} "
              f"members={b.get('members')} carries={b.get('carries', '')[:60]}")
        cot = b.get("cot")
        if cot:
            print(f"  trace: {cot_canonical(cot)}")
    return 0


# ------------------------------------------------------------- init/members ----

def cmd_init(args, root):
    if os.path.exists(config_path(root)) and not args.force:
        raise Refused(f"config already exists at {config_path(root)} — "
                      "pass --force to overwrite deliberately")
    cfg = default_config(root, args.name, args.output_dir, args.ledger,
                         args.ledger_file, args.read_cmd, args.append_cmd)
    os.makedirs(vault_dir(root), exist_ok=True)
    if (cfg["ledger"]["adapter"] == "file"):
        lp = cfg["ledger"]["file"]
        if not os.path.isabs(lp):
            lp = os.path.join(root, lp)
        os.makedirs(os.path.dirname(lp), exist_ok=True)
        if not os.path.exists(lp):
            atomic_write(lp, "")
    save_config(root, cfg)
    print(f"initialized chain '{cfg['chain_name']}' at {root}")
    print(f"ledger:   {cfg['ledger']['adapter']}"
          + (f" ({cfg['ledger'].get('file')})" if cfg["ledger"]["adapter"] == "file" else ""))
    if cfg["ledger"]["adapter"] == "file":
        print("NOTE: a file ledger inside the workspace is NOT wipe-safe — for real "
              "protection use --ledger-file pointing outside this machine, or a "
              "command adapter over any append-only channel you have.")
    print("next:")
    print("  member add <path> [--critical]   # repeat for everything whose loss hurts")
    print("  build --carries \"what this generation holds\" --register")
    return 0


def cmd_member(args, root):
    cfg = load_config(root)
    if args.action == "list":
        for mem in cfg["members"]:
            extra = ""
            if mem.get("exclude"):
                extra = "  [excl: " + " ".join(mem["exclude"]) + "]"
            print(f"{'[critical] ' if mem.get('critical') else '           '}{mem['path']}{extra}")
        return 0
    if not args.path:
        raise Refused(f"'member {args.action}' needs a PATH argument")
    rel = normalize_member(args.path)
    if args.action == "add":
        if not os.path.exists(os.path.join(root, rel)):
            raise GateError(f"path does not exist (add members that exist so --critical "
                            f"means something): {rel}")
        for mem in cfg["members"]:
            if mem["path"] == rel:
                print(f"already a member: {rel}")
                return 0
        pats = list(getattr(args, "exclude", None) or [])
        for p in pats:
            if not isinstance(p, str) or not p.strip() or "\x00" in p:
                raise Refused(f"exclude pattern must be a non-empty string: {p!r}")
        entry = {"path": rel, "critical": bool(args.critical)}
        if pats:
            entry["exclude"] = pats  # opt-in curation; absent = old behavior
        cfg["members"].append(entry)
        cfg["members"].sort(key=lambda m: m["path"])
        print(f"member added: {rel}" + ("  [critical]" if args.critical else "")
              + (f"  [excl: {' '.join(pats)}]" if pats else ""))
    elif args.action == "remove":
        before = len(cfg["members"])
        cfg["members"] = [m for m in cfg["members"] if m["path"] != rel]
        if len(cfg["members"]) == before:
            print(f"not a member: {rel}")
            return 0
        print(f"member removed: {rel}")
    save_config(root, cfg)
    return 0


def cmd_evict(args, root):
    """Custody-preserving member removal (v1.2, opt-in).

    The dead-weight lesson generalized: removing a chain member should be a
    RECORDED act with custody, not a silent config edit. The member's
    current content is packaged (with a per-member hash map), the package is
    handed to the operator's chosen destination (--stow-to DIR with a hash
    roundtrip, or --stow-cmd CMD fed on stdin), and only then is the member
    untracked. A witness line (`event=evict`) records the act. Without a
    stow destination the eviction is refused — silent custody loss is what
    this command exists to prevent ('member remove' remains the deliberate
    silent drop). Files on disk are never touched: eviction stops TRACKING
    content, it does not delete it."""
    cfg = load_config(root)
    rel = normalize_member(args.path)
    mem = next((m for m in cfg["members"] if m["path"] == rel), None)
    if mem is None:
        raise Refused(f"not a member: {rel} — evict removes a chain member "
                      "with custody; use 'member remove' for silent removal")
    stow_to = getattr(args, "stow_to", None)
    stow_cmd = getattr(args, "stow_cmd", None)
    if not stow_to and not stow_cmd:
        raise Refused("evict refuses to drop custody silently — pass "
                      "--stow-to DIR or --stow-cmd CMD so the content lands "
                      "somewhere before tracking stops (or use 'member "
                      "remove' for a deliberate silent drop)")
    note = getattr(args, "note", None) or ""
    if has_line_break(note):
        raise Refused("evict note must be a single line")
    if len(note) > EVICT_NOTE_CAP:
        raise Refused(f"evict note exceeds {EVICT_NOTE_CAP} chars ({len(note)})")
    nxt, _src, _ls = next_generation(cfg)
    head = max(nxt - 1, 0)
    # Collect the member's current content, honoring its own excludes.
    # critical is deliberately dropped: a vanished evictee is recorded as
    # absence, not refused — the package manifest IS the record.
    sub = dict(cfg)
    m2 = {k: v for k, v in mem.items() if k != "critical"}
    sub["members"] = [m2]
    files, dirs, _missing = collect_members(sub)
    # The package lives in the output dir: the built-in *.tar.gz
    # self-exclusion keeps it out of future member collection, and the name
    # never matches the <chain>-g<GEN> build prefix. Audit T09 (round 8):
    # evict had inherited the pre-round-4 pattern and would write the
    # eviction package and its receipt through a symlinked output_dir
    # component; the SAME shared realpath containment build uses now guards
    # this write too, checked BEFORE makedirs (a refusal leaves nothing
    # behind, not even a directory). Custody escapes stay a per-invocation
    # CLI act: --stow-to/--stow-cmd.
    outdir = contained_output_dir(
        cfg, escape="hand custody off with --stow-to DIR or --stow-cmd CMD "
                    "for this invocation")
    os.makedirs(outdir, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    base = safe_name_component(os.path.basename(rel.rstrip("/\\")) or rel.replace("/", "_"))
    out = os.path.abspath(os.path.join(
        outdir, f"{cfg['chain_name']}-evict-g{head}-{ts}-{base}.tar.gz"))
    manifest = {
        "kind": "backup-chain eviction package",
        "protocol": "backup-chain/1",
        "chain_name": cfg["chain_name"],
        "evicted_path": rel,
        "evicted_at": now_iso(),
        "chain_head_at_eviction": head,
        "was_critical": bool(mem.get("critical")),
        "excludes": list(mem.get("exclude", []) or []),
        "note": note,
        "member_count": len(files),
        "members": {r: sha256_file(files[r]) for r in sorted(files)},
    }
    # v1.3.0: same mode resolution as build — resolved before anything is
    # written; a bad value refuses the eviction, rc 2, member stays tracked.
    mode = resolve_archive_mode(getattr(args, "archive_mode", None), cfg)
    # T09 (round 6): same staging discipline as the build archive.
    fd, tmp_out = secure_staging(out, "evict")
    try:
        set_fd_mode(fd, mode)
        with os.fdopen(fd, "wb") as fh, \
                tarfile.open(fileobj=fh, mode="w:gz",
                             format=tarfile.GNU_FORMAT, dereference=True) as tf:
            mb = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8")
            ti = tarfile.TarInfo(EVICT_MANIFEST_NAME)
            ti.size = len(mb)
            ti.mode = 0o644
            ti.mtime = int(time.time())
            tf.addfile(ti, io.BytesIO(mb))
            for d in sorted(dirs):
                ti = tarfile.TarInfo(d)
                ti.type = tarfile.DIRTYPE
                ti.mode = 0o755
                ti.mtime = int(time.time())
                tf.addfile(ti)
            for r in sorted(files):
                tf.add(files[r], arcname=r, recursive=False)
        os.replace(tmp_out, out)
    finally:
        discard_staging(tmp_out)
    with tarfile.open(out, "r:gz") as tf:
        names = tf.getnames()
    validate_archive_names(names)
    digest = sha256_file(out)
    atomic_write(out + ".sha256", f"{digest}  {os.path.basename(out)}\n", mode=mode)
    for r in secret_warnings(files):
        print(f"SECRET-WARN evicted content looks credential-like: {r} — the "
              "package inherits every archive rule (see references/SECURITY.md)",
              file=sys.stderr)
    # Custody hand-off — this MUST succeed or the member stays tracked.
    if stow_to:
        dest = os.path.abspath(stow_to)
        why = stow_to_dir(out, digest, dest, mode=mode)
        if why:
            raise GateError(f"custody hand-off failed ({why}) — member NOT "
                            f"evicted; the package is at {out}")
    if stow_cmd:
        why = run_stow_cmd(stow_cmd, out)
        if why:
            raise GateError(f"custody hand-off failed ({why}) — member NOT "
                            f"evicted; the package is at {out}")
    # Custody established: untrack + record (witness, best-effort by the
    # same doctrine as every event line — the package manifest is the
    # durable record even if the ledger hiccuped).
    cfg["members"] = [m for m in cfg["members"] if m["path"] != rel]
    save_config(root, cfg)
    extra = (f"path={ledger_field(rel)} "
             f"file={ledger_field(os.path.basename(out))} sha={digest[:16]}…")
    if note:
        extra += f" note={note}"
    if ledger_event(cfg, "evict", head, extra=extra):
        print("event:    evict recorded in ledger")
    else:
        print("NOTE  event not recorded (ledger unavailable) — the eviction "
              "package manifest is the durable record", file=sys.stderr)
    print(f"OK: {rel} evicted with custody — {len(files)} file(s) packaged, "
          f"member untracked; package: {out}")
    print("witness, not gate: future builds will not include this path; "
          "files on disk were not touched")
    return 0


def cmd_next_gen(args, root):
    cfg = load_config(root)
    gen, src, _ = next_generation(cfg)
    print(f"{gen}  # from {src}")
    return 0


def cmd_ledger_line(args, root):
    cfg = load_config(root)
    tb = os.path.abspath(args.tarball)
    m = read_manifest(tb)
    gen = m.get("generation") if m else None
    if gen is None:
        raise GateError("archive has no manifest — cannot compose a ledger line")
    parent, psrc = resolve_parent(cfg, gen, ledger_state(cfg))
    if m.get("parent_sha256") and not parent:
        parent = m["parent_sha256"]
        psrc = "archive manifest (fallback)"
    if m.get("parent_sha256") and parent and parent != m["parent_sha256"]:
        print(f"WARN  resolved parent differs from manifest parent "
              f"({parent[:12]}… vs {m['parent_sha256'][:12]}…)", file=sys.stderr)
    cot = m.get("cot")
    line = ledger_line(gen, tb, parent, len(m.get("members") or {}),
                       cot_digest(cot) if cot else None)
    print(line)
    print(f"parent source: {psrc}")
    if args.append:
        where = ledger_append(cfg, line)
        print(f"appended: {where}")
    return 0


def cmd_ack(args, root):
    """Operator acknowledgment — the human witness. Written when the operator
    actually looks, never on a schedule; attests the looking, not the
    believing. A witness, not a gate: nothing is refused for lack of an ack."""
    cfg = load_config(root)
    try:
        gen = int(args.gen)
    except ValueError:
        raise Refused(f"GEN must be an integer, got: {args.gen!r}")
    if gen <= 0:
        raise Refused(f"GEN must be a positive integer, got: {gen}")
    note = args.note or ""
    if has_line_break(note):
        raise Refused("ack note must be a single line")
    if len(note) > ACK_NOTE_CAP:
        raise Refused(f"ack note exceeds {ACK_NOTE_CAP} chars ({len(note)}) — "
                      "witnesses stay small")
    if acks_disabled(cfg):
        raise Refused(
            "acks are disabled by recorded decision ("
            + ack_policy_desc(cfg.get("ack_policy"))
            + ") — a no-ack chain is a policy on record, not a silence to "
            "fill; if you actually looked and want to ack, re-enable first: "
            "`ack-policy on` (itself witnessed as event=ack-on)")
    if (cfg.get("ledger") or {}).get("adapter", "none") == "none":
        raise Refused("no ledger configured — an ack needs a witness layer to "
                      "live in (adapter 'none' has none)")
    ls = ledger_state(cfg)
    if not ls["reachable"]:
        raise GateError(f"ledger unreachable — cannot ack what cannot be seen "
                        f"({ls['note']})")
    known = ledger_entry_for(ls, gen) is not None or any(
        a.get("gen") == gen for a in local_archives(cfg))
    if not known:
        raise Refused(f"gen {gen} is unknown to the ledger and the local chain — "
                      "an ack witnesses something; there is nothing here to witness")
    line = f"op=ack gen={gen} ts={now_iso()}" + (f" note={note}" if note else "")
    where = ledger_append(cfg, line)
    print(line)
    print(f"acknowledged: gen {gen} ({where})")
    print("witness, not gate: future commands do not require this ack")
    return 0


def cmd_ack_policy(args, root):
    """Show or change the ack policy — and witness every change.

    Acks are witnesses, not gates, so disabling them is a legitimate choice
    (a chat-only deployment whose human cannot run a shell, for one). What it
    may never be is traceless: a chain with no acks on record must say WHY in
    the same ledger an ack would live in, or 'disabled by decision' and
    'nobody watching' are indistinguishable to every later reader, and
    verify's empty-witness note reads as perpetual debt. So both the off and
    on acts append event=ack-off / event=ack-on through the SAME adapter path
    and consent boundaries as acks themselves (a command adapter still needs
    --allow-cmd-ledger, an external file ledger still needs
    --allow-external-ledger), and both REFUSE when the ledger is unreachable
    or nonexistent — an un-witnessable policy change is refused, not made.
    The config key is operational state only; the ledger line is the record."""
    cfg = load_config(root)
    action = args.action  # None (show) | "off" | "on"
    pol = cfg.get("ack_policy")
    off_now = acks_disabled(cfg)
    if action is None:
        if off_now:
            print(f"acks:     DISABLED by recorded decision "
                  f"({ack_policy_desc(pol)})")
            print("  effect: `ack GEN` refuses; verify/status attribute the "
                  "absence to this policy, not to neglect")
            print("  undo:   `ack-policy on` (appends event=ack-on)")
        else:
            print("acks:     enabled (default) — `ack GEN` writes op=ack when "
                  "a human actually looks")
            print("  policy: `ack-policy off [--note WHY]` disables, witnessed "
                  "as event=ack-off; refuses without a reachable ledger, "
                  "because an un-witnessed policy is exactly the traceless "
                  "act this command exists to prevent")
        return 0

    note = args.note or ""
    if has_line_break(note):
        raise Refused("policy note must be a single line")
    if len(note) > ACK_NOTE_CAP:
        raise Refused(f"policy note exceeds {ACK_NOTE_CAP} chars ({len(note)}) "
                      "— witnesses stay small")
    if (cfg.get("ledger") or {}).get("adapter", "none") == "none":
        raise Refused(
            "no ledger configured — a policy change must be witnessed where "
            "acks would have lived, and adapter 'none' has no witness layer "
            "(re-init with --ledger file, or a command adapter, first)")
    if action == "off" and off_now:
        raise Refused(
            "acks are already disabled (recorded at ts="
            f"{pol.get('ts') or 'unknown time'}) — the decision is on record; "
            "`ack-policy on` first if you intend to change it")
    if action == "on" and not off_now:
        raise Refused("acks are not disabled — nothing to re-enable")
    ls = ledger_state(cfg)
    if not ls["reachable"]:
        raise GateError(
            "ledger unreachable — a policy change without its witness line "
            "is the tracelessness this command exists to prevent "
            f"({ls['note']})")
    head = chain_head(cfg, ls)
    ts = now_iso()
    line = (f"event=ack-{action} gen={head} ts={ts}"
            + (f" note={note}" if note else ""))
    ledger_append(cfg, line)  # raises on failure — no policy change unwitnessed
    if action == "off":
        cfg["ack_policy"] = {"mode": "off", "ts": ts, "gen": head,
                             "note": note}
    else:
        cfg.pop("ack_policy", None)
    save_config(root, cfg)
    print(line)
    if action == "off":
        print(f"acks disabled by recorded decision (head gen {head}) — "
              "`ack GEN` now refuses; verify/status attribute the absence to "
              "this policy")
        print("witness, not gate: builds, drills, restores are unaffected")
    else:
        print(f"acks re-enabled (head gen {head}) — `ack GEN` writes again; "
              "the gap in between stays explained by the two policy lines")
    return 0


# -------------------------------------------------------------------- main ----

def main(argv=None):
    global CMD_LEDGER_ALLOWED, EXTERNAL_LEDGER_ALLOWED
    ap = argparse.ArgumentParser(
        prog="backup_chain",
        description="Fenced, hash-chained workspace backups (protocol invariants in "
                    "references/PROTOCOL.md). No network; off-site distribution is yours.")
    ap.add_argument("--root", default=".",
                    help="project root (default: cwd; config at <root>/.vault/config.json)")
    ap.add_argument("--version", action="version", version=f"backup-chain {VERSION}")
    # Shared guard (audit T09, round 3): every subcommand accepts the explicit
    # per-invocation opt-in that the command-ledger adapter requires to run.
    guard = argparse.ArgumentParser(add_help=False)
    guard.add_argument("--allow-cmd-ledger", action="store_true",
                       help="opt in to executing the command-ledger adapter from "
                            ".vault/config.json for THIS invocation (refused "
                            "without it; file/none ledgers unaffected)")
    # Shared guard (audit T09, round 5): same consent class for a file-ledger
    # destination that resolves outside the workspace (absolute, traversing,
    # or through a planted symlink). In-root ledgers never consult it.
    guard.add_argument("--allow-external-ledger", action="store_true",
                       help="opt in to a file-ledger destination outside the "
                            "workspace for THIS invocation (refused without it; "
                            "in-root ledgers unaffected)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="initialize a chain in the project root",
                       parents=[guard])
    p.add_argument("--name"); p.add_argument("--output-dir")
    p.add_argument("--ledger", choices=["none", "file", "command"], default="file")
    p.add_argument("--ledger-file"); p.add_argument("--read-cmd"); p.add_argument("--append-cmd")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("member", help="add/remove/list chain members",
                       parents=[guard])
    p.add_argument("action", choices=["add", "remove", "list"])
    p.add_argument("path", nargs="?")
    p.add_argument("--critical", action="store_true")
    p.add_argument("--exclude", action="append", default=[], metavar="PATTERN",
                   help="(add) opt-in exclusion for this member's contents: "
                        "fnmatch on the path relative to the project root and "
                        "on the basename; repeatable; a matching directory "
                        "prunes its whole subtree. No excludes exist by "
                        "default beyond the chain's own archives")
    p.set_defaults(fn=cmd_member)

    p = sub.add_parser("evict", help="custody-preserving member removal (v1.2): "
                                    "package the member, hand it to a stow "
                                    "destination, untrack it, record the act",
                       parents=[guard])
    p.add_argument("path", help="member path to evict (must be a member; the "
                                "files on disk are never touched)")
    p.add_argument("--stow-to", dest="stow_to", metavar="DIR",
                   help="copy the eviction package here (created; hash-verified "
                        "at the destination — custody refused if the roundtrip "
                        "fails)")
    p.add_argument("--stow-cmd", dest="stow_cmd", metavar="CMD",
                   help="your own command; the package bytes arrive on its "
                        "stdin (per-invocation, never stored in config; success "
                        "is the command's exit code, claimed not verified)")
    p.add_argument("--note", help=f"single-line reason for the record "
                                  f"(≤{EVICT_NOTE_CAP} chars)")
    p.add_argument("--archive-mode", dest="archive_mode", metavar="MODE",
                   help="permission mode for the package, its receipt and any "
                        "stow copy, octal, e.g. 600 (default, owner-only) or "
                        "644; applied verbatim (umask does not widen it); "
                        "the persistent form is the config key archive_mode "
                        "(v1.3.1: config may narrow only — widening is "
                        "CLI-only, audit T09)")
    p.set_defaults(fn=cmd_evict)

    p = sub.add_parser("next-gen", help="print next generation (max(local, ledger)+1)",
                       parents=[guard])
    p.set_defaults(fn=cmd_next_gen)

    p = sub.add_parser("build", help="gated build: presence → manifest → roundtrip → "
                                     "receipt → drill", parents=[guard])
    p.add_argument("--carries", help="free-text note on what this generation holds")
    p.add_argument("--cot-trigger", help="decision trace trigger (v1.1): one of "
                                         + ", ".join(COT_TRIGGERS))
    p.add_argument("--cot-belief", help="decision trace: what was believed about "
                                         "workspace state at build time (≤140 chars)")
    p.add_argument("--cot-risk", help="decision trace: risk consciously accepted "
                                       "(≤80 chars)")
    p.add_argument("--cot-falsifier", help="decision trace: one checkable claim that, "
                                           "if false, indicts this generation's "
                                           "reasoning (≤80 chars)")
    p.add_argument("--label", help="optional filename label: <name>-g<GEN>-<label>.tar.gz")
    p.add_argument("--register", action="store_true", help="append the ledger line")
    p.add_argument("--output", help="override output path")
    p.add_argument("--archive-mode", dest="archive_mode", metavar="MODE",
                   help="permission mode for the archive, its receipt and any "
                        "stow copy, octal, e.g. 600 (default, owner-only) or "
                        "644; applied verbatim (umask does not widen it); "
                        "the persistent form is the config key archive_mode "
                        "(v1.3.1: config may narrow only — widening is "
                        "CLI-only, audit T09)")
    p.add_argument("--stow-to", dest="stow_to", metavar="DIR",
                   help="(v1.2, opt-in) copy the finished archive + receipt here "
                        "and hash-verify the copy (the off-site roundtrip "
                        "pattern); failure warns, never gates")
    p.add_argument("--stow-cmd", dest="stow_cmd", metavar="CMD",
                   help="(v1.2, opt-in) your own upload command; the finished "
                        "archive arrives on its stdin (per-invocation, never "
                        "stored in config; failure warns, never gates)")
    p.set_defaults(fn=cmd_build)

    p = sub.add_parser("ledger-line", help="print (or append) the ledger entry",
                       parents=[guard])
    p.add_argument("tarball"); p.add_argument("--append", action="store_true")
    p.set_defaults(fn=cmd_ledger_line)

    p = sub.add_parser("verify", help="sha256 vs receipt and ledger entry",
                       parents=[guard])
    p.add_argument("tarball")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("drill", help="standalone restore drill (extract + hash-verify; "
                                     "records a witness event)",
                       parents=[guard])
    p.add_argument("tarball")
    p.set_defaults(fn=cmd_drill)

    p = sub.add_parser("ack", help="operator acknowledgment appended to the ledger "
                                   "(v1.1 witness — never a gate)", parents=[guard])
    p.add_argument("gen", help="generation being acknowledged (must be known to "
                               "ledger or local chain)")
    p.add_argument("note", nargs="?", help=f"optional single-line note (≤{ACK_NOTE_CAP} chars)")
    p.set_defaults(fn=cmd_ack)

    p = sub.add_parser("ack-policy", help="show or change the ack policy; every "
                       "change is itself witnessed (event=ack-off / event=ack-on)",
                       parents=[guard])
    p.add_argument("action", nargs="?", choices=["off", "on"],
                   help="'off' disables acks (witnessed; refuses without a "
                        "reachable ledger); 'on' re-enables (witnessed); "
                        "omit to show the current policy")
    p.add_argument("--note", help=f"optional single-line why (≤{ACK_NOTE_CAP} chars)")
    p.set_defaults(fn=cmd_ack_policy)

    p = sub.add_parser("check", help="pre-restore fencing gate → JSON",
                       parents=[guard])
    p.add_argument("tarball")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("restore", help="per-member verified restore into --target",
                       parents=[guard])
    p.add_argument("tarball")
    p.add_argument("--target", required=True)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_restore)

    p = sub.add_parser("recheck", help="post-apply receipt → JSON",
                       parents=[guard])
    p.add_argument("gen")
    p.set_defaults(fn=cmd_recheck)

    p = sub.add_parser("status", help="chain state: members, local head, ledger head",
                       parents=[guard])
    p.set_defaults(fn=cmd_status)

    args = ap.parse_args(argv)
    CMD_LEDGER_ALLOWED = bool(getattr(args, "allow_cmd_ledger", False))
    EXTERNAL_LEDGER_ALLOWED = bool(getattr(args, "allow_external_ledger", False))
    root = os.path.abspath(args.root)
    try:
        return args.fn(args, root)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    except GateError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        # Same exit code a raw traceback gave (1), without the traceback.
        print(f"FAIL: I/O error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
