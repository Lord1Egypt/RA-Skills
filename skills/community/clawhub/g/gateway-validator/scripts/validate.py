#!/usr/bin/env python3
"""
Gateway Validator - Tests config changes before applying to production.
Uses provider-level testing when isolated gateway isn't available.
"""

import sys
import os
import json
import time
import tempfile
import subprocess
import urllib.request
import urllib.error
import ssl
from pathlib import Path
from typing import Dict, Tuple, Optional
import shutil


def load_config(path: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str]]:
    """Load OpenClaw config file."""
    try:
        import yaml
    except ImportError:
        return None, "PyYAML not installed"
    
    if not path:
        for p in [Path.home() / '.openclaw' / 'config.yaml', Path.home() / '.openclaw' / 'config.yml']:
            if p.exists():
                path = str(p)
                break
    
    if not path:
        return None, "Config file not found"
    
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f), None
    except Exception as e:
        return None, f"Error loading config: {e}"


def validate_syntax(config: Dict) -> Tuple[bool, str]:
    """Validate config syntax and structure."""
    if not config:
        return False, "Config is empty"
    
    if 'gateway' not in config:
        return False, "Missing 'gateway' section"
    
    gateway = config['gateway']
    
    if 'providers' not in gateway or not gateway['providers']:
        return False, "No providers configured"
    
    if 'defaultProvider' in gateway:
        default = gateway['defaultProvider']
        if default not in gateway['providers']:
            return False, f"Default provider '{default}' not in configured providers"
    
    for name, settings in gateway['providers'].items():
        if not isinstance(settings, dict):
            return False, f"Provider '{name}' settings must be a dictionary"
        
        if name in ['openai', 'anthropic', 'moonshot']:
            if not settings.get('apiKey'):
                return False, f"Provider '{name}' requires an API key"
        
        if 'temperature' in settings:
            t = settings['temperature']
            if not isinstance(t, (int, float)) or t < 0 or t > 2:
                return False, f"Temperature must be 0-2, got {t}"
        
        if 'maxTokens' in settings:
            m = settings['maxTokens']
            if not isinstance(m, int) or m < 1:
                return False, f"maxTokens must be >= 1, got {m}"
    
    return True, "Config syntax valid"


def test_openai(api_key: str, base_url: Optional[str], model: Optional[str]) -> Tuple[bool, str]:
    """Test OpenAI API."""
    url = (base_url or 'https://api.openai.com/v1') + '/models'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}'})
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200:
                if model:
                    data = json.loads(resp.read().decode())
                    models = [m['id'] for m in data.get('data', [])]
                    if model not in models:
                        return False, f"Model '{model}' not available from OpenAI"
                return True, "API key valid"
            return False, f"API returned {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "API key is invalid or expired"
        elif e.code == 404:
            return False, "Endpoint not found"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {str(e)[:100]}"


def test_anthropic(api_key: str, base_url: Optional[str], model: Optional[str]) -> Tuple[bool, str]:
    """Test Anthropic API."""
    url = (base_url or 'https://api.anthropic.com') + '/v1/messages'
    test_model = model or 'claude-3-5-sonnet-20241022'
    
    data = json.dumps({
        'model': test_model,
        'max_tokens': 1,
        'messages': [{'role': 'user', 'content': 'Hi'}]
    }).encode()
    
    req = urllib.request.Request(
        url, data=data,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
    )
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return True, "API key valid"
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        if e.code == 401:
            return False, "API key is invalid or expired"
        elif 'model' in err.lower():
            return False, f"Model '{test_model}' not found or invalid"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {str(e)[:100]}"


def test_moonshot(api_key: str, base_url: Optional[str], model: Optional[str]) -> Tuple[bool, str]:
    """Test Moonshot API."""
    url = (base_url or 'https://api.moonshot.cn/v1') + '/models'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {api_key}'})
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200 and model:
                data = json.loads(resp.read().decode())
                models = [m['id'] for m in data.get('data', [])]
                if model not in models:
                    return False, f"Model '{model}' not available from Moonshot"
            return True, "API key valid"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "API key is invalid or expired"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {str(e)[:100]}"


def test_google(api_key: str, base_url: Optional[str], model: Optional[str]) -> Tuple[bool, str]:
    """Test Google Gemini API."""
    test_model = model or 'gemini-1.5-flash'
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_model}?key={api_key}"
    
    req = urllib.request.Request(url)
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return True, "API key valid"
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        if e.code == 400 and 'API key' in err:
            return False, "API key is invalid"
        elif e.code == 404 or 'not found' in err.lower():
            return False, f"Model '{test_model}' not found"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {str(e)[:100]}"


def test_ollama(base_url: Optional[str], model: Optional[str]) -> Tuple[bool, str]:
    """Test Ollama connection."""
    url = (base_url or 'http://localhost:11434') + '/api/tags'
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200 and model:
                data = json.loads(resp.read().decode())
                models = [m['name'] for m in data.get('models', [])]
                if model not in models:
                    return False, f"Model '{model}' not pulled locally. Run: ollama pull {model}"
            return True, "Ollama is running"
    except urllib.error.URLError:
        return False, "Ollama not running"
    except Exception as e:
        return False, f"Connection failed: {str(e)[:100]}"


def test_provider(name: str, settings: Dict) -> Tuple[bool, str]:
    """Test a provider."""
    api_key = settings.get('apiKey', '')
    base_url = settings.get('baseUrl')
    model = settings.get('model')
    
    if name == 'openai':
        return test_openai(api_key, base_url, model)
    elif name == 'anthropic':
        return test_anthropic(api_key, base_url, model)
    elif name == 'moonshot':
        return test_moonshot(api_key, base_url, model)
    elif name == 'google':
        return test_google(api_key, base_url, model)
    elif name == 'ollama':
        return test_ollama(base_url, model)
    elif name == 'azure':
        return test_openai(api_key, base_url, model)  # Azure uses OpenAI-compatible API
    else:
        return True, f"Unknown provider '{name}', validation skipped"


def validate_changes(changes: Dict, config_path: Optional[str] = None) -> Tuple[bool, str]:
    """Main validation function."""
    current_config, error = load_config(config_path)
    if not current_config:
        return False, f"Cannot load config: {error}"
    
    # Apply changes
    try:
        import copy
        test_config = copy.deepcopy(current_config)
        
        for key, value in changes.items():
            parts = key.split('.')
            target = test_config
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            target[parts[-1]] = value
    except Exception as e:
        return False, f"Error applying changes: {e}"
    
    print("🧪 Testing configuration changes...")
    
    # Level 1: Syntax
    print("   Checking config syntax...")
    valid, msg = validate_syntax(test_config)
    if not valid:
        return False, msg
    print("   ✅ Syntax valid")
    
    # Level 2: Test providers
    gateway = test_config.get('gateway', {})
    providers = gateway.get('providers', {})
    default = gateway.get('defaultProvider')
    
    if not providers:
        return False, "No providers configured"
    
    print("   Testing providers...")
    
    # Test default first
    if default and default in providers:
        print(f"      {default}...", end=" ")
        success, msg = test_provider(default, providers[default])
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
            return False, f"Default provider '{default}' failed: {msg}"
    
    # Test others
    for name, settings in providers.items():
        if name == default:
            continue
        print(f"      {name}...", end=" ")
        success, msg = test_provider(name, settings)
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
            return False, f"Provider '{name}' failed: {msg}"
    
    return True, "All tests passed"


def main():
    """CLI entry point."""
    config_path = None
    changes = {}
    
    for arg in sys.argv[1:]:
        if arg.startswith('--config='):
            config_path = arg.split('=', 1)[1]
        elif '=' in arg:
            key, value = arg.split('=', 1)
            changes[key] = value
    
    if not changes:
        print("Usage: validate.py [--config=path] key1=value1 [key2=value2 ...]")
        print("Example: validate.py providers.anthropic.apiKey=sk-xxx defaultProvider=anthropic")
        sys.exit(1)
    
    should_apply, message = validate_changes(changes, config_path)
    
    if should_apply:
        print(f"\n✅ {message}")
        print("   Change can be safely applied to production.")
        sys.exit(0)
    else:
        print(f"\n❌ {message}")
        print("   This change would break the gateway.")
        sys.exit(1)


if __name__ == "__main__":
    main()
