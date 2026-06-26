"""ArmorClaw — Authentication: master password + machine binding."""
import hashlib, hmac, os, re, socket, uuid, json
from pathlib import Path

MIN_LENGTH   = 12
REQUIRE_UPPER   = True
REQUIRE_NUMBER  = True
REQUIRE_SPECIAL = True
SPECIAL_CHARS   = set("!@#$%^&*()_+-=[]{}|;':\",./<>?")


# ── Password validation ───────────────────────────────────────────────────

def validate_password(password: str) -> list[str]:
    """Returns list of errors. Empty list = password is valid."""
    errors = []
    if len(password) < MIN_LENGTH:
        errors.append(f"Must be at least {MIN_LENGTH} characters")
    if REQUIRE_UPPER and not any(c.isupper() for c in password):
        errors.append("Must contain at least one uppercase letter")
    if REQUIRE_NUMBER and not any(c.isdigit() for c in password):
        errors.append("Must contain at least one number")
    if REQUIRE_SPECIAL and not any(c in SPECIAL_CHARS for c in password):
        errors.append("Must contain at least one special character (!@#$%^&* etc.)")
    return errors


# ── Machine fingerprint ───────────────────────────────────────────────────

def get_mac_address() -> str:
    """Get primary network interface MAC address."""
    mac = uuid.getnode()
    return ":".join(f"{(mac >> (i*8)) & 0xff:02x}" for i in reversed(range(6)))


def get_hostname() -> str:
    return socket.gethostname()


def get_machine_fingerprint() -> str:
    """Stable machine identifier from MAC + hostname."""
    mac = get_mac_address()
    host = get_hostname()
    raw = f"{mac}:{host}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_local_ip() -> str:
    """Best-effort local/internal IP detection."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_external_ip() -> str:
    """Fetch external/public IP from a trusted lookup service."""
    import urllib.request, ssl
    services = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
    ]
    ctx = ssl.create_default_context()
    for url in services:
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=5) as r:
                return r.read().decode().strip()
        except Exception:
            continue
    return ""


def get_current_ip(mode: str = "local") -> str:
    """Return IP based on mode: 'local' or 'external'."""
    if mode == "external":
        return get_external_ip() or get_local_ip()
    return get_local_ip()


# ── Lock mode config ──────────────────────────────────────────────────────

class LockConfig:
    """Controls how ArmorClaw unlocks."""

    def __init__(self, data: dict | None = None):
        d = data or {}
        self.mode:         str        = d.get("mode", "password")
        # modes:
        #   password           — always prompt for master password
        #   machine            — auto-unlock on registered machine only
        #   static-ip          — external static IP restriction only
        #   machine+static-ip  — strongest: machine AND external static IP
        #   bot                — bot auto-unlocks (password stored encrypted)

        self.registered_fingerprint: str  = d.get("registered_fingerprint", "")
        self.registered_ip:          str  = d.get("registered_ip", "")
        self.ip_type:                str  = d.get("ip_type", "local")   # local | external
        self.allow_auto_unlock:      bool = d.get("allow_auto_unlock", False)

    def to_dict(self) -> dict:
        return {
            "mode":                    self.mode,
            "registered_fingerprint":  self.registered_fingerprint,
            "registered_ip":           self.registered_ip,
            "ip_type":                 self.ip_type,
            "allow_auto_unlock":       self.allow_auto_unlock,
        }

    def check_machine(self) -> tuple[bool, str]:
        """Returns (allowed, reason)."""
        fp = get_machine_fingerprint()
        if self.registered_fingerprint and fp != self.registered_fingerprint:
            return False, f"Machine not registered. Expected fingerprint does not match."
        return True, "ok"

    def check_ip(self) -> tuple[bool, str]:
        mode = "external" if self.ip_type == "external" else "local"
        ip = get_current_ip(mode=mode)
        if self.registered_ip and ip != self.registered_ip:
            return False, (
                f"Access denied from {'external' if mode == 'external' else 'local'} "
                f"IP {ip}. Registered: {self.registered_ip}"
            )
        return True, "ok"

    def check_access(self) -> tuple[bool, str]:
        """Run all configured access checks."""
        if "machine" in self.mode:
            ok, reason = self.check_machine()
            if not ok:
                return False, reason
        if "ip" in self.mode or "static-ip" in self.mode:
            ok, reason = self.check_ip()
            if not ok:
                return False, reason
        return True, "ok"
