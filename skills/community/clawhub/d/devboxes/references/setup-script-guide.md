# Project Setup Script Guide

Each project can include `.openclaw/setup.sh` to automate environment setup inside a devbox.

## Available Environment Variables

The setup script has access to:

- `APP_PORT_1..5` — Internal container ports (8003-8007)
- `APP_TAG_1..5` — Route tag names (e.g. api, kiosk, console)
- `APP_URL_1..5` — Full external URLs (e.g. https://api-1.oc.example.com)
- `DEVBOX_ID` — The devbox numeric ID
- `DEVBOX_DOMAIN` — Base domain
- `NVM_DIR` — nvm is pre-installed at `/root/.nvm`

## Conventions

- Use `nvm install` / `nvm use` (reads `.nvmrc`) — do not hardcode Node versions
- Use `APP_PORT_x` for the project's listen port
- Use `APP_URL_x` for the project's external URL
- DB/Redis host: `172.17.0.1` (Docker gateway to host)
- Use `tar --no-same-owner` when extracting archives (avoids ownership errors)
- Start long-running processes in tmux sessions

## Example

```bash
#!/bin/bash

export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

nvm install
nvm use
npm install

cp template.env dev-local.env
sed -i "s/PORT=.*/PORT=$APP_PORT_1/" dev-local.env

source ./dev-local.env
tmux new -d -s my-server "source /root/.nvm/nvm.sh; nvm use; npm run start:dev; exec \$SHELL"

echo "Server running at $APP_URL_1"
```
