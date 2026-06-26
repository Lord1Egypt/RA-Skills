"""
抖音发布技能 - 图片生成模块
自动生成与文章主题相关的封面图片
"""

import os
import sys
import random
import requests
from datetime import datetime
from typing import Optional, Tuple

# 添加工作目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    WORKSPACE_DIR, IMAGES_DIR, IMAGE_GENERATION, 
    THEME_CATEGORIES, COVER_STYLES
)

class ImageGenerator:
    """图片生成器"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """创建必要的目录结构"""
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
    def get_theme_keywords(self, theme: str) -> list:
        """
        根据主题获取相关关键词
        
        Args:
            theme: 主题
            
        Returns:
            关键词列表
        """
        # 扩展主题分类
        extended_categories = {
            **THEME_CATEGORIES,
            "美食": ["美食", "烹饪", "料理", "佳肴", "美味", "食材", "做法", "食谱"],
            "运动": ["运动", "健身", "锻炼", "跑步", "游泳", "瑜伽", "户外"],
            "宠物": ["宠物", "动物", "猫咪", "狗狗", "可爱", "萌宠"],
            "音乐": ["音乐", "歌手", "旋律", "节奏", "乐器", "创作"],
            "电影": ["电影", "影评", "剧照", "导演", "演员", "剧情"],
            "设计": ["设计", "创意", "美学", "视觉", "平面", "UI设计"],
            "美妆": ["美妆", "护肤", "彩妆", "产品", "推荐", "教程"],
            "数码": ["数码", "科技", "手机", "相机", "电脑", "设备"]
        }
        
        for category, keywords in extended_categories.items():
            if any(keyword in theme for keyword in keywords):
                return keywords
                
        return [theme]
        
    def get_appropriate_style(self, theme: str) -> str:
        """
        根据主题获取合适的封面风格
        
        Args:
            theme: 主题
            
        Returns:
            封面风格
        """
        # 预设的风格映射
        style_mapping = {
            "科技": ["科技感", "简洁现代", "商务专业"],
            "人工智能": ["科技感", "创意抽象", "未来感"],
            "旅游": ["自然风景", "创意抽象", "艺术感"],
            "美食": ["温馨生活", "创意抽象", "艺术感"],
            "学习": ["简洁现代", "商务专业", "创意抽象"],
            "音乐": ["创意抽象", "艺术感", "现代简约"],
            "电影": ["创意抽象", "艺术感", "电影感"],
            "设计": ["创意抽象", "艺术感", "现代简约"],
            "美妆": ["温馨生活", "创意抽象", "艺术感"],
            "数码": ["科技感", "简洁现代", "商务专业"],
            "运动": ["活力动感", "创意抽象", "科技感"],
            "宠物": ["温馨生活", "创意抽象", "艺术感"]
        }
        
        for category, keywords in style_mapping.items():
            if category in theme:
                return random.choice(keywords)
                
        return random.choice(COVER_STYLES)
        
    def generate_dalle_image(self, prompt: str, style: str = "standard") -> Optional[str]:
        """
        使用DALL-E生成图片
        
        Args:
            prompt: 图片生成提示词
            style: 图片风格
            
        Returns:
            图片文件路径，如果生成失败返回None
        """
        try:
            # 这里需要配置OpenAI API密钥
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("警告: 未找到OpenAI API密钥，将使用默认风格的图片")
                return self.create_simple_image(prompt, style)
                
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 生成图片的请求
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data["data"][0]["url"]
                
                # 下载并保存图片
                image_data = requests.get(image_url).content
                return self.save_generated_image(image_data, prompt)
            else:
                print(f"DALL-E API错误: {response.status_code}, {response.text}")
                return self.create_simple_image(prompt, style)
                
        except Exception as e:
            print(f"生成图片时出错: {e}")
            return self.create_simple_image(prompt, style)
            
    def create_simple_image(self, prompt: str, style: str = "standard") -> Optional[str]:
        """
        创建简单的合成图片（基于风格生成）
        
        Args:
            prompt: 图片描述
            style: 图片风格
            
        Returns:
            图片文件路径
        """
        try:
            # 这里可以使用其他图像生成库，如PIL、diffusers等
            # 目前先创建一个简单的测试图片
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            # 创建基础图片
            width, height = 1024, 1024
            image = Image.new('RGB', (width, height), color='#f0f0f0')
            draw = ImageDraw.Draw(image)
            
            # 添加风格元素
            if style in ["科技感", "未来感", "创意抽象"]:
                for i in range(20):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    size = random.randint(10, 50)
                    draw.ellipse([x, y, x+size, y+size], fill='#4a9cff', outline='#4a9cff', width=2)
                    
                for i in range(15):
                    x1, y1 = random.randint(0, width), random.randint(0, height)
                    x2, y2 = random.randint(0, width), random.randint(0, height)
                    draw.line([x1, y1, x2, y2], fill='#888888', width=2)
                    
                # 添加数字和几何形状
                import numpy as np
                if np.random.random() > 0.5:
                    draw.rectangle([200, 300, 800, 700], fill='#ffffff', outline='#4a9cff', width=3)
                    
            elif style in ["自然风景", "艺术感", "温馨生活"]:
                # 创建渐变背景
                gradient = Image.new('RGB', (width, height), color='#ffffff')
                for y in range(height):
                    color_value = int(200 - (y / height) * 100)
                    color = (color_value, 150 + int((y / height) * 50), 200)
                    for x in range(width):
                        gradient.putpixel((x, y), color)
                        
                image = gradient
                
                # 添加自然元素
                draw.ellipse([200, 300, 800, 700], fill='#ffffff', outline='#4caf50', width=5)
                draw.ellipse([300, 400, 700, 600], fill='#ffffff', outline='#81c784', width=5)
                
            else:
                # 基础风格
                draw.rectangle([100, 100, 900, 900], fill='#f5f5f5', outline='#cccccc', width=3)
                
            # 添加文字
            try:
                # 尝试使用系统字体
                font_size = 60 if len(prompt) < 20 else 40
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttc", font_size)
                wrapped_text = textwrap.wrap(prompt, width=15)
                
                y_text = 400
                for line in wrapped_text:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = (width - text_width) // 2
                    draw.text((x, y_text), line, fill='#333333', font=font)
                    y_text += 70
            except:
                # 备用字体处理
                font = ImageFont.load_default()
                draw.text((200, 500), prompt[:20], fill='#333333', font=font)
                
            # 保存图片
            return self.save_image(image, prompt)
            
        except ImportError:
            print("警告: PIL未安装，无法生成图片")
            return None
        except Exception as e:
            print(f"创建简单图片时出错: {e}")
            return None
            
    def save_generated_image(self, image_data: bytes, prompt: str) -> Optional[str]:
        """
        保存生成的图片
        
        Args:
            image_data: 图片数据
            prompt: 原始提示词
            
        Returns:
            图片文件路径
        """
        try:
            # 创建图片文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cover_generated_{timestamp}.jpg"
            filepath = os.path.join(IMAGES_DIR, filename)
            
            # 保存图片
            with open(filepath, "wb") as f:
                f.write(image_data)
                
            print(f"生成的图片已保存到: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"保存生成的图片时出错: {e}")
            return None
            
    def save_image(self, image, prompt: str) -> Optional[str]:
        """
        保存PIL图像对象
        
        Args:
            image: PIL图像对象
            prompt: 描述文本
            
        Returns:
            图片文件路径
        """
        try:
            # 创建图片文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cover_{prompt.replace(' ', '_')[:20]}_{timestamp}.jpg"
            filepath = os.path.join(IMAGES_DIR, filename)
            
            # 保存图片
            image.save(filepath, 'JPEG', quality=95)
            
            print(f"合成图片已保存到: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"保存合成图片时出错: {e}")
            return None
            
    def generate_and_save_cover(self, theme: str, title: str = None) -> Optional[str]:
        """
        生成并保存封面图片
        
        Args:
            theme: 主题
            title: 文章标题（可选，如果提供则使用标题）
            
        Returns:
            图片文件路径
        """
        # 获取主题关键词
        keywords = self.get_theme_keywords(theme)
        keyword = random.choice(keywords)
        
        # 获取合适的风格
        style = self.get_appropriate_style(theme)
        
        # 构建生成提示词
        prompt = f"{style}风格的{keyword}主题封面设计，高质量，专业摄影，1024x1024"
        
        # 生成图片
        if title and len(title) > 5:
            prompt = f"{style}风格的{title}，{keyword}主题，专业摄影，1024x1024"
            
        print(f"正在生成封面图片: '{prompt}'")
        filepath = self.generate_dalle_image(prompt, style)
        
        return filepath

# 使用示例
if __name__ == "__main__":
    generator = ImageGenerator()
    
    # 测试生成图片
    test_theme = "人工智能"
    filepath = generator.generate_and_save_cover(test_theme)
    print(f"测试封面图片已生成: {filepath}")