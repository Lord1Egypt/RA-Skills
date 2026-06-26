"""Deterministic planning helpers for APOA token minting."""
from __future__ import annotations

import os
from dataclasses import dataclass
import json
import secrets
import subprocess
from pathlib import Path
from typing import Mapping

from local_protocol import create_local_token


@dataclass(frozen=True)
class RolePlan:
    user_role: str
    user_flag_prefix: str
    ai_flag_prefix: str
    ai_env_prefix: str


@dataclass(frozen=True)
class MintIdentity:
    founder_name: str
    founder_title: str
    investor_name: str
    investor_firm: str
    company: str


_PLACEHOLDER_VALUES = {
    "alex chen",
    "angel ventures",
    "apoa founder ai agent",
    "apoa investor ai agent",
    "company",
    "demo capital",
    "demo founder",
    "demo investor",
    "founder",
    "investor",
    "investor firm",
    "jane doe",
}


def identity_value(value: object, *, field: str = "", drop_placeholders: bool = True) -> str:
    """Return a user-facing identity value, dropping known demo/bot placeholders."""
    text = str(value or "").strip()
    if not text:
        return ""
    lowered = " ".join(text.lower().split())
    if drop_placeholders and lowered in _PLACEHOLDER_VALUES:
        return ""
    if "ai agent" in lowered:
        return ""
    if drop_placeholders and field == "company" and lowered == "apoa":
        # APOA is the demo/bot brand in this skill, not the user's startup.
        return ""
    return text


def normalize_user_role(role: object) -> str:
    """Return a supported negotiation role, defaulting safely to founder."""
    normalized = str(role or "founder").strip().lower()
    if normalized not in ("founder", "investor"):
        return "founder"
    return normalized


def role_plan(role: object) -> RolePlan:
    """Map the user's role to local user/counterparty defaults."""
    user_role = normalize_user_role(role)
    if user_role == "investor":
        return RolePlan(
            user_role=user_role,
            user_flag_prefix="--investor-",
            ai_flag_prefix="--founder-",
            ai_env_prefix="FOUNDER_",
        )
    return RolePlan(
        user_role=user_role,
        user_flag_prefix="--founder-",
        ai_flag_prefix="--investor-",
        ai_env_prefix="INVESTOR_",
    )


def resolve_mint_identity(
    constraints: Mapping[str, object],
    *,
    env: Mapping[str, str] | None = None,
) -> MintIdentity:
    """Resolve party display fields for local token/config generation."""
    environ = env if env is not None else os.environ
    user_role = normalize_user_role(constraints.get("role"))
    mode = str(constraints.get("mode") or "demo").strip().lower()
    is_demo = mode == "demo"

    demo_founder_name = "Demo Founder" if is_demo and user_role == "investor" else ""
    demo_founder_title = "CEO" if is_demo and user_role == "investor" else ""
    demo_investor_name = "Demo Investor" if is_demo and user_role == "founder" else ""
    demo_investor_firm = "Demo Capital" if is_demo and user_role == "founder" else ""

    return MintIdentity(
        founder_name=(
            identity_value(constraints.get("founder_name"), drop_placeholders=False)
            or identity_value(environ.get("FOUNDER_NAME"))
            or demo_founder_name
            or "Founder"
        ),
        founder_title=(
            identity_value(constraints.get("founder_title"), drop_placeholders=False)
            or identity_value(environ.get("FOUNDER_TITLE"))
            or demo_founder_title
            or "CEO"
        ),
        investor_name=(
            identity_value(constraints.get("investor_name"), drop_placeholders=False)
            or identity_value(environ.get("INVESTOR_NAME"))
            or demo_investor_name
            or "Investor"
        ),
        investor_firm=(
            identity_value(constraints.get("investor_firm"), drop_placeholders=False)
            or identity_value(environ.get("INVESTOR_FIRM"))
            or demo_investor_firm
            or "Investor Firm"
        ),
        company=(
            identity_value(constraints.get("company_name"), field="company", drop_placeholders=False)
            or identity_value(environ.get("COMPANY_NAME"), field="company")
            or "Company"
        ),
    )


def slugify_company(company: str) -> str:
    return "".join(
        c.lower() if c.isalnum() else "-" for c in company
    ).strip("-")


def build_service_name(company: str, negotiation_id: str) -> str:
    return f"safe:{slugify_company(company)}:{negotiation_id}"


def resolve_investment_amount(constraints: Mapping[str, object]) -> float:
    """Return a representative check size for defaults and display."""
    amount = (
        constraints.get("investment_amount")
        or constraints.get("investment_amount_min")
        or 500_000.0
    )
    return float(amount)


def resolve_investment_amount_bounds(constraints: Mapping[str, object]) -> tuple[float, float]:
    amount = resolve_investment_amount(constraints)
    amount_min = float(constraints.get("investment_amount_min") or amount)
    amount_max = float(constraints.get("investment_amount_max") or amount)
    return amount_min, amount_max


def _role_constraints(constraints: Mapping[str, object]) -> dict:
    discount_min = float(constraints.get("discount_min", 0))
    return {
        "valuation_cap_min": int(constraints["valuation_cap_min"]),
        "valuation_cap_max": int(constraints["valuation_cap_max"]),
        "investment_amount_min": resolve_investment_amount_bounds(constraints)[0],
        "investment_amount_max": resolve_investment_amount_bounds(constraints)[1],
        "discount_rate_min": discount_min,
        "discount_rate_max": float(constraints.get("discount_max", discount_min)),
        "pro_rata_required": constraints.get("pro_rata") == "required",
        "mfn_required": constraints.get("mfn") == "required",
    }


def _env_counterparty_constraints(prefix: str, amount: float) -> dict:
    def _get_float(name: str, default: float) -> float:
        raw = os.environ.get(f"{prefix}_{name}")
        return float(raw) if raw else default

    def _get_int(name: str, default: int) -> int:
        raw = os.environ.get(f"{prefix}_{name}")
        return int(raw) if raw else default

    def _get_bool(name: str, default: bool) -> bool:
        raw = os.environ.get(f"{prefix}_{name}")
        return raw.lower() in ("true", "1", "yes") if raw else default

    discount_min = _get_float("DISCOUNT_MIN", 0.15)
    return {
        "valuation_cap_min": _get_int("CAP_MIN", 6_000_000),
        "valuation_cap_max": _get_int("CAP_MAX", 10_000_000),
        "investment_amount_min": _get_float("INVESTMENT_AMOUNT_MIN", amount),
        "investment_amount_max": _get_float("INVESTMENT_AMOUNT_MAX", amount),
        "discount_rate_min": discount_min,
        "discount_rate_max": _get_float("DISCOUNT_MAX", discount_min),
        "pro_rata_required": _get_bool("PRO_RATA_REQUIRED", False),
        "mfn_required": _get_bool("MFN_REQUIRED", False),
    }


def _create_signing_key(
    *,
    sshsign_host: str,
    constraints: dict,
    require_signature: bool = True,
    runner=None,
) -> str:
    runner = runner or subprocess.run
    argv = [
        "ssh",
        sshsign_host,
        "create-key",
        "--scope", "safe-agreement",
        "--tier", "cosign",
        "--constraints", json.dumps(constraints, separators=(",", ":")),
    ]
    if require_signature:
        argv.append("--require-signature")
    result = runner(argv, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "create-key failed").strip())
    payload = json.loads(result.stdout or "{}")
    key_id = str(payload.get("key_id") or "")
    if not key_id:
        raise RuntimeError("create-key did not return key_id")
    return key_id


def write_local_mint_files(
    *,
    negotiation_id: str,
    constraints: Mapping[str, object],
    neg_dir: str | Path,
    expires_at_epoch: int,
    expires_str: str,
    service: str,
    shared_session: bool = False,
    sshsign_host: str = "sshsign.dev",
    env: Mapping[str, str] | None = None,
    runner=None,
) -> tuple[dict, str]:
    """Create local token/config files without an external negotiate engine."""
    environ = env if env is not None else os.environ
    runner = runner or subprocess.run
    neg_path = Path(neg_dir)
    keys_dir = neg_path / "keys"
    tokens_dir = neg_path / "tokens"
    keys_dir.mkdir(parents=True, exist_ok=True)
    tokens_dir.mkdir(parents=True, exist_ok=True)

    plan = role_plan(constraints.get("role"))
    identity = resolve_mint_identity(constraints, env=environ)
    amount = resolve_investment_amount(constraints)
    amount_min, amount_max = resolve_investment_amount_bounds(constraints)

    user_constraints = _role_constraints(constraints)
    ai_prefix = plan.ai_env_prefix.rstrip("_")
    ai_constraints = _env_counterparty_constraints(ai_prefix, amount)
    founder_constraints = user_constraints if plan.user_role == "founder" else ai_constraints
    investor_constraints = user_constraints if plan.user_role == "investor" else ai_constraints

    founder_secret = secrets.token_urlsafe(32)
    investor_secret = secrets.token_urlsafe(32)
    (keys_dir / "founder_private.pem").write_text(founder_secret, encoding="utf-8")
    (keys_dir / "founder_public.pem").write_text(founder_secret, encoding="utf-8")
    (keys_dir / "investor_private.pem").write_text(investor_secret, encoding="utf-8")
    (keys_dir / "investor_public.pem").write_text(investor_secret, encoding="utf-8")

    principal_id = environ.get("USER_DID") or "did:apoa:default"

    def _payload(role: str, constraints_payload: dict) -> dict:
        return {
            "iss": principal_id,
            "sub": f"did:apoa:{role}-agent",
            "aud": service,
            "role": role,
            "scope": ["offer:submit", "offer:accept", "document:sign"],
            "constraints": constraints_payload,
            "exp": expires_at_epoch,
        }

    (tokens_dir / "founder.jwt").write_text(
        create_local_token(payload=_payload("founder", founder_constraints), secret=founder_secret),
        encoding="utf-8",
    )
    (tokens_dir / "investor.jwt").write_text(
        create_local_token(payload=_payload("investor", investor_constraints), secret=investor_secret),
        encoding="utf-8",
    )

    founder_key_id = _create_signing_key(
        sshsign_host=sshsign_host,
        constraints={
            "valuation_cap": {"min": founder_constraints["valuation_cap_min"], "max": founder_constraints["valuation_cap_max"]},
            "investment_amount": {"min": founder_constraints["investment_amount_min"], "max": founder_constraints["investment_amount_max"]},
            "discount_rate": {"min": founder_constraints["discount_rate_min"], "max": founder_constraints["discount_rate_max"]},
            "pro_rata": {"required": founder_constraints["pro_rata_required"]},
        },
        runner=runner,
    )
    investor_key_id = _create_signing_key(
        sshsign_host=sshsign_host,
        constraints={
            "valuation_cap": {"min": investor_constraints["valuation_cap_min"], "max": investor_constraints["valuation_cap_max"]},
            "investment_amount": {"min": investor_constraints["investment_amount_min"], "max": investor_constraints["investment_amount_max"]},
            "discount_rate": {"min": investor_constraints["discount_rate_min"], "max": investor_constraints["discount_rate_max"]},
            "pro_rata": {"required": investor_constraints["pro_rata_required"]},
        },
        runner=runner,
    )

    shared = {
        "negotiation_id": negotiation_id,
        "session_id": f"session_{negotiation_id}",
        "schema": "",
        "sshsign_host": sshsign_host,
        "investment_amount": amount,
        "company_name": identity.company,
        "date": "",
        "founder_signing_key_id": founder_key_id,
        "investor_signing_key_id": investor_key_id,
    }
    founder_config = {
        **shared,
        "role": "founder",
        "token": str(tokens_dir / "founder.jwt"),
        "pubkey": str(keys_dir / "founder_public.pem"),
        "signing_key_id": founder_key_id,
        "name": identity.founder_name,
        "title": identity.founder_title,
        "party_name": identity.founder_name,
        "investor_name": identity.investor_name,
        "investor_firm": identity.investor_firm,
    }
    investor_config = {
        **shared,
        "role": "investor",
        "token": str(tokens_dir / "investor.jwt"),
        "pubkey": str(keys_dir / "investor_public.pem"),
        "signing_key_id": investor_key_id,
        "name": identity.investor_name,
        "party_name": identity.investor_name,
        "founder_name": identity.founder_name,
        "founder_title": identity.founder_title,
        "investor_firm": identity.investor_firm,
    }
    (neg_path / "founder.json").write_text(json.dumps(founder_config, indent=2), encoding="utf-8")
    (neg_path / "investor.json").write_text(json.dumps(investor_config, indent=2), encoding="utf-8")

    output = {
        "negotiation_id": negotiation_id,
        "founder_config_path": str(neg_path / "founder.json"),
        "investor_config_path": str(neg_path / "investor.json"),
        "founder_token_path": str(tokens_dir / "founder.jwt"),
        "investor_token_path": str(tokens_dir / "investor.jwt"),
        "expires_at": expires_str,
        "service": service,
        "founder_constraints": founder_constraints,
        "investor_constraints": investor_constraints,
    }
    return output, plan.user_role
