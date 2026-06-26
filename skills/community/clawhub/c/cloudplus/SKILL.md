---
name: cloudplus
description: "操作云加（CloudPlus）企业通讯应用。当用户需要通过云加发消息、发文件、搜索联系人、查聊天记录、搜索群聊、搜索文件、打开应用或链接时触发。关键词：云加、发消息、发文件、聊天记录、搜索联系人、群聊、轻应用。"
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
---

# CloudPlus Skill

## 环境准备

在执行任何操作前，按以下顺序检查：

**第一步：检查 Node.js 是否安装**
```bash
node --version
```
如果命令不存在，告知用户先安装 Node.js（https://nodejs.org），安装完成后再继续。

**第二步：检查 mcp-cloudplus 是否安装**
```bash
which mcp-cloudplus
```
如果命令不存在，执行安装：
```bash
npm install -g cloudplus-mcp-server
```

安装完成后继续执行用户请求。

## 命令列表

所有命令输出 JSON，格式为 `{"success":true,"data":{...}}` 或 `{"success":false,"error":"..."}`。

### 发送消息
```bash
mcp-cloudplus send-text --to <用户名或群名> --message <内容>
```

### 发送文件

```bash
mcp-cloudplus send-file --to <用户名或群名> --file <文件路径>
```

发送之前先确认完整路径，并检查文件是否存在

### 搜索联系人

```bash
mcp-cloudplus search-user <关键词>
```
支持姓名、手机号模糊搜索，最多返回 50 条。

### 搜索群聊
```bash
mcp-cloudplus search-group-chat <关键词>
```

### 搜索聊天文件
```bash
mcp-cloudplus search-file <关键词>
```

### 搜索聊天消息
```bash
mcp-cloudplus search-message <关键词>
```

### 搜索轻应用
```bash
mcp-cloudplus search-light-apps <关键词>
```

### 获取聊天记录
```bash
mcp-cloudplus get-chat-history --username <用户名或群名> --start <YYYY-MM-DD> [--end <YYYY-MM-DD>]
```
`--end` 不填默认为当前时间。

### 获取收藏内容
```bash
mcp-cloudplus get-collect-content
```

### 在云加中打开链接
```bash
mcp-cloudplus open-url <url>
```

### 在云加中打开轻应用
```bash
mcp-cloudplus open-app <应用名>
```

### 启动云加
```bash
mcp-cloudplus open-cloudplus
```

## 错误处理

- `找不到管道路径文件` → 提示用户确认云加桌面客户端是否已启动
- `success: false` 且其他错误 → 将 `error` 字段内容告知用户
- 命令不存在 → 重新执行安装步骤

## 操作流程

1. 检查 `mcp-cloudplus` 是否安装，未安装则安装
2. 执行对应命令
3. 解析 JSON 结果
4. 用自然语言向用户反馈结果，不要把原始 JSON 直接展示给用户
