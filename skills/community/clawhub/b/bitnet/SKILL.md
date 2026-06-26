---
name: bitnet
description: 微软官方 1-bit LLM 推理框架，在 CPU 上运行 1.58-bit 量化大语言模型，速度提升 1.4-6x、能耗降低 55-82%，单 CPU 可运行 100B 参数模型，达到人类阅读速度
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - cmake
    emoji: ⚡
    homepage: https://github.com/microsoft/BitNet
---

# BitNet — 1-bit LLM 本地高效推理

bitnet.cpp 是微软研究院发布的官方 1-bit LLM 推理框架，基于 llama.cpp 构建，专为 BitNet b1.58 系列模型优化。在 x86 CPU 上速度提升 2.37-6.17 倍，能耗降低 71-82%；在 ARM CPU 上速度提升 1.37-5.07 倍，能耗降低 55-70%。单台消费级 CPU 即可以 5-7 tokens/秒的速度运行 100B 参数模型，达到人类阅读速度，彻底改变本地 LLM 部署的经济性。

## 核心使用场景

- **CPU 本地 LLM 推理**：无需 GPU，在消费级 CPU 上运行数十亿参数模型
- **边缘设备部署**：极低能耗，适合嵌入式设备、笔记本电脑、服务器 CPU
- **隐私敏感场景**：完全本地运行，数据不离开设备
- **大规模批量推理**：多线程优化，节省数据中心能源成本
- **学术研究**：研究 1-bit LLM 量化技术和推理优化

## AI 辅助使用流程

1. **环境搭建** — AI 创建 conda 环境并安装编译依赖（Python、CMake、Clang）
2. **克隆仓库** — AI 执行 `git clone --recursive https://github.com/microsoft/BitNet.git`
3. **下载模型** — AI 使用 `huggingface-cli download` 下载官方 BitNet 模型
4. **编译环境** — AI 运行 `python setup_env.py` 量化模型并编译推理内核
5. **运行推理** — AI 执行 `python run_inference.py` 进行对话或文本生成
6. **性能测试** — AI 运行 `python e2e_benchmark.py` 测量吞吐量和延迟

## 关键章节导航

- [安装指南](guides/01-installation.md) — 依赖安装、conda 环境、模型下载
- [快速开始](guides/02-quickstart.md) — 编译量化、运行推理、对话模式
- [高级用法](guides/03-advanced-usage.md) — GPU 推理、性能测试、多线程配置
- [故障排查](troubleshooting.md) — 编译错误、模型加载失败、性能问题

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 搭建 conda 环境并安装编译依赖（CMake、Clang）
- ✅ 克隆 BitNet 仓库并安装 Python 依赖
- ✅ 使用 `huggingface-cli` 下载指定 BitNet 模型
- ✅ 运行 `setup_env.py` 完成量化和环境配置
- ✅ 执行 `run_inference.py` 进行对话推理
- ✅ 运行 `e2e_benchmark.py` 测试推理性能
- ✅ 配置多线程参数优化吞吐量

## 核心功能

- ✅ **极速 CPU 推理** — x86 CPU 提升 2.4-6.2x，ARM CPU 提升 1.4-5.1x
- ✅ **超低能耗** — 比传统 INT8 推理节能 55-82%
- ✅ **大模型单 CPU** — 100B 模型在单 CPU 以 5-7 tokens/秒运行
- ✅ **官方量化内核** — I2_S、TL1、TL2 三种针对不同硬件优化的内核
- ✅ **GPU 支持** — 官方 GPU 推理内核（2025 年发布）
- ✅ **多模型支持** — BitNet-b1.58 2B/3B、Llama3-8B-1.58bit、Falcon3 系列
- ✅ **对话模式** — `-cnv` 标志启用交互式聊天（系统提示支持）
- ✅ **性能基准** — 内置 `e2e_benchmark.py` 测量 tokens/秒和能耗

## 快速示例

```bash
# 克隆并进入项目
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet

# 安装依赖
conda create -n bitnet-cpp python=3.9 && conda activate bitnet-cpp
pip install -r requirements.txt

# 下载官方模型并量化
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 运行对话推理
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "You are a helpful assistant" \
  -cnv
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Python | >= 3.9 |
| CMake | >= 3.22 |
| Clang | >= 18 |
| conda | 推荐（环境隔离） |
| 磁盘空间 | 模型约 1-20 GB |

## 项目链接

- GitHub：https://github.com/microsoft/BitNet
- 官方模型（HuggingFace）：https://huggingface.co/microsoft/BitNet-b1.58-2B-4T
- GPU 推理文档：https://github.com/microsoft/BitNet/blob/main/gpu/README.md
- 技术报告：https://arxiv.org/abs/2410.16144
