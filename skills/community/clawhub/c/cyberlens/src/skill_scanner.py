"""Local CLAW skill scanner. Downloads, extracts, analyses, and cleans up."""

import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx


CLAWHUB_HOSTS = {
    "clawhub.ai",
    "www.clawhub.ai",
    "claw-hub.net",
    "www.claw-hub.net",
    "openclaw-hub.org",
    "www.openclaw-hub.org",
}

# Dangerous code patterns
_CODE_PATTERNS: List[Dict[str, Any]] = [
    # Critical
    {
        "pattern": re.compile(r"eval\s*\("),
        "severity": "critical",
        "title": "eval() usage detected",
        "description": "eval() executes arbitrary code and is a common injection vector.",
        "recommendation": "Replace eval() with safer alternatives like JSON parsing or AST-based evaluation.",
    },
    {
        "pattern": re.compile(r"exec\s*\(\s*[\"'`]|os\.system\s*\(|subprocess\.(call|run|Popen)\s*\("),
        "severity": "critical",
        "title": "Shell command execution",
        "description": "Direct shell command execution can lead to command injection.",
        "recommendation": "Use parameterised commands and avoid passing user input to shell execution.",
    },
    {
        "pattern": re.compile(r"child_process"),
        "severity": "critical",
        "title": "child_process module imported",
        "description": "child_process allows arbitrary command execution on the host system.",
        "recommendation": "Avoid child_process unless absolutely necessary. Document why it is needed.",
    },
    # High
    {
        "pattern": re.compile(
            r"(?:api[_-]?key|secret[_-]?key|password|token|auth)\s*[:=]\s*[\"'][A-Za-z0-9+/=_-]{16,}[\"']",
            re.IGNORECASE,
        ),
        "severity": "high",
        "title": "Possible hardcoded secret",
        "description": "A string resembling an API key, token, or password is hardcoded in the source.",
        "recommendation": "Move secrets to environment variables or a secure vault. Never commit credentials.",
    },
    {
        "pattern": re.compile(r"fetch\s*\(\s*[\"']http://"),
        "severity": "high",
        "title": "Insecure HTTP request",
        "description": "Plaintext HTTP requests expose data in transit to interception.",
        "recommendation": "Use HTTPS for all external requests.",
    },
    {
        "pattern": re.compile(r"requests\.get\s*\(\s*[\"']http://|httpx\.(get|post)\s*\(\s*[\"']http://"),
        "severity": "high",
        "title": "Insecure HTTP request (Python)",
        "description": "Plaintext HTTP requests expose data in transit to interception.",
        "recommendation": "Use HTTPS for all external requests.",
    },
    {
        "pattern": re.compile(r"fs\.unlink|fs\.rmdir|fs\.rm\b|os\.remove|os\.unlink|shutil\.rmtree"),
        "severity": "high",
        "title": "File deletion operation",
        "description": "Skill performs file deletion which could damage user data.",
        "recommendation": "Ensure file deletion is scoped to the skill's own working directory only.",
    },
    {
        "pattern": re.compile(r"\bopen\s*\([^)]*,\s*[\"']w"),
        "severity": "medium",
        "title": "File write operation",
        "description": "Skill writes to the filesystem. Verify writes are scoped and intentional.",
        "recommendation": "Ensure file writes are limited to expected directories (e.g., memory/, output/).",
    },
    # Medium
    {
        "pattern": re.compile(r"import\s+pickle|from\s+pickle\s+import|pickle\.loads?\("),
        "severity": "medium",
        "title": "Pickle deserialisation",
        "description": "Pickle can execute arbitrary code during deserialisation.",
        "recommendation": "Use JSON or another safe serialisation format instead of pickle.",
    },
    {
        "pattern": re.compile(r"import\s+ctypes|from\s+ctypes"),
        "severity": "medium",
        "title": "ctypes usage",
        "description": "ctypes allows calling C functions and manipulating memory directly.",
        "recommendation": "Avoid ctypes unless there is a clear, documented need for native code access.",
    },
    # Low
    {
        "pattern": re.compile(r"process\.env|os\.environ|os\.getenv"),
        "severity": "low",
        "title": "Environment variable access",
        "description": "Skill reads environment variables, which may contain sensitive data.",
        "recommendation": "Document which environment variables the skill needs and why.",
    },
]

_SEVERITY_WEIGHT = {"critical": 20, "high": 10, "medium": 5, "low": 2, "info": 0}
_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
_CODE_EXTENSIONS = {".py", ".js", ".ts", ".sh", ".bash", ".yaml", ".yml", ".json", ".toml"}


async def resolve_skill_download_url(skill_url: str) -> str:
    """Resolve a Claw Hub or direct URL to a downloadable skill zip URL.

    Accepted inputs:
        - https://clawhub.ai/skills/skill-name  (Claw Hub page)
        - https://clawhub.ai/author/skill-name  (Claw Hub page)
        - https://*.convex.site/api/v1/download?slug=skill-name  (direct)

    Returns the direct download URL.
    """
    parsed = urlparse(skill_url)

    # Already a direct download link
    if parsed.hostname and parsed.hostname.endswith(".convex.site"):
        return skill_url

    # Claw Hub URL — fetch page, extract download link
    if parsed.hostname and parsed.hostname in CLAWHUB_HOSTS:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(skill_url)
            response.raise_for_status()
            html = response.text

        match = re.search(
            r"https://[a-z0-9-]+\.convex\.site/api/v1/download\?[^\s\"'<>]+",
            html,
        )
        if not match:
            raise ValueError(
                "Could not find a download link on the Claw Hub page. "
                "The skill may not be published or the page format has changed."
            )
        return match.group(0)

    # GitHub/GitLab — not a CLAW skill zip
    if parsed.hostname in {"github.com", "gitlab.com", "bitbucket.org"}:
        raise ValueError(
            "Repository URLs cannot be scanned as CLAW skills directly. "
            "Use scan_repository for repo security audits, or provide the Claw Hub URL."
        )

    # Unknown — try as-is
    return skill_url


def _analyse_file(content: str, relative_path: str) -> List[Dict[str, Any]]:
    """Run pattern checks against a single file."""
    findings: List[Dict[str, Any]] = []
    for check in _CODE_PATTERNS:
        for match in check["pattern"].finditer(content):
            line_num = content[:match.start()].count("\n") + 1
            findings.append({
                "severity": check["severity"],
                "title": check["title"],
                "description": check["description"],
                "file": relative_path,
                "line": line_num,
                "recommendation": check["recommendation"],
            })
    return findings


def _analyse_manifest(meta: Dict[str, Any], skill_md: Optional[str]) -> List[Dict[str, Any]]:
    """Check _meta.json and SKILL.md for completeness."""
    findings: List[Dict[str, Any]] = []

    if not meta.get("slug"):
        findings.append({
            "severity": "medium",
            "title": "Missing skill slug",
            "description": "Skill metadata is missing a slug identifier.",
            "recommendation": "Ensure _meta.json includes a slug field.",
        })
    if not meta.get("version"):
        findings.append({
            "severity": "low",
            "title": "Missing version",
            "description": "Skill metadata does not specify a version.",
            "recommendation": "Include a version field in _meta.json for tracking.",
        })

    if skill_md:
        fm_match = re.match(r"^---\n(.*?)\n---", skill_md, re.DOTALL)
        if not fm_match:
            findings.append({
                "severity": "medium",
                "title": "Missing SKILL.md frontmatter",
                "description": "SKILL.md should have YAML frontmatter with name and description.",
                "recommendation": "Add frontmatter with at minimum: name, description.",
            })
        else:
            fm = fm_match.group(1)
            if "name:" not in fm:
                findings.append({
                    "severity": "medium",
                    "title": "Missing skill name in SKILL.md",
                    "description": "SKILL.md frontmatter should include a name field.",
                    "recommendation": "Add 'name:' to SKILL.md frontmatter.",
                })
            if "description:" not in fm:
                findings.append({
                    "severity": "low",
                    "title": "Missing description in SKILL.md",
                    "description": "SKILL.md frontmatter should include a description.",
                    "recommendation": "Add 'description:' to SKILL.md frontmatter.",
                })
    else:
        findings.append({
            "severity": "medium",
            "title": "Missing SKILL.md",
            "description": "No SKILL.md found. This file documents the skill's purpose and usage.",
            "recommendation": "Add a SKILL.md with frontmatter (name, description) and usage documentation.",
        })

    return findings


def _analyse_dependencies(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Check for unpinned dependencies."""
    findings: List[Dict[str, Any]] = []
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
        if file_path.endswith("requirements.txt"):
            if "==" not in trimmed and ">=" not in trimmed and "~=" not in trimmed:
                findings.append({
                    "severity": "low",
                    "title": "Unpinned dependency",
                    "description": f'Dependency "{trimmed}" has no version constraint.',
                    "file": file_path,
                    "recommendation": "Pin dependencies to specific versions for reproducibility.",
                })
    return findings


def _collect_external_urls(files: Dict[str, str]) -> List[Dict[str, Any]]:
    """Check all files for insecure external URLs."""
    url_re = re.compile(r"https?://[^\s\"'`,)}\]>]+")
    all_urls: set[str] = set()
    for content in files.values():
        all_urls.update(url_re.findall(content))

    findings: List[Dict[str, Any]] = []
    for url in all_urls:
        if url.startswith("http://") and not url.startswith(("http://localhost", "http://127.0.0.1")):
            findings.append({
                "severity": "medium",
                "title": "Insecure HTTP URL referenced",
                "description": f"The skill references an insecure URL: {url}",
                "recommendation": "Use HTTPS for all external communications.",
            })

    https_urls = [u for u in all_urls if u.startswith("https://")]
    if https_urls:
        preview = ", ".join(https_urls[:5])
        extra = f" and {len(https_urls) - 5} more" if len(https_urls) > 5 else ""
        findings.append({
            "severity": "info",
            "title": "External endpoints",
            "description": f"Skill communicates with {len(https_urls)} external HTTPS endpoint(s): {preview}{extra}",
            "recommendation": "Verify these endpoints are legitimate and necessary.",
        })

    return findings


def _calculate_score(findings: List[Dict[str, Any]]) -> int:
    """Calculate a 0-100 security score from findings."""
    score = 100
    for f in findings:
        score -= _SEVERITY_WEIGHT.get(f["severity"], 0)
    return max(0, score)


def _score_to_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


async def scan_skill_local(skill_url: str, timeout: float = 30.0) -> Dict[str, Any]:
    """Download a CLAW skill, analyse its contents locally, and return results.

    Args:
        skill_url: Claw Hub URL or direct download URL.
        timeout: HTTP timeout for downloading.

    Returns:
        Dictionary matching the format used by other scan_* tools.
    """
    download_url = await resolve_skill_download_url(skill_url)

    tmp_dir = Path(tempfile.mkdtemp(prefix="cyberlens-skill-"))
    zip_path = tmp_dir / "skill.zip"
    extract_dir = tmp_dir / "extracted"

    try:
        # Download
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(download_url)
            response.raise_for_status()
            zip_path.write_bytes(response.content)

        # Extract
        extract_dir.mkdir()
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)

        # Read all files
        files: Dict[str, str] = {}
        for file_path in extract_dir.rglob("*"):
            if file_path.is_file():
                try:
                    relative = str(file_path.relative_to(extract_dir))
                    files[relative] = file_path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    pass

        # Parse metadata
        meta: Dict[str, Any] = {}
        if "_meta.json" in files:
            try:
                meta = json.loads(files["_meta.json"])
            except (json.JSONDecodeError, ValueError):
                pass

        skill_md = files.get("SKILL.md")

        # Run analyses
        findings: List[Dict[str, Any]] = []
        findings.extend(_analyse_manifest(meta, skill_md))

        files_analysed = 0
        for relative_path, content in files.items():
            suffix = Path(relative_path).suffix
            if suffix in _CODE_EXTENSIONS:
                findings.extend(_analyse_file(content, relative_path))
                files_analysed += 1
            if relative_path.endswith("requirements.txt"):
                findings.extend(_analyse_dependencies(content, relative_path))
                files_analysed += 1
            if suffix == ".md":
                files_analysed += 1

        findings.extend(_collect_external_urls(files))

        # Sort by severity
        findings.sort(key=lambda f: _SEVERITY_ORDER.get(f["severity"], 99))

        score = _calculate_score(findings)
        grade = _score_to_grade(score)
        skill_name = meta.get("slug", "unknown-skill")
        version = meta.get("version", "unknown")

        crit_count = sum(1 for f in findings if f["severity"] == "critical")
        high_count = sum(1 for f in findings if f["severity"] == "high")

        if crit_count > 0:
            assessment = f"Critical security issues found. Do NOT install without reviewing the {crit_count} critical finding(s)."
        elif high_count > 0:
            assessment = f"{high_count} high-severity issue(s) found. Review before installing."
        elif score >= 80:
            assessment = "Skill appears safe to install. Minor issues noted below."
        else:
            assessment = "Several issues found. Review findings before installing."

        return {
            "success": True,
            "source": "local",
            "scan_mode": "local_skill_package",
            "coverage": "local skill package analysis",
            "target_type": "skill",
            "url": skill_url,
            "download_url": download_url,
            "skill_name": skill_name,
            "version": version,
            "score": score,
            "security_score": score,
            "grade": grade,
            "assessment": assessment,
            "files_analysed": files_analysed,
            "total_files": len(files),
            "findings_count": len(findings),
            "findings": findings,
        }

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
