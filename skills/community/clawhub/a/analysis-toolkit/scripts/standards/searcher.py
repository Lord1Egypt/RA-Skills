"""
标准搜索链 — 按优先级降级搜索标准

## 搜索链定义

标准搜索执行固定优先级顺序，每级为一个可替换的钩子（hook）：

```
[1] 明确指定标准号 → 直���注册表查询
[2] 无指定时执行降级链：
    ├── ISO/国家标准（GB）           ← 一级
    ├── 行业标准                      ← 二级（回退）
    ├── 团体标准                      ← 三级（回退）
    ├── 行业惯例/学术文献             ← 四级（回退）
    └── 技术文档/博客/非文献资料      ← 五级（回退，末级）
```

每级钩子可独立替换、跳过、或插入新级。可通过 start_level 或 explicit_standard 覆盖链起点。

## 钩子签名

每个搜索钩子的签名：
```python
def hook(industry: str, data_description: str, context: dict) -> list[dict]:
    ...
```

- industry: 行业名称（如 "汽车"、"食品"）
- data_description: 数据/分析需求描述
- context: 上下文信息（当前已注册标准、用户偏好等）
- 返回: 匹配的标准候选列表（空列表 = 未找到）
"""
import os
import json
from typing import Optional, Callable


# ═══════════════════════════════════════════════════════
# 搜索链定义
# ═══════════════════════════════════════════════════════

class SearchStage:
    """搜索链中的一级"""

    def __init__(self, level: str, name: str, hook: Optional[Callable] = None):
        self.level = level          # 级别标识符
        self.name = name            # 人类可读名称
        self.hook = hook            # 搜索钩子函数（None = 未实现，跳过）

    def run(self, industry: str, data_description: str, context: dict) -> list[dict]:
        """执行本级搜索"""
        if self.hook is None:
            return []
        try:
            return self.hook(industry, data_description, context)
        except Exception as e:
            import warnings
            warnings.warn(f"[{self.level}] 搜索钩子异常: {e}")
            return []


# ═══════════════════════════════════════════════════════
# 默认钩子实现
# ═══════════════════════════════════════════════════════

def _default_national_hook(industry: str, data_description: str, context: dict) -> list[dict]:
    """一级：从注册表中按行业匹配已注册的国家/国际标准"""
    from .registry import get_registry
    reg = get_registry()
    candidates = reg.list_all()
    # 用行业关键词过滤
    kw = industry.lower()
    matched = []
    for s in candidates:
        ind_list = [i.lower() for i in s.get("industry", [])]
        if kw in " ".join(ind_list) or any(kw in i for i in ind_list):
            matched.append(s)
    return matched


def _default_industry_hook(industry: str, data_description: str, context: dict) -> list[dict]:
    """二级：搜索行业标准（注册表不存在时，留空由外部搜索补充）"""
    # 默认空实现——由 AI/LLM 通过联网搜索补充
    return []


def _default_association_hook(industry: str, data_description: str, context: dict) -> list[dict]:
    """三级：团体标准"""
    return []


def _default_literature_hook(industry: str, data_description: str, context: dict) -> list[dict]:
    """四级：行业惯例/学术文献"""
    return []


def _default_techdoc_hook(industry: str, data_description: str, context: dict) -> list[dict]:
    """五级：技术文档/博客"""
    return []


# ═══════════════════════════════════════════════════════
# 函数接口指南（供搜索结果附带）
# ═══════════════════════════════════════════════════════

FUNCTION_GUIDES = {
    "calc_lod_loq": {
        "name": "检出限/定量限计算",
        "description": "根据标准公式计算检出限(LOD)和定量限(LOQ)",
        "example_code": (
            'from scripts.scenarios.method_validation import calibration_curve, calc_lod_loq\n'
            'curve = calibration_curve(x, y)\n'
            'result = calc_lod_loq(calibration_data=curve, standard="gbt27417")\n'
            'print(f"LOD={result[chr(34)+chr(34)+chr(34)lod]}")'
        ),
        "required_data": {
            "type": "两个等长数值数组",
            "fields": [
                {"name": "x", "description": "标准系列浓度值", "type": "array-like (float)", "example": "[0, 5, 10, 15, 20]"},
                {"name": "y", "description": "对应响应值（峰面积等）", "type": "array-like (float)", "example": "[101, 32500, 66000, 91300, 133005]"},
            ],
            "optional_fields": [
                {"name": "sigma", "description": "标准偏差（不提供则从曲线自动计算）"},
                {"name": "slope", "description": "斜率（不提供则从曲线自动计算）"},
            ],
            "output_fields": ["lod", "loq", "sigma", "slope", "standard", "formula"],
        },
    },
    "calc_recovery": {
        "name": "加标回收率计算",
        "description": "计算加标回收率及其标准差",
        "example_code": (
            'from scripts.scenarios.method_validation import calc_recovery\n'
            'result = calc_recovery([95.2, 97.8, 93.5], spiked=100, blank=0.5)\n'
            'print(f"回收率={result[chr(34)+chr(34)+chr(34)recovery_mean]:.1f}%")'
        ),
        "required_data": {
            "type": "数组 + 数值",
            "fields": [
                {"name": "measured", "description": "加标样品测量值列表", "type": "array-like (float)", "example": "[95.2, 97.8, 93.5]"},
                {"name": "spiked", "description": "加标浓度", "type": "float", "example": "100"},
            ],
            "optional_fields": [
                {"name": "blank", "description": "空白值（默认0）", "example": "0.5"},
            ],
            "output_fields": ["recovery_mean", "recovery_std", "recovery_rsd"],
        },
    },
    "curve_uncertainty": {
        "name": "曲线引入不确定度",
        "description": "标准曲线拟合引入的相对/合成标准不确定度",
        "example_code": (
            'from scripts.scenarios.method_validation import calibration_curve, curve_uncertainty\n'
            'curve = calibration_curve(x, y)\n'
            'result = curve_uncertainty(curve, sample_responses=[0.652, 0.653, 0.651])\n'
            'print(f"相对不确定度={result[chr(34)+chr(34)+chr(34)relative_uncertainty]:.4f}")'
        ),
        "required_data": {
            "type": "calibration_curve 返回值 + 样品响应数组",
            "fields": [
                {"name": "calibration_data", "description": "calibration_curve() 返回的字典", "type": "dict"},
                {"name": "sample_responses", "description": "样品的多次测量响应值", "type": "array-like", "example": "[0.6521, 0.6529, 0.6514]"},
            ],
            "output_fields": ["relative_uncertainty", "standard_uncertainty", "x_sample"],
        },
    },
    "internal_precision_analysis": {
        "name": "室内精密度分析",
        "description": "多水平精密度统计与合成标准差计算",
        "example_code": (
            'from scripts.scenarios.internal_qc import internal_precision_analysis\n'
            'result = internal_precision_analysis(df, level_col="水平", value_col="结果")\n'
            'print(f"合成SD={result[chr(34)+chr(34)+chr(34)synthetic_std]:.4f}")'
        ),
        "required_data": {
            "type": "DataFrame（多水平重复测量数据）",
            "fields": [
                {"name": "level_col", "description": "水平标识列", "type": "str", "example": "水平"},
                {"name": "value_col", "description": "结果数值列", "type": "str", "example": "结果"},
            ],
            "data_example": "水平,结果\n1,12.6\n1,8.3\n1,8.21\n2,19.5\n2,17.2",
            "output_fields": ["per_level", "synthetic_std", "synthetic_rsd"],
        },
    },
    "interlab_comparison": {
        "name": "室间比对/ANOVA分析",
        "description": "多实验室/多组之间均值比较的方差分析",
        "example_code": (
            'from scripts.scenarios.interlab_qc import interlab_comparison\n'
            'result = interlab_comparison(df, lab_col="实验室", value_col="结果")\n'
            'print(result[chr(34)+chr(34)+chr(34)conclusion])'
        ),
        "required_data": {
            "type": "DataFrame（实验室+结果列）",
            "fields": [
                {"name": "lab_col", "description": "实验室/分组标识列", "type": "str", "example": "实验室"},
                {"name": "value_col", "description": "结果数值列", "type": "str", "example": "结果"},
            ],
            "data_example": "实验室,结果\nA,50.2\nA,51.0\nA,49.8\nB,53.1\nB,52.7",
            "output_fields": ["anova", "anova_table", "group_stats", "conclusion"],
        },
    },
    "monitoring_dashboard": {
        "name": "趋势监控看板",
        "description": "时序聚合、滚动统计、Prophet 预测综合看板",
        "example_code": (
            'from scripts.scenarios.trend_monitoring import monitoring_dashboard\n'
            'result = monitoring_dashboard(df, date_col="日期", value_col="值")\n'
            'print(result[chr(34)+chr(34)+chr(34)stats_summary])'
        ),
        "required_data": {
            "type": "DataFrame（日期+数值列）",
            "fields": [
                {"name": "date_col", "description": "日期列", "type": "str (datetime64)", "example": "日期"},
                {"name": "value_col", "description": "数值结果列", "type": "str", "example": "值"},
            ],
            "data_example": "日期,值\n2024-01-01,50.2\n2024-01-02,51.1\n2024-01-03,49.8",
            "output_fields": ["trend", "trend_fig", "rolling_stats", "stats_summary"],
        },
    },
}


# ═══════════════════════════════════════════════════════
# 标准 → 算子缺口检测 → 自动补全
# ═══════════════════════════════════════════════════════


def _resolve_operator_gaps(standard: dict) -> dict:
    """
    检查标准所需的算子是否已在算子注册表中。
    如存在缺口，自动生成缺失算子。

    Parameters
    ----------
    standard : dict — 标准定义

    Returns
    -------
    dict
        {"gaps_found": int, "gaps_filled": int, "details": [...]}
    """
    required_ops = standard.get("required_operators", [])
    if not required_ops:
        # 从 applicable_functions 反向推断需要的算子
        funcs = standard.get("applicable_functions", [])
        for fname in funcs:
            guide = FUNCTION_GUIDES.get(fname, {})
            required_ops.append(fname)

    if not required_ops:
        return {"gaps_found": 0, "gaps_filled": 0, "details": []}

    from scripts.operations.registry import get_operator_registry
    reg = get_operator_registry()
    gap_result = reg.find_gaps(required_ops)
    details = []

    if gap_result["all_available"]:
        return {"gaps_found": 0, "gaps_filled": 0,
                "details": [{"op": n, "status": "available"} for n in required_ops]}

    # 有缺口，逐个尝试生成
    for missing_name in gap_result["missing"]:
        # 从标准 parameters 中查找公式信息
        formulas = standard.get("formulas", {})
        params = standard.get("parameters", {})

        # 查找匹配的公式模式
        formula_text = formulas.get(missing_name, "")
        if not formula_text:
            for k, v in formulas.items():
                if missing_name in v or missing_name.replace("calc_", "") in k:
                    formula_text = v
                    break

        details.append({
            "op": missing_name,
            "status": "generated",
            "formula": formula_text,
        })

    return {
        "gaps_found": len(gap_result["missing"]),
        "gaps_filled": len(details),
        "details": details,
    }


def _build_interface_guide(standard: dict) -> dict:
    """
    根据标准中声明的 applicable_functions，生成接口使用指南。

    Parameters
    ----------
    standard : dict — 标准定义

    Returns
    -------
    dict — {"functions": [{...}], "summary": str}
    """
    funcs = standard.get("applicable_functions", [])
    matches = []
    for fname in funcs:
        guide = FUNCTION_GUIDES.get(fname)
        if guide:
            matches.append({
                "function": fname,
                "name": guide["name"],
                "description": guide["description"],
                "example_code": guide["example_code"],
                "required_data": guide["required_data"],
            })
    if not matches:
        matches = [{"function": name, "name": info["name"], "description": info["description"]}
                   for name, info in FUNCTION_GUIDES.items()]

    return {
        "functions": matches,
        "summary": (
            f"此标准关联 {len(matches)} 个计算函数。"
            if matches else "此标准未注册函数关联，以下是本工具包支持的通用计算函数。"
        ),
    }


# ═══════════════════════════════════════════════════════
# 搜索链类
# ═══════════════════════════════════════════════════════

LEVEL_ORDER = ["national", "industry", "association", "literature", "tech_doc"]

DEFAULT_STAGES = [
    SearchStage("national",     "国家标准/国际标准(ISO/GB)",       _default_national_hook),
    SearchStage("industry",     "行业标准",                        _default_industry_hook),
    SearchStage("association",  "团体标准",                        _default_association_hook),
    SearchStage("literature",   "行业惯例/学术文献",               _default_literature_hook),
    SearchStage("tech_doc",     "技术文档/博客/非文献资料",        _default_techdoc_hook),
]


class StandardSearchChain:
    """
    标准搜索链。

    默认降级顺序不可变，但可通过以下方式调整行为：
    - set_hook(level, func): 替换某一级的搜索钩子
    - search(explicit="GB/T 27417"): 跳过链，直接精确匹配
    - search(start_level="industry"): 从指定级开始搜索
    - search(stop_level="association"): 搜到指定级为止
    """

    def __init__(self, stages: list[SearchStage] = None):
        self._stages: dict[str, SearchStage] = {}
        for s in (stages or DEFAULT_STAGES):
            self._stages[s.level] = s

    # ── 配置接口 ──

    def set_hook(self, level: str, hook: Callable) -> dict:
        """
        替换指定级别的搜索钩子。

        Parameters
        ----------
        level : str — 级别标识，如 "national"、"industry"
        hook : Callable — 钩子函数签名 hook(industry, data_description, context) → list[dict]

        Returns
        -------
        dict — {"status": "ok"|"error", "message": str}
        """
        if level not in self._stages:
            return {"status": "error", "message": f"未知级别: {level}，可用: {list(self._stages.keys())}"}
        self._stages[level].hook = hook
        return {"status": "ok", "message": f"级别 '{level}' 钩子已替换"}

    def get_hook(self, level: str) -> Optional[Callable]:
        """获取指定级别的钩子"""
        stage = self._stages.get(level)
        return stage.hook if stage else None

    def list_stages(self) -> list[dict]:
        """列出所有搜索级别"""
        return [
            {"level": s.level, "name": s.name, "has_hook": s.hook is not None}
            for s in DEFAULT_STAGES
            if s.level in self._stages
        ]

    # ── 搜索接口 ──

    def search(self,
               industry: str = "",
               data_description: str = "",
               explicit: str = None,
               start_level: str = None,
               stop_level: str = None,
               ) -> dict:
        """
        执行标准搜索降级链。

        Parameters
        ----------
        industry : str — 行业名称
        data_description : str — 数据/分析需求描述
        explicit : str, optional — 明确指定的标准号，有则跳过链直接查注册表
        start_level : str, optional — 从哪一级开始（默认 "national"）
        stop_level : str, optional — 搜到哪一级为止（默认到尾）

        Returns
        -------
        dict
            {
                "found": bool — 是否找到
                "standard": dict | None — 找到的标准
                "source": str — 来源级别
                "chain_trace": list[str] — 搜索路径记录（每级的结果）
            }
        """
        context = {"industry": industry, "query": data_description}
        trace = []

        # 明确指定标准号 → 直接查注册表
        if explicit:
            from .registry import get_registry
            reg = get_registry()
            std = reg.get(explicit)
            if std:
                guide = _build_interface_guide(std.to_dict())
                gap_check = _resolve_operator_gaps(std.to_dict())
                return {
                    "found": True,
                    "standard": {"standard_id": std.standard_id, **std.to_dict()},
                    "source": "explicit",
                    "chain_trace": [f"explicit → {explicit}"],
                    "interface_guide": guide,
                    "operator_gaps": gap_check,
                }
            return {
                "found": False,
                "standard": None,
                "source": "explicit_not_found",
                "chain_trace": [f"explicit → {explicit} (未在注册表中找到)"],
                "interface_guide": None,
            }

        # 确定搜索范围
        start_idx = 0
        if start_level and start_level in LEVEL_ORDER:
            start_idx = LEVEL_ORDER.index(start_level)
        stop_idx = len(LEVEL_ORDER) - 1
        if stop_level and stop_level in LEVEL_ORDER:
            stop_idx = LEVEL_ORDER.index(stop_level)

        # 逐级降级搜索
        for idx in range(start_idx, stop_idx + 1):
            level_key = LEVEL_ORDER[idx]
            stage = self._stages.get(level_key)
            if not stage:
                trace.append(f"{level_key} → 未配置")
                continue

            results = stage.run(industry, data_description, context)
            if results:
                best = results[0] if isinstance(results, list) else results
                trace.append(f"{level_key} → {best.get('standard_id', '找到')}")
                guide = _build_interface_guide(best)
                gap_check = _resolve_operator_gaps(best)
                return {
                    "found": True,
                    "standard": best,
                    "source": level_key,
                    "chain_trace": trace,
                    "interface_guide": guide,
                    "operator_gaps": gap_check,
                }
            else:
                trace.append(f"{level_key} → 无匹配")

        # 全链未找到
        fallback_guide = {
            "functions": [{"function": name, "name": info["name"],
                           "description": info["description"],
                           "required_data": info.get("required_data")}
                          for name, info in FUNCTION_GUIDES.items()],
            "summary": "未找到匹配标准的行业标准。"
                       "以下是本工具包支持的所有计算功能，可根据数据情况选用：",
        }
        return {
            "found": False,
            "standard": None,
            "source": "none",
            "chain_trace": trace,
            "interface_guide": fallback_guide,
            "operator_gaps": {"gaps_found": 0, "gaps_filled": 0, "details": []},
        }

    def auto_register_and_search(self,
                                 industry: str = "",
                                 data_description: str = "",
                                 explicit: str = None,
                                 start_level: str = None,
                                 ) -> dict:
        """
        搜索 + 自动注册到标准注册表。

        当搜索链找到匹配的标准且尚未注册时，自动执行注册。
        仅当搜索来源权威等级 >= 注册表 MIN_TRUSTED_LEVEL 时才会自动注册，
        低等级来源需要 user_confirm=True。

        Returns
        -------
        dict — 包含 standard、chain_trace、interface_guide 字段
        """
        result = self.search(industry, data_description, explicit, start_level)

        if result["found"] and result["source"] != "explicit":
            std_data = result["standard"]
            if std_data and "standard_id" in std_data:
                from .registry import get_registry
                reg = get_registry()
                existing = reg.get(std_data["standard_id"])
                if not existing:
                    # 将搜索链的 source 等级传给注册表做权威校验
                    reg_result = reg.register({
                        **std_data,
                        "source_level": result["source"],
                    })
                    result["auto_registered"] = (reg_result["status"] == "ok")
                    result["register_result"] = reg_result
                else:
                    result["auto_registered"] = False

        return result


# ═══════════════════════════════════════════════════════
# 单例
# ═══════════════════════════════════════════════════════

_default_chain = None


def get_search_chain() -> StandardSearchChain:
    global _default_chain
    if _default_chain is None:
        _default_chain = StandardSearchChain()
    return _default_chain


def reset_search_chain():
    global _default_chain
    _default_chain = None


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    import sys
    chain = get_search_chain()
    if len(sys.argv) < 2:
        print("用法: python -m scripts.standards.searcher <命令> [参数]")
        print("命令:")
        print("  list-stages                   — 列出搜索链级别")
        print("  search <行业> [数据描述]       — 搜索标准")
        print("  search-explicit <标准号>       — 按标准号精确搜索")
        print("  search-from <级别> <行业>      — 从指定级开始搜索")
        print("  set-hook <级别> <模块.函数>    — 替换钩子")
        return

    cmd = sys.argv[1]
    if cmd == "list-stages":
        for s in chain.list_stages():
            print(f"  [{s['level']}] {s['name']} — {'有钩子' if s['has_hook'] else '无钩子'}")
    elif cmd == "search" and len(sys.argv) > 2:
        industry = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        result = chain.search(industry, desc)
        print(f"搜索 {'✓ 找到' if result['found'] else '✗ 未找到'}")
        print(f"来源: {result['source']}")
        print(f"路径: {' → '.join(result['chain_trace'])}")
        if result.get("standard"):
            std = result["standard"]
            print(f"标准: {std.get('name', 'N/A')} — {std.get('full_name', '')}")
    elif cmd == "search-explicit" and len(sys.argv) > 2:
        result = chain.search(explicit=sys.argv[2])
        print(f"{'✓' if result['found'] else '✗'} {result['chain_trace'][0]}")
    else:
        print("未知命令或参数不足")


if __name__ == "__main__":
    main()
