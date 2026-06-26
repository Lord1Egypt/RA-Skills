"""Tests for PR analyzer."""

import pytest
from unittest.mock import MagicMock, patch

from code_review.pr_analyzer import PRAnalyzer


class TestPRAnalyzer:
    """Test PR analyzer functionality."""

    @pytest.fixture
    def mock_claude_client(self):
        """Create a mock Claude client."""
        client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test analysis")]
        client.messages.create.return_value = mock_response
        return client

    @pytest.fixture
    def mock_pr(self):
        """Create a mock PR."""
        mock_pr = MagicMock()
        mock_pr.number = 123
        mock_pr.title = "Test PR"
        mock_pr.body = "Test description"
        mock_pr.user.login = "testuser"
        mock_pr.state = "open"

        # Mock files
        mock_file1 = MagicMock()
        mock_file1.filename = "file1.py"
        mock_file1.status = "modified"
        mock_file1.additions = 10
        mock_file1.deletions = 5

        mock_file2 = MagicMock()
        mock_file2.filename = "file2.py"
        mock_file2.status = "added"
        mock_file2.additions = 20
        mock_file2.deletions = 0

        mock_pr.get_files.return_value = [mock_file1, mock_file2]

        return mock_pr

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_init(self, mock_claude_config):
        """Test PRAnalyzer initialization."""
        analyzer = PRAnalyzer()
        assert analyzer.model == "claude-3-7-sonnet-20250219"

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_analyze_pr(self, mock_claude_config_class, mock_claude_client, mock_pr):
        """Test PR analysis."""
        mock_claude_config = MagicMock()
        mock_claude_config.get_client.return_value = mock_claude_client
        mock_claude_config_class.return_value = mock_claude_config

        analyzer = PRAnalyzer()
        diff_content = "+print('hello')\n-print('world')"

        analysis = analyzer.analyze_pr(mock_pr, diff_content)

        assert "analysis" in analysis
        assert "pr_number" in analysis
        assert analysis["pr_number"] == 123
        assert "model" in analysis

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_build_pr_context(self, mock_claude_config, mock_pr):
        """Test PR context building."""
        analyzer = PRAnalyzer()
        diff_content = "+print('hello')"

        context = analyzer._build_pr_context(mock_pr, diff_content)

        assert "Test PR" in context
        assert "Test description" in context
        assert "testuser" in context
        assert "file1.py" in context
        assert "file2.py" in context

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_create_analysis_prompt(self, mock_claude_config):
        """Test analysis prompt creation."""
        analyzer = PRAnalyzer()
        context = "Test context"

        prompt = analyzer._create_analysis_prompt(context)

        assert "code review" in prompt.lower()
        assert "Overall Assessment" in prompt
        assert "Code Quality Issues" in prompt
        assert "Security Considerations" in prompt
        assert "Best Practices" in prompt
        assert "Recommendations" in prompt

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_high(self, mock_claude_config):
        """Test code quality scoring for high quality."""
        analyzer = PRAnalyzer()
        analysis = "This is great code. No issues found."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 100

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_with_critical(self, mock_claude_config):
        """Test code quality scoring with critical issues."""
        analyzer = PRAnalyzer()
        analysis = "CRITICAL: Security vulnerability. CRITICAL: Another issue."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 50  # 100 - 25*2

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_with_high(self, mock_claude_config):
        """Test code quality scoring with high priority issues."""
        analyzer = PRAnalyzer()
        analysis = "High priority issue 1. High priority issue 2. High priority issue 3."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 70  # 100 - 10*3

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_with_medium(self, mock_claude_config):
        """Test code quality scoring with medium priority issues."""
        analyzer = PRAnalyzer()
        analysis = "Medium priority issue 1. Medium priority issue 2."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 90  # 100 - 5*2

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_mixed(self, mock_claude_config):
        """Test code quality scoring with mixed priorities."""
        analyzer = PRAnalyzer()
        analysis = "CRITICAL issue. High priority issue 1. High priority issue 2. Medium priority issue 1."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 50  # 100 - 25 - 10 - 10 - 5

    @patch('code_review.pr_analyzer.ClaudeConfig')
    def test_get_code_quality_score_clamp(self, mock_claude_config):
        """Test code quality scoring clamps to 0 minimum."""
        analyzer = PRAnalyzer()
        analysis = "CRITICAL. CRITICAL. CRITICAL. CRITICAL. CRITICAL."

        score = analyzer.get_code_quality_score(analysis)

        assert score == 0  # 100 - 25*5 = -25, clamped to 0
