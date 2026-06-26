# Birth System Manager Skill

Manages OpenClaw agent birth encoding, migration packing/unpacking, identity verification, secure wallet decryption, and **full family tree lineage tracking** for agent cloning with parent-child relationships.

## Features

- **Birth Init**: Generate unique Birth ID for new instances with Ethereum wallet and cryptographic signature
- **Pack Instance**: Bundle current OpenClaw instance for migration (encrypts sensitive data with password)
- **Unpack Clone**: Install cloned instances from migration packages
- **Initialize Clone**: Mark unpacked instance as clone with new birth ID and parent lineage tracking
- **Whoami**: View agent birth identity, lineage, family tree, and verification status
- **Decrypt Wallet**: Securely decrypt wallet private key with password
- **Family Tree**: View complete ancestor chain with generation tracking
- **Fix Clone**: Manually fix clone identity when clone-init was missed after unpacking

## Installation

Via ClawHub:
```bash
clawhub install birth-system-manager
```

## Usage

In OpenClaw chat, use natural language commands:

### Birth Initialization (New Instances)

- **Initialize birth system**: "birth init" or "出生认证"
- **Generate Birth ID**: "generate birth id" or "初始化出生系统"

**⚠️ Important**: For new OpenClaw installations, run birth initialization first:
```bash
node ~/.openclaw/birth-system/generate-birth-id.js
```

This generates a unique Birth ID (DID) using Ethereum, creates a wallet for cryptographic proof, and sets up signature verification.

### Migration & Cloning

- **Pack for migration**: "pack my instance" or "打包迁移"
- **Unpack clone**: "unpack ~/Downloads/openclaw-lobster-pack.tar.gz"
- **Initialize clone**: "mark as clone" or "init clone"

**⚠️ Important**: After unpacking, ALWAYS mark as clone:
```bash
export IS_CLONE=true
node ~/.openclaw/birth-system/clone-init.js
```

This generates a new birth ID, sets parent ID, and builds the family tree.

### Identity & Lineage

- **View identity**: "whoami" or "我的身份"
- **View family tree**: "family tree" or "家族树" (shows complete ancestor chain)
- **Decrypt wallet**: "decrypt wallet with password"
- **Fix clone**: "fix clone" or "修复克隆" (if clone-init was missed)

### Environment Variables

- `BIRTH_PRIVATE_KEY_PASSWORD`: Password for wallet decryption (preferred over CLI args)
- `BIRTH_PACK_PASSWORD`: Default password for packing (CLI args override this)
- `IS_CLONE=true`: Required when initializing a clone instance

## Architecture

The birth system provides unique agent identity and tracks clone lineage with family tree:

1. **Birth ID**: Unique identifier for each agent instance
2. **Type**: "original" or "clone"
3. **Parent ID**: Birth ID of parent instance (null for originals)
4. **Ancestors**: Array tracking complete lineage chain
5. **Clone Suffix**: Random hex string identifying this specific clone
6. **Wallet**: Ethereum wallet for cryptographic proof of identity
7. **Signature**: Cryptographic signature for authenticity verification

## Family Tree Example

After cloning, `whoami` output shows complete lineage:

```
🧬 Lineage / Family Tree:
   📌 did:ethr:...-clone-a1b2c3d4
      Type: Clone
      ├─ did:ethr:0xF80042413226cf4a5F1b7de458Cf0EEd19237662 [Original]
        Created: 2026-03-06 16:20:57
```

Multi-generation clones show full ancestor chain with each level.

## Fixing Clone Identity

If you forgot to run `clone-init.js` after unpacking, use `fix-clone.js` to manually specify the parent birth ID:

```bash
# 1. Extract parent birth ID from the original package
mkdir -p /tmp/extract
tar -xzf ~/Desktop/birth-pack-xxx.tar.gz -C /tmp/extract ./.openclaw/birth-info.json
cat /tmp/extract/.openclaw/birth-info.json | grep birth_id

# 2. Run fix-clone with the parent birth ID
node ~/.openclaw/birth-system/fix-clone.js <parent_birth_id> --auto

# Example:
node ~/.openclaw/birth-system/fix-clone.js did:ethr:0xF80042413226cf4a5F1b7de458Cf0EEd19237662 --auto
```

This will generate a new clone birth ID, set the parent_id, and update the family tree.

## Security Notes

- All operations run locally; no network calls
- Passwords should be provided via environment variables, not CLI args where possible
- Never commit `birth-info.json` to version control (contains encrypted keys)
- Review code before use in production environments
- Family tree data is stored locally in `birth-info.json`

## Version History

### v1.2.0 (Current)
- ✨ Added `generate-birth-id.js` for birth initialization of new instances
- ✨ Automatic clone detection via IS_CLONE environment variable
- ✨ Generates unique Birth IDs using Ethereum DID
- ✨ Creates cryptographic wallet for signature verification
- ✨ Validates existing Birth IDs to prevent tampering

### v1.1.1
- 🔧 Added `fix-clone.js` tool to manually fix clone identity when clone-init was missed
- 🔧 Supports manual parent_id specification for fixing cloning mistakes
- 🔧 Includes clone_fixed_at timestamp for tracking repairs

### v1.1.0
- ✨ Added full family tree lineage tracking with parent-child relationships
- ✨ New `clone-init.js` script for proper clone initialization
- ✨ Enhanced `whoami.js` with family tree visualization
- ✨ Support for ancestors array and generation tracking

### v1.0.0
- Initial release with pack/unpack/whoami/decrypt-wallet features

## License

MIT License - see LICENSE file
