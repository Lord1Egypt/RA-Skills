#!/usr/bin/env python3
"""
CNBlogs MetaWeblog API - 保存草稿
Usage: python save_draft.py "标题" "content.md" ["分类1,分类2"]

配置环境变量：
export CNBLOGS_BLOG_URL="https://rpc.cnblogs.com/metaweblog/sueyyyy"
export CNBLOGS_USERNAME="suyang320"
export CNBLOGS_TOKEN="your-token"
"""

import sys
import os
from xmlrpc.client import ServerProxy, Fault, Transport
import ssl

# 配置
BLOG_URL = os.getenv("CNBLOGS_BLOG_URL", "https://rpc.cnblogs.com/metaweblog/sueyyyy")
USERNAME = os.getenv("CNBLOGS_USERNAME", "suyang320")
PASSWORD = os.getenv("CNBLOGS_TOKEN", "")

class CustomTransport(Transport):
    """自定义传输层，处理 SSL"""
    def __init__(self):
        super().__init__()
        self.context = ssl._create_unverified_context()
    
    def make_connection(self, host):
        import http.client
        return http.client.HTTPSConnection(host, context=self.context)

def save_draft(title, content, categories=None):
    """保存文章到博客园草稿箱"""
    
    if not PASSWORD:
        print("❌ 错误：请配置环境变量 CNBLOGS_TOKEN")
        print("\n示例：")
        print('export CNBLOGS_TOKEN="your-metaweblog-token"')
        return None
    
    try:
        server = ServerProxy(BLOG_URL, transport=CustomTransport())
        
        # 构建文章结构
        post = {
            "title": title,
            "description": content,
            "categories": categories or ["[随笔分类]"],
            "mt_keywords": "",
        }
        
        print(f"正在保存文章: {title}")
        
        # 调用 newPost 方法（publish=False 表示保存为草稿）
        post_id = server.metaWeblog.newPost(
            "422078",  # blogid
            USERNAME,
            PASSWORD,
            post,
            False  # False = 草稿，True = 直接发布
        )
        
        print(f"✅ 草稿保存成功！")
        print(f"   文章 ID: {post_id}")
        print(f"   标题: {title}")
        print(f"   分类: {', '.join(categories) if categories else '[随笔分类]'}")
        print(f"\n   编辑链接: https://i.cnblogs.com/posts/edit;postId={post_id}")
        
        return post_id
        
    except Fault as e:
        print(f"❌ API 错误: {e.faultCode} - {e.faultString}")
        return None
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("用法: python save_draft.py \"文章标题\" \"content.md\" [\"分类1,分类2\"]")
        print("\n示例:")
        print('  python save_draft.py "我的第一篇博客" "./article.md"')
        print('  python save_draft.py "技术文章" "./tech.md" "Java,Spring"')
        sys.exit(1)
    
    title = sys.argv[1]
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
    
    # 保存草稿
    post_id = save_draft(title, content, categories)
    
    if post_id:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
