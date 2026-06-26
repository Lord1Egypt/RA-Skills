"""
解析器基类模块

定义文件解析器的抽象基类和数据模型
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, BinaryIO, Union
from pathlib import Path
from datetime import datetime
import os


@dataclass
class FinancialData:
    """标准化财务数据结构"""
    
    # 基本信息
    company_name: str = ""
    tax_id: str = ""
    report_period: str = ""  # 报表期间，如 "2024年度"
    report_date: str = ""    # 报表日期
    currency: str = "CNY"
    
    # 资产负债表数据
    balance_sheet: Dict[str, float] = field(default_factory=dict)
    
    # 利润表数据
    income_statement: Dict[str, float] = field(default_factory=dict)
    
    # 现金流量表数据
    cash_flow: Dict[str, float] = field(default_factory=dict)
    
    # 附注信息
    notes: Dict[str, Any] = field(default_factory=dict)
    
    # 原始数据（保留原始解析结果）
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    # 数据来源信息
    source_file: str = ""
    source_software: str = ""  # 金蝶、用友等
    parser_version: str = "1.0"
    
    def get_ratio(self, numerator: str, denominator: str) -> Optional[float]:
        """计算财务比率"""
        num = self.balance_sheet.get(numerator) or self.income_statement.get(numerator)
        den = self.balance_sheet.get(denominator) or self.income_statement.get(denominator)
        
        if num is not None and den is not None and den != 0:
            return num / den
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'company_name': self.company_name,
            'tax_id': self.tax_id,
            'report_period': self.report_period,
            'report_date': self.report_date,
            'currency': self.currency,
            'balance_sheet': self.balance_sheet,
            'income_statement': self.income_statement,
            'cash_flow': self.cash_flow,
            'notes': self.notes,
            'source_file': self.source_file,
            'source_software': self.source_software,
            'parser_version': self.parser_version,
        }


@dataclass
class ParseResult:
    """文件解析结果"""
    
    success: bool
    file_path: str
    file_type: str = ""           # 文件类型
    software_type: str = ""       # 财务软件类型
    data: FinancialData = field(default_factory=FinancialData)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    parsed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_error(self, error: str):
        """添加错误信息"""
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str):
        """添加警告信息"""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'success': self.success,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'software_type': self.software_type,
            'data': self.data.to_dict() if self.data else None,
            'errors': self.errors,
            'warnings': self.warnings,
            'parsed_at': self.parsed_at,
        }


class BaseParser(ABC):
    """
    文件解析器基类
    
    所有具体解析器应继承此类并实现 parse 方法
    """
    
    # 解析器信息
    name: str = "base_parser"
    description: str = "基础解析器"
    supported_extensions: List[str] = []
    supported_software: List[str] = []
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化解析器
        
        Args:
            config: 解析器配置参数
        """
        self.config = config or {}
        self.encoding = self.config.get('encoding', 'utf-8')
        self.debug = self.config.get('debug', False)
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """
        检查是否能解析该文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否能解析
        """
        pass
    
    @abstractmethod
    def parse(self, file_path: str) -> ParseResult:
        """
        解析文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            ParseResult: 解析结果
        """
        pass
    
    def validate_file_exists(self, file_path: str) -> bool:
        """验证文件是否存在"""
        if not os.path.exists(file_path):
            return False
        if not os.path.isfile(file_path):
            return False
        return True
    
    def get_file_extension(self, file_path: str) -> str:
        """获取文件扩展名（小写）"""
        return Path(file_path).suffix.lower()
    
    def create_success_result(self, file_path: str) -> ParseResult:
        """创建成功结果"""
        return ParseResult(
            success=True,
            file_path=file_path,
            file_type=self.name
        )
    
    def create_error_result(self, file_path: str, error: str) -> ParseResult:
        """创建错误结果"""
        result = ParseResult(
            success=False,
            file_path=file_path,
            file_type=self.name
        )
        result.add_error(error)
        return result


# 标准科目映射表（用于标准化不同软件的科目名称）
STANDARD_ACCOUNT_MAPPING = {
    # 资产负债表 - 资产
    '货币资金': ['货币资金', '现金及现金等价物', 'Cash', 'cash', '银行存款'],
    '交易性金融资产': ['交易性金融资产', '以公允价值计量且其变动计入当期损益的金融资产'],
    '应收账款': ['应收账款', '应收帐款', 'Accounts Receivable', 'trade_receivables'],
    '预付款项': ['预付款项', '预付账款', '预付帐款', 'Prepayments'],
    '其他应收款': ['其他应收款', '其他应收帐款', 'Other Receivables'],
    '存货': ['存货', 'Inventory', '库存商品'],
    '流动资产合计': ['流动资产合计', 'Current Assets', '流动资产总计'],
    '固定资产': ['固定资产', 'Fixed Assets', 'property_plant_equipment'],
    '无形资产': ['无形资产', 'Intangible Assets'],
    '资产总计': ['资产总计', '资产合计', '资产总额', 'Total Assets', '总资产'],
    
    # 资产负债表 - 负债
    '短期借款': ['短期借款', 'Short-term Borrowings'],
    '应付账款': ['应付账款', '应付帐款', 'Accounts Payable', 'trade_payables'],
    '预收款项': ['预收款项', '预收账款', '预收帐款', 'Contract Liabilities'],
    '应付职工薪酬': ['应付职工薪酬', '应付工资', 'Salaries Payable'],
    '应交税费': ['应交税费', '应交税金', 'Taxes Payable'],
    '其他应付款': ['其他应付款', '其他应付帐款', 'Other Payables'],
    '流动负债合计': ['流动负债合计', 'Current Liabilities', '流动负债总计'],
    '长期借款': ['长期借款', 'Long-term Borrowings'],
    '负债合计': ['负债合计', '负债总计', '负债总额', 'Total Liabilities', '总负债'],
    
    # 资产负债表 - 权益
    '实收资本': ['实收资本', '股本', 'Paid-in Capital', 'Share Capital'],
    '资本公积': ['资本公积', 'Capital Reserve', '资本公积金'],
    '未分配利润': ['未分配利润', 'Undistributed Profit', 'Retained Earnings'],
    '所有者权益合计': ['所有者权益合计', '股东权益合计', 'Total Equity', '净资产'],
    
    # 利润表
    '营业收入': ['营业收入', '主营业务收入', 'Revenue', 'Sales', '收入'],
    '营业成本': ['营业成本', '主营业务成本', 'Cost of Sales', 'COGS'],
    '税金及附加': ['税金及附加', '营业税金及附加', 'Taxes and Surcharges'],
    '销售费用': ['销售费用', '营业费用', 'Selling Expenses'],
    '管理费用': ['管理费用', 'General and Administrative Expenses', '管理成本'],
    '研发费用': ['研发费用', '研究费用', 'R&D Expenses', '研发支出'],
    '财务费用': ['财务费用', 'Finance Costs', 'Financial Expenses'],
    '营业利润': ['营业利润', 'Operating Profit', 'Operating Income'],
    '利润总额': ['利润总额', 'Total Profit', 'Profit Before Tax'],
    '所得税费用': ['所得税费用', '所得税', 'Income Tax Expense'],
    '净利润': ['净利润', 'Net Profit', 'Net Income'],
    
    # 现金流量表
    '销售商品收到的现金': ['销售商品、提供劳务收到的现金', '销售商品提供劳务收到的现金'],
    '经营活动现金流': ['经营活动产生的现金流量净额', '经营活动现金流量净额'],
    '投资活动现金流': ['投资活动产生的现金流量净额', '投资活动现金流量净额'],
    '筹资活动现金流': ['筹资活动产生的现金流量净额', '筹资活动现金流量净额'],
}


def normalize_account_name(account_name: str) -> str:
    """
    标准化科目名称
    
    Args:
        account_name: 原始科目名称
        
    Returns:
        str: 标准化后的科目名称
    """
    if not account_name:
        return ""
    
    # 清理科目名称
    cleaned = account_name.strip()
    cleaned = cleaned.replace(' ', '')
    cleaned = cleaned.replace('　', '')
    cleaned = cleaned.replace('\n', '')
    cleaned = cleaned.replace('\t', '')
    
    # 查找标准名称
    for standard_name, aliases in STANDARD_ACCOUNT_MAPPING.items():
        if cleaned in aliases or cleaned == standard_name:
            return standard_name
    
    return cleaned


def extract_number(value: Any) -> Optional[float]:
    """
    从各种格式中提取数值
    
    Args:
        value: 原始值
        
    Returns:
        float: 提取的数值，失败返回 None
    """
    if value is None:
        return None
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # 移除千分位分隔符
        value = value.replace(',', '')
        value = value.replace('，', '')
        # 移除货币符号
        value = value.replace('¥', '')
        value = value.replace('$', '')
        value = value.replace('元', '')
        value = value.strip()
        
        # 处理括号表示的负数 (1000) -> -1000
        if value.startswith('(') and value.endswith(')'):
            value = '-' + value[1:-1]
        
        # 处理负号
        if value.endswith('-'):
            value = '-' + value[:-1]
        
        try:
            return float(value)
        except ValueError:
            return None
    
    return None


__all__ = [
    'BaseParser',
    'ParseResult',
    'FinancialData',
    'STANDARD_ACCOUNT_MAPPING',
    'normalize_account_name',
    'extract_number',
]
