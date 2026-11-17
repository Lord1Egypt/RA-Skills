"""Deterministic Phase 15.4 provider discovery and configuration management."""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import stat
from types import MappingProxyType
from typing import Any, Callable, Mapping

from .base import OCRProvider
from .errors import OCRError
from .resolution import resolve_provider
from .validation import validate_provider

_KEYS = frozenset({"provider", "allow_fallback"})
_ORIGINS = ("explicit", "project", "user", "default")


def _error(message: str, code: str = "OCR_PROVIDER_CONTRACT_INVALID") -> OCRError:
    return OCRError(message, code)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _error("duplicate OCR configuration key")
        result[key] = value
    return result


@dataclass(frozen=True)
class OCRProviderConfiguration:
    provider: str
    allow_fallback: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.provider, str) or not self.provider or self.provider.strip() != self.provider:
            raise _error("provider must be a non-empty canonical identifier")
        if isinstance(self.allow_fallback, bool) is False:
            raise _error("allow_fallback must be boolean")

    def to_dict(self) -> dict[str, Any]:
        return {"allow_fallback": self.allow_fallback, "provider": self.provider}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"

    @classmethod
    def from_bytes(cls, raw: bytes) -> "OCRProviderConfiguration":
        try:
            value = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=_pairs)
        except OCRError:
            raise
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise _error("OCR configuration is invalid JSON") from exc
        if not isinstance(value, dict) or set(value) != _KEYS:
            raise _error("OCR configuration must contain only provider and allow_fallback")
        return cls(value["provider"], value["allow_fallback"])


@dataclass(frozen=True)
class EffectiveOCRConfiguration:
    configured: Mapping[str, str | None]
    selected_provider: str
    selection_origin: str
    allow_fallback: bool
    fallback_provider: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "configured", MappingProxyType(dict(self.configured)))
        if self.selection_origin not in _ORIGINS:
            raise _error("invalid selection origin")

    def to_dict(self) -> dict[str, Any]:
        return {
            "allow_fallback": self.allow_fallback,
            "configured": dict(self.configured),
            "fallback_provider": self.fallback_provider,
            "selected_provider": self.selected_provider,
            "selection_origin": self.selection_origin,
        }


class OCRConfigurationStore:
    """Own the two bounded configuration files without exposing their paths."""

    def __init__(self, project_root: Path | str, user_config_root: Path | str):
        self.project_root = Path(project_root).resolve()
        self.user_config_root = Path(user_config_root).resolve()
        self._paths = {
            "project": self.project_root / ".agy" / "ocr-provider.json",
            "user": self.user_config_root / "agy-ppt" / "ocr-provider.json",
        }

    def _path(self, scope: str) -> Path:
        if scope not in self._paths:
            raise _error("configuration scope must be project or user")
        return self._paths[scope]

    def _root(self, scope: str) -> Path:
        return self.project_root if scope == "project" else self.user_config_root

    def _validate_path(self, scope: str, *, writing: bool) -> Path:
        path = self._path(scope)
        root = self._root(scope)
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise _error("OCR configuration path escapes its scope") from exc
        current = root
        for part in path.relative_to(root).parts[:-1]:
            current = current / part
            if current.exists() and current.is_symlink():
                raise _error("symlink configuration directories are forbidden")
        if path.is_symlink():
            raise _error("symlink configuration files are forbidden")
        if writing and root.exists() and root.is_symlink():
            raise _error("symlink configuration roots are forbidden")
        return path

    def read(self, scope: str) -> OCRProviderConfiguration | None:
        path = self._validate_path(scope, writing=False)
        try:
            raw = path.read_bytes()
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise _error("OCR configuration cannot be read") from exc
        if len(raw) > 16_384:
            raise _error("OCR configuration exceeds size limit")
        return OCRProviderConfiguration.from_bytes(raw)

    def write(self, scope: str, config: OCRProviderConfiguration) -> None:
        path = self._validate_path(scope, writing=True)
        parent = path.parent
        parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if parent.is_symlink():
            raise _error("symlink configuration directories are forbidden")
        payload = config.to_json().encode("utf-8")
        temp = parent / ("." + path.name + ".tmp")
        if temp.exists() or temp.is_symlink():
            raise _error("stale OCR configuration temporary file")
        fd: int | None = None
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(temp, flags, stat.S_IRUSR | stat.S_IWUSR)
            with os.fdopen(fd, "wb", closefd=True) as handle:
                fd = None
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp, path)
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        except OCRError:
            raise
        except OSError as exc:
            raise _error("OCR configuration cannot be written") from exc
        finally:
            if fd is not None:
                os.close(fd)
            try:
                temp.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass

    def unset(self, scope: str) -> bool:
        path = self._validate_path(scope, writing=True)
        try:
            path.unlink()
        except FileNotFoundError:
            return False
        except OSError as exc:
            raise _error("OCR configuration cannot be removed") from exc
        try:
            path.parent.rmdir()
        except OSError:
            pass
        return True


ValidationProbe = Callable[[OCRProvider, tuple[str, ...]], Mapping[str, Any] | None]


class OCRProviderManager:
    """Management-only facade over the frozen registry and resolver."""

    def __init__(self, providers: Mapping[str, OCRProvider], store: OCRConfigurationStore, *,
                 default: str = "tesseract", validation_probes: Mapping[str, ValidationProbe] | None = None):
        self.providers = MappingProxyType(dict(providers))
        self.store = store
        self.default = default
        self.validation_probes = MappingProxyType(dict(validation_probes or {}))
        for provider_id, provider in self.providers.items():
            if provider_id != getattr(provider, "provider_id", None):
                raise _error("registry key must match provider_id")

    def list_providers(self) -> tuple[dict[str, Any], ...]:
        rows = []
        for provider_id in sorted(self.providers):
            provider = self.providers[provider_id]
            code = None
            try:
                validate_provider(provider)
                available = True
            except OCRError as exc:
                available = False
                code = exc.error_code
            capabilities = getattr(provider, "capabilities", None)
            cap_dict = dict(vars(capabilities)) if capabilities is not None and hasattr(capabilities, "__dataclass_fields__") else None
            rows.append({
                "availability_error": code,
                "available": available,
                "capabilities": cap_dict,
                "default": provider_id == self.default,
                "provider_id": provider_id,
                "provider_version": getattr(provider, "provider_version", None),
            })
        return tuple(rows)

    def effective(self, *, explicit: str | None = None) -> EffectiveOCRConfiguration:
        project = self.store.read("project")
        user = self.store.read("user")
        _, resolution = resolve_provider(
            self.providers, explicit=explicit,
            project=project.provider if project else None,
            user=user.provider if user else None, default=self.default,
        )
        fallback_source = project or user
        allow_fallback = fallback_source.allow_fallback if fallback_source else False
        return EffectiveOCRConfiguration(
            configured={"explicit": explicit, "project": project.provider if project else None,
                        "user": user.provider if user else None, "default": self.default},
            selected_provider=resolution.actual_provider,
            selection_origin=resolution.selection_origin or "default",
            allow_fallback=allow_fallback,
            fallback_provider=self.default if allow_fallback and resolution.actual_provider != self.default else None,
        )

    def validate(self, *, provider_id: str | None = None, explicit: str | None = None,
                 languages: tuple[str, ...] = ()) -> dict[str, Any]:
        if provider_id is None:
            effective = self.effective(explicit=explicit)
            provider_id = effective.selected_provider
        provider = self.providers.get(provider_id)
        if provider is None:
            raise OCRError(f"provider not found: {provider_id}", "OCR_PROVIDER_NOT_FOUND")
        validate_provider(provider)
        details: Mapping[str, Any] = {}
        probe = self.validation_probes.get(provider_id)
        if probe is not None:
            details = probe(provider, languages) or {}
        return {"details": dict(details), "provider_id": provider_id, "valid": True}

    def set(self, scope: str, provider_id: str, *, allow_fallback: bool | None = None) -> OCRProviderConfiguration:
        provider = self.providers.get(provider_id)
        if provider is None:
            raise OCRError(f"provider not found: {provider_id}", "OCR_PROVIDER_NOT_FOUND")
        validate_provider(provider)
        if allow_fallback is not None and not isinstance(allow_fallback, bool):
            raise _error("allow_fallback must be boolean")
        previous = self.store.read(scope)
        fallback = previous.allow_fallback if previous is not None and allow_fallback is None else bool(allow_fallback)
        config = OCRProviderConfiguration(provider_id, fallback)
        self.store.write(scope, config)
        return config

    def unset(self, scope: str) -> bool:
        return self.store.unset(scope)


def tesseract_validation_probe(provider: OCRProvider, languages: tuple[str, ...]) -> Mapping[str, Any]:
    """Use existing Tesseract probes without invoking recognition."""
    version = provider.detect_version()  # type: ignore[attr-defined]
    details: dict[str, Any] = {"engine_version": version}
    if languages:
        models = provider.discover_traineddata(languages)  # type: ignore[attr-defined]
        details["models"] = [
            {"model_digest": model.model_digest, "model_id": model.model_id, "model_source": model.model_source}
            for model in models
        ]
    return details
