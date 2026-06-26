#!/usr/bin/env python3
"""
run_all.py — 采集编排器：生成所有 JS → 合并 → 输出完整提取脚本

agent 使用方式:
  1. python3 run_all.py generate    → 输出合并后的 JS 代码
  2. agent 调用 browser act(kind="evaluate", fn=js_code)
  3. python3 run_all.py parse '<result_json>'  → 解析+校验+自愈报告

模块导入使用:
  from scripts.run_all import generate, parse
  js = generate()
  result = parse(json_str)

兼容环境:
  - OpenClaw Agent Framework
  - Claude Code
  - Jupyter Notebook
  - 命令行
"""

import sys
import json
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 各 gen 脚本输出的是 JS body 片段（不含 IIFE 包裹）
# gen_product.py 已改为 body-only 输出，此处统一拼接
GEN_SCRIPTS = [
    "gen_product.py",   # 产品基础字段
    "gen_spirit.py",    # 卖家精灵
    "gen_sif.py",       # SIF 插件
    "gen_variants.py",  # 变体
    "gen_bsr.py",       # BSR 排名
]


def _run_gen_script(script_name: str) -> str:
    """运行单个 gen 脚本，返回其标准输出"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        return ""
    r = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        raise RuntimeError(f"{script_name} 执行失败: {r.stderr.strip()}")
    return r.stdout.strip()


def generate() -> str:
    """合并所有 gen_*.py 生成的 JS body 为一个 evaluate 调用
    
    返回:
        str: 完整的 IIFE 格式 JS 代码，可直接用于 browser.evaluate
    
    示例:
        >>> js = generate()
        >>> # 在浏览器中执行: browser.evaluate(fn=js)
    """
    body_parts = []

    for script_name in GEN_SCRIPTS:
        output = _run_gen_script(script_name)
        if output:
            body_parts.append(output)

    merged_body = "\n\n".join(body_parts)
    js = f"""(() => {{
  const r = {{}};
{merged_body}
  return JSON.stringify(r, null, 1);
}})()"""
    return js


def _run_script(script_name: str, args: list = None) -> str:
    """运行指定脚本，检查 returncode，失败则抛出 RuntimeError"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{script_name} 执行失败: {r.stderr.strip() or '未知错误'}")
    return r.stdout.strip()


def parse(result_json: str) -> dict:
    """解析 evaluate 返回结果 + 正则提取插件子字段 + 校验
    
    参数:
        result_json: browser.evaluate 返回的 JSON 字符串
        
    返回:
        dict: 包含 data(解析后数据), validation(校验结果), healing(自愈信息)
        
    示例:
        >>> result = parse('{"asin":"B0123456789", ...}')
        >>> print(result['data'])
        
    条件:
        - 所有子进程调用均检查 returncode，失败时返回 error 而非静默忽略
    """
    try:
        json.loads(result_json)
    except json.JSONDecodeError:
        return {
            "data": {},
            "validation": {"valid": False, "error": "Invalid JSON input"},
            "healing": None
        }

    try:
        r_out = _run_script("parse_raw.py", ["all", result_json])
        parsed = json.loads(r_out)
    except (RuntimeError, json.JSONDecodeError) as e:
        return {
            "data": {},
            "validation": {"valid": False, "error": f"parse_raw 失败: {str(e)}"},
            "healing": None
        }

    try:
        r_out = _run_script("validate.py", [json.dumps(parsed)])
        first_line = r_out.split("\n")[0]
        validation = json.loads(first_line)
    except (RuntimeError, json.JSONDecodeError, IndexError) as e:
        validation = {"valid": False, "error": f"validate 失败: {str(e)}"}

    healing = None
    if validation.get("missing"):
        try:
            r_out = _run_script("healer.py", ["diagnose", json.dumps(validation["missing"])])
            healing = {
                "diagnose_js": r_out,
                "missing_fields": validation["missing"],
                "message": f"缺失 {len(validation['missing'])} 个字段，可执行 diagnose_js 诊断"
            }
        except RuntimeError:
            healing = {
                "diagnose_js": "",
                "missing_fields": validation["missing"],
                "message": f"缺失 {len(validation['missing'])} 个字段，但 healer 诊断失败"
            }

    return {
        "data": parsed,
        "validation": validation,
        "healing": healing,
    }


def main():
    """命令行入口函数"""
    if len(sys.argv) < 2:
        print("""用法:
python3 run_all.py generate                     # 生成合并 JS
python3 run_all.py parse '<evaluate_result>'    # 解析结果
python3 run_all.py help                         # 显示帮助

示例:
  # 生成提取JS
  python3 run_all.py generate > extract.js
  
  # 解析浏览器返回的结果
  python3 run_all.py parse '{"asin":"B0123456789"}'
""")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "generate":
        js = generate()
        print(js)
    elif mode == "parse":
        if len(sys.argv) < 3:
            print("错误: 需要提供 JSON 字符串参数")
            sys.exit(1)
        result_json = sys.argv[2]
        output = parse(result_json)
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif mode == "help":
        print(__doc__)
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
