#!/usr/bin/env python3
"""publish.py — 组装本周头条 report.json 并经飞书连接器推送头条卡片（P0）。

数据来源（均为 generate_site.py 已产出的结构化产物，不重新跑生成器）：
  --news-json       news.json        {count, items[{title,url,summary,source,category,score}]}
  --insights-json   insights.json    {lead, insights[{kicker,title,insight}], keywords[], audience_summary?}
  --audience-json   audience_summary.json  {角色: 摘要}   (可选，缺省回退 insights.audience_summary)

产出：
  --output report.json   本周头条结构化载荷（headlines/insights/audience/keywords/view_url）
  --dry-run              仅构造卡片并打印，不发起网络请求

推送通道：**飞书连接器（lark-cli，密钥由连接器托管，绝不落配置文件）**，取代原 Webhook 自定义机器人路径。
目标会话解析（优先级，首个命中生效）：
  1. --chat-id / --user-id CLI 参数
  2. 环境变量 FEISHU_CHAT_ID / FEISHU_USER_ID
  3. delivery/feishu_target.json {"chat_id": "oc_xxx"} 或 {"user_id": "ou_xxx"}
  三者皆空 -> 仅警告、exit 0（不阻断上游生成管线，符合"推送失败不丢报告"原则）。

度量：view_url 自动追加 ?src=feishu&uid=<uid>，uid 默认 auto 生成短 uuid。

合规：经 WorkBuddy 飞书连接器（lark-cli）发送，不引入任何第三方商业 API / SDK，webhook token 不落仓库。
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

# 让 repo 根（含 delivery/ 包）可导入
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from delivery.feishu_bot import build_headline_card  # noqa: E402
from delivery.feishu_connector import resolve_target, send_card  # noqa: E402

# 关键词保送集（与 aiweekly.insights._PRIORITY_ALIASES 对齐，确保民间绰号等
# 高感知词在飞书卡片 6 槽截断时不被吃掉）。导入失败则回退本地最小集。
try:
    from aiweekly.insights import _PRIORITY_ALIASES as _PRIORITY_KW
except Exception:  # noqa: BLE001
    _PRIORITY_KW = {"牛来"}

logger = logging.getLogger("aiweekly.publish")


def _load(path: str | None) -> dict | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        logger.warning("输入文件不存在，跳过：%s", p)
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError) as e:
        logger.warning("读取失败 %s: %s", p, e)
        return None


def _safe_score(item: dict) -> float:
    """从新闻条目安全解析 score（脏数据如 "N/A"、"high" 兜底为 0，不崩）。"""
    try:
        return float(item.get("score") or 0)
    except (TypeError, ValueError):
        return 0.0


def build_report(
    news: dict | None,
    insights: dict | None,
    audience: dict | None,
    view_url: str | None,
    uid: str,
    top_n: int = 5,
) -> dict[str, Any]:
    """从结构化产物组装飞书卡片所需的 headline 载荷。"""
    news = news or {}
    insights = insights or {}

    # 头条：按 score 降序取前 top_n（脏数据由 _safe_score 兜底）
    items = news.get("items", []) or []
    ranked = sorted(items, key=_safe_score, reverse=True)
    headlines = []
    for it in ranked[:top_n]:
        score = _safe_score(it)
        headlines.append({
            "title": it.get("title", ""),
            "url": it.get("url", ""),
            "summary": it.get("summary", ""),
            "source": it.get("source", ""),
            "category": it.get("category", ""),
            "mustRead": bool(it.get("mustRead") or score >= 8),
        })

    ins_list = insights.get("insights", []) or []
    ins_cards = [
        {"kicker": i.get("kicker", ""), "title": i.get("title", ""), "insight": i.get("insight", "")}
        for i in ins_list[:3]
    ]

    # 受众摘要：audience_json 优先；否则 insights.audience_summary
    aud = audience if isinstance(audience, dict) else None
    if aud is None:
        aud = insights.get("audience_summary")
    if isinstance(aud, dict) and "audience_summary" in aud and len(aud) == 1:
        # 防止嵌套一层
        aud = aud["audience_summary"]
    if not isinstance(aud, dict):
        aud = {}

    # 关键词：保送集（牛来等）优先，再截断到 6 槽，确保高感知词不被吃掉
    raw_kws = [k for k in (insights.get("keywords", []) or []) if k.get("term")]
    raw_kws.sort(key=lambda k: (0 if k.get("term") in _PRIORITY_KW else 1,))
    kws = [
        {"term": k.get("term", ""), "tag": k.get("tag", "")}
        for k in raw_kws[:6]
    ]

    week = news.get("week") or insights.get("week") or "本周"
    lead = insights.get("lead", "")

    final_view = None
    if view_url:
        sep = "&" if "?" in view_url else "?"
        final_view = f"{view_url}{sep}src=feishu&uid={uid}"

    return {
        "week": week,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "lead": lead,
        "headlines": headlines,
        "insights": ins_cards,
        "audience": aud,
        "keywords": kws,
        "view_url": final_view,
        "view_label": "查看完整周报",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="组装本周头条 report.json 并推送飞书卡片（P0）")
    ap.add_argument("--platform", default="feishu", choices=["feishu"],
                    help="目标平台。**当前仅支持 feishu**；钉钉等通道尚未实现（见 CHN-1），"
                         "传入其他值会由 argparse 直接报错退出。本参数为未来多通道预留，"
                         "当前不构成能力开关")
    ap.add_argument("--news-json", required=True, help="news.json 路径")
    ap.add_argument("--insights-json", default=None,
                    help="insights.json 路径（可选；缺省时由本周新闻自动派生看点/关键词，"
                         "与 generate_site.py 行为一致——静态 insights.json 已废弃，勿再传入）")
    ap.add_argument("--audience-json", default=None, help="audience_summary.json（可选，缺省用 insights.audience_summary）")
    ap.add_argument("--report-json", default=None, help="直接复用已生成的 report.json（跳过组装）")
    ap.add_argument("--chat-id", default=None, help="飞书目标群 chat_id（oc_xxx）；优先于环境变量与 feishu_target.json")
    ap.add_argument("--user-id", default=None, help="飞书目标用户 open_id（ou_xxx），用于私聊")
    ap.add_argument("--as", dest="identity", default="bot", choices=["bot", "user"],
                    help="发送身份（默认 bot·应用机器人；user 为以本人身份私聊）")
    ap.add_argument("--view-url", default=None, help="完整周报托管链接（自动追加 ?src=feishu&uid=）")
    ap.add_argument("--uid", default="auto", help="度量 uid；'auto' 生成短 uuid")
    ap.add_argument("--output", default=None, help="report.json 写出路径（默认 news 同目录/report.json）")
    ap.add_argument("--top-n", type=int, default=5, help="头条条数（默认 5）")
    ap.add_argument("--dry-run", action="store_true", help="仅构造卡片并打印，不推送")
    ap.add_argument("--html", default=None, help="生成的周报 HTML 路径（配合 --deploy 部署）")
    ap.add_argument("--deploy", action="store_true",
                    help="生成 report.json 后顺便部署（默认后端 github-pages，需 --html）")
    ap.add_argument("--deploy-to", default="github-pages",
                    choices=["github-pages", "tencent-cos", "vercel", "netlify",
                             "cloudflare-pages", "local"],
                    help="部署后端（P0-1：去 GitHub 化；默认 github-pages，零破坏）。"
                         "非 github-pages 后端无需配置 GitHub。")
    ap.add_argument("--view-base", default=None,
                    help="周报公开基址（覆盖后端推导的 view_base，用于拼 view_url）")
    ap.add_argument("--no-push", action="store_true", help="部署时仅本地提交不推送（保留以兼容旧调用）")
    ap.add_argument("--push", action="store_true", help="部署时推送（默认不推送，仅本地生成+提交）")
    # 注：Pages 源切换（gh-pages/root）请直接用 `python scripts/deploy_ghpages.py --html <file> --switch-pages`。
    # 本脚本曾提供 --switch-pages 转发开关，但 deploy() 的 github-pages 分支并不消费该参数，
    # 传入后会被静默忽略——属于虚假承诺，故移除；需要切源请走上面的真实入口。
    args = ap.parse_args()

    uid = args.uid if args.uid != "auto" else uuid.uuid4().hex[:8]

    # 复用已生成的 report.json
    if args.report_json and Path(args.report_json).exists():
        report = json.load(open(args.report_json, encoding="utf-8"))
        print(f"♻️ 复用已有 report.json：{args.report_json}")
    else:
        news = _load(args.news_json)
        if not news:
            print("❌ 缺少 news.json，无法组装报告。")
            return 1
        # insights 缺省时由本周新闻自动派生（与 generate_site 一致）；派生失败则降级为空卡
        if args.insights_json:
            insights = _load(args.insights_json)
        else:
            insights = None
            try:
                from aiweekly import insights as INS
                items = news.get("items") or []
                auto_ins = INS._auto_insights(news, 6)
                insights = {
                    "insights": auto_ins,
                    "keywords": INS._auto_keywords(news, 8),
                    "lead": INS._auto_lead(items, len(items), auto_ins),
                    "audience_summary": INS._DEFAULT_AUDIENCE_SUMMARY,
                    "week": news.get("week"),
                }
            except Exception as e:  # noqa: BLE001  best-effort：派生异常则降级为空卡（仅头条）
                print(f"  ⚠️ 自动派生看点失败（降级为空卡）：{e}")
                insights = None
        audience = _load(args.audience_json)
        report = build_report(news, insights, audience, args.view_url, uid, top_n=args.top_n)

    out = args.output or str(Path(args.news_json).resolve().parent / "report.json")
    Path(out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ report.json 已写入：{out}")

    card = build_headline_card(report)
    print(f"📦 卡片段落数：{len(card['card']['elements'])} | "
          f"headlines={len(report['headlines'])} insights={len(report['insights'])} "
          f"audience={len(report['audience'])} keywords={len(report['keywords'])}")

    if args.dry_run:
        print("🛑 dry-run：不推送。卡片 JSON 预览（截断 2400 字）：")
        print(json.dumps(card, ensure_ascii=False, indent=2)[:2400])
        return 0

    rc = 0
    # 推送通道：飞书连接器（lark-cli）。目标解析优先级：CLI > 环境变量 > feishu_target.json
    flag, val = resolve_target(argparse.Namespace(chat_id=args.chat_id, user_id=args.user_id))
    if not flag:
        print("⚠️ 未配置飞书推送目标（--chat-id/--user-id / $FEISHU_CHAT_ID/$FEISHU_USER_ID / "
              "delivery/feishu_target.json 均空），跳过推送（报告已生成，不阻断）。")
    else:
        try:
            res = send_card(card["card"], flag, val, args.identity, dry_run=False)
            if res.stdout:
                sys.stdout.write(res.stdout)
            if res.stderr:
                sys.stderr.write(res.stderr)
            if res.returncode == 0:
                print("✅ 飞书连接器推送成功。")
            else:
                print(f"❌ 飞书连接器推送失败（returncode={res.returncode}）。")
                rc = 1
        except Exception as e:  # noqa: BLE001  传输层错误，best-effort 上报
            logger.warning("飞书连接器推送异常: %s", e)
            print(f"❌ 飞书连接器推送异常：{e}")
            rc = 1

    # 流水线最终分发步骤：按 --deploy-to 部署周报到公开托管（P0-1：多后端·去 GitHub 化）
    if args.deploy or args.deploy_to != "github-pages":
        if not args.html or not Path(args.html).exists():
            print("⚠️ 部署需要有效的 --html 路径，跳过部署。")
        else:
            backend = args.deploy_to if args.deploy else "github-pages"
            print(f"🌐 部署周报到 {backend}…")
            try:
                sys.path.insert(0, str(REPO_ROOT / "scripts"))
                from deploy import deploy as dispatch_deploy  # noqa: E402
                dep = dispatch_deploy(
                    args.html, backend=backend, view_base=args.view_base,
                    no_push=not args.push, dry_run=args.dry_run,
                )
                # 用后端返回的 view_base 补上 view_url（若本次未显式给 --view-url）
                if not args.view_url and dep.get("view_base") and report.get("view_url") is None:
                    base = dep["view_base"].rstrip("/")
                    html_name = Path(args.html).name
                    report["view_url"] = f"{base}/{html_name}?src=feishu&uid={uid}"
                    report["view_label"] = "查看完整周报"
                    # 回写 report.json，使飞书卡片指向正确链接
                    Path(out).write_text(
                        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
                    )
                    print(f"🔗 周报链接已写入 view_url：{report['view_url']}")
                elif not args.view_url and not dep.get("view_base"):
                    print("⚠️ 部署后端未返回公开基址，飞书卡片将不含「查看完整周报」链接"
                          "（可在部署配置里设置 view_base / COS_BASE_URL 等）。")
            except Exception as exc:  # noqa: BLE001  部署为 best-effort：失败不回滚已生成的报告，仅告警并记录
                logger.warning("部署异常: %s", exc)
                print(f"❌ 部署异常：{exc}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
