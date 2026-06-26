"""Tests for GitHub client."""

import pytest
from unittest.mock import patch, MagicMock

from code_review.github_client import GitHubConfig
from github import Github


class TestGitHubConfig:
    """Test GitHub configuration management."""

    def test_init_without_token(self):
        """Test initialization without GitHub token."""
        with patch.dict('os.environ', {}, clear=True):
            config = GitHubConfig()
            assert config.github_token is None

    def test_init_with_token(self):
        """Test initialization with GitHub token."""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
            config = GitHubConfig()
            assert config.github_token == 'test_token'

    def test_is_configured_without_token(self):
        """Test is_configured returns False without token."""
        with patch.dict('os.environ', {}, clear=True):
            config = GitHubConfig()
            assert config.is_configured() is False

    def test_is_configured_with_token(self):
        """Test is_configured returns True with token."""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
            config = GitHubConfig()
            assert config.is_configured() is True

    def test_get_client_without_token(self):
        """Test get_client raises error without token."""
        with patch.dict('os.environ', {}, clear=True):
            config = GitHubConfig()
            with pytest.raises(ValueError, match="GITHUB_TOKEN not found"):
                config.get_client()

    def test_get_client_with_token(self):
        """Test get_client returns Github client with token."""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test_token'}):
            config = GitHubConfig()
            client = config.get_client()
            assert isinstance(client, Github)

    @patch('code_review.github_client.load_dotenv')
    def test_load_env_file(self, mock_load_dotenv):
        """Test that .env file is loaded."""
        mock_load_dotenv.return_value = None
        with patch.dict('os.environ', {}, clear=True):
            GitHubConfig()
            mock_load_dotenv.assert_called_once()
