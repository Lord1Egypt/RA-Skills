#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 儿童故事视频生成器
根据主题自动生成故事 → ComfyUI 图片 → 语音 → 视频
"""

import os
import sys
import json
import time
import random
import requests
import websocket
import uuid
from pathlib import Path
from datetime import datetime

# 配置
COMFYUI_URL = "http://127.0.0.1:8188"
COMFYUI_WS_URL = "ws://127.0.0.1:8188/ws"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
ASSETS_DIR = Path(__file__).parent.parent / "assets"

class StoryVideoGenerator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
        self.client_id = str(uuid.uuid4())
        
    def generate_story(self, theme, num_scenes=5):
        """生成儿童故事并分段"""
        
        characters = ["小兔子", "小熊", "小猫", "小狗", "小狐狸", "小松鼠"]
        settings = ["美丽的森林", "彩虹花园", "魔法城堡", "阳光草原", "星空湖畔"]
        
        char1, char2 = random.sample(characters, 2)
        setting = random.choice(settings)
        
        story_structure = {
            "title": f"{char1}和{char2}的{theme}冒险",
            "theme": theme,
            "characters": [char1, char2],
            "setting": setting,
            "scenes": []
        }
        
        # 生成场景
        scenes = [
            {
                "text": f"从前，在{setting}里，住着{char1}和{char2}。它们是最好的朋友。",
                "mood": "温馨",
                "duration": 5
            },
            {
                "text": f"有一天，{char1}发现了一个关于{theme}的秘密，它决定和{char2}一起去探索。",
                "mood": "好奇",
                "duration": 6
            },
            {
                "text": f"它们在旅途中遇到了一些小困难，但是{char1}和{char2}互相帮助，勇敢地克服了。",
                "mood": "勇敢",
                "duration": 7
            },
            {
                "text": f"最终，它们找到了答案，学会了{theme}的真正意义。",
                "mood": "开心",
                "duration": 6
            },
            {
                "text": f"从此以后，{char1}和{char2}成为了更亲密的朋友，它们的故事也被大家传颂。",
                "mood": "温馨",
                "duration": 5
            }
        ]
        
        story_structure["scenes"] = scenes[:num_scenes]
        
        return story_structure
    
    def text_to_prompt(self, scene_text, mood, characters, setting):
        """将场景文本转为 ComfyUI 提示词"""
        
        # 基础风格
        base_style = "children's book illustration, cute cartoon style, soft colors, gentle lighting, high quality, detailed, whimsical, storybook art"
        
        # 根据场景情绪调整
        mood_modifiers = {
            "温馨": "warm lighting, cozy atmosphere, soft pastel colors, heartwarming",
            "好奇": "bright lighting, sense of wonder, discovery, magical sparkles",
            "勇敢": "dynamic composition, heroic pose, determination, courage",
            "开心": "joyful, vibrant colors, smiling characters, cheerful atmosphere",
            "神秘": "soft shadows, magical glow, mysterious atmosphere, enchanted"
        }
        
        mood_prompt = mood_modifiers.get(mood, "cute and friendly")
        
        # 背景环境描述 - 更丰富的背景细节
        setting_descriptions = {
            "美丽的森林": "lush green forest with tall trees, sunlight filtering through leaves, wildflowers, gentle stream, distant mountains, wide landscape",
            "彩虹花园": "colorful garden with rainbow flowers, butterflies, fairy-tale greenhouse, stone paths, ancient trees, panoramic view",
            "魔法城堡": "magical castle with towers and flags, stone walls, flagstone courtyard, dramatic clouds, distant kingdom, expansive vista",
            "阳光草原": "golden meadow with tall grass, rolling hills, wildflowers, distant farmhouse, blue sky with fluffy clouds, wide horizon",
            "星空湖畔": "serene lakeside at night, reflection on water, starry sky, moonlight, willow trees, gentle waves, mystical atmosphere"
        }
        
        setting_prompt = setting_descriptions.get(setting, f"{setting} with rich environmental details, wide landscape view")
        
        # 构建提示词 - 强调背景环境，角色占比小
        prompt = (
            f"{base_style}, {mood_prompt}, "
            f"wide angle shot, expansive background, {setting_prompt}, "
            f"small cute {', '.join(characters)} in distance, "
            f"beautiful environment dominates frame, "
            f"landscape-oriented composition, depth of field, "
            f"{scene_text[:80]}"
        )
        
        # 负面提示词 - 避免角色占比太大
        negative = (
            "scary, dark, violent, adult content, low quality, blurry, distorted, ugly, scary faces, "
            "close-up on character, character takes up most of frame, tight frame, cropped composition, "
            "no background, empty background, plain background"
        )
        
        return {
            "positive": prompt,
            "negative": negative,
            "width": 1024,
            "height": 576,  # 16:9 适合视频
            "seed": random.randint(1, 999999999)
        }
    
    def queue_prompt(self, prompt_workflow):
        """发送提示词到 ComfyUI"""
        p = {"prompt": prompt_workflow, "client_id": self.client_id}
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(p).encode('utf-8')
        
        try:
            req = requests.post(f"{COMFYUI_URL}/prompt", headers=headers, data=data)
            print(f"   📡 ComfyUI 响应: {req.status_code}")
            if req.status_code != 200:
                print(f"   ❌ 错误: {req.text[:300]}")
            return req.json()
        except Exception as e:
            print(f"❌ 无法连接到 ComfyUI: {e}")
            print(f"请确保 ComfyUI 在 {COMFYUI_URL} 运行")
            return None
    
    def get_history(self, prompt_id):
        """获取生成历史"""
        try:
            with requests.get(f"{COMFYUI_URL}/history/{prompt_id}") as response:
                return response.json()
        except:
            return {}
    
    def get_image(self, filename, subfolder, folder_type):
        """下载生成的图片"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = requests.compat.urlencode(data)
        
        try:
            response = requests.get(f"{COMFYUI_URL}/view?{url_values}")
            return response.content
        except:
            return None
    
    def generate_image(self, prompt_data, output_path):
        """使用 ComfyUI 生成单张图片"""
        
        # 加载基础 workflow
        workflow = self.load_workflow()
        if not workflow:
            print("❌ 无法加载 workflow")
            return False
        
        # 更新 workflow 中的提示词
        for node_id, node in workflow.items():
            if node.get("class_type") == "CLIPTextEncode":
                # 根据节点 ID 判断：1 是 positive，2 是 negative
                if node_id == "1":
                    workflow[node_id]["inputs"]["text"] = prompt_data["positive"]
                elif node_id == "2":
                    workflow[node_id]["inputs"]["text"] = prompt_data["negative"]
            elif node.get("class_type") == "EmptyLatentImage":
                workflow[node_id]["inputs"]["width"] = prompt_data["width"]
                workflow[node_id]["inputs"]["height"] = prompt_data["height"]
            elif node.get("class_type") == "KSampler":
                workflow[node_id]["inputs"]["seed"] = prompt_data["seed"]
        
        # 发送请求
        response = self.queue_prompt(workflow)
        if not response:
            return False
        
        prompt_id = response.get('prompt_id')
        print(f"⏳ 生成中... (ID: {prompt_id[:8]})")
        
        # 等待生成完成
        ws = websocket.WebSocket()
        try:
            ws.connect(f"{COMFYUI_WS_URL}?clientId={self.client_id}")
            
            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        data = message['data']
                        if data['node'] is None and data['prompt_id'] == prompt_id:
                            break
            
            ws.close()
        except Exception as e:
            print(f"⚠️ WebSocket 错误: {e}")
            ws.close()
        
        # 获取生成的图片
        history = self.get_history(prompt_id)
        if prompt_id in history:
            outputs = history[prompt_id].get('outputs', {})
            for node_id, node_output in outputs.items():
                if 'images' in node_output:
                    for image in node_output['images']:
                        image_data = self.get_image(
                            image['filename'], 
                            image['subfolder'], 
                            image['type']
                        )
                        if image_data:
                            with open(output_path, 'wb') as f:
                                f.write(image_data)
                            print(f"✅ 已保存: {output_path}")
                            return True
        
        return False
    
    def load_workflow(self):
        """加载 ComfyUI workflow"""
        workflow_path = ASSETS_DIR / "basic_workflow.json"
        if workflow_path.exists():
            with open(workflow_path, 'r') as f:
                return json.load(f)
        
        # 如果没有 workflow 文件，返回基础 workflow
        return self.create_basic_workflow()
    
    def create_basic_workflow(self):
        """创建基础 workflow"""
        return {
            "1": {
                "inputs": {"text": "", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "2": {
                "inputs": {"text": "", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {
                    "seed": 123456,
                    "steps": 25,
                    "cfg": 8.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["1", 0],
                    "negative": ["2", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {"ckpt_name": "counterfeitV30_v30.safetensors"},
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {"width": 1024, "height": 576, "batch_size": 1},
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode"
            },
            "7": {
                "inputs": {"filename_prefix": "ComfyUI", "images": ["6", 0]},
                "class_type": "SaveImage"
            }
        }
    
    def generate_tts(self, text, output_path):
        """生成语音 (使用 macOS say 命令)"""
        # 简化版：使用 macOS 内置 TTS
        # 后期可以集成更好的 TTS（如 Azure、ElevenLabs）
        
        temp_aiff = output_path.replace('.mp3', '.aiff')
        
        # 使用 say 命令生成语音
        cmd = f'say -v "Ting-Ting" -o "{temp_aiff}" "{text}"'
        os.system(cmd)
        
        # 转换为 mp3
        cmd = f'ffmpeg -i "{temp_aiff}" -codec:a libmp3lame -qscale:a 2 "{output_path}" -y 2>/dev/null'
        os.system(cmd)
        
        # 删除临时文件
        if os.path.exists(temp_aiff):
            os.remove(temp_aiff)
        
        return os.path.exists(output_path)
    
    def create_video(self, story_data, image_paths, audio_paths, output_path):
        """合成最终视频"""
        
        # 创建临时文件列表
        list_file = self.output_dir / "temp_concat_list.txt"
        with open(list_file, 'w') as f:
            for i, (img_path, audio_path, scene) in enumerate(zip(image_paths, audio_paths, story_data['scenes'])):
                duration = scene['duration']
                f.write(f"file '{img_path}'\n")
                f.write(f"duration {duration}\n")
        
        # 使用 ffmpeg 合成视频
        # 图片 + 音频 + 字幕
        cmd = f'''
        ffmpeg -f concat -safe 0 -i "{list_file}" 
        -i "{self.output_dir / 'temp_audio.mp3'}" 
        -vf "fps=30,format=yuv420p" 
        -c:v libx264 -c:a aac -shortest 
        "{output_path}" -y
        '''
        
        # 简化版本：只合成图片序列
        cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -vf "fps=30,format=yuv420p" -c:v libx264 -pix_fmt yuv420p "{output_path}" -y 2>&1'
        
        result = os.system(cmd)
        
        # 清理临时文件
        if list_file.exists():
            list_file.unlink()
        
        return result == 0
    
    def run(self, theme="友谊"):
        """运行完整流程"""
        
        print(f"🎬 开始生成 '{theme}' 主题的儿童故事视频\n")
        
        # 1. 生成故事
        print("📖 正在生成故事...")
        story = self.generate_story(theme)
        print(f"   标题: {story['title']}")
        print(f"   场景数: {len(story['scenes'])}\n")
        
        # 2. 生成图片
        print("🎨 正在使用 ComfyUI 生成图片...")
        image_paths = []
        for i, scene in enumerate(story['scenes']):
            print(f"\n   场景 {i+1}/{len(story['scenes'])}")
            print(f"   文本: {scene['text'][:50]}...")
            
            prompt_data = self.text_to_prompt(
                scene['text'], 
                scene['mood'], 
                story['characters'], 
                story['setting']
            )
            
            img_path = self.output_dir / f"scene_{i+1:02d}.png"
            
            if self.generate_image(prompt_data, img_path):
                image_paths.append(img_path)
            else:
                print(f"   ❌ 图片生成失败，使用占位图")
                image_paths.append(None)
            
            time.sleep(1)  # 避免请求过快
        
        # 3. 生成语音
        print("\n🔊 正在生成语音旁白...")
        audio_paths = []
        for i, scene in enumerate(story['scenes']):
            audio_path = self.output_dir / f"scene_{i+1:02d}.mp3"
            if self.generate_tts(scene['text'], str(audio_path)):
                audio_paths.append(audio_path)
            else:
                audio_paths.append(None)
        
        # 4. 合成视频
        print("\n🎞️ 正在合成视频...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = self.output_dir / f"story_{theme}_{timestamp}.mp4"
        
        # 保存故事 JSON
        story_json_path = self.output_dir / f"story_{theme}_{timestamp}.json"
        with open(story_json_path, 'w', encoding='utf-8') as f:
            json.dump(story, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 完成！")
        print(f"   故事: {story_json_path}")
        print(f"   图片: {self.output_dir}/scene_*.png")
        print(f"   音频: {self.output_dir}/scene_*.mp3")
        
        return story, image_paths, audio_paths


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='ComfyUI 儿童故事视频生成器')
    parser.add_argument('--theme', '-t', default='友谊', help='故事主题')
    parser.add_argument('--scenes', '-s', type=int, default=5, help='场景数量')
    
    args = parser.parse_args()
    
    generator = StoryVideoGenerator()
    generator.run(args.theme)


if __name__ == "__main__":
    main()