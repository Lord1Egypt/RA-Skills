#!/usr/bin/env python3
"""
投资研究系统 - 行情监控模块
仅使用白名单域名：qt.gtimg.cn (HTTPS)
"""
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
import time
import sys
import os

# 导入配置文件
try:
    from config import REQUEST_DELAY, REQUEST_TIMEOUT
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import REQUEST_DELAY, REQUEST_TIMEOUT


class AShareMonitor:
    """A 股实时监控器 - 仅使用白名单域名"""
    
    # 白名单域名
    ALLOWED_DOMAINS = ["qt.gtimg.cn"]
    
    def __init__(self, delay: float = REQUEST_DELAY):
        """初始化监控器"""
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        })
        
    def _format_code(self, stock_code: str) -> str:
        """转换股票代码格式"""
        code = stock_code.split('.')[0] if '.' in stock_code else stock_code
        # 腾讯格式：sh600919 或 sz000921
        return f"sh{code}" if code.startswith('6') else f"sz{code}"
    
    def _fetch_tencent(self, code: str) -> Optional[Dict]:
        """
        从腾讯财经获取实时行情（HTTPS）
        
        白名单域名：qt.gtimg.cn
        """
        try:
            tencent_code = self._format_code(code)
            # 使用 HTTPS
            url = f"https://qt.gtimg.cn/q={tencent_code}"
            
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.encoding = 'gbk'
            
            if '=' in response.text:
                data_str = response.text.split('=')[1].strip().strip('"')
                fields = data_str.split('~')
                
                if len(fields) >= 40 and fields[2] and fields[3]:
                    current = float(fields[3])
                    yesterday_close = float(fields[4])
                    
                    # 安全转换数值
                    def safe_float(val, default=0):
                        try:
                            return float(val) if val else default
                        except:
                            return default
                    
                    return {
                        'source': '腾讯财经',
                        '代码': code,
                        '名称': fields[1] if fields[1] else '未知',
                        '现价': f"{current:.2f}",
                        '涨跌额': f"{current - yesterday_close:+.2f}",
                        '涨跌幅': f"{((current/yesterday_close - 1) * 100):+.2f}%",
                        '今开': f"{safe_float(fields[5]):.2f}",
                        '昨收': f"{yesterday_close:.2f}",
                        '最高': f"{safe_float(fields[33]):.2f}",
                        '最低': f"{safe_float(fields[34]):.2f}",
                        '成交量': f"{safe_float(fields[6])/100:.0f}手",
                        '成交额': f"{safe_float(fields[37])/10000:.2f}万"
                    }
        except Exception as e:
            print(f"腾讯财经获取失败: {e}")
        
        return None
    
    def get_quote(self, stock_code: str) -> Dict[str, Any]:
        """
        获取股票行情
        
        Args:
            stock_code: 股票代码 (如 600919 或 600919.SH)
            
        Returns:
            包含行情数据的字典
        """
        result = self._fetch_tencent(stock_code)
        
        if result:
            return result
        
        return {
            'error': f'无法获取 {stock_code} 的数据',
            '建议': '可能是非交易时间、网络问题或股票代码有误'
        }
    
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
            time.sleep(self.delay)
        
        return results


if __name__ == "__main__":
    # 测试示例
    monitor = AShareMonitor()
    
    print("=" * 60)
    print("📈 行情监控测试")
    print("=" * 60)
    print(f"白名单域名: {monitor.ALLOWED_DOMAINS}")
    print()
    
    codes = ['600919', '000921']
    monitor.batch_quotes(codes)