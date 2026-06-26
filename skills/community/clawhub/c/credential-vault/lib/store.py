"""Encrypted credential store management."""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from . import crypto


DEFAULT_VAULT_DIR = Path.home() / ".openclaw" / "vault"
VAULT_FILE = "vault.enc.json"
SESSION_FILE = "session"  # Stores unlocked key temporarily


class VaultError(Exception):
    """Base exception for vault operations."""
    pass


class VaultLocked(VaultError):
    """Vault is locked and requires unlock."""
    pass


class VaultNotInitialized(VaultError):
    """Vault has not been initialized."""
    pass


class Store:
    """Manages encrypted credential storage."""
    
    def __init__(self, vault_dir: Optional[Path] = None):
        self.vault_dir = vault_dir or DEFAULT_VAULT_DIR
        self.vault_file = self.vault_dir / VAULT_FILE
        self.session_file = self.vault_dir / SESSION_FILE
        self._session_key: Optional[bytes] = None
    
    def init(self, master_password: str) -> None:
        """Initialize a new vault with master password.
        
        Args:
            master_password: Master password for the vault
        
        Raises:
            VaultError: If vault already exists
        """
        if self.vault_file.exists():
            raise VaultError("Vault already initialized. Use 'vault unlock' to access.")
        
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
        salt = crypto.generate_salt()
        password_hash = crypto.hash_password(master_password)
        
        vault_data = {
            "version": "1.0",
            "salt": crypto.encode_b64(salt),
            "password_hash": password_hash,
            "entries": {}
        }
        
        self._write_vault(vault_data)
        print(f"✅ Vault initialized at {self.vault_file}")
    
    def unlock(self, master_password: str) -> None:
        """Unlock the vault for the current session.
        
        Args:
            master_password: Master password
        
        Raises:
            VaultNotInitialized: If vault doesn't exist
            VaultError: If password is incorrect
        """
        if not self.vault_file.exists():
            raise VaultNotInitialized("Vault not initialized. Run 'vault init' first.")
        
        vault_data = self._read_vault()
        
        # Verify password
        password_hash = crypto.hash_password(master_password)
        if password_hash != vault_data["password_hash"]:
            raise VaultError("❌ Incorrect master password")
        
        # Derive and store session key
        salt = crypto.decode_b64(vault_data["salt"])
        self._session_key = crypto.derive_key(master_password, salt)
        
        # Store key in session file (for multi-command usage)
        self.session_file.write_bytes(self._session_key)
        print("🔓 Vault unlocked")
    
    def lock(self) -> None:
        """Lock the vault and clear session key."""
        self._session_key = None
        if self.session_file.exists():
            self.session_file.unlink()
        print("🔒 Vault locked")
    
    def is_unlocked(self) -> bool:
        """Check if vault is currently unlocked."""
        if self._session_key:
            return True
        if self.session_file.exists():
            self._session_key = self.session_file.read_bytes()
            return True
        return False
    
    def _ensure_unlocked(self) -> bytes:
        """Ensure vault is unlocked and return session key.
        
        Returns:
            Session encryption key
        
        Raises:
            VaultLocked: If vault is locked
        """
        if not self.is_unlocked():
            raise VaultLocked("Vault is locked. Run 'vault unlock' first.")
        return self._session_key
    
    def add(self, key_name: str, value: str, tags: Optional[List[str]] = None, 
            expires: Optional[str] = None) -> None:
        """Add or update a credential.
        
        Args:
            key_name: Name of the credential
            value: Secret value
            tags: Optional list of tags (e.g., skill names)
            expires: Optional expiry date (ISO format: YYYY-MM-DD)
        
        Raises:
            VaultLocked: If vault is locked
        """
        session_key = self._ensure_unlocked()
        vault_data = self._read_vault()
        
        # Encrypt the value
        nonce, ciphertext, tag = crypto.encrypt(value, session_key)
        
        vault_data["entries"][key_name] = {
            "nonce": crypto.encode_b64(nonce),
            "ciphertext": crypto.encode_b64(ciphertext),
            "tag": crypto.encode_b64(tag),
            "metadata": {
                "created": datetime.utcnow().isoformat(),
                "modified": datetime.utcnow().isoformat(),
                "tags": tags or [],
                "expires": expires
            }
        }
        
        self._write_vault(vault_data)
        print(f"✅ Added credential: {key_name}")
    
    def get(self, key_name: str) -> str:
        """Retrieve and decrypt a credential.
        
        Args:
            key_name: Name of the credential
        
        Returns:
            Decrypted value
        
        Raises:
            VaultLocked: If vault is locked
            KeyError: If credential not found
        """
        session_key = self._ensure_unlocked()
        vault_data = self._read_vault()
        
        if key_name not in vault_data["entries"]:
            raise KeyError(f"Credential not found: {key_name}")
        
        entry = vault_data["entries"][key_name]
        nonce = crypto.decode_b64(entry["nonce"])
        ciphertext = crypto.decode_b64(entry["ciphertext"])
        tag = crypto.decode_b64(entry["tag"])
        
        return crypto.decrypt(nonce, ciphertext, tag, session_key)
    
    def list(self, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all credentials (values masked).
        
        Args:
            tag: Optional tag filter
        
        Returns:
            List of credential metadata
        """
        if not self.vault_file.exists():
            return []
        
        vault_data = self._read_vault()
        results = []
        
        for key_name, entry in vault_data["entries"].items():
            metadata = entry["metadata"]
            
            # Filter by tag if specified
            if tag and tag not in metadata.get("tags", []):
                continue
            
            results.append({
                "name": key_name,
                "tags": metadata.get("tags", []),
                "expires": metadata.get("expires"),
                "created": metadata.get("created"),
                "modified": metadata.get("modified")
            })
        
        return results
    
    def remove(self, key_name: str) -> None:
        """Remove a credential.
        
        Args:
            key_name: Name of the credential
        
        Raises:
            VaultLocked: If vault is locked
            KeyError: If credential not found
        """
        session_key = self._ensure_unlocked()
        vault_data = self._read_vault()
        
        if key_name not in vault_data["entries"]:
            raise KeyError(f"Credential not found: {key_name}")
        
        del vault_data["entries"][key_name]
        self._write_vault(vault_data)
        print(f"🗑️  Removed credential: {key_name}")
    
    def status(self) -> Dict[str, Any]:
        """Get vault status information.
        
        Returns:
            Dict with vault status
        """
        if not self.vault_file.exists():
            return {
                "initialized": False,
                "locked": True,
                "count": 0
            }
        
        vault_data = self._read_vault()
        return {
            "initialized": True,
            "locked": not self.is_unlocked(),
            "count": len(vault_data["entries"]),
            "path": str(self.vault_file)
        }
    
    def _read_vault(self) -> Dict[str, Any]:
        """Read vault file."""
        with open(self.vault_file, 'r') as f:
            return json.load(f)
    
    def _write_vault(self, data: Dict[str, Any]) -> None:
        """Write vault file."""
        with open(self.vault_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Secure permissions (owner read/write only)
        os.chmod(self.vault_file, 0o600)
