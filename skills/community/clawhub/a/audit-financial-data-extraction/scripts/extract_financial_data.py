#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审计报告财务数据自动提取与计算工具
功能：从2025年度审计报告PDF中自动提取数据，并计算各项财务指标，区分合并报表和母公司报表
用于招投标填列
Author: RongClaw 团队
Version: 1.1.0
Date: 2026-07-15
"""

import re
import argparse
import pandas as pd
from pathlib import Path


class FinancialDataExtractor:
    """财务数据提取器"""

    def __init__(self):
        # 需要提取的基础指标定义
        self.base_metrics = [
            {
                'name': '主营业务收入',
                'patterns': {
                    '合并': [
                        r'合并.*主营业务收入.*?([\d,\.]+)',
                        r'主营业务收入.*?合并.*?([\d,\.]+)',
                        r'营业收入.*?合并.*?([\d,\.]+)',
                        r'合并.*营业收入.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*主营业务收入.*?([\d,\.]+)',
                        r'主营业务收入.*?(公司|母公司).*?([\d,\.]+)',
                        r'营业收入.*?(公司|母公司).*?([\d,\.]+)',
                        r'(公司|母公司).*营业收入.*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '主营业务成本',
                'patterns': {
                    '合并': [
                        r'合并.*主营业务成本.*?([\d,\.]+)',
                        r'主营业务成本.*?合并.*?([\d,\.]+)',
                        r'营业成本.*?合并.*?([\d,\.]+)',
                        r'合并.*营业成本.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*主营业务成本.*?([\d,\.]+)',
                        r'主营业务成本.*?(公司|母公司).*?([\d,\.]+)',
                        r'营业成本.*?(公司|母公司).*?([\d,\.]+)',
                        r'(公司|母公司).*营业成本.*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '营业利润',
                'patterns': {
                    '合并': [
                        r'合并.*营业利润.*?([\d,\.]+)',
                        r'营业利润.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*营业利润.*?([\d,\.]+)',
                        r'营业利润.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '净利润',
                'patterns': {
                    '合并': [
                        r'合并.*净利润.*?([\d,\.]+)',
                        r'净利润.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*净利润.*?([\d,\.]+)',
                        r'净利润.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '资产总额',
                'patterns': {
                    '合并': [
                        r'合并.*资产总计.*?([\d,\.]+)',
                        r'合并.*资产总额.*?([\d,\.]+)',
                        r'资产总计.*?合并.*?([\d,\.]+)',
                        r'资产总额.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*资产总计.*?([\d,\.]+)',
                        r'(公司|母公司).*资产总额.*?([\d,\.]+)',
                        r'资产总计.*?(公司|母公司).*?([\d,\.]+)',
                        r'资产总额.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '负债总额',
                'patterns': {
                    '合并': [
                        r'合并.*负债总计.*?([\d,\.]+)',
                        r'合并.*负债总额.*?([\d,\.]+)',
                        r'负债总计.*?合并.*?([\d,\.]+)',
                        r'负债总额.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*负债总计.*?([\d,\.]+)',
                        r'(公司|母公司).*负债总额.*?([\d,\.]+)',
                        r'负债总计.*?(公司|母公司).*?([\d,\.]+)',
                        r'负债总额.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '流动资产',
                'patterns': {
                    '合并': [
                        r'合并.*流动资产合计.*?([\d,\.]+)',
                        r'流动资产合计.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*流动资产合计.*?([\d,\.]+)',
                        r'流动资产合计.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '流动负债',
                'patterns': {
                    '合并': [
                        r'合并.*流动负债合计.*?([\d,\.]+)',
                        r'流动负债合计.*?合并.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*流动负债合计.*?([\d,\.]+)',
                        r'流动负债合计.*?(公司|母公司).*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '经营活动现金流量净额',
                'patterns': {
                    '合并': [
                        r'合并.*经营活动.*现金流量净额.*?([\d,\.]+)',
                        r'经营活动产生的现金流量净额.*?合并.*?([\d,\.]+)',
                        r'合并.*经营活动产生的现金流量净额.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'(公司|母公司).*经营活动.*现金流量净额.*?([\d,\.]+)',
                        r'经营活动产生的现金流量净额.*?(公司|母公司).*?([\d,\.]+)',
                        r'(公司|母公司).*经营活动产生的现金流量净额.*?([\d,\.]+)'
                    ]
                }
            },
            # 上期数据用于增长率计算
            {
                'name': '上期主营业务收入',
                'patterns': {
                    '合并': [
                        r'上期.*合并.*主营业务收入.*?([\d,\.]+)',
                        r'上年.*合并.*主营业务收入.*?([\d,\.]+)',
                        r'上期.*合并.*营业收入.*?([\d,\.]+)',
                        r'上年.*合并.*营业收入.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'上期.*(公司|母公司).*主营业务收入.*?([\d,\.]+)',
                        r'上年.*(公司|母公司).*主营业务收入.*?([\d,\.]+)',
                        r'上期.*(公司|母公司).*营业收入.*?([\d,\.]+)',
                        r'上年.*(公司|母公司).*营业收入.*?([\d,\.]+)'
                    ]
                }
            },
            {
                'name': '上期资产总额',
                'patterns': {
                    '合并': [
                        r'上期.*合并.*资产总计.*?([\d,\.]+)',
                        r'上年.*合并.*资产总计.*?([\d,\.]+)',
                        r'期初.*合并.*资产总计.*?([\d,\.]+)'
                    ],
                    '母公司': [
                        r'上期.*(公司|母公司).*资产总计.*?([\d,\.]+)',
                        r'上年.*(公司|母公司).*资产总计.*?([\d,\.]+)',
                        r'期初.*(公司|母公司).*资产总计.*?([\d,\.]+)'
                    ]
                }
            }
        ]

        # 需要计算的衍生指标
        self.derived_metrics = [
            {
                'name': '毛利率',
                'formula': lambda data, scope: ((data[f'{scope}_主营业务收入'] - data[f'{scope}_主营业务成本']) / data[f'{scope}_主营业务收入'] * 100 if data[f'{scope}_主营业务收入'] and data[f'{scope}_主营业务收入'] != 0 else None),
                'unit': '%'
            },
            {
                'name': '净利润率',
                'formula': lambda data, scope: (data[f'{scope}_净利润'] / data[f'{scope}_主营业务收入'] * 100 if data[f'{scope}_主营业务收入'] and data[f'{scope}_主营业务收入'] != 0 else None),
                'unit': '%'
            },
            {
                'name': '资产负债率',
                'formula': lambda data, scope: (data[f'{scope}_负债总额'] / data[f'{scope}_资产总额'] * 100 if data[f'{scope}_资产总额'] and data[f'{scope}_资产总额'] != 0 else None),
                'unit': '%'
            },
            {
                'name': '流动比率',
                'formula': lambda data, scope: (data[f'{scope}_流动资产'] / data[f'{scope}_流动负债'] if data[f'{scope}_流动负债'] and data[f'{scope}_流动负债'] != 0 else None),
                'unit': ''
            },
            {
                'name': '总资产增长率',
                'formula': lambda data, scope: ((data[f'{scope}_资产总额'] - data[f'{scope}_上期资产总额']) / data[f'{scope}_上期资产总额'] * 100 if data[f'{scope}_上期资产总额'] and data[f'{scope}_上期资产总额'] != 0 else None),
                'unit': '%'
            },
            {
                'name': '营业收入增长率',
                'formula': lambda data, scope: ((data[f'{scope}_主营业务收入'] - data[f'{scope}_上期主营业务收入']) / data[f'{scope}_上期主营业务收入'] * 100 if data[f'{scope}_上期主营业务收入'] and data[f'{scope}_上期主营业务收入'] != 0 else None),
                'unit': '%'
            }
        ]

    def _parse_number(self, num_str):
        """解析数字，处理千分位逗号"""
        if not num_str:
            return None
        # 移除千分位逗号
        num_str = num_str.replace(',', '')
        try:
            return float(num_str)
        except:
            return None

    def _extract_by_patterns(self, text, patterns):
        """根据多个正则表达式模式尝试提取数据"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                # 有些模式捕获组在第二个位置
                if len(match.groups()) > 1:
                    num_str = match.groups()[-1]
                else:
                    num_str = match.group(1)
                return self._parse_number(num_str)
        return None

    def extract_from_text(self, text):
        """从文本中提取所有基础数据"""
        data = {}
        for metric in self.base_metrics:
            for scope in ['合并', '母公司']:
                key = f'{scope}_{metric["name"]}'
                value = self._extract_by_patterns(text, metric['patterns'][scope])
                data[key] = value
        return data

    def calculate_derived(self, data):
        """计算所有衍生指标"""
        result = data.copy()
        for scope in ['合并', '母公司']:
            for metric in self.derived_metrics:
                key = f'{scope}_{metric["name"]}'
                try:
                    result[key] = metric['formula'](data, scope)
                except:
                    result[key] = None
        return result

    def to_dataframe(self, data):
        """转换为DataFrame输出"""
        rows = []
        # 整理基础指标
        for metric in self.base_metrics:
            row = {
                '指标类型': '基础数据',
                '指标名称': metric['name'],
                '合并数据': data.get(f'合并_{metric["name"]}'),
                '母公司数据': data.get(f'母公司_{metric["name"]}'),
                '单位': '元（或万元，依审计报告单位）'
            }
            rows.append(row)
        # 整理计算指标
        for metric in self.derived_metrics:
            unit = metric.get('unit', '')
            row = {
                '指标类型': '计算指标',
                '指标名称': metric['name'],
                '合并数据': data.get(f'合并_{metric["name"]}'),
                '母公司数据': data.get(f'母公司_{metric["name"]}'),
                '单位': unit
            }
            rows.append(row)
        # 单独增加经营活动现金流量净额到结果中（它已经是基础数据）
        # 检查是否已经添加
        has_cash = any(r['指标名称'] == '经营活动现金流量净额' for r in rows)
        if not has_cash:
            rows.insert(-len(self.derived_metrics), {
                '指标类型': '基础数据',
                '指标名称': '经营活动现金流量净额',
                '合并数据': data.get('合并_经营活动现金流量净额'),
                '母公司数据': data.get('母公司_经营活动现金流量净额'),
                '单位': '元（或万元，依审计报告单位）'
            })
        df = pd.DataFrame(rows)
        return df

    def process_pdf_text(self, text):
        """完整处理流程：提取+计算+整理"""
        # 提取基础数据
        data = self.extract_from_text(text)
        # 计算衍生指标
        data = self.calculate_derived(data)
        # 转换为DataFrame
        df = self.to_dataframe(data)
        return data, df


def main():
    parser = argparse.ArgumentParser(description='从审计报告文本中自动提取财务数据并计算指标')
    parser.add_argument('input', help='输入文件路径（.txt 或提取好的PDF文本）')
    parser.add_argument('-o', '--output', help='输出Excel文件路径', default='audit_financial_data_result.xlsx')
    args = parser.parse_args()

    # 读取输入文本
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()

    # 提取计算
    extractor = FinancialDataExtractor()
    data, df = extractor.process_pdf_text(text)

    # 保存结果
    df.to_excel(args.output, index=False, sheet_name='财务指标结果')
    print(f"提取计算完成！结果已保存到: {args.output}")
    print("\n提取结果预览：")
    print(df.to_string(index=False))

    # 检查哪些指标未提取到
    missing = df[(df['合并数据'].isna()) & (df['指标类型'] == '基础数据')]
    if not missing.empty:
        print("\n⚠️ 以下合并数据指标未自动提取到，请手工补充：")
        for _, row in missing.iterrows():
            print(f" - {row['指标名称']}")

    missing_company = df[(df['母公司数据'].isna()) & (df['指标类型'] == '基础数据')]
    if not missing_company.empty:
        print("\n⚠️ 以下母公司数据指标未自动提取到，请手工补充：")
        for _, row in missing_company.iterrows():
            print(f" - {row['指标名称']}")


if __name__ == '__main__':
    main()
