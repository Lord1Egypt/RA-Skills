#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据管理模块 - 负责读取和写入Excel数据
"""

import pandas as pd
import os
from datetime import datetime

class DataManager:
    """数据管理类"""
    
    def __init__(self, excel_path="/Users/mac/美兰中心C+服务.xlsx"):
        """初始化"""
        self.excel_path = excel_path
        
    def read_fee_data(self):
        """读取费用数据"""
        try:
            # 读取费用收缴表
            df = pd.read_excel(self.excel_path, sheet_name='费用收缴')
            
            # 数据清洗和转换
            df['应缴日期'] = pd.to_datetime(df['应缴日期']).dt.date
            df['实缴日期'] = pd.to_datetime(df['实缴日期'], errors='coerce').dt.date
            
            return df
        except Exception as e:
            print(f"读取费用数据失败: {e}")
            return pd.DataFrame()
    
    def read_customer_data(self):
        """读取客户数据"""
        try:
            # 读取客户信息表
            df = pd.read_excel(self.excel_path, sheet_name='客户信息')
            return df
        except Exception as e:
            print(f"读取客户数据失败: {e}")
            return pd.DataFrame()
    
    def update_fee_status(self, fee_id, status, payment_date=None, payment_amount=None):
        """更新费用状态"""
        try:
            # 读取现有数据
            df = pd.read_excel(self.excel_path, sheet_name='费用收缴')
            
            # 找到对应记录
            idx = df[df['费用ID'] == fee_id].index
            if len(idx) > 0:
                df.loc[idx[0], '缴费状态'] = status
                if payment_date:
                    df.loc[idx[0], '实缴日期'] = payment_date
                if payment_amount:
                    df.loc[idx[0], '实缴金额'] = payment_amount
                
                # 保存回Excel
                with pd.ExcelWriter(self.excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name='费用收缴', index=False)
                
                print(f"费用ID {fee_id} 状态更新为: {status}")
                return True
            else:
                print(f"未找到费用ID: {fee_id}")
                return False
        except Exception as e:
            print(f"更新费用状态失败: {e}")
            return False
    
    def get_customers_by_fee_status(self, status='未缴'):
        """根据费用状态获取客户列表"""
        try:
            fee_df = self.read_fee_data()
            customer_df = self.read_customer_data()
            
            # 筛选出指定状态的费用
            filtered_fees = fee_df[fee_df['缴费状态'] == status]
            
            # 关联客户信息
            result = pd.merge(filtered_fees, customer_df, on='客户ID', how='left')
            return result
        except Exception as e:
            print(f"获取客户列表失败: {e}")
            return pd.DataFrame()
    
    def backup_excel(self):
        """备份Excel文件"""
        try:
            backup_dir = "/Users/mac/.qclaw/skills/fee-collection/backups"
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