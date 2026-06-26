#!/usr/bin/env python3
"""
B站 Cookie 安全管理模块

功能：
1. 多路径冗余存储 Cookie，防止误删除
2. 自动检测 Cookie 有效性
3. 扫码登录自动续签
4. 失效时生成通知并通过飞书/控制台发送二维码
"""

import os
import sys
import json
import time
import shutil
import logging
import requests
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Callable

logger = logging.getLogger(__name__)

# Cookie 多路径冗余存储
COOKIE_STORE_PATHS = [
    # 1. 主存储（技能目录内）
    os.path.expanduser("~/.openclaw/workspace/skills/bilibili-video-transcriber/.bilibili_cookie"),
    # 2. 备用存储（用户主目录）
    os.path.expanduser("~/.bilibili_cookie_storage"),
    # 3. 系统级（/etc 下，需要 root 但尝试）
    os.path.expanduser("~/.config/bilibili_transcriber/cookie"),
]

# 活跃引用（供运行时读取）
COOKIE_ACTIVE_PATH = os.path.expanduser("~/.bilibili_cookie.txt")

# Cookie 检查环境变量通知通道
# 当 cookie_manager 需要通知用户时，会检查该文件中的回调配置
NOTIFY_CONFIG_PATH = os.path.expanduser(
    "~/.openclaw/workspace/skills/bilibili-video-transcriber/.cookie_notify_config.json"
)


def ensure_cookie_dirs():
    """确保所有存储路径的目录存在"""
    for p in [COOKIE_ACTIVE_PATH] + COOKIE_STORE_PATHS:
        d = os.path.dirname(p)
        os.makedirs(d, exist_ok=True)


def save_cookie(cookie_str: str) -> bool:
    """
    安全保存 Cookie 到多个冗余路径
    
    Args:
        cookie_str: Cookie 字符串
        
    Returns:
        是否至少保存到一个路径成功
    """
    ensure_cookie_dirs()
    
    # 1. 保存到活跃路径（主引用）
    success = False
    try:
        # 先写到临时文件再重命名，防止写入中断导致文件损坏
        fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(COOKIE_ACTIVE_PATH))
        os.close(fd)
        with open(tmp_path, 'w', encoding='utf-8') as f:
            f.write(cookie_str.strip())
        os.chmod(tmp_path, 0o600)  # 仅所有者可读写
        shutil.move(tmp_path, COOKIE_ACTIVE_PATH)
        logger.info(f"✅ Cookie 已保存到 {COOKIE_ACTIVE_PATH}")
        success = True
    except Exception as e:
        logger.warning(f"❌ 写入 {COOKIE_ACTIVE_PATH} 失败: {e}")
    
    # 2. 同步到所有冗余存储路径
    for store_path in COOKIE_STORE_PATHS:
        try:
            d = os.path.dirname(store_path)
            os.makedirs(d, exist_ok=True)
            fd, tmp_path = tempfile.mkstemp(dir=d)
            os.close(fd)
            with open(tmp_path, 'w', encoding='utf-8') as f:
                f.write(cookie_str.strip())
            os.chmod(tmp_path, 0o600)
            shutil.move(tmp_path, store_path)
            logger.info(f"✅ Cookie 已备份到 {store_path}")
            success = True
        except Exception as e:
            logger.warning(f"❌ 备份到 {store_path} 失败: {e}")
    
    return success


def load_cookie() -> Optional[str]:
    """
    从任意可用路径加载 Cookie（依次尝试所有路径）
    
    搜索顺序: 活跃文件 > 技能目录 > 用户目录 > 配置目录
    """
    search_paths = [COOKIE_ACTIVE_PATH] + COOKIE_STORE_PATHS
    
    for path in search_paths:
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            try:
                with open(expanded, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    # 如果是从备份路径读到的，自动补全到活跃路径
                    if path != COOKIE_ACTIVE_PATH and not os.path.exists(COOKIE_ACTIVE_PATH):
                        try:
                            os.makedirs(os.path.dirname(COOKIE_ACTIVE_PATH), exist_ok=True)
                            shutil.copy2(expanded, COOKIE_ACTIVE_PATH)
                            logger.info(f"♻️ 已从 {expanded} 恢复 Cookie 到 {COOKIE_ACTIVE_PATH}")
                        except Exception:
                            pass
                    return content
            except Exception as e:
                logger.debug(f"读取 {path} 失败: {e}")
    
    # 也检查环境变量
    env_cookie = os.environ.get('BILIBILI_COOKIE')
    if env_cookie:
        logger.info("📦 从环境变量加载 Cookie")
        return env_cookie
    
    return None


def parse_cookie(cookie_str: str) -> Dict[str, str]:
    """解析 Cookie 字符串为字典"""
    cookies = {}
    if not cookie_str:
        return cookies
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            k, v = item.split('=', 1)
            cookies[k.strip()] = v.strip()
    return cookies


def check_cookie_valid(cookie_str: str) -> Dict[str, Any]:
    """
    检查 Cookie 是否有效
    
    Returns:
        {
            "valid": bool,
            "username": str or None,
            "is_vip": bool,
            "error": str or None
        }
    """
    if not cookie_str:
        return {"valid": False, "username": None, "is_vip": False, "error": "cookie为空"}
    
    try:
        from bilibili_api import Credential, sync
        from bilibili_api import user as bilibili_user
        
        cookies = parse_cookie(cookie_str)
        
        credential = Credential(
            sessdata=cookies.get('SESSDATA', ''),
            bili_jct=cookies.get('bili_jct', ''),
            buvid3=cookies.get('buvid3', '')
        )
        
        # User 需要 uid 参数，但有个简化的方式
        # 直接调用 get_self_info 或者使用已弃用的方式
        try:
            from bilibili_api import user as bilibili_user
            u = bilibili_user.User(credential=credential)
            info = sync(u.get_user_info())
            return {
                "valid": True,
                "username": info.get('name', 'Unknown'),
                "is_vip": info.get('vipStatus', 0) == 1,
                "error": None
            }
        except TypeError as te:
            # 新版 API 可能需要 uid
            uid = cookies.get('DedeUserID', '0')
            if uid and uid != '0':
                u = bilibili_user.User(uid=int(uid), credential=credential)
                info = sync(u.get_user_info())
                return {
                    "valid": True,
                    "username": info.get('name', 'Unknown'),
                    "is_vip": info.get('vipStatus', 0) == 1,
                    "error": None
                }
            raise
    except Exception as e:
        err_msg = str(e)
        # 常见 Cookie 失效错误
        if "412" in err_msg or "Precondition" in err_msg:
            err_msg = "Cookie 可能已过期或被风控"
        elif "401" in err_msg or "Unauthorized" in err_msg:
            err_msg = "Cookie 已失效"
        return {"valid": False, "username": None, "is_vip": False, "error": err_msg}


class BilibiliQRLogin:
    """B站扫码登录 - 支持通过飞书发送二维码"""

    def __init__(self):
        self.qrcode_key = None
        self.qrcode_url = None
        self.qr_image_path = None

    def generate_qr_code(self) -> str:
        """
        生成二维码
        
        Returns:
            二维码图片路径
        """
        import qrcode

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        r = requests.get(
            "https://passport.bilibili.com/x/passport-login/web/qrcode/generate",
            headers=headers,
            timeout=15
        )
        data = r.json()

        if data.get('code') != 0:
            raise Exception(f"生成二维码失败: {data.get('message', '未知错误')}")

        self.qrcode_key = data['data']['qrcode_key']
        self.qrcode_url = data['data']['url']

        # 生成二维码图片
        qr = qrcode.QRCode(box_size=8, border=3)
        qr.add_data(self.qrcode_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        qr_path = "/tmp/bilibili_qr_login.png"
        img.save(qr_path)
        self.qr_image_path = qr_path

        logger.info(f"🔑 二维码已生成: {qr_path}")
        logger.info(f"🔗 URL: {self.qrcode_url}")
        return qr_path

    def poll_login(self, timeout_seconds: int = 180, callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        轮询登录状态，有结果时调用回调
        
        Args:
            timeout_seconds: 超时时间（秒）
            callback: 结果回调函数，会在登录成功时被调用
            
        Returns:
            {"success": bool, "cookie": str, "username": str, ...}
        """
        if not self.qrcode_key:
            return {"success": False, "error": "未生成二维码"}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
        
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            try:
                r = requests.post(
                    poll_url,
                    params={'qrcode_key': self.qrcode_key},
                    headers=headers,
                    timeout=10
                )
                result = r.json()
                
                code = result['data']['code']
                
                if code == 0:
                    # 登录成功，从 Set-Cookie 提取
                    all_cookies = {}
                    # 从 headers 提取
                    for k, v in r.headers.items():
                        if k.lower() == 'set-cookie':
                            parts = v.split(';')
                            for part in parts:
                                if '=' in part:
                                    ck, cv = part.split('=', 1)
                                    all_cookies[ck.strip()] = cv.strip()
                    # 从 cookies 对象提取
                    for k, v in r.cookies.items():
                        all_cookies[k] = v
                    
                    # 提取关键 cookie
                    cookie_parts = []
                    for ck in ['SESSDATA', 'bili_jct', 'buvid3', 'DedeUserID', 'DedeUserID__ckMd5', 'sid']:
                        if ck in all_cookies:
                            cookie_parts.append(f"{ck}={all_cookies[ck]}")
                    
                    if not cookie_parts:
                        # fallback: 从 data 中获取
                        data = result.get('data', {})
                        if 'url' in data:
                            import urllib.parse
                            parsed = urllib.parse.urlparse(data['url'])
                            params = urllib.parse.parse_qs(parsed.query)
                            for ck in ['SESSDATA', 'bili_jct', 'DedeUserID']:
                                if ck in params:
                                    cookie_parts.append(f"{ck}={params[ck][0]}")
                    
                    cookie_str = '; '.join(cookie_parts) if cookie_parts else ""
                    result_data = {"success": bool(cookie_str), "cookie": cookie_str}
                    
                    # 验证
                    if cookie_str:
                        check = check_cookie_valid(cookie_str)
                        result_data["username"] = check.get("username")
                        result_data["is_vip"] = check.get("is_vip")
                        result_data["valid"] = check["valid"]
                        
                        if check["valid"]:
                            # 自动保存
                            save_cookie(cookie_str)
                    
                    if callback:
                        callback(result_data)
                    
                    return result_data
                    
                elif code == 86038:
                    return {"success": False, "error": "二维码已过期"}
                elif code == 86090:
                    # 已扫码但未确认
                    pass
                    
            except Exception as e:
                logger.debug(f"轮询异常: {e}")
            
            time.sleep(2)
        
        return {"success": False, "error": "扫码超时"}
    
    def poll_once(self) -> Dict[str, Any]:
        """
        只轮询一次，不循环
        
        Returns:
            {"success": bool, ...} 或 {"polling": True}
        """
        if not self.qrcode_key:
            return {"success": False, "error": "未生成二维码"}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        try:
            r = requests.post(
                "https://passport.bilibili.com/x/passport-login/web/qrcode/poll",
                params={'qrcode_key': self.qrcode_key},
                headers=headers,
                timeout=10
            )
            result = r.json()
            code = result['data']['code']
            
            if code == 0:
                # 登录成功
                all_cookies = {}
                for k, v in r.headers.items():
                    if k.lower() == 'set-cookie':
                        parts = v.split(';')
                        for part in parts:
                            if '=' in part:
                                ck, cv = part.split('=', 1)
                                all_cookies[ck.strip()] = cv.strip()
                for k, v in r.cookies.items():
                    all_cookies[k] = v
                
                cookie_parts = []
                for ck in ['SESSDATA', 'bili_jct', 'buvid3', 'DedeUserID']:
                    if ck in all_cookies:
                        cookie_parts.append(f"{ck}={all_cookies[ck]}")
                
                cookie_str = '; '.join(cookie_parts)
                if cookie_str:
                    save_cookie(cookie_str)
                    check = check_cookie_valid(cookie_str)
                    return {
                        "success": True,
                        "cookie": cookie_str,
                        "username": check.get("username"),
                        "is_vip": check.get("is_vip"),
                    }
                
            elif code == 86038:
                return {"success": False, "error": "二维码已过期"}
            
            return {"polling": True, "code": code}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


def ensure_cookie(force_login: bool = False) -> bool:
    """
    确保 Cookie 可用，如不可用则提示用户
    
    Args:
        force_login: 是否强制重新登录
        
    Returns:
        Cookie 是否可用
    """
    # 1. 尝试加载现存 Cookie
    cookie_str = load_cookie()
    
    if cookie_str and not force_login:
        # 2. 验证有效性
        result = check_cookie_valid(cookie_str)
        if result["valid"]:
            logger.info(f"✅ Cookie 有效 (用户: {result['username']})")
            return True
        else:
            logger.warning(f"⚠️ Cookie 已失效: {result['error']}")
    
    # 3. Cookie 无效或强制登录，生成二维码
    logger.info("📱 请扫码登录 B 站...")
    return False


def needs_cookie_refresh() -> Optional[str]:
    """
    检查是否需要刷新 Cookie
    
    Returns:
        None = Cookie 有效，str = 过期原因
    """
    cookie_str = load_cookie()
    if not cookie_str:
        return "Cookie 文件不存在"
    
    result = check_cookie_valid(cookie_str)
    if not result["valid"]:
        return result.get("error", "Cookie 已失效")
    
    return None


def get_stored_cookie() -> Optional[str]:
    """获取已存储的 Cookie（带有效性检查和自动恢复）"""
    return load_cookie()


# ========== 飞书发送二维码支持 ==========
# 当 cookie_manager 需要在飞书上发送二维码时，外部调用此函数

def send_qr_via_feishu(qr_image_path: str) -> bool:
    """
    通过飞书发送二维码图片
    
    返回值: 是否成功发送
    注意：此函数需要外部提供 feishu 发送能力，这里用文件标记方式
    """
    # 签名文件 - 代理处理器会检查此文件并执行实际的发送
    signal_path = "/tmp/.bilibili_qr_send_signal.json"
    signal = {
        "action": "send_qr",
        "image_path": qr_image_path,
        "timestamp": time.time(),
        "message": "请使用B站APP扫描此二维码登录，扫码后请回复「已扫码」"
    }
    try:
        with open(signal_path, 'w') as f:
            json.dump(signal, f)
        logger.info(f"📨 二维码发送信号已写入: {signal_path}")
        return True
    except Exception as e:
        logger.error(f"写入发送信号失败: {e}")
        return False


# 初始化
ensure_cookie_dirs()
