"""
ArmorClaw — Encrypted secrets manager for OpenClaw agents.
Stores API keys, tokens, and credentials in an AES-256 encrypted vault.

Quick start:
    from armorclaw import ArmorClaw

    ck = ArmorClaw()
    ck.unlock("your-master-password")

    api_key = ck.get("OPENAI_KEY")
    ck.set("NEW_KEY", "value")
"""
from .core    import ArmorClaw
from .store   import init_vault, is_initialized, VAULT_DIR
from .auth    import validate_password, LockConfig
from .session import ArmorClawSession

__version__ = "1.0.0"
__all__ = ["ArmorClaw", "init_vault", "is_initialized", "validate_password",
           "LockConfig", "ArmorClawSession", "VAULT_DIR"]
