from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Tuple


PERIOD_PATTERNS = [
    (re.compile(r"(?P<year>\d{4})年1-(?P<month>\d{1,2})月财政收支情况"), "range"),
    (re.compile(r"(?P<year>\d{4})年(?:前)?(?P<quarter>[一二三])季度财政收支情况"), "quarter"),
    (re.compile(r"(?P<year>\d{4})年上半年财政收支情况"), "half"),
    (re.compile(r"(?P<year>\d{4})年财政收支情况"), "annual"),
    (re.compile(r"(?P<year>\d{4})年(?P<month>\d{1,2})月财政收支情况"), "single"),
]

SECTION_ALIASES = {
    "一般公共预算收入情况": ("财政收入", "一般公共预算收入"),
    "一般公共预算支出情况": ("财政支出", "一般公共预算支出"),
    "政府性基金预算收入情况": ("财政收入", "政府性基金预算收入"),
    "政府性基金预算支出情况": ("财政支出", "政府性基金预算支出"),
}

METRIC_SPECS = [
    ("全国一般公共预算收入", "财政收入", "一般公共预算收入"),
    ("全国税收收入", "财政收入", "一般公共预算收入"),
    ("全国非税收入", "财政收入", "一般公共预算收入"),
    ("中央一般公共预算收入", "财政收入", "一般公共预算收入"),
    ("地方一般公共预算本级收入", "财政收入", "一般公共预算收入"),
    ("国内增值税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("国内消费税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("企业所得税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("个人所得税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("进口货物增值税、消费税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("关税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("出口退税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("城市维护建设税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("车辆购置税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("印花税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("证券交易印花税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("资源税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("契税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("房产税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("城镇土地使用税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("土地增值税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("耕地占用税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("环境保护税", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("车船税、船舶吨税、烟叶税等其他各项税收收入合计", "财政收入", "一般公共预算收入/主要税收收入项目"),
    ("全国政府性基金预算收入", "财政收入", "政府性基金预算收入"),
    ("中央政府性基金预算收入", "财政收入", "政府性基金预算收入"),
    ("地方政府性基金预算本级收入", "财政收入", "政府性基金预算收入"),
    ("国有土地使用权出让收入", "财政收入", "政府性基金预算收入"),
    ("全国一般公共预算支出", "财政支出", "一般公共预算支出"),
    ("中央一般公共预算本级支出", "财政支出", "一般公共预算支出"),
    ("地方一般公共预算支出", "财政支出", "一般公共预算支出"),
    ("教育支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("科学技术支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("文化旅游体育与传媒支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("社会保障和就业支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("卫生健康支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("节能环保支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("城乡社区支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("农林水支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("交通运输支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("债务付息支出", "财政支出", "一般公共预算支出/主要支出科目"),
    ("全国政府性基金预算支出", "财政支出", "政府性基金预算支出"),
    ("中央政府性基金预算本级支出", "财政支出", "政府性基金预算支出"),
    ("地方政府性基金预算支出", "财政支出", "政府性基金预算支出"),
    ("国有土地使用权出让收入相关支出", "财政支出", "政府性基金预算支出"),
]


@dataclass(frozen=True)
class DocumentMeta:
    title: str
    url: str
    publish_date: date
    source_department: str
    content: str
    period_text: str
    cutoff_month: str


def build_period_label(period_text: str, cutoff_month: str) -> str:
    year = cutoff_month.split("-")[0]
    if period_text == "1-2月":
        return f"{year}-01~02"
    return cutoff_month


def build_source_period_key(period_text: str, cutoff_month: str) -> str:
    year, cutoff = cutoff_month.split("-")
    if period_text.startswith("1-") and period_text.endswith("月"):
        end_month = period_text[2:-1].zfill(2)
        return f"{year}01-{year}{end_month}"
    month = cutoff.zfill(2)
    return f"{year}{month}-{year}{month}"


def build_derived_period_display(period_label: str) -> str:
    if "~" in period_label:
        start, end = period_label.split("~")
        start_year, start_month = start.split("-")
        if "-" in end:
            _, end_month = end.split("-")
        else:
            end_month = end
        return f"{start_year}{start_month}～{end_month.zfill(2)}"
    year, month = period_label.split("-")
    return f"{year}{month.zfill(2)}"


def is_combined_jan_feb(period_text: str, cutoff_month: str) -> bool:
    return period_text == "1-2月" and cutoff_month.endswith("-02")


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_extraction_text(text: str) -> str:
    text = normalize_text(text)
    text = text.replace("\n", "")
    text = re.sub(r"(?<=\d)\s*(?=亿元)", "", text)
    text = re.sub(r"(?<=\d)\s*(?=%)", "", text)
    text = re.sub(r"同比\s*(增长|下降)\s*", r"同比\1", text)
    text = re.sub(r"(\d)\s*\.\s*", r"\1.", text)
    text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)
    return text


def parse_period_from_title(title: str) -> Tuple[str, str]:
    title = normalize_text(title)
    for pattern, kind in PERIOD_PATTERNS:
        match = pattern.search(title)
        if not match:
            continue
        year = int(match.group("year"))
        if kind == "range":
            month = int(match.group("month"))
            return f"1-{month}月", f"{year:04d}-{month:02d}"
        if kind == "quarter":
            quarter_map = {"一": 3, "二": 6, "三": 9}
            month = quarter_map[match.group("quarter")]
            return f"1-{month}月", f"{year:04d}-{month:02d}"
        if kind == "half":
            return "1-6月", f"{year:04d}-06"
        if kind == "annual":
            return "1-12月", f"{year:04d}-12"
        if kind == "single":
            month = int(match.group("month"))
            return f"{month}月", f"{year:04d}-{month:02d}"
    raise ValueError(f"无法从标题解析期间: {title}")


def month_to_int(month: str) -> int:
    return int(month.split("-")[1])


def previous_month(month: str) -> Optional[str]:
    year, mon = month.split("-")
    mon_int = int(mon)
    if mon_int <= 1:
        return None
    return f"{year}-{mon_int - 1:02d}"


def parse_yoy_value(text: str) -> Optional[float]:
    match = re.search(r"同比(增长|下降)(\d+(?:\.\d+)?)(%|倍)", text)
    if not match:
        return None
    direction, value_text, unit = match.groups()
    value = float(value_text)
    if unit == "倍":
        value *= 100.0
    if direction == "下降":
        value = -value
    return round(value, 6)


def extract_amount_after(metric_name: str, text: str) -> Optional[float]:
    pattern = re.compile(re.escape(metric_name) + r"(\d+(?:\.\d+)?)亿元")
    match = pattern.search(text)
    if not match:
        return None
    return float(match.group(1))


def split_sentences(content: str) -> List[str]:
    text = normalize_extraction_text(content)
    return [segment.strip() for segment in re.split(r"[。\n]+", text) if segment.strip()]


def detect_section(line: str) -> Optional[Tuple[str, str]]:
    for key, value in SECTION_ALIASES.items():
        if key in line:
            return value
    return None


def metric_aliases(metric_name: str) -> List[str]:
    if metric_name == "全国税收收入":
        return ["全国税收收入", "税收收入"]
    if metric_name == "全国非税收入":
        return ["全国非税收入", "非税收入"]
    if metric_name == "出口退税":
        return ["出口退税", "出口货物退增值税、消费税"]
    return [metric_name]


def extract_metrics_from_content(doc_id: str, meta: DocumentMeta) -> List[Dict[str, object]]:
    current_direction = ""
    current_category = ""
    records: List[Dict[str, object]] = []
    seen = set()
    order_index = 0
    for sentence in split_sentences(meta.content):
        section = detect_section(sentence)
        if section:
            current_direction, current_category = section
        sentence_matches = []
        for metric_name, direction, category in METRIC_SPECS:
            matched_source_name = None
            value = None
            yoy = None
            matched_pos = None
            for alias in metric_aliases(metric_name):
                alias_pos = sentence.find(alias)
                if alias_pos < 0:
                    continue
                value = extract_amount_after(alias, sentence)
                if value is None:
                    continue
                matched_source_name = alias
                matched_pos = alias_pos
                yoy = parse_yoy_value(sentence[sentence.find(alias) :])
                break
            if matched_source_name is None or value is None or matched_pos is None:
                continue
            record_key = (doc_id, metric_name)
            if record_key in seen:
                continue
            sentence_matches.append(
                (
                    matched_pos,
                    metric_name,
                    {
                        "record_id": f"{doc_id}:{metric_name}",
                        "metric_month": meta.cutoff_month,
                        "period_label": build_period_label(meta.period_text, meta.cutoff_month),
                        "standard_metric_name": metric_name,
                        "source_metric_name": matched_source_name,
                        "metric_category": category or current_category,
                        "direction": direction or current_direction,
                        "value": value,
                        "unit": "亿元",
                        "yoy_growth": yoy,
                        "source_document_id": doc_id,
                        "source_title": meta.title,
                        "source_publish_date": meta.publish_date.isoformat(),
                        "period_text": meta.period_text,
                        "cutoff_month": meta.cutoff_month,
                    },
                )
            )
        for _, metric_name, record in sorted(sentence_matches, key=lambda item: item[0]):
            seen.add((doc_id, metric_name))
            order_index += 1
            record["source_order"] = order_index
            records.append(record)
    return records
