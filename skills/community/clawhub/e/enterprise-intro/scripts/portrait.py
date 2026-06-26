#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合画像一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base import call_api, debug_print


# ============ 映射表 ============

MODULE_NAME_MAPPING = {
    'attribute_profile': '属性画像',
    'industry': '国民经济行业',
    'scale_classification': '规模划型',
    'tech_qual_list': '科技型企业认证',
    'strategic_emerging': '战略新兴产业认定',
    'green_entiden_list': '绿色产业认定',
    'green_qual_list': '绿色资质认证',
    'rual_entiden_list': '乡村振兴企业认定',
    'fourup_ent': '四上企业认定',
    'address_qual_list': '地址属性',
    'operate_profile': '经营画像',
    'compintro': '企业官网简介',
    'product_service_list': '产品服务',
    'merchant_qual_list': '产业链',
    'tax_qual': '税务属性',
    'financial_index_list': '财务指标',
    'listing_qual': '上市属性',
    'credit_review_list': '信用评价',
    'qual_honor': '资质荣誉统计',
    'main_business_qual_list': '主营业务资质',
    'board_list': '榜单',
    'honor_rewards_list': '荣誉奖励'
}

# 码值转换映射表
EMPLOYEE_MAPPING = {
    0: "值为0时", 1: "(0~10]", 2: "(10~100]", 3: "(100~200]",
    4: "(200~300]", 5: "(300~400]", 6: "(400~500]", 7: "(500~600]",
    8: "(600~700]", 9: "(700~800]", 10: "(800~900]", 11: "(900~1000]",
    12: "(1000~5000]", 13: "(5000~10000]", 14: "(10000~40000]",
    15: "(40000~80000]", 16: "(80000~120000]", 17: "(120000~160000]",
    18: "(160000~200000]", 19: "(200000以上]", 999: "值为空"
}

VENDINC_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~100万]",
    6: "(100万~500万]", 7: "(500万~1000万]", 8: "(1000万~5000万]",
    9: "(5000万~1亿]", 10: "(1亿~5亿]", 11: "(5亿~10亿]",
    12: "(10亿~20亿]", 13: "(20亿~30亿]", 14: "(30亿~40亿]",
    15: "(40亿~50亿]", 16: "(50亿以上]", 999: "值为空"
}

ASSGRO_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~10万]",
    6: "(10万~50万]", 7: "(50万~100万]", 8: "(100万~500万]",
    9: "(500万~1000万]", 10: "(1000万~5000万]", 11: "(5000万~1亿]",
    12: "(1亿~5亿]", 13: "(5亿~10亿]", 14: "(10亿~20亿]",
    15: "(20亿~30亿]", 16: "(30亿~40亿]", 17: "(40亿~50亿]",
    18: "(50亿以上]", 999: "值为空"
}

RATGRO_MAPPING = {
    0: "值为0", 1: "(0~1万元]", 2: "(1万~10万]", 3: "(10万~50万]",
    4: "(50万~100万]", 5: "(100万~500万]", 6: "(500万~1000万]",
    7: "(1000万以上]", 999: "值为空"
}

PROGRO_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~1万]",
    6: "(1万~50万]", 7: "(50万~100万]", 8: "(100万~500万]",
    9: "(500万~1000万]", 10: "(1000万~5000万]", 11: "(5000万~1亿]",
    12: "(1亿~5亿]", 13: "(5亿~10亿]", 14: "(10亿~50亿]",
    15: "(50亿以上]", 999: "值为空"
}

NETINC_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~10万]",
    6: "(10万~50万]", 7: "(50万~100万]", 8: "(100万~500万]",
    9: "(500万~1000万]", 10: "(1000万~5000万]", 11: "(5000万~1亿]",
    12: "(1亿~5亿]", 13: "(5亿~10亿]", 14: "(10亿~50亿]",
    15: "(50亿以上]", 999: "值为空"
}

LIAGRO_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~50万]",
    6: "(50万~100万]", 7: "(100万~500万]", 8: "(500万~1000万]",
    9: "(1000万~5000万]", 10: "(5000万~1亿]", 11: "(1亿~10亿]",
    12: "(10亿~50亿]", 13: "(50亿以上]", 999: "值为空"
}

TOTEQU_MAPPING = {
    0: "值为0", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~50万]",
    6: "(50万~100万]", 7: "(100万~500万]", 8: "(500万~1000万]",
    9: "(1000万~5000万]", 10: "(5000万~1亿]", 11: "(1亿~10亿]",
    12: "(10亿~50亿]", 13: "(50亿以上]", 999: "值为空"
}

MAIBUSINC_MAPPING = {
    0: "值为0时", 1: "(负5000万以下]", 2: "(负5000万~负1000万]",
    3: "(负1000万~负100万]", 4: "(负100万~小于0]", 5: "(0~50万]",
    6: "(50万~100万]", 7: "(100万~500万]", 8: "(500万~1000万]",
    9: "(1000万~5000万]", 10: "(5000万~1亿]", 11: "(1亿~5亿]",
    12: "(5亿~10亿]", 13: "(10亿以上]", 999: "值为空"
}

FIELD_MAPPINGS = {
    'employee': EMPLOYEE_MAPPING,
    'vendinc': VENDINC_MAPPING,
    'assgro': ASSGRO_MAPPING,
    'ratgro': RATGRO_MAPPING,
    'progro': PROGRO_MAPPING,
    'netinc': NETINC_MAPPING,
    'liagro': LIAGRO_MAPPING,
    'totequ': TOTEQU_MAPPING,
    'maibusinc': MAIBUSINC_MAPPING
}


# ============ 辅助函数 ============

def _safe_get(data: Any, key: str, default: Any = None) -> Any:
    """安全获取字典值"""
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def _convert_code_to_interval(code_value: Any, field_type: str = None) -> str:
    """将码值转换为区间值"""
    if code_value is None or code_value == '':
        return ""

    try:
        code_int = int(str(code_value))
    except (ValueError, TypeError):
        return str(code_value)

    if field_type and field_type in FIELD_MAPPINGS:
        mapping = FIELD_MAPPINGS[field_type]
        if code_int in mapping:
            return mapping[code_int]
    else:
        for mapping in FIELD_MAPPINGS.values():
            if code_int in mapping:
                return mapping[code_int]

    return str(code_value)


def _add_percentage_unit(value: Any) -> str:
    """为比率类指标添加百分号单位"""
    if not value or value == '':
        return ""
    if '%' in str(value):
        return str(value)
    return f"{value}%"


def _is_listed_company(data: Dict) -> bool:
    """判断是否为上市公司"""
    try:
        operate_profile = data.get('data', {}).get('operate_profile', {})
        listing_qual = operate_profile.get('listing_qual', {})
        listing_type = listing_qual.get('listing_type')
        if listing_type and str(listing_type).strip():
            return True
        return False
    except:
        return False


# ============ API 数据处理 ============

def _process_attribute_profile(attribute_profile: Dict) -> Dict[str, Any]:
    """处理属性画像模块"""
    if not attribute_profile or not isinstance(attribute_profile, dict):
        attribute_profile = {}

    result = {}

    # 属性画像基础信息
    attribute_basic = {}
    market_type = _safe_get(attribute_profile, 'market_type')
    if market_type:
        if isinstance(market_type, dict) and market_type.get('market_typename'):
            attribute_basic['主体类型名称'] = market_type['market_typename']
        elif isinstance(market_type, str):
            attribute_basic['主体类型名称'] = market_type
        else:
            attribute_basic['主体类型名称'] = ""
    else:
        attribute_basic['主体类型名称'] = ""

    attribute_basic['企业分类'] = _safe_get(attribute_profile, 'ent_classification') or _safe_get(attribute_profile, 'ent_class') or ""
    attribute_basic['经济成分'] = _safe_get(attribute_profile, 'economic_sector') or ""
    attribute_basic['国民经济部门'] = _safe_get(attribute_profile, 'neconomic_org') or ""
    result['属性画像'] = attribute_basic

    # 国民经济行业
    industry = _safe_get(attribute_profile, 'industry', {})
    if isinstance(industry, dict):
        result['国民经济行业'] = {
            '行业门类': industry.get('industryphy_name', ''),
            '行业大类': industry.get('industrybig_name', ''),
            '行业中类': industry.get('industrymid_name', ''),
            '行业小类': industry.get('industrysmall_name', '')
        }
    else:
        result['国民经济行业'] = {'行业门类': '', '行业大类': '', '行业中类': '', '行业小类': ''}

    # 规模划型
    scale_classification = _safe_get(attribute_profile, 'scale_classification', [])
    scale_data = scale_classification[0] if isinstance(scale_classification, list) and scale_classification else (scale_classification if isinstance(scale_classification, dict) else {})
    result['规模划型'] = {
        '企业规模（2011版）': scale_data.get('ent_scale_old', ''),
        '企业规模识别年份': scale_data.get('ent_scale_idyear', ''),
        '是否纳入小微企业目录': '是' if scale_data.get('is_xwqy_gsxt') == '是' else '否',
        '是否是分支机构': scale_data.get('is_branch', '')
    }

    # 科技型企业认证
    tech_qual_list = _safe_get(attribute_profile, 'tech_qual_list', [])
    processed_tech_list = []
    if isinstance(tech_qual_list, list):
        for item in tech_qual_list:
            if isinstance(item, dict):
                tech_item = {}
                field_mapping = {
                    'idenname': '认证名称', 'identype': '认证类型', 'leadpro': '主导产品',
                    'idenlevel': '认证级别', 'idenyear': '认证年份', 'idenorg': '认定机构',
                    'idenprovince': '认定省份', 'idencity': '认定城市', 'public_date': '发布日期',
                    'certstart': '有效期起', 'certend': '有效期至', 'hcldate': '撤销日期'
                }
                for eng, chn in field_mapping.items():
                    if item.get(eng):
                        tech_item[chn] = item[eng]
                if tech_item:
                    processed_tech_list.append(tech_item)
    result['科技型企业认证'] = processed_tech_list

    # 战略新兴产业认定
    strategic_emerging = _safe_get(attribute_profile, 'strategic_emerging', {})
    result['战略新兴产业认定'] = {
        '战略新兴产业名称': strategic_emerging.get('industry_name', '') if isinstance(strategic_emerging, dict) else ''
    }

    # 绿色产业认定
    green_ent = _safe_get(attribute_profile, 'green_ent', {})
    processed_green = []
    if isinstance(green_ent, dict):
        green_entiden_list = green_ent.get('green_entiden_list', [])
        if isinstance(green_entiden_list, list):
            for item in green_entiden_list:
                if isinstance(item, dict):
                    green_item = {}
                    for key in ['gigc_level1', 'gigc_level2', 'gigc_level3']:
                        if item.get(key):
                            chn_key = key.replace('gigc_level1', '绿色产业指导目录一级').replace('gigc_level2', '绿色产业指导目录二级').replace('gigc_level3', '绿色产业指导目录三级')
                            green_item[chn_key] = item[key]
                    if green_item:
                        processed_green.append(green_item)
    result['绿色产业认定'] = processed_green

    return result


def _process_operate_profile(operate_profile: Dict, is_listed: bool) -> Dict[str, Any]:
    """处理经营画像模块"""
    if not operate_profile or not isinstance(operate_profile, dict):
        operate_profile = {}

    result = {}

    # 企业官网简介
    compintro = _safe_get(operate_profile, 'compintro', {})
    try:
        import json
        json_str = compintro.replace('\n', '').replace('      ⋮ ', '')
        data_dict = json.loads(json_str)
        result['企业官网简介'] = data_dict.get('public_intro', '')
    except:
        result['企业官网简介'] = ""

    # 产品服务
    product_service_list = _safe_get(operate_profile, 'product_service_list', [])
    processed_product_list = []
    if isinstance(product_service_list, list):
        for item in product_service_list:
            if isinstance(item, dict):
                product_item = {}
                if item.get('ps_name'):
                    product_item['产品名称'] = item['ps_name']
                if item.get('ps_class'):
                    product_item['产品服务分类'] = item['ps_class']
                if product_item:
                    processed_product_list.append(product_item)
    result['产品服务'] = processed_product_list

    # 产业链
    merchant_qual_list = _safe_get(operate_profile, 'merchant_qual_list', [])
    processed_merchant_list = []
    if isinstance(merchant_qual_list, list):
        for item in merchant_qual_list:
            if isinstance(item, dict):
                merchant_item = {}
                if item.get('industry_chain_name'):
                    merchant_item['产业链名称'] = item['industry_chain_name']
                if item.get('industrial_links'):
                    merchant_item['产业环节'] = item['industrial_links']
                if item.get('industrial_nodes'):
                    merchant_item['产业节点'] = item['industrial_nodes']
                if merchant_item:
                    processed_merchant_list.append(merchant_item)
    result['产业链'] = processed_merchant_list

    # 上市属性
    listing_qual = _safe_get(operate_profile, 'listing_qual', {})
    listing_result = {
        '上市辅导阶段': '', '拟IPO板块': '', '拟IPO阶段': '',
        '拟IPO结果': '', '交易市场': '', '上市类型': '', '是否H股公司': ''
    }
    if isinstance(listing_qual, dict):
        field_mapping = {
            'listing_coaching_stage': '上市辅导阶段',
            'pro_ipo_sector': '拟IPO板块',
            'pro_ipo_stage': '拟IPO阶段',
            'pro_ipo_results': '拟IPO结果',
            'trading_market': '交易市场',
            'listing_type': '上市类型',
            'is_hshare': '是否H股公司'
        }
        for eng, chn in field_mapping.items():
            listing_result[chn] = listing_qual.get(eng, '')
    result['上市属性'] = listing_result

    # 信用评价
    credit_review_list = _safe_get(operate_profile, 'credit_review_list', [])
    processed_credit_list = []
    if isinstance(credit_review_list, list):
        for item in credit_review_list:
            if isinstance(item, dict):
                credit_item = {}
                field_mapping = {
                    'eval_type': '评价类型', 'eval_year': '评价年度',
                    'eval_field': '参评领域', 'credit_level': '信用等级',
                    'eval_date': '评价日期', 'certend': '有效期至', 'idenorg': '评价机构'
                }
                for eng, chn in field_mapping.items():
                    if item.get(eng):
                        credit_item[chn] = item[eng]
                if credit_item:
                    processed_credit_list.append(credit_item)
    result['信用评价'] = processed_credit_list

    return result


def _process_qual_honor(qual_honor: Dict) -> Dict[str, Any]:
    """处理资质荣誉模块"""
    if not qual_honor or not isinstance(qual_honor, dict):
        qual_honor = {}

    result = {}

    # 资质荣誉统计
    result['资质荣誉统计'] = {
        '主营业务资质统计数量': qual_honor.get('main_business_qual_count', ''),
        '榜单统计数量': qual_honor.get('board_count', ''),
        '荣誉奖励数量': qual_honor.get('honorary_rewards_count', '')
    }

    # 主营业务资质
    main_business_qual_list = _safe_get(qual_honor, 'main_business_qual_list', [])
    processed_business_list = []
    if isinstance(main_business_qual_list, list):
        for item in main_business_qual_list:
            if isinstance(item, dict):
                business_item = {}
                field_mapping = {
                    'cert_project': '认证项目', 'cert_org': '发证机构',
                    'award_year': '认证年份', 'award_date': '发证日期',
                    'end_date': '截止日期', 'type_name': '证书类型名称'
                }
                for eng, chn in field_mapping.items():
                    if item.get(eng):
                        business_item[chn] = item[eng]
                if business_item:
                    processed_business_list.append(business_item)
    result['主营业务资质'] = processed_business_list

    # 榜单
    board_list = _safe_get(qual_honor, 'board_list', [])
    processed_board_list = []
    if isinstance(board_list, list):
        for item in board_list:
            if isinstance(item, dict):
                board_item = {}
                field_mapping = {
                    'board_name': '榜单名称', 'board_year': '榜单年份',
                    'publish_date': '发布日期', 'publish_unit': '发布单位'
                }
                for eng, chn in field_mapping.items():
                    if item.get(eng):
                        board_item[chn] = item[eng]
                if board_item:
                    processed_board_list.append(board_item)
    result['榜单'] = processed_board_list

    # 荣誉奖励
    honor_rewards_list = _safe_get(qual_honor, 'honor_rewards_list', [])
    processed_honor_list = []
    if isinstance(honor_rewards_list, list):
        for item in honor_rewards_list:
            if isinstance(item, dict):
                honor_item = {}
                field_mapping = {
                    'identype': '认证类型', 'proname': '产品名称',
                    'centerlabname': '中心或实验室名称', 'idenname': '认证名称',
                    'idenyear': '认证年份', 'batch': '批次',
                    'idenorg': '公告(认定)机构', 'level': '级别',
                    'province': '发布省份', 'city': '发布城市',
                    'pubdate': '发布日期', 'certstart': '有效期起',
                    'certend': '有效期至', 'hcldate': '撤销日期'
                }
                for eng, chn in field_mapping.items():
                    if item.get(eng):
                        honor_item[chn] = item[eng]
                if honor_item:
                    processed_honor_list.append(honor_item)
    result['荣誉奖励'] = processed_honor_list

    return result


# ============ API 调用 ============

def _call_portrait_api(entname: str) -> Dict[str, Any]:
    """调用企业综合画像 API"""
    response = call_api('/integrated/portrayal/entinfo', {'entname': entname}, method='GET')
    return response


def _fetch_portrait_data(entname: str) -> Optional[Dict[str, Any]]:
    """获取并处理画像数据"""
    response = _call_portrait_api(entname)

    if response.get('code') != 200:
        return None

    raw_data = response.get('data', {})
    if not raw_data:
        return None

    is_listed = _is_listed_company(response)

    processed_data = {}

    # 处理属性画像
    attribute_profile = raw_data.get('attribute_profile', {})
    if attribute_profile:
        processed_data.update(_process_attribute_profile(attribute_profile))

    # 处理经营画像
    operate_profile = raw_data.get('operate_profile', {})
    if operate_profile:
        processed_data.update(_process_operate_profile(operate_profile, is_listed))

    # 处理资质荣誉
    qual_honor = raw_data.get('qual_honor', {})
    if qual_honor:
        processed_data.update(_process_qual_honor(qual_honor))

    return processed_data


# ============ Markdown 格式化 ============

def _extract_enterprise_overview(portrait: Dict, labels: Dict = None) -> str:
    """提取企业概要"""
    if labels is None:
        labels = {}

    lines = ["### 企业概要"]

    # 核心身份定性
    attr = portrait.get('属性画像', {})
    scale = portrait.get('规模划型', {})
    industry = portrait.get('国民经济行业', {})

    subject_type = attr.get('主体类型名称', '')
    enterprise_scale = scale.get('企业规模（2011版）', '')
    industry_category = industry.get('行业门类', '')

    parts = []
    if subject_type:
        parts.append(subject_type)
    if enterprise_scale:
        parts.append(enterprise_scale)
    if industry_category:
        parts.append(f"{industry_category}企业")

    if parts:
        lines.append(f"核心身份定性：{''.join(parts)}")

    # 行业定位
    ind_category = industry.get('行业门类', '')
    ind_class = industry.get('行业大类', '')
    ind_subclass = industry.get('行业中类', '')
    if ind_category and ind_class:
        industry_path = f"{ind_category}>{ind_class}"
        if ind_subclass:
            industry_path += f">{ind_subclass}"
        lines.append(f"行业定位：{industry_path}")

    # 上市状态
    listing = portrait.get('上市属性', {})
    listing_type = listing.get('上市类型', '')
    trading_market = listing.get('交易市场', '')
    if listing_type:
        status_parts = [listing_type]
        if trading_market:
            status_parts.append(trading_market)
        lines.append(f"上市状态：{'，'.join([p for p in status_parts if p])}")

    # 科技属性
    certifications = portrait.get('科技型企业认证', [])
    if certifications:
        seen = set()
        top_certs = []
        for cert in certifications[:5]:
            cert_name = cert.get('认证名称', '')
            cert_level = cert.get('认证级别', '')
            if cert_name and cert_name not in seen:
                seen.add(cert_name)
                if cert_level:
                    top_certs.append(f"{cert_name}（{cert_level}）")
                else:
                    top_certs.append(cert_name)
                if len(top_certs) >= 3:
                    break
        if top_certs:
            lines.append(f"科技属性：{'，'.join(top_certs)}")

    return '\n'.join(lines)


def _extract_main_business(portrait: Dict) -> str:
    """提取主营业务"""
    lines = ["### 主营业务"]

    # 业务范围 - 从产品服务获取
    products = portrait.get('产品服务', [])
    if products:
        product_names = [p.get('产品名称', '') for p in products if p.get('产品名称')]
        if product_names:
            lines.append(f"业务范围：{'，'.join(product_names[:10])}")
    else:
        intro = portrait.get('企业官网简介', '')
        if intro:
            lines.append(f"业务范围：{intro[:200]}")

    # 产业链定位
    chain = portrait.get('产业链', [])
    if chain:
        chain_names = [c.get('产业链名称', '') for c in chain if c.get('产业链名称')]
        if chain_names:
            lines.append(f"产业链定位：{'，'.join(chain_names[:5])}")
    else:
        lines.append("产业链定位：未明确上游/中游/下游")

    # 核心技术资质
    qualifications = portrait.get('主营业务资质', [])
    if qualifications:
        qual_strs = []
        for qual in qualifications[:5]:
            qual_name = qual.get('认证项目', '') or qual.get('资质名称', '')
            qual_org = qual.get('发证机构', '') or qual.get('发证机关', '')
            if qual_name:
                if qual_org:
                    qual_strs.append(f"{qual_name}（{qual_org}）")
                else:
                    qual_strs.append(qual_name)
        if qual_strs:
            lines.append(f"核心技术资质：{'，'.join(qual_strs)}")

    return '\n'.join(lines)


def _extract_market_competitiveness(portrait: Dict) -> str:
    """提取市场竞争力"""
    lines = ["### 市场竞争力"]

    # 榜单信息
    rankings = portrait.get('榜单', [])
    if rankings:
        important_rankings = []
        for r in rankings[:5]:
            ranking_name = r.get('榜单名称', '')
            ranking_year = r.get('榜单年份', '')
            if ranking_name:
                if ranking_year:
                    important_rankings.append(f"{ranking_year}年{ranking_name}")
                else:
                    important_rankings.append(ranking_name)
        if important_rankings:
            lines.append(f"行业地位：{'，'.join(important_rankings[:3])}")

    # 信用评价
    credit_reviews = portrait.get('信用评价', [])
    if credit_reviews:
        credit_strs = []
        for credit in credit_reviews[:3]:
            eval_type = credit.get('评价类型', '')
            credit_level = credit.get('信用等级', '')
            if eval_type and credit_level:
                credit_strs.append(f"{eval_type}：{credit_level}")
        if credit_strs:
            lines.append(f"质量与声誉：{'，'.join(credit_strs)}")

    return '\n'.join(lines)


def _extract_brand_influence(portrait: Dict) -> str:
    """提取品牌影响力"""
    lines = ["### 品牌影响力"]

    # 荣誉奖励
    honors = portrait.get('荣誉奖励', [])
    if honors:
        honor_strs = []
        for honor in honors[:5]:
            honor_name = honor.get('认证名称', '')
            honor_year = honor.get('认证年份', '')
            if honor_name:
                if honor_year:
                    honor_strs.append(f"{honor_year}年{honor_name}")
                else:
                    honor_strs.append(honor_name)
        if honor_strs:
            lines.append(f"荣誉背书：{'，'.join(honor_strs)}")

    # 榜单
    rankings = portrait.get('榜单', [])
    if rankings:
        ranking_strs = []
        for r in rankings[:3]:
            board_name = r.get('榜单名称', '')
            board_year = r.get('榜单年份', '')
            if board_name:
                if board_year:
                    ranking_strs.append(f"{board_year}年{board_name}")
                else:
                    ranking_strs.append(board_name)
        if ranking_strs:
            lines.append(f"榜单荣誉：{'，'.join(ranking_strs)}")

    return '\n'.join(lines)


def _extract_value_growth(portrait: Dict) -> str:
    """提取价值与成长"""
    lines = ["### 价值与成长"]

    # 政策契合度
    strategic = portrait.get('战略新兴产业认定', {})
    green = portrait.get('绿色产业认定', [])

    strategic_name = strategic.get('战略新兴产业名称', '') if isinstance(strategic, dict) else ''
    green_name = green[0].get('绿色产业指导目录一级', '') if isinstance(green, list) and len(green) > 0 else ''

    parts = []
    if strategic_name:
        parts.append(f"战略新兴产业：{strategic_name}")
    if green_name:
        parts.append(f"绿色产业：{green_name}")

    if parts:
        lines.append(f"政策契合度：{'、'.join(parts)}")
    else:
        lines.append("政策契合度：未明确所属的战略新兴产业或绿色产业")

    # 科技认证
    tech_certs = portrait.get('科技型企业认证', [])
    if tech_certs:
        cert_years = [c.get('认证年份', '') for c in tech_certs if c.get('认证年份')]
        if cert_years:
            lines.append(f"科技认证历程：{'、'.join(cert_years[:5])}")

    return '\n'.join(lines)


def _extract_enterprise_association(portrait: Dict) -> str:
    """提取企业关联分析"""
    lines = ["### 企业关联分析"]

    # 是否分支机构
    scale = portrait.get('规模划型', {})
    is_branch = scale.get('是否是分支机构', '')
    if is_branch == '是':
        lines.append("集团关联：为分支机构")
    else:
        lines.append("集团关联：非分支机构")

    # 产业链关联
    chain = portrait.get('产业链', [])
    if chain:
        chain_info = []
        for c in chain[:3]:
            chain_name = c.get('产业链名称', '')
            chain_link = c.get('产业环节', '')
            if chain_name:
                if chain_link:
                    chain_info.append(f"{chain_name}（{chain_link}）")
                else:
                    chain_info.append(chain_name)
        if chain_info:
            lines.append(f"产业链关联：{'，'.join(chain_info)}")

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    if not data:
        return "# 企业综合画像\n\n暂无综合画像数据"

    sections = ["# 企业综合画像提炼"]

    # 企业概要
    overview = _extract_enterprise_overview(data)
    if overview:
        sections.append("")
        sections.append(overview)

    # 主营业务
    business = _extract_main_business(data)
    if business:
        sections.append("")
        sections.append(business)

    # 市场竞争力
    competitiveness = _extract_market_competitiveness(data)
    if competitiveness:
        sections.append("")
        sections.append(competitiveness)

    # 品牌影响力
    brand = _extract_brand_influence(data)
    if brand:
        sections.append("")
        sections.append(brand)

    # 价值与成长
    value = _extract_value_growth(data)
    if value:
        sections.append("")
        sections.append(value)

    # 企业关联分析
    association = _extract_enterprise_association(data)
    if association:
        sections.append("")
        sections.append(association)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业综合画像信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的综合画像信息
    """
    # 1. 获取画像数据
    data = _fetch_portrait_data(entname)

    if not data:
        return "# 企业综合画像\n\n未查询到企业综合画像信息"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s16_portrait <企业名称>")
