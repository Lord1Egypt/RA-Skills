# Open the fly in Chrome

Use the Gateway-hosted OpenClaw dashboard. The standalone page on port 4318 does not send tasks into chat.

1. Resolve the current session key with the session/dashboard tools. Arrange its `fly-picker` widget before opening the browser. Reuse an already paired Chrome tab for this session when available; keep only one active fly tab per round so two simulations do not compete to save a pick.
2. Run `openclaw dashboard --json` through the host shell tool and consume the JSON in the same process. Open `browserUrl`, not the legacy `url`. It contains a single-use, ten-minute bootstrap that pairs Chrome to this Gateway. Never print or paste that URL into chat, logs, a release file, or a screenshot. Do not read the shared Gateway token.
3. Open explicitly in Google Chrome. On macOS with cua-driver available, this tested recipe passes the private URL directly to the native launcher without printing it:

```python
import json, subprocess
connection = json.loads(subprocess.check_output(
    ["openclaw", "dashboard", "--json"], text=True))
if not connection.get("ok") or not connection.get("browserUrl"):
    raise RuntimeError("OpenClaw browser handoff unavailable")
result = subprocess.run(
    ["cua-driver", "launch_app", json.dumps({
        "bundle_id": "com.google.Chrome",
        "urls": [connection["browserUrl"]]
    })], capture_output=True, text=True)
if result.returncode:
    raise RuntimeError("Chrome launch failed; inspect the native launcher without logging the bootstrap")
print("Opened OpenClaw in Chrome")
```

Use a supported browser tool/opener on other hosts; do not silently use Safari or the Mac embedded browser. A loopback URL is reachable only from the Gateway host. For remote use, reuse an already configured authenticated HTTPS Control UI; do not expose the Gateway for this task.

4. Wait until the launched Chrome tab finishes pairing and shows the connected Control UI. Use the launcher’s returned process/window identity or fresh native discovery, not a remembered Chrome PID; several Chrome processes can coexist. After Chrome connects, use `screen navigate` with the exact owning `sessionKey`, then `dashboard focus_tab` (`fly`) and `set_presentation` (`expanded`). These commands reach all capable connected clients; the target session should be this conversation. Alternatively select the owning session in Chrome using its current UI. The tested clean route is `/dashboard/<agent>/<session-slug>`, but obtain it from the current UI: do not invent or hardcode a slug. The old root `?session=...` is not a reliable bootstrap deep link.
5. Verify the actual Chrome window shows the fly, brain panel and **Accept & start**. Use the fullscreen control for arena-only recording. Keep the browser open while it decides; leave acceptance to the human.
6. Give only the clean, credential-free browser URL in the final response. If Chrome is unpaired, pair it using a fresh bootstrap through the same private launch flow. A copied clean URL alone does not authenticate a new browser.

If a different Gateway is already selected, the Control UI can ask to confirm the destination. Read that prompt before proceeding; do not overwrite an unrelated connection silently.

## Failure handling

- **Importing a module script failed in the native Mac app:** open the same session in Chrome. The browser-first release does not fix native WebKit HTTP cookies.
- **Custom plugin UI disabled:** inspect the existing setting and enable it under Settings → Labs as part of the authorized companion installation. Preserve other settings; restart only if that setting changed.
- **Handoff unconfirmed:** inspect the chosen round and conversation before retrying. Never bypass the durable acceptance claim.
- **Browser opened but no fly:** verify the owning session, Fly tab, round ID and plugin activation; opening a tab is not rendering proof.
