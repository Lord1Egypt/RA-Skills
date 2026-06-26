"""
LLM Client for Ghostclaw.
"""

import json
import logging
import asyncio
from typing import AsyncGenerator, Optional, List, Dict, Any
from pathlib import Path

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from ghostclaw.core.config import GhostclawConfig
from .providers import OpenAIProvider, AnthropicProvider

logger = logging.getLogger("ghostclaw.llm_client")


class TokenBudgetExceededError(Exception):
    """Raised when token budget for LLM prompt is exceeded."""
    pass


class LLMClient:
    """Wrapper for connecting to LLM providers and orchestrating analysis."""

    def __init__(self, config: GhostclawConfig, repo_path: str):
        self.config = config
        self.repo_path = repo_path
        self.max_tokens = 100000
        self.provider = None
        self.model = ""
        
        # Token usage tracking
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.total_tokens: int = 0

        self._setup_provider()

    def _setup_provider(self):
        """Initialize the specific provider based on config."""
        provider_name = self.config.ai_provider
        api_key = self.config.api_key

        if provider_name == "openai":
            self.model = self.config.ai_model or "gpt-4o"
            self.provider = OpenAIProvider(api_key=api_key, client_cls=AsyncOpenAI)
        elif provider_name == "anthropic":
            self.model = self.config.ai_model or "claude-3-5-sonnet-20241022"
            self.provider = AnthropicProvider(api_key=api_key, client_cls=AsyncAnthropic)
        else: # Default fallback (openrouter or unknown)
            self.model = self.config.ai_model or "anthropic/claude-3.5-sonnet"
            base_url = "https://openrouter.ai/api/v1"
            headers = {
                "HTTP-Referer": "https://github.com/Ev3lynx727/ghostclaw",
                "X-Title": "Ghostclaw Architecture Engine",
            }
            self.provider = OpenAIProvider(api_key=api_key, base_url=base_url, headers=headers, client_cls=AsyncOpenAI)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for a given text."""
        if HAS_TIKTOKEN:
            try:
                encoding = tiktoken.get_encoding("cl100k_base")
                return len(encoding.encode(text))
            except Exception:
                return len(text) // 4
        return len(text) // 4

    def _check_token_budget(self, prompt: str) -> str:
        """Check if prompt fits in budget; throw error or truncate if not."""
        token_count = self._estimate_tokens(prompt)

        if self.config.dry_run:
            print(f"[DRY RUN] Token budget check: Estimated {token_count} tokens.")
            print(f"[DRY RUN] Payload snippet:\n{prompt[:500]}...\n")
            return prompt

        if token_count > self.max_tokens:
            raise TokenBudgetExceededError(
                f"Prompt token count ({token_count}) exceeds the maximum allowed ({self.max_tokens})."
            )
        return prompt

    def _log_verbose(self, payload: dict, response_data: dict = None, error: str = None):
        """Log API requests and responses if verbose mode is enabled."""
        if not self.config.verbose:
            return

        debug_log_path = Path(self.repo_path) / ".ghostclaw" / "debug.log"
        debug_log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {"request": payload}
        if response_data: log_entry["response"] = response_data
        if error: log_entry["error"] = error

        try:
            with open(debug_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, indent=2) + "\n\n")
        except Exception as e:
            logger.error(f"Failed to write verbose log: {e}")

    async def _retry(self, func, *args, **kwargs):
        """Retry wrapper for async non-generator functions."""
        attempts = 0
        while attempts < self.config.retry_attempts:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts >= self.config.retry_attempts: raise
                if isinstance(e, (TokenBudgetExceededError, ValueError)): raise
                delay = min(self.config.retry_backoff_factor * (2 ** (attempts - 1)), self.config.retry_max_delay)
                logger.warning(f"Retry {attempts}/{self.config.retry_attempts} for {func.__name__}")
                await asyncio.sleep(delay)

    async def _retry_stream(self, gen_func, *args, **kwargs):
        """Retry wrapper for async generator functions."""
        attempts = 0
        while attempts < self.config.retry_attempts:
            try:
                async for item in gen_func(*args, **kwargs):
                    yield item
                return
            except Exception as e:
                attempts += 1
                if attempts >= self.config.retry_attempts: raise
                if isinstance(e, (TokenBudgetExceededError, ValueError)): raise
                delay = min(self.config.retry_backoff_factor * (2 ** (attempts - 1)), self.config.retry_max_delay)
                logger.warning(f"Retry stream {attempts}/{self.config.retry_attempts}")
                await asyncio.sleep(delay)

    async def generate_analysis(self, prompt: str) -> dict:
        """Generate analysis from the LLM."""
        prompt = self._check_token_budget(prompt)
        if self.config.dry_run:
            return {"content": "Dry run enabled. API call skipped."}
        if not self.config.api_key:
            raise ValueError("API key not provided.")

        system_prompt = "You are Ghostclaw, an expert software architect. Analyze the provided codebase metrics and context and output a markdown report detailing system-level flow, cohesion, and tech stack best practices."

        async def _api_call():
            result = await self.provider.generate(self.model, system_prompt, prompt)
            usage = result.get("usage")
            if usage:
                self.prompt_tokens += usage["prompt_tokens"]
                self.completion_tokens += usage["completion_tokens"]
                self.total_tokens = self.prompt_tokens + self.completion_tokens
            return {"content": result["content"], "reasoning": result.get("reasoning")}

        return await self._retry(_api_call)

    async def stream_analysis(self, prompt: str) -> AsyncGenerator[dict, None]:
        """Stream analysis from the LLM."""
        prompt = self._check_token_budget(prompt)
        if self.config.dry_run:
            yield {"type": "content", "content": "Dry run enabled. API call skipped."}
            return
        if not self.config.api_key:
            raise ValueError("API key not provided.")

        system_prompt = "You are Ghostclaw, an expert software architect. Analyze the provided codebase metrics and context and output a markdown report detailing system-level flow, cohesion, and tech stack best practices."

        # Reset counters
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

        async def _stream_call():
            async for chunk in self.provider.stream(self.model, system_prompt, prompt):
                if chunk["type"] == "usage":
                    self.prompt_tokens += chunk["prompt_tokens"]
                    self.completion_tokens += chunk["completion_tokens"]
                    self.total_tokens = self.prompt_tokens + self.completion_tokens
                else:
                    yield chunk

        async for item in self._retry_stream(_stream_call):
            yield item

    async def test_connection(self) -> bool:
        """Test the connection to the LLM provider."""
        if not self.provider or not self.config.api_key:
            return False
        try:
            if isinstance(self.provider, AnthropicProvider):
                await self.provider.client.messages.create(
                    model=self.model, max_tokens=1, 
                    messages=[{"role": "user", "content": "ping"}]
                )
            else:
                await self.provider.client.models.list()
            return True
        except Exception:
            return False

    async def list_models(self) -> list:
        """List available models."""
        if not self.provider or not self.config.api_key:
            return [self.model]
        try:
            if isinstance(self.provider, OpenAIProvider):
                response = await self.provider.client.models.list()
                return sorted([m.id for m in response.data])
            return [self.model]
        except Exception:
            return [self.model]
