"""
CSV文件解析器

支持解析 CSV 格式的财务数据
"""
import csv
import io
from typing import Dict, List, Any, Optional

from .base_parser import BaseParser, ParseResult, FinancialData, normalize_account_name, extract_number


class CSVParser(BaseParser):
    """
    CSV文件解析器
    
    支持各种分隔符和编码格式
    """
    
    name = "csv_parser"
    description = "CSV文件解析器"
    supported_extensions = ['.csv']
    supported_software = ['GENERIC', 'UFIDA']
    
    # 常见编码
    ENCODINGS = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'latin-1']
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.delimiter = self.config.get('delimiter', None)  # None表示自动检测
        self.encoding = self.config.get('encoding', None)    # None表示自动检测
    
    def can_parse(self, file_path: str) -> bool:
        """检查是否能解析该文件"""
        if not self.validate_file_exists(file_path):
            return False
        
        ext = self.get_file_extension(file_path)
        return ext == '.csv'
    
    def parse(self, file_path: str) -> ParseResult:
        """解析CSV文件"""
        if not self.can_parse(file_path):
            return self.create_error_result(file_path, "无法解析该文件格式")
        
        try:
            # 自动检测编码
            encoding = self.encoding or self._detect_encoding(file_path)
            
            # 自动检测分隔符
            delimiter = self.delimiter or self._detect_delimiter(file_path, encoding)
            
            # 读取CSV文件
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                reader = csv.reader(f, delimiter=delimiter)
                rows = list(reader)
            
            if not rows:
                return self.create_error_result(file_path, "CSV文件为空")
            
            result = self.create_success_result(file_path)
            result.file_type = 'CSV'
            result.data = FinancialData()
            result.data.source_file = file_path
            result.data.source_software = 'GENERIC'
            
            # 检测报表类型并解析
            report_type = self._detect_report_type(rows)
            
            if report_type == 'balance_sheet':
                result.data.balance_sheet = self._parse_standard_format(rows)
                result.add_warning("识别为资产负债表格式")
            elif report_type == 'income_statement':
                result.data.income_statement = self._parse_standard_format(rows)
                result.add_warning("识别为利润表格式")
            elif report_type == 'cash_flow':
                result.data.cash_flow = self._parse_standard_format(rows)
                result.add_warning("识别为现金流量表格式")
            elif report_type == 'trial_balance':
                # 科目余额表，可以提取多个报表的数据
                self._parse_trial_balance(rows, result.data)
                result.add_warning("识别为科目余额表格式")
            else:
                # 通用解析
                result.data.raw_data['csv_content'] = self._parse_generic(rows)
                result.add_warning("无法确定报表类型，执行通用解析")
            
            return result
            
        except Exception as e:
            return self.create_error_result(file_path, f"解析失败: {str(e)}")
    
    def _detect_encoding(self, file_path: str) -> str:
        """检测文件编码"""
        for encoding in self.ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1024)  # 读取前1KB测试
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        return 'utf-8'  # 默认使用utf-8
    
    def _detect_delimiter(self, file_path: str, encoding: str) -> str:
        """检测分隔符"""
        with open(file_path, 'r', encoding=encoding) as f:
            sample = f.read(2048)
        
        # 常见分隔符
        delimiters = [',', ';', '\t', '|', '#']
        counts = {}
        
        for delim in delimiters:
            counts[delim] = sample.count(delim)
        
        # 选择出现次数最多的分隔符
        best_delim = max(counts, key=counts.get)
        
        # 如果都没有出现，默认使用逗号
        if counts[best_delim] == 0:
            return ','
        
        return best_delim
    
    def _detect_report_type(self, rows: List[List[str]]) -> str:
        """检测报表类型"""
        # 将所有文本合并进行分析
        all_text = ' '.join([' '.join(row) for row in rows[:20]]).lower()
        
        # 关键字匹配
        if any(kw in all_text for kw in ['科目余额', '科目代码', 'accvouch', 'ledger']):
            return 'trial_balance'
        
        if any(kw in all_text for kw in ['资产', '负债', 'asset', 'liability', 'balance sheet']):
            return 'balance_sheet'
        
        if any(kw in all_text for kw in ['收入', '成本', '利润', 'revenue', 'profit', 'income']):
            return 'income_statement'
        
        if any(kw in all_text for kw in ['现金', '流量', 'cash', 'flow']):
            return 'cash_flow'
        
        return 'unknown'
    
    def _parse_standard_format(self, rows: List[List[str]]) -> Dict[str, float]:
        """解析标准格式的报表"""
        data = {}
        
        for row in rows[1:]:  # 跳过标题行
            if not row or len(row) < 2:
                continue
            
            account_name = row[0].strip() if row[0] else ""
            if not account_name:
                continue
            
            standard_name = normalize_account_name(account_name)
            
            # 查找数值
            for cell in reversed(row[1:]):
                value = extract_number(cell)
                if value is not None:
                    data[standard_name] = value
                    break
        
        return data
    
    def _parse_trial_balance(self, rows: List[List[str]], data: FinancialData):
        """解析科目余额表"""
        # 科目余额表通常包含：科目代码、科目名称、期初余额、本期发生、期末余额
        
        balance_sheet = {}
        income_statement = {}
        
        # 查找标题行
        header_row_idx = 0
        for i, row in enumerate(rows[:5]):
            if any(kw in ' '.join(row).lower() for kw in ['科目', 'account', '名称', 'name']):
                header_row_idx = i
                break
        
        # 确定列索引
        headers = [h.lower() for h in rows[header_row_idx]]
        
        name_col = self._find_column_index(headers, ['科目名称', '名称', 'account name', 'name'])
        end_balance_col = self._find_column_index(headers, ['期末余额', '期末', 'ending balance', 'end balance'])
        
        if name_col is None:
            name_col = 1  # 默认第二列
        
        # 解析数据行
        for row in rows[header_row_idx + 1:]:
            if not row or len(row) <= name_col:
                continue
            
            account_name = row[name_col].strip() if row[name_col] else ""
            if not account_name:
                continue
            
            standard_name = normalize_account_name(account_name)
            
            # 获取期末余额
            value = None
            if end_balance_col is not None and len(row) > end_balance_col:
                value = extract_number(row[end_balance_col])
            else:
                # 尝试最后一列
                value = extract_number(row[-1])
            
            if value is not None:
                # 根据科目类型分类
                if any(kw in standard_name for kw in ['收入', '成本', '费用', '利润', '营业外']):
                    income_statement[standard_name] = value
                else:
                    balance_sheet[standard_name] = value
        
        data.balance_sheet = balance_sheet
        data.income_statement = income_statement
    
    def _find_column_index(self, headers: List[str], keywords: List[str]) -> Optional[int]:
        """查找列索引"""
        for i, header in enumerate(headers):
            for kw in keywords:
                if kw.lower() in header.lower():
                    return i
        return None
    
    def _parse_generic(self, rows: List[List[str]]) -> List[Dict]:
        """通用解析，返回原始数据结构"""
        result = []
        
        if not rows:
            return result
        
        # 使用第一行作为标题
        headers = rows[0]
        
        for row in rows[1:]:
            if len(row) != len(headers):
                continue
            
            row_dict = {}
            for i, value in enumerate(row):
                header = headers[i] if i < len(headers) else f"Column_{i}"
                
                # 尝试转换为数值
                num_value = extract_number(value)
                row_dict[header] = num_value if num_value is not None else value
            
            result.append(row_dict)
        
        return result


__all__ = ['CSVParser']
