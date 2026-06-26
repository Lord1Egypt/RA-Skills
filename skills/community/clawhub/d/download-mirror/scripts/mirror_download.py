#!/usr/bin/env python3
"""
mirror_download.py
一键镜像下载封装：自动检测连通性，选择最佳源下载 HuggingFace 模型或 GitHub 仓库。

用法（命令行）:
    python3 mirror_download.py Qwen/Qwen2-7B-Instruct --local-dir ./model
    python3 mirror_download.py https://github.com/owner/repo --local-dir ./repo

用法（Python 导入）:
    from mirror_download import auto_download
    auto_download("Qwen/Qwen2-7B-Instruct", local_dir="./model")
"""

import os
import re
import sys
import subprocess
import time
from pathlib import Path


# ============================================================
# 连通性检测（带缓存，避免重复检测消耗时间）
# ============================================================

_connectivity_cache: dict = {}
_cache_ttl = 60  # 缓存 60 秒内有效


def check_host(host: str, timeout: int = 4) -> bool:
    now = time.time()
    if host in _connectivity_cache:
        ok, ts = _connectivity_cache[host]
        if now - ts < _cache_ttl:
            return ok
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--connect-timeout", "3", "--max-time", str(timeout),
             f"https://{host}"],
            capture_output=True, text=True, timeout=timeout + 1
        )
        ok = r.stdout.strip() not in ["000", ""]
    except Exception:
        ok = False
    _connectivity_cache[host] = (ok, now)
    return ok


def best_hf_endpoint() -> str:
    """返回当前最佳的 HuggingFace 端点"""
    if check_host("huggingface.co"):
        return "https://huggingface.co"
    if check_host("hf-mirror.com"):
        return "https://hf-mirror.com"
    return None  # 两者都不可达


def best_ms_available() -> bool:
    """魔搭社区是否可达"""
    return check_host("modelscope.cn")


# ============================================================
# HuggingFace / hf-mirror 下载
# ============================================================

# HuggingFace -> ModelScope ID 映射
_OWNER_MAP = {
    "Qwen":         lambda n: f"qwen/{n.split('/')[-1]}",
    "THUDM":        lambda n: f"ZhipuAI/{n.split('/')[-1]}",
    "deepseek-ai":  lambda n: f"deepseek-ai/{n.split('/')[-1]}",
    "meta-llama":   lambda n: f"LLM-Research/{n.split('/')[-1]}",
    "mistralai":    lambda n: f"LLM-Research/{n.split('/')[-1]}",
    "google":       lambda n: f"google/{n.split('/')[-1]}",
    "microsoft":    lambda n: f"LLM-Research/{n.split('/')[-1]}",
    "baichuan-inc": lambda n: f"baichuan-inc/{n.split('/')[-1]}",
    "01-ai":        lambda n: f"01ai/{n.split('/')[-1]}",
    "internlm":     lambda n: f"Shanghai_AI_Laboratory/{n.split('/')[-1]}",
    "BAAI":         lambda n: f"BAAI/{n.split('/')[-1]}",
    "sentence-transformers": lambda n: f"sentence-transformers/{n.split('/')[-1]}",
}


def hf_id_to_ms(hf_id: str) -> str | None:
    if "/" not in hf_id:
        return None
    owner = hf_id.split("/")[0]
    fn = _OWNER_MAP.get(owner)
    return fn(hf_id) if fn else hf_id  # 未知 owner 原样尝试


def download_hf_model(
    model_id: str,
    local_dir: str = "./model",
    ignore_patterns: list = None,
    token: str = None,
    revision: str = None,
) -> str:
    """
    从 HuggingFace 或镜像下载模型/数据集。
    自动选择可用端点：原站 > hf-mirror > 魔搭社区。
    返回本地模型目录路径。
    """
    # 清理 URL 格式
    model_id = re.sub(r'https?://huggingface\.co/', '', model_id).strip('/')
    
    # 尝试安装依赖
    _ensure_package("huggingface_hub")

    endpoint = best_hf_endpoint()
    
    if endpoint:
        print(f"[mirror-download] 使用端点: {endpoint}")
        os.environ["HF_ENDPOINT"] = endpoint
        
        try:
            from huggingface_hub import snapshot_download
            kwargs = dict(
                repo_id=model_id,
                local_dir=local_dir,
                local_dir_use_symlinks=False,
            )
            if ignore_patterns:
                kwargs["ignore_patterns"] = ignore_patterns
            if token:
                kwargs["token"] = token
            if revision:
                kwargs["revision"] = revision
                
            path = snapshot_download(**kwargs)
            print(f"[mirror-download] ✓ 下载完成: {path}")
            return path
        except Exception as e:
            print(f"[mirror-download] HF 下载失败: {e}")
            print("[mirror-download] 尝试切换到魔搭社区...")
    
    # 回退到魔搭社区
    if best_ms_available():
        ms_id = hf_id_to_ms(model_id)
        if ms_id:
            return download_modelscope(ms_id, local_dir)
        else:
            raise RuntimeError(
                f"无法确定 {model_id} 在 ModelScope 的对应 ID，"
                f"请手动在 https://modelscope.cn 查找"
            )
    
    raise RuntimeError(
        "所有下载源均不可达。请检查网络连接，或设置代理后重试。\n"
        "提示: export HTTPS_PROXY=http://127.0.0.1:7890"
    )


# ============================================================
# 魔搭社区下载
# ============================================================

def download_modelscope(
    model_id: str,
    local_dir: str = "./model",
    revision: str = None,
) -> str:
    """从魔搭社区下载模型"""
    _ensure_package("modelscope")
    
    print(f"[mirror-download] 使用魔搭社区下载: {model_id}")
    
    from modelscope import snapshot_download as ms_download
    kwargs = dict(model_id=model_id, cache_dir=local_dir)
    if revision:
        kwargs["revision"] = revision
    
    path = ms_download(**kwargs)
    print(f"[mirror-download] ✓ 下载完成: {path}")
    return path


# ============================================================
# GitHub 仓库下载
# ============================================================

def download_github_repo(
    repo_url: str,
    local_dir: str = None,
    branch: str = "main",
    shallow: bool = True,
) -> str:
    """
    克隆 GitHub 仓库，自动选择可用镜像。
    repo_url: 完整URL如 https://github.com/owner/repo
              或短格式 owner/repo
    """
    # 标准化 URL
    if not repo_url.startswith("http"):
        repo_url = f"https://github.com/{repo_url}"
    
    # 提取 owner/repo
    match = re.search(r'github\.com/(.+?)(?:\.git)?$', repo_url)
    if not match:
        raise ValueError(f"无法解析 GitHub URL: {repo_url}")
    repo_path = match.group(1).rstrip('/')
    
    if local_dir is None:
        local_dir = repo_path.split('/')[-1]
    
    # 尝试各镜像
    candidates = []
    if check_host("github.com"):
        candidates.append(f"https://github.com/{repo_path}.git")
    if check_host("gitcode.com"):
        candidates.append(f"https://gitcode.com/mirrors/{repo_path}.git")
    if check_host("ghfast.top"):
        candidates.append(f"https://ghfast.top/https://github.com/{repo_path}.git")
    
    if not candidates:
        raise RuntimeError("所有 GitHub 镜像源均不可达，请检查网络。")
    
    for clone_url in candidates:
        print(f"[mirror-download] 尝试 clone: {clone_url}")
        cmd = ["git", "clone"]
        if shallow:
            cmd += ["--depth", "1"]
        cmd += ["-b", branch, clone_url, local_dir]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[mirror-download] ✓ Clone 完成: {local_dir}")
            return local_dir
        else:
            print(f"[mirror-download] 失败，尝试下一个源... ({result.stderr[:100]})")
    
    raise RuntimeError(f"所有镜像源均 clone 失败，请检查仓库名称: {repo_path}")


# ============================================================
# 统一入口
# ============================================================

def auto_download(target: str, local_dir: str = None, **kwargs) -> str:
    """
    智能下载入口：自动识别目标类型并选择最佳下载方案。
    
    target: HuggingFace 模型ID、HF URL 或 GitHub URL
    local_dir: 本地保存目录
    **kwargs: 传递给具体下载函数的额外参数
    """
    if "github.com" in target or (
        "/" in target and not target.startswith("http") and 
        not any(x in target for x in ["huggingface", "modelscope"])
        and len(target.split("/")) == 2
        and "." not in target.split("/")[0]  # owner 不含点，可能是 GitHub
    ):
        # 偏向 GitHub 格式检测
        if "github.com" in target:
            return download_github_repo(target, local_dir or "./repo", **kwargs)
    
    # 默认当作 HuggingFace 模型处理
    return download_hf_model(target, local_dir or "./model", **kwargs)


# ============================================================
# 工具函数
# ============================================================

def _ensure_package(package: str) -> None:
    """确保 Python 包已安装"""
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"[mirror-download] 正在安装 {package}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "-q"],
            check=True
        )


# ============================================================
# 命令行入口
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="镜像下载工具：自动选择可用源下载 HuggingFace 模型或 GitHub 仓库"
    )
    parser.add_argument("target", help="模型ID (如 Qwen/Qwen2-7B) 或仓库URL")
    parser.add_argument("--local-dir", default=None, help="本地保存目录")
    parser.add_argument("--token", default=None, help="HuggingFace Token（用于私有/门控模型）")
    parser.add_argument("--revision", default=None, help="指定版本/分支/tag")
    parser.add_argument("--no-safetensors-only", action="store_true",
                        help="不过滤，下载全部文件（默认跳过 .bin 权重文件）")
    parser.add_argument("--branch", default="main", help="GitHub 分支名（默认 main）")
    
    args = parser.parse_args()
    
    try:
        if "github.com" in args.target:
            result = download_github_repo(
                args.target,
                local_dir=args.local_dir,
                branch=args.branch,
            )
        else:
            ignore = None if args.no_safetensors_only else ["*.bin", "*.pt", "pytorch_model*"]
            result = download_hf_model(
                args.target,
                local_dir=args.local_dir or "./model",
                ignore_patterns=ignore,
                token=args.token,
                revision=args.revision,
            )
        print(f"\n✅ 完成！文件保存在: {result}")
    except Exception as e:
        print(f"\n❌ 下载失败: {e}", file=sys.stderr)
        sys.exit(1)
