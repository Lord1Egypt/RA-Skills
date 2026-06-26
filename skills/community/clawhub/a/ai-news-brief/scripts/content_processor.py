#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的内容获取和摘要生成模块
"""

import re
import json
import requests
import websocket
import time

# ========== 内容获取 ==========

def fetch_page_content(ws, url):
    """
    获取页面完整内容
    策略：
    1. 获取页面标题
    2. 获取meta描述
    3. 获取文章正文（更精确的选择器）
    4. 提取第一段有意义的文字
    """
    try:
        # 导航
        msg = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}})
        ws.send(msg)
        time.sleep(3)
        
        # 获取页面完整信息
        script = """
        (function() {
            var result = {
                title: document.title,
                url: window.location.href,
                description: '',
                content: '',
                publishDate: '',
                author: ''
            };
            
            // 获取 meta 描述
            var metaDesc = document.querySelector('meta[name="description"]');
            if (metaDesc) result.description = metaDesc.content;
            
            // 获取 OG 描述
            if (!result.description) {
                var ogDesc = document.querySelector('meta[property="og:description"]');
                if (ogDesc) result.description = ogDesc.content;
            }
            
            // 获取文章正文 - 尝试多种选择器
            var contentSelectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                '#content',
                '.text',
                'main',
                '.main-text'
            ];
            
            for (var i = 0; i < contentSelectors.length; i++) {
                var elem = document.querySelector(contentSelectors[i]);
                if (elem && elem.innerText.length > 200) {
                    result.content = elem.innerText;
                    break;
                }
            }
            
            // 如果没找到，尝试获取 body
            if (!result.content) {
                result.content = document.body.innerText;
            }
            
            // 获取发布日期
            var dateSelectors = [
                'time[datetime]',
                '.publish-time',
                '.pub-date',
                '.date',
                '.timestamp',
                '[class*="date"]',
                '[class*="time"]'
            ];
            
            for (var i = 0; i < dateSelectors.length; i++) {
                var elem = document.querySelector(dateSelectors[i]);
                if (elem) {
                    result.publishDate = elem.innerText || elem.getAttribute('datetime') || elem.getAttribute('content');
                    break;
                }
            }
            
            // 获取作者
            var authorSelectors = [
                '.author',
                '.writer',
                '[rel="author"]',
                '.name'
            ];
            
            for (var i = 0; i < authorSelectors.length; i++) {
                var elem = document.querySelector(authorSelectors[i]);
                if (elem && elem.innerText.length < 50) {
                    result.author = elem.innerText;
                    break;
                }
            }
            
            return JSON.stringify(result);
        })();
        """
        
        msg = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": script}})
        ws.send(msg)
        
        response = ws.recv()
        data = json.loads(response)
        
        if 'result' in data:
            content = json.loads(data['result']['result']['value'])
            return content
        
        return {}
        
    except Exception as e:
        return {}


# ========== 摘要生成 ==========

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    
    # 移除常见的无用字符
    text = text.replace('\u200b', '')  # 零宽空格
    text = text.replace('\xa0', ' ')   # 不间断空格
    
    return text.strip()


def extract_summary(content_data, max_length=300):
    """
    从内容中提取摘要
    策略：
    1. 如果有 meta 描述，使用它
    2. 否则，从正文中提取第一段有意义的文字
    3. 清理并截断到合理长度
    """
    # 优先使用 meta 描述
    description = content_data.get('description', '')
    if description and len(description) > 20:
        return clean_text(description)[:max_length]
    
    # 从正文提取
    content = content_data.get('content', '')
    if not content:
        return "暂无摘要"
    
    # 清理文本
    content = clean_text(content)
    
    # 尝试找到第一段有意义的文字
    # 分割成段落
    paragraphs = re.split(r'[\n\r]+', content)
    
    for para in paragraphs:
        para = para.strip()
        # 跳过太短的段落
        if len(para) < 50:
            continue
        # 跳过看起来像导航/菜单的段落
        if any(x in para.lower() for x in ['登录', '注册', '关注', '分享', '评论', '版权所有', '客服', '微信']):
            continue
        
        # 找到第一段有意义的
        return para[:max_length]
    
    # 如果没找到合适的，返回前200字符
    return content[:max_length]


def generate_key_points(content_data):
    """
    生成文章关键点
    策略：
    1. 从正文中提取关键句子
    2. 包含数字的句子通常是重点
    3. 包含"将"、"计划"、"发布"等动词的句子可能是重点
    """
    content = content_data.get('content', '')
    if not content or len(content) < 100:
        return []
    
    # 清理
    content = clean_text(content)
    
    # 分割成句子
    sentences = re.split(r'[。！？\n\r]+', content)
    
    key_points = []
    important_keywords = [
        '亿', '万', '千', '百分', '%',  # 数字
        '发布', '推出', '上线', '发布',  # 动作
        '首次', '首个', '第一', '首次',  # 最高级
        '增长', '下降', '突破', '超过',  # 变化
        '融资', '投资', '收购', '上市',  # 商业
        '新模型', '新版本', '新产品', '新功能',  # 新产品
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20 or len(sentence) > 200:
            continue
        
        # 检查是否包含关键词
        if any(kw in sentence for kw in important_keywords):
            key_points.append(sentence)
        
        # 如果已经找到3个关键点，就停止
        if len(key_points) >= 3:
            break
    
    # 如果不够3个，补充一些其他的句子
    if len(key_points) < 3:
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in key_points and len(sentence) > 30:
                key_points.append(sentence)
                if len(key_points) >= 3:
                    break
    
    # 去重并返回
    return list(dict.fromkeys(key_points))[:3]


def process_article(url, ws=None):
    """
    处理单篇文章，获取完整内容和摘要
    """
    if not ws:
        # 需要Chrome连接
        return None
    
    # 获取内容
    content_data = fetch_page_content(ws, url)
    
    if not content_data:
        return {
            'title': '',
            'summary': '获取内容失败',
            'key_points': [],
            'publish_date': '',
            'author': ''
        }
    
    # 生成摘要
    summary = extract_summary(content_data)
    
    # 生成关键点
    key_points = generate_key_points(content_data)
    
    return {
        'title': content_data.get('title', ''),
        'summary': summary,
        'key_points': key_points,
        'publish_date': content_data.get('publishDate', ''),
        'author': content_data.get('author', '')
    }


# ========== 测试 ==========

def test_content_fetch():
    """测试内容获取"""
    # 连接 Chrome
    try:
        resp = requests.get('http://localhost:9222/json/list', timeout=5)
        pages = resp.json()
        page = [p for p in pages if p['type'] == 'page'][0]
        ws_url = page['webSocketDebuggerUrl']
        
        ws = websocket.WebSocket()
        ws.settimeout(20)
        ws.connect(ws_url)
        
        # 测试获取
        test_urls = [
            'https://www.qbitai.com/2026/04/396535.html',
            'https://www.36kr.com/p/3751046517129735'
        ]
        
        for url in test_urls:
            print(f"\n=== 测试: {url} ===")
            result = process_article(url, ws)
            print(f"标题: {result['title'][:60]}")
            print(f"摘要: {result['summary'][:150]}...")
            print(f"关键点: {result['key_points']}")
        
        ws.close()
        
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_content_fetch()