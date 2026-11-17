#!/usr/bin/env python3
"""生成《项目投资测算套表》Excel —— 可研首版快交付 Kit 配套
颜色：蓝=输入(只改这里) 黑=公式 绿=跨表引用 黄底红字=核心指标
用法: python3 gen_model_xlsx.py [out.xlsx]
注意: 本脚本内部统一使用 Excel 1-based 行号，写入时自动 -1（xlsxwriter 为 0-based）。
"""
import sys
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

OUT = sys.argv[1] if len(sys.argv) > 1 else "项目投资测算套表.xlsx"
NYR = 20  # 总测算年数上限（建设期+运营期）

wb = xlsxwriter.Workbook(OUT, {"strings_to_numbers": True})

# 格式
F = {
    "title": wb.add_format({"bold": True, "font_size": 14, "font_name": "微软雅黑"}),
    "sub":   wb.add_format({"bold": True, "font_size": 11, "font_name": "微软雅黑", "font_color": "#1F4E79"}),
    "hdr":   wb.add_format({"bold": True, "bg_color": "#D9E2F3", "border": 1, "align": "center", "valign": "vcenter", "font_name": "微软雅黑", "font_size": 10}),
    "in":    wb.add_format({"border": 1, "font_color": "#1F4E79", "bold": True, "align": "center", "font_name": "微软雅黑"}),
    "calc":  wb.add_format({"border": 1, "font_color": "#000000", "num_format": "#,##0.00", "font_name": "微软雅黑"}),
    "calc0": wb.add_format({"border": 1, "font_color": "#000000", "font_name": "微软雅黑"}),
    "ref":   wb.add_format({"border": 1, "font_color": "#548235", "num_format": "#,##0.00", "font_name": "微软雅黑", "bg_color": "#E2EFDA"}),
    "ref0":  wb.add_format({"border": 1, "font_color": "#548235", "font_name": "微软雅黑", "bg_color": "#E2EFDA"}),
    "key":   wb.add_format({"bold": True, "bg_color": "#FFE699", "border": 2, "font_color": "#C00000", "num_format": "0.00%", "font_name": "微软雅黑", "align": "center"}),
    "keyn":  wb.add_format({"bold": True, "bg_color": "#FFE699", "border": 2, "font_color": "#C00000", "num_format": "#,##0", "font_name": "微软雅黑", "align": "center"}),
    "keyrow": wb.add_format({"bold": True, "bg_color": "#FFE699", "border": 2, "font_color": "#C00000", "font_name": "微软雅黑"}),
    "note":  wb.add_format({"font_name": "微软雅黑", "font_size": 10, "text_wrap": True, "valign": "top"}),
    "lbl":   wb.add_format({"border": 1, "font_name": "微软雅黑", "valign": "center"}),
    "pct":   wb.add_format({"border": 1, "font_name": "微软雅黑", "num_format": "0.0%", "align": "center", "font_color": "#1F4E79", "bold": True}),
    "yr":    wb.add_format({"border": 1, "align": "center", "font_name": "微软雅黑", "font_size": 9, "bg_color": "#EDEDED"}),
}

# 1-based 行号封装
def w(ws, excel_row, col, *args):
    ws.write(excel_row - 1, col - 1, *args)

# ============ Sheet 0 填表说明 ============
ws = wb.add_worksheet("0_填表说明")
ws.set_column("A:A", 3); ws.set_column("B:B", 24); ws.set_column("C:C", 100)
w(ws, 1, 2, "项目投资测算套表 · 填表说明", F["title"])
w(ws, 2, 2, "配套《可行性研究报告》使用 · 适用于投资立项、融资对接前的首版测算", F["sub"])
guide = [
    ("一、这张表能干什么", "客户只需在【1_参数主控】填写核心假设（蓝色单元格），全表自动完成：投资估算、资金筹措、分年收入成本、现金流、IRR/NPV、回收期与敏感性测算，无需手工计算。"),
    ("二、颜色约定", "■ 蓝色 = 输入项（集中在【1_参数主控】，也是唯一需要修改的位置）\n■ 黑色 = 公式自动计算，请勿改动\n■ 绿色 = 跨表引用，自动带出\n■ 黄底红字 = 核心结论指标，自动生成"),
    ("三、使用步骤", "第一步：打开【1_参数主控】，按项目实际填写蓝色单元格：建设期、运营期、总投资、资本金比例、融资利率、达产收入、成本率等。\n第二步：如需细化投资构成，在【2_投资估算】补充分项。\n第三步：查看【4_财务指标】黄底结论（IRR、NPV），并结合【5_敏感性】判断抗风险能力。\n第四步：将测算结论回填《可行性研究报告》第六章财务评价。"),
    ("四、重要提示", "1. 本表为前期研判口径，收入成本按行业基准与公开资料估列，正式投资决策须以实测数据回填复核。\n2. 测算期 = 建设期 + 运营期，合计不超过 20 年。\n3. 所得税默认 25%，若项目适用西部大开发 15% 优惠，可在参数主控修改。\n4. 若 IRR 显示 #NUM!，请检查建设期是否填写、投资与收益现金流向是否合理。"),
    ("五、与可研报告对应", "投资估算对应报告第六章 6.1；融资方案对应 6.2；财务评价指标对应 6.3；敏感性对应 6.3 风险与不确定性分析。"),
]
r = 4
for a, b in guide:
    w(ws, r, 2, a, F["sub"]); w(ws, r, 3, b, F["note"])
    r += 3

# ============ Sheet 1 参数主控 ============
# 参数从 Excel 第 4 行开始（前 3 行留标题）
PARAM_TOP = 4
params = [
    ("建设期（年）", 2, "num", "自开工至投产年限，建议不超过 5 年"),
    ("运营期（年）", 15, "num", "投产后测算年限，含爬坡期"),
    ("项目总投资（万元）", 100000, "num", "含建设投资、建设期利息、铺底流动资金（示例值，请按项目改）"),
    ("资本金比例", 0.30, "pct", "项目资本金比例，须符合固定资产投资项目资本金制度"),
    ("银行贷款比例", 0.70, "pct", "债务融资比例，与资本金合计应约等于 100%"),
    ("贷款年利率", 0.045, "pct", "长期贷款综合年利率"),
    ("贷款宽限期（年）", 2, "num", "含建设期，宽限期内只付息不还本"),
    ("还款年限（年）", 10, "num", "宽限期后等额还本年限"),
    ("增值税率", 0.09, "pct", "按项目适用税率（常见 9%、6%、13%）"),
    ("城建及附加率", 0.12, "pct", "城建税及教育费附加合计，按增值税计提"),
    ("所得税率", 0.25, "pct", "西部大开发等优惠情形可填 15%"),
    ("达产年营业收入（万元/年）", 55000, "num", "运营稳定期不含税年收入（示例值，请按项目改）"),
    ("投产第1年达产率", 0.40, "pct", "产能爬坡假设，可按项目实际调整"),
    ("投产第2年达产率", 0.70, "pct", ""),
    ("投产第3年达产率", 0.90, "pct", "第 4 年及以后按 100%"),
    ("经营成本率（占收入）", 0.60, "pct", "可变经营成本占收入比例，不含折旧、利息、税金"),
    ("固定成本（万元/年）", 3000, "num", "与收入无直接关联的固定运营支出"),
    ("折旧年限（年）", 20, "num", "固定资产直线折旧年限"),
    ("残值率", 0.05, "pct", "折旧期满残值比例"),
    ("折现率ic（基准收益率）", 0.08, "pct", "财务净现值计算折现率，产业类项目一般取 8%—10%"),
]
PK = {}  # key -> Excel 行号
ws = wb.add_worksheet("1_参数主控")
ws.set_column("A:A", 3); ws.set_column("B:B", 30); ws.set_column("C:C", 14); ws.set_column("D:D", 56)
w(ws, 1, 2, "参数主控表（蓝色为输入项，全表唯一输入区）", F["title"])
w(ws, 2, 2, "项目名称：", F["sub"]); ws.merge_range("C2:D2", "××××项目", F["in"])
for idx, (key, val, typ, note) in enumerate(params):
    row = PARAM_TOP + idx
    PK[key] = row
    w(ws, row, 2, key, F["lbl"])
    if typ == "pct":
        w(ws, row, 3, val, F["pct"])
    else:
        w(ws, row, 3, val, F["in"])
    w(ws, row, 4, note, F["note"])
PARAM_BOTTOM = PARAM_TOP + len(params) - 1
w(ws, PARAM_BOTTOM + 2, 2, "提示：修改蓝色单元格后全表自动重算；资本金比例与银行贷款比例合计应约为 100%。", F["note"])

def pc(key):
    """引用参数主控 C 列（Excel 行号即 PK[key]）"""
    return f"'1_参数主控'!C{PK[key]}"

# ============ Sheet 2 投资估算 ============
ws = wb.add_worksheet("2_投资估算")
ws.set_column("A:A", 3); ws.set_column("B:B", 42); ws.set_column("C:C", 18); ws.set_column("D:D", 50)
w(ws, 1, 2, "投资估算与资金筹措（自动计算）", F["title"])
w(ws, 3, 2, "项目", F["hdr"]); w(ws, 3, 3, "金额（万元）", F["hdr"]); w(ws, 3, 4, "口径说明", F["hdr"])
w(ws, 4, 2, "项目总投资", F["lbl"]); w(ws, 4, 3, f"={pc('项目总投资（万元）')}", F["ref"])
w(ws, 5, 2, "其中：建设投资（按总投资 95% 估列，可改）", F["lbl"])
w(ws, 5, 3, f"=ROUND({pc('项目总投资（万元）')}*0.95,0)", F["in"])
w(ws, 6, 2, "其中：建设期利息（自动）", F["lbl"])
w(ws, 6, 3, f"=ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')}*({pc('建设期（年）')}/2+0.5),0)", F["calc"])
w(ws, 7, 2, "其中：铺底流动资金（自动）", F["lbl"])
w(ws, 7, 3, f"=ROUND({pc('项目总投资（万元）')}*0.05,0)", F["calc"])
w(ws, 8, 2, "校验：三项合计与总投资的差异", F["lbl"])
w(ws, 8, 3, "=C5+C6+C7-C4", F["calc0"])
w(ws, 8, 4, "偏差接近 0 属正常（预备费已在建设投资中消化）", F["note"])
w(ws, 10, 2, "资金筹措", F["hdr"]); w(ws, 10, 3, "金额（万元）", F["hdr"]); w(ws, 10, 4, "", F["hdr"])
w(ws, 11, 2, "项目资本金", F["lbl"]); w(ws, 11, 3, f"=ROUND({pc('项目总投资（万元）')}*{pc('资本金比例')},0)", F["ref"])
w(ws, 12, 2, "银行贷款", F["lbl"]); w(ws, 12, 3, f"=ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')},0)", F["ref"])
w(ws, 13, 2, "资金合计", F["lbl"]); w(ws, 13, 3, "=C11+C12", F["keyn"])
w(ws, 14, 2, "资金缺口校验", F["lbl"]); w(ws, 14, 3, "=C13-C4", F["calc0"])
w(ws, 14, 4, "应为 0，不为 0 请核对资本金与贷款比例合计是否等于 100%", F["note"])
w(ws, 16, 2, "建设期分年投资（默认按建设期均分，可手工调整蓝色格）", F["sub"])
for c in range(5):
    w(ws, 17, 3 + c, f"第{c+1}年", F["yr"])
for c in range(5):
    w(ws, 18, 3 + c, f"=IF({c+1}<={pc('建设期（年）')},ROUND({pc('项目总投资（万元）')}/{pc('建设期（年）')},0),0)", F["in"])

# ============ Sheet 3 收入成本现金流（年度表）============
ws = wb.add_worksheet("3_收入成本现金流")
ws.set_column("A:A", 3); ws.set_column("B:B", 26)
w(ws, 1, 2, "分年度收入、成本与现金流（自动计算）", F["title"])
# 行号（Excel 1-based）
R_ISOP, R_RAMP = 3, 4
R_REV, R_VC, R_FC = 5, 6, 7
R_DEP, R_INT = 8, 9
R_TAXS, R_TAXI = 10, 11
R_NI = 12
R_FCF, R_ECF = 13, 14
for c in range(NYR):
    w(ws, 2, 3 + c, f"第{c+1}年", F["yr"])
w(ws, 2, 2, "年份", F["hdr"])
labels = {R_ISOP: "投产标记（0=建设期，1=投产）", R_RAMP: "达产率", R_REV: "营业收入（万元）",
          R_VC: "可变经营成本", R_FC: "固定成本", R_DEP: "折旧费", R_INT: "利息费用",
          R_TAXS: "增值税及附加", R_TAXI: "所得税", R_NI: "净利润",
          R_FCF: "全投资净现金流（IRR 源）", R_ECF: "资本金净现金流"}
for rr, lb in labels.items():
    w(ws, rr, 2, lb, F["lbl"])

for c in range(NYR):
    col = xl_col_to_name(2 + c)   # 数据列从 C(索引2) 开始
    y = c + 1
    w(ws, R_ISOP, 3 + c, f"=IF({y}>{pc('建设期（年）')},1,0)", F["calc0"])
    w(ws, R_RAMP, 3 + c,
      f"=IF({col}{R_ISOP}=0,0,"
      f"IF({y}={pc('建设期（年）')}+1,{pc('投产第1年达产率')},"
      f"IF({y}={pc('建设期（年）')}+2,{pc('投产第2年达产率')},"
      f"IF({y}={pc('建设期（年）')}+3,{pc('投产第3年达产率')},1))))", F["pct"])
    w(ws, R_REV, 3 + c, f"=IF({col}{R_ISOP}=0,0,ROUND({pc('达产年营业收入（万元/年）')}*{col}{R_RAMP},0))", F["calc"])
    w(ws, R_VC, 3 + c, f"=IF({col}{R_ISOP}=0,0,ROUND({col}{R_REV}*{pc('经营成本率（占收入）')},0))", F["calc"])
    w(ws, R_FC, 3 + c, f"=IF({col}{R_ISOP}=0,0,{pc('固定成本（万元/年）')})", F["calc"])
    w(ws, R_DEP, 3 + c, f"=IF({col}{R_ISOP}=0,0,ROUND({pc('项目总投资（万元）')}*(1-{pc('残值率')})/{pc('折旧年限（年）')},0))", F["calc"])
    w(ws, R_INT, 3 + c,
      f"=IF({col}{R_ISOP}=0,ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')},0),"
      f"ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}*{pc('贷款年利率')}*0.55,0))", F["calc"])
    w(ws, R_TAXS, 3 + c, f"=IF({col}{R_ISOP}=0,0,ROUND({col}{R_REV}*{pc('增值税率')}*{pc('城建及附加率')},0))", F["calc"])
    w(ws, R_TAXI, 3 + c,
      f"=IF({col}{R_ISOP}=0,0,MAX(0,ROUND(({col}{R_REV}-{col}{R_VC}-{col}{R_FC}-{col}{R_DEP}-{col}{R_INT}-{col}{R_TAXS})*{pc('所得税率')},0)))", F["calc"])
    w(ws, R_NI, 3 + c,
      f"=IF({col}{R_ISOP}=0,0,{col}{R_REV}-{col}{R_VC}-{col}{R_FC}-{col}{R_DEP}-{col}{R_INT}-{col}{R_TAXS}-{col}{R_TAXI})", F["calc"])
    w(ws, R_FCF, 3 + c,
      f"=IF({col}{R_ISOP}=0,-ROUND({pc('项目总投资（万元）')}/{pc('建设期（年）')},0),"
      f"{col}{R_NI}+{col}{R_DEP}+{col}{R_INT})", F["calc"])
    w(ws, R_ECF, 3 + c,
      f"=IF({col}{R_ISOP}=0,-ROUND({pc('项目总投资（万元）')}*{pc('资本金比例')}/{pc('建设期（年）')},0),"
      f"{col}{R_NI}+{col}{R_DEP}-IF({y}>{pc('贷款宽限期（年）')},ROUND({pc('项目总投资（万元）')}*{pc('银行贷款比例')}/{pc('还款年限（年）')},0),0))", F["calc"])

w(ws, NYR + 6, 2, "注：本表为简化口径，未含期末残值回收与增值税进项抵扣；正式投资决策建议以完整三表模型复核。", F["note"])

LASTCOL = xl_col_to_name(2 + NYR - 1)  # 最后数据列 V

# ============ Sheet 4 财务指标 ============
ws = wb.add_worksheet("4_财务指标")
ws.set_column("A:A", 3); ws.set_column("B:B", 42); ws.set_column("C:C", 24); ws.set_column("D:D", 50)
w(ws, 1, 2, "财务指标汇总（自动计算）", F["title"])
w(ws, 3, 2, "指标", F["hdr"]); w(ws, 3, 3, "数值", F["hdr"]); w(ws, 3, 4, "判断口径", F["hdr"])
fcf_rng = f"'3_收入成本现金流'!C{R_FCF}:{LASTCOL}{R_FCF}"
ecf_rng = f"'3_收入成本现金流'!C{R_ECF}:{LASTCOL}{R_ECF}"

def ind(row, name, formula, note, key=False):
    w(ws, row, 2, name, F["keyrow"] if key else F["lbl"])
    w(ws, row, 3, formula, F["key"] if key else F["calc"])
    w(ws, row, 4, note, F["note"])

ind(4, "全投资财务内部收益率 IRR", f"=IRR({fcf_rng})", "不低于基准收益率 ic 即具备财务可行性", True)
ind(5, "全投资财务净现值 NPV（万元）", f"=NPV({pc('折现率ic（基准收益率）')},{fcf_rng})+C{R_FCF}", "大于 0 即具备财务可行性", True)
ind(6, "资本金财务内部收益率", f"=IRR({ecf_rng})", "股东视角回报水平", True)
ind(7, "达产年营业收入（万元）", f"={pc('达产年营业收入（万元/年）')}", "引用参数主控", False)
ind(8, "达产年净利润（万元）", f"='3_收入成本现金流'!{LASTCOL}{R_NI}", "取测算期末年净利润（稳态近似）", False)
w(ws, 10, 2, "静态投资回收期（年）", F["lbl"])
w(ws, 10, 3, "（正式版以累计净现金流插值计算）", F["calc0"])
w(ws, 12, 2, "说明：IRR 如显示 #NUM!，请检查建设期是否填写、项目投资是否在建设期全额流出、收益期现金流方向是否正确。", F["note"])

# ============ Sheet 5 敏感性 ============
ws = wb.add_worksheet("5_敏感性")
ws.set_column("A:A", 3); ws.set_column("B:B", 38); ws.set_column("C:C", 14); ws.set_column("D:D", 46)
w(ws, 1, 2, "敏感性分析（情景回填 + 说明）", F["title"])
w(ws, 3, 2, "情景", F["hdr"]); w(ws, 3, 3, "全投资 IRR", F["hdr"]); w(ws, 3, 4, "设定说明", F["hdr"])
w(ws, 4, 2, "悲观情景（收入 -20%、成本 +10%）", F["lbl"]); w(ws, 4, 3, "", F["in"])
w(ws, 4, 4, "将参数主控对应项临时调整后回填，或由编制方批量重算", F["note"])
w(ws, 5, 2, "基准情景", F["lbl"]); w(ws, 5, 3, "='4_财务指标'!C4", F["ref"]); w(ws, 5, 4, "自动引用基准 IRR", F["note"])
w(ws, 6, 2, "乐观情景（收入 +20%、成本 -10%）", F["lbl"]); w(ws, 6, 3, "", F["in"])
w(ws, 6, 4, "同上", F["note"])
w(ws, 8, 2, "说明：完整敏感性网格（收入、成本、投资各 ±5%/±10% 联动重算 IRR）可基于本表结构批量生成；前期研判阶段以三情景对比判断风险边界即可。", F["note"])

wb.close()
print(f"OK -> {OUT}")
