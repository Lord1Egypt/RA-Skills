---
name: clickmap
description: Chrome UI automation skill for saving named on-screen targets and reusing them with reliable click/type actions. Use when browser automation is flaky, selectors break, or you need deterministic "click this named point, then type" flows for tools like Suno, internal dashboards, forms, and repetitive web tasks.
---

# ClickMap

Make flaky web automation stable: save named points once, then click/type by name every time.

## Why people use this
- Stops brittle selector/DOM failures in UI automation flows
- Reuses human-readable names instead of random coordinates
- Great for repeat tasks: click target → type text → submit

## Resources
- Extension folder: `assets/chrome-extension/`
- Local bridge: `scripts/bridge-server.js`
- Optional launcher: `scripts/start-bridge.cmd`
- Autostart installer: `scripts/install-autostart.ps1`
- Action runner: `scripts/clickmap-actions.ps1`
- Data file: `data/pois.json`

## Capture flow (user)
1. Load unpacked extension from `assets/chrome-extension`.
2. Start bridge (`node scripts/bridge-server.js` or `start-bridge.cmd`).
   - Optional: `powershell -ExecutionPolicy Bypass -File scripts/install-autostart.ps1 -RunNow` to keep bridge auto-running after reload/login.
3. Open target page (example: `https://suno.com/create`).
4. Toggle marking ON from popup.
5. Hover mouse at exact pixel and press **P** to add point.
6. Native prompt opens: enter POI name and save.
7. Press **D** while hovering near a point to delete nearest saved POI.
8. Bright pink dots show saved points on that page.

POIs auto-sync to bridge when possible. Use popup **Sync POIs** if needed.

## Agent action commands (no desktop-control)
Always use the ClickMap action runner for clicks/types:

```powershell
# List points
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/clickmap/scripts/clickmap-actions.ps1" -Action list

# Click saved point exactly (screen coords)
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/clickmap/scripts/clickmap-actions.ps1" -Action click -PoiName "suno_com.LyricsBox"

# Type text into focused field (paste mode by default)
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/clickmap/scripts/clickmap-actions.ps1" -Action type -Text "hello world" -ClearFirst

# Click then type in one call
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/clickmap/scripts/clickmap-actions.ps1" -Action click-type -PoiName "suno_com.songName" -Text "Still Learning My Name (Remix)" -ClearFirst
```

## Notes
- Best results come from POIs that include `coords.screen` (new captures do this automatically).
- If an old POI misses screen coords, just re-save it once.
- Use clear names (example: `suno_com.StylesBox`) so automations stay readable.
- The bridge runs locally on your machine (localhost only).
