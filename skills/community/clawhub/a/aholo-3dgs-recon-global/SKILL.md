---
name: aholo-3dgs-reconstruction-global
description: "Aholo OpenAPI v1 global 3D tasks (reconstruction/generation): upload, create (worldId), poll/status. Gateway api.aholo3d.com, /global/world/v1. Default one create per single intent; multiple creates allowed when user explicitly chooses separate 3DGS per video. Not for 2D."
---

# Aholo 3D Reconstruction Skill — Global (OpenAPI v1)

> **Aholo global Open Platform** (`api.aholo3d.com`). Agent runs `aholo_reconstruct.py`; user sets `AHOLO_API_KEY` only.

## 1. When to use

**Use:** 3D reconstruction, 3D generation, `worldId` status/poll, PLY/SPZ/SOG.

**Do not use:** 2D renders only; no 3D outcome requested.

**Ambiguous requests:** Clarify 2D single image vs 3D task (worldId + poll). Example: "generate a room from a reference image" → ask whether the user wants a 2D single render or a 3D task (worldId, pollable). Enter this skill only if user picks 3D.

## 2. Prerequisites & API

| Item | Detail |
|------|--------|
| Env | `AHOLO_API_KEY` — [api-keys](https://labs.aholo3d.com/api-keys) |
| Auth | `Authorization: <API Key>`, no `Bearer` |
| Create header | `x-source: skills` → platform `OPEN_API_SKILL` |
| Gateway | `https://api.aholo3d.com`; upload token `GET /global/asset/v1/token`; world tasks `/global/world/v1/*` |
| Viewer | `https://studio.aholo3d.com/3dgs-model/{worldId}` |
| Actions | `create` / `create-reconstruction` / `create-generation` / `status` / `poll` / `list` |
| Create success | `WorldAsyncOperation` contains `worldId` only |
| Credits `11003` | Say insufficient credits; link [www.aholo3d.com/pricing](https://www.aholo3d.com/pricing); no invented URLs; **no** `create*` retry for **same video / same intent** |

**Missing API key:** Tell user to set env and reply **continue**; agent runs script — do not make manual `python` the main path.

### TLS (script default behavior)

- Script **enables** SSL verification by default (secure by default).
- Corporate/self-signed certs: set `AHOLO_INSECURE_SKIP_VERIFY=1` (or `true` / `yes` / `on`) to explicitly disable verification; prefer `REQUESTS_CA_BUNDLE` to point at your enterprise CA.
- On `CERTIFICATE_VERIFY_FAILED`, configure CA certs first; use `AHOLO_INSECURE_SKIP_VERIFY` only when you accept the risk.

### Responses & errors

- **OpenAPI success:** HTTP 200; create returns JSON `WorldAsyncOperation` with `worldId` only.
- **OpenAPI failure:** HTTP 4xx/5xx, body is `ApiError`: `code`, `message`, `status`, `details.metaData.bizCode` (e.g. `10004` not authenticated, `11003` insufficient credits).
- **OUS upload:** asset upload uses the upload domain returned by the token endpoint.

## 3. Agent hard constraints (mandatory)

| # | Rule |
|---|------|
| 0 | 2D-only → **no** create/status/poll from this skill |
| 7 | Unclear 3D intent → 2D/3D clarify first (§1) |
| 1–3 | **Reconstruction only:** need confirmed `scene` (`model`/`space`) + `taskQuality` (`low`/`normal`/`high`) before create; **no** defaults (e.g. `high`/`model`) placed on behalf of the user |
| 1–4 | **Reconstruction only:** the initial `AskQuestion` round **must simultaneously include** the `useMask` option (note: "only effective when `scene=model`; ignored when `scene=space`"); **never** default to `false` silently; **never** defer to a second round |
| 4 | **Generation:** do **not** ask `scene`/`taskQuality`; create when `prompt`/image ready |
| 8 | Image folder → use **`imageDir`** for all images; never upload a subset only |
| 11 | **Multiple videos:** ask before create (**do not** choose for user): **A** one 3DGS (one create, all in `videoPaths`); **B** one 3DGS per video (see #9). Only 1 video → skip question |
| 9 | **Create POST (high cost)** — **Default:** one user **single** 3D intent → at most **one** create per conversation round; no retry on same intent after fail/timeout/missing `worldId` unless user **explicitly re-orders**. **Pre-upload failure** (POST not sent) → one first create after fix. **Charged but no worldId** → task list / status/list, not another create. **Multi-video B:** user chose separate 3DGS → create **per video** (`videoPaths` one each), warn N tasks/charges upfront; **no** duplicate create for same video; failed video → no retry, continue with remaining. Use `forbidCreate` only to block accidental **duplicate for the same completed task**, not the next video in B |
| 10 | `projectName` only if user explicitly asks; never invent from folder name or timestamp |
| 5–6 | After each `worldId` → **ask** wait or not; if wait → **sync** `poll` (`intervalSeconds=60`, `timeoutSeconds=14400`); if not → link only. **No** background poll + "I'll notify you"; **no** poll without asking |

### `taskQuality` display names (API values unchanged)

| Value | Display |
|-------|---------|
| `low` | Fast Preview (极速预览) |
| `normal` | Standard (标准) |
| `high` | Professional — recommended (专业，推荐) |

## 4. Standard flow

1. Applicability + 2D/3D (§1).
2. `reconstruction` vs `generation`.
3. **Reconstruction:** `AskQuestion` first — **confirm `scene`, `taskQuality`, and `useMask` in one round** (§5 table); normalize free text before confirming; **do not split into two rounds**.
4. **Multiple videos (2+):** A merge vs B separate (§5 template).
5. token → upload → create (§3 #9, #11).
6. Record `worldId`; ask wait (§5 template).
7. Wait → sync `poll`; else link only.
8. No further create same round except **new order** or **next video** in B (§3 #9).

## 5. User prompts

**Reconstruction — initial confirm (scene, taskQuality, useMask — one round, do not split):**

Use `AskQuestion` with all three questions simultaneously:

| Question | Options |
|----------|---------|
| scene | `model` (object) / `space` (scene) |
| taskQuality | `low` Fast Preview / `normal` Standard / `high` Professional (recommended) |
| useMask | Enable (auto background removal, best for plain backgrounds) / Disable (keep original background, default) — **only effective when `scene=model`; ignored when `scene=space`** |

**Multiple videos:**

```text
You provided N videos. Choose (I will not choose for you):
A) One 3DGS — one worldId
B) Separate 3DGS per video — N worldIds (N tasks, processed one video at a time)
```

**After create:**

```text
Task created, worldId: {worldId}
View when ready: https://studio.aholo3d.com/3dgs-model/{worldId}
(Link may not be accessible until the task completes)

Wait until complete?
- wait / yes — sync poll in this session
- no — poll later or open the link yourself
```

## 6. Task rules & parameters

### reconstruction

- `videoPaths` (no fixed limit) **or** `imagePaths`/`imageDir` (≥20 images), pick one
  - `.mp4` / `.mov` → `type=video`; `.insv` (Insta360 panoramic video) → `type=insv`; detected automatically from extension
- Required: `scene`, `taskQuality`
- Optional: `useMask` (boolean; auto background removal; **only effective when `scene=model`**; default `false`; ignored when `scene=space`)
- `imageDir` scans jpg/jpeg/png/webp only (excludes bmp/gif)

### generation

- ≤1 image; `prompt` and image not both empty; no `videoPaths`; no `scene`/`taskQuality`

### Key params

| Param | Description |
|-------|-------------|
| `action` / `workflow` | see §2 actions |
| `imageDir` | preferred for image-folder reconstruction |
| `videoPaths` | no fixed limit; `.insv` auto-detected as `type=insv`, others as `type=video` |
| `useMask` | boolean, background removal (optional; **reconstruction + `scene=model` only**; default `false`) |
| `worldId` | for `status` / `poll` |
| `pageNum` / `pageSize` / `statusList` | `list` pagination params |
| `forbidCreate` | guard against accidental duplicate create for **same task**; do not set for next video in multi-video B |

### Examples (agent runs with `python -u`)

JSON argument on a **single line** as the second argv. See Windows/PowerShell section below for Windows-specific rules.

```bash
# Reconstruction (image directory)
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create","workflow":"reconstruction","imageDir":"D:/images","scene":"space","taskQuality":"high"}'

# Reconstruction (Insta360 panoramic video, auto-detected as type=insv)
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create","workflow":"reconstruction","videoPaths":["D:/room.insv"],"scene":"space","taskQuality":"high"}'

# Reconstruction (with background removal)
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create","workflow":"reconstruction","videoPaths":["D:/obj.mp4"],"scene":"model","taskQuality":"normal","useMask":true}'

# Generation
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create-generation","imagePaths":["D:/seed.jpg"],"prompt":"modern minimal interior"}'

# Poll
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"poll","worldId":"xxx","intervalSeconds":60,"timeoutSeconds":14400}'

# List (running + succeeded)
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"list","pageNum":0,"pageSize":20,"statusList":["RUNNING","SUCCEEDED"]}'
```

### Windows / PowerShell (agent must read)

When the user is on **Windows**, the agent must follow these rules:

- **Shell:** Use **PowerShell** by default; **no** bash syntax (e.g. `&&` chaining); use `;` to separate commands, or issue one `python -u ...` at a time.
- **JSON arg:** Put the entire JSON on a **single line** wrapped in **single quotes** as the second argument; **never** break it across multiple lines (PowerShell will split arguments).
- **Paths:** Use forward slashes in Windows paths, e.g. `D:/images/0001.jpg`, to avoid unescaped backslash issues.
- **Working directory:** Run from the repo root or the directory containing `.cursor/skills/aholo-3dgs-reconstruction-global/`.
- **Output:** Always include `-u` so create/upload/poll progress streams in real time.
- **User self-debug (optional):** `$env:AHOLO_API_KEY="..."` then the same single-line `python -u ...`; agent-run is still the preferred path.

## 7. Appendix

**API paths:** `GET /global/asset/v1/token` · `POST /global/world/v1/reconstructions` · `POST /global/world/v1/generations` · `GET /global/world/v1/{worldId}` · `POST /global/world/v1/list` · OUS upload uses domain from token response (no `/global` prefix on OUS)

**Terminal states:** `SUCCEEDED` · `FAILED` · `CANCELED` · `TIMEOUT` · `REJECTED`

**Output fields (after SUCCEEDED):** `plyPath` · `spzPath` · `lodMetaPath` (LOD chunk metadata, optional) · `panoUrl` (AI panorama, generation only)

### Local debug (optional)

```powershell
$env:AHOLO_API_KEY="your_api_key"
# Self-signed certs (not recommended): $env:AHOLO_INSECURE_SKIP_VERIFY="1"
# Or set CA bundle: $env:REQUESTS_CA_BUNDLE="D:/certs/corp-ca.pem"
```

Agent-run is preferred; user sets the key and replies **continue**.
