"""
Determinability Checker Core Engine
Implements CheckDeterminability (Theorem 10.1), Conflict Graph, Evidence Coverage (Theorem 8.2)
"""
from typing import List, Dict, Tuple, Set, Optional, Any, Callable
from collections import defaultdict
from .security import canonical

def scalar_key(value):
    if value is not None and not isinstance(value,(str,bool,int,float)):
        raise ValueError("Observation and target must be JSON scalars")
    return canonical(value).decode()

from .types import (
    Config, CheckResult, DeterminabilityResult, DecisionTable,
    CounterExample, ConflictEdge, EvidenceGap, OmegaFunc, TargetFunc, EvidenceFunc
)


class DeterminabilityCore:
    """
    Core engine for causal sufficiency determinability checking.
    Direct implementation of the paper algorithm.
    """

    @staticmethod
    def check(
        configs: List[Config],
        omega: OmegaFunc,
        target: TargetFunc,
        evidences: Optional[List[Tuple[str, EvidenceFunc]]] = None
    ) -> CheckResult:
        if not 1 <= len(configs) <= 128:
            raise ValueError("Provide 1 to 128 configurations")
        if len({c.config_id for c in configs}) != len(configs) or any(not isinstance(c.config_id,str) or not c.config_id for c in configs):
            raise ValueError("Unique nonempty configuration IDs required")
        if evidences and len(evidences)>32: raise ValueError("At most 32 evidence fields")
        observations={c.config_id:scalar_key(omega(c)) for c in configs}
        targets={c.config_id:scalar_key(target(c)) for c in configs}
        groups: Dict[Any, List[Config]] = defaultdict(list)
        for C in configs:
            groups[scalar_key(omega(C))].append(C)

        decision_table = {}
        counterexample = None
        conflict_edges = []

        for w, group in groups.items():
            values = {scalar_key(target(C)) for C in group}
            if len(values) > 1:
                vals = list(values)
                C1 = next(C for C in group if scalar_key(target(C)) == vals[0])
                C2 = next(C for C in group if scalar_key(target(C)) == vals[1])
                counterexample = CounterExample(
                    config1=C1, config2=C2,
                    observation_value=w,
                    target1=target(C1), target2=target(C2)
                )
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        if scalar_key(target(group[i])) != scalar_key(target(group[j])):
                            conflict_edges.append(ConflictEdge(
                                config1=group[i], config2=group[j],
                                observation_class=w
                            ))
            else:
                decision_table[w] = target(group[0])

        if counterexample:
            result = CheckResult(
                result=DeterminabilityResult.NOT_DETERMINED,
                counterexample=counterexample,
                conflict_graph=conflict_edges,
                message=(f"Non-determinability proven: configs {counterexample.config1.config_id} "
                         f"and {counterexample.config2.config_id} share observation {counterexample.observation_value} "
                         f"but differ on target ({counterexample.target1} vs {counterexample.target2}).")
            )
            if evidences:
                result.evidence_gaps = DeterminabilityCore._analyze_evidence_gaps(
                    conflict_edges, evidences
                )
            return result

        return CheckResult(
            result=DeterminabilityResult.DETERMINED,
            decision_table=DecisionTable(
                mapping=decision_table,
                observation_count=len(groups),
                config_count=len(configs)
            ),
            message=f"Target is zero-error determinable. Decision table covers {len(groups)} observation classes over {len(configs)} configurations."
        )

    @staticmethod
    def _analyze_evidence_gaps(
        conflict_edges: List[ConflictEdge],
        evidences: List[Tuple[str, EvidenceFunc]]
    ) -> List[EvidenceGap]:
        gaps = []
        for edge in conflict_edges:
            required = []
            for name, E in evidences:
                if canonical(E(edge.config1)) != canonical(E(edge.config2)):
                    required.append(name)
            gaps.append(EvidenceGap(
                conflict_edge=edge,
                required_evidence=required
            ))
        return gaps

    @staticmethod
    def find_minimal_evidence_cover(
        conflict_edges: List[ConflictEdge],
        evidences: List[Tuple[str, EvidenceFunc]]
    ) -> Optional[List[str]]:
        if len(conflict_edges)>8128 or len(evidences)>32: raise ValueError("Evidence work limit exceeded")
        if not conflict_edges:
            return []

        uncovered = set(range(len(conflict_edges)))
        evidence_covers: Dict[str, Set[int]] = {}

        for name, E in evidences:
            covers = set()
            for idx, edge in enumerate(conflict_edges):
                if canonical(E(edge.config1)) != canonical(E(edge.config2)):
                    covers.add(idx)
            evidence_covers[name] = covers

        selected = []
        while uncovered:
            best_name = None
            best_cover = set()
            for name, covers in evidence_covers.items():
                current = covers & uncovered
                if len(current) > len(best_cover):
                    best_cover = current
                    best_name = name

            if not best_cover or best_name is None:
                return None

            selected.append(best_name)
            uncovered -= best_cover

        return selected

    @staticmethod
    def ambiguity_set_size(
        configs: List[Config],
        omega: OmegaFunc,
        target: TargetFunc
    ) -> Dict[Any, int]:
        if not 1 <= len(configs) <= 128: raise ValueError("Provide 1 to 128 configurations")
        groups: Dict[Any, List[Config]] = defaultdict(list)
        for C in configs:
            groups[scalar_key(omega(C))].append(C)
        return {
            w: len({scalar_key(target(C)) for C in group})
            for w, group in groups.items()
        }
