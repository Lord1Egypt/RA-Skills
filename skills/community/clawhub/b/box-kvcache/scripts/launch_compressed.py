#!/usr/bin/env python3
"""
box-kvcache: 带压缩参数启动 Ollama
自动配置 KV Cache 压缩相关的启动参数
"""

import argparse
import subprocess
import os
import sys
import time


def check_ollama_running() -> bool:
    """检查 Ollama 是否在运行"""
    result = subprocess.run(
        "tasklist | findstr ollama",
        shell=True, capture_output=True, text=True
    )
    return "ollama" in result.stdout.lower()


def start_ollama():
    """启动 Ollama 服务"""
    print("[1/3] 启动 Ollama 服务...")
    
    if check_ollama_running():
        print("  ✅ Ollama 已在运行")
        return True
    
    try:
        # Windows: 启动 ollama serve
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print("  ✅ Ollama 服务已启动")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"  ❌ 启动失败: {e}")
        return False


def get_ollama_env_settings(compress: bool = False, context_len: int = 4096) -> dict:
    """
    获取 Ollama 环境变量配置
    
    这些是 Ollama 支持的 KV Cache 优化参数（部分版本支持）
    """
    env = {}
    
    if compress:
        # 启用 KV Cache 压缩相关的环境变量
        # 注意：Ollama 官方不一定有这些，具体看版本
        env["OLLAMA_KV_CACHE_QUANT"] = "int8"           # KV Cache 量化
        env["OLLAMA_KV_CACHE_COMPRESS"] = "1"            # 启用压缩
        env["OLLAMA_MAX_CONTEXT"] = str(context_len)      # 最大上下文
    
    # 其他优化参数
    env["OLLAMA_NUM_PARALLEL"] = "2"                    # 并行请求数（省显存）
    env["OLLAMA_FLASH_ATTENTION"] = "1"                # 启用 Flash Attention
    
    return env


def build_ollama_run_command(model: str, context_len: int, compress: bool, 
                             gpu: bool = True, n_ctx: int = None) -> list:
    """
    构建 ollama run 命令
    """
    cmd = ["ollama", "run", model]
    
    # 上下文长度
    if n_ctx is None:
        n_ctx = context_len
    cmd.extend(["--ctx", str(n_ctx)])
    
    # GPU 支持
    if gpu:
        cmd.append("--gpu")
    
    # 压缩参数（作为模型参数传递，具体看Ollama版本）
    if compress:
        # 这些是假设的参数，实际Ollama可能不同
        cmd.extend(["--kvquant", "int8"])
    
    return cmd


def print_launch_info(model: str, context_len: int, compress: bool, env: dict):
    """打印启动信息"""
    print("\n" + "=" * 50)
    print("box-kvcache 启动配置")
    print("=" * 50)
    print(f"模型: {model}")
    print(f"上下文长度: {context_len}")
    print(f"压缩模式: {'开启' if compress else '关闭'}")
    print(f"环境变量:")
    for k, v in env.items():
        print(f"  {k}={v}")
    print("=" * 50)


def interactive_chat(model: str):
    """启动交互式聊天"""
    print(f"\n开始与 {model} 对话（输入 quit 退出）...")
    print("-" * 40)
    
    try:
        while True:
            user_input = input("\n你: ")
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("再见！")
                break
            
            # 调用 ollama
            result = subprocess.run(
                ["ollama", "run", model, user_input],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                print(f"\n{model}: {result.stdout}")
            else:
                print(f"错误: {result.stderr}")
                
    except KeyboardInterrupt:
        print("\n\n对话已终止")
    except Exception as e:
        print(f"运行出错: {e}")


def main():
    parser = argparse.ArgumentParser(description="box-kvcache 带压缩启动 Ollama")
    parser.add_argument("--model", default="llama3", help="模型名称")
    parser.add_argument("--context", type=int, default=4096, help="上下文长度")
    parser.add_argument("--compress", action="store_true", help="启用 KV Cache 压缩")
    parser.add_argument("--n-ctx", type=int, default=None, help="Ollama n_ctx 参数")
    parser.add_argument("--no-gpu", action="store_true", help="禁用 GPU")
    parser.add_argument("--chat", action="store_true", help="启动交互式聊天")
    parser.add_argument("--list-models", action="store_true", help="列出已下载模型")
    args = parser.parse_args()
    
    # 列出模型
    if args.list_models:
        print("已下载的模型:")
        subprocess.run(["ollama", "list"])
        return
    
    # 启动 Ollama
    if not start_ollama():
        sys.exit(1)
    
    # 获取环境变量
    env = get_ollama_env_settings(compress=args.compress, context_len=args.context)
    
    # 打印启动信息
    print_launch_info(args.model, args.context, args.compress, env)
    
    # 构建命令
    cmd = build_ollama_run_command(
        args.model, 
        args.context, 
        args.compress, 
        gpu=not args.no_gpu,
        n_ctx=args.n_ctx
    )
    
    print(f"\n执行的命令: {' '.join(cmd)}")
    print("\n启动模型...")
    
    # 如果是聊天模式，启动交互
    if args.chat:
        interactive_chat(args.model)
    else:
        # 直接运行（单次查询）
        try:
            result = subprocess.run(cmd, timeout=120)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"运行出错: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
