"""
Core Consensus Engine Unit Tests
Run: pytest tests/test_core.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import ConsensusEngine
from skill.types import COEEvent, Primitive, VerificationResult, ConsensusPolicy
from datetime import datetime, timezone
from skill.security import sign_event,b64
from skill.core import event_digest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
keys={i:Ed25519PrivateKey.generate() for i in ["A","B","C","D","E"]}
public={i:{"test":b64(k.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw))} for i,k in keys.items()}


def test_simple_majority_consensus():
    """Three confirmations out of three -> resolved."""
    engine = ConsensusEngine(validators=["B","C","D","E"],trusted_keys=public,policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j1", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t1",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v1 = COEEvent("v1", Primitive.VERIFY, "B", datetime.now(timezone.utc), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v2", Primitive.VERIFY, "C", datetime.now(timezone.utc), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)
    v3 = COEEvent("v3", Primitive.VERIFY, "D", datetime.now(timezone.utc), "t1",
                  verify_of=["j1"], verification_result=VerificationResult.CONFIRMED, confidence=0.85)

    for e in [j, v1, v2, v3]:
        if e.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            ref=e.verify_of[0] if e.verify_of else e.terminate_of
            e.reference_digest=event_digest(next(p for p in engine.events if p.event_id==ref))
        e.signature=sign_event(e,engine.context,keys[e.issuer],"test")
        engine.add_event(e)

    result = engine.run(target="t1")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "open"
    assert result.sws.assertions[0]["confirmations"] == 3


def test_weighted_trust_consensus():
    """Weighted trust exceeds threshold -> resolved."""
    engine = ConsensusEngine(validators=["B","C","D","E"],trusted_keys=public,policy=ConsensusPolicy.WEIGHTED_TRUST)
    engine.set_weighted_threshold(2.0)
    engine.set_trust_weight("B", 0.8)
    engine.set_trust_weight("C", 1.0)

    j = COEEvent("j2", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t2",
                 assertion={"subject": "door", "predicate": "status", "value": "closed"}, confidence=0.95)
    v1 = COEEvent("v4", Primitive.VERIFY, "B", datetime.now(timezone.utc), "t2",
                  verify_of=["j2"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v5", Primitive.VERIFY, "C", datetime.now(timezone.utc), "t2",
                  verify_of=["j2"], verification_result=VerificationResult.CONFIRMED, confidence=1.0)

    v3 = COEEvent("extra",Primitive.VERIFY,"D",datetime.now(timezone.utc),"t2",verify_of=["j2"],verification_result=VerificationResult.CONFIRMED,confidence=1.0)
    for e in [j, v1, v2, v3]:
        if e.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            ref=e.verify_of[0] if e.verify_of else e.terminate_of
            e.reference_digest=event_digest(next(p for p in engine.events if p.event_id==ref))
        e.signature=sign_event(e,engine.context,keys[e.issuer],"test")
        engine.add_event(e)

    result = engine.run(target="t2")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "closed"


def test_bft_consensus():
    """BFT with n=4 and f=1 requires n-f=3 distinct confirmations."""
    engine = ConsensusEngine(validators=["B","C","D","E"],trusted_keys=public,policy=ConsensusPolicy.BFT)
    engine.set_bft_params(1)

    j = COEEvent("j3", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t3",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v1 = COEEvent("v6", Primitive.VERIFY, "B", datetime.now(timezone.utc), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v7", Primitive.VERIFY, "C", datetime.now(timezone.utc), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)
    v3 = COEEvent("v8", Primitive.VERIFY, "D", datetime.now(timezone.utc), "t3",
                  verify_of=["j3"], verification_result=VerificationResult.CONFIRMED, confidence=0.85)

    for e in [j, v1, v2, v3]:
        if e.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            ref=e.verify_of[0] if e.verify_of else e.terminate_of
            e.reference_digest=event_digest(next(p for p in engine.events if p.event_id==ref))
        e.signature=sign_event(e,engine.context,keys[e.issuer],"test")
        engine.add_event(e)

    result = engine.run(target="t3")
    assert result.resolved is True
    assert result.sws is not None


def test_termination_invalidates_old():
    """Terminate event removes old assertion from consensus."""
    engine = ConsensusEngine(validators=["B","C","D","E"],trusted_keys=public,policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j4", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t4",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    t = COEEvent("t1", Primitive.TERMINATE, "A", datetime.now(timezone.utc), "t4", terminate_of="j4")
    j2 = COEEvent("j5", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t4",
                  assertion={"subject": "door", "predicate": "status", "value": "closed"}, confidence=0.9)
    v = COEEvent("v9", Primitive.VERIFY, "B", datetime.now(timezone.utc), "t4",
                 verify_of=["j5"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)
    v2 = COEEvent("v10", Primitive.VERIFY, "C", datetime.now(timezone.utc), "t4",
                  verify_of=["j5"], verification_result=VerificationResult.CONFIRMED, confidence=0.8)

    v3 = COEEvent("extra",Primitive.VERIFY,"D",datetime.now(timezone.utc),"t4",verify_of=["j5"],verification_result=VerificationResult.CONFIRMED,confidence=1.0)
    for e in [j, t, j2, v, v2, v3]:
        if e.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            ref=e.verify_of[0] if e.verify_of else e.terminate_of
            e.reference_digest=event_digest(next(p for p in engine.events if p.event_id==ref))
        e.signature=sign_event(e,engine.context,keys[e.issuer],"test")
        engine.add_event(e)

    result = engine.run(target="t4")
    assert result.resolved is True
    assert result.sws is not None
    assert result.sws.assertions[0]["value"] == "closed"


def test_unresolved_insufficient_verifications():
    """Only one verification -> unresolved under simple majority."""
    engine = ConsensusEngine(validators=["B","C","D","E"],trusted_keys=public,policy=ConsensusPolicy.SIMPLE_MAJORITY)

    j = COEEvent("j6", Primitive.JUDGE, "A", datetime.now(timezone.utc), "t5",
                 assertion={"subject": "door", "predicate": "status", "value": "open"}, confidence=0.9)
    v = COEEvent("v11", Primitive.VERIFY, "B", datetime.now(timezone.utc), "t5",
                 verify_of=["j6"], verification_result=VerificationResult.CONFIRMED, confidence=0.9)

    for e in [j, v]:
        if e.primitive in (Primitive.VERIFY,Primitive.TERMINATE):
            ref=e.verify_of[0] if e.verify_of else e.terminate_of
            e.reference_digest=event_digest(next(p for p in engine.events if p.event_id==ref))
        e.signature=sign_event(e,engine.context,keys[e.issuer],"test")
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
