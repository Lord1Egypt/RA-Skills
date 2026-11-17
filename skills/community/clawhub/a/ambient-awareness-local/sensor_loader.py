from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from sensor_api import BaseSensor


class SensorLoadError(RuntimeError):
    pass


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def import_class_from_file(file_path: Path, class_name: str):
    module_name = f"ambient_sensor_{file_path.parent.name}_{file_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise SensorLoadError(f"Could not load module spec from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return getattr(module, class_name)
    except AttributeError as exc:
        raise SensorLoadError(f"Class {class_name} not found in {file_path}") from exc


def parse_entrypoint(manifest_path: Path, entrypoint: str) -> Tuple[Path, str]:
    if ":" not in entrypoint:
        raise SensorLoadError(f"Invalid entrypoint '{entrypoint}', expected 'file.py:ClassName'")
    file_part, class_name = entrypoint.split(":", 1)
    return manifest_path.parent / file_part, class_name


def load_sensors(root: Path, registry_path: Path) -> List[BaseSensor]:
    registry = read_json(registry_path)
    sensors: List[BaseSensor] = []

    for item in registry.get("enabled_sensors", []):
        manifest_path = root / item["manifest_path"]
        manifest = read_json(manifest_path)
        sensor_file, class_name = parse_entrypoint(manifest_path, manifest["entrypoint"])
        sensor_class = import_class_from_file(sensor_file, class_name)
        sensor = sensor_class()

        if not isinstance(sensor, BaseSensor):
            raise SensorLoadError(f"{class_name} must inherit BaseSensor")

        sensor.id = manifest.get("id", sensor.id)
        sensor.capabilities = manifest.get("capabilities", sensor.capabilities)
        sensor.permission_class = int(manifest.get("permission_class", sensor.permission_class))
        sensor.setup(item.get("config", {}))
        sensors.append(sensor)

    return sensors
