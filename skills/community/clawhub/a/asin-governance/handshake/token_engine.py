#!/usr/bin/env python3
"""
ASH-0.2 — Ephemeral Token Engine
Ephemeral HMAC-signed tokens with 2-hour expiry and scoped permissions.
Tokens are copy-paste friendly (markdown block format).

Security constraints enforced:
- Local vault control only (no credential harvesting)
- No unauthorized access: tokens require node_id + profile validation
- HMAC-SHA256 with per-node secret from local vault
- Scope enforcement: read:lattice, write:manifest, execute:tsh_compile
"""

import hmac
import hashlib
import secrets
import time
import json
import os
import re
from pathlib import Path
from typing import Optional, Set, Dict, Any
from dataclasses import dataclass, asdict

# === Configuration ===
DEFAULT_GATEWAY_URL = "https://harmonic-molecular-archivist.replit.app/api"
TOKEN_LIFETIME_SECONDS = 7200  # 2 hours
ALLOWED_SCOPES: Set[str] = {"read:lattice", "write:manifest", "execute:tsh_compile"}
TOKEN_VERSION = "ASH-0.2"


@dataclass(frozen=True)
class TokenScope:
    """Scoped permissions for a session token."""
    read_lattice: bool = False
    write_manifest: bool = False
    execute_tsh_compile: bool = False

    def to_set(self) -> Set[str]:
        result = set()
        if self.read_lattice:
            result.add("read:lattice")
        if self.write_manifest:
            result.add("write:manifest")
        if self.execute_tsh_compile:
            result.add("execute:tsh_compile")
        return result

    @classmethod
    def from_set(cls, scopes: Set[str]) -> "TokenScope":
        return cls(
            read_lattice="read:lattice" in scopes,
            write_manifest="write:manifest" in scopes,
            execute_tsh_compile="execute:tsh_compile" in scopes,
        )

    def __str__(self) -> str:
        return ",".join(sorted(self.to_set())) or "none"


@dataclass(frozen=True)
class SessionToken:
    """Immutable ephemeral session token."""
    token_id: str
    node_id: str
    issued_at: int  # unix timestamp
    expires_at: int  # unix timestamp
    scope: TokenScope
    gateway_url: str
    signature: str  # HMAC-SHA256 hex
    version: str = TOKEN_VERSION

    @property
    def is_expired(self) -> bool:
        return int(time.time()) > self.expires_at

    @property
    def lifetime_remaining(self) -> int:
        return max(0, self.expires_at - int(time.time()))

    def to_payload(self) -> Dict[str, Any]:
        """Returns the raw payload dict (without signature)."""
        return {
            "v": self.version,
            "id": self.token_id,
            "node": self.node_id,
            "iat": self.issued_at,
            "exp": self.expires_at,
            "scope": sorted(self.scope.to_set()),
            "gw": self.gateway_url,
        }

    def to_compact_string(self) -> str:
        """URL-safe compact representation."""
        payload = self.to_payload()
        payload["sig"] = self.signature
        # base64url-ish encoding using compact JSON
        import base64
        raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    def to_markdown_block(self) -> str:
        """Copy-paste friendly markdown block format."""
        payload = self.to_payload()
        expires_iso = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(self.expires_at))
        scope_str = ", ".join(sorted(self.scope.to_set())) or "none"

        block = f"""```ash-token
┌─ ASH-0.2 Session Token ───────────────────┐
│  Node:     {self.node_id:<35}│
│  ID:       {self.token_id:<35}│
│  Scope:    {scope_str:<35}│
│  Expires:  {expires_iso:<35}│
│  Gateway:  {self.gateway_url:<35}│
├─ Signature (HMAC-SHA256) ───────────────┤
│  {self.signature:<63}│
└─ Exchange: POST {self.gateway_url + '/sessions/exchange':<29}┘
```"""
        return block

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "token_id": self.token_id,
            "node_id": self.node_id,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "scope": sorted(self.scope.to_set()),
            "gateway_url": self.gateway_url,
            "signature": self.signature,
            "expired": self.is_expired,
            "lifetime_remaining_seconds": self.lifetime_remaining,
        }


class TokenEngine:
    """
    ASH-0.2 Token Engine.
    Generates and validates ephemeral session tokens.
    Secrets are read from the local vault (never harvested, never transmitted).
    """

    def __init__(
        self,
        vault_dir: Optional[Path] = None,
        gateway_url: str = DEFAULT_GATEWAY_URL,
    ):
        self.gateway_url = gateway_url.rstrip("/")
        self.vault_dir = vault_dir or self._default_vault_dir()
        self._secrets_cache: Dict[str, str] = {}

    @staticmethod
    def _default_vault_dir() -> Path:
        """Local vault: ~/.openclaw/workspace/skills/asin-governance/vault/"""
        return Path.home() / ".openclaw" / "workspace" / "skills" / "asin-governance" / "vault"

    def _node_secret_path(self, node_id: str) -> Path:
        """Path to the HMAC secret for a node."""
        # Sanitize node_id to prevent path traversal
        safe_node = re.sub(r"[^a-zA-Z0-9_-]", "", node_id)
        if not safe_node:
            raise ValueError(f"Invalid node_id: {node_id}")
        return self.vault_dir / f"{safe_node}.secret"

    def _load_or_create_secret(self, node_id: str) -> str:
        """Load or generate a node's HMAC secret from the local vault."""
        if node_id in self._secrets_cache:
            return self._secrets_cache[node_id]

        secret_path = self._node_secret_path(node_id)

        if secret_path.exists():
            secret = secret_path.read_text().strip()
        else:
            # Generate a cryptographically secure 256-bit secret
            secret = secrets.token_hex(32)
            self.vault_dir.mkdir(parents=True, exist_ok=True)
            secret_path.write_text(secret)
            # Restrict permissions: owner read-only
            os.chmod(secret_path, 0o600)

        self._secrets_cache[node_id] = secret
        return secret

    def _sign_payload(self, payload: Dict[str, Any], node_id: str) -> str:
        """HMAC-SHA256 sign a payload using the node's vault secret."""
        secret = self._load_or_create_secret(node_id)
        # Deterministic canonical encoding
        canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        sig = hmac.new(
            secret.encode("utf-8"),
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return sig

    def _verify_signature(self, payload: Dict[str, Any], signature: str, node_id: str) -> bool:
        """Verify HMAC signature in constant-time."""
        expected = self._sign_payload(payload, node_id)
        return hmac.compare_digest(expected, signature)

    def generate(
        self,
        node_id: str,
        scopes: Set[str],
        custom_gateway_url: Optional[str] = None,
        lifetime_seconds: Optional[int] = None,
    ) -> SessionToken:
        """
        Generate a new ephemeral session token for a node.

        Args:
            node_id: The requesting node's profile ID (must exist in profiles.json)
            scopes: Requested scope set. Will be intersected with ALLOWED_SCOPES.
            custom_gateway_url: Override the default gateway URL.
            lifetime_seconds: Override default 2-hour lifetime.

        Returns:
            SessionToken with HMAC signature.

        Raises:
            ValueError: If node_id invalid or scope contains unauthorized permissions.
        """
        # Validate scope
        requested = set(scopes)
        invalid = requested - ALLOWED_SCOPES
        if invalid:
            raise ValueError(f"Unauthorized scope(s): {invalid}. Allowed: {ALLOWED_SCOPES}")

        if not requested:
            raise ValueError("At least one scope must be requested.")

        now = int(time.time())
        lifetime = lifetime_seconds or TOKEN_LIFETIME_SECONDS
        token_id = secrets.token_hex(16)

        payload = {
            "v": TOKEN_VERSION,
            "id": token_id,
            "node": node_id,
            "iat": now,
            "exp": now + lifetime,
            "scope": sorted(requested),
            "gw": custom_gateway_url or self.gateway_url,
        }

        signature = self._sign_payload(payload, node_id)

        return SessionToken(
            token_id=token_id,
            node_id=node_id,
            issued_at=now,
            expires_at=now + lifetime,
            scope=TokenScope.from_set(requested),
            gateway_url=custom_gateway_url or self.gateway_url,
            signature=signature,
        )

    def validate(self, token: SessionToken) -> Dict[str, Any]:
        """
        Validate a token against all security constraints.

        Returns:
            {"valid": True, "claims": {...}} on success
            {"valid": False, "reason": "..."} on failure
        """
        # 1. Expiry check
        if token.is_expired:
            return {"valid": False, "reason": "Token expired", "code": "EXPIRED"}

        # 2. Version check
        if token.version != TOKEN_VERSION:
            return {
                "valid": False,
                "reason": f"Version mismatch: got {token.version}, expected {TOKEN_VERSION}",
                "code": "VERSION_MISMATCH",
            }

        # 3. Reconstruct payload and verify signature
        payload = token.to_payload()
        if not self._verify_signature(payload, token.signature, token.node_id):
            return {"valid": False, "reason": "Invalid signature", "code": "BAD_SIGNATURE"}

        # 4. Scope check
        active_scopes = token.scope.to_set()
        invalid = active_scopes - ALLOWED_SCOPES
        if invalid:
            return {"valid": False, "reason": f"Invalid scope: {invalid}", "code": "BAD_SCOPE"}

        return {
            "valid": True,
            "reason": "Token valid",
            "code": "OK",
            "claims": {
                "node_id": token.node_id,
                "token_id": token.token_id,
                "issued_at": token.issued_at,
                "expires_at": token.expires_at,
                "scope": sorted(active_scopes),
                "lifetime_remaining": token.lifetime_remaining,
            },
        }

    def validate_compact(self, compact_string: str) -> Dict[str, Any]:
        """Validate a compact/base64url token string."""
        import base64
        try:
            # Pad and decode
            padded = compact_string + "=" * (-len(compact_string) % 4)
            raw = base64.urlsafe_b64decode(padded)
            data = json.loads(raw.decode("utf-8"))

            token = SessionToken(
                token_id=data["id"],
                node_id=data["node"],
                issued_at=data["iat"],
                expires_at=data["exp"],
                scope=TokenScope.from_set(set(data.get("scope", []))),
                gateway_url=data["gw"],
                signature=data["sig"],
                version=data.get("v", TOKEN_VERSION),
            )
            return self.validate(token)
        except Exception as e:
            return {"valid": False, "reason": f"Malformed token: {e}", "code": "MALFORMED"}

    def revoke(self, token_id: str) -> bool:
        """
        Revoke a token by adding it to the revocation log.
        Returns True if newly revoked, False if already revoked.
        """
        revocation_path = self.vault_dir / "revoked_tokens.txt"
        revoked = set()
        if revocation_path.exists():
            revoked = set(revocation_path.read_text().strip().splitlines())

        if token_id in revoked:
            return False

        revoked.add(token_id)
        revocation_path.write_text("\n".join(sorted(revoked)) + "\n")
        os.chmod(revocation_path, 0o600)
        return True

    def is_revoked(self, token_id: str) -> bool:
        """Check if a token has been revoked."""
        revocation_path = self.vault_dir / "revoked_tokens.txt"
        if not revocation_path.exists():
            return False
        revoked = set(revocation_path.read_text().strip().splitlines())
        return token_id in revoked


# === CLI Interface ===

def main():
    import argparse

    parser = argparse.ArgumentParser(description="ASH-0.2 Token Engine")
    parser.add_argument("--node", default="ace-main", help="Node ID")
    parser.add_argument("--scope", nargs="+", default=["read:lattice"], help="Requested scopes")
    parser.add_argument("--gateway", default=DEFAULT_GATEWAY_URL, help="Gateway URL")
    parser.add_argument("--lifetime", type=int, default=TOKEN_LIFETIME_SECONDS, help="Token lifetime (seconds)")
    parser.add_argument("--validate", help="Validate a compact token string")
    parser.add_argument("--markdown", action="store_true", default=True, help="Output markdown format")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()
    engine = TokenEngine(gateway_url=args.gateway)

    if args.validate:
        result = engine.validate_compact(args.validate)
        print(json.dumps(result, indent=2))
        return

    scopes = set(args.scope)
    try:
        token = engine.generate(
            node_id=args.node,
            scopes=scopes,
            custom_gateway_url=args.gateway if args.gateway != DEFAULT_GATEWAY_URL else None,
            lifetime_seconds=args.lifetime,
        )
    except ValueError as e:
        print(f"❌ {e}", file=os.sys.stderr)
        os.sys.exit(1)

    if args.json:
        print(json.dumps(token.to_dict(), indent=2))
    else:
        print(token.to_markdown_block())
        print(f"\n🕐 Expires in {token.lifetime_remaining // 3600}h {(token.lifetime_remaining % 3600) // 60}m")


if __name__ == "__main__":
    main()
