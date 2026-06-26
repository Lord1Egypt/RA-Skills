"""OpenAI provider."""

import json
from typing import Any

import httpx

from .base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI API provider."""

    name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com",
    ):
        super().__init__(api_key, model)
        self.base_url = base_url

    async def analyze(
        self,
        directories: list[dict[str, Any]],
        user_context: str | None = None,
        target_drive: str | None = None,
    ) -> dict[str, Any]:
        """Analyze using OpenAI API."""
        prompt = self._build_prompt(directories, user_context, target_drive)

        # Determine the correct endpoint
        # Standard OpenAI: /v1/chat/completions
        # Baidu Qianfan Coding: /chat/completions (no /v1)
        if "/v1" in self.base_url or self.base_url.endswith("/v1"):
            endpoint = f"{self.base_url}/chat/completions"
        elif "/v2/coding" in self.base_url or self.base_url.endswith("/coding"):
            endpoint = f"{self.base_url}/chat/completions"
        else:
            endpoint = f"{self.base_url}/v1/chat/completions"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a disk space management expert. "
                                "Respond only with valid JSON."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Parse JSON response
            try:
                # Try direct parse first
                try:
                    result = json.loads(content.strip())
                except json.JSONDecodeError:
                    # Try to extract JSON from markdown code block
                    import re
                    # Try ```json ... ```
                    json_match = re.search(r'```json\s*\n?(\{.*?\})\s*```', content, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group(1))
                    else:
                        # Try to find JSON object directly
                        json_match = re.search(r'\{[\s\S]*"recommendations"[\s\S]*\}', content)
                        if json_match:
                            result = json.loads(json_match.group(0))
                        else:
                            raise json.JSONDecodeError("No JSON found", content, 0)
                return {
                    "recommendations": result.get("recommendations", []),
                    "summary": result.get("summary", ""),
                    "total_releasable_mb": result.get("total_releasable_mb", 0),
                    "provider": self.name,
                }
            except json.JSONDecodeError as e:
                return {
                    "recommendations": [],
                    "summary": content,
                    "total_releasable_mb": 0,
                    "provider": self.name,
                    "error": f"Failed to parse AI response as JSON: {str(e)}",
                }

    async def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/v1/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                return response.status_code == 200
        except Exception:
            return False
