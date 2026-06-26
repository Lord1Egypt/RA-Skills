"""
Kickstarter 热门项目追踪器
抓取 funding 比例超过阈值的项目
"""

import requests
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import argparse

# 配置
KICKSTARTER_DISCOVER_URL = "https://www.kickstarter.com/discover/advanced"
DEFAULT_FUNDING_THRESHOLD = 1000  # 1000% funded
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "kickstarter_cache.json")

class KickstarterTracker:
    def __init__(self, threshold: int = DEFAULT_FUNDING_THRESHOLD):
        self.threshold = threshold
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    
    def fetch_projects(self, sort: str = "popular", state: str = "live") -> List[Dict]:
        """
        从 Kickstarter 获取项目列表
        
        Args:
            sort: 排序方式 - popular, newest, end_date, most_backed
            state: 项目状态 - live, successful, submitted
        """
        projects = []
        page = 1
        max_pages = 5  # 最多抓取5页
        
        print(f"Fetching Kickstarter projects (threshold: {self.threshold}%)...")
        
        while page <= max_pages:
            url = f"{KICKSTARTER_DISCOVER_URL}?sort={sort}&state={state}&seed={int(datetime.now().timestamp())}&page={page}"
            
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找项目卡片
                project_cards = soup.find_all('div', class_=re.compile('project-card'))
                
                if not project_cards:
                    # 尝试其他选择器
                    project_cards = soup.select('[data-project]')
                
                if not project_cards:
                    print(f"No more projects found on page {page}")
                    break
                
                for card in project_cards:
                    project = self._parse_project_card(card)
                    if project:
                        projects.append(project)
                
                print(f"Page {page}: Found {len(project_cards)} projects")
                page += 1
                
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break
        
        return projects
    
    def _parse_project_card(self, card) -> Optional[Dict]:
        """解析项目卡片，提取关键信息"""
        try:
            # 提取项目名称
            name_elem = card.find('h3') or card.find('a', class_=re.compile('project-title'))
            name = name_elem.get_text(strip=True) if name_elem else "Unknown"
            
            # 提取项目链接
            link_elem = card.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                url = f"https://www.kickstarter.com{href}" if href.startswith('/') else href
            else:
                url = ""
            
            # 提取描述
            desc_elem = card.find('p', class_=re.compile('description|blurb'))
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # 提取 funding 百分比
            funding_elem = card.find(string=re.compile(r'\d+%'))
            funding_percent = 0
            
            if funding_elem:
                match = re.search(r'(\d+)%', str(funding_elem))
                if match:
                    funding_percent = int(match.group(1))
            else:
                # 尝试从 progress bar 或其他元素提取
                progress_elem = card.find('div', class_=re.compile('progress'))
                if progress_elem:
                    style = progress_elem.get('style', '')
                    match = re.search(r'width:\s*(\d+)%', style)
                    if match:
                        funding_percent = int(match.group(1))
            
            # 提取已筹金额
            pledged_elem = card.find(string=re.compile(r'\$[\d,]+'))
            pledged = ""
            if pledged_elem:
                match = re.search(r'\$[\d,]+', str(pledged_elem))
                if match:
                    pledged = match.group(0)
            
            # 提取 backers 数量
            backers_elem = card.find(string=re.compile(r'\d+\s*backer'))
            backers = ""
            if backers_elem:
                match = re.search(r'(\d+)\s*backer', str(backers_elem))
                if match:
                    backers = match.group(1)
            
            return {
                'name': name,
                'url': url,
                'description': description,
                'funding_percent': funding_percent,
                'pledged': pledged,
                'backers': backers,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error parsing project card: {e}")
            return None
    
    def filter_hot_projects(self, projects: List[Dict]) -> List[Dict]:
        """筛选出 funding 比例超过阈值的项目"""
        hot_projects = [
            p for p in projects 
            if p.get('funding_percent', 0) >= self.threshold
        ]
        # 按 funding 比例排序
        hot_projects.sort(key=lambda x: x.get('funding_percent', 0), reverse=True)
        return hot_projects
    
    def load_cache(self) -> List[Dict]:
        """加载缓存的项目数据"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
        return []
    
    def save_cache(self, projects: List[Dict]):
        """保存项目数据到缓存"""
        try:
            os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(projects, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def get_new_projects(self, current_projects: List[Dict]) -> List[Dict]:
        """获取新增的项目（与缓存对比）"""
        cached = self.load_cache()
        cached_urls = {p['url'] for p in cached}
        
        new_projects = [
            p for p in current_projects 
            if p['url'] and p['url'] not in cached_urls
        ]
        return new_projects
    
    def generate_report(self, projects: List[Dict], new_only: bool = False) -> str:
        """生成简报文本"""
        if not projects:
            return f"🎯 Kickstarter 热门项目追踪\n\n本周没有发现 funding 超过 {self.threshold}% 的热门项目。"
        
        report_lines = [
            f"🚀 Kickstarter 热门项目追踪",
            f"📊 Funding 阈值: {self.threshold}%",
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"\n{'='*50}\n"
        ]
        
        for i, p in enumerate(projects[:10], 1):  # 最多显示10个
            status_emoji = "🔥" if p.get('funding_percent', 0) >= 5000 else "⭐" if p.get('funding_percent', 0) >= 2000 else "✨"
            
            report_lines.append(f"{status_emoji} #{i} {p['name']}")
            report_lines.append(f"   💰 Funding: {p.get('funding_percent', 'N/A')}% {p.get('pledged', '')}")
            report_lines.append(f"   👥 Backers: {p.get('backers', 'N/A')}")
            report_lines.append(f"   🔗 {p['url']}")
            if p.get('description'):
                # 截断描述
                desc = p['description'][:150] + "..." if len(p['description']) > 150 else p['description']
                report_lines.append(f"   📝 {desc}")
            report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description='Kickstarter 热门项目追踪器')
    parser.add_argument('--threshold', type=int, default=1000, help='Funding 百分比阈值 (默认: 1000)')
    parser.add_argument('--new-only', action='store_true', help='只显示新增项目')
    parser.add_argument('--dry-run', action='store_true', help='测试模式，不保存缓存')
    parser.add_argument('--output', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    tracker = KickstarterTracker(threshold=args.threshold)
    
    # 抓取项目
    all_projects = tracker.fetch_projects()
    print(f"Total projects fetched: {len(all_projects)}")
    
    # 筛选热门项目
    hot_projects = tracker.filter_hot_projects(all_projects)
    print(f"Hot projects (>{args.threshold}%): {len(hot_projects)}")
    
    # 如果是 new-only 模式，只显示新增项目
    if args.new_only:
        display_projects = tracker.get_new_projects(hot_projects)
        print(f"New hot projects: {len(display_projects)}")
    else:
        display_projects = hot_projects
    
    # 生成报告
    report = tracker.generate_report(display_projects, args.new_only)
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
    
    # 保存缓存（如果不是 dry-run）
    if not args.dry_run:
        tracker.save_cache(hot_projects)
        print(f"\nCache saved: {len(hot_projects)} projects")
    
    return hot_projects


if __name__ == "__main__":
    main()
