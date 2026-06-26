#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面图搜索模块 v2.0 - 优化版
组合策略：新闻源原图 → AI生成 → 图库搜索
"""

import os
import sys
import requests
import re
from collections import Counter

def _get_unsplash_key():
    """获取 Unsplash API Key"""
    import json
    
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                unsplash_key = config.get('custom', {}).get('unsplash', {}).get('accessKey')
                if unsplash_key:
                    return unsplash_key
                unsplash_key = config.get('env', {}).get('UNSPLASH_ACCESS_KEY')
                if unsplash_key:
                    return unsplash_key
        except Exception:
            pass
    
    unsplash_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if unsplash_key:
        return unsplash_key
    
    return None


UNSPLASH_KEY = _get_unsplash_key()


def _extract_core_entities(keyword, news_items):
    """从关键词和新闻标题中提取核心实体，用于优化图片搜索
    
    例如：
    - "张雪机车首次亮相广交会" → ["张雪机车", "广交会", "摩托车"]
    - "华为 Mate80 发布" → ["华为", "Mate80", "手机"]
    """
    entities = []
    
    # 1. 提取关键词中的核心名词（去除动词和时间词）
    stop_words = ['首次', '亮相', '发布', '宣布', '举行', '召开', '进行', '开展', 
                  '今天', '昨日', '近日', '最新', '正式', '重磅', '突发', '首次']
    
    keyword_clean = keyword
    for sw in stop_words:
        keyword_clean = keyword_clean.replace(sw, '')
    keyword_clean = keyword_clean.strip()
    
    if keyword_clean:
        entities.append(keyword_clean)
    
    # 2. 从新闻标题中提取高频实体词
    if news_items:
        all_titles = ' '.join([item.get('title', '') for item in news_items[:5]])
        words = re.findall(r'[\u4e00-\u9fa5]{2,8}', all_titles)
        word_freq = Counter(words)
        top_words = [w for w, c in word_freq.most_common(3) if c >= 1 and len(w) >= 2]
        entities.extend(top_words)
    
    # 3. 添加类别词作为兜底
    category_hints = {
        '机车': '摩托车',
        '摩托': '摩托车',
        '汽车': '汽车',
        '电动车': '电动汽车',
        '手机': '智能手机',
        '芯片': '半导体芯片',
        'AI': '人工智能',
        '无人机': '无人机',
        '广交会': '广交会 展会',
        '车展': '汽车展览',
    }
    
    for hint, category in category_hints.items():
        if hint in keyword and category not in entities:
            entities.append(category)
            break
    
    # 去重并保持顺序
    seen = set()
    unique_entities = []
    for e in entities:
        if e not in seen and len(e) >= 2:
            seen.add(e)
            unique_entities.append(e)
    
    return unique_entities[:3]


def _fetch_image_from_news_source(news_items, keyword):
    """从新闻源网页抓取配图 - 优化版
    
    抓取策略优先级：
    1. og:image（Open Graph 标准，社交媒体分享图）
    2. twitter:image（Twitter 卡片图）
    3. article 标签内的首图
    4. 内容区域的大图（>300px）
    """
    try:
        from bs4 import BeautifulSoup
        
        for item in news_items[:5]:
            url = item.get('url', '')
            if not url or not url.startswith('http'):
                continue
            
            try:
                response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                img_url = None
                source_name = item.get('source', '未知来源')
                
                # 策略1: Open Graph 图片
                og_img = soup.find('meta', property='og:image')
                if og_img and og_img.get('content'):
                    img_url = og_img['content']
                    print(f'    [INFO] 从 {source_name} 获取 og:image')
                
                # 策略2: Twitter 卡片图
                if not img_url:
                    twitter_img = soup.find('meta', attrs={'name': 'twitter:image'})
                    if twitter_img and twitter_img.get('content'):
                        img_url = twitter_img['content']
                        print(f'    [INFO] 从 {source_name} 获取 twitter:image')
                
                # 策略3: article 标签内的首图
                if not img_url:
                    article = soup.find('article')
                    if article:
                        img = article.find('img')
                        if img:
                            img_url = img.get('src') or img.get('data-src')
                            if img_url:
                                print(f'    [INFO] 从 {source_name} article 获取图片')
                
                # 策略4: 内容区域的大图
                if not img_url:
                    content_div = soup.find(['div', 'section'], class_=re.compile(r'content|article|main|body'))
                    if content_div:
                        imgs = content_div.find_all('img')
                        for img in imgs:
                            src = img.get('src') or img.get('data-src')
                            if src:
                                # 检查图片尺寸提示
                                width = img.get('width', '')
                                if width and int(width) > 300:
                                    img_url = src
                                    print(f'    [INFO] 从 {source_name} 内容区获取大图')
                                    break
                                # 没有尺寸信息，取第一张
                                if not img_url:
                                    img_url = src
                                    print(f'    [INFO] 从 {source_name} 内容区获取图片')
                
                # 策略5: 任何带 alt 包含关键词的图片
                if not img_url:
                    imgs = soup.find_all('img', alt=re.compile(keyword[:4], re.I))
                    if imgs:
                        img_url = imgs[0].get('src') or imgs[0].get('data-src')
                        if img_url:
                            print(f'    [INFO] 从 {source_name} 获取关键词匹配图片')
                
                if img_url:
                    # 处理相对路径
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        from urllib.parse import urljoin
                        img_url = urljoin(url, img_url)
                    
                    # 下载图片
                    img_response = requests.get(img_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': url
                    }, timeout=15)
                    img_response.raise_for_status()
                    
                    # 检查图片大小（至少10KB，避免下载到图标）
                    if len(img_response.content) < 10240:
                        print(f'    [WARN] 图片太小 ({len(img_response.content)} bytes)，跳过')
                        continue
                    
                    return img_response.content, source_name
                    
            except Exception as e:
                print(f'    [WARN] 从 {item.get("source", "未知")} 抓取失败: {e}')
                continue
        
        return None, None
        
    except ImportError:
        print('  [WARN] BeautifulSoup 未安装，跳过网页抓取')
        return None, None
    except Exception as e:
        print(f'  [WARN] 新闻源抓取失败: {e}')
        return None, None


def _generate_ai_image(keyword, news_items, output_path):
    """使用 AI 生成配图"""
    try:
        # 提取关键信息用于生成提示词
        entities = _extract_core_entities(keyword, news_items)
        
        # 构建更精确的提示词
        if entities:
            subject = entities[0]
            prompt = f'{subject} 新闻配图，专业摄影风格，高清，适合新闻播报封面，16:9 横版构图'
        else:
            prompt = f'{keyword} 新闻配图，专业摄影风格，高清，适合新闻播报封面'
        
        print(f'    [INFO] AI 生成提示词: {prompt}')
        
        # 尝试使用 autoglm-generate-image
        autoglm_skill = os.path.expanduser('~/.agents/skills/autoglm-generate-image')
        if os.path.exists(autoglm_skill):
            import subprocess
            script_path = os.path.join(autoglm_skill, 'scripts', 'generate.py')
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path,
                     '--prompt', prompt,
                     '--output', output_path],
                    capture_output=True, text=True, timeout=120)
                if result.returncode == 0 and os.path.exists(output_path):
                    print(f'    [OK] AI 生成封面图已保存: {output_path}')
                    return True
        
        print('  [WARN] AI 生成失败')
        return False
        
    except Exception as e:
        print(f'  [WARN] AI 生成失败: {e}')
        return False


def _search_stock_image(keyword, news_items, output_path):
    """从图库搜索图片（兜底方案）"""
    # 检查是否配置了 Unsplash Key
    if not UNSPLASH_KEY:
        print('  [WARN] 未配置 Unsplash API Key，跳过图库搜索')
        print('  [INFO] 配置方式：')
        print('    1. 在 ~/.openclaw/openclaw.json 中添加：')
        print('       {"custom": {"unsplash": {"accessKey": "你的Key"}}}')
        print('    2. 或设置环境变量：UNSPLASH_ACCESS_KEY')
        return False
    
    # 提取核心实体，优化搜索词
    entities = _extract_core_entities(keyword, news_items)
    
    # 构建搜索查询（优先使用核心实体）
    search_queries = []
    if entities:
        search_queries.append(entities[0])  # 最相关的实体
        if len(entities) > 1:
            search_queries.append(f'{entities[0]} {entities[1]}')  # 组合查询
    search_queries.append(keyword)  # 原始关键词
    search_queries.extend(['news', 'breaking news'])  # 兜底
    
    print(f'    [INFO] 图库搜索词: {search_queries[:3]}')
    
    # 方案 1: Unsplash API
    for q in search_queries[:3]:
        try:
            print(f'    [INFO] Unsplash 搜索: {q}')
            r = requests.get('https://api.unsplash.com/search/photos',
                             params={'query': q, 'per_page': 5, 'orientation': 'landscape'},
                             headers={'Authorization': f'Client-ID {UNSPLASH_KEY}'},
                             timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('results'):
                    # 选择最相关的图片（简单策略：第一个）
                    for img in data['results'][:3]:
                        img_url = img['urls']['regular']
                        img_data = requests.get(img_url, timeout=15).content
                        if len(img_data) >= 10240:  # 至少10KB
                            with open(output_path, 'wb') as f:
                                f.write(img_data)
                            print(f'    [OK] Unsplash 封面图已保存: {output_path}')
                            print(f'      图片来源: {img["user"]["name"]}')
                            return True
        except Exception as e:
            print(f'    [WARN] Unsplash 搜索失败: {e}')
            continue
    
    print('  [WARN] 图库搜索失败')
    return False


def search_cover_image_v2(keyword, output_dir, news_items=None):
    """搜索并下载封面图 - 组合策略优化版
    
    优先级：
    1. 从新闻源网页抓取原图（最准确）
    2. AI 生成配图（最可控）
    3. 图库搜索（兜底）
    """
    os.makedirs(output_dir, exist_ok=True)
    cover_path = os.path.join(output_dir, 'cover.jpg')
    
    print(f'\n[Step 7] 搜索封面图...')
    print(f'  关键词: {keyword}')
    
    # 方案 1: 从新闻源抓取原图
    if news_items:
        print('  尝试方案1: 从新闻源抓取原图...')
        img_data, source = _fetch_image_from_news_source(news_items, keyword)
        if img_data:
            with open(cover_path, 'wb') as f:
                f.write(img_data)
            print(f'  [OK] 新闻源封面图已保存: {cover_path}')
            print(f'    来源: {source}')
            return cover_path
    
    # 方案 2: AI 生成
    print('  尝试方案2: AI 生成配图...')
    if _generate_ai_image(keyword, news_items, cover_path):
        return cover_path
    
    # 方案 3: 图库搜索（兜底）
    print('  尝试方案3: 图库搜索...')
    if _search_stock_image(keyword, news_items, cover_path):
        return cover_path
    
    print('  [WARN] 所有图片搜索方案均失败，未生成封面图')
    return None


if __name__ == '__main__':
    # 测试
    test_keyword = "张雪机车首次亮相广交会"
    test_output = "C:\\Users\\tombf\\.openclaw\\workspace\\test_output"
    result = search_cover_image_v2(test_keyword, test_output)
    print(f'结果: {result}')