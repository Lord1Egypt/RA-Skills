#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-accounting - 自动记账 Skill
Copyright (c) 2026 摇摇

本软件受著作权法保护。虽然采用 MIT-0 许可证允许商用，
但必须保留原始版权声明。

禁止：
- 移除或修改版权声明
- 声称为自己开发
- 在非授权环境使用

官方环境：小艺 Claw + 一日记账 APP
联系方式：QQ 2756077825
"""

"""
记账历史记录管理
记录和管理记账历史
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional


class AccountingHistory:
    """记账历史管理"""
    
    def __init__(self, history_path: Optional[str] = None):
        """
        初始化历史管理
        
        Args:
            history_path: 历史记录文件路径
        """
        self.history_path = history_path
        self.history: List[Dict[str, Any]] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """加载历史记录"""
        if self.history_path and os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    def save_history(self) -> bool:
        """保存历史记录"""
        if not self.history_path:
            return False
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def add_record(self, record: Dict[str, Any]) -> str:
        """
        添加记账记录
        
        Args:
            record: 记账记录
            
        Returns:
            记录ID
        """
        record_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        record["id"] = record_id
        record["created_at"] = datetime.now().isoformat()
        self.history.append(record)
        self.save_history()
        return record_id
    
    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        获取记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            记录或 None
        """
        for record in self.history:
            if record.get("id") == record_id:
                return record
        return None
    
    def get_recent_records(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的记录
        
        Args:
            limit: 数量限制
            
        Returns:
            记录列表
        """
        return self.history[-limit:][::-1]
    
    def get_records_by_date(self, date: str) -> List[Dict[str, Any]]:
        """
        获取指定日期的记录
        
        Args:
            date: 日期 (YYYY-MM-DD)
            
        Returns:
            记录列表
        """
        return [
            r for r in self.history
            if r.get("time", "").startswith(date)
        ]
    
    def get_records_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        获取指定分类的记录
        
        Args:
            category: 分类
            
        Returns:
            记录列表
        """
        return [r for r in self.history if r.get("category") == category]
    
    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        获取统计数据
        
        Args:
            days: 统计天数
            
        Returns:
            统计数据
        """
        now = datetime.now()
        start_date = now.replace(day=now.day - days).strftime("%Y-%m-%d")
        
        recent_records = [
            r for r in self.history
            if r.get("time", "") >= start_date
        ]
        
        # 总支出
        total_expense = sum(
            r.get("amount", 0)
            for r in recent_records
            if r.get("type") == "支出"
        )
        
        # 总收入
        total_income = sum(
            r.get("amount", 0)
            for r in recent_records
            if r.get("type") == "收入"
        )
        
        # 分类统计
        category_stats = {}
        for r in recent_records:
            cat = r.get("category", "其他")
            if cat not in category_stats:
                category_stats[cat] = {"count": 0, "amount": 0}
            category_stats[cat]["count"] += 1
            category_stats[cat]["amount"] += r.get("amount", 0)
        
        return {
            "period_days": days,
            "total_records": len(recent_records),
            "total_expense": total_expense,
            "total_income": total_income,
            "net": total_income - total_expense,
            "category_stats": category_stats
        }
    
    def delete_record(self, record_id: str) -> bool:
        """
        删除记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            是否成功
        """
        for i, record in enumerate(self.history):
            if record.get("id") == record_id:
                self.history.pop(i)
                self.save_history()
                return True
        return False
    
    def clear_history(self) -> None:
        """清空历史"""
        self.history = []
        self.save_history()


class FailedRecordManager:
    """失败记录管理"""
    
    def __init__(self, failed_path: Optional[str] = None):
        """
        初始化失败记录管理
        
        Args:
            failed_path: 失败记录文件路径
        """
        self.failed_path = failed_path
        self.failed_records: List[Dict[str, Any]] = []
        self._load_failed()
    
    def _load_failed(self) -> None:
        """加载失败记录"""
        if self.failed_path and os.path.exists(self.failed_path):
            try:
                with open(self.failed_path, 'r', encoding='utf-8') as f:
                    self.failed_records = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.failed_records = []
    
    def save_failed(self) -> bool:
        """保存失败记录"""
        if not self.failed_path:
            return False
        try:
            os.makedirs(os.path.dirname(self.failed_path), exist_ok=True)
            with open(self.failed_path, 'w', encoding='utf-8') as f:
                json.dump(self.failed_records, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def add_failed(self, record: Dict[str, Any], error: str) -> str:
        """
        添加失败记录
        
        Args:
            record: 记账记录
            error: 错误信息
            
        Returns:
            记录ID
        """
        record_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        failed_record = {
            "id": record_id,
            "record": record,
            "error": error,
            "failed_at": datetime.now().isoformat(),
            "retry_count": 0
        }
        self.failed_records.append(failed_record)
        self.save_failed()
        return record_id
    
    def get_failed_records(self) -> List[Dict[str, Any]]:
        """获取所有失败记录"""
        return self.failed_records
    
    def remove_failed(self, record_id: str) -> bool:
        """移除失败记录"""
        for i, r in enumerate(self.failed_records):
            if r.get("id") == record_id:
                self.failed_records.pop(i)
                self.save_failed()
                return True
        return False
    
    def increment_retry(self, record_id: str) -> None:
        """增加重试次数"""
        for r in self.failed_records:
            if r.get("id") == record_id:
                r["retry_count"] = r.get("retry_count", 0) + 1
                r["last_retry_at"] = datetime.now().isoformat()
                self.save_failed()
                break
