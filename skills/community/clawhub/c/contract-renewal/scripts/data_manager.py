#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同续租管理数据管理模块
负责读取和写入合同续租数据
"""

import pandas as pd
import os
from datetime import datetime

class ContractRenewalDataManager:
    """合同续租数据管理类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
    
    def get_all_customers(self):
        """获取所有客户列表"""
        try:
            # 读取客户信息表
            df = pd.read_excel(self.excel_path, sheet_name='客户信息')
            
            # 数据清洗
            df = df.dropna(subset=['客户名称'])
            
            return df
        except Exception as e:
            print(f"读取客户信息失败: {e}")
            return pd.DataFrame()
    
    def get_customer_by_id(self, customer_id):
        """根据客户ID获取客户数据"""
        try:
            df = self.get_all_customers()
            
            if df.empty:
                return None
            
            customer = df[df['客户ID'] == customer_id]
            
            if customer.empty:
                return None
            
            return customer.iloc[0].to_dict()
        except Exception as e:
            print(f"获取客户数据失败: {e}")
            return None
    
    def add_renewal_plan(self, plan):
        """添加续租计划"""
        try:
            # 读取现有记录
            if os.path.exists(self.excel_path):
                try:
                    df = pd.read_excel(self.excel_path, sheet_name='续租计划')
                except:
                    # 如果续租计划表不存在，创建新表
                    df = pd.DataFrame(columns=[
                        '计划ID', '客户ID', '客户名称', '房号', '企业画像',
                        '匹配方案', '方案要点', '租金策略', '建议措施',
                        '预计成功率', '状态', '创建时间', '更新时间'
                    ])
            else:
                df = pd.DataFrame(columns=[
                    '计划ID', '客户ID', '客户名称', '房号', '企业画像',
                    '匹配方案', '方案要点', '租金策略', '建议措施',
                    '预计成功率', '状态', '创建时间', '更新时间'
                ])
            
            # 添加新记录
            new_record = pd.DataFrame([plan])
            df = pd.concat([df, new_record], ignore_index=True)
            
            # 保存
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='续租计划', index=False)
            
            print(f"续租计划已添加: {plan.get('计划ID', '')}")
            return True
        except Exception as e:
            print(f"添加续租计划失败: {e}")
            return False
    
    def get_renewal_plan_by_id(self, plan_id):
        """根据计划ID获取续租计划"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name='续租计划')
            
            if df.empty:
                return None
            
            plan = df[df['计划ID'] == plan_id]
            
            if plan.empty:
                return None
            
            return plan.iloc[0].to_dict()
        except Exception as e:
            print(f"获取续租计划失败: {e}")
            return None
    
    def get_renewal_plans_by_date_range(self, start_date, end_date):
        """按日期范围获取续租计划"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name='续租计划')
            
            if df.empty:
                return pd.DataFrame()
            
            # 筛选日期范围
            df['创建时间'] = pd.to_datetime(df['创建时间'], errors='coerce')
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            mask = (df['创建时间'] >= start_dt) & (df['创建时间'] <= end_dt)
            return df[mask]
        except Exception as e:
            print(f"按日期范围获取续租计划失败: {e}")
            return pd.DataFrame()
    
    def update_renewal_plan(self, plan_id, update_data):
        """更新续租计划"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name='续租计划')
            
            if df.empty:
                print("无续租计划")
                return False
            
            # 找到对应记录
            idx = df[df['计划ID'] == plan_id].index
            if len(idx) == 0:
                print(f"未找到计划ID: {plan_id}")
                return False
            
            # 更新字段
            for key, value in update_data.items():
                if key in df.columns:
                    df.loc[idx[0], key] = value
            
            # 更新时间
            df.loc[idx[0], '更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 保存
            with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='续租计划', index=False)
            
            print(f"续租计划 {plan_id} 已更新")
            return True
        except Exception as e:
            print(f"更新续租计划失败: {e}")
            return False
    
    def get_customers_expiring_soon(self, months=6):
        """获取即将到期的客户"""
        try:
            df = self.get_all_customers()
            
            if df.empty:
                return pd.DataFrame()
            
            # 筛选即将到期的客户
            df['合同到期日期'] = pd.to_datetime(df['合同到期日期'], errors='coerce')
            
            today = datetime.now()
            future_date = today + pd.DateOffset(months=months)
            
            mask = (df['合同到期日期'] >= today) & (df['合同到期日期'] <= future_date)
            return df[mask]
        except Exception as e:
            print(f"获取即将到期客户失败: {e}")
            return pd.DataFrame()
    
    def get_renewal_statistics(self):
        """获取续租统计"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name='续租计划')
            
            if df.empty:
                return {
                    '总计划数': 0,
                    '已完成数': 0,
                    '成功率': 0
                }
            
            total = len(df)
            completed = len(df[df['状态'] == '已完成']) if '状态' in df.columns else 0
            
            return {
                '总计划数': total,
                '已完成数': completed,
                '成功率': round(completed / total * 100, 1) if total > 0 else 0
            }
        except Exception as e:
            print(f"获取续租统计失败: {e}")
            return {}
    
    def get_enterprise_profiles(self):
        """获取企业画像数据"""
        try:
            df = pd.read_excel(self.excel_path, sheet_name='企业画像')
            
            return df
        except Exception as e:
            print(f"获取企业画像失败: {e}")
            return pd.DataFrame()