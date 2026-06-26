#!/usr/bin/env python3
"""
A-Share Pro 核心监控模块
支持腾讯财经、雪球、百度股市通、Tushare 多数据源自动切换
"""
import requests
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
import time
import sys

# 导入配置文件
try:
    from config import (
        DATA_SOURCES_PRIORITY,
        TUSHARE_TOKEN,
        REQUEST_DELAY,
        REQUEST_TIMEOUT
    )
except ImportError:
    # 如果单独运行此脚本，添加路径
    sys.path.insert(0, '/Users/wangrx/.openclaw/workspace/skills/a-share-pro/scripts')
    from config import (
        DATA_SOURCES_PRIORITY,
        TUSHARE_TOKEN,
        REQUEST_DELAY,
        REQUEST_TIMEOUT
    )


class AShareMonitor:
    """A 股实时监控器 - 多数据源自动选择"""
    
    def __init__(self, delay: float = REQUEST_DELAY):
        """初始化监控器"""
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        })
        
    def _format_code(self, stock_code: str, source: str = 'tencent') -> str:
        """转换股票代码格式以适应不同数据源"""
        code = stock_code.split('.')[0] if '.' in stock_code else stock_code
        
        if source == 'tencent':
            return f"sh{code}" if code.startswith('6') else f"sz{code}"
        elif source == 'xueqiu':
            exchange = 'SH' if code.startswith('6') or code.startswith('8') else 'SZ'
            return f"{exchange}{code}"
        else:
            return code
    
    # ========== 1. 腾讯财经 ==========
    def _fetch_tencent(self, code: str) -> Optional[Dict]:
        """从腾讯财经获取实时行情"""
        try:
            tencent_code = self._format_code(code, 'tencent')
            url = f"http://qt.gtimg.cn/q={tencent_code}"
            
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.encoding = 'gbk'
            
            if '=' in response.text:
                data_str = response.text.split('=')[1].strip().strip('"')
                fields = data_str.split('~')
                
                if len(fields) >= 40 and fields[2] and fields[3]:
                    current = float(fields[3])
                    yesterday_close = float(fields[4])
                    
                    return {
                        'source': '🐧 腾讯财经',
                        '代码': code,
                        '名称': fields[1] if fields[1] else '未知',
                        '现价': f"{current:.2f}",
                        '涨跌额': f"{current - yesterday_close:+.2f}",
                        '涨跌幅': f"{((current/yesterday_close - 1) * 100):+.2f}%",
                        '今开': f"{fields[5]:.2f}" if fields[5] else 'N/A',
                        '昨收': f"{yesterday_close:.2f}",
                        '最高': f"{fields[6]:.2f}" if fields[6] else 'N/A',
                        '最低': f"{fields[7]:.2f}" if fields[7] else 'N/A',
                        '成交量': f"{float(fields[8])/100:.0f}手" if fields[8] else 'N/A',
                        '成交额': f"{float(fields[9])/10000:.2f}万" if fields[9] else 'N/A'
                    }
        except:
            pass
        
        return None
    
    # ========== 2. 雪球 ==========
    def _fetch_xueqiu(self, code: str) -> Optional[Dict]:
        """从雪球获取实时行情"""
        try:
            xueqiu_code = self._format_code(code, 'xueqiu')
            
            headers = self.session.headers.copy()
            headers['Referer'] = f'https://xueqiu.com/S/{xueqiu_code}'
            headers['X-Requested-With'] = 'XMLHttpRequest'
            
            # 先访问首页获取 Cookie
            self.session.get("https://www.xueqiu.com/", timeout=3, headers=headers)
            
            url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json"
            params = {'symbol': xueqiu_code}
            
            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            data = response.json()
            
            if data.get('error_code') == 0 and 'data' in data:
                quote = data['data']
                if isinstance(quote, list) and len(quote) > 0:
                    quote = quote[0]
                
                current = quote.get('current', 0)
                last_close = quote.get('last_close', quote.get('prev_close', 0))
                
                if current and last_close:
                    change_pct = ((current / last_close) - 1) * 100
                else:
                    change_pct = 0
                
                return {
                    'source': '📱 雪球',
                    '代码': code,
                    '名称': quote.get('name', '未知'),
                    '现价': f"{current:.2f}",
                    '涨跌额': f"{current - last_close:+.2f}" if last_close else 'N/A',
                    '涨跌幅': f"{change_pct:+.2f}%" if last_close else 'N/A',
                    '今开': f"{quote.get('open', 0):.2f}" if quote.get('open') else 'N/A',
                    '昨收': f"{last_close:.2f}" if last_close else 'N/A',
                    '最高': f"{quote.get('high', 0):.2f}" if quote.get('high') else 'N/A',
                    '最低': f"{quote.get('low', 0):.2f}" if quote.get('low') else 'N/A',
                    '成交量': f"{quote.get('volume', 0)/100:.0f}手" if quote.get('volume') else 'N/A',
                    '成交额': f"{quote.get('amount', 0)/10000:.2f}万" if quote.get('amount') else 'N/A'
                }
        except:
            pass
        
        return None
    
    # ========== 3. 百度股市通 ==========
    def _fetch_baidu(self, code: str) -> Optional[Dict]:
        """从百度股市通获取实时行情"""
        try:
            pure_code = code.split('.')[0] if '.' in code else code
            
            url = "https://finance.pae.baidu.com/selfselect/getstockinfo"
            params = {'code': pure_code, 'market': 'ab', 'type': 'stock'}
            
            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            data = response.json()
            
            if 'data' in data and 'marketData' in data['data']:
                md = data['data']['marketData']
                
                return {
                    'source': '🔍 百度股市通',
                    '代码': code,
                    '名称': md.get('name', '未知'),
                    '现价': f"{md.get('price', 0):.2f}",
                    '涨跌额': f"{md.get('change', 0):+.2f}",
                    '涨跌幅': f"{md.get('changeRate', 0):+.2f}%",
                    '今开': f"{md.get('open', 0):.2f}",
                    '昨收': f"{md.get('preClose', 0):.2f}",
                    '最高': f"{md.get('high', 0):.2f}",
                    '最低': f"{md.get('low', 0):.2f}",
                    '成交量': f"{md.get('volume', 0)/100:.0f}手",
                    '成交额': f"{md.get('amount', 0)/10000:.2f}万"
                }
        except:
            pass
        
        return None
    
    # ========== 主查询函数 ==========
    def get_quote(self, stock_code: str) -> Dict[str, Any]:
        """
        获取股票行情（自动选择最佳数据源）
        
        Args:
            stock_code: 股票代码 (如 600919.SH 或 600919)
            
        Returns:
            包含行情数据的字典
        """
        # 按优先级尝试各个数据源
        for source in DATA_SOURCES_PRIORITY:
            if source == 'tencent':
                result = self._fetch_tencent(stock_code)
            elif source == 'xueqiu':
                result = self._fetch_xueqiu(stock_code)
            elif source == 'baidu':
                result = self._fetch_baidu(stock_code)
            elif source == 'tushare':
                result = self._fetch_tushare(stock_code)
            else:
                continue
            
            if result:
                return result
            
            # 在请求间隔后继续尝试下一个
            time.sleep(self.delay)
        
        return {
            'error': f'所有数据源均无法获取{stock_code}的数据',
            '建议': '可能是非交易时间、网络问题或股票代码有误'
        }
    
    # ========== 批量查询 ==========
    def batch_quotes(self, stock_codes: List[str]) -> List[Dict[str, Any]]:
        """批量查询多个股票"""
        results = []
        
        print(f"📊 正在查询 {len(stock_codes)} 只股票...\n")
        
        for i, code in enumerate(stock_codes, 1):
            print(f"[{i}/{len(stock_codes)}] {code:12} ", end="")
            
            result = self.get_quote(code)
            
            if 'error' not in result:
                print(f"✅ ¥{result.get('现价', 'N/A'):>8} {result.get('涨跌幅', 'N/A'):>10}")
            else:
                print(f"❌ {result['error']}")
            
            results.append(result)
        
        return results


if __name__ == "__main__":
    # 测试示例
    monitor = AShareMonitor()
    
    print("=" * 60)
    print("📈 A-Share Pro 监控测试")
    print("=" * 60)
    
    codes = ['600919', '600926', '159681']
    monitor.batch_quotes(codes)
