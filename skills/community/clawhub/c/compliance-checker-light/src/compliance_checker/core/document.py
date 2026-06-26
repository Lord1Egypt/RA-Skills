"""
文档数据模型 (Pydantic v2)

定义文档的数据结构。
注意：此文件只包含数据模型定义和数据访问方法，不包含业务逻辑。
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """文档类型枚举"""

    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    IMAGE = "image"
    UNKNOWN = "unknown"


class PageContent(BaseModel):
    """单页内容"""

    page_num: int = Field(description="页码（从0开始）")
    text: str = Field(default="", description="页面文本内容")
    ocr_text: Optional[str] = Field(default=None, description="OCR识别文本（扫描件）")
    has_text_layer: bool = Field(default=True, description="是否有文本层")

    def get_full_text(self) -> str:
        """获取完整文本（优先使用OCR结果）"""
        if self.ocr_text:
            return self.ocr_text
        return self.text


class DocumentMetadata(BaseModel):
    """文档元数据"""

    title: Optional[str] = Field(default=None, description="文档标题")
    author: Optional[str] = Field(default=None, description="作者")
    subject: Optional[str] = Field(default=None, description="主题")
    creator: Optional[str] = Field(default=None, description="创建工具")
    producer: Optional[str] = Field(default=None, description="生成工具")
    creation_date: Optional[datetime] = Field(default=None, description="创建日期")
    modification_date: Optional[datetime] = Field(default=None, description="修改日期")
    issue_date: Optional[str] = Field(default=None, description="签发日期（从内容提取）")
    valid_from: Optional[str] = Field(default=None, description="有效期开始")
    valid_to: Optional[str] = Field(default=None, description="有效期结束")
    document_number: Optional[str] = Field(default=None, description="文件编号")
    custom: Dict[str, Any] = Field(default_factory=dict, description="自定义元数据")


class Document(BaseModel):
    """
    文档对象模型

    属性:
        path: 文件绝对路径
        name: 文件名
        type: 文件类型
        pages: 页数
        pages_content: 各页内容列表
        metadata: 文档元数据
        content: 原始文本内容（所有页面合并）
    """

    path: str = Field(description="文件绝对路径")
    name: str = Field(description="文件名")
    type: DocumentType = Field(default=DocumentType.UNKNOWN, description="文件类型")
    pages: int = Field(default=0, description="页数")
    pages_content: List[PageContent] = Field(default_factory=list, description="各页内容列表")
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata, description="文档元数据")

    @property
    def content(self) -> str:
        """获取所有页面的合并文本"""
        texts = []
        for page in sorted(self.pages_content, key=lambda p: p.page_num):
            texts.append(page.get_full_text())
        return "\n\n".join(texts)

    def get_page(self, page_num: int) -> Optional[PageContent]:
        """获取指定页码的内容"""
        for page in self.pages_content:
            if page.page_num == page_num:
                return page
        return None

    def get_page_text(self, page_num: int) -> str:
        """获取指定页码的文本内容"""
        page = self.get_page(page_num)
        if page:
            return page.get_full_text()
        return ""

    def search_text(self, keyword: str) -> List[int]:
        """搜索关键词，返回包含关键词的页码列表"""
        matched_pages = []
        for page in self.pages_content:
            if keyword in page.get_full_text():
                matched_pages.append(page.page_num)
        return matched_pages


class ParseResult(BaseModel):
    """文档解析结果"""

    documents: List[Document] = Field(default_factory=list, description="解析成功的文档列表")
    errors: List[Dict[str, str]] = Field(default_factory=list, description="解析错误列表")

    def add_document(self, document: Document) -> None:
        """添加解析成功的文档"""
        self.documents.append(document)

    def add_error(self, file_path: str, error_message: str) -> None:
        """添加解析错误"""
        self.errors.append({"file_path": file_path, "error": error_message})

    def is_success(self) -> bool:
        """是否全部解析成功"""
        return len(self.errors) == 0

    def get_document_by_name(self, name: str) -> Optional[Document]:
        """根据文件名获取文档"""
        for doc in self.documents:
            if doc.name == name:
                return doc
        return None
