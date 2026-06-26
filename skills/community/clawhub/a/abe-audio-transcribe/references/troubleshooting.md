# Troubleshooting

## Missing API key
Symptom:

- `Missing API key. Set ASSEMBLYAI_API_KEY or pass --api-key.`

Fix:

- export `ASSEMBLYAI_API_KEY`
- or inject it through the agent environment

## 403 `Cannot access uploaded file`
Most common cause:

- the upload was created with one AssemblyAI project/API key
- the transcript request used a different project/API key

Fix:

- make sure upload and transcription use the same AssemblyAI project credentials

## Transcript status becomes `error`
Common causes documented by AssemblyAI include:

- corrupted or unsupported media
- a URL that points to an HTML page rather than media
- a URL not reachable from AssemblyAI servers
- very short audio (around sub-160ms)

Useful checks:

- verify the file opens locally
- if using a URL, try downloading it manually
- prefer uploading a local file when the remote URL is uncertain

## Language is wrong
Try one of these:

- explicit `--language-code`
- `--expected-languages`
- explicit `--speech-model universal-3-pro` for supported languages
- `--speech-model universal-2` for broader fallback coverage

## Speaker names are still generic
Checklist:

- did you enable `--speaker-labels` when transcribing?
- if post-processing, does the transcript actually contain diarised utterances?
- did you pass `--known-speakers` or `--speaker-profiles` in the right shape?
- if the names still need tweaking, add `--speaker-map`

## Output is too large for stdout
Prefer:

- `--out FILE`
- `--bundle-dir DIR`

This is especially important for long meetings and word-level timestamps.

## Need a newly added API parameter
This skill deliberately exposes raw passthrough options:

- `--config` for transcription requests
- `--understanding-request` for speech understanding
- `--request` for LLM Gateway chat completions

Use those rather than editing the script immediately.

## EU routing
If the user wants EU processing:

```bash
export ASSEMBLYAI_BASE_URL=https://api.eu.assemblyai.com
export ASSEMBLYAI_LLM_BASE_URL=https://llm-gateway.eu.assemblyai.com
```

Or pass them explicitly with `--base-url` and `--llm-base-url`.

## Rate limits / retries
The CLI retries common transient failures such as:

- `429`
- `500`
- `502`
- `503`
- `504`

If the issue persists, slow down the workflow or inspect the exact request body with `--dry-run`.
