from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class MachineError(ValueError):
    pass


@dataclass(frozen=True)
class MachineProfile:
    name: str
    transport: str
    target: str | None
    workspace_root: str
    checkout_root: str
    aliases: tuple[str, ...] = ()

    def source_path_text(self, repo_dir: str) -> str:
        return f"{self.workspace_root.rstrip('/')}/{repo_dir}"

    def source_path(self, repo_dir: str) -> Path:
        value = self.source_path_text(repo_dir)
        return Path(os.path.expandvars(os.path.expanduser(value)))

    def remote_checkout(self, run_id: str) -> str:
        return f"{self.checkout_root.rstrip('/')}/{run_id}/source"


class MachineRegistry:
    def __init__(self, profiles: dict[str, MachineProfile]):
        self.profiles = profiles
        self._aliases: dict[str, str] = {}
        for name, profile in profiles.items():
            for alias in (name, *profile.aliases):
                if alias in self._aliases:
                    raise MachineError(f"duplicate machine alias: {alias}")
                self._aliases[alias] = name

    @classmethod
    def load(cls, path: str | Path) -> MachineRegistry:
        with Path(path).open("rb") as handle:
            raw = tomllib.load(handle)
        machines = raw.get("machines")
        if not isinstance(machines, dict) or not machines:
            raise MachineError("machines file requires [machines.*] profiles")
        profiles: dict[str, MachineProfile] = {}
        for name, value in machines.items():
            if not isinstance(value, dict):
                raise MachineError(f"[machines.{name}] must be a table")
            transport = str(value.get("transport", "")).lower()
            if transport not in {"local", "ssh", "runpod"}:
                raise MachineError(
                    f"[machines.{name}].transport must be local, ssh, or runpod"
                )
            target = str(value["target"]) if value.get("target") else None
            if transport == "ssh" and not target:
                raise MachineError(f"[machines.{name}].target is required")
            aliases = value.get("aliases", [])
            if not isinstance(aliases, list) or not all(
                isinstance(alias, str) for alias in aliases
            ):
                raise MachineError(f"[machines.{name}].aliases must be strings")
            profiles[name] = MachineProfile(
                name=name,
                transport=transport,
                target=target,
                workspace_root=str(value.get("workspace_root", "~/projects")),
                checkout_root=str(
                    value.get(
                        "checkout_root",
                        "~/.axiotic-experiments/checkouts",
                    )
                ),
                aliases=tuple(aliases),
            )
        return cls(profiles)

    def resolve(self, name: str) -> MachineProfile:
        canonical = self._aliases.get(name)
        if canonical is None:
            raise MachineError(f"unknown machine profile: {name}")
        return self.profiles[canonical]

    def to_public_dict(self) -> dict[str, Any]:
        return {
            name: {
                "transport": profile.transport,
                "target": profile.target,
                "workspace_root": profile.workspace_root,
                "checkout_root": profile.checkout_root,
                "aliases": list(profile.aliases),
            }
            for name, profile in sorted(self.profiles.items())
        }
