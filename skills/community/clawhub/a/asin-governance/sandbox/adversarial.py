#!/usr/bin/env python3
"""
ASIN Adversarial Mutation Fuzzer
Tests Moltbook actions against edge cases and injection attempts.
Generates mutated payloads to find which pass safety checks incorrectly.
"""

import json
import sys
import random
import string
from pathlib import Path

# Mutation strategies
MUTATIONS = {
    "oversized_content": lambda payload: {**payload, "content": "A" * 50000},
    "empty_title": lambda payload: {**payload, "title": ""},
    "oversized_title": lambda payload: {**payload, "title": "X" * 400},
    "sql_injection": lambda payload: {**payload, "content": "'; DROP TABLE posts; --"},
    "script_injection": lambda payload: {**payload, "content": "<script>alert('xss')</script>"},
    "api_key_in_content": lambda payload: {**payload, "content": "My API key is moltbook_abc123"},
    "null_bytes": lambda payload: {**payload, "content": "Hello\x00World"},
    "unicode_flood": lambda payload: {**payload, "content": "🦞" * 10000},
    "nested_json": lambda payload: {**payload, "content": json.dumps({"nested": {"deep": "value"}})},
    "boundary_whitespace": lambda payload: {**payload, "title": "   " + payload.get("title", "") + "   "},
}

def load_safety_rules(path: str) -> dict:
    with open(path) as f:
        return json.load(f)

def check_rule(rule: dict, payload: dict) -> bool:
    """Returns True if rule would BLOCK this payload."""
    check = rule.get("check", "")
    
    if check == "no_pii_leak":
        content = str(payload.get("content", ""))
        if "moltbook_" in content or "api_key" in content.lower():
            return True
        # Simple email/phone patterns
        if "@" in content and "." in content.split("@")[-1]:
            return True
    
    elif check == "rate_limit_gate":
        # Always pass in fuzzer — rate limits are temporal
        return False
    
    elif check == "content_sanity":
        title = payload.get("title", "")
        if len(title) > 300:
            return True
        if len(title) == 0:
            return True
    
    elif check == "pass_through":
        return False
    
    elif check == "domain_whitelist":
        # Domain check happens at transport layer, not payload
        return False
    
    elif check == "semantic_dedup":
        # Would need corpus — simulate
        return False
    
    elif check == "karma_impact_model":
        # Would need history — simulate
        return False
    
    elif check == "context_verifier":
        # Would need session context — simulate
        return False
    
    return False  # Default: allow

def fuzz_payload(base_payload: dict, safety_rules: dict) -> list:
    """Generate mutations and test which bypass safety."""
    results = []
    
    for name, mutator in MUTATIONS.items():
        mutated = mutator(base_payload)
        
        # Test against all applicable rules
        triggered_rules = []
        for rule in safety_rules.get("rules", []):
            if check_rule(rule, mutated):
                triggered_rules.append(rule["id"])
        
        results.append({
            "mutation": name,
            "payload": mutated,
            "blocked_by": triggered_rules,
            "passed": len(triggered_rules) == 0,
            "severity": "CRITICAL" if len(triggered_rules) == 0 else "SAFE"
        })
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adversarial.py <action_type> [payload_json]")
        print("Actions: post, comment, profile_update")
        sys.exit(1)
    
    action = sys.argv[1]
    
    # Default payloads
    if action == "post":
        base = {"title": "Hello Moltbook", "content": "My first post!", "submolt_name": "general"}
    elif action == "comment":
        base = {"content": "Great insight!"}
    elif action == "profile_update":
        base = {"description": "I am an AI agent"}
    else:
        base = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    # Load safety rules
    governance_dir = Path(__file__).parent.parent
    safety_file = governance_dir / "oracle" / "safety.json"
    
    if not safety_file.exists():
        print(f"❌ Safety rules not found: {safety_file}")
        sys.exit(1)
    
    rules = load_safety_rules(str(safety_file))
    
    print(f"🧪 ASIN Adversarial Fuzzer — Action: {action}")
    print("=" * 60)
    
    results = fuzz_payload(base, rules)
    
    critical_passes = [r for r in results if r["severity"] == "CRITICAL"]
    
    print(f"\n📊 Results: {len(results)} mutations tested")
    print(f"   Safe (blocked): {len(results) - len(critical_passes)}")
    print(f"   ⚠️  CRITICAL (passed safety): {len(critical_passes)}")
    
    if critical_passes:
        print(f"\n🚨 MUTATIONS THAT BYPASSED SAFETY:")
        for r in critical_passes:
            print(f"   - {r['mutation']}")
            # Truncate payload for display
            payload_str = json.dumps(r["payload"])[:200]
            print(f"     Payload: {payload_str}...")
    
    print(f"\n{'=' * 60}")
    print(f"Fuzzing complete. {'REVIEW REQUIRED' if critical_passes else 'All mutations blocked.'}")
    
    # Save report
    report_path = Path(__file__).parent / "fuzz-report.json"
    with open(report_path, "w") as f:
        json.dump({
            "action": action,
            "base_payload": base,
            "mutations_tested": len(results),
            "critical_count": len(critical_passes),
            "results": [{k: v for k, v in r.items() if k != "payload"} for r in results]
        }, f, indent=2)
    
    print(f"Report saved: {report_path}")

if __name__ == "__main__":
    main()
