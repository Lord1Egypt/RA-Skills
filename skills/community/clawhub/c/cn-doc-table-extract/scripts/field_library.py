#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""共享字段库与解析工具 —— 被 extract_tables.py 与 validate_fields.py 复用。

本模块只依赖 Python 标准库，因此即使 pdfplumber / openpyxl / python-docx /
pandas 全部缺失，抽取结果的校验环节依然可以运行。

内容分三部分：
1. 文本归一化（全角转半角、去空白、去货币符号）
2. 金额 / 日期解析（支持千分位、全角、人民币符号、年月日中文写法）
3. 文档画像（profile）与字段别名表（中英对照）

字段别名的权威说明见 references/chinese-document-field-library.md。
"""
from __future__ import annotations

import datetime as _dt
import re

# --------------------------------------------------------------------------
# 1. 文本归一化
# --------------------------------------------------------------------------

#: 表示"无金额 / 无日期"的中文占位符
NULL_TOKENS = {
    "", "-", "--", "—", "——", "—— ", "/", "\\", "n/a", "na", "null", "none",
    "无", "无金额", "不适用", "空", "略", "见附注", "见备注", "待定", "待补充",
}

#: 金额字段中需要剥除的货币标识
CURRENCY_TOKENS = [
    "人民币", "RMB", "CNY", "rmb", "cny", "¥", "￥", "$", "＄", "元", "圆",
]

_FULLWIDTH_OFFSET = 0xFEE0


def normalize_text(value) -> str:
    """全角转半角 + 去除多余空白 + 统一标点。"""
    if value is None:
        return ""
    if isinstance(value, (_dt.datetime, _dt.date)):
        return format_datetime(value)
    text = str(value)
    out = []
    for ch in text:
        code = ord(ch)
        if code == 0x3000:  # 全角空格
            out.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:  # 全角 ASCII
            out.append(chr(code - _FULLWIDTH_OFFSET))
        elif code == 0x00A0:  # 不换行空格
            out.append(" ")
        else:
            out.append(ch)
    text = "".join(out)
    # 常见中文标点统一
    text = text.replace("：", ":").replace("，", ",").replace("；", ";")
    text = text.replace("（", "(").replace("）", ")").replace("　", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_datetime(value) -> str:
    if isinstance(value, _dt.datetime):
        if value.hour or value.minute or value.second:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value.strftime("%Y-%m-%d")
    if isinstance(value, _dt.date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def normalize_header(value) -> str:
    """表头归一化：去空白、去尾部冒号、转小写，用于别名匹配。"""
    text = normalize_text(value)
    text = text.rstrip(":：")
    text = text.replace(" ", "").replace("\u200b", "")
    return text.lower()


def is_null_token(value) -> bool:
    """判断一个单元格是否表示"空 / 无值"。"""
    return normalize_text(value).lower() in NULL_TOKENS


# --------------------------------------------------------------------------
# 2. 金额解析
# --------------------------------------------------------------------------

_AMOUNT_RE = re.compile(r"^-?\d+(\.\d+)?$")


def parse_amount(raw):
    """解析金额。

    返回 ``(value, status, note)``：
      value  —— float 或 None
      status —— "ok" / "missing" / "invalid" / "ambiguous"
      note   —— 可选的补充说明（如单位为万元、格式存疑）

    支持：千分位、全角数字、人民币符号、CNY/RMB 前缀与后缀、
    会计负数括号、尾随负号、欧洲式 ``1.234,56``。
    拒绝：``12.3.4``、``1,2,3``、``abc`` 等不自洽写法。
    """
    if raw is None:
        return None, "missing", None
    if isinstance(raw, bool):
        return None, "invalid", "boolean is not an amount"
    if isinstance(raw, (int, float)):
        return float(raw), "ok", None
    if isinstance(raw, (_dt.datetime, _dt.date)):
        return None, "invalid", "date value in an amount column"

    text = normalize_text(raw)
    if text.lower() in NULL_TOKENS:
        return None, "missing", None

    negative = False
    note = None

    # 会计负数 (1,234.56)
    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1].strip()
    # 尾随负号 1234.56-
    if text.endswith("-"):
        negative = True
        text = text[:-1].strip()
    # 前导负号
    if text.startswith("-"):
        negative = True
        text = text[1:].strip()

    # 剥离货币标识与单位
    for token in CURRENCY_TOKENS:
        if token in text:
            if token in ("元", "圆") and "万元" in text:
                note = "unit_wan_yuan"
            text = text.replace(token, "")
    text = text.replace(" ", "").replace("\u00a0", "")

    if text.lower() in NULL_TOKENS:
        return None, "missing", None
    if not text:
        return None, "missing", None

    has_comma = "," in text
    has_dot = "." in text

    if has_comma and has_dot:
        # 取最后出现的分隔符作为小数点
        if text.rfind(",") > text.rfind("."):
            # 欧洲式：1.234,56
            if not re.match(r"^\d{1,3}(\.\d{3})*,\d{1,2}$", text):
                return None, "invalid", "mixed separators are inconsistent"
            text = text.replace(".", "").replace(",", ".")
        else:
            # 中国/美国式：1,234.56
            if not re.match(r"^-?\d{1,3}(,\d{3})*(\.\d{1,2})?$", text):
                return None, "invalid", "mixed separators are inconsistent"
            text = text.replace(",", "")
    elif has_comma:
        groups = text.split(",")
        if len(groups) == 2 and len(groups[1]) == 3 and groups[0].isdigit():
            # 1,234 -> 千分位
            text = groups[0] + groups[1]
        elif len(groups) == 2 and len(groups[1]) == 2 and groups[0].isdigit():
            # 1,23 -> 欧洲式小数
            text = groups[0] + "." + groups[1]
        elif len(groups) > 2 and all(len(g) == 3 for g in groups[1:]) and groups[0].isdigit():
            text = "".join(groups)
        else:
            return None, "invalid", "comma grouping is inconsistent"
    elif has_dot:
        groups = text.split(".")
        if len(groups) > 2:
            return None, "invalid", "too many decimal points"
        if len(groups) == 2 and len(groups[1]) == 3 and groups[0].isdigit():
            # 1.234 既可能是 1234 也可能是 1.234
            value = float(text)
            note = "ambiguous_grouping"
            return (-value if negative else value), "ambiguous", note
        if not re.match(r"^\d+(\.\d+)?$", text):
            return None, "invalid", "not a numeric string"

    if not re.match(r"^\d+(\.\d+)?$", text):
        return None, "invalid", "not a numeric string"

    value = float(text)
    if negative:
        value = -value
    return value, "ok", note


# --------------------------------------------------------------------------
# 3. 日期解析
# --------------------------------------------------------------------------

_DATE_PATTERNS = [
    (re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$"), "ymd"),
    (re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})$"), "ymd"),
    (re.compile(r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$"), "ymd"),
    (re.compile(r"^(\d{4})年(\d{1,2})月(\d{1,2})日$"), "ymd"),
    (re.compile(r"^(\d{4})年(\d{1,2})月$"), "ym"),
    (re.compile(r"^(\d{4})(\d{2})(\d{2})$"), "ymd"),
]

#: 明确视为"无法自动判定"的写法
AMBIGUOUS_DATE_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}$")


def parse_date(raw):
    """解析日期。

    返回 ``(iso_string_or_None, status, note)``：
      status —— "ok" / "missing" / "invalid" / "ambiguous"
    不合法日期（如 2024年2月30日）与歧义日期（01/02/2024）一律返回 None。
    """
    if raw is None:
        return None, "missing", None
    if isinstance(raw, _dt.datetime):
        return raw.strftime("%Y-%m-%d"), "ok", None
    if isinstance(raw, _dt.date):
        return raw.strftime("%Y-%m-%d"), "ok", None

    text = normalize_text(raw)
    if text.lower() in NULL_TOKENS:
        return None, "missing", None

    # 带时间的先截断
    head = re.split(r"[ T]", text)[0]
    if head != text and not head:
        head = text

    if AMBIGUOUS_DATE_RE.match(text):
        return None, "ambiguous", "day/month order cannot be determined"

    for pattern, kind in _DATE_PATTERNS:
        m = pattern.match(text)
        if not m:
            continue
        if kind == "ym":
            year, month, day = int(m.group(1)), int(m.group(2)), 1
            note = "day_defaulted"
        else:
            year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
            note = None
        try:
            _dt.date(year, month, day)
        except ValueError:
            return None, "invalid", "not a real calendar date"
        return "%04d-%02d-%02d" % (year, month, day), "ok", note

    return None, "invalid", "unrecognised date format"


# --------------------------------------------------------------------------
# 4. 文档画像与字段别名
# --------------------------------------------------------------------------

#: canonical key -> (中文原文, English label)
FIELD_LABELS = {
    # 通用
    "date": ("日期", "date"),
    "amount": ("金额", "amount"),
    "quantity": ("数量", "quantity"),
    "unit_price": ("单价", "unit price"),
    "remarks": ("备注", "remarks"),
    # 对账单
    "transaction_date": ("交易日期", "transaction date"),
    "summary": ("摘要", "summary"),
    "debit_amount": ("借方发生额", "debit amount"),
    "credit_amount": ("贷方发生额", "credit amount"),
    "balance": ("余额", "balance"),
    "counterparty": ("对方户名", "counterparty"),
    "counterparty_account": ("对方账号", "counterparty account"),
    "account_no": ("本方账号", "account no"),
    "currency": ("币种", "currency"),
    "transaction_no": ("流水号", "transaction no"),
    # 发票
    "invoice_code": ("发票代码", "invoice code"),
    "invoice_number": ("发票号码", "invoice number"),
    "issue_date": ("开票日期", "issue date"),
    "tax_amount": ("税额", "tax amount"),
    "total_amount": ("价税合计", "total amount"),
    "seller": ("销方名称", "seller"),
    "seller_tax_id": ("销方税号", "seller tax id"),
    "buyer": ("购方名称", "buyer"),
    "buyer_tax_id": ("购方税号", "buyer tax id"),
    "drawer": ("开票人", "drawer"),
    "item_name": ("项目名称", "item name"),
    "tax_rate": ("税率", "tax rate"),
    # 保单
    "policy_no": ("保单号", "policy no"),
    "policyholder": ("投保人", "policyholder"),
    "insured": ("被保人", "insured"),
    "subject": ("保险标的", "subject"),
    "coverage": ("保险责任", "coverage"),
    "sum_insured": ("保额", "sum insured"),
    "premium": ("保费", "premium"),
    "payment_term": ("缴费期", "payment term"),
    "effective_date": ("生效日期", "effective date"),
    "expiry_date": ("到期日期", "expiry date"),
    "payment_mode": ("缴费方式", "payment mode"),
    "insurer": ("保险公司", "insurer"),
    "agent": ("业务员", "agent"),
    # 工资表
    "name": ("姓名", "name"),
    "employee_no": ("工号", "employee no"),
    "id_no": ("身份证号", "id no"),
    "department": ("部门", "department"),
    "position": ("岗位", "position"),
    "gross_pay": ("应发工资", "gross pay"),
    "deduction_total": ("扣款合计", "deduction total"),
    "income_tax": ("个人所得税", "income tax"),
    "social_insurance": ("社保个人", "social insurance"),
    "housing_fund": ("公积金个人", "housing fund"),
    "net_pay": ("实发工资", "net pay"),
    "bank_account": ("银行账号", "bank account"),
    "hire_date": ("入职日期", "hire date"),
    # 物流 / 报关
    "waybill_no": ("运单号", "waybill no"),
    "shipper": ("发货人", "shipper"),
    "consignee": ("收货人", "consignee"),
    "goods_name": ("品名", "goods name"),
    "gross_weight": ("毛重", "gross weight"),
    "net_weight": ("净重", "net weight"),
    "volume": ("体积", "volume"),
    "freight": ("运费", "freight"),
    "origin": ("起运地", "origin"),
    "destination": ("目的地", "destination"),
    "declaration_no": ("报关单号", "declaration no"),
    "hs_code": ("商品编号", "HS code"),
    "trade_term": ("成交方式", "trade term"),
    "origin_country": ("原产地", "origin country"),
}

#: canonical key -> 该字段接受的表头写法（中英混排，匹配前会先做归一化）
FIELD_ALIASES = {
    "transaction_date": ["交易日期", "交易日", "记账日期", "交易时间", "日期", "交易发生日期"],
    "summary": ["摘要", "交易摘要", "摘要说明", "交易类型", "用途", "附言"],
    "debit_amount": ["借方发生额", "借方金额", "借方", "支出金额", "付出金额", "支出", "转出金额"],
    "credit_amount": ["贷方发生额", "贷方金额", "贷方", "收入金额", "存入金额", "收入", "转入金额"],
    "amount": ["发生额", "交易金额", "金额", "交易额", "金额(元)", "金额（元）"],
    "balance": ["余额", "账户余额", "本方余额", "联方余额", "余额(元)"],
    "counterparty": ["对方户名", "对方账户名称", "对方账户名", "对方单位名称", "交易对手", "收款人", "付款人", "对方姓名"],
    "counterparty_account": ["对方账号", "对方账户", "交易对手账号", "对方卡号"],
    "account_no": ["本方账号", "本方账户", "账号", "卡号", "账户账号", "本方帐号"],
    "currency": ["币种", "货币", "货币代码", "钞汇标志"],
    "transaction_no": ["流水号", "交易流水号", "凭证号", "业务编号", "参考号", "回单编号", "交易序号"],
    "invoice_code": ["发票代码", "票据代码", "发票编码"],
    "invoice_number": ["发票号码", "票据号码", "发票号", "票据号", "发票流水号"],
    "issue_date": ["开票日期", "填开日期", "开具日期", "出发日期", "开具时间"],
    "tax_amount": ["税额", "合计税额", "增值税额", "税额合计", "增值税"],
    "total_amount": ["价税合计", "价税合计金额", "价税总计", "小写合计", "合计金额"],
    "seller": ["销方名称", "销售方名称", "销售方", "销方", "收款方", "销售方(盖章)"],
    "seller_tax_id": ["销方纳税人识别号", "销售方纳税人识别号", "纳税人识别号", "税号", "统一社会信用代码", "销方税号"],
    "buyer": ["购方名称", "购买方名称", "购买方", "购方", "付款方", "购买方(盖章)"],
    "buyer_tax_id": ["购方纳税人识别号", "购买方纳税人识别号", "购方税号"],
    "drawer": ["开票人", "制单人", "复核人", "开票人(签名)"],
    "item_name": ["项目名称", "货物或应税劳务、服务名称", "商品名称", "品名", "货物名称", "名称"],
    "quantity": ["数量", "件数", "台数", "数量(件)", "数量（件）", "申报数量", "成交数量"],
    "unit_price": ["单价", "单价(元)", "单价（元）", "成交单价", "申报单价"],
    "tax_rate": ["税率", "税率(%)", "税率（%）", "征收率"],
    "remarks": ["备注", "备注栏", "附加说明"],
    "policy_no": ["保单号", "保单号码", "保险单号", "合同号", "保险合同号", "保单号/合同号"],
    "policyholder": ["投保人", "投保人名称", "投保人姓名", "客户名称", "投保单位"],
    "insured": ["被保人", "被保险人", "被保险人名称", "被保人姓名", "保险受益人"],
    "subject": ["保险标的", "标的", "保险标的名称", "承保标的"],
    "coverage": ["保险责任", "保险责任范围", "承保范围"],
    "sum_insured": ["保额", "保险金额", "保险金额(元)", "保险金额（万元）", "保险金额(万元)", "责任限额", "累计责任限额"],
    "premium": ["保费", "保险费", "保险费(元)", "年保费", "保费合计", "期缴保费"],
    "payment_term": ["缴费期", "缴费期间", "缴费期限", "交费期间", "保险期间", "保障期间", "保险期限"],
    "effective_date": ["生效日期", "保险起期", "起保日期", "生效日", "起始日期", "起期"],
    "expiry_date": ["到期日期", "保险止期", "终止日期", "终保日期", "失效日期", "止期"],
    "payment_mode": ["缴费方式", "交费方式", "支付方式", "交费年期"],
    "insurer": ["保险公司", "承保公司", "保险人", "保险机构"],
    "agent": ["业务员", "代理人", "保险经纪人", "营销员", "展业人员"],
    "name": ["姓名", "员工姓名", "职工姓名", "人员姓名", "名字"],
    "employee_no": ["工号", "员工工号", "员工编号", "人员编号", "职工号", "序号"],
    "id_no": ["身份证号", "身份证号码", "公民身份号码", "证件号码", "身份证"],
    "department": ["部门", "所属部门", "部门名称", "中心", "所属中心"],
    "position": ["岗位", "职位", "岗位名称", "职务"],
    "gross_pay": ["应发工资", "应发合计", "工资总额", "应发金额", "应发工资合计", "应发薪酬"],
    "deduction_total": ["扣款合计", "扣款小计", "扣款总额", "各项扣款合计", "扣款金额合计"],
    "income_tax": ["个人所得税", "个税", "所得税", "代扣个税", "个人所得税(元)", "扣个人所得税"],
    "social_insurance": ["社保", "社保个人", "个人社保", "养老保险", "医疗保险个人", "社保(个人)", "个人社保合计"],
    "housing_fund": ["公积金", "住房公积金", "个人公积金", "公积金个人", "个人公积金合计"],
    "net_pay": ["实发工资", "实发合计", "实发金额", "税后工资", "实发薪酬"],
    "bank_account": ["银行账号", "银行卡号", "工资卡号", "账号", "银行帐号"],
    "hire_date": ["入职日期", "入职时间", "参加工作日期"],
    "waybill_no": ["运单号", "运单号码", "货运单号", "物流单号", "提单号", "快递单号"],
    "shipper": ["发货人", "发货方", "托运人", "寄件人", "卖方"],
    "consignee": ["收货人", "收货方", "收货单位", "收件人", "买方"],
    "goods_name": ["品名", "货物名称", "商品名称", "物品名称", "货品名称"],
    "gross_weight": ["毛重", "毛重(kg)", "毛重（kg）", "总重", "重量"],
    "net_weight": ["净重", "净重(kg)", "净重（kg）", "净重量"],
    "volume": ["体积", "体积(m3)", "体积（m3）", "材积"],
    "freight": ["运费", "运杂费", "物流费用", "运输费用", "费用合计"],
    "origin": ["起运地", "发货地", "起运站"],
    "destination": ["目的地", "到达地", "目的站", "收货地"],
    "declaration_no": ["报关单号", "海关单号", "进出口报关单号", "报关单号码"],
    "hs_code": ["商品编号", "hs编码", "商品编码", "海关编码", "税则号列", "商品hs编码"],
    "trade_term": ["成交方式", "贸易方式", "交货方式"],
    "origin_country": ["原产地", "原产国"],
    "date": ["日期", "年月日"],
}

#: 画像定义：必填字段 + 参与合计校验的字段 + 标识符字段
PROFILES = {
    "bank_statement": {
        "zh": "银行对账单 / 交易明细",
        "required": ["transaction_date"],
        "one_of": [["debit_amount", "credit_amount", "amount"]],
        "amount_fields": ["debit_amount", "credit_amount", "amount", "balance"],
        "date_fields": ["transaction_date"],
        "id_fields": ["transaction_no", "account_no", "counterparty_account"],
        "unique_id_fields": ["transaction_no"],
        "key_fields": ["transaction_date", "debit_amount", "credit_amount", "counterparty"],
        "footer_keywords": ["合计", "小计", "总计", "共计", "本页合计", "合 计", "累计"],
        "arithmetic": [],
    },
    "vat_invoice": {
        "zh": "增值税发票 / 收据",
        "required": ["invoice_number", "issue_date", "seller"],
        "one_of": [["amount", "total_amount"]],
        "amount_fields": ["amount", "tax_amount", "total_amount"],
        "date_fields": ["issue_date"],
        "id_fields": ["invoice_number", "invoice_code", "seller_tax_id", "buyer_tax_id"],
        "unique_id_fields": ["invoice_number"],
        "key_fields": ["invoice_number", "issue_date", "seller", "amount"],
        "footer_keywords": ["价税合计", "合计", "小计", "总计"],
        "arithmetic": [{"rule": "total_not_additive", "level": "error",
                        "add": ["amount", "tax_amount"], "equals": "total_amount",
                        "hint": "价税合计必须等于金额加税额，请回原文核对三处数字"}],
    },
    "insurance_policy": {
        "zh": "保单 / 保险合同",
        "required": ["policy_no", "policyholder", "insured", "sum_insured", "premium", "payment_term", "effective_date"],
        "one_of": [],
        "amount_fields": ["sum_insured", "premium", "freight"],
        "date_fields": ["effective_date", "expiry_date"],
        "id_fields": ["policy_no", "agent"],
        "unique_id_fields": ["policy_no"],
        "key_fields": ["policy_no"],
        "footer_keywords": ["合计", "小计", "总计", "共计"],
        "arithmetic": [],
    },
    "payroll": {
        "zh": "工资表 / 社保公积金表",
        "required": ["name", "employee_no", "gross_pay", "net_pay"],
        "one_of": [],
        "amount_fields": ["gross_pay", "deduction_total", "income_tax", "social_insurance", "housing_fund", "net_pay"],
        "date_fields": ["hire_date"],
        "id_fields": ["employee_no", "id_no", "bank_account"],
        "unique_id_fields": ["employee_no"],
        "key_fields": ["employee_no", "name"],
        "footer_keywords": ["合计", "小计", "总计", "共计"],
        "arithmetic": [{"rule": "payroll_not_additive", "level": "warning",
                        "add": ["gross_pay"], "subtract": ["deduction_total"], "equals": "net_pay",
                        "hint": "实发工资应等于应发工资减扣款合计，请核对扣款项是否漏抽"}],
    },
    "logistics": {
        "zh": "物流运单 / 招投标明细",
        "required": ["waybill_no", "shipper", "consignee", "goods_name", "quantity"],
        "one_of": [],
        "amount_fields": ["freight", "quantity", "unit_price", "amount"],
        "date_fields": [],
        "id_fields": ["waybill_no"],
        "unique_id_fields": ["waybill_no"],
        "key_fields": ["waybill_no", "goods_name", "quantity"],
        "footer_keywords": ["合计", "小计", "总计", "共计"],
        "arithmetic": [{"rule": "line_amount_mismatch", "level": "warning",
                        "multiply": ["quantity", "unit_price"], "equals": "amount",
                        "hint": "数量乘单价应等于金额，请核对数量与单价是否串行"}],
    },
    "customs": {
        "zh": "报关单",
        "required": ["declaration_no", "hs_code", "quantity", "amount", "currency"],
        "one_of": [],
        "amount_fields": ["amount", "quantity", "unit_price"],
        "date_fields": [],
        "id_fields": ["declaration_no", "hs_code"],
        "unique_id_fields": ["declaration_no"],
        "key_fields": ["declaration_no", "hs_code", "quantity", "unit_price"],
        "footer_keywords": ["合计", "小计", "总计", "共计"],
        "arithmetic": [],
    },
    "generic": {
        "zh": "通用明细表",
        "required": [],
        "one_of": [],
        "amount_fields": [],
        "date_fields": [],
        "id_fields": [],
        "unique_id_fields": [],
        "key_fields": [],
        "footer_keywords": ["合计", "小计", "总计", "共计"],
        "arithmetic": [],
    },
}

#: 反向索引：归一化别名 -> canonical key
ALIAS_INDEX = {}
for _key, _aliases in FIELD_ALIASES.items():
    for _alias in _aliases:
        ALIAS_INDEX.setdefault(normalize_header(_alias), _key)
# 补充：中文原文本身也作为别名
for _key, (_zh, _en) in FIELD_LABELS.items():
    ALIAS_INDEX.setdefault(normalize_header(_zh), _key)
# 补充：canonical key 本身也作为别名（下游用英文字段名做表头时可直接命中）
for _key in FIELD_LABELS:
    ALIAS_INDEX.setdefault(normalize_header(_key), _key)

#: 发票号码 / 发票代码的合法长度
INVOICE_NUMBER_LENGTHS = {8, 20}
INVOICE_CODE_LENGTHS = {10, 12}


def match_header(header, profile=None):
    """把一个原始表头映射到 canonical key。

    返回 ``(canonical_key_or_None, matched_alias)``。profile 为 None 时使用全局别名表。
    """
    norm = normalize_header(header)
    if not norm:
        return None, None
    if profile and profile in PROFILES:
        # 画像内字段优先命中，避免 "金额" 抢走 "借方发生额" 之外的语义
        for key in FIELD_ALIASES:
            if key not in PROFILES[profile]["amount_fields"] and key not in PROFILES[profile]["required"]:
                continue
            for alias in FIELD_ALIASES.get(key, []):
                if normalize_header(alias) == norm:
                    return key, alias
    key = ALIAS_INDEX.get(norm)
    if key:
        return key, norm
    # 退化匹配：包含关系（例如"借方发生额(元)"）
    for alias_norm, key in sorted(ALIAS_INDEX.items(), key=lambda kv: -len(kv[0])):
        if len(alias_norm) >= 3 and alias_norm in norm:
            return key, alias_norm
    return None, None


def get_profile(profile_key):
    if profile_key not in PROFILES:
        raise KeyError(profile_key)
    return PROFILES[profile_key]


def normalize_value(key, raw_text, profile_def):
    """按字段类型归一化一个单元格。

    返回 ``(value, status, note)``：
      status —— "ok" / "missing" / "invalid" / "ambiguous"
    归一化只作用于展示值；原文串由调用方单独保留。
    """
    if raw_text is None:
        return None, "missing", None
    text = normalize_text(raw_text)
    if is_null_token(text):
        return None, "missing", None
    if key in profile_def.get("amount_fields", []):
        value, status, note = parse_amount(text)
        if status == "missing":
            return None, "missing", None
        return value, ("ok" if status != "invalid" else "invalid"), note
    if key in profile_def.get("date_fields", []):
        return parse_date(text)
    if "date" in key or "日期" in key:
        value, status, note = parse_date(text)
        if status == "ok":
            return value, "ok", note
    return text, "ok", None


def label_for(key):
    zh, en = FIELD_LABELS.get(key, (key, key))
    return "%s / %s" % (zh, en)
