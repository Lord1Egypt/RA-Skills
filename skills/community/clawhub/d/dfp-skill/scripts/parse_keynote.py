#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keynote 文件解析器 (.key file parser)
=====================================

作者: Wang Dongjie, CGMA/AICPA&CIMA, © 2026

解析 Apple Keynote (.key) 文档，提取幻灯片结构和文本内容。
作为数智财务演示 Skill 的配套工具，支持解析已有演示文稿内容。

Keynote 的 .key 文件本质上是一个 ZIP 压缩包（iWork Archive 格式），
内部包含多个 .iwa 文件（iWork Archive 文件），使用 Protobuf 序列化格式。

此脚本实现了一个简化版的 .key 解析器，能够：
1. 解压 .key 文件
2. 解析幻灯片结构
3. 提取文本内容（标题、正文、备注）
4. 输出 JSON / Markdown 格式报告

用法:
    python3 parse_keynote.py <file.key> [--output output.json] [--format json|markdown]
"""

import os
import sys
import json
import zipfile
import argparse
import tempfile
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET


class KeynoteParser:
    """Keynote (.key) 文件解析器"""

    def __init__(self, key_file_path):
        self.key_file = Path(key_file_path)
        if not self.key_file.exists():
            raise FileNotFoundError(f"文件不存在: {key_file_path}")
        if self.key_file.suffix.lower() != '.key':
            print(f"⚠️  警告: 文件扩展名不是 .key: {self.key_file.suffix}")
        self.extract_dir = None
        self.slides = []

    def extract(self):
        """解压 .key 文件到临时目录"""
        self.extract_dir = tempfile.mkdtemp(prefix='keynote_extract_')
        try:
            with zipfile.ZipFile(self.key_file, 'r') as zf:
                zf.extractall(self.extract_dir)
            print(f"✓ 已解压到: {self.extract_dir}")
            return self.extract_dir
        except zipfile.BadZipFile:
            # 尝试作为包目录处理（macOS 上 .key 有时是 bundle）
            if self.key_file.is_dir():
                shutil.copytree(self.key_file, self.extract_dir, dirs_exist_ok=True)
                print(f"✓ 已复制 bundle 到: {self.extract_dir}")
                return self.extract_dir
            raise

    def list_contents(self):
        """列出 .key 文件中的内容结构"""
        if not self.extract_dir:
            self.extract()

        contents = []
        extract_path = Path(self.extract_dir)

        for item in extract_path.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(extract_path)
                size = item.stat().st_size
                contents.append({
                    'path': str(rel_path),
                    'size': size
                })

        contents.sort(key=lambda x: x['path'])
        return contents

    def parse_slides(self):
        """解析幻灯片内容"""
        if not self.extract_dir:
            self.extract()

        extract_path = Path(self.extract_dir)
        slides = []

        # 方法1: 尝试从 Index/ 目录解析 .iwa 文件
        index_dir = extract_path / 'Index'
        if index_dir.exists():
            slides = self._parse_from_index(index_dir)

        # 方法2: 从 preview.pdf 或 preview 中提取（如无法解析 iwa）
        if not slides:
            slides = self._parse_from_preview(extract_path)

        # 方法3: 降级方案 - 从任何文本/XML文件中提取
        if not slides:
            slides = self._parse_from_text_files(extract_path)

        self.slides = slides
        return slides

    def _parse_from_index(self, index_dir):
        """从 Index 目录解析幻灯片"""
        slides = []
        slide_num = 0

        # 查找幻灯片相关的文件
        iwa_files = sorted(index_dir.glob('*.iwa'))

        # 尝试解析每个 iwa 文件（简化版 - 搜索可读文本）
        for iwa_file in iwa_files:
            try:
                with open(iwa_file, 'rb') as f:
                    content = f.read()

                # 尝试提取可读的文本片段
                text_parts = []
                try:
                    # 尝试作为 protobuf-lite 的文本提取
                    decoded = content.decode('utf-8', errors='ignore')
                    # 提取看起来像中文/英文的文本片段
                    import re
                    # 匹配中文和英文文本
                    matches = re.findall(r'[\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9\s\.,;:!?、，。；：！？]{2,}', decoded)
                    text_parts = [m.strip() for m in matches if len(m.strip()) > 2]
                except:
                    pass

                if text_parts:
                    slide_num += 1
                    slide = {
                        'slide_number': slide_num,
                        'source_file': iwa_file.name,
                        'title': text_parts[0] if text_parts else '',
                        'body': '\n'.join(text_parts[1:5]) if len(text_parts) > 1 else '',
                        'text_fragments': text_parts
                    }
                    slides.append(slide)
            except Exception as e:
                print(f"  解析 {iwa_file.name} 时出错: {e}")

        return slides

    def _parse_from_preview(self, extract_path):
        """从 preview 文件解析（降级方案）"""
        slides = []

        # 查找 preview.pdf
        preview_pdf = extract_path / 'preview.pdf'
        if preview_pdf.exists():
            slides.append({
                'slide_number': 1,
                'note': '检测到 preview.pdf，可使用 PDF 解析工具进一步提取内容',
                'preview_size': preview_pdf.stat().st_size
            })

        # 查找缩略图
        thumbnails_dir = extract_path / 'thumbnails'
        if thumbnails_dir.exists():
            thumb_files = list(thumbnails_dir.glob('*'))
            slides.append({
                'slide_number': 0,
                'note': f'检测到 {len(thumb_files)} 个缩略图文件',
                'thumbnails': [f.name for f in thumb_files[:10]]
            })

        return slides

    def _parse_from_text_files(self, extract_path):
        """从各种文本/XML文件中提取内容（最后的降级方案）"""
        slides = []
        text_content = []

        # 搜索所有可能包含文本的文件
        for pattern in ['*.xml', '*.txt', '*.json', '*.rels']:
            for filepath in extract_path.rglob(pattern):
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if content.strip():
                        # 提取简短描述
                        rel_path = filepath.relative_to(extract_path)
                        text_content.append(f"[{rel_path}] {content[:200]}...")
                except:
                    pass

        if text_content:
            slides.append({
                'slide_number': 1,
                'note': '从辅助文件中提取的文本片段',
                'extracted_texts': text_content[:20]
            })

        return slides

    def to_json(self):
        """转换为 JSON 格式"""
        return {
            'source_file': str(self.key_file),
            'file_size': self.key_file.stat().st_size,
            'slide_count': len(self.slides),
            'slides': self.slides
        }

    def to_markdown(self):
        """转换为 Markdown 格式报告"""
        lines = []
        lines.append(f"# Keynote 文档分析报告")
        lines.append("")
        lines.append(f"- **文件**: `{self.key_file.name}`")
        lines.append(f"- **文件大小**: {self.key_file.stat().st_size:,} bytes")
        lines.append(f"- **幻灯片数量**: {len(self.slides)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for slide in self.slides:
            num = slide.get('slide_number', '?')
            lines.append(f"## 幻灯片 {num}")
            lines.append("")

            if 'title' in slide and slide['title']:
                lines.append(f"**标题**: {slide['title']}")
                lines.append("")

            if 'body' in slide and slide['body']:
                lines.append("**内容**:")
                lines.append("")
                lines.append(slide['body'])
                lines.append("")

            if 'text_fragments' in slide and slide['text_fragments']:
                lines.append("**文本片段**:")
                lines.append("")
                for i, fragment in enumerate(slide['text_fragments'][:10], 1):
                    lines.append(f"{i}. {fragment}")
                lines.append("")

            if 'note' in slide:
                lines.append(f"*注意: {slide['note']}*")
                lines.append("")

            if 'extracted_texts' in slide:
                lines.append("**提取内容**:")
                lines.append("")
                for text in slide['extracted_texts']:
                    lines.append(f"- {text}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return '\n'.join(lines)

    def cleanup(self):
        """清理临时文件"""
        if self.extract_dir and os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)
            print(f"✓ 已清理临时目录")


def main():
    parser = argparse.ArgumentParser(
        description='解析 Keynote (.key) 文件，提取幻灯片内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 parse_keynote.py presentation.key
  python3 parse_keynote.py presentation.key --output result.json
  python3 parse_keynote.py presentation.key --format markdown --output report.md
        """
    )
    parser.add_argument('key_file', help='Keynote .key 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径（默认输出到控制台）')
    parser.add_argument('--format', '-f',
                       choices=['json', 'markdown', 'json-pretty'],
                       default='json-pretty',
                       help='输出格式 (默认: json-pretty)')
    parser.add_argument('--list-files', action='store_true',
                       help='仅列出 .key 文件内的内容结构')

    args = parser.parse_args()

    print(f"🔍 正在解析: {args.key_file}")
    print("=" * 60)

    kn_parser = KeynoteParser(args.key_file)

    try:
        # 解压
        kn_parser.extract()

        # 如果只需要列出内容
        if args.list_files:
            contents = kn_parser.list_contents()
            print(f"\n📋 文件内容结构 ({len(contents)} 个文件):\n")
            for item in contents:
                size_kb = item['size'] / 1024 if item['size'] > 1024 else item['size']
                unit = 'KB' if item['size'] > 1024 else 'B'
                print(f"  {size_kb:8.1f} {unit}  {item['path']}")
            kn_parser.cleanup()
            return

        # 解析幻灯片
        slides = kn_parser.parse_slides()

        print(f"\n✓ 解析完成: 共 {len(slides)} 张幻灯片")
        print("=" * 60)

        # 格式化输出
        if args.format == 'json':
            output = json.dumps(kn_parser.to_json(), ensure_ascii=False)
        elif args.format == 'json-pretty':
            output = json.dumps(kn_parser.to_json(), ensure_ascii=False, indent=2)
        else:  # markdown
            output = kn_parser.to_markdown()

        # 输出
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n💾 结果已保存: {output_path}")
        else:
            print("\n" + output)

    except Exception as e:
        print(f"\n❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        kn_parser.cleanup()


if __name__ == '__main__':
    main()
