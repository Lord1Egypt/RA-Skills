#!/usr/bin/env python3
"""
Sanitize Session Transcripts — Redacts sensitive data from JSON/JSONL transcript files.

This script redacts:
- API keys and tokens (GitHub, AWS, OpenAI, generic Bearer tokens, etc.)
- Email addresses
- Phone numbers
- IP addresses (IPv4 and IPv6)
- Hostnames and internal domain names
- Generic secrets/credentials patterns

IMPORTANT: This script NEVER modifies the original file. Output goes to stdout or a specified output file.

Usage:
    python3 sanitize_transcript.py < input.jsonl > sanitized.jsonl
    python3 sanitize_transcript.py input.jsonl -o sanitized.jsonl
    python3 sanitize_transcript.py --help

The script is DETERMINISTIC: same input always produces same output.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# =============================================================================
# REDACTION PATTERNS — Allowlist approach
# Each pattern is a compiled regex with a clear description.
# =============================================================================

REDACTION_PATTERNS = [
    # -------------------------------------------------------------------------
    # API Keys & Tokens
    # -------------------------------------------------------------------------
    (
        r'\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b',
        '[REDACTED-GITHUB-TOKEN]',
        'GitHub personal access tokens (ghp_, gho_, ghu_, ghs_, ghr_)',
    ),
    (
        r'\b(github_pat_[A-Za-z0-9_]{22,})\b',
        '[REDACTED-GITHUB-PAT]',
        'GitHub fine-grained PATs',
    ),
    (
        r'\b(akpk|[Aa]pi[_-]?[Kk]ey)[_-]?[A-Za-z0-9]{16,}\b',
        '[REDACTED-API-KEY]',
        'Generic API key patterns (apikey_xxx, api-key-xxx)',
    ),
    (
        r'\b(Bearer\s+[A-Za-z0-9_\-\.]{20,})',
        'Bearer [REDACTED]',
        'Bearer authorization tokens',
    ),
    (
        r'\b(ghs_[A-Za-z0-9_]{36,})\b',
        '[REDACTED-GITHUB-TOKEN]',
        'GitHub server access tokens',
    ),
    (
        r'\b(EAACEdE[0-9A-Za-z\-_]{200,})\b',
        '[REDACTED-FACEBOOK-TOKEN]',
        'Facebook access tokens',
    ),
    (
        r'\b(ya29\.[A-Za-z0-9_\-]{100,})\b',
        '[REDACTED-GOOGLE-TOKEN]',
        'Google OAuth tokens (ya29.)',
    ),
    (
        r'\b(AIza[0-9A-Za-z\-_]{35,})\b',
        '[REDACTED-GOOGLE-API]',
        'Google API keys (AIza...)',
    ),
    (
        r'\b(sk\-[A-Za-z0-9_\-]{48,})\b',
        '[REDACTED-OPENAI-KEY]',
        'OpenAI API keys (sk-...)',
    ),
    (
        r'\b(sk-proj-[A-Za-z0-9_\-]{48,})\b',
        '[REDACTED-OPENAI-PROJ-KEY]',
        'OpenAI project keys (sk-proj-...)',
    ),
    (
        r'\b(sk-ant-[A-Za-z0-9_\-]{48,})\b',
        '[REDACTED-ANTHROPIC-KEY]',
        'Anthropic/Claude API keys (sk-ant-...)',
    ),
    (
        r'\b(aws_access_key_id|aws_secret_access_key)\s*[=:]\s*[A-Za-z0-9/+=]{20,}\b',
        'AWS_ACCESS_KEY_ID=[REDACTED]',
        'AWS credentials',
    ),
    (
        r'\b(AC[a-zA-Z0-9]{32,})\b',
        '[REDACTED-STRIPE-KEY]',
        'Stripe access keys (Ac...)',
    ),
    (
        # Generic high-entropy secret pattern — only redact if clearly a secret
        # Matches strings that look like base64 or hex secrets, 32+ chars
        r'\b([A-Za-z0-9+/]{64,}={0,2})\b',
        '[REDACTED-SECRET]',
        'High-entropy base64 secrets (64+ chars)',
    ),
    (
        r'\b([0-9a-f]{64})\b',
        '[REDACTED-HEX-SECRET]',
        '64-char hex secrets (比特币-style)',
    ),

    # -------------------------------------------------------------------------
    # Email Addresses
    # -------------------------------------------------------------------------
    (
        r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b',
        '[REDACTED-EMAIL]',
        'Email addresses',
    ),

    # -------------------------------------------------------------------------
    # Phone Numbers — Various international formats
    # -------------------------------------------------------------------------
    (
        r'\b(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})\b',
        '[REDACTED-PHONE]',
        'US/Canada phone numbers',
    ),
    (
        r'\b(\+?[0-9]{1,3}[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4})\b',
        '[REDACTED-PHONE]',
        'International phone numbers',
    ),

    # -------------------------------------------------------------------------
    # IP Addresses
    # -------------------------------------------------------------------------
    (
        r'\b((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\b',
        '[REDACTED-IP]',
        'IPv4 addresses',
    ),
    (
        r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
        '[REDACTED-IPV6]',
        'IPv6 addresses (full)',
    ),
    (
        r'\b([0-9a-fA-F]{1,4}:){1,7}:\b',
        '[REDACTED-IPV6]',
        'IPv6 addresses (compressed)',
    ),

    # -------------------------------------------------------------------------
    # Hostnames & Internal Domains
    # -------------------------------------------------------------------------
    (
        r'\b([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+(local|internal|private|intranet|lan)\b',
        '[REDACTED-HOSTNAME]',
        'Internal/private hostnames',
    ),
    (
        r'\b(ip-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3})\b',
        '[REDACTED-HOSTNAME]',
        'AWS EC2 hostnames (ip-xxx-xxx-xxx-xxx)',
    ),
    (
        r'\b(ec2-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3})\b',
        '[REDACTED-HOSTNAME]',
        'AWS EC2 DNS names',
    ),
    (
        r'\b([a-zA-Z0-9\-]{1,50}\.amazonaws\.com)\b',
        '[REDACTED-AWS-HOST]',
        'AWS service hostnames',
    ),

    # -------------------------------------------------------------------------
    # Generic Credential Patterns in URLs/Environment Variables
    # -------------------------------------------------------------------------
    (
        r'([A-Za-z0-9_-]*(?:password|passwd|pwd|secret|token|auth)[A-Za-z0-9_-]*)\s*[=:]\s*[^\s\"\';,]{8,}',
        r'\1=[REDACTED]',
        'Environment variable credentials (password=, token=, secret=, etc.)',
    ),
    (
        r'://[^:\s]+:[^@\s]+@[a-zA-Z0-9.\-]+',
        '://[REDACTED]@[host]',
        'Basic auth credentials in URLs (user:pass@host)',
    ),
]

# Strict mode patterns — additional checks when --strict is enabled
STRICT_PATTERNS = [
    # Lines containing sensitive keywords — redact the entire line
    (
        r'.*\b(token|secret|key|password|credential)s?\b.*',
        '[REDACTED-STRICT]',
        'Lines containing sensitive keywords (token, secret, key, password, credential)',
    ),
    # HTTP Authorization headers
    (
        r'.*Authorization:.*',
        '[REDACTED-AUTH-HEADER]',
        'HTTP Authorization headers',
    ),
]


def redact_text(text: str, strict: bool = False) -> str:
    """
    Apply all redaction patterns to a text string.
    Returns the redacted string.
    """
    result = str(text)
    for pattern, replacement, description in REDACTION_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    if strict:
        for pattern, replacement, description in STRICT_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def sanitize_value(value: Any, strict: bool = False) -> Any:
    """
    Recursively sanitize a value, preserving structure.
    - Strings are redacted
    - Dicts preserve keys, redact values
    - Lists sanitize each element
    """
    if isinstance(value, str):
        return redact_text(value, strict=strict)
    elif isinstance(value, dict):
        return {k: sanitize_value(v, strict=strict) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_value(item, strict=strict) for item in value]
    else:
        # int, float, bool, None — return as-is
        return value


def process_jsonl(input_path: Path, output_handle, strict: bool = False) -> int:
    """
    Process a JSONL file, sanitizing each line.
    Returns the number of records processed.
    """
    count = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                sanitized = sanitize_value(record, strict=strict)
                output_handle.write(json.dumps(sanitized, ensure_ascii=False) + '\n')
                count += 1
            except json.JSONDecodeError as e:
                if strict:
                    redacted = redact_text(line)
                    raise RuntimeError(f"JSON parse error on line {line_num} (line was sanitized before error): {e}\nSanitized: {redacted[:200]}")
                # Non-JSON lines are still sanitized before being passed through
                output_handle.write(redact_text(line) + '\n')
    return count


def process_json(input_path: Path, output_handle, strict: bool = False) -> int:
    """
    Process a JSON file (array or object), sanitizing all strings.
    Returns the number of records processed.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sanitized = sanitize_value(data, strict=strict)
    
    if isinstance(sanitized, list):
        for item in sanitized:
            output_handle.write(json.dumps(item, ensure_ascii=False) + '\n')
        return len(sanitized)
    else:
        output_handle.write(json.dumps(sanitized, ensure_ascii=False) + '\n')
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Sanitize session transcripts — redact API keys, emails, IPs, hostnames, and credentials.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        'input',
        nargs='?',
        type=Path,
        default=None,
        help='Input JSONL or JSON file (reads from stdin if not specified)',
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        dest='output',
        help='Output file (writes to stdout if not specified)',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on JSON parse errors instead of passing through',
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run built-in tests and exit',
    )

    args = parser.parse_args()

    # Built-in test mode
    if args.test:
        test_cases = [
            (
                '{"content": [{"text": "token ghp_abcdefghijklmnopqrstuvwxyz12345678901234567890 email test@example.com ip 192.168.1.1"}]}',
                '[REDACTED-GITHUB-TOKEN]',
                '[REDACTED-EMAIL]',
                '[REDACTED-IP]',
            ),
            (
                '{"text": "API key sk-1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz"}',
                '[REDACTED-OPENAI-KEY]',
            ),
            (
                '{"text": "Connecting to ec2-12-34-56-78.compute-1.amazonaws.com from 10.0.1.100"}',
                '[REDACTED-HOSTNAME]',
                '[REDACTED-IP]',
            ),
        ]
        print("Running built-in tests...")
        passed = 0
        failed = 0
        for json_str, *expected_substrings in test_cases:
            result = sanitize_value(json.loads(json_str))
            result_str = json.dumps(result)
            ok = all(sub in result_str for sub in expected_substrings)
            status = "PASS" if ok else "FAIL"
            print(f"  {status}: {json_str[:60]}...")
            if not ok:
                print(f"    Got: {result_str[:100]}")
                failed += 1
            else:
                passed += 1
        print(f"\n{passed}/{passed+failed} tests passed.")
        if failed:
            sys.exit(1)
        return

    # Determine input source
    if args.input:
        input_handle = open(args.input, 'r', encoding='utf-8')
    elif not sys.stdin.isatty():
        input_handle = sys.stdin
    else:
        parser.print_help()
        print("\nError: No input provided. Pass a file path or pipe data via stdin.", file=sys.stderr)
        sys.exit(1)
        return

    # Determine output destination
    if args.output:
        output_handle = open(args.output, 'w', encoding='utf-8')
    else:
        output_handle = sys.stdout

    try:
        # Auto-detect format based on extension
        if args.input:
            suffix = args.input.suffix.lower()
            if suffix == '.jsonl' or suffix == '.jsonl.gz':
                count = process_jsonl(args.input, output_handle, args.strict)
            elif suffix == '.json':
                count = process_json(args.input, output_handle, args.strict)
            else:
                # Try JSONL by default for unknown extensions
                count = process_jsonl(args.input, output_handle, args.strict)
        else:
            # stdin — try to detect or default to JSONL
            count = process_jsonl(Path('/dev/stdin'), output_handle, args.strict)

        if args.output:
            print(f"Sanitized {count} record(s) → {args.output}", file=sys.stderr)
    finally:
        if input_handle != sys.stdin:
            input_handle.close()
        if output_handle != sys.stdout:
            output_handle.close()


if __name__ == '__main__':
    main()
