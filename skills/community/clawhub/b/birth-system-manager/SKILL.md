---
name: birth-system-manager
description: Manage birth encoding, migration packing/unpacking, identity whoami, secure wallet decryption, and full family tree lineage tracking for OpenClaw agents with clone parent-child relationships.
version: 1.2.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [node]
    env: []
---

## Skill Instructions

- When user says "birth init", "generate birth id", "出生认证", "初始化出生系统" or similar:
  Run: node {baseDir}/generate-birth-id.js
  This will generate a unique Birth ID for new instances, create an Ethereum wallet, and generate a cryptographic signature.
  If IS_CLONE=true is set, it will automatically generate a clone Birth ID.
  Return the generated Birth ID, wallet address, and signature verification status.

- When user says "pack", "migrate pack", "birth pack", "打包迁移" or similar:
  Ask for password if not provided (use env BIRTH_PRIVATE_KEY_PASSWORD if set).
  Run: node {baseDir}/pack.js [password]
  Return the generated tar.gz path.

- When user says "unpack", "install clone", "解包克隆", "unpack birth-pack" + path:
  Ask for package path and target dir (default ~/openclaw-new-lobster).
  Run: node {baseDir}/unpack.js <path> <target>
  **IMPORTANT**: After unpacking, remind user to mark as clone:
  ```bash
  export IS_CLONE=true
  node ~/.openclaw/birth-system/clone-init.js
  ```
  Or run directly: node {baseDir}/clone-init.js (requires IS_CLONE=true env var)
  This will generate new birth_id, set parent_id, and build family tree.

- When user says "whoami", "birth whoami", "我的身份", "出生信息":
  Run: node {baseDir}/whoami.js
  Return full output including:
  - Birth ID, Type (Original/Clone), Parent ID
  - Full family tree with ancestor chain
  - Creation time, Age
  - Wallet address, Signature verification
  - Clone suffix and ancestor count

- When user says "mark as clone", "init clone", "initialize clone", "标记克隆":
  Check if IS_CLONE=true is set. If not, instruct user to run:
  ```bash
  export IS_CLONE=true
  node {baseDir}/clone-init.js
  ```
  This will:
  - Generate new birth_id (parent_id + '-clone-' + random suffix)
  - Set parent_id to original birth_id
  - Update type to 'clone'
  - Build ancestors array with full lineage
  - Re-sign with new signature
  Return new birth_id and family tree.

- When user says "family tree", "lineage tree", "家族树", "克隆谱系":
  Run: node {baseDir}/whoami.js --verbose
  Return detailed family tree showing complete ancestor chain with creation dates.

- When user says "fix clone", "修复克隆", "补救克隆身份":
  If user missed clone initialization after unpacking, guide them to:
  1. Find parent_birth_id from the original package:
     ```bash
     tar -xzf birth-pack-xxx.tar.gz ./.openclaw/birth-info.json
     cat .openclaw/birth-info.json | grep birth_id
     ```
  2. Run fix-clone with parent ID:
     ```bash
     node {baseDir}/fix-clone.js <parent_birth_id> --auto
     ```
  This will:
  - Generate new birth_id for this instance
  - Set parent_id to the specified parent
  - Update type to 'clone'
  - Build ancestors array
  - Mark the fix timestamp (clone_fixed_at)
  Return updated birth_id and family tree.

- When user says "decrypt wallet", "解密钱包", "show private key":
  Require password (env or ask).
  Run: node {baseDir}/decrypt-wallet.js ~/.openclaw/birth-info.json [password]
  Return ONLY wallet address and success message, NEVER show full private key.

- General: If user asks about "龙虾出生系统", "clone lineage", "birth system":
  Explain it's for unique agent identity and cloning tracking with full family tree lineage tracking.

**Security**: All operations local, no network calls. Passwords via env only.

**Migration Notes**:
- When cloning, ALWAYS set `export IS_CLONE=true` before running `clone-init.js`
- Skipping clone initialization will result in identity being treated as "Original"
- Family tree tracking requires proper clone marking at each generation
