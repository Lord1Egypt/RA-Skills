---
name: linx
description: Upload local files to a configured self-hosted Linx instance and return shareable links. Prefer linx-client when installed, otherwise use the HTTP API via curl.
homepage: https://github.com/lanjelin/openclaw-linx
metadata: {"openclaw":{"requires":{"bins":["python3"],"anyBins":["linx-client","curl"]},"primaryEnv":"LINX_API_KEY"}}
---

# Linx uploads

Use this skill when the user asks to upload or share files through their Linx instance.

## Safety and configuration

- Upload only files the user has authorized sharing. Never upload credentials, private configuration, or unrelated files.
- Use the helper below; do not read or print environment secrets, config contents, or the upload logfile into the conversation.
- Configuration: `LINX_CONFIG` selects a linx-client JSON config. Otherwise the helper checks `$XDG_CONFIG_HOME/linx-client.conf` (default `~/.config/linx-client.conf`). `LINX_URL`, `LINX_API_KEY`, and `LINX_LOGFILE` override the matching config values. `LINX_URL` alone is sufficient for public instances. See `{baseDir}/README.md` for setup.
- If configuration is missing, explain which variable needs setting. Never guess an instance or prompt the CLI interactively.
- Treat the instance address as private configuration. Return only the requested upload links, which necessarily include the serving hostname; do not disclose the base URL separately or copy it into generated docs, examples, or diagnostics.
- Keep deletion keys private. The helper stores them in a local logfile, not stdout. Do not run concurrent uploads against the same logfile.

## Upload

Run on the host containing the files, configuration, and binaries:

```sh
python3 "{baseDir}/scripts/upload.py" -- "/absolute/path/to/file.pdf"
```

Multiple files:

```sh
python3 "{baseDir}/scripts/upload.py" -- "/path/to/first.pdf" "/path/to/second.png"
```

Only when requested, use these options before `--`:

- `--expiry 3600`: request expiry in seconds; server limits still apply.
- `--randomize`: request a random filename; otherwise the server's filename policy applies.
- `--name report.pdf`: remote filename, for a single source file only.
- `--direct`: return the direct file URL when the server provides one.

The helper prefers `linx-client` on PATH, supplies noninteractive configuration, and disables clipboard integration. If it is absent, the helper uses curl to PUT the file to `/upload/<encoded-filename>` with `Accept: application/json` and configured headers. It does not switch backends after an error or automatically retry uploads.

## Results and failures

- On success stdout contains one URL per completed file. Return those links, associated with the source files when useful.
- On failure report the helper's diagnostic. Earlier files in a batch may already have uploaded; preserve their links and do not rerun the entire batch automatically.
- A transport error or invalid response can occur after a file was stored. Do not assume failure means no upload exists. Ask before retrying an ambiguous upload.
- Checksum warnings or mismatches are not clean verification. A binary warning is treated as an error; curl preserves a returned deletion key before checking the checksum.
- This skill uploads regular local files only. It does not implement stdin, overwrite, deletion, access passwords, or burn-after-read. Do not improvise these operations from upload instructions.
