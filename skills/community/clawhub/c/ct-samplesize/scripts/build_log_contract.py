#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_log_contract.py — 契约单一真相源 → 各部署单元各一份产物（2026-11-15）。

背景（近 30 天飞书日志实证）：
  `adapters/coze_client.py::_load_contract_required()` 原先只认
  `adapters/workbench/publish/tests/coze_cases/_contract_index.json`，而该路径在
  发布包中不存在（真实文件在 `workbench/publish/tests/`，且 §16 红线把 `tests/`
  整目录排除）。契约加载失败 → build_params 发送全部 argparse 默认值（136 键），
  出站守卫 `_trim_bloated_params` 也因同一依赖失效而放行 → 50/252 行日志膨胀。

设计（**不做防御性副本**）：
  权威源 = tests/coze_cases/_contract_index.json + scripts/samplesize_power.py，
  仅存在于开发树、不进任何发布包。本脚本按「消费者各自的加载方式」各产出一份：
    · 本地技能客户端（读 JSON）   → config/log_contract.json
    · 工作台独立发布目录（读 JSON）→ workbench/publish/config/log_contract.json
    · Coze 运行时节点（import）   → src/graphs/nodes/log_contract_data.py
  Coze 侧**不再有文件路径探测**：契约作为 Python 常量随包 import，部署布局
  （项目根挂在哪、sys.path 怎么设）与它完全无关。少一个文件 = 少一处部署故障点。

用法：python scripts/build_log_contract.py
"""
import ast
import json
import pprint
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / "tests" / "coze_cases" / "_contract_index.json"
CLI = ROOT / "scripts" / "samplesize_power.py"
# 三个**不同部署单元各自必需**的产物；同一单元内绝不放第二份。
OUT_SKILL = ROOT / "config" / "log_contract.json"
OUT_WORKBENCH = ROOT / "workbench" / "publish" / "config" / "log_contract.json"
OUT_COZE_MODULE = (ROOT / "adapters" / "coze" / "src" / "graphs" / "nodes"
                   / "log_contract_data.py")

# 通用键：任何 test 都可能携带，裁剪时一律保留（与客户端 _ALWAYS_ALLOWED_PARAMS 对齐）
COMMON = [
    "alpha", "power", "nobs", "side", "alt", "d_val", "solve_for_power",
    "user_language", "locale", "sd", "effect", "ratio", "dropout_rate",
    "curve_n_seq", "curve_power_seq", "curve_effects", "curve_effect_seq",
    "plot_dist", "curve_power_time_seq", "curve_heatmap",
    "evidence_source", "effect_ref", "justify", "audit", "show_assumptions",
    "verify_design", "verify_looks", "verify_spending",
    "n_sim", "n_cv", "account_id", "billing_token",
]

# 参数有效域（与 src/r_engine/run_task.R::.PARAM_RANGE_HINTS 逐条对齐）
# 客户端出站前用它做零网络往返的本地拦截；Coze 端作为二次兜底。
RANGES = [
    {"keys": ["effect"], "only_test": "correlation", "lo": -1, "hi": 1,
     "open": True, "zh": "相关系数", "en": "correlation coefficient"},
    {"keys": ["correlation_must", "correlation"], "only_test": None,
     "lo": -1, "hi": 1, "open": True, "zh": "相关系数", "en": "correlation coefficient"},
    {"keys": ["p1", "p2", "p1_t", "p1_c", "p_control", "p_treatment", "p_exp",
              "prop", "pi"], "only_test": None, "lo": 0, "hi": 1,
     "open": False, "zh": "率/比例", "en": "rate / proportion"},
    {"keys": ["alpha", "power", "type_i_error", "power_target", "sig_level"],
     "only_test": None, "lo": 0, "hi": 1, "open": True,
     "zh": "alpha / power", "en": "alpha / power"},
    {"keys": ["icc", "cv", "i2"], "only_test": None, "lo": 0, "hi": 1,
     "open": False, "zh": "ICC / CV / I²", "en": "ICC / CV / I2"},
    {"keys": ["s0", "s1", "sd", "sd0", "sd1", "sigma", "stdev"],
     "only_test": None, "lo": 0, "hi": None, "open": True,
     "zh": "标准差", "en": "standard deviation"},
    {"keys": ["hr", "hazard_ratio"], "only_test": None, "lo": 0, "hi": None,
     "open": True, "zh": "风险比 HR", "en": "hazard ratio"},
    {"keys": ["r", "r1", "r2"], "only_test": None, "lo": 0, "hi": None,
     "open": True, "zh": "率/比值", "en": "rate / ratio"},
]

# 已知 67 种检验的中文场景关键词（P2-7：能力发现 / 方案段落 → test 建议）
INTENT_HINTS = {
    "ttest_ind": ["两独立样本", "均数比较", "平行对照", "two-sample", "mean difference"],
    "ttest_paired": ["配对", "交叉设计", "paired", "crossover"],
    "proportion_one": ["单组率", "单臂", "single arm", "one proportion"],
    "proportion_two": ["两率比较", "有效率比较", "two proportions"],
    "non_inferiority": ["非劣效", "non-inferiority", "非劣"],
    "equivalence": ["等效性", "equivalence"],
    "be_tost": ["生物等效", "BE", "bioequivalence"],
    "survival": ["生存分析", "OS", "总生存", "log-rank", "中位生存"],
    "ni_survival": ["生存非劣效", "non-inferior survival"],
    "survival_equivalence": ["生存等效"],
    "group_sequential": ["成组序贯", "中期分析", "interim", "group sequential"],
    "gsd_survival": ["生存序贯", "interim survival"],
    "cluster": ["整群随机", "集群随机", "cluster randomized"],
    "meta_planning": ["meta", "荟萃", "研究数", "异质性", "I2"],
    "ci_prop": ["率的置信区间", "CI for proportion"],
    "ci_mean": ["均数置信区间", "CI for mean"],
    "dose_escalation": ["剂量递增", "3+3", "DLT", "dose escalation"],
    "adaptive": ["适应性设计", "adaptive design"],
    "bayesian": ["贝叶斯", "bayesian", "历史对照借用"],
    "multiple_endpoints": ["多重终点", "multiple endpoints"],
    "dunnett": ["多臂", "Dunnett", "multiple arms"],
    "win_ratio": ["win ratio", "获胜比"],
    "roc": ["ROC", "AUC", "诊断试验"],
    "correlation": ["相关性", "correlation"],
    "poisson": ["泊松", "复发事件率", "poisson"],
    "cox_covariate": ["Cox", "协变量", "HR 校正"],
    "superiority_margin": ["优效", "superiority margin"],
    "vaccine_efficacy": ["疫苗效力", "vaccine efficacy"],
}


def _argparse_defaults(path: Path) -> dict:
    """静态解析 samplesize_power.py 的 p.add_argument(default=...)，零导入副作用。"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"):
            continue
        opts = [a.value for a in node.args
                if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        long = next((o[2:].replace("-", "_") for o in opts if o.startswith("--")), None)
        dest = next((k.value.value for k in node.keywords
                     if k.arg == "dest" and isinstance(k.value, ast.Constant)
                     and isinstance(k.value.value, str)), None)
        key = dest or long
        dflt = next((k.value for k in node.keywords if k.arg == "default"), None)
        if not key or dflt is None:
            continue
        try:
            out[key] = ast.literal_eval(dflt)
        except Exception:
            continue
    return out


def main():
    if not IDX.exists():
        sys.exit("[错误] 契约索引不存在：%s" % IDX)
    idx = json.loads(IDX.read_text(encoding="utf-8"))
    tests = {}
    for e in idx.get("tests", []):
        tests[e["test"]] = {
            "required": list(e.get("required") or []),
            "optional": list(e.get("optional") or []),
        }
    defaults = _argparse_defaults(CLI) if CLI.exists() else {}
    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_of_truth": "tests/coze_cases/_contract_index.json + scripts/samplesize_power.py",
        "note": "发布包内契约，禁止依赖 tests/；由 scripts/build_log_contract.py 重建",
        "tests": tests,
        "common": COMMON,
        "ranges": RANGES,
        "argparse_defaults": defaults,
        "intent_hints": INTENT_HINTS,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    for p in (OUT_SKILL, OUT_WORKBENCH):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print("[written] %s (%d bytes)" % (p, len(text.encode("utf-8"))))

    # Coze 运行时：契约即 Python 常量，随包 import，零文件 IO / 零路径假设。
    body = pprint.pformat(payload, width=100, sort_dicts=True)
    module_src = (
        '# -*- coding: utf-8 -*-\n'
        '"""ct-samplesize 契约常量 — 自动生成，勿手工编辑。\n\n'
        '由 scripts/build_log_contract.py 从\n'
        '  tests/coze_cases/_contract_index.json + scripts/samplesize_power.py\n'
        '烘焙生成；随 Coze 部署包分发。Coze 侧 log_aggregator 直接 import 本模块，\n'
        '不做任何文件路径探测——部署目录布局与契约加载无关。\n'
        '"""\n'
        'CONTRACT = ' + body + '\n'
    )
    # 生成期自检：字面量可解析且与 JSON 产物语义完全一致（防止两侧漂移）
    literal = module_src.split("CONTRACT = ", 1)[1]
    if ast.literal_eval(literal) != payload:
        sys.exit("[错误] 生成的契约常量与 JSON 产物不一致，已中止")
    OUT_COZE_MODULE.parent.mkdir(parents=True, exist_ok=True)
    OUT_COZE_MODULE.write_text(module_src, encoding="utf-8")
    print("[written] %s (%d bytes)" % (OUT_COZE_MODULE,
                                       len(module_src.encode("utf-8"))))
    print("tests=%d  ranges=%d  argparse_defaults=%d  intent_hints=%d"
          % (len(tests), len(RANGES), len(defaults), len(INTENT_HINTS)))


if __name__ == "__main__":
    main()
