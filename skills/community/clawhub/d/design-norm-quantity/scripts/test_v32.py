# -*- coding: utf-8 -*-
"""Test script for v3.2"""
import sys
sys.path.insert(0, 'scripts')

from uncertainty_estimator import (
    UncertaintyEstimator, 
    ProjectParams, 
    BuildingType, 
    StructureType, 
    Region,
    INTERNATIONAL_QS_AVAILABLE
)

print("=" * 60)
print("DLHZ Uncertainty Estimator v3.2 Test")
print("=" * 60)

# Test main estimator
estimator = UncertaintyEstimator()
params = ProjectParams(
    building_type=BuildingType.OFFICE,
    structure_type=StructureType.FRAME_SHEAR_WALL,
    total_area=50000,
    floor_count=33,
    basement_area=10000,
    basement_floors=2,
    decoration_level="standard",
    has_central_ac=True,
    has_pile=True,
    seismic_level="7度",
    region=Region.FOSHAN,
    year=2026
)

result = estimator.estimate(params, enable_monte_carlo=True, use_database_calibration=False)

print("\n[Cost Estimate]")
cost = result["造价估算"]
print(f"  Unit Cost: {cost['单方造价区间']['低限']} ~ {cost['单方造价区间']['高限']}")
print(f"  Total Cost: {cost['总造价区间']['低限']} ~ {cost['总造价区间']['高限']}")

print(f"\n[International QS Available: {INTERNATIONAL_QS_AVAILABLE}]")

if INTERNATIONAL_QS_AVAILABLE:
    from international_qs_methods import quick_qs_estimate
    qs = quick_qs_estimate(
        total_area=50000,
        building_type="办公",
        structure_type="框架-核心筒",
        city="深圳",
        floor_count=30,
        quality_level="high"
    )
    
    print("\n[International QS Methods]")
    print(f"  Arcadis: {qs['method_estimates']['arcadis']['unit_cost']:,.0f} CNY/m2")
    print(f"  RLB: {qs['method_estimates']['rlb']['unit_cost']:,.0f} CNY/m2")
    print(f"  Davis Langdon: {qs['method_estimates']['davis_langdon']['unit_cost']:,.0f} CNY/m2")
    print(f"  Fused: {qs['fused_estimate']['unit_cost']:,.0f} CNY/m2")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
