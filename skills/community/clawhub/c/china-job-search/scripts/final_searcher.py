#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版招聘搜索技能
确保始终可用的招聘搜索解决方案
"""

import sys
import os
import json
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from urllib.parse import quote, urljoin

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4 fake-useragent")
    sys.exit(1)


@dataclass
class FinalJob:
    """最终版岗位信息"""
    platform: str
    title: str
    company: str
    salary: str
    location: str
    experience: str
    education: str
    skills: List[str]
    url: str
    source: str = "mock"  # real, mock
    timestamp: str = ""
    
    def to_dict(self):
        """转换为字典"""
        return asdict(self)


class FinalJobSearcher:
    """最终版招聘搜索器 - 确保始终可用"""
    
    def __init__(self, config_path: str = None):
        """初始化"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.ua = UserAgent()
        self.session = requests.Session()
        self._setup_session()
        
        # 加载丰富的模拟数据
        self.mock_data = self._load_rich_mock_data()
        
        # 设置时间戳
        import datetime
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _setup_session(self):
        """设置会话参数"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
        })
    
    def _load_rich_mock_data(self) -> Dict:
        """加载丰富的模拟数据"""
        return {
            "Python": [
                {"title": "Python高级开发工程师", "company": "字节跳动", "salary": "25-50K·16薪", 
                 "location": "北京·海淀区", "experience": "3-5年", "education": "本科",
                 "skills": ["Python", "Django/Flask", "MySQL", "Redis", "Docker", "微服务"]},
                {"title": "Python数据分析师", "company": "阿里巴巴", "salary": "20-40K·14薪",
                 "location": "杭州·余杭区", "experience": "2-4年", "education": "本科",
                 "skills": ["Python", "Pandas", "SQL", "统计学", "机器学习", "数据可视化"]},
                {"title": "Python后端开发", "company": "腾讯", "salary": "22-45K·15薪",
                 "location": "深圳·南山区", "experience": "3-6年", "education": "本科",
                 "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "K8s"]},
                {"title": "Python自动化测试", "company": "华为", "salary": "18-35K·15薪",
                 "location": "深圳·龙岗区", "experience": "2-5年", "education": "本科",
                 "skills": ["Python", "Selenium", "自动化测试", "接口测试", "性能测试"]},
            ],
            "Java": [
                {"title": "Java高级开发工程师", "company": "腾讯", "salary": "30-60K·15薪",
                 "location": "深圳·南山区", "experience": "5-8年", "education": "本科",
                 "skills": ["Java", "Spring", "微服务", "分布式", "高并发", "Redis"]},
                {"title": "Java架构师", "company": "百度", "salary": "40-80K",
                 "location": "北京·海淀区", "experience": "8年以上", "education": "本科",
                 "skills": ["Java", "架构设计", "系统优化", "团队管理", "云计算"]},
                {"title": "Java开发工程师", "company": "京东", "salary": "20-40K·14薪",
                 "location": "北京·朝阳区", "experience": "3-6年", "education": "本科",
                 "skills": ["Java", "Spring Boot", "MySQL", "消息队列", "分布式"]},
            ],
            "前端": [
                {"title": "前端开发专家", "company": "美团", "salary": "25-45K·15薪",
                 "location": "上海·浦东新区", "experience": "4-7年", "education": "本科",
                 "skills": ["React", "Vue", "TypeScript", "Node.js", "Webpack", "性能优化"]},
                {"title": "前端开发工程师", "company": "滴滴", "salary": "18-35K·14薪",
                 "location": "北京·朝阳区", "experience": "2-5年", "education": "本科",
                 "skills": ["JavaScript", "Vue", "小程序", "移动端", "CSS3"]},
                {"title": "全栈开发工程师", "company": "小米", "salary": "22-42K·14薪",
                 "location": "北京·海淀区", "experience": "3-6年", "education": "本科",
                 "skills": ["React", "Node.js", "Python", "MySQL", "Docker"]},
            ],
            "测试": [
                {"title": "测试开发工程师", "company": "字节跳动", "salary": "20-40K·16薪",
                 "location": "北京·海淀区", "experience": "3-5年", "education": "本科",
                 "skills": ["Python", "自动化测试", "性能测试", "接口测试", "CI/CD"]},
                {"title": "软件测试工程师", "company": "阿里巴巴", "salary": "15-30K·14薪",
                 "location": "杭州·余杭区", "experience": "2-4年", "education": "本科",
                 "skills": ["功能测试", "自动化测试", "SQL", "Linux", "测试用例"]},
            ],
            "运维": [
                {"title": "运维开发工程师", "company": "腾讯", "salary": "22-45K·15薪",
                 "location": "深圳·南山区", "experience": "3-7年", "education": "本科",
                 "skills": ["Linux", "Python", "Docker", "K8s", "CI/CD", "监控"]},
                {"title": "云计算工程师", "company": "华为", "salary": "25-50K·15薪",
                 "location": "深圳·龙岗区", "experience": "4-8年", "education": "本科",
                 "skills": ["云计算", "K8s", "Docker", "网络", "安全", "自动化"]},
            ],
            "默认": [
                {"title": "软件开发工程师", "company": "某科技公司", "salary": "15-30K·13薪",
                 "location": "全国", "experience": "1-3年", "education": "本科",
                 "skills": ["编程", "算法", "数据结构", "团队协作"]},
                {"title": "技术专员", "company": "某互联网企业", "salary": "12-25K",
                 "location": "全国", "experience": "1-2年", "education": "大专",
                 "skills": ["技术支持", "问题解决", "沟通能力"]},
            ]
        }
    
    def search_with_guarantee(self, keyword: str, city: str = "北京", 
                             max_results: int = 15) -> Dict[str, List[FinalJob]]:
        """
        保证有结果的搜索
        优先尝试真实搜索，失败时使用模拟数据
        """
        print(f"\n搜索: {keyword} - {city}")
        print("=" * 50)
        
        results = {}
        
        # 尝试各平台
        platforms = [
            ("前程无忧", self._try_qiancheng_search),
            ("BOSS直聘", self._try_boss_search),
            ("智联招聘", self._try_zhilian_search),
        ]
        
        for platform_name, search_func in platforms:
            print(f"\n{platform_name}:")
            
            try:
                jobs = search_func(keyword, city, max_results // 2)
                
                if jobs:
                    print(f"  找到 {len(jobs)} 个岗位")
                    results[platform_name] = jobs
                else:
                    print("  未找到岗位，使用模拟数据")
                    mock_jobs = self._get_mock_jobs(keyword, city, platform_name, max_results // 3)
                    results[platform_name] = mock_jobs
                    
            except Exception as e:
                print(f"  搜索失败: {e}")
                print("  使用模拟数据")
                mock_jobs = self._get_mock_jobs(keyword, city, platform_name, max_results // 3)
                results[platform_name] = mock_jobs
        
        # 确保至少有结果
        if not any(results.values()):
            print("\n所有平台搜索失败，使用默认模拟数据")
            for platform_name, _ in platforms:
                results[platform_name] = self._get_mock_jobs(keyword, city, platform_name, 3)
        
        # 统计
        total = sum(len(jobs) for jobs in results.values())
        real_count = sum(1 for jobs in results.values() for job in jobs if job.source == "real")
        
        print(f"\n搜索完成:")
        print(f"  总岗位数: {total}")
        print(f"  真实数据: {real_count}")
        print(f"  模拟数据: {total - real_count}")
        
        return results
    
    def _try_qiancheng_search(self, keyword: str, city: str, max_results: int) -> List[FinalJob]:
        """尝试前程无忧搜索"""
        jobs = []
        
        try:
            # 构建搜索URL
            city_code = self._get_city_code("qiancheng", city)
            search_url = f"https://search.51job.com/list/{city_code},000000,0000,00,9,99,{quote(keyword)},2,1.html"
            
            # 添加延迟
            time.sleep(random.uniform(1, 2))
            
            # 发送请求
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                # 尝试解析
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 多种选择器尝试
                selectors = [
                    '.j_joblist .e',
                    '.dw_table .el',
                    '.joblist .job_item',
                    '[class*="job"]',
                ]
                
                job_items = []
                for selector in selectors:
                    job_items = soup.select(selector)
                    if job_items:
                        print(f"  使用选择器: {selector}")
                        break
                
                for item in job_items[:max_results]:
                    try:
                        job = self._parse_qiancheng_item(item, city)
                        if job:
                            jobs.append(job)
                    except:
                        continue
                
                # 标记来源
                for job in jobs:
                    job.source = "real"
                    job.timestamp = self.timestamp
                    
        except Exception as e:
            print(f"  前程无忧搜索错误: {e}")
        
        return jobs
    
    def _parse_qiancheng_item(self, item, city: str) -> Optional[FinalJob]:
        """解析前程无忧职位项"""
        try:
            # 尝试多种选择器组合
            title = None
            company = None
            
            # 标题选择器
            title_selectors = ['.jname', '.t1', '.t2', 'a[class*="name"]', 'span[class*="title"]']
            for selector in title_selectors:
                elem = item.select_one(selector)
                if elem and elem.text.strip():
                    title = elem.text.strip()
                    break
            
            # 公司选择器
            company_selectors = ['.cname', '.cname a', '.company', 'a[class*="company"]']
            for selector in company_selectors:
                elem = item.select_one(selector)
                if elem and elem.text.strip():
                    company = elem.text.strip()
                    break
            
            if not title or not company:
                return None
            
            # 薪资
            salary = "面议"
            salary_elem = item.select_one('.sal')
            if salary_elem and salary_elem.text.strip():
                salary = salary_elem.text.strip()
            
            # 地点
            location = city
            location_elem = item.select_one('.d.at')
            if location_elem and location_elem.text.strip():
                location = location_elem.text.strip()
            
            # 经验和学历
            experience = "经验不限"
            education = "学历不限"
            
            info_elem = item.select_one('.jtag .t1')
            if info_elem:
                info_text = info_elem.text
                import re
                exp_match = re.search(r'(\d+[-]?\d*年?)经验', info_text)
                if exp_match:
                    experience = exp_match.group(1) + "经验"
                
                edu_keywords = ['中专', '高中', '大专', '本科', '硕士', '博士']
                for edu in edu_keywords:
                    if edu in info_text:
                        education = edu
                        break
            
            # 技能
            skills = []
            tag_elems = item.select('.jtag .t2 span')
            for tag in tag_elems:
                skill = tag.text.strip()
                if skill and len(skill) < 15:
                    skills.append(skill)
            
            # URL
            url = "https://www.51job.com"
            link_elem = item.select_one('a')
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                if href.startswith('http'):
                    url = href
                else:
                    url = urljoin("https://www.51job.com", href)
            
            return FinalJob(
                platform="前程无忧",
                title=title,
                company=company,
                salary=salary,
                location=location,
                experience=experience,
                education=education,
                skills=skills[:5],
                url=url,
                source="real",
                timestamp=self.timestamp
            )
            
        except Exception:
            return None
    
    def _try_boss_search(self, keyword: str, city: str, max_results: int) -> List[FinalJob]:
        """尝试BOSS直聘搜索"""
        # 目前使用模拟数据，可以后续实现真实搜索
        return self._get_mock_jobs(keyword, city, "BOSS直聘", max_results)
    
    def _try_zhilian_search(self, keyword: str, city: str, max_results: int) -> List[FinalJob]:
        """尝试智联招聘搜索"""
        # 目前使用模拟数据，可以后续实现真实搜索
        return self._get_mock_jobs(keyword, city, "智联招聘", max_results)
    
    def _get_mock_jobs(self, keyword: str, city: str, platform: str, max_results: int) -> List[FinalJob]:
        """获取模拟岗位"""
        jobs = []
        
        # 查找匹配的模拟数据
        mock_list = self.mock_data.get(keyword, [])
        if not mock_list:
            # 尝试部分匹配
            for key in self.mock_data:
                if key in keyword or keyword in key:
                    mock_list = self.mock_data[key]
                    break
        
        # 使用默认数据
        if not mock_list:
            mock_list = self.mock_data["默认"]
        
        # 创建岗位
        for i, mock in enumerate(mock_list[:max_results]):
            # 调整地点
            location = city
            if '·' in mock["location"]:
                location = city + "·" + mock["location"].split("·")[-1]
            
            job = FinalJob(
                platform=platform,
                title=mock["title"],
                company=mock["company"],
                salary=mock["salary"],
                location=location,
                experience=mock["experience"],
                education=mock["education"],
                skills=mock["skills"],
                url=f"https://www.example.com/job_{platform}_{i}",
                source="mock",
                timestamp=self.timestamp
            )
            jobs.append(job)
        
        return jobs
    
    def _get_city_code(self, platform: str, city: str) -> str:
        """获取城市代码"""
        city_maps = {
            "qiancheng": {
                '北京': '010000', '上海': '020000', '广州': '030200', '深圳': '030300',
                '杭州': '080200', '成都': '090200', '武汉': '180200', '南京': '070200',
                '西安': '200200', '重庆': '040000'
            },
            "boss": {
                '北京': '101010100', '上海': '101020100', '广州': '101280100',
                '深圳': '101280600', '杭州': '101210100', '成都': '101270100',
                '武汉': '101200100', '南京': '101190100', '西安': '101110100',
                '重庆': '101040100'
            },
            "zhilian": {
                '北京': '530', '上海': '538', '广州': '763', '深圳': '765',
                '杭州': '653', '成都': '801', '武汉': '736', '南京': '635',
                '西安': '854', '重庆': '551'
            }
        }
        
        platform_map = city_maps.get(platform, {})
        return platform_map.get(city, list(platform_map.values())[0] if platform_map else '010000')
    
    def format_results(self, results: Dict[str, List[FinalJob]], show_details: bool = True) -> str:
        """格式化输出结果"""
        if not results:
            return "未找到任何岗位"
        
        output = "=" * 80 + "\n"
        output += "招聘搜索结果\n"
        output += f"搜索时间: {self.timestamp}\n"
        output += "=" * 80 + "\n\n"
        
        total_jobs = 0
        real_jobs = 0
        
        for platform, jobs in results.items():
            if not jobs:
                continue
            
            platform_real = sum(1 for job in jobs if job.source == "real")
            platform_mock = len(jobs) - platform_real
            
            total_jobs += len(jobs)
            real_jobs += platform_real
            
            source_info = ""
            if platform_real > 0 and platform_mock > 0:
                source_info = f" ({platform_real}真实 + {platform_mock}模拟)"
            elif platform_real > 0:
                source_info = " (真实数据)"
            elif platform_mock > 0:
                source_info = " (模拟数据)"
            
            output += f"{platform}{source_info}:\n"
            output += "-" * 60 + "\n"
            
            for i, job in enumerate(jobs[:5], 1):
                source_mark = "[R]" if job.source == "real" else "[M]"
                output += f"{source_mark} {i}. {job.title}\n"
                
                if show_details:
                    output += f"   公司: {job.company} | 薪资: {job.salary}\n"
                    output += f"   地点: {job.location} | 要求: {job.experience} | {job.education}\n"
                    if job.skills:
                        output += f"   技能: {', '.join(job.skills[:3])}\n"
                output += "\n"
            
            if len(jobs) > 5:
                output += f"  ... 还有 {len(jobs)-5} 个岗位\n"
            output += "\n"
        
        output += "=" * 80 + "\n"
        output += f"统计: {real_jobs} 个真实岗位 + {total_jobs-real_jobs} 个模拟岗位 = {total_jobs} 个岗位\n"
        
        if total_jobs - real_jobs > 0:
            output += "注: [R] 表示真实数据，[M] 表示模拟数据（当真实搜索失败时使用）\n"
        
        output += "=" * 80
        
        return output
    
    def save_results(self, results: Dict[str, List[FinalJob]], filename: str = None) -> str:
        """保存结果到文件"""
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.json"
        
        data = []
        for platform, jobs in results.items():
            for job in jobs:
                data.append(job.to_dict())
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到: {filename}")
        return filename
    
    def export_to_csv(self, results: Dict[str, List[FinalJob]], filename: str = None) -> str:
        """导出为CSV格式"""
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.csv"
        
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['平台', '职位', '公司', '薪资', '地点', '经验', '学历', '技能', '数据来源', '时间'])
            
            for platform, jobs in results.items():
                for job in jobs:
                    writer.writerow([
                        platform,
                        job.title,
                        job.company,
                        job.salary,
                        job.location,
                        job.experience,
                        job.education,
                        ','.join(job.skills),
                        '真实' if job.source == 'real' else '模拟',
                        job.timestamp
                    ])
        
        print(f"CSV结果已保存到: {filename}")
        return filename


def main():
    """主函数"""
    print("最终版招聘搜索技能")
    print("=" * 60)
    print("说明: 保证始终有结果的招聘搜索解决方案")
    print("=" * 60)
    
    import sys
    
    # 创建搜索器
    searcher = FinalJobSearcher()
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        city = sys.argv[2] if len(sys.argv) > 2 else "北京"
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    else:
        # 交互模式
        print("\n请输入搜索参数:")
        keyword = input("关键词 (默认: Python): ").strip() or "Python"
        city = input("城市 (默认: 北京): ").strip() or "北京"
        max_results = 15
    
    # 执行搜索
    results = searcher.search_with_guarantee(keyword, city, max_results)
    
    # 输出结果
    output = searcher.format_results(results)
    print(output)
    
    # 保存结果
    json_file = searcher.save_results(results)
    csv_file = searcher.export_to_csv(results)
    
    print(f"\n搜索完成!")
    print(f"JSON文件: {json_file}")
    print(f"CSV文件: {csv_file}")
    print(f"\n提示: 可以导入Excel或数据分析工具进行进一步处理")


if __name__ == '__main__':
    main()
