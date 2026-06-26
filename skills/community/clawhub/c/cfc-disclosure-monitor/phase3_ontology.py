"""
Phase 3: 知识图谱构建
从 cfc_raw_data/{company}/ 读取结构化披露数据 → 写入 ontology graph.jsonl

支持实体类型:
  - Company (公司/机构)
  - DisclosureList (披露清单)
  - DisclosureDocument (具体披露文档)

用法:
  python3 phase3_ontology.py              # 处理所有公司
  python3 phase3_ontology.py 中邮消费金融  # 只处理指定公司
"""
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path

# ontology graph.jsonl 路径
# __file__ = .../workspace/skills/cfc-disclosure-monitor/phase3_ontology.py
# parent.parent = .../workspace/skills/  → parent.parent.parent = .../workspace/
ONTOLOGY_FILE = Path(__file__).parent.parent.parent / "memory" / "ontology" / "graph.jsonl"
RAW_DIR = Path(__file__).parent.parent.parent / "cfc_raw_data"

def ts() -> str:
    """当前 UTC+8 时间，ISO 格式。"""
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

DISCLOSURE_TYPE_MAP = {
    "催收合作机构": "CollectionAgency",
    "互联网贷款增信服务机构": "GuaranteeAgency",
    "互联网贷款平台运营机构": "PlatformOperator",
    "关联交易": "RelatedTransaction",
    "消费者保护": "ConsumerProtection",
    "重要公告": "ImportantAnnouncement",
    "不良资产转让": "NPLTransfer",
    "合作机构": "CooperationAgency",
}

COMPANY_TYPE_MAP = {
    "律师事务所": "LawFirm",
    "法律顾问": "LawFirm",
    "法律咨询": "LawFirm",
    "融资担保": "GuaranteeCompany",
    "担保公司": "GuaranteeCompany",
    "信息技术": "TechCompany",
    "数据科技": "TechCompany",
    "网络科技": "TechCompany",
    "软件": "TechCompany",
    "信用管理": "CollectionBPO",
    "服务外包": "CollectionBPO",
    "企业管理": "CollectionBPO",
    "资产管理": "CollectionBPO",
    "商务咨询": "CollectionBPO",
    "商务信息": "CollectionBPO",
    "消费金融": "FinancialInstitution",
    "银行": "FinancialInstitution",
    "小额贷款": "FinancialInstitution",
}


def safe_id(prefix: str, name: str) -> str:
    h = hashlib.md5(name.encode()).hexdigest()[:10]
    return f"{prefix}_{h}"


def classify_company(name: str) -> str:
    for kw, ctype in COMPANY_TYPE_MAP.items():
        if kw in name:
            return ctype
    return "Unknown"


# 消金公司全称→简称映射（统一 ID 生成）
CFC_SHORT_NAMES = {
    "中邮消费金融有限公司": "中邮消费金融",
    "浙江宁银消费金融股份有限公司": "宁银消费金融",
    "北京阳光消费金融股份有限公司": "阳光消费金融",
    "小米消费金融有限公司": "小米消费金融",
    "尚诚消费金融有限公司": "尚诚消费金融",
    "北银消费金融有限公司": "北银消费金融",
    "南银法巴消费金融有限公司": "南银法巴消费金融",
    "哈银消费金融有限责任公司": "哈银消费金融",
    "天津京东消费金融有限公司": "天津京东消费金融",
    "平安消费金融有限公司": "平安消费金融",
    "建信消费金融有限责任公司": "建信消费金融",
    "招联消费金融有限公司": "招联消费金融",
    "晋商消费金融股份有限公司": "晋商消费金融",
    "杭银消费金融有限责任公司": "杭银消费金融",
    "河北幸福消费金融股份有限公司": "河北幸福消费金融",
    "海尔消费金融有限公司": "海尔消费金融",
    "湖北消费金融股份有限公司": "湖北消费金融",
    "盛银消费金融有限公司": "盛银消费金融",
    "苏银凯基消费金融有限公司": "苏银凯基消费金融",
    "蒙商消费金融有限公司": "蒙商消费金融",
    "蚂蚁消费金融有限公司": "蚂蚁消费金融",
    "厦门金美信消费金融有限责任公司": "金美信消费金融",
    "锦程消费金融有限公司": "锦程消费金融",
    "长银五八消费金融有限公司": "长银五八消费金融",
    "陕西长银消费金融有限责任公司": "陕西长银消费金融",
    "马上消费金融股份有限公司": "马上消费金融",
    "中原消费金融股份有限公司": "中原消费金融",
    "中银消费金融有限公司": "中银消费金融",
    "中信消费金融有限公司": "中信消费金融",
    "兴业消费金融股份有限公司": "兴业消费金融",
}


def normalize_company(name: str) -> str:
    """将消金公司全称映射为简称，用于统一 ID 生成。"""
    return CFC_SHORT_NAMES.get(name, name)

def canonical_name(name: str) -> str:
    """返回规范化的公司名（全称→简称，非消金→原名）。"""
    return normalize_company(name)

def cfc_company_id(company: str) -> str:
    """
    返回消金公司的稳定 entity ID。
    基于简称生成，保证 announcements 和 structured JSON 用同一个 ID。
    """
    return safe_id("co", normalize_company(company))


def extract_company_names(text: str) -> list[str]:
    if not text:
        return []
    pattern = r'([\u4e00-\u9fa5]{4,20}(?:有限公司|股份有限公司|有限责任公司|集团|事务所|中心))'
    return list(dict.fromkeys(re.findall(pattern, text)))


def create_company(name: str, source: str, dtype: str, phone: str = "",
                     collected_at: str = "") -> dict:
    # 消金公司全称 → 用简称生成稳定 ID，解决 announcements 和 structured JSON ID 不一致问题
    norm_name = normalize_company(name)
    cid = safe_id("co", norm_name)
    co_type = classify_company(name)
    props = {
        "name": name,  # 保留原始名称（可能有全称）
        "source_company": source,
        "disclosure_type": dtype,
        "company_type": co_type,
    }
    if phone:
        props["phone"] = phone
    if collected_at:
        props["collected_at"] = collected_at
    return {"op": "create", "entity": {"id": cid, "type": "Company", "properties": props}}


def create_disclosure_list(company: str, dtype: str, count: int, date: str,
                             source_url: str = "", collected_at: str = "") -> dict:
    lid = safe_id("dl", f"{company}_{dtype}_{date}")
    props = {
        "name": f"{company}_{dtype}_{date}",
        "company": company,
        "disclosure_type": dtype,
        "count": count,
        "date": date,
    }
    if source_url:
        props["source_url"] = source_url
    if collected_at:
        props["collected_at"] = collected_at
    return {"op": "create", "entity": {"id": lid, "type": "DisclosureList", "properties": props}}


def create_relation(from_id: str, rel: str, to_id: str, props: dict = None) -> dict:
    r = {"op": "relate", "from": from_id, "rel": rel, "to": to_id}
    if props:
        r["properties"] = props
    return r


def detect_disclosure_type(title: str, category: str) -> str:
    for dtype in DISCLOSURE_TYPE_MAP:
        if dtype in title:
            return dtype
    return category if category else "Unknown"


def inject_ts(entries: list[dict], inserted_at: str) -> list[dict]:
    """给所有 entry 注入 inserted_at 时间戳。"""
    result = []
    for e in entries:
        e = dict(e)  # shallow copy
        if e.get("op") == "create":
            e["entity"] = dict(e["entity"])
            e["entity"]["properties"] = dict(e["entity"].get("properties", {}))
            e["entity"]["properties"]["inserted_at"] = inserted_at
        elif e.get("op") == "relate":
            e["properties"] = dict(e.get("properties", {}))
            e["properties"]["inserted_at"] = inserted_at
        result.append(e)
    return result


def process_collection_file(fpath: Path, company: str, inserted_at: str) -> list[dict]:
    """处理结构化的合作机构 JSON 文件（如 催收2026.json）。"""
    entries = []
    fname = fpath.name

    if "催收" in fname:
        dtype = "催收合作机构"
    elif "增信" in fname or "担保" in fname:
        dtype = "互联网贷款增信服务机构"
    elif "平台" in fname or "运营" in fname:
        dtype = "互联网贷款平台运营机构"
    else:
        dtype = "合作机构"

    # 文件修改时间作为数据采集时间
    mtime = datetime.fromtimestamp(fpath.stat().st_mtime).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

    date_match = re.search(r'20\d{2}[-_]\d{2}[-_]\d{2}', fname)
    date = date_match.group().replace('_', '-') if date_match else ""

    with open(fpath) as f:
        data = json.load(f)

    if not isinstance(data, list):
        return entries

    count = len(data)

    # DisclosureList 实体
    list_entity = create_disclosure_list(company, dtype, count, date, collected_at=mtime)
    entries.append(list_entity)
    list_id = list_entity["entity"]["id"]
    source_id = cfc_company_id(company)

    # 源公司 publishes disclosure
    entries.append(create_relation(source_id, "publishes_disclosure", list_id))

    for item in data:
        name = item.get("name", "")
        phone = item.get("phone", "")
        if not name or len(name) < 4:
            continue

        cid = safe_id("co", name)
        co_type = classify_company(name)

        # Company 实体（collected_at = 文件修改时间）
        entry = create_company(name, company, dtype, phone, collected_at=mtime)
        entries.append(entry)

        # DisclosureList includes company
        entries.append(create_relation(list_id, "includes_company", cid, {"role": co_type}))

        # Company cooperates_with source
        entries.append(create_relation(cid, "cooperates_with", source_id, {
            "cooperation_type": dtype,
            "disclosure_date": date,
        }))

    return entries


def process_announcements(company: str, ann_file: Path, inserted_at: str) -> list[dict]:
    """处理 announcements.json，提取文档实体和关联公司。"""
    entries = []
    with open(ann_file) as f:
        announcements = json.load(f)

    for item in announcements:
        title = item.get("title", "")[:100]
        date = item.get("date", "")
        url = item.get("url", "")
        category = item.get("category", "")
        text = item.get("text", "")[:1000]
        dtype = detect_disclosure_type(title, category)

        doc_id = safe_id("doc", f"{company}_{url}")
        source_id = cfc_company_id(company)

        # DisclosureDocument 实体
        doc_props = {
            "title": title,
            "date": date,
            "url": url,
            "category": category,
            "disclosure_type": dtype,
            "source_company": company,
        }
        if date:
            # 公告发布日期作为 collected_at
            doc_props["collected_at"] = date + "T00:00:00+0800"
        doc_props["inserted_at"] = inserted_at
        entries.append({"op": "create", "entity": {"id": doc_id, "type": "DisclosureDocument", "properties": doc_props}})

        # Document disclosed_by source company
        entries.append(create_relation(doc_id, "disclosed_by", source_id))

        # 从正文中提取公司名
        extracted_names = extract_company_names(text)
        for cname in extracted_names:
            cid = safe_id("co", cname)
            c_at = (date + "T00:00:00+0800") if date else ""
            entries.append(create_company(cname, company, dtype, collected_at=c_at))
            entries.append(create_relation(cid, "appears_in_document", doc_id, {
                "disclosure_type": dtype,
            }))
            entries.append(create_relation(cid, "cooperates_with", source_id, {
                "cooperation_type": dtype,
                "disclosure_date": date,
            }))

    return entries


def deduplicate(entries: list[dict]) -> list[dict]:
    """按 (op, id/from, rel, to) 去重，保留首次出现的版本。"""
    seen = {}
    result = []
    for e in entries:
        key = (
            e.get("op", ""),
            e.get("entity", {}).get("id", "") or e.get("from", ""),
            e.get("rel", ""),
            e.get("to", ""),
        )
        if key not in seen:
            seen[key] = True
            result.append(e)
    return result


def run(source_dir: Path = None, company: str = None) -> int:
    """
    Phase 3 主入口。

    数据分布两种模式:
      1. 顶层结构化文件: cfc_raw_data/{公司}_合作机构_*.json
      2. 按日期归档:     cfc_raw_data/{日期}/{公司}/announcements.json

    对每家找到的公司:
      - *合作机构*.json  → process_collection_file()
      - announcements.json → process_announcements()

    输出追加写入 ontology graph.jsonl。
    """
    if source_dir is None:
        source_dir = RAW_DIR

    written = 0
    batch = []
    now = ts()  # 统一入库时间戳

    # ── 第一遍：顶层结构化文件 ──────────────────────────────────────
    # 匹配 cfc_raw_data/{公司}_合作机构_*.json
    for fpath in sorted(source_dir.glob("*_合作机构_*.json")):
        # 从文件名提取公司名："中邮消费金融_合作机构_催收2026.json"
        parts = fpath.stem.split("_", 1)  # ['中邮消费金融', '合作机构_催收2026']
        co_name = parts[0]
        if company and co_name != company:
            continue
        print(f"  [顶层] {co_name}: {fpath.name}")
        batch.extend(process_collection_file(fpath, co_name, now))

    # ── 第二遍：按日期归档的 announcements.json ───────────────────
    # 匹配 cfc_raw_data/{日期}/{公司}/announcements.json
    # 收集每个公司最后一次（最新日期）的 announcements
    latest_ann: dict[str, Path] = {}
    for date_dir in sorted(source_dir.iterdir()):
        if not date_dir.is_dir():
            continue
        if not re.match(r'^20\d{2}-\d{2}-\d{2}$', date_dir.name):
            continue
        for co_dir in sorted(date_dir.iterdir()):
            if not co_dir.is_dir():
                continue
            ann_file = co_dir / "announcements.json"
            if ann_file.exists():
                # 保留最新日期的 announcements
                if co_dir.name not in latest_ann:
                    latest_ann[co_dir.name] = ann_file
                else:
                    # compare dates
                    existing = latest_ann[co_dir.name]
                    # already latest, skip

    for co_name, ann_file in sorted(latest_ann.items()):
        if company and co_name != company:
            continue
        print(f"  [归档] {co_name}: {ann_file.parent.parent.name}/{ann_file.parent.name}/announcements.json")
        batch.extend(process_announcements(co_name, ann_file, now))

    # 全局去重
    batch = deduplicate(batch)

    # 注入 inserted_at 时间戳
    if batch:
        batch = inject_ts(batch, now)

    if batch:
        ONTOLOGY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ONTOLOGY_FILE, "a") as f:
            for e in batch:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
                written += 1
        print(f"Phase 3: Wrote {written} entries ({len(deduplicate(batch))} unique) → {ONTOLOGY_FILE.name}")
    else:
        print("Phase 3: Nothing new to write")

    return written


if __name__ == "__main__":
    import sys
    co = sys.argv[1] if len(sys.argv) > 1 else None
    run(company=co)
