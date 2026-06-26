#!/usr/bin/env python3
"""
机票全网比价脚本
通过浏览器自动化访问飞猪、携程、去哪儿等平台，查询航班价格并对比

Usage:
    python search_flights.py --from 北京 --to 上海 --date 2026-03-20
    python search_flights.py --from 北京 --to 三亚 --date 2026-03-20 --return-date 2026-03-25
    python search_flights.py --from 广州 --to 成都 --date 明天 --platforms 携程，飞猪
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

# 依赖检查
try:
    from openclaw import browser
except ImportError:
    print("❌ 需要 OpenClaw 环境")
    print("请确保在 OpenClaw 中运行此脚本")
    sys.exit(1)


class FlightPriceComparator:
    """机票全网比价器"""
    
    # 平台配置
    PLATFORMS = {
        "fliggy": {
            "name": "飞猪",
            "url": "https://www.fliggy.com/",
            "search_url": "https://www.fliggy.com/flights",
            "emoji": "🐷"
        },
        "ctrip": {
            "name": "携程",
            "url": "https://www.ctrip.com/",
            "search_url": "https://flights.ctrip.com/",
            "emoji": "🐬"
        }
    }
    
    def __init__(self, platforms: Optional[List[str]] = None):
        """
        初始化比价器
        
        Args:
            platforms: 指定要对比的平台，None 表示全部
        """
        self.platforms = platforms or list(self.PLATFORMS.keys())
        self.results = {}
        self.browser_profile = "openclaw"
        
    def parse_date(self, date_str: str) -> str:
        """
        解析日期字符串
        
        Args:
            date_str: 日期字符串，支持多种格式
            
        Returns:
            标准化日期格式 YYYY-MM-DD
        """
        today = datetime.now()
        
        # 处理特殊关键词
        if date_str in ["今天", "今日"]:
            return today.strftime("%Y-%m-%d")
        elif date_str in ["明天", "明日"]:
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_str in ["后天"]:
            return (today + timedelta(days=2)).strftime("%Y-%m-%d")
        elif "周" in date_str or "星期" in date_str:
            # 处理"下周一"、"这周五"等
            return self._parse_weekday(date_str, today)
        elif "月" in date_str:
            # 处理"3 月 20 日"、"03-20"等
            return self._parse_month_day(date_str, today.year)
        else:
            # 尝试直接解析 YYYY-MM-DD
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except:
                pass
        
        # 默认返回今天
        return today.strftime("%Y-%m-%d")
    
    def _parse_weekday(self, date_str: str, today: datetime) -> str:
        """解析星期几"""
        weekdays = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}
        
        # 提取星期几
        match = re.search(r'周 ([一二三四五六日天])', date_str)
        if not match:
            return today.strftime("%Y-%m-%d")
        
        target_weekday = weekdays[match.group(1)]
        current_weekday = today.weekday()
        
        # 计算目标日期
        if "下" in date_str:
            days_ahead = 7 + (target_weekday - current_weekday)
        elif "这" in date_str:
            days_ahead = (target_weekday - current_weekday) % 7
        else:
            days_ahead = (target_weekday - current_weekday) % 7
            if days_ahead == 0:
                days_ahead = 7
        
        return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    
    def _parse_month_day(self, date_str: str, year: int) -> str:
        """解析月日"""
        # 处理"3 月 20 日"格式
        match = re.search(r'(\d{1,2}) 月 (\d{1,2}) 日？', date_str)
        if match:
            month, day = int(match.group(1)), int(match.group(2))
            return f"{year}-{month:02d}-{day:02d}"
        
        # 处理"03-20"格式
        match = re.search(r'(\d{1,2})-(\d{1,2})', date_str)
        if match:
            month, day = int(match.group(1)), int(match.group(2))
            return f"{year}-{month:02d}-{day:02d}"
        
        return datetime.now().strftime("%Y-%m-%d")
    
    def search_fliggy(self, from_city: str, to_city: str, date: str, 
                     return_date: Optional[str] = None) -> Dict:
        """
        搜索飞猪航班
        
        Returns:
            航班信息字典
        """
        print(f"\n🐷 正在搜索飞猪：{from_city} → {to_city} ({date})")
        
        try:
            # 打开飞猪航班搜索页
            browser.action = "open"
            browser.profile = self.browser_profile
            browser.url = self.PLATFORMS["fliggy"]["search_url"]
            browser()
            
            # 等待页面加载
            import time
            time.sleep(3)
            
            # 获取页面快照
            browser.action = "snapshot"
            browser.refs = "aria"
            snapshot = browser()
            
            # TODO: 实现具体的搜索逻辑
            # 1. 找到出发地输入框并填写
            # 2. 找到目的地输入框并填写
            # 3. 找到日期选择器并选择日期
            # 4. 点击搜索按钮
            # 5. 等待结果加载
            # 6. 提取航班信息和价格
            
            return {
                "platform": "fliggy",
                "flights": [],  # 航班列表
                "lowest_price": None,
                "error": None
            }
            
        except Exception as e:
            return {
                "platform": "fliggy",
                "flights": [],
                "lowest_price": None,
                "error": str(e)
            }
    
    def search_ctrip(self, from_city: str, to_city: str, date: str,
                    return_date: Optional[str] = None) -> Dict:
        """搜索携程航班"""
        print(f"\n🐬 正在搜索携程：{from_city} → {to_city} ({date})")
        
        try:
            # 打开携程航班搜索页
            browser.action = "open"
            browser.profile = self.browser_profile
            browser.url = self.PLATFORMS["ctrip"]["search_url"]
            browser()
            
            # TODO: 实现具体的搜索逻辑
            
            return {
                "platform": "ctrip",
                "flights": [],
                "lowest_price": None,
                "error": None
            }
            
        except Exception as e:
            return {
                "platform": "ctrip",
                "flights": [],
                "lowest_price": None,
                "error": str(e)
            }
    

    
    def compare_prices(self, from_city: str, to_city: str, date: str,
                      return_date: Optional[str] = None) -> Dict:
        """
        对比所有平台的航班价格
        
        Returns:
            比价结果字典
        """
        print("=" * 60)
        print(f"✈️  机票比价：{from_city} → {to_city}")
        print(f"📅 日期：{date}" + (f" (往返：{return_date})" if return_date else ""))
        print("=" * 60)
        
        # 搜索各平台
        search_funcs = {
            "fliggy": self.search_fliggy,
            "ctrip": self.search_ctrip
        }
        
        for platform in self.platforms:
            if platform in search_funcs:
                result = search_funcs[platform](
                    from_city, to_city, date, return_date
                )
                self.results[platform] = result
        
        # 生成比价报告
        return self._generate_report(from_city, to_city, date, return_date)
    
    def _generate_report(self, from_city: str, to_city: str, 
                        date: str, return_date: Optional[str] = None) -> Dict:
        """生成比价报告"""
        print("\n" + "=" * 60)
        print("📊 比价结果")
        print("=" * 60)
        
        # 收集所有有效结果
        valid_results = []
        for platform, result in self.results.items():
            if result.get("lowest_price") and not result.get("error"):
                valid_results.append({
                    "platform": platform,
                    "price": result["lowest_price"],
                    "flights": result["flights"]
                })
        
        if not valid_results:
            print("⚠️  未获取到有效价格信息")
            return {"success": False, "error": "无有效数据"}
        
        # 按价格排序
        valid_results.sort(key=lambda x: x["price"])
        
        # 输出结果
        print(f"\n**航线：** {from_city} → {to_city}")
        print(f"**日期：** {date}")
        print(f"\n### 价格对比\n")
        print("| 排名 | 平台 | 最低价 | 航班 | 时间 |")
        print("|------|------|--------|------|------|")
        
        for i, result in enumerate(valid_results):
            platform_info = self.PLATFORMS.get(result["platform"], {})
            emoji = platform_info.get("emoji", "")
            name = platform_info.get("name", result["platform"])
            
            flight_info = result["flights"][0] if result["flights"] else {}
            flight_no = flight_info.get("flight_no", "-")
            time_range = flight_info.get("time", "-")
            
            rank = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            
            print(f"| {rank} | {emoji} {name} | ¥{result['price']} | {flight_no} | {time_range} |")
        
        # 推荐
        cheapest = valid_results[0]
        print(f"\n### 💡 推荐\n")
        print(f"**最便宜：** {self.PLATFORMS[cheapest['platform']]['name']} ¥{cheapest['price']}")
        
        return {
            "success": True,
            "results": valid_results,
            "cheapest": cheapest,
            "from": from_city,
            "to": to_city,
            "date": date
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='机票全网比价')
    parser.add_argument('--from', dest='from_city', required=True, help='出发地')
    parser.add_argument('--to', dest='to_city', required=True, help='目的地')
    parser.add_argument('--date', required=True, help='出发日期')
    parser.add_argument('--return-date', dest='return_date', help='返回日期（往返）')
    parser.add_argument('--platforms', help='指定平台，逗号分隔（fliggy,ctrip,qunar）')
    parser.add_argument('--adults', type=int, default=1, help='成人数量')
    parser.add_argument('--children', type=int, default=0, help='儿童数量')
    
    args = parser.parse_args()
    
    # 解析平台列表
    platforms = None
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(',')]
    
    # 创建比价器
    comparator = FlightPriceComparator(platforms=platforms)
    
    # 执行比价
    result = comparator.compare_prices(
        args.from_city,
        args.to_city,
        args.date,
        args.return_date
    )
    
    return 0 if result.get("success") else 1


if __name__ == '__main__':
    sys.exit(main())
