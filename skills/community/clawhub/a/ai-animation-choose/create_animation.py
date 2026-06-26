# -*- coding: utf-8 -*-
"""
AI Animation Studio - 动画制作工具
支持两种生成模式：图片转视频 / 图片动画化再生成视频
"""
import subprocess
import os
import json
import re
import time
import shutil
from typing import List, Dict, Optional

class AIAnimationCreator:
    """AI动画制作器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.doubao_script = r"C:\Users\10954\.openclaw\workspace\skills\doubao-media\scripts\doubao_media.py"
        self.bgm_library = {
            "儿童动画": [
                "菊次郎的夏天 - K.Williams.mp3",
                "DJ喜羊羊.mp3",
                "嘟嘟~嘟嘟~哒哒哒.mp3"
            ],
            "励志热血": [
                "Beautiful Now.mp3",
                "The Spectre.mp3",
                "易燃易爆炸.mp3"
            ],
            "搞笑娱乐": [
                "喜剧的搞笑背景音效.mp3",
                "很火的滑稽背景音乐.mp3",
                "爱滴魔力转圈圈.mp3"
            ],
            "浪漫温馨": [
                "恋爱循环.mp3",
                "Hold On (Radio Edit).mp3",
                "雨爱.mp3"
            ],
            "科幻冒险": [
                "The Spectre.mp3",
                "Geisha (Original Mix).mp3",
                "Run Free (feat. IVIE).mp3"
            ]
        }
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_image(self, prompt: str, size: str = "1024x1792") -> Optional[Dict]:
        """生成图片"""
        cmd = [
            "python", self.doubao_script,
            "img", prompt,
            "--size", size
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"  [ERROR] 图片生成失败: {result.stderr[:100]}")
            return None
        
        # 提取URL和路径
        url_match = re.search(r'"image_url":\s*"([^"]+)"', result.stdout)
        path_match = re.search(r'"local_path":\s*"([^"]+)"', result.stdout)
        
        if url_match and path_match:
            return {
                "url": url_match.group(1),
                "path": path_match.group(1)
            }
        return None
    
    def image_to_video(self, image_url: str, animation_prompt: str, 
                       duration: int = 5, ratio: str = "9:16") -> Optional[str]:
        """图片转视频"""
        cmd = [
            "python", self.doubao_script,
            "vid", animation_prompt,
            "--image", image_url,
            "--duration", str(duration),
            "--ratio", ratio
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"  [ERROR] 视频生成失败: {result.stderr[:100]}")
            return None
        
        # 提取视频路径
        path_match = re.search(r'"local_path":\s*"([^"]+)"', result.stdout)
        return path_match.group(1) if path_match else None
    
    def select_bgm(self, category: str = None, random_select: bool = False) -> Optional[str]:
        """
        选择BGM
        
        Args:
            category: BGM分类（儿童动画/励志热血/搞笑娱乐/浪漫温馨/科幻冒险）
            random_select: 是否随机选择
        
        Returns:
            BGM文件路径
        """
        bgm_dir = r"D:\AI视频资源\音效素材包"
        
        if random_select:
            # 随机选择
            all_categories = list(self.bgm_library.keys())
            category = random.choice(all_categories)
        
        if category and category in self.bgm_library:
            bgm_list = self.bgm_library[category]
            bgm_name = random.choice(bgm_list)
            
            # 在卡点音乐目录中查找
            bgm_path = os.path.join(bgm_dir, "卡点音乐", bgm_name)
            if os.path.exists(bgm_path):
                return bgm_path
            
            # 在最新流行音效目录中查找
            bgm_path = os.path.join(bgm_dir, "最新流行音效", bgm_name)
            if os.path.exists(bgm_path):
                return bgm_path
        
        return None
    
    def add_bgm_to_video(self, video_path: str, bgm_path: str, 
                         bgm_volume: float = 0.3, output_path: str = None) -> Optional[str]:
        """
        为最终视频添加BGM（在所有场景合并、配音添加后使用）
        
        工作流程：
        1. 场景1.mp4 + 场景2.mp4 + ... → 合并视频.mp4
        2. 合并视频.mp4 + 配音.mp3 → 视频_配音.mp4
        3. 视频_配音.mp4 + BGM.mp3 → 最终视频.mp4 （本方法）
        
        Args:
            video_path: 已添加配音的视频文件路径
            bgm_path: BGM文件路径
            bgm_volume: BGM音量（0.0-1.0，默认0.3即30%）
            output_path: 输出文件路径
        
        Returns:
            输出文件路径
        """
        if not output_path:
            output_path = video_path.replace('.mp4', '_final.mp4')
        
        # 使用 aloop 让BGM循环以匹配视频时长
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", bgm_path,
            "-filter_complex",
            f"[1:a]volume={bgm_volume},aloop=loop=-1:size=2e+09[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]
        
        print(f"\n[BGM] 添加背景音乐: {os.path.basename(bgm_path)}")
        print(f"  音量: {int(bgm_volume*100)}%")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  [OK] {output_path}")
            return output_path
        else:
            print(f"  [ERROR] {result.stderr[:200]}")
            return None
    
    def create_scene_mode1(self, scene: Dict) -> Optional[str]:
        """
        模式一：图片转视频
        1. 生成图片
        2. 图片直接转视频
        """
        print(f"\n[模式一] 场景{scene['id']}: {scene['name']}")
        
        # 第一步：生成图片
        print(f"  [1/2] 生成图片...")
        img_result = self.generate_image(scene['image_prompt'])
        
        if not img_result:
            return None
        
        print(f"  [OK] {img_result['path']}")
        time.sleep(2)
        
        # 第二步：图片转视频
        print(f"  [2/2] 图片转视频...")
        video_path = self.image_to_video(
            img_result['url'],
            scene['animation_prompt'],
            scene.get('duration', 5)
        )
        
        if video_path:
            # 复制到输出目录
            dest = os.path.join(self.output_dir, f"scene_{scene['id']:02d}.mp4")
            shutil.copy(video_path, dest)
            print(f"  [OK] {dest}")
            return dest
        
        return None
    
    def create_scene_mode2(self, scene: Dict) -> Optional[str]:
        """
        模式二：图片动画化再生成视频
        1. 生成动画风格图片（在prompt中加入动画化指令）
        2. 图片转视频（添加更强的动画效果）
        """
        print(f"\n[模式二] 场景{scene['id']}: {scene['name']}")
        
        # 第一步：生成动画风格图片
        print(f"  [1/2] 生成动画风格图片...")
        
        # 在prompt中加入动画化关键词
        animated_prompt = f"{scene['image_prompt']}，动态效果，生动活泼，充满运动感"
        img_result = self.generate_image(animated_prompt)
        
        if not img_result:
            return None
        
        print(f"  [OK] {img_result['path']}")
        time.sleep(2)
        
        # 第二步：图片转视频（更强的动画效果）
        print(f"  [2/2] 生成动态视频...")
        
        # 增强动画prompt
        enhanced_animation = f"{scene['animation_prompt']}，流畅自然的动态效果，电影级运镜"
        video_path = self.image_to_video(
            img_result['url'],
            enhanced_animation,
            scene.get('duration', 5)
        )
        
        if video_path:
            # 复制到输出目录
            dest = os.path.join(self.output_dir, f"scene_{scene['id']:02d}.mp4")
            shutil.copy(video_path, dest)
            print(f"  [OK] {dest}")
            return dest
        
        return None
    
    def create_animation(self, scenes: List[Dict], mode: int = 1) -> List[str]:
        """
        创建完整动画
        
        Args:
            scenes: 场景列表
            mode: 1=图片转视频模式，2=图片动画化再生成视频模式
        
        Returns:
            生成的视频路径列表
        """
        print(f"\n{'='*50}")
        print(f"AI Animation Studio - 模式{mode}")
        print(f"{'='*50}\n")
        
        videos = []
        
        for scene in scenes:
            if mode == 1:
                video = self.create_scene_mode1(scene)
            else:
                video = self.create_scene_mode2(scene)
            
            if video:
                videos.append(video)
            
            time.sleep(3)  # 避免请求过快
        
        print(f"\n[完成] 生成了 {len(videos)}/{len(scenes)} 个场景")
        return videos


def get_default_scenes():
    """获取默认场景配置（小小科学家）"""
    return [
        {
            "id": 1,
            "name": "小明的房间",
            "image_prompt": "皮克斯动画风格，明亮温暖的儿童房，阳光透过窗户洒进来，房间里有各种齿轮、螺丝、电线，墙上贴着科学海报，蓝色和橙色主色调，3D卡通渲染，全景镜头",
            "animation_prompt": "镜头缓慢推进，阳光从窗户照射进来，窗帘轻轻飘动，桌上的齿轮和螺丝微微震动",
            "duration": 5
        },
        {
            "id": 2,
            "name": "小明特写",
            "image_prompt": "皮克斯动画风格，8岁小男孩特写，戴着圆圆的眼镜，眼睛闪闪发光充满兴奋，手里拿着画满图纸的纸，背景虚化，温暖的光线，卡通3D渲染，特写镜头",
            "animation_prompt": "小男孩眨眼睛，眼镜反光，嘴巴说话动作，表情充满兴奋和期待",
            "duration": 4
        },
        {
            "id": 3,
            "name": "组装过程",
            "image_prompt": "皮克斯动画风格，小男孩在工作室里忙碌，桌上摆放着旧闹钟、吸尘器零件、彩色围裙，小男孩拿着螺丝刀专注工作，背景有散落的零件，温馨的灯光，3D卡通渲染，中景镜头",
            "animation_prompt": "小男孩的手拿起螺丝刀，螺丝轻微旋转，围裙飘动，专注工作的动作",
            "duration": 5
        },
        {
            "id": 4,
            "name": "机器人诞生",
            "image_prompt": "皮克斯动画风格，可爱的机器人站在房间中央，身体由闹钟和吸尘器组成，穿着花围裙，头顶有小灯泡闪闪发光，眼睛是两个圆圆的表盘，充满童趣，背景是小明兴奋的表情，明亮色彩，3D卡通渲染，全景镜头",
            "animation_prompt": "机器人站起来，头顶灯泡闪烁，眼睛眨呀眨，身体轻微晃动，充满生命力",
            "duration": 5
        },
        {
            "id": 5,
            "name": "机器人特写",
            "image_prompt": "皮克斯动画风格，可爱的机器人特写，圆形表盘眼睛眨呀眨，嘴巴是个小喇叭，头顶灯泡闪烁，金属质感但柔和可爱，背景是温馨的家，3D卡通渲染，特写镜头",
            "animation_prompt": "机器人眼睛转动，嘴巴喇叭震动说话，灯泡闪烁发出光芒",
            "duration": 4
        },
        {
            "id": 6,
            "name": "妈妈回家",
            "image_prompt": "皮克斯动画风格，温馨的客厅，地板闪闪发光，妈妈穿着职业装刚进门，惊讶又开心的表情，小明站在旁边自豪地笑，机器人站在一旁鞠躬，温暖的橙黄色调，3D卡通渲染，中景镜头",
            "animation_prompt": "妈妈走进门，惊讶的表情变化，小明微笑，机器人鞠躬动作",
            "duration": 5
        },
        {
            "id": 7,
            "name": "结尾",
            "image_prompt": "皮克斯动画风格，小男孩站在房间中央自信地笑，身后是各种发明图纸，旁边是可爱的机器人，窗外是星空和月亮，充满希望和梦想的氛围，温暖的蓝紫色调，3D卡通渲染，结尾画面，全景镜头",
            "animation_prompt": "窗外星星闪烁，小明自信微笑，机器人挥手，灯光渐暗，温馨结尾",
            "duration": 4
        }
    ]


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI动画制作工具")
    parser.add_argument("--mode", type=int, choices=[1, 2], default=1,
                       help="生成模式：1=图片转视频，2=图片动画化再生成视频")
    parser.add_argument("--output", type=str, default="D:/AI视频资源/output/animation",
                       help="输出目录")
    parser.add_argument("--scene", type=int, default=None,
                       help="只生成指定场景（1-7），不指定则生成全部")
    
    args = parser.parse_args()
    
    # 创建动画制作器
    creator = AIAnimationCreator(args.output)
    
    # 获取场景
    scenes = get_default_scenes()
    if args.scene:
        scenes = [s for s in scenes if s['id'] == args.scene]
    
    # 生成动画
    videos = creator.create_animation(scenes, args.mode)
    
    print(f"\n视频保存位置: {args.output}")
