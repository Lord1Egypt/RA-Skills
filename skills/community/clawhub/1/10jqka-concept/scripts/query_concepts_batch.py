#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺 F10 概念批量查询脚本（带缓存）
- 仅查询重点个股（涨跌幅>5%）
- 缓存概念数据，减少重复查询
- 缓存有效期：当日有效
"""

import requests
import json
import os
import sys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

# 配置
CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/cache")
CACHE_FILE = os.path.join(CACHE_DIR, "10jqka_concepts.json")
CACHE_EXPIRY_HOURS = 24  # 缓存有效期（小时）

def ensure_cache_dir():
    """确保缓存目录存在"""
    os.makedirs(CACHE_DIR, exist_ok=True)

def load_cache():
    """加载缓存"""
    ensure_cache_dir()
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 检查缓存是否过期
                cache_time = datetime.fromisoformat(data.get("cache_time", "2000-01-01"))
                if datetime.now() - cache_time < timedelta(hours=CACHE_EXPIRY_HOURS):
                    return data
        except Exception as e:
            print(f"加载缓存失败：{e}", file=sys.stderr)
    return {"stocks": {}, "cache_time": None}

def save_cache(data):
    """保存缓存"""
    ensure_cache_dir()
    data["cache_time"] = datetime.now().isoformat()
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存缓存失败：{e}", file=sys.stderr)

def get_stock_concepts(stock_code, use_cache=True):
    """
    获取股票所属概念板块（带缓存）
    使用同花顺问财搜索 API 获取概念数据
    
    Args:
        stock_code: 股票代码（如 300059）
        use_cache: 是否使用缓存
    
    Returns:
        dict: 包含股票信息和概念列表
    """
    # 检查缓存
    if use_cache:
        cache = load_cache()
        if stock_code in cache.get("stocks", {}):
            cached = cache["stocks"][stock_code]
            cached_time = datetime.fromisoformat(cached.get("cached_at", "2000-01-01"))
            if datetime.now() - cached_time < timedelta(hours=CACHE_EXPIRY_HOURS):
                return {**cached, "from_cache": True}
    
    # 方法 1: 尝试问财搜索 API
    concepts = query_iwencai(stock_code)
    
    # 方法 2: 如果问财失败，尝试爬取 F10 页面
    if not concepts:
        concepts = scrape_f10_page(stock_code)
    
    # 获取股票名称
    stock_name = get_stock_name(stock_code)
    
    result = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "concepts": concepts,
        "concept_count": len(concepts),
        "cached_at": datetime.now().isoformat(),
        "from_cache": False
    }
    
    # 更新缓存
    if use_cache and not result.get("error"):
        cache = load_cache()
        if "stocks" not in cache:
            cache["stocks"] = {}
        cache["stocks"][stock_code] = result
        save_cache(cache)
    
    return result


# 常见股票核心概念映射（缓存常用股票，减少爬取）
STOCK_CONCEPTS = {
    "300059": ["券商", "互联网金融", "基金", "财富管理", "数字经济"],  # 东方财富
    "000725": ["面板", "显示", "半导体", "消费电子", "物联网"],  # 京东方 A
    "002594": ["新能源汽车", "锂电池", "电池", "光伏", "储能"],  # 比亚迪
    "000001": ["银行", "金融科技", "普惠金融", "数字经济"],  # 平安银行
    "000002": ["房地产", "物业管理", "基建", "央企改革"],  # 万科 A
    "600519": ["白酒", "消费", "食品饮料", "奢侈品"],  # 贵州茅台
    "300750": ["新能源汽车", "锂电池", "储能", "电池"],  # 宁德时代
    "000858": ["白酒", "消费", "食品饮料"],  # 五粮液
    "601318": ["保险", "金融科技", "财富管理"],  # 中国平安
    "600030": ["券商", "证券", "财富管理", "金融科技"],  # 中信证券
    "002230": ["人工智能", "语音技术", "大数据", "云计算"],  # 科大讯飞
    "002415": ["安防", "人工智能", "大数据", "物联网"],  # 海康威视
    "300124": ["工业自动化", "机器人", "智能制造", "新能源汽车"],  # 汇川技术
    "601888": ["旅游", "酒店", "消费", "免税"],  # 中国中免
    "600276": ["创新药", "生物医药", "医疗器械", "医药"],  # 恒瑞医药
    "601127": ["新能源汽车", "自动驾驶", "锂电池", "消费电子"],  # 赛力斯
    "002475": ["消费电子", "苹果产业链", "通信设备", "精密制造"],  # 立讯精密
    "600036": ["银行", "金融科技", "财富管理"],  # 招商银行
    "601899": ["黄金", "有色金属", "贵金属", "资源"],  # 紫金矿业
    "000333": ["家电", "消费", "智能制造", "机器人"],  # 美的集团
    # 新增：科技/制造类
    "688059": ["工业母机", "数控刀具", "智能制造", "高端装备", "科创板"],  # 华锐精密
    "603690": ["半导体", "清洗设备", "集成电路", "芯片", "科创板"],  # 至纯科技
    "688012": ["半导体", "中微公司", "刻蚀机", "集成电路", "科创板"],  # 中微公司
    "688981": ["半导体", "中芯国际", "集成电路", "芯片制造", "科创板"],  # 中芯国际
    "300316": ["工业自动化", "机器人", "智能制造", "新能源汽车"],  # 汇川技术
    "002371": ["半导体", "芯片", "集成电路", "消费电子"],  # 北方华创
    "600703": ["半导体", "LED", "芯片", "光电"],  # 三安光电
    "002049": ["芯片", "紫光国微", "集成电路", "军工"],  # 紫光国微
    "300782": ["半导体", "卓胜微", "芯片", "射频"],  # 卓胜微
    "688008": ["半导体", "澜起科技", "芯片", "内存接口"],  # 澜起科技
    "300661": ["半导体", "圣邦股份", "芯片", "模拟芯片"],  # 圣邦股份
    "603986": ["半导体", "兆易创新", "芯片", "存储"],  # 兆易创新
    "002185": ["半导体", "华天科技", "芯片", "封装测试"],  # 华天科技
    "002156": ["半导体", "通富微电", "芯片", "封装测试"],  # 通富微电
    "600584": ["半导体", "长电科技", "芯片", "封装测试"],  # 长电科技
    # 更多科技股（修复错误缓存）
    "688802": ["GPU", "芯片", "集成电路", "人工智能", "科创板"],  # 沐曦股份
    "601869": ["光纤光缆", "通信设备", "5G", "光通信"],  # 长飞光纤
    "603061": ["半导体", "芯片", "测试设备", "集成电路"],  # 金海通
    "301005": ["紧固件", "航空航天", "军工", "高端装备"],  # 超捷股份
    "001309": ["存储", "芯片", "半导体", "消费电子"],  # 德明利
    "002850": ["锂电池结构件", "新能源汽车", "宁德时代链", "高端装备"],  # 科达利
    "688308": ["数控刀具", "工业母机", "智能制造", "科创板"],  # 欧科亿
    "001400": ["PCB", "电子", "半导体", "科技"],  # 江顺科技
    "688200": ["半导体", "测试设备", "集成电路", "科创板"],  # 华峰测控
    "688630": ["激光直写", "半导体", "PCB", "科创板"],  # 芯碁微装
    "301232": ["风电", "紧固件", "高端装备", "新能源"],  # 飞沃科技
    "301377": ["刀具", "工业母机", "高端装备", "科创板"],  # 鼎泰高科
    "688019": ["半导体", "材料", "集成电路", "科创板"],  # 安集科技
    "688120": ["半导体", "设备", "CMP", "科创板"],  # 华海清科
    "688025": ["激光", "光通信", "半导体", "科创板"],  # 杰普特
    "301306": ["检测", "军工", "航空航天", "创业板"],  # 西测测试
    "688072": ["半导体", "设备", "薄膜沉积", "科创板"],  # 拓荆科技
    "688336": ["生物药", "医药", "创新药", "科创板"],  # 三生国健
    "688693": ["半导体", "功率器件", "科创板"],  # 锴威特
    "688270": ["军工", "航空航天", "半导体", "科创板"],  # 臻镭科技
    "300548": ["光模块", "通信", "AI", "创业板"],  # 长芯博创
    "688677": ["医疗器械", "医疗", "科创板"],  # 海泰新光
    "688257": ["刀具", "工业母机", "高端装备", "科创板"],  # 新锐股份
    "301018": ["空调", "数据中心", "储能", "创业板"],  # 申菱环境
    "301200": ["PCB", "激光", "半导体", "创业板"],  # 大族数控
    "002432": ["医疗器械", "血糖仪", "医疗", "消费"],  # 九安医疗
    "688331": ["生物药", "医药", "创新药", "科创板"],  # 荣昌生物
    "603256": ["电子布", "玻纤", "电子", "科技"],  # 宏和科技
    "002222": ["激光", "光通信", "半导体", "科技"],  # 福晶科技
    "688409": ["半导体", "精密件", "航空航天", "科创板"],  # 富创精密
    "300900": ["航空航天", "军工", "无人机", "创业板"],  # 广联航空
    "688383": ["半导体", "设备", "固晶机", "科创板"],  # 新益昌
    "300567": ["显示", "面板", "半导体", "创业板"],  # 精测电子
    "688809": ["半导体", "芯片", "科创板"],  # 强一股份
    "688368": ["半导体", "芯片", "电源管理", "科创板"],  # 晶丰明源
    "301008": ["家电", "塑料", "消费", "创业板"],  # 宏昌科技
    "301338": ["激光", "设备", "半导体", "创业板"],  # 凯格精机
    "688372": ["半导体", "测试", "芯片", "科创板"],  # 伟测科技
    "688375": ["军工", "芯片", "航空航天", "科创板"],  # 国博电子
    "001270": ["军工", "芯片", "相控阵", "中小板"],  # *ST 铖昌
    "603083": ["半导体", "设备", "清洗", "科创板"],  # 芯源微
    "688037": ["半导体", "设备", "刻蚀", "科创板"],  # 芯源微
    "688147": ["半导体", "材料", "光刻胶", "科创板"],  # 微导纳米
    "688234": ["半导体", "设备", "检测", "科创板"],  # 天准科技
    # 医药类
    "000538": ["中药", "云南白药", "医药", "消费"],  # 云南白药
    "000999": ["医药", "华润三九", "中药", "OTC"],  # 华润三九
    "600436": ["中药", "片仔癀", "医药", "消费"],  # 片仔癀
    "000519": ["军工", "中兵红箭", "兵器", "国防"],  # 中兵红箭
    # 新能源/光伏
    "002460": ["锂", "赣锋锂业", "新能源汽车", "锂电池"],  # 赣锋锂业
    "002466": ["锂", "天齐锂业", "新能源汽车", "锂电池"],  # 天齐锂业
    "002812": ["锂电池", "恩捷股份", "隔膜", "新能源汽车"],  # 恩捷股份
    "300014": ["锂电池", "亿纬锂能", "电池", "储能"],  # 亿纬锂能
    "002594": ["新能源汽车", "比亚迪", "锂电池", "电池"],  # 比亚迪
    "601012": ["光伏", "隆基绿能", "太阳能", "硅片"],  # 隆基绿能
    "300274": ["光伏", "阳光电源", "逆变器", "储能"],  # 阳光电源
    "002459": ["光伏", "晶澳科技", "太阳能", "电池片"],  # 晶澳科技
    # 消费/食品
    "000858": ["白酒", "五粮液", "消费", "食品饮料"],  # 五粮液
    "000568": ["白酒", "泸州老窖", "消费", "食品饮料"],  # 泸州老窖
    "002304": ["白酒", "洋河股份", "消费", "食品饮料"],  # 洋河股份
    "600887": ["乳业", "伊利股份", "消费", "食品饮料"],  # 伊利股份
    "000895": ["猪肉", "双汇发展", "食品", "消费"],  # 双汇发展
    # 金融
    "601398": ["银行", "工商银行", "金融", "央企"],  # 工商银行
    "601939": ["银行", "建设银行", "金融", "央企"],  # 建设银行
    "601288": ["银行", "农业银行", "金融", "央企"],  # 农业银行
    "601988": ["银行", "中国银行", "金融", "央企"],  # 中国银行
    "600016": ["银行", "民生银行", "金融"],  # 民生银行
    "601166": ["银行", "兴业银行", "金融"],  # 兴业银行
    "600000": ["银行", "浦发银行", "金融"],  # 浦发银行
    "000001": ["银行", "平安银行", "金融", "金融科技"],  # 平安银行
    "601628": ["保险", "中国人寿", "金融"],  # 中国人寿
    "601601": ["保险", "中国太保", "金融"],  # 中国太保
    "601336": ["保险", "新华保险", "金融"],  # 新华保险
    "600030": ["券商", "中信证券", "证券", "金融"],  # 中信证券
    "300059": ["券商", "东方财富", "互联网金融", "金融"],  # 东方财富
    "601688": ["券商", "华泰证券", "证券", "金融"],  # 华泰证券
    # 周期/资源
    "600028": ["石油", "中国石化", "能源", "央企"],  # 中国石化
    "601857": ["石油", "中国石油", "能源", "央企"],  # 中国石油
    "600938": ["石油", "中国海油", "能源", "央企"],  # 中国海油
    "600547": ["黄金", "山东黄金", "贵金属", "资源"],  # 山东黄金
    "600489": ["黄金", "中金黄金", "贵金属", "资源"],  # 中金黄金
    "000630": ["铜", "铜陵有色", "有色金属", "资源"],  # 铜陵有色
    "000878": ["铜", "云南铜业", "有色金属", "资源"],  # 云南铜业
    "601600": ["铝", "中国铝业", "有色金属", "资源"],  # 中国铝业
    "000807": ["铝", "云铝股份", "有色金属", "资源"],  # 云铝股份
    "600595": ["铝", "中孚实业", "有色金属", "资源"],  # 中孚实业
    "601088": ["煤炭", "中国神华", "能源", "央企"],  # 中国神华
    "600188": ["煤炭", "兖矿能源", "能源"],  # 兖矿能源
    # 基建/建筑
    "601390": ["基建", "中国中铁", "建筑", "央企"],  # 中国中铁
    "601186": ["基建", "中国铁建", "建筑", "央企"],  # 中国铁建
    "601668": ["基建", "中国建筑", "建筑", "央企"],  # 中国建筑
    "601800": ["基建", "中国交建", "建筑", "央企"],  # 中国交建
    "600585": ["水泥", "海螺水泥", "建材", "周期"],  # 海螺水泥
    # 科技/通信
    "000063": ["5G", "中兴通讯", "通信设备", "科技"],  # 中兴通讯
    "300308": ["光模块", "中际旭创", "通信", "AI"],  # 中际旭创
    "300502": ["光模块", "新易盛", "通信", "AI"],  # 新易盛
    "300394": ["光模块", "天孚通信", "通信", "AI"],  # 天孚通信
    "002281": ["光通信", "光迅科技", "通信", "芯片"],  # 光迅科技
    "600498": ["通信", "烽火通信", "5G", "科技"],  # 烽火通信
    "002139": ["芯片", "紫光国微", "半导体", "军工"],  # 紫光国微
    # 军工
    "000768": ["军工", "中航西飞", "航空", "央企"],  # 中航西飞
    "600760": ["军工", "中航沈飞", "航空", "央企"],  # 中航沈飞
    "600893": ["军工", "航发动力", "航空发动机", "央企"],  # 航发动力
    "002389": ["军工", "航天彩虹", "无人机", "航天"],  # 航天彩虹
    "688297": ["军工", "中无人机", "无人机", "科创板"],  # 中无人机
    "002179": ["军工", "光电股份", "光电", "兵器"],  # 光电股份
    # 其他热门
    "002405": ["软件", "四维图新", "自动驾驶", "地图"],  # 四维图新
    "002230": ["AI", "科大讯飞", "人工智能", "语音"],  # 科大讯飞
    "600570": ["软件", "恒生电子", "金融科技", "AI"],  # 恒生电子
    "300496": ["AI", "中科创达", "智能汽车", "软件"],  # 中科创达
    "002415": ["安防", "海康威视", "AI", "大数据"],  # 海康威视
    "002236": ["安防", "大华股份", "AI", "视频监控"],  # 大华股份
    "600745": ["存储", "兆易创新", "芯片", "半导体"],  # 兆易创新
    "688126": ["半导体", "沪硅产业", "硅片", "科创板"],  # 沪硅产业
}


def query_iwencai(stock_code):
    """
    获取股票核心概念
    优先使用预定义映射，其次爬取问财
    只返回核心概念和主营业务（最多 5 个）
    """
    # 优先使用预定义映射
    if stock_code in STOCK_CONCEPTS:
        return [{"name": c, "source": "preset"} for c in STOCK_CONCEPTS[stock_code][:5]]
    
    try:
        # 查询主营业务
        url = f"https://www.iwencai.com/unifiedwap/result?w={stock_code} 主营业务 所属概念"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=10)
        text = response.text
        
        concepts = []
        
        # 核心概念优先级列表
        core_concepts = [
            "券商", "证券", "银行", "保险", "互金", "互联网金融", "金融科技", "财富管理",
            "人工智能", "AI", "大数据", "云计算", "区块链", "信创", "数字经济",
            "半导体", "芯片", "集成电路", "面板", "显示", "消费电子", "光学光电子",
            "新能源汽车", "锂电池", "电池", "光伏", "风电", "储能", "电动车",
            "5G", "通信设备", "光模块", "CPO", "卫星导航",
            "创新药", "生物医药", "医疗器械", "中药", "医药",
            "机器人", "工业自动化", "智能制造", "航空航天", "军工",
            "白酒", "食品饮料", "家电", "消费", "电商", "零售", "旅游", "酒店",
            "房地产", "基建", "建材", "工程机械", "物业管理",
            "有色金属", "稀土", "黄金", "钢铁", "煤炭", "化工", "石油",
            "一带一路", "国企改革", "央企改革", "专精特新", "科创板", "创业板"
        ]
        
        found_concepts = []
        for concept in core_concepts:
            if concept in text:
                found_concepts.append(concept)
        
        # 去重并限制最多 5 个
        seen = set()
        for c in found_concepts:
            if c not in seen:
                seen.add(c)
                concepts.append({"name": c, "source": "iwencai"})
        
        return concepts[:5]
        
    except Exception as e:
        return []


def scrape_f10_page(stock_code):
    """
    爬取同花顺 F10 页面获取概念
    """
    url = f"https://basic.10jqka.com.cn/{stock_code}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "gbk"
        
        soup = BeautifulSoup(response.text, "html.parser")
        concepts = []
        
        # 查找概念相关的表格或列表
        for tag in soup.find_all(["a", "span", "td"]):
            text = tag.get_text(strip=True)
            href = tag.get("href", "")
            
            # 检查是否是概念链接
            if "gn/detail" in href or "concept" in href.lower():
                if text and len(text) > 1 and text not in ["返回", "首页", "更多", "概念题材"]:
                    if text not in [c["name"] for c in concepts]:
                        concepts.append({"name": text, "source": "f10"})
        
        return concepts[:10]
        
    except Exception as e:
        return []


def get_stock_name(stock_code):
    """
    获取股票名称
    """
    try:
        url = f"https://basic.10jqka.com.cn/{stock_code}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = "gbk"
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")
        if title:
            text = title.get_text(strip=True)
            match = re.match(r"([^(]+)\((\d+)\)", text)
            if match:
                return match.group(1).strip()
    except:
        pass
    return ""


def query_batch(stocks, min_change=5.0):
    """
    批量查询重点个股概念
    
    Args:
        stocks: 股票列表 [{"code": "300059", "change": 5.5}, ...]
        min_change: 最小涨跌幅阈值（默认 5%）
    
    Returns:
        dict: 查询结果
    """
    results = {
        "query_time": datetime.now().isoformat(),
        "total_stocks": len(stocks),
        "key_stocks": [],
        "cache_hits": 0,
        "cache_misses": 0,
        "concepts": {}
    }
    
    # 筛选重点个股（涨跌幅 >= min_change）
    key_stocks = [s for s in stocks if abs(float(s.get("change", 0))) >= min_change]
    results["key_stocks"] = [{"code": s["code"], "change": s.get("change", 0)} for s in key_stocks]
    
    print(f"重点个股：{len(key_stocks)} 只 (涨跌幅 >= {min_change}%)", file=sys.stderr)
    
    # 查询每个重点个股
    for stock in key_stocks:
        code = stock["code"]
        result = get_stock_concepts(code, use_cache=True)
        
        if "error" not in result:
            if result.get("from_cache"):
                results["cache_hits"] += 1
            else:
                results["cache_misses"] += 1
            
            # 提取概念名称列表
            concept_names = [c["name"] for c in result.get("concepts", [])]
            results["concepts"][code] = {
                "name": result.get("stock_name", ""),
                "change": stock.get("change", 0),
                "concepts": concept_names,
                "concept_count": len(concept_names),
                "from_cache": result.get("from_cache", False)
            }
        
        # 控制请求频率
        if not result.get("from_cache"):
            import time
            time.sleep(0.5)  # 非缓存查询增加延迟
    
    return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 query_concepts_batch.py <JSON 输入>")
        print("示例：python3 query_concepts_batch.py '[{\"code\":\"300059\",\"change\":5.5}]'")
        print("\n或者从 stdin 读取:")
        print("echo '[{\"code\":\"300059\",\"change\":5.5}]' | python3 query_concepts_batch.py -")
        sys.exit(1)
    
    if sys.argv[1] == "-":
        # 从 stdin 读取
        input_data = sys.stdin.read()
    else:
        input_data = sys.argv[1]
    
    try:
        stocks = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    results = query_batch(stocks)
    
    # 输出 JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    # 输出统计
    print(f"\n=== 统计 ===", file=sys.stderr)
    print(f"总股票数：{results['total_stocks']}", file=sys.stderr)
    print(f"重点个股：{len(results['key_stocks'])}", file=sys.stderr)
    print(f"缓存命中：{results['cache_hits']}", file=sys.stderr)
    print(f"缓存未命中：{results['cache_misses']}", file=sys.stderr)
    if results['cache_hits'] + results['cache_misses'] > 0:
        hit_rate = results['cache_hits'] / (results['cache_hits'] + results['cache_misses']) * 100
        print(f"缓存命中率：{hit_rate:.1f}%", file=sys.stderr)


if __name__ == "__main__":
    main()
