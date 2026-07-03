"""
Pipeline 引擎 — 定义和执行分析流水线。

一个 Pipeline 是一系列有序步骤（Step），
每个步骤指向一个函数及其参数，
上一步的结果可传递给下一步。

集成：
  - 钩子系统（pipeline:pre / step:post）：运行前校验 + 执行中守卫
  - 自动验证（verify）：执行后数学交叉验证
  - 自动报告（report）：default_report 存在时自动渲染 HTML

示例：

    pipe = Pipeline("我的分析", steps=[
        Step("加载", "core.loader.load_data", {"path": "data.xlsx"}),
        Step("精密度", "scenarios.internal_qc.internal_precision_analysis",
             {"data": "%加载%", "level_col": "水平", "value_col": "结果"}),
        Step("质控图", "scenarios.internal_qc.control_chart",
             {"data": "%加载%", "value_col": "结果"}),
    ])
    r = pipe.run(input_data)
    # → {"精密度": {...}, "质控图": {...}, "__verify__": {...}, "__report_path__": "..."}
"""
import importlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable


@dataclass
class Step:
    """流水线的一个步骤"""
    name: str                              # 步骤名称（用于引用输出）
    target: str                            # "module.func_name"，如 "scenarios.internal_qc.control_chart"
    params: Dict[str, Any] = field(default_factory=dict)  # 参数
    description: str = ""                  # 可选说明

    def resolve(self, context: Dict[str, Any]) -> Callable:
        """将 target 字符串解析为实际函数"""
        mod_path, func_name = self.target.rsplit(".", 1)
        mod = importlib.import_module(f"scripts.{mod_path}")
        return getattr(mod, func_name)

    def resolve_params(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """将参数中的引用替换为上下文中的实际值。

        引用语法：
            %input%     — 整个原始输入数据
            %step_name% — 上一步的完整返回值 dict
            %step_name.key% — 上一步返回值中的某个字段
        """
        resolved = {}
        for k, v in self.params.items():
            if isinstance(v, str) and v.startswith("%") and v.endswith("%"):
                ref = v[1:-1]
                if ref == "input":
                    resolved[k] = context.get("__input__")
                elif ref.startswith("input."):
                    key = ref[6:]
                    inp = context.get("__input__", {})
                    resolved[k] = inp.get(key) if isinstance(inp, dict) else inp
                elif "." in ref:
                    step, key = ref.split(".", 1)
                    step_result = context.get(step, {})
                    resolved[k] = step_result.get(key) if isinstance(step_result, dict) else step_result
                else:
                    resolved[k] = context.get(ref)
            else:
                resolved[k] = v
        return resolved


@dataclass
class Pipeline:
    """分析流水线"""
    name: str
    steps: List[Step]
    description: str = ""
    tags: List[str] = field(default_factory=list)
    default_report: str = ""  # v2: 默认关联的特色报告模板名

    def run(self, input_data=None, verbose=True) -> Dict[str, Any]:
        """
        依次执行所有步骤。

        流程：
          1. pipeline:pre 钩子（引用/函数/报告校验）
          2. 依次执行 Step（每步后 step:post 钩子）
          3. 自动验证（verify）
          4. 自动渲染报告（default_report 存在时）

        Parameters
        ----------
        input_data : any, optional
        verbose : bool

        Returns
        -------
        dict
            {step_name: step_return, ..., "__verify__": ..., "__report_path__": "...", "__report_html__": "..."}
        """
        context = {"__input__": input_data, "_pipeline": self}
        results = {}

        # ── 1. pipeline:pre 钩子 ──
        from .hooks import run as run_hooks
        pre_check = run_hooks("pipeline:pre", context)
        if pre_check.get("block"):
            results["__hook_error__"] = pre_check
            return results

        if verbose:
            print(f"▶ 运行流水线: {self.name}")
            print(f"  共 {len(self.steps)} 步")
            print()

        # ── 2. 依次执行步骤 ──
        for i, step in enumerate(self.steps):
            if verbose:
                print(f"  [{i+1}/{len(self.steps)}] {step.name} ... ", end="", flush=True)

            step_failed = False
            try:
                func = step.resolve(context)
                params = step.resolve_params(context)

                import inspect
                sig = inspect.signature(func)
                filtered_params = {}
                for pname in sig.parameters:
                    if pname in params:
                        filtered_params[pname] = params[pname]

                result = func(**filtered_params)
                context[step.name] = result
                results[step.name] = result

                # step:post 钩子
                ctx = context.copy()
                ctx["_current_step"] = step
                ctx["_current_result"] = result
                post_check = run_hooks("step:post", ctx)
                if post_check.get("block"):
                    results[step.name] = {"error": post_check.get("reason", "步后校验失败"),
                                          "hook_suggestion": post_check.get("suggestion", "")}
                    step_failed = True
                    if verbose:
                        print(f"✗ {post_check.get('reason', '校验失败')}")
                else:
                    if verbose:
                        rtype = type(result).__name__
                        print(f"✓ ({rtype})")

            except Exception as e:
                if verbose:
                    print(f"✗ 失败: {e}")
                results[step.name] = {"error": str(e)}
                step_failed = True

            # 标记失败步骤，下游依赖它的步骤可以跳过
            if step_failed:
                context[step.name] = None

        if verbose:
            success = sum(1 for v in results.values()
                         if not (isinstance(v, dict) and "error" in v))
            print(f"  ✅ 完成: {success}/{len(self.steps)} 步成功")

        # ── 3. 自动验证 ──
        try:
            from .verify import verify_all, verify_summary
            v_results = verify_all(results, context)
            results["__verify__"] = {
                "results": v_results,
                "summary": verify_summary(v_results),
                "passed": all(v.get("pass") for v in v_results if v.get("pass") is not None),
            }
            if verbose:
                print(f"\n{results['__verify__']['summary']}")
        except Exception as e:
            if verbose:
                print(f"\n  ⚠ 验证未执行: {e}")

        # ── 4. 自动渲染报告 ──
        if self.default_report:
            try:
                from scripts.reporting.report_engine import load_report_config, render_report
                from scripts.reporting.renderer import save_html

                report_config = load_report_config(self.default_report)
                html = render_report(report_config, results, {"__input__": input_data})

                # 保存报告文件
                safe_name = self.name.replace(" ", "_").replace("/", "_")
                report_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    ".standardization", "analysis-toolkit", "data", "reports"
                )
                os.makedirs(report_dir, exist_ok=True)
                report_path = os.path.join(report_dir, f"{safe_name}_report.html")
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(html)

                results["__report_html__"] = html
                results["__report_path__"] = report_path
                results["__report_name__"] = self.default_report

                if verbose:
                    print(f"\n  📄 报告已生成: {self.default_report}")

            except Exception as e:
                results["__report_error__"] = str(e)
                if verbose:
                    print(f"\n  ⚠ 报告渲染失败: {e}")

        return results

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "steps": [{"name": s.name, "target": s.target, "params": s.params, "description": s.description}
                      for s in self.steps],
        }
        if self.default_report:
            result["default_report"] = self.default_report
        return result

    @classmethod
    def from_dict(cls, d: dict) -> "Pipeline":
        steps = [Step(**s) for s in d["steps"]]
        return cls(name=d["name"], steps=steps,
                   description=d.get("description", ""),
                   tags=d.get("tags", []),
                   default_report=d.get("default_report", ""))


def pipeline(*steps, name="未命名流水线", description="", tags=None):
    """快速创建 Pipeline 的便捷函数。"""
    return Pipeline(
        name=name,
        steps=list(steps),
        description=description,
        tags=tags or [],
    )


def step(name, target, **params):
    """创建单个步骤的便捷函数。"""
    return Step(name=name, target=target, params=params)
