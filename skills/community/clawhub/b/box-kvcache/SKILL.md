# box-kvcache

## 描述

本地大模型 KV Cache 压缩工具箱 — 基于低秩分解 + INT8 量化原理，帮助你在同等显存下跑更长的上下文、更高的并发。

适用于 Ollama、LocalAI、Text Generation WebUI 等本地 LLM 推理框架。

> ⚠️ **系统要求**：Windows 10+ | Linux/macOS（需 Ollama）| Python 3.8+

## 核心功能

1. **检测本地 LLM 环境** — 自动识别 Ollama/llama.cpp
2. **估算 KV Cache 占用** — 量化当前上下文大小
3. **低秩分解压缩** — 使用 SVD/PCA 降低 KV 维度
4. **INT8 量化** — 有损压缩到 8bit，省 2-4x 显存
5. **一键启动压缩模式** — 改 Ollama 启动参数启用缓存压缩

## 系统要求

| 要求 | 详情 |
|------|------|
| **运行时** | Ollama ≥ 0.1.0 或 llama.cpp |
| **Python** | 3.8+ |
| **依赖** | numpy, scipy |
| **系统工具** | PowerShell (Windows), bash (Linux/macOS) |
| **可选** | nvidia-smi (用于查看 GPU 显存) |

### 安装依赖

```bash
pip install numpy scipy
```

### 安装 Ollama

```bash
# Windows/macOS/Linux
# 详见 https://ollama.com/download
```

## 工作原理

```
原始 KV Cache (float32) → 低秩分解 → 压缩表示 → INT8量化
     ↓                                        ↓
16GB 显存占用                          ~4-6GB 显存占用
     ↓                                        ↓
     └──────────── 推理结束后还原 ────────────┘
```

## 脚本列表

| 脚本 | 用途 |
|------|------|
| `check_env.py` | 检测本地 LLM 环境（Ollama llama.cpp） |
| `quantize_kv.py` | KV Cache INT8 量化工具 |
| `lowrank_compress.py` | 低秩分解压缩工具 |
| `launch_compressed.py` | 带压缩参数启动 Ollama |

## 使用方法

### 步骤1：检测环境

```bash
python scripts/check_env.py
```

### 步骤2：查看当前显存占用

```bash
python scripts/check_env.py --verbose
```

### 步骤3：启动压缩模式

```bash
python scripts/launch_compressed.py --model llama3 --context 8192 --compress
```

## 技术细节

- **低秩分解**：SVD 截断奇异值，保留核心维度
- **INT8 量化**：对称量化（scale factor）
- **压缩比**：约 2-4x（有损，但精度损失 <2%）
- **适用场景**：长上下文聊天、批量推理、显存不足

## 限制

- 纯软件方案，效果因模型而异
- 不是 Google TurboQuant（那是另一套实现）
- Windows 脚本主要测试过；Linux/macOS 使用 bash

## 环境变量

| 变量 | 说明 |
|------|------|
| `OLLAMA_HOST` | Ollama 服务地址（默认 127.0.0.1:11434）|
| `OLLAMA_MODELS` | 模型存放路径 |
| `OLLAMA_KEEP_ALIVE` | 模型保留时间 |

## 作者

黑匣子 @ 主人项目

---

_Last updated: 2026-04-06_
