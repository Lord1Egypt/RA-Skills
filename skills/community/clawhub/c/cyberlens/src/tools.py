"""Tool function implementations for OpenClaw integration."""

import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from .scanner import SecurityScanner
from .api_client import CyberLensAPIClient, CyberLensQuotaExceededError
from .auth import (
    build_upgrade_url,
    load_api_base_url,
    load_api_key,
    open_upgrade_page,
    run_connect_flow,
)
from .skill_scanner import scan_skill_local
from .models import (
    ScanResult,
    SecurityScore,
    Finding,
    FindingExplanation,
    ScanRule,
)


CLAWHUB_HOSTS = {
    "clawhub.ai",
    "www.clawhub.ai",
    "claw-hub.net",
    "www.claw-hub.net",
    "openclaw-hub.org",
    "www.openclaw-hub.org",
}


CLAWHUB_RESERVED_PATHS = {
    "about",
    "api",
    "plugins",
    "privacy",
    "search",
    "settings",
    "sign-in",
    "terms",
}


GITHUB_RESERVED_PATHS = {
    "about",
    "account",
    "apps",
    "collections",
    "contact",
    "customer-stories",
    "enterprise",
    "events",
    "explore",
    "features",
    "gist",
    "gists",
    "issues",
    "login",
    "marketplace",
    "new",
    "notifications",
    "orgs",
    "organizations",
    "pricing",
    "pulls",
    "search",
    "security",
    "settings",
    "site",
    "sponsors",
    "topics",
    "trending",
    "users",
}


# Finding explanations database
FINDING_EXPLANATIONS = {
    "missing-csp": {
        "explanation": "Content Security Policy (CSP) is a browser security feature that controls what resources (scripts, styles, images) can load on your page. Without it, attackers can inject malicious scripts that steal data or take over user sessions.",
        "severity": "medium",
        "remediation": "Add a Content-Security-Policy header to your HTTP responses. Start with a permissive policy like \"default-src 'self'\" and gradually tighten it as you test.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP",
            "https://csp-evaluator.withgoogle.com/",
        ],
    },
    "missing-hsts": {
        "explanation": "HTTP Strict Transport Security (HSTS) tells browsers to always use HTTPS for your site, preventing SSL stripping attacks where attackers downgrade connections to HTTP.",
        "severity": "high",
        "remediation": "Add Strict-Transport-Security: max-age=31536000; includeSubDomains; preload to all HTTPS responses. Test thoroughly before enabling preload.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
            "https://hstspreload.org/",
        ],
    },
    "missing-x-frame-options": {
        "explanation": "X-Frame-Controls whether your site can be embedded in iframes. Without it, attackers can embed your site in a hidden frame and trick users into clicking elements (clickjacking attacks).",
        "severity": "medium",
        "remediation": "Add X-Frame-Options: DENY to prevent all framing, or SAMEORIGIN to allow only same-site framing.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
        ],
    },
    "missing-x-content-type-options": {
        "explanation": "X-Content-Type-Options prevents browsers from MIME-sniffing responses away from the declared content type. Without it, attackers might upload files that execute as scripts.",
        "severity": "low",
        "remediation": "Add X-Content-Type-Options: nosniff to all responses.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
        ],
    },
    "missing-referrer-policy": {
        "explanation": "Referrer Policy controls how much referrer information is sent with requests. Without it, sensitive URL parameters might leak to third parties.",
        "severity": "low",
        "remediation": "Add Referrer-Policy: strict-origin-when-cross-origin to balance privacy and functionality.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy",
        ],
    },
    "missing-permissions-policy": {
        "explanation": "Permissions Policy (formerly Feature Policy) controls which browser features (camera, microphone, geolocation) can be used on your site. Without it, embedded content might access sensitive APIs.",
        "severity": "low",
        "remediation": "Add Permissions-Policy with restrictive defaults: camera=(), microphone=(), geolocation=(), etc.",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy",
        ],
    },
    "no-https": {
        "explanation": "Your site doesn't use HTTPS, which means all data transmitted between users and your server is unencrypted and can be intercepted or modified by attackers.",
        "severity": "critical",
        "remediation": "Install an SSL/TLS certificate and redirect all HTTP traffic to HTTPS. Let's Encrypt provides free certificates.",
        "references": [
            "https://letsencrypt.org/",
            "https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security",
        ],
    },
    "information-disclosure": {
        "explanation": "Your server is revealing technology information in HTTP headers. Attackers can use this to find known vulnerabilities for your specific software versions.",
        "severity": "low",
        "remediation": "Remove X-Powered-By headers from your server configuration. This doesn't prevent attacks but makes reconnaissance harder.",
        "references": [
            "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/",
        ],
    },
    "server-version-exposed": {
        "explanation": "Your server software version is visible in the Server header. Attackers can look up CVEs for that specific version and craft targeted attacks.",
        "severity": "low",
        "remediation": "Configure your web server to hide version information. In nginx: server_tokens off; In Apache: ServerTokens Prod",
        "references": [
            "https://nginx.org/en/docs/http/ngx_http_core_module.html#server_tokens",
            "https://httpd.apache.org/docs/current/mod/core.html#servertokens",
        ],
    },
    "insecure-form-action": {
        "explanation": "A form on your page submits to an HTTP URL. Even if your page is HTTPS, the form data will be sent unencrypted, exposing passwords and other sensitive data.",
        "severity": "high",
        "remediation": "Update all form actions to use HTTPS URLs. Also check that the form's action attribute uses https://",
        "references": [
            "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form",
        ],
    },
    "missing-csrf-protection": {
        "explanation": "A form that changes state (POST request) doesn't include a CSRF token. Attackers can trick users into submitting forms they didn't intend to, potentially changing passwords or making purchases.",
        "severity": "medium",
        "remediation": "Add CSRF tokens to all state-changing forms. Most web frameworks (Django, Rails, Laravel) have built-in CSRF protection.",
        "references": [
            "https://owasp.org/www-community/attacks/cs",
            "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html",
        ],
    },
}


def _validate_target_url(target: str) -> Optional[str]:
    """Validate that the provided target is an HTTP(S) URL."""
    if not target.startswith(("http://", "https://")):
        return "URL must start with http:// or https://"

    parsed = urlparse(target)
    if not parsed.scheme or not parsed.netloc:
        return "URL must include a valid hostname"

    return None


def _is_clawhub_skill_path(path_parts: List[str]) -> bool:
    """Return True when the Claw Hub path looks like a skill detail page."""
    if len(path_parts) < 2:
        return False

    first_segment = path_parts[0].lower()
    if first_segment == "skills":
        return True

    return first_segment not in CLAWHUB_RESERVED_PATHS


def _is_skill_download_url(parsed) -> bool:
    """Return True when the URL points at a direct skill download endpoint."""
    host = (parsed.hostname or "").lower()
    return host.endswith(".convex.site") and parsed.path.rstrip("/") == "/api/v1/download"


def _classify_target(target: str) -> str:
    """Classify a scan target as a website, GitHub repository, or Claw Hub skill."""
    validation_error = _validate_target_url(target)
    if validation_error:
        return "invalid"

    parsed = urlparse(target)
    host = (parsed.hostname or "").lower()
    path_parts = [part for part in parsed.path.split("/") if part]

    if _is_skill_download_url(parsed):
        return "skill"

    # Claw Hub skill pages: clawhub.ai/skills/skill-name or clawhub.ai/author/skill-name
    if host in CLAWHUB_HOSTS and _is_clawhub_skill_path(path_parts):
        return "skill"

    if host in {"github.com", "www.github.com"} and len(path_parts) >= 2:
        owner = path_parts[0].lower()
        repo = path_parts[1]
        if owner not in GITHUB_RESERVED_PATHS and repo:
            return "repository"

    return "website"


def _normalize_cloud_vulnerabilities(vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize website vulnerability payloads from the CyberLens cloud API."""
    return [
        {
            "test_id": vulnerability.get("testId") or vulnerability.get("type", "unknown"),
            "type": vulnerability.get("testId") or vulnerability.get("type", "unknown"),
            "severity": vulnerability.get("severity", "info"),
            "message": vulnerability.get("message") or vulnerability.get("title") or vulnerability.get("description", ""),
            "description": vulnerability.get("message") or vulnerability.get("title") or vulnerability.get("description", ""),
            "details": vulnerability.get("details") or vulnerability.get("description", ""),
            "recommendation": vulnerability.get("recommendation", ""),
            "passed": bool(vulnerability.get("passed", False)),
        }
        for vulnerability in vulnerabilities
    ]


def _flatten_repository_findings(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten repository scan sections into a single findings list."""
    findings: List[Dict[str, Any]] = []

    for finding in result.get("security_findings", []) or []:
        findings.append({
            "source_section": "security_findings",
            "type": finding.get("test_id") or finding.get("category") or "repository-security-finding",
            "test_id": finding.get("test_id"),
            "severity": finding.get("severity", "info"),
            "confidence": finding.get("confidence"),
            "message": finding.get("message", ""),
            "description": finding.get("details") or finding.get("message", ""),
            "details": finding.get("details"),
            "recommendation": finding.get("recommendation"),
            "category": finding.get("category"),
            "cve": finding.get("cve"),
        })

    for finding in result.get("dependency_vulnerabilities", []) or []:
        package_name = finding.get("package_name", "unknown")
        current_version = finding.get("current_version", "unknown")
        findings.append({
            "source_section": "dependency_vulnerabilities",
            "type": "dependency-vulnerability",
            "severity": finding.get("severity", "info"),
            "message": f"{package_name}@{current_version} may have vulnerabilities",
            "description": finding.get("remediation", ""),
            "details": f"Current version: {current_version}",
            "recommendation": finding.get("remediation"),
            "package_name": package_name,
            "current_version": current_version,
            "patched_version": finding.get("patched_version"),
            "cve_ids": finding.get("cve_ids", []),
        })

    for finding in result.get("trust_posture_findings", []) or []:
        findings.append({
            "source_section": "trust_posture_findings",
            "type": "trust-posture",
            "severity": finding.get("severity", "info"),
            "message": finding.get("title") or finding.get("message", ""),
            "description": finding.get("message", ""),
            "details": finding.get("message"),
            "recommendation": finding.get("remediation"),
            "classification": finding.get("classification"),
        })

    for section_name in (
        "secret_findings",
        "behavioral_findings",
        "malicious_code_findings",
        "malicious_package_findings",
        "artifact_findings",
    ):
        for finding in result.get(section_name, []) or []:
            findings.append({
                "source_section": section_name,
                "type": finding.get("type") or finding.get("title") or section_name.rstrip("s"),
                "severity": finding.get("severity", "info"),
                "message": finding.get("message") or finding.get("title", ""),
                "description": finding.get("details") or finding.get("message") or finding.get("title", ""),
                "details": finding.get("details"),
                "recommendation": finding.get("recommendation") or finding.get("remediation"),
            })

    return findings


def _is_repository_scan_result(result: Dict[str, Any]) -> bool:
    """Return True when a cloud result matches the repository assessment schema."""
    return result.get("report_type") == "repository_security_assessment" or any(
        key in result
        for key in (
            "security_findings",
            "dependency_vulnerabilities",
            "trust_posture_findings",
            "repository",
        )
    )


def _format_repository_cloud_result(result: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Format a repository assessment response from the CyberLens cloud API."""
    security_score = result.get("security_score", 0) or 0
    grade = _score_to_grade(security_score)
    findings = _flatten_repository_findings(result)
    findings_count = result.get("summary", {}).get("total_findings")
    if not isinstance(findings_count, int):
        findings_count = len(findings)

    return {
        "success": True,
        "source": "cloud",
        "scan_mode": "cloud_full",
        "coverage": "cloud repository assessment",
        "target_type": "repository",
        "url": result.get("target", target),
        "score": security_score,
        "security_score": security_score,
        "trust_score": result.get("trust_score"),
        "grade": grade,
        "assessment": _get_grade_assessment(grade),
        "report_type": result.get("report_type", "repository_security_assessment"),
        "generated_at": result.get("generated_at"),
        "scan_date": result.get("scan_date"),
        "scan_type": result.get("scan_type"),
        "findings_count": findings_count,
        "summary": result.get("summary", {}),
        "repository": result.get("repository", {}),
        "ai_analysis": result.get("ai_analysis"),
        "findings": findings,
        "security_findings": result.get("security_findings", []),
        "dependency_vulnerabilities": result.get("dependency_vulnerabilities", []),
        "trust_posture_findings": result.get("trust_posture_findings", []),
        "secret_findings": result.get("secret_findings", []),
        "behavioral_findings": result.get("behavioral_findings", []),
        "malicious_code_findings": result.get("malicious_code_findings", []),
        "malicious_package_findings": result.get("malicious_package_findings", []),
        "artifact_findings": result.get("artifact_findings", []),
    }


def _format_website_cloud_result(result: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Format a website scan response from the CyberLens cloud API."""
    vulnerabilities = result.get("vulnerabilities", []) or []
    findings_count = result.get("summary", {}).get("vulnerabilities_found")
    if not isinstance(findings_count, int):
        findings_count = len(vulnerabilities)

    return {
        "success": True,
        "source": "cloud",
        "scan_mode": "cloud_full",
        "coverage": "70+ cloud checks",
        "target_type": "website",
        "url": result.get("url", target),
        "score": result.get("scores", {}).get("overall", 0),
        "grade": _score_to_grade(result.get("scores", {}).get("overall", 0)),
        "scan_type": result.get("scan_type"),
        "started_at": result.get("started_at"),
        "completed_at": result.get("completed_at"),
        "findings_count": findings_count,
        "summary": result.get("summary", {}),
        "ssl_info": result.get("ssl_info", {}),
        "headers_analysis": result.get("headers_analysis", {}),
        "database_passive_results": result.get("database_passive_results", []),
        "ai_insights": result.get("ai_insights"),
        "findings": _normalize_cloud_vulnerabilities(vulnerabilities),
    }


def _format_cloud_scan_result(result: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Format a CyberLens cloud result for either websites or repositories."""
    if _is_repository_scan_result(result):
        return _format_repository_cloud_result(result, target)
    return _format_website_cloud_result(result, target)


def _build_quota_upgrade_payload(
    error: CyberLensQuotaExceededError,
    target_type: str,
) -> Dict[str, Any]:
    """Build a user-facing upgrade prompt from a quota exhaustion error."""
    quota_type = error.quota_type or ("repository" if target_type in ("repository", "skill") else "website")
    upgrade_url = error.upgrade_url or build_upgrade_url(quota_type)
    open_upgrade_page(upgrade_url)

    payload: Dict[str, Any] = {
        "upgrade_required": True,
        "upgrade_url": upgrade_url,
        "upgrade_message": str(error),
        "opened_upgrade_page": True,
        "quota_type": quota_type,
    }

    if error.used is not None:
        payload["quota_used"] = error.used
    if error.limit is not None:
        payload["quota_limit"] = error.limit

    return payload


def _build_local_website_mode_payload(
    scan_depth: str,
    reason: str,
    quota_prompt: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Describe the local website fallback mode honestly for callers and UIs."""
    messages = [
        "This result came from the local quick website scan with roughly 15 core checks."
    ]

    if scan_depth != "quick":
        messages.append(
            f'Requested scan depth "{scan_depth}" is not available in local mode. '
            'The local quick scan was used instead.'
        )

    if reason == "no_account":
        messages.append(
            "Connect a CyberLens account to unlock the full cloud scan with 70+ checks, "
            "AI analysis, scan history, and repository scanning."
        )
    elif reason == "quota_exhausted" and quota_prompt:
        messages.append(
            "Cloud website quota is exhausted, so CyberLens fell back to the local quick scan. "
            f"Upgrade to restore full cloud coverage: {quota_prompt['upgrade_url']}"
        )
    elif reason == "local_requested":
        messages.append("Local mode was used because use_cloud=False was requested.")

    return {
        "scan_mode": "local_quick",
        "coverage": "~15 core local checks",
        "requested_scan_depth": scan_depth,
        "effective_scan_depth": "quick",
        "account_recommended": True,
        "notice": " ".join(messages),
    }


async def connect_account() -> Dict[str, Any]:
    """
    Connect your CyberLens account for cloud-powered scanning.

    Opens a browser window to sign in or create a CyberLens account.
    Once authenticated, your API key is stored locally for future scans.

    Returns:
        Dictionary with connection status
    """
    try:
        existing = load_api_key()
        if existing:
            return {
                "success": True,
                "message": "Already connected to CyberLens.",
                "key_prefix": existing[:12] + "...",
                "hint": "Run this again to reconnect with a new key.",
            }

        key = await run_connect_flow()
        return {
            "success": True,
            "message": "Successfully connected to CyberLens!",
            "key_prefix": key[:12] + "...",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


async def scan_target(
    target: str,
    scan_depth: str = "standard",
    timeout: float = 30.0,
    use_cloud: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Scan a live website, GitHub repository URL, or Claw Hub skill.

    Website targets use the local quick scan without an account and the full
    CyberLens cloud scan when connected.
    GitHub repository targets use the CyberLens cloud API and require an account.
    Claw Hub skills are downloaded and analysed locally so the package contents
    are inspected instead of the hosted marketplace page.

    Args:
        target: Website URL, GitHub repository URL, Claw Hub skill URL, or direct skill download URL
        scan_depth: Requested depth ("quick", "standard", "deep"). Local mode
            always uses the quick website scan and warns when a deeper mode was
            requested.
        timeout: Request timeout in seconds
        use_cloud: Force cloud (True) or local (False) scanning. None = auto-detect.

    Returns:
        Dictionary with scan results tailored to the detected target type
    """
    validation_error = _validate_target_url(target)
    if validation_error:
        return {"success": False, "error": validation_error, "url": target}

    target_type = _classify_target(target)
    api_key = load_api_key()
    api_base_url = load_api_base_url()
    should_use_cloud = use_cloud if use_cloud is not None else bool(api_key)
    quota_prompt: Optional[Dict[str, Any]] = None

    if target_type == "skill":
        try:
            result = await scan_skill_local(target, timeout=timeout)
            result["account_recommended"] = True
            messages = ["This result came from the local skill package scan."]
            if should_use_cloud and api_key:
                messages.append(
                    "Connected-account cloud scanning is not used for Claw Hub skill URLs because CyberLens should inspect the skill package, not the Claw Hub page."
                )
            else:
                messages.append(
                    "Connect a CyberLens account when you want cloud website scanning or repository scanning."
                )
            result["notice"] = " ".join(messages)
            return result
        except Exception as e:
            return {
                "success": False,
                "target_type": "skill",
                "url": target,
                "error": f"Local skill scan failed: {e}",
            }

    if target_type == "repository":
        if not (should_use_cloud and api_key):
            return {
                "success": False,
                "target_type": "repository",
                "url": target,
                "error": (
                    "Repository scanning requires a connected CyberLens account. "
                    "Run connect_account or set CYBERLENS_API_KEY."
                ),
            }

        try:
            async with CyberLensAPIClient(api_key, timeout=timeout, api_base=api_base_url) as client:
                result = await client.scan(target)
                return _format_cloud_scan_result(result, target)
        except CyberLensQuotaExceededError as e:
            return {
                "success": False,
                "target_type": "repository",
                "url": target,
                "error": str(e),
                **_build_quota_upgrade_payload(e, "repository"),
            }
        except Exception as e:
            return {
                "success": False,
                "target_type": "repository",
                "url": target,
                "error": f"Cloud repository scan failed: {e}",
            }

    if should_use_cloud and api_key:
        try:
            async with CyberLensAPIClient(api_key, timeout=timeout, api_base=api_base_url) as client:
                result = await client.scan(target)
                return _format_cloud_scan_result(result, target)
        except CyberLensQuotaExceededError as e:
            quota_prompt = _build_quota_upgrade_payload(e, "website")
        except Exception as e:
            if use_cloud is True:
                return {
                    "success": False,
                    "target_type": "website",
                    "error": f"Cloud scan failed: {e}",
                    "url": target,
                }
            # Fall through to local website scan

    async with SecurityScanner(timeout=timeout) as scanner:
        result = await scanner.scan(target)

        if result.error:
            failure = {
                "success": False,
                "target_type": "website",
                "error": result.error,
                "url": result.url,
            }
            failure.update(
                _build_local_website_mode_payload(
                    scan_depth,
                    "quota_exhausted" if quota_prompt else ("local_requested" if use_cloud is False else "no_account"),
                    quota_prompt,
                )
            )
            if quota_prompt:
                failure.update(quota_prompt)
            return failure

        output = {
            "success": True,
            "source": "local",
            "target_type": "website",
            "url": result.url,
            "score": result.score,
            "grade": result.grade,
            "scan_time_ms": result.scan_time_ms,
            "technologies": result.technologies,
            "findings_count": len(result.findings),
            "findings": [
                {
                    "type": f.type,
                    "severity": f.severity,
                    "description": f.description,
                    "remediation": f.remediation,
                    "evidence": f.evidence,
                }
                for f in result.findings
            ],
        }
        output.update(
            _build_local_website_mode_payload(
                scan_depth,
                "quota_exhausted" if quota_prompt else ("local_requested" if use_cloud is False else "no_account"),
                quota_prompt,
            )
        )
        if quota_prompt:
            output.update(quota_prompt)
            output["cloud_quota_exceeded"] = True

        return output


async def scan_website(
    url: str,
    scan_depth: str = "standard",
    timeout: float = 30.0,
    use_cloud: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Perform a security scan on a website URL.

    Uses the local quick scan without an account and the full CyberLens cloud
    API when connected. If cloud quota is exhausted, it falls back to the local
    quick scan automatically.

    Args:
        url: The website URL to scan (must include https:// or http://)
        scan_depth: Requested depth ("quick", "standard", "deep"). Local mode
            always uses the quick scan and warns when a deeper mode was
            requested.
        timeout: Request timeout in seconds
        use_cloud: Force cloud (True) or local (False) scanning. None = auto-detect.

    Returns:
        Dictionary with scan results including score, grade, and findings
    """
    return await scan_target(
        target=url,
        scan_depth=scan_depth,
        timeout=timeout,
        use_cloud=use_cloud,
    )


async def scan_repository(
    repository_url: str,
    timeout: float = 60.0,
    use_cloud: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Scan a GitHub repository URL with CyberLens cloud analysis.

    Args:
        repository_url: GitHub repository URL such as https://github.com/owner/repo
        timeout: Request timeout in seconds
        use_cloud: Force cloud behavior. Repository scanning requires cloud access.

    Returns:
        Dictionary with repository security findings, scores, and summary
    """
    if _classify_target(repository_url) not in ("repository", "skill"):
        return {
            "success": False,
            "error": (
                "Expected a GitHub repository URL (e.g. https://github.com/owner/repo) "
                "or a Claw Hub skill URL (e.g. https://clawhub.ai/author/skill-name)."
            ),
            "url": repository_url,
        }

    return await scan_target(
        target=repository_url,
        timeout=timeout,
        use_cloud=use_cloud,
    )


async def get_security_score(
    url: str,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    """
    Quick security score check for a URL.

    Uses the CyberLens cloud API if connected, otherwise local scanning.

    Args:
        url: The website URL to check
        timeout: Request timeout in seconds

    Returns:
        Dictionary with score and grade
    """
    validation_error = _validate_target_url(url)
    if validation_error:
        return {"success": False, "error": validation_error, "url": url}

    target_type = _classify_target(url)
    api_key = load_api_key()
    api_base_url = load_api_base_url()
    quota_result: Optional[Dict[str, Any]] = None

    if target_type == "skill":
        try:
            result = await scan_skill_local(url, timeout=timeout)
            score = result.get("score", result.get("security_score", 0))
            grade = _score_to_grade(score)
            messages = ["This score came from the local skill package scan."]
            if api_key:
                messages.append(
                    "Connected-account cloud scanning is not used for Claw Hub skill URLs because CyberLens should score the skill package, not the Claw Hub page."
                )
            else:
                messages.append(
                    "Connect a CyberLens account for cloud website scanning or repository scanning."
                )
            return {
                "success": True,
                "source": "local",
                "scan_mode": "local_skill_package",
                "coverage": "local skill package analysis",
                "target_type": "skill",
                "url": result.get("url", url),
                "score": score,
                "security_score": score,
                "grade": grade,
                "assessment": result.get("assessment", _get_grade_assessment(grade)),
                "account_recommended": True,
                "notice": " ".join(messages),
            }
        except Exception as e:
            return {
                "success": False,
                "target_type": "skill",
                "url": url,
                "error": f"Local skill scoring failed: {e}",
            }

    if target_type == "repository":
        if not api_key:
            return {
                "success": False,
                "target_type": "repository",
                "url": url,
                "error": (
                    "Repository scoring requires a connected CyberLens account. "
                    "Run connect_account or set CYBERLENS_API_KEY."
                ),
            }

        try:
            async with CyberLensAPIClient(api_key, timeout=timeout, api_base=api_base_url) as client:
                result = await client.scan(url)
                score = result.get("security_score", 0) or 0
                grade = _score_to_grade(score)
                return {
                    "success": True,
                    "source": "cloud",
                    "scan_mode": "cloud_full",
                    "coverage": "cloud repository assessment",
                    "target_type": target_type,
                    "url": result.get("target", url),
                    "score": score,
                    "security_score": score,
                    "trust_score": result.get("trust_score"),
                    "grade": grade,
                    "assessment": _get_grade_assessment(grade),
                }
        except CyberLensQuotaExceededError as e:
            return {
                "success": False,
                "target_type": "repository",
                "url": url,
                "error": str(e),
                **_build_quota_upgrade_payload(e, "repository"),
            }
        except Exception as e:
            return {
                "success": False,
                "target_type": "repository",
                "url": url,
                "error": f"Cloud repository scoring failed: {e}",
            }

    if api_key:
        try:
            async with CyberLensAPIClient(api_key, timeout=timeout, api_base=api_base_url) as client:
                result = await client.scan(url)
                score = result.get("scores", {}).get("overall", 0)
                grade = _score_to_grade(score)
                return {
                    "success": True,
                    "source": "cloud",
                    "scan_mode": "cloud_full",
                    "coverage": "70+ cloud checks",
                    "target_type": "website",
                    "url": url,
                    "score": score,
                    "grade": grade,
                    "assessment": _get_grade_assessment(grade),
                }
        except CyberLensQuotaExceededError as e:
            quota_prompt = _build_quota_upgrade_payload(e, "website")
            quota_result = {
                "upgrade_required": True,
                "upgrade_url": quota_prompt["upgrade_url"],
                "upgrade_message": quota_prompt["upgrade_message"],
                "opened_upgrade_page": quota_prompt["opened_upgrade_page"],
                "quota_type": quota_prompt["quota_type"],
                "cloud_quota_exceeded": True,
            }
            if "quota_used" in quota_prompt:
                quota_result["quota_used"] = quota_prompt["quota_used"]
            if "quota_limit" in quota_prompt:
                quota_result["quota_limit"] = quota_prompt["quota_limit"]
        except Exception:
            quota_result = None

    async with SecurityScanner(timeout=timeout) as scanner:
        result = await scanner.scan(url)
        if result.error:
            failure = {
                "success": False,
                "target_type": "website",
                "url": result.url,
                "error": result.error,
            }
            failure.update(
                _build_local_website_mode_payload(
                    "quick",
                    "quota_exhausted" if quota_result else "no_account",
                    quota_result,
                )
            )
            if quota_result:
                failure.update(quota_result)
            return failure

        output = {
            "success": True,
            "source": "local",
            "target_type": "website",
            "url": result.url,
            "score": result.score,
            "grade": result.grade,
            "assessment": _get_grade_assessment(result.grade),
        }
        output.update(
            _build_local_website_mode_payload(
                "quick",
                "quota_exhausted" if quota_result else "no_account",
                quota_result,
            )
        )
        if quota_result:
            output.update(quota_result)

        return output


def _score_to_grade(score: int) -> str:
    """Convert a numeric score to a letter grade."""
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


def _get_grade_assessment(grade: str) -> str:
    """Get a human-readable assessment for a grade."""
    assessments = {
        "A": "Excellent security posture. Minor improvements possible.",
        "B": "Good security with some room for improvement.",
        "C": "Average security. Several issues should be addressed.",
        "D": "Below average. Significant security improvements needed.",
        "F": "Poor security. Critical issues must be fixed immediately.",
    }
    return assessments.get(grade, "Unknown grade")


def explain_finding(
    finding_type: str,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a plain-English explanation of a security finding.
    
    Args:
        finding_type: The type of finding (e.g., "missing-csp", "no-https")
        context: Optional context about where the finding was detected
    
    Returns:
        Dictionary with explanation, severity, and remediation advice
    """
    explanation = FINDING_EXPLANATIONS.get(finding_type)
    
    if not explanation:
        return {
            "success": False,
            "error": f"Unknown finding type: {finding_type}",
            "known_types": list(FINDING_EXPLANATIONS.keys()),
        }
    
    result = {
        "success": True,
        "finding_type": finding_type,
        "explanation": explanation["explanation"],
        "severity": explanation["severity"],
        "remediation": explanation["remediation"],
        "references": explanation["references"],
    }
    
    if context:
        result["context"] = context
    
    return result


def list_scan_rules() -> Dict[str, Any]:
    """
    List all available scan rules/categories.
    
    Returns:
        Dictionary with available scan rules organized by category
    """
    categories = {
        "headers": {
            "description": "HTTP security header checks",
            "rules": [
                {"name": "content-security-policy", "severity": "medium"},
                {"name": "strict-transport-security", "severity": "high"},
                {"name": "x-frame-options", "severity": "medium"},
                {"name": "x-content-type-options", "severity": "low"},
                {"name": "referrer-policy", "severity": "low"},
                {"name": "permissions-policy", "severity": "low"},
            ],
        },
        "https": {
            "description": "HTTPS and TLS configuration checks",
            "rules": [
                {"name": "https-enforced", "severity": "critical"},
                {"name": "hsts-enabled", "severity": "high"},
            ],
        },
        "disclosure": {
            "description": "Information disclosure detection",
            "rules": [
                {"name": "server-header", "severity": "low"},
                {"name": "x-powered-by", "severity": "low"},
                {"name": "version-exposure", "severity": "low"},
            ],
        },
        "forms": {
            "description": "Form security analysis",
            "rules": [
                {"name": "csrf-protection", "severity": "medium"},
                {"name": "secure-form-action", "severity": "high"},
            ],
        },
        "repository": {
            "description": "Cloud repository scanning categories for GitHub repositories and OpenClaw skills",
            "rules": [
                {"name": "dependency-vulnerabilities", "severity": "high"},
                {"name": "trust-posture", "severity": "medium"},
                {"name": "secret-detection", "severity": "high"},
                {"name": "malicious-package-review", "severity": "high"},
            ],
        },
    }
    
    total_rules = sum(len(cat["rules"]) for cat in categories.values())

    return {
        "success": True,
        "total_rules": total_rules,
        "categories": categories,
    }


async def scan_skill(
    skill_url: str,
    timeout: float = 60.0,
) -> Dict[str, Any]:
    """
    Scan a Claw Hub skill before installing it.

    Accepts a Claw Hub URL (e.g. https://clawhub.ai/skills/skill-name),
    a direct download URL (e.g. https://*.convex.site/api/v1/download?slug=name),
    or a GitHub repository URL for an OpenClaw skill.

    The skill zip is downloaded, extracted, and analysed locally for security
    issues including hardcoded secrets, dangerous code patterns, insecure
    network requests, and manifest completeness. No CyberLens account is
    required for skill scanning.

    For GitHub repository URLs, use scan_repository instead (requires a
    CyberLens account).

    Args:
        skill_url: Claw Hub skill URL, direct download URL, or GitHub repo URL
        timeout: Request timeout in seconds (default: 60)

    Returns:
        Dictionary with security score, grade, assessment, and detailed findings
    """
    validation_error = _validate_target_url(skill_url)
    if validation_error:
        return {"success": False, "error": validation_error, "url": skill_url}

    target_type = _classify_target(skill_url)

    # GitHub repos should use scan_repository
    if target_type == "repository":
        return {
            "success": False,
            "error": (
                "Repository URLs cannot be scanned as CLAW skills directly. "
                "Use scan_repository for repo security audits, or provide the "
                "Claw Hub URL (e.g. https://clawhub.ai/skills/skill-name)."
            ),
            "url": skill_url,
        }

    if target_type not in ("skill", "website"):
        return {
            "success": False,
            "error": (
                "Expected a Claw Hub skill URL (e.g. https://clawhub.ai/skills/skill-name) "
                "or a direct download URL."
            ),
            "url": skill_url,
        }

    try:
        return await scan_skill_local(skill_url, timeout=timeout)
    except Exception as e:
        return {
            "success": False,
            "target_type": "skill",
            "url": skill_url,
            "error": f"Skill scan failed: {e}",
        }


# ---------------------------------------------------------------------------
# Report generation helpers
# ---------------------------------------------------------------------------

_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def _severity_sort_key(finding: Dict[str, Any]) -> int:
    return _SEVERITY_ORDER.get(finding.get("severity", "info"), 5)


def _severity_emoji(severity: str) -> str:
    return {
        "critical": "[!]",
        "high": "[H]",
        "medium": "[M]",
        "low": "[L]",
        "info": "[i]",
    }.get(severity, "[-]")


def generate_report(scan_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a formatted markdown report from scan results.

    Takes the output of scan_target, scan_skill, scan_website, or
    scan_repository and produces a clean markdown report suitable for
    sharing via messaging (Telegram, Discord, Signal), the web UI, or
    any channel that renders markdown.

    Args:
        scan_result: The dictionary returned by any CyberLens scan tool

    Returns:
        Dictionary with 'success', 'format' ("markdown"), and 'report' (the
        markdown string)
    """
    if not scan_result.get("success"):
        return {
            "success": False,
            "error": scan_result.get("error", "Cannot generate report from a failed scan."),
        }

    target_type = scan_result.get("target_type", "website")
    url = scan_result.get("url", "Unknown")
    score = scan_result.get("score") or scan_result.get("security_score", "N/A")
    grade = scan_result.get("grade", "N/A")
    trust_score = scan_result.get("trust_score")
    assessment = scan_result.get("assessment", "")
    source = scan_result.get("source", "cloud")
    generated_at = scan_result.get("generated_at") or scan_result.get("scan_date") or datetime.now(timezone.utc).isoformat()
    findings = scan_result.get("findings", [])
    ai_analysis = scan_result.get("ai_analysis") or scan_result.get("ai_insights")

    # Header
    type_label = {"skill": "Claw Hub Skill", "repository": "Repository", "website": "Website"}.get(target_type, target_type.title())
    lines: List[str] = []
    lines.append(f"# CyberLens Security Report")
    lines.append("")
    lines.append(f"**Target:** {url}")
    lines.append(f"**Type:** {type_label}")
    lines.append(f"**Scan Source:** {source}")
    lines.append(f"**Date:** {generated_at}")
    lines.append("")

    # Score card
    lines.append("## Score")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Security Score | {score} / 100 |")
    lines.append(f"| Grade | {grade} |")
    if trust_score is not None:
        lines.append(f"| Trust Score | {trust_score} / 100 |")
    if assessment:
        lines.append(f"| Assessment | {assessment} |")
    lines.append("")

    # AI analysis
    if ai_analysis:
        lines.append("## AI Analysis")
        lines.append("")
        if isinstance(ai_analysis, dict):
            for key, value in ai_analysis.items():
                lines.append(f"**{key.replace('_', ' ').title()}:** {value}")
                lines.append("")
        else:
            lines.append(str(ai_analysis))
            lines.append("")

    # Summary
    summary = scan_result.get("summary")
    if summary and isinstance(summary, dict):
        lines.append("## Summary")
        lines.append("")
        for key, value in summary.items():
            lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        lines.append("")

    # Findings
    if findings:
        sorted_findings = sorted(findings, key=_severity_sort_key)
        lines.append(f"## Findings ({len(findings)} total)")
        lines.append("")
        for i, f in enumerate(sorted_findings, 1):
            sev = f.get("severity", "info")
            marker = _severity_emoji(sev)
            msg = f.get("message") or f.get("description", "No description")
            lines.append(f"### {i}. {marker} {msg}")
            lines.append("")
            lines.append(f"- **Severity:** {sev}")
            if f.get("type"):
                lines.append(f"- **Type:** {f['type']}")
            if f.get("category"):
                lines.append(f"- **Category:** {f['category']}")
            if f.get("description") and f.get("description") != msg:
                lines.append(f"- **Details:** {f['description']}")
            if f.get("details") and f.get("details") != f.get("description"):
                lines.append(f"- **Details:** {f['details']}")
            if f.get("recommendation") or f.get("remediation"):
                lines.append(f"- **Recommendation:** {f.get('recommendation') or f.get('remediation')}")
            if f.get("cve"):
                lines.append(f"- **CVE:** {f['cve']}")
            if f.get("cve_ids"):
                lines.append(f"- **CVE IDs:** {', '.join(f['cve_ids'])}")
            lines.append("")
    else:
        lines.append("## Findings")
        lines.append("")
        lines.append("No findings detected.")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("*Generated by CyberLens Security Scanner — https://cyberlensai.com*")

    report_text = "\n".join(lines)

    return {
        "success": True,
        "format": "markdown",
        "report": report_text,
        "url": url,
        "target_type": target_type,
        "score": score,
        "grade": grade,
    }


def export_report_pdf(
    scan_result: Dict[str, Any],
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Export scan results as a PDF file.

    Takes the output of scan_target, scan_skill, scan_website, or
    scan_repository and writes a professionally formatted PDF report.
    Requires the reportlab package (pip install reportlab).

    Args:
        scan_result: The dictionary returned by any CyberLens scan tool
        output_path: Where to save the PDF. Defaults to
                     ~/cyberlens-report-<timestamp>.pdf

    Returns:
        Dictionary with 'success' and 'path' (absolute path to the PDF)
    """
    if not scan_result.get("success"):
        return {
            "success": False,
            "error": scan_result.get("error", "Cannot generate PDF from a failed scan."),
        }

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError:
        return {
            "success": False,
            "error": (
                "PDF export requires the reportlab package. "
                "Install it with: pip install reportlab"
            ),
        }

    # Resolve output path
    if not output_path:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        output_path = os.path.expanduser(f"~/cyberlens-report-{ts}.pdf")
    output_path = os.path.abspath(os.path.expanduser(output_path))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Extract data
    target_type = scan_result.get("target_type", "website")
    url = scan_result.get("url", "Unknown")
    score = scan_result.get("score") or scan_result.get("security_score", "N/A")
    grade = scan_result.get("grade", "N/A")
    trust_score = scan_result.get("trust_score")
    assessment = scan_result.get("assessment", "")
    source = scan_result.get("source", "cloud")
    generated_at = scan_result.get("generated_at") or scan_result.get("scan_date") or datetime.now(timezone.utc).isoformat()
    findings = scan_result.get("findings", [])
    ai_analysis = scan_result.get("ai_analysis") or scan_result.get("ai_insights")
    summary = scan_result.get("summary")
    type_label = {"skill": "Claw Hub Skill", "repository": "Repository", "website": "Website"}.get(target_type, target_type.title())

    # Grade colour
    grade_colour = {
        "A": colors.HexColor("#22c55e"),
        "B": colors.HexColor("#84cc16"),
        "C": colors.HexColor("#eab308"),
        "D": colors.HexColor("#f97316"),
        "F": colors.HexColor("#ef4444"),
    }.get(grade, colors.grey)

    severity_colour = {
        "critical": colors.HexColor("#ef4444"),
        "high": colors.HexColor("#f97316"),
        "medium": colors.HexColor("#eab308"),
        "low": colors.HexColor("#3b82f6"),
        "info": colors.HexColor("#6b7280"),
    }

    # Build PDF
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("CL_Title", parent=styles["Title"], fontSize=22, spaceAfter=6)
    heading_style = ParagraphStyle("CL_Heading", parent=styles["Heading2"], fontSize=14, spaceBefore=16, spaceAfter=6)
    body_style = ParagraphStyle("CL_Body", parent=styles["Normal"], fontSize=10, spaceAfter=4)
    small_style = ParagraphStyle("CL_Small", parent=styles["Normal"], fontSize=8, textColor=colors.grey)

    story: list = []

    # Title
    story.append(Paragraph("CyberLens Security Report", title_style))
    story.append(Spacer(1, 8))

    # Meta table
    meta_data = [
        ["Target", url],
        ["Type", type_label],
        ["Scan Source", source],
        ["Date", str(generated_at)],
    ]
    meta_table = Table(meta_data, colWidths=[1.4 * inch, 5.0 * inch])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Score card
    story.append(Paragraph("Score", heading_style))
    score_data = [["Security Score", f"{score} / 100"], ["Grade", str(grade)]]
    if trust_score is not None:
        score_data.append(["Trust Score", f"{trust_score} / 100"])
    if assessment:
        score_data.append(["Assessment", assessment])
    score_table = Table(score_data, colWidths=[1.8 * inch, 4.6 * inch])
    score_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (1, 0), (1, 0), grade_colour),
        ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 12))

    # AI Analysis
    if ai_analysis:
        story.append(Paragraph("AI Analysis", heading_style))
        if isinstance(ai_analysis, dict):
            for key, value in ai_analysis.items():
                story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", body_style))
        else:
            story.append(Paragraph(str(ai_analysis), body_style))
        story.append(Spacer(1, 8))

    # Summary
    if summary and isinstance(summary, dict):
        story.append(Paragraph("Summary", heading_style))
        for key, value in summary.items():
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", body_style))
        story.append(Spacer(1, 8))

    # Findings
    story.append(Paragraph(f"Findings ({len(findings)} total)", heading_style))
    if findings:
        sorted_findings = sorted(findings, key=_severity_sort_key)
        for i, f in enumerate(sorted_findings, 1):
            sev = f.get("severity", "info")
            msg = f.get("message") or f.get("description", "No description")
            sev_color = severity_colour.get(sev, colors.grey)

            # Finding header row
            header_data = [[f"#{i}", sev.upper(), msg]]
            header_table = Table(header_data, colWidths=[0.4 * inch, 0.8 * inch, 5.2 * inch])
            header_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BACKGROUND", (1, 0), (1, 0), sev_color),
                ("TEXTCOLOR", (1, 0), (1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(header_table)

            detail_parts = []
            if f.get("type"):
                detail_parts.append(f"Type: {f['type']}")
            if f.get("description") and f.get("description") != msg:
                detail_parts.append(f"Details: {f['description']}")
            if f.get("recommendation") or f.get("remediation"):
                detail_parts.append(f"Recommendation: {f.get('recommendation') or f.get('remediation')}")
            if f.get("cve"):
                detail_parts.append(f"CVE: {f['cve']}")
            if detail_parts:
                story.append(Paragraph("<br/>".join(detail_parts), body_style))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No findings detected.", body_style))

    # Footer
    story.append(Spacer(1, 24))
    story.append(Paragraph("Generated by CyberLens Security Scanner — https://cyberlensai.com", small_style))

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    doc.build(story)

    return {
        "success": True,
        "path": output_path,
        "url": url,
        "target_type": target_type,
        "score": score,
        "grade": grade,
    }
