"""
大乐透数据源 - huiniao API
免费无限制，支持HTTPS，返回JSON
API: https://api.huiniao.top/interface/home/lotteryHistory?type=dlt&page=1&limit=100
"""
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
from datetime import datetime

# 协议白名单：仅允许 http/https，拒绝 file:/ftp:/data: 等危险协议（修复 bandit B310 + 防 MITM/file:// 误用）
_ALLOWED_SCHEMES = ('http', 'https')


def safe_urlopen(req, timeout=15):
    """带协议白名单的 urlopen：仅允许 http/https，拒绝 file:/ftp:/data: 等危险协议。

    修复 bandit B310（Audit url open for permitted schemes），并对抗传输层 MITM。
    传入 Request 或裸 URL 均可；超时沿用调用方设定。
    """
    url = req.full_url if hasattr(req, 'full_url') else str(req)
    scheme = urlparse(url).scheme.lower()
    if scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"拒绝不安全协议 '{scheme}': {url}")
    return urllib.request.urlopen(req, timeout=timeout)  # nosec B310  # 上方已校验 scheme ∈ {http,https}


def fetch_huiniao_dlt(page=1, limit=100):
    """从huiniao API获取大乐透历史数据
    
    Args:
        page: 页码，从1开始
        limit: 每页数量，最大100
    
    Returns:
        list of dict: [{period, date, front:[5], back:[2]}, ...]
    """
    url = f"https://api.huiniao.top/interface/home/lotteryHistory?type=dlt&page={page}&limit={limit}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    with safe_urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    if data.get('code') != 1:
        raise ValueError(f"API返回错误: {data.get('info')}")
    
    items = data['data']['data']['list']
    results = []
    
    for item in items:
        front = [int(item['one']), int(item['two']), int(item['three']), 
                 int(item['four']), int(item['five'])]
        back = [int(item['six']), int(item['seven'])]
        results.append({
            'period': item['code'],
            'date': item['day'],
            'front': front,
            'back': back,
            'open_time': item.get('open_time', '')
        })
    
    return results


def fetch_all_huiniao(total_pages=None):
    """获取全部大乐透历史数据
    
    Args:
        total_pages: 总页数，None则自动获取
    
    Returns:
        list: 全部历史数据，按期号升序
    """
    if total_pages is None:
        # 先获取第一页拿到总数
        first_batch = fetch_huiniao_dlt(page=1, limit=100)
        # 获取总页数
        url = "https://api.huiniao.top/interface/home/lotteryHistory?type=dlt&page=1&limit=100"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with safe_urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        total_pages = int(data['data']['data']['totalPage'])
        print(f"  总页数: {total_pages}, 总记录: {data['data']['data']['totalCount']}")
        
        all_data = list(first_batch)
        for p in range(2, total_pages + 1):
            batch = fetch_huiniao_dlt(page=p, limit=100)
            all_data.extend(batch)
            if p % 10 == 0:
                print(f"  已获取 {p}/{total_pages} 页, {len(all_data)} 期")
    else:
        all_data = []
        for p in range(1, total_pages + 1):
            batch = fetch_huiniao_dlt(page=p, limit=100)
            all_data.extend(batch)
    
    # 按期号升序排序
    all_data.sort(key=lambda x: x['period'])
    return all_data


def fetch_latest_huiniao(limit=20):
    """获取最新N期数据（用于增量更新校验）
    
    Args:
        limit: 获取期数
    
    Returns:
        list: 最新N期数据
    """
    data = fetch_huiniao_dlt(page=1, limit=limit)
    data.sort(key=lambda x: x['period'])
    return data


def merge_huiniao_with_existing(existing_data, new_data):
    """合并huiniao数据与现有数据，保留更完整的
    
    Args:
        existing_data: 现有数据列表
        new_data: huiniao新数据列表
    
    Returns:
        list: 合并后的数据
    """
    existing_periods = {d['period'] for d in existing_data}
    new_periods = {d['period'] for d in new_data}
    
    # 找出新数据中已有的期
    merged = list(existing_data)
    added = 0
    for item in new_data:
        if item['period'] not in existing_periods:
            merged.append(item)
            added += 1
    
    # 按期号排序
    merged.sort(key=lambda x: x['period'])
    
    if added > 0:
        print(f"  huiniao新增 {added} 期数据")
    else:
        print(f"  huiniao数据与现有数据一致，无新增")
    
    return merged


if __name__ == '__main__':
    print("测试huiniao API...")
    latest = fetch_latest_huiniao(limit=5)
    for item in latest:
        print(f"  {item['period']} ({item['date']}): 前区={item['front']} 后区={item['back']}")
    print(f"\n最新期号: {latest[-1]['period']}")
    print(f"总记录数(API): ", end='')
    
    # 获取总数
    url = "https://api.huiniao.top/interface/home/lotteryHistory?type=dlt&page=1&limit=1"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with safe_urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    print(f"{data['data']['data']['totalCount']} 期")
