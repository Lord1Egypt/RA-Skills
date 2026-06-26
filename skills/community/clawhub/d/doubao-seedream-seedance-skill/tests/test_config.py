"""
Tests for configuration management.

Tests verify configuration loading and priority.
"""

import pytest
import os
from pathlib import Path
from toolkit.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_default_config(self):
        """Test that default configuration is loaded."""
        config = ConfigManager()
        assert config.get("timeout") == 30
        assert config.get("max_retries") == 3
        assert config.get("base_url") == "https://ark.cn-beijing.volces.com/api/v3"
    
    def test_get_nonexistent_key(self):
        """Test getting nonexistent configuration key."""
        config = ConfigManager()
        assert config.get("nonexistent") is None
        assert config.get("nonexistent", "default") == "default"
    
    def test_set_and_get(self):
        """Test setting and getting configuration values."""
        config = ConfigManager()
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"
    
    def test_get_api_key(self):
        """Test getting API key."""
        config = ConfigManager()
        # Should be None by default
        assert config.get_api_key() is None
        
        # Set and get
        config.set("api_key", "test-api-key")
        assert config.get_api_key() == "test-api-key"
    
    def test_get_base_url(self):
        """Test getting base URL."""
        config = ConfigManager()
        assert "volces.com" in config.get_base_url()
    
    def test_get_timeout(self):
        """Test getting timeout."""
        config = ConfigManager()
        assert config.get_timeout() == 30
    
    def test_get_output_dir(self, tmp_path):
        """Test getting output directory."""
        config = ConfigManager(project_root=tmp_path)
        output_dir = config.get_output_dir()
        assert output_dir.exists()
        assert output_dir.is_dir()
    
    def test_to_dict(self):
        """Test getting configuration as dictionary."""
        config = ConfigManager()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "timeout" in config_dict
        assert "base_url" in config_dict
    
    def test_env_variable_override(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("ARK_API_KEY", "env-api-key")
        monkeypatch.setenv("VOLCENGINE_TIMEOUT", "60")
        
        config = ConfigManager()
        assert config.get_api_key() == "env-api-key"
        assert config.get_timeout() == 60
    
    def test_project_config_loading(self, tmp_path):
        """Test loading project configuration file."""
        # Create project config
        config_dir = tmp_path / ".volcengine"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("timeout: 45\nmax_retries: 5\n")
        
        config = ConfigManager(project_root=tmp_path)
        assert config.get_timeout() == 45
        assert config.get("max_retries") == 5
    
    def test_env_overrides_project_config(self, tmp_path, monkeypatch):
        """Test that environment variables override project config."""
        # Create project config
        config_dir = tmp_path / ".volcengine"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("timeout: 45\n")
        
        # Set env variable
        monkeypatch.setenv("VOLCENGINE_TIMEOUT", "90")
        
        config = ConfigManager(project_root=tmp_path)
        assert config.get_timeout() == 90
    
    def test_save_project_config(self, tmp_path):
        """Test saving configuration to project file."""
        config = ConfigManager(project_root=tmp_path)
        config.set("custom_setting", "test_value")
        config.save_project_config()
        
        # Verify file was created
        config_file = tmp_path / ".volcengine" / "config.yaml"
        assert config_file.exists()
        
        # Load and verify
        new_config = ConfigManager(project_root=tmp_path)
        assert new_config.get("custom_setting") == "test_value"
    
    def test_missing_config_file(self, tmp_path):
        """Test behavior when config file doesn't exist."""
        config = ConfigManager(project_root=tmp_path)
        # Should still have defaults
        assert config.get_timeout() == 30
        assert config.get("max_retries") == 3
    
    def test_invalid_yaml_config(self, tmp_path):
        """Test handling of invalid YAML config file."""
        config_dir = tmp_path / ".volcengine"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        # Should not crash, use defaults
        config = ConfigManager(project_root=tmp_path)
        assert config.get_timeout() == 30
