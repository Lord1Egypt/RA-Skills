#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.
# Credentials are read from OpenClaw model config or OPENAI_API_KEY env var.

"""
LLM Adapter for doc2slides.
Supports multiple providers: OpenAI, Zhipu (GLM), local models.

Configuration read from ~/.openclaw/models.json or environment variables.
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import OpenAI SDK
try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    logger.warning("openai not installed. Run: pip install openai>=1.0.0")


class LLMAdapter:
    """
    Async LLM adapter supporting multiple providers.
    
    Supported providers:
    - openai: OpenAI GPT models
    - zhipu: Zhipu GLM models
    - deepseek: DeepSeek models
    - local: Local models via Ollama
    """
    
    def __init__(self, model: str = None, config_path: str = None):
        """
        Initialize LLM adapter.
        
        Args:
            model: Model name (e.g., "glm-4-flash", "gpt-4o", "deepseek-chat")
            config_path: Path to config file (default: ~/.openclaw/models.json)
        """
        self.model = model or self._get_default_model()
        self.config = self._load_config(config_path)
        self.client = None

        if self.model:
            self.provider = self._detect_provider()
            try:
                self.client = self._init_client()
            except (ValueError, RuntimeError):
                self.client = None  # No credentials available, LLM mode disabled
        else:
            self.provider = None  # No LLM configured, template mode only
    
    def _get_default_model(self) -> str:
        """Get default model from environment or OpenClaw config."""
        # 1. Check environment variable
        env_model = os.getenv("LLM_MODEL")
        if env_model:
            return env_model

        # 2. Check OpenClaw models.json for first available model
        models_config = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "models.json"
        if models_config.exists():
            try:
                with open(models_config, 'r') as f:
                    config = json.load(f)
                providers = config.get("providers", {})
                for provider_name, provider_config in providers.items():
                    models = provider_config.get("models", [])
                    if models:
                        return models[0].get("id", "glm-4-flash")
            except:
                pass

        # 3. No model configured — return None to signal "no LLM available"
        return None
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load model configuration."""
        # Try config file first
        if config_path:
            path = Path(config_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # Try OpenClaw config location
        openclaw_config = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_config.exists():
            with open(openclaw_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Extract models.providers config
                providers = config.get("models", {}).get("providers", {})
                return {"providers": providers}
        
        # Try default models.json
        default_config = Path.home() / ".openclaw" / "models.json"
        if default_config.exists():
            with open(default_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Return empty config
        return {}
    
    def _detect_provider(self) -> str:
        """Detect provider from model name."""
        if not self.model:
            return None
        if self.model.startswith("glm") or "zhipu" in self.model:
            return "zhipu"
        elif self.model.startswith("gpt") or "openai" in self.model:
            return "openai"
        elif "deepseek" in self.model:
            return "deepseek"
        elif self.model.startswith("local/"):
            return "local"
        else:
            # Try to get from config
            model_config = self.config.get("models", {}).get(self.model, {})
            return model_config.get("provider", "zhipu")
    
    def _init_client(self) -> AsyncOpenAI:
        """Initialize API client based on provider."""
        if not HAS_OPENAI:
            raise RuntimeError("openai package not installed. Run: pip install openai>=1.0.0")
        
        # Get API key and base URL based on provider
        api_key = None
        base_url = None
        
        if self.provider == "zhipu":
            api_key = os.getenv("ZHIPU_API_KEY") or self._get_config_value("apiKey")
            base_url = "https://open.bigmodel.cn/api/paas/v4"
        
        elif self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY") or self._get_config_value("apiKey")
            base_url = os.getenv("OPENAI_BASE_URL") or self._get_config_value("baseUrl")
        
        elif self.provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY") or self._get_config_value("apiKey")
            base_url = "https://api.deepseek.com"
        
        elif self.provider == "local":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            api_key = "ollama"  # Dummy key for Ollama
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        if not api_key:
            raise ValueError(f"API key not found for provider: {self.provider}")
        
        return AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    def _get_config_value(self, key: str) -> Optional[str]:
        """Get value from provider config."""
        # Try providers config first
        providers = self.config.get("providers", {})
        provider_config = providers.get(self.provider, {})
        value = provider_config.get(key)
        if value:
            return value
        
        # Fallback to model-specific config
        model_config = self.config.get("models", {}).get(self.model, {})
        return model_config.get(key)
    
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system_prompt: str = None,
        stream: bool = False,
        timeout: float = 300.0
    ) -> Dict[str, Any]:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: System prompt (optional)
            stream: Enable streaming (not implemented yet)
            timeout: Request timeout in seconds (default: 300)

        Returns:
            Dict with 'content' and 'usage' keys
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            # For GLM reasoning models, disable thinking mode
            extra_body = {}
            if self.provider == "zhipu" and ("glm-4.5" in self.model or "glm-5" in self.model):
                extra_body["enable_thinking"] = False

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                extra_body=extra_body if extra_body else None,
                timeout=timeout
            )
            
            # Extract content
            content = response.choices[0].message.content or ""
            
            # Handle reasoning models that return reasoning_content
            if not content and hasattr(response.choices[0].message, 'reasoning_content'):
                content = response.choices[0].message.reasoning_content or ""
            
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            return {
                "content": content,
                "usage": usage,
                "model": self.model,
                "provider": self.provider
            }
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    async def generate_stream(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate text with streaming.
        
        Yields:
            Text chunks
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            extra_body = {}
            if self.provider == "zhipu" and ("glm-4.5" in self.model or "glm-5" in self.model):
                extra_body["enable_thinking"] = False
            
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
                extra_body=extra_body if extra_body else None
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}")
            raise


# Test function
async def test_adapter():
    """Test LLM adapter."""
    print("Testing LLM Adapter...")
    
    try:
        adapter = LLMAdapter(model="glm-4-flash")
        print(f"  Provider: {adapter.provider}")
        print(f"  Model: {adapter.model}")
        
        result = await adapter.generate(
            prompt="用一句话介绍你自己",
            max_tokens=100
        )
        
        print(f"\n  Response: {result['content']}")
        print(f"  Tokens: {result['usage']}")
        
        print("\n✅ LLM Adapter test passed")
    
    except Exception as e:
        print(f"\n❌ LLM Adapter test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_adapter())
