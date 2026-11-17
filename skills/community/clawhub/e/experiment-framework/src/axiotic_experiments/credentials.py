from __future__ import annotations

import os
import re
from collections.abc import Mapping

from .machines import MachineProfile


class CredentialError(RuntimeError):
    pass


BASE_CREDENTIALS = ("WANDB_API_KEY", "HF_TOKEN", "GITHUB_TOKEN")
RUNPOD_CREDENTIALS = ("RUNPOD_API_KEY",)
_SENSITIVE_NAME = re.compile(r"(TOKEN|PASSWORD|SECRET|API_KEY|PRIVATE_KEY)$")


def required_credentials(profile: MachineProfile) -> tuple[str, ...]:
    if profile.transport == "runpod":
        return BASE_CREDENTIALS + RUNPOD_CREDENTIALS
    return BASE_CREDENTIALS


def resolve_credentials(
    profile: MachineProfile,
    environ: Mapping[str, str] | None = None,
) -> dict[str, str]:
    source = environ if environ is not None else os.environ
    names = required_credentials(profile)
    missing = [name for name in names if not source.get(name)]
    if missing:
        raise CredentialError(
            "missing runtime credential: " + ", ".join(sorted(missing))
        )
    return {name: source[name] for name in names}


def redact(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: (
                "[redacted]"
                if _SENSITIVE_NAME.search(str(key).upper())
                else redact(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item) for item in value)
    return value
