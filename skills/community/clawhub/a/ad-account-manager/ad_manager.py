#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广告账户管理核心模块
实现Cookie登录、账户管理和状态查看功能
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Platform(Enum):
    """广告平台枚举"""
    GUANGDIANTONG = "guangdiantong"  # 广点通
    JULIANG = "juliang"  # 巨量引擎


class AccountType(Enum):
    """账户类型枚举"""
    ADVERTISER = "advertiser"  # 广告主
    AGENCY = "agency"  # 服务商


@dataclass
class AdAccount:
    """广告账户数据结构"""
    id: str
    platform: str
    account_type: str
    name: str
    cookies: List[Dict]
    created_at: float
    last_used: float
    balance: float = 0.0
    daily_cost: float = 0.0
    budget: float = 0.0
    status: str = "normal"  # normal, warning, error


class AdAccountManager:
    """广告账户管理器"""

    def __init__(self, storage_dir: Optional[str] = None):
        """
        初始化账户管理器
        
        Args:
            storage_dir: 存储目录，默认为当前目录下的data文件夹
        """
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), "data")
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.accounts_file = self.storage_dir / "accounts.json"
        self.accounts: Dict[str, AdAccount] = {}
        
        # 加载已保存的账户
        self._load_accounts()

    def _load_accounts(self):
        """从文件加载账户数据"""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for account_id, account_data in data.items():
                        self.accounts[account_id] = AdAccount(**account_data)
            except Exception as e:
                print(f"加载账户数据失败: {e}")

    def _save_accounts(self):
        """保存账户数据到文件"""
        data = {}
        for account_id, account in self.accounts.items():
            data[account_id] = asdict(account)
        
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_platform_login_url(self, platform: Platform, account_type: Optional[AccountType] = None) -> str:
        """
        获取平台登录URL
        
        Args:
            platform: 广告平台
            account_type: 账户类型（仅广点通需要）
            
        Returns:
            登录URL
        """
        if platform == Platform.GUANGDIANTONG:
            if account_type == AccountType.AGENCY:
                return "https://e.qq.com/agency"
            return "https://e.qq.com/ads"
        elif platform == Platform.JULIANG:
            return "https://ad.oceanengine.com"
        return ""

    def add_account(self, platform: Platform, account_type: AccountType, 
                    name: str, cookies: List[Dict]) -> str:
        """
        添加新账户
        
        Args:
            platform: 广告平台
            account_type: 账户类型
            name: 账户名称
            cookies: Cookie列表
            
        Returns:
            账户ID
        """
        account_id = f"{platform.value}_{account_type.value}_{int(time.time())}"
        
        account = AdAccount(
            id=account_id,
            platform=platform.value,
            account_type=account_type.value,
            name=name,
            cookies=cookies,
            created_at=time.time(),
            last_used=time.time()
        )
        
        self.accounts[account_id] = account
        self._save_accounts()
        
        return account_id

    def get_account(self, account_id: str) -> Optional[AdAccount]:
        """获取指定账户"""
        return self.accounts.get(account_id)

    def list_accounts(self) -> List[AdAccount]:
        """列出所有账户"""
        return list(self.accounts.values())

    def update_account_cookies(self, account_id: str, cookies: List[Dict]) -> bool:
        """更新账户Cookie"""
        if account_id in self.accounts:
            self.accounts[account_id].cookies = cookies
            self.accounts[account_id].last_used = time.time()
            self._save_accounts()
            return True
        return False

    def delete_account(self, account_id: str) -> bool:
        """删除账户"""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self._save_accounts()
            return True
        return False

    def update_account_status(self, account_id: str, balance: float, 
                              daily_cost: float, budget: float, status: str):
        """更新账户状态信息"""
        if account_id in self.accounts:
            account = self.accounts[account_id]
            account.balance = balance
            account.daily_cost = daily_cost
            account.budget = budget
            account.status = status
            account.last_used = time.time()
            self._save_accounts()

    def get_accounts_overview(self) -> List[Dict[str, Any]]:
        """获取所有账户总览信息"""
        overview = []
        for account in self.accounts.values():
            # 判断是否为异常账户
            is_abnormal = False
            if account.balance < 100 or account.status in ["error", "rejected"]:
                is_abnormal = True
            
            overview.append({
                "id": account.id,
                "name": account.name,
                "platform": account.platform,
                "account_type": account.account_type,
                "balance": account.balance,
                "daily_cost": account.daily_cost,
                "budget": account.budget,
                "status": account.status,
                "is_abnormal": is_abnormal,
                "last_used": account.last_used
            })
        return overview
