#!/usr/bin/env python3
"""V2.0 测试套件 — 覆盖全部 4 个脚本"""
import sys, json, tempfile, shutil, os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / 'scripts'))

# === validate.py 测试 ===
import validate


def test_bluf_pass():
    ok, detail = validate.check_bluf('建议立即启动采购平台建设，预计年省1200万。')
    assert ok, f'BLUF 应通过: {detail}'


def test_bluf_fail():
    ok, detail = validate.check_bluf('背景：随着行业数字化转型加速，我们注意到...')
    assert not ok, f'BLUF 应失败: {detail}'


def test_so_what_pass():
    text = '## 业务影响\n\n这将导致收入下降15%。'
    ok, detail = validate.check_so_what(text)
    assert ok, f'So What 应通过: {detail}'


def test_so_what_fail():
    ok, detail = validate.check_so_what('## 关键发现\n\n发现了一些问题。')
    assert not ok, f'So What 应失败: {detail}'


def test_data_support_pass():
    text = '收入增长15%，节省成本约200万元，用户增长3倍。'
    ok, detail = validate.check_data_support(text)
    assert ok, f'数据支撑应通过: {detail}'


def test_data_support_fail():
    ok, detail = validate.check_data_support('系统有了很大提升。')
    assert not ok, f'数据支撑应失败: {detail}'


def test_action_clarity_pass():
    text = '## 建议行动\n1. 启动采购平台 — 张总负责 — Q3完成'
    ok, detail = validate.check_action_clarity(text)
    assert ok, f'行动明确性应通过: {detail}'


def test_action_clarity_fail():
    ok, detail = validate.check_action_clarity('## 建议行动\n1. 建议优化流程')
    assert not ok, f'行动明确性应失败: {detail}'


def test_word_limit_pass():
    ok, detail = validate.check_word_limit('核心结论：建议启动项目。' * 5)
    assert ok, f'篇幅应通过: {detail}'


def test_word_limit_fail():
    long_text = '这是一个非常长的报告内容。' * 200
    ok, detail = validate.check_word_limit(long_text)
    assert not ok, f'篇幅应失败: {detail}'


def test_confidence_pass():
    ok, detail = validate.check_confidence('发现1 [置信度：HIGH]')
    assert ok, f'置信度应通过: {detail}'


def test_confidence_fail():
    ok, detail = validate.check_confidence('发现了一个重要问题。')
    assert not ok, f'置信度应失败: {detail}'


def test_passive_voice_pass():
    ok, detail = validate.check_passive_voice('我们建议启动项目。')
    assert ok, f'被动语态应通过: {detail}'


def test_passive_voice_fail():
    ok, detail = validate.check_passive_voice('项目被建议启动，方案遭到质疑，数据被覆盖，结果得以验证。')
    assert not ok, f'被动语态应失败: {detail}'


def test_full_validate_report():
    sample = """# 测试报告

## 核心结论

建议启动电子采购平台，预期年成本节省1200万元。

## 关键发现

• 发现1：采购成本高于行业均值30% [置信度：HIGH]
• 发现2：供应商集中度风险上升 [置信度：MEDIUM]

## 业务影响

这将直接影响净利润率约1.5个百分点。

## 建议行动

1. 启动采购平台建设 — 张总负责 — Q3完成
2. 完成供应商评估 — 李经理负责 — 8月15日前

## 风险

• 系统上线延迟风险
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                      encoding='utf-8') as f:
        f.write(sample)
        f.flush()
        report = validate.validate(f.name)
    Path(f.name).unlink()

    assert report['summary']['passed'] >= 5, f'应至少5项通过，实际: {report["summary"]["score"]}'
    assert report['summary']['grade'] in ('A', 'B'), f'评级应为A或B: {report["summary"]["grade"]}'


# === density.py 测试 ===
import density


def test_density_data():
    result = density.data_density('收入增长15%，节省成本200万元，用户增长3倍。')
    assert result['总数'] >= 3, f'应检测到≥3处数据: {result}'


def test_density_paragraph():
    result = density.paragraph_analysis('短段落。\n\n中等段落内容。' * 10)
    assert result['段落数'] > 0, f'应有段落: {result}'


def test_density_fluff():
    result = density.fluff_detection('众所周知，我们要高度重视，深入推进。')
    assert len(result) > 0, f'应检测到空洞: {result}'


def test_density_action():
    result = density.action_density('建议启动项目，需要审批预算。')
    assert result['行动词'] >= 2, f'应有行动词: {result}'


def test_density_reading_time():
    result = density.estimate_reading_time('这是测试内容。' * 50)
    assert '分钟' in result or '<1' in result, f'应有阅读时间: {result}'


# === init.py 测试 ===
def test_init_smoke():
    """测试 init.py 能否正常导入"""
    import importlib
    mod = importlib.import_module('init')
    assert mod is not None, 'init.py 应可导入'


# === bump.py 测试 ===
def test_bump_smoke():
    """测试 bump.py 能否正常导入"""
    import importlib
    mod = importlib.import_module('bump')
    assert mod.parse_version('1.2.3') == (1, 2, 3)
    assert mod.parse_version('10.20.30') == (10, 20, 30)
    try:
        mod.parse_version('invalid')
        assert False, '应抛出 ValueError'
    except ValueError:
        pass


if __name__ == '__main__':
    # Manual test runner
    tests = [
        test_bluf_pass, test_bluf_fail,
        test_so_what_pass, test_so_what_fail,
        test_data_support_pass, test_data_support_fail,
        test_action_clarity_pass, test_action_clarity_fail,
        test_word_limit_pass, test_word_limit_fail,
        test_confidence_pass, test_confidence_fail,
        test_passive_voice_pass, test_passive_voice_fail,
        test_full_validate_report,
        test_density_data, test_density_paragraph,
        test_density_fluff, test_density_action,
        test_density_reading_time,
        test_init_smoke, test_bump_smoke,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print(f'  ✅ {test.__name__}')
        except AssertionError as e:
            print(f'  ❌ {test.__name__}: {e}')
        except Exception as e:
            print(f'  💥 {test.__name__}: {e}')
    print(f'\n{passed}/{len(tests)} 测试通过')
