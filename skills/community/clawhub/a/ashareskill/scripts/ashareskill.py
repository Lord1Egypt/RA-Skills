"""
AShareSkill - A股数据获取工具
功能：获取股票K线数据及完整技术指标（均线、MACD、KDJ、RSI、BOLL、CCI等）
数据源：使用BaoStock API获取真实实盘数据
"""

import baostock as bs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Union
import warnings
import argparse
import os
import sys

warnings.filterwarnings('ignore')


class AShareSkill:
    """AShareSkill - A股数据获取工具"""
    
    # K线频率映射
    FREQUENCY_MAP = {
        'd': 'd',  # 日线
        'w': 'w',  # 周线
        'm': 'm',  # 月线
        'day': 'd',
        'week': 'w',
        'month': 'm',
        '日线': 'd',
        '周线': 'w',
        '月线': 'm'
    }
    
    # 复权类型映射
    ADJUST_MAP = {
        '1': '1',  # 前复权
        '2': '2',  # 后复权
        '3': '3',  # 不复权
        'pre': '1',
        'post': '2',
        'none': '3',
        '前复权': '1',
        '后复权': '2',
        '不复权': '3'
    }
    
    def __init__(self):
        self.lg = None
        self.stock_list_cache = None
        self.stock_name_to_code = {}
        self.stock_code_to_name = {}
        self._login()
        self._init_stock_list()
    
    def _login(self):
        """登录BaoStock"""
        print("[AShareSkill] 正在登录BaoStock...")
        self.lg = bs.login()
        if self.lg.error_code != '0':
            print(f"[AShareSkill] ✗ 登录失败: {self.lg.error_msg}")
            raise ConnectionError(f"BaoStock登录失败: {self.lg.error_msg}")
        else:
            print(f"[AShareSkill] ✓ 登录成功")
    
    def _logout(self):
        """登出BaoStock"""
        if self.lg:
            bs.logout()
            print("[AShareSkill] 已登出BaoStock")
    
    def _init_stock_list(self):
        """初始化股票列表缓存"""
        try:
            print("[AShareSkill] 正在加载股票列表...")
            
            # 获取沪深A股列表
            today = datetime.now()
            stock_list = []
            
            for i in range(10):  # 尝试最近10天
                date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                rs = bs.query_all_stock(day=date_str)
                
                stock_list = []
                while (rs.error_code == '0') & rs.next():
                    stock_list.append(rs.get_row_data())
                
                if len(stock_list) > 1000:
                    print(f"[AShareSkill]   使用日期: {date_str}")
                    break
            
            self.stock_list_cache = pd.DataFrame(stock_list, columns=rs.fields)
            self._enrich_stock_info()
            print(f"[AShareSkill] ✓ 已加载 {len(self.stock_list_cache)} 只股票")
            
        except Exception as e:
            print(f"[AShareSkill] ✗ 初始化失败: {e}")
            self.stock_list_cache = pd.DataFrame()
    
    def _enrich_stock_info(self):
        """获取股票详细信息（名称、行业等）"""
        print("[AShareSkill] 正在构建股票名称映射...")
        
        if 'code_name' in self.stock_list_cache.columns:
            # 过滤有效股票代码
            stock_df = self.stock_list_cache[
                self.stock_list_cache['code'].str.match(r'^(sh\.(6|9)|sz\.(0|3|2))', na=False)
            ].copy()
            
            for _, row in stock_df.iterrows():
                name = row.get('code_name', '')
                code = row['code']
                if name and code:
                    self.stock_name_to_code[name] = code
                    self.stock_code_to_name[code] = name
            
            print(f"[AShareSkill]   ✓ 成功构建 {len(self.stock_name_to_code)} 只股票映射")
        else:
            print("[AShareSkill]   ! 股票列表中没有code_name字段，将仅支持股票代码查询")
    
    def search_stock(self, keyword: str) -> List[Dict[str, str]]:
        """
        根据关键词搜索股票
        
        Args:
            keyword: 股票名称或代码（支持模糊匹配）
            
        Returns:
            匹配的股票列表
        """
        if self.stock_list_cache is None or len(self.stock_list_cache) == 0:
            print("[AShareSkill] 股票列表未加载，重新初始化...")
            self._init_stock_list()
        
        results = []
        keyword = keyword.strip()
        keyword_upper = keyword.upper()
        
        # 精确匹配代码（支持各种格式）
        exact_code = None
        if keyword_upper.startswith(('SH.', 'SZ.')):
            exact_code = keyword_lower = keyword.lower()
        elif len(keyword) == 6 and keyword.isdigit():
            # 6位数字代码，自动添加前缀
            if keyword.startswith('6'):
                exact_code = f'sh.{keyword}'
            else:
                exact_code = f'sz.{keyword}'
        
        if exact_code:
            exact_match = self.stock_list_cache[self.stock_list_cache['code'] == exact_code]
            if len(exact_match) > 0:
                for _, row in exact_match.iterrows():
                    results.append({
                        'code': row['code'],
                        'name': row.get('code_name', 'N/A'),
                        'tradeStatus': row.get('tradeStatus', 'N/A')
                    })
                return results
        
        # 模糊匹配代码
        code_matches = self.stock_list_cache[
            self.stock_list_cache['code'].str.contains(keyword, case=False, na=False)
        ]
        for _, row in code_matches.iterrows():
            results.append({
                'code': row['code'],
                'name': row.get('code_name', 'N/A'),
                'tradeStatus': row.get('tradeStatus', 'N/A')
            })
        
        # 模糊匹配名称
        if 'code_name' in self.stock_list_cache.columns:
            name_matches = self.stock_list_cache[
                self.stock_list_cache['code_name'].str.contains(keyword, na=False)
            ]
            for _, row in name_matches.iterrows():
                if not any(r['code'] == row['code'] for r in results):
                    results.append({
                        'code': row['code'],
                        'name': row['code_name'],
                        'tradeStatus': row.get('tradeStatus', 'N/A')
                    })
        
        return results[:20]
    
    def get_stock_code(self, input_str: str) -> Optional[str]:
        """
        获取股票代码（支持自动解析名称或代码）
        
        Args:
            input_str: 输入的股票名称或代码
            
        Returns:
            股票代码或None
        """
        input_str = input_str.strip()
        
        # 先查缓存
        if input_str in self.stock_name_to_code:
            return self.stock_name_to_code[input_str]
        
        # 搜索匹配
        results = self.search_stock(input_str)
        
        if len(results) == 0:
            print(f"[AShareSkill] ✗ 未找到匹配 '{input_str}' 的股票")
            return None
        elif len(results) == 1:
            print(f"[AShareSkill] ✓ {input_str} -> {results[0]['name']} ({results[0]['code']})")
            return results[0]['code']
        else:
            print(f"[AShareSkill] ! 找到 {len(results)} 只匹配股票：")
            for i, r in enumerate(results[:10], 1):
                status = "正常" if r.get('tradeStatus') == '1' else "停牌"
                print(f"    {i}. {r['name']} ({r['code']}) [{status}]")
            print(f"[AShareSkill] 请使用更精确的名称或代码")
            return None
    
    def get_index_components(self, index_code: str) -> List[str]:
        """
        获取指数成分股列表
        
        Args:
            index_code: 指数代码（如 000905 中证500，000300 沪深300）
            
        Returns:
            成分股代码列表
        """
        # 标准化指数代码
        index_code = index_code.strip()
        if not index_code.startswith(('sh.', 'sz.')):
            if index_code.startswith('0') or index_code.startswith('3'):
                index_code = f'sz.{index_code}'
            else:
                index_code = f'sh.{index_code}'
        
        print(f"[AShareSkill] 正在获取 {index_code} 的成分股列表...")
        
        # 使用query_stock_industry或query_all_stock获取成分股
        # BaoStock没有直接的指数成分股查询，使用query_stock_industry替代
        try:
            # 获取特定日期
            today = datetime.now()
            for i in range(10):
                date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                
                # 尝试获取指数成分股
                rs = bs.query_zz500_stocks(date=date_str) if '000905' in index_code else \
                     bs.query_hs300_stocks(date=date_str) if '000300' in index_code else \
                     bs.query_sz50_stocks(date=date_str) if '000016' in index_code else None
                
                if rs is None:
                    print(f"[AShareSkill] ! 暂不支持该指数的成分股查询: {index_code}")
                    return []
                
                stocks = []
                while (rs.error_code == '0') & rs.next():
                    row = rs.get_row_data()
                    if len(row) > 1:
                        stocks.append(row[1])  # 成分股代码
                
                if len(stocks) > 0:
                    print(f"[AShareSkill]   ✓ 获取到 {len(stocks)} 只成分股（日期: {date_str}）")
                    return stocks
                    
        except Exception as e:
            print(f"[AShareSkill] ✗ 获取成分股失败: {e}")
            return []
        
        return []
    
    def resolve_stock_codes(self, stock_input: Union[str, List[str]]) -> List[str]:
        """
        解析股票输入，支持字符串（单只或多只逗号分隔）或列表
        
        Args:
            stock_input: 股票输入（字符串或列表）
            
        Returns:
            股票代码列表
        """
        if isinstance(stock_input, str):
            # 按逗号分隔
            stock_list = [s.strip() for s in stock_input.split(',')]
        elif isinstance(stock_input, (list, tuple)):
            stock_list = list(stock_input)
        else:
            stock_list = [str(stock_input)]
        
        codes = []
        for stock in stock_list:
            code = self.get_stock_code(stock)
            if code:
                codes.append(code)
        
        return codes
    
    def get_kline_data(self, 
                       stock_code: str,
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None,
                       frequency: str = 'd',
                       adjustflag: str = '3') -> pd.DataFrame:
        """
        获取单只股票的K线数据及技术指标
        
        Args:
            stock_code: 股票代码（BaoStock格式或名称）
            start_date: 开始日期 (YYYY-MM-DD)，默认一年前
            end_date: 结束日期 (YYYY-MM-DD)，默认今天
            frequency: K线频率: d(日线), w(周线), m(月线)
            adjustflag: 复权类型: 1(前复权), 2(后复权), 3(不复权)
            
        Returns:
            包含K线数据和技术指标的DataFrame
        """
        # 解析股票代码
        if not stock_code.startswith(('sh.', 'sz.', 'SH.', 'SZ.')):
            resolved_code = self.get_stock_code(stock_code)
            if not resolved_code:
                return pd.DataFrame()
            stock_code = resolved_code
        
        # 标准化频率
        freq = self.FREQUENCY_MAP.get(frequency, 'd')
        
        # 标准化复权类型
        adjust = self.ADJUST_MAP.get(adjustflag, '3')
        
        # 处理日期
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        stock_name = self.stock_code_to_name.get(stock_code, '')
        
        print(f"[AShareSkill] 正在获取 {stock_name or stock_code} 的{frequency}数据...")
        print(f"[AShareSkill]   时间范围: {start_date} ~ {end_date}")
        
        # 确保已登录
        if self.lg is None or self.lg.error_code != '0':
            self._login()
        
        # 获取K线数据
        kline_df = self._query_kline(stock_code, start_date, end_date, freq, adjust)
        if len(kline_df) == 0:
            return pd.DataFrame()
        
        # 获取技术指标
        indicators_df = self._query_indicators(stock_code, start_date, end_date, freq, adjust)
        
        # 合并数据
        result_df = kline_df.copy()
        if len(indicators_df) > 0:
            # 根据date合并
            result_df = pd.merge(result_df, indicators_df, on='date', how='left', suffixes=('', '_ind'))
            # 处理重复的列
            for col in result_df.columns:
                if col.endswith('_ind'):
                    orig_col = col[:-4]
                    if orig_col in result_df.columns:
                        result_df[orig_col] = result_df[col].combine_first(result_df[orig_col])
                        result_df.drop(columns=[col], inplace=True)
        
        # 获取估值指标
        valuation_df = self._query_valuation(stock_code, start_date, end_date)
        if len(valuation_df) > 0:
            result_df = pd.merge(result_df, valuation_df, on='date', how='left')
        
        # 添加股票信息列
        result_df.insert(0, 'code', stock_code)
        result_df.insert(1, 'name', stock_name)
        
        # 转换数值类型
        numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 
                       'turn', 'pctChg', 'peTTM', 'pbMRQ', 'psTTM', 'pcfNcfTTM',
                       'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120', 'ma250',
                       'macd_dif', 'macd_dea', 'macd',
                       'kdj_k', 'kdj_d', 'kdj_j',
                       'rsi_6', 'rsi_12', 'rsi_24',
                       'boll_upper', 'boll_middle', 'boll_lower', 'cci']
        
        for col in numeric_cols:
            if col in result_df.columns:
                result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
        
        print(f"[AShareSkill]   ✓ 获取到 {len(result_df)} 条数据")
        
        return result_df
    
    def _query_kline(self, stock_code: str, start_date: str, end_date: str, 
                     frequency: str, adjustflag: str) -> pd.DataFrame:
        """查询K线基础数据"""
        # 月线查询不支持preclose字段
        if frequency in ['w', 'm']:
            fields = "date,open,high,low,close,volume,amount,turn,pctChg"
        else:
            fields = "date,open,high,low,close,preclose,volume,amount,turn,pctChg,isST"
        
        rs = bs.query_history_k_data_plus(
            stock_code,
            fields,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        
        if rs.error_code != '0':
            print(f"[AShareSkill]   ✗ K线数据查询失败: {rs.error_msg}")
            return pd.DataFrame()
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if len(data_list) == 0:
            return pd.DataFrame()
        
        df = pd.DataFrame(data_list, columns=rs.fields)
        return df
    
    def _query_indicators(self, stock_code: str, start_date: str, end_date: str,
                          frequency: str, adjustflag: str) -> pd.DataFrame:
        """查询技术指标数据（通过K线数据计算）"""
        # 获取扩展日期范围以计算长期均线（需要更多历史数据）
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        extended_start = (start_dt - timedelta(days=400)).strftime("%Y-%m-%d")
        
        # 获取K线数据用于计算指标
        fields = "date,open,high,low,close,volume"
        rs = bs.query_history_k_data_plus(
            stock_code, fields,
            start_date=extended_start, end_date=end_date,
            frequency=frequency, adjustflag=adjustflag
        )
        
        if rs.error_code != '0':
            return pd.DataFrame()
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if len(data_list) == 0:
            return pd.DataFrame()
        
        df = pd.DataFrame(data_list, columns=rs.fields)
        df['date'] = pd.to_datetime(df['date'])
        
        # 转换数值类型
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 计算技术指标
        df = self._calculate_ma(df)      # 均线
        df = self._calculate_macd(df)    # MACD
        df = self._calculate_kdj(df)     # KDJ
        df = self._calculate_rsi(df)     # RSI
        df = self._calculate_boll(df)    # BOLL
        df = self._calculate_cci(df)     # CCI
        
        # 过滤回原始日期范围
        df = df[df['date'] >= start_date]
        
        # 转换date为字符串格式
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        return df
    
    def _calculate_ma(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算移动平均线"""
        df = df.copy()
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma30'] = df['close'].rolling(window=30).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()
        df['ma120'] = df['close'].rolling(window=120).mean()
        df['ma250'] = df['close'].rolling(window=250).mean()
        return df
    
    def _calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """计算MACD指标"""
        df = df.copy()
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        df['macd_dif'] = ema_fast - ema_slow
        df['macd_dea'] = df['macd_dif'].ewm(span=signal, adjust=False).mean()
        df['macd'] = 2 * (df['macd_dif'] - df['macd_dea'])
        return df
    
    def _calculate_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
        """计算KDJ指标"""
        df = df.copy()
        low_list = df['low'].rolling(window=n, min_periods=n).min()
        high_list = df['high'].rolling(window=n, min_periods=n).max()
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        
        df['kdj_k'] = rsv.ewm(alpha=1/m1, adjust=False).mean()
        df['kdj_d'] = df['kdj_k'].ewm(alpha=1/m2, adjust=False).mean()
        df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
        return df
    
    def _calculate_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算RSI指标"""
        df = df.copy()
        
        def calc_rsi(prices, period):
            delta = prices.diff()
            gain = delta.where(delta > 0, 0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        df['rsi_6'] = calc_rsi(df['close'], 6)
        df['rsi_12'] = calc_rsi(df['close'], 12)
        df['rsi_24'] = calc_rsi(df['close'], 24)
        return df
    
    def _calculate_boll(self, df: pd.DataFrame, n: int = 20, k: int = 2) -> pd.DataFrame:
        """计算布林带指标"""
        df = df.copy()
        df['boll_middle'] = df['close'].rolling(window=n).mean()
        std = df['close'].rolling(window=n).std()
        df['boll_upper'] = df['boll_middle'] + k * std
        df['boll_lower'] = df['boll_middle'] - k * std
        return df
    
    def _calculate_cci(self, df: pd.DataFrame, n: int = 14) -> pd.DataFrame:
        """计算CCI指标"""
        df = df.copy()
        tp = (df['high'] + df['low'] + df['close']) / 3
        ma_tp = tp.rolling(window=n).mean()
        md = tp.rolling(window=n).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
        df['cci'] = (tp - ma_tp) / (0.015 * md)
        return df
    
    def _query_valuation(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """查询估值指标"""
        rs = bs.query_history_k_data_plus(
            stock_code,
            "date,peTTM,pbMRQ,psTTM,pcfNcfTTM",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
        
        if rs.error_code != '0':
            return pd.DataFrame()
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if len(data_list) == 0:
            return pd.DataFrame()
        
        return pd.DataFrame(data_list, columns=rs.fields)
    
    def get_stock_pool_data(self,
                           stock_list: Union[str, List[str]],
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           frequency: str = 'd',
                           adjustflag: str = '3') -> pd.DataFrame:
        """
        获取股票池数据
        
        Args:
            stock_list: 股票列表（字符串逗号分隔或列表）
            start_date: 开始日期
            end_date: 结束日期
            frequency: K线频率
            adjustflag: 复权类型
            
        Returns:
            合并后的DataFrame
        """
        codes = self.resolve_stock_codes(stock_list)
        
        if len(codes) == 0:
            print("[AShareSkill] ✗ 没有有效的股票代码")
            return pd.DataFrame()
        
        print(f"[AShareSkill] 开始获取 {len(codes)} 只股票的数据...")
        print("=" * 60)
        
        all_data = []
        for i, code in enumerate(codes, 1):
            print(f"\n[AShareSkill] [{i}/{len(codes)}]")
            df = self.get_kline_data(code, start_date, end_date, frequency, adjustflag)
            if len(df) > 0:
                all_data.append(df)
        
        print("\n" + "=" * 60)
        
        if len(all_data) == 0:
            print("[AShareSkill] ✗ 未获取到任何数据")
            return pd.DataFrame()
        
        # 合并所有数据
        result = pd.concat(all_data, ignore_index=True)
        print(f"[AShareSkill] ✓ 总计获取 {len(result)} 条数据（{len(all_data)} 只股票）")
        
        return result
    
    def save_to_csv(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """
        保存数据到CSV文件
        
        Args:
            df: DataFrame数据
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if df is None or len(df) == 0:
            print("[AShareSkill] ✗ 没有数据可保存")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ashareskill_data_{timestamp}.csv"
        
        # 确保目录存在
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存数据
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"[AShareSkill] ✓ 数据已保存: {os.path.abspath(filename)}")
        print(f"[AShareSkill]   记录数: {len(df)}, 字段数: {len(df.columns)}")
        
        return os.path.abspath(filename)
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        获取数据摘要信息
        
        Args:
            df: DataFrame数据
            
        Returns:
            摘要信息字典
        """
        if df is None or len(df) == 0:
            return {}
        
        summary = {
            'record_count': len(df),
            'stock_count': df['code'].nunique() if 'code' in df.columns else 0,
            'stocks': df['code'].unique().tolist() if 'code' in df.columns else [],
            'date_range': {
                'start': df['date'].min() if 'date' in df.columns else None,
                'end': df['date'].max() if 'date' in df.columns else None
            },
            'columns': df.columns.tolist()
        }
        
        return summary


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='AShareSkill - A股数据获取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 单只股票，日线数据
  python ashareskill.py -s 600519 --start 2023-01-01 --end 2024-01-01
  
  # 股票池，周线数据
  python ashareskill.py -s "贵州茅台,中国平安,宁德时代" --start 2023-01-01 -f w
  
  # 指数成分股（中证500）月线数据
  python ashareskill.py -i 000905 --start 2024-01-01 -f m -o zz500.csv
  
  # 指定输出文件
  python ashareskill.py -s 000001 -o mydata.csv
        '''
    )
    
    parser.add_argument('-s', '--stock', 
                       help='股票名称或代码，多只股票用逗号分隔')
    parser.add_argument('-i', '--index',
                       help='指数代码，获取指数成分股（如 000905 中证500，000300 沪深300）')
    parser.add_argument('--start',
                       help='开始日期 (YYYY-MM-DD)，默认一年前')
    parser.add_argument('--end',
                       help='结束日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('-f', '--freq', default='d',
                       choices=['d', 'w', 'm', 'day', 'week', 'month'],
                       help='K线级别: d(日线), w(周线), m(月线)，默认d')
    parser.add_argument('-a', '--adjust', default='3',
                       choices=['1', '2', '3'],
                       help='复权类型: 1(前复权), 2(后复权), 3(不复权)，默认3')
    parser.add_argument('-o', '--output',
                       help='输出文件名')
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.stock and not args.index:
        parser.error('必须指定 --stock 或 --index 参数')
    
    skill = None
    try:
        # 初始化
        skill = AShareSkill()
        
        # 获取股票列表
        if args.index:
            # 获取指数成分股
            stock_codes = skill.get_index_components(args.index)
            if len(stock_codes) == 0:
                print(f"[AShareSkill] ✗ 未能获取指数 {args.index} 的成分股")
                return
            df = skill.get_stock_pool_data(
                stock_list=stock_codes,
                start_date=args.start,
                end_date=args.end,
                frequency=args.freq,
                adjustflag=args.adjust
            )
        elif ',' in args.stock:
            # 股票池
            df = skill.get_stock_pool_data(
                stock_list=args.stock,
                start_date=args.start,
                end_date=args.end,
                frequency=args.freq,
                adjustflag=args.adjust
            )
        else:
            # 单只股票
            df = skill.get_kline_data(
                stock_code=args.stock,
                start_date=args.start,
                end_date=args.end,
                frequency=args.freq,
                adjustflag=args.adjust
            )
        
        # 保存数据
        if len(df) > 0:
            skill.save_to_csv(df, args.output)
            
            # 打印摘要
            summary = skill.get_data_summary(df)
            print("\n" + "=" * 60)
            print("[AShareSkill] 数据摘要:")
            print(f"  股票数量: {summary.get('stock_count', 0)}")
            print(f"  记录数量: {summary.get('record_count', 0)}")
            print(f"  日期范围: {summary.get('date_range', {}).get('start', 'N/A')} ~ {summary.get('date_range', {}).get('end', 'N/A')}")
            print(f"  字段列表: {', '.join(summary.get('columns', [])[:5])}...")
            print("=" * 60)
        else:
            print("[AShareSkill] ✗ 未获取到数据")
            
    except KeyboardInterrupt:
        print("\n[AShareSkill] 用户中断操作")
    except Exception as e:
        print(f"\n[AShareSkill] ✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if skill:
            skill._logout()


if __name__ == "__main__":
    main()
