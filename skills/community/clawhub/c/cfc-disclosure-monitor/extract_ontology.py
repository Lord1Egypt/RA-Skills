#!/usr/bin/env python3
"""
extract_ontology.py — Phase 3: 消金信披知识图谱构建 v2
═══════════════════════════════════════════════════════════════════════
从807条有效公告中提取结构化实体和关系，构建知识图谱存入 SQLite。

实体类型：
  Company              消费金融公司（30家）
  Announcement         公告
  CooperationPartner   合作机构（助贷/导流）
  CollectionAgency     催收机构
  PaymentChannel      支付渠道（精确匹配）
  TechPartner          科技合作方
  Counterparty         关联交易对手
  RegulationRef        引用法规
  FinancialMetric     监管指标

关系类型：
  Company → ANNOUNCES → Announcement
  Company → HAS_PARTNER → CooperationPartner   (助贷合作)
  Company → HAS_COLLECTION_AGENCY → CollectionAgency  (催收合作)
  Company → SUPPORTS_PAYMENT → PaymentChannel (支付渠道)
  Company → TECH_PARTNERS → TechPartner       (科技合作)
  Company → HAS_COUNTERPARTY → Counterparty (关联交易对手)
  Company → CITES_REGULATION → RegulationRef (引用法规)
  Announcement → DISCLOSES_METRIC → FinancialMetric

用法：
  python3 extract_ontology.py --init          # 初始化数据库
  python3 extract_ontology.py --extract          # 全量提取
  python3 extract_ontology.py --stats            # 统计
  python3 extract_ontology.py --query "关键词"    # 查询
  python3 extract_ontology.py --export-json > ontology.json
"""

import argparse
import hashlib
import json
import re
import sqlite3
import time
from datetime import datetime
from pathlib import Path

# ── 路径配置 ────────────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent / "ontology.db"
ROOT_DIR = Path.home() / ".openclaw" / "workspace" / "cfc_raw_data"
CLEANED_DIR = ROOT_DIR / "cleaned_2026-04-14"

# ── Schema ─────────────────────────────────────────────────────────────────
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entities (
    id          TEXT PRIMARY KEY,
    type        TEXT NOT NULL,
    name        TEXT NOT NULL,
    props       TEXT DEFAULT '{}',
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);

CREATE TABLE IF NOT EXISTS relations (
    id              TEXT PRIMARY KEY,
    from_id         TEXT NOT NULL,
    to_id           TEXT NOT NULL,
    relation_type   TEXT NOT NULL,
    props           TEXT DEFAULT '{}',
    created_at      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_relations_from  ON relations(from_id);
CREATE INDEX IF NOT EXISTS idx_relations_to    ON relations(to_id);
CREATE INDEX IF NOT EXISTS idx_relations_type  ON relations(relation_type);
"""

# ── 关系类型 ────────────────────────────────────────────────────────────────
REL_ANNOUNCES              = "ANNOUNCES"
REL_HAS_PARTNER            = "HAS_PARTNER"
REL_HAS_COLLECTION_AGENCY  = "HAS_COLLECTION_AGENCY"
REL_SUPPORTS_PAYMENT       = "SUPPORTS_PAYMENT"
REL_TECH_PARTNERS          = "TECH_PARTNERS"
REL_HAS_COUNTERPARTY       = "HAS_COUNTERPARTY"
REL_CITES_REGULATION       = "CITES_REGULATION"
REL_DISCLOSES_METRIC       = "DISCLOSES_METRIC"

# ── 监管文件 ────────────────────────────────────────────────────────────────
REGULATION_PATTERNS = [
    (r"《消费金融公司消保管理办法》", "消费金融公司消保管理办法"),
    (r"《消费金融公司管理办法》", "消费金融公司管理办法"),
    (r"《商业银行互联网贷款管理暂行办法》", "商业银行互联网贷款管理暂行办法"),
    (r"《网络小额贷款业务管理暂行办法》", "网络小额贷款业务管理暂行办法"),
    (r"《个人信息保护法》", "个人信息保护法"),
    (r"《征信业务管理办法》", "征信业务管理办法"),
    (r"《银行保险机构消费者权益保护管理办法》", "银行保险机构消费者权益保护管理办法"),
    (r"《金融消费者权益保护实施办法》", "金融消费者权益保护实施办法"),
    (r"《商业银行信息科技风险管理指引》", "商业银行信息科技风险管理指引"),
    (r"《银行业金融机构数据治理指引》", "银行业金融机构数据治理指引"),
    (r"《资本管理办法》", "资本管理办法"),
    (r"《关联交易管理办法》", "关联交易管理办法"),
    (r"《不良资产处置管理办法》", "不良资产处置管理办法"),
    (r"《消费者投诉处理管理办法》", "消费者投诉处理管理办法"),
    (r"《银行保险机构关联交易管理办法》", "银行保险机构关联交易管理办法"),
    (r"《商业银行资本管理办法》", "商业银行资本管理办法"),
    (r"《刑法》", "刑法"),
    (r"《民法典》", "民法典"),
]

# ── 支付渠道（精确匹配，消除噪声）─────────────────────────────────────────
PAYMENT_KEYWORDS = [
    "微信支付","支付宝","云闪付","银联在线","网银支付","京东支付",
    "百度支付","美团支付","抖音支付","快手支付","拼多多支付","QQ支付",
    "翼支付","和包支付","拉卡拉","富友支付","连连支付","汇付天下",
    "宝付","易宝支付","银联云闪付","Apple Pay","华为支付","小米支付",
]

# ─────────────────────────────────────────────────────────────────────────────
# 表格公司名提取
# ─────────────────────────────────────────────────────────────────────────────

_SUFFIXES = [
    '股份有限公司','网络科技有限公司','信息科技有限公司','科技有限公司',
    '金融服务有限公司','信用管理有限公司','咨询有限公司','管理有限公司',
    '商务有限公司','网络有限公司','技术有限公司','集团有限公司',
    '有限责任公司','有限公司','科技公司','网络公司','集团','公司',
]

def _extract_table_spaced(text: str) -> list[str]:
    """有空格格式：序号 + 公司名 + 类型（阳光格式）"""
    results, seen = [], set()
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        m = re.match(r'^\s*(\d+)\s+', line)
        if not m: continue
        rest = line[m.end():].strip()
        name_end, matched = -1, ''
        for suf in _SUFFIXES:
            idx = rest.find(suf)
            if idx != -1 and idx + len(suf) > name_end:
                name_end, matched = idx + len(suf), suf
        if name_end > 0:
            name = rest[:name_end].strip()
            if name and len(name) >= 5 and name not in seen:
                seen.add(name)
                results.append(name)
    return results

def _extract_table_concat(text: str) -> list[str]:
    """无空格格式：数字+公司名+后缀+下一数字（蒙商格式）"""
    suffixes = ['有限公司','集团有限公司','有限责任公司']
    results, seen, i = [], set(), 0
    while i < len(text):
        m = re.match(r'(\d+)', text[i:])
        if not m: break
        i += m.end()
        best_end = -1
        for j in range(i, min(i + 120, len(text))):
            chunk = text[i:j+1]
            for suf in suffixes:
                if chunk.endswith(suf) and j+1 > best_end:
                    best_end = j + 1
            if best_end > 0 and j+1 < len(text) and text[j+1].isdigit():
                break
        if best_end > 0:
            name = text[i:best_end]
            i = best_end
        else:
            i += 1; continue
        if len(name) >= 4 and name not in seen:
            seen.add(name)
            results.append(name)
    # 处理尾部（最后一个序号后没有跟着数字）
    return results

# ─────────────────────────────────────────────────────────────────────────────
# 提取函数
# ─────────────────────────────────────────────────────────────────────────────

def _eid(etype: str, name: str) -> str:
    return hashlib.md5(f"{etype}:{name}".encode()).hexdigest()[:12]

def extract_regulations(text: str) -> list[str]:
    found = []
    for pat, name in REGULATION_PATTERNS:
        if re.search(pat, text):
            found.append(name)
    return list(dict.fromkeys(found))

def extract_partners(text: str, title: str) -> list[str]:
    """提取合作机构（助贷/导流）"""
    partners = []
    # 表格格式检测
    has_table = ('序号' in text and '合作机构' in text) or any(k in title for k in ['助贷业务合作机构','合作机构名单','合作名单'])
    if has_table:
        # 有空格优先
        spaced = _extract_table_spaced(text)
        if spaced:
            partners.extend(spaced)
        else:
            concat = _extract_table_concat(text)
            partners.extend(concat)
    # 通用兜底
    for pat in [
        r'合作方[：:]\s*([^\n，,。；:]{4,40})',
        r'合作机构[：:]\s*([^\n，,。；:]{4,40})',
    ]:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            if name and 4 <= len(name) <= 40 and name not in partners:
                partners.append(name)
    return partners

def extract_collection_agencies(text: str) -> list[str]:
    """提取催收机构"""
    agencies = []
    # 表格格式检测
    if any(k in text[:300] for k in ['催收机构名单','清收处置','委外催收','催收合作机构','逾期贷款','催收公司']):
        spaced = _extract_table_spaced(text)
        if spaced:
            agencies.extend(spaced)
        else:
            concat = _extract_table_concat(text)
            agencies.extend(concat)
    # 通用兜底
    for pat in [
        r'委托\s+([^\s，。、；：:]{4,30}(?:催收|处置|资产管理|律所|律师|事务所))',
        r'催收机构[：:]\s*([^\n，,。；]{2,40})',
        r'合作催收[：:]\s*([^\n，,。；]{2,40})',
    ]:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            if name and 4 <= len(name) <= 40 and name not in agencies:
                agencies.append(name)
    return agencies

def extract_payment_channels(text: str) -> list[str]:
    """提取支付渠道（精确匹配）"""
    channels = []
    for kw in PAYMENT_KEYWORDS:
        if kw in text and kw not in channels:
            channels.append(kw)
    return channels

def extract_tech_partners(text: str) -> list[str]:
    """提取科技合作方"""
    partners = []
    for pat in [
        r'与\s+([^\s，。、；：:]{2,20}(?:科技|技术|智能|数据|信息))\s+(?:合作|签署|开展)',
        r'科技合作[：:]\s*([^\n，,。；]{2,40})',
        r'技术服务[：:]\s*([^\n，,。；]{2,40})',
    ]:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            if name and 4 <= len(name) <= 30 and name not in partners:
                partners.append(name)
    return partners

def extract_counterparties(text: str, company: str) -> list[str]:
    """提取关联交易对手"""
    counterparties = []
    for m in re.finditer(r'交易对手[：:]\s*([^\n，,。；:]{2,40})', text):
        name = m.group(1).strip()
        if name and len(name) >= 4:
            counterparties.append(name)
    # 识别"XXX有限公司"类关联方
    for m in re.finditer(r'([^\s，。、；：:]{5,30}有限公司)\s*(?:为|系|属于|是)', text):
        name = m.group(1).strip()
        if name and name != company and '消费金融' not in name and name not in counterparties:
            counterparties.append(name)
    return counterparties

def extract_metrics(text: str) -> dict:
    """提取监管指标"""
    metrics = {}
    for pat, label in [
        (r"核心一级资本净额[为:：]?\s*([\d，,.]+\s*万?元?)", "核心一级资本净额"),
        (r"一级资本净额[为:：]?\s*([\d，,.]+\s*万?元?)", "一级资本净额"),
        (r"资本净额[为:：]?\s*([\d，,.]+\s*万?元?)", "资本净额"),
        (r"核心一级资本充足率[为:：]?\s*([\d.]+%)", "核心一级资本充足率"),
        (r"一级资本充足率[为:：]?\s*([\d.]+%)", "一级资本充足率"),
        (r"资本充足率[为:：]?\s*([\d.]+%)", "资本充足率"),
        (r"不良率[为:：]?\s*([\d.]+%)", "不良率"),
        (r"不良贷款率[为:：]?\s*([\d.]+%)", "不良贷款率"),
        (r"拨备覆盖率[为:：]?\s*([\d.]+%)", "拨备覆盖率"),
        (r"注册资本[为:：]?\s*([\d，,.]+\s*亿?万?元?)", "注册资本"),
        (r"总资产[为:：]?\s*([\d，,.]+\s*亿?万?元?)", "总资产"),
        (r"贷款余额[为:：]?\s*([\d，,.]+\s*亿?万?元?)", "贷款余额"),
    ]:
        m = re.search(pat, text)
        if m:
            metrics[label] = m.group(1).strip()
    return metrics

# ─────────────────────────────────────────────────────────────────────────────
# 数据库操作
# ─────────────────────────────────────────────────────────────────────────────

def _conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as c:
        c.executescript(SCHEMA_SQL)
    print(f"数据库已初始化: {DB_PATH}")

def upsert_entity(eid: str, etype: str, name: str, props: dict = None):
    conn = _conn()
    now = datetime.now().isoformat()
    props = props or {}
    conn.execute(
        "INSERT OR REPLACE INTO entities (id,type,name,props,created_at) VALUES (?,?,?,?,COALESCE((SELECT created_at FROM entities WHERE id=?),?))",
        (eid, etype, name, json.dumps(props, ensure_ascii=False), eid, now)
    )
    conn.commit()
    conn.close()

def upsert_relation(rid: str, from_id: str, to_id: str, rel_type: str, props: dict = None):
    conn = _conn()
    now = datetime.now().isoformat()
    props = props or {}
    conn.execute(
        "INSERT OR REPLACE INTO relations (id,from_id,to_id,relation_type,props,created_at) VALUES (?,?,?,?,?,COALESCE((SELECT created_at FROM relations WHERE id=?),?))",
        (rid, from_id, to_id, rel_type, json.dumps(props, ensure_ascii=False), rid, now)
    )
    conn.commit()
    conn.close()

def get_or_create_company(company: str) -> str:
    cid = _eid("Company", company)
    upsert_entity(cid, "Company", company)
    return cid

# ─────────────────────────────────────────────────────────────────────────────
# 数据加载
# ─────────────────────────────────────────────────────────────────────────────

def load_announcements():
    """直接从raw data扫描，不依赖valid_announcements.json"""
    announcements = []

    for date_dir in ["2026-04-14"]:
        dp = ROOT_DIR / date_dir
        if not dp.exists(): continue
        for co_dir in sorted(dp.glob("*/")):
            ann_file = co_dir / "announcements.json"
            if not ann_file.exists(): continue
            try:
                anns = json.loads(ann_file.read_text(encoding="utf-8"))
            except:
                continue

            for ann in anns:
                aid = ann.get("_content_id", "")
                url = ann.get("url", "")
                title = ann.get("title", "")[:200]
                ann_date = ann.get("date", "")
                category = ann.get("category", "重要公告")

                # 找fulltext
                ft_text = ""
                for ft_name in ["fulltext.txt", ".pdf_text.txt"]:
                    fp = co_dir / aid / ft_name
                    if fp.exists():
                        try:
                            ft_text = fp.read_text(encoding="utf-8", errors="replace")
                        except:
                            pass
                        break

                if not ft_text or len(ft_text.strip()) < 50:
                    continue

                announcements.append({
                    "company": co_dir.name,
                    "title": title,
                    "date": ann_date,
                    "url": url,
                    "category": category,
                    "text": ft_text,
                    "source_date": date_dir,
                    "score": 3,
                })

    print(f"  直接扫描加载 {len(announcements)} 条公告")
    return announcements

# ─────────────────────────────────────────────────────────────────────────────
# 全量提取
# ─────────────────────────────────────────────────────────────────────────────

def extract_all():
    announcements = load_announcements()
    if not announcements:
        return

    # 注册所有公司实体
    companies_seen = set()
    for ann in announcements:
        co = ann['company']
        if co not in companies_seen:
            get_or_create_company(co)
            companies_seen.add(co)
    print(f"注册 {len(companies_seen)} 家公司实体")

    stats = {k: 0 for k in ['ann','partners','agencies','channels','techs','counterparties','regs','metrics']}

    for i, ann in enumerate(announcements):
        company = ann['company']
        title = ann.get('title', '')[:200]
        ann_date = ann.get('date', '')
        category = ann.get('category', '重要公告')
        text = ann.get('text', '')
        url = ann.get('url', '')
        score = ann.get('score', 3)
        source_date = ann.get('source_date', '')

        if not text or len(text.strip()) < 50:
            continue

        if (i + 1) % 50 == 0:
            print(f"\n[{i+1}/{len(announcements)}] ...")

        # Announcement 实体
        ann_eid = _eid("Announcement", f"{company}:{url or title}")
        upsert_entity(ann_eid, "Announcement", title[:60], {
            "date": ann_date, "category": category, "url": url,
            "score": score, "source_date": source_date,
        })

        # 发布关系
        co_eid = _eid("Company", company)
        rid = _eid("Rel", f"{co_eid}:{REL_ANNOUNCES}:{ann_eid}")
        upsert_relation(rid, co_eid, ann_eid, REL_ANNOUNCES)
        stats['ann'] += 1

        # 合作机构
        partners = extract_partners(text, title)
        for p in partners:
            p_eid = _eid("CooperationPartner", p)
            upsert_entity(p_eid, "CooperationPartner", p, {"source": company})
            rid = _eid("Rel", f"{co_eid}:{REL_HAS_PARTNER}:{p_eid}")
            upsert_relation(rid, co_eid, p_eid, REL_HAS_PARTNER)
            stats['partners'] += 1
            if stats['partners'] <= 5:
                print(f"    🤝 合作机构: {p}")

        # 催收机构
        agencies = extract_collection_agencies(text)
        for a in agencies:
            a_eid = _eid("CollectionAgency", a)
            upsert_entity(a_eid, "CollectionAgency", a, {"source": company})
            rid = _eid("Rel", f"{co_eid}:{REL_HAS_COLLECTION_AGENCY}:{a_eid}")
            upsert_relation(rid, co_eid, a_eid, REL_HAS_COLLECTION_AGENCY)
            stats['agencies'] += 1
            if stats['agencies'] <= 3:
                print(f"    ⚠️ 催收机构: {a}")

        # 支付渠道
        channels = extract_payment_channels(text)
        for c in channels:
            c_eid = _eid("PaymentChannel", c)
            upsert_entity(c_eid, "PaymentChannel", c, {"source": company})
            rid = _eid("Rel", f"{co_eid}:{REL_SUPPORTS_PAYMENT}:{c_eid}")
            upsert_relation(rid, co_eid, c_eid, REL_SUPPORTS_PAYMENT)
            stats['channels'] += 1

        # 科技合作
        techs = extract_tech_partners(text)
        for t in techs:
            t_eid = _eid("TechPartner", t)
            upsert_entity(t_eid, "TechPartner", t, {"source": company})
            rid = _eid("Rel", f"{co_eid}:{REL_TECH_PARTNERS}:{t_eid}")
            upsert_relation(rid, co_eid, t_eid, REL_TECH_PARTNERS)
            stats['techs'] += 1

        # 交易对手
        cps = extract_counterparties(text, company)
        for cp in cps:
            cp_eid = _eid("Counterparty", cp)
            upsert_entity(cp_eid, "Counterparty", cp, {"source": company})
            rid = _eid("Rel", f"{co_eid}:{REL_HAS_COUNTERPARTY}:{cp_eid}")
            upsert_relation(rid, co_eid, cp_eid, REL_HAS_COUNTERPARTY)
            stats['counterparties'] += 1

        # 监管文件
        regs = extract_regulations(text)
        for r in regs:
            r_eid = _eid("RegulationRef", r)
            upsert_entity(r_eid, "RegulationRef", r)
            rid = _eid("Rel", f"{co_eid}:{REL_CITES_REGULATION}:{r_eid}")
            upsert_relation(rid, co_eid, r_eid, REL_CITES_REGULATION)
            stats['regs'] += 1

        # 监管指标
        metrics = extract_metrics(text)
        for mk, mv in metrics.items():
            m_eid = _eid("FinancialMetric", f"{company}:{ann_date}:{mk}")
            upsert_entity(m_eid, "FinancialMetric", f"{mk}={mv}", {"value": mv, "date": ann_date, "source": company, "metric_type": mk})
            rid = _eid("Rel", f"{ann_eid}:{REL_DISCLOSES_METRIC}:{m_eid}")
            upsert_relation(rid, ann_eid, m_eid, REL_DISCLOSES_METRIC)
            stats['metrics'] += 1

    print(f"\n{'='*50}")
    print(f"提取完成！")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"数据库: {DB_PATH}")

# ─────────────────────────────────────────────────────────────────────────────
# 查询与统计
# ─────────────────────────────────────────────────────────────────────────────

def stats():
    conn = _conn()
    print(f"\n{'='*50}")
    print(f"知识图谱统计 — {DB_PATH}")
    print(f"{'='*50}")

    print(f"\n实体统计:")
    for r in conn.execute("SELECT type, COUNT(*) FROM entities GROUP BY type ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]:<28} {r[1]:>5}")

    total_e = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    print(f"  {'合计':<28} {total_e:>5}")

    print(f"\n关系统计:")
    for r in conn.execute("SELECT relation_type, COUNT(*) FROM relations GROUP BY relation_type ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]:<30} {r[1]:>5}")

    total_r = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
    print(f"  {'合计':<30} {total_r:>5}")
    conn.close()

def query(keyword: str):
    conn = _conn()
    print(f"\n查询: {keyword}")
    print(f"{'='*50}")

    rows = conn.execute(
        "SELECT id, type, name FROM entities WHERE name LIKE ? LIMIT 10",
        (f"%{keyword}%",)
    ).fetchall()
    print(f"找到 {len(rows)} 个实体:\n")
    for eid, etype, name in rows:
        print(f"  [{etype}] {name}")

    if not rows: return

    for eid, etype, name in rows[:5]:
        print(f"\n  — {name} 的关系 —")
        rels = conn.execute("""
            SELECT r.relation_type, e.type, e.name, r.props FROM relations r
            JOIN entities e ON r.to_id=e.id WHERE r.from_id=?
            UNION ALL
            SELECT r.relation_type, e.type, e.name, r.props FROM relations r
            JOIN entities e ON r.from_id=e.id WHERE r.to_id=?
            LIMIT 10
        """, (eid, eid)).fetchall()
        for rel, to_type, to_name, props in rels:
            pd = json.loads(props or '{}')
            extra = f" ({pd.get('value','')})" if 'value' in pd else ''
            print(f"    {rel} → [{to_type}] {to_name}{extra}")
    conn.close()

def export_json():
    conn = _conn()
    entities = [dict(zip(['id','type','name','props','created_at'], r))
                for r in conn.execute("SELECT * FROM entities").fetchall()]
    relations = [dict(zip(['id','from_id','to_id','relation_type','props','created_at'], r))
                 for r in conn.execute("SELECT * FROM relations").fetchall()]
    conn.close()
    print(json.dumps({
        "entities": entities, "relations": relations,
        "exported_at": datetime.now().isoformat()
    }, ensure_ascii=False, indent=2))

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--init', action='store_true')
    ap.add_argument('--extract', action='store_true')
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--query', type=str)
    ap.add_argument('--export-json', action='store_true')
    args = ap.parse_args()

    if args.init:
        init_db()
    elif args.extract:
        init_db()
        extract_all()
    elif args.stats:
        stats()
    elif args.query:
        query(args.query)
    elif args.export_json:
        export_json()
    else:
        ap.print_help()
