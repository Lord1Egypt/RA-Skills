#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论核心算法 - 分型、笔、线段识别
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import requests

# 支持的股票市场类型
VALID_SECURITY_TYPES = frozenset({
    "沪A", "深A", "创业板", "科创板", "美股", "港股"
})

# 用户输入周期 → 接口周期参数
PERIOD_MAP: Dict[str, str] = {
    "日": "day",   "日线": "day", "d": "day", "daily": "day",
    "周": "week",  "周线": "week", "w": "week", "weekly": "week",
    "月": "month", "月线": "month", "m": "month", "monthly": "month",
}

# 美股交易所 → 腾讯后缀
US_EXCHANGE_SUFFIX: Dict[str, str] = {
    "NASDAQ": ".OQ",
    "NYSE":   ".N",
    "AMEX":   ".AM",
}

# A 股市场前缀
SH_PREFIXES = ("6", "9")  # 6 开头主板 / 9 开头 B 股 → 上交所

API_BASE_URLS = {
    "美股": "https://web.ifzq.gtimg.cn/appstock/app/usfqkline/get" ,
    "港股": "https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get" ,
    "A股": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get" ,
}

# K 线字段名
KLINE_COLUMNS = ["datetime", "open", "close", "high", "low", "volume"]

REQUEST_TIMEOUT = 10  # 秒

HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

class ChanLunCore:
    """缠论核心算法类"""
    
    def __init__(self, df: pd.DataFrame):
        """
        初始化缠论分析器
        
        Args:
            df: DataFrame，包含 columns: ['open', 'high', 'low', 'close', 'volume']
        """
        self.df = df.copy()
        self.df = self.df.reset_index(drop=True)
        self.processed_klines = self._process_klines()
        self.fractals = {'tops': [], 'bottoms': []}
        self.strokes = []
        self.segments = []
    
    def _process_klines(self) -> pd.DataFrame:
        """K 线包含处理"""
        df = self.df.copy()
        # 使用栈来保存处理后的K线
        processed = []
        
        for i in range(len(df)):
            curr = df.iloc[i].copy()
            curr['index_original'] = i
            processed.append(curr)
            
            # 只要栈里至少有两根K线，就持续检查是否需要合并
            while len(processed) >= 2:
                k2 = processed[-1]  # 后一根 (当前K线或合并后的K线)
                k1 = processed[-2]  # 前一根
                
                # 1. 判断包含关系 (必须双向判断)
                is_contain = (k2['high'] >= k1['high'] and k2['low'] <= k1['low']) or \
                            (k1['high'] >= k2['high'] and k1['low'] <= k2['low'])
                
                if not is_contain:
                    break  # 没有包含关系，跳出内层循环，读取下一根原始K线
                    
                # 2. 判断方向 (看 k1 前面的那根 k0)
                if len(processed) >= 3:
                    k0 = processed[-3]
                    # 缠论规则：高点高的为向上，高点相同的看低点，低点高的为向上
                    if k1['high'] > k0['high']:
                        direction = 1  # 向上
                    elif k1['high'] < k0['high']:
                        direction = -1 # 向下
                    else:
                        direction = 1 if k1['low'] > k0['low'] else -1
                else:
                    # 只有最前面两根K线发生包含，没有K0作为参考
                    # 此时默认按这两根K线的相对关系定方向（取高的方向）
                    if k1['high'] > k2['high']:
                        direction = 1
                    elif k1['high'] < k2['high']:
                        direction = -1
                    else:
                        direction = 1 if k1['low'] > k2['low'] else -1
                
                # 3. 根据方向进行合并
                if direction == 1:  # 向上包含：取高高，取低高
                    new_high = max(k1['high'], k2['high'])
                    new_low = max(k1['low'], k2['low'])
                    new_index=k1['index_original'] if k1['high'] > k2['high'] else k2['index_original']
                    new_date=k1['datetime'] if k1['high'] > k2['high'] else k2['datetime']
                else:               # 向下包含：取低高，取低低
                    new_high = min(k1['high'], k2['high'])
                    new_low = min(k1['low'], k2['low'])
                    new_index=k1['index_original'] if k1['low'] < k2['low'] else k2['index_original']
                    new_date=k1['datetime'] if k1['low'] < k2['low'] else k2['datetime']
                    
                # 4. 生成合并后的新K线
                # 注意：缠论并没有严格规定合并后K线的 Open/Close 怎么取
                # 行业通用标准：Open取前一根(k1)，Close取后一根(k2)，时间取后一根，成交量相加
                merged_kline = pd.Series({
                    'open': k1['open'],
                    'high': new_high,
                    'low': new_low,
                    'close': k2['close'],
                    'volume': k1['volume'] + k2['volume'],
                    #'datetime': k2.get('datetime', k1.get('datetime')),
                    #'index_original': k2['index_original'] # 记录最终合并到的原始索引
                    'datetime': new_date,
                    'index_original': new_index # 记录最终合并到的原始索引
                })
                
                # 弹出原来的两根，压入合并后的新K线
                processed.pop()
                processed.pop()
                processed.append(merged_kline)

        return pd.DataFrame(processed).reset_index(drop=True)
    
    def identify_fractals(self) -> Dict:
        """识别顶底分型"""
        klines = self.processed_klines
        
        tops = []
        bottoms = []
        
        for i in range(1, len(klines) - 1):
            prev = klines.iloc[i-1]
            curr = klines.iloc[i]
            next_k = klines.iloc[i+1]
            
            # 顶分型判断
            if (curr['high'] > prev['high'] and 
                curr['high'] > next_k['high'] and
                curr['low'] > prev['low'] and
                curr['low'] > next_k['low']):
                tops.append({
                    'index': i,
                    'price': curr['high'],
                    'low': curr['low'],
                    'date': curr.get('datetime', i),
                    'kline': curr['index_original']
                })
            
            # 底分型判断
            elif (curr['low'] < prev['low'] and 
                  curr['low'] < next_k['low'] and
                  curr['high'] < prev['high'] and
                  curr['high'] < next_k['high']):
                bottoms.append({
                    'index': i,
                    'price': curr['low'],
                    'high': curr['high'],
                    'date': curr.get('datetime', i),
                    'kline': curr['index_original']
                })
        
        self.fractals = {'tops': tops, 'bottoms': bottoms}
        return self.fractals

    def identify_strokes(self) -> List[Dict]:
        if not self.fractals['tops'] or not self.fractals['bottoms']:
            self.identify_fractals()
        
        tops = self.fractals['tops']
        bottoms = self.fractals['bottoms']
        
        if not tops or not bottoms:
            return []

        # ==========================================
        # 第一步：将顶底分型合并为一个按时间顺序排列的事件列表
        # ==========================================
        events = []
        for t in tops: events.append({**t, 'type': 'top'})
        for b in bottoms: events.append({**b, 'type': 'bottom'})
        events.sort(key=lambda x: x['index'])

        # ==========================================
        # 第二步：Parse2 核心逻辑 - 化简上下上/下上下
        # ==========================================
        changed = True
        while changed:
            changed = False
            i = 0
            # 至少需要4个点才能构成：点1 -> 点2 -> 点3 -> 点4
            while i <= len(events) - 4:
                e1, e2, e3, e4 = events[i], events[i+1], events[i+2], events[i+3]
                
                # 必须是交替的顶底结构：顶底顶底 或 底顶底顶
                if e1['type'] == e3['type'] and e2['type'] == e4['type'] and e1['type'] != e2['type']:
                    
                    # ---- 高点化简：底1 -> 顶2 -> 底3 -> 顶4 （整体上升趋势） ----
                    if e1['type'] == 'bottom' and e4['price'] >= e2['price'] and e3['price'] > e1['price']:
                        # 因为K线已处理过包含关系，直接用索引差值计算跨度
                        d1 = e2['index'] - e1['index']
                        d2 = e3['index'] - e2['index']
                        d3 = e4['index'] - e3['index']
                        
                        # 跨度 < 4 代表不足5根K线
                        if d1 < 4 or d2 < 4 or d3 < 4:
                            del events[i+1] # 删掉顶2
                            del events[i+1] # 删掉底3 (原i+2因前移变成i+1)
                            changed = True
                            continue # 发生化简，原地重新检查
                    
                    # ---- 低点化简：顶1 -> 底2 -> 顶3 -> 底4 （整体下降趋势） ----
                    elif e1['type'] == 'top' and e4['price'] <= e2['price'] and e3['price'] < e1['price']:
                        d1 = e2['index'] - e1['index']
                        d2 = e3['index'] - e2['index']
                        d3 = e4['index'] - e3['index']
                        
                        if d1 < 4 or d2 < 4 or d3 < 4:
                            del events[i+1] # 删掉底2
                            del events[i+1] # 删掉顶3
                            changed = True
                            continue
                
                i += 1 # 未发生化简，检查下一个四点结构

        # ==========================================
        # 第三步：根据化简后的 events 序列，生成笔字典
        # ==========================================
        strokes = []
        for i in range(len(events) - 1):
            start_e = events[i]
            end_e = events[i+1]
            
            direction = 'down' if start_e['type'] == 'top' else 'up'
            stroke = {
                'direction': direction,
                'start': start_e['index'],
                'end': end_e['index'],
                'start_price': start_e['price'],
                'end_price': end_e['price'],
                'height': start_e['price'] - end_e['price'] if direction == 'down' else end_e['price'] - start_e['price'],
                'klines': end_e.get('kline') - start_e.get('kline')-1,
                'kline_start': start_e.get('kline'),
                'kline_end': end_e.get('kline')
            }
            strokes.append(stroke)
            
        self.strokes = strokes
        return strokes

    def identify_segments(self) -> List[Dict]:
        """
        识别线段（基于笔的重叠与延伸修正版）
        """
        if not self.strokes:
            self.identify_strokes()
        
        if len(self.strokes) < 3:
            return []

        # ================= 1. 笔格式转换 =================
        ref_strokes = []
        if self.strokes:
            # 将第一笔的起点构建为顶和底或者底和顶的参考笔，这样在后续的线段识别中可以处理第一个线段的起点
            first_s = self.strokes[0]
            # 如果第一笔是向上，则起点是底('d')；如果是向下，起点是顶('g')
            start_fx = 'g' if first_s['direction'] == 'up' else 'd'
            # 兼容获取起点价格（如果你的 stroke 字典里没有 start_price，请用 high/low 替代）
            start_price = first_s.get('start_price', first_s.get('low') if start_fx == 'd' else first_s.get('high'))
            
            ref_strokes.append({
                'dt': first_s['start'],
                'fx_mark': start_fx,
                'bi': start_price
            })
            # 如果第一笔是向上，则起点是底('d')；如果是向下，起点是顶('g')
            start_fx = 'd' if first_s['direction'] == 'up' else 'g'
            # 兼容获取起点价格（如果你的 stroke 字典里没有 start_price，请用 high/low 替代）
            start_price = first_s.get('start_price', first_s.get('low') if start_fx == 'd' else first_s.get('high'))
            
            ref_strokes.append({
                'dt': first_s['start'],
                'fx_mark': start_fx,
                'bi': start_price
            })

        for s in self.strokes:
            ref_strokes.append({
                'dt': s['end'],  
                'fx_mark': 'g' if s['direction'] == 'up' else 'd',  
                'bi': s['end_price']
            })

        end_s = ref_strokes[-1]
        end_fx = 'd' if end_s['fx_mark'] == 'g' else 'g'
        ref_strokes.append({
            'dt': end_s['dt'],
            'fx_mark': end_fx,
            'bi': end_s['bi']
        })
        
        # ================= 2. 阶段1：获取潜在线段端点 =================
        potential_xd = self._get_potential_xd(ref_strokes)
        
        # 强制将首尾笔的端点加入候选，防止首部/尾部线段起点丢失
        start_point = ref_strokes[0]
        end_point = ref_strokes[-1]
        
        all_xd_candidates = potential_xd
        #all_xd_candidates = [start_point] + potential_xd + [end_point]
        
        # 去重并按时间排序
        seen = set()
        unique_candidates = []
        for x in all_xd_candidates:
            if x['dt'] not in seen:
                seen.add(x['dt'])
                unique_candidates.append(x)
        unique_candidates = sorted(unique_candidates, key=lambda x: x['dt'])
        
        if len(unique_candidates) < 2:
            return []

        # ================= 【核心修复 2】根据 unique_candidates 构建 raw_xd_list =================
        # 严格保证 raw_xd_list 从首个元素开始就是顶底交替的
        raw_xd_list = [unique_candidates[0]]
        for xp in unique_candidates[1:]:
            last_xd = raw_xd_list[-1]
            if last_xd['fx_mark'] == xp['fx_mark']:
                # 同向取极值：顶取最高，底取最低
                if (last_xd['fx_mark'] == 'd' and last_xd['bi'] > xp['bi']) or \
                   (last_xd['fx_mark'] == 'g' and last_xd['bi'] < xp['bi']):
                    raw_xd_list[-1] = xp
            else:
                bi_inside = [x for x in ref_strokes if last_xd['dt'] <= x['dt'] <= xp['dt']]
                if len(bi_inside) >= 4:  # 缠论线段要求至少3笔（即4个端点）
                    raw_xd_list.append(xp)

        if len(raw_xd_list) < 2:
            return []

        # ================= 3. 阶段2：严格验证线段端点 =================
        keep_xd_index = []
        for i in range(1, len(raw_xd_list) - 2):
            xd1 = raw_xd_list[i - 1]
            xd2 = raw_xd_list[i]
            xd3 = raw_xd_list[i + 1]
            xd4 = raw_xd_list[i + 2]

            bi_seq1 = [x for x in ref_strokes if xd2['dt'] >= x['dt'] >= xd1['dt']]
            bi_seq2 = [x for x in ref_strokes if xd3['dt'] >= x['dt'] >= xd2['dt']]
            bi_seq3 = [x for x in ref_strokes if xd4['dt'] >= x['dt'] >= xd3['dt']]

            if self._is_valid_xd(bi_seq1, bi_seq2, bi_seq3):
                keep_xd_index.append(i)

        # 处理最近一个确定的线段标记
        bi_seq3 = [] 
        if len(raw_xd_list) >= 4:
            bi_seq1 = [x for x in ref_strokes if raw_xd_list[-2]['dt'] >= x['dt'] >= raw_xd_list[-3]['dt']]
            bi_seq2 = [x for x in ref_strokes if raw_xd_list[-1]['dt'] >= x['dt'] >= raw_xd_list[-2]['dt']]
            bi_seq3 = [x for x in ref_strokes if x['dt'] >= raw_xd_list[-1]['dt']]
            if not (len(bi_seq1) == 0 or len(bi_seq2) == 0 or len(bi_seq3) == 0):
                if self._is_valid_xd(bi_seq1, bi_seq2, bi_seq3):
                    if (len(raw_xd_list) - 2) not in keep_xd_index:
                        keep_xd_index.append(len(raw_xd_list) - 2)

        if len(bi_seq3) >= 4:
            if (len(raw_xd_list) - 1) not in keep_xd_index:
                keep_xd_index.append(len(raw_xd_list) - 1)

        # ================= 【核心修复】确保首尾线段不丢失 =================
        if not keep_xd_index:
            keep_xd_index = [0]
        else:
            # 强制加入起点 0
            if 0 not in keep_xd_index:
                keep_xd_index.insert(0, 0)
        
        # 强制把所有满足“至少包含3笔”的候选端点加入列表（解决首尾未确认线段丢失问题）
        # 从前往后推，只要前一个保留点到当前点之间>=3笔，就保留当前点
        final_keep = []
        for i in range(len(raw_xd_list)):
            if not final_keep:
                final_keep.append(i)
                continue
                
            last_kept = final_keep[-1]
            # 如果是严格验证通过的，直接保留
            if i in keep_xd_index:
                final_keep.append(i)
            else:
                # 如果未通过严格验证，检查它到上一个保留点之间是否有至少3笔
                bi_inside = [x for x in ref_strokes if raw_xd_list[i]['dt'] >= x['dt'] >= raw_xd_list[last_kept]['dt']]
                if len(bi_inside) >= 4:
                    final_keep.append(i)
                    
        keep_xd_index = sorted(list(set(final_keep)))

        # 组装 final_xd_list，同向取极值去重
        final_xd = []
        for j in keep_xd_index:
            xd_point = raw_xd_list[j]
            if not final_xd:
                final_xd.append(xd_point)
            else:
                if final_xd[-1]['fx_mark'] == xd_point['fx_mark']:
                    # 同向取极值：顶取最高，底取最低
                    if (final_xd[-1]['fx_mark'] == 'd' and final_xd[-1]['bi'] > xd_point['bi']) or \
                       (final_xd[-1]['fx_mark'] == 'g' and final_xd[-1]['bi'] < xd_point['bi']):
                        final_xd[-1] = xd_point
                else:
                    final_xd.append(xd_point)

        # ================= 4. 构建 Segment 输出 =================
        segments = []
        for i in range(len(final_xd) - 1):
            xd_start = final_xd[i]
            xd_end = final_xd[i+1]

            # 线段起点找以该端点为 start 的笔（即线段的第一笔）
            start_idx = next((idx for idx, s in enumerate(self.strokes) if s['start'] == xd_start['dt']), None)
            # 线段终点找以该端点为 end 的笔（即线段的最后一笔）
            end_idx = next((idx for idx, s in enumerate(self.strokes) if s['end'] == xd_end['dt']), None)

            if start_idx is not None and end_idx is not None and end_idx >= start_idx:
                strokes_detail = self.strokes[start_idx:end_idx+1]
                direction = 'up' if xd_start['fx_mark'] == 'd' else 'down'

                segments.append({
                    'direction': direction,
                    'start': xd_start['dt'],
                    'end': xd_end['dt'],
                    'start_price': xd_start['bi'],
                    'end_price': xd_end['bi'],
                    'strokes': len(strokes_detail),
                    'strokes_detail': strokes_detail,
                    'kline_start': strokes_detail[0].get('kline_start', xd_start['dt']),
                    'kline_end': strokes_detail[-1].get('kline_end', xd_end['dt'])
                })

        self.segments = segments
        return segments
    
    # =========================================================================
    # 核心移植逻辑：特征序列构建与包含处理
    # =========================================================================
    def _seq_standardized(self, bi_seq: List[Dict]) -> List[Dict]:
        """计算标准特征序列 (移植自 analyze.py)"""
        if not bi_seq:
            return []
        
        if bi_seq[0]['fx_mark'] == 'd':
            direction = "up"
        elif bi_seq[0]['fx_mark'] == 'g':
            direction = "down"
        else:
            raise ValueError("fx_mark must be 'g' or 'd'")

        # 提取特征元素
        raw_seq = [{"start_dt": bi_seq[i]['dt'], "end_dt": bi_seq[i + 1]['dt'],
                    'high': max(bi_seq[i]['bi'], bi_seq[i + 1]['bi']),
                    'low': min(bi_seq[i]['bi'], bi_seq[i + 1]['bi'])}
                   for i in range(1, len(bi_seq), 2) if i <= len(bi_seq) - 2]

        seq = []
        for row in raw_seq:
            if not seq:
                seq.append(row)
                continue

            last = seq[-1]
            cur_h, cur_l = row['high'], row['low']
            last_h, last_l = last['high'], last['low']

            # 左包含 or 右包含
            if (cur_h <= last_h and cur_l >= last_l) or (cur_h >= last_h and cur_l <= last_l):
                seq.pop(-1)  # 有包含关系，按方向分别处理
                if direction == "up":
                    last_h = max(last_h, cur_h)
                    last_l = max(last_l, cur_l)
                elif direction == "down":
                    last_h = min(last_h, cur_h)
                    last_l = min(last_l, cur_l)
                else:
                    raise ValueError("Direction error")
                seq.append({"start_dt": last['start_dt'], "end_dt": row['end_dt'], "high": last_h, "low": last_l})
            else:
                seq.append(row)
        return seq

    # =========================================================================
    # 核心移植逻辑：线段两种情况的判定
    # =========================================================================
    def _is_valid_xd(self, bi_seq1: List[Dict], bi_seq2: List[Dict], bi_seq3: List[Dict]) -> bool:
        """判断线段标记是否有效（第二种情况判定）(移植自 analyze.py)"""
        if not bi_seq1 or not bi_seq2 or not bi_seq3:
            return False
            
        standard_bi_seq1 = self._seq_standardized(bi_seq1)
        if len(standard_bi_seq1) == 0 or len(bi_seq2) < 4:
            return False

        # 第一种情况（向上线段起始）：破坏笔未破坏前段特征序列极值
        if bi_seq2[0]['fx_mark'] == 'd' and bi_seq2[1]['bi'] >= min([x['low'] for x in standard_bi_seq1]):
            if bi_seq2[-1]['bi'] < bi_seq2[1]['bi']:
                return False

        # 第一种情况（向下线段起始）
        if bi_seq2[0]['fx_mark'] == 'g' and bi_seq2[1]['bi'] <= max([x['high'] for x in standard_bi_seq1]):
            if bi_seq2[-1]['bi'] > bi_seq2[1]['bi']:
                return False

        # 第二种情况（向上线段起始）：破坏笔破坏了前段特征序列极值
        if bi_seq2[0]['fx_mark'] == 'd' and bi_seq2[1]['bi'] < min([x['low'] for x in standard_bi_seq1]):
            bi_seq2_ext = bi_seq2 + bi_seq3[1:]  # 避免修改原列表
            standard_bi_seq2 = self._seq_standardized(bi_seq2_ext)
            if len(standard_bi_seq2) < 3:
                return False

            standard_bi_seq2_g = []
            for i in range(1, len(standard_bi_seq2) - 1):
                bi1, bi2, bi3 = standard_bi_seq2[i - 1: i + 2]
                if bi1['high'] < bi2['high'] > bi3['high']:
                    standard_bi_seq2_g.append(bi2)
                    # 特征序列顶分型完全在底分型区间，返回 False
                    if min(bi1['low'], bi2['low'], bi3['low']) < bi_seq2[0]['bi']:
                        return False
            if len(standard_bi_seq2_g) == 0:
                return False

        # 第二种情况（向下线段起始）
        if bi_seq2[0]['fx_mark'] == 'g' and bi_seq2[1]['bi'] > max([x['high'] for x in standard_bi_seq1]):
            bi_seq2_ext = bi_seq2 + bi_seq3[1:]
            standard_bi_seq2 = self._seq_standardized(bi_seq2_ext)
            if len(standard_bi_seq2) < 3:
                return False

            standard_bi_seq2_d = []
            for i in range(1, len(standard_bi_seq2) - 1):
                bi1, bi2, bi3 = standard_bi_seq2[i - 1: i + 2]
                if bi1['low'] > bi2['low'] < bi3['low']:
                    standard_bi_seq2_d.append(bi2)
                    # 特征序列的底分型在顶分型区间，返回 False
                    if max(bi1['high'], bi2['high'], bi3['high']) > bi_seq2[0]['bi']:
                        return False
            if len(standard_bi_seq2_d) == 0:
                return False

        return True

    # =========================================================================
    # 辅助逻辑：寻找潜在线段端点
    # =========================================================================
    def _get_potential_xd(self, ref_strokes: List[Dict]) -> List[Dict]:
        """获取潜在线段标记点（在顶底分型中寻找）"""
        xd_p = []
        bi_d = [x for x in ref_strokes if x['fx_mark'] == 'd']
        bi_g = [x for x in ref_strokes if x['fx_mark'] == 'g']

        for i in range(1, len(bi_d) - 1):
            d1, d2, d3 = bi_d[i - 1: i + 2]
            if d1['bi'] > d2['bi'] < d3['bi']:
                xd_p.append(d2)

        for j in range(1, len(bi_g) - 1):
            g1, g2, g3 = bi_g[j - 1: j + 2]
            if g1['bi'] < g2['bi'] > g3['bi']:
                xd_p.append(g2)

        xd_p = sorted(xd_p, key=lambda x: x['dt'], reverse=False)
        return xd_p
    
    def identify_pivots(self) -> List[Dict]:
        """
        识别中枢（基于至少 3 笔重叠，支持中枢延伸/生长）
        """
        if not self.strokes:
            self.identify_strokes()
        
        if len(self.strokes) < 3:
            return []
        
        pivots = []
        i = 0
        
        while i < len(self.strokes) - 2:
            s1 = self.strokes[i]
            s2 = self.strokes[i+1]
            s3 = self.strokes[i+2]
            
            # 1. 计算前三笔的重叠区间 (ZG: 中枢上沿, ZD: 中枢下沿)
            highs = [max(s['start_price'], s['end_price']) for s in [s1, s2, s3]]
            lows = [min(s['start_price'], s['end_price']) for s in [s1, s2, s3]]
            
            zg = min(highs) # 中枢上沿：三个笔高点的最低点
            zd = max(lows)  # 中枢下沿：三个笔低点的最高点
            
            # 2. 判断是否形成有效中枢 (ZG 必须大于 ZD)
            if zg > zd:
                # 建立中枢基础
                pivot = {
                    'start_index': s1['start'],
                    'end_index': s3['start'],
                    'high': zg,      # 中枢上沿固定不变
                    'low': zd,       # 中枢下沿固定不变
                    'strokes': [s1, s2, s3],
                    'direction': s1['direction'],
                    'kline_start': s1['kline_start'],
                    'kline_end': s3['kline_start']
                }
                
                # 3. 【核心修正】检查中枢是否向后延伸
                k = i + 3
                while k < len(self.strokes):
                    sk = self.strokes[k]
                    sk_high = max(sk['start_price'], sk['end_price'])
                    sk_low = min(sk['start_price'], sk['end_price'])
                    
                    # 缠论规则：只要后续的笔有波动区间与 ZG-ZD 有重叠，就算进入中枢（延伸）
                    # 注意：这里用 <= 和 >= 是标准的接触即算进入
                    if sk_high >= zd and sk_low <= zg:
                        # 中枢延伸！更新结束时间和包含的笔，但 ZG 和 ZD 绝对不变！
                        pivot['end_index'] = sk['start']
                        pivot['strokes'].append(sk)
                        pivot['kline_end'] = sk['kline_start']
                        k += 1
                    else:
                        # 笔走出了中枢区间，中枢结束！
                        break
                        
                pivots.append(pivot)
                
                # 4. 【关键步进】下一个中枢的起点，必须从离开当前中枢的那一笔开始算
                i = k
                
            else:
                # 没有形成3笔重叠，正常往后挪一笔
                i += 1
                
        self.pivots = pivots
        return pivots

    def get_current_trend(self) -> str:
        """判断当前走势类型"""
        if not self.strokes:
            return 'unknown'
        
        last_stroke = self.strokes[-1]
        
        # 检查是否有中枢
        pivots = self.identify_pivots()
        
        if len(pivots) >= 2:
            # 检查中枢方向
            if pivots[-1]['high'] > pivots[-2]['high'] and pivots[-1]['low'] > pivots[-2]['low']:
                return 'uptrend'
            elif pivots[-1]['high'] < pivots[-2]['high'] and pivots[-1]['low'] < pivots[-2]['low']:
                return 'downtrend'
            else:
                return 'consolidation'
        elif len(pivots) == 1:
            return 'consolidation'
        else:
            return 'uptrend' if last_stroke['direction'] == 'up' else 'downtrend'

def _safe_get_json(url: str, params: dict) -> dict:
    """发起 GET 请求并安全解析 JSON，失败时抛出 RuntimeError"""
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()  # 非 2xx 立即抛异常
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"请求失败: {e}") from e

def search_stock_code(stock_name: str) -> Optional[Dict[str, str]]:
    """通过股票名称搜索股票代码"""
    url = "https://searchapi.eastmoney.com/api/suggest/get"
    params = {"input": stock_name, "type": 14, "count": 5}

    data = _safe_get_json(url, params)
        
    items: List[dict] = (
        data.get("QuotationCodeTable", {})
            .get("Data", [])
    )
    for item in items:
        if item.get("SecurityTypeName") in VALID_SECURITY_TYPES:
            return {
                "name":   item["Name"],
                "code":   item["Code"],
                "JYS":    item["JYS"],
                "market": item["SecurityTypeName"],
            }
    return None

def _build_tencent_code(stock_code: str, stock_type: str, stock_jys: str) -> str:
    """根据市场类型拼接腾讯接口所需的股票代码"""
    if stock_type == "美股":
        suffix = US_EXCHANGE_SUFFIX.get(stock_jys, "")
        return f"us{stock_code.upper()}{suffix}"
    if stock_type == "港股":
        return f"hk{stock_code}"
    # A 股（沪A / 深A / 创业板 / 科创板）
    prefix = "sh" if stock_code.startswith(SH_PREFIXES) else "sz"
    return f"{prefix}{stock_code}"

def get_kline(stock_code: str, stock_type: str, stock_jys: str, period: str, bars: int = 500) -> pd.DataFrame:
    """使用腾讯API获取K线数据"""
    per = PERIOD_MAP.get(period, "day")
    t_code = _build_tencent_code(stock_code, stock_type, stock_jys)

    # 判断使用哪个 API（A股 / 港股 / 美股）
    market_key = stock_type if stock_type in API_BASE_URLS else "A股"
    base_url = API_BASE_URLS[market_key]

    params = {"param": f"{t_code},{per},,,{bars},qfq"}
    resp_data = _safe_get_json(base_url, params)
    
    # 逐层安全取值
    #k_data = resp_data.get("data", {}).get(t_code, {}).get(f"qfq{per}")
    temp_dict = resp_data.get("data", {}).get(t_code, {})
    k_data = temp_dict.get(f"qfq{per}") or temp_dict.get(f"{per}")
    
    if not k_data:
        raise RuntimeError(
            f"接口未返回有效K线数据（code={t_code}, period={per}）"
        )
    
    # 腾讯的API返回数据在派息日当天会多一个派息信息，需要裁剪
    k_data_trimmed = [row[:6] for row in k_data]
    
    return pd.DataFrame(k_data_trimmed, columns=KLINE_COLUMNS)

def analyze_stock(stock_code: str, period: str = 'daily', bars: int = 500) -> ChanLunCore:
    """
    分析股票
    
    Args:
        stock_code: 股票代码（如 601688）
        period: 周期（daily/weekly/monthly 等）
    
    Returns:
        ChanLunCore 分析器实例
    """
    try:
        result = search_stock_code(stock_code)
        df = get_kline(result["code"], result["market"], result["JYS"], period, bars)
    except RuntimeError as e:
        print(e)
        raise

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)

    required_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in required_cols:
        df[col]=pd.to_numeric(df[col])
    
    # 创建分析器
    analyzer = ChanLunCore(df)
    
    return analyzer
