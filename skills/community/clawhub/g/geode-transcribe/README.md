# Geode On-device Transcribe Skill

This skill provides **Geode**'s local transcription and summarization capabilities to OpenClaw and other AI agents.

## Features
- **Privacy-First**: All processing happens locally on your Mac. No data leaves your device.
- **Asynchronous**: Submit large files and continue your conversation while the worker processes in the background.
- **High Performance**: Optimized for Apple Silicon and high-end hardware.

## Prerequisites
You must have the **Geode.app** installed on your macOS device. If it is missing, the CLI will fail.
- **Download on the App Store:** [Get Geode](https://apps.apple.com/app/apple-store/id6752685916?pt=127800752&ct=openclaw&mt=8)

## Technical Details
- **CLI Path:** `/Applications/Geode.app/Contents/Helpers/GeodeCLI`
- **Shared Container:** `group.com.privycloudless.privyecho`
- **Storage:** Audio files should be copied to the `CLIInbox` within the App Group container for best results.

## Usage
The AI agent will automatically use `submit_transcription` when you provide an audio file and `check_task_status` to retrieve your results once finished.
