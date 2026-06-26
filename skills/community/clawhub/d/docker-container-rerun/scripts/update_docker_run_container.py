#!/usr/bin/env python3
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


class CommandError(Exception):
    pass


@dataclass
class Result:
    container_name: str
    image: str
    current_image_id: Optional[str]
    latest_image_id: str
    needs_update: bool
    recreated: bool
    recreate_command: str


def run(cmd, check=True, capture=True):
    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=capture,
        check=False,
    )
    if check and proc.returncode != 0:
        raise CommandError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc


def validate_recreate_command(recreate_command: str) -> None:
    stripped = recreate_command.strip()
    if not stripped.startswith("docker run"):
        raise ValueError("recreate_command must start with 'docker run'")


def extract_image(recreate_command: str) -> str:
    tokens = shlex.split(recreate_command, posix=True)
    if len(tokens) < 3 or tokens[0] != "docker" or tokens[1] != "run":
        raise ValueError("recreate_command is not a valid docker run command")

    i = 2
    while i < len(tokens):
        token = tokens[i]
        if token == "--":
            i += 1
            break

        if token.startswith("-"):
            # Flags that consume the next token when provided in split form.
            if token in {
                "--name", "--network", "--restart", "-v", "--volume", "-p", "--publish",
                "-e", "--env", "--health-cmd", "--health-interval", "--health-retries",
                "--health-timeout", "--hostname", "--user", "--workdir", "--entrypoint",
                "--label", "--log-driver", "--log-opt", "--memory", "--cpus", "--platform",
                "--add-host", "--dns", "--dns-search", "--shm-size", "--ulimit", "--device",
                "--network-alias", "--stop-timeout", "--env-file", "--volume-from", "--ipc",
                "--pid", "--cgroup-parent", "--tmpfs", "--mount",
            }:
                i += 2
                continue
            # Flags in --flag=value or short clusters do not consume next token here.
            i += 1
            continue

        return token

    raise ValueError("could not extract image from recreate_command")


def get_current_image_id(container_name: str) -> Optional[str]:
    proc = run(["docker", "inspect", "-f", "{{.Image}}", container_name], check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def pull_image(image: str) -> None:
    proc = subprocess.run(["docker", "pull", image], text=True)
    if proc.returncode != 0:
        raise CommandError(f"docker pull failed for image: {image}")


def get_latest_image_id(image: str) -> str:
    proc = run(["docker", "image", "inspect", image, "--format", "{{.Id}}"])
    value = proc.stdout.strip()
    if not value:
        raise CommandError(f"could not read image Id for: {image}")
    return value


def stop_and_remove(container_name: str) -> None:
    run(["docker", "stop", container_name])
    run(["docker", "rm", container_name])


def recreate(recreate_command: str) -> None:
    proc = subprocess.run(recreate_command, shell=True, executable="/bin/bash", text=True)
    if proc.returncode != 0:
        raise CommandError("recreate_command execution failed")


def inspect_state(container_name: str) -> dict:
    ps = run(["docker", "ps", "--filter", f"name={container_name}", "--format", "{{json .}}"], check=False)
    inspect = run(["docker", "inspect", container_name], check=False)
    logs = run(["docker", "logs", "--tail", "100", container_name], check=False)

    parsed_inspect = None
    if inspect.returncode == 0 and inspect.stdout.strip():
        try:
            data = json.loads(inspect.stdout)
            if isinstance(data, list) and data:
                parsed_inspect = data[0]
        except json.JSONDecodeError:
            parsed_inspect = None

    health = None
    status = None
    if parsed_inspect:
        state = parsed_inspect.get("State") or {}
        status = state.get("Status")
        health = (state.get("Health") or {}).get("Status")

    return {
        "docker_ps": ps.stdout.strip(),
        "status": status,
        "health": health,
        "logs_tail": logs.stdout.strip() if logs.returncode == 0 else (logs.stderr.strip() or logs.stdout.strip()),
    }


def main():
    parser = argparse.ArgumentParser(description="Update a docker run container by comparing current and latest image Ids.")
    parser.add_argument("--container-name", required=True)
    parser.add_argument("--recreate-command", required=True)
    parser.add_argument("--apply", action="store_true", help="Actually stop/remove/recreate when image Id changed")
    args = parser.parse_args()

    validate_recreate_command(args.recreate_command)
    image = extract_image(args.recreate_command)
    current_image_id = get_current_image_id(args.container_name)
    pull_image(image)
    latest_image_id = get_latest_image_id(image)
    needs_update = current_image_id != latest_image_id
    recreated = False

    if needs_update and args.apply:
        stop_and_remove(args.container_name)
        recreate(args.recreate_command)
        recreated = True

    state = inspect_state(args.container_name)
    result = {
        "container_name": args.container_name,
        "image": image,
        "current_image_id": current_image_id,
        "latest_image_id": latest_image_id,
        "needs_update": needs_update,
        "recreated": recreated,
        "apply_mode": bool(args.apply),
        "post_state": state,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
