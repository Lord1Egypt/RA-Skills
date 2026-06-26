#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fund Keeper - 收益统计与定投管理
功能：
1. 收益统计（累计收益、收益率、趋势）
2. 定投计划管理
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

try:
    import pandas as pd
except ImportError:
    print("Missing dependency: pandas")
    print("Install with: pip install pandas")
    sys.exit(1)


class FundStats:
    """收益统计类"""
    
    def __init__(self, funds_dir):
        # 优先使用技能目录下的 funds
        if funds_dir is None:
            skill_funds_dir = Path(__file__).parent / "funds"
            if skill_funds_dir.exists():
                self.funds_dir = skill_funds_dir
            else:
                # 兼容旧版
                self.funds_dir = Path(__file__).parent.parent.parent / "funds"
                self.funds_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.funds_dir = Path(funds_dir)
        self.my_funds_file = self.funds_dir / "my-funds.md"
        self.stats_file = self.funds_dir / "stats.json"
        self.sip_plan_file = self.funds_dir / "sip-plan.json"
        self.sip_record_file = self.funds_dir / "sip-record.md"
    
    def get_fund_list(self):
        """获取持仓基金列表"""
        if not self.my_funds_file.exists():
            return []
        
        funds = []
        with open(self.my_funds_file, "r", encoding="utf-8") as f:
            in_table = False
            for line in f:
                line = line.strip()
                if line.startswith("|") and "基金代码" in line:
                    in_table = True
                    continue
                if in_table and line.startswith("|"):
                    parts = line.split("|")
                    if len(parts) >= 5:
                        code = parts[1].strip()
                        if code and code != "---" and not code.startswith("-") and code.isdigit():
                            try:
                                # 新格式：基金代码|基金名称|持有金额|持有收益|止盈%|止损%|定投日|备注
                                amount = float(parts[3].strip() or 0)
                                profit_str = parts[4].strip() if len(parts) > 4 else "0"
                                sip_day = int(parts[7].strip()) if len(parts) > 7 and parts[7].strip().isdigit() else 0
                                note = parts[8].strip() if len(parts) > 8 else ""
                                
                                # 解析收益
                                try:
                                    profit = float(profit_str.replace("+", "").replace("元", ""))
                                except:
                                    profit = 0
                                
                                # 计算成本
                                cost = amount - profit
                                
                                funds.append({
                                    "code": code,
                                    "name": parts[2].strip(),
                                    "amount": amount,
                                    "cost": cost,
                                    "profit": profit,
                                    "sip_day": sip_day,
                                    "note": note,
                                    "is_sip": sip_day > 0
                                })
                            except ValueError:
                                pass
        return funds
    
    def calculate_stats(self):
        """计算收益统计"""
        funds = self.get_fund_list()
        if not funds:
            return None
        
        total_cost = sum(f["cost"] for f in funds)
        total_amount = sum(f["amount"] for f in funds)
        total_profit = total_amount - total_cost
        profit_rate = (total_profit / total_cost * 100) if total_cost > 0 else 0
        
        # 单个基金收益贡献
        for fund in funds:
            fund["profit_contribution"] = (fund["profit"] / total_profit * 100) if total_profit != 0 else 0
        
        # 按收益排序
        funds_sorted = sorted(funds, key=lambda x: x["profit"], reverse=True)
        
        stats = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_cost": total_cost,
            "total_amount": total_amount,
            "total_profit": total_profit,
            "profit_rate": profit_rate,
            "fund_count": len(funds),
            "sip_count": sum(1 for f in funds if f["is_sip"]),
            "top_contributor": funds_sorted[0] if funds_sorted else None,
            "funds": funds_sorted
        }
        
        # 保存到文件
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return stats
    
    def print_stats(self, show_chart=False):
        """打印收益统计"""
        stats = self.calculate_stats()
        if not stats:
            print("No holdings data")
            return
        
        print("\n" + "="*60)
        print(f"【收益统计】{stats['date']}")
        print("="*60 + "\n")
        
        print(f"总投入：  {stats['total_cost']:,.2f} 元")
        print(f"当前值：  {stats['total_amount']:,.2f} 元")
        print(f"累计收益：{stats['total_profit']:+,.2f} 元 ({stats['profit_rate']:+.2f}%)")
        print(f"持有基金：{stats['fund_count']} 支 ({stats['sip_count']} 支定投)")
        
        if stats['top_contributor']:
            top = stats['top_contributor']
            print(f"收益贡献王：{top['code']} {top['name']} ({top['profit']:+,.2f} 元)")
        
        print("\n【收益贡献排名】")
        print("-"*60)
        for i, fund in enumerate(stats['funds'][:5], 1):
            bar_len = int(abs(fund['profit_contribution']) / 2)
            # Use ASCII bars to avoid encoding issues
            bar = "[+]" * bar_len if fund['profit'] >= 0 else "[-]" * bar_len
            print(f"{i}. {fund['code']} {fund['name']:<15} {fund['profit']:>+8,.2f} {bar} {fund['profit_contribution']:+.1f}%")
        
        print("\n" + "="*60)
        
        if show_chart:
            self.print_pie_chart(stats)
            self.print_profit_chart(stats)
    
    def print_pie_chart(self, stats):
        """打印持仓饼图（文本）"""
        print("\n【持仓分布】\n")
        
        total = stats['total_amount']
        if total == 0:
            return
        
        # 按金额排序
        funds = sorted(stats['funds'], key=lambda x: x['amount'], reverse=True)
        
        for fund in funds:
            percent = fund['amount'] / total * 100
            bar_len = int(percent / 2)  # 每2%一格
            
            # 根据收益选择颜色标记
            marker = "+" if fund['profit'] >= 0 else "-"
            
            # 构建条形图
            bar = f"[{marker}]" * bar_len
            
            print(f"{fund['code']} {fund['name'][:8]:<8} {fund['amount']:>8,.0f}元 {percent:>5.1f}% {bar}")
        
        print()
    
    def print_profit_chart(self, stats):
        """打印收益对比图（文本）"""
        print("\n【收益对比】\n")
        
        # 找出最大收益和最小收益
        profits = [f['profit'] for f in stats['funds']]
        if not profits:
            return
        
        max_profit = max(profits) if profits else 0
        min_profit = min(profits) if profits else 0
        
        # 确定刻度
        scale = max(abs(max_profit), abs(min_profit), 100)
        
        # 打印收益条形图
        for fund in sorted(stats['funds'], key=lambda x: x['profit'], reverse=True):
            profit = fund['profit']
            
            # 计算条形长度（正数向右，负数向左）
            if profit >= 0:
                bar_len = int(profit / scale * 20)
                bar = "." * 20 + "|" + "+" * bar_len
            else:
                bar_len = int(abs(profit) / scale * 20)
                bar = "." * (20 - bar_len) + "-" * bar_len + "|" + "." * 20
            
            print(f"{fund['code']} {fund['name'][:8]:<8} {profit:>+8,.0f} {bar}")
        
        # 打印刻度
        print(f"\n刻度: -{scale:.0f}元 {'.'*20}|{'.'*20} +{scale:.0f}元\n")
    
    def print_trend_chart(self, days=7):
        """打印收益趋势图（需要历史数据）"""
        stats_file = self.funds_dir / "stats_history.json"
        
        if not stats_file.exists():
            print("\n暂无历史数据，无法显示趋势图")
            print("提示：每日运行 stats 命令会自动记录数据\n")
            return
        
        try:
            with open(stats_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            print("\n历史数据读取失败\n")
            return
        
        if len(history) < 2:
            print("\n历史数据不足（至少需要2天）\n")
            return
        
        print("\n【收益趋势】（最近{}天）\n".format(min(days, len(history))))
        
        # 取最近N天的数据
        recent = history[-days:]
        
        # 找出最大最小值
        profits = [h['total_profit'] for h in recent]
        max_p = max(profits) if profits else 0
        min_p = min(profits) if profits else 0
        scale = max(abs(max_p), abs(min_p), 100)
        
        # 打印趋势图
        for h in recent:
            profit = h['total_profit']
            date = h['date'][:10]
            
            # 计算条形
            if profit >= 0:
                bar_len = int(profit / scale * 20)
                bar = "." * 20 + "|" + "+" * bar_len
            else:
                bar_len = int(abs(profit) / scale * 20)
                bar = "." * (20 - bar_len) + "-" * bar_len + "|" + "." * 20
            
            print(f"{date} {profit:>+8,.0f} {bar}")
        
        print()
    
    def save_stats_history(self):
        """保存历史统计数据"""
        stats = self.calculate_stats()
        if not stats:
            return
        
        stats_history_file = self.funds_dir / "stats_history.json"
        
        # 读取现有历史
        history = []
        if stats_history_file.exists():
            try:
                with open(stats_history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except:
                history = []
        
        # 添加今日数据（只保留关键字段）
        today_data = {
            "date": stats['date'],
            "total_cost": stats['total_cost'],
            "total_amount": stats['total_amount'],
            "total_profit": stats['total_profit'],
            "profit_rate": stats['profit_rate']
        }
        
        # 检查是否已有今天的数据
        today_str = stats['date'][:10]
        existing_today = [i for i, h in enumerate(history) if h['date'].startswith(today_str)]
        
        if existing_today:
            # 更新今天的数据
            history[existing_today[0]] = today_data
        else:
            # 添加新数据
            history.append(today_data)
        
        # 只保留最近30天
        history = history[-30:]
        
        # 保存
        with open(stats_history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)


class SIPManager:
    """定投计划管理类"""
    
    def __init__(self, funds_dir):
        self.funds_dir = Path(funds_dir)
        self.sip_plan_file = self.funds_dir / "sip-plan.json"
        self.sip_record_file = self.funds_dir / "sip-record.md"
    
    def load_plans(self):
        """加载定投计划"""
        if self.sip_plan_file.exists():
            with open(self.sip_plan_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"plans": []}
    
    def save_plans(self, plans):
        """保存定投计划"""
        with open(self.sip_plan_file, "w", encoding="utf-8") as f:
            json.dump(plans, f, indent=2, ensure_ascii=False)
    
    def add_plan(self, fund_code, fund_name, amount, day_of_month, note=""):
        """添加定投计划"""
        plans = self.load_plans()
        
        # 检查是否已存在
        for plan in plans["plans"]:
            if plan["fund_code"] == fund_code and plan["status"] == "active":
                print(f"Fund {fund_code} already has an active SIP plan")
                return False
        
        new_plan = {
            "fund_code": fund_code,
            "fund_name": fund_name,
            "amount": amount,
            "day_of_month": day_of_month,
            "status": "active",
            "note": note,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        
        plans["plans"].append(new_plan)
        self.save_plans(plans)
        
        # 记录到日志
        self._log_action("ADD", fund_code, amount, day_of_month)
        
        print(f"Added SIP plan: {fund_code} {fund_name}, {amount} yuan/month, day {day_of_month}")
        return True
    
    def list_plans(self):
        """列出定投计划"""
        plans = self.load_plans()
        
        if not plans["plans"]:
            print("No SIP plans")
            return []
        
        print("\n" + "="*60)
        print("【定投计划】")
        print("="*60 + "\n")
        
        active_plans = [p for p in plans["plans"] if p["status"] == "active"]
        inactive_plans = [p for p in plans["plans"] if p["status"] != "active"]
        
        if active_plans:
            print("【进行中】")
            for plan in active_plans:
                print(f"  {plan['fund_code']} {plan['fund_name']:<15} {plan['amount']:>6} 元/月  每月{plan['day_of_month']:>2}日")
        
        if inactive_plans:
            print("\n【已暂停/已完成】")
            for plan in inactive_plans:
                print(f"  {plan['fund_code']} {plan['fund_name']:<15} [{plan['status']}]")
        
        print("\n" + "="*60)
        
        # 计算月度定投总额
        monthly_total = sum(p["amount"] for p in active_plans)
        print(f"月度定投总额：{monthly_total} 元")
        print("="*60 + "\n")
        
        return plans["plans"]
    
    def pause_plan(self, fund_code):
        """暂停定投计划"""
        plans = self.load_plans()
        
        found = False
        for plan in plans["plans"]:
            if plan["fund_code"] == fund_code and plan["status"] == "active":
                plan["status"] = "paused"
                plan["paused_at"] = datetime.now().strftime("%Y-%m-%d")
                found = True
                break
        
        if found:
            self.save_plans(plans)
            self._log_action("PAUSE", fund_code, 0, 0)
            print(f"Paused SIP plan: {fund_code}")
        else:
            print(f"No active SIP plan found for {fund_code}")
    
    def resume_plan(self, fund_code):
        """恢复定投计划"""
        plans = self.load_plans()
        
        found = False
        for plan in plans["plans"]:
            if plan["fund_code"] == fund_code and plan["status"] == "paused":
                plan["status"] = "active"
                plan["resumed_at"] = datetime.now().strftime("%Y-%m-%d")
                found = True
                break
        
        if found:
            self.save_plans(plans)
            self._log_action("RESUME", fund_code, 0, 0)
            print(f"Resumed SIP plan: {fund_code}")
        else:
            print(f"No paused SIP plan found for {fund_code}")
    
    def delete_plan(self, fund_code):
        """删除定投计划"""
        plans = self.load_plans()
        
        original_count = len(plans["plans"])
        plans["plans"] = [p for p in plans["plans"] if p["fund_code"] != fund_code]
        
        if len(plans["plans"]) < original_count:
            self.save_plans(plans)
            self._log_action("DELETE", fund_code, 0, 0)
            print(f"Deleted SIP plan: {fund_code}")
        else:
            print(f"No SIP plan found for {fund_code}")
    
    def _log_action(self, action, fund_code, amount, day):
        """记录操作日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not self.sip_record_file.exists():
            with open(self.sip_record_file, "w", encoding="utf-8") as f:
                f.write("# 定投操作记录\n\n")
        
        with open(self.sip_record_file, "a", encoding="utf-8") as f:
            f.write(f"- [{timestamp}] {action}: {fund_code}, Amount: {amount}, Day: {day}\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fund Keeper - 收益统计与定投管理")
    parser.add_argument("mode", choices=["stats", "sip"], help="模式：stats(收益统计), sip(定投管理)")
    
    # stats 参数
    parser.add_argument("--chart", action="store_true", help="显示图表（文本）")
    
    # sip 参数
    parser.add_argument("--add", action="store_true", help="添加定投计划")
    parser.add_argument("--list", action="store_true", help="列出定投计划")
    parser.add_argument("--pause", help="暂停定投计划（基金代码）")
    parser.add_argument("--resume", help="恢复定投计划（基金代码）")
    parser.add_argument("--delete", help="删除定投计划（基金代码）")
    parser.add_argument("--fund", help="基金代码")
    parser.add_argument("--name", help="基金名称")
    parser.add_argument("--amount", type=float, help="定投金额（元）")
    parser.add_argument("--day", type=int, help="每月定投日（1-28）")
    
    args = parser.parse_args()
    
    # funds 目录优先使用技能目录
    skill_funds_dir = Path(__file__).parent / "funds"
    if skill_funds_dir.exists():
        funds_dir = skill_funds_dir
    else:
        # 兼容旧版
        import os
        funds_dir = Path(os.path.abspath(os.path.join(os.getcwd(), "../../funds")))
    
    if args.mode == "stats":
        stats = FundStats(funds_dir)
        stats.print_stats(show_chart=args.chart)
    
    elif args.mode == "sip":
        sip = SIPManager(funds_dir)
        
        if args.add:
            if not args.fund or not args.amount or not args.day:
                print("Error: --fund, --amount, and --day are required for adding a plan")
                print("Usage: py fund_stats.py sip --add --fund 011608 --amount 500 --day 15")
                return
            name = args.name or "Unknown"
            sip.add_plan(args.fund, name, args.amount, args.day)
        
        elif args.list:
            sip.list_plans()
        
        elif args.pause:
            sip.pause_plan(args.pause)
        
        elif args.resume:
            sip.resume_plan(args.resume)
        
        elif args.delete:
            sip.delete_plan(args.delete)
        
        else:
            print("Please specify an action: --add, --list, --pause, --resume, or --delete")
            print("\nExamples:")
            print("  py fund_stats.py sip --list")
            print("  py fund_stats.py sip --add --fund 011608 --amount 500 --day 15")
            print("  py fund_stats.py sip --pause 011608")


if __name__ == "__main__":
    main()
