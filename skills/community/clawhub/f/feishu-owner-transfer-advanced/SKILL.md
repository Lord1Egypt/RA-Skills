---
name: feishu-owner-transfer-advanced
description: |
  飞书文档/多维表格所有权转移工具（增强版）。支持单个/批量转移，支持wiki空间扫描，支持lark-cli和Python两种调用方式。
  触发词：转移所有权、转移文档、转移owner、文档转给我、所有权转移、批量转移、transfer owner、feishu owner
version: "1.0.0"
---

# 飞书文档所有权转移 Skill（增强版）

将 AI 机器人创建的飞书文档所有权转移给指定用户。

## 核心能力

- ✅ 单个文件转移（docx / sheet / bitable / mindnote / file）
- ✅ 扫描根目录批量转移
- ⚠️ Wiki节点：节点本身由创建者（通常是老板）所有，无需转移
  - Wiki节点指向的文档(obj_token)，若owner非目标用户才需转移
- ✅ 支持 lark-cli 和 Python requests 两种调用方式
- ✅ 自动过滤：跳过已是人类所有者的文件

---

## 方式一：lark-cli（推荐，已配置好环境）

### 单个转移
```bash
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_owner.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 \
  --token docx:文档token
```

### 扫描根目录批量转移
```bash
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_owner.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 \
  --all
```

### Dry-run（只列出，不转移）
```bash
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_owner.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 \
  --all --list
```

### 扫描wiki空间批量转移
```bash
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_wiki.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 \
  --space 7530421454261829636
```

---

## 方式二：Python requests（韩博原始脚本）

适合需要自定义参数时使用。

```python
import requests

# -------- 配置区 --------
APP_ID = "cli_xxxxxxxx"
APP_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxx"
TENANT_TOKEN = "t-xxxxxxxxxxxxxxxxxxxxxxxx"  # AI智能体的tenant_access_token
FILE_TOKEN = "doxcnxxxxxxxxxxxxxxxxxxxxxxxx"  # 要转的文档token
MY_USER_ID = "ou_xxxxxxxxxxxxxxxxxxxxxxxx"   # 你的openid
# --------------------------------------

url = "https://open.feishu.cn/open-apis/drive/permission/member/transfer"
headers = {
    "Authorization": f"Bearer {TENANT_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "type": "doc",  # doc / sheet / bitable / file
    "token": FILE_TOKEN,
    "owner": {
        "member_type": "openid",
        "member_id": MY_USER_ID
    },
    "remove_old_owner": False,
    "cancel_notify": False
}
resp = requests.post(url, json=data, headers=headers)
print(resp.json())
```

---

## 常用参数

| 参数 | 值 | 说明 |
|------|-----|------|
| type | `docx` | 在线文档 |
| type | `sheet` | 电子表格 |
| type | `bitable` | 多维表格 |
| type | `mindnote` | 思维导图 |
| type | `file` | 普通文件 |
| member_type | `openid` | 用户ID类型（默认openid） |
| remove_old_owner | `False` | 保留AI机器人权限 |

---

## 老板的固定配置

- 目标用户 open_id：`ou_b2d0ace4a1175bb8d914678b0e9b1f10`（韩博）
- lark-cli 已安装并登录，开箱即用

---

## 快速命令汇总

```bash
# 转移单个文档（最常用）
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_owner.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 \
  --token docx:doxcnxxxxxxxxxxxxxxxxxxxxxxxx

# 扫描所有文件并批量转移
python3 ~/.qclaw/skills/feishu-owner-transfer-advanced/scripts/transfer_owner.py \
  --target ou_b2d0ace4a1175bb8d914678b0e9b1f10 --all
```
