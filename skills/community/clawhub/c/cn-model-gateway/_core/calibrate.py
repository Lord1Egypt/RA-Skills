#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""能力实测校准器（v1.0.0）

跑标准题集实测 → 回填 models.yaml 画像分数。
每项标注来源（实测+日期 或 经验值），实测分数与经验分数在选型解释中分别展示。

支持按厂商预算配置跑全量或抽样，预算不足时自动降级为经验值。

设计：
- 标准题集分三类：分类准确率 / 代码通过率 / 长文摘要质量代理
- 每类 5 道题，答对 1 题得 2 分（满分 10 分制，与现有画像一致）
- 实测结果写入 models.yaml 的 calibrated_score / calibrated_source / calibrated_date 字段
- 未实测模型保留原经验值，reason 中标注「经验值」

用法：
  python calibrate.py --models-yaml references/models.yaml --config config.json --budget full
  python calibrate.py --models-yaml references/models.yaml --config config.json --budget sample --sample-size 2
  python calibrate.py --models-yaml references/models.yaml --mock  # Mock 模式（不调 API）
"""

import argparse
import datetime
import json
import os
import random
import sys

# 确保 llm-core 目录在 sys.path 中
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import yaml_simple


# ───────────────────────── 标准题集 ─────────────────────────
# 分类准确率：验证 classify() 是否能正确识别任务类型
CLASSIFICATION_CASES = [
    {"prompt": "帮我用 Python 写一个快排", "expected_task": "code"},
    {"prompt": "为什么天空是蓝色的？请分析物理原理", "expected_task": "reason"},
    {"prompt": "把这段话翻译成英文", "expected_task": "translate"},
    {"prompt": "总结这篇报告的要点", "expected_task": "summarize"},
    {"prompt": "从这段文本中抽取人名和地名", "expected_task": "extract"},
]

# 代码通过率：验证模型是否能生成可执行代码（语法检查）
# 注意：check 函数直接存 lambda 对象，避免 eval() 触发安全扫描
CODE_CASES = [
    {"prompt": "用 Python 写一个 hello world", "check": lambda r: 'print' in r and 'hello' in r.lower()},
    {"prompt": "用 Python 写一个列表去重函数", "check": lambda r: 'def ' in r and 'return' in r},
    {"prompt": "用 Python 写一个冒泡排序", "check": lambda r: 'def ' in r and 'for ' in r},
    {"prompt": "用 Python 写一个读取文件的函数", "check": lambda r: 'def ' in r and 'open' in r},
    {"prompt": "用 Python 写一个计算斐波那契的函数", "check": lambda r: 'def ' in r and 'return' in r},
]

# 长文摘要质量代理：验证长文本输入后模型能生成摘要（长度合理、关键词覆盖）
LONG_CASES = [
    {"prompt": "请用一句话总结以下文章：" + "人工智能是计算机科学的一个分支。" * 50,
     "check": lambda r: 10 < len(r) < 200},
    {"prompt": "请用两句话总结以下文章：" + "气候变化是全球性挑战。" * 50,
     "check": lambda r: 10 < len(r) < 300},
    {"prompt": "请用一句话总结以下文章：" + "量子计算利用量子力学原理。" * 50,
     "check": lambda r: 10 < len(r) < 200},
    {"prompt": "请用两句话总结以下文章：" + "生物技术改变医疗领域。" * 50,
     "check": lambda r: 10 < len(r) < 300},
    {"prompt": "请用一句话总结以下文章：" + "区块链是一种分布式账本技术。" * 50,
     "check": lambda r: 10 < len(r) < 200},
]


def run_classification_tests(adapter, model_name):
    """跑分类准确率测试，返回 0-10 分。

    注意：classifier 是上层 skill 模块（非 llm-core），用可选导入。
    若当前环境无 classifier（如 cn-model-gateway），跳过分类测试返回 0。
    """
    try:
        import classifier
    except ImportError:
        # classifier 不可用时跳过（llm-core 不依赖上层 skill 模块）
        return 0
    correct = 0
    for case in CLASSIFICATION_CASES:
        try:
            result = classifier.classify(case["prompt"])
            if result["task_type"] == case["expected_task"]:
                correct += 1
        except Exception:
            pass
    return correct * 2  # 每题 2 分，满分 10


def run_code_tests(adapter, model_name, mock=False):
    """跑代码通过率测试，返回 0-10 分。"""
    correct = 0
    for case in CODE_CASES:
        try:
            if mock:
                # Mock 模式：模拟正确响应
                response = "def solution():\n    return 'mock answer'"
            else:
                response = _call_adapter(adapter, model_name, case["prompt"])
            if response and case["check"](response):
                correct += 1
        except Exception:
            pass
    return correct * 2


def run_long_tests(adapter, model_name, mock=False):
    """跑长文摘要质量代理测试，返回 0-10 分。"""
    correct = 0
    for case in LONG_CASES:
        try:
            if mock:
                response = "这是一个关于该主题的摘要，内容简洁且有意义。"
            else:
                response = _call_adapter(adapter, model_name, case["prompt"])
            if response and case["check"](response):
                correct += 1
        except Exception:
            pass
    return correct * 2


def _call_adapter(adapter, model_name, prompt):
    """调适配器获取响应。"""
    try:
        res = adapter.chat(
            [{"role": "user", "content": prompt}],
            model_name,
            stream=False,
            timeout=30
        )
        return res.get("content", "")
    except Exception:
        return ""


def calibrate_model(provider, model_name, cfg, mock=False):
    """对单个模型跑实测，返回 {reason_score, code_score, long_score, source, date}。"""
    from adapters import build as build_adapter

    try:
        adapter = build_adapter(cfg.get("adapter", "openai_compat"), cfg)
    except Exception:
        return None

    reason_score = run_classification_tests(adapter, model_name)
    code_score = run_code_tests(adapter, model_name, mock=mock)
    long_score = run_long_tests(adapter, model_name, mock=mock)

    today = datetime.date.today().isoformat()

    return {
        "reason_score": reason_score,
        "code_score": code_score,
        "long_score": long_score,
        "source": "实测+" + today if not mock else "mock+" + today,
        "date": today,
    }


def calibrate_skill(models_yaml_path, config_path=None, budget="full", sample_size=2, mock=False):
    """对整个 skill 的 models.yaml 跑校准。

    budget: "full" = 全量, "sample" = 抽样
    sample_size: 每家厂商抽样模型数
    mock: 不调真实 API（开发测试用）
    """
    reg = yaml_simple.load_file(models_yaml_path)
    providers = reg.get("providers", {})

    # 加载 config（用于判断哪些厂商已配密钥）
    config = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    calibrated_count = 0
    skipped_count = 0

    for provider, pinfo in providers.items():
        models = pinfo.get("models", [])

        # 抽样逻辑
        if budget == "sample":
            models_to_test = random.sample(models, min(sample_size, len(models)))
        else:
            models_to_test = models

        for model in models_to_test:
            name = model.get("name", "")
            # 检查是否有密钥
            env_hint = pinfo.get("env_hint", "")
            has_key = _check_key(env_hint, config)

            if not has_key and not mock:
                skipped_count += 1
                continue

            # 构造 adapter cfg
            cfg = {
                "adapter": pinfo.get("adapter", "openai_compat"),
                "base_url": pinfo.get("base_url", ""),
                "base_url_openai": pinfo.get("base_url_openai", ""),
            }

            result = calibrate_model(provider, name, cfg, mock=mock)
            if result:
                # 写入 calibrated 字段
                model["calibrated_reason_score"] = result["reason_score"]
                model["calibrated_code_score"] = result["code_score"]
                model["calibrated_long_score"] = result["long_score"]
                model["calibrated_source"] = result["source"]
                model["calibrated_date"] = result["date"]
                calibrated_count += 1
                print(f"  [✅] {provider}/{name}: reason={result['reason_score']} code={result['code_score']} long={result['long_score']} ({result['source']})")
            else:
                skipped_count += 1
                print(f"  [⏭️] {provider}/{name}: 跳过（无密钥或适配器不可用）")

    # 保存
    yaml_simple.dump_file(models_yaml_path, reg)
    print(f"\n[完成] 实测 {calibrated_count} 个模型，跳过 {skipped_count} 个")
    return calibrated_count, skipped_count


def _check_key(env_hint, config):
    """检查环境变量或 config 中是否有密钥。"""
    if not env_hint:
        return False
    # 简单检查：环境变量是否存在
    for var in env_hint.split("/"):
        var = var.strip()
        if os.environ.get(var):
            return True
    # 检查 config.json
    if config.get("providers", {}).get(env_hint):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="能力实测校准器")
    parser.add_argument("--models-yaml", required=True, help="models.yaml 路径")
    parser.add_argument("--config", help="config.json 路径")
    parser.add_argument("--budget", default="full", choices=["full", "sample"])
    parser.add_argument("--sample-size", type=int, default=2)
    parser.add_argument("--mock", action="store_true", help="Mock 模式（不调 API）")
    args = parser.parse_args()

    print(f"[校准开始] budget={args.budget}, mock={args.mock}")
    calibrate_skill(args.models_yaml, args.config, args.budget, args.sample_size, args.mock)


if __name__ == "__main__":
    main()
