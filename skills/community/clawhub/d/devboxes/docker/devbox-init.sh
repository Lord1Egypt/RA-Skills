#!/bin/bash
#
# devbox-init — called by the devbox agent with the assigned DEVBOX_ID.
# Usage: devbox-init <id>
#
# Builds URL env vars, writes env files, and sets up routing
# (Traefik or Cloudflare Tunnel) based on the assigned DEVBOX_ID.
#
set -e

if [ -z "${1:-}" ]; then
    echo "[devbox-init] ERROR: Missing argument. Usage: devbox-init <id>"
    exit 1
fi

export DEVBOX_ID="$1"

# Read port/tag defaults from the environment (set by entrypoint)
: "${VSCODE_PORT:=8000}"
: "${NOVNC_PORT:=8002}"
: "${APP_PORT_1:=8003}"
: "${APP_PORT_2:=8004}"
: "${APP_PORT_3:=8005}"
: "${APP_PORT_4:=8006}"
: "${APP_PORT_5:=8007}"
: "${DEVBOX_DOMAIN}"
: "${APP_TAG_1:=app1}"
: "${APP_TAG_2:=app2}"
: "${APP_TAG_3:=app3}"
: "${APP_TAG_4:=app4}"
: "${APP_TAG_5:=app5}"

echo "[devbox-init] Initializing with DEVBOX_ID=$DEVBOX_ID"

########################################
# Build APP_URL_* env vars
########################################
for i in 1 2 3 4 5; do
    tag_var="APP_TAG_$i"
    export "APP_URL_$i=https://${!tag_var}-${DEVBOX_ID}.${DEVBOX_DOMAIN}"
done
export VSCODE_URL="https://vscode-${DEVBOX_ID}.${DEVBOX_DOMAIN}"
export NOVNC_URL="https://novnc-${DEVBOX_ID}.${DEVBOX_DOMAIN}/vnc.html"

########################################
# Write env files
########################################
cat > /etc/devbox.env << EOF
export DEVBOX_ID=$DEVBOX_ID
export DEVBOX_DOMAIN=$DEVBOX_DOMAIN
export VSCODE_URL=$VSCODE_URL
export NOVNC_URL=$NOVNC_URL
$(for i in 1 2 3 4 5; do
    tag_var="APP_TAG_$i"
    port_var="APP_PORT_$i"
    echo "export APP_TAG_$i=${!tag_var}"
    echo "export APP_PORT_$i=${!port_var}"
    echo "export APP_URL_$i=$(eval echo \$APP_URL_$i)"
done)
EOF

# Make env vars available in all new shells
cp /etc/devbox.env /etc/profile.d/devbox.sh
grep -q '/etc/devbox.env' /root/.bashrc 2>/dev/null || echo ". /etc/devbox.env" >> /root/.bashrc

# Source into the current shell
. /etc/devbox.env

echo "[devbox-init] Env files written"

########################################
# Routing: Traefik or Cloudflare Tunnel
########################################
: "${ROUTING_MODE:=traefik}"

if [ "$ROUTING_MODE" = "cloudflared" ]; then
    ########################################
    # Cloudflare Tunnel routing
    ########################################
    echo "[devbox-init] Routing mode: cloudflared"

    if [ -z "${CF_TUNNEL_TOKEN:-}" ]; then
        echo "[devbox-init] ERROR: CF_TUNNEL_TOKEN is required for cloudflared routing mode"
        exit 1
    fi

    # Build ingress config
    CF_CONFIG_DIR="/etc/cloudflared"
    mkdir -p "$CF_CONFIG_DIR"

    cat > "${CF_CONFIG_DIR}/config.yml" << CFEOF
ingress:
  - hostname: vscode-${DEVBOX_ID}.${DEVBOX_DOMAIN}
    service: http://localhost:${VSCODE_PORT}
  - hostname: novnc-${DEVBOX_ID}.${DEVBOX_DOMAIN}
    service: http://localhost:${NOVNC_PORT}
$(for i in 1 2 3 4 5; do
    tag_var="APP_TAG_$i"
    port_var="APP_PORT_$i"
    echo "  - hostname: ${!tag_var}-${DEVBOX_ID}.${DEVBOX_DOMAIN}"
    echo "    service: http://localhost:${!port_var}"
done)
  - service: http_status:404
CFEOF

    echo "[devbox-init] Cloudflared config written: ${CF_CONFIG_DIR}/config.yml"

    # Register DNS records via CF API
    if [ -n "${CF_API_TOKEN:-}" ] && [ -n "${CF_ZONE_ID:-}" ] && [ -n "${CF_TUNNEL_ID:-}" ]; then
        HOSTNAMES="vscode-${DEVBOX_ID}.${DEVBOX_DOMAIN} novnc-${DEVBOX_ID}.${DEVBOX_DOMAIN}"
        for i in 1 2 3 4 5; do
            tag_var="APP_TAG_$i"
            HOSTNAMES="$HOSTNAMES ${!tag_var}-${DEVBOX_ID}.${DEVBOX_DOMAIN}"
        done

        for h in $HOSTNAMES; do
            curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/dns_records" \
                -H "Authorization: Bearer ${CF_API_TOKEN}" \
                -H "Content-Type: application/json" \
                -d "{\"type\":\"CNAME\",\"name\":\"${h}\",\"content\":\"${CF_TUNNEL_ID}.cfargotunnel.com\",\"proxied\":true}" \
                > /dev/null 2>&1 || true
        done
        echo "[devbox-init] DNS records registered for devbox-${DEVBOX_ID}"
    else
        echo "[devbox-init] WARNING: CF_API_TOKEN/CF_ZONE_ID/CF_TUNNEL_ID not set, skipping DNS registration"
    fi

    # Start cloudflared tunnel
    cloudflared tunnel --config "${CF_CONFIG_DIR}/config.yml" run --token "${CF_TUNNEL_TOKEN}" &
    echo "[devbox-init] Cloudflared tunnel started"

else
    ########################################
    # Traefik registration (default)
    ########################################
    echo "[devbox-init] Routing mode: traefik"

    TRAEFIK_DIR="/traefik"
    if [ -d "$TRAEFIK_DIR" ]; then
        CONTAINER_NAME=$(hostname)
        CONFIG_FILE="${TRAEFIK_DIR}/devbox-${DEVBOX_ID}.yml"

        python3 -c "
import sys
devbox_id = '${DEVBOX_ID}'
container = '${CONTAINER_NAME}'
domain = '${DEVBOX_DOMAIN}'

services = {'vscode': ${VSCODE_PORT}, 'novnc': ${NOVNC_PORT}}
tags = ['${APP_TAG_1}','${APP_TAG_2}','${APP_TAG_3}','${APP_TAG_4}','${APP_TAG_5}']
ports = [${APP_PORT_1},${APP_PORT_2},${APP_PORT_3},${APP_PORT_4},${APP_PORT_5}]
for tag, port in zip(tags, ports):
    services[tag] = port

lines = ['http:', '  routers:']
for name in services:
    svc = f'{name}-{devbox_id}'
    lines += [
        f'    {svc}:',
        f'      rule: \"Host(\`{svc}.{domain}\`)\"',
        f'      service: {svc}',
        f'      entryPoints:',
        f'        - web',
    ]
lines.append('  services:')
for name, port in services.items():
    svc = f'{name}-{devbox_id}'
    lines += [
        f'    {svc}:',
        f'      loadBalancer:',
        f'        servers:',
        f'          - url: \"http://{container}:{port}\"',
    ]
with open('${CONFIG_FILE}', 'w') as f:
    f.write('\n'.join(lines) + '\n')
"
        echo "[devbox-init] Traefik config written: $CONFIG_FILE"
    else
        echo "[devbox-init] WARNING: /traefik not mounted, skipping Traefik registration"
    fi
fi

########################################
# Summary
########################################
echo "[devbox-init] URLs:"
echo "  VSCode:  $VSCODE_URL"
echo "  noVNC:   $NOVNC_URL"
for i in 1 2 3 4 5; do
    tag_var="APP_TAG_$i"
    port_var="APP_PORT_$i"
    url_var="APP_URL_$i"
    echo "  App $i (${!tag_var}): port=${!port_var} url=${!url_var}"
done
echo "[devbox-init] Done."
