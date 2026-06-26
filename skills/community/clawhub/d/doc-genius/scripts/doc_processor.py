#!/usr/bin/env python3
"""
Doc Genius - 智能文档处理助手
支持PDF/Word/Markdown智能摘要、格式转换、批量处理
"""
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any
import concurrent.futures
from dataclasses import dataclass, asdict

# 本地依赖
try:
    import PyPDF2
    from docx import Document
    import markdown
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请安装: pip install PyPDF2 python-docx markdown beautifulsoup4")
    sys.exit(1)

# 可选：OpenAI API
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@dataclass
class DocumentInfo:
    """文档信息"""
    file: str
    type: str
    summary: str
    keywords: List[str]
    word_count: int
    pages: Optional[int] = None
    error: Optional[str] = None


class DocumentProcessor:
    """文档处理器"""

    def __init__(self, method: str = "local", model: str = "gpt-3.5-turbo"):
        """
        初始化
        
        Args:
            method: 摘要方法（local/ai）
            model: AI模型（仅method=ai时使用）
        """
        self.method = method
        self.model = model
        
        # 检查OpenAI API
        if method == "ai" and not OPENAI_AVAILABLE:
            print("⚠️ OpenAI未安装，自动切换到本地模式")
            self.method = "local"
        
        if method == "ai" and not os.environ.get("OPENAI_API_KEY"):
            print("⚠️ 未设置OPENAI_API_KEY，自动切换到本地模式")
            self.method = "local"

    # ═══════════════════════════════════════════════════
    # 文本提取
    # ═══════════════════════════════════════════════════

    def extract_text_pdf(self, file_path: Path) -> tuple[str, int]:
        """从PDF提取文本"""
        text = []
        pages = 0
        
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = len(reader.pages)
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"PDF提取失败: {e}")
        
        return '\n'.join(text), pages

    def extract_text_docx(self, file_path: Path) -> str:
        """从Word提取文本"""
        try:
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n'.join(paragraphs)
        except Exception as e:
            raise Exception(f"Word提取失败: {e}")

    def extract_text_markdown(self, file_path: Path) -> str:
        """从Markdown提取文本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 转换为HTML并提取纯文本
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        except Exception as e:
            raise Exception(f"Markdown提取失败: {e}")

    def extract_text(self, file_path: Path) -> tuple[str, str, Optional[int]]:
        """
        自动识别格式并提取文本
        
        Returns:
            (文本内容, 文件类型, 页数)
        """
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            text, pages = self.extract_text_pdf(file_path)
            return text, 'pdf', pages
        elif suffix in ['.docx', '.doc']:
            text = self.extract_text_docx(file_path)
            return text, 'word', None
        elif suffix in ['.md', '.markdown']:
            text = self.extract_text_markdown(file_path)
            return text, 'markdown', None
        elif suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, 'text', None
        else:
            raise ValueError(f"不支持的格式: {suffix}")

    # ═══════════════════════════════════════════════════
    # 智能摘要
    # ═══════════════════════════════════════════════════

    def summarize_local(self, text: str, max_sentences: int = 5) -> str:
        """
        本地摘要（TextRank算法简化版）
        
        Args:
            text: 文本内容
            max_sentences: 最大句子数
        """
        # 分句
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        sentences += [s.strip() for s in text.split('.') if s.strip() and s.strip() not in sentences]
        
        if not sentences:
            return "无法生成摘要（文本太短或格式异常）"
        
        # 简单策略：选择前N个重要句子
        # （实际应用可以用TextRank/TF-IDF，这里简化）
        word_freq = {}
        for sentence in sentences:
            for word in sentence.split():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按词频评分句子
        sentence_scores = []
        for sentence in sentences:
            score = sum(word_freq.get(word, 0) for word in sentence.split())
            sentence_scores.append((sentence, score))
        
        # 选择得分最高的N句
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:max_sentences]]
        
        # 按原文顺序排列
        ordered_summary = []
        for sentence in sentences:
            if sentence in top_sentences:
                ordered_summary.append(sentence)
        
        return '。'.join(ordered_summary[:max_sentences])

    def summarize_ai(self, text: str, max_words: int = 200) -> str:
        """
        AI摘要（OpenAI API）
        
        Args:
            text: 文本内容
            max_words: 最大字数
        """
        if not OPENAI_AVAILABLE:
            return self.summarize_local(text)
        
        try:
            client = openai.OpenAI()
            
            # 限制输入长度
            if len(text) > 10000:
                text = text[:10000] + "..."
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的文档摘要助手。请用简洁、准确的语言总结文档的核心内容。"
                    },
                    {
                        "role": "user",
                        "content": f"请用{max_words}字以内总结以下文档：\n\n{text}"
                    }
                ],
                max_tokens=max_words * 2,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ AI摘要失败，切换到本地模式: {e}")
            return self.summarize_local(text)

    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """提取关键词（简化版TF-IDF）"""
        # 分词（简化版）
        words = []
        for word in text.split():
            # 过滤停用词
            if len(word) > 2 and word not in ['的', '是', '在', '和', '了', 'the', 'a', 'an', 'is', 'are']:
                words.append(word)
        
        # 统计词频
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序并返回
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:max_keywords]]

    # ═══════════════════════════════════════════════════
    # 格式转换
    # ═══════════════════════════════════════════════════

    def convert_to_markdown(self, text: str, doc_type: str) -> str:
        """转换为Markdown格式"""
        if doc_type == 'markdown':
            return text
        
        # 添加标题
        lines = text.split('\n')
        markdown_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # 简单的格式推断
            if i == 0:
                markdown_lines.append(f"# {line}\n")
            elif len(line) < 50 and line.endswith(':'):
                markdown_lines.append(f"\n## {line[:-1]}\n")
            else:
                markdown_lines.append(line)
        
        return '\n'.join(markdown_lines)

    def convert_to_html(self, text: str, doc_type: str) -> str:
        """转换为HTML格式"""
        # 先转Markdown
        md_text = self.convert_to_markdown(text, doc_type)
        
        # Markdown → HTML
        html_content = markdown.markdown(md_text)
        
        # 添加HTML骨架
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Converted Document</title>
</head>
<body>
{html_content}
</body>
</html>"""
        return html

    # ═══════════════════════════════════════════════════
    # 主要接口
    # ═══════════════════════════════════════════════════

    def summarize(self, file_path: Path, output_format: str = "json") -> Dict[str, Any]:
        """
        智能摘要
        
        Args:
            file_path: 文件路径
            output_format: 输出格式（json/markdown）
        """
        # 提取文本
        text, doc_type, pages = self.extract_text(file_path)
        
        # 生成摘要
        if self.method == "ai":
            summary = self.summarize_ai(text)
        else:
            summary = self.summarize_local(text)
        
        # 提取关键词
        keywords = self.extract_keywords(text)
        
        # 统计字数
        word_count = len(text.split())
        
        # 构造结果
        result = DocumentInfo(
            file=str(file_path.name),
            type=doc_type,
            summary=summary,
            keywords=keywords,
            word_count=word_count,
            pages=pages
        )
        
        if output_format == "json":
            return asdict(result)
        elif output_format == "markdown":
            return self._format_as_markdown(result)
        else:
            return summary

    def convert(self, file_path: Path, output_format: str, out_file: Optional[Path] = None) -> str:
        """
        格式转换
        
        Args:
            file_path: 输入文件路径
            output_format: 输出格式（markdown/html）
            out_file: 输出文件路径（可选）
        """
        # 提取文本
        text, doc_type, _ = self.extract_text(file_path)
        
        # 转换
        if output_format == "markdown":
            converted = self.convert_to_markdown(text, doc_type)
            ext = ".md"
        elif output_format == "html":
            converted = self.convert_to_html(text, doc_type)
            ext = ".html"
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")
        
        # 保存到文件
        if out_file:
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"✅ 已保存到: {out_file}")
        
        return converted

    def batch_process(
        self,
        folder_path: Path,
        action: str = "summarize",
        output_format: str = "markdown",
        workers: int = 5,
        output_dir: Optional[Path] = None
    ) -> List[Dict]:
        """
        批量处理
        
        Args:
            folder_path: 文件夹路径
            action: 操作类型（summarize/convert）
            output_format: 输出格式
            workers: 并发数
            output_dir: 输出目录
        """
        # 扫描文件
        supported_ext = ['.pdf', '.docx', '.doc', '.md', '.markdown', '.txt']
        files = [f for f in folder_path.rglob('*') if f.suffix.lower() in supported_ext]
        
        if not files:
            print(f"⚠️ 未找到支持的文件")
            return []
        
        print(f"📁 找到 {len(files)} 个文件")
        
        results = []
        
        # 并发处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            
            for file_path in files:
                if action == "summarize":
                    future = executor.submit(self.summarize, file_path, output_format)
                elif action == "convert":
                    if output_dir:
                        out_file = output_dir / (file_path.stem + f".{output_format}")
                    else:
                        out_file = None
                    future = executor.submit(self.convert, file_path, output_format, out_file)
                else:
                    continue
                
                futures.append((file_path, future))
            
            # 收集结果
            for i, (file_path, future) in enumerate(futures, 1):
                try:
                    result = future.result()
                    results.append(result if isinstance(result, dict) else {"file": str(file_path), "result": result})
                    print(f"✅ [{i}/{len(files)}] {file_path.name}")
                except Exception as e:
                    print(f"❌ [{i}/{len(files)}] {file_path.name}: {e}")
                    results.append({"file": str(file_path), "error": str(e)})
        
        return results

    def _format_as_markdown(self, doc_info: DocumentInfo) -> str:
        """格式化为Markdown"""
        md = f"""# 文档摘要

**文件**: {doc_info.file}  
**类型**: {doc_info.type}  
**字数**: {doc_info.word_count}  
"""
        
        if doc_info.pages:
            md += f"**页数**: {doc_info.pages}\n"
        
        md += f"""
---

## 摘要

{doc_info.summary}

---

## 关键词

{', '.join(doc_info.keywords)}
"""
        
        return md


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='Doc Genius - 智能文档处理助手')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # summarize命令
    summarize_parser = subparsers.add_parser('summarize', help='智能摘要')
    summarize_parser.add_argument('file', type=Path, help='文件路径')
    summarize_parser.add_argument('--format', choices=['json', 'markdown', 'text'], default='json', help='输出格式')
    summarize_parser.add_argument('--method', choices=['local', 'ai'], default='local', help='摘要方法')
    summarize_parser.add_argument('--model', default='gpt-3.5-turbo', help='AI模型')
    
    # convert命令
    convert_parser = subparsers.add_parser('convert', help='格式转换')
    convert_parser.add_argument('file', type=Path, help='文件路径')
    convert_parser.add_argument('--output', required=True, choices=['markdown', 'html'], help='输出格式')
    convert_parser.add_argument('--out-file', type=Path, help='输出文件路径')
    
    # batch命令
    batch_parser = subparsers.add_parser('batch', help='批量处理')
    batch_parser.add_argument('folder', type=Path, help='文件夹路径')
    batch_parser.add_argument('--action', choices=['summarize', 'convert'], default='summarize', help='操作类型')
    batch_parser.add_argument('--output', choices=['markdown', 'html', 'json'], default='markdown', help='输出格式')
    batch_parser.add_argument('--workers', type=int, default=5, help='并发数')
    batch_parser.add_argument('--output-dir', type=Path, help='输出目录')
    batch_parser.add_argument('--report', type=Path, help='生成报告文件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化处理器
    processor = DocumentProcessor(
        method=getattr(args, 'method', 'local'),
        model=getattr(args, 'model', 'gpt-3.5-turbo')
    )
    
    # 执行命令
    try:
        if args.command == 'summarize':
            result = processor.summarize(args.file, args.format)
            
            if args.format == 'json':
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result)
        
        elif args.command == 'convert':
            result = processor.convert(args.file, args.output, args.out_file)
            
            if not args.out_file:
                print(result)
        
        elif args.command == 'batch':
            results = processor.batch_process(
                args.folder,
                args.action,
                args.output,
                args.workers,
                args.output_dir
            )
            
            # 生成报告
            if args.report:
                with open(args.report, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"\n📊 报告已生成: {args.report}")
            
            # 打印摘要
            success = sum(1 for r in results if 'error' not in r)
            print(f"\n✅ 完成: {success}/{len(results)}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
