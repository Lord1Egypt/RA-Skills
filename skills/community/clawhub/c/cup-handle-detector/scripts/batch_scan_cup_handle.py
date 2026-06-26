#!/usr/bin/env python3
"""
批量扫描杯柄形态

从SQLite数据库读取所有股票日K线数据，批量检测杯柄形态。
将符合形态的股票图表保存并生成汇总报告。
"""

import argparse
import os
import sys
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import warnings

warnings.filterwarnings('ignore')


def get_chinese_font():
    """获取中文字体，优先使用技能自带的思源黑体"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    font_path = os.path.join(skill_dir, 'assets', 'NotoSansSC-Regular.otf')
    
    if os.path.exists(font_path):
        return FontProperties(fname=font_path)
    
    system_fonts = [
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    
    for path in system_fonts:
        if os.path.exists(path):
            return FontProperties(fname=path)
    
    return None


CHINESE_FONT = get_chinese_font()
FONT_AVAILABLE = CHINESE_FONT is not None


class CupHandleDetectorFromSQLite:
    """从SQLite数据检测杯柄形态"""
    
    def __init__(self, db_path, table_name, output_dir=None):
        self.db_path = db_path
        self.table_name = table_name
        self.stock_code = table_name.replace('_', '.')
        self.output_dir = output_dir or os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', 'temp')
        self.data = None
        self.pattern_result = None
        
    def fetch_data(self):
        """从SQLite读取日K线数据"""
        conn = sqlite3.connect(self.db_path)
        
        query = f"SELECT ts_code, trade_date, open, high, low, close, vol, amount FROM {self.table_name} ORDER BY trade_date ASC"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return None
        
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
        self.data = df
        return df
    
    def detect_u_shape(self, prices, window_size=30):
        """检测U型底部"""
        if len(prices) < window_size:
            return 0, None
        
        bottom_idx = np.argmin(prices)
        left_idx = max(0, bottom_idx - int(window_size * 0.15))
        right_idx = min(len(prices), bottom_idx + int(window_size * 0.15))
        
        bottom_region = prices[left_idx:right_idx]
        bottom_std = np.std(bottom_region)
        price_range = np.max(prices) - np.min(prices)
        
        flatness_score = 1 - (bottom_std / price_range) if price_range > 0 else 0
        
        def calc_slope(p):
            if len(p) < 2: return 0
            return np.polyfit(np.arange(len(p)), p, 1)[0] / (np.max(p) - np.min(p)) if np.max(p) != np.min(p) else 0
        
        left_slope = calc_slope(prices[:bottom_idx+1])
        right_slope = calc_slope(prices[bottom_idx:])
        
        slope_score = 0
        if left_slope < 0 and right_slope > 0:
            slope_score = min(abs(left_slope), abs(right_slope)) / max(abs(left_slope), abs(right_slope))
        
        return (flatness_score * 0.4 + slope_score * 0.6), bottom_idx
    
    def detect_cup(self, data, min_days=30, max_days=180, max_rim_delay_days=30):
        """
        检测杯身
        
        参数:
            max_rim_delay_days: 右杯口距离最新交易日最大天数（默认30天）
        """
        if data is None or len(data) < max_days:
            return None
        
        prices = data['close'].values
        latest_idx = len(prices) - 1  # 最新交易日索引
        best_cup = None
        best_score = 0
        
        for start_offset in range(min_days, min(len(prices) - min_days, max_days)):
            cup_end = min(start_offset + max_days, len(prices))
            candidate_prices = prices[-cup_end:-cup_end+start_offset+min_days] if cup_end < len(prices) else prices[-start_offset-min_days:]
            
            if len(candidate_prices) < min_days: continue
            
            u_score, bottom_idx = self.detect_u_shape(candidate_prices, len(candidate_prices))
            if u_score < 0.3: continue
            
            cup_high = max(candidate_prices[0], candidate_prices[-1])
            cup_low = candidate_prices[bottom_idx]
            cup_depth = (cup_high - cup_low) / cup_high
            
            # 计算右杯口索引
            right_rim_idx = len(prices) - cup_end + len(candidate_prices) - 1
            
            # 【关键约束】右杯口必须接近最新交易日
            if right_rim_idx < latest_idx - max_rim_delay_days:
                continue  # 右杯口距离最新交易日太远，跳过
            
            pre_trend_len = min(60, len(prices) - cup_end)
            if pre_trend_len > 10:
                pre_prices = prices[-cup_end-pre_trend_len:-cup_end]
                pre_gain = (max(pre_prices) - pre_prices[0]) / pre_prices[0]
                
                if pre_gain < 0.3: continue
                if cup_depth < 0.1 or cup_depth > 0.5: continue
                
                score = u_score * 0.4 + (0.5 if 0.15 <= cup_depth <= 0.35 else 0.2) * 0.3 + (pre_gain / 2) * 0.3
                
                if score > best_score:
                    best_score = score
                    best_cup = {
                        'left_rim_idx': len(prices) - cup_end,
                        'bottom_idx': len(prices) - cup_end + bottom_idx,
                        'right_rim_idx': right_rim_idx,
                        'cup_depth': cup_depth,
                        'u_score': u_score,
                        'pre_gain': pre_gain,
                        'score': score,
                        'rim_distance_to_latest': latest_idx - right_rim_idx
                    }
        
        return best_cup
    
    def detect_handle(self, data, cup_info, min_days=5, max_days=30, max_delay_days=5):
        """
        检测把手
        
        参数:
            max_delay_days: 把手结束点距离最新交易日最大天数（默认5天）
            设为0表示把手必须结束在最新交易日
        """
        if cup_info is None or data is None:
            return None
        
        prices = data['close'].values
        latest_idx = len(prices) - 1  # 最新交易日索引
        
        handle_start = cup_info['right_rim_idx'] + 1
        handle_end = min(handle_start + max_days, len(prices))
        
        if handle_end - handle_start < min_days: return None
        
        # 【关键约束】把手结束点必须接近最新交易日
        handle_last_idx = handle_end - 1
        if handle_last_idx < latest_idx - max_delay_days:
            return None  # 把手结束点距离最新交易日太远，不符合
        
        handle_prices = prices[handle_start:handle_end]
        
        def calc_slope(p):
            if len(p) < 2: return 0
            return np.polyfit(np.arange(len(p)), p, 1)[0] / (np.max(p) - np.min(p)) if np.max(p) != np.min(p) else 0
        
        handle_slope = calc_slope(handle_prices)
        if handle_slope > 0.1: return None
        
        handle_depth = (max(handle_prices) - min(handle_prices)) / max(handle_prices)
        if handle_depth > cup_info['cup_depth'] / 3: return None
        if min(handle_prices) < prices[cup_info['bottom_idx']]: return None
        
        vol_ratio = np.mean(data['vol'].values[handle_start:handle_end]) / np.mean(data['vol'].values[cup_info['left_rim_idx']:cup_info['right_rim_idx']+1])
        
        score = (1 - vol_ratio if vol_ratio < 1 else 0) * 0.3 + (1 - handle_depth / (cup_info['cup_depth'] / 3)) * 0.4 + (1 if handle_slope < 0 else 0.5) * 0.3
        
        return {
            'start_idx': handle_start,
            'end_idx': handle_end - 1,
            'handle_depth': handle_depth,
            'handle_slope': handle_slope,
            'vol_ratio': vol_ratio,
            'score': score,
        }
    
    def detect_pattern(self):
        """综合检测杯柄形态"""
        if self.data is None:
            return {'detected': False, 'reason': '数据未加载'}
        
        cup_info = self.detect_cup(self.data)
        if cup_info is None:
            return {'detected': False, 'reason': '未检测到符合条件的杯身'}
        
        handle_info = self.detect_handle(self.data, cup_info)
        if handle_info is None:
            return {'detected': False, 'reason': '未检测到符合条件的把手'}
        
        prices = self.data['close'].values
        breakout_level = prices[cup_info['right_rim_idx']]
        latest_price = prices[-1]
        
        breakout_signal = latest_price >= breakout_level * 0.95
        
        volumes = self.data['vol'].values
        vol_breakout = np.mean(volumes[-5:]) > np.mean(volumes[cup_info['left_rim_idx']:handle_info['end_idx']]) * 1.5
        
        total_score = cup_info['score'] * 0.4 + handle_info['score'] * 0.3 + (1 if breakout_signal else 0) * 0.2 + (1 if vol_breakout else 0) * 0.1
        
        self.pattern_result = {
            'detected': True,
            'cup': cup_info,
            'handle': handle_info,
            'breakout_signal': breakout_signal,
            'total_score': total_score,
            'breakout_level': breakout_level,
            'latest_price': latest_price
        }
        return self.pattern_result
    
    def generate_chart(self, save_path=None):
        """生成杯柄形态识别示意图（含轮廓线）"""
        if self.pattern_result is None or not self.pattern_result['detected']:
            return None
        if self.data is None:
            return None
        
        cup = self.pattern_result['cup']
        handle = self.pattern_result['handle']
        
        df = self.data.copy()
        one_year_ago = df['trade_date'].max() - timedelta(days=365)
        df_display = df[df['trade_date'] >= one_year_ago].copy()
        offset = len(df) - len(df_display)
        display_len = len(df_display)
        
        # 标签
        labels = {
            'left': '左杯口' if FONT_AVAILABLE else 'Left Rim',
            'bottom': '杯底' if FONT_AVAILABLE else 'Cup Bottom',
            'right': '右杯口' if FONT_AVAILABLE else 'Right Rim',
            'handle': '把手' if FONT_AVAILABLE else 'Handle',
            'neckline': '颈线' if FONT_AVAILABLE else 'Neckline',
            'cup_outline': '杯身轮廓' if FONT_AVAILABLE else 'Cup Outline',
            'handle_outline': '把手轮廓' if FONT_AVAILABLE else 'Handle Outline',
            'price': '价格' if FONT_AVAILABLE else 'Price',
            'volume': '成交量' if FONT_AVAILABLE else 'Volume',
            'date': '日期' if FONT_AVAILABLE else 'Date',
            'title': '杯柄形态识别' if FONT_AVAILABLE else 'Cup and Handle Pattern',
        }
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # 蜡烛图
        width = 0.6
        width2 = 0.1
        
        up = df_display[df_display['close'] >= df_display['open']]
        down = df_display[df_display['close'] < df_display['open']]
        
        ax1.bar(up['trade_date'], up['close'] - up['open'], width, bottom=up['open'], color='red')
        ax1.bar(up['trade_date'], up['high'] - up['close'], width2, bottom=up['close'], color='red')
        ax1.bar(up['trade_date'], up['low'] - up['open'], width2, bottom=up['open'], color='red')
        
        ax1.bar(down['trade_date'], down['close'] - down['open'], width, bottom=down['open'], color='green')
        ax1.bar(down['trade_date'], down['high'] - down['open'], width2, bottom=down['open'], color='green')
        ax1.bar(down['trade_date'], down['low'] - down['close'], width2, bottom=down['close'], color='green')
        
        ax1.grid(True, alpha=0.3)
        
        # 调整索引
        cup_left_idx = cup['left_rim_idx'] - offset
        cup_bottom_idx = cup['bottom_idx'] - offset
        cup_right_idx = cup['right_rim_idx'] - offset
        handle_start_idx = handle['start_idx'] - offset
        handle_end_idx = handle['end_idx'] - offset
        
        # 绘制杯柄轮廓线（分段绘制，处理部分超出范围的情况）
        outline_drawn = False
        
        # 绘制杯身轮廓（蓝色U型）- 从可见部分开始
        if 0 <= cup_right_idx < display_len:
            right_rim_date = df_display.iloc[cup_right_idx]['trade_date']
            right_rim_price = df_display.iloc[cup_right_idx]['close']
            
            # 如果杯底在范围内，绘制杯底到右杯口
            if 0 <= cup_bottom_idx < display_len:
                bottom_date = df_display.iloc[cup_bottom_idx]['trade_date']
                bottom_price = df_display.iloc[cup_bottom_idx]['close']
                
                ax1.plot([bottom_date, right_rim_date], [bottom_price, right_rim_price], 
                         color='#1E90FF', linewidth=3, linestyle='-', label=labels['cup_outline'])
                outline_drawn = True
                
                ax1.scatter([bottom_date, right_rim_date], [bottom_price, right_rim_price],
                            color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
                ax1.text(bottom_date, bottom_price - 3, labels['bottom'], fontsize=12, color='green', ha='center', weight='bold')
                
                # 如果左杯口也在范围内，绘制完整杯身
                if 0 <= cup_left_idx < display_len:
                    left_rim_date = df_display.iloc[cup_left_idx]['trade_date']
                    left_rim_price = df_display.iloc[cup_left_idx]['close']
                    ax1.plot([left_rim_date, bottom_date], [left_rim_price, bottom_price], 
                             color='#1E90FF', linewidth=3, linestyle='-')
                    ax1.scatter([left_rim_date], [left_rim_price],
                                color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
                    ax1.text(left_rim_date, left_rim_price + 2, labels['left'], fontsize=12, color='#1E90FF', ha='center', weight='bold')
            
            ax1.scatter([right_rim_date], [right_rim_price],
                        color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
            ax1.text(right_rim_date, right_rim_price + 2, labels['right'], fontsize=12, color='#1E90FF', ha='center', weight='bold')
        
        # 把手轮廓线（橙色）
        if 0 <= handle_start_idx < display_len and 0 <= handle_end_idx < display_len:
            handle_prices = df_display.iloc[handle_start_idx:handle_end_idx+1]['close'].values
            
            handle_high_idx = np.argmax(handle_prices)
            handle_low_idx = np.argmin(handle_prices)
            
            handle_high_date = df_display.iloc[handle_start_idx + handle_high_idx]['trade_date']
            handle_high_price = handle_prices[handle_high_idx]
            
            handle_low_date = df_display.iloc[handle_start_idx + handle_low_idx]['trade_date']
            handle_low_price = handle_prices[handle_low_idx]
            
            handle_end_date = df_display.iloc[handle_end_idx]['trade_date']
            handle_end_price = df_display.iloc[handle_end_idx]['close']
            
            # 连接右杯口到把手起点
            if 0 <= cup_right_idx < display_len:
                right_rim_date = df_display.iloc[cup_right_idx]['trade_date']
                right_rim_price = df_display.iloc[cup_right_idx]['close']
                ax1.plot([right_rim_date, handle_high_date], [right_rim_price, handle_high_price],
                         color='#FF8C00', linewidth=3, linestyle='-', label=labels['handle_outline'])
            else:
                ax1.plot([handle_high_date, handle_low_date], [handle_high_price, handle_low_price],
                         color='#FF8C00', linewidth=3, linestyle='-', label=labels['handle_outline'])
            
            ax1.plot([handle_high_date, handle_low_date], [handle_high_price, handle_low_price],
                     color='#FF8C00', linewidth=3, linestyle='-')
            ax1.plot([handle_low_date, handle_end_date], [handle_low_price, handle_end_price],
                     color='#FF8C00', linewidth=3, linestyle='-')
            
            ax1.scatter([handle_high_date, handle_low_date], 
                        [handle_high_price, handle_low_price],
                        color='#FF8C00', s=100, zorder=5, edgecolors='white', linewidths=2)
            ax1.text(handle_high_date, handle_high_price + 1.5, labels['handle'], fontsize=12, color='#FF8C00', ha='center', weight='bold')
            outline_drawn = True
        
        # 颈线
        ax1.hlines(self.pattern_result['breakout_level'], 
                   df_display['trade_date'].min(), df_display['trade_date'].max(),
                   colors='red', linestyles='--', linewidth=2.5, label=labels['neckline'])
        
        # 成交量
        colors = ['red' if c >= o else 'green' for c, o in zip(df_display['close'], df_display['open'])]
        ax2.bar(df_display['trade_date'], df_display['vol'], width=0.6, color=colors, alpha=0.7)
        ax2.grid(True, alpha=0.3)
        
        # 标签
        ax1.set_title(f'{self.stock_code} - {labels["title"]}\nScore: {self.pattern_result["total_score"]:.2f}',
                      fontsize=14, fontweight='bold')
        ax1.set_ylabel(labels['price'], fontsize=12)
        ax2.set_ylabel(labels['volume'], fontsize=12)
        ax2.set_xlabel(labels['date'], fontsize=12)
        
        # 日期格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        locator = mdates.AutoDateLocator()
        locator.intervald[mdates.DAILY] = [7, 14, 21]
        ax1.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_locator(locator)
        
        plt.xticks(rotation=45, ha='right')
        ax1.legend(loc='upper left', fontsize=11)
        
        plt.tight_layout()
        
        if save_path is None:
            os.makedirs(self.output_dir, exist_ok=True)
            save_path = os.path.join(self.output_dir, f'cup_handle_{self.stock_code}.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return save_path


def batch_scan(db_path, output_dir, report_path=None):
    """批量扫描所有股票"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    conn.close()
    
    print(f"共发现 {len(tables)} 只股票")
    
    matched_stocks = []
    os.makedirs(output_dir, exist_ok=True)
    
    for i, table_name in enumerate(tables, 1):
        stock_code = table_name.replace('_', '.')
        
        print(f"[{i}/{len(tables)}] 正在扫描 {stock_code}...")
        
        try:
            detector = CupHandleDetectorFromSQLite(db_path, table_name, output_dir)
            detector.fetch_data()
            
            if detector.data is None or len(detector.data) < 180:
                continue
            
            result = detector.detect_pattern()
            
            if result['detected']:
                print(f"  ✓ 检测到杯柄形态！评分: {result['total_score']:.2f}")
                
                chart_path = detector.generate_chart()
                
                matched_stocks.append({
                    'code': stock_code,
                    'score': result['total_score'],
                    'cup_depth': result['cup']['cup_depth'],
                    'pre_gain': result['cup']['pre_gain'],
                    'latest_price': result['latest_price'],
                    'breakout_level': result['breakout_level'],
                    'breakout_signal': result['breakout_signal'],
                    'chart_path': chart_path
                })
                
        except Exception as e:
            continue
    
    if report_path and matched_stocks:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 杯柄形态扫描结果\n\n")
            f.write(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"扫描股票数: {len(tables)}\n")
            f.write(f"符合杯柄形态: {len(matched_stocks)}\n\n")
            
            for stock in sorted(matched_stocks, key=lambda x: x['score'], reverse=True):
                f.write(f"- **{stock['code']}**: 评分 {stock['score']:.2f}, 当前价 {stock['latest_price']:.2f}, 突破位 {stock['breakout_level']:.2f}\n")
    
    return matched_stocks


def main():
    parser = argparse.ArgumentParser(description='批量扫描杯柄形态')
    parser.add_argument('--db', required=True, help='SQLite数据库路径')
    parser.add_argument('--output-dir', default=os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', 'temp'),
                        help='图表输出目录')
    parser.add_argument('--report', default=None, help='报告输出路径')
    
    args = parser.parse_args()
    
    db_path = os.path.expanduser(args.db)
    output_dir = os.path.expanduser(args.output_dir)
    report_path = args.report or os.path.join(output_dir, 'cup_handle_scan_report.md')
    
    print("=" * 50)
    print("杯柄形态批量扫描")
    print("=" * 50)
    
    matched_stocks = batch_scan(db_path, output_dir, report_path)
    
    print("\n" + "=" * 50)
    print("扫描完成！")
    print(f"符合杯柄形态: {len(matched_stocks)} 只")
    print("=" * 50)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())