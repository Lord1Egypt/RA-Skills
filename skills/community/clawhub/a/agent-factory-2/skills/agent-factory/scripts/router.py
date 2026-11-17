#!/usr/bin/env python3
"""
Advanced Dynamic Semantic & Canary Router for OpenClaw.
Features:
1. Instantaneous Semantic Cache Lookup (>0.98 similarity -> 0 tokens)
2. Cryptographic Manifest Integrity Verification
3. Canary Deployment (traffic splitting)
4. Security Sandbox & Circuit Breaker Enforcement
"""

import json
import os
import random
from typing import Dict, Any, Optional, List
from semantic_cache import lookup as cache_lookup, store as cache_store, get_embedding, _cosine_similarity
from crypto_signer import verify_manifest
from security_sandbox import SecuritySandbox
from alerts import dispatch_alert

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")
sandbox = SecuritySandbox()


def list_active_agents() -> List[Dict[str, Any]]:
    """Scans agents directory and loads active manifest configurations."""
    active_agents = []
    if not os.path.exists(AGENTS_DIR):
        return []

    for agent_dir in os.listdir(AGENTS_DIR):
        agent_path = os.path.join(AGENTS_DIR, agent_dir)
        if not os.path.isdir(agent_path):
            continue
        for v in os.listdir(agent_path):
            v_path = os.path.join(agent_path, v)
            manifest_file = os.path.join(v_path, "manifest.json")
            if os.path.isfile(manifest_file):
                # Verify manifest signature if available
                sig_valid, msg = verify_manifest(manifest_file)
                # If sig file exists and invalid, skip for security
                if os.path.exists(manifest_file + ".sig") and not sig_valid:
                    print(f"⚠️ Alerte sécurité : Manifeste corrompu ou falsifié ignoré pour {agent_dir}/{v}")
                    continue

                with open(manifest_file, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    if manifest.get("status") in ["active", "canary"]:
                        manifest["_file_path"] = manifest_file
                        active_agents.append(manifest)
    return active_agents


def route_and_execute(prompt: str) -> Dict[str, Any]:
    """
    Full routing workflow:
    1. Check Semantic Cache (0-token fast path)
    2. Compute Embedding & match active/canary sub-agents
    3. Check Circuit Breaker & Rate limits
    4. Perform Canary routing or Generalist fallback
    """
    # 1. Semantic Cache check
    cached = cache_lookup(prompt)
    if cached:
        return {
            "source": "SEMANTIC_CACHE",
            "tokens_consumed": 0,
            "latency_ms": 1.2,
            "served_by": cached["served_by_agent"],
            "cache_similarity": cached["hit_similarity"],
            "result": cached["response"]
        }

    # 2. Vector Matching
    prompt_vector = get_embedding(prompt)
    active_agents = list_active_agents()

    best_match: Optional[Dict[str, Any]] = None
    best_sim: float = -1.0

    for agent in active_agents:
        routing = agent.get("routing_config", {})
        centroid = routing.get("centroid_vector", [])
        radius = routing.get("confidence_radius", 0.3)

        # Pad vector if needed
        if len(centroid) < len(prompt_vector):
            centroid = centroid + [0.0] * (len(prompt_vector) - len(centroid))
        elif len(centroid) > len(prompt_vector):
            prompt_vector = prompt_vector + [0.0] * (len(centroid) - len(prompt_vector))

        sim = _cosine_similarity(prompt_vector, centroid)
        if sim > best_sim:
            best_sim = sim
            if (1.0 - sim) <= radius:
                best_match = agent

    # 3. Decision & Sandbox Circuit Check
    if best_match:
        agent_id = best_match["agent_id"]
        status = best_match.get("status", "active")

        # Canary Traffic Split: if canary, route 25% to subagent, 75% to generalist
        if status == "canary" and random.random() > 0.25:
            return {
                "source": "GENERALIST_ORCHESTRATOR",
                "canary_holdback": True,
                "reason": "Canary traffic split testing",
                "target_canary_agent": agent_id
            }

        # Check Circuit Breaker
        allowed, reason = sandbox.check_and_record(agent_id, estimated_tokens=400)
        if not allowed:
            dispatch_alert("CIRCUIT_BREAKER", f"Circuit Breaker déclenché pour {agent_id}", reason, "WARNING")
            return {
                "source": "GENERALIST_ORCHESTRATOR",
                "fallback_reason": f"Circuit breaker tripped: {reason}",
                "target_agent": agent_id
            }

        # Simulated specialized execution
        simulated_response = {
            "status": "success",
            "domain": best_match["target_domain"],
            "output": f"Processed by specialized {agent_id} ({best_match['version']})",
            "tokens_used": 350
        }
        sandbox.record_success(agent_id)

        # Store in semantic cache for future exact/near-exact hits
        cache_store(prompt, simulated_response, agent_id)

        return {
            "source": "SPECIALIZED_SUBAGENT",
            "agent_id": agent_id,
            "version": best_match["version"],
            "similarity_score": round(best_sim, 4),
            "tokens_consumed": simulated_response["tokens_used"],
            "allowed_tools": best_match.get("allowed_tools", []),
            "result": simulated_response
        }

    # Fallback to Generalist
    return {
        "source": "GENERALIST_ORCHESTRATOR",
        "agent_id": "orchestrator_core",
        "reason": "No sub-agent within confidence radius",
        "best_similarity": round(best_sim, 4),
        "tokens_consumed": 1400
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advanced Router")
    parser.add_argument("--prompt", type=str, required=True, help="Task prompt")
    args = parser.parse_args()

    res = route_and_execute(args.prompt)
    print("\n🧭 --- Semantic & Canary Routing Result ---")
    print(json.dumps(res, indent=2))
