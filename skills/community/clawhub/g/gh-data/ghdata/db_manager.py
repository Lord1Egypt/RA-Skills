"""
数据库管理器 — 通过 WebAPI HTTP 接口访问
技能包唯一依赖的端点：POST /api/klineanalyze, POST /api/screen

可用端点：
  POST /klineanalyze    → 全量分析（含匹配率/规律/统计/信号/技术指标）
  POST /screen          → 条件筛选（方向/评分统计）
"""
import time
import requests
from typing import Optional, Any
from . import config

_session = requests.Session()
_session.headers.update({
    "User-Agent": "ghdataskill/1.0",
    "Content-Type": "application/json",
})

# ===== 购买链接（token化，v2.2.50）=====
# 平台支持：POST /api/key/get-token（Key→token）→ 购买页 ?token= → 服务端解析下单
# 不再把完整 APIKey 拼进 URL；token 获取失败时降级为购买页链接（不含Key，防日志泄露）
_GET_TOKEN_URL = "https://payskl.smtso.com/ghdata/api/key/get-token"
_PAYMENT_CACHE: dict = {"ts": 0.0, "url": ""}
_PAYMENT_CACHE_TTL = 300  # 5秒缓存? 不，5分钟；平台token短时有效，客户端避免频繁请求


def get_payment_url() -> str:
    """
    生成购买链接 — 优先使用平台短时 token（URL 不含完整 APIKey）

    流程：POST _GET_TOKEN_URL {"apiKey": config.API_KEY}
          → data.payUrl（含 ?token=xxx）
    失败时降级为购买页链接（不含Key，平台故障/无token时兜底，防止凭证泄露）
    """
    now = time.time()
    if _PAYMENT_CACHE["url"] and now - _PAYMENT_CACHE["ts"] < _PAYMENT_CACHE_TTL:
        return _PAYMENT_CACHE["url"]

    if not config.API_KEY:
        return "https://www.oraskl.com/ghdata-admin"

    try:
        resp = requests.post(
            _GET_TOKEN_URL,
            json={"apiKey": config.API_KEY},
            timeout=min(config.TIMEOUT, 10),
        )
        if resp.status_code == 200:
            body = resp.json()
            if body.get("code") == 0:
                pay_url = (body.get("data") or {}).get("payUrl")
                if pay_url:
                    _PAYMENT_CACHE["ts"] = now
                    _PAYMENT_CACHE["url"] = pay_url
                    return pay_url
            print(f"[db] get-token 返回异常: {body}")
        else:
            print(f"[db] get-token 返回 {resp.status_code}")
    except Exception as e:
        print(f"[db] get-token 失败，返回购买页链接（不含Key）: {e}")

    # 安全兜底：绝不把完整 APIKey 拼进 URL（查询参数会被浏览器/代理/服务器日志记录，导致凭证泄露）
    return "https://www.oraskl.com/ghdata-admin"


def _url(path: str) -> str:
    return f"{config.WEBAPI_BASE_URL}/{path.lstrip('/')}"


def _post(path: str, json_body: dict = None, raw: bool = False) -> Optional[Any]:
    """POST 并解包 result.data（WebAPI 返回结构：{result:{data:{...}}}）

    默认返回解包后的 data；非200状态返回 None。
    raw=True 时返回完整响应（含状态码），供调用方判断具体错误原因。
    """
    try:
        resp = _session.post(_url(path), json=json_body or {}, timeout=config.TIMEOUT)
        if resp.status_code not in (200, 201):
            # 读取服务端错误信息，便于调试和降级提示
            try:
                err = resp.json()
                error_msg = err.get("error", str(err))
            except Exception:
                error_msg = resp.text or f"HTTP {resp.status_code}"
            print(f"[db] {path} 返回 {resp.status_code}: {error_msg}")
            return None
        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            # 再解一层：result.data → 直接返回 data 内容
            if isinstance(r, dict) and "data" in r:
                return r["data"]
            return r
        return data
    except Exception as e:
        print(f"[db] POST {path} 失败: {e}")
        return None


# ===== 核心分析接口（唯一依赖）=====

def kline_teaser(code: str) -> dict:
    """
    POST /klineanalyze/teaser — 免费预览
    无APIKey验证，仅返回基础技术指标（MA/MACD/KDJ/RSI/信号汇总）
    用于APIKey无效时向客户展示1-2行真实数据作为试看
    返回数据中包含 _payment_url 供LLM生成购买链接
    """
    body = {"code": code}
    data = _post("klineanalyze/teaser", body)
    if data and isinstance(data, dict) and not data.get("error"):
        return {
            "preview": True,
            "indicators": data.get("indicators"),
            "signals": data.get("signals"),
            "realtime": data.get("realtime"),
            "_payment_url": get_payment_url(),
        }
    return {}


def kline_analyze(code: str, today_kline: dict = None) -> dict:
    """
    POST /klineanalyze — 全量分析
    服务端计算：技术指标 + 信号 + 规律 + 匹配率 + 摘要
    这是技能包唯一调用的WebAPI接口
    自动传入全局APIKey用于验证

    当APIKey无效/免费次数用完/服务端故障时，自动降级调用 kline_teaser() 返回基础预览数据。
    降级时返回的数据中会携带 _error_info 字段说明原因。
    所有返回路径均包含 _payment_url 供LLM生成购买链接。
    """
    body = {"code": code}
    if config.API_KEY:
        body["apiKey"] = config.API_KEY
    if today_kline:
        body["todayKline"] = today_kline
    payment_url = get_payment_url()
    data = _post("klineanalyze", body)
    if data and isinstance(data, dict):
        # 检测无效APIKey错误（服务端返回含 code/message 时的分支）
        if data.get("code") == 1 or (data.get("message") and "APIKey" in str(data.get("message", ""))):
            teaser = kline_teaser(code)
            if teaser:
                teaser["_error_info"] = data.get("message", "APIKey 无效，已降级为免费预览")
                if "_payment_url" not in teaser:
                    teaser["_payment_url"] = payment_url
            return teaser
        # 正常返回完整数据，附上 _payment_url
        data["_payment_url"] = payment_url
        return data
    # 非200状态码/网络错误等 → 降级为teaser并说明原因
    teaser = kline_teaser(code)
    if teaser:
        teaser["_error_info"] = "免费版本每日每工具限3次，已用尽或APIKey未激活，已降级为预览模式"
        if "_payment_url" not in teaser:
            teaser["_payment_url"] = payment_url
    return teaser


# ===== 个股行为画像（方案B数据）=====


def kline_analyze_v3(code: str, today_kline: dict = None) -> dict:
    """
    POST /klineanalyze/v3 — 全量分析v3（融合ETF资金流+券商研报）
    在 v2 基础上增加：
      - factors.etf_factor: ETF板块资金支撑/压力评分
      - factors.research_factor: 券商研报共识评分
      - factors.raw_score: 原始K线评分
      - factors.adjusted_score: 调整后评分
      - factors.etf_summary / research_summary: 解读文本

    当APIKey无效时，自动降级调用 kline_teaser() 返回基础预览数据
    """
    body = {"code": code}
    if config.API_KEY:
        body["apiKey"] = config.API_KEY
    if today_kline:
        body["todayKline"] = today_kline
    data = _post("klineanalyze/v3", body)
    if data and isinstance(data, dict):
        if data.get("code") == 1 or (data.get("message") and "APIKey" in str(data.get("message", ""))):
            teaser = kline_teaser(code)
            return teaser
        return data
    teaser = kline_teaser(code)
    return teaser


# ===== 个股行为画像（方案B数据）=====

def get_stock_profile(code: str) -> dict:
    """
    从 klineanalyze 结果中提取个股行为画像数据
    包含：估值分析、多周期技术分析、资金面画像、季节性规律等
    返回原始 stockProfile 字典，LLM可直接解析展示
    """
    result = kline_analyze(code)
    return result.get("stockProfile", {}) or {}


# ===== 匹配率统计 =====

def get_match_stats(code: str, days: int = 36500) -> dict:
    """
    从 klineanalyze 响应中提取方向匹配率
    accuracy 结构: { all:{total,correct,rate}, period30:{...}, period60:{...} }
    """
    result = kline_analyze(code)
    acc = result.get("accuracy", {})

    if days >= 36500:
        stats = acc.get("all", {})
    elif days >= 60:
        stats = acc.get("period60", {})
    else:
        stats = acc.get("period30", {})

    if stats:
        return {
            "total": stats.get("total", 0),
            "correct": stats.get("correct", 0),
            "rate": round(stats.get("rate", 0), 1),
        }
    return {"total": 0, "correct": 0, "rate": 0}


# ===== 最新信号 =====

def get_latest_signals(code: str, limit: int = 30) -> list:
    """从 klineanalyze 提取最新信号"""
    result = kline_analyze(code)
    lp = result.get("latestPrediction", {}) or {}
    if lp:
        return [{
            "predict_date": lp.get("predictDate", ""),
            "direction": lp.get("direction", ""),
            "total_score": lp.get("totalScore", 0),
            "range_forecast": lp.get("rangeForecast", ""),
            "t1_direction": lp.get("t1Direction", ""),
            "t2_direction": lp.get("t2Direction", ""),
            "weekly_direction": lp.get("weeklyDirection", ""),
            "vote_detail": lp.get("voteDetail", ""),
        }]
    return []


# ===== 规律数据 =====

def get_patterns(code: str) -> list:
    """从 klineanalyze 提取规律"""
    result = kline_analyze(code)
    patterns = result.get("patterns", [])
    if patterns and isinstance(patterns, list):
        return [{
            "pattern_type": p.get("name", ""),
            "description": p.get("advice", ""),
            "avg_d3": p.get("avgD3", ""),
            "samples": p.get("samples", []),
        } for p in patterns]
    return []


def get_learning_summary(code: str) -> list:
    """从 klineanalyze 提取自学习摘要"""
    result = kline_analyze(code)
    return result.get("learningSummary", []) or []


# ===== 经验数据 =====

def get_experience(code: str) -> Optional[dict]:
    """从 klineanalyze 结果中提取经验摘要"""
    result = kline_analyze(code)
    if result:
        return {
            "stock_code": code,
            "stock_name": result.get("name", ""),
            "direction": result.get("latestPrediction", {}).get("direction", ""),
            "total_score": result.get("latestPrediction", {}).get("totalScore", 0),
            "accuracy_rate": result.get("accuracy", {}).get("all", {}).get("rate", 0),
        }
    return None


# ===== 条件筛选 =====

def screen_stocks(directions: list = None, min_score: float = None,
                  min_accuracy: float = None, min_correct_count: int = None,
                  sort_by: str = "score", top: int = 20, page: int = 1) -> dict:
    """
    POST /api/screen — 条件筛选
    基于 experience + accuracy_tracking 表筛选符合条件的股票

    参数:
        directions:     方向过滤，如 ["偏多","震荡偏多"]（不传查全部）
        min_score:      最低综合评分（0-10）
        min_accuracy:   最低匹配率（%，如 60）
        min_correct_count: 最少正确次数
        sort_by:        排序字段：score(默认) / accuracy
        top:            每页条数，默认20
        page:           页码，默认1

    返回:
        { total: 总数, page: 页码, top: 每页条数,
          stocks: [{ code, name, direction, score, accuracy }] }

    示例:
        >>> screen_stocks(directions=["偏多"], min_score=5.0, min_accuracy=60, top=10)
    """
    body = {"top": top, "page": page, "sortBy": sort_by}
    if directions:
        body["directions"] = directions
    if min_score is not None:
        body["minScore"] = min_score
    if min_accuracy is not None:
        body["minAccuracy"] = min_accuracy
    if min_correct_count is not None:
        body["minCorrectCount"] = min_correct_count
    if config.API_KEY:
        body["apiKey"] = config.API_KEY

    data = _post("screen", body)
    if data and isinstance(data, dict):
        inner = data.get("data")
        if inner is not None:
            return inner
        return data
    return {"total": 0, "page": page, "top": top, "stocks": []}


def advanced_screen(mode: str = "momentum", base_directions: list = None,
                    base_min_score: float = None, base_min_accuracy: float = None,
                    momentum_chg20: float = None, momentum_ma_only: bool = False,
                    reversal_rsi: float = None, reversal_oversold: bool = False,
                    tech_ma_bullish: bool = False, tech_macd_golden: bool = False,
                    tech_vol_surge: bool = False,
                    sort_by: str = "score", top: int = 20) -> dict:
    """
    POST /api/screen/advanced — 高级筛选（动量/反转/技术信号）

    参数:
        mode: "momentum"(动量) / "reversal"(反转) / "techsignal"(技术信号)
        base_directions: 基础方向过滤
        base_min_score: 基础最低评分
        base_min_accuracy: 基础最低匹配率
        momentum_chg20: 最低近20日涨幅(%)
        momentum_ma_only: 仅均线多头
        reversal_rsi: RSI低于此值
        reversal_oversold: 超卖+MACD金叉
        tech_ma_bullish: 均线多头
        tech_macd_golden: MACD金叉
        tech_vol_surge: 放量
        sort_by: score / chg20 / rsi
        top: 最多返回条数

    返回:
        { total: 总数, stocks: [{ code, name, direction, score, accuracy,
          maStatus, chg20, rsi14, macdBar, volRatio, matchReasons }] }
    """
    body = {"mode": mode, "top": top, "sortBy": sort_by}
    if base_directions: body["baseDirections"] = base_directions
    if base_min_score is not None: body["baseMinScore"] = base_min_score
    if base_min_accuracy is not None: body["baseMinAccuracy"] = base_min_accuracy
    if momentum_chg20 is not None: body["momentumChg20"] = momentum_chg20
    if momentum_ma_only: body["momentumMAOnly"] = True
    if reversal_rsi is not None: body["reversalRSI"] = reversal_rsi
    if reversal_oversold: body["reversalOversold"] = True
    if tech_ma_bullish: body["techMABullish"] = True
    if tech_macd_golden: body["techMACDGolden"] = True
    if tech_vol_surge: body["techVolSurge"] = True
    if config.API_KEY:
        body["apiKey"] = config.API_KEY

    data = _post("screen/advanced", body)
    if data and isinstance(data, dict):
        inner = data.get("data")
        return inner if inner is not None else data
    return {"total": 0, "stocks": []}


# ===== 行业ETF资金流向 =====

def get_etf_flow(code: str, days: int = 15) -> dict:
    """
    GET /api/etf/industry-flow/{code}?days=N
    查询个股关联的行业ETF资金流向
    返回: { matched_etfs: [...], etf_flow: {code: [...]}, summary: "..." }
    """
    try:
        resp = _session.get(
            _url(f"etf/industry-flow/{code}"),
            params={"days": days},
            timeout=config.TIMEOUT
        )
        if resp.status_code not in (200, 201):
            return {"matched_etfs": [], "etf_flow": {}, "summary": "ETF数据暂不可用"}
        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            if isinstance(r, dict) and "data" in r:
                result = r["data"]
            else:
                result = r
        else:
            result = {"matched_etfs": [], "etf_flow": {}, "summary": "ETF数据格式异常"}

        # ---- 本地兜底映射 ----
        # 当API的 stock_etf_mapping 表无匹配时，用本地字典补全
        if not result.get("matched_etfs"):
            summary = result.get("summary", "")
            for kw, (ecode, ename) in _LOCAL_ETF_MAP.items():
                if kw in summary:
                    result["matched_etfs"] = [{"code": ecode, "name": ename}]
                    result["summary"] = "（本地映射，无逐日资金流明细）"
                    break
        return result

    except Exception as e:
        print(f"[db] get_etf_flow({code}) 失败: {e}")
        return {"matched_etfs": [], "etf_flow": {}, "summary": "ETF数据请求失败"}


# 本地ETF兜底映射：行业关键词 → (ETF代码, ETF名称)
# 当WebAPI的 stock_etf_mapping 表未覆盖时使用
_LOCAL_ETF_MAP = {
    "石油石化": ("159930", "石油ETF"),
    "炼化":     ("159930", "石油ETF"),
    "炼油":     ("159930", "石油ETF"),
    "煤炭":     ("515220", "煤炭ETF"),
    "有色金属": ("512400", "有色金属ETF"),
    "黄金":     ("159812", "黄金ETF"),
    "化工":     ("159870", "化工ETF"),
    "化学制品": ("159870", "化工ETF"),
    "化学原料": ("159870", "化工ETF"),
    "电子":     ("159997", "电子ETF"),
    "半导体":   ("512480", "半导体ETF"),
    "芯片":     ("159995", "芯片ETF"),
    "医药":     ("512010", "医药ETF"),
    "医疗":     ("512170", "医疗ETF"),
    "生物":     ("512010", "医药ETF"),
    "军工":     ("512660", "军工ETF"),
    "航空":     ("512660", "军工ETF"),
    "银行":     ("512800", "银行ETF"),
    "证券":     ("512880", "证券ETF"),
    "保险":     ("512070", "非银ETF"),
    "食品饮料": ("515170", "食品饮料ETF"),
    "白酒":     ("512690", "酒ETF"),
    "新能源":   ("515030", "新能源ETF"),
    "光伏":     ("515790", "光伏ETF"),
    "电力":     ("159611", "电力ETF"),
    "计算机":   ("512720", "计算机ETF"),
    "通信":     ("515880", "通信ETF"),
    "传媒":     ("159805", "传媒ETF"),
    "房地产":   ("512200", "房地产ETF"),
    "基建":     ("516970", "基建ETF"),
    "汽车":     ("515030", "新能源ETF"),
    "家电":     ("159996", "家电ETF"),
    "农业":     ("516650", "农业ETF"),
    "建材":     ("516750", "建材ETF"),
    "机械":     ("516960", "机械ETF"),
    "机器人":   ("516960", "机械ETF"),
}


# ===== 券商研报（通过WebAPI，无需直连数据库）=====

def _get_research_stock(code: str, days: int = 90, page_size: int = 20) -> list:
    """GET /api/research-report/stock/{code}?days=N&pageSize=N"""
    try:
        resp = _session.get(
            _url(f"research-report/stock/{code}"),
            params={"days": days, "pageSize": page_size},
            timeout=config.TIMEOUT
        )
        if resp.status_code not in (200, 201):
            return []
        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            # 返回格式: { result: { list: [...] } } 或 { result: { data: { rows: [...] } } }
            if isinstance(r, dict):
                lst = r.get("list", [])
                if lst:
                    return lst
                inner = r.get("data", {})
                if isinstance(inner, dict):
                    return inner.get("rows", [])
            if isinstance(r, list):
                return r
        return []
    except Exception as e:
        print(f"[db] _get_research_stock({code}) 失败: {e}")
        return []

def _get_research_list(**params) -> list:
    """GET /api/research-report/list?params"""
    try:
        resp = _session.get(
            _url("research-report/list"),
            params={k:v for k,v in params.items() if v is not None},
            timeout=config.TIMEOUT
        )
        if resp.status_code not in (200, 201):
            return []
        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            if isinstance(r, dict):
                lst = r.get("list", [])
                if lst:
                    return lst
                inner = r.get("data", {})
                if isinstance(inner, dict):
                    return inner.get("rows", [])
            if isinstance(r, list):
                return r
        return []
    except Exception as e:
        print(f"[db] _get_research_list 失败: {e}")
        return []

def get_research_summary(code: str, days: int = 90) -> str:
    """个股研报汇总 — 格式化文本"""
    rows = _get_research_stock(code, days, 20)
    if not rows:
        return f"近{days}天无券商研报覆盖。"
    parts = []
    parts.append(f"券商观点（近{days}天，{len(rows)}篇）")
    parts.append("=" * 60)
    for r in rows:
        date = r.get("reportDate","")[:10]
        org = r.get("orgName","")
        rating = r.get("rating","")
        title = r.get("title","")
        researcher = r.get("researcher","")
        eps_this = r.get("epsThisYear")
        eps_next = r.get("epsNextYear")
        eps_after = r.get("epsYearAfter")
        pe_this = r.get("peThisYear")
        pe_next = r.get("peNextYear")
        pe_after = r.get("peYearAfter")

        eps_str = ""
        if eps_this is not None and eps_next is not None and eps_after is not None:
            eps_str = f"EPS={eps_this:.2f}->{eps_next:.2f}->{eps_after:.2f}"
        elif eps_this is not None and eps_next is not None:
            eps_str = f"EPS={eps_this:.2f}->{eps_next:.2f}"

        pe_str = ""
        if pe_this is not None and pe_next is not None and pe_after is not None:
            pe_str = f"PE={pe_this:.1f}x->{pe_next:.1f}x->{pe_after:.1f}x"
        elif pe_this is not None and pe_next is not None:
            pe_str = f"PE={pe_this:.1f}x->{pe_next:.1f}x"

        parts.append(f"  {date}  {org:<12s} {rating:<6s}  {eps_str}")
        if title:
            parts.append(f"        {title[:50]}（{researcher}）")
        if eps_str and pe_str:
            parts.append(f"       {eps_str}  |  {pe_str}")
        parts.append("")
    return "\n".join(parts)

def get_eps_consistency(code: str, days: int = 180) -> str:
    """EPS一致性预期 — 统计各机构EPS预测的分歧程度"""
    rows = _get_research_stock(code, days, 50)
    # 取每个机构最新的EPS预测值
    org_eps = {}
    for r in rows:
        org = r.get("orgName","")
        eps = r.get("epsThisYear")
        date = r.get("reportDate","")
        if org and eps is not None:
            if org not in org_eps or date > org_eps[org][1]:
                org_eps[org] = (eps, date)
    if not org_eps:
        return f"近{days}天无EPS预测数据。"
    eps_values = [v[0] for v in org_eps.values()]
    n = len(eps_values)
    mean_eps = sum(eps_values) / n
    std_eps = (sum((v - mean_eps)**2 for v in eps_values) / n) ** 0.5
    cv = std_eps / mean_eps * 100 if mean_eps != 0 else 0
    if cv <= 5:
        verdict = "高度一致"
    elif cv <= 15:
        verdict = "基本一致（中等分歧）"
    else:
        verdict = "分歧较大"
    parts = []
    parts.append(f"EPS一致性预期 — {code}")
    parts.append(f"  覆盖机构: {n}家")
    parts.append(f"  平均EPS: {mean_eps:.3f}")
    parts.append(f"  标准差: {std_eps:.3f}")
    parts.append(f"  变异系数: {cv:.1f}%")
    parts.append(f"  判定: {verdict}")
    if eps_values:
        parts.append(f"  预期区间: [{min(eps_values):.3f} ~ {max(eps_values):.3f}]")
    parts.append("")
    parts.append("  各机构预期:")
    for org, (eps, date) in sorted(org_eps.items(), key=lambda x: x[1][0], reverse=True):
        dev = (eps - mean_eps) / mean_eps * 100 if mean_eps != 0 else 0
        parts.append(f"    {org:<12s} {date[:10]}  EPS={eps:.3f}  {dev:+.1f}%")
    return "\n".join(parts)

def get_broker_ranking(code: str = None, days: int = 90) -> str:
    """券商覆盖统计 — 有code则针对个股，无code返回提示"""
    if not code:
        return "（全市场券商排名需额外查询接口）"
    rows = _get_research_stock(code, days, 50)
    if not rows:
        return f"近{days}天无研报覆盖。"
    org_stats = {}
    for r in rows:
        org = r.get("orgName","")
        rating = r.get("rating","")
        if not org:
            continue
        if org not in org_stats:
            org_stats[org] = {"total": 0, "buy": 0}
        org_stats[org]["total"] += 1
        if "买入" in rating or "增持" in rating:
            org_stats[org]["buy"] += 1
    if not org_stats:
        return "无法统计券商覆盖。"
    sorted_orgs = sorted(org_stats.items(), key=lambda x: x[1]["total"], reverse=True)
    parts = []
    parts.append(f"券商覆盖（近{days}天，{len(rows)}篇）")
    parts.append("=" * 50)
    parts.append(f"{'券商机构':<14s} {'篇数':>4s} {'买入/增持':>8s} {'买入率':>5s}")
    parts.append("-" * 35)
    for org, st in sorted_orgs:
        rate = st["buy"] / st["total"] * 100 if st["total"] > 0 else 0
        parts.append(f"  {org:<12s} {st['total']:>4d} {st['buy']:>8d} {rate:>4.0f}%")
    return "\n".join(parts)

def get_rating_wind_today(code: str = None) -> str:
    """今日评级变动 — 有code则查个股，无code查全市场（可能有数据限制）"""
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    if code:
        rows = _get_research_stock(code, 1, 10)  # 查最近1天
        # 过滤今日数据
        today_rows = [r for r in rows if (r.get("reportDate","")[:10]) == today]
        if not today_rows:
            return f"今日({today})该股无研报更新。"
        upgrades = [r for r in today_rows if "调高" in (r.get("ratingChange","") or "")]
        downgrades = [r for r in today_rows if "调低" in (r.get("ratingChange","") or "")]
        parts = []
        parts.append(f"今日({today})该股研报动态")
        parts.append("=" * 40)
        for r in today_rows:
            parts.append(f"  {r.get('orgName','')}: {r.get('rating','')} \"{r.get('title','')[:30]}\"")
        return "\n".join(parts)
    # 全市场查询 — 通过list接口（可能有限制）
    rows = _get_research_list(startDate=today, endDate=today, pageSize=30)
    if not rows:
        return f"今日({today})无全市场研报数据。"
    upgrades, downgrades, others = [], [], []
    for r in rows:
        chg = r.get("ratingChange","")
        stock = r.get("stockName","") or r.get("stockCode","")
        org = r.get("orgName","")
        rating = r.get("rating","")
        entry = f"{stock}({org}:{rating})"
        if "调高" in str(chg) or "上调" in str(chg):
            upgrades.append(entry)
        elif "调低" in str(chg) or "下调" in str(chg):
            downgrades.append(entry)
        else:
            others.append(entry)
    parts = [f"今日({today})评级风向标"]
    if upgrades:
        parts.append(f"  调高: {'; '.join(upgrades[:5])}")
    if downgrades:
        parts.append(f"  调低: {'; '.join(downgrades[:5])}")
    if others:
        parts.append(f"  其他/新覆盖: {len(others)}条")
    if not upgrades and not downgrades:
        parts.append("  今日无评级变动。")
    return "\n".join(parts)


def get_afterhours_ranking(
    trade_date: str = "",
    min_amt: float = 100,
    top_n: int = 20
) -> list:
    """
    查询盘后固定价格交易活跃板块排名 — GET /api/etf/afterhours-ranking
    
    返回指定日期全市场ETF盘后成交活跃度TOP榜单
    用于板块轮动分析和盘前T+1策略
    
    Args:
        trade_date: 日期 YYYY-MM-DD（不传默认当天）
        min_amt:    最低盘后成交额门槛（万元），默认100=🔴活跃
        top_n:      返回前N条，默认20
    
    Returns:
        [{
            "rank": 1,
            "etf_code": "588170",
            "etf_name": "科创半导体ETF华夏",
            "net_inflow": -50000000,
            "after_hours_vol": 116692,
            "after_hours_amt": 1507.66
        }, ...]
    """
    try:
        params = {"minAmt": min_amt, "topN": top_n}
        if trade_date:
            params["date"] = trade_date

        import requests
        url = f"{config.WEBAPI_BASE_URL}/etf/afterhours-ranking"
        resp = requests.get(url, params=params, timeout=config.TIMEOUT)
        if resp.status_code not in (200, 201):
            return []

        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            if isinstance(r, dict) and "data" in r:
                return r["data"].get("rankings", [])
            return r.get("rankings", [])
        return []
    except Exception as e:
        print(f"[db] get_afterhours_ranking 失败: {e}")
        return []


def get_etf_stats(
    start_date: str = "",
    end_date: str = "",
    min_amt: float = 0,
    top_n: int = 20,
    sort_by: str = "after_hours_amt",
    order: str = "desc"
) -> list:
    """
    查询指定日期范围ETF数据统计（含盘后数据聚合）— GET /api/etf/stats
    
    用于板块轮动趋势分析、盘后活跃度持续追踪。
    支持按净流入/盘后额/盘后量排序，返回多天聚合统计。
    
    Args:
        start_date: 起始日期 YYYY-MM-DD（默认当天）
        end_date:   截止日期 YYYY-MM-DD（默认当天）
        min_amt:    最低盘后成交额门槛（万元），默认0
        top_n:      返回前N条，默认20
        sort_by:    排序字段 — "net_inflow" / "after_hours_amt" / "after_hours_vol"
        order:      排序方向 — "desc" 降序 / "asc" 升序
    
    Returns:
        [{
            "rank": 1,
            "etf_code": "588170",
            "etf_name": "科创半导体ETF华夏",
            "days_with_data": 8,
            "avg_net_inflow": -500000,       # 日均净流入
            "total_net_inflow": -4000000,     # 累计净流入
            "total_after_hours_amt": 8500.5,  # 累计盘后成交额(万)
            "avg_after_hours_amt": 1062.6,    # 日均盘后额(万)
            "total_after_hours_vol": 680000,  # 累计盘后成交量(手)
            "avg_after_hours_vol": 85000,     # 日均盘后量(手)
            "active_days": 6,                 # 盘后活跃天数(≥20万)
        }, ...]
    """
    try:
        params = {"minAmt": min_amt, "topN": top_n, "sortBy": sort_by, "order": order}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        import requests
        url = f"{config.WEBAPI_BASE_URL}/etf/stats"
        resp = requests.get(url, params=params, timeout=config.TIMEOUT)
        if resp.status_code not in (200, 201):
            return []

        data = resp.json()
        if isinstance(data, dict):
            r = data.get("result", data)
            return r.get("stats", [])
        return []
    except Exception as e:
        print(f"[db] get_etf_stats 失败: {e}")
        return []
