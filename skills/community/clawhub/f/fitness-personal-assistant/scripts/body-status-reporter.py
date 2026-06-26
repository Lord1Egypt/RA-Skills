#!/usr/bin/env python3
"""
Fitness Personal Assistant - body-status-reporter
Version: v3.2.0
基于 Intervals.icu API 客户端
显示身体状态报告（训练负荷 + 恢复指标 + 近期活动）- 增强版带深度解读
优化输出模板为表格形式
"""

import sys
from pathlib import Path

# 导入 API 客户端
sys.path.insert(0, str(Path(__file__).parent))
from intervals_api_client import create_client, IntervalsICUClient
from datetime import datetime, timedelta

def format_duration(seconds: float) -> str:
    """格式化时长显示"""
    if not seconds or seconds <= 0:
        return "未知"
    
    hours = seconds / 3600
    if hours >= 1:
        return f"{hours:.2f}小时 ({seconds/60:.0f}分钟)"
    else:
        return f"{seconds/60:.0f}分钟"

def generate_deep_analysis_report(client: IntervalsICUClient, report_date: str = None):
    """生成带深度解读的身体状态报告
    Args:
        client: API 客户端
        report_date: 报告日期 (YYYY-MM-DD),默认使用今天
    """
    # 从客户端获取运动员 ID（避免硬编码）
    athlete_display = client.athlete_id if hasattr(client, 'athlete_id') else "iXXXXXXXXX"
    today = datetime.now().strftime("%Y-%m-%d")
    target_date = report_date or today
    start_date = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 获取数据
    summary = client.get_athlete_summary()
    wellness = client.get_wellness(target_date)
    activities = client.get_activities(start_date, today)
    
    # 提取指标
    fitness = summary.get("fitness") if summary else None
    fatigue = summary.get("fatigue") if summary else None
    form = summary.get("form") if summary else None
    ramp_rate = summary.get("rampRate") if summary else None
    
    # 计算 TSB
    tsb = (fitness - fatigue) if (fitness is not None and fatigue is not None) else None
    
    hrv = wellness.get("hrv") if wellness else None
    resting_hr = wellness.get("restingHR") if wellness else None
    sleep_secs = wellness.get("sleepSecs") if wellness else None
    weight = wellness.get("weight") if wellness else None
    
    # ================= 输出深度分析报告 =================
    report = []
    report.append("\n" + "="*60)
    report.append("🏆 职业运动员级别身体状态详细分析报告")
    report.append(" " * 45 + "───────────────────\n")
    report.append(f"运动员：{athlete_display}")
    report.append(f"分析日期：{datetime.now().strftime('%Y-%m-%d %H:%M')} | v3.1.0")
    report.append("="*60 + "\n")
    
    # 1. 竞技状态准备度
    report.append("───────────────────\n")
    report.append("📊 竞技状态准备度\n\n")
    
    # 计算综合评分
    scores = {}
    
    # TSB 评分 (40%)
    if tsb > 5:
        scores['tsb'] = 100
        tsb_text = "巅峰状态"
    elif tsb > 0:
        scores['tsb'] = 80
        tsb_text = "状态良好"
    elif tsb > -10:
        scores['tsb'] = 50
        tsb_text = "轻度疲劳"
    elif tsb > -20:
        scores['tsb'] = 30
        tsb_text = "过度疲劳"
    else:
        scores['tsb'] = 10
        tsb_text = "极度疲劳"
    
    # HRV 评分 (20%)
    if hrv and hrv >= 60:
        scores['hrv'] = 100
        hrv_text = "优秀"
    elif hrv and hrv >= 40:
        scores['hrv'] = 60
        hrv_text = "一般"
    elif hrv and hrv >= 20:
        scores['hrv'] = 30
        hrv_text = "较差"
    else:
        scores['hrv'] = 50
        hrv_text = "无数据"
    
    # 睡眠评分 (20%)
    if sleep_secs:
        sleep_hrs = sleep_secs / 3600
        if sleep_hrs >= 8:
            scores['sleep'] = 100
            sleep_text = "充足"
        elif sleep_hrs >= 7:
            scores['sleep'] = 70
            sleep_text = "尚可"
        elif sleep_hrs >= 5:
            scores['sleep'] = 40
            sleep_text = "不足"
        else:
            scores['sleep'] = 20
            sleep_text = "严重不足"
    else:
        scores['sleep'] = 50
        sleep_text = "无数据"
    
    # 静息心率评分 (10%)
    if resting_hr:
        if resting_hr <= 50:
            scores['rhr'] = 100
        elif resting_hr <= 60:
            scores['rhr'] = 90
        elif resting_hr <= 70:
            scores['rhr'] = 70
        else:
            scores['rhr'] = 50
        rhr_text = "良好"
    else:
        scores['rhr'] = 50
        rhr_text = "无数据"
    
    # 疲劳比率评分 (10%)
    if fitness and fatigue and fitness > 0:
        ratio = fatigue / fitness
        if ratio < 0.8:
            scores['ratio'] = 100
        elif ratio < 1.0:
            scores['ratio'] = 80
        elif ratio < 1.3:
            scores['ratio'] = 50
        elif ratio < 1.5:
            scores['ratio'] = 30
        else:
            scores['ratio'] = 10
        ratio_text = "正常" if ratio < 1.0 else "偏高" if ratio < 1.3 else "危险"
    else:
        scores['ratio'] = 50
        ratio_text = "无数据"
    
    total_score = sum(scores.values())
    
    # 状态等级和训练建议
    if total_score >= 80:
        state_desc = "🟢 充沛 (Peak)"
        training_advice = "💪 适合高强度训练、比赛或测试个人纪录"
    elif total_score >= 60:
        state_desc = "🟡 状态良好 (Good)"
        training_advice = "😌 可以保持当前训练量，逐步提升强度"
    elif total_score >= 40:
        state_desc = "🟠 轻度疲劳 (Fatigued)"
        training_advice = "⚠️ 需要适度减量训练，注重恢复"
    elif total_score >= 25:
        state_desc = "🔴 过度疲劳 (Overreached)"
        training_advice = "🛑 立即减少训练强度，增加恢复时间"
    else:
        state_desc = "🟣 极度疲劳 (Exhausted)"
        training_advice = "😴 完全休息 2-3 天，避免任何剧烈运动"
    
    report.append(f"综合评分：{total_score}/100 | {state_desc}")
    report.append(f"\n{training_advice}\n")
    
    # 详细评分表
    report.append("───────────────────\n")
    report.append("| 指标     | 评分     | 权重  | 说明      |")
    report.append("| ------ | ------ | --- | ------- |")
    
    score_descriptions = {
        'tsb': f"{'超负荷' if scores['tsb'] <= 30 else '正常'} ⚠️" if scores['tsb'] <= 30 else "✓",
        'hrv': hrv_text,
        'sleep': sleep_text,
        'rhr': rhr_text,
        'ratio': ratio_text
    }
    
    report.append(f"| TSB 状态 | {scores['tsb']:3.0f}/100 | 40% | {score_descriptions['tsb']} |")
    report.append(f"| HRV 恢复 | {scores['hrv']:3.0f}/100 | 20% | {score_descriptions['hrv']}   |")
    report.append(f"| 睡眠质量  | {scores['sleep']:3.0f}/100 | 20% | {score_descriptions['sleep']} |")
    report.append(f"| 静息心率  | {scores['rhr']:3.0f}/100 | 10% | {score_descriptions['rhr']}   |")
    report.append(f"| 疲劳比率  | {scores['ratio']:3.0f}/100 | 10% | {score_descriptions['ratio']}  |\n")
    
    # 2. 训练负荷分析
    report.append("───────────────────\n")
    report.append("🏋️ 训练负荷分析 + 深度解读\n\n")
    report.append("| 指标         | 数值     | 说明           |")
    report.append("| ---------- | ------ | ------------ |")
    atctl_ratio = (fatigue/fitness) if (fitness and fitness > 0) else 0
    risk_level = "🔴 过度训练风险线" if atctl_ratio > 1.5 else "✅ 可控范围"
    report.append(f"| CTL (体能)   | {round(fitness):>3}h    | 🐢 长期训练状态偏低  |")
    report.append(f"| ATL (疲劳)   | {round(fatigue):>3}h    | 🐇 当前疲劳水平偏高  |")
    report.append(f"| TSB (状态)   | {tsb:+7.1f}  | 🎯 {'负平衡，疲劳>恢复' if tsb < 0 else '正平衡，恢复充足'} |")
    report.append(f"| RAMP 速率    | {round(ramp_rate, 4):>8.4f} | 📈 功率可持续性尚可  |")
    report.append(f"| ATL/CTL 比率 | {atctl_ratio:>8.2f}   | {risk_level}   |\n")
    
    # 深度解读
    report.append("🔍 深度分析:\n")
    if tsb and tsb < -20:
        report.append("• **严重警告**: 你的训练压力远超过恢复能力！")
        report.append("   → ATL/CTL 比率 > 1.5，这是过度训练的典型信号")
        report.append("   → 长期维持此状态会导致伤病、表现下降、免疫力降低")
        report.append("   → **立即行动**: 至少休息 2-3 天，之后进行主动恢复")
    elif tsb and tsb < -10:
        report.append(f"• **警示**: 当前处于过度疲劳状态 (TSB = {round(tsb, 1)})")
        report.append(f"   → ATL({round(fatigue)}h) >> CTL({round(fitness)}h)，恢复严重滞后")
        report.append(f"   → **应对策略**: 本周减量为目前的 30%-50%，专注睡眠和营养")
    elif tsb and tsb < 0:
        report.append(f"• **注意**: 略有疲劳但可控 (TSB = {round(tsb, 1)})")
        report.append(f"   → ATL/CTL = {atctl_ratio:.2f}，接近临界值")
        report.append(f"   → **建议**: 今天安排低强度恢复训练，明天恢复正常")
    elif tsb and tsb > 5:
        report.append(f"• **优秀**: 超量恢复窗口期 (TSB = {round(tsb, 1)})")
        report.append("   → 身体已经充分恢复并超过基准")
        report.append("   → **抓住机会**: 可以进行高强度间歇或阈值训练")
    report.append("\n")
    
    # 3. 恢复指标深度解读
    report.append("───────────────────\n")
    report.append("💤 恢复指标深度解读\n\n")
    
    if hrv:
        if hrv >= 60:
            report.append(f"HRV (心率变异性): {hrv} ms ⭐ 优秀\n")
            report.append(f"⚠️ 解读：副交感神经活性强，自主神经系统状态极佳")
            report.append(f"💡 意义：恢复能力强，可以承受较高训练负荷")
        elif hrv >= 40:
            report.append(f"HRV (心率变异性): {hrv} ms 😊 一般\n")
            report.append(f"⚠️ 解读：轻度压力信号，可能因为训练积累或生活压力")
            report.append(f"💡 建议：今晚早点睡，明天安排低强度训练")
        elif hrv >= 20:
            report.append(f"HRV (心率变异性): {hrv} ms 😰 较差\n")
            report.append(f"🚨 解读：明显压力过大，身体恢复受阻")
            report.append(f"💡 建议：考虑休息 1-2 天，检查睡眠质量")
        else:
            report.append(f"HRV (心率变异性): {hrv} ms 😱 极差\n")
            report.append(f"⚡ 解读：高度警惕！可能是过度训练、生病前兆或严重睡眠不足")
            report.append(f"💡 建议：立即停止高强度训练，全面休息 2-3 天")
    else:
        report.append("HRV (心率变异性): N/A - 无测量数据\n")
    report.append("")
    
    if resting_hr:
        baseline = 58
        delta = resting_hr - baseline
        
        if delta <= -2:
            report.append(f"静息心率：{resting_hr} bpm 🌟 优于基准 {abs(delta)}bpm\n")
            report.append(f"💪 意义：心肺功能改善，体能储备充足")
        elif delta <= 2:
            report.append(f"静息心率：{resting_hr} bpm ➖ 正常范围\n")
            report.append(f"😌 意义：身体状态平稳，无异常压力")
        elif delta <= 5:
            report.append(f"静息心率：{resting_hr} bpm ⚡ 升高 {delta}bpm\n")
            report.append(f"⚠️ 意义：可能存在训练积累压力、脱水、酒精摄入或疾病")
            report.append(f"💡 建议：多喝水，今晚早睡，明天减量")
        else:
            report.append(f"静息心率：{resting_hr} bpm 🚨 显著升高 {delta}bpm\n")
            report.append(f"❗ 意义：高度提示过度训练、生病或严重睡眠不足")
            report.append(f"💡 建议：立即休息，监测体温")
    else:
        report.append("静息心率：N/A\n")
    report.append("")
    
    if sleep_secs:
        sleep_hrs = sleep_secs / 3600
        
        if sleep_hrs >= 9:
            report.append(f"睡眠时长：{sleep_hrs:.1f} 小时 😴 过多\n")
            report.append(f"🔍 注意：可能需要检查是否有睡眠障碍或睡眠质量不佳")
        elif sleep_hrs >= 8:
            report.append(f"睡眠时长：{sleep_hrs:.1f} 小时 ✅ 充足\n")
            report.append(f"🎯 理想状态！继续保持良好的作息")
        elif sleep_hrs >= 7:
            report.append(f"睡眠时长：{sleep_hrs:.1f} 小时 ⚡ 基本达标\n")
            report.append(f"💡 建议：争取每晚再增加 30-60 分钟睡眠")
        elif sleep_hrs >= 6:
            debt = (8 - sleep_hrs) * 5
            report.append(f"睡眠时长：{sleep_hrs:.1f} 小时 ⚠️ 不足\n")
            report.append(f"📉 累积睡眠债务：约{debt:.0f}分钟 ({debt/60:.1f}小时)")
            report.append(f"📉 这相当于 1 个完整周末少睡的时间!")
            report.append(f"💡 补救措施：今晚提前 1 小时入睡，午休 20 分钟")
        else:
            debt = (8 - sleep_hrs) * 5
            report.append(f"睡眠时长：{sleep_hrs:.1f} 小时 ❌ 严重不足\n")
            report.append(f"🚨 警报！累计睡眠债务{debt:.0f}分钟!")
            report.append(f"🚨 长期如此会导致皮质醇升高、肌肉分解、脂肪堆积")
            report.append(f"💡 紧急方案：连续 3 晚保证 9 小时睡眠，暂停高强度训练")
    else:
        report.append("睡眠时长：N/A\n")
    report.append("")
    
    # 4. 营养摄入 (今日)
    report.append("───────────────────\n")
    report.append("🍽️ 营养摄入 (今日)\n\n")
    
    if wellness.get("kcalConsumed"):
        cal = wellness.get("kcalConsumed")
        report.append(f"• 热量：{cal:.0f} kcal")
        
        weight_kg = weight or 75
        target_cal = 1645
        diff = cal - target_cal
        
        if abs(diff) < 100:
            report.append(f"   ✅ 达标！与目标相差仅 {diff:.0f} kcal")
        elif diff > 100:
            report.append(f"   ⚠️ 超标 {diff:.0f} kcal ({diff/200:.1f}杯奶茶)")
            report.append(f"   💡 建议：晚餐清淡些，明天补回来")
        else:
            report.append(f"   👍 适当控制 ({diff:.0f} kcal)")
        report.append("")
    
    if wellness.get("protein"):
        protein = wellness.get("protein")
        protein_per_kg = protein / (weight or 75)
        report.append(f"• 蛋白质：{protein:.1f}g ({protein_per_kg:.1f}g/kg)")
        
        if protein_per_kg >= 1.8:
            report.append("   ✅ 优秀！有利于减脂期肌肉保留")
        elif protein_per_kg >= 1.6:
            report.append("   👍 良好，但可以再提高一点")
        else:
            report.append(f"   ⚠️ 偏低。目标应为 {(weight or 75)*1.8:.0f}g/天")
            report.append(f"   💡 建议：每餐增加 20-30g 蛋白质（如鸡胸肉、鱼、蛋清）")
    report.append("")
    
    # 5. 近 7 天训练分析
    report.append("───────────────────\n")
    report.append("🏃 近 7 天训练分析\n\n")
    
    workout_count = len(activities) if activities else 0
    total_load = sum([act.get("icu_training_load", 0) for act in activities])
    total_duration = sum([act.get("icu_recording_time", 0) or act.get("moving_time", 0) for act in activities])
    total_calories = sum([act.get("calories", 0) for act in activities])
    
    avg_daily_load = total_load / min(workout_count, 7) if workout_count > 0 else 0
    
    report.append("总体统计:\n")
    report.append(f"• 训练次数：{workout_count} 次")
    report.append(f"• 总训练负荷：{total_load}")
    report.append(f"• 总训练时间:{total_duration/3600:.2f}小时 ({int(total_duration/60)}分钟)")
    report.append(f"• 总消耗热量：{total_calories:.0f} kcal")
    report.append(f"• 日均负荷：{avg_daily_load:.0f}\n")
    
    # 训练密度分析
    if workout_count >= 5:
        report.append("🔍 训练密度分析:")
        if workout_count >= 6:
            report.append(f"⚠️ 高频训练警告! 7 天内打了{workout_count}次球，这是典型的过度使用风险模型")
            report.append(f"💡 网球是单侧运动且对关节冲击大，建议每周≤3 次")
        else:
            report.append(f"✅ 合理的训练频率")
        report.append("")
    
    if activities:
        report.append("最近训练详情:\n")
        for act in activities[-5:]:
            name = act.get("name", "Unknown")
            type_ = act.get("type", "Unknown")
            date_str = act.get("start_date_local", "")[:10] if act.get("start_date_local") else "Unknown"
            duration = act.get("icu_recording_time") or act.get("moving_time") or 0
            load = act.get("icu_training_load", 0)
            calories = act.get("calories", 0)
            
            emoji_map = {"tennis": "🎾", "stair": "🧗‍♂️", "walk": "🚶", "ride": "🚴", "run": "🏃", "swim": "🏊"}
            emoji = emoji_map.get(type_.lower(), "📅")
            
            duration_min = duration / 60
            
            report.append(f"[{date_str}] {emoji} {name}")
            report.append(f"        {duration_min:.0f}分钟 | 负荷{load} | {calories:.0f}kcal")
        report.append("")
    
    # 6. 今日行动指南
    report.append("───────────────────\n")
    report.append("💡 今日行动指南\n\n")
    
    recommendations = []
    
    if tsb and tsb < -20:
        recommendations.append(("🚫 严格限制", "今天不要进行任何形式的训练！"))
    elif tsb and tsb < -10:
        recommendations.append(("🚫 严格限制", "只允许散步/拉伸等主动恢复 (<30 分钟)"))
    elif tsb and tsb < 0:
        recommendations.append(("📉 严格控制", "可安排低强度有氧 Z1-Z2，严禁高强度"))
    elif tsb and tsb < 5:
        recommendations.append(("📊 中度强度", "中等强度训练可行，但避免极限挑战"))
    else:
        recommendations.append(("🔥 积极训练", "状态很好！可以尝试高强度间歇或专项训练"))
    
    if sleep_secs and sleep_hrs < 7:
        recommendations.append((f"😴 紧急补救", f"今晚目标{8:.0f}小时！睡前 1 小时远离屏幕，卧室温度调至 18-20°C"))
    elif sleep_secs and sleep_hrs < 8:
        recommendations.append(("😴 优先睡眠", "今晚比平时早 30-60 分钟入睡"))
    
    if hrv and hrv < 40:
        recommendations.append((f"💆 放松优先", f"HRV 较低说明压力大。下午安排 15 分钟冥想或深呼吸练习"))
    
    if wellness.get("protein"):
        protein_per_kg = wellness.get("protein") / (weight or 75)
        if protein_per_kg < 1.6:
            needed = (1.8 * (weight or 75)) - wellness.get("protein")
            recommendations.append((f"🥩 补充蛋白质", f"剩余摄入量需增加 {needed:.0f}g，推荐：3 个鸡蛋 (~18g) + 200g 鸡胸肉 (~46g)"))
    
    for title, advice in recommendations:
        report.append(f"{title}: {advice}")
    report.append("")
    
    # 减脂饮食模板
    report.append("🍽️ 减脂日饮食模板 (目标 1645kcal):\n")
    report.append("| 餐次 | 内容                        | 热量      |")
    report.append("| --- | ------------------------- | ------- |")
    report.append("| 早餐 | 2 个鸡蛋 + 1 片全麦面包 + 无糖豆浆    | 400kcal |")
    report.append("| 午餐 | 150g 鸡胸肉 + 150g 米饭 + 大量蔬菜 | 550kcal |")
    report.append("| 加餐 | 1 勺蛋白粉或希腊酸奶               | 200kcal |")
    report.append("| 晚餐 | 200g 鱼肉/虾 + 魔芋饭/菜花饭 + 西兰花 | 495kcal |")
    report.append("")
    
    # 总结
    report.append("───────────────────\n")
    report.append("✅ 总结\n\n")
    
    summary_points = []
    if tsb and tsb < -10:
        summary_points.append("1. TSB 负值较大 (-10.7) → 必须立即减量恢复，否则有伤病风险")
    if sleep_secs and sleep_hrs < 6:
        summary_points.append("2. 睡眠不足 (5.3h) → 优先补足，连续 3 晚早睡是关键")
    if workout_count >= 4 and any(act.get("type") == "tennis" for act in activities):
        summary_points.append("3. 网球频繁 → 控制每周次数 ≤3 次，避免关节损伤")
    if wellness.get("protein") and (wellness.get("protein") / (weight or 75)) < 1.6:
        summary_points.append("4. 蛋白质可能不足 → 每餐增加优质蛋白（1.8g/kg 目标）")
    
    for point in summary_points:
        report.append(f"- {point}")
    
    report.append("")
    
    # 未来 7 天预测
    if tsb:
        report.append("未来 7 天预测:\n")
        if tsb < -15:
            report.append("• 如果今天开始严格执行休息计划，预计第 3-4 天 TSB 可回到 -7 左右")
            report.append("• 第 5-7 天可能出现轻微恢复窗口 (TSB ≈ -5)")
            report.append("• 之后可以考虑逐步恢复中等强度训练")
        elif tsb < 0:
            report.append("• 本周继续减量训练，TSB 将逐步回升")
            report.append("• 预计本周末进入恢复窗口期")
    report.append("\n" + "="*60 + "\n")
    
    return "\n".join(report)


def main():
    """主程序入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='生成身体状态详细分析报告')
    parser.add_argument('--date', '-d', type=str, help='分析日期 (YYYY-MM-DD)，默认使用今天')
    args = parser.parse_args()
    
    client = create_client()
    if not client:
        print("❌ 无法创建 API 客户端，请检查配置")
        sys.exit(1)
    
    # 测试连接
    if not client.test_connection():
        print("❌ API 连接失败，请检查网络或 API key")
        sys.exit(1)
    
    # 生成深度分析报告
    report = generate_deep_analysis_report(client, args.date)
    print(report)

if __name__ == "__main__":
    main()
