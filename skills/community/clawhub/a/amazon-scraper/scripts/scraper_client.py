"""Shared wrapper around `docker run amazon-scraper`.

The three monitor scripts each had their own copy of this with the same two bugs:

1. `docker run -t` allocated a PTY, which merges the container's stderr into stdout
   and rewrites line endings, so the JSON being parsed was already corrupted. There
   is no reason to allocate a TTY for a non-interactive capture.
2. They inferred "blocked" from `price is None`, which is indistinguishable from a
   genuinely price-less listing. The handler now reports status/failures explicitly,
   so a soft block never gets recorded as a real observation.
"""
from __future__ import annotations

import json
import subprocess

IMAGE = "amazon-scraper"
DEFAULT_TIMEOUT = 180


class ScrapeError(RuntimeError):
    """The scrape did not produce a trustworthy observation."""


def _extract_json(stdout: str) -> dict:
    start = stdout.find("{")
    if start == -1:
        raise ScrapeError("no JSON on stdout")
    try:
        return json.loads(stdout[start:])
    except json.JSONDecodeError as e:
        raise ScrapeError(f"unparseable JSON on stdout: {e}") from e


def scrape_url(url: str, *, timeout: int = DEFAULT_TIMEOUT, extra_args: list[str] | None = None) -> dict:
    """Run the handler for one URL and return its parsed payload.

    Raises ScrapeError unless the handler reported SUCCESS.
    """
    cmd = ["docker", "run", "--rm", IMAGE, "node", "assets/amazon_handler.js", url]
    if extra_args:
        cmd.extend(extra_args)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise ScrapeError(f"timeout after {timeout}s") from e

    payload = _extract_json(proc.stdout)
    status = payload.get("status")
    if status != "SUCCESS":
        raise ScrapeError(f"handler status={status}: {payload.get('failures') or payload.get('message')}")
    return payload


def scrape_detail(asin: str, *, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Return the product dict for one ASIN, or raise ScrapeError."""
    payload = scrape_url(f"https://www.amazon.com/dp/{asin}", timeout=timeout)
    products = payload.get("products") or []
    if not products:
        raise ScrapeError("handler returned no products")
    return products[0]
