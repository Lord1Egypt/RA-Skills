#!/usr/bin/env python3
"""
招投标信息采集主脚本（改进版）
支持7个已验证网站的自动采集、解析、筛选、存储
增加详细的调试信息和错误处理
"""

import argparse
import hashlib
import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./招投标数据/logs/crawler_{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, db_path: str = './招投标数据/history.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表结构"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建主表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bidding_projects (
                id TEXT PRIMARY KEY,
                source_site TEXT NOT NULL,
                source_url TEXT,
                publish_date DATE,
                project_name TEXT NOT NULL,
                budget REAL,
                budget_text TEXT,
                detail_url TEXT,
                region TEXT,
                purchaser TEXT,
                deadline DATETIME,
                project_type TEXT,
                procurement_method TEXT,
                contact_name TEXT,
                contact_phone TEXT,
                industry TEXT,
                description TEXT,
                raw_content TEXT,
                crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT UNIQUE,
                push_status INTEGER DEFAULT 0,
                push_time DATETIME
            )
        ''')

        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_date ON bidding_projects(publish_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_region ON bidding_projects(region)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON bidding_projects(source_site)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_push_status ON bidding_projects(push_status)')

        # 创建日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawl_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawl_date DATE,
                source_site TEXT,
                total_count INTEGER,
                new_count INTEGER,
                update_count INTEGER,
                error_count INTEGER,
                duration_seconds INTEGER,
                status TEXT,
                error_message TEXT,
                crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def insert_project(self, project: Dict) -> bool:
        """插入项目数据，返回是否为新增"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 检查是否已存在
            cursor.execute('SELECT id FROM bidding_projects WHERE id = ?', (project['id'],))
            exists = cursor.fetchone()

            if exists:
                # 更新
                cursor.execute('''
                    UPDATE bidding_projects SET
                        budget=?, budget_text=?, purchaser=?, deadline=?,
                        project_type=?, procurement_method=?, contact_name=?,
                        contact_phone=?, industry=?, description=?, raw_content=?,
                        crawl_time=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (
                    project.get('budget'),
                    project.get('budget_text'),
                    project.get('purchaser'),
                    project.get('deadline'),
                    project.get('project_type'),
                    project.get('procurement_method'),
                    project.get('contact_name'),
                    project.get('contact_phone'),
                    project.get('industry'),
                    project.get('description'),
                    project.get('raw_content'),
                    project['id']
                ))
                conn.commit()
                logger.debug(f"更新项目: {project['project_name'][:50]}")
                return False
            else:
                # 插入
                cursor.execute('''
                    INSERT INTO bidding_projects VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, 0, NULL
                    )
                ''', (
                    project['id'],
                    project['source_site'],
                    project.get('source_url'),
                    project.get('publish_date'),
                    project['project_name'],
                    project.get('budget'),
                    project.get('budget_text'),
                    project.get('detail_url'),
                    project.get('region'),
                    project.get('purchaser'),
                    project.get('deadline'),
                    project.get('project_type'),
                    project.get('procurement_method'),
                    project.get('contact_name'),
                    project.get('contact_phone'),
                    project.get('industry'),
                    project.get('description'),
                    project.get('raw_content'),
                    project['hash']
                ))
                conn.commit()
                logger.info(f"新增项目: {project['project_name'][:50]} | 区域: {project.get('region', 'N/A')}")
                return True
        except Exception as e:
            logger.error(f"数据库操作失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_new_projects(self, date: str) -> List[Dict]:
        """获取指定日期的新增项目"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM bidding_projects
            WHERE publish_date = ? AND push_status = 0
            ORDER BY region, source_site, publish_date
        ''', (date,))

        columns = [desc[0] for desc in cursor.description]
        projects = []
        for row in cursor.fetchall():
            project = dict(zip(columns, row))
            projects.append(project)

        conn.close()
        return projects

    def update_push_status(self, project_ids: List[str]):
        """更新推送状态"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for pid in project_ids:
            cursor.execute('UPDATE bidding_projects SET push_status = 1, push_time = CURRENT_TIMESTAMP WHERE id = ?', (pid,))

        conn.commit()
        conn.close()


class RegionMatcher:
    """区域匹配器"""

    # 目标区域关键词
    KEYWORDS = {
        "盐南高新区": ["盐南高新区", "盐南", "城南新区", "城南"],
        "经开区": ["经开区", "经济技术开发区", "开发区"]
    }

    # 需要排除的区县关键词（这些区县的开发区要剔除）
    EXCLUDED_COUNTIES = [
        "亭湖", "盐都", "大丰", "响水", "滨海", "建湖", "射阳", "东台", "阜宁"
    ]

    @classmethod
    def match(cls, text: str) -> Optional[str]:
        """匹配区域 - 先排除区县，再匹配目标区域"""

        # 首先检查是否包含区县关键词（优先级最高，先排除）
        for county in cls.EXCLUDED_COUNTIES:
            if county in text:
                logger.debug(f"排除区县项目: {county} - {text[:50]}")
                return None

        # 排除区县后，再匹配目标区域
        for region, keywords in cls.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return region

        return None


class ProjectExtractor:
    """项目信息提取器"""

    @staticmethod
    def generate_id(project_name: str, publish_date: str, source_site: str) -> str:
        """生成唯一标识"""
        content = f"{project_name}|{publish_date}|{source_site}"
        return hashlib.md5(content.encode()).hexdigest()

    @staticmethod
    def generate_hash(project: Dict) -> str:
        """生成内容哈希"""
        content = json.dumps(project, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(content.encode()).hexdigest()


class BaseCrawler:
    """采集器基类"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        raise NotImplementedError

    def _save_project(self, project: Dict) -> bool:
        """保存项目"""
        try:
            # 生成ID和hash
            project['id'] = ProjectExtractor.generate_id(
                project['project_name'],
                project.get('publish_date', datetime.now().strftime('%Y-%m-%d')),
                project['source_site']
            )
            project['hash'] = ProjectExtractor.generate_hash(project)

            # 所有项目都先进行区县名检查（优先级最高）
            for county in RegionMatcher.EXCLUDED_COUNTIES:
                if county in project['project_name']:
                    logger.debug(f"排除区县项目: {county} - {project['project_name'][:50]}")
                    return False

            # 区域匹配（区域内公司跳过此步骤）
            if getattr(self, 'REGIONAL_COMPANY', False):
                # 根据网站名称设置不同的区域标记
                if self.SITE_NAME == "城南新区公共资源交易网":
                    project['region'] = "盐南高新区"
                else:
                    project['region'] = "区域内"
                return self.db_manager.insert_project(project)

            # 非区域内公司，进行区域匹配（仅根据标题）
            text = project['project_name']
            project['region'] = RegionMatcher.match(text)

            if project['region']:
                return self.db_manager.insert_project(project)
            else:
                logger.debug(f"跳过（不匹配区域）: {project['project_name'][:50]}")
            return False
        except Exception as e:
            logger.error(f"保存项目失败: {e}")
            return False

    def _parse_date(self, date_str: str) -> str:
        """解析日期字符串"""
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')

        # 尝试多种日期格式
        import re
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2024-04-10
            r'(\d{4})/(\d{1,2})/(\d{1,2})',  # 2024/04/10
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2024年4月10日
            r'(\d{4})\.(\d{1,2})\.(\d{1,2})',  # 2024.04.10
        ]

        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                year, month, day = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        return datetime.now().strftime('%Y-%m-%d')

    def _match_region(self, title: str) -> Optional[str]:
        """匹配项目名称中的区域关键词"""
        for region, keywords in {"盐南高新区": ["盐南高新区", "盐南", "城南新区", "城南"],
                                 "经开区": ["经开区", "经济技术开发区", "开发区"]}.items():
            if any(keyword in title for keyword in keywords):
                return region
        return None

    def _ensure_encoding(self, response: requests.Response, default_encoding: str = 'utf-8'):
        """确保响应编码正确"""
        if response.encoding == 'ISO-8859-1':
            response.encoding = default_encoding
        return response

    def _extract_date_from_text(self, text: str) -> Optional[str]:
        """从文本中提取日期"""
        import re
        date_patterns = [
            r'(\d{4})[.\-/年](\d{1,2})[.\-/月](\d{1,2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return None

    def _extract_date_from_url(self, url: str, date_pattern: str = r'/(\d{4})(\d{2})(\d{2})/') -> Optional[str]:
        """从URL中提取日期"""
        import re
        match = re.search(date_pattern, url)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month}-{day}"
        return None

    def _is_valid_url(self, url: str, pattern: str = None) -> bool:
        """验证URL格式"""
        if not url or len(url) < 10:
            return False
        if pattern:
            import re
            return bool(re.match(pattern, url))
        return True

    def _clean_text(self, text: str) -> str:
        """清理文本（去除多余空格、换行等）"""
        if not text:
            return ""
        return ' '.join(text.split())

    def _extract_number(self, text: str) -> Optional[float]:
        """从文本中提取数字"""
        import re
        match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
        if match:
            try:
                return float(match.group(1))
            except:
                return None
        return None


class YanchengGovCrawler(BaseCrawler):
    """盐城市政府采购网采集器"""

    SITE_NAME = "盐城市政府采购网"
    BASE_URL = "https://czj.yancheng.gov.cn"

    # 子版块配置
    COLUMNS = {
        "采购意向": 24547,
        "单一来源公示": 24549,
        "资格预审和招标公告": 31691,
        "竞争性谈判公告": 20176,
        "竞争性磋商公告": 20177,
        "询价公告": 20179,
        "中标（成交）公告": 31692,
        "终止公告": 20182,
        "更正公告": 20183,
        "其他公告": 20184,
        "征集公告": 33999,
        "入围公告": 33998,
        "合同公告": 20185
    }

    # 需要访问详情页获取标题的版块
    NEED_DETAIL_PAGE = {31691, 31692, 20185}

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        for col_name, col_id in self.COLUMNS.items():
            try:
                # 使用用户提供的URL格式（包含webname和permissiontype参数）
                url = f"{self.BASE_URL}/module/web/jpage/dataproxy.jsp?page=1&appid=1&webid=7&path=/&columnid={col_id}&unitid=135567&webname=%25E7%259B%2590%25E5%259F%258E%25E5%25B8%2582%25E8%25B4%25A2%25E6%2594%25BF%25E5%25B1%2580&permissiontype=0"
                logger.debug(f"请求版块: {col_name} (col_id={col_id})")

                # 使用用户提供的请求头
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Referer": "https://czj.yancheng.gov.cn/",
                }

                response = self.session.get(url, headers=headers, timeout=20)

                if response.status_code == 200:
                    projects = self._parse_response(response.text, col_id)
                    logger.info(f"版块 {col_name} 解析到 {len(projects)} 条数据")

                    for project in projects:
                        if self._save_project(project):
                            new_count += 1
                        total_count += 1
                else:
                    logger.warning(f"版块 {col_name} 请求失败: 状态码 {response.status_code}")

                time.sleep(1)  # 避免请求过快
            except Exception as e:
                logger.error(f"采集版块 {col_name} 失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_response(self, text: str, col_id: int) -> List[Dict]:
        """解析响应数据 - 使用用户提供的正则表达式方法"""
        projects = []
        import re

        try:
            # 使用正则表达式匹配 <record><![CDATA[...]]></record> 格式
            records = re.findall(r'<record><!\[CDATA\[(.*?)\]\]></record>', text, re.S | re.I)
            logger.debug(f"找到 {len(records)} 个record元素")

            for record in records:
                try:
                    # 提取href（URL）
                    href_match = re.search(r"href=['\"]([^'\"]+)['\"]", record)
                    if not href_match:
                        continue

                    href = href_match.group(1)
                    if href and not href.startswith('http'):
                        detail_url = self.BASE_URL + href
                    else:
                        detail_url = href

                    # 从URL提取日期
                    date_match = re.search(r'/art/(\d{4})/(\d{1,2})/(\d{1,2})/', detail_url)
                    if not date_match:
                        continue

                    year, month, day = date_match.groups()
                    publish_date = f"{year}-{int(month):02d}-{int(day):02d}"

                    # 检查是否是特殊版块（标题是占位符）
                    is_placeholder_title = False
                    title = ""

                    # 先尝试提取title属性
                    title_match = re.search(r"title=['\"]([^'\"]+)['\"]", record)
                    if title_match:
                        title_candidate = title_match.group(1).strip()
                        # 检查是否是占位符
                        if title_candidate in ['<!--标题-->', '&nbsp;', ''] or len(title_candidate) < 2:
                            is_placeholder_title = True
                        else:
                            title = title_candidate

                    # 如果title属性为空或占位符，尝试从<a>标签内提取
                    if not title or is_placeholder_title:
                        a_tag_match = re.search(r"<a[^>]*>([^<]*)</a>", record)
                        if a_tag_match:
                            title_candidate = a_tag_match.group(1).strip()
                            # 清理HTML实体
                            title_candidate = title_candidate.replace('&nbsp;', '').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                            if title_candidate and title_candidate not in ['<!--标题-->', ''] and len(title_candidate) >= 2:
                                title = title_candidate

                    # 如果需要获取详情页的版块，获取真实标题
                    if col_id in self.NEED_DETAIL_PAGE and (not title or '<!--' in title or len(title) < 5):
                        title = self._fetch_detail_title(detail_url)

                    if not title or len(title) < 5:
                        logger.debug(f"跳过: 标题过短 - {title[:30]}")
                        continue

                    project = {
                        'source_site': self.SITE_NAME,
                        'source_url': self.BASE_URL,
                        'project_name': title,
                        'publish_date': publish_date,
                        'detail_url': detail_url,
                        'project_type': self._get_category(col_id),
                        'raw_content': record
                    }

                    projects.append(project)
                except Exception as e:
                    logger.warning(f"解析记录失败: {e}")
                    continue
        except Exception as e:
            logger.error(f"解析响应失败: {e}")

        return projects

    def _fetch_detail_title(self, url: str) -> str:
        """从详情页获取标题"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                title = soup.find('title')
                if title:
                    return title.text.strip()
        except Exception as e:
            logger.warning(f"获取详情页标题失败: {e}")
        return ""

    def _get_category(self, col_id: int) -> str:
        """根据版块ID获取分类"""
        for name, cid in self.COLUMNS.items():
            if cid == col_id:
                return name
        return "其他"


class BigDataCrawler(BaseCrawler):
    """盐城市大数据集团采集器"""

    SITE_NAME = "盐城市大数据集团"
    BASE_URL = "https://www.ycdatagroup.cn"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    KEYWORDS = ["公告", "中标", "结果", "公示", "招标", "采购"]

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            url = f"{self.BASE_URL}/news/19.html"
            response = self.session.get(url, timeout=30)

            # 强制设置正确的编码
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            if response.status_code == 200:
                projects = self._parse_list(response.text)
                logger.info(f"解析到 {len(projects)} 条数据")

                for project in projects:
                    if self._save_project(project):
                        new_count += 1
                    total_count += 1
        except Exception as e:
            logger.error(f"采集失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')

        # 查找所有链接
        links = soup.find_all('a', href=True)

        logger.debug(f"找到 {len(links)} 个链接")

        for link in links:
            try:
                href = link.get('href', '')
                title = link.text.strip()

                # 过滤：必须是新闻链接
                if not href.startswith('/news/'):
                    continue

                if not title or len(title) < 5:
                    continue

                # 关键词过滤（放宽条件）
                if not any(kw in title for kw in self.KEYWORDS):
                    logger.debug(f"跳过（不包含关键词）: {title}")
                    continue

                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                # 尝试从父元素提取日期
                publish_date = datetime.now().strftime('%Y-%m-%d')

                # 尝试从父元素或兄弟元素中提取日期
                parent = link.parent
                if parent:
                    parent_text = parent.text
                    import re
                    # 查找常见日期格式
                    date_match = re.search(r'(\d{4})[.\-/年](\d{1,2})[.\-/月](\d{1,2})', parent_text)
                    if date_match:
                        year, month, day = date_match.groups()
                        publish_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                # 如果从父元素没有提取到日期，尝试从URL中提取（如果URL包含日期）
                if publish_date == datetime.now().strftime('%Y-%m-%d'):
                    import re
                    url_date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})', href)
                    if url_date_match:
                        year, month, day = url_date_match.groups()
                        publish_date = f"{year}-{month}-{day}"
                parent = link.parent
                if parent:
                    parent_text = parent.text
                    # 查找日期格式: 2026.04.12 或 2026-04-12 或 092026.04
                    import re
                    date_match = re.search(r'(\d{2})(\d{4})\.(\d{1,2})|(\d{4})[.\-](\d{1,2})[.\-](\d{1,2})', parent_text)
                    if date_match:
                        # 处理两种格式：
                        # 格式1: 092026.04 (日月.年份月) -> day=09, year=2026, month=04
                        # 格式2: 2026.04.12 (年份.月份.日期) -> year=2026, month=04, day=12
                        if date_match.group(1):  # 格式1: 092026.04
                            day = date_match.group(1)
                            year = date_match.group(2)
                            month = date_match.group(3)
                            publish_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                        else:  # 格式2: 2026.04.12
                            year = date_match.group(4)
                            month = date_match.group(5)
                            day = date_match.group(6)
                            publish_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'project_type': '公告',
                    'raw_content': str(link)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析链接失败: {e}")
                continue

        return projects


class JscnCrawler(BaseCrawler):
    """江苏世纪新城采集器"""

    SITE_NAME = "江苏世纪新城"
    BASE_URL = "https://jscncg.com"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    KEYWORDS = ["公告", "中标", "结果", "公示"]

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            url = f"{self.BASE_URL}/tenderLease/tender/"
            response = self.session.get(url, timeout=30)

            # 强制设置正确的编码
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            if response.status_code == 200:
                projects = self._parse_list(response.text)
                logger.info(f"解析到 {len(projects)} 条数据")
                for project in projects:
                    if self._save_project(project):
                        new_count += 1
                    total_count += 1
        except Exception as e:
            logger.error(f"采集失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')
        import re

        # 查找所有<li>元素，筛选包含招标链接的
        list_items = soup.find_all('li', myid=True)

        for li in list_items:
            try:
                link = li.find('a', href=True)
                if not link:
                    continue

                href = link.get('href', '')
                title = link.text.strip()

                if not title or len(title) < 5:
                    continue

                # URL格式: /tenderLease/tender/2026-04-10/3711.html
                if not re.match(r'/tenderLease/tender/\d{4}-\d{2}-\d{2}/\d+\.html', href):
                    continue

                # 从URL中提取日期
                date_match = re.search(r'/(\d{4}-\d{2}-\d{2})/', href)
                if date_match:
                    publish_date = date_match.group(1)
                else:
                    publish_date = datetime.now().strftime('%Y-%m-%d')

                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'raw_content': str(li)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue

        return projects


class DongfangCrawler(BaseCrawler):
    """盐城市东方集团采集器"""

    SITE_NAME = "盐城市东方集团"
    BASE_URL = "https://www.orientalgroup.net.cn"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            url = f"{self.BASE_URL}/zbzl/qzzgs/"
            response = self.session.get(url, timeout=30)

            # 强制设置正确的编码
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            if response.status_code == 200:
                projects = self._parse_list(response.text)
                logger.info(f"解析到 {len(projects)} 条数据")
                for project in projects:
                    if self._save_project(project):
                        new_count += 1
                    total_count += 1
        except Exception as e:
            logger.error(f"采集失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')
        import re

        # 查找所有<li>元素（东方集团使用class="col-xs-9"的链接）
        list_items = soup.find_all('li')

        for li in list_items:
            try:
                link = li.find('a', href=True)
                if not link:
                    continue

                href = link.get('href', '')
                title = link.text.strip()

                if not title or len(title) < 5:
                    continue

                # URL格式: /zbzl/qzzgs/2026-04-10/5585.html
                if not re.match(r'/zbzl/qzzgs/\d{4}-\d{2}-\d{2}/\d+\.html', href):
                    continue

                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                # 从URL提取日期
                date_match = re.search(r'/(\d{4}-\d{2}-\d{2})/', detail_url)
                if date_match:
                    publish_date = date_match.group(1)
                else:
                    publish_date = datetime.now().strftime('%Y-%m-%d')
                parent = link.parent
                if parent:
                    parent_text = parent.text
                    # 查找日期格式: 2026.04.12 或 2026-04-12
                    import re
                    date_match = re.search(r'(\d{4})[.\-](\d{1,2})[.\-](\d{1,2})', parent_text)
                    if date_match:
                        publish_date = f"{date_match.group(1)}-{date_match.group(2).zfill(2)}-{date_match.group(3).zfill(2)}"

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'raw_content': str(li)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue

        return projects


class DushiCrawler(BaseCrawler):
    """盐城市都市建设投资集团采集器"""

    SITE_NAME = "盐城市都市建设投资集团"
    BASE_URL = "http://www.ycdsjt.cn"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    KEYWORDS = ["公告", "中标", "结果", "公示", "招标", "采购"]

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        # 采集通知和招标两个分类
        categories = ['tongzhi', 'zhaobiao']

        for cat in categories:
            try:
                url = f"{self.BASE_URL}/?{cat}/"
                logger.debug(f"采集分类: {cat}")

                response = self.session.get(url, timeout=30)

                # 强制设置正确的编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'

                if response.status_code == 200:
                    projects = self._parse_list(response.text, cat)
                    logger.info(f"分类 {cat} 解析到 {len(projects)} 条数据")

                    for project in projects:
                        if self._save_project(project):
                            new_count += 1
                        total_count += 1

                time.sleep(1)
            except Exception as e:
                logger.error(f"采集分类 {cat} 失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str, category: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')

        links = soup.find_all('a', href=True)

        for link in links:
            try:
                href = link.get('href', '')
                title = link.text.strip()

                # 关键词过滤
                if not any(kw in title for kw in self.KEYWORDS):
                    continue

                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                # 访问详情页提取发布时间
                publish_date = self._extract_publish_date(detail_url)

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'project_type': category,
                    'raw_content': str(link)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue

        return projects

    def _extract_publish_date(self, detail_url: str) -> str:
        """从详情页提取发布时间"""
        try:
            response = self.session.get(detail_url, timeout=30)
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')

                # 查找包含"发布时间"的元素
                all_text = soup.get_text()
                import re
                date_match = re.search(r'发布时间[：:]\s*(\d{4}-\d{2}-\d{2})', all_text)
                if date_match:
                    return date_match.group(1)

                # 备用：查找"20XX年X月X日"格式
                date_match = re.search(r'(20\d{2}年\d{1,2}月\d{1,2}日)', all_text)
                if date_match:
                    date_str = date_match.group(1)
                    date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
                    if date_match:
                        year, month, day = date_match.groups()
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        except Exception as e:
            logger.warning(f"提取发布时间失败: {e}")

        return datetime.now().strftime('%Y-%m-%d')


class ChengnanCrawler(BaseCrawler):
    """城南新区公共资源交易网采集器"""

    SITE_NAME = "城南新区公共资源交易网"
    BASE_URL = "http://221.231.11.22:8099"
    REGIONAL_COMPANY = True  # 全量采集，标记为"盐南高新区"

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            url = f"{self.BASE_URL}/jyxx/tradeInfo.html"
            response = self.session.get(url, timeout=30)

            # 强制设置正确的编码
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'

            if response.status_code == 200:
                projects = self._parse_list(response.text)
                logger.info(f"解析到 {len(projects)} 条数据")

                for project in projects:
                    if self._save_project(project):
                        new_count += 1
                    total_count += 1
        except Exception as e:
            logger.error(f"采集失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')
        import re

        # 查找所有链接
        links = soup.find_all('a', href=True)

        for link in links:
            try:
                href = link.get('href', '')
                title = link.text.strip()

                # 匹配项目链接格式: /jyxx/数字/数字/日期/UUID.html
                if not re.match(r'/jyxx/\d+/\d+/\d{8}/[a-f0-9\-]+\.html', href):
                    continue

                if not title or len(title) < 5:
                    continue

                # 提取日期
                date_match = re.search(r'/(\d{8})/', href)
                if date_match:
                    date_str = date_match.group(1)
                    publish_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                else:
                    publish_date = datetime.now().strftime('%Y-%m-%d')

                # 构建完整URL
                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'raw_content': str(link)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue

        return projects


class JingkaiCrawler(BaseCrawler):
    """经开城发集团采集器"""

    SITE_NAME = "经开城发集团"
    BASE_URL = "http://www.ycjkct.com"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    KEYWORDS = ["公告", "中标", "结果", "公示", "招标", "采购", "通知"]

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        # 采集招标信息和中标信息两个分类
        categories = [
            ('zbxx', '招标信息'),
            ('zbgs', '中标信息')
        ]

        for cat_code, cat_name in categories:
            try:
                url = f"{self.BASE_URL}/zbcg/{cat_code}/"
                logger.debug(f"采集分类: {cat_name}")

                response = self.session.get(url, timeout=30)

                # 强制设置正确的编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'

                if response.status_code == 200:
                    projects = self._parse_list(response.text, cat_name)
                    logger.info(f"分类 {cat_name} 解析到 {len(projects)} 条数据")

                    for project in projects:
                        if self._save_project(project):
                            new_count += 1
                        total_count += 1

                time.sleep(1)
            except Exception as e:
                logger.error(f"采集分类 {cat_name} 失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str, category: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')

        # 查找主要内容区域
        main_content = soup.find('div', class_=lambda x: x and 'main' in x.lower()) or soup.find('main') or soup.find('div', class_=lambda x: x and 'content' in x.lower())

        if main_content:
            # 在主要内容区域查找li元素
            list_items = main_content.find_all('li')
            logger.debug(f"在主要内容区域找到 {len(list_items)} 个li元素")
        else:
            # 如果没有找到主要内容区域，则查找所有li
            list_items = soup.find_all('li')
            logger.debug(f"在全局找到 {len(list_items)} 个li元素")

        for li in list_items:
            try:
                link = li.find('a')
                if not link:
                    continue

                href = link.get('href', '')
                title = link.text.strip()

                # 过滤：必须是有效的标题
                if not title or len(title) < 5 or title in ['更多', '查看更多', '首页']:
                    continue

                # 关键词过滤 - 只过滤纯导航链接
                if any(nav in title for nav in ['首页', '联系我们', '集团介绍', '业务板块', '新闻中心']):
                    continue

                if not href.startswith('http'):
                    detail_url = self.BASE_URL + href
                else:
                    detail_url = href

                # 只采集招标采购相关的链接
                if not ('/zbcg/' in detail_url):
                    continue

                # 从URL提取日期: /zbcg/zbxx/2026-04-12/123.html
                import re
                date_match = re.search(r'/(\d{4}-\d{2}-\d{2})/', detail_url)
                if date_match:
                    publish_date = date_match.group(1)
                else:
                    publish_date = datetime.now().strftime('%Y-%m-%d')

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': title,
                    'publish_date': publish_date,
                    'detail_url': detail_url,
                    'project_type': category,
                    'raw_content': str(li)
                }

                projects.append(project)
            except Exception as e:
                logger.warning(f"解析列表项失败: {e}")
                continue

        return projects


class YuedaCrawler(BaseCrawler):
    """悦达集团采集器"""

    SITE_NAME = "悦达集团"
    BASE_URL = "http://www.ydtender.com"
    REGIONAL_COMPANY = True  # 区域内公司，全量采集

    KEYWORDS = ["公告", "中标", "结果", "公示", "招标", "采购", "评审"]

    # 12个子分类
    CATEGORIES = [
        ('zbgg', '综合公告'),
        ('zgcgg', '工程公告'),
        ('zhwgg', '货物公告'),
        ('zfwgg', '服务公告'),
        ('jgcgg', '结果公告-工程'),
        ('jhwgg', '结果公告-货物'),
        ('jfwgg', '结果公告-服务'),
        ('pgcgg', '评审公示-工程'),
        ('phwgg', '评审公示-货物'),
        ('pfwgg', '评审公示-服务'),
        ('yyzbgg', '运营采购公告'),
        ('yyjggg', '运营结果公告')
    ]

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        for cat_code, cat_name in self.CATEGORIES:
            try:
                url = f"{self.BASE_URL}/{cat_code}/index.jhtml"
                logger.debug(f"采集分类: {cat_name}")

                response = self.session.get(url, timeout=30)

                # 强制设置正确的编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'

                if response.status_code == 200:
                    projects = self._parse_list(response.text, cat_name)
                    logger.info(f"分类 {cat_name} 解析到 {len(projects)} 条数据")

                    for project in projects:
                        if self._save_project(project):
                            new_count += 1
                        total_count += 1

                time.sleep(1)
            except Exception as e:
                logger.error(f"采集分类 {cat_name} 失败: {e}")

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _parse_list(self, html: str, category: str) -> List[Dict]:
        """解析列表页"""
        projects = []
        soup = BeautifulSoup(html, 'lxml')

        # 查找List2容器
        list_divs = soup.find_all('div', class_='List2')
        logger.debug(f"找到 {len(list_divs)} 个List2容器")

        for list_div in list_divs:
            # 查找内部的li元素
            li_items = list_div.find_all('li')
            logger.debug(f"List2容器内找到 {len(li_items)} 个li元素")

            for li in li_items:
                try:
                    link = li.find('a')
                    if not link:
                        continue

                    href = link.get('href', '')
                    title = link.text.strip()

                    # 过滤：必须是有效的标题
                    if not title or len(title) < 10 or title in ['更多', '查看更多', '首页']:
                        continue

                    if not href.startswith('http'):
                        detail_url = self.BASE_URL + href
                    else:
                        detail_url = href

                    # 尝试提取发布时间
                    publish_date = datetime.now().strftime('%Y-%m-%d')

                    # 查找包含"Gray" class的元素（可能是span或p）
                    gray_element = li.find(class_='Gray')
                    if gray_element:
                        gray_str = gray_element.text
                        # 查找发布时间: 格式如 "发布时间：2026-04-10 23:04:00"
                        import re
                        date_match = re.search(r'发布时间[：:]\s*(\d{4}-\d{2}-\d{2})', gray_str)
                        if date_match:
                            publish_date = date_match.group(1)

                    project = {
                        'source_site': self.SITE_NAME,
                        'source_url': self.BASE_URL,
                        'project_name': title,
                        'publish_date': publish_date,
                        'detail_url': detail_url,
                        'project_type': category,
                        'raw_content': str(li)
                    }

                    projects.append(project)
                except Exception as e:
                    logger.warning(f"解析列表项失败: {e}")
                    continue

        return projects


class KfqaCrawler(BaseCrawler):
    """开发区公共资源交易网采集器"""

    SITE_NAME = "开发区公共资源交易网"
    BASE_URL = "http://218.92.181.186:8081"
    LIST_URL = "http://218.92.181.186:8081/jyxx/about.html"
    REGION_KEYWORDS = ["盐南高新区", "经开区", "经济技术开发区", "开发区", "步凤镇", "新城街道"]
    REGIONAL_COMPANY = False  # 需要区域筛选

    def __init__(self, db_manager: DatabaseManager):
        super().__init__(db_manager)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'http://218.92.181.186:8081/'
        }

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            # 访问列表页
            response = self.session.get(
                self.LIST_URL,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                timeout=30
            )
            response.encoding = 'utf-8'

            if response.status_code != 200:
                logger.error(f"访问列表页失败: {response.status_code}")
                return {"total": 0, "new": 0, "region_match": 0}

            soup = BeautifulSoup(response.text, 'lxml')

            # 提取所有链接
            links = soup.find_all('a', href=True)
            logger.info(f"找到 {len(links)} 个链接")

            for link in links:
                try:
                    href = link.get('href', '')
                    title = link.get('title', '').strip()

                    # 筛选有效的招投标链接
                    if not href or not href.startswith('/jyxx/'):
                        continue

                    # 跳过导航链接
                    if 'about.html' in href or 'tradeInfo.html' in href:
                        continue

                    # 构建完整URL
                    detail_url = self.BASE_URL + href

                    # 如果没有title，从链接文本提取
                    if not title:
                        title = link.get_text(strip=True)

                    if not title or len(title) < 5:
                        continue

                    # 从URL提取发布日期
                    date_match = self._extract_date_from_url(href)
                    publish_date = date_match if date_match else datetime.now().strftime('%Y-%m-%d')

                    # 区域匹配（所有数据都与经开区相关，标记为"区域内"）
                    region = "经开区"  # 开发区公共资源交易网的所有数据都是经开区相关

                    # 提取详情内容
                    detail_response = self.session.get(
                        detail_url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                        timeout=30
                    )
                    detail_response.encoding = 'utf-8'

                    if detail_response.status_code == 200:
                        detail_soup = BeautifulSoup(detail_response.text, 'lxml')
                        content_div = detail_soup.find('div', class_='ewb-article-info')
                        content = content_div.get_text(strip=True) if content_div else ""

                        # 构建项目数据
                        project = {
                            'id': self._generate_project_id(title, publish_date, self.SITE_NAME),
                            'hash': self._generate_content_hash(title, publish_date, detail_url, content),
                            'source_site': self.SITE_NAME,
                            'source_url': detail_url,
                            'detail_url': detail_url,
                            'publish_date': publish_date,
                            'project_name': title,
                            'region': region,
                            'raw_content': content[:5000] if content else "",
                            'description': content[:500] if content else ""
                        }

                        total_count += 1

                        # 使用BaseCrawler的_save_project方法保存数据
                        if self._save_project(project):
                            new_count += 1
                            logger.info(f"✅ 新增项目: {title}")

                    # 添加延时避免请求过快
                    time.sleep(0.5)

                except Exception as e:
                    logger.error(f"处理链接时出错: {str(e)}")
                    continue

            logger.info(f"{self.SITE_NAME} 采集完成 - 总计: {total_count}条, 新增: {new_count}条")
            return {"total": total_count, "new": new_count}

        except Exception as e:
            logger.error(f"{self.SITE_NAME} 采集失败: {str(e)}")
            return {"total": 0, "new": 0, "region_match": 0}

    def _generate_project_id(self, title: str, publish_date: str, site: str) -> str:
        """生成项目ID"""
        content = f"{title}|{publish_date}|{site}"
        return hashlib.md5(content.encode()).hexdigest()

    def _generate_content_hash(self, title: str, publish_date: str, url: str, content: str) -> str:
        """生成内容哈希"""
        import json
        data = {
            'title': title,
            'publish_date': publish_date,
            'url': url,
            'content': content[:1000]  # 只使用前1000字符计算哈希
        }
        content_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(content_str.encode()).hexdigest()

    def _extract_date_from_url(self, url: str) -> Optional[str]:
        """从URL中提取日期"""
        # URL格式: /jyxx/002003/002003001/20260410/dbcfa17f-cd20-4127-961e-17706291c338.html
        import re
        pattern = r'/(\d{4})(\d{2})(\d{2})/'
        match = re.search(pattern, url)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month}-{day}"
        return None

class SufuCrawler(BaseCrawler):
    """苏服采采集器 - 使用Playwright模拟浏览器操作，完全按照 sufu-workflow.md 实现"""

    SITE_NAME = "苏服采"
    BASE_URL = "https://js.fwgov.cn"
    REGIONAL_COMPANY = True  # 已经通过地区选择过滤，标记为"区域内"

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据 - 使用JavaScript执行地区选择，失败时跳过采集"""
        logger.info(f"开始采集: {self.SITE_NAME} (使用JavaScript地区选择)")

        total_count = 0
        new_count = 0

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # 访问苏服采公开比选页面
                page.goto(f"{self.BASE_URL}/bidding?serviceType=1")
                page.wait_for_load_state('networkidle')
                logger.info("页面加载完成")
                # 增加等待时间，确保页面完全稳定
                time.sleep(5)

                # 截图保存初始页面
                os.makedirs('./招投标数据/screenshots', exist_ok=True)
                screenshot_path = f'./招投标数据/screenshots/苏服采_初始页面_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                page.screenshot(path=screenshot_path)
                logger.info(f"初始页面截图已保存: {screenshot_path}")

                # 检查是否需要登录（更精确的检测）
                login_check = page.evaluate("""
                    () => {
                        const title = document.title || '';
                        const bodyText = document.body.innerText || '';

                        // 检查是否真的在登录页面
                        const isLoginPage = bodyText.includes('登录') &&
                                          (bodyText.includes('账号') || bodyText.includes('密码') || bodyText.includes('用户名'));

                        // 检查是否有登录表单
                        const hasLoginForm = document.querySelector('.login-form, .login-container, [class*="login"]');

                        // 检查页面是否包含地区选择框（正常页面应该有）
                        const hasRegionSelect = document.querySelector('.ivu-select');

                        return {
                            hasLogin: isLoginPage && hasLoginForm,
                            hasRegionSelect: hasRegionSelect,
                            title: title,
                            bodyTextLength: bodyText.length
                        };
                    }
                """)

                logger.info(f"页面检查: 标题='{login_check.get('title')}', 有地区选择框={login_check.get('hasRegionSelect')}")

                # 只有在确实检测到登录页面且没有地区选择框时才跳过
                if login_check.get('hasLogin') and not login_check.get('hasRegionSelect'):
                    logger.warning(f"检测到登录界面（页面标题: {login_check.get('title')}），跳过采集")
                    browser.close()
                    return {"total": 0, "new": 0}

                # 根据您的截图，页面有3个选择框，第三个是地区选择框
                # 直接操作第三个选择框，搜索"盐南高新区"和"经开区"
                region_selected = False
                try:
                    set_region_script = """
                    async () => {
                        let logs = [];
                        function log(msg) { logs.push(msg); }

                        log('开始地区筛选（使用第三个选择框）...');

                        // 查找所有选择框
                        let selectContainers = document.querySelectorAll('.ivu-select-selection');
                        log(`找到 ${selectContainers.length} 个选择框容器`);

                        if (selectContainers.length < 3) {
                            log('❌ 选择框数量不足');
                            return {status: 'error', logs: logs};
                        }

                        // 使用第三个选择框（索引2）
                        const regionSelect = selectContainers[2];
                        const currentText = regionSelect.innerText || '';
                        log(`第三个选择框当前选择: ${currentText}`);

                        // 点击打开下拉菜单
                        log('点击第三个选择框，打开下拉菜单...');
                        regionSelect.click();
                        await new Promise(r => setTimeout(r, 800));

                        log('✓ 下拉菜单已打开');

                        // 查找输入框
                        let inputElement = document.querySelector('.ivu-select-dropdown input[type="text"]');
                        if (!inputElement) {
                            inputElement = document.querySelector('.ivu-select-dropdown .ivu-input');
                        }
                        if (!inputElement) {
                            inputElement = document.querySelector('.ivu-select-dropdown input');
                        }

                        if (!inputElement) {
                            log('❌ 未找到输入框，尝试直接勾选');
                            // 如果没有输入框，尝试直接查找选项
                            const allOptions = document.querySelectorAll('.ivu-select-dropdown-list .ivu-select-item');
                            log(`找到 ${allOptions.length} 个选项`);

                            let yannanFound = false;
                            let jingkaiFound = false;

                            // 勾选"盐南高新区"（精确匹配"江苏省 / 盐城市 / 盐南高新区"）
                            for (const opt of allOptions) {
                                const optText = opt.innerText || '';
                                // 必须是盐城市下的盐南高新区
                                if (optText === '江苏省 / 盐城市 / 盐南高新区') {
                                    log(`勾选: ${optText}`);
                                    opt.click();
                                    await new Promise(r => setTimeout(r, 500));
                                    log('✓ 已勾选盐南高新区');
                                    yannanFound = true;
                                    break;
                                }
                            }

                            // 等待一下，再查找经开区
                            await new Promise(r => setTimeout(r, 600));

                            const allOptions2 = document.querySelectorAll('.ivu-select-dropdown-list .ivu-select-item');
                            for (const opt of allOptions2) {
                                const optText = opt.innerText || '';
                                // 必须是盐城市下的经开区，不要常州经开区、镇江经开区等
                                if (optText === '江苏省 / 盐城市 / 经开区') {
                                    log(`勾选: ${optText}`);
                                    opt.click();
                                    await new Promise(r => setTimeout(r, 500));
                                    log('✓ 已勾选盐城市经开区');
                                    jingkaiFound = true;
                                    break;
                                }
                            }

                            // 点击网页空白处
                            await new Promise(r => setTimeout(r, 500));
                            document.body.click();
                            await new Promise(r => setTimeout(r, 800));

                            if (yannanFound && jingkaiFound) {
                                return {status: 'success', logs: logs};
                            } else {
                                log('⚠️  部分选项未找到');
                                return {status: 'partial', logs: logs};
                            }
                        }

                        // 第一步：搜索"盐南高新区"
                        log('步骤1: 搜索"盐南高新区"...');
                        inputElement.focus();
                        inputElement.value = '';

                        // 逐字输入
                        const text1 = '盐南高新区';
                        for (let char of text1) {
                            inputElement.value += char;
                            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
                            await new Promise(r => setTimeout(r, 50));
                        }
                        inputElement.dispatchEvent(new Event('change', { bubbles: true }));
                        await new Promise(r => setTimeout(r, 800));
                        log('✓ 已输入"盐南高新区"');

                        // 等待搜索结果
                        await new Promise(r => setTimeout(r, 800));

                        // 勾选"盐南高新区"
                        const options1 = document.querySelectorAll('.ivu-select-dropdown-list .ivu-select-item');
                        log(`搜索"盐南高新区"后找到 ${options1.length} 个选项`);

                        let yannanFound = false;
                        for (const opt of options1) {
                            const optText = opt.innerText || '';
                            // 必须是盐城市下的盐南高新区
                            if (optText === '江苏省 / 盐城市 / 盐南高新区') {
                                log(`勾选: ${optText}`);
                                opt.click();
                                await new Promise(r => setTimeout(r, 500));
                                log('✓ 已勾选盐南高新区');
                                yannanFound = true;
                                break;
                            }
                        }

                        if (!yannanFound) {
                            log('⚠️  未找到"盐南高新区"选项');
                        }

                        // 第二步：搜索"经开区"
                        await new Promise(r => setTimeout(r, 600));

                        log('步骤2: 搜索"经开区"...');
                        inputElement.focus();
                        inputElement.value = '';

                        // 逐字输入
                        const text2 = '经开区';
                        for (let char of text2) {
                            inputElement.value += char;
                            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
                            await new Promise(r => setTimeout(r, 50));
                        }
                        inputElement.dispatchEvent(new Event('change', { bubbles: true }));
                        await new Promise(r => setTimeout(r, 800));
                        log('✓ 已输入"经开区"');

                        // 等待搜索结果
                        await new Promise(r => setTimeout(r, 800));

                        // 勾选"经开区"
                        const options2 = document.querySelectorAll('.ivu-select-dropdown-list .ivu-select-item');
                        log(`搜索"经开区"后找到 ${options2.length} 个选项`);

                        let jingkaiFound = false;
                        for (const opt of options2) {
                            const optText = opt.innerText || '';
                            // 必须是盐城市下的经开区，不要常州经开区、镇江经开区等
                            if (optText === '江苏省 / 盐城市 / 经开区') {
                                log(`勾选: ${optText}`);
                                opt.click();
                                await new Promise(r => setTimeout(r, 500));
                                log('✓ 已勾选盐城市经开区');
                                jingkaiFound = true;
                                break;
                            }
                        }

                        if (!jingkaiFound) {
                            log('⚠️  未找到"经开区"选项');
                        }

                        // 点击网页空白处，隐藏下拉框
                        log('点击网页空白处，隐藏下拉框...');
                        await new Promise(r => setTimeout(r, 500));
                        document.body.click();
                        await new Promise(r => setTimeout(r, 800));

                        log('✓ 下拉框已隐藏，等待页面刷新...');

                        if (yannanFound && jingkaiFound) {
                            return {status: 'success', logs: logs};
                        } else {
                            log('⚠️  部分选项未找到');
                            return {status: 'partial', logs: logs};
                        }
                    }
                    """

                    result = page.evaluate(set_region_script)
                    logger.info(f"地区筛选结果: {result['status']}")

                    # 打印详细日志
                    if 'logs' in result:
                        for log in result['logs']:
                            logger.info(f"  {log}")

                    if result['status'] == 'success':
                        logger.info("地区筛选完成：江苏省 → 盐城市 → [盐南高新区 + 经开区]")
                        region_selected = True
                        # 截图保存筛选后的页面
                        screenshot_path2 = f'./招投标数据/screenshots/苏服采_筛选后_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                        page.screenshot(path=screenshot_path2)
                        logger.info(f"筛选后页面截图已保存: {screenshot_path2}")
                    else:
                        logger.warning(f"地区筛选未完成: {result['status']}")
                        # 如果地区选择失败，跳过采集
                        logger.warning("地区选择失败，跳过苏服采数据采集")
                        browser.close()
                        return {"total": 0, "new": 0}

                except Exception as e:
                    logger.warning(f"地区筛选操作失败: {e}")
                    logger.warning("地区选择失败，跳过苏服采数据采集")
                    browser.close()
                    return {"total": 0, "new": 0}

                # 等待数据刷新（页面会自动监听选择变化并刷新）
                # 增加等待时间，确保数据完全加载
                logger.info("等待页面数据刷新...")
                time.sleep(20)  # 增加到20秒

                # 检查页面是否真的刷新了（查看项目列表）
                refresh_check = page.evaluate("""
                    () => {
                        const projectCards = document.querySelectorAll('.ivu-card, .ivu-list-item, [class*="project"], [class*="bidding"]');
                        return {
                            projectCount: projectCards.length,
                            hasData: projectCards.length > 0
                        };
                    }
                """)
                
                logger.info(f"页面刷新检查: 项目数={refresh_check.get('projectCount')}, 有数据={refresh_check.get('hasData')}")

                # 提取项目数据
                if region_selected:
                    projects = self._extract_project_cards(page)
                    logger.info(f"提取到 {len(projects)} 条数据")

                    # 验证数据：检查是否只包含盐南高新区和经开区的项目
                    project_regions = {}
                    for project in projects:
                        title = project.get('title', '')
                        purchaser = project.get('purchaser', '')
                        region = 'other'

                        # 根据采购人判断区域
                        if any(kw in purchaser for kw in ['盐南', '城南', '开发区', '经开', '新河', '伍佑', '新都']):
                            region = 'target'

                        project_regions[title[:30]] = region

                    target_count = sum(1 for r in project_regions.values() if r == 'target')
                    logger.info(f"区域匹配统计: 目标区域 {target_count}/{len(projects)}")

                    for project in projects:
                        # 过滤掉响应截止的项目 - 检查 project_type、response_time 和 project_name
                        project_type = project.get('project_type', '')
                        response_time = project.get('response_time', '')
                        project_name = project.get('project_name', '')

                        # 检查是否为"响应截止"状态
                        is_deadline = (
                            '响应截止' in project_type or
                            '响应截止' in response_time or
                            '响应截止' in project_name
                        )

                        if is_deadline:
                            logger.debug(f"跳过响应截止项目: {project_name[:50]}")
                            continue

                        if self._save_project(project):
                            new_count += 1
                        total_count += 1
                else:
                    logger.warning("地区未选择成功，不提取数据")
                    browser.close()
                    return {"total": 0, "new": 0}

                # 最终截图
                screenshot_path3 = f'./招投标数据/screenshots/苏服采_采集完成_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                page.screenshot(path=screenshot_path3)
                logger.info(f"采集完成截图已保存: {screenshot_path3}")

                browser.close()

        except ImportError:
            logger.error("Playwright未安装，请先安装: pip install playwright && playwright install chromium")
            return {"total": 0, "new": 0}
        except Exception as e:
            logger.error(f"{self.SITE_NAME} 采集失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return {"total": 0, "new": 0}

        logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
        return {"total": total_count, "new": new_count}

    def _extract_project_cards(self, page) -> List[Dict]:
        """提取项目卡片信息 - 使用JavaScript智能提取"""
        projects = []

        try:
            # 根据截图分析，苏服采使用卡片式布局
            # 每个项目卡片应该包含：项目状态、项目名称、响应时间、预算、发布时间、采购单位
            script = """
            () => {
                const projectData = [];

                // 查找所有包含项目信息的卡片或列表项
                const possibleSelectors = [
                    '.bidding-list-item',
                    '.project-item',
                    '.service-item',
                    '[class*="project-card"]',
                    '[class*="bidding-card"]',
                    '.ivu-card',
                    '.el-card',
                    '.list-item'
                ];

                let cards = [];
                for (const selector of possibleSelectors) {
                    const elements = document.querySelectorAll(selector);
                    if (elements.length > 0) {
                        console.log(`Found ${elements.length} elements with selector: ${selector}`);
                        cards = Array.from(elements);
                        break;
                    }
                }

                // 如果没有找到卡片，尝试查找包含"响应开始"或"响应截止"的元素
                if (cards.length === 0) {
                    const allElements = document.querySelectorAll('*');
                    for (const el of allElements) {
                        const text = el.innerText || '';
                        if ((text.includes('响应开始') || text.includes('响应截止')) &&
                            text.length > 20 && text.length < 200) {
                            cards.push(el);
                        }
                    }
                }

                for (const card of cards) {
                    try {
                        const cardText = card.innerText || '';

                        // 过滤条件：必须包含项目相关信息
                        if (!cardText.includes('响应') ||
                            cardText.length < 20 ||
                            cardText.includes('注册') ||
                            cardText.includes('登录') ||
                            cardText.includes('上传') ||
                            cardText.includes('投诉') ||
                            cardText.includes('反馈') ||
                            (cardText.includes('供应商') && !cardText.includes('采购单位'))) {
                            continue;
                        }

                        // 提取项目状态
                        let status = '';
                        if (cardText.includes('响应即将开始')) {
                            status = '响应即将开始';
                        } else if (cardText.includes('响应中')) {
                            status = '响应中';
                        } else if (cardText.includes('响应截止')) {
                            status = '响应截止';
                        }

                        // 过滤响应截止的项目
                        if (status === '响应截止') {
                            continue;
                        }

                        // 提取项目名称 - 通常是第一个长的文本行
                        const lines = cardText.split('\\n').map(l => l.trim()).filter(l => l.length > 5);
                        let title = '';
                        let budget = '';
                        let publishTime = '';
                        let purchaser = '';
                        let responseTime = '';

                        // 解析各行文本
                        for (let i = 0; i < lines.length; i++) {
                            const line = lines[i];

                            // 查找项目名称（通常不包含特殊关键词）
                            if (!title &&
                                !line.includes('响应') &&
                                !line.includes('预算') &&
                                !line.includes('发布') &&
                                !line.includes('采购单位') &&
                                !line.includes('元') &&
                                line.length > 5 && line.length < 100) {
                                title = line;
                            }

                            // 查找预算（包含"元"）
                            if (line.includes('元') && !budget) {
                                budget = line;
                            }

                            // 查找发布时间（包含日期格式）
                            if (line.match(/\\d{4}\\.\\d+\\.\\d+/) && !publishTime) {
                                publishTime = line;
                            }

                            // 查找采购单位
                            if (line.includes('采购单位') && !purchaser) {
                                purchaser = line.replace('采购单位：', '').trim();
                            }

                            // 查找响应时间
                            if ((line.includes('响应开始') || line.includes('响应截止')) && !responseTime) {
                                responseTime = line;
                            }
                        }

                        // 如果找到了有效的标题，则添加到结果
                        if (title && title.length > 5) {
                            projectData.push({
                                status,
                                title,
                                budget,
                                publishTime,
                                purchaser,
                                responseTime
                            });
                        }

                    } catch (e) {
                        continue;
                    }
                }

                console.log(`Extracted ${projectData.length} valid projects`);
                return projectData;
            }
            """

            project_cards = page.evaluate(script)
            logger.info(f"JavaScript提取到 {len(project_cards)} 个有效项目")

            # 转换为标准格式
            for card in project_cards:
                # 解析发布时间 - 优先使用 publishTime，如果没有则使用 responseTime
                publish_time_text = card.get('publishTime', '')
                if not publish_time_text:
                    publish_time_text = card.get('responseTime', '')

                # 尝试从 publishTime 或 responseTime 中提取日期
                publish_date = self._parse_date(publish_time_text)

                # 如果仍然没有提取到有效日期，使用当前日期
                if not publish_date or '距响应截止' in publish_date:
                    logger.warning(f"无法从以下文本提取有效日期: {publish_time_text}")
                    # 尝试从 responseTime 中计算实际日期
                    import re
                    match = re.search(r'距响应截止：(\d+)天(\d+)时(\d+)分', publish_time_text)
                    if match:
                        days = int(match.group(1))
                        from datetime import datetime
                        # 假设响应截止时间是相对于采集时间的未来时间
                        # 计算发布日期 = 采集日期 - 截止天数
                        publish_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
                        logger.info(f"从响应时间计算发布日期: {publish_date}")
                    else:
                        # 如果无法计算，使用当前日期
                        publish_date = datetime.now().strftime('%Y-%m-%d')
                        logger.warning(f"使用当前日期作为发布日期: {publish_date}")

                project = {
                    'source_site': self.SITE_NAME,
                    'source_url': self.BASE_URL,
                    'project_name': card.get('title', ''),
                    'publish_date': publish_date,
                    'detail_url': f"{self.BASE_URL}/bidding",
                    'project_type': card.get('status', ''),
                    'budget': card.get('budget', ''),
                    'purchaser': card.get('purchaser', ''),
                    'response_time': card.get('responseTime', ''),
                    'raw_content': str(card)
                }

                projects.append(project)

        except Exception as e:
            logger.error(f"提取项目卡片失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())

        return projects
class YanchengCityGovCrawler(BaseCrawler):
    """盐城市人民政府网采集器（市政府官网）"""

    SITE_NAME = "盐城市人民政府网"
    BASE_URL = "https://www.yancheng.gov.cn"
    SEARCH_URL = "https://www.yancheng.gov.cn/module/xxgk/search_custom.jsp"
    REGIONAL_COMPANY = False  # 需要区域筛选

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            # 计算日期范围
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            days_diff = (end - start).days + 1

            # 分页采集，每页15条记录
            page_size = 15
            max_pages = 140  # 根据网站显示的最大页数

            for page in range(1, min(max_pages + 1, days_diff + 1)):  # 限制页数
                logger.debug(f"正在采集第 {page} 页...")

                try:
                    # 构建请求参数
                    params = {
                        'fieldConfigId': 38195,
                        'area': '',
                        'infotypeId': 'A00025A00010A00001,A00025A00010A00002,A00025A00010A00003,A00025A00010A00004,A00025A00010A00005,A00025A00010A00006,A00025A00010A00007',
                        'jdid': 1,
                        'fields': '',
                        'hasNoPages': 0,
                        'infoCount': 15,
                        'sortfield': 'createdatetime:0',
                        'currpage': page
                    }

                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Referer': f'{self.BASE_URL}/col/col16735/index.html'
                    }

                    response = requests.get(self.SEARCH_URL, params=params, headers=headers, timeout=10)

                    # 检查编码
                    if response.encoding == 'ISO-8859-1':
                        response.encoding = 'utf-8'

                    if response.status_code != 200:
                        logger.warning(f"第 {page} 页请求失败: {response.status_code}")
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')

                    # 提取表格行
                    rows = soup.find_all('tr', class_=['tr_main_value_odd', 'tr_main_value_even'])

                    if not rows:
                        logger.debug(f"第 {page} 页没有数据，停止采集")
                        break

                    for row in rows:
                        try:
                            # 提取链接和标题
                            link_tag = row.find('a')
                            if not link_tag:
                                continue

                            title = link_tag.get('title', '').strip()
                            detail_url = link_tag.get('href', '').strip()

                            if not detail_url:
                                continue

                            # 确保URL是完整的
                            if detail_url.startswith('http'):
                                pass
                            elif detail_url.startswith('/'):
                                detail_url = self.BASE_URL + detail_url
                            else:
                                detail_url = f"{self.BASE_URL}/{detail_url}"

                            # 提取日期
                            date_text = row.find('td', align='right').get_text(strip=True)
                            date_text = date_text.replace('[', '').replace(']', '')
                            publish_date = self._parse_date(date_text)

                            if not publish_date:
                                continue

                            # 检查日期范围
                            publish_dt = datetime.strptime(publish_date, '%Y-%m-%d')
                            if publish_dt < start or publish_dt > end:
                                continue

                            # 构建项目数据
                            project_data = {
                                'source_site': self.SITE_NAME,
                                'source_url': detail_url,
                                'publish_date': publish_date,
                                'project_name': title,
                                'budget': None,
                                'budget_text': None,
                                'detail_url': detail_url,
                                'region': self._match_region(title),
                                'purchaser': None,
                                'deadline': None,
                                'project_type': None,
                                'procurement_method': None,
                                'contact_name': None,
                                'contact_phone': None,
                                'industry': None,
                                'description': None,
                                'raw_content': None
                            }

                            # 存储到数据库
                            is_new, project = self.db_manager.save_project(project_data)
                            total_count += 1
                            if is_new:
                                new_count += 1
                                logger.debug(f"新增项目: {title}")

                        except Exception as e:
                            logger.error(f"解析项目失败: {e}")
                            continue

                except Exception as e:
                    logger.error(f"采集第 {page} 页失败: {e}")
                    continue

            logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
            return {"total": total_count, "new": new_count}

        except Exception as e:
            logger.error(f"{self.SITE_NAME} 采集失败: {e}")
            return {"total": 0, "new": 0}


class HnzbcgxxwCrawler(BaseCrawler):
    """全国招标采购公共服务平台采集器"""

    SITE_NAME = "全国招标采购公共服务平台"
    BASE_URL = "https://www.hnzbcgxxw.com"
    REGIONAL_COMPANY = False  # 需要区域筛选

    def crawl(self, start_date: str, end_date: str) -> Dict:
        """采集数据"""
        logger.info(f"开始采集: {self.SITE_NAME}")

        total_count = 0
        new_count = 0

        try:
            # 计算日期范围
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            days_diff = (end - start).days + 1

            # 采集多个分类
            categories = [
                {'id': 4, 'name': '招标/采购公告'},
                {'id': 5, 'name': '中标/成交公告'},
                {'id': 6, 'name': '变更/补充公告'},
                {'id': 10, 'name': '其他公告/公示'}
            ]

            for category in categories:
                logger.debug(f"正在采集分类: {category['name']}")

                try:
                    page = 1
                    category_count = 0

                    while True:
                        try:
                            url = f"{self.BASE_URL}/list/{category['id']}.html?page={page}"

                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                            }

                            response = requests.get(url, headers=headers, timeout=10)

                            # 检查编码
                            if response.encoding == 'ISO-8859-1':
                                response.encoding = 'utf-8'

                            if response.status_code != 200:
                                logger.warning(f"分类 {category['name']} 第 {page} 页请求失败: {response.status_code}")
                                break

                            soup = BeautifulSoup(response.text, 'html.parser')

                            # 提取列表项
                            list_items = soup.find_all('li', class_='info_list_li')

                            if not list_items:
                                logger.debug(f"分类 {category['name']} 第 {page} 页没有数据，停止采集")
                                break

                            logger.debug(f"分类 {category['name']} 第 {page} 页找到 {len(list_items)} 条数据")

                            for item in list_items:
                                try:
                                    # 提取链接和标题
                                    link_tag = item.find('a')
                                    if not link_tag:
                                        continue

                                    title = link_tag.get_text(strip=True)
                                    detail_url = link_tag.get('href', '').strip()

                                    if not detail_url:
                                        continue

                                    # 确保URL是完整的
                                    if detail_url.startswith('http'):
                                        pass
                                    elif detail_url.startswith('/'):
                                        detail_url = self.BASE_URL + detail_url
                                    else:
                                        detail_url = f"{self.BASE_URL}/{detail_url}"

                                    # 提取日期
                                    date_span = item.find('span')
                                    if not date_span:
                                        continue

                                    date_text = date_span.get_text(strip=True)
                                    publish_date = self._parse_date(date_text)

                                    if not publish_date:
                                        continue

                                    # 检查日期范围
                                    publish_dt = datetime.strptime(publish_date, '%Y-%m-%d')
                                    if publish_dt < start or publish_dt > end:
                                        continue

                                    # 构建项目数据
                                    project_data = {
                                        'source_site': self.SITE_NAME,
                                        'source_url': detail_url,
                                        'publish_date': publish_date,
                                        'project_name': title,
                                        'budget': None,
                                        'budget_text': None,
                                        'detail_url': detail_url,
                                        'region': self._match_region(title),
                                        'purchaser': None,
                                        'deadline': None,
                                        'project_type': category['name'],
                                        'procurement_method': None,
                                        'contact_name': None,
                                        'contact_phone': None,
                                        'industry': None,
                                        'description': None,
                                        'raw_content': None
                                    }

                                    # 存储到数据库
                                    is_new, project = self.db_manager.save_project(project_data)
                                    total_count += 1
                                    category_count += 1
                                    if is_new:
                                        new_count += 1
                                        logger.debug(f"新增项目: {title}")

                                except Exception as e:
                                    logger.error(f"解析项目失败: {e}")
                                    continue

                            page += 1

                            # 限制每页最多采集100条
                            if category_count >= 100:
                                logger.debug(f"分类 {category['name']} 已达到采集限制")
                                break

                            # 限制最大页数
                            if page > 10:
                                logger.debug(f"分类 {category['name']} 已达到最大页数")
                                break

                        except Exception as e:
                            logger.error(f"采集分类 {category['name']} 第 {page} 页失败: {e}")
                            break

                    logger.debug(f"分类 {category['name']} 采集完成: {category_count} 条")

                except Exception as e:
                    logger.error(f"采集分类 {category['name']} 失败: {e}")
                    continue

            logger.info(f"{self.SITE_NAME} 采集完成: 总计 {total_count} 条, 新增 {new_count} 条")
            return {"total": total_count, "new": new_count}

        except Exception as e:
            logger.error(f"{self.SITE_NAME} 采集失败: {e}")
            return {"total": 0, "new": 0}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='招投标信息采集脚本')
    parser.add_argument('--days', type=int, default=7, help='采集最近几天的数据')
    parser.add_argument('--skip-push', action='store_true', help='跳过飞书推送')
    parser.add_argument('--sites', nargs='*', help='指定采集的网站')

    args = parser.parse_args()

    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)

    logger.info(f"采集日期范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")

    # 初始化数据库
    db_manager = DatabaseManager()

    # 创建采集器列表
    crawlers = [
        YanchengGovCrawler(db_manager),  # 盐城市政府采购网
        YanchengCityGovCrawler(db_manager),  # 盐城市人民政府网
        KfqaCrawler(db_manager),
        BigDataCrawler(db_manager),
        JscnCrawler(db_manager),
        DongfangCrawler(db_manager),
        DushiCrawler(db_manager),
        ChengnanCrawler(db_manager),
        JingkaiCrawler(db_manager),
        YuedaCrawler(db_manager),
        SufuCrawler(db_manager),
        HnzbcgxxwCrawler(db_manager)  # 全国招标采购公共服务平台
    ]

    # 如果指定了网站，则过滤采集器
    if args.sites:
        crawlers = [c for c in crawlers if c.SITE_NAME in args.sites]
        logger.info(f"指定采集网站: {[c.SITE_NAME for c in crawlers]}")

    # 执行采集
    total_stats = {'total': 0, 'new': 0}
    for crawler in crawlers:
        try:
            stats = crawler.crawl(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            total_stats['total'] += stats['total']
            total_stats['new'] += stats['new']
        except Exception as e:
            logger.error(f"{crawler.SITE_NAME} 采集异常: {e}")

    logger.info(f"采集完成! 总计: {total_stats['total']} 条, 新增: {total_stats['new']} 条")

    # 生成每日快照
    today = datetime.now().strftime('%Y-%m-%d')
    new_projects = db_manager.get_new_projects(today)

    snapshot = {
        'date': today,
        'crawl_time': datetime.now().isoformat(),
        'summary': {
            'total_projects': total_stats['total'],
            'new_projects': total_stats['new'],
            'yannan_count': len([p for p in new_projects if p['region'] == '盐南高新区']),
            'jingkai_count': len([p for p in new_projects if p['region'] == '经开区'])
        },
        'projects': [
            {
                'id': p['id'],
                'source_site': p['source_site'],
                'project_name': p['project_name'],
                'publish_date': p['publish_date'],
                'budget': p['budget'],
                'budget_text': p['budget_text'],
                'region': p['region'],
                'detail_url': p['detail_url'],
                'is_new': True
            }
            for p in new_projects
        ]
    }

    # 保存快照
    os.makedirs('./招投标数据/daily', exist_ok=True)
    with open(f'./招投标数据/daily/{today}.json', 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    logger.info(f"每日快照已保存: ./招投标数据/daily/{today}.json")

    # 推送飞书
    if not args.skip_push and total_stats['new'] > 0:
        logger.info("开始推送飞书...")
        try:
            import subprocess
            subprocess.run([
                sys.executable,
                'scripts/feishu_pusher.py',
                '--pdf-path', f'./招投标数据/exports/招投标日报_{today}.pdf'
            ], check=True)
        except Exception as e:
            logger.error(f"飞书推送失败: {e}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
