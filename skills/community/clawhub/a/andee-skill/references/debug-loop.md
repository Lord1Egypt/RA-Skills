# Step 3 — the debug loop

Only for people **developing** Andee. If they just wanted it running, `build-and-install.md` was the
end of the road.

The loop is: **change code → `./gradlew installDebug` → look at the device.** Everything below is how
to "look at the device" without guessing.

## 3.1 adb, and the three ways it lies to you

`adb` lives in **Android SDK Platform-Tools** and is often *not* on `PATH`. On macOS that is
`$HOME/Library/Android/sdk/platform-tools/adb`, and you can read the real location out of the
repository's `local.properties` (`sdk.dir`). Write the full path once into a shell variable and use
that — do not spend a round discovering `command not found`.

```bash
adb devices -l
adb -s <serial> shell wm size          # screen size
adb -s <serial> shell wm density       # DPI — this is what changes how the overlay lays out
```

| `adb devices` shows | What is actually wrong |
|---|---|
| **empty**, and the USB device is also absent at the OS level | **Physical layer** — a charge-only cable, or the wrong port. `system_profiler SPUSBDataType` on macOS shows whether the OS sees it at all. Do not go looking in phone settings |
| `unauthorized` | The phone's side — the screen is locked, or nobody tapped the authorization dialog |
| **empty**, but the OS **does** see the device | The **adb server** is confused. `adb kill-server` and retry — this is common and the fix is one command |

> After `kill-server`, the `transport_id` **always** changes, so **any `adb forward` rule is gone**.
> Re-establish it (§3.3) and confirm with a read-only call before trusting anything else.

### Wireless adb, and the single-USB-port problem

If the app is going to use the robot-dog USB OTG dongle, the dongle and the cable want the same
socket. Move debugging onto the network **while the cable is still plugged in**:

```bash
adb tcpip 5555
adb connect <device IP>:5555
# now unplug the cable and give the port to the dongle
adb usb                    # to switch back
```

## 3.2 logcat

The tags that matter (read them out of the source if these drift — each file declares its own):

| Tag | Where it comes from |
|---|---|
| `Body` | `ScreenBodyService`, `TreeHelper`, `Notebook`, `Scheduler`, `ChatHistory`, the UI, self-check |
| `Brain` | `LocalBrain`, `LlmClient`, `NotificationTriage` — the agent loop |
| `BodyWs` / `BodyWsClient` | the device's WS server, and the client that dials the hub |
| `Wake` | the offline wake word |
| `Asr` / `Tts` / `AudioIO` / `AudioFocus` | the voice pipeline |
| `Dog` | the USB dongle and the robot dog |
| `Ime` / `Card` / `Meeting` | keyboard switching, cards, meeting recorder |

```bash
adb logcat -s Body:* Brain:*          # the two you will actually live in
adb logcat -s Wake:*                  # wake word: `wake: d=1.52 <= 1.96` vs `no wake: d=… > …`
```

Two lines worth memorising:

- `Body: ws server started on 0.0.0.0:9008` — the service is alive. This is the proof
  `onServiceConnected` fired, i.e. accessibility is actually granted.
- `hub: registered as body-xxx with N tools` — the device reached a remote brain hub.

## 3.3 The device's own WebSocket tool port — the fastest way to drive it

`ScreenBodyService` runs a WebSocket server **on the device**, port **9008**, exposing every tool the
brain can call. This is how you verify a screen behaviour without involving the microphone, the ASR
or the model — all three of which are variables you do not want in a debugging loop.

```bash
adb forward tcp:9008 tcp:9008      # re-do this after every replug / kill-server
```

Protocol (JSON, one request per frame):

```jsonc
// you → device
{"type":"request","id":"1","method":"device.battery","params":{}}

// device → you
{"type":"response","id":"1","result":{ ... }}
{"type":"response","id":"1","error":"..."}
```

**Probe with a read-only call first.** If the service is not up, or the dispatcher is not wired,
a request **hangs until timeout and nothing happens on screen** — which reads as "the device is
broken" when it is really "nothing is listening". `device.battery` is the cheapest probe.

Method names are the ones in **`app/src/main/java/net/kuafuai/andee/net/CommandDispatcher.kt`** —
read them there rather than trusting any list, including this one. Groups you will use:

| Group | Examples | Notes |
|---|---|---|
| `screen.*` | `screen.ui_tree`, `screen.screenshot`, `screen.tap`, `screen.tap_id`, `screen.type`, `screen.submit_input`, `screen.swipe`, `screen.global` | **These fold the full-screen card back into the ball first** (`ensureCompact()` fires on the `screen.` prefix). If a card is open and your taps seem to do nothing, this is why |
| `device.*` | `device.battery`, `device.apps`, `device.permissions`, `device.launch`, `device.notifications` | Read-only ones are the safe probes |
| `ui.*` | `ui.ask`, `ui.alert`, `ui.show_html` | These do **not** fold the card — they live in it. `ui.ask` / `ui.alert` **block until dismissed or until `timeout_ms`**, so run them in the background if you also want to screenshot |
| `note.*` / `scene.*` | `note.remember`, `note.todos`, `scene.list`, `scene.save` | The private notebook and scenes |
| `dog.*` | `dog.move`, `dog.stop`, `dog.status` | Robot dog. `dog.stop` is the first thing to call when someone says "stop" |

Two behavioural facts to keep in mind while driving it by hand:

- A turn started by a notification runs with `untrusted = true`, and the dispatcher **refuses**
  `device.vault.*` and `scene.save` / `scene.enter` / `scene.delete` on it. That refusal is in the
  dispatcher, not in the prompt — which is the point.
- The notebook tools are `localOnly`: they are filtered out of the hub payload, so habits and
  promises physically cannot leave the device.

**Optional convenience:** the repository already ships `tools/body.py`, a thin CLI over this same
port (it needs the `websocket-client` Python package). Use it if you like; it is not required, and
anything it does you can do with a raw frame.

```bash
./tools/body.py ui_tree
./tools/body.py device.battery
```

## 3.4 Verifying a change when no device is attached

`adb devices` coming back empty is the normal state, not a blocker. Four things cover most changes:

1. **It compiles:** `./gradlew :app:assembleDebug`.
2. **A new string really made it into the package.** `aapt2 dump strings` reads the *resource string
   pool* out of the built APK — grep the literal:
   ```bash
   AAPT2=$(ls -d "$HOME"/Library/Android/sdk/build-tools/*/aapt2 | tail -1)
   cd app/build/outputs/apk/debug
   "$AAPT2" dump strings app-arm64-v8a-debug.apk > /tmp/apk_strings.txt
   grep -c -- "<exact substring you expect>" /tmp/apk_strings.txt
   ```
   Match on an **exact substring**. Counting on a remembered paraphrase of the copy gives a zero hit
   and sends you hunting for a problem that does not exist.
3. **An XML resource change is valid** — inspect the **compiled** artifact, not the source file:
   ```bash
   "$AAPT2" dump xmltree --file res/xml/network_security_config.xml app-arm64-v8a-debug.apk
   ```
   A source file can look perfect and still fail at `mergeDebugResources` (XML comments containing
   `--` are the classic one).
4. **A network contract is what you think it is.** Hit the real endpoint with the real URL while the
   device is still off. Note that `org.json`'s `optString` returns the **string** `"null"` for a JSON
   `null`, not an empty string — so "what shape is this field actually" has to be measured, not
   assumed.

## 3.5 Traps that look like broken hardware

| Symptom | Real cause |
|---|---|
| `ConnectionRefusedError` on `127.0.0.1:9008` | The `adb forward` rule vanished (replug / `kill-server` / wake from sleep). `adb forward --list`, re-add it |
| A `502` from a proxy when talking to `127.0.0.1` | The machine has `HTTP_PROXY` / `HTTPS_PROXY` set and the WS client is sending **loopback** through it. A `502` here has nothing to do with the device. Unset the proxy variables for the call (`NO_PROXY` alone is often not enough) |
| "I called a tool and nothing happened on screen" | The card was open and the method did not start with `screen.` — call `screen.ui_tree` to fold it, or tap the ✕ on the ball |
| A `ui.ask` / `ui.alert` call hangs forever | By design — it blocks until dismissed or `timeout_ms`. Pass an explicit generous `timeout_ms` when a human is in the loop |
| A tool returns `denied("sms")` (or similar) | Working as intended: every sensitive tool checks its runtime permission *before* acting and reports the refusal instead of working around it. Grant the permission, or accept the degraded behaviour |
| A `dog_*` call reports the command went out but nothing moved | Check `dog_status` first — either the original IR remote is still on (it shares the channel and the two transmitters fight), or something is within 20cm (the dog refuses to advance) |

## 3.6 The actual edit loop

```bash
# edit code…
./gradlew :app:assembleDebug      # fast fail on compile errors
./gradlew installDebug            # push to the attached device
adb logcat -s Body:* Brain:*
```

Debug builds are not minified, so **method names appear verbatim in the dex** — pulling the installed
APK and grepping it is a reliable way to prove the device is running the code you think it is:

```bash
adb -s <serial> shell pm path net.kuafuai.andee    # → path to the installed base.apk
adb -s <serial> pull <that path> /tmp/base.apk
unzip -q -o /tmp/base.apk 'classes*.dex' -d /tmp/dex
grep -la "<a method name you just added>" /tmp/dex/*.dex
```

## 3.7 While debugging

- **Do not commit** `local.properties`, device serial numbers, logcat dumps containing real messages,
  or screenshots. This app reads the screen, so a screenshot is a picture of somebody's chats.
- **Match the codebase's style**: no Compose, no DI framework, no coroutines. It is deliberate, and
  there are reasons in the README for each.
- **Do not touch the persona/character casually.** Tone and expression are a documented part of the
  system in this project; `CONTRIBUTING.md` has a section on changing a persona or a mood.
- **When a tool's behaviour changes, its description changes in the same commit.**
  `net/ToolSchemas.kt` is the only manual the model ever reads.
