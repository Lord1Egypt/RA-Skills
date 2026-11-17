#!/usr/bin/env python3
"""earnings_lint.py 的单元测试。

覆盖三类用例:
    1. 好样例（PASS，退出码 0）
    2. 坏样例（FAIL，退出码 2）
    3. 用法错误（退出码 3）

运行: python3 scripts/tests/test_earnings_lint.py
"""

import os
import sys
import tempfile
import unittest

# 将 scripts 目录加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from earnings_lint import lint


class TestGoodReport(unittest.TestCase):
    """好样例：完整报告，应全部通过。"""

    GOOD_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>测试公司 2025Q2 财报深度解读</title>
<style>body{font-family:sans-serif;}</style>
</head>
<body>
<div class="container">
  <div class="header"><h1>测试公司 2025Q2 财报深度解读</h1></div>

  <div class="conclusion-box">
    <h2 id="core-conclusion">核心结论</h2>
    <ol><li>收入增长稳健，同比增 15%。</li><li>毛利率持平，成本控制良好。</li><li>经营现金流健康，利润质量高。</li></ol>
  </div>

  <section><h2 id="overview">业绩概览</h2>
    <table><tr><th>指标</th><th>本期</th><th>同比</th></tr>
    <tr><td>收入</td><td>100亿</td><td>+15%</td></tr></table>
    <p>本期收入 100 亿元，同比增长 15%，符合市场预期。</p>
  </section>

  <section><h2 id="revenue">收入分析</h2>
    <p>总收入同比增长 15%，主要驱动来自核心业务 A 的销量增长，销量同比增 12%，单价同比增 3%。</p>
  </section>

  <section><h2 id="gross-margin">毛利率分析</h2>
    <p>毛利率 45.2%，同比持平。原材料成本下降被产品结构变化抵消。</p>
  </section>

  <section><h2 id="expenses">费用分析</h2>
    <p>期间费用率 18.5%，同比下降 0.5 个百分点。销售费用率持平，研发费用率微降。</p>
  </section>

  <section><h2 id="profitability">盈利能力</h2>
    <p>净利率 22.0%，同比提升 1.2 个百分点。扣非净利润增速高于归母净利润增速，盈利质量良好。</p>
  </section>

  <section><h2 id="cashflow">现金流</h2>
    <p>经营现金流净额 25 亿元，盈余现金保障倍数 1.14，利润有现金流支撑。自由现金流 15 亿元。</p>
  </section>

  <section><h2 id="working-capital">营运资本</h2>
    <p>应收账款增速 12%，低于收入增速 15%，回款良好。存货增速 8%，无积压。合同负债环比增 5%。</p>
  </section>

  <section><h2 id="anomalies">经营异常</h2>
    <p>经逐条检查 A01-A15 规则，本期均未触发高严重级异常。</p>
    <p>以下规则未触发：A01、A02、A03、A04、A05、A06、A07、A08、A09、A10、A11、A12、A13、A14、A15。</p>
  </section>

  <section><h2 id="anomaly-causes">异常原因</h2>
    <p>本期无触发的异常，无需原因分析。</p>
  </section>

  <section><h2 id="risks">风险</h2>
    <ul><li>行业竞争加剧可能导致毛利率承压。</li><li>海外业务占比 30%，汇率波动风险。</li><li>新业务尚在投入期，短期拖累利润。</li></ul>
  </section>

  <section><h2 id="investment-implications">投资含义</h2>
    <p>本期财报反映收入增长稳健、利润质量高，对投资逻辑有正面支撑。但需关注行业竞争对毛利率的潜在影响。</p>
    <p>注：本节不构成买入/卖出建议，仅分析财报对投资逻辑的影响。</p>
  </section>

  <section><h2 id="data-sources">数据来源</h2>
    <ul><li>用户提供：2025Q2 财报 PDF</li><li>web_search 检索：市场预期数据，2025-08-15</li></ul>
  </section>

  <div class="footer"><p>本报告由财报深度解读助手生成。</p></div>
</div>
</body>
</html>"""

    def test_good_report_passes(self):
        fails, warns = lint(self.GOOD_HTML)
        self.assertEqual(fails, [], f"好样例不应有 FAIL，但得到: {fails}")
        # W02 可能触发因为异常节虽提到了 A01-A15 但格式是文本
        # W03 不应触发因为有"不构成"和"投资建议"
        w03_triggered = any(w["code"] == "W03" for w in warns)
        self.assertFalse(w03_triggered, "好样例不应触发 W03")


class TestBadReport(unittest.TestCase):
    """坏样例：各种缺陷，应触发 FAIL。"""

    def test_missing_section(self):
        """缺少必需章节 → F03 FAIL"""
        html = """<!DOCTYPE html><html><head><title>test</title></head><body>
        <h2 id="core-conclusion">核心结论</h2><p>结论内容</p>
        <h2 id="overview">业绩概览</h2><p>概览内容</p>
        </body></html>"""
        fails, warns = lint(html)
        fail_codes = [f["code"] for f in fails]
        self.assertIn("F03", fail_codes, "缺少章节应触发 F03")

    def test_placeholder_not_replaced(self):
        """未替换占位符 → F05 FAIL"""
        html = """<!DOCTYPE html><html><head><title>test</title></head><body>
        <h2 id="core-conclusion">核心结论</h2><p>{{结论1}}</p>
        <h2 id="overview">业绩概览</h2><p>概览内容足够长</p>
        <h2 id="revenue">收入分析</h2><p>收入内容足够长</p>
        <h2 id="gross-margin">毛利率分析</h2><p>毛利率内容足够长</p>
        <h2 id="expenses">费用分析</h2><p>费用内容足够长</p>
        <h2 id="profitability">盈利能力</h2><p>盈利内容足够长</p>
        <h2 id="cashflow">现金流</h2><p>现金流内容足够长</p>
        <h2 id="working-capital">营运资本</h2><p>营运资本内容足够长</p>
        <h2 id="anomalies">经营异常</h2><p>异常内容足够长</p>
        <h2 id="anomaly-causes">异常原因</h2><p>原因内容足够长</p>
        <h2 id="risks">风险</h2><p>风险内容足够长</p>
        <h2 id="investment-implications">投资含义</h2><p>投资含义内容足够长</p>
        <h2 id="data-sources">数据来源</h2><p>来源内容足够长</p>
        </body></html>"""
        fails, warns = lint(html)
        fail_codes = [f["code"] for f in fails]
        self.assertIn("F05", fail_codes, "未替换占位符应触发 F05")

    def test_external_resource(self):
        """外部资源引用 → F06 FAIL"""
        html = """<!DOCTYPE html><html><head>
        <title>test</title>
        <link rel="stylesheet" href="https://cdn.example.com/style.css">
        </head><body>
        <h2 id="core-conclusion">核心结论</h2><p>结论内容足够长</p>
        <h2 id="overview">业绩概览</h2><p>概览内容足够长</p>
        <h2 id="revenue">收入分析</h2><p>收入内容足够长</p>
        <h2 id="gross-margin">毛利率分析</h2><p>毛利率内容足够长</p>
        <h2 id="expenses">费用分析</h2><p>费用内容足够长</p>
        <h2 id="profitability">盈利能力</h2><p>盈利内容足够长</p>
        <h2 id="cashflow">现金流</h2><p>现金流内容足够长</p>
        <h2 id="working-capital">营运资本</h2><p>营运资本内容足够长</p>
        <h2 id="anomalies">经营异常</h2><p>异常内容足够长</p>
        <h2 id="anomaly-causes">异常原因</h2><p>原因内容足够长</p>
        <h2 id="risks">风险</h2><p>风险内容足够长</p>
        <h2 id="investment-implications">投资含义</h2><p>投资含义内容足够长</p>
        <h2 id="data-sources">数据来源</h2><p>来源内容足够长</p>
        </body></html>"""
        fails, warns = lint(html)
        fail_codes = [f["code"] for f in fails]
        self.assertIn("F06", fail_codes, "外部资源引用应触发 F06")

    def test_empty_section(self):
        """章节内容过短 → F04 FAIL"""
        html = """<!DOCTYPE html><html><head><title>test</title></head><body>
        <section><h2 id="core-conclusion">核心结论</h2></section>
        <section><h2 id="overview">业绩概览</h2><p>足够长的概览内容</p></section>
        <section><h2 id="revenue">收入分析</h2><p>足够长的收入内容</p></section>
        <section><h2 id="gross-margin">毛利率分析</h2><p>足够长的毛利率内容</p></section>
        <section><h2 id="expenses">费用分析</h2><p>足够长的费用内容</p></section>
        <section><h2 id="profitability">盈利能力</h2><p>足够长的盈利内容</p></section>
        <section><h2 id="cashflow">现金流</h2><p>足够长的现金流内容</p></section>
        <section><h2 id="working-capital">营运资本</h2><p>足够长的营运资本内容</p></section>
        <section><h2 id="anomalies">经营异常</h2><p>足够长的异常内容</p></section>
        <section><h2 id="anomaly-causes">异常原因</h2><p>足够长的原因内容</p></section>
        <section><h2 id="risks">风险</h2><p>足够长的风险内容</p></section>
        <section><h2 id="investment-implications">投资含义</h2><p>足够长的投资含义内容</p></section>
        <section><h2 id="data-sources">数据来源</h2><p>足够长的来源内容</p></section>
        </body></html>"""
        fails, warns = lint(html)
        fail_codes = [f["code"] for f in fails]
        self.assertIn("F04", fail_codes, "空章节应触发 F04")

    def test_not_html(self):
        """不是 HTML → F02 FAIL"""
        html = "这是一段纯文本，不是 HTML 报告。"
        fails, warns = lint(html)
        fail_codes = [f["code"] for f in fails]
        self.assertIn("F02", fail_codes, "非 HTML 应触发 F02")


class TestUsageError(unittest.TestCase):
    """用法错误：文件不存在 → 退出码 3。"""

    def test_file_not_found(self):
        """文件不存在 → 退出码 3"""
        import subprocess
        script_path = os.path.join(os.path.dirname(__file__), "..", "earnings_lint.py")
        result = subprocess.run(
            [sys.executable, script_path, "/nonexistent/path/report.html"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 3, f"文件不存在应返回退出码 3，实际: {result.returncode}")

    def test_no_argument(self):
        """无参数 → 退出码 3"""
        import subprocess
        script_path = os.path.join(os.path.dirname(__file__), "..", "earnings_lint.py")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 3, f"无参数应返回退出码 3，实际: {result.returncode}")


class TestWarnCases(unittest.TestCase):
    """WARN 情况：可交付但有建议项。"""

    def test_too_many_conclusions(self):
        """核心结论超过 5 条 → W01 WARN"""
        html = """<!DOCTYPE html><html><head><title>test</title></head><body>
        <section><h2 id="core-conclusion">核心结论</h2>
        <ol><li>结论1</li><li>结论2</li><li>结论3</li><li>结论4</li><li>结论5</li><li>结论6</li></ol></section>
        <section><h2 id="overview">业绩概览</h2><p>足够长的概览内容</p></section>
        <section><h2 id="revenue">收入分析</h2><p>足够长的收入内容</p></section>
        <section><h2 id="gross-margin">毛利率分析</h2><p>足够长的毛利率内容</p></section>
        <section><h2 id="expenses">费用分析</h2><p>足够长的费用内容</p></section>
        <section><h2 id="profitability">盈利能力</h2><p>足够长的盈利内容</p></section>
        <section><h2 id="cashflow">现金流</h2><p>足够长的现金流内容</p></section>
        <section><h2 id="working-capital">营运资本</h2><p>足够长的营运资本内容</p></section>
        <section><h2 id="anomalies">经营异常</h2><p>经检查 A01-A15 均未触发</p></section>
        <section><h2 id="anomaly-causes">异常原因</h2><p>无异常需要分析</p></section>
        <section><h2 id="risks">风险</h2><p>足够长的风险内容</p></section>
        <section><h2 id="investment-implications">投资含义</h2><p>不构成投资建议</p></section>
        <section><h2 id="data-sources">数据来源</h2><p>用户提供财报</p></section>
        </body></html>"""
        fails, warns = lint(html)
        self.assertEqual(fails, [], f"不应有 FAIL: {fails}")
        warn_codes = [w["code"] for w in warns]
        self.assertIn("W01", warn_codes, "核心结论超过5条应触发 W01")


if __name__ == "__main__":
    unittest.main(verbosity=2)
