#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 获取博客信息
Usage: python get_blog_info.py
"""

import os
from xmlrpc.client import ServerProxy, Fault, Transport
import ssl

# 配置
BLOG_URL = os.getenv("CNBLOGS_BLOG_URL", "")
USERNAME = os.getenv("CNBLOGS_USERNAME", "")
PASSWORD = os.getenv("CNBLOGS_TOKEN", "")

class CustomTransport(Transport):
    """自定义传输层"""
    def __init__(self):
        super().__init__()
        self.context = ssl._create_unverified_context()
    
    def make_connection(self, host):
        import http.client
        return http.client.HTTPSConnection(host, context=self.context)

def get_blog_info():
    """获取博客信息"""
    
    if not all([BLOG_URL, USERNAME, PASSWORD]):
        print("❌ 错误：请配置环境变量")
        print(f"   CNBLOGS_BLOG_URL={BLOG_URL}")
        print(f"   CNBLOGS_USERNAME={USERNAME}")
        print(f"   CNBLOGS_TOKEN={'*' * len(PASSWORD) if PASSWORD else '未设置'}")
        return
    
    print(f"尝试连接: {BLOG_URL}")
    print(f"用户名: {USERNAME}")
    print(f"令牌: {'*' * 10}...")
    print()
    
    try:
        server = ServerProxy(BLOG_URL, transport=CustomTransport())
        
        # 尝试获取博客列表
        print("1. 尝试获取用户博客列表...")
        try:
            blogs = server.blogger.getUsersBlogs("", USERNAME, PASSWORD)
            print(f"   ✅ 成功！找到 {len(blogs)} 个博客")
            for blog in blogs:
                print(f"      - {blog.get('blogName', 'N/A')} (ID: {blog.get('blogid', 'N/A')})")
                print(f"        URL: {blog.get('url', 'N/A')}")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
        
        # 尝试获取分类列表
        print("\n2. 尝试获取分类列表...")
        try:
            categories = server.metaWeblog.getCategories("", USERNAME, PASSWORD)
            print(f"   ✅ 成功！找到 {len(categories)} 个分类")
            for cat in categories[:5]:  # 只显示前5个
                print(f"      - {cat.get('title', 'N/A')}")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
        
        # 尝试获取最近文章
        print("\n3. 尝试获取最近文章...")
        try:
            posts = server.metaWeblog.getRecentPosts("", USERNAME, PASSWORD, 5)
            print(f"   ✅ 成功！找到 {len(posts)} 篇文章")
            for post in posts:
                print(f"      - {post.get('title', '无标题')} (ID: {post.get('postid', 'N/A')})")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
        
    except Exception as e:
        print(f"❌ 连接错误: {type(e).__name__}: {e}")

def test_different_urls():
    """测试不同的 API URL 格式"""
    urls = [
        "https://rpc.cnblogs.com/metaweblog/suyang320",
        "https://www.cnblogs.com/suyang320/services/metaweblog.aspx",
        "https://www.cnblogs.com/suyang320/services/metablogapi.aspx",
    ]
    
    print("测试不同的 API URL 格式:\n")
    
    for url in urls:
        print(f"测试: {url}")
        try:
            server = ServerProxy(url, transport=CustomTransport())
            blogs = server.blogger.getUsersBlogs("", USERNAME, PASSWORD)
            print(f"   ✅ 成功！找到 {len(blogs)} 个博客")
            break
        except Exception as e:
            print(f"   ❌ 失败: {type(e).__name__}")
        print()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test-urls":
        test_different_urls()
    else:
        get_blog_info()
