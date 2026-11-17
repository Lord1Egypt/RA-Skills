"""Parse dependency manifests centrally, preserving sources without executing build scripts."""

from __future__ import annotations

import ast
import configparser
import json
import re
import tomllib
import tokenize
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC_REGISTRY_HOSTS = {
    "python": frozenset(
        {
            "pypi.org",
            "pypi.python.org",
            "files.pythonhosted.org",
            "pypi.tuna.tsinghua.edu.cn",
            "mirrors.tuna.tsinghua.edu.cn",
            "mirrors.aliyun.com",
            "mirrors.cloud.tencent.com",
            "pypi.mirrors.ustc.edu.cn",
            "mirrors.ustc.edu.cn",
            "repo.huaweicloud.com",
            "mirrors.huaweicloud.com",
            "mirrors.bfsu.edu.cn",
            "mirror.sjtu.edu.cn",
            "mirrors.sjtug.sjtu.edu.cn",
            "mirrors.nju.edu.cn",
            "mirrors.cernet.edu.cn",
            "mirrors.163.com",
            "pypi.doubanio.com",
        }
    ),
    "javascript": frozenset(
        {
            "registry.npmjs.org",
            "registry.yarnpkg.com",
            "registry.npmmirror.com",
            "registry.npm.taobao.org",
            "mirrors.cloud.tencent.com",
            "repo.huaweicloud.com",
            "mirrors.huaweicloud.com",
        }
    ),
    "rust": frozenset(
        {
            "index.crates.io",
            "crates.io",
            "rsproxy.cn",
            "mirrors.ustc.edu.cn",
            "mirrors.tuna.tsinghua.edu.cn",
            "mirrors.bfsu.edu.cn",
            "mirror.sjtu.edu.cn",
            "mirrors.sjtug.sjtu.edu.cn",
            "mirrors.cernet.edu.cn",
            "mirrors.aliyun.com",
            "mirrors.nju.edu.cn",
        }
    ),
}
LOCAL_SOURCES = frozenset({"path", "git", "url", "git_or_url", "workspace"})
CREDENTIALS = re.compile(r"(?<=://)[^/@\s]+@")
PEP508_NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*(.*)$")
INLINE_COMMENT = re.compile(r"(?:^|\s)#")
PER_REQUIREMENT_OPTIONS = re.compile(
    r"\s--(?:hash|config-settings|global-option|install-option)(?:=|\s+)\S+"
)
PIP_OPTION = re.compile(r"^(-[A-Za-z]|--[a-z][a-z-]*)(?:\s*=\s*|\s+)?(.*)$")
DIRECT_REFERENCE = re.compile(r"^(?:[a-z][a-z0-9+.-]*://|(?:git|hg|svn|bzr)\+|file:|\.{1,2}(?:/|$)|/)")
HARMLESS_PIP_OPTIONS = frozenset(
    {
        "--pre",
        "--trusted-host",
        "--prefer-binary",
        "--only-binary",
        "--no-binary",
        "--use-feature",
        "--upgrade-strategy",
        "--require-hashes",
    }
)
PIP_INDEX_OPTIONS = {
    "-i": "index-url",
    "--index-url": "index-url",
    "--extra-index-url": "extra-index-url",
    "-f": "find-links",
    "--find-links": "find-links",
}
SETUP_GROUPS = {"install_requires": "runtime", "setup_requires": "build", "tests_require": "test"}
NPMRC_REGISTRY = re.compile(r"^\s*(?:(@[^:\s]+):)?registry\s*=\s*(\S+)")


def redact(value: object) -> object:
    """Hide URL user-info such as tokens before a declaration is copied into a report."""
    if isinstance(value, str):
        return CREDENTIALS.sub("***@", value)
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def registry_entry(
    origin: str,
    url: str,
    lang: str,
    option: str = "index",
    scope: str | None = None,
) -> dict:
    """Describe a configured registry by host only and classify known public mirrors.

    Public entries reachable over http(s) also carry a credential-free query base; for Cargo
    only sparse indexes qualify, because git indexes cannot be queried by path.
    """
    text = url.strip().strip("\"'")
    sparse = text.startswith("sparse+")
    for prefix in ("sparse+", "registry+", "git+"):
        text = text.removeprefix(prefix)
    parts = urlsplit(text)
    host = (parts.hostname or "").lower() or None
    public = host in PUBLIC_REGISTRY_HOSTS.get(lang, ()) and not (
        parts.username or parts.password
    )
    if lang == "rust" and host == "github.com":
        public = parts.path.rstrip("/").removesuffix(".git") == "/rust-lang/crates.io-index"
    entry = {"origin": origin, "option": option, "host": host, "public": public}
    if scope:
        entry["scope"] = scope
    if public and parts.scheme in {"http", "https"} and (lang != "rust" or sparse):
        entry["base"] = f"{parts.scheme}://{parts.netloc}{parts.path}".rstrip("/")
    return entry


def local_entry(origin: str, option: str) -> dict:
    """Describe a non-URL package source, such as --no-index or a vendored directory."""
    return {"origin": origin, "option": option, "host": None, "public": False}


def mark_private(records: list[dict], entries: list[dict]) -> None:
    """Treat default-registry records as private when their manifest adds a non-public index."""
    if any(not entry["public"] for entry in entries if not entry.get("explicit")):
        for record in records:
            if record["source"] == "registry":
                record["source"] = "private_registry"


def load_manifest(path: Path) -> dict:
    """Read declarative manifests and propagate errors instead of reporting zero dependencies."""
    if path.suffix == ".json":
        data = json.loads(path.read_bytes())
    else:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: expected an object")
    return data


def dependency(
    name: str,
    spec: object,
    manifest: Path,
    root: Path,
    group: str = "runtime",
    source: str = "registry",
) -> dict:
    """Build a traceable declaration record without inferring package existence from its version."""
    return {
        "name": name,
        "specifier": redact(spec),
        "source": source,
        "group": group,
        "manifest": manifest.relative_to(root).as_posix(),
    }


def cargo_manifests(root: Path, data: dict, warnings: list[str]) -> list[Path]:
    """Locate workspace members within the root and expose external or unmatched members."""
    workspace = data.get("workspace", {})
    manifests = {root / "Cargo.toml"}
    for pattern in workspace.get("members", []):
        if Path(pattern).is_absolute():
            raise ValueError("workspace member patterns must be relative")
        members = list(root.glob(pattern))
        if not members:
            warnings.append(f"workspace member pattern matched no paths: {pattern}")
        for member in members:
            resolved = member.resolve()
            if resolved.is_relative_to(root) and (resolved / "Cargo.toml").is_file():
                manifests.add(resolved / "Cargo.toml")
            else:
                warnings.append("workspace member outside root or without Cargo.toml")
    if workspace.get("exclude"):
        warnings.append(
            "workspace excludes require Cargo metadata to confirm active members"
        )
    return sorted(manifests)


def cargo_dependency(
    alias: str,
    raw: object,
    inherited: dict,
    manifest: Path,
    root: Path,
    group: str,
    warnings: list[str],
) -> dict:
    """Resolve one Cargo declaration while preserving inheritance, aliases, and source identity."""
    spec = raw
    if isinstance(spec, dict) and spec.get("workspace"):
        spec = inherited.get(alias)
        if spec is None:
            warnings.append(f"unresolved workspace dependency: {alias}")
            return dependency(alias, raw, manifest, root, group, "workspace")
    detail = spec if isinstance(spec, dict) else {}
    source = next(
        (key for key in ("path", "git", "registry") if key in detail), "registry"
    )
    if source == "registry" and detail.get("registry"):
        source = "private_registry"
    return dependency(detail.get("package", alias), spec, manifest, root, group, source)


def rust_dependencies(root: Path, found: dict) -> tuple[list[dict], list[str]]:
    """Collect Cargo package, target, development, and build declarations with shared parsing."""
    path = root / "Cargo.toml"
    data = load_manifest(path)
    inherited = data.get("workspace", {}).get("dependencies", {})
    manifests = cargo_manifests(root, data, found["warnings"])
    records: list[dict] = []
    for manifest in manifests:
        package = data if manifest == path else load_manifest(manifest)
        tables = [("", package)]
        tables.extend(
            (f"target:{target}/", table)
            for target, table in package.get("target", {}).items()
        )
        for prefix, table in tables:
            for key, group in (
                ("dependencies", "runtime"),
                ("dev-dependencies", "development"),
                ("build-dependencies", "build"),
            ):
                records.extend(
                    cargo_dependency(
                        alias,
                        raw,
                        inherited,
                        manifest,
                        root,
                        prefix + group,
                        found["warnings"],
                    )
                    for alias, raw in table.get(key, {}).items()
                )
        if package.get("patch") or package.get("replace"):
            found["warnings"].append(
                f"{manifest.relative_to(root)} has overrides; confirm resolved sources with Cargo metadata"
            )
    if not records and inherited:
        found["warnings"].append(
            "workspace dependency declarations alone do not prove member usage"
        )
    return records, [p.relative_to(root).as_posix() for p in manifests]


def python_requirement(raw: str, path: Path, root: Path, group: str) -> dict:
    """Extract a PEP 508 name, keep direct URL sources, and reject unsupported requirement text."""
    raw = INLINE_COMMENT.split(raw, maxsplit=1)[0].strip()
    match = PEP508_NAME.match(raw)
    if not match:
        raise ValueError(f"unsupported requirement {redact(raw)!r}")
    suffix = match.group(2)
    if suffix and not suffix.startswith(("@", ";", "<", ">", "=", "!", "~", "(")):
        raise ValueError(f"unsupported requirement syntax {redact(raw)!r}")
    source = "url" if suffix.startswith("@") else "registry"
    return dependency(match.group(1), raw, path, root, group, source)


def direct_reference(target: str) -> tuple[str, str]:
    """Name a URL, VCS or local-path requirement and classify its source without fetching it."""
    egg = re.search(r"[#&]egg=([A-Za-z0-9][A-Za-z0-9._-]*)", target)
    if re.match(r"(?:git|hg|svn|bzr)\+", target):
        source = "git"
    elif re.match(r"[a-z][a-z0-9+.-]*://", target, re.I) and not target.startswith("file:"):
        source = "url"
    else:
        source = "path"
    if egg:
        return egg.group(1), source
    tail = re.split(r"[?#]", target, maxsplit=1)[0].rstrip("/").rsplit("/", 1)[-1]
    tail = tail.split("@", 1)[0].removesuffix(".git")
    stem = re.split(r"-\d", tail, maxsplit=1)[0] if re.search(r"\.(?:whl|zip|tar\.gz)$", tail) else tail
    return (stem or str(redact(target))), source


def requirement_lines(text: str) -> list[tuple[int, str]]:
    """Join backslash continuations and drop comments; each logical line keeps its first number."""
    lines, buffer, first = [], [], 0
    for number, line in enumerate(text.splitlines(), 1):
        if not buffer:
            first = number
        content = line.rstrip()
        if content.endswith("\\"):
            buffer.append(content[:-1])
            continue
        buffer.append(content)
        joined = INLINE_COMMENT.split(" ".join(part.strip() for part in buffer), 1)[0]
        buffer = []
        if joined.strip():
            lines.append((first, joined.strip()))
    if buffer and " ".join(buffer).strip():
        lines.append((first, " ".join(part.strip() for part in buffer).strip()))
    return lines


def requirement_option(
    option: str,
    value: str,
    path: Path,
    root: Path,
    location: str,
    found: dict,
    seen: set[Path],
) -> list[dict]:
    """Interpret one pip option line: follow includes, record indexes, name editable targets."""
    if option in {"-r", "--requirement"}:
        include = (path.parent / value).resolve()
        if not include.is_relative_to(root) or not include.is_file():
            found["warnings"].append(
                f"{location}: include {value} is outside --root or missing; not expanded"
            )
            return []
        return requirements_file(include, root, found, seen)
    if option in {"-c", "--constraint"}:
        return []  # Constraints pin versions of packages declared elsewhere; they add none.
    if option in {"-e", "--editable"}:
        name, source = direct_reference(value)
        return [dependency(name, value, path, root, "requirements:editable", source)]
    if option in PIP_INDEX_OPTIONS:
        found["registries"].append(
            registry_entry(location, value, "python", PIP_INDEX_OPTIONS[option])
        )
    elif option == "--no-index":
        found["registries"].append(local_entry(location, "no-index"))
    elif option not in HARMLESS_PIP_OPTIONS:
        found["warnings"].append(f"{location}: option {option} not interpreted")
    return []


def requirements_file(
    path: Path, root: Path, found: dict, seen: set[Path]
) -> list[dict]:
    """Read one requirements file, following local -r includes, with per-line error locations."""
    resolved = path.resolve()
    if resolved in seen:
        return []
    seen.add(resolved)
    relative = resolved.relative_to(root).as_posix()
    group = "requirements" if relative == "requirements.txt" else f"requirements:{relative}"
    records = []
    with tokenize.open(resolved) as stream:
        text = stream.read()
    for number, line in requirement_lines(text):
        location = f"{relative}:{number}"
        hashed = "--hash" in line
        line = PER_REQUIREMENT_OPTIONS.sub("", f" {line}").strip()
        option = PIP_OPTION.match(line)
        if option:
            records.extend(
                requirement_option(
                    option.group(1), option.group(2).strip(), resolved, root, location, found, seen
                )
            )
            continue
        try:
            if DIRECT_REFERENCE.match(line):
                name, source = direct_reference(line)
                record = dependency(name, line, resolved, root, group, source)
            else:
                record = python_requirement(line, resolved, root, group)
        except ValueError as error:
            found["errors"].append(f"{location}: {error}")
            continue
        if hashed:
            record["hash_pinned"] = True
        records.append(record)
    return records


def requirement_files(root: Path) -> list[Path]:
    """Find conventional requirements files at the package root."""
    patterns = ("requirements*.txt", "*-requirements.txt", "requirements/*.txt")
    return sorted({path for pattern in patterns for path in root.glob(pattern) if path.is_file()})


def requirement_list(
    values: list, path: Path, root: Path, group: str, found: dict
) -> list[dict]:
    """Parse a list of requirement strings, recording invalid entries without dropping the rest."""
    records = []
    for raw in values:
        if not isinstance(raw, str):
            raise ValueError(f"{path.name}: invalid requirement in {group}")
        if not raw.strip():
            continue
        try:
            records.append(python_requirement(raw, path, root, group))
        except ValueError as error:
            found["errors"].append(f"{path.name} [{group}]: {error}")
    return records


def python_project_groups(data: dict, path: Path, root: Path, found: dict) -> list[dict]:
    """Read declarative pyproject groups and expose unresolved dynamic or included declarations."""
    project = data.get("project", {})
    groups = {"runtime": project.get("dependencies", [])}
    groups.update(
        {
            f"optional:{k}": v
            for k, v in project.get("optional-dependencies", {}).items()
        }
    )
    groups.update(
        {f"development:{k}": v for k, v in data.get("dependency-groups", {}).items()}
    )
    records = []
    for group, values in groups.items():
        if not isinstance(values, list):
            raise ValueError(f"{path.name}: dependency group {group} must be an array")
        if group.startswith("development:"):
            included = [raw for raw in values if isinstance(raw, dict) and "include-group" in raw]
            if included:
                found["warnings"].append(f"unresolved dependency-group inclusion: {group}")
            values = [raw for raw in values if raw not in included]
        records.extend(requirement_list(values, path, root, group, found))
    if set(project.get("dynamic", [])) & {"dependencies", "optional-dependencies"}:
        found["warnings"].append("dynamic Python dependencies require build-backend metadata")
    return records


def apply_uv_sources(records: list[dict], data: dict, path: Path, found: dict) -> None:
    """Apply uv sources and indexes so workspace, path, git and index-pinned names stay local."""
    uv = data.get("tool", {}).get("uv", {})
    sources = {
        canonical_name(name, "python"): spec for name, spec in uv.get("sources", {}).items()
    }
    kinds = (
        ("workspace", "workspace"),
        ("path", "path"),
        ("git", "git"),
        ("url", "url"),
        ("index", "private_registry"),
    )
    for record in records:
        spec = sources.get(canonical_name(record["name"], "python"))
        if isinstance(spec, list):
            spec = spec[0] if spec else None
        if isinstance(spec, dict):
            record["source"] = next(
                (kind for key, kind in kinds if key in spec), record["source"]
            )
    entries = []
    for index in uv.get("index", []):
        if isinstance(index, dict) and index.get("url"):
            entry = registry_entry(f"{path.name} [tool.uv.index]", index["url"], "python")
            if index.get("explicit"):
                entry["explicit"] = True
            entries.append(entry)
    for key, option in (("index-url", "index-url"), ("extra-index-url", "extra-index-url")):
        values = uv.get(key, [])
        for url in [values] if isinstance(values, str) else values:
            entries.append(registry_entry(f"{path.name} [tool.uv]", url, "python", option))
    found["registries"].extend(entries)
    mark_private(records, entries)
    if uv.get("workspace"):
        found["warnings"].append(
            "uv workspace members need separate --root audits or uv metadata"
        )


def poetry_dependencies(poetry: dict, path: Path, root: Path, found: dict) -> list[dict]:
    """Read Poetry groups without assuming public PyPI is authoritative for custom sources."""
    groups = {"runtime": poetry.get("dependencies", {})}
    groups.update(
        {
            f"development:{k}": v.get("dependencies", {})
            for k, v in poetry.get("group", {}).items()
        }
    )
    if poetry.get("dev-dependencies"):
        groups["development:legacy"] = poetry["dev-dependencies"]
    entries = []
    for item in poetry.get("source", []):
        if isinstance(item, dict):
            entry = registry_entry(
                f"{path.name} [tool.poetry.source]", item.get("url", ""), "python"
            )
            if item.get("priority") == "explicit":
                entry["explicit"] = True
            entries.append(entry)
    found["registries"].extend(entries)
    records = []
    for group, items in groups.items():
        for name, spec in items.items():
            if name.lower() == "python":
                continue
            source = "registry"
            if isinstance(spec, dict):
                source = next(
                    (k for k in ("path", "git", "url") if k in spec),
                    "private_registry" if "source" in spec else source,
                )
            records.append(dependency(name, spec, path, root, group, source))
    mark_private(records, entries)
    return records


def pipfile_dependencies(path: Path, root: Path, found: dict) -> list[dict]:
    """Read Pipfile packages and sources declaratively, without running pipenv."""
    data = load_manifest(path)
    public_sources, entries = {}, []
    for item in data.get("source", []):
        if isinstance(item, dict):
            entry = registry_entry(f"{path.name} [[source]]", item.get("url", ""), "python")
            public_sources[item.get("name")] = entry["public"]
            entries.append(entry)
    found["registries"].extend(entries)
    records = []
    for key, group in (("packages", "runtime"), ("dev-packages", "development")):
        for name, spec in data.get(key, {}).items():
            source = "registry"
            if isinstance(spec, dict):
                source = next(
                    (kind for field, kind in (("path", "path"), ("file", "url"), ("git", "git")) if field in spec),
                    source,
                )
                if "index" in spec and not public_sources.get(spec["index"], False):
                    source = "private_registry"
            records.append(dependency(name, spec, path, root, group, source))
    mark_private(records, entries)
    return records


def setup_cfg_dependencies(path: Path, root: Path, found: dict) -> list[dict]:
    """Read declarative setup.cfg requirements without executing setuptools."""
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(path.read_text(encoding="utf-8-sig"))
    groups = {
        group: parser.get("options", key)
        for key, group in SETUP_GROUPS.items()
        if parser.has_option("options", key)
    }
    if parser.has_section("options.extras_require"):
        groups.update(
            {
                f"optional:{extra}": value
                for extra, value in parser.items("options.extras_require")
            }
        )
    records = []
    for group, value in groups.items():
        if value.strip().startswith("file:"):
            found["warnings"].append(f"setup.cfg {group} uses a file: directive; not expanded")
            continue
        lines = [INLINE_COMMENT.split(line, 1)[0] for line in value.splitlines()]
        records.extend(requirement_list(lines, path, root, group, found))
    return records


def setup_dependencies(path: Path, root: Path, found: dict) -> list[dict]:
    """Extract literal setup() requirement arguments without executing setup.py."""
    tree = ast.parse(path.read_bytes(), filename=str(path))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id == "setup")
            or (isinstance(node.func, ast.Attribute) and node.func.attr == "setup")
        )
    ]
    if not calls:
        found["warnings"].append(
            "setup.py has no literal setup() call; dependencies not statically resolved"
        )
        return []
    records = []
    for keyword in (item for call in calls for item in call.keywords):
        if keyword.arg is None:
            found["warnings"].append(
                "setup.py passes **kwargs to setup(); dependencies not statically resolved"
            )
            continue
        if keyword.arg not in SETUP_GROUPS and keyword.arg != "extras_require":
            continue
        try:
            values = ast.literal_eval(keyword.value)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            found["warnings"].append(f"setup.py {keyword.arg} is dynamic; not executed")
            continue
        if keyword.arg == "extras_require":
            if not isinstance(values, dict):
                raise ValueError("setup.py extras_require must be a literal dict")
            groups = {f"optional:{extra}": items for extra, items in values.items()}
        else:
            groups = {SETUP_GROUPS[keyword.arg]: values}
        for group, items in groups.items():
            if isinstance(items, str):
                items = items.splitlines()
            if not isinstance(items, (list, tuple)):
                raise ValueError("setup.py requirements must be literal lists/tuples")
            records.extend(requirement_list(list(items), path, root, group, found))
    return records


def python_dependencies(root: Path, found: dict) -> tuple[list[dict], list[str]]:
    """Combine every Python manifest at the package root using a focused parser for each format."""
    records: list[dict] = []
    manifests: list[str] = []
    path = root / "pyproject.toml"
    if path.is_file():
        data = load_manifest(path)
        manifests.append(path.name)
        project = python_project_groups(data, path, root, found)
        apply_uv_sources(project, data, path, found)
        records.extend(project)
        records.extend(
            poetry_dependencies(data.get("tool", {}).get("poetry", {}), path, root, found)
        )
    seen: set[Path] = set()
    start = len(found["registries"])
    requirements = []
    for path in requirement_files(root):
        requirements.extend(requirements_file(path, root, found, seen))
    # pip applies index options from any requirements file to the whole installation.
    mark_private(requirements, found["registries"][start:])
    records.extend(requirements)
    manifests.extend(sorted(p.relative_to(root).as_posix() for p in seen))
    for name, reader in (
        ("setup.cfg", setup_cfg_dependencies),
        ("setup.py", setup_dependencies),
        ("Pipfile", pipfile_dependencies),
    ):
        path = root / name
        if path.is_file():
            manifests.append(name)
            records.extend(reader(path, root, found))
    return records, manifests


def npmrc_entries(path: Path, origin: str) -> list[dict]:
    """Read registry lines from an .npmrc file by scope, keeping hosts and dropping tokens."""
    entries = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        match = NPMRC_REGISTRY.match(line)
        if match:
            entries.append(
                registry_entry(
                    f"{origin}:{number}", match.group(2), "javascript", "registry", match.group(1)
                )
            )
    return entries


def npm_registry_for(name: str, entries: list[dict]) -> dict | None:
    """Return the configured entry npm would use for a package; later entries take precedence."""
    scope = name.split("/", 1)[0] if name.startswith("@") else None
    scoped = [entry for entry in entries if scope and entry.get("scope") == scope]
    candidates = scoped or [entry for entry in entries if not entry.get("scope")]
    return candidates[-1] if candidates else None


def javascript_dependencies(root: Path, found: dict) -> tuple[list[dict], list[str]]:
    """Resolve npm aliases, local sources and scoped registries for one package root."""
    path = root / "package.json"
    data = load_manifest(path)
    records: list[dict] = []
    entries = npmrc_entries(root / ".npmrc", ".npmrc") if (root / ".npmrc").is_file() else []
    yarnrc = root / ".yarnrc.yml"
    if yarnrc.is_file():
        match = re.search(
            r"(?m)^npmRegistryServer:\s*[\"']?([^\"'\s]+)",
            yarnrc.read_text(encoding="utf-8-sig"),
        )
        if match:
            entries.append(registry_entry(".yarnrc.yml", match.group(1), "javascript", "registry"))
    found["registries"].extend(entries)
    for key, group in (
        ("dependencies", "runtime"),
        ("devDependencies", "development"),
        ("optionalDependencies", "optional"),
        ("peerDependencies", "peer"),
    ):
        for alias, spec in data.get(key, {}).items():
            if not isinstance(spec, str):
                raise ValueError(f"package.json: invalid specifier for {alias}")
            name, source = alias, "registry"
            if spec.startswith("npm:"):
                name = spec[4:].rsplit("@", 1)[0] if "@" in spec[5:] else spec[4:]
                if not name:
                    raise ValueError("package.json: empty npm alias")
            elif spec.startswith(
                ("workspace:", "catalog:", "file:", "link:", ".", "/")
            ):
                source = (
                    "workspace"
                    if spec.startswith(("workspace:", "catalog:"))
                    else "path"
                )
            elif (
                re.match(r"(?:git|https?|ssh|github|gitlab|bitbucket)[+:]", spec)
                or "/" in spec
            ):
                source = "git_or_url"
            if source == "registry":
                entry = npm_registry_for(name, entries)
                if entry and not entry["public"]:
                    source = "private_registry"
            records.append(dependency(name, spec, path, root, group, source))
    workspace_files = [
        name for name in ("pnpm-workspace.yaml", "lerna.json") if (root / name).is_file()
    ]
    if data.get("workspaces") or workspace_files:
        found["warnings"].append(
            "workspace members need separate --root audits or package-manager metadata"
        )
    return records, [path.name, *workspace_files]


def conan_requirements(path: Path, root: Path) -> list[dict]:
    """Read only the requires section of conanfile.txt as dependency declarations."""
    records = []
    active = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        value = line.strip()
        if value.startswith("["):
            active = value == "[requires]"
        elif active and value and not value.startswith("#"):
            records.append(
                dependency(value.split("/", 1)[0], value, path, root, source="conan")
            )
    return records


def native_dependencies(root: Path, found: dict) -> tuple[list[dict], list[str]]:
    """Read explicit native manifests without guessing public package names from CMake labels."""
    warnings = found["warnings"]
    records: list[dict] = []
    manifests: list[str] = []
    vcpkg = root / "vcpkg.json"
    if vcpkg.is_file():
        data = load_manifest(vcpkg)
        manifests.append(vcpkg.name)
        for item in data.get("dependencies", []):
            name = item if isinstance(item, str) else item["name"]
            records.append(dependency(name, item, vcpkg, root, source="vcpkg"))
        if data.get("features"):
            warnings.append("vcpkg optional features require active-feature resolution")
    conan = root / "conanfile.txt"
    if conan.is_file():
        manifests.append(conan.name)
        records.extend(conan_requirements(conan, root))
    if (root / "conanfile.py").is_file():
        manifests.append("conanfile.py")
        warnings.append("executable conanfile.py requires Conan metadata; not executed")
    for name in ("CMakeLists.txt", "meson.build", "Makefile", "makefile"):
        if (root / name).is_file():
            if name == "CMakeLists.txt":
                (root / name).read_text(encoding="utf-8-sig")
            manifests.append(name)
            warnings.append(
                f"{name} is executable build logic; dependency resolution not inferred by regex"
            )
    warnings.append(
        "native dependency inventory is best-effort; system/private registries are not resolved"
    )
    return records, manifests


def canonical_name(name: str, lang: str) -> str:
    """Normalize package identity consistently for inventory counts and registry deduplication."""
    return (re.sub(r"[-_.]+", "-", name) if lang == "python" else name).casefold()


READERS = {
    "rust": rust_dependencies,
    "python": python_dependencies,
    "javascript": javascript_dependencies,
    "c": native_dependencies,
    "cpp": native_dependencies,
}


def read_dependencies(root: Path, lang: str) -> dict:
    """Collect declarations and coverage limits without running package managers or writing locks."""
    root = root.resolve()
    result = {
        "language": lang,
        "direct": [],
        "count": 0,
        "manifests": [],
        "registries": [],
        "warnings": [],
        "errors": [],
        "scope": "declared dependencies, not usage or installed graph",
    }
    if lang not in READERS:
        result["errors"].append(
            "choose --lang and a package --root for unknown/mixed projects"
            if lang in {"mixed", "unknown", "auto"}
            else f"no dependency reader for {lang}; inspect its manifests with the native toolchain"
        )
        return result
    try:
        records, manifests = READERS[lang](root, result)
        result["direct"] = records
        result["manifests"] = manifests
        identities = {(canonical_name(r["name"], lang), r["source"]) for r in records}
        result["count"] = len(identities)
        if not manifests:
            result["errors"].append("no supported dependency manifest found")
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        SyntaxError,
        configparser.Error,
    ) as error:
        result["errors"].append(
            f"manifest parsing failed: {type(error).__name__}: {error}"
        )
    return result
