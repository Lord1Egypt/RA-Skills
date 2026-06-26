#!/usr/bin/env python3
"""
杯柄形态（Cup and Handle）识别器

功能：
1. 获取股票日线数据
2. 识别是否符合杯柄形态
3. 如果符合，生成叠加在蜡烛图上的识别示意图（含杯柄轮廓线）
4. 如果不符合，输出提示信息
"""

import argparse
import os
import sys
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


def get_font_and_labels():
    """
    获取字体和标签映射
    
    返回:
        font: FontProperties对象（如果可用）
        labels: 标签字典（中文或英文）
    """
    # 尝试加载本地字体
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    
    font_paths = [
        os.path.join(skill_dir, 'assets', 'SourceHanSansSC.ttf'),
        os.path.join(skill_dir, 'assets', 'SimHei.ttf'),
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path) and os.path.getsize(path) > 100000:
            try:
                font = FontProperties(fname=path)
                # 测试字体是否可用
                break
            except:
                continue
    
    # 标签映射（根据字体可用性选择中英文）
    use_chinese = font is not None
    
    labels = {
        'title': '杯柄形态识别示意图' if use_chinese else 'Cup and Handle Pattern',
        'left_rim': '左杯口' if use_chinese else 'Left Rim',
        'cup_bottom': '杯底' if use_chinese else 'Cup Bottom',
        'right_rim': '右杯口' if use_chinese else 'Right Rim',
        'handle': '把手' if use_chinese else 'Handle',
        'cup_outline': '杯身轮廓' if use_chinese else 'Cup Outline',
        'handle_outline': '把手轮廓' if use_chinese else 'Handle Outline',
        'neckline': '颈线（突破位）' if use_chinese else 'Neckline',
        'price': '价格' if use_chinese else 'Price',
        'volume': '成交量' if use_chinese else 'Volume',
        'date': '日期' if use_chinese else 'Date',
        'score': '形态评分' if use_chinese else 'Score',
        'features': '形态特征' if use_chinese else 'Features',
        'u_score': 'U型得分' if use_chinese else 'U-score',
        'cup_depth': '杯身深度' if use_chinese else 'Cup Depth',
        'handle_depth': '把手深度' if use_chinese else 'Handle Depth',
        'pre_gain': '前期涨幅' if use_chinese else 'Pre-trend',
        'current': '当前价' if use_chinese else 'Current',
        'breakout': '突破位' if use_chinese else 'Breakout',
        'target': '目标价' if use_chinese else 'Target',
        'ideal': '(理想15-33%)' if use_chinese else '(ideal 15-33%)',
        'limit': '(应<杯深/3)' if use_chinese else '(<cup/3)',
        'pattern_detected': '检测到杯柄形态！' if use_chinese else 'Cup and Handle detected!',
        'not_detected': '不匹配杯柄形态' if use_chinese else 'No Cup and Handle pattern',
    }
    
    return font, labels, use_chinese


# 获取字体和标签
FONT, LABELS, USE_CHINESE = get_font_and_labels()

# 尝试导入Tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False


class CupHandleDetector:
    """杯柄形态识别器"""
    
    def __init__(self, stock_code, output_dir=None):
        self.stock_code = stock_code
        self.output_dir = output_dir or os.path.join(os.path.expanduser('~'), 'temp')
        self.data = None
        self.pattern_result = None
        
    def fetch_data(self, start_date=None, end_date=None, days=365):
        """获取股票日线数据"""
        if not TUSHARE_AVAILABLE:
            raise ImportError("需要安装Tushare: pip install tushare")
            
        token = os.environ.get('TUSHARE_TOKEN')
        if not token:
            raise ValueError("需要设置环境变量 TUSHARE_TOKEN")
        
        ts.set_token(token)
        pro = ts.pro_api()
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        df = pro.daily(ts_code=self.stock_code, start_date=start_date, end_date=end_date)
        
        if df.empty:
            raise ValueError(f"未获取到股票 {self.stock_code} 的数据")
        
        df = df.sort_values('trade_date').reset_index(drop=True)
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        
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
        # handle_end - 1 是把手的最后一个索引
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
        """
        生成杯柄形态识别示意图
        - 仅显示最近一年数据
        - 绘制杯柄轮廓线
        - 自适应日期标签
        - 支持中英文标签
        """
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
        
        # 使用手动布局，避免tight_layout的字体问题
        fig = plt.figure(figsize=(14, 10))
        ax1 = fig.add_axes([0.08, 0.35, 0.88, 0.55])
        ax2 = fig.add_axes([0.08, 0.08, 0.88, 0.22])
        
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
        display_len = len(df_display)
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
                         color='#1E90FF', linewidth=3, linestyle='-', label=LABELS['cup_outline'])
                outline_drawn = True
                
                ax1.scatter([bottom_date, right_rim_date], [bottom_price, right_rim_price],
                            color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
                ax1.text(bottom_date, bottom_price - 3, LABELS['cup_bottom'], 
                         fontsize=12, color='green', fontproperties=FONT, ha='center', weight='bold')
                
                # 如果左杯口也在范围内，绘制完整杯身
                if 0 <= cup_left_idx < display_len:
                    left_rim_date = df_display.iloc[cup_left_idx]['trade_date']
                    left_rim_price = df_display.iloc[cup_left_idx]['close']
                    ax1.plot([left_rim_date, bottom_date], [left_rim_price, bottom_price], 
                             color='#1E90FF', linewidth=3, linestyle='-')
                    ax1.scatter([left_rim_date], [left_rim_price],
                                color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
                    ax1.text(left_rim_date, left_rim_price + 2, LABELS['left_rim'], 
                             fontsize=12, color='#1E90FF', fontproperties=FONT, ha='center', weight='bold')
            
            ax1.scatter([right_rim_date], [right_rim_price],
                        color='#1E90FF', s=120, zorder=5, edgecolors='white', linewidths=2)
            ax1.text(right_rim_date, right_rim_price + 2, LABELS['right_rim'], 
                     fontsize=12, color='#1E90FF', fontproperties=FONT, ha='center', weight='bold')
        
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
                         color='#FF8C00', linewidth=3, linestyle='-', label=LABELS['handle_outline'])
            else:
                ax1.plot([handle_high_date, handle_low_date], [handle_high_price, handle_low_price],
                         color='#FF8C00', linewidth=3, linestyle='-', label=LABELS['handle_outline'])
            
            ax1.plot([handle_high_date, handle_low_date], [handle_high_price, handle_low_price],
                     color='#FF8C00', linewidth=3, linestyle='-')
            ax1.plot([handle_low_date, handle_end_date], [handle_low_price, handle_end_price],
                     color='#FF8C00', linewidth=3, linestyle='-')
            
            ax1.scatter([handle_high_date, handle_low_date], 
                        [handle_high_price, handle_low_price],
                        color='#FF8C00', s=100, zorder=5, edgecolors='white', linewidths=2)
            ax1.text(handle_high_date, handle_high_price + 1.5, LABELS['handle'], 
                     fontsize=12, color='#FF8C00', fontproperties=FONT, ha='center', weight='bold')
            outline_drawn = True
        
        # 颈线（突破位）
        ax1.hlines(self.pattern_result['breakout_level'], 
                   df_display['trade_date'].min(), df_display['trade_date'].max(),
                   colors='red', linestyles='--', linewidth=2, label=LABELS['neckline'])
        
        # 成交量
        colors = ['red' if c >= o else 'green' for c, o in zip(df_display['close'], df_display['open'])]
        ax2.bar(df_display['trade_date'], df_display['vol'], width=0.6, color=colors, alpha=0.7)
        ax2.grid(True, alpha=0.3)
        
        # 标签
        ax1.set_title(f'{self.stock_code} - {LABELS["title"]}\n{LABELS["score"]}: {self.pattern_result["total_score"]:.2f}',
                      fontsize=14, fontweight='bold', fontproperties=FONT)
        ax1.set_ylabel(LABELS['price'], fontsize=12, fontproperties=FONT)
        ax2.set_ylabel(LABELS['volume'], fontsize=12, fontproperties=FONT)
        ax2.set_xlabel(LABELS['date'], fontsize=12, fontproperties=FONT)
        
        # 日期格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        locator = mdates.AutoDateLocator()
        locator.intervald[mdates.DAILY] = [7, 14, 21]
        ax1.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_locator(locator)
        
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        ax1.legend(loc='upper left', fontsize=10, prop=FONT)
        
        # 信息框
        info_items = [
            f"{LABELS['features']}:",
            f"• {LABELS['u_score']}: {cup['u_score']:.2f}",
            f"• {LABELS['cup_depth']}: {cup['cup_depth']*100:.1f}% {LABELS['ideal']}",
            f"• {LABELS['handle_depth']}: {handle['handle_depth']*100:.1f}% {LABELS['limit']}",
            f"• {LABELS['pre_gain']}: {cup['pre_gain']*100:.1f}%",
            f"• {LABELS['current']}: {self.pattern_result['latest_price']:.2f}",
            f"• {LABELS['breakout']}: {self.pattern_result['breakout_level']:.2f}",
            f"• {LABELS['target']}: {self.pattern_result['breakout_level'] + (self.pattern_result['breakout_level'] - df.iloc[cup['bottom_idx']]['close']):.2f}",
        ]
        
        ax1.text(0.02, 0.95, '\n'.join(info_items), transform=ax1.transAxes,
                 fontsize=10, verticalalignment='top', fontproperties=FONT,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='gray'))
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'cup_handle_{self.stock_code}_{timestamp}.png')
        
        os.makedirs(self.output_dir, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close()
        
        return save_path


def main():
    parser = argparse.ArgumentParser(description='杯柄形态识别器')
    parser.add_argument('stock_code', help='股票代码（如 600519.SH）')
    parser.add_argument('--output-dir', help='输出目录', 
                        default=os.path.join(os.path.expanduser('~'), 'temp'))
    parser.add_argument('--days', type=int, default=365, help='获取数据天数')
    
    args = parser.parse_args()
    
    try:
        detector = CupHandleDetector(args.stock_code, args.output_dir)
        
        print(f"正在获取 {args.stock_code} 的日线数据...")
        detector.fetch_data(days=args.days)
        
        print(f"正在检测杯柄形态...")
        result = detector.detect_pattern()
        
        if result['detected']:
            print(f"\n✓ {LABELS['pattern_detected']}")
            print(f"  - {LABELS['score']}: {result['total_score']:.2f}")
            print(f"  - {LABELS['cup_depth']}: {result['cup']['cup_depth']*100:.1f}%")
            print(f"  - {LABELS['pre_gain']}: {result['cup']['pre_gain']*100:.1f}%")
            print(f"  - {LABELS['handle_depth']}: {result['handle']['handle_depth']*100:.1f}%")
            print(f"  - {LABELS['breakout']}: {result['breakout_level']:.2f}")
            print(f"  - {LABELS['current']}: {result['latest_price']:.2f}")
            
            print(f"\n正在生成识别示意图...")
            chart_path = detector.generate_chart()
            print(f"  - 图表已保存: {chart_path}")
            
            return 0
        else:
            print(f"\n× {result['reason']}")
            print(LABELS['not_detected'])
            return 1
            
    except Exception as e:
        print(f"错误: {e}")
        return 2


if __name__ == '__main__':
    sys.exit(main())