#!/usr/bin/env python3
"""
Clash Auto Switch - 跨平台版本
支持: Linux, macOS, Windows
"""

import os
import sys
import json
import time
import argparse
from typing import List, Dict, Any, Optional

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)


class ClashAutoSwitch:
    """Clash 代理自动切换工具"""
    
    def __init__(self, api_url: str, secret: str, proxy_url: str = "http://127.0.0.1:7890"):
        self.api_url = api_url.rstrip('/')
        self.secret = secret
        self.proxy_url = proxy_url
        self.headers = {"Authorization": f"Bearer {secret}"}
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """发送 API 请求"""
        url = f"{self.api_url}{endpoint}"
        try:
            if method.upper() == "GET":
                r = requests.get(url, headers=self.headers, timeout=10, **kwargs)
            elif method.upper() == "PUT":
                r = requests.put(url, headers=self.headers, timeout=10, **kwargs)
            else:
                return None
            return r.json() if r.status_code in [200, 204] else None
        except Exception as e:
            print(f"请求错误: {e}")
            return None
    
    def get_proxies(self) -> Dict[str, Any]:
        """获取所有代理"""
        return self._request("GET", "/proxies") or {}
    
    def get_proxy_group(self, name: str) -> Dict[str, Any]:
        """获取代理组详情"""
        return self._request("GET", f"/proxies/{name}") or {}
    
    def set_proxy(self, group: str, node: str) -> bool:
        """切换节点"""
        result = self._request("PUT", f"/proxies/{group}", json={"name": node})
        return result is not None
    
    def test_delay(self, node: str) -> int:
        """测试节点延迟"""
        encoded = requests.utils.quote(node)
        url = f"{self.api_url}/proxies/{encoded}/delay?timeout=5000&url=http://www.gstatic.com/generate_204"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            data = r.json()
            return data.get("delay", 99999)
        except:
            return 99999
    
    def health_check(self, targets: List[str]) -> tuple:
        """健康检查"""
        success = 0
        proxies = {"http": self.proxy_url, "https": self.proxy_url}
        
        for target in targets:
            try:
                r = requests.get(target, proxies=proxies, timeout=5)
                if r.status_code < 500:
                    success += 1
            except:
                pass
        
        return success, len(targets)
    
    def list_groups(self) -> Dict[str, str]:
        """列出所有代理组"""
        data = self.get_proxies()
        groups = {}
        for name, info in data.get("proxies", {}).items():
            if info.get("type") == "Selector":
                groups[name] = info.get("now", "未知")
        return groups
    
    def auto_switch(self, preferred_regions: List[str] = None, test_targets: List[str] = None) -> bool:
        """自动切换到最佳节点"""
        if test_targets is None:
            test_targets = [
                "https://api.telegram.org",
                "https://api.anthropic.com", 
                "https://www.google.com"
            ]
        
        # 健康检查
        success, total = self.health_check(test_targets)
        rate = success * 100 // total
        print(f"健康度: {success}/{total} ({rate}%)")
        
        if rate >= 60:
            print("✓ 代理健康，无需切换")
            return True
        
        print("✗ 代理不健康，开始自动切换...")
        
        # 找最佳节点
        best_node = None
        best_delay = 99999
        
        groups = self.list_groups()
        for group, current in groups.items():
            if current == "节点选择":
                info = self.get_proxy_group(group)
                nodes = info.get("all", [])
                
                for node in nodes:
                    if node == "节点选择":
                        continue
                    
                    delay = self.test_delay(node)
                    print(f"  {node}: {delay}ms")
                    
                    # 检查是否优先区域
                    is_preferred = any(r.lower() in node.lower() for r in (preferred_regions or []))
                    
                    if is_preferred and delay < best_delay:
                        best_node = node
                        best_delay = delay
                    elif not best_node and delay < best_delay:
                        best_node = node
                        best_delay = delay
                
                if best_node:
                    print(f"切换到: {best_node} ({best_delay}ms)")
                    self.set_proxy(group, best_node)
        
        return best_node is not None


def main():
    parser = argparse.ArgumentParser(description="Clash Auto Switch")
    parser.add_argument("--api", "-a", default="http://127.0.0.1:58871", help="Clash API 地址")
    parser.add_argument("--secret", "-s", default="", help="API 密钥")
    parser.add_argument("--proxy", "-p", default="http://127.0.0.1:7890", help="代理地址")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有代理组")
    parser.add_argument("--check", "-c", action="store_true", help="健康检查")
    parser.add_argument("--auto", action="store_true", help="自动切换")
    parser.add_argument("--group", "-g", help="指定代理组")
    parser.add_argument("--node", "-n", help="切换到指定节点")
    
    args = parser.parse_args()
    
    # 如果没有提供 secret，从环境变量读取
    secret = args.secret or os.environ.get("CLASH_SECRET", "")
    if not secret:
        print("请提供 --secret 或设置 CLASH_SECRET 环境变量")
        sys.exit(1)
    
    clash = ClashAutoSwitch(args.api, secret, args.proxy)
    
    if args.list:
        print("========== 代理组 ==========")
        for group, current in clash.list_groups().items():
            print(f"{group}: {current}")
    
    elif args.check:
        clash.health_check([
            "https://api.telegram.org",
            "https://api.anthropic.com",
            "https://www.google.com"
        ])
    
    elif args.auto:
        clash.auto_switch()
    
    elif args.group and args.node:
        if clash.set_proxy(args.group, args.node):
            print(f"✓ 已切换 {args.group} -> {args.node}")
        else:
            print(f"✗ 切换失败")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
