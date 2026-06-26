#!/usr/bin/env python3
"""
ClawPaw 手机自动化控制脚本
通过 HTTP API 控制 Android 手机执行各种操作
"""

import requests
import base64
import xml.etree.ElementTree as ET
import time
import os
import json
from typing import Optional, Dict, Any, List

# 尝试加载配置文件
def load_config():
    """加载配置文件 config.yaml"""
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except:
        return {}

class ClawPawController:
    """ClawPaw 手机控制器"""
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, timeout: Optional[int] = None):
        """
        初始化控制器
        
        Args:
            host: 手机 IP 地址（Tailscale 或局域网），默认从 config.yaml 读取
            port: HTTP 服务器端口（默认 8765）
            timeout: 请求超时时间（默认 10 秒）
        """
        config = load_config()
        self.port = port or config.get("port", 8765)
        self.timeout = timeout or config.get("timeout", 10)
        
        # 根据网络类型决定 host
        network_type = config.get("network_type", "local")
        if network_type == "local" or network_type == "ssh":
            # SSH 反向隧道，固定用本地
            self.host = "127.0.0.1"
            self.network_info = "SSH 反向隧道（本地）"
        else:
            # Tailscale / WiFi，读取 config 里的 host（必须配置）
            self.host = host or config.get("host")
            if not self.host:
                raise ValueError("config.yaml 中必须配置 host 字段（Tailscale 或 WiFi IP）")
            if self.host.startswith("100."):
                self.network_info = "Tailscale"
            elif self.host.startswith("192.168."):
                self.network_info = "WiFi 局域网"
            else:
                self.network_info = network_type
        
        self.base_url = f"http://{self.host}:{self.port}"
        
        # 仅使用 config.yaml，不设置任何默认值
        self.config = config
    
    def check_status(self) -> Dict[str, Any]:
        """检查服务状态"""
        try:
            resp = requests.get(f"{self.base_url}/api/status", timeout=self.timeout)
            return resp.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_layout(self) -> str:
        """
        获取当前界面布局（XML）
        
        Returns:
            解码后的 XML 布局字符串
        """
        resp = requests.get(f"{self.base_url}/api/layout", timeout=self.timeout)
        data = resp.json()
        layout_b64 = data.get("layout", "")
        return base64.b64decode(layout_b64).decode("utf-8", errors="ignore")
    
    def get_screenshot(self, save_path: Optional[str] = None) -> bytes:
        """
        获取截图
        
        Args:
            save_path: 可选，保存截图到文件
            
        Returns:
            截图的 PNG 数据
        """
        resp = requests.get(f"{self.base_url}/api/screenshot", timeout=self.timeout)
        data = resp.json()
        screenshot_b64 = data.get("screenshot", "")
        png_data = base64.b64decode(screenshot_b64)
        
        if save_path:
            with open(save_path, "wb") as f:
                f.write(png_data)
        
        return png_data
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        执行命令
        
        Args:
            action: 动作类型 (click, input_text, swipe, back, open_amap, screenshot, get_layout)
            **kwargs: 动作参数
            
        Returns:
            执行结果
        """
        payload = {"action": action, **kwargs}
        resp = requests.post(
            f"{self.base_url}/api/execute",
            json=payload,
            timeout=self.timeout
        )
        return resp.json()
    
    def click(self, x: int, y: int, return_layout_after: bool = True) -> Dict[str, Any]:
        """
        点击指定坐标
        
        Args:
            x, y: 点击坐标
            return_layout_after: 执行后自动返回布局（默认 True）
        """
        return self.execute("click", x=x, y=y, return_layout_after=return_layout_after)
    
    def input_text(self, x: int, y: int, text: str, return_layout_after: bool = True) -> Dict[str, Any]:
        """
        在指定坐标输入文本（需要启用 ClawPaw 输入法）
        
        Args:
            x, y: 输入框坐标
            text: 要输入的文本
            return_layout_after: 执行后自动返回布局（默认 True）
        """
        return self.execute("input_text", x=x, y=y, text=text, return_layout_after=return_layout_after)
    
    def input_text_direct(self, x: int, y: int, text: str, return_layout_after: bool = True) -> Dict[str, Any]:
        """
        用无障碍服务直接设输入框文字（不依赖输入法）
        
        Args:
            x, y: 输入框坐标
            text: 要输入的文本
            return_layout_after: 执行后自动返回布局（默认 True）
        """
        return self.execute("input_text_direct", x=x, y=y, text=text, return_layout_after=return_layout_after)
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, 
              duration: int = 300) -> Dict[str, Any]:
        """滑动"""
        return self.execute("swipe", start_x=start_x, start_y=start_y, 
                           end_x=end_x, end_y=end_y, duration=duration)
    
    def back(self) -> Dict[str, Any]:
        """返回"""
        return self.execute("back")
    
    def open_amap(self) -> Dict[str, Any]:
        """打开高德地图"""
        return self.execute("open_amap")
    
    def open_schema(self, schema: str = "", uri: str = "", return_layout_after: bool = True) -> Dict[str, Any]:
        """
        打开任意应用（通过 schema/URI 或包名）
        
        Args:
            schema: 应用 schema/URI（如 `baidumap://`、`com.android.chrome`、`https://...`）
            uri: 同 schema（别名）
            return_layout_after: 执行后自动返回布局（默认 True）
        """
        # 支持 schema 或 uri 参数
        target = schema or uri
        return self.execute("open_schema", schema=target, return_layout_after=return_layout_after)
    
    def get_battery(self) -> Dict[str, Any]:
        """获取电量"""
        return self.execute("get_battery")
    
    def get_location(self) -> Dict[str, Any]:
        """获取定位"""
        return self.execute("get_location")
    
    def get_wifi_name(self) -> Dict[str, Any]:
        """获取 WiFi 名称"""
        return self.execute("get_wifi_name")
    
    def get_screen_state(self) -> Dict[str, Any]:
        """获取屏幕状态"""
        return self.execute("get_screen_state")
    
    def get_state(self) -> Dict[str, Any]:
        """获取完整状态"""
        return self.execute("get_state")
    
    def vibrate(self, duration_ms: int = 200) -> Dict[str, Any]:
        """震动"""
        return self.execute("vibrate", duration_ms=duration_ms)
    
    def camera_rear(self) -> Dict[str, Any]:
        """后置拍照"""
        return self.execute("camera_rear")
    
    def camera_front(self) -> Dict[str, Any]:
        """前置拍照（异步保存）"""
        return self.execute("camera_front")
    
    def camera_snap(self, facing: int = 0) -> Dict[str, Any]:
        """
        同步拍照
        
        Args:
            facing: 0 后置 / 1 前置
        """
        return self.execute("camera.snap", facing=facing)
    
    # ========== 设备信息 ==========
    
    def device_info(self) -> Dict[str, Any]:
        """
        获取设备信息
        
        Returns:
            设备信息（model、manufacturer、androidVersion、displayName 等）
        """
        return self.execute("device.info")
    
    # ========== 通知管理 ==========
    
    def notifications_list(self, limit: int = 50) -> Dict[str, Any]:
        """
        获取当前通知列表
        
        Args:
            limit: 限制数量（默认 50）
            
        Returns:
            通知列表（packageName、title、text、postTime、key）
        """
        return self.execute("notifications.list", limit=limit)
    
    def notifications_actions(self, action: str, key: str) -> Dict[str, Any]:
        """
        操作通知（dismiss/open/reply）
        
        Args:
            action: 操作类型（dismiss/open/reply）
            key: 通知 key（来自 notifications.list）
            
        Note: 仅 Node (WebSocket) 方式支持，HTTP/ADB 返回未实现
        """
        return self.execute("notifications.actions", action=action, key=key)
    
    def notification_show(self, title: str, text: str) -> Dict[str, Any]:
        """
        推送本地通知
        
        Args:
            title: 通知标题
            text: 通知内容
        """
        return self.execute("notification.show", title=title, text=text)
    
    def notifications_push(self, title: str, body: str) -> Dict[str, Any]:
        """
        推送本地通知（同 notification_show）
        
        Args:
            title: 通知标题
            body: 通知内容
        """
        return self.execute("notifications.push", title=title, body=body)
    
    # ========== 联系人 ==========
    
    def contacts_list(self, limit: int = 500) -> Dict[str, Any]:
        """
        获取联系人列表
        
        Args:
            limit: 限制数量（默认 500）
        """
        return self.execute("contacts.list", limit=limit)
    
    def contacts_search(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """
        搜索联系人
        
        Args:
            query: 搜索关键词
            limit: 限制数量（默认 100）
        """
        return self.execute("contacts.search", query=query, limit=limit)
    
    # ========== 照片 ==========
    
    def photos_list(self, limit: int = 50) -> Dict[str, Any]:
        """
        获取最近照片列表
        
        Args:
            limit: 限制数量（默认 50）
        """
        return self.execute("photos.list", limit=limit)
    
    def photos_latest(self, limit: int = 50) -> Dict[str, Any]:
        """
        获取最近照片
        
        Args:
            limit: 限制数量（默认 50，与 ClawPaw 一致）
        """
        return self.execute("photos.latest", limit=limit)
    
    # ========== 日历 ==========
    
    def calendar_list(self, limit: int = 100) -> Dict[str, Any]:
        """
        获取日历事件列表
        
        Args:
            limit: 限制数量（默认 100）
        """
        return self.execute("calendar.list", limit=limit)
    
    def calendar_events(self, limit: int = 100) -> Dict[str, Any]:
        """
        获取日历事件列表（同 calendar_list）
        
        Args:
            limit: 限制数量（默认 100）
        """
        return self.execute("calendar.events", limit=limit)
    
    # ========== 音量控制 ==========
    
    def volume_get(self) -> Dict[str, Any]:
        """
        获取音量
        
        Returns:
            媒体/铃声音量与最大值
        """
        return self.execute("volume.get")
    
    def volume_set(self, stream: str = "media", volume: int = 5) -> Dict[str, Any]:
        """
        设置音量
        
        Args:
            stream: 流类型（media/ring）
            volume: 音量值
        """
        return self.execute("volume.set", stream=stream, volume=volume)
    
    # ========== 文件读写 ==========
    
    def file_read_text(self, path: str) -> Dict[str, Any]:
        """
        读取文件为 UTF-8 文本
        
        Args:
            path: 文件路径
        """
        return self.execute("file.read_text", path=path)
    
    def file_read_base64(self, path: str) -> Dict[str, Any]:
        """
        读取文件为 Base64
        
        Args:
            path: 文件路径
        """
        return self.execute("file.read_base64", path=path)
    
    # ========== 传感器 ==========
    
    def sensors_steps(self) -> Dict[str, Any]:
        """
        获取步数
        
        Returns:
            步数（steps、available）
        """
        return self.execute("sensors.steps")
    
    def sensors_light(self) -> Dict[str, Any]:
        """
        获取光照强度
        
        Returns:
            光照 lux
        """
        return self.execute("sensors.light")
    
    def sensors_info(self) -> Dict[str, Any]:
        """
        获取传感器列表摘要
        """
        return self.execute("sensors.info")
    
    # ========== 蓝牙 ==========
    
    def bluetooth_list(self) -> Dict[str, Any]:
        """
        获取已配对设备列表
        
        Returns:
            设备列表（name、address）
        """
        return self.execute("bluetooth.list")
    
    # ========== WiFi ==========
    
    def wifi_info(self) -> Dict[str, Any]:
        """
        获取 WiFi 状态
        
        Returns:
            WiFi 状态（enabled、ssid、bssid、rssi、ipAddress）
        """
        return self.execute("wifi.info")
    
    def wifi_enable(self, enabled: bool = True) -> Dict[str, Any]:
        """
        开/关 WiFi
        
        Args:
            enabled: True 开启 / False 关闭
        """
        return self.execute("wifi.enable", enabled=enabled)
    
    # ========== 手势操作 ==========
    
    def long_press(self, x: int, y: int, return_layout_after: bool = True) -> Dict[str, Any]:
        """
        长按指定坐标（700ms）
        
        Args:
            x, y: 长按坐标
            return_layout_after: 执行后自动返回布局（默认 True）
        """
        return self.execute("long_press", x=x, y=y, return_layout_after=return_layout_after)
    
    def two_finger_swipe_same(self, start_x: int, start_y: int, 
                              end_x: int, end_y: int) -> Dict[str, Any]:
        """
        两指同向滑动（如放大地图）
        
        Args:
            start_x, start_y: 起始坐标
            end_x, end_y: 结束坐标
        """
        return self.execute("two_finger_swipe_same", 
                           start_x=start_x, start_y=start_y, 
                           end_x=end_x, end_y=end_y)
    
    def two_finger_swipe_opposite(self, start_x: int, start_y: int, 
                                  end_x: int, end_y: int) -> Dict[str, Any]:
        """
        两指反向滑动（并拢缩小/张开放大）
        
        Args:
            start_x, start_y: 起始坐标
            end_x, end_y: 结束坐标（另一指从 end 滑向 start）
        """
        return self.execute("two_finger_swipe_opposite", 
                           start_x=start_x, start_y=start_y, 
                           end_x=end_x, end_y=end_y)
    
    def screen_on(self) -> Dict[str, Any]:
        """
        点亮/唤醒屏幕
        """
        return self.execute("screen_on")
    
    # =========================================
    
    def find_element(self, layout: str, search_text: str = "", 
                     resource_id: str = "", content_desc: str = "") -> Optional[Dict]:
        """
        在布局中查找元素
        
        Args:
            layout: XML 布局字符串
            search_text: 搜索文本（包含匹配）
            resource_id: 资源 ID
            content_desc: 内容描述
            
        Returns:
            元素信息字典，包含 bounds、text 等，未找到返回 None
        """
        try:
            root = ET.fromstring(layout)
            for node in root.iter():
                text = node.attrib.get("text", "")
                res_id = node.attrib.get("resource-id", "")
                desc = node.attrib.get("content-desc", "")
                bounds = node.attrib.get("bounds", "")
                
                # 匹配条件
                matched = False
                if search_text and search_text in text:
                    matched = True
                if resource_id and resource_id in res_id:
                    matched = True
                if content_desc and content_desc in desc:
                    matched = True
                
                if matched:
                    # 解析坐标
                    coords = self._parse_bounds(bounds)
                    return {
                        "text": text,
                        "resource-id": res_id,
                        "content-desc": desc,
                        "bounds": bounds,
                        "center_x": (coords[0] + coords[2]) // 2,
                        "center_y": (coords[1] + coords[3]) // 2
                    }
        except Exception as e:
            print(f"解析布局失败：{e}")
        
        return None
    
    def _parse_bounds(self, bounds: str) -> List[int]:
        """解析 bounds 字符串为坐标列表 [left, top, right, bottom]"""
        try:
            # 格式：[left,top][right,bottom]
            bounds = bounds.strip("[]")
            parts = bounds.split("][")
            left_top = parts[0].split(",")
            right_bottom = parts[1].split(",")
            return [int(left_top[0]), int(left_top[1]), 
                    int(right_bottom[0]), int(right_bottom[1])]
        except:
            return [0, 0, 0, 0]
    

    
    def wait_for_element(self, search_text: str = "", timeout: int = 10, 
                         interval: float = 1.0) -> Optional[Dict]:
        """
        等待元素出现
        
        Args:
            search_text: 搜索文本
            timeout: 超时时间（秒）
            interval: 轮询间隔（秒）
            
        Returns:
            元素信息，超时返回 None
        """
        start = time.time()
        while time.time() - start < timeout:
            layout = self.get_layout()
            element = self.find_element(layout, search_text=search_text)
            if element:
                return element
            time.sleep(interval)
        return None
    
    def decode_layout(self, layout_b64: str) -> str:
        """
        解码 Base64 布局字符串
        
        Args:
            layout_b64: Base64 编码的布局
            
        Returns:
            解码后的 XML 字符串
        """
        return base64.b64decode(layout_b64).decode("utf-8", errors="ignore")
    
    def _get_screenshot_base64(self) -> str:
        """
        获取截图的 Base64 数据
        
        Returns:
            Base64 编码的截图数据
        """
        resp = requests.get(f"{self.base_url}/api/screenshot", timeout=self.timeout)
        data = resp.json()
        return data.get("screenshot", "")
    
    def _save_screenshot_by_timestamp(self, screenshot_b64: str, 
                                       save_dir: str = "./screenshots") -> str:
        """
        按时间戳保存截图到指定目录
        
        Args:
            screenshot_b64: Base64 编码的截图数据
            save_dir: 保存目录（相对于脚本所在目录，默认 ./screenshots）
            
        Returns:
            保存的文件路径（绝对路径）
        """
        import datetime
        # 获取脚本所在目录作为基准
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 确保目录存在（相对于脚本目录）
        abs_save_dir = os.path.normpath(os.path.join(script_dir, save_dir))
        os.makedirs(abs_save_dir, exist_ok=True)
        
        # 生成时间戳文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(abs_save_dir, filename)
        
        # 保存文件
        png_data = base64.b64decode(screenshot_b64)
        with open(filepath, "wb") as f:
            f.write(png_data)
        
        return filepath
    
    def _call_vision_api(self, api_base: str, api_key: str, model: str, 
                         image_b64: str, prompt: str) -> Dict[str, Any]:
        """
        调用视觉大模型分析图片（通用 OpenAI 格式）
        
        Args:
            api_base: API 基础 URL
            api_key: API Key
            model: 模型名称
            image_b64: Base64 编码的图片数据
            prompt: 分析提示词
            
        Returns:
            模型返回的分析结果
        """
        # 构建请求
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                    ]
                }],
                "temperature": 0.1,
                "max_tokens": 500
            },
            timeout=120
        )
        
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        
        # 尝试提取 JSON
        try:
            import re
            import json
            json_match = re.search(r'\{[^}]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return {"raw_response": content}
        except:
            return {"raw_response": content}
    

    def analyze_screen(self, prompt: str, save: bool = True, 
                       include_layout: bool = True) -> Dict[str, Any]:
        """
        获取截图 + XML 布局，让大模型分析并返回坐标
        
        根据 vision_status 决定行为：
        - uninitialized: 未初始化（不保存截图，提示配置）
        - disabled: 禁用（保存截图，可调用 image 工具）
        - enabled: 启用（自动调用视觉 API 分析）
        
        Args:
            prompt: 分析提示（如"找到搜索框并返回点击坐标"）
            save: 是否保存截图（默认 True）
            include_layout: 是否同时发送 XML 布局（默认 True）
            
        Returns:
            分析结果（包含 status 字段）
        """
        # 第 1 步：检查 vision_status
        status = self.config.get("vision_status", "uninitialized")
        
        if status == "uninitialized":
            # 未初始化：不保存截图，只提示需要配置
            return {
                "status": "uninitialized",
                "message": "视觉分析未初始化",
                "suggestion": "请配置 vision_llm 后设置 vision_status: enabled"
            }
        
        elif status == "disabled":
            # 禁用：保存截图，提示可用 image 工具
            screenshot_b64 = self._get_screenshot_base64()
            saved_path = self._save_screenshot_by_timestamp(screenshot_b64)
            return {
                "status": "disabled",
                "message": "视觉分析已禁用，截图已保存",
                "screenshot_path": saved_path,
                "suggestion": f"可调用 image 工具分析：image(image=\"{saved_path}\")"
            }
        
        elif status == "enabled":
            # 检查 API 配置（仅支持 vision_llm 通用格式）
            vision_config = self.config.get("vision_llm", {})
            if not vision_config:
                return {
                    "status": "error",
                    "message": "视觉分析已启用但缺少 vision_llm 配置",
                    "suggestion": "请在 config.yaml 中配置 vision_llm.api_base, vision_llm.api_key, vision_llm.model"
                }
            
            api_base = vision_config.get("api_base")
            api_key = vision_config.get("api_key")
            model = vision_config.get("model")
            
            # 检查必需配置
            missing = []
            if not api_base:
                missing.append("api_base")
            if not api_key:
                missing.append("api_key")
            if not model:
                missing.append("model")
            
            if missing:
                return {
                    "status": "error",
                    "message": f"视觉分析已启用但缺少配置：{', '.join(missing)}",
                    "suggestion": f"请在 config.yaml 中填写 vision_llm.{', vision_llm.'.join(missing)}"
                }
            
            # 获取截图和 XML
            screenshot_b64 = self._get_screenshot_base64()
            layout_xml = ""
            if include_layout:
                try:
                    layout_xml = self.get_layout()
                except Exception as e:
                    print(f"⚠️ 获取布局失败：{e}，仅使用截图分析")
            
            # 可选保存
            saved_path = None
            if save and screenshot_b64:
                saved_path = self._save_screenshot_by_timestamp(screenshot_b64)
                print(f"📸 截图已保存：{saved_path}")
            
            # 构建增强提示词
            enhanced_prompt = f"""【任务】{prompt}

【截图】见下方图片

【XML 布局】
```xml
{layout_xml[:30000]}
```

【要求】
1. 结合截图和 XML 布局，找到目标元素
2. 返回 JSON 格式：{{"action": "click", "x": 500, "y": 1200, "reason": "说明"}}"""
            
            # 调用 LLM API
            print(f"🔍 分析中（截图 + XML）...")
            result = self._call_vision_api(api_base, api_key, model, screenshot_b64, enhanced_prompt)
            
            return {
                "status": "success",
                "message": "视觉分析完成",
                "data": result
            }
        
        # 不应该到这里
        raise ValueError(f"未知的 vision_status: {status}")


# 命令行工具
if __name__ == "__main__":
    import sys
    
    controller = ClawPawController()
    
    def usage():
        print("""用法：python3 clawpaw_controller.py <命令> [参数]

基础命令:
  status              - 检查服务状态
  open_schema <schema> - 打开任意应用（包名或 schema）
  click <x> <y>       - 点击坐标
  input_text <x> <y> <text> - 输入文本（需要输入法）
  input_text_direct <x> <y> <text> - 直接输入（无障碍）
  swipe <x1> <y1> <x2> <y2> - 滑动
  back                - 返回键
  layout              - 获取界面布局（XML）
  long_press <x> <y>  - 长按（700ms）
  two_finger_swipe_same <x1> <y1> <x2> <y2> - 两指同向滑动
  two_finger_swipe_opposite <x1> <y1> <x2> <y2> - 两指反向滑动
  screen_on           - 点亮屏幕

状态查询:
  get_battery         - 获取电量
  get_location        - 获取定位
  get_wifi_name       - 获取 WiFi 名称
  get_screen_state    - 获取屏幕状态
  get_state           - 获取完整状态
  device_info         - 获取设备信息

硬件控制:
  vibrate [duration]  - 震动（默认 200ms）
  camera_rear         - 后置拍照（异步）
  camera_front        - 前置拍照（异步）
  camera_snap <0|1>   - 同步拍照（0 后置/1 前置）

通知管理:
  notifications_list [limit]        - 获取通知列表（默认 50）
  notifications_actions <act> <key> - 操作通知（dismiss/open/reply）⚠️仅 Node
  notification_show <title> <text>  - 推送通知

联系人/照片/日历:
  contacts_list [limit]         - 联系人列表（默认 500）
  contacts_search <query> [limit] - 搜索联系人（默认 100，脚本侧过滤）
  photos_list [limit]           - 照片列表（默认 50）
  photos_latest [limit]         - 最近照片（默认 50）
  calendar_list [limit]         - 日历事件（默认 100）
  calendar_events [limit]       - 日历事件（同 calendar_list）

音量控制:
  volume_get          - 获取音量
  volume_set <stream> <vol> - 设置音量（stream: media/ring）

文件读写:
  file_read_text <path>     - 读取文本文件
  file_read_base64 <path>   - 读取文件为 Base64

传感器:
  sensors_steps       - 步数
  sensors_light       - 光照 lux
  sensors_info        - 传感器列表

蓝牙/WiFi:
  bluetooth_list      - 已配对设备列表
  wifi_info           - WiFi 状态
  wifi_enable <true|false> - 开关 WiFi

视觉分析:
  analyze <prompt>              - 视觉分析屏幕（截图+XML 布局，自动保存截图）
  analyze <prompt> --no-save    - 视觉分析（不保存截图）
  analyze <prompt> --no-layout  - 仅截图分析（不发送 XML 布局）

示例:
  python3 clawpaw_controller.py status
  python3 clawpaw_controller.py click 500 1000
  python3 clawpaw_controller.py input_text 400 300 "搜索内容"
  python3 clawpaw_controller.py get_battery
  python3 clawpaw_controller.py vibrate 500
  python3 clawpaw_controller.py analyze "找到搜索框并返回坐标"
  python3 clawpaw_controller.py long_press 500 1000
  python3 clawpaw_controller.py device_info
  python3 clawpaw_controller.py notifications_list
  python3 clawpaw_controller.py camera_snap 0
  python3 clawpaw_controller.py volume_set media 5
  python3 clawpaw_controller.py wifi_enable true
""")
    
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "status":
            status = controller.check_status()
            print(f"服务状态：{status}")
            if status.get("status") == "ok" or status.get("success"):
                print("✅ 服务正常")
            else:
                print("❌ 服务不可用")
                sys.exit(1)
        
        elif cmd == "open_amap":
            result = controller.open_amap()
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "open_schema":
            if len(sys.argv) < 3:
                print("❌ 需要指定 schema/包名")
                sys.exit(1)
            schema = sys.argv[2]
            result = controller.open_schema(schema=schema)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "click":
            if len(sys.argv) < 4:
                print("❌ 需要指定坐标 x y")
                sys.exit(1)
            x, y = int(sys.argv[2]), int(sys.argv[3])
            result = controller.click(x, y)
            # 有布局就只打印 XML，否则打印原始结果
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "input_text":
            if len(sys.argv) < 5:
                print("❌ 需要指定 x y text")
                sys.exit(1)
            x, y = int(sys.argv[2]), int(sys.argv[3])
            text = sys.argv[4]
            result = controller.input_text(x, y, text)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "input_text_direct":
            if len(sys.argv) < 5:
                print("❌ 需要指定 x y text")
                sys.exit(1)
            x, y = int(sys.argv[2]), int(sys.argv[3])
            text = sys.argv[4]
            result = controller.input_text_direct(x, y, text)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "swipe":
            if len(sys.argv) < 6:
                print("❌ 需要指定 start_x start_y end_x end_y")
                sys.exit(1)
            x1, y1 = int(sys.argv[2]), int(sys.argv[3])
            x2, y2 = int(sys.argv[4]), int(sys.argv[5])
            result = controller.swipe(x1, y1, x2, y2)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "back":
            result = controller.back()
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "layout":
            layout = controller.get_layout()
            print(layout)
        
        elif cmd == "screenshot":
            path = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
            controller.get_screenshot(save_path=path)
            print(f"截图已保存到：{path}")
        
        elif cmd == "get_battery":
            result = controller.get_battery()
            print(result)
        
        elif cmd == "get_location":
            result = controller.get_location()
            print(result)
        
        elif cmd == "get_wifi_name":
            result = controller.get_wifi_name()
            print(result)
        
        elif cmd == "get_screen_state":
            result = controller.get_screen_state()
            print(result)
        
        elif cmd == "get_state":
            result = controller.get_state()
            print(result)
        
        elif cmd == "vibrate":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 200
            result = controller.vibrate(duration_ms=duration)
            print(result)
        
        elif cmd == "camera_rear":
            result = controller.camera_rear()
            print(result)
        
        elif cmd == "camera_front":
            result = controller.camera_front()
            print(result)
        
        elif cmd == "camera_snap":
            facing = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            result = controller.camera_snap(facing=facing)
            print(result)
        
        elif cmd == "device_info":
            result = controller.device_info()
            print(result)
        
        elif cmd == "notifications_list":
            result = controller.notifications_list()
            print(result)
        
        elif cmd == "notification_show":
            if len(sys.argv) < 4:
                print("❌ 需要指定 title 和 text")
                sys.exit(1)
            title = sys.argv[2]
            text = sys.argv[3]
            result = controller.notification_show(title, text)
            print(result)
        
        elif cmd == "notifications_push":
            if len(sys.argv) < 4:
                print("❌ 需要指定 title 和 body")
                sys.exit(1)
            title = sys.argv[2]
            body = sys.argv[3]
            result = controller.notifications_push(title, body)
            print(result)
        
        elif cmd == "contacts_list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 500
            result = controller.contacts_list(limit=limit)
            print(result)
        
        elif cmd == "photos_list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            result = controller.photos_list(limit=limit)
            print(result)
        
        elif cmd == "calendar_list":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            result = controller.calendar_list(limit=limit)
            print(result)
        
        elif cmd == "calendar_events":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            result = controller.calendar_events(limit=limit)
            print(result)
        
        elif cmd == "notifications_actions":
            if len(sys.argv) < 4:
                print("❌ 需要指定 action 和 key")
                print("用法：python3 clawpaw_controller.py notifications_actions <dismiss|open|reply> <key>")
                sys.exit(1)
            action = sys.argv[2]
            key = sys.argv[3]
            result = controller.notifications_actions(action=action, key=key)
            print(result)
        
        elif cmd == "contacts_search":
            if len(sys.argv) < 3:
                print("❌ 需要指定搜索关键词")
                sys.exit(1)
            query = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
            result = controller.contacts_search(query=query, limit=limit)
            print(result)
        
        elif cmd == "photos_latest":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            result = controller.photos_latest(limit=limit)
            print(result)
        
        elif cmd == "volume_get":
            result = controller.volume_get()
            print(result)
        
        elif cmd == "volume_set":
            if len(sys.argv) < 4:
                print("❌ 需要指定 stream 和 volume")
                sys.exit(1)
            stream = sys.argv[2]
            volume = int(sys.argv[3])
            result = controller.volume_set(stream=stream, volume=volume)
            print(result)
        
        elif cmd == "file_read_text":
            if len(sys.argv) < 3:
                print("❌ 需要指定文件路径")
                sys.exit(1)
            path = sys.argv[2]
            result = controller.file_read_text(path=path)
            print(result)
        
        elif cmd == "file_read_base64":
            if len(sys.argv) < 3:
                print("❌ 需要指定文件路径")
                sys.exit(1)
            path = sys.argv[2]
            result = controller.file_read_base64(path=path)
            print(result)
        
        elif cmd == "sensors_steps":
            result = controller.sensors_steps()
            print(result)
        
        elif cmd == "sensors_light":
            result = controller.sensors_light()
            print(result)
        
        elif cmd == "sensors_info":
            result = controller.sensors_info()
            print(result)
        
        elif cmd == "bluetooth_list":
            result = controller.bluetooth_list()
            print(result)
        
        elif cmd == "wifi_info":
            result = controller.wifi_info()
            print(result)
        
        elif cmd == "wifi_enable":
            if len(sys.argv) < 3:
                print("❌ 需要指定 true 或 false")
                sys.exit(1)
            enabled = sys.argv[2].lower() == "true"
            result = controller.wifi_enable(enabled=enabled)
            print(result)
        
        # ========== 手势操作 ==========
        
        elif cmd == "long_press":
            if len(sys.argv) < 4:
                print("❌ 需要指定坐标 x y")
                sys.exit(1)
            x, y = int(sys.argv[2]), int(sys.argv[3])
            result = controller.long_press(x, y)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "two_finger_swipe_same":
            if len(sys.argv) < 6:
                print("❌ 需要指定 start_x start_y end_x end_y")
                sys.exit(1)
            x1, y1 = int(sys.argv[2]), int(sys.argv[3])
            x2, y2 = int(sys.argv[4]), int(sys.argv[5])
            result = controller.two_finger_swipe_same(x1, y1, x2, y2)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "two_finger_swipe_opposite":
            if len(sys.argv) < 6:
                print("❌ 需要指定 start_x start_y end_x end_y")
                sys.exit(1)
            x1, y1 = int(sys.argv[2]), int(sys.argv[3])
            x2, y2 = int(sys.argv[4]), int(sys.argv[5])
            result = controller.two_finger_swipe_opposite(x1, y1, x2, y2)
            if result.get("layout"):
                layout = controller.decode_layout(result["layout"])
                print(layout)
            else:
                print(result)
        
        elif cmd == "screen_on":
            result = controller.screen_on()
            print(result)
        
        elif cmd == "analyze":
            if len(sys.argv) < 3:
                print("❌ 需要指定分析提示词")
                print("用法：python3 clawpaw_controller.py analyze <提示词> [--no-save] [--no-layout]")
                sys.exit(1)
            
            # 解析参数
            save = True
            include_layout = True
            prompt_parts = []
            for arg in sys.argv[2:]:
                if arg == "--no-save":
                    save = False
                elif arg == "--no-layout":
                    include_layout = False
                else:
                    prompt_parts.append(arg)
            
            prompt = " ".join(prompt_parts)
            
            if not prompt:
                print("❌ 需要指定分析提示词")
                sys.exit(1)
            
            # 执行分析
            result = controller.analyze_screen(prompt, save=save, include_layout=include_layout)
            print("-" * 50)
            print("✅ 分析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        else:
            print(f"❌ 未知命令：{cmd}")
            usage()
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        sys.exit(1)
