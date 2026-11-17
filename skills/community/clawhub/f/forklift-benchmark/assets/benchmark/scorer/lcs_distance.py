"""FK-Bench v2 — Action sequence similarity via LCS.

The action sequence is reduced to a list of action ``kind`` strings
(NAVIGATE, LIFT, ...). The similarity is the length of the longest
common subsequence divided by the length of the longer sequence, with
ties broken by Jaccard similarity on the kind sets.

Returns a float in [0, 1].
"""

from __future__ import annotations

from typing import List, Sequence

from dsl.actions import Action


def _lcs_ratio(a: Sequence[str], b: Sequence[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
    lcs = dp[m][n]
    return lcs / max(m, n)


def _jaccard(a: Sequence[str], b: Sequence[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def action_sequence_similarity(gold: List[Action], pred: List[Action]) -> float:
    """Compute action sequence similarity in [0, 1].

    0.7 * LCS(kind string) + 0.3 * Jaccard(kind set).
    """
    gk = [a.kind for a in gold]
    pk = [a.kind for a in pred]
    return round(0.7 * _lcs_ratio(gk, pk) + 0.3 * _jaccard(gk, pk), 4)
