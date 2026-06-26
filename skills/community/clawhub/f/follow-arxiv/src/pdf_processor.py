"""PDF 处理与转换模块"""

import os
import requests
import fitz  # PyMuPDF
from typing import Dict, Any, Optional
from pathlib import Path
import re


class PDFProcessor:
    """PDF 处理器，支持 LaTeX 公式保留"""

    def __init__(self, config: Dict[str, Any]):
        self.pdf_dir = config.get('pdf_download_dir', './pdfs')
        self.max_retries = config.get('max_retries', 3)
        os.makedirs(self.pdf_dir, exist_ok=True)

    def download_pdf(self, pdf_url: str, arxiv_id: str) -> str:
        """
        下载 PDF 文件

        Args:
            pdf_url: PDF 的 URL
            arxiv_id: Arxiv ID

        Returns:
            下载后的文件路径
        """
        pdf_path = os.path.join(self.pdf_dir, f"{arxiv_id}.pdf")

        # 如果已存在，直接返回
        if os.path.exists(pdf_path):
            return pdf_path

        # 下载 PDF
        for attempt in range(self.max_retries):
            try:
                response = requests.get(pdf_url, timeout=30)
                response.raise_for_status()

                with open(pdf_path, 'wb') as f:
                    f.write(response.content)

                return pdf_path

            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"下载 PDF 失败: {e}")
                continue

        raise Exception("下载 PDF 失败")

    def extract_text_with_latex(self, pdf_path: str) -> Dict[str, Any]:
        """
        提取 PDF 文本，尽可能保留 LaTeX 公式

        Args:
            pdf_path: PDF 文件路径

        Returns:
            包含结构化文本内容的字典
        """
        try:
            doc = fitz.open(pdf_path)

            sections = []
            full_text = []
            equations = []

            for page_num, page in enumerate(doc):
                # 提取文本块
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if "lines" in block:
                        block_text = []

                        for line in block["lines"]:
                            line_text = ""
                            for span in line["spans"]:
                                text = span["text"]
                                font = span["font"]

                                # 检测是否为数学公式（基于字体）
                                if self._is_math_font(font):
                                    # 尝试保留 LaTeX 格式
                                    latex_text = self._extract_latex(text, font)
                                    line_text += latex_text
                                    if latex_text.strip():
                                        equations.append({
                                            'page': page_num + 1,
                                            'content': latex_text
                                        })
                                else:
                                    line_text += text

                            block_text.append(line_text)

                        section_text = '\n'.join(block_text)
                        if section_text.strip():
                            sections.append({
                                'page': page_num + 1,
                                'text': section_text,
                                'bbox': block.get("bbox", [])
                            })
                            full_text.append(section_text)

            # 在关闭文档之前获取页数
            total_pages = len(doc)
            doc.close()

            return {
                'full_text': '\n\n'.join(full_text),
                'sections': sections,
                'equations': equations,
                'metadata': {
                    'total_pages': total_pages,
                    'total_equations': len(equations)
                }
            }

        except Exception as e:
            raise Exception(f"提取 PDF 文本失败: {e}")

    def _is_math_font(self, font_name: str) -> bool:
        """判断是否为数学字体"""
        math_keywords = ['math', 'symbol', 'cal', 'cmr', 'cmsy', 'cmmi']
        font_lower = font_name.lower()
        return any(keyword in font_lower for keyword in math_keywords)

    def _extract_latex(self, text: str, font: str) -> str:
        """尝试提取 LaTeX 公式"""
        # 简单的 LaTeX 保留策略
        # 如果文本包含特殊数学符号，尝试用 LaTeX 表示

        # 常见符号映射
        symbol_map = {
            'α': r'\alpha',
            'β': r'\beta',
            'γ': r'\gamma',
            'δ': r'\delta',
            'ε': r'\epsilon',
            'θ': r'\theta',
            'λ': r'\lambda',
            'μ': r'\mu',
            'π': r'\pi',
            'σ': r'\sigma',
            'φ': r'\phi',
            'ω': r'\omega',
            '∞': r'\infty',
            '∑': r'\sum',
            '∏': r'\prod',
            '∫': r'\int',
            '∂': r'\partial',
            '∇': r'\nabla',
            '≤': r'\leq',
            '≥': r'\geq',
            '≠': r'\neq',
            '∈': r'\in',
            '⊂': r'\subset',
            '→': r'\rightarrow',
        }

        latex_text = text
        for symbol, latex in symbol_map.items():
            latex_text = latex_text.replace(symbol, latex)

        return latex_text

    def process_paper(self, paper_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理论文：下载 PDF 并提取文本

        Args:
            paper_metadata: 论文元数据

        Returns:
            包含元数据和文本内容的字典
        """
        arxiv_id = paper_metadata['arxiv_id']
        pdf_url = paper_metadata['pdf_url']

        # 下载 PDF
        pdf_path = self.download_pdf(pdf_url, arxiv_id)

        # 提取文本
        text_data = self.extract_text_with_latex(pdf_path)

        # 合并元数据和文本
        result = {
            **paper_metadata,
            'content': text_data
        }

        return result


def process_pdf(
    paper_metadata: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    处理 PDF 的便捷函数

    Args:
        paper_metadata: 论文元数据
        config: 配置字典

    Returns:
        处理后的论文数据
    """
    if config is None:
        from utils import load_config
        config = load_config()

    processor = PDFProcessor(config)
    return processor.process_paper(paper_metadata)
