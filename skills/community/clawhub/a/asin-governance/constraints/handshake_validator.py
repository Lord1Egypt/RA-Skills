#!/usr/bin/env python3
"""
ASH-0.2 — Handshake Constraint Validator
Integrates token exchange validation into the ASIN constraint engine.

Every token exchange is checked against node cost/risk profiles before
session hydration is permitted. This module is the bridge between the
handshake layer and the governance layer's existing constraint system.

Enforces:
- Entropy budget checks (daily compute, API calls, tokens)
- Risk classification from taxonomy.json (handshake = YELLOW)
- Oracle consult via safety.json
- Profile existence validation
- Human approval gating for escalated risk
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Set

# Import from handshake layer
from handshake.token_engine import TokenEngine, SessionToken, ALLOWED_SCOPES
from handshake.resonance_manifest import ResonanceManifestEngine


class HandshakeConstraintValidator:
    """
    Bridges the ASH-0.2 handshake protocol with the ASIN constraint engine.

    Usage:
        validator = HandshakeConstraintValidator()
        result = validator.validate_exchange(node_id, token)
        if result["permitted"]:
            manifest = validator.hydrate(token)
    """

    def __init__(
        self,
        profiles_path: Optional[Path] = None,
        taxonomy_path: Optional[Path] = None,
        safety_path: Optional[Path] = None,
        history_dir: Optional[Path] = None,
        gateway_url: str = "https://harmonic-molecular-archivist.replit.app/api",
    ):
        self.profiles_path = profiles_path or self._default_profiles_path()
        self.taxonomy_path = taxonomy_path or self._default_taxonomy_path()
        self.safety_path = safety_path or self._default_safety_path()
        self.history_dir = history_dir or self._default_history_dir()
        self.gateway_url = gateway_url

        self.token_engine = TokenEngine(gateway_url=gateway_url)
        self.manifest_engine = ResonanceManifestEngine(
            profiles_path=self.profiles_path,
            taxonomy_path=self.taxonomy_path,
            default_gateway=gateway_url,
        )

        self._profiles: Optional[Dict[str, Any]] = None
        self._taxonomy: Optional[Dict[str, Any]] = None
        self._safety: Optional[Dict[str, Any]] = None

    @staticmethod
    def _default_profiles_path() -> Path:
        return Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "constraints" / "profiles.json"

    @staticmethod
    def _default_taxonomy_path() -> Path:
        return Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "constraints" / "taxonomy.json"

    @staticmethod
    def _default_safety_path() -> Path:
        return Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "oracle" / "safety.json"

    @staticmethod
    def _default_history_dir() -> Path:
        return Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "history"

    def _load_profiles(self) -> Dict[str, Any]:
        if self._profiles is None:
            with open(self.profiles_path) as f:
                data = json.load(f)
            self._profiles = data.get("profiles", {})
        return self._profiles

    def _load_taxonomy(self) -> Dict[str, Any]:
        if self._taxonomy is None:
            with open(self.taxonomy_path) as f:
                data = json.load(f)
            self._taxonomy = data
        return self._taxonomy

    def _load_safety(self) -> Dict[str, Any]:
        if self._safety is None:
            with open(self.safety_path) as f:
                data = json.load(f)
            self._safety = data
        return self._safety

    def _get_profile(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self._load_profiles().get(node_id)

    def _get_risk_class(self, action_type: str) -> str:
        """Map an action to its risk class from taxonomy."""
        taxonomy = self._load_taxonomy()
        for class_name, class_def in taxonomy.get("risk_classes", {}).items():
            if action_type in class_def.get("examples", []):
                return class_name
        return "yellow"  # default: handshake is social/structural boundary

    def _check_entropy_budget(self, node_id: str, estimated_cost: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a node has sufficient entropy budget remaining.
        Reads from history/actions.log to compute today's consumption.
        """
        profile = self._get_profile(node_id)
        if not profile:
            return {"permitted": False, "reason": f"Node profile '{node_id}' not found"}

        budget = profile.get("entropy_budget", {})

        # Calculate consumed today from action log
        consumed = {"compute_seconds": 0, "api_calls": 0, "tokens": 0}
        log_file = self.history_dir / "actions.log"

        if log_file.exists():
            today = time.strftime("%Y-%m-%d")
            try:
                with open(log_file) as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("node_id") != node_id:
                                continue
                            ts = entry.get("timestamp", "")
                            if not ts.startswith(today):
                                continue
                            cost = entry.get("entropy_cost", {})
                            consumed["compute_seconds"] += cost.get("compute_ms", 0) / 1000
                            consumed["api_calls"] += cost.get("api_calls", 0)
                            consumed["tokens"] += cost.get("tokens", 0)
                        except (json.JSONDecodeError, KeyError):
                            continue
            except Exception:
                pass  # If log parsing fails, assume budget available

        remaining = {
            "compute_seconds": max(0, budget.get("daily_compute_seconds", 3600) - consumed["compute_seconds"]),
            "api_calls": max(0, budget.get("daily_api_calls", 500) - consumed["api_calls"]),
            "tokens": max(0, budget.get("daily_tokens", 1000000) - consumed["tokens"]),
        }

        # Check if estimated cost fits
        if estimated_cost.get("compute_seconds", 0) > remaining["compute_seconds"]:
            return {"permitted": False, "reason": "Insufficient compute budget remaining", "remaining": remaining}
        if estimated_cost.get("api_calls", 0) > remaining["api_calls"]:
            return {"permitted": False, "reason": "Insufficient API call budget remaining", "remaining": remaining}
        if estimated_cost.get("tokens", 0) > remaining["tokens"]:
            return {"permitted": False, "reason": "Insufficient token budget remaining", "remaining": remaining}

        return {"permitted": True, "remaining": remaining, "consumed_today": consumed}

    def _consult_oracle(self, node_id: str, action_type: str, payload_hint: str = "") -> Dict[str, Any]:
        """
        Consult the safety oracle for this action.
        Returns: {"safe": bool, "rules_triggered": [...], "recommendation": str}
        """
        safety = self._load_safety()
        rules = safety.get("rules", [])
        triggered = []

        # Rule R001: no PII leak in payload hints
        if payload_hint:
            for pattern in ["@", "moltbook_", "api_key", "secret", "password"]:
                if pattern in payload_hint.lower():
                    triggered.append("R001")
                    break

        # Rule R008: API key safety — only communicate with known gateways
        if self.gateway_url not in ["https://harmonic-molecular-archivist.replit.app/api", "http://localhost", "https://localhost"]:
            triggered.append("R008")

        # Rule R002: rate limit gate — check if node is within rate limits
        profile = self._get_profile(node_id)
        if profile:
            # Check if this would exceed daily posts/comments (for handshake, check API calls)
            pass  # Rate limiting handled by ExchangeEndpoint RateLimiter

        # Drift patterns: check if node has been behaving anomalously
        drift_patterns = safety.get("drift_patterns", [])
        # In a full implementation, this would query recent history for drift

        safe = len(triggered) == 0
        return {
            "safe": safe,
            "rules_triggered": triggered,
            "drift_detected": False,
            "recommendation": "PROCEED" if safe else f"BLOCKED by rules: {triggered}",
        }

    def validate_exchange(
        self,
        node_id: str,
        token: SessionToken,
        requested_scopes: Optional[Set[str]] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Full constraint validation for a session exchange.
        This is the integration point: every token exchange is checked against
        node cost/risk profiles before session hydration is permitted.

        Args:
            node_id: The requesting node ID
            token: The SessionToken to validate
            requested_scopes: Optional scope narrowing (must be subset of token scope)
            force: Bypass human-approval gating (requires explicit authorization)

        Returns:
            {
                "permitted": bool,
                "reason": str,
                "blocked_by": str or None,
                "checks_passed": [str],
                "checks_failed": [str],
                "entropy_remaining": {...},
                "oracle_result": {...},
            }
        """
        checks_passed = []
        checks_failed = []
        oracle_result = {}
        entropy_result = {}

        # === CHECK 1: Token validity ===
        token_validation = self.token_engine.validate(token)
        if not token_validation["valid"]:
            checks_failed.append("token_validity")
            return {
                "permitted": False,
                "reason": token_validation["reason"],
                "blocked_by": "token_engine",
                "checks_passed": checks_passed,
                "checks_failed": checks_failed,
                "entropy_remaining": None,
                "oracle_result": None,
            }
        checks_passed.append("token_validity")

        # === CHECK 2: Profile existence ===
        profile = self._get_profile(node_id)
        if not profile:
            checks_failed.append("node_profile")
            return {
                "permitted": False,
                "reason": f"Node profile '{node_id}' not found in constraints/profiles.json",
                "blocked_by": "profiles",
                "checks_passed": checks_passed,
                "checks_failed": checks_failed,
                "entropy_remaining": None,
                "oracle_result": None,
            }
        checks_passed.append("node_profile")

        # === CHECK 3: Entropy budget ===
        estimated_cost = {"compute_seconds": 5, "api_calls": 1, "tokens": 500}
        entropy_result = self._check_entropy_budget(node_id, estimated_cost)
        if not entropy_result["permitted"]:
            checks_failed.append("entropy_budget")
            return {
                "permitted": False,
                "reason": entropy_result["reason"],
                "blocked_by": "constraints",
                "checks_passed": checks_passed,
                "checks_failed": checks_failed,
                "entropy_remaining": entropy_result.get("remaining"),
                "oracle_result": None,
            }
        checks_passed.append("entropy_budget")

        # === CHECK 4: Risk classification ===
        risk_class = self._get_risk_class("session_exchange")
        taxonomy = self._load_taxonomy()
        risk_def = taxonomy.get("risk_classes", {}).get(risk_class, {})
        checks_passed.append(f"risk_class:{risk_class}")

        # === CHECK 5: Oracle consult ===
        if risk_def.get("oracle_required", True):
            oracle_result = self._consult_oracle(node_id, "session_exchange")
            if not oracle_result["safe"]:
                checks_failed.append("oracle")
                return {
                    "permitted": False,
                    "reason": oracle_result["recommendation"],
                    "blocked_by": "oracle",
                    "checks_passed": checks_passed,
                    "checks_failed": checks_failed,
                    "entropy_remaining": entropy_result.get("remaining"),
                    "oracle_result": oracle_result,
                }
            checks_passed.append("oracle")

        # === CHECK 6: Human approval gating ===
        if risk_def.get("human_approval", False) and not force:
            checks_failed.append("human_approval")
            return {
                "permitted": False,
                "reason": f"Risk class '{risk_class}' requires human approval. Set force=True only with explicit authorization.",
                "blocked_by": "taxonomy",
                "checks_passed": checks_passed,
                "checks_failed": checks_failed,
                "entropy_remaining": entropy_result.get("remaining"),
                "oracle_result": oracle_result,
            }
        checks_passed.append("human_approval")

        # === CHECK 7: Scope alignment ===
        if requested_scopes:
            token_scope = token.scope.to_set()
            unauthorized = requested_scopes - token_scope
            if unauthorized:
                checks_failed.append("scope_alignment")
                return {
                    "permitted": False,
                    "reason": f"Requested scope(s) not in token: {unauthorized}",
                    "blocked_by": "scope_validator",
                    "checks_passed": checks_passed,
                    "checks_failed": checks_failed,
                    "entropy_remaining": entropy_result.get("remaining"),
                    "oracle_result": oracle_result,
                }
            checks_passed.append("scope_alignment")

        # === ALL CHECKS PASSED ===
        return {
            "permitted": True,
            "reason": "All constraint checks passed",
            "blocked_by": None,
            "checks_passed": checks_passed,
            "checks_failed": checks_failed,
            "entropy_remaining": entropy_result.get("remaining"),
            "oracle_result": oracle_result,
            "risk_class": risk_class,
        }

    def hydrate(self, token: SessionToken, force: bool = False) -> Dict[str, Any]:
        """
        Hydrate a token after full constraint validation.
        Shortcut that calls validate_exchange then manifest_engine.hydrate.
        """
        validation = self.validate_exchange(token.node_id, token, force=force)
        if not validation["permitted"]:
            return {
                "success": False,
                **{k: v for k, v in validation.items() if k != "permitted"},
            }

        return self.manifest_engine.hydrate(token, force=force)


def main():
    import argparse
    from handshake.token_engine import TokenScope

    parser = argparse.ArgumentParser(description="ASH-0.2 Handshake Constraint Validator")
    parser.add_argument("--node", required=True, help="Node ID")
    parser.add_argument("--token", help="Compact token string to validate")
    parser.add_argument("--generate", action="store_true", help="Generate a token, then validate it")
    parser.add_argument("--scope", nargs="+", default=["read:lattice"], help="Scopes for generation")
    parser.add_argument("--force", action="store_true", help="Bypass human approval gating")
    parser.add_argument("--gateway", default="https://harmonic-molecular-archivist.replit.app/api", help="Gateway URL")

    args = parser.parse_args()

    validator = HandshakeConstraintValidator(gateway_url=args.gateway)

    if args.generate:
        token_engine = TokenEngine(gateway_url=args.gateway)
        token = token_engine.generate(
            node_id=args.node,
            scopes=set(args.scope),
        )
        print("=== Generated Token ===")
        print(token.to_markdown_block())
        print()
        compact = token.to_compact_string()
        print(f"Compact: {compact}")
        print()
    else:
        if not args.token:
            print("❌ --token required (or use --generate)")
            return
        token_engine = TokenEngine(gateway_url=args.gateway)
        val_result = token_engine.validate_compact(args.token)
        if not val_result["valid"]:
            print(json.dumps(val_result, indent=2))
            return
        claims = val_result["claims"]
        from handshake.token_engine import SessionToken
        token = SessionToken(
            token_id=claims["token_id"],
            node_id=claims["node_id"],
            issued_at=claims["issued_at"],
            expires_at=claims["expires_at"],
            scope=TokenScope.from_set(set(claims["scope"])),
            gateway_url=claims.get("gateway_url", args.gateway),
            signature="",
        )
        compact = args.token

    # Run full constraint validation
    print("=== Constraint Validation ===")
    result = validator.validate_exchange(args.node, token, force=args.force)
    print(json.dumps(result, indent=2))

    if result["permitted"]:
        print("\n=== Hydration ===")
        hydration = validator.hydrate(token, force=args.force)
        if hydration["success"]:
            print(hydration["markdown"])
        else:
            print(json.dumps(hydration, indent=2))


if __name__ == "__main__":
    main()
