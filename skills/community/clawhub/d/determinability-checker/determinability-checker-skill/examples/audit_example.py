"""
Paper Section 10.2 Reproduction: LLM Agent Tool-Call Audit
Run: python audit_example.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import DeterminabilityCore
from skill.types import Config, DeterminabilityResult


def run_paper_example():
    """Reproduce Table 1 from the paper: 8-configuration audit case."""

    configs_data = [
        {"id": "C1", "output": "correct", "tool": "code", "verif_flag": 1, "verif_hash": "valid_hash",   "target": 1},
        {"id": "C2", "output": "correct", "tool": "code", "verif_flag": 0, "verif_hash": "none",         "target": 0},
        {"id": "C3", "output": "correct", "tool": "calc", "verif_flag": 0, "verif_hash": "none",         "target": 0},
        {"id": "C4", "output": "correct", "tool": "search", "verif_flag": 0, "verif_hash": "none",       "target": 0},
        {"id": "C5", "output": "error",   "tool": "code", "verif_flag": 1, "verif_hash": "failed_hash",  "target": 0},
        {"id": "C6", "output": "correct", "tool": "code", "verif_flag": 1, "verif_hash": "forged_hash",  "target": 0},
        {"id": "C7", "output": "error",   "tool": "search", "verif_flag": 0, "verif_hash": "none",        "target": 0},
        {"id": "C8", "output": "error",   "tool": "calc", "verif_flag": 0, "verif_hash": "none",         "target": 0},
    ]

    configs = [Config(config_id=d["id"], data=d) for d in configs_data]

    evidences = [
        ("tool_type", lambda C: C.data["tool"]),
        ("verif_flag", lambda C: C.data["verif_flag"]),
        ("verif_hash", lambda C: C.data["verif_hash"]),
    ]

    print("=" * 70)
    print("Paper Section 10.2 Reproduction: LLM Agent Tool-Call Audit")
    print("=" * 70)

    observation_levels = [
        ("Omega0: output only", lambda C: C.data["output"]),
        ("OmegaT: output + tool type", lambda C: (C.data["output"], C.data["tool"])),
        ("OmegaTV: output + tool + verification flag", lambda C: (C.data["output"], C.data["tool"], C.data["verif_flag"])),
        ("OmegaTVH: output + tool + flag + hash", lambda C: (C.data["output"], C.data["tool"], C.data["verif_flag"], C.data["verif_hash"])),
    ]

    for name, omega in observation_levels:
        print(f"\n[{name}]")
        result = DeterminabilityCore.check(configs, omega, lambda C: C.data["target"], evidences)

        if result.result == DeterminabilityResult.DETERMINED:
            print(f"  Result: DETERMINED [OK]")
            print(f"  Decision Table: {result.decision_table.mapping}")
        else:
            print(f"  Result: NOT_DETERMINED [FAIL]")
            ce = result.counterexample
            print(f"  Counterexample: {ce.config1.config_id} vs {ce.config2.config_id}")
            print(f"    Observation={ce.observation_value}, Target conflict={ce.target1} vs {ce.target2}")

            if result.evidence_gaps:
                print(f"  Conflict edges: {len(result.conflict_graph)}")
                minimal = DeterminabilityCore.find_minimal_evidence_cover(result.conflict_graph, evidences)
                if minimal:
                    print(f"  Minimal evidence cover: {minimal}")

    print("\n" + "=" * 70)
    print("Expected results:")
    print("  Omega0      -> NOT_DETERMINED (C1/C2 conflict under 'correct')")
    print("  OmegaT      -> NOT_DETERMINED (C1/C2 conflict under (correct, code))")
    print("  OmegaTV     -> NOT_DETERMINED (C1/C6 conflict under (correct, code, 1))")
    print("  OmegaTVH    -> DETERMINED (valid_hash uniquely maps to 1)")
    print("=" * 70)


if __name__ == "__main__":
    run_paper_example()
