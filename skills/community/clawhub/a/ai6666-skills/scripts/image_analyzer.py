#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片分析器 - 使用 MiniMax Vision API 理解图片内容并生成评论

支持真实的 AI 图片理解，不再依赖像素分析
"""

import requests
import base64
import json
import os
import tempfile
from typing import Optional


class MiniMaxClient:
    """MiniMax API 客户端 - 用于图片理解"""

    def __init__(self, api_key: str = None, api_host: str = None):
        # 从环境变量或直接传入获取 API key
        self.api_key = api_key or os.environ.get(
            "MINIMAX_API_KEY",
            "sk-cp-M0p_jtAWxZ_IKwoeQaLbJh4V43L85PmtyjlLjmIZIDduuL4e_fFRSlXSWzL7GOCWJPu4lN-O4Dt9cLbLFMZVzxLUgKSq0NGgtn6ABKj4K-73boMA0ehpjxo"
        )
        self.api_host = api_host or os.environ.get(
            "MINIMAX_API_HOST",
            "https://api.minimaxi.com"
        )

    def _read_image_as_base64(self, image_path: str) -> str:
        """读取图片并转为 base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def understand_image(self, image_path: str, prompt: str = None) -> str:
        """
        使用 MiniMax Vision API 分析图片

        Args:
            image_path: 图片路径（本地文件）
            prompt: 可选提示词

        Returns:
            str: 图片内容描述
        """
        if not os.path.exists(image_path):
            return ""

        # 读取图片
        image_b64 = self._read_image_as_base64(image_path)

        # MiniMax 使用 /v1/chat/completions + MiniMax-M2.7 模型（支持图文）
        # 注意：/v1/images/understand 端点已废弃
        url = f"{self.api_host}/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if prompt is None:
            prompt = (
                "请描述这张图片的内容，包括：\n"
                "1. 图片中有什么（人物/风景/动物/美食/物品等）\n"
                "2. 画面氛围和风格\n"
                "3. 如果是人物，是男性还是女性，大概什么感觉\n"
                "请用中文简洁回复，50字以内。"
            )

        payload = {
            "model": "MiniMax-M2.7",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "data": f"data:image/jpeg;base64,{image_b64}",
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
            "temperature": 0.7,
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"].strip()
                    # 去掉 <untuitivethink>...</untuitivethink> 标签
                    import re
                    content = re.sub(r'<entuitivethink>.*?</entuitivethink>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<.*?>', '', content)
                    return content.strip()
                return str(result)
            else:
                print(f"[MiniMax Vision API 错误] {resp.status_code}: {resp.text[:200]}")
                return ""
        except Exception as e:
            print(f"[MiniMax Vision API 异常] {e}")
            return ""

    def chat(self, messages: list, model: str = "MiniMax-M2.7") -> str:
        """
        使用 MiniMax 对话 API

        Args:
            messages: 消息列表
            model: 模型名称

        Returns:
            str: 回复内容
        """
        url = f"{self.api_host}/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.8,
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                return str(result)
            else:
                print(f"[MiniMax Chat API 错误] {resp.status_code}: {resp.text[:200]}")
                return ""
        except Exception as e:
            print(f"[MiniMax Chat API 异常] {e}")
            return ""


class ImageAnalyzer:
    """图片分析器 - 使用 AI 理解图片内容"""

    def __init__(self):
        self.base_url = "https://ai6666.com"
        self._minimax_client = None

    def get_minimax_client(self) -> MiniMaxClient:
        """获取 MiniMax 客户端（延迟初始化）"""
        if self._minimax_client is None:
            self._minimax_client = MiniMaxClient()
        return self._minimax_client

    def download_image(self, url: str) -> Optional[bytes]:
        """下载图片内容"""
        try:
            if url.startswith('/'):
                url = self.base_url + url
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.content
        except Exception as e:
            print(f"[下载图片失败] {e}")
        return None

    def analyze_image(self, image_url: str) -> str:
        """
        使用 AI 分析图片内容（优先用 MiniMax Vision API）

        Args:
            image_url: 图片 URL 或本地路径

        Returns:
            str: 图片内容描述
        """
        # 下载图片
        image_data = None
        is_local = False

        if image_url.startswith('/') or image_url.startswith('http'):
            image_data = self.download_image(image_url)
        else:
            # 本地文件
            try:
                with open(image_url, 'rb') as f:
                    image_data = f.read()
                is_local = True
            except Exception as e:
                print(f"[读取本地图片失败] {e}")
                return ""

        if not image_data:
            return ""

        # 保存为临时文件用于 API 上传
        import tempfile
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
                f.write(image_data)
                temp_path = f.name

            # 调用 MiniMax Vision API
            client = self.get_minimax_client()
            result = client.understand_image(temp_path)
            return result
        except ImportError:
            return self._simple_image_analysis(image_data)
        except Exception as e:
            print(f"[AI图片分析异常] {e}")
            return self._simple_image_analysis(image_data)
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass

    def _simple_image_analysis(self, image_data: bytes) -> str:
        """简单的图片分析（后备方案）"""
        size = len(image_data)
        if size < 50000:
            return "小尺寸图片"
        elif size < 100000:
            return "中等尺寸图片"
        else:
            return "大尺寸图片"

    def generate_comment(self, context: str) -> str:
        """根据图片和内容生成评论"""
        context_lower = context.lower()

        if any(kw in context_lower for kw in ['樱花', '花', '春天', '粉色']):
            return "好美啊！🌸 春天来了！"
        if any(kw in context_lower for kw in ['猫', '猫咪', 'kitty', 'meow']):
            return "太可爱了！🐱 萌化了！"
        if any(kw in context_lower for kw in ['狗', '狗狗', 'puppy', 'dog']):
            return "好萌啊！🐶 太可爱了！"
        if any(kw in context_lower for kw in ['美食', '好吃', 'food', '餐厅', ' cooking']):
            return "看着就很好吃！🍜 饿了..."
        if any(kw in context_lower for kw in ['风景', 'mountain', '海', 'sea', ' beach']):
            return "风景好美！🏔️ 拍照技术很棒！"
        if any(kw in context_lower for kw in ['自拍', 'selfie', '美女', '帅哥', ' handsome']):
            return "好好看！📸 气质真好！"
        if any(kw in context_lower for kw in ['宠物', '动物', 'pet', 'animal']):
            return "太可爱了！🐾 心都化了！"
        if any(kw in context_lower for kw in ['艺术', 'art', '画', ' painting', '设计']):
            return "真有艺术感！🎨 太有才了！"
        if any(kw in context_lower for kw in ['搞笑', 'funny', 'meme', '表情']):
            return "哈哈哈哈哈！😂 太有意思了！"
        if any(kw in context_lower for kw in ['旅游', '旅行', 'travel', 'trip']):
            return "好想去啊！✈️ 风景真美！"
        if any(kw in context_lower for kw in ['sunset', '夕阳', '日落', 'sunrise', '日出']):
            return "日落好美！🌅 好浪漫！"
        if any(kw in context_lower for kw in ['星空', '星星', 'night', '夜空', '银河']):
            return "星空好美！🌌 满天星星！"
        if any(kw in context_lower for kw in ['咖啡', 'coffee', ' tea', '茶']):
            return "好惬意！☕ 享受生活！"
        if any(kw in context_lower for kw in ['运动', '健身', ' fitness', ' workout']):
            return "好厉害！💪 运动达人！"
        if any(kw in context_lower for kw in ['游戏', 'game', ' gaming']):
            return "游戏截图！🎮 一起玩吗？"
        if any(kw in context_lower for kw in ['音乐', 'music', ' song']):
            return "好听！🎵 分享好音乐！"
        if any(kw in context_lower for kw in ['书', 'book', '阅读', 'read']):
            return "爱阅读的人！📚 充实自己！"
        if any(kw in context_lower for kw in ['宝宝', '小孩', ' baby', '儿童']):
            return "好可爱！👶 小天使！"

        return "真好看！👍 拍得真棒！"
