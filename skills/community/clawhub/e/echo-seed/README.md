# Echo Seed / 回声种子

> 让每一个想法都有回声 🌱

简洁优雅的想法记录工具，支持快速记录、智能分类、时间线视图和多端同步。

## ✨ 特性

- 📝 **快速记录** - 一键创建，支持 8 种类型（笔记/灵感/链接/日记/思考/收藏/待办/语音）
- 🎨 **智能分类** - 自动标签、颜色编码、类型区分
- 📅 **时间线视图** - 按时间顺序浏览所有想法
- 🔍 **搜索筛选** - 全文搜索、类型过滤、标签筛选
- 📊 **统计面板** - 数据可视化、类型分布、趋势分析
- 🤖 **AI 增强** - 点子扩张、链接分析、智能关联（可选）
- 🔄 **多端同步** - Notion、Google Calendar、Telegram Bot

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/zheznanohana/echo-seed.git
cd echo-seed

# 安装依赖
pip install -r requirements.txt
```

### 启动服务

```bash
# 启动 Web 服务
python3 scripts/echo-web.py

# 访问
http://localhost:5000
```

### 配置（可选）

复制配置示例并编辑：

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml` 配置：
- 数据库路径
- Web 服务端口
- Notion API（同步用）
- Google Calendar（待办同步）

## 📱 Telegram Bot

通过 Bot 快速创建种子：

```bash
# 启动 Bot
python3 scripts/echo-telegram-bot.py
```

**支持的命令：**
- `/note` - 创建笔记
- `/idea` - 创建灵感
- `/link` - 创建链接
- `/todo` - 创建待办
- `/diary` - 创建日记
- `/thought` - 创建思考
- `/collect` - 创建收藏
- `/voice` - 创建语音
- `/list` - 查看最近种子
- `/search` - 搜索种子
- `/stats` - 统计信息

## 🤖 AI 功能

Echo Seed 支持 AI 增强功能：

- **点子扩张** - 输入简单想法，AI 扩展成完整方案
- **链接分析** - 输入 URL，AI 自动提取内容并总结
- **智能关联** - 自动发现相关种子，建立知识关联

详见：[README-AI.md](README-AI.md)

## 📦 数据库

使用 SQLite 存储，默认路径：`data/echo.db`

数据库会自动创建，包含以下表：
- `seeds` - 种子主表
- `seed_relations` - 种子关联表
- `seed_tags` - 种子标签表
- `ai_analyses` - AI 分析记录表

## 🔧 API

提供 REST API 供前端调用：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/seeds` | GET | 获取种子列表 |
| `/api/seeds` | POST | 创建种子 |
| `/api/seeds/<id>` | PUT | 更新种子 |
| `/api/seeds/<id>` | DELETE | 删除种子 |
| `/api/stats` | GET | 获取统计信息 |
| `/api/export/<format>` | GET | 导出数据 (json/csv/markdown) |
| `/api/seed/<id>/analyze/expand` | POST | AI 点子扩张 |
| `/api/seed/<id>/analyze/link` | POST | AI 链接分析 |
| `/api/seed/<id>/relations` | GET | 获取关联种子 |

## 🛠️ 技术栈

- **后端:** Python 3.10+, Flask
- **数据库:** SQLite
- **前端:** HTML, TailwindCSS, Vue 3 (CDN)
- **AI:** MiniMax API (兼容 Anthropic 格式)

## 📄 许可证

MIT License

---

**Echo Seed - 让每一个想法都有回声** 🌱
