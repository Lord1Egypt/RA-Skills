"""
COE Consensus Engine Core
Implements three consensus policies from COE Protocol Section 4.2:
- Simple Majority
- Weighted Trust
- Byzantine Fault Tolerance (BFT)
"""
from typing import List, Dict, Optional, Any, Tuple
from collections import defaultdict
from datetime import datetime
from uuid import uuid4

from .types import (
    COEEvent, Primitive, ConsensusPolicy, VerificationResult,
    AssertionKey, SharedWorldState, ConsensusResult, TrustWeight
)


class ConsensusEngine:
    """
    COE Consensus Engine.
    Collects J/V events, resolves conflicts, produces Shared World State.
    """

    def __init__(self, policy: ConsensusPolicy = ConsensusPolicy.SIMPLE_MAJORITY):
        self.policy = policy
        self.events: List[COEEvent] = []
        self.trust_weights: Dict[str, float] = {}
        self.bft_fault_tolerance: int = 1  # f for BFT policy
        self.weighted_threshold: float = 1.5
        self.min_verifications: int = 3  # minimum V events before evaluation
        self.timeout_seconds: float = 30.0

    def add_event(self, event: COEEvent) -> None:
        """Ingest a COE event into the engine."""
        self.events.append(event)

    def set_trust_weight(self, issuer: str, weight: float) -> None:
        """Set trust weight for a Cognitive Unit."""
        self.trust_weights[issuer] = weight

    def set_bft_params(self, fault_tolerance: int) -> None:
        """Configure BFT fault tolerance parameter f."""
        self.bft_fault_tolerance = fault_tolerance

    def set_weighted_threshold(self, threshold: float) -> None:
        """Configure weighted trust confirmation threshold."""
        self.weighted_threshold = threshold

    def run(self, target: Optional[str] = None) -> ConsensusResult:
        """
        Execute consensus on collected events.

        Args:
            target: Optional target world model ID to filter events.

        Returns:
            ConsensusResult with SWS or unresolved conflicts.
        """
        events = [e for e in self.events if target is None or e.target == target]

        if not events:
            return ConsensusResult(
                sws=None,
                resolved=False,
                conflicts=[],
                policy=self.policy,
                message="No events to process.",
                events_processed=0,
                events_by_issuer={}
            )

        # Group events by issuer for stats
        events_by_issuer = defaultdict(int)
        for e in events:
            events_by_issuer[e.issuer] += 1

        # Separate J and V events
        j_events = [e for e in events if e.primitive == Primitive.JUDGE]
        v_events = [e for e in events if e.primitive == Primitive.VERIFY]
        t_events = [e for e in events if e.primitive == Primitive.TERMINATE]

        # Apply terminations: remove terminated assertions
        terminated_ids = {e.terminate_of for e in t_events if e.terminate_of}
        active_j = [e for e in j_events if e.event_id not in terminated_ids]

        # Group active assertions by key
        assertion_groups: Dict[AssertionKey, List[COEEvent]] = defaultdict(list)
        for e in active_j:
            if e.assertion:
                key = AssertionKey(
                    target=e.target,
                    subject=e.assertion.get("subject", ""),
                    predicate=e.assertion.get("predicate", "")
                )
                assertion_groups[key].append(e)

        # For each assertion, collect verifications
        sws_assertions = []
        unresolved_conflicts = []

        for key, j_list in assertion_groups.items():
            # Get verifications for any J event in this group
            j_ids = {j.event_id for j in j_list}
            relevant_v = [v for v in v_events if v.verify_of and any(vid in j_ids for vid in v.verify_of)]

            # Evaluate consensus for this assertion
            consensus_value, confidence, confirmations, resolved = self._evaluate_assertion(
                j_list, relevant_v
            )

            if resolved:
                sws_assertions.append({
                    "subject": key.subject,
                    "predicate": key.predicate,
                    "value": consensus_value,
                    "confidence": confidence,
                    "based_on": [j.event_id for j in j_list],
                    "consensus_policy": self.policy.value,
                    "confirmations": confirmations
                })
            else:
                # Collect conflict info
                values = {}
                for j in j_list:
                    val = j.assertion.get("value") if j.assertion else None
                    values[val] = values.get(val, 0) + 1

                unresolved_conflicts.append({
                    "subject": key.subject,
                    "predicate": key.predicate,
                    "target": key.target,
                    "proposed_values": values,
                    "verifications_received": len(relevant_v),
                    "reason": "Insufficient verifications to reach consensus under current policy."
                })

        # Build SWS if we have any resolved assertions
        sws = None
        if sws_assertions:
            sws = SharedWorldState(
                sws_id=str(uuid4()),
                target=target or "global",
                timestamp=datetime.utcnow(),
                assertions=sws_assertions
            )

        resolved = len(unresolved_conflicts) == 0 and len(sws_assertions) > 0

        return ConsensusResult(
            sws=sws,
            resolved=resolved,
            conflicts=unresolved_conflicts,
            policy=self.policy,
            message=f"Consensus complete. {len(sws_assertions)} assertions resolved, {len(unresolved_conflicts)} conflicts remain.",
            events_processed=len(events),
            events_by_issuer=dict(events_by_issuer)
        )

    def _evaluate_assertion(
        self,
        j_events: List[COEEvent],
        v_events: List[COEEvent]
    ) -> Tuple[Any, float, int, bool]:
        """
        Evaluate consensus for a single assertion.

        Returns:
            (consensus_value, confidence, confirmation_count, is_resolved)
        """
        if not j_events:
            return None, 0.0, 0, False

        # Default to the most recent J event value if no verifications
        if not v_events:
            if self.policy == ConsensusPolicy.SIMPLE_MAJORITY and len(j_events) == 1:
                val = j_events[0].assertion.get("value") if j_events[0].assertion else None
                conf = j_events[0].confidence or 1.0
                return val, conf, 0, True
            return None, 0.0, 0, False

        # Count by value
        value_votes: Dict[Any, List[COEEvent]] = defaultdict(list)
        for v in v_events:
            if v.verification_result == VerificationResult.CONFIRMED:
                # Find which J event this verifies
                for j in j_events:
                    if v.verify_of and j.event_id in v.verify_of:
                        val = j.assertion.get("value") if j.assertion else None
                        value_votes[val].append(v)
                        break

        if self.policy == ConsensusPolicy.SIMPLE_MAJORITY:
            return self._simple_majority(value_votes, v_events)
        elif self.policy == ConsensusPolicy.WEIGHTED_TRUST:
            return self._weighted_trust(value_votes, j_events)
        elif self.policy == ConsensusPolicy.BFT:
            return self._bft(value_votes, v_events)

        return None, 0.0, 0, False

    def _simple_majority(
        self,
        value_votes: Dict[Any, List[COEEvent]],
        all_v: List[COEEvent]
    ) -> Tuple[Any, float, int, bool]:
        total = len(all_v)
        if total < self.min_verifications:
            return None, 0.0, total, False

        best_value = None
        best_count = 0
        for val, votes in value_votes.items():
            if len(votes) > best_count:
                best_count = len(votes)
                best_value = val

        if best_count > total * 0.5:
            confidence = best_count / total
            return best_value, confidence, best_count, True

        return best_value, best_count / total if total > 0 else 0.0, best_count, False

    def _weighted_trust(
        self,
        value_votes: Dict[Any, List[COEEvent]],
        j_events: List[COEEvent]
    ) -> Tuple[Any, float, int, bool]:
        # Calculate weighted confirmation score per value
        value_weights: Dict[Any, float] = defaultdict(float)
        value_counts: Dict[Any, int] = defaultdict(int)

        for val, votes in value_votes.items():
            for v in votes:
                w = self.trust_weights.get(v.issuer, 0.5)
                conf = v.confidence or 1.0
                value_weights[val] += w * conf
                value_counts[val] += 1

        if not value_weights:
            return None, 0.0, 0, False

        best_value = max(value_weights, key=lambda k: value_weights[k])
        best_weight = value_weights[best_value]

        if best_weight > self.weighted_threshold:
            return best_value, min(best_weight / (self.weighted_threshold * 1.5), 1.0), value_counts[best_value], True

        return best_value, best_weight / self.weighted_threshold if self.weighted_threshold > 0 else 0.0, value_counts[best_value], False

    def _bft(
        self,
        value_votes: Dict[Any, List[COEEvent]],
        all_v: List[COEEvent]
    ) -> Tuple[Any, float, int, bool]:
        f = self.bft_fault_tolerance
        total = len(all_v)

        # Need at least 2f+1 total verifications
        if total < 2 * f + 1:
            return None, 0.0, total, False

        best_value = None
        best_count = 0
        for val, votes in value_votes.items():
            if len(votes) > best_count:
                best_count = len(votes)
                best_value = val

        # Need more than f+1 confirmed for a value
        if best_count > f + 1:
            confidence = best_count / total
            return best_value, confidence, best_count, True

        return best_value, best_count / total if total > 0 else 0.0, best_count, False
