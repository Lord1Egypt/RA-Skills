# Audio Transcribe ZH — 中文音频转文字 Skill

快速部署**中文语音转文字**环境，基于 FunASR Paraformer 和阿里 ModelScope 国内镜像，**全程走国内源，无需科学上网**。

---

## 📋 适用场景

- 批量将中文音频/视频文件转录为文字
- 每个音频输出一个 `.txt` 文件（同目录）
- 视频文件自动提取音频后转录

---

## 🖥 推荐硬件配置

### 已验证的配置（当前机器）

| 组件 | 型号 / 规格 |
|:----|:-----------|
| **CPU** | Intel Core i7-12700KF (12核20线程, 3.6GHz) |
| **GPU** | NVIDIA RTX 4060 (8GB VRAM, CUDA 12.4) |
| **RAM** | 32GB |
| **OS** | Windows 10 64-bit |
| **Python** | 3.12+ (通过 uv 管理) |
| **磁盘** | NVMe SSD |

### 最低要求

| 配置 | CPU 方案 | GPU 方案 |
|:----|:--------|:--------|
| CPU | 4核 @ 2.0GHz 或更高 | 同左 |
| GPU | 不需要 | NVIDIA 6GB+ VRAM, CUDA 11.8+ |
| RAM | 4GB+ | 4GB+ |
| 磁盘空间 | 5GB+ | 5GB+ |
| 操作系统 | Linux / Windows / macOS | Linux / Windows |

---

## 🚀 快速部署

### 第 1 步：安装 uv（Python 包管理器）

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 第 2 步：创建虚拟环境并安装依赖

```bash
# 1. 创建 venv
uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate       # Windows

# 2. 安装 PyTorch + CUDA（NVIDIA GPU 方案）
#    国内加速：加清华镜像
uv pip install torch==2.5.1+cu124 torchvision==0.20.1+cu124 --index-url https://download.pytorch.org/whl/cu124 --extra-index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 3. 安装 FunASR（国内用 modelscope 源）
uv pip install funasr==1.3.1 --extra-index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 4. 安装 ffmpeg（Win 需要手动下载）
#    ↓ 见第 3 步

# --- 仅 CPU 方案（无 NVIDIA 显卡） ---
# 如果机器没有 NVIDIA GPU，装 CPU 版 PyTorch 即可：
# uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
# 后续在代码中设置 device='cpu'
```

### 第 3 步：安装 ffmpeg

```bash
# Windows：从 BtbN/FFmpeg-Builds 下载
# 国内加速：使用 gh-proxy.com
$url = "https://gh-proxy.com/https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\ffmpeg.zip"
Expand-Archive "$env:TEMP\ffmpeg.zip" -DestinationPath "$env:TEMP\ffmpeg"
# 然后解压后的 ffmpeg.exe 在 ffmpeg-master-latest-win64-gpl\bin\ 下
# 建议放到 C:\ffmpeg\ 并加入 PATH

# Linux (apt)
sudo apt install ffmpeg -y

# macOS (Homebrew)
brew install ffmpeg
```

验证：
```bash
ffmpeg -version | head -n 1
```

### 第 4 步：下载模型

Paraformer-large 模型约 **1.2GB**，首次运行时会自动下载缓存到：
- Windows: `%USERPROFILE%\.cache\modelscope\hub\models\iic\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch`
- Linux: `~/.cache/modelscope/hub/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch`
- macOS: `~/.cache/modelscope/hub/models/...`

也可以手动预下载：

```bash
# 方式一：用 Python 下载（推荐）
uv run python -c "
from modelscope import snapshot_download
snapshot_download('iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')
"

# 方式二：直接设置镜像环境变量（所有 HuggingFace/ModelScope 下载走国内）
# Windows PowerShell:
$env:MODELSCOPE_CACHE = "$env:USERPROFILE\.cache\modelscope"
# 或使用 modelscope 镜像：
$env:MODELSCOPE_MODE = "mirror"

# Linux:
export MODELSCOPE_CACHE=~/.cache/modelscope
```

**模型国内下载地址：**
```
官方源：  https://www.modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
HuggingFace镜像： https://hf-mirror.com/funasr/paraformer-large  （有的话优先 modelscope 源）
```

---

## ⚙️ 中文音频转文字脚本

### 单文件转录 `transcribe_one.py`

```python
"""
单文件转录脚本
用法：uv run python transcribe_one.py <音频文件路径>
"""
import sys, time, os
from funasr import AutoModel

def transcribe(audio_path, device='cuda'):
    """
    转录单个音频文件
    device: 'cuda' 或 'cpu'
    """
    model = AutoModel(
        model='iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        vad_model='iic/speech_fsmn_vad_zh-cn-16k-common-pytorch',
        punc_model='iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
        device=device,
        disable_update=True,   # 禁止自动更新
        disable_log=True,
    )
    result = model.generate(input=audio_path)
    text = result[0]['text'].strip()
    return text

if __name__ == '__main__':
    audio = sys.argv[1]
    t0 = time.time()
    text = transcribe(audio)
    elapsed = time.time() - t0
    print(f'[{elapsed:.2f}s] {text}')
```

### 视频批量转录 `batch_transcribe.py`

```python
"""
批量转录视频（自动提取音频 → 转录 → 保存 .txt）

用法：
  uv run python batch_transcribe.py E:\视频文件夹
  uv run python batch_transcribe.py E:\视频文件夹 --device=cpu

输出：每个视频同目录下生成同名 .txt 文件
"""
import sys, os, time, subprocess, argparse
from funasr import AutoModel

# ── 配置 ──────────────────────────────────────────────────
FFMPEG_PATH = r'C:\Users\PC\.openclaw\workspace\ffmpeg-bin\ffmpeg.exe'
TMP_AUDIO = os.path.join(os.path.dirname(__file__), 'audio_tmp.wav')
# ───────────────────────────────────────────────────────────

def extract_audio(video_path, output_wav):
    """用 ffmpeg 从视频中提取 16kHz WAV 音频"""
    cmd = [
        FFMPEG_PATH, '-y', '-loglevel', 'error', '-i', video_path,
        '-ar', '16000', '-ac', '1', '-sample_fmt', 's16',
        output_wav
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def main():
    parser = argparse.ArgumentParser(description='批量转录视频')
    parser.add_argument('root_dir', help='视频根目录（递归搜索所有 .mp4）')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'],
                        help='推理设备，默认 cuda')
    args = parser.parse_args()

    root = args.root_dir
    device = args.device

    # 加载模型
    print(f'[加载模型] device={device} ...')
    t0 = time.time()
    model = AutoModel(
        model='iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        vad_model='iic/speech_fsmn_vad_zh-cn-16k-common-pytorch',
        punc_model='iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
        device=device,
        disable_update=True,
        disable_log=True,
    )
    print(f'[模型已加载] 耗时 {time.time()-t0:.1f}s')

    # 扫描所有视频
    videos = []
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith('.mp4'):
                txt_dest = os.path.join(dirpath, f.replace('.mp4', '.txt'))
                if not os.path.exists(txt_dest):
                    videos.append(os.path.join(dirpath, f))
                else:
                    print(f'  ⏭ 跳过（已有txt）{f}')
    print(f'等待处理: {len(videos)} 个视频')
    if not videos:
        return

    ok, fail = 0, 0
    for i, vpath in enumerate(videos, 1):
        basename = os.path.basename(vpath)
        txt_dest = vpath.replace('.mp4', '.txt')
        print(f'[{i}/{len(videos)}] {basename[:40]}...', end=' ', flush=True)

        try:
            t1 = time.time()
            extract_audio(vpath, TMP_AUDIO)
            result = model.generate(input=TMP_AUDIO)
            text = result[0]['text'].strip()
            elapsed = time.time() - t1

            with open(txt_dest, 'w', encoding='utf-8') as f:
                f.write(text)
            ok += 1
            print(f'✅ {elapsed:.1f}s')
        except Exception as e:
            fail += 1
            print(f'❌ {e}')

    # 清理临时文件
    if os.path.exists(TMP_AUDIO):
        os.remove(TMP_AUDIO)

    print(f'\n===== 完成! ✅ {ok} 成功, ❌ {fail} 失败 =====')

if __name__ == '__main__':
    main()
```

---

## ⏱ 性能基准（46秒中文音频）

| 方案 | 设备 | 转录耗时 | 速度比 | 推荐场景 |
|:----|:----|:--------:|:-----:|:--------|
| **FunASR Paraformer** 🔥✅ | RTX 4060 | **0.58s** | 1x | 首选，中文最佳 |
| **FunASR Paraformer** ✅ | i7-12700KF CPU | **1.39s** | 2.4x | 无 GPU 时也够用 |
| **Whisper Small** | RTX 4060 | 3.7s | 6x | 英文/多语言备选 |
| **Whisper Medium** | RTX 4060 | 5.5s | 9x | 中文还行但慢 |
| **Whisper Large-v3** | RTX 4060 | 98.8s | 170x | ❌ 太慢，不推荐 |

**性价比结论：FunASR Paraformer 在 RTX 4060 上，中文转录比 Whisper Medium 快 9 倍，比 Whisper Large-v3 快 170 倍，而且中文准确率更高（自带标点）。**

---

## 📦 国内镜像速查表

| 资源 | 镜像地址 | 用途 |
|:----|:--------|:----|
| **PyTorch (CUDA)** | `https://download.pytorch.org/whl/cu124` | torch 主源 |
| **PyTorch (CPU)** | `https://download.pytorch.org/whl/cpu` | torch CPU 版 |
| **PyPI** | `https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple` | 通用 Python 包国内加速 |
| **ModelScope** | `https://www.modelscope.cn` | 模型国内主源（Paraformer等） |
| **HuggingFace 镜像** | `https://hf-mirror.com` | HuggingFace 模型国内备用镜像 |
| **GitHub 加速** | `https://gh-proxy.com/` | GitHub Release/代码下载代理 |
| **FFmpeg 下载** | `https://gh-proxy.com/https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip` | Windows ffmpeg |

### pip 永久配置国内镜像（可选）

```bash
# 设置清华 PyPI 镜像
uv pip config set index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

## ❓ 常见问题

### Q: OSError: [WinError 1114] DLL 加载失败
**原因**：PyTorch 版本与 CUDA 驱动不匹配。
**解决**：确保 CUDA 驱动 ≥ 12.4，装对应版本：
```bash
uv pip install torch==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124
```

### Q: 模型首次下载很慢
**原因**：从 HuggingFace 或 ModelScope 国外源下载。
**解决**：代码中已默认使用 `modelscope`（国内阿里源），无需科学上网。如果仍慢，设置：
```bash
$env:MODELSCOPE_MODE = "mirror"  # Windows PowerShell
export MODELSCOPE_MODE=mirror     # Linux
```

### Q: "嗯嗯嗯" 或 背景音乐干扰 导致转录质量差
**原因**：音频中有背景人声/音乐，Paraformer 会尝试转录所有声音。
**解决**：
- 优先使用 `Paraformer-large`（已用，抗干扰最强）
- 配合 VAD 模型（代码中已加 `vad_model`）过滤静音段
- 如果视频本身背景音过大，转录会包含杂音，属于正常现象

### Q: 批量处理时 CUDA out of memory
**原因**：模型一次处理多个音频时显存不够。
**解决**：一次处理一个文件（我们的批量脚本已逐个处理），或使用 CPU：
```bash
uv run python batch_transcribe.py E:\视频 --device=cpu
```

### Q: 输出文本没有标点
**原因**：未加载标点模型。
**解决**：脚本中已包含 `punc_model='iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch'`

---

## 🗑 清理缓存

```bash
# 模型缓存
rm -rf %USERPROFILE%\.cache\modelscope\hub     # Windows
rm -rf ~/.cache/modelscope/hub                  # Linux/macOS

# Whisper 缓存（如果安装了）
rm -rf %USERPROFILE%\.cache\whisper             # Windows
rm -rf ~/.cache/whisper                         # Linux/macOS
```

---

## 🔄 性能优化建议

1. **分块处理长音频**：>10分钟的音频自动分段（Paraformer 自带 VAD 分段）
2. **预处理降噪**：对背景噪音大的音频，可先过一遍降噪滤波器
3. **搭配 CPU 方案**：轻量任务用 CPU，批量任务用 GPU
4. **使用 ssd 存储**：ffmpeg 提取音频是 IO 密集型，SSD 比 HDD 快很多
