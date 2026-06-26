"""
PDF文件解析器

支持解析 PDF 格式的财务报告
"""
import re
from typing import Dict, List, Any, Optional, Tuple

from .base_parser import BaseParser, ParseResult, FinancialData, normalize_account_name, extract_number


class PDFParser(BaseParser):
    """
    PDF文件解析器
    
    支持从PDF文档中提取文本和表格数据
    """
    
    name = "pdf_parser"
    description = "PDF文件解析器"
    supported_extensions = ['.pdf']
    supported_software = ['GENERIC']
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.extract_tables = self.config.get('extract_tables', True)
        self.page_range = self.config.get('page_range', None)  # 如 (0, 10) 表示前10页
    
    def can_parse(self, file_path: str) -> bool:
        """检查是否能解析该文件"""
        if not self.validate_file_exists(file_path):
            return False
        
        ext = self.get_file_extension(file_path)
        return ext == '.pdf'
    
    def parse(self, file_path: str) -> ParseResult:
        """解析PDF文件"""
        if not self.can_parse(file_path):
            return self.create_error_result(file_path, "无法解析该文件格式")
        
        try:
            # 尝试使用不同的PDF解析库
            
            # 方法1: 使用 pdfplumber（推荐，支持表格）
            try:
                return self._parse_with_pdfplumber(file_path)
            except ImportError:
                pass
            
            # 方法2: 使用 PyPDF2
            try:
                return self._parse_with_pypdf2(file_path)
            except ImportError:
                pass
            
            # 方法3: 使用 pdfminer
            try:
                return self._parse_with_pdfminer(file_path)
            except ImportError:
                pass
            
            return self.create_error_result(
                file_path,
                "缺少PDF解析库，请安装 pdfplumber 或 PyPDF2 (pip install pdfplumber)"
            )
            
        except Exception as e:
            return self.create_error_result(file_path, f"解析失败: {str(e)}")
    
    def _parse_with_pdfplumber(self, file_path: str) -> ParseResult:
        """使用 pdfplumber 解析PDF"""
        import pdfplumber
        
        result = self.create_success_result(file_path)
        result.file_type = 'PDF'
        result.data = FinancialData()
        result.data.source_file = file_path
        result.data.source_software = 'GENERIC'
        
        with pdfplumber.open(file_path) as pdf:
            # 确定页面范围
            if self.page_range:
                start_page, end_page = self.page_range
                pages = pdf.pages[start_page:end_page]
            else:
                pages = pdf.pages
            
            all_tables = []
            
            for i, page in enumerate(pages):
                # 提取表格
                if self.extract_tables:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            all_tables.append(table)
            
            # 处理提取的表格
            if all_tables:
                self._process_tables(all_tables, result.data, result)
        
        return result
    
    def _parse_with_pypdf2(self, file_path: str) -> ParseResult:
        """使用 PyPDF2 解析PDF"""
        import PyPDF2
        
        result = self.create_success_result(file_path)
        result.file_type = 'PDF'
        result.data = FinancialData()
        result.data.source_file = file_path
        result.data.source_software = 'GENERIC'
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # 确定页面范围
            if self.page_range:
                start_page, end_page = self.page_range
                pages = reader.pages[start_page:end_page]
            else:
                pages = reader.pages
            
            text_content = []
            
            for page in pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
            
            # 合并文本
            full_text = '\n'.join(text_content)
            result.data.raw_data['text_content'] = full_text
            
            # 尝试从文本中提取财务数据
            self._extract_from_text(full_text, result.data, result)
        
        return result
    
    def _parse_with_pdfminer(self, file_path: str) -> ParseResult:
        """使用 pdfminer 解析PDF"""
        from pdfminer.high_level import extract_text
        
        result = self.create_success_result(file_path)
        result.file_type = 'PDF'
        result.data = FinancialData()
        result.data.source_file = file_path
        result.data.source_software = 'GENERIC'
        
        # 提取文本
        text = extract_text(file_path)
        result.data.raw_data['text_content'] = text
        
        # 尝试从文本中提取财务数据
        self._extract_from_text(text, result.data, result)
        
        return result
    
    def _process_tables(self, tables: List[List], data: FinancialData, result: ParseResult):
        """处理提取的表格"""
        for i, table in enumerate(tables):
            # 识别表格类型
            table_type = self._identify_table_type(table)
            
            parsed_data = self._parse_table_data(table)
            
            if table_type == 'balance_sheet':
                data.balance_sheet.update(parsed_data)
                result.add_warning(f"表格{i+1}识别为资产负债表")
            elif table_type == 'income_statement':
                data.income_statement.update(parsed_data)
                result.add_warning(f"表格{i+1}识别为利润表")
            elif table_type == 'cash_flow':
                data.cash_flow.update(parsed_data)
                result.add_warning(f"表格{i+1}识别为现金流量表")
            else:
                data.raw_data[f'table_{i+1}'] = parsed_data
    
    def _identify_table_type(self, table: List[List]) -> str:
        """识别表格类型"""
        sample_text = ' '.join([' '.join([str(cell) for cell in row]) for row in table[:5]])
        sample_text = sample_text.lower()
        
        if any(kw in sample_text for kw in ['资产', '负债', 'asset', 'liability']):
            return 'balance_sheet'
        
        if any(kw in sample_text for kw in ['收入', '成本', '利润', 'revenue', 'profit']):
            return 'income_statement'
        
        if any(kw in sample_text for kw in ['现金', '流量', 'cash', 'flow']):
            return 'cash_flow'
        
        return 'unknown'
    
    def _parse_table_data(self, table: List[List]) -> Dict[str, float]:
        """解析表格数据"""
        data = {}
        
        for row in table:
            if not row or len(row) < 2:
                continue
            
            # 第一列通常是科目名称
            account_name = str(row[0]) if row[0] else ""
            account_name = account_name.strip()
            
            if not account_name:
                continue
            
            # 跳过标题行
            if any(kw in account_name for kw in ['项目', '科目', 'Item', 'Account']):
                continue
            
            standard_name = normalize_account_name(account_name)
            
            # 查找数值
            for cell in reversed(row[1:]):
                value = extract_number(cell)
                if value is not None:
                    data[standard_name] = value
                    break
        
        return data
    
    def _extract_from_text(self, text: str, data: FinancialData, result: ParseResult):
        """从文本中提取财务数据"""
        # 尝试使用正则表达式提取关键财务指标
        
        # 提取营业收入
        revenue_patterns = [
            r'营业收入[\s:：]+([\d,\.]+)',
            r'Revenue[\s:：]+\$?([\d,\.]+)',
        ]
        
        for pattern in revenue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = extract_number(match.group(1))
                if value:
                    data.income_statement['营业收入'] = value
                    break
        
        # 提取净利润
        profit_patterns = [
            r'净利润[\s:：]+([\d,\.]+)',
            r'Net Profit[\s:：]+\$?([\d,\.]+)',
        ]
        
        for pattern in profit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = extract_number(match.group(1))
                if value:
                    data.income_statement['净利润'] = value
                    break
        
        # 提取总资产
        assets_patterns = [
            r'资产总计[\s:：]+([\d,\.]+)',
            r'Total Assets[\s:：]+\$?([\d,\.]+)',
        ]
        
        for pattern in assets_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = extract_number(match.group(1))
                if value:
                    data.balance_sheet['资产总计'] = value
                    break


__all__ = ['PDFParser']
