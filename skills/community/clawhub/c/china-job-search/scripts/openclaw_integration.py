#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw招聘搜索技能集成
提供命令行和API两种使用方式
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Optional

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from job_searcher import JobSearcher, Job
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖已安装: pip install -r requirements.txt")
    sys.exit(1)


class JobSearchSkill:
    """OpenClaw招聘搜索技能"""
    
    def __init__(self, config_path: str = None):
        """初始化技能"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        self.searcher = JobSearcher(config_path)
        self.last_results = []
    
    def handle_command(self, command: str) -> str:
        """
        处理搜索命令
        
        命令格式:
        - 搜索 Python 北京
        - 搜索 boss Java 上海
        - 搜索 智联 前端 广州 15-30K
        - 搜索 前程无忧 测试 深圳 3-5年
        """
        parts = command.strip().split()
        
        if len(parts) < 2:
            return "命令格式错误。用法: 搜索 [平台] [关键词] [地点] [条件]"
        
        # 解析参数
        platform = None
        keyword = parts[1]
        city = "北京"  # 默认
        conditions = []
        
        # 检查是否指定了平台
        platform_keywords = ['boss', '智联', '前程无忧', 'zhilian', 'qiancheng']
        if parts[1].lower() in platform_keywords and len(parts) >= 3:
            platform_map = {
                'boss': ['boss'],
                '智联': ['zhilian'],
                'zhilian': ['zhilian'],
                '前程无忧': ['qiancheng'],
                'qiancheng': ['qiancheng']
            }
            platform = platform_map.get(parts[1].lower())
            keyword = parts[2]
        
        # 提取地点（简单判断）
        city_keywords = ['北京', '上海', '广州', '深圳', '杭州', '成都', 
                        '武汉', '南京', '西安', '重庆']
        
        for i, part in enumerate(parts):
            if part in city_keywords:
                city = part
                break
        
        # 执行搜索
        try:
            self.last_results = self.searcher.search(
                keyword=keyword,
                city=city,
                platforms=platform,
                max_results=20
            )
            
            if not self.last_results:
                return f"未找到与 '{keyword}' 相关的岗位（地点: {city}）"
            
            # 格式化输出
            output = self.searcher.format_results(self.last_results, 'table')
            return output
            
        except Exception as e:
            return f"搜索失败: {str(e)}"
    
    def get_stats(self) -> Dict:
        """获取搜索统计信息"""
        if not self.last_results:
            return {"total": 0, "platforms": {}}
        
        stats = {
            "total": len(self.last_results),
            "platforms": {},
            "salary_range": {"min": 999, "max": 0, "avg": 0}
        }
        
        # 统计各平台数量
        for job in self.last_results:
            platform = job.platform
            if platform not in stats["platforms"]:
                stats["platforms"][platform] = 0
            stats["platforms"][platform] += 1
        
        # 计算薪资范围
        salaries = []
        for job in self.last_results:
            salary_text = job.salary
            if 'K' in salary_text or 'k' in salary_text:
                import re
                numbers = re.findall(r'\d+', salary_text)
                if numbers:
                    salary_vals = list(map(int, numbers))
                    salaries.extend(salary_vals)
        
        if salaries:
            stats["salary_range"]["min"] = min(salaries)
            stats["salary_range"]["max"] = max(salaries)
            stats["salary_range"]["avg"] = sum(salaries) / len(salaries)
        
        return stats
    
    def export_results(self, format: str = 'json', filepath: str = None) -> str:
        """导出搜索结果"""
        if not self.last_results:
            return "没有可导出的数据"
        
        if format == 'json':
            data = []
            for job in self.last_results:
                data.append({
                    "platform": job.platform,
                    "title": job.title,
                    "company": job.company,
                    "salary": job.salary,
                    "location": job.location,
                    "experience": job.experience,
                    "education": job.education,
                    "skills": job.skills,
                    "url": job.url
                })
            
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(json_str)
                return f"数据已导出到: {filepath}"
            else:
                return json_str
        
        elif format == 'csv':
            import csv
            if not filepath:
                filepath = 'job_search_results.csv'
            
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['平台', '职位', '公司', '薪资', '地点', '经验', '学历', '技能', '链接'])
                
                for job in self.last_results:
                    writer.writerow([
                        job.platform,
                        job.title,
                        job.company,
                        job.salary,
                        job.location,
                        job.experience,
                        job.education,
                        ','.join(job.skills),
                        job.url
                    ])
            
            return f"CSV数据已导出到: {filepath}"
        
        else:
            return f"不支持的导出格式: {format}"


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='OpenClaw招聘搜索技能')
    parser.add_argument('command', nargs='?', help='搜索命令，如: "搜索 Python 北京"')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--export', choices=['json', 'csv'], help='导出格式')
    parser.add_argument('--output', help='导出文件路径')
    parser.add_argument('--test', action='store_true', help='测试所有平台')
    
    args = parser.parse_args()
    
    skill = JobSearchSkill()
    
    if args.test:
        print("测试招聘搜索技能...")
        # 简单测试
        result = skill.handle_command("搜索 Python 北京")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        stats = skill.get_stats()
        print(f"\n统计信息: {stats}")
        
    elif args.stats:
        if skill.last_results:
            stats = skill.get_stats()
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("请先执行搜索")
    
    elif args.export:
        if skill.last_results:
            result = skill.export_results(args.export, args.output)
            print(result)
        else:
            print("请先执行搜索")
    
    elif args.command:
        result = skill.handle_command(args.command)
        print(result)
    
    else:
        # 交互模式
        print("OpenClaw招聘搜索技能")
        print("=" * 50)
        print("命令格式: 搜索 [平台] [关键词] [地点]")
        print("示例: 搜索 Python 北京")
        print("示例: 搜索 boss Java 上海")
        print("输入 'quit' 退出")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if user_input.startswith('搜索'):
                    result = skill.handle_command(user_input)
                    print(result)
                elif user_input == '统计':
                    stats = skill.get_stats()
                    print(json.dumps(stats, ensure_ascii=False, indent=2))
                elif user_input.startswith('导出'):
                    parts = user_input.split()
                    if len(parts) >= 2:
                        format = parts[1]
                        result = skill.export_results(format)
                        print(result)
                    else:
                        print("用法: 导出 [json|csv]")
                else:
                    print("未知命令。可用命令: 搜索, 统计, 导出, quit")
                    
            except KeyboardInterrupt:
                print("\n退出")
                break
            except Exception as e:
                print(f"错误: {e}")


if __name__ == '__main__':
    main()