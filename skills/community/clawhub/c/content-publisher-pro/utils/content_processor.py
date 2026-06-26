"""
内容处理器 - 解析和处理Markdown文章
"""

import re
import yaml


class ContentProcessor:
    """处理Markdown文章内容"""
    
    def parse(self, content):
        """解析Markdown文件，提取front matter和正文"""
        # 匹配YAML front matter
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            front_matter = yaml.safe_load(match.group(1))
            body = match.group(2).strip()
        else:
            front_matter = {}
            body = content.strip()
        
        return {
            'title': front_matter.get('title', 'Untitled'),
            'date': front_matter.get('date', ''),
            'tags': front_matter.get('tags', []),
            'cover_image': front_matter.get('cover_image', ''),
            'excerpt': front_matter.get('excerpt', ''),
            'body': body,
            'front_matter': front_matter
        }
    
    def generate_summary(self, article_data, ratio=0.7):
        """生成文章摘要（保留ratio比例的内容）"""
        body = article_data['body']
        lines = body.split('\n')
        
        # 计算保留的行数
        keep_lines = int(len(lines) * ratio)
        summary_lines = lines[:keep_lines]
        
        # 添加引流footer
        blog_url = "https://your-blog-url.com"
        footer = f"""

---

> 📢 **本文为精简版，完整版包含更多深度分析和独家内容，请访问 [博客]({blog_url}) 查看！**

*关注获取最新技术资讯和教程！*
"""
        
        summary_body = '\n'.join(summary_lines) + footer
        
        return {
            **article_data,
            'body': summary_body,
            'is_summary': True
        }
    
    def generate_abstract(self, article_data):
        """生成文章摘要（适合社交平台）"""
        title = article_data['title']
        excerpt = article_data.get('excerpt', '')
        
        if not excerpt:
            # 从正文提取前200字
            body = article_data['body']
            excerpt = body[:200] + '...' if len(body) > 200 else body
        
        blog_url = "https://your-blog-url.com"
        
        return {
            'title': title,
            'body': f"{excerpt}\n\n👉 阅读全文: {blog_url}",
            'tags': article_data.get('tags', []),
            'is_abstract': True
        }
