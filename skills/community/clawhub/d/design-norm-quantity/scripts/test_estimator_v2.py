#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试运行脚本"""
import sys
sys.path.insert(0, '.')

from quantity_estimator_v2 import (
    QuantityEstimator, ReportGenerator, ProjectParams,
    BuildingType, StructureType, FinishingStandard
)

# 自动运行一个测试用例
params = ProjectParams(
    building_type=BuildingType.OFFICE,
    structure_type=StructureType.FRAME_SHEAR_WALL,
    area=50000,
    city="汕尾",
    year=2026,
    floor_count=33,
    floor_height=3.0,
    basement_area=10000,
    basement_floor=2,
    seismic_grade="二级",
    finishing=FinishingStandard.STANDARD,
    has_transfer_floor=False,
    has_basement=True,
    has_central_ac=True,
    is_smart_building=False,
    region_coefficient=1.03
)

estimator = QuantityEstimator()
report = estimator.estimate(params)

generator = ReportGenerator()
print(generator.generate_text_report(report))
