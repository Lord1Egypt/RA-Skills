#!/usr/bin/env python3
"""
box-kvcache: 本地 LLM 环境检测工具
检测 Ollama / llama.cpp 是否安装，以及当前显存/内存占用
"""

import sys
import os
import subprocess
import json
import argparse
from pathlib import Path


def run_cmd(cmd, timeout=5):
    """执行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1


def check_ollama():
    """检测 Ollama 是否安装"""
    print("[1/4] 检测 Ollama...")
    output, code = run_cmd("ollama --version")
    if code == 0:
        print(f"  ✅ Ollama 已安装: {output}")
        
        # 获取运行中的模型
        models_out, _ = run_cmd("ollama list")
        print(f"  已下载模型:\n{models_out}")
        
        # 检查Ollama服务状态
        ps_out, _ = run_cmd("tasklist | findstr ollama")
        if "ollama" in ps_out.lower():
            print("  ✅ Ollama 服务正在运行")
        else:
            print("  ⚠️  Ollama 服务未运行")
        return True
    else:
        print("  ❌ Ollama 未安装")
        return False


def check_llama_cpp():
    """检测 llama.cpp 是否安装"""
    print("\n[2/4] 检测 llama.cpp...")
    
    # 检查常见路径
    possible_paths = [
        "llama-cli",
        "build\\bin\\Release\\llama-cli.exe",
        "C:\\llama.cpp\\build\\bin\\Release\\llama-cli.exe",
        os.path.expanduser("~\\llama.cpp\\build\\bin\\Release\\llama-cli.exe")
    ]
    
    for path in possible_paths:
        output, code = run_cmd(f'where "{path}"' if ":" in path else f'where {path}')
        if code == 0:
            print(f"  ✅ llama.cpp 已安装: {output}")
            return True
    
    # 检查Python包
    output, code = run_cmd("pip show llama-cpp-python")
    if code == 0:
        print(f"  ✅ llama-cpp-python 已安装")
        print(f"  {output}")
        return True
    
    print("  ❌ llama.cpp 未安装")
    return False


def check_hardware():
    """检测硬件信息"""
    print("\n[3/4] 检测硬件...")
    
    # GPU 信息
    gpu_info, _ = run_cmd('nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>nul')
    if gpu_info and "nvidia" not in gpu_info.lower():
        print(f"  ✅ NVIDIA GPU: {gpu_info}")
    else:
        # Windows: 用 PowerShell 获取显卡信息
        ps_cmd = 'Get-WmiObject Win32_VideoController | Select-Object Name,AdapterRAM | Format-List'
        adapter_out, _ = run_cmd(f'powershell -Command "{ps_cmd}"')
        if adapter_out:
            print(f"  🖥️  显卡信息:\n{adapter_out}")
        else:
            print("  ⚠️  无法获取GPU信息")
    
    # 内存信息
    mem_cmd = 'systeminfo | findstr "Memory"'
    mem_out, _ = run_cmd(mem_cmd)
    if mem_out:
        print(f"  💾 {mem_out}")


def estimate_kv_cache(model_name="llama3", context_len=4096, hidden_dim=4096, layers=32):
    """
    估算 KV Cache 显存占用
    
    公式:
    KV Cache per layer = 2 * seq_len * hidden_dim * bytes_per_param
    Total = layers * 2 * seq_len * hidden_dim * 2 (K + V) * 2 (float16 = 2 bytes)
    
    简化: 2 * layers * seq_len * hidden_dim * 2 bytes
    """
    print("\n[4/4] KV Cache 显存估算...")
    
    # 假设 float16 (2 bytes)
    bytes_per_param = 2
    
    # K + V 两个矩阵
    kv_params = 2
    
    # 计算
    cache_params = kv_params * layers * context_len * hidden_dim * bytes_per_param
    cache_gb = cache_params / (1024 ** 3)
    
    print(f"  模型: {model_name}")
    print(f"  隐藏层维度: {hidden_dim}")
    print(f"  层数: {layers}")
    print(f"  上下文长度: {context_len}")
    print(f"  ─────────────────────")
    print(f"  KV Cache 占用: {cache_gb:.2f} GB")
    
    # 量化后 (INT8 = 1 byte, 压缩率 ~2x)
    cache_int8_gb = cache_gb / 2
    print(f"  INT8 量化后: {cache_int8_gb:.2f} GB (省约 {cache_gb - cache_int8_gb:.2f} GB)")
    
    # 低秩压缩 (压缩率 ~4x)
    cache_lowrank_gb = cache_gb / 4
    print(f"  低秩压缩后: {cache_lowrank_gb:.2f} GB (省约 {cache_gb - cache_lowrank_gb:.2f} GB)")
    
    return {
        "float16_gb": cache_gb,
        "int8_gb": cache_int8_gb,
        "lowrank_gb": cache_lowrank_gb
    }


def main():
    parser = argparse.ArgumentParser(description="box-kvcache 环境检测")
    parser.add_argument("--model", default="llama3", help="模型名称")
    parser.add_argument("--context", type=int, default=4096, help="上下文长度")
    parser.add_argument("--verbose", action="store_true", help="详细模式")
    parser.add_argument("--estimate-only", action="store_true", help="仅估算，不检测环境")
    args = parser.parse_args()
    
    print("=" * 50)
    print("box-kvcache 本地 LLM 环境检测")
    print("=" * 50)
    
    if args.estimate_only:
        estimate_kv_cache(args.model, args.context)
        return
    
    check_ollama()
    check_llama_cpp()
    check_hardware()
    estimate_kv_cache(args.model, args.context)
    
    print("\n" + "=" * 50)
    print("检测完成！")
    print("=" * 50)
    
    if args.verbose:
        print("""
下一步:
  1. 安装 Ollama: https://ollama.com
  2. 下载模型: ollama pull llama3
  3. 使用压缩启动: python scripts/launch_compressed.py --model llama3 --compress
        """)


if __name__ == "__main__":
    main()
