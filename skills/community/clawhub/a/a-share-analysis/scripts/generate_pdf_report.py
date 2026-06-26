#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股专业详细 PDF 报告生成器
生成内容详细、专业、可商用的 PDF 格式分析报告
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareDetailedPDFReport:
    """A 股详细 PDF 报告生成器（专业版）"""

    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.expanduser("~/.openclaw/workspace")
        self.workspace_path = workspace_path
        self.output_dir = os.path.join(workspace_path, "a-share-reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self._register_fonts()
        self._create_styles()

    def _register_fonts(self):
        """注册中文字体"""
        font_paths = {
            'SimSun': r'C:\Windows\Fonts\simsun.ttc',
            'SimHei': r'C:\Windows\Fonts\simhei.ttf',
        }
        
        for name, path in font_paths.items():
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont(name, path))
                except Exception as e:
                    logger.warning(f"字体注册失败 {name}: {e}")

    def _create_styles(self):
        """创建样式"""
        self.styles = getSampleStyleSheet()
        
        # 主标题样式
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontName='SimHei',
            fontSize=20,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=TA_CENTER,
            spaceAfter=20,
            spaceBefore=30
        ))
        
        # 章节标题样式
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontName='SimHei',
            fontSize=14,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=12,
            spaceBefore=15,
            borderWidth=1,
            borderColor=colors.HexColor('#1e3a8a'),
            leftPadding=5
        ))
        
        # 子标题样式
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading3'],
            fontName='SimHei',
            fontSize=11,
            textColor=colors.HexColor('#0891b2'),
            spaceAfter=8,
            spaceBefore=10
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='ChineseText',
            parent=self.styles['Normal'],
            fontName='SimSun',
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_LEFT
        ))
        
        # 列表样式
        self.styles.add(ParagraphStyle(
            name='ListText',
            parent=self.styles['ChineseText'],
            leftIndent=20,
            spaceBefore=4,
            spaceAfter=4
        ))

    def generate_pdf(self, data: Dict) -> str:
        """生成详细 PDF 报告（按股票代码分类存储）"""
        # 确保所有必需数据存在并有效
        if 'price' not in data or data['price'] is None:
            data['price'] = 0
        if 'change_percent' not in data or data['change_percent'] is None:
            data['change_percent'] = 0
        if 'change' not in data or data['change'] is None:
            data['change'] = 0
        if 'open' not in data or data['open'] is None:
            data['open'] = data.get('price', 0)
        if 'high' not in data or data['high'] is None:
            data['high'] = data.get('price', 0)
        if 'low' not in data or data['low'] is None:
            data['low'] = data.get('price', 0)
        if 'pre_close' not in data or data['pre_close'] is None:
            data['pre_close'] = data.get('price', 0)
        if 'volume' not in data or data['volume'] is None:
            data['volume'] = 'N/A'
        if 'amount' not in data or data['amount'] is None:
            data['amount'] = 'N/A'
        if 'time' not in data or data['time'] is None:
            data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'technical' not in data or data['technical'] is None:
            data['technical'] = {}
        if 'news_sentiment' not in data or data['news_sentiment'] is None:
            data['news_sentiment'] = {}
        if 'memory_history' not in data or data['memory_history'] is None:
            data['memory_history'] = {}
        
        # 确保 technical 数据存在
        tech = data['technical']
        if 'ma' not in tech or tech['ma'] is None:
            tech['ma'] = {}
        if 'macd' not in tech or tech['macd'] is None:
            tech['macd'] = {}
        if 'support' not in tech or tech['support'] is None:
            tech['support'] = data.get('price', 0) * 0.9
        if 'resistance' not in tech or tech['resistance'] is None:
            tech['resistance'] = data.get('price', 0) * 1.1
        if 'volume_ratio' not in tech or tech['volume_ratio'] is None:
            tech['volume_ratio'] = 1
        if 'rsi' not in tech or tech['rsi'] is None:
            tech['rsi'] = 50
        
        stock_name = data.get('stock_name', '未知股票')
        stock_code = data.get('stock_code', '000000')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建股票代码二级目录
        stock_dir = os.path.join(self.output_dir, stock_code)
        os.makedirs(stock_dir, exist_ok=True)
        
        filename = f"{stock_code}_{stock_name}_{timestamp}_DETAILED.pdf"
        filepath = os.path.join(stock_dir, filename)
        
        # 创建 PDF 文档
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=2.5*cm,
            rightMargin=2.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
            title=f"{stock_name} ({stock_code}) 深度分析报告"
        )
        
        # 构建内容
        content = []
        
        # 1. 封面页
        content.extend(self._create_cover(data))
        content.append(PageBreak())
        
        # 2. 重要声明
        content.extend(self._create_disclaimer())
        content.append(Spacer(1, 0.5*cm))
        
        # 3. 投资评级
        content.extend(self._create_rating(data))
        content.append(Spacer(1, 0.5*cm))
        
        # 4. 核心摘要
        content.extend(self._create_executive_summary(data))
        content.append(Spacer(1, 0.5*cm))
        
        # 5. 实时行情
        content.extend(self._create_market_data_detailed(data))
        content.append(Spacer(1, 0.5*cm))
        
        # 6. 技术分析（超详细）
        if data.get('technical'):
            content.extend(self._create_technical_analysis_super_detailed(data))
            content.append(Spacer(1, 0.5*cm))
        
        # 7. 新闻情绪
        if data.get('news_sentiment'):
            content.extend(self._create_sentiment_analysis_detailed(data))
            content.append(Spacer(1, 0.5*cm))
        
        # 8. 历史回顾
        if data.get('memory_history') and data['memory_history'].get('analysis_count', 0) > 0:
            content.extend(self._create_history_review_detailed(data))
            content.append(Spacer(1, 0.5*cm))
        
        # 9. 投资建议（详细）
        content.extend(self._create_investment_advice_detailed(data))
        content.append(Spacer(1, 0.5*cm))
        
        # 10. 情景分析
        content.extend(self._create_scenario_analysis(data))
        content.append(Spacer(1, 0.5*cm))
        
        # 11. 风险提示（详细）
        content.extend(self._create_risk_warning_detailed())
        content.append(Spacer(1, 0.5*cm))
        
        # 12. 报告附录
        content.extend(self._create_appendix(data))
        
        # 生成 PDF
        doc.build(content)
        
        logger.info(f"详细 PDF 报告已生成：{filepath}")
        return filepath

    def _create_cover(self, data: Dict) -> list:
        """创建专业封面"""
        content = []
        
        # 顶部间距
        content.append(Spacer(1, 2*cm))
        
        # 主标题
        title = Paragraph("A 股深度研究报告", self.styles['MainTitle'])
        content.append(title)
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['ChineseText'],
            fontSize=12,
            textColor=colors.HexColor('#64748b'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        subtitle = Paragraph("A-SHARE IN-DEPTH RESEARCH REPORT", subtitle_style)
        content.append(subtitle)
        content.append(Spacer(1, 1.5*cm))
        
        # 分隔线
        line_table = Table([['=' * 50]], colWidths=[15*cm])
        line_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        content.append(line_table)
        content.append(Spacer(1, 1.5*cm))
        
        # 股票信息
        stock_name = data.get('stock_name', '未知股票')
        stock_code = data.get('stock_code', '000000')
        analysis_time = data.get('analysis_timestamp', datetime.now().isoformat())[:19].replace('T', ' ')
        
        info_style = ParagraphStyle(
            'CoverInfo',
            parent=self.styles['ChineseText'],
            fontSize=11,
            spaceBefore=8,
            spaceAfter=8
        )
        
        content.append(Paragraph(f"股票名称：{stock_name}", info_style))
        content.append(Paragraph(f"股票代码：{stock_code}", info_style))
        content.append(Paragraph(f"报告类型：深度研究报告", info_style))
        content.append(Paragraph(f"分析时间：{analysis_time}", info_style))
        content.append(Spacer(1, 1*cm))
        
        # 编制机构
        org_style = ParagraphStyle(
            'OrgInfo',
            parent=self.styles['ChineseText'],
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            spaceBefore=5
        )
        content.append(Paragraph(f"编制机构：A 股专业分析系统", org_style))
        content.append(Paragraph(f"系统版本：v2.7 详细版", org_style))
        content.append(Paragraph(f"分 析 师：AI 分析师", org_style))
        content.append(Paragraph(f"报告编号：ASHARE-{stock_code}-{datetime.now().strftime('%Y%m%d')}", org_style))
        content.append(Spacer(1, 2*cm))
        
        # 保密等级
        secret_style = ParagraphStyle(
            'Secret',
            parent=self.styles['ChineseText'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            alignment=TA_CENTER,
            spaceBefore=10
        )
        content.append(Paragraph("内部资料·注意保密", secret_style))
        
        return content

    def _create_disclaimer(self) -> list:
        """创建重要声明"""
        content = []
        
        title = Paragraph("一、重要声明", self.styles['SectionTitle'])
        content.append(title)
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=self.styles['ChineseText'],
            spaceBefore=6,
            spaceAfter=6,
            leftIndent=10
        )
        
        disclaimers = [
            "1. 报告性质：本报告由 AI 分析系统自动生成，基于公开数据进行技术分析，仅供参考。",
            "2. 投资建议：本报告不构成任何投资建议或推荐，投资者应独立判断，自主决策。",
            "3. 数据准确性：报告数据来源于公开渠道，可能存在延迟或误差，以交易所数据为准。",
            "4. 风险提示：股市有风险，投资需谨慎。过往表现不代表未来收益。",
            "5. 使用限制：本报告仅供个人参考，未经书面许可，不得用于商业用途或公开传播。",
            "6. 责任免除：因使用本报告导致的任何损失，编制方不承担法律责任。"
        ]
        
        for d in disclaimers:
            content.append(Paragraph(d, disclaimer_style))
        
        return content

    def _create_rating(self, data: Dict) -> list:
        """创建投资评级"""
        content = []
        
        title = Paragraph("二、投资评级", self.styles['SectionTitle'])
        content.append(title)
        
        # 确保数据有效
        current_price = data.get('price') or 0
        if current_price <= 0:
            current_price = 0.01  # 避免除零错误
        
        score = self._calculate_score(data)
        rating = self._get_rating_label(score)
        rating_en = self._get_rating_label_en(score)
        target_price = self._calculate_target_price(data) or current_price
        stop_loss = self._calculate_stop_loss(data) or (current_price * 0.9)
        upside = ((target_price - current_price) / current_price * 100) if current_price > 0 else 0
        downside = ((stop_loss - current_price) / current_price * 100) if current_price > 0 else 0
        
        # 评级表格
        rating_data = [
            ['综合评分', f'{score:.1f} / 10.0'],
            ['投资评级', f'{rating} ({rating_en})'],
            ['当前价格', f'¥{current_price:.2f}'],
            ['目标价格', f'¥{target_price:.2f} (潜在空间：{upside:+.1f}%)'],
            ['止损价格', f'¥{stop_loss:.2f} (风险空间：{downside:.1f}%)']
        ]
        
        rating_table = Table(rating_data, colWidths=[5*cm, 8*cm])
        rating_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(rating_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 评级说明
        subtitle = Paragraph("评级说明:", self.styles['SubTitle'])
        content.append(subtitle)
        
        rating_explain = [
            ['强烈推荐', '预计涨幅>20%，技术面与基本面共振向好'],
            ['推荐', '预计涨幅 10-20%，整体表现良好'],
            ['中性', '预计涨幅 -10% 至 10%，震荡整理'],
            ['谨慎', '预计跌幅 10-20%，风险较高'],
            ['回避', '预计跌幅>20%，多项指标走弱']
        ]
        
        explain_table = Table(rating_explain, colWidths=[4*cm, 9*cm])
        explain_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(explain_table)
        
        return content

    def _create_executive_summary(self, data: Dict) -> list:
        """创建核心摘要"""
        content = []
        
        title = Paragraph("三、核心摘要", self.styles['SectionTitle'])
        content.append(title)
        
        stock_name = data.get('stock_name', '未知股票')
        stock_code = data.get('stock_code', '000000')
        price = data.get('price', 0)
        change = data.get('change_percent', 0)
        
        # 基本信息
        summary_data = [
            ['股票名称', f'{stock_name} ({stock_code})'],
            ['当前价格', f'¥{price:.2f}'],
            ['涨跌幅', f'{change:+.2f}%'],
            ['分析时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        summary_table = Table(summary_data, colWidths=[5*cm, 8*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 技术要点
        technical = data.get('technical', {})
        subtitle = Paragraph("技术要点:", self.styles['SubTitle'])
        content.append(subtitle)
        
        tech_points = [
            f"均线排列：{technical.get('ma_arrangement', 'N/A')}",
            f"MACD 信号：{technical.get('macd', {}).get('signal', 'N/A')}",
            f"趋势方向：{technical.get('trend', 'N/A')}",
            f"RSI 指标：{technical.get('rsi', 'N/A')}"
        ]
        
        for point in tech_points:
            content.append(Paragraph(f"• {point}", self.styles['ListText']))
        
        return content

    def _create_market_data_detailed(self, data: Dict) -> list:
        """创建详细行情数据"""
        content = []
        
        title = Paragraph("四、实时行情", self.styles['SectionTitle'])
        content.append(title)
        
        price = data.get('price', 0)
        high = data.get('high', price)
        low = data.get('low', price)
        amplitude = ((high - low) / low * 100) if low else 0
        
        # 行情表格
        market_data = [
            ['当前价', f'¥{price:.2f}', '涨跌额', f'{data.get("change", 0):+.2f}'],
            ['涨跌幅', f'{data.get("change_percent", 0):+.2f}%', '成交量', data.get('volume', 'N/A')],
            ['开盘价', f'¥{data.get("open", 0):.2f}', '成交额', data.get('amount', 'N/A')],
            ['最高价', f'¥{high:.2f}', '昨收价', f'¥{data.get("pre_close", 0):.2f}'],
            ['最低价', f'¥{low:.2f}', '更新时间', str(data.get('time', 'N/A'))[:16]],
            ['日内振幅', f'{amplitude:.2f}%', '量比', str(data.get('technical', {}).get('volume_ratio', 'N/A'))]
        ]
        
        market_table = Table(market_data, colWidths=[4*cm, 5*cm, 4*cm, 5*cm])
        market_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(market_table)
        
        return content

    def _create_technical_analysis_super_detailed(self, data: Dict) -> list:
        """创建超详细技术分析"""
        content = []
        
        title = Paragraph("五、技术分析（详细）", self.styles['SectionTitle'])
        content.append(title)
        
        tech = data.get('technical', {})
        ma = tech.get('ma', {})
        macd = tech.get('macd', {})
        price = data.get('price', 0)
        
        # 1. 均线系统
        subtitle = Paragraph("1. 均线系统", self.styles['SubTitle'])
        content.append(subtitle)
        
        ma_data = [
            ['均线', '数值', '位置', '说明'],
            ['MA5', str(ma.get(5, 'N/A')), self._get_ma_position(price, ma.get(5)), '短期趋势线'],
            ['MA10', str(ma.get(10, 'N/A')), self._get_ma_position(price, ma.get(10)), '半月趋势线'],
            ['MA20', str(ma.get(20, 'N/A')), self._get_ma_position(price, ma.get(20)), '月线（生命线）'],
            ['MA60', str(ma.get(60, 'N/A')), self._get_ma_position(price, ma.get(60)), '季线（决策线）']
        ]
        
        ma_table = Table(ma_data, colWidths=[3*cm, 4*cm, 3*cm, 5*cm])
        ma_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(ma_table)
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph(f"均线排列：{tech.get('ma_arrangement', 'N/A')}", self.styles['ChineseText']))
        content.append(Spacer(1, 0.3*cm))
        
        # 2. MACD 指标
        subtitle = Paragraph("2. MACD 指标", self.styles['SubTitle'])
        content.append(subtitle)
        
        macd_data = [
            ['指标', '数值', '说明'],
            ['DIF（快线）', str(macd.get('dif', 'N/A')), '差离值'],
            ['DEA（慢线）', str(macd.get('dea', 'N/A')), '信号线'],
            ['MACD 柱', str(macd.get('macd', 'N/A')), '红绿柱'],
            ['信号', macd.get('signal', 'N/A'), self._interpret_macd(macd)]
        ]
        
        macd_table = Table(macd_data, colWidths=[5*cm, 4*cm, 6*cm])
        macd_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(macd_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 3. RSI 指标
        subtitle = Paragraph("3. RSI 指标", self.styles['SubTitle'])
        content.append(subtitle)
        
        rsi = tech.get('rsi', 'N/A')
        content.append(Paragraph(f"RSI 数值：{rsi}", self.styles['ChineseText']))
        content.append(Paragraph(f"RSI 状态：{self._get_rsi_status(rsi)}", self.styles['ChineseText']))
        content.append(Paragraph(f"RSI 解读：{self._interpret_rsi(rsi)}", self.styles['ChineseText']))
        content.append(Spacer(1, 0.3*cm))
        
        # 4. 成交量
        subtitle = Paragraph("4. 成交量分析", self.styles['SubTitle'])
        content.append(subtitle)
        
        volume_ratio = tech.get('volume_ratio', 'N/A')
        content.append(Paragraph(f"量比：{volume_ratio}", self.styles['ChineseText']))
        content.append(Paragraph(f"量比解读：{self._interpret_volume_ratio(volume_ratio)}", self.styles['ChineseText']))
        content.append(Spacer(1, 0.3*cm))
        
        # 5. 支撑阻力
        subtitle = Paragraph("5. 支撑与阻力", self.styles['SubTitle'])
        content.append(subtitle)
        
        sr_data = [
            ['类型', '价格', '说明'],
            ['第一支撑位', f"¥{tech.get('support', 'N/A')}", '近期低点'],
            ['第二支撑位', f"¥{tech.get('support', 0) * 0.95 if tech.get('support') else 'N/A'}", '支撑位下方 5%'],
            ['第一阻力位', f"¥{tech.get('resistance', 'N/A')}", '近期高点'],
            ['第二阻力位', f"¥{tech.get('resistance', 0) * 1.05 if tech.get('resistance') else 'N/A'}", '阻力位上方 5%']
        ]
        
        sr_table = Table(sr_data, colWidths=[4*cm, 5*cm, 6*cm])
        sr_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (2, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(sr_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 6. 综合技术评级
        subtitle = Paragraph("6. 综合技术评级", self.styles['SubTitle'])
        content.append(subtitle)
        
        tech_score = self._calculate_technical_score(tech)
        tech_rating = self._get_technical_rating(tech)
        
        rating_data = [
            ['技术评分', f'{tech_score}/100'],
            ['技术评级', tech_rating]
        ]
        
        rating_table = Table(rating_data, colWidths=[5*cm, 8*cm])
        rating_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(rating_table)
        
        return content

    def _create_sentiment_analysis_detailed(self, data: Dict) -> list:
        """创建详细新闻情绪分析"""
        content = []
        
        title = Paragraph("六、新闻情绪分析", self.styles['SectionTitle'])
        content.append(title)
        
        sentiment = data.get('news_sentiment', {})
        
        # 情绪概览
        sentiment_data = [
            ['指标', '数值'],
            ['新闻总数', str(sentiment.get('news_count', 0))],
            ['情绪评分', f'{sentiment.get("avg_sentiment_score", 0):.3f}'],
            ['总体情绪', sentiment.get('overall_sentiment', 'N/A')]
        ]
        
        sentiment_table = Table(sentiment_data, colWidths=[6*cm, 7*cm])
        sentiment_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(sentiment_table)
        
        return content

    def _create_history_review_detailed(self, data: Dict) -> list:
        """创建详细历史回顾"""
        content = []
        
        title = Paragraph("七、历史分析回顾", self.styles['SectionTitle'])
        content.append(title)
        
        history = data.get('memory_history', {})
        
        history_data = [
            ['分析次数', f'{history.get("analysis_count", 0)} 次'],
            ['首次分析', history.get('first_analysis', 'N/A')],
            ['最近分析', history.get('last_analysis', 'N/A')],
            ['主要建议', history.get('most_common_recommendation', 'N/A')]
        ]
        
        history_table = Table(history_data, colWidths=[5*cm, 8*cm])
        history_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(history_table)
        
        return content

    def _create_investment_advice_detailed(self, data: Dict) -> list:
        """创建详细投资建议"""
        content = []
        
        title = Paragraph("八、投资建议", self.styles['SectionTitle'])
        content.append(title)
        
        score = self._calculate_score(data)
        rating = self._get_rating_label(score)
        tech = data.get('technical', {})
        price = data.get('price', 0)
        
        support = tech.get('support', price * 0.9)
        resistance = tech.get('resistance', price * 1.1)
        target_price = self._calculate_target_price(data)
        stop_loss = self._calculate_stop_loss(data)
        
        # 综合建议
        advice_data = [
            ['投资评级', f'{rating}'],
            ['综合评分', f'{score:.1f}/10'],
            ['建议操作', self._get_operation_suggestion(score)],
            ['建议仓位', self._get_position_suggestion(score)]
        ]
        
        advice_table = Table(advice_data, colWidths=[5*cm, 8*cm])
        advice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(advice_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 价格目标
        subtitle = Paragraph("价格目标:", self.styles['SubTitle'])
        content.append(subtitle)
        
        target_data = [
            ['类型', '价格', '空间', '说明'],
            ['短期目标', f'¥{target_price:.2f}', f'{((target_price - price) / price * 100):+.1f}%', '1-2 周'],
            ['中期目标', f'¥{(target_price * 1.1):.2f}', f'{((target_price * 1.1 - price) / price * 100):+.1f}%', '1-3 个月'],
            ['止损价位', f'¥{stop_loss:.2f}', f'{((stop_loss - price) / price * 100):+.1f}%', '风险控制']
        ]
        
        target_table = Table(target_data, colWidths=[4*cm, 4*cm, 4*cm, 5*cm])
        target_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(target_table)
        content.append(Spacer(1, 0.3*cm))
        
        # 操作策略
        subtitle = Paragraph("操作策略:", self.styles['SubTitle'])
        content.append(subtitle)
        
        strategy = self._get_detailed_strategy(score, tech)
        content.append(Paragraph(strategy, self.styles['ChineseText']))
        content.append(Spacer(1, 0.3*cm))
        
        # 关注要点
        subtitle = Paragraph("关注要点:", self.styles['SubTitle'])
        content.append(subtitle)
        
        points = [
            f"关注{support:.2f}支撑位的有效性",
            f"关注{resistance:.2f}阻力位的突破情况",
            "关注 MACD 指标是否持续金叉",
            "关注 RSI 是否出现超买信号",
            "关注成交量变化配合情况"
        ]
        
        for point in points:
            content.append(Paragraph(f"• {point}", self.styles['ListText']))
        
        return content

    def _create_scenario_analysis(self, data: Dict) -> list:
        """创建情景分析"""
        content = []
        
        title = Paragraph("九、情景分析", self.styles['SectionTitle'])
        content.append(title)
        
        price = data.get('price', 0)
        tech = data.get('technical', {})
        support = tech.get('support', price * 0.9)
        resistance = tech.get('resistance', price * 1.1)
        
        # 乐观情景
        subtitle = Paragraph("1. 乐观情景（概率 30%）", self.styles['SubTitle'])
        content.append(subtitle)
        content.append(Paragraph(f"触发条件：突破{resistance:.2f}阻力位，成交量放大 50% 以上", self.styles['ChineseText']))
        content.append(Paragraph(f"目标价格：¥{resistance * 1.15:.2f}", self.styles['ChineseText']))
        content.append(Paragraph(f"操作建议：加仓至 7-8 成，设置移动止损", self.styles['ChineseText']))
        content.append(Spacer(1, 0.2*cm))
        
        # 基准情景
        subtitle = Paragraph("2. 基准情景（概率 50%）", self.styles['SubTitle'])
        content.append(subtitle)
        content.append(Paragraph(f"触发条件：在{support:.2f}-{resistance:.2f}区间震荡", self.styles['ChineseText']))
        content.append(Paragraph(f"目标价格：¥{(support + resistance) / 2:.2f}", self.styles['ChineseText']))
        content.append(Paragraph(f"操作建议：保持 5-6 成仓位，高抛低吸", self.styles['ChineseText']))
        content.append(Spacer(1, 0.2*cm))
        
        # 悲观情景
        subtitle = Paragraph("3. 悲观情景（概率 20%）", self.styles['SubTitle'])
        content.append(subtitle)
        content.append(Paragraph(f"触发条件：跌破{support:.2f}支撑位，MACD 死叉", self.styles['ChineseText']))
        content.append(Paragraph(f"目标价格：¥{support * 0.85:.2f}", self.styles['ChineseText']))
        content.append(Paragraph(f"操作建议：减仓至 3 成以下，严格止损", self.styles['ChineseText']))
        content.append(Spacer(1, 0.2*cm))
        
        # 风险收益比
        upside = ((resistance - price) / price * 100) if price else 0
        downside = ((price - support * 0.85) / price * 100) if price else 0
        ratio = ((resistance - price) / (price - support * 0.85)) if (price - support * 0.85) else 0
        
        risk_reward_data = [
            ['预期收益', f'{upside:.1f}%（乐观情景）'],
            ['预期损失', f'{downside:.1f}%（悲观情景）'],
            ['风险收益比', f'{ratio:.2f}:1']
        ]
        
        rr_table = Table(risk_reward_data, colWidths=[5*cm, 8*cm])
        rr_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(rr_table)
        
        return content

    def _create_risk_warning_detailed(self) -> list:
        """创建详细风险提示"""
        content = []
        
        title = Paragraph("十、风险提示", self.styles['SectionTitle'])
        content.append(title)
        
        risk_style = ParagraphStyle(
            'Risk',
            parent=self.styles['ChineseText'],
            spaceBefore=4,
            spaceAfter=4,
            leftIndent=10
        )
        
        content.append(Paragraph("市场风险:", self.styles['SubTitle']))
        risks_market = [
            "□ 大盘系统性风险（风险等级：中高）",
            "□ 行业政策变化风险（风险等级：中）",
            "□ 市场流动性风险（风险等级：低）"
        ]
        for r in risks_market:
            content.append(Paragraph(r, risk_style))
        
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("技术风险:", self.styles['SubTitle']))
        risks_tech = [
            "□ 技术指标失效风险（风险等级：中）",
            "□ 数据延迟风险（风险等级：低）",
            "□ 模型误差风险（风险等级：中）"
        ]
        for r in risks_tech:
            content.append(Paragraph(r, risk_style))
        
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("风险应对:", self.styles['SubTitle']))
        risk_measures = [
            "1. 严格控制仓位，单只股票不超过总仓位的 20%",
            "2. 设置止损位，亏损达到 5% 坚决止损",
            "3. 分散投资，不集中持有单一行业股票",
            "4. 定期复盘，及时调整投资策略",
            "5. 关注公告，及时获取公司信息"
        ]
        for r in risk_measures:
            content.append(Paragraph(r, risk_style))
        
        content.append(Spacer(1, 0.3*cm))
        
        # 风险评级
        risk_rating_data = [
            ['综合风险等级', '中等风险（R3）'],
            ['适合投资者', '稳健型及以上']
        ]
        
        risk_rating_table = Table(risk_rating_data, colWidths=[5*cm, 8*cm])
        risk_rating_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(risk_rating_table)
        
        return content

    def _create_appendix(self, data: Dict) -> list:
        """创建报告附录"""
        content = []
        
        title = Paragraph("十一、报告附录", self.styles['SectionTitle'])
        content.append(title)
        
        appendix_style = ParagraphStyle(
            'Appendix',
            parent=self.styles['ChineseText'],
            spaceBefore=4,
            spaceAfter=4
        )
        
        content.append(Paragraph("数据来源:", self.styles['SubTitle']))
        sources = [
            "1. 实时行情：新浪财经 API",
            "2. 技术指标：东方财富网 API",
            "3. 新闻情绪：Firecrawl 网页抓取（可选）",
            "4. 历史记忆：Elite Long-term Memory"
        ]
        for s in sources:
            content.append(Paragraph(s, appendix_style))
        
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("分析方法:", self.styles['SubTitle']))
        methods = [
            "1. 技术分析：均线、MACD、RSI 等指标分析",
            "2. 情绪分析：新闻文本 AI 情感分析",
            "3. 综合评分：多维度加权评分模型"
        ]
        for m in methods:
            content.append(Paragraph(m, appendix_style))
        
        content.append(Spacer(1, 0.2*cm))
        content.append(Paragraph("指标说明:", self.styles['SubTitle']))
        indicators = [
            "MA：移动平均线，反映价格趋势",
            "MACD：指数平滑异同移动平均线，反映趋势强弱",
            "RSI：相对强弱指标，反映超买超卖状态"
        ]
        for i in indicators:
            content.append(Paragraph(i, appendix_style))
        
        content.append(Spacer(1, 0.3*cm))
        
        # 报告信息
        info_data = [
            ['报告生成时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['报告生成系统', 'A 股专业分析系统 v2.7'],
            ['数据截止时间', str(data.get('time', 'N/A'))[:16]],
            ['报告编号', f'ASHARE-{data.get("stock_code", "000000")}-{datetime.now().strftime("%Y%m%d")}']
        ]
        
        info_table = Table(info_data, colWidths=[5*cm, 8*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        
        content.append(info_table)
        
        return content

    # ========== 辅助方法 ==========

    def _calculate_score(self, data: Dict) -> float:
        """计算综合评分"""
        score = 5.0
        technical = data.get('technical', {})
        
        if technical.get('signal') == 'bullish':
            score += 1.5
        elif technical.get('signal') == 'bearish':
            score -= 1.5
        
        if technical.get('trend') == 'bullish':
            score += 0.5
        elif technical.get('trend') == 'bearish':
            score -= 0.5
        
        sentiment = data.get('news_sentiment', {})
        sentiment_score = sentiment.get('avg_sentiment_score', 0.5)
        score += (sentiment_score - 0.5) * 3
        
        change = data.get('change_percent', 0)
        if change > 3:
            score += 0.5
        elif change < -3:
            score -= 0.5
        
        return max(0, min(10, score))

    def _get_rating_label(self, score: float) -> str:
        if score >= 8: return "强烈推荐"
        elif score >= 6: return "推荐"
        elif score >= 4: return "中性"
        elif score >= 2: return "谨慎"
        else: return "回避"

    def _get_rating_label_en(self, score: float) -> str:
        if score >= 8: return "STRONG BUY"
        elif score >= 6: return "BUY"
        elif score >= 4: return "HOLD"
        elif score >= 2: return "CAUTION"
        else: return "AVOID"

    def _calculate_target_price(self, data: Dict) -> float:
        tech = data.get('technical', {})
        return tech.get('resistance', data.get('price', 0) * 1.1)

    def _calculate_stop_loss(self, data: Dict) -> float:
        tech = data.get('technical', {})
        support = tech.get('support', data.get('price', 0) * 0.9)
        return support * 0.97

    def _get_ma_position(self, price: float, ma) -> str:
        if ma == 'N/A' or ma == 0: return "N/A"
        return "上方" if price > ma else "下方"

    def _interpret_macd(self, macd: Dict) -> str:
        signal = macd.get('signal', '')
        interpretations = {
            'bullish': '多头强势',
            'bearish': '空头强势',
            'golden_cross': '金叉买入',
            'dead_cross': '死叉卖出'
        }
        return interpretations.get(signal, '信号不明')

    def _get_rsi_status(self, rsi) -> str:
        if rsi == 'N/A': return "N/A"
        if rsi >= 80: return "严重超买"
        elif rsi >= 70: return "超买"
        elif rsi >= 50: return "偏强"
        elif rsi >= 30: return "偏弱"
        else: return "超卖"

    def _interpret_rsi(self, rsi) -> str:
        if rsi == 'N/A': return "数据不足"
        if rsi >= 80: return "RSI 严重超买，警惕回调风险，建议减仓"
        elif rsi >= 70: return "RSI 超买，短期可能回调，建议谨慎"
        elif rsi >= 50: return "RSI 偏强，上涨动能充足，可继续持有"
        elif rsi >= 30: return "RSI 偏弱，下跌动能释放，建议观望"
        else: return "RSI 超卖，可能反弹，可关注"

    def _interpret_volume_ratio(self, volume_ratio) -> str:
        if volume_ratio == 'N/A': return "数据不足"
        if volume_ratio > 2: return "成交量明显放大，资金活跃，关注持续性"
        elif volume_ratio > 1: return "成交量温和放大，资金流入，健康状态"
        elif volume_ratio > 0.5: return "成交量正常，市场平稳"
        else: return "成交量萎缩，市场清淡，观望为主"

    def _calculate_technical_score(self, tech: Dict) -> int:
        score = 50
        if tech.get('signal') == 'bullish': score += 20
        elif tech.get('signal') == 'bearish': score -= 20
        if tech.get('trend') == 'bullish': score += 15
        elif tech.get('trend') == 'bearish': score -= 15
        rsi = tech.get('rsi', 50)
        if 40 <= rsi <= 60: score += 10
        elif rsi > 70 or rsi < 30: score -= 10
        return max(0, min(100, score))

    def _get_technical_rating(self, tech: Dict) -> str:
        score = self._calculate_technical_score(tech)
        if score >= 80: return "强势（建议积极操作）"
        elif score >= 60: return "偏强（建议适度参与）"
        elif score >= 40: return "中性（建议观望）"
        elif score >= 20: return "偏弱（建议谨慎）"
        else: return "弱势（建议回避）"

    def _get_operation_suggestion(self, score: float) -> str:
        if score >= 8: return "积极买入，逢低布局"
        elif score >= 6: return "适度增持，波段操作"
        elif score >= 4: return "保持观望，等待信号"
        elif score >= 2: return "谨慎减持，控制仓位"
        else: return "建议回避，等待企稳"

    def _get_position_suggestion(self, score: float) -> str:
        if score >= 8: return "建议仓位 7-8 成，可积极操作"
        elif score >= 6: return "建议仓位 5-6 成，适度参与"
        elif score >= 4: return "建议仓位 3-4 成，保持灵活"
        elif score >= 2: return "建议仓位 1-2 成，控制风险"
        else: return "建议仓位 0-1 成，观望为主"

    def _get_detailed_strategy(self, score: float, tech: Dict) -> str:
        support = tech.get('support', 0)
        resistance = tech.get('resistance', 0)
        if score >= 7:
            return f"突破{resistance:.2f}加仓，回调{support:.2f}不破持有，止损设{support * 0.97:.2f}"
        elif score >= 5:
            return f"{support:.2f}-{resistance:.2f}区间操作，突破跟进，破位止损"
        else:
            return f"反弹{resistance:.2f}减仓，跌破{support:.2f}止损，观望为主"

    def save_report(self, report: str, stock_code: str, stock_name: str) -> str:
        """保存报告（兼容接口）"""
        # PDF 报告直接生成，此方法用于兼容
        return self.generate_pdf({})


if __name__ == "__main__":
    # 测试
    test_data = {
        "stock_code": "600619",
        "stock_name": "海立股份",
        "price": 18.99,
        "change_percent": 1.28,
        "technical": {
            "signal": "bullish",
            "trend": "neutral",
            "ma": {5: 18.68, 10: 18.53, 20: 18.85, 60: 20.25},
            "ma_arrangement": "震荡整理",
            "macd": {"dif": -0.4622, "dea": -0.5699, "macd": 0.2155, "signal": "golden_cross"},
            "rsi": 53.23,
            "volume_ratio": 1.24,
            "support": 18.02,
            "resistance": 18.99
        },
        "news_sentiment": {"avg_sentiment_score": 0.5, "overall_sentiment": "UNKNOWN"}
    }
    
    generator = AShareDetailedPDFReport()
    filepath = generator.generate_pdf(test_data)
    print(f"详细 PDF 已生成：{filepath}")
