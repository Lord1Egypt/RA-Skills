"""
GitHub发布模块 - 发布到GitHub Pages博客
"""

import requests
import base64
import json
from datetime import datetime


class GitHubPublisher:
    """GitHub Pages博客发布器"""
    
    def __init__(self, config):
        self.token = config['token']
        self.repo = config['repo']
        self.api_base = "https://api.github.com"
    
    def _make_request(self, method, endpoint, data=None):
        """发送GitHub API请求"""
        url = f"{self.api_base}{endpoint}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
        
        return response
    
    def _generate_slug(self, title):
        """生成URL友好的slug"""
        import re
        slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title.lower())
        slug = slug.strip('-')
        return slug[:50]
    
    def _build_jekyll_post(self, article_data):
        """构建Jekyll格式的博客文章"""
        title = article_data['title']
        date = article_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        tags = article_data.get('tags', [])
        cover = article_data.get('cover_image', '')
        body = article_data['body']
        
        # 构建front matter
        front_matter = {
            'title': title,
            'date': date,
            'categories': ['技术'],
            'tags': tags
        }
        
        if cover:
            front_matter['cover_image'] = cover
        
        # 转换为YAML格式
        import yaml
        fm_yaml = yaml.dump(front_matter, allow_unicode=True, default_flow_style=False)
        
        # 构建完整文章
        post_content = f"---\n{fm_yaml}---\n\n{body}"
        
        return post_content
    
    def publish(self, article_data, mode='full'):
        """发布文章到GitHub Pages"""
        # 生成文件名
        date = datetime.now().strftime('%Y-%m-%d')
        slug = self._generate_slug(article_data['title'])
        filename = f"_posts/{date}-{slug}.md"
        
        # 构建文章内容
        post_content = self._build_jekyll_post(article_data)
        
        # 检查文件是否已存在
        check_response = self._make_request("GET", f"/repos/{self.repo}/contents/{filename}")
        
        sha = None
        if check_response.status_code == 200:
            # 文件已存在，获取SHA
            sha = check_response.json().get('sha')
            print(f"⚠️  文件已存在，将更新: {filename}")
        
        # 准备提交数据
        commit_message = f"Add post: {article_data['title']}"
        content_encoded = base64.b64encode(post_content.encode('utf-8')).decode('utf-8')
        
        data = {
            "message": commit_message,
            "content": content_encoded
        }
        
        if sha:
            data["sha"] = sha
        
        # 提交到GitHub
        response = self._make_request("PUT", f"/repos/{self.repo}/contents/{filename}", data)
        
        if response.status_code in [200, 201]:
            # 构建文章URL
            username = self.repo.split('/')[0]
            url = f"https://{username}.github.io/{date}/{slug}/"
            return url
        else:
            raise Exception(f"GitHub API错误: {response.status_code} - {response.text}")
    
    def check_duplicate(self, title):
        """检查是否已存在相同标题的文章"""
        slug = self._generate_slug(title)
        date_prefix = datetime.now().strftime('%Y-%m-%d')
        
        # 获取_posts目录下的文件列表
        response = self._make_request("GET", f"/repos/{self.repo}/contents/_posts")
        
        if response.status_code == 200:
            files = response.json()
            for file in files:
                if slug in file['name'].lower():
                    return True
        
        return False
