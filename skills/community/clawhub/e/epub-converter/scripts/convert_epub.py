#!/usr/bin/env python3
"""
EPUB繁简转换工具
将繁体中文EPUB电子书转换为简体中文版本
"""

import sys
import os
import argparse
from pathlib import Path

def check_dependencies():
    """检查并安装必要的依赖"""
    venv_path = Path.home() / ".openclaw" / "epub_venv"
    
    # 如果虚拟环境存在，尝试从中导入
    if venv_path.exists():
        # 添加虚拟环境到Python路径
        site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        if site_packages.exists():
            sys.path.insert(0, str(site_packages))
    
    try:
        from ebooklib import epub
        from opencc import OpenCC
        return True
    except ImportError:
        print("📦 正在安装必要的依赖...")
        import subprocess
        
        # 创建虚拟环境
        if not venv_path.exists():
            print(f"创建虚拟环境: {venv_path}")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        # 安装依赖
        pip_path = venv_path / "bin" / "pip"
        subprocess.run([str(pip_path), "install", "ebooklib", "opencc-python-reimplemented"], check=True)
        
        print("✅ 依赖安装完成")
        
        # 重新添加到路径
        site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        if site_packages.exists():
            sys.path.insert(0, str(site_packages))
        
        # 再次尝试导入
        try:
            from ebooklib import epub
            from opencc import OpenCC
            return True
        except ImportError:
            print("⚠️  依赖安装后仍无法导入，请重新运行脚本")
            return False

def convert_epub(input_path, output_path=None, direction='t2s'):
    """
    转换EPUB文件的繁简体
    
    Args:
        input_path: 输入EPUB文件路径
        output_path: 输出EPUB文件路径（可选）
        direction: 转换方向，'t2s'=繁转简，'s2t'=简转繁
    """
    from ebooklib import epub
    from opencc import OpenCC
    
    # 初始化转换器
    cc = OpenCC(direction)
    
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        return False
    
    # 生成输出文件名
    if output_path is None:
        suffix = "_简体" if direction == 't2s' else "_繁體"
        output_path = input_path.parent / f"{input_path.stem}{suffix}{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    print(f"📖 正在读取EPUB文件: {input_path.name}")
    
    try:
        # 读取EPUB
        book = epub.read_epub(str(input_path))
        print("✅ 成功读取EPUB")
        
        # 获取书籍信息
        title = book.get_metadata('DC', 'title')
        if title:
            original_title = title[0][0]
            print(f"📚 原书名: {original_title}")
        
        # 转换所有文档内容
        items = list(book.get_items())
        print(f"📄 找到 {len(items)} 个项目")
        
        converted_count = 0
        for item in items:
            # ITEM_DOCUMENT = 9
            if item.get_type() == 9:
                try:
                    content = item.get_content().decode('utf-8')
                    converted_content = cc.convert(content)
                    item.set_content(converted_content.encode('utf-8'))
                    converted_count += 1
                    print(f"  ✓ 已转换: {item.get_name()}")
                except Exception as e:
                    print(f"  ✗ 跳过: {item.get_name()}")
        
        print(f"\n✅ 成功转换 {converted_count} 个文档")
        
        # 转换元数据
        if title:
            new_title = cc.convert(original_title)
            book.set_title(new_title)
            print(f"📝 转换后书名: {new_title}")
        
        # 修复目录结构中的None值
        def fix_toc(toc_items):
            fixed = []
            for item in toc_items:
                if isinstance(item, tuple):
                    section, children = item
                    if hasattr(section, 'uid') and section.uid is None:
                        section.uid = f"navpoint_{len(fixed)}"
                    fixed_children = fix_toc(children)
                    fixed.append((section, fixed_children))
                else:
                    if hasattr(item, 'uid') and item.uid is None:
                        item.uid = f"navpoint_{len(fixed)}"
                    fixed.append(item)
            return fixed
        
        if hasattr(book, 'toc') and book.toc:
            print("\n🔧 修复目录结构...")
            book.toc = fix_toc(book.toc)
        
        # 保存新的EPUB
        print(f"\n💾 正在保存到: {output_path.name}")
        epub.write_epub(str(output_path), book, {})
        
        # 显示文件信息
        original_size = input_path.stat().st_size / 1024
        new_size = output_path.stat().st_size / 1024
        
        print(f"\n🎉 转换完成！")
        print(f"📁 输出文件: {output_path}")
        print(f"📊 原始文件: {original_size:.1f} KB")
        print(f"📊 新文件: {new_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='EPUB繁简转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 繁体转简体
  %(prog)s input.epub
  
  # 指定输出文件
  %(prog)s input.epub -o output.epub
  
  # 简体转繁体
  %(prog)s input.epub --direction s2t
        """
    )
    
    parser.add_argument('input', help='输入EPUB文件路径')
    parser.add_argument('-o', '--output', help='输出EPUB文件路径（可选）')
    parser.add_argument('-d', '--direction', 
                       choices=['t2s', 's2t'],
                       default='t2s',
                       help='转换方向: t2s=繁转简(默认), s2t=简转繁')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 执行转换
    success = convert_epub(args.input, args.output, args.direction)
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
