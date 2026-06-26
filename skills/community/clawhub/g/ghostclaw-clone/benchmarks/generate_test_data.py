"""
Generate synthetic analysis reports for QMD benchmark testing.

Creates N dummy reports with realistic JSON structure and varied content.
"""

import argparse
import asyncio
import json
import random
import time
from pathlib import Path

from ghostclaw.core.adapters.storage.qmd import QMDStorageAdapter
from ghostclaw.core.qmd_store import QMDMemoryStore

SAMPLE_ISSUES = [
    "Potential SQL injection in user input handling",
    "Missing authentication on sensitive endpoint",
    "Memory leak in event handler",
    "Race condition in shared resource access",
    "Unvalidated user input leading to XSS",
    "Hardcoded credentials in configuration",
    "Insecure direct object reference",
    "Buffer overflow in string concatenation",
    "Improper error handling exposing stack traces",
    "Unencrypted sensitive data transmission",
]

STACKS = ["python", "javascript", "go", "rust", "java"]

async def generate_reports(store: QMDMemoryStore, count: int, repo_path: str):
    """Generate and save synthetic reports."""
    print(f"Generating {count} synthetic reports...")
    for i in range(count):
        # Simulate a realistic report
        vibe_score = random.randint(60, 95)
        stack = random.choice(STACKS)
        files_analyzed = random.randint(10, 200)
        total_lines = random.randint(500, 5000)
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - random.randint(0, 30*24*3600)))

        # Create a report with chunks (issues)
        issues = random.sample(SAMPLE_ISSUES, k=random.randint(1, 5))
        report = {
            "metadata": {
                "repo_path": repo_path,
                "timestamp": timestamp,
                "vibe_score": vibe_score,
                "stack": [stack],
                "files_analyzed": files_analyzed,
                "total_lines": total_lines,
                "vcs_commit": f"abc{i:04d}",
                "vcs_branch": "main"
            },
            "issues": [
                {
                    "type": random.choice(["security", "performance", "maintainability"]),
                    "title": issue,
                    "description": f"Detailed description of {issue} with context and recommendations.",
                    "file": f"src/{random.choice(['main', 'utils', 'api', 'core'])}.py",
                    "line": random.randint(1, 500)
                }
                for issue in issues
            ],
            "ghosts": [],
            "flags": [],
            "ai_synthesis": f"Overall assessment: The codebase shows {['good', 'fair', 'excellent'][random.randint(0,2)]} practices. Focus on {random.choice(['security hardening', 'performance tuning', 'documentation'])}."
        }

        # Generate unique report_id
        report_id = i + 1

        # Save via store (this will trigger embedding generation if enhanced)
        await store.save_run(report, repo_path=repo_path)

        if (i+1) % 10 == 0:
            print(f"  Generated {i+1}/{count}...")

    print(f"✅ Done. Total reports: {count}")

async def main():
    parser = argparse.ArgumentParser(description="Generate synthetic QMD reports")
    parser.add_argument("repo", type=Path, help="Repository root path")
    parser.add_argument("--count", type=int, default=500, help="Number of reports to generate")
    parser.add_argument("--use-qmd", action="store_true", help="Use QMD backend (requires fastembed/lancedb)")
    args = parser.parse_args()

    # We'll bypass the adapter and directly use QMDMemoryStore for generation
    db_path = args.repo / ".ghostclaw" / "storage" / "qmd" / "ghostclaw.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    store = QMDMemoryStore(
        db_path=db_path,
        use_enhanced=args.use_qmd,
        embedding_backend="fastembed",
        ai_buff_enabled=False
    )
    # Vector store will initialize on first use

    await generate_reports(store, args.count, str(args.repo))

if __name__ == "__main__":
    asyncio.run(main())
