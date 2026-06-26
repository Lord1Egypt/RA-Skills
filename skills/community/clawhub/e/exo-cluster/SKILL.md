---
name: exo-cluster
version: 1.0.1
description: Exo 分布式 AI 集群 - 将多台 Mac/PC/WSL2 设备整合为统一 GPU 集群，本地运行大模型。支持 DeepSeek、Qwen、LLaMA。
keywords: [Exo,分布式,GPU集群,大模型,本地部署,DeepSeek,Mac Studio,WSL2,Windows]
---

# Exo 分布式 AI 集群
将闲置设备整合为统一算力集群

---

## 概述

**Exo** 可将多台 Mac、PC、手机等设备整合为一个 GPU 集群，在本地运行大模型。

| 项目 | 信息 |
|------|------|
| **Stars** | 44.5K |
| **官网** | https://exolabs.net/ |
| **GitHub** | `exo-explore/exo` |

---

## 支持的模型

- DeepSeek V3 / V2
- Qwen3-235B
- Kimi2-Thinking
- LLaMA (MLX)
- Mistral
- LlaVA

---

## 触发词

`搭建集群` / `exo集群` / `本地部署大模型` / `分布式推理`

---

## 环境准备

### Mac (推荐)
```bash
# 1. 安装 Xcode
xcode-select --install

# 2. 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. 安装依赖
brew install uv node rust

# 4. 安装 Exo
git clone https://github.com/exo-explore/exo
cd exo
```

### WSL2 / Windows
```bash
# 方式1: 用社区原生版
git clone https://github.com/tensorsofthewall/exo_windows
exo_windows

# 方式2: WSL2 中运行
git clone https://github.com/exo-explore/exo
cd exo
pip install -e .
python -m exo.main --role master
```

### Linux + NVIDIA
```bash
# 安装 CUDA 和相关驱动
# 然后同样 clone exo
git clone https://github.com/exo-explore/exo
cd exo
```

---

## 快速开始

### 方式一：Nix（最简单）
```bash
# 如果有 Nix
nix run .#exo
```

### 方式二：手动安装
```bash
cd exo

# 启动主节点
python -m exo.main --role master --port 8080 --name "home-cluster"

# 其他设备加入（从节点）
python -m exo.main --role worker --master-addr 主节点IP:8080 --name "设备名"

# 低配设备轻量模式
python -m exo.main --role worker --master-addr 主节点IP:8080 --light-mode
```

### WSL2 快速启动
```bash
# 1. 克隆
cd ~
git clone https://github.com/tensorsofthewall/exo_windows
exo_windows

# 2. 安装依赖
pip install -e .
# 或
pip install torch tinygrad

# 3. 启动
python -m exo.main --role master --port 8080 --name "wsl2-cluster"

# 浏览器打开 http://localhost:52415
```

---

## 查看和部署模型

### 查看可用模型
```bash
python -m exo.master.api --list-available-models
```

### 部署模型
```bash
# 部署 DeepSeek 7B
python -m exo.master.api --deploy-model deepseek-7b --min-nodes 2 --max-nodes 4

# 部署更大的模型
python -m exo.master.api --deploy-model qwen3-235b --min-nodes 2 --max-nodes 4
```

---

## 使用 API

Exo 提供多种 API 兼容：

### OpenAI 风格
```bash
curl http://localhost:52415/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-7b",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### Claude 风格
```bash
curl http://localhost:52415/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-7b",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### Ollama 风格
```bash
curl http://localhost:52415/api/generate \
  -d '{"model": "deepseek-7b", "prompt": "你好"}'
```

---

## 集群管理

### 打开 Dashboard
```
http://主节点IP:52415
```

### 查看集群状态
```bash
python -m exo.main --status
```

### 硬件诊断
```bash
python -m exo.utils.info_gatherer.system_info --detailed
```

---

## 性能优化

### 推荐配置
| 设备数量 | 推荐模型 | 内存要求 |
|----------|---------|----------|
| 1 台 | 7B | ~16GB |
| 2 台 | 14B | ~32GB |
| 4 台 | 70B | ~128GB |
| 4 台 Mac Studio 512GB | 671B (8-bit) | 2TB 统一内存 |

### 优化技巧
1. 使用 RDMA over Thunderbolt（Mac 之间）
2. 启用 Tensor Parallel
3. 模型量化（8-bit / 4-bit）
4. 调整任务分配策略

---

## 常见问题

### Q: 设备发现不了？
A: 确保在同一局域网，使用有线或 5GHz WiFi

### Q: 跑不动大模型？
A: 从 7B 开始测试，确认单设备能跑再增加节点

### Q: 速度慢？
A: 使用 Thunderbolt 联网，或启用 RDMA

---

## 快速指令表

| 需求 | 命令 |
|------|------|
| 启动主节点 | `exo --role master` |
| 设备加入集群 | `exo --role worker --master-addr IP` |
| 部署模型 | `exo --deploy-model 模型名` |
| 查看模型列表 | `exo --list-models` |
| 查看状态 | `exo --status` |
| 打开管理界面 | `http://localhost:52415` |

---

## 与 OpenClaw 集成

**可以配合使用：**
1. 在 Mac 上部署 Exo 集群
2. 通过 API 调用模型
3. OpenClaw 作为前端交互

**示例：**
```bash
# 让集群运行推理
curl -X POST http://mac-server:52415/v1/chat/completions \
  -d '{"model": "deepseek-7b", "messages": [{"role": "user", "content": "解释量子计算"}]}'
```

*Exo | 分布式 AI 集群框架*