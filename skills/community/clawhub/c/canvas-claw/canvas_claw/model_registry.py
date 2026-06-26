from __future__ import annotations

from dataclasses import dataclass, field

from canvas_claw.errors import CanvasClawError


@dataclass(frozen=True)
class ModelSpec:
    capability: str
    catalog_key: str
    provider: str
    model_id: str
    task_type: str
    default_options: dict[str, object] = field(default_factory=dict)


MODEL_SPECS: tuple[ModelSpec, ...] = (
    ModelSpec(
        capability="image-create",
        catalog_key="image-plus",
        provider="vg",
        model_id="qwen-image-2",
        task_type="text_to_image",
        default_options={"aspect_ratio": "1:1", "resolution": "2K"},
    ),
    ModelSpec(
        capability="image-remix",
        catalog_key="image-multi",
        provider="vg",
        model_id="nano-banana-2",
        task_type="text_to_image",
        default_options={"aspect_ratio": "1:1", "resolution": "2K"},
    ),
    ModelSpec(
        capability="video-create",
        catalog_key="video-dream-standard",
        provider="vg",
        model_id="seedance-1-5-pro",
        task_type="text_to_video",
        default_options={"aspect_ratio": "16:9", "resolution": "720p", "duration": 8, "sound": True},
    ),
    ModelSpec(
        capability="video-animate",
        catalog_key="video-dream-standard",
        provider="vg",
        model_id="seedance-1-5-pro",
        task_type="image_to_video",
        default_options={"aspect_ratio": "16:9", "resolution": "720p", "duration": 8, "sound": True},
    ),
)


def resolve_model(*, capability: str, catalog_key: str | None) -> ModelSpec:
    matches = [spec for spec in MODEL_SPECS if spec.capability == capability]
    if not matches:
        raise CanvasClawError(f"Unsupported capability: {capability}")
    if catalog_key is None:
        return matches[0]
    for spec in matches:
        if spec.catalog_key == catalog_key:
            return spec
    raise CanvasClawError(f"Unsupported catalog_key for {capability}: {catalog_key}")


def list_models_for_capability(capability: str) -> list[ModelSpec]:
    return [spec for spec in MODEL_SPECS if spec.capability == capability]
