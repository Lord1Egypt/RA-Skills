#!/usr/bin/env python3
"""Test script for Code Review Automation CLI."""

import sys
import subprocess

def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("Output:")
    print(result.stdout)

    if result.stderr:
        print("Errors:")
        print(result.stderr)

    return result.returncode == 0

def main():
    """Run all tests."""
    print("Code Review Automation CLI Test Suite")
    print("="*60)

    # Test 1: CLI help
    success = run_command(
        ["python", "-m", "code_review.cli", "--help"],
        "CLI help command"
    )

    # Test 2: list-prs help
    success = success and run_command(
        ["python", "-m", "code_review.cli", "list-prs", "--help"],
        "list-prs help command"
    )

    # Test 3: pr-info help
    success = success and run_command(
        ["python", "-m", "code_review.cli", "pr-info", "--help"],
        "pr-info help command"
    )

    # Test 4: pr-files help
    success = success and run_command(
        ["python", "-m", "code_review.cli", "pr-files", "--help"],
        "pr-files help command"
    )

    # Test 5: search-prs help
    success = success and run_command(
        ["python", "-m", "code_review.cli", "search-prs", "--help"],
        "search-prs help command"
    )

    # Test 6: repo-info help
    success = success and run_command(
        ["python", "-m", "code_review.cli", "repo-info", "--help"],
        "repo-info help command"
    )

    # Summary
    print("\n" + "="*60)
    if success:
        print("✓ All tests passed!")
        print("="*60)
        return 0
    else:
        print("✗ Some tests failed")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
