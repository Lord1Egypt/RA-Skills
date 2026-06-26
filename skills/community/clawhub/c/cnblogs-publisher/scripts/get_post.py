#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 获取单篇文章
Usage: python get_post.py <post-id>
"""

import sys
import os
from xmlrpc.client import ServerProxy, Fault, Transport
import ssl

BLOG_URL = os.getenv("CNBLOGS_BLOG_URL", "https://rpc.cnblogs.com/metaweblog/sueyyyy")
USERNAME = os.getenv("CNBLOGS_USERNAME", "suyang320")
PASSWORD = os.getenv("CNBLOGS_TOKEN", "")

class CustomTransport(Transport):
    def __init__(self):
        super().__init__()
        self.context = ssl._create_unverified_context()
    
    def make_connection(self, host):
        import http.client
        return http.client.HTTPSConnection(host, context=self.context)

def get_post(post_id):
    """获取单篇文章详情"""
    
    if not PASSWORD:
        print("❌ 错误：请配置环境变量 CNBLOGS_TOKEN")
        return None
    
    try:
        server = ServerProxy(BLOG_URL, transport=CustomTransport())
        
        print(f"正在获取文章 ID: {post_id}")
        post = server.metaWeblog.getPost(post_id, USERNAME, PASSWORD)
        
        if not post:
            print(f"❌ 文章不存在: {post_id}")
            return None
        
        print(f"\n📄 文章详情:")
        print(f"   标题: {post.get('title', '无标题')}")
        print(f"   ID: {post.get('postid', 'N/A')}")
        print(f"   链接: {post.get('link', 'N/A')}")
        print(f"   分类: {', '.join(post.get('categories', []))}")
        print(f"   关键词: {post.get('mt_keywords', 'N/A')}")
        
        date = post.get('dateCreated', '未知')
        if hasattr(date, 'value'):
            date_str = date.value
        else:
            date_str = str(date)
        print(f"   创建时间: {date_str}")
        
        # 内容预览（前200字符）
        content = post.get('description', '')
        preview = content[:200].replace('\n', ' ')
        print(f"\n   内容预览:")
        print(f"   {preview}...")
        
        return post
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
        return None
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python get_post.py <post-id>")
        print("\n示例:")
        print('  python get_post.py 12345')
        sys.exit(1)
    
    post_id = sys.argv[1]
    
    # 获取文章
    post = get_post(post_id)
    
    sys.exit(0 if post else 1)

if __name__ == "__main__":
    main()
