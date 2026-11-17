#!/usr/bin/env python3
"""
generate_site.py

把新闻 JSON（RSS 自治抓取，AI HOT 兼容 schema）渲染为单文件 AI 新闻网站 HTML。

本文件只负责三件事（其余逻辑均在 aiweekly 子包）：
  1. 命令行解析与输入校验（--api-json / 榜单 / 看点 / 图表 / 翻译等）；
  2. 顺序编排：抓榜 → 同步模型档案 → 读看点 → 调用渲染层 → 写运行日志；
  3. 运行结果与告警的对外呈现。

逻辑归属速查：
  RSS 抓取与新闻归一化   -> aiweekly.news       网络 IO 与出站代理 -> aiweekly.utils
  排行榜抓取与模型档案   -> aiweekly.leaderboard   市场数据与图表 -> aiweekly.market / charts_svg
  本周看点与关键词       -> aiweekly.insights      HTML 装配 -> aiweekly.render
  健康检查（--health-check）-> aiweekly.health
`from generate_site import generate` 仍然可用（转出口自 aiweekly.render，属兼容垫层）。

本技能**默认不调用任何付费/商业 API**；新闻默认全部来自公开 RSS 聚合。
唯一例外是可选的 NewsAPI 接入（`--news-api` + 自备 `NEWSAPI_KEY`，默认关闭，见 fetch_ai_news.py）。

可选外部增强：如希望用 AI HOT、或任何「AI 行业知识类」外部 API 增强报告可信度，
请自行从其官方渠道获取数据并导出为 JSON（schema 见下），再用 --external-news-json
注入。是否启用完全由你决定，风险自担（需遵守该 API 的服务条款）。

  ⚠️ AI HOT 停服提醒：其 legacy `/api/public/*` 接口已于 2026-10-31 停止服务，
     域名已 301 到 aihot.news。v1（`/api/v1/*`）是完全不同的形态：端点从 9 个扩到
     33 个（新增 `weeklies` / `monthlies` / `stories/{id}` / `agent/*` 等 12 个 Agent
     专用端点），参数 `take` → `limit`、`since` → `window`、另有 `by`。
     沿用 legacy 参数的脚本切到 v1 不会抛异常，而是拿到
     `400 {"detail":"Unknown query parameter: take."}` —— 静默失败、取数为空，
     排查起来很费时间。取数前请先对照目标 API 的 openapi 确认参数名。

用法：
  # 用 RSS 抓取结果生成（默认，无任何第三方 API 依赖）
  python scripts/generate_site.py --api-json news.json --output AI_News.html

  # 叠加用户自备的外部 API 数据增强（例：AI HOT 导出 JSON）
  python scripts/generate_site.py --api-json news.json \
      --external-news-json aihot_export.json --external-source-name "AI HOT" \
      --external-source-url "https://aihot.news" -o AI_News.html

  # 从自定义排行榜 JSON 文件生成
  python scripts/generate_site.py --api-json news.json --ranking-json ranking.json -o AI_News.html

  # 跳过排行榜自动获取（显示「暂无实时数据」）
  python scripts/generate_site.py --api-json news.json --no-live-ranking -o AI_News.html

  # 只看数据摘要 / 只探测网络（不生成）
  python scripts/generate_site.py --api-json news.json --dry-run
  python scripts/generate_site.py --health-check

新闻 / 外部增强 JSON 格式（裸 items 列表或 {"items": [...]} 均可）：
  [{"title":"...","summary":"...","url":"...","source":"...",
    "publishedAt":"...","category":"ai-models","score":0}, ...]

排行榜 JSON 格式：
  [{"name":"...","developer":"...","open_source":false,"score":"92","rank":1}, ...]

输出：
  - 新闻卡片（分类色块缩略图 + 来源链接 + 相对时间）
  - 市场规模 + 融资趋势图（服务端预渲染 SVG，Chart.js 为可选增强）
  - Top 10 模型排行榜表格（实时数据，标注来源与排名标准）
  - 搜索栏 + 分类筛选标签
  - 暗色模式 + 响应式布局
"""

import argparse
import logging
import os
import sys
from collections import Counter
from datetime import datetime

try:
    from bs4 import BeautifulSoup  # noqa: F401  启动依赖自检：渲染/抓取层依赖它
except ImportError:
    print("❌ 缺少依赖(beautifulsoup4)。请使用仓库根目录的 run_report.sh 启动，"
          "或：python -m pip install -r requirements.txt")
    sys.exit(1)

# 本地子包导入必须晚于上面的依赖自检——子包自身 import bs4，
# 缺依赖时先由自检给出人话提示，而不是抛裸 ImportError。
import aiweekly.insights as INS  # noqa: E402
import aiweekly.leaderboard as LB  # noqa: E402
import aiweekly.market as _mk  # noqa: E402  --check-snapshot 只需 market 的快照体检
from aiweekly import const as _ac  # noqa: E402
from aiweekly.cli_utils import (  # noqa: E402
    _CountingWriter, _parse_csv_arg, _parse_num_arg,
    bounded_int, load_json_soft, load_json_strict,
    resolve_search_sources, write_run_log,
)
from aiweekly.diagnostics import print_user_hints  # noqa: E402
from aiweekly.health import run_health_check  # noqa: E402
from aiweekly.news import merge_external_news  # noqa: E402
from aiweekly.render import generate  # noqa: E402  兼容垫层：see __all__
from aiweekly.utils import (  # noqa: E402
    _parse_date_arg, _parse_snapshot_date, configure_proxy,
)


logger = logging.getLogger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    """构造 CLI 解析器（选项表属「接口定义」，与流程编排分开）。"""
    parser = argparse.ArgumentParser(description="生成 AI 新闻网站 HTML")
    parser.add_argument("--api-json", help="新闻 JSON 文件路径（RSS 抓取结果，AI HOT 兼容 schema）")
    parser.add_argument("--output", "-o", help="输出 HTML 文件路径")
    parser.add_argument("--dry-run", action="store_true", help="仅显示数据摘要，不生成")
    # 可选外部 API 增强：用户自备（如 AI HOT 或其他 AI 行业知识 API），自行承担合规风险
    # 注：AI HOT 的 legacy /api/public/* 已于 2026-10-31 停服（域名 301 到 aihot.news）。
    # v1 参数形态不同（take→limit、since→window、新增 by），沿用 legacy 参数会静默返回 400 空结果。
    parser.add_argument("--external-news-json", help="可选：自备外部 API 导出的新闻 JSON（增强报告，如 AI HOT；其 legacy 接口已于 2026-10-31 停服，需按 v1 参数取数）")
    parser.add_argument("--external-source-name", help="外部数据源名称（页脚署名，如 AI HOT）")
    parser.add_argument("--external-source-url", help="外部数据源主页 URL（页脚链接，可选）")
    parser.add_argument("--ranking-json", help="从本地 JSON 文件读取排行榜数据（覆盖自动获取）")
    parser.add_argument("--profiles-json", help="追加的模型资料卡 profile JSON（按模型名索引）；会与技能目录 canonical 档案合并并写回，实现档案实时累积更新")
    parser.add_argument("--no-live-ranking", action="store_true",
                        help="跳过自动获取排行榜，显示'暂无实时数据'")
    parser.add_argument("--ranking-top", type=bounded_int(1, 50, "--ranking-top"), default=10,
                        help="排行榜获取条数（默认 10，上限 50）")
    parser.add_argument("--date", default=None,
                        help="固定报告周期截止日 YYYY-MM-DD（如 2026-08-02）；不提供则用当前日期")
    parser.add_argument("--region", default="auto",
                        choices=["auto", "cn", "global"],
                        help="网络环境：auto=探测(默认) / cn=优先国内源 / global=优先国外源")
    parser.add_argument("--proxy", default=None,
                        help="显式指定出站代理（如 http://127.0.0.1:7890）。仅用于企业内网等"
                         "要求全部出站流量经统一代理的网络架构")
    parser.add_argument("--data-snapshot", default=None,
                        help="市场数据快照日期 YYYY-MM-DD（展示在图表注释，标注为静态快照；默认取 --date 或当天）")
    # 图表数据（由 Agent 从 WebSearch 获取真实值后注入；不提供则标注为估算）
    parser.add_argument("--market-data", help="市场规模数据，逗号分隔，如 51,71,103,...")
    parser.add_argument("--market-labels", help="市场规模标签，逗号分隔，如 2020,2021,...")
    parser.add_argument("--funding-data", help="融资额数据，逗号分隔")
    parser.add_argument("--funding-labels", help="融资额标签，逗号分隔")
    parser.add_argument("--market-source", help="市场规模数据来源说明（如 Statista 2026）")
    parser.add_argument("--funding-source", help="融资额数据来源说明（如 Crunchbase 2026）")
    # 中国分轨（国内源）：与全球分轨并列，单位亿元（RMB）
    parser.add_argument("--cn-market-data", help="中国 AI 市场规模数据，逗号分隔，如 9188,12000,17000")
    parser.add_argument("--cn-market-labels", help="中国市场规模标签，逗号分隔，如 2024,2025,2026E")
    parser.add_argument("--cn-funding-data", help="中国 AI 融资额数据，逗号分隔")
    parser.add_argument("--cn-funding-labels", help="中国融资额标签，逗号分隔")
    parser.add_argument("--cn-market-source", help="中国市场规模来源说明（如 中国信通院/中商产业研究院）")
    parser.add_argument("--cn-funding-source", help="中国融资额来源说明（如 新浪创投Plus 2025）")
    parser.add_argument("--ranking-criteria", help="排行榜排名标准说明（覆盖默认 LMMarketCap 综合评分说明）")
    # 编辑钉选：把命中关键词的报道强制钉进「必读」（重大事件不被算法稀释）
    parser.add_argument("--pin-terms", default=None,
                        help="逗号分隔的钉选词（子串匹配标题）；命中条目强制必读。例：--pin-terms \"DeepSeek Harness,GLM-5.3\"")
    parser.add_argument("--translate-en", action="store_true", default=True,
                        help="为英文报道生成中文总结（调用本地 Ollama；默认开启。需本机运行 Ollama，"
                             "失败/超时保留英文原文，不影响生成）")
    parser.add_argument("--no-translate-en", dest="translate_en", action="store_false",
                        help="关闭英文报道中文总结（如无本地 Ollama 或想加速）")
    parser.add_argument("--translate-model", default=_ac.TRANSLATE_MODEL_DEFAULT,
                        help=f"翻译所用本地 Ollama 模型（默认 {_ac.TRANSLATE_MODEL_DEFAULT}，非推理模型更快）")
    parser.add_argument("--translate-workers", type=bounded_int(1, 32, "--translate-workers"),
                        default=_ac.TRANSLATE_WORKERS_DEFAULT,
                        help="翻译并发线程数（默认 3；CPU 本地推理下过高会互相抢资源导致超时丢条）")
    parser.add_argument("--translate-timeout", type=bounded_int(5, 600, "--translate-timeout"),
                        default=_ac.TRANSLATE_TIMEOUT_DEFAULT,
                        help="单条翻译超时秒数（默认 45；CPU 本地推理较慢，过短会大量超时丢条）")
    parser.add_argument("--translate-retries", type=bounded_int(0, 10, "--translate-retries"),
                        default=_ac.TRANSLATE_RETRIES_DEFAULT,
                        help="单条翻译失败后的重试次数（默认 2，总尝试 = retries+1）")
    parser.add_argument("--translate-num-predict", type=bounded_int(64, 8192, "--translate-num-predict"),
                        default=_ac.TRANSLATE_NUM_PREDICT_DEFAULT,
                        help="译文 token 上限（默认 600，摘要偏长避免截断）")
    parser.add_argument("--no-translate-title", dest="translate_title",
                        action="store_false", default=True,
                        help="关闭中文标题翻译（默认开启：卡片标题显示中文+原文小字）")
    parser.add_argument("--translations-url", default=_ac.DEFAULT_TRANSLATIONS_URL,
                        help="远程译文源 URL（无本地 Ollama 时复用已发布译文；"
                             "默认 https://elisabeth15501.github.io/ai-weekly/translations.json）。"
                             "请只指向你信任的来源")
    parser.add_argument("--no-remote-translations", action="store_true",
                        help="关闭远程译文源（完全离线时用本地 Ollama，或改用 --translations-url 指向离线包）")
    parser.add_argument("--translate-cache", default=None,
                        help="译文缓存文件路径（默认：与 --api-json 同目录的 .translate_cache.json；"
                             "命中即复用、带原文哈希防脏，避免每周重译）")
    # 本周看点（编辑洞察 + 关键词）：由 Agent 基于本周新闻撰写
    parser.add_argument("--insights-json", help="本周看点 JSON 文件（{keywords:[{term,note}], insights:[{kicker,title,analysis,insight,related:[{title,url}]}]}）")
    parser.add_argument("--lead", help="本周看点顶部导语一句话（电梯演讲，可选）")
    parser.add_argument("--keyword-search-base",
                        default="https://www.baidu.com/s?wd=",
                        help="关键词点击跳转的网页搜索基址（默认百度；搜索词将追加「词语 AI 行业」）")
    # 面向目标用户群的「本周看点」优化（Plan A-F）
    parser.add_argument("--audience-summary",
                        help="面向受众的一句话结论，JSON 格式 {开发者:..., PM:..., 媒体:...}；渲染在关键词区上方")
    parser.add_argument("--feishu-push", action="store_true",
                        help="声明本报告会走飞书分发（每周一·应用机器人推送）；仅用于能力卡如实标注，不暴露任何 token/user_id")
    parser.add_argument("--keyword-search-sources", default=_ac.DEFAULT_SEARCH_SOURCES_JSON,
                        help="可切换的搜索源 JSON {name:url} 或该 JSON 的文件路径；默认百度/谷歌/ arXiv")
    parser.add_argument("--health-check", action="store_true",
                        help="只探测网络/榜源可达性，不生成报告（CI/定时任务前置探测）")
    parser.add_argument("--check-snapshot", action="store_true",
                        help="只校验市场快照 assets/market_snapshot.json 的新鲜度，不生成报告"
                             "（缺失或超过阈值天数则退出码非 0）")
    parser.add_argument("--snapshot-max-age-days", type=bounded_int(1, 3650, "--snapshot-max-age-days"),
                        default=None,
                        help=f"快照过期阈值天数（默认取 market.SNAPSHOT_STALE_DAYS）")
    return parser


def _validate_date_args(parser, args) -> None:
    """CLI 层即时校验 ISO 8601 日期——非法值立刻 parser.error 退出（exit 2），
    不再等到渲染中途抛 ValueError 才中断。

    这是本文件错误处理的范式：参数问题就在参数层解决，并给出可照抄的示例。
    """
    for flag, value, parse in (
        ("--date", args.date, _parse_date_arg),
        ("--data-snapshot", args.data_snapshot, _parse_snapshot_date),
    ):
        if not value:
            continue
        try:
            if parse(value) is None:
                raise ValueError("无法解析为日期")
        except ValueError as e:
            parser.error(
                f"{flag} 需为 ISO 8601 日期："
                f"YYYY-MM-DD（如 2026-08-08）或完整形式（如 2026-08-08T00:00:00+08:00）。"
                f"收到 {value!r} —— {e}"
            )


def _as_news_payload(data) -> dict:
    """把新闻 JSON 归一化为 ``{"items": [...], ...}``。

    模块 docstring 承诺「裸 items 列表或 {"items": [...]}」两种形态都合法，
    此处一次性抹平差异，后续代码只需面对字典，不必到处判断类型。
    """
    if isinstance(data, dict):
        payload = dict(data)
        if not isinstance(payload.get("items"), list):
            print("  ⚠️ 新闻 JSON 的 items 字段不是数组，已按空列表处理")
            payload["items"] = []
        return payload
    if not isinstance(data, list):
        print("  ⚠️ 新闻 JSON 根节点既不是数组也不是对象，已按空列表处理")
        return {"items": [], "count": 0}
    items = [it for it in data if isinstance(it, dict)]
    return {"items": items, "count": len(items)}


def _leaderboard_rows(data) -> tuple:
    """取出榜单三列行数据 ``(综合榜左, 综合榜右, 开源榜)``。

    逐层 ``.get`` 并容忍缺失：上游结构变更时这里安静地返回空列表（由调用方
    按「暂无实时数据」处理并打告警），而不是抛 KeyError 被外层 best-effort
    except 吞掉——那样只会看到「暂无实时数据」，看不到真实原因。
    """
    comp = (data or {}).get("comprehensive") or {}
    open_source = (data or {}).get("open_source") or {}

    def _rows(bucket, key):
        return (bucket.get(key) or {}).get("rows") or []

    return _rows(comp, "lmarena"), _rows(comp, "aa"), _rows(open_source, "hf")


def _warn_audience_key_mismatch(audience_summary, keywords) -> None:
    """非致命检查：keywords[].note 的受众键须与 audience_summary 的键一致。

    不一致时，切到某张「给本周的你」受众卡会取不到对应 note 值而显示空白，故提前提示。
    """
    aud_keys = set((audience_summary or INS.DEFAULT_AUDIENCE_SUMMARY).keys())
    note_keys = set()
    for kw in (keywords or []):
        if isinstance(kw, dict) and isinstance(kw.get("note"), dict):
            note_keys |= set(kw["note"].keys())
    if not note_keys or note_keys == aud_keys:
        return
    print(f"  ⚠️ 受众键不一致：audience_summary={sorted(aud_keys)}，"
          f"keywords[].note={sorted(note_keys)}")
    if aud_keys - note_keys:
        print(f"     切到 {sorted(aud_keys - note_keys)} 时部分关键词注释将为空")
    if note_keys - aud_keys:
        print(f"     多余受众键（无对应受众卡，永不显示）：{sorted(note_keys - aud_keys)}")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = build_arg_parser()
    _counter = _CountingWriter(sys.stdout)  # 聚合本次运行的 ⚠️/❌ 计数（写入 run.log）
    sys.stdout = _counter
    args = parser.parse_args()

    _validate_date_args(parser, args)

    # 搜索源是纯参数校验（文件路径 / 内联 JSON 两种形态都当场验合法性 + 非空 {name: url}），
    # 与日期校验同属「参数问题在参数层解决」，放在流程最前——连 --dry-run 也能第一时间发现。
    search_sources_data = resolve_search_sources(parser, args.keyword_search_sources)

    # 出站代理一次到位（--proxy / 环境变量 / 系统代理，含 SOCKS 挂载），后续抓榜、
    # 拉译文源、翻译共用。此前的写法是「在自动抓榜分支里改写 utils 的私有全局」，
    # 导致 --no-live-ranking / --ranking-json 路径下 --proxy 被静默忽略。
    configure_proxy(args.proxy)

    if args.health_check:
        run_health_check(args.no_live_ranking, args.translate_model)
        return

    # 市场快照体检（HON-2）：与 --health-check 同为「只检查不生成」的独立子命令。
    # 放在读 --api-json 之前，缺失/过期时立刻以非 0 退出，不浪费一次新闻读取。
    if args.check_snapshot:
        _max_age = (args.snapshot_max_age_days if args.snapshot_max_age_days is not None
                    else _mk.SNAPSHOT_STALE_DAYS)
        sys.exit(_mk.run_snapshot_check(_max_age))

    # 获取新闻数据（默认仅 RSS 自治抓取结果；不内置任何第三方 API）
    if not args.api_json:
        parser.error("需要 --api-json（请先运行 fetch_ai_news.py 抓取 RSS 新闻）")
    print(f"📂 读取 {args.api_json} ...")
    api_data = _as_news_payload(load_json_strict(parser, args.api_json, "--api-json"))

    # 可选：合并用户自备的外部 API 新闻（如 AI HOT），按 url/title 去重
    external_source = None
    if args.external_news_json:
        print(f"🔌 合并外部增强新闻 {args.external_news_json} ...")
        ext = load_json_strict(parser, args.external_news_json, "--external-news-json")
        ext_raw = (ext.get("items", []) if isinstance(ext, dict) else ext)
        ext_items = [it for it in ext_raw if isinstance(it, dict)] if isinstance(ext_raw, list) else []
        merged = merge_external_news(api_data["items"], ext_items)
        api_data["items"] = merged
        api_data["count"] = len(merged)
        external_source = (args.external_source_name or "外部API", args.external_source_url)
        print(f"  ✅ 外部补充 {len(ext_items)} 条，去重后共 {len(merged)} 条"
              + (f"（来源：{args.external_source_name}）" if args.external_source_name else ""))

    count = api_data.get("count", len(api_data["items"]))
    print(f"  获取到 {count} 条新闻")

    if args.dry_run:
        items = [it for it in api_data["items"] if isinstance(it, dict)]
        cats = Counter(it.get("category", "unknown") for it in items)
        print("\n📊 分类统计：")
        for c, n in sorted(cats.items()):
            print(f"  {c}: {n}")
        print("\n📝 前 5 条标题：")
        for it in items[:5]:
            print(f"  [{it.get('category', 'unknown')}] {it.get('title', '')[:60]}...")
        return

    # 获取双排行榜数据（综合榜 + 开源模型榜），每源独立容错
    leaderboard_data = None
    if args.ranking_json:
        print(f"🏆 从 {args.ranking_json} 读取排行榜...")
        custom = load_json_soft(args.ranking_json, "排行榜 JSON")
        if custom is not None:  # 读取失败时保持 None → 后续按「暂无实时数据」处理
            leaderboard_data = custom
            print("  已加载自定义排行榜数据")
    elif not args.no_live_ranking:
        print("🏆 抓取双排行榜（按网络环境自适应选择国内外源）...")
        try:
            leaderboard_data = LB.fetch_all_leaderboards(args.ranking_top, region=args.region)
            lm, aa, hf = _leaderboard_rows(leaderboard_data)
            if lm or aa or hf:
                print(f"  ✅ 综合榜左 {len(lm)} 条、综合榜右 {len(aa)} 条、开源榜 {len(hf)} 条")
            else:
                print("  ⚠️ 榜单返回结构里没有任何行数据（上游结构可能已变更）")
        except Exception as e:  # noqa: BLE001  best-effort 抓取：单源失败不阻断生成
            print(f"  ⚠️ 排行榜抓取异常（{type(e).__name__}）：{e}（将显示「暂无实时数据」）")

    # 模型档案同步：自动加载 canonical 档案 + 合并传入的新档案 + 检测新上榜模型
    model_profiles_data = LB.sync_model_profiles(args.profiles_json, leaderboard_data)

    # 本周看点（编辑洞察 + 关键词）：由 Agent 基于本周新闻撰写，可选
    insights = None
    keywords = None
    audience_summary_data = None
    if args.insights_json:
        print(f"📌 读取本周看点 {args.insights_json} ...")
        data = load_json_strict(parser, args.insights_json, "--insights-json")
        if isinstance(data, dict):
            insights = data.get("insights", [])
            keywords = data.get("keywords", [])
            # 允许在 insights.json 内联 audience_summary（受众键同关键词：开发者/PM/自媒体）
            audience_summary_data = data.get("audience_summary")
        else:
            insights = data
        errs = INS.validate_insights(data)
        if errs:
            print("❌ insights.json 校验失败：")
            for e in errs:
                print("  -", e)
            sys.exit(1)
        print(f"  ✅ 载入 {len(insights or [])} 条看点"
              + (f"、{len(keywords or [])} 个关键词" if keywords else "")
              + (f"、受众结论 {len(audience_summary_data or {})} 类" if audience_summary_data else ""))
        _warn_audience_key_mismatch(audience_summary_data, keywords)

    # 读取面向受众的一句话结论（独立文件优先；缺失则回退 insights.json 内联或内置默认）
    if args.audience_summary:
        standalone = load_json_soft(args.audience_summary, "受众结论 JSON")
        if standalone is not None:
            audience_summary_data = standalone

    # 生成
    logger.info("开始渲染 HTML（新闻数=%d）", count)
    output = args.output or f"AI_News_{datetime.now().strftime('%Y-%m-%d')}.html"
    html = generate(
        api_data, output_path=output,
        market_data=_parse_num_arg(args.market_data),
        market_labels=_parse_csv_arg(args.market_labels),
        funding_data=_parse_num_arg(args.funding_data),
        funding_labels=_parse_csv_arg(args.funding_labels),
        market_source=args.market_source,
        funding_source=args.funding_source,
        cn_market_data=_parse_num_arg(args.cn_market_data),
        cn_market_labels=_parse_csv_arg(args.cn_market_labels),
        cn_funding_data=_parse_num_arg(args.cn_funding_data),
        cn_funding_labels=_parse_csv_arg(args.cn_funding_labels),
        cn_market_source=args.cn_market_source,
        cn_funding_source=args.cn_funding_source,
        external_source=external_source,
        leaderboard_data=leaderboard_data,
        model_profiles=model_profiles_data,
        insights=insights,
        region=((leaderboard_data or {}).get("meta") or {}).get("region") or args.region,
        lead=args.lead,
        keywords=keywords,
        keyword_search_base=args.keyword_search_base,
        audience_summary=audience_summary_data,
        keyword_search_sources=search_sources_data,
        report_date=args.date,
        data_snapshot=args.data_snapshot,
        pin_terms=[t.strip() for t in (args.pin_terms or "").split(",") if t.strip()],
        translate_en=args.translate_en,
        translate_model=args.translate_model,
        translate_workers=args.translate_workers,
        translate_timeout=args.translate_timeout,
        translate_retries=args.translate_retries,
        translate_num_predict=args.translate_num_predict,
        translate_title=args.translate_title,
        feishu_push=args.feishu_push,
        translations_url=None if args.no_remote_translations else args.translations_url,
        translate_cache=args.translate_cache or (
            os.path.join(os.path.dirname(os.path.abspath(args.api_json)), ".translate_cache.json")
            if (args.translate_en and args.api_json) else None),
    )
    _lb_ok = bool(any(_leaderboard_rows(leaderboard_data)))
    print(f"✅ 已生成 {output}（{len(html.encode('utf-8'))} bytes，{count} 条新闻，"
          f"双排行榜: {'已填充' if _lb_ok else '暂无实时数据'}）")

    # 错误聚合报告：把本次运行的 ⚠️/❌ 计数写入 <output>.run.log（供无人值守复盘）
    run_log = write_run_log(output, count, _counter)
    if run_log:
        print(f"📝 运行日志已保存：{run_log}（warnings={_counter.warns} / errors={_counter.errors}）")

    print_user_hints(getattr(_counter, "messages", []))

    # Chart.js 已内联进 HTML（见 render 层 [CHARTJS_LIB_PLACEHOLDER] 替换），无需附带外部 js 文件


# `generate` 的实现位于 aiweekly.render，此处保留转出口仅为兼容历史调用点
# `from generate_site import generate`（垫层，非本文件逻辑）。
__all__ = [
    "main", "generate",
]


if __name__ == "__main__":
    main()
