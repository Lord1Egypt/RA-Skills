#!/usr/bin/env python3
"""
安装测试脚本 - 测试智能写书技能的所有组件
"""

import os
import sys
import importlib
import json
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"🔍 {text}")
    print("=" * 60)

def print_result(name, status, details=""):
    """打印测试结果"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {name}: {'通过' if status else '失败'}")
    if details:
        print(f"   详情: {details}")

def test_python_version():
    """测试Python版本"""
    print_header("测试Python版本")

    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    # 检查是否满足最低要求
    min_version = (3, 8)
    is_ok = (version.major > min_version[0]) or \
            (version.major == min_version[0] and version.minor >= min_version[1])

    print_result("Python版本", is_ok,
                 f"需要Python {min_version[0]}.{min_version[1]}+")
    return is_ok

def test_dependencies():
    """测试依赖包"""
    print_header("测试依赖包")

    dependencies = [
        ("openai", ">=1.0.0"),
        ("requests", ">=2.28.0"),
        ("yaml", ">=6.0"),  # PyYAML的模块名是yaml
        ("tiktoken", ">=0.3.0"),
    ]

    all_ok = True
    for package, required_version in dependencies:
        try:
            module = importlib.import_module(package)
            version = getattr(module, "__version__", "未知")
            print_result(f"{package}", True, f"版本: {version}")
        except ImportError as e:
            print_result(f"{package}", False, f"未安装: {e}")
            all_ok = False

    return all_ok

def test_api_keys():
    """测试API密钥"""
    print_header("测试API密钥环境变量")

    api_keys = [
        ("OPENAI_API_KEY", "OpenAI API密钥"),
        ("GOOGLE_CSE_ID", "Google自定义搜索引擎ID"),
        ("GOOGLE_API_KEY", "Google API密钥")
    ]

    available_keys = []
    for key, description in api_keys:
        value = os.environ.get(key)
        if value:
            masked_value = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print_result(description, True, f"已设置 ({masked_value})")
            available_keys.append(key)
        else:
            print_result(description, False, "未设置")

    if available_keys:
        print(f"\n📋 可用的API服务: {len(available_keys)}/{len(api_keys)}")
        return True
    else:
        print(f"\n⚠️  警告: 未设置任何API密钥，将使用模拟模式")
        return True  # 仍然返回True，因为模拟模式可用

def test_skill_modules():
    """测试技能模块"""
    print_header("测试技能模块")

    # 添加当前目录到Python路径
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    modules_to_test = [
        "scripts.book_writer",
        "scripts.content_optimizer",
        "scripts.material_searcher",
        "scripts.install_dependencies"
    ]

    all_ok = True
    for module_path in modules_to_test:
        try:
            module = importlib.import_module(module_path)
            print_result(module_path, True, "加载成功")
        except Exception as e:
            print_result(module_path, False, f"加载失败: {e}")
            all_ok = False

    return all_ok

def test_directory_structure():
    """测试目录结构"""
    print_header("测试目录结构")

    required_dirs = [
        "scripts",
        "assets/templates",
        "generated_books",
        "temp_files",
        "logs"
    ]

    required_files = [
        "SKILL.md",
        "config.yaml",
        "scripts/book_writer.py",
        "scripts/content_optimizer.py",
        "scripts/material_searcher.py",
        "scripts/install_dependencies.py"
    ]

    all_ok = True

    # 检查目录
    for directory in required_dirs:
        if Path(directory).exists():
            print_result(f"目录: {directory}", True)
        else:
            print_result(f"目录: {directory}", False, "不存在")
            all_ok = False

    # 检查文件
    for file_path in required_files:
        if Path(file_path).exists():
            print_result(f"文件: {file_path}", True)
        else:
            print_result(f"文件: {file_path}", False, "不存在")
            all_ok = False

    return all_ok

def test_book_writer():
    """测试书籍生成器"""
    print_header("测试书籍生成器（模拟模式）")

    try:
        from scripts.book_writer import BookWriter

        # 创建生成器
        writer = BookWriter()

        # 测试大纲生成（模拟模式）
        print("   正在测试大纲生成...")
        outline = writer.generate_outline("人工智能导论", max_chapters=3)
        
        print(f"   书籍标题: {outline.title}")
        print(f"   章节数量: {len(outline.chapters)}")
        
        if len(outline.chapters) > 0:
            print(f"   第一章: {outline.chapters[0]['title']}")
            print_result("大纲生成", True, f"成功生成{len(outline.chapters)}章")
        else:
            print_result("大纲生成", False, "未生成任何章节")
            return False

        # 测试章节扩写（模拟模式）
        print("   正在测试章节扩写...")
        if len(outline.chapters) > 0:
            chapter = writer.expand_chapter(outline.chapters[0], 1)
            print(f"   章节标题: {chapter.title}")
            print(f"   内容长度: {len(chapter.content)} 字符")
            print_result("章节扩写", True, "成功扩写章节内容")
        else:
            print_result("章节扩写", False, "没有章节可供扩写")
            return False

        return True

    except Exception as e:
        print_result("书籍生成器", False, f"错误: {e}")
        return False

def test_content_optimizer():
    """测试内容优化器"""
    print_header("测试内容优化器")

    try:
        from scripts.content_optimizer import ContentOptimizer
        
        optimizer = ContentOptimizer()
        
        test_content = """
        # 第一章 引言
        本章将介绍相关内容.这是第一段内容.这是第二句话。
        - 列表项1
        - 列表项2
        代码块如下:
        ```
        print("Hello, world!")
        ```
        这里有一个公式 $E=mc^2$ 和另一个 $$\\int_0^\\infty e^{-x^2} dx$$
        """
        
        optimized = optimizer.optimize_content(test_content)
        quality = optimizer.validate_content_quality(optimized)
        
        print(f"   原始字符数: {len(test_content)}")
        print(f"   优化后字符数: {len(optimized)}")
        print(f"   句子数: {quality['sentence_count']}")
        print(f"   段落数: {quality['paragraph_count']}")
        print(f"   可读性分数: {quality['readability_score']}")
        
        print_result("内容优化器", True, "功能正常")
        return True
    except Exception as e:
        print_result("内容优化器", False, f"错误: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print_header("生成测试报告")

    tests = [
        ("Python版本", test_python_version()),
        ("依赖包", test_dependencies()),
        ("API密钥", test_api_keys()),
        ("技能模块", test_skill_modules()),
        ("目录结构", test_directory_structure()),
        ("内容优化器", test_content_optimizer()),
        ("书籍生成器", test_book_writer()),
    ]

    # 统计结果
    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    print_header("测试总结")
    print(f"📊 总计测试: {total} 项")
    print(f"✅ 通过: {passed} 项")
    print(f"❌ 失败: {total - passed} 项")
    print(f"📈 通过率: {(passed/total)*100:.1f}%")

    if passed == total:
        print("\n🎉 所有测试通过！技能已准备好使用。")
        print("\n💡 使用示例:")
        print("   1. python scripts/book_writer.py --action outline --prompt \"机器学习基础\"")
        print("   2. python scripts/book_writer.py --action expand --book-path ml_fundamentals --chapters 1,2,3")
        print("   3. 查看generated_books/目录中的输出")
    else:
        print("\n⚠️  部分测试失败，请检查并修复问题。")
        print("💡 建议:")
        print("   1. 运行: python scripts/install_dependencies.py")
        print("   2. 设置必要的API密钥环境变量")
        print("   3. 确保所有脚本文件存在")

    return passed == total

def main():
    """主函数"""
    print("🚀 智能写书技能安装测试")
    print("=" * 60)

    try:
        success = generate_test_report()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())