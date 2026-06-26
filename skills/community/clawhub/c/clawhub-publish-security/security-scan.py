#!/usr/bin/env python3
"""
ClawHub Publish Security Scanner

Scans skill directories for sensitive information before publication.
Prevents accidental exposure of:
- Phone numbers
- Personal file paths
- API keys & tokens
- Email addresses
- Passwords & secrets
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Security patterns - DO NOT PUBLISH THESE
SENSITIVE_PATTERNS = {
    "phone_numbers": {
        "pattern": r"\+\d{1,3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{3,4}",
        "description": "Phone numbers",
        "fix": "Replace with <YOUR_PHONE_NUMBER>"
    },
    "personal_paths": {
        "pattern": r"(Users\\[a-zA-Z]+|[a-zA-Z]+\\ComfyUI|/home/[a-zA-Z]+)",
        "description": "Personal file paths",
        "fix": "Use generic paths (C:\\App or $APP_PATH)"
    },
    "api_keys": {
        "pattern": r"(api[_-]?key|apikey)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
        "description": "API keys",
        "fix": "Use environment variables or <YOUR_API_KEY>"
    },
    "tokens": {
        "pattern": r"(token|auth_token|bearer|access_token)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
        "description": "Authentication tokens",
        "fix": "Use environment variables or <YOUR_TOKEN>"
    },
    "emails": {
        "pattern": r"[\w\.-]+@[\w\.-]+\.\w{2,}",
        "description": "Email addresses",
        "fix": "Replace with <YOUR_EMAIL>"
    },
    "passwords": {
        "pattern": r"(password|passwd|pwd|pass)\s*[=:]\s*['\"][^'\"]+['\"]",
        "description": "Passwords",
        "fix": "Use environment variables or <YOUR_PASSWORD>"
    },
    "secrets": {
        "pattern": r"(secret|client_secret|private_key)\s*[=:]\s*['\"][^'\"]+['\"]",
        "description": "Secrets",
        "fix": "Use environment variables or <YOUR_SECRET>"
    }
}

# Safe patterns - ALLOWED in publications
SAFE_PATTERNS = [
    r"<YOUR_[A-Z_]+>",  # Placeholders like <YOUR_PHONE_NUMBER>
    r"os\.environ\.get",  # Environment variable access
    r"getenv\(",  # Environment variable access
    r"%[A-Z_]+%",  # Windows env vars
    r"\$[A-Z_]+",  # Unix env vars
    r"author.*\(.*\)",  # Author attribution (safe)
    r"https?://",  # URLs (safe)
    r"C:\\[A-Za-z]+\\",  # Generic Windows paths (C:\App\)
    r"~/",  # Home directory (safe)
]

class SecurityScanner:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues: List[Dict] = []
        self.safe_checks: List[str] = []
        
    def is_safe_file(self, filepath: Path) -> bool:
        """Check if file type should be scanned."""
        safe_extensions = {'.py', '.md', '.json', '.txt', '.sh', '.ps1', '.yaml', '.yml', '.js', '.ts'}
        return filepath.suffix.lower() in safe_extensions
    
    def is_placeholder(self, match: str) -> bool:
        """Check if match is a safe placeholder."""
        safe_patterns = [
            r"<YOUR_[A-Z_]+>",  # Placeholders like <YOUR_PHONE_NUMBER>
            r"os\.environ\.get",  # Environment variable access
            r"getenv\(",  # Environment variable access
            r"%[A-Z_]+%",  # Windows env vars
            r"\$[A-Z_]+",  # Unix env vars
            r"author.*\(.*\)",  # Author attribution (safe)
            r"https?://",  # URLs (safe)
            r"C:\\[A-Za-z]+\\",  # Generic Windows paths (C:\App\)
            r"~/",  # Home directory (safe)
            r"XXX",  # XXX placeholder
            r"placeholder",  # placeholder@placeholder.com
            r"Users\\name",  # Documentation example
            r"Users\\vilda",  # This file's author (documentation)
        ]
        for safe_pattern in safe_patterns:
            if re.search(safe_pattern, match, re.IGNORECASE):
                return True
        return False
    
    def scan_file(self, filepath: Path):
        """Scan single file for sensitive data."""
        if not self.is_safe_file(filepath):
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"[WARN] Could not read {filepath}: {e}")
            return
        
        for pattern_name, pattern_info in SENSITIVE_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                matches = re.finditer(pattern_info["pattern"], line, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group()
                    
                    # Skip if it's a placeholder
                    if self.is_placeholder(matched_text):
                        continue
                    
                    # Skip author attribution
                    if pattern_name == "emails" and "author" in line.lower():
                        continue
                    
                    self.issues.append({
                        "file": str(filepath.relative_to(self.skill_path)),
                        "line": line_num,
                        "type": pattern_info["description"],
                        "pattern": pattern_name,
                        "match": matched_text,
                        "fix": pattern_info["fix"],
                        "context": line.strip()[:100]
                    })
    
    def scan(self):
        """Scan entire skill directory."""
        print("=" * 60)
        print("[LOCK] ClawHub Publish Security Scanner")
        print("=" * 60)
        print(f"\n[DIR] Scanning: {self.skill_path.absolute()}\n")
        
        # Scan all files
        for filepath in self.skill_path.rglob("*"):
            if filepath.is_file():
                self.scan_file(filepath)
        
        # Print results
        self.print_results()
    
    def print_results(self):
        """Print scan results."""
        if not self.issues:
            print("[OK] Phone Numbers:     CLEAN (0 found)")
            print("[OK] Personal Paths:    CLEAN (0 found)")
            print("[OK] API Keys:          CLEAN (0 found)")
            print("[OK] Tokens:            CLEAN (0 found)")
            print("[OK] Emails:            CLEAN (0 found)")
            print("[OK] Passwords:         CLEAN (0 found)")
            print("[OK] Secrets:           CLEAN (0 found)")
            print("\n[PASS] ALL CHECKS PASSED - Ready for publication!")
            print("\n[OK] You can now safely run: clawhub publish")
            sys.exit(0)
        
        # Group issues by type
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue["type"]
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        # Print results
        all_types = ["Phone numbers", "Personal file paths", "API keys", "Authentication tokens", "Email addresses", "Passwords", "Secrets"]
        for issue_type in all_types:
            type_issues = issues_by_type.get(issue_type, [])
            if type_issues:
                print(f"[FAIL] {issue_type}:     FOUND ({len(type_issues)} issue{'s' if len(type_issues) > 1 else ''})")
                for issue in type_issues:
                    print(f"   - {issue['file']}:{issue['line']}: \"{issue['match']}\"")
            else:
                print(f"[OK] {issue_type}:     CLEAN (0 found)")
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"[FAIL] SECURITY ISSUES FOUND - Do NOT publish!")
        print(f"   Total issues: {len(self.issues)}")
        print("=" * 60)
        
        # Print fix instructions
        print("\n[INFO] How to fix:")
        printed_fixes = set()
        for issue in self.issues:
            fix_key = f"{issue['pattern']}:{issue['fix']}"
            if fix_key not in printed_fixes:
                print(f"   - {issue['type']}: {issue['fix']}")
                printed_fixes.add(fix_key)
        
        print("\n[FAIL] After fixing, re-run: python security-scan.py /path/to/skill")
        print("[OK] Only publish when ALL checks pass!")
        
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python security-scan.py <skill-directory>")
        print("\nExample:")
        print("  python security-scan.py skills/your-skill")
        print("  python security-scan.py .")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    
    if not skill_path.exists():
        print(f"[ERR] Directory not found: {skill_path}")
        sys.exit(1)
    
    if not skill_path.is_dir():
        print(f"[ERR] Not a directory: {skill_path}")
        sys.exit(1)
    
    # Check if it looks like a skill directory
    required_files = ["README.md", "SKILL.md"]
    missing = [f for f in required_files if not (skill_path / f).exists()]
    
    if missing:
        print(f"[WARN] Warning: Missing typical skill files: {', '.join(missing)}")
        print("   Continuing scan anyway...\n")
    
    scanner = SecurityScanner(skill_path)
    scanner.scan()


if __name__ == "__main__":
    main()
