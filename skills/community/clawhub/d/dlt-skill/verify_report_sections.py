# -*- coding: utf-8 -*-
"""
报告板块完整性反遗漏自检 (V8.9.7 新增, 用户需求: 增强版报告不得遗漏信息)

机制:
  - 定义"增强版报告必须包含的板块清单" (基础报告全部板块 + 增强层注入板块)
  - 生成报告后逐板块断言存在(按独特关键字匹配), 缺一个即列为缺失并 exit(1)
  - 接入两处:
      1) dlt_enhance.py 生成增强版后调用 (生成即自查, 缺失即告警)
      2) dlt_healthcheck_all.py 第14项 (护栏常驻巡检最近增强版报告)

为何用关键字而非精确标题: 标题可能微调, 但板块核心关键字稳定, 避免误报。
"""
import glob
import os
import sys

# 基础报告 (dlt_auto.generate_report 产出) 必需板块: (展示名, 匹配关键字)
REQUIRED_BASE = [
    ("预测组(第1~5组)", "第1组"),
    ("预测组(第1~5组)", "第5组"),
    ("胆拖方案(性价比最高)", "性价比最高胆拖组合"),
    ("各号码出现频率参考", "各号码出现频率参考"),
    ("最热/最冷组合", "最热组合"),
    ("最终诚实结论", "最终诚实结论"),
    ("历史中奖估计(你最该看的板块)", "大概中几等奖"),
    ("凯利/投注建议", "凯利"),
]

# 增强层 (dlt_enhance.enhance_report 注入) 必需板块
REQUIRED_ENHANCED_EXTRA = [
    ("号码冷热图(近30期)", "号码冷热图"),
    ("本期实时抓取专家推荐热度", "实时抓取专家推荐热度"),
    ("机器学习模型预测(第6-8组)", "机器学习模型预测"),
    ("增强模块说明", "增强模块说明"),
    ("专家体系总览(常驻名录)", "常驻专家名录总览"),
    ("专家对比分析(战绩自算)", "专家对比分析"),
]

REQUIRED_ENHANCED = REQUIRED_BASE + REQUIRED_ENHANCED_EXTRA


def verify_report(html_path, enhanced=True, verbose=True):
    """返回缺失板块的展示名列表 (空列表=完整)"""
    with open(html_path, 'r', encoding='utf-8') as f:
        text = f.read()
    req = REQUIRED_ENHANCED if enhanced else REQUIRED_BASE
    seen = {}
    missing = []
    for name, kw in req:
        if kw in text:
            seen[name] = seen.get(name, 0) + 1
        else:
            missing.append(name)
    # 去重 (第1组/第5组同属"预测组")
    missing = list(dict.fromkeys(missing))
    if verbose:
        if missing:
            print(f"  ✗ 报告缺失板块: {' | '.join(missing)}")
        else:
            print(f"  ✅ 报告板块完整性: {len(req)} 项全部齐全 ({html_path})")
    return missing


def find_latest_enhanced():
    fs = sorted(glob.glob('大乐透*_V85_增强版.html'))
    return fs[-1] if fs else None


def find_latest_base():
    fs = sorted(glob.glob('大乐透*预测报告_V8_全面修复.html'))
    return fs[-1] if fs else None


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else find_latest_enhanced()
    if not target:
        print("✗ 未找到增强版报告 (大乐透*_V85_增强版.html)")
        raise SystemExit(1)
    if not os.path.exists(target):
        print(f"✗ 文件不存在: {target}")
        raise SystemExit(1)
    missing = verify_report(target, enhanced=True, verbose=True)
    if missing:
        print(f"❌ 反遗漏自检失败: 缺失 {len(missing)} 个板块")
        raise SystemExit(1)
    print("✅ 反遗漏自检通过")
    raise SystemExit(0)
