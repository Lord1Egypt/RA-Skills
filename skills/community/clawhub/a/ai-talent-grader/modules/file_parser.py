"""
文件解析模块 - 支持多种格式的简历和面试记录解析
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from loguru import logger

# 可选依赖
try:
    from PyPDF2 import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    logger.warning("PyPDF2 not installed, PDF parsing disabled")

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    logger.warning("python-docx not installed, DOCX parsing disabled")


@dataclass
class CandidateInfo:
    """候选人结构化信息"""
    candidate_id: str = ""
    name: Optional[str] = None
    years_of_experience: Optional[float] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    education: List[Dict] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    projects: List[Dict] = field(default_factory=list)
    work_history: List[Dict] = field(default_factory=list)
    raw_text: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class InterviewRecord:
    """面试记录结构化信息"""
    candidate_id: str = ""
    interview_date: Optional[str] = None
    interviewer: Optional[str] = None
    questions_and_answers: List[Dict] = field(default_factory=list)
    interviewer_notes: str = ""
    overall_impression: str = ""
    score: Optional[float] = None
    recommendation: Optional[str] = None
    raw_text: str = ""
    metadata: Dict = field(default_factory=dict)


class FileParser:
    """文件解析器"""

    SUPPORTED_FORMATS = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.txt': 'text',
        '.md': 'text',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.max_file_size = self.config.get('max_file_size_mb', 20) * 1024 * 1024

    def parse_file(self, file_path: str) -> str:
        """解析任意格式文件，返回纯文本内容"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        if path.stat().st_size > self.max_file_size:
            raise ValueError(f"文件大小超过限制 ({self.max_file_size // 1024 // 1024}MB): {file_path}")

        ext = path.suffix.lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的文件格式: {ext}")

        parser_method = getattr(self, f"_parse_{self.SUPPORTED_FORMATS[ext]}", None)
        if parser_method is None:
            raise ValueError(f"解析方法未实现: {ext}")

        logger.info(f"解析文件: {file_path} (格式: {ext})")
        return parser_method(str(path))

    def parse_resume(self, file_path: str) -> CandidateInfo:
        """解析简历文件，提取结构化信息"""
        raw_text = self.parse_file(file_path)
        candidate = self._extract_candidate_info(raw_text)
        candidate.raw_text = raw_text
        candidate.metadata['source_file'] = file_path
        return candidate

    def parse_interview(self, file_path: str) -> InterviewRecord:
        """解析面试记录文件"""
        raw_text = self.parse_file(file_path)
        record = self._extract_interview_info(raw_text)
        record.raw_text = raw_text
        record.metadata['source_file'] = file_path
        return record

    def _parse_pdf(self, file_path: str) -> str:
        """解析PDF文件"""
        if not HAS_PDF:
            raise ImportError("缺少 PyPDF2 依赖，请使用 pip 安装 pypdf2")

        text_parts = []
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return '\n\n'.join(text_parts)

    def _parse_docx(self, file_path: str) -> str:
        """解析DOCX文件"""
        if not HAS_DOCX:
            raise ImportError("缺少 python-docx 依赖，请使用 pip 安装")

        doc = Document(file_path)
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        return '\n\n'.join(text_parts)

    def _parse_text(self, file_path: str) -> str:
        """解析纯文本文件"""
        for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"无法识别文件编码: {file_path}")

    def _parse_json(self, file_path: str) -> str:
        """解析JSON文件，转换为可读文本"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _parse_yaml(self, file_path: str) -> str:
        """解析YAML文件，转换为可读文本"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)

    def _extract_candidate_info(self, text: str) -> CandidateInfo:
        """从文本中提取候选人基本信息"""
        info = CandidateInfo()
        info.candidate_id = f"CAND_{hash(text) % 100000:05d}"

        # 提取工作年限
        exp_patterns = [
            r'(\d+)[\s\-]*年.*?(?:工作|开发|从业)',
            r'(?:工作|从业).*?(\d+)[\s\-]*年',
            r'(\d+)\s*years?\s*(?:of\s*)?experience',
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info.years_of_experience = float(match.group(1))
                break

        # 提取技能
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'Go', 'Rust', 'C++', 'TypeScript',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
            'TensorFlow', 'PyTorch', 'Kubernetes', 'Docker', 'AWS', 'Azure',
            'SQL', 'MongoDB', 'Redis', 'Kafka', 'Elasticsearch', 'GraphQL',
            'LangChain', 'RAG', 'LLM', 'Prompt Engineering', 'Fine-tuning',
        ]
        info.skills = [kw for kw in skill_keywords if kw.lower() in text.lower()]

        return info

    def _extract_interview_info(self, text: str) -> InterviewRecord:
        """从文本中提取面试记录信息"""
        record = InterviewRecord()

        # 尝试提取日期
        date_patterns = [
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                record.interview_date = match.group(1)
                break

        # 提取Q&A对
        qa_pattern = r'(?:Q|问|问题)[:：\s]*\d*[:：]?\s*(.+?)\s*(?:A|答|回答)[:：\s]*(.+?)(?=(?:Q|问|问题)|$)'
        for match in re.finditer(qa_pattern, text, re.DOTALL | re.IGNORECASE):
            record.questions_and_answers.append({
                'question': match.group(1).strip(),
                'answer': match.group(2).strip(),
            })

        return record

    def parse_batch(self, file_paths: List[str]) -> Dict[str, CandidateInfo]:
        """批量解析简历文件"""
        results = {}
        for fp in file_paths:
            try:
                results[fp] = self.parse_resume(fp)
            except Exception as e:
                logger.error(f"解析失败 {fp}: {e}")
                results[fp] = None
        return results