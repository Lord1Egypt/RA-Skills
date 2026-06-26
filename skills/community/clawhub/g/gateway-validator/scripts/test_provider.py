#!/usr/bin/env python3
"""
Test provider connectivity and model validity.
Makes lightweight API calls to verify credentials and model availability.
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, Tuple, Optional
import urllib.request
import urllib.error
import ssl

# Provider API endpoints for validation
PROVIDER_ENDPOINTS = {
    'openai': {
        'models_url': 'https://api.openai.com/v1/models',
        'test_model': 'gpt-4o-mini',
    },
    'anthropic': {
        'models_url': None,  # No models endpoint, use messages
        'test_model': 'claude-3-5-sonnet-20241022',
        'api_version': '2023-06-01',
    },
    'moonshot': {
        'models_url': 'https://api.moonshot.cn/v1/models',
        'test_model': 'kimi-k2.5',
    },
    'google': {
        'models_url': None,  # Use direct model check
        'test_model': 'gemini-1.5-flash',
    },
}


def load_config(config_path: Optional[str] = None) -> Tuple[Optional[Dict], Optional[str]]:
    """Load config and return parsed providers."""
    try:
        import yaml
    except ImportError:
        return None, "PyYAML not installed, cannot parse config"
    
    if config_path:
        path = Path(config_path)
    else:
        path = Path.home() / '.openclaw' / 'config.yaml'
    
    if not path.exists():
        return None, f"Config not found: {path}"
    
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        return config, None
    except Exception as e:
        return None, f"Error loading config: {e}"


def test_openai_api(api_key: str, base_url: str = None, model: str = None) -> Tuple[bool, str]:
    """Test OpenAI API connectivity and model."""
    url = (base_url or 'https://api.openai.com/v1') + '/models'
    
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                if model:
                    model_ids = [m['id'] for m in data.get('data', [])]
                    if model not in model_ids:
                        return False, f"Model '{model}' not found in available models"
                return True, "API key valid"
            return False, f"API returned status {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Invalid API key (401 Unauthorized)"
        elif e.code == 404:
            return False, f"Model or endpoint not found (404)"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {e}"


def test_anthropic_api(api_key: str, base_url: str = None, model: str = None) -> Tuple[bool, str]:
    """Test Anthropic API with a minimal request."""
    url = (base_url or 'https://api.anthropic.com') + '/v1/messages'
    
    test_model = model or 'claude-3-5-sonnet-20241022'
    
    data = json.dumps({
        'model': test_model,
        'max_tokens': 1,
        'messages': [{'role': 'user', 'content': 'Hi'}]
    }).encode()
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
    )
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200:
                return True, "API key valid"
            return False, f"API returned status {resp.status}"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        if e.code == 401:
            return False, "Invalid API key (401 Unauthorized)"
        elif e.code == 404:
            if model and model in err_body:
                return False, f"Model '{model}' not found"
            return False, "API endpoint not found (404)"
        elif 'model' in err_body.lower():
            return False, f"Invalid model: {model}"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {e}"


def test_moonshot_api(api_key: str, base_url: str = None, model: str = None) -> Tuple[bool, str]:
    """Test Moonshot API."""
    url = (base_url or 'https://api.moonshot.cn/v1') + '/models'
    
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                if model:
                    model_ids = [m['id'] for m in data.get('data', [])]
                    if model not in model_ids:
                        return False, f"Model '{model}' not available"
                return True, "API key valid"
            return False, f"API returned status {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Invalid API key (401 Unauthorized)"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {e}"


def test_google_api(api_key: str, base_url: str = None, model: str = None) -> Tuple[bool, str]:
    """Test Google Gemini API."""
    test_model = model or 'gemini-1.5-flash'
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_model}?key={api_key}"
    
    req = urllib.request.Request(url)
    
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.status == 200:
                return True, "API key valid"
            return False, f"API returned status {resp.status}"
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        if e.code == 400 and 'API key' in err_body:
            return False, "Invalid API key"
        elif e.code == 404 or 'not found' in err_body.lower():
            return False, f"Model '{test_model}' not found"
        return False, f"API error: {e.code}"
    except Exception as e:
        return False, f"Connection failed: {e}"


def test_ollama_api(base_url: str = None, model: str = None) -> Tuple[bool, str]:
    """Test Ollama connectivity."""
    url = (base_url or 'http://localhost:11434') + '/api/tags'
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                if model:
                    data = json.loads(resp.read().decode())
                    models = [m['name'] for m in data.get('models', [])]
                    if model not in models:
                        return False, f"Model '{model}' not pulled locally. Run: ollama pull {model}"
                return True, "Ollama is running"
            return False, f"Ollama returned status {resp.status}"
    except urllib.error.URLError:
        return False, "Ollama not running at {url}"
    except Exception as e:
        return False, f"Connection failed: {e}"


def test_provider(provider: str, settings: Dict) -> Tuple[bool, str]:
    """Test a specific provider configuration."""
    api_key = settings.get('apiKey', '')
    base_url = settings.get('baseUrl')
    model = settings.get('model')
    
    if provider == 'openai':
        return test_openai_api(api_key, base_url, model)
    elif provider == 'anthropic':
        return test_anthropic_api(api_key, base_url, model)
    elif provider == 'moonshot':
        return test_moonshot_api(api_key, base_url, model)
    elif provider == 'google':
        return test_google_api(api_key, base_url, model)
    elif provider == 'ollama':
        return test_ollama_api(base_url, model)
    else:
        return False, f"Unknown provider: {provider}"


def main():
    """CLI entry point."""
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    config, error = load_config(config_path)
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    if 'gateway' not in config or 'providers' not in config['gateway']:
        print("❌ No providers configured")
        sys.exit(1)
    
    providers = config['gateway']['providers']
    all_passed = True
    
    print("🧪 Testing provider connectivity...")
    
    for provider_name, settings in providers.items():
        print(f"\n  Testing {provider_name}...", end=" ")
        
        success, message = test_provider(provider_name, settings)
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All providers validated successfully")
        sys.exit(0)
    else:
        print("❌ Some providers failed validation")
        sys.exit(1)


if __name__ == "__main__":
    main()
