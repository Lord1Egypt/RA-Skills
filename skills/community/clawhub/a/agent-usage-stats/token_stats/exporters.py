"""Export token statistics to XLSX, CSV, and JSON."""

from __future__ import annotations

import json
import os
from datetime import datetime
import zipfile
import xml.etree.ElementTree as ET

from .pricing import calc_cost, calc_total_cost, fmt_total_cost, get_model_price, to_cny
from .formatting import is_total_mode, skip_model


# ═══════════════════════════════════════════════════
#  导出 — 纯 stdlib XLSX 写入器 + 交互式导出函数
# ═══════════════════════════════════════════════════

_METRIC_LABELS = {'input': '输入', 'output': '输出', 'cache': '缓存',
                  'cache_ratio': '缓存率', 'calls': '调用',
                  'total': '总计', 'total_with_cache': '总计(含缓存)',
                  'cost': '预估费用'}
_METRIC_ORDER = ['input', 'output', 'cache', 'cache_ratio', 'calls', 'total', 'total_with_cache', 'cost']

_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', _NS)


def _xml_tag(tag):
    return f'{{{_NS}}}{tag}'


class _XLSXWriter:
    """纯 stdlib XLSX 写入器。"""

    def __init__(self):
        self.sheets = {}
        self.col_widths = {}
        self.merges = {}
        self.freezes = {}
        self._strings = []
        self._str_idx = {}

    def _add_str(self, s):
        s = str(s)
        if s not in self._str_idx:
            self._str_idx[s] = len(self._strings)
            self._strings.append(s)
        return self._str_idx[s]

    def add_sheet(self, name, col_widths=None, merges=None, freeze=None):
        name = name[:31]
        self.sheets[name] = []
        if col_widths:
            self.col_widths[name] = col_widths
        if merges:
            self.merges[name] = merges
        if freeze:
            self.freezes[name] = freeze

    def add_row(self, sheet, values):
        self.sheets[sheet].append(values)

    def _col_letter(self, n):
        s = ''
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s

    def _build_styles_xml(self):
        fonts_el = ET.Element(_xml_tag('fonts'), count='3')
        ET.SubElement(fonts_el, _xml_tag('font'))
        fb = ET.SubElement(fonts_el, _xml_tag('font'))
        ET.SubElement(fb, _xml_tag('b'))
        ET.SubElement(fb, _xml_tag('color'), rgb='FFFFFFFF')
        fb2 = ET.SubElement(fonts_el, _xml_tag('font'))
        ET.SubElement(fb2, _xml_tag('b'))
        fills_el = ET.Element(_xml_tag('fills'), count='5')
        ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(ET.SubElement(fills_el, _xml_tag('fill')), _xml_tag('patternFill'), patternType='gray125')
        fh = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(fh, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FF4472C4'))
        ft = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(ft, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FFD9E2F3'))
        fg = ET.SubElement(fills_el, _xml_tag('fill'))
        ET.SubElement(fg, _xml_tag('patternFill'), patternType='solid').append(
            ET.Element(_xml_tag('fgColor'), rgb='FFF2F2F2'))
        borders_el = ET.Element(_xml_tag('borders'), count='1')
        ET.SubElement(borders_el, _xml_tag('border'))
        style_xml = ET.Element(_xml_tag('styleSheet'))
        style_xml.append(fonts_el)
        style_xml.append(fills_el)
        style_xml.append(borders_el)
        ET.SubElement(style_xml, _xml_tag('cellStyleXfs'), count='1').append(
            ET.Element(_xml_tag('xf'), numFmtId='0', fontId='0', fillId='0', borderId='0'))
        xfs = ET.SubElement(style_xml, _xml_tag('cellXfs'), count='5')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='0', fillId='0', borderId='0', xfId='0')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='1', fillId='2', borderId='0', xfId='0', applyFont='1', applyFill='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='2', fillId='3', borderId='0', xfId='0', applyFont='1', applyFill='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='2', fillId='0', borderId='0', xfId='0', applyFont='1')
        ET.SubElement(xfs, _xml_tag('xf'), numFmtId='0', fontId='0', fillId='4', borderId='0', xfId='0', applyFill='1')
        return ET.tostring(style_xml, encoding='utf-8', xml_declaration=True)

    def _build_shared_strings_xml(self):
        sst = ET.Element(_xml_tag('sst'), count=str(len(self._strings)),
                         uniqueCount=str(len(self._strings)))
        for s in self._strings:
            si = ET.SubElement(sst, _xml_tag('si'))
            ET.SubElement(si, _xml_tag('t')).text = s
        return ET.tostring(sst, encoding='utf-8', xml_declaration=True)

    def _build_sheet_xml(self, name):
        ws = ET.Element(_xml_tag('worksheet'))
        rows = self.sheets[name]
        if name in self.col_widths:
            cols_el = ET.SubElement(ws, _xml_tag('cols'))
            for letter, width in sorted(self.col_widths[name].items()):
                col_num = 0
                for ch in letter:
                    col_num = col_num * 26 + (ord(ch.upper()) - 64)
                ET.SubElement(cols_el, _xml_tag('col'), min=str(col_num), max=str(col_num),
                              width=str(width), customWidth='1')
        sd = ET.SubElement(ws, _xml_tag('sheetData'))
        for row_idx, row_data in enumerate(rows, 1):
            row_el = ET.SubElement(sd, _xml_tag('row'), r=str(row_idx))
            for col_idx, item in enumerate(row_data, 1):
                val, style = item if isinstance(item, tuple) else (item, 0)
                ref = f'{self._col_letter(col_idx)}{row_idx}'
                if isinstance(val, str):
                    idx = self._add_str(val)
                    v_el = ET.Element(_xml_tag('v'))
                    v_el.text = str(idx)
                    ET.SubElement(row_el, _xml_tag('c'), r=ref, t='s', s=str(style)).append(v_el)
                elif isinstance(val, (int, float)):
                    v_el = ET.Element(_xml_tag('v'))
                    v_el.text = str(int(val))
                    ET.SubElement(row_el, _xml_tag('c'), r=ref, s=str(style)).append(v_el)
        if name in self.merges:
            mc_el = ET.SubElement(ws, _xml_tag('mergeCells'), count=str(len(self.merges[name])))
            for r1, c1, r2, c2 in self.merges[name]:
                ref = f'{self._col_letter(c1)}{r1}:{self._col_letter(c2)}{r2}'
                ET.SubElement(mc_el, _xml_tag('mergeCell'), ref=ref)
        if name in self.freezes:
            fp = self.freezes[name]
            sv = ET.SubElement(ws, _xml_tag('sheetViews'))
            sv_el = ET.SubElement(sv, _xml_tag('sheetView'), tabSelected='1', workbookViewId='0')
            pane_el = ET.SubElement(sv_el, _xml_tag('pane'))
            cl = ''.join(c for c in fp if c.isalpha())
            rn = int(''.join(c for c in fp if c.isdigit()))
            pane_el.set('ySplit', str(rn - 1))
            pane_el.set('topLeftCell', fp)
            pane_el.set('activePane', 'bottomRight')
            pane_el.set('state', 'frozen')
        return ET.tostring(ws, encoding='utf-8', xml_declaration=True)

    def save(self, filepath):
        # 安全检查：确保有数据可写
        for name, rows in self.sheets.items():
            if not rows:
                raise ValueError(f"Sheet \"{name}\" 没有数据行，请先调用 add_row()")
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            ct_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                      '<Default Extension="xml" ContentType="application/xml"/>'
                      '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>')
            for name in list(self.sheets.keys()):
                safe = name.replace(' ', '')
                ct_xml += f'<Override PartName="/xl/worksheets/{safe}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            ct_xml += ('<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                       '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
                       '</Types>')
            zf.writestr('[Content_Types].xml', ct_xml)
            zf.writestr('_rels/.rels',
                        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                        '</Relationships>')
            wb_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                      '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
                      ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>')
            for i, name in enumerate(self.sheets.keys(), 1):
                safe = name.replace(' ', '')
                wb_xml += f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>'
            wb_xml += '</sheets></workbook>'
            zf.writestr('xl/workbook.xml', wb_xml)
            rels_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">')
            for i, name in enumerate(self.sheets.keys(), 1):
                safe = name.replace(' ', '')
                rels_xml += f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/{safe}.xml"/>'
            rels_xml += ('<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                         '<Relationship Id="rIdStrings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
                         '</Relationships>')
            zf.writestr('xl/_rels/workbook.xml.rels', rels_xml)
            zf.writestr('xl/styles.xml', self._build_styles_xml())
            # 先构建所有 sheet XML（填充 shared strings）
            sheet_xmls = {}
            for name in self.sheets.keys():
                safe = name.replace(' ', '')
                sheet_xmls[safe] = self._build_sheet_xml(name)
            # 再写 shared strings（此时已填充完毕）
            zf.writestr('xl/sharedStrings.xml', self._build_shared_strings_xml())
            # 最后写 sheet XML
            for safe, sxml in sheet_xmls.items():
                zf.writestr(f'xl/worksheets/{safe}.xml', sxml)
        # 写入后检查文件大小
        try:
            fsize = os.path.getsize(filepath)
            if fsize < 200:
                print(f"⚠️ 警告: 导出文件异常小 ({fsize} bytes)，可能缺少数据")
        except Exception:
            pass


HDR_STYLE = 1  # 白字蓝底
TOT_STYLE = 2  # 加粗蓝底


def get_price(model: str, project_root: str):
    return get_model_price(model, _load_prices(project_root))


def _load_prices(project_root: str) -> dict:
    from .pricing import load_model_prices
    return load_model_prices(project_root, os.getcwd())


def calc_total_cost_for_models(per_model_list: list, project_root: str) -> dict[str, float]:
    return calc_total_cost(per_model_list, lambda model: get_price(model, project_root))


def calc_cache_rate(inp: int, cache: int) -> float | None:
    if cache <= 0 or inp <= 0:
        return None
    if cache > inp:
        return cache / (cache + inp) * 100
    return cache / inp * 100


def _pm_total(pm: dict) -> int:
    return int(pm.get('input', 0) or 0) + int(pm.get('output', 0) or 0)


def _cost_for_pm(pm: dict, project_root: str) -> str:
    if is_total_mode(pm):
        return "-"
    inp = int(pm.get('input', 0) or 0)
    out = int(pm.get('output', 0) or 0)
    cache = int(pm.get('cache', 0) or 0)
    pc = get_price(pm.get('model', 'unknown'), project_root)
    if not pc:
        return "-"
    cost_val = calc_cost(inp, out, cache, pc)
    return f"≈¥{to_cny(cost_val, pc.get('currency', 'CNY')):.4f}"


def _print_pm_detail(pm: dict, fmt_num, indent: str = "    "):
    inp = pm.get("input", 0) or 0
    out = pm.get("output", 0) or 0
    cache = pm.get("cache", 0) or 0
    calls = pm.get("calls", 0) or 0
    total_tok = inp + out
    total_w_cache = total_tok + cache
    if is_total_mode(pm):
        print(f"{indent}总计 tokens     {fmt_num(total_tok):>8}")
        print(f"{indent}调用次数        {calls} 次")
        print(f"{indent}─────────────────────────────────────")
        print(f"{indent}总计            {fmt_num(total_tok)}")
        return
    print(f"{indent}输入 tokens     {fmt_num(inp):>8}")
    print(f"{indent}输出 tokens     {fmt_num(out):>8}")
    print(f"{indent}缓存 tokens     {fmt_num(cache):>8}")
    print(f"{indent}调用次数        {calls} 次")
    print(f"{indent}─────────────────────────────────────")
    print(f"{indent}总计/+缓存     {fmt_num(total_tok)}/{fmt_num(total_w_cache)}")


def _write_xlsx_simple(filepath, agent_name, agent_display, filtered_models, project_root):
    """单 Agent 简单 XLSX（含 Agent 列 + 合并单元格 + 合计行）。"""
    wb = _XLSXWriter()
    col_widths = {'A': 18, 'B': 22}
    for i in range(3, 9):
        col_widths[wb._col_letter(i)] = 16
    merges = []
    wb.add_sheet(agent_display, col_widths=col_widths, merges=merges, freeze='C2')
    headers = ['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用']
    wb.add_row(agent_display, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    ms = row_num
    for pm in filtered_models:
        inp = int(pm.get('input', 0))
        out = int(pm.get('output', 0))
        cache = int(pm.get('cache', 0))
        calls = int(pm.get('calls', 0))
        model = pm.get('model', 'unknown')
        cr = calc_cache_rate(inp, cache)
        cr_str = f"{cr:.1f}%" if cr is not None else "-"
        cost_str = _cost_for_pm(pm, project_root)
        wb.add_row(agent_display, [agent_display, model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cost_str])
        row_num += 1
    if filtered_models:
        merges.append((ms, 1, row_num - 1, 1))
    # 多模型时展示 Agent 合计（单模型则跳过，避免重复）
    if len(filtered_models) > 1:
        ti = int(sum(pm.get('input', 0) for pm in filtered_models))
        to = int(sum(pm.get('output', 0) for pm in filtered_models))
        tc = int(sum(pm.get('cache', 0) for pm in filtered_models))
        tca = int(sum(pm.get('calls', 0) for pm in filtered_models))
        tcr = calc_cache_rate(ti, tc)
        tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
        tcost_str = fmt_total_cost(calc_total_cost_for_models(filtered_models, project_root))
        tcost_str = f"{tcost_str} (仅供参考)" if tcost_str else "-"
        wb.add_row(agent_display, [
            (f'{agent_display} 合计', TOT_STYLE), ('', TOT_STYLE), (ti, TOT_STYLE), (to, TOT_STYLE),
            (tc, TOT_STYLE), (tcr_str, TOT_STYLE), (tca, TOT_STYLE),
            (ti + to, TOT_STYLE), (ti + to + tc, TOT_STYLE), (tcost_str, TOT_STYLE)])
    wb.merges[agent_display] = merges
    wb.save(filepath)


def _write_xlsx_multi_simple(filepath, results, project_root):
    """多 Agent 简单 XLSX（Agent 列合并单元格 + 每个 Agent 单独合计 + 总合计）。"""
    wb = _XLSXWriter()
    col_widths = {'A': 18, 'B': 22}
    for i in range(3, 9):
        col_widths[wb._col_letter(i)] = 16
    merges = []
    wb.add_sheet('MultiAgent', col_widths=col_widths, merges=merges, freeze='C2')
    headers = ['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用']
    wb.add_row('MultiAgent', [(h, HDR_STYLE) for h in headers])
    row_num = 2
    grand_ti = grand_to = grand_tc = grand_tca = 0
    grand_cost = 0.0
    total_agents = 0
    for agent, data in results:
        agent_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]
        if not agent_models:
            continue
        total_agents += 1
        ms = row_num
        ti = to = tc = tca = 0
        at_cost = 0.0
        for pm in agent_models:
            inp = int(pm.get('input', 0))
            out = int(pm.get('output', 0))
            cache = int(pm.get('cache', 0))
            calls = int(pm.get('calls', 0))
            model = pm.get('model', 'unknown')
            cr = calc_cache_rate(inp, cache)
            cr_str = f"{cr:.1f}%" if cr is not None else "-"
            cs = _cost_for_pm(pm, project_root)
            if cs.startswith("≈¥"):
                at_cost += float(cs[2:])
            wb.add_row('MultiAgent', [agent.display_name(), model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
            ti += inp; to += out; tc += cache; tca += calls
            row_num += 1
        merges.append((ms, 1, row_num - 1, 1))
        # 多模型时展示 Agent 合计
        if len(agent_models) > 1:
            tcr = calc_cache_rate(ti, tc)
            tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
            at_cs = f"≈¥{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
            wb.add_row('MultiAgent', [
                (f'{agent.display_name()} 合计', TOT_STYLE), ('', TOT_STYLE), (ti, TOT_STYLE),
                (to, TOT_STYLE), (tc, TOT_STYLE), (tcr_str, TOT_STYLE), (tca, TOT_STYLE),
                (ti + to, TOT_STYLE), (ti + to + tc, TOT_STYLE), (at_cs, TOT_STYLE)])
            row_num += 1
        grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
        grand_cost += at_cost
    # 全部总计
    if total_agents > 1:
        gtt = grand_ti + grand_to
        gtcr = calc_cache_rate(grand_ti, grand_tc)
        gtcr_str = f"{gtcr:.1f}%" if gtcr is not None else "-"
        gcs = f"≈¥{grand_cost:.4f} (仅供参考)" if grand_cost > 0 else "-"
        wb.add_row('MultiAgent', [
            ('全部总计', TOT_STYLE), ('', TOT_STYLE), (grand_ti, TOT_STYLE),
            (grand_to, TOT_STYLE), (grand_tc, TOT_STYLE), (gtcr_str, TOT_STYLE), (grand_tca, TOT_STYLE),
            (gtt, TOT_STYLE), (gtt + grand_tc, TOT_STYLE), (gcs, TOT_STYLE)])
    wb.merges['MultiAgent'] = merges
    wb.save(filepath)


def _write_xlsx_monthly(filepath, agent_name, agent_display, monthly_data, all_months):
    """单 Agent 年度 XLSX，按月拆分列，含 Agent 列合并 + 合计。"""
    wb = _XLSXWriter()
    month_count = len(all_months)
    all_models = sorted({m for d in monthly_data.values() for m in d})
    # A=Agent, B=Model, C=Metric, then months, then 合计
    col_widths = {'A': 18, 'B': 22, 'C': 14}
    for i in range(month_count):
        col_widths[wb._col_letter(4 + i)] = 16
    col_widths[wb._col_letter(4 + month_count)] = 16
    merges = []
    wb.add_sheet(agent_display, col_widths=col_widths, merges=merges, freeze='D2')
    headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
    wb.add_row(agent_display, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    ag_ms = row_num  # agent merge start
    for model in all_models:
        ms = row_num
        for metric in _METRIC_ORDER:
            vals = [
                ('' if (model == all_models[0] and metric == 'input') else '', 0),
                ('' if metric != 'input' else model, 0),
                (_METRIC_LABELS[metric], 0)]
            tot = 0
            for m_label in all_months:
                md = monthly_data[m_label].get(model, {})
                if metric == 'total':
                    v = md.get('input', 0) + md.get('output', 0)
                elif metric == 'total_with_cache':
                    v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                else:
                    v = md.get(metric, 0)
                tot += v
                vals.append((v if metric != "cost" else (f"≈¥{v:.4f}" if v else "0"), 0))
            vals.append((tot if metric != "cost" else (f"≈¥{tot:.4f}" if tot else "0"), 0))
            wb.add_row(agent_display, vals)
            row_num += 1
        merges.append((ms, 2, row_num - 1, 2))  # Model merge
    if all_models:
        merges.append((ag_ms, 1, row_num - 1, 1))  # Agent merge
    # 多模型时展示合计（单模型跳过避免重复）
    if len(all_models) > 1:
        gt = row_num
        for metric in _METRIC_ORDER:
            vals = [
                ('' if metric != 'input' else f'{agent_display} 合计', TOT_STYLE),
                ('' if metric != 'input' else '合计', TOT_STYLE),
                (_METRIC_LABELS[metric], TOT_STYLE)]
            gt_all = 0
            for m_label in all_months:
                ct = 0
                for model in all_models:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        ct += md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        ct += md.get(metric, 0)
                gt_all += ct
                vals.append((ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"), TOT_STYLE))
            vals.append((gt_all if metric != "cost" else (f"≈¥{gt_all:.4f}" if gt_all else "0"), TOT_STYLE))
            wb.add_row(agent_display, vals)
            row_num += 1
        merges.append((gt, 1, row_num - 1, 1))
    wb.merges[agent_display] = merges
    wb.save(filepath)


def _write_xlsx_multi_monthly(filepath, agents_monthly, all_months, agent_order):
    """多 Agent 年度 XLSX，全部 Agent 在一个 Sheet，含每个 Agent 单独合计 + 总合计。"""
    wb = _XLSXWriter()
    month_count = len(all_months)
    col_widths = {'A': 18, 'B': 22, 'C': 14}
    for i in range(month_count):
        col_widths[wb._col_letter(4 + i)] = 16
    col_widths[wb._col_letter(4 + month_count)] = 16
    merges = []
    sheet_name = 'YearlyStats'
    wb.add_sheet(sheet_name, col_widths=col_widths, merges=merges, freeze='D2')
    headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
    # 手动管理行列表，避免插入时行号计算错误
    rows_data = []  # [(row_values, row_type), ...]
    for agent_name, agent_display, monthly_data in agent_order:
        all_models = sorted({m for d in monthly_data.values() for m in d})
        if not all_models:
            continue
        for model in all_models:
            for metric in _METRIC_ORDER:
                vals = [
                    ('' if metric != 'input' else agent_display, 0),
                    ('' if metric != 'input' else model, 0),
                    (_METRIC_LABELS[metric], 0)]
                tot = 0
                for m_label in all_months:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        v = md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        v = md.get(metric, 0)
                    tot += v
                    vals.append((v if metric != "cost" else (f"≈¥{v:.4f}" if v else "0"), 0))
                vals.append((tot if metric != "cost" else (f"≈¥{tot:.4f}" if tot else "0"), 0))
                rows_data.append((vals, 'data', agent_name, agent_display, model))
        # 多模型时展示 Agent 合计
        if len(all_models) > 1:
            for metric in _METRIC_ORDER:
                vals = [
                    ('' if metric != 'input' else f'{agent_display} 合计', TOT_STYLE),
                    ('' if metric != 'input' else '合计', TOT_STYLE),
                    (_METRIC_LABELS[metric], TOT_STYLE)]
                ag_total = 0
                for m_label in all_months:
                    ct = 0
                    for model in all_models:
                        md = monthly_data[m_label].get(model, {})
                        if metric == 'total':
                            ct += md.get('input', 0) + md.get('output', 0)
                        elif metric == 'total_with_cache':
                            ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                        else:
                            ct += md.get(metric, 0)
                    ag_total += ct
                    vals.append((ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"), TOT_STYLE))
                vals.append((ag_total if metric != "cost" else (f"≈¥{ag_total:.4f}" if ag_total else "0"), TOT_STYLE))
                rows_data.append((vals, 'agent_subtotal', agent_name, agent_display, None))

    # 写入 header
    wb.add_row(sheet_name, [(h, HDR_STYLE) for h in headers])
    row_num = 2
    # 追踪 merge ranges：数据行 Agent+Model、合计行 Agent+Model
    agent_ranges = {}  # agent_name -> (start_row, end_row) — 仅数据行
    model_ranges = {}  # (agent_name, model) -> (start_row, end_row)
    subtotal_agent_ranges = {}  # agent_name -> (start_row, end_row) — 合计行 Agent 列
    subtotal_model_ranges = {}  # agent_name -> (start_row, end_row) — 合计行 Model 列
    current_agent = None
    current_model = None
    agent_start = None
    model_start = None

    subtotal_start = None
    subtotal_agent = None

    def _close_data_ranges():
        nonlocal current_agent, current_model, agent_start, model_start
        if current_agent is not None:
            agent_ranges[current_agent] = (agent_start, row_num - 1)
        if current_model is not None and current_agent is not None:
            model_ranges[(current_agent, current_model)] = (model_start, row_num - 1)

    def _close_subtotal_ranges():
        nonlocal subtotal_agent, subtotal_start
        if subtotal_agent is not None and subtotal_start is not None:
            subtotal_agent_ranges[subtotal_agent] = (subtotal_start, row_num - 1)
            subtotal_model_ranges[subtotal_agent] = (subtotal_start, row_num - 1)
            subtotal_agent = None
            subtotal_start = None

    for vals, rtype, ag_name, ag_display, model in rows_data:
        wb.add_row(sheet_name, vals)
        if rtype == 'data':
            _close_subtotal_ranges()
            if ag_name != current_agent:
                _close_data_ranges()
                current_agent = ag_name
                agent_start = row_num
                current_model = None
                model_start = None
            if model != current_model or current_model is None:
                if current_model is not None and current_agent == ag_name:
                    model_ranges[(current_agent, current_model)] = (model_start, row_num - 1)
                current_model = model
                model_start = row_num
        elif rtype == 'agent_subtotal':
            _close_data_ranges()
            current_agent = None
            current_model = None
            if subtotal_start is None:
                subtotal_start = row_num
                subtotal_agent = ag_name
        row_num += 1

    _close_subtotal_ranges()

    # 构建 merges
    for ag_name, (sr, er) in agent_ranges.items():
        merges.append((sr, 1, er, 1))
    for (ag_name, model), (sr, er) in model_ranges.items():
        merges.append((sr, 2, er, 2))
    for ag_name, (sr, er) in subtotal_agent_ranges.items():
        merges.append((sr, 1, er, 1))
    for ag_name, (sr, er) in subtotal_model_ranges.items():
        merges.append((sr, 2, er, 2))

    # 全部总计
    gt = row_num
    for metric in _METRIC_ORDER:
        vals = [('', TOT_STYLE) if metric != 'input' else ('全部总计', TOT_STYLE), ('', TOT_STYLE),
                (_METRIC_LABELS[metric], TOT_STYLE)]
        gt_all = 0
        for m_label in all_months:
            ct = 0
            for ag_name, ag_display, monthly_data in agent_order:
                for model in sorted({m for d in monthly_data.values() for m in d}):
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        ct += md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        ct += md.get(metric, 0)
            gt_all += ct
            vals.append((ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"), TOT_STYLE))
        vals.append((gt_all if metric != "cost" else (f"≈¥{gt_all:.4f}" if gt_all else "0"), TOT_STYLE))
        wb.add_row(sheet_name, vals)
        row_num += 1
    merges.append((gt, 1, row_num - 1, 1))
    merges.append((gt, 2, row_num - 1, 2))
    wb.merges[sheet_name] = merges
    wb.save(filepath)


# ═══════════════════════════════════════════════════
#  CSV 导出
# ═══════════════════════════════════════════════════

def _write_csv_simple(filepath, agent_name, agent_display, filtered_models, project_root):
    """单 Agent 简单 CSV。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用'])
        ti = to = tc = tca = 0
        at_cost = 0.0
        for pm in filtered_models:
            inp = int(pm.get('input', 0))
            out = int(pm.get('output', 0))
            cache = int(pm.get('cache', 0))
            calls = int(pm.get('calls', 0))
            model = pm.get('model', 'unknown')
            cr = calc_cache_rate(inp, cache)
            cr_str = f"{cr:.1f}%" if cr is not None else "-"
            cs = _cost_for_pm(pm, project_root)
            if cs.startswith("≈¥"):
                at_cost += float(cs[2:])
            w.writerow([agent_display, model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
            ti += inp; to += out; tc += cache; tca += calls
        if len(filtered_models) > 1:
            tcr = calc_cache_rate(ti, tc)
            tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
            at_cs = f"≈¥{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
            w.writerow([f'{agent_display} 合计', '', ti, to, tc, tcr_str, tca, ti + to, ti + to + tc, at_cs])


def _write_csv_multi_simple(filepath, results, project_root):
    """多 Agent 简单 CSV，含每个 Agent 单独合计 + 总合计。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(['Agent', '模型', '输入', '输出', '缓存', '缓存率', '调用', '总计', '总计(含缓存)', '预估费用'])
        grand_ti = grand_to = grand_tc = grand_tca = 0
        grand_cost = 0.0
        total_agents = 0
        for agent, data in results:
            agent_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]
            if not agent_models:
                continue
            total_agents += 1
            ti = to = tc = tca = 0
            at_cost = 0.0
            for pm in agent_models:
                inp = int(pm.get('input', 0))
                out = int(pm.get('output', 0))
                cache = int(pm.get('cache', 0))
                calls = int(pm.get('calls', 0))
                model = pm.get('model', 'unknown')
                cr = calc_cache_rate(inp, cache)
                cr_str = f"{cr:.1f}%" if cr is not None else "-"
                cs = _cost_for_pm(pm, project_root)
                if cs.startswith("≈¥"):
                    at_cost += float(cs[2:])
                w.writerow([agent.display_name(), model, inp, out, cache, cr_str, calls, inp + out, inp + out + cache, cs])
                ti += inp; to += out; tc += cache; tca += calls
            if len(agent_models) > 1:
                tcr = calc_cache_rate(ti, tc)
                tcr_str = f"{tcr:.1f}%" if tcr is not None else "-"
                at_cs = f"≈¥{at_cost:.4f} (仅供参考)" if at_cost > 0 else "-"
                w.writerow([f'{agent.display_name()} 合计', '', ti, to, tc, tcr_str, tca, ti + to, ti + to + tc, at_cs])
            grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
            grand_cost += at_cost
        if total_agents > 1:
            gtt = grand_ti + grand_to
            gtcr = calc_cache_rate(grand_ti, grand_tc)
            gtcr_str = f"{gtcr:.1f}%" if gtcr is not None else "-"
            gcs = f"≈¥{grand_cost:.4f} (仅供参考)" if grand_cost > 0 else "-"
            w.writerow(['全部总计', '', grand_ti, grand_to, grand_tc, gtcr_str, grand_tca, gtt, gtt + grand_tc, gcs])


def _write_csv_monthly(filepath, agent_name, agent_display, monthly_data, all_months):
    """单 Agent 年度 CSV，按月拆分列。"""
    import csv
    all_models = sorted({m for d in monthly_data.values() for m in d})
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
        w.writerow(headers)
        for model in all_models:
            for metric in _METRIC_ORDER:
                row = [agent_display if metric == 'input' else '', model if metric == 'input' else '', _METRIC_LABELS[metric]]
                tot = 0
                for m_label in all_months:
                    md = monthly_data[m_label].get(model, {})
                    if metric == 'total':
                        v = md.get('input', 0) + md.get('output', 0)
                    elif metric == 'total_with_cache':
                        v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                    else:
                        v = md.get(metric, 0)
                    tot += v
                    row.append(v if metric != "cost" else (f"≈¥{v:.4f}" if v else "0"))
                row.append(tot if metric != "cost" else (f"≈¥{tot:.4f}" if tot else "0"))
                w.writerow(row)
        # 多模型时展示合计
        if len(all_models) > 1:
            for metric in _METRIC_ORDER:
                row = [f'{agent_display} 合计' if metric == 'input' else '',
                       '合计' if metric == 'input' else '',
                       _METRIC_LABELS[metric]]
                gt_all = 0
                for m_label in all_months:
                    ct = 0
                    for model in all_models:
                        md = monthly_data[m_label].get(model, {})
                        if metric == 'total':
                            ct += md.get('input', 0) + md.get('output', 0)
                        elif metric == 'total_with_cache':
                            ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                        else:
                            ct += md.get(metric, 0)
                    gt_all += ct
                    row.append(ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"))
                row.append(gt_all if metric != "cost" else (f"≈¥{gt_all:.4f}" if gt_all else "0"))
                w.writerow(row)


def _write_csv_multi_monthly(filepath, agent_order, all_months):
    """多 Agent 年度 CSV，含每个 Agent 单独合计 + 总合计。"""
    import csv
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        headers = ['Agent', 'Model', 'Metric'] + [f'{m}月' for m in all_months] + ['合计']
        w.writerow(headers)
        for agent_name, agent_display, monthly_data in agent_order:
            all_models = sorted({m for d in monthly_data.values() for m in d})
            if not all_models:
                continue
            for model in all_models:
                for metric in _METRIC_ORDER:
                    row = [agent_display if metric == 'input' else '', model if metric == 'input' else '', _METRIC_LABELS[metric]]
                    tot = 0
                    for m_label in all_months:
                        md = monthly_data[m_label].get(model, {})
                        if metric == 'total':
                            v = md.get('input', 0) + md.get('output', 0)
                        elif metric == 'total_with_cache':
                            v = md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                        else:
                            v = md.get(metric, 0)
                        tot += v
                        row.append(v if metric != "cost" else (f"≈¥{v:.4f}" if v else "0"))
                    row.append(tot if metric != "cost" else (f"≈¥{tot:.4f}" if tot else "0"))
                    w.writerow(row)
            # 多模型时展示 Agent 合计
            if len(all_models) > 1:
                for metric in _METRIC_ORDER:
                    row = [f'{agent_display} 合计' if metric == 'input' else '',
                           '合计' if metric == 'input' else '',
                           _METRIC_LABELS[metric]]
                    ag_total = 0
                    for m_label in all_months:
                        ct = 0
                        for model in all_models:
                            md = monthly_data[m_label].get(model, {})
                            if metric == 'total':
                                ct += md.get('input', 0) + md.get('output', 0)
                            elif metric == 'total_with_cache':
                                ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                            else:
                                ct += md.get(metric, 0)
                        ag_total += ct
                        row.append(ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"))
                    row.append(ag_total if metric != "cost" else (f"≈¥{ag_total:.4f}" if ag_total else "0"))
                    w.writerow(row)
        # 全部总计
        if len(agent_order) > 1:
            for metric in _METRIC_ORDER:
                row = ['全部总计' if metric == 'input' else '', '', _METRIC_LABELS[metric]]
                gt_all = 0
                for m_label in all_months:
                    ct = 0
                    for ag_name, ag_display, monthly_data in agent_order:
                        for model in sorted({m for d in monthly_data.values() for m in d}):
                            md = monthly_data[m_label].get(model, {})
                            if metric == 'total':
                                ct += md.get('input', 0) + md.get('output', 0)
                            elif metric == 'total_with_cache':
                                ct += md.get('input', 0) + md.get('output', 0) + md.get('cache', 0)
                            else:
                                ct += md.get(metric, 0)
                    gt_all += ct
                    row.append(ct if metric != "cost" else (f"≈¥{ct:.4f}" if ct else "0"))
                row.append(gt_all if metric != "cost" else (f"≈¥{gt_all:.4f}" if gt_all else "0"))
                w.writerow(row)


def export_interactive(data, agent, *, version: str, split_months, skip_model, calc_cache_rate,
                       fmt_num, detect_context, project_root: str,
                       from_ts: float = None, to_ts: float = None,
                       is_year: bool = False, export_dir: str = None):
    """交互式导出统计。is_year=True 时按月拆分，导出 XLSX/CSV/JSON。"""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # ── 年度导出：预先收集月度数据（仅一次，避免重复收集）──
        monthly_data = None
        month_labels = None
        if is_year and from_ts is not None and to_ts is not None:
            months = split_months(from_ts, to_ts)
            month_labels = [label for label, _, _ in months]
            monthly_data = {}
            total_months = len(months)
            for idx, (label, m_start, m_end) in enumerate(months, 1):
                print(f"  ⏳ 正在收集 {label} 数据 ({idx}/{total_months})...", end="\r", flush=True)
                m_data = agent.collect(from_ts=m_start, to_ts=m_end)
                monthly_data[label] = {}
                for pm in (m_data.per_model or []):
                    if skip_model(pm):
                        continue
                    mn = pm.get("model", "unknown")
                    inp = pm.get("input", 0) or 0
                    out = pm.get("output", 0) or 0
                    cache = pm.get("cache", 0) or 0
                    pc = get_price(mn, project_root)
                    cost = 0 if is_total_mode(pm) else (to_cny(calc_cost(inp, out, cache, pc), pc.get('currency', 'CNY')) if pc else 0)
                    monthly_data[label][mn] = {
                        "input": inp, "output": out, "cache": cache,
                        "calls": pm.get("calls", 0), "cost": cost,
                    }
            print(" " * 40, end="\r")
            # 从月度数据汇总 filtered_models
            all_models = sorted({m for d in monthly_data.values() for m in d})
            agg = {}
            for model in all_models:
                agg[model] = {"input": 0, "output": 0, "cache": 0, "calls": 0}
                for label in month_labels:
                    md = monthly_data[label].get(model, {})
                    agg[model]["input"] += md.get("input", 0)
                    agg[model]["output"] += md.get("output", 0)
                    agg[model]["cache"] += md.get("cache", 0)
                    agg[model]["calls"] += md.get("calls", 0)
            filtered_models = [{"model": m, **v} for m, v in agg.items()]
        else:
            filtered_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]

        # ── 显示格式化汇总 ──
        print()
        print(f"📊 {data.display_name if data else agent.display_name()} — 导出 ({date_str})")
        print("═" * 52)
        for pm in filtered_models:
            m = pm.get("model", "unknown")
            inp = pm.get("input", 0)
            out = pm.get("output", 0)
            cache = pm.get("cache", 0)
            calls = pm.get("calls", 0)
            total_tok = inp + out
            total_w_cache = total_tok + cache
            print(f"  {m}")
            if agent._has_live_context:
                cw = detect_context(m)
                pct = round(total_tok / cw * 100, 1) if cw else 0
                print(f"    上下文          {fmt_num(total_tok):>8} / {fmt_num(cw):<8} ({pct}%)")
            _print_pm_detail(pm, fmt_num, indent="    ")

        # ── 合计（多模型时显示） ──
        if filtered_models and len(filtered_models) > 1:
            ti = sum(pm.get("input", 0) for pm in filtered_models)
            to = sum(pm.get("output", 0) for pm in filtered_models)
            tc = sum(pm.get("cache", 0) for pm in filtered_models)
            tca = sum(pm.get("calls", 0) for pm in filtered_models)
            tt = ti + to
            print(f"  {'─' * 42}")
            print(f"  合计")
            if any(is_total_mode(pm) for pm in filtered_models):
                print(f"    总计 tokens     {fmt_num(tt):>8}")
                print(f"    调用次数        {tca} 次")
                print(f"    ─────────────────────────────────────")
                print(f"    总计            {fmt_num(tt)}")
            else:
                print(f"    输入 tokens     {fmt_num(ti):>8}")
                print(f"    输出 tokens     {fmt_num(to):>8}")
                print(f"    缓存 tokens     {fmt_num(tc):>8}")
                print(f"    调用次数        {tca} 次")
                print(f"    ─────────────────────────────────────")
                print(f"    总计/+缓存     {fmt_num(tt)}/{fmt_num(tt + tc)}")
        print()

        # Step 1: 输入目录（如果已提供路径则跳过交互）
        if export_dir:
            dir_path = os.path.expanduser(export_dir)
            if not os.path.isdir(dir_path):
                print(f"⚠️ 目录不存在: {dir_path}，使用当前目录")
                dir_path = os.getcwd()
        else:
            dir_path = os.getcwd()
            try:
                while True:
                    dir_input = input("\n请输入导出目录路径 (回车=当前目录, q=取消): ").strip()
                    if not dir_input:
                        break
                    if dir_input.lower() == "q":
                        print("已取消导出")
                        return
                    p = os.path.expanduser(dir_input)
                    if os.path.isdir(p):
                        dir_path = p
                        break
                    print(f"⚠️ 目录不存在: {p}, 请重试")
            except EOFError:
                pass

        # Step 2: 选择格式
        print("\n选择导出格式:")
        print("  [1] XLSX（默认）")
        print("  [2] CSV")
        print("  [3] JSON")
        fmt = "xlsx"
        try:
            fmt_choice = input("请选择 (1/2/3, 回车=1): ").strip().lower()
            if fmt_choice in ("2", "csv"):
                fmt = "csv"
            elif fmt_choice in ("3", "json"):
                fmt = "json"
        except EOFError:
            pass

        # Step 3: 写文件
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        if is_year:
            prefix = f"token-stats_{agent.name()}_yearly"
        else:
            prefix = f"token-stats_{agent.name()}"
        filename = f"{prefix}_{timestamp}.{fmt}"
        filepath = os.path.join(dir_path, filename)

        if fmt == "json":
            export_data = {
                "tool": "token-stats",
                "version": version,
                "agent": agent.name(),
                "agent_display": agent.display_name(),
                "export_date": date_str,
                "exported_at": now.isoformat(),
                "per_model": [{
                    "model": pm.get("model", "unknown"),
                    "input_tokens": pm.get("input", 0),
                    "output_tokens": pm.get("output", 0),
                    "cache_tokens": pm.get("cache", 0),
                    "token_mode": pm.get("token_mode", "split"),
                    "cache_ratio": round(calc_cache_rate(pm.get("input",0), pm.get("cache",0)), 1) if calc_cache_rate(pm.get("input",0), pm.get("cache",0)) is not None else None,
                    "calls": pm.get("calls", 0),
                    "total_tokens": pm.get("input", 0) + pm.get("output", 0),
                    "total_with_cache": pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0),
                } for pm in filtered_models],
                "summary": (
                    {
                        "total_input_tokens": sum(pm.get("input", 0) for pm in filtered_models),
                        "total_output_tokens": sum(pm.get("output", 0) for pm in filtered_models),
                        "total_cache_tokens": sum(pm.get("cache", 0) for pm in filtered_models),
                        "total_calls": sum(pm.get("calls", 0) for pm in filtered_models),
                        "total_tokens": sum(pm.get("input", 0) + pm.get("output", 0) for pm in filtered_models),
                        "total_with_cache": sum(pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0) for pm in filtered_models),
                    }
                    if filtered_models and len(filtered_models) > 1
                    else None
                ),
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        elif fmt == "csv":
            if is_year and monthly_data is not None:
                _write_csv_monthly(filepath, agent.name(), agent.display_name(),
                                   monthly_data, month_labels)
            else:
                _write_csv_simple(filepath, agent.name(), agent.display_name(),
                                  filtered_models, project_root)
        else:
            if is_year and monthly_data is not None:
                _write_xlsx_monthly(filepath, agent.name(), agent.display_name(),
                                    monthly_data, month_labels)
            else:
                _write_xlsx_simple(filepath, agent.name(), agent.display_name(),
                                   filtered_models, project_root)

        print(f"✅ 已导出到: {filepath}")
    except KeyboardInterrupt:
        print()
        print("已取消导出")


def export_multi(results: list[tuple], *, version: str, split_months, skip_model, calc_cache_rate,
                  fmt_num, detect_context, project_root: str,
                  is_year: bool = False, from_ts: float = None, to_ts: float = None,
                  export_dir: str = None):
    """导出多个 Agent 的统计（合并输出）。is_year=True 时按月拆分。"""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # ── 年度导出：预先收集月度数据（仅一次，避免重复收集）──
        agent_order = None
        month_labels = None
        if is_year and from_ts is not None and to_ts is not None:
            months = split_months(from_ts, to_ts)
            month_labels = [label for label, _, _ in months]
            agent_order = []
            total_agents = len(results)
            agent_idx = 0
            for agent, data in results:
                agent_idx += 1
                agent_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]
                if not agent_models:
                    continue
                monthly_data = {}
                total_months = len(months)
                for idx, (label, m_start, m_end) in enumerate(months, 1):
                    print(f"  ⏳ 正在收集 {agent.display_name()} {label} 数据 ({idx}/{total_months}) [{agent_idx}/{total_agents}]...", end="\r", flush=True)
                    m_data = agent.collect(from_ts=m_start, to_ts=m_end)
                    monthly_data[label] = {}
                    for pm in (m_data.per_model or []):
                        if skip_model(pm):
                            continue
                        mn = pm.get("model", "unknown")
                        inp = pm.get("input", 0) or 0
                        out = pm.get("output", 0) or 0
                        cache = pm.get("cache", 0) or 0
                        pc = get_price(mn, project_root)
                        cost = 0 if is_total_mode(pm) else (to_cny(calc_cost(inp, out, cache, pc), pc.get('currency', 'CNY')) if pc else 0)
                        monthly_data[label][mn] = {
                            "input": inp, "output": out, "cache": cache,
                            "calls": pm.get("calls", 0), "cost": cost,
                        }
                print(" " * 60, end="\r")
                agent_order.append((agent.name(), agent.display_name(), monthly_data))
            print(" " * 60, end="\r")

        # ── 显示格式化汇总 ──
        print()
        print(f"📊 多 Agent 导出 ({date_str})")
        print("═" * 52)
        grand_ti = grand_to = grand_tc = grand_tca = 0
        for agent, data in results:
            print(f"\n  🤖 {agent.display_name()}")
            agent_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]
            for pm in agent_models:
                m = pm.get("model", "unknown")
                inp = pm.get("input", 0)
                out = pm.get("output", 0)
                cache = pm.get("cache", 0)
                calls = pm.get("calls", 0)
                total_tok = inp + out
                total_w_cache = total_tok + cache
                print(f"    {m}")
                if agent._has_live_context:
                    cw = detect_context(m)
                    pct = round(total_tok / cw * 100, 1) if cw else 0
                    print(f"      上下文          {fmt_num(total_tok):>8} / {fmt_num(cw):<8} ({pct}%)")
                _print_pm_detail(pm, fmt_num, indent="      ")

            # Agent 内合计
            if agent_models and len(agent_models) > 1:
                ti = sum(pm.get("input", 0) for pm in agent_models)
                to = sum(pm.get("output", 0) for pm in agent_models)
                tc = sum(pm.get("cache", 0) for pm in agent_models)
                tca = sum(pm.get("calls", 0) for pm in agent_models)
                tt = ti + to
                print(f"    {'─' * 42}")
                print(f"    合计")
                if any(is_total_mode(pm) for pm in agent_models):
                    print(f"      总计 tokens     {fmt_num(tt):>8}")
                    print(f"      调用次数        {tca} 次")
                    print(f"      ─────────────────────────────────────")
                    print(f"      总计            {fmt_num(tt)}")
                else:
                    print(f"      输入 tokens     {fmt_num(ti):>8}")
                    print(f"      输出 tokens     {fmt_num(to):>8}")
                    print(f"      缓存 tokens     {fmt_num(tc):>8}")
                    print(f"      调用次数        {tca} 次")
                    print(f"      ─────────────────────────────────────")
                    print(f"      总计/+缓存     {fmt_num(tt)}/{fmt_num(tt + tc)}")
                grand_ti += ti; grand_to += to; grand_tc += tc; grand_tca += tca
            else:
                pm = agent_models[0] if agent_models else {}
                grand_ti += pm.get("input", 0)
                grand_to += pm.get("output", 0)
                grand_tc += pm.get("cache", 0)
                grand_tca += pm.get("calls", 0)

        # 所有 Agent 总计
        if len(results) > 1:
            gtt = grand_ti + grand_to
            print(f"\n  {'═' * 42}")
            print(f"  全部 Agent 总计")
            print(f"    输入 tokens     {fmt_num(grand_ti):>8}")
            print(f"    输出 tokens     {fmt_num(grand_to):>8}")
            print(f"    缓存 tokens     {fmt_num(grand_tc):>8}")
            print(f"    调用次数        {grand_tca} 次")
            print(f"    ─────────────────────────────────────")
            print(f"    总计/+缓存     {fmt_num(gtt)}/{fmt_num(gtt + grand_tc)}")

        # Step 1: 输入目录
        if export_dir:
            dir_path = os.path.expanduser(export_dir)
            if not os.path.isdir(dir_path):
                print(f"⚠️ 目录不存在: {dir_path}，使用当前目录")
                dir_path = os.getcwd()
        else:
            dir_path = os.getcwd()
            try:
                while True:
                    dir_input = input("\n请输入导出目录路径 (回车=当前目录, q=取消): ").strip()
                    if not dir_input:
                        break
                    if dir_input.lower() == "q":
                        print("已取消导出")
                        return
                    p = os.path.expanduser(dir_input)
                    if os.path.isdir(p):
                        dir_path = p
                        break
                    print(f"⚠️ 目录不存在: {p}, 请重试")
            except EOFError:
                pass

        # Step 2: 选择格式
        fmt = "xlsx"
        try:
            print("\n选择导出格式:")
            print("  [1] XLSX（默认）")
            print("  [2] CSV")
            print("  [3] JSON")
            fmt_choice = input("请选择 (1/2/3, 回车=1): ").strip().lower()
            if fmt_choice in ("2", "csv"):
                fmt = "csv"
            elif fmt_choice in ("3", "json"):
                fmt = "json"
        except EOFError:
            pass

        # Step 3: 写文件
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        agent_names = "+".join(agent.name() for agent, _ in results)
        if is_year:
            filename = f"token-stats_{agent_names}_yearly_{timestamp}.{fmt}"
        else:
            filename = f"token-stats_{agent_names}_{timestamp}.{fmt}"
        filepath = os.path.join(dir_path, filename)

        if fmt == "json":
            agents_json = []
            for agent, data in results:
                agent_models = [pm for pm in (data.per_model or []) if not skip_model(pm)]
                per_model = [{
                    "model": pm.get("model", "unknown"),
                    "input_tokens": pm.get("input", 0),
                    "output_tokens": pm.get("output", 0),
                    "cache_tokens": pm.get("cache", 0),
                    "token_mode": pm.get("token_mode", "split"),
                    "cache_ratio": round(calc_cache_rate(pm.get("input",0), pm.get("cache",0)), 1) if calc_cache_rate(pm.get("input",0), pm.get("cache",0)) is not None else None,
                    "calls": pm.get("calls", 0),
                    "total_tokens": pm.get("input", 0) + pm.get("output", 0),
                    "total_with_cache": pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0),
                } for pm in agent_models]
                entry = {
                    "agent": agent.name(),
                    "agent_display": agent.display_name(),
                    "per_model": per_model,
                }
                if agent_models and len(agent_models) > 1:
                    entry["summary"] = {
                        "total_input_tokens": sum(pm.get("input", 0) for pm in agent_models),
                        "total_output_tokens": sum(pm.get("output", 0) for pm in agent_models),
                        "total_cache_tokens": sum(pm.get("cache", 0) for pm in agent_models),
                        "total_calls": sum(pm.get("calls", 0) for pm in agent_models),
                        "total_tokens": sum(pm.get("input", 0) + pm.get("output", 0) for pm in agent_models),
                        "total_with_cache": sum(pm.get("input", 0) + pm.get("output", 0) + pm.get("cache", 0) for pm in agent_models),
                    }
                agents_json.append(entry)

            export_data = {
                "tool": "token-stats",
                "version": version,
                "export_date": date_str,
                "exported_at": now.isoformat(),
                "agents": agents_json,
            }
            if len(results) > 1:
                export_data["grand_total"] = {
                    "total_input_tokens": grand_ti,
                    "total_output_tokens": grand_to,
                    "total_cache_tokens": grand_tc,
                    "total_calls": grand_tca,
                    "total_tokens": grand_ti + grand_to,
                    "total_with_cache": grand_ti + grand_to + grand_tc,
                }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"  {filepath}")
            print(f"多 Agent 数据已合并导出")
        elif fmt == "csv":
            if is_year and agent_order is not None:
                _write_csv_multi_monthly(filepath, agent_order, month_labels)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
            else:
                _write_csv_multi_simple(filepath, results, project_root)
        else:
            if is_year and agent_order is not None:
                _write_xlsx_multi_monthly(filepath, agent_order, month_labels, agent_order)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
            else:
                _write_xlsx_multi_simple(filepath, results, project_root)
                print(f"  {filepath}")
                print(f"多 Agent 数据已合并导出")
    except KeyboardInterrupt:
        print()
        print("已取消导出")
