#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档上传脚本 - 上传蓝源军规.pdf到企业知识库

使用方法:
python upload_document.py
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    print("=" * 60)
    print("📚 企业知识库 - 文档上传工具")
    print("=" * 60)
    
    try:
        # 设置API密钥
        print("1️⃣  设置API密钥...")
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("   ❌ 未设置 DASHSCOPE_API_KEY 环境变量")
            print("   请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
            return
        print(f"   ✓ DashScope API密钥已设置: {api_key[:10]}...")
        
        # 导入模块
        print("2️⃣  导入模块...")
        from src import load_config, DocumentProcessor
        print("   ✓ 模块导入成功")
        
        # 加载配置
        print("3️⃣  加载配置...")
        config = load_config()
        print(f"   ✓ 嵌入模型: {config.embedding_model}")
        print(f"   ✓ 提供商: {config.embedding_provider}")
        print(f"   ✓ 数据库路径: 系统自动配置")
        print(f"   ✓ API密钥: {config.embedding_api_key[:10] if config.embedding_api_key else '未设置'}...")
        
        # 检查PDF文件
        print("4️⃣  检查PDF文件...")
        # 查找工作区根目录下的PDF文件
        workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(workspace_root, "蓝源军规.pdf")
        if not os.path.exists(pdf_path):
            print(f"   ❌ 文件不存在: {pdf_path}")
            print("   💡 请将PDF文件放在工作区根目录下")
            return
        
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
        print(f"   ✓ 找到文件: 蓝源军规.pdf ({file_size:.2f} MB)")
        
        # 初始化文档处理器
        print("5️⃣  初始化文档处理器...")
        processor = DocumentProcessor(config)
        print("   ✓ 文档处理器就绪")
        
        # 处理PDF文档
        print("6️⃣  开始处理文档...")
        print("   📄 正在解析PDF...")
        print("   ✂️  正在分块...")
        print("   🔢 正在生成嵌入向量...")
        print("   💾 正在存储到向量数据库...")
        
        result = processor.process_document(pdf_path, "蓝源军规")
        
        if result.success:
            print("\n" + "=" * 60)
            print("✅ 文档上传成功！")
            print("=" * 60)
            print(f"📄 文档名称: {result.document_name}")
            print(f"🆔 文档ID: {result.document_id}")
            print(f"📊 创建块数: {result.chunk_count}")
            print(f"💬 状态信息: {result.message}")
            
            # 显示使用提示
            print("\n📖 使用方法:")
            print("现在你可以向知识库提问，例如:")
            print("- 蓝源的核心价值观是什么？")
            print("- 蓝源的安全规定有哪些？")
            print("- 蓝源员工行为准则是什么？")
            
        else:
            print("\n" + "=" * 60)
            print("❌ 文档上传失败")
            print("=" * 60)
            print(f"错误信息: {result.error}")
            
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()