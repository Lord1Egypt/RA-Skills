#!/usr/bin/env python3
"""
知识库索引生成器
将文档目录转换为结构化 Markdown 索引
"""

import json
from pathlib import Path
from datetime import datetime
from markitdown import MarkItDown


class KnowledgeBaseIndexer:
    """知识库索引生成器"""

    def __init__(self, input_dir, output_dir, markdown_dir=None):
        """
        初始化索引器

        Args:
            input_dir: 源文档目录
            output_dir: 索引输出目录
            markdown_dir: 转换后的 Markdown 存放目录（默认同 output_dir）
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.markdown_dir = Path(markdown_dir) if markdown_dir else self.output_dir
        self.md_converter = MarkItDown()
        self.catalog = {
            "generated_at": datetime.now().isoformat(),
            "input_dir": str(self.input_dir),
            "files": [],
            "statistics": {}
        }

    def convert_document(self, file_path):
        """转换单个文档并返回元数据"""
        try:
            result = self.md_converter.convert(str(file_path))

            # 计算相对路径
            rel_path = file_path.relative_to(self.input_dir)
            md_filename = rel_path.with_suffix('.md')
            md_output_path = self.markdown_dir / md_filename

            # 确保输出目录存在
            md_output_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存 Markdown 文件
            md_output_path.write_text(result.text_content, encoding='utf-8')

            # 收集元数据
            metadata = {
                "original_path": str(file_path),
                "relative_path": str(rel_path),
                "markdown_path": str(md_output_path.relative_to(self.output_dir)),
                "size_bytes": file_path.stat().st_size,
                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "title": result.metadata.get('title', rel_path.stem),
                "author": result.metadata.get('author', ''),
                "line_count": len(result.text_content.splitlines()),
                "char_count": len(result.text_content)
            }

            return metadata, None

        except Exception as e:
            return None, str(file_path.name, str(e))

    def generate_index(self, recursive=True, overwrite=False):
        """生成完整索引"""
        print(f"开始处理目录: {self.input_dir}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 收集文件
        if recursive:
            files = list(self.input_dir.rglob("*"))
        else:
            files = list(self.input_dir.glob("*"))

        # 筛选支持的文件类型
        supported_ext = {'.pdf', '.docx', '.pptx', '.xlsx', '.txt',
                        '.html', '.csv', '.json', '.xml', '.zip',
                        '.epub', '.png', '.jpg', '.jpeg'}

        files_to_process = [f for f in files if f.is_file() and f.suffix.lower() in supported_ext]

        print(f"找到 {len(files_to_process)} 个支持的文件")

        success_count = 0
        error_list = []

        for i, file_path in enumerate(files_to_process, 1):
            print(f"[{i}/{len(files_to_process)}] 处理: {file_path.name}", end='\r')

            metadata, error = self.convert_document(file_path)

            if metadata:
                self.catalog["files"].append(metadata)
                success_count += 1
            else:
                error_list.append(error)

        print(f"\n✓ 成功转换 {success_count} 个文件")

        # 统计信息
        if self.catalog["files"]:
            total_lines = sum(f["line_count"] for f in self.catalog["files"])
            total_chars = sum(f["char_count"] for f in self.catalog["files"])
            total_size = sum(f["size_bytes"] for f in self.catalog["files"])

            self.catalog["statistics"] = {
                "total_files": success_count,
                "total_lines": total_lines,
                "total_characters": total_chars,
                "total_size_bytes": total_size,
                "error_count": len(error_list)
            }

        # 保存索引文件
        index_md = self.output_dir / "INDEX.md"
        catalog_json = self.output_dir / "CATALOG.json"

        self._write_markdown_index(index_md)
        self._write_json_catalog(catalog_json)

        # 保存错误日志
        if error_list:
            error_log = self.output_dir / "conversion_errors.log"
            error_log.write_text('\n'.join(error_list), encoding='utf-8')
            print(f"⚠  {len(error_list)} 个文件转换失败，详见: {error_log}")

        print(f"📄 索引文件: {index_md}")
        print(f"📊 目录数据: {catalog_json}")

    def _write_markdown_index(self, output_path):
        """生成人类可读的 Markdown 索引"""
        lines = [
            f"# 知识库索引",
            f"",
            f"> 生成时间: {self.catalog['generated_at']}",
            f"> 源目录: `{self.catalog['input_dir']}`",
            f"",
            f"## 统计概览",
            f"",
            f"- 📁 总文件数: **{self.catalog['statistics'].get('total_files', 0)}**",
            f"- 📝 总行数: **{self.catalog['statistics'].get('total_lines', 0):,}**",
            f"- 📊 总字符数: **{self.catalog['statistics'].get('total_characters', 0):,}**",
            f"- 💾 总大小: **{self.catalog['statistics'].get('total_size_bytes', 0):,} 字节**",
            f"",
            f"## 文件列表",
            f"",
        ]

        # 按目录分组
        files_by_dir = {}
        for file in self.catalog["files"]:
            parent = str(Path(file["relative_path"]).parent)
            if parent == '.':
                parent = '根目录'
            files_by_dir.setdefault(parent, []).append(file)

        for dir_name in sorted(files_by_dir.keys()):
            lines.append(f"### {dir_name}")
            lines.append("")
            for file in sorted(files_by_dir[dir_name], key=lambda x: x["relative_path"]):
                rel_md = file["markdown_path"]
                lines.append(f"- [`{file['title']}`]({rel_md})")
                lines.append(f"  - 原文件: `{file['original_path']}`")
                lines.append(f"  - 行数: {file['line_count']:,} | 字符: {file['char_count']:,}")
                if file['author']:
                    lines.append(f"  - 作者: {file['author']}")
                lines.append("")

        output_path.write_text('\n'.join(lines), encoding='utf-8')

    def _write_json_catalog(self, output_path):
        """生成机器可读的 JSON 目录"""
        output_path.write_text(json.dumps(self.catalog, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='知识库索引生成器 - 批量转换文档并生成搜索索引',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ./source_docs ./kb_index
  %(prog)s ./papers ./index --markdown-dir ./markdown
  %(prog)s ./input ./output --no-recursive
        """
    )

    parser.add_argument('input_dir', help='源文档目录')
    parser.add_argument('output_dir', help='索引输出目录')
    parser.add_argument('--markdown-dir', '-m', help='Markdown 文件存放目录（默认同输出目录）')
    parser.add_argument('--no-recursive', action='store_true', help='不递归处理子目录')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已转换的文件')

    args = parser.parse_args()

    indexer = KnowledgeBaseIndexer(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        markdown_dir=args.markdown_dir
    )

    indexer.generate_index(recursive=not args.no_recursive, overwrite=args.overwrite)


if __name__ == '__main__':
    main()