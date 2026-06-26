"""文本后处理 - 修复 PDF 提取的连字问题 + OCR 支持"""
import re
import subprocess
from pathlib import Path
from typing import Optional

# 常见英文单词列表（用于猜测分词）
COMMON_WORDS = {
    # 常用词
    "the", "and", "of", "to", "a", "in", "is", "that", "for", "it", "as", "was", "with", 
    "on", "by", "at", "from", "or", "an", "be", "this", "which", "are", "not", "but", 
    "have", "has", "will", "can", "all", "its", "if", "they", "there", "been", "more",
    # ML/统计常见词
    "probability", "distribution", "gaussian", "likelihood", "maximum", "maximum likelihood",
    "variance", "expectation", "random", "variable", "function", "parameter", "estimate",
    "sample", "mean", "value", "model", "data", "set", "training", "test", "error",
    "density", "posterior", "prior", "bayesian", "inference", "network", "neural",
    "chapter", "section", "exercise", "figure", "table", "equation", "result", "solution",
    "problem", "approach", "method", "algorithm", "gradient", "descent", "optimization",
}

# 大写开头的词（可能是专有名词）
CAPITAL_WORDS = {
    "ML", "MLE", "PDF", "OCR", "CNN", "RNN", "LSTM", "GAN", "VAE", "BERT", "GPT",
    "E", "N", "M", "K", "x", "y", "z", "i", "j", "n", "k", "µ", "σ", "α", "β", "γ",
}


def fix_spacing(text: str) -> str:
    """修复 PDF 提取的连字问题，尝试在合适位置添加空格
    
    策略：
    1. 数字和字母之间加空格：abc123 → abc 123
    2. 小写字母后跟大写字母加空格：sampleVariance → sample Variance
    3. 连续大写字母（ acronyms）后加空格：ML estimate → ML estimate
    4. 常见词匹配：如果匹配到常见词，优先分词
    """
    if not text:
        return text
    
    # 1. 数字和字母/单词之间
    # "sample123" → "sample 123"
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    
    # 2. 小写字母后跟大写字母 "sampleVariance" → "sample Variance"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # 3. 连续大写字母后跟小写字母 "MLEestimate" → "MLE estimate"
    text = re.sub(r'([A-Z]{2,})([A-Z][a-z])', r'\1 \2', text)
    
    # 4. 处理常见学术符号
    text = re.sub(r'\(cid:\d+\)', '', text)  # 移除 PDF cid 标记
    
    # 5. 处理连字符 "over-fitting" → "over-fitting"
    text = re.sub(r'-', '-', text)
    
    # 6. 处理 "ML" 后面的空格
    text = re.sub(r'\bML\b', 'ML', text)
    
    # 7. 移除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def enhance_text(text: str, use_spellcheck: bool = False) -> str:
    """增强文本可读性
    
    Args:
        text: 原始提取的文本
        use_spellcheck: 是否使用拼写检查（暂未实现）
    
    Returns:
        增强后的文本
    """
    if not text:
        return text
    
    # 修复间距
    text = fix_spacing(text)
    
    # 尝试智能分词（保守）
    text = _insert_spaces_by_dict(text)
    
    # 清理
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def _insert_spaces_by_dict(text: str) -> str:
    """用词典匹配尝试分词 - 只在非常确定的地方分词"""
    # 这个功能暂时保守处理，只处理连续大写字母
    # 更 aggressive 的分词容易出错
    
    # 处理连续大写字母 + 小写：MLestimate → ML estimate
    result = re.sub(r'([A-Z]{2,})([A-Z][a-z])', r'\1 \2', text)
    
    # 处理小写后跟大写：sampleVariance → sample Variance  
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', result)
    
    return result


def is_scanned_pdf(pdf_path: str) -> bool:
    """检测 PDF 是否为扫描件（无文本层）"""
    import pdfplumber
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 提取所有页文本
            total_text = ""
            for page in pdf.pages:
                text = page.extract_text() or ""
                total_text += text
            
            # 如果文本量少于预期，认为是扫描件
            # 一页正常 PDF 应该有至少 500 字符
            avg_chars_per_page = len(total_text) / max(len(pdf.pages), 1)
            return avg_chars_per_page < 50
            
    except Exception:
        return False


def extract_with_ocr(pdf_path: str, page_num: int, lang: str = "eng") -> str:
    """用 OCR 提取扫描件 PDF 的文本
    
    需要安装 tesseract:
    - macOS: brew install tesseract
    - Ubuntu: sudo apt install tesseract-ocr
    
    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（1-based）
        lang: OCR 语言（默认英语）
    
    Returns:
        提取的文本
    """
    import fitz  # PyMuPDF
    
    # 1. PDF → 图片
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    
    # 转成图片（300 DPI 保证清晰度）
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
    
    # 保存临时图片
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img_path = tmp.name
        pix.save(img_path)
    
    doc.close()
    
    try:
        # 2. OCR 识别
        result = subprocess.run(
            ["tesseract", img_path, "-", "-l", lang],
            capture_output=True,
            text=True,
            timeout=60
        )
        text = result.stdout
        
        # 3. 后处理
        text = enhance_text(text)
        
        return text
        
    finally:
        # 清理临时文件
        Path(img_path).unlink(missing_ok=True)


def extract_textsmart(pdf_path: str, page_num: int, force_ocr: bool = False) -> str:
    """智能文本提取：自动选择最佳提取方式
    
    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（1-based）
        force_ocr: 强制使用 OCR
    
    Returns:
        提取的文本
    """
    import pdfplumber
    
    # 先尝试直接提取
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        text = page.extract_text() or ""
    
    # 检查是否需要 OCR
    needs_ocr = force_ocr or len(text.strip()) < 50
    
    if needs_ocr:
        try:
            text = extract_with_ocr(pdf_path, page_num)
        except FileNotFoundError:
            # tesseract 未安装
            raise RuntimeError(
                "OCR 需要安装 tesseract: brew install tesseract (macOS) 或 "
                "sudo apt install tesseract-ocr (Ubuntu)"
            )
    
    # 后处理
    text = enhance_text(text)
    
    return text
