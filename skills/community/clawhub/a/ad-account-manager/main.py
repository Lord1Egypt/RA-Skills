#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广告账户管理 Skill 主入口
提供交互式命令行界面
"""

import asyncio
import sys
from ad_manager import AdAccountManager, Platform, AccountType
from browser_helper import BrowserHelper


class AdAccountSkill:
    """广告账户管理 Skill"""

    def __init__(self):
        self.manager = AdAccountManager()
        self.browser = None

    async def _init_browser(self):
        """初始化浏览器"""
        if not self.browser:
            self.browser = BrowserHelper(headless=False)
            await self.browser.start()

    async def close(self):
        """关闭资源"""
        if self.browser:
            await self.browser.close()

    async def handle_manage_ad_accounts(self):
        """处理管理广告账户请求"""
        print("请选择要管理的广告平台：")
        print("1. 广点通")
        print("2. 巨量引擎")
        
        choice = input("请输入选项 (1/2): ").strip()
        
        if choice == "1":
            await self.handle_guangdiantong()
        elif choice == "2":
            await self.handle_juliang()
        else:
            print("无效选项")

    async def handle_guangdiantong(self):
        """处理广点通账户"""
        print("\n请选择账户类型：")
        print("1. 广告主后台")
        print("2. 服务商后台")
        
        choice = input("请输入选项 (1/2): ").strip()
        
        account_type = AccountType.ADVERTISER if choice == "1" else AccountType.AGENCY
        login_url = self.manager.get_platform_login_url(Platform.GUANGDIANTONG, account_type)
        
        print(f"\n即将打开登录页面：{login_url}")
        await self._init_browser()
        
        # 打开登录页面等待扫码
        cookies = await self.browser.navigate_and_wait_for_login(login_url, timeout=300)
        
        if cookies:
            account_name = input("\n请输入账户名称：").strip()
            account_id = self.manager.add_account(
                Platform.GUANGDIANTONG,
                account_type,
                account_name,
                cookies
            )
            print(f"\n账户添加成功！账户ID: {account_id}")

    async def handle_juliang(self):
        """处理巨量引擎账户"""
        login_url = self.manager.get_platform_login_url(Platform.JULIANG)
        
        print(f"\n即将打开登录页面：{login_url}")
        await self._init_browser()
        
        # 打开登录页面等待扫码
        cookies = await self.browser.navigate_and_wait_for_login(login_url, timeout=300)
        
        if cookies:
            account_name = input("\n请输入账户名称：").strip()
            account_id = self.manager.add_account(
                Platform.JULIANG,
                AccountType.ADVERTISER,
                account_name,
                cookies
            )
            print(f"\n账户添加成功！账户ID: {account_id}")

    async def handle_one_click_login(self):
        """一键登录账户"""
        accounts = self.manager.list_accounts()
        
        if not accounts:
            print("没有已保存的账户")
            return
        
        print("\n请选择要登录的账户：")
        for i, account in enumerate(accounts, 1):
            platform_name = "广点通" if account.platform == "guangdiantong" else "巨量引擎"
            type_name = "广告主" if account.account_type == "advertiser" else "服务商"
            print(f"{i}. {account.name} ({platform_name} - {type_name})")
        
        choice = input("\n请输入选项: ").strip()
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(accounts):
                account = accounts[index]
                login_url = self.manager.get_platform_login_url(
                    Platform(account.platform),
                    AccountType(account.account_type)
                )
                
                print(f"\n正在登录: {account.name}")
                await self._init_browser()
                success = await self.browser.login_with_cookies(login_url, account.cookies)
                
                if success:
                    print("登录成功！浏览器已打开")
                    # 更新最后使用时间
                    self.manager.update_account_cookies(account.id, account.cookies)
            else:
                print("无效选项")
        except ValueError:
            print("无效输入")

    async def handle_account_overview(self):
        """账户状态总览"""
        overview = self.manager.get_accounts_overview()
        
        if not overview:
            print("没有已保存的账户")
            return
        
        print("\n===== 账户状态总览 =====")
        for item in overview:
            platform_name = "广点通" if item["platform"] == "guangdiantong" else "巨量引擎"
            status_emoji = "🔴" if item["is_abnormal"] else "🟢"
            
            print(f"\n{status_emoji} {item['name']} ({platform_name})")
            print(f"   余额: ¥{item['balance']:.2f}")
            print(f"   当日消耗: ¥{item['daily_cost']:.2f}")
            print(f"   预算: ¥{item['budget']:.2f}")
            print(f"   状态: {item['status']}")
            
            if item["is_abnormal"]:
                print("   ⚠️  异常提醒：余额不足或状态异常！")

    async def run(self):
        """运行主循环"""
        while True:
            print("\n===== 广告账户管理 =====")
            print("1. 管理广告账户（扫码登录）")
            print("2. 一键登录账户")
            print("3. 账户状态总览")
            print("4. 退出")
            
            choice = input("\n请输入选项 (1-4): ").strip()
            
            if choice == "1":
                await self.handle_manage_ad_accounts()
            elif choice == "2":
                await self.handle_one_click_login()
            elif choice == "3":
                await self.handle_account_overview()
            elif choice == "4":
                await self.close()
                print("再见！")
                break
            else:
                print("无效选项")


async def main():
    """主函数"""
    skill = AdAccountSkill()
    try:
        await skill.run()
    except KeyboardInterrupt:
        await skill.close()
        print("\n再见！")


if __name__ == "__main__":
    asyncio.run(main())
