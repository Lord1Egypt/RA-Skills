"""Dependency file parser for /depradar.

Supports: package.json, requirements.txt, pyproject.toml, Pipfile,
          setup.cfg, go.mod, Cargo.toml, Gemfile, pom.xml

Lock file support (exact installed versions):
          package-lock.json, yarn.lock, pnpm-lock.yaml
"""

from __future__ import annotations

import configparser
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from schema import DepInfo
from semver import extract_numeric


# ── Filename → ecosystem mapping ─────────────────────────────────────────────

_ECOSYSTEM_MAP: Dict[str, str] = {
    "package.json":       "npm",
    "requirements.txt":   "pypi",
    "pyproject.toml":     "pypi",
    "Pipfile":            "pypi",
    "setup.cfg":          "pypi",
    "go.mod":             "go",
    "Cargo.toml":         "cargo",
    "Gemfile":            "gem",
    "pom.xml":            "maven",
}

_DEP_FILENAMES: List[str] = list(_ECOSYSTEM_MAP.keys())

# Lock files — supplementary (not primary dep files, used for exact version resolution)
_LOCK_FILENAMES: List[str] = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"]


# ── Public API ────────────────────────────────────────────────────────────────

def detect_ecosystem(path: str) -> str:
    """Return ecosystem name from filename."""
    name = os.path.basename(path)
    return _ECOSYSTEM_MAP.get(name, "unknown")


def find_dep_files(project_root: str) -> List[str]:
    """Walk up from project_root to git root, collect all dep files found.

    Starts at project_root, walks up until a .git directory is found or the
    filesystem root is reached.  Collects every recognised dependency file.
    """
    found: List[str] = []
    visited: set = set()

    root = Path(project_root).resolve()

    # Determine the git root (upper boundary)
    git_root = _find_git_root(root)
    if git_root is None:
        git_root = root  # no git repo — search only in project_root

    # Walk from git_root down, but only collect inside project_root and parents
    # up to git_root.  Collect by walking from root upward to git_root.
    current = root
    while True:
        for fname in _DEP_FILENAMES:
            candidate = current / fname
            if candidate.is_file() and str(candidate) not in visited:
                found.append(str(candidate))
                visited.add(str(candidate))
        if current == git_root:
            break
        parent = current.parent
        if parent == current:
            break
        current = parent

    # Also do a downward walk from project_root (for monorepos)
    depth_warnings: List[str] = []
    _collect_below(root, found, visited, max_depth=5, depth_warnings=depth_warnings)

    return found, depth_warnings


def parse_all(
    dep_files: List[str], include_dev: bool = False
) -> Tuple[Dict[str, DepInfo], List[str]]:
    """Parse all files, return (merged_dict, errors).

    Workspace-safe: when the same package appears in multiple sub-projects,
    all versions are accumulated in DepInfo.workspace_versions instead of
    last-file-wins overwriting. The primary version is the first one seen.
    """
    result: Dict[str, DepInfo] = {}
    errors: List[str] = []
    parsers = {
        "package.json":     lambda p: parse_package_json(p, include_dev=include_dev),
        "requirements.txt": parse_requirements_txt,
        "pyproject.toml":   parse_pyproject_toml,
        "Pipfile":          parse_pipfile,
        "setup.cfg":        lambda p: parse_setup_cfg(p, include_dev=include_dev),
        "go.mod":           parse_go_mod,
        "Cargo.toml":       parse_cargo_toml,
        "Gemfile":          parse_gemfile,
        "pom.xml":          parse_pom_xml,
    }
    for path in dep_files:
        fname = os.path.basename(path)
        parser = parsers.get(fname)
        if parser is None:
            continue
        try:
            deps = parser(path)
        except Exception as exc:
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
            continue
        for name, info in deps.items():
            if name in result:
                # Accumulate workspace version instead of overwriting
                result[name].workspace_versions[path] = info.version
            else:
                result[name] = info
                result[name].workspace_versions = {path: info.version}
    return result, errors


# ── Per-format parsers ────────────────────────────────────────────────────────

def parse_package_json(path: str, include_dev: bool = False) -> Dict[str, DepInfo]:
    """Parse npm/yarn package.json, preferring exact versions from lock files."""
    import json as _json
    result: Dict[str, DepInfo] = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        data = _json.load(fh)

    source = os.path.basename(path)

    def _add(name: str, spec: str, is_dev: bool) -> None:
        numeric = extract_numeric(spec) or spec
        result[name] = DepInfo(
            name=name,
            version_spec=spec,
            version=numeric,
            ecosystem="npm",
            source_file=source,
            is_dev=is_dev,
        )

    for name, spec in (data.get("dependencies") or {}).items():
        _add(name, str(spec), False)
    if include_dev:
        for name, spec in (data.get("devDependencies") or {}).items():
            _add(name, str(spec), True)
    # peerDependencies are runtime requirements — include always
    for name, spec in (data.get("peerDependencies") or {}).items():
        if name not in result:
            _add(name, str(spec), False)

    # Prefer exact installed versions from lock files (more accurate than ^x.y.z)
    lock_versions = _read_lock_file(Path(path).parent)
    for name, dep_info in result.items():
        if name in lock_versions:
            dep_info.version = lock_versions[name]

    return result


def parse_requirements_txt(path: str) -> Dict[str, DepInfo]:
    """Parse pip requirements.txt.

    Handles: pkg==1.2.3, pkg>=1.0,<2.0, pkg~=1.4, pkg (no version),
             -r other.txt (ignored), # comments, extras pkg[extra]==1.0.
    """
    result: Dict[str, DepInfo] = {}
    source = os.path.basename(path)

    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        # Strip inline comment
        line = re.split(r"\s+#", line)[0].strip()
        # Package name (with optional extras)
        m = re.match(r"^([A-Za-z0-9_\-\.]+)(\[.*?\])?\s*([><=!~,\s0-9\.\*\+]+)?", line)
        if not m:
            continue
        name = m.group(1).strip()
        spec_raw = (m.group(3) or "").strip()
        # Normalise: keep first specifier for numeric extraction
        spec = spec_raw if spec_raw else "*"
        numeric = extract_numeric(spec) or ""
        result[name] = DepInfo(
            name=name,
            version_spec=spec,
            version=numeric,
            ecosystem="pypi",
            source_file=source,
        )
    return result


def parse_pyproject_toml(path: str) -> Dict[str, DepInfo]:
    """Parse PEP 621 pyproject.toml [project].dependencies."""
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}

    text = Path(path).read_text(encoding="utf-8", errors="replace")
    data = _load_toml(text)

    deps: List[str] = []
    if data:
        project = data.get("project", {})
        deps = project.get("dependencies", [])
        # Also handle [tool.poetry.dependencies]
        if not deps:
            tool = data.get("tool", {})
            poetry = tool.get("poetry", {})
            raw_poetry_deps = poetry.get("dependencies", {})
            for name, spec_val in raw_poetry_deps.items():
                if name.lower() in ("python",):
                    continue
                if isinstance(spec_val, dict):
                    spec = spec_val.get("version", "*")
                else:
                    spec = str(spec_val)
                numeric = extract_numeric(spec) or ""
                result[name] = DepInfo(
                    name=name,
                    version_spec=spec,
                    version=numeric,
                    ecosystem="pypi",
                    source_file=source,
                )
    else:
        # Regex fallback for [project].dependencies array
        deps = _regex_toml_array(text, "project", "dependencies")

    for dep_str in deps:
        dep_str = dep_str.strip().strip('"').strip("'")
        if not dep_str:
            continue
        m = re.match(r"^([A-Za-z0-9_\-\.]+)(\[.*?\])?\s*([><=!~,\s0-9\.\*]+)?", dep_str)
        if not m:
            continue
        name = m.group(1).strip()
        spec = (m.group(3) or "").strip() or "*"
        numeric = extract_numeric(spec) or ""
        result[name] = DepInfo(
            name=name,
            version_spec=spec,
            version=numeric,
            ecosystem="pypi",
            source_file=source,
        )
    return result


def parse_pipfile(path: str) -> Dict[str, DepInfo]:
    """Parse Pipfile [packages] section."""
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}
    text = Path(path).read_text(encoding="utf-8", errors="replace")

    data = _load_toml(text)
    if data:
        for section in ("packages", "dev-packages"):
            is_dev = section == "dev-packages"
            for name, spec_val in (data.get(section) or {}).items():
                if isinstance(spec_val, dict):
                    spec = spec_val.get("version", "*")
                elif spec_val == "*":
                    spec = "*"
                else:
                    spec = str(spec_val)
                numeric = extract_numeric(spec) or ""
                result[name] = DepInfo(
                    name=name,
                    version_spec=spec,
                    version=numeric,
                    ecosystem="pypi",
                    source_file=source,
                    is_dev=is_dev,
                )
    else:
        # Regex fallback: parse [packages] section line by line
        in_packages = False
        for line in text.splitlines():
            stripped = line.strip()
            if re.match(r"^\[packages\]", stripped):
                in_packages = True
                continue
            if re.match(r"^\[", stripped) and not re.match(r"^\[packages\]", stripped):
                in_packages = False
                continue
            if in_packages and "=" in stripped and not stripped.startswith("#"):
                name, _, spec_raw = stripped.partition("=")
                name = name.strip()
                spec = spec_raw.strip().strip('"').strip("'") or "*"
                numeric = extract_numeric(spec) or ""
                result[name] = DepInfo(
                    name=name,
                    version_spec=spec,
                    version=numeric,
                    ecosystem="pypi",
                    source_file=source,
                )
    return result


def parse_go_mod(path: str) -> Dict[str, DepInfo]:
    """Parse go.mod require block.

    Handles single-line: require example.com/pkg v1.2.3
    And block:
        require (
            example.com/pkg v1.2.3
        )
    """
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}

    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    # Remove // comments
    text_no_comments = re.sub(r"//[^\n]*", "", text)

    # Block requires
    block_re = re.compile(r"require\s*\(([^)]*)\)", re.DOTALL)
    for block_match in block_re.finditer(text_no_comments):
        block = block_match.group(1)
        for line in block.splitlines():
            _parse_go_require_line(line.strip(), source, result)

    # Single-line requires
    single_re = re.compile(r"^require\s+(\S+)\s+(\S+)", re.MULTILINE)
    for m in single_re.finditer(text_no_comments):
        module_path = m.group(1)
        version_str = m.group(2)
        _add_go_dep(module_path, version_str, source, result)

    return result


def parse_cargo_toml(path: str) -> Dict[str, DepInfo]:
    """Parse Cargo.toml [dependencies] and [dev-dependencies]."""
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}
    text = Path(path).read_text(encoding="utf-8", errors="replace")

    data = _load_toml(text)
    if data:
        for section in ("dependencies", "dev-dependencies", "build-dependencies"):
            is_dev = section != "dependencies"
            for name, spec_val in (data.get(section) or {}).items():
                if isinstance(spec_val, dict):
                    spec = spec_val.get("version", "*")
                    if spec is None:
                        spec = "*"
                elif isinstance(spec_val, str):
                    spec = spec_val
                else:
                    spec = str(spec_val)
                numeric = extract_numeric(spec) or ""
                result[name] = DepInfo(
                    name=name,
                    version_spec=spec,
                    version=numeric,
                    ecosystem="cargo",
                    source_file=source,
                    is_dev=is_dev,
                )
    else:
        # Regex fallback: parse sections line by line
        current_section = ""
        for line in text.splitlines():
            stripped = line.strip()
            sec_m = re.match(r"^\[(.*?)\]", stripped)
            if sec_m:
                current_section = sec_m.group(1).strip()
                continue
            if current_section in ("dependencies", "dev-dependencies", "build-dependencies"):
                if "=" in stripped and not stripped.startswith("#"):
                    is_dev = current_section != "dependencies"
                    name, _, rest = stripped.partition("=")
                    name = name.strip()
                    rest = rest.strip()
                    # Could be: name = "1.2.3" or name = { version = "1.2.3" }
                    ver_m = re.search(r'"([^"]+)"', rest)
                    spec = ver_m.group(1) if ver_m else "*"
                    numeric = extract_numeric(spec) or ""
                    result[name] = DepInfo(
                        name=name,
                        version_spec=spec,
                        version=numeric,
                        ecosystem="cargo",
                        source_file=source,
                        is_dev=is_dev,
                    )
    return result


def parse_gemfile(path: str) -> Dict[str, DepInfo]:
    """Parse Ruby Gemfile gem declarations.

    Handles:
        gem 'rails', '~> 7.0'
        gem 'nokogiri'
        gem "pg", ">= 0.18", "< 2.0"
    """
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}

    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # gem 'name', 'version_spec'
        m = re.match(r"""^gem\s+['"]([^'"]+)['"]\s*(?:,\s*['"]([^'"]+)['"])?""", line)
        if not m:
            continue
        name = m.group(1).strip()
        spec = m.group(2).strip() if m.group(2) else "*"
        numeric = extract_numeric(spec) or ""
        result[name] = DepInfo(
            name=name,
            version_spec=spec,
            version=numeric,
            ecosystem="gem",
            source_file=source,
        )
    return result


def parse_pom_xml(path: str) -> Dict[str, DepInfo]:
    """Parse Maven pom.xml <dependencies> block.

    Uses defusedxml when available to prevent XXE attacks; falls back to
    stdlib xml.etree.ElementTree which is safe for local trusted files but
    lacks full XXE protection against adversarially crafted XML.
    """
    # Prefer defusedxml for XXE protection
    try:
        import defusedxml.ElementTree as ET  # type: ignore[import]
    except ImportError:
        import xml.etree.ElementTree as ET  # type: ignore[assignment]

    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}

    try:
        tree = ET.parse(path)
    except Exception:
        return result

    root_elem = tree.getroot()

    # Handle namespace (Maven pom.xml uses xmlns)
    ns_m = re.match(r"\{([^}]+)\}", root_elem.tag)
    ns = f"{{{ns_m.group(1)}}}" if ns_m else ""

    # Collect properties for variable substitution
    props: Dict[str, str] = {}
    props_elem = root_elem.find(f"{ns}properties")
    if props_elem is not None:
        for child in props_elem:
            tag = child.tag.replace(ns, "")
            if child.text:
                props[tag] = child.text.strip()

    def _resolve(val: str) -> str:
        """Replace ${prop.name} with value from properties."""
        def replacer(m: re.Match) -> str:
            return props.get(m.group(1), m.group(0))
        return re.sub(r"\$\{([^}]+)\}", replacer, val)

    # Find all <dependency> elements (both direct and in dependencyManagement)
    for dep in root_elem.iter(f"{ns}dependency"):
        group_id_el  = dep.find(f"{ns}groupId")
        artifact_el  = dep.find(f"{ns}artifactId")
        version_el   = dep.find(f"{ns}version")
        scope_el     = dep.find(f"{ns}scope")

        if group_id_el is None or artifact_el is None:
            continue

        group_id   = _resolve((group_id_el.text or "").strip())
        artifact   = _resolve((artifact_el.text or "").strip())
        version    = _resolve((version_el.text or "").strip()) if version_el is not None else ""
        scope      = ((scope_el.text or "compile") if scope_el is not None else "compile").strip().lower()

        name = f"{group_id}:{artifact}"
        spec = version or "*"
        numeric = extract_numeric(spec) or ""
        is_dev = scope in ("test", "provided")

        result[name] = DepInfo(
            name=name,
            version_spec=spec,
            version=numeric,
            ecosystem="maven",
            source_file=source,
            is_dev=is_dev,
        )
    return result


# ── Internal helpers ──────────────────────────────────────────────────────────

def _find_git_root(start: Path) -> Optional[Path]:
    """Walk up from start until .git is found. Returns that directory or None."""
    current = start
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


_SKIP_DIRS = frozenset({
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", "target", ".cache", ".next", ".nuxt", "vendor",
    "third_party", ".tox", ".mypy_cache", ".pytest_cache",
})


def _collect_below(
    root: Path,
    found: List[str],
    visited: set,
    max_depth: int = 5,
    current_depth: int = 0,
    depth_warnings: Optional[List[str]] = None,
) -> None:
    """Recursively collect dep files below root, up to max_depth levels.

    When dep files are found exactly AT the boundary depth, a warning is added
    so users know to increase --depth if they have deeper monorepo structures.
    """
    if current_depth > max_depth:
        return
    try:
        entries = list(root.iterdir())
    except PermissionError:
        return
    for entry in entries:
        if entry.is_dir():
            if entry.name in _SKIP_DIRS:
                continue
            if current_depth == max_depth:
                # At boundary — check one level deeper and warn if dep files exist
                if depth_warnings is not None:
                    for fname in _DEP_FILENAMES:
                        candidate = entry / fname
                        if candidate.exists():
                            depth_warnings.append(
                                f"Dep file found beyond scan depth ({max_depth}): "
                                f"{candidate} — use a higher depth setting to include it"
                            )
            else:
                _collect_below(entry, found, visited, max_depth, current_depth + 1,
                                depth_warnings)
        elif entry.is_file():
            if entry.name in _DEP_FILENAMES and str(entry) not in visited:
                found.append(str(entry))
                visited.add(str(entry))


def parse_setup_cfg(path: str, include_dev: bool = False) -> Dict[str, DepInfo]:
    """Parse install_requires and extras_require from setup.cfg."""
    source = os.path.basename(path)
    result: Dict[str, DepInfo] = {}
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")

    def _add_pep508(line: str, is_dev: bool) -> None:
        line = line.strip()
        if not line or line.startswith("#"):
            return
        m = re.match(r"^([A-Za-z0-9_\-\.]+)(\[.*?\])?\s*([><=!~,\s0-9\.\*]+)?", line)
        if not m:
            return
        name = m.group(1).strip()
        spec = (m.group(3) or "").strip() or "*"
        numeric = extract_numeric(spec) or ""
        result[name] = DepInfo(
            name=name, version_spec=spec, version=numeric,
            ecosystem="pypi", source_file=source, is_dev=is_dev,
        )

    install_requires = cfg.get("options", "install_requires", fallback="")
    for line in install_requires.strip().splitlines():
        _add_pep508(line, False)

    if include_dev and cfg.has_section("options.extras_require"):
        for _extra, requires in cfg.items("options.extras_require"):
            for line in requires.strip().splitlines():
                _add_pep508(line, True)

    return result


def parse_package_lock_json(path: str) -> Dict[str, str]:
    """Return {package_name: exact_version} from package-lock.json v2/v3."""
    import json as _json
    try:
        data = _json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    result: Dict[str, str] = {}
    # v2/v3 format uses "packages" with "node_modules/pkg" keys
    packages = data.get("packages", {})
    if packages:
        for pkg_path, info in packages.items():
            if not pkg_path:
                continue
            if not pkg_path.startswith("node_modules/"):
                continue
            name = pkg_path[len("node_modules/"):]
            # Skip nested: node_modules/a/node_modules/b
            if "node_modules/" in name:
                continue
            ver = info.get("version", "")
            if ver:
                result[name] = ver
    else:
        # v1 format uses "dependencies" dict
        for name, info in (data.get("dependencies") or {}).items():
            ver = info.get("version", "")
            if ver:
                result[name] = ver
    return result


def parse_yarn_lock(path: str) -> Dict[str, str]:
    """Return {package_name: resolved_version} from yarn.lock v1."""
    result: Dict[str, str] = {}
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return result
    current_packages: List[str] = []
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        if not line.startswith(" ") and not line.startswith("\t"):
            # Package header: "package@^1.2, package@^1.3:"
            current_packages = []
            raw = line.rstrip(":")
            for part in raw.split(","):
                part = part.strip().strip('"')
                m = re.match(r"(@?[^@]+)@", part)
                if m:
                    pkg_name = m.group(1).strip()
                    if pkg_name:
                        current_packages.append(pkg_name)
        elif current_packages:
            m = re.match(r'\s+version\s+"?([^"\s]+)"?', line)
            if m:
                ver = m.group(1)
                for pkg in current_packages:
                    result[pkg] = ver
                current_packages = []
    return result


def parse_pnpm_lock(path: str) -> Dict[str, str]:
    """Return {package_name: resolved_version} from pnpm-lock.yaml (v5/v6/v8)."""
    result: Dict[str, str] = {}
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return result
    for line in text.splitlines():
        # Only process top-level package entries (indented 2 spaces, not 4+)
        if not (line.startswith("  ") and not line.startswith("    ")):
            continue
        stripped = line.strip()
        if not stripped.endswith(":"):
            continue
        key = stripped.rstrip(":")

        # v6/v8 format: "/stripe@8.0.0" or "stripe@8.0.0"
        m = re.match(r"^/?(@?[a-zA-Z0-9_\-\.]+(?:/[a-zA-Z0-9_\-\.]+)?)@(\d[^\s:/]*)$", key)
        if m:
            result[m.group(1)] = m.group(2)
            continue

        # v5 format: "/express/4.18.2" or "/@scope/pkg/1.0.0"
        m5 = re.match(r"^/(@?[^/]+(?:/[^/]+)?)/(\d[^/:\s]*)$", key)
        if m5:
            result[m5.group(1)] = m5.group(2)
    return result


def _read_lock_file(pkg_dir: Path) -> Dict[str, str]:
    """Read the first available lock file in pkg_dir, return {name: exact_version}."""
    for lock_name, parser in [
        ("package-lock.json", parse_package_lock_json),
        ("yarn.lock", parse_yarn_lock),
        ("pnpm-lock.yaml", parse_pnpm_lock),
    ]:
        lock_path = pkg_dir / lock_name
        if lock_path.is_file():
            return parser(str(lock_path))
    return {}


def _parse_go_require_line(line: str, source: str, result: Dict[str, DepInfo]) -> None:
    """Parse a single line from inside a go.mod require() block."""
    if not line or line.startswith("//"):
        return
    parts = line.split()
    if len(parts) >= 2:
        _add_go_dep(parts[0], parts[1], source, result)


def _add_go_dep(module_path: str, version_str: str, source: str,
                result: Dict[str, DepInfo]) -> None:
    """Add a single Go dependency to result dict."""
    # Strip // indirect comment suffix
    version_str = version_str.split("//")[0].strip()
    numeric = extract_numeric(version_str) or version_str.lstrip("v")
    result[module_path] = DepInfo(
        name=module_path,
        version_spec=version_str,
        version=numeric,
        ecosystem="go",
        source_file=source,
    )


def _load_toml(text: str) -> Optional[Dict]:
    """Try tomllib (3.11+), then tomli, then fall back to simple regex parser."""
    try:
        import tomllib  # type: ignore
        return tomllib.loads(text)
    except ImportError:
        pass
    try:
        import tomli  # type: ignore
        return tomli.loads(text)
    except ImportError:
        pass
    # Minimal regex-based TOML parser — handles flat key=value and simple tables
    return _simple_toml_parse(text)


def _simple_toml_parse(text: str) -> Dict:
    """Very minimal TOML parser for basic key=value and [section] support.

    Handles the subset needed for pyproject.toml and Cargo.toml:
    - [section] and [[array.of.tables]]
    - key = "value" and key = ['a', 'b']  (simple string arrays)
    - key = { version = "1.0" }  (inline tables, basic)
    """
    result: Dict = {}
    current: Dict = result
    current_path: List[str] = []

    def _set_nested(root: Dict, keys: List[str], value) -> None:
        d = root
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def _get_nested(root: Dict, keys: List[str]) -> Dict:
        d = root
        for k in keys:
            d = d.setdefault(k, {})
        return d

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("#"):
            continue
        # Section header
        if line.startswith("[["):
            m = re.match(r"^\[\[([^\]]+)\]\]", line)
            if m:
                current_path = [p.strip() for p in m.group(1).split(".")]
                # array of tables
                target = result
                for k in current_path[:-1]:
                    target = target.setdefault(k, {})
                last_key = current_path[-1]
                arr = target.setdefault(last_key, [])
                new_table: Dict = {}
                arr.append(new_table)
                current = new_table
            continue
        if line.startswith("["):
            m = re.match(r"^\[([^\]]+)\]", line)
            if m:
                current_path = [p.strip() for p in m.group(1).split(".")]
                current = _get_nested(result, current_path)
            continue
        # Key-value
        if "=" in line and not line.startswith("#"):
            key, _, val_raw = line.partition("=")
            key = key.strip()
            val_raw = val_raw.strip()
            # Multiline array
            if val_raw.startswith("[") and not val_raw.rstrip().endswith("]"):
                combined = val_raw
                while i < len(lines) and not combined.rstrip().endswith("]"):
                    combined += " " + lines[i].strip()
                    i += 1
                val_raw = combined
            parsed_val = _parse_toml_value(val_raw)
            current[key] = parsed_val

    return result


def _parse_toml_value(raw: str):
    """Parse a TOML value string into a Python object (best effort)."""
    raw = raw.strip()
    # Boolean
    if raw == "true":
        return True
    if raw == "false":
        return False
    # Integer
    if re.match(r"^-?\d+$", raw):
        return int(raw)
    # Float
    if re.match(r"^-?\d+\.\d+$", raw):
        return float(raw)
    # Double-quoted string
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    # Single-quoted string
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    # Array
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in _split_toml_array(inner):
            items.append(_parse_toml_value(item.strip()))
        return items
    # Inline table
    if raw.startswith("{") and raw.endswith("}"):
        inner = raw[1:-1].strip()
        table: Dict = {}
        for part in _split_toml_array(inner):
            if "=" in part:
                k, _, v = part.partition("=")
                table[k.strip()] = _parse_toml_value(v.strip())
        return table
    # Fallback: return as string
    return raw


def _split_toml_array(s: str) -> List[str]:
    """Split a comma-separated TOML array/table body respecting nesting."""
    items = []
    depth = 0
    current = []
    for ch in s:
        if ch in ("{", "["):
            depth += 1
            current.append(ch)
        elif ch in ("}", "]"):
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            items.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        item = "".join(current).strip()
        if item:
            items.append(item)
    return items


def _regex_toml_array(text: str, table: str, key: str) -> List[str]:
    """Extract a string array value from a TOML text using regex."""
    # Match [table] section then key = [...]
    pattern = re.compile(
        r"\[" + re.escape(table) + r"\].*?" + re.escape(key) + r"\s*=\s*\[([^\]]*)\]",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        return []
    inner = m.group(1)
    items = []
    for item in re.findall(r"""['"]([^'"]+)['"]""", inner):
        items.append(item)
    return items
