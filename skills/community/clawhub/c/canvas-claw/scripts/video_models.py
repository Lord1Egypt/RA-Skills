#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from canvas_claw.model_registry import list_models_for_capability


def main() -> None:
    models = list_models_for_capability("video-create") + list_models_for_capability("video-animate")
    seen: set[tuple[str, str, str]] = set()
    for model in models:
        key = (model.capability, model.catalog_key, model.model_id)
        if key in seen:
            continue
        seen.add(key)
        print(f"{model.capability}: {model.catalog_key} -> {model.provider}/{model.model_id} ({model.task_type})")


if __name__ == "__main__":
    main()
