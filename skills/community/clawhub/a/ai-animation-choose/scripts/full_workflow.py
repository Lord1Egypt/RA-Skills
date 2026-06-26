#!/usr/bin/env python3
"""
AI Animation Studio - Complete Workflow Script
完整工作流脚本：图片 → 视频 → 配音 → 字幕 → BGM → 最终视频

Author: systiger
Version: 2.2.0
"""

import os
import sys
import json
import time
import asyncio
import requests
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# API Configuration
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
API_KEY = os.getenv("ARK_API_KEY", "")
MODEL_ID = "doubao-seedance-1-0-pro-250528"

# BGM Library
BGM_LIBRARY = {
    "励志热血": [
        ("The Spectre.mp3", "激励人心的战斗音乐"),
        ("Beautiful Now.mp3", "优美励志"),
        ("Run Free.mp3", "自由奔跑"),
    ],
    "儿童动画": [
        ("菊次郎的夏天 - K.Williams.mp3", "温馨童年"),
        ("DJ喜羊羊", "活泼欢快"),
    ],
    "搞笑娱乐": [
        ("喜剧背景音效.mp3", "搞笑氛围"),
    ],
}


class AIAnimationStudio:
    """AI动画工作室"""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not API_KEY:
            raise ValueError("ARK_API_KEY not set!")
        
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        self.scenes = []
        self.video_files = []
        self.audio_files = []
        self.subtitle_list = []
    
    def generate_image(self, prompt: str, scene_id: int) -> str:
        """生成场景图片"""
        print(f"[Scene {scene_id}] 生成图片...")
        
        payload = {
            "model": "doubao-seedream-3-0-t2i-250415",
            "prompt": prompt,
            "n": 1,
            "size": "1920x1080"
        }
        
        response = requests.post(
            f"{BASE_URL}/images/generations",
            headers=self.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"图片生成失败: {response.text}")
        
        result = response.json()
        image_url = result["data"][0]["url"]
        
        # 下载图片
        local_path = self.output_dir / f"scene_{scene_id}.jpg"
        img_response = requests.get(image_url, timeout=30)
        with open(local_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"   ✅ 图片已保存: {local_path}")
        return image_url
    
    def generate_video(self, image_url: str, prompt: str, scene_id: int, duration: int = 5) -> str:
        """生成场景视频（图片转视频）"""
        print(f"[Scene {scene_id}] 生成视频 ({duration}s)...")
        
        payload = {
            "model": MODEL_ID,
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ],
            "ratio": "16:9",
            "duration": duration,
            "watermark": False
        }
        
        # 创建任务
        response = requests.post(
            f"{BASE_URL}/contents/generations/tasks",
            headers=self.headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"视频任务创建失败: {response.text}")
        
        task_id = response.json()["id"]
        print(f"   Task ID: {task_id}")
        
        # 等待完成
        print(f"   等待生成...")
        while True:
            time.sleep(5)
            status_response = requests.get(
                f"{BASE_URL}/contents/generations/tasks/{task_id}",
                headers=self.headers,
                timeout=30
            )
            
            status = status_response.json()
            
            if status["status"] == "succeeded":
                video_url = status["content"]["video_url"]
                
                # 下载视频
                local_path = self.output_dir / f"scene_{scene_id}.mp4"
                video_response = requests.get(video_url, timeout=120)
                with open(local_path, "wb") as f:
                    f.write(video_response.content)
                
                print(f"   ✅ 视频已保存: {local_path}")
                return str(local_path)
                
            elif status["status"] == "failed":
                raise Exception("视频生成失败")
            
            else:
                print(f"   Status: {status['status']}...")
    
    async def generate_tts(self, text: str, scene_id: int, voice: str = "zh-CN-XiaoyiNeural") -> str:
        """生成配音"""
        import edge_tts
        
        print(f"[Scene {scene_id}] 生成配音: {text[:30]}...")
        
        output_path = self.output_dir / f"voice_{scene_id}.mp3"
        
        communicate = edge_tts.Communicate(text, voice, pitch="+50Hz")
        await communicate.save(output_path)
        
        print(f"   ✅ 配音已保存: {output_path}")
        return str(output_path)
    
    def merge_video_audio(self, video_path: str, audio_path: str, scene_id: int) -> str:
        """合并视频和音频"""
        print(f"[Scene {scene_id}] 合并视频和音频...")
        
        output_path = self.output_dir / f"merged_{scene_id}.mp4"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ 已合并: {output_path}")
            return str(output_path)
        else:
            raise Exception(f"合并失败: {result.stderr[:200]}")
    
    def burn_subtitles(self, video_path: str, subtitles: List[Dict], scene_id: int) -> str:
        """烧录字幕到视频"""
        print(f"[Scene {scene_id}] 烧录字幕...")
        
        from subtitle_burner import SubtitleBurner
        
        burner = SubtitleBurner(font_size=42)
        output_path = self.output_dir / f"subtitled_{scene_id}.mp4"
        
        burner.burn_subtitles(video_path, subtitles, str(output_path))
        
        return str(output_path)
    
    def concat_videos(self, video_files: List[str], output_file: str) -> str:
        """合并所有视频"""
        print("合并所有场景视频...")
        
        # 创建 concat 文件
        concat_file = self.output_dir / "concat_list.txt"
        with open(concat_file, "w") as f:
            for vf in video_files:
                f.write(f"file '{vf}'\n")
        
        output_path = self.output_dir / output_file
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:v", "libx264",
            "-preset", "medium",
            "-c:a", "aac",
            "-movflags", "+faststart",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 视频已合并: {output_path}")
            return str(output_path)
        else:
            raise Exception(f"合并失败: {result.stderr[:500]}")
    
    def add_bgm(self, video_path: str, bgm_file: str, output_file: str, bgm_volume: float = 0.3) -> str:
        """添加BGM背景音乐"""
        print(f"添加BGM背景音乐...")
        
        # 获取视频时长
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", video_path],
            capture_output=True,
            text=True
        )
        duration = float(json.loads(result.stdout)["format"]["duration"])
        
        output_path = self.output_dir / output_file
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", bgm_file,
            "-filter_complex",
            f"[1:a]volume={bgm_volume},aloop=loop=-1:size=2e+09[bgm];"
            f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-t", str(duration),
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ BGM已添加: {output_path}")
            return str(output_path)
        else:
            raise Exception(f"BGM添加失败: {result.stderr[:500]}")
    
    def create_animation(
        self,
        scenes: List[Dict],
        style: str = "Marvel superhero comic style",
        bgm_category: str = "励志热血",
        bgm_index: int = 0
    ) -> str:
        """
        创建完整动画
        
        Args:
            scenes: 场景列表 [{"duration": 4, "narration": "配音文本", "image_prompt": "图片提示词", "video_prompt": "视频提示词"}, ...]
            style: 动画风格
            bgm_category: BGM分类
            bgm_index: BGM索引
        
        Returns:
            最终视频路径
        """
        print("🎬 开始制作动画")
        print("=" * 60)
        print(f"场景数量: {len(scenes)}")
        print(f"动画风格: {style}")
        print(f"BGM分类: {bgm_category}")
        print()
        
        # 步骤1: 生成所有场景图片
        print("\n📷 步骤1: 生成场景图片")
        print("-" * 60)
        image_urls = []
        for i, scene in enumerate(scenes, 1):
            full_prompt = f"{style}, {scene['image_prompt']}"
            image_url = self.generate_image(full_prompt, i)
            image_urls.append(image_url)
        
        # 步骤2: 生成所有场景视频
        print("\n🎥 步骤2: 生成场景视频")
        print("-" * 60)
        video_files = []
        for i, scene in enumerate(scenes, 1):
            video_file = self.generate_video(
                image_urls[i-1],
                scene['video_prompt'],
                i,
                scene['duration']
            )
            video_files.append(video_file)
        
        # 步骤3: 生成所有配音
        print("\n🎙️ 步骤3: 生成配音")
        print("-" * 60)
        audio_files = []
        
        async def generate_all_tts():
            tasks = []
            for i, scene in enumerate(scenes, 1):
                tasks.append(self.generate_tts(scene['narration'], i))
            return await asyncio.gather(*tasks)
        
        audio_files = asyncio.run(generate_all_tts())
        
        # 步骤4: 合并视频和音频
        print("\n🔗 步骤4: 合并视频和音频")
        print("-" * 60)
        merged_files = []
        for i, scene in enumerate(scenes, 1):
            merged_file = self.merge_video_audio(video_files[i-1], audio_files[i-1], i)
            merged_files.append(merged_file)
        
        # 步骤5: 合并所有场景
        print("\n🎬 步骤5: 合并所有场景")
        print("-" * 60)
        concat_video = self.concat_videos(merged_files, "final_no_bgm.mp4")
        
        # 步骤6: 添加BGM
        print("\n🎵 步骤6: 添加BGM背景音乐")
        print("-" * 60)
        
        # 选择BGM
        bgm_list = BGM_LIBRARY.get(bgm_category, BGM_LIBRARY["励志热血"])
        bgm_name, bgm_desc = bgm_list[bgm_index % len(bgm_list)]
        bgm_file = Path(r"D:\AI视频资源\音效素材包\卡点音乐") / bgm_name
        
        print(f"BGM: {bgm_name} ({bgm_desc})")
        
        final_video = self.add_bgm(concat_video, str(bgm_file), "final_animation.mp4")
        
        print("\n" + "=" * 60)
        print("🎉 动画制作完成!")
        print(f"最终视频: {final_video}")
        
        return final_video


def main():
    """示例：创建飞天狗大战钢铁猫动画"""
    
    # 定义场景
    scenes = [
        {
            "duration": 4,
            "narration": "城市黄昏，飞天狗与钢铁猫屋顶对峙",
            "image_prompt": "aerial view of futuristic city at dusk, heroic flying dog with white fur and angel wings facing a menacing robotic steel cat with glowing red eyes on a rooftop, dramatic lighting, high contrast, 16:9",
            "video_prompt": "Camera slowly zooms in on the confrontation scene, wind blowing slightly"
        },
        {
            "duration": 4,
            "narration": "钢铁猫眼中红光闪烁，激光束射出",
            "image_prompt": "close-up shot of menacing robotic steel cat with glowing red eyes and metallic silver body, firing a powerful red laser beam from eyes, futuristic city rooftop background, dramatic lighting, high contrast, action scene, 16:9",
            "video_prompt": "Laser beam shoots from cat's eyes, camera shakes slightly"
        },
        {
            "duration": 5,
            "narration": "飞天狗侧身闪避，翅膀展开反击",
            "image_prompt": "heroic flying dog with white fur and angel wings dodging laser beam, wings spread wide, powerful counterattack stance, mid-air action pose, dramatic lighting, high contrast, dynamic action scene, 16:9",
            "video_prompt": "Flying dog dodges gracefully, wings spread wide, counterattack motion"
        },
        {
            "duration": 5,
            "narration": "空中激战，火花四溅",
            "image_prompt": "intense aerial battle scene, flying dog with angel wings fighting robotic steel cat, sparks flying, energy blasts, dynamic combat, dramatic lighting, high contrast, action-packed, 16:9",
            "video_prompt": "Intense aerial combat, sparks flying, dynamic action camera movement"
        },
        {
            "duration": 5,
            "narration": "飞天狗蓄力，释放终极光波",
            "image_prompt": "heroic flying dog with white fur and angel wings powering up, glowing golden energy aura, preparing ultimate attack, dramatic lighting, high contrast, epic moment, 16:9",
            "video_prompt": "Flying dog powering up with glowing energy aura, epic slow motion"
        },
        {
            "duration": 4,
            "narration": "钢铁猫被击飞，坠落爆炸",
            "image_prompt": "robotic steel cat being hit by powerful energy blast, flying backward, explosion debris, defeated pose, dramatic lighting, high contrast, action climax, 16:9",
            "video_prompt": "Steel cat hit by energy blast, explosion debris, flying backward"
        },
        {
            "duration": 3,
            "narration": "飞天狗落地，胜利姿态",
            "image_prompt": "victorious flying dog with white fur and angel wings landing heroically on rooftop, power pose, futuristic city skyline background, dramatic lighting, high contrast, heroic ending, 16:9",
            "video_prompt": "Victorious landing, heroic pose, cape flowing in wind"
        },
    ]
    
    # 创建动画
    studio = AIAnimationStudio(output_dir="output")
    
    final_video = studio.create_animation(
        scenes=scenes,
        style="Marvel superhero comic style",
        bgm_category="励志热血",
        bgm_index=0  # The Spectre
    )
    
    print(f"\n✅ 最终视频: {final_video}")


if __name__ == "__main__":
    main()
