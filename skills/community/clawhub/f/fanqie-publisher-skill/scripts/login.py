# -*- coding: utf-8 -*-
"""
番茄小说自动发布 - 登录模块
"""

import time
from browser import FanqieBrowser, get_browser
from config import SELECTORS, TIMEOUT, BASE_URL


class FanqieLogin:
    """番茄小说登录管理"""
    
    def __init__(self):
        self.browser: FanqieBrowser = get_browser()
    
    def login(self) -> dict:
        """
        执行登录流程
        
        Returns:
            dict: 登录结果
        """
        result = {
            "success": False,
            "message": "",
            "cookies_saved": False
        }
        
        try:
            # 浏览器会自动启动（通过属性访问）
            
            # 直接进入登录页面
            print("[登录] 正在打开登录页面...")
            self.browser.goto("https://fanqienovel.com/main/writer/login?enter_from=skill")
            
            # 等待用户扫码登录
            print("\n" + "="*50)
            print("请在浏览器窗口中扫码登录")
            print("支持扫码登录")
            print("="*50 + "\n")
            
            # 等待登录成功（检测跳转到作家专区或工作台）
            qr_result = self._wait_for_login()
            
            if qr_result["success"]:
                # 保存Cookie
                self.browser.save_cookies()
                result["success"] = True
                result["message"] = "登录成功！Cookie已保存，后续操作无需重复登录"
                result["cookies_saved"] = True
            else:
                result["message"] = qr_result["message"]
        
        except Exception as e:
            result["message"] = f"登录失败: {str(e)}"
            print(f"[登录] 错误: {e}")
        
        return result
    
    def _wait_for_login(self) -> dict:
        """
        等待用户扫码登录
        
        Returns:
            dict: 登录结果
        """
        result = {"success": False, "message": ""}
        
        try:
            # 等待登录成功（检测URL跳转或登录成功元素）
            print("[登录] 等待扫码登录中...")
            
            # 方法1: 等待URL跳转到工作台
            max_wait = 120  # 最长等待2分钟
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                current_url = self.browser.page.url
                
                # 检测是否跳转到作家专区或工作台
                if "writer/zone" in current_url and "login" not in current_url:
                    result["success"] = True
                    result["message"] = "扫码登录成功"
                    print("\n[登录] [OK] 检测到登录成功！")
                    return result
                
                # 检测页面上是否有"工作台"或用户信息
                try:
                    # 检查是否有用户头像或工作台入口
                    user_element = self.browser.page.query_selector("text=工作台")
                    if user_element:
                        result["success"] = True
                        result["message"] = "扫码登录成功"
                        print("\n[登录] [OK] 检测到登录成功！")
                        return result
                except:
                    pass
                
                time.sleep(1)
                # 显示等待进度
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0 and elapsed > 0:
                    print(f"[登录] 已等待 {elapsed} 秒...")
            
            result["message"] = "登录超时，请重新尝试"
            print("[登录] ✗ 登录超时")
        
        except Exception as e:
            result["message"] = f"登录检测失败: {str(e)}"
        
        return result
    
    def logout(self):
        """退出登录（清除Cookie）"""
        self.browser.clear_cookies()
        print("[登录] 已退出登录，Cookie已清除")
    
    def check_login_status(self) -> dict:
        """
        检查登录状态
        
        Returns:
            dict: 包含登录状态和信息
        """
        result = {
            "logged_in": False,
            "message": "",
            "cookie_file_exists": False
        }
        
        # 检查Cookie文件是否存在
        if not self.browser.cookie_path.exists():
            result["message"] = "未找到登录信息，请先执行登录"
            return result
        
        result["cookie_file_exists"] = True
        
        try:
            # 浏览器会自动启动
            
            # 加载Cookie
            if not self.browser.load_cookies():
                result["message"] = "Cookie加载失败，请重新登录"
                return result
            
            # 访问作品管理页面验证（这是正确的作品列表页面）
            self.browser.goto("https://fanqienovel.com/main/writer/book-manage")
            
            # 等待页面加载
            import time
            time.sleep(3)
            self.browser.page.wait_for_load_state("domcontentloaded", timeout=30000)
            
            # 检查是否跳转到登录页
            current_url = self.browser.page.url
            if "login" in current_url:
                result["message"] = "登录已过期，请重新登录"
                return result
            
            # 检查是否有作品列表元素
            try:
                # 检查作品卡片
                work_element = self.browser.page.query_selector(".long-article-table-item, .work-item, .book-item")
                if work_element:
                    result["logged_in"] = True
                    result["message"] = "登录状态有效"
                    return result
            except:
                pass
            
            # 检查是否有工作台元素
            try:
                work_panel = self.browser.page.query_selector("text=工作台")
                if work_panel:
                    result["logged_in"] = True
                    result["message"] = "登录状态有效"
                    return result
            except:
                pass
            
            # 如果URL在正确的页面，也认为登录有效
            if "book-manage" in current_url or "writer" in current_url:
                result["logged_in"] = True
                result["message"] = "登录状态有效（基于URL判断）"
                return result
            
            result["message"] = "登录状态未知，建议重新登录"
            
        except Exception as e:
            result["message"] = f"检查登录状态失败: {str(e)}"
        
        return result


def login():
    """登录入口函数"""
    login_manager = FanqieLogin()
    return login_manager.login()


def logout():
    """登出入口函数"""
    login_manager = FanqieLogin()
    login_manager.logout()


def check_login():
    """检查登录状态（简化版，返回布尔值）"""
    login_manager = FanqieLogin()
    result = login_manager.check_login_status()
    return result.get("logged_in", False)


def check_login_detail():
    """检查登录状态（详细版，返回完整信息）"""
    login_manager = FanqieLogin()
    return login_manager.check_login_status()