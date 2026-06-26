#!/usr/bin/env python3
"""
整合查询脚本 - 同时查询天眼查、企查查和裁判文书网

使用方法:
    python scripts/query_all.py "公司名称"
    python scripts/query_all.py "公司名称" --output result.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from query_tianyancha import TianyanchaQuery
from query_qichacha import QichachaQuery
from query_wenshu import WenshuQuery


def merge_data(tianyancha_data: Dict, qichacha_data: Dict, wenshu_data: Dict) -> Dict:
    """合并天眼查、企查查和裁判文书网数据"""
    merged = {
        'query_time': datetime.now().isoformat(),
        'sources': [],
        'tianyancha': tianyancha_data,
        'qichacha': qichacha_data,
        'wenshu': wenshu_data,
    }
    
    # 记录数据来源
    if tianyancha_data.get('success'):
        merged['sources'].append('天眼查')
    if qichacha_data.get('success'):
        merged['sources'].append('企查查')
    if wenshu_data.get('success'):
        merged['sources'].append('裁判文书网')
    
    # 合并基本信息（优先使用非空值）
    basic_fields = [
        'name', '法定代表人', '注册资本', '实缴资本', '成立日期',
        '经营状态', '统一社会信用代码', '纳税人识别号', '注册号',
        '组织机构代码', '企业类型', '行业', '核准日期', '登记机关',
        '注册地址', '经营范围', '营业期限', '英文名称', '曾用名', '参保人数'
    ]
    
    for field in basic_fields:
        value = None
        
        # 优先使用天眼查的数据
        if tianyancha_data.get(field):
            value = tianyancha_data[field]
        elif qichacha_data.get(field):
            value = qichacha_data[field]
        
        if value:
            merged[field] = value
    
    # 合并 URL
    urls = []
    if tianyancha_data.get('url'):
        urls.append({'source': '天眼查', 'url': tianyancha_data['url']})
    if qichacha_data.get('url'):
        urls.append({'source': '企查查', 'url': qichacha_data['url']})
    if wenshu_data.get('search_url'):
        urls.append({'source': '裁判文书网', 'url': wenshu_data['search_url']})
    
    if urls:
        merged['urls'] = urls
    
    # 合并股东信息
    if tianyancha_data.get('shareholders') or qichacha_data.get('shareholders'):
        tianyancha_count = len(tianyancha_data.get('shareholders', []))
        qichacha_count = len(qichacha_data.get('shareholders', []))
        
        if tianyancha_count >= qichacha_count:
            merged['shareholders'] = tianyancha_data.get('shareholders', [])
        else:
            merged['shareholders'] = qichacha_data.get('shareholders', [])
        
        merged['shareholder_count'] = len(merged['shareholders'])
    
    # 合并主要人员
    if tianyancha_data.get('key_persons') or qichacha_data.get('key_persons'):
        tianyancha_count = len(tianyancha_data.get('key_persons', []))
        qichacha_count = len(qichacha_data.get('key_persons', []))
        
        if tianyancha_count >= qichacha_count:
            merged['key_persons'] = tianyancha_data.get('key_persons', [])
        else:
            merged['key_persons'] = qichacha_data.get('key_persons', [])
        
        merged['key_person_count'] = len(merged['key_persons'])
    
    # 合并对外投资
    if tianyancha_data.get('investments') or qichacha_data.get('investments'):
        tianyancha_count = len(tianyancha_data.get('investments', []))
        qichacha_count = len(qichacha_data.get('investments', []))
        
        if tianyancha_count >= qichacha_count:
            merged['investments'] = tianyancha_data.get('investments', [])
        else:
            merged['investments'] = qichacha_data.get('investments', [])
        
        merged['investment_count'] = len(merged['investments'])
    
    # 企查查的风险信息
    if qichacha_data.get('risks'):
        merged['risks'] = qichacha_data['risks']
    
    # 裁判文书网的诉讼信息
    if wenshu_data.get('success'):
        merged['litigation'] = {
            'cases': wenshu_data.get('cases', []),
            'case_count': wenshu_data.get('case_count', 0),
            'statistics': wenshu_data.get('statistics', {}),
        }
    
    # 统计信息
    merged['success'] = len(merged['sources']) > 0
    merged['source_count'] = len(merged['sources'])
    
    return merged


def query_all(company_name: str, headless: bool = True, include_wenshu: bool = True) -> Dict:
    """同时查询天眼查、企查查和裁判文书网"""
    
    print("=" * 60)
    print(f"整合查询: {company_name}")
    print("=" * 60)
    print()
    
    tianyancha_data = {}
    qichacha_data = {}
    wenshu_data = {}
    
    # 查询天眼查
    print("【1/3】查询天眼查...")
    try:
        query = TianyanchaQuery(headless=headless)
        tianyancha_data = query.query(company_name)
    except Exception as e:
        print(f"天眼查查询失败: {e}")
        tianyancha_data = {'error': str(e)}
    
    print()
    
    # 查询企查查
    print("【2/3】查询企查查...")
    try:
        query = QichachaQuery(headless=headless)
        qichacha_data = query.query(company_name)
    except Exception as e:
        print(f"企查查查询失败: {e}")
        qichacha_data = {'error': str(e)}
    
    print()
    
    # 查询裁判文书网
    if include_wenshu:
        print("【3/3】查询裁判文书网...")
        try:
            query = WenshuQuery(headless=headless)
            wenshu_data = query.query(company_name)
        except Exception as e:
            print(f"裁判文书网查询失败: {e}")
            wenshu_data = {'error': str(e)}
    else:
        print("【3/3】跳过裁判文书网查询")
        wenshu_data = {}
    
    print()
    
    # 合并数据
    print("合并数据...")
    merged = merge_data(tianyancha_data, qichacha_data, wenshu_data)
    
    print(f"✓ 整合完成，数据来源: {', '.join(merged['sources'])}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="整合查询天眼查、企查查和裁判文书网")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器")
    parser.add_argument("--skip-wenshu", action="store_true", help="跳过裁判文书网查询")

    args = parser.parse_args()

    result = query_all(
        args.company, 
        headless=not args.no_headless,
        include_wenshu=not args.skip_wenshu
    )

    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n结果已保存: {args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
