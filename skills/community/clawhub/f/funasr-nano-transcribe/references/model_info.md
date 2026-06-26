# Fun-ASR-Nano-2512 模型信息

## 模型规格

| 属性 | 规格 |
|------|------|
| 模型名称 | Fun-ASR-Nano-2512 |
| 模型类型 | FunASRNano (Custom Implementation) |
| 模型大小 | **~1.85GB** |
| 架构 | Audio Encoder + LLM (Qwen3-0.6B) |
| 训练框架 | FunASR |
| 支持语言 | 中文（主要）、英文 |

## 文件结构

```
models/Fun-ASR-Nano-2512/
├── config.yaml           # 模型配置
├── configuration.json    # 额外配置
├── model.pt             # 模型权重文件 (~1.5GB)
├── Qwen3-0.6B/          # LLM 模型文件
│   ├── config.json
│   ├── merges.txt
│   ├── tokenizer_config.json
│   └── vocab.json
├── example/             # 示例音频
├── tokens.json          # 词表文件
└── ...                  # 其他依赖文件
```

## 模型获取与分发

### 获取方式

| 方式 | 命令/路径 | 说明 |
|------|-----------|------|
| **技能已包含** | `models/Fun-ASR-Nano-2512/` | 推荐，开箱即用 |
| **ModelScope** | `modelscope download --model FunAudioLLM/Fun-ASR-Nano-2512` | 需网络 |
| **手动复制** | `cp -r /path/to/model models/` | 从其他位置复制 |

### 技能发布时的模型处理

由于模型文件较大（1.85GB），发布技能时可以考虑以下方案：

**方案一：包含完整模型（推荐）**
- 优点：用户开箱即用，无需额外下载
- 缺点：技能包体积大（1.85GB）
- 适用：内部使用、本地部署

**方案二：不包含模型，提供下载脚本**
- 优点：技能包体积小
- 缺点：用户首次使用需下载模型
- 适用：公开发布、网络环境良好

**方案三：提供模型压缩包下载链接**
- 优点：灵活分发
- 缺点：用户需手动下载解压
- 适用：大规模部署

### 模型验证

```bash
# 检查模型完整性
python scripts/download_model.py --check

# 查看模型详细信息
python scripts/download_model.py --info

# 验证文件大小
du -sh models/Fun-ASR-Nano-2512/
# 预期输出：约 1.9GB
```

## 加载方式

模型使用自定义加载方式：

```python
from funasr import AutoModel

model = AutoModel(
    model="models/Fun-ASR-Nano-2512",
    trust_remote_code=True,
    remote_code="./FunASRNano.py",
    device="cpu",  # 或 "cuda:0"
    disable_update=True,
)
```

## 性能指标

### 资源配置

| 配置 | 内存/显存占用 | 处理速度 |
|------|---------------|----------|
| CPU (4核) | ~2-3GB RAM | 2-3x 实时 |
| CUDA | ~2GB VRAM | 5-10x 实时 |

### 热词支持

预配置热词列表：
- 人名：吴晓阳
- 社保术语：统账结合、单建统筹
- 医疗术语：个账、异地、门特
- 保险术语：大爱无疆、共济账户、共济定点、门诊共济、家庭共济
- 报销术语：零星报销

## 与其他模型对比

| 模型 | 大小 | 中文准确率 | 特点 |
|------|------|------------|------|
| Fun-ASR-Nano-2512 | **1.85GB** | 高 | 热词优化、领域专用、LLM架构 |
| Paraformer-zh | 220MB | 高 | 通用中文 |
| Whisper small | 244MB | 中 | 多语言 |
| Whisper medium | 769MB | 高 | 多语言 |

## 使用场景

- ✅ 社保/医保领域语音识别
- ✅ 保险业务对话转录
- ✅ 医疗术语密集内容
- ✅ 中文会议记录
- ✅ 中英混合音频

## 注意事项

- 模型加载需要 2-3GB 内存（CPU模式）或 2GB 显存（GPU模式）
- 首次加载模型约需 30-40 秒
- 使用 FastAPI 服务可避免重复加载模型
- 模型文件较大，传输/备份时请预留足够空间
