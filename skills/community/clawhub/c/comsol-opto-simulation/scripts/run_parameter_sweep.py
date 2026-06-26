#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数扫描批量仿真脚本（Parameter Sweep Batch Simulation）。

功能：
  1. 基于单个基础配置（base config），自动生成多组参数组合的仿真配置
  2. 串行或并行调度光学 / 光电子 / 热耦合仿真
  3. 每组仿真后自动调用 extract_detector_metrics.py 提取性能指标
  4. 汇总所有工况结果到统一 CSV 与对比图

支持的扫描模式：
  - single_parameter: 单参数线性/对数扫描
  - multi_parameter:  多参数笛卡尔积网格扫描
  - sequential:       断点续跑（跳过已有结果的工况）
  - parallel:           多进程并行（需 COMSOL 许可证支持多实例）

用法：
    python run_parameter_sweep.py --config config_sweep.json

config_sweep.json 示例见：templates/config_sweep.json
"""

from __future__ import annotations

import argparse
import copy
import csv
import itertools
import json
import math
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Sequence

# ── path setup ─────────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

# ── dataclasses ──────────────────────────────────────────────────

@dataclass
class SweepResult:
    """单个工况的汇总结果。"""
    case_id: int
    params: dict
    status: str = "pending"
    output_dir: str = ""
    model_path: str = ""
    metrics: dict = field(default_factory=dict)
    elapsed_sec: float = 0.0
    error_message: str = ""


@dataclass
class SweepConfig:
    """扫描总配置（由 JSON 解析）。"""
    base_config: dict                        # 基础仿真配置（Type A/B/C）
    simulation_type: str                     # "optical" | "optoelectronic" | "thermal_coupled"
    sweep_parameters: list[dict]              # 扫描参数定义列表
    parallel: bool = False                   # 是否并行
    max_workers: int = 1                     # 并行进程数
    output_dir: str = "output/sweep"          # 总输出目录
    resume: bool = True                       # 断点续跑（跳过已存在的 case）
    extract_metrics: bool = True            # 仿真后是否自动提取指标
    generate_summary_plots: bool = True       # 是否生成汇总对比图
    verbose: bool = True


# ── parameter generators ─────────────────────────────────────────

def generate_values(spec: dict) -> list[Any]:
    """根据 spec 生成参数值列表。
    
    spec 格式：
      { "name": "<CONFIGURE_MATERIAL_OR_COMPONENT_A>.thickness_nm", "mode": "lin", "start": 50, "stop": 200, "points": 4 }
      { "name": "<CONFIGURE_MATERIAL_OR_COMPONENT_A>.Na", "mode": "log", "start": 1e16, "stop": 1e18, "points": 5 }
      { "name": "<CONFIGURE_MATERIAL_OR_COMPONENT_A>.Na", "mode": "list", "values": [1e16, 5e16, 1e17, 5e17, 1e18] }
    """
    mode = spec.get("mode", "lin")
    if mode == "list":
        return spec["values"]
    
    start = float(spec["start"])
    stop = float(spec["stop"])
    points = int(spec["points"])
    
    if mode == "lin":
        if points == 1:
            return [start]
        step = (stop - start) / (points - 1)
        return [start + step * i for i in range(points)]
    
    elif mode == "log":
        if points == 1:
            return [start]
        log_start = math.log10(start)
        log_stop = math.log10(stop)
        step = (log_stop - log_start) / (points - 1)
        return [10 ** (log_start + step * i) for i in range(points)]
    
    else:
        raise ValueError(f"Unsupported sweep mode: {mode}")


def generate_all_combinations(sweep_parameters: list[dict]) -> list[tuple[int, dict]]:
    """生成所有参数组合的笛卡尔积，返回 [(case_id, param_dict), ...]。"""
    names = [p["name"] for p in sweep_parameters]
    value_lists = [generate_values(p) for p in sweep_parameters]
    
    combos = []
    case_id = 0
    for combo in itertools.product(*value_lists):
        param_dict = dict(zip(names, combo))
        combos.append((case_id, param_dict))
        case_id += 1
    
    return combos


# ── config injection ───────────────────────────────────────────

def inject_param(base_config: dict, param_path: str, value: Any) -> dict:
    """按路径将参数注入到配置字典中。路径用 '.' 分隔。
    
    示例：
      "device_stack.layers.1.thickness_nm" -> 修改第 1 层的厚度
      "temperature_K" -> 顶层字段
      "bias_range.start_V" -> 嵌套字段
    """
    cfg = copy.deepcopy(base_config)
    keys = param_path.split(".")
    
    target = cfg
    i = 0
    while i < len(keys):
        key = keys[i]
        if key == "layers" and i + 1 < len(keys):
            # 下一个是层索引
            idx = int(keys[i + 1])
            if "device_stack" in target and "layers" in target["device_stack"]:
                target = target["device_stack"]["layers"][idx]
            elif "layers" in target:
                target = target["layers"][idx]
            else:
                raise KeyError(f"Cannot resolve path: {param_path}")
            i += 2
        else:
            if i == len(keys) - 1:
                # 最后一个 key：写入值
                target[key] = value
                break
            else:
                target = target[key]
                i += 1
    
    return cfg


# ── runner ─────────────────────────────────────────────────────

def run_single_case(case_id: int, params: dict, sweep_cfg: SweepConfig) -> SweepResult:
    """执行单个工况的仿真 + 可选提取。"""
    
    result = SweepResult(case_id=case_id, params=params)
    t0 = time.time()
    
    try:
        # 构建该工况的专属输出目录
        case_dir = Path(sweep_cfg.output_dir) / f"case_{case_id:04d}"
        case_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(case_dir)
        
        # 断点续跑检查
        done_marker = case_dir / ".done"
        if sweep_cfg.resume and done_marker.exists():
            result.status = "skipped"
            result.elapsed_sec = 0.0
            # 尝试读取已有的 metrics
            metrics_file = case_dir / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file, "r", encoding="utf-8") as f:
                    result.metrics = json.load(f)
            return result
        
        # 注入参数，生成临时 config
        case_config = copy.deepcopy(sweep_cfg.base_config)
        for path, val in params.items():
            case_config = inject_param(case_config, path, val)
        
        # 设置该工况的输出目录（覆盖 base_config 中的 output_dir）
        case_config["output_dir"] = str(case_dir)
        
        # 保存该工况的 config
        case_config_path = case_dir / "case_config.json"
        with open(case_config_path, "w", encoding="utf-8") as f:
            json.dump(case_config, f, indent=2, ensure_ascii=False)
        
        # ── 调用对应仿真脚本 ───────────────────────────────────
        sim_type = sweep_cfg.simulation_type
        
        # Support mock override for offline testing
        if sim_type == "mock":
            mock_script = os.environ.get("MOCK_SIM_SCRIPT")
            if mock_script and Path(mock_script).exists():
                script = Path(mock_script)
            else:
                raise ValueError("MOCK_SIM_SCRIPT env var required for simulation_type='mock'")
        elif sim_type == "optical":
            script = SCRIPT_DIR / "run_optical_simulation.py"
        elif sim_type == "optoelectronic":
            script = SCRIPT_DIR / "run_optoelectronic_sim.py"
        elif sim_type == "thermal_coupled":
            script = SCRIPT_DIR / "run_thermal_coupled_sim.py"
        else:
            raise ValueError(f"Unknown simulation_type: {sim_type}")
        
        # 设置 PYTHONPATH 包含 vendor
        env = os.environ.copy()
        pp = str(VENDOR_DIR)
        if env.get("PYTHONPATH"):
            pp = os.pathsep.join([pp, env["PYTHONPATH"]])
        env["PYTHONPATH"] = pp
        
        cmd = [
            sys.executable, str(script),
            "--config", str(case_config_path)
        ]
        
        if sweep_cfg.verbose:
            print(f"[Case {case_id:04d}] Running: {' '.join(cmd)}")
        
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(SKILL_DIR),
            env=env,
            check=False,
        )
        
        # 解析仿真输出
        sim_output = {}
        try:
            sim_output = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else {}
        except json.JSONDecodeError:
            sim_output = {"raw_stdout": proc.stdout.strip()[-500:]}
        
        if proc.returncode != 0:
            result.status = "sim_error"
            result.error_message = f"Simulation failed (rc={proc.returncode}): {proc.stderr.strip()[-500:]}"
            return result
        
        result.model_path = sim_output.get("model_saved", "")
        
        # ── 自动提取指标 ───────────────────────────────────────
        if sweep_cfg.extract_metrics and result.model_path:
            extract_script = SCRIPT_DIR / "extract_detector_metrics.py"
            extract_config_path = case_dir / "extract_config.json"
            extract_config = {
                "extraction_type": "detector_metrics",
                "model_path": result.model_path,
                "wavelengths_nm": case_config.get("wavelengths_nm", [400, 500, 600, 700, 800]),
                "optical_power_W": 0.001,
                "device_area_m2": 1e-6,
                "dark_current_density_A_per_m2": case_config.get("dark_current_density_A_per_m2", 1.0),
                "output_dir": str(case_dir / "metrics"),
            }
            with open(extract_config_path, "w", encoding="utf-8") as f:
                json.dump(extract_config, f, indent=2, ensure_ascii=False)
            
            extract_cmd = [
                sys.executable, str(extract_script),
                "--model", result.model_path,
                "--config", str(extract_config_path),
            ]
            
            extract_proc = subprocess.run(
                extract_cmd,
                capture_output=True,
                text=True,
                cwd=str(SKILL_DIR),
                env=env,
                check=False,
            )
            
            try:
                extract_output = json.loads(extract_proc.stdout.strip().splitlines()[-1]) if extract_proc.stdout.strip() else {}
                result.metrics = extract_output
            except json.JSONDecodeError:
                result.metrics = {"raw_extract_stdout": extract_proc.stdout.strip()[-500:]}
            
            # 保存 metrics 到文件以便断点续跑读取
            with open(case_dir / "metrics.json", "w", encoding="utf-8") as f:
                json.dump(result.metrics, f, indent=2, ensure_ascii=False)
        
        result.status = "ok"
        
        # 标记完成
        done_marker.write_text(time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")
        
    except Exception as exc:
        result.status = "exception"
        result.error_message = f"{type(exc).__name__}: {str(exc)}"
    
    result.elapsed_sec = round(time.time() - t0, 2)
    return result


# ── summary / plotting ─────────────────────────────────────────

def write_summary_csv(results: list[SweepResult], output_dir: Path) -> None:
    """将所有结果写入 summary.csv。"""
    
    summary_path = output_dir / "summary.csv"
    
    # 收集所有参数字段和指标字段
    param_keys = set()
    metric_keys = set()
    for r in results:
        param_keys.update(r.params.keys())
        if isinstance(r.metrics, dict):
            metric_keys.update(k for k in r.metrics.keys() if not isinstance(r.metrics[k], (dict, list)))
    
    param_keys = sorted(param_keys)
    metric_keys = sorted(metric_keys)
    
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["case_id", "status", "elapsed_sec"] + param_keys + metric_keys
        writer.writerow(header)
        
        for r in results:
            row = [r.case_id, r.status, r.elapsed_sec]
            row += [r.params.get(k, "") for k in param_keys]
            if isinstance(r.metrics, dict):
                row += [r.metrics.get(k, "") for k in metric_keys]
            else:
                row += [""] * len(metric_keys)
            writer.writerow(row)
    
    print(f"Summary CSV written: {summary_path}")


def generate_summary_plots(results: list[SweepResult], output_dir: Path) -> None:
    """尝试生成汇总对比图（需要 matplotlib）。"""
    
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("[WARN] matplotlib not available, skipping summary plots.")
        return
    
    # 只取成功的 case
    ok_results = [r for r in results if r.status == "ok"]
    if not ok_results:
        return
    
    # 判断是单参数还是双参数扫描
    param_names = list(ok_results[0].params.keys())
    
    if len(param_names) == 1:
        # 单参数：横轴为参数，纵轴为关键指标
        p_name = param_names[0]
        x_vals = [r.params[p_name] for r in ok_results]
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f"Parameter Sweep: {p_name}")
        
        # 提取指标（假设 metrics 中有能用的标量值）
        def _get_scalar(metrics, key, default=None):
            if not isinstance(metrics, dict):
                return default
            val = metrics.get(key)
            if isinstance(val, (int, float)):
                return val
            return default
        
        # Plot placeholders — 实际字段取决于 extract_detector_metrics.py 的输出结构
        # 这里画出 case_id vs 时间作为示例，后续可根据实际 metrics 字段定制
        
        axes[0, 0].plot(x_vals, [r.elapsed_sec for r in ok_results], "o-")
        axes[0, 0].set_xlabel(p_name)
        axes[0, 0].set_ylabel("Elapsed Time (s)")
        axes[0, 0].set_title("Simulation Time")
        axes[0, 0].grid(True)
        
        axes[0, 1].axis("off")
        axes[1, 0].axis("off")
        axes[1, 1].axis("off")
        
        fig.tight_layout()
        fig.savefig(output_dir / "summary_plot.png", dpi=200)
        plt.close(fig)
        print(f"Summary plot saved: {output_dir / 'summary_plot.png'}")
    
    elif len(param_names) == 2:
        # 双参数：热力图
        p0, p1 = param_names
        # 构造 2D 网格
        x_vals = sorted(set(r.params[p0] for r in ok_results))
        y_vals = sorted(set(r.params[p1] for r in ok_results))
        
        fig, ax = plt.subplots(figsize=(8, 6))
        # 占位热力图
        Z = np.zeros((len(y_vals), len(x_vals)))
        for i, y in enumerate(y_vals):
            for j, x in enumerate(x_vals):
                for r in ok_results:
                    if r.params[p0] == x and r.params[p1] == y:
                        Z[i, j] = r.elapsed_sec
                        break
        
        im = ax.imshow(Z, aspect="auto", origin="lower", cmap="viridis")
        ax.set_xticks(range(len(x_vals)))
        ax.set_xticklabels([f"{v:.2e}" for v in x_vals], rotation=45, ha="right")
        ax.set_yticks(range(len(y_vals)))
        ax.set_yticklabels([f"{v:.2e}" for v in y_vals])
        ax.set_xlabel(p0)
        ax.set_ylabel(p1)
        ax.set_title("Simulation Time Heatmap")
        plt.colorbar(im, ax=ax, label="Elapsed (s)")
        fig.tight_layout()
        fig.savefig(output_dir / "summary_heatmap.png", dpi=200)
        plt.close(fig)
        print(f"Summary heatmap saved: {output_dir / 'summary_heatmap.png'}")


# ── main ───────────────────────────────────────────────────────

def run_parameter_sweep(sweep_cfg: SweepConfig) -> dict:
    """主入口：调度所有工况。"""
    
    output_dir = Path(sweep_cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成参数组合
    combos = generate_all_combinations(sweep_cfg.sweep_parameters)
    total = len(combos)
    print(f"[Sweep] Total cases to run: {total}")
    if total == 0:
        return {"status": "error", "message": "No parameter combinations generated."}
    
    # 保存 sweep 配置
    with open(output_dir / "sweep_config.json", "w", encoding="utf-8") as f:
        dump = {
            "simulation_type": sweep_cfg.simulation_type,
            "parallel": sweep_cfg.parallel,
            "max_workers": sweep_cfg.max_workers,
            "output_dir": sweep_cfg.output_dir,
            "resume": sweep_cfg.resume,
            "extract_metrics": sweep_cfg.extract_metrics,
            "sweep_parameters": sweep_cfg.sweep_parameters,
            "total_cases": total,
        }
        json.dump(dump, f, indent=2, ensure_ascii=False)
    
    results: list[SweepResult] = []
    
    if sweep_cfg.parallel and sweep_cfg.max_workers > 1:
        # 并行运行
        with ProcessPoolExecutor(max_workers=sweep_cfg.max_workers) as executor:
            futures = {
                executor.submit(run_single_case, cid, params, sweep_cfg): cid
                for cid, params in combos
            }
            for future in as_completed(futures):
                cid = futures[future]
                try:
                    res = future.result()
                    results.append(res)
                    print(f"[Case {cid:04d}] {res.status} ({res.elapsed_sec:.1f}s)")
                except Exception as exc:
                    print(f"[Case {cid:04d}] EXCEPTION: {exc}")
                    results.append(SweepResult(
                        case_id=cid,
                        params=combos[cid][1],
                        status="executor_exception",
                        error_message=str(exc),
                    ))
    else:
        # 串行运行
        for idx, (cid, params) in enumerate(combos):
            res = run_single_case(cid, params, sweep_cfg)
            results.append(res)
            tag = "OK" if res.status == "ok" else f"ERR {res.status}"
            print(f"[{idx+1}/{total}] Case {cid:04d} {tag} ({res.elapsed_sec:.1f}s)")
    
    # 排序保证顺序
    results.sort(key=lambda r: r.case_id)
    
    # 写 summary CSV
    write_summary_csv(results, output_dir)
    
    # 写 summary JSON
    summary_json = [asdict(r) for r in results]
    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_json, f, indent=2, ensure_ascii=False)
    
    # 汇总图
    if sweep_cfg.generate_summary_plots:
        generate_summary_plots(results, output_dir)
    
    ok_count = sum(1 for r in results if r.status == "ok")
    skip_count = sum(1 for r in results if r.status == "skipped")
    err_count = total - ok_count - skip_count
    
    print(f"\n[Sweep Done] OK={ok_count}, Skipped={skip_count}, Error={err_count}/{total}")
    
    return {
        "status": "ok",
        "total_cases": total,
        "ok": ok_count,
        "skipped": skip_count,
        "error": err_count,
        "output_dir": str(output_dir),
        "summary_csv": str(output_dir / "summary.csv"),
        "summary_json": str(output_dir / "summary.json"),
    }


def parse_sweep_config(config_path: str) -> SweepConfig:
    """从 JSON 解析扫描配置。"""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    return SweepConfig(
        base_config=raw["base_config"],
        simulation_type=raw.get("simulation_type", "optoelectronic"),
        sweep_parameters=raw.get("sweep_parameters", []),
        parallel=raw.get("parallel", False),
        max_workers=raw.get("max_workers", 1),
        output_dir=raw.get("output_dir", "output/sweep"),
        resume=raw.get("resume", True),
        extract_metrics=raw.get("extract_metrics", True),
        generate_summary_plots=raw.get("generate_summary_plots", True),
        verbose=raw.get("verbose", True),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="COMSOL parameter sweep batch simulation")
    parser.add_argument("--config", required=True, help="Path to sweep config JSON")
    args = parser.parse_args()
    
    sweep_cfg = parse_sweep_config(args.config)
    result = run_parameter_sweep(sweep_cfg)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


