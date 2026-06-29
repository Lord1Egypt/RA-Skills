#!/usr/bin/env python3
"""
Cross-Border Multi-Country Tax Quick Lookup
跨境多国税务速查 — 30+国家税率/申报周期/注册门槛/EU OSS方案
Usage:
    python cross_border_tax.py "德国VAT税率"
    python cross_border_tax.py "英国 法国 日本 对比"
    python cross_border_tax.py "欧盟OSS怎么报"
    python cross_border_tax.py --list  # 列出所有支持国家
"""

import sys
import os
import json
import re

# Fix Windows GBK encoding for emoji output
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime, date
from pathlib import Path

# ─── Tax Database ───────────────────────────────────────────────

TAX_DB = {
    # ═══ EU 27 Member States ═══
    "德国": {
        "en": "Germany", "code": "DE", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 19, "reduced_rates": [7],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟卖家）/ 本国小企业€22,000豁免",
        "filing_frequency": "月度（标准）/ 季度（年VAT<€7,500）",
        "filing_deadline": "每月10日（次年5月31日前提交年度汇总）",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "平台（Amazon/eBay）对非欧盟卖家≤€150商品承担代收代缴义务",
            "电子服务B2C按消费者所在国税率",
            "逆向征税适用于B2B交易",
        ],
        "notes": "欧盟最大电商市场，VAT合规最严格",
    },
    "法国": {
        "en": "France", "code": "FR", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 20, "reduced_rates": [10, 5.5, 2.1],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟卖家）/ 本国服务业€36,800/商品€91,900豁免",
        "filing_frequency": "月度（标准）/ 季度（可选）",
        "filing_deadline": "每月15-24日（视地区）",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "有四档税率（20%/10%/5.5%/2.1%），为EU最复杂税率体系之一",
            "电子书适用5.5%减税率",
            "2024年起平台代收代缴扩展",
        ],
        "notes": "四档税率，注意区分商品类别",
    },
    "意大利": {
        "en": "Italy", "code": "IT", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 22, "reduced_rates": [10, 5, 4],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟卖家）/ 本国€85,000小规模豁免",
        "filing_frequency": "月度（或季度，需付1%附加费）",
        "filing_deadline": "每月16日，季度为次月16日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "电子书适用4%超减税率",
            "平台代收代缴非欧盟卖家VAT",
            "FBA库存必须本地VAT注册",
        ],
        "notes": "欧盟第三大电商市场",
    },
    "西班牙": {
        "en": "Spain", "code": "ES", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [10, 4],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（一般无小企业豁免）",
        "filing_frequency": "月度/季度（SII即时申报系统）",
        "filing_deadline": "每月20日（季度: Q1→4/20, Q2→7/20, Q3→10/20, Q4→1/30）",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "SII实时信息系统要求大型企业8天内提交",
            "加那利群岛、休达和梅利利亚适用不同税制",
            "数字服务4%税率",
        ],
        "notes": "SII系统对年营收>€6M企业强制",
    },
    "荷兰": {
        "en": "Netherlands", "code": "NL", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [9],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€20,000小企业豁免",
        "filing_frequency": "季度（标准）/ 月度（高额）",
        "filing_deadline": "季度结束后次月最后一天",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "欧盟主要物流枢纽，多国库存极易触发本地注册",
            "电子书适用9%减税率",
            "允许申请增值税递延（Article 23）",
        ],
        "notes": "⚠ FBA卖家高发区：荷兰仓库库存自动触发本地VAT注册",
    },
    "比利时": {
        "en": "Belgium", "code": "BE", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [12, 6],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€25,000小企业豁免",
        "filing_frequency": "月度（标准）/ 季度（年VAT<€50,000）",
        "filing_deadline": "每月20日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "EU总部所在地，VAT合规要求严格",
            "Liège机场为重要物流节点",
        ],
        "notes": "",
    },
    "波兰": {
        "en": "Poland", "code": "PL", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 23, "reduced_rates": [8, 5],
        "currency": "PLN", "currency_symbol": "zł",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国PLN 200,000（约€47,000）豁免",
        "filing_frequency": "月度（标准）/ 季度（小企业）",
        "filing_deadline": "每月25日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "欧盟增长最快的电商市场之一",
            "JPK审计文件强制电子提交",
        ],
        "notes": "东欧最大电商市场",
    },
    "瑞典": {
        "en": "Sweden", "code": "SE", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 25, "reduced_rates": [12, 6],
        "currency": "SEK", "currency_symbol": "kr",
        "registration_threshold": "无最低门槛（非欧盟）",
        "filing_frequency": "月度（大企业）/ 季度（中小企业）/ 年度（微型）",
        "filing_deadline": "月度: 12日；季度/年: 次月12日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "北欧最大电商市场",
            "食品12%，书籍/文化6%",
        ],
        "notes": "",
    },
    "奥地利": {
        "en": "Austria", "code": "AT", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 20, "reduced_rates": [13, 10],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€35,000小企业豁免",
        "filing_frequency": "月度（标准）/ 季度（上年VAT<€12,000）",
        "filing_deadline": "月度/季度结束后次月15日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "爱尔兰": {
        "en": "Ireland", "code": "IE", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 23, "reduced_rates": [13.5, 9, 4.8],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国服务€40,000/商品€80,000豁免",
        "filing_frequency": "双月（标准）/ 季度/ 半年/ 年",
        "filing_deadline": "双月: 次月19日；季度: 次月23日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "有四档税率（23%/13.5%/9%/4.8%）",
            "英国脱欧后贸易合规边界",
        ],
        "notes": "",
    },
    "葡萄牙": {
        "en": "Portugal", "code": "PT", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 23, "reduced_rates": [13, 6],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€14,500小企业豁免",
        "filing_frequency": "月度（年营收>€650,000）/ 季度（<€650,000）",
        "filing_deadline": "月度: 次月10日；季度: 次月15日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "马德拉群岛和亚速尔群岛适用不同税率",
        ],
        "notes": "",
    },
    "希腊": {
        "en": "Greece", "code": "GR", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 24, "reduced_rates": [13, 6],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€10,000小企业豁免",
        "filing_frequency": "月度（标准）/ 季度（小企业）",
        "filing_deadline": "月度: 次月最后一天",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "部分岛屿适用减税率（30%折扣）",
        ],
        "notes": "",
    },
    "捷克": {
        "en": "Czech Republic", "code": "CZ", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [12],
        "currency": "CZK", "currency_symbol": "Kč",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国CZK 2,000,000（约€85,000）豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月25日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "控制报告（Kontrolní hlášení）强制电子提交",
        ],
        "notes": "",
    },
    "罗马尼亚": {
        "en": "Romania", "code": "RO", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [9, 5],
        "currency": "RON", "currency_symbol": "lei",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国RON 300,000（约€60,000）豁免",
        "filing_frequency": "月度（标准）/ 季度（小企业）",
        "filing_deadline": "每月25日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "⚠ 2026年标准税率可能从19%上调至21%（讨论中）",
            "SAF-T电子审计文件强制",
        ],
        "notes": "税率上调正在讨论中，需密切关注",
    },
    "匈牙利": {
        "en": "Hungary", "code": "HU", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 27, "reduced_rates": [18, 5],
        "currency": "HUF", "currency_symbol": "Ft",
        "registration_threshold": "无最低门槛（非欧盟）",
        "filing_frequency": "月度（标准）/ 季度/ 年（低额）",
        "filing_deadline": "每月20日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "⚠ 欧盟最高VAT税率27%",
            "实时发票报告系统强制",
        ],
        "notes": "全球最高VAT之一，定价需特别注意",
    },
    "丹麦": {
        "en": "Denmark", "code": "DK", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 25, "reduced_rates": [],
        "currency": "DKK", "currency_symbol": "kr",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国DKK 50,000豁免",
        "filing_frequency": "半年（标准）/ 季度（大企业）",
        "filing_deadline": "半年度: 3月1日/9月1日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "⚠ 唯一无减免税率的EU国家，几乎所有商品服务25%",
        ],
        "notes": "无减税率！所有商品统一25%",
    },
    "芬兰": {
        "en": "Finland", "code": "FI", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 25.5, "reduced_rates": [14, 10],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€15,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "次月12日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "2024年9月从24%上调至25.5%",
        ],
        "notes": "近年税率上调",
    },
    "保加利亚": {
        "en": "Bulgaria", "code": "BG", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 20, "reduced_rates": [9],
        "currency": "BGN", "currency_symbol": "лв",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国BGN 50,000（约€25,500）豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月14日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "克罗地亚": {
        "en": "Croatia", "code": "HR", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 25, "reduced_rates": [13, 5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€35,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月20日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "2023年加入欧元区",
        ],
        "notes": "",
    },
    "斯洛伐克": {
        "en": "Slovakia", "code": "SK", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 23, "reduced_rates": [10],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€49,790豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月25日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "⚠ 2025年1月从20%大幅上调至23%",
        ],
        "notes": "近年大幅上调税率",
    },
    "立陶宛": {
        "en": "Lithuania", "code": "LT", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [9, 5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€45,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月25日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "拉脱维亚": {
        "en": "Latvia", "code": "LV", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 21, "reduced_rates": [12, 5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€50,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月20日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "斯洛文尼亚": {
        "en": "Slovenia", "code": "SI", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 22, "reduced_rates": [9.5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€50,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "次月最后一天",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "爱沙尼亚": {
        "en": "Estonia", "code": "EE", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 24, "reduced_rates": [9],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€40,000豁免",
        "filing_frequency": "月度",
        "filing_deadline": "每月20日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "⚠ 2026年1月从22%上调至24%",
            "电子居民计划便利远程注册",
        ],
        "notes": "2026年刚上调2个点",
    },
    "塞浦路斯": {
        "en": "Cyprus", "code": "CY", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 19, "reduced_rates": [9, 5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€15,600豁免",
        "filing_frequency": "季度",
        "filing_deadline": "季度结束次月10日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },
    "卢森堡": {
        "en": "Luxembourg", "code": "LU", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 17, "reduced_rates": [14, 8, 3],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€35,000豁免",
        "filing_frequency": "月度（年VAT>€10,000）/ 季度（<€10,000）",
        "filing_deadline": "月度: 次月15日；季度: 次月15日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [
            "欧盟最低标准VAT税率17%",
            "流行作为欧盟数字服务总部",
        ],
        "notes": "欧盟最低税率",
    },
    "马耳他": {
        "en": "Malta", "code": "MT", "region": "EU",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 18, "reduced_rates": [7, 5],
        "currency": "EUR", "currency_symbol": "€",
        "registration_threshold": "无最低门槛（非欧盟）/ 本国€35,000豁免（部分行业€24,000）",
        "filing_frequency": "季度",
        "filing_deadline": "季度结束次月15日",
        "oss_eligible": True, "ioss_eligible": False,
        "special_rules": [],
        "notes": "",
    },

    # ═══ 欧洲其他 ═══
    "英国": {
        "en": "United Kingdom", "code": "GB", "region": "Europe",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 20, "reduced_rates": [5, 0],
        "currency": "GBP", "currency_symbol": "£",
        "registration_threshold": "非英国卖家：无最低门槛（有销售即须注册）/ 本国£90,000（12个月滚动）",
        "filing_frequency": "季度",
        "filing_deadline": "季度结束后1个月+7天",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "⚠ B2C货值≤£135：VAT在销售点由卖家/平台收取并缴纳（平台代收代缴）",
            "B2C货值>£135：VAT与关税在边境向买方收取",
            "脱欧后不再适用EU OSS，需单独注册UK VAT",
            "英国有自己的OSS-like系统（UK OSS仅用于北爱尔兰）",
            "数字服务2%",
        ],
        "notes": "脱欧后独立税制，≤£135商品平台强制代收",
    },

    # ═══ 北美 ═══
    "美国": {
        "en": "United States", "code": "US", "region": "Americas",
        "tax_type": "Sales Tax", "tax_name_cn": "销售税",
        "standard_rate": "0-10%+（各州不同，平均6-8%）",
        "currency": "USD", "currency_symbol": "$",
        "registration_threshold": "经济关联（Economic Nexus）：典型$100,000年销售额或200笔交易（各州不同）",
        "filing_frequency": "月度/季度/年（取决于各州销售额）",
        "filing_deadline": "各州不同，一般为次月20日",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "⚠ 无联邦销售税，45州+DC分别征收",
            "主要电商州税率：加州7.25%起，纽约4%起，德州6.25%起",
            "Marketplace Facilitator规则：Amazon/Walmart等平台代收代缴",
            "2026年起取消$800进口免税（de minimis废止）",
        ],
        "notes": "45个州+DC独立税制，平台代收减轻合规负担",
    },
    "加拿大": {
        "en": "Canada", "code": "CA", "region": "Americas",
        "tax_type": "GST/HST/PST", "tax_name_cn": "商品服务税/统一销售税",
        "standard_rate": "GST 5% + PST(各省0-10%)",
        "currency": "CAD", "currency_symbol": "C$",
        "registration_threshold": "非居民卖家年销售>CAD 30,000须注册GST/HST",
        "filing_frequency": "季度/年度（取决于年销售额）",
        "filing_deadline": "季度结束次月最后一天",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "联邦GST 5% + 省级PST/HST（安大略HST 13%，魁北克QST 9.975%）",
            "2025年7月起平台（Amazon等）年销售>CAD 30k须代收代缴",
            "进口低价值商品GST起征仅CAD $20",
        ],
        "notes": "联邦+省双层税制，低价值商品GST起征极低",
    },

    # ═══ 亚太 ═══
    "日本": {
        "en": "Japan", "code": "JP", "region": "Asia-Pacific",
        "tax_type": "CT", "tax_name_cn": "消费税",
        "standard_rate": 10, "reduced_rates": [8],
        "currency": "JPY", "currency_symbol": "¥",
        "registration_threshold": "年度应税销售>¥10,000,000（约$67,000）须注册",
        "filing_frequency": "年度（可选择中期申报）",
        "filing_deadline": "财年结束后2个月内（通常3月底→5月底）",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "食品/饮料（不含酒类）适用8%减税率",
            "非居民企业须指定日本国内纳税管理人",
            "2023年10月发票制度改革（インボイス制度）",
            "跨境数字服务按消费者所在征税",
        ],
        "notes": "发票制度改革后需注册开具合格发票",
    },
    "澳大利亚": {
        "en": "Australia", "code": "AU", "region": "Asia-Pacific",
        "tax_type": "GST", "tax_name_cn": "商品服务税",
        "standard_rate": 10, "reduced_rates": [],
        "currency": "AUD", "currency_symbol": "A$",
        "registration_threshold": "年度营业额>A$75,000须注册",
        "filing_frequency": "月度/季度（取决于年营业额）",
        "filing_deadline": "月度: 次月21日；季度: 次月28日",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "⚠ 进口低价值商品（≤A$1,000）也须缴纳GST",
            "平台（Amazon/eBay/Etsy）就低价值进口商品代收代缴GST",
            "B2B逆向征税适用非居民供应商",
        ],
        "notes": "低价值进口商品GST起征点为A$0（即无豁免），平台代收",
    },
    "新加坡": {
        "en": "Singapore", "code": "SG", "region": "Asia-Pacific",
        "tax_type": "GST", "tax_name_cn": "商品服务税",
        "standard_rate": 9, "reduced_rates": [],
        "currency": "SGD", "currency_symbol": "S$",
        "registration_threshold": "全球年营收>S$1,000,000或本地B2C销售>S$100,000须注册（海外数字服务供应商）",
        "filing_frequency": "季度",
        "filing_deadline": "季度结束后1个月内",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "2024年1月从8%上调至9%",
            "海外数字服务供应商强制GST注册（Overseas Vendor Registration）",
            "低价值进口商品自2023年1月起征收GST",
        ],
        "notes": "2024年刚上调至9%",
    },
    "新西兰": {
        "en": "New Zealand", "code": "NZ", "region": "Asia-Pacific",
        "tax_type": "GST", "tax_name_cn": "商品服务税",
        "standard_rate": 15, "reduced_rates": [],
        "currency": "NZD", "currency_symbol": "NZ$",
        "registration_threshold": "年度营业额>NZD 60,000须注册（含海外卖家远程销售）",
        "filing_frequency": "月度/双月/半年（取决于营业额）",
        "filing_deadline": "次月28日",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "低价值进口商品（≤NZD 1,000）由平台代收GST",
            "海外服务供应商年销售>NZD 60,000须注册",
        ],
        "notes": "",
    },
    "印度": {
        "en": "India", "code": "IN", "region": "Asia-Pacific",
        "tax_type": "GST", "tax_name_cn": "商品服务税",
        "standard_rate": "多档（最常用18%）",
        "currency": "INR", "currency_symbol": "₹",
        "registration_threshold": "年度销售>INR 20 lakhs（约$25,000）须注册",
        "filing_frequency": "月度/季度（取决于方案）",
        "filing_deadline": "月度: 次月20日；季度方案: 次月25日",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "多档税率: 0%/5%/12%/18%/28%",
            "跨境电商需注册并指定印度代理人",
            "2024年废除了2%平衡税",
        ],
        "notes": "多档税率体系复杂，18%最为常用",
    },

    # ═══ 中东 ═══
    "阿联酋": {
        "en": "United Arab Emirates", "code": "AE", "region": "Middle East",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 5, "reduced_rates": [],
        "currency": "AED", "currency_symbol": "د.إ",
        "registration_threshold": "年度进口/销售>AED 375,000（约$102,000）强制注册；AED 187,500可自愿注册",
        "filing_frequency": "季度（标准）",
        "filing_deadline": "季度结束后28天内",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "全球最低VAT之一（5%）",
            "企业所得税基本0%（自贸区外9%）",
            "非居民供应商若向UAE消费者销售需注册",
        ],
        "notes": "全球最低VAT税率之一",
    },
    "沙特阿拉伯": {
        "en": "Saudi Arabia", "code": "SA", "region": "Middle East",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 15, "reduced_rates": [],
        "currency": "SAR", "currency_symbol": "ر.س",
        "registration_threshold": "年度营业额>SAR 375,000（约$100,000）强制注册",
        "filing_frequency": "月度（年营收>SAR 40M）/ 季度（<SAR 40M）",
        "filing_deadline": "月度/季度结束后次月最后一天",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "非居民供应商需指定沙特税务代表",
            "2020年从5%大幅上调至15%",
        ],
        "notes": "",
    },

    # ═══ 拉美 ═══
    "墨西哥": {
        "en": "Mexico", "code": "MX", "region": "Americas",
        "tax_type": "VAT", "tax_name_cn": "增值税",
        "standard_rate": 16, "reduced_rates": [0],
        "currency": "MXN", "currency_symbol": "Mex$",
        "registration_threshold": "⚠ 无最低门槛，无论销售额均须注册",
        "filing_frequency": "月度",
        "filing_deadline": "每月17日",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "⚠ 无注册门槛！任何销售都需注册",
            "自2025年1月起外国电商平台强制代收16% VAT",
            "进口纺织品加征35%关税",
            "需指定墨西哥本地法定代表人",
        ],
        "notes": "⚠ 无门槛强制注册，2025年平台代收规则生效",
    },
    "巴西": {
        "en": "Brazil", "code": "BR", "region": "Americas",
        "tax_type": "ICMS/IPI/ISS", "tax_name_cn": "流转税/工业品税/服务税",
        "standard_rate": "~18%（ICMS州税为主），另加IPI和ISS",
        "currency": "BRL", "currency_symbol": "R$",
        "registration_threshold": "复杂：各州不同，跨境电商平台需代收ICMS",
        "filing_frequency": "月度（各州ICMS）",
        "filing_deadline": "各州不同",
        "oss_eligible": False, "ioss_eligible": False,
        "special_rules": [
            "⚠ 世界最复杂的税制之一：联邦+州+市三级",
            "跨境电商平台（Shopee/AliExpress/Shein）须代收17% ICMS",
            "2024年Remessa Conforme计划：≤$50进口包裹适用17% ICMS",
            "需本地实体或代理人",
        ],
        "notes": "税制极其复杂，建议通过本地代理或平台销售",
    },
}

# ═══ EU OSS / IOSS Knowledge Base ═══

OSS_IOSS_KNOWLEDGE = {
    "overview": {
        "title": "EU OSS/IOSS 一站式申报方案",
        "description": "OSS（One-Stop Shop）是欧盟为简化跨境电商VAT申报推出的机制，允许卖家在一国注册后覆盖全EU申报。IOSS专用于从非欧盟进口的低价值商品。",
    },
    "schemes": [
        {
            "name": "Union OSS",
            "who": "在欧盟境内设立的卖家",
            "covers": "跨境B2C商品销售（已在EU境内）+数字/TBE服务",
            "register_where": "卖家本国",
            "filing": "季度一次",
            "threshold": "欧盟跨境B2C年销售合计>€10,000",
        },
        {
            "name": "Non-Union OSS",
            "who": "非欧盟设立的企业",
            "covers": "向EU消费者提供数字/TBE服务",
            "register_where": "任选一个EU成员国",
            "filing": "季度一次",
            "threshold": "无门槛，自愿注册",
        },
        {
            "name": "IOSS (Import OSS)",
            "who": "任何从非欧盟向EU发货的卖家",
            "covers": "B2C进口商品，单件内在价值≤€150",
            "register_where": "EU成员国 + 需指定财政代表（非EU卖家）",
            "filing": "月度一次",
            "threshold": "无门槛，自愿注册（仅限≤€150商品）",
        },
    ],
    "filing_deadlines": {
        "Q1": "4月30日",
        "Q2": "7月31日",
        "Q3": "10月31日",
        "Q4": "次年1月31日",
        "IOSS_monthly": "次月最后一天",
    },
    "key_changes": [
        {"date": "2025年7月1日", "event": "平台视为供应商规则扩展（短租/客运推迟至2028/2030）"},
        {"date": "2026年7月1日", "event": "⚠ 150欧元关税豁免废止，每个包裹征收€3过渡统一关税"},
        {"date": "约2028年3月1日", "event": "IOSS 150欧元上限取消；平台成为视为进口商；€3过渡关税终止"},
        {"date": "2028年7月1日", "event": "ViDA单一VAT注册生效：多库存国不再需要逐国注册"},
    ],
    "important_notes": [
        "即使低于€10,000阈值，如果在多个成员国持有库存（如泛欧FBA），也必须逐国注册！",
        "非欧盟主体不能使用Union OSS，必须用IOSS（≤€150）或逐国注册",
        "消费税商品（酒精、烟草、能源产品）不适用OSS，必须目的国注册",
        "OSS申报中包含的VAT不能用于进项抵扣",
    ],
}

# ═══ Alias Mapping ═══

ALIASES = {
    "de": "德国", "germany": "德国", "deu": "德国",
    "fr": "法国", "france": "法国", "fra": "法国",
    "it": "意大利", "italy": "意大利", "ita": "意大利",
    "es": "西班牙", "spain": "西班牙", "esp": "西班牙",
    "nl": "荷兰", "netherlands": "荷兰", "nld": "荷兰", "holland": "荷兰",
    "be": "比利时", "belgium": "比利时", "bel": "比利时",
    "pl": "波兰", "poland": "波兰", "pol": "波兰",
    "se": "瑞典", "sweden": "瑞典", "swe": "瑞典",
    "at": "奥地利", "austria": "奥地利", "aut": "奥地利",
    "ie": "爱尔兰", "ireland": "爱尔兰", "irl": "爱尔兰",
    "pt": "葡萄牙", "portugal": "葡萄牙", "prt": "葡萄牙",
    "gr": "希腊", "greece": "希腊", "grc": "希腊",
    "cz": "捷克", "czech": "捷克", "cze": "捷克", "czech republic": "捷克",
    "ro": "罗马尼亚", "romania": "罗马尼亚", "rou": "罗马尼亚",
    "hu": "匈牙利", "hungary": "匈牙利", "hun": "匈牙利",
    "dk": "丹麦", "denmark": "丹麦", "dnk": "丹麦",
    "fi": "芬兰", "finland": "芬兰", "fin": "芬兰",
    "bg": "保加利亚", "bulgaria": "保加利亚", "bgr": "保加利亚",
    "hr": "克罗地亚", "croatia": "克罗地亚", "hrv": "克罗地亚",
    "sk": "斯洛伐克", "slovakia": "斯洛伐克", "svk": "斯洛伐克",
    "lt": "立陶宛", "lithuania": "立陶宛", "ltu": "立陶宛",
    "lv": "拉脱维亚", "latvia": "拉脱维亚", "lva": "拉脱维亚",
    "si": "斯洛文尼亚", "slovenia": "斯洛文尼亚", "svn": "斯洛文尼亚",
    "ee": "爱沙尼亚", "estonia": "爱沙尼亚", "est": "爱沙尼亚",
    "cy": "塞浦路斯", "cyprus": "塞浦路斯", "cyp": "塞浦路斯",
    "lu": "卢森堡", "luxembourg": "卢森堡", "lux": "卢森堡",
    "mt": "马耳他", "malta": "马耳他", "mlt": "马耳他",
    "gb": "英国", "uk": "英国", "united kingdom": "英国", "england": "英国", "gbr": "英国",
    "us": "美国", "usa": "美国", "united states": "美国", "america": "美国",
    "ca": "加拿大", "canada": "加拿大", "can": "加拿大",
    "jp": "日本", "japan": "日本", "jpn": "日本",
    "au": "澳大利亚", "australia": "澳大利亚", "aus": "澳大利亚",
    "sg": "新加坡", "singapore": "新加坡", "sgp": "新加坡",
    "nz": "新西兰", "new zealand": "新西兰", "nzl": "新西兰",
    "in": "印度", "india": "印度", "ind": "印度",
    "ae": "阿联酋", "uae": "阿联酋", "united arab emirates": "阿联酋", "are": "阿联酋",
    "sa": "沙特阿拉伯", "saudi arabia": "沙特阿拉伯", "saudi": "沙特阿拉伯", "sau": "沙特阿拉伯",
    "mx": "墨西哥", "mexico": "墨西哥", "mex": "墨西哥",
    "br": "巴西", "brazil": "巴西", "bra": "巴西",
}

REGION_ALIASES = {
    "eu": "欧盟",
    "欧盟": "欧盟",
    "europe": "欧盟",
    "欧洲": "欧盟",
    "americas": "美洲",
    "美洲": "美洲",
    "asia": "亚太",
    "亚太": "亚太",
    "亚洲": "亚太",
    "middle east": "中东",
    "中东": "中东",
}

EU_COUNTRIES = ["德国", "法国", "意大利", "西班牙", "荷兰", "比利时", "波兰", "瑞典", "奥地利",
    "爱尔兰", "葡萄牙", "希腊", "捷克", "罗马尼亚", "匈牙利", "丹麦", "芬兰",
    "保加利亚", "克罗地亚", "斯洛伐克", "立陶宛", "拉脱维亚", "斯洛文尼亚",
    "爱沙尼亚", "塞浦路斯", "卢森堡", "马耳他"]


# ═── Query Parser ═────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """Parse natural language query and extract intent + countries."""
    q = query.lower().strip()

    # Detect OSS/IOSS topic
    if any(k in q for k in ["oss", "ioss", "一站式", "one stop shop", "oss怎么报", "ioss是什么"]):
        return {"type": "oss_ioss", "countries": []}

    # Detect specific countries
    found_countries = []
    # Try Chinese names first
    for cn_name in TAX_DB:
        if cn_name in query:
            found_countries.append(cn_name)

    # Try aliases (word boundary matching to avoid "at" matching "vat")
    for alias, cn_name in ALIASES.items():
        pattern = rf'\b{re.escape(alias)}\b'
        if re.search(pattern, q) and cn_name not in found_countries:
            found_countries.append(cn_name)

    # Region queries
    for region_key, region_name in REGION_ALIASES.items():
        if region_key in q and region_name == "欧盟":
            found_countries = list(set(found_countries + EU_COUNTRIES))
            break

    # Detect intent type
    intent = "general"
    if any(k in q for k in ["注册门槛", "注册", "门槛", "threshold", "registration"]):
        intent = "threshold"
    elif any(k in q for k in ["申报周期", "申报", "截止", "deadline", "filing", "频率", "多久报"]):
        intent = "filing"
    elif any(k in q for k in ["税率", "vat", "gst", "rate", "税", "多少"]):
        intent = "rate"
    elif any(k in q for k in ["对比", "比较", "compare", "vs"]):
        intent = "compare"
    elif any(k in q for k in ["特殊规则", "特殊", "规则", "special"]):
        intent = "special"

    # Deduplicate
    found_countries = list(dict.fromkeys(found_countries))

    # If no countries found and not OSS, try fuzzy match
    if not found_countries and intent != "oss_ioss":
        # Check each character-level match
        pass

    return {"type": intent, "countries": found_countries}


# ═── HTML Report Generator ═─────────────────────────────────────

def get_rate_color(rate) -> str:
    """Map tax rate to color."""
    try:
        r = float(rate)
    except (ValueError, TypeError):
        return "#9E9E9E"  # gray for complex rates
    if r < 10:
        return "#4CAF50"  # green
    elif r < 20:
        return "#FFC107"  # yellow/amber
    elif r < 25:
        return "#FF9800"  # orange
    else:
        return "#F44336"  # red


def get_rate_bg(rate) -> str:
    """Map tax rate to background color."""
    try:
        r = float(rate)
    except (ValueError, TypeError):
        return "#F5F5F5"
    if r < 10:
        return "#E8F5E9"
    elif r < 20:
        return "#FFF8E1"
    elif r < 25:
        return "#FFF3E0"
    else:
        return "#FFEBEE"


def format_rate(rate) -> str:
    """Format rate for display."""
    if isinstance(rate, (int, float)):
        return f"{rate}%"
    return str(rate)


def generate_country_card(cn_name: str, data: dict) -> str:
    """Generate HTML card for a single country."""
    flag_map = {c: f"https://flagcdn.com/w40/{data['code'].lower()}.png" for c in [cn_name]}
    flags = {
        "DE": "🇩🇪", "FR": "🇫🇷", "IT": "🇮🇹", "ES": "🇪🇸", "NL": "🇳🇱",
        "BE": "🇧🇪", "PL": "🇵🇱", "SE": "🇸🇪", "AT": "🇦🇹", "IE": "🇮🇪",
        "PT": "🇵🇹", "GR": "🇬🇷", "CZ": "🇨🇿", "RO": "🇷🇴", "HU": "🇭🇺",
        "DK": "🇩🇰", "FI": "🇫🇮", "BG": "🇧🇬", "HR": "🇭🇷", "SK": "🇸🇰",
        "LT": "🇱🇹", "LV": "🇱🇻", "SI": "🇸🇮", "EE": "🇪🇪", "CY": "🇨🇾",
        "LU": "🇱🇺", "MT": "🇲🇹",
        "GB": "🇬🇧", "US": "🇺🇸", "CA": "🇨🇦", "JP": "🇯🇵", "AU": "🇦🇺",
        "SG": "🇸🇬", "NZ": "🇳🇿", "IN": "🇮🇳", "AE": "🇦🇪", "SA": "🇸🇦",
        "MX": "🇲🇽", "BR": "🇧🇷",
    }
    flag = flags.get(data.get("code", ""), "🏳️")

    rate = data.get("standard_rate", 0)
    rate_color = get_rate_color(rate)
    rate_bg = get_rate_bg(rate)
    rate_display = format_rate(rate)

    # Reduced rates string
    reduced = data.get("reduced_rates", [])
    reduced_str = ", ".join([f"{r}%" for r in reduced]) if reduced else "无"

    # Special rules
    special_html = ""
    if data.get("special_rules"):
        for rule in data["special_rules"]:
            alert_class = "alert-warn" if "⚠" in rule else "alert-info"
            special_html += f'<div class="rule-tag {alert_class}">{rule}</div>'

    notes = data.get("notes", "")
    notes_html = f'<div class="notes">{notes}</div>' if notes else ""

    oss_html = ""
    if data.get("oss_eligible"):
        oss_html = '<span class="badge badge-oss">OSS</span>'
    if data.get("ioss_eligible"):
        oss_html += '<span class="badge badge-ioss">IOSS</span>'

    return f"""
    <div class="country-card">
      <div class="card-header">
        <div class="country-flag">{flag}</div>
        <div>
          <div class="country-name">{cn_name} <span class="country-code">{data.get('code', '')}</span></div>
          <div class="country-tax-type">{data.get('tax_name_cn', '')} ({data.get('tax_type', '')})</div>
        </div>
        <div class="card-badges">{oss_html}</div>
      </div>
      <div class="rate-section" style="background:{rate_bg}; border-color:{rate_color}">
        <div class="rate-label">标准税率</div>
        <div class="rate-value" style="color:{rate_color}">{rate_display}</div>
        <div class="rate-reduced">减税率：{reduced_str}</div>
      </div>
      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">💰 货币</div>
          <div class="info-value">{data.get('currency', '')} ({data.get('currency_symbol', '')})</div>
        </div>
        <div class="info-item">
          <div class="info-label">📋 注册门槛</div>
          <div class="info-value">{data.get('registration_threshold', '—')}</div>
        </div>
        <div class="info-item">
          <div class="info-label">📅 申报频率</div>
          <div class="info-value">{data.get('filing_frequency', '—')}</div>
        </div>
        <div class="info-item">
          <div class="info-label">⏰ 截止日期</div>
          <div class="info-value">{data.get('filing_deadline', '—')}</div>
        </div>
      </div>
      {notes_html}
      <div class="special-rules">{special_html}</div>
    </div>"""


def generate_oss_section() -> str:
    """Generate EU OSS/IOSS knowledge section."""
    deadlines = OSS_IOSS_KNOWLEDGE["filing_deadlines"]
    schemes_html = ""
    for s in OSS_IOSS_KNOWLEDGE["schemes"]:
        schemes_html += f"""
        <tr>
          <td><strong>{s['name']}</strong></td>
          <td>{s['who']}</td>
          <td>{s['covers']}</td>
          <td>{s['filing']}</td>
          <td>{s['threshold']}</td>
          <td>{s['register_where']}</td>
        </tr>"""

    changes_html = ""
    for c in OSS_IOSS_KNOWLEDGE["key_changes"]:
        changes_html += f"""
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-date">{c['date']}</div>
            <div class="timeline-text">{c['event']}</div>
          </div>
        </div>"""

    notes_html = ""
    for n in OSS_IOSS_KNOWLEDGE["important_notes"]:
        notes_html += f'<div class="rule-tag alert-warn">{n}</div>'

    return f"""
    <div class="oss-section">
      <h2>🇪🇺 EU OSS/IOSS 一站式申报方案</h2>
      <p class="oss-intro">{OSS_IOSS_KNOWLEDGE['overview']['description']}</p>

      <h3>三种方案对比</h3>
      <div class="table-wrapper">
        <table class="oss-table">
          <thead>
            <tr><th>方案</th><th>适用对象</th><th>覆盖范围</th><th>申报频率</th><th>门槛</th><th>注册地</th></tr>
          </thead>
          <tbody>{schemes_html}</tbody>
        </table>
      </div>

      <h3>OSS季度申报截止日</h3>
      <div class="deadline-grid">
        <div class="deadline-card"><div>Q1</div><div>1-3月</div><div class="deadline-date">{deadlines['Q1']}</div></div>
        <div class="deadline-card"><div>Q2</div><div>4-6月</div><div class="deadline-date">{deadlines['Q2']}</div></div>
        <div class="deadline-card"><div>Q3</div><div>7-9月</div><div class="deadline-date">{deadlines['Q3']}</div></div>
        <div class="deadline-card"><div>Q4</div><div>10-12月</div><div class="deadline-date">{deadlines['Q4']}</div></div>
      </div>
      <p style="text-align:center;color:#64748B;font-size:13px;margin-top:4px;">IOSS月度申报截止日：{deadlines['IOSS_monthly']}</p>

      <h3>⚠ 重要提醒</h3>
      <div class="special-rules">{notes_html}</div>

      <h3>关键时间节点</h3>
      <div class="timeline">{changes_html}</div>
    </div>"""


def generate_compare_table(countries: list) -> str:
    """Generate comparison table for multiple countries."""
    rows = ""
    for cn_name in countries:
        d = TAX_DB[cn_name]
        rate = format_rate(d.get("standard_rate", ""))
        reduced = ", ".join([f"{r}%" for r in d.get("reduced_rates", [])]) or "—"
        rows += f"""
        <tr>
          <td><strong>{cn_name}</strong></td>
          <td class="rate-cell" style="color:{get_rate_color(d.get('standard_rate', 0))}; font-weight:700">{rate}</td>
          <td>{reduced}</td>
          <td>{d.get('filing_frequency', '—')}</td>
          <td>{d.get('filing_deadline', '—')}</td>
        </tr>"""

    return f"""
    <div class="compare-section">
      <h2>📊 多国税务对比表</h2>
      <div class="table-wrapper">
        <table class="compare-table">
          <thead>
            <tr><th>国家/地区</th><th>标准税率</th><th>减税率</th><th>申报频率</th><th>截止日</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>"""


def build_html(result: dict) -> str:
    """Build complete HTML report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    query_type = result.get("type", "general")
    countries = result.get("countries", [])
    query = result.get("query", "")

    title = f"跨境税务速查 · {query[:30]}"
    if not query:
        title = "跨境多国税务速查报告"

    body_sections = []
    oss_shown = False

    if query_type == "oss_ioss":
        body_sections.append(generate_oss_section())
        body_sections.append('<div class="quick-lookup"><h2>🔍 快速查税率</h2><p>输入国家名即可查：如「德国」「英国」「日本」</p></div>')
        oss_shown = True
    elif countries:
        if len(countries) >= 3:
            body_sections.append(generate_compare_table(countries))

        # Check if any EU country
        has_eu = any(c in EU_COUNTRIES for c in countries)
        if has_eu and not oss_shown:
            body_sections.append('<div class="oss-reminder"><p>💡 涉及欧盟国家，<a href="#oss">查看EU OSS一站式申报方案↓</a></p></div>')

        for cn_name in countries:
            body_sections.append(generate_country_card(cn_name, TAX_DB[cn_name]))

        if has_eu and len(countries) > 0:
            body_sections.insert(0, generate_oss_section())
            oss_shown = True
    else:
        body_sections.append("""
        <div class="no-result">
          <h2>🤔 未识别到具体国家</h2>
          <p>试试这样问：</p>
          <ul>
            <li>"德国VAT税率" → 查具体国家</li>
            <li>"欧盟OSS怎么报" → 了解OSS一站式方案</li>
            <li>"美国 英国 日本 对比" → 多国对比</li>
            <li>"德国 注册门槛" → 查注册要求</li>
          </ul>
          <div class="suggestions">
            <h3>热门查询</h3>
            <div class="tag-cloud">
              <span onclick="alert('试试输入：德国 VAT')" class="tag">🇩🇪 德国 19%</span>
              <span onclick="alert('试试输入：英国 税率')" class="tag">🇬🇧 英国 20%</span>
              <span onclick="alert('试试输入：美国 销售税')" class="tag">🇺🇸 美国 Sales Tax</span>
              <span onclick="alert('试试输入：日本 消费税')" class="tag">🇯🇵 日本 10%</span>
              <span onclick="alert('试试输入：欧盟OSS')" class="tag">🇪🇺 EU OSS</span>
              <span onclick="alert('试试输入：墨西哥 VAT')" class="tag">🇲🇽 墨西哥 16%</span>
              <span onclick="alert('试试输入：阿联酋 VAT')" class="tag">🇦🇪 阿联酋 5%</span>
              <span onclick="alert('试试输入：加拿大 GST')" class="tag">🇨🇦 加拿大 GST</span>
            </div>
          </div>
        </div>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #F0F4F8; color: #1A202C; line-height: 1.6; }}
.container {{ max-width: 960px; margin: 0 auto; padding: 20px; }}
.header {{ text-align: center; padding: 32px 20px 24px; background: linear-gradient(135deg, #1E3A5F 0%, #2D6A9F 100%); color: white; border-radius: 16px; margin-bottom: 24px; }}
.header h1 {{ font-size: 26px; margin-bottom: 8px; }}
.header p {{ font-size: 14px; opacity: 0.85; }}
.oss-section {{ background: white; border-radius: 14px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.oss-section h2 {{ font-size: 22px; margin-bottom: 12px; }}
.oss-section h3 {{ font-size: 17px; margin: 20px 0 12px; color: #1E3A5F; }}
.oss-intro {{ color: #64748B; margin-bottom: 16px; font-size: 14px; }}
.table-wrapper {{ overflow-x: auto; margin: 12px 0; }}
.oss-table, .compare-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.oss-table th, .compare-table th {{ background: #F1F5F9; padding: 10px 12px; text-align: left; font-weight: 600; color: #334155; white-space: nowrap; }}
.oss-table td, .compare-table td {{ padding: 10px 12px; border-bottom: 1px solid #E2E8F0; }}
.oss-table tr:hover td, .compare-table tr:hover td {{ background: #F8FAFC; }}
.deadline-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }}
.deadline-card {{ background: #F1F5F9; border-radius: 10px; padding: 16px; text-align: center; }}
.deadline-card div:first-child {{ font-weight: 700; color: #1E3A5F; font-size: 16px; }}
.deadline-card div:nth-child(2) {{ font-size: 12px; color: #64748B; }}
.deadline-date {{ color: #E53935; font-weight: 700; font-size: 14px; margin-top: 6px; }}
.timeline {{ position: relative; padding-left: 24px; margin: 12px 0; }}
.timeline::before {{ content: ""; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: #CBD5E1; }}
.timeline-item {{ display: flex; align-items: flex-start; margin-bottom: 14px; position: relative; }}
.timeline-dot {{ width: 10px; height: 10px; border-radius: 50%; background: #2D6A9F; flex-shrink: 0; margin-right: 14px; margin-top: 4px; z-index: 1; }}
.timeline-content {{ font-size: 13px; }}
.timeline-date {{ font-weight: 700; color: #2D6A9F; font-size: 12px; }}
.timeline-text {{ color: #334155; }}
.country-card {{ background: white; border-radius: 14px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.card-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }}
.country-flag {{ font-size: 32px; }}
.country-name {{ font-size: 20px; font-weight: 700; color: #1E3A5F; }}
.country-code {{ font-size: 12px; color: #94A3B8; font-weight: 400; background: #F1F5F9; padding: 2px 6px; border-radius: 4px; }}
.country-tax-type {{ font-size: 12px; color: #64748B; }}
.card-badges {{ margin-left: auto; display: flex; gap: 6px; }}
.badge {{ padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }}
.badge-oss {{ background: #E8F0FE; color: #1E6FD6; }}
.badge-ioss {{ background: #FCE4EC; color: #C62828; }}
.rate-section {{ padding: 16px; border-radius: 10px; border: 2px solid; text-align: center; margin-bottom: 16px; }}
.rate-label {{ font-size: 12px; color: #64748B; text-transform: uppercase; }}
.rate-value {{ font-size: 42px; font-weight: 800; }}
.rate-reduced {{ font-size: 13px; color: #64748B; margin-top: 4px; }}
.info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }}
.info-item {{ background: #F8FAFC; padding: 10px 12px; border-radius: 8px; }}
.info-label {{ font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 600; }}
.info-value {{ font-size: 13px; color: #334155; margin-top: 2px; }}
.notes {{ background: #FFF8E1; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #FFC107; margin-bottom: 12px; font-size: 13px; color: #5D4037; }}
.special-rules {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.rule-tag {{ padding: 6px 12px; border-radius: 6px; font-size: 12px; line-height: 1.4; }}
.alert-warn {{ background: #FFF3E0; border: 1px solid #FFB74D; color: #E65100; }}
.alert-info {{ background: #E3F2FD; border: 1px solid #90CAF9; color: #1565C0; }}
.compare-section {{ background: white; border-radius: 14px; padding: 28px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.compare-section h2 {{ font-size: 20px; margin-bottom: 16px; }}
.oss-reminder {{ background: #E8F0FE; padding: 14px 20px; border-radius: 10px; margin-bottom: 20px; font-size: 14px; }}
.oss-reminder a {{ color: #1E6FD6; font-weight: 600; }}
.no-result {{ background: white; border-radius: 14px; padding: 40px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.no-result h2 {{ margin-bottom: 12px; }}
.no-result ul {{ text-align: left; display: inline-block; margin: 12px auto; color: #64748B; font-size: 14px; }}
.no-result li {{ margin-bottom: 6px; }}
.tag-cloud {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 12px; }}
.tag {{ background: #F1F5F9; padding: 8px 16px; border-radius: 20px; font-size: 13px; cursor: pointer; border: 1px solid #E2E8F0; transition: all 0.2s; }}
.tag:hover {{ background: #E8F0FE; border-color: #90CAF9; }}
.footer {{ text-align: center; padding: 24px; color: #94A3B8; font-size: 12px; }}
.quick-lookup {{ background: white; border-radius: 14px; padding: 28px; margin-bottom: 24px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
.rate-cell {{ font-size: 18px; }}
@media (max-width: 640px) {{
  .deadline-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .info-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🌍 跨境多国税务速查</h1>
    <p>查询时间: {now} · 数据来源: 各国税务局/欧盟委员会/2026年公开数据</p>
  </div>
  {"".join(body_sections)}
  <div class="footer">
    <p>⚠ 免责声明：本报告仅供参考，不构成税务/法律建议。税率和规则可能随时变化，请以各国官方税务局最新公告为准。</p>
    <p style="margin-top: 8px;">Cross-Border Tax Quick Lookup v1.0 · Powered by WorkBuddy</p>
  </div>
</div>
</body>
</html>"""

    return html


# ═── Main ═───────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("""跨境多国税务速查 v1.0
Usage:
  python cross_border_tax.py "<查询内容>"
  python cross_border_tax.py --list   列出所有支持国家
  python cross_border_tax.py --oss    查看EU OSS详细方案
""")
        return

    query = sys.argv[1]

    if query == "--list":
        print("支持的国家/地区 (按区域):\n")
        print("🇪🇺 欧盟27国:")
        for c in EU_COUNTRIES:
            d = TAX_DB[c]
            print(f"  {c:6s} {d['code']:3s}  {format_rate(d['standard_rate']):>6s}  {d['currency_symbol']}")
        print("\n🇬🇧 欧洲其他: 英国 (GB) 20% £")
        print("🇺🇸 北美: 美国 (US) 各州不同 $ | 加拿大 (CA) 5%+省税 C$")
        print("🌏 亚太: 日本 (JP) 10% ¥ | 澳大利亚 (AU) 10% A$ | 新加坡 (SG) 9% S$ | 新西兰 (NZ) 15% NZ$ | 印度 (IN) 18% ₹")
        print("🇸🇦 中东: 阿联酋 (AE) 5% د.إ | 沙特阿拉伯 (SA) 15% ر.س")
        print("🌎 拉美: 墨西哥 (MX) 16% Mex$ | 巴西 (BR) ~18% R$")
        return

    if query == "--oss":
        result = {"type": "oss_ioss", "countries": [], "query": "EU OSS/IOSS"}
        html = build_html(result)
        output_path = os.path.expanduser("~/.workbuddy/skills/cross-border-tax/output/eu_oss_report.html")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"EU OSS/IOSS报告已生成: {output_path}")
        return

    # Parse query
    result = parse_query(query)
    result["query"] = query
    countries = result["countries"]

    if result["type"] != "oss_ioss" and not countries:
        # If no countries found but query has OSS keywords
        if any(k in query.lower() for k in ["oss", "ioss", "一站式"]):
            result["type"] = "oss_ioss"

    # Generate HTML
    html = build_html(result)

    # Write to output
    output_dir = os.path.expanduser("~/.workbuddy/skills/cross-border-tax/output")
    os.makedirs(output_dir, exist_ok=True)
    safe_name = re.sub(r'[^\w\-]', '_', query)[:40] or "tax_report"
    output_path = os.path.join(output_dir, f"{safe_name}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 税务速查报告已生成: {output_path}")
    if countries:
        print(f"📍 已查询: {', '.join(countries)}")
    if result["type"] == "oss_ioss":
        print("📋 已包含EU OSS/IOSS一站式申报方案")


if __name__ == "__main__":
    main()
