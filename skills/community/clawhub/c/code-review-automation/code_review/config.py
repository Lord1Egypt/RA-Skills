"""Configuration management for code review."""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

from .logger import setup_logger
from .exceptions import ConfigurationError, ValidationError

logger = setup_logger(__name__)


@dataclass
class SecurityConfig:
    """Security scanning configuration."""

    enabled: bool = True
    severity_threshold: str = 'medium'  # low, medium, high, critical
    check_secrets: bool = True
    check_sql_injection: bool = True
    check_command_injection: bool = True
    check_hardcoded_credentials: bool = True
    check_weak_crypto: bool = True
    check_unsafe_deserialization: bool = True


@dataclass
class StyleConfig:
    """Style checking configuration."""

    enabled: bool = True
    severity_threshold: str = 'warning'  # info, warning, error
    check_line_length: bool = True
    max_line_length: int = 88
    check_naming: bool = True
    check_imports: bool = True
    check_blank_lines: bool = True
    check_whitespace: bool = True
    check_docstrings: bool = True


@dataclass
class LLMConfig:
    """LLM analysis configuration."""

    enabled: bool = True
    model: str = 'claude-3-7-sonnet-20250219'
    max_tokens: int = 4096
    temperature: float = 0.7
    quality_threshold: int = 70  # Score below this requires review


@dataclass
class ReviewConfig:
    """Main code review configuration."""

    security: SecurityConfig = field(default_factory=SecurityConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)

    # General settings
    max_diff_size: int = 100000  # Max diff characters to analyze
    timeout: int = 60  # Request timeout in seconds

    # Output settings
    output_format: str = 'markdown'  # markdown, json, text
    show_code_snippets: bool = True
    show_recommendations: bool = True


class ConfigManager:
    """Manage code review configuration from files."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file (.reviewrc, .reviewrc.json, .reviewrc.yaml)
        """
        self.config_path = self._find_config_file(config_path)
        self.config = ReviewConfig()

        if self.config_path and self.config_path.exists():
            self.load_config(self.config_path)

    def _find_config_file(self, config_path: Optional[str] = None) -> Optional[Path]:
        """Find configuration file in current or parent directories.

        Args:
            config_path: Explicit config file path

        Returns:
            Path to config file or None
        """
        if config_path:
            return Path(config_path)

        # Search in current directory and parent directories
        current_dir = Path.cwd()
        config_filenames = [
            '.reviewrc',
            '.reviewrc.json',
            '.reviewrc.yaml',
            '.reviewrc.yml',
            'reviewrc.json',
            'reviewrc.yaml',
        ]

        for _ in range(10):  # Search up to 10 parent directories
            for filename in config_filenames:
                config_file = current_dir / filename
                if config_file.exists():
                    return config_file

            parent = current_dir.parent
            if parent == current_dir:  # Reached root
                break
            current_dir = parent

        return None

    def load_config(self, config_path: Path):
        """Load configuration from file.

        Args:
            config_path: Path to configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            ConfigurationError: If config file cannot be loaded
        """
        if not config_path.exists():
            logger.error(f"Config file not found: {config_path}")
            raise FileNotFoundError(f"Config file not found: {config_path}")

        logger.debug(f"Loading config from: {config_path}")

        try:
            # Determine file type and load
            if config_path.suffix in ['.yaml', '.yml']:
                self._load_yaml_config(config_path)
            elif config_path.suffix == '.json':
                self._load_json_config(config_path)
            elif config_path.suffix == '' or config_path.name == '.reviewrc':
                # Try YAML first, then JSON
                try:
                    self._load_yaml_config(config_path)
                except Exception:
                    self._load_json_config(config_path)
            else:
                raise ValueError(f"Unsupported config file format: {config_path.suffix}")

            logger.info(f"Configuration loaded successfully from {config_path}")

        except Exception as e:
            logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise ConfigurationError(
                f"Failed to load configuration: {e}",
                suggestion="Check that the configuration file is valid JSON or YAML"
            )

    def _load_yaml_config(self, config_path: Path):
        """Load YAML configuration file.

        Args:
            config_path: Path to YAML config file

        Raises:
            ConfigurationError: If YAML cannot be parsed
        """
        try:
            import yaml
        except ImportError as e:
            logger.error("PyYAML not installed")
            raise ImportError(
                "PyYAML is required for YAML config files. "
                "Install with: pip install pyyaml"
            )

        try:
            logger.debug(f"Parsing YAML config: {config_path}")
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)

            if config_data:
                logger.debug(f"Loaded {len(config_data)} config sections from YAML")
                self._merge_config(config_data)

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML config: {e}")
            raise ConfigurationError(
                f"Failed to parse YAML configuration: {e}",
                suggestion="Check that the YAML syntax is correct"
            )

        except Exception as e:
            logger.error(f"Error loading YAML config: {e}")
            raise ConfigurationError(f"Error loading YAML config: {e}")

    def _load_json_config(self, config_path: Path):
        """Load JSON configuration file.

        Args:
            config_path: Path to JSON config file

        Raises:
            ConfigurationError: If JSON cannot be parsed
        """
        try:
            logger.debug(f"Parsing JSON config: {config_path}")
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            if config_data:
                logger.debug(f"Loaded {len(config_data)} config sections from JSON")
                self._merge_config(config_data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON config: {e}")
            raise ConfigurationError(
                f"Failed to parse JSON configuration: {e}",
                suggestion="Check that the JSON syntax is correct"
            )

        except Exception as e:
            logger.error(f"Error loading JSON config: {e}")
            raise ConfigurationError(f"Error loading JSON config: {e}")

    def _merge_config(self, config_data: Dict[str, Any]):
        """Merge configuration data into config object.

        Args:
            config_data: Configuration data dictionary
        """
        # Security config
        if 'security' in config_data:
            security_data = config_data['security']
            for key, value in security_data.items():
                if hasattr(self.config.security, key):
                    setattr(self.config.security, key, value)

        # Style config
        if 'style' in config_data:
            style_data = config_data['style']
            for key, value in style_data.items():
                if hasattr(self.config.style, key):
                    setattr(self.config.style, key, value)

        # LLM config
        if 'llm' in config_data:
            llm_data = config_data['llm']
            for key, value in llm_data.items():
                if hasattr(self.config.llm, key):
                    setattr(self.config.llm, key, value)

        # Main config
        for key, value in config_data.items():
            if key not in ['security', 'style', 'llm'] and hasattr(self.config, key):
                setattr(self.config, key, value)

    def save_config(self, config_path: Optional[Path] = None):
        """Save configuration to file.

        Args:
            config_path: Path to save config file (default: self.config_path)
        """
        save_path = config_path or self.config_path

        if not save_path:
            save_path = Path.cwd() / '.reviewrc'

        # Convert config to dict
        config_dict = {
            'security': {
                'enabled': self.config.security.enabled,
                'severity_threshold': self.config.security.severity_threshold,
                'check_secrets': self.config.security.check_secrets,
                'check_sql_injection': self.config.security.check_sql_injection,
                'check_command_injection': self.config.security.check_command_injection,
                'check_hardcoded_credentials': self.config.security.check_hardcoded_credentials,
                'check_weak_crypto': self.config.security.check_weak_crypto,
                'check_unsafe_deserialization': self.config.security.check_unsafe_deserialization,
            },
            'style': {
                'enabled': self.config.style.enabled,
                'severity_threshold': self.config.style.severity_threshold,
                'check_line_length': self.config.style.check_line_length,
                'max_line_length': self.config.style.max_line_length,
                'check_naming': self.config.style.check_naming,
                'check_imports': self.config.style.check_imports,
                'check_blank_lines': self.config.style.check_blank_lines,
                'check_whitespace': self.config.style.check_whitespace,
                'check_docstrings': self.config.style.check_docstrings,
            },
            'llm': {
                'enabled': self.config.llm.enabled,
                'model': self.config.llm.model,
                'max_tokens': self.config.llm.max_tokens,
                'temperature': self.config.llm.temperature,
                'quality_threshold': self.config.llm.quality_threshold,
            },
            'max_diff_size': self.config.max_diff_size,
            'timeout': self.config.timeout,
            'output_format': self.config.output_format,
            'show_code_snippets': self.config.show_code_snippets,
            'show_recommendations': self.config.show_recommendations,
        }

        # Determine format and save
        if save_path.suffix in ['.yaml', '.yml']:
            try:
                import yaml
            except ImportError:
                raise ImportError(
                    "PyYAML is required for YAML config files. "
                    "Install with: pip install pyyaml"
                )

            with open(save_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
        else:
            # Default to JSON
            with open(save_path, 'w') as f:
                json.dump(config_dict, f, indent=2)

    def create_default_config(self, config_path: Optional[Path] = None):
        """Create default configuration file.

        Args:
            config_path: Path to save config file (default: .reviewrc)
        """
        self.config = ReviewConfig()
        self.save_config(config_path)
        return config_path or Path.cwd() / '.reviewrc'

    def get_security_config(self) -> SecurityConfig:
        """Get security scanning configuration.

        Returns:
            SecurityConfig object
        """
        return self.config.security

    def get_style_config(self) -> StyleConfig:
        """Get style checking configuration.

        Returns:
            StyleConfig object
        """
        return self.config.style

    def get_llm_config(self) -> LLMConfig:
        """Get LLM analysis configuration.

        Returns:
            LLMConfig object
        """
        return self.config.llm

    def get_config(self) -> ReviewConfig:
        """Get full configuration.

        Returns:
            ReviewConfig object
        """
        return self.config
