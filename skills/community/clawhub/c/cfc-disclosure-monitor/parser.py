#!/usr/bin/env python3
"""
parser.py — Phase 4: 消金公告结构化解析引擎
═══════════════════════════════════════════════════════════════
从非结构化公告文本（fulltext.txt）中提取结构化字段。

依赖：
    pip install httpx anthropic  # LLM 调用（可选）

用法：
    python3 parser.py --company "蚂蚁消费金融" --date 2026-04-11
    python3 parser.py --company "中银消费金融" --parse-all
    python3 parser.py --batch  # 批量处理所有公司

LLM 模式（需要有效 API key）：
    MINIMAX_API_KEY=xxx python3 parser.py --llm --company "蚂蚁消费金融"

降级策略：
    1. LLM 可用 → MiniMax/GLM API 结构化提取
    2. LLM 不可用 → 规则+正则提取（标题/日期已有，补充公司/分类/监管文件识别）
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# ── 路径设置 ─────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
ROOT_DIR = SKILL_DIR.parent.parent / "cfc_raw_data"
TODAY_STR = str(date.today())

# ── API 配置 ─────────────────────────────────────────────────────────────────
# MiniMax coding plan key（VLM，不支持text模型，仅限特定端点）
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"
# z.ai GLM API key（支持 glm-4v-flash 视觉理解）
GLM_API_KEY = os.getenv("GLM_API_KEY", "c132c9e7f2a94c25abece42d428da8e3.oFfGIlhetyLiS0E0")
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GLM_MODEL = "glm-4v-flash"   # 支持文本+图像的结构化提取

# ── Schema 定义 ──────────────────────────────────────────────────────────────
CATEGORIES = [
    "关联交易", "资本信息", "合作机构", "社会责任",
    "年度信披", "服务价格", "债权转让", "消费者保护", "营业执照", "重要公告",
]

SENTIMENT_OPTIONS = ["positive", "neutral", "negative"]
IMPORTANCE_OPTIONS = ["high", "medium", "low"]

# 监管文件特征词（用于无 LLM 时的规则匹配）
REGULATION_PATTERNS = [
    (r"《消费金融公司消保管理办法》", "消费金融公司消保管理办法"),
    (r"《消费金融公司管理办法》", "消费金融公司管理办法"),
    (r"《商业银行互联网贷款管理暂行办法》", "商业银行互联网贷款管理暂行办法"),
    (r"《网络小额贷款业务管理暂行办法》", "网络小额贷款业务管理暂行办法"),
    (r"《个人信息保护法》", "个人信息保护法"),
    (r"《征信业务管理办法》", "征信业务管理办法"),
    (r"《银行业消费者权益保护工作指引》", "银行业消费者权益保护工作指引"),
    (r"《关于加强金融消费者权益保护工作的指导意见》", "关于加强金融消费者权益保护工作的指导意见"),
    (r"《消费金融公司信息披露监管评价办法》", "消费金融公司信息披露监管评价办法"),
    (r"《消费金融公司非现场监管报表指标与填报规则》", "消费金融公司非现场监管报表指标与填报规则"),
    (r"《银行保险机构消费者权益保护管理办法》", "银行保险机构消费者权益保护管理办法"),
    (r"《金融消费者权益保护实施办法》", "金融消费者权益保护实施办法"),
    (r"《商业银行信息科技风险管理指引》", "商业银行信息科技风险管理指引"),
    (r"《银行业金融机构数据治理指引》", "银行业金融机构数据治理指引"),
    (r"《金融稳定报告》", "金融稳定报告"),
    (r"《资本管理办法》", "资本管理办法"),
    (r"《关联交易管理办法》", "关联交易管理办法"),
    (r"《不良资产处置管理办法》", "不良资产处置管理办法"),
    (r"《消费者投诉处理管理办法》", "消费者投诉处理管理办法"),
    (r"《互联网贷款管理办法》", "互联网贷款管理办法"),
]

# 公司名称候选（用于识别 related_companies）
KNOWN_CFC_COMPANIES = [
    "蚂蚁消费金融", "中银消费金融", "中原消费金融", "中邮消费金融",
    "兴业消费金融", "北银消费金融", "南银法巴消费金融", "哈银消费金融",
    "天津京东消费金融", "宁银消费金融", "小米消费金融", "尚诚消费金融",
    "平安消费金融", "建信消费金融", "招联消费金融", "晋商消费金融",
    "杭银消费金融", "河北幸福消费金融", "海尔消费金融", "盛银消费金融",
    "蒙商消费金融", "苏银凯基消费金融", "长银五八消费金融", "中金百利消费金融",
    "湖北消费金融", "陕西长银消费金融", "吉林亿联消费金融", "内蒙古蒙商消费金融",
    "四川锦程消费金融", "福建海联消费金融",
]


# ─────────────────────────────────────────────────────────────────────────────
#  LLM API 调用
# ─────────────────────────────────────────────────────────────────────────────

def _call_llm(prompt: str, system: str = "", model: str = "auto",
              max_tokens: int = 1024, temperature: float = 0.1,
              image_base64: str = None) -> Optional[str]:
    """
    调用 GLM-4V-flash（优先）→ GLM-4-flash → 返回 None
    image_base64: 可选，传入 Base64 图像启用 VLM 模式
    """
    import httpx

    # 构建消息
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    
    if image_base64:
        content_parts = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            {"type": "text", "text": prompt},
        ]
    else:
        content_parts = prompt

    messages.append({"role": "user", "content": content_parts})

    # ── 优先：GLM-4V-flash（视觉+文本结构化提取） ─────────────────────────
    if image_base64:
        try:
            resp = httpx.post(
                GLM_API_URL,
                headers={"Authorization": f"Bearer {GLM_API_KEY}", "Content-Type": "application/json"},
                json={"model": "glm-4v-flash", "messages": messages, "max_tokens": max_tokens},
                timeout=30.0,
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("choices"):
                return data["choices"][0]["message"]["content"]
            print(f"    ⚠️ GLM-4V-flash(image): {data.get('error', data.get('message', ''))}", file=sys.stderr)
        except Exception as e:
            print(f"    ⚠️ GLM-4V-flash(image) 请求异常: {e}", file=sys.stderr)

    # ── GLM-4-flash（纯文本） ──────────────────────────────────────────────
    for glm_model in ["glm-4-flash", "glm-4v-flash"]:
        try:
            resp = httpx.post(
                GLM_API_URL,
                headers={"Authorization": f"Bearer {GLM_API_KEY}", "Content-Type": "application/json"},
                json={"model": glm_model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature},
                timeout=30.0,
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("choices"):
                return data["choices"][0]["message"]["content"]
            err = data.get("error", {})
            if isinstance(err, dict):
                print(f"    ⚠️ {glm_model}: {err.get('message', err)}", file=sys.stderr)
        except Exception as e:
            print(f"    ⚠️ {glm_model} 请求异常: {e}", file=sys.stderr)
            continue

    return None


# ─────────────────────────────────────────────────────────────────────────────
#  规则引擎（降级模式）
# ─────────────────────────────────────────────────────────────────────────────

def _extract_regulations(text: str) -> list[str]:
    """用正则识别监管文件名称"""
    found = []
    for pat, name in REGULATION_PATTERNS:
        if re.search(pat, text):
            found.append(name)
    # 去重
    seen = set()
    unique = []
    for f in found:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def _extract_dates(text: str) -> list[str]:
    """识别文中其他日期（除发布日期外）"""
    dates = []
    # YYYY年MM月DD日 / YYYY-MM-DD / YYYY/MM/DD
    for m in re.finditer(
        r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?)", text
    ):
        d = m.group(1).replace("年", "-").replace("月", "-").replace("日", "")
        dates.append(d)
    # 季报期间
    for m in re.finditer(r"(\d{4}年第[一二三四]季度)", text):
        dates.append(m.group(1))
    # 去重保持顺序
    seen, unique = set(), []
    for d in dates:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    return unique


def _extract_metrics(text: str) -> dict:
    """提取关键数据指标"""
    metrics = {}
    # 注册资本
    m = re.search(r"注册资本[为:：]?\s*([\d亿万千百]+[亿元]?)", text)
    if m:
        metrics["注册资本"] = m.group(1)
    # 不良率
    m = re.search(r"不良[贷款率]+[为:：]?\s*([\d.]+%)", text)
    if m:
        metrics["不良率"] = m.group(1)
    # 资本充足率
    m = re.search(r"资本充足率[为:：]?\s*([\d.]+%)", text)
    if m:
        metrics["资本充足率"] = m.group(1)
    # 拨备覆盖率
    m = re.search(r"拨备覆盖率[为:：]?\s*([\d.]+%)", text)
    if m:
        metrics["拨备覆盖率"] = m.group(1)
    # 资产规模
    m = re.search(r"(?:总资产|资产规模)[为:：]?\s*([\d.]+[万亿]?元?)", text)
    if m:
        metrics["资产规模"] = m.group(1)
    # 贷款余额
    m = re.search(r"贷款余额[为:：]?\s*([\d.]+[万亿]?元?)", text)
    if m:
        metrics["贷款余额"] = m.group(1)
    # 营收/利润
    m = re.search(r"营业收入[为:：]?\s*([\d.]+[亿元]?)", text)
    if m:
        metrics["营业收入"] = m.group(1)
    m = re.search(r"净利润[为:：]?\s*([\d.\-]+[亿元]?)", text)
    if m:
        metrics["净利润"] = m.group(1)
    # 关联交易金额
    m = re.search(r"关联交易[金额为:：]?\s*([\d.]+[亿元]?)", text)
    if m:
        metrics["关联交易金额"] = m.group(1)
    return metrics


def _extract_partners(text: str) -> list[str]:
    """提取合作机构（银行/信托/科技公司等）"""
    partners = []
    # 合作机构关键词
    patterns = [
        r"与\s+([^\s，,，]{2,20}(?:银行|信托|基金|科技|电商|支付|保险公司))\s+(?:合作|签署|开展)",
        r"合作伙伴[：:]\s*([^\n，,，]{2,30})",
        r"合作方[：:]\s*([^\n，,，]{2,30})",
        r"委托\s+([^\s，,，]{2,20}(?:催收|处置))",
        r"增信机构[：:]\s*([^\n，,，]{2,30})",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            partner = m.group(1).strip()
            if partner and 2 < len(partner) < 30:
                partners.append(partner)
    # 合作银行通用模式
    for m in re.finditer(r"([^\s，,，]{2,10}银行)\s*(?:总行|分行|支行|合作)", text):
        partners.append(m.group(1))
    # 去重
    seen, unique = set(), []
    for p in partners:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def _extract_related_companies(text: str, self_company: str) -> list[str]:
    """识别文中提及的其他消金公司"""
    related = []
    for name in KNOWN_CFC_COMPANIES:
        if name != self_company and name in text:
            related.append(name)
    return related


def _detect_sentiment(title: str, text: str, category: str) -> str:
    """规则判断舆情倾向"""
    combined = title + text
    negative_words = ["处罚", "整改", "违规", "投诉", "不良", "风险", "欺诈", "重大损失"]
    positive_words = ["合规", "达标", "增长", "盈利", "获奖", "创新", "合作", "拓展"]
    neg_count = sum(1 for w in negative_words if w in combined)
    pos_count = sum(1 for w in positive_words if w in combined)
    if neg_count > pos_count + 1:
        return "negative"
    elif pos_count > neg_count:
        return "positive"
    return "neutral"


def _detect_importance(title: str, text: str, category: str) -> str:
    """规则判断重要程度"""
    title_text = title + text
    high_indicators = ["重大", "重要", "核心", "变更", "转让", "处罚", "违规", "年度", "年报", "战略"]
    medium_indicators = ["关联", "资本", "风险", "合作", "信息披露"]
    if any(w in title_text for w in high_indicators):
        return "high"
    elif any(w in title_text for w in medium_indicators) or category in ["年度信披", "关联交易"]:
        return "medium"
    return "low"


def _rule_based_extract(text: str, meta: dict) -> dict:
    """纯规则提取（无 LLM 降级）"""
    company = meta.get("company", "")
    title = meta.get("title", "")
    ann_date = meta.get("date", "")
    category = meta.get("category", "重要公告")
    url = meta.get("url", "")

    regulations = _extract_regulations(text)
    dates_mentioned = _extract_dates(text)
    metrics = _extract_metrics(text)
    partners = _extract_partners(text)
    related_companies = _extract_related_companies(text, company)
    sentiment = _detect_sentiment(title, text, category)
    importance = _detect_importance(title, text, category)

    # 生成摘要
    summary = title[:100] if len(title) <= 100 else title[:97] + "..."
    if not text.startswith(title):
        snippet = text[:200].replace("\n", " ").strip()
        if snippet:
            summary = snippet[:100] + ("..." if len(snippet) > 100 else "")

    # 生成高亮（最多3条）
    highlights = []
    if regulations:
        highlights.append(f"提及监管文件：{', '.join(regulations[:2])}")
    if metrics:
        metric_strs = [f"{k}:{v}" for k, v in list(metrics.items())[:3]]
        highlights.append(f"关键指标：{' '.join(metric_strs)}")
    if partners:
        highlights.append(f"合作机构：{', '.join(partners[:2])}")
    if not highlights:
        highlights.append(f"分类：{category}")

    return {
        "company": company,
        "title": title,
        "date": ann_date,
        "category": category,
        "content_type": meta.get("content_type", "unknown"),
        "url": url,
        "regulations": regulations,
        "metrics": metrics,
        "partners": partners,
        "dates_mentioned": dates_mentioned,
        "related_companies": related_companies,
        "summary": summary,
        "highlights": highlights[:5],
        "sentiment": sentiment,
        "importance": importance,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  LLM 提取模式
# ─────────────────────────────────────────────────────────────────────────────

LLM_SYSTEM_PROMPT = ('输出纯JSON，一行，无代码块，无注释。'
    '字段：{"company":"","title":"","date":"","category":"",'
    '"content_type":"","url":"","regulations":[],'
    '"metrics":{},"partners":[],'
    '"dates_mentioned":[],"related_companies":[],'
    '"summary":"","highlights":[],'
    '"sentiment":"","importance":""}。'
    '分类：关联交易/资本信息/合作机构/社会责任/年度信披/服务价格/债权转让/消费者保护/营业执照/重要公告。'
    'sentiment：positive=正面，neutral=中性，negative=负面。'
    'importance：high=重大，medium=一般，low=次要。')


LLM_USER_PROMPT_TEMPLATE = """请提取以下公告的结构化信息：

公司：{company}
标题：{title}
日期：{date}
分类：{category}
URL：{url}

正文内容：
{fulltext}
"""


def _llm_extract(text: str, meta: dict) -> Optional[dict]:
    """使用 LLM 提取，返回 None 表示 LLM 不可用"""
    prompt = LLM_USER_PROMPT_TEMPLATE.format(
        company=meta.get("company", ""),
        title=meta.get("title", ""),
        date=meta.get("date", ""),
        category=meta.get("category", ""),
        url=meta.get("url", ""),
        fulltext=text[:8000],   # 限制 token
    )

    # 用短prompt避免截断（正文截断到前3000字）
    short_text = text[:3000]
    user_prompt = (
        f"公司：{meta.get('company','')}。标题：{meta.get('title','')}。"
        f"分类：{meta.get('category','')}。日期：{meta.get('date','')}。"
        f"正文：{short_text}。只输出JSON，不要任何其他文字。"
    )
    response = _call_llm(user_prompt, system=LLM_SYSTEM_PROMPT, max_tokens=4096)
    if not response:
        return None

    # ── JSON 提取与修复 ─────────────────────────────────────────────────────
    def _extract_json(text: str) -> Optional[dict]:
        """从 LLM 响应中提取并解析 JSON（处理各种异常格式）"""
        text = text.strip()
        # 去掉 markdown 代码块
        text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s*```\s*$', '', text)
        # 去掉 // 注释
        text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)

        # 直接解析尝试
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 提取 { ... } 部分（处理响应以非JSON文本开头的情况）
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            text = m.group(0)

        # 去掉字段间的换行和多余空格（非字符串内容内部）
        fixed = []
        in_string = False
        escape = False
        for c in text:
            if c == '\\' and in_string:
                escape = True
                fixed.append(c)
                continue
            if c == '"' and not escape:
                in_string = not in_string
                fixed.append(c)
                escape = False
                continue
            if in_string:
                fixed.append(c)
                escape = False
                continue
            # 非字符串内
            if c in ' \t\r':
                continue  # 跳过空格/tab/CR
            if c == '\n':
                continue  # 跳过换行（字段分隔）
            fixed.append(c)
            escape = False

        text = ''.join(fixed).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        return None

    result = _extract_json(response)
    if result:
        for key in ["company", "title", "date", "url"]:
            if not result.get(key):
                result[key] = meta.get(key, "")
        if not result.get("category") and meta.get("category"):
            result["category"] = meta["category"]
        if not result.get("content_type"):
            result["content_type"] = meta.get("content_type", "unknown")
        return result

    print(f"    ⚠️ LLM JSON 解析失败（尝试所有修复方案）", file=sys.stderr)
    print(f"    原始响应（前200字）: {response[:200]}", file=sys.stderr)
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  核心 API
# ─────────────────────────────────────────────────────────────────────────────

def parse_announcement(text: str, meta: dict, use_llm: bool = True) -> dict:
    """
    解析单条公告，返回 AnnouncementSchema dict。

    Args:
        text: 公告全文（fulltext.txt 内容）
        meta:  元数据 dict，必须包含：company, title, date, url, category
        use_llm: 是否优先使用 LLM（失败后自动降级为规则）

    Returns:
        AnnouncementSchema dict
    """
    # 基础验证
    if not text or len(text.strip()) < 10:
        # 没有正文，降级为纯 meta
        return {
            "company": meta.get("company", ""),
            "title": meta.get("title", ""),
            "date": meta.get("date", ""),
            "category": meta.get("category", "重要公告"),
            "content_type": meta.get("content_type", "unknown"),
            "url": meta.get("url", ""),
            "regulations": [],
            "metrics": {},
            "partners": [],
            "dates_mentioned": [],
            "related_companies": [],
            "summary": meta.get("title", "")[:100],
            "highlights": [],
            "sentiment": "neutral",
            "importance": "low",
        }

    # LLM 模式
    if use_llm:
        result = _llm_extract(text, meta)
        if result:
            print(f"    ✅ LLM 解析成功: {result.get('title', '')[:50]}")
            return result

    # 降级为规则引擎
    print(f"    🔧 规则引擎解析: {meta.get('title', '')[:50]}")
    return _rule_based_extract(text, meta)


def parse_batch(announcements: list, company: str, use_llm: bool = True,
                delay: float = 1.0, dry_run: bool = False) -> list:
    """
    批量解析一组公告。

    Args:
        announcements: list[dict]，每条包含 text(可选) 和 meta
        company: 公司名称（用于日志）
        use_llm: 是否使用 LLM
        delay: 每条间隔秒数（避免 API 限流）
        dry_run: True=只打印不解析（用于测试）

    Returns:
        list[AnnouncementSchema]
    """
    results = []
    for i, item in enumerate(announcements):
        meta = item.get("meta", {})
        meta["company"] = meta.get("company") or company
        text = item.get("text", "")

        if dry_run:
            print(f"  [{i+1}/{len(announcements)}] DRY RUN: {meta.get('title','')[:60]}")
            continue

        print(f"  [{i+1}/{len(announcements)}] 解析中: {meta.get('title','')[:60]}")
        try:
            result = parse_announcement(text, meta, use_llm=use_llm)
            results.append(result)
        except Exception as e:
            print(f"    ❌ 解析异常: {e}", file=sys.stderr)
            # 降级返回最小结构
            results.append({
                "company": meta.get("company", company),
                "title": meta.get("title", ""),
                "date": meta.get("date", ""),
                "category": meta.get("category", "重要公告"),
                "content_type": meta.get("content_type", "unknown"),
                "url": meta.get("url", ""),
                "regulations": [],
                "metrics": {},
                "partners": [],
                "dates_mentioned": [],
                "related_companies": [],
                "summary": meta.get("title", "")[:100],
                "highlights": [],
                "sentiment": "neutral",
                "importance": "low",
            })

        if use_llm and i < len(announcements) - 1 and delay > 0:
            time.sleep(delay)

    return results


# ─────────────────────────────────────────────────────────────────────────────
#  文件系统交互
# ─────────────────────────────────────────────────────────────────────────────

def _find_content_dir(company: str, date_str: str = None) -> Optional[Path]:
    """查找 content 目录"""
    date_str = date_str or TODAY_STR
    base = ROOT_DIR / date_str / company / "content"
    if base.exists():
        return base
    # 尝试其他格式
    for d in (ROOT_DIR).glob(f"*/{company}/content"):
        return d
    for d in (ROOT_DIR).glob(f"*/{company}/content"):
        return d
    return None


def load_announcements(company: str, date_str: str = None) -> list:
    """加载 announcements.json"""
    date_str = date_str or TODAY_STR
    f = ROOT_DIR / date_str / company / "announcements.json"
    if not f.exists():
        print(f"❌ 文件不存在: {f}", file=sys.stderr)
        return []
    return json.loads(f.read_text(encoding="utf-8"))


def load_content(company: str, url: str, date_str: str = None) -> str:
    """加载 fulltext.txt"""
    content_dir = _find_content_dir(company, date_str)
    if not content_dir:
        return ""
    # 用 URL 的 hash 作为文件名
    url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
    fulltext_path = content_dir / url_hash / "fulltext.txt"
    if fulltext_path.exists():
        return fulltext_path.read_text(encoding="utf-8")
    # 尝试直接匹配
    for p in content_dir.glob("*/fulltext.txt"):
        try:
            ann = load_announcements(company, date_str)
            for a in ann:
                if a.get("url") == url:
                    return p.read_text(encoding="utf-8")
        except Exception:
            pass
    return ""


def save_parsed(company: str, parsed: list, date_str: str = None) -> Path:
    """保存解析结果"""
    date_str = date_str or TODAY_STR
    out_dir = SKILL_DIR / "parsed" / date_str / company
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "parsed.json"
    out_file.write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"💾 已保存: {out_file} ({len(parsed)} 条)")
    return out_file


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="消金公告结构化解析 — Phase 4")
    p.add_argument("--company", default=None, help="公司名称")
    p.add_argument("--date", default=None, help="采集日期（默认今天）")
    p.add_argument("--parse-all", action="store_true", help="解析该公司所有公告")
    p.add_argument("--batch", action="store_true", help="批量处理所有公司")
    p.add_argument("--llm", action="store_true", default=False,
                   help="强制使用 LLM 模式（默认自动降级）")
    p.add_argument("--no-llm", action="store_true", help="禁用 LLM，只用规则引擎")
    p.add_argument("--dry-run", action="store_true", help="只打印，不解析")
    p.add_argument("--limit", type=int, default=0, help="最多解析 N 条（0=全部）")
    p.add_argument("--delay", type=float, default=1.0, help="LLM 请求间隔（秒）")
    p.add_argument("--output", default=None, help="输出路径")
    return p.parse_args()


def main():
    args = parse_args()
    date_str = args.date or TODAY_STR

    if args.batch:
        # 批量处理所有公司
        date_dir = ROOT_DIR / date_str
        if not date_dir.exists():
            print(f"❌ 日期目录不存在: {date_dir}")
            sys.exit(1)
        companies = [d.name for d in date_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
        print(f"╔══ Batch: {len(companies)} 家公司 ══╗")
    elif args.company:
        companies = [args.company]
    else:
        print("❌ 请指定 --company 或 --batch")
        sys.exit(1)

    use_llm = not args.no_llm
    all_results = {}

    for company in companies:
        announcements_file = ROOT_DIR / date_str / company / "announcements.json"
        if not announcements_file.exists():
            print(f"⚠️ 跳过（无数据）: {company}")
            continue

        announcements = json.loads(announcements_file.read_text(encoding="utf-8"))
        if not announcements:
            print(f"⚠️ 跳过（空列表）: {company}")
            continue

        print(f"\n▶ {company} ({len(announcements)} 条公告)")

        items = []
        for ann in announcements:
            meta = {
                "company": company,
                "title": ann.get("title", ""),
                "date": ann.get("date", ""),
                "category": ann.get("category", "重要公告"),
                "url": ann.get("url", ""),
                "content_type": "unknown",
            }
            # 尝试加载正文
            text = load_content(company, ann.get("url", ""), date_str)
            items.append({"meta": meta, "text": text})

        # 限制条数
        if args.limit > 0:
            items = items[:args.limit]

        results = parse_batch(items, company, use_llm=use_llm,
                              delay=args.delay, dry_run=args.dry_run)
        all_results[company] = results

        if not args.dry_run and results:
            save_parsed(company, results, date_str)

    # 汇总
    total = sum(len(v) for v in all_results.values())
    print(f"\n✅ 完成：{total} 条公告解析完成，{len(all_results)} 家公司")

    if args.output and all_results:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"💾 汇总已保存: {out}")


if __name__ == "__main__":
    main()
