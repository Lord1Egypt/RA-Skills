"""Spacebase1 adapter — maps Spacebase concepts onto the cognitive mesh orchestrator.

The adapter is a thin layer that translates between the flat ITP protocol
(post / scan / enter) and Consensus Commons' multi-agent decision-room
model. The core mapping is:

* Spacebase **root intent** → decision *problem* statement
* Each **TurnResult** from the orchestrator → a *child intent* inside the room
* Each **expansion / compression trace** → the *body* of the child post
* The final **Workflow** → *summary* child
* **CHP / adversary output** → *validation* child

The adapter does NOT rewrite the mesh engine. It consumes TurnResult objects
produced by the existing EnterpriseOrchestrator and renders them as nested
Spacebase1 posts with full Consensus Commons metadata.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from cme.spacebase.client import SpacebaseClient
from cme.spacebase.models import (
    Intent,
    LockState,
    Post,
    PostTree,
    ScanResult,
)
from cme.spacebase.routing import IntentRouter, RouteDecision
from cme.spacebase.council import CouncilRunner, CouncilReport

logger = logging.getLogger(__name__)


class SpacebaseAdapter:
    """Bidirectional adapter between Spacebase1 intents and CME orchestrator.

    Responsibilities:

    1. **scan_intents()** — pull candidate decision problems from a Spacebase
       space and classify them via the IntentRouter.
    2. **enter_space()** — enter a specific intent's interior and retrieve
       any existing child posts (idempotent — safe for repeated runs).
    3. **post_child()** — render an agent's TurnResult as a child post with
       full metadata (agent, confidence, trace_id, lock_state, etc.).
    4. **run_council()** — orchestrate the full multi-agent decision loop:
       spawn agents, collect turns, apply CHP validation, and lock the room.
    """

    def __init__(
        self,
        client: SpacebaseClient,
        router: IntentRouter | None = None,
        council: CouncilRunner | None = None,
    ) -> None:
        self.client = client
        self.router = router or IntentRouter()
        self.council = council or CouncilRunner()
        self._seen_intents: set[str] = set()

    async def scan_intents(self, space_id: str, since: float | None = None) -> list[dict[str, Any]]:
        """Scan a Spacebase space and return classified candidate intents.

        Returns a list of dicts, each containing:

        * ``intent`` — the raw Intent model
        * ``route`` — the RouteDecision from the IntentRouter
        * ``is_new`` — True if this intent was not seen in a previous scan

        Filtered intents (route.is_supported=False) are still returned
        but marked for informational purposes only.
        """
        result: ScanResult = await self.client.scan(space_id, since=since)
        classified = []
        for intent in result.intents:
            is_new = intent.intent_id not in self._seen_intents
            self._seen_intents.add(intent.intent_id)
            route = self.router.classify(intent)
            classified.append({
                "intent": intent,
                "route": route,
                "is_new": is_new,
            })
            logger.info(
                "Classified intent %s -> %s (new=%s)",
                intent.intent_id,
                route.role,
                is_new,
            )
        return classified

    async def enter_space(self, intent_id: str) -> PostTree | None:
        """Enter an intent's interior and return the existing post tree.

        This is idempotent: calling it twice for the same intent_id will
        not create duplicate child rooms. It simply reads what exists.
        """
        tree = await self.client.get_post_tree(intent_id)
        if tree is not None:
            logger.info(
                "Entered space %s — %d direct children",
                intent_id,
                len(tree.children),
            )
        else:
            logger.info("Entered space %s — empty (new decision room)", intent_id)
        return tree

    async def post_child(
        self,
        parent_id: str,
        title: str,
        body: str,
        agent: str = "",
        confidence: float | None = None,
        produces: list[str] | None = None,
        consumes: list[str] | None = None,
        lock_state: LockState = LockState.PROVISIONAL,
        trace_id: str = "",
        parent_intent_id: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Post:
        """Render an agent's TurnResult as a child post inside a decision room.

        All Consensus Commons metadata is attached so the demo visibly proves
        the system is native to nested intent spaces.

        Args:
            parent_id: The intent_id of the parent decision room.
            title: Short title for the agent's contribution.
            body: Full body text (expansion/compression trace, analysis, etc.).
            agent: Name/role of the contributing agent.
            confidence: 0.0–1.0 confidence score (if applicable).
            produces: Data artifacts this post produces.
            consumes: Data artifacts this post consumes.
            lock_state: Current lock state of this post.
            trace_id: Correlation ID for the orchestrator trace.
            parent_intent_id: Root intent ID for traceability.
            extra: Additional metadata fields.

        Returns:
            The created Post model.
        """
        metadata = {
            "agent": agent,
            "confidence": confidence,
            "produces": produces or [],
            "consumes": consumes or [],
            "lock_state": lock_state.value,
            "parent_intent_id": parent_intent_id,
            "trace_id": trace_id,
            **(extra or {}),
        }
        post = await self.client.post_child(parent_id, title, body, metadata=metadata)
        logger.info(
            "Posted child %s [%s] under %s (lock=%s)",
            post.post_id,
            agent,
            parent_id,
            lock_state.value,
        )
        return post

    async def run_council(
        self,
        intent: Intent,
        topic: str | None = None,
        max_agents: int = 4,
    ) -> CouncilReport:
        """Run the full multi-agent decision council on an intent.

        This is the main entry point for the demo:

        1. Classify the intent via the router.
        2. Spawn agents according to the route's role set.
        3. Each agent produces a TurnResult (rendered as a child post).
        4. An adversarial agent challenges the consensus.
        5. A validator agent checks for soundness.
        6. If validated, the room is locked.

        Args:
            intent: The root intent representing the decision problem.
            topic: Override topic string (defaults to intent.content).
            max_agents: Maximum number of agents to spawn.

        Returns:
            A CouncilReport with all posts, the final lock state, and timing.
        """
        topic = topic or intent.content
        trace_id = uuid.uuid4().hex[:8]
        start_time = time.time()

        logger.info("Starting council for intent %s (trace=%s)", intent.intent_id, trace_id)

        # 1. Classify
        route = self.router.classify(intent)
        logger.info("Route: role=%s, supported=%s, agents=%s", route.role, route.is_supported, route.agents)

        if not route.is_supported:
            logger.warning("Intent %s not supported: %s", intent.intent_id, route.reason)
            await self.post_child(
                parent_id=intent.intent_id,
                title="Unsupported Intent",
                body=f"This topic is not supported for public council: {route.reason}",
                agent="router",
                lock_state=LockState.FAILED,
                trace_id=trace_id,
                parent_intent_id=intent.intent_id,
            )
            await self.client.lock_intent(intent.intent_id, LockState.FAILED)
            return CouncilReport(
                root_intent_id=intent.intent_id,
                topic=topic,
                trace_id=trace_id,
                posts=[],
                final_state=LockState.FAILED,
                duration=time.time() - start_time,
            )

        # 2. Run council via CouncilRunner
        report = await self.council.run(
            adapter=self,
            intent=intent,
            route=route,
            trace_id=trace_id,
            max_agents=max_agents,
        )

        report.duration = time.time() - start_time
        logger.info(
            "Council complete: %d posts, final_state=%s (%.2fs)",
            len(report.posts),
            report.final_state.value,
            report.duration,
        )
        return report

    async def close(self) -> None:
        """Clean up resources."""
        if hasattr(self.client, "close"):
            await self.client.close()
