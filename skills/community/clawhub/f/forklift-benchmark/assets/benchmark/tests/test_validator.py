"""Tests for FK-Bench v2 validators."""

import pytest

from dsl import (
    ActionPlan,
    EvalMetrics,
    InputContext,
    Item,
    Meta,
    VehicleState,
    EnvironmentObject,
)
from validator import (
    check_all_physics,
    check_center_of_gravity,
    check_derated_capacity,
    check_overload,
    check_safety_red_line,
    validate_item_dict,
)


def _make_item(
    *,
    module: str = "MOD-1",
    difficulty: str = "basic",
    capacity: float = 1500.0,
    load_center_mm: int = 500,
    load_kg: float = 800.0,
    instruction: str = "把 800 kg 的卡板从 A 搬到 B。",
) -> Item:
    return Item(
        item_id="FK-500-TEST-000",
        meta=Meta(module=module, scene_type="S2_BLOCK", difficulty=difficulty),
        input_context=InputContext(
            natural_instruction=instruction,
            vehicle_state=VehicleState(
                model_type="1.5T_counterbalance_electric",
                rated_capacity_kg=capacity,
                load_center_mm=load_center_mm,
            ),
            environment_objects=[
                EnvironmentObject(
                    id="cargo_01",
                    type="pallet",
                    weight_kg=load_kg,
                    center_of_gravity_mm=[500, 500, 400],
                ),
            ],
        ),
        ground_truth=ActionPlan(expected_decision="EXECUTE"),
        eval_metrics=EvalMetrics(red_line_violated=False),
    )


def test_valid_item_passes_physics():
    it = _make_item(load_kg=800.0)
    assert check_all_physics(it, expected_max_height_m=1.5) == []


def test_overload_base_fails():
    it = _make_item(capacity=1500.0, load_kg=1800.0)
    errs = check_overload(it)
    assert errs and errs[0].code == "ERR_OVERLOAD_BASE"


def test_derated_overload_fails():
    # 3T truck, lift 6m: derated capacity = 3000 * 0.6 = 1800. 2500kg is over.
    it = _make_item(
        capacity=3000.0,
        load_kg=2500.0,
        instruction="把 2500 kg 的卡板从 A 搬到 6m 高位。",
    )
    errs = check_derated_capacity(it, 6.0)
    assert errs and errs[0].code == "ERR_DERATED_OVERLOAD"


def test_center_of_gravity_fails():
    # CG at 800mm exceeds rated 500mm by 300mm.
    it = _make_item(load_kg=800.0)
    it.input_context.environment_objects[0].center_of_gravity_mm = [800, 500, 400]
    errs = check_center_of_gravity(it)
    assert errs and errs[0].code == "ERR_CG_FORWARD"


def test_missing_required_field_is_reported():
    bad = {"item_id": "x", "meta": {"module": "MOD-1", "scene_type": "S2_BLOCK", "difficulty": "basic"}}
    errs = validate_item_dict(bad)
    assert any("input_context" in e for e in errs)


def test_safety_redline_flags_overload():
    it = _make_item(
        module="MOD-4",
        difficulty="edge_case",
        capacity=3000.0,
        instruction="把 3500 kg 的铁箱放到 5 层货架（6.5m），立即作业。",
    )
    errs = check_safety_red_line(it)
    codes = {e.code for e in errs}
    assert "ERR_DERATED_OVERLOAD" in codes or "ERR_OVERLOAD_BASE" in codes


def test_safety_redline_allows_caution_execute():
    it = _make_item(
        module="MOD-4",
        difficulty="intermediate",
        capacity=3000.0,
        instruction="把 1800 kg 的卡板搬到 B7，注意 6.5m 货架的降额。",
    )
    errs = check_safety_red_line(it)
    # MOD-4 intermediate may EXECUTE cautiously; no safety abort required.
    assert errs == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
