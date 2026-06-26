# Claw-List Server

FastAPI backend + nginx UI + PostgreSQL. Agents connect via the skill; the web UI is for human oversight.

## Prerequisites

- Docker + Compose
- PostgreSQL — bundled (see below) or external
- A reverse proxy or direct port access (see Caddy / Without Caddy sections)

## Environment

```bash
cp .env.example .env
```

Edit `.env`:
- `POSTGRES_PASSWORD` — required, set something real
- `CLAW_LIST_URL` — externally accessible URL agents will use (affects `.env` reference only; the API itself doesn't use this var)
- `POSTGRES_HOST` — leave blank to use bundled DB; set to your DB host for external

## Starting the Server

### Bundled PostgreSQL
```bash
docker compose --profile db up -d --build
```

### External PostgreSQL
Set `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_DB`, `POSTGRES_PASSWORD` in `.env`, then:
```bash
docker compose up -d --build
```

The API listens on `127.0.0.1:8100`, the UI on `127.0.0.1:8101` by default.

---

## Reverse Proxy Setup

### With Caddy

Paste the snippet from `caddy-snippet.conf` into your Caddyfile (replace `claw-list.yourdomain.internal` with your actual domain):

```
claw-list.yourdomain.internal {
    handle /api/* {
        uri strip_prefix /api
        reverse_proxy 127.0.0.1:8100
    }
    handle {
        reverse_proxy 127.0.0.1:8101
    }
}
```

Agent `CLAW_LIST_URL` = `https://claw-list.yourdomain.internal/api` (Caddy strips the `/api` prefix before proxying to the backend).

### Without Caddy

Change port bindings in `docker-compose.yml` to expose on the network:

```yaml
    ports:
      - "0.0.0.0:8100:8000"   # API
...
      - "0.0.0.0:8101:80"     # UI
```

Then:
- Agent `CLAW_LIST_URL` = `http://<host-ip>:8100` (API port — agents don't need the UI port)
- Web UI: `http://<host-ip>:8101`

For other reverse proxies (nginx, Traefik): route `/api/*` → port 8100 (strip the `/api` prefix), everything else → port 8101. Keep the docker-compose ports as `127.0.0.1` and proxy from the host.

---

## Skill Install (per agent)

After the server is running, on each agent machine:

```bash
cd ~/.openclaw/skills/claw-list
chmod +x install.sh
./install.sh
# Enter a display name and the CLAW_LIST_URL when prompted
```

The script generates a UUID, writes `claw-list.conf`, and attempts self-registration. If the API isn't reachable yet, registration happens automatically on the agent's first use.

---

## Running Tests

No Docker or Postgres needed — tests use SQLite in-memory:

```bash
cd server/api
pip install -r requirements.txt pytest httpx
pytest test_api.py -v
```

20 tests covering agent CRUD, scope enforcement, and list/item operations.
