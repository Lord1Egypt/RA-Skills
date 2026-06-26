#!/usr/bin/env python3
"""
Claw Stack Manager v5 — stack operations via Portainer API.
Portainer 2.41 compatible: preserves stack Env vars during redeploy.

- Claw stack → one-shot redeployer: stop → PUT (compose + env) → async deploy
- Other stacks → same PUT-based flow
"""
import json, os, urllib.parse, urllib.request, sys
from datetime import datetime, timezone, timedelta

# Auto-load .env from workspace root
_env_path = '/home/node/.openclaw/workspace/liyj/.env'
if os.path.isfile(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and '=' in _line and not _line.startswith('#'):
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

KEY = os.environ.get("PORTAINER_API_KEY")
if not KEY:
    print("❌ PORTAINER_API_KEY environment variable is required")
    sys.exit(1)

HOST = os.environ.get("PORTAINER_URL")
if not HOST:
    print("❌ PORTAINER_URL environment variable required")
    sys.exit(1)

IMAGE = os.environ.get("CLAW_IMAGE", "liyujiang/openclaw:latest")
EP = int(os.environ.get("PORTAINER_ENDPOINT", "2"))
CLAW_STACK_ID = int(os.environ.get("CLAW_STACK_ID", "89"))

STACK_NAMES = {
    "claw": 89,
    "searxng": 92,
    "openclaw-liyj": 97,
}

cst = timezone(timedelta(hours=8))

def log(msg):
    t = datetime.now().astimezone(cst).strftime("%H:%M:%S")
    print(f"  [{t}] {msg}")

def api(method, path, data=None, timeout=30, raw=False):
    req = urllib.request.Request(f"{HOST}/api{path}", method=method)
    req.add_header("X-API-Key", KEY)
    req.add_header("Content-Type", "application/json")
    if data is not None:
        req.data = json.dumps(data).encode()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        if raw:
            return resp.status, resp.read()
        return resp.status, json.loads(resp.read())
    except Exception as e:
        return 0, {"error": str(e)}

def resolve_stack(stack_arg):
    """Resolve --stack to (id, name). Accepts numeric id or name string."""
    if not stack_arg:
        return CLAW_STACK_ID, f"stack#{CLAW_STACK_ID}"
    try:
        sid = int(stack_arg)
        return sid, f"stack#{sid}"
    except ValueError:
        s = stack_arg.lower()
        if s in STACK_NAMES:
            return STACK_NAMES[s], s
        log(f"❌ Unknown stack name '{stack_arg}', try numeric id")
        sys.exit(1)

def pull_image():
    log(f"Pulling: {IMAGE}")
    status, body = api("POST", f"/endpoints/{EP}/docker/images/create?fromImage={IMAGE}",
                       timeout=600, raw=True)
    if status in (200, 201):
        log("✅ Image pulled")
        return True
    log(f"❌ Pull failed (HTTP {status})")
    return False

def get_stack_config(stack_id):
    """Get current compose content and Env for a stack."""
    s1, stack = api("GET", f"/stacks/{stack_id}")
    if s1 != 200:
        log(f"❌ Failed to get stack: HTTP {s1}")
        return None, None
    env = stack.get("Env", [])

    s2, file_resp = api("GET", f"/stacks/{stack_id}/file")
    if s2 != 200:
        log(f"❌ Failed to get stack file: HTTP {s2}")
        return None, None
    content = file_resp.get("StackFileContent", "")

    return content, env

def get_stack_status(stack_id):
    """Check if stack is already inactive."""
    s, stack = api("GET", f"/stacks/{stack_id}")
    return stack.get("Status") if s == 200 else None

def cleanup_container(name):
    """Remove stale containers by name pattern."""
    enc = urllib.parse.quote(json.dumps({"name": [name]}))
    s, cs = api("GET", f"/endpoints/{EP}/docker/containers/json?all=true&filters={enc}")
    for c in (cs or []):
        api("DELETE", f"/endpoints/{EP}/docker/containers/{c['Id']}?force=true")

def create_update_redeployer(stack_id, new_content=None, env=None):
    """
    Create one-shot redeployer that:
    1. Stops the stack (skip if already inactive)
    2. PUT updated compose + env → triggers async deploy
    """
    if new_content is None or env is None:
        new_content, env = get_stack_config(stack_id)
        if new_content is None:
            return False

    # Check if stack is already stopped
    status = get_stack_status(stack_id)
    need_stop = status != 2  # 2 = inactive

    payload = json.dumps({
        "StackFileContent": new_content,
        "Env": env,
        "RepullImageAndRedeploy": False,
        "Prune": False
    })

    log(f"Stack env vars ({len(env)}): {[e.get('name','?') for e in env]}")

    if need_stop:
        script = (
            'apk add -q curl\n'
            f'echo "R: 1/2 Stopping stack {stack_id}..."\n'
            f'curl -sS -X POST -H "X-API-Key: {KEY}" '
            f'{HOST}/api/stacks/{stack_id}/stop?endpointId={EP} >/dev/null\n'
            f'echo ""\n'
            f'echo "R: 2/2 Deploying with updated config..."\n'
            f'curl -sS -X PUT -H "X-API-Key: {KEY}" '
            f'-H "Content-Type: application/json" '
            f'-d \'@-\' '
            f'{HOST}/api/stacks/{stack_id}?endpointId={EP} << "PAYLOAD"\n'
            f'{payload}\n'
            f'PAYLOAD\n'
            f'echo ""\n'
            f'echo "R: Done."\n'
        )
    else:
        script = (
            'apk add -q curl\n'
            f'echo "R: Stack already stopped, deploying..."\n'
            f'curl -sS -X PUT -H "X-API-Key: {KEY}" '
            f'-H "Content-Type: application/json" '
            f'-d \'@-\' '
            f'{HOST}/api/stacks/{stack_id}?endpointId={EP} << "PAYLOAD"\n'
            f'{payload}\n'
            f'PAYLOAD\n'
            f'echo ""\n'
            f'echo "R: Done."\n'
        )

    # Use unique name to avoid collision
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    container_name = f"claw-redep-{ts}"

    config = {
        "Image": "alpine:latest",
        "Cmd": ["/bin/sh", "-c", script.strip()],
        "HostConfig": {"NetworkMode": "host"},
        "Labels": {"io.portainer.stack.name": f"redeployer-{stack_id}"}
    }

    cleanup_container("claw-redep-")
    cleanup_container("ng-agent")

    log("Creating one-shot redeployer container...")
    status, result = api("POST",
        f"/endpoints/{EP}/docker/containers/create?name={container_name}",
        data=config, timeout=30)

    if status not in (200, 201, 204):
        log(f"❌ Create failed: {result.get('error', str(result)[:200])}")
        return False

    cid = result.get("Id", "")
    if not cid:
        log("❌ No container ID returned")
        return False

    log(f"Redeployer: {cid[:20]}...")
    api("POST", f"/endpoints/{EP}/docker/containers/{cid}/start", timeout=10)
    log("✅ Redeployer launched")
    return True

def container_restart():
    enc = urllib.parse.quote(json.dumps({"name": ["openclaw-gateway"]}))
    s, containers = api("GET",
        f"/endpoints/{EP}/docker/containers/json?filters={enc}")
    if not containers:
        log("❌ Container not found")
        return False
    cid = containers[0]["Id"]
    log(f"Restarting {cid[:20]}...")
    s, _ = api("POST", f"/endpoints/{EP}/docker/containers/{cid}/restart", timeout=30)
    if s in (200, 204):
        log("✅ Restarted (~10s)")
        return True
    log(f"❌ HTTP {s}")
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage Docker stacks via Portainer API")
    parser.add_argument("--mode", choices=["update", "restart", "pull-only"],
                        required=True)
    parser.add_argument("--stack", default="",
                        help="Stack id or name (default: claw)")
    parser.add_argument("--no-pull", action="store_true",
                        help="Skip image pull before redeploy")

    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Stack Manager v5 — mode: {args.mode}")
    print(f"{'='*50}\n")

    if args.mode == "restart":
        container_restart()
        return

    if args.mode == "pull-only":
        pull_image()
        return

    if args.mode == "update":
        stack_id, stack_name = resolve_stack(args.stack)

        if not args.no_pull:
            if not pull_image():
                log("❌ ABORTED: image pull failed")
                sys.exit(1)

        content, env = get_stack_config(stack_id)
        if content is None:
            sys.exit(1)

        log(f"Redeploying {stack_name} (id={stack_id})...")
        create_update_redeployer(stack_id, content, env)

        if stack_id == CLAW_STACK_ID:
            log("⚠️  Gateway will restart shortly. Session may disconnect.")

if __name__ == "__main__":
    main()
