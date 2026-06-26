"""Tests for configuration management."""

import pytest
import json
import tempfile
import os
from pathlib import Path

from code_review.config import (
    ConfigManager,
    ReviewConfig,
    SecurityConfig,
    StyleConfig,
    LLMConfig
)


class TestConfigManager:
    """Test configuration manager functionality."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ReviewConfig()

        assert config.security.enabled is True
        assert config.security.severity_threshold == 'medium'
        assert config.security.check_secrets is True

        assert config.style.enabled is True
        assert config.style.severity_threshold == 'warning'
        assert config.style.max_line_length == 88

        assert config.llm.enabled is True
        assert config.llm.model == 'claude-3-7-sonnet-20250219'
        assert config.llm.max_tokens == 4096

    def test_create_default_config_json(self):
        """Test creating default JSON configuration file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = Path(f.name)

        try:
            config_mgr = ConfigManager()
            config_mgr.create_default_config(config_path)

            assert config_path.exists()

            with open(config_path, 'r') as f:
                config_data = json.load(f)

            assert 'security' in config_data
            assert 'style' in config_data
            assert 'llm' in config_data

        finally:
            if config_path.exists():
                config_path.unlink()

    def test_load_config_json(self):
        """Test loading JSON configuration file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = Path(f.name)
            json.dump({
                'security': {
                    'enabled': False,
                    'severity_threshold': 'high'
                }
            }, f)

        try:
            config_mgr = ConfigManager(str(config_path))
            assert config_mgr.config.security.enabled is False
            assert config_mgr.config.security.severity_threshold == 'high'

        finally:
            if config_path.exists():
                config_path.unlink()

    def test_get_security_config(self):
        """Test getting security configuration."""
        config_mgr = ConfigManager()
        security_config = config_mgr.get_security_config()

        assert isinstance(security_config, SecurityConfig)
        assert security_config.enabled is True

    def test_get_style_config(self):
        """Test getting style configuration."""
        config_mgr = ConfigManager()
        style_config = config_mgr.get_style_config()

        assert isinstance(style_config, StyleConfig)
        assert style_config.enabled is True

    def test_get_llm_config(self):
        """Test getting LLM configuration."""
        config_mgr = ConfigManager()
        llm_config = config_mgr.get_llm_config()

        assert isinstance(llm_config, LLMConfig)
        assert llm_config.enabled is True


class TestSecurityConfig:
    """Test security configuration."""

    def test_default_values(self):
        """Test default security configuration values."""
        config = SecurityConfig()

        assert config.enabled is True
        assert config.severity_threshold == 'medium'
        assert config.check_secrets is True
        assert config.check_sql_injection is True
        assert config.check_command_injection is True
        assert config.check_hardcoded_credentials is True
        assert config.check_weak_crypto is True
        assert config.check_unsafe_deserialization is True


class TestStyleConfig:
    """Test style configuration."""

    def test_default_values(self):
        """Test default style configuration values."""
        config = StyleConfig()

        assert config.enabled is True
        assert config.severity_threshold == 'warning'
        assert config.check_line_length is True
        assert config.max_line_length == 88
        assert config.check_naming is True
        assert config.check_imports is True
        assert config.check_blank_lines is True
        assert config.check_whitespace is True
        assert config.check_docstrings is True


class TestLLMConfig:
    """Test LLM configuration."""

    def test_default_values(self):
        """Test default LLM configuration values."""
        config = LLMConfig()

        assert config.enabled is True
        assert config.model == 'claude-3-7-sonnet-20250219'
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.quality_threshold == 70
