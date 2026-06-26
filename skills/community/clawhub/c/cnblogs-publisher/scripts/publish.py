#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 发布文章
Usage: python publish.py <post-id>
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

def publish_post(post_id):
    """发布博客园文章"""
    
    if not PASSWORD:
        print("❌ 错误：请配置环境变量 CNBLOGS_TOKEN")
        return False
    
    try:
        server = ServerProxy(BLOG_URL, transport=CustomTransport())
        
        # 先获取文章信息
        print(f"正在获取文章信息 ID: {post_id}")
        post = server.metaWeblog.getPost(post_id, USERNAME, PASSWORD)
        
        if not post:
            print(f"❌ 文章不存在: {post_id}")
            return False
        
        title = post.get('title', '无标题')
        print(f"标题: {title}")
        
        # 更新文章为发布状态
        print(f"正在发布文章...")
        
        # 构建文章结构（保持原有内容）
        updated_post = {
            "title": post.get('title', ''),
            "description": post.get('description', ''),
            "categories": post.get('categories', ['[随笔分类]']),
            "mt_keywords": post.get('mt_keywords', ''),
        }
        
        # 调用 editPost，publish=True
        result = server.metaWeblog.editPost(
            post_id,
            USERNAME,
            PASSWORD,
            updated_post,
            True  # True = 发布
        )
        
        if result:
            print(f"✅ 文章发布成功！")
            print(f"   文章 ID: {post_id}")
            print(f"   标题: {title}")
            print(f"   访问链接: {post.get('link', f'https://www.cnblogs.com/sueyyyy/p/{post_id}.html')}")
            return True
        else:
            print(f"❌ 发布失败")
            return False
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
        return False
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python publish.py <post-id>")
        print("\n示例:")
        print('  python publish.py 12345')
        sys.exit(1)
    
    post_id = sys.argv[1]
    
    # 发布文章
    success = publish_post(post_id)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
