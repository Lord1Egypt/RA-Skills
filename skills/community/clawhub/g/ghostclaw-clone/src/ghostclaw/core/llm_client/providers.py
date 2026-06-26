"""
LLM providers for Ghostclaw.
"""

import logging
from typing import AsyncGenerator, Optional, Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

logger = logging.getLogger("ghostclaw.llm_client.providers")


class BaseProvider:
    """Base class for LLM providers."""
    async def generate(self, model: str, system_prompt: str, prompt: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def stream(self, model: str, system_prompt: str, prompt: str) -> AsyncGenerator[Dict[str, Any], None]:
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI and OpenRouter (OpenAI-compatible)."""

    def __init__(self, api_key: str, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None, client_cls=AsyncOpenAI):
        self.base_url = base_url
        self.client = client_cls(api_key=api_key, base_url=base_url, default_headers=headers)

    async def generate(self, model: str, system_prompt: str, prompt: str) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        message = response.choices[0].message
        content = message.content
        reasoning = getattr(message, 'reasoning_content', None)
        usage = getattr(response, 'usage', None)
        
        return {
            "content": content,
            "reasoning": reasoning,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            } if usage else None
        }

    async def stream(self, model: str, system_prompt: str, prompt: str) -> AsyncGenerator[Dict[str, Any], None]:
        kwargs = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": True,
        }
        
        # stream_options is only supported by native OpenAI
        if self.base_url is None:
            kwargs["stream_options"] = {"include_usage": True}
            
        stream = await self.client.chat.completions.create(**kwargs)
        async for chunk in stream:
            if not chunk.choices:
                if hasattr(chunk, 'usage') and chunk.usage:
                    yield {
                        "type": "usage",
                        "prompt_tokens": chunk.usage.prompt_tokens,
                        "completion_tokens": chunk.usage.completion_tokens
                    }
                continue
            
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content is not None:
                yield {"type": "content", "content": delta.content}
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                yield {"type": "reasoning", "content": delta.reasoning_content}


class AnthropicProvider(BaseProvider):
    """Provider for Anthropic Claude."""

    def __init__(self, api_key: str, client_cls=AsyncAnthropic):
        self.client = client_cls(api_key=api_key)

    async def generate(self, model: str, system_prompt: str, prompt: str) -> Dict[str, Any]:
        response = await self.client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        reasoning = getattr(response, 'thinking', None)
        usage = getattr(response, 'usage', None)

        return {
            "content": content,
            "reasoning": reasoning,
            "usage": {
                "prompt_tokens": usage.input_tokens,
                "completion_tokens": usage.output_tokens,
                "total_tokens": usage.input_tokens + usage.output_tokens
            } if usage else None
        }

    async def stream(self, model: str, system_prompt: str, prompt: str) -> AsyncGenerator[Dict[str, Any], None]:
        async with self.client.messages.stream(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for event in stream:
                if event.type == "text_delta" and event.text is not None:
                    yield {"type": "content", "content": event.text}
                elif event.type == "thinking_delta" and event.thinking is not None:
                    yield {"type": "reasoning", "content": event.thinking}
            
            usage = stream.get_final_usage()
            if usage:
                yield {
                    "type": "usage",
                    "prompt_tokens": usage.input_tokens,
                    "completion_tokens": usage.output_tokens
                }
