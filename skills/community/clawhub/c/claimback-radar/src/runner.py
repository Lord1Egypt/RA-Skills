import json
import os
from pathlib import Path
from typing import Dict, Any

from openai import OpenAI


class ClaimbackRadar:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / "system.txt"
        return prompt_path.read_text(encoding="utf-8")

    def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        user_input: matches schema/input.json
        returns: matches schema/output.json
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": json.dumps(user_input, ensure_ascii=False)}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2
        )

        raw = response.choices[0].message.content
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Model returned invalid JSON: {e}\nRaw: {raw}")

        # Minimal validation: ensure required keys exist
        if "confirmation_card" not in result or "action_receipts" not in result:
            raise ValueError(f"Missing required keys in output. Got: {list(result.keys())}")

        return result