#!/usr/bin/env python3
"""
场内基金数据源抽象层
支持多数据源自动降级：东方财富 → 新浪财经 → 腾讯财经
每个数据源独立实现，互不影响。
"""

import json
import re
import urllib.request
import urllib.error
from abc import ABC, abstractmethod


# ============================================================
# 基础工具
# ============================================================

def get_market_code(fund_code: str) -> int:
    """根据基金代码判断市场：1=上海，0=深圳"""
    prefix = fund_code[:2]
    if prefix in ('51', '50', '56', '58'):
        return 1
    elif prefix in ('15', '16', '12'):
        return 0
    return 1 if fund_code.startswith('6') else 0


def http_get(url: str, headers: dict = None, timeout: int = 10, encoding: str = "utf-8") -> tuple:
    """
    发送HTTP GET请求。
    返回 (success: bool, content: str, error: str)
    """
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return True, raw.decode(encoding, errors="ignore"), ""
    except urllib.error.URLError as e:
        return False, "", f"网络错误: {e}"
    except Exception as e:
        return False, "", f"{type(e).__name__}: {e}"


# ============================================================
# 数据源抽象基类
# ============================================================

class DataSource(ABC):
    """所有数据源的基类"""
    name: str = "base"

    @abstractmethod
    def get_realtime_price(self, fund_code: str) -> dict:
        """
        获取实时行情。
        返回: {"price": float, "name": str, "open": float, "high": float,
               "low": float, "prev_close": float, "change_pct": float}
        失败返回: {"error": str}
        """
        pass

    @abstractmethod
    def get_latest_nav(self, fund_code: str) -> dict:
        """
        获取最新净值。
        返回: {"nav": float, "nav_date": str}
        失败返回: {"error": str}
        """
        pass

    def get_intraday_estimate(self, fund_code: str) -> dict:
        """
        获取盘中估值（可选，默认不可用）。
        返回: {"available": True, "estimated_nav": float, ...} 或 {"available": False}
        """
        return {"available": False}

    def get_history_klines(self, fund_code: str, days: int) -> tuple:
        """
        获取历史K线（可选，默认不支持）。
        返回: (name: str, records: [{"date": str, "close": float}])
        失败返回: ("", [])
        """
        return "", []


# ============================================================
# 数据源1: 东方财富（主力）
# ============================================================

class EastmoneySource(DataSource):
    name = "东方财富"

    def get_realtime_price(self, fund_code: str) -> dict:
        market = get_market_code(fund_code)
        url = (
            f"https://push2.eastmoney.com/api/qt/stock/get"
            f"?secid={market}.{fund_code}"
            f"&fields=f43,f44,f45,f46,f57,f58,f60,f170"
        )
        ok, text, err = http_get(url)
        if not ok:
            return {"error": err}
        try:
            data = json.loads(text).get("data")
            if not data:
                return {"error": "未找到行情数据"}
            return {
                "price": data.get("f43", 0) / 1000,
                "name": data.get("f58", fund_code),
                "open": data.get("f46", 0) / 1000,
                "high": data.get("f44", 0) / 1000,
                "low": data.get("f45", 0) / 1000,
                "prev_close": data.get("f60", 0) / 1000,
                "change_pct": data.get("f170", 0) / 100,
            }
        except Exception as e:
            return {"error": f"解析失败: {e}"}

    def get_latest_nav(self, fund_code: str, page_size: int = 1) -> dict:
        url = (
            f"http://api.fund.eastmoney.com/f10/lsjz"
            f"?fundCode={fund_code}&pageIndex=1&pageSize={page_size}"
        )
        ok, text, err = http_get(url, headers={"Referer": "http://fund.eastmoney.com/"})
        if not ok:
            return {"error": err}
        try:
            data = json.loads(text)
            nav_list = data.get("Data", {}).get("LSJZList", [])
            if not nav_list:
                return {"error": "未找到净值数据"}
            latest = nav_list[0]
            return {
                "nav": float(latest["DWJZ"]),
                "nav_date": latest["FSRQ"],
            }
        except Exception as e:
            return {"error": f"解析失败: {e}"}

    def get_intraday_estimate(self, fund_code: str) -> dict:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        ok, text, err = http_get(url)
        if not ok:
            return {"available": False}
        match = re.search(r'jsonpgz\((\{.*?\})\)', text)
        if not match:
            return {"available": False}
        try:
            data = json.loads(match.group(1))
            return {
                "available": True,
                "estimated_nav": float(data.get("gsz", 0)),
                "estimate_time": data.get("gztime", ""),
                "nav_date": data.get("jzrq", ""),
                "prev_nav": float(data.get("dwjz", 0)),
                "estimate_change_pct": float(data.get("gszzl", 0)),
            }
        except Exception:
            return {"available": False}

    def get_history_klines(self, fund_code: str, days: int) -> tuple:
        market = get_market_code(fund_code)
        url = (
            f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
            f"?secid={market}.{fund_code}"
            f"&fields1=f1,f2,f3,f4"
            f"&fields2=f51,f52,f53,f54,f55,f56"
            f"&klt=101&fqt=0&end=20500101&lmt={days}"
        )
        ok, text, err = http_get(url)
        if not ok:
            return "", []
        try:
            data = json.loads(text)
            d = data.get("data", {})
            name = d.get("name", fund_code)
            klines = d.get("klines", [])
            records = []
            for line in klines:
                parts = line.split(",")
                records.append({"date": parts[0], "close": float(parts[2])})
            return name, records
        except Exception:
            return "", []


# ============================================================
# 数据源2: 新浪财经（备用1）
# ============================================================

class SinaSource(DataSource):
    name = "新浪财经"

    def _sina_code(self, fund_code: str) -> str:
        """转换为新浪代码格式: sh513050 / sz159915"""
        market = get_market_code(fund_code)
        return f"{'sh' if market == 1 else 'sz'}{fund_code}"

    def get_realtime_price(self, fund_code: str) -> dict:
        code = self._sina_code(fund_code)
        url = f"http://hq.sinajs.cn/list={code}"
        ok, text, err = http_get(url, headers={"Referer": "http://finance.sina.com.cn"}, encoding="gbk")
        if not ok:
            return {"error": err}

        # 解析新浪行情格式
        # var hq_str_sh513050="名称,开盘价,昨收,当前价,最高,最低,..."
        match = re.search(r'"(.+)"', text)
        if not match:
            return {"error": "新浪行情数据解析失败"}

        parts = match.group(1).split(",")
        if len(parts) < 32 or not parts[3]:
            return {"error": "新浪行情数据不完整"}

        try:
            name = parts[0]
            open_ = float(parts[1])
            prev_close = float(parts[2])
            price = float(parts[3])
            high = float(parts[4])
            low = float(parts[5])
            change_pct = ((price - prev_close) / prev_close * 100) if prev_close > 0 else 0
            return {
                "price": price,
                "name": name,
                "open": open_,
                "high": high,
                "low": low,
                "prev_close": prev_close,
                "change_pct": change_pct,
            }
        except (ValueError, IndexError) as e:
            return {"error": f"新浪行情数值解析失败: {e}"}

    def get_latest_nav(self, fund_code: str) -> dict:
        """通过新浪基金净值接口获取"""
        url = (
            f"http://stock.finance.sina.com.cn/fundInfo/api/openapi.php"
            f"/CaihuiFundInfoService.getNav?symbol={fund_code}"
            f"&datefrom=2026-05-01&dateto=2026-06-03"
        )
        ok, text, err = http_get(url)
        if not ok:
            return {"error": err}
        try:
            data = json.loads(text)
            nav_list = data.get("result", {}).get("data", {}).get("data", [])
            if not nav_list:
                return {"error": "新浪未找到净值数据"}
            latest = nav_list[0]
            date_str = latest.get("fbrq", "")[:10]  # "2026-06-01 00:00:00" → "2026-06-01"
            return {
                "nav": float(latest["jjjz"]),
                "nav_date": date_str,
            }
        except Exception as e:
            return {"error": f"新浪净值解析失败: {e}"}

    def get_history_klines(self, fund_code: str, days: int) -> tuple:
        """新浪历史K线（日线）"""
        code = self._sina_code(fund_code)
        url = (
            f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php"
            f"/CN_MarketData.getKLineData?symbol={code}"
            f"&scale=240&ma=no&datalen={days}"
        )
        ok, text, err = http_get(url)
        if not ok:
            return "", []
        try:
            data = json.loads(text)
            if not data:
                return "", []
            name = fund_code  # 新浪K线接口不返回名称
            records = [{"date": k["day"], "close": float(k["close"])} for k in data]
            return name, records
        except Exception:
            return "", []


# ============================================================
# 数据源3: 腾讯财经（备用2 - 仅实时行情）
# ============================================================

class TencentSource(DataSource):
    name = "腾讯财经"

    def _tencent_code(self, fund_code: str) -> str:
        market = get_market_code(fund_code)
        return f"{'sh' if market == 1 else 'sz'}{fund_code}"

    def get_realtime_price(self, fund_code: str) -> dict:
        code = self._tencent_code(fund_code)
        url = f"http://qt.gtimg.cn/q={code}"
        ok, text, err = http_get(url, encoding="gbk")
        if not ok:
            return {"error": err}

        # 腾讯行情格式（字段用~分隔）
        # v_sh513050="1~名称~代码~现价~昨收~...~涨跌幅~..."
        match = re.search(r'v_[a-z]+\d+="(.+)"', text)
        if not match:
            return {"error": "腾讯行情数据解析失败"}

        parts = match.group(1).split("~")
        if len(parts) < 45:
            return {"error": "腾讯行情数据字段不足"}

        try:
            name = parts[1]
            price = float(parts[3])
            prev_close = float(parts[4])
            open_ = float(parts[5])
            volume = int(parts[6]) if parts[6] else 0
            high = float(parts[33]) if parts[33] else 0
            low = float(parts[34]) if parts[34] else 0
            change_pct = float(parts[32]) if parts[32] else 0
            return {
                "price": price,
                "name": name,
                "open": open_,
                "high": high,
                "low": low,
                "prev_close": prev_close,
                "change_pct": change_pct,
            }
        except (ValueError, IndexError) as e:
            return {"error": f"腾讯行情数值解析失败: {e}"}

    def get_latest_nav(self, fund_code: str) -> dict:
        """腾讯不提供基金净值接口"""
        return {"error": "腾讯财经不支持基金净值查询"}


# ============================================================
# 数据源工厂 + 自动降级
# ============================================================

# 默认数据源优先级
DEFAULT_SOURCES = [EastmoneySource, SinaSource, TencentSource]


def create_sources(source_classes: list = None) -> list:
    """创建数据源实例列表"""
    classes = source_classes or DEFAULT_SOURCES
    return [cls() for cls in classes]


def fetch_with_fallback(sources: list, method: str, fund_code: str) -> tuple:
    """
    带自动降级的数据获取。
    遍历数据源列表，直到某个源成功返回。
    返回: (result_dict, source_name)
    """
    errors = []
    for source in sources:
        try:
            if method == "realtime_price":
                result = source.get_realtime_price(fund_code)
            elif method == "latest_nav":
                result = source.get_latest_nav(fund_code)
            elif method == "intraday_estimate":
                result = source.get_intraday_estimate(fund_code)
            elif method == "history_klines":
                result = source.get_history_klines(fund_code, 0)  # days handled by caller
            else:
                return {"error": f"未知方法: {method}"}, ""

            if "error" not in result:
                return result, source.name
            errors.append(f"{source.name}({result['error']})")
        except Exception as e:
            errors.append(f"{source.name}(异常: {e})")

    return {"error": f"所有数据源失败: {'; '.join(errors)}"}, ""


# ============================================================
# 便捷函数（供外部脚本直接调用）
# ============================================================

def get_fund_realtime_price(fund_code: str, sources: list = None) -> tuple:
    """获取实时行情（自动降级）。返回 (result, source_name)"""
    srcs = sources or create_sources()
    return fetch_with_fallback(srcs, "realtime_price", fund_code)


def get_fund_nav(fund_code: str, sources: list = None) -> tuple:
    """获取最新净值（自动降级）。返回 (result, source_name)"""
    srcs = sources or create_sources()
    return fetch_with_fallback(srcs, "latest_nav", fund_code)


def get_fund_intraday_estimate(fund_code: str, sources: list = None) -> tuple:
    """获取盘中估值（自动降级）。返回 (result, source_name)"""
    srcs = sources or create_sources()
    return fetch_with_fallback(srcs, "intraday_estimate", fund_code)


def get_fund_history_klines(fund_code: str, days: int, sources: list = None) -> tuple:
    """获取历史K线（自动降级）。返回 ((name, records), source_name)"""
    srcs = sources or create_sources()
    errors = []
    for source in srcs:
        try:
            name, records = source.get_history_klines(fund_code, days)
            if records:
                return (name, records), source.name
            errors.append(f"{source.name}(无数据)")
        except Exception as e:
            errors.append(f"{source.name}(异常: {e})")
    return ("", []), ""


if __name__ == "__main__":
    # 自测
    import time

    test_codes = ["513050", "159915", "518880", "161226"]
    sources = create_sources()

    print("=== 实时行情测试 ===")
    for code in test_codes:
        result, src = get_fund_realtime_price(code, sources)
        if "error" not in result:
            print(f"  [{src}] {result['name']}({code}): {result['price']}")
        else:
            print(f"  ❌ {code}: {result['error']}")
        time.sleep(0.5)

    print("\n=== 净值查询测试 ===")
    for code in ["513050", "161226"]:
        result, src = get_fund_nav(code, sources)
        if "error" not in result:
            print(f"  [{src}] {code}: 净值={result['nav']} ({result['nav_date']})")
        else:
            print(f"  ❌ {code}: {result['error']}")
        time.sleep(0.5)

    print("\n=== 历史K线测试 ===")
    for code in ["513050", "159915"]:
        (name, records), src = get_fund_history_klines(code, 3, sources)
        if records:
            print(f"  [{src}] {name}({code}): {len(records)}条K线")
            for r in records:
                print(f"    {r['date']} 收盘:{r['close']}")
        else:
            print(f"  ❌ {code}: 无数据")
        time.sleep(0.5)
