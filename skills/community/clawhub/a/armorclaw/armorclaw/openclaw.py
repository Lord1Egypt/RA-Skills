"""
ArmorClaw — OpenClaw integration.

Intercepts `vault:KEY_NAME` references in OpenClaw config/env and
resolves them from the encrypted vault at runtime.

Usage in OpenClaw workspace (AGENTS.md or tool):
    from armorclaw.openclaw import inject_vault_env
    inject_vault_env(password="your-master-password")

Or via environment variable (bot auto-unlock):
    export ARMORCLAW_PASSWORD="your-master-password"
    # Then call inject_vault_env() with no args
"""
import os
from .core import ArmorClaw

VAULT_PREFIX = "vault:"


def resolve_vault_refs(env: dict, ck: ArmorClaw, skill: str = "openclaw") -> dict:
    """
    Scan env dict for vault: references and resolve them.
    Returns new dict with resolved values.
    """
    resolved = {}
    for key, value in env.items():
        if isinstance(value, str) and value.startswith(VAULT_PREFIX):
            secret_name = value[len(VAULT_PREFIX):]
            secret_val  = ck.get(secret_name, skill=skill)
            if secret_val is not None:
                resolved[key] = secret_val
            else:
                resolved[key] = value  # leave as-is if not found
        else:
            resolved[key] = value
    return resolved


def inject_vault_env(password: str | None = None,
                     skill: str = "openclaw",
                     auto_unlock: bool = True) -> dict:
    """
    Unlock vault and inject all secrets into os.environ.
    Also resolves any vault: references already in os.environ.
    Auto-resolves machine-encrypted passwords (enc:v1:...).

    Returns dict of injected keys.
    """
    ck = ArmorClaw()
    if not ck.is_setup:
        return {}

    raw_pwd = password or os.getenv("ARMORCLAW_PASSWORD")
    if not raw_pwd:
        return {}

    # Auto-decrypt machine-bound passwords
    try:
        from .machine_crypto import resolve_password
        pwd = resolve_password(raw_pwd)
    except Exception:
        pwd = raw_pwd  # fallback to plain text if decrypt fails

    if not pwd:
        return {}

    result = ck.unlock(pwd)
    if not result["ok"]:
        return {}

    injected = {}

    # Inject all vault secrets into environment
    for item in ck.list():
        val = ck.get(item["name"], skill=skill)
        if val:
            os.environ[item["name"]] = val
            injected[item["name"]] = val

    # Resolve any vault: references in existing env
    for key, value in list(os.environ.items()):
        if isinstance(value, str) and value.startswith(VAULT_PREFIX):
            secret_name = value[len(VAULT_PREFIX):]
            secret_val  = ck.get(secret_name, skill=skill)
            if secret_val:
                os.environ[key] = secret_val
                injected[key]   = secret_val

    ck.lock()
    return injected


def get_vault_key(name: str, password: str | None = None,
                  skill: str = "openclaw") -> str | None:
    """
    Get a single key from the vault without injecting into environment.
    Useful for one-off lookups.
    """
    ck = ArmorClaw()
    if not ck.is_setup:
        return None

    raw_pwd = password or os.getenv("ARMORCLAW_PASSWORD")
    if not raw_pwd:
        return None

    try:
        from .machine_crypto import resolve_password
        pwd = resolve_password(raw_pwd)
    except Exception:
        pwd = raw_pwd

    result = ck.unlock(pwd)
    if not result["ok"]:
        return None

    val = ck.get(name, skill=skill)
    ck.lock()
    return val
