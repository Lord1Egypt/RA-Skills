#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coser Card - 模卡生成器
快速制作专业的 Cosplay/模特展示卡片
"""

import os
import sys
import json
import argparse
import glob
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from PIL import Image, ImageDraw, ImageFont

# 设置输出编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@dataclass
class CoserProfile:
    """Coser 信息"""
    name: str = ""                    # CN名称
    cn: str = ""                      # 罗马音/英文名
    height: int = 0                   # 身高 cm
    weight: int = 0                   # 体重 kg
    bust: int = 0                     # 胸围 cm
    waist: int = 0                    # 腰围 cm
    hip: int = 0                      # 臀围 cm
    shoe: int = 0                     # 鞋码
    contact: str = ""                 # 联系方式
    location: str = ""                # 所在城市
    experience: str = ""              # 经验
    # 社交账号
    douyin: str = ""                  # 抖音
    weibo: str = ""                   # 微博
    bilibili: str = ""                # B站
    xiaohongshu: str = ""             # 小红书
    photos: List[str] = None          # 照片路径列表
    
    def __post_init__(self):
        if self.photos is None:
            self.photos = []


# 风格配置
STYLE_CONFIGS = {
    "japanese": {
        "name": "日系清新",
        "bg_color": (255, 252, 245),      # 米白
        "text_color": (80, 80, 80),       # 深灰
        "accent_color": (255, 183, 178),  # 樱花粉
        "font_title": None,
        "font_body": None,
    },
    "elegant": {
        "name": "优雅简约",
        "bg_color": (250, 250, 250),      # 纯白
        "text_color": (40, 40, 40),       # 黑色
        "accent_color": (180, 160, 140),  # 香槟金
        "font_title": None,
        "font_body": None,
    },
    "cyber": {
        "name": "赛博朋克",
        "bg_color": (20, 20, 30),         # 深黑蓝
        "text_color": (0, 255, 255),      # 青色
        "accent_color": (255, 0, 128),    # 霓虹粉
        "font_title": None,
        "font_body": None,
    },
    "retro": {
        "name": "复古胶片",
        "bg_color": (245, 235, 220),      # 暖黄
        "text_color": (100, 70, 50),      # 棕色
        "accent_color": (200, 100, 80),   # 砖红
        "font_title": None,
        "font_body": None,
    },
    "minimal": {
        "name": "极简白底",
        "bg_color": (255, 255, 255),      # 纯白
        "text_color": (50, 50, 50),       # 深灰
        "accent_color": (200, 200, 200),  # 浅灰
        "font_title": None,
        "font_body": None,
    },
    "colorful": {
        "name": "多彩活泼",
        "bg_color": (255, 248, 240),      # 暖白
        "text_color": (60, 60, 60),       # 深灰
        "accent_color": (255, 150, 100),  # 橙色
        "font_title": None,
        "font_body": None,
    },
    "anime": {
        "name": "二次元风",
        "bg_color": (60, 60, 65),         # 深灰背景
        "text_color": (255, 255, 255),    # 白色文字
        "accent_color": (255, 100, 150),  # 樱花粉强调
        "font_title": None,
        "font_body": None,
    },
}


# 输出尺寸配置
FORMAT_SIZES = {
    "a4": (2480, 3508),        # 300dpi A4
    "mobile": (1080, 1920),    # 9:16 手机
    "square": (1080, 1080),    # 1:1 正方形
    "banner": (1500, 500),     # 3:1 横幅
    "wide": (2560, 1080),      # 21:9 宽屏（参考 coser_0.jpg）
    "landscape": (1920, 1080), # 16:9 横向
}


def interactive_input() -> CoserProfile:
    """交互式输入 Coser 信息 - 用户可选择性提供"""
    print("\n" + "="*50)
    print("  Coser 模卡生成器 - 交互式输入")
    print("  (直接回车跳过不想填的项)")
    print("="*50 + "\n")
    
    profile = CoserProfile()
    
    # 基本信息
    print("【基本信息】")
    profile.name = input("CN名称 (如: 赤西夜夜): ").strip()
    profile.cn = input("英文名/罗马音 (可选，回车跳过): ").strip()
    
    # 身体数据
    print("\n【身体数据】(可选，回车跳过)")
    height_input = input("身高 (cm): ").strip()
    if height_input:
        try:
            profile.height = int(height_input)
        except:
            print("  ⚠️  身高格式错误，已跳过")
    
    weight_input = input("体重 (kg): ").strip()
    if weight_input:
        try:
            profile.weight = int(weight_input)
        except:
            print("  ⚠️  体重格式错误，已跳过")
    
    print("三围 (可选)")
    bust = input("  胸围 (cm): ").strip()
    if bust:
        try:
            profile.bust = int(bust)
        except:
            pass
    waist = input("  腰围 (cm): ").strip()
    if waist:
        try:
            profile.waist = int(waist)
        except:
            pass
    hip = input("  臀围 (cm): ").strip()
    if hip:
        try:
            profile.hip = int(hip)
        except:
            pass
    
    shoe_input = input("鞋码: ").strip()
    if shoe_input:
        try:
            profile.shoe = int(shoe_input)
        except:
            pass
    
    # 社交账号
    print("\n【社交账号】(可选，回车跳过)")
    profile.douyin = input("抖音 (粉丝数或ID): ").strip()
    profile.weibo = input("微博 (ID): ").strip()
    profile.bilibili = input("B站 (ID): ").strip()
    profile.xiaohongshu = input("小红书 (ID): ").strip()
    
    # 联系方式
    print("\n【联系方式】(可选，回车跳过)")
    profile.contact = input("微信/QQ/邮箱: ").strip()
    profile.location = input("所在城市: ").strip()
    
    # 显示填写摘要
    print("\n" + "="*50)
    print("  信息填写摘要")
    print("="*50)
    filled = []
    if profile.name:
        filled.append(f"CN: {profile.name}")
    if profile.height:
        filled.append(f"身高: {profile.height}cm")
    if profile.weight:
        filled.append(f"体重: {profile.weight}kg")
    if profile.bust and profile.waist and profile.hip:
        filled.append(f"三围: {profile.bust}-{profile.waist}-{profile.hip}")
    if profile.shoe:
        filled.append(f"鞋码: {profile.shoe}")
    if profile.douyin:
        filled.append(f"抖音: {profile.douyin}")
    if profile.contact:
        filled.append(f"联系方式: {profile.contact}")
    
    if filled:
        for item in filled:
            print(f"  ✓ {item}")
    else:
        print("  (未填写任何信息，将生成纯图片模卡)")
    print("="*50)
    
    return profile


def check_text_overflow(text: str, font, max_width: int) -> bool:
    """检查文字是否会超出给定宽度"""
    try:
        # 创建一个临时图片来获取文字尺寸
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        return text_width > max_width
    except:
        # 如果无法获取精确尺寸，使用估算
        estimated_width = len(text) * font.size * 0.6
        return estimated_width > max_width


def truncate_text(text: str, font, max_width: int) -> str:
    """截断文字以适应给定宽度"""
    if not text:
        return ""
    
    try:
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # 检查是否需要截断
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return text
        
        # 二分查找最大长度
        left, right = 0, len(text)
        while left < right:
            mid = (left + right + 1) // 2
            truncated = text[:mid] + "..."
            bbox = temp_draw.textbbox((0, 0), truncated, font=font)
            if bbox[2] - bbox[0] <= max_width:
                left = mid
            else:
                right = mid - 1
        
        return text[:left] + "..." if left < len(text) else text
    except:
        # 降级处理：按字符数截断
        max_chars = int(max_width / (font.size * 0.6))
        if len(text) > max_chars:
            return text[:max_chars-3] + "..."
        return text


def get_font(size: int, font_name: str = "default"):
    """获取字体"""
    # 尝试不同平台的字体
    font_paths = [
        # Windows
        "C:/Windows/Fonts/simhei.ttf",      # 黑体
        "C:/Windows/Fonts/simsun.ttc",      # 宋体
        "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    
    # 回退到默认字体
    return ImageFont.load_default()


def load_photos(photo_paths: str) -> List[str]:
    """加载照片路径列表"""
    photos = []
    
    # 支持逗号分隔
    if "," in photo_paths:
        paths = [p.strip() for p in photo_paths.split(",")]
    else:
        paths = [photo_paths]
    
    for path in paths:
        # 支持通配符
        if "*" in path:
            matched = glob.glob(path)
            photos.extend(sorted(matched))
        elif os.path.exists(path):
            photos.append(path)
        else:
            print(f"警告: 找不到照片 {path}")
    
    return photos


def create_grid3_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建三图网格布局 (一大两小)"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.03)
    info_height = int(height * 0.15)
    photo_area_height = height - info_height - margin * 2
    
    # 大图 (上方 60%)
    big_height = int(photo_area_height * 0.6)
    if len(photos) >= 1:
        big_img = photos[0].copy()
        big_img.thumbnail((width - margin * 2, big_height), Image.Resampling.LANCZOS)
        x = (width - big_img.width) // 2
        canvas.paste(big_img, (x, margin))
    
    # 小图 (下方 40%，并排)
    small_y = margin + big_height + margin
    small_height = photo_area_height - big_height - margin
    small_width = (width - margin * 3) // 2
    
    for i, photo in enumerate(photos[1:3], 1):
        img = photo.copy()
        img.thumbnail((small_width, small_height), Image.Resampling.LANCZOS)
        x = margin + (i - 1) * (small_width + margin)
        y = small_y + (small_height - img.height) // 2
        canvas.paste(img, (x, y))
    
    return canvas


def create_grid4_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建四图网格布局 (2x2)"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.03)
    info_height = int(height * 0.12)
    
    # 计算图片区域
    grid_width = (width - margin * 3) // 2
    grid_height = (height - info_height - margin * 4) // 2
    
    for i, photo in enumerate(photos[:4]):
        row = i // 2
        col = i % 2
        
        x = margin + col * (grid_width + margin)
        y = margin + row * (grid_height + margin)
        
        img = photo.copy()
        img.thumbnail((grid_width, grid_height), Image.Resampling.LANCZOS)
        
        # 居中
        paste_x = x + (grid_width - img.width) // 2
        paste_y = y + (grid_height - img.height) // 2
        canvas.paste(img, (paste_x, paste_y))
    
    return canvas


def create_vertical_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建竖排布局"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.03)
    info_height = int(height * 0.12)
    photo_count = min(len(photos), 5)
    
    if photo_count == 0:
        return canvas
    
    photo_height = (height - info_height - margin * (photo_count + 1)) // photo_count
    
    for i, photo in enumerate(photos[:photo_count]):
        img = photo.copy()
        img.thumbnail((width - margin * 2, photo_height), Image.Resampling.LANCZOS)
        
        x = (width - img.width) // 2
        y = margin + i * (photo_height + margin)
        canvas.paste(img, (x, y))
    
    return canvas


def create_horizontal_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建横排布局"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.03)
    info_height = int(height * 0.15)
    photo_count = min(len(photos), 5)
    
    if photo_count == 0:
        return canvas
    
    photo_width = (width - margin * (photo_count + 1)) // photo_count
    photo_height = height - info_height - margin * 2
    
    for i, photo in enumerate(photos[:photo_count]):
        img = photo.copy()
        img.thumbnail((photo_width, photo_height), Image.Resampling.LANCZOS)
        
        x = margin + i * (photo_width + margin) + (photo_width - img.width) // 2
        y = margin + (photo_height - img.height) // 2
        canvas.paste(img, (x, y))
    
    return canvas


def create_grid6_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建六图网格布局 (3x2)"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.025)
    info_height = int(height * 0.12)
    
    # 计算网格尺寸
    grid_width = (width - margin * 4) // 3
    grid_height = (height - info_height - margin * 4) // 2
    
    for i, photo in enumerate(photos[:6]):
        row = i // 3
        col = i % 3
        
        x = margin + col * (grid_width + margin)
        y = margin + row * (grid_height + margin)
        
        img = photo.copy()
        img.thumbnail((grid_width, grid_height), Image.Resampling.LANCZOS)
        
        # 居中
        paste_x = x + (grid_width - img.width) // 2
        paste_y = y + (grid_height - img.height) // 2
        canvas.paste(img, (paste_x, paste_y))
    
    return canvas


def create_hero_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建主图+缩略图布局"""
    canvas = Image.new('RGB', (width, height), (255, 255, 255))
    
    margin = int(width * 0.03)
    info_height = int(height * 0.12)
    
    # 主图区域 (上方 70%)
    hero_height = int((height - info_height - margin * 3) * 0.7)
    
    if len(photos) >= 1:
        hero_img = photos[0].copy()
        hero_img.thumbnail((width - margin * 2, hero_height), Image.Resampling.LANCZOS)
        x = (width - hero_img.width) // 2
        canvas.paste(hero_img, (x, margin))
    
    # 缩略图区域 (下方 30%)
    thumb_y = margin + hero_height + margin
    thumb_height = height - info_height - thumb_y - margin
    thumb_count = min(len(photos) - 1, 5)
    
    if thumb_count > 0:
        thumb_width = (width - margin * (thumb_count + 1)) // thumb_count
        
        for i, photo in enumerate(photos[1:thumb_count+1], 1):
            img = photo.copy()
            img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            
            x = margin + (i - 1) * (thumb_width + margin) + (thumb_width - img.width) // 2
            y = thumb_y + (thumb_height - img.height) // 2
            canvas.paste(img, (x, y))
    
    return canvas


def create_film_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建电影胶片风格布局"""
    canvas = Image.new('RGB', (width, height), (30, 30, 30))
    
    margin = int(width * 0.04)
    info_height = int(height * 0.12)
    film_border = int(height * 0.04)
    
    # 胶片上下黑边
    film_top = margin + film_border
    film_height = height - info_height - margin * 2 - film_border * 2
    
    # 绘制胶片孔
    hole_size = int(film_border * 0.5)
    hole_spacing = int(width * 0.08)
    draw = ImageDraw.Draw(canvas)
    
    for x in range(margin + hole_spacing // 2, width - margin, hole_spacing):
        # 上排孔
        draw.rectangle([x, margin + film_border // 4, 
                       x + hole_size, margin + film_border // 4 + hole_size], 
                      fill=(200, 200, 200))
        # 下排孔
        draw.rectangle([x, height - info_height - margin - film_border // 4 - hole_size,
                       x + hole_size, height - info_height - margin - film_border // 4], 
                      fill=(200, 200, 200))
    
    # 照片数量
    photo_count = min(len(photos), 4)
    if photo_count > 0:
        photo_width = (width - margin * 2 - margin * (photo_count - 1)) // photo_count
        
        for i, photo in enumerate(photos[:photo_count]):
            img = photo.copy()
            img.thumbnail((photo_width, film_height), Image.Resampling.LANCZOS)
            
            x = margin + i * (photo_width + margin) + (photo_width - img.width) // 2
            y = film_top + (film_height - img.height) // 2
            canvas.paste(img, (x, y))
    
    return canvas


def create_sidebar_layout(photos: List[Image.Image], width: int, height: int, sidebar_left: bool = True) -> Image.Image:
    """创建侧边栏布局 - 参考 coser_8, coser_9 风格
    
    Args:
        photos: 照片列表
        width: 画布宽度
        height: 画布高度
        sidebar_left: True=信息栏在左侧, False=信息栏在右侧
    """
    # 使用深色背景
    canvas = Image.new('RGB', (width, height), (25, 25, 30))
    
    # 布局参数
    gap = max(3, int(width * 0.008))
    sidebar_width = int(width * 0.22)  # 侧边栏占 22%
    photo_area_width = width - sidebar_width - gap * 3
    photo_area_height = height - gap * 2
    
    # 确定侧边栏位置
    if sidebar_left:
        sidebar_x = gap
        photos_start_x = sidebar_x + sidebar_width + gap
    else:
        photos_start_x = gap
        sidebar_x = width - sidebar_width - gap
    
    # 绘制侧边栏背景
    draw = ImageDraw.Draw(canvas)
    sidebar_bg = (35, 35, 40)
    draw.rectangle([sidebar_x, gap, sidebar_x + sidebar_width, height - gap], fill=sidebar_bg)
    
    # 右侧图片网格布局
    if len(photos) >= 1:
        count = min(len(photos), 8)  # 最多8张图
        
        # 计算网格：根据数量决定行列
        if count <= 2:
            cols, rows = 2, 1
        elif count <= 4:
            cols, rows = 2, 2
        elif count <= 6:
            cols, rows = 3, 2
        else:
            cols, rows = 4, 2
        
        # 计算每个格子的尺寸
        total_gap_x = gap * (cols - 1)
        total_gap_y = gap * (rows - 1)
        cell_width = (photo_area_width - total_gap_x) // cols
        cell_height = (photo_area_height - total_gap_y) // rows
        
        for i, photo in enumerate(photos[:count]):
            row = i // cols
            col = i % cols
            
            x = photos_start_x + col * (cell_width + gap)
            y = gap + row * (cell_height + gap)
            
            # 使用智能裁剪，保留完整图片
            img = smart_crop(photo, cell_width, cell_height, face_priority=False)
            
            canvas.paste(img, (x, y))
    
    return canvas


def create_floating_info_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建浮动信息布局 - 信息悬浮在图片底部，半透明不遮挡
    
    特点：
    - 图片占满全屏
    - 信息栏悬浮在底部，半透明黑色背景
    - 文字与图片错开，不会遮挡人脸
    - 适合展示全身照或场景照
    """
    # 计算布局
    gap = max(4, int(width * 0.01))
    info_height = int(height * 0.20)  # 信息栏占 20%
    photo_area_height = height - info_height - gap
    
    # 创建画布（深色背景）
    canvas = Image.new('RGB', (width, height), (20, 20, 25))
    
    # 计算网格
    count = min(len(photos), 6)
    if count <= 2:
        cols, rows = 2, 1
    elif count <= 4:
        cols, rows = 2, 2
    else:
        cols, rows = 3, 2
    
    # 计算图片格子尺寸
    total_gap_x = gap * (cols + 1)
    total_gap_y = gap * (rows + 1)
    cell_width = (width - total_gap_x) // cols
    cell_height = (photo_area_height - total_gap_y) // rows
    
    # 绘制图片网格（偏上，给信息栏留空间）
    for i, photo in enumerate(photos[:count]):
        row = i // cols
        col = i % cols
        
        x = gap + col * (cell_width + gap)
        y = gap + row * (cell_height + gap)
        
        # 使用智能裁剪，保留完整图片
        img = smart_crop(photo, cell_width, cell_height, face_priority=False)
        canvas.paste(img, (x, y))
    
    # 绘制底部浮动信息栏背景（半透明）
    draw = ImageDraw.Draw(canvas)
    info_y = height - info_height
    
    # 半透明黑色背景
    overlay = Image.new('RGBA', (width, info_height), (0, 0, 0, 180))
    canvas_rgba = canvas.convert('RGBA')
    canvas_rgba.paste(overlay, (0, info_y), overlay)
    canvas = canvas_rgba.convert('RGB')
    draw = ImageDraw.Draw(canvas)
    
    return canvas


def smart_crop(img: Image.Image, target_width: int, target_height: int, 
               face_priority: bool = True) -> Image.Image:
    """智能裁剪图片，优先保留上半部分（人脸通常在上方）
    
    Args:
        img: 原始图片
        target_width: 目标宽度
        target_height: 目标高度
        face_priority: 是否优先保留上半部分
    """
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        # 图片更宽，需要裁剪左右
        new_height = target_height
        new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 从中心裁剪
        crop_left = (new_width - target_width) // 2
        crop_top = 0 if face_priority else (new_height - target_height) // 2
        img = img.crop((crop_left, crop_top,
                       crop_left + target_width,
                       crop_top + target_height))
    else:
        # 图片更高，需要裁剪上下
        new_width = target_width
        new_height = int(new_width / img_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if face_priority:
            # 优先保留上半部分（人脸通常在上方 1/3 处）
            crop_top = 0
        else:
            # 从中心裁剪
            crop_top = (new_height - target_height) // 2
        
        img = img.crop((0, crop_top,
                       target_width,
                       crop_top + target_height))
    
    return img


def create_wide_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建宽屏横向布局 - 参考 coser_0.jpg 风格 (2560x1080)
    
    特点：
    - 左侧竖排信息栏（占宽度 15%）
    - 右侧图片横向排列（2行 x 3-4列）
    - 适合 21:9 宽屏显示
    """
    # 深色背景
    canvas = Image.new('RGB', (width, height), (25, 25, 30))
    
    gap = max(3, int(width * 0.008))
    sidebar_width = int(width * 0.15)  # 侧边栏占 15%
    photo_area_width = width - sidebar_width - gap * 3
    photo_area_height = height - gap * 2
    
    sidebar_x = gap
    photos_start_x = sidebar_x + sidebar_width + gap
    
    # 绘制侧边栏背景
    draw = ImageDraw.Draw(canvas)
    sidebar_bg = (35, 35, 40)
    draw.rectangle([sidebar_x, gap, sidebar_x + sidebar_width, height - gap], fill=sidebar_bg)
    
    # 右侧图片网格 - 横向优先排列
    if len(photos) >= 1:
        count = min(len(photos), 8)
        
        # 宽屏布局：横向排列优先
        if count <= 3:
            cols, rows = count, 1
        elif count <= 6:
            cols, rows = 3, 2
        else:
            cols, rows = 4, 2
        
        total_gap_x = gap * (cols - 1)
        total_gap_y = gap * (rows - 1)
        cell_width = (photo_area_width - total_gap_x) // cols
        cell_height = (photo_area_height - total_gap_y) // rows
        
        for i, photo in enumerate(photos[:count]):
            row = i // cols
            col = i % cols
            
            x = photos_start_x + col * (cell_width + gap)
            y = gap + row * (cell_height + gap)
            
            # 使用智能裁剪，保留完整图片
            img = smart_crop(photo, cell_width, cell_height, face_priority=False)
            canvas.paste(img, (x, y))
    
    return canvas


def create_compact_anime_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """创建二次元紧凑布局 - 参考专业模特卡风格"""
    canvas = Image.new('RGB', (width, height), (50, 50, 55))
    
    # 极小边距，紧凑布局
    gap = max(2, int(width * 0.005))  # 2-5px 间隙
    info_height = int(height * 0.09)  # 信息区域只占 9%
    photo_area_height = height - info_height - gap
    
    # 布局：左大右小
    left_ratio = 0.42  # 左侧占 42%
    left_width = int((width - gap * 3) * left_ratio)
    right_width = width - left_width - gap * 3
    
    # 计算可用高度（确保左右对齐）
    available_height = photo_area_height - gap * 2
    
    if len(photos) >= 1:
        # 左侧大图 - 严格控制在左半边
        left_img = photos[0].copy()
        # 按比例缩放，填满左侧区域
        left_target_height = available_height
        left_target_width = left_width
        
        # 计算缩放比例，保持比例填充
        img_ratio = left_img.width / left_img.height
        target_ratio = left_target_width / left_target_height
        
        if img_ratio > target_ratio:
            # 图片更宽，按高度缩放
            new_height = left_target_height
            new_width = int(new_height * img_ratio)
        else:
            # 图片更高，按宽度缩放
            new_width = left_target_width
            new_height = int(new_width / img_ratio)
        
        left_img = left_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 居中裁剪
        crop_left = (new_width - left_target_width) // 2
        crop_top = (new_height - left_target_height) // 2
        left_img = left_img.crop((crop_left, crop_top, 
                                   crop_left + left_target_width, 
                                   crop_top + left_target_height))
        
        canvas.paste(left_img, (gap, gap))
    
    # 右侧网格布局 - 严格控制在右半边
    if len(photos) >= 2:
        right_photos = photos[1:]
        right_x = left_width + gap * 2
        
        # 根据剩余图片数量决定网格布局
        count = min(len(right_photos), 6)  # 最多6张
        
        # 计算网格：尽量让图片填满右侧区域
        if count <= 2:
            cols, rows = 1, 2
        elif count <= 4:
            cols, rows = 2, 2
        else:
            cols, rows = 2, 3  # 5-6张用 2x3
        
        # 计算每个格子的尺寸（严格填满，不留多余空白）
        total_gap_x = gap * (cols - 1)
        total_gap_y = gap * (rows - 1)
        cell_width = (right_width - total_gap_x) // cols
        cell_height = (available_height - total_gap_y) // rows
        
        for i, photo in enumerate(right_photos[:count]):
            row = i // cols
            col = i % cols
            
            x = right_x + col * (cell_width + gap)
            y = gap + row * (cell_height + gap)
            
            # 缩放图片填满格子
            img = photo.copy()
            img_ratio = img.width / img.height
            cell_ratio = cell_width / cell_height
            
            if img_ratio > cell_ratio:
                new_height = cell_height
                new_width = int(new_height * img_ratio)
            else:
                new_width = cell_width
                new_height = int(new_width / img_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 居中裁剪填满
            crop_left = (new_width - cell_width) // 2
            crop_top = (new_height - cell_height) // 2
            img = img.crop((crop_left, crop_top,
                           crop_left + cell_width,
                           crop_top + cell_height))
            
            canvas.paste(img, (x, y))
    
    return canvas


def add_compact_info_section(draw, canvas, profile: CoserProfile, config, width: int, height: int):
    """添加紧凑信息区域 - 类似参考图片的专业模特卡风格"""
    # 信息区域在底部，只占 10% 高度
    info_height = int(height * 0.10)
    info_y = height - info_height
    
    # 使用深灰背景
    bg_color = config.get("bg_color", (60, 60, 65))
    text_color = config.get("text_color", (255, 255, 255))
    accent_color = config.get("accent_color", (255, 100, 150))
    
    # 绘制背景
    draw.rectangle([0, info_y, width, height], fill=bg_color)
    
    # 字体大小 - 紧凑布局
    font_name = get_font(int(height * 0.045))  # 名字大一些
    font_data = get_font(int(height * 0.028))  # 数据小一些
    font_label = get_font(int(height * 0.020))  # 标签更小
    
    margin = int(width * 0.03)
    gap = int(width * 0.025)
    
    # 垂直居中
    center_y = info_y + info_height // 2
    
    # 左侧：姓名（加粗竖线装饰）
    # 绘制竖线装饰
    line_x = margin
    line_top = center_y - int(height * 0.035)
    line_bottom = center_y + int(height * 0.035)
    draw.rectangle([line_x, line_top, line_x + 4, line_bottom], fill=accent_color)
    
    # 绘制姓名
    name_x = line_x + 15
    name_y = center_y - int(height * 0.025)
    draw.text((name_x, name_y), profile.name or "CN", font=font_name, fill=text_color)
    
    # 如果有CN，放在名字下方小字显示
    if profile.cn:
        cn_y = name_y + int(height * 0.038)
        draw.text((name_x, cn_y), profile.cn, font=font_label, fill=(180, 180, 180))
    
    # 右侧：数据项横向排列
    # 计算起始位置 - 从右往左排列
    data_items = []
    
    if profile.shoe:
        data_items.append(("鞋码", f"{profile.shoe}"))
    if profile.hip:
        data_items.append(("臀围", f"{profile.hip}"))
    if profile.waist:
        data_items.append(("腰围", f"{profile.waist}"))
    if profile.bust:
        data_items.append(("胸围", f"{profile.bust}"))
    if profile.weight:
        data_items.append(("体重", f"{profile.weight}"))
    if profile.height:
        data_items.append(("身高", f"{profile.height}cm"))
    
    # 从右往左绘制
    current_x = width - margin
    
    for label, value in data_items:
        # 计算文本宽度
        try:
            value_bbox = draw.textbbox((0, 0), value, font=font_data)
            value_width = value_bbox[2] - value_bbox[0]
            label_bbox = draw.textbbox((0, 0), label, font=font_label)
            label_width = label_bbox[2] - label_bbox[0]
        except:
            value_width = len(value) * int(height * 0.028) * 0.6
            label_width = len(label) * int(height * 0.020) * 0.6
        
        item_width = max(value_width, label_width)
        
        # 绘制数值（大）
        value_x = current_x - value_width
        value_y = center_y - int(height * 0.02)
        draw.text((value_x, value_y), value, font=font_data, fill=text_color)
        
        # 绘制标签（小，在数值上方）
        label_x = current_x - label_width
        label_y = center_y - int(height * 0.045)
        draw.text((label_x, label_y), label, font=font_label, fill=(150, 150, 150))
        
        # 更新位置，留间隙
        current_x -= max(item_width + gap, int(width * 0.08))


def add_sidebar_info_section(draw, canvas, profile: CoserProfile, config, width: int, height: int, template: str):
    """添加侧边栏信息区域 - 参考 coser_8, coser_9 风格"""
    # 侧边栏参数 - wide 模板使用更窄的侧边栏
    gap = max(3, int(width * 0.008))
    
    if template == "wide":
        sidebar_width = int(width * 0.15)
        sidebar_x = gap  # wide 模板侧边栏在左侧
    elif template == "sidebar":
        sidebar_width = int(width * 0.22)
        sidebar_x = gap  # sidebar 模板侧边栏在左侧
    elif template == "sidebar_right":
        sidebar_width = int(width * 0.22)
        sidebar_x = width - sidebar_width - gap  # sidebar_right 模板侧边栏在右侧
    else:
        sidebar_width = int(width * 0.22)
        sidebar_x = gap
    
    # 文字颜色
    text_color = (255, 255, 255)
    accent_color = (255, 100, 150)  # 樱花粉强调色
    label_color = (150, 150, 150)   # 标签灰色
    
    # 字体大小
    font_title = get_font(int(height * 0.038))
    font_name = get_font(int(height * 0.055))
    font_data = get_font(int(height * 0.032))
    font_label = get_font(int(height * 0.022))
    font_small = get_font(int(height * 0.020))
    
    # 起始位置
    margin_x = sidebar_x + int(sidebar_width * 0.12)
    current_y = gap + int(height * 0.05)
    line_spacing = int(height * 0.055)
    
    # 绘制装饰竖线
    line_x = sidebar_x + int(sidebar_width * 0.06)
    line_top = current_y
    line_bottom = line_top + int(height * 0.08)
    draw.rectangle([line_x, line_top, line_x + 3, line_bottom], fill=accent_color)
    
    # 绘制标题标签 "NAME/CN"
    draw.text((margin_x, current_y), "NAME", font=font_label, fill=label_color)
    current_y += int(height * 0.025)
    
    # 绘制姓名（大号）
    name_text = profile.name or "CN"
    draw.text((margin_x, current_y), name_text, font=font_name, fill=text_color)
    current_y += line_spacing
    
    # 如果有 CN/英文名
    if profile.cn:
        draw.text((margin_x, current_y), profile.cn, font=font_small, fill=label_color)
        current_y += int(height * 0.04)
    
    current_y += int(height * 0.03)  # 额外间距
    
    # 绘制数据项 - 竖向排列（标签在上，数值在下）
    data_items = [
        ("身高", f"{profile.height}cm" if profile.height else ""),
        ("体重", f"{profile.weight}" if profile.weight else ""),
        ("胸围", f"{profile.bust}" if profile.bust else ""),
        ("腰围", f"{profile.waist}" if profile.waist else ""),
        ("臀围", f"{profile.hip}" if profile.hip else ""),
        ("鞋码", f"{profile.shoe}" if profile.shoe else ""),
    ]
    
    # 添加地点
    if profile.location:
        data_items.append(("地点", profile.location))
    
    # 添加社交账号（优先显示抖音）
    if profile.douyin:
        data_items.append(("抖音", profile.douyin))
    elif profile.weibo:
        data_items.append(("微博", profile.weibo))
    elif profile.bilibili:
        data_items.append(("B站", profile.bilibili))
    
    for label, value in data_items:
        if value:  # 只显示有数据的项
            # 标签（小字，灰色）
            draw.text((margin_x, current_y), f"{label}", font=font_label, fill=label_color)
            current_y += int(height * 0.028)
            
            # 数值（中字，白色）- 自适应字体，不截断
            max_text_width = sidebar_width - int(sidebar_width * 0.15)
            display_font = font_data
            try:
                bbox = draw.textbbox((0, 0), value, font=font_data)
                text_width = bbox[2] - bbox[0]
                # 如果文字太长，缩小字体而不是截断
                if text_width > max_text_width:
                    new_size = int(font_data.size * max_text_width / text_width * 0.95)
                    if new_size < 10:
                        new_size = 10
                    display_font = get_font(new_size)
            except:
                pass
            
            draw.text((margin_x, current_y), value, font=display_font, fill=text_color)
            current_y += int(height * 0.045)
    
    # 底部：联系方式
    if profile.contact:
        current_y += int(height * 0.03)
        draw.text((margin_x, current_y), "联系", font=font_label, fill=label_color)
        current_y += int(height * 0.028)
        
        # 截断过长的联系信息
        contact = profile.contact
        if len(contact) > 12:
            contact = contact[:11] + "..."
        draw.text((margin_x, current_y), contact, font=font_small, fill=text_color)


def add_info_section(canvas: Image.Image, profile: CoserProfile, style: str, template: str):
    """添加信息区域"""
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    
    # 获取风格配置
    config = STYLE_CONFIGS.get(style, STYLE_CONFIGS["minimal"])
    
    # sidebar 布局使用特殊信息展示
    if template in ["sidebar", "sidebar_right", "wide"]:
        add_sidebar_info_section(draw, canvas, profile, config, width, height, template)
        return
    
    # floating 布局使用底部悬浮信息栏
    if template == "floating":
        add_floating_info_section(draw, canvas, profile, config, width, height)
        return
    
    # 紧凑模板使用特殊布局
    if template == "compact":
        add_compact_info_section(draw, canvas, profile, config, width, height)
        return
    
    # 信息区域位置 - 根据模板调整
    margin = int(width * 0.05)
    if template in ["grid3", "vertical"]:
        info_y = height - int(height * 0.18)
        info_height = int(height * 0.18)
    elif template == "film":
        info_y = height - int(height * 0.15)
        info_height = int(height * 0.15)
    else:
        info_y = height - int(height * 0.15)
        info_height = int(height * 0.15)
    
    # 绘制背景条
    draw.rectangle([0, info_y, width, height], fill=config["bg_color"])
    
    # 绘制装饰线
    line_y = info_y + int(height * 0.015)
    line_thickness = max(2, int(height * 0.005))
    draw.line([(margin, line_y), (width - margin, line_y)], 
              fill=config["accent_color"], width=line_thickness)
    
    # 加载字体 - 根据画布大小调整
    base_font_size = max(16, int(height * 0.035))
    font_large = get_font(base_font_size)
    font_medium = get_font(max(12, int(height * 0.022)))
    font_small = get_font(max(10, int(height * 0.018)))
    
    text_color = config["text_color"]
    accent_color = config["accent_color"]
    
    # 布局参数
    content_y = info_y + int(height * 0.04)
    line_spacing = int(height * 0.038)
    
    # 左侧：名称和基本信息
    # 绘制名称
    name_text = profile.name or "CN"
    if profile.cn:
        name_text += f" / {profile.cn}"
    draw.text((margin, content_y), name_text, font=font_large, fill=text_color)
    
    # 第二行：身体数据
    stats = []
    if profile.height:
        stats.append(f"身高 {profile.height}cm")
    if profile.weight:
        stats.append(f"体重 {profile.weight}kg")
    if profile.shoe:
        stats.append(f"鞋码 {profile.shoe}")
    
    if stats:
        stats_text = "  |  ".join(stats)
        draw.text((margin, content_y + line_spacing), 
                 stats_text, font=font_medium, fill=text_color)
    
    # 第三行：三围（如果有）
    if profile.bust and profile.waist and profile.hip:
        size_text = f"三围 {profile.bust}-{profile.waist}-{profile.hip}"
        draw.text((margin, content_y + line_spacing * 2), 
                 size_text, font=font_small, fill=text_color)
    
    # 右侧：联系方式和地点
    right_x = width - margin
    right_y = content_y
    
    # 地点（最显眼）
    if profile.location:
        loc_text = f"@{profile.location}"
        try:
            bbox = draw.textbbox((0, 0), loc_text, font=font_medium)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(loc_text) * base_font_size * 0.6
        draw.text((right_x - text_width, right_y), 
                 loc_text, font=font_medium, fill=accent_color)
        right_y += line_spacing
    
    # 联系方式
    if profile.contact:
        contact_text = profile.contact
        if len(contact_text) > 25:
            contact_text = contact_text[:22] + "..."
        try:
            bbox = draw.textbbox((0, 0), contact_text, font=font_small)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(contact_text) * base_font_size * 0.4
        
        # 确保不超出左边界
        if right_x - text_width > width * 0.4:
            draw.text((right_x - text_width, right_y), 
                     contact_text, font=font_small, fill=text_color)
        else:
            # 如果太长，放到新的一行
            draw.text((margin, content_y + line_spacing * 3), 
                     contact_text, font=font_small, fill=text_color)


def get_adaptive_font(size: int, text: str, max_width: int, draw) -> ImageFont.FreeTypeFont:
    """获取适应给定宽度的字体，如果太大则自动缩小"""
    font = get_font(size)
    
    # 检查文字宽度
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    except:
        text_width = len(text) * size * 0.6
    
    # 如果文字太宽，逐步缩小字体
    while text_width > max_width and size > 10:
        size -= 2
        font = get_font(size)
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = len(text) * size * 0.6
    
    return font


def add_floating_info_section(draw, canvas, profile: CoserProfile, config, width: int, height: int):
    """添加浮动信息区域 - 底部半透明悬浮栏
    
    特点：
    - 文字与图片错开（悬浮在底部）
    - 自动检测文字长度并截断
    - 自动调整字体大小防止遮挡
    - 多列布局显示更多信息
    """
    # 信息区域参数
    info_height = int(height * 0.22)  # 增加高度到 22%
    info_y = height - info_height
    margin = int(width * 0.04)
    
    # 创建临时draw对象用于计算字体大小
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 布局：三列
    col_width = (width - margin * 4) // 3
    
    # 计算左列内容确定字体大小
    left_content = []
    if profile.name:
        left_content.append(profile.name)
    if profile.cn:
        left_content.append(profile.cn)
    if profile.contact:
        left_content.append(profile.contact)
    
    # 自适应字体大小
    base_name_size = int(height * 0.040)
    base_data_size = int(height * 0.025)
    base_label_size = int(height * 0.018)
    base_social_size = int(height * 0.022)
    
    # 根据内容调整字体
    if left_content:
        font_name = get_adaptive_font(base_name_size, left_content[0], col_width, temp_draw)
    else:
        font_name = get_font(base_name_size)
    
    font_data = get_font(base_data_size)
    font_label = get_font(base_label_size)
    font_social = get_font(base_social_size)
    
    text_color = (255, 255, 255)
    accent_color = (255, 100, 150)
    label_color = (180, 180, 180)
    
    # 左列
    left_x = margin
    current_y = info_y + int(info_height * 0.12)
    
    # 姓名
    if profile.name:
        name_text = truncate_text(profile.name, font_name, col_width)
        draw.text((left_x, current_y), name_text, font=font_name, fill=text_color)
        current_y += int(info_height * 0.22)
    
    # CN
    if profile.cn:
        cn_font = get_adaptive_font(base_data_size, profile.cn, col_width, temp_draw)
        cn_text = truncate_text(profile.cn, cn_font, col_width)
        draw.text((left_x, current_y), cn_text, font=cn_font, fill=label_color)
        current_y += int(info_height * 0.18)
    
    # 联系方式
    if profile.contact:
        contact_font = get_adaptive_font(base_label_size, profile.contact, col_width, temp_draw)
        contact = truncate_text(profile.contact, contact_font, col_width)
        draw.text((left_x, current_y), contact, font=contact_font, fill=label_color)
    
    # 中列：身体数据
    mid_x = margin + col_width + margin
    current_y = info_y + int(info_height * 0.10)
    
    data_items = []
    if profile.height:
        data_items.append(("身高", f"{profile.height}cm"))
    if profile.weight:
        data_items.append(("体重", f"{profile.weight}"))
    if profile.bust and profile.waist and profile.hip:
        data_items.append(("三围", f"{profile.bust}-{profile.waist}-{profile.hip}"))
    if profile.shoe:
        data_items.append(("鞋码", f"{profile.shoe}"))
    
    # 如果数据项太多，调整间距
    item_spacing = int(info_height * 0.18) if len(data_items) <= 4 else int(info_height * 0.14)
    
    for label, value in data_items:
        # 标签
        draw.text((mid_x, current_y), label, font=font_label, fill=label_color)
        current_y += int(info_height * 0.10)
        # 数值
        value_font = get_adaptive_font(base_data_size, value, col_width, temp_draw)
        value_text = truncate_text(value, value_font, col_width)
        draw.text((mid_x, current_y), value_text, font=value_font, fill=text_color)
        current_y += item_spacing
    
    # 右列：社交账号
    right_x = margin + (col_width + margin) * 2
    current_y = info_y + int(info_height * 0.10)
    
    social_items = []
    if profile.douyin:
        social_items.append(("抖音", profile.douyin))
    if profile.weibo:
        social_items.append(("微博", profile.weibo))
    if profile.bilibili:
        social_items.append(("B站", profile.bilibili))
    if profile.xiaohongshu:
        social_items.append(("小红书", profile.xiaohongshu))
    
    if social_items:
        draw.text((right_x, current_y), "社交账号", font=font_label, fill=label_color)
        current_y += int(info_height * 0.13)
        
        # 调整社交账号间距
        social_spacing = int(info_height * 0.18) if len(social_items) <= 3 else int(info_height * 0.14)
        
        for platform, value in social_items:
            # 平台名
            text = f"{platform}: "
            draw.text((right_x, current_y), text, font=font_label, fill=label_color)
            # 值
            value_x = right_x + int(col_width * 0.22)
            value_width = col_width - int(col_width * 0.22)
            
            # 自适应字体
            value_font = get_adaptive_font(base_social_size, value, value_width, temp_draw)
            value_text = truncate_text(value, value_font, value_width)
            draw.text((value_x, current_y), value_text, font=value_font, fill=accent_color)
            current_y += social_spacing
    elif profile.location:
        # 如果没有社交账号，显示地点
        draw.text((right_x, current_y), f"@{profile.location}", font=font_social, fill=accent_color)


def add_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    """为图片添加圆角"""
    # 创建圆角遮罩
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
    
    # 应用遮罩
    output = img.copy()
    if output.mode != 'RGBA':
        output = output.convert('RGBA')
    output.putalpha(mask)
    return output


def apply_style_effects(img: Image.Image, style: str) -> Image.Image:
    """应用风格滤镜效果"""
    if style == "retro":
        # 复古暖色调
        r, g, b = img.split()
        r = r.point(lambda i: min(255, int(i * 1.1)))
        b = b.point(lambda i: int(i * 0.9))
        img = Image.merge('RGB', (r, g, b))
    elif style == "cyber":
        # 赛博朋克 - 增强对比度
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
    elif style == "japanese":
        # 日系 - 柔和
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
    
    return img


# ═══════════════════════════════════════════════════════════════
#  智能分析模块
# ═══════════════════════════════════════════════════════════════

def classify_photo(img: Image.Image) -> str:
    """判断照片方向类型"""
    ratio = img.width / img.height
    if ratio > 1.25:
        return "landscape"   # 横图
    elif ratio < 0.82:
        return "portrait"    # 竖图
    else:
        return "square"      # 方图


def analyze_photos(photos: List[Image.Image]) -> dict:
    """分析一批照片的构成，返回统计信息"""
    types = [classify_photo(p) for p in photos]
    portrait_count  = types.count("portrait")
    landscape_count = types.count("landscape")
    square_count    = types.count("square")
    dominant = max(["portrait", "landscape", "square"],
                   key=lambda t: types.count(t))
    return {
        "total": len(photos),
        "portrait": portrait_count,
        "landscape": landscape_count,
        "square": square_count,
        "dominant": dominant,
        "mixed": len({t for t in types}) > 1,
    }


def extract_dominant_colors(img: Image.Image, n: int = 5) -> List[Tuple[int,int,int]]:
    """用PIL提取图片主色调（无需sklearn）
    
    思路：缩小图片 → 量化调色板 → 取前N个颜色
    """
    # 缩小加速
    small = img.resize((80, 80), Image.Resampling.LANCZOS)
    # 转为调色板模式，强制量化为 n 种颜色
    quantized = small.quantize(colors=n, method=Image.Quantize.FASTOCTREE)
    palette_data = quantized.getpalette()  # 扁平 RGB 列表
    colors = []
    for i in range(n):
        r = palette_data[i * 3]
        g = palette_data[i * 3 + 1]
        b = palette_data[i * 3 + 2]
        colors.append((r, g, b))
    return colors


def color_temperature(r: int, g: int, b: int) -> str:
    """判断颜色冷暖"""
    warm_score = r * 1.2 + g * 0.5 - b * 0.8
    if warm_score > 160:
        return "warm"
    elif warm_score < 80:
        return "cool"
    else:
        return "neutral"


def color_brightness(r: int, g: int, b: int) -> float:
    """感知亮度 0-1"""
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def auto_style_from_photos(photos: List[Image.Image]) -> str:
    """根据照片主色调自动推荐最匹配的风格
    
    Returns:
        style name 字符串
    """
    if not photos:
        return "anime"

    # 分析前2张的主色（避免太慢）
    sample = photos[:2]
    all_colors: List[Tuple[int,int,int]] = []
    for p in sample:
        all_colors.extend(extract_dominant_colors(p, n=4))

    # 统计冷暖
    temps = [color_temperature(*c) for c in all_colors]
    warm_ratio = temps.count("warm") / len(temps)
    cool_ratio = temps.count("cool") / len(temps)

    # 平均亮度
    avg_brightness = sum(color_brightness(*c) for c in all_colors) / len(all_colors)

    # 饱和度（最大通道 - 最小通道的平均）
    avg_saturation = sum(
        (max(c) - min(c)) / 255 for c in all_colors
    ) / len(all_colors)

    # 决策树
    if avg_brightness < 0.28:
        # 整体暗色调
        if cool_ratio > 0.5:
            return "cyber"      # 暗+冷 → 赛博
        else:
            return "anime"      # 暗+暖/中 → 二次元
    elif avg_saturation < 0.15:
        # 低饱和（灰调）
        if avg_brightness > 0.65:
            return "minimal"    # 亮灰 → 极简
        else:
            return "elegant"    # 暗灰 → 优雅
    elif warm_ratio > 0.55:
        # 暖色为主
        if avg_saturation > 0.35:
            return "retro"      # 高饱和暖色 → 复古
        else:
            return "japanese"   # 低饱和暖色 → 日系
    elif cool_ratio > 0.55:
        return "cyber"          # 冷色为主 → 赛博
    else:
        return "colorful"       # 混合 → 多彩


def smart_select_template(photo_count: int, photo_analysis: dict = None,
                           has_social: bool = False) -> str:
    """根据照片数量 + 照片方向类型 自动选最合适的模板
    
    比原来纯靠数量判断更准确：
    - 竖图多 → sidebar / compact（竖向空间用得好）
    - 横图多 → wide / floating（横向展开）
    - 混合   → magazine（黄金比例布局，自动适配）
    """
    if photo_analysis is None:
        photo_analysis = {}

    dominant = photo_analysis.get("dominant", "portrait")
    mixed    = photo_analysis.get("mixed", False)
    total    = photo_count

    if total == 1:
        return "hero"
    if total == 2:
        return "sidebar"

    if mixed:
        # 混合比例 → magazine 最优（黄金比例，能同时容纳横竖图）
        return "magazine" if total >= 3 else "compact"

    if dominant == "landscape":
        # 横图为主
        return "wide" if total >= 4 else "floating"
    elif dominant == "portrait":
        # 竖图为主
        if total <= 4:
            return "compact"
        elif total <= 6:
            return "sidebar"
        else:
            return "wide"
    else:
        # 方图为主
        if total <= 4:
            return "grid4"
        else:
            return "grid6"


# ═══════════════════════════════════════════════════════════════
#  杂志风布局（黄金比例，自适应横竖混排）
# ═══════════════════════════════════════════════════════════════

GOLDEN = 1.618


def create_magazine_layout(photos: List[Image.Image], width: int, height: int) -> Image.Image:
    """杂志风黄金比例布局 - 自适应横竖混排，有视觉层次
    
    策略：
    - 按比例分类，竖图用大格，横图用宽格
    - 主图（第一张）占黄金比例面积
    - 其余图按分析结果填充右侧/底部网格
    - 深色底 + 极小间距，营造专业感
    """
    canvas = Image.new('RGB', (width, height), (22, 22, 26))
    gap = max(3, int(min(width, height) * 0.007))
    info_h = int(height * 0.10)
    photo_h = height - info_h - gap

    types = [classify_photo(p) for p in photos]
    total = min(len(photos), 7)

    # ── 单图 ────────────────────────────────────────────────────
    if total == 1:
        img = smart_crop(photos[0], width, photo_h)
        canvas.paste(img, (0, 0))
        return canvas

    # ── 主图宽度按黄金比例 ──────────────────────────────────────
    main_w = int(width / GOLDEN)        # ≈ 61.8%
    side_w = width - main_w - gap       # ≈ 38.2%

    # 主图（第一张）
    main_img = smart_crop(photos[0], main_w, photo_h, face_priority=True)
    canvas.paste(main_img, (0, 0))

    # ── 右侧剩余图 ──────────────────────────────────────────────
    rest = photos[1:total]
    n = len(rest)

    if n == 0:
        return canvas

    # 右侧按照 n 决定行数
    rows = min(n, 3)
    row_gap_total = gap * (rows - 1)
    cell_h = (photo_h - row_gap_total) // rows

    for i, photo in enumerate(rest[:rows]):
        y = i * (cell_h + gap)
        x = main_w + gap

        # 如果这一行有"超额"图（n > rows），最后一格横向再分两列
        if i == rows - 1 and n > rows:
            # 把剩余图横向排在最后一行
            remaining = rest[i:]
            n_rem = min(len(remaining), 3)
            sub_w = (side_w - gap * (n_rem - 1)) // n_rem
            for j, sub_photo in enumerate(remaining[:n_rem]):
                sx = x + j * (sub_w + gap)
                sub_img = smart_crop(sub_photo, sub_w, cell_h, face_priority=True)
                canvas.paste(sub_img, (sx, y))
        else:
            cell_img = smart_crop(photo, side_w, cell_h, face_priority=True)
            canvas.paste(cell_img, (x, y))

    return canvas


def get_batch_preview_combinations(photo_count: int, learn_data: dict = None) -> list:
    """生成批量预览的模板+风格组合，优先历史高频配置"""
    # 核心候选
    templates_by_count = {
        1: ["hero", "sidebar", "floating"],
        2: ["sidebar", "compact", "hero"],
        3: ["magazine", "sidebar", "wide", "compact"],
        4: ["magazine", "compact", "sidebar", "wide", "floating"],
        5: ["magazine", "sidebar", "wide", "compact", "floating"],
        6: ["magazine", "wide", "sidebar", "compact", "floating", "grid6"],
    }
    count_key = min(photo_count, 6)
    candidate_templates = templates_by_count.get(count_key, ["wide", "sidebar", "compact", "floating"])

    styles = ["anime", "elegant", "cyber", "retro", "japanese", "minimal"]

    # 如果有历史数据，把最常用的放最前
    if learn_data:
        pref_templates = learn_data.get("preferences", {}).get("templates", {})
        pref_styles = learn_data.get("preferences", {}).get("styles", {})
        if pref_templates:
            candidate_templates = sorted(
                set(candidate_templates),
                key=lambda t: -pref_templates.get(t, 0)
            )
        if pref_styles:
            styles = sorted(set(styles), key=lambda s: -pref_styles.get(s, 0))

    # 生成 6 种组合（模板优先，风格轮换）
    combos = []
    for i, tmpl in enumerate(candidate_templates[:6]):
        style = styles[i % len(styles)]
        combos.append((tmpl, style))
    # 补够 6 个
    while len(combos) < 6:
        combos.append(combos[-1])
    return combos[:6]


def generate_batch_preview(profile: CoserProfile, format_type: str, output_dir: str,
                           learn_data: dict = None) -> str:
    """批量生成多种组合的预览图，拼成一张选择图
    
    返回预览图路径
    """
    from PIL import ImageFont
    import tempfile, os

    combos = get_batch_preview_combinations(len(profile.photos), learn_data)
    
    # 每个小卡的尺寸（缩小到预览尺寸）
    preview_w, preview_h = FORMAT_SIZES.get(format_type, FORMAT_SIZES["wide"])
    thumb_scale = 0.35
    thumb_w = int(preview_w * thumb_scale)
    thumb_h = int(preview_h * thumb_scale)

    cols = 3
    rows = 2
    label_height = 55
    margin = 18
    
    total_w = cols * thumb_w + (cols + 1) * margin
    total_h = rows * (thumb_h + label_height) + (rows + 1) * margin

    canvas = Image.new('RGB', (total_w, total_h), (30, 30, 35))
    draw = ImageDraw.Draw(canvas)
    font = get_font(22)
    font_small = get_font(17)

    print(f"\n🎬 正在批量生成 {len(combos)} 种预览组合...")

    for idx, (tmpl, style) in enumerate(combos):
        row = idx // cols
        col = idx % cols
        x = margin + col * (thumb_w + margin)
        y = margin + row * (thumb_h + label_height + margin)

        # 生成这个组合的卡片（内存临时）
        try:
            # 直接调用内部布局函数，不走文件保存
            photos_loaded = []
            for path in profile.photos:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img = apply_style_effects(img, style)
                photos_loaded.append(img)

            if tmpl == "grid3":
                card = create_grid3_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "grid4":
                card = create_grid4_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "grid6":
                card = create_grid6_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "hero":
                card = create_hero_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "compact":
                card = create_compact_anime_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "sidebar":
                card = create_sidebar_layout(photos_loaded, preview_w, preview_h, sidebar_left=True)
            elif tmpl == "wide":
                card = create_wide_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "floating":
                card = create_floating_info_layout(photos_loaded, preview_w, preview_h)
            elif tmpl == "magazine":
                card = create_magazine_layout(photos_loaded, preview_w, preview_h)
            else:
                card = create_wide_layout(photos_loaded, preview_w, preview_h)

            add_info_section(card, profile, style, tmpl)

            # 缩放为预览尺寸
            thumb = card.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            canvas.paste(thumb, (x, y))

            # 序号标注（左上角）
            num_x, num_y = x + 8, y + 8
            draw.rectangle([num_x - 2, num_y - 2, num_x + 28, num_y + 26], fill=(0, 0, 0, 180))
            draw.text((num_x, num_y), f"#{idx+1}", font=font, fill=(255, 220, 80))

            # 底部标签
            label_y = y + thumb_h + 6
            label_text = f"#{idx+1} {tmpl} · {style}"
            draw.rectangle([x, label_y, x + thumb_w, label_y + label_height], fill=(20, 20, 25))
            draw.text((x + 8, label_y + 8), label_text, font=font_small, fill=(200, 200, 200))

            print(f"  ✓ #{idx+1} {tmpl} + {style}")
        except Exception as e:
            print(f"  ✗ #{idx+1} {tmpl} + {style} 失败: {e}")
            # 填充错误占位
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], fill=(60, 30, 30))
            draw.text((x + 10, y + thumb_h // 2), f"#{idx+1} 生成失败", font=font, fill=(200, 100, 100))

    # 顶部说明
    tip_text = f"批量预览 · {profile.name} · 格式: {format_type} · 看中哪个用 --template 和 --style 指定"
    draw.text((margin, 6), tip_text, font=font_small, fill=(140, 140, 140))

    preview_path = os.path.join(output_dir, f"{profile.name}_batch_preview_{format_type}.jpg")
    os.makedirs(output_dir, exist_ok=True)
    canvas.save(preview_path, quality=90)
    print(f"\n📋 预览图已保存: {preview_path}")
    print(f"   查看预览图后，用 --template <模板> --style <风格> 生成你满意的那个")
    
    # 打印组合对照表
    print(f"\n组合对照表:")
    for idx, (tmpl, style) in enumerate(combos):
        print(f"  #{idx+1}  --template {tmpl} --style {style}")
    
    return preview_path


def generate_card(profile: CoserProfile, template: str, style: str, 
                 format_type: str, output_path: str, add_watermark: bool = False):
    """生成单张模卡"""
    
    # 加载图片
    photos = []
    for path in profile.photos:
        try:
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # 应用风格滤镜
            img = apply_style_effects(img, style)
            photos.append(img)
        except Exception as e:
            print(f"错误: 无法加载图片 {path}: {e}")
    
    if not photos:
        print("错误: 没有可使用的照片")
        return False

    # ── 自动风格检测（用户没有明确指定时）─────────────────────
    if style == "auto":
        style = auto_style_from_photos(photos)
        print(f"  🎨 自动识别风格: {style} ({STYLE_CONFIGS[style]['name']})")

    # ── 自动模板选择（用户没有明确指定时）─────────────────────
    if template == "auto":
        analysis = analyze_photos(photos)
        template = smart_select_template(len(photos), analysis)
        print(f"  📐 自动选择模板: {template}  (照片构成: {analysis['portrait']}竖/{analysis['landscape']}横/{analysis['square']}方)")

    # 获取尺寸
    width, height = FORMAT_SIZES.get(format_type, FORMAT_SIZES["mobile"])
    
    # 根据模板创建布局
    if template == "grid3":
        canvas = create_grid3_layout(photos, width, height)
    elif template == "grid4":
        canvas = create_grid4_layout(photos, width, height)
    elif template == "grid6":
        canvas = create_grid6_layout(photos, width, height)
    elif template == "vertical":
        canvas = create_vertical_layout(photos, width, height)
    elif template == "horizontal":
        canvas = create_horizontal_layout(photos, width, height)
    elif template == "hero":
        canvas = create_hero_layout(photos, width, height)
    elif template == "film":
        canvas = create_film_layout(photos, width, height)
    elif template == "compact":
        canvas = create_compact_anime_layout(photos, width, height)
    elif template == "sidebar":
        canvas = create_sidebar_layout(photos, width, height, sidebar_left=True)
    elif template == "sidebar_right":
        canvas = create_sidebar_layout(photos, width, height, sidebar_left=False)
    elif template == "wide":
        canvas = create_wide_layout(photos, width, height)
    elif template == "floating":
        canvas = create_floating_info_layout(photos, width, height)
    elif template == "magazine":
        canvas = create_magazine_layout(photos, width, height)
    else:
        canvas = create_grid4_layout(photos, width, height)
    
    # 应用风格背景
    config = STYLE_CONFIGS.get(style, STYLE_CONFIGS["minimal"])
    
    # 添加信息区域
    add_info_section(canvas, profile, style, template)
    
    # 添加水印（可选）
    if add_watermark and profile.name:
        draw = ImageDraw.Draw(canvas)
        font_small = get_font(int(height * 0.018))
        watermark = f"@{profile.name}"
        draw.text((width - 150, height - 30), watermark, font=font_small, fill=(150, 150, 150, 128))
    
    # 保存
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    canvas.save(output_path, quality=95)
    print(f"已生成: {output_path}")
    
    # 生成后检测
    if not verify_card(output_path, profile):
        print(f"⚠️  警告: {output_path} 可能存在问题，请检查")
    
    return True


def verify_card(image_path: str, profile: CoserProfile) -> bool:
    """验证生成的模卡是否完整
    
    检查项：
    1. 图片是否能正常打开
    2. 图片尺寸是否正确
    3. 文件大小是否合理
    
    Returns:
        True: 检测通过
        False: 可能存在问题
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width < 500 or height < 500:
                print(f"  ⚠️  图片尺寸过小 ({width}x{height})")
                return False
            
            file_size = os.path.getsize(image_path)
            if file_size < 10 * 1024:  # 小于 10KB
                print(f"  ⚠️  文件过小 ({file_size} bytes)，可能生成失败")
                return False
            
            print(f"  ✓ 验证通过: {width}x{height}, {file_size/1024:.1f}KB")
            return True
            
    except Exception as e:
        print(f"  ✗ 验证失败: {e}")
        return False


def get_recommended_config(photo_count: int = 6, has_social: bool = False, has_location: bool = False) -> dict:
    """根据学习数据推荐最佳配置
    
    Returns:
        dict: 推荐的 template, style, format
    """
    import json
    import os
    
    learn_file = os.path.join(os.path.dirname(__file__), '..', 'learning_data.json')
    
    # 默认推荐
    default = {
        "template": "wide",
        "style": "anime",
        "format": "wide",
        "reason": "默认推荐：宽屏展示效果最佳"
    }
    
    if not os.path.exists(learn_file):
        return default
    
    try:
        with open(learn_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        pref = data.get("preferences", {})
        
        # 找出最常用的模板
        templates = pref.get("templates", {})
        if templates:
            best_template = max(templates, key=templates.get)
        else:
            best_template = "wide"
        
        # 找出最常用的风格
        styles = pref.get("styles", {})
        if styles:
            best_style = max(styles, key=styles.get)
        else:
            best_style = "anime"
        
        # 找出最常用的格式
        formats = pref.get("formats", {})
        if formats:
            best_format = max(formats, key=formats.get)
        else:
            best_format = "wide"
        
        # 根据条件调整
        reason = f"基于历史数据推荐：模板 '{best_template}' 使用 {templates.get(best_template, 0)} 次"
        
        if has_social and has_location:
            # 如果有社交和地点信息，推荐能显示更多信息的模板
            if best_template in ["sidebar", "wide"]:
                reason += "，适合展示完整信息"
        
        return {
            "template": best_template,
            "style": best_style,
            "format": best_format,
            "reason": reason
        }
        
    except Exception as e:
        return default


def mark_as_best(profile: CoserProfile, template: str, style: str, format_type: str):
    """标记某个配置为'最佳'，保存为默认模板"""
    import json
    import os
    from datetime import datetime
    
    learn_file = os.path.join(os.path.dirname(__file__), '..', 'learning_data.json')
    
    data = {"history": [], "preferences": {}, "best_configs": []}
    if os.path.exists(learn_file):
        try:
            with open(learn_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
    
    if "best_configs" not in data:
        data["best_configs"] = []
    
    # 添加最佳配置
    best_entry = {
        "name": profile.name,
        "template": template,
        "style": style,
        "format": format_type,
        "timestamp": datetime.now().isoformat()
    }
    data["best_configs"].append(best_entry)
    
    # 同时设置为默认推荐
    data["default_template"] = template
    data["default_style"] = style
    data["default_format"] = format_type
    
    with open(learn_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  ⭐ 已标记为最佳模板！")
    print(f"     模板: {template}, 风格: {style}, 格式: {format_type}")
    print(f"     下次将优先推荐此配置")


# 保存函数引用，供外部调用
__all__ = ['generate_card', 'CoserProfile', 'save_best_config', 'get_recommended_config', 'mark_as_best']


# 更新生成函数，自动保存配置
original_generate_card = generate_card

def generate_card_with_learning(profile: CoserProfile, template: str, style: str, 
                                 format_type: str, output_path: str, add_watermark: bool = False):
    """包装原生成函数，添加学习功能"""
    result = original_generate_card(profile, template, style, format_type, output_path, add_watermark)
    
    if result:
        # 保存配置到学习数据库
        save_best_config(profile, template, style, format_type, output_path)
    
    return result


# 替换原函数
import sys
sys.modules[__name__].generate_card = generate_card_with_learning


# 先定义学习功能函数，供包装函数使用
def save_best_config(profile: CoserProfile, template: str, style: str, format_type: str, output_path: str):
    """保存最佳配置到学习数据库
    
    记录用户偏好的模板/风格组合，用于未来推荐
    """
    import json
    import os
    from datetime import datetime
    
    # 学习数据库文件
    learn_file = os.path.join(os.path.dirname(__file__), '..', 'learning_data.json')
    
    # 读取现有数据
    data = {"history": [], "preferences": {}}
    if os.path.exists(learn_file):
        try:
            with open(learn_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
    
    # 记录这次生成
    entry = {
        "timestamp": datetime.now().isoformat(),
        "name": profile.name,
        "template": template,
        "style": style,
        "format": format_type,
        "output": os.path.basename(output_path),
        "has_social": bool(profile.douyin or profile.weibo or profile.bilibili),
        "has_location": bool(profile.location),
        "photo_count": len(profile.photos) if profile.photos else 0
    }
    data["history"].append(entry)
    
    # 更新偏好统计
    pref = data["preferences"]
    
    # 模板偏好
    if "templates" not in pref:
        pref["templates"] = {}
    pref["templates"][template] = pref["templates"].get(template, 0) + 1
    
    # 风格偏好
    if "styles" not in pref:
        pref["styles"] = {}
    pref["styles"][style] = pref["styles"].get(style, 0) + 1
    
    # 格式偏好
    if "formats" not in pref:
        pref["formats"] = {}
    pref["formats"][format_type] = pref["formats"].get(format_type, 0) + 1
    
    # 保存
    with open(learn_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  📝 配置已记录到学习数据库")


def verify_card(image_path: str, profile: CoserProfile) -> bool:
    """验证生成的模卡是否完整
    
    检查项：
    1. 图片是否能正常打开
    2. 图片尺寸是否正确
    3. （可选）文字是否被截断
    
    Returns:
        True: 检测通过
        False: 可能存在问题
    """
    try:
        with Image.open(image_path) as img:
            # 基本检查
            width, height = img.size
            if width < 500 or height < 500:
                print(f"  ⚠️  图片尺寸过小 ({width}x{height})")
                return False
            
            # 检查是否成功保存（文件大小）
            import os
            file_size = os.path.getsize(image_path)
            if file_size < 10 * 1024:  # 小于 10KB
                print(f"  ⚠️  文件过小 ({file_size} bytes)，可能生成失败")
                return False
            
            print(f"  ✓ 验证通过: {width}x{height}, {file_size/1024:.1f}KB")
            return True
            
    except Exception as e:
        print(f"  ✗ 验证失败: {e}")
        return False


def generate_demo(args):
    """生成演示数据用于测试"""
    from PIL import ImageDraw, ImageFont
    
    demo_dir = os.path.join(args.output if hasattr(args, 'output') else './output', 'demo_photos')
    os.makedirs(demo_dir, exist_ok=True)
    
    # 生成 6 张彩色测试图片
    colors = [
        (255, 182, 193),  # 粉红
        (173, 216, 230),  # 浅蓝
        (221, 160, 221),  # 紫罗兰
        (255, 218, 185),  # 桃色
        (152, 251, 152),  # 浅绿
        (255, 255, 224),  # 浅黄
    ]
    
    photo_paths = []
    for i, color in enumerate(colors):
        # 创建 3:4 比例的测试图
        img = Image.new('RGB', (600, 800), color)
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = f"Photo {i+1}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (600 - text_width) // 2
        y = (800 - text_height) // 2
        draw.text((x, y), text, fill=(50, 50, 50), font=font)
        
        path = os.path.join(demo_dir, f"demo_{i+1}.jpg")
        img.save(path)
        photo_paths.append(path)
        print(f"生成测试图片: {path}")
    
    print(f"\n演示图片已生成，保存在: {demo_dir}")
    print(f"\n现在可以运行:")
    print(f'  python coser_card.py --photos "{demo_dir}/*.jpg" --name "小樱" --template grid4 --style japanese')
    return True


def main():
    parser = argparse.ArgumentParser(description="Coser Card - 模卡生成器")
    parser.add_argument("--photos", help="照片路径（逗号分隔或通配符）")
    parser.add_argument("--name", help="CN名称")
    parser.add_argument("--cn", help="罗马音/英文名")
    parser.add_argument("--height", type=int, help="身高 cm")
    parser.add_argument("--weight", type=int, help="体重 kg")
    parser.add_argument("--bust", type=int, help="胸围 cm")
    parser.add_argument("--waist", type=int, help="腰围 cm")
    parser.add_argument("--hip", type=int, help="臀围 cm")
    parser.add_argument("--shoe", type=int, help="鞋码")
    parser.add_argument("--contact", help="联系方式")
    parser.add_argument("--location", help="所在城市")
    parser.add_argument("--experience", help="拍摄经验")
    parser.add_argument("--douyin", help="抖音账号/粉丝数")
    parser.add_argument("--weibo", help="微博账号")
    parser.add_argument("--bilibili", help="B站账号")
    parser.add_argument("--xiaohongshu", help="小红书账号")
    parser.add_argument("--template", default="grid4",
                       choices=["grid3", "grid4", "grid6", "vertical", "horizontal", "hero",
                                "film", "compact", "sidebar", "sidebar_right", "wide",
                                "floating", "magazine", "auto"],
                       help="排版模板（auto=根据照片自动选择）")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式输入信息")
    parser.add_argument("--style", default="minimal",
                       choices=["japanese", "elegant", "cyber", "retro", "minimal",
                                "colorful", "anime", "auto"],
                       help="风格模板（auto=根据照片色调自动匹配）")
    parser.add_argument("--formats", default="mobile",
                       help="输出格式，逗号分隔 (a4,mobile,square,banner,all)")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--config", help="从JSON配置文件读取")
    parser.add_argument("--watermark", action="store_true", help="添加水印")
    parser.add_argument("--demo", action="store_true", help="生成演示用的测试图片")
    parser.add_argument("--batch-preview", "-b", action="store_true",
                        help="批量生成6种组合预览图，快速挑选满意的风格（推荐首次使用）")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="快速模式：根据历史学习数据自动选最优模板+风格，无需手动指定")

    args = parser.parse_args()

    # 生成演示数据
    if args.demo:
        return generate_demo(args)
    
    # 交互式输入
    if args.interactive:
        profile = interactive_input()
        # 交互式输入后询问照片路径
        photos_input = input("\n照片路径（支持通配符如: *.jpg）: ").strip()
        profile.photos = load_photos(photos_input)
        if not profile.photos:
            print("错误: 没有找到照片")
            return
        # 询问模板和风格
        print("\n可用模板: grid3, grid4, grid6, compact, sidebar, sidebar_right, wide, floating")
        template_input = input("选择模板 [默认: floating]: ").strip()
        if template_input:
            args.template = template_input
        print("\n可用风格: japanese, elegant, cyber, retro, minimal, colorful, anime")
        style_input = input("选择风格 [默认: anime]: ").strip()
        if style_input:
            args.style = style_input
    elif args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取 profile 相关字段
        profile_fields = {k: v for k, v in data.items() if k in CoserProfile.__dataclass_fields__}
        profile = CoserProfile(**profile_fields)
        
        # 处理照片路径
        if "photos" in data:
            profile.photos = load_photos(",".join(data["photos"]))
        
        # 从配置文件读取模板和风格（如果存在）
        if "template" in data:
            args.template = data["template"]
        if "style" in data:
            args.style = data["style"]
        if "formats" in data:
            args.formats = data["formats"]
    else:
        # 检查必要参数
        if not args.photos or not args.name:
            parser.print_help()
            print("\n错误: 必须提供 --photos 和 --name 参数，或使用 --config 配置文件，或使用 -i 交互式输入")
            print("      使用 --demo 生成测试图片进行体验")
            return
            
        profile = CoserProfile(
            name=args.name,
            cn=args.cn or "",
            height=args.height or 0,
            weight=args.weight or 0,
            bust=args.bust or 0,
            waist=args.waist or 0,
            hip=args.hip or 0,
            shoe=args.shoe or 0,
            contact=args.contact or "",
            location=args.location or "",
            experience=args.experience or "",
            douyin=args.douyin or "",
            weibo=args.weibo or "",
            bilibili=args.bilibili or "",
            xiaohongshu=args.xiaohongshu or "",
            photos=load_photos(args.photos)
        )
    
    if not profile.photos:
        print("错误: 没有找到照片，请检查路径")
        return
    
    print(f"找到 {len(profile.photos)} 张照片")
    print(f"CN: {profile.name}")

    # ── 读取学习数据（供 quick / batch-preview 使用）──────────────────
    learn_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'learning_data.json')
    learn_data = None
    if os.path.exists(learn_file):
        try:
            with open(learn_file, 'r', encoding='utf-8') as f:
                learn_data = json.load(f)
        except:
            pass

    # ── 快速模式：自动选最优配置 ───────────────────────────────────────
    if args.quick:
        rec = get_recommended_config(
            photo_count=len(profile.photos),
            has_social=bool(profile.douyin or profile.weibo or profile.bilibili),
            has_location=bool(profile.location)
        )
        # 如果用户没有手动指定，用推荐值覆盖
        if args.template == parser.get_default("template"):
            args.template = rec["template"]
        if args.style == parser.get_default("style"):
            args.style = rec["style"]
        if args.formats == parser.get_default("formats"):
            args.formats = rec["format"]
        print(f"\n⚡ 快速模式：{rec['reason']}")
        print(f"   模板: {args.template}  风格: {args.style}  格式: {args.formats}")

    # ── 批量预览模式 ───────────────────────────────────────────────────
    if args.batch_preview:
        fmt = args.formats if args.formats not in ("all",) else "wide"
        # 加载照片做分析，用于预览组合排序
        sample_photos = []
        for path in profile.photos[:3]:
            try:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                sample_photos.append(img)
            except:
                pass
        if sample_photos:
            detected_style = auto_style_from_photos(sample_photos)
            analysis = analyze_photos(sample_photos)
            detected_tmpl = smart_select_template(len(profile.photos), analysis)
            print(f"\n🔍 照片分析结果:")
            print(f"   构成: {analysis['portrait']}张竖图 / {analysis['landscape']}张横图 / {analysis['square']}张方图")
            print(f"   推荐模板: {detected_tmpl}  推荐风格: {detected_style} (auto 模式会自动用这个)")
        generate_batch_preview(profile, fmt, args.output, learn_data)
        return

    print(f"模板: {args.template}")
    print(f"风格: {args.style}")
    
    # 解析输出格式
    if args.formats == "all":
        formats = ["a4", "mobile", "square"]
    else:
        formats = [f.strip() for f in args.formats.split(",")]
    
    # 生成各格式
    for fmt in formats:
        if fmt not in FORMAT_SIZES:
            print(f"警告: 未知格式 {fmt}，跳过")
            continue
        
        output_file = os.path.join(args.output, f"{profile.name}_{args.template}_{args.style}_{fmt}.jpg")
        generate_card(profile, args.template, args.style, fmt, output_file, args.watermark)
    
    print(f"\n✅ 完成！输出目录: {os.path.abspath(args.output)}")
    print(f"   生成了 {len(formats)} 种格式的模卡")


if __name__ == "__main__":
    main()
