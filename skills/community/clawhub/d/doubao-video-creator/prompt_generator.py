#!/usr/bin/env python3
"""
豆包视频创作助手 - 提示词生成器 v2.0
借鉴 Seedance Storyboard 的专业提示词结构
"""

from typing import Dict, List, Optional
import json


class PromptGenerator:
    """专业提示词生成器"""
    
    def __init__(self):
        # 镜头语言词库
        self.camera_movements = ["推", "拉", "摇", "移", "跟", "环绕", "升降", "希区柯克变焦"]
        self.shot_sizes = ["远景", "全景", "中景", "近景", "特写"]
        self.transitions = ["硬切", "渐变", "匹配剪辑", "特效转场", "无缝渐变"]
        self.special_effects = ["一镜到底", "慢动作", "延时摄影", "粒子效果", "光影流转"]
        
        # 质量词库
        self.quality_words = ["高清写实", "电影级画质", "4K 细节", "专业摄影", "超清质感"]
        self.lighting_words = ["自然光", "逆光", "侧光", "柔光", "戏剧性光影", "黄金时刻"]
        self.atmosphere_words = ["温馨", "科技感", "悬疑", "浪漫", "史诗", "现代", "复古"]
    
    def generate_scene_prompt(
        self,
        scene: Dict,
        style: Dict,
        camera: Optional[Dict] = None,
        action: Optional[Dict] = None,
        sound: Optional[Dict] = None,
        reference_images: Optional[List[str]] = None
    ) -> str:
        """
        生成单个场景的专业提示词
        
        Args:
            scene: 场景信息（description, time_range, duration 等）
            style: 风格信息（style, atmosphere, lighting 等）
            camera: 镜头信息（movement, shot_size 等）
            action: 动作信息（main_action, rhythm 等）
            sound: 声音信息（music, sfx 等）
            reference_images: 参考图片路径列表
            
        Returns:
            prompt: 完整的专业提示词
        """
        # 【整体描述】
        overall = self._generate_overall_description(scene, style)
        
        # 【分镜描述】
        scene_desc = self._generate_scene_description(scene, camera, action, style)
        
        # 【声音说明】
        sound_desc = self._generate_sound_description(sound) if sound else ""
        
        # 【参考素材】
        ref_desc = self._generate_reference_description(reference_images) if reference_images else ""
        
        # 组合完整提示词
        prompt_parts = [overall, scene_desc]
        if sound_desc:
            prompt_parts.append(sound_desc)
        if ref_desc:
            prompt_parts.append(ref_desc)
        
        return "\n\n".join(prompt_parts)
    
    def _generate_overall_description(self, scene: Dict, style: Dict) -> str:
        """生成整体描述"""
        duration = scene.get('duration', 5)
        ratio = scene.get('ratio', '9:16')
        style_name = style.get('style', '现代')
        atmosphere = style.get('atmosphere', '专业氛围')
        
        return f"【整体描述】\n{style_name}风格，{duration}秒，{ratio}，{atmosphere}"
    
    def _generate_scene_description(
        self,
        scene: Dict,
        camera: Optional[Dict],
        action: Optional[Dict],
        style: Dict
    ) -> str:
        """生成分镜描述"""
        time_range = scene.get('time_range', '0-5 秒')
        description = scene.get('description', '')
        
        # 镜头运动
        if camera and camera.get('movement'):
            movement = camera['movement']
            shot_size = camera.get('shot_size', '中景')
            camera_text = f"{shot_size}{movement}镜头"
        else:
            camera_text = "镜头"
        
        # 主体动作
        if action and action.get('main_action'):
            action_text = action['main_action']
        else:
            action_text = "主体动作"
        
        # 光影效果
        lighting = style.get('lighting', '自然光')
        lighting_text = f"{lighting}照明"
        
        # 质量词
        quality = style.get('quality', '高清写实')
        
        # 组合分镜描述
        scene_text = f"【分镜描述】\n{time_range}：{camera_text}，{description}，{action_text}，{lighting_text}，{quality}"
        
        return scene_text
    
    def _generate_sound_description(self, sound: Dict) -> str:
        """生成声音说明"""
        parts = ["【声音说明】"]
        
        if sound.get('music'):
            parts.append(f"配乐：{sound['music']}")
        if sound.get('sfx'):
            parts.append(f"音效：{sound['sfx']}")
        if sound.get('voiceover'):
            parts.append(f"旁白：{sound['voiceover']}")
        
        return "\n".join(parts)
    
    def _generate_reference_description(self, reference_images: List[str]) -> str:
        """生成参考素材说明"""
        if not reference_images:
            return ""
        
        parts = ["【参考素材】"]
        for i, img_path in enumerate(reference_images, 1):
            # 根据路径推测图片类型
            if 'character' in img_path or 'person' in img_path:
                usage = "作为角色形象参考"
            elif 'scene' in img_path or 'background' in img_path:
                usage = "作为场景风格参考"
            elif 'product' in img_path:
                usage = "作为产品外观参考"
            else:
                usage = "作为视觉参考"
            
            parts.append(f"@图片{i} {usage}")
        
        return "\n".join(parts)
    
    def generate_multi_scene_prompt(
        self,
        scenes: List[Dict],
        overall_style: Dict,
        reference_images: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, str]:
        """
        为多个场景生成提示词
        
        Args:
            scenes: 场景列表
            overall_style: 整体风格
            reference_images: 每个场景的参考图片
            
        Returns:
            prompts: 场景 ID 到提示词的映射
        """
        prompts = {}
        
        for scene in scenes:
            scene_id = scene.get('id', 1)
            
            # 获取场景特定信息
            scene_style = overall_style.copy()
            scene_style.update(scene.get('style', {}))
            
            # 获取参考图片
            scene_refs = reference_images.get(str(scene_id), []) if reference_images else []
            
            # 生成提示词
            prompt = self.generate_scene_prompt(
                scene=scene,
                style=scene_style,
                camera=scene.get('camera'),
                action=scene.get('action'),
                sound=scene.get('sound'),
                reference_images=scene_refs
            )
            
            prompts[scene_id] = prompt
        
        return prompts
    
    def optimize_prompt(self, prompt: str, feedback: str) -> str:
        """
        根据反馈优化提示词
        
        Args:
            prompt: 原提示词
            feedback: 用户反馈
            
        Returns:
            optimized_prompt: 优化后的提示词
        """
        # 简单优化逻辑（后续可以增强）
        optimized = prompt
        
        if "太暗" in feedback:
            optimized = optimized.replace("昏暗", "明亮")
            optimized += "，光线充足"
        
        if "不够清晰" in feedback:
            optimized += "，超清 4K 画质，细节清晰"
        
        if "节奏太快" in feedback:
            optimized = optimized.replace("快速", "缓慢")
            optimized += "，节奏舒缓"
        
        return optimized
    
    def get_prompt_suggestions(self, scene_type: str) -> Dict:
        """
        根据场景类型获取提示词建议
        
        Args:
            scene_type: 场景类型（product, story, demo 等）
            
        Returns:
            suggestions: 建议的镜头、动作、风格等
        """
        suggestions = {
            "product": {
                "camera": ["特写", "推镜头", "环绕"],
                "lighting": ["侧光", "柔光", "黄金时刻"],
                "quality": ["高清写实", "电影级画质", "商业广告质感"]
            },
            "story": {
                "camera": ["中景", "近景", "跟镜头"],
                "lighting": ["自然光", "戏剧性光影"],
                "quality": ["电影级画质", "纪录片风格"]
            },
            "demo": {
                "camera": ["中景", "特写", "固定镜头"],
                "lighting": ["自然光", "柔光"],
                "quality": ["高清写实", "清晰直观"]
            }
        }
        
        return suggestions.get(scene_type, suggestions["product"])


# 示例用法
if __name__ == "__main__":
    generator = PromptGenerator()
    
    # 测试场景
    scene = {
        "id": 1,
        "time_range": "0-5 秒",
        "duration": 5,
        "ratio": "9:16",
        "description": "智能手表表盘，光线扫过屏幕展示质感"
    }
    
    style = {
        "style": "现代科技感",
        "atmosphere": "简约商务氛围",
        "lighting": "自然光从侧面射入",
        "quality": "高清写实，电影级画质"
    }
    
    camera = {
        "movement": "从下往上缓缓推近",
        "shot_size": "特写"
    }
    
    action = {
        "main_action": "展示产品细节和质感"
    }
    
    # 生成提示词
    prompt = generator.generate_scene_prompt(
        scene=scene,
        style=style,
        camera=camera,
        action=action,
        reference_images=["/path/to/product.png"]
    )
    
    print("生成的提示词：")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
