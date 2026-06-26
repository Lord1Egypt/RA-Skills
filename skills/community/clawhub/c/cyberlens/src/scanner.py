"""Core security scanner implementation for CyberLens skill."""

import asyncio
import ssl
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import time

try:
    import httpx
except ImportError:
    raise ImportError("httpx is required. Install with: pip install httpx")

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("beautifulsoup4 is required. Install with: pip install beautifulsoup4")


@dataclass
class Finding:
    """A security finding from a scan."""
    type: str
    severity: str  # critical, high, medium, low, info
    description: str
    remediation: str
    url: Optional[str] = None
    evidence: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class ScanResult:
    """Complete result from a security scan."""
    url: str
    score: int  # 0-100
    grade: str  # A-F
    findings: List[Finding]
    headers: Dict[str, str] = field(default_factory=dict)
    technologies: List[str] = field(default_factory=list)
    scan_time_ms: int = 0
    error: Optional[str] = None


class SecurityScanner:
    """Async security scanner for websites."""
    
    # Security headers that should be present
    RECOMMENDED_HEADERS = {
        "content-security-policy": {
            "severity": "medium",
            "description": "Content-Security-Policy header is missing",
            "remediation": "Add a Content-Security-Policy header to prevent XSS and data injection attacks. Example: default-src 'self'",
        },
        "strict-transport-security": {
            "severity": "high",
            "description": "HTTP Strict Transport Security (HSTS) is not enabled",
            "remediation": "Add Strict-Transport-Security: max-age=31536000; includeSubDomains to force HTTPS connections",
        },
        "x-frame-options": {
            "severity": "medium",
            "description": "X-Frame-Options header is missing",
            "remediation": "Add X-Frame-Options: DENY or SAMEORIGIN to prevent clickjacking attacks",
        },
        "x-content-type-options": {
            "severity": "low",
            "description": "X-Content-Type-Options header is missing",
            "remediation": "Add X-Content-Type-Options: nosniff to prevent MIME sniffing",
        },
        "referrer-policy": {
            "severity": "low",
            "description": "Referrer-Policy header is missing",
            "remediation": "Add Referrer-Policy: strict-origin-when-cross-origin to control referrer information",
        },
        "permissions-policy": {
            "severity": "low",
            "description": "Permissions-Policy header is missing",
            "remediation": "Add Permissions-Policy to control browser features like camera, microphone, geolocation",
        },
    }
    
    # Technology signatures
    TECH_SIGNATURES = {
        "server": ["nginx", "apache", "cloudflare", "fastly", "akamai"],
        "x-powered-by": ["php", "asp.net", "express", "django", "rails"],
        "x-generator": ["wordpress", "drupal", "joomla", "next.js", "nuxt"],
    }
    
    def __init__(
        self,
        timeout: float = 30.0,
        max_redirects: int = 5,
        user_agent: str = "CyberLens-Skill/1.1.1",
    ):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.user_agent = user_agent
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            max_redirects=self.max_redirects,
            headers={"User-Agent": self.user_agent},
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    def _calculate_score(self, findings: List[Finding]) -> tuple[int, str]:
        """Calculate security score and grade from findings."""
        # Start at 100, deduct points for findings
        score = 100
        
        severity_weights = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3,
            "info": 0,
        }
        
        for finding in findings:
            score -= severity_weights.get(finding.severity, 0)
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        
        # Assign grade
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        return score, grade
    
    def _check_https(self, url: str, headers: Dict[str, str]) -> List[Finding]:
        """Check HTTPS configuration."""
        findings = []
        parsed = urlparse(url)
        
        if parsed.scheme != "https":
            findings.append(Finding(
                type="no-https",
                severity="critical",
                description=f"Site does not use HTTPS: {url}",
                remediation="Enable HTTPS by installing an SSL/TLS certificate. Use Let's Encrypt for free certificates.",
                references=["https://letsencrypt.org/"],
            ))
        else:
            # Check for mixed content indicator (would need page content)
            pass
        
        return findings
    
    def _check_headers(self, headers: Dict[str, str]) -> List[Finding]:
        """Check security headers."""
        findings = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        for header, config in self.RECOMMENDED_HEADERS.items():
            if header not in headers_lower:
                findings.append(Finding(
                    type=f"missing-{header.replace('-', '-')}",
                    severity=config["severity"],
                    description=config["description"],
                    remediation=config["remediation"],
                    references=["https://securityheaders.com/"],
                ))
            else:
                # Check for weak configurations
                if header == "x-frame-options":
                    value = headers_lower[header].upper()
                    if value not in ["DENY", "SAMEORIGIN"]:
                        findings.append(Finding(
                            type="weak-x-frame-options",
                            severity="medium",
                            description=f"X-Frame-Options has weak value: {value}",
                            remediation="Use DENY (strongest) or SAMEORIGIN instead of ALLOW-FROM or other values",
                        ))
        
        return findings
    
    def _detect_technologies(self, headers: Dict[str, str]) -> List[str]:
        """Detect technologies from headers."""
        technologies = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        for header, signatures in self.TECH_SIGNATURES.items():
            if header in headers_lower:
                value = headers_lower[header].lower()
                for sig in signatures:
                    if sig in value:
                        technologies.append(sig)
        
        # Check Server header
        if "server" in headers_lower:
            server = headers_lower["server"]
            if "/" in server:
                technologies.append(server.split("/")[0])
            else:
                technologies.append(server.split()[0])
        
        return list(set(technologies))
    
    def _check_information_disclosure(self, headers: Dict[str, str]) -> List[Finding]:
        """Check for information disclosure in headers."""
        findings = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        # Check X-Powered-By
        if "x-powered-by" in headers_lower:
            findings.append(Finding(
                type="information-disclosure",
                severity="low",
                description=f"X-Powered-By reveals technology: {headers_lower['x-powered-by']}",
                remediation="Remove the X-Powered-By header from server configuration to hide implementation details",
            ))
        
        # Check Server header for version info
        if "server" in headers_lower:
            server = headers_lower["server"]
            if "/" in server and any(c.isdigit() for c in server):
                findings.append(Finding(
                    type="server-version-exposed",
                    severity="low",
                    description=f"Server version information exposed: {server}",
                    remediation="Configure server to hide version numbers. In nginx: server_tokens off; in Apache: ServerTokens Prod",
                ))
        
        return findings
    
    async def _analyze_page(self, url: str, response: httpx.Response) -> List[Finding]:
        """Analyze page content for security issues."""
        findings = []
        
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Check forms
            forms = soup.find_all("form")
            for form in forms:
                action = form.get("action", "")
                method = form.get("method", "get").lower()
                
                # Check for insecure form action
                if action.startswith("http://"):
                    findings.append(Finding(
                        type="insecure-form-action",
                        severity="high",
                        description=f"Form submits to HTTP endpoint: {action}",
                        remediation="Update form action to use HTTPS",
                    ))
                
                # Check for missing CSRF token on POST forms
                if method == "post":
                    csrf_inputs = form.find_all("input", {"name": ["csrf", "csrf_token", "_token", "authenticity_token"]})
                    if not csrf_inputs:
                        findings.append(Finding(
                            type="missing-csrf-protection",
                            severity="medium",
                            description="POST form without CSRF token detected",
                            remediation="Add CSRF tokens to all state-changing forms",
                        ))
            
            # Check for inline scripts (potential XSS indicator)
            inline_scripts = soup.find_all("script", src=False)
            if len(inline_scripts) > 5:
                findings.append(Finding(
                    type="many-inline-scripts",
                    severity="info",
                    description=f"Found {len(inline_scripts)} inline scripts",
                    remediation="Consider moving scripts to external files and using CSP for better security",
                ))
        
        except Exception:
            # If parsing fails, skip content analysis
            pass
        
        return findings
    
    async def scan(self, url: str) -> ScanResult:
        """Perform a full security scan on a URL."""
        start_time = time.time()
        
        if not self._client:
            raise RuntimeError("Scanner must be used as async context manager")
        
        # Validate URL
        if not url.startswith(("http://", "https://")):
            return ScanResult(
                url=url,
                score=0,
                grade="F",
                findings=[],
                error="URL must start with http:// or https://",
                scan_time_ms=0,
            )
        
        try:
            # Make request
            response = await self._client.get(url)
            headers = dict(response.headers)
            
            # Collect all findings
            all_findings: List[Finding] = []
            
            # HTTPS check
            all_findings.extend(self._check_https(str(response.url), headers))
            
            # Header checks
            all_findings.extend(self._check_headers(headers))
            
            # Information disclosure
            all_findings.extend(self._check_information_disclosure(headers))
            
            # Page content analysis
            all_findings.extend(await self._analyze_page(str(response.url), response))
            
            # Detect technologies
            technologies = self._detect_technologies(headers)
            
            # Calculate score
            score, grade = self._calculate_score(all_findings)
            
            scan_time_ms = int((time.time() - start_time) * 1000)
            
            return ScanResult(
                url=str(response.url),
                score=score,
                grade=grade,
                findings=all_findings,
                headers=headers,
                technologies=technologies,
                scan_time_ms=scan_time_ms,
            )
        
        except httpx.TimeoutException:
            return ScanResult(
                url=url,
                score=0,
                grade="F",
                findings=[],
                error=f"Request timed out after {self.timeout}s",
                scan_time_ms=int((time.time() - start_time) * 1000),
            )
        
        except httpx.ConnectError as e:
            return ScanResult(
                url=url,
                score=0,
                grade="F",
                findings=[],
                error=f"Could not connect to {url}: {str(e)}",
                scan_time_ms=int((time.time() - start_time) * 1000),
            )
        
        except Exception as e:
            return ScanResult(
                url=url,
                score=0,
                grade="F",
                findings=[],
                error=f"Scan failed: {str(e)}",
                scan_time_ms=int((time.time() - start_time) * 1000),
            )
    
    async def get_score(self, url: str) -> tuple[int, str]:
        """Get just the security score (faster than full scan)."""
        result = await self.scan(url)
        return result.score, result.grade
