#!/usr/bin/env python3
"""
CDP 会话管理器 - 保持 WebSocket 连接持久化

解决 Chrome CDP 连接超时问题，实现会话复用
"""

import json
import time
import websocket
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class SessionManager:
    """CDP 会话管理器"""
    
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.ws: Optional[websocket.WebSocket] = None
        self.last_activity: datetime = datetime.now()
        self.timeout_seconds = 300  # 5 分钟超时
        self.msg_id = 0
        self.session_id: Optional[str] = None
    
    def connect(self) -> bool:
        """建立或恢复连接"""
        try:
            if self.ws and self.ws.connected:
                # 检查是否超时
                if datetime.now() - self.last_activity > timedelta(seconds=self.timeout_seconds):
                    print("会话超时，重新连接...")
                    self.ws.close()
                    self.ws = None
                else:
                    return True
            
            # 建立新连接
            self.ws = websocket.create_connection(self.ws_url, timeout=10)
            self.last_activity = datetime.now()
            print(f"✅ CDP 会话已建立：{self.ws_url[:50]}...")
            return True
        
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return False
    
    def send(self, method: str, params: Optional[Dict] = None) -> Dict:
        """发送命令并更新活动时间"""
        if not self.connect():
            raise ConnectionError("无法建立连接")
        
        self.msg_id += 1
        message = {
            "id": self.msg_id,
            "method": method,
            "params": params or {}
        }
        
        self.ws.send(json.dumps(message))
        response = self.ws.recv()
        self.last_activity = datetime.now()
        
        data = json.loads(response)
        if "error" in data:
            print(f"⚠️ CDP 错误：{data['error'].get('message', 'unknown')}")
        
        return data.get("result", {})
    
    def keep_alive(self, interval_seconds: int = 60):
        """保持连接活跃（定时发送空命令）"""
        def _ping():
            while True:
                time.sleep(interval_seconds)
                if self.ws and self.ws.connected:
                    try:
                        # 发送一个简单的命令保持连接
                        self.send("Runtime.evaluate", {"expression": "1"})
                        print(f"💓 会话保持活跃 [{datetime.now().strftime('%H:%M:%S')}]")
                    except:
                        pass
        
        import threading
        thread = threading.Thread(target=_ping, daemon=True)
        thread.start()
        return thread
    
    def close(self):
        """关闭会话"""
        if self.ws:
            self.ws.close()
            print("✅ 会话已关闭")


class CDPWithSession:
    """带会话保持的 CDP 客户端"""
    
    def __init__(self, ws_url: str):
        self.session = SessionManager(ws_url)
        self._keep_alive_thread = None
    
    def enable_keep_alive(self, interval: int = 60):
        """启用会话保持"""
        self._keep_alive_thread = self.session.keep_alive(interval)
    
    def navigate(self, url: str) -> Dict:
        """导航"""
        return self.session.send("Page.navigate", {"url": url})
    
    def screenshot(self, path: str = "screenshot.png") -> bytes:
        """截图"""
        import base64
        result = self.session.send("Page.captureScreenshot", {"format": "png"})
        data = base64.b64decode(result.get("data", ""))
        
        with open(path, "wb") as f:
            f.write(data)
        
        print(f"📸 截图已保存：{path}")
        return data
    
    def click(self, selector: str) -> Dict:
        """点击"""
        root = self.session.send("DOM.getDocument")
        root_id = root["root"]["nodeId"]
        
        node = self.session.send("DOM.querySelector", {
            "nodeId": root_id,
            "selector": selector
        })
        
        if not node.get("nodeId"):
            raise RuntimeError(f"元素未找到：{selector}")
        
        box = self.session.send("DOM.getBoxModel", {"nodeId": node["nodeId"]})
        border = box["model"]["border"]
        x = (border[0] + border[2]) / 2
        y = (border[0] + border[1]) / 2
        
        self.session.send("Input.dispatchMouseEvent", {
            "type": "mousePressed",
            "x": x, "y": y,
            "button": "left", "clickCount": 1
        })
        self.session.send("Input.dispatchMouseEvent", {
            "type": "mouseReleased",
            "x": x, "y": y,
            "button": "left", "clickCount": 1
        })
        
        return {"x": x, "y": y}
    
    def type_text(self, selector: str, text: str) -> Dict:
        """输入文本"""
        self.click(selector)
        
        for char in text:
            self.session.send("Input.dispatchKeyEvent", {
                "type": "keyDown", "text": char
            })
            self.session.send("Input.dispatchKeyEvent", {
                "type": "keyUp", "text": char
            })
        
        return {"text": text}
    
    def evaluate(self, script: str) -> Any:
        """执行 JS"""
        result = self.session.send("Runtime.evaluate", {"expression": script})
        return result.get("result", {}).get("value")
    
    def close(self):
        """关闭"""
        self.session.close()


# 使用示例
if __name__ == "__main__":
    # 示例：连接到本地 Chrome
    ws_url = "ws://127.0.0.1:9222/devtools/page/..."  # 从 /json/list 获取
    
    client = CDPWithSession(ws_url)
    client.enable_keep_alive(interval=60)
    
    try:
        client.navigate("https://example.com")
        time.sleep(2)
        client.screenshot("test.png")
        
        # 保持运行
        print("按 Ctrl+C 退出...")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        client.close()
        print("已退出")
