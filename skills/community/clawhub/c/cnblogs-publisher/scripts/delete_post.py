#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 删除文章
Usage: python delete_post.py <post-id>
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

def delete_post(post_id):
    """删除博客园文章"""
    
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
        
        # 确认删除
        confirm = input(f"\n⚠️  确认删除文章 \"{title}\"? (yes/no): ")
        if confirm.lower() != 'yes':
            print("已取消删除")
            return False
        
        # 调用 blogger.deletePost
        print(f"正在删除文章...")
        result = server.blogger.deletePost(
            "",  # appKey（博客园忽略）
            post_id,
            USERNAME,
            PASSWORD,
            True  # publish（删除时设为 True）
        )
        
        if result:
            print(f"✅ 文章删除成功！")
            return True
        else:
            print(f"❌ 删除失败")
            return False
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
        return False
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python delete_post.py <post-id>")
        print("\n示例:")
        print('  python delete_post.py 12345')
        sys.exit(1)
    
    post_id = sys.argv[1]
    
    # 删除文章
    success = delete_post(post_id)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
