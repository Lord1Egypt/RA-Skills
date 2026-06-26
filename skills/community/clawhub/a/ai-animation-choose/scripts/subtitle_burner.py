#!/usr/bin/env python3
"""
Subtitle Burner - 字幕烧录工具
使用 Pillow 在视频帧上绘制字幕，解决 ffmpeg 中文编码问题

Author: systiger
Version: 1.0.0
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import tempfile
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class SubtitleBurner:
    """字幕烧录类"""
    
    def __init__(self, font_path: str = None, font_size: int = 42):
        """
        初始化字幕烧录器
        
        Args:
            font_path: 字体文件路径（默认使用微软雅黑）
            font_size: 字体大小
        """
        self.font_size = font_size
        self.font_path = font_path or "C:/Windows/Fonts/msyh.ttc"
        
        # 加载字体
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except Exception as e:
            print(f"⚠️ 字体加载失败: {e}")
            self.font = ImageFont.load_default()
    
    def get_video_info(self, video_path: str) -> dict:
        """获取视频信息"""
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,duration",
            "-of", "json",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        stream = data["streams"][0]
        
        # 解析帧率
        fps_parts = stream["r_frame_rate"].split("/")
        fps = int(fps_parts[0]) / int(fps_parts[1]) if len(fps_parts) == 2 else 30
        
        return {
            "width": int(stream["width"]),
            "height": int(stream["height"]),
            "fps": fps,
            "duration": float(stream.get("duration", 0))
        }
    
    def draw_subtitle_on_frame(self, frame_path: str, subtitle_text: str, output_path: str):
        """
        在视频帧上绘制字幕
        
        Args:
            frame_path: 输入帧图片路径
            subtitle_text: 字幕文本
            output_path: 输出帧图片路径
        """
        # 加载图片
        img = Image.open(frame_path)
        draw = ImageDraw.Draw(img)
        
        # 去除标点符号
        import re
        subtitle_text = re.sub(
            r'[，。！？、；：""''（）【】《》,.!?;:\'\"\(\)\[\]<>]',
            '',
            subtitle_text
        )
        
        if not subtitle_text:
            img.save(output_path)
            return
        
        # 计算字幕位置（底部居中）
        bbox = draw.textbbox((0, 0), subtitle_text, font=self.font)
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) // 2
        y = img.height - 50 - self.font_size
        
        # 绘制描边（黑色，2-3像素）
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), subtitle_text, font=self.font, fill="black")
        
        # 绘制正文（白色）
        draw.text((x, y), subtitle_text, font=self.font, fill="white")
        
        # 保存
        img.save(output_path)
    
    def burn_subtitles(self, video_path: str, subtitles: list, output_path: str):
        """
        烧录字幕到视频
        
        Args:
            video_path: 输入视频路径
            subtitles: 字幕列表 [{"start": 0, "end": 4, "text": "字幕文本"}, ...]
            output_path: 输出视频路径
        """
        print(f"🎬 烧录字幕: {video_path}")
        print(f"   字幕数量: {len(subtitles)}")
        
        # 获取视频信息
        info = self.get_video_info(video_path)
        print(f"   视频尺寸: {info['width']}x{info['height']}")
        print(f"   帧率: {info['fps']:.2f} fps")
        print(f"   时长: {info['duration']:.2f}s")
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix="subtitle_")
        print(f"   临时目录: {temp_dir}")
        
        try:
            # 提取视频帧
            frames_dir = os.path.join(temp_dir, "frames")
            os.makedirs(frames_dir)
            
            print("   📤 提取视频帧...")
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                os.path.join(frames_dir, "frame_%06d.png")
            ], capture_output=True)
            
            # 获取帧文件列表
            frame_files = sorted(Path(frames_dir).glob("frame_*.png"))
            print(f"   找到 {len(frame_files)} 帧")
            
            # 创建输出帧目录
            output_frames_dir = os.path.join(temp_dir, "output_frames")
            os.makedirs(output_frames_dir)
            
            # 处理每一帧
            print("   ✍️ 绘制字幕...")
            for i, frame_file in enumerate(frame_files):
                frame_time = i / info["fps"]
                
                # 查找当前帧对应的字幕
                current_subtitle = None
                for sub in subtitles:
                    if sub["start"] <= frame_time < sub["end"]:
                        current_subtitle = sub["text"]
                        break
                
                # 处理帧
                output_frame = os.path.join(output_frames_dir, f"frame_{i+1:06d}.png")
                
                if current_subtitle:
                    self.draw_subtitle_on_frame(
                        str(frame_file),
                        current_subtitle,
                        output_frame
                    )
                else:
                    # 无字幕，直接复制
                    shutil.copy(str(frame_file), output_frame)
                
                # 进度显示
                if (i + 1) % 100 == 0 or i == len(frame_files) - 1:
                    print(f"      进度: {i+1}/{len(frame_files)} 帧")
            
            # 合成视频
            print("   📥 合成视频...")
            subprocess.run([
                "ffmpeg", "-y",
                "-framerate", str(info["fps"]),
                "-i", os.path.join(output_frames_dir, "frame_%06d.png"),
                "-i", video_path, "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-preset", "medium",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                output_path
            ], capture_output=True)
            
            print(f"   ✅ 完成: {output_path}")
            
        finally:
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def burn_subtitle_to_video_simple(self, video_path: str, subtitle_text: str, output_path: str):
        """
        简化版：在视频全程显示固定字幕（使用 ffmpeg drawtext）
        
        Args:
            video_path: 输入视频路径
            subtitle_text: 字幕文本
            output_path: 输出视频路径
        """
        print(f"🎬 烧录字幕: {subtitle_text[:30]}...")
        
        # 去除标点
        import re
        subtitle_text = re.sub(
            r'[，。！？、；：""''（）【】《》,.!?;:\'\"\(\)\[\]<>]',
            '',
            subtitle_text
        )
        
        # 使用 ffmpeg drawtext（Windows 兼容）
        # 注意：需要处理中文编码
        filter_str = (
            f"drawtext=text='{subtitle_text}':"
            f"fontfile='{self.font_path}':"
            f"fontsize={self.font_size}:"
            f"fontcolor=white:"
            f"borderw=2:bordercolor=black:"
            f"x=(w-text_w)/2:y=h-50-th"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", filter_str,
            "-c:a", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ 完成: {output_path}")
            return True
        else:
            print(f"   ❌ 失败: {result.stderr[:200]}")
            return False


def main():
    """测试字幕烧录"""
    burner = SubtitleBurner()
    
    # 测试字幕列表
    subtitles = [
        {"start": 0, "end": 4, "text": "城市黄昏，飞天狗与钢铁猫屋顶对峙"},
        {"start": 4, "end": 8, "text": "钢铁猫眼中红光闪烁，激光束射出"},
        {"start": 8, "end": 13, "text": "飞天狗侧身闪避，翅膀展开反击"},
    ]
    
    print("字幕烧录工具测试")
    print("=" * 60)
    print("使用方法:")
    print("  burner = SubtitleBurner()")
    print("  burner.burn_subtitles('input.mp4', subtitles, 'output.mp4')")
    print()
    print("或简化版（全程固定字幕）:")
    print("  burner.burn_subtitle_to_video_simple('input.mp4', '字幕文本', 'output.mp4')")


if __name__ == "__main__":
    main()
