#!/usr/bin/env python3
"""
提示词生成器 for ComfyUI
"""

import json
import random
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PromptGenerator:
    """提示词生成和优化引擎"""
    
    def __init__(self, templates_file: str = None):
        self.templates_file = templates_file
        self.templates = self._load_templates()
        self.style_presets = self._load_style_presets()
        self.quality_presets = self._load_quality_presets()
        
    def _load_templates(self) -> Dict:
        """加载提示词模板"""
        templates = {
            "realistic_photo": {
                "template": "professional photography, {subject}, {quality}, realistic, detailed, sharp focus, cinematic lighting",
                "variables": ["subject", "quality", "lighting", "background", "perspective"],
                "defaults": {
                    "quality": "8k, high resolution, photorealistic",
                    "lighting": "cinematic lighting",
                    "perspective": "wide angle shot"
                }
            },
            "anime_style": {
                "template": "{subject}, anime style, vibrant colors, detailed background, {artist} style, {quality}",
                "variables": ["subject", "artist", "quality", "background", "mood"],
                "defaults": {
                    "artist": "studio ghibli",
                    "quality": "masterpiece, best quality, detailed",
                    "mood": "whimsical, magical"
                }
            },
            "cyberpunk": {
                "template": "cyberpunk style, {subject}, neon lights, futuristic city, rain, night scene, {quality}",
                "variables": ["subject", "quality", "time", "weather", "mood"],
                "defaults": {
                    "quality": "8k, cinematic, dramatic lighting",
                    "time": "night",
                    "weather": "rain"
                }
            },
            "oil_painting": {
                "template": "oil painting of {subject}, brush strokes, textured, gallery style, {artist} style, {quality}",
                "variables": ["subject", "artist", "quality", "style", "frame"],
                "defaults": {
                    "artist": "van gogh",
                    "quality": "masterpiece, detailed, artistic",
                    "frame": "golden frame"
                }
            },
            "watercolor": {
                "template": "watercolor painting of {subject}, soft edges, transparent colors, artistic, {quality}",
                "variables": ["subject", "quality", "color_palette", "paper_texture"],
                "defaults": {
                    "quality": "delicate, beautiful, artistic",
                    "paper_texture": "textured watercolor paper"
                }
            },
            "sketch": {
                "template": "sketch drawing of {subject}, pencil lines, artistic, {quality}",
                "variables": ["subject", "quality", "paper_type", "shading"],
                "defaults": {
                    "quality": "detailed, clean lines, artistic",
                    "paper_type": "sketchbook paper"
                }
            }
        }
        
        # 如果指定了模板文件，从文件加载
        if self.templates_file:
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    file_templates = json.load(f)
                    templates.update(file_templates)
            except Exception as e:
                logger.warning(f"无法加载模板文件: {e}")
        
        return templates
    
    def _load_style_presets(self) -> Dict:
        """加载风格预设"""
        return {
            "artists": [
                "van gogh",
                "claude monet",
                "pablo picasso",
                "salvador dali",
                "studio ghibli",
                "moebius",
                "hayao miyazaki",
                "katsuhiro otomo",
                "takashi murakami"
            ],
            "art_styles": [
                "impressionism",
                "cubism",
                "surrealism",
                "expressionism",
                "pop art",
                "art nouveau",
                "art deco",
                "minimalism",
                "abstract"
            ],
            "photography_styles": [
                "cinematic",
                "documentary",
                "portrait",
                "landscape",
                "street photography",
                "macro",
                "black and white",
                "vintage"
            ]
        }
    
    def _load_quality_presets(self) -> Dict:
        """加载质量预设"""
        return {
            "basic": "basic quality, simple",
            "standard": "standard quality, good details",
            "high": "high quality, detailed, sharp",
            "excellent": "excellent quality, 8k, masterpiece",
            "ultra": "ultra quality, photorealistic, perfect"
        }
    
    def generate(self, template_name: str, variables: Dict = None) -> str:
        """生成提示词"""
        if template_name not in self.templates:
            raise ValueError(f"模板不存在: {template_name}")
        
        template_data = self.templates[template_name]
        template = template_data["template"]
        
        # 合并变量
        merged_vars = template_data.get("defaults", {}).copy()
        if variables:
            merged_vars.update(variables)
        
        # 确保主题存在
        if "subject" not in merged_vars:
            merged_vars["subject"] = "a beautiful scene"
        
        # 确保质量存在
        if "quality" not in merged_vars:
            merged_vars["quality"] = self.quality_presets["high"]
        
        # 替换变量
        for key, value in merged_vars.items():
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
        
        # 清理未使用的占位符
        template = re.sub(r'\{.*?\}', '', template)
        template = re.sub(r'\s+', ' ', template).strip()
        
        # 优化提示词
        template = self.optimize(template)
        
        return template
    
    def optimize(self, prompt: str) -> str:
        """优化提示词"""
        # 分割成单词
        words = [w.strip() for w in prompt.split(',') if w.strip()]
        
        # 移除重复词
        unique_words = []
        seen = set()
        
        for word in words:
            word_lower = word.lower()
            if word_lower not in seen:
                seen.add(word_lower)
                unique_words.append(word)
        
        # 重新组合
        optimized = ', '.join(unique_words)
        
        # 确保有质量标签
        quality_keywords = ["8k", "high resolution", "detailed", "sharp", "masterpiece", "best quality"]
        has_quality = any(keyword in optimized.lower() for keyword in quality_keywords)
        
        if not has_quality:
            optimized += ", " + ", ".join(quality_keywords[:3])
        
        # 确保有适当的长度
        if len(optimized.split()) < 10:
            # 添加一些通用修饰词
            modifiers = [
                "detailed",
                "sharp focus",
                "professional",
                "artistic"
            ]
            optimized += ", " + ", ".join(modifiers[:2])
        
        # 限制长度
        if len(optimized) > 400:
            words = optimized.split(', ')
            optimized = ', '.join(words[:20])  # 限制到前20个词
        
        return optimized
    
    def generate_variants(self, base_prompt: str, num_variants: int = 3) -> List[str]:
        """生成提示词变体"""
        variants = []
        
        # 变体修饰词
        composition_modifiers = [
            "wide angle shot",
            "close-up shot",
            "dynamic composition",
            "symmetrical composition",
            "from above perspective",
            "from below perspective",
            "low angle",
            "high angle",
            "panoramic view",
            "macro shot"
        ]
        
        lighting_modifiers = [
            "cinematic lighting",
            "dramatic lighting",
            "soft lighting",
            "golden hour lighting",
            "blue hour lighting",
            "neon lighting",
            "studio lighting",
            "natural lighting"
        ]
        
        effect_modifiers = [
            "with bokeh effect",
            "with lens flare",
            "with motion blur",
            "with depth of field",
            "with soft focus",
            "with vignette effect",
            "with film grain",
            "with chromatic aberration"
        ]
        
        for i in range(num_variants):
            variant = base_prompt
            
            # 添加随机修饰词
            if random.random() > 0.3:  # 70%概率添加构图修饰
                mod = random.choice(composition_modifiers)
                variant += f", {mod}"
            
            if random.random() > 0.4:  # 60%概率添加光照修饰
                mod = random.choice(lighting_modifiers)
                variant += f", {mod}"
            
            if random.random() > 0.5:  # 50%概率添加效果修饰
                mod = random.choice(effect_modifiers)
                variant += f", {mod}"
            
            # 优化变体
            variant = self.optimize(variant)
            variants.append(variant)
        
        return variants
    
    def analyze(self, prompt: str) -> Dict:
        """分析提示词"""
        analysis = {
            "length_chars": len(prompt),
            "word_count": len(prompt.split()),
            "comma_count": prompt.count(','),
            "has_quality_tags": False,
            "has_style": False,
            "has_composition": False,
            "has_lighting": False,
            "quality_score": 0,
            "suggestions": []
        }
        
        # 检查质量标签
        quality_keywords = ["8k", "high resolution", "detailed", "sharp", "masterpiece", "best quality", "photorealistic"]
        found_quality = [kw for kw in quality_keywords if kw in prompt.lower()]
        analysis["has_quality_tags"] = len(found_quality) > 0
        analysis["quality_score"] = len(found_quality)
        
        # 检查风格
        style_keywords = ["style", "painting", "sketch", "drawing", "art", "photo", "photography"]
        analysis["has_style"] = any(keyword in prompt.lower() for keyword in style_keywords)
        
        # 检查构图
        composition_keywords = ["close-up", "wide angle", "from above", "low angle", "composition", "perspective", "view"]
        analysis["has_composition"] = any(keyword in prompt.lower() for keyword in composition_keywords)
        
        # 检查光照
        lighting_keywords = ["lighting", "light", "sunlight", "shadow", "illumination"]
        analysis["has_lighting"] = any(keyword in prompt.lower() for keyword in lighting_keywords)
        
        # 生成建议
        if not analysis["has_quality_tags"]:
            analysis["suggestions"].append("添加质量标签: 8k, high resolution, detailed")
        
        if not analysis["has_style"]:
            analysis["suggestions"].append("添加风格描述: painting style, photo style, etc.")
        
        if not analysis["has_composition"]:
            analysis["suggestions"].append("添加构图描述: wide angle, close-up, etc.")
        
        if not analysis["has_lighting"]:
            analysis["suggestions"].append("添加光照描述: cinematic lighting, soft lighting, etc.")
        
        if analysis["word_count"] < 10:
            analysis["suggestions"].append("提示词较短，添加更多细节")
        
        if analysis["word_count"] > 50:
            analysis["suggestions"].append("提示词较长，考虑精简")
        
        return analysis
    
    def get_available_templates(self) -> List[str]:
        """获取可用模板列表"""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name: str) -> Optional[Dict]:
        """获取模板信息"""
        if template_name in self.templates:
            return self.templates[template_name]
        return None

# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="提示词生成器")
    parser.add_argument("--template", type=str, help="模板名称")
    parser.add_argument("--subject", type=str, default="a beautiful landscape", help="主题")
    parser.add_argument("--variants", type=int, default=3, help="生成变体数量")
    parser.add_argument("--analyze", type=str, help="分析提示词")
    parser.add_argument("--list", action="store_true", help="列出可用模板")
    
    args = parser.parse_args()
    
    generator = PromptGenerator()
    
    if args.list:
        print("可用模板:")
        for template in generator.get_available_templates():
            info = generator.get_template_info(template)
            print(f"  • {template}: {info.get('template', '')[:50]}...")
    
    elif args.analyze:
        print(f"分析提示词: {args.analyze}")
        analysis = generator.analyze(args.analyze)
        print(f"字符数: {analysis['length_chars']}")
        print(f"单词数: {analysis['word_count']}")
        print(f"质量分数: {analysis['quality_score']}")
        print(f"建议: {analysis['suggestions']}")
    
    elif args.template:
        variables = {"subject": args.subject}
        prompt = generator.generate(args.template, variables)
        print(f"生成的提示词: {prompt}")
        
        if args.variants > 0:
            variants = generator.generate_variants(prompt, args.variants)
            print(f"\n生成 {args.variants} 个变体:")
            for i, variant in enumerate(variants, 1):
                print(f"  {i}. {variant}")