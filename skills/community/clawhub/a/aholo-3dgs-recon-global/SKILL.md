---
name: aholo-3dgs-reconstruction-global
description: "Aholo OpenAPI v1 global 3D tasks (reconstruction/generation): upload, create (worldId), poll/status. Gateway api.aholo3d.com, /global/world/v1. Default one create per single intent; multiple creates allowed when user explicitly chooses separate 3DGS per video. Not for 2D."
---

# Aholo 3D Reconstruction Skill — Global (OpenAPI v1)

> **Aholo global Open Platform** (`api.aholo3d.com`). Agent runs `aholo_reconstruct.py`; user sets `AHOLO_API_KEY` only.

## 1. When to use

**Use:** 3D reconstruction, 3D generation, `worldId` status/poll, PLY/SPZ/SOG.

**Do not use:** 2D renders only; no 3D outcome requested.

**Ambiguous requests:** Clarify 2D single image vs 3D task (worldId + poll). Enter flow only if user picks 3D.

## 2. Prerequisites & API

| Item | Detail |
|------|--------|
| Env | `AHOLO_API_KEY` — [api-keys](https://labs.aholo3d.com/api-keys) |
| Auth | `Authorization: <API Key>`, no `Bearer` |
| Create header | `x-source: skills` → platform `OPEN_API_SKILL` |
| Gateway | `https://api.aholo3d.com`; paths `/global/world/v1/*` |
| Viewer | `https://studio.aholo3d.com/3dgs-model/{worldId}` |
| Actions | `create` / `create-reconstruction` / `create-generation` / `status` / `poll` |
| Credits `11003` | Say insufficient credits; link [labs.aholo3d.com/quickstart](https://labs.aholo3d.com/quickstart); no invented URLs; no `create*` retry for **same video / same intent** |

**Missing API key:** Tell user to set env and reply **continue**; agent runs script — do not make manual `python` the main path.

**TLS:** Verification off by default; `AHOLO_FORCE_SSL_VERIFY=1` to enable.

## 3. Agent hard constraints (mandatory)

| # | Rule |
|---|------|
| 0 | 2D-only → no create/status/poll from this skill |
| 7 | Unclear 3D intent → 2D/3D clarify first (§1) |
| 1–3 | **Reconstruction only:** need confirmed `scene` + `taskQuality`; **no** defaults (e.g. `high`/`model`) |
| 4 | **Generation:** do **not** ask `scene`/`taskQuality`; create when `prompt`/image ready |
| 8 | Image folder → **`imageDir`** for all images; never upload a subset only |
| 11 | **2–3 videos:** ask before create (**do not** choose): **A** one 3DGS (one create, all in `videoPaths`); **B** one 3DGS per video (see #9). One video → skip |
| 9 | **Create POST (high cost)** — **Default:** one user **single** 3D intent → at most **one** create per conversation round; no retry on same intent after fail/timeout/missing `worldId` unless user **explicitly re-orders**. **Pre-upload failure** → one first create after fix. **Charged but no worldId** → task list / status/list, not another create. **Multi-video B:** user chose separate 3DGS → create **per video** (`videoPaths` length 1 each), N creates for N videos (N≤3); warn N tasks/charges upfront; **no** duplicate create for same video; failed video → no retry, continue with remaining. Use `forbidCreate` only to block accidental **duplicate for the same task**, not the next video in B |
| 10 | `projectName` only if user explicitly asks |
| 5–6 | After each `worldId` → **ask** wait or not; if wait → **sync** `poll`; if not → link only. **No** background poll + “I'll notify you”; **no** poll without asking |

### `taskQuality` display (API values unchanged)

| Value | Display |
|-------|---------|
| `low` | Fast Preview (极速预览) |
| `normal` | Standard (标准) |
| `high` | Professional (专业) |

## 4. Standard flow

1. Applicability + 2D/3D (§1).
2. `reconstruction` vs `generation`.
3. **Reconstruction:** confirm `scene` × `taskQuality` (§5 table); normalize free text first.
4. **2–3 videos:** A merge vs B separate (§5).
5. token → upload → create (§3 #9, #11).
6. Record `worldId`; ask wait (§5).
7. Wait → sync `poll` (`intervalSeconds=60`, `timeoutSeconds=14400`); else link only.
8. No further create same round except **new order** or **next video** in B (§3 #9).

## 5. User prompts

**Reconstruction — pick one of 6 (or split questions):**

| # | scene | taskQuality |
|---|-------|-------------|
| 1–3 | model | low / normal / high |
| 4–6 | space | low / normal / high |

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

Wait until complete?
- wait / yes — sync poll in this session
- no — poll later or open the link
```

## 6. Task rules & parameters

### reconstruction

- `videoPaths` (1–3) **or** `imagePaths`/`imageDir` (≥20)
- Required: `scene`, `taskQuality`

### generation

- ≤1 image; prompt and image not both empty; no video; no scene/quality

### Key params

`imageDir` · `videoPaths` (one per create in mode B) · `worldId` · `forbidCreate` (same-task guard only)

### Examples (agent runs with `python -u`)

```bash
python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create","workflow":"reconstruction","imageDir":"D:/images","scene":"space","taskQuality":"high"}'

python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"create-generation","imagePaths":["D:/seed.jpg"],"prompt":"modern minimal interior"}'

python -u .cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py '{"action":"poll","worldId":"xxx","intervalSeconds":60,"timeoutSeconds":14400}'
```

## 7. Appendix

**Paths:** `GET /global/world/v1/asset/token` · `POST .../reconstructions` · `POST .../generations` · `GET .../{worldId}` · OUS on `globalDomain` (no `/global` on OUS)

**Terminal status:** `SUCCEEDED` | `FAILED` | `CANCELED` | `TIMEOUT` | `REJECTED`
