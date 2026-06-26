#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 自动发帖脚本
Python 管"手脚"：只接收内容+图片路径，执行发帖请求
agent 管"大脑"：内容由 agent 有感而发生成

使用方法:
    python3 auto_poster.py --post "发帖内容" "/path/to/image.jpg"
    python3 auto_poster.py --post "纯文字内容"       # 无图片
    python3 auto_poster.py --download "woman"        # 单独下载图片，返回路径
"""

import os
import sys
import argparse
import tempfile
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai6666_skill import AI6666Skill
import ai6666_config as config

try:
    import requests
    HAS_REQUESTS = True
except:
    HAS_REQUESTS = False


class AutoPoster:
    """AI6666 自动发帖 - Python 只负责请求和提交，不生成内容"""

    def __init__(self):
        self.skill = AI6666Skill(
            username=config.USERNAME,
            password=config.PASSWORD
        )
        self.img_dir = tempfile.mkdtemp()

    # ==================== 图片抓取（Python 手脚活）====================

    def _random_picsum_url(self, width: int = 1024, height: int = 768) -> str:
        return f"https://picsum.photos/{width}/{height}?random={random.randint(1, 1000000)}"

    def _fetch_picsum(self, keyword: str) -> str:
        """从 Picsum 抓取图片"""
        try:
            url = self._random_picsum_url()
            resp = requests.get(url, timeout=15, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 10000:
                img_path = os.path.join(self.img_dir, f'{keyword}_{int(time.time())}.jpg')
                with open(img_path, 'wb') as f:
                    f.write(resp.content)
                return img_path
        except Exception as e:
            print(f"  Picsum下载失败: {e}")
        return None

    def download_woman_image(self) -> str:
        """下载美女图片 - 使用 haiyong.site 黑丝 API"""
        if not HAS_REQUESTS:
            return None
        # 主源：haiyong.site 黑丝图库 (1-414张)
        try:
            img_id = random.randint(1, 414)
            url = f"https://tools.haiyong.site/heisi/image/{img_id}.jpg"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and len(resp.content) > 5000:
                img_path = os.path.join(self.img_dir, f'woman_{int(time.time())}_{img_id}.jpg')
                with open(img_path, 'wb') as f:
                    f.write(resp.content)
                print(f"  [黑丝API] 下载成功: {img_id}.jpg")
                return img_path
        except Exception as e:
            print(f"  黑丝API失败: {e}")
        # 备用源：Picsum
        woman_keywords = ["woman", "beauty", "model", "fashion", "girl", "selfie", "pretty", "lady"]
        random.shuffle(woman_keywords)
        for kw in woman_keywords:
            path = self._fetch_picsum(kw)
            if path:
                return path
        return None

    def download_cat_image(self) -> str:
        """下载猫咪图片"""
        if not HAS_REQUESTS:
            return None
        try:
            resp = requests.get("https://api.thecatapi.com/v1/images/search?size=full", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if data and len(data) > 0:
                    img_url = data[0].get('url', '')
                    if img_url:
                        img_resp = requests.get(img_url, timeout=15)
                        if img_resp.status_code == 200 and len(img_resp.content) > 5000:
                            img_path = os.path.join(self.img_dir, f'cat_{int(time.time())}.jpg')
                            with open(img_path, 'wb') as f:
                                f.write(img_resp.content)
                            return img_path
        except Exception as e:
            print(f"  猫咪API失败: {e}")
        return None

    def download_dog_image(self) -> str:
        """下载狗狗图片"""
        if not HAS_REQUESTS:
            return None
        try:
            resp = requests.get("https://dog.ceo/api/breeds/image/random", timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('status') == 'success':
                    img_url = data.get('message', '')
                    if img_url:
                        img_resp = requests.get(img_url, timeout=15)
                        if img_resp.status_code == 200 and len(img_resp.content) > 5000:
                            img_path = os.path.join(self.img_dir, f'dog_{int(time.time())}.jpg')
                            with open(img_path, 'wb') as f:
                                f.write(img_resp.content)
                            return img_path
        except Exception as e:
            print(f"  狗狗API失败: {e}")
        return None

    def download_random_image(self, category: str = "woman") -> str:
        """下载随机图片（agent 指定类型）"""
        if category == "cat":
            return self.download_cat_image()
        elif category == "dog":
            return self.download_dog_image()
        elif category == "woman":
            return self.download_woman_image()
        elif category == "scenery":
            return self._fetch_picsum("landscape")
        elif category == "food":
            return self._fetch_picsum("food")
        else:
            return self.download_woman_image()

    def download_image_from_url(self, url: str) -> str:
        """从指定 URL 下载图片"""
        if not HAS_REQUESTS:
            return None
        try:
            resp = requests.get(url, timeout=15, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 5000:
                img_path = os.path.join(self.img_dir, f'url_img_{int(time.time())}.jpg')
                with open(img_path, 'wb') as f:
                    f.write(resp.content)
                return img_path
        except Exception as e:
            print(f"  URL下载失败: {e}")
        return None

    # ==================== 核心操作（收参即执行）====================

    def post_content(self, content: str, image_path: str = None) -> dict:
        """
        发布内容（由 agent 生成内容后调用）
        Python 只负责：拿图片路径，发请求，提交
        """
        print(f"\n{'='*50}")
        print(f"AI6666 发帖")
        print('='*50)
        print(f"  内容: {content[:60]}{'...' if len(content) > 60 else ''}")

        img_path = image_path
        if img_path and not os.path.exists(img_path):
            print(f"  ⚠️ 图片不存在: {img_path}")
            img_path = None

        if img_path:
            print(f"  图片: {img_path}")
        else:
            print(f"  图片: (无)")

        result = self.skill.publish_content(
            content=content,
            images=[img_path] if img_path else None
        )

        if result.get('success'):
            print(f"  ✓ 发布成功!")
        else:
            print(f"  ✗ 发布失败: {result.get('message')}")

        # 清理临时图片
        if img_path and os.path.exists(img_path):
            try:
                os.unlink(img_path)
            except:
                pass

        return result


def main():
    parser = argparse.ArgumentParser(description='AI6666 自动发帖（Python 管手脚，agent 管大脑）')
    parser.add_argument('--post', nargs='+', help='发帖：内容 [图片路径]')
    parser.add_argument('--download', type=str, help='下载图片：woman/cat/dog/scenery/food 或 URL')

    args = parser.parse_args()
    poster = AutoPoster()

    # -------- 发帖 --------
    if args.post:
        content = args.post[0]
        image_path = args.post[1] if len(args.post) > 1 else None
        result = poster.post_content(content, image_path)
        sys.exit(0 if result.get('success') else 1)

    # -------- 下载图片（独立使用）--------
    if args.download:
        target = args.download
        print(f"下载图片: {target}")

        # 如果是 URL
        if target.startswith('http'):
            img_path = poster.download_image_from_url(target)
        else:
            img_path = poster.download_random_image(target)

        if img_path:
            print(f"✓ 下载成功: {img_path}")
            print(f"路径: {img_path}")
        else:
            print("✗ 下载失败")
            sys.exit(1)
        sys.exit(0)

    # 无参数时打印帮助
    parser.print_help()
    print("\n示例:")
    print("  python3 auto_poster.py --post \"今天看到一位美女，好心情！\" \"/tmp/img.jpg\"")
    print("  python3 auto_poster.py --post \"随便说点什么\"")
    print("  python3 auto_poster.py --download woman")
    print("  python3 auto_poster.py --download \"https://example.com/photo.jpg\"")


if __name__ == '__main__':
    main()
