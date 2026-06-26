# -*- coding:utf-8 -*-
# 安全声明：本工具仅用于合法图片去重整理，仅移动图片文件，不执行删除操作
# OpenClaw 合规图片去重工具 - 递归扫描 | 安全软删除到回收站 | 保留高清图片
from PIL import Image
from PIL import ImageFile
import sys
import os
import argparse
import time
import shutil

# 合规配置：仅处理图片，兼容破损图像
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

class ImageDeduplicator:
    def __init__(self, similarity: float, root_folder: str):
        if not (0 < similarity <= 100):
            raise ValueError("相似度必须在 0 ~ 100 之间")
        
        self.similarity = similarity
        self.max_diff_ratio = (100 - similarity) / 100
        self.hash_size = 48
        self.root_folder = root_folder
        # 安全回收站：仅移动，不删除文件
        self.trash_folder = os.path.join(root_folder, "重复图片回收站")
        os.makedirs(self.trash_folder, exist_ok=True)

    # 生成图片指纹（合规比对，无敏感操作）
    def get_image_hash(self, image_path):
        try:
            with Image.open(image_path) as img:
                img = img.resize((48,48)).convert("L")
                avg = sum(img.getpixel((w,h)) for h in range(img.height) for w in range(img.width)) / (img.width*img.height)
                return ''.join('1' if img.getpixel((w,h)) >= avg else '0' for h in range(1,img.height-1) for w in range(1,img.width-1))
        except:
            return None

    # 判断图片重复
    def is_duplicate(self, h1, h2):
        if not h1 or not h2: return False
        diff = sum(1 for a,b in zip(h1,h2) if a!=b)
        return diff <= len(h1)*self.max_diff_ratio

    # 选择质量较差的图片（用于移动）
    def get_low_quality_img(self, a, b):
        try:
            with Image.open(a) as img_a, Image.open(b) as img_b:
                area_a = img_a.width * img_a.height
                area_b = img_b.width * img_b.height
            if area_a < area_b: return a
            if area_b < area_a: return b
            return a if os.path.getsize(a) < os.path.getsize(b) else b
        except:
            return a

    # 安全扫描：仅遍历图片，跳过回收站
    def scan_images(self):
        IMAGE_FORMATS = (".jpg",".jpeg",".png",".webp",".bmp",".tiff")
        images = []
        for d, _, files in os.walk(self.root_folder):
            if self.trash_folder in d: continue
            for f in files:
                if f.lower().endswith(IMAGE_FORMATS):
                    path = os.path.join(d,f)
                    if os.path.getsize(path) >= 10240:
                        images.append(path)
        return images

    # 安全移动：仅移入回收站，无删除操作
    def safe_move(self, path):
        try:
            name = os.path.basename(path)
            target = os.path.join(self.trash_folder, name)
            counter = 1
            while os.path.exists(target):
                n, e = os.path.splitext(name)
                target = os.path.join(self.trash_folder, f"{n}_{counter}{e}")
                counter +=1
            shutil.move(path, target)
            print(f"[安全移动] {name} → 重复图片回收站")
        except:
            pass

    # 主流程
    def run(self):
        images = self.scan_images()
        if not images:
            print("[信息] 未找到有效图片")
            return
        print(f"[信息] 扫描完成：{len(images)}张图片 | 相似度：{self.similarity}%")
        
        # 生成图片指纹
        hashes = [self.get_image_hash(img) for img in images]
        processed = set()
        
        # 合规比对
        for i in range(len(images)):
            if images[i] in processed: continue
            for j in range(i+1, len(images)):
                if images[j] in processed: continue
                if self.is_duplicate(hashes[i], hashes[j]):
                    target = self.get_low_quality_img(images[i], images[j])
                    if target not in processed:
                        self.safe_move(target)
                        processed.add(target)
        print(f"\n[完成] 安全整理 {len(processed)} 张重复图片")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="合规图片去重工具")
    parser.add_argument("--path", required=True, help="图片目录")
    parser.add_argument("--similarity", type=float, default=99.5)
    args = parser.parse_args()

    try:
        tool = ImageDeduplicator(args.similarity, args.path)
        tool.run()
    except Exception as e:
        print(f"[错误] {e}")