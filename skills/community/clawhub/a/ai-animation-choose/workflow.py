# -*- coding: utf-8 -*-
"""
AI Animation Studio - 动画制作工作流
从故事到动画的全流程自动化
"""

import os
import json
import random
from pathlib import Path
from typing import List, Dict, Optional

# 导入资源索引
from resource_index import (
    load_storyboard_template,
    load_style_prompts,
    load_shot_prompts,
    load_ai_prompts,
    get_random_effect,
    get_random_audio
)

class AIAnimationStudio:
    """AI动画工作室"""
    
    def __init__(self, story: str):
        self.story = story
        self.config = {
            "style": None,
            "aspect_ratio": "9:16",  # 默认竖版
            "duration": "30s",
            "bgm_type": "轻松",
            "voice_style": {}
        }
        self.scenes = []
        self.shots = []
        
        # 加载资源
        self.templates = load_storyboard_template()
        self.styles = load_style_prompts()
        self.shot_prompts = load_shot_prompts()
        self.ai_prompts = load_ai_prompts()
    
    def ask_preferences(self) -> Dict:
        """询问用户偏好"""
        questions = {
            "style": {
                "question": "选择动画风格：",
                "options": [
                    {"label": "宫崎骏风", "desc": "自然色彩+清新构图+手绘质感"},
                    {"label": "皮克斯风", "desc": "明亮色彩+卡通建模+情感流动"},
                    {"label": "诺兰电影风", "desc": "非线性时间轴+暗色调"},
                    {"label": "童话故事风", "desc": "柔和色调+梦幻氛围"},
                ]
            },
            "aspect_ratio": {
                "question": "选择视频比例：",
                "options": [
                    {"label": "竖版 9:16", "desc": "抖音/快手/小红书"},
                    {"label": "横版 16:9", "desc": "B站/YouTube"},
                    {"label": "方形 1:1", "desc": "微信视频号"},
                ]
            },
            "duration": {
                "question": "选择视频时长：",
                "options": [
                    {"label": "30秒", "desc": "短视频"},
                    {"label": "1-3分钟", "desc": "中等长度"},
                    {"label": "5分钟+", "desc": "长视频"},
                ]
            }
        }
        
        return questions
    
    def set_config(self, **kwargs):
        """设置配置"""
        self.config.update(kwargs)
    
    def analyze_story(self) -> List[Dict]:
        """分析故事，提取场景"""
        # 简单分句（实际应使用AI分析）
        sentences = [s.strip() for s in self.story.replace('。', '。\n').split('\n') if s.strip()]
        
        scenes = []
        for i, sentence in enumerate(sentences[:10]):  # 最多10个场景
            # 根据内容选择模板
            template = self._select_template(sentence)
            
            scene = {
                "scene_id": i + 1,
                "content": sentence,
                "template": template,
                "shot_type": self._select_shot(sentence),
                "style": self._get_style_prompt(),
                "duration": 3  # 默认3秒
            }
            scenes.append(scene)
        
        self.scenes = scenes
        return scenes
    
    def _select_template(self, content: str) -> Dict:
        """根据内容选择分镜模板"""
        # 简单关键词匹配
        keywords = {
            "采访": "街头采访",
            "医疗": "医疗检查",
            "儿童": "儿童活动",
            "农村": "农村劳作",
            "美食": "美食制作",
            "旅行": "旅行探险"
        }
        
        for keyword, scene_type in keywords.items():
            if keyword in content:
                for t in self.templates:
                    if t.get("场景") == scene_type:
                        return t
        
        # 随机返回一个模板
        return random.choice(self.templates) if self.templates else {}
    
    def _select_shot(self, content: str) -> str:
        """根据内容选择镜头类型"""
        # 根据内容特征选择镜头
        if "特写" in content or "表情" in content:
            return "特写镜头"
        elif "全景" in content or "场景" in content:
            return "全景镜头"
        elif "细节" in content:
            return "微距镜头"
        else:
            return random.choice(["中景镜头", "特写镜头", "全景镜头"])
    
    def _get_style_prompt(self) -> str:
        """获取风格提示词"""
        style_name = self.config.get("style", "")
        
        for s in self.styles:
            if style_name in s.get("category", "") or style_name in s.get("prompt", ""):
                return s.get("prompt", "")
        
        # 返回随机风格
        return random.choice(self.styles).get("prompt", "") if self.styles else ""
    
    def generate_shot_prompts(self) -> List[Dict]:
        """为每个场景生成画面提示词"""
        shots = []
        
        for scene in self.scenes:
            # 组合提示词
            prompt = {
                "scene_id": scene["scene_id"],
                "content": scene["content"],
                "shot_prompt": f"{scene['shot_type']}：{scene['content'][:50]}",
                "style_prompt": scene["style"],
                "full_prompt": f"{scene['shot_type']}，{scene['style']}，{scene['content'][:100]}",
                "duration": scene["duration"]
            }
            shots.append(prompt)
        
        self.shots = shots
        return shots
    
    def assign_voices(self, characters: List[str]) -> Dict:
        """为角色分配音色"""
        voice_presets = {
            "儿童": {"voice": "zh-CN-XiaoyiNeural", "pitch": "+15%"},
            "少年": {"voice": "zh-CN-YunxiNeural", "pitch": "+5%"},
            "成年男": {"voice": "zh-CN-YunxiNeural", "pitch": "default"},
            "成年女": {"voice": "zh-CN-XiaoxiaoNeural", "pitch": "default"},
            "老年男": {"voice": "zh-CN-YunxiNeural", "pitch": "-10%"},
            "老年女": {"voice": "zh-CN-XiaoxiaoNeural", "pitch": "-10%"},
            "旁白": {"voice": "zh-CN-YunyangNeural", "pitch": "default"},
        }
        
        assignments = {}
        for i, char in enumerate(characters):
            # 根据角色名推测类型
            char_type = "成年男"
            if any(k in char for k in ["小", "孩", "童"]):
                char_type = "儿童"
            elif any(k in char for k in ["奶奶", "婆婆", "老妇"]):
                char_type = "老年女"
            elif any(k in char for k in ["爷爷", "公公", "老翁"]):
                char_type = "老年男"
            elif any(k in char for k in ["女", "她", "妈", "姐", "妹"]):
                char_type = "成年女"
            
            assignments[char] = voice_presets.get(char_type, voice_presets["成年男"])
        
        # 添加旁白
        assignments["旁白"] = voice_presets["旁白"]
        
        return assignments
    
    def select_effects(self) -> Dict:
        """选择特效素材"""
        effects = {
            "transitions": [],
            "overlays": [],
            "backgrounds": []
        }
        
        # 根据场景数量选择转场
        for i in range(len(self.scenes) - 1):
            transition = get_random_effect("转场")
            if transition:
                effects["transitions"].append(transition)
        
        # 选择背景
        background = get_random_effect("背景")
        if background:
            effects["backgrounds"].append(background)
        
        # 选择叠加特效
        overlay = get_random_effect("特效")
        if overlay:
            effects["overlays"].append(overlay)
        
        return effects
    
    def select_audio(self) -> Dict:
        """选择音效素材"""
        audio = {
            "bgm": None,
            "sfx": [],
            "voice_prompts": []
        }
        
        # 选择背景音乐
        bgm = get_random_audio("bgm")
        if bgm:
            audio["bgm"] = bgm
        
        # 为每个场景选择音效
        for scene in self.scenes:
            sfx = get_random_audio("sfx")
            if sfx:
                audio["sfx"].append({
                    "scene_id": scene["scene_id"],
                    "path": sfx
                })
        
        return audio
    
    def export_script(self, output_path: str = None) -> str:
        """导出完整脚本"""
        if not output_path:
            output_path = f"animation_script_{hash(self.story) % 10000}.json"
        
        script = {
            "story": self.story,
            "config": self.config,
            "scenes": self.scenes,
            "shots": self.shots,
            "effects": self.select_effects(),
            "audio": self.select_audio()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def generate_production_checklist(self) -> List[str]:
        """生成制作清单"""
        checklist = [
            "✅ 第一步：需求确认",
            "  - 风格选择完成",
            "  - 视频比例确定",
            "  - 时长设定",
            "",
            "⬜ 第二步：脚本分解",
            f"  - 共 {len(self.scenes)} 个场景待处理",
            "",
            "⬜ 第三步：画面生成",
            "  - 使用豆包/即梦生成每个分镜",
            "  - 确保人物风格一致",
            "",
            "⬜ 第四步：动画生成",
            "  - 将静态画面转为动态视频",
            "  - 添加镜头运动",
            "",
            "⬜ 第五步：配音字幕",
            "  - 为角色分配音色",
            "  - 生成字幕时间轴",
            "",
            "⬜ 第六步：特效合成",
            "  - 添加转场特效",
            "  - 添加背景音乐",
            "  - 最终合成输出",
        ]
        
        return checklist


# 使用示例
if __name__ == "__main__":
    # 测试
    story = """
    在一片神秘的森林里，住着一只可爱的小精灵。
    她有着透明的翅膀，闪闪发光。
    每天清晨，她都会飞到花丛中采集露珠。
    有一天，她遇到了一个迷路的小男孩...
    """
    
    studio = AIAnimationStudio(story)
    
    # 显示问题
    questions = studio.ask_preferences()
    for key, q in questions.items():
        print(f"\n{q['question']}")
        for i, opt in enumerate(q['options']):
            print(f"  {chr(65+i)}. {opt['label']} - {opt['desc']}")
    
    # 设置配置
    studio.set_config(style="宫崎骏风", aspect_ratio="9:16", duration="30s")
    
    # 分析故事
    scenes = studio.analyze_story()
    print(f"\n=== 分析结果 ===")
    print(f"共提取 {len(scenes)} 个场景")
    for scene in scenes[:3]:
        print(f"\n场景{scene['scene_id']}: {scene['content'][:30]}...")
        print(f"  镜头: {scene['shot_type']}")
        print(f"  风格: {scene['style'][:30]}...")
    
    # 生成提示词
    shots = studio.generate_shot_prompts()
    print(f"\n=== 画面提示词 ===")
    for shot in shots[:2]:
        print(f"\n场景{shot['scene_id']}:")
        print(f"  完整提示词: {shot['full_prompt'][:80]}...")
    
    # 导出脚本
    output = studio.export_script()
    print(f"\n脚本已导出: {output}")
    
    # 生成清单
    checklist = studio.generate_production_checklist()
    print("\n=== 制作清单 ===")
    for item in checklist:
        print(item)
