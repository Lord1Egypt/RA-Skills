---
name: avatar-runtime
description: >
  Embeds and controls a virtual avatar using the avatar-runtime npm package.
  Provides Live2D rendering, VRM 3D, vector fallback, and control-driven expression/body/scene animation
  via a provider-agnostic session bridge.
  Use when the user asks for a virtual avatar, face-control animation, Live2D character,
  avatar widget embedding, or when starting/stopping an avatar session.
license: MIT
compatibility: Requires node >= 18, npm, and curl. Runtime executes via npx — internet access required for first run.
env-vars:
  optional:
    - AVATAR_RUNTIME_URL
    - AVATAR_PROVIDER
    - HEYGEN_API_KEY
    - HEYGEN_AVATAR_ID
    - HEYGEN_STRICT
    - LIVE2D_ENDPOINT
    - LIVE2D_STRICT
    - VRM_BRIDGE_ENDPOINT
    - KUSAPICS_API_KEY
    - KUSAPICS_BASE_URL
metadata:
  author: openpersona
  version: "0.2.1"
  source: https://github.com/acnlabs/avatar-runtime
allowed-tools: Bash(node:*) Bash(curl:*) Bash(npm:*) Bash(bash:*)
---

# Avatar Runtime Skill

## Security & Trust

This skill contains **no bundled server code** — it instructs the agent to download and execute the `avatar-runtime` npm package via `npx` at runtime. Before running:

1. **Verify the source** — Review the [avatar-runtime repository](https://github.com/acnlabs/avatar-runtime) and confirm you are installing the official package from the npm registry.
2. **Review setup scripts before running** — `scripts/ensure-default-vrm-sample.sh` and `scripts/ensure-default-live2d-sample.sh` download third-party assets at runtime. Inspect their contents before executing them in your environment.
3. **Sandbox first** — Run `npx avatar-runtime` in an isolated environment and monitor outbound network connections before deploying to production.
4. **Live2D licensing** — The sample Live2D model (`live2d-widget-model-chitose`) is subject to the [Live2D Free Material License](https://www.live2d.com/en/sdk/license/free-material/), which prohibits redistribution and commercial use. Use it for local development only.
5. **API key handling** — `HEYGEN_API_KEY` and `KUSAPICS_API_KEY` are passed as environment variables directly to `npx avatar-runtime`. Ensure these are not logged or exposed in shared environments.

## Runtime endpoint

Default: `http://127.0.0.1:3721`  
Override: `AVATAR_RUNTIME_URL` env var (default applied automatically if unset).

```bash
export AVATAR_RUNTIME_URL="${AVATAR_RUNTIME_URL:-http://127.0.0.1:3721}"
```

## First-time setup

### VRM 3D avatar (free, no account required)

```bash
# Run from the package root
bash scripts/ensure-default-vrm-sample.sh
```

Downloads `VRM1_Constraint_Twist_Sample.vrm` from `@pixiv/three-vrm` (CC BY 4.0 — free to use with attribution).
Sets it as `assets/vrm/slot/default.vrm` so `npm run dev:vrm-bridge` serves it automatically.

### Live2D avatar

The Live2D slot (`assets/live2d/slot/`) requires a model file before the `live2d` provider can render.

**Option A — Use your own model** (recommended):  
Copy any Cubism 2 (`.model.json`) or Cubism 4 (`.model3.json`) model you hold a license for into `assets/live2d/slot/`, named `default.model.json` / `default.model3.json`.

**Option B — Local dev bootstrap only** (risk acknowledged):

```bash
# Run from the package root (where package.json lives)
bash scripts/ensure-default-live2d-sample.sh
```

Downloads `chitose` from the npm package `live2d-widget-model-chitose@1.0.5` for local testing.  
⚠️ The original model is subject to the [Live2D Free Material License](https://www.live2d.com/en/sdk/license/free-material/), which prohibits redistribution and commercial use. Do **not** deploy or distribute with this model.

## Starting the server

```bash
# zero-config (mock provider — no API key required)
AVATAR_PROVIDER=mock npx avatar-runtime

# with Live2D local bridge
npm run dev:live2d-cubism-bridge          # terminal A — bridge on :3755
AVATAR_PROVIDER=live2d LIVE2D_ENDPOINT=http://127.0.0.1:3755 npx avatar-runtime  # terminal B

# with VRM 3D avatar (free models from https://hub.vroid.com — place .vrm in assets/vrm/slot/)
npm run dev:vrm-bridge                    # terminal A — asset server on :3756
AVATAR_PROVIDER=vrm npx avatar-runtime   # terminal B
```

## Session API

```bash
# start session
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"{{slug}}","form":"image"}'

# send text to active session
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/input/text" \
  -H "content-type: application/json" \
  -d '{"sessionId":"<sessionId>","text":"hello"}'

# query current state (includes control namespace for renderer)
curl -s "$AVATAR_RUNTIME_URL/v1/status"
```

## Avatar control API (v0.2)

The runtime uses a unified `control` namespace replacing the legacy `faceControl` field.

```bash
# Set face expression
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{
    "face": {
      "pose":  { "yaw": 0.2 },
      "mouth": { "smile": 0.7 }
    },
    "emotion": { "valence": 0.8, "arousal": 0.3, "label": "happy" }
  }'

# Set body pose (VRM only)
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{
    "body": {
      "preset": "wave",
      "skeleton": { "rightUpperArm": { "x": 0, "y": 0, "z": 60 } }
    }
  }'

# Set scene (VRM only)
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/scene/set" \
  -H "content-type: application/json" \
  -d '{
    "camera": { "fov": 40, "position": { "x": 0, "y": 1.4, "z": 2.5 } },
    "world": { "ambientLight": 0.5, "keyLight": { "intensity": 1.2 } }
  }'

# Full control patch in one call
curl -s -X POST "$AVATAR_RUNTIME_URL/v1/control/set" \
  -H "content-type: application/json" \
  -d '{
    "avatar": {
      "face": { "mouth": { "smile": 0.5 } },
      "emotion": { "label": "neutral" }
    },
    "scene": { "world": { "background": "#001133" } }
  }'
```

**Partial patches:** Only supplied sub-objects are merged. Each sub-domain (`avatar.face`, `avatar.body`, `avatar.emotion`, `scene`) merges independently — patching `mouth.smile` does not clobber `eyes`.

## Embedding an avatar widget (browser)

Minimal script-tag usage — vendor scripts are auto-loaded:

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  var widget = new AvatarWidget(document.getElementById('avatar'), {
    modelUrl: '/packages/avatar-runtime/assets/live2d/slot/default.model.json',
    stateUrl: 'http://127.0.0.1:3721/v1/status',   // polls control namespace
    pollMs:   500,
    // vendorBase: '/your/vendor-dist',              // required for Live2D in production
  });
  widget.ready().catch(function(e) { console.error(e); });
</script>
```

VRM 3D avatar:

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    vrmUrl:   '/packages/avatar-runtime/assets/vrm/slot/default.vrm',
    stateUrl: 'http://127.0.0.1:3721/v1/status',
  });
</script>
```

Without a model (vector fallback — no files needed):

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:360px;height:360px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    stateUrl: 'http://127.0.0.1:3721/v1/status'
  });
</script>
```

## Driving avatar control manually (widget)

`update()` accepts a mediaState with a `control` object.  
Safe to call before `ready()` resolves — buffered and applied on mount.

```js
widget.update({
  control: {
    avatar: {
      face: {
        pose:  { yaw: 0.2, pitch: 0.1, roll: 0 },
        eyes:  { blinkL: 0.9, blinkR: 0.9, gazeX: 0, gazeY: 0 },
        mouth: { jawOpen: 0.3, smile: 0.5 }
      },
      emotion: { valence: 0.7, arousal: 0.2, label: 'content', intensity: 0.6 }
    }
  }
});
```

## control from runtime state

The `/v1/status` response includes a `control` field produced by the active provider merged with agent-set values.  
`AvatarWidget` with `stateUrl` polls this automatically at `pollMs` interval.

For manual polling:

```bash
curl -s "$AVATAR_RUNTIME_URL/v1/status" | jq .control
```

## Provider configuration

| Provider | Env vars | Notes |
|----------|----------|-------|
| `mock` | — | Development default, no key needed |
| `heygen` | `HEYGEN_API_KEY` | Real streaming avatar. `HEYGEN_STRICT=false` degrades to mock |
| `live2d` | `LIVE2D_ENDPOINT` | Local Cubism bridge required. `LIVE2D_STRICT=false` degrades |
| `vrm` | `VRM_BRIDGE_ENDPOINT` | Local 3D avatar, client-side rendering. Free models from [VRoid Hub](https://hub.vroid.com). No API key. |
| `kusapics` | `KUSAPICS_API_KEY`, `KUSAPICS_BASE_URL` | Anime-oriented image provider |

## Provider capabilities

| Provider | faceRig | lipSync | gaze | blink | bodyMotion | streaming | bodyRig | sceneControl |
|----------|:-------:|:-------:|:----:|:-----:|:----------:|:---------:|:-------:|:------------:|
| `mock`     | ✓ | — | ✓ | ✓ | — | — | — | — |
| `heygen`   | ✓ | ✓ | — | — | ✓ | ✓ | — | — |
| `live2d`   | ✓ | ✓ | ✓ | ✓ | — | — | — | — |
| `vrm`      | ✓ | — | ✓ | ✓ | — | — | ✓ | ✓ |
| `kusapics` | — | — | — | — | — | — | — | — |

`bodyRig` and `sceneControl` are VRM-only features — use `/v1/control/avatar/set` with a `body` field and `/v1/control/scene/set` respectively.

## Quick-start: VRM 3D avatar (no API key)

```bash
# Terminal A — Download sample VRM model + serve assets on :3756
cd packages/avatar-runtime
bash scripts/ensure-default-vrm-sample.sh   # one-time download (CC BY 4.0)
npm run dev:vrm-bridge                       # keeps running

# Terminal B — Start runtime pointing at the VRM bridge
AVATAR_PROVIDER=vrm npx avatar-runtime
```

Test face + body control:

```bash
BASE=http://127.0.0.1:3721
SESSION=$(curl -s -X POST "$BASE/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"demo","form":"image"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")

# Face expression
curl -s -X POST "$BASE/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{"face":{"pose":{"yaw":0.2},"mouth":{"smile":0.7}},"emotion":{"label":"happy","valence":0.8}}'

# Body pose (VRM only)
curl -s -X POST "$BASE/v1/control/avatar/set" \
  -H "content-type: application/json" \
  -d '{"body":{"preset":"wave","skeleton":{"rightUpperArm":{"x":0,"y":0,"z":60}}}}'

# Camera scene (VRM only)
curl -s -X POST "$BASE/v1/control/scene/set" \
  -H "content-type: application/json" \
  -d '{"camera":{"fov":35,"position":{"x":0,"y":1.5,"z":2.2}},"world":{"ambientLight":0.6}}'
```

Embed the VRM viewer in a page:

```html
<script src="/packages/avatar-runtime/web/avatar-widget.js"></script>
<div id="avatar" style="width:400px;height:600px"></div>
<script>
  new AvatarWidget(document.getElementById('avatar'), {
    vrmUrl:   '/packages/avatar-runtime/assets/vrm/slot/default.vrm',
    stateUrl: 'http://127.0.0.1:3721/v1/status',
    pollMs:   400,
  });
</script>
```

## Quick-start: HeyGen streaming avatar

Prerequisites: HeyGen API key + an avatar ID from your HeyGen account.

```bash
export HEYGEN_API_KEY="your-key"
export HEYGEN_AVATAR_ID="your-avatar-id"   # from HeyGen dashboard

AVATAR_PROVIDER=heygen npx avatar-runtime
```

Start a session and stream a talking clip:

```bash
BASE=http://127.0.0.1:3721
SESSION=$(curl -s -X POST "$BASE/v1/session/start" \
  -H "content-type: application/json" \
  -d '{"personaId":"demo","form":"video"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")

curl -s -X POST "$BASE/v1/input/text" \
  -H "content-type: application/json" \
  -d "{\"sessionId\":\"$SESSION\",\"text\":\"Hello! I am your AI companion.\"}"

# Poll for a video URL in the response:
curl -s "$BASE/v1/status" | python3 -c "import sys,json; s=json.load(sys.stdin); print(s.get('avatarVideo','(pending)'))"
```

Graceful degradation: when `HEYGEN_STRICT` is unset (default `false`), the runtime automatically falls back to `mock` if the API key is missing or the request fails — useful for local development without a key.

## Fallback policy

If the runtime is unavailable or returns an error:
- Continue interaction in text mode
- Inform the user avatar mode is currently unavailable
- Do not claim rendering or voice playback succeeded

## Additional reference

- [WEB-EMBEDDING.md](references/WEB-EMBEDDING.md) — Renderer Registry, custom renderer implementation, npm usage
