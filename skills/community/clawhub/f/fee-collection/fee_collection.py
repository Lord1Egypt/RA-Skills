#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
费用催缴管理技能 - 主程序
基于《C+基础保障服务手册》第十一章费用收缴管理规程
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import requests
import os
import sys

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from data_manager import DataManager
from fee_calculator import FeeCalculator
from reminder_generator import ReminderGenerator
from wecom_sender import WeComSender

class FeeCollectionManager:
    """费用催缴管理主类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        self.data_manager = DataManager(excel_path)
        self.fee_calculator = FeeCalculator()
        self.reminder_generator = ReminderGenerator()
        self.wecom_sender = WeComSender()
        
    def check_overdue_fees(self):
        """检查逾期费用"""
        print("开始检查逾期费用...")
        
        # 读取费用数据
        df = self.data_manager.read_fee_data()
        
        # 计算逾期天数
        today = datetime.now().date()
        df['逾期天数'] = df['应缴日期'].apply(lambda x: (today - x).days if x < today else 0)
        
        # 分类处理
        overdue_1_7 = df[(df['逾期天数'] >= 1) & (df['逾期天数'] <= 7)]
        overdue_8_30 = df[(df['逾期天数'] >= 8) & (df['逾期天数'] <= 30)]
        overdue_31_plus = df[df['逾期天数'] >= 31]
        
        results = {
            'total_overdue': len(df[df['逾期天数'] > 0]),
            'overdue_1_7': len(overdue_1_7),
            'overdue_8_30': len(overdue_8_30),
            'overdue_31_plus': len(overdue_31_plus),
            'details': []
        }
        
        # 生成催缴提醒
        for _, row in df[df['逾期天数'] > 0].iterrows():
            reminder = self.reminder_generator.generate_reminder(row)
            results['details'].append(reminder)
            
        return results
    
    def send_reminders(self, results):
        """发送催缴提醒"""
        print(f"开始发送催缴提醒，共{len(results['details'])}条...")
        
        # 按分级处理
        for reminder in results['details']:
            if reminder['分级'] == '1-7天':
                # 静默处理，仅记录
                print(f"静默处理：{reminder['客户名称']} - {reminder['费用类型']}")
            elif reminder['分级'] == '8-30天':
                # 推送提醒
                message = self.reminder_generator.format_message(reminder)
                self.wecom_sender.send_message(message, reminder['企微群ID'])
            elif reminder['分级'] == '31天+':
                # 升级处理，@all
                message = f"@all 【紧急催缴】{reminder['客户名称']} - {reminder['费用类型']} 已逾期{reminder['逾期天数']}天，请尽快处理！"
                self.wecom_sender.send_message(message, reminder['企微群ID'])
    
    def generate_monthly_report(self):
        """生成月度催缴报告"""
        print("生成月度催缴报告...")
        
        df = self.data_manager.read_fee_data()
        today = datetime.now()
        
        # 计算各项指标
        total_fee = df['应缴金额'].sum()
        collected_fee = df[df['缴费状态'] == '已缴']['实缴金额'].sum()
        overdue_fee = df[df['缴费状态'] == '未缴']['应缴金额'].sum()
        
        collection_rate = (collected_fee / total_fee * 100) if total_fee > 0 else 0
        
        report = {
            '报告月份': today.strftime('%Y年%m月'),
            '总费用': total_fee,
            '已缴费用': collected_fee,
            '欠缴费用': overdue_fee,
            '收缴率': f"{collection_rate:.2f}%",
            '逾期客户数': len(df[df['缴费状态'] == '未缴']),
            '生成时间': today.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存报告
        report_path = f"/Users/mac/.qclaw/skills/fee-collection/reports/月度催缴报告_{today.strftime('%Y%m')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"月度报告已保存：{report_path}")
        return report
    
    def run_daily_check(self):
        """每日检查任务"""
        print(f"开始每日费用催缴检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 检查逾期费用
        results = self.check_overdue_fees()
        
        # 2. 发送催缴提醒
        if results['total_overdue'] > 0:
            self.send_reminders(results)
        
        # 3. 生成日报
        daily_report = {
            '检查日期': datetime.now().strftime('%Y-%m-%d'),
            '逾期总数': results['total_overdue'],
            '1-7天': results['overdue_1_7'],
            '8-30天': results['overdue_8_30'],
            '31天+': results['overdue_31_plus'],
            '处理状态': '已完成'
        }
        
        # 保存日报
        report_path = f"/Users/mac/.qclaw/skills/fee-collection/reports/日报_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(daily_report, f, ensure_ascii=False, indent=2)
        
        print(f"每日检查完成，日报已保存：{report_path}")
        return daily_report

def main():
    """主函数"""
    manager = FeeCollectionManager()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == 'check':
            manager.run_daily_check()
        elif task == 'report':
            manager.generate_monthly_report()
        else:
            print(f"未知任务：{task}")
    else:
        # 默认执行每日检查
        manager.run_daily_check()

if __name__ == "__main__":
    main()
