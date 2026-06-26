---
name: boss-job
description: BOSS直聘求职者工具 - 通过 OpenCLI 实现职位搜索、打招呼、聊天等功能。Install OpenCLI first: npm install -g @jackwener/opencli. Use when user wants to: (1) 搜索或推荐职位 (2) 查看职位详情 (3) 向 HR 打招呼 (4) 查看聊天列表或发送消息。Requires Chrome login on zhipin.com and OpenCLI Chrome extension.
---

# BOSS直聘求职者工具

OpenCLI 插件，复用 Chrome 登录态操作 BOSS直聘。

## 前置条件

1. 安装 OpenCLI
   ```bash
   npm install -g @jackwener/opencli
   ```
   或访问: https://github.com/jackwener/opencli

2. 在 Chrome 中登录 zhipin.com

3. 安装 OpenCLI Chrome 扩展

4. 安装插件: `opencli plugin install github:SPYQWER1/opencli-plugin-boss-job`

## 命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `search` | 搜索职位 | `opencli boss-job search 前端 --city 杭州` |
| `recommend` | 推荐职位 | `opencli boss-job recommend --limit 10` |
| `detail` | 职位详情 | `opencli boss-job detail <security-id>` |
| `greet` | 打招呼 | `opencli boss-job greet <security-id>` |
| `chatlist` | 聊天列表 | `opencli boss-job chatlist` |
| `chatmsg` | 聊天记录 | `opencli boss-job chatmsg <uid> --security-id <id>` |
| `send` | 发送消息 | `opencli boss-job send <uid> "消息内容"` |

## ID 说明

- **securityId**: 用于 `detail` 和 `greet`，从 `search`/`recommend` 的 `security_id` 字段获取
- **encryptUid**: 用于 `chatmsg` 和 `send`，从 `chatlist` 的 `encrypt_uid` 字段获取

## 详细用法

### search - 搜索职位

```bash
opencli boss-job search <关键词> \
  --city <城市> \
  --experience <经验> \
  --degree <学历> \
  --salary <薪资> \
  --limit <数量>
```

参数:
- `--city`: 城市 (北京/上海/杭州/深圳等)
- `--experience`: 应届/1-3年/3-5年/5-10年/10年以上
- `--degree`: 大专/本科/硕士/博士
- `--salary`: 3K以下/3-5K/5-10K/10-15K/15-20K/20-30K/30-50K/50K以上

### greet - 打招呼

```bash
opencli boss-job greet <security-id>
```

### chatmsg - 聊天记录

```bash
opencli boss-job chatmsg <encrypt-uid> --security-id <security-id>
```

需要同时提供 `encrypt_uid` 和 `security_id`，两者都来自 `chatlist` 命令。

## 常见工作流

### 工作流 1: 搜索并打招呼

```bash
# 1. 搜索职位
opencli boss-job search 前端 --city 杭州 --limit 10

# 2. 查看详情
opencli boss-job detail <security-id>

# 3. 打招呼
opencli boss-job greet <security-id> --text "您好，我对这个职位很感兴趣"
```

### 工作流 2: 回复消息

```bash
# 1. 查看聊天列表
opencli boss-job chatlist --limit 20

# 2. 查看聊天记录
opencli boss-job chatmsg <encrypt-uid> --security-id <security-id>

# 3. 回复消息
opencli boss-job send <encrypt-uid> "好的，我稍后发简历给您"
```

## 错误处理

- **Cookie 过期**: 在 Chrome 中重新登录 zhipin.com
