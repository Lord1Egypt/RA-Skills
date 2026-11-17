#!/usr/bin/env python3
"""
OpenClaw Security Audit
Read-only, local-only security checks for an OpenClaw installation.

- Python 3.8+ standard library only (no pip install needed).
- Makes no network requests and sends no telemetry.
- Never writes secret values to the console or reports: findings show the
  file, line, key name and secret type only. Home-directory paths are
  shortened to "~" so reports can be shared without exposing your username.
"""

import argparse
import fnmatch
import html
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

__version__ = "1.1.0"

HOME = str(Path.home())

DEFAULT_CONFIG: Dict[str, Any] = {
    "openclaw_paths": {
        "home": "~/.openclaw",
        "gateway_config": "~/.openclaw/openclaw.json",
        "agent_configs": "~/.openclaw/agents",
        "skills_dirs": ["~/.openclaw/plugin-skills", "~/.openclaw/skills", "~/.agents/skills"],
        "logs_dir": "~/.openclaw/logs",
        "state_dir": "~/.openclaw/state",
    },
    "env_scan_roots": ["~/.openclaw"],
    "checks": {
        "secrets_scan": True,
        "config_validation": True,
        "permissions_audit": True,
        "network_exposure": True,
        "crypto_hygiene": True,
        "supply_chain": True,
        "session_hygiene": True,
    },
    "exclusions": {"paths": [], "patterns": []},
    "limits": {"max_files": 20000, "max_file_mb": 2, "max_depth": 8},
    "output": {
        "report_path": "./security-audit-report.json",
        "html_report": "./security-audit-report.html",
        "redact_home": True,
    },
}

# Directories never worth walking (huge, vendored, or generated).
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", ".cache",
             "site-packages", "dist", "build", ".next", "Cache", "GPUCache"}

SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|apikey|secret|token|password|passwd|private[_-]?key|mnemonic|seed[_-]?phrase|webhook[_-]?url|bearer)",
    re.IGNORECASE)
# Keys that look secret-ish but hold non-secret values.
NON_SECRET_KEY_RE = re.compile(
    r"(max[_-]?tokens?|token[_-]?(limit|budget|count|usage|type|url|endpoint)|tokens$|password[_-]?(env|file|ref)|secret[_-]?(ref|name|id|env))",
    re.IGNORECASE)
KNOWN_TOKEN_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"sk-(?:ant-|proj-)?[A-Za-z0-9_\-]{20,}"), "OpenAI/Anthropic-style key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "GitHub token"),
    (re.compile(r"glpat-[A-Za-z0-9_\-]{20,}"), "GitLab token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"), "Slack token"),
    (re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_\-]{30,}\b"), "Telegram bot token"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "Private key block"),
]
PLACEHOLDER_RE = re.compile(r"^(\$\{.*\}|<.*>|\*+|x+|changeme|your[_-].*|example.*|placeholder|null|none|true|false|env:.*|secret:.*)$",
                            re.IGNORECASE)

CHECK_TOGGLES = {
    "SEC001": "secrets_scan", "SEC002": "secrets_scan", "SEC003": "secrets_scan",
    "CFG001": "config_validation", "PERM001": "permissions_audit", "NET001": "network_exposure",
    "CRYPTO001": "crypto_hygiene", "SUPPLY001": "supply_chain", "SESSION001": "session_hygiene",
}


@dataclass
class CheckResult:
    check_id: str
    name: str
    category: str
    severity: str  # critical, high, medium, low, info
    status: str    # pass, fail, warning, info, skip
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    remediation: Optional[str] = None


@dataclass
class AuditReport:
    tool_version: str
    timestamp: str
    openclaw_version: str
    platform: str
    python: str
    checks_total: int
    checks_passed: int
    checks_failed: int
    checks_warning: int
    checks_info: int
    checks_skipped: int
    results: List[CheckResult]


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _run(cmd: List[str], timeout: int = 10, cwd: Optional[str] = None) -> Optional[subprocess.CompletedProcess]:
    """Run a command safely; returns None if the tool is missing or fails to start."""
    if not shutil.which(cmd[0]):
        return None
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                              encoding="utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return None


class SecurityAuditor:
    def __init__(self, config_path: Optional[str] = None, verbose: bool = False):
        self.verbose = verbose
        self.results: List[CheckResult] = []
        self.walk_errors = 0
        self.config = self._load_config(config_path)
        lim = self.config["limits"]
        self.max_files = int(lim.get("max_files", 20000))
        self.max_bytes = int(float(lim.get("max_file_mb", 2)) * 1024 * 1024)
        self.max_depth = int(lim.get("max_depth", 8))

    # ---------------------------------------------------------------- helpers

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        config = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
        if not config_path:
            return config
        try:
            with open(config_path, "r", encoding="utf-8-sig") as f:
                user_config = json.load(f)
            if not isinstance(user_config, dict):
                raise ValueError("config root must be an object")
            _deep_merge(config, user_config)
        except (OSError, ValueError) as e:
            print(f"[warn] Could not load config {config_path}: {e}. Using defaults.", file=sys.stderr)
        # Backwards compatibility with the 1.0 single "skills_dir" key.
        paths = config["openclaw_paths"]
        if "skills_dir" in paths and paths["skills_dir"] not in paths["skills_dirs"]:
            paths["skills_dirs"].append(paths.pop("skills_dir"))
        return config

    def _log(self, msg: str):
        if self.verbose:
            print(f"  [debug] {msg}", file=sys.stderr)

    @staticmethod
    def _p(path: str) -> Path:
        return Path(os.path.expandvars(os.path.expanduser(path)))

    def _show(self, path: Any) -> str:
        """Display form of a path: home directory replaced with ~."""
        s = str(path)
        if self.config["output"].get("redact_home", True) and HOME and s.lower().startswith(HOME.lower()):
            s = "~" + s[len(HOME):]
        return s

    def _excluded(self, path: Path) -> bool:
        s = str(path)
        for ex in self.config["exclusions"].get("paths", []):
            if s.lower().startswith(str(self._p(ex)).lower()):
                return True
        for pat in self.config["exclusions"].get("patterns", []):
            if fnmatch.fnmatch(path.name, pat) or pat in s:
                return True
        return False

    def _walk(self, root: Path, name_filter=None) -> Iterator[Path]:
        """Bounded, error-tolerant file walker (handles long paths, locked files, junction loops)."""
        if not root.is_dir():
            return
        count = 0
        root_depth = len(root.parts)

        def onerror(err):
            self.walk_errors += 1
            self._log(f"walk skipped: {err}")

        for dirpath, dirnames, filenames in os.walk(root, onerror=onerror, followlinks=False):
            current = Path(dirpath)
            if len(current.parts) - root_depth >= self.max_depth:
                dirnames[:] = []
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not self._excluded(current / d)]
            for fn in filenames:
                if name_filter and not name_filter(fn):
                    continue
                p = current / fn
                if self._excluded(p):
                    continue
                count += 1
                if count > self.max_files:
                    self._log(f"file limit reached under {root}")
                    return
                yield p

    def _read_text(self, path: Path) -> Optional[str]:
        try:
            if not path.is_file() or path.stat().st_size > self.max_bytes:
                return None
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            self.walk_errors += 1
            self._log(f"read skipped {self._show(path)}: {e}")
            return None

    @staticmethod
    def _looks_like_secret(value: str) -> bool:
        v = value.strip()
        if len(v) < 12 or PLACEHOLDER_RE.match(v):
            return False
        if v.startswith(("http://localhost", "http://127.", "https://localhost")):
            return False
        if " " in v and len(v.split()) > 3 and not re.search(r"\d", v):
            return False  # prose, not a key (mnemonics are handled by key name)
        classes = sum(bool(re.search(p, v)) for p in (r"[a-z]", r"[A-Z]", r"\d", r"[_\-+/=.:]"))
        return classes >= 2

    def _scan_text_for_secrets(self, path: Path, text: str) -> List[Dict[str, Any]]:
        findings = []
        seen_lines = set()
        lines = text.splitlines()
        kv_re = re.compile(r"""["']?([A-Za-z0-9_.\-]+)["']?\s*[:=]\s*["']([^"'\n]+)["']""")
        for i, line in enumerate(lines, 1):
            for m in kv_re.finditer(line):
                key, val = m.group(1), m.group(2)
                if SECRET_KEY_RE.search(key) and not NON_SECRET_KEY_RE.search(key) and self._looks_like_secret(val):
                    findings.append({"file": self._show(path), "line": i, "key": key,
                                     "type": "Hardcoded secret value", "length": len(val)})
                    seen_lines.add(i)
            if i in seen_lines:
                continue
            for rx, label in KNOWN_TOKEN_PATTERNS:
                if rx.search(line):
                    findings.append({"file": self._show(path), "line": i, "type": label})
                    break
        return findings

    def _add(self, check_id, name, category, severity, func):
        toggle = CHECK_TOGGLES.get(check_id)
        if toggle and not self.config["checks"].get(toggle, True):
            self.results.append(CheckResult(check_id, name, category, severity, "skip", "Disabled in config"))
            return
        try:
            r = func()
        except Exception as e:  # a buggy check must never crash the audit
            r = {"status": "skip", "message": f"Check could not run: {type(e).__name__}: {self._show(e)}"}
        self.results.append(CheckResult(check_id, name, category, severity, r.get("status", "pass"),
                                        r.get("message", ""), r.get("details", {}), r.get("remediation")))

    # ----------------------------------------------------------------- checks

    def check_secrets_in_config(self) -> Dict[str, Any]:
        paths = self.config["openclaw_paths"]
        files = [self._p(paths["gateway_config"])]
        files += list(self._walk(self._p(paths["agent_configs"]),
                                 lambda n: n.lower().endswith((".json", ".json5", ".yaml", ".yml", ".toml"))))
        findings, scanned = [], 0
        for f in files:
            if self._excluded(f):
                continue
            text = self._read_text(f)
            if text is None:
                continue
            scanned += 1
            findings += self._scan_text_for_secrets(f, text)
        if findings:
            return {"status": "fail",
                    "message": f"{len(findings)} hardcoded secret(s) in {len({x['file'] for x in findings})} config file(s) (values hidden)",
                    "details": {"files_scanned": scanned, "findings": findings[:50]},
                    "remediation": "Move secrets into the OpenClaw secrets store or environment variables and reference them "
                                   "(SecretRef / ${VAR}) instead of plain text. Rotate any key that was ever shared or committed."}
        return {"status": "pass", "message": f"No hardcoded secrets in {scanned} config file(s)", "details": {"files_scanned": scanned}}

    def check_env_files(self) -> Dict[str, Any]:
        findings, files = [], 0
        for root in self.config.get("env_scan_roots", []):
            for f in self._walk(self._p(root), lambda n: n == ".env" or n.startswith(".env.") or n.endswith(".env")):
                if f.name.endswith((".example", ".sample", ".template")):
                    continue
                text = self._read_text(f)
                if text is None:
                    continue
                files += 1
                for i, line in enumerate(text.splitlines(), 1):
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.replace("export ", "").strip()
                    val = val.strip().strip("\"'")
                    if self._looks_like_secret(val) and (SECRET_KEY_RE.search(key) or any(rx.search(val) for rx, _ in KNOWN_TOKEN_PATTERNS)):
                        findings.append({"file": self._show(f), "line": i, "key": key, "length": len(val)})
        if findings:
            return {"status": "warning",
                    "message": f"{len(findings)} secret(s) stored in {files} .env file(s) (values hidden)",
                    "details": {"findings": findings[:50]},
                    "remediation": "Keep .env files out of git (.gitignore), restrict them to your user account, "
                                   "and never include them in skill packages or backups you share."}
        return {"status": "pass", "message": f"No plain-text secrets found in {files} .env file(s)", "details": {}}

    def check_git_history_secrets(self) -> Dict[str, Any]:
        repo = self.config.get("git_repo") or os.getcwd()
        probe = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo)
        if probe is None:
            return {"status": "skip", "message": "git not installed"}
        if probe.returncode != 0:
            return {"status": "skip", "message": "Current directory is not a git repository (use --git-repo PATH)"}
        log = _run(["git", "log", "-p", "-n", "50", "--all", "--no-color", "--format=commit %h"], timeout=60, cwd=repo)
        if log is None or log.returncode != 0:
            return {"status": "skip", "message": "Could not read git history"}
        findings, commit = [], "?"
        for line in log.stdout.splitlines():
            if line.startswith("commit "):
                commit = line.split()[1]
            elif line.startswith("+") and not line.startswith("+++"):
                for rx, label in KNOWN_TOKEN_PATTERNS:
                    if rx.search(line):
                        findings.append({"commit": commit, "type": label})
                        break
        if findings:
            return {"status": "fail", "message": f"{len(findings)} secret(s) added in the last 50 commits (values hidden)",
                    "details": {"findings": findings[:50]},
                    "remediation": "Rotate the exposed credentials first, then purge history with git-filter-repo or BFG."}
        return {"status": "pass", "message": "No known secret formats in the last 50 commits"}

    def _load_gateway_config(self) -> Optional[Dict[str, Any]]:
        text = self._read_text(self._p(self.config["openclaw_paths"]["gateway_config"]))
        if text is None:
            return None
        try:
            data = json.loads(text)
            return data if isinstance(data, dict) else None
        except ValueError:
            return None

    def check_config_validation(self) -> Dict[str, Any]:
        path = self._p(self.config["openclaw_paths"]["gateway_config"])
        if not path.exists():
            return {"status": "skip", "message": f"Gateway config not found at {self._show(path)}"}
        cfg = self._load_gateway_config()
        if cfg is None:
            return {"status": "skip", "message": "Gateway config is not strict JSON (JSON5?) - structural checks skipped"}
        issues = []
        gw = cfg.get("gateway") if isinstance(cfg.get("gateway"), dict) else {}
        bind = str(gw.get("bind", "")).lower()
        auth = gw.get("auth") if isinstance(gw.get("auth"), dict) else {}
        auth_mode = str(auth.get("mode", "")).lower()
        if bind and bind not in ("loopback", "localhost", "127.0.0.1", "::1", "tailnet", "tailscale"):
            issues.append(f"Gateway bind is '{bind}' (reachable from other devices); make sure auth is enabled")
            if auth_mode in ("none", "off", ""):
                issues.append("Gateway is network-reachable without an auth mode configured")
        if auth_mode in ("none", "off"):
            issues.append("Gateway auth is disabled")
        if cfg.get("debug") is True:
            issues.append("debug=true in gateway config")
        tools = cfg.get("tools") if isinstance(cfg.get("tools"), dict) else {}
        exec_cfg = tools.get("exec") if isinstance(tools.get("exec"), dict) else {}
        if str(exec_cfg.get("security", "")).lower() == "full" and str(exec_cfg.get("ask", "")).lower() == "off":
            issues.append("Shell exec runs with full access and no approval prompts")
        channels = cfg.get("channels") if isinstance(cfg.get("channels"), dict) else {}
        for name, ch in channels.items():
            if not isinstance(ch, dict) or ch.get("enabled") is False:
                continue
            policy = str(ch.get("dmPolicy", "")).lower()
            if policy == "open":
                issues.append(f"Channel '{name}' accepts DMs from anyone (dmPolicy=open)")
            allow = ch.get("allowFrom")
            if isinstance(allow, list) and "*" in [str(a) for a in allow]:
                issues.append(f"Channel '{name}' allowFrom contains '*'")
        if issues:
            return {"status": "warning", "message": f"{len(issues)} risky gateway setting(s)", "details": {"issues": issues},
                    "remediation": "Bind the gateway to loopback (or use Tailscale), keep auth on, restrict channel senders "
                                   "with allowlists, and keep exec approvals enabled. Run `openclaw security audit` too if available."}
        return {"status": "pass", "message": "No risky gateway settings detected (heuristic)"}

    def _sensitive_files(self) -> List[Path]:
        paths = self.config["openclaw_paths"]
        out = [self._p(paths["gateway_config"])]
        for root in self.config.get("env_scan_roots", []):
            out += list(self._walk(self._p(root), lambda n: n == ".env" or n.startswith(".env.")))
        state = self._p(paths["state_dir"])
        if state.is_dir():
            out += [p for p in state.iterdir() if p.is_file() and p.suffix in (".sqlite", ".json", ".db")]
        return [p for p in out if p.is_file()][:200]

    def check_file_permissions(self) -> Dict[str, Any]:
        files = self._sensitive_files()
        if not files:
            return {"status": "skip", "message": "No sensitive files found to check"}
        issues, unchecked = [], 0
        if os.name == "nt":
            if not shutil.which("icacls"):
                return {"status": "skip", "message": "icacls not available"}
            broad = re.compile(r"(Everyone|BUILTIN\\Users|Authenticated Users|NT AUTHORITY\\Authenticated Users):\(.*?(F|M|R|RX|W)\b",
                               re.IGNORECASE)
            for f in files:
                r = _run(["icacls", str(f)], timeout=10)
                if r is None or r.returncode != 0:
                    unchecked += 1
                    continue
                for line in r.stdout.splitlines():
                    m = broad.search(line)
                    if m:
                        issues.append({"file": self._show(f), "issue": f"Readable by {m.group(1)}"})
                        break
        else:
            for f in files:
                try:
                    mode = f.stat().st_mode
                except OSError:
                    unchecked += 1
                    continue
                if mode & (stat.S_IRWXG | stat.S_IRWXO):
                    issues.append({"file": self._show(f), "issue": "Accessible by group/others", "mode": oct(mode & 0o777)})
        details = {"files_checked": len(files) - unchecked, "files_unreadable": unchecked}
        if issues:
            fix = ("icacls <file> /inheritance:r /grant:r \"%USERNAME%:F\"" if os.name == "nt" else "chmod 600 <file>")
            return {"status": "warning", "message": f"{len(issues)} sensitive file(s) readable by other users",
                    "details": {**details, "issues": issues[:30]}, "remediation": f"Restrict to your user only: {fix}"}
        return {"status": "pass", "message": f"{details['files_checked']} sensitive file(s) restricted to your account", "details": details}

    def check_network_exposure(self) -> Dict[str, Any]:
        if sys.platform == "win32":
            r = _run(["netstat", "-an", "-p", "TCP"])
        elif sys.platform == "darwin":
            r = _run(["netstat", "-an", "-p", "tcp"])
        else:
            r = _run(["ss", "-tln"]) or _run(["netstat", "-tln"])
        if r is None:
            return {"status": "skip", "message": "netstat/ss not available"}
        known = {9222: "Chrome DevTools remote debugging", 18789: "OpenClaw gateway", 18800: "OpenClaw managed browser (CDP)",
                 3000: "dev server", 5173: "dev server", 8080: "HTTP proxy/dev", 8888: "Jupyter", 11434: "Ollama",
                 5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB"}
        exposed, local = [], []
        for line in r.stdout.splitlines():
            if not re.search(r"LISTEN", line, re.IGNORECASE):
                continue
            for addr in re.findall(r"(\S+)[:.](\d+)\s", line + " "):
                host, port = addr[0], int(addr[1])
                if port not in known:
                    continue
                entry = {"port": port, "service": known[port], "address": host}
                if host in ("0.0.0.0", "*", "[::]", "::", "0:0:0:0:0:0:0:0"):
                    if entry not in exposed:
                        exposed.append(entry)
                elif entry not in local:
                    local.append(entry)
                break
        tunnels = []
        procs = _run(["tasklist", "/fo", "csv", "/nh"]) if os.name == "nt" else _run(["ps", "-A", "-o", "comm="])
        if procs is not None:
            names = procs.stdout.lower()
            tunnels = [t for t in ("ngrok", "cloudflared", "localtunnel", "frpc", "bore") if t in names]
        details = {"exposed_on_all_interfaces": exposed, "loopback_only": local, "tunnels_running": tunnels}
        if exposed or tunnels:
            return {"status": "warning",
                    "message": f"{len(exposed)} sensitive port(s) open to the network, {len(tunnels)} tunnel(s) running",
                    "details": details,
                    "remediation": "Bind debugging/admin ports to 127.0.0.1, firewall them, and put tunnels behind authentication."}
        return {"status": "pass", "message": f"No sensitive ports exposed beyond localhost ({len(local)} loopback-only)", "details": details}

    def check_crypto_hygiene(self) -> Dict[str, Any]:
        issues = []
        root = self._p(self.config["openclaw_paths"]["home"])
        for f in self._walk(root, lambda n: n.lower().endswith((".pem", ".key", ".p12", ".pfx", ".ppk")) or n in ("id_rsa", "id_ed25519")):
            text = self._read_text(f)
            if text is None:
                continue
            if "PRIVATE KEY" in text and "ENCRYPTED" not in text:
                issues.append({"file": self._show(f), "issue": "Unencrypted private key"})
            elif f.suffix.lower() in (".p12", ".pfx"):
                issues.append({"file": self._show(f), "issue": "Certificate bundle stored in OpenClaw folder"})
        cfg_text = self._read_text(self._p(self.config["openclaw_paths"]["gateway_config"])) or ""
        if re.search(r'"(rejectUnauthorized|verifySsl|verify_ssl|tlsVerify)"\s*:\s*false', cfg_text, re.IGNORECASE):
            issues.append({"file": self._show(self.config["openclaw_paths"]["gateway_config"]), "issue": "TLS certificate verification disabled"})
        if issues:
            return {"status": "warning", "message": f"{len(issues)} crypto hygiene issue(s)", "details": {"issues": issues[:30]},
                    "remediation": "Encrypt or remove private keys from the OpenClaw folder and keep TLS verification on."}
        return {"status": "pass", "message": "No unencrypted keys or disabled TLS verification found"}

    def check_supply_chain(self) -> Dict[str, Any]:
        issues, skills = [], 0
        risky_kw = re.compile(r"\b(curl|wget|iwr|invoke-webrequest|powershell|bash\s+-c|eval|base64\s+-d|frombase64string)\b", re.IGNORECASE)
        for d in self.config["openclaw_paths"]["skills_dirs"]:
            base = self._p(d)
            if not base.is_dir():
                continue
            try:
                entries = [e for e in base.iterdir() if e.is_dir()]
            except OSError:
                continue
            for skill in entries:
                skills += 1
                binaries = [self._show(p) for p in self._walk(skill, lambda n: n.lower().endswith((".exe", ".dll", ".so", ".dylib", ".bat", ".scr")))]
                if binaries:
                    issues.append({"skill": skill.name, "issue": "Ships executable/binary files", "files": binaries[:10]})
                pkg = skill / "package.json"
                if pkg.is_file():
                    try:
                        scripts = json.loads(pkg.read_text(encoding="utf-8", errors="ignore")).get("scripts", {}) or {}
                    except (OSError, ValueError, AttributeError):
                        scripts = {}
                    for hook in ("preinstall", "install", "postinstall", "prepare"):
                        cmd = str(scripts.get(hook, ""))
                        if cmd and risky_kw.search(cmd):
                            issues.append({"skill": skill.name, "issue": f"npm {hook} script downloads/executes code"})
                md = skill / "SKILL.md"
                text = self._read_text(md) if md.is_file() else None
                if text and re.search(r"(curl|iwr|wget)[^\n|]*\|\s*(sh|bash|iex|powershell)", text, re.IGNORECASE):
                    issues.append({"skill": skill.name, "issue": "SKILL.md pipes a download straight into a shell"})
        if issues:
            return {"status": "warning", "message": f"{len(issues)} supply-chain risk(s) across {skills} skill(s)",
                    "details": {"issues": issues[:30]},
                    "remediation": "Review these skills manually; only keep skills from sources you trust and pin their versions."}
        return {"status": "pass", "message": f"No risky patterns in {skills} installed skill(s)"}

    def check_session_hygiene(self) -> Dict[str, Any]:
        items = []
        paths = self.config["openclaw_paths"]
        state = self._p(paths["state_dir"])
        if state.is_dir():
            for db in state.glob("*.sqlite*"):
                try:
                    mb = db.stat().st_size / 1048576
                except OSError:
                    continue
                if mb > 500:
                    items.append({"file": self._show(db), "size_mb": round(mb), "issue": "Very large state database"})
        logs = self._p(paths["logs_dir"])
        if logs.is_dir():
            now = datetime.now().timestamp()
            old = 0
            for log in logs.glob("*.log*"):
                try:
                    if (now - log.stat().st_mtime) / 86400 > 30:
                        old += 1
                except OSError:
                    pass
            if old:
                items.append({"folder": self._show(logs), "old_logs": old, "issue": "Log files older than 30 days (may contain chat content)"})
        if items:
            return {"status": "info", "message": f"{len(items)} housekeeping item(s)", "details": {"items": items},
                    "remediation": "Enable session maintenance / cold storage in OpenClaw and delete old logs you no longer need."}
        return {"status": "pass", "message": "No oversized databases or stale logs"}

    # ------------------------------------------------------------------ run

    CHECKS = [
        ("SEC001", "Secrets in Config Files", "secrets", "critical", "check_secrets_in_config"),
        ("SEC002", "Secrets in .env Files", "secrets", "high", "check_env_files"),
        ("SEC003", "Secrets in Git History", "secrets", "critical", "check_git_history_secrets"),
        ("CFG001", "Gateway Config Review", "config", "high", "check_config_validation"),
        ("PERM001", "Sensitive File Permissions", "permissions", "medium", "check_file_permissions"),
        ("NET001", "Network Exposure", "network", "high", "check_network_exposure"),
        ("CRYPTO001", "Crypto Hygiene", "crypto", "medium", "check_crypto_hygiene"),
        ("SUPPLY001", "Supply Chain Risks", "supply_chain", "medium", "check_supply_chain"),
        ("SESSION001", "Session Hygiene", "sessions", "low", "check_session_hygiene"),
    ]

    def run(self, only: Optional[List[str]] = None) -> AuditReport:
        for cid, name, cat, sev, fn in self.CHECKS:
            if only and cid not in only:
                continue
            print(f"  Checking {cid} {name}...", file=sys.stderr)
            self._add(cid, name, cat, sev, getattr(self, fn))
        count = lambda s: sum(1 for r in self.results if r.status == s)
        return AuditReport(__version__, datetime.now().isoformat(timespec="seconds"), self._openclaw_version(),
                           sys.platform, sys.version.split()[0], len(self.results), count("pass"), count("fail"),
                           count("warning"), count("info"), count("skip"), self.results)

    @staticmethod
    def _openclaw_version() -> str:
        r = _run(["openclaw", "--version"], timeout=15)
        if r is None and os.name == "nt":
            r = _run(["openclaw.cmd", "--version"], timeout=15)
        return (r.stdout.strip().splitlines() or ["unknown"])[0] if r and r.returncode == 0 else "unknown"

    # --------------------------------------------------------------- output

    @staticmethod
    def to_json(report: AuditReport) -> str:
        return json.dumps(asdict(report), indent=2, ensure_ascii=False)

    @staticmethod
    def to_html(report: AuditReport) -> str:
        e = html.escape
        colors = {"critical": "#dc2626", "high": "#ea580c", "medium": "#d97706", "low": "#65a30d", "info": "#2563eb",
                  "pass": "#16a34a", "fail": "#dc2626", "warning": "#d97706", "skip": "#6b7280"}
        rows = []
        for r in report.results:
            details = e(json.dumps(r.details, indent=2, ensure_ascii=False)) if r.details else ""
            fix = f"<p class='fix'>&rarr; {e(r.remediation)}</p>" if r.remediation and r.status != "pass" else ""
            rows.append(
                f"<tr><td>{e(r.check_id)}</td><td>{e(r.name)}</td>"
                f"<td><span class='b' style='background:{colors.get(r.severity, '#6b7280')}'>{e(r.severity.upper())}</span></td>"
                f"<td><span class='b' style='background:{colors.get(r.status, '#6b7280')}'>{e(r.status.upper())}</span></td>"
                f"<td>{e(r.message)}{fix}" + (f"<details><summary>details</summary><pre>{details}</pre></details>" if details else "") + "</td></tr>")
        cards = "".join(f"<div class='c'><h3 style='color:{col}'>{n}</h3><p>{lbl}</p></div>" for n, lbl, col in (
            (report.checks_passed, "Passed", "#16a34a"), (report.checks_failed, "Failed", "#dc2626"),
            (report.checks_warning, "Warnings", "#d97706"), (report.checks_info, "Info", "#2563eb"),
            (report.checks_skipped, "Skipped", "#6b7280")))
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>OpenClaw Security Audit</title><style>
body{{font-family:system-ui,sans-serif;margin:2rem;color:#111}}.s{{display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0}}
.c{{background:#f3f4f6;border-radius:8px;padding:1rem 1.5rem;text-align:center;min-width:90px}}.c h3{{margin:0;font-size:1.8rem}}.c p{{margin:.3rem 0 0;color:#6b7280}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:.6rem;text-align:left;border-bottom:1px solid #e5e7eb;vertical-align:top}}th{{background:#f3f4f6}}
.b{{padding:.15rem .45rem;border-radius:4px;color:#fff;font-size:.75rem;font-weight:600}}pre{{background:#f3f4f6;padding:.5rem;max-height:240px;overflow:auto;font-size:.78rem}}
.fix{{color:#374151;font-size:.85rem;margin:.4rem 0}}</style></head><body>
<h1>OpenClaw Security Audit</h1>
<p>Generated {e(report.timestamp)} &middot; {e(report.platform)} &middot; Python {e(report.python)} &middot; OpenClaw {e(report.openclaw_version)} &middot; tool v{e(report.tool_version)}</p>
<p><small>Secret values are never included in this report. Home paths are shown as ~.</small></p>
<div class="s">{cards}</div>
<table><thead><tr><th>ID</th><th>Check</th><th>Severity</th><th>Status</th><th>Result</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table></body></html>"""

    @staticmethod
    def print_summary(report: AuditReport):
        print("\n=== OpenClaw Security Audit ===")
        print(f"Total {report.checks_total} | Pass {report.checks_passed} | Fail {report.checks_failed} | "
              f"Warn {report.checks_warning} | Info {report.checks_info} | Skip {report.checks_skipped}")
        for r in report.results:
            print(f"  [{r.status.upper():7}] {r.check_id:10} {r.message}")
            if r.remediation and r.status in ("fail", "warning", "info"):
                print(f"            -> {r.remediation}")


def main(argv: Optional[List[str]] = None) -> int:
    for s in (sys.stdout, sys.stderr):  # avoid UnicodeEncodeError on legacy Windows consoles
        try:
            s.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Read-only, local-only security audit for OpenClaw")
    ap.add_argument("--config", "-c", help="Path to a JSON config file")
    ap.add_argument("--output", "-o", help="JSON report path")
    ap.add_argument("--html", help="HTML report path")
    ap.add_argument("--no-report", action="store_true", help="Print to console only, write no files")
    ap.add_argument("--check", action="append", help="Run only this check ID (repeatable)")
    ap.add_argument("--git-repo", help="Git repository to scan for SEC003 (default: current directory)")
    ap.add_argument("--list-checks", action="store_true", help="List checks and exit")
    ap.add_argument("--version", action="version", version=f"openclaw-security-audit {__version__}")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args(argv)

    if args.list_checks:
        for cid, name, _, sev, _ in SecurityAuditor.CHECKS:
            print(f"  {cid:10} {name} [{sev}]")
        return 0

    auditor = SecurityAuditor(args.config, args.verbose)
    if args.git_repo:
        auditor.config["git_repo"] = args.git_repo
    only = [c.upper() for c in args.check] if args.check else None
    if only:
        unknown = set(only) - {c[0] for c in SecurityAuditor.CHECKS}
        if unknown:
            print(f"Unknown check ID(s): {', '.join(sorted(unknown))}. Use --list-checks.", file=sys.stderr)
            return 64
    report = auditor.run(only)

    if not args.no_report:
        out = Path(args.output or auditor.config["output"]["report_path"])
        page = Path(args.html or auditor.config["output"]["html_report"])
        try:
            out.write_text(auditor.to_json(report), encoding="utf-8")
            page.write_text(auditor.to_html(report), encoding="utf-8")
            print(f"\nReports: {out}  |  {page}  (keep them private; do not commit)")
        except OSError as err:
            print(f"Could not write report: {err}", file=sys.stderr)

    auditor.print_summary(report)
    if auditor.walk_errors:
        print(f"  ({auditor.walk_errors} unreadable/locked path(s) skipped; use -v to list)")
    if report.checks_failed:
        return 1
    if report.checks_warning:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
