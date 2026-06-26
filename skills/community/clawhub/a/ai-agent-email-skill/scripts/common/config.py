from pathlib import Path
from typing import Any

from .errors import SkillError
from .auth import _detect_auth_type


def load_config() -> dict[str, Any]:
    config_dir = Path(__file__).resolve().parent.parent
    config_name = "config.toml"
    config_path = config_dir / config_name
    if not config_path.exists():
        raise SkillError(
            "CONFIG_ERROR",
            f"config file not found",
            {"configPath": str(config_path)},
        )
    with config_path.open("rb") as f:
        import tomllib
        return tomllib.load(f)


def _get_account_names(config: dict[str, Any]) -> list[str]:
    accounts = config.get("accounts")
    if not isinstance(accounts, dict) or not accounts:
        return []
    return list(accounts.keys())


def _get_nested_value(config: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    """Safely get a nested value from config using a list of keys."""
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def _merge_account_config(global_cfg: dict[str, Any], account_cfg: dict[str, Any]) -> dict[str, Any]:
    """Merge global settings with account-specific settings (account takes precedence)."""
    merged = {}
    
    # Deep merge function for nested dicts
    def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    return deep_merge(global_cfg, account_cfg) if global_cfg else account_cfg


def validate_account_config(account_name: str, account_cfg: dict[str, Any]) -> None:
    """Validate account configuration and raise descriptive errors."""
    # Required fields
    if not account_cfg.get("email"):
        raise SkillError("CONFIG_ERROR", f"Account '{account_name}' missing required field: email")
    
    # Auth detection (from environment variables)
    auth_type = _detect_auth_type()
    if not auth_type:
        raise SkillError(
            "CONFIG_ERROR",
            f"Account '{account_name}': No credentials configured. Set EMAIL_PASSWORD (or EMAIL_OAUTH2_*) environment variable."
        )
    
    # IMAP validation
    imap_cfg = account_cfg.get("imap", {})
    if not imap_cfg.get("host"):
        raise SkillError("CONFIG_ERROR", f"Account '{account_name}': imap.host is required")
    if not imap_cfg.get("port"):
        imap_cfg["port"] = 993 if imap_cfg.get("tls", True) else 143
    
    # SMTP validation
    smtp_cfg = account_cfg.get("smtp", {})
    if not smtp_cfg.get("host"):
        raise SkillError("CONFIG_ERROR", f"Account '{account_name}': smtp.host is required")
    if not smtp_cfg.get("port"):
        smtp_cfg["port"] = 465 if smtp_cfg.get("tls", True) else 587
    
    # TLS/STARTTLS conflict check
    tls_conflict_imap = imap_cfg.get("tls", False) and imap_cfg.get("starttls", False)
    tls_conflict_smtp = smtp_cfg.get("tls", False) and smtp_cfg.get("starttls", False)
    
    if tls_conflict_imap:
        raise SkillError(
            "CONFIG_ERROR",
            f"Account '{account_name}': imap.tls and imap.starttls cannot both be true"
        )
    if tls_conflict_smtp:
        raise SkillError(
            "CONFIG_ERROR",
            f"Account '{account_name}': smtp.tls and smtp.starttls cannot both be true"
        )


def resolve_account(config: dict[str, Any], requested_account: str | None) -> tuple[str, dict[str, Any]]:
    accounts = config.get("accounts")
    if not isinstance(accounts, dict) or not accounts:
        raise SkillError("CONFIG_ERROR", "[accounts] table is missing or empty in config.toml")

    if requested_account:
        account = accounts.get(requested_account)
        if not isinstance(account, dict):
            raise SkillError("CONFIG_ERROR", f"Account not found: {requested_account}")
        
        # Merge with global settings
        global_cfg = config.get("global", {})
        merged_cfg = _merge_account_config(global_cfg, account)
        
        # Validate the merged configuration
        validate_account_config(requested_account, merged_cfg)
        
        return requested_account, merged_cfg

    for account_name, account_cfg in accounts.items():
        if isinstance(account_cfg, dict) and account_cfg.get("default") is True:
            # Merge with global settings
            global_cfg = config.get("global", {})
            merged_cfg = _merge_account_config(global_cfg, account_cfg)
            
            # Validate the merged configuration
            validate_account_config(account_name, merged_cfg)
            
            return account_name, merged_cfg

    # Fallback to first account
    first_name = next(iter(accounts.keys()))
    first_cfg = accounts[first_name]
    if not isinstance(first_cfg, dict):
        raise SkillError("CONFIG_ERROR", f"Invalid account config shape for: {first_name}")
    
    # Merge with global settings
    global_cfg = config.get("global", {})
    merged_cfg = _merge_account_config(global_cfg, first_cfg)
    
    # Validate the merged configuration
    validate_account_config(first_name, merged_cfg)
    
    return first_name, merged_cfg
