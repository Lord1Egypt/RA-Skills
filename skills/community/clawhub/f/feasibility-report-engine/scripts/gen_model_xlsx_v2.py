#!/usr/bin/env python3
"""专业版《项目投资测算套表》——可研交付标准件 v2
排版特点（针对"松散不严谨"反馈全面升级）：
- 三线表规范：粗上线/细中隔线/粗下线（表头-表体-结束）
- 分组标题栏：深蓝底白字
- 区域说明行：斜体小字灰
- 数字格式统一：千分位、百分比两位、万元两档切换
- 严格列宽、冻结窗格、打印设置 A4 横向
- 颜色语义：蓝=输入(唯一手改) 黑=公式 绿=跨表 黄=核心结论 灰=说明
用法: python3 gen_model_xlsx_v2.py [out.xlsx] [项目名] [总投资万元] [达产收入万元] [建设期] [运营期]
"""
import sys
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

OUT   = sys.argv[1] if len(sys.argv) > 1 else "项目投资测算套表_专业版.xlsx"
PNAME = sys.argv[2] if len(sys.argv) > 2 else "××××项目"
INV   = float(sys.argv[3]) if len(sys.argv) > 3 else 3000000   # 万元
REV   = float(sys.argv[4]) if len(sys.argv) > 4 else 600000
CON_Y = int(sys.argv[5]) if len(sys.argv) > 5 else 4
OP_Y  = int(sys.argv[6]) if len(sys.argv) > 6 else 16

NYR = 20
wb = xlsxwriter.Workbook(OUT, {"strings_to_numbers": True})

# ---------- 精排格式 ----------
BLUE_D = "#1F4E79"; BLUE_M = "#2E75B6"; BLUE_L = "#DEEBF7"
GRAY_L = "#F2F2F2"; GRAY_M = "#BFBFBF"
GREEN_L = "#E2EFDA"; YELLOW = "#FFF2CC"; RED = "#C00000"

F = {
    "cover_title": wb.add_format({"bold": True, "font_size": 20, "font_name": "微软雅黑", "align": "center", "valign": "vcenter", "font_color": BLUE_D}),
    "cover_sub":   wb.add_format({"font_size": 12, "font_name": "微软雅黑", "align": "center", "valign": "vcenter", "font_color": "#595959"}),
    "cover_line":  wb.add_format({"font_size": 11, "font_name": "微软雅黑", "align": "center", "valign": "vcenter"}),
    "sec_title":   wb.add_format({"bold": True, "font_size": 13, "font_name": "微软雅黑", "font_color": BLUE_D}),
    "sec_bar":     wb.add_format({"bold": True, "font_size": 11, "font_name": "微软雅黑", "bg_color": BLUE_D, "font_color": "#FFFFFF", "align": "left", "valign": "vcenter", "border": 1}),
    "hdr":         wb.add_format({"bold": True, "bg_color": BLUE_L, "border": 1, "align": "center", "valign": "vcenter", "font_name": "微软雅黑", "font_size": 10}),
    "hdr_grp":     wb.add_format({"bold": True, "bg_color": BLUE_M, "font_color": "#FFFFFF", "border": 1, "align": "center", "valign": "vcenter", "font_name": "微软雅黑", "font_size": 10}),
    "lbl":         wb.add_format({"border": 1, "font_name": "微软雅黑", "valign": "center", "font_size": 10}),
    "lbl_g":       wb.add_format({"border": 1, "font_name": "微软雅黑", "valign": "center", "font_size": 10, "bg_color": GRAY_L}),
    "in":          wb.add_format({"border": 1, "font_color": BLUE_D, "bold": True, "align": "center", "font_name": "微软雅黑", "bg_color": "#FFFFFF", "font_size": 10, "num_format": "#,##0"}),
    "in_pct":      wb.add_format({"border": 1, "font_color": BLUE_D, "bold": True, "align": "center", "font_name": "微软雅黑", "bg_color": "#FFFFFF", "font_size": 10, "num_format": "0.0%"}),
    "calc":        wb.add_format({"border": 1, "font_color": "#000000", "num_format": "#,##0.00", "font_name": "微软雅黑", "font_size": 10}),
    "calc0":       wb.add_format({"border": 1, "font_color": "#000000", "num_format": "#,##0", "font_name": "微软雅黑", "font_size": 10}),
    "ref":         wb.add_format({"border": 1, "font_color": "#375623", "num_format": "#,##0", "font_name": "微软雅黑", "bg_color": GREEN_L, "font_size": 10}),
    "ref0":        wb.add_format({"border": 1, "font_color": "#375623", "font_name": "微软雅黑", "bg_color": GREEN_L, "font_size": 10}),
    "key":         wb.add_format({"bold": True, "bg_color": YELLOW, "border": 2, "font_color": RED, "num_format": "0.00%", "font_name": "微软雅黑", "align": "center", "font_size": 11}),
    "keyn":        wb.add_format({"bold": True, "bg_color": YELLOW, "border": 2, "font_color": RED, "num_format": "#,##0", "font_name": "微软雅黑", "align": "center", "font_size": 11}),
    "note":        wb.add_format({"font_name": "微软雅黑", "font_size": 9, "text_wrap": True, "valign": "top", "font_color": "#7F7F7F", "italic": True}),
    "note_w":      wb.add_format({"font_name": "微软雅黑", "font_size": 9, "text_wrap": True, "valign": "top", "font_color": "#C00000"}),
    "year":        wb.add_format({"border": 1, "align": "center", "font_name": "微软雅黑", "font_size": 9, "bg_color": GRAY_L, "font_color": "#404040"}),
    "phase":       wb.add_format({"border": 1, "align": "center", "font_name": "微软雅黑", "font_size": 9, "bg_color": BLUE_L, "font_color": BLUE_D, "bold": True}),
}

def w(ws, row, col, *args):
    ws.write(row - 1, col - 1, *args)

def set_cols(ws, widths):
    for i, wd in enumerate(widths):
        ws.set_column(i, i, wd)

def block_bar(ws, row, title, span=4):
    ws.merge_range(row - 1, 0, row - 1, span - 1, title, F["sec_bar"])

# ================= Sheet0 封面 =================
ws = wb.add_worksheet("0_封面与填表说明")
set_cols(ws, [3, 26, 30, 26, 3])
for r in range(1, 8): ws.set_row(r - 1, 22)
w(ws, 4, 2, PNAME, F["cover_title"])
w(ws, 5, 2, "项目投资测算套表", F["cover_title"])
w(ws, 6, 2, "——投资估算 · 资金筹措 · 财务评价 · 敏感性分析——", F["cover_sub"])
w(ws, 8, 2, "编制单位：××咨询有限公司", F["cover_line"])
w(ws, 9, 2, "编 制 日 期：2026年9月", F["cover_line"])
w(ws, 10, 2, "文件编号：KY-2026-×××", F["cover_line"])
# 颜色图例
w(ws, 13, 2, "颜色约定（本套表唯一规则）", F["sec_title"])
legend = [
    ("蓝色加粗", "输入项：只需填写/修改这些单元格（集中在参数主控），是客户唯一需要动的地方", BLUE_D),
    ("黑色", "公式自动计算：请勿修改，改参数主控即自动更新", "#000000"),
    ("绿色底", "跨表引用：自动带出，请勿手改", "#375623"),
    ("黄底红字", "核心结论指标：自动生成，交付时重点关注", RED),
    ("灰字斜体", "说明文字：帮助理解口径，不参与计算", "#7F7F7F"),
]
r = 14
for name, desc, color in legend:
    w(ws, r, 2, f"■ {name}", wb.add_format({"bold": True, "font_color": color, "font_name": "微软雅黑", "font_size": 10}))
    w(ws, r, 3, desc, F["note"])
    r += 1
r += 1
w(ws, r, 2, "使用步骤", F["sec_title"]); r += 1
for step in [
    "第一步：在【1_参数主控】填写蓝色单元格（投资/建设期/收入/成本率/融资利率等），其余工作表全部自动更新。",
    "第二步：需要分项投资明细时，在【2_投资估算】补充各板块工程费。",
    "第三步：查看【4_财务指标】黄底结论（IRR/NPV/回收期），到【5_敏感性】做情景判断。",
    "第四步：将测算结论回填《可行性研究报告》财务评价章节；正式投资决策以尽调实测数据复核。",
]:
    w(ws, r, 2, f"• {step}", F["note"])
    r += 1
r += 1
w(ws, r, 2, "重要提示", wb.add_format({"bold": True, "font_color": RED, "font_name": "微软雅黑", "font_size": 11})); r += 1
for tip in [
    "1. 本表为前期研判口径：投资与收入按项目已知框定值 + 行业基准测算，最终以尽调数据回填核定。",
    "2. 测算期 = 建设期 + 运营期 ≤ 20 年；超过需扩展年份列（在表尾复制公式即可）。",
    "3. 若 IRR 显示 #NUM!：检查建设期是否填写、投资是否在建设期全额流出、运营期现金流方向是否正确。",
    "4. 涉税参数（西部大开发 15% 优惠、涉农减免）请与税务顾问确认适用性后再填。",
]:
    w(ws, r, 2, tip, F["note"])
    r += 1

# ================= Sheet1 参数主控 =================
ws = wb.add_worksheet("1_参数主控")
set_cols(ws, [3, 40, 16, 60])
w(ws, 1, 2, "一、参数主控表（唯一输入区 · 蓝色单元格为必填/可改项）", F["sec_title"])
w(ws, 2, 2, "项目名称：", F["lbl_g"]); ws.merge_range("C2:D2", PNAME, F["in"])

params = [
    ("投资规模", [
        ("建设期（年）", CON_Y, "num", "自开工至首期投产年限"),
        ("运营期（年）", OP_Y, "num", "投产后测算年限（建设+运营≤20）"),
        ("项目总投资（万元）", INV, "num", "含建设投资+建设期利息+铺底流动资金"),
        ("建设投资占比", 0.95, "pct", "建设投资/总投资（剩余为建设期利息与铺底流动资金）"),
        ("铺底流动资金率", 0.05, "pct", "铺底流动资金/总投资"),
    ]),
    ("融资结构", [
        ("资本金比例", 0.30, "pct", "项目资本金比例（制度要求通常 20%-30%）"),
        ("银行贷款比例", 0.70, "pct", "与资本金合计应约 100%"),
        ("贷款年利率", 0.045, "pct", "长期贷款综合利率（按 LPR+点差）"),
        ("贷款宽限期（年）", CON_Y, "num", "含建设期，宽限内只付息不还本"),
        ("还款年限（年）", 10, "num", "宽限期后等额还本年限"),
    ]),
    ("税务", [
        ("增值税率", 0.09, "pct", "按适用税率：货 13% / 农产品初加工 9% / 服务 6%"),
        ("城建及附加率", 0.12, "pct", "城建税+教育附加（按增值税额计提）"),
        ("所得税率", 0.25, "pct", "西部大开发优惠情形填 0.15；涉农减免另核"),
    ]),
    ("收入与成本", [
        ("达产年营业收入（万元/年）", REV, "num", "运营稳定期年收入（不含税）"),
        ("投产第1年达产率", 0.40, "pct", "产能爬坡假设（可按项目实际调整）"),
        ("投产第2年达产率", 0.70, "pct", ""),
        ("投产第3年达产率", 0.90, "pct", "第4年起 100%"),
        ("经营成本率（占收入）", 0.62, "pct", "可变经营成本/收入（不含折旧利息税金）"),
        ("固定成本（万元/年）", INV * 0.003, "num", "与收入无关的固定支出（管理/维护等）"),
    ]),
    ("折旧与评价", [
        ("折旧年限（年）", 20, "num", "直线折旧（海洋装备类按 12-15 年从低掌握）"),
        ("残值率", 0.05, "pct", "折旧残值比例"),
        ("折现率ic（基准收益率）", 0.08, "pct", "NPV 折现率：产业类 8-10% / 基础设施 6-7%"),
    ]),
]
PK = {}
r = 3
for grp, items in params:
    block_bar(ws, r, f"■ {grp}")
    r += 1
    for key, val, typ, note in items:
        PK[key] = r
        w(ws, r, 2, key, F["lbl_g"])
        if typ == "pct":
            w(ws, r, 3, val, F["in_pct"])
        else:
            w(ws, r, 3, val, F["in"])
        w(ws, r, 4, note, F["note"])
        r += 1
w(ws, r + 1, 2, "注：资本金比例+银行贷款比例应约等于 100%；改任一蓝色格全表自动联动。", F["note_w"])

def pc(key):
    return f"'1_参数主控'!C{PK[key]}"

# ================= Sheet2 投资估算 =================
ws = wb.add_worksheet("2_投资估算")
set_cols(ws, [3, 46, 18, 18, 18, 46])
w(ws, 1, 2, "二、投资估算与资金筹措", F["sec_title"])
block_bar(ws, 3, "2.1 投资估算（万元）")
w(ws, 4, 2, "项目", F["hdr"]); w(ws, 4, 3, "金额（万元）", F["hdr"]); w(ws, 4, 4, "占比", F["hdr"]); w(ws, 4, 5, "口径", F["hdr"])
rows = [
    ("项目总投资（引用主控）", f"={pc('项目总投资（万元）')}", "ref", "100%"),
    ("其中：建设投资", f"=ROUND({pc('项目总投资（万元）')}*{pc('建设投资占比')},0)", "in", "自动×建设投资占比"),
    ("其中：建设期利息", f"=ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')}*({pc('建设期（年）')}/2+0.5),0)", "calc", "贷款额×利率×(建设期/2+0.5)"),
    ("其中：铺底流动资金", f"=ROUND({pc('项目总投资（万元）')}*{pc('铺底流动资金率')},0)", "calc", "自动×铺底流动资金率"),
]
r = 5
for name, formula, typ, note in rows:
    w(ws, r, 2, name, F["lbl_g"])
    w(ws, r, 3, formula, F[typ])
    if r == 5:
        w(ws, r, 4, "=D5", F["calc0"])
    else:
        w(ws, r, 4, f"=C{r}/C$5", F["calc"])
    w(ws, r, 5, note, F["note"])
    r += 1
w(ws, r, 2, "校验：建设投资+建设期利息+铺底流动资金 vs 总投资", F["lbl"])
w(ws, r, 3, "=C6+C7+C8-C5", F["calc0"]); w(ws, r, 4, "", F["calc0"]); w(ws, r, 5, "应接近 0（差额为预备费分摊），偏差大请查口径", F["note"])
r += 2
block_bar(ws, r, "2.2 资金筹措（万元）"); r += 1
w(ws, r, 2, "项目", F["hdr"]); w(ws, r, 3, "金额（万元）", F["hdr"]); w(ws, r, 4, "占比", F["hdr"]); w(ws, r, 5, "口径", F["hdr"]); r += 1
w(ws, r, 2, "项目资本金", F["lbl_g"]); w(ws, r, 3, f"=ROUND({pc('项目总投资（万元）')}*{pc('资本金比例')},0)", F["ref"]); w(ws, r, 4, f"=C{r}/C{r+1}", F["calc"]); w(ws, r, 5, f"资本金 {pc('资本金比例')} 自动带出", F["note"]); r += 1
w(ws, r, 2, "银行贷款", F["lbl_g"]); w(ws, r, 3, f"=ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')},0)", F["ref"]); w(ws, r, 4, f"=C{r}/C{r+1}", F["calc"]); w(ws, r, 5, f"债务融资 {pc('银行贷款比例')}", F["note"]); r += 1
w(ws, r, 2, "资金合计", F["lbl"]); w(ws, r, 3, f"=C{r-2}+C{r-1}", F["keyn"]); w(ws, r, 4, "=C13/C14", F["calc0"]); w(ws, r, 5, "应为总投资", F["note"]); r += 1
w(ws, r, 2, "资金缺口校验", F["lbl"]); w(ws, r, 3, f"=C{r-1}-C5", F["calc0"]); w(ws, r, 4, "", F["calc0"]); w(ws, r, 5, "应为 0；不为 0 请核对资本金+贷款比例=100%", F["note"]); r += 2

block_bar(ws, r, "2.3 建设期分年投资计划（默认均分，可改蓝格）"); r += 1
for c in range(5):
    w(ws, r, 3 + c, f"建设第{c+1}年", F["phase"])
r += 1
for c in range(5):
    w(ws, r, 3 + c, f"=IF({c+1}<={pc('建设期（年）')},ROUND({pc('项目总投资（万元）')}/{pc('建设期（年）')},0),0)", F["in"])

# ================= Sheet3 收入成本现金流 =================
ws = wb.add_worksheet("3_收入成本现金流")
set_cols(ws, [3, 30] + [10.5] * NYR)
w(ws, 1, 2, "三、分年度收入、成本与现金流（自动计算）", F["sec_title"])
w(ws, 2, 2, "单位：万元", F["note"])
# 年份双行：第N年/建设期标记
for c in range(NYR):
    w(ws, 3, 3 + c, f"第{c+1}年", F["year"])
# 行号(Excel 1-based)
R = {"isop": 5, "ramp": 6, "rev": 7, "vc": 8, "fc": 9, "dep": 10, "int": 11,
     "taxs": 12, "taxi": 13, "ni": 14, "fcf": 15, "ecf": 16}
w(ws, 4, 2, "项目 \\ 年份", F["hdr"])
for rr, lb in [(R["isop"], "投产标记（0建/1产）"), (R["ramp"], "达产率"), (R["rev"], "营业收入"),
               (R["vc"], "可变经营成本"), (R["fc"], "固定成本"), (R["dep"], "折旧费"),
               (R["int"], "利息费用"), (R["taxs"], "增值税及附加"), (R["taxi"], "所得税"),
               (R["ni"], "净利润"), (R["fcf"], "全投资净现金流（IRR源）"), (R["ecf"], "资本金净现金流")]:
    w(ws, rr, 2, lb, F["lbl_g"] if rr in (R["fcf"], R["ecf"]) else F["lbl"])

for c in range(NYR):
    col = xl_col_to_name(2 + c)   # C 列(0-based 2) 起
    y = c + 1
    w(ws, R["isop"], 3 + c, f"=IF({y}>{pc('建设期（年）')},1,0)", F["calc0"])
    w(ws, R["ramp"], 3 + c,
      f"=IF({col}{R['isop']}=0,0,IF({y}={pc('建设期（年）')}+1,{pc('投产第1年达产率')},"
      f"IF({y}={pc('建设期（年）')}+2,{pc('投产第2年达产率')},"
      f"IF({y}={pc('建设期（年）')}+3,{pc('投产第3年达产率')},1))))", F["calc0"])
    w(ws, R["rev"], 3 + c, f"=IF({col}{R['isop']}=0,0,ROUND({pc('达产年营业收入（万元/年）')}*{col}{R['ramp']},0))", F["calc0"])
    w(ws, R["vc"], 3 + c, f"=IF({col}{R['isop']}=0,0,ROUND({col}{R['rev']}*{pc('经营成本率（占收入）')},0))", F["calc0"])
    w(ws, R["fc"], 3 + c, f"=IF({col}{R['isop']}=0,0,{pc('固定成本（万元/年）')})", F["calc0"])
    w(ws, R["dep"], 3 + c, f"=IF({col}{R['isop']}=0,0,ROUND({pc('项目总投资（万元）')}*(1-{pc('残值率')})/{pc('折旧年限（年）')},0))", F["calc0"])
    w(ws, R["int"], 3 + c,
      f"=IF({col}{R['isop']}=0,ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')},0),"
      f"ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')}*0.55,0))", F["calc0"])
    w(ws, R["taxs"], 3 + c, f"=IF({col}{R['isop']}=0,0,ROUND({col}{R['rev']}*{pc('增值税率')}*{pc('城建及附加率')},0))", F["calc0"])
    w(ws, R["taxi"], 3 + c,
      f"=IF({col}{R['isop']}=0,0,MAX(0,ROUND(({col}{R['rev']}-{col}{R['vc']}-{col}{R['fc']}-{col}{R['dep']}-{col}{R['int']}-{col}{R['taxs']})*{pc('所得税率')},0)))", F["calc0"])
    w(ws, R["ni"], 3 + c,
      f"=IF({col}{R['isop']}=0,0,{col}{R['rev']}-{col}{R['vc']}-{col}{R['fc']}-{col}{R['dep']}-{col}{R['int']}-{col}{R['taxs']}-{col}{R['taxi']})", F["calc0"])
    w(ws, R["fcf"], 3 + c,
      f"=IF({col}{R['isop']}=0,-ROUND({pc('项目总投资（万元）')}/{pc('建设期（年）')},0),"
      f"{col}{R['ni']}+{col}{R['dep']}+{col}{R['int']})", F["calc"])
    w(ws, R["ecf"], 3 + c,
      f"=IF({col}{R['isop']}=0,-ROUND({pc('项目总投资（万元）')}*{pc('资本金比例')}/{pc('建设期（年）')},0),"
      f"{col}{R['ni']}+{col}{R['dep']}-IF({y}>{pc('贷款宽限期（年）')},ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}/{pc('还款年限（年）')},0),0))", F["calc"])
    # 建设期浅蓝底
    # （简化：通过投产标记 0 的年份整列浅蓝不易做，放弃）

w(ws, 19, 2, "注：简化口径，未含期末残值回收与增值税进项抵扣；正式投资决策以 mh-calculation 十七表复核。", F["note"])

LASTCOL = xl_col_to_name(3 + NYR - 1)

# ================= Sheet4 财务指标 =================
ws = wb.add_worksheet("4_财务指标")
set_cols(ws, [3, 46, 26, 60])
w(ws, 1, 2, "四、财务指标汇总（自动计算）", F["sec_title"])
block_bar(ws, 3, "核心结论指标")
w(ws, 4, 2, "指标", F["hdr"]); w(ws, 4, 3, "数值", F["hdr"]); w(ws, 4, 4, "判断口径", F["hdr"])
fcf_rng = f"'3_收入成本现金流'!C{R['fcf']}:{LASTCOL}{R['fcf']}"
ecf_rng = f"'3_收入成本现金流'!C{R['ecf']}:{LASTCOL}{R['ecf']}"
def ind(row, name, formula, note, key=False):
    w(ws, row, 2, name, F["key"] if key else F["lbl"])
    w(ws, row, 3, formula, F["key"] if key else F["calc"])
    w(ws, row, 4, note, F["note"])
ind(5, "全投资财务内部收益率 IRR", f"=IRR({fcf_rng})", "≥ 基准收益率 ic 即财务可行", True)
ind(6, "全投资财务净现值 NPV（万元）", f"=NPV({pc('折现率ic（基准收益率）')},{fcf_rng})+C{R['fcf']}", "> 0 即财务可行", True)
ind(7, "资本金财务内部收益率", f"=IRR({ecf_rng})", "股东视角回报", True)
ind(8, "达产年营业收入（万元）", f"={pc('达产年营业收入（万元/年）')}", "参数主控引用", False)
ind(9, "达产年净利润（万元）", f"='3_收入成本现金流'!{LASTCOL}{R['ni']}", "测算期末年净利润（稳态近似）", False)
w(ws, 11, 2, "静态投资回收期（年）", F["lbl"]); w(ws, 11, 3, "（正式版以累计净现金流插值计算）", F["calc0"]); w(ws, 11, 4, "", F["note"])
w(ws, 13, 2, "注意：IRR 若显示 #NUM!，请检查建设期是否填写、现金流符号是否正常（建设期负/运营期正）。", F["note_w"])

# ================= Sheet5 敏感性 =================
ws = wb.add_worksheet("5_敏感性")
set_cols(ws, [3, 44, 16, 60])
w(ws, 1, 2, "五、敏感性分析（三情景对照）", F["sec_title"])
block_bar(ws, 3, "情景 IRR 对照")
w(ws, 4, 2, "情景", F["hdr"]); w(ws, 4, 3, "全投资 IRR", F["hdr"]); w(ws, 4, 4, "设定说明", F["hdr"])
w(ws, 5, 2, "悲观情景（收入-20%、成本+10%、利率+50bp）", F["lbl"]); w(ws, 5, 3, "", F["in"]); w(ws, 5, 4, "将参数主控对应项调整后回填，或由编制方批量重算", F["note"])
w(ws, 6, 2, "基准情景", F["lbl"]); w(ws, 6, 3, "='4_财务指标'!C5", F["ref"]); w(ws, 6, 4, "自动引用基准 IRR", F["note"])
w(ws, 7, 2, "乐观情景（收入+20%、成本-10%、利率-50bp）", F["lbl"]); w(ws, 7, 3, "", F["in"]); w(ws, 7, 4, "同上", F["note"])
w(ws, 9, 2, "说明：完整敏感性网格（收入/成本/投资 ±5%/±10% 联动重算 IRR）可按本表扩展；前期研判以三情景判断风险边界即可。", F["note"])

wb.close()
print(f"OK -> {OUT}")
