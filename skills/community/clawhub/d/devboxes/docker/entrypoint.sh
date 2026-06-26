#!/bin/bash
set -e

# Source nvm
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# Ports
: "${VSCODE_PORT:=8000}"
: "${NOVNC_PORT:=8002}"
: "${CDP_PORT:=9222}"
: "${APP_PORT_1:=8003}"
: "${APP_PORT_2:=8004}"
: "${APP_PORT_3:=8005}"
: "${APP_PORT_4:=8006}"
: "${APP_PORT_5:=8007}"

# Tags & domain
: "${DEVBOX_DOMAIN}"
: "${APP_TAG_1:=app1}"
: "${APP_TAG_2:=app2}"
: "${APP_TAG_3:=app3}"
: "${APP_TAG_4:=app4}"
: "${APP_TAG_5:=app5}"

echo "[devbox] Starting services..."

########################################
# Browser + CDP (sandbox-browser pattern)
########################################
# Xvfb virtual display
Xvfb :1 -screen 0 1280x800x24 -ac -nolisten tcp &
sleep 1

# Chromium with CDP on internal port
CHROME_CDP_INTERNAL=$((CDP_PORT + 1))
chromium \
    --remote-debugging-address=127.0.0.1 \
    --remote-debugging-port="${CHROME_CDP_INTERNAL}" \
    --user-data-dir=/tmp/.chrome \
    --no-first-run \
    --no-default-browser-check \
    --disable-dev-shm-usage \
    --disable-background-networking \
    --disable-features=TranslateUI \
    --disable-breakpad \
    --disable-crash-reporter \
    --metrics-recording-only \
    --no-sandbox \
    about:blank &

# Wait for CDP to be ready
for _ in $(seq 1 50); do
    if curl -sS --max-time 1 "http://127.0.0.1:${CHROME_CDP_INTERNAL}/json/version" >/dev/null 2>&1; then
        break
    fi
    sleep 0.1
done

# socat: expose CDP on 0.0.0.0 for OpenClaw browser tool
socat TCP-LISTEN:"${CDP_PORT}",fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:"${CHROME_CDP_INTERNAL}" &
echo "[devbox] CDP ready on port ${CDP_PORT}"

########################################
# VNC + noVNC
########################################
if [ "${ENABLE_VNC:-false}" = "true" ]; then
    VNC_PORT=5900
    x11vnc -display :1 -rfbport "${VNC_PORT}" -shared -forever -nopw -localhost &
    websockify --web=/usr/share/novnc "${NOVNC_PORT}" "localhost:${VNC_PORT}" > /dev/null 2>&1 &
    echo "[devbox] noVNC ready on port ${NOVNC_PORT}"
fi

########################################
# VSCode Web
########################################
if [ "${ENABLE_VSCODE:-false}" = "true" ]; then
    "${OPENVSCODE_SERVER_ROOT}/bin/openvscode-server" \
        --host 0.0.0.0 \
        --port "${VSCODE_PORT}" \
        --without-connection-token \
        --default-folder /workspace \
        > /dev/null 2>&1 &
    echo "[devbox] VSCode ready on port ${VSCODE_PORT}"
fi

########################################
# Summary
########################################
echo "[devbox] Services started. Ports:"
echo "  VSCode:  ${VSCODE_PORT}"
echo "  noVNC:   ${NOVNC_PORT}"
echo "  CDP:     ${CDP_PORT}"
for i in 1 2 3 4 5; do
    port_var="APP_PORT_$i"
    echo "  App $i: port=${!port_var}"
done
echo ""
echo "[devbox] DEVBOX_ID not yet assigned."
echo "[devbox] The agent must run: devbox-init <id>"
echo "[devbox] Ready."

exec "$@"
