#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag_profile_enrich.py

标签画像补全（零依赖版v2）：支持双Sheet标签画像表，按"最后一级+来源隔离"匹配。
不依赖pandas/openpyxl，使用标准库zipfile+xml解析xlsx。

新画像表结构（标签指标表.xlsx）：
- Sheet「明略和合作伙伴标签大盘占比&来源」：用于 coverage_rate（大盘占比）与 来源
- Sheet「明略和合作伙伴标签量级」：用于 audience_size（标签量级）与 来源

说明：本脚本会将 coverage_rate 与 audience_size 合并到同一份画像记录中（按“标签名+来源”对齐），供后续展示与策略判断使用。

匹配逻辑（优先级从高到低）：
1. 取候选标签名最后一级（按_分割）→ 同来源精确匹配
2. 归一化精确匹配（去括号、去"岁"后缀、去标点）
3. 子串包含匹配（短名<2字时用全路径辅助判断）
4. TF-IDF字符n-gram模糊匹配兜底
5. 来源（source）严格隔离：明略标签只匹配明略画像，合作伙伴标签只匹配合作伙伴画像
"""

import argparse
import csv
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Tuple


# ---------- xlsx parser (stdlib only) ----------

def _col_letter_to_idx(letter: str) -> int:
    n = 0
    for c in letter:
        n = n * 26 + (ord(c.upper()) - ord('A') + 1)
    return n - 1


def _parse_sheet(z: zipfile.ZipFile, sheet_file: str, shared_strings: List[str],
                 ns: Dict[str, str]) -> List[Dict[int, str]]:
    """Parse a single sheet XML into a list of row dicts {col_idx: value}."""
    sheet_xml = z.read(sheet_file)
    sheet_root = ET.fromstring(sheet_xml)
    rows = []
    for row in sheet_root.findall('.//main:row', ns):
        cells = {}
        max_col = 0
        for c in row.findall('main:c', ns):
            ref = c.get('r', '')
            col_m = re.match(r'([A-Z]+)', ref)
            col_letters = col_m.group(1) if col_m else 'A'
            col_idx = _col_letter_to_idx(col_letters)
            t = c.get('t', '')
            v_elem = c.find('main:v', ns)
            is_elem = c.find('main:is', ns)
            val = ''
            if t == 's' and v_elem is not None:
                idx = int(v_elem.text)
                val = shared_strings[idx] if 0 <= idx < len(shared_strings) else ''
            elif t == 'inlineStr' and is_elem is not None:
                val = ''.join([(t_.text or '') for t_ in is_elem.findall('.//main:t', ns)])
            elif v_elem is not None:
                val = v_elem.text or ''
            cells[col_idx] = val
            if col_idx > max_col:
                max_col = col_idx
        rows.append(cells)
    return rows


def _read_xlsx_all_sheets(path: str) -> Dict[str, List[Dict[int, str]]]:
    """Read all sheets from xlsx, returns {sheet_name: [row_dicts]}."""
    ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path, 'r') as z:
        # shared strings
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            ss_root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in ss_root.findall('.//main:si', ns):
                shared_strings.append(''.join([(t.text or '') for t in si.findall('.//main:t', ns)]))

        # sheet name → r:id mapping
        sheets = []
        wb_root = ET.fromstring(z.read('xl/workbook.xml'))
        for s in wb_root.findall('.//main:sheet', ns):
            sheets.append((s.get('name'), s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')))

        # r:id → sheet file mapping
        rels_root = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rid_to_target = {}
        for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            rid_to_target[rel.get('Id')] = rel.get('Target')

        result = {}
        for sheet_name, rid in sheets:
            target = rid_to_target.get(rid, '')
            sheet_path = 'xl/' + target if not target.startswith('/') else target.lstrip('/')
            if sheet_path in z.namelist():
                result[sheet_name] = _parse_sheet(z, sheet_path, shared_strings, ns)
        return result


# ---------- Profile record builders ----------

def _to_float(v) -> Optional[float]:
    if v is None:
        return None
    s = str(v).strip().replace('%', '').replace(',', '').replace('"', '')
    if s in ('', 'nan', 'None', 'null', '-'):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _build_records_明略(rows: List[Dict[int, str]]) -> List[Dict[str, Any]]:
    """Parse 明略标签画像 sheet.

    明略Sheet是树形层级结构：
    - 前半段（人口属性等单级标签）：A=标签名, F=大盘占比(5), G=来源(6)
    - 后半段（兴趣爱好/媒体等多级标签）：A=一级大类, B/C/D/E=二~五级分类,
      最深层非空列即为标签名（叶子节点）, F=大盘占比, G=来源
    统一处理：扫描B~E列取最深非空值作为标签名；若B~E全空则A列就是标签名。
    """
    records = []
    for row in rows[1:]:  # skip header
        coverage_raw = str(row.get(5, '')).strip()
        source = str(row.get(6, '')).strip() or '明略标签'
        coverage = _to_float(coverage_raw)
        if coverage is None:
            continue  # 跳过占比无效的行

        # 找最深层非空列（B=1到E=4）作为标签名
        leaf_name = ''
        category = ''  # 二级分类（如"美妆个护"、"视频服务"）
        for col_idx in range(4, 0, -1):  # E→D→C→B
            v = str(row.get(col_idx, '')).strip()
            if v:
                leaf_name = v
                break
        # 如果B~E全空，A列就是标签名
        if not leaf_name:
            leaf_name = str(row.get(0, '')).strip()

        # category取B列值（二级分类）
        category = str(row.get(1, '')).strip()
        # 如果B列也空，用A列
        if not category:
            category = str(row.get(0, '')).strip()

        if not leaf_name:
            continue

        records.append({
            'name': leaf_name,
            'coverage_rate': coverage,
            'audience_size': None,
            'source': source,
            'category': category,
            'dimension': str(row.get(0, '')).strip(),  # 一级大类作为dimension
        })
    return records


def _build_records_合作伙伴(rows: List[Dict[int, str]]) -> List[Dict[str, Any]]:
    """Parse 合作伙伴标签画像 sheet: A=一级分类(0), B=标签名(1), E=大盘占比(4), F=来源(5)."""
    records = []
    current_category = ''
    for row in rows[1:]:  # skip header
        cat = str(row.get(0, '')).strip()
        name = str(row.get(1, '')).strip()
        coverage_raw = str(row.get(4, '')).strip()
        source = str(row.get(5, '')).strip() or '合作伙伴标签'
        coverage = _to_float(coverage_raw)
        if cat:
            current_category = cat
        if not name or coverage is None:
            continue
        records.append({
            'name': name,
            'coverage_rate': coverage,
            'source': source,
            'category': current_category,
            'dimension': current_category,
        })
    return records


def _build_size_map(rows: List[Dict[int, str]]) -> Dict[tuple, int]:
    """Parse '明略和合作伙伴标签量级' sheet: 标签(0), 标签量级(1), 来源(2)

    Returns map key=(name, source) -> audience_size(int)
    """
    size_map: Dict[tuple, int] = {}
    if not rows:
        return size_map
    for row in rows[1:]:  # skip header
        name = str(row.get(0, '')).strip()
        size_raw = str(row.get(1, '')).strip()
        source = str(row.get(2, '')).strip()
        if not name or not size_raw or not source:
            continue
        try:
            size_val = int(float(size_raw.replace(',', '')))
        except Exception:
            continue
        size_map[(name, source)] = size_val
    return size_map



# ---------- Name matching ----------

def _normalize_name(name: str) -> str:
    """标准化：去括号内容、去'岁'后缀、去标点空格"""
    s = str(name).strip()
    s = re.sub(r'[（(][^）)]*[）)]', '', s)   # 去括号补充说明
    s = re.sub(r'岁$', '', s)                  # 去末尾"岁"
    s = re.sub(r'\+$', '', s)                  # 去末尾"+"（如"45+"）
    s = re.sub(r'[\s\-—_/·、，,。.！!？?（）()\[\]【】]', '', s)
    return s


def _last_segment(tag_name: str) -> str:
    """取标签名最后一级：基础属性_性别_女 → 女"""
    parts = str(tag_name).strip().split('_')
    return parts[-1].strip() if parts else str(tag_name).strip()


def _char_ngrams(text: str, n: int = 2) -> List[str]:
    text = re.sub(r'[^\u4e00-\u9fff\w]', '', text.strip().lower())
    if len(text) < n:
        return [text] if text else []
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def _fuzzy_score(query: str, candidate: str) -> float:
    """TF-IDF式字符n-gram Dice系数相似度。"""
    q_grams, c_grams = [], []
    for n in (1, 2, 3):
        q_grams.extend(_char_ngrams(query, n))
        c_grams.extend(_char_ngrams(candidate, n))
    if not q_grams or not c_grams:
        return 0.0
    q_set, c_set = set(q_grams), set(c_grams)
    inter = q_set & c_set
    if not inter:
        return 0.0
    return 2 * len(inter) / (len(q_set) + len(c_set))


def _detect_source(tag: Dict[str, Any]) -> str:
    """从候选标签的source/labelSource/tagSource字段判断来源。"""
    for key in ('source', 'labelSource', 'tagSource', 'tag_source', 'dataSource'):
        v = str(tag.get(key, '') or '').strip()
        if v:
            return v
    # 通过tagId前缀或目录特征推断
    tag_name = str(tag.get('tagName', '') or '')
    if tag_name.startswith('基础属性_') or tag_name.startswith('城市分布_') or \
       tag_name.startswith('兴趣偏好_') or tag_name.startswith('品牌_') or \
       tag_name.startswith('机型_') or tag_name.startswith('场景偏好_') or \
       tag_name.startswith('省份分布_') or tag_name.startswith('消费水平_') or \
       tag_name.startswith('消费行为_') or tag_name.startswith('运营商_') or \
       tag_name.startswith('系统语言_') or tag_name.startswith('有小孩_') or \
       tag_name.startswith('职业') or tag_name.startswith('婚姻状态_') or \
       tag_name.startswith('感情状态_') or tag_name.startswith('居住地区_') or \
       tag_name.startswith('性别') or tag_name.startswith('年龄'):
        return '合作伙伴标签'
    # 明略标签路径前缀
    if tag_name.startswith('兴趣爱好_') or tag_name.startswith('人口属性_') or \
       tag_name.startswith('应用偏好_') or tag_name.startswith('媒体偏好_'):
        return '明略标签'
    return ''


def _match_tag(last_seg: str, tag_full: str, source: str,
               records_by_source: Dict[str, List[Dict[str, Any]]]) -> Tuple[Optional[Dict], float, str]:
    """按优先级匹配单个标签，返回 (best_record, score, match_type)。"""
    candidates = records_by_source.get(source, [])
    if not candidates:
        # 如果来源未知，在所有记录中搜索
        candidates = []
        for recs in records_by_source.values():
            candidates.extend(recs)

    last_norm = _normalize_name(last_seg)
    full_norm = _normalize_name(tag_full)

    # ---- 1) 最后一级精确匹配 ----
    for rec in candidates:
        if rec['name'] == last_seg:
            return rec, 1.0, 'last_exact'

    # ---- 2) 归一化精确匹配 ----
    for rec in candidates:
        if _normalize_name(rec['name']) == last_norm:
            return rec, 0.95, 'last_norm_exact'

    # ---- 3) 子串包含匹配 ----
    # 短名（<2字）用全路径辅助判断，避免"女"匹配到"男女同款"等误匹配
    is_short = len(last_norm) < 2
    for rec in candidates:
        rnorm = _normalize_name(rec['name'])
        if not rnorm or not last_norm:
            continue
        # 双向包含
        if last_norm in rnorm or rnorm in last_norm:
            if is_short and len(rnorm) != len(last_norm):
                # 短名字串匹配要求全路径也有重叠，降低误匹配
                if rnorm in full_norm or last_norm in _normalize_name(rec.get('category', '')):
                    return rec, 0.7, 'substring_fullpath'
                continue
            return rec, 0.8, 'substring'

    # ---- 4) 模糊匹配兜底 ----
    best_score, best_rec = 0.0, None
    for rec in candidates:
        if not rec['name']:
            continue
        score = _fuzzy_score(last_seg, rec['name'])
        # 短名要求更高阈值避免误匹配
        threshold = 0.5 if is_short else 0.35
        if score > best_score and score >= threshold:
            best_score = score
            best_rec = rec
    if best_rec:
        return best_rec, round(best_score, 4), 'fuzzy'

    return None, 0.0, 'none'


# ---------- CSV / JSON loaders (legacy format support) ----------

def _read_csv(path: str) -> List[List[Optional[str]]]:
    rows = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def _build_records_from_rows(raw_rows: List[List[Optional[str]]]) -> Dict[str, List[Dict[str, Any]]]:
    """Legacy loader for old single-sheet format with headers: tag_id/tag_name/fill_rate/coverage_rate/audience_size/source/dimension/category"""
    # Find header
    header_idx = 0
    for i in range(min(20, len(raw_rows))):
        row_vals = [str(v).strip().lower() if v else '' for v in raw_rows[i]]
        if any(v in ('tag_name', 'tagname', '标签名', 'name') for v in row_vals):
            header_idx = i
            break
    headers = [str(v).strip() if v else '' for v in raw_rows[header_idx]]

    # Find columns
    name_col = fill_col = cov_col = aud_col = src_col = dim_col = cat_col = None
    for j, h in enumerate(headers):
        hl = h.lower()
        if name_col is None and hl in ('tag_name', 'tagname', '标签名', 'name'):
            name_col = j
        if fill_col is None and ('fill' in hl or '填充' in h):
            fill_col = j
        if cov_col is None and ('coverage' in hl or 'cover' in hl or '覆盖' in h or '大盘占比' in h):
            cov_col = j
        if aud_col is None and ('audience' in hl or '量级' in h or '人群量' in h):
            aud_col = j
        if src_col is None and ('source' in hl or '来源' in h):
            src_col = j
        if dim_col is None and ('dimension' in hl or '维度' in h):
            dim_col = j
        if cat_col is None and ('category' in hl or '类目' in h or '分类' in h):
            cat_col = j
    if name_col is None:
        return {}

    records = []
    for row in raw_rows[header_idx + 1:]:
        name = str(row[name_col]).strip() if name_col < len(row) and row[name_col] else ''
        if not name:
            continue
        cov = _to_float(row[cov_col]) if cov_col is not None and cov_col < len(row) else None
        fil = _to_float(row[fill_col]) if fill_col is not None and fill_col < len(row) else None
        src = str(row[src_col]).strip() if src_col is not None and src_col < len(row) and row[src_col] else ''
        dim = str(row[dim_col]).strip() if dim_col is not None and dim_col < len(row) and row[dim_col] else ''
        cat = str(row[cat_col]).strip() if cat_col is not None and cat_col < len(row) and row[cat_col] else ''
        records.append({
            'name': name, 'coverage_rate': cov, 'fill_rate': fil,
            'source': src, 'category': cat, 'dimension': dim
        })

    # Group by source
    by_source: Dict[str, List[Dict]] = {}
    for r in records:
        s = r.get('source', '') or 'unknown'
        by_source.setdefault(s, []).append(r)
    return by_source


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True, help="candidates.json")
    ap.add_argument("--profile", default="assets/标签指标表.xlsx", help="标签指标表")
    ap.add_argument("--out", required=True, help="enriched.json")
    ap.add_argument("--match-threshold", type=float, default=0.25, help="模糊匹配阈值(0-1)")
    args = ap.parse_args()

    with open(args.candidates, "r", encoding="utf-8") as f:
        cands: List[Dict[str, Any]] = json.load(f)

    ext = os.path.splitext(args.profile)[1].lower()
    records_by_source: Dict[str, List[Dict[str, Any]]] = {}

    if ext == '.xlsx':
        sheets = _read_xlsx_all_sheets(args.profile)
        all_records = []
        # 量级表：name+source -> audience_size
        size_map: Dict[tuple, int] = {}
        for sheet_name, rows in sheets.items():
            if '标签量级' in sheet_name:
                size_map.update(_build_size_map(rows))

        for sheet_name, rows in sheets.items():
            if '大盘占比' in sheet_name or '占比' in sheet_name:
                # 该sheet用于coverage
                recs = _build_records_明略(rows)
                # 为每条记录补齐audience_size（按name+source）
                for r in recs:
                    r['audience_size'] = size_map.get((r.get('name'), r.get('source')))
                # 按来源入桶（明略/合作伙伴）
                for r in recs:
                    src = r.get('source') or ''
                    if '合作伙伴' in src:
                        records_by_source.setdefault('合作伙伴标签', []).append(r)
                    else:
                        records_by_source.setdefault('明略标签', []).append(r)
                all_records.extend(recs)
            else:
                # 其他sheet忽略（如标签量级已单独处理）
                continue

        # Fallback: if no sheets matched by name, try legacy flat format from first sheet
        if not all_records and sheets:
            first_sheet = list(sheets.values())[0]
            raw = [[r.get(i, '') for i in range(max(r.keys()) + 1) if r] for r in first_sheet]
            records_by_source = _build_records_from_rows(raw)

    elif ext == '.csv':
        raw = _read_csv(args.profile)
        records_by_source = _build_records_from_rows(raw)
    elif ext == '.json':
        with open(args.profile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for rec in data if isinstance(data, list) else []:
            s = rec.get('source', '') or 'unknown'
            records_by_source.setdefault(s, []).append(rec)
    else:
        raise SystemExit(f"不支持的文件类型: {ext}")

    # Stats
    total_records = sum(len(v) for v in records_by_source.values())
    if total_records == 0:
        raise SystemExit("画像表为空或无法解析，请检查格式")
    print(f"[tag_profile_enrich] 画像表加载完成: " +
          ", ".join(f"{s}={len(r)}条" for s, r in records_by_source.items()), flush=True)

    # Match each candidate
    out = []
    stat = {'exact': 0, 'norm_exact': 0, 'substring': 0, 'fuzzy': 0, 'missing': 0}

    for c in cands:
        tag_name = str(c.get("tagName", '') or '').strip()
        source = _detect_source(c)
        last_seg = _last_segment(tag_name)

        best_rec, best_score, match_type = _match_tag(last_seg, tag_name, source, records_by_source)

        c2 = dict(c)
        if best_rec and best_score >= args.match_threshold:
            cr = best_rec.get('coverage_rate')
            aud_sz = best_rec.get('audience_size')

            # 百分比→0~1（如果>1则视为百分比；本技能量级版仍可能从旧画像表读到百分比）
            if cr is not None and cr > 1:
                cr = cr / 100.0

            # eng_score：避免量纲冲突，仅用 coverage_rate 作为质量代理（量级仅用于展示）
            eng = round(cr, 4) if cr is not None else None

            c2.update({
                "audience_size": int(aud_sz) if aud_sz is not None else None,
                "coverage_rate": round(cr, 4) if cr is not None else None,
                "eng_score": eng,
                "dimension": best_rec.get('dimension', ''),
                "category": best_rec.get('category', ''),
                "profile_source": best_rec.get('source', ''),
                "profile_status": "OK",
                "profile_match_name": best_rec.get('name', ''),
                "profile_match_score": best_score,
                "profile_match_type": match_type,
                "profile_last_segment": last_seg,
            })
            stat[match_type if match_type in stat else 'exact'] += 1
        else:
            c2.update({
                "coverage_rate": None,
                "audience_size": None,
                "eng_score": None,
                "dimension": '',
                "category": '',
                "profile_source": source or '',
                "profile_status": "MISSING",
                "profile_match_name": None,
                "profile_match_score": 0,
                "profile_match_type": 'none',
                "profile_last_segment": last_seg,
            })
            stat['missing'] += 1
        out.append(c2)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "ok": True, "in": len(cands), "out": len(out),
        "ok_count": len(cands) - stat['missing'],
        "missing_count": stat['missing'],
        "match_breakdown": {k: v for k, v in stat.items() if v > 0},
        "file": args.out
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()