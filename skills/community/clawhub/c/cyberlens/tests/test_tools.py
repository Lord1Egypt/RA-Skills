"""Tests for CyberLens skill tools."""

import pytest
from src.api_client import CyberLensQuotaExceededError
from src.scanner import Finding as LocalFinding
from src.scanner import ScanResult as LocalScanResult
from src.tools import (
    explain_finding,
    list_scan_rules,
    _classify_target,
    _get_grade_assessment,
)


class _FakeCloudClient:
    def __init__(self, result):
        self._result = result

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def scan(self, url):
        return self._result


class _FakeLocalScanner:
    def __init__(self, result):
        self._result = result

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def scan(self, url):
        return self._result


class _FailingCloudClient:
    def __init__(self, error):
        self._error = error

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def scan(self, url):
        raise self._error


class TestExplainFinding:
    """Tests for explain_finding tool."""
    
    def test_explain_known_finding(self):
        """Test explaining a known finding type."""
        result = explain_finding("missing-csp")
        
        assert result["success"] is True
        assert result["finding_type"] == "missing-csp"
        assert "explanation" in result
        assert "severity" in result
        assert "remediation" in result
        assert "references" in result
        assert len(result["references"]) > 0
    
    def test_explain_with_context(self):
        """Test explaining with context."""
        context = "Detected on login page"
        result = explain_finding("missing-csp", context=context)
        
        assert result["success"] is True
        assert result["context"] == context
    
    def test_explain_unknown_finding(self):
        """Test explaining an unknown finding type."""
        result = explain_finding("unknown-finding-type")
        
        assert result["success"] is False
        assert "error" in result
        assert "known_types" in result
        assert "missing-csp" in result["known_types"]
    
    def test_all_severity_levels_present(self):
        """Verify all severity levels have explanations."""
        critical = explain_finding("no-https")
        assert critical["severity"] == "critical"
        
        high = explain_finding("missing-hsts")
        assert high["severity"] == "high"
        
        medium = explain_finding("missing-csp")
        assert medium["severity"] == "medium"
        
        low = explain_finding("information-disclosure")
        assert low["severity"] == "low"


class TestListScanRules:
    """Tests for list_scan_rules tool."""
    
    def test_returns_success(self):
        """Test that list_scan_rules returns success."""
        result = list_scan_rules()
        
        assert result["success"] is True
        assert "total_rules" in result
        assert "categories" in result
    
    def test_has_categories(self):
        """Test that categories are present."""
        result = list_scan_rules()
        categories = result["categories"]
        
        assert "headers" in categories
        assert "https" in categories
        assert "disclosure" in categories
        assert "forms" in categories
    
    def test_headers_category_has_rules(self):
        """Test headers category has expected rules."""
        result = list_scan_rules()
        headers = result["categories"]["headers"]
        
        assert "description" in headers
        assert "rules" in headers
        
        rule_names = [r["name"] for r in headers["rules"]]
        assert "content-security-policy" in rule_names
        assert "strict-transport-security" in rule_names
    
    def test_total_rules_matches(self):
        """Test total_rules matches actual rule count."""
        result = list_scan_rules()
        total = result["total_rules"]
        
        calculated = sum(
            len(cat["rules"])
            for cat in result["categories"].values()
        )
        
        assert total == calculated


class TestTargetClassification:
    """Tests for target classification helpers."""

    def test_classifies_clawhub_skill_urls_as_skills(self):
        assert _classify_target("https://clawhub.ai/skills/demo") == "skill"
        assert _classify_target("https://clawhub.ai/author/demo-skill") == "skill"

    def test_classifies_direct_skill_download_urls_as_skills(self):
        assert (
            _classify_target("https://abc123.convex.site/api/v1/download?slug=demo")
            == "skill"
        )

    def test_does_not_treat_generic_clawhub_pages_as_skills(self):
        assert _classify_target("https://clawhub.ai/about") == "website"
        assert _classify_target("https://clawhub.ai/plugins") == "website"


class TestGetGradeAssessment:
    """Tests for grade assessment helper."""
    
    def test_all_grades_have_assessments(self):
        """Test all valid grades return assessments."""
        for grade in ["A", "B", "C", "D", "F"]:
            assessment = _get_grade_assessment(grade)
            assert len(assessment) > 0
            assert "Excellent" in assessment or "Good" in assessment or "Average" in assessment or "Below" in assessment or "Poor" in assessment
    
    def test_unknown_grade(self):
        """Test unknown grade returns default."""
        assessment = _get_grade_assessment("Z")
        assert "Unknown" in assessment


@pytest.mark.asyncio
class TestScanWebsite:
    """Tests for scan_website async tool."""
    
    async def test_cloud_scan_surfaces_full_api_fields(self, monkeypatch):
        """Test cloud scan output preserves the CyberLens API response shape."""
        from src import tools

        cloud_result = {
            "url": "https://example.com",
            "scores": {"overall": 82},
            "summary": {"vulnerabilities_found": 2},
            "scan_type": "premium",
            "started_at": "2026-03-26T18:00:00Z",
            "completed_at": "2026-03-26T18:00:12Z",
            "ssl_info": {"isHTTPS": True},
            "headers_analysis": {"csp": {"present": False}},
            "database_passive_results": [{"testId": "db_git_folder_exposed", "severity": "high"}],
            "ai_insights": {"summary": "Security posture needs work."},
            "vulnerabilities": [
                {
                    "testId": "missing_csp",
                    "message": "Missing Content Security Policy",
                    "details": "The response does not include a CSP header.",
                    "severity": "medium",
                    "recommendation": "Add a Content-Security-Policy header.",
                    "passed": False,
                },
                {
                    "testId": "hsts_missing",
                    "message": "HSTS header missing",
                    "details": "Strict-Transport-Security is not set.",
                    "severity": "medium",
                    "recommendation": "Set HSTS with a long max-age.",
                    "passed": False,
                },
            ],
        }

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FakeCloudClient(cloud_result),
        )

        result = await tools.scan_website("https://example.com", use_cloud=True)

        assert result["success"] is True
        assert result["source"] == "cloud"
        assert result["scan_type"] == "premium"
        assert result["started_at"] == "2026-03-26T18:00:00Z"
        assert result["completed_at"] == "2026-03-26T18:00:12Z"
        assert result["findings_count"] == 2
        assert len(result["findings"]) == 2
        assert result["ssl_info"] == {"isHTTPS": True}
        assert result["headers_analysis"] == {"csp": {"present": False}}
        assert result["database_passive_results"] == [{"testId": "db_git_folder_exposed", "severity": "high"}]
        assert result["ai_insights"] == {"summary": "Security posture needs work."}
        assert result["findings"][0] == {
            "test_id": "missing_csp",
            "type": "missing_csp",
            "severity": "medium",
            "message": "Missing Content Security Policy",
            "description": "Missing Content Security Policy",
            "details": "The response does not include a CSP header.",
            "recommendation": "Add a Content-Security-Policy header.",
            "passed": False,
        }

    async def test_cloud_scan_supports_repository_reports(self, monkeypatch):
        """Test that repository reports are surfaced explicitly when scanning GitHub URLs."""
        from src import tools

        repository_result = {
            "report_type": "repository_security_assessment",
            "target": "https://github.com/shadoprizm/cyberlens-skill",
            "security_score": 92,
            "trust_score": 98,
            "scan_type": "agency",
            "summary": {
                "total_findings": 2,
                "dependency_alerts": 1,
                "trust_posture_issues": 1,
            },
            "repository": {
                "provider": "github",
                "owner": "shadoprizm",
                "name": "cyberlens-skill",
            },
            "security_findings": [
                {
                    "test_id": "openclaw_vulnerable_dependencies",
                    "severity": "high",
                    "confidence": "confirmed",
                    "message": "Project has package files that should be checked for vulnerabilities",
                    "details": "requirements.txt",
                    "recommendation": "Run a full dependency vulnerability scan.",
                    "category": "openclaw_behavior",
                }
            ],
            "trust_posture_findings": [
                {
                    "title": "Missing: SECURITY.md or security policy",
                    "message": "No SECURITY.md — no clear way to report vulnerabilities",
                    "severity": "info",
                    "remediation": "Add a SECURITY.md with vulnerability disclosure instructions.",
                    "classification": "weak_trust",
                }
            ],
            "dependency_vulnerabilities": [],
            "secret_findings": [],
            "behavioral_findings": [],
            "malicious_code_findings": [],
            "malicious_package_findings": [],
            "artifact_findings": [],
        }

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FakeCloudClient(repository_result),
        )

        result = await tools.scan_target(
            "https://github.com/shadoprizm/cyberlens-skill",
            use_cloud=True,
        )

        assert result["success"] is True
        assert result["source"] == "cloud"
        assert result["target_type"] == "repository"
        assert result["security_score"] == 92
        assert result["trust_score"] == 98
        assert result["score"] == 92
        assert result["grade"] == "A"
        assert result["findings_count"] == 2
        assert result["repository"] == {
            "provider": "github",
            "owner": "shadoprizm",
            "name": "cyberlens-skill",
        }
        assert result["findings"][0]["source_section"] == "security_findings"
        assert result["findings"][0]["type"] == "openclaw_vulnerable_dependencies"
        assert result["findings"][1]["source_section"] == "trust_posture_findings"
        assert result["findings"][1]["type"] == "trust-posture"

    async def test_scan_repository_requires_github_url(self):
        """Test repository scans reject non-GitHub URLs."""
        from src.tools import scan_repository

        result = await scan_repository("https://example.com")

        assert result["success"] is False
        assert "GitHub repository URL" in result["error"]

    async def test_scan_repository_requires_cloud_access(self, monkeypatch):
        """Test repository scans fail cleanly when the account is not connected."""
        from src import tools

        monkeypatch.setattr(tools, "load_api_key", lambda: None)

        result = await tools.scan_repository("https://github.com/shadoprizm/cyberlens-skill")

        assert result["success"] is False
        assert result["target_type"] == "repository"
        assert "requires a connected CyberLens account" in result["error"]

    async def test_scan_repository_returns_upgrade_prompt_when_quota_is_exhausted(self, monkeypatch):
        """Repository scans should surface an upgrade prompt instead of a generic error."""
        from src import tools

        upgrade_calls = []

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FailingCloudClient(
                CyberLensQuotaExceededError(
                    "Monthly repository scan limit reached (2/2). Upgrade your plan to continue scanning immediately.",
                    upgrade_url="https://www.cyberlensai.com/pricing?source=api_quota_exceeded&quota_type=repository#plans",
                    quota_type="repository",
                    used=2,
                    limit=2,
                )
            ),
        )
        monkeypatch.setattr(tools, "open_upgrade_page", lambda url: upgrade_calls.append(url))

        result = await tools.scan_repository("https://github.com/shadoprizm/cyberlens-skill")

        assert result["success"] is False
        assert result["upgrade_required"] is True
        assert result["quota_type"] == "repository"
        assert result["quota_used"] == 2
        assert result["quota_limit"] == 2
        assert result["upgrade_url"].endswith("quota_type=repository#plans")
        assert upgrade_calls == [result["upgrade_url"]]

    async def test_scan_valid_https_site(self, monkeypatch):
        """Test scanning a valid HTTPS site."""
        from src import tools

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com",
                    score=88,
                    grade="B",
                    findings=[
                        LocalFinding(
                            type="missing-csp",
                            severity="medium",
                            description="Content-Security-Policy header is missing",
                            remediation="Add a CSP header.",
                        )
                    ],
                    technologies=["nginx"],
                    scan_time_ms=12,
                )
            ),
        )

        result = await tools.scan_website("https://example.com")

        assert result["success"] is True
        assert "url" in result
        assert "score" in result
        assert "grade" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100
        assert result["grade"] in ["A", "B", "C", "D", "F"]
        assert result["scan_mode"] == "local_quick"
        assert result["effective_scan_depth"] == "quick"
        assert "Connect a CyberLens account" in result["notice"]

    async def test_website_quota_exceeded_falls_back_locally_with_upgrade_prompt(self, monkeypatch):
        """Website scans should preserve the local fallback but still expose an upgrade prompt."""
        from src import tools

        upgrade_calls = []

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FailingCloudClient(
                CyberLensQuotaExceededError(
                    "Monthly website scan limit reached (3/3). Upgrade your plan to continue scanning immediately.",
                    upgrade_url="https://www.cyberlensai.com/pricing?source=api_quota_exceeded&quota_type=website#plans",
                    quota_type="website",
                    used=3,
                    limit=3,
                )
            ),
        )
        monkeypatch.setattr(tools, "open_upgrade_page", lambda url: upgrade_calls.append(url))
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com",
                    score=88,
                    grade="B",
                    findings=[],
                    technologies=["nginx"],
                    scan_time_ms=15,
                )
            ),
        )

        result = await tools.scan_website("https://example.com")

        assert result["success"] is True
        assert result["source"] == "local"
        assert result["cloud_quota_exceeded"] is True
        assert result["upgrade_required"] is True
        assert result["scan_mode"] == "local_quick"
        assert result["upgrade_url"].endswith("quota_type=website#plans")
        assert "fell back to the local quick scan" in result["notice"]
        assert upgrade_calls == [result["upgrade_url"]]

    async def test_website_quota_exceeded_still_falls_back_when_cloud_is_forced(self, monkeypatch):
        """Cloud-forced website scans should still degrade to the local quick scan on quota exhaustion."""
        from src import tools

        upgrade_calls = []

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FailingCloudClient(
                CyberLensQuotaExceededError(
                    "Monthly website scan limit reached (3/3). Upgrade your plan to continue scanning immediately.",
                    upgrade_url="https://www.cyberlensai.com/pricing?source=api_quota_exceeded&quota_type=website#plans",
                    quota_type="website",
                    used=3,
                    limit=3,
                )
            ),
        )
        monkeypatch.setattr(tools, "open_upgrade_page", lambda url: upgrade_calls.append(url))
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com",
                    score=84,
                    grade="B",
                    findings=[],
                    technologies=["nginx"],
                    scan_time_ms=22,
                )
            ),
        )

        result = await tools.scan_website(
            "https://example.com",
            scan_depth="deep",
            use_cloud=True,
        )

        assert result["success"] is True
        assert result["source"] == "local"
        assert result["cloud_quota_exceeded"] is True
        assert result["effective_scan_depth"] == "quick"
        assert 'Requested scan depth "deep" is not available in local mode' in result["notice"]
        assert upgrade_calls == [result["upgrade_url"]]
    
    async def test_scan_invalid_url(self):
        """Test scanning an invalid URL."""
        from src.tools import scan_website
        
        result = await scan_website("not-a-valid-url")
        
        assert result["success"] is False
        assert "error" in result
    
    async def test_scan_missing_scheme(self):
        """Test URL without scheme returns error."""
        from src.tools import scan_website
        
        result = await scan_website("example.com")
        
        assert result["success"] is False
        assert "error" in result
    
    async def test_scan_with_timeout(self, monkeypatch):
        """Test scan respects timeout parameter."""
        from src import tools

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com/slow",
                    score=0,
                    grade="F",
                    findings=[],
                    error="Request timed out after 0.1s",
                )
            ),
        )

        result = await tools.scan_website("https://example.com/slow", timeout=0.1)

        assert result["success"] is False
        assert "timeout" in result["error"].lower() or "timed out" in result["error"].lower()


@pytest.mark.asyncio
class TestGetSecurityScore:
    """Tests for get_security_score async tool."""
    
    async def test_get_score_returns_data(self, monkeypatch):
        """Test get_security_score returns expected fields."""
        from src import tools

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com",
                    score=91,
                    grade="A",
                    findings=[],
                    scan_time_ms=9,
                )
            ),
        )

        result = await tools.get_security_score("https://example.com")

        assert result["success"] is True
        assert "url" in result
        assert "score" in result
        assert "grade" in result
        assert "assessment" in result
        assert result["scan_mode"] == "local_quick"

    async def test_get_score_supports_repository_reports(self, monkeypatch):
        """Test repository score requests use the repository security score from cloud results."""
        from src import tools

        repository_result = {
            "report_type": "repository_security_assessment",
            "target": "https://github.com/shadoprizm/cyberlens-skill",
            "security_score": 88,
            "trust_score": 97,
        }

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda api_key, timeout=30.0, api_base=None: _FakeCloudClient(repository_result),
        )

        result = await tools.get_security_score("https://github.com/shadoprizm/cyberlens-skill")

        assert result["success"] is True
        assert result["target_type"] == "repository"
        assert result["score"] == 88
        assert result["security_score"] == 88
        assert result["trust_score"] == 97
        assert result["grade"] == "B"

    async def test_scan_target_uses_local_skill_scan_without_an_account(self, monkeypatch):
        """Claw Hub skill URLs should stay useful through scan_target without an account."""
        from src import tools

        async def fake_scan_skill_local(url, timeout=60.0):
            return {
                "success": True,
                "source": "local",
                "target_type": "skill",
                "url": url,
                "score": 93,
                "security_score": 93,
                "grade": "A",
                "assessment": "Looks safe.",
                "findings": [],
            }

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(tools, "scan_skill_local", fake_scan_skill_local)

        result = await tools.scan_target("https://clawhub.ai/skills/demo")

        assert result["success"] is True
        assert result["target_type"] == "skill"
        assert result["source"] == "local"
        assert "local skill package scan" in result["notice"]

    async def test_get_score_uses_local_skill_scan_without_an_account(self, monkeypatch):
        """Skill score checks should also remain available without an account."""
        from src import tools

        async def fake_scan_skill_local(url, timeout=30.0):
            return {
                "success": True,
                "source": "local",
                "target_type": "skill",
                "url": url,
                "score": 91,
                "security_score": 91,
                "grade": "A",
                "assessment": "Looks safe.",
                "findings": [],
            }

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(tools, "scan_skill_local", fake_scan_skill_local)

        result = await tools.get_security_score("https://clawhub.ai/skills/demo")

        assert result["success"] is True
        assert result["target_type"] == "skill"
        assert result["source"] == "local"
        assert result["score"] == 91
        assert result["scan_mode"] == "local_skill_package"

    async def test_scan_target_uses_local_skill_scan_with_connected_account(self, monkeypatch):
        """Skill URLs should still scan the package even when cloud access is available."""
        from src import tools

        async def fake_scan_skill_local(url, timeout=60.0):
            return {
                "success": True,
                "source": "local",
                "scan_mode": "local_skill_package",
                "coverage": "local skill package analysis",
                "target_type": "skill",
                "url": url,
                "score": 88,
                "security_score": 88,
                "grade": "B",
                "assessment": "Package reviewed.",
                "findings": [],
            }

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(tools, "scan_skill_local", fake_scan_skill_local)
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda *args, **kwargs: pytest.fail("Skill URLs should not hit the cloud scan API."),
        )

        result = await tools.scan_target("https://clawhub.ai/rexshang/skillscanner")

        assert result["success"] is True
        assert result["target_type"] == "skill"
        assert result["source"] == "local"
        assert result["scan_mode"] == "local_skill_package"
        assert "not used for Claw Hub skill URLs" in result["notice"]

    async def test_get_score_uses_local_skill_scan_with_connected_account(self, monkeypatch):
        """Skill score checks should stay package-based even when an account is connected."""
        from src import tools

        async def fake_scan_skill_local(url, timeout=30.0):
            return {
                "success": True,
                "source": "local",
                "scan_mode": "local_skill_package",
                "coverage": "local skill package analysis",
                "target_type": "skill",
                "url": url,
                "score": 89,
                "security_score": 89,
                "grade": "B",
                "assessment": "Package reviewed.",
                "findings": [],
            }

        monkeypatch.setattr(tools, "load_api_key", lambda: "clns_acct_test")
        monkeypatch.setattr(tools, "scan_skill_local", fake_scan_skill_local)
        monkeypatch.setattr(
            tools,
            "CyberLensAPIClient",
            lambda *args, **kwargs: pytest.fail("Skill URLs should not hit the cloud scan API."),
        )

        result = await tools.get_security_score("https://clawhub.ai/rexshang/skillscanner")

        assert result["success"] is True
        assert result["target_type"] == "skill"
        assert result["source"] == "local"
        assert result["score"] == 89
        assert result["scan_mode"] == "local_skill_package"
        assert "not used for Claw Hub skill URLs" in result["notice"]
    
    async def test_score_matches_grade(self, monkeypatch):
        """Test score and grade are consistent."""
        from src import tools

        monkeypatch.setattr(tools, "load_api_key", lambda: None)
        monkeypatch.setattr(
            tools,
            "SecurityScanner",
            lambda timeout=30.0: _FakeLocalScanner(
                LocalScanResult(
                    url="https://example.com",
                    score=78,
                    grade="C",
                    findings=[],
                    scan_time_ms=11,
                )
            ),
        )

        result = await tools.get_security_score("https://example.com")
        score = result["score"]
        grade = result["grade"]
        
        if score >= 90:
            assert grade == "A"
        elif score >= 80:
            assert grade == "B"
        elif score >= 70:
            assert grade == "C"
        elif score >= 60:
            assert grade == "D"
        else:
            assert grade == "F"
