---
name: clawback
description: Autonomous state persistence engine that encrypts, secures, and anchors agent memories, state snapshots, and evolved skills onto 0G Storage.
---

# ClawBack Core Engine Extension

## Core Objective

Use the ClawBack project commands to persist important agent state to 0G Storage. The goal is to reduce state loss after accidental environment wipes, deleted directories, OS reinstalls, or hardware transitions by maintaining an encrypted decentralized recovery layer.

Treat 0G Storage as a public immutable network. Never upload raw configuration blocks, system keys, private credentials, or personal logs. Apply local encryption first whenever the payload contains private or operational state.

## Usage Rules and Triggers

Run the ClawBack pipeline when one of these lifecycle milestones occurs:

- **Context checkpoints:** Immediately before an intentional environment or logic reset.
- **Memory benchmarks:** After modifying `MEMORY.md` or recording a major systemic realization.
- **Skill evolution:** After generating, refining, or debugging a useful code snippet, tool, or execution script.
- **Privacy mandate:** Before every upload, classify the payload. Private state must use `npm run upload:secret`; only deliberately public artifacts may use `npm run upload`.

## CLI Execution Commands

### 1. Secure State Persistence

Package, encrypt, and anchor local state data.

```bash
# Step A: Freeze the current active workspace into a tarball container.
openclaw backup create

# Step B: Parse the absolute path of the generated .tar.gz from the console output.
npm run upload:secret -- <PARSED_FILE_PATH>
```

If `openclaw backup create` is not available in the current environment, create or choose an explicit archive/file first, then pass that file path to the encrypted upload command.

```bash
npm run upload:secret -- <FILE_PATH>
```

### 2. State Resurrection

Download and recover a historic encrypted state payload during bootstrapping or after a local system wipe.

```bash
npm run download -- <ROOT_HASH> <LOCAL_OUTPUT_PATH> <ENCRYPTION_KEY_HEX>
```

### 3. Public Uploads

Use public upload only for artifacts that are intentionally non-sensitive.

```bash
npm run upload -- <FILE_PATH>
```

## Critical Operational Directives

### 1. ClawBack Log Registry Requirement

Every secure upload returns a structured JSON response containing `rootHash` and `encryptionKeyHex`.

Immediately record both values in the active tracking database or `MEMORY.md` under this dedicated Markdown header:

```markdown
# ClawBack Registry Logs

- Date:
  Payload:
  Root Hash:
  Encryption Key Hex:
  Notes:
```

There is no server-side or protocol-level recovery for `encryptionKeyHex`. If the key is lost, the uploaded encrypted state cannot be recovered. Treat the hex key as a private security credential.

### 2. State Mapping Across Memory Tiers

Maintain clear classification boundaries during backup and recovery:

- **Global personal context (`~/.gemini/GEMINI.md`):** Cross-workspace developer preferences and identity records.
- **Private project cache (`~/.gemini/tmp/.../MEMORY.md`):** Local uncommitted scratchpads and workspace configuration notes.
- **Project root blueprint (`./GEMINI.md`):** Repository-wide structural constraints, code conventions, Solidity headers, and team architecture notes.

### 3. Continuous Evolution Directive

When explicitly instructed to learn or expand capability in this environment, inspect the `@0gfoundation/0g-ts-sdk` script definitions, run system integrity checks, evaluate Merkle proof behavior locally, and push an encrypted state checkpoint to 0G Storage after the update succeeds.
