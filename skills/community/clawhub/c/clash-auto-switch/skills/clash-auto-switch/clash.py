#!/usr/bin/env python3
"""
Clash Auto Switch - OpenClaw Skill 实现
"""

import json
import os
import sys
import argparse
from typing import Optional, Dict, List, Tuple

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)


class ClashAutoSwitch:
    """Clash 代理自动切换工具"""
    
    def __init__(self, api_url: str = None, secret: str = None, proxy_url: str = None):
        self.api_url = api_url or os.environ.get("CLASH_API", "http://127.0.0.1:58871")
        self.secret = secret or os.environ.get("CLASH_SECRET", "")
        self.proxy_url = proxy_url or os.environ.get("CLASH_PROXY", "http://127.0.0.1:7890")
        
        if not self.secret:
            print("错误: 请设置 CLASH_SECRET 环境变量或提供 --secret 参数")
            sys.exit(1)
            
        self.headers = {"Authorization": f"Bearer {self.secret}"}
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """发送 API 请求"""
        url = f"{self.api_url.rstrip('/')}{endpoint}"
        try:
            if method.upper() == "GET":
                r = requests.get(url, headers=self.headers, timeout=10, **kwargs)
            elif method.upper() == "PUT":
                r = requests.put(url, headers=self.headers, timeout=10, **kwargs)
            else:
                return None
            return r.json() if r.status_code in [200, 204] else None
        except Exception as e:
            return None
    
    def get_proxies(self) -> Dict:
        """获取所有代理"""
        return self._request("GET", "/proxies") or {}
    
    def get_proxy_group(self, name: str) -> Dict:
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
    
    def health_check(self, targets: List[str] = None) -> Tuple[int, int]:
        """健康检查"""
        if targets is None:
            targets = [
                "https://api.telegram.org",
                "https://api.anthropic.com",
                "https://www.google.com"
            ]
        
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
    
    def find_best_node(self, preferred_regions: List[str] = None) -> Tuple[Optional[str], Optional[str], int]:
        """找最佳节点"""
        if preferred_regions is None:
            preferred_regions = ["新加坡", "香港", "日本", "美国", "SG", "HK", "JP", "US"]
        
        best_node = None
        best_group = None
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
                    
                    # 检查是否优先区域
                    is_preferred = any(r.lower() in node.lower() for r in preferred_regions)
                    
                    if is_preferred and delay < best_delay:
                        best_node = node
                        best_group = group
                        best_delay = delay
                    elif not best_node and delay < best_delay:
                        best_node = node
                        best_group = group
                        best_delay = delay
        
        return best_node, best_group, best_delay
    
    def auto_switch(self, preferred_regions: List[str] = None) -> str:
        """自动切换"""
        # 健康检查
        success, total = self.health_check()
        rate = success * 100 // total if total > 0 else 0
        
        if rate >= 60:
            return f"✓ 代理健康 ({success}/{total})"
        
        # 找最佳节点
        node, group, delay = self.find_best_node(preferred_regions)
        
        if node and group:
            self.set_proxy(group, node)
            return f"✓ 已切换 {group} -> {node} ({delay}ms)"
        else:
            return "✗ 未找到可用节点"


def main():
    parser = argparse.ArgumentParser(description="Clash Auto Switch - OpenClaw Skill")
    parser.add_argument("--api", default=os.environ.get("CLASH_API"), help="Clash API 地址")
    parser.add_argument("--secret", "-s", default=os.environ.get("CLASH_SECRET"), help="API 密钥")
    parser.add_argument("--proxy", default=os.environ.get("CLASH_PROXY"), help="代理地址")
    parser.add_argument("--list", "-l", action="store_true", help="列出代理组")
    parser.add_argument("--health", action="store_true", help="健康检查")
    parser.add_argument("--auto", "-a", action="store_true", help="自动切换")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--switch", nargs=2, metavar=("GROUP", "NODE"), help="切换节点")
    parser.add_argument("--sg", action="store_true", help="切换到新加坡")
    parser.add_argument("--us", action="store_true", help="切换到美国")
    parser.add_argument("--jp", action="store_true", help="切换到日本")
    parser.add_argument("--hk", action="store_true", help="切换到香港")
    
    args = parser.parse_args()
    
    clash = ClashAutoSwitch(args.api, args.secret, args.proxy)
    
    # 健康检查
    if args.health:
        success, total = clash.health_check()
        rate = success * 100 // total if total > 0 else 0
        if rate >= 60:
            print(f"✓ 代理健康 ({success}/{total})")
        else:
            print(f"✗ 代理不健康 ({success}/{total})")
    
    # 列出节点
    elif args.list:
        for group, current in clash.list_groups().items():
            print(f"{group}: {current}")
    
    # 自动切换
    elif args.auto:
        print(clash.auto_switch())
    
    # 状态
    elif args.status:
        success, total = clash.health_check()
        print(f"健康度: {success}/{total}")
        print("\n代理组:")
        for group, current in clash.list_groups().items():
            print(f"  {group}: {current}")
    
    # 手动切换
    elif args.switch:
        group, node = args.switch
        if clash.set_proxy(group, node):
            print(f"✓ 已切换 {group} -> {node}")
        else:
            print(f"✗ 切换失败")
    
    # 区域切换
    elif args.sg:
        print(clash.auto_switch(["新加坡", "SG"]))
    elif args.us:
        print(clash.auto_switch(["美国", "US", "LA"]))
    elif args.jp:
        print(clash.auto_switch(["日本", "JP"]))
    elif args.hk:
        print(clash.auto_switch(["香港", "HK"]))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
