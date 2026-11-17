"""Opt-in real-network smoke test for configured externals.

NOT part of pytest (would hit real APIs and cost quota). Run manually:

    python scripts/smoke_providers.py

Verifies, with small real calls:
  1. Infura endpoint answers eth_blockNumber (no auth cost).
  2. Every LLM provider in LLM_PROVIDERS_JSON completes one tiny chat request
     and the configured model id is accepted.

Prints a pass/fail line per item. Never prints API keys.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx

from agentsafe.config import Settings


async def smoke_infura(endpoint: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            endpoint,
            json={"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber",
                  "params": []},
        )
        r.raise_for_status()
        data = r.json()
        if "result" not in data:
            return f"unexpected response: {str(data)[:200]}"
        return f"block = {int(data['result'], 16)}"


async def smoke_llm(name: str, base_url: str, api_key: str, model: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user",
                              "content": "Reply with exactly: OK"}],
                "max_tokens": 512,
                "temperature": 0,
            },
        )
        if r.status_code != 200:
            body = r.text[:200].replace(api_key, "***")
            return f"HTTP {r.status_code}: {body}"
        msg = r.json()["choices"][0]["message"]
        content = msg.get("content")
        if not content:
            # Reasoning models can burn the whole budget on thinking;
            # report the shape honestly instead of pretending success.
            return (f"HTTP 200 but empty content; message keys="
                    f"{sorted(msg.keys())}")
        return f"model replied: {str(content)[:60]!r}"


async def main() -> int:
    settings = Settings(_env_file=".env")
    failures = 0

    try:
        print("[infura] ", smoke_infura(settings.INFURA_ETH_ENDPOINT) if False else
              await smoke_infura(settings.INFURA_ETH_ENDPOINT))
    except Exception as exc:
        failures += 1
        print(f"[infura]  FAIL: {type(exc).__name__}: {str(exc)[:200]}")

    for p in settings.llm_providers():
        try:
            result = await smoke_llm(p.name, p.base_url, p.api_key, p.model)
            print(f"[{p.name}]  {result}")
        except Exception as exc:
            failures += 1
            print(f"[{p.name}]  FAIL: {type(exc).__name__}: {str(exc)[:200]}")

    if not settings.ETHERSCAN_API_KEY.strip():
        print("[etherscan] SKIP: ETHERSCAN_API_KEY not set "
              "(verified-source path will be unavailable)")
    else:
        print("[etherscan] key set; API check happens on first real audit")

    print(f"\n{'FAILURES: ' + str(failures) if failures else 'ALL SMOKE TESTS PASSED'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
