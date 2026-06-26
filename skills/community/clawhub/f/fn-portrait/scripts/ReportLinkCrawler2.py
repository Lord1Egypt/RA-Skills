#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
ReportLinkCrawler2.py - 年报/半年报 PDF 下载爬虫（增强版）
基于巨潮资讯网API，支持参数化配置、预统计、增量下载

使用方法：
    python ReportLinkCrawler2.py <报告期> <板块> <保存文件夹>
    
示例：
    python ReportLinkCrawler2.py 2025年报   科创板 RAWPDF-2025A
    python ReportLinkCrawler2.py 2025半年报 科创板 RAWPDF-2025H
    python ReportLinkCrawler2.py 2024年报   创业板 RAWPDF-2024CY
    python ReportLinkCrawler2.py 2025年报   沪主板 RAWPDF-2025SH

支持板块：
    科创板, 创业板, 沪主板, 深主板
    （也可用代码：shkcp, szcy, shmb, szmb）
"""

from __future__ import annotations

import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

import requests

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 板块名称映射
PLATE_NAME_MAP: Dict[str, str] = {
    '科创板': 'shkcp',
    '创业板': 'szcy',
    '沪主板': 'shmb',
    '深主板': 'szmb',
    'shkcp': 'shkcp',
    'szcy': 'szcy',
    'shmb': 'shmb',
    'szmb': 'szmb',
}

PLATE_DISPLAY_MAP: Dict[str, str] = {
    'shkcp': '科创板',
    'szcy': '创业板',
    'shmb': '沪主板',
    'szmb': '深主板',
}

# 报告类型配置
REPORT_CONFIG: Dict[str, Dict[str, Any]] = {
    '年报': {
        'category': 'category_ndbg_szsh',
        'search_months': (3, 4),        # 次年3-4月发布
        'title_keyword': '年度报告',
        'exclude_keywords': ['英文', '摘要', '已取消', '修订版', '更正后', 'XBRL'],
        'file_suffix': '年报',
    },
    '半年报': {
        'category': 'category_bndbg_szsh',
        'search_months': (7, 8),        # 当年7-8月发布
        'title_keyword': '半年度报告',
        'exclude_keywords': ['英文', '摘要', '已取消', '修订版', '更正后', 'XBRL'],
        'file_suffix': '半年报',
    },
}


@dataclass(frozen=True)
class ReportPeriod:
    """报告期解析结果"""
    year: int
    report_type: str        # '年报' 或 '半年报'


@dataclass(frozen=True)
class CrawlerConfig:
    """爬虫配置类"""
    target_year: int
    report_type: str = '年报'
    plate: str = "shkcp"
    max_retries: int = 3
    retry_delay: int = 5
    timeout: int = 30
    output_dir: str = "./RAWPDF"
    delay_between_downloads: float = 1.0


class CNINFOClient:
    """巨潮资讯API客户端"""
    
    BASE_URL = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    PDF_BASE_URL = "http://static.cninfo.com.cn/"
    
    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.cninfo.com.cn",
        "Origin": "http://www.cninfo.com.cn",
        "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    def __init__(self, config: CrawlerConfig) -> None:
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.report_cfg = REPORT_CONFIG[config.report_type]
    
    def search_announcements(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        搜索指定日期范围内的公告
        """
        date_range = f"{start_date}~{end_date}"
        all_results = []
        page_num = 1
        
        while True:
            data = {
                "pageNum": page_num,
                "pageSize": 30,
                "column": "sse",
                "tabName": "fulltext",
                "plate": self.config.plate,
                "searchkey": "",
                "secid": "",
                "category": self.report_cfg['category'],
                "trade": "",
                "seDate": date_range,
                "sortName": "time",
                "sortType": "desc",
                "isHLtitle": "false"
            }
            
            try:
                response = self.session.post(
                    self.BASE_URL,
                    data=data,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                result = response.json()
                
                announcements = result.get("announcements", [])
                if not announcements:
                    break
                
                all_results.extend(announcements)
                
                total_pages = result.get("totalpages", 0)
                if page_num >= total_pages:
                    break
                
                page_num += 1
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"搜索失败: {e}")
                break
        
        return all_results
    
    def download_pdf(self, adjunct_url: str, save_path: str, company_code: str, company_name: str) -> bool:
        """下载PDF文件"""
        try:
            pdf_url = f"{self.PDF_BASE_URL}{adjunct_url}"
            
            logging.info(f"  下载: {company_code} {company_name}")
            logging.info(f"  URL: {pdf_url}")
            
            pdf_session = requests.Session()
            pdf_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search',
                'Connection': 'keep-alive',
            }
            
            response = pdf_session.get(
                pdf_url,
                headers=pdf_headers,
                timeout=self.config.timeout,
                stream=True,
                allow_redirects=True
            )
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = os.path.getsize(save_path) / 1024
            logging.info(f"  ✓ 成功: {os.path.basename(save_path)} ({file_size:.1f} KB)")
            return True
            
        except Exception as e:
            logging.error(f"  ✗ 失败: {e}")
            return False


class ReportLinkCrawler:
    """报告下载爬虫主类"""
    
    def __init__(self, config: CrawlerConfig) -> None:
        self.config = config
        self.client = CNINFOClient(config)
        self.report_cfg = REPORT_CONFIG[config.report_type]
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'already_exists': 0,
        }
        self.existing_codes: set[str] = set()
    
    def _extract_year_from_title(self, title: str) -> Optional[int]:
        """从标题中提取年份"""
        match = re.search(r'(\d{4})年', title)
        if match:
            return int(match.group(1))
        return None
    
    def _should_download(self, title: str, year: int) -> bool:
        """判断是否应该下载"""
        title_year = self._extract_year_from_title(title)
        if title_year != year:
            return False
        
        for keyword in self.report_cfg['exclude_keywords']:
            if keyword in title:
                return False
        
        return True
    
    def _construct_filename(self, company_code: str, company_name: str, year: int) -> str:
        """构造文件名"""
        company_name_clean = re.sub(r'[\\/:*?"<>|]', '', company_name)
        suffix = self.report_cfg['file_suffix']
        return f"{company_code}_{company_name_clean}_{year}{suffix}.pdf"
    
    def _get_search_date_range(self, year: int) -> Tuple[str, str]:
        """
        根据报告类型计算搜索日期范围
        
        Returns:
            (start_date, end_date)
        """
        start_month, end_month = self.report_cfg['search_months']
        
        if self.config.report_type == '年报':
            # 年报在次年发布
            search_year = year + 1
        else:
            # 半年报在当年发布
            search_year = year
        
        start_date = f"{search_year}-{start_month:02d}-01"
        
        # 计算结束月份的最后一天
        if end_month == 12:
            end_date = f"{search_year}-{end_month:02d}-31"
        else:
            # 下月第一天减一天
            from datetime import datetime, timedelta
            next_month = datetime(search_year, end_month + 1, 1)
            last_day = (next_month - timedelta(days=1)).day
            end_date = f"{search_year}-{end_month:02d}-{last_day}"
        
        return start_date, end_date
    
    def _scan_existing_files(self, output_dir: Path) -> set[str]:
        """扫描目标目录中已存在的文件，提取公司代码"""
        existing_codes: set[str] = set()
        if not output_dir.exists():
            return existing_codes
        
        suffix = self.report_cfg['file_suffix']
        for f in output_dir.iterdir():
            if f.is_file() and f.suffix.lower() == '.pdf':
                # 匹配文件名格式: 688352_颀中科技_2025年报.pdf 或 688352_颀中科技_2025半年报.pdf
                pattern = rf'(\d{{6}})_.*_{re.escape(suffix)}\.pdf$'
                match = re.match(pattern, f.name)
                if match:
                    existing_codes.add(match.group(1))
        
        return existing_codes
    
    def preview_announcements(self, year: int) -> tuple[List[Dict[str, Any]], Path]:
        """
        预览阶段：搜索并统计符合条件的公告，同时扫描已有文件
        """
        suffix = self.report_cfg['file_suffix']
        
        logging.info("=" * 80)
        logging.info(f"【{suffix}下载爬虫 - 预览模式】")
        logging.info("=" * 80)
        logging.info(f"报告期: {year}{suffix}")
        logging.info(f"板块: {PLATE_DISPLAY_MAP.get(self.config.plate, self.config.plate)} ({self.config.plate})")
        logging.info(f"输出目录: {self.config.output_dir}")
        logging.info("")
        
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 扫描已有文件
        self.existing_codes = self._scan_existing_files(output_dir)
        logging.info(f"📁 扫描本地目录: {output_dir}")
        logging.info(f"   已存在 {len(self.existing_codes)} 个公司{suffix}文件")
        if self.existing_codes:
            logging.info(f"   已下载公司: {', '.join(sorted(self.existing_codes))}")
        logging.info("")
        
        # 计算搜索日期范围
        start_date, end_date = self._get_search_date_range(year)
        
        logging.info(f"🔍 搜索日期范围: {start_date} ~ {end_date}")
        logging.info(f"正在搜索{suffix}公告...")
        
        announcements = self.client.search_announcements(start_date, end_date)
        logging.info(f"   API 返回 {len(announcements)} 条公告")
        logging.info("")
        
        # 筛选
        qualified: List[Dict[str, Any]] = []
        skipped_keywords = 0
        skipped_wrong_year = 0
        skipped_existing = 0
        
        seen_codes: set[str] = set()
        
        for ann in announcements:
            try:
                company_code = ann["secCode"]
                company_name = ann["secName"]
                title = ann["announcementTitle"]
                
                # 检查年份
                title_year = self._extract_year_from_title(title)
                if title_year != year:
                    skipped_wrong_year += 1
                    continue
                
                # 检查排除关键词
                if any(kw in title for kw in self.report_cfg['exclude_keywords']):
                    skipped_keywords += 1
                    continue
                
                # 检查是否已存在
                if company_code in self.existing_codes:
                    skipped_existing += 1
                    continue
                
                # 同一公司去重
                if company_code in seen_codes:
                    continue
                seen_codes.add(company_code)
                
                qualified.append(ann)
                
            except Exception as e:
                logging.warning(f"  处理公告出错: {e}")
                continue
        
        # 打印统计
        logging.info("=" * 80)
        logging.info("【预览统计】")
        logging.info("=" * 80)
        logging.info(f"API 返回公告总数:    {len(announcements)}")
        logging.info(f"  └─ 非目标年份:     {skipped_wrong_year}")
        logging.info(f"  └─ 含排除关键词:   {skipped_keywords}")
        logging.info(f"  └─ 本地已存在:     {skipped_existing}")
        logging.info(f"  └─ 去重后待下载:   {len(qualified)}")
        logging.info("")
        
        if qualified:
            logging.info("待下载公司列表:")
            for idx, ann in enumerate(qualified, 1):
                code = ann["secCode"]
                name = ann["secName"]
                title = ann["announcementTitle"]
                logging.info(f"  {idx:3d}. {code} {name} - {title}")
            logging.info("")
        else:
            logging.info("✅ 没有需要下载的新文件。")
            logging.info("")
        
        return qualified, output_dir
    
    def download_announcements(self, announcements: List[Dict[str, Any]], output_dir: Path, year: int, max_downloads: int = None) -> None:
        """下载指定的公告列表"""
        if not announcements:
            return
        
        suffix = self.report_cfg['file_suffix']
        
        logging.info("=" * 80)
        logging.info("【开始下载】")
        logging.info("=" * 80)
        logging.info("")
        
        if max_downloads is not None:
            announcements = announcements[:max_downloads]
            logging.info(f"⚠️ 测试模式：仅下载前 {max_downloads} 个文件")
            logging.info("")
        
        total = len(announcements)
        for idx, announcement in enumerate(announcements, 1):
            try:
                company_code = announcement["secCode"]
                company_name = announcement["secName"]
                title = announcement["announcementTitle"]
                adjunct_url = announcement["adjunctUrl"]
                
                logging.info(f"[{idx}/{total}] {company_code} {company_name}")
                logging.info(f"  标题: {title}")
                
                self.stats['total'] += 1
                
                filename = self._construct_filename(company_code, company_name, year)
                save_path = output_dir / filename
                
                if save_path.exists():
                    logging.info(f"  跳过: 文件已存在")
                    self.stats['already_exists'] += 1
                    continue
                
                success = self.client.download_pdf(
                    adjunct_url, str(save_path), company_code, company_name
                )
                
                if success:
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
                
                if idx < total:
                    time.sleep(self.config.delay_between_downloads)
                
            except Exception as e:
                logging.error(f"  处理出错: {e}")
                self.stats['failed'] += 1
            
            logging.info("")
        
        self._print_stats()
    
    def _print_stats(self) -> None:
        """打印统计信息"""
        suffix = self.report_cfg['file_suffix']
        logging.info("=" * 80)
        logging.info("【下载统计】")
        logging.info("=" * 80)
        logging.info(f"总任务数:   {self.stats['total']}")
        logging.info(f"成功下载:   {self.stats['success']}")
        logging.info(f"本地已存在: {self.stats['already_exists']}")
        logging.info(f"下载失败:   {self.stats['failed']}")
        logging.info("")


def parse_plate(plate_input: str) -> str:
    """解析板块输入，返回标准代码"""
    plate = plate_input.strip()
    if plate in PLATE_NAME_MAP:
        return PLATE_NAME_MAP[plate]
    raise ValueError(f"不支持的板块: {plate}。支持的板块: {', '.join(PLATE_NAME_MAP.keys())}")


def parse_report_period(period_input: str) -> ReportPeriod:
    """
    解析报告期参数
    
    支持格式:
        2025年报, 2025半年报
        2025年报, 2025年半年报（自动提取）
    """
    period = period_input.strip()
    
    # 尝试匹配: 2025年报 或 2025半年报
    match = re.match(r'^(\d{4})(年?[半]?年报)$', period)
    if match:
        year = int(match.group(1))
        type_str = match.group(2)
        # 统一处理
        if '半年' in type_str:
            report_type = '半年报'
        else:
            report_type = '年报'
        return ReportPeriod(year=year, report_type=report_type)
    
    # 尝试更宽松的匹配
    match2 = re.match(r'^(\d{4}).*$', period)
    if match2:
        year = int(match2.group(1))
        if '半年' in period:
            report_type = '半年报'
        else:
            report_type = '年报'
        return ReportPeriod(year=year, report_type=report_type)
    
    raise ValueError(
        f"无效的报告期格式: '{period_input}'。"
        f"支持的格式如: '2025年报', '2025半年报'"
    )


def run(
    report_period: str = '2025年报',
    plate: str = '科创板',
    output_dir: str = './RAWPDF',
    auto_confirm: bool = False,
    max_downloads: int = None,
    stock_codes: list = None,
) -> None:
    """
    手动运行函数（参数直接写在代码里，适合 Jupyter/IDE 调用）
    
    Args:
        report_period: 报告期，如 '2025年报'、'2025半年报'
        plate: 板块，如 '科创板'、'创业板'、'沪主板'、'深主板'
        output_dir: 保存文件夹路径
        auto_confirm: 是否自动确认下载（跳过 y/n 交互）
        max_downloads: 限制下载数量（用于测试）
        stock_codes: 指定股票代码列表，如 ['688199', '688302']，只下载这些公司的报告
    """
    # 解析参数
    period = parse_report_period(report_period)
    plate_code = parse_plate(plate)
    
    suffix = REPORT_CONFIG[period.report_type]['file_suffix']
    logging.info("=" * 80)
    logging.info(f"【巨潮资讯{suffix}下载爬虫 - 手动模式】")
    logging.info("=" * 80)
    logging.info(f"报告期:   {period.year}{suffix}")
    logging.info(f"板块:     {PLATE_DISPLAY_MAP.get(plate_code, plate_code)} ({plate_code})")
    logging.info(f"保存目录: {output_dir}")
    logging.info(f"自动确认: {'是' if auto_confirm else '否（需手动确认）'}")
    if stock_codes:
        logging.info(f"指定股票: {', '.join(stock_codes)}")
    logging.info("")
    
    # 配置
    config = CrawlerConfig(
        target_year=period.year,
        report_type=period.report_type,
        plate=plate_code,
        output_dir=output_dir,
        delay_between_downloads=1.0
    )
    
    # 创建爬虫实例
    crawler = ReportLinkCrawler(config)
    
    # 阶段 1: 预览
    qualified, output_dir_path = crawler.preview_announcements(year=period.year)
    
    # 按股票代码过滤
    if stock_codes and qualified:
        filtered = [q for q in qualified if any(code in q['secCode'] for code in stock_codes)]
        logging.info(f"股票过滤: {len(qualified)} → {len(filtered)} 个文件")
        qualified = filtered
    
    # 阶段 2: 确认
    if not qualified:
        logging.info("任务完成，没有需要下载的新文件。")
        return
    
    if not auto_confirm:
        try:
            confirm = input(f"确认下载以上 {len(qualified)} 个文件? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("")
            confirm = 'n'
        
        if confirm not in ('y', 'yes', '是', '确认', '1'):
            logging.info("用户取消下载，程序退出。")
            return
    else:
        logging.info(f"自动确认已开启，开始下载 {len(qualified)} 个文件...")
    
    # 阶段 3: 执行下载
    crawler.download_announcements(qualified, output_dir_path, period.year, max_downloads)
    
    logging.info("=" * 80)
    logging.info("程序执行完成！")
    logging.info("=" * 80)


def main():
    """主函数：支持命令行参数"""
    if len(sys.argv) < 4:
        print("用法: python ReportLinkCrawler2.py <报告期> <板块> <保存文件夹>")
        print("")
        print("示例:")
        print("  python ReportLinkCrawler2.py 2025年报   科创板 RAWPDF-2025A")
        print("  python ReportLinkCrawler2.py 2025半年报 科创板 RAWPDF-2025H")
        print("  python ReportLinkCrawler2.py 2024年报   创业板 RAWPDF-2024CY")
        print("  python ReportLinkCrawler2.py 2025年报   沪主板 RAWPDF-2025SH")
        print("")
        print("支持板块: 科创板, 创业板, 沪主板, 深主板")
        print("          (也可用代码: shkcp, szcy, shmb, szmb)")
        sys.exit(1)
    
    # 参数 1: 报告期
    try:
        period = parse_report_period(sys.argv[1])
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 参数 2: 板块
    try:
        plate_code = parse_plate(sys.argv[2])
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 参数 3: 保存文件夹
    output_dir = sys.argv[3].strip()
    
    # 打印配置信息
    suffix = REPORT_CONFIG[period.report_type]['file_suffix']
    logging.info("=" * 80)
    logging.info(f"【巨潮资讯{suffix}下载爬虫 - 增强版】")
    logging.info("=" * 80)
    logging.info(f"报告期:   {period.year}{suffix}")
    logging.info(f"板块:     {PLATE_DISPLAY_MAP.get(plate_code, plate_code)} ({plate_code})")
    logging.info(f"保存目录: {output_dir}")
    logging.info("")
    
    # 配置
    config = CrawlerConfig(
        target_year=period.year,
        report_type=period.report_type,
        plate=plate_code,
        output_dir=output_dir,
        delay_between_downloads=1.0
    )
    
    # 创建爬虫实例
    crawler = ReportLinkCrawler(config)
    
    # 阶段 1: 预览
    qualified, output_dir_path = crawler.preview_announcements(year=period.year)
    
    # 阶段 2: 用户确认
    if not qualified:
        logging.info("任务完成，没有需要下载的新文件。")
        return
    
    try:
        confirm = input(f"确认下载以上 {len(qualified)} 个文件? (y/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("")
        confirm = 'n'
    
    if confirm not in ('y', 'yes', '是', '确认', '1'):
        logging.info("用户取消下载，程序退出。")
        return
    
    # 阶段 3: 执行下载
    crawler.download_announcements(qualified, output_dir_path, period.year)
    
    logging.info("=" * 80)
    logging.info("程序执行完成！")
    logging.info("=" * 80)


if __name__ == '__main__':
    main()
