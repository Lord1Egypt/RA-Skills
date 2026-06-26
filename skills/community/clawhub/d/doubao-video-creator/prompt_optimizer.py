#!/usr/bin/env python3
"""
视频提示词优化器
根据脚本和参考图生成详细的视频生成提示词
"""

import json


class PromptOptimizer:
    """提示词优化器"""
    
    def __init__(self):
        # 质量增强词
        self.quality_boosters = {
            "写实": "高清写实，电影级画质，4K 细节，专业摄影，自然光影",
            "科技感": "未来科技感，霓虹灯光，金属质感，赛博朋克风格",
            "温馨": "温暖色调，柔和光线，家庭氛围，治愈系风格",
            "专业": "商务专业，简洁大气，高端质感，企业级水准",
            "活力": "鲜艳色彩，动感十足，青春活力，运动风格"
        }
        
        # 镜头语言
        self.camera_moves = {
            "特写": "镜头特写，聚焦细节，微距拍摄",
            "全景": "广角全景，宏大场景，鸟瞰视角",
            "移动": "镜头缓缓移动，平稳推拉，流畅运镜",
            "定格": "镜头定格，静态构图，经典画面"
        }
    
    def optimize_scene_prompt(self, scene_script, key_elements=None):
        """
        优化场景提示词
        
        Args:
            scene_script: 场景脚本信息
            key_elements: 已确认的关键元素
            
        Returns:
            optimized_prompt: 优化后的提示词
        """
        # 基础描述
        base = scene_script.get("description", "")
        style = scene_script.get("style", "写实")
        
        # 构建提示词
        prompt_parts = []
        
        # 1. 风格
        prompt_parts.append(f"{style}风格")
        
        # 2. 画面描述
        if base:
            prompt_parts.append(base)
        
        # 3. 参考元素
        if key_elements:
            if key_elements.get("characters"):
                confirmed_chars = [c for c in key_elements["characters"] if c.get("status") == "confirmed"]
                if confirmed_chars:
                    prompt_parts.append("人物形象参考已确认的主角")
            
            if key_elements.get("scenes"):
                confirmed_scenes = [s for s in key_elements["scenes"] if s.get("status") == "confirmed"]
                if confirmed_scenes:
                    prompt_parts.append("场景风格参考已确认的背景")
            
            if key_elements.get("objects"):
                confirmed_objects = [o for o in key_elements["objects"] if o.get("status") == "confirmed"]
                if confirmed_objects:
                    prompt_parts.append("物品参考已确认的产品")
        
        # 4. 镜头语言（根据场景类型）
        if "特写" in base or "close" in base.lower():
            prompt_parts.append(self.camera_moves["特写"])
        elif "全景" in base or "wide" in base.lower():
            prompt_parts.append(self.camera_moves["全景"])
        elif "移动" in base or "缓缓" in base:
            prompt_parts.append(self.camera_moves["移动"])
        else:
            prompt_parts.append("镜头缓缓移动，平稳流畅")
        
        # 5. 质量增强
        if style in self.quality_boosters:
            prompt_parts.append(self.quality_boosters[style])
        else:
            prompt_parts.append("高清写实，电影级画质，4K 细节")
        
        # 组合提示词
        optimized_prompt = "，".join(prompt_parts)
        
        return optimized_prompt
    
    def generate_prompt_variants(self, base_prompt, count=2):
        """
        生成多个提示词版本供选择
        
        Args:
            base_prompt: 基础提示词
            count: 生成数量
            
        Returns:
            variants: 提示词变体列表
        """
        variants = [base_prompt]  # 原版
        
        for i in range(count):
            if i == 0:
                # 简洁版
                variant = base_prompt.split("，")[0] + "，" + base_prompt.split("，")[-1]
                variants.append(variant)
            elif i == 1:
                # 详细版
                variant = base_prompt + "，精细细节，专业调色，大师级作品"
                variants.append(variant)
        
        return variants
    
    def explain_prompt(self, prompt):
        """
        解释提示词会生成什么画面
        
        Args:
            prompt: 提示词
            
        Returns:
            explanation: 画面描述
        """
        explanation = []
        
        # 分析提示词元素
        if "写实" in prompt:
            explanation.append("📸 写实风格，像真实拍摄的画面")
        
        if "科技感" in prompt:
            explanation.append("🔮 科技感风格，未来感十足")
        
        if "镜头特写" in prompt or "特写" in prompt:
            explanation.append("🔍 镜头特写，聚焦细节")
        
        if "缓缓移动" in prompt:
            explanation.append("📹 镜头缓慢移动，流畅运镜")
        
        if "4K" in prompt or "高清" in prompt:
            explanation.append("✨ 高清画质，4K 细节")
        
        # 总结
        if not explanation:
            explanation.append("🎬 根据提示词生成 4 秒视频")
        
        return "\n".join(explanation)


def main():
    """测试函数"""
    optimizer = PromptOptimizer()
    
    # 测试脚本
    scene_script = {
        "description": "现代办公室，白色办公桌，桌上放置智能手表",
        "style": "现代科技感"
    }
    
    # 优化提示词
    optimized = optimizer.optimize_scene_prompt(scene_script)
    
    print("=" * 60)
    print("优化后的提示词：")
    print("=" * 60)
    print(optimized)
    print()
    
    # 解释会生成什么
    print("=" * 60)
    print("这个提示词会生成：")
    print("=" * 60)
    print(optimizer.explain_prompt(optimized))
    print()
    
    # 生成变体
    variants = optimizer.generate_prompt_variants(optimized, count=2)
    
    print("=" * 60)
    print("提示词变体：")
    print("=" * 60)
    for i, variant in enumerate(variants, 1):
        print(f"\n版本{i}:")
        print(variant)


if __name__ == "__main__":
    main()
