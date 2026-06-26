#!/usr/bin/env python3
"""
Validate OpenClaw gateway configuration.
Checks syntax, required fields, and value ranges without running a gateway.
"""

import sys
import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Valid providers and their requirements
VALID_PROVIDERS = {
    'openai': {'required': ['apiKey'], 'optional': ['baseUrl', 'model', 'timeout']},
    'anthropic': {'required': ['apiKey'], 'optional': ['baseUrl', 'model', 'timeout']},
    'google': {'required': ['apiKey'], 'optional': ['baseUrl', 'model', 'timeout']},
    'moonshot': {'required': ['apiKey'], 'optional': ['baseUrl', 'model', 'timeout']},
    'ollama': {'required': [], 'optional': ['baseUrl', 'model', 'timeout']},
    'azure': {'required': ['apiKey', 'baseUrl'], 'optional': ['model', 'timeout']},
}

# Known models per provider (subset for validation)
KNOWN_MODELS = {
    'openai': [
        'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo',
        'gpt-4o-latest', 'o1', 'o1-mini', 'o3-mini'
    ],
    'anthropic': [
        'claude-3-5-sonnet-latest', 'claude-3-5-sonnet-20241022',
        'claude-3-opus-latest', 'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307', 'claude-2.1', 'claude-2.0'
    ],
    'google': [
        'gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash',
        'gemini-1.5-flash-8b', 'gemini-1.5-pro', 'gemini-1.0-pro'
    ],
    'moonshot': [
        'kimi-k2.5', 'kimi-latest', 'kimi-k1.5', 'kimi-k1'
    ],
    'ollama': [],  # Any model name is valid for ollama
}


def find_config_file() -> Optional[Path]:
    """Find OpenClaw config file in common locations."""
    paths = [
        Path.home() / '.openclaw' / 'config.yaml',
        Path.home() / '.openclaw' / 'config.yml',
        Path('/etc/openclaw/config.yaml'),
        Path('/etc/openclaw/config.yml'),
    ]
    for path in paths:
        if path.exists():
            return path
    return None


def load_config(config_path: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str]]:
    """Load YAML config file. Returns (config, error_message)."""
    if config_path:
        path = Path(config_path)
    else:
        path = find_config_file()
    
    if not path:
        return None, "Config file not found. Looked in ~/.openclaw/config.yaml and /etc/openclaw/config.yaml"
    
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return config, None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML syntax: {e}"
    except Exception as e:
        return None, f"Error reading config: {e}"


def validate_provider_config(provider: str, settings: Dict) -> List[str]:
    """Validate configuration for a specific provider."""
    errors = []
    
    if provider not in VALID_PROVIDERS:
        valid_list = ', '.join(VALID_PROVIDERS.keys())
        errors.append(f"Unknown provider '{provider}'. Valid: {valid_list}")
        return errors
    
    reqs = VALID_PROVIDERS[provider]
    
    # Check required fields
    for field in reqs['required']:
        if field not in settings or not settings[field]:
            errors.append(f"Provider '{provider}' requires '{field}'")
    
    # Check model validity
    if 'model' in settings and settings['model']:
        model = settings['model']
        valid_models = KNOWN_MODELS.get(provider, [])
        if valid_models and model not in valid_models:
            # Allow unknown models with a warning pattern
            if not re.match(r'^[a-zA-Z0-9._-]+$', model):
                errors.append(f"Model name '{model}' contains invalid characters")
    
    # Check numeric ranges
    if 'temperature' in settings:
        temp = settings['temperature']
        if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
            errors.append(f"Temperature must be between 0 and 2, got {temp}")
    
    if 'maxTokens' in settings:
        max_tokens = settings['maxTokens']
        if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 32000:
            errors.append(f"maxTokens must be between 1 and 32000, got {max_tokens}")
    
    if 'timeout' in settings:
        timeout = settings['timeout']
        if not isinstance(timeout, (int, float)) or timeout < 1:
            errors.append(f"Timeout must be a positive number, got {timeout}")
    
    return errors


def validate_config(config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate OpenClaw configuration.
    Returns (is_valid, list_of_errors).
    """
    errors = []
    
    if not config:
        return False, ["Config is empty"]
    
    # Check gateway section
    if 'gateway' not in config:
        errors.append("Missing required 'gateway' section")
    else:
        gateway = config['gateway']
        
        # Check providers
        if 'providers' not in gateway or not gateway['providers']:
            errors.append("No providers configured in gateway.providers")
        else:
            providers = gateway['providers']
            if not isinstance(providers, dict):
                errors.append("gateway.providers must be a dictionary")
            else:
                for provider_name, settings in providers.items():
                    if not isinstance(settings, dict):
                        errors.append(f"Provider '{provider_name}' settings must be a dictionary")
                    else:
                        provider_errors = validate_provider_config(provider_name, settings)
                        errors.extend(provider_errors)
        
        # Check default provider
        if 'defaultProvider' in gateway:
            default = gateway['defaultProvider']
            if 'providers' in gateway and default not in gateway['providers']:
                errors.append(f"Default provider '{default}' not found in configured providers")
    
    # Check for unknown top-level sections
    known_sections = ['gateway', 'logging', 'security', 'notifications']
    for key in config.keys():
        if key not in known_sections:
            errors.append(f"Unknown config section: '{key}'")
    
    return len(errors) == 0, errors


def main():
    """CLI entry point."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    config, error = load_config(config_path)
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    is_valid, errors = validate_config(config)
    
    if is_valid:
        print("✅ Config syntax is valid")
        sys.exit(0)
    else:
        print("❌ Config validation failed:")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
