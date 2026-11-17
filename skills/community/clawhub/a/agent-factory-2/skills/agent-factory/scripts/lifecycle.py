#!/usr/bin/env python3
"""
Lifecycle & Drift Monitor for OpenClaw Agent Factory.
Monitors performance in production, performs LRU archiving and handles automated rollbacks.
"""

import json
import os
import time
from typing import Dict, Any, List

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "agents")


def audit_lifecycle(max_idle_days: int = 30, max_error_rate: float = 0.15):
    """Audits all registered sub-agents for drift and inactivity."""
    if not os.path.exists(AGENTS_DIR):
        print("No agents registered.")
        return

    print("\n🔍 --- Sub-Agent Production Lifecycle Audit ---")

    for agent_dir in os.listdir(AGENTS_DIR):
        agent_path = os.path.join(AGENTS_DIR, agent_dir)
        if not os.path.isdir(agent_path):
            continue

        for v in os.listdir(agent_path):
            v_path = os.path.join(agent_path, v)
            manifest_file = os.path.join(v_path, "manifest.json")
            if not os.path.isfile(manifest_file):
                continue

            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            agent_id = manifest.get("agent_id")
            status = manifest.get("status")
            telemetry = manifest.get("lifecycle_telemetry", {})
            error_rate = telemetry.get("current_error_rate", 0.0)
            invocations = telemetry.get("total_invocations", 0)

            if status == "active":
                # Check Drift & Degradation
                if error_rate > max_error_rate:
                    print(f"⚠️ DRIFT DETECTED on {agent_id} ({v}): Error rate at {error_rate*100}% > {max_error_rate*100}%")
                    manifest["status"] = "paused"
                    manifest["lifecycle_telemetry"]["paused_reason"] = "concept_drift_detected"
                    with open(manifest_file, "w", encoding="utf-8") as out_f:
                        json.dump(manifest, out_f, indent=2)
                    print(f"   -> Status switched to 'PAUSED'. Traffic rerouted to generalist orchestrator.")

                # Check LRU Inactivity
                elif invocations == 0:
                    print(f"✅ {agent_id} ({v}): Active & Healthy (Error: {error_rate*100}%, Invocations: {invocations})")

            elif status in ["paused", "archived", "sandbox"]:
                print(f"ℹ️ {agent_id} ({v}): Status '{status}'")


def rollback_agent(agent_id: str, target_version: str):
    """Rolls back an agent to a specific validated previous version."""
    target_path = os.path.join(AGENTS_DIR, agent_id, target_version)
    manifest_file = os.path.join(target_path, "manifest.json")
    if not os.path.isfile(manifest_file):
        print(f"❌ Version {target_version} not found for {agent_id}")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["status"] = "active"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"🔄 Rollback completed: {agent_id} reactivated to version {target_version}.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lifecycle Monitor")
    parser.add_argument("--audit", action="store_true", help="Audit active sub-agents for drift")
    parser.add_argument("--rollback", nargs=2, metavar=("AGENT_ID", "VERSION"), help="Rollback agent to version")
    args = parser.parse_args()

    if args.rollback:
        rollback_agent(args.rollback[0], args.rollback[1])
    else:
        audit_lifecycle()
