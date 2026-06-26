import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}
ET.register_namespace("w", W_NS)


DEFAULT_TEMPLATE_B64 = ROOT / "assets" / "beijing_office_annual_template.docx.base64.txt"
DEFAULT_OUTPUT_DIR = ROOT / "outputs"
DEFAULT_OUTPUT_NAME = "annual-insurance-report-{year}.docx"
DEFAULT_TABLE = "gh_hg_bscyearall_dues"


def _run_mysql_cli(
    sql: str,
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    charset: str,
    mysql_cli: str,
) -> List[Dict[str, str]]:
    args = [
        mysql_cli,
        "--batch",
        "--raw",
        f"--default-character-set={charset}",
        f"--host={host}",
        f"--port={port}",
        f"--user={user}",
        f"--password={password}",
        f"--database={database}",
        f"--execute={sql}",
    ]
    completed = subprocess.run(args, capture_output=True, text=True, check=True)
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        return []
    headers = lines[0].split("\t")
    rows: List[Dict[str, str]] = []
    for line in lines[1:]:
        values = line.split("\t")
        row = {}
        for idx, header in enumerate(headers):
            row[header] = values[idx] if idx < len(values) else ""
        rows.append(row)
    return rows


def _run_pymysql(
    sql: str,
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    charset: str,
) -> List[Dict[str, str]]:
    import pymysql  # type: ignore

    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset,
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return [{k: "" if v is None else str(v) for k, v in row.items()} for row in rows]
    finally:
        conn.close()


def query_mysql(sql: str, **kwargs) -> List[Dict[str, str]]:
    try:
        import pymysql  # noqa: F401

        return _run_pymysql(sql, **kwargs)
    except Exception:
        fallback_kwargs = dict(kwargs)
        mysql_cli = fallback_kwargs.pop("mysql_cli", None) or "mysql"
        return _run_mysql_cli(sql, mysql_cli=mysql_cli, **fallback_kwargs)


def parse_year(explicit_year: Optional[str], request_text: Optional[str]) -> str:
    if explicit_year:
        return explicit_year
    if request_text:
        match = re.search(r"(?<!\d)(20\d{2})(?!\d)", request_text)
        if match:
            return match.group(1)
    raise ValueError("year is required, or request_text must contain a four-digit year.")


def decimal_text(value: Optional[str]) -> str:
    if value is None or str(value).strip() == "":
        return ""
    text = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return text


def wan_yuan_text(value: Optional[str]) -> str:
    if value is None or str(value).strip() == "":
        return ""
    text = f"{float(value) / 10000:.2f}".rstrip("0").rstrip(".")
    return text


def sum_sql(table_name: str, year: str) -> str:
    return f"""
SELECT
  typecode,
  SUM(COALESCE(tuanyi, 0)) AS tuanyi,
  SUM(COALESCE(zinv, 0)) AS zinv,
  SUM(COALESCE(nvgongteji, 0) + COALESCE(nvgongteji25, 0)) AS nvgongteji,
  SUM(COALESCE(zhongji, 0) + COALESCE(zhongdajibing90, 0) + COALESCE(zhongdajibing40, 0)) AS zhongji,
  SUM(COALESCE(qingzheng, 0)) AS qingzheng,
  SUM(COALESCE(yiliao, 0)) AS yiliao,
  SUM(COALESCE(jintie, 0)) AS jintie,
  SUM(COALESCE(buchongyiliao, 0)) AS buchongyiliao,
  SUM(COALESCE(liangai, 0)) AS liangai,
  SUM(COALESCE(zonghea, 0)) AS zonghea,
  SUM(COALESCE(zongheb, 0)) AS zongheb,
  SUM(
    COALESCE(tuanyi, 0) + COALESCE(zinv, 0) + COALESCE(nvgongteji, 0) + COALESCE(nvgongteji25, 0) +
    COALESCE(zhongji, 0) + COALESCE(zhongdajibing90, 0) + COALESCE(zhongdajibing40, 0) +
    COALESCE(qingzheng, 0) + COALESCE(yiliao, 0) + COALESCE(jintie, 0) +
    COALESCE(buchongyiliao, 0) + COALESCE(liangai, 0) + COALESCE(zonghea, 0) + COALESCE(zongheb, 0)
  ) AS total
FROM {table_name}
WHERE date_year = {year}
  AND typecode IN (1, 2, 3, 4, 5, 6)
GROUP BY typecode
ORDER BY typecode
"""


def metadata_sql(database: str, table_name: str) -> str:
    return f"""
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  ORDINAL_POSITION,
  COLUMN_NAME,
  DATA_TYPE,
  COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '{database}'
  AND TABLE_NAME = '{table_name}'
ORDER BY ORDINAL_POSITION
"""


def load_data(
    *,
    year: str,
    database: str,
    table_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
    charset: str,
    mysql_cli: Optional[str],
) -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]], List[Dict[str, str]]]:
    common = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "charset": charset,
        "mysql_cli": mysql_cli,
    }
    rows = query_mysql(sum_sql(table_name, year), **common)
    if not rows:
        raise RuntimeError(f"No data found for year {year}.")
    prev_rows = query_mysql(sum_sql(table_name, str(int(year) - 1)), **common)
    metadata_rows = query_mysql(metadata_sql(database, table_name), **common)
    current = {str(int(float(row["typecode"]))): row for row in rows}
    previous = {str(int(float(row["typecode"]))): row for row in prev_rows}
    return current, previous, metadata_rows


def build_placeholder_map(
    year: str,
    current: Dict[str, Dict[str, str]],
    previous: Dict[str, Dict[str, str]],
) -> Dict[str, str]:
    def get_value(source: Dict[str, Dict[str, str]], typecode: str, field: str = "total") -> Optional[str]:
        row = source.get(typecode)
        return None if row is None else row.get(field)

    insured_count = get_value(current, "3")
    prev_insured_count = get_value(previous, "3")
    insured_times = get_value(current, "1")
    insured_amount = get_value(current, "2")
    beneficiary_times = get_value(current, "4")
    aid_amount = get_value(current, "5")
    prev_aid_amount = get_value(previous, "5")

    def pct_change(now: Optional[str], old: Optional[str]) -> str:
        if not now or not old or float(old) == 0:
            return ""
        return decimal_text(abs(((float(now) - float(old)) / float(old)) * 100))

    return {
        "dateYear": year,
        "year": year,
        "data1": wan_yuan_text((float(insured_count) - float(prev_insured_count)) if insured_count and prev_insured_count else None),
        "data2": "" if not insured_count or not prev_insured_count or float(prev_insured_count) == 0 else decimal_text(((float(insured_count) - float(prev_insured_count)) / float(prev_insured_count)) * 100),
        "data3": wan_yuan_text(insured_times),
        "data4": wan_yuan_text(insured_amount),
        "data5": year,
        "data6": decimal_text(beneficiary_times),
        "data7": wan_yuan_text(aid_amount),
        "data8": pct_change(aid_amount, prev_aid_amount),
        "data9": year,
        "data10": decimal_text(beneficiary_times),
        "data11": wan_yuan_text(aid_amount),
        "beneficiaryTimes": decimal_text(beneficiary_times),
        "beneficiaryCount": decimal_text(get_value(current, "6")),
        "sumMoney": wan_yuan_text(aid_amount),
        "aidAmount": decimal_text(aid_amount),
        "insuredAmount": decimal_text(insured_amount),
    }


def replace_paragraphs(root: ET.Element, replacements: Dict[str, str]) -> None:
    for paragraph in root.findall(".//w:p", NS):
        text_nodes = paragraph.findall(".//w:t", NS)
        if not text_nodes:
            continue
        joined = "".join(node.text or "" for node in text_nodes)
        updated = joined
        for key, value in replacements.items():
            updated = updated.replace(f"{{{{{key}}}}}", value)
        if "year" in replacements:
            updated = updated.replace("#{year}", replacements["year"])
            updated = updated.replace("{year}", replacements["year"])
        if updated != joined:
            text_nodes[0].text = updated
            for node in text_nodes[1:]:
                node.text = ""


def set_cell_text(cell: ET.Element, text: str) -> None:
    text_nodes = cell.findall(".//w:t", NS)
    if not text_nodes:
        p = ET.SubElement(cell, f"{{{W_NS}}}p")
        r = ET.SubElement(p, f"{{{W_NS}}}r")
        t = ET.SubElement(r, f"{{{W_NS}}}t")
        t.text = text
        return
    text_nodes[0].text = text
    for node in text_nodes[1:]:
        node.text = ""


def fill_table(root: ET.Element, current: Dict[str, Dict[str, str]]) -> None:
    tables = root.findall(".//w:tbl", NS)
    if not tables:
        raise RuntimeError("No table found in template.")
    target_table = tables[0]
    rows = target_table.findall("./w:tr", NS)
    row_type_map = {
        4: "3",
        5: "1",
        6: "2",
        7: "6",
        8: "4",
        9: "5",
    }
    for row_index, typecode in row_type_map.items():
        if row_index - 1 >= len(rows):
            continue
        row_data = current.get(typecode)
        if not row_data:
            continue
        cells = rows[row_index - 1].findall("./w:tc", NS)
        if len(cells) < 13:
            continue
        label = "".join(node.text or "" for node in cells[0].findall(".//w:t", NS))
        values = [
            label,
            decimal_text(row_data.get("tuanyi")),
            decimal_text(row_data.get("zinv")),
            decimal_text(row_data.get("nvgongteji")),
            decimal_text(row_data.get("zhongji")),
            decimal_text(row_data.get("qingzheng")),
            decimal_text(row_data.get("yiliao")),
            decimal_text(row_data.get("jintie")),
            decimal_text(row_data.get("buchongyiliao")),
            decimal_text(row_data.get("liangai")),
            decimal_text(row_data.get("zonghea")),
            decimal_text(row_data.get("zongheb")),
            decimal_text(row_data.get("total")),
        ]
        for idx, value in enumerate(values):
            set_cell_text(cells[idx], value)


def inspect_metadata(metadata_rows: Iterable[Dict[str, str]]) -> Dict[str, str]:
    comment_map = {row["COLUMN_NAME"]: row.get("COLUMN_COMMENT", "") for row in metadata_rows}
    expected = {
        "tuanyi": "团意",
        "zinv": "子女",
        "yiliao": "住院",
        "jintie": "津贴",
        "qingzheng": "轻症",
        "nvgongteji": "女工",
        "zhongji": "重疾",
        "buchongyiliao": "补充",
        "liangai": "两癌",
        "zonghea": "综合A",
        "zongheb": "综合B",
    }
    mismatches = []
    for column, keyword in expected.items():
        comment = comment_map.get(column, "")
        if comment and keyword not in comment:
            mismatches.append(f"{column}:{comment}")
    return {
        "column_count": str(len(comment_map)),
        "mismatch_count": str(len(mismatches)),
        "mismatches": ", ".join(mismatches),
    }


def render_docx(
    *,
    template_path: Path,
    output_path: Path,
    replacements: Dict[str, str],
    current: Dict[str, Dict[str, str]],
) -> None:
    with tempfile.TemporaryDirectory(prefix="annual_insurance_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / "source.zip"
        extract_dir = tmp_path / "unzipped"
        extract_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(template_path, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        document_xml = extract_dir / "word" / "document.xml"
        tree = ET.parse(document_xml)
        root = tree.getroot()
        replace_paragraphs(root, replacements)
        fill_table(root, current)
        tree.write(document_xml, encoding="utf-8", xml_declaration=True)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()
        new_zip = tmp_path / "output.zip"
        with zipfile.ZipFile(new_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in extract_dir.rglob("*"):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(extract_dir))
        shutil.move(str(new_zip), output_path)


def materialize_default_template(temp_dir: Path) -> Path:
    target = temp_dir / "default_template.docx"
    encoded = DEFAULT_TEMPLATE_B64.read_text(encoding="ascii")
    target.write_bytes(base64.b64decode(encoded))
    return target


def run(
    *,
    request_text: Optional[str] = None,
    year: Optional[str] = None,
    template_path: Optional[str] = None,
    output_path: Optional[str] = None,
    db_host: str = "127.0.0.1",
    db_port: int = 3306,
    db_user: str = "root",
    db_password: str = "root",
    database: str = "test_db",
    table_name: str = DEFAULT_TABLE,
    charset: str = "utf8mb4",
    mysql_cli: Optional[str] = None,
) -> Dict[str, object]:
    resolved_year = parse_year(year, request_text)
    resolved_output = Path(output_path) if output_path else (DEFAULT_OUTPUT_DIR / DEFAULT_OUTPUT_NAME.format(year=resolved_year))
    current, previous, metadata_rows = load_data(
        year=resolved_year,
        database=database,
        table_name=table_name,
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password,
        charset=charset,
        mysql_cli=mysql_cli,
    )
    replacements = build_placeholder_map(resolved_year, current, previous)
    metadata_summary = inspect_metadata(metadata_rows)
    if template_path:
        resolved_template = Path(template_path)
        render_docx(
            template_path=resolved_template,
            output_path=resolved_output,
            replacements=replacements,
            current=current,
        )
    else:
        with tempfile.TemporaryDirectory(prefix="annual_template_") as tmp_dir:
            resolved_template = materialize_default_template(Path(tmp_dir))
            render_docx(
                template_path=resolved_template,
                output_path=resolved_output,
                replacements=replacements,
                current=current,
            )
    return {
        "year": resolved_year,
        "template_path": str(resolved_template if template_path else DEFAULT_TEMPLATE_B64),
        "output_path": str(resolved_output),
        "database": database,
        "table_name": table_name,
        "metadata_summary": metadata_summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate annual insurance welfare Word reports.")
    parser.add_argument("--request-text", help="Natural-language request that may contain the target year.")
    parser.add_argument("--year", help="Target year, for example 2023.")
    parser.add_argument("--template-path", help="Path to the .docx template.")
    parser.add_argument("--output-path", help="Path to write the generated .docx file.")
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="root")
    parser.add_argument("--database", default="test_db")
    parser.add_argument("--table-name", default=DEFAULT_TABLE)
    parser.add_argument("--charset", default="utf8mb4")
    parser.add_argument("--mysql-cli", help="Optional mysql CLI path used as a fallback when PyMySQL is unavailable.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = run(
        request_text=args.request_text,
        year=args.year,
        template_path=args.template_path,
        output_path=args.output_path,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        database=args.database,
        table_name=args.table_name,
        charset=args.charset,
        mysql_cli=args.mysql_cli,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
