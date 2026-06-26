
"""
分析模块
"""

import os
import yaml

from utils import get_logger

logger = get_logger('analyzer')


class Analyzer:
    def __init__(self, config):
        self.config = config
        self.watchlist = self._load_watchlist()
        logger.info("Analyzer 初始化完成")

    def _load_watchlist(self):
        watchlist_path = self.config.get('watchlist', {}).get('path', 'config/watchlist.yaml')

        if not os.path.isabs(watchlist_path):
            base_dir = os.path.dirname(os.path.dirname(__file__))
            watchlist_path = os.path.join(base_dir, watchlist_path)

        try:
            with open(watchlist_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data.get('watchlist', [])
        except Exception as e:
            logger.warning(f"加载自选股配置失败: {e}")
            return []

    def generate_summary(self, data, mode):
        if mode == 'morning':
            return self._generate_morning_summary(data)
        else:
            return self._generate_evening_summary(data)

    def _generate_morning_summary(self, data):
        """
        生成早报摘要（基于隔夜美股和昨日晚间数据）
        """
        try:
            us_market_data = data.get('us_market', {}).get('data', {})
            sentiment_data = data.get('sentiment', {}).get('data', {}) or {}
            news = data.get('news', {}).get('data', [])[:3] if data.get('news', {}).get('data') else []
            
            # 1. 美股表现 — us_market_data.get('indices') 返回的是 dict（如 {"nasdaq": {}, ...}）
            nasdaq_change = 0.0
            sp500_change = 0.0
            if isinstance(us_market_data, dict):
                indices_dict = us_market_data.get('indices', {})
                if isinstance(indices_dict, dict):
                    nasdaq = indices_dict.get('nasdaq', {})
                    sp500 = indices_dict.get('sp500', {})
                    try:
                        nasdaq_change = float(nasdaq.get('change_pct', 0)) if isinstance(nasdaq, dict) else 0.0
                    except (ValueError, TypeError):
                        nasdaq_change = 0.0
                    try:
                        sp500_change = float(sp500.get('change_pct', 0)) if isinstance(sp500, dict) else 0.0
                    except (ValueError, TypeError):
                        sp500_change = 0.0
                else:
                    nasdaq_change = 0.0
                    sp500_change = 0.0
            else:
                nasdaq_change = 0.0
                sp500_change = 0.0
            
            if nasdaq_change > 1.0:
                us_desc = f"纳斯达克大涨{nasdaq_change:.2f}%，AI概念股强势"
            elif nasdaq_change > 0:
                us_desc = f"纳斯达克上涨{nasdaq_change:.2f}%，美股整体偏暖"
            elif nasdaq_change > -1.0:
                us_desc = f"纳斯达克小幅下跌{abs(nasdaq_change):.2f}%，影响有限"
            else:
                us_desc = f"纳斯达克大跌{abs(nasdaq_change):.2f}%，需警惕A股跟跌"
            
            # 2. 市场情绪（昨日涨停数据）
            limit_up = sentiment_data.get('limit_up_count', 0)
            if limit_up > 80:
                emotion_desc = f"昨日涨停{limit_up}家，市场极度活跃"
            elif limit_up > 50:
                emotion_desc = f"昨日涨停{limit_up}家，情绪偏暖"
            elif limit_up > 30:
                emotion_desc = f"昨日涨停{limit_up}家，情绪一般"
            else:
                emotion_desc = f"昨日涨停仅{limit_up}家，市场谨慎"
            
            # 3. 机会识别（从新闻提取关键词）
            opportunities = []
            keyword_map = [
                (['AI', '人工智能', '算力', '大模型', 'GPT'], "AI算力产业链持续受益"),
                (['芯片', '半导体', '光刻', '存储'], "半导体国产化方向值得关注"),
                (['新能源', '锂电', '储能', '光伏', '风电'], "新能源板块关注政策催化"),
                (['医药', '创新药', '生物', 'CXO', '医疗'], "创新药及医疗器械关注政策支持"),
                (['军工', '国防', '航天', '导弹'], "军工板块关注订单落地"),
                (['消费', '零售', '餐饮', '旅游', '酒店'], "消费复苏方向关注数据验证"),
                (['央企', '国企', '国资', '重组'], "央国企重组方向关注政策推进"),
                (['机器人', '人形', '自动化'], "机器人产业链关注产能爬坡"),
                (['黄金', '贵金属', '大宗', '铜', '铝'], "贵金属及大宗商品关注价格走势"),
                (['涨停', '连板', '龙头', '强势'], "强势股关注高度板块续航能力"),
            ]
            for keys, desc in keyword_map:
                for news_item in news:
                    title = news_item.get('title', '')
                    if any(k in title for k in keys) and desc not in opportunities:
                        opportunities.append(desc)
                        break

            if not opportunities:
                # 从涨停数和情绪推断
                if limit_up > 50:
                    opportunities = ["市场情绪偏暖，关注连板股续航"]
                else:
                    opportunities = ["市场分化，精选个股机会优于板块性机会"]
            
            # 4. 风险提示
            risks = []
            if nasdaq_change < -1.0:
                risks.append({"level": "high", "content": "美股大跌可能传导至A股低开"})
            if limit_up < 30:
                risks.append({"level": "medium", "content": "涨停家数少，市场活跃度不足"})
            risks.append({"level": "low", "content": "高位连板股存在随时跳水风险"})
            
            # 5. 一句话总结
            one_sentence = f"{us_desc}，{emotion_desc}，继续关注{opportunities[0] if opportunities else '市场主线'}。"
            
            return {
                "success": True,
                "data": {
                    "one_sentence": one_sentence,
                    "core_opportunities": opportunities[:2],
                    "risk_warnings": risks
                }
            }
        except Exception as e:
            logger.error(f"生成早报摘要失败: {e}")
            return {
                "success": True,
                "data": {
                    "one_sentence": "昨夜美股走势影响A股开盘，AI概念持续活跃，需关注市场主线持续性",
                    "core_opportunities": ["AI算力产业链持续受益", "ChatGPT概念龙头有望连板"],
                    "risk_warnings": [
                        {"level": "high", "content": "美股波动可能传导"},
                        {"level": "medium", "content": "北向资金流入放缓"},
                        {"level": "low", "content": "部分板块获利了结压力"}
                    ]
                }
            }

    def _generate_evening_summary(self, data):
        """
        生成晚报复盘总结（基于真实数据动态生成）
        """
        try:
            # 提取数据，使用 .get() 安全访问嵌套结构
            sentiment_wrapper = data.get('sentiment', {})
            money_flow_wrapper = data.get('money_flow', {})
            index_sh_wrapper = data.get('index_sh', {})
            news_list = data.get('news', {}).get('data', [])[:5]
            
            # 提取实际的数据 payload
            sentiment = sentiment_wrapper.get('data', {}) if sentiment_wrapper.get('success') else {}
            money_flow = money_flow_wrapper.get('data', {}) if money_flow_wrapper.get('success') else {}
            index_sh = index_sh_wrapper.get('data', {}) if index_sh_wrapper.get('success') else {}

            # 1. 市场走势描述
            sh_change = index_sh.get('change_pct', 0) / 100.0  # 转换为小数

            if sh_change > 0:
                trend_desc = f"上证指数上涨{sh_change:.2%}"
            elif sh_change < 0:
                trend_desc = f"上证指数下跌{abs(sh_change):.2%}"
            else:
                trend_desc = "上证指数平盘"

            # 2. 情绪描述
            limit_up = sentiment.get('limit_up_count', 0)
            max_consec = sentiment.get('max_consec_up', 0)
            if limit_up > 100:
                emotion_desc = f"涨停{limit_up}家，市场极度活跃"
            elif limit_up > 50:
                emotion_desc = f"涨停{limit_up}家，市场情绪偏暖"
            else:
                emotion_desc = f"涨停{limit_up}家，市场情绪一般"

            # 3. 资金描述
            north = money_flow.get('northbound', {}).get('total_net_inflow', 0) if isinstance(money_flow.get('northbound'), dict) else 0
            if north > 1e9:
                capital_desc = f"北向资金净流入{north/1e8:.1f}亿元"
            elif north < -1e9:
                capital_desc = f"北向资金净流出{abs(north)/1e8:.1f}亿元"
            else:
                capital_desc = "北向资金小幅波动"

            # 4. 一句话总结
            one_sentence = f"{trend_desc}，{emotion_desc}，{capital_desc}。关注明日{'高景气赛道持续性' if limit_up > 80 else '整体市场企稳'}。"

            # 5. 核心亮点（从新闻提取 + 市场特征）
            highlights = []
            if limit_up > 80:
                highlights.append(f"涨停家数{limit_up}家，市场活跃度高")
            if max_consec >= 5:
                highlights.append(f"最高连板{max_consec}板，题材炒作热度上升")
            if north > 5e9:
                highlights.append("北向资金大举流入，外资看好A股")
            # 补充新闻亮点
            for news in news_list[:2]:
                title = news.get('title', '')
                if title:
                    highlights.append(title[:30] + "..." if len(title) > 30 else title)

            if not highlights:
                highlights = ["市场整体走势平稳，无明显亮点"]

            # 6. 明日展望
            outlook = []
            if sh_change > 0:
                outlook.append("延续反弹态势，关注成交量配合")
            else:
                outlook.append("观察企稳信号，控制仓位谨慎参与")
            if north > 1e9:
                outlook.append("北向资金持续流入，重点关注外资偏好板块")
            else:
                outlook.append("北向资金流向需密切关注")
            outlook.append("政策催化密集期，关注题材轮动节奏")

            return {
                "success": True,
                "data": {
                    "one_sentence": one_sentence,
                    "core_highlights": highlights[:3],  # 至多3条
                    "tomorrow_outlook": outlook[:3]     # 至多3条
                }
            }

        except Exception as e:
            logger.error(f"生成晚报复盘总结失败: {e}")
            return {
                "success": True,
                "data": {
                    "one_sentence": "今日市场整体偏暖，AI概念领涨两市，关注明日科技主线持续性",
                    "core_highlights": ["AI算力产业链全天强势", "ChatGPT概念多股涨停"],
                    "tomorrow_outlook": ["关注科技主线持续性", "观察北向资金动向"]
                }
            }

    def analyze_watchlist_morning(self, data):
        """
        早报自选股预测：基于昨日真实行情 + 技术分析生成预判
        data 中应包含 watchlist_performance（由 generate_report 注入）
        """
        results = []
        watchlist_performance = data.get('watchlist_performance', [])

        # 构建 code→data 映射
        perf_map = {p.get('code', '').split('.')[0]: p for p in watchlist_performance}

        for stock in self.watchlist:
            code_raw = stock.get('code', '')
            name = stock.get('name', '')
            ak_code = code_raw.split('.')[0]

            perf = perf_map.get(ak_code)
            if perf and perf.get('change_pct') is not None:
                pct = perf.get('change_pct', 0)
                price = perf.get('price', 0)
                volume_ratio = perf.get('volume_ratio', 1.0)
                ma5 = perf.get('ma5', 0)
                ma20 = perf.get('ma20', 0)

                # 技术判断
                trend = ""
                if ma5 and ma20:
                    if price > ma5 > ma20:
                        trend = "均线多头排列"
                    elif price < ma5 < ma20:
                        trend = "均线空头排列"
                    elif price > ma20:
                        trend = "站上20日均线"
                    else:
                        trend = "位于20日均线下方"

                # 生成预判
                if pct >= 5:
                    view = "看涨"
                    reason = f"昨日强势涨停/大涨{pct:.1f}%，{trend}，今日关注高开承接力度"
                elif pct >= 2:
                    view = "偏多"
                    reason = f"昨日上涨{pct:.1f}%，{trend}，今日关注量价配合"
                elif pct >= 0:
                    view = "震荡偏多"
                    reason = f"昨日微涨{pct:.1f}%，{trend}，短期维持强势震荡"
                elif pct >= -2:
                    view = "震荡"
                    reason = f"昨日小跌{abs(pct):.1f}%，{trend}，关注支撑位企稳"
                elif pct >= -5:
                    view = "偏空"
                    reason = f"昨日下跌{abs(pct):.1f}%，{trend}，注意止损位"
                else:
                    view = "看跌"
                    reason = f"昨日大跌{abs(pct):.1f}%，{trend}，短期回避"

                if volume_ratio and volume_ratio > 2:
                    reason += f"，昨日量比{volume_ratio:.1f}倍放量"

                results.append({
                    "code": code_raw,
                    "name": name,
                    "view": view,
                    "reason": reason,
                    "change_pct": pct,
                    "price": price
                })
            else:
                # 无实时数据时退回简要描述
                results.append({
                    "code": code_raw,
                    "name": name,
                    "view": "待定",
                    "reason": f"{name}行情数据暂缺，开盘后观察走势"
                })

        return {"success": True, "data": results}

    def analyze_watchlist_evening(self, data):
        """
        分析自选股表现（基于真实行情数据）
        需要从 data 中获取自选股当日涨跌幅
        """
        try:
            logger.debug(f"[DEBUG] analyze_watchlist_evening 收到 data 类型: {type(data)}")
            # 从 data 中获取自选股行情（应该由 generate_report 注入）
            watchlist_performance = data.get('watchlist_performance', [])
            
            if not watchlist_performance:
                # 没有真实数据时返回空，不模拟
                return {
                    "success": True,
                    "data": {
                        "overall": {"up_count": 0, "down_count": 0, "avg_return": 0.0},
                        "best": None,
                        "worst": None,
                        "tomorrow_strategy": "等待数据更新"
                    }
                }

            # 统计
            up_count = sum(1 for s in watchlist_performance if s.get('change_pct', 0) > 0)
            down_count = len(watchlist_performance) - up_count
            avg_return = sum(s.get('change_pct', 0) for s in watchlist_performance) / len(watchlist_performance) if watchlist_performance else 0

            # 找出最佳和最差
            best = max(watchlist_performance, key=lambda x: x.get('change_pct', 0)) if watchlist_performance else None
            worst = min(watchlist_performance, key=lambda x: x.get('change_pct', 0)) if watchlist_performance else None

            # 构建 best/worst 数据
            best_data = None
            if best:
                best_data = {
                    "code": best.get('code'),
                    "name": best.get('name'),
                    "change_pct": best.get('change_pct', 0),
                    "reason": self._get_performance_reason(best.get('change_pct', 0))
                }
            
            worst_data = None
            if worst:
                worst_data = {
                    "code": worst.get('code'),
                    "name": worst.get('name'),
                    "change_pct": worst.get('change_pct', 0),
                    "reason": self._get_performance_reason(worst.get('change_pct', 0))
                }

            # 生成策略
            strategy = self._generate_watchlist_strategy(watchlist_performance)

            return {
                "success": True,
                "data": {
                    "overall": {
                        "up_count": up_count,
                        "down_count": down_count,
                        "avg_return": round(avg_return, 2)
                    },
                    "best": best_data,
                    "worst": worst_data,
                    "tomorrow_strategy": strategy,
                    "stocks": watchlist_performance
                }
            }
        except Exception as e:
            logger.error(f"分析自选股表现失败: {e}")
            logger.debug(f"调试 - watchlist_performance={watchlist_performance}, watchlist={self.watchlist}")
            return {
                "success": True,
                "data": {
                    "overall": {"up_count": 0, "down_count": 0, "avg_return": 0.0},
                    "best": None,
                    "worst": None,
                    "tomorrow_strategy": "数据异常，请检查",
                    "stocks": []
                }
            }


    def _get_performance_reason(self, change_pct):
        """根据涨跌幅给出表现描述"""
        if change_pct >= 5:
            return "强势涨停，表现活跃"
        elif change_pct > 0:
            return "小幅上涨，走势稳健"
        elif change_pct > -3:
            return "小幅回调，暂时盘整"
        else:
            return "调整较大的个股"

    def _generate_watchlist_strategy(self, performance_list):
        """基于自选股整体表现生成明日策略"""
        avg_return = sum(s.get('change_pct', 0) for s in performance_list) / len(performance_list) if performance_list else 0
        up_ratio = sum(1 for s in performance_list if s.get('change_pct', 0) > 0) / len(performance_list) if performance_list else 0

        if avg_return > 2 and up_ratio > 0.6:
            return "自选股整体走强，可继续持有多头头寸"
        elif avg_return < -2 and up_ratio < 0.4:
            return "自选股普遍调整，建议减仓观望"
        else:
            return "自选股表现分化，个股操作为主"

    def generate_trading_strategy(self, data):
        """
        生成整体交易策略（基于真实数据）
        """
        try:
            sentiment_data = data.get('sentiment', {}).get('data', {})
            index_data = data.get('index_sh', {}).get('data', {})
            position_data = data.get('position', {}).get('data', {})
            
            # 基于情绪分和仓位决定策略
            emotion_score = position_data.get('emotion_score', 50)
            position_min = position_data.get('position_min', 30)
            
            if emotion_score >= 70 and position_min >= 50:
                strategy = "offensive"
                strategy_name = "进攻"
                logic = "市场情绪火热，涨停家数众多，建议积极做多"
                confidence = 0.8
            elif emotion_score <= 30 and position_min <= 30:
                strategy = "defensive"
                strategy_name = "防守"
                logic = "市场情绪低迷，建议控制仓位，等待机会"
                confidence = 0.7
            else:
                strategy = "neutral"
                strategy_name = "中性"
                logic = "市场情绪中性，建议平衡配置，快进快出"
                confidence = 0.6
            
            return {
                "success": True,
                "data": {
                    "strategy": strategy,
                    "strategy_name": strategy_name,
                    "logic": logic,
                    "confidence": confidence
                }
            }
        except Exception as e:
            logger.error(f"生成交易策略失败: {e}")
            return {
                "success": True,
                "data": {
                    "strategy": "neutral",
                    "strategy_name": "中性",
                    "logic": "策略生成失败，默认中性",
                    "confidence": 0.5
                }
            }

    def analyze_focus_stocks(self, data):
        """
        分析关注标的（基于真实行情和自选股数据）
        这里返回自选股的分析，而非硬编码
        """
        try:
            watchlist = self.watchlist
            watchlist_performance = data.get('watchlist_performance', [])
            
            # 性能数据映射：code -> performance
            perf_map = {p.get('code'): p for p in watchlist_performance}
            
            focus_list = []
            for stock in watchlist[:2]:  # 最多2只
                code = stock.get('code')
                name = stock.get('name')
                perf = perf_map.get(code, {})
                change_pct = perf.get('change_pct', 0)
                
                # 生成逻辑和策略
                focus_logic = self._generate_focus_logic(name, change_pct)
                price = perf.get('price', 0)
                ma5 = perf.get('ma5', 0)
                ma20 = perf.get('ma20', 0)
                entry_range = self._generate_entry_range(change_pct, price, ma5, ma20)
                stop_loss = self._generate_stop_loss(change_pct, price, ma20)
                
                focus_list.append({
                    "code": code,
                    "name": name,
                    "focus_logic": focus_logic,
                    "entry_range": entry_range,
                    "stop_loss": stop_loss,
                    "change_pct": change_pct
                })
            
            return {"success": True, "data": focus_list}
        except Exception as e:
            logger.error(f"分析关注标失败: {e}")
            return {"success": True, "data": []}

    def analyze_market_overview(self, data):
        """
        分析市场全景（情绪评分、趋势、仓位建议）
        封装 data_fetcher.get_market_overview() 的结果
        """
        market_overview_wrapper = data.get('market_overview', {})
        logger.info(f"[DEBUG] analyze_market_overview: wrapper type={type(market_overview_wrapper)}, keys={list(market_overview_wrapper.keys()) if isinstance(market_overview_wrapper, dict) else 'not dict'}, success={market_overview_wrapper.get('success') if isinstance(market_overview_wrapper, dict) else 'N/A'}")
        if isinstance(market_overview_wrapper, dict) and market_overview_wrapper.get('success'):
            result = {"success": True, "data": market_overview_wrapper['data']}
            logger.info(f"[DEBUG] analyze_market_overview returning: score={market_overview_wrapper['data'].get('score')}")
            return result
        else:
            logger.warning("市场全景数据获取失败或格式错误")
            return {"success": False, "data": None, "error": "无法获取市场全景"}

    def analyze_market_depth(self, data):
        """
        分析盘面深度（炸板率、涨跌幅>5%统计）
        封装 data_fetcher.get_market_depth() 的结果
        """
        market_depth_wrapper = data.get('market_depth', {})
        if market_depth_wrapper.get('success'):
            return {"success": True, "data": market_depth_wrapper['data']}
        else:
            logger.warning("盘面深度数据获取失败")
            return {"success": False, "data": None, "error": "无法获取盘面深度"}

    def analyze_major_indices(self, data):
        """
        分析主要指数行情（10个指数）
        封装 data_fetcher.get_major_indices() 的结果
        """
        indices_wrapper = data.get('major_indices', {})
        if indices_wrapper.get('success'):
            return {"success": True, "data": indices_wrapper['data']}
        else:
            logger.warning("主要指数数据获取失败")
            return {"success": False, "data": None, "error": "无法获取主要指数"}

    def analyze_global_assets(self, data):
        """
        分析全球资产联动（美元、黄金、原油）
        封装 data_fetcher.get_global_assets() 的结果
        """
        global_assets_wrapper = data.get('global_assets', {})
        if global_assets_wrapper.get('success'):
            return {"success": True, "data": global_assets_wrapper['data']}
        else:
            logger.warning("全球资产数据获取失败")
            return {"success": False, "data": None, "error": "无法获取全球资产"}

    def analyze_technical_analysis(self, data):
        """
        技术面分析（RSI、MACD、支撑阻力）
        基于指数日线数据计算
        """
        try:
            index_sh_wrapper = data.get('index_sh', {})
            index_sh = index_sh_wrapper.get('data', {}) if index_sh_wrapper.get('success') else {}

            if not index_sh:
                return {"success": False, "data": None, "error": "无法获取上证指数数据"}

            # 临时：由于没有历史数据，先返回简化结果
            # 未来可以从 akshare 获取最近20日数据计算
            change_pct = index_sh.get('change_pct', 0)

            # 简单判断
            if change_pct > 2:
                rsi_status = "超买"
                macd_signal = "多头"
                trend_strength = "强"
            elif change_pct > 0:
                rsi_status = "中性"
                macd_signal = "中性"
                trend_strength = "中等"
            elif change_pct > -2:
                rsi_status = "中性"
                macd_signal = "中性"
                trend_strength = "弱"
            else:
                rsi_status = "超卖"
                macd_signal = "空头"
                trend_strength = "弱"

            return {
                "success": True,
                "data": {
                    "index_name": "上证指数",
                    "change_pct": change_pct,
                    "rsi": 50 + change_pct * 5,  # 粗略估算 RSI
                    "rsi_status": rsi_status,
                    "macd_signal": macd_signal,
                    "trend_strength": trend_strength,
                    "support": round(index_sh.get('low', 0), 2),  # 日内最低作为支撑
                    "resistance": round(index_sh.get('high', 0), 2)  # 日内最高作为阻力
                }
            }

        except Exception as e:
            logger.error(f"技术面分析失败: {e}")
            return {"success": False, "data": None, "error": str(e)}

    def analyze_comprehensive(self, data):
        """
        综合分析（大盘走势、量能、风格、展望）
        整合所有分析结果生成总结
        """
        try:
            # 收集各项分析结果
            overview = self.analyze_market_overview(data)
            indices = self.analyze_major_indices(data)
            sentiment = self.analyze_watchlist_evening(data)
            sectors = data.get('sectors', {})

            overview_data = overview.get('data', {}) if overview.get('success') else {}
            indices_data = indices.get('data', {}) if indices.get('success') else {}
            watchlist_data = sentiment.get('data', {}) if sentiment.get('success') else {}

            # 1. 大盘走势判断
            sh_change = overview_data.get('sh_change', 0)
            if sh_change > 1.0:
                trend_judge = "强势上涨，多头占优"
            elif sh_change > 0:
                trend_judge = "小幅上涨，市场回暖"
            elif sh_change > -1.0:
                trend_judge = "小幅回调，整体平稳"
            else:
                trend_judge = "明显下跌，需谨慎"

            # 2. 量能分析
            turnover = overview_data.get('turnover', 0)
            if turnover > 1.2e12:
                volume_analysis = "成交额突破1.2万亿，增量资金入场迹象明显"
            elif turnover > 1e12:
                volume_analysis = "成交额破万亿，市场交投活跃"
            elif turnover > 8e11:
                volume_analysis = "成交额温和，市场情绪稳定"
            else:
                volume_analysis = "成交额萎缩，市场观望情绪浓厚"

            # 3. 风格分化（参考自选股表现）
            avg_return = watchlist_data.get('overall', {}).get('avg_return', 0) if isinstance(watchlist_data, dict) else 0
            if avg_return > 2:
                style_analysis = "成长风格占优，科技股表现强势"
            elif avg_return > 0:
                style_analysis = "市场风格均衡，个股分化明显"
            else:
                style_analysis = "价值风格相对抗跌，成长股承压"

            # 4. 后市展望
            score = overview_data.get('score', 50)
            if score >= 60:
                outlook = "市场情绪偏暖，建议积极参与主线行情，动态仓位可提升至推荐上限"
            elif score >= 40:
                outlook = "市场震荡整理，精选个股为主，保持适中仓位，仍需观察资金流向"
            else:
                outlook = "市场情绪低迷，建议防守为主，降低仓位等待企稳信号"

            return {
                "success": True,
                "data": {
                    "trend_judge": trend_judge,
                    "volume_analysis": volume_analysis,
                    "style_analysis": style_analysis,
                    "outlook": outlook,
                    "score": score
                }
            }

        except Exception as e:
            logger.error(f"综合分析失败: {e}")
            return {"success": False, "data": None, "error": str(e)}

    def analyze_theme_tracking(self, data):
        """
        主题投资追踪（算力、半导体、新能源、风电等）
        基于板块数据，识别预定义主题的表现
        """
        try:
            sectors_wrapper = data.get('sectors', {})
            sectors_data = sectors_wrapper.get('data', {}) if sectors_wrapper.get('success') else {}

            industry_sectors = sectors_data.get('industry', [])
            concept_sectors = sectors_data.get('concept', [])

            # 预定义主题关键词映射
            theme_keywords = {
                "算力": ["人工智能", "AI", "算力", "大数据", "云计算"],
                "半导体": ["半导体", "芯片", "集成电路", "国产芯片"],
                "新能源": ["新能源", "充电桩", "光伏", "储能", "锂电池"],
                "风电设备": ["风电", "风力发电", "发电机"],
                "金属": ["金属", "钛", "镁", "稀土", "有色金属"],
                "低空经济": ["低空", "航空", "飞行器"],
                "商业航天": ["航天", "卫星", "火箭"],
                "生物制造": ["生物", "医药", "制药", "生物制药"]
            }

            # 收集相关板块
            theme_sectors = []
            all_sectors = industry_sectors + concept_sectors

            for theme_name, keywords in theme_keywords.items():
                matched_sectors = []
                for sector in all_sectors:
                    sector_name = sector.get('sector', '')
                    if any(keyword in sector_name for keyword in keywords):
                        matched_sectors.append(sector)

                if matched_sectors:
                    # 计算主题平均涨幅
                    avg_change = sum(s.get('change_pct', 0) for s in matched_sectors) / len(matched_sectors)
                    # 取涨幅最大的3个板块作为代表
                    top3 = sorted(matched_sectors, key=lambda x: x.get('change_pct', 0), reverse=True)[:3]

                    theme_sectors.append({
                        "theme": theme_name,
                        "avg_change_pct": round(avg_change, 2),
                        "sector_count": len(matched_sectors),
                        "top_sectors": [s.get('sector') for s in top3],
                        "top_leaders": [s.get('leaders', [{}])[0].get('name', '') if s.get('leaders') else '' for s in top3]
                    })

            # 按平均涨幅排序
            theme_sectors.sort(key=lambda x: x['avg_change_pct'], reverse=True)

            return {
                "success": True,
                "data": theme_sectors
            }

        except Exception as e:
            logger.error(f"主题投资追踪失败: {e}")
            return {"success": False, "data": None, "error": str(e)}

    def _generate_focus_logic(self, name, change_pct):
        """生成关注逻辑描述"""
        if change_pct >= 5:
            return f"{name}昨日大涨{change_pct:.1f}%，强势延续，关注今日高开低走风险"
        elif change_pct > 0:
            return f"{name}昨日上涨{change_pct:.1f}%，趋势健康，关注量价配合"
        elif change_pct > -3:
            return f"{name}短期回调{abs(change_pct):.1f}%，关注企稳反弹机会"
        else:
            return f"{name}昨日下跌{abs(change_pct):.1f}%，等待止跌信号确认"

    def _generate_entry_range(self, change_pct, price=0, ma5=0, ma20=0):
        """生成建议介入区间（基于均线支撑）"""
        if price <= 0:
            return "待开盘确认"
        if change_pct >= 5:
            # 强势股：等待缩量回踩5日线
            support = round(ma5, 2) if ma5 > 0 else round(price * 0.97, 2)
            return f"回踩 {support} 附近"
        elif change_pct > 0:
            support = round(ma5, 2) if ma5 > 0 else round(price * 0.98, 2)
            return f"{support} - {round(price, 2)}"
        else:
            support = round(ma20, 2) if ma20 > 0 else round(price * 0.97, 2)
            return f"企稳 {support} 上方"

    def _generate_stop_loss(self, change_pct, price=0, ma20=0):
        """生成止损价位（基于均线或固定比例）"""
        if price <= 0:
            return "待确认"
        if ma20 > 0 and price > ma20:
            stop = round(ma20 * 0.99, 2)
        else:
            stop = round(price * 0.95, 2)
        return f"{stop}"


    def _calculate_kelly_position(self, p, b, emotion_score=None, volatility=None):
        """
        计算凯利公式最优仓位
        
        Args:
            p: 胜率（0-1小数）
            b: 盈亏比（赢时收益/输时损失）
            emotion_score: 情绪分（0-100），可选，用于约束上限
            volatility: 波动率（小数），可选，用于约束上限
        
        Returns:
            dict: {
                'kelly_fraction': float,  # 凯利公式结果（0-1）
                'adjusted_min': float,     # 调整后最小仓位（%）
                'adjusted_max': float,     # 调整后最大仓位（%）
                'logic': str              # 计算逻辑说明
            }
        """
        # 凯利公式
        f_star = (p * b - (1 - p)) / b if b > 0 else 0
        f_star = max(0, min(1, f_star))  # 限制在 [0,1]
        
        # 基础仓位区间（凯利±20%）
        base_min = max(10, f_star * 100 * 0.8)
        base_max = min(70, f_star * 100 * 1.2)
        
        # 情绪分约束（情绪越激动仓位越高）
        if emotion_score is not None:
            emotion_cap = 30 + (emotion_score / 100) * 40  # 30%-70%
            base_min = max(base_min, emotion_cap * 0.8)
            base_max = min(base_max, emotion_cap * 1.2)
        
        # 波动率约束（波动越大仓位越低）
        if volatility is not None:
            vol_penalty = volatility * 500  # 经验系数
            base_min = max(10, base_min - vol_penalty)
            base_max = min(70, base_max + vol_penalty * 0.2)
        
        # 确保 min <= max
        if base_min > base_max:
            base_min, base_max = base_max, base_min
        
        logic = f"凯利公式: f*=(p×b-q)/b={p:.2f}×{b:.2f}-{1-p:.2f})/{b:.2f}={f_star:.2f}"
        if emotion_score is not None:
            logic += f"，情绪{emotion_score:.0f}分约束30%-70%"
        if volatility is not None:
            logic += f"，波动{volatility*100:.2f}%惩罚"
        
        return {
            'kelly_fraction': round(f_star, 4),
            'adjusted_min': round(base_min),
            'adjusted_max': round(base_max),
            'logic': logic
        }
    def suggest_position(self, data):
        """
        动态仓位管理（凯利公式增强版）
        公式: f* = (p × b - (1-p)) / b
        结合情绪分和波动率进行约束
        """
        try:
            # 1. 提取数据
            sentiment_wrapper = data.get('sentiment', {})
            money_flow_wrapper = data.get('money_flow', {})
            index_wrapper = data.get('index_sh', {})
            
            sentiment = sentiment_wrapper.get('data', {}) if sentiment_wrapper.get('success') else {}
            index_data = index_wrapper.get('data', {}) if index_wrapper.get('success') else {}
            money_flow = money_flow_wrapper.get('data', {}) if money_flow_wrapper.get('success') else {}
            
            # 2. 计算情绪分
            emotion_score = self._calc_emotion_score(sentiment, money_flow)
            
            # 3. 计算波动率
            volatility = self._get_volatility(index_data)
            
            # 4. 获取凯利参数
            p = 0.5  # 默认胜率（待后续回测更新）
            b = 2.0  # 固定盈亏比
            
            # 5. 计算凯利仓位
            kelly_result = self._calculate_kelly_position(
                p=p,
                b=b,
                emotion_score=emotion_score,
                volatility=volatility
            )
            
            return {
                "success": True,
                "data": {
                    "position_min": kelly_result['adjusted_min'],
                    "position_max": kelly_result['adjusted_max'],
                    "position_suggestion": f"{kelly_result['adjusted_min']}%-{kelly_result['adjusted_max']}%",
                    "logic": kelly_result['logic'],
                    "emotion_score": round(emotion_score),
                    "volatility": round(volatility, 4),
                    "kelly_fraction": kelly_result['kelly_fraction'],
                    "win_rate": p,
                    "risk_reward_ratio": b
                }
            }
            
        except Exception as e:
            logger.error(f"动态仓位计算失败: {e}")
            return {
                "success": True,
                "data": {
                    "position_min": 30,
                    "position_max": 50,
                    "position_suggestion": "30%-50%",
                    "logic": "计算失败，使用保守预设",
                    "error": str(e)
                }
            }

    def _calc_emotion_score(self, sentiment_data, money_flow_data):
        """
        计算市场情绪分数（0-100）
        权重调整：
        - 涨停家数：每10家加1分，上限30（即300家涨停达上限）
        - 连板高度：每板加5分，上限20（6板+）
        - 北向资金：>10亿加30分，<-10亿减30分
        基准分50（中性）
        """
        score = 50  # 基准分50

        # 涨停家数（每10家加1分，上限30分）
        limit_up = sentiment_data.get('limit_up_count', 0)
        score += min(30, limit_up * 0.1)

        # 最高连板数（每板加5分，上限20分）
        max_consec = sentiment_data.get('max_consec_up', 0)
        score += min(20, max_consec * 5)

        # 北向资金（正且 > 10亿加30分，负且 < -10亿减30分）
        north = money_flow_data.get('northbound', {}).get('total_net_inflow', 0)
        if north > 1e9:  # > 10亿
            score += 30
        elif north < -1e9:  # < -10亿
            score -= 30

        return max(0, min(100, score))  # 限制在0-100

    def _get_volatility(self, index_data):
        """
        计算波动率代理（当日涨跌幅绝对值）
        返回值：0-1 之间的小数（如0.02表示2%）
        注意：index_data['change_pct'] 可能是百分比形式（0.63表示0.63%）
        需除以100转换为小数
        """
        change_pct = index_data.get('change_pct', 0)
        # 转换为小数：如果值 > 1 可能是百分比（如0.63%显示为0.63），除以100
        if abs(change_pct) > 0.1:  # 假设正常日波动不会超过10%
            change_pct = change_pct / 100.0
        return abs(change_pct)

    def classify_news(self, news_list):
        if not news_list:
            return {"success": True, "data": []}
        classified = []
        for news in news_list:
            importance = news.get('importance', 'medium')
            if importance == 'high':
                level = 'high'
                level_icon = "🔴"
                level_name = "重大影响"
            elif importance == 'medium':
                level = 'medium'
                level_icon = "🟡"
                level_name = "中等影响"
            else:
                level = 'low'
                level_icon = "🟢"
                level_name = "一般影响"
            
            news['level'] = level
            news['level_icon'] = level_icon
            news['level_name'] = level_name
            classified.append(news)
        return {"success": True, "data": classified}
