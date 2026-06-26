"""Bird Buddy camera entity — snapshot and livestream support.

Installation:
  Copy this file to:
    {{HA_CONFIG_DIR}}/custom_components/birdbuddy/camera.py

  Then add Platform.CAMERA to the PLATFORMS list in __init__.py:
    PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.CAMERA]

  Requires ha-birdbuddy v0.0.21+ and pybirdbuddy 0.0.19+.

How it works:
  1. When HA requests a camera frame, the entity checks the feeder state.
  2. If NOT in DEEP_SLEEP, it starts a Bird Buddy watching session via GraphQL:
       watchingWarmup → watchingStartV2(feederId) → poll watchingActiveKeep
       until STREAMING/READY_TO_STREAM (timeout 45s) → watchingActiveTakeSnapshot
       → download image bytes → watchingActiveStop
  3. If DEEP_SLEEP (or snapshot fails), returns the last cached image.
  4. Listens for `birdbuddy_new_postcard_sighting` HA events to keep the cache
     fresh with the latest postcard thumbnail.

No credentials are stored in this file. Authentication re-uses the existing
coordinator client that was configured via the HA config entry.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER
from .coordinator import BirdBuddyDataUpdateCoordinator
from .device import BirdBuddyDevice
from .entity import BirdBuddyMixin

# GraphQL mutations for watching/snapshot
_MUTATION_WARMUP = """
mutation { watchingWarmup { ... on Success { success } } }
"""

_MUTATION_START_V2 = """
mutation WatchingStart($input: StartWatchingInput!) {
  watchingStartV2(startWatchingInput: $input) {
    ... on WatchingActiveResult {
      watching { id state streamUrl }
    }
    ... on WatchingStartInProgressResult {
      watching { id state }
    }
    ... on WatchingFailedResult {
      failedReason
    }
  }
}
"""

_MUTATION_KEEP = """
mutation {
  watchingActiveKeep {
    id
    state
    streamUrl
  }
}
"""

_MUTATION_SNAPSHOT = """
mutation WatchingSnapshot($ts: Float!) {
  watchingActiveTakeSnapshot(timestamp: $ts) {
    ... on WatchingActiveTakeSnapshotSucceededResult {
      imageUrl
    }
    ... on WatchingActiveTakeSnapshotFailedResult {
      errorCode
      errorMessage
    }
  }
}
"""

_MUTATION_STOP = """
mutation { watchingActiveStop { id state } }
"""

# Feeder states that allow livestream
_STREAMABLE_STATES = {"TAKING_POSTCARDS", "READY_TO_STREAM", "STREAMING", "ONLINE"}
# Max seconds to wait for feeder to transition from REQUESTED → STREAMING
_STREAM_TIMEOUT = 45
# How long a snapshot is valid before refreshing (seconds)
_SNAPSHOT_CACHE_TTL = 30


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bird Buddy camera entities from a config entry."""
    coordinator: BirdBuddyDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        BirdBuddyCamera(feeder, coordinator)
        for feeder in coordinator.feeders.values()
    ]
    async_add_entities(entities)


class BirdBuddyCamera(BirdBuddyMixin, Camera):
    """Camera entity that delivers snapshot images from a Bird Buddy feeder.

    When the feeder is awake (state != DEEP_SLEEP), it starts a watching session,
    takes a snapshot, and returns the image bytes.  When the feeder is asleep it
    returns the last cached image (if any) so HA always has *something* to show.
    """

    _attr_name = "Bird Buddy Camera"
    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature(0)

    # Cached image bytes and the URL they came from
    _cached_image: bytes | None = None
    _cached_url: str | None = None
    _watching_session_id: str | None = None
    _snapshot_lock: asyncio.Lock

    def __init__(
        self,
        feeder: BirdBuddyDevice,
        coordinator: BirdBuddyDataUpdateCoordinator,
    ) -> None:
        """Initialise."""
        BirdBuddyMixin.__init__(self, feeder, coordinator)
        Camera.__init__(self)
        self._snapshot_lock = asyncio.Lock()
        self._attr_unique_id = f"{feeder.id}_camera"
        self._attr_entity_registry_enabled_default = True

    @property
    def is_recording(self) -> bool:
        """Return True while a watching session is active."""
        return self._watching_session_id is not None

    @property
    def is_on(self) -> bool:
        """Return True if the feeder is not in deep sleep."""
        state = (self.feeder.get("state") or "").upper()
        return state != "DEEP_SLEEP"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose feeder state and last snapshot URL for automations."""
        return {
            "feeder_state": self.feeder.get("state"),
            "last_snapshot_url": self._cached_url,
            "watching_session_id": self._watching_session_id,
        }

    # ------------------------------------------------------------------
    # Core snapshot method called by HA when someone requests a frame
    # ------------------------------------------------------------------

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the feeder.

        Tries to start a watching session and take a live snapshot.  Falls back
        to the most recently cached image if the feeder is sleeping or if the
        snapshot request fails.
        """
        if self._snapshot_lock.locked():
            # Another call is already obtaining a frame — return the cache
            return self._cached_image

        async with self._snapshot_lock:
            feeder_state = (self.feeder.get("state") or "").upper()
            if feeder_state == "DEEP_SLEEP":
                LOGGER.debug(
                    "Bird Buddy feeder %s is in DEEP_SLEEP; returning cached image",
                    self.feeder.name,
                )
                return self._cached_image

            # Try to get a live snapshot
            try:
                image = await self._fetch_live_snapshot()
                if image:
                    self._cached_image = image
                    return image
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.warning(
                    "Bird Buddy snapshot failed for %s: %s", self.feeder.name, err
                )

        return self._cached_image

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _graphql(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL mutation using the underlying BirdBuddy client."""
        client = self.coordinator.client
        await client._check_auth()
        from python_graphql_client import GraphqlClient as _GQL
        # Re-use the existing graphql client that already knows the endpoint
        response = await client.graphql.execute_async(
            query=query,
            variables=variables or {},
            headers=client._headers(),
        )
        errors = (response or {}).get("errors", [])
        if errors:
            LOGGER.warning("GraphQL errors: %s", errors)
        return (response or {}).get("data", {})

    async def _fetch_live_snapshot(self) -> bytes | None:
        """Start a watching session (if needed) and take a snapshot."""
        # Step 1: warmup
        await self._graphql(_MUTATION_WARMUP)

        # Step 2: start watching
        start_data = await self._graphql(
            _MUTATION_START_V2,
            {"input": {"feederId": self.feeder.id}},
        )
        result = (start_data.get("watchingStartV2") or {})
        watching = result.get("watching") or {}
        failed_reason = result.get("failedReason")
        if failed_reason:
            LOGGER.warning(
                "Bird Buddy watching start failed for %s: %s",
                self.feeder.name,
                failed_reason,
            )
            return None

        self._watching_session_id = watching.get("id")
        state = watching.get("state", "UNKNOWN")
        LOGGER.debug("Watching session started: id=%s state=%s", self._watching_session_id, state)

        # Step 3: poll until STREAMING or timeout
        deadline = asyncio.get_event_loop().time() + _STREAM_TIMEOUT
        while state not in ("STREAMING", "READY_TO_STREAM") and asyncio.get_event_loop().time() < deadline:
            await asyncio.sleep(3)
            keep_data = await self._graphql(_MUTATION_KEEP)
            watching = keep_data.get("watchingActiveKeep") or {}
            state = watching.get("state", state)
            LOGGER.debug("Watching state poll: %s", state)
            if state in ("FAILED", "ENDED", "EXPIRED"):
                LOGGER.warning("Watching session ended prematurely: %s", state)
                self._watching_session_id = None
                return None

        if state not in ("STREAMING", "READY_TO_STREAM"):
            LOGGER.debug("Feeder %s did not reach streaming state in time (state=%s)", self.feeder.name, state)
            await self._stop_watching()
            return None

        # Step 4: take snapshot
        import time
        ts = time.time()
        snap_data = await self._graphql(_MUTATION_SNAPSHOT, {"ts": ts})
        snap_result = snap_data.get("watchingActiveTakeSnapshot") or {}
        image_url = snap_result.get("imageUrl")
        if not image_url:
            error_msg = snap_result.get("errorMessage", "unknown error")
            LOGGER.warning("Snapshot failed for %s: code=%s msg=%s",
                           self.feeder.name, snap_result.get("errorCode"), error_msg)
            await self._stop_watching()
            return None

        self._cached_url = image_url
        LOGGER.debug("Got snapshot URL: %s", image_url[:80])

        # Step 5: fetch the image bytes
        image_bytes = await self._download_image(image_url)

        # Step 6: stop the watching session to conserve feeder battery
        await self._stop_watching()

        return image_bytes

    async def _stop_watching(self) -> None:
        """Stop an active watching session."""
        if self._watching_session_id:
            try:
                await self._graphql(_MUTATION_STOP)
                LOGGER.debug("Watching session stopped")
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.debug("Error stopping watching session: %s", err)
            self._watching_session_id = None

    async def _download_image(self, url: str) -> bytes | None:
        """Download image bytes from a URL."""
        import aiohttp
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.read()
                LOGGER.warning("Image download failed: HTTP %s for %s", resp.status, url[:80])
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.warning("Image download error: %s", err)
        return None

    async def async_will_remove_from_hass(self) -> None:
        """Stop watching session on entity removal."""
        await self._stop_watching()

    # ------------------------------------------------------------------
    # Postcard event listener — cache thumbnails from new postcards
    # ------------------------------------------------------------------

    async def async_added_to_hass(self) -> None:
        """Register event listener for new postcard events."""
        await super().async_added_to_hass()
        from .const import EVENT_NEW_POSTCARD_SIGHTING
        self.async_on_remove(
            self.hass.bus.async_listen(
                EVENT_NEW_POSTCARD_SIGHTING,
                self._handle_new_postcard,
            )
        )

    async def _handle_new_postcard(self, event) -> None:
        """Cache the thumbnail from a new postcard sighting event."""
        try:
            medias = event.data.get("sighting", {}).get("medias", [])
            if medias:
                thumbnail_url = medias[0].get("thumbnailUrl")
                if thumbnail_url and thumbnail_url != self._cached_url:
                    LOGGER.debug(
                        "Caching postcard thumbnail for %s: %s",
                        self.feeder.name,
                        thumbnail_url[:60],
                    )
                    image_bytes = await self._download_image(thumbnail_url)
                    if image_bytes:
                        self._cached_image = image_bytes
                        self._cached_url = thumbnail_url
                        self.async_write_ha_state()
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.debug("Error caching postcard thumbnail: %s", err)
