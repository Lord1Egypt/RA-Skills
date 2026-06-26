from abc import ABC, abstractmethod

from car_cli.models.car import Car, CarDetail
from car_cli.models.filter import SearchFilter


class BaseClient(ABC):
    """Abstract base class for all platform adapters.

    Every platform adapter must implement these methods,
    returning unified data models regardless of the source platform.
    """

    platform_name: str = ""

    @abstractmethod
    async def search(self, filters: SearchFilter) -> list[Car]:
        """Search used cars with given filters, return unified Car list."""
        ...

    @abstractmethod
    async def detail(self, car_id: str) -> CarDetail:
        """Get car detail by platform-specific ID."""
        ...

    async def list_series(self, brand: str) -> list[dict[str, str]]:
        """List available series for a brand.

        Returns list of {"series_id": "...", "series_name": "..."}.
        Override in subclasses that support series lookup.
        """
        return []
