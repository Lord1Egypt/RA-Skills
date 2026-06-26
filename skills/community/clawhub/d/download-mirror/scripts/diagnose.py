#!/usr/bin/env python3
"""
mirror-download diagnose.py
自动检测网络连通性，并为 HuggingFace/GitHub 下载任务推荐最佳镜像方案
用法: python3 diagnose.py "<模型ID或仓库URL>"
"""

import subprocess
import sys
import time
import re

# ============================================================
# 连通性检测
# ============================================================

SOURCES = {
    "huggingface_co":   {"name": "HuggingFace 原站", "host": "huggingface.co"},
    "hf_mirror":        {"name": "hf-mirror",        "host": "hf-mirror.com"},
    "modelscope":       {"name": "魔搭社区",           "host": "modelscope.cn"},
    "github":           {"name": "GitHub 原站",        "host": "github.com"},
    "gitcode":          {"name": "GitCode 镜像",       "host": "gitcode.com"},
    "ghfast":           {"name": "ghfast.top 代理",    "host": "ghfast.top"},
}


def check_host(host: str, timeout: int = 4) -> tuple[bool, float]:
    """检测 host 是否可达，返回 (是否可达, 耗时秒)"""
    try:
        start = time.time()
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--connect-timeout", "3", "--max-time", str(timeout),
             f"https://{host}"],
            capture_output=True, text=True, timeout=timeout + 1
        )
        elapsed = time.time() - start
        ok = r.stdout.strip() not in ["000", ""]
        return ok, elapsed
    except Exception:
        return False, timeout


def detect_all() -> dict:
    """并行检测所有源（串行模拟）"""
    results = {}
    for key, info in SOURCES.items():
        ok, elapsed = check_host(info["host"])
        results[key] = {"ok": ok, "elapsed": elapsed, **info}
    return results


# ============================================================
# 模型 ID 解析
# ============================================================

# HuggingFace -> ModelScope 常用映射
HF_TO_MS_MAP = {
    # Qwen 系列
    "Qwen":         lambda name: f"qwen/{name.split('/')[-1]}",
    # ZhipuAI 系列
    "THUDM":        lambda name: f"ZhipuAI/{name.split('/')[-1].replace('chatglm', 'chatglm')}",
    # DeepSeek 系列
    "deepseek-ai":  lambda name: f"deepseek-ai/{name.split('/')[-1]}",
    # Meta LLaMA
    "meta-llama":   lambda name: f"LLM-Research/{name.split('/')[-1]}",
    # Mistral
    "mistralai":    lambda name: f"LLM-Research/{name.split('/')[-1]}",
    # Google BERT/T5
    "google":       lambda name: f"google/{name.split('/')[-1]}",
    # Microsoft
    "microsoft":    lambda name: f"LLM-Research/{name.split('/')[-1]}",
    # Baichuan
    "baichuan-inc": lambda name: f"baichuan-inc/{name.split('/')[-1]}",
    # 01-ai (Yi)
    "01-ai":        lambda name: f"01ai/{name.split('/')[-1]}",
    # InternLM
    "internlm":     lambda name: f"Shanghai_AI_Laboratory/{name.split('/')[-1]}",
}

def hf_to_modelscope_id(hf_id: str) -> str | None:
    """尝试将 HuggingFace 模型ID转换为 ModelScope 模型ID"""
    if "/" not in hf_id:
        return None
    owner = hf_id.split("/")[0]
    if owner in HF_TO_MS_MAP:
        return HF_TO_MS_MAP[owner](hf_id)
    # 默认：保持原样尝试
    return hf_id


def classify_target(target: str) -> str:
    """判断目标类型"""
    if "github.com" in target or target.endswith(".git"):
        return "github_repo"
    if "huggingface.co" in target:
        return "hf_model"
    if "/" in target and not target.startswith("http"):
        # owner/model 格式
        return "hf_model"
    return "unknown"


# ============================================================
# 推荐方案生成
# ============================================================

def recommend_hf(target: str, results: dict) -> None:
    """为 HuggingFace 下载生成推荐方案"""
    # 清理 URL，提取模型ID
    model_id = re.sub(r'https?://huggingface\.co/', '', target).strip('/')

    print(f"\n📦 目标模型: {model_id}")
    print("=" * 60)

    if results["huggingface_co"]["ok"]:
        print("\n✅ 方案 1 (推荐): HuggingFace 原站可达，直接下载")
        print(f"""
  pip install huggingface_hub -q
  huggingface-cli download {model_id} --local-dir ./model
""")
    
    if results["hf_mirror"]["ok"]:
        print("\n✅ 方案 2: hf-mirror 镜像下载")
        print(f"""
  # 方式A: 命令行
  HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \\
      {model_id} --local-dir ./model --local-dir-use-symlinks False

  # 方式B: Python
  import os; os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
  from huggingface_hub import snapshot_download
  snapshot_download(repo_id='{model_id}', local_dir='./model')
""")

    ms_id = hf_to_modelscope_id(model_id)
    if results["modelscope"]["ok"] and ms_id:
        print(f"\n✅ 方案 3: 魔搭社区下载 (ModelScope ID: {ms_id})")
        print(f"""
  pip install modelscope -q
  from modelscope import snapshot_download
  snapshot_download(model_id='{ms_id}', cache_dir='./model')
""")
    elif results["modelscope"]["ok"]:
        print(f"\n⚠️  魔搭社区可达，但未找到 {model_id} 的对应 ID")
        print(f"    请手动在 https://modelscope.cn 搜索对应模型")

    if not any([results["huggingface_co"]["ok"], results["hf_mirror"]["ok"], 
                (results["modelscope"]["ok"] and ms_id)]):
        print("\n❌ 所有下载源均不可达，建议:")
        print("   1. 检查网络连接和代理设置")
        print("   2. 设置 HTTP_PROXY / HTTPS_PROXY 环境变量")
        print("   3. 稍后重试")


def recommend_github(target: str, results: dict) -> None:
    """为 GitHub 仓库下载生成推荐方案"""
    # 提取 owner/repo
    repo = re.sub(r'https?://github\.com/', '', target).rstrip('/')
    if repo.endswith('.git'):
        repo = repo[:-4]

    print(f"\n📁 目标仓库: {repo}")
    print("=" * 60)

    if results["github"]["ok"]:
        print("\n✅ 方案 1 (推荐): GitHub 原站可达，直接 clone")
        print(f"""
  git clone https://github.com/{repo}.git
""")

    if results["gitcode"]["ok"]:
        print("\n✅ 方案 2: GitCode 镜像")
        print(f"""
  git clone https://gitcode.com/mirrors/{repo}.git
""")

    if results["ghfast"]["ok"]:
        print("\n✅ 方案 3: ghfast.top 代理加速")
        print(f"""
  git clone https://ghfast.top/https://github.com/{repo}.git

  # 只下载代码包（不含 git 历史，更快）
  wget "https://ghfast.top/https://github.com/{repo}/archive/refs/heads/main.tar.gz" \\
       -O {repo.split('/')[-1]}.tar.gz
""")

    if not any([results["github"]["ok"], results["gitcode"]["ok"], results["ghfast"]["ok"]]):
        print("\n❌ 所有 GitHub 源均不可达，建议:")
        print("   1. 检查代理设置: git config --global http.proxy http://127.0.0.1:7890")
        print("   2. 尝试设置 SSH 下载: git clone git@github.com:{repo}.git")
        print("   3. 稍后重试")


# ============================================================
# 主函数
# ============================================================

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else ""
    
    print("🔍 正在检测各下载源连通性...")
    results = detect_all()
    
    print("\n=== 连通性结果 ===")
    for key, info in results.items():
        status = f"✓ {info['elapsed']:.1f}s" if info["ok"] else "✗ 不可达"
        print(f"  {info['name']:18s}: {status}")

    if not target:
        print("\n💡 用法: python3 diagnose.py '<模型ID或GitHub仓库URL>'")
        print("   示例: python3 diagnose.py 'Qwen/Qwen2-7B-Instruct'")
        print("   示例: python3 diagnose.py 'https://github.com/huggingface/transformers'")
        return

    target_type = classify_target(target)
    
    print(f"\n🎯 目标类型: {'HuggingFace 模型/数据集' if target_type == 'hf_model' else 'GitHub 仓库'}")
    
    if target_type == "hf_model":
        recommend_hf(target, results)
    elif target_type == "github_repo":
        recommend_github(target, results)
    else:
        print(f"\n⚠️  无法识别目标类型，请手动指定完整 URL")
        recommend_hf(target, results)
        recommend_github(target, results)


if __name__ == "__main__":
    main()
