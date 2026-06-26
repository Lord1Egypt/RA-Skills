---
name: agentcadia-tools
description: Upload or download Agentcadia agent drafts with one skill. Supports two command-style flows: `upload` (sync a local OpenClaw-style workspace into Agentcadia, including required metadata writeback) and `download` (pull an Agentcadia agent package into a local workspace). Use when the user has an Agentcadia upload taskId, download token, or copied automation instruction and wants a deterministic file-transfer workflow.
---

# Agentcadia Tools

A unified Agentcadia skill for **uploading** and **downloading** agent workspaces.

## Core rule

This skill exposes two explicit command-style actions:

- `upload`
- `download`

Always decide which action the user needs, then run the matching subcommand through the unified script:

```bash
python3 scripts/agentcadia_tools.py upload ...
python3 scripts/agentcadia_tools.py download ...
```

Do not invent alternative flows when the bundled scripts already cover the task.

---

## Action: upload

Use `upload` when the user wants to sync the current local workspace into an Agentcadia draft.

### Required workflow

A successful upload must include **all** of these phases:

1. upload workspace markdown + packaged skills
2. generate draft metadata from the uploaded agent workspace
3. write that metadata back to Agentcadia
4. send the owner a standalone metadata-summary message containing the exact metadata that was written back
5. when a share image is available, send that share image to the owner as a separate image message

If you skip metadata writeback and only provide “suggested copy”, the task is **not complete**.

### Metadata synthesis rules

Generate metadata from the workspace itself.

Prefer agent-level sources such as:

- `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, and `TOOLS.md` (combine these to infer the agent’s name, personality, self-introduction, intended audience, and operating context)
- README-like files
- persona / workflow / intro files
- other root markdown that describes the whole workspace

Quality bar:

- `summary` must read like a short product intro for the agent
- `detailDescription` must expand on positioning, scenarios, and value
- do not write generic template copy
- do not write “uploaded workspace”, “packaged skills”, or similar process-language as the user-facing description
- explicitly synthesize from `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, and `TOOLS.md`
- do not block on `agent.md`, `AGENT.md`, or `agent_download.md`
- do not ask the owner to provide title/summary/detailDescription/category/tags first unless the workspace is genuinely too sparse; even then, present your best draft first

Required metadata fields:

- `title`
- `summary`
- `detailDescription`
- `description`
- `category`
- `tags`

### Upload command

Generate metadata first, save it as a temporary JSON file, then run:

```bash
python3 scripts/agentcadia_tools.py upload \
  --task-id <taskId> \
  --origin <origin> \
  --workspace <workspacePath> \
  --metadata-file <tempMetadataJsonPath>
```

Treat uploader output as authoritative.

If the script returns:

- `success: false`
- or `metadataWritebackSucceeded: false`
- or `incompleteReason: METADATA_WRITEBACK_REQUIRED`

then the upload is **not complete**, even if files were uploaded.

### Owner delivery rules for upload

After upload succeeds, deliver owner-facing output in two separate steps:

1. **Metadata summary message first**
   - Send a standalone text message containing at least: title, category, tags, summary, detailDescription, workspace path used, uploaded markdown files, and uploaded skill packages.
   - Do not merge this into the share-image caption only. The owner must be able to read the written metadata as a separate message.

2. **Share image message second**
   - If a share image is available, send it as a real image message to the owner.
   - Do not stop at sending only `agentUrl` or `shareImageUrl` as plain text.
   - If the runtime can send images only from local files, download the share image first, save it to a temporary local path, then send that local image file.
   - The final owner-visible step should be the image message, not a plain text link.

### Upload completion rules

- upload ok + metadata writeback ok + metadata summary message sent + share image sent as an image when available = complete
- upload ok + metadata writeback failed = partial success, not complete
- upload ok + metadata ok + metadata summary not sent = partial success, not complete
- upload ok + metadata ok + share image available but not sent as an image = partial success, not complete
- upload failed = failed

---

## Action: download

Use `download` when the user wants to pull an Agentcadia agent package into the local workspace.

### Download behavior

The download flow should:

1. determine the target workspace path
2. download the agent package with the provided bearer token
3. extract or place the files into the workspace
4. report all placed files and any conflicts
5. clean up temporary files

Do not overwrite existing files unless the user explicitly asked for it.

### Download command

```bash
python3 scripts/agentcadia_tools.py download \
  --agent-id <agentId> \
  --token <downloadToken> \
  --origin <origin> \
  --workspace <workspacePath>
```

If the user explicitly approved overwriting existing files, add:

```bash
--allow-overwrite
```

### Download reporting rules

Always report:

- workspace path used
- whether the payload was zip or markdown
- files placed or extracted
- conflicts skipped because overwrite was not allowed

If any conflicts were skipped, treat the result as partial and tell the user exactly which files need a decision.

---

## Runtime notes

When upload returns a share image, sending that image to the owner is mandatory unless the runtime truly cannot send images. The owner-facing metadata summary and the share image must be sent as two separate messages, with the image sent last.

See `references/openclaw-runtime.md` for OpenClaw-oriented owner-delivery behavior.

## Boundaries

- Use this skill for deterministic file sync, not final publish approval
- Never expose upload tokens or internal upload URLs in user-visible output
- Stop and report clearly if a packaged skill exceeds size limits
- Do not fabricate share assets if the server did not return them
- Do not overwrite existing local files during download unless the user explicitly approved it
