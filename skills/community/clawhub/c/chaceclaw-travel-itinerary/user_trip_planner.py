#!/usr/bin/env python3
"""
为用户规划泰国普吉岛7日家庭度假
"""

import sys
sys.path.append('/Users/tom/.openclaw/workspace/skills/travel-itinerary-planner')

from travel_planner import TravelItineraryPlanner

def main():
    # 创建规划器
    planner = TravelItineraryPlanner()

    # 用户输入
    user_input = "我想去泰国普吉岛度假，7天，预算15000元，家庭旅行（带小孩），喜欢海滩和美食，中档旅行风格"

    print("🔍 收集旅行信息...")
    travel_info = planner.collect_travel_info(user_input)
    print(f"✅ 目的地: {travel_info.destination}")
    print(f"✅ 天数: {travel_info.days}")
    print(f"✅ 预算: ¥{travel_info.budget_total}")
    print(f"✅ 旅行者: {travel_info.travelers}")
    print(f"✅ 兴趣: {', '.join(travel_info.interests)}")
    print(f"✅ 风格: {travel_info.style}")
    print()

    # 创建行程
    print("📝 创建行程...")
    itinerary = planner.create_itinerary(travel_info)
    print("✅ 行程创建完成")
    print()

    # 格式化输出
    print("📋 行程详情:")
    print("=" * 80)
    formatted_itinerary = planner.format_itinerary(itinerary)
    print(formatted_itinerary)
    print("=" * 80)

    # 保存行程
    print("💾 保存行程...")
    filepath = planner.save_itinerary(itinerary)
    print(f"✅ 行程已保存到: {filepath}")

    # 针对家庭旅行的特别建议
    print("\n👨‍👩‍👧‍👦 家庭旅行特别建议:")
    print("- [ ] 准备儿童防晒用品和泳衣")
    print("- [ ] 携带常用药品（退烧药、创可贴、防蚊液）")
    print("- [ ] 下载儿童友好的离线娱乐内容")
    print("- [ ] 选择有儿童设施的酒店")
    print("- [ ] 预订家庭房或连通房")
    print("- [ ] 准备轻便的推车（如果需要）")
    print("- [ ] 了解当地儿童医院位置")
    print("- [ ] 准备零食和水，避免孩子饿肚子")

if __name__ == "__main__":
    main()
