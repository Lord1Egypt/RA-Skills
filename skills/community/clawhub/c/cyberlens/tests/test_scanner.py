"""Tests for CyberLens scanner module."""

import pytest
import httpx
from src import __version__
from src import scanner as scanner_module
from src.scanner import SecurityScanner, Finding, ScanResult


class _FakeAsyncClient:
    """Minimal async HTTP client stub for scanner tests."""

    def __init__(self, response=None, error=None):
        self._response = response
        self._error = error

    async def get(self, url):
        if self._error:
            raise self._error
        return self._response

    async def aclose(self):
        return None


def _build_response(url: str, headers=None, text: str = "<html></html>") -> httpx.Response:
    """Create an httpx response with an attached request and URL."""
    return httpx.Response(
        200,
        headers=headers or {},
        text=text,
        request=httpx.Request("GET", url),
    )


def _patch_async_client(monkeypatch, response=None, error=None):
    """Patch the scanner's AsyncClient factory with a deterministic stub."""
    monkeypatch.setattr(
        scanner_module.httpx,
        "AsyncClient",
        lambda *args, **kwargs: _FakeAsyncClient(response=response, error=error),
    )


class TestFinding:
    """Tests for Finding dataclass."""
    
    def test_finding_creation(self):
        """Test creating a Finding."""
        finding = Finding(
            type="test-finding",
            severity="high",
            description="Test description",
            remediation="Fix it",
        )
        
        assert finding.type == "test-finding"
        assert finding.severity == "high"
        assert finding.description == "Test description"
        assert finding.remediation == "Fix it"
        assert finding.references == []
    
    def test_finding_with_references(self):
        """Test creating a Finding with references."""
        finding = Finding(
            type="test-finding",
            severity="medium",
            description="Test",
            remediation="Fix",
            references=["https://example.com"],
        )
        
        assert finding.references == ["https://example.com"]


class TestScanResult:
    """Tests for ScanResult dataclass."""
    
    def test_scan_result_creation(self):
        """Test creating a ScanResult."""
        result = ScanResult(
            url="https://example.com",
            score=85,
            grade="B",
            findings=[],
        )
        
        assert result.url == "https://example.com"
        assert result.score == 85
        assert result.grade == "B"
        assert result.findings == []
    
    def test_scan_result_with_findings(self):
        """Test ScanResult with findings."""
        finding = Finding(
            type="test",
            severity="low",
            description="Test finding",
            remediation="Fix it",
        )
        
        result = ScanResult(
            url="https://example.com",
            score=90,
            grade="A",
            findings=[finding],
        )
        
        assert len(result.findings) == 1
        assert result.findings[0].type == "test"


class TestSecurityScannerInit:
    """Tests for SecurityScanner initialization."""
    
    def test_default_init(self):
        """Test default initialization."""
        scanner = SecurityScanner()
        
        assert scanner.timeout == 30.0
        assert scanner.max_redirects == 5
        assert scanner.user_agent == f"CyberLens-Skill/{__version__}"
    
    def test_custom_init(self):
        """Test initialization with custom values."""
        scanner = SecurityScanner(
            timeout=60.0,
            max_redirects=10,
            user_agent="CustomAgent/1.0",
        )
        
        assert scanner.timeout == 60.0
        assert scanner.max_redirects == 10
        assert scanner.user_agent == "CustomAgent/1.0"


class TestCalculateScore:
    """Tests for score calculation."""
    
    def test_perfect_score(self):
        """Test score with no findings."""
        scanner = SecurityScanner()
        score, grade = scanner._calculate_score([])
        
        assert score == 100
        assert grade == "A"
    
    def test_critical_finding(self):
        """Test score with critical finding."""
        scanner = SecurityScanner()
        finding = Finding(
            type="test",
            severity="critical",
            description="Test",
            remediation="Fix",
        )
        score, grade = scanner._calculate_score([finding])
        
        assert score == 75
        assert grade == "C"
    
    def test_multiple_findings(self):
        """Test score with multiple findings."""
        scanner = SecurityScanner()
        findings = [
            Finding(type="h1", severity="high", description="High", remediation="Fix"),
            Finding(type="m1", severity="medium", description="Medium", remediation="Fix"),
            Finding(type="l1", severity="low", description="Low", remediation="Fix"),
        ]
        score, grade = scanner._calculate_score(findings)
        
        assert score == 100 - 15 - 8 - 3  # 74
        assert grade == "C"
    
    def test_minimum_score(self):
        """Test score doesn't go below 0."""
        scanner = SecurityScanner()
        findings = [
            Finding(type=f"c{i}", severity="critical", description="Critical", remediation="Fix")
            for i in range(10)
        ]
        score, grade = scanner._calculate_score(findings)
        
        assert score == 0
        assert grade == "F"


class TestCheckHTTPS:
    """Tests for HTTPS checking."""
    
    def test_http_url(self):
        """Test HTTP URL generates finding."""
        scanner = SecurityScanner()
        findings = scanner._check_https("http://example.com", {})
        
        assert len(findings) == 1
        assert findings[0].type == "no-https"
        assert findings[0].severity == "critical"
    
    def test_https_url(self):
        """Test HTTPS URL has no findings."""
        scanner = SecurityScanner()
        findings = scanner._check_https("https://example.com", {})
        
        assert len(findings) == 0


class TestCheckHeaders:
    """Tests for header security checks."""
    
    def test_all_headers_present(self):
        """Test no findings when all headers present."""
        scanner = SecurityScanner()
        headers = {
            "Content-Security-Policy": "default-src 'self'",
            "Strict-Transport-Security": "max-age=31536000",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin",
            "Permissions-Policy": "camera=()",
        }
        findings = scanner._check_headers(headers)
        
        assert len(findings) == 0
    
    def test_missing_all_headers(self):
        """Test findings when all headers missing."""
        scanner = SecurityScanner()
        findings = scanner._check_headers({})
        
        assert len(findings) == 6  # All 6 recommended headers
        severities = [f.severity for f in findings]
        assert "high" in severities  # HSTS is high
        assert "medium" in severities  # CSP and X-Frame-Options are medium
    
    def test_weak_x_frame_options(self):
        """Test weak X-Frame-Options value."""
        scanner = SecurityScanner()
        headers = {
            "X-Frame-Options": "ALLOW-FROM https://example.com",
        }
        findings = scanner._check_headers(headers)
        
        weak_framing = [f for f in findings if f.type == "weak-x-frame-options"]
        assert len(weak_framing) == 1


class TestDetectTechnologies:
    """Tests for technology detection."""
    
    def test_nginx_detection(self):
        """Test nginx server detection."""
        scanner = SecurityScanner()
        headers = {"Server": "nginx/1.18.0"}
        techs = scanner._detect_technologies(headers)
        
        assert "nginx" in techs
    
    def test_php_detection(self):
        """Test PHP detection via X-Powered-By."""
        scanner = SecurityScanner()
        headers = {"X-Powered-By": "PHP/7.4.3"}
        techs = scanner._detect_technologies(headers)
        
        assert "php" in techs
    
    def test_multiple_technologies(self):
        """Test detection of multiple technologies."""
        scanner = SecurityScanner()
        headers = {
            "Server": "nginx/1.18.0",
            "X-Powered-By": "Express",
        }
        techs = scanner._detect_technologies(headers)
        
        assert "nginx" in techs
        assert "express" in techs


class TestInformationDisclosure:
    """Tests for information disclosure detection."""
    
    def test_x_powered_by_detected(self):
        """Test X-Powered-By detection."""
        scanner = SecurityScanner()
        headers = {"X-Powered-By": "PHP/7.4"}
        findings = scanner._check_information_disclosure(headers)
        
        assert len(findings) >= 1
        xpb = [f for f in findings if "x-powered-by" in f.type or "information-disclosure" in f.type]
        assert len(xpb) >= 1
    
    def test_server_version_detected(self):
        """Test Server version detection."""
        scanner = SecurityScanner()
        headers = {"Server": "Apache/2.4.41"}
        findings = scanner._check_information_disclosure(headers)
        
        version_finding = [f for f in findings if "version" in f.type]
        assert len(version_finding) >= 1


@pytest.mark.asyncio
class TestAsyncScan:
    """Tests for async scan functionality."""
    
    async def test_scan_valid_url(self, monkeypatch):
        """Test scanning a valid URL."""
        _patch_async_client(
            monkeypatch,
            response=_build_response(
                "https://example.com",
                headers={
                    "Content-Security-Policy": "default-src 'self'",
                    "Strict-Transport-Security": "max-age=31536000",
                    "X-Frame-Options": "DENY",
                    "X-Content-Type-Options": "nosniff",
                    "Referrer-Policy": "strict-origin",
                    "Permissions-Policy": "camera=()",
                    "Server": "nginx",
                },
                text="<html><body>Hello</body></html>",
            ),
        )

        async with SecurityScanner() as scanner:
            result = await scanner.scan("https://example.com")
            
            assert isinstance(result, ScanResult)
            assert result.error is None
            assert 0 <= result.score <= 100
            assert result.grade in ["A", "B", "C", "D", "F"]
            assert result.scan_time_ms >= 0
    
    async def test_scan_invalid_url(self):
        """Test scanning invalid URL format."""
        async with SecurityScanner() as scanner:
            result = await scanner.scan("not-a-url")
            
            assert result.error is not None
            assert "http://" in result.error or "https://" in result.error
    
    async def test_scan_timeout(self, monkeypatch):
        """Test scan timeout handling."""
        _patch_async_client(
            monkeypatch,
            error=httpx.TimeoutException("Request timed out"),
        )

        async with SecurityScanner(timeout=0.1) as scanner:
            result = await scanner.scan("https://example.com/slow")
            
            assert result.error is not None
            assert "timeout" in result.error.lower() or "timed out" in result.error.lower()
    
    async def test_get_score(self, monkeypatch):
        """Test get_score method."""
        _patch_async_client(
            monkeypatch,
            response=_build_response(
                "https://example.com",
                headers={"Server": "nginx"},
            ),
        )

        async with SecurityScanner() as scanner:
            score, grade = await scanner.get_score("https://example.com")
            
            assert isinstance(score, int)
            assert 0 <= score <= 100
            assert grade in ["A", "B", "C", "D", "F"]
