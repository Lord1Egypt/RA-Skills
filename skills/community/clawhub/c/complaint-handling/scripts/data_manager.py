#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投诉处理数据管理模块
负责读取和写入投诉数据
"""

import pandas as pd
import os
from datetime import datetime

class ComplaintDataManager:
    """投诉处理数据管理类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        
    def read_all_complaints(self):
        """读取所有投诉记录"""
        try:
            # 读取投诉记录表
            df = pd.read_excel(self.excel_path, sheet_name='投诉记录')
            
            # 数据清洗
            if '投诉日期' in df.columns:
                df['投诉日期'] = pd.to_datetime(df['投诉日期'], errors='coerce').dt.date
            if '创建时间' in df.columns:
                df['创建时间'] = pd.to_datetime(df['创建时间'], errors='coerce')
            
            return df
        except Exception as e:
            print(f"读取投诉记录失败: {e}")
            # 返回空DataFrame
            return pd.DataFrame(columns=[
                '投诉ID', '客户ID', '客户名称', '房号', '投诉日期', '投诉时间',
                '投诉类型', '投诉性质', '投诉级别', '是否升级投诉', '升级类型',
                '投诉内容', '响应时间', '回复时间', '处理状态', '处理人',
                '处理结果', '关闭时间', '回访状态', '回访时间', '回访满意度',
                '企微群ID', '创建时间'
            ])
    
    def get_complaint_by_id(self, complaint_id):
        """根据投诉ID获取投诉记录"""
        try:
            df = self.read_all_complaints()
            
            if df.empty:
                return None
            
            complaint = df[df['投诉ID'] == complaint_id]
            
            if complaint.empty:
                return None
            
            return complaint.iloc[0].to_dict()
        except Exception as e:
            print(f"获取投诉记录失败: {e}")
            return None
    
    def get_complaints_by_date_range(self, start_date, end_date):
        """按日期范围获取投诉记录"""
        try:
            df = self.read_all_complaints()
            
            if df.empty:
                return pd.DataFrame()
            
            # 确保日期列是datetime类型
            if '投诉日期' in df.columns:
                df['投诉日期'] = pd.to_datetime(df['投诉日期'], errors='coerce')
                start_dt = pd.to_datetime(start_date)
                end_dt = pd.to_datetime(end_date)
                
                # 筛选日期范围
                mask = (df['投诉日期'] >= start_dt) & (df['投诉日期'] <= end_dt)
                return df[mask]
            
            return pd.DataFrame()
        except Exception as e:
            print(f"按日期范围获取投诉记录失败: {e}")
            return pd.DataFrame()
    
    def add_complaint_record(self, complaint_record):
        """添加投诉记录"""
        try:
            # 读取现有记录
            if os.path.exists(self.excel_path):
                try:
                    df = pd.read_excel(self.excel_path, sheet_name='投诉记录')
                except:
                    # 如果投诉记录表不存在，创建新表
                    df = pd.DataFrame(columns=[
                        '投诉ID', '客户ID', '客户名称', '房号', '投诉日期', '投诉时间',
                        '投诉类型', '投诉性质', '投诉级别', '是否升级投诉', '升级类型',
                        '投诉内容', '响应时间', '回复时间', '处理状态', '处理人',
                        '处理结果', '关闭时间', '回访状态', '回访时间', '回访满意度',
                        '企微群ID', '创建时间'
                    ])
            else:
                df = pd.DataFrame(columns=[
                    '投诉ID', '客户ID', '客户名称', '房号', '投诉日期', '投诉时间',
                    '投诉类型', '投诉性质', '投诉级别', '是否升级投诉', '升级类型',
                    '投诉内容', '响应时间', '回复时间', '处理状态', '处理人',
                    '处理结果', '关闭时间', '回访状态', '回访时间', '回访满意度',
                    '企微群ID', '创建时间'
                ])
            
            # 添加新记录
            new_record = pd.DataFrame([complaint_record])
            df = pd.concat([df, new_record], ignore_index=True)
            
            # 保存
            self._save_complaints(df)
            
            print(f"投诉记录已添加: {complaint_record.get('投诉ID', '')}")
            return True
        except Exception as e:
            print(f"添加投诉记录失败: {e}")
            return False
    
    def update_complaint_status(self, complaint_id, **kwargs):
        """更新投诉状态"""
        try:
            # 读取现有记录
            df = self.read_all_complaints()
            
            if df.empty:
                print("无投诉记录")
                return False
            
            # 找到对应记录
            idx = df[df['投诉ID'] == complaint_id].index
            if len(idx) == 0:
                print(f"未找到投诉ID: {complaint_id}")
                return False
            
            # 更新字段
            for key, value in kwargs.items():
                if key in df.columns:
                    df.loc[idx[0], key] = value
            
            # 保存
            self._save_complaints(df)
            
            print(f"投诉ID {complaint_id} 状态已更新")
            return True
        except Exception as e:
            print(f"更新投诉状态失败: {e}")
            return False
    
    def _save_complaints(self, df):
        """保存投诉记录"""
        try:
            # 使用ExcelWriter追加模式
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='投诉记录', index=False)
            
            print("投诉记录已保存")
            return True
        except Exception as e:
            print(f"保存投诉记录失败: {e}")
            return False
    
    def get_complaints_by_customer(self, customer_id):
        """获取客户的投诉记录"""
        try:
            df = self.read_all_complaints()
            
            if df.empty:
                return pd.DataFrame()
            
            # 筛选客户记录
            customer_complaints = df[df['客户ID'] == customer_id]
            
            return customer_complaints
        except Exception as e:
            print(f"获取客户投诉记录失败: {e}")
            return pd.DataFrame()
    
    def get_complaint_stats(self):
        """获取投诉统计"""
        try:
            df = self.read_all_complaints()
            
            if df.empty:
                return {
                    'total': 0,
                    'valid': 0,
                    'invalid': 0,
                    'major': 0,
                    'escalation': 0,
                    'pending_response': 0,
                    'pending_reply': 0,
                    'pending_close': 0,
                    'closed': 0,
                    'follow_up_rate': '0%'
                }
            
            # 统计
            stats = {
                'total': len(df),
                'valid': len(df[df['投诉性质'] == '有效投诉']),
                'invalid': len(df[df['投诉性质'] == '无效投诉']),
                'major': len(df[df['投诉级别'] == '重大投诉']),
                'escalation': len(df[df['是否升级投诉'] == '是']),
                'pending_response': len(df[df['处理状态'] == '待响应']),
                'pending_reply': len(df[df['处理状态'] == '已响应']),
                'pending_close': len(df[df['处理状态'] == '已回复']),
                'closed': len(df[df['处理状态'] == '已关闭'])
            }
            
            # 计算回访率
            valid_complaints = df[df['投诉性质'] == '有效投诉']
            if len(valid_complaints) > 0:
                followed_up = len(valid_complaints[valid_complaints['回访状态'] == '已回访'])
                stats['follow_up_rate'] = f"{followed_up / len(valid_complaints) * 100:.1f}%"
            else:
                stats['follow_up_rate'] = '0%'
            
            return stats
        except Exception as e:
            print(f"获取投诉统计失败: {e}")
            return {}
    
    def backup_excel(self):
        """备份Excel文件"""
        try:
            backup_dir = "/Users/mac/.qclaw/skills/complaint-handling/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(backup_dir, f"美兰中心C+服务_{timestamp}.xlsx")
            
            # 复制文件
            import shutil
            shutil.copy2(self.excel_path, backup_path)
            
            print(f"Excel文件已备份: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
            return None