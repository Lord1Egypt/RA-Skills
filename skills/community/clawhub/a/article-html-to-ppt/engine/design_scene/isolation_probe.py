"""Fixed, non-networking-to-the-internet probe for the deployment boundary.

Run with ``python -m engine.design_scene.isolation_probe --output-dir DIR``.
The worker attempts loopback TCP and a task-local Unix socket, and reads/writes
its own sentinel outside the permitted child directory. No user files are used.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import uuid
from pathlib import Path

from .runtime import clean_environment, run_process, sandbox_command
from .store import DesignError, Store


def probe():
    result = {}
    with socket.socket() as s:
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", 9))
            result["ip_network_denied"] = False
        except PermissionError:
            result["ip_network_denied"] = True
        except OSError:
            result["ip_network_denied"] = False  # Connection refused is not sandbox enforcement.
    for key, action in (
        ("outside_read_denied", lambda: Path("../sentinel.txt").read_bytes()),
        ("outside_write_denied", lambda: Path("../sentinel.txt").write_bytes(b"unexpected")),
    ):
        try:
            action()
            result[key] = False
        except PermissionError:
            result[key] = True
    Path("inside.txt").write_bytes(b"allowed")
    result["inside_write_allowed"] = Path("inside.txt").read_bytes() == b"allowed"
    name = "./OSL_PIPE_" + str(os.getuid()) + "_SingleOfficeIPC_" + uuid.uuid4().hex
    with socket.socket(socket.AF_UNIX) as server:
        server.bind(name)
        server.listen(1)
        result["private_local_ipc_allowed"] = True
    os.unlink(name)
    print(json.dumps(result))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir")
    p.add_argument("--worker", action="store_true")
    args = p.parse_args()
    if args.worker:
        probe()
        return 0
    if not args.output_dir:
        p.error("--output-dir is required")
    with Store(args.output_dir, create=True) as store:
        run = "probe-" + uuid.uuid4().hex
        store.write(run + "/sentinel.txt", b"preserved", exclusive=True)
        store.write(run + "/child/tmp/.owner", b"probe", exclusive=True)
        child = store.root / run / "child"
        command = sandbox_command([sys.executable, "-B", "-m", "engine.design_scene.isolation_probe", "--worker"], child, "macos")
        try:
            result = json.loads(run_process(command, cwd=child, timeout=15, env=clean_environment(child)))
            result["sentinel_preserved"] = store.read(run + "/sentinel.txt") == b"preserved"
            result["status"] = "passed" if all(result.values()) else "failed"
        except (DesignError, OSError, ValueError) as exc:
            result = {"status": "failed", "error": str(exc)}
        store.put_json(run + "/result.json", result, exclusive=True)
        print(json.dumps({**result, "record": run + "/result.json"}, indent=2))
        return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
