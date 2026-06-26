"""LLM summarizer for feed digests."""
from __future__ import annotations

import os
from pathlib import Path

import requests


class LLMSummaryError(Exception):
    """Raised when LLM summarization fails."""


def summarize(
    digest_markdown: str,
    provider: str,
    model: str,
    prompt_template: str,
    max_tokens: int = 800,
    temperature: float = 0.2,
) -> str:
    """Generate an LLM summary from the digest."""
    if provider == "perplexity":
        return _call_perplexity(
            digest_markdown, model, prompt_template, max_tokens, temperature
        )
    elif provider == "openai":
        return _call_openai(
            digest_markdown, model, prompt_template, max_tokens, temperature
        )
    elif provider == "ollama":
        return _call_ollama(
            digest_markdown, model, prompt_template, max_tokens, temperature
        )
    else:
        raise LLMSummaryError(f"Unbekannter LLM-Provider: {provider}")


def _call_perplexity(
    digest: str, model: str, prompt_template: str, max_tokens: int, temperature: float
) -> str:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise LLMSummaryError("PERPLEXITY_API_KEY nicht gesetzt")

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": digest[:15000]},  # truncate
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise LLMSummaryError(f"Perplexity API-Fehler: {e}") from e
    except (KeyError, IndexError) as e:
        raise LLMSummaryError(f"Unerwartete Perplexity-Response: {e}") from e


def _call_openai(
    digest: str, model: str, prompt_template: str, max_tokens: int, temperature: float
) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise LLMSummaryError("OPENAI_API_KEY nicht gesetzt")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": digest[:15000]},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise LLMSummaryError(f"OpenAI API-Fehler: {e}") from e
    except (KeyError, IndexError) as e:
        raise LLMSummaryError(f"Unerwartete OpenAI-Response: {e}") from e


def _call_ollama(
    digest: str, model: str, prompt_template: str, max_tokens: int, temperature: float
) -> str:
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    url = f"{ollama_host}/api/generate"
    payload = {
        "model": model,
        "prompt": f"{prompt_template}\n\n---\n\n{digest[:15000]}",
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }

    try:
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")
    except requests.RequestException as e:
        raise LLMSummaryError(f"Ollama API-Fehler: {e}") from e


def load_prompt_template(prompt_file: str | Path) -> str:
    """Load prompt template from file."""
    path = Path(prompt_file)
    if not path.exists():
        # Try relative to skill root
        skill_root = Path(__file__).resolve().parent.parent.parent
        path = skill_root / prompt_file

    if not path.exists():
        raise LLMSummaryError(f"Prompt-Template nicht gefunden: {prompt_file}")

    with open(path, encoding="utf-8") as f:
        return f.read()
