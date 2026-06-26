#!/usr/bin/env python3
"""
上传图片到飞书文档的辅助脚本
"""
import sys
import os

# 添加 OpenClaw 路径
sys.path.insert(0, '/root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.7_@napi-rs+canvas@0.1.96_@types+express@5.0.6_hono@4.12.5_node-llama-cpp@3.16.2/node_modules/openclaw')

try:
    # 尝试导入 feishu_doc 工具
    from extensions.feishu.tools import feishu_doc
    
    def upload_image(doc_token, image_path):
        """上传图片到飞书文档"""
        result = feishu_doc.execute({
            'action': 'upload_image',
            'doc_token': doc_token,
            'file_path': image_path
        })
        return result.get('success', False)
    
    if __name__ == '__main__':
        if len(sys.argv) < 3:
            print("Usage: python3 upload-image.py <doc_token> <image_path>")
            sys.exit(1)
        
        doc_token = sys.argv[1]
        image_path = sys.argv[2]
        
        # 上传图片
        success = upload_image(doc_token, image_path)
        sys.exit(0 if success else 1)

except ImportError:
    # 如果无法导入，使用 subprocess 调用 openclaw CLI
    import subprocess
    
    if __name__ == '__main__':
        if len(sys.argv) < 3:
            print("Usage: python3 upload-image.py <doc_token> <image_path>")
            sys.exit(1)
        
        doc_token = sys.argv[1]
        image_path = sys.argv[2]
        
        # 调用 CLI
        cmd = f'openclaw feishu-doc upload-image --doc-token "{doc_token}" --file-path "{image_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        sys.exit(result.returncode)
