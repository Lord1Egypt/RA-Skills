# Binance Monitor - 币安公告 + X 账号监控技能

> 一站式监控币安官方公告和 X 账号动态，第一时间获取币安最新信息

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://clawhub.ai)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## 📖 简介

Binance Monitor 是一个 OpenClaw 技能，用于实时监控币安（Binance）官方公告和 X（Twitter）账号动态，检测到新内容时立即通过飞书发送通知给用户。

### 核心特性

- ⚡ **双重监控** - 同时监控公告 API 和 X 账号动态
- 🔔 **即时通知** - 检测到新内容立即推送飞书消息
- 📝 **内容摘要** - 自动提取公告/推文关键信息
- 🐦 **X 账号监控** - 监控 @binance 和 @binancezh 两个官方账号
- 💾 **状态持久化** - 智能记录已读动态，避免重复通知
- 🔄 **自动运行** - 后台持续监控，无需人工干预
- 🛡️ **安全可靠** - 请求频率在 API 限流范围内

### 使用场景

| 场景 | 说明 |
|------|------|
| 🪙 上币/下架公告 | 第一时间获知新币上线或下架信息 |
| 📊 交易规则变更 | 及时了解合约调整、手续费变化 |
| 🔧 系统维护通知 | 提前准备 API 维护、系统升级 |
| 🎁 活动空投公告 | 不错过任何官方活动和空投 |
| 📰 重要政策更新 | 快速响应监管政策、业务调整 |
| 🐦 X 账号动态 | 监控 @binance 和 @binancezh 最新推文 |

---

## 🚀 快速开始

### 前置要求

- Node.js >= 18.0.0
- OpenClaw 运行环境
- 飞书账号（用于接收通知）

### 安装

```bash
# 方式 1: 从 ClawHub 安装（推荐）
clawhub install binance-announce-monitor

# 方式 2: 手动克隆
git clone https://github.com/your-repo/binance-announce-monitor.git
cd binance-announce-monitor
```

### 配置

复制配置文件并根据需要修改：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "checkIntervalSeconds": 30,
  "targetUser": "ou_xxxxxxxxxxxxxx",
  "channel": "feishu"
}
```

| 参数 | 默认值 | 必填 | 说明 |
|------|--------|------|------|
| `checkIntervalSeconds` | 30 | 否 | 公告检查间隔（秒），建议 >= 30 |
| `targetUser` | 当前用户 | 否 | 飞书 open_id |
| `channel` | feishu | 否 | 通知渠道 |

### 启动

```bash
# 方式 1: 启动全部监控（推荐）
./start-all.sh

# 方式 2: 只启动公告监控
./start.sh
# 或
node monitor.js

# 方式 3: 只启动 X 账号监控
node x-monitor.js

# 方式 4: 后台运行全部监控
nohup ./start-all.sh > monitor.log 2>&1 &
```

---

## 📋 使用说明

### 基本命令

```bash
# 启动全部监控
./start-all.sh

# 只启动公告监控
node monitor.js

# 只启动 X 账号监控
node x-monitor.js

# 查看运行日志
tail -f monitor.log

# 查看已读公告记录
cat binance-announce-state.json

# 查看已读 X 动态记录
cat binance-x-state.json

# 查看待发送通知
cat binance-*-notify.json
```

### 后台运行

#### 使用 nohup

```bash
nohup ./start-all.sh > monitor.log 2>&1 &

# 查看进程
ps aux | grep -E "(monitor|x-monitor).js"

# 停止进程
kill <PID>
```

#### 使用 screen

```bash
# 创建会话
screen -S binance-monitor

# 启动监控
./start-all.sh

# 退出屏幕（保持运行）
Ctrl+A, D

# 重新连接
screen -r binance-monitor

# 停止监控
Ctrl+C
```

#### 使用 systemd（生产环境）

创建服务文件 `/etc/systemd/system/binance-monitor.service`：

```ini
[Unit]
Description=Binance Monitor (Announce + X)
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/binance-announce-monitor
ExecStart=/bin/bash ./start-all.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable binance-monitor
sudo systemctl start binance-monitor

# 查看状态
sudo systemctl status binance-monitor

# 查看日志
sudo journalctl -u binance-monitor -f
```

---

## 📬 通知格式

### 公告通知

```
📢 **币安新公告**

**{公告标题}**

{公告摘要}

👉 [查看详情](https://www.binance.com/en/support/announcement/{id})
```

### X 账号动态通知

```
🐦 **币安 X 动态**

**{账号名称}**

{推文内容}

👉 [查看推文](https://twitter.com/{account})
```

### 示例

**公告通知：**
```
📢 **币安新公告**

**Binance Will List XXX (XXX) with Seed Tag Applied**

Binance will list XXX (XXX) and open trading for XXX/BTC, XXX/USDT, XXX/BNB, XXX/FDUSD and XXX/TRY trading pairs at 2024-03-15 10:00 (UTC).

👉 [查看详情](https://www.binance.com/en/support/announcement/12345678)
```

**X 动态通知：**
```
🐦 **币安 X 动态**

**Binance 英文**

🚀 Binance will list new tokens! Trading opens at 2024-03-15 10:00 UTC.

👉 [查看推文](https://twitter.com/binance)
```

---

## 📁 文件说明

### 核心文件

| 文件 | 说明 | 大小 |
|------|------|------|
| `monitor.js` | 公告监控脚本 | ~5KB |
| `x-monitor.js` | X 账号监控脚本 | ~6KB |
| `start-all.sh` | 一键启动全部监控 | ~1KB |
| `start.sh` | 启动公告监控 | ~1KB |
| `SKILL.md` | 完整技能文档 | ~4KB |
| `README.md` | 本文件，快速入门指南 | ~10KB |

### 配置文件

| 文件 | 说明 | 是否必需 |
|------|------|----------|
| `config.json` | 运行时配置 | 否（使用默认值） |
| `config.example.json` | 配置示例 | 否 |
| `package.json` | Node.js 项目配置 | 是 |

### 自动生成的文件

| 文件 | 说明 | 清理建议 |
|------|------|----------|
| `binance-announce-state.json` | 已读公告状态 | 自动维护（保留 100 条） |
| `binance-x-state.json` | 已读 X 动态状态 | 自动维护（保留 200 条） |
| `binance-pending-notify.json` | 待发送通知队列 | 自动清空 |
| `binance-x-notify.json` | X 待发送通知队列 | 自动清空 |
| `binance-sent-ids.json` | 已发送记录 | 自动维护（保留 100 条） |

---

## 🔧 高级配置

### 修改检查频率

**公告监控：** 编辑 `monitor.js`

```javascript
const CONFIG = {
    checkIntervalMs: 30000,  // 改为 60000 即 1 分钟
    // ...
};
```

**X 账号监控：** 编辑 `x-monitor.js`

```javascript
const CONFIG = {
    checkIntervalMs: 60000,  // 改为 120000 即 2 分钟
    // ...
};
```

⚠️ **注意**: 不建议设置为低于 10 秒，可能触发 API 限流。

### 添加其他 X 账号

编辑 `x-monitor.js` 中的 `CONFIG.accounts`：

```javascript
const CONFIG = {
    accounts: [
        {
            id: 'binance',
            name: 'Binance 英文',
            url: 'https://r.jina.ai/twitter/binance',
            lang: 'en'
        },
        {
            id: 'binancezh',
            name: 'Binance 中文',
            url: 'https://r.jina.ai/twitter/binancezh',
            lang: 'zh'
        },
        {
            id: 'cz_binance',
            name: 'CZ',
            url: 'https://r.jina.ai/twitter/cz_binance',
            lang: 'en'
        }
    ]
};
```

### 添加其他通知渠道

修改通知函数，支持：

- Telegram Bot
- Discord Webhook
- 微信企业机器人
- 邮件通知

### 监控其他交易所

创建独立的监控脚本：

```javascript
// okx-monitor.js
const OKX_ANNOUNCE_URL = 'https://www.okx.com/api/v5/support/announcements';

// bybit-monitor.js
const BYBIT_ANNOUNCE_URL = 'https://api.bybit.com/spot/v1/announcement';
```

---

## 🐛 故障排除

### 无法获取公告

**症状**: 日志显示 "网络请求失败" 或 "JSON 解析失败"

**解决方法**:

```bash
# 测试 API 连通性
curl -s "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=5&catalogId=48" | head

# 检查网络连接
ping www.binance.com

# 检查 Node.js 版本
node -v  # 需要 >= 18.0.0
```

### 无法获取 X 动态

**症状**: 日志显示 X 账号检查失败

**解决方法**:

```bash
# 测试 Jina AI API
curl -s "https://r.jina.ai/twitter/binance" | head -20

# 检查网络连接
ping r.jina.ai
```

### 通知未发送

**症状**: 检测到新内容但未收到飞书消息

**解决方法**:

```bash
# 检查通知队列
cat binance-*-notify.json

# 检查已发送记录
cat binance-sent-ids.json

# 查看运行日志
tail -f monitor.log

# 重启监控
ps aux | grep -E "(monitor|x-monitor).js
kill <PID>
./start-all.sh
```

### 重复通知

**症状**: 同一条内容收到多次通知

**解决方法**:

```bash
# 删除状态文件重置
rm binance-announce-state.json
rm binance-x-state.json
rm binance-sent-ids.json

# 重新启动
./start-all.sh
```

### 内存占用过高

**症状**: 进程内存持续增长

**解决方法**:

```bash
# 定期重启（添加到 crontab）
0 0 * * * pkill -f "node monitor.js" && pkill -f "node x-monitor.js" && cd /path/to/skill && ./start-all.sh &
```

---

## 🔒 安全说明

### API 限流

- 币安公告 API 为公开接口，无需 API Key
- X 账号使用 Jina AI Reader API（免费，无需认证）
- 建议检查间隔 >= 30 秒（公告）和 >= 60 秒（X）
- 过高的请求频率可能导致 IP 被临时限制

### 数据安全

- 状态文件存储在本地，不包含敏感信息
- 通知队列文件在发送后自动清空
- 建议定期清理历史状态文件

### 网络要求

- 需要能访问 `www.binance.com`
- 需要能访问 `r.jina.ai`（X 内容抓取）
- 如在中国大陆，可能需要代理配置

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 内存占用 | ~80MB（双监控） |
| CPU 占用 | < 2% |
| 网络请求 | 每 30 秒 1 次（公告）+ 每 60 秒 2 次（X 账号） |
| 响应延迟 | < 2 秒（检测到通知） |
| 状态文件大小 | < 20KB（300 条记录） |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/your-repo/binance-announce-monitor.git
cd binance-announce-monitor

# 安装依赖（如有）
npm install

# 运行测试
npm test

# 本地调试
./start-all.sh
```

### 代码规范

- 使用 ES6+ 语法
- 添加必要的注释
- 保持代码简洁
- 提交前运行测试

---

## 📝 版本历史

### v1.1.0 (2026-03-12)

- ✨ 新增 X（Twitter）账号监控功能
- ✨ 支持监控 @binance 和 @binancezh 两个账号
- 🐦 使用 Jina AI Reader API 抓取 X 内容
- 📝 简化 X 动态通知格式
- 📄 更新文档和配置文件

### v1.0.0 (2026-03-12)

- ✨ 初始版本发布
- ✅ 支持币安公告实时监控
- ✅ 支持飞书通知
- ✅ 状态持久化
- ✅ 后台运行支持

---

## 📄 许可证

MIT License

Copyright (c) 2026 OpenClaw Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📞 联系方式

- **项目主页**: https://github.com/your-repo/binance-announce-monitor
- **问题反馈**: https://github.com/your-repo/binance-announce-monitor/issues
- **OpenClaw 文档**: https://docs.openclaw.ai
- **ClawHub**: https://clawhub.ai

---

<div align="center">

**Made with ❤️ by OpenClaw Community**

[⭐ Star on GitHub](https://github.com/your-repo/binance-announce-monitor) | [📦 View on ClawHub](https://clawhub.ai)

</div>
