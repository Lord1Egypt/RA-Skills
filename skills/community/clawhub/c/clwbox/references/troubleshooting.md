# Troubleshooting

## Cannot connect to API

```
Cannot connect to API at https://clawbox.ink
```

- Check if the server is running: `clawbox status`
- For local dev, start the server: `python -m src.main`
- Check the configured URL: `clawbox config --show`
- Change the URL: `clawbox config --api-url http://localhost:8000`

## Missing token

```
No token configured. Run 'clawbox init' first.
```

```bash
clawbox init
# Or set manually:
clawbox config --token <token>
```

## Search unavailable

```
Search is not available. Google API key not configured.
```

Search requires a Google API key (Gemini) configured on the server side. This is a server config issue, not a CLI issue. If self-hosting, add `GOOGLE_API_KEY` to your `.env`.

## Local Docker returns Internal Server Error

```
Failed to list files: Internal Server Error
```

If you self-hosted with Docker Compose, the app container is up but the database
schema has not been migrated yet. Run:

```bash
docker compose exec app alembic upgrade head
```

Then point the CLI at your local server and get a local token if needed:

```bash
clawbox config --api-url http://localhost:8000
clawbox init
```

## Upload fails with 413

```
Storage quota exceeded
```

- Anonymous tokens have 10 MB storage
- Sign in with Google at the web UI for 1 GB
- Check current usage: `clawbox status`

## Embedding failed

```
Embedding failed — file stored but not searchable
```

The file was uploaded but text extraction or embedding generation failed. Retry with:

```bash
clawbox embed <file_id>
# Or retry all failed:
clawbox embed --failed
```

## Invalid or expired token

```
Invalid or expired token
```

The token in your config no longer exists on the server. Get a new one:

```bash
clawbox init
```

Note: this creates a new token — you won't have access to files from the old token unless you sign in with the same Google account.
