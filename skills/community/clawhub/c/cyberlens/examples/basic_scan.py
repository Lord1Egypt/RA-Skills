"""Basic scan example - Single URL security scan."""

import asyncio
from src.scanner import SecurityScanner


async def main():
    """Run a basic security scan."""
    url = "https://example.com"
    
    print(f"🔍 Scanning {url}...\n")
    
    async with SecurityScanner() as scanner:
        result = await scanner.scan(url)
        
        if result.error:
            print(f"❌ Scan failed: {result.error}")
            return
        
        # Print summary
        print(f"✅ Scan complete in {result.scan_time_ms}ms")
        print(f"📊 Security Score: {result.score}/100 (Grade: {result.grade})")
        
        # Print technologies
        if result.technologies:
            print(f"🔧 Detected: {', '.join(result.technologies)}")
        
        # Print findings
        if result.findings:
            print(f"\n⚠️  Found {len(result.findings)} issue(s):\n")
            
            # Group by severity
            by_severity = {}
            for finding in result.findings:
                sev = finding.severity
                by_severity.setdefault(sev, []).append(finding)
            
            for severity in ["critical", "high", "medium", "low", "info"]:
                if severity in by_severity:
                    print(f"  {severity.upper()}:")
                    for finding in by_severity[severity]:
                        print(f"    • {finding.description}")
                        print(f"      Fix: {finding.remediation}")
        else:
            print("\n✨ No security issues found!")


if __name__ == "__main__":
    asyncio.run(main())
