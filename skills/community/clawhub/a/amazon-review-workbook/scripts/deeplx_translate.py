from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Iterable

import requests

# Unicode Private Use Area character used as batch separator.
# DeepLX preserves this character through translation, allowing us to
# reliably split the combined result back into individual translations.
_BATCH_SEP = "\ue001"


def parse_translation(payload: object) -> str:
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, dict):
        for key in ("data", "translation", "translatedText", "result", "text"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        alternatives = payload.get("alternatives")
        if isinstance(alternatives, list) and alternatives:
            first = alternatives[0]
            if isinstance(first, str) and first.strip():
                return first.strip()
    raise ValueError(f"Unsupported DeepLX response payload: {payload!r}")


def candidate_env_files() -> list[Path]:
    files = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[1] / ".env",
    ]
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        if path not in seen:
            seen.add(path)
            deduped.append(path)
    return deduped


def read_env_value(key: str) -> str:
    explicit = os.getenv(key)
    if explicit:
        return explicit
    for env_path in candidate_env_files():
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            env_key, env_value = stripped.split("=", 1)
            if env_key.strip() != key:
                continue
            value = env_value.strip().strip("'").strip('"')
            if value:
                return value
    return ""


def resolve_api_url(explicit: str | None = None) -> str:
    api_url = explicit or read_env_value("DEEPLX_API_URL") or ""
    if not api_url:
        raise SystemExit("缺少 DEEPLX_API_URL。")
    return api_url


def resolve_api_key(explicit: str | None = None) -> str:
    return explicit or read_env_value("DEEPLX_API_KEY") or ""


def probe_deeplx(
    api_url: str, api_key: str = "", *, timeout: int = 12
) -> tuple[bool, str]:
    try:
        translated = translate_text(
            "hello",
            api_url=api_url,
            api_key=api_key,
            timeout=timeout,
            retries=1,
        )
        return True, translated
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def call_deeplx(
    text: str,
    *,
    api_url: str,
    api_key: str = "",
    source_lang: str = "auto",
    target_lang: str = "ZH",
    timeout: int = 30,
) -> str:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-api-key"] = api_key
        headers["apikey"] = api_key

    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(
            {
                "text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
        ),
        timeout=timeout,
    )
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError:
        payload = response.text
    return parse_translation(payload)


def translate_text(
    text: str,
    *,
    api_url: str,
    api_key: str = "",
    source_lang: str = "auto",
    target_lang: str = "ZH",
    timeout: int = 30,
    retries: int = 3,
    retry_sleep_seconds: float = 0.8,
) -> str:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return call_deeplx(
                text,
                api_url=api_url,
                api_key=api_key,
                source_lang=source_lang,
                target_lang=target_lang,
                timeout=timeout,
            )
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(retry_sleep_seconds)
    raise RuntimeError(
        f"DeepLX translation failed after {retries} attempts: {last_error}"
    )


def _join_for_translation(texts: list[str]) -> str:
    """Join multiple texts with a Unicode PUA separator that DeepLX preserves."""
    return _BATCH_SEP.join(texts)


def _split_translated(
    combined: str,
    original_count: int,
) -> list[str]:
    """Split the combined translation back into individual results.

    Uses the PUA separator to split. If the separator count doesn't match,
    falls back to safe defaults to prevent index misalignment.
    """
    sep_count = combined.count(_BATCH_SEP)
    expected_sep = original_count - 1

    if sep_count == expected_sep:
        parts = combined.split(_BATCH_SEP)
        return [p.strip() for p in parts]

    # Fallback: separator count mismatch (shouldn't happen with PUA char,
    # but guard against it anyway)
    if sep_count > expected_sep:
        # Too many separators — take first N parts
        parts = combined.split(_BATCH_SEP)[:original_count]
        # Pad if still short
        while len(parts) < original_count:
            parts.append("")
        return [p.strip() for p in parts]

    # Too few or zero separators — return empty strings to signal failure
    return [""] * original_count


def call_deeplx_batch(
    texts: list[str],
    *,
    api_url: str,
    api_key: str = "",
    source_lang: str = "auto",
    target_lang: str = "ZH",
    timeout: int = 60,
) -> list[str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-api-key"] = api_key
        headers["apikey"] = api_key

    combined = _join_for_translation(texts)

    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(
            {
                "text": combined,
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
        ),
        timeout=timeout,
    )
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError:
        raise ValueError(
            f"DeepLX batch response is not valid JSON: {response.text[:200]}"
        )

    translated = parse_translation(payload)
    return _split_translated(translated, len(texts))


def translate_texts_batch(
    texts: list[str],
    *,
    api_url: str,
    api_key: str = "",
    source_lang: str = "auto",
    target_lang: str = "ZH",
    timeout: int = 60,
    retries: int = 3,
    batch_size: int = 50,
    retry_sleep_seconds: float = 1.0,
) -> list[str]:
    all_results: list[str] = [""] * len(texts)
    batches = [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]

    for batch_idx, batch in enumerate(batches):
        last_error: Exception | None = None
        start_idx = batch_idx * batch_size
        batch_failed_completely = False
        for attempt in range(retries):
            try:
                results = call_deeplx_batch(
                    batch,
                    api_url=api_url,
                    api_key=api_key,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    timeout=timeout,
                )
                for j, result in enumerate(results):
                    if start_idx + j < len(all_results):
                        all_results[start_idx + j] = result
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                error_str = str(exc).lower()
                if "400" in error_str and attempt == 0:
                    batch_failed_completely = True
                    break
                if attempt + 1 < retries:
                    time.sleep(retry_sleep_seconds)
        else:
            if not batch_failed_completely:
                for j in range(len(batch)):
                    if start_idx + j < len(all_results):
                        all_results[start_idx + j] = f"[翻译失败: {last_error}]"

        if batch_failed_completely:
            for j, text in enumerate(batch):
                idx = start_idx + j
                if idx >= len(all_results):
                    break
                try:
                    result = translate_text(
                        text,
                        api_url=api_url,
                        api_key=api_key,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        timeout=min(timeout, 15),
                        retries=2,
                    )
                    all_results[idx] = result
                except Exception:  # noqa: BLE001
                    all_results[idx] = "[待翻译]"
                if (j + 1) % 10 == 0:
                    print(f"translate_fallback={idx + 1}/{len(texts)}")

    return all_results


def translate_texts(
    texts: Iterable[str],
    *,
    api_url: str,
    api_key: str = "",
    source_lang: str = "auto",
    target_lang: str = "ZH",
    timeout: int = 30,
    retries: int = 3,
    retry_sleep_seconds: float = 0.8,
) -> list[str]:
    return [
        translate_text(
            text,
            api_url=api_url,
            api_key=api_key,
            source_lang=source_lang,
            target_lang=target_lang,
            timeout=timeout,
            retries=retries,
            retry_sleep_seconds=retry_sleep_seconds,
        )
        for text in texts
    ]
