#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firecrawl 自动认证模块
使用免费 API 密钥或环境变量自动完成认证
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirecrawlAutoAuth:
    """Firecrawl 自动认证器"""

    def __init__(self):
        self.cli_path = self._find_firecrawl_cli()
        self.config_dir = Path.home() / ".firecrawl"
        self.config_file = self.config_dir / "config.json"

    def _find_firecrawl_cli(self) -> Optional[str]:
        """查找 firecrawl CLI 路径"""
        # 尝试常见路径
        possible_paths = [
            Path.home() / ".npm-global" / "bin" / "firecrawl",
            Path.home() / "node_modules" / ".bin" / "firecrawl",
            Path("C:\\Users\\fj\\AppData\\Roaming\\npm\\firecrawl.cmd"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # 尝试在 PATH 中查找
        try:
            result = subprocess.run(
                ["where", "firecrawl"] if sys.platform == "win32" else ["which", "firecrawl"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split("\n")[0]
        except:
            pass
        
        return None

    def check_status(self) -> Dict:
        """检查 Firecrawl 状态"""
        if not self.cli_path:
            return {
                "installed": False,
                "authenticated": False,
                "error": "Firecrawl CLI 未安装"
            }
        
        try:
            result = subprocess.run(
                [self.cli_path, "--status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout
            
            return {
                "installed": True,
                "authenticated": "Authenticated" in output or "Not authenticated" not in output,
                "raw_output": output,
                "credits": self._extract_credits(output),
                "error": None
            }
            
        except Exception as e:
            return {
                "installed": True,
                "authenticated": False,
                "error": str(e)
            }

    def _extract_credits(self, output: str) -> Optional[int]:
        """从输出中提取信用额度"""
        try:
            import re
            match = re.search(r"Credits: ([\d,]+)", output)
            if match:
                return int(match.group(1).replace(",", ""))
        except:
            pass
        return None

    def auto_auth(self) -> bool:
        """
        自动认证
        
        尝试以下方式:
        1. 检查环境变量 FIRECRAWL_API_KEY
        2. 使用免费 API 密钥 (如果有)
        3. 引导用户进行浏览器认证
        """
        # 1. 检查环境变量
        api_key = os.environ.get("FIRECRAWL_API_KEY")
        
        if api_key:
            logger.info("检测到 FIRECRAWL_API_KEY 环境变量")
            return self._set_api_key(api_key)
        
        # 2. 检查配置文件
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    if config.get("apiKey"):
                        logger.info("检测到配置文件中的 API 密钥")
                        return True
            except:
                pass
        
        # 3. 尝试使用免费 API 密钥
        free_key = self._get_free_api_key()
        if free_key:
            logger.info("使用免费 API 密钥")
            return self._set_api_key(free_key)
        
        # 4. 引导浏览器认证
        logger.info("启动浏览器认证...")
        return self._browser_auth()

    def _set_api_key(self, api_key: str) -> bool:
        """设置 API 密钥"""
        try:
            # 创建配置目录
            self.config_dir.mkdir(exist_ok=True)
            
            # 写入配置
            config = {
                "apiKey": api_key,
                "apiUrl": "https://api.firecrawl.dev"
            }
            
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"API 密钥已保存至 {self.config_file}")
            
            # 验证
            status = self.check_status()
            return status.get("authenticated", False)
            
        except Exception as e:
            logger.error(f"设置 API 密钥失败：{e}")
            return False

    def _get_free_api_key(self) -> Optional[str]:
        """
        获取免费 API 密钥
        
        注意：这里可以集成一些提供免费额度的服务
        目前返回 None，需要用户自行获取
        """
        # 可以在这里添加获取免费 API 密钥的逻辑
        # 例如：某些服务提供免费的开发者密钥
        return None

    def _browser_auth(self) -> bool:
        """浏览器认证"""
        try:
            if not self.cli_path:
                logger.error("Firecrawl CLI 未找到")
                return False
            
            # 启动认证
            result = subprocess.run(
                [self.cli_path, "login", "--browser"],
                timeout=120
            )
            
            if result.returncode == 0:
                logger.info("认证成功")
                return True
            else:
                logger.error("认证失败")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("认证超时")
            return False
        except Exception as e:
            logger.error(f"认证过程出错：{e}")
            return False

    def get_usage(self) -> Optional[Dict]:
        """获取使用量信息"""
        if not self.cli_path:
            return None
        
        try:
            result = subprocess.run(
                [self.cli_path, "credit-usage", "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        
        return None


def setup_firecrawl() -> bool:
    """
    一键设置 Firecrawl
    
    Returns:
        bool: 设置是否成功
    """
    print("=" * 60)
    print("Firecrawl 自动设置向导")
    print("=" * 60)
    
    auth = FirecrawlAutoAuth()
    
    # 检查安装
    status = auth.check_status()
    
    if not status.get("installed"):
        print("\n❌ Firecrawl CLI 未安装")
        print("请先运行：npm install -g firecrawl-cli")
        return False
    
    print("\n✓ Firecrawl CLI 已安装")
    
    if status.get("authenticated"):
        print("✓ 已认证")
        if status.get("credits"):
            print(f"  可用额度：{status['credits']}")
        return True
    
    print("⚠ 未认证")
    print("\n开始自动认证...")
    
    if auth.auto_auth():
        print("\n✓ 认证成功!")
        new_status = auth.check_status()
        if new_status.get("credits"):
            print(f"  可用额度：{new_status['credits']}")
        return True
    else:
        print("\n❌ 认证失败")
        print("\n手动认证方法:")
        print("1. 访问 https://www.firecrawl.dev/app")
        print("2. 注册/登录账户")
        print("3. 获取 API 密钥")
        print("4. 设置环境变量：setx FIRECRAWL_API_KEY \"your-key\"")
        return False


if __name__ == "__main__":
    success = setup_firecrawl()
    sys.exit(0 if success else 1)
