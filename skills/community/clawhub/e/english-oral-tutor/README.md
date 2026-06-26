# English Oral Tutor — Share Bundle

A complete, portable English conversation tutor for OpenClaw. This bundle
contains everything another OpenClaw user needs to install the skill on
their own machine, customized for their own student.

## What's in the bundle

```
skill/
├── README.md                       # this file
│
├── plugin-design/                  # design documentation
│   ├── SKILL.md                    #   main design doc + install steps
│   ├── AGENT-SPEC.md               #   deeper internal spec
│   └── references/
│       └── companion-files.md      #   plugin/config/voice runtime details
│
├── workspace/                      # agent workspace template
│   ├── SOUL.md                     #   authoritative rule source
│   ├── AGENTS.md                   #   operational index (defers to SOUL.md)
│   ├── USER.md.template            #   fill in with your student's info
│   ├── IDENTITY.md.template        #   fill in agent name / student name
│   ├── TOOLS.md                    #   local environment notes (optional)
│   └── HEARTBEAT.md                #   periodic tasks (default: empty)
│
├── plugin/
│   └── tutor-timing/               # session phase injector plugin
│       ├── index.js
│       ├── openclaw.plugin.json
│       ├── package.json
│       └── package-lock.json
│
├── topic-library/
│   └── topic-library.md            # PET/FCE topic prompts
│
└── voice/                          # optional browser voice I/O
    └── openclaw-voice-userscript.js   # Tampermonkey userscript
```

## What is NOT in this bundle (and why)

The following files exist in the original developer's setup but are
**personal to their student** and must never be shared:

- `conversation-history.md` — per-session summaries
- `teaching-transcript.md` — verbatim chat logs
- `BOOTSTRAP.archive.md` — old wizard scaffold (no longer needed)

Recipients will accumulate their own equivalents as they use the tutor.

---

## Install in 4 steps

### 1. Copy the workspace to your OpenClaw workspace

Pick an agent ID (e.g. `english-oral-teacher`) and copy the workspace:

```bash
mkdir -p ~/.openclaw/workspace/english-oral-teacher
cp -r workspace/* ~/.openclaw/workspace/english-oral-teacher/
```

Then customize the two templates:

```bash
cd ~/.openclaw/workspace/english-oral-teacher
mv USER.md.template USER.md       # fill in student name, age, level
mv IDENTITY.md.template IDENTITY.md   # fill in agent name
```

Edit `USER.md` and `IDENTITY.md` to replace the `[PLACEHOLDERS]` with your
student's actual info.

Also copy the topic library into your agent directory:

```bash
mkdir -p ~/.openclaw/agents/english-oral-teacher/english-oral-tutor/references
cp topic-library/topic-library.md ~/.openclaw/agents/english-oral-teacher/english-oral-tutor/references/
```

### 2. Install the plugin

```bash
cp -r plugin/tutor-timing ~/.openclaw/extensions/tutor-timing
```

Then register it in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "tutor-timing": { "enabled": true }
    }
  }
}
```

### 3. Add the agent entry

In the same `openclaw.json`, add to `agents.list`:

```json
{
  "id": "english-oral-teacher",
  "workspace": "C:\\Users\\<you>\\.openclaw\\workspace\\english-oral-teacher",
  "agentDir": "C:\\Users\\<you>\\.openclaw\\agents\\english-oral-teacher",
  "tts": { "auto": "off" }
}
```

(Replace `<you>` with your Windows username. On macOS/Linux, use the
appropriate path style — OpenClaw accepts POSIX paths on those systems.)

TTS `auto: off` is **critical** — voice output is handled by the optional
Tampermonkey userscript below, not by OpenClaw. If you forget this, the agent
will emit `[[audio_as_voice]]` directives that conflict with the userscript.

### 4. Restart the gateway and verify

```bash
openclaw gateway restart
```

Open the Control UI at `http://127.0.0.1:18789/` and select the
`english-oral-teacher` agent. Send a test message — you should see a
`[System Context]` block appear with the current timestamp, elapsed
minutes, and current phase. If it does, the plugin is wired up correctly.

---

## Optional: Voice I/O (browser)

The `voice/openclaw-voice-userscript.js` adds speech-to-text input and
text-to-speech output via Tampermonkey in the OpenClaw Control UI.

1. Install [Tampermonkey](https://www.tampermonkey.net/) for your browser
   (Chrome / Edge recommended)
2. Create a new userscript and paste the contents of
   `voice/openclaw-voice-userscript.js`
3. Visit `http://127.0.0.1:18789/` — a floating "VOICE" panel appears in
   the bottom-left
4. Press `F6` or `Ctrl+Shift+M` to toggle the microphone

Features:
- STT via Web Speech API `SpeechRecognition` (browser-native, free)
- TTS via Web Speech API `SpeechSynthesis` with incremental sentence queue
- 30s TTS timeout recovery (Chrome engine suspend workaround)
- 1.10x default rate, Microsoft Sonia Neural (en-GB) voice

---

## Customization

| To change... | Edit... |
|--------------|---------|
| Student name/age/level | `USER.md` |
| Agent name/persona | `IDENTITY.md` |
| Iron rules (e.g. allow Chinese) | `workspace/SOUL.md` Core Truths |
| Phase durations | `plugin/tutor-timing/index.js` |
| Add topics | `topic-library/topic-library.md` |
| TTS voice | `openclaw.json` tts.providers.microsoft |

For a deeper design read, see `plugin-design/SKILL.md` and
`plugin-design/AGENT-SPEC.md`. The `plugin-design/references/companion-files.md`
explains the plugin's hook architecture and state machine.

---

## Known issues

- **`openclaw configure` and `openclaw doctor --fix` may overwrite workspace
  files** (issue #27919). Always back up `workspace/english-oral-teacher/`
  before running either.
- **The agent may sometimes still output `[[audio_as_voice]]`** despite the
  iron rule. Reinforce in `SOUL.md` Core Truth #6 if it happens.
- **Plugin context is empty in some hooks.** The `tutor-timing` plugin uses
  module-level state and unconditional injection to work around this. If
  you fork the plugin, keep this design.

---

## License

This bundle is shared as-is for educational use. No warranty — review the
content and adapt it for your student's specific needs before deploying.
