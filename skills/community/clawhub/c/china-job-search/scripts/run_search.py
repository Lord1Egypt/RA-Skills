#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 招聘搜索技能入口脚本
"""

import sys
import os
import json
import argparse
from job_searcher import JobSearcher

def parse_search_query(query: str):
    """解析搜索查询字符串"""
    parts = query.strip().split()
    
    if len(parts) < 2:
        return None, "搜索格式错误，请使用：搜索 [关键词] [地点] 或 搜索 [平台] [关键词] [地点]"
    
    # 检查是否指定了平台
    platforms = ['boss', 'zhipin', '智联', 'zhilian', 'zhaopin', '前程无忧', 'qiancheng', '51job']
    
    if parts[0].lower() in platforms:
        if len(parts) < 3:
            return None, "平台指定搜索格式：搜索 [平台] [关键词] [地点]"
        platform = parts[0].lower()
        keyword = parts[1]
        location = parts[2]
        # 处理可能的额外参数
        salary = None
        experience = None
        if len(parts) > 3 and '-' in parts[3] and 'K' in parts[3]:
            salary = parts[3]
            if len(parts) > 4 and '-' in parts[4] and '年' in parts[4]:
                experience = parts[4]
    else:
        platform = None
        keyword = parts[0]
        location = parts[1]
        salary = None
        experience = None
        if len(parts) > 2 and '-' in parts[2] and 'K' in parts[2]:
            salary = parts[2]
            if len(parts) > 3 and '-' in parts[3] and '年' in parts[3]:
                experience = parts[3]
    
    return {
        'platform': platform,
        'keyword': keyword,
        'location': location,
        'salary': salary,
        'experience': experience
    }, None

def main():
    parser = argparse.ArgumentParser(description='招聘搜索技能')
    parser.add_argument('--query', type=str, help='搜索查询字符串')
    parser.add_argument('--platform', type=str, help='指定平台')
    parser.add_argument('--keyword', type=str, help='搜索关键词')
    parser.add_argument('--location', type=str, help='工作地点')
    parser.add_argument('--salary', type=str, help='薪资范围')
    parser.add_argument('--experience', type=str, help='经验要求')
    
    args = parser.parse_args()
    
    # 优先使用查询字符串
    if args.query:
        params, error = parse_search_query(args.query)
        if error:
            print(json.dumps({'error': error}, ensure_ascii=False))
            return
    else:
        params = {
            'platform': args.platform,
            'keyword': args.keyword,
            'location': args.location,
            'salary': args.salary,
            'experience': args.experience
        }
    
    # 验证必要参数
    if not params['keyword'] or not params['location']:
        print(json.dumps({'error': '缺少必要参数：关键词和地点'}, ensure_ascii=False))
        return
    
    try:
        # 初始化搜索器
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        searcher = JobSearcher(config_path)
        
        # 执行搜索
        results = searcher.search(
            keyword=params['keyword'],
            location=params['location'],
            platform=params['platform'],
            salary_range=params['salary'],
            experience=params['experience']
        )
        
        # 格式化输出
        output = {
            'success': True,
            'count': len(results),
            'results': []
        }
        
        for job in results:
            output['results'].append({
                'platform': job.platform,
                'title': job.title,
                'company': job.company,
                'salary': job.salary,
                'location': job.location,
                'experience': job.experience,
                'education': job.education,
                'skills': job.skills,
                'url': job.url,
                'publish_time': job.publish_time,
                'company_size': job.company_size,
                'company_type': job.company_type
            })
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({'error': f'搜索失败: {str(e)}'}, ensure_ascii=False))

if __name__ == '__main__':
    main()