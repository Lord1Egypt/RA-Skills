---
name: a2a-e2ee-encryption
description: |
  Implements end-to-end encryption (E2EE) utilities for secure A2A (Agent-to-Agent)
  communication. Provides key generation, message encryption/decryption, and key
  management capabilities.

  **Trigger scenarios:**
  - User asks about E2EE implementation for agent communication
  - Need to encrypt messages between agents
  - Key management for secure A2A channels
  - Implementing secure communication protocols
---

# A2A End-to-End Encryption

Provides encryption utilities for secure agent-to-agent communication.

## Features

- **Key Generation**: RSA key pair generation for asymmetric encryption
- **Message Encryption**: Encrypt messages with recipient's public key
- **Message Decryption**: Decrypt messages with own private key
- **Key Exchange**: Secure key exchange protocols
- **Key Rotation**: Automatic key rotation support
- **Message Integrity**: HMAC-based message authentication

## Usage

```javascript
const e2ee = require('./skills/a2a-e2ee-encryption');

// Generate key pair
const keyPair = e2ee.generateKeyPair();

// Encrypt message
const encrypted = e2ee.encrypt('secret message', recipientPublicKey);

// Decrypt message
const decrypted = e2ee.decrypt(encrypted, privateKey);

// Export/Import keys
const exported = e2ee.exportKey(keyPair.publicKey);
const imported = e2ee.importKey(exported);
```

## Architecture

```
┌─────────────┐                    ┌─────────────┐
│   Agent A   │                    │   Agent B   │
│             │                    │             │
│ Private Key │                    │ Private Key │
│ Public Key  │◄──── Exchange ────►│ Public Key  │
│             │                    │             │
│ Encrypt     │──── Encrypted ────►│ Decrypt     │
│ with B's    │      Message       │ with A's    │
│ Public Key  │                    │ Public Key  │
└─────────────┘                    └─────────────┘
```

## Security Considerations

1. **Key Storage**: Private keys should be stored securely (env vars, vault)
2. **Key Rotation**: Rotate keys periodically for forward secrecy
3. **Key Validation**: Always verify key fingerprints before use
4. **Message Size**: Large messages should use hybrid encryption
