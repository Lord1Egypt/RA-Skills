#!/usr/bin/env python3
"""
ClawValue 图片生成模块

使用阿里云万象（Wanx）API 生成龙虾主题趣味图片。

功能：
- 根据用户评估结果生成个性化龙虾图片
- 支持多种风格：赛博朋克、简约、卡通等
- 自动生成提示词

参考文档:
https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
import random


# =============================================================================
# 常量定义
# =============================================================================

# API 端点（北京地域）
WANX_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

# 模型名称
WANX_MODEL = 'wan2.6-t2i'

# 默认图片尺寸
DEFAULT_SIZE = '1280*1280'

# Icon尺寸（生成后缩放）
ICON_SIZE = '1280*1280'
ICON_OUTPUT_SIZE = (64, 64)  # 最终输出尺寸


# =============================================================================
# 提示词模板
# =============================================================================

class LobsterPromptTemplates:
    """
    龙虾主题图片提示词模板
    
    根据用户等级和使用风格生成不同的图片。
    """
    
    # 基础风格模板
    STYLES = {
        'cartoon': {
            'name': '卡通风',
            'prefix': '可爱的卡通风格,Q版角色设计,圆润的线条,鲜艳明亮的色彩,',
            'suffix': '，数字插画风格,扁平化设计,暖色调背景,童趣感,不需要真实感'
        },
        'cyberpunk': {
            'name': '赛博朋克风',
            'prefix': '赛博朋克风格，霓虹灯光，未来科技感，',
            'suffix': '，紫色蓝色渐变背景，发光线条，数字元素'
        },
        'minimalist': {
            'name': '简约风',
            'prefix': '简约扁平化设计，干净背景，',
            'suffix': '，柔和渐变色，现代感'
        },
        'realistic': {
            'name': '写实风',
            'prefix': '高清写实摄影，细节丰富，',
            'suffix': '，自然光影，专业构图'
        },
        'fantasy': {
            'name': '奇幻风',
            'prefix': '奇幻插画风格，魔法元素，',
            'suffix': '，梦幻色彩，神秘氛围'
        }
    }
    
    # 默认风格
    DEFAULT_STYLE = 'cartoon'
    
    # 场景模板（根据等级）- 全部使用卡通风格
    SCENES = {
        1: {
            'scene': '一只刚孵化的小龙虾宝宝,大大的圆眼睛,可爱的小钳子,好奇地看着世界,探索周围',
            'props': '旁边漂浮着简单的工具图标,发光的星星点缀',
            'mood': '萌新探索'
        },
        2: {
            'scene': '一只可爱的卡通龙虾,手持小工具,正在认真学习,表情专注可爱',
            'props': '桌上有迷你的代码屏幕和技术文档图标,周围有气泡提示',
            'mood': '努力学习中'
        },
        3: {
            'scene': '一只自信的卡通龙虾,坐在工位上,多屏操作,露出满意的笑容',
            'props': '周围有多个技能图标悬浮,数据流动的粒子效果',
            'mood': '得心应手'
        },
        4: {
            'scene': '一只酷炫的卡通机械龙虾,戴着科技眼镜,掌控全局,表情自信',
            'props': '背后是数据流和自动化流程图,能量光环',
            'mood': '效率大师'
        },
        5: {
            'scene': '一只传说中的龙虾大师,金色发光的外壳,头戴皇冠,威风凛凛',
            'props': '坐在科技宝座上,周围环绕着工具和技能光环,烟花绽放',
            'mood': '传说级存在'
        }
    }
    
    # 特殊道具（根据成就）
    ACHIEVEMENT_PROPS = {
        'skill_master': '，身边漂浮着多个技能图标',
        'automation_pro': '，面前有自动运转的机器',
        'multi_channel': '，多屏幕显示不同平台',
        'power_user': '，闪电环绕，能量充沛',
        'early_adopter': '，戴着探索者帽子'
    }
    
    @classmethod
    def generate_prompt(
        cls,
        level: int,
        style: str = 'cyberpunk',
        achievements: List[str] = None,
        custom_prompt: str = None
    ) -> str:
        """
        生成完整的提示词
        
        Args:
            level: 用户等级 (1-5)
            style: 风格名称
            achievements: 成就列表
            custom_prompt: 自定义补充
            
        Returns:
            完整的提示词
        """
        # 获取风格模板
        style_info = cls.STYLES.get(style, cls.STYLES['cyberpunk'])
        
        # 获取场景模板
        scene_info = cls.SCENES.get(level, cls.SCENES[1])
        
        # 构建基础提示词
        prompt = f"{style_info['prefix']}{scene_info['scene']}"
        
        # 添加道具
        props = scene_info['props']
        if achievements:
            for ach in achievements[:2]:  # 最多添加2个成就道具
                if ach in cls.ACHIEVEMENT_PROPS:
                    props += cls.ACHIEVEMENT_PROPS[ach]
        prompt += f"，{props}"
        
        # 添加风格后缀
        prompt += style_info['suffix']
        
        # 添加自定义内容
        if custom_prompt:
            prompt += f"，{custom_prompt}"
        
        return prompt
    
    @classmethod
    def get_random_style(cls) -> str:
        """随机获取一个风格"""
        return random.choice(list(cls.STYLES.keys()))


# =============================================================================
# 图片生成器
# =============================================================================

@dataclass
class ImageGenerationResult:
    """图片生成结果"""
    success: bool
    image_url: str = ''
    request_id: str = ''
    error: str = ''
    prompt: str = ''
    style: str = ''


class WanxImageGenerator:
    """
    阿里云万象图片生成器
    
    使用 DashScope API 生成图片。
    
    Example:
        >>> generator = WanxImageGenerator(api_key='sk-xxx')
        >>> result = generator.generate_lobster(level=3)
        >>> if result.success:
        ...     print(f"图片URL: {result.image_url}")
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化图片生成器
        
        Args:
            api_key: DashScope API Key，可从环境变量 DASHSCOPE_API_KEY 获取
        """
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            # 尝试从 TOOLS.md 配置获取
            self.api_key = self._get_api_key_from_config()
    
    def _get_api_key_from_config(self) -> Optional[str]:
        """从配置文件获取 API Key"""
        # 首先检查环境变量
        env_key = os.getenv('DASHSCOPE_API_KEY')
        if env_key:
            return env_key
        
        # 检查常见的配置位置
        config_paths = [
            os.path.expanduser('~/.openclaw/workspace/TOOLS.md'),
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # 查找 DashScope API Key
                    import re
                    # 尝试多种格式匹配
                    patterns = [
                        # 匹配 "### 阿里云百炼" 后面的 "- **API Key**: `xxx`"
                        r'阿里云百炼.*?\n.*?API Key[`:\s*]+([a-zA-Z0-9-]+)',
                        # 匹配 DashScope 标题后的 API Key
                        r'DashScope.*?\n.*?API Key[`:\s*]+([a-zA-Z0-9-]+)',
                        # 通用格式
                        r'API Key[`:\s]+`?([a-zA-Z0-9-]+)`?',
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                        if match:
                            return match.group(1)
                except Exception:
                    pass
        
        return None
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = '',
        size: str = DEFAULT_SIZE,
        n: int = 1,
        prompt_extend: bool = True,
        watermark: bool = False
    ) -> ImageGenerationResult:
        """
        生成图片
        
        Args:
            prompt: 正向提示词
            negative_prompt: 反向提示词
            size: 图片尺寸
            n: 生成数量
            prompt_extend: 是否开启智能改写
            watermark: 是否添加水印
            
        Returns:
            ImageGenerationResult 生成结果
        """
        if not self.api_key:
            return ImageGenerationResult(
                success=False,
                error='未配置 DashScope API Key，请设置 DASHSCOPE_API_KEY 环境变量'
            )
        
        # 构建请求
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': WANX_MODEL,
            'input': {
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'text': prompt}
                        ]
                    }
                ]
            },
            'parameters': {
                'prompt_extend': prompt_extend,
                'watermark': watermark,
                'n': n,
                'negative_prompt': negative_prompt,
                'size': size
            }
        }
        
        try:
            response = requests.post(
                WANX_API_URL,
                headers=headers,
                json=payload,
                timeout=120  # 图片生成可能需要较长时间
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get('output', {}).get('finished'):
                choices = result.get('output', {}).get('choices', [])
                if choices:
                    image_url = choices[0].get('message', {}).get('content', [{}])[0].get('image', '')
                    return ImageGenerationResult(
                        success=True,
                        image_url=image_url,
                        request_id=result.get('request_id', ''),
                        prompt=prompt
                    )
            
            # 处理错误
            error_msg = result.get('message', result.get('code', '未知错误'))
            return ImageGenerationResult(
                success=False,
                error=str(error_msg),
                request_id=result.get('request_id', '')
            )
            
        except requests.Timeout:
            return ImageGenerationResult(
                success=False,
                error='请求超时，图片生成可能需要较长时间'
            )
        except Exception as e:
            return ImageGenerationResult(
                success=False,
                error=str(e)
            )
    
    def generate_achievement_icon(
        self,
        achievement_name: str,
        achievement_desc: str
    ) -> ImageGenerationResult:
        """
        生成成就图标
        
        Args:
            achievement_name: 成就名称（如"技能大师"）
            achievement_desc: 成就描述
            
        Returns:
            ImageGenerationResult 生成结果
        """
        # 构建icon提示词 - 简洁的图标风格
        prompt = f"一个精美的成就图标，{achievement_name}，{achievement_desc}，扁平化设计，简洁的图形符号，明亮的渐变色背景，居中构图，无文字，图标设计风格，适合小尺寸显示"
        
        negative_prompt = "复杂细节，文字，水印，照片级渲染，阴影，模糊，噪点"
        
        result = self.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            size=ICON_SIZE
        )
        
        result.style = 'Icon'
        return result
    
    def generate_lobster(
        self,
        level: int,
        style: str = None,
        achievements: List[str] = None,
        custom_prompt: str = None
    ) -> ImageGenerationResult:
        """
        生成龙虾主题图片
        
        Args:
            level: 用户等级 (1-5)
            style: 风格名称，不指定则默认卡通风格
            achievements: 成就列表
            custom_prompt: 自定义补充
            
        Returns:
            ImageGenerationResult 生成结果
        """
        # 默认使用卡通风格
        if not style:
            style = self.DEFAULT_STYLE
        
        # 生成提示词
        prompt = LobsterPromptTemplates.generate_prompt(
            level=level,
            style=style,
            achievements=achievements,
            custom_prompt=custom_prompt
        )
        
        # 反向提示词 - 强调不要真实感
        negative_prompt = '真实照片,写实风格,模糊,变形,多余肢体,文字,水印,签名,恐怖,暗黑,血腥,过于复杂的细节,照片级渲染'
        
        # 生成图片
        result = self.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt
        )
        result.style = LobsterPromptTemplates.STYLES.get(style, {}).get('name', style)
        
        return result


# =============================================================================
# CLI 测试
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🦞 龙虾图片生成测试")
    print("=" * 60)
    
    # 测试提示词生成
    print("\n📝 测试提示词生成:")
    for level in range(1, 6):
        prompt = LobsterPromptTemplates.generate_prompt(
            level=level,
            style='cyberpunk',
            achievements=['skill_master']
        )
        print(f"\n等级 {level}:")
        print(f"  {prompt[:80]}...")
    
    # 测试图片生成（需要 API Key）
    generator = WanxImageGenerator()
    
    if generator.api_key:
        print("\n🎨 测试图片生成...")
        result = generator.generate_lobster(level=3)
        
        if result.success:
            print(f"✅ 生成成功!")
            print(f"   风格: {result.style}")
            print(f"   URL: {result.image_url}")
        else:
            print(f"❌ 生成失败: {result.error}")
    else:
        print("\n⚠️ 未配置 API Key，跳过图片生成测试")
        print("   请设置环境变量: export DASHSCOPE_API_KEY=sk-xxx")