#!/usr/bin/env python3
"""
PDF报告生成器（修复版）
修复中文乱码问题，支持中文字体
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus.flowables import HRFlowable

import sqlite3
import logging
import re

logger = logging.getLogger(__name__)

# 来源网站固定排序
SITE_ORDER = [
    '盐城市政府采购网',
    '苏服采',
    '城南新区公共资源交易网',
    '开发区公共资源交易网',
    '盐城市大数据集团',
    '盐城市都市建设投资集团',
    '盐城市东方集团',
    '江苏世纪新城',
    '经开城发集团',
    '悦达集团',
]


class PDFGenerator:
    """PDF报告生成器（修复版）"""

    # 网站配置映射
    SITE_CONFIG = {
        '盐城市政府采购网': {
            'crawl_strategy': 'dataproxy接口',
            'filter_strategy': '区域关键词筛选（盐南高新区、经开区）',
            'crawl_method': 'requests + 正则解析',
            'categories': '13个子版块（采购意向、公告、中标等）'
        },
        '开发区公共资源交易网': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"经开区"（无需筛选）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '招标公告、中标公告、采购公告等'
        },
        '城南新区公共资源交易网': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"盐南高新区"（无需筛选）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '交易信息'
        },
        '江苏世纪新城': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '招标租赁'
        },
        '盐城市大数据集团': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '新闻资讯'
        },
        '盐城市东方集团': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '招标采购'
        },
        '盐城市都市建设投资集团': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '通知、招标'
        },
        '经开城发集团': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '招标信息、中标信息'
        },
        '悦达集团': {
            'crawl_strategy': '全量采集',
            'filter_strategy': '标记为"区域内"（跳过关键词匹配）',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '12个子分类（工程、货物、服务等）'
        },
        '苏服采': {
            'crawl_strategy': '地区筛选后采集',
            'filter_strategy': '选择区域（经开区、盐南高新区）',
            'crawl_method': 'Playwright浏览器自动化',
            'categories': '招标采购'
        },
        '盐城市人民政府网': {
            'crawl_strategy': '区域关键词筛选',
            'filter_strategy': '匹配"盐南高新区"、"经开区"',
            'crawl_method': 'requests + BeautifulSoup + iframe',
            'categories': '政府信息公开'
        },
        '全国招标采购公共服务平台': {
            'crawl_strategy': '区域关键词筛选',
            'filter_strategy': '匹配"盐南高新区"、"经开区"',
            'crawl_method': 'requests + BeautifulSoup',
            'categories': '招标/采购公告、中标/成交公告等'
        }
    }

    def __init__(self, db_path: str = './招投标数据/history.db'):
        self.db_path = db_path
        self.output_dir = './招投标数据/daily'
        os.makedirs(self.output_dir, exist_ok=True)

        # 注册中文字体
        self._register_fonts()
        self.chinese_font = self._get_chinese_font()

    def _register_fonts(self):
        """注册中文字体"""
        try:
            # 尝试使用系统中的中文字体
            font_paths = [
                # Linux
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 微米黑
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 正黑
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Droid Sans
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Noto Sans CJK
                '/usr/share/fonts/truetype/arphic/uming.ttc',  # 文鼎PL简中黑
                # macOS
                '/System/Library/Fonts/PingFang.ttc',
                '/System/Library/Fonts/STHeiti Light.ttc',
                # Windows
                'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                'C:/Windows/Fonts/simhei.ttf',  # 黑体
                'C:/Windows/Fonts/simsun.ttc',  # 宋体
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    logger.info(f"✅ 成功注册中文字体: {font_path}")
                    return

            # 如果找不到系统字体，尝试使用内置字体
            logger.warning("⚠️ 未找到系统中的中文字体，尝试使用备用方案")
            self._register_backup_fonts()

        except Exception as e:
            logger.warning(f"⚠️ 注册中文字体失败: {e}")
            self._register_backup_fonts()

    def _register_backup_fonts(self):
        """注册备用字体"""
        try:
            # 尝试使用reportlab内置的字体（可能不支持中文）
            logger.warning("使用备用字体方案，中文可能显示为乱码")
            # 这里不注册任何字体，让reportlab使用默认字体
        except Exception as e:
            logger.warning(f"注册备用字体失败: {e}")

    def _get_chinese_font(self) -> str:
        """获取中文字体名称"""
        try:
            # 检查字体是否已注册
            if 'ChineseFont' in pdfmetrics.getRegisteredFontNames():
                return 'ChineseFont'
            else:
                logger.warning("未找到中文字体，使用默认字体（中文可能显示为乱码）")
                return 'Helvetica'  # 默认字体
        except Exception as e:
            logger.warning(f"获取中文字体失败: {e}")
            return 'Helvetica'

    def generate_daily_report(self, date: str) -> Optional[str]:
        """生成日报PDF（修复版）

        Args:
            date: 日期字符串，格式: YYYY-MM-DD

        Returns:
            PDF文件路径，如果生成失败返回None
        """
        try:
            # 查询数据
            daily_summary = self._get_daily_summary(date)
            monthly_summary = self._get_monthly_summary(date)
            daily_projects = self._get_daily_projects(date)
            monthly_projects = self._get_monthly_projects(date)

            if not daily_projects and not monthly_projects:
                logger.warning(f"日期 {date} 没有数据，跳过生成PDF")
                return None

            # 生成PDF文件名
            filename = f"招投标信息日报_{date}.pdf"
            filepath = os.path.join(self.output_dir, filename)

            # 创建PDF文档
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )

            # 构建内容
            story = []

            # 第1页：招标信息概况
            story.extend(self._create_summary_page(date, daily_summary, monthly_summary))

            # 第2页：当日清单
            if daily_projects:
                story.append(PageBreak())
                story.extend(self._create_daily_list_page(date, daily_projects))

            # 第3页开始：当月分平台清单
            if monthly_projects:
                story.append(PageBreak())
                story.extend(self._create_monthly_platform_pages(date, monthly_projects))

            # 生成PDF
            doc.build(story)

            logger.info(f"✅ PDF报告生成成功: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"❌ 生成PDF报告失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_monthly_report(self, year: int, month: int) -> Optional[str]:
        """生成月度报告PDF

        Args:
            year: 年份
            month: 月份

        Returns:
            PDF文件路径，如果生成失败返回None
        """
        try:
            # 计算月份的第一天和最后一天
            first_day = datetime(year, month, 1).strftime('%Y-%m-%d')

            if month == 12:
                next_month_first_day = datetime(year + 1, 1, 1)
            else:
                next_month_first_day = datetime(year, month + 1, 1)

            last_day = (next_month_first_day - timedelta(days=1)).strftime('%Y-%m-%d')
            report_date = f"{year}年{month}月"

            logger.info(f"生成月度报告: {report_date} ({first_day} ~ {last_day})")

            # 查询数据
            monthly_summary = self._get_monthly_summary_data(first_day, last_day)
            monthly_projects = self._get_monthly_projects_by_site(first_day, last_day)

            if not monthly_projects:
                logger.warning(f"{report_date} 没有数据，跳过生成PDF")
                return None

            # 生成PDF文件名
            filename = f"招投标信息月报_{year}年{month:02d}月.pdf"
            filepath = os.path.join(self.output_dir, filename)

            # 创建PDF文档
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )

            # 构建内容
            story = []

            # 第1页：月度概况
            story.extend(self._create_monthly_summary_page(report_date, first_day, last_day, monthly_summary))

            # 第2页开始：分平台清单
            story.append(PageBreak())
            story.extend(self._create_monthly_platform_pages(report_date, monthly_projects))

            # 生成PDF
            doc.build(story)

            logger.info(f"✅ 月度PDF报告生成成功: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"❌ 生成月度PDF报告失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _get_monthly_summary_data(self, first_day: str, last_day: str) -> Dict:
        """获取月度汇总数据（按网站统计）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                source_site,
                COUNT(*) as count
            FROM bidding_projects
            WHERE publish_date BETWEEN ? AND ?
            GROUP BY source_site
        ''', (first_day, last_day))

        summary = {}
        for site, count in cursor.fetchall():
            summary[site] = count

        conn.close()
        return summary

    def _sort_sites(self, sites: List[str]) -> List[str]:
        """按 SITE_ORDER 排序网站列表"""
        def sort_key(site):
            if site in SITE_ORDER:
                return SITE_ORDER.index(site)
            return 999
        return sorted(sites, key=sort_key)

    def _get_monthly_projects_by_site(self, first_day: str, last_day: str) -> Dict[str, List[Dict]]:
        """获取月度项目数据（按网站分类）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                source_site,
                publish_date,
                project_name,
                detail_url
            FROM bidding_projects
            WHERE publish_date BETWEEN ? AND ?
            ORDER BY source_site, publish_date DESC, project_name
        ''', (first_day, last_day))

        columns = ['source_site', 'publish_date', 'project_name', 'detail_url']

        # 按网站分类
        projects_by_site = {}
        for row in cursor.fetchall():
            project = dict(zip(columns, row))
            site = project['source_site']

            if site not in projects_by_site:
                projects_by_site[site] = []
            projects_by_site[site].append(project)

        conn.close()
        return projects_by_site

    def _get_daily_summary(self, date: str) -> Dict:
        """获取当日汇总数据（按网站统计）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                source_site,
                COUNT(*) as count
            FROM bidding_projects
            WHERE publish_date = ?
            GROUP BY source_site
            ORDER BY count DESC
        ''', (date,))

        summary = {}
        for site, count in cursor.fetchall():
            summary[site] = count

        conn.close()
        return summary

    def _get_monthly_summary(self, date: str) -> Dict:
        """获取当月汇总数据（按网站统计）"""
        # 计算当月第一天和最后一天
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        first_day = date_obj.replace(day=1).strftime('%Y-%m-%d')

        # 计算下个月的第一天，然后减一天得到当月的最后一天
        if date_obj.month == 12:
            next_month_first_day = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            next_month_first_day = date_obj.replace(month=date_obj.month + 1, day=1)
        last_day = (next_month_first_day - timedelta(days=1)).strftime('%Y-%m-%d')

        return self._get_monthly_summary_data(first_day, last_day)

    def _get_daily_projects(self, date: str) -> List[Dict]:
        """获取当日项目数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                source_site,
                publish_date,
                project_name,
                detail_url
            FROM bidding_projects
            WHERE publish_date = ?
            ORDER BY source_site, publish_date, project_name
        ''', (date,))

        columns = ['source_site', 'publish_date', 'project_name', 'detail_url']

        projects = []
        for row in cursor.fetchall():
            project = dict(zip(columns, row))
            projects.append(project)

        conn.close()
        return projects

    def _get_monthly_projects(self, date: str) -> Dict[str, List[Dict]]:
        """获取当月项目数据（按网站分类）"""
        # 计算当月第一天和最后一天
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        first_day = date_obj.replace(day=1).strftime('%Y-%m-%d')

        if date_obj.month == 12:
            next_month_first_day = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            next_month_first_day = date_obj.replace(month=date_obj.month + 1, day=1)
        last_day = (next_month_first_day - timedelta(days=1)).strftime('%Y-%m-%d')

        return self._get_monthly_projects_by_site(first_day, last_day)

    def _create_summary_page(self, date: str, daily_summary: Dict, monthly_summary: Dict) -> List:
        """创建第1页：招标信息概况"""
        page = []

        # 标题
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Heading1'],
            fontName=self.chinese_font,
            fontSize=22,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=0.5*cm
        )
        page.append(Paragraph("招投标信息概况", title_style))

        # 日期
        date_style = ParagraphStyle(
            'Date',
            parent=getSampleStyleSheet()['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=1*cm
        )
        page.append(Paragraph(f"报告日期：{date}", date_style))

        # 单元格样式（用于触发自动换行）
        cell_center_style = ParagraphStyle('CellCenter', fontName=self.chinese_font, fontSize=9, alignment=TA_CENTER, leading=11, wordWrap='CJK')
        cell_left_style = ParagraphStyle('CellLeft', fontName=self.chinese_font, fontSize=9, alignment=TA_LEFT, leading=11, wordWrap='CJK')
        header_style = ParagraphStyle('Header', fontName=self.chinese_font, fontSize=10, alignment=TA_CENTER, leading=12, wordWrap='CJK')

        # 汇总表格（包含爬虫策略和筛选策略）
        table_data = [[
            Paragraph('网站名称', header_style),
            Paragraph('当日条数', header_style),
            Paragraph('当月条数', header_style),
            Paragraph('爬虫策略', header_style),
            Paragraph('筛选策略', header_style)
        ]]

        # 获取所有网站（合并当日和当月的网站）
        all_sites = set(daily_summary.keys()) | set(monthly_summary.keys())

        for site in sorted(all_sites, key=lambda x: -daily_summary.get(x, 0)):
            daily_count = daily_summary.get(site, 0)
            monthly_count = monthly_summary.get(site, 0)

            # 获取网站配置
            config = self.SITE_CONFIG.get(site, {})
            crawl_strategy = config.get('crawl_strategy', '-')
            filter_strategy = config.get('filter_strategy', '-')

            table_data.append([
                Paragraph(site, cell_center_style),
                Paragraph(str(daily_count), cell_center_style),
                Paragraph(str(monthly_count), cell_center_style),
                Paragraph(crawl_strategy, cell_left_style),
                Paragraph(filter_strategy, cell_left_style)
            ])

        # 创建表格（调整列宽以适应新增列）
        table = Table(table_data, colWidths=[5*cm, 2*cm, 2*cm, 3.5*cm, 4*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))

        page.append(table)

        # 添加总统计
        total_daily = sum(daily_summary.values())
        total_monthly = sum(monthly_summary.values())

        total_style = ParagraphStyle(
            'Total',
            parent=getSampleStyleSheet()['Normal'],
            fontName=self.chinese_font,
            fontSize=11,
            alignment=TA_LEFT,
            spaceBefore=0.5*cm
        )

        page.append(Paragraph(f"<b>当日总计：</b>{total_daily} 条", total_style))
        page.append(Paragraph(f"<b>当月总计：</b>{total_monthly} 条", total_style))

        return page

    def _create_monthly_summary_page(self, report_date: str, first_day: str, last_day: str, monthly_summary: Dict) -> List:
        """创建月度概况页"""
        page = []

        # 标题
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Heading1'],
            fontName=self.chinese_font,
            fontSize=22,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=0.5*cm
        )
        page.append(Paragraph("招投标信息月度报告", title_style))

        # 日期范围
        date_style = ParagraphStyle(
            'Date',
            parent=getSampleStyleSheet()['Normal'],
            fontName=self.chinese_font,
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=0.5*cm
        )
        page.append(Paragraph(f"报告时间：{report_date}", date_style))
        page.append(Paragraph(f"统计范围：{first_day} 至 {last_day}", date_style))
        page.append(Spacer(1, 0.3*cm))

        # 计算今天和昨天
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # 单元格样式（用于触发自动换行）
        cell_center_style = ParagraphStyle('CellCenter', fontName=self.chinese_font, fontSize=9, alignment=TA_CENTER, leading=11, wordWrap='CJK')
        cell_left_style = ParagraphStyle('CellLeft', fontName=self.chinese_font, fontSize=9, alignment=TA_LEFT, leading=11, wordWrap='CJK')
        header_style = ParagraphStyle('Header', fontName=self.chinese_font, fontSize=10, alignment=TA_CENTER, leading=12, wordWrap='CJK', textColor=colors.white)
        sum_cell_style = ParagraphStyle('SumCell', fontName=self.chinese_font, fontSize=10, alignment=TA_CENTER, leading=12, wordWrap='CJK')

        # 汇总表格：网站名称、数据条数、当日数据、前一日数据
        table_data = [[
            Paragraph('网站名称', header_style),
            Paragraph('数据条数', header_style),
            Paragraph('当日数据', header_style),
            Paragraph('前一日数据', header_style),
            Paragraph('爬虫策略', header_style),
            Paragraph('筛选策略', header_style)
        ]]

        # 按 SITE_ORDER 排序，不在列表中的排后面
        def sort_key(item):
            site, count = item
            if site in SITE_ORDER:
                return SITE_ORDER.index(site)
            return 999

        sorted_items = sorted(monthly_summary.items(), key=sort_key)

        total_count = 0
        total_today = 0
        total_yesterday = 0

        for site, count in sorted_items:
            today_count = self._get_daily_count_for_site(site, today)
            yesterday_count = self._get_daily_count_for_site(site, yesterday)

            # 获取网站配置
            config = self.SITE_CONFIG.get(site, {})
            crawl_strategy = config.get('crawl_strategy', '-')
            filter_strategy = config.get('filter_strategy', '-')

            table_data.append([
                Paragraph(site, cell_center_style),
                Paragraph(str(count), cell_center_style),
                Paragraph(str(today_count), cell_center_style),
                Paragraph(str(yesterday_count), cell_center_style),
                Paragraph(crawl_strategy, cell_left_style),
                Paragraph(filter_strategy, cell_left_style)
            ])

            total_count += count
            total_today += today_count
            total_yesterday += yesterday_count

        # 添加求和行
        table_data.append([
            Paragraph('合计', sum_cell_style),
            Paragraph(str(total_count), sum_cell_style),
            Paragraph(str(total_today), sum_cell_style),
            Paragraph(str(total_yesterday), sum_cell_style),
            Paragraph('-', sum_cell_style),
            Paragraph('-', sum_cell_style)
        ])

        # 创建表格
        table = Table(table_data, colWidths=[3.5*cm, 2*cm, 2*cm, 2*cm, 2.5*cm, 3.5*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
            # 求和行样式
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d9e2f3')),
            ('ALIGN', (4, 1), (5, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))

        page.append(table)

        return page

    def _get_daily_count_for_site(self, site: str, date: str) -> int:
        """获取指定网站指定日期的数据条数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM bidding_projects
            WHERE source_site = ? AND publish_date = ?
        ''', (site, date))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _get_monthly_summary_data_by_date(self, date: str) -> Dict:
        """获取指定日期所在月份的汇总数据（按网站统计）"""
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        first_day = date_obj.replace(day=1).strftime('%Y-%m-%d')

        if date_obj.month == 12:
            next_month_first_day = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
        else:
            next_month_first_day = date_obj.replace(month=date_obj.month + 1, day=1)
        last_day = (next_month_first_day - timedelta(days=1)).strftime('%Y-%m-%d')

        return self._get_monthly_summary_data(first_day, last_day)

    def _create_daily_list_page(self, date: str, projects: List[Dict]) -> List:
        """创建第2页：当日清单"""
        page = []

        # 标题
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Heading1'],
            fontName=self.chinese_font,
            fontSize=18,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=0.5*cm
        )
        page.append(Paragraph(f"当日招标信息清单（{date}）", title_style))

        # 单元格样式（用于触发自动换行）
        cell_style = ParagraphStyle('Cell', fontName=self.chinese_font, fontSize=9, alignment=TA_LEFT, leading=11, wordWrap='CJK')
        header_style = ParagraphStyle('Header', fontName=self.chinese_font, fontSize=10, alignment=TA_CENTER, leading=12, wordWrap='CJK')
        link_style = ParagraphStyle('Link', fontName=self.chinese_font, fontSize=8, alignment=TA_LEFT, leading=10, wordWrap='LTR', textColor=colors.blue)

        # 创建表格数据
        table_data = [[
            Paragraph('网站', header_style),
            Paragraph('日期', header_style),
            Paragraph('标题', header_style),
            Paragraph('链接', header_style)
        ]]

        for project in projects:
            url = project['detail_url'] or ''

            # 项目名称用 Paragraph 触发自动换行
            title_para = Paragraph(project['project_name'], cell_style)

            # 链接用可点击的 Paragraph
            if url:
                link_para = Paragraph(f'<link href="{url}" color="blue" underline="0"><u>{url}</u></link>', link_style)
            else:
                link_para = Paragraph('-', link_style)

            table_data.append([
                Paragraph(project['source_site'], cell_style),
                Paragraph(project['publish_date'], cell_style),
                title_para,
                link_para
            ])

        # 创建表格
        table = Table(table_data, colWidths=[4*cm, 2.5*cm, 6*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))

        page.append(table)

        return page

    def _create_monthly_platform_pages(self, report_date: str, projects_by_site: Dict[str, List[Dict]]) -> List:
        """创建第3页开始：当月分平台清单（按 SITE_ORDER 排序，网址为超链接）"""
        pages = []

        # 按 SITE_ORDER 排序
        def sort_key(site):
            if site in SITE_ORDER:
                return SITE_ORDER.index(site)
            return 999

        sorted_sites = sorted(projects_by_site.keys(), key=sort_key)

        for idx, site in enumerate(sorted_sites):
            projects = projects_by_site[site]
            page = []

            # 标题
            title_style = ParagraphStyle(
                'Title',
                parent=getSampleStyleSheet()['Heading1'],
                fontName=self.chinese_font,
                fontSize=16,
                textColor=colors.darkblue,
                alignment=TA_CENTER,
                spaceAfter=0.5*cm
            )
            page.append(Paragraph(f"{site}（共{len(projects)}条）", title_style))

            # 单元格样式（用于触发自动换行）
            cell_style = ParagraphStyle('Cell', fontName=self.chinese_font, fontSize=9, alignment=TA_LEFT, leading=11, wordWrap='CJK')
            header_style = ParagraphStyle('Header', fontName=self.chinese_font, fontSize=10, alignment=TA_CENTER, leading=12, wordWrap='CJK', textColor=colors.white)
            link_cell_style = ParagraphStyle(
                'LinkCell',
                fontName=self.chinese_font,
                fontSize=8,
                textColor=colors.blue,
                leading=10,
                wordWrap='LTR',
            )

            # 创建表格数据
            table_data = [[
                Paragraph('网站', header_style),
                Paragraph('日期', header_style),
                Paragraph('项目名称', header_style),
                Paragraph('链接', header_style)
            ]]

            for project in projects:
                url = project['detail_url'] or ''

                # 项目名称用 Paragraph 包裹，自动换行
                name_para = Paragraph(project['project_name'], cell_style)

                # 链接列用 Paragraph 包裹，实现可点击超链接
                if url:
                    link_para = Paragraph(
                        f"<link href='{url}' color='blue' underline='yes'>{url}</link>",
                        link_cell_style
                    )
                else:
                    link_para = Paragraph('-', link_cell_style)

                table_data.append([
                    Paragraph(project['source_site'], cell_style),
                    Paragraph(project['publish_date'], cell_style),
                    name_para,
                    link_para
                ])

            # 创建表格（网站3cm，日期2.5cm，项目名称7cm，链接4cm）
            table = Table(table_data, colWidths=[3*cm, 2.5*cm, 7*cm, 4*cm], repeatRows=1)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]))

            page.append(table)

            pages.extend(page)

            # 如果不是最后一个网站，添加分页
            if idx < len(sorted_sites) - 1:
                pages.append(PageBreak())

        return pages


if __name__ == '__main__':
    import sys

    generator = PDFGenerator()

    # 根据参数选择生成日报还是月报
    if len(sys.argv) > 1 and sys.argv[1] == 'monthly':
        # 生成月报
        year = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
        month = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        filepath = generator.generate_monthly_report(year, month)
        print(f"{'生成成功' if filepath else '生成失败'}: {filepath}")
    else:
        # 生成日报
        today = datetime.now().strftime('%Y-%m-%d')
        filepath = generator.generate_daily_report(today)
        print(f"{'生成成功' if filepath else '生成失败'}: {filepath}")
