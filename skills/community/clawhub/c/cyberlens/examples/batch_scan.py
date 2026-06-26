"""Batch scan example - Scan multiple URLs and generate a report."""

import asyncio
from typing import List
from dataclasses import dataclass
from src.scanner import SecurityScanner, ScanResult


@dataclass
class SiteResult:
    """Result for a single site in batch scan."""
    url: str
    score: int
    grade: str
    issues: int
    error: str = None


async def scan_single(url: str, scanner: SecurityScanner) -> SiteResult:
    """Scan a single URL and return simplified result."""
    result = await scanner.scan(url)
    
    if result.error:
        return SiteResult(url=url, score=0, grade="F", issues=0, error=result.error)
    
    return SiteResult(
        url=result.url,
        score=result.score,
        grade=result.grade,
        issues=len(result.findings),
    )


async def batch_scan(urls: List[str], max_concurrent: int = 3) -> List[SiteResult]:
    """Scan multiple URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def scan_with_limit(url: str, scanner: SecurityScanner) -> SiteResult:
        async with semaphore:
            return await scan_single(url, scanner)
    
    async with SecurityScanner() as scanner:
        tasks = [scan_with_limit(url, scanner) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results


def print_report(results: List[SiteResult]):
    """Print a formatted report of batch scan results."""
    print("\n" + "=" * 70)
    print("📊 BATCH SCAN REPORT")
    print("=" * 70)
    
    # Summary stats
    total = len(results)
    successful = sum(1 for r in results if r.error is None)
    failed = total - successful
    avg_score = sum(r.score for r in results if r.error is None) / successful if successful > 0 else 0
    
    print(f"\n📈 Summary:")
    print(f"   Total sites: {total}")
    print(f"   Successful:  {successful}")
    print(f"   Failed:      {failed}")
    print(f"   Avg score:   {avg_score:.1f}/100")
    
    # Grade distribution
    grades = {}
    for r in results:
        if r.error is None:
            grades[r.grade] = grades.get(r.grade, 0) + 1
    
    print(f"\n📋 Grade Distribution:")
    for grade in ["A", "B", "C", "D", "F"]:
        count = grades.get(grade, 0)
        bar = "█" * count + "░" * (successful - count if successful > 0 else 0)
        print(f"   {grade}: {bar} ({count})")
    
    # Detailed results
    print(f"\n📑 Results:")
    print("-" * 70)
    
    # Sort by score (best first)
    sorted_results = sorted(results, key=lambda r: (-r.score, r.url))
    
    for result in sorted_results:
        status = "✅" if result.error is None else "❌"
        if result.error:
            print(f"{status} {result.url[:50]:<50} ERROR: {result.error[:20]}")
        else:
            grade_emoji = {"A": "🟢", "B": "🟢", "C": "🟡", "D": "🟠", "F": "🔴"}[result.grade]
            print(f"{status} {result.url[:50]:<50} {grade_emoji} {result.grade} ({result.score}) {result.issues} issues")
    
    print("=" * 70)


async def main():
    """Run batch scan on multiple URLs."""
    urls = [
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
        "https://example.com",
        "https://httpbin.org/get",
    ]
    
    print(f"🚀 Starting batch scan of {len(urls)} URLs...")
    print(f"   (Max concurrent: 3)\n")
    
    results = await batch_scan(urls, max_concurrent=3)
    print_report(results)
    
    # Save to JSON
    import json
    report_data = [
        {
            "url": r.url,
            "score": r.score,
            "grade": r.grade,
            "issues": r.issues,
            "error": r.error,
        }
        for r in results
    ]
    
    with open("batch_scan_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print("\n💾 Report saved to batch_scan_report.json")


if __name__ == "__main__":
    asyncio.run(main())
