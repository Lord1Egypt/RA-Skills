"""ArmorClaw — Configuration manager. Change lock mode, IP, machine binding."""
import json
from pathlib import Path
from .store import get_lock_config, mark_initialized, _conn
from .auth  import (LockConfig, validate_password, get_machine_fingerprint,
                    get_external_ip, get_local_ip, get_current_ip)


def update_lock_config(new_config: LockConfig):
    """Persist updated lock config to vault meta."""
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO vault_meta(key,value) VALUES('lock_config',?)",
                  (json.dumps(new_config.to_dict()),))


def add_static_ip(use_external: bool = True) -> tuple[bool, str]:
    """Register current IP for lock restriction. Returns (ok, message)."""
    cfg = get_lock_config()

    if use_external:
        print("  Fetching your external IP...")
        ip = get_external_ip()
        if not ip:
            return False, "Could not detect external IP. Check your connection."
        ip_type = "external"
    else:
        ip = get_local_ip()
        ip_type = "local"

    print(f"  Detected IP: {ip}")
    cfg.registered_ip = ip
    cfg.ip_type = ip_type

    # Update mode to include ip
    if "static-ip" not in cfg.mode:
        if "machine" in cfg.mode:
            cfg.mode = "machine+static-ip"
        else:
            cfg.mode = "static-ip"

    update_lock_config(cfg)
    return True, f"IP restriction added: {ip} ({ip_type})"


def remove_ip_restriction() -> tuple[bool, str]:
    """Remove IP restriction from vault."""
    cfg = get_lock_config()
    cfg.registered_ip = ""
    cfg.ip_type = "local"
    cfg.mode = cfg.mode.replace("+static-ip", "").replace("static-ip", "password").strip("+")
    if not cfg.mode:
        cfg.mode = "password"
    update_lock_config(cfg)
    return True, "IP restriction removed"


def add_machine_binding() -> tuple[bool, str]:
    """Register current machine for lock restriction."""
    cfg = get_lock_config()
    fp = get_machine_fingerprint()
    cfg.registered_fingerprint = fp
    if "machine" not in cfg.mode:
        if "static-ip" in cfg.mode:
            cfg.mode = "machine+static-ip"
        else:
            cfg.mode = "machine"
    update_lock_config(cfg)
    return True, f"Machine binding registered (fingerprint: {fp[:16]}...)"


def remove_machine_binding() -> tuple[bool, str]:
    """Remove machine binding from vault."""
    cfg = get_lock_config()
    cfg.registered_fingerprint = ""
    cfg.mode = cfg.mode.replace("machine+", "").replace("machine", "password").strip("+")
    if not cfg.mode:
        cfg.mode = "password"
    update_lock_config(cfg)
    return True, "Machine binding removed"


def export_to_env(password: str, output_path: str,
                  names: list[str] | None = None) -> dict:
    """
    Export vault secrets back to a .env file.
    Requires master password. Optionally filter by key names.
    Returns: {exported: [...], skipped: [...]}
    """
    from .store import list_secrets, get_secret
    from pathlib import Path

    path = Path(output_path).expanduser().resolve()

    # Safety: warn if file exists
    if path.exists():
        return {"error": f"File already exists: {path}. Delete it first or choose a different path."}

    all_secrets = list_secrets()
    exported, skipped = [], []

    lines = ["# Exported from ArmorClaw vault\n"]
    for item in all_secrets:
        name = item["name"]
        if names and name not in names:
            skipped.append(name)
            continue
        try:
            val = get_secret(name, password, skill="export")
            if val:
                lines.append(f"{name}={val}\n")
                exported.append(name)
            else:
                skipped.append(name)
        except Exception as e:
            skipped.append(f"{name} (error: {e})")

    with open(path, "w") as f:
        f.writelines(lines)
    path.chmod(0o600)  # owner read/write only

    return {"exported": exported, "skipped": skipped, "path": str(path)}
