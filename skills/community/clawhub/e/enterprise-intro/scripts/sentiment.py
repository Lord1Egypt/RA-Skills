#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舆情信息一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base import call_api, debug_print


# ============ 映射表 ============

def _get_news_class_mapping() -> Dict[str, str]:
    """新闻分类码值转换为中文"""
    return {
        "A01001": "信贷债务违约",
        "A01002": "信用评级负面信息",
        "A01003": "制假售假、虚假宣传",
        "A01004": "违背约定",
        "A01005": "移用资金",
        "A01006": "逃避债务",
        "A01007": "信贷债务展期",
        "A01008": "改变资金用途",
        "A01009": "偷税漏税",
        "A01010": "虚假融资",
        "A01011": "列入经营异常、严重违法",
        "A01012": "其他企业信用信息",
        "A01013": "提前兑付",
        "A01014": "兑付存在不确定性",
        "A01015": "信用评级上调",
        "A01016": "信用评级信息",
        "A01017": "授信信息",
        "A01018": "付息兑付",
        "B01001": "暂停交易/上市、推迟/取消发行",
        "B01002": "股权质押、冻结、拍卖",
        "B01003": "限售股份解禁、股份减持",
        "B01004": "股价波动",
        "B01005": "做空股价",
        "B01006": "其他市场交易信息",
        "B01007": "停复牌",
        "B01008": "股票戴帽",
        "B01009": "退市风险",
        "B01010": "承诺不减持",
        "B01011": "股份增持",
        "B01012": "股份回购",
        "B01013": "投资融资",
        "B01014": "发行上市",
        "B01015": "机构调研",
        "B01016": "大宗交易",
        "B01017": "摘星摘帽",
        "B01018": "恢复上市",
        "B01019": "对赌",
        "B01020": "股权转让",
        "C01001": "发生业绩亏损/主要财务指标下降",
        "C01002": "盈利能力降低",
        "C01003": "资金回收异常/资金周转等流动性风险",
        "C01004": "资产负债率过高/资不抵债",
        "C01005": "资产重大减值/资产异常",
        "C01006": "财务造假",
        "C01007": "放弃债权和财产",
        "C01008": "对外借款或对外担保过多,存在代偿风险",
        "C01009": "财务管理混乱",
        "C01010": "账目记录差错、会计差错更正、会计估计变更",
        "C01011": "注册会计师出具非无保留意见的审计报告",
        "C01012": "频繁更换会计师事务所",
        "C01013": "其他财务预警",
        "C01014": "财务向好",
        "C01015": "利润分配",
        "C01016": "政府补贴",
        "C01017": "理财",
        "D01001": "重组失败/取消或重组存在问题",
        "D01002": "经营业务发生重大变化",
        "D01003": "投资决策失误",
        "D01004": "虚假注资/抽逃资金/转移资产",
        "D01005": "经营活动/环境发生变化",
        "D01006": "公司资产被查封、扣押、冻结、司法划转",
        "D01007": "市场竞争力下降、市场份额下滑",
        "D01008": "破产清算",
        "D01009": "关联方（实际控制人、控股股东、供应商、客户、被担保企业、其他关联企业）出现问题",
        "D01010": "法律诉讼",
        "D01011": "产品缺陷问题",
        "D01012": "审批不通过事项或撤销公司某项经营许可",
        "D01013": "犯罪事件",
        "D01014": "公司违规或被问询",
        "D01015": "停工停产",
        "D01016": "偷排偷放废气（水）",
        "D01017": "与合作方企业订单减少、中断合作、丧失特许经营权",
        "D01018": "出售、变卖公司主要经营性资产",
        "D01019": "主业不突出、盲目扩张",
        "D01020": "环保不达标",
        "D01021": "安全生产条件不达标",
        "D01022": "其他生产经营条件不符合政策要求",
        "D01023": "企业、实际控制人或关联方涉及民间借贷",
        "D01024": "出现拖欠税费、电费、水费等欠款",
        "D01025": "其他经营预警",
        "D01026": "拖欠供应商货款",
        "D01027": "生产要素成本上升",
        "D01028": "安全生产事故",
        "D01029": "减资、合并、分立",
        "D01030": "债务重组存在问题",
        "D01031": "无证施工",
        "D01032": "垄断",
        "D01033": "客户投诉",
        "D01034": "重要合作",
        "D01035": "招投标信息",
        "D01036": "重大合同",
        "D01037": "生产投产",
        "D01038": "资质牌照",
        "D01039": "专利",
        "D01040": "荣誉奖项",
        "D01041": "事件澄清",
        "D01042": "中介机构变更",
        "D01043": "接管托管",
        "D01044": "关联交易",
        "D01045": "工商变更",
        "D01046": "融资失败或取消",
        "E01001": "股东之间、股东与管理层之间出现矛盾",
        "E01002": "处罚事件或问询事件",
        "E01003": "实控人/高管人员出现变更或职位频繁变动，核心人员离职",
        "E01004": "实际控制人/主要自然人股东/高管/员工涉及违法、自杀或婚姻危机等事项",
        "E01005": "拖欠员工工资、大量辞工或员工大面积离职",
        "E01006": "组织形式变化而不利于企业架构稳定或管理",
        "E01007": "实际控制人（自然人）、高管无法履职",
        "E01008": "实际控制人、高管能力不足",
        "E01009": "企业后继接班人出现问题",
        "E01010": "虚假注资、抽逃资金或注资不到位",
        "E01011": "其他管理预警",
        "E01012": "招聘信息",
        "E01013": "员工关怀",
        "E01014": "股权激励",
        "E01015": "员工持股计划",
        "F01001": "项目审批手续不完备",
        "F01002": "项目投产后产能或经济效益与预期存在差距",
        "F01003": "项目资金未达标、未按计划到位",
        "F01004": "项目出现停建、缓建、拖期",
        "F01005": "项目资金超预算",
        "F01006": "其他项目预警",
        "G01001": "担保物、抵(质)押物存在问题",
        "G01002": "对外担保过多、金额巨大",
        "G01003": "担保链风险",
        "G01004": "违规担保",
        "G01005": "保证人、担保保人（含自然人）出现问题",
        "G01006": "与担保方关系恶化，担保方是否出现试图撤销或更改担保情况",
        "G01007": "其他担保信息",
        "H01001": "遭遇地震、火灾、水灾等不可抗力风险等",
        "I01001": "产品设计与生产缺陷，产品、生产工艺属于国家限制类或淘汰类",
        "I01002": "金融产品（包括通道业务）逾期贷款、不良贷款增加",
        "I01003": "产品设计或功能缺陷导致投入市场后与预期不符",
        "I01004": "产品侵权",
        "I01005": "其他产品预警",
        "I01006": "金融产品投资对象出现问题",
        "I01007": "主要产品价格呈下降趋势",
        "I01008": "产品信息",
        "J01001": "问询/关注函",
        "J01002": "监管谈话/监管函",
        "J01003": "行政处罚",
        "J01004": "审批不通过（批准）、监管叫停",
        "J01005": "监管机构对公司采取了更为严格的管理措施",
        "J01006": "各类指标接近或超过监管比率底线要求",
        "J01007": "其他监管预警",
        "K01001": "违规举债",
        "K01002": "违规收费",
        "K01003": "违规征地",
        "K01004": "挪用专项资金或改变既定资金用途",
        "K01005": "财政困难",
        "K01006": "虚报数据或工作进度",
        "K01007": "政策或相关工作落实不到位",
        "K01008": "政府部门负责人或直接责任人被调查或问责等",
        "K01009": "其他政府预警",
        "L01001": "其他风险类事件",
        "L01002": "领导视察",
        "L01003": "其他新闻"
    }


def _get_emotion_mapping() -> Dict[str, str]:
    """情感代码转换为中文"""
    return {
        "0": "中性",
        "1": "正面",
        "2": "负面"
    }


def _get_degree_mapping() -> Dict[str, str]:
    """影响程度代码转换为中文"""
    return {
        "3": "重大利好",
        "2": "较大利好",
        "1": "中度利好",
        "0": "较小影响",
        "-1": "中度影响",
        "-2": "较大影响",
        "-3": "严重影响"
    }


# ============ 辅助函数 ============

def _get_list_str(items: List[str], separator: str = '、') -> str:
    """将列表转换为字符串"""
    return separator.join(items) if items else ''


# ============ API 调用 ============

def _call_sentiment_api(entname: str, start_time: str = None, size: int = None) -> Dict[str, Any]:
    """调用舆情信息 API"""
    params = {
        'entname': entname,
        'newsEmotionCode': '0,1,2',
        'entEmotionCode': '0,1,2'
    }

    if start_time:
        params['startTime'] = start_time
    if size:
        params['size'] = size

    return call_api('/opinion/list', params, method='GET')


def _fetch_sentiment_data(entname: str) -> Dict[str, Any]:
    """获取舆情数据，支持重试逻辑"""
    # 计算近三个月的日期
    three_months_ago = datetime.now() - timedelta(days=90)
    start_time = three_months_ago.strftime('%Y-%m-%d')

    # 第一次查询：带时间限制
    response = _call_sentiment_api(entname, start_time)
    response_code = response.get('code') or response.get('CODE')

    # 如果失败，去掉时间限制查询前100条
    if response_code != 200:
        debug_print("近三个月查询失败，正在查询全部数据的前100条...")
        response = _call_sentiment_api(entname, size=100)
        response_code = response.get('code') or response.get('CODE')

        if response_code != 200:
            return {}

    return response


# ============ 数据处理 ============

def _process_sentiment_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理舆情数据"""
    news_class_mapping = _get_news_class_mapping()
    emotion_mapping = _get_emotion_mapping()
    degree_mapping = _get_degree_mapping()

    total_count = response.get('TOTALCOUNT', 0)
    original_data_list = response.get('DATA', [])

    # 处理统计信息
    publish_year_count = []
    if 'PUBLISHYEARCOUNT' in response:
        for item in response['PUBLISHYEARCOUNT']:
            publish_year_count.append({
                "发布年份": item.get('PUBLISHYEAR'),
                "数量": item.get('COUNT')
            })

    effect_count = []
    if 'EFFECTCOUNT' in response:
        for item in response['EFFECTCOUNT']:
            effect_count.append({
                "影响类型": item.get('EFFECT'),
                "数量": item.get('COUNT')
            })

    ent_emotion_count = []
    if 'ENTEMOTIONCOUNT' in response:
        for item in response['ENTEMOTIONCOUNT']:
            emotion_code = item.get('ENT_EMOTIONCODE', '')
            emotion_chinese = emotion_mapping.get(str(emotion_code), item.get('ENT_EMOTION', ''))
            ent_emotion_count.append({
                "企业情感": emotion_chinese,
                "数量": item.get('COUNT')
            })

    news_class_count = []
    if 'NEWSCLASSCOUNT' in response:
        for item in response['NEWSCLASSCOUNT']:
            news_class_code = item.get('NEWS_CLASSCODE')
            news_class_chinese = news_class_mapping.get(news_class_code, news_class_code)
            news_class_count.append({
                "新闻分类": news_class_chinese,
                "数量": item.get('COUNT')
            })

    degree_count = []
    if 'DEGREECOUNT' in response:
        for item in response['DEGREECOUNT']:
            degree_code = item.get('DEGREECODE', '')
            degree_chinese = degree_mapping.get(str(degree_code), item.get('DEGREE', ''))
            degree_count.append({
                "影响程度": degree_chinese,
                "数量": item.get('COUNT')
            })

    # 处理舆情详情
    data_list = []
    for item in original_data_list:
        # 转换新闻分类码值
        news_class_list = []
        if 'NEWS_CLASS' in item and isinstance(item['NEWS_CLASS'], list):
            news_class_list = item['NEWS_CLASS']
        elif 'NEWS_CLASSCODE' in item and isinstance(item['NEWS_CLASSCODE'], list):
            for code in item['NEWS_CLASSCODE']:
                news_class_list.append(news_class_mapping.get(code, code))

        # 转换情感和程度
        news_emotion_code = item.get('NEWS_EMOTIONCODE', '')
        news_emotion = emotion_mapping.get(str(news_emotion_code), item.get('NEWS_EMOTION', ''))

        ent_emotion_code = item.get('ENT_EMOTIONCODE', '')
        ent_emotion = emotion_mapping.get(str(ent_emotion_code), item.get('ENT_EMOTION', ''))

        degree_code = item.get('DEGREECODE', '')
        degree = degree_mapping.get(str(degree_code), item.get('DEGREE', ''))

        data_list.append({
            "新闻标题": item.get('NEWSTITLE'),
            "新闻摘要": item.get('NEWSSUMMARY'),
            "发布日期": item.get('PUBLISHDATE'),
            "影响类型": item.get('EFFECT'),
            "新闻来源": item.get('NEWSSOURCE'),
            "新闻情感": news_emotion,
            "新闻分类": news_class_list,
            "企业情感": ent_emotion,
            "影响程度": degree
        })

    return {
        "舆情总数": total_count,
        "发布年份统计": publish_year_count,
        "影响类型统计": effect_count,
        "企业情感统计": ent_emotion_count,
        "新闻分类统计": news_class_count,
        "影响程度统计": degree_count,
        "舆情详情": data_list
    }


# ============ Markdown 格式化 ============

def _extract_enterprise_history(data: Dict[str, Any]) -> str:
    """提取企业历程"""
    lines = ["### 企业历程"]
    news_list = data.get('舆情详情', [])

    if news_list:
        # 提取最新发布日期
        dates = [news.get('发布日期', '')[:10] for news in news_list if news.get('发布日期')]
        if dates:
            latest_date = max(dates)
            lines.append(f"重大舆情事件时间线：{latest_date}（发布日期）")

        # 事件标题摘要（前20条）
        titles = [news.get('新闻标题', '') for news in news_list[:20] if news.get('新闻标题')]
        if titles:
            lines.append(f"事件标题摘要：{'；'.join(titles)}")

        # 影响类型分布
        impact_types = []
        for news in news_list:
            types = news.get('影响类型', [])
            if isinstance(types, list):
                impact_types.extend(types)
        unique_types = list(dict.fromkeys(impact_types))
        if unique_types:
            lines.append(f"影响类型分布：{_get_list_str(unique_types)}")

        # 影响程度分级
        impact_levels = list(dict.fromkeys([news.get('影响程度', '') for news in news_list if news.get('影响程度')]))
        if impact_levels:
            lines.append(f"影响程度分级：{_get_list_str(impact_levels)}")

    return '\n'.join(lines)


def _extract_main_business(data: Dict[str, Any]) -> str:
    """提取主营业务"""
    lines = ["### 主营业务"]
    news_list = data.get('舆情详情', [])

    if news_list:
        # 舆情涉及业务领域
        impact_types = []
        for news in news_list:
            types = news.get('影响类型', [])
            if isinstance(types, list):
                impact_types.extend(types)
        unique_types = list(dict.fromkeys(impact_types))
        if unique_types:
            lines.append(f"舆情涉及业务领域：{_get_list_str(unique_types)}")

        # 新闻分类关联性
        news_classes = []
        for news in news_list:
            classes = news.get('新闻分类', [])
            if isinstance(classes, list):
                news_classes.extend(classes)
        unique_classes = list(dict.fromkeys(news_classes))
        if unique_classes:
            lines.append(f"新闻分类关联性：{_get_list_str(unique_classes)}")

    return '\n'.join(lines)


def _extract_market_competitiveness(data: Dict[str, Any]) -> str:
    """提取市场竞争力"""
    lines = ["### 市场竞争力"]

    # 企业情感倾向统计
    sentiment_stats = data.get('企业情感统计', [])
    if sentiment_stats:
        strs = [f"{item.get('企业情感', '')}（{item.get('数量', 0)}）" for item in sentiment_stats]
        lines.append(f"企业情感倾向统计：{_get_list_str(strs)}")

    # 影响程度评估
    impact_level_stats = data.get('影响程度统计', [])
    if impact_level_stats:
        strs = [f"{item.get('影响程度', '')}（{item.get('数量', 0)}）" for item in impact_level_stats]
        lines.append(f"影响程度评估：{_get_list_str(strs)}")

    return '\n'.join(lines)


def _extract_brand_influence(data: Dict[str, Any]) -> str:
    """提取品牌影响力"""
    lines = ["### 品牌影响力"]

    # 情感属性分布
    sentiment_stats = data.get('企业情感统计', [])
    if sentiment_stats:
        strs = [f"{item.get('企业情感', '')}（{item.get('数量', 0)}）" for item in sentiment_stats]
        lines.append(f"情感属性分布：{_get_list_str(strs)}")

    news_list = data.get('舆情详情', [])
    if news_list:
        # 媒体来源覆盖
        sources = list(dict.fromkeys([news.get('新闻来源', '') for news in news_list if news.get('新闻来源')]))
        if sources:
            lines.append(f"媒体来源覆盖：{_get_list_str(sources[:10])}")

        # 新闻分类品牌关联
        news_classes = []
        for news in news_list:
            classes = news.get('新闻分类', [])
            if isinstance(classes, list):
                news_classes.extend(classes)
        unique_classes = list(dict.fromkeys(news_classes))
        if unique_classes:
            lines.append(f"新闻分类品牌关联：{_get_list_str(unique_classes)}")

    return '\n'.join(lines)


def _extract_risk_credit(data: Dict[str, Any]) -> str:
    """提取风险与信用"""
    lines = ["### 风险与信用"]

    # 负面舆情统计
    sentiment_stats = data.get('企业情感统计', [])
    negative_count = 0
    for item in sentiment_stats:
        if item.get('企业情感') == '负面':
            negative_count = item.get('数量', 0)
            break

    if negative_count > 0:
        # 筛选负面相关的新闻分类
        news_class_stats = data.get('新闻分类统计', [])
        negative_keywords = ['亏损', '下降', '重组失败', '犯罪', '减值', '诉讼', '停工', '查封', '扣押',
                            '冻结', '行政处罚', '退市', '破产', '暂停', '取消', '质押', '垄断', '违法',
                            '违约', '拖欠', '辞工', '地震', '火灾', '水灾', '制假', '虚假', '负面',
                            '投诉', '异常', '严重违法', '缺陷', '造假', '环保不达标', '偷税', '问询',
                            '关注函', '监管', '戴帽', '流动性风险', '预警', '无证', '停建', '缓建', '拖期']

        negative_classes = [item.get('新闻分类', '') for item in news_class_stats
                          if any(kw in item.get('新闻分类', '') for kw in negative_keywords)]

        if negative_classes:
            lines.append(f"负面舆情数量与类型：负面（{negative_count}），涉及新闻分类包括{_get_list_str(negative_classes)}")

    # 司法合规相关新闻分类
    news_class_stats = data.get('新闻分类统计', [])
    compliance_keywords = ['法律诉讼', '行政处罚', '监管', '问询', '关注函', '犯罪', '制假', '虚假',
                          '偷税', '环保不达标', '安全生产', '违法', '严重违法', '查封', '扣押', '冻结', '划转']

    compliance_classes = [item.get('新闻分类', '') for item in news_class_stats
                         if any(kw in item.get('新闻分类', '') for kw in compliance_keywords)]
    if compliance_classes:
        lines.append(f"司法合规相关新闻分类：{_get_list_str(compliance_classes)}")

    return '\n'.join(lines)


def _extract_operation_capital(data: Dict[str, Any]) -> str:
    """提取经营与资本"""
    lines = ["### 经营与资本"]

    news_list = data.get('舆情详情', [])

    # 资本运作新闻分类
    capital_keywords = ['股价', '投资', '融资', '发行', '股份', '股权', '重组', '破产', '退市',
                       '利润', '财务', '资产', '信用', '大宗', '对赌', '员工持股', '激励', '资金']
    capital_classes = []

    for news in news_list:
        classes = news.get('新闻分类', [])
        if isinstance(classes, list):
            for cls in classes:
                if any(kw in cls for kw in capital_keywords):
                    capital_classes.append(cls)

    unique_capital = list(dict.fromkeys(capital_classes))
    if unique_capital:
        lines.append(f"资本运作新闻分类：{_get_list_str(unique_capital)}")

    # 时间趋势分析
    year_stats = data.get('发布年份统计', [])
    if year_stats:
        strs = [f"{item.get('发布年份', '')}年（{item.get('数量', 0)}）" for item in year_stats]
        lines.append(f"时间趋势分析：发布年份统计为{_get_list_str(strs)}")

    return '\n'.join(lines)


def _extract_value_growth(data: Dict[str, Any]) -> str:
    """提取价值与成长"""
    lines = ["### 价值与成长"]

    sentiment_stats = data.get('企业情感统计', [])

    # 正面舆情
    positive_count = 0
    for item in sentiment_stats:
        if item.get('企业情感') == '正面':
            positive_count = item.get('数量', 0)
            break

    if positive_count > 0:
        # 提取影响类型
        impact_type_stats = data.get('影响类型统计', [])
        positive_types = [item.get('影响类型', '') for item in impact_type_stats if item.get('影响类型')]

        # 提取正面影响程度
        impact_level_stats = data.get('影响程度统计', [])
        positive_level_strs = [f"{item.get('影响程度', '')}（{item.get('数量', 0)}）"
                              for item in impact_level_stats if '利好' in item.get('影响程度', '')]

        # 筛选成长相关分类
        news_class_stats = data.get('新闻分类统计', [])
        growth_keywords = ['合作', '财务向好', '投资', '融资', '产品', '增持', '专利', '荣誉',
                          '合同', '投产', '资质', '补贴', '评级上调', '视察', '持股', '激励', '摘帽']
        growth_classes = [item.get('新闻分类', '') for item in news_class_stats
                         if any(kw in item.get('新闻分类', '') for kw in growth_keywords)]

        lines.append(f"成长驱动舆情信号：正面情感（{positive_count}），对应影响类型包括{_get_list_str(positive_types)}，"
                    f"影响程度为{_get_list_str(positive_level_strs)}，新闻分类包括{_get_list_str(growth_classes)}")

    # 负面舆情
    negative_count = 0
    for item in sentiment_stats:
        if item.get('企业情感') == '负面':
            negative_count = item.get('数量', 0)
            break

    if negative_count > 0:
        impact_type_stats = data.get('影响类型统计', [])
        negative_types = [item.get('影响类型', '') for item in impact_type_stats if item.get('影响类型')]

        impact_level_stats = data.get('影响程度统计', [])
        negative_levels = [item.get('影响程度', '') for item in impact_level_stats
                         if '影响' in item.get('影响程度', '')]

        lines.append(f"发展约束舆情指示：负面情感（{negative_count}），影响类型包括{_get_list_str(negative_types)}，"
                    f"影响程度为{_get_list_str(negative_levels)}")

    return '\n'.join(lines)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业舆情信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的舆情信息
    """
    # 1. 调用 API
    response = _fetch_sentiment_data(entname)

    if not response:
        return "# 舆情信息\n\n未查询到近期新闻舆情信息"

    # 2. 处理数据
    data = _process_sentiment_data(response)

    if not data or data.get('舆情总数', 0) == 0:
        return "# 舆情信息\n\n暂无舆情数据"

    # 3. 生成 Markdown
    sections = ["# 舆情信息提炼"]

    # 企业历程
    history = _extract_enterprise_history(data)
    if history and history != "### 企业历程":
        sections.append("")
        sections.append(history)

    # 主营业务
    business = _extract_main_business(data)
    if business and business != "### 主营业务":
        sections.append("")
        sections.append(business)

    # 市场竞争力
    competitiveness = _extract_market_competitiveness(data)
    if competitiveness and competitiveness != "### 市场竞争力":
        sections.append("")
        sections.append(competitiveness)

    # 品牌影响力
    brand = _extract_brand_influence(data)
    if brand and brand != "### 品牌影响力":
        sections.append("")
        sections.append(brand)

    # 风险与信用
    risk = _extract_risk_credit(data)
    if risk and risk != "### 风险与信用":
        sections.append("")
        sections.append(risk)

    # 经营与资本
    operation = _extract_operation_capital(data)
    if operation and operation != "### 经营与资本":
        sections.append("")
        sections.append(operation)

    # 价值与成长
    value = _extract_value_growth(data)
    if value and value != "### 价值与成长":
        sections.append("")
        sections.append(value)

    return '\n'.join(sections)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s06_sentiment <企业名称>")
