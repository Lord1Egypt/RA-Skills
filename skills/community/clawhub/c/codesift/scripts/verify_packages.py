#!/usr/bin/env python3
"""Check public registry names without claiming package safety, version validity, or API compatibility."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import configparser
import locale
import os
import re
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from detect_lang import require_python  # noqa: E402

# Check the interpreter before importing modules that need Python 3.11+ (tomllib).
require_python()

import tomllib  # noqa: E402

from dependencies import (  # noqa: E402
    LOCAL_SOURCES,
    canonical_name,
    local_entry,
    npm_registry_for,
    npmrc_entries,
    read_dependencies,
    registry_entry,
)
from detect_lang import (  # noqa: E402
    add_project_arguments,
    positive_int,
    print_report,
    select_language,
)

USER_AGENT = "codesift/3 (+https://github.com/zanw1/CodeSift)"
DEFAULT_BASES = {
    "python": "https://pypi.org/simple",
    "javascript": "https://registry.npmjs.org",
    "rust": "https://index.crates.io",
}
MIRRORS = {
    "cn": {
        "python": "https://pypi.tuna.tsinghua.edu.cn/simple",
        "javascript": "https://registry.npmmirror.com",
        "rust": "https://mirrors.tuna.tsinghua.edu.cn/crates.io-index",
    }
}
CANARIES = {"python": "pip", "javascript": "npm", "rust": "serde"}
BASE_OPTIONS = {"index", "index-url", "registry", "replace-with"}
# A tuple overrides platform discovery, including an empty tuple for isolated tests.
SYSTEM_PIP_CONFIGS: tuple[Path, ...] | None = None
PIP_OPTIONS = ("index-url", "extra-index-url", "find-links", "no-index")
PIP_TRUE = {"1", "true", "yes", "on"}
PIP_FALSE = {"0", "false", "no", "off"}
WORKERS = 4
BREAKER = 3


def crate_index_path(name: str) -> str:
    """Map a crate name to its Cargo sparse-index file path."""
    name = name.lower()
    if len(name) <= 2:
        return f"{len(name)}/{name}"
    if len(name) == 3:
        return f"3/{name[0]}/{name}"
    return f"{name[:2]}/{name[2:4]}/{name}"


def registry_url(name: str, lang: str, base: str) -> str:
    """Build the per-name URL: PEP 503 simple page, npm package document, or sparse-index file."""
    base = base.rstrip("/")
    if lang == "python":
        normalized = re.sub(r"[-_.]+", "-", name).lower()
        return f"{base}/{urllib.parse.quote(normalized)}/"
    if lang == "javascript":
        return f"{base}/{urllib.parse.quote(name, safe='@')}"
    return f"{base}/{urllib.parse.quote(crate_index_path(name))}"


def proxy_label(url: str) -> str | None:
    """Name the proxy urllib would use for a URL, without user-info or credentials."""
    parts = urllib.parse.urlsplit(url)
    try:
        if urllib.request.proxy_bypass(parts.hostname or ""):
            return None
        proxy = urllib.request.getproxies().get(parts.scheme)
        if not proxy:
            return None
        proxy_parts = urllib.parse.urlsplit(proxy if "://" in proxy else f"http://{proxy}")
        port = f":{proxy_parts.port}" if proxy_parts.port else ""
    except (OSError, ValueError):
        return "unknown"
    return f"{proxy_parts.hostname}{port}"


def network_reason(error: Exception, url: str, timeout: int) -> str:
    """Describe a network failure with the host and any proxy so users can fix routing."""
    host = urllib.parse.urlsplit(url).hostname
    detail = getattr(error, "reason", error)
    text = (
        f"timed out after {timeout}s"
        if isinstance(detail, TimeoutError) or "timed out" in str(detail)
        else f"{type(detail).__name__}: {detail}"
    )
    proxy = proxy_label(url)
    route = f"via proxy {proxy}" if proxy else "without a proxy"
    return f"could not reach {host} {route}: {text}"


def check_registry(
    name: str, lang: str, timeout: int = 10, base: str | None = None
) -> tuple[str, str]:
    """Treat only registry HTTP 404/410 as absence; keep other failures unresolved with host details.

    HEAD avoids downloading large package documents; GET is the fallback for servers without HEAD.
    """
    url = registry_url(name, lang, base or DEFAULT_BASES[lang])
    host = urllib.parse.urlsplit(url).hostname
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(
            url, method=method, headers={"User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status == 200:
                    return (
                        "registry_match",
                        f"name exists on {host}; version, provenance and safety not checked",
                    )
                return "error", f"unexpected HTTP status {response.status} from {host}"
        except urllib.error.HTTPError as error:
            if method == "HEAD" and error.code in {405, 501}:
                continue
            if error.code in {404, 410}:
                return (
                    "not_found",
                    f"name absent from {host}; not proof of hallucination",
                )
            return "error", f"HTTP {error.code} from {host}"
        except (OSError, ValueError) as error:
            return "error", network_reason(error, url, timeout)
    return "error", f"{host} rejected HEAD and GET"


def run_checks(
    names: list[str], lang: str, timeout: int, base: str
) -> list[tuple[str, str] | None]:
    """Check names in small parallel batches; stop after consecutive errors with no success.

    Unchecked positions stay None so the caller can report them as not_checked.
    """
    outcomes: list[tuple[str, str] | None] = [None] * len(names)
    consecutive = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for start in range(0, len(names), WORKERS):
            if consecutive >= BREAKER:
                break
            batch = names[start : start + WORKERS]
            results = pool.map(lambda name: check_registry(name, lang, timeout, base), batch)
            for offset, outcome in enumerate(results):
                outcomes[start + offset] = outcome
                consecutive = consecutive + 1 if outcome[0] == "error" else 0
    return outcomes


def display_path(path: Path, home: Path) -> str:
    """Show configuration paths relative to the home directory for shorter reports."""
    return f"~/{path.relative_to(home).as_posix()}" if path.is_relative_to(home) else str(path)


def pip_site_prefix() -> Path:
    """Locate site configuration for the helper's actual interpreter, not VIRTUAL_ENV."""
    return Path(sys.prefix)


def pip_config_encoding() -> str:
    """Match pip's interpreter-dependent default encoding without changing the locale."""
    return "utf-8" if sys.flags.utf8_mode else locale.getpreferredencoding(False)


def read_pip_config(path: Path) -> str:
    """Decode pip configuration strictly, giving an explicit UTF-8 BOM precedence."""
    data = path.read_bytes()
    encoding = "utf-8-sig" if data.startswith(b"\xef\xbb\xbf") else pip_config_encoding()
    return data.decode(encoding)


def pip_config_paths(
    environ: dict, home: Path, *, platform: str, prefix: Path
) -> list[Path]:
    """Discover pip files in precedence order while honoring explicit-file suppression."""
    configured = environ.get("PIP_CONFIG_FILE", "")
    null_names = {os.devnull.casefold()}
    if platform == "win32":
        null_names.add("nul")
    if configured.casefold() in null_names:
        return []
    explicit = Path(configured) if configured else None
    if SYSTEM_PIP_CONFIGS is not None:
        system = list(SYSTEM_PIP_CONFIGS)
    elif platform == "win32":
        programdata = environ.get("PROGRAMDATA") or environ.get("ProgramData") or "C:/ProgramData"
        system = [Path(programdata) / "pip/pip.ini"]
    else:
        system = [
            Path(directory) / "pip/pip.conf"
            for directory in environ.get("XDG_CONFIG_DIRS", "/etc/xdg").split(os.pathsep)
            if directory
        ]
        system.append(Path("/etc/pip.conf"))
        if platform == "darwin":
            system.append(Path("/Library/Application Support/pip/pip.conf"))
    if platform == "win32":
        user = [home / "pip/pip.ini"]
        appdata = environ.get("APPDATA") or environ.get("AppData")
        if appdata:
            user.append(Path(appdata) / "pip/pip.ini")
        site = prefix / "pip.ini"
    else:
        modern = Path(environ.get("XDG_CONFIG_HOME") or home / ".config") / "pip/pip.conf"
        mac_user = home / "Library/Application Support/pip/pip.conf"
        if platform == "darwin" and mac_user.parent.is_dir():
            modern = mac_user
        user = [home / ".pip/pip.conf", modern]
        site = prefix / "pip.conf"
    if explicit is not None and explicit.exists():
        user = []
    return list(dict.fromkeys([*system, *user, site, *([explicit] if explicit else [])]))


def pip_setting_entries(origin: str, section: str, option: str, value: str) -> list[dict]:
    """Keep source provenance without retaining credentials or silently repairing invalid values."""
    values = value.split()
    if not values:
        return []
    if option == "no-index":
        enabled = value.strip().lower()
        item = local_entry(origin, option if enabled in PIP_TRUE | PIP_FALSE else "unparsed")
        item["enabled"] = enabled in PIP_TRUE
        records = [item]
    elif option == "index-url" and len(values) != 1:
        records = [local_entry(origin, "unparsed")]
    else:
        records = []
        for url in values:
            try:
                records.append(registry_entry(origin, url, "python", option))
            except ValueError:
                records.append(local_entry(origin, "unparsed"))
    return [{**item, "section": section, "active": False} for item in records]


def activate_pip_profile(settings: dict, command: str) -> tuple:
    """Apply section and environment precedence, marking only effective sources as active."""
    effective = {}
    for section in ("global", command, ":env:"):
        effective.update({key: value for key, value in settings[section].items() if value[0]})
    no_index = effective.get("no-index", ("", []))[0].strip().lower() in PIP_TRUE
    signature = {}
    for option, (value, records) in effective.items():
        if option == "no-index" and value.strip().lower() in PIP_FALSE:
            continue
        if no_index and option in {"index-url", "extra-index-url"}:
            continue
        signature[option] = tuple(value.split())
        for item in records:
            item["active"] = True
    if not no_index:
        signature.setdefault("index-url", (DEFAULT_BASES["python"],))
    return tuple(sorted(signature.items()))


def pip_entries(
    environ: dict, home: Path, *, platform: str | None = None, prefix: Path | None = None
) -> list[dict]:
    """Resolve effective pip settings and expose command or interpreter ambiguities explicitly."""
    platform = sys.platform if platform is None else platform
    prefix = pip_site_prefix() if prefix is None else Path(prefix)
    entries: list[dict] = []
    settings = {section: {} for section in ("global", "install", "download", ":env:")}
    try:
        paths = pip_config_paths(environ, home, platform=platform, prefix=prefix)
    except (OSError, ValueError):
        paths = []
        entries.append({**local_entry("pip configuration paths", "unparsed"), "active": True})
    for path in paths:
        origin = display_path(path, home)
        parser = configparser.ConfigParser(interpolation=None)
        try:
            if not path.exists():
                continue
            parser.read_string(read_pip_config(path))
            for section in ("global", "install", "download"):
                if not parser.has_section(section):
                    continue
                for key, value in parser.items(section, raw=True):
                    option = key.replace("_", "-")
                    if option in PIP_OPTIONS:
                        records = pip_setting_entries(origin, section, option, value)
                        entries.extend(records)
                        settings[section][option] = (value, records)
        except (configparser.Error, UnicodeError, OSError):
            entries.append({**local_entry(origin, "unparsed"), "active": True})
    for variable, option in (
        ("PIP_INDEX_URL", "index-url"),
        ("PIP_EXTRA_INDEX_URL", "extra-index-url"),
        ("PIP_FIND_LINKS", "find-links"),
        ("PIP_NO_INDEX", "no-index"),
    ):
        if variable in environ:
            value = environ[variable]
            records = pip_setting_entries(f"${variable}", ":env:", option, value)
            entries.extend(records)
            settings[":env:"][option] = (value, records)
    install = activate_pip_profile(settings, "install")
    download = activate_pip_profile(settings, "download")
    if install != download:
        entries.append({**local_entry("pip install/download settings differ", "ambiguous"), "active": True})
    virtualenv = environ.get("VIRTUAL_ENV")
    if virtualenv and Path(virtualenv).resolve() != prefix.resolve():
        entries.append({**local_entry("$VIRTUAL_ENV differs from sys.prefix", "interpreter-mismatch"), "active": True})
    target_python = environ.get("PIP_PYTHON")
    if target_python and Path(target_python).resolve() not in {prefix.resolve(), Path(sys.executable).resolve()}:
        entries.append({**local_entry("$PIP_PYTHON selects another interpreter", "interpreter-mismatch"), "active": True})
    uv_default = environ.get("UV_DEFAULT_INDEX") or environ.get("UV_INDEX_URL")
    for variable, option in (
        ("UV_INDEX_URL", "index-url"),
        ("UV_DEFAULT_INDEX", "index-url"),
        ("UV_EXTRA_INDEX_URL", "extra-index-url"),
        ("UV_INDEX", "extra-index-url"),
    ):
        for value in environ.get(variable, "").split():
            name, _, url = value.partition("=")
            url = url if "://" in url and "://" not in name else value
            records = pip_setting_entries(f"${variable}", ":uv:", option, url)
            for item in records:
                item["active"] = option != "index-url" or value == uv_default
            entries.extend(records)
    if uv_default:
        pip_defaults = [dict(profile).get("index-url") for profile in (install, download)]
        pip_explicit = any(item.get("active") and item["option"] in {"index-url", "no-index"}
                           and item.get("section") != ":uv:" for item in entries)
        if pip_explicit and any(value != (uv_default,) for value in pip_defaults):
            entries.append({**local_entry("pip/uv default indexes differ", "ambiguous"), "active": True})
    return entries


def npm_entries(environ: dict, home: Path) -> tuple[list[dict], list[dict]]:
    """Read the user .npmrc (lower precedence) and npm registry environment overrides (higher)."""
    user = Path(
        environ.get("NPM_CONFIG_USERCONFIG")
        or environ.get("npm_config_userconfig")
        or home / ".npmrc"
    )
    try:
        files = npmrc_entries(user, display_path(user, home)) if user.is_file() else []
    except (OSError, ValueError):
        files = [local_entry(display_path(user, home), "unparsed")]
    variables = [
        registry_entry(f"${name}", environ[name], "javascript", "registry")
        for name in ("NPM_CONFIG_REGISTRY", "npm_config_registry")
        if environ.get(name)
    ]
    return files, variables


def cargo_entries(root: Path, environ: dict, home: Path) -> list[dict]:
    """Resolve crates-io source replacement across Cargo config files in increasing precedence."""
    cargo_home = Path(environ.get("CARGO_HOME") or home / ".cargo")
    candidates = [cargo_home / "config", cargo_home / "config.toml"]
    for directory in reversed([root, *root.parents]):
        candidates += [directory / ".cargo" / "config", directory / ".cargo" / "config.toml"]
    sources: dict[str, dict] = {}
    replacement, origin, seen = None, None, set()
    for path in candidates:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        try:
            with path.open("rb") as stream:
                data = tomllib.load(stream)
        except (OSError, ValueError):
            return [local_entry(display_path(path, home), "unparsed")]
        for name, table in data.get("source", {}).items():
            if not isinstance(table, dict):
                continue
            sources[name] = {**sources.get(name, {}), **table}
            if name == "crates-io" and table.get("replace-with"):
                replacement, origin = table["replace-with"], display_path(path, home)
    if not replacement:
        return []
    target = sources.get(replacement, {})
    if "registry" in target:
        return [registry_entry(origin, target["registry"], "rust", "replace-with")]
    option = next((key for key in ("local-registry", "directory") if key in target), "replace-with")
    return [local_entry(origin, option)]


def configured_registries(
    root: Path, lang: str, inventory: dict, environ: dict, home: Path
) -> list[dict]:
    """Merge user, project and environment registry settings in increasing precedence."""
    project = inventory.get("registries", [])
    if lang == "python":
        return [*pip_entries(environ, home), *project]
    if lang == "javascript":
        files, variables = npm_entries(environ, home)
        return [*files, *project, *variables]
    if lang == "rust":
        return cargo_entries(root, environ, home)
    return []


def select_base(
    lang: str, registry_base: str | None, mirror: str | None, entries: list[dict]
) -> tuple[str, str]:
    """Choose where to query: explicit base, mirror preset, configured public mirror, or default."""
    if registry_base:
        return registry_base, "--registry-base"
    if mirror:
        return MIRRORS[mirror][lang], f"--mirror {mirror}"
    usable = [
        entry
        for entry in entries
        if entry.get("active", True) and entry.get("base")
        and not entry.get("scope") and entry["option"] in BASE_OPTIONS
    ]
    if usable:
        return usable[-1]["base"], usable[-1]["origin"]
    return DEFAULT_BASES[lang], "default"


def custom_registry(name: str, lang: str, entries: list[dict]) -> dict | None:
    """Return the non-public registry setting that could serve this name, if any."""
    entries = [entry for entry in entries if entry.get("active", True)]
    if lang == "javascript":
        entry = npm_registry_for(name, entries)
        return entry if entry and not entry["public"] else None
    return next((entry for entry in entries if not entry["public"]), None)


def classify_item(
    item: dict, lang: str, entries: list[dict], public_registry: bool, offline: bool
) -> tuple[str, str]:
    """Decide whether one declaration can be checked against the selected public registry."""
    source = item["source"]
    if source in LOCAL_SOURCES:
        return "not_applicable", f"{source} dependency; validate with its resolver/build"
    if source != "registry" or lang not in DEFAULT_BASES:
        return "unresolved", "registry/source requires project-specific resolver metadata"
    custom = None if public_registry else custom_registry(item["name"], lang, entries)
    if custom:
        where = custom["host"] or custom["option"]
        return (
            "unresolved",
            f"configured registry {where} ({custom['origin']}) may serve this name; "
            "pass --public-registry if the public registry is authoritative",
        )
    if offline:
        return "not_checked", "offline mode"
    return "pending", ""


def absence_problem(lang: str, timeout: int, base: str) -> str | None:
    """Confirm a non-default registry answers 200 for a known name and 404 for a random one."""
    known = check_registry(CANARIES[lang], lang, timeout, base)
    absent = check_registry(f"codesift-absent-{secrets.token_hex(6)}", lang, timeout, base)
    if known[0] == "registry_match" and absent[0] == "not_found":
        return None
    host = urllib.parse.urlsplit(base).hostname
    return (
        f"{host} did not answer 200 for '{CANARIES[lang]}' and 404 for a random name; "
        "its absence answers are not trusted"
    )


def verify_inventory(
    inventory: dict,
    root: Path,
    offline: bool = False,
    public_registry: bool = False,
    max_checks: int = 100,
    timeout: int = 10,
    registry_base: str | None = None,
    mirror: str | None = None,
    environ: dict | None = None,
    home: Path | None = None,
) -> dict:
    """Deduplicate checks by source and expose offline, private, budget, mirror and network limits."""
    lang = inventory["language"]
    environ = dict(os.environ) if environ is None else environ
    home = Path.home() if home is None else home
    entries = configured_registries(root, lang, inventory, environ, home)
    warnings = [*inventory["warnings"], *(
        f"{entry['origin']}: registry configuration is {entry['option']}"
        for entry in entries
        if entry.get("active", True)
        and entry["option"] in {"unparsed", "ambiguous", "interpreter-mismatch"}
    )]
    base, selected_by = (
        select_base(lang, registry_base, mirror, entries)
        if lang in DEFAULT_BASES
        else (None, None)
    )
    results: list[dict] = []
    pending: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for item in inventory["direct"]:
        identity = (canonical_name(item["name"], lang), item["source"])
        if identity in seen:
            continue
        seen.add(identity)
        status, reason = classify_item(item, lang, entries, public_registry, offline)
        if status == "pending" and len(pending) >= max_checks:
            status, reason = "not_checked", "request budget exhausted"
        result = {"name": item["name"], "source": item["source"], "status": status, "reason": reason}
        results.append(result)
        if status == "pending":
            pending.append(result)
    outcomes = run_checks([r["name"] for r in pending], lang, timeout, base) if pending else []
    host = urllib.parse.urlsplit(base).hostname if base else None
    skipped = (
        "not_checked",
        f"skipped after {BREAKER} consecutive errors from {host}; "
        "try --mirror cn, --registry-base or --offline",
    )
    for result, outcome in zip(pending, outcomes):
        result["status"], result["reason"] = outcome or skipped
    if base and base != DEFAULT_BASES[lang] and any(r["status"] == "not_found" for r in results):
        problem = absence_problem(lang, timeout, base)
        for result in results:
            if result["status"] == "not_found":
                result["status"], result["reason"] = (
                    ("unresolved", problem)
                    if problem
                    else (
                        "mirror_not_found",
                        f"{result['reason']}; mirrors can lag the upstream registry, "
                        "so confirm on the upstream registry before treating it as missing",
                    )
                )
    incomplete = bool(
        inventory["errors"]
        or warnings
        or any(
            r["status"] in {"error", "not_checked", "unresolved", "mirror_not_found"}
            for r in results
        )
    )
    missing = any(r["status"] == "not_found" for r in results)
    return {
        "language": lang,
        "status": "failed" if missing else ("incomplete" if incomplete else "completed"),
        "complete": not incomplete,
        "checks_performed": sum(outcome is not None for outcome in outcomes),
        "registry": {"base": base, "selected_by": selected_by, "configured": entries},
        "results": results,
        "warnings": warnings,
        "errors": inventory["errors"],
        "evidence_scope": "public registry name existence only; not installed version, API or supply-chain safety",
    }


def registry_base_argument(value: str) -> str:
    """Accept an http(s) registry base without embedded credentials."""
    value = value.removeprefix("sparse+").rstrip("/")
    parts = urllib.parse.urlsplit(value)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise argparse.ArgumentTypeError("must be an http(s) URL")
    if parts.username or parts.password:
        raise argparse.ArgumentTypeError("must not contain credentials")
    return value


def main() -> int:
    """Run bounded registry checks without installing packages or executing project code."""
    parser = argparse.ArgumentParser(description=__doc__)
    add_project_arguments(parser)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--public-registry",
        action="store_true",
        help="confirm public registry is authoritative despite user-level registry settings",
    )
    parser.add_argument(
        "--mirror",
        choices=sorted(MIRRORS),
        help="query a public mirror preset; cn = TUNA (PyPI, crates.io index) and npmmirror",
    )
    parser.add_argument(
        "--registry-base",
        type=registry_base_argument,
        help="query this base: a PyPI simple index, an npm registry, or a Cargo sparse index URL",
    )
    parser.add_argument("--max-checks", type=positive_int, default=100)
    parser.add_argument("--timeout", type=positive_int, default=10)
    args = parser.parse_args()
    if args.mirror and args.registry_base:
        parser.error("choose either --mirror or --registry-base")
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    inventory = read_dependencies(root, select_language(root, args.lang))
    report = verify_inventory(
        inventory,
        root,
        args.offline,
        args.public_registry,
        args.max_checks,
        args.timeout,
        args.registry_base,
        args.mirror,
    )
    print_report(report, args.json)
    return 1 if report["status"] == "failed" else (0 if report["complete"] else 2)


if __name__ == "__main__":
    sys.exit(main())
