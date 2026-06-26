# -*- coding: utf-8 -*-
"""Test script for Data Calibrator"""

import sys
sys.path.insert(0, 'scripts')

from data_calibrator import quick_calibrate, get_verified_data, get_city_info

print("=" * 60)
print("DLHZ Data Calibrator v1.0 - Suzhou 18F Test")
print("=" * 60)

# Test calibration
result = quick_calibrate(
    city='苏州',
    building_type='住宅',
    structure_type='框架-剪力墙',
    total_area=25000,
    floor_count=18,
    original_unit_price=5000,
    original_steel=45,
    original_concrete=0.35
)

print("Accuracy Level: " + result.accuracy_level)
print("Unit Price: {0:,.0f} ~ {1:,.0f} CNY/m2".format(result.unit_price_low, result.unit_price_high))
print("Total Cost: {0:,.0f} ~ {1:,.0f} 10k CNY".format(result.total_cost_low/10000, result.total_cost_high/10000))
print("Data Sources: " + str(result.data_sources))

print("")
print("City Factors:")
for city in ["深圳", "广州", "苏州", "汕尾"]:
    info = get_city_info(city)
    if info:
        print("  {0}: BuildFactor={1}, Date={2}".format(city, info['build_factor'], info['data_date']))

print("")
print("Database Records:")
data = get_verified_data("深圳", "住宅", "框架-剪力墙")
if data:
    for d in data:
        print("  {0} {1} {2}: {3:,.0f} ~ {4:,.0f} CNY/m2".format(d.city, d.building_type, d.structure_type, d.unit_price_low, d.unit_price_high))

print("")
print("=" * 60)
print("Test Complete!")
print("=" * 60)
