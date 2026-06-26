#!/usr/bin/env python3
"""
关键元素参考图生成器
使用通义万相 2.7 生成人物、场景、物品的参考图

模型: wan2.7-image-pro (2026-04-01 上线)
- 支持 4K 输出
- 文字渲染更强
- 主体一致性更好
- 复杂指令遵循更优
"""

import requests
import base64
import os
import subprocess
from datetime import datetime

# 配置
API_KEY = "sk-d05aba5a2dae4453b97ed07fdb983e5a"
WANXIANG_SCRIPT = "/root/.openclaw/workspace/wanxiang_generate.py"


class ElementGenerator:
    """关键元素生成器"""
    
    def __init__(self):
        self.api_key = API_KEY
        self.output_dir = "/root/.openclaw/workspace/doubao-video-temp/elements"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_character(self, description, style="写实"):
        """
        生成人物参考图
        
        Args:
            description: 人物描述（如"年轻白领男性，30 岁左右，商务休闲装扮"）
            style: 风格（写实/插画/3D）
            
        Returns:
            (success, image_path)
        """
        prompt = f"{style}风格，{description}，正面照，高清细节，专业摄影"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.output_dir}/character_{timestamp}.png"
        
        return self._generate_image(prompt, output_path)
    
    def generate_scene(self, description, style="写实"):
        """
        生成场景参考图
        
        Args:
            description: 场景描述（如"现代健身房，明亮光线，简约风格"）
            style: 风格（写实/插画/3D）
            
        Returns:
            (success, image_path)
        """
        prompt = f"{style}风格，{description}，高清细节，环境氛围感"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.output_dir}/scene_{timestamp}.png"
        
        return self._generate_image(prompt, output_path)
    
    def generate_object(self, description, style="写实"):
        """
        生成物品参考图
        
        Args:
            description: 物品描述（如"智能手表，银色表壳，黑色表带"）
            style: 风格（写实/插画/3D）
            
        Returns:
            (success, image_path)
        """
        prompt = f"{style}风格，{description}，产品摄影，白色背景，高清细节"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.output_dir}/object_{timestamp}.png"
        
        return self._generate_image(prompt, output_path)
    
    def _generate_image(self, prompt, output_path):
        """
        调用通义万相 API 生成图片
        
        Args:
            prompt: 提示词
            output_path: 输出路径
            
        Returns:
            (success, image_path)
        """
        print(f"🎨 生成图片：{prompt[:50]}...")
        
        try:
            # 调用 wanxiang_generate.py 脚本
            result = subprocess.run(
                ["python3", WANXIANG_SCRIPT, prompt, output_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ 图片生成成功：{output_path}")
                
                # 显示文件大小
                size_mb = os.path.getsize(output_path) / 1024 / 1024
                print(f"   文件大小：{size_mb:.2f} MB")
                
                return True, output_path
            else:
                print(f"❌ 图片生成失败：{result.stderr}")
                return False, None
                
        except subprocess.TimeoutExpired:
            print("⏰ 生成超时（60 秒）")
            return False, None
        except Exception as e:
            print(f"❌ 生成异常：{e}")
            return False, None
    
    def generate_variants(self, element_type, description, count=2, style="写实"):
        """
        生成多个版本供选择
        
        Args:
            element_type: "character", "scene", 或 "object"
            description: 描述
            count: 生成数量
            style: 风格
            
        Returns:
            images: [(success, image_path), ...]
        """
        images = []
        
        for i in range(count):
            print(f"\n生成版本 {i+1}/{count}...")
            
            # 添加变化描述
            if i == 0:
                variant_desc = description
            elif i == 1:
                variant_desc = f"{description}，略有不同"
            else:
                variant_desc = f"{description}，另一种风格"
            
            if element_type == "character":
                success, path = self.generate_character(variant_desc, style)
            elif element_type == "scene":
                success, path = self.generate_scene(variant_desc, style)
            else:
                success, path = self.generate_object(variant_desc, style)
            
            images.append((success, path))
        
        return images


def main():
    """测试函数"""
    generator = ElementGenerator()
    
    # 测试生成人物
    print("=" * 60)
    print("测试：生成人物参考图")
    print("=" * 60)
    
    success, path = generator.generate_character(
        "年轻白领男性，30 岁左右，商务休闲装扮，微笑",
        style="写实"
    )
    
    if success:
        print(f"\n✅ 人物参考图已生成：{path}")
    else:
        print("\n❌ 人物参考图生成失败")
    
    # 测试生成场景
    print("\n" + "=" * 60)
    print("测试：生成场景参考图")
    print("=" * 60)
    
    success, path = generator.generate_scene(
        "现代健身房，明亮光线，简约风格，运动器材",
        style="写实"
    )
    
    if success:
        print(f"\n✅ 场景参考图已生成：{path}")
    else:
        print("\n❌ 场景参考图生成失败")


if __name__ == "__main__":
    main()
