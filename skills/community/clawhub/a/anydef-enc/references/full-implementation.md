# Local Encryption Architecture

The `anydef-enc` skill is a privacy-first encryption toolkit.

## Zero Knowledge Logic

1.  **Reboot & Persistence**:
    -   When you first set a passphrase, we generate a random 16-byte **Salt**.
    -   We store this **Salt** in `window.storage.get("enc-vault-salt")`.
    -   When you reboot, we combine your passphrase with this saved Salt to recreate the **exact SAME Master Key**.
    -   This allows the Master Key to unwrap your existing **KEK** and Access your data.

2.  **Why this is Secure**:
    -   Even if a hacker gets your browser storage data, they only have the Salt, the Wrapped KEK, and the Wrapped DEKs.
    -   Without the **Passphrase**, they cannot derive the Master Key.
    -   Since the Master Key is never stored (only derived and held in memory), the data is safe while the vault is locked.

## Encryption Standards
-   **Derivation**: PBKDF2-HMAC-SHA256 (100,000 rounds).
-   **Cipher**: AES-GCM (256-bit).
-   **IV**: 12-byte random IV per operation.
