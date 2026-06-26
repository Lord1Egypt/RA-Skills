"""Custom rules example - Adding your own scan rules."""

import asyncio
from typing import List, Dict
from src.scanner import SecurityScanner, Finding


class CustomSecurityScanner(SecurityScanner):
    """Extended scanner with custom rules."""
    
    def check_custom_header(self, headers: Dict[str, str]) -> List[Finding]:
        """Check for custom application header."""
        findings = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        if "x-custom-app" in headers_lower:
            findings.append(Finding(
                type="x-custom-header-present",
                severity="info",
                description=f"Custom header detected: {headers_lower['x-custom-app']}",
                remediation="Custom headers are fine for debugging but may leak info in production",
            ))
        
        return findings
    
    def check_deprecated_server(self, headers: Dict[str, str]) -> List[Finding]:
        """Check for deprecated server versions."""
        findings = []
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        if "server" not in headers_lower:
            return findings
        
        server = headers_lower["server"].lower()
        
        # Check for known deprecated versions
        deprecated_patterns = [
            ("apache/2.2", "Apache 2.2 reached EOL in 2018"),
            ("nginx/1.8", "Nginx 1.8 is outdated, upgrade recommended"),
            ("nginx/1.6", "Nginx 1.6 is outdated, upgrade recommended"),
            ("iis/6", "IIS 6.0 is extremely outdated and insecure"),
            ("iis/7.0", "IIS 7.0 is outdated, consider upgrading"),
        ]
        
        for pattern, message in deprecated_patterns:
            if pattern in server:
                findings.append(Finding(
                    type="deprecated-server-version",
                    severity="high",
                    description=f"Deprecated server detected: {message}",
                    remediation="Upgrade to the latest stable version of your web server",
                    references=["https://endoflife.software/"],
                ))
                break
        
        return findings
    
    async def scan(self, url: str):
        """Run scan with custom rules."""
        result = await super().scan(url)
        
        if result.error:
            return result
        
        # Add custom findings
        custom_findings = []
        custom_findings.extend(self.check_custom_header(result.headers))
        custom_findings.extend(self.check_deprecated_server(result.headers))
        
        # Add custom findings to result
        result.findings.extend(custom_findings)
        
        # Recalculate score
        result.score, result.grade = self._calculate_score(result.findings)
        
        return result


def print_custom_findings(findings: List[Finding]):
    """Print only custom rule findings."""
    custom_types = [
        "x-custom-header-present",
        "deprecated-server-version",
    ]
    
    custom = [f for f in findings if f.type in custom_types]
    
    if custom:
        print("\n🔧 Custom Rule Findings:")
        for finding in custom:
            print(f"  [{finding.severity.upper()}] {finding.type}")
            print(f"    {finding.description}")
            print(f"    → {finding.remediation}")
    else:
        print("\n✅ No custom rule findings")


async def main():
    """Demonstrate custom rules."""
    url = "https://httpbin.org/get"
    
    print(f"🔍 Scanning with custom rules: {url}\n")
    
    async with CustomSecurityScanner() as scanner:
        result = await scanner.scan(url)
        
        if result.error:
            print(f"❌ Error: {result.error}")
            return
        
        print(f"Score: {result.score}/100 (Grade: {result.grade})")
        print(f"Total findings: {len(result.findings)}")
        
        # Show custom findings
        print_custom_findings(result.findings)
        
        # Show how to add your own rule
        print("\n💡 To add your own rule:")
        print("""
1. Create a subclass of SecurityScanner
2. Add a method that returns List[Finding]
3. Override scan() to call your method
4. Update the score after adding findings

Example:
    def check_my_rule(self, headers, content):
        findings = []
        if "bad-thing" in content:
            findings.append(Finding(
                type="my-custom-rule",
                severity="medium",
                description="Found bad thing",
                remediation="Remove bad thing",
            ))
        return findings
""")


if __name__ == "__main__":
    asyncio.run(main())
