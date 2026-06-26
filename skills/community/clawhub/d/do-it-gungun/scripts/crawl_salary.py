#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
do-it 薪资数据抓取脚本
抓取拉勾网/Boss 直聘/猎聘网的薪资数据

使用方法:
    python crawl_salary.py --keyword "财务 BP" --city "深圳"
    python crawl_salary.py --batch  # 批量抓取多个城市

注意: 请遵守网站 robots.txt 和使用条款
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
import argparse

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 目标城市和职位
TARGET_CITIES = ['深圳', '广州', '长沙', '惠州', '上海', '北京', '杭州']
TARGET_ROLES = ['财务 BP', '财务分析', '财务经理', '财务专家', '财务总监']
TARGET_INDUSTRIES = ['跨境电商', '互联网', '物流', '科技']


def crawl_lagou(keyword: str, city: str) -> List[Dict]:
    """
    抓取拉勾网薪资数据
    
    注意：拉勾网有反爬机制，实际使用需要处理登录/验证码
    这里提供框架，实际抓取需要完善
    """
    jobs = []
    
    try:
        # 模拟搜索 URL
        url = f"https://www.lagou.com/jobs/list_{keyword}?city={city}"
        
        # 实际项目中需要处理登录和反爬
        # response = requests.get(url, headers=HEADERS, timeout=10)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # 解析职位信息...
        
        print(f"[拉勾] {city} - {keyword}: 需要登录/反爬处理")
        
    except Exception as e:
        print(f"[拉勾] 抓取失败：{e}")
    
    return jobs


def crawl_boss(keyword: str, city: str) -> List[Dict]:
    """
    抓取 Boss 直聘薪资数据
    
    注意：Boss 直聘反爬严格，需要登录
    """
    jobs = []
    
    try:
        # Boss 直聘需要登录才能查看完整信息
        print(f"[Boss] {city} - {keyword}: 需要登录")
        
    except Exception as e:
        print(f"[Boss] 抓取失败：{e}")
    
    return jobs


def crawl_liepin(keyword: str, city: str) -> List[Dict]:
    """
    抓取猎聘网薪资数据 (中高端职位)
    """
    jobs = []
    
    try:
        print(f"[猎聘] {city} - {keyword}: 需要登录")
        
    except Exception as e:
        print(f"[猎聘] 抓取失败：{e}")
    
    return jobs


def aggregate_salary_data(jobs_list: List[Dict]) -> Dict:
    """
    聚合多源薪资数据，计算统计值
    """
    if not jobs_list:
        return {}
    
    salaries = [job.get('salary', 0) for job in jobs_list if job.get('salary')]
    
    if not salaries:
        return {}
    
    return {
        'min': min(salaries),
        'median': sorted(salaries)[len(salaries)//2],
        'max': max(salaries),
        'avg': sum(salaries) / len(salaries),
        'sample_size': len(salaries)
    }


def save_to_json(data: Dict, filepath: str):
    """保存数据到 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存：{filepath}")


def batch_crawl():
    """批量抓取多个城市/职位的薪资数据"""
    all_data = {
        'meta': {
            'version': '1.0.0',
            'updated_at': datetime.now().strftime('%Y-%m-%d'),
            'source': 'do-it 数据采集'
        },
        'data': []
    }
    
    print("开始批量抓取薪资数据...")
    print(f"城市：{TARGET_CITIES}")
    print(f"职位：{TARGET_ROLES}")
    
    for city in TARGET_CITIES:
        for role in TARGET_ROLES:
            print(f"\n抓取：{city} - {role}")
            
            # 抓取各平台数据
            lagou_jobs = crawl_lagou(role, city)
            boss_jobs = crawl_boss(role, city)
            liepin_jobs = crawl_liepin(role, city)
            
            # 聚合数据
            all_jobs = lagou_jobs + boss_jobs + liepin_jobs
            stats = aggregate_salary_data(all_jobs)
            
            if stats:
                record = {
                    'id': f"{city[:2].upper()}-{role[:3].upper()}-{len(all_data['data'])+1:03d}",
                    'city': city,
                    'role': role,
                    'salary_min': stats['min'],
                    'salary_median': stats['median'],
                    'salary_max': stats['max'],
                    'salary_avg': stats['avg'],
                    'sample_size': stats['sample_size'],
                    'data_source': '拉勾/Boss/猎聘',
                    'updated_at': datetime.now().strftime('%Y-%m-%d')
                }
                all_data['data'].append(record)
            
            # 避免请求过快
            time.sleep(random.uniform(1, 3))
    
    # 保存数据
    save_to_json(all_data, 'data/salary/batch_salary_data.json')
    print(f"\n抓取完成！共 {len(all_data['data'])} 条记录")


def manual_input_mode():
    """手动录入模式 - 用于初期数据积累"""
    print("手动录入薪资数据模式")
    print("输入格式：城市，职位，行业，经验年限，最低，中位数，最高")
    print("示例：深圳，财务 BP，跨境电商，5-8 年，20000,25000,35000")
    print("输入 q 退出\n")
    
    data = []
    
    while True:
        user_input = input("录入数据：").strip()
        
        if user_input.lower() == 'q':
            break
        
        try:
            parts = user_input.split(',')
            if len(parts) >= 7:
                record = {
                    'id': f"MANUAL-{len(data)+1:03d}",
                    'city': parts[0].strip(),
                    'role': parts[1].strip(),
                    'industry': parts[2].strip(),
                    'experience_years': parts[3].strip(),
                    'salary_min': int(parts[4].strip()),
                    'salary_median': int(parts[5].strip()),
                    'salary_max': int(parts[6].strip()),
                    'sample_size': 1,
                    'data_source': '手动录入',
                    'updated_at': datetime.now().strftime('%Y-%m-%d')
                }
                data.append(record)
                print(f"✓ 已录入：{record['city']} - {record['role']}")
        except Exception as e:
            print(f"✗ 录入失败：{e}")
    
    if data:
        # 读取现有数据
        try:
            with open('data/salary/finance_bp_salary.json', 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except:
            existing = {'meta': {}, 'data': []}
        
        # 合并数据
        existing['data'].extend(data)
        existing['meta']['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        
        # 保存
        save_to_json(existing, 'data/salary/finance_bp_salary.json')
        print(f"\n已保存 {len(data)} 条新数据")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='do-it 薪资数据抓取')
    parser.add_argument('--keyword', type=str, help='职位名称')
    parser.add_argument('--city', type=str, help='城市')
    parser.add_argument('--batch', action='store_true', help='批量抓取')
    parser.add_argument('--manual', action='store_true', help='手动录入模式')
    
    args = parser.parse_args()
    
    if args.manual:
        manual_input_mode()
    elif args.batch:
        batch_crawl()
    elif args.keyword and args.city:
        print(f"抓取 {args.city} - {args.keyword} 的薪资数据...")
        # 单城市抓取逻辑
    else:
        print("用法:")
        print("  python crawl_salary.py --keyword '财务 BP' --city '深圳'")
        print("  python crawl_salary.py --batch  # 批量抓取")
        print("  python crawl_salary.py --manual  # 手动录入")
