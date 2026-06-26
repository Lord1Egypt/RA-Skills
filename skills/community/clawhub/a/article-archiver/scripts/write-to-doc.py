#!/usr/bin/env python3
"""
写入内容到飞书文档的辅助脚本
"""
import sys
import os

# 添加 OpenClaw 路径
sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.7_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.5_node-llama-cpp@3.16.2/node_modules/openclaw')

try:
    # 尝试导入 feishu_doc 工具
    from extensions.feishu.tools import feishu_doc
    
    def write_to_doc(doc_token, content, action='write'):
        """写入内容到飞书文档"""
        result = feishu_doc.execute({
            'action': action,
            'doc_token': doc_token,
            'content': content
        })
        return result.get('success', False)
    
    if __name__ == '__main__':
        if len(sys.argv) < 4:
            print("Usage: python3 write-to-doc.py <doc_token> <content_file> <action>")
            sys.exit(1)
        
        doc_token = sys.argv[1]
        content_file = sys.argv[2]
        action = sys.argv[3]  # 'write' or 'append'
        
        # 读取内容
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 写入文档
        success = write_to_doc(doc_token, content, action)
        sys.exit(0 if success else 1)

except ImportError:
    # 如果无法导入，使用 subprocess 调用 openclaw CLI
    import subprocess
    
    if __name__ == '__main__':
        if len(sys.argv) < 4:
            print("Usage: python3 write-to-doc.py <doc_token> <content_file> <action>")
            sys.exit(1)
        
        doc_token = sys.argv[1]
        content_file = sys.argv[2]
        action = sys.argv[3]
        
        # 读取内容
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转义内容
        content_escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('$', '\\$')
        
        # 调用 CLI
        cmd = f'openclaw feishu-doc {action} --doc-token "{doc_token}" --content "{content_escaped}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        sys.exit(result.returncode)
