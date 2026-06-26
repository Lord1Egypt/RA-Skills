# 法大大电子签 SDK (FASC API 5.0)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

基于法大大 FASC API 5.0 的官方 Python SDK，提供一键式电子合同创建、发送、签署全流程解决方案。

## ✨ 核心特性

- **一键发送** - 一行代码完成文件上传、任务创建、获取签署链接
- **正确签名** - 严格按照官方文档实现 HMAC-SHA256 两步签名算法
- **智能配置** - 支持环境变量、配置文件、代码传入多种配置方式
- **命令行工具** - 提供 `fadada` CLI 工具，无需编写代码即可发送合同
- **完整功能** - 支持发送、查询、下载全流程

## 🚀 快速开始

### 安装

```bash
pip install requests
```

### 配置凭证

**方式一：环境变量（推荐）**
```bash
export FADADA_APP_ID="your_app_id"
export FADADA_APP_SECRET="your_app_secret"
export FADADA_OPEN_CORP_ID="your_open_corp_id"
```

**方式二：配置文件**
```bash
mkdir -p ~/.fadada
cat > ~/.fadada/config.json << EOF
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret",
  "open_corp_id": "your_open_corp_id"
}
EOF
```

### 发送合同（最简单的方式）

```python
from fadada_esign import FaDaDaClient, Signer

# 创建客户端
client = FaDaDaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    open_corp_id="your_open_corp_id"
)

# 一键发送合同
result = client.send_to_single_signer(
    file_path="/path/to/contract.pdf",
    signer_name="张三",
    signer_mobile="13800138000",
    task_subject="劳动合同签署"
)

print(f"签署链接: {result['sign_url']}")
```

### 命令行发送

```bash
# 发送给单个签署人
fadada send contract.pdf --signer "张三:13800138000"

# 发送给多个签署人
fadada send contract.pdf --signer "张三:13800138000" --signer "李四:13900139000"
```

## 📖 更多文档

详见 [SKILL.md](SKILL.md)

## 📄 License

MIT License
