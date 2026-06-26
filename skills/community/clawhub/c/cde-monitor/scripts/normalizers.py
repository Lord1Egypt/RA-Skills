from __future__ import annotations

import json
import re
from typing import Any, Dict, Iterable, List, Optional


DRUG_FIELDS = (
    "drgnamecn",
    "drug_name",
    "drugName",
    "drugname",
    "varietyName",
    "ypmc",
    "name",
    "title",
)

COMPANY_FIELDS = (
    "company",
    "companyName",
    "companys",
    "applicant",
    "applyPerson",
    "registerApplicant",
    "enterpriseName",
    "entname",
    "sqr",
)

ACCEPTANCE_FIELDS = (
    "acceptid",
    "acceptance_no",
    "acceptNo",
    "slh",
    "subcode",
)

TITLE_FIELDS = (
    "title",
    "noticeTitle",
    "pubTitle",
    "announcementTitle",
    "drug_name",
    "drgnamecn",
)

DATE_FIELDS = (
    "publicDate",
    "pubDate",
    "acceptDate",
    "createdate",
    "createTime",
    "date",
    "sqrq",
)

DRUG_TYPE_FIELDS = (
    "drugtype",
    "drugType",
)

APPLICATION_TYPE_FIELDS = (
    "applytype",
    "applyType",
)

REGISTRATION_CATEGORY_FIELDS = (
    "registerkind",
    "registerKind",
)

ID_FIELDS = (
    "paidCODE",
    "pridCODE",
    "bcaidCODE",
    "bcnidCODE",
    "pdidCODE",
    "bcdidCODE",
    "acceptidCODE",
    "idCODE",
)


def _first_value(record: Dict[str, Any], candidates: Iterable[str]) -> Optional[str]:
    for key in candidates:
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _infer_year(value: Optional[str], fallback_year: Optional[int]) -> Optional[int]:
    if fallback_year is not None:
        return fallback_year
    if not value:
        return None
    match = re.search(r"(20\d{2})", value)
    if match:
        return int(match.group(1))
    return None


def normalize_record(
    raw_record: Dict[str, Any],
    *,
    source_menu: str,
    source_tab: str,
    page: int,
    year: Optional[int] = None,
) -> Dict[str, Any]:
    date_value = _first_value(raw_record, DATE_FIELDS)
    normalized = {
        "record_id": _first_value(raw_record, ID_FIELDS),
        "drug_name": _first_value(raw_record, DRUG_FIELDS),
        "company_name": _first_value(raw_record, COMPANY_FIELDS),
        "acceptance_no": _first_value(raw_record, ACCEPTANCE_FIELDS),
        "drug_type": _first_value(raw_record, DRUG_TYPE_FIELDS),
        "application_type": _first_value(raw_record, APPLICATION_TYPE_FIELDS),
        "registration_category": _first_value(raw_record, REGISTRATION_CATEGORY_FIELDS),
        "publication_title": _first_value(raw_record, TITLE_FIELDS),
        "publication_date": date_value,
        "stage": source_tab,
        "year": _infer_year(date_value, year),
        "source_menu": source_menu,
        "source_tab": source_tab,
        "page": page,
    }
    return {"normalized": normalized, "raw": raw_record}


def _fingerprint(record: Dict[str, Any]) -> str:
    normalized = record.get("normalized", {})
    values = [
        normalized.get("source_menu"),
        normalized.get("source_tab"),
        normalized.get("record_id"),
        normalized.get("acceptance_no"),
        normalized.get("drug_name"),
        normalized.get("company_name"),
        normalized.get("publication_title"),
        normalized.get("year"),
    ]
    compact = [str(value).strip().lower() for value in values if value not in (None, "")]
    if compact:
        return "|".join(compact)
    return json.dumps(record.get("raw", record), ensure_ascii=False, sort_keys=True)


def dedupe_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    unique: Dict[str, Dict[str, Any]] = {}
    for record in records:
        unique.setdefault(_fingerprint(record), record)
    return list(unique.values())
