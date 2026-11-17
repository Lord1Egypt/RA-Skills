import copy
import json
import subprocess
import sys
import unittest
from decimal import Decimal as D
from pathlib import Path
from calculate import calculate, tax


def request(mode, data, start='2026-01-01', end='2026-12-31'):
    return {'mode': mode, 'period_start': start, 'period_end': end,
            'scope_confirmed': True, 'data': data}


def small(sales, end='2026-03-31', cycle='quarter'):
    return request('small_vat', {'cycle': cycle, 'sales': sales, 'prepaid': '0'}, end=end)


def sale(amount, rate='.01', waived=False):
    return {'net_sales': amount, 'rate': rate, 'waive_exemption': waived}


class TaxTests(unittest.TestCase):
    def test_vat_threshold_2026_strict(self):
        for amount, expected in [('299999.99', '0'), ('300000', '3000'), ('300000.01', '3000')]:
            with self.subTest(amount=amount):
                self.assertEqual(calculate(small([sale(amount)]))['result']['tax_liability'], D(expected))

    def test_month_threshold_and_no_deduction_of_cost(self):
        r = calculate(small([sale('100000')], '2026-01-31', 'month'))['result']
        self.assertEqual(r['due'], D('1000'))

    def test_special_invoice_below_threshold(self):
        r = calculate(small([sale('200000'), sale('50000', waived=True)]))['result']
        self.assertEqual(r['due'], D('500'))
        self.assertEqual(r['exempt_sales'], D('200000'))

    def test_special_invoice_counts_toward_threshold(self):
        r = calculate(small([sale('250000'), sale('50000', waived=True)]))['result']
        self.assertEqual(r['due'], D('3000'))

    def test_mixed_rates(self):
        r = calculate(small([sale('100000'), sale('200000', '.03')]))['result']
        self.assertEqual(r['due'], D('7000'))

    def test_general_vat_and_prepayment(self):
        data = dict(sales=[dict(net_sales='100000', rate='.13')], deductible_input='10000',
                    input_transfer_out='500', opening_credit='1000', prepaid='500')
        r = calculate(request('general_vat', data))['result']
        self.assertEqual(r['tax_liability'], D('2500'))
        self.assertEqual(r['due'], D('2000'))
        data.update(deductible_input='20000', prepaid='2000')
        r = calculate(request('general_vat', data))['result']
        self.assertEqual(r['carryforward_input_credit'], D('7500'))
        self.assertEqual(r['prepayment_balance_to_review'], D('2000'))

    def test_cit_small_and_cliff(self):
        data = dict(assessment='annual', tax_base='3000000', employees_average='300',
                    assets_average='50000000', industry_allowed=True, prepaid='100000')
        r = calculate(request('cit', data))['result']
        self.assertEqual(r['due'], D('50000'))
        data['tax_base'] = '3000000.01'
        self.assertEqual(calculate(request('cit', data))['result']['tax_liability'], D('750000.00'))

    def test_cit_employee_asset_industry_conditions(self):
        data = dict(assessment='annual', tax_base='100000', employees_average='10',
                    assets_average='1000000', industry_allowed=True, prepaid='0')
        for k, v in [('employees_average', '300.01'), ('assets_average', '50000000.01'), ('industry_allowed', False)]:
            bad = dict(data, **{k: v})
            self.assertEqual(calculate(request('cit', bad))['result']['tax_liability'], D('25000'))

    def test_cit_cumulative_overpayment(self):
        data = dict(assessment='prepayment', tax_base='-1000', employees_average='3',
                    assets_average='1000000', industry_allowed=True, prepaid='2000')
        r = calculate(request('cit', data, end='2026-09-30'))['result']
        self.assertEqual(r['due'], 0)
        self.assertEqual(r['overpayment_to_review'], D('2000'))
        with self.assertRaises(ValueError):
            calculate(request('cit', data, '2026-07-01', '2026-09-30'))

    def test_payroll_cumulative_and_no_negative_refund(self):
        data = dict(income_ytd='120000', exempt_income_ytd='0', basic_deduction_ytd='30000',
                    social_deductions_ytd='9000', additional_deductions_ytd='12000',
                    other_deductions_ytd='0', relief_ytd='0', withheld_ytd='3000')
        r = calculate(request('payroll', data, end='2026-06-30'))['result']
        self.assertEqual(r['base'], D('69000'))
        self.assertEqual(r['due'], D('1380'))
        data['withheld_ytd'] = '5000'
        r = calculate(request('payroll', data, end='2026-06-30'))['result']
        self.assertEqual(r['due'], 0)
        self.assertEqual(r['excess_withheld_no_current_refund'], D('620'))

    def test_iit_income_conversion_and_refund(self):
        data = dict(wages='240000', labor='50000', author_fees='10000', royalties='10000',
                    deductions='36000', relief='0', withheld='25000')
        r = calculate(request('iit_annual', data))['result']
        self.assertEqual(r['income_amount'], D('293600'))
        self.assertEqual(r['tax_after_relief'], D('22600'))
        self.assertEqual(r['refund_candidate'], D('2400'))
        self.assertTrue(r['filing_exemption_review_required'])

    def test_bonus_unused_deductions(self):
        r = calculate(request('bonus_compare', dict(annual_net_before_bonus='-10000', bonus='36000', eligible_once=True)))['result']
        self.assertEqual(r['separate_total_annual_tax'], D('1080'))
        self.assertEqual(r['merged_total_annual_tax'], D('780'))
        self.assertEqual(r['lower_tax_option'], 'merged')

    def test_bonus_threshold_cliff_and_quick_deduction_once(self):
        for bonus, expected in [('36000', '1080'), ('36000.01', '3390.00'), ('42000', '3990')]:
            r = calculate(request('bonus_compare', dict(annual_net_before_bonus='100000', bonus=bonus, eligible_once=True)))['result']
            self.assertEqual(r['bonus_separate_tax'], D(expected))

    def test_bonus_single_opportunity_required(self):
        with self.assertRaises(ValueError):
            calculate(request('bonus_compare', dict(annual_net_before_bonus='1000', bonus='1000', eligible_once=False)))

    def test_surcharge_education_threshold_differs_from_vat(self):
        data = dict(cycle='quarter', period_sales='300000', city_base='3000',
                    education_base='3000', local_education_base='3000', city_rate='.07', six_taxes_eligible=True)
        r = calculate(request('surcharges', data, end='2026-03-31'))['result']
        self.assertTrue(r['education_exempt'])
        self.assertEqual(r['tax_liability'], D('105'))
        data['period_sales'] = '300000.01'
        r = calculate(request('surcharges', data, end='2026-03-31'))['result']
        self.assertEqual(r['tax_liability'], D('180'))

    def test_surcharge_education_exemption_without_six_taxes(self):
        data = dict(cycle='month', period_sales='100000', city_base='1000', education_base='1000',
                    local_education_base='1000', city_rate='.05', six_taxes_eligible=False)
        self.assertEqual(calculate(request('surcharges', data, end='2026-01-31'))['result']['tax_liability'], D('50'))

    def test_stamp_two_items(self):
        for item, expected in [('goods_contract', '150'), ('capital_books', '125')]:
            r = calculate(request('stamp', dict(item=item, taxable_amount='1000000', six_taxes_eligible=True)))['result']
            self.assertEqual(r['tax_liability'], D(expected))

    def test_progressive_tax_against_independent_bracket_integration(self):
        # 独立分段累加，不复用速算扣除公式；覆盖每个边界及两侧。
        limits = [D(0), D(36000), D(144000), D(300000), D(420000), D(660000), D(960000), D(2000000)]
        rates = list(map(D, ['.03', '.10', '.20', '.25', '.30', '.35', '.45']))
        for edge in limits[1:-1]:
            for base in (edge - D('.01'), edge, edge + D('.01')):
                expected = sum((max(min(base, hi) - lo, D(0)) * r for lo, hi, r in zip(limits, limits[1:], rates)), D(0))
                self.assertEqual(tax(base)['tax'], expected.quantize(D('.01'), rounding='ROUND_HALF_UP'))

    def test_bad_or_out_of_scope_inputs(self):
        valid = small([sale('100000')])
        for mutation in [dict(scope_confirmed=False), dict(period_start='2025-01-01'),
                         dict(period_end='2028-03-31'), dict(unexpected=True)]:
            with self.assertRaises(ValueError):
                calculate(dict(valid, **mutation))
        for amount in ['NaN', 'Infinity', '-1', '0.001', True, 'abc']:
            with self.assertRaises(ValueError):
                calculate(small([sale(amount)]))
        with self.assertRaises(ValueError):
            calculate(small([sale('100000', '.05')]))
        with self.assertRaises(ValueError):
            calculate(small([sale('100000')], end='2026-02-15'))
        missing = copy.deepcopy(valid)
        del missing['data']['prepaid']
        with self.assertRaises(ValueError):
            calculate(missing)

    def test_cli_batch_examples_and_failure(self):
        root = Path(__file__).resolve().parents[1]
        run = subprocess.run([sys.executable, str(root / 'scripts/calculate.py'), str(root / 'assets/examples.json')], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        results = json.loads(run.stdout)['calculations']
        self.assertEqual(len(results), 8)
        self.assertTrue(all(r['status'] == 'draft_calculation_not_filed' for r in results))
        bad = subprocess.run([sys.executable, str(root / 'scripts/calculate.py'), '-'], input='{}', capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertFalse(json.loads(bad.stdout)['success'])


if __name__ == '__main__':
    unittest.main()
