#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
best_time.py - 最佳发布时间推荐器
基于平台算法和用户活跃数据，推荐最佳发布时间
"""

import json
import argparse
import logging
from datetime import datetime, timedelta
import random

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BestTime')

class BestTimeRecommender:
    """最佳发布时间推荐器"""
    
    # 平台活跃时间段（模拟数据）
    PLATFORM_PEAK_HOURS = {
        "douyin": {
            "18-24": [18, 19, 20, 21, 22],  # 晚上18-22点
            "25-34": [12, 13, 18, 19, 20, 21],
            "35+": [7, 8, 12, 13, 18, 19]
        },
        "xiaohongshu": {
            "18-24": [9, 10, 11, 12, 18, 19, 20, 21, 22],
            "25-34": [8, 9, 10, 12, 13, 18, 19, 20, 21],
            "35+": [7, 8, 9, 10, 12, 13, 18, 19]
        },
        "bilibili": {
            "18-24": [12, 13, 18, 19, 20, 21, 22, 23],
            "25-34": [12, 13, 18, 19, 20, 21, 22],
            "35+": [12, 13, 18, 19, 20]
        },
        "youtube": {
            "18-24": [15, 16, 17, 18, 19, 20, 21],
            "25-34": [12, 13, 18, 19, 20, 21],
            "35+": [8, 9, 12, 13, 18, 19]
        }
    }
    
    def __init__(self, data_path="scripts/audience_data.json"):
        """初始化推荐器"""
        self.audience_data = self.load_audience_data(data_path)
    
    def load_audience_data(self, data_path):
        """加载受众数据（模拟）"""
        # 实际应该从平台API或数据库加载
        # 这里返回模拟数据
        return {
            "douyin": {
                "main_age_group": "18-24",
                "active_hours": [18, 19, 20, 21, 22]
            },
            "xiaohongshu": {
                "main_age_group": "25-34",
                "active_hours": [9, 10, 12, 13, 18, 19, 20, 21]
            }
        }
    
    def recommend(self, platform, target_audience="18-24", content_type="video"):
        """
        推荐最佳发布时间
        
        Args:
            platform: 平台名称
            target_audience: 目标受众年龄段 (18-24/25-34/35+)
            content_type: 内容类型 (video/image/article)
        
        Returns:
            dict: 推荐时间信息
        """
        if platform not in self.PLATFORM_PEAK_HOURS:
            logger.warning(f"⚠️ 平台 {platform} 无数据，使用默认推荐")
            return self.get_default_time(platform)
        
        # 获取平台活跃时间段
        peak_hours = self.PLATFORM_PEAK_HOURS[platform].get(target_audience, [18, 19, 20, 21])
        
        # 根据内容类型微调
        if content_type == "video":
            # 视频内容推荐在晚上
            preferred_hours = [h for h in peak_hours if h >= 18]
            if not preferred_hours:
                preferred_hours = peak_hours
        elif content_type == "image":
            # 图文内容推荐在白天
            preferred_hours = [h for h in peak_hours if 8 <= h <= 20]
            if not preferred_hours:
                preferred_hours = peak_hours
        else:
            preferred_hours = peak_hours
        
        # 随机选择最佳小时（实际应该基于历史数据预测）
        best_hour = random.choice(preferred_hours)
        
        # 生成推荐时间（今天或明天）
        now = datetime.now()
        today_best = now.replace(hour=best_hour, minute=0, second=0, microsecond=0)
        
        if now > today_best:
            # 今天已过最佳时间，推荐明天
            best_time = today_best + timedelta(days=1)
        else:
            best_time = today_best
        
        # 生成推荐理由
        reason = self.generate_reason(platform, target_audience, best_hour, content_type)
        
        return {
            "platform": platform,
            "target_audience": target_audience,
            "content_type": content_type,
            "best_time": best_time.strftime("%Y-%m-%d %H:%M"),
            "best_hour": best_hour,
            "reason": reason,
            "alternative_times": self.get_alternative_times(platform, target_audience, best_hour)
        }
    
    def generate_reason(self, platform, target_audience, hour, content_type):
        """生成推荐理由"""
        reasons = []
        
        # 平台角度
        if platform == "douyin":
            reasons.append("抖音算法在此时段推荐权重较高")
        elif platform == "xiaohongshu":
            reasons.append("小红书用户此时段活跃度高")
        elif platform == "bilibili":
            reasons.append("B站此时段流量高峰")
        elif platform == "youtube":
            reasons.append("YouTube全球用户此时段在线")
        
        # 受众角度
        if target_audience == "18-24":
            reasons.append("18-24岁用户此时段最活跃")
        elif target_audience == "25-34":
            reasons.append("25-34岁用户此时段有空闲时间")
        elif target_audience == "35+":
            reasons.append("35+岁用户此时段习惯浏览")
        
        # 内容角度
        if content_type == "video":
            reasons.append("视频内容在此时段完播率更高")
        elif content_type == "image":
            reasons.append("图文内容在此时段点击率更高")
        
        # 时间角度
        if 18 <= hour <= 21:
            reasons.append("晚间黄金时段，用户休闲时间充足")
        elif 12 <= hour <= 13:
            reasons.append("午休时间，用户有碎片化浏览习惯")
        elif 7 <= hour <= 9:
            reasons.append("早间通勤时间，用户习惯刷内容")
        
        return "；".join(reasons)
    
    def get_alternative_times(self, platform, target_audience, best_hour):
        """获取备选时间"""
        peak_hours = self.PLATFORM_PEAK_HOURS[platform].get(target_audience, [18, 19, 20, 21])
        
        # 选择除最佳时间外的其他活跃时段
        alternatives = [h for h in peak_hours if h != best_hour]
        
        # 返回前3个备选（今天或明天）
        now = datetime.now()
        result = []
        
        for hour in alternatives[:3]:
            alt_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if now > alt_time:
                alt_time += timedelta(days=1)
            result.append(alt_time.strftime("%Y-%m-%d %H:%M"))
        
        return result
    
    def get_default_time(self, platform):
        """获取默认推荐时间"""
        now = datetime.now()
        default_time = now.replace(hour=18, minute=0, second=0, microsecond=0)
        
        if now > default_time:
            default_time += timedelta(days=1)
        
        return {
            "platform": platform,
            "target_audience": "unknown",
            "content_type": "video",
            "best_time": default_time.strftime("%Y-%m-%d %H:%M"),
            "best_hour": 18,
            "reason": "默认推荐：晚间18:00（通用黄金时段）",
            "alternative_times": []
        }
    
    def analyze_history(self, platform, history_data):
        """
        基于历史数据优化推荐（高级功能）
        
        Args:
            platform: 平台名称
            history_data: 历史发布数据 [{"time": "...", "views": 1000, ...}]
        
        Returns:
            dict: 优化后的推荐
        """
        # 分析历史数据中表现最好的发布时间
        if not history_data:
            return self.get_default_time(platform)
        
        # 按小时统计平均表现
        hour_performance = {}
        for item in history_data:
            hour = datetime.fromisoformat(item["time"]).hour
            if hour not in hour_performance:
                hour_performance[hour] = {"total_views": 0, "count": 0}
            
            hour_performance[hour]["total_views"] += item.get("views", 0)
            hour_performance[hour]["count"] += 1
        
        # 计算平均表现
        for hour in hour_performance:
            count = hour_performance[hour]["count"]
            if count > 0:
                hour_performance[hour]["avg_views"] = hour_performance[hour]["total_views"] / count
        
        # 找到表现最好的小时
        best_hour = max(hour_performance.keys(), key=lambda h: hour_performance[h].get("avg_views", 0))
        
        now = datetime.now()
        best_time = now.replace(hour=best_hour, minute=0, second=0, microsecond=0)
        
        if now > best_time:
            best_time += timedelta(days=1)
        
        return {
            "platform": platform,
            "best_time": best_time.strftime("%Y-%m-%d %H:%M"),
            "best_hour": best_hour,
            "reason": f"基于历史数据优化：{best_hour}:00 平均浏览量最高（{hour_performance[best_hour]['avg_views']:.0f}）",
            "hour_performance": hour_performance
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='最佳发布时间推荐器')
    parser.add_argument('--platform', required=True, 
                        choices=['douyin', 'xiaohongshu', 'bilibili', 'youtube'],
                        help='平台名称')
    parser.add_argument('--audience', default='18-24',
                        choices=['18-24', '25-34', '35+'],
                        help='目标受众年龄段')
    parser.add_argument('--type', default='video',
                        choices=['video', 'image', 'article'],
                        help='内容类型')
    parser.add_argument('--json', action='store_true',
                        help='以JSON格式输出')
    
    args = parser.parse_args()
    
    # 初始化推荐器
    recommender = BestTimeRecommender()
    
    # 获取推荐
    recommendation = recommender.recommend(
        platform=args.platform,
        target_audience=args.audience,
        content_type=args.type
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(recommendation, indent=2, ensure_ascii=False))
    else:
        print("\n" + "="*60)
        print("📅 最佳发布时间推荐")
        print("="*60)
        print(f"平台: {recommendation['platform']}")
        print(f"目标受众: {recommendation['target_audience']}")
        print(f"内容类型: {recommendation['content_type']}")
        print(f"\n🎯 最佳发布时间: {recommendation['best_time']}")
        print(f"\n📝 推荐理由:")
        for reason in recommendation['reason'].split('；'):
            print(f"   - {reason}")
        
        if recommendation.get('alternative_times'):
            print(f"\n🔄 备选时间:")
            for i, alt_time in enumerate(recommendation['alternative_times'], 1):
                print(f"   {i}. {alt_time}")
        
        print("="*60)
    
    return 0

if __name__ == '__main__':
    exit(main())
