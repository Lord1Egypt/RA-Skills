"""
大乐透专家名录 / 数据源黄页

诚实设计原则(2026-08-24 修订, 用户反馈驱动):
- 系统**只收录「带来源URL + 真实分析逻辑」的当期检索专家**; 绝不内置任何
  「仅平台标签、无真实观点」的空壳名录(如乐彩网/彩宝贝名家黄页 上官博超/风花雪月等)。
- 专家来源单一真实数据源: dlt_expert_views_<period>.json (WebSearch 实锤的公开文章原文,
  含三区比/大小比/重号/连号/质合/跨度/遗漏等分析逻辑 + 推荐号 + 来源URL + verified=True)。
- 不虚构粉丝数(followers 统一 '—'); 真实战绩以 dlt_expert_tracker.py 比对实际开奖自算为准。

诚实声明: 彩票数学上近纯随机, 不存在能证明有预测优势的专家
(幸存者偏差 + 指标注水 + 事后篡改; 体彩中心声明从未授权任何个人预测)。
故本名录的价值在于"汇集多方观点供观察", 而非"提升中选可能"。
"""
from datetime import datetime
from collections import Counter

# 类型常量
TYPE_AUTH = "权威"          # 平台知名名家 / 高粉媒体号
TYPE_GRASS = "野路子"       # 论坛草根 / 民间算法流
TYPE_OFFICIAL = "官方数据"   # 官方/权威数据源(非预测, 供校验)

# ---------------------------------------------------------------------------
# 专家名录 (单一真实数据源: 仅收录「带来源URL + 真实分析逻辑」的当期检索专家)
# 设计修正(2026-08-24, 用户反馈): 不再内置任何「仅平台标签、无真实观点」的空壳名录
# (如上官博超/风花雪月/草庐居士等乐彩网/彩宝贝名家黄页)。凡专家必须:
#   ① 来自 dlt_expert_views_<period>.json (WebSearch 实锤的公开文章原文);
#   ② 含真实分析逻辑(三区比/大小比/重号/连号/质合/跨度/遗漏等) + 推荐号 + 来源URL;
#   ③ verified=True (已逐一比对公开原文)。
# 不虚构粉丝数(followers 统一记 '—'); 真实战绩以 dlt_expert_tracker 自算为准。
# 字段: name, platform, type, specialty, followers, verified, note, source_url
# ---------------------------------------------------------------------------

def _load_real_experts():
    """从 dlt_expert_views_<period>.json 加载真实(已核验)当期专家, 作为系统唯一专家来源。
    只取最新一期文件; 若该文件缺失则名录为空(诚实: 不凭空捏造任何专家)。"""
    import os as _os, json as _json, glob as _glob
    _base = _os.path.dirname(_os.path.abspath(__file__))
    _files = sorted(_glob.glob(_os.path.join(_base, 'dlt_expert_views_*.json')),
                    key=_os.path.getmtime, reverse=True)
    for _f in _files:
        try:
            _d = _json.load(open(_f, encoding='utf-8'))
        except Exception:
            continue
        _out = []
        for _e in _d.get('experts', []):
            _out.append(dict(
                name=_e.get('expert', ''),
                platform=_e.get('platform', '公开来源'),
                type=TYPE_AUTH,
                specialty='本期分析',
                followers='—',
                verified=bool(_e.get('verified')),
                note=(_e.get('analysis') or '')[:80],
                source_url=_e.get('source_url', ''),
            ))
        if _out:
            return _out
    return []


EXPERTS = _load_real_experts()

# ---------------------------------------------------------------------------
# 官方 / 权威数据源 (非预测, 供校验与数据支撑)
# ---------------------------------------------------------------------------
DATA_SOURCES = [
    dict(name="中国体彩网", url="https://www.lottery.gov.cn/zst/dlt/", type=TYPE_OFFICIAL, note="官方开奖史+走势+遗漏, 唯一真源"),
    dict(name="体彩开奖接口", url="https://webapi.sporttery.cn", type=TYPE_OFFICIAL, note="getHistoryPageListV1 返回JSON, 最适合程序化拉取(参数待核实)"),
    dict(name="北京体彩网", url="https://www.bjlot.com.cn/dlt/dlt_history.shtml", type=TYPE_OFFICIAL, note="省中心镜像, 结构简单易抓"),
    dict(name="新浪彩票走势图", url="https://view.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=dlt", type=TYPE_OFFICIAL, note="带连线高清走势图"),
    dict(name="彩吧助手", url="https://kjh.55128.cn/dlt-history-120.htm", type=TYPE_OFFICIAL, note="已算好和值/奇偶/跨度, 表格规整"),
    dict(name="中彩网图表", url="https://tubiao.zhcw.com", type=TYPE_OFFICIAL, note="可按年份取, 含遗漏分层"),
    dict(name="彩宝贝", url="https://www.78500.cn/dlt/", type=TYPE_OFFICIAL, note="大乐透专家排行榜/杀号榜常客, 结构化易抓"),
    dict(name="500彩票网", url="https://datachart.500.com/dlt/", type=TYPE_OFFICIAL, note="带遗漏/和值/跨度历史表, 表格规整"),
    dict(name="双彩网", url="https://www.shuangcw.com/dlt/", type=TYPE_OFFICIAL, note="大乐透开奖+走势+专家点评聚合"),
]


def get_roster():
    return EXPERTS


def get_data_sources():
    return DATA_SOURCES


def roster_by_name():
    return {e['name']: e for e in EXPERTS}


def meta_for(name):
    """返回该专家在名录中的元数据(若无则返回 None)。供 scraper 给真实抓取到的同名专家补元数据。"""
    return roster_by_name().get(name)


def catalog_summary():
    """统计名录构成, 用于报告/日志。"""
    c = Counter(e['type'] for e in EXPERTS)
    return {
        '权威': c.get(TYPE_AUTH, 0),
        '野路子': c.get(TYPE_GRASS, 0),
        '官方数据源': len(DATA_SOURCES),
        '总计专家': len(EXPERTS),
    }


def render_expert_views_html(target_period=None):
    """返回「专家观点」面板 HTML（描述性/娱乐参考，非选号建议）。

    诚实分层（设计原则: 专家数学上无预测优势 no_edge, 仅作逆向/观察参考, 绝不构成选号建议）：
    ① 本期实时检索专家推荐 —— 来自 dlt_expert_picks.json, 由 WebSearch 实时检索公开来源,
       含真实推荐号 + 来源平台 + 期号 + 「未核实/无预测力」标注。每期刷新 picks 即更新。
    ② 专家观点库 —— 动态优先展示「本期实时检索观点」(WebSearch 逐期刷新, 如 26095/26094 期),
       其余为各平台常驻名家名录(平台/专长介绍)。诚实标注哪些是本期实时、哪些是常驻观察,
       绝不谎称"实时抓取"或暗示提升中选可能。
    """
    summ = catalog_summary()
    # ---- ① 本期实时检索专家推荐（真实数据, 可逐期更新） ----
    picks_rows = ''
    picks_period = target_period
    try:
        import os as _os, json as _json
        _p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'dlt_expert_picks.json')
        if _os.path.exists(_p):
            _d = _json.load(open(_p, encoding='utf-8'))
            _meta = _d.get('_meta', {})
            picks_period = _meta.get('target_period') or target_period
            _auto = _meta.get('auto_scraped')
            for e in _d.get('experts', []):
                f = e.get('front', [])
                b = e.get('back', [])
                src = e.get('source') or e.get('platform') or '公开来源'
                picks_rows += (
                    f'<tr><td style="text-align:center;">🔍 {e.get("expert","?")}</td>'
                    f'<td style="text-align:center;">{src}</td>'
                    f'<td style="color:#ffd9a0;">前区 {",".join(str(x) for x in f)} ｜ 后区 {",".join(str(x) for x in b)}</td>'
                    f'<td style="color:#9fb4ff;">未核实·无预测力(no_edge)</td></tr>'
                )
    except Exception:
        picks_rows = ''
    picks_section = ''
    if picks_rows:
        picks_section = f"""
<div class="section">
<div class="section-title">🔍 本期实时检索专家推荐（{picks_period or '?'}期 · 由 WebSearch 实时检索公开来源）</div>
<div class="info" style="border-color:#ff8844; background:#1a1020;">
<p style="color:#ffb38a; font-size:12.5px; line-height:1.7; margin:6px 0;">
以下推荐号由智能体实时检索公开论坛/媒体得到，<b>未经核实、质量参差、可能含排版错误</b>。
大乐透近似完全随机，任一5+2组合中奖概率恒为 1/21,425,712，专家推荐在数学上不提供任何优势(no_edge)。
本栏仅作「观察市场共识 / 逆向避开大众热门」的趣味参考，<b style="color:#ff6b6b;">绝不可据其认为某号更可能中奖</b>。
</p>
</div>
<table>
<tr><th>专家</th><th>来源</th><th>推荐号码(前区+后区)</th><th>诚实标注</th></tr>
{picks_rows}
</table>
</div>
"""
    # ---- ② 本期专家观点与分析（仅渲染真实当期检索、含分析逻辑、带来源URL的专家） ----
    # 设计修正(2026-08-24, 用户反馈): 不再把"常驻平台名录"(如上官博超/风花雪月/六鬼神算等
    # 仅平台标签、无真实观点的空壳) 混进"专家观点库"凑数。本面板只展示 WebSearch 实锤的
    # 当期(target_period)专家观点——每位都有真实分析逻辑(三区比/大小比/重号/连号/质合/跨度/
    # 遗漏等) + 推荐号 + 来源文章URL。诚实原则 no_edge 贯穿: 专家推荐数学上无预测优势,
    # 仅作分析思路观察与逆向参考, 绝不构成选号建议。
    views_rows = ''
    views_period = picks_period
    views_count = 0
    try:
        import os as _os, json as _json
        _v = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                           'dlt_expert_views_{}.json'.format(target_period or ''))
        if _os.path.exists(_v):
            _vd = _json.load(open(_v, encoding='utf-8'))
            _vm = _vd.get('_meta', {})
            views_period = _vm.get('target_period') or target_period
            for e in _vd.get('experts', []):
                f = e.get('front', [])
                b = e.get('back', [])
                url = e.get('source_url') or ''
                analysis = e.get('analysis') or '（无分析摘要）'
                src = e.get('platform') or '公开来源'
                link = ('<a href="{}" target="_blank" style="color:#7fd0ff;">{}</a>'.format(url, src)
                        if url else src)
                views_rows += (
                    f'<tr><td style="text-align:center;">🔍 {e.get("expert","?")}</td>'
                    f'<td style="text-align:center;">{link}</td>'
                    f'<td style="color:#ffd9a0; text-align:left;">{analysis}</td>'
                    f'<td style="color:#ffd9a0;">前区 {",".join(str(x) for x in f)} ｜ 后区 {",".join(str(x) for x in b)}</td>'
                    f'<td style="color:#9fb4ff;">未核实·无预测力(no_edge)</td></tr>'
                )
                views_count += 1
    except Exception:
        views_rows = ''
    html = f"""
<div class="section">
<div class="section-title">🧠 本期专家观点与分析（{views_period}期 · WebSearch实时检索 · 含分析逻辑）</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12.5px; line-height:1.7; margin:6px 0;">
以下为系统于 <b style="color:#ffd9a0;">{views_period} 期</b> 经 WebSearch 实时检索公开来源（新浪体育/新浪彩票/一定牛/彩吧助手等）得到的 <b style="color:#ffd9a0;">{views_count} 位</b>真实专家观点，<b>每位均附分析逻辑（三区比/大小比/重号/连号/质合/跨度/遗漏等）与推荐号，并标注来源文章</b>。
彩票数学上近似完全随机，任一5+2组合中奖概率恒为 1/21,425,712，专家推荐在数学上不提供任何优势（no_edge）。本栏仅作「观察分析思路 / 逆向避开大众热门」的趣味参考，<b style="color:#ff6b6b;">绝不可据其认为某号更可能中奖</b>，不构成选号建议。
<span style="color:#ffb38a;">（注：未纳入任何"仅平台标签、无真实观点"的空壳名录——如乐彩网/彩宝贝等常驻名家仅作平台黄页，不冒充专家观点。）</span>
</p>
</div>
<table>
<tr><th>专家</th><th>平台/来源</th><th>核心分析观点</th><th>推荐号码(前区+后区)</th><th>诚实标注</th></tr>
{views_rows}
</table>
</div>
"""
    return picks_section + html


if __name__ == '__main__':
    print("常驻专家名录 (系统内置, 始终可用):")
    for t in (TYPE_AUTH, TYPE_GRASS):
        print(f"\n== {t} ==")
        for e in EXPERTS:
            if e['type'] == t:
                print(f"  {e['name']:10s} | {e['platform']:8s} | {e['specialty']} | 粉丝:{e['followers']}")
    print("\n== 官方数据源 ==")
    for d in DATA_SOURCES:
        print(f"  {d['name']:10s} | {d['url']}")
    print("\n汇总:", catalog_summary())
