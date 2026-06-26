# audiolla setup

## Requirements

- Linux/macOS host with Docker
- ~3 GB disk for the CPU image, ~8 GB for the CUDA image (PyTorch + CUDA runtime is heavy)
- 4 GB RAM minimum, 8 GB recommended (Demucs separation peaks around 3-5 GB)
- NVIDIA GPU + drivers + `nvidia-container-toolkit` for the CUDA variant (CUDA 12.6+)

## Quick install

CPU image — no GPU needed:

```bash
docker run -d --rm --name audiolla \
  -v $HOME/.audiolla-data:/data \
  -p 8000:8000 \
  psyb0t/audiolla:latest
```

CUDA image — GPU-accelerated Demucs separation:

```bash
docker run -d --rm --name audiolla \
  --gpus all \
  -v $HOME/.audiolla-data:/data \
  -e AUDIOLLA_DEVICE=cuda \
  -p 8000:8000 \
  psyb0t/audiolla:latest-cuda
```

First run downloads the image (~3 GB CPU, ~8 GB CUDA), then on container start prefetches Demucs model weights (~600 MB) into `/data/torch_cache/`. The model fetch logs to the container's stdout — `docker logs -f audiolla` to watch.

After that, subsequent runs reuse the volume and skip the download.

**Verify:** `curl http://localhost:8000/healthz` → `{"ok": true, "device": "cpu", "engines": [...]}`.

## Configuration

All config is via environment variables passed at `docker run`:

| Variable | Default | Description |
|----------|---------|-------------|
| `AUDIOLLA_DEVICE` | `auto` | `auto`, `cpu`, `cuda`, or `cuda:N` for a specific GPU |
| `AUDIOLLA_ENGINES_FILE` | `/app/engines.json` | path to engines registry |
| `AUDIOLLA_DATA_DIR` | `/data` | where models and staged files live |
| `AUDIOLLA_AUTH_TOKEN` | _(none)_ | bearer token; empty means no auth |
| `AUDIOLLA_ENABLED_ENGINES` | _(all)_ | comma-separated slugs to allow; empty = all |
| `AUDIOLLA_PRELOAD` | _(none)_ | comma-separated slugs to load into memory at startup |
| `AUDIOLLA_ENGINE_TTL` | `600` | seconds idle before an engine is unloaded (`10m` also works) |
| `AUDIOLLA_SWEEPER_INTERVAL` | `60` | how often the idle-engine sweeper runs, in seconds |
| `AUDIOLLA_MAX_UPLOAD_BYTES` | `209715200` | upload cap (default 200 MB); also caps remote URL fetch body size |
| `AUDIOLLA_FETCH_MODE` | `disabled` | `disabled` / `allowlist` / `denylist` — server-side fetch policy for `file_url` and `output_url` |
| `AUDIOLLA_FETCH_HOSTS` | _(none)_ | comma-separated host patterns (`bucket.s3.amazonaws.com`, `*.s3.amazonaws.com`) — required when mode=allowlist |
| `AUDIOLLA_FETCH_SCHEMES` | `https` | comma-separated schemes; add `http` only for trusted local networks |
| `AUDIOLLA_FETCH_ALLOW_PRIVATE` | `false` | allow URLs resolving to private / loopback / link-local IPs (e.g. internal MinIO) |
| `AUDIOLLA_FETCH_TIMEOUT` | `30` | per-fetch/upload timeout (seconds; also accepts `30s`, `1m`) |
| `AUDIOLLA_FETCH_MAX_REDIRECTS` | `5` | max redirects per fetch; each `Location` re-validated through the policy |
| `AUDIOLLA_SOUNDFONT` | `/usr/share/sounds/sf2/FluidR3_GM.sf2` (prod images) | Default SoundFont (`.sf2`) path used by `/v1/midi/render`. Empty = midi-render refuses unless `soundfont_path` is passed on the request. Prod images install FluidR3_GM via `apt install fluid-soundfont-gm`. |

### Authentication

By default audiolla runs with no auth — anyone who can reach port 8000 can use it. For anything beyond `localhost`, set a bearer token:

```bash
docker run -d --rm --name audiolla \
  -v $HOME/.audiolla-data:/data \
  -e AUDIOLLA_AUTH_TOKEN="$(openssl rand -hex 32)" \
  -p 8000:8000 \
  psyb0t/audiolla:latest
```

Every endpoint except `/healthz` then requires `Authorization: Bearer <token>`. Without it the server returns 401.

> **`AUDIOLLA_AUTH_TOKEN` must be set to a strong random value before audiolla is reachable by anything other than localhost.** Without a token, anyone who can hit port 8000 can run arbitrary audio processing on your hardware (Demucs is CPU/GPU-heavy — a hostile caller can keep your machine saturated indefinitely). They can also upload up to `AUDIOLLA_MAX_UPLOAD_BYTES` per request to your staging area. Generate a token with `openssl rand -hex 32` and keep it out of git.

### Remote URL fetching (file_url / output_url)

Audiolla can fetch input files from a URL and PUT outputs to presigned URLs (S3, R2, etc.). This is **disabled by default** because the fetch path is a classic SSRF surface — without guardrails, an attacker can use it to read your cloud metadata service or probe internal hosts.

Pick a mode that matches your setup:

```bash
# Default — no URL I/O.
-e AUDIOLLA_FETCH_MODE=disabled

# Allowlist — preferred. Only listed hosts can be fetched/PUT to.
-e AUDIOLLA_FETCH_MODE=allowlist
-e AUDIOLLA_FETCH_HOSTS="*.s3.amazonaws.com,*.r2.cloudflarestorage.com,my-bucket.example.com"

# Denylist — anything goes except listed hosts. Leaky by design — only
# safe with AUDIOLLA_FETCH_ALLOW_PRIVATE=false (the default), which
# already blocks private IPs and the metadata service. Use this only
# if you control the network or have a strong reason.
-e AUDIOLLA_FETCH_MODE=denylist
-e AUDIOLLA_FETCH_HOSTS="*.internal,localhost"
```

Host pattern syntax — exact match or single-wildcard subdomain. `*.s3.amazonaws.com` matches `bucket.s3.amazonaws.com` but NOT `s3.amazonaws.com` itself (add that explicitly if needed).

Always-on protections regardless of mode:

- DNS-resolved private / loopback / link-local IPs rejected. The AWS/GCP/Azure metadata service at `169.254.169.254` falls into this. Toggle off only if you genuinely need internal S3-compatible storage on a private network.
- Schemes restricted to `AUDIOLLA_FETCH_SCHEMES` (default `https`). `file://`, `gopher://`, etc. are always rejected.
- Each HTTP redirect's `Location` re-validated through the full policy before following.
- Body size capped at `AUDIOLLA_MAX_UPLOAD_BYTES` — streamed, abort on overrun.
- Every fetch / upload URL logged at INFO.

For internal MinIO / S3-compatible storage:

```bash
-e AUDIOLLA_FETCH_MODE=allowlist \
-e AUDIOLLA_FETCH_HOSTS=minio.internal.example.com \
-e AUDIOLLA_FETCH_ALLOW_PRIVATE=true
```

### Engine selection

Only enable the engines you actually need:

```bash
docker run -d --rm --name audiolla \
  -v $HOME/.audiolla-data:/data \
  -e AUDIOLLA_ENABLED_ENGINES=htdemucs,matchering,librosa-analyze \
  -p 8000:8000 \
  psyb0t/audiolla:latest
```

Disabled engines are absent from `GET /v1/engines` and return 404 on use.

### Preloading

By default, engines lazy-load on first request. To avoid the cold-start latency on critical engines, preload at startup:

```bash
docker run -d --rm --name audiolla \
  -v $HOME/.audiolla-data:/data \
  -e AUDIOLLA_PRELOAD=htdemucs,matchering \
  -p 8000:8000 \
  psyb0t/audiolla:latest
```

Preload happens during container startup; the server doesn't accept traffic until preload finishes. Failed preloads log a warning and continue.

### Idle unload

The idle sweeper unloads engines that haven't been used for `AUDIOLLA_ENGINE_TTL` seconds. This frees memory (Demucs holds several GB when loaded). Set to `0` to disable.

```bash
-e AUDIOLLA_ENGINE_TTL=10m       # Go-style duration
-e AUDIOLLA_ENGINE_TTL=600       # plain seconds
-e AUDIOLLA_ENGINE_TTL=0         # never unload
```

Memory footprints (approximate):
- `htdemucs` / `mdx_extra`: ~1.5 GB
- `htdemucs_ft`: ~2 GB (CUDA-only at usable speed)
- `htdemucs_6s`: ~2 GB
- `matchering`: ~200 MB
- `pedalboard-chain`, `librosa-analyze`, `sox-transform`: negligible (no model weights)

## Data directory layout

`/data` (or wherever `AUDIOLLA_DATA_DIR` points) contains:

```
/data/
  torch_cache/          # Demucs model weights — survives container restarts
    hub/checkpoints/    # downloaded .th files
  files/                # staging area for /v1/files endpoints
  models/               # additional model storage (currently unused)
  hf/                   # HuggingFace cache (CUDA image only — HF_HOME)
```

Mount the same path on subsequent runs to skip the model re-download and keep staged files.

## docker-compose

```yaml
services:
  audiolla:
    image: psyb0t/audiolla:latest        # or :latest-cuda
    container_name: audiolla
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"           # bind to loopback only
    volumes:
      - ./data:/data
    environment:
      AUDIOLLA_DEVICE: auto
      AUDIOLLA_AUTH_TOKEN: ${AUDIOLLA_AUTH_TOKEN}     # from .env
      AUDIOLLA_ENGINE_TTL: 10m
      AUDIOLLA_MAX_UPLOAD_BYTES: 209715200
    # For CUDA image only:
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
```

`.env`:

```bash
AUDIOLLA_AUTH_TOKEN=<openssl rand -hex 32 output>
```

## Logs

audiolla logs to stdout — read with `docker logs -f audiolla`. Key log lines:

- `audiolla starting: device=... engines=[...] ttl=... files_dir=... auth=on|off` — boot banner
- `[entrypoint] demucs variants to prefetch: [...]` — model prefetch
- `idle sweeper: unloading <slug> (idle ...s >= ...s)` — engine eviction
- `evicting N sibling engine(s) before loading <slug>` — pre-separation eviction
- `preload <slug> failed` — `AUDIOLLA_PRELOAD` entry couldn't load

## Public access

audiolla has no built-in TLS or reverse-proxy support. For public access:

1. **Set `AUDIOLLA_AUTH_TOKEN`** to a strong random value first. Non-negotiable.
2. Front it with a reverse proxy that terminates TLS (Caddy, nginx, Traefik).
3. Consider a tailnet-only deployment if you don't actually need internet exposure — Tailscale/WireGuard authenticate at the network layer.
4. Per-IP rate limiting at the proxy. Demucs runs at line rate against a hostile caller will pin a GPU or saturate every CPU core; rate limiting is the only thing between you and a denial-of-wallet event.

## Build from source

If you want to build the image yourself instead of pulling:

```bash
git clone https://github.com/psyb0t/docker-audiolla
cd docker-audiolla
make build         # CPU image
make build-cuda    # CUDA image
make run           # builds + runs CPU image on port 8000
```

Heavy ML deps are hash-locked in `requirements-heavy-{cpu,cuda}.txt`. Light deps live in `uv.lock`. Build will fail with a hash mismatch if anything has been tampered with — that's the design.

## Troubleshooting

**`/healthz` returns but engine calls 404 with "unknown engine"**
The engine is filtered out by `AUDIOLLA_ENABLED_ENGINES`. Check `GET /v1/engines` for what's actually exposed.

**`htdemucs_ft` returns 400 with "cuda_only"**
The CUDA-only fine-tuned variant won't run on the CPU image. Either use the CUDA image with `--gpus all`, or pick `htdemucs` / `htdemucs_ft`'s lighter sibling.

**Separation request hangs for minutes**
Demucs on CPU is slow — `htdemucs` on a 3-min track takes 1-3 min on a mid-range CPU; `htdemucs_ft` is ~4x that. CUDA image is 5-10x faster. Watch `docker logs -f audiolla` for engine load progress.

**Upload returns 413**
Hit the `AUDIOLLA_MAX_UPLOAD_BYTES` cap (default 200 MB). Bump it via env var, or use `/v1/files` PUT (same cap applies per upload but you can pipeline multiple files).

**Upload returns 401**
The server has `AUDIOLLA_AUTH_TOKEN` set and the request didn't carry `Authorization: Bearer ...` (or carried the wrong token).

**Container exits during startup**
Check `docker logs audiolla` for `preload <slug> failed` or engine-init exceptions. The most common cause is a corrupt `/data/torch_cache/` — delete the volume and let the container re-download.
