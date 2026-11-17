"""
测试知识库模块
"""
import json
import os
import sys

# 添加当前目录到path以便导入knowledge_base
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from knowledge_base import KnowledgeBase


def test_local_file(file_path):
    """测试本地文件数据源"""
    print("=" * 60)
    print("测试 1: 本地文件数据源")
    print("=" * 60)
    
    config = {
        "source_type": "local",
        "source_config": {
            "file_path": file_path
        }
    }
    
    try:
        kb = KnowledgeBase(config)
        print(f"✅ KnowledgeBase 初始化成功")
        print(f"   数据源类型: {kb.source_type}")
        print(f"   文件路径: {file_path}")
        
        # 测试读取所有数据
        print("\n📖 测试 get_all() 方法...")
        all_data = kb.get_all()
        print(f"✅ 成功读取 {len(all_data)} 条数据")
        
        if len(all_data) > 0:
            print(f"\n📋 第一条数据结构示例:")
            first_row = all_data[0]
            for key, value in list(first_row.items())[:5]:
                print(f"   {key}: {value}")
            if len(first_row) > 5:
                print(f"   ... (共 {len(first_row)} 个字段)")
        
        # 测试查询
        print("\n🔍 测试 query() 方法...")
        if len(all_data) > 0:
            # 使用第一个字段的值作为查询关键词
            first_key = list(first_row.keys())[0]
            first_value = str(first_row[first_key])
            if first_value:
                results = kb.query(first_value)
                print(f"✅ 查询 '{first_value}' 返回 {len(results)} 条结果")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ 文件不存在: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_knowledge_base_config():
    """测试从配置文件加载"""
    print("\n" + "=" * 60)
    print("测试 2: 从配置文件加载")
    print("=" * 60)
    
    config_file = "knowledge_base_config.json"
    
    if not os.path.exists(config_file):
        print(f"⚠️  配置文件不存在: {config_file}")
        print(f"   请先创建配置文件（参考 knowledge_base_config.example.json）")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ 配置文件读取成功")
        print(f"   数据源类型: {config.get('source_type')}")
        print(f"   配置: {config.get('source_config')}")
        
        kb = KnowledgeBase(config)
        print(f"✅ KnowledgeBase 初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ima_source():
    """测试 IMA 知识库数据源（仅检查配置）"""
    print("\n" + "=" * 60)
    print("测试 3: IMA 知识库数据源（配置检查）")
    print("=" * 60)
    
    config = {
        "source_type": "ima",
        "source_config": {
            "kb_id": "test-kb-id"
        }
    }
    
    try:
        kb = KnowledgeBase(config)
        print(f"✅ KnowledgeBase 初始化成功")
        print(f"   数据源类型: {kb.source_type}")
        print(f"   KB ID: {kb.source_config.get('kb_id')}")
        
        # 注意：实际查询需要调用 MCP 工具
        print(f"\n⚠️  注意: IMA 数据源的 query() 方法需要 MCP 工具支持")
        print(f"   在实际使用中，AI 会调用 IMA MCP 工具执行查询")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_tencent_docs_source():
    """测试腾讯文档数据源（仅检查配置）"""
    print("\n" + "=" * 60)
    print("测试 4: 腾讯文档数据源（配置检查）")
    print("=" * 60)
    
    config = {
        "source_type": "tencent_docs",
        "source_config": {
            "doc_id": "test-doc-id"
        }
    }
    
    try:
        kb = KnowledgeBase(config)
        print(f"✅ KnowledgeBase 初始化成功")
        print(f"   数据源类型: {kb.source_type}")
        print(f"   Doc ID: {kb.source_config.get('doc_id')}")
        
        # 注意：实际查询需要调用 MCP 工具
        print(f"\n⚠️  注意: 腾讯文档数据源的 query() 方法需要 MCP 工具支持")
        print(f"   在实际使用中，AI 会调用腾讯文档 MCP 工具执行查询")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "🧪 " * 15)
    print("知识库模块测试")
    print("🧪 " * 15 + "\n")
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        test_local_file(file_path)
    else:
        # 自动查找当前目录下的 Excel 文件
        print("未提供文件路径，自动查找当前目录下的 Excel 文件...\n")
        excel_files = []
        for file in os.listdir('.'):
            if file.endswith(('.xlsx', '.xls')):
                excel_files.append(file)
        
        if len(excel_files) > 0:
            print(f"找到 {len(excel_files)} 个 Excel 文件:")
            for i, f in enumerate(excel_files):
                print(f"  {i+1}. {f}")
            
            # 使用第一个文件进行测试
            test_local_file(excel_files[0])
        else:
            print("⚠️  未找到 Excel 文件")
            print("   请提供文件路径: python test_knowledge_base.py <path/to/file.xlsx>")
    
    # 测试配置文件加载
    test_knowledge_base_config()
    
    # 测试 IMA 数据源（配置检查）
    test_ima_source()
    
    # 测试腾讯文档数据源（配置检查）
    test_tencent_docs_source()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
