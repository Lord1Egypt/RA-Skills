"""Security vulnerability scanner for code review."""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .logger import setup_logger, log_security_issue

logger = setup_logger(__name__)


@dataclass
class SecurityIssue:
    """Security issue found in code."""

    severity: str  # critical, high, medium, low
    category: str  # SQL Injection, XSS, Hardcoded secrets, etc.
    description: str
    line_number: int
    filename: str
    code_snippet: str
    recommendation: str


class SecurityScanner:
    """Security vulnerability scanner using static analysis."""

    def __init__(self):
        self.issues: List[SecurityIssue] = []
        logger.debug("Security scanner initialized")

    def scan_diff(self, diff_content: str, repo_name: str) -> List[SecurityIssue]:
        """Scan diff content for security vulnerabilities.

        Args:
            diff_content: Diff content from PR
            repo_name: Repository name for context

        Returns:
            List of security issues found
        """
        logger.debug(f"Scanning diff for security issues in {repo_name} ({len(diff_content)} chars)")
        self.issues = []

        try:
            self._scan_for_secrets(diff_content)
            self._scan_for_sql_injection(diff_content)
            self._scan_for_command_injection(diff_content)
            self._scan_for_hardcoded_credentials(diff_content)
            self._scan_for_weak_crypto(diff_content)
            self._scan_for_unsafe_deserialization(diff_content)

            # Log each security issue
            for issue in self.issues:
                log_security_issue(logger, issue.severity, issue.category, issue.filename, issue.line_number)

            logger.info(f"Security scan complete: {len(self.issues)} issues found")
            return self.issues

        except Exception as e:
            logger.error(f"Error during security scan: {e}")
            # Return any issues found before the error
            return self.issues

    def _scan_for_secrets(self, diff_content: str):
        """Scan for exposed secrets and API keys."""
        secret_patterns = {
            'api_key': [
                r'api[_-]?key\s*=\s*["\'][\w\-]{20,}["\']',
                r'apikey\s*=\s*["\'][\w\-]{20,}["\']',
            ],
            'aws_access_key': [
                r'aws[_-]access[_-]?key[_-]?id\s*=\s*["\'][A-Z0-9]{20}["\']',
                r'aws[_-]secret[_-]?access[_-]?key\s*=\s*["\'][\w/+]{40}["\']',
            ],
            'private_key': [
                r'-----BEGIN (RSA )?PRIVATE KEY-----',
                r'private[_-]?key\s*=\s*["\']-----BEGIN',
            ],
            'password': [
                r'password\s*=\s*["\'][\w\-]+["\']',
                r'passwd\s*=\s*["\'][\w\-]+["\']',
            ],
            'token': [
                r'github[_-]?token\s*=\s*["\'][\w\-]{20,}["\']',
                r'token\s*=\s*["\'][\w\-]{20,}["\']',
            ],
        }

        for category, patterns in secret_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, diff_content, re.IGNORECASE):
                    line_number = self._extract_line_number(diff_content, match.start())
                    self.issues.append(SecurityIssue(
                        severity='critical',
                        category='Exposed Secrets',
                        description=f'Potential {category.replace("_", " ")} exposed in code',
                        line_number=line_number,
                        filename='unknown',
                        code_snippet=match.group(0),
                        recommendation=f'Remove hardcoded {category}. Use environment variables or secrets manager.'
                    ))

    def _scan_for_sql_injection(self, diff_content: str):
        """Scan for potential SQL injection vulnerabilities."""
        # Pattern: f"SELECT * FROM table WHERE id = {user_input}"
        sql_injection_patterns = [
            r'(execute|query|cursor\.execute|conn\.execute)\s*\(\s*f?["\'][^"\']*{[^}]+}[^"\']*["\']',
            r'(execute|query)\s*\(\s*["\'][^"\']*\+\s*\w+[^"\']*["\']',
        ]

        for pattern in sql_injection_patterns:
            for match in re.finditer(pattern, diff_content):
                line_number = self._extract_line_number(diff_content, match.start())
                self.issues.append(SecurityIssue(
                    severity='high',
                    category='SQL Injection',
                    description='Potential SQL injection vulnerability detected',
                    line_number=line_number,
                    filename='unknown',
                    code_snippet=match.group(0)[:100],
                    recommendation='Use parameterized queries or an ORM with built-in SQL injection protection.'
                ))

    def _scan_for_command_injection(self, diff_content: str):
        """Scan for command injection vulnerabilities."""
        # Pattern: os.system(user_input), subprocess.call(user_input)
        command_injection_patterns = [
            r'\b(os\.system|subprocess\.(call|run|Popen))\s*\(\s*\w+\s*\)',
            r'\b(os\.system|subprocess\.(call|run|Popen))\s*\(\s*f?["\'][^"\']*{[^}]+}[^"\']*["\']',
        ]

        for pattern in command_injection_patterns:
            for match in re.finditer(pattern, diff_content):
                line_number = self._extract_line_number(diff_content, match.start())
                self.issues.append(SecurityIssue(
                    severity='high',
                    category='Command Injection',
                    description='Potential command injection vulnerability detected',
                    line_number=line_number,
                    filename='unknown',
                    code_snippet=match.group(0),
                    recommendation='Use subprocess with proper argument validation and avoid shell=True.'
                ))

    def _scan_for_hardcoded_credentials(self, diff_content: str):
        """Scan for hardcoded credentials."""
        credential_patterns = [
            r'database[_-]?url\s*=\s*["\'][^"\']*:[^"\']*@',
            r'db[_-]?host\s*=\s*["\'][\w\.]+["\']',
            r'db[_-]?user\s*=\s*["\'][\w]+["\']',
            r'db[_-]?pass\s*=\s*["\'][\w]+["\']',
        ]

        for pattern in credential_patterns:
            for match in re.finditer(pattern, diff_content, re.IGNORECASE):
                line_number = self._extract_line_number(diff_content, match.start())
                self.issues.append(SecurityIssue(
                    severity='critical',
                    category='Hardcoded Credentials',
                    description='Hardcoded database or service credentials detected',
                    line_number=line_number,
                    filename='unknown',
                    code_snippet=match.group(0),
                    recommendation='Move credentials to environment variables or a secrets manager.'
                ))

    def _scan_for_weak_crypto(self, diff_content: str):
        """Scan for weak cryptographic implementations."""
        weak_crypto_patterns = [
            (r'MD5\(\)', 'MD5 is cryptographically broken and should not be used for security purposes'),
            (r'SHA1\(\)', 'SHA1 is deprecated and vulnerable to collision attacks'),
            (r'hash\.md5\(', 'MD5 is cryptographically broken and should not be used for security purposes'),
            (r'hash\.sha1\(', 'SHA1 is deprecated and vulnerable to collision attacks'),
            (r'Crypto\.Cipher\.ARC4', 'RC4 is a weak stream cipher and should not be used'),
            (r'Crypto\.Cipher\.DES', 'DES is a weak block cipher and should not be used'),
        ]

        for pattern, description in weak_crypto_patterns:
            for match in re.finditer(pattern, diff_content):
                line_number = self._extract_line_number(diff_content, match.start())
                self.issues.append(SecurityIssue(
                    severity='medium',
                    category='Weak Cryptography',
                    description=description,
                    line_number=line_number,
                    filename='unknown',
                    code_snippet=match.group(0),
                    recommendation='Use stronger cryptographic primitives (e.g., SHA-256, AES-256, bcrypt)'
                ))

    def _scan_for_unsafe_deserialization(self, diff_content: str):
        """Scan for unsafe deserialization patterns."""
        unsafe_deserialize_patterns = [
            r'pickle\.loads\s*\(',
            r'pickle\.load\s*\(',
            r'cPickle\.loads\s*\(',
            r'cPickle\.load\s*\(',
        ]

        for pattern in unsafe_deserialize_patterns:
            for match in re.finditer(pattern, diff_content):
                line_number = self._extract_line_number(diff_content, match.start())
                self.issues.append(SecurityIssue(
                    severity='high',
                    category='Unsafe Deserialization',
                    description='Unsafe pickle deserialization can lead to arbitrary code execution',
                    line_number=line_number,
                    filename='unknown',
                    code_snippet=match.group(0),
                    recommendation='Use safe serialization formats like JSON with schema validation'
                ))

    def _extract_line_number(self, diff_content: str, position: int) -> int:
        """Extract line number from position in diff content."""
        lines_before = diff_content[:position].count('\n')
        return lines_before + 1

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of security issues found.

        Returns:
            Dictionary with severity breakdown
        """
        summary = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'total': len(self.issues),
            'by_category': {}
        }

        for issue in self.issues:
            summary[issue.severity] += 1

            category = issue.category
            if category not in summary['by_category']:
                summary['by_category'][category] = 0
            summary['by_category'][category] += 1

        return summary
