# Audio PT Auto-Reply 🎙️🇧🇷

Talk to your OpenClaw agent in Brazilian Portuguese, and get a voice reply back.

That is the whole idea.

You send an audio message.
The skill transcribes it locally.
Your OpenClaw agent answers.
The answer comes back as audio. 🔊

No big platform. No weird magic. Just a small, useful voice loop for people who would rather speak than type.

## Why this exists ✨

Typing is not always the best way to talk to an agent.

Sometimes you are on your phone. Sometimes you are walking. Sometimes you are doing something else. Sometimes voice just feels more natural.

Audio PT Auto-Reply gives OpenClaw a simple PT-BR voice workflow that feels closer to messaging a person than operating a tool.

It is especially useful for Telegram-style interactions, accessibility workflows, quick mobile replies, and hands-busy situations.

## What it does 🧩

Audio PT Auto-Reply adds a focused voice pipeline to OpenClaw:

* 🎧 transcribes Brazilian Portuguese audio locally with `jonatasgrosman/wav2vec2-large-xlsr-53-portuguese`
* 🧠 asks your local OpenClaw agent to generate a short reply by default
* ☁️ can optionally use Anthropic only when `ANTHROPIC_API_KEY` is set
* 🗣️ turns the answer into speech with local Piper voices
* 🎚️ lets you choose voices with `/voz`
* 🩺 includes a health check so setup problems are easier to find

## What it does not do 🚧

This skill is intentionally small and careful.

It does not request `sudo`.
It does not install system packages behind your back.
It does not modify other skills.
It does not read unrelated files.
It does not upload audio files to third-party services.
It does not ship a public automatic audio hook that expands untrusted template values inside a shell command.

That last part matters.

Earlier hook-based builds were too easy to make risky because values like `{{MediaPath}}` could be expanded by the platform into a shell command before the skill code had a chance to validate them.

So this build keeps the useful part, the voice pipeline, and removes the risky public hook surface. Safer, cleaner, easier to review. 🛡️

## Privacy model 🔒

By default, the skill is local-first:

* audio transcription runs locally
* speech synthesis runs locally
* response generation uses the local OpenClaw CLI
* audio files are not uploaded by this skill

Optional external mode:

* if `ANTHROPIC_API_KEY` is present, transcript text may be sent to Anthropic for response generation
* audio is still not uploaded by this skill
* unset `ANTHROPIC_API_KEY` to keep response generation local

## Install ⚙️

Run:

```bash
bash install.sh
```

The installer creates a virtualenv inside the skill directory, installs Python dependencies there, downloads Piper, downloads PT-BR voices, writes the default voice config, and runs a health check.

It expects these system dependencies to already exist:

```text
python3
ffmpeg
tar
curl or wget
```

If something is missing, the installer stops and tells you what to install manually.

## Use 🗣️

List available voices:

```bash
/voz listar
```

Choose a voice:

```bash
/voz jeff
/voz cadu
/voz faber
/voz miro
/voz feminina
/voz masculina
```

Process an audio file manually:

```bash
bash process.sh --audio-file /absolute/path/to/audio.ogg
```

When synthesis succeeds, the script prints a `MEDIA:` directive pointing to the generated voice reply.

## Optional environment variables 🧰

```text
ANTHROPIC_API_KEY     Enables Anthropic response generation
AUDIO_VOICE           Sets the default voice
RESPONSE_TIMEOUT      Response timeout in seconds, default 30
SYNTHESIS_TIMEOUT     Synthesis timeout in seconds, default 45
WORKSPACE             Overrides the OpenClaw workspace path
PYTHON_BIN            Overrides the Python executable used by install.sh
```

## Safety note for hooks 🛡️

This public package does not register an automatic `message.audio.receive` hook.

That is deliberate.

Shell-templated hooks can become unsafe when the platform expands values like media paths, targets, or message IDs into a shell command string before your script receives them.

For public distribution, the safer choice is to ship the voice pipeline without that hook. `LOCAL_HOOK_EXAMPLE.md` exists only for local operators who understand the risk and want to wire a hook manually in a controlled environment.

## Files included 📦

```text
install.sh                         Installer with local virtualenv setup
process.sh                         Main voice-processing entry point
health_check.py                    Setup validation
LOCAL_HOOK_EXAMPLE.md              Local-only hook notes
requirements.txt                   Required Python dependencies
requirements-optional.txt          Optional Anthropic dependency
scripts/transcribe_universal.py    Local PT-BR transcription
scripts/claude_adapter.py          OpenClaw or optional Anthropic response generation
scripts/synthesize_universal.py    Piper TTS synthesis
scripts/voice_config.py            Voice selection storage
```

## Good fit ✅

Use this skill if you want a small Portuguese voice loop for OpenClaw, especially when you care about local transcription, local speech synthesis, and a public package that avoids unnecessary permission creep.

It is not trying to be a full voice assistant platform.

It is just a focused voice-reply helper: audio in, agent response, audio out. 🎙️→🧠→🔊
