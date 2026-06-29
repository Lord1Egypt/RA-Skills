#!/usr/bin/env python3
"""
auto-populate-models.py — Auto-populate orchestrator model inventory
from OpenClaw's own gateway configuration.

Reads `~/.openclaw/openclaw.json` and extracts all configured model
entries (IDs, names, providers, context windows, costs, aliases).
Merges into orchestrator-data/models.json, preserving all manually-curated
fields (tier, speed_rating, capabilities, notes, research).

Usage:
  python3 scripts/auto-populate-models.py [--dry-run] [--verbose]

Silent on cron — no stdin prompts. Manual edits go through the dashboard WebUI.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get(
    "ORCHESTRATOR_DATA_DIR",
    SKILL_DIR.parent.parent / "orchestrator-data"
))
MODELS_FILE = DATA_DIR / "models.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

VERBOSE = "--verbose" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

# ── Helpers ────────────────────────────────────────────────────

def log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"info": "  •", "ok": "  ✅", "warn": "  ⚠️", "err": "  ❌"}
    p = prefix.get(level, "  •")
    label = "[DRY-RUN] " if DRY_RUN else ""
    if level == "info" and not VERBOSE:
        return
    print(f"{ts} {p} {label}{msg}")


def get_model_id_with_provider(provider_id, model_id):
    """Construct the canonical model ID used in orchestrator routing.
    
    Provider models are referenced as <provider>/<model_id> in the routing config.
    Some built-in providers (openrouter, opencode-go) already include their
    provider prefix in the model ID.
    """
    if "/" in model_id:
        # Already has a provider prefix (e.g. openrouter/free)
        return model_id
    return f"{provider_id}/{model_id}"


# ═══════════════════════════════════════════════════════════════
#  CONFIG PARSER
# ═══════════════════════════════════════════════════════════════

def parse_config():
    """Read OpenClaw config and extract model definitions.
    
    Returns:
        models_by_id: dict of model_id -> model metadata dict
            Sources consulted in priority order:
            1. models.providers.<provider>.models — full definitions
            2. agents.defaults.models — routing registry with aliases
            3. agents.defaults.model.{primary, fallbacks} — active routing
            4. agents.list[] agent-specific model configs
    """
    if not OPENCLAW_CONFIG.exists():
        log(f"Config not found: {OPENCLAW_CONFIG}", "err")
        sys.exit(1)

    with open(OPENCLAW_CONFIG) as f:
        cfg = json.load(f)

    models_by_id = {}

    # ── Source 1: Provider-defined models ──
    providers = cfg.get("models", {}).get("providers", {})
    for prov_id, prov_cfg in providers.items():
        for m in prov_cfg.get("models", []):
            mid = get_model_id_with_provider(prov_id, m["id"])
            cost = m.get("cost", {})
            models_by_id[mid] = {
                "id": mid,
                "provider": prov_id,
                "name": m.get("name", m["id"]),
                "context_window": m.get("contextWindow", 0),
                "max_tokens": m.get("maxTokens", 0),
                "input_types": m.get("input", []),
                "has_vision": "image" in m.get("input", []),
                "has_reasoning": m.get("reasoning", False),
                "cost_input": cost.get("input", 0),
                "cost_output": cost.get("output", 0),
                "cost_cache_read": cost.get("cacheRead", 0),
                "cost_cache_write": cost.get("cacheWrite", 0),
                "source": "provider_definition",
                "base_url": prov_cfg.get("baseUrl", ""),
            }

    # ── Source 2: agents.defaults.models (routing registry with aliases) ──
    routed_models = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    for mid, mcfg in routed_models.items():
        alias = mcfg.get("alias", "")
        if mid not in models_by_id:
            # New model from built-in/cloud provider — no provider definition
            provider = mid.split("/")[0] if "/" in mid else "unknown"
            models_by_id[mid] = {
                "id": mid,
                "provider": provider,
                "name": alias or mid.split("/")[-1],
                "context_window": 0,
                "max_tokens": 0,
                "input_types": [],
                "has_vision": False,
                "has_reasoning": False,
                "cost_input": 0,
                "cost_output": 0,
                "source": "routing_registry",
            }
        else:
            # Ensure name is set from alias if we have one
            if alias and not models_by_id[mid].get("name"):
                models_by_id[mid]["name"] = alias
            elif alias:
                models_by_id[mid]["alias"] = alias

    # ── Source 3: agents.defaults.model primary + fallbacks ──
    model_cfg = cfg.get("agents", {}).get("defaults", {}).get("model", {})
    primary = model_cfg.get("primary", "")
    fallbacks = model_cfg.get("fallbacks", [])
    all_active = set()
    if primary:
        all_active.add(primary)
    all_active.update(fallbacks)

    for mid in all_active:
        if mid not in models_by_id:
            provider = mid.split("/")[0] if "/" in mid else "unknown"
            models_by_id[mid] = {
                "id": mid,
                "provider": provider,
                "name": mid.split("/")[-1],
                "context_window": 0,
                "max_tokens": 0,
                "source": "fallback_chain",
            }

    # ── Source 4: Agent-specific models ──
    for agent in cfg.get("agents", {}).get("list", []):
        am = agent.get("model", {})
        agent_primary = am.get("primary", "")
        agent_fallbacks = am.get("fallbacks", [])
        agent_models = am.get("models", {})
        all_agent = set()
        if agent_primary:
            all_agent.add(agent_primary)
        all_agent.update(agent_fallbacks)
        all_agent.update(agent_models.keys())

        for mid in all_agent:
            if mid not in models_by_id:
                provider = mid.split("/")[0] if "/" in mid else "unknown"
                models_by_id[mid] = {
                    "id": mid,
                    "provider": provider,
                    "name": mid.split("/")[-1],
                    "context_window": 0,
                    "max_tokens": 0,
                    "source": "agent_specific",
                }

    log(f"Parsed OpenClaw config: {len(models_by_id)} unique model IDs", "ok")
    return models_by_id


# ═══════════════════════════════════════════════════════════════
#  MODEL BUILDER
# ═══════════════════════════════════════════════════════════════

def build_orchestrator_model(mid, info, existing):
    """Convert a raw config model entry to orchestrator models.json format.
    
    Preserves existing manual data (tier, speed_rating, capabilities, etc.)
    and only overwrites auto-discoverable fields.
    """
    old = next((e for e in existing if e["id"] == mid), None)

    # Determine cost type
    if info.get("cost_input", -1) == 0 and info.get("cost_output", -1) == 0:
        cost_type = "local_free"
        cost_amount = 0
        cost_period = "unlimited"
        cost_limits = "Local — no rate limits"
    elif info.get("source") in ("routing_registry", "fallback_chain"):
        cost_type = "unknown"
        cost_amount = 0
        cost_period = "per_token"
        cost_limits = "Auto-discovered — verify pricing"
    else:
        cost_type = "pay_per_token"
        cost_amount = min(info.get("cost_input", 0), info.get("cost_output", 0)) or 0
        cost_period = "per_token"
        cost_limits = "From gateway config"

    entry = {
        "id": mid,
        "provider": info.get("provider", "unknown"),
        "name": info.get("name", mid.split("/")[-1]),
        "tier": 0,
        "capabilities": {
            "reasoning": 0,
            "coding": 0,
            "creative": 0,
            "vision": info.get("has_vision", False),
            "tool_calls": True,
            "thinking": info.get("has_reasoning", False),
        },
        "speed_rating": 0,
        "cost": {
            "type": cost_type,
            "amount": cost_amount,
            "period": cost_period,
            "limits": cost_limits,
            "last_checked": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "source_url": info.get("base_url", ""),
        },
        "status": "active" if old and old.get("status") in ("active", "discovered") else "discovered",
        "agent_ready": old.get("agent_ready", False) if old else False,
        "architecture": old.get("architecture", "") if old else "",
        "context_window": info.get("context_window", 0),
        "notes": old.get("notes", "Auto-populated from OpenClaw config.") if old else "Auto-populated from OpenClaw config. Needs manual review.",
        "catalogued_by": old.get("catalogued_by", "auto_populate") if old else "auto_populate",
        "last_tested": old.get("last_tested", "") if old else "",
    }

    if old:
        # Preserve manual ratings
        PRESERVED = ["tier", "speed_rating", "user_notes", "research_notes", "research_sources"]
        for field in PRESERVED:
            if field in old and old.get(field) not in (None, "", 0):
                entry[field] = old[field]
        # Preserve capabilities that were manually set
        if old.get("capabilities"):
            for k in ("reasoning", "coding", "creative"):
                if old["capabilities"].get(k, 0) > 0:
                    entry["capabilities"][k] = old["capabilities"][k]

    return entry


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Model Auto-Population Engine                          ║")
    print("║   Reads: OpenClaw gateway config (openclaw.json)        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    log(f"Config:   {OPENCLAW_CONFIG}")
    log(f"Data dir: {DATA_DIR}")
    log(f"Models:   {MODELS_FILE}")
    print()

    # ── Load existing orchestrator catalog ──
    existing = []
    if MODELS_FILE.exists():
        try:
            with open(MODELS_FILE) as f:
                existing = json.load(f).get("models", [])
            log(f"Existing catalog: {len(existing)} models", "ok")
        except (json.JSONDecodeError, KeyError) as e:
            log(f"Corrupt {MODELS_FILE}: {e}", "err")
            log("Starting fresh", "warn")
    else:
        log("No existing catalog — starting fresh", "warn")

    # ── Parse OpenClaw config ──
    config_models = parse_config()

    # ── Build entries ──
    seen_config = set(config_models.keys())
    
    # 1) Models from OpenClaw config → build/merge (preserves manual ratings)
    config_entries = []
    for mid in sorted(seen_config):
        info = config_models[mid]
        entry = build_orchestrator_model(mid, info, existing)
        config_entries.append(entry)
    
    # 2) Existing models NOT in config → keep as-is (don't drop manual data)
    orphan_entries = [m for m in existing if m["id"] not in seen_config]
    
    # Combine: config models first, then orphans
    new_catalog = config_entries + orphan_entries
    
    # ── Stats ──
    previously_existed = {m["id"] for m in existing}
    newly = [m for m in config_entries if m["id"] not in previously_existed]

    print()
    log(f"Results:", "info")
    log(f"  Total in catalog:     {len(new_catalog)}", "ok")
    log(f"  From OpenClaw config: {len(seen_config)}", "ok")
    log(f"  New/discovered:       {len(newly)}", "warn")
    log(f"  Orphans (preserved):  {len(orphan_entries)}", "info")

    if orphan_entries and VERBOSE:
        log("Models preserved from existing catalog (not in gateway config):", "info")
        for m in orphan_entries:
            log(f"  {m['id']}", "info")

    # ── Write ──
    if DRY_RUN:
        print()
        log("DRY RUN — no changes written", "warn")
        return True

    output = {
        "version": "1.0",
        "schema": "orchestrator-models-v1",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "description": "Model inventory — auto-populated from OpenClaw config. Manually curated via dashboard WebUI.",
        "models": new_catalog,
    }

    tmp_file = MODELS_FILE.with_suffix(".json.tmp")
    try:
        with open(tmp_file, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        tmp_file.replace(MODELS_FILE)
        log(f"Written {len(new_catalog)} models → {MODELS_FILE}", "ok")
    except OSError as e:
        log(f"Write failed: {e}", "err")
        return False

    print()
    log("Auto-population complete.", "ok")
    log("Edit ratings/tiers/notes via dashboard: http://localhost:8766", "info")
    print()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
