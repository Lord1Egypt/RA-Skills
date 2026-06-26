# Troubleshooting

## WOODPECKER_TOKEN empty after init

The OAuth2 flow failed. Common causes:

1. **URL-encoded redirect_uri mismatch**: Forgejo logs show "Unregistered Redirect URI".
   The init script must rewrite both plain and URL-encoded Docker hostnames.

2. **Forgejo must_change_password**: Admin user was created with forced password change.
   The init script calls `--must-change-password=false` but Forgejo 11.x sometimes ignores it.

3. **WOODPECKER_OPEN not set**: WP refuses first-user OAuth registration without it.

Manual fix: reset admin password and re-run the token generation manually, or
use the Woodpecker UI to create a token.

## WP CI agent won't connect (DeadlineExceeded)

gRPC over Docker bridge fails in LXD (and possibly other nested container environments).
The compose template uses `network_mode: host` + `privileged: true` for the agent.
If you see this error, check:
- Server exposes port 9000: `grep "9000:9000" docker-compose.yml`
- Agent uses `localhost:9000`: `grep "WOODPECKER_SERVER" docker-compose.yml`
- Agent has `network_mode: host`

## CI clone fails (could not resolve host)

CI containers need to resolve Docker service names (e.g., `forgejo`).
Check `WOODPECKER_BACKEND_DOCKER_NETWORK` is set on the agent.

## Webhooks not delivered

Forgejo blocks outgoing webhooks by default. Check:
```bash
docker logs disinto-forgejo-1 2>&1 | grep "webhook.*ALLOWED_HOST_LIST"
```
Fix: add `FORGEJO__webhook__ALLOWED_HOST_LIST: "private"` to Forgejo environment.

Also verify the webhook exists:
```bash
curl -sf -u "disinto-admin:<password>" "http://localhost:3000/api/v1/repos/<org>/<repo>/hooks" | jq '.[].config.url'
```
If missing, deactivate and reactivate the repo in Woodpecker to auto-create it.

## Dev-agent fails with "cd: no such file or directory"

`PROJECT_REPO_ROOT` inside the agents container points to a host path that doesn't
exist in the container. Check the compose env:
```bash
docker inspect disinto-agents-1 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep PROJECT_REPO_ROOT
```
Should be `/home/agent/repos/<name>`, not `/home/<user>/<name>`.
