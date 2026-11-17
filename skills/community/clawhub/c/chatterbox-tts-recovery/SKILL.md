---
name: "chatterbox-tts-recovery"
description: "Restore and verify the Chatterbox TTS browser/OpenAI-compatible bridge stack after upgrades, reinstalls, or damaged local state."
---

# Chatterbox TTS Recovery

Use this skill when Chatterbox TTS, the browser add-on, Voice Lab, or the local OpenAI-compatible bridge stops working after an upgrade/reinstall or when local state has drifted from the known-good setup.

## Canonical source

Treat `pinguy/chatterbox-tts-addon` as the canonical implementation.

Do **not** copy backend source into this skill and do not maintain a second patched copy here. The canonical repository owns:

- `chatterbox_nano_server.py`
- `openwebui_audio_bridge.py`
- `chatterbox_voice_app.py`
- Voice Lab template
- Firefox and Chrome/Chromium extension source
- backend installer
- package/build validation

This skill owns the recovery procedure, protected behaviour, and acceptance checks.

If the live installation disagrees with the canonical repository, identify the reason before overwriting it. Preserve deliberate local configuration and user-created voices.

## Protected behaviour

The normal local topology is:

```text
Firefox / Chrome
    |
    v
127.0.0.1:8010  OpenAI-compatible bridge
    |
    | starts Chatterbox on demand
    v
127.0.0.1:8020  Chatterbox-Nano service

127.0.0.1:8030  Voice Lab
    |
    +-------------------------------> 127.0.0.1:8020
```

Protect these semantics:

- Services bind to loopback by default.
- Chatterbox is CPU-only by default and starts only when speech is requested.
- The installer assigns logical CPU count minus one to OMP/MKL/OpenBLAS work and one Torch inter-op thread.
- Chatterbox remains warm between requests, then exits after `CHATTERBOX_IDLE_SECONDS` (normally 1200 seconds).
- The bridge accepts OpenAI-compatible speech requests on port 8010.
- Long TTS input is split internally at bounded sentence/line/whitespace boundaries (`CHATTERBOX_CHUNK_CHARS`, normally 500) and returned as one joined WAV.
- Browser add-ons own line-aware buffering, playback ordering, job ownership, replay/download, and browser-side Stop behaviour.
- Stop immediately halts browser playback and invalidates queued browser/bridge work.
- Stop does **not** forcibly kill an inference request already running inside Chatterbox. That result may finish and be discarded; the model exits later through normal idle shutdown.
- Voice Lab shares the same Chatterbox service and can start it on demand.
- Per-preview reference conditioning must not leak into later normal TTS requests.
- A selected default voice is persisted through the user systemd drop-in and survives service restart.
- Whisper STT is optional. Failure or absence of Whisper must not break TTS.

Do not reintroduce older semantics where Stop kills the Chatterbox service immediately or where Open WebUI immutable frontend chunks must be patched to provide buffering.

## Durable state

Normal installed runtime state lives under:

```text
~/.local/share/chatterbox-tts/
```

Important user state includes:

- `~/.local/share/chatterbox-tts/voices/`
- `~/.config/systemd/user/chatterbox-nano.service.d/20-voice-app-default.conf`
- other deliberate user drop-ins under `~/.config/systemd/user/chatterbox-nano.service.d/`

Important user units include:

- `~/.config/systemd/user/chatterbox-nano.service`
- `~/.config/systemd/user/openwebui-audio-bridge.service`
- `~/.config/systemd/user/chatterbox-voice-app.service`

Treat voice libraries, selected defaults, and local service overrides as user data. Back them up before destructive recovery.

Do not commit live voice libraries, generated backups, local `.env` files, service state, or authentication material to the Skills repository.

## Recovery workflow

### 1. Inspect before changing anything

Collect:

```bash
systemctl --user status openwebui-audio-bridge.service --no-pager
systemctl --user status chatterbox-voice-app.service --no-pager
systemctl --user status chatterbox-nano.service --no-pager
curl -fsS http://127.0.0.1:8010/health
```

Also inspect:

- current `CHATTERBOX_INSTALL_ROOT` if overridden;
- current systemd drop-ins;
- current default/reference voice;
- browser add-on version/source;
- whether the failure is backend, bridge, Voice Lab, browser extension, or native OpenAI-compatible client integration.

Do not reinstall everything merely because one layer is unhealthy.

### 2. Validate canonical source

Use a clean/current checkout of `pinguy/chatterbox-tts-addon`.

Before installing from it:

```bash
make validate
```

Do not deploy a checkout that fails its own validation.

The validation covers Python syntax, manifests, installer/build shell syntax, Firefox/Chrome JavaScript syntax, and browser package construction.

### 3. Protect user state

Before a reinstall or replacement:

- back up the managed `voices/` directory;
- back up `chatterbox-nano.service.d/`;
- record any custom environment variables or non-default ports;
- record current service enablement/state;
- preserve any separately configured Whisper worker/model paths.

Do not replace user-created voice data with bundled starter voices.

### 4. Repair the smallest broken layer

Prefer the narrowest repair:

- extension-only problem -> reinstall/reload the relevant browser extension;
- bridge problem -> replace/reinstall the canonical bridge and restart only the bridge;
- Voice Lab problem -> replace/reinstall Voice Lab and restart only that service;
- Chatterbox backend/model problem -> repair the backend/model and restart Chatterbox;
- unit/install drift across several components -> use the canonical installer.

For a full backend reinstall:

```bash
bash chatterbox-tts-addon/install.sh
```

The installer uses a private environment under `~/.local/share/chatterbox-tts/`, installs the canonical backend files and user units, and enables the bridge and Voice Lab. Chatterbox itself remains on-demand.

After unit changes:

```bash
systemctl --user daemon-reload
```

Restart only services whose executable/configuration changed.

### 5. Restore local configuration

Reapply only deliberate local overrides that are still needed.

Prefer environment variables and systemd user drop-ins over editing canonical source.

Typical configuration knobs include:

- `CHATTERBOX_INSTALL_ROOT`
- `CHATTERBOX_MODEL_DIR`
- `CHATTERBOX_REFERENCE_ROOT`
- `CHATTERBOX_REFERENCE_WAV`
- `CHATTERBOX_IDLE_SECONDS`
- `CHATTERBOX_CHUNK_CHARS`
- `CHATTERBOX_PORT`
- `CHATTERBOX_VOICE_APP_PORT`
- `BRIDGE_API_KEY`
- optional Whisper variables

If exposing any service beyond loopback, do not keep the development API key.

### 6. Restore the browser client

Firefox uses the signed/temporary Firefox extension source/package.

Chrome/Chromium uses the Manifest V3 extension, normally through **Load unpacked** for a local install.

Do not patch generated Open WebUI frontend chunks merely to restore extension playback semantics.

If a separate client uses the bridge as an OpenAI-compatible TTS endpoint, configure that client to use the bridge rather than modifying the bridge to impersonate unrelated frontend state.

## Acceptance checks

Configuration is not acceptance. Verify the real path.

### Static/source checks

From the canonical checkout:

```bash
make validate
```

This must pass before blaming runtime state on the source tree.

### Bridge health

```bash
curl -fsS http://127.0.0.1:8010/health
```

Confirm:

- `"ok": true`;
- TTS backend is Chatterbox-Nano;
- Chatterbox health transitions correctly between unloaded and loaded states;
- optional Whisper status does not block TTS.

### Direct speech canary

Send a short authenticated request to the bridge and save the WAV.

Verify:

- HTTP 200;
- valid WAV container;
- mono PCM output;
- 24 kHz sample rate;
- non-zero audio duration.

A successful `/health` response alone is not proof that synthesis works.

### Long-text canary

Use input longer than one internal chunk.

Confirm:

- the request succeeds;
- the bridge splits work without exceeding the configured chunk limit;
- returned audio is one valid joined WAV;
- ordering is correct;
- there are no repeated or missing segments.

### Browser canary

Use the real installed browser extension.

Verify:

- selected text/page/popup speech reaches the bridge;
- playback starts and remains ordered;
- line-aware buffering works under slower CPU inference;
- replay/download still work where expected;
- no duplicate jobs appear across tabs/popup.

### Stop canary

Stop during active multi-part speech.

Confirm:

- browser playback stops immediately;
- queued browser work is invalidated;
- the bridge advances its cancellation epoch and abandons remaining chunks;
- an already-running Chatterbox inference is not assumed to die instantly;
- Chatterbox remains available until its normal idle shutdown.

Do not mark Stop broken merely because `chatterbox-nano.service` is still alive immediately after cancellation.

### Voice Lab canary

Open:

```text
http://127.0.0.1:8030/
```

Verify:

- existing managed voices are listed;
- a preview uses the requested reference;
- preview conditioning does not become the next normal TTS voice accidentally;
- changing the default voice persists through restart;
- attempting to delete the current default is rejected;
- rollback restores the previous drop-in if a default switch fails.

### Idle lifecycle

Confirm the server reports the configured idle-shutdown interval.

When practical, use a temporary short idle interval for a dedicated test rather than waiting the production default. Verify Chatterbox exits only after it is idle and is started again by the next speech/preview request.

## Failure handling

If recovery fails:

1. stop changing layers;
2. state which layer is failing: browser, bridge, Chatterbox, Voice Lab, systemd, model, or optional STT;
3. capture the exact command/error and service logs;
4. state what was changed and what user state was preserved;
5. restore backed-up voice/default configuration if the repair changed it;
6. do not repeatedly reinstall the full stack without a new hypothesis.

Useful logs:

```bash
journalctl --user -u openwebui-audio-bridge.service -n 100 --no-pager
journalctl --user -u chatterbox-nano.service -n 100 --no-pager
journalctl --user -u chatterbox-voice-app.service -n 100 --no-pager
```

## Source-of-truth rule

When this skill conflicts with the current canonical Chatterbox add-on repository, inspect the current implementation and tests before deciding which is stale.

The skill describes protected behaviour and recovery intent. The canonical repository defines the current executable implementation.
