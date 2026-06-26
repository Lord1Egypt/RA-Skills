"""Spacebase1 client abstraction — provider boundary for Consensus Commons.

The MVP supports two modes:

* **MockSpacebaseClient** — deterministic in-memory client for offline demos
  and testing. No network required; all operations are recorded so the demo
  can be replayed identically.
* **HttpSpacebaseClient** — real client that speaks the Spacebase1 ITP wire
  protocol over HTTP. Requires valid station credentials obtained via Welcome
  Mat v1 / DPoP enrollment.

Both share the same ``SpacebaseClient`` abstract interface so the adapter
layer is completely provider-agnostic.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any

import httpx

from cme.spacebase.models import Intent, LockState, Post, PostTree, ScanResult

logger = logging.getLogger(__name__)


class SpacebaseClient(ABC):
    """Abstract interface for Spacebase1 operations.

    Every method mirrors a core ITP verb (POST / SCAN / ENTER) plus
    Consensus Commons extensions for posting child intents.
    """

    @abstractmethod
    async def scan(self, space_id: str, since: float | None = None) -> ScanResult:
        """Scan a space for intents posted since *since* (epoch seconds)."""

    @abstractmethod
    async def enter(self, intent_id: str) -> Intent | None:
        """Enter an intent's interior space and return its metadata."""

    @abstractmethod
    async def post(
        self,
        content: str,
        parent_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Intent:
        """Post a new intent (or child intent if *parent_id* is set)."""

    @abstractmethod
    async def post_child(
        self,
        parent_id: str,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> Post:
        """Post a child response inside a parent intent's space."""

    @abstractmethod
    async def lock_intent(self, intent_id: str, state: LockState) -> bool:
        """Request a lock-state change on an intent."""

    @abstractmethod
    async def get_post_tree(self, intent_id: str) -> PostTree | None:
        """Return the full nested post tree for an intent."""


# ---------------------------------------------------------------------------
# Mock client
# ---------------------------------------------------------------------------


class MockSpacebaseClient(SpacebaseClient):
    """In-memory mock Spacebase1 client.

    All operations are deterministic and recorded in an internal log
    so tests and demos can inspect what happened. The mock never hits
    the network.
    """

    def __init__(self, commons_space: str = "mock-commons") -> None:
        self.commons_space = commons_space
        self._intents: dict[str, Intent] = {}
        self._posts: dict[str, list[Post]] = {}
        self._lock_states: dict[str, LockState] = {}
        self._log: list[dict[str, Any]] = []
        self._seq = 0

    # -- helpers for seeding -----------------------------------------------

    def seed_intent(self, intent: Intent) -> None:
        """Pre-populate an intent (useful for demo scenarios)."""
        self._intents[intent.intent_id] = intent
        self._posts.setdefault(intent.intent_id, [])
        self._seq += 1
        self._log.append({"op": "seed", "intent_id": intent.intent_id})

    def get_log(self) -> list[dict[str, Any]]:
        """Return the operation log (for assertions in tests)."""
        return list(self._log)

    # -- SpacebaseClient interface ----------------------------------------

    async def scan(self, space_id: str, since: float | None = None) -> ScanResult:
        self._seq += 1
        candidates = [
            i
            for i in self._intents.values()
            if i.parent_id == space_id or i.intent_id == space_id
        ]
        if since is not None:
            candidates = [i for i in candidates if i.timestamp >= since]
        result = ScanResult(space_id=space_id, intents=candidates, latest_seq=self._seq)
        self._log.append({"op": "scan", "space_id": space_id, "count": len(candidates)})
        logger.info("Mock scan(%s) -> %d intents", space_id, len(candidates))
        return result

    async def enter(self, intent_id: str) -> Intent | None:
        self._seq += 1
        intent = self._intents.get(intent_id)
        self._log.append({"op": "enter", "intent_id": intent_id, "found": intent is not None})
        return intent

    async def post(
        self,
        content: str,
        parent_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Intent:
        self._seq += 1
        intent = Intent(
            intent_id=uuid.uuid4().hex[:12],
            parent_id=parent_id,
            content=content,
            payload=payload or {},
            sender="consensus-commons",
            timestamp=time.time(),
        )
        self._intents[intent.intent_id] = intent
        self._posts.setdefault(intent.intent_id, [])
        self._log.append({"op": "post", "intent_id": intent.intent_id, "parent_id": parent_id})
        logger.info("Mock post -> intent_id=%s", intent.intent_id)
        return intent

    async def post_child(
        self,
        parent_id: str,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> Post:
        self._seq += 1
        post = Post(
            post_id=uuid.uuid4().hex[:12],
            parent_id=parent_id,
            intent_id=parent_id,
            title=title,
            body=body,
            sender="consensus-commons",
            timestamp=time.time(),
            **(metadata or {}),
        )
        self._posts.setdefault(parent_id, []).append(post)
        self._log.append({"op": "post_child", "post_id": post.post_id, "parent_id": parent_id})
        logger.info("Mock post_child -> post_id=%s under %s", post.post_id, parent_id)
        return post

    async def lock_intent(self, intent_id: str, state: LockState) -> bool:
        current = self._lock_states.get(intent_id, LockState.PROVISIONAL)
        allowed = self._allowed_transition(current, state)
        if allowed:
            self._lock_states[intent_id] = state
        self._log.append(
            {
                "op": "lock",
                "intent_id": intent_id,
                "from": current.value,
                "to": state.value if allowed else current.value,
                "allowed": allowed,
            }
        )
        return allowed

    async def get_post_tree(self, intent_id: str) -> PostTree | None:
        posts = self._posts.get(intent_id, [])
        if not posts:
            return None
        root = Post(post_id=intent_id, intent_id=intent_id, title="root", body="", sender="system")
        return self._build_tree(root, posts)

    @staticmethod
    def _build_tree(root: Post, all_posts: list[Post]) -> PostTree:
        children_map: dict[str, list[Post]] = {}
        for p in all_posts:
            children_map.setdefault(p.parent_id or p.intent_id, []).append(p)
        direct = children_map.get(root.post_id, [])

        def _sub(post: Post) -> PostTree:
            kids = children_map.get(post.post_id, [])
            return PostTree(post=post, children=[_sub(k) for k in kids])

        return PostTree(post=root, children=[_sub(c) for c in direct])

    @staticmethod
    def _allowed_transition(current: LockState, target: LockState) -> bool:
        transitions: dict[LockState, set[LockState]] = {
            LockState.PROVISIONAL: {LockState.CHALLENGED, LockState.VALIDATED, LockState.LOCKED, LockState.FAILED},
            LockState.CHALLENGED: {LockState.VALIDATED, LockState.LOCKED, LockState.FAILED},
            LockState.VALIDATED: {LockState.LOCKED, LockState.CHALLENGED},
            LockState.LOCKED: set(),
            LockState.FAILED: set(),
        }
        return target in transitions.get(current, set())


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------

ITP_ENDPOINT = "https://spacebase1.differ.ac/spaces/commons/itp"
SCAN_ENDPOINT = "https://spacebase1.differ.ac/spaces/commons/scan"


class HttpSpacebaseClient(SpacebaseClient):
    """Real Spacebase1 client that speaks the ITP wire protocol over HTTP.

    Requires a ``station_token`` obtained via Welcome Mat v1 / DPoP
    enrollment. All writes are signed; reads use the station's cursor.

    Usage::

        client = HttpSpacebaseClient(
            station_token="eyJ...",
            agent_name="council-validator",
            commons_space="commons",
        )
        await client.connect()
        result = await client.scan("commons")
    """

    def __init__(
        self,
        station_token: str,
        agent_name: str = "consensus-commons",
        commons_space: str = "commons",
        base_url: str | None = None,
    ) -> None:
        self.station_token = station_token
        self.agent_name = agent_name
        self.commons_space = commons_space
        self.base_url = base_url or ITP_ENDPOINT
        self._connected = False
        self._http: httpx.AsyncClient | None = None

    async def connect(self) -> None:
        """Establish connection and verify station binding."""
        self._http = httpx.AsyncClient(
            base_url="https://spacebase1.differ.ac",
            headers={"Authorization": f"Bearer {self.station_token}"},
            timeout=30.0,
        )
        # verify binding via continue endpoint
        try:
            resp = await self._http.post(
                "/spaces/commons/continue",
                json={"station_token": self.station_token},
            )
            resp.raise_for_status()
            self._connected = True
            logger.info("Connected to Spacebase1 as %s", self.agent_name)
        except httpx.HTTPError as exc:
            logger.error("Connection failed: %s", exc)
            raise

    def _ensure_connected(self) -> httpx.AsyncClient:
        if not self._connected or self._http is None:
            raise RuntimeError("Not connected — call await client.connect() first")
        return self._http

    async def _send_itp(self, verb: str, body: dict[str, Any]) -> dict[str, Any]:
        """Send an ITP act and return the parsed response."""
        http = self._ensure_connected()
        envelope = {
            "verb": verb,
            "sender": self.agent_name,
            "timestamp": time.time(),
            "body": body,
        }
        resp = await http.post(ITP_ENDPOINT, json=envelope)
        resp.raise_for_status()
        return resp.json()

    async def scan(self, space_id: str, since: float | None = None) -> ScanResult:
        http = self._ensure_connected()
        body: dict[str, Any] = {"space": space_id}
        if since is not None:
            body["since"] = since
        resp = await http.post(SCAN_ENDPOINT, json=body)
        resp.raise_for_status()
        data = resp.json()
        intents = [Intent(**i) for i in data.get("intents", [])]
        return ScanResult(
            space_id=space_id,
            intents=intents,
            latest_seq=data.get("latest_seq"),
        )

    async def enter(self, intent_id: str) -> Intent | None:
        try:
            result = await self._send_itp("SCAN", {"space": intent_id})
            entries = result.get("intents", [])
            return Intent(**entries[0]) if entries else None
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    async def post(
        self,
        content: str,
        parent_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Intent:
        result = await self._send_itp(
            "INTENT",
            {
                "parent": parent_id or self.commons_space,
                "body": content,
                "payload": payload or {},
            },
        )
        return Intent(
            intent_id=result.get("intent_id", uuid.uuid4().hex[:12]),
            parent_id=parent_id,
            content=content,
            payload=payload or {},
            sender=self.agent_name,
            timestamp=time.time(),
        )

    async def post_child(
        self,
        parent_id: str,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> Post:
        intent = await self.post(
            content=f"{title}\n\n{body}",
            parent_id=parent_id,
            payload=metadata or {},
        )
        return Post(
            post_id=intent.intent_id,
            parent_id=parent_id,
            intent_id=parent_id,
            title=title,
            body=body,
            sender=self.agent_name,
            timestamp=time.time(),
            **(metadata or {}),
        )

    async def lock_intent(self, intent_id: str, state: LockState) -> bool:
        try:
            await self._send_itp(
                "INTENT",
                {
                    "parent": intent_id,
                    "body": f"[LOCK] {state.value}",
                    "payload": {"lock_state": state.value},
                },
            )
            return True
        except httpx.HTTPError:
            return False

    async def get_post_tree(self, intent_id: str) -> PostTree | None:
        intent = await self.enter(intent_id)
        if intent is None:
            return None
        scan_result = await self.scan(intent_id)
        root_post = Post(
            post_id=intent_id,
            intent_id=intent_id,
            title=intent.content[:80],
            body=intent.content,
            sender=intent.sender,
        )
        children = []
        for child_intent in scan_result.intents:
            child_post = Post(
                post_id=child_intent.intent_id,
                parent_id=intent_id,
                intent_id=intent_id,
                title=child_intent.content[:80],
                body=child_intent.content,
                sender=child_intent.sender,
                **child_intent.payload,
            )
            children.append(PostTree(post=child_post))
        return PostTree(post=root_post, children=children)

    async def close(self) -> None:
        if self._http:
            await self._http.aclose()
            self._connected = False
