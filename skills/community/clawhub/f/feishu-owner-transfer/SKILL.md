---
name: feishu-owner-transfer
description: |
  飞书文档/多维表格所有权转移工具。将AI机器人创建的飞书文档、多维表格、电子表格、思维导图等文件的所有权转移给指定用户。
  触发词：转移所有者、transfer owner、文档所有者、转让文档、转移文档所有权、把文档转给、文档归档转移、批量转移、owner transfer。
---

# 飞书文档所有权转移 Skill

将 AI 机器人创建的飞书文档的所有者转移给指定人类用户。

## 前置条件
- lark-cli 已安装并登录（lark-cli auth list 显示 valid）
- 目标用户有有效的 open_id

## API

**端点**: POST /open-apis/drive/permission/member/transfer

**参数**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | Y | 文档类型：doc / sheet / bitable / mindnote / file |
| token | string | Y | 文档 token |
| owner.member_type | string | Y | openid / userid / unionid |
| owner.member_id | string | Y | 目标用户 ID |
| remove_old_owner | bool | N | 是否移除原所有者权限（默认 false） |
| cancel_notify | bool | N | 是否取消通知（默认 false） |

## 使用方式

### 单个文件转移
通过 lark-cli 调用 API 即可。

### 批量转移（使用脚本）
```bash
python3 scripts/transfer_owner.py --target ou_xxx --all
python3 scripts/transfer_owner.py --target ou_xxx --list  # dry-run
python3 scripts/transfer_owner.py --target ou_xxx --token bitable:HlJbbGw6SaC50Tse9Tnc96Avncb
```

## 文档类型映射
| 飞书文档 | doc |
| 电子表格 | sheet |
| 多维表格 | bitable |
| 思维导图 | mindnote |
| 文件 | file |
