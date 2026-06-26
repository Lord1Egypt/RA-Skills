---
name: fadada-esign
description: 法大大电子合同与电子签署技能（FASC API 5.0）。一键发送合同给对方签署，支持查询签署状态、下载已签署合同。适用于HR合同、销售合同、协议签署等场景。当用户提到"发合同"、"让对方签合同"、"电子签"、"法大大"、"合同签署"、"查询签署状态"、"下载合同"等场景时触发。
license: MIT
---

# 法大大电子签 Skill（FASC API 5.0）

基于法大大 FASC API 5.0，提供一键式合同创建、发送、签署全流程解决方案。

## ✨ 核心特性

- **一键发送** - 只需一行代码即可完成文件上传、任务创建、获取签署链接
- **正确签名** - 严格按照官方文档实现 HMAC-SHA256 两步签名算法
- **智能配置** - 支持环境变量、配置文件、代码传入多种配置方式
- **命令行工具** - 提供 `fadada` CLI 工具，无需编写代码即可发送合同
- **完整功能** - 支持发送、查询、下载全流程

## 🚀 快速开始

### 1. 安装

```bash
# 安装依赖
pip install requests
```

### 2. 配置凭证

**方式一：环境变量**
```bash
export FADADA_APP_ID="your_app_id"
export FADADA_APP_SECRET="your_app_secret"
export FADADA_OPEN_CORP_ID="your_open_corp_id"
```

**方式二：配置文件**
```bash
# 创建配置文件
mkdir -p ~/.fadada
cat > ~/.fadada/config.json << EOF
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret",
  "open_corp_id": "your_open_corp_id"
}
EOF
```

**方式三：代码中直接传入**
```python
from fadada_esign import FaDaDaClient, Signer

client = FaDaDaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    open_corp_id="your_open_corp_id"
)
```

### 3. 发送合同（最简单的方式）

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

### 4. 命令行发送

```bash
# 发送给单个签署人
fadada send contract.pdf --signer "张三:13800138000"

# 发送给多个签署人
fadada send contract.pdf --signer "张三:13800138000" --signer "李四:13900139000"

# 指定任务主题
fadada send contract.pdf --signer "张三:13800138000" --subject "销售合同"
```

## 📖 API 文档

### 客户端初始化

```python
from fadada_esign import FaDaDaClient

# 正式环境
client = FaDaDaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    open_corp_id="your_open_corp_id"
)

# 沙箱环境
client = FaDaDaClient(
    app_id="your_app_id",
    app_secret="your_app_secret",
    open_corp_id="your_open_corp_id",
    sandbox=True
)
```

### 一键发送文档

```python
from fadada_esign import FaDaDaClient, Signer

client = FaDaDaClient(...)

# 方式1：发送给单个签署人（最简单）
result = client.send_to_single_signer(
    file_path="/path/to/contract.pdf",
    signer_name="张三",
    signer_mobile="13800138000"
)

# 方式2：发送给多个签署人
signers = [
    Signer(name="张三", mobile="13800138000", actor_id="signer1"),
    Signer(name="李四", mobile="13900139000", actor_id="signer2")
]

result = client.send_document(
    file_path="/path/to/contract.pdf",
    signers=signers,
    task_subject="多方合同"
)

# 返回结果
print(result)
# {
#     "sign_task_id": "1774590564587181726",
#     "sign_url": "https://fdd1.cn/dQFiT0SDcw1",
#     "task_subject": "多方合同",
#     "file_path": "/path/to/contract.pdf",
#     "signers": [...]
# }
```

### 分步操作

```python
from fadada_esign import FaDaDaClient, Signer

client = FaDaDaClient(...)

# 1. 上传文件
file_id = client.upload_file("/path/to/contract.pdf")

# 2. 创建签署任务
signer = Signer(name="张三", mobile="13800138000")
sign_task_id = client.create_sign_task(
    task_subject="合同签署",
    file_id=file_id,
    signers=[signer]
)

# 3. 获取签署链接
sign_url = client.get_sign_url(sign_task_id)
```

### 查询签署状态

```python
# 查询任务详情
detail = client.query_task_detail(sign_task_id)
print(detail)
# {
#     "signTaskId": "xxx",
#     "signTaskSubject": "合同签署",
#     "signTaskStatus": "sign_progress",
#     "actors": [...]
# }
```

### 下载已签署文档

```python
# 获取下载链接
download_url = client.get_download_url(sign_task_id)
print(f"下载链接: {download_url}")

# 或者直接下载
import requests
response = requests.get(download_url)
with open("signed_contract.pdf", "wb") as f:
    f.write(response.content)
```

## 🔧 命令行工具

### 配置管理

```bash
# 交互式配置
fadada config setup

# 查看当前配置
fadada config show
```

### 发送合同

```bash
# 基础用法
fadada send contract.pdf --signer "张三:13800138000"

# 多个签署人
fadada send contract.pdf \
    --signer "张三:13800138000" \
    --signer "李四:13900139000" \
    --subject "合作协议"

# 保存结果到文件
fadada send contract.pdf \
    --signer "张三:13800138000" \
    --output result.json
```

### 查询状态

```bash
fadada status <task_id>
```

### 下载合同

```bash
fadada download <task_id> --output ./signed_contract.pdf
```

## 📋 签署任务状态

| 状态 | 说明 |
|------|------|
| draft | 创建中 |
| submitting | 提交中 |
| fill_wait | 等待填写 |
| filled | 填写完成 |
| sign_progress | 签署进行中 |
| finished | 已完成 |
| cancelled | 已撤销 |
| expired | 已过期 |

## 📝 签署人配置

```python
from fadada_esign import Signer

# 基础配置
signer = Signer(
    name="张三",
    mobile="13800138000"
)

# 完整配置
signer = Signer(
    name="张三",
    mobile="13800138000",
    actor_id="signer1",
    actor_type="person",  # person 或 corp
    permissions=["sign"],
    notification={
        "sendNotification": True,
        "notifyWay": "mobile",
        "notifyAddress": "13800138000"
    },
    id_number="11010119900101xxxx",  # 可选
    email="zhangsan@example.com"  # 可选
)
```

## ⚙️ 配置优先级

配置加载优先级（从高到低）：

1. 代码中显式传入的参数
2. 环境变量（`FADADA_APP_ID`, `FADADA_APP_SECRET`, `FADADA_OPEN_CORP_ID`）
3. 本地配置文件（`.fadada.json` 或 `fadada_config.json`）
4. 全局配置文件（`~/.fadada/config.json`）

## 🔐 安全注意事项

- **App Secret 不要硬编码**在代码中，建议使用环境变量或配置文件
- **配置文件权限**建议设置为 `600`（仅所有者可读写）
- **生产环境**建议使用正式环境（sandbox=False）

## 🐛 错误处理

```python
from fadada_esign import FaDaDaClient, Signer
from fadada_esign.exceptions import FaDaDaError, FaDaDaAuthError, FaDaDaAPIError

client = FaDaDaClient(...)

try:
    result = client.send_to_single_signer(...)
except FaDaDaAuthError as e:
    print(f"认证失败: {e}")
except FaDaDaAPIError as e:
    print(f"API 错误: {e.code} - {e}")
except FaDaDaError as e:
    print(f"操作失败: {e}")
```

## 📚 完整示例

```python
#!/usr/bin/env python3
"""
法大大电子签 - 完整示例
"""

from fadada_esign import FaDaDaClient, Signer

def main():
    # 初始化客户端
    client = FaDaDaClient(
        app_id="your_app_id",
        app_secret="your_app_secret",
        open_corp_id="your_open_corp_id",
        sandbox=False  # 生产环境
    )
    
    # 创建签署人
    signers = [
        Signer(name="张三", mobile="13800138000", actor_id="signer1"),
        Signer(name="李四", mobile="13900139000", actor_id="signer2")
    ]
    
    # 发送合同
    result = client.send_document(
        file_path="./劳动合同.pdf",
        signers=signers,
        task_subject="2024年劳动合同"
    )
    
    print("=" * 50)
    print("✅ 合同发送成功！")
    print("=" * 50)
    print(f"任务 ID: {result['sign_task_id']}")
    print(f"签署链接: {result['sign_url']}")
    print()
    
    # 保存任务ID供后续查询
    task_id = result['sign_task_id']
    
    # 稍后查询状态
    # detail = client.query_task_detail(task_id)
    # print(f"当前状态: {detail['signTaskStatus']}")
    
    # 签署完成后下载
    # download_url = client.get_download_url(task_id)
    # print(f"下载链接: {download_url}")

if __name__ == "__main__":
    main()
```

## 📄 文件结构

```
fadada_esign/
├── __init__.py      # 包入口
├── client.py        # 核心客户端
├── signer.py        # 签署人模型
├── config.py        # 配置管理
├── cli.py           # 命令行工具
└── exceptions.py    # 异常类
```

## 🔗 相关链接

- [法大大开放平台](https://www.fadada.com/)
- [FASC API 5.0 文档](https://docs.fadada.com/)

## 📄 License

MIT License
