# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from uncertainty_estimator import quick_estimate

# 一行代码快速估算
result = quick_estimate(
    building_type="办公",
    total_area=50000,
    floor_count=31,
    region="苏州"
)

# 直接输出用户需要的值到文件
with open('output.txt', 'w', encoding='utf-8') as f:
    cost_data = result["造价估算"]["总造价区间"]
    f.write(f"苏州31层办公楼 (50,000m2) 造价估算结果:\n")
    f.write(f"总造价中值: {cost_data['中值']}\n")
    f.write(f"总造价区间: {cost_data['低限']} ~ {cost_data['高限']}\n")

