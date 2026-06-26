"""
Core Consensus Engine Unit Tests
Run: pytest tests/test_core.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import ConsensusEngine
from skill.types import COEEvent, Primitive, VerificationResult, ConsensusPolicy
from datetime import datetime


def test_simple_majority_consensus():
    """Three confirmations out of three -> resolved."""
    engine = ConsensusEngine(policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j1", Primitive.JUDGE, "A", datetime.now(), "t1",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v1 = COEEvent("v1", Primitive.VERIFY, "B", datetime.now(), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v2", Primitive.VERIFY, "C", datetime.now(), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)
    v3 = COEEvent("v3", Primitive.VERIFY, "D", datetime.now(), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.85)

    for e in [j, v1, v2, v3]:
        engine.add_event(e)

    result = engine.run(target="t1")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "open"
    assert result.sws.assertions[0]["confirmations"] == 3


def test_weighted_trust_consensus():
    """Weighted trust exceeds threshold -> resolved."""
    engine = ConsensusEngine(policy=ConsensusPolicy.WEIGHTED_TRUST)
    engine.set_weighted_threshold(1.5)
    engine.set_trust_weight("B", 0.8)
    engine.set_trust_weight("C", 1.0)

    j = COEEvent("j2", Primitive.JUDGE, "A", datetime.now(), "t2",
                 assertion={"subject": "door", "predicate": "status", "value": "closed"}, confidence=0.95)
    v1 = COEEvent("v4", Primitive.VERIFY, "B", datetime.now(), "t2",
                  verify_of=["j2"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v5", Primitive.VERIFY, "C", datetime.now(), "t2",
                  verify_of=["j2"], verification_result=VerificationResult.CONFIRMED, confidence=1.0)

    for e in [j, v1, v2]:
        engine.add_event(e)

    result = engine.run(target="t2")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "closed"


def test_bft_consensus():
    """BFT with f=1 requires >2 confirmations (f+1=2) out of >=3 total (2f+1=3)."""
    engine = ConsensusEngine(policy=ConsensusPolicy.BFT)
    engine.set_bft_params(1)

    j = COEEvent("j3", Primitive.JUDGE, "A", datetime.now(), "t3",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v1 = COEEvent("v6", Primitive.VERIFY, "B", datetime.now(), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v7", Primitive.VERIFY, "C", datetime.now(), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)
    v3 = COEEvent("v8", Primitive.VERIFY, "D", datetime.now(), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.85)

    for e in [j, v1, v2, v3]:
        engine.add_event(e)

    result = engine.run(target="t3")
    assert result.resolved is True
    assert result.sws is not None


def test_termination_invalidates_old():
    """Terminate event removes old assertion from consensus."""
    engine = ConsensusEngine(policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j4", Primitive.JUDGE, "A", datetime.now(), "t4",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    t = COEEvent("t1", Primitive.TERMINATE, "A", datetime.now(), "t4", terminate_of="j4")
    j2 = COEEvent("j5", Primitive.JUDGE, "A", datetime.now(), "t4",
                  assertion={"subject": "door", "predicate": "status", "value": "closed"}, confidence=0.9)
    v = COEEvent("v9", Primitive.VERIFY, "B", datetime.now(), "t4",
                 verify_of=["j5"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v10", Primitive.VERIFY, "C", datetime.now(), "t4",
                  verify_of=["j5"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)

    for e in [j, t, j2, v, v2]:
        engine.add_event(e)

    result = engine.run(target="t4")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "closed"


def test_unresolved_insufficient_verifications():
    """Only one verification -> unresolved under simple majority."""
    engine = ConsensusEngine(policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j6", Primitive.JUDGE, "A", datetime.now(), "t5",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v = COEEvent("v11", Primitive.VERIFY, "B", datetime.now(), "t5",
                 verify_of=["j6"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)

    for e in [j, v]:
        engine.add_event(e)

    result = engine.run(target="t5")
    assert result.resolved is False
    assert result.sws is None
    assert len(result.conflicts) > 0


if __name__ == "__main__":
    test_simple_majority_consensus()
    test_weighted_trust_consensus()
    test_bft_consensus()
    test_termination_invalidates_old()
    test_unresolved_insufficient_verifications()
    print("All tests passed.")
