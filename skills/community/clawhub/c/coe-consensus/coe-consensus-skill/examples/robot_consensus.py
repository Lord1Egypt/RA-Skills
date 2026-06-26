"""
COE Consensus Skill Example: Multi-Robot Door State Consensus
Reproduces COE Protocol Appendix A verification workflow.
Run: python robot_consensus.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import ConsensusEngine
from skill.types import COEEvent, Primitive, VerificationResult, ConsensusPolicy
from datetime import datetime


def run_robot_example():
    """Three robots (A, B, C) collaboratively confirm door state."""

    print("=" * 70)
    print("COE Consensus Example: Robot Door-State Consensus")
    print("=" * 70)

    # --- Scenario 1: Simple Majority ---
    print("\n[Policy: Simple Majority]")
    engine = ConsensusEngine(policy=ConsensusPolicy.SIMPLE_MAJORITY)

    events_sm = [
        COEEvent("evt-1", Primitive.JUDGE, "robot-A", datetime(2026, 4, 19, 10, 30, 0), "warehouse-zone-3",
                 assertion={"subject": "door_01", "predicate": "status", "value": "open"}, confidence=0.95),
        COEEvent("evt-2", Primitive.VERIFY, "robot-B", datetime(2026, 4, 19, 10, 30, 5), "warehouse-zone-3",
                 verify_of=["evt-1"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
        COEEvent("evt-3", Primitive.VERIFY, "robot-C", datetime(2026, 4, 19, 10, 30, 10), "warehouse-zone-3",
                 verify_of=["evt-1"], verification_result=VerificationResult.CONFIRMED, confidence=0.85),
    ]
    for e in events_sm:
        engine.add_event(e)

    result = engine.run(target="warehouse-zone-3")
    print(f"  Resolved: {result.resolved}")
    print(f"  Message: {result.message}")
    if result.sws:
        for a in result.sws.assertions:
            print(f"  SWS: {a['subject']} = {a['value']} (confidence={a['confidence']:.2f}, confirmations={a['confirmations']})")

    # --- Scenario 2: Weighted Trust ---
    print("\n[Policy: Weighted Trust]")
    engine2 = ConsensusEngine(policy=ConsensusPolicy.WEIGHTED_TRUST)
    engine2.set_weighted_threshold(1.5)
    engine2.set_trust_weight("robot-A", 0.9)
    engine2.set_trust_weight("robot-B", 0.8)
    engine2.set_trust_weight("human-1", 1.0)

    events_wt = [
        COEEvent("evt-4", Primitive.JUDGE, "robot-A", datetime(2026, 4, 19, 10, 35, 0), "warehouse-zone-3",
                 assertion={"subject": "door_01", "predicate": "status", "value": "closed"}, confidence=0.95),
        COEEvent("evt-5", Primitive.VERIFY, "robot-B", datetime(2026, 4, 19, 10, 35, 5), "warehouse-zone-3",
                 verify_of=["evt-4"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
        COEEvent("evt-6", Primitive.VERIFY, "human-1", datetime(2026, 4, 19, 10, 35, 10), "warehouse-zone-3",
                 verify_of=["evt-4"], verification_result=VerificationResult.CONFIRMED, confidence=1.0),
    ]
    for e in events_wt:
        engine2.add_event(e)

    result2 = engine2.run(target="warehouse-zone-3")
    print(f"  Resolved: {result2.resolved}")
    print(f"  Message: {result2.message}")
    if result2.sws:
        for a in result2.sws.assertions:
            print(f"  SWS: {a['subject']} = {a['value']} (confidence={a['confidence']:.2f}, confirmations={a['confirmations']})")

    # --- Scenario 3: BFT ---
    print("\n[Policy: Byzantine Fault Tolerance (f=1)]")
    engine3 = ConsensusEngine(policy=ConsensusPolicy.BFT)
    engine3.set_bft_params(1)

    events_bft = [
        COEEvent("evt-7", Primitive.JUDGE, "robot-A", datetime(2026, 4, 19, 10, 40, 0), "warehouse-zone-3",
                 assertion={"subject": "door_01", "predicate": "status", "value": "open"}, confidence=0.95),
        COEEvent("evt-8", Primitive.VERIFY, "robot-B", datetime(2026, 4, 19, 10, 40, 5), "warehouse-zone-3",
                 verify_of=["evt-7"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
        COEEvent("evt-9", Primitive.VERIFY, "robot-C", datetime(2026, 4, 19, 10, 40, 10), "warehouse-zone-3",
                 verify_of=["evt-7"], verification_result=VerificationResult.CONFIRMED, confidence=0.85),
        COEEvent("evt-10", Primitive.VERIFY, "robot-D", datetime(2026, 4, 19, 10, 40, 15), "warehouse-zone-3",
                 verify_of=["evt-7"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
    ]
    for e in events_bft:
        engine3.add_event(e)

    result3 = engine3.run(target="warehouse-zone-3")
    print(f"  Resolved: {result3.resolved}")
    print(f"  Message: {result3.message}")
    if result3.sws:
        for a in result3.sws.assertions:
            print(f"  SWS: {a['subject']} = {a['value']} (confidence={a['confidence']:.2f}, confirmations={a['confirmations']})")

    # --- Scenario 4: Termination + Re-consensus ---
    print("\n[Scenario: Terminate old state, re-consensus new state]")
    engine4 = ConsensusEngine(policy=ConsensusPolicy.SIMPLE_MAJORITY)

    events_term = [
        COEEvent("evt-11", Primitive.JUDGE, "robot-A", datetime(2026, 4, 19, 10, 45, 0), "warehouse-zone-3",
                 assertion={"subject": "door_01", "predicate": "status", "value": "open"}, confidence=0.95),
        COEEvent("evt-12", Primitive.VERIFY, "robot-B", datetime(2026, 4, 19, 10, 45, 5), "warehouse-zone-3",
                 verify_of=["evt-11"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
        COEEvent("evt-13", Primitive.VERIFY, "robot-C", datetime(2026, 4, 19, 10, 45, 10), "warehouse-zone-3",
                 verify_of=["evt-11"], verification_result=VerificationResult.CONFIRMED, confidence=0.85),
        COEEvent("evt-14", Primitive.TERMINATE, "robot-A", datetime(2026, 4, 19, 10, 46, 0), "warehouse-zone-3",
                 terminate_of="evt-11"),
        COEEvent("evt-15", Primitive.JUDGE, "robot-A", datetime(2026, 4, 19, 10, 46, 5), "warehouse-zone-3",
                 assertion={"subject": "door_01", "predicate": "status", "value": "closed"}, confidence=0.95),
        COEEvent("evt-16", Primitive.VERIFY, "robot-B", datetime(2026, 4, 19, 10, 46, 10), "warehouse-zone-3",
                 verify_of=["evt-15"], verification_result=VerificationResult.CONFIRMED, confidence=0.9),
        COEEvent("evt-17", Primitive.VERIFY, "robot-C", datetime(2026, 4, 19, 10, 46, 15), "warehouse-zone-3",
                 verify_of=["evt-15"], verification_result=VerificationResult.CONFIRMED, confidence=0.85),
    ]
    for e in events_term:
        engine4.add_event(e)

    result4 = engine4.run(target="warehouse-zone-3")
    print(f"  Resolved: {result4.resolved}")
    print(f"  Message: {result4.message}")
    if result4.sws:
        for a in result4.sws.assertions:
            print(f"  SWS: {a['subject']} = {a['value']} (confidence={a['confidence']:.2f}, confirmations={a['confirmations']})")

    print("\n" + "=" * 70)
    print("All scenarios completed.")
    print("=" * 70)


if __name__ == "__main__":
    run_robot_example()
