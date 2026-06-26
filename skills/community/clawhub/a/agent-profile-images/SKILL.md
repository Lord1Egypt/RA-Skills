---
name: agent-profile-images
version: 1.0.0
author: Charles Sears
description: "Agent Profile Images for OpenClaw Control UI — upload custom avatars, generate themed AI profile images, preview before saving, and persist agent avatars across refreshes."
---

# agent-profile-images

**name:** agent-profile-images  
**version:** 1.0.0  
**author:** Charles Sears  
**description:** Adds agent profile image upload, AI generation, preview/keep-regenerate-cancel flow, and avatar persistence fixes to the OpenClaw Control UI.

---

## What This Skill Adds

### 1. Agent Profile Image Card in Agents → Overview
Adds a dedicated **Profile Image** section to the Agents Overview panel with:
- current avatar preview
- upload button
- remove button
- theme selector
- custom generation instructions
- generate button
- preview state messaging

### 2. Avatar Upload RPC
Adds `agents.avatar.upload` so the Control UI can upload a PNG/JPG/WEBP/GIF image and save it into the agent workspace.

### 3. AI Avatar Generation RPC
Adds `agents.avatar.generate` for themed image generation using OpenAI Images.

### 4. Preview / Keep / Regenerate / Cancel Loop
Generation does **not** auto-save. Instead:
- **Generate** → preview only
- **Keep** → saves generated image as the agent avatar
- **Regenerate** → requests a new preview
- **Cancel** → discards preview and preserves the previous avatar

### 5. Persistent Avatar Resolution
Fixes the gateway agent-list/session-utils path so avatar information from workspace `IDENTITY.md` is reflected correctly across Agents UI, chat UI, refreshes, and reloads.

### 6. Fresh Identity Reloads on Agents Tab
Fixes stale UI state by forcing the Agents tab to refresh identity data when entering the tab and after avatar-changing actions.

---

## Backend Methods Added

| Method | Description |
|---|---|
| `agents.avatar.upload` | Upload and save a profile image into the agent workspace |
| `agents.avatar.generate` | Generate a themed avatar preview using OpenAI Images |
| `agents.avatar.remove` | Remove the current stored avatar |

---

## Theme Presets Included

- Professional
- Sci-Fi
- Cyberpunk
- Fantasy
- Space Opera
- Creature Collector
- Mascot
- Noir

---

## Storage Model

Saved avatars are written into the agent workspace under `avatars/` and persisted via `IDENTITY.md` using:

```md
- Avatar: avatars/profile.png
```

This reuses the existing Control UI avatar serving path (`/avatar/:agentId`) and keeps images portable with the agent workspace.

---

## Files Included

The `references/` folder contains the feature implementation snapshots for these files:

- `src/gateway/method-scopes.ts`
- `src/gateway/protocol/index.ts`
- `src/gateway/protocol/schema/agent.ts`
- `src/gateway/protocol/schema/agents-models-skills.ts`
- `src/gateway/protocol/schema/protocol-schemas.ts`
- `src/gateway/protocol/schema/types.ts`
- `src/gateway/server-methods-list.ts`
- `src/gateway/server-methods/agent.ts`
- `src/gateway/server-methods/agents.ts`
- `src/gateway/session-utils.ts`
- `ui/src/ui/app-render.ts`
- `ui/src/ui/app-view-state.ts`
- `ui/src/ui/app.ts`
- `ui/src/ui/types.ts`
- `ui/src/ui/views/agents-panels-overview.ts`
- `ui/src/ui/views/agents.ts`

---

## Notes

- This skill packages the **source-level feature implementation**.
- A temporary live compiled-bundle hotfix was used during development to unblock testing, but that tactical dist patch is **not** part of this skill package.
- OpenAI image generation is currently the implemented provider path in this package.
- The full OpenClaw repo may contain unrelated build/runtime issues outside this feature; this skill is scoped only to agent profile image functionality.

---

## Recommended Publish Changelog

```text
Initial release: agent profile image upload, themed AI generation, preview/keep-regenerate-cancel loop, and refresh-state fixes.
```
