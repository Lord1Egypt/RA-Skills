"""
入口函数模块
处理命令行参数，调用解析器
"""

import sys
from pathlib import Path

from .extractor import EnhancedHTMLExtractor, _setup_utf8_output


def main():
    """主入口函数"""
    # 设置UTF-8输出编码（解决Windows终端编码问题）
    _setup_utf8_output()

    if len(sys.argv) < 2:
        print("用法: python html-extractor.py <html文件> [输出格式: markdown|json|interactive]")
        print("")
        print("输出格式说明:")
        print("  markdown     - 标准分析报告（默认）")
        print("  json         - JSON格式数据")
        print("  interactive  - 交互式业务分析（包含流程推断和问题）")
        print("")
        print("示例: python html-extractor.py page.html markdown")
        print("      python html-extractor.py page.html interactive")
        sys.exit(1)

    html_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "markdown"

    if not Path(html_file).exists():
        print(f"错误: HTML文件不存在: {html_file}")
        sys.exit(1)

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    extractor = EnhancedHTMLExtractor(html_content, f"file://{html_file}")

    try:
        if output_format.lower() == "interactive":
            # 交互式分析模式
            interactive = extractor.extract_interactive_analysis()
            result = extractor.to_interactive_markdown(interactive)
        elif output_format.lower() == "json":
            analysis = extractor.extract_full_structure()
            result = extractor.to_json(analysis)
        else:
            analysis = extractor.extract_full_structure()
            result = extractor.to_markdown(analysis)
    except Exception as e:
        print(f"分析HTML失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()