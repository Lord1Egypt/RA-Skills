"""Tests for Claude client."""

import pytest
from unittest.mock import patch, MagicMock

from code_review.claude_client import ClaudeConfig
from anthropic import Anthropic


class TestClaudeConfig:
    """Test Claude configuration management."""

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict('os.environ', {}, clear=True):
            config = ClaudeConfig()
            assert config.api_key is None

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            config = ClaudeConfig()
            assert config.api_key == 'test_key'

    def test_is_configured_without_key(self):
        """Test is_configured returns False without key."""
        with patch.dict('os.environ', {}, clear=True):
            config = ClaudeConfig()
            assert config.is_configured() is False

    def test_is_configured_with_key(self):
        """Test is_configured returns True with key."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            config = ClaudeConfig()
            assert config.is_configured() is True

    def test_get_client_without_key(self):
        """Test get_client raises error without key."""
        with patch.dict('os.environ', {}, clear=True):
            config = ClaudeConfig()
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
                config.get_client()

    def test_get_client_with_key(self):
        """Test get_client returns Anthropic client with key."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            config = ClaudeConfig()
            client = config.get_client()
            assert isinstance(client, Anthropic)

    @patch('code_review.claude_client.load_dotenv')
    def test_load_env_file(self, mock_load_dotenv):
        """Test that .env file is loaded."""
        mock_load_dotenv.return_value = None
        with patch.dict('os.environ', {}, clear=True):
            ClaudeConfig()
            mock_load_dotenv.assert_called_once()
