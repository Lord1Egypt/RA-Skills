#!/usr/bin/env python3
"""
Clash Verge API 客户端示例
用于通过 RESTful API 控制 Clash Verge (mihomo 内核)
"""

import requests
import json
import sys
from typing import Optional, Dict, Any


class ClashController:
    """Clash Verge API 控制器"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9090, secret: Optional[str] = None):
        self.base_url = f"http://{host}:{port}"
        self.headers = {}
        if secret:
            self.headers["Authorization"] = f"Bearer {secret}"
    
    def get_proxies(self) -> Dict[str, Any]:
        """获取所有代理"""
        resp = requests.get(f"{self.base_url}/proxies", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_proxy(self, name: str) -> Dict[str, Any]:
        """获取指定代理信息"""
        resp = requests.get(f"{self.base_url}/proxies/{requests.utils.quote(name)}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def set_proxy(self, group_name: str, proxy_name: str) -> Dict[str, Any]:
        """切换代理节点"""
        resp = requests.put(
            f"{self.base_url}/proxies/{requests.utils.quote(group_name)}",
            headers=self.headers,
            json={"name": proxy_name}
        )
        resp.raise_for_status()
        return resp.json()
    
    def test_delay(self, proxy_name: str, url: str = "https://www.google.com", timeout: int = 5000) -> Dict[str, Any]:
        """测试代理延迟"""
        resp = requests.get(
            f"{self.base_url}/proxies/{requests.utils.quote(proxy_name)}/delay",
            params={"url": url, "timeout": timeout},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()
    
    def get_groups(self) -> Dict[str, Any]:
        """获取策略组"""
        resp = requests.get(f"{self.base_url}/group", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_group(self, group_name: str) -> Dict[str, Any]:
        """获取指定策略组"""
        resp = requests.get(f"{self.base_url}/group/{requests.utils.quote(group_name)}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_connections(self) -> Dict[str, Any]:
        """获取连接列表"""
        resp = requests.get(f"{self.base_url}/connections", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def close_all_connections(self) -> None:
        """关闭所有连接"""
        resp = requests.delete(f"{self.base_url}/connections", headers=self.headers)
        resp.raise_for_status()
    
    def get_traffic(self) -> Dict[str, Any]:
        """获取流量信息"""
        resp = requests.get(f"{self.base_url}/traffic", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        resp = requests.get(f"{self.base_url}/configs", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def update_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """更新配置"""
        resp = requests.patch(
            f"{self.base_url}/configs",
            headers=self.headers,
            json=config
        )
        resp.raise_for_status()
        return resp.json()
    
    def restart(self) -> None:
        """重启内核"""
        resp = requests.post(f"{self.base_url}/restart", headers=self.headers)
        resp.raise_for_status()
    
    def get_version(self) -> Dict[str, Any]:
        """获取版本"""
        resp = requests.get(f"{self.base_url}/version", headers=self.headers)
        resp.raise_for_status()
        return resp.json()
    
    def flush_dns(self) -> None:
        """清除 DNS 缓存"""
        resp = requests.post(f"{self.base_url}/cache/dns/flush", headers=self.headers)
        resp.raise_for_status()
    
    def flush_fakeip(self) -> None:
        """清除 FakeIP 缓存"""
        resp = requests.post(f"{self.base_url}/cache/fakeip/flush", headers=self.headers)
        resp.raise_for_status()


def main():
    """命令行使用示例"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clash Verge API 客户端")
    parser.add_argument("--host", default="127.0.0.1", help="API 主机地址")
    parser.add_argument("--port", type=int, default=9090, help="API 端口")
    parser.add_argument("--secret", help="API 密钥")
    parser.add_argument("--action", choices=["list", "version", "traffic", "restart"], 
                        default="version", help="操作")
    parser.add_argument("--group", help="策略组名称")
    parser.add_argument("--proxy", help="代理名称")
    
    args = parser.parse_args()
    client = ClashController(args.host, args.port, args.secret)
    
    try:
        if args.action == "version":
            info = client.get_version()
            print(json.dumps(info, indent=2, ensure_ascii=False))
        
        elif args.action == "list":
            proxies = client.get_proxies()
            print(json.dumps(proxies, indent=2, ensure_ascii=False))
        
        elif args.action == "traffic":
            traffic = client.get_traffic()
            print(json.dumps(traffic, indent=2, ensure_ascii=False))
        
        elif args.action == "restart":
            client.restart()
            print("内核已重启")
    
    except requests.exceptions.RequestException as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
