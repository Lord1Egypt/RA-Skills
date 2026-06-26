#!/usr/bin/env python3
"""
每日美图推送脚本
从小红书搜索真人美女博主，返回1位博主的9张全身照美图
"""

import json
import os
import subprocess
import requests
from pathlib import Path
from datetime import datetime

# 配置
MCP_URL = "http://localhost:18060/mcp"
DATA_DIR = Path(__file__).parent / "data"
IMG_DIR = Path.home() / ".openclaw" / "workspace" / "img"
PUSHED_BLOGGERS_FILE = DATA_DIR / "pushed_bloggers.json"
PUSHED_IMAGES_FILE = DATA_DIR / "pushed_images.json"

# 黑名单关键词
BLACKLIST_KEYWORDS = [
    # AI类
    "comfyui", "ai", "AI", "机器人", "重绘",
    # 壁纸类
    "壁纸", "图源网络", "侵删", "收集", "整理", "分享图片", "高清", "全面屏",
    # 营销类
    "地陪", "商务", "服务", "合作请联系"
]

# 搜索关键词列表
SEARCH_KEYWORDS = ["全身照美女", "辣妹穿搭", "美女自拍"]


class MCPClient:
    """小红书 MCP 客户端"""
    
    def __init__(self):
        self.session_id = None
        self.headers = {"Content-Type": "application/json"}
    
    def init_session(self):
        """初始化 MCP 会话"""
        resp = requests.post(
            MCP_URL,
            headers=self.headers,
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "openclaw", "version": "1.0"}
                },
                "id": 1
            }
        )
        # 从响应头获取 session id
        self.session_id = resp.headers.get("Mcp-Session-Id")
        if self.session_id:
            self.headers["Mcp-Session-Id"] = self.session_id
        
        # 确认初始化
        requests.post(
            MCP_URL,
            headers=self.headers,
            json={
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
        )
        
        return self.session_id
    
    def search_feeds(self, keyword):
        """搜索帖子"""
        resp = requests.post(
            MCP_URL,
            headers=self.headers,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "search_feeds",
                    "arguments": {"keyword": keyword}
                },
                "id": 2
            },
            timeout=30
        )
        result = resp.json()
        
        # 解析返回的 JSON 字符串
        if "result" in result and "content" in result["result"]:
            text = result["result"]["content"][0]["text"]
            return json.loads(text)
        return {"feeds": [], "count": 0}
    
    def get_user_profile(self, user_id, xsec_token):
        """获取用户主页"""
        resp = requests.post(
            MCP_URL,
            headers=self.headers,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "user_profile",
                    "arguments": {
                        "user_id": user_id,
                        "xsec_token": xsec_token
                    }
                },
                "id": 3
            },
            timeout=30
        )
        result = resp.json()
        
        if "result" in result and "content" in result["result"]:
            text = result["result"]["content"][0]["text"]
            return json.loads(text)
        return None


class DailyBeauty:
    """每日美图推送"""
    
    def __init__(self):
        self.mcp = MCPClient()
        self.pushed_bloggers = self.load_json(PUSHED_BLOGGERS_FILE, {"bloggers": []})
        self.pushed_images = self.load_json(PUSHED_IMAGES_FILE, {"images": []})
    
    def load_json(self, filepath, default):
        """加载 JSON 文件"""
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return default
    
    def save_json(self, filepath, data):
        """保存 JSON 文件"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data["lastUpdated"] = datetime.now().isoformat()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def is_blacklisted(self, text):
        """检查是否包含黑名单关键词"""
        if not text:
            return False
        text_lower = text.lower()
        for keyword in BLACKLIST_KEYWORDS:
            if keyword.lower() in text_lower:
                return True
        return False
    
    def is_full_body_photo(self, width, height):
        """检查是否是全身照（宽高比 >= 1.3 且宽度 > 800）"""
        if width <= 800:
            return False
        ratio = height / width if width > 0 else 0
        return ratio >= 1.3
    
    def find_blogger(self):
        """搜索并筛选真人博主"""
        self.mcp.init_session()
        
        for keyword in SEARCH_KEYWORDS:
            print(f"搜索关键词: {keyword}")
            result = self.mcp.search_feeds(keyword)
            feeds = result.get("feeds", [])
            
            for feed in feeds:
                if feed.get("modelType") != "note":
                    continue
                
                note_card = feed.get("noteCard", {})
                user = note_card.get("user", {})
                user_id = user.get("userId", "")
                nickname = user.get("nickname", "")
                xsec_token = feed.get("xsecToken", "")
                display_title = note_card.get("displayTitle", "")
                
                # 排除已推送的博主
                if user_id in self.pushed_bloggers.get("bloggers", []):
                    print(f"跳过已推送博主: {nickname}")
                    continue
                
                # 排除黑名单关键词
                if self.is_blacklisted(display_title):
                    print(f"跳过黑名单博主: {nickname} - {display_title}")
                    continue
                
                # 获取博主主页检查简介
                profile = self.mcp.get_user_profile(user_id, xsec_token)
                if not profile:
                    continue
                
                user_info = profile.get("userBasicInfo", {})
                desc = user_info.get("desc", "")
                
                # 排除黑名单简介
                if self.is_blacklisted(desc):
                    print(f"跳过黑名单简介: {nickname}")
                    continue
                
                # 检查粉丝数
                interactions = profile.get("interactions", [])
                fans_count = 0
                for interaction in interactions:
                    if interaction.get("type") == "fans":
                        fans_count = int(interaction.get("count", "0").replace(",", ""))
                        break
                
                if fans_count < 1000:
                    print(f"跳过粉丝数不足: {nickname} - {fans_count}")
                    continue
                
                # 找到符合条件的博主
                print(f"找到博主: {nickname} (粉丝: {fans_count})")
                return {
                    "user_id": user_id,
                    "nickname": nickname,
                    "xsec_token": xsec_token,
                    "profile": profile
                }
        
        return None
    
    def select_images(self, profile):
        """从博主主页选择9张全身照"""
        feeds = profile.get("feeds", [])
        selected_images = []
        
        for feed in feeds:
            if len(selected_images) >= 9:
                break
            
            note_card = feed.get("noteCard", {})
            cover = note_card.get("cover", {})
            width = cover.get("width", 0)
            height = cover.get("height", 0)
            url = cover.get("urlDefault", "") or cover.get("urlPre", "")
            
            # 检查是否是全身照
            if not self.is_full_body_photo(width, height):
                continue
            
            # 检查是否已推送过
            if url in self.pushed_images.get("images", []):
                continue
            
            selected_images.append({
                "url": url,
                "width": width,
                "height": height,
                "title": note_card.get("displayTitle", "")
            })
        
        return selected_images[:9]
    
    def download_images(self, images):
        """下载图片"""
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        downloaded = []
        
        for i, img in enumerate(images, 1):
            url = img["url"]
            webp_path = IMG_DIR / f"beauty_{i}.webp"
            png_path = IMG_DIR / f"beauty_{i}.png"
            
            # 下载图片
            try:
                resp = requests.get(url, timeout=30)
                with open(webp_path, "wb") as f:
                    f.write(resp.content)
                
                # 转换为 PNG
                subprocess.run(
                    ["convert", str(webp_path), str(png_path)],
                    capture_output=True,
                    check=True
                )
                
                downloaded.append({
                    "url": url,
                    "path": str(png_path)
                })
                print(f"下载图片 {i}/9: {img['title']}")
                
            except Exception as e:
                print(f"下载失败: {e}")
        
        return downloaded
    
    def update_records(self, user_id, image_urls):
        """更新去重记录"""
        # 更新博主记录
        if user_id not in self.pushed_bloggers.get("bloggers", []):
            self.pushed_bloggers["bloggers"].append(user_id)
        self.save_json(PUSHED_BLOGGERS_FILE, self.pushed_bloggers)
        
        # 更新图片记录
        for url in image_urls:
            if url not in self.pushed_images.get("images", []):
                self.pushed_images["images"].append(url)
        self.save_json(PUSHED_IMAGES_FILE, self.pushed_images)
    
    def run(self):
        """执行主流程"""
        print("=== 开始搜索博主 ===")
        
        blogger = self.find_blogger()
        if not blogger:
            print("未找到符合条件的博主")
            return None
        
        print(f"\n=== 找到博主: {blogger['nickname']} ===")
        
        # 获取博主详细信息
        profile = blogger.get("profile", {})
        user_info = profile.get("userBasicInfo", {})
        interactions = profile.get("interactions", [])
        
        fans = likes = "0"
        for interaction in interactions:
            if interaction.get("type") == "fans":
                fans = interaction.get("count", "0")
            elif interaction.get("type") == "interaction":
                likes = interaction.get("count", "0")
        
        # 选择图片
        print("\n=== 选择图片 ===")
        images = self.select_images(profile)
        
        if len(images) < 9:
            print(f"图片数量不足: {len(images)}/9")
            return None
        
        # 下载图片
        print("\n=== 下载图片 ===")
        downloaded = self.download_images(images)
        
        if len(downloaded) < 9:
            print(f"下载失败，只有 {len(downloaded)} 张图片")
            return None
        
        # 更新去重记录
        print("\n=== 更新去重记录 ===")
        image_urls = [img["url"] for img in downloaded]
        self.update_records(blogger["user_id"], image_urls)
        
        # 返回结果
        return {
            "nickname": blogger["nickname"],
            "fans": fans,
            "likes": likes,
            "desc": user_info.get("desc", ""),
            "images": downloaded
        }


if __name__ == "__main__":
    beauty = DailyBeauty()
    result = beauty.run()
    
    if result:
        print("\n=== 推送信息 ===")
        print(f"博主: {result['nickname']}")
        print(f"粉丝: {result['fans']} | 获赞: {result['likes']}")
        print(f"简介: {result['desc']}")
        print(f"图片数量: {len(result['images'])}")
        
        # 输出 JSON 供调用方使用
        print("\n=== JSON 输出 ===")
        output = {
            "success": True,
            "blogger": {
                "nickname": result["nickname"],
                "fans": result["fans"],
                "likes": result["likes"],
                "desc": result["desc"]
            },
            "images": [img["path"] for img in result["images"]]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"success": False, "error": "未找到符合条件的博主"}, ensure_ascii=False))
