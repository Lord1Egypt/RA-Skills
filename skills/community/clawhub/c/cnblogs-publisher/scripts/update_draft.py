#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 更新草稿
Usage: python update_draft.py <post-id> "content.md" ["分类1,分类2"]
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

def update_draft(post_id, title, content, categories=None):
    """更新博客园草稿"""
    
    if not PASSWORD:
        print("❌ 错误：请配置环境变量 CNBLOGS_TOKEN")
        return False
    
    try:
        server = ServerProxy(BLOG_URL, transport=CustomTransport())
        
        # 构建文章结构
        post = {
            "title": title,
            "description": content,
            "categories": categories or ["[随笔分类]"],
            "mt_keywords": "",
        }
        
        print(f"正在更新文章 ID: {post_id}")
        print(f"标题: {title}")
        
        # 调用 editPost 方法
        result = server.metaWeblog.editPost(
            post_id,
            USERNAME,
            PASSWORD,
            post,
            False  # False = 保持草稿状态
        )
        
        if result:
            print(f"✅ 草稿更新成功！")
            print(f"   文章 ID: {post_id}")
            print(f"   编辑链接: https://i.cnblogs.com/posts/edit;postId={post_id}")
            return True
        else:
            print(f"❌ 更新失败")
            return False
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
        return False
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("用法: python update_draft.py <post-id> \"content.md\" [\"分类1,分类2\"]")
        print("\n示例:")
        print('  python update_draft.py 12345 "./updated.md"')
        print('  python update_draft.py 12345 "./tech.md" "Java,Spring"')
        sys.exit(1)
    
    post_id = sys.argv[1]
    content_file = sys.argv[2]
    categories = None
    
    if len(sys.argv) > 3:
        categories = [c.strip() for c in sys.argv[3].split(",")]
    
    # 读取内容文件
    if not os.path.exists(content_file):
        print(f"❌ 文件不存在: {content_file}")
        sys.exit(1)
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从内容中提取标题（第一行 # 标题）
    title = None
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    if not title:
        title = f"更新于 {os.path.basename(content_file)}"
    
    # 更新草稿
    success = update_draft(post_id, title, content, categories)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
