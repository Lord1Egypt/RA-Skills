#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_quota_engine.py - cnsdoce1 增强1：AI 智能组价专家（借鉴广联达 AI 组价专家）

功能：用户输入一句话清单描述（如"DN200碳钢法兰蝶阀安装10个"），自动完成：
  1. 清单特征解析（LLM hy3-preview，无Key时规则降级）
  2. 定额组合推荐（主定额 + 消耗量）
  3. Step0 单位比对（清单单位 vs 定额单位，自动折算系数）
  4. 三级查价（询价库 → 信息价第6期 → 济南价目表）
  5. 自动组价 AD = 基价 + 人工费×48.08%（按项目口径，不含利润税金）
  6. 输出结构化 JSON（供报价表/价格自检/指标引擎下游使用）

数据源（仅核心库，禁用 backup/*_work）：
  ~/.workbuddy/skills/cnsdoce1/assets/
    quota_consumption.db  quota_price.db  inquiry_inquiry.db  quota_jinan_2026.db  quota_reference.db

用法：
  python ai_quota_engine.py "DN200碳钢法兰蝶阀安装 10 个"
  python ai_quota_engine.py --json '{"name":"低压法兰阀门安装","spec":"200","qty":10,"unit":"个"}'
  python ai_quota_engine.py --no-llm "DN350 不锈钢平焊法兰 2 副"
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

ASSETS = Path(__file__).parent.parent / "assets"

# 管理费率（安装工程，济南）——从 fee_rates 动态读取，硬编码仅为降级兜底
DEFAULT_MGMT_RATE = 0.4808
DEFAULT_PROFIT_RATE = 0.2915

# ─────────────────────────── 三级价格查询 ───────────────────────────

def _connect(db_name):
    """连接数据库（只读模式，避免污染挂载盘）"""
    path = ASSETS / db_name
    if not path.exists():
        return None
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def lookup_price_3tier(resource_name, resource_spec=""):
    """
    三级查价：
      1. inquiry_inquiry.db 询价库（公司ERP采购价，优先）
      2. quota_price.db 信息价第6期 COALESCE(_06,_05,...)
      3. quota_jinan_2026.db 价目表 price_determination
    返回 {price, source, min_price, max_price, vendor_count, note}
    """
    result = {"price": None, "source": None, "min_price": None,
              "max_price": None, "vendor_count": None, "note": ""}
    name = (resource_name or "").strip()
    spec = (resource_spec or "").strip()

    # 1) 询价库
    conn = _connect("inquiry_inquiry.db")
    if conn:
        try:
            sql = "SELECT material_name, spec, min_price, max_price, avg_price, vendor_count FROM inquiry_materials WHERE 1=1"
            params = []
            if name:
                sql += " AND material_name LIKE ?"
                params.append(f"%{name}%")
            if spec:
                sql += " AND (spec LIKE ? OR material_name LIKE ?)"
                params.extend([f"%{spec}%", f"%{spec}%"])
            sql += " ORDER BY inquiry_count DESC, last_inquiry_date DESC LIMIT 5"
            rows = conn.execute(sql, params).fetchall()
            if rows:
                r = rows[0]
                result.update({
                    "price": r["avg_price"],
                    "source": "公司询价库(ERP)",
                    "min_price": r["min_price"],
                    "max_price": r["max_price"],
                    "vendor_count": r["vendor_count"],
                    "note": f"匹配 {len(rows)} 条，取最新最高频"
                })
                conn.close()
                return result
        except Exception:
            pass
        conn.close()

    # 2) 信息价（最新非空期）
    conn = _connect("quota_price.db")
    if conn:
        try:
            sql = """SELECT resource_name, resource_spec, resource_unit,
                     COALESCE(price_jinan_2026_06, price_jinan_2026_05, price_jinan_2026_04,
                              price_jinan_2026_03, price_jinan_2026_02, price_jinan_2026_01) AS p
                     FROM price_list WHERE 1=1"""
            params = []
            if name:
                sql += " AND resource_name LIKE ?"
                params.append(f"%{name}%")
            if spec:
                sql += " AND resource_spec LIKE ?"
                params.append(f"%{spec}%")
            sql += " AND p IS NOT NULL LIMIT 5"
            rows = conn.execute(sql, params).fetchall()
            if rows:
                r = rows[0]
                result.update({
                    "price": r["p"],
                    "source": "济南信息价2026第6期(COALESCE最新)",
                    "note": f"匹配 {len(rows)} 条"
                })
                conn.close()
                return result
        except Exception:
            pass
        conn.close()

    # 3) 价目表取定单价
    conn = _connect("quota_jinan_2026.db")
    if conn:
        try:
            sql = "SELECT resource_name, resource_spec, price_tax, tax_rate FROM price_determination WHERE 1=1"
            params = []
            if name:
                sql += " AND resource_name LIKE ?"
                params.append(f"%{name}%")
            if spec:
                sql += " AND resource_spec LIKE ?"
                params.append(f"%{spec}%")
            sql += " LIMIT 5"
            rows = conn.execute(sql, params).fetchall()
            if rows:
                r = rows[0]
                result.update({
                    "price": r["price_tax"],
                    "source": "济南价目表2026(取定单价)",
                    "note": f"税率{r['tax_rate']}"
                })
                conn.close()
                return result
        except Exception:
            pass
        conn.close()

    result["note"] = "⚠️ 三库均无收录，须标注估算/询价，严禁编造"
    return result


def get_management_rate(engineering_type="安装工程", city="济南市"):
    """从 fee_rates 取费率（安装 48.08%），失败降级默认值"""
    conn = _connect("quota_reference.db")
    if conn:
        try:
            row = conn.execute(
                "SELECT management_rate, profit_rate, calculation_base FROM fee_rates WHERE engineering_type=? AND city=?",
                (engineering_type, city)).fetchone()
            conn.close()
            if row:
                return row["management_rate"] / 100.0, row["profit_rate"] / 100.0, row["calculation_base"]
        except Exception:
            pass
        conn.close()
    return DEFAULT_MGMT_RATE, DEFAULT_PROFIT_RATE, "人工费"


# ─────────────────────────── 定额匹配 ───────────────────────────

# 阀门/管件连接方式关键词 → subsection 匹配（第8册陷阱：子目名只写"公称直径(mm以内) X"）
_VALVE_CONNECTION_KEYWORDS = {
    "法兰": "法兰阀门", "对焊": "对焊阀门", "承插": "承插焊阀门",
    "螺纹": "螺纹阀门", "丝接": "螺纹阀门", "安全": "安全阀门",
    "调节": "调节阀门", "电动": "电动阀门", "液压": "液压阀门",
}
# 阀门类型泛词 → 至少匹配到阀门节
_VALVE_GENERIC = ("阀门", "蝶阀", "闸阀", "截止阀", "止回阀", "球阀", "调节阀")


def match_quota(name_keyword, spec="", volume_hint="", limit=10, connection_hint=""):
    """
    定额匹配（消耗量库 quota_items）：
      优先精确 spec + 关键词（name/section/subsection），回退 name LIKE
    适配第8册陷阱：子目 name 仅写"公称直径(mm以内) X"，阀门类型在 subsection
    返回 [{quota_no, name, spec, unit, base_price, labor_fee, work_content}]
    """
    conn = _connect("quota_consumption.db")
    if not conn:
        print("⚠️ 未找到 quota_consumption.db（山东消耗量定额库）。"
              "请设置唯一来源模式：联系作者（📧 3047871993@qq.com）获取完整数据库放入 assets/，"
              "或使用默认 LLM 推理模式（无需本地库）。", file=sys.stderr)
        return []
    rows = []
    try:
        kw = name_keyword or ""
        spec_digits = re.sub(r"\D", "", str(spec or "")) or None

        # ── 策略A：阀门/管件类，用 subsection 精确识别连接方式 ──
        # ⚠️ 仅当名称确为"阀门"类时启用连接方式推断；若只有"法兰/管件"（无阀门词），
        #    应走常规匹配命中"法兰安装"章（AZ-8-4）或"管件"章（AZ-8-2），勿误判为阀门
        is_valve_like = any(g in kw for g in _VALVE_GENERIC)
        # ⚠️ 压力等级偏好（低压/中压/高压 → section 前缀），阀门/管道/法兰都适用
        pressure_hint = None
        for p in ("低压", "中压", "高压"):
            if p in kw:
                pressure_hint = p
                break
        sub_keyword = None
        if is_valve_like:
            if connection_hint:
                for k, v in _VALVE_CONNECTION_KEYWORDS.items():
                    if k in connection_hint:
                        sub_keyword = v
                        break
            if not sub_keyword:
                for k, v in _VALVE_CONNECTION_KEYWORDS.items():
                    if k in kw:
                        sub_keyword = v
                        break

        if is_valve_like or sub_keyword:
            # ⚠️ 优先 AZ（安装工程）——工业管道蝶阀/法兰阀门必须套安装定额，
            #    市政 SZ 的"法兰阀门、分水卡子操作杆安装"是附属设施，切勿混用。
            #    注意不能靠 LIMIT 后过滤（SZ 基价小会挤掉 AZ 行），要先用 AZ 前缀限定查询
            def _query_az(prefix_filter):
                sql = "SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, section, subsection, volume_name FROM quota_items WHERE 1=1"
                params = []
                if prefix_filter:
                    sql += " AND quota_no LIKE ?"
                    params.append(prefix_filter)
                if pressure_hint:
                    # ⚠️ 压力等级映射：低压/中压/高压 对应 section 前缀 一、/二、/三、
                    #    但"一、"前缀太泛（会匹配"一、低压阀门"以外的所有"一、"节），
                    #    需同时校验 section 含压力等级词（"低压"等）
                    level_map = {"低压": "一、", "中压": "二、", "高压": "三、"}
                    sql += " AND section LIKE ? AND section LIKE ?"
                    params.extend([f"%{level_map[pressure_hint]}%", f"%{pressure_hint}%"])
                if sub_keyword:
                    sql += " AND subsection LIKE ?"
                    params.append(f"%{sub_keyword}%")
                else:
                    # 泛阀门：匹配所有阀门节（一、二、三 低压/中压/高压）
                    sql += " AND (section LIKE '%阀门%' OR subsection LIKE '%阀门%')"
                if spec_digits:
                    sql += " AND spec = ?"
                    params.append(spec_digits)
                if volume_hint:
                    sql += " AND volume_name LIKE ?"
                    params.append(f"%{volume_hint}%")
                sql += " ORDER BY base_price LIMIT ?"
                params.append(limit)
                rows2 = [dict(r) for r in conn.execute(sql, params).fetchall()]
                # ⚠️ 工业管道优先：同规格下第八册(工业管道)排最前（用户主业为工业管道/设备安装）
                rows2.sort(key=lambda r: 0 if "工业管道" in str(r.get("volume_name", "")) else 1)
                return rows2

            rows = _query_az("AZ-%")          # 先限安装工程
            if not rows:
                rows = _query_az(None)        # 回退全专业（含市政给水等）
            if rows:
                conn.close()
                return rows

        # ── 策略C：法兰/管件/管道/除锈类（无"阀门"字样），按 section 匹配 ──
        #    subsection 含材质+连接方式（如"不锈钢平焊法兰( 电弧焊)"），需忽略 304/316 等数字前缀
        elif any(w in kw for w in ("法兰", "管件", "弯头", "三通", "异径", "管帽",
                                   "管道", "钢管", "无缝钢管", "除锈", "保温", "刷油")):
            def _query_az_section(prefix_filter, section_kw):
                sql = "SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, section, subsection, volume_name FROM quota_items WHERE 1=1"
                params = []
                if prefix_filter:
                    sql += " AND quota_no LIKE ?"
                    params.append(prefix_filter)
                if pressure_hint:
                    level_map = {"低压": "一、", "中压": "二、", "高压": "三、"}
                    sql += " AND section LIKE ? AND section LIKE ?"
                    params.extend([f"%{level_map[pressure_hint]}%", f"%{pressure_hint}%"])
                sql += " AND section LIKE ?"
                params.append(f"%{section_kw}%")
                if spec_digits:
                    sql += " AND spec = ?"
                    params.append(spec_digits)
                # subsection 关键词：去材质数字（304/316/20#）与压力等级前缀（低压/中压/高压）
                # ⚠️ 管材别名：无缝钢管→碳钢管（第8册 subsection 用词）
                sub_kw = re.sub(r"\d+[#号]?", "", kw).replace("无缝钢管", "碳钢管")
                sub_kw = re.sub(r"(安装|制作|DN|PN|Φ|φ|低压|中压|高压)", " ", sub_kw)
                sub_parts = [p for p in re.split(r"[\s,，、]+", sub_kw) if len(p) >= 2]
                for part in sub_parts[:2]:
                    sql += " AND subsection LIKE ?"
                    params.append(f"%{part}%")
                sql += " ORDER BY base_price LIMIT ?"
                params.append(limit)
                return [dict(r) for r in conn.execute(sql, params).fetchall()]

            # 按优先级尝试：与关键词最相关的 section 优先（kw含"钢管"→先试"管道"，含"法兰"→先"法兰"）
            sec_priority = []
            # 具体册/节词 → 精确 section
            for w, sec in (("镀锌钢管", "镀锌钢管"), ("喷淋", "水喷淋"), ("消防", "水喷淋"),
                           ("手工除锈", "手工除锈"), ("管道", "管道"), ("钢管", "管道"),
                           ("无缝钢管", "管道"), ("法兰", "法兰"), ("管件", "管件"),
                           ("弯头", "管件"), ("三通", "管件"), ("保温", "保温"), ("刷油", "刷油")):
                if w in kw and sec not in sec_priority:
                    sec_priority.append(sec)
            for sec_kw in sec_priority + [s for s in ("法兰", "管件", "管道", "除锈", "保温", "刷油") if s not in sec_priority]:
                rows = _query_az_section("AZ-%", sec_kw)
                if rows:
                    rows.sort(key=lambda r: 0 if "工业管道" in str(r.get("volume_name", "")) else 1)
                    conn.close()
                    return rows
            # 回退：放宽 subsection 限制
            def _query_az_section_loose(prefix_filter, section_kw):
                sql = "SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, section, subsection, volume_name FROM quota_items WHERE 1=1"
                params = []
                if prefix_filter:
                    sql += " AND quota_no LIKE ?"
                    params.append(prefix_filter)
                if pressure_hint:
                    level_map = {"低压": "一、", "中压": "二、", "高压": "三、"}
                    sql += " AND section LIKE ? AND section LIKE ?"
                    params.extend([f"%{level_map[pressure_hint]}%", f"%{pressure_hint}%"])
                sql += " AND section LIKE ?"
                params.append(f"%{section_kw}%")
                if spec_digits:
                    sql += " AND spec = ?"
                    params.append(spec_digits)
                sql += " ORDER BY base_price LIMIT ?"
                params.append(limit)
                rows3 = [dict(r) for r in conn.execute(sql, params).fetchall()]
                # ⚠️ loose 结果按 subsection 与关键词匹配度排序（base_price 升序会把
                #    同规格"塑料排水管"等无关子目排前面）
                sub_parts2 = [p for p in re.split(r"[\s,，、]+",
                             re.sub(r"(安装|制作|DN|PN|Φ|φ|低压|中压|高压)", " ",
                                    kw.replace("无缝钢管", "碳钢管"))) if len(p) >= 2]
                if sub_parts2:
                    def _c_hit(r):
                        text = f"{r.get('name','')} {r.get('section','')} {r.get('subsection','')}"
                        return sum(1 for p in sub_parts2 if p in text)
                    rows3.sort(key=lambda r: -_c_hit(r))
                return rows3
            for sec_kw in sec_priority + [s for s in ("管道", "法兰", "管件", "除锈", "保温", "刷油") if s not in sec_priority]:
                rows = _query_az_section_loose("AZ-%", sec_kw)
                if rows:
                    conn.close()
                    return rows
            rows = _query_az_section_loose(None, "管道")
            if rows:
                conn.close()
                return rows

        # ── 策略B：常规名称/规格匹配 ──
        # ⚠️ 多关键词用 OR 召回（AND 太严格会导致空结果），靠 spec 精确 + 词数排序
        sql = "SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, section, subsection, volume_name FROM quota_items WHERE 1=1"
        params = []
        # 名称关键词拆分：取不含规格的实体词（去"安装/拆除"动词、DN/PN数字）
        # ⚠️ "制作"保留为搜索词（节名"一、支架制作"/"一、容器制作"等核心组成部分）
        # ⚠️ 管材同义词：第8册 subsection 用"碳钢管"表示无缝钢管（SKILL.md §七 陷阱）
        kw_alias = kw.replace("无缝钢管", "碳钢管")
        kw_clean = re.sub(r"(安装|拆除|DN\d+|PN[\d.]+|Φ[\d.]+|φ[\d.]+|1kV|0\.6)", " ", kw_alias)
        kw_parts = [p for p in re.split(r"[\s,，、]+", kw_clean) if len(p) >= 2]
        # ⚠️ 构件词拆分：长词含"风机/阀门/管道/法兰"等构件词时拆分（"离心式风机"→"离心式"+"风机"），
        #    否则整词 LIKE 匹配不到库内"离心式通( 引) 风机"等表达。左右片段都保留（"电力电缆敷设"→
        #    "电力"+"电缆"+"敷设"，勿丢"敷设"等关键区分词）
        split_parts = []
        for part in kw_parts:
            found = False
            for w in ("风机", "阀门", "管道", "法兰", "管件", "电缆", "仪表", "除锈", "保温", "刷油"):
                if len(part) > len(w) and w in part:
                    idx = part.index(w)
                    left = part[:idx].strip(" -（(）)")
                    right = part[idx+len(w):].strip(" -（(）)")
                    if left and len(left) >= 2:
                        split_parts.append(left)
                    split_parts.append(w)
                    if right and len(right) >= 2:
                        split_parts.append(right)
                    found = True
                    break
            if not found:
                split_parts.append(part)
        split_parts = list(dict.fromkeys(split_parts))
        search_parts = split_parts if len(split_parts) >= len(kw_parts) else kw_parts
        if search_parts:
            or_clauses = []
            for part in search_parts[:4]:
                or_clauses.append("(name LIKE ? OR section LIKE ? OR subsection LIKE ?)")
                params.extend([f"%{part}%", f"%{part}%", f"%{part}%"])
            sql += " AND (" + " OR ".join(or_clauses) + ")"
        elif kw:
            sql += " AND (name LIKE ? OR section LIKE ? OR subsection LIKE ?)"
            params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%"])
        if spec_digits:
            sql += " AND spec = ?"
            params.append(spec_digits)
        if volume_hint:
            sql += " AND volume_name LIKE ?"
            params.append(f"%{volume_hint}%")
        # ⚠️ 先 AND 精确（多词全部命中），无结果再 OR 回退——避免"电力/电缆/敷设"等宽词
        #    OR 召回大量无关子目（如"电力工程"），提高 precision
        def _run_b(sql_where, params2, extra_limit):
            sql2 = ("SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, "
                    "section, subsection, volume_name FROM quota_items WHERE 1=1")
            sql2 += sql_where
            if spec_digits:
                sql2 += " AND spec = ?"
                params2.append(spec_digits)
            if volume_hint:
                sql2 += " AND volume_name LIKE ?"
                params2.append(f"%{volume_hint}%")
            sql2 += " LIMIT ?"
            params2.append(extra_limit)
            return [dict(r) for r in conn.execute(sql2, params2).fetchall()]

        rows = []
        if search_parts:
            # 尝试1：AND（所有词都命中）——候选取大集再排序，避免 rowid 截断
            and_params = []
            for part in search_parts[:3]:
                and_params.extend([f"%{part}%", f"%{part}%", f"%{part}%"])
            rows = _run_b(" AND " + " AND ".join(
                ["(name LIKE ? OR section LIKE ? OR subsection LIKE ?)"] * min(3, len(search_parts))),
                and_params, limit * 10)
            # 尝试2：OR（放宽召回）
            if not rows and len(search_parts) >= 2:
                or_params = []
                for part in search_parts[:4]:
                    or_params.extend([f"%{part}%", f"%{part}%", f"%{part}%"])
                rows = _run_b(" AND (" + " OR ".join(
                    ["(name LIKE ? OR section LIKE ? OR subsection LIKE ?)"] * min(4, len(search_parts))) + ")",
                    or_params, limit * 8)
        elif kw:
            rows = _run_b(" AND (name LIKE ? OR section LIKE ? OR subsection LIKE ?)",
                          [f"%{kw}%", f"%{kw}%", f"%{kw}%"], limit)
        # 词数排序：命中词越多排越前（工业管道优先已由 volume_name 处理）
        if search_parts:
            def _hit_count(r):
                name = r.get("name", "") or ""
                sec = r.get("section", "") or ""
                sub = r.get("subsection", "") or ""
                # ⚠️ name 命中权重更高（"离心式通( 引) 风机"name 含"离心式"+"风机"=2，
                #    "离心式压缩机解体安装"name 仅含"离心式"=1，即使 section="七、冷风机"含"风机"）
                name_hits = sum(1 for p in search_parts if p in name)
                other_hits = sum(1 for p in search_parts if p in f"{sec} {sub}")
                return name_hits * 10 + other_hits
            def _section_exact(r):
                # ⚠️ 节级精确优先：section 含用户核心词完整串（"风机安装"、"支架制作"）排最前
                sec = r.get("section", "") or ""
                return 1 if any(p in sec and len(p) >= 3 for p in search_parts) else 0
            rows.sort(key=lambda r: (-_section_exact(r), -_hit_count(r),
                                     0 if "工业管道" in str(r.get("volume_name", "")) else 1))
            rows = rows[:limit]
        # ⚠️ 追加：若结果为空，退化为单关键词宽松匹配（解决"离心式风机"等拆词后 OR 仍未命中的情况）
        if not rows and kw:
            kw2 = kw.replace("无缝钢管", "碳钢管")
            # 无结果时用 2-gram 片段兜底：整词在库中不存在（如"离心式风机" vs "离心式通( 引) 风机"），
            # 拆成 2-gram 片段参与 OR（仅回退路径使用，不影响主路径召回）
            grams = []
            # ⚠️ 构件词拆分优先：把"离心式风机"拆为"离心式"+"风机"（风机/阀门/管道等构件词前后断开）
            part_words = []
            for w in ("风机", "阀门", "管道", "法兰", "管件", "电缆", "钢管", "仪表"):
                if w in kw2 and len(kw2) > len(w):
                    idx = kw2.index(w)
                    left = kw2[:idx].strip(" -（(）)")
                    if left and len(left) >= 2:
                        part_words.append(left)
                    part_words.append(w)
                    kw2 = kw2[:idx] + " " + kw2[idx:]
            for p in kw2.split():
                if len(p) >= 2:
                    grams.append(p)
                    if len(p) >= 4:
                        grams.extend(p[i:i+2] for i in range(len(p)-1))
            grams = list(dict.fromkeys(grams))[:8]
            sql2 = "SELECT id, quota_no, name, spec, unit, base_price, labor_fee, work_content, section, subsection, volume_name FROM quota_items WHERE quota_no LIKE 'AZ-%' AND ("
            clauses = []
            for g in grams:
                clauses.append("name LIKE ? OR section LIKE ? OR subsection LIKE ?")
            sql2 += " OR ".join(clauses) + ")"
            params2 = []
            for g in grams:
                params2.extend([f"%{g}%", f"%{g}%", f"%{g}%"])
            if spec_digits:
                sql2 += " AND spec = ?"
                params2.append(spec_digits)
            sql2 += " LIMIT ?"
            params2.append(limit)
            rows = [dict(r) for r in conn.execute(sql2, params2).fetchall()]
            # 2-gram 命中排序：拆词原词（"离心式"/"风机"）命中优先于 2-gram 碎片
            # ⚠️ 优先用 part_words（构件词拆分结果），退而求其次用 kw_parts
            sort_words = part_words if part_words else (kw_parts or [])
            def _g_hit(r):
                text = f"{r['name']} {r.get('section','')} {r.get('subsection','')}"
                word_hits = sum(1 for p in sort_words if len(p) >= 2 and p in text)
                gram_hits = sum(1 for g in grams if g in text)
                return word_hits * 100 + gram_hits
            rows.sort(key=lambda r: -_g_hit(r))
            rows = rows[:limit]
    except Exception as e:
        print(f"⚠️ 定额匹配异常: {e}", file=sys.stderr)
    conn.close()
    return rows


def get_consumptions(quota_id):
    """
    获取定额消耗量明细。
    ⚠️ 主材识别规则（SKILL.md §七）：
      - consumption>0 的常规材料正常返回
      - is_unpriced=1 或 is_main_material=1 的材料即使 consumption=0 也保留（未计价主材/螺栓等，须另计）
      - 名称含 阀门/法兰/管件/弯头/钢管/电缆 等构件词且 consumption=0 的资源 → 标记为主材候选（另计）
    返回 [{resource_name, resource_spec, resource_unit, consumption, is_unpriced, is_main_material, main_candidate}]
    """
    conn = _connect("quota_consumption.db")
    if not conn:
        return []
    rows = []
    try:
        sql = """SELECT resource_name, resource_spec, resource_unit, consumption, is_unpriced, is_main_material
                 FROM consumptions WHERE quota_id=?
                 ORDER BY resource_type"""
        all_rows = [dict(r) for r in conn.execute(sql, (quota_id,)).fetchall()]
        main_word = ("阀门", "法兰", "管件", "弯头", "三通", "钢管", "管道", "电缆", "接头",
                     "蝶阀", "闸阀", "截止阀", "止回阀", "软管", "补偿器")
        for r in all_rows:
            name = r.get("resource_name") or ""
            cons = r.get("consumption") or 0
            unpriced = r.get("is_unpriced") or 0
            is_main = r.get("is_main_material") or 0
            main_cand = 0
            if cons > 0:
                rows.append(r)                       # 常规消耗
            elif unpriced or is_main:
                r["main_candidate"] = 1              # 未计价主材（螺栓/法兰等）
                r["consumption"] = cons
                rows.append(r)
            elif any(w in name for w in main_word):
                r["main_candidate"] = 1              # 构件主材 consumption=0 → 另计候选
                r["consumption"] = cons
                rows.append(r)
    except Exception as e:
        print(f"⚠️ 消耗量查询异常: {e}", file=sys.stderr)
    conn.close()
    return rows


# ─────────────────────────── Step0 单位比对 ───────────────────────────

UNIT_CONVERSION = {
    ("10m", "m"): 0.1, ("100m", "m"): 0.01, ("10m²", "m²"): 0.1,
    ("100m²", "m²"): 0.01, ("10个", "个"): 0.1, ("100个", "个"): 0.01,
    ("100kg", "kg"): 0.01, ("10kg", "kg"): 0.1,
    ("10m³", "个"): "volume/10", ("10m³", "项"): "volume/10",
}
EQUIVALENT_UNITS = {("处", "个"), ("台", "个"), ("套", "个"), ("副", "副"), ("m", "m"),
                    ("个", "个"), ("米", "m"), ("kg", "kg"), ("t", "t"),
                    ("片", "片"), ("只", "只"), ("张", "张")}
# 1副法兰=2片（SKILL.md §六/材料匹配：片→副 ×2）
UNIT_CONVERSION.update({("副", "片"): 0.5, ("片", "副"): 2.0})


def unit_check(list_unit, quota_unit):
    """
    Step0 单位比对：返回 (折算系数, 提示)
      - 一致/等价 → 1.0
      - 可换算 → 固定系数
      - 10m³/个 → 需体积折算（特殊标记）
      - 不可换算 → None（提醒人工）
    """
    lu = (list_unit or "").strip()
    qu = (quota_unit or "").strip()
    if not lu or not qu:
        return 1.0, "单位信息不全，按1:1处理"
    if lu == qu:
        return 1.0, "单位一致"
    if (lu, qu) in EQUIVALENT_UNITS or (qu, lu) in EQUIVALENT_UNITS:
        return 1.0, f"等价单位 {lu}↔{qu}，按1:1"
    if (qu, lu) in UNIT_CONVERSION:
        v = UNIT_CONVERSION[(qu, lu)]
        if v == "volume/10":
            return None, f"⚠️ {qu}→{lu} 需体积折算（从规格提取长×宽×厚，体积÷10）"
        return v, f"{qu}→{lu} 折算系数×{v}"
    if (lu, qu) in UNIT_CONVERSION:
        v = UNIT_CONVERSION[(lu, qu)]
        if v == "volume/10":
            return None, f"⚠️ {lu}→{qu} 需体积折算"
        return 1 / v, f"{lu}→{qu} 折算系数×{1/v}"
    return None, f"⚠️ 单位 {lu} vs {qu} 无法自动换算，须人工确认"


# ─────────────────────────── 清单特征解析 ───────────────────────────

def _parse_rule(text):
    """规则解析（无LLM时的降级）：提取 名称/规格DN/数量/单位"""
    name, spec, qty, unit = text.strip(), "", 1, "个"
    # 数量+单位
    m = re.search(r"(\d+(?:\.\d+)?)\s*(个|台|套|副|米|m|处|项|kg|t|根|支|片|组)", text)
    if m:
        qty = float(m.group(1))
        unit = m.group(2)
        name = text[:m.start()].strip()
    # 规格 DN/PN/Φ
    m = re.search(r"(DN\s*\d+|PN\s*[\d.]+|Φ\s*[\d.]+|\d{2,4})", text)
    if m:
        spec = m.group(1).replace(" ", "").upper()
    return {"name": name or text, "spec": spec, "qty": qty, "unit": unit}


def parse_list_item(text, use_llm=True):
    """
    清单特征解析：
      LLM（hy3-preview，TokenHub）→ {名称, 规格, 数量, 单位, 专业, 特征}
      失败/无Key → 规则降级
    """
    # LLM 路径（环境变量就绪时才尝试）
    api_key = os.environ.get("HUNYUAN_API_KEY", "")
    if use_llm and api_key:
        try:
            import requests
            prompt = f"""你是造价清单解析器。从清单描述提取结构化JSON，仅输出JSON：
{{
  "名称": "法兰蝶阀安装",
  "规格": "DN200",
  "数量": 10,
  "单位": "个",
  "专业": "安装工程",
  "特征": "碳钢、法兰连接"
}}
清单描述：{text}"""
            resp = requests.post(
                os.environ.get("HUNYUAN_URL", "https://tokenhub.tencentmaas.com/v1/chat/completions"),
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": os.environ.get("HUNYUAN_MODEL", "hy3-preview"),
                      "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.1, "max_tokens": 300},
                timeout=30)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                m = re.search(r"\{.*\}", content, re.S)
                if m:
                    data = json.loads(m.group(0))
                    return {
                        "name": data.get("名称") or data.get("name") or "",
                        "spec": data.get("规格") or data.get("spec") or "",
                        "qty": float(data.get("数量") or data.get("qty") or 1),
                        "unit": data.get("单位") or data.get("unit") or "个",
                        "major": data.get("专业") or "安装工程",
                        "feature": data.get("特征") or "",
                        "llm": True,
                    }
        except Exception:
            pass  # 降级规则
    r = _parse_rule(text)
    r["major"] = "安装工程"
    r["feature"] = ""
    r["llm"] = False
    return r


# ─────────────────────────── 主流程：自动组价 ───────────────────────────

def compose_quota(text, use_llm=True, spec_override=None, qty_override=None, unit_override=None):
    """
    自动组价主流程：
      text → 解析 → 定额匹配 → 消耗量 → 三级查价 → Step0 → 组价 AD
    返回完整 JSON
    """
    parsed = parse_list_item(text, use_llm=use_llm)
    if spec_override:
        parsed["spec"] = spec_override
    if qty_override:
        parsed["qty"] = float(qty_override)
    if unit_override:
        parsed["unit"] = unit_override

    mgmt_rate, profit_rate, calc_base = get_management_rate(parsed.get("major", "安装工程"))

    # 1) 定额匹配（connection_hint 从名称/特征推断连接方式，适配第8册 subsection 陷阱）
    conn_hint = (parsed.get("feature") or "") + parsed["name"]
    candidates = match_quota(parsed["name"], spec=parsed["spec"],
                             connection_hint=conn_hint, limit=8)
    if not candidates:
        return {"ok": False, "error": f"未匹配到定额: {parsed['name']} {parsed['spec']}",
                "parsed": parsed}

    # 取第一个为主定额，剩余为候选
    main = candidates[0]
    consumes = get_consumptions(main["id"])

    # 2) Step0 单位比对
    factor, unit_note = unit_check(parsed["unit"], main["unit"])

    # 3) 主材三级查价 + 组价明细
    # ⚠️ 主材查价名推断：定额主材常为泛称（"法兰阀门"），用清单构件词（"蝶阀"）查价更准
    part_name = parsed["name"]
    for w in ("蝶阀", "闸阀", "截止阀", "止回阀", "球阀", "调节阀", "安全阀", "阀门"):
        if w in part_name:
            part_name = w
            break
    main_materials = []   # is_unpriced=1 / is_main_material=1 / 构件主材（另计）
    aux_materials = []    # 已计价辅材（消耗量×含价，含在基价内）
    for c in consumes:
        main_cand = c.get("main_candidate") or c.get("is_unpriced") == 1 or c.get("is_main_material") == 1
        # ⚠️ 未计价主材 consumption=0 → 按清单量 1:1 计（阀门/法兰/管件等构件主材）
        eff_cons = c["consumption"] if (c["consumption"] or 0) > 0 else (1.0 if main_cand else 0)
        # 查价名：构件主材泛称（法兰阀门）→ 用清单构件词；螺栓类 → 名称+型号更精确
        lookup_name = c["resource_name"]
        if main_cand and c["resource_name"] in ("法兰阀门", "阀门", "法兰", "管件") and part_name:
            lookup_name = part_name
        price_info = lookup_price_3tier(lookup_name, c.get("resource_spec", ""))
        item = {
            "resource_name": c["resource_name"],
            "lookup_name": lookup_name,
            "resource_spec": c.get("resource_spec", ""),
            "unit": c.get("resource_unit", ""),
            "consumption": eff_cons,
            "is_unpriced": c.get("is_unpriced", 0),
            "is_main_material": c.get("is_main_material", 0),
            "main_candidate": 1 if main_cand else 0,
            "price": price_info["price"],
            "price_source": price_info["source"],
            "price_note": price_info["note"],
            "amount": round(eff_cons * (price_info["price"] or 0), 2) if price_info["price"] else None,
        }
        if main_cand:
            main_materials.append(item)
        else:
            aux_materials.append(item)

    # 4) 组价计算
    labor = main.get("labor_fee") or 0
    base = main.get("base_price") or 0
    management_fee = labor * mgmt_rate
    material_cost = sum(m["amount"] for m in main_materials if m["amount"])
    # 已计价辅材在基价内，不再叠加
    ad_unit = base + management_fee          # 安装单价AD（不含利润税金，主材另计）
    ad_unit_with_main = ad_unit + material_cost   # 含主材
    # 综合单价（含利润+税金，供参考口径：税前=AD+利润，含税=税前×1.09）
    profit = (base + management_fee) * profit_rate
    tax_included = (ad_unit_with_main + profit) * 1.09

    # 折算到清单单位
    if factor:
        ad_total = ad_unit * parsed["qty"] * factor
        main_cost_total = material_cost * parsed["qty"] * factor
    else:
        ad_total = None
        main_cost_total = None

    result = {
        "ok": True,
        "parsed": parsed,
        "llm_used": parsed.get("llm", False),
        "quota": {
            "quota_no": main["quota_no"],
            "name": main["name"],
            "spec": main["spec"],
            "unit": main["unit"],
            "base_price": base,
            "labor_fee": labor,
            "work_content": (main.get("work_content") or "")[:200],
            "section": main.get("section", ""),
            "subsection": main.get("subsection", ""),
        },
        "step0": {"factor": factor, "note": unit_note,
                  "list_unit": parsed["unit"], "quota_unit": main["unit"]},
        "rate": {"management_rate": round(mgmt_rate * 100, 2), "profit_rate": round(profit_rate * 100, 2),
                 "calculation_base": calc_base},
        "pricing": {
            "management_fee": round(management_fee, 2),
            "main_material_cost": round(material_cost, 2),
            "ad_unit": round(ad_unit, 2),                 # 安装单价AD（清单单位，未乘数量）
            "ad_unit_with_main": round(ad_unit_with_main, 2),
            "profit": round(profit, 2),
            "tax_included": round(tax_included, 2),       # 含税综合单价（参考）
            "ad_total": round(ad_total, 2) if ad_total else None,
            "main_cost_total": round(main_cost_total, 2) if main_cost_total else None,
            "qty": parsed["qty"],
            "unit_factor": factor,
        },
        "main_materials": main_materials,
        "aux_materials_count": len(aux_materials),
        "candidates_count": len(candidates),
        "candidates": [{"quota_no": c["quota_no"], "name": c["name"], "spec": c["spec"],
                        "unit": c["unit"], "base_price": c["base_price"]} for c in candidates],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return result


# ─────────────────────────── CLI ───────────────────────────

def main():
    args = sys.argv[1:]
    use_llm = "--no-llm" not in args
    json_mode = "--json" in args
    spec = qty = unit = None
    if "--spec" in args:
        spec = args[args.index("--spec") + 1]
    if "--qty" in args:
        qty = args[args.index("--qty") + 1]
    if "--unit" in args:
        unit = args[args.index("--unit") + 1]

    if json_mode:
        idx = args.index("--json")
        data = json.loads(args[idx + 1])
        text = data.get("name", "") + " " + data.get("spec", "")
        spec = spec or data.get("spec")
        qty = qty or data.get("qty")
        unit = unit or data.get("unit")
    else:
        texts = [a for a in args if not a.startswith("--")]
        if not texts:
            print(__doc__)
            sys.exit(1)
        text = " ".join(texts)

    result = compose_quota(text, use_llm=use_llm, spec_override=spec,
                           qty_override=qty, unit_override=unit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
