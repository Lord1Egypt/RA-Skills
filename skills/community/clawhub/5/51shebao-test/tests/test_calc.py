"""hr-calculator 计算逻辑测试（对照 hr-tool 原实现）。
运行：python3 skills/hr-calculator/tests/test_calc.py -v
"""
import json
import os
import subprocess
import sys
import unittest
from decimal import Decimal

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

from calc.util import r2  # noqa: E402

D = Decimal
HR_CALC = os.path.join(SCRIPTS, "hr_calc.py")


class TestR2(unittest.TestCase):
    def test_half_up(self):
        self.assertEqual(r2(D("151.485")), D("151.49"))
        self.assertEqual(r2(D("17398.015")), D("17398.02"))
        self.assertEqual(r2(D("2.674")), D("2.67"))

    def test_two_places(self):
        self.assertEqual(str(r2(D("8000"))), "8000.00")


from calc.salary import salary_calculation  # noqa: E402


class TestSalary(unittest.TestCase):
    def test_spec_example(self):
        """设计文档示例：税前20000 期数1 社保1050.50 公积金1400 六项6500 养老金1000"""
        r = salary_calculation(D("20000"), periods=1, social_ee=D("1050.50"),
                               fund_ee=D("1400"), child_edu=D("2000"),
                               house=D("1500"), elder=D("3000"),
                               personal_pension=D("1000"))
        self.assertEqual(r["taxable_income"], "5049.50")
        self.assertEqual(r["tax_rate"], "3")
        self.assertEqual(r["quick_deduction"], "0.00")
        self.assertEqual(r["personal_income_tax"], "151.49")
        # 到手用未舍入税额：20000-151.485-1400-1050.50=17398.015 → 17398.02
        self.assertEqual(r["after_tax_income"], "17398.02")
        self.assertEqual(r["five_deduction"]["monthly_total"], "6500.00")
        self.assertEqual(r["personal_pension_total"], "1000.00")

    def test_first_month_no_deduction(self):
        """税前20000 无任何扣除：(20000-5000)*3%=450"""
        r = salary_calculation(D("20000"))
        self.assertEqual(r["taxable_income"], "15000.00")
        self.assertEqual(r["personal_income_tax"], "450.00")
        self.assertEqual(r["after_tax_income"], "19550.00")

    def test_multi_period_cumulative(self):
        """12 期累计：累计应纳税所得 180000 落 20% 档，减去前 11 月已缴 16080"""
        r = salary_calculation(D("20000"), periods=12)
        self.assertEqual(r["taxable_income"], "180000.00")
        # 累计税 180000*0.2-16920=19080；已缴 165000*0.2-16920=16080；本期 3000
        self.assertEqual(r["personal_income_tax"], "3000.00")
        self.assertEqual(r["tax_rate"], "20")
        self.assertEqual(r["after_tax_income"], "17000.00")

    def test_taxable_income_floor_zero(self):
        """扣除超过收入时，应纳税所得额下限 0"""
        r = salary_calculation(D("4000"), house=D("3000"))
        self.assertEqual(r["taxable_income"], "0.00")
        self.assertEqual(r["personal_income_tax"], "0.00")

    def test_pension_not_in_paid_tax(self):
        """怪癖锁定：已缴(n-1月)税额计算不扣个人养老金（与原实现一致）。
        2 期，养老金 1000/月：
        本期累计税 = (20000*2-5000*2-1000*2)*3% = 28000*3% = 840
        已缴 = (20000-5000)*3% = 450（注意：不含养老金扣除）
        本期 = 840-450 = 390"""
        r = salary_calculation(D("20000"), periods=2, personal_pension=D("1000"))
        self.assertEqual(r["personal_income_tax"], "390.00")


from calc.salary import reverse_salary_calculation  # noqa: E402


class TestReverseSalary(unittest.TestCase):
    def test_round_trip_15000(self):
        """到手 15000 反推：应落 3% 档，before≈(15000-150)/0.97=15309.28"""
        r = reverse_salary_calculation(D("15000"))
        before = D(r["before_tax_income"])
        self.assertLessEqual(abs(before - D("15309.28")), D("1.10"))
        # 回代正算，到手与目标误差 ≤1 元（原服务收敛容差）
        check = salary_calculation(before)
        self.assertLessEqual(abs(D(check["after_tax_income"]) - D("15000")), D("1.00"))
        self.assertEqual(r["after_tax_income"], "15000.00")

    def test_round_trip_with_deductions(self):
        """带扣除项的反推回代（kwargs 须与目标到手额的口径一致，含个人养老金）"""
        kwargs = dict(social_ee=D("1050.50"), fund_ee=D("1400"),
                      child_edu=D("2000"), house=D("1500"), elder=D("3000"),
                      personal_pension=D("1000"))
        r = reverse_salary_calculation(D("17398.02"), **kwargs)
        before = D(r["before_tax_income"])
        self.assertLessEqual(abs(before - D("20000")), D("1.10"))
        check = salary_calculation(before, **kwargs)
        self.assertLessEqual(abs(D(check["after_tax_income"]) - D("17398.02")), D("1.00"))


from calc.remuneration import labor_calculate, reverse_labor_calculate  # noqa: E402


class TestLabor(unittest.TestCase):
    def test_textbook_10000(self):
        """教科书值（锁定正确逻辑，原 Java 此处有 context 误传 bug）"""
        r = labor_calculate(D("10000"))
        self.assertEqual(r["taxable_income"], "8000.00")
        self.assertEqual(r["income_tax"], "1600.00")
        self.assertEqual(r["after_tax_income"], "8400.00")
        self.assertEqual(r["withholding_rate"], "20%")
        self.assertEqual(r["quick_calc_deduction"], "0")

    def test_exempt_800(self):
        r = labor_calculate(D("800"))
        self.assertEqual(r["income_tax"], "0")
        self.assertEqual(r["after_tax_income"], "800.00")
        self.assertEqual(r["taxable_income_formula"], "免税")
        self.assertEqual(r["withholding_rate"], "")

    def test_mid_3000(self):
        r = labor_calculate(D("3000"))
        self.assertEqual(r["taxable_income"], "2200.00")
        self.assertEqual(r["income_tax"], "440.00")
        self.assertEqual(r["after_tax_income"], "2560.00")

    def test_level2_30000(self):
        r = labor_calculate(D("30000"))
        self.assertEqual(r["taxable_income"], "24000.00")
        self.assertEqual(r["income_tax"], "5200.00")
        self.assertEqual(r["quick_calc_deduction"], "2000")
        self.assertEqual(r["withholding_rate"], "30%")
        self.assertEqual(r["after_tax_income"], "24800.00")

    def test_level3_100000(self):
        r = labor_calculate(D("100000"))
        self.assertEqual(r["taxable_income"], "80000.00")
        self.assertEqual(r["income_tax"], "25000.00")
        self.assertEqual(r["quick_calc_deduction"], "7000")
        self.assertEqual(r["withholding_rate"], "40%")
        self.assertEqual(r["after_tax_income"], "75000.00")

    def test_nonpositive_raises(self):
        with self.assertRaises(ValueError):
            labor_calculate(D("0"))
        with self.assertRaises(ValueError):
            labor_calculate(D("-100"))


class TestReverseLabor(unittest.TestCase):
    def test_reverse_8400(self):
        r = reverse_labor_calculate(D("8400"))
        self.assertEqual(r["before_tax_income"], "10000.00")
        self.assertEqual(r["income_tax"], "1600.00")
        self.assertEqual(r["after_tax_income"], "8400.00")

    def test_reverse_3300_segment1(self):
        """[800,3360) 段：(3300-160)/0.8=3925 → 税 625 → 到手 3300"""
        r = reverse_labor_calculate(D("3300"))
        self.assertEqual(r["before_tax_income"], "3925.00")
        self.assertEqual(r["after_tax_income"], "3300.00")

    def test_reverse_700_below_800(self):
        r = reverse_labor_calculate(D("700"))
        self.assertEqual(r["before_tax_income"], "700.00")
        self.assertEqual(r["income_tax"], "0")

    def test_reverse_49000_segment3(self):
        """[21000,49500) 段：(49000-2000)/0.76=61842.11 → 所得 49473.69
        → 税 49473.69*0.3-2000=12842.11 → 到手 49000.00"""
        r = reverse_labor_calculate(D("49000"))
        self.assertEqual(r["before_tax_income"], "61842.11")
        self.assertEqual(r["income_tax"], "12842.11")
        self.assertEqual(r["after_tax_income"], "49000.00")

    def test_reverse_49500_boundary(self):
        """>=49500 段：(49500-7000)/0.68=62500 → 所得 50000（30% 档上边界）
        → 税 13000 → 到手 49500"""
        r = reverse_labor_calculate(D("49500"))
        self.assertEqual(r["before_tax_income"], "62500.00")
        self.assertEqual(r["income_tax"], "13000.00")
        self.assertEqual(r["withholding_rate"], "30%")
        self.assertEqual(r["after_tax_income"], "49500.00")


from calc.remuneration import (author_calculate, privilege_calculate,  # noqa: E402
                               reverse_privilege_calculate)


class TestAuthor(unittest.TestCase):
    def test_5000_above_4000(self):
        """5000*0.8*0.7=2800，税 560"""
        r = author_calculate(D("5000"))
        self.assertEqual(r["taxable_income"], "2800.00")
        self.assertEqual(r["income_tax"], "560.00")
        self.assertEqual(r["after_tax_income"], "4440.00")
        self.assertEqual(r["withholding_rate"], "20%")

    def test_2000_below_4000(self):
        """(2000-800)*0.7=840，税 168"""
        r = author_calculate(D("2000"))
        self.assertEqual(r["taxable_income"], "840.00")
        self.assertEqual(r["income_tax"], "168.00")
        self.assertEqual(r["after_tax_income"], "1832.00")

    def test_4000_boundary(self):
        """4000 走 ≤4000 分支：(4000-800)*0.7=2240，税 448"""
        r = author_calculate(D("4000"))
        self.assertEqual(r["taxable_income"], "2240.00")
        self.assertEqual(r["income_tax"], "448.00")
        self.assertEqual(r["after_tax_income"], "3552.00")


class TestPrivilege(unittest.TestCase):
    def test_5000_above_4000(self):
        """5000*0.8=4000，税 800"""
        r = privilege_calculate(D("5000"))
        self.assertEqual(r["taxable_income"], "4000.00")
        self.assertEqual(r["income_tax"], "800.00")
        self.assertEqual(r["after_tax_income"], "4200.00")

    def test_3000_below_4000(self):
        """3000-800=2200，税 440"""
        r = privilege_calculate(D("3000"))
        self.assertEqual(r["taxable_income"], "2200.00")
        self.assertEqual(r["income_tax"], "440.00")
        self.assertEqual(r["after_tax_income"], "2560.00")


class TestReversePrivilege(unittest.TestCase):
    def test_reverse_4200_two_branch(self):
        """one=(4200-160)/0.8=5050>4000 → two=4200/0.84=5000 → 税 800 → 到手 4200"""
        r = reverse_privilege_calculate(D("4200"))
        self.assertEqual(r["before_tax_income"], "5000.00")
        self.assertEqual(r["income_tax"], "800.00")
        self.assertEqual(r["after_tax_income"], "4200.00")

    def test_reverse_2560_one_branch(self):
        """one=(2560-160)/0.8=3000≤4000 → 税 440 → 到手 2560"""
        r = reverse_privilege_calculate(D("2560"))
        self.assertEqual(r["before_tax_income"], "3000.00")
        self.assertEqual(r["income_tax"], "440.00")
        self.assertEqual(r["after_tax_income"], "2560.00")


from calc.remuneration import compensation_calculate  # noqa: E402


class TestCompensation(unittest.TestCase):
    def test_below_exempt(self):
        """300000 ≤ 免税额 12000*12*3=432000 → 不缴税"""
        r = compensation_calculate(D("300000"), D("12000"))
        self.assertEqual(r["after_tax_income"], "300000.00")
        self.assertEqual(r["income_tax"], "0.00")
        self.assertEqual(r["withholding_rate"], "0%")
        self.assertEqual(r["last_year_city_avg_salary"], "12000.00")

    def test_bracket_20pct(self):
        """600000-432000=168000 → 20% 档：168000*0.2-16920=16680"""
        r = compensation_calculate(D("600000"), D("12000"))
        self.assertEqual(r["taxable_income"], "168000.00")
        self.assertEqual(r["income_tax"], "16680.00")
        self.assertEqual(r["withholding_rate"], "20%")
        self.assertEqual(r["quick_calc_deduction"], "16920.00")
        self.assertEqual(r["after_tax_income"], "583320.00")

    def test_bracket_30pct(self):
        """1000000-360000=640000 → 30% 档：640000*0.3-52920=139080"""
        r = compensation_calculate(D("1000000"), D("10000"))
        self.assertEqual(r["income_tax"], "139080.00")
        self.assertEqual(r["withholding_rate"], "30%")
        self.assertEqual(r["after_tax_income"], "860920.00")


def run_cli(*args):
    return subprocess.run([sys.executable, HR_CALC, *args],
                          capture_output=True, text=True)


class TestCli(unittest.TestCase):
    def test_salary_json(self):
        p = run_cli("salary", "--before-tax", "20000", "--periods", "1",
                    "--social-ee", "1050.50", "--fund-ee", "1400",
                    "--deduction-child-edu", "2000", "--deduction-house", "1500",
                    "--deduction-elder", "3000", "--personal-pension", "1000")
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertEqual(data["after_tax_income"], "17398.02")
        self.assertEqual(data["personal_income_tax"], "151.49")

    def test_reverse_salary(self):
        p = run_cli("reverse-salary", "--after-tax", "15000")
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertEqual(data["after_tax_income"], "15000.00")

    def test_labor(self):
        p = run_cli("labor", "--before-tax", "10000")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["income_tax"], "1600.00")

    def test_compensation(self):
        p = run_cli("compensation", "--before-tax", "600000", "--avg-salary", "12000")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["income_tax"], "16680.00")

    def test_bad_amount_errors(self):
        p = run_cli("salary", "--before-tax", "abc")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("参数错误", p.stderr)

    def test_negative_amount_errors(self):
        p = run_cli("labor", "--before-tax", "-100")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("参数错误", p.stderr)

    def test_bad_periods_errors(self):
        p = run_cli("salary", "--before-tax", "10000", "--periods", "1.5")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("参数错误", p.stderr)

    def test_missing_required_errors(self):
        p = run_cli("salary")
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
