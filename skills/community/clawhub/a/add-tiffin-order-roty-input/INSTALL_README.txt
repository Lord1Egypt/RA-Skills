Goal: register add-tiffin-order-roty-input so the gateway will route Telegram messages matching (?i)\broty input\b to scripts/handle_message.py (isolated, API-only).

Files created:
- /data/.openclaw/workspace/skills/add-tiffin-order-roty-input/skill.json  (manifest)

Recommended registration steps (run on the host):

1) Copy manifest into the container (if not already):

docker exec -i openclaw-y89t-openclaw-1 bash -lc 'cat > /tmp/roty_entry.json <<"JSON"\n'"$(cat /data/.openclaw/workspace/skills/add-tiffin-order-roty-input/skill.json)"'\nJSON'

2) Try to install via ClawHub (preferred):

# From host: install the skill package using npx clawhub (container runs it)
docker exec -it openclaw-y89t-openclaw-1 bash -lc 'cd /data/.openclaw/workspace/skills && npx clawhub install ./add-tiffin-order-roty-input || echo "clawhub install failed; see fallback below"'

3) If ClawHub install doesn't apply for your build, use the OpenClaw skills CLI check/enable sequence:

# Check system-wide skill readiness
docker exec -it openclaw-y89t-openclaw-1 bash -lc 'openclaw skills check'

# List current registered skills
docker exec -it openclaw-y89t-openclaw-1 bash -lc 'openclaw skills list'

# If your build supports an enable/install command, use it. If not, Fall back to step 4.

4) Fallback immediate approach (exec wrapper + LLM routing until registration is available)
- I can create a small wrapper script that the LLM or any existing hook can call to run the handler with ROTIES_FORCE_API_ONLY enforced. (This is a temporary measure.)

Verification (after install):
- Restart container: docker restart openclaw-y89t-openclaw-1
- Run DRY_RUN: docker exec -it openclaw-y89t-openclaw-1 bash -lc 'cd /data/.openclaw/workspace/skills/add-tiffin-order-roty-input && DRY_RUN=1 python3 scripts/handle_message.py OPENCLAW "Roty input Test User 60 Kwinana St Glen Waverley veg 6 rotis tomorrow" --openclaw'
- Send a Telegram test message and check logs: docker logs -f openclaw-y89t-openclaw-1

If you run the install step(s) and paste the output here, I’ll verify and walk you through the DRY_RUN and live test.
