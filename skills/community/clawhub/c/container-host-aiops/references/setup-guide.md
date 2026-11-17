# container-host-aiops setup & security guide

> The Docker path has been exercised against a live daemon; the Portainer and Podman
> paths are mock-validated only (see `docs/VERIFICATION.md`).
> `container-host-aiops doctor` is the fastest live check on any platform.

## 1. Install

```bash
uv tool install container-host-aiops     # or: pipx install container-host-aiops
```

## 2. What you need

- **Docker (unix socket)** — read/write access to the Docker socket (default
  `/var/run/docker.sock`). No secret is stored; the socket's file permissions are
  the trust boundary. Treat socket access as **root-equivalent** on the host.
- **Docker (TCP)** — a host + port (2375 plain, 2376 TLS). Enable TLS in
  production; a plain TCP daemon is unauthenticated.
- **Portainer** — the Portainer host + HTTPS port (default 9443), an **API token**
  (Portainer → My account → Access tokens), and the **endpoint id** of the managed
  Docker environment you want to read/manage (list them with `stack endpoints`).
- **Podman (unix socket)** — a running Podman **service** socket (rootful
  `/run/podman/podman.sock`, or rootless `$XDG_RUNTIME_DIR/podman/podman.sock` after
  `systemctl --user enable --now podman.socket`). No secret; the socket's file
  permissions are the trust boundary. Autodetection prefers the rootless socket,
  then the rootful one.

## 3. Onboard (interactive)

```bash
container-host-aiops init
```

The wizard asks, per target, for the **platform** (`docker` / `portainer` / `podman`):

- **docker** — connect over a **unix socket** (path, default `/var/run/docker.sock`)
  or a **TCP host** (host + optional TLS). No secret.
- **portainer** — host, HTTPS port, managed **endpoint id**, TLS verification, and
  the **API token** (stored encrypted). A master password (used to encrypt
  `secrets.enc`) is prompted the first time a Portainer token is stored.
- **podman** — connect over a **unix socket** (path defaults to the autodetected
  rootless/rootful Podman socket) or a **TCP host**. No secret. Podman speaks the
  Docker-compatible API (so all Docker reads/writes/analyses work) plus libpod-native
  pod reads (`pod list`).

Non-secret connection details go to `~/.container-host-aiops/config.yaml`; a
Portainer token goes to `~/.container-host-aiops/secrets.enc` (encrypted).

### Manual config (`~/.container-host-aiops/config.yaml`)

```yaml
targets:
  - name: local
    platform: docker
    socket_path: /var/run/docker.sock

  - name: remote-tcp
    platform: docker
    host: 10.0.0.5
    port: 2376
    verify_ssl: true

  - name: portainer1
    platform: portainer
    host: portainer.lan
    port: 9443
    endpoint_id: "1"
    verify_ssl: false        # true in production

  - name: podman-local
    platform: podman
    # socket_path omitted → autodetect rootless ($XDG_RUNTIME_DIR/podman/podman.sock)
    # then rootful (/run/podman/podman.sock); set socket_path to pin one explicitly.
```

Then store the Portainer token (encrypted):

```bash
container-host-aiops secret set portainer1
container-host-aiops doctor
```

## 4. Credentials & security

- Only **Portainer** needs a secret; **Docker and Podman** sockets need none (file
  permissions are the boundary). The Portainer API token is **never** written to disk
  in plaintext — it lives encrypted in `~/.container-host-aiops/secrets.enc` (Fernet /
  AES-128 + a scrypt-derived key; chmod 600). The master password is never stored.
- The master password is resolved from `CONTAINER_HOST_AIOPS_MASTER_PASSWORD`
  (non-interactive / MCP / CI) or an interactive prompt (CLI on a TTY).
- A legacy plaintext env var `CONTAINER_HOST_<TARGET_NAME_UPPER>_TOKEN` is honoured
  as a fallback with a deprecation warning (migrate with `secret migrate`).
- The token is sent in the `X-API-Key` header at request time and held only in
  memory; secrets are never logged or echoed.
- `verify_ssl` defaults to true; disable only for a self-signed Portainer / TLS
  Docker daemon in a lab. A unix-socket Docker/Podman target does not use TLS.

## 5. Governance

Every MCP tool runs through the bundled `@governed_tool` harness:

- **Audit** — all calls logged to `~/.container-host-aiops/audit.db` (relocatable via
  `CONTAINER_HOST_AIOPS_HOME`), agent-attributed, secret-redacted.
- **Runaway guard** — a safety backstop (not authorization): a tight-loop breaker
  plus optional call/time ceilings. Disable with `CONTAINER_HOST_RUNAWAY_MAX=0`.
- **Risk tier** — a descriptive label on each audit row derived from `risk_level`;
  it gates nothing. `CONTAINER_HOST_AUDIT_APPROVED_BY` / `CONTAINER_HOST_AUDIT_RATIONALE`
  are optional annotations recorded on the row, never required.
- **Undo recording** — reversible writes capture the before-state and record an
  inverse (`stop`→`start`, `update_container`→restore prior limits).

## 6. Verify

```bash
container-host-aiops doctor            # Docker/Podman: GET /version · Portainer: GET /api/endpoints
container-host-aiops overview          # one-shot host health
```

## Missing a capability?

Coverage is a curated subset of the Docker Engine + Portainer + Podman (libpod)
APIs. Missing a call or want another container host family? **Open an issue or PR**
— contributions welcome.
