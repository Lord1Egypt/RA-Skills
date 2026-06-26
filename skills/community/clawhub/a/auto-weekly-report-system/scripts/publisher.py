#!/usr/bin/env python3
"""
发布器 - 将周报发布到企业微信文档
"""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path

class WeComPublisher:
    def __init__(self):
        self.report_file = "/tmp/weekly_report_auto.md"
    
    def read_report(self):
        """读取生成的报告"""
        try:
            with open(self.report_file, 'r') as f:
                return f.read()
        except:
            return None
    
    def publish(self, title=None):
        """发布到企业微信"""
        title = title or f"MoltbookAgent 周报 {datetime.now().strftime('%Y-%m-%d')}"
        content = self.read_report()
        
        if not content:
            print("❌ 未找到报告文件，先运行 generator.py")
            return False
        
        print(f"📤 准备发布到企业微信")
        print(f"   标题: {title}")
        print(f"   内容长度: {len(content)} 字符")
        
        # 由于 wecom_mcp 需要实际调用，这里生成命令供用户执行
        print("\n" + "="*60)
        print("请执行以下命令完成发布:")
        print("="*60)
        
        print(f"""
# 步骤 1: 创建文档
wecom_mcp call doc create_doc '{{"doc_type": 3, "doc_name": "{title}"}}'

# 步骤 2: 从返回结果中获取 docid，然后编辑内容
# (将下面的 DOCID 替换为实际返回的 docid)
wecom_mcp call doc edit_doc_content '{{"docid": "DOCID", "content": {repr(content)}, "content_type": 1}}'
""")
        
        print("="*60)
        
        # 同时保存命令到文件方便执行
        cmd_file = "/tmp/publish_commands.sh"
        with open(cmd_file, 'w') as f:
            f.write(f"""#!/bin/bash
# 企业微信文档发布命令
# 生成时间: {datetime.now().isoformat()}

echo "步骤 1: 创建文档..."
wecom_mcp call doc create_doc '{{"doc_type": 3, "doc_name": "{title}"}}'

echo ""
echo "步骤 2: 请复制上面返回的 docid，然后执行:"
echo "wecom_mcp call doc edit_doc_content '{{\"docid\": \"YOUR_DOCID\", \"content\": \"...\", \"content_type\": 1}}'"
""")
        
        print(f"\n💾 命令已保存到: {cmd_file}")
        print(f"   执行: bash {cmd_file}")
        
        return True
    
    def publish_simulation(self, title=None):
        """模拟发布（用于测试）"""
        title = title or f"MoltbookAgent 周报 {datetime.now().strftime('%Y-%m-%d')}"
        content = self.read_report()
        
        if not content:
            print("❌ 未找到报告文件")
            return False
        
        print(f"\n{'='*60}")
        print(f"📄 模拟发布: {title}")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}")
        print(f"✅ 报告已生成（模拟模式）")
        print(f"   实际发布请使用: python3 publisher.py --title \"{title}\"")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="周报发布器")
    parser.add_argument("--title", help="文档标题")
    parser.add_argument("--dry-run", action="store_true", help="模拟发布（不实际调用API）")
    
    args = parser.parse_args()
    
    publisher = WeComPublisher()
    
    if args.dry_run:
        publisher.publish_simulation(args.title)
    else:
        publisher.publish(args.title)

if __name__ == "__main__":
    main()
