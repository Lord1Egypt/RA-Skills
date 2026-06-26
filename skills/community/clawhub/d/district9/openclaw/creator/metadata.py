"""Token metadata builder with DISTRICT9 tag injection."""

from ..launcher.constants import D9_TAG_PREFIX, D9_TAG_SUFFIX


class MetadataBuilder:
    """Build token metadata with DISTRICT9 identification tags."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def build(self, name: str, symbol: str, narrative: str, logo_url: str = "") -> dict:
        """Build complete metadata dict for IPFS upload."""
        d9_tag = f"{D9_TAG_PREFIX}{self.agent_name}{D9_TAG_SUFFIX}"
        description = f"{narrative} {d9_tag}"

        return {
            "name": name,
            "symbol": symbol.replace("$", ""),
            "description": description,
            "image": logo_url,
            "website": "",  # Set by launcher after CREATE2 address is known
            "twitter": "",
            "telegram": "",
        }
