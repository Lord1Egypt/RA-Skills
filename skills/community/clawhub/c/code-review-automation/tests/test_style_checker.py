"""Tests for style checker."""

import pytest

from code_review.style_checker import StyleChecker, StyleIssue


class TestStyleChecker:
    """Test style checker functionality."""

    def test_check_line_length_too_long(self):
        """Test detection of lines that are too long."""
        checker = StyleChecker()
        diff = '''+'+def very_long_function_name_that_exceeds_the_recommended_line_length_limit(): return "this_line_is_way_too_long_for_pep8_compliance_and_should_be_broken_up"'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        line_issues = [i for i in issues if i.category == 'Line Length']
        assert len(line_issues) > 0

    def test_check_naming_class_lowercase(self):
        """Test detection of lowercase class names."""
        checker = StyleChecker()
        diff = '''+'+class myclass:
+    pass'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        naming_issues = [i for i in issues if i.category == 'Naming Convention']
        assert len(naming_issues) > 0

    def test_check_naming_function_uppercase(self):
        """Test detection of uppercase function names."""
        checker = StyleChecker()
        diff = '''+'+def MyFunction():
+    pass'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        naming_issues = [i for i in issues if i.category == 'Naming Convention']
        assert len(naming_issues) > 0

    def test_check_trailing_whitespace(self):
        """Test detection of trailing whitespace."""
        checker = StyleChecker()
        diff = '''+def test():
+    pass    
+'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        whitespace_issues = [i for i in issues if i.category == 'Whitespace']
        assert len(whitespace_issues) > 0

    def test_check_clean_code(self):
        """Test that clean code has no issues."""
        checker = StyleChecker()
        diff = '''+def clean_function():
+    """This is a clean function."""
+    return "safe"'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) == 0

    def test_check_missing_docstring_function(self):
        """Test detection of missing function docstrings."""
        checker = StyleChecker()
        diff = '''+'+def function_without_docstring():
+    return "no docstring"'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        docstring_issues = [i for i in issues if i.category == 'Docstrings']
        assert len(docstring_issues) > 0

    def test_check_missing_docstring_class(self):
        """Test detection of missing class docstrings."""
        checker = StyleChecker()
        diff = '''+'+class ClassWithoutDocstring:
+    pass'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        docstring_issues = [i for i in issues if i.category == 'Docstrings']
        assert len(docstring_issues) > 0

    def test_get_summary(self):
        """Test summary generation."""
        checker = StyleChecker()
        diff = '''+'+def MyFunction():  # Naming issue
+    pass     # Trailing whitespace'''

        checker.check_diff(diff, "test/repo")
        summary = checker.get_summary()

        assert 'total' in summary
        assert 'error' in summary
        assert 'warning' in summary
        assert 'info' in summary
        assert 'by_category' in summary
        assert summary['total'] > 0

    def test_multiple_blank_lines(self):
        """Test detection of multiple blank lines."""
        checker = StyleChecker()
        diff = '''+'+


+def function():
+    pass'''

        issues = checker.check_diff(diff, "test/repo")

        assert len(issues) > 0
        blank_issues = [i for i in issues if i.category == 'Blank Lines']
        assert len(blank_issues) > 0


class TestStyleIssue:
    """Test style issue dataclass."""

    def test_style_issue_creation(self):
        """Test creating a style issue."""
        issue = StyleIssue(
            severity='error',
            category='Line Length',
            description='Line too long',
            line_number=10,
            filename='test.py',
            code_snippet='very_long_line_here',
            suggestion='Break line'
        )

        assert issue.severity == 'error'
        assert issue.category == 'Line Length'
        assert issue.line_number == 10
        assert issue.filename == 'test.py'
        assert issue.code_snippet == 'very_long_line_here'
        assert issue.suggestion == 'Break line'
