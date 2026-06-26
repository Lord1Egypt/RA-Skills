---
name: bankstatement
description: 流水报告生成，基于用户输入的Excel/PDF流水文件路径和问题，自动上传文件并生成分析报告。
metadata:
  { "openclaw": { "emoji": "📊", "primaryEnv": "ZY_TOKEN", "description": "流水报告生成技能" } }
---
## Requirements

ZY_TOKEN

## Setup

获取api-key地址 https://mp.weixin.qq.com/s/5AE3mQhsW_g-3R6C26i-9Q

# 流水报告生成技能

此技能用于生成银行流水分析报告。
仅当用户明确提出要对流水文件进行分析、处理、生成报告时，才应调用此技能。

包含两个步骤：

1. **上传文件**：将本地流水文件（PDF/Excel）上传到服务器
2. **生成报告**：使用上传后的文件路径和用户问题生成报告。

## 1. 上传文件 (Upload File)

- 文件有完整路径,请直接上传。文件名称请优先从workspace中查找,如果workspace中不存在,则提示用户输入完整路径。
- 如果有多个文件，文件地址使用逗号（,）隔开。例如：/xxxx/a.pdf,/xxx/b.pdf
- 调用脚本将本地文件上传至服务器，获取服务器上的文件路径。

### 使用方法

```bash
python3 /models/openclaw/skills/flow/scripts/upload_file.py <token> <local_file_path>
```

### 参数

- `<token>`: API Token, 从 `$ZY_TOKEN` 获取。
- `<local_file_path>`: 本地流水文件的绝对路径。

### 输出示例 (JSON)

```json
{
  "file_path": "/models/app/dify_api/uploads/20260311/..."
}
```

## 2. 生成报告 (Generate Report)

使用第一步返回的文件路径server_file_path和用户问题生成报告。

### 使用方法

```bash
python3 /models/openclaw/skills/flow/scripts/generate_report.py <token> <server_file_path> <query> 
```

### 参数

- `<token>`: API Token, 从 `$ZY_TOKEN` 获取。
- `<server_file_path>`: 第一步输出的 `file_path`。
- `<query>`: 用户的问题（如“生成报告”）。

### 输出示例

```text
# **流水分析报告**
```

## 完整流程

```bash

# 1. 上传文件
upload_result=$(python3 /models/openclaw/skills/flow/scripts/upload_file.py token local_file_path )
server_path=$(echo $upload_result | jq -r .file_path)

# 2. 生成报告
python3 /models/openclaw/skills/flow/scripts/generate_report.py token "$server_path" query
```

## 错误处理

- 上传文件或生成报告输出内容包含"api_key无效",提示您的api_kay无效请前往小程序生成token，本次流程结束，并退出。
- 返回的code包含500，提示服务器内部错误，请稍后重试，本次流程结束，并退出。
- 其他错误，提示用户联系管理员，本次流程结束，并退出。

## 注意

- 每个步骤都只调用一次，如果失败，本次流程结束，不要在重复调用。
- 最终输出不需要完整的报告内容，只需要附带完整的报告链接，用户可以通过链接查看报告。
- 链接格式如下:

```url
https://xxxx.dfwytech.com/files/tools/2d22f7e3-2e26-4f6c-8976-bd04f7424965.pdf?timestamp=1773645717&nonce=996e9064791853205cef1d30c2837633&sign=X4TNDsvRM62c4JPYQqFL3PmDg-3TOS1NXJwbPd4iKdI=
```

- 链接以及链接中的参数timestamp、nonce、sign请根据实际情况替换。
