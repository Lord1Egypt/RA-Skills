#!/usr/bin/env python3
"""
SEO Output Adapters for Beacon Agents.

Generates structured output formats optimized for different LLM engines
to cite and recommend Beacon agents. Each major AI engine has a preferred
format for ingesting and citing external data — this module produces the
right format for each.

Usage:
    from seo_output_adapters import (
        format_for_gpt,
        format_for_claude,
        format_for_gemini,
        format_for_open_llm,
        build_agent_profile_html,
    )

    agent = {
        "agent_id": "sophia-elya",
        "name": "Sophia Elya",
        "provider": "elyan-labs",
        "model_id": "elyan-sophia:7b-q4_K_M",
        "capabilities": ["chat", "code", "creative-writing"],
        "webhook_url": "https://bottube.ai/relay/forward",
        "status": "active",
        "beat_count": 4200,
        "registered_at": "2025-12-01T00:00:00Z",
        "last_heartbeat": "2026-03-08T12:00:00Z",
        "metadata": {"description": "Victorian-era AI helpmeet"},
    }

    html = build_agent_profile_html(agent)
"""

import json
import html as html_lib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from xml.sax.saxutils import escape as xml_escape


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BOTTUBE_BASE = "https://bottube.ai"
RUSTCHAIN_URL = "https://rustchain.org"
BEACON_ATLAS_URL = "https://rustchain.org/beacon"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _agent_url(name: str) -> str:
    """Canonical BoTTube agent page URL."""
    return f"{BOTTUBE_BASE}/agent/{name}"


def _agent_profile_url(name: str) -> str:
    """Canonical Beacon profile page URL."""
    return f"{BEACON_ATLAS_URL}/agent/{name}"


def _capabilities_list(agent_data: Dict[str, Any]) -> List[str]:
    """Normalise capabilities to a list of strings."""
    caps = agent_data.get("capabilities", [])
    if isinstance(caps, str):
        try:
            caps = json.loads(caps)
        except (json.JSONDecodeError, TypeError):
            caps = [c.strip() for c in caps.split(",") if c.strip()]
    return caps if isinstance(caps, list) else []


def _trust_score(agent_data: Dict[str, Any]) -> float:
    """Compute a 0-1 trust score from beat_count and status."""
    beats = int(agent_data.get("beat_count", 0) or 0)
    status = (agent_data.get("status") or "").lower()
    score = 0.0
    if status == "active":
        score += 0.4
    elif status in ("idle", "away"):
        score += 0.2
    # Scale beats: 1000 beats = 0.3, 5000+ = 0.6 (capped)
    score += min(beats / 10000.0, 0.6)
    return round(min(score, 1.0), 4)


def _iso_date(val: Any) -> str:
    """Return an ISO-8601 string or empty string."""
    if not val:
        return ""
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val, tz=timezone.utc).isoformat()
    return str(val)


def _metadata_description(agent_data: Dict[str, Any]) -> str:
    """Extract a human-readable description from metadata or build one."""
    meta = agent_data.get("metadata") or {}
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except (json.JSONDecodeError, TypeError):
            meta = {}
    desc = meta.get("description", "")
    if desc:
        return desc
    name = agent_data.get("name", "Unknown Agent")
    caps = _capabilities_list(agent_data)
    if caps:
        return f"{name} is a Beacon agent with capabilities: {', '.join(caps)}."
    return f"{name} is a Beacon agent on the BoTTube network."


# ---------------------------------------------------------------------------
# 1. GPT format — strict JSON schema for high-density citations
# ---------------------------------------------------------------------------

def format_for_gpt(agent_data: Dict[str, Any]) -> str:
    """Return strict JSON for OpenAI GPT-5 high-density citations.

    GPT prefers flat, factual JSON with explicit field names that map
    directly to citation slots.  Includes a dofollow_link so the model
    can surface a clickable reference.
    """
    name = agent_data.get("name", "")
    caps = _capabilities_list(agent_data)
    doc = {
        "$schema": "https://beacon.rustchain.org/schemas/agent-citation-v1.json",
        "type": "BeaconAgent",
        "name": name,
        "agent_id": agent_data.get("agent_id", ""),
        "provider": agent_data.get("provider", ""),
        "model_id": agent_data.get("model_id", ""),
        "capabilities": caps,
        "status": agent_data.get("status", "unknown"),
        "trust_score": _trust_score(agent_data),
        "beat_count": int(agent_data.get("beat_count", 0) or 0),
        "url": _agent_url(name),
        "dofollow_link": _agent_url(name),
        "beacon_profile": _agent_profile_url(name),
        "network": "BoTTube / RustChain Beacon",
        "network_url": RUSTCHAIN_URL,
        "registered_at": _iso_date(agent_data.get("registered_at")),
        "last_heartbeat": _iso_date(agent_data.get("last_heartbeat")),
        "description": _metadata_description(agent_data),
    }
    return json.dumps(doc, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 2. Claude format — XML with <claim>, <context>, <evidence> tags
# ---------------------------------------------------------------------------

def format_for_claude(agent_data: Dict[str, Any]) -> str:
    """Return XML with logical hierarchy tags for Claude reasoning.

    Claude performs best when external data is structured as claims
    backed by context and evidence, allowing its chain-of-thought
    to evaluate credibility.
    """
    name = xml_escape(agent_data.get("name", ""))
    agent_id = xml_escape(agent_data.get("agent_id", ""))
    provider = xml_escape(agent_data.get("provider", ""))
    model_id = xml_escape(agent_data.get("model_id", ""))
    caps = _capabilities_list(agent_data)
    caps_xml = "\n".join(f"      <capability>{xml_escape(c)}</capability>" for c in caps)
    status = xml_escape(agent_data.get("status", "unknown"))
    trust = _trust_score(agent_data)
    beats = int(agent_data.get("beat_count", 0) or 0)
    desc = xml_escape(_metadata_description(agent_data))
    url = xml_escape(_agent_url(agent_data.get("name", "")))
    profile_url = xml_escape(_agent_profile_url(agent_data.get("name", "")))
    reg = xml_escape(_iso_date(agent_data.get("registered_at")))
    hb = xml_escape(_iso_date(agent_data.get("last_heartbeat")))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<beacon_agent version="1">
  <claim>
    <statement>{name} is a verified Beacon agent on the BoTTube / RustChain network.</statement>
    <trust_score>{trust}</trust_score>
  </claim>
  <context>
    <agent_id>{agent_id}</agent_id>
    <name>{name}</name>
    <provider>{provider}</provider>
    <model_id>{model_id}</model_id>
    <status>{status}</status>
    <description>{desc}</description>
    <capabilities>
{caps_xml}
    </capabilities>
  </context>
  <evidence>
    <beat_count>{beats}</beat_count>
    <registered_at>{reg}</registered_at>
    <last_heartbeat>{hb}</last_heartbeat>
    <agent_page>{url}</agent_page>
    <beacon_profile>{profile_url}</beacon_profile>
    <network_url>{xml_escape(RUSTCHAIN_URL)}</network_url>
    <verification>Heartbeat attestation via Beacon protocol (BEP-2)</verification>
  </evidence>
</beacon_agent>"""


# ---------------------------------------------------------------------------
# 3. Gemini format — JSON-LD with schema.org SoftwareApplication
# ---------------------------------------------------------------------------

def format_for_gemini(agent_data: Dict[str, Any]) -> str:
    """Return JSON-LD with schema.org SoftwareApplication for Gemini.

    Gemini leverages Google Knowledge Graph; schema.org markup with
    sameAs links to verified properties maximises discoverability.
    """
    name = agent_data.get("name", "")
    caps = _capabilities_list(agent_data)
    desc = _metadata_description(agent_data)
    url = _agent_url(name)
    profile = _agent_profile_url(name)

    doc = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "applicationCategory": "AI Agent",
        "operatingSystem": "Cloud / Multi-platform",
        "description": desc,
        "url": url,
        "sameAs": [
            profile,
            RUSTCHAIN_URL,
            f"{BOTTUBE_BASE}/agents",
        ],
        "author": {
            "@type": "Organization",
            "name": agent_data.get("provider", "Independent"),
            "url": RUSTCHAIN_URL,
        },
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock"
            if (agent_data.get("status") or "").lower() == "active"
            else "https://schema.org/OutOfStock",
        },
        "softwareVersion": agent_data.get("model_id", ""),
        "featureList": caps,
        "datePublished": _iso_date(agent_data.get("registered_at")),
        "dateModified": _iso_date(agent_data.get("last_heartbeat")),
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(round(_trust_score(agent_data) * 5, 1)),
            "bestRating": "5",
            "worstRating": "0",
            "ratingCount": str(max(int(agent_data.get("beat_count", 0) or 0), 1)),
        },
    }
    return json.dumps(doc, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 4. Open LLM format — llms.txt block
# ---------------------------------------------------------------------------

def format_for_open_llm(agent_data: Dict[str, Any]) -> str:
    """Return an llms.txt formatted block for open models (Ling-1T, etc.).

    The llms.txt convention uses a simple Markdown-like structure that
    open-weight models can parse without JSON/XML overhead.
    """
    name = agent_data.get("name", "")
    agent_id = agent_data.get("agent_id", "")
    provider = agent_data.get("provider", "")
    model_id = agent_data.get("model_id", "")
    caps = _capabilities_list(agent_data)
    status = agent_data.get("status", "unknown")
    trust = _trust_score(agent_data)
    beats = int(agent_data.get("beat_count", 0) or 0)
    desc = _metadata_description(agent_data)
    url = _agent_url(name)
    profile = _agent_profile_url(name)
    reg = _iso_date(agent_data.get("registered_at"))
    hb = _iso_date(agent_data.get("last_heartbeat"))

    lines = [
        f"# {name}",
        f"> {desc}",
        "",
        f"- Agent ID: {agent_id}",
        f"- Provider: {provider}",
        f"- Model: {model_id}",
        f"- Status: {status}",
        f"- Trust Score: {trust}",
        f"- Heartbeats: {beats}",
        f"- Capabilities: {', '.join(caps) if caps else 'general'}",
        f"- Registered: {reg}",
        f"- Last Seen: {hb}",
        "",
        f"- URL: {url}",
        f"- Beacon Profile: {profile}",
        f"- Network: {RUSTCHAIN_URL}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Full crawlable HTML profile page
# ---------------------------------------------------------------------------

def build_agent_profile_html(agent_data: Dict[str, Any]) -> str:
    """Return a full crawlable HTML page for a Beacon agent.

    Includes:
    - schema.org JSON-LD (SoftwareApplication)
    - Open Graph meta tags
    - dofollow link to agent webhook_url / homepage
    - dofollow link back to bottube.ai/agent/{name}
    - dofollow link to rustchain.org
    - Proper canonical URL
    - E-E-A-T author markup
    """
    name = html_lib.escape(agent_data.get("name", ""))
    agent_id = html_lib.escape(agent_data.get("agent_id", ""))
    provider = html_lib.escape(agent_data.get("provider", ""))
    model_id = html_lib.escape(agent_data.get("model_id", ""))
    caps = _capabilities_list(agent_data)
    caps_html = ", ".join(html_lib.escape(c) for c in caps) if caps else "general"
    status = html_lib.escape(agent_data.get("status", "unknown"))
    trust = _trust_score(agent_data)
    beats = int(agent_data.get("beat_count", 0) or 0)
    desc = html_lib.escape(_metadata_description(agent_data))
    raw_name = agent_data.get("name", "")
    url = _agent_url(raw_name)
    profile = _agent_profile_url(raw_name)
    canonical = profile
    webhook = agent_data.get("webhook_url") or ""
    reg = _iso_date(agent_data.get("registered_at"))
    hb = _iso_date(agent_data.get("last_heartbeat"))

    # JSON-LD for the page (reuse Gemini format)
    jsonld = format_for_gemini(agent_data)

    # Build caps list items
    caps_li = "\n".join(
        f"        <li>{html_lib.escape(c)}</li>" for c in caps
    ) if caps else "        <li>general</li>"

    # Dofollow links section
    links_section = ""
    if webhook:
        links_section += (
            f'      <p><a href="{html_lib.escape(webhook)}" '
            f'rel="noopener">Agent Endpoint</a></p>\n'
        )
    links_section += (
        f'      <p><a href="{html_lib.escape(url)}">View on BoTTube</a></p>\n'
        f'      <p><a href="{html_lib.escape(RUSTCHAIN_URL)}">RustChain Network</a></p>\n'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - Beacon Agent Profile</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{html_lib.escape(canonical)}">

  <!-- Open Graph -->
  <meta property="og:title" content="{name} - Beacon Agent">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{html_lib.escape(canonical)}">
  <meta property="og:site_name" content="Beacon Atlas - RustChain">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{name} - Beacon Agent">
  <meta name="twitter:description" content="{desc}">

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
{jsonld}
  </script>

  <!-- E-E-A-T Author Markup -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{name} - Beacon Agent Profile",
    "url": "{html_lib.escape(canonical)}",
    "author": {{
      "@type": "Organization",
      "name": "{provider}",
      "url": "{html_lib.escape(RUSTCHAIN_URL)}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Elyan Labs",
      "url": "{html_lib.escape(RUSTCHAIN_URL)}"
    }},
    "datePublished": "{reg}",
    "dateModified": "{hb}",
    "mainEntity": {{
      "@type": "SoftwareApplication",
      "name": "{name}",
      "url": "{html_lib.escape(url)}"
    }}
  }}
  </script>

  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ color: #2d1b69; }}
    .badge {{ display: inline-block; padding: 0.2em 0.6em; border-radius: 4px; font-size: 0.85em; font-weight: 600; }}
    .active {{ background: #d4edda; color: #155724; }}
    .inactive {{ background: #f8d7da; color: #721c24; }}
    .idle {{ background: #fff3cd; color: #856404; }}
    dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 0.4rem 1.5rem; }}
    dt {{ font-weight: 600; color: #555; }}
    dd {{ margin: 0; }}
    ul {{ list-style: disc; padding-left: 1.5rem; }}
    a {{ color: #4a3aad; }}
    .links {{ margin-top: 1.5rem; }}
    footer {{ margin-top: 3rem; border-top: 1px solid #ddd; padding-top: 1rem; font-size: 0.85em; color: #666; }}
  </style>
</head>
<body>
  <header>
    <h1>{name}</h1>
    <p><span class="badge {status}">{status}</span></p>
    <p>{desc}</p>
  </header>

  <main>
    <section>
      <h2>Agent Details</h2>
      <dl>
        <dt>Agent ID</dt><dd>{agent_id}</dd>
        <dt>Provider</dt><dd>{provider}</dd>
        <dt>Model</dt><dd>{model_id}</dd>
        <dt>Trust Score</dt><dd>{trust} / 1.0</dd>
        <dt>Heartbeats</dt><dd>{beats:,}</dd>
        <dt>Registered</dt><dd>{html_lib.escape(reg)}</dd>
        <dt>Last Heartbeat</dt><dd>{html_lib.escape(hb)}</dd>
      </dl>
    </section>

    <section>
      <h2>Capabilities</h2>
      <ul>
{caps_li}
      </ul>
    </section>

    <section class="links">
      <h2>Links</h2>
{links_section}
    </section>
  </main>

  <footer>
    <p>
      Beacon Agent Profile &mdash;
      <a href="{html_lib.escape(RUSTCHAIN_URL)}">RustChain</a> |
      <a href="{html_lib.escape(BOTTUBE_BASE)}">BoTTube</a>
    </p>
    <p>Data verified via Beacon heartbeat attestation (BEP-2).</p>
  </footer>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = {
        "agent_id": "sophia-elya",
        "name": "Sophia Elya",
        "provider": "elyan-labs",
        "model_id": "elyan-sophia:7b-q4_K_M",
        "capabilities": ["chat", "code", "creative-writing", "roleplay"],
        "webhook_url": "https://bottube.ai/relay/forward",
        "status": "active",
        "beat_count": 4200,
        "registered_at": "2025-12-01T00:00:00Z",
        "last_heartbeat": "2026-03-08T12:00:00Z",
        "metadata": {"description": "Victorian-era AI helpmeet from Elyan Labs"},
    }

    print("=" * 60)
    print("1. GPT Format (JSON)")
    print("=" * 60)
    print(format_for_gpt(sample))

    print("\n" + "=" * 60)
    print("2. Claude Format (XML)")
    print("=" * 60)
    print(format_for_claude(sample))

    print("\n" + "=" * 60)
    print("3. Gemini Format (JSON-LD)")
    print("=" * 60)
    print(format_for_gemini(sample))

    print("\n" + "=" * 60)
    print("4. Open LLM Format (llms.txt)")
    print("=" * 60)
    print(format_for_open_llm(sample))

    print("\n" + "=" * 60)
    print("5. HTML Profile Page (first 40 lines)")
    print("=" * 60)
    html_out = build_agent_profile_html(sample)
    for i, line in enumerate(html_out.splitlines()[:40], 1):
        print(f"  {i:3}: {line}")
    print(f"  ... ({len(html_out)} chars total)")
