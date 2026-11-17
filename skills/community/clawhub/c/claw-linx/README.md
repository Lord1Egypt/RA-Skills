# openclaw-linx

An [OpenClaw](https://openclaw.ai/) skill for uploading local files to a self-hosted [Linx](https://github.com/gabe565/linx-server) instance.

Uses [Lanjelin/linx-client](https://github.com/Lanjelin/linx-client) when `linx-client` is on PATH. Otherwise uploads through the HTTP API using curl. No hosted service or instance address is bundled.

## Requirements

- Python 3.11 or newer (standard library only).
- The forked `linx-client` binary, or curl with `--header @file` support (7.55.0+).
- Network access to your instance and permission to read the source files.

Install the client from its [releases](https://github.com/Lanjelin/linx-client/releases), or build it using that repository's instructions. It remains an optional, separately installed GPL-3.0 dependency; no client code is included here.

## Install

Clone into OpenClaw's managed skills directory:

```sh
git clone https://github.com/lanjelin/openclaw-linx.git ~/.openclaw/skills/linx
```

For one workspace instead, clone to `<workspace>/skills/linx`. With a custom OpenClaw state directory, use `<state-dir>/skills/linx`. The canonical entry point is uppercase `SKILL.md`, as required by OpenClaw discovery. Start a new session after installation or configuration changes. `openclaw skills check` can diagnose missing prerequisites.

## Configuration

### Environment only

Set variables in the environment of the process executing the skill, not merely an unrelated terminal:

```sh
export LINX_URL='https://linx.example.com/'
# Only for instances requiring authentication:
export LINX_API_KEY='your-api-key'
```

Use the instance base URL, including any deployment subpath, **not** `/api` or `/upload`. HTTP and HTTPS are supported; use HTTPS outside trusted local networks. Credentials in URLs, query strings, and fragments are not supported.

### Existing client configuration

`LINX_CONFIG` points to the same JSON format used by the forked client:

```sh
export LINX_CONFIG="$HOME/.config/linx-client.conf"
chmod 600 "$LINX_CONFIG"
```

Example config (replace placeholders locally; never commit real settings):

```json
{
  "siteurl": "https://linx.example.com/",
  "logfile": "~/.local/state/openclaw-linx/uploads.json",
  "apikey": ""
}
```

| Setting | Environment override | Config key | Default |
| --- | --- | --- | --- |
| Config file | `LINX_CONFIG` | — | `$XDG_CONFIG_HOME/linx-client.conf`, or `~/.config/linx-client.conf` |
| Instance base URL | `LINX_URL` | `siteurl` | Required |
| API key | `LINX_API_KEY` | `apikey` | Empty (public instance) |
| Deletion-key logfile | `LINX_LOGFILE` | `logfile` | `$XDG_STATE_HOME/openclaw-linx/uploads.json`, or `~/.local/state/openclaw-linx/uploads.json` |

Environment values override config values. An explicitly empty `LINX_API_KEY` clears a configured key; an empty URL is an error. An explicit `LINX_CONFIG` must be readable and valid JSON, even with environment overrides. A missing default config is fine; an existing malformed config is an error. Paths expand `~` and environment variables and resolve relative to the working directory. Use absolute config/log paths for predictable automation.

The helper never modifies your config or launches client setup. It writes a temporary, mode-0600 effective client config inside a private temporary directory and removes it afterward. Both backends use the same effective settings and logfile. The fallback persists the server's deletion key using the client's `{ "upload URL": "deletion key" }` format. Do not run simultaneous uploads or client logfile operations against the same logfile: the client does not provide coordinated locking.

### OpenClaw environment injection

Alternatively, merge an entry into your private `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "linx": {
        "enabled": true,
        "env": {
          "LINX_CONFIG": "/absolute/path/to/linx-client.conf"
        }
      }
    }
  }
}
```

For environment-only setup, replace `LINX_CONFIG` with `LINX_URL` and optionally `LINX_API_KEY`. OpenClaw's `skills.entries.linx.apiKey` also maps to `LINX_API_KEY` via the skill's `primaryEnv` metadata. Keep all real values outside this repository.

OpenClaw's per-skill environment injection applies to host execution, not automatically to sandbox containers. For sandbox/node execution, install the dependencies and provide variables, configuration, source files, and a writable persistent logfile **inside that execution environment**. The helper must be able to reach the instance from there.

## Usage

Ask the agent, for example:

> Upload `/path/to/report.pdf` to Linx and give me the link, expiring in one hour.

Or run the helper directly:

```sh
python3 scripts/upload.py -- /path/to/report.pdf
python3 scripts/upload.py --expiry 3600 --randomize -- /path/to/report.pdf
python3 scripts/upload.py --name shared-report.pdf --direct -- /path/to/report.pdf
python3 scripts/upload.py -- /path/to/first.png /path/to/second.pdf
```

Options precede `--`; quote paths containing spaces. Stdout contains one URL per successful file; diagnostics go to stderr. The server controls allowed expiry and naming policies. `--expiry 0` requests no expiry (the client omits its expiry header for zero); server defaults/limits still apply. No expiry option leaves the server default unchanged. `--direct` falls back to the public page URL if no direct URL is available.

Only regular local files are supported. Stdin, overwrite, deletion, password protection, and burn-after-read are outside this skill's interface. Deletion keys remain available locally for separate client management, such as `linx-client -c "$LINX_CONFIG" -d 'UPLOAD_URL'`, provided that config points to the same logfile. Environment-only users must configure the client separately before using it for management.

## Backend behavior and failures

1. Resolve and validate settings and source files before uploading.
2. If `linx-client` exists on PATH, run it with `-c` and `-no-cb`. No curl dependency is required for this path.
3. Otherwise, curl sends a PUT to `<base>/upload/<encoded-filename>` with JSON response negotiation, optional API key, expiry, and randomization headers. Credentials are passed via a private header file rather than curl arguments. Curl configuration files are disabled, TLS verification remains enabled, and redirects are not followed.
4. Save deletion keys locally. The fallback compares a returned SHA-256 checksum against the source file; a missing checksum produces a warning. The client performs its own comparison; client warnings are treated as failures rather than successful verification.

There are no automatic retries or fallback after a binary error, including an incompatible installed client. This avoids duplicate uploads. The helper also detects client upload errors printed to stdout with a zero exit status. A timeout, malformed response, checksum failure, or logfile-write error can leave an uploaded file on the server. Inspect the private logfile/server before retrying. In a batch, earlier successes remain uploaded and their URLs have already been printed.

## Privacy

Instance addresses, API keys, and deletion keys belong in private runtime configuration, never skill text or Git. Generated share links necessarily reveal their serving hostname. Only request sharing when that disclosure is acceptable. The helper suppresses raw subprocess/server errors to avoid echoing private settings; it does not hide network destinations from the local OS, proxy, or server operator. No real instance is contacted by the local verification suite.

## Verification

```sh
python3 -m unittest discover -s tests -v
```

The suite uses a loopback HTTP server and real curl. Set `LINX_TEST_CLIENT` to the built fork's binary to additionally exercise actual client uploads against that server.

## License

MIT © 2026 Lanjelin. See [LICENSE](LICENSE). The separately installed linx-client retains its own GPL-3.0 license.
