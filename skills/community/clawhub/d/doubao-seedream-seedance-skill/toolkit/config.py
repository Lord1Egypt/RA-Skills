"""
Configuration management for Volcengine API Skill.

Supports multi-level configuration: Environment > Project > Global > Defaults

Security Notes:
- API keys are sensitive data. Prefer environment variables over config files.
- If storing API keys in config files, ensure proper file permissions (600).
- Config files with API keys should never be committed to version control.
"""

import os
import stat
import warnings
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


# Sensitive keys that should be masked in logs/displays
SENSITIVE_KEYS = {"api_key", "ARK_API_KEY", "password", "secret", "token"}

# Secure file permissions for config files (read/write for owner only)
SECURE_FILE_MODE = 0o600
SECURE_DIR_MODE = 0o700


def mask_sensitive_value(key: str, value: Any) -> str:
    """
    Mask sensitive values for safe display.
    
    Args:
        key: Configuration key name
        value: Configuration value
        
    Returns:
        Masked string representation
    """
    if value is None:
        return "None"
    
    str_value = str(value)
    
    # Check if key contains sensitive keywords
    key_lower = key.lower()
    is_sensitive = any(
        sensitive in key_lower 
        for sensitive in ["api_key", "password", "secret", "token", "key"]
    )
    
    if is_sensitive and str_value:
        # Show first 4 and last 4 characters, mask the rest
        if len(str_value) <= 8:
            return "*" * len(str_value)
        return f"{str_value[:4]}{'*' * (len(str_value) - 8)}{str_value[-4:]}"
    
    return str_value


def check_file_permissions(file_path: Path) -> Dict[str, Any]:
    """
    Check if file permissions are secure for sensitive data.
    
    Args:
        file_path: Path to the config file
        
    Returns:
        Dict with 'secure' (bool), 'mode' (int), 'warning' (str or None)
    """
    if not file_path.exists():
        return {"secure": True, "mode": None, "warning": None}
    
    try:
        file_stat = file_path.stat()
        mode = stat.S_IMODE(file_stat.st_mode)
        
        # Check if file is readable by others
        others_readable = bool(mode & stat.S_IROTH)
        others_writable = bool(mode & stat.S_IWOTH)
        group_readable = bool(mode & stat.S_IRGRP)
        
        is_secure = not (others_readable or others_writable or group_readable)
        
        warning = None
        if not is_secure:
            warning = (
                f"Config file {file_path} has insecure permissions (mode: {oct(mode)}). "
                f"Recommend running: chmod 600 {file_path}"
            )
        
        return {
            "secure": is_secure,
            "mode": mode,
            "warning": warning
        }
    except Exception as e:
        return {
            "secure": False,
            "mode": None,
            "warning": f"Could not check permissions for {file_path}: {e}"
        }


class ConfigManager:
    """
    Manages configuration with priority-based loading.
    
    Priority order (highest to lowest):
    1. Environment variables
    2. Project configuration (.volcengine/config.yaml)
    3. Global configuration (~/.volcengine/config.yaml)
    4. Default values
    
    Security Features:
    - Validates file permissions on config files
    - Masks sensitive values in string representations
    - Sets secure permissions when saving config files
    - Warns about insecure configurations
    """
    
    DEFAULT_CONFIG = {
        "api_key": None,
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "timeout": 30,
        "max_retries": 3,
        "output_dir": "./output",
        "default_image_width": 1024,
        "default_image_height": 1024,
        "default_video_duration": 5.0,
    }
    
    def __init__(
        self,
        project_root: Optional[Path] = None,
        config_dir: Optional[str] = ".volcengine",
        strict_security: bool = False
    ):
        """
        Initialize ConfigManager.
        
        Args:
            project_root: Project root directory (defaults to cwd)
            config_dir: Config directory name (defaults to .volcengine)
            strict_security: If True, raise errors on security issues
        """
        self.project_root = project_root or Path.cwd()
        self.config_dir = config_dir
        self.strict_security = strict_security
        self._config: Dict[str, Any] = {}
        self._security_warnings: list = []
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from all sources in priority order."""
        # Start with defaults
        self._config = self.DEFAULT_CONFIG.copy()
        
        # Load global config
        global_config_path = Path.home() / ".volcengine" / "config.yaml"
        if global_config_path.exists():
            self._check_and_load_yaml_config(global_config_path, "global")
        
        # Load project config
        project_config_path = self.project_root / self.config_dir / "config.yaml"
        if project_config_path.exists():
            self._check_and_load_yaml_config(project_config_path, "project")
        
        # Load environment variables (highest priority)
        self._load_env_config()
        
        # Emit security warnings if any
        if self._security_warnings:
            for warning_msg in self._security_warnings:
                if self.strict_security:
                    raise SecurityError(warning_msg)
                else:
                    warnings.warn(warning_msg, UserWarning)
    
    def _check_and_load_yaml_config(self, config_path: Path, config_type: str) -> None:
        """
        Check security and load configuration from YAML file.
        
        Args:
            config_path: Path to config file
            config_type: Type of config ('global' or 'project')
        """
        # Check file permissions
        perm_check = check_file_permissions(config_path)
        
        if not perm_check["secure"] and perm_check["warning"]:
            self._security_warnings.append(perm_check["warning"])
        
        # Load the config
        self._load_yaml_config(config_path)
    
    def _load_yaml_config(self, config_path: Path) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self._config.update(yaml_config)
        except Exception:
            # Silently ignore config file errors
            pass
    
    def _load_env_config(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "ARK_API_KEY": "api_key",
            "VOLCENGINE_BASE_URL": "base_url",
            "VOLCENGINE_TIMEOUT": "timeout",
            "VOLCENGINE_MAX_RETRIES": "max_retries",
            "VOLCENGINE_OUTPUT_DIR": "output_dir",
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert to appropriate type
                if config_key == "timeout":
                    value = int(value)
                elif config_key == "max_retries":
                    value = int(value)
                self._config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value (in memory only).
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self._config[key] = value
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from configuration."""
        return self.get("api_key")
    
    def get_masked_api_key(self) -> str:
        """
        Get masked API key for safe display.
        
        Returns:
            Masked API key string
        """
        api_key = self.get_api_key()
        return mask_sensitive_value("api_key", api_key)
    
    def get_base_url(self) -> str:
        """Get API base URL."""
        return self.get("base_url")
    
    def get_timeout(self) -> int:
        """Get request timeout in seconds."""
        return self.get("timeout")
    
    def get_output_dir(self) -> Path:
        """Get output directory path."""
        output_dir = self.get("output_dir")
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def to_dict(self, mask_sensitive: bool = False) -> Dict[str, Any]:
        """
        Get all configuration as dictionary.
        
        Args:
            mask_sensitive: If True, mask sensitive values
            
        Returns:
            Configuration dictionary
        """
        if mask_sensitive:
            return {
                k: mask_sensitive_value(k, v) 
                for k, v in self._config.items()
            }
        return self._config.copy()
    
    def save_project_config(self, exclude_api_key: bool = True) -> None:
        """
        Save current configuration to project config file.
        
        Args:
            exclude_api_key: If True, exclude API key from saved config
                           (recommended for security)
        """
        config_path = self.project_root / self.config_dir / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare config to save
        config_to_save = self._config.copy()
        
        # Optionally exclude API key for security
        if exclude_api_key and "api_key" in config_to_save:
            del config_to_save["api_key"]
            # Add comment about API key
            config_to_save["# api_key"] = "Set via ARK_API_KEY environment variable for security"
        
        # Write config file
        with open(config_path, 'w') as f:
            yaml.dump(config_to_save, f, default_flow_style=False)
        
        # Set secure file permissions
        try:
            os.chmod(config_path, SECURE_FILE_MODE)
        except Exception:
            warnings.warn(
                f"Could not set secure permissions on {config_path}. "
                f"Please run: chmod 600 {config_path}",
                UserWarning
            )
    
    def save_global_config(self, exclude_api_key: bool = True) -> None:
        """
        Save current configuration to global config file.
        
        Args:
            exclude_api_key: If True, exclude API key from saved config
                           (recommended for security)
        """
        config_path = Path.home() / ".volcengine" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare config to save
        config_to_save = self._config.copy()
        
        # Optionally exclude API key for security
        if exclude_api_key and "api_key" in config_to_save:
            del config_to_save["api_key"]
            config_to_save["# api_key"] = "Set via ARK_API_KEY environment variable for security"
        
        # Write config file
        with open(config_path, 'w') as f:
            yaml.dump(config_to_save, f, default_flow_style=False)
        
        # Set secure permissions for both directory and file
        try:
            os.chmod(config_path.parent, SECURE_DIR_MODE)
            os.chmod(config_path, SECURE_FILE_MODE)
        except Exception:
            warnings.warn(
                f"Could not set secure permissions on {config_path}. "
                f"Please run: chmod 700 {config_path.parent} && chmod 600 {config_path}",
                UserWarning
            )
    
    def get_security_warnings(self) -> list:
        """
        Get list of security warnings from config loading.
        
        Returns:
            List of warning messages
        """
        return self._security_warnings.copy()
    
    def __repr__(self) -> str:
        """String representation with masked sensitive values."""
        masked_config = self.to_dict(mask_sensitive=True)
        return f"ConfigManager({masked_config})"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        lines = ["ConfigManager:"]
        for key, value in self._config.items():
            display_value = mask_sensitive_value(key, value)
            lines.append(f"  {key}: {display_value}")
        return "\n".join(lines)


class SecurityError(Exception):
    """Raised when a security issue is detected in strict mode."""
    pass
