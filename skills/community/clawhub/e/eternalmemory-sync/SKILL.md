---
slug: memory-sync
display_name: EternalClaw Memory Sync
description: Securely backup and restore Openclaw agent memory from remote URLs using AES-256-GCM encryption.
author: Applied-Energetic
version: 1.0.0
tags: [memory, sync, backup, encryption, agent-state]
license: MIT-0
---

# EternalClaw Memory Sync

This skill enables Openclaw agents to securely synchronize their memory state from a remote URL. It handles downloading, decrypting with AES-256-GCM, and restoring memory files to ensure seamless context continuity across environments.

## Capabilities

- **Secure Restoration**: Fetch and decrypt memory blobs from a user-provided URL.
- **Cross-Environment Sync**: Transfer agent context securely between different machines or sessions.
- **Local Decryption**: Perform decryption locally using a password-derived key (Argon2id).

## Usage

This skill includes Python scripts that perform the actual restoration logic.

### prerequisites

Ensure the following Python libraries are installed in your environment:

```bash
pip install cryptography requests argon2-cffi
```

### Restore Memory

To restore memory from a backup URL, execute the included script:

```bash
# Execute from project root
python skills/memory-sync/scripts/restore_secure.py --url "<YOUR_BACKUP_URL>" --password "<YOUR_PASSWORD>"
```

*Note: Replace `<YOUR_BACKUP_URL>` and `<YOUR_PASSWORD>` with your actual backup details.*

## Implementation Details

The skill relies on `scripts/restore_secure.py` (included in this package) to handle sensitive cryptographic operations.

1. **Download**: Fetches the encrypted blob from the URL.
2. **Key Derivation**: Derives the decryption key using `Argon2id` and the provided password.
3. **Decryption**: Decrypts the data using `AES-256-GCM` to ensure confidentiality and integrity.
4. **Restoration**: Unpacks the memory files to the current workspace.

## Included Files

- `SKILL.md`: Documentation (this file).
- `scripts/restore_secure.py`: Main restoration script.
- `scripts/crypto_utils.py`: Shared encryption utilities.
