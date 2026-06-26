#!/usr/bin/env python3
"""
完整的旅行规划系统演示 - 集成所有扩展功能
"""

import sys
sys.path.append('/Users/tom/.openclaw/workspace/skills/travel-itinerary-planner')

from travel_planner import TravelItineraryPlanner
from travel_planner_extensions import TravelPlannerExtensions

def main():
    print("🌟 完整的旅行规划系统演示")
    print("=" * 80)

    # 创建主规划器
    planner = TravelItineraryPlanner()

    # 创建扩展功能
    extensions = TravelPlannerExtensions()

    # 用户输入
    user_input = "我想去泰国普吉岛度假，7天，预算15000元，家庭旅行（带小孩），喜欢海滩和美食，中档旅行风格"

    print(f"\n📍 用户需求: {user_input}")
    print("=" * 80)

    # 1. 收集旅行信息
    print("\n🔍 步骤 1: 收集旅行信息")
    print("-" * 80)
    travel_info = planner.collect_travel_info(user_input)
    print(f"✅ 目的地: {travel_info.destination}")
    print(f"✅ 天数: {travel_info.days}")
    print(f"✅ 预算: ¥{travel_info.budget_total}")
    print(f"✅ 旅行者: {travel_info.travelers}")
    print(f"✅ 兴趣: {', '.join(travel_info.interests)}")
    print(f"✅ 风格: {travel_info.style}")

    # 2. 创建行程
    print("\n📝 步骤 2: 创建行程")
    print("-" * 80)
    itinerary = planner.create_itinerary(travel_info)
    print("✅ 行程创建完成")

    # 3. 天气预报
    print("\n🌤️ 步骤 3: 天气预报")
    print("-" * 80)
    weather_data = extensions.get_weather_forecast(travel_info.destination, travel_info.days)
    print(extensions.format_weather_forecast(weather_data))

    # 4. 预订链接
    print("\n🔗 步骤 4: 预订链接")
    print("-" * 80)
    booking_links = extensions.get_booking_links(travel_info.destination)
    print(extensions.format_booking_links(booking_links))

    # 5. 儿童友好活动
    print("\n👨‍👩‍👧‍👦 步骤 5: 儿童友好活动")
    print("-" * 80)
    kid_friendly = extensions.filter_kid_friendly_activities(travel_info.destination)
    print(extensions.format_kid_friendly_activities(kid_friendly))

    # 6. 紧急联系信息
    print("\n🚨 步骤 6: 紧急联系信息")
    print("-" * 80)
    emergency_contacts = extensions.get_emergency_contacts(travel_info.destination)
    print(extensions.format_emergency_contacts(emergency_contacts))

    # 7. 行程分享
    print("\n📤 步骤 7: 行程分享")
    print("-" * 80)
    share_link = extensions.generate_shareable_link(itinerary)
    print(f"🔗 分享链接: {share_link}")

    pdf_content = extensions.generate_pdf_content(itinerary)
    pdf_file = extensions.save_pdf_content(pdf_content)
    print(f"📄 PDF内容已保存: {pdf_file}")

    # 8. 费用追踪
    print("\n💰 步骤 8: 费用追踪")
    print("-" * 80)
    expense_tracker_file = extensions.create_expense_tracker(itinerary)
    print(f"✅ 费用追踪器已创建: {expense_tracker_file}")

    # 9. 照片整理
    print("\n📸 步骤 9: 照片整理建议")
    print("-" * 80)
    photo_tips = extensions.get_photo_organization_tips(travel_info.destination)
    print(extensions.format_photo_organization_tips(photo_tips))

    # 10. 旅行日记
    print("\n📝 步骤 10: 旅行日记模板")
    print("-" * 80)
    diary_template = extensions.generate_travel_diary_template(itinerary)
    diary_file = extensions.save_diary_template(diary_template)
    print(f"✅ 旅行日记模板已创建: {diary_file}")

    # 11. 保存完整行程
    print("\n💾 步骤 11: 保存完整行程")
    print("-" * 80)
    itinerary_file = planner.save_itinerary(itinerary)
    print(f"✅ 完整行程已保存: {itinerary_file}")

    # 12. 格式化输出
    print("\n📋 步骤 12: 格式化输出")
    print("-" * 80)
    formatted_itinerary = planner.format_itinerary(itinerary)
    print(formatted_itinerary)

    print("\n" + "=" * 80)
    print("🎉 完整的旅行规划系统演示完成！")
    print("=" * 80)

    print("\n📊 系统功能总结:")
    print("✅ 智能信息收集")
    print("✅ 详细行程规划")
    print("✅ 实时天气预报")
    print("✅ 预订链接集成")
    print("✅ 儿童友好活动")
    print("✅ 紧急联系信息")
    print("✅ 行程分享功能")
    print("✅ 费用追踪系统")
    print("✅ 照片整理建议")
    print("✅ 旅行日记模板")
    print("✅ 预算管理")
    print("✅ 实用建议生成")

    print("\n🎯 所有功能已就绪，可以开始规划你的完美旅行！")


if __name__ == "__main__":
    main()
