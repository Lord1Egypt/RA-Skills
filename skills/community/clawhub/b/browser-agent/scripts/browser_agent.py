#!/usr/bin/env python3
"""
Browser Agent - Chrome CDP 自动化脚本

基于 Chrome DevTools Protocol (CDP) 实现浏览器自动化控制
支持 WebSocket 直连，绕过安全提示弹窗

用法:
  python browser_agent.py --check                    # 检查浏览器连接
  python browser_agent.py --url "https://example.com" --action screenshot
  python browser_agent.py --url "https://example.com" --action "click" --selector "#button"
  python browser_agent.py --script "my_automation.py"
"""

import sys
import os
import json
import time
import argparse
import websocket
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime

# CDP 默认配置
DEFAULT_CDP_PORT = 18800  # OpenClaw 浏览器默认端口
DEFAULT_CDP_HOST = "127.0.0.1"
CDP_VERSION = "1.3"


class CDPConnector:
    """Chrome DevTools Protocol 连接器"""
    
    def __init__(self, host: str = DEFAULT_CDP_HOST, port: int = DEFAULT_CDP_PORT):
        self.host = host
        self.port = port
        self.ws_url: Optional[str] = None
        self.ws: Optional[websocket.WebSocket] = None
        self.session_id: Optional[str] = None
        self.target_id: Optional[str] = None
        self.msg_id = 0
    
    def get_debugger_url(self) -> str:
        """获取 WebSocket 调试器 URL"""
        try:
            resp = requests.get(f"http://{self.host}:{self.port}/json/version", timeout=5)
            data = resp.json()
            return data.get("webSocketDebuggerUrl", "")
        except Exception as e:
            raise ConnectionError(f"无法连接到 Chrome CDP: {e}")
    
    def get_targets(self) -> List[Dict]:
        """获取所有可用目标（标签页）"""
        try:
            resp = requests.get(f"http://{self.host}:{self.port}/json/list", timeout=5)
            return resp.json()
        except Exception as e:
            raise ConnectionError(f"无法获取目标列表：{e}")
    
    def connect(self, target_url: Optional[str] = None) -> bool:
        """连接到 Chrome CDP"""
        # 获取目标列表
        targets = self.get_targets()
        
        # 找到合适的目标（优先匹配 URL 或选择第一个 page 类型）
        target = None
        if target_url:
            target = next((t for t in targets if target_url in t.get("url", "")), None)
        
        if not target:
            # 选择第一个 page 类型的目标
            target = next((t for t in targets if t.get("type") == "page"), None)
        
        if not target:
            raise RuntimeError("未找到可用的浏览器标签页")
        
        self.target_id = target.get("id")
        self.ws_url = target.get("webSocketDebuggerUrl")
        
        # 建立 WebSocket 连接
        try:
            self.ws = websocket.create_connection(self.ws_url, timeout=10)
            return True
        except Exception as e:
            raise ConnectionError(f"WebSocket 连接失败：{e}")
    
    def send(self, method: str, params: Optional[Dict] = None) -> Dict:
        """发送 CDP 命令"""
        self.msg_id += 1
        message = {
            "id": self.msg_id,
            "method": method,
            "params": params or {}
        }
        
        if self.session_id:
            message["sessionId"] = self.session_id
        
        self.ws.send(json.dumps(message))
        response = self.ws.recv()
        data = json.loads(response)
        
        if "error" in data:
            raise RuntimeError(f"CDP 命令错误：{data['error']}")
        
        return data.get("result", {})
    
    def navigate(self, url: str) -> Dict:
        """导航到 URL"""
        return self.send("Page.navigate", {"url": url})
    
    def screenshot(self, path: str = "screenshot.png", fmt: str = "png") -> bytes:
        """截取屏幕截图"""
        result = self.send("Page.captureScreenshot", {"format": fmt})
        import base64
        data = base64.b64decode(result.get("data", ""))
        
        with open(path, "wb") as f:
            f.write(data)
        
        return data
    
    def click(self, selector: str) -> Dict:
        """点击元素（使用 query_selector + dispatch_event）"""
        # 查询元素
        root_result = self.send("DOM.getDocument")
        root_node_id = root_result["root"]["nodeId"]
        
        query_result = self.send(
            "DOM.querySelector",
            {"nodeId": root_node_id, "selector": selector}
        )
        
        node_id = query_result.get("nodeId")
        if not node_id:
            raise RuntimeError(f"未找到元素：{selector}")
        
        # 获取元素边界
        box_result = self.send("DOM.getBoxModel", {"nodeId": node_id})
        border = box_result["model"]["border"]
        x = (border[0] + border[2]) / 2
        y = (border[0] + border[1]) / 2
        
        # 模拟点击
        self.send("Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        self.send("Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": x,
            "y": y,
            "button": "left",
            "clickCount": 1
        })
        
        return {"success": True, "x": x, "y": y}
    
    def type_text(self, selector: str, text: str) -> Dict:
        """在输入框中输入文本"""
        # 先点击元素获得焦点
        self.click(selector)
        
        # 输入文本
        for char in text:
            self.send("Input.dispatchKeyEvent", {
                "type": "keyDown",
                "text": char
            })
            self.send("Input.dispatchKeyEvent", {
                "type": "keyUp",
                "text": char
            })
        
        return {"success": True, "text": text}
    
    def evaluate(self, script: str) -> Any:
        """执行 JavaScript 代码"""
        result = self.send("Runtime.evaluate", {"expression": script})
        return result.get("result", {}).get("value")
    
    def close(self):
        """关闭连接"""
        if self.ws:
            self.ws.close()


class BrowserAgent:
    """浏览器自动化 Agent"""
    
    def __init__(self, host: str = DEFAULT_CDP_HOST, port: int = DEFAULT_CDP_PORT):
        self.connector = CDPConnector(host, port)
    
    def check_connection(self) -> bool:
        """检查浏览器连接状态"""
        try:
            targets = self.connector.get_targets()
            print(f"✅ Chrome CDP 连接正常")
            print(f"   活跃标签页：{len(targets)}")
            for t in targets[:5]:  # 显示前 5 个
                print(f"   - {t.get('title', 'Untitled')[:60]}")
            return True
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return False
    
    def run_action(self, url: str, action: str, **kwargs):
        """执行指定动作"""
        self.connector.connect(url)
        
        try:
            if action == "navigate":
                result = self.connector.navigate(url)
                print(f"导航到：{url}")
                print(f"结果：{result.get('frameId', 'unknown')}")
            
            elif action == "screenshot":
                path = kwargs.get("output", "screenshot.png")
                self.connector.navigate(url)
                time.sleep(1)  # 等待页面加载
                self.connector.screenshot(path)
                print(f"截图已保存：{path}")
            
            elif action == "click":
                selector = kwargs.get("selector")
                if not selector:
                    raise ValueError("需要指定 selector 参数")
                self.connector.navigate(url)
                time.sleep(1)
                result = self.connector.click(selector)
                print(f"点击成功：{selector} @ ({result['x']}, {result['y']})")
            
            elif action == "type":
                selector = kwargs.get("selector")
                text = kwargs.get("text", "")
                if not selector:
                    raise ValueError("需要指定 selector 参数")
                self.connector.navigate(url)
                time.sleep(1)
                result = self.connector.type_text(selector, text)
                print(f"输入成功：{text}")
            
            elif action == "eval":
                script = kwargs.get("script", "")
                result = self.connector.evaluate(script)
                print(f"执行结果：{result}")
            
            else:
                print(f"未知动作：{action}")
        
        finally:
            self.connector.close()


def main():
    parser = argparse.ArgumentParser(description="Browser Agent - Chrome CDP 自动化")
    parser.add_argument("--host", default=DEFAULT_CDP_HOST, help=f"CDP 主机 (默认：{DEFAULT_CDP_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_CDP_PORT, help=f"CDP 端口 (默认：{DEFAULT_CDP_PORT})")
    parser.add_argument("--check", action="store_true", help="检查浏览器连接")
    parser.add_argument("--url", help="目标 URL")
    parser.add_argument("--action", choices=["navigate", "screenshot", "click", "type", "eval"], help="执行动作")
    parser.add_argument("--selector", help="CSS 选择器（用于 click/type）")
    parser.add_argument("--text", help="输入文本（用于 type）")
    parser.add_argument("--script", help="JavaScript 代码（用于 eval）")
    parser.add_argument("--output", help="输出文件路径（用于 screenshot）")
    
    args = parser.parse_args()
    
    agent = BrowserAgent(args.host, args.port)
    
    if args.check:
        success = agent.check_connection()
        sys.exit(0 if success else 1)
    
    elif args.url and args.action:
        agent.run_action(
            args.url,
            args.action,
            selector=args.selector,
            text=args.text,
            script=args.script,
            output=args.output
        )
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
