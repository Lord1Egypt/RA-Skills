---
name: "backendenc"
description: "Backend Agent Data Encryption. High-security MK->KEK->DEK hierarchy for backend environments."
---

# backendenc: Backend Security Toolkit

This skill provides mandatory encryption for OpenClaw agents running in **Node.js/Backend** environments. It operates in **Local Manual Mode**, using the Node.js built-in `crypto` module.

## Context
Unlike the frontend version which uses Web Crypto, this version is designed for server-side execution, CLI tools, or background agents. It stores metadata in a persistent local file (or compatible storage provider).

## Key Hierarchy

1.  **Master Key (MK)**: Derived from your passphrase using `crypto.pbkdf2`. 
    *   **Persistence**: A unique "Salt" is stored in your configuration. As long as you remember your passphrase, the same Master Key will be generated across reboots.
2.  **Key Encryption Key (KEK)**: Generated randomly and encrypted by your MK.
3.  **Data Encryption Keys (DEKs)**: Scoped keys (e.g., `memory`, `assets`) encrypted by the KEK.

## Security Disclosure

-   **Zero Network**: This skill does NOT perform any external network requests. All operations happen via the Node.js `crypto` module.
-   **No Cleartext Keys**: Keys are never stored in cleartext. They are always "wrapped" (encrypted) by a higher-level key using AES-256-GCM.
-   **Passphrase Obligation**: You must provide your passphrase to "unlock" the vault after هر server reboot.

## Multi-User & Channel Isolation

Designed for high-concurrency backend environments:
-   **Key Partitioning**: All storage keys follow the `${userId}:${channelId}:key` format.
-   **Security**: Ensures that even if the underlying storage file is compromised, keys for different users remain cryptographically separated.

## Usage (Backend)

```javascript
import { EncryptionService } from './encryption-service.js';

// Access context IDs
const { userId, channelId } = agent.context;

// Unlock for context
await EncryptionService.unlock(userId, channelId, 'passphrase');

// Scoped encryption
const encrypted = await EncryptionService.encrypt(userId, channelId, 'history', 'data');
```
