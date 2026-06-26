"""
_connect.py - Shared helper: connect to an existing E2B Desktop sandbox.
Sourced by other scripts via: exec(open('_connect.py').read())

After exec, 'desktop' is available as the connected Sandbox instance.
"""
import os, json, sys
from e2b_desktop import Sandbox

api_key = os.environ.get("E2B_API_KEY")
if not api_key:
    print("ERROR: E2B_API_KEY not set", file=sys.stderr)
    sys.exit(1)

sandbox_id = os.environ.get("E2B_SANDBOX_ID")
if not sandbox_id:
    state_path = os.path.expanduser("~/.e2b_state")
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
        sandbox_id = state.get("sandbox_id")

if not sandbox_id:
    print("ERROR: No sandbox ID found. Run start_sandbox.sh first or set E2B_SANDBOX_ID", file=sys.stderr)
    sys.exit(1)

desktop = Sandbox.connect(sandbox_id)
