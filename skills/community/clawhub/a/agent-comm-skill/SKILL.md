# Agent Communication Skill (PassDeck)

This skill provides the security and networking foundation for AI Agent swarms. It handles DID (Decentralized Identity) registration, cryptographically secure signing using Ed25519, and E2EE (End-to-End Encryption) for sensitive data.

## 🚀 Key Actions

### `agent.register`
- **Description**: Registers a new local agent identity or restores an existing one. Returns the agent's unique DID.
- **Parameters**: `{ alias?: string }`
- **Output**: `{ localId: string, did: string, publicKey: hex }`

### `message.sign`
- **Description**: Signs a payload using the agent's private key. Ensures data integrity and non-repudiation.
- **Parameters**: `{ localId: string, payload: any }`
- **Output**: `{ signature: hex }`

### `message.verify`
- **Description**: Verifies a signed message against a public key. Used to detect data tampering or unauthorized updates.
- **Parameters**: `{ publicKeyHex: string, payload: any, signatureHex: string }`
- **Output**: `{ verified: boolean }`

### `network.connect`
- **Description**: Establishes an authorized connection to a Relay server. Implements a DID challenge-response handshake.
- **Parameters**: `{ sessionId: string, localId: string, did: string, onUpdate: function }`
- **Output**: `{ success: true }`

### `secret.encrypt / secret.decrypt`
- **Description**: High-level E2EE functions for managing secure credentials within the collaborative pool.
- **Parameters**: `{ payload/ciphertext: any, sessionKey: string }`
- **Output**: `{ ciphertext/decrypted: any }`
