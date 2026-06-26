"""Unified configuration loader for MLLM providers."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ProviderConfig:
    api_key: str
    base_url: str
    model: str


@dataclass
class VideoConfig:
    max_frames: int = 30
    frame_interval_sec: int = 2
    max_resolution: tuple[int, int] = (1280, 720)


@dataclass
class ImageConfig:
    max_resolution: tuple[int, int] = (1280, 720)
    supported_formats: list[str] = field(
        default_factory=lambda: ["png", "jpg", "jpeg", "webp", "bmp"]
    )


@dataclass
class SkillConfig:
    default_os: list[str] = field(default_factory=lambda: ["darwin", "linux", "win32"])
    default_emoji: str = "🔧"


@dataclass
class Config:
    provider: str
    provider_config: ProviderConfig
    video: VideoConfig
    image: ImageConfig
    skill: SkillConfig


def load_config(config_path: str | None = None) -> Config:
    """Load configuration from YAML file with environment variable overrides."""
    if config_path is None:
        config_path = str(Path(__file__).parent.parent / "config.yaml")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    # Determine active provider
    provider = os.environ.get("MLLM_PROVIDER", raw.get("provider", "openai"))

    # Get provider-specific config
    providers = raw.get("providers", {})
    pconf = providers.get(provider, {})

    # Environment variables override config file
    api_key = os.environ.get("MLLM_API_KEY", pconf.get("api_key", ""))
    base_url = os.environ.get("MLLM_BASE_URL", pconf.get("base_url", ""))
    model = os.environ.get("MLLM_MODEL", pconf.get("model", ""))

    provider_config = ProviderConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )

    # Video config
    vconf = raw.get("video", {})
    video = VideoConfig(
        max_frames=vconf.get("max_frames", 30),
        frame_interval_sec=vconf.get("frame_interval_sec", 2),
        max_resolution=tuple(vconf.get("max_resolution", [1280, 720])),
    )

    # Image config
    iconf = raw.get("image", {})
    image = ImageConfig(
        max_resolution=tuple(iconf.get("max_resolution", [1280, 720])),
        supported_formats=iconf.get(
            "supported_formats", ["png", "jpg", "jpeg", "webp", "bmp"]
        ),
    )

    # Skill config
    sconf = raw.get("skill", {})
    skill = SkillConfig(
        default_os=sconf.get("default_os", ["darwin", "linux", "win32"]),
        default_emoji=sconf.get("default_emoji", "🔧"),
    )

    return Config(
        provider=provider,
        provider_config=provider_config,
        video=video,
        image=image,
        skill=skill,
    )
