---
name: "anydef-enc"
description: "Local-Only Agent Data Encryption. High-security MK->KEK->DEK hierarchy for local agent data."
---

# anydef-enc: Local Security Toolkit

This skill provides mandatory encryption for OpenClaw agents. It operates in **Local Manual Mode**, meaning no external network requests are made, and encryption keys are derived from a user passphrase.

## Key Hierarchy

1.  **Master Key (MK)**: Derived from your passphrase using PBKDF2 (100,000 iterations). 
    *   **Persistence**: A unique "Salt" is stored in your environment. As long as you remember your passphrase, the same Master Key will be generated across reboots.
2.  **Key Encryption Key (KEK)**: Generated randomly and encrypted by your MK. Stored in `window.storage`.
3.  **Data Encryption Keys (DEKs)**: Scoped keys (e.g., `memory`, `assets`) encrypted by the KEK and stored in `window.storage`.

## Security Disclosure

-   **Zero Network**: This skill does NOT perform any external network requests. All `crypto` operations happen via standard Web APIs in your browser.
-   **No Cleartext Keys**: Keys are never stored in cleartext. They are always "wrapped" (encrypted) by a higher-level key.
-   **Passphrase Obligation**: You must provide your passphrase to "unlock" the vault after هر reboot or session expiry. If you forget your passphrase, existing encrypted data is **lost forever**.

## Selective Encryption

Configure which scopes to protect in your settings:
-   `history`: Conversation logs.
-   `memory`: Agent's semantic memory.
-   `assets`: All uploaded files.

## Usage

```javascript
import { EncryptionService } from './encryption-service.js';

// Unlock once per session
await EncryptionService.unlock('your-passphrase');

// Use throughout the session
const secretData = await EncryptionService.encrypt('memory', 'Sensitive intelligence...');
```
