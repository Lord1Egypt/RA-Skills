#!/usr/bin/env python3
"""有限范围中国计税复算；无网络/申报接口。金额为人民币元。"""
import argparse
import calendar
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

D = Decimal
ZERO = D('0')
CENT = D('0.01')
SNAPSHOT = '2026-10-10'
ANNUAL = [(36000, '.03', 0), (144000, '.10', 2520),
          (300000, '.20', 16920), (420000, '.25', 31920),
          (660000, '.30', 52920), (960000, '.35', 85920),
          (None, '.45', 181920)]


def check(condition, message):
    if not condition:
        raise ValueError(message)


def fields(obj, required, optional=()):
    check(isinstance(obj, dict), '输入必须是对象')
    required = set(required.split())
    check(not required - obj.keys(), '缺字段: ' + ', '.join(sorted(required - obj.keys())))
    extra = obj.keys() - required - set(optional)
    check(not extra, '未知字段: ' + ', '.join(sorted(extra)))


def number(value):
    check(not isinstance(value, (bool, float)), '金额/比例请使用十进制字符串或整数')
    try:
        result = D(value)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError('无效十进制数字') from None
    check(result.is_finite(), '数字必须有限')
    check(abs(result) < D('1e18'), '数字超过本工具范围')
    return result


def money(value, signed=False):
    result = number(value)
    check(signed or result >= 0, '金额不得为负；红字/更正需专项处理')
    check(result == result.quantize(CENT), '输入金额最多两位小数，单位为元')
    return result


def flag(obj, key):
    check(type(obj[key]) is bool, key + ' 必须是布尔值')
    return obj[key]


def q(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def tax(base, monthly=False):
    base = max(base, ZERO)
    divisor = D(12) if monthly else D(1)
    for ceiling, rate, deduction in ANNUAL:
        if ceiling is None or base <= D(ceiling) / divisor:
            return {'base': base, 'rate': D(rate),
                    'quick_deduction': D(deduction) / divisor,
                    'tax': q(base * D(rate) - D(deduction) / divisor)}


def period_threshold(req, cycle):
    check(cycle in ('month', 'quarter'), 'cycle 必须为 month 或 quarter')
    start, end = date.fromisoformat(req['period_start']), date.fromisoformat(req['period_end'])
    first_month = end.month if cycle == 'month' else ((end.month - 1) // 3) * 3 + 1
    last_month = first_month if cycle == 'month' else first_month + 2
    check(start == date(end.year, first_month, 1) and
          end == date(end.year, last_month, calendar.monthrange(end.year, last_month)[1]),
          '本模式要求完整自然月/季；首期短期间或不规则期间需专项核验')
    return D(100000 if cycle == 'month' else 300000)


def annual_period(req):
    year = date.fromisoformat(req['period_end']).year
    check(req['period_start'] == f'{year}-01-01' and req['period_end'] == f'{year}-12-31',
          '本模式要求完整年度；短纳税年度需专项核验')


def small_vat(req, data):
    fields(data, 'cycle sales prepaid')
    threshold = period_threshold(req, data['cycle'])
    check(isinstance(data['sales'], list) and data['sales'], 'sales 需至少一行；零收入填明确的0行')
    rows = []
    for row in data['sales']:
        fields(row, 'net_sales rate waive_exemption')
        net, rate = money(row['net_sales']), number(row['rate'])
        check(rate in (D('.01'), D('.03')), '仅普通1%/3%小规模业务')
        rows.append((net, rate, flag(row, 'waive_exemption')))
    total = sum((r[0] for r in rows), ZERO)
    below = total < threshold  # 2026增值税法第23条，等于起征点也全额计税。
    taxable_by_rate = {r: sum((n for n, rr, w in rows if rr == r and (w or not below)), ZERO)
                       for r in (D('.01'), D('.03'))}
    breakdown = [{'rate': r, 'taxable_sales': n, 'tax': q(n * r)}
                 for r, n in taxable_by_rate.items()]
    liability = sum((r['tax'] for r in breakdown), ZERO)
    prepaid = money(data['prepaid'])
    return {'sales_total': total, 'threshold': threshold, 'below_threshold': below,
            'exempt_sales': total - sum(taxable_by_rate.values(), ZERO),
            'breakdown': breakdown, 'tax_liability': liability,
            'prepaid': prepaid, 'due': max(liability - prepaid, ZERO),
            'prepayment_balance_to_review': max(prepaid - liability, ZERO),
            'formula': '各征收率组应税不含税销售额×征收率，按组舍入后合计；再减已预缴',
            'policy_ids': ['VAT-LAW', 'VAT-2026-10', 'VAT-2026-4']}


def general_vat(req, data):
    fields(data, 'sales deductible_input input_transfer_out opening_credit prepaid')
    check(isinstance(data['sales'], list) and data['sales'], 'sales 需至少一行')
    groups = {r: ZERO for r in (D('.13'), D('.09'), D('.06'))}
    for row in data['sales']:
        fields(row, 'net_sales rate')
        rate = number(row['rate'])
        check(rate in groups, '一般模式仅普通13%/9%/6%；简易/免税/出口等另算')
        groups[rate] += money(row['net_sales'])
    breakdown = [{'rate': r, 'net_sales': n, 'output_tax': q(n * r)} for r, n in groups.items()]
    output = sum((r['output_tax'] for r in breakdown), ZERO)
    inputs = money(data['deductible_input'])
    transfer = money(data['input_transfer_out'])
    opening, prepaid = money(data['opening_credit']), money(data['prepaid'])
    balance = output + transfer - inputs - opening
    liability = max(balance, ZERO)
    return {'breakdown': breakdown, 'output_tax': output, 'input_credit': inputs,
            'input_transfer_out': transfer, 'opening_credit': opening,
            'tax_liability': liability, 'carryforward_input_credit': max(-balance, ZERO),
            'prepaid': prepaid, 'due': max(liability - prepaid, ZERO),
            'prepayment_balance_to_review': max(prepaid - liability, ZERO),
            'formula': '销项+进项转出−本期可抵扣进项−上期留抵；负数为留抵，预缴另外扣减',
            'policy_ids': ['VAT-LAW', 'VAT-REG']}


def cit(req, data):
    fields(data, 'assessment tax_base employees_average assets_average industry_allowed prepaid')
    check(data['assessment'] in ('annual', 'prepayment'), 'assessment 必须为 annual/prepayment')
    if data['assessment'] == 'annual':
        annual_period(req)
    else:
        end = date.fromisoformat(req['period_end'])
        check(req['period_start'] == f'{end.year}-01-01', '预缴基数及已预缴必须为本年累计')
    base = max(money(data['tax_base'], signed=True), ZERO)
    employees = number(data['employees_average'])
    check(employees >= 0, '从业人数不能为负')
    assets = money(data['assets_average'])
    small = flag(data, 'industry_allowed') and base <= 3000000 and employees <= 300 and assets <= 50000000
    rate = D('.05') if small else D('.25')
    liability, prepaid = q(base * rate), money(data['prepaid'])
    return {'assessment': data['assessment'], 'tax_base': base,
            'small_low_profit_eligible_on_inputs': small, 'effective_rate': rate,
            'tax_liability': liability, 'prepaid': prepaid,
            'due': max(liability - prepaid, ZERO),
            'overpayment_to_review': max(prepaid - liability, ZERO),
            'formula': '已审核年度应纳税所得额/累计实际利润额×有效税率−累计已预缴',
            'policy_ids': ['CIT-LAW', 'SME-2023-12']}


def payroll(req, data):
    fields(data, 'income_ytd exempt_income_ytd basic_deduction_ytd social_deductions_ytd additional_deductions_ytd other_deductions_ytd relief_ytd withheld_ytd')
    end = date.fromisoformat(req['period_end'])
    check(req['period_start'] == f'{end.year}-01-01' and end.day == calendar.monthrange(end.year, end.month)[1],
          '工资数据必须为当年截至本月末在本单位的累计数据')
    values = {k: money(v) for k, v in data.items()}
    check(values['basic_deduction_ytd'] <= 60000, '基本费用累计不能超过60000')
    check(values['exempt_income_ytd'] <= values['income_ytd'], '免税收入不能超过累计收入')
    deductions = sum((values[k] for k in ('exempt_income_ytd', 'basic_deduction_ytd',
                     'social_deductions_ytd', 'additional_deductions_ytd', 'other_deductions_ytd')), ZERO)
    result = tax(values['income_ytd'] - deductions)
    after_relief = max(result['tax'] - values['relief_ytd'], ZERO)
    result.update({'tax_after_relief': after_relief, 'withheld_ytd': values['withheld_ytd'],
                   'due': max(after_relief - values['withheld_ytd'], ZERO),
                   'excess_withheld_no_current_refund': max(values['withheld_ytd'] - after_relief, ZERO),
                   'formula': '累计收入−累计免税/费用/扣除→年度级距税额−累计减免−累计已扣；负数当期不退',
                   'policy_ids': ['IIT-LAW', 'IIT-WITHHOLD']})
    return result


def iit_annual(req, data):
    fields(data, 'wages labor author_fees royalties deductions relief withheld')
    annual_period(req)
    values = {k: money(v) for k, v in data.items()}
    income = values['wages'] + values['labor'] * D('.8') + values['author_fees'] * D('.56') + values['royalties'] * D('.8')
    net = income - D(60000) - values['deductions']
    result = tax(net)
    liability = max(result['tax'] - values['relief'], ZERO)
    result.update({'income_amount': income, 'net_before_floor': net,
                   'tax_after_relief': liability, 'withheld': values['withheld'],
                   'balance_payable_before_filing_exemption_review': max(liability - values['withheld'], ZERO),
                   'refund_candidate': max(values['withheld'] - liability, ZERO),
                   'filing_exemption_review_required': True,
                   'formula': '工资+劳务×80%+稿酬×56%+特许权×80%−60000−合法扣除→年度税额−减免−已缴',
                   'policy_ids': ['IIT-LAW', 'IIT-FILING-2023-32']})
    return result


def bonus_compare(req, data):
    fields(data, 'annual_net_before_bonus bonus eligible_once')
    annual_period(req)
    check(flag(data, 'eligible_once'), '需符合全年一次性奖金条件且本年单独计税机会尚可用')
    net = money(data['annual_net_before_bonus'], signed=True)
    bonus = money(data['bonus'])
    monthly = tax(bonus / D(12), monthly=True)
    bonus_tax = q(bonus * monthly['rate'] - monthly['quick_deduction'])
    separate = tax(net)['tax'] + bonus_tax
    merged = tax(net + bonus)['tax']
    return {'annual_net_before_bonus': net, 'bonus': bonus,
            'bonus_monthly_basis': bonus / D(12), 'bonus_rate': monthly['rate'],
            'bonus_quick_deduction': monthly['quick_deduction'], 'bonus_separate_tax': bonus_tax,
            'separate_total_annual_tax': separate, 'merged_total_annual_tax': merged,
            'lower_tax_option': 'equal' if merged == separate else ('merged' if merged < separate else 'separate'),
            'difference': abs(merged - separate),
            'formula': '比较综合所得税(max(净所得,0))+奖金单独税 与 综合所得税(max(净所得+奖金,0))',
            'policy_ids': ['IIT-LAW', 'IIT-BONUS', 'IIT-BONUS-ONCE']}


def surcharges(req, data):
    fields(data, 'cycle period_sales city_base education_base local_education_base city_rate six_taxes_eligible')
    threshold = period_threshold(req, data['cycle'])
    sales = money(data['period_sales'])
    city_rate = number(data['city_rate'])
    check(city_rate in (D('.07'), D('.05'), D('.01')), '城建税率必须已按所在地确认7%/5%/1%')
    half = D('.5') if flag(data, 'six_taxes_eligible') else D(1)
    exempt = sales <= threshold  # 财税2016年第12号“不超过”，与增值税不同。
    rows = []
    for label, field, rate in [('city_tax', 'city_base', city_rate),
                               ('education', 'education_base', D('.03')),
                               ('local_education', 'local_education_base', D('.02'))]:
        base = money(data[field])
        gross = q(base * rate)
        payable = ZERO if exempt and label != 'city_tax' else q(base * rate * half)
        relief = gross - payable
        rows.append({'item': label, 'base': base, 'rate': rate, 'gross_tax': gross,
                     'relief': relief, 'tax': gross - relief})
    return {'education_exempt': exempt, 'six_taxes_half': half == D('.5'),
            'breakdown': rows, 'tax_liability': sum((r['tax'] for r in rows), ZERO),
            'formula': '分别确认的基数×各费率，先判教育附加免征，再判六税两费减半',
            'policy_ids': ['SURCHARGE-LAW', 'EDU-RATES', 'EDU-2016-12', 'SME-2023-12']}


def stamp(req, data):
    fields(data, 'item taxable_amount six_taxes_eligible')
    rates = {'goods_contract': D('.0003'), 'capital_books': D('.00025')}
    check(data['item'] in rates, '仅动产买卖合同/资金账簿；其他税目另核验')
    base, rate = money(data['taxable_amount']), rates[data['item']]
    gross = q(base * rate)
    payable = q(base * rate * D('.5')) if flag(data, 'six_taxes_eligible') else gross
    reduction = gross - payable
    return {'taxable_amount': base, 'rate': rate, 'gross_tax': gross,
            'reduction': reduction, 'tax_liability': gross - reduction,
            'formula': '已核实计税金额×税率−六税两费减免；账簿仅输入应税增加额',
            'policy_ids': ['STAMP-LAW', 'STAMP-GOODS' if data['item'] == 'goods_contract' else 'STAMP-CAPITAL', 'SME-2023-12']}


MODES = {'small_vat': small_vat, 'general_vat': general_vat, 'cit': cit,
         'payroll': payroll, 'iit_annual': iit_annual, 'bonus_compare': bonus_compare,
         'surcharges': surcharges, 'stamp': stamp}


def calculate(req):
    fields(req, 'mode period_start period_end scope_confirmed data', ('id',))
    check(flag(req, 'scope_confirmed'), '需先按calculator.md确认主体/资格、数据口径与业务范围')
    start, end = date.fromisoformat(req['period_start']), date.fromisoformat(req['period_end'])
    check(date(2026, 1, 1) <= start <= end <= date(2027, 12, 31) and start.year == end.year,
          '仅支持2026—2027同一年度内所属期；旧期/跨年/优惠到期需更新政策与算法')
    check(req['mode'] in MODES, '不支持的计算模式')
    result = MODES[req['mode']](req, req['data'])
    return {'id': req.get('id'), 'mode': req['mode'], 'period_start': req['period_start'],
            'period_end': req['period_end'], 'status': 'draft_calculation_not_filed',
            'currency': 'CNY', 'policy_snapshot': SNAPSHOT,
            'policy_index': 'references/policies.md', 'current_policy_review_required': True,
            'rounding': 'Decimal ROUND_HALF_UP; cents; reconcile official form rounding',
            'input': req['data'], 'result': result}


def encode(obj):
    if isinstance(obj, D):
        return format(obj, 'f')
    raise TypeError(type(obj).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON文件，单个请求或请求数组；- 从stdin读取')
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.input == '-' else Path(args.input).read_text(encoding='utf-8')
        payload = json.loads(raw, parse_float=D)
        check(not isinstance(payload, list) or bool(payload), '请求数组不能为空')
        result = [calculate(r) for r in payload] if isinstance(payload, list) else calculate(payload)
        print(json.dumps({'success': True, 'calculations': result}, ensure_ascii=False, indent=2, default=encode))
        return 0
    except (ValueError, TypeError, KeyError, InvalidOperation, OSError) as exc:
        print(json.dumps({'success': False, 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
