"""LLM client abstraction — supports OpenAI, Anthropic, and OpenRouter."""

import json

from ..utils.logger import log


class LLMClient:
    """Unified LLM interface for concept generation."""

    def __init__(self, provider: str, model: str, api_key: str, base_url: str | None = None):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.9) -> str:
        """Generate a completion from the LLM. Returns raw text response."""
        if self.provider == "anthropic":
            return self._anthropic(system_prompt, user_prompt, temperature)
        else:
            # openai, openrouter both use OpenAI-compatible API
            return self._openai_compat(system_prompt, user_prompt, temperature)

    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.9) -> dict | list:
        """Generate and parse a JSON response from the LLM."""
        text = self.generate(system_prompt, user_prompt, temperature)
        # Try to extract JSON from the response
        text = text.strip()
        if text.startswith("```"):
            # Strip markdown code blocks
            lines = text.split("\n")
            lines = [l for l in lines if not l.startswith("```")]
            text = "\n".join(lines)
        return json.loads(text)

    def _openai_compat(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """OpenAI-compatible API (works with OpenAI, OpenRouter)."""
        from openai import OpenAI

        base_url = self.base_url
        if not base_url:
            if self.provider == "openrouter":
                base_url = "https://openrouter.ai/api/v1"
            # else: default OpenAI base URL

        client = OpenAI(api_key=self.api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content

    def _anthropic(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Anthropic Claude API."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("Install anthropic: pip install openclaw[anthropic]")

        client = anthropic.Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return resp.content[0].text
