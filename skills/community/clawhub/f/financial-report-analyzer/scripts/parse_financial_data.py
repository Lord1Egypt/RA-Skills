#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务数据解析工具
从提取的文本中识别并解析财务数据
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class FinancialDataParser:
    """财务数据解析器"""
    
    # 关键财务指标关键词映射
    METRIC_PATTERNS = {
        # 盈利能力
        "营业收入": ["营业收入", "营业总收入", "销售收入", "营业总收入（元）", "营业收入（元）"],
        "净利润": ["净利润", "归属于母公司股东的净利润", "归母净利润", "归属于上市公司股东的净利润", "净利润（元）"],
        "毛利率": ["毛利率", "销售毛利率", "营业毛利率"],
        "净利率": ["净利率", "销售净利率", "净利润率"],
        "ROE": ["ROE", "净资产收益率", "加权平均净资产收益率", "加权平均净资产收益率（%）"],
        "ROA": ["ROA", "总资产收益率", "总资产报酬率"],
        
        # 成长能力
        "营收增长率": ["营业收入增长率", "营收增长率", "收入增长率", "营业收入同比增长率"],
        "净利润增长率": ["净利润增长率", "利润增长率", "净利润同比增长率"],
        "总资产增长率": ["总资产增长率", "资产增长率"],
        
        # 偿债能力
        "资产负债率": ["资产负债率", "负债比率", "资产负债率（%）"],
        "流动比率": ["流动比率", "流动比率（倍）"],
        "速动比率": ["速动比率", "速动比率（倍）"],
        
        # 运营能力
        "总资产周转率": ["总资产周转率", "总资产周转率（次）"],
        "应收账款周转天数": ["应收账款周转天数", "应收账款周转天数（天）"],
        "存货周转天数": ["存货周转天数", "存货周转天数（天）"],
    }
    
    def __init__(self, text_content: str):
        self.text = text_content
        self.data = {}
        
    def extract_company_info(self) -> Dict:
        """提取公司基本信息"""
        info = {}
        
        # 提取公司名称
        company_patterns = [
            r'([^\n]{2,20}股份有限公司)',
            r'([^\n]{2,20}有限公司)',
            r'公司名称[：:]\s*([^\n]+)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, self.text)
            if match:
                info["company_name"] = match.group(1).strip()
                break
        
        # 提取股票代码
        code_patterns = [
            r'股票代码[：:]\s*(\d{6})',
            r'(\d{6})\s*[股股份]',
            r'(6\d{5}|0\d{5}|3\d{5})',
        ]
        
        for pattern in code_patterns:
            match = re.search(pattern, self.text)
            if match:
                info["stock_code"] = match.group(1)
                break
        
        # 提取报告期
        period_patterns = [
            r'(20\d{2})\s*年[度报]*\s*[报告]*',
            r'报告期[：:]\s*(20\d{2})',
            r'(20\d{2})\s*年度',
        ]
        
        for pattern in period_patterns:
            match = re.search(pattern, self.text)
            if match:
                info["report_period"] = match.group(1)
                break
                
        return info
    
    def extract_financial_metrics(self) -> Dict:
        """提取财务指标数据"""
        metrics = {}
        
        # 数字匹配模式（支持亿、万、元、%）
        number_pattern = r'[-—]?\s*[\d,]+\.?\d*\s*[亿万元%]?'
        
        for metric_name, keywords in self.METRIC_PATTERNS.items():
            for keyword in keywords:
                # 构建匹配模式
                patterns = [
                    rf'{keyword}[\s：:]*({number_pattern})',
                    rf'{keyword}.*?({number_pattern})',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, self.text)
                    if match:
                        value_str = match.group(1).strip()
                        value = self._parse_number(value_str)
                        if value is not None:
                            # 自动检测单位
                            unit = self._auto_detect_unit(value, value_str)
                            metrics[metric_name] = {
                                "value": value,
                                "unit": unit,
                                "raw": value_str
                            }
                            break
                
                if metric_name in metrics:
                    break
        
        return metrics
    
    def _parse_number(self, value_str: str) -> Optional[float]:
        """解析数值字符串"""
        try:
            # 去除空格和逗号
            value_str = value_str.replace(',', '').replace(' ', '')
            
            # 处理百分比
            if '%' in value_str:
                return float(value_str.replace('%', ''))
            
            # 处理单位
            unit_multiplier = 1
            unit_str = ''
            if '亿' in value_str:
                unit_multiplier = 100000000
                unit_str = '亿元'
                value_str = value_str.replace('亿', '')
            elif '万' in value_str:
                unit_multiplier = 10000
                unit_str = '万元'
                value_str = value_str.replace('万', '')
            elif '元' in value_str:
                unit_str = '元'
                value_str = value_str.replace('元', '')
            
            # 处理横线（表示无数据）
            if value_str in ['-', '—', '']:
                return None
            
            value = float(value_str) * unit_multiplier
            return value
            
        except (ValueError, TypeError):
            return None
    
    def _auto_detect_unit(self, value: float, original_str: str) -> str:
        """自动检测数值单位"""
        # 如果原始字符串有单位，优先使用
        if '亿' in original_str:
            return '亿元'
        elif '万' in original_str:
            return '万元'
        elif '%' in original_str:
            return '%'
        elif '元' in original_str:
            return '元'
        
        # 根据数值大小自动判断
        if value > 100000000:
            return '亿元'
        elif value > 10000:
            return '万元'
        elif value < 100:
            return ''  # 可能是比率或百分比
        else:
            return '元'
    
    def _detect_unit(self, value_str: str) -> str:
        """检测数值单位"""
        if '%' in value_str:
            return "%"
        elif '亿' in value_str:
            return "亿元"
        elif '万' in value_str:
            return "万元"
        elif '元' in value_str:
            return "元"
        return ""
    
    def parse(self) -> Dict:
        """执行完整解析"""
        self.data = {
            "company_info": self.extract_company_info(),
            "financial_metrics": self.extract_financial_metrics(),
            "raw_text_length": len(self.text)
        }
        return self.data


def parse_from_file(input_path: str) -> Dict:
    """
    从文件解析财务数据
    
    Args:
        input_path: 输入文件路径（支持.txt或.json）
        
    Returns:
        Dict: 解析后的财务数据
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")
    
    # 根据文件类型读取内容
    if input_path.suffix == '.json':
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = data.get('full_text', '')
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    # 解析数据
    parser = FinancialDataParser(text)
    result = parser.parse()
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parse_financial_data.py <提取的文本文件路径>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        print(f"正在解析: {input_file}")
        data = parse_from_file(input_file)
        
        # 保存结果
        output_path = Path(input_file).stem + "_parsed.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 解析完成")
        print(f"  公司名称: {data['company_info'].get('company_name', '未识别')}")
        print(f"  股票代码: {data['company_info'].get('stock_code', '未识别')}")
        print(f"  报告期: {data['company_info'].get('report_period', '未识别')}")
        print(f"  提取指标数: {len(data['financial_metrics'])}")
        print(f"  输出文件: {output_path}")
        
        # 打印提取的指标
        if data['financial_metrics']:
            print("\n  提取的财务指标:")
            for metric, info in data['financial_metrics'].items():
                print(f"    {metric}: {info['value']}{info['unit']}")
        
    except Exception as e:
        print(f"[ERROR] 解析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
