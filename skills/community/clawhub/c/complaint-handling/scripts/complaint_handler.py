#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理主程序
基于《C+基础保障服务手册》第十三章客户投诉处理规程
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from data_manager import ComplaintDataManager
from reminder_generator import ComplaintReminderGenerator
from wecom_sender import WecomSender

class ComplaintHandler:
    """投诉处理主类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        self.data_manager = ComplaintDataManager(excel_path)
        self.reminder = ComplaintReminderGenerator()
        self.sender = WecomSender()
        
        # 投诉分类配置
        self.complaint_types = {
            '安全服务类': ['消防隐患', '治安问题', '车辆管理', '人员进出'],
            '设施维护类': ['电梯故障', '空调问题', '水电问题', '网络问题'],
            '保洁类': ['公共区域清洁', '垃圾清运', '卫生间卫生'],
            '绿化类': ['绿化养护', '病虫害', '修剪'],
            '装修管理类': ['噪音扰民', '违规施工', '材料堆放'],
            '服务人员类': ['服务态度', '响应速度', '专业能力'],
            '其他类': ['其他问题']
        }
        
        # 升级投诉类型
        self.escalation_types = [
            '网络媒体投诉',
            '上级单位投诉',
            '群诉（≥5人）',
            '重复投诉',
            '安全风险类',
            '职业道德类',
            '涉及赔付类'
        ]
        
        # 处理时限配置（小时）
        self.time_limits = {
            'response': 0.5,      # 30分钟响应
            'reply': 24,          # 24小时回复
            'close': 168,         # 7日关闭
            'extension_max': 168  # 最长延期7天
        }
    
    def create_complaint(self, complaint_data):
        """创建投诉记录"""
        print(f"创建投诉记录: {complaint_data.get('客户名称', '')}")
        
        # 生成投诉ID
        complaint_id = self._generate_complaint_id()
        
        # 判断投诉分类
        complaint_type = self._classify_complaint(complaint_data.get('投诉内容', ''))
        
        # 判断投诉性质（有效/无效）
        is_valid = self._validate_complaint(complaint_data)
        
        # 判断投诉级别
        complaint_level = self._determine_complaint_level(complaint_data, is_valid)
        
        # 判断是否需要升级
        need_escalation = self._check_escalation(complaint_data)
        
        # 构建完整投诉记录
        record = {
            '投诉ID': complaint_id,
            '客户ID': complaint_data.get('客户ID', ''),
            '客户名称': complaint_data.get('客户名称', ''),
            '房号': complaint_data.get('房号', ''),
            '投诉日期': datetime.now().strftime('%Y-%m-%d'),
            '投诉时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '投诉类型': complaint_type,
            '投诉性质': '有效投诉' if is_valid else '无效投诉',
            '投诉级别': complaint_level,
            '是否升级投诉': '是' if need_escalation else '否',
            '升级类型': complaint_data.get('升级类型', '') if need_escalation else '',
            '投诉内容': complaint_data.get('投诉内容', ''),
            '响应时间': '',
            '回复时间': '',
            '处理状态': '待响应',
            '处理人': '',
            '处理结果': '',
            '关闭时间': '',
            '回访状态': '待回访',
            '回访时间': '',
            '回访满意度': '',
            '企微群ID': complaint_data.get('企微群ID', ''),
            '创建时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存投诉记录
        self.data_manager.add_complaint_record(record)
        
        # 发送响应提醒（30分钟内）
        self._schedule_response_reminder(complaint_id)
        
        # 如果是升级投诉，立即通知管理层
        if need_escalation:
            self._escalate_complaint(complaint_id, record)
        
        print(f"投诉记录已创建: {complaint_id}")
        return complaint_id
    
    def _generate_complaint_id(self):
        """生成投诉ID"""
        today = datetime.now().strftime('%Y%m%d')
        # 简化实现，实际应从数据库获取序号
        return f"CP-{today}-{datetime.now().strftime('%H%M%S')}"
    
    def _classify_complaint(self, content):
        """分类投诉"""
        # 简化实现，实际应使用关键词匹配或NLP
        for type_name, keywords in self.complaint_types.items():
            for keyword in keywords:
                if keyword in content:
                    return type_name
        return '其他类'
    
    def _validate_complaint(self, complaint_data):
        """验证投诉是否有效"""
        # 简化实现，实际应根据具体规则判断
        content = complaint_data.get('投诉内容', '')
        # 如果投诉内容为空或过于简单，判定为无效
        if len(content) < 5:
            return False
        return True
    
    def _determine_complaint_level(self, complaint_data, is_valid):
        """确定投诉级别"""
        if not is_valid:
            return '一般投诉'
        
        # 检查是否升级投诉
        if self._check_escalation(complaint_data):
            return '重大投诉'
        
        # 根据投诉类型和影响程度判断
        # 简化实现
        return '一般投诉'
    
    def _check_escalation(self, complaint_data):
        """检查是否需要升级"""
        # 检查升级类型
        escalation_type = complaint_data.get('升级类型', '')
        if escalation_type in self.escalation_types:
            return True
        
        # 检查是否群诉（≥5人）
        if complaint_data.get('投诉人数', 1) >= 5:
            return True
        
        # 检查是否重复投诉
        if complaint_data.get('是否重复投诉', False):
            return True
        
        return False
    
    def _schedule_response_reminder(self, complaint_id):
        """安排响应提醒"""
        # 30分钟后提醒
        reminder_time = datetime.now() + timedelta(hours=self.time_limits['response'])
        print(f"已安排响应提醒: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 实际实现应使用定时任务系统
        # 这里仅打印提示
    
    def _escalate_complaint(self, complaint_id, complaint_data):
        """升级投诉"""
        print(f"投诉 {complaint_id} 需要升级处理")
        
        # 发送升级通知到管理层
        escalation_message = f"""【投诉升级通知】
投诉ID: {complaint_id}
客户名称: {complaint_data['客户名称']}
房号: {complaint_data['房号']}
投诉类型: {complaint_data['投诉类型']}
升级原因: {complaint_data.get('升级类型', '需人工判断')}
投诉内容: {complaint_data['投诉内容']}

请立即处理！
"""
        
        # 发送到管理层企微群（需配置）
        # self.sender.send_to_management(escalation_message)
        print(escalation_message)
    
    def respond_complaint(self, complaint_id, handler_name):
        """响应投诉"""
        print(f"响应投诉: {complaint_id}")
        
        # 更新投诉状态
        update_data = {
            '处理状态': '已响应',
            '响应时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '处理人': handler_name
        }
        
        self.data_manager.update_complaint_status(complaint_id, **update_data)
        
        # 安排回复提醒（24小时内）
        self._schedule_reply_reminder(complaint_id)
        
        print(f"投诉 {complaint_id} 已响应")
    
    def _schedule_reply_reminder(self, complaint_id):
        """安排回复提醒"""
        # 24小时后提醒
        reminder_time = datetime.now() + timedelta(hours=self.time_limits['reply'])
        print(f"已安排回复提醒: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def reply_complaint(self, complaint_id, reply_content):
        """回复投诉"""
        print(f"回复投诉: {complaint_id}")
        
        # 更新投诉状态
        update_data = {
            '处理状态': '已回复',
            '回复时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '处理结果': reply_content
        }
        
        self.data_manager.update_complaint_status(complaint_id, **update_data)
        
        # 安排关闭提醒（7日内）
        self._schedule_close_reminder(complaint_id)
        
        print(f"投诉 {complaint_id} 已回复")
    
    def _schedule_close_reminder(self, complaint_id):
        """安排关闭提醒"""
        # 7日后提醒
        reminder_time = datetime.now() + timedelta(hours=self.time_limits['close'])
        print(f"已安排关闭提醒: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def close_complaint(self, complaint_id, close_result):
        """关闭投诉"""
        print(f"关闭投诉: {complaint_id}")
        
        # 更新投诉状态
        update_data = {
            '处理状态': '已关闭',
            '关闭时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '处理结果': close_result
        }
        
        self.data_manager.update_complaint_status(complaint_id, **update_data)
        
        # 判断是否需要回访（有效投诉100%回访）
        complaint = self.data_manager.get_complaint_by_id(complaint_id)
        if complaint and complaint.get('投诉性质') == '有效投诉':
            self._schedule_follow_up(complaint_id)
        
        print(f"投诉 {complaint_id} 已关闭")
    
    def _schedule_follow_up(self, complaint_id):
        """安排回访"""
        print(f"已安排回访: {complaint_id}")
        
        # 回访提醒（关闭后3天内）
        reminder_time = datetime.now() + timedelta(days=3)
        print(f"回访时间: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def follow_up_complaint(self, complaint_id, satisfaction):
        """回访投诉"""
        print(f"回访投诉: {complaint_id}")
        
        # 更新回访状态
        update_data = {
            '回访状态': '已回访',
            '回访时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '回访满意度': satisfaction
        }
        
        self.data_manager.update_complaint_status(complaint_id, **update_data)
        
        print(f"投诉 {complaint_id} 已回访，满意度: {satisfaction}")
    
    def check_overdue_complaints(self):
        """检查逾期投诉"""
        print("检查逾期投诉...")
        
        # 读取所有投诉记录
        complaints = self.data_manager.read_all_complaints()
        
        if complaints.empty:
            print("无投诉记录")
            return []
        
        overdue_list = []
        now = datetime.now()
        
        for _, complaint in complaints.iterrows():
            complaint_id = complaint['投诉ID']
            status = complaint['处理状态']
            create_time = datetime.strptime(complaint['创建时间'], '%Y-%m-%d %H:%M:%S')
            
            # 检查响应逾期（30分钟）
            if status == '待响应':
                elapsed = (now - create_time).total_seconds() / 3600
                if elapsed > self.time_limits['response']:
                    overdue_list.append({
                        '投诉ID': complaint_id,
                        '逾期类型': '响应逾期',
                        '逾期时长': f"{elapsed:.1f}小时",
                        '客户名称': complaint['客户名称'],
                        '投诉内容': complaint['投诉内容']
                    })
            
            # 检查回复逾期（24小时）
            elif status == '已响应':
                response_time = datetime.strptime(complaint['响应时间'], '%Y-%m-%d %H:%M:%S')
                elapsed = (now - response_time).total_seconds() / 3600
                if elapsed > self.time_limits['reply']:
                    overdue_list.append({
                        '投诉ID': complaint_id,
                        '逾期类型': '回复逾期',
                        '逾期时长': f"{elapsed:.1f}小时",
                        '客户名称': complaint['客户名称'],
                        '投诉内容': complaint['投诉内容']
                    })
            
            # 检查关闭逾期（7日）
            elif status == '已回复':
                reply_time = datetime.strptime(complaint['回复时间'], '%Y-%m-%d %H:%M:%S')
                elapsed = (now - reply_time).total_seconds() / 3600
                if elapsed > self.time_limits['close']:
                    overdue_list.append({
                        '投诉ID': complaint_id,
                        '逾期类型': '关闭逾期',
                        '逾期时长': f"{elapsed:.1f}小时",
                        '客户名称': complaint['客户名称'],
                        '投诉内容': complaint['投诉内容']
                    })
        
        print(f"发现 {len(overdue_list)} 条逾期投诉")
        return overdue_list
    
    def generate_complaint_report(self, start_date, end_date):
        """生成投诉报告"""
        print(f"生成投诉报告: {start_date} 至 {end_date}")
        
        # 读取指定时间范围的投诉记录
        complaints = self.data_manager.get_complaints_by_date_range(start_date, end_date)
        
        if complaints.empty:
            print("该时间段无投诉记录")
            return None
        
        # 统计分析
        report = {
            '报告周期': f"{start_date} 至 {end_date}",
            '投诉总数': len(complaints),
            '有效投诉数': len(complaints[complaints['投诉性质'] == '有效投诉']),
            '无效投诉数': len(complaints[complaints['投诉性质'] == '无效投诉']),
            '重大投诉数': len(complaints[complaints['投诉级别'] == '重大投诉']),
            '升级投诉数': len(complaints[complaints['是否升级投诉'] == '是']),
            '投诉类型分布': complaints['投诉类型'].value_counts().to_dict(),
            '处理状态分布': complaints['处理状态'].value_counts().to_dict(),
            '平均响应时间': self._calculate_avg_response_time(complaints),
            '平均关闭时间': self._calculate_avg_close_time(complaints),
            '回访率': self._calculate_follow_up_rate(complaints),
            '满意度分布': complaints['回访满意度'].value_counts().to_dict() if '回访满意度' in complaints.columns else {},
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存报告
        report_path = f"/Users/mac/.qclaw/skills/complaint-handling/reports/投诉报告_{start_date}_{end_date}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"投诉报告已生成: {report_path}")
        return report
    
    def _calculate_avg_response_time(self, complaints):
        """计算平均响应时间"""
        # 简化实现
        return "待计算"
    
    def _calculate_avg_close_time(self, complaints):
        """计算平均关闭时间"""
        # 简化实现
        return "待计算"
    
    def _calculate_follow_up_rate(self, complaints):
        """计算回访率"""
        valid_complaints = complaints[complaints['投诉性质'] == '有效投诉']
        if len(valid_complaints) == 0:
            return "0%"
        
        followed_up = len(valid_complaints[valid_complaints['回访状态'] == '已回访'])
        rate = followed_up / len(valid_complaints) * 100
        return f"{rate:.1f}%"
    
    def run_daily_task(self):
        """每日任务"""
        print(f"开始每日投诉管理任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 检查逾期投诉
        overdue_complaints = self.check_overdue_complaints()
        
        # 2. 生成逾期提醒
        if overdue_complaints:
            for complaint in overdue_complaints:
                reminder = self.reminder.generate_overdue_reminder(complaint)
                print(f"逾期提醒: {reminder}")
        
        # 3. 生成日报
        today = datetime.now().strftime('%Y-%m-%d')
        daily_report = {
            '日期': today,
            '逾期投诉数': len(overdue_complaints),
            '逾期详情': overdue_complaints,
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 保存日报
        report_path = f"/Users/mac/.qclaw/skills/complaint-handling/reports/日报_{today}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(daily_report, f, ensure_ascii=False, indent=2)
        
        print(f"每日任务完成，日报已保存: {report_path}")
        return daily_report

def main():
    """主函数"""
    handler = ComplaintHandler()
    
    # 根据命令行参数执行不同任务
    if len(sys.argv) > 1:
        task = sys.argv[1]
        if task == 'check':
            handler.check_overdue_complaints()
        elif task == 'report':
            start_date = sys.argv[2] if len(sys.argv) > 2 else "2024-01-01"
            end_date = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime('%Y-%m-%d')
            handler.generate_complaint_report(start_date, end_date)
        elif task == 'daily':
            handler.run_daily_task()
        else:
            print(f"未知任务: {task}")
    else:
        # 默认执行每日任务
        handler.run_daily_task()

if __name__ == "__main__":
    main()
