# Third-Party Notices

This directory is a publishable single-skill package derived from the broader `bili-mindmap` development workspace.

## Included / Referenced Components

### `bilibili-cli`

- Role: external command-line dependency used for login, metadata retrieval, subtitles, comments, and audio extraction
- Packaging status: not bundled as a source directory in this publish package
- Expected usage: installed separately on the target machine and exposed as the `bili` command

### `vendor/aliyun_asr/`

- Role: bundled cloud-based file transcription fallback implementation
- Origin: adapted from the local `aliyun-asr` companion skill used in the development workspace
- Packaging status: bundled in this publish package as vendored implementation files

### `parakeet-local-asr`

- Role: optional external local ASR service for Linux / macOS
- Packaging status: not bundled as a source directory in this publish package
- Expected usage: started separately and exposed via an OpenAI-compatible transcription endpoint

### `xmind-generator`

- Role in development workspace: XMind export support
- Packaging status: not bundled as a source directory in this publish package
- Note: this publish package uses its own pure Python `.xmind` writer instead of depending on the original `xmind-generator` directory

## Publication Notes

- Review upstream licenses and attribution requirements before wider redistribution or commercial use.
- Keep this file updated if bundled vendor code changes.
