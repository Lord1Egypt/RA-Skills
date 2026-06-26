#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fund Keeper v2.7 - 国内场外基金智能顾问
参考养基宝逻辑，提供实时估值、买卖建议、基金组合管理
支持：历史分位、技术指标、止盈止损提醒、收益可视化、贵金属、基金搜索
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

import pandas as pd
import requests


class FundKeeper:
    """基金顾问核心类"""

    def __init__(self, workspace_dir=None):
        # 优先使用技能目录下的 funds，兼容旧版路径
        if workspace_dir is None:
            # 尝试技能目录下的 funds
            skill_funds_dir = Path(__file__).parent / "funds"
            if skill_funds_dir.exists():
                self.funds_dir = skill_funds_dir
            else:
                # 兼容旧版：workspace/funds
                self.funds_dir = Path(__file__).parent.parent.parent / "funds"
                self.funds_dir.mkdir(exist_ok=True)
        else:
            self.funds_dir = Path(workspace_dir) / "funds"
            self.funds_dir.mkdir(exist_ok=True)

        self.config_file = self.funds_dir / "config.json"
        self.my_funds_file = self.funds_dir / "my-funds.md"
        self.history_file = self.funds_dir / "history.md"
        self.cache_file = self.funds_dir / "cache.json"
        self.transactions_file = self.funds_dir / "transactions.json"

        self.config = self._load_config()
        self.cache = self._load_cache()
        self.transactions = self._load_transactions()
        
        # 数据源优先级（按可靠性排序）
        self.data_sources = ["ttjj", "eastmoney", "sina"]

    def _load_transactions(self):
        """加载交易记录"""
        if self.transactions_file.exists():
            try:
                with open(self.transactions_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_transactions(self):
        """保存交易记录"""
        with open(self.transactions_file, "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, indent=2, ensure_ascii=False)
    
    def _load_cache(self):
        """加载缓存数据"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"funds": {}, "last_update": ""}
        return {"funds": {}, "last_update": ""}
    
    def _save_cache(self):
        """保存缓存数据"""
        self.cache["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def _get_cache_data(self, fund_code, max_age_minutes=30):
        """从缓存获取数据（默认30分钟内有效）"""
        if fund_code in self.cache.get("funds", {}):
            cached = self.cache["funds"][fund_code]
            try:
                cache_time = datetime.strptime(cached.get("cache_time", ""), "%Y-%m-%d %H:%M:%S")
                if (datetime.now() - cache_time).total_seconds() < max_age_minutes * 60:
                    cached["from_cache"] = True
                    return cached
            except:
                pass
        return None
    
    def _set_cache_data(self, fund_code, data):
        """设置缓存数据"""
        if "funds" not in self.cache:
            self.cache["funds"] = {}
        data["cache_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cache["funds"][fund_code] = data
        self._save_cache()

    def _load_config(self):
        """加载配置"""
        default_config = {
            "alert_threshold": 3.0
        }

        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**default_config, **config}
        else:
            self._save_config(default_config)
            return default_config

    def _save_config(self, config):
        """保存配置"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def get_fund_list(self, exclude_sip=False):
        """获取持仓基金列表"""
        if not self.my_funds_file.exists():
            return []

        funds = []
        with open(self.my_funds_file, "r", encoding="utf-8") as f:
            in_table = False
            for line in f:
                line = line.strip()
                if line.startswith("|") and "基金代码" in line:
                    in_table = True
                    continue
                if in_table and line.startswith("|"):
                    parts = line.split("|")
                    if len(parts) >= 5:
                        code = parts[1].strip()
                        if code and code != "---" and not code.startswith("-") and code.isdigit():
                            try:
                                # 新格式：基金代码|基金名称|持有金额|持有收益|止盈%|止损%|定投日|备注
                                note = parts[8].strip() if len(parts) > 8 else ""
                                sip_day = int(parts[7].strip()) if len(parts) > 7 and parts[7].strip().isdigit() else 0
                                stop_loss = float(parts[6].strip()) if len(parts) > 6 and parts[6].strip() else 0
                                profit_target = float(parts[5].strip()) if len(parts) > 5 and parts[5].strip() else 0
                                
                                is_sip = sip_day > 0
                                
                                if exclude_sip and is_sip:
                                    continue
                                
                                funds.append({
                                    "code": code,
                                    "name": parts[2].strip(),
                                    "amount": float(parts[3].strip() or 0),
                                    "profit": parts[4].strip() if len(parts) > 4 else "0",
                                    "profit_target": profit_target,
                                    "stop_loss": stop_loss,
                                    "sip_day": sip_day,
                                    "note": note,
                                    "is_sip": is_sip
                                })
                            except ValueError:
                                pass
        return funds

    def get_fund_nav_estimate_single(self, fund_code, source="ttjj"):
        """从单个数据源获取基金实时净值估算"""
        if source == "ttjj":
            # 天天基金网
            try:
                url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Referer": f"http://fund.eastmoney.com/{fund_code}.html"
                }
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    content = response.text
                    if content.startswith("jsonpgz(") and content.endswith(");"):
                        data = json.loads(content[8:-2])
                        return {
                            "code": data.get("fundcode"),
                            "name": data.get("name"),
                            "current_nav": float(data.get("gsz", 0)),
                            "last_nav": float(data.get("dwjz", 0)),
                            "estimate_growth": float(data.get("gszzl", 0)),
                            "update_time": data.get("gztime", ""),
                            "source": "天天基金网"
                        }
            except Exception as e:
                pass
        elif source == "akshare":
            # AKShare
            try:
                import akshare as ak
                fund_etf_fund_info_em = ak.fund_etf_fund_info_em(fund=fund_code)
                if fund_etf_fund_info_em is not None and not fund_etf_fund_info_em.empty:
                    row = fund_etf_fund_info_em.iloc[0]
                    return {
                        "code": fund_code,
                        "name": row.get("基金简称", ""),
                        "current_nav": float(row.get("最新价", 0)),
                        "last_nav": float(row.get("昨收", 0)),
                        "estimate_growth": float(row.get("涨跌幅", 0)),
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "source": "AKShare"
                    }
            except Exception as e:
                pass
        elif source == "eastmoney":
            # 东方财富网
            try:
                url = f"http://fund.eastmoney.com/{fund_code}.html"
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    import re
                    nav_match = re.search(r'"unit_nav":"([\d.]+)"', response.text)
                    if nav_match:
                        current_nav = float(nav_match.group(1))
                        return {
                            "code": fund_code,
                            "name": "",
                            "current_nav": current_nav,
                            "last_nav": current_nav,
                            "estimate_growth": 0,
                            "update_time": datetime.now().strftime("%Y-%m-%d"),
                            "source": "东方财富网"
                        }
            except Exception as e:
                pass
        elif source == "sina":
            # 新浪财经
            try:
                url = f"http://hq.sinajs.cn/list=fu_{fund_code}"
                headers = {
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "http://finance.sina.com.cn/fund/"
                }
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    content = response.text
                    if 'var hq_str_fu_' in content:
                        # 解析格式：var hq_str_fu_000001="基金名称,净值,累计净值,涨跌幅,..."
                        import re
                        match = re.search(r'="(.*?)"', content)
                        if match:
                            parts = match.group(1).split(',')
                            if len(parts) >= 4:
                                return {
                                    "code": fund_code,
                                    "name": parts[0] if parts[0] else "",
                                    "current_nav": float(parts[1]) if parts[1] else 0,
                                    "last_nav": float(parts[1]) if parts[1] else 0,
                                    "estimate_growth": float(parts[3]) if parts[3] else 0,
                                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "source": "新浪财经"
                                }
            except Exception as e:
                pass
        return None

    def get_fund_nav_estimate(self, fund_code, cross_validate=False, use_cache=True, offline=False):
        """获取基金实时净值估算（支持多数据源、缓存、离线模式）
        
        Args:
            fund_code: 基金代码
            cross_validate: 是否进行多数据源交叉验证
            use_cache: 是否使用缓存
            offline: 离线模式（仅使用缓存）
        
        Returns:
            dict: 净值数据
        """
        # 离线模式：仅使用缓存
        if offline:
            cached = self._get_cache_data(fund_code, max_age_minutes=999999)
            if cached:
                cached["offline_mode"] = True
                return cached
            return None
        
        # 尝试从缓存获取（30分钟内有效）
        if use_cache:
            cached = self._get_cache_data(fund_code, max_age_minutes=30)
            if cached:
                return cached
        
        # 单数据源模式（快速，按优先级尝试）
        if not cross_validate:
            for source in self.data_sources:
                result = self.get_fund_nav_estimate_single(fund_code, source)
                if result:
                    # 缓存结果
                    self._set_cache_data(fund_code, result)
                    return result
            
            # 所有数据源都失败，尝试使用旧缓存
            cached = self._get_cache_data(fund_code, max_age_minutes=999999)
            if cached:
                cached["stale_cache"] = True
                return cached
            
            return None
        
        # 多数据源交叉验证模式
        results = []
        
        for source in self.data_sources:
            data = self.get_fund_nav_estimate_single(fund_code, source)
            if data:
                results.append(data)
        
        if not results:
            # 所有数据源都失败，尝试使用旧缓存
            cached = self._get_cache_data(fund_code, max_age_minutes=999999)
            if cached:
                cached["stale_cache"] = True
                return cached
            return None
        
        if len(results) == 1:
            # 只有一个数据源
            self._set_cache_data(fund_code, results[0])
            return results[0]
        
        # 多个数据源，进行交叉验证
        growths = [r["estimate_growth"] for r in results]
        avg_growth = sum(growths) / len(growths)
        
        max_diff = max(growths) - min(growths)
        consistency = "高" if max_diff < 0.3 else ("中" if max_diff < 1.0 else "低")
        
        result = {
            "code": fund_code,
            "name": results[0].get("name", ""),
            "current_nav": sum(r["current_nav"] for r in results) / len(results),
            "last_nav": sum(r["last_nav"] for r in results) / len(results),
            "estimate_growth": avg_growth,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "source": f"多源校验 ({len(results)} 个)",
            "cross_validation": {
                "sources_count": len(results),
                "sources": [r["source"] for r in results],
                "consistency": consistency,
                "max_diff": round(max_diff, 2),
                "details": results
            }
        }
        
        self._set_cache_data(fund_code, result)
        return result

    def get_fund_history(self, fund_code, days=90):
        """获取基金历史净值（多数据源）
        
        优先级：
        1. AKShare（更稳定）
        2. 天天基金网
        """
        # 方案 1: AKShare - 尝试多个接口
        try:
            import akshare as ak
            
            # 尝试 ETF 基金历史数据
            try:
                fund_hist = ak.fund_etf_hist_em(symbol=fund_code, period="daily", start_date="20240101", end_date=datetime.now().strftime("%Y%m%d"))
                if fund_hist is not None and not fund_hist.empty:
                    history = []
                    for _, row in fund_hist.head(days).iterrows():
                        history.append({
                            "date": row.get("日期", ""),
                            "unit_nav": float(row.get("收盘", 0)),
                            "accumulated_nav": float(row.get("收盘", 0))
                        })
                    if history:
                        return history
            except:
                pass
            
            # 尝试 LOF 基金历史数据
            try:
                fund_hist = ak.fund_lof_hist_em(symbol=fund_code, period="日常", start_date="20240101", end_date=datetime.now().strftime("%Y%m%d"))
                if fund_hist is not None and not fund_hist.empty:
                    history = []
                    for _, row in fund_hist.head(days).iterrows():
                        history.append({
                            "date": row.get("日期", ""),
                            "unit_nav": float(row.get("收盘", 0)),
                            "accumulated_nav": float(row.get("收盘", 0))
                        })
                    if history:
                        return history
            except:
                pass
                
        except Exception as e:
            print(f"[AKShare 历史] 获取失败：{e}")
        
        # 方案 2: 天天基金网
        try:
            url = f"http://fund.eastmoney.com/f10/jjjz_{fund_code}.html"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                import re
                nav_pattern = r'<td>(\d{4}-\d{2}-\d{2})</td>\s*<td>([\d.]+)</td>\s*<td>([\d.]+)</td>'
                matches = re.findall(nav_pattern, response.text)
                
                if matches:
                    history = []
                    for date, unit_nav, accumulated_nav in matches[:days]:
                        history.append({
                            "date": date,
                            "unit_nav": float(unit_nav),
                            "accumulated_nav": float(accumulated_nav)
                        })
                    return history
        except Exception as e:
            print(f"[天天基金网历史] 获取失败：{e}")
        
        return None

    def calculate_percentile(self, current_value, historical_values):
        """计算历史百分位"""
        if not historical_values or len(historical_values) < 20:
            return None
        
        count_below = sum(1 for v in historical_values if v < current_value)
        percentile = (count_below / len(historical_values)) * 100
        return round(percentile, 1)

    def calculate_ma(self, values, period=20):
        """计算移动平均线"""
        if len(values) < period:
            return None
        return sum(values[-period:]) / period

    def analyze_fund(self, fund_code, nav_data):
        """综合分析基金，给出买卖建议"""
        analysis = {
            "code": fund_code,
            "name": nav_data.get("name", ""),
            "current_nav": nav_data.get("current_nav", 0),
            "estimate_growth": nav_data.get("estimate_growth", 0),
            "recommendation": "[WAIT]",
            "confidence": "中",
            "reasons": []
        }

        # 1. 获取历史数据
        history = self.get_fund_history(fund_code, days=90)
        
        if history and len(history) >= 20:
            nav_values = [h["unit_nav"] for h in history]
            current_nav = nav_data.get("current_nav", nav_values[0])
            
            # 2. 历史分位分析
            percentile = self.calculate_percentile(current_nav, nav_values)
            if percentile is not None:
                analysis["percentile"] = percentile
                
                if percentile < 20:
                    analysis["reasons"].append(f"历史分位 {percentile}% - 严重低估")
                    analysis["recommendation"] = "[STRONG BUY]"
                    analysis["confidence"] = "高"
                elif percentile < 40:
                    analysis["reasons"].append(f"历史分位 {percentile}% - 偏低估")
                    analysis["recommendation"] = "[BUY]"
                    analysis["confidence"] = "中"
                elif percentile > 80:
                    analysis["reasons"].append(f"历史分位 {percentile}% - 高估")
                    analysis["recommendation"] = "[SELL]"
                    analysis["confidence"] = "中"
                elif percentile > 90:
                    analysis["reasons"].append(f"历史分位 {percentile}% - 严重高估")
                    analysis["recommendation"] = "[STRONG SELL]"
                    analysis["confidence"] = "高"
                else:
                    analysis["reasons"].append(f"历史分位 {percentile}% - 合理区间")
            
            # 3. 技术指标 - 均线
            ma20 = self.calculate_ma(nav_values, 20)
            ma60 = self.calculate_ma(nav_values, 60) if len(nav_values) >= 60 else None
            
            if ma20:
                if current_nav > ma20:
                    analysis["reasons"].append(f"站上年线 (MA20: {ma20:.3f})")
                    if analysis["recommendation"] == "[WAIT]":
                        analysis["recommendation"] = "[HOLD]"
                else:
                    analysis["reasons"].append(f"低于年线 (MA20: {ma20:.3f})")
            
            # 4. 趋势判断
            if len(nav_values) >= 10:
                recent_trend = nav_values[-1] - nav_values[-10]
                if recent_trend > 0:
                    analysis["reasons"].append("近期上升趋势")
                else:
                    analysis["reasons"].append("近期下降趋势")
        
        # 5. 今日涨幅调整
        growth = nav_data.get("estimate_growth", 0)
        if growth > 3:
            analysis["reasons"].append(f"今日大涨 +{growth}% - 不宜追高")
            if analysis["recommendation"] in ["[BUY]", "[STRONG BUY]"]:
                analysis["recommendation"] = "[HOLD]"
        elif growth < -3:
            analysis["reasons"].append(f"今日大跌 {growth}% - 关注机会")
            if analysis["recommendation"] == "[WAIT]":
                analysis["recommendation"] = "[BUY]"
        elif growth < 0:
            analysis["reasons"].append(f"今日下跌 {growth}%")
        
        # 6. 止盈止损检查
        profit_target = self.config.get("profit_target_percent", 20)
        stop_loss = self.config.get("stop_loss_percent", 10)
        
        current_profit = float(nav_data.get("current_nav", 0)) - float(nav_data.get("last_nav", 0))
        if current_profit > profit_target / 100:
            analysis["reasons"].append(f"达到止盈目标 ({profit_target}%)")
            analysis["recommendation"] = "[SELL]"
        elif current_profit < -stop_loss / 100:
            analysis["reasons"].append(f"触及止损线 ({stop_loss}%)")
            if analysis["recommendation"] not in ["[STRONG SELL]", "[SELL]"]:
                analysis["recommendation"] = "[HOLD]"

        return analysis

    def print_portfolio(self, cross_validate=False, offline=False):
        """打印持仓概览
        
        Args:
            cross_validate: 是否启用多数据源交叉验证（默认关闭，加快速度）
            offline: 离线模式（仅使用缓存）
        """
        funds = self.get_fund_list()
        if not funds:
            print("No holdings data")
            return
        
        if offline:
            print(f"\n[Fund Portfolio] {datetime.now().strftime('%Y-%m-%d %H:%M')} [离线模式]\n")
        else:
            print(f"\n[Fund Portfolio] {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        print(f"{'Code':<8} {'Name':<25} {'Amount':>10} {'Profit':>10} {'Today':>8}")
        print("-" * 65)

        total_amount = 0
        total_profit = 0

        for fund in funds:
            code = fund["code"]
            name = fund["name"][:25] if len(fund["name"]) > 25 else fund["name"]
            amount = fund.get("amount", 0)
            profit_str = fund.get("profit", "0")
            is_sip = fund.get("is_sip", False)
            
            nav_data = self.get_fund_nav_estimate(code, cross_validate=cross_validate, offline=offline)
            growth_str = "--"
            source_str = ""
            if nav_data:
                growth_str = f"{nav_data['estimate_growth']:+.2f}%"
                source_str = f" [{nav_data.get('source', '')}]"
                if nav_data.get("from_cache"):
                    source_str += " [缓存]"
                if nav_data.get("offline_mode"):
                    source_str += " [离线]"
                if nav_data.get("stale_cache"):
                    source_str += " [旧缓存]"
                if "cross_validation" in nav_data:
                    cv = nav_data["cross_validation"]
                    source_str += f" [{cv['consistency']}一致性]"
            
            sip_marker = " [SIP]" if is_sip else ""
            print(f"{code:<8} {name:<25} {amount:>10.2f} {profit_str:>10} {growth_str:>8}{sip_marker}{source_str}")
            
            try:
                total_amount += float(amount)
                profit_val = float(profit_str.replace("+", ""))
                total_profit += profit_val
            except:
                pass

        print("-" * 65)
        print(f"Total: {total_amount:.2f} CNY (Profit: {total_profit:+.2f} CNY)")
        if cross_validate:
            print("* 已启用多数据源交叉验证")
        print()

    def print_advice(self, fund_code=None, exclude_sip=True, show_all=False, cross_validate=False, offline=False):
        """打印详细买卖建议
        
        Args:
            fund_code: 指定基金代码
            exclude_sip: 是否排除定投基金
            show_all: 显示全部基金
            cross_validate: 是否启用交叉验证
            offline: 离线模式（仅使用缓存）
        """
        funds = self.get_fund_list(exclude_sip=exclude_sip)
        if not funds:
            print("No holdings data (or all funds are SIP)")
            return

        if fund_code:
            funds = [f for f in funds if f["code"] == fund_code]

        print(f"\n[Fund Advice] {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        if offline:
            print("* 离线模式（仅使用缓存数据）\n")
        if exclude_sip:
            print("* 定投基金已排除，仅分析非定投持仓\n")
        if cross_validate:
            print("* 已启用多数据源交叉验证（可能需要 30-60 秒）\n")

        for fund in funds:
            print(f"正在分析 {fund['code']}...")
            nav_data = self.get_fund_nav_estimate(fund["code"], cross_validate=cross_validate, offline=offline)
            if not nav_data:
                print(f"[NO DATA] {fund['code']} - 获取数据失败\n")
                continue
            
            analysis = self.analyze_fund(fund["code"], nav_data)
            
            print(f"\n{analysis['recommendation']} {fund['code']} - {fund['name']}")
            print(f"  当前净值：{analysis['current_nav']:.4f} (估算 {analysis['estimate_growth']:+.2f}%)")
            print(f"  建议置信度：{analysis['confidence']}")
            
            # 显示交叉验证信息
            if "cross_validation" in nav_data:
                cv = nav_data["cross_validation"]
                print(f"  数据源校验：{cv['sources_count']} 个数据源，一致性：{cv['consistency']}")
                print(f"  数据源：{', '.join(cv['sources'])}")
                print(f"  最大差异：{cv['max_diff']:.2f}%")
                if cv['max_diff'] > 0.5:
                    print(f"  ⚠️ 注意：数据源差异较大，建议谨慎参考")
            else:
                print(f"  数据源：{nav_data.get('source', '未知')}")
            
            if "percentile" in analysis:
                print(f"  历史分位：{analysis['percentile']}%")
            
            print(f"  分析依据:")
            for reason in analysis["reasons"]:
                print(f"    - {reason}")
            print()

    def edit_fund(self, code, field=None, value=None):
        """编辑基金信息
        
        Args:
            code: 基金代码
            field: 要编辑的字段（name/amount/profit/stop/day/note）
            value: 新值
        """
        funds = self.get_fund_list()
        
        # 查找基金
        fund_index = -1
        for i, f in enumerate(funds):
            if f["code"] == code:
                fund_index = i
                break
        
        if fund_index == -1:
            print(f"Error: 基金 {code} 不存在\n")
            return False
        
        fund = funds[fund_index]
        
        # 交互式编辑
        if not field:
            print(f"\n【编辑基金】{code} {fund['name']}\n")
            print("当前信息:")
            print(f"  1. 基金名称: {fund['name']}")
            print(f"  2. 持有金额: {fund['amount']} 元")
            print(f"  3. 止盈目标: {fund['profit_target']}%")
            print(f"  4. 止损线: {fund['stop_loss']}%")
            print(f"  5. 定投日: {fund['sip_day']}")
            print(f"  6. 备注: {fund['note']}")
            print()
            
            field_input = input("选择要编辑的字段（1-6）: ").strip()
            field_map = {
                "1": "name",
                "2": "amount",
                "3": "profit",
                "4": "stop",
                "5": "day",
                "6": "note"
            }
            field = field_map.get(field_input)
            
            if not field:
                print("Error: 无效的选择\n")
                return False
            
            value = input(f"新值: ").strip()
        
        # 更新字段
        if field == "name":
            fund["name"] = value
        elif field == "amount":
            fund["amount"] = float(value)
        elif field == "profit":
            fund["profit_target"] = float(value)
        elif field == "stop":
            fund["stop_loss"] = float(value)
        elif field == "day":
            fund["sip_day"] = int(value)
        elif field == "note":
            fund["note"] = value
        else:
            print(f"Error: 未知字段 {field}\n")
            return False
        
        # 保存到文件
        self._update_fund_in_file(funds)
        
        print(f"\n✓ 已更新: {code} {field} = {value}\n")
        return True
    
    def remove_fund(self, code, confirm=True):
        """删除基金
        
        Args:
            code: 基金代码
            confirm: 是否需要确认
        """
        funds = self.get_fund_list()
        
        # 查找基金
        fund_index = -1
        for i, f in enumerate(funds):
            if f["code"] == code:
                fund_index = i
                break
        
        if fund_index == -1:
            print(f"Error: 基金 {code} 不存在\n")
            return False
        
        fund = funds[fund_index]
        
        # 确认删除
        if confirm:
            print(f"\n【删除基金】{code} {fund['name']}\n")
            print(f"  持有金额: {fund['amount']} 元")
            print(f"  止盈目标: {fund['profit_target']}%")
            print()
            
            confirm_input = input("确认删除？(y/N): ").strip().lower()
            if confirm_input != 'y':
                print("已取消\n")
                return False
        
        # 删除基金
        funds.pop(fund_index)
        
        # 保存到文件
        self._update_fund_in_file(funds)
        
        print(f"\n✓ 已删除: {code} {fund['name']}\n")
        return True
    
    def _update_fund_in_file(self, funds):
        """更新基金列表到文件"""
        # 重新生成表格
        content = "# 我的基金持仓\n\n"
        content += "| 基金代码 | 基金名称 | 持有金额 | 持有收益 | 止盈% | 止损% | 定投日 | 备注 |\n"
        content += "|----------|----------|----------|----------|-------|-------|--------|------|\n"
        
        for f in funds:
            content += f"| {f['code']} | {f['name']} | {f['amount']:.2f} | {f['profit']} | {f['profit_target']} | {f['stop_loss']} | {f['sip_day']} | {f['note']} |\n"
        
        with open(self.my_funds_file, "w", encoding="utf-8") as file:
            file.write(content)

    def add_fund_from_image(self, image_path):
        """从截图识别添加基金"""
        try:
            import easyocr
            
            print(f"Recognizing image: {image_path}")
            reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)
            results = reader.readtext(image_path)
            
            texts = [result[1] for result in results]
            full_text = '\n'.join(texts)
            
            fund_codes = re.findall(r'\b(\d{6})\b', full_text)
            fund_codes = list(set(fund_codes))
            
            if not fund_codes:
                print("No fund codes found")
                return None
            
            funds_found = []
            for code in fund_codes:
                fund_info = {"code": code, "name": "", "note": "OCR identified"}
                for i, text in enumerate(texts):
                    if code in text and i > 0:
                        fund_info["name"] = texts[i-1].strip()
                        break
                funds_found.append(fund_info)
            
            return funds_found
            
        except Exception as e:
            print(f"OCR failed: {e}")
            return None

    def add_fund_interactive(self, code=None, name=None, amount=None, profit_target=None, stop_loss=None, sip_day=None, note=None):
        """交互式添加基金"""
        print("\n" + "="*60)
        print("【添加基金】")
        print("="*60 + "\n")
        
        # 获取基金代码
        if not code:
            code = input("基金代码（6位数字）: ").strip()
        if not code or not code.isdigit() or len(code) != 6:
            print("Error: 基金代码必须是6位数字")
            return False
        
        # 检查是否已存在
        funds = self.get_fund_list()
        for f in funds:
            if f["code"] == code:
                print(f"Error: 基金 {code} 已存在")
                return False
        
        # 获取基金名称（如果没提供，尝试从网络获取）
        if not name:
            print("正在查询基金信息...")
            nav_data = self.get_fund_nav_estimate(code)
            if nav_data and nav_data.get("name"):
                name = nav_data["name"]
                print(f"基金名称: {name}")
                confirm = input("确认使用此名称？(Y/n): ").strip().lower()
                if confirm == 'n':
                    name = input("请输入基金名称: ").strip()
            else:
                name = input("基金名称: ").strip()
        
        if not name:
            name = "Unknown"
        
        # 获取持有金额
        if not amount:
            amount_input = input("持有金额（元）: ").strip()
            if not amount_input:
                print("Error: 持有金额不能为空")
                return False
            amount = float(amount_input)
        amount = float(amount)
        
        # 获取止盈目标（必填）
        if profit_target is None:
            pt_input = input("止盈目标%（必填）: ").strip()
            if not pt_input:
                print("Error: 止盈目标不能为空")
                return False
            profit_target = float(pt_input)
        profit_target = float(profit_target)
        
        # 获取止损线（必填）
        if stop_loss is None:
            sl_input = input("止损线%（必填）: ").strip()
            if not sl_input:
                print("Error: 止损线不能为空")
                return False
            stop_loss = float(sl_input)
        stop_loss = float(stop_loss)
        
        # 获取定投日（必填，0=不定投）
        if sip_day is None:
            sip_input = input("定投日（1-28，0=不定投，必填）: ").strip()
            if not sip_input:
                print("Error: 定投日不能为空")
                return False
            sip_day = int(sip_input)
        sip_day = int(sip_day)
        
        # 获取备注
        if not note:
            note = input("备注（可选）: ").strip()
        
        # 添加到文件
        self._add_fund_to_file(code, name, amount, profit_target, stop_loss, sip_day, note)
        
        print(f"\n✓ 已添加: {code} {name}")
        print(f"  持有金额: {amount} 元")
        print(f"  止盈目标: {profit_target}%")
        print(f"  止损线: {stop_loss}%")
        print(f"  定投日: 每月 {sip_day} 日" if sip_day > 0 else "  定投日: 不定投")
        print(f"  备注: {note}" if note else "")
        
        return True
    
    def _add_fund_to_file(self, code, name, amount, profit_target, stop_loss, sip_day, note):
        """添加基金到文件"""
        # 读取现有内容
        lines = []
        in_table = False
        table_header_found = False
        table_separator_found = False
        
        if self.my_funds_file.exists():
            with open(self.my_funds_file, "r", encoding="utf-8") as f:
                for line in f:
                    lines.append(line.rstrip('\n'))
        
        # 查找或创建表格
        table_header = "| 基金代码 | 基金名称 | 持有金额(元) | 持有收益 | 止盈% | 止损% | 定投日 | 备注 |"
        table_separator = "|---------|---------|-------------|---------|------|------|-------|------|"
        new_row = f"| {code} | {name} | {amount:.2f} | +0.00 | {profit_target} | {stop_loss} | {sip_day} | {note} |"
        
        # 检查表格是否存在
        has_table = any("基金代码" in line for line in lines)
        
        if not has_table:
            # 创建新表格
            lines.append("")
            lines.append(table_header)
            lines.append(table_separator)
            lines.append(new_row)
            lines.append("")
        else:
            # 在表格末尾添加
            for i, line in enumerate(lines):
                if line.strip().startswith("|") and "---" in line:
                    table_separator_found = True
                if table_separator_found and line.strip().startswith("|") and "---" not in line:
                    # 找到第一个数据行，继续找最后一行
                    pass
            
            # 简单处理：找到分隔行后，在最后一个数据行后添加
            last_data_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("|") and "---" not in line and "基金代码" not in line and line.strip() != "|":
                    parts = line.split("|")
                    if len(parts) >= 2 and parts[1].strip().isdigit():
                        last_data_idx = i
            
            if last_data_idx >= 0:
                lines.insert(last_data_idx + 1, new_row)
            else:
                # 找不到数据行，在分隔行后添加
                for i, line in enumerate(lines):
                    if "---" in line and line.strip().startswith("|"):
                        lines.insert(i + 1, new_row)
                        break
        
        # 写回文件
        with open(self.my_funds_file, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines) + '\n')
    
    def update_fund(self, code, **kwargs):
        """更新基金参数"""
        funds = self.get_fund_list()
        found = False
        
        lines = []
        with open(self.my_funds_file, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(line.rstrip('\n'))
        
        for i, line in enumerate(lines):
            if line.strip().startswith("|") and code in line:
                parts = line.split("|")
                if len(parts) >= 9 and parts[1].strip() == code:
                    # 更新指定字段
                    if 'amount' in kwargs:
                        parts[3] = f" {kwargs['amount']:.2f} "
                    if 'profit' in kwargs:
                        parts[4] = f" {kwargs['profit']} "
                    if 'profit_target' in kwargs:
                        parts[5] = f" {kwargs['profit_target']} "
                    if 'stop_loss' in kwargs:
                        parts[6] = f" {kwargs['stop_loss']} "
                    if 'sip_day' in kwargs:
                        parts[7] = f" {kwargs['sip_day']} "
                    if 'note' in kwargs:
                        parts[8] = f" {kwargs['note']} "
                    
                    lines[i] = "|".join(parts)
                    found = True
                    break
        
        if found:
            with open(self.my_funds_file, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines) + '\n')
            print(f"✓ 已更新: {code}")
        else:
            print(f"Error: 基金 {code} 不存在")
        
        return found

    def buy_fund(self, code, amount, name=None, fee_rate=0.0015, note=""):
        """买入基金
        
        Args:
            code: 基金代码
            amount: 买入金额（元）
            name: 基金名称（可选）
            fee_rate: 申购费率（默认0.15%）
            note: 备注
        
        Returns:
            dict: 交易记录
        """
        # 获取基金信息
        if not name:
            nav_data = self.get_fund_nav_estimate(code)
            if nav_data:
                name = nav_data.get("name", "")
            else:
                name = "Unknown"
        
        # 计算申购费和实际买入金额
        fee = round(amount * fee_rate, 2)
        actual_amount = amount - fee
        
        # 获取当前净值
        nav_data = self.get_fund_nav_estimate(code)
        nav = nav_data.get("current_nav", 1.0) if nav_data else 1.0
        
        # 计算买入份额
        shares = round(actual_amount / nav, 2) if nav > 0 else 0
        
        # 记录交易
        transaction = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "type": "buy",
            "code": code,
            "name": name,
            "amount": amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "actual_amount": actual_amount,
            "nav": nav,
            "shares": shares,
            "note": note,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.transactions.append(transaction)
        self._save_transactions()
        
        # 更新持仓
        self._update_holding_after_buy(code, name, amount, shares)
        
        return transaction
    
    def sell_fund(self, code, shares=None, amount=None, fee_rate=0.005, note=""):
        """卖出基金
        
        Args:
            code: 基金代码
            shares: 卖出份额（与amount二选一）
            amount: 卖出金额（元）
            fee_rate: 赎回费率（默认0.5%）
            note: 备注
        
        Returns:
            dict: 交易记录
        """
        # 获取基金信息
        nav_data = self.get_fund_nav_estimate(code)
        name = nav_data.get("name", "") if nav_data else "Unknown"
        nav = nav_data.get("current_nav", 1.0) if nav_data else 1.0
        
        # 计算卖出金额
        if shares:
            sell_amount = round(shares * nav, 2)
        elif amount:
            sell_amount = amount
            shares = round(amount / nav, 2) if nav > 0 else 0
        else:
            print("Error: 需要指定卖出份额或金额")
            return None
        
        # 计算赎回费
        fee = round(sell_amount * fee_rate, 2)
        actual_amount = sell_amount - fee
        
        # 记录交易
        transaction = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "type": "sell",
            "code": code,
            "name": name,
            "shares": shares,
            "amount": sell_amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "actual_amount": actual_amount,
            "nav": nav,
            "note": note,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.transactions.append(transaction)
        self._save_transactions()
        
        # 更新持仓
        self._update_holding_after_sell(code, shares, actual_amount)
        
        return transaction
    
    def _update_holding_after_buy(self, code, name, amount, shares):
        """买入后更新持仓"""
        # 简单实现：更新 my-funds.md
        funds = self.get_fund_list()
        found = False
        
        for fund in funds:
            if fund["code"] == code:
                # 已存在，更新金额
                new_amount = fund["amount"] + amount
                self.update_fund(code, amount=new_amount)
                found = True
                break
        
        if not found:
            # 不存在，需要添加
            print(f"\n新基金 {code} {name}")
            print(f"买入金额: {amount} 元")
            print(f"买入份额: {shares} 份")
            print("\n请使用 add 命令设置止盈止损参数：")
            print(f"  py fund_keeper.py add --fund {code} --name \"{name}\" --amount {amount} --profit <止盈> --stop <止损> --day 0")
    
    def _update_holding_after_sell(self, code, shares, actual_amount):
        """卖出后更新持仓"""
        funds = self.get_fund_list()
        
        for fund in funds:
            if fund["code"] == code:
                # 更新金额（简化处理）
                new_amount = max(0, fund["amount"] - actual_amount)
                if new_amount < 100:  # 清仓
                    print(f"\n✓ 已清仓 {code}")
                    # 可以选择删除记录或标记为0
                else:
                    self.update_fund(code, amount=new_amount)
                break
    
    def get_transactions(self, code=None, days=30):
        """获取交易记录
        
        Args:
            code: 基金代码（可选）
            days: 查询天数
        
        Returns:
            list: 交易记录列表
        """
        result = []
        cutoff = datetime.now() - timedelta(days=days)
        
        for t in self.transactions:
            try:
                t_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M:%S")
                if t_time >= cutoff:
                    if code is None or t["code"] == code:
                        result.append(t)
            except:
                pass
        
        return sorted(result, key=lambda x: x["time"], reverse=True)
    
    def print_transactions(self, code=None, days=30):
        """打印交易记录"""
        transactions = self.get_transactions(code, days)
        
        if not transactions:
            print("\n暂无交易记录\n")
            return
        
        print(f"\n【交易记录】最近 {days} 天\n")
        print(f"{'时间':<20} {'类型':<4} {'代码':<8} {'金额':>10} {'费用':>8} {'备注'}")
        print("-" * 70)
        
        total_buy = 0
        total_sell = 0
        total_fee = 0
        
        for t in transactions:
            type_str = "买入" if t["type"] == "buy" else "卖出"
            amount = t.get("amount", 0)
            fee = t.get("fee", 0)
            note = t.get("note", "")
            
            print(f"{t['time']:<20} {type_str:<4} {t['code']:<8} {amount:>10.2f} {fee:>8.2f} {note}")
            
            if t["type"] == "buy":
                total_buy += amount
            else:
                total_sell += amount
            total_fee += fee
        
        print("-" * 70)
        print(f"合计: 买入 {total_buy:.2f} 元 | 卖出 {total_sell:.2f} 元 | 费用 {total_fee:.2f} 元\n")
    
    def calculate_real_profit(self, code=None):
        """计算真实收益（含手续费）
        
        Returns:
            dict: 收益统计
        """
        buy_total = 0
        sell_total = 0
        fee_total = 0
        
        for t in self.transactions:
            if code and t["code"] != code:
                continue
            
            if t["type"] == "buy":
                buy_total += t.get("amount", 0)
            else:
                sell_total += t.get("actual_amount", 0)
            
            fee_total += t.get("fee", 0)
        
        # 当前持仓市值
        funds = self.get_fund_list()
        current_value = 0
        
        for fund in funds:
            if code and fund["code"] != code:
                continue
            
            nav_data = self.get_fund_nav_estimate(fund["code"])
            if nav_data:
                current_value += fund["amount"]
        
        # 真实收益 = 当前市值 + 已卖出金额 - 买入总金额 - 总手续费
        real_profit = current_value + sell_total - buy_total - fee_total
        
        return {
            "buy_total": buy_total,
            "sell_total": sell_total,
            "current_value": current_value,
            "fee_total": fee_total,
            "real_profit": real_profit,
            "profit_rate": (real_profit / buy_total * 100) if buy_total > 0 else 0
        }

    def check_alerts(self):
        """检查止盈止损提醒（分级）"""
        funds = self.get_fund_list()
        alerts = []
        
        for fund in funds:
            code = fund["code"]
            name = fund["name"]
            amount = fund.get("amount", 0)
            profit_target = fund.get("profit_target", 0)
            stop_loss = fund.get("stop_loss", 0)
            
            # 获取今日估值
            nav_data = self.get_fund_nav_estimate(code)
            if not nav_data:
                continue
            
            today_growth = nav_data.get("estimate_growth", 0)
            
            # 计算持有收益率（简化：从 profit 字段解析）
            profit_str = fund.get("profit", "0")
            try:
                profit_value = float(profit_str.replace("+", ""))
                profit_rate = (profit_value / amount * 100) if amount > 0 else 0
            except:
                profit_rate = 0
            
            # 止盈检查
            if profit_target > 0:
                if profit_rate >= profit_target:
                    # 触发止盈
                    alerts.append({
                        "level": "🔴 严重",
                        "type": "止盈触发",
                        "code": code,
                        "name": name,
                        "message": f"已达止盈线 {profit_target}%，当前收益 {profit_rate:.2f}%，建议卖出",
                        "action": "卖出"
                    })
                elif profit_rate >= profit_target - 1:
                    # 接近止盈（差1%）
                    alerts.append({
                        "level": "🟡 警告",
                        "type": "接近止盈",
                        "code": code,
                        "name": name,
                        "message": f"接近止盈线，当前收益 {profit_rate:.2f}%，距止盈差 {profit_target - profit_rate:.2f}%",
                        "action": "观察"
                    })
            
            # 止损检查
            if stop_loss > 0:
                if profit_rate <= -stop_loss:
                    # 触发止损
                    alerts.append({
                        "level": "🔴 严重",
                        "type": "止损触发",
                        "code": code,
                        "name": name,
                        "message": f"已跌破止损线 {stop_loss}%，当前亏损 {abs(profit_rate):.2f}%，建议止损",
                        "action": "卖出"
                    })
                elif profit_rate <= -stop_loss + 1:
                    # 接近止损（差1%）
                    alerts.append({
                        "level": "🟡 警告",
                        "type": "接近止损",
                        "code": code,
                        "name": name,
                        "message": f"接近止损线，当前亏损 {abs(profit_rate):.2f}%，距止损差 {abs(-stop_loss + 1 - profit_rate):.2f}%",
                        "action": "观察"
                    })
            
            # 今日涨跌幅提醒（超过3%）
            threshold = self.config.get("alert_threshold", 3.0)
            if abs(today_growth) >= threshold:
                alerts.append({
                    "level": "🔵 提示",
                    "type": "大幅波动",
                    "code": code,
                    "name": name,
                    "message": f"今日{'上涨' if today_growth > 0 else '下跌'} {abs(today_growth):.2f}%",
                    "action": "关注"
                })
        
        return alerts
    
    def print_alerts(self):
        """打印止盈止损提醒"""
        alerts = self.check_alerts()
        
        if not alerts:
            print("\n✅ 暂无止盈止损提醒\n")
            return
        
        # 按严重程度排序
        level_order = {"🔴 严重": 0, "🟡 警告": 1, "🔵 提示": 2}
        alerts.sort(key=lambda x: level_order.get(x["level"], 99))
        
        print("\n" + "="*60)
        print("【止盈止损提醒】")
        print("="*60 + "\n")
        
        for alert in alerts:
            print(f"{alert['level']} {alert['type']}")
            print(f"  基金：{alert['code']} {alert['name']}")
            print(f"  状态：{alert['message']}")
            print(f"  建议：{alert['action']}")
            print()
        
        print("="*60 + "\n")

    def get_gold_price(self):
        """获取国际金价（现货黄金）"""
        try:
            # 从新浪财经获取黄金价格
            url = "http://hq.sinajs.cn/list=autd"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "http://finance.sina.com.cn/futuremarket/"
            }
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text
                # 解析格式：var hq_str_autd="品种,开盘价,最新价,涨跌额,涨跌幅,..."
                import re
                match = re.search(r'="(.*?)"', content)
                if match:
                    parts = match.group(1).split(',')
                    if len(parts) >= 5:
                        return {
                            "name": "现货黄金",
                            "code": "AUTD",
                            "price": float(parts[2]) if parts[2] else 0,
                            "change": float(parts[3]) if parts[3] else 0,
                            "change_percent": float(parts[4].replace('%', '')) if parts[4] else 0,
                            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "source": "新浪财经"
                        }
        except Exception as e:
            pass
        
        # 备用：从东方财富获取
        try:
            url = "http://push2.eastmoney.com/api/qt/stock/get?secid=142.AUTD&fields=f43,f44,f45,f46,f47,f48"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    d = data["data"]
                    return {
                        "name": "现货黄金",
                        "code": "AUTD",
                        "price": d.get("f43", 0) / 100 if d.get("f43") else 0,
                        "change": d.get("f44", 0) / 100 if d.get("f44") else 0,
                        "change_percent": d.get("f45", 0) / 100 if d.get("f45") else 0,
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "source": "东方财富"
                    }
        except Exception as e:
            pass
        
        return None
    
    def get_silver_price(self):
        """获取白银价格（现货白银）"""
        try:
            # 从新浪财经获取白银价格
            url = "http://hq.sinajs.cn/list=agtd"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "http://finance.sina.com.cn/futuremarket/"
            }
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                content = response.text
                import re
                match = re.search(r'="(.*?)"', content)
                if match:
                    parts = match.group(1).split(',')
                    if len(parts) >= 5:
                        return {
                            "name": "现货白银",
                            "code": "AGTD",
                            "price": float(parts[2]) if parts[2] else 0,
                            "change": float(parts[3]) if parts[3] else 0,
                            "change_percent": float(parts[4].replace('%', '')) if parts[4] else 0,
                            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "source": "新浪财经"
                        }
        except Exception as e:
            pass
        
        # 备用：从东方财富获取
        try:
            url = "http://push2.eastmoney.com/api/qt/stock/get?secid=142.AGTD&fields=f43,f44,f45,f46,f47,f48"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    d = data["data"]
                    return {
                        "name": "现货白银",
                        "code": "AGTD",
                        "price": d.get("f43", 0) / 100 if d.get("f43") else 0,
                        "change": d.get("f44", 0) / 100 if d.get("f44") else 0,
                        "change_percent": d.get("f45", 0) / 100 if d.get("f45") else 0,
                        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "source": "东方财富"
                    }
        except Exception as e:
            pass
        
        return None
    
    def print_gold_report(self):
        """打印贵金属投资报告"""
        print("\n" + "="*60)
        print("【贵金属投资报告】")
        print("="*60 + "\n")
        
        # 获取国际金价
        gold_price = self.get_gold_price()
        if gold_price:
            print(f"现货黄金 (AUTD)")
            print(f"  最新价：{gold_price['price']:.2f} 元/克")
            print(f"  涨跌额：{gold_price['change']:+.2f} 元")
            print(f"  涨跌幅：{gold_price['change_percent']:+.2f}%")
            print(f"  数据源：{gold_price['source']}")
            print()
        else:
            print("⚠️ 黄金价格获取失败\n")
        
        # 获取白银价格
        silver_price = self.get_silver_price()
        if silver_price:
            print(f"现货白银 (AGTD)")
            print(f"  最新价：{silver_price['price']:.2f} 元/千克")
            print(f"  涨跌额：{silver_price['change']:+.2f} 元")
            print(f"  涨跌幅：{silver_price['change_percent']:+.2f}%")
            print(f"  数据源：{silver_price['source']}")
            print()
        else:
            print("⚠️ 白银价格获取失败\n")
        
        # 获取黄金基金数据
        gold_fund_code = "000218"
        nav_data = self.get_fund_nav_estimate(gold_fund_code)
        
        if nav_data:
            print(f"黄金基金 (000218 国泰黄金ETF联接A)")
            print(f"  当前净值：{nav_data['current_nav']:.4f}")
            print(f"  昨日净值：{nav_data['last_nav']:.4f}")
            print(f"  今日估值：{nav_data['estimate_growth']:+.2f}%")
            print()
            
            # 分析
            growth = nav_data['estimate_growth']
            
            print("【投资建议】")
            if growth < -3:
                print("  🔵 强烈建议补仓")
                print(f"  理由：今日大跌 {growth}%，黄金坑机会")
            elif growth < -2:
                print("  🟢 建议补仓")
                print(f"  理由：今日跌幅 {growth}%，达到补仓阈值")
            elif growth > 3:
                print("  🔴 建议部分止盈")
                print(f"  理由：今日大涨 +{growth}%，考虑止盈")
            elif growth > 2:
                print("  🟡 关注止盈机会")
                print(f"  理由：今日涨幅 +{growth}%，接近止盈线")
            else:
                print("  ⚪ 继续持有")
                print(f"  理由：今日波动 {growth:+.2f}%，未触发操作信号")
        else:
            print("⚠️ 黄金基金数据获取失败\n")
        
        print("\n" + "="*60 + "\n")

    def search_fund(self, keyword):
        """搜索基金
        
        Args:
            keyword: 搜索关键词（基金名称/代码）
        
        Returns:
            list: 匹配的基金列表
        """
        # 如果是6位数字，直接查询
        if keyword.isdigit() and len(keyword) == 6:
            detail = self.get_fund_detail(keyword)
            if detail:
                return [{
                    "code": detail["code"],
                    "name": detail["name"],
                    "type": detail.get("type", "未知")
                }]
            return []
        
        # 使用东方财富基金搜索 API
        try:
            url = "http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx"
            params = {
                "m": "9",
                "key": keyword,
                "_": str(int(datetime.now().timestamp() * 1000))
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "http://fund.eastmoney.com/"
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                text = response.text
                
                # 解析 JSONP 回调
                import re
                match = re.search(r'\((\[.*?\])\)', text, re.DOTALL)
                if match:
                    import json
                    data = json.loads(match.group(1))
                    
                    results = []
                    for item in data[:10]:
                        results.append({
                            "code": item.get("CODE", ""),
                            "name": item.get("NAME", ""),
                            "type": item.get("FundType", "未知")
                        })
                    
                    return results
        except Exception as e:
            pass
        
        # 备用：使用天天基金搜索
        try:
            url = "http://so.eastmoney.com/web/suggest?cb=jQuery&input=" + keyword
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "http://fund.eastmoney.com/"
            }
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                text = response.text
                
                # 解析返回数据
                import re
                results = []
                
                # 提取基金代码和名称
                pattern = r'"FundCode":"(\d+)".*?"FundName":"([^"]+)"'
                matches = re.findall(pattern, text)
                
                for code, name in matches[:10]:
                    results.append({
                        "code": code,
                        "name": name,
                        "type": self._get_fund_type(code)
                    })
                
                return results
        except Exception as e:
            pass
        
        return []
    
    def _get_fund_type(self, code):
        """获取基金类型"""
        # 简化版：根据代码前缀判断
        if code.startswith("00"):
            return "混合型"
        elif code.startswith("01"):
            return "债券型"
        elif code.startswith("16"):
            return "股票型"
        elif code.startswith("51"):
            return "ETF"
        elif code.startswith("15"):
            return "LOF"
        else:
            return "未知"
    
    def get_fund_detail(self, code):
        """获取基金详情"""
        try:
            url = f"http://fundgz.1234567.com.cn/js/{code}.js"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": f"http://fund.eastmoney.com/{code}.html"
            }
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                content = response.text
                if content.startswith("jsonpgz(") and content.endswith(");"):
                    import json
                    data = json.loads(content[8:-2])
                    
                    return {
                        "code": data.get("fundcode"),
                        "name": data.get("name"),
                        "type": data.get("fundtype", "未知"),
                        "current_nav": float(data.get("gsz", 0)),
                        "last_nav": float(data.get("dwjz", 0)),
                        "estimate_growth": float(data.get("gszzl", 0)),
                        "update_time": data.get("gztime", ""),
                        "manager": data.get("jzrq", ""),  # 基金经理（简化）
                        "scale": "未知"  # 规模
                    }
        except Exception as e:
            pass
        
        return None
    
    def print_search_results(self, keyword):
        """打印搜索结果"""
        print(f"\n【搜索基金】关键词: {keyword}\n")
        
        results = self.search_fund(keyword)
        
        if not results:
            print("未找到匹配的基金\n")
            return
        
        print(f"{'代码':<8} {'名称':<30} {'类型':<8}")
        print("-" * 50)
        
        for fund in results:
            print(f"{fund['code']:<8} {fund['name']:<30} {fund['type']:<8}")
        
        print(f"\n共找到 {len(results)} 支基金")
        print("\n查看详情: py fund_keeper.py search --fund <代码>\n")
    
    def print_fund_detail(self, code):
        """打印基金详情"""
        print(f"\n【基金详情】{code}\n")
        
        detail = self.get_fund_detail(code)
        
        if not detail:
            print("获取基金详情失败\n")
            return
        
        print(f"基金代码：{detail['code']}")
        print(f"基金名称：{detail['name']}")
        print(f"基金类型：{detail['type']}")
        print()
        print(f"当前净值：{detail['current_nav']:.4f}")
        print(f"昨日净值：{detail['last_nav']:.4f}")
        print(f"今日估值：{detail['estimate_growth']:+.2f}%")
        print(f"更新时间：{detail['update_time']}")
        print()
        print("添加到持仓:")
        print(f"  py fund_keeper.py add --fund {detail['code']} --name \"{detail['name']}\" --amount <金额> --profit <止盈> --stop <止损> --day 0\n")

    def show_config(self):
        """显示当前配置"""
        print("\n" + "="*60)
        print("【Fund Keeper 配置】")
        print("="*60 + "\n")
        
        print(f"  涨跌幅提醒阈值：{self.config.get('alert_threshold', 3.0)}%")
        
        print("\n" + "="*60)
        print("说明: 止盈/止损/定投日等参数在添加基金时单独设置")
        print("="*60 + "\n")

    def set_config(self, key, value):
        """修改配置项"""
        # 验证 key
        valid_keys = ['alert_threshold']
        
        if key not in valid_keys:
            print(f"Error: 无效的配置项 '{key}'")
            print(f"有效配置项: {', '.join(valid_keys)}")
            return False
        
        # 转换 value 类型
        try:
            value = float(value) if '.' in str(value) else int(value)
        except ValueError:
            print(f"Error: 无效的值 '{value}'")
            return False
        
        # 更新配置
        self.config[key] = value
        self._save_config(self.config)
        
        print(f"✓ 已更新: {key} = {value}")
        return True

    def reset_config(self):
        """重置为默认配置"""
        default_config = {
            "alert_threshold": 3.0
        }
        
        self.config = default_config
        self._save_config(default_config)
        
        print("✓ 已重置为默认配置")
        self.show_config()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Fund Keeper v2.7 - 基金智能顾问（离线模式、买卖记录、收益可视化、贵金属、基金搜索、持仓管理）")
    parser.add_argument("command", 
                       choices=["portfolio", "advice", "market", "add", "ocr", "stats", "sip", "stock", "config", "buy", "sell", "history", "alert", "trend", "gold", "search", "edit", "remove"],
                       help="命令：portfolio(持仓), advice(建议), market(市场), add(添加), ocr(识图), stats(收益), sip(定投), stock(股票), config(配置), buy(买入), sell(卖出), history(交易记录), alert(提醒), trend(趋势), gold(黄金), search(搜索), edit(编辑), remove(删除)")
    parser.add_argument("--fund", help="基金代码")
    parser.add_argument("--image", help="截图路径")
    parser.add_argument("--all", action="store_true", help="分析全部基金（包括定投）")
    parser.add_argument("--cross-validate", action="store_true", help="启用多数据源交叉验证")
    parser.add_argument("--offline", action="store_true", help="离线模式（仅使用缓存数据）")
    
    # stats 参数
    parser.add_argument("--chart", action="store_true", help="显示图表")
    
    # sip 参数
    parser.add_argument("--add", action="store_true", help="添加定投计划")
    parser.add_argument("--list", action="store_true", help="列出定投计划")
    parser.add_argument("--pause", help="暂停定投计划")
    parser.add_argument("--resume", help="恢复定投计划")
    parser.add_argument("--delete", help="删除定投计划")
    parser.add_argument("--name", help="基金名称")
    parser.add_argument("--amount", type=float, help="金额")
    parser.add_argument("--shares", type=float, help="份额（卖出时使用）")
    parser.add_argument("--day", type=int, help="每月定投日")
    parser.add_argument("--profit", type=float, help="止盈目标百分比")
    parser.add_argument("--stop", type=float, help="止损线百分比")
    parser.add_argument("--note", help="备注")
    
    # stock 参数
    parser.add_argument("--code", help="股票代码")
    parser.add_argument("--gainers", action="store_true", help="涨幅榜")
    parser.add_argument("--losers", action="store_true", help="跌幅榜")
    parser.add_argument("--count", type=int, default=10, help="榜单数量")
    
    # config 参数
    parser.add_argument("--set", dest="set_config", help="修改配置 (格式: key=value)")
    parser.add_argument("--show", action="store_true", help="显示当前配置")
    parser.add_argument("--reset", action="store_true", help="重置为默认配置")
    
    # edit/remove 参数
    parser.add_argument("--field", help="要编辑的字段（name/amount/profit/stop/day/note）")
    parser.add_argument("--value", help="新值")
    parser.add_argument("--force", action="store_true", help="强制删除（无需确认）")

    args = parser.parse_args()
    keeper = FundKeeper()

    if args.command == "portfolio":
        keeper.print_portfolio(cross_validate=args.cross_validate, offline=args.offline)
    elif args.command == "advice":
        keeper.print_advice(args.fund, exclude_sip=not args.all, cross_validate=args.cross_validate, offline=args.offline)
    elif args.command == "market":
        print("Market overview coming soon...")
    elif args.command == "ocr":
        if args.image:
            print("Starting OCR...\n")
            funds = keeper.add_fund_from_image(args.image)
            if funds:
                print("\nIdentified funds:\n")
                for fund in funds:
                    print(f"  Code: {fund['code']}, Name: {fund['name']}")
            else:
                print("No fund codes found")
        else:
            print("Please provide image path: --image <path>")
    elif args.command == "add":
        if args.fund:
            # 命令行模式
            keeper.add_fund_interactive(
                code=args.fund,
                name=args.name,
                amount=args.amount,
                profit_target=args.profit if hasattr(args, 'profit') and args.profit else None,
                stop_loss=args.stop if hasattr(args, 'stop') and args.stop else None,
                sip_day=args.day if hasattr(args, 'day') else None,
                note=args.note if hasattr(args, 'note') else None
            )
        elif args.image:
            # OCR 模式
            funds = keeper.add_fund_from_image(args.image)
            if funds:
                print("\n识别到的基金：")
                for fund in funds:
                    print(f"  {fund['code']} {fund['name']}")
                print("\n请使用以下命令添加到持仓：")
                print("  py fund_keeper.py add --fund <代码> --name <名称> --amount <金额>")
        else:
            # 交互式模式
            keeper.add_fund_interactive()
    elif args.command == "stats":
        from fund_stats import FundStats
        stats = FundStats(None)  # 使用默认路径
        stats.print_stats(show_chart=args.chart)
        stats.save_stats_history()  # 自动保存历史数据
    
    elif args.command == "trend":
        from fund_stats import FundStats
        stats = FundStats(None)  # 使用默认路径
        days = args.count if args.count else 7
        stats.print_trend_chart(days)
    
    elif args.command == "gold":
        keeper.print_gold_report()
    
    elif args.command == "search":
        if args.fund:
            # 查看指定基金详情
            keeper.print_fund_detail(args.fund)
        elif args.name:
            # 按名称搜索
            keeper.print_search_results(args.name)
        else:
            print("用法:")
            print("  py fund_keeper.py search --name 黄金      # 搜索黄金基金")
            print("  py fund_keeper.py search --fund 000218    # 查看基金详情")
    elif args.command == "sip":
        import os
        from fund_stats import SIPManager
        funds_dir = Path(os.path.abspath(os.path.join(os.getcwd(), "../../funds")))
        sip = SIPManager(funds_dir)
        
        if args.add:
            if not args.fund or not args.amount or not args.day:
                print("Error: --fund, --amount, and --day required")
                return
            name = args.name or "Unknown"
            sip.add_plan(args.fund, name, args.amount, args.day)
        elif args.list:
            sip.list_plans()
        elif args.pause:
            sip.pause_plan(args.pause)
        elif args.resume:
            sip.resume_plan(args.resume)
        elif args.delete:
            sip.delete_plan(args.delete)
        else:
            print("Specify action: --add, --list, --pause, --resume, --delete")
    
    elif args.command == "stock":
        from stock_data import StockData
        stock = StockData()
        
        if args.code:
            stock.print_quote(args.code)
        elif args.gainers:
            stock.print_top_gainers(args.count)
        elif args.losers:
            stock.print_top_losers(args.count)
        else:
            print("Usage: py fund_keeper.py stock --code 000001")
            print("       py fund_keeper.py stock --gainers")
            print("       py fund_keeper.py stock --losers")
    
    elif args.command == "config":
        if args.reset:
            keeper.reset_config()
        elif args.set_config:
            # 解析 key=value
            if '=' in args.set_config:
                key, value = args.set_config.split('=', 1)
                keeper.set_config(key.strip(), value.strip())
            else:
                print("Error: 格式错误，请使用 --set key=value")
                print("示例: --set profit_target_percent=10")
        else:
            # 默认显示配置
            keeper.show_config()
    
    elif args.command == "buy":
        if not args.fund or not args.amount:
            print("Error: --fund 和 --amount 必填")
            print("示例: py fund_keeper.py buy --fund 000218 --amount 1000 --note '补仓'")
            return
        
        transaction = keeper.buy_fund(
            code=args.fund,
            amount=args.amount,
            name=args.name,
            note=args.note or ""
        )
        
        print(f"\n✓ 买入成功")
        print(f"  基金：{transaction['code']} {transaction['name']}")
        print(f"  金额：{transaction['amount']:.2f} 元")
        print(f"  费用：{transaction['fee']:.2f} 元（费率 {transaction['fee_rate']*100:.2f}%）")
        print(f"  净值：{transaction['nav']:.4f}")
        print(f"  份额：{transaction['shares']:.2f} 份")
        print(f"  时间：{transaction['time']}\n")
    
    elif args.command == "sell":
        if not args.fund:
            print("Error: --fund 必填")
            print("示例: py fund_keeper.py sell --fund 000218 --amount 1000")
            print("      py fund_keeper.py sell --fund 000218 --shares 500")
            return
        
        if not args.amount and not args.shares:
            print("Error: --amount 或 --shares 必填其一")
            return
        
        transaction = keeper.sell_fund(
            code=args.fund,
            amount=args.amount,
            shares=args.shares,
            note=args.note or ""
        )
        
        if transaction:
            print(f"\n✓ 卖出成功")
            print(f"  基金：{transaction['code']} {transaction['name']}")
            print(f"  份额：{transaction['shares']:.2f} 份")
            print(f"  金额：{transaction['amount']:.2f} 元")
            print(f"  费用：{transaction['fee']:.2f} 元（费率 {transaction['fee_rate']*100:.2f}%）")
            print(f"  到账：{transaction['actual_amount']:.2f} 元")
            print(f"  净值：{transaction['nav']:.4f}")
            print(f"  时间：{transaction['time']}\n")
    
    elif args.command == "history":
        keeper.print_transactions(code=args.fund, days=args.count * 3 if args.count else 30)
    
    elif args.command == "alert":
        keeper.print_alerts()
    
    elif args.command == "edit":
        if not args.fund:
            print("Error: --fund 必填")
            print("示例: py fund_keeper.py edit --fund 000218")
            return
        keeper.edit_fund(args.fund, field=args.field if hasattr(args, 'field') else None, 
                         value=args.value if hasattr(args, 'value') else None)
    
    elif args.command == "remove":
        if not args.fund:
            print("Error: --fund 必填")
            print("示例: py fund_keeper.py remove --fund 000218")
            return
        keeper.remove_fund(args.fund, confirm=not args.force if hasattr(args, 'force') else True)


if __name__ == "__main__":
    main()
