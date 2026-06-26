#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 获取草稿列表
Usage: python list_drafts.py
"""

import os
from xmlrpc.client import ServerProxy, Fault

# 配置
BLOG_URL = os.getenv("CNBLOGS_BLOG_URL", "")
USERNAME = os.getenv("CNBLOGS_USERNAME", "")
PASSWORD = os.getenv("CNBLOGS_TOKEN", "")

def list_recent_posts(num_posts=20):
    """获取最近的文章列表（包括草稿）"""
    
    if not all([BLOG_URL, USERNAME, PASSWORD]):
        print("❌ 错误：请配置环境变量 CNBLOGS_BLOG_URL, CNBLOGS_USERNAME, CNBLOGS_TOKEN")
        return
    
    try:
        server = ServerProxy(BLOG_URL)
        
        # 获取最近文章
        posts = server.metaWeblog.getRecentPosts(
            "",  # blogid
            USERNAME,
            PASSWORD,
            num_posts
        )
        
        if not posts:
            print("📭 没有找到文章")
            return
        
        print(f"📋 最近 {len(posts)} 篇文章:\n")
        print("-" * 80)
        
        for post in posts:
            post_id = post.get("postid", "N/A")
            title = post.get("title", "无标题")
            date = post.get("dateCreated", "未知时间")
            categories = post.get("categories", [])
            
            # 格式化日期
            if hasattr(date, 'value'):
                date_str = date.value
            else:
                date_str = str(date)
            
            print(f"\n📝 {title}")
            print(f"   ID: {post_id}")
            print(f"   时间: {date_str}")
            print(f"   分类: {', '.join(categories) if categories else '无'}")
            print(f"   编辑: https://i.cnblogs.com/posts/edit;postId={post_id}")
        
        print("\n" + "-" * 80)
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
    except Exception as e:
        print(f"❌ 错误: {e}")

def main():
    list_recent_posts()

if __name__ == "__main__":
    main()
