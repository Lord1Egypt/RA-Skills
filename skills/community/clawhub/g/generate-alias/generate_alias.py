#!/usr/bin/env python3
"""
企业别名智能生成器 v3.0.0
核心策略：
1. 优先使用品牌映射中的股票名称/品牌名
2. 提取企业核心词作为补充
3. 严格过滤通用词，确保关键字独特性
4. 可选维基百科查询（需配置 USE_WIKI = True）
"""

import re
import sys
import os
from typing import List

# 品牌映射（完整名称 -> 品牌/股票名）
BRAND_MAP = {
    # 互联网/科技
    '阿里巴巴': ['阿里', '淘宝', '天猫', '支付宝'],
    '腾讯': ['腾讯', '微信', 'QQ'],
    '百度': ['百度'],
    '京东': ['京东', 'JD'],
    '美团': ['美团'],
    '字节跳动': ['字节', '抖音', '头条'],
    '网易': ['网易'],
    '小米': ['小米'],
    '华为': ['华为'],
    '联想': ['联想'],
    '比亚迪': ['比亚迪', 'BYD'],
    '格力': ['格力'],
    '海尔': ['海尔'],
    '美的': ['美的'],
    '苹果': ['苹果'],
    '三星': ['三星'],
    'OPPO': ['OPPO'],
    'vivo': ['vivo'],
    '中兴': ['中兴'],
    
    # 金融
    '中国平安': ['平安'],
    '招商银行': ['招行'],
    '工商银行': ['工行'],
    '建设银行': ['建行'],
    '农业银行': ['农行'],
    '中国银行': ['中行'],
    '交通银行': ['交行'],
    '浦发银行': ['浦发'],
    '兴业银行': ['兴业'],
    '民生银行': ['民生'],
    '光大银行': ['光大'],
    '中信证券': ['中信'],
    '国泰君安': ['君安'],
    '华泰证券': ['华泰'],
    '中金公司': ['中金'],
    
    # 消费
    '贵州茅台': ['茅台'],
    '五粮液': ['五粮液'],
    '泸州老窖': ['老窖'],
    '伊利': ['伊利'],
    '蒙牛': ['蒙牛'],
    '海天味业': ['海天'],
    '农夫山泉': ['农夫'],
    '康师傅': ['康师傅'],
    '统一': ['统一'],
    '娃哈哈': ['娃哈哈'],
    
    # 医药
    '云南白药': ['白药'],
    '恒瑞医药': ['恒瑞'],
    '复星医药': ['复星'],
    '同仁堂': ['同仁'],
    '片仔癀': ['片仔'],
    '白云山': ['白云'],
    
    # 地产/建筑
    '万科': ['万科'],
    '碧桂园': ['碧桂'],
    '保利': ['保利'],
    '华润': ['华润'],
    '龙湖': ['龙湖'],
    '恒大': ['恒大'],
    '融创': ['融创'],
    '绿地': ['绿地'],
    
    # 工业/制造
    '三一重工': ['三一'],
    '中联重科': ['中联'],
    '徐工': ['徐工'],
    '柳工': ['柳工'],
    '中国中车': ['中车'],
    '中国中铁': ['中铁'],
    '中国建筑': ['中建'],
    '宝武': ['宝武'],
    '鞍钢': ['鞍钢'],
    '包钢': ['包钢'],
    '华能': ['华能'],
    '大唐': ['大唐'],
    
    # 汽车
    '长城汽车': ['长城', '哈弗'],
    '吉利汽车': ['吉利'],
    '上汽': ['上汽'],
    '广汽': ['广汽'],
    '北汽': ['北汽'],
    '一汽': ['一汽'],
    '东风': ['东风'],
    '蔚来': ['蔚来'],
    '理想': ['理想'],
    '小鹏': ['小鹏'],
}

# 通用前缀（需要移除的）
PREFIX_FILTER = {
    '中国', '中华', '国家', '国际', '全国',
    '北京', '上海', '天津', '重庆',
    '浙江', '江苏', '广东', '山东', '四川', '湖北', '湖南', '福建',
    '安徽', '河南', '河北', '辽宁', '陕西', '山西', '江西', '广西',
    '云南', '贵州', '甘肃', '宁夏', '新疆', '西藏', '青海', '内蒙古',
    '黑龙江', '吉林', '海南',
}

# 通用后缀（需要移除的）
SUFFIX_FILTER = {
    '集团股份有限公司', '集团有限公司', '集团控股有限公司',
    '股份有限公司', '有限责任公司', '有限公司',
    '控股股份有限公司', '投资有限公司', '科技股份有限公司',
    '实业股份有限公司', '发展股份有限公司', '投资股份有限公司',
    '集团', '控股', '股份', '有限', '公司', '责任',
}

# 行业词（不适合作为关键字）
INDUSTRY_WORDS = {
    # 企业类型
    '集团', '控股', '股份', '有限', '责任', '企业', '公司',
    # 地区前缀
    '中国', '中华', '国际', '全国',
    '北京', '上海', '天津', '重庆',
    '浙江', '江苏', '广东', '山东', '四川', '湖北', '湖南', '福建',
    '安徽', '河南', '河北', '辽宁', '陕西', '山西', '江西', '广西',
    '云南', '贵州', '甘肃', '宁夏', '新疆', '西藏', '青海', '内蒙古',
    '黑龙江', '吉林', '海南',
}

# 配置
USE_WIKI = False  # 是否使用维基百科查询
WIKI_TIMEOUT = 5  # 维基百科请求超时（秒）


def is_government(name: str) -> bool:
    """判断是否为政府部门"""
    patterns = ['政府', '部', '委', '局', '办', '署', '院']
    return any(p in name for p in patterns)


def clean_name(name: str) -> str:
    """清理企业名称"""
    result = name
    # 移除括号内容
    result = re.sub(r'[（(][^）)]*[）)]', '', result)
    # 移除后缀
    for suffix in sorted(SUFFIX_FILTER, key=len, reverse=True):
        if result.endswith(suffix):
            result = result[:-len(suffix)]
            break
    return result.strip()


def get_brand_name(company_name: str) -> List[str]:
    """从品牌映射获取品牌名"""
    for full_name, brands in BRAND_MAP.items():
        if full_name in company_name:
            return brands
    
    short = company_name[:4]
    for full_name, brands in BRAND_MAP.items():
        if short in full_name:
            return brands
    
    return []


def extract_core_words(company_name: str) -> List[str]:
    """提取核心词"""
    words = []
    cleaned = clean_name(company_name)
    if not cleaned:
        return words
    
    # 移除前缀
    remaining = cleaned
    for prefix in sorted(PREFIX_FILTER, key=len, reverse=True):
        if remaining.startswith(prefix):
            remaining = remaining[len(prefix):]
            break
    
    if not remaining:
        return words
    
    # 提取最后2-4个字（通常是核心词）
    if len(remaining) >= 2:
        words.append(remaining[-2:])
    if len(remaining) >= 3:
        words.append(remaining[-3:])
    if len(remaining) >= 4:
        words.append(remaining[-4:])
    
    # 如果有控股/集团，也可以提取前面的词
    if '控股' in company_name or '集团' in company_name:
        if len(remaining) >= 3:
            words.append(remaining[:3])
    
    return words


def is_valid_keyword(word: str) -> bool:
    """判断是否为有效关键字"""
    if not word or len(word) < 2:
        return False
    
    # 必须包含中文或英文
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z]+$', word):
        return False
    
    # 整体等于过滤词 -> 过滤
    if word in INDUSTRY_WORDS:
        return False
    
    # 包含地区前缀词 -> 过滤
    for prefix in PREFIX_FILTER:
        if word.startswith(prefix):
            return False
    
    # 包含企业类型词 -> 过滤
    for suffix in SUFFIX_FILTER:
        if word.endswith(suffix) and word != suffix:
            return False
    
    # 太短的词 -> 过滤（至少3个字）
    if len(word) < 3:
        return False
    
    return True


def dedupe(keywords: List[str]) -> List[str]:
    """去重"""
    seen = set()
    result = []
    for kw in keywords:
        kw = kw.strip()
        if not kw or len(kw) < 2:
            continue
        if kw in seen:
            continue
        seen.add(kw)
        result.append(kw)
    # 按长度排序
    result.sort(key=len)
    return result


def search_wiki(company_name: str) -> List[str]:
    """从维基百科搜索简称"""
    if not USE_WIKI:
        return []
    
    try:
        import requests
        
        # 准备搜索名称
        suffixes = ['股份有限公司', '有限责任公司', '有限公司', 
                   '集团有限公司', '集团股份有限公司']
        search_name = company_name
        for suffix in suffixes:
            if search_name.endswith(suffix):
                search_name = search_name[:-len(suffix)]
                break
        
        if len(search_name) < 3:
            return []
        
        url = 'https://zh.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': search_name,
            'format': 'json',
            'limit': 3
        }
        
        headers = {'User-Agent': 'EnterpriseKeywordBot/1.0'}
        resp = requests.get(url, params=params, headers=headers, timeout=WIKI_TIMEOUT)
        
        if resp.status_code == 200:
            data = resp.json()
            short_names = []
            if 'query' in data and 'search' in data['query']:
                for item in data['query']['search']:
                    title = item['title']
                    # 清理标题中的括号
                    title_clean = re.sub(r'[（(][^）)]*[）)]', '', title)
                    if 2 <= len(title_clean) <= 6:
                        short_names.append(title_clean)
            return short_names
        
    except Exception as e:
        pass
    
    return []


def generate_rule_based_aliases(company_name: str) -> List[str]:
    """
    生成企业别名（规则引擎）
    
    Args:
        company_name: 企业名称
        
    Returns:
        别名列表，按优先级排序
    """
    keywords = []
    
    # 1. 政府部门 -> 返回全称
    if is_government(company_name):
        return [company_name]
    
    # 2. 维基百科简称（如果启用）
    if USE_WIKI:
        wiki_names = search_wiki(company_name)
        for name in wiki_names:
            if is_valid_keyword(name):
                keywords.append(name)
    
    # 3. 品牌映射
    brand_names = get_brand_name(company_name)
    for name in brand_names:
        if is_valid_keyword(name) and name not in keywords:
            keywords.append(name)
    
    # 4. 核心词
    core_words = extract_core_words(company_name)
    for name in core_words:
        if is_valid_keyword(name) and name not in keywords:
            keywords.append(name)
    
    # 5. 去重
    keywords = dedupe(keywords)
    
    # 6. 如果没有结果，返回全称
    if not keywords:
        cleaned = clean_name(company_name)
        return [cleaned] if cleaned else [company_name]
    
    return keywords[:5]  # 最多5个关键字


def generate_aliases(company_name: str, use_web: bool = True) -> List[str]:
    """
    生成企业别名（主入口）
    
    Args:
        company_name: 企业名称
        use_web: 是否使用网络搜索（暂未实现）
        
    Returns:
        别名列表
    """
    return generate_rule_based_aliases(company_name)


if __name__ == "__main__":
    # 命令行测试
    import argparse
    
    parser = argparse.ArgumentParser(description='企业别名智能生成器')
    parser.add_argument('company', nargs='?', help='企业名称')
    
    args = parser.parse_args()
    
    if args.company:
        aliases = generate_rule_based_aliases(args.company)
        print(args.company)
        print('输出:', ' | '.join(aliases))
    else:
        # 批量测试
        test_companies = [
            "比亚迪股份有限公司",
            "内蒙古伊利实业集团股份有限公司",
            "云南白药集团股份有限公司",
            "北京东方雨虹防水技术股份有限公司",
            "长城汽车股份有限公司",
            "佛山市海天调味食品股份有限公司",
            "中国工商银行股份有限公司",
            "腾讯控股有限公司",
            "浙江省人民政府国有资产监督管理委员会",
        ]
        
        print('=' * 60)
        print('企业别名智能生成器 v3.0.0 测试')
        print('=' * 60)
        
        for company in test_companies:
            aliases = generate_rule_based_aliases(company)
            print(f'\n{company}')
            print('  -> ' + ' | '.join(aliases))