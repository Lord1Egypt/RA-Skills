# DeBox 社区管理及个人社交数据报告 Skill 使用教程

本教程将帮助你快速上手 DeBox 社区管理 Skill，实现群组信息查询、成员验证、个人数据报告等功能。

---

## 目录

1. [环境准备](#1-环境准备)
2. [获取 DeBox API Key](#2-获取-debox-api-key)
3. [安装与配置](#3-安装与配置)
4. [功能介绍](#4-功能介绍)
5. [快速开始](#5-快速开始)
6. [实际场景示例](#6-实际场景示例)
7. [常见问题](#7-常见问题)

---

## 1. 环境准备

### 1.1 系统要求

- Node.js 16+
- npm 或 yarn

### 1.2 安装 OpenClaw

```bash
npm install -g openclaw
```

---

## 2. 获取 DeBox API Key

### 2.1 注册开发者账号

1. 访问 [DeBox 开发者平台](https://developer.debox.pro)
2. 使用 DeBox App 扫码登录
3. 进入控制台，创建应用

### 2.2 获取 API Key

在应用详情页面，复制你的 API Key。

---

## 3. 安装与配置

### 3.1 安装 Skill

将 `debox-community` 文件夹放置在 OpenClaw 工作目录：

```
~/.openclaw/workspace/debox-community/
```

### 3.2 安装依赖

```bash
cd ~/.openclaw/workspace/debox-community
npm install
```

### 3.3 配置 API Key

**方式一：环境变量（推荐）**

```bash
export DEBOX_API_KEY="your-api-key-here"
```

**方式二：配置文件**

创建 `config.json` 文件：

```bash
cd ~/.openclaw/workspace/debox-community
```

创建 `config.json`：

```json
{
  "apiKey": "your-api-key-here",
  "defaultGroupId": "可选-默认群组ID"
}
```

---

## 4. 功能介绍

### 4.1 命令列表

| 命令 | 功能 | 推荐指数 |
|------|------|---------|
| `profile` | 个人数据报告（支持生成图片） | ⭐⭐⭐⭐⭐ |
| `info` | 群组信息查询 | ⭐⭐⭐ |
| `check-member` | 验证用户是否在群 | ⭐⭐⭐ |
| `user-info` | 用户信息查询 | ⭐⭐⭐ |
| `vote-stats` | 投票统计 | ⭐⭐ |
| `lottery-stats` | 抽奖统计 | ⭐⭐ |
| `praise-info` | 点赞信息 | ⭐⭐ |
| `verify` | 综合验证 | ⭐⭐⭐⭐ |
| `batch-verify` | 批量验证 | ⭐⭐⭐⭐ |

---

## 5. 快速开始

### 5.1 查看帮助

```bash
node scripts/debox-community.js
```

### 5.2 个人数据报告（推荐）

```bash
# 查看文字报告
node scripts/debox-community.js profile --user-id "你的user_id"

# 生成图片报告
node scripts/debox-community.js profile --user-id "你的user_id" --image
```

**如何获取 user_id：**
1. 打开 DeBox App
2. 进入个人主页
3. 点击右上角分享按钮
4. 复制链接，链接中的 `id` 参数就是 user_id

例如链接是 `https://m.debox.pro/user?id=abc123`，那么 user_id 就是 `abc123`。

### 5.3 查询群组信息

```bash
node scripts/debox-community.js info --url "https://m.debox.pro/group?id=xxx"
```

### 5.4 验证用户是否在群

```bash
node scripts/debox-community.js check-member --wallet "0xabc..." --group-url "https://m.debox.pro/group?id=xxx"
```

### 5.5 查询用户信息

```bash
node scripts/debox-community.js user-info --user-id "xxx"
```

---

## 6. 实际场景示例

### 场景一：查看自己的 DeBox 数据报告

```bash
# 文字版
node scripts/debox-community.js profile --user-id "trxuvgm9"

# 图片版（可分享）
node scripts/debox-community.js profile --user-id "trxuvgm9" --image --output "my-report.png"
```

**输出示例：**

```
╔════════════════════════════════════════╗
║        🎫 DeBox 个人数据报告           ║
╠════════════════════════════════════════╣
║  👤 基本信息                           ║
╠════════════════════════════════════════╣
║  昵称：ZanyK                           ║
║  用户ID：trxuvgm9                      ║
║  钱包：0xcd44ffeb...4c3643             ║
║  等级：Lv.2                            ║
╠════════════════════════════════════════╣
║  ❤️  社交互动                           ║
╠════════════════════════════════════════╣
║  收到的点赞：0                          ║
║  发出的点赞：2                          ║
╚════════════════════════════════════════╝
```

![image-20260310094107019](C:\Users\ZFT15\AppData\Roaming\Typora\typora-user-images\image-20260310094107019.png)

### 场景二：验证用户是否满足空投条件

```bash
# 验证用户是否在群 + 是否投票
node scripts/debox-community.js verify \
  --wallet "0xabc..." \
  --group-url "https://m.debox.pro/group?id=xxx" \
  --min-votes 3
```

### 场景三：批量验证白名单

1. 创建 `wallets.txt` 文件，每行一个钱包地址：

```
0xabc123...
0xdef456...
0x789ghi...
```

2. 运行批量验证：

```bash
node scripts/debox-community.js batch-verify \
  --file wallets.txt \
  --group-url "https://m.debox.pro/group?id=xxx" \
  --min-votes 1
```

---

## 7. 常见问题

### Q1: API Key 报错怎么办？

**错误信息：** `Error: INVALID_API_KEY`

**解决方案：**
1. 确认 API Key 是否正确
2. 确认 API Key 是否已过期
3. 检查环境变量或配置文件是否正确设置

### Q2: 找不到 user_id 怎么办？

**解决方案：**
1. 打开 DeBox App
2. 进入个人主页
3. 点击右上角分享按钮
4. 复制链接，链接格式为 `https://m.debox.pro/user?id=xxx`
5. `id` 参数就是 user_id

### Q3: 头像显示不出来怎么办？

**解决方案：**
- 确保 `ClawBot.png` 文件存在于 skill 目录
- 检查网络是否能访问 DeBox 头像服务器

### Q4: 群组暂无投票/抽奖活动是什么意思？

**说明：** 该群组目前没有进行中的投票或抽奖活动，所以无法查询相关数据。

---

## 附录

### 相关链接

- DeBox 官网：https://debox.pro
- DeBox 开发者平台：https://developer.debox.pro
- DeBox API 文档：https://docs.debox.pro
- OpenClaw 文档：https://docs.openclaw.ai

### 技术支持

如有问题，可加入 DeBox 技术支持群：`cc0onr82`

---

**Happy Coding! 🎉**