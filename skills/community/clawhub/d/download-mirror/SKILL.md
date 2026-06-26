---
name: mirror-download
description: >
  当用户需要从 HuggingFace 或 GitHub 下载模型、数据集或代码仓库，且网络连接失败、超时或速度缓慢时，**立即启用此 skill**，自动切换到国内镜像站（hf-mirror、魔搭社区、GitCode 等）完成下载，避免无意义重试消耗大量 token。
  
  触发场景包括：
  - 用户提到"下载模型"、"clone 仓库"、"连不上 HuggingFace/GitHub"
  - 出现 ConnectionError、Timeout、SSLError、huggingface_hub 报错
  - 用户在中国大陆环境下载 AI 模型或数据集
  - 任何涉及 huggingface_hub、modelscope、git clone 的下载任务
  
  **不要反复重试原站**——第一次失败后立即切换镜像。
---

# Mirror Download Skill

## 核心原则

> **一次失败，立即切换**。不要重复 retry 原站，直接用镜像站完成任务。

---

## 第一步：快速连通性检测

在下载前，**先用一条命令**检测哪些源可用，最多等 4 秒：

```bash
python3 - << 'EOF'
import subprocess, time, sys

def ping(host, timeout=4):
    try:
        r = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
             '--connect-timeout', '3', '--max-time', str(timeout), f'https://{host}'],
            capture_output=True, text=True, timeout=timeout+1
        )
        ok = r.stdout.strip() not in ['000', '']
        return ok
    except:
        return False

sources = {
    'HuggingFace 原站': 'huggingface.co',
    'hf-mirror':        'hf-mirror.com',
    '魔搭社区':          'modelscope.cn',
    'GitHub 原站':       'github.com',
    'GitCode':          'gitcode.com',
}

print("=== 连通性检测 ===")
available = []
for name, host in sources.items():
    ok = ping(host)
    status = "✓ 可用" if ok else "✗ 不可达"
    print(f"  {name:12s} ({host}): {status}")
    if ok:
        available.append(name)

print(f"\n可用源: {', '.join(available) if available else '全部不可达'}")
EOF
```

根据检测结果，**选择第一个可用的镜像**进入对应下载流程。

---

## 第二步：HuggingFace 模型/数据集下载

### 方案 A：hf-mirror（推荐首选）

通过 `HF_ENDPOINT` 环境变量一键切换，无需修改任何代码：

```bash
# 方式1: 命令行临时切换（推荐）
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
    <模型ID> \
    --local-dir <本地目录> \
    --local-dir-use-symlinks False

# 方式2: Python 代码中切换
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='<模型ID>',          # 例如: "Qwen/Qwen2-7B-Instruct"
    local_dir='<本地目录>',
    ignore_patterns=['*.bin'],    # 可选: 跳过旧格式权重，只下载 safetensors
)
```

**安装 huggingface_hub（若未安装）：**
```bash
pip install huggingface_hub -q
```

---

### 方案 B：魔搭社区（ModelScope）

适合 Qwen、ChatGLM、通义系列等国产模型，命名与 HF 基本一致：

```bash
pip install modelscope -q
```

```python
from modelscope import snapshot_download

# 模型ID映射规则（见下方参考表）
model_dir = snapshot_download(
    model_id='<ModelScope模型ID>',  # 例如: "qwen/Qwen2-7B-Instruct"
    cache_dir='<本地目录>',
)
print(f"下载完成: {model_dir}")
```

**HuggingFace → ModelScope 常用映射：**

| HuggingFace ID | ModelScope ID | 说明 |
|---|---|---|
| `Qwen/Qwen2-7B-Instruct` | `qwen/Qwen2-7B-Instruct` | Qwen 系列完全一致 |
| `Qwen/Qwen2.5-7B-Instruct` | `qwen/Qwen2.5-7B-Instruct` | Qwen2.5 系列 |
| `THUDM/chatglm3-6b` | `ZhipuAI/chatglm3-6b` | owner 有变化 |
| `THUDM/glm-4-9b-chat` | `ZhipuAI/glm-4-9b-chat` | GLM4 系列 |
| `deepseek-ai/DeepSeek-V2-Chat` | `deepseek-ai/DeepSeek-V2-Chat` | DeepSeek 一致 |
| `meta-llama/Llama-3-8B-Instruct` | `LLM-Research/Meta-Llama-3-8B-Instruct` | Meta 系列 owner 变化 |
| `mistralai/Mistral-7B-Instruct-v0.3` | `LLM-Research/Mistral-7B-Instruct-v0.3` | Mistral 系列 |

> ⚠️ 若不确定 ModelScope ID，用 `search_modelscope` 脚本查找（见下方）

---

### 方案 C：手动 wget/aria2 直接下载（适合单文件）

```bash
# 使用 hf-mirror 直接下载单个文件
wget "https://hf-mirror.com/<owner>/<model>/resolve/main/<filename>" \
     -O <本地文件名>

# 使用 aria2c 多线程加速（推荐大文件）
aria2c -x 16 -s 16 \
    "https://hf-mirror.com/<owner>/<model>/resolve/main/model.safetensors" \
    -o model.safetensors
```

---

## 第三步：GitHub 仓库下载

### 方案 A：GitCode 镜像

```bash
# 将 github.com 替换为 gitcode.com
# 原始: git clone https://github.com/owner/repo.git
git clone https://gitcode.com/mirrors/owner/repo.git

# 或者设置代理（已有VPN/代理时）
git config --global http.proxy http://127.0.0.1:7890
git clone https://github.com/owner/repo.git
```

### 方案 B：加速下载（ghproxy）

```bash
# 使用 ghfast.top 代理（速度快）
git clone https://ghfast.top/https://github.com/owner/repo.git

# 下载 Release 文件
wget "https://ghfast.top/https://github.com/owner/repo/releases/download/v1.0/file.zip"
```

### 方案 C：仅下载 Release 压缩包（不 clone）

```bash
# 直接下载 tarball（避免 .git 历史，更快）
wget "https://ghfast.top/https://github.com/owner/repo/archive/refs/heads/main.tar.gz" \
     -O repo.tar.gz
tar xzf repo.tar.gz
```

---

## 快速诊断脚本

遇到下载报错时，运行此脚本自动诊断并给出推荐方案：

```bash
python3 /path/to/mirror-download/scripts/diagnose.py "<模型或仓库ID>"
```

参考 `scripts/diagnose.py` 和 `scripts/mirror_download.py`。

---

## 下载后验证

```python
# 验证模型文件完整性
import os, glob

def check_download(model_dir):
    files = glob.glob(f"{model_dir}/**", recursive=True)
    total_size = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
    print(f"文件数量: {len([f for f in files if os.path.isfile(f)])}")
    print(f"总大小: {total_size / 1024**3:.2f} GB")
    
    # 检查关键文件
    for name in ['config.json', 'tokenizer_config.json']:
        path = os.path.join(model_dir, name)
        print(f"{'✓' if os.path.exists(path) else '✗'} {name}")

check_download("<模型目录>")
```

---

## 决策流程

```
用户要下载模型/仓库
       │
       ▼
  运行连通性检测
       │
  ┌────┴────┐
  │         │
HF可达    HF不可达
  │         │
直接下载  ┌──┴──────────┐
       hf-mirror     魔搭社区
       可达?          可达?
         │              │
        用它           用它
                        │
                   两者都不可达
                        │
                  检查 GitHub/GitCode
                  或提示用户检查网络
```

---

## 常见报错 → 解决方案速查

| 报错信息 | 原因 | 解决 |
|---|---|---|
| `ConnectionError: HTTPSConnectionPool` | 原站不可达 | 切换 hf-mirror |
| `requests.exceptions.Timeout` | 超时 | 切换镜像，增加 `--timeout 120` |
| `OSError: We couldn't connect to...` | huggingface_hub 连不上 | 设置 `HF_ENDPOINT` |
| `SSL: CERTIFICATE_VERIFY_FAILED` | SSL 问题 | 加 `--no-check-certificate` 或更新证书 |
| `Repository not found` | 模型ID有误 | 查 ModelScope 搜索对应ID |
| `GatedRepo` / 需要登录 | 模型需授权 | 用 `--token <hf_token>` 或换用 ModelScope |
| `git: unable to connect` | GitHub 不可达 | 切换 GitCode 或 ghfast.top |

---

## 参考文件

- `scripts/diagnose.py` — 自动连通性检测 + 推荐下载方案
- `scripts/mirror_download.py` — 一键镜像下载封装函数
- `references/modelscope_id_map.md` — 详细的 HF→MS 模型ID映射表
