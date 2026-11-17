#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dlt_draw_announcement.py — 体彩中心大乐透开奖公告获取器

数据源: 中国体彩网官方API (webapi.sporttery.cn)
功能: 获取指定期号的开奖公告(销售金额/摇奖球/出球顺序/各奖级中奖/奖池/兑奖截止等)
缓存: 本地 JSON (dlt_draw_announcement.json), 避免频繁请求
容错: API不可达时回退缓存; 无缓存时返回None(报告静默跳过字幕)

作者: DLT Smart System
版本: 1.0.0 (2026-08-05)
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime
from dlt_huiniao_api import safe_urlopen  # 协议白名单校验(防 file:// / MITM)

# ── 常量 ──
API_URL = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
GAME_NO = "85"  # 大乐透
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dlt_draw_announcement.json")
CACHE_TTL_HOURS = 6  # 缓存有效期(小时), 超过则重新获取
TIMEOUT = 15  # API请求超时(秒)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.lottery.gov.cn/kj/kjlb.html?dlt',
}


def _load_cache():
    """加载本地缓存"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_cache(data):
    """保存到本地缓存"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _fetch_from_api(period=None):
    """从体彩官方API获取开奖公告
    
    Args:
        period: 指定期号(字符串如"26087"), None则获取最新一期
    
    Returns:
        dict or None: 开奖公告数据, 失败返回None
    """
    try:
        url = "{}?gameNo={}&provinceId=0&pageSize=30&isVerify=1&pageNo=1".format(API_URL, GAME_NO)
        req = urllib.request.Request(url, headers=HEADERS)
        with safe_urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        if not data.get('success'):
            return None

        value = data.get('value', {})
        items = value.get('list', [])

        if not items:
            return None

        # 如果指定期号, 找到对应的那期; 否则取最新
        if period:
            target = str(period)
            for item in items:
                if str(item.get('lotteryDrawNum', '')) == target:
                    return _parse_announcement(item)
            # 如果在最近30期里没找到, 尝试lastPoolDraw
            lpd = value.get('lastPoolDraw', {})
            if str(lpd.get('lotteryDrawNum', '')) == target:
                return _parse_announcement(lpd, is_pool_draw=True)
        else:
            # 取最新一期
            return _parse_announcement(items[0])

    except Exception as e:
        print("  [开奖公告] 官方开奖公告接口暂不可用，已自动回退本地缓存（不影响主报告）。")
        return None


def _parse_announcement(item, is_pool_draw=False):
    """解析API返回的单期数据为结构化开奖公告
    
    Args:
        item: API返回的单期数据dict
        is_pool_draw: 是否来自lastPoolDraw(字段较少)
    
    Returns:
        dict: 结构化开奖公告
    """
    result = {
        'period': str(item.get('lotteryDrawNum', '')),
        'draw_time': item.get('lotteryDrawTime', ''),
        'game_name': item.get('lotteryGameName', '超级大乐透'),
        'draw_result': item.get('lotteryDrawResult', ''),  # 排序后号码
        'unsorted_result': item.get('lotteryUnsortDrawresult', ''),  # 出球顺序
        'total_sale_amount': item.get('totalSaleAmount', ''),
        'pool_balance': item.get('poolBalance', ''),
        'pool_balance_after': item.get('poolBalanceAfterdraw', ''),
        'equipment_count': item.get('lotteryEquipmentCount', ''),
        'sale_begin': item.get('lotterySaleBeginTime', ''),
        'sale_end': item.get('lotterySaleEndtime', ''),
        'paid_begin': item.get('lotteryPaidBeginTime', ''),
        'paid_end': item.get('lotteryPaidEndTime', ''),
        'pdf_url': item.get('drawPdfUrl', ''),
        'prize_levels': [],
        'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # 解析开奖号码
    nums = result['draw_result'].split()
    if len(nums) >= 7:
        result['front'] = nums[:5]
        result['back'] = nums[5:7]
    else:
        result['front'] = []
        result['back'] = []

    # 解析出球顺序
    unsorted = result['unsorted_result'].split()
    if len(unsorted) >= 7:
        result['unsorted_front'] = unsorted[:5]
        result['unsorted_back'] = unsorted[5:7]
    else:
        result['unsorted_front'] = []
        result['unsorted_back'] = []

    # 解析各奖级
    for p in item.get('prizeLevelList', []):
        result['prize_levels'].append({
            'level': p.get('prizeLevel', ''),
            'count': p.get('stakeCount', ''),
            'amount': p.get('stakeAmount', ''),
            'total': p.get('totalPrizeamount', ''),
        })

    return result


def get_draw_announcement(period=None):
    """获取开奖公告(带缓存)
    
    Args:
        period: 期号(字符串如"26087"), None则获取最新
    
    Returns:
        dict or None: 开奖公告数据
    """
    cache = _load_cache()
    cache_key = str(period) if period else 'latest'

    # 检查缓存是否有效
    cached = cache.get(cache_key)
    if cached:
        fetched_at = cached.get('fetched_at', '')
        try:
            cached_time = datetime.strptime(fetched_at, '%Y-%m-%d %H:%M:%S')
            age_hours = (datetime.now() - cached_time).total_seconds() / 3600
            if age_hours < CACHE_TTL_HOURS:
                return cached
        except Exception:
            pass

    # 从API获取
    announcement = _fetch_from_api(period)

    if announcement:
        cache[cache_key] = announcement
        _save_cache(cache)
        return announcement

    # API失败, 回退缓存(即使过期)
    if cached:
        print("  [开奖公告] API不可达, 使用缓存(已过期)")
        return cached

    return None


def format_marquee_text(a):
    """将开奖公告格式化为滚动字幕文本
    
    Args:
        a: 开奖公告dict
    
    Returns:
        str: 适合滚动的纯文本(HTML转义后)
    """
    from html import escape

    parts = []

    # 标题
    parts.append("📢 体彩中心第{}期{}开奖公告".format(a['period'], a['game_name']))

    # 开奖日期
    if a.get('draw_time'):
        parts.append("开奖日期: {}".format(a['draw_time']))

    # 销售金额
    if a.get('total_sale_amount'):
        parts.append("本期销售金额: ¥{}".format(a['total_sale_amount']))

    # 摇奖球
    if a.get('equipment_count'):
        parts.append("使用第{}套摇奖球".format(a['equipment_count']))

    # 出球顺序
    if a.get('unsorted_front') and a.get('unsorted_back'):
        uf = ' '.join(a['unsorted_front'])
        ub = ' '.join(a['unsorted_back'])
        parts.append("出球顺序: 前区 {} | 后区 {}".format(uf, ub))

    # 开奖号码
    if a.get('front') and a.get('back'):
        f = ' '.join(a['front'])
        b = ' '.join(a['back'])
        parts.append("开奖号码: 前区 {} | 后区 {}".format(f, b))

    # 各奖级中奖情况
    for p in a.get('prize_levels', []):
        parts.append("{}: {}注 每注¥{} (合计¥{})".format(
            p['level'], p['count'], p['amount'], p['total']))

    # 奖池
    if a.get('pool_balance_after'):
        parts.append("奖池余额(滚入下期): ¥{}".format(a['pool_balance_after']))

    # 兑奖截止
    if a.get('paid_end'):
        parts.append("兑奖截止日期: {}".format(a['paid_end']))

    # 温馨提示
    parts.append("温馨提示: 彩票有风险, 购彩需理性。未成年人不得购彩兑奖。")

    # 开奖信息查询
    if a.get('pdf_url'):
        parts.append("开奖公告详情: {}".format(a['pdf_url']))

    # 用 · 分隔, 转义HTML
    text = "  ·  ".join(parts)
    return escape(text)


def generate_marquee_html(period=None):
    """生成滚动字幕HTML代码
    
    Args:
        period: 期号, None则自动取最新
    
    Returns:
        str: HTML代码(插入到报告中的<div>区块), 获取失败返回空字符串
    """
    a = get_draw_announcement(period)
    if not a:
        return ""

    text = format_marquee_text(a)

    return """
<div style="margin: 10px 0; overflow: hidden; background: linear-gradient(90deg, #0a0e27, #0d1b3e, #0a0e27); border: 1px solid #1a3a6e; border-radius: 8px; padding: 0; position: relative;">
  <div style="display: flex; align-items: center; height: 38px;">
    <span style="background: linear-gradient(135deg, #CA090A, #E84E18); color: #fff; font-size: 12px; font-weight: bold; padding: 4px 12px; border-radius: 4px 0 0 4px; white-space: nowrap; flex-shrink: 0; letter-spacing: 1px;">开奖公告</span>
    <div style="overflow: hidden; flex: 1; position: relative; height: 38px;">
      <div style="display: inline-block; white-space: nowrap; color: #aaccff; font-size: 13px; line-height: 38px; padding-left: 100%; animation: dlt-marquee {duration}s linear infinite;">
        {text}
      </div>
    </div>
  </div>
</div>
<style>
@keyframes dlt-marquee {{
  0% {{ transform: translateX(0); }}
  100% {{ transform: translateX(-100%); }}
}}
</style>
""".format(text=text, duration=max(30, len(text) // 8))


if __name__ == '__main__':
    # 测试
    print("=== 获取最新开奖公告 ===")
    a = get_draw_announcement()
    if a:
        print("期号:", a['period'])
        print("开奖日期:", a['draw_time'])
        print("销售金额:", a.get('total_sale_amount'))
        print("摇奖球:", a.get('equipment_count'))
        print("出球顺序:", a.get('unsorted_result'))
        print("开奖号码:", a.get('draw_result'))
        print("奖池余额:", a.get('pool_balance_after'))
        print("兑奖截止:", a.get('paid_end'))
        for p in a.get('prize_levels', []):
            print("  {}: {}注 x {} = {}".format(p['level'], p['count'], p['amount'], p['total']))
        print()
        print("=== 滚动字幕文本 ===")
        print(format_marquee_text(a))
    else:
        print("获取失败")
