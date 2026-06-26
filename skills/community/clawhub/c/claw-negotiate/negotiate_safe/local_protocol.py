"""Self-contained SAFE protocol and local APOA token helpers.

It contains the small protocol surface this OpenClaw skill needs at runtime:
alternating-offer state, offer validation, and constraints loaded from a
per-negotiation token.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SAFE_SCHEMA = {
    "protocol": "apoa-alternating-offers",
    "version": "0.1",
    "based_on": "Rubinstein Alternating Offers (Econometrica, 1982)",
    "negotiation_id": "neg_<uuid>",
    "document_type": "safe-agreement",
    "issues": {
        "valuation_cap": {"type": "number", "label": "Valuation Cap ($)"},
        "investment_amount": {"type": "number", "label": "Investment Amount ($)"},
        "discount_rate": {"type": "number", "label": "Discount Rate (decimal)"},
        "pro_rata": {"type": "boolean", "label": "Pro-Rata Rights"},
        "mfn": {"type": "boolean", "label": "Most Favored Nation"},
    },
    "rules": {
        "max_rounds": 10,
        "first_mover": "founder",
        "offer_timeout_seconds": 300,
    },
}

VALID_OFFER_TYPES = {"offer", "counter", "accept", "reject"}
TYPE_MAP = {"number": (int, float), "boolean": bool}


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64url(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def create_local_token(*, payload: dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    head = _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body = _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    sig = hmac.new(secret.encode("utf-8"), f"{head}.{body}".encode("ascii"), hashlib.sha256).digest()
    return f"{head}.{body}.{_b64url(sig)}"


def load_apoa_token(token_path: str | Path, pubkey_path: str | Path = "") -> tuple[str, dict]:
    token = Path(token_path).read_text(encoding="utf-8").strip()
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid apoa token")
    secret = ""
    if pubkey_path:
        try:
            secret = Path(pubkey_path).read_text(encoding="utf-8").strip()
        except OSError:
            secret = ""
    if secret:
        expected = hmac.new(
            secret.encode("utf-8"),
            f"{parts[0]}.{parts[1]}".encode("ascii"),
            hashlib.sha256,
        ).digest()
        actual = _unb64url(parts[2])
        if not hmac.compare_digest(expected, actual):
            raise ValueError("invalid apoa token signature")
    payload = json.loads(_unb64url(parts[1]).decode("utf-8"))
    exp = payload.get("exp")
    if exp is not None and time.time() >= float(exp):
        raise ValueError("invalid apoa token: expired")
    constraints = payload.get("constraints") or {}
    if not isinstance(constraints, dict):
        raise ValueError("invalid apoa token constraints")
    return token, constraints


@dataclass
class ProtocolSchema:
    protocol: str
    version: str
    based_on: str
    negotiation_id: str
    document_type: str
    issues: dict[str, dict[str, str]]
    rules: dict[str, Any]

    @classmethod
    def load(cls, path: str | Path | None = None) -> "ProtocolSchema":
        data = SAFE_SCHEMA
        if path:
            try:
                data = json.loads(Path(path).read_text(encoding="utf-8"))
            except OSError:
                data = SAFE_SCHEMA
        neg_id = data.get("negotiation_id") or ""
        if neg_id == "neg_<uuid>":
            neg_id = f"neg_{uuid.uuid4().hex[:12]}"
        return cls(
            protocol=data["protocol"],
            version=data["version"],
            based_on=data.get("based_on", ""),
            negotiation_id=neg_id,
            document_type=data["document_type"],
            issues=data["issues"],
            rules=data["rules"],
        )


@dataclass
class NegotiationState:
    schema: ProtocolSchema
    history: list[dict] = field(default_factory=list)
    current_round: int = 0
    terminated: bool = False
    outcome: str | None = None

    @property
    def max_rounds(self) -> int:
        return int(self.schema.rules["max_rounds"])

    @property
    def first_mover(self) -> str:
        return str(self.schema.rules["first_mover"])

    def whose_turn(self) -> str:
        parties = ["founder", "investor"]
        if self.first_mover == "investor":
            parties = ["investor", "founder"]
        return parties[self.current_round % 2]

    def record_offer(self, offer: dict) -> None:
        self.history.append(offer)
        if offer["type"] == "accept":
            self.terminated = True
            self.outcome = "accepted"
        elif offer["type"] == "reject":
            self.terminated = True
            self.outcome = "rejected"
        else:
            self.current_round += 1
            if self.current_round >= self.max_rounds:
                self.terminated = True
                self.outcome = "max_rounds"

    def last_offer(self) -> dict | None:
        return self.history[-1] if self.history else None

    def agreed_terms(self) -> dict | None:
        if self.outcome != "accepted" or len(self.history) < 2:
            return None
        return self.history[-2].get("terms")


def validate_offer_structure(
    offer: dict,
    schema: ProtocolSchema,
    previous_offer: dict | None = None,
) -> tuple[bool, str]:
    if offer.get("type") not in VALID_OFFER_TYPES:
        return False, f"Invalid offer type: {offer.get('type')}"
    if offer["type"] in ("accept", "reject"):
        if offer["type"] == "accept" and "terms" in offer and previous_offer and "terms" in previous_offer:
            for key, value in previous_offer["terms"].items():
                if offer["terms"].get(key) != value:
                    return False, f"Accept terms mismatch on {key}"
        return True, ""
    terms = offer.get("terms")
    if not isinstance(terms, dict):
        return False, "Missing 'terms' field"
    for issue_name, issue_def in schema.issues.items():
        if issue_name not in terms:
            return False, f"Missing required issue: {issue_name}"
        expected = TYPE_MAP.get(issue_def["type"])
        if expected and not isinstance(terms[issue_name], expected):
            return False, f"Wrong type for '{issue_name}'"
    return True, ""


def validate_offer_turn(offer: dict, state: NegotiationState) -> tuple[bool, str]:
    expected = state.whose_turn()
    from_party = offer.get("from", "")
    if from_party and from_party != expected:
        return False, f"Not {from_party}'s turn. Expected: {expected}"
    return True, ""


def validate_apoa_constraints(terms: dict, constraints: dict) -> tuple[bool, list[str]]:
    violations: list[str] = []
    is_legacy = any(isinstance(v, dict) for v in constraints.values())
    if is_legacy:
        for field_name, rules in constraints.items():
            if field_name not in terms:
                violations.append(f"Missing constrained field: {field_name}")
                continue
            value = terms[field_name]
            if "min" in rules and isinstance(value, (int, float)) and value < rules["min"]:
                violations.append(f"{field_name}: {value} is below minimum {rules['min']}")
            if "max" in rules and isinstance(value, (int, float)) and value > rules["max"]:
                violations.append(f"{field_name}: {value} is above maximum {rules['max']}")
            if "required" in rules and isinstance(value, bool) and rules["required"] and not value:
                violations.append(f"{field_name}: required to be true but is false")
    else:
        aliases = {"discount": "discount_rate"}
        for key, constraint_value in constraints.items():
            if key.endswith("_min"):
                field = aliases.get(key.removesuffix("_min"), key.removesuffix("_min"))
                value = terms.get(field)
                if isinstance(value, (int, float)) and value < constraint_value:
                    violations.append(f"{field}: {value} is below minimum {constraint_value}")
            elif key.endswith("_max"):
                field = aliases.get(key.removesuffix("_max"), key.removesuffix("_max"))
                value = terms.get(field)
                if isinstance(value, (int, float)) and value > constraint_value:
                    violations.append(f"{field}: {value} is above maximum {constraint_value}")
            elif key.endswith("_required") and constraint_value:
                field = key.removesuffix("_required")
                if terms.get(field) is not True:
                    violations.append(f"{field}: required to be true but is false")
    return not violations, violations
