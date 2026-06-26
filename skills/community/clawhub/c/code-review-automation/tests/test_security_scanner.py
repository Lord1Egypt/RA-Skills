"""Tests for security scanner."""

import pytest

from code_review.security_scanner import SecurityScanner, SecurityIssue


class TestSecurityScanner:
    """Test security scanner functionality."""

    def test_scan_for_api_keys(self):
        """Test detection of API keys."""
        scanner = SecurityScanner()
        diff = '''+api_key = "sk-1234567890abcdefghijklmnopqrstuv"
+token = "ghp_1234567890abcdefghijklmnopqrstuv"'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        api_key_issues = [i for i in issues if i.category == 'Exposed Secrets']
        assert len(api_key_issues) > 0

    def test_scan_for_passwords(self):
        """Test detection of hardcoded passwords."""
        scanner = SecurityScanner()
        diff = '''+password = "mypassword123"
+db_password = "secretpassword"'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        # Check for password issues (either in category, description, or code snippet)
        password_issues = [i for i in issues if 'password' in i.category.lower() or 'password' in i.description.lower() or 'password' in i.code_snippet.lower()]
        assert len(password_issues) > 0

    def test_scan_for_sql_injection(self):
        """Test detection of SQL injection vulnerabilities."""
        scanner = SecurityScanner()
        diff = '''+cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
+query = "SELECT * FROM users WHERE name = " + user_name'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        sql_issues = [i for i in issues if i.category == 'SQL Injection']
        assert len(sql_issues) > 0

    def test_scan_for_command_injection(self):
        """Test detection of command injection vulnerabilities."""
        scanner = SecurityScanner()
        diff = '''+os.system(user_input)
+subprocess.call(user_input, shell=True)'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        cmd_issues = [i for i in issues if i.category == 'Command Injection']
        assert len(cmd_issues) > 0

    def test_scan_for_weak_crypto(self):
        """Test detection of weak cryptography."""
        scanner = SecurityScanner()
        diff = '''+hash_value = MD5(data)
+signature = SHA1(data)
+cipher = Crypto.Cipher.ARC4.new(key)'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        crypto_issues = [i for i in issues if i.category == 'Weak Cryptography']
        assert len(crypto_issues) > 0

    def test_scan_for_unsafe_deserialization(self):
        """Test detection of unsafe deserialization."""
        scanner = SecurityScanner()
        diff = '''+data = pickle.loads(serialized_data)
+obj = pickle.load(file)'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) > 0
        pickle_issues = [i for i in issues if i.category == 'Unsafe Deserialization']
        assert len(pickle_issues) > 0

    def test_scan_clean_code(self):
        """Test that clean code has no issues."""
        scanner = SecurityScanner()
        diff = '''+def clean_function():
+    """This is a clean function."""
+    return "safe"'''

        issues = scanner.scan_diff(diff, "test/repo")

        assert len(issues) == 0

    def test_get_summary(self):
        """Test summary generation."""
        scanner = SecurityScanner()
        diff = '''+api_key = "sk-1234567890abcdefghijklmnopqrstuv"
+password = "mypassword123"'''

        scanner.scan_diff(diff, "test/repo")
        summary = scanner.get_summary()

        assert 'total' in summary
        assert 'critical' in summary
        assert 'high' in summary
        assert 'medium' in summary
        assert 'low' in summary
        assert 'by_category' in summary
        assert summary['total'] > 0


class TestSecurityIssue:
    """Test security issue dataclass."""

    def test_security_issue_creation(self):
        """Test creating a security issue."""
        issue = SecurityIssue(
            severity='critical',
            category='Exposed Secrets',
            description='API key exposed',
            line_number=10,
            filename='test.py',
            code_snippet='api_key = "sk-123"',
            recommendation='Use environment variables'
        )

        assert issue.severity == 'critical'
        assert issue.category == 'Exposed Secrets'
        assert issue.line_number == 10
        assert issue.filename == 'test.py'
        assert issue.code_snippet == 'api_key = "sk-123"'
        assert issue.recommendation == 'Use environment variables'
