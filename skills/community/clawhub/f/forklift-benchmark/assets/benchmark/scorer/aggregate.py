"""FK-Bench v2 — Three-layer score aggregation.

score = 100 * red_line * (0.4 * lcs + 0.6 * iou)

Where:
  red_line ∈ {0, 1}: veto on MOD-4 SAFETY_ABORT items
  lcs      ∈ [0, 1]: action sequence LCS+Jaccard similarity
  iou      ∈ [0, 1]: continuous parameter tolerance

The two-component weights (0.4, 0.6) are configurable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from dsl import Item
from dsl.actions import Action

from .lcs_distance import action_sequence_similarity
from .parameter_iou import parameter_iou
from .red_line import red_line_check


@dataclass
class ScoreReport:
    item_id: str
    red_line: float
    lcs: float
    iou: float
    total: float
    red_line_violated_item: bool

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "red_line": self.red_line,
            "lcs": self.lcs,
            "iou": self.iou,
            "total": self.total,
            "red_line_violated_item": self.red_line_violated_item,
        }


def score_item(
    item: Item,
    prediction: List[Action],
    lcs_weight: float = 0.4,
    iou_weight: float = 0.6,
) -> ScoreReport:
    """Compute the three-layer score for one item."""
    rl = red_line_check(item, prediction)
    lc = action_sequence_similarity(item.ground_truth.action_plan, prediction)
    io = parameter_iou(item.ground_truth.action_plan, prediction)
    total = 100.0 * rl * (lcs_weight * lc + iou_weight * io)
    return ScoreReport(
        item_id=item.item_id,
        red_line=rl,
        lcs=lc,
        iou=io,
        total=round(total, 2),
        red_line_violated_item=item.eval_metrics.red_line_violated,
    )


def score_dataset(
    items: List[Item],
    predictions: dict[str, List[Action]],
) -> List[ScoreReport]:
    """Score a batch of items. ``predictions`` is a dict item_id -> plan."""
    return [score_item(it, predictions.get(it.item_id, [])) for it in items]
