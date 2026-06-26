"""
Dev.to发布模块 - 发布到Dev.to开发者社区
"""

import requests
import json


class DevToPublisher:
    """Dev.to发布器"""
    
    def __init__(self, config):
        self.api_key = config['api_key']
        self.api_base = "https://dev.to/api"
    
    def _make_request(self, method, endpoint, data=None):
        """发送Dev.to API请求"""
        url = f"{self.api_base}{endpoint}"
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
        
        return response
    
    def check_duplicate(self, title):
        """检查是否已存在相同标题的文章"""
        response = self._make_request("GET", "/articles/me?per_page=100")
        
        if response.status_code == 200:
            articles = response.json()
            for article in articles:
                if article['title'].lower() == title.lower():
                    return True, article['id']
        
        return False, None
    
    def _build_markdown(self, article_data):
        """构建Dev.to格式的markdown"""
        title = article_data['title']
        body = article_data['body']
        tags = article_data.get('tags', [])
        cover = article_data.get('cover_image', '')
        
        # 构建front matter
        front_matter = f"""---
title: "{title}"
published: true
"""
        
        if tags:
            tags_str = json.dumps(tags, ensure_ascii=False)
            front_matter += f"tags: {tags_str}\n"
        
        if cover:
            front_matter += f"cover_image: {cover}\n"
        
        front_matter += "---\n\n"
        
        return front_matter + body
    
    def publish(self, article_data, mode='summary'):
        """发布文章到Dev.to"""
        # 检查重复
        is_dup, existing_id = self.check_duplicate(article_data['title'])
        if is_dup:
            raise Exception(f"文章已存在 (ID: {existing_id})")
        
        # 构建markdown
        markdown = self._build_markdown(article_data)
        
        # 准备发布数据
        data = {
            "article": {
                "body_markdown": markdown,
                "published": True
            }
        }
        
        # 发布
        response = self._make_request("POST", "/articles", data)
        
        if response.status_code == 201:
            result = response.json()
            return result['url']
        else:
            raise Exception(f"Dev.to API错误: {response.status_code} - {response.text}")
