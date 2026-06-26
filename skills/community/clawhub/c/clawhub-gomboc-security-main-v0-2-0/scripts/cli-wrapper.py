#!/usr/bin/env python3
"""
Gomboc Code Remediation CLI Tool

Command-line interface for scanning and fixing code issues using Gomboc.ai.
Fully functional wrapper around the Gomboc API.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

GOMBOC_PAT = os.getenv("GOMBOC_PAT")
GOMBOC_API_URL = "https://api.app.gomboc.ai/graphql"

def call_gomboc_api(query, variables=None):
    """Call Gomboc GraphQL API."""
    if not GOMBOC_PAT:
        raise RuntimeError("GOMBOC_PAT environment variable not set")
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        req = urllib.request.Request(
            GOMBOC_API_URL,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GOMBOC_PAT}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read())
            
            if "errors" in result:
                raise RuntimeError(f"Gomboc API error: {result['errors'][0]['message']}")
            
            return result.get("data", {})
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        if "401" in str(e.code):
            raise RuntimeError("Authentication failed. Check your GOMBOC_PAT.")
        raise RuntimeError(f"API error {e.code}: {error_body[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection failed: {e.reason}. Is Gomboc API available?")

def scan(args):
    """Scan code for issues."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        print("Set it with: export GOMBOC_PAT='gpt_your_token'")
        print("Get a token at: https://app.gomboc.ai/settings/tokens")
        return 1
    
    # Verify path exists
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔍 Scanning {args.path} for code issues...")
    print(f"   Policy: {args.policy}")
    print(f"   Format: {args.format}")
    
    try:
        # Call Gomboc API to scan
        query = """
        query ScanCode($path: String!, $policy: String!) {
            scan(path: $path, policy: $policy) {
                id
                path
                issueCount
                issues {
                    id
                    severity
                    title
                    description
                    file
                    line
                }
            }
        }
        """
        
        result = call_gomboc_api(query, {
            "path": args.path,
            "policy": args.policy
        })
        
        scan_data = result.get("scan", {})
        issue_count = scan_data.get("issueCount", 0)
        
        print(f"\n✅ Scan complete - Found {issue_count} issue(s)")
        
        if args.format == "json":
            print(json.dumps(scan_data, indent=2))
        elif args.format == "markdown":
            print(f"\n# Code Scan Results\n")
            for issue in scan_data.get("issues", []):
                print(f"## {issue['title']}")
                print(f"- **Severity:** {issue['severity']}")
                print(f"- **File:** {issue['file']}:{issue['line']}")
                print(f"- **Description:** {issue['description']}\n")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def fix(args):
    """Generate code fixes."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Generating fixes for {args.path}...")
    print(f"   Format: {args.format}")
    
    if args.apply:
        print("⚠️  Warning: --apply will modify your code")
    
    try:
        # First scan to get issues
        query = """
        query ScanCode($path: String!, $policy: String!) {
            scan(path: $path, policy: $policy) {
                id
                issueCount
            }
        }
        """
        
        scan_result = call_gomboc_api(query, {
            "path": args.path,
            "policy": args.policy
        })
        
        scan_id = scan_result.get("scan", {}).get("id")
        
        # Then generate fixes
        fix_query = """
        query GenerateFixes($scanId: String!, $format: String!) {
            generateFixes(scanId: $scanId, format: $format) {
                id
                issueId
                title
                description
                confidence
                code
                status
            }
        }
        """
        
        fix_result = call_gomboc_api(fix_query, {
            "scanId": scan_id,
            "format": args.format
        })
        
        fixes = fix_result.get("generateFixes", [])
        
        print(f"\n✅ Generated {len(fixes)} fix(es)")
        
        if args.format == "json":
            print(json.dumps(fixes, indent=2))
        else:
            for fix in fixes:
                print(f"\n## {fix['title']}")
                print(f"- **Confidence:** {fix['confidence']}%")
                print(f"- **Status:** {fix['status']}")
                if fix.get('code'):
                    print(f"\n```\n{fix['code']}\n```")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def remediate(args):
    """Apply fixes to code."""
    if not GOMBOC_PAT:
        print("❌ Error: GOMBOC_PAT environment variable not set")
        return 1
    
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return 1
    
    print(f"🔧 Remediating {args.path}...")
    
    if args.commit:
        print("   Will auto-commit changes")
    if args.push:
        print("   Will push to remote")
    
    try:
        query = """
        mutation ApplyFixes($path: String!, $commit: Boolean, $push: Boolean) {
            applyFixes(path: $path, commit: $commit, push: $push) {
                fixesApplied
                status
                commitHash
            }
        }
        """
        
        result = call_gomboc_api(query, {
            "path": args.path,
            "commit": args.commit,
            "push": args.push
        })
        
        remediate_data = result.get("applyFixes", {})
        fixes_applied = remediate_data.get("fixesApplied", 0)
        
        print(f"\n✅ Applied {fixes_applied} fix(es)")
        
        if args.commit:
            print(f"   Committed as: {remediate_data.get('commitHash', 'N/A')}")
        
        return 0
    
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1

def config(args):
    """Manage configuration."""
    if args.show_token:
        if GOMBOC_PAT:
            # Never print the actual token
            masked = GOMBOC_PAT[:10] + "***" if len(GOMBOC_PAT) > 10 else "***"
            print(f"✅ GOMBOC_PAT is set (masked: {masked})")
            return 0
        else:
            print("❌ GOMBOC_PAT is not set")
            print("Get a token at: https://app.gomboc.ai/settings/tokens")
            return 1
    
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gomboc Code Remediation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gomboc scan --path ./terraform
  gomboc fix --path ./src --format json
  gomboc remediate --path ./code --commit
  gomboc config --show-token
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan code for issues")
    scan_parser.add_argument("--path", required=True, help="Path to scan")
    scan_parser.add_argument("--policy", default="default", help="Policy to use")
    scan_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    scan_parser.set_defaults(func=scan)
    
    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Generate fixes")
    fix_parser.add_argument("--path", required=True, help="Path to fix")
    fix_parser.add_argument("--format", choices=["json", "markdown", "code"], default="json")
    fix_parser.add_argument("--apply", action="store_true", help="Apply fixes")
    fix_parser.set_defaults(func=fix)
    
    # Remediate command
    remediate_parser = subparsers.add_parser("remediate", help="Apply fixes to code")
    remediate_parser.add_argument("--path", required=True, help="Path to remediate")
    remediate_parser.add_argument("--commit", action="store_true", help="Auto-commit changes")
    remediate_parser.add_argument("--push", action="store_true", help="Push to remote")
    remediate_parser.set_defaults(func=remediate)
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--show-token", action="store_true", help="Show token status")
    config_parser.set_defaults(func=config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(args.func(args))
