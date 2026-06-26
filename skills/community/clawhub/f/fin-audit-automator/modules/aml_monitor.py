#!/usr/bin/env python3
"""
反洗钱 (AML) 监测模块
Anti-Money Laundering Monitoring Module
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta


class AMLDetector:
    """反洗钱检测器"""
    
    def __init__(self):
        # 加载AML规则库
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, Any]:
        """加载AML检测规则"""
        return {
            "high_freq_threshold": 5,  # 1小时内超过5笔
            "large_amount_threshold": 50000,  # 5万元
            "round_amount_threshold": 0.8,  # 80%整数金额
            "structuring_threshold": 45000,  # 结构化交易阈值
        }
    
    def detect_suspicious(self, transactions: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        识别可疑交易模式
        """
        alerts = []
        
        if transactions.empty:
            return alerts
        
        # 确保时间列是datetime类型
        if 'timestamp' in transactions.columns:
            transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
        
        # 规则1: 高频交易 (1小时内超过阈值)
        high_freq_alerts = self._check_high_frequency(transactions)
        alerts.extend(high_freq_alerts)
        
        # 规则2: 整数金额偏好
        round_amount_alerts = self._check_round_amounts(transactions)
        alerts.extend(round_amount_alerts)
        
        # 规则3: 分散转入集中转出 (或反之)
        structuring_alerts = self._check_structuring(transactions)
        alerts.extend(structuring_alerts)
        
        # 规则4: 大额现金交易
        large_cash_alerts = self._check_large_cash(transactions)
        alerts.extend(large_cash_alerts)
        
        # 规则5: 异常时间交易
        time_alerts = self._check_unusual_hours(transactions)
        alerts.extend(time_alerts)
        
        return alerts
    
    def _check_high_frequency(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """检查高频交易"""
        alerts = []
        
        if 'account_id' not in df.columns or 'timestamp' not in df.columns:
            return alerts
        
        # 按账户分组，检查1小时内的交易数量
        for account_id in df['account_id'].unique():
            account_df = df[df['account_id'] == account_id].sort_values('timestamp')
            
            if len(account_df) < self.rules['high_freq_threshold']:
                continue
            
            # 使用滚动窗口检查
            for i in range(len(account_df) - self.rules['high_freq_threshold'] + 1):
                window = account_df.iloc[i:i + self.rules['high_freq_threshold']]
                time_span = (window['timestamp'].max() - window['timestamp'].min()).total_seconds() / 3600
                
                if time_span <= 1:  # 1小时内
                    alerts.append({
                        "type": "HIGH_FREQUENCY",
                        "severity": "HIGH",
                        "account_id": account_id,
                        "description": f"1小时内{self.rules['high_freq_threshold']}笔交易",
                        "time_span": f"{time_span:.2f}小时",
                        "transaction_count": len(window),
                        "total_amount": window['amount'].sum() if 'amount' in window.columns else 0
                    })
                    break  # 每个账户只报一次
        
        return alerts
    
    def _check_round_amounts(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """检查整数金额偏好"""
        alerts = []
        
        if 'amount' not in df.columns:
            return alerts
        
        # 检查整数金额比例
        round_amounts = df[df['amount'] % 10000 == 0]
        ratio = len(round_amounts) / len(df)
        
        if ratio > self.rules['round_amount_threshold']:
            alerts.append({
                "type": "ROUND_AMOUNT_PATTERN",
                "severity": "MEDIUM",
                "description": f"{ratio*100:.1f}%的交易为整数金额",
                "round_count": len(round_amounts),
                "total_count": len(df),
                "examples": round_amounts['amount'].head(3).tolist() if not round_amounts.empty else []
            })
        
        return alerts
    
    def _check_structuring(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """检查结构化交易 (分散转入集中转出)"""
        alerts = []
        
        if 'account_id' not in df.columns or 'amount' not in df.columns:
            return alerts
        
        for account_id in df['account_id'].unique():
            account_df = df[df['account_id'] == account_id]
            
            # 检查是否有多个小额转入后大额转出
            small_in = account_df[account_df['amount'] < self.rules['structuring_threshold']]
            large_out = account_df[account_df['amount'] > self.rules['structuring_threshold']]
            
            if len(small_in) >= 3 and not large_out.empty:
                alerts.append({
                    "type": "STRUCTURING",
                    "severity": "HIGH",
                    "account_id": account_id,
                    "description": "疑似结构化交易：多笔小额转入后大额转出",
                    "small_in_count": len(small_in),
                    "small_in_total": small_in['amount'].sum(),
                    "large_out_count": len(large_out),
                    "large_out_total": large_out['amount'].sum()
                })
        
        return alerts
    
    def _check_large_cash(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """检查大额现金交易"""
        alerts = []
        
        if 'amount' not in df.columns:
            return alerts
        
        large_transactions = df[df['amount'] >= self.rules['large_amount_threshold']]
        
        for _, tx in large_transactions.iterrows():
            alerts.append({
                "type": "LARGE_CASH_TRANSACTION",
                "severity": "MEDIUM",
                "account_id": tx.get('account_id', 'unknown'),
                "amount": tx['amount'],
                "description": f"大额交易: {tx['amount']}元",
                "timestamp": str(tx.get('timestamp', ''))
            })
        
        return alerts
    
    def _check_unusual_hours(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """检查异常时间交易 (凌晨2-5点)"""
        alerts = []
        
        if 'timestamp' not in df.columns:
            return alerts
        
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        unusual_hours = df[(df['hour'] >= 2) & (df['hour'] <= 5)]
        
        if not unusual_hours.empty:
            for account_id in unusual_hours['account_id'].unique():
                account_unusual = unusual_hours[unusual_hours['account_id'] == account_id]
                if len(account_unusual) >= 2:  # 至少2笔异常时间交易
                    alerts.append({
                        "type": "UNUSUAL_HOURS",
                        "severity": "LOW",
                        "account_id": account_id,
                        "description": f"凌晨时段({account_unusual['hour'].iloc[0]}点)多笔交易",
                        "transaction_count": len(account_unusual),
                        "total_amount": account_unusual['amount'].sum() if 'amount' in account_unusual.columns else 0
                    })
        
        return alerts


if __name__ == "__main__":
    # 测试
    test_data = {
        'account_id': ['A001', 'A001', 'A001', 'A001', 'A001', 'A001', 'A002'],
        'timestamp': [
            '2024-01-01 10:00:00',
            '2024-01-01 10:15:00',
            '2024-01-01 10:30:00',
            '2024-01-01 10:45:00',
            '2024-01-01 11:00:00',
            '2024-01-01 11:15:00',
            '2024-01-01 12:00:00'
        ],
        'amount': [10000, 10000, 10000, 10000, 10000, 50000, 30000],
        'type': ['in', 'in', 'in', 'in', 'in', 'out', 'in']
    }
    
    df = pd.DataFrame(test_data)
    detector = AMLDetector()
    alerts = detector.detect_suspicious(df)
    
    print(f"检测到 {len(alerts)} 个可疑交易预警:")
    for alert in alerts:
        print(f"  - [{alert['severity']}] {alert['type']}: {alert['description']}")
