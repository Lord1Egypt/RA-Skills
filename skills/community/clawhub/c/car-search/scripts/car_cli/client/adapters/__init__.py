from car_cli.client.adapters.dongchedi import DongchediClient  # noqa: F401
from car_cli.client.adapters.guazi import GuaziClient  # noqa: F401
from car_cli.client.adapters.che168 import Che168Client  # noqa: F401
from car_cli.client.adapters.youxinpai import YouxinpaiClient  # noqa: F401

ADAPTER_REGISTRY: dict[str, type] = {
    "dongchedi": DongchediClient,
    "guazi": GuaziClient,
    "che168": Che168Client,
    "youxinpai": YouxinpaiClient,
}

# 在此处注释掉不想使用的平台
ENABLED_PLATFORMS: list[str] = [
    "dongchedi",
    # "guazi",
    "che168",
    "youxinpai",
]

ALL_PLATFORMS = [p for p in ENABLED_PLATFORMS if p in ADAPTER_REGISTRY]


def get_adapters(platform: str) -> list:
    """Return adapter instances for the given platform selector.

    Args:
        platform: "all" or comma-separated platform names (e.g. "dongchedi").

    Returns:
        List of adapter instances.
    """
    if platform == "all":
        names = ALL_PLATFORMS
    else:
        names = [p.strip() for p in platform.split(",")]

    adapters = []
    for name in names:
        cls = ADAPTER_REGISTRY.get(name)
        if cls is None:
            raise _usage_error(f"Unknown platform: {name}")
        adapters.append(cls())
    return adapters


def _usage_error(msg: str):
    import click
    return click.UsageError(msg)
