# Setup and Input Requirements

## Install the CLI

The skill requires Node.js 18 or newer and the official BizMuse CLI:

```bash
npm install -g bizmuse-cli
bizmuse --help
```

## Configure Authentication

Create an API key at `https://bizmuse.ai/settings/apikeys`, then configure it in the user's own terminal:

```bash
bizmuse auth set-api-key <key>
bizmuse auth status
```

Never request an API key in chat. The CLI stores authentication in its local application configuration, not in the project directory.

## Supported Audio

- Local MP3, WAV, M4A, or AAC file.
- Direct public HTTP or HTTPS audio URL.
- Duration from 10 to 180 seconds.
- Maximum local upload size of 20 MB.

Platform page URLs are not media URLs. Export or download audio from Suno, YouTube, Udio, SoundCloud, or similar services before submission.

## Supported Images

- 1-7 local JPG, JPEG, PNG, or WebP files.
- Direct public HTTP or HTTPS image URLs.
- Maximum local upload size of 50 MB per image.

## Account Requirements

Generation requires a BizMuse account and sufficient credits. Current plans and costs are listed at `https://bizmuse.ai/pricing`.
