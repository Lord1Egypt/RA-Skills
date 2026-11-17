"""cite-holmes v6.0.0 模块层：ch_cli（由手术脚本从单文件引擎分层，
判定语义与 API 见壳 verify_refs.py 与 ADR-0010）。一切跨层符号与被
测试 patch 的函数一律经 _ROOT（由壳注入主壳命名空间）——patch 语义
与 trunk/mcp 双壳隔离（目录前缀加载）共同由该机制保证。"""

import argparse
import csv
import difflib
import hashlib
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from urllib.parse import urlparse, urlunparse, quote

_ROOT = None  # 由 verify_refs 壳注入


def _bind(root):
    global _ROOT
    _ROOT = root


def main_with_check_document(args, results, text_path):
    text = open(text_path, encoding="utf-8").read()
    cd = _ROOT.check_document(text, results, float(getattr(args, "anchor_threshold", 0.34) or 0.34))
    return cd


def main() -> int:
    ap = argparse.ArgumentParser(description="deep-research 引用机械验证器（五态判定）")
    ap.add_argument(
        "--refs", help="引用清单路径：JSON 数组（research_refs.json）或 BibTeX（refs.bib，v1.9）"
    )
    ap.add_argument(
        "--discover",
        help="v4.5.0 文献发现：主题检索双源（PubMed+OpenAlex）找文献，"
        '结果带官方标识符交全栈核验——出生即核验（如 --discover "bronchiolitis diagnosis"）',
    )
    ap.add_argument(
        "--discover-limit", type=int, default=10, help="文献发现每源条数上限（默认 10，封顶 25）"
    )
    ap.add_argument(
        "--discover-since",
        type=int,
        default=None,
        help="文献发现出版年下限（如 --discover-since 2020 只收 2020 及以后）",
    )
    ap.add_argument(
        "--discover-sort",
        choices=("relevance", "cited", "newest"),
        default="relevance",
        help="文献发现排序：relevance 相关性（默认）/ cited 被引优先"
        "（OpenAlex 直通，PubMed 无此序回退 relevance）/ newest 最新优先",
    )
    ap.add_argument(
        "--review-kit",
        action="store_true",
        help="v4.9.0 综述工作台：报告之外另出「综述就绪」三件套文件"
        "（综述表格+标注书目+即贴 GB/T 参考文献表，每条带官方核验"
        "判定与被引数；配合 --discover 主题检索即查即验即用）",
    )
    ap.add_argument(
        "--plan",
        default="",
        help="v5.2.0 研究计划工件：PLAN 阶段的结构化计划 JSON 路径"
        "（subquestions/budget_searches 必填，CALIBRATE 四要素缺失"
        "给 WARN）——引擎做完整性校验并渲染人读工件，绝不替用户改计划",
    )
    ap.add_argument(
        "--plan-out", default="", help="研究计划渲染输出路径（默认 research_plan.md；配合 --plan）"
    )
    ap.add_argument(
        "--source-policy",
        default="",
        help="v5.2.0 信源政策：journal_only（discover 期只留期刊源）/"
        "allow-domain=a.org|b.org/deny-domain=x.com（核验期注记+"
        "转人工，绝不改判定）；逗号分段、竖线分域",
    )
    ap.add_argument(
        "--trace",
        default="",
        help="v5.2.0 研究底稿：append-only 审计链——discover/verify 各轮"
        "追加轮次记录（主题/命中/政策过滤/判定分布），只追加绝不改写",
    )
    ap.add_argument(
        "--research-profile",
        default="",
        help="v5.3.0 持久研究档案：JSON 路径（preset/source_policy/"
        "export 三键作默认值注入，显式 CLI 旗标优先；未知键注记"
        "忽略）——跨会话研究偏好，绝不改判定语义",
    )
    ap.add_argument(
        "--reviewer",
        action="store_true",
        help="v5.4.0 审稿人预演嵌入：核验报告尾部自动追加对抗审查"
        "问题单（--grill 的同款生成器就地嵌入，免二跳；判定不变）",
    )
    ap.add_argument(
        "--check-paper",
        metavar="DOC",
        help="v6.1.0 投稿前审计包：完整论文稿件一条命令产出审计包——"
        "引用核验报告+稿件审计分级（P0/P1/P2）+GB/T/BibTeX 导出+"
        "INDEX 总览（机械层投稿就绪结论 READY/NOT READY+人工"
        "边界声明）。= --check-document + --audit-mode + "
        "--preset submission 的组合（含 csv 台账），另加 INDEX 装配；"
        "与 --check-document 同给时以本旗标为准",
    )
    ap.add_argument(
        "--audit-mode",
        action="store_true",
        help="v5.4.0 稿件审计：面向编辑/审稿人/教师输出审计风格报告"
        "（<out>.audit.md——疑点按 P0 编造嫌疑/P1 高风险线索/P2 "
        "复核项分级+行动清单；机械层口径，非语义判断）",
    )
    ap.add_argument(
        "--refs-dir",
        default="",
        help="v5.5.0 本地文献库批量：目录下全部 .json/.bib/.md 引用文件"
        "一次装载进同一核验批（按文件名排序；坏文件跳过并警告，"
        "全零才失败）——Zotero/JabRef 导出目录即扫即验",
    )
    ap.add_argument(
        "--next-round",
        dest="next_round",
        metavar="REPORT_JSON",
        default="",
        help="v5.5.0 下一轮种子：从 JSON 报告提取未决条目"
        "（partial/unreachable/unverified——invalid 不回收）生成"
        "可编辑的重验骨架 <stem>_next_round.json（零网络，判定"
        "原样透出）——把研究缺口变成下一轮输入",
    )
    ap.add_argument(
        "--demo",
        action="store_true",
        help="v4.5.0 零门槛体验：用内置样例清单（8 条含 3 处预埋伪造）跑完整判定流程",
    )
    ap.add_argument("--claims", help="内联 JSON 引用数组（同 --refs 的 schema）")
    ap.add_argument("--out", default="verify_report.md", help="Markdown 报告输出路径")
    ap.add_argument("--json-out", help="JSON 报告输出路径（默认 <out>.json）")
    ap.add_argument("--offline", action="store_true", help="不联网，仅结构/字段检查")
    ap.add_argument("--strict", action="store_true", help="unreachable/invalid 计为失败（exit 1）")
    ap.add_argument("--timeout", type=float, default=10.0, help="单 URL 超时秒数（默认 10）")
    ap.add_argument("--interval", type=float, default=1.0, help="请求间隔秒数（默认 1.0）")
    ap.add_argument(
        "--check-document",
        default="",
        help="v4.4.0 单文件模式:仅给文档路径(含参考文献节)即一体化核验;"
        "或配合 --refs 做文档级上下文核验:解析 in-text "
        "引用标记([12]/[1-4]/(Author, Year)/doi.org 链接),绑定 --refs "
        "核验结果并做锚词匹配(需与 --refs 同用)",
    )
    ap.add_argument(
        "--anchor-threshold",
        type=float,
        default=0.34,
        help="上下文核验锚词率阈值(默认 0.34;低于=疑似错配引文,人工复核)",
    )
    ap.add_argument(
        "--preflight",
        action="store_true",
        help="v3.7.0 注册库预检面板:核验前探测各官方源可达性(3s 超时)," "弱网环境先看状态再跑批",
    )
    ap.add_argument(
        "--preset",
        choices=["submission", "deep"],
        default="",
        help="v3.12 场景预设：submission=投稿前参考文献终检"
        "（--strict 严格退出码 + --export gbt7714,bibtex,csv 组合，"
        "判定语义不变，只打包常用旗标）；deep=v5.2 深度研究档"
        "（discover 上限抬至 25、超时下限 20s；搜索预算 ≤40 轮由"
        " agent 侧遵守，建议配 --workers 8）",
    )
    ap.add_argument(
        "--grill",
        metavar="REPORT_JSON",
        default="",
        help="v3.14 对抗审查：对已生成的 JSON 报告出「审稿人预演」问题单"
        "（逐条最强挑战+清单级追问，纯模板零网络，不改变任何判定）",
    )
    ap.add_argument(
        "--explain",
        type=int,
        metavar="N",
        default=None,
        help="v3.12 跑批后对第 N 条输出判定链人话解释"
        "（判定语义/依据步骤/错误码/注记/完整度/建议动作）",
    )
    ap.add_argument(
        "--doctor",
        action="store_true",
        help="v3.10 环境自检：零外呼体检（版本/缓存/配置/文件形态），"
        "配合 --net 加测各学术注册库连通性与延迟；FAIL 存在时退出码 1",
    )
    ap.add_argument(
        "--net", action="store_true", help="--doctor 配套：加测注册库连通性探针（单独使用无效果）"
    )
    ap.add_argument(
        "--cn",
        action="store_true",
        help="CN 韧性预设(v3.6)：超时下限 25s；DOI.org 三试全败时回源 "
        "api.crossref.org 同构 CSL(独立主机)；其余逻辑不变",
    )
    ap.add_argument(
        "--profile",
        choices=["general", "medical"],
        default="general",
        help="信源预设：medical=医学期刊层域名扩展(Cochrane/CTS/NMPA/CDC/万方等)+社区层降级警示",
    )
    ap.add_argument(
        "--export",
        help="附加导出，逗号分隔：bibtex（仅verified，可直接进论文）/ "
        "gbt7714（v3.6 GB/T 7714-2025 参考文献表,注册库元数据为准）/ "
        "ris（v3.7 RIS,Zotero/EndNote 通用）/ "
        "csv（全量审计台账）/ auditjson（v1.9 透明工作底稿：逐项检查明细）",
    )
    ap.add_argument(
        "--format",
        choices=["md", "html"],
        default="md",
        help="报告格式：md（默认）或 html（自包含单文件，零外链，可直接分享/存档）",
    )
    ap.add_argument(
        "--easy",
        action="store_true",
        help="傻瓜模式：自动识别医学引用启用医学预设，验证后自动导出 bibtex+csv，无需其他参数",
    )
    ap.add_argument(
        "--openalex-key",
        default="",
        help="OpenAlex API key（2026-02 起生产调用需要；也可用环境变量 OPENALEX_API_KEY）",
    )
    ap.add_argument(
        "--require-version",
        action="store_true",
        help="v6.4.0 M3 严格档：多修订版本 arXiv 引用未指定版本号时"
        "降 partial 人工确认版本（默认 off——仅注记不降级；"
        "未指定版本绝不判 invalid）",
    )
    ap.add_argument(
        "--judge-url",
        default="",
        help="L4 外置裁判端点（OpenAI 兼容 /chat/completions,如 ollama/llama-server;"
        "自备模型,cite-holmes 只出框架——零依赖不破）",
    )
    ap.add_argument(
        "--judge-model",
        default="qwen3.8-27b",
        help="L4 裁判模型名（配合 --judge-url；URL 带 /v1=OpenAI 兼容,否则=ollama 原生 think:false+结构化输出）",
    )
    ap.add_argument(
        "--no-contexts",
        action="store_true",
        help="关闭 L3 引文语境层（v3.0.0 默认开：verified 引文拉取 S2 引用语境/学界评价）",
    )
    ap.add_argument(
        "--ncbi-key",
        default="",
        help="NCBI E-utilities API key（3→10 req/s 提速并行批验证；"
        "也可用环境变量 NCBI_API_KEY）",
    )
    ap.add_argument(
        "--s2-key",
        default="",
        help="Semantic Scholar API key（免钥为共享限速池；也可用环境变量 S2_API_KEY）",
    )
    ap.add_argument(
        "--nli-url",
        default="",
        help="L2 NLI 第三票服务(nli_service.py;弃权式,分歧标人工复核不翻案)",
    )
    ap.add_argument(
        "--fast-judge-url",
        default="",
        help="fast-judge 预筛服务(任何 OpenAI 兼容端点;小型分类器即可——仅对语义"
        "待定且无官方文本可升级的条目做预筛,高置信 SUPPORTS 只加参考"
        "note 永不判定;默认关闭)",
    )
    ap.add_argument(
        "--fast-judge-threshold",
        type=float,
        default=0.95,
        help="fast-judge 预筛 note 触发阈值(默认 0.95=校准曲线选定:"
        "SUPPORTS 精度 0.82/覆盖 0.32;模型过度自信,top 桶 0.97 置信"
        "实际 acc 0.77——故产品姿态=note-only 永不判定;精度优先可调 0.99)",
    )
    ap.add_argument(
        "--retraction-cache",
        default="",
        help="撤稿本地缓存 JSON 索引（Crossref GitLab dump 构建,63k+ DOI;"
        "命中零网络,离线可用;未配置走 Crossref 在线查询）",
    )
    ap.add_argument(
        "--mailto",
        default="",
        help="联系邮箱：进入 Crossref polite pool（限速更宽松），机构/CI 用户建议配置",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=4,
        help="引用并行验证线程数（默认 4；1=串行；offline 模式自动串行）。"
        "条与条独立，整批耗时约 ÷N；v1.10 新增",
    )
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="关闭持久磁盘缓存（v1.12 默认开：TTL 内复跑直接复用稳定判定，零外呼）",
    )
    ap.add_argument(
        "--cache-ttl",
        type=float,
        default=168.0,
        help="磁盘缓存有效期小时数（默认 168=7 天；撤稿状态等可变信息以 TTL 为界）",
    )
    ap.add_argument(
        "--cache-path",
        default="~/.cache/cite-holmes/cache.sqlite3",
        help="磁盘缓存文件路径（默认 ~/.cache/cite-holmes/cache.sqlite3）",
    )
    ap.add_argument(
        "--refresh-cache", action="store_true", help="绕过缓存读取强制重验（结果仍回写缓存）"
    )
    ap.add_argument(
        "--proxy",
        default="",
        help="显式 HTTP(S) 代理地址（如 http://127.0.0.1:7890）；"
        "不指定时自动遵循 HTTP_PROXY/HTTPS_PROXY 环境变量",
    )
    args = ap.parse_args()
    if getattr(args, "research_profile", ""):  # v5.3.0 F33 档案默认值（显式旗标优先）
        _profile_applied = _ROOT.apply_research_profile(args.research_profile, args)
        if _profile_applied is None:
            return 2  # 硬错误已打印
        if _profile_applied:
            print(
                f"[profile] 研究档案已应用（{os.path.basename(args.research_profile)}）："
                + "；".join(_profile_applied)
                + "——显式旗标优先，判定语义不变"
            )
    if getattr(args, "check_paper", ""):  # v6.1.0 F51 投稿前审计包：组合旗标不改判定语义
        args.check_document = args.check_paper  # 同一条稿件解析通路（复用不重造）
        args.audit_mode = True
        args.strict = True
        _user_exp = [x for x in (args.export or "").split(",") if x]
        for _e in ("gbt7714", "bibtex", "csv"):
            if _e not in _user_exp:
                _user_exp.append(_e)
        args.export = ",".join(_user_exp)
        print(
            "[check-paper] 投稿前审计包：--check-document + --audit-mode + "
            "--strict + GB/T/BibTeX 导出已组合，另出 INDEX 就绪总览"
            "（判定语义与逐项模式完全一致）"
        )
    if getattr(args, "preset", "") == "submission":  # v3.12 投稿终检预设:组合旗标不改判定语义
        args.strict = True
        args.export = args.export or "gbt7714,bibtex,csv"
        print(
            f"[preset] submission：--strict + --export {args.export} 已组合"
            "（投稿前一键终检；判定语义与默认模式完全一致。"
            "注意 --strict 语义含绕过磁盘缓存读——复跑为全量外呼）"
        )
    if getattr(args, "preset", "") == "deep":  # v5.2.0 深度研究档（Google DR 分档借鉴）
        args.discover_limit = max(int(args.discover_limit or 10), 25)
        args.timeout = max(float(args.timeout or 10.0), 20.0)
        print(
            "[preset] deep：discover 上限 25 · 超时 ≥20s（搜索预算 ≤40 轮由 agent 侧"
            "遵守，建议配 --workers 8；判定语义与默认模式完全一致）"
        )
    _policy = None
    if getattr(args, "source_policy", ""):
        _policy = _ROOT._parse_source_policy(args.source_policy)
        if _policy is None:
            print(
                "❌ --source-policy 格式不合法（支持 journal_only / "
                "allow-domain=a.org|b.org / deny-domain=x.com；逗号分段、竖线分域）",
                file=sys.stderr,
            )
            return 2
        _pol_desc = [
            k
            for k, v in (
                ("journal_only", _policy["journal_only"]),
                ("allow-domain", _policy["allow"]),
                ("deny-domain", _policy["deny"]),
            )
            if v
        ]
        print(
            f"[policy] 信源政策已装载：{' + '.join(_pol_desc)}"
            "（discover 期策展过滤；核验期注记不改判定）"
        )
    if getattr(args, "plan", ""):  # v5.2.0 F28 计划工件：校验+渲染（可独立子命令式退出）
        try:
            with open(os.path.expanduser(args.plan), encoding="utf-8") as f:
                _plan_doc = json.load(f)
        except (OSError, ValueError) as e:
            print(f"❌ 研究计划读取失败：{e}（--plan 需要结构化 JSON 计划）", file=sys.stderr)
            return 2
        _plan_warns = _ROOT.render_plan_artifact(_plan_doc, args.plan_out or "research_plan.md")
        if _plan_warns is None:
            return 2  # 硬错误已在函数内打印
        if _plan_warns:
            print(
                f"[plan] 计划工件已渲染，{len(_plan_warns)} 项 WARN（CALIBRATE "
                "要素缺失——agent 侧补齐默认值后可重跑校验）"
            )
        if not (args.refs or args.claims or args.discover or args.check_document or args.demo):
            return 0  # 仅计划模式：渲染完即退（协作定稿后用户可编辑再执行）
    if getattr(args, "grill", ""):
        gpath = os.path.expanduser(args.grill)
        if not os.path.isfile(gpath):
            print(f"❌ 报告文件不存在：{gpath}（--grill 需要一次真实核验产出的 JSON 报告）")
            return 2
        try:
            with open(gpath, encoding="utf-8") as f:
                doc = json.load(f)
        except (ValueError, UnicodeDecodeError) as e:
            print(
                f"❌ 不是有效的 JSON 报告：{gpath}（{type(e).__name__}）——"
                "请先跑一次 --refs 核验生成报告"
            )
            return 2
        if not (doc.get("results") or []):
            print(f"❌ {gpath} 内无 results 字段——请提供本工具生成的完整 JSON 报告")
            return 2
        items = _ROOT.grill_report(doc.get("results") or [])
        sc = doc.get("scorecard") or {}
        out = args.out if args.out != "verify_report.md" else gpath.rsplit(".", 1)[0] + "_grill.md"
        with open(out, "w", encoding="utf-8") as f:
            f.write(_ROOT.render_grill_md(items, sc))
        n_q = sum(len(x["questions"]) for x in items)
        print(f"[grill] 对抗审查问题单：{len(items)} 条引用 · {n_q} 个挑战问题 → {out}")
        print("[grill] 判定不变（自查工具）；逐条作答后再投稿。")
        return 0
    if getattr(args, "next_round", ""):  # v5.5.0 F41 下一轮种子（零网络，独立退出）
        _nr_path = os.path.expanduser(args.next_round)
        if not os.path.isfile(_nr_path):
            print(
                f"❌ 报告文件不存在：{_nr_path}（--next-round 需要一次核验的 JSON 报告）",
                file=sys.stderr,
            )
            return 2
        try:
            with open(_nr_path, encoding="utf-8") as f:
                _nr_doc = json.load(f)
            _nr_out = (
                _nr_path.rsplit(".", 1)[0] if "." in _nr_path else _nr_path
            ) + "_next_round.json"
            _nr_out, _nr_n = _ROOT.build_next_round(_nr_doc, _nr_out)
        except (ValueError, OSError) as e:
            print(f"❌ 下一轮种子生成失败：{e}", file=sys.stderr)
            return 2
        print(
            f"[next-round] 重验骨架：{_nr_out}（{_nr_n} 条未决："
            "partial/unreachable/unverified；invalid 不回收）——修订后作 --refs 输入"
        )
        return 0
    if getattr(args, "doctor", False):
        return _ROOT.run_doctor(
            net=getattr(args, "net", False),
            timeout=min(args.timeout, 8.0),
            cache_path=args.cache_path,
        )
    medical = args.profile == "medical"
    _ROOT._net_reset()  # 断路器+全局网络降级状态按批次重置（v1.6/v1.10）
    if args.proxy.strip():
        proxy = args.proxy.strip()
        if "://" not in proxy:
            proxy = "http://" + proxy
        urllib.request.install_opener(
            urllib.request.build_opener(
                urllib.request.ProxyHandler({"http": proxy, "https": proxy})
            )
        )
        print(f"[proxy] 显式代理已启用：{proxy}")
    if getattr(args, "cn", False) and args.timeout < 25:
        args.timeout = 25.0  # --cn 超时下限(v3.6):跨国 RTT 抖动下不误判 unreachable
    if getattr(args, "preflight", False):
        # v3.7.0 注册库预检面板:3s 探测,弱网先看状态再跑批(CN 韧性可观测化)
        import socket as _sk

        print("== 注册库预检(3s 超时) ==")
        for name, host, port in (
            ("DOI.org", "doi.org", 443),
            ("PubMed E-utilities", "eutils.ncbi.nlm.nih.gov", 443),
            ("arXiv", "export.arxiv.org", 443),
            ("Crossref", "api.crossref.org", 443),
            ("Semantic Scholar", "api.semanticscholar.org", 443),
            ("Wayback", "web.archive.org", 443),
        ):
            t0 = time.time()
            try:
                _sk.create_connection((host, port), timeout=3)
                st = f"✓ 可达 ({(time.time()-t0)*1000:.0f}ms)"
            except Exception as e:
                st = f"✗ 不可达({type(e).__name__})"
            print(f"  {name:20s} {st}")
    args.cache = not args.no_cache
    args.cache_path = os.path.expanduser(args.cache_path)
    _ROOT._OPTS.update(
        {
            "openalex_key": args.openalex_key or os.environ.get("OPENALEX_API_KEY", ""),
            "require_version": bool(args.require_version),
            "s2_key": args.s2_key or os.environ.get("S2_API_KEY", ""),
            "ncbi_key": args.ncbi_key or os.environ.get("NCBI_API_KEY", ""),
            "retraction_cache": args.retraction_cache.strip(),
            "nli_url": args.nli_url.strip(),
            "fast_judge_url": args.fast_judge_url.strip(),
            "fast_judge_threshold": args.fast_judge_threshold,
            "mailto": args.mailto.strip(),
            "contexts": not args.no_contexts,
            "cn_mode": bool(getattr(args, "cn", False)),
            "judge_url": args.judge_url.strip(),
            "judge_model": args.judge_model.strip(),
        }
    )

    refs = None
    if getattr(args, "demo", False) and not args.refs and not args.claims:
        _demo = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "examples", "demo_refs.json"
        )
        try:
            with open(_demo, encoding="utf-8") as f:
                refs = json.load(f)
        except OSError:
            # v6.2.0 安装态（uvx/pip wheel）不随带 examples/——给可操作指引而非堆栈
            print(
                "❌ --demo 样例文件不在当前安装形态中（wheel 分发仅含引擎与 MCP 层）。"
                "替代：用 --refs 指向自己的引用清单（JSON/BibTeX 均可），或从 "
                "GitHub 仓库 docsor1212/cite-holmes 获取完整目录后跑 --demo。"
            )
            return 2
        print(f"[demo] 内置样例清单 {len(refs)} 条（含 3 处预埋伪造）——体验五态判定全流程")
    if getattr(args, "discover", "") and not args.refs and not args.claims and not refs:
        if args.offline:
            print("❌ 文献发现需要联网检索——--offline 模式不适用", file=sys.stderr)
            return 2
        _drefs, _dnotes = _ROOT.discover_refs(
            args.discover,
            args.discover_limit,
            args.timeout,
            since=getattr(args, "discover_since", None),
            sort=getattr(args, "discover_sort", "relevance"),
            policy=_policy,
        )
        for _n in _dnotes:
            print(f"[discover] {_n}")
        if getattr(args, "trace", ""):
            _ROOT._trace_append(
                args.trace,
                "discover",
                {
                    "topic": args.discover,
                    "limit": args.discover_limit,
                    "命中": f"{len(_drefs)} 条（去重+政策过滤后）",
                    "notes": "；".join(_dnotes) or "（无）",
                },
            )
        if _drefs:
            refs = _drefs
            print(f"[discover] 双源命中 {len(refs)} 条（去重后）——进入核验栈，出生即核验")
        else:
            print("❌ 文献发现双源零命中——请换检索词或检查网络", file=sys.stderr)
            return 2
    if getattr(args, "check_document", "") and not refs and not args.refs and not args.claims:
        # v4.4.0 单文件一体化：--check-document 独用=从文档自身「参考文献」
        # 节提取清单再全量核验——dogfood 实录同一文件传两遍是最大使用摩擦
        # （审计 P2：not refs 守卫——否则无条件覆盖 demo/discover 已装载清单）
        try:
            _doctext = open(args.check_document, encoding="utf-8", errors="replace").read()
        except (OSError, ValueError) as e:
            print(f"❌ 读取文档失败：{e}", file=sys.stderr)
            return 2
        refs = _ROOT.parse_markdown_refs(_doctext)
        if refs:
            print(f"[one-file] 自文档参考文献节提取 {len(refs)} 条（GB/T/Vancouver）")
    if (
        getattr(args, "refs_dir", "") and not refs and not args.refs and not args.claims
    ):  # v5.5.0 审计 P2-3：互斥序对齐 discover/_ROOT.check_document
        import glob as _glob

        _rd = os.path.expanduser(args.refs_dir)
        if os.path.isfile(_rd):
            _files = [_rd]
        elif os.path.isdir(_rd):
            _files = sorted(
                p
                for ext in ("*.json", "*.bib", "*.md")
                for p in _glob.glob(os.path.join(_rd, ext))
                if not os.path.basename(p).startswith("README")
            )
        else:
            print(f"❌ --refs-dir 路径不存在：{_rd}", file=sys.stderr)
            return 2
        if not _files:
            print(f"❌ {_rd} 下没有 .json/.bib/.md 引用文件", file=sys.stderr)
            return 2
        refs = []
        for _fp in _files:
            try:
                _part = _ROOT.load_refs_file(_fp)
            except (OSError, ValueError) as e:
                print(f"[refs-dir] 跳过 {_fp}（{type(e).__name__}）", file=sys.stderr)
                continue
            if _part:
                refs.extend(_part)
                print(f"[refs-dir] {_fp}: {len(_part)} 条")
        if not refs:
            print("❌ 文献库批量装载为 0 条（全部文件空或无参考文献节）", file=sys.stderr)
            return 2
        print(f"[refs-dir] 批量装载 {len(refs)} 条（来自 {len(_files)} 个文件）——进入核验栈")
    if not args.refs and not args.claims and not refs:
        print(
            "❌ 需要 --refs 或 --claims 之一；--check-document 指向含「参考文献」节"
            "的文档（v4.4.0 单文件模式）；--discover 主题检索（v4.5.0 文献发现）；"
            "或 --demo 零门槛体验",
            file=sys.stderr,
        )
        return 2
    try:
        if args.claims:
            refs = json.loads(args.claims)
        elif args.refs:
            refs = _ROOT.load_refs_file(args.refs)  # v1.9：JSON 或 BibTeX 自动识别
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"❌ 读取引用清单失败：{e}", file=sys.stderr)
        print(
            "   支持 JSON 数组（research_refs.json）或 BibTeX 文件（v1.9 起 --refs refs.bib）",
            file=sys.stderr,
        )
        return 2
    if not isinstance(refs, list) or not refs:
        print("❌ 引用清单须为非空数组（JSON 或 BibTeX）", file=sys.stderr)
        return 2

    if args.easy:
        # 傻瓜模式：有 PMID/PubMed 信号 → 直接启用医学预设；仅医学期刊域命中
        # （如万方）需 ≥2 条才触发——v1.8 修复：单条万方来源的技术类清单被误判成医学清单
        hints = False
        med_hits = 0
        for r in refs:
            if not isinstance(r, dict):
                continue
            u = str(r.get("url") or "")
            if str(r.get("pmid") or "").strip() or "pubmed" in u.lower():
                hints = True
                break
            # v4.2.0：中文医学注册库升为无条件 journal 层后，「medical 才升层」
            # 信号对它们失效——改用显式注册库清单计数
            if re.search(r"(wanfangdata|cnki|yiigle|cqvip)\.", u.lower()):
                med_hits += 1
                continue
            try:
                if (
                    _ROOT.classify_tier(u, True) == "journal"
                    and _ROOT.classify_tier(u, False) == "blog"
                ):
                    med_hits += 1
            except Exception:
                pass
        if not hints and med_hits >= 2:
            hints = True
        if hints:
            args.profile = "medical"
        if not args.export:
            args.export = "bibtex,csv"
        medical = args.profile == "medical"
        print(f"[easy] 傻瓜模式：医学预设={'开' if medical else '关'}；自动导出 {args.export}")

    def _safe_verify_one(i, ref):
        # 单条坏数据（非对象/标量）确凿 invalid；处理异常降 unverified+转人工
        # （v5.8.0 语义保真：程序故障≠确凿判死），两类都绝不拖垮整批
        if not isinstance(ref, dict):
            return {
                "index": i,
                "title": str(ref)[:48],
                "url": "",
                "doi": "",
                "pmid": "",
                "arxiv": "",
                "source": "",
                "year": None,
                "tier": "-",
                "semantic": "",
                "verdict": "invalid",
                "http_status": None,
                "note": "条目不是对象",
                "needs_human_check": False,
                "checks": {},
            }
        # v1.12 持久磁盘缓存：TTL 内复用稳定判定（复跑零外呼）；--strict 绕过读保 CI
        # 诚实；--refresh-cache 绕过读但仍写；offline 不读不写（offline 判定不可入库）。
        # 仅带标识符(doi/url/pmid/arxiv)的引用入缓存——与批内缓存同口径；
        # 纯标题引用不走磁盘缓存（其判定多为结构性 invalid，无外呼可省）
        dc_key = (
            _ROOT._dc_key(ref, args.profile)
            if (args.cache and not args.offline and _ROOT._cache_key(ref))
            else ""
        )
        if dc_key and not args.strict and not args.refresh_cache:
            hit = _ROOT._dc_get(_ROOT._dc_path(args), dc_key, args.cache_ttl)
            if hit is not None:
                r, age_h = hit
                r = dict(r)
                r["index"] = i
                r["note"] = (
                    (r.get("note") + "；") if r.get("note") else ""
                ) + f"磁盘缓存命中（{age_h:.0f}h 前验证；--refresh-cache 强制重验）"
                return r
        try:
            r = _ROOT.verify_one(ref, i, args.offline, args.timeout, medical)
        except Exception as e:
            # v5.8.0 语义保真：程序故障≠机械层确凿判死——invalid 的语义保留给
            # 真实伪造（评测 errorHandling 点名），故障条目降 unverified+转人工；
            # 审计 P2：回填原始标识符，--next-round 骨架不退化为纯标题重试
            return {
                "index": i,
                "title": str(ref.get("title") or "")[:48] or "(无标题)",
                "url": str(ref.get("url") or ""),
                "doi": str(ref.get("doi") or ""),
                "pmid": str(ref.get("pmid") or ""),
                "arxiv": str(ref.get("arxiv") or ""),
                "source": str(ref.get("source") or ""),
                "year": ref.get("year"),
                "tier": "-",
                "semantic": "",
                "verdict": "unverified",
                "http_status": None,
                "note": f"条目处理异常（{type(e).__name__}）——非判定结果，"
                f"建议 --refresh-cache 重跑；持续复现请反馈",
                "needs_human_check": True,
                "checks": {},
            }
        if dc_key and r.get("verdict") in _ROOT._DC_CACHEABLE:
            _ROOT._dc_put(_ROOT._dc_path(args), dc_key, r)
        return r

    results = [None] * len(refs)
    workers = max(1, int(args.workers or 1))
    if args.offline or workers <= 1 or len(refs) <= 1:
        # 串行路径（offline 模式 / --workers 1 / 单条）：保留逐条 interval 控频
        for i, ref in enumerate(refs, 1):
            r = _safe_verify_one(i, ref)
            results[i - 1] = r
            print(f"[{i}/{len(refs)}] {_ROOT.VERDICT_ZH[r['verdict']]} {r['title'][:40]}")
            if not args.offline and i < len(refs) and args.interval > 0:
                time.sleep(args.interval)
    else:
        # v1.10 引用级并行验证：条与条相互独立（共享状态仅断路器/限速器，均已加锁），
        # 整批耗时约 ÷workers——跨国数据库验证慢的机制层缓解。进度行按完成顺序
        # 打印（带真实序号），最终结果按 index 有序回填，报告/JSON 顺序与串行一致。
        # 并行下不做逐条 interval（并发本身就是节流；单主机礼貌由断路器+限速锁保证）。

        def _task(i, ref):
            # 双保险：任何意外异常都降 unverified+转人工（v5.8.0 语义保真），
            # 绝不拖垮整批
            try:
                return _safe_verify_one(i, ref)
            except Exception as e:
                return {
                    "index": i,
                    "title": (
                        str(ref.get("title") if isinstance(ref, dict) else ref)[:48] or "(无标题)"
                    ),
                    "url": "",
                    "doi": "",
                    "pmid": "",
                    "arxiv": "",
                    "source": "",
                    "year": None,
                    "tier": "-",
                    "semantic": "",
                    "verdict": "unverified",
                    "http_status": None,
                    "note": f"条目处理异常（{type(e).__name__}）——非判定结果，"
                    f"建议 --refresh-cache 重跑；持续复现请反馈",
                    "needs_human_check": True,
                    "checks": {},
                }

        with ThreadPoolExecutor(max_workers=min(workers, len(refs))) as ex:
            # v1.10 批内缓存（领导者-跟随者）：同 DOI/URL/PMID/arXiv 只验证一次。
            # 并行下两条同键引用会同时起飞，「先查缓存后存储」永远轮空——④c 真网
            # 验收抓到，改为派发前去重：首个入键者为领导者，其余为跟随者，待领导者
            # 完成后复制判定（跟随者零网络调用）。
            futs = {}
            leader_of, followers = {}, {}
            for i, ref in enumerate(refs, 1):
                key = _ROOT._cache_key(ref) if isinstance(ref, dict) else ()
                if key and key in leader_of:
                    followers.setdefault(leader_of[key], []).append(i)
                    continue
                if key:
                    leader_of[key] = i
                futs[i] = ex.submit(_task, i, ref)
            for fut in as_completed(futs.values()):
                r = fut.result()
                results[r["index"] - 1] = r
                print(
                    f"[{r['index']}/{len(refs)}] {_ROOT.VERDICT_ZH[r['verdict']]} {r['title'][:40]}"
                )
            for lead_idx in sorted(followers):
                lead = results[lead_idx - 1]
                for j in followers[lead_idx]:
                    r = dict(lead)
                    r["checks"] = dict(lead.get("checks") or {})
                    r["index"] = j
                    # v1.11 语义底稿按各自引用重建（缓存只复用机械判定——同
                    # DOI/URL 的两条引用可以引向不同论断，语义判定不得共享）
                    r["semantic_audit"] = _ROOT.build_semantic_audit(refs[j - 1])
                    r["note"] = (
                        (lead.get("note") + "；") if lead.get("note") else ""
                    ) + "同 DOI/URL 本批已验证，复用缓存判定"
                    results[j - 1] = r
                    print(f"[{j}/{len(refs)}] {_ROOT.VERDICT_ZH[r['verdict']]} {r['title'][:40]}")
        if _ROOT._NET_STATE["degraded"]:
            print(
                "⚠️ 全局网络降级：本批次多个外部主机连续传输失败（出海受限特征），"
                "部分外呼已快速跳过——建议配置代理/更换网络后重跑以获得更完整结果"
            )

    _ROOT.mark_duplicates(results)
    _n_clone = _ROOT.detect_clone_pairs(results)  # v3.10 克隆引用搭档检测（只注记不改判定）
    if _n_clone:
        print(
            f"[clone] 克隆引用对 {_n_clone} 组（同题不同 DOI / 同 DOI 不同题）——详见报告克隆引用对区块"
        )
    # v3.11 预印本→正式版提示（注记级;offline 显式零网络,不依赖跨函数不变量）
    _n_preprint = 0 if args.offline else _ROOT.annotate_preprint_upgrades(results, args.timeout)
    if _n_preprint:
        print(f"[preprint] {_n_preprint} 条预印本已登记正式发表——建议引用正式版（详见各条注记）")
    _ROOT.annotate_completeness(results)  # v3.11 逐条完整度（JSON 字段）
    _ROOT.apply_semantic_cap(results)  # v1.11：语义否定判定封顶（在去重后统一执行）
    for _r in results:  # v3.9.0 结构化错误码(errorHandling):五态之上的机器可读细分
        try:
            _r["error_codes"] = _ROOT.derive_error_codes(_r)
        except Exception:
            _r["error_codes"] = []
    _ROOT.apply_l4_cascade(
        results, args.timeout
    )  # v3.1：L4 证据升级级联（--judge-url 时激活；零配置零变化）
    _ROOT.apply_fast_judge(
        results, args.timeout
    )  # v3.5.0：fast-judge 预筛（--fast-judge-url 时激活；零配置零变化）
    _n_pol = _ROOT.apply_source_policy(results, _policy, medical)  # v5.2.0 注记级，绝不改判定
    if _n_pol:
        print(f"[policy] {_n_pol} 条命中信源政策（注记+转人工，判定不变——详见各条注记）")
    scorecard = _ROOT.compute_scorecard(results)
    if getattr(args, "trace", ""):
        c2 = scorecard["counts"]
        _ROOT._trace_append(
            args.trace,
            "verify",
            {
                "条数": len(results),
                "判定": " ".join(
                    f"{k} {c2.get(k, 0)}"
                    for k in ("verified", "partial", "unreachable", "invalid", "unverified")
                ),
                "CiteScore": f"{scorecard['score']}/100 {scorecard['grade']}",
                "政策注记": _n_pol,
            },
        )
    cd = None
    if getattr(args, "check_document", ""):
        cd = _ROOT.check_document(
            open(args.check_document, encoding="utf-8", errors="replace").read(),
            results,
            float(args.anchor_threshold),
        )
    content = (
        _ROOT.render_html(results, args.offline, args.profile, context_check=cd)
        if args.format == "html"
        else _ROOT.render_md(results, args.offline, args.profile, context_check=cd)
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(content)
    json_path = args.json_out or (args.out.rsplit(".", 1)[0] + ".json")
    _json_doc = {
        "version": _ROOT.VERSION,
        "profile": args.profile,
        "offline": args.offline,
        "bluf": _ROOT.render_bluf_dict(results, scorecard),  # v3.2.0 规范 L1:对象
        "bluf_yaml": _ROOT.render_bluf(results, scorecard),  # 兼容:YAML 文本
        "scorecard": scorecard,
        "results": results,
        "bibliography_profile": _ROOT.profile_bibliography(results),
    }  # v3.11 清单画像
    if cd is not None:
        _json_doc["context_check"] = cd
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(_json_doc, f, ensure_ascii=False, indent=2)
    if cd is not None:
        print(f"\n== 上下文核验({args.check_document}) ==")
        print(
            f"  in-text 引用 {cd['n_citations']} 处:未绑定 {cd['n_unbound']},"
            f"锚词不足 {cd['n_low_anchor']}(阈值 {cd['anchor_threshold']})"
        )
        if cd.get("n_listed"):
            print(
                f"  引用覆盖 {cd['coverage']:.0%}:清单 {cd['n_listed']} 条中 "
                f"{cd['n_uncited']} 条未在正文引用"
                f"{(':' + '、'.join(str(i) for i in (cd.get('uncited_refs') or [])[:10]) + ('…' if len(cd.get('uncited_refs') or []) > 10 else '')) if cd.get('uncited_refs') else ''}"
                "（漏引或冗列建议，非真伪判定）"
            )
        for c in cd["citations"][:12]:
            flag = (
                "未绑定"
                if not c["bound"]
                else f"锚词率 {c['anchor_rate']}{'⚠' if c['anchor'] == 'low' else ''}"
            )
            print(f"  {c['marker']:22s} → 条目{c['ref_index'] or '-'} {flag}")
        if cd["n_citations"] > 12:
            print(f"  …其余 {cd['n_citations'] - 12} 处见 JSON")
    print(f"CiteScore: {scorecard['score']}/100 ({scorecard['grade']} 级，{scorecard['total']} 条)")

    if getattr(args, "explain", None) is not None:  # v3.12 单条判定链人话解释
        target = next((r for r in results if r.get("index") == args.explain), None)
        print()
        print(
            _ROOT.explain_ref(target)
            if target
            else f"第 {args.explain} 条不存在——有效范围 1-{len(results)}"
        )

    if getattr(args, "review_kit", False) and not args.export:
        args.export = "gbt7714,bibtex"  # 综述工作台：即贴书目+BibTeX 默认齐活
    if args.export:
        base = args.out.rsplit(".", 1)[0] if "." in args.out else args.out
        for fmt in [x.strip().lower() for x in args.export.split(",") if x.strip()]:
            if fmt == "bibtex":
                p = base + ".bib"
                n = _ROOT.export_bibtex(results, p)
                print(f"导出：{p}（{n} 条 verified，可直接进论文）")
            elif fmt == "ris":
                p = base + ".ris"
                n = _ROOT.export_ris(results, p)
                print(f"导出：{p}（{n} 条，RIS/Zotero/EndNote 通用）")
            elif fmt in ("gbt7714", "gb"):
                p = base + "_GB-T7714.txt"
                n = _ROOT.export_gbt7714(results, p)
                print(
                    f"导出：{p}（{n} 条 verified/元数据一致，GB/T 7714-2025 参考文献表，"
                    "元数据以注册库登记为准）"
                )
            elif fmt == "csv":
                p = base + ".csv"
                _ROOT.export_csv(results, p)
                print(f"导出：{p}（{len(results)} 条全量审计台账）")
            elif fmt == "auditjson":
                p = base + ".audit.json"
                _ROOT.export_audit(results, p, args.offline, args.profile)
                print(f"导出：{p}（透明工作底稿：逐项检查明细）")
            else:
                print(
                    f"⚠️ 未知导出格式 {fmt}（支持 bibtex,gbt7714,ris,csv,auditjson）",
                    file=sys.stderr,
                )

    if getattr(args, "review_kit", False):
        base = args.out.rsplit(".", 1)[0] if "." in args.out else args.out
        _kit_path = base + ".review_kit.md"
        _kit = _ROOT.build_review_kit(
            results,
            refs,
            topic=str(getattr(args, "discover", "") or ""),
            cite_date=time.strftime("%Y-%m-%d"),
        )
        with open(_kit_path, "w", encoding="utf-8") as f:
            f.write(_kit)
        _n_kit = sum(1 for _ln in _kit.splitlines() if re.match(r"\[\d+\] ", _ln))
        print(f"综述工作台：{_kit_path}（综述表格/标注书目/即贴 GB/T 参考文献表 " f"{_n_kit} 条）")

    if getattr(args, "reviewer", False):  # v5.4.0 F34：审稿人预演就地嵌入（免二跳）
        _items = _ROOT.grill_report(results)
        with open(args.out, "a", encoding="utf-8") as f:
            f.write("\n\n---\n\n" + _ROOT.render_grill_md(_items, scorecard))
        print(
            f"[reviewer] 审稿人预演问题单已嵌入报告尾部"
            f"（{sum(len(x['questions']) for x in _items)} 个挑战；判定不变）"
        )
    if getattr(args, "audit_mode", False):  # v5.4.0 F35：稿件审计报告
        _audit_path = (args.out.rsplit(".", 1)[0] if "." in args.out else args.out) + ".audit.md"
        with open(_audit_path, "w", encoding="utf-8") as f:
            f.write(_ROOT.render_audit_report(results, cd, scorecard))
        print(f"稿件审计：{_audit_path}（P0 编造嫌疑/P1 高风险/P2 复核 分级+行动清单）")
    if getattr(args, "check_paper", ""):  # v6.1.0 F51：INDEX 就绪总览（审计包最后一件）
        _arts = [os.path.basename(args.out), os.path.basename(json_path)]
        if getattr(args, "audit_mode", False):
            _arts.append(os.path.basename(_audit_path))
        for _sfx in ("_GB-T7714.txt", ".bib", ".csv"):
            _p = args.out.rsplit(".", 1)[0] + _sfx
            if os.path.exists(_p):
                _arts.append(os.path.basename(_p))
        _idx_path = args.out.rsplit(".", 1)[0] + ".INDEX.md"
        with open(_idx_path, "w", encoding="utf-8") as f:
            f.write(_ROOT.build_submission_index(results, cd, scorecard, _arts))
        _rd = _ROOT.submission_readiness(results, cd)
        print(
            f"投稿审计包 INDEX：{_idx_path}（就绪结论："
            f"{'READY——机械层零阻断项' if _rd['ready'] else 'NOT READY——见阻断清单'}）"
        )

    _n_crash = sum(1 for r in results if str(r.get("note") or "").startswith("条目处理异常"))
    if _n_crash:
        # 审计 P2：整体性引擎故障=全 unverified+exit 0，CI 机器信号会全哑——
        # strict 下对「处理异常」条目显式 stderr 警示，防故障被当干净批吞掉
        print(
            f"⚠️ {_n_crash} 条处理异常（unverified，不计 strict 失败）——"
            "若整批大面积出现，多为引擎/环境故障而非引用问题，请排查后重跑",
            file=sys.stderr,
        )
    bad = [r for r in results if r["verdict"] in ("unreachable", "invalid")]
    print(f"\n报告：{args.out}\nJSON：{json_path}")
    if bad:
        print(
            f"⚠️ {len(bad)} 条 unreachable/invalid"
            + ("（strict 模式 → exit 1）" if args.strict else "")
        )
    return 1 if (args.strict and bad) else 0
