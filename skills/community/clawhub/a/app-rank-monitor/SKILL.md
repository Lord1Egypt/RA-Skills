# App Rank Monitor - 应用榜单监控 Skill

> **版本**: v5.0  
> **创建时间**: 2026-03-17  
> **更新时间**: 2026-03-24 (移除下架检测功能)  
> **状态**: ✅ 完成

---

## 📋 技能说明

专注应用榜单爬取和数据统计

**核心功能**:
- ✅ 榜单爬取（苹果官方 RSS + 点点数据）
- ✅ 钉钉通知（文字 + 文件上传）
- ✅ 自动生成 Markdown 报告
- ✅ 数据管理（自动清理，保留 7 天）

---

## 📊 支持数据源

| 数据源 | 状态 | 说明 |
|--------|------|------|
| 🍎 苹果官方 RSS | ✅ | 免费榜/付费榜/新上架（总榜） |
| 📈 点点数据 | ⚠️ | 需 Cookie（官网注册，有效期 24 小时） |

---

## 🚀 使用方法

### 自然语言触发

直接对钳钳说：

```
- 查看今天的苹果榜单
- 爬取点点榜单
- 发送日报
- 清理过期数据
```

### 命令行（高级）

```bash
cd ~/.openclaw/workspace/skills/app-rank-monitor

# 爬取苹果榜单
python src/main.py apple-rank

# 爬取点点榜单
python src/main.py rank --platform diandian

# 查看统计
python tools/show_stats.py
```

---

## 📁 文件结构

```
app-rank-monitor/
├── src/
│   ├── main.py              # 主入口
│   ├── monitor.py           # 监控调度器
│   ├── rankers/             # 榜单爬虫
│   │   ├── apple_ranker.py  # 苹果 RSS
│   │   ├── diandian.py      # 点点数据
│   │   └── diandian_android.py  # 点点安卓渠道
│   ├── models/              # 数据模型
│   ├── notifiers/           # 通知发送
│   └── reporters/           # 报告生成
├── config/
│   ├── dingtalk.yaml        # 钉钉配置
│   ├── diandian.yaml        # 点点配置
│   └── ios_rank.yaml        # 苹果榜单配置
├── database/
│   └── apps.db              # SQLite 数据库
├── logs/                    # 日志文件
└── docs/                    # 文档
```

---

## 🔧 配置说明

### 钉钉配置

编辑 `config/dingtalk.yaml`:

```yaml
dingtalk:
  client_id: "你的企业应用 client_id"
  client_secret: "你的企业应用 client_secret"
  chat_id: "群聊 ID"
  webhook: "机器人 Webhook"
```

### 点点数据配置

编辑 `config/diandian.yaml`:

```yaml
diandian:
  cookie: "你的 Cookie（含 token）"
```

**获取 Cookie**:
1. 访问 https://www.diandian.com/
2. 登录账号
3. 按 F12 打开开发者工具
4. 刷新页面
5. 复制 Cookie 字符串

---

## 📅 定时任务

已配置定时任务：
- **每天 8:00** - 爬取 iOS 榜单并发送日报

查看任务状态：
```bash
openclaw cron list
```

---

## 🛠️ 常用命令

```bash
# 查看定时任务
openclaw cron list

# 手动触发爬取
openclaw cron run <task-id>

# 查看执行日志
cat logs/cron_execution.log

# 查看数据库统计
python tools/show_stats.py
```

---

## 📝 更新日志

### v5.0 (2026-03-24) - 移除下架检测功能
- ❌ 移除下架检测模块 (`src/detectors/`)
- ❌ 移除下架数据模型 (`OfflineAppRecord`, `AppleOfflineAlert`)
- ❌ 移除 `offline` 命令
- ❌ 移除 `--detect-offline` 参数
- ✅ 专注榜单爬取和日报生成

### v4.3 (2026-03-23) - 移除七麦数据
- ❌ 移除七麦数据爬虫 (`qimai_browser.py`)
- ❌ 移除七麦配置文件 (`config/qimai.yaml`)
- ❌ 移除日报中的七麦板块
- ✅ 专注点点数据和苹果官方 RSS

### v4.2 (2026-03-17)
- ✅ 优化定时任务配置
- ✅ 修复 delivery 问题

### v4.1 (2026-03-16)
- ✅ 集成点点数据自动登录
- ✅ 支持安卓 8 大渠道

### v4.0 (2026-03-15)
- ✅ 精简架构，移除冗余功能
- ✅ 优化日报生成逻辑

---

## 💡 故障排查

### Cookie 过期

**症状**: 日报无数据，收到告警通知

**解决**:
1. 重新登录点点数据官网
2. 复制新 Cookie 到 `config/diandian.yaml`
3. 手动触发：`python src/main.py rank --send-report`

### 定时任务未执行

**检查**:
```bash
openclaw cron list
openclaw cron runs --id <task-id>
```

---

## 📖 详细文档

- `docs/配置说明.md` - 详细配置指南
- `docs/定时任务配置说明.md` - 定时任务设置
- `docs/故障排查指南.md` - 常见问题解决

---

## 🦞 有问题？

随时问钳钳！
