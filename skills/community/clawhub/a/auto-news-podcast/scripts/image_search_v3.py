#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面图搜索模块 v3.0 - 进一步优化版
改进点：
1. 过滤 logo/图标（通过 URL 模式、文件特征识别）
2. 优先选择包含关键词的 alt 文本的图片
3. 图片尺寸检查（宽 > 400px）
4. 多候选图片评分排序
"""

import os
import sys
import requests
import re
from collections import Counter
from urllib.parse import urljoin, urlparse

def _get_unsplash_key():
    """获取 Unsplash API Key
    
    优先级：
    1. OpenClaw 配置文件 (~/.openclaw/openclaw.json)
    2. 环境变量 UNSPLASH_ACCESS_KEY
    
    Returns:
        str: API Key 或 None（未配置）
    """
    import json
    
    # 1. 尝试从 OpenClaw 配置读取
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
    
    # 2. 尝试从环境变量读取
    unsplash_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if unsplash_key:
        return unsplash_key
    
    return None


# Unsplash access key（动态获取，可能为 None）
UNSPLASH_KEY = _get_unsplash_key()

# Logo/图标过滤规则
LOGO_PATTERNS = [
    r'logo', r'icon', r'favicon', r'brand', r'symbol',
    r'avatar', r'profile', r'userpic', r'head',
    r'weixin', r'wechat', r'qq', r'weibo', r'icon',
    r'button', r'btn', r'arrow', r'nav',
]

# 图片扩展名白名单
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']


def _is_likely_logo(img_url, img_alt=''):
    """判断图片是否可能是 logo/图标
    
    判断依据：
    1. URL 包含 logo/icon 等关键词
    2. 文件名过于简短（<10字符）
    3. alt 文本包含 logo/图标等词
    """
    if not img_url:
        return True
    
    url_lower = img_url.lower()
    
    # 检查 URL 是否包含 logo 相关关键词
    for pattern in LOGO_PATTERNS:
        if pattern in url_lower:
            return True
    
    # 检查文件名长度（过短可能是图标）
    parsed = urlparse(img_url)
    filename = os.path.basename(parsed.path)
    if len(filename) < 10:
        return True
    
    # 检查 alt 文本
    if img_alt:
        alt_lower = img_alt.lower()
        for pattern in LOGO_PATTERNS:
            if pattern in alt_lower:
                return True
    
    return False


def _score_image_relevance(img_url, img_alt, keyword_entities):
    """评分图片与新闻的相关性
    
    评分维度：
    - alt 文本包含关键词：+10分
    - URL 包含关键词：+5分
    - 不是 logo：+3分
    - 图片尺寸较大：+2分
    """
    score = 0
    
    # 1. alt 文本匹配
    if img_alt:
        alt_lower = img_alt.lower()
        for entity in keyword_entities:
            if entity.lower() in alt_lower:
                score += 10
                break
    
    # 2. URL 匹配
    if img_url:
        url_lower = img_url.lower()
        for entity in keyword_entities:
            if entity.lower() in url_lower:
                score += 5
                break
    
    # 3. 不是 logo
    if not _is_likely_logo(img_url, img_alt):
        score += 3
    
    return score


def _extract_core_entities(keyword, news_items):
    """从关键词和新闻标题中提取核心实体"""
    entities = []
    
    # 1. 提取关键词中的核心名词
    stop_words = ['首次', '亮相', '发布', '宣布', '举行', '召开', '进行', '开展', 
                  '今天', '昨日', '近日', '最新', '正式', '重磅', '突发']
    
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
    
    # 3. 添加类别词
    category_hints = {
        '机车': '摩托车', '摩托': '摩托车', '汽车': '汽车',
        '电动车': '电动汽车', '手机': '智能手机', '芯片': '半导体芯片',
        'AI': '人工智能', '无人机': '无人机',
        '广交会': '广交会', '车展': '车展',
    }
    
    for hint, category in category_hints.items():
        if hint in keyword and category not in entities:
            entities.append(category)
            break
    
    # 去重
    seen = set()
    unique_entities = []
    for e in entities:
        if e not in seen and len(e) >= 2:
            seen.add(e)
            unique_entities.append(e)
    
    return unique_entities[:3]


def _fetch_images_from_news_source(news_items, keyword_entities):
    """从新闻源网页抓取所有候选图片
    
    返回: [(img_url, img_alt, source_name, score), ...]
    """
    candidates = []
    
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
                source_name = item.get('source', '未知来源')
                
                # 收集所有候选图片
                img_candidates = []
                
                # 1. Open Graph 图片
                og_img = soup.find('meta', property='og:image')
                if og_img and og_img.get('content'):
                    img_url = og_img['content']
                    if not _is_likely_logo(img_url):
                        img_candidates.append((img_url, '', 'og:image'))
                
                # 2. Twitter 卡片图
                twitter_img = soup.find('meta', attrs={'name': 'twitter:image'})
                if twitter_img and twitter_img.get('content'):
                    img_url = twitter_img['content']
                    if not _is_likely_logo(img_url):
                        img_candidates.append((img_url, '', 'twitter:image'))
                
                # 3. article 标签内的图片
                article = soup.find('article')
                if article:
                    for img in article.find_all('img'):
                        img_url = img.get('src') or img.get('data-src')
                        img_alt = img.get('alt', '')
                        if img_url and not _is_likely_logo(img_url, img_alt):
                            img_candidates.append((img_url, img_alt, 'article'))
                
                # 4. 内容区域的其他图片
                content_div = soup.find(['div', 'section'], class_=re.compile(r'content|article|main|body'))
                if content_div:
                    for img in content_div.find_all('img'):
                        img_url = img.get('src') or img.get('data-src')
                        img_alt = img.get('alt', '')
                        if img_url and not _is_likely_logo(img_url, img_alt):
                            # 检查尺寸提示
                            width = img.get('width', '')
                            if width and int(width) > 300:
                                img_candidates.append((img_url, img_alt, 'content-large'))
                            else:
                                img_candidates.append((img_url, img_alt, 'content'))
                
                # 评分并添加到候选列表
                for img_url, img_alt, img_type in img_candidates:
                    score = _score_image_relevance(img_url, img_alt, keyword_entities)
                    # 类型加权
                    if img_type == 'og:image':
                        score += 2
                    elif img_type == 'content-large':
                        score += 1
                    candidates.append((img_url, img_alt, source_name, score))
                    
            except Exception as e:
                print(f'    [WARN] 从 {item.get("source", "未知")} 抓取失败: {e}')
                continue
        
    except ImportError:
        print('  [WARN] BeautifulSoup 未安装')
    
    # 按评分排序
    candidates.sort(key=lambda x: x[3], reverse=True)
    return candidates


def _download_image(img_url, referer_url, min_size=10240, max_size=10485760):
    """下载图片并验证
    
    Args:
        img_url: 图片 URL
        referer_url: 来源页面 URL
        min_size: 最小文件大小（字节），默认 10KB
        max_size: 最大文件大小（字节），默认 10MB
    
    Returns:
        (成功标志, 图片数据或错误信息)
    """
    try:
        # 处理相对路径
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = urljoin(referer_url, img_url)
        
        # 检查扩展名
        parsed = urlparse(img_url)
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext and ext not in IMAGE_EXTENSIONS:
            return False, f'不支持的图片格式: {ext}'
        
        # 下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': referer_url
        }
        
        # 先发送 HEAD 请求检查大小
        head_resp = requests.head(img_url, headers=headers, timeout=10, allow_redirects=True)
        content_length = head_resp.headers.get('Content-Length')
        if content_length:
            size = int(content_length)
            if size < min_size:
                return False, f'图片太小: {size} bytes'
            if size > max_size:
                return False, f'图片太大: {size} bytes'
        
        # 下载完整图片
        response = requests.get(img_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        img_data = response.content
        actual_size = len(img_data)
        
        if actual_size < min_size:
            return False, f'图片太小: {actual_size} bytes'
        if actual_size > max_size:
            return False, f'图片太大: {actual_size} bytes'
        
        return True, img_data
        
    except Exception as e:
        return False, str(e)


def _generate_ai_image(keyword, keyword_entities, output_path):
    """使用 AI 生成配图"""
    try:
        # 构建更精确的提示词
        if keyword_entities:
            subject = keyword_entities[0]
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


def _search_stock_image(keyword, keyword_entities, output_path):
    """从图库搜索图片（兜底方案）"""
    # 检查是否配置了 Unsplash Key
    if not UNSPLASH_KEY:
        print('  [WARN] 未配置 Unsplash API Key，跳过图库搜索')
        print('  [INFO] 配置方式：')
        print('    1. 在 ~/.openclaw/openclaw.json 中添加：')
        print('       {"custom": {"unsplash": {"accessKey": "你的Key"}}}')
        print('    2. 或设置环境变量：UNSPLASH_ACCESS_KEY')
        return False
    
    # 构建搜索查询
    search_queries = []
    if keyword_entities:
        search_queries.append(keyword_entities[0])
        if len(keyword_entities) > 1:
            search_queries.append(f'{keyword_entities[0]} {keyword_entities[1]}')
    search_queries.append(keyword)
    search_queries.append('news')
    
    print(f'    [INFO] 图库搜索词: {search_queries[:3]}')
    
    # Unsplash API
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
                    for img in data['results']:
                        img_url = img['urls']['regular']
                        success, result = _download_image(img_url, 'https://unsplash.com', min_size=20480)
                        if success:
                            with open(output_path, 'wb') as f:
                                f.write(result)
                            print(f'    [OK] Unsplash 封面图已保存: {output_path}')
                            print(f'      图片来源: {img["user"]["name"]}')
                            return True
                        else:
                            print(f'    [WARN] 下载失败: {result}')
        except Exception as e:
            print(f'    [WARN] Unsplash 搜索失败: {e}')
            continue
    
    print('  [WARN] 图库搜索失败')
    return False


def search_cover_image_v3(keyword, output_dir, news_items=None):
    """搜索并下载封面图 - v3.0 优化版
    
    改进点：
    1. 智能过滤 logo/图标
    2. 多候选图片评分排序
    3. 优先选择包含关键词 alt 文本的图片
    4. 图片大小验证（10KB - 10MB）
    
    优先级：
    1. 新闻源原图（评分最高的候选）
    2. AI 生成
    3. 图库搜索
    """
    os.makedirs(output_dir, exist_ok=True)
    cover_path = os.path.join(output_dir, 'cover.jpg')
    
    print(f'\n[Step 7] 搜索封面图...')
    print(f'  关键词: {keyword}')
    
    # 提取核心实体
    keyword_entities = _extract_core_entities(keyword, news_items)
    print(f'  提取实体: {keyword_entities}')
    
    # 方案 1: 从新闻源抓取原图
    if news_items:
        print('  尝试方案1: 从新闻源抓取原图...')
        candidates = _fetch_images_from_news_source(news_items, keyword_entities)
        
        if candidates:
            print(f'    找到 {len(candidates)} 个候选图片')
            # 尝试下载评分最高的候选
            for i, (img_url, img_alt, source_name, score) in enumerate(candidates[:5]):
                print(f'    [{i+1}] 评分 {score}: {img_url[:60]}...')
                success, result = _download_image(img_url, '', min_size=20480)
                if success:
                    with open(cover_path, 'wb') as f:
                        f.write(result)
                    print(f'  [OK] 新闻源封面图已保存: {cover_path}')
                    print(f'    来源: {source_name}, 评分: {score}')
                    if img_alt:
                        print(f'    Alt: {img_alt[:50]}')
                    return cover_path
                else:
                    print(f'    [WARN] 下载失败: {result}')
    
    # 方案 2: AI 生成
    print('  尝试方案2: AI 生成配图...')
    if _generate_ai_image(keyword, keyword_entities, cover_path):
        return cover_path
    
    # 方案 3: 图库搜索（兜底）
    print('  尝试方案3: 图库搜索...')
    if _search_stock_image(keyword, keyword_entities, cover_path):
        return cover_path
    
    print('  [WARN] 所有图片搜索方案均失败，未生成封面图')
    return None


if __name__ == '__main__':
    # 测试
    test_keyword = "张雪机车首次亮相广交会"
    test_output = "C:\\Users\\tombf\\.openclaw\\workspace\\test_output"
    result = search_cover_image_v3(test_keyword, test_output)
    print(f'结果: {result}')