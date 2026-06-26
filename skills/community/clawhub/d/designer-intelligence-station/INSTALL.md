# 设计师情报站 - 安装与运行指南

## ⚠️ 安全声明

**在首次运行前，请阅读以下安全说明：**

### 安全承诺

本技能**仅抓取公开内容**，承诺：
- ❌ **不登录** - 不需要任何账号
- ❌ **不提交表单** - 不会与网站交互
- ❌ **不绕过付费墙** - 只访问公开页面
- ❌ **不存储敏感数据** - 所有数据本地保存
- ✅ **仅公开 URL** - 所有监测源都是公开网站

### 监测源审查

首次运行前，请审查 `data/default_sources.json` 中的所有 URL，确认都是你信任的公开站点。

```bash
# 查看所有监测源
cat data/default_sources.json | grep '"url"'

# 按类别查看
python3 tools/sources_manager.py list
```

---

## 📦 安装步骤

### 方式一：从 ClawHub 安装（推荐）

```bash
# 安装技能
clawhub install designer-intelligence-station

# 进入技能目录
cd ~/.clawhub/skills/designer-intelligence-station

# 安装 Python 依赖
pip install -r requirements.txt

# 初始化数据库
python3 data/import_sources.py

# 验证安装
python3 tools/sources_manager.py list
```

### 方式二：手动安装

```bash
# 克隆或下载技能到本地
cd ~/openclaw/workspace/skills/designer-intelligence-station

# 安装 Python 依赖
pip install -r requirements.txt

# 初始化数据库
python3 data/import_sources.py
```

---

## 🔧 依赖说明

### Python 依赖

所有依赖都是标准库或知名开源包：

```txt
feedparser>=6.0.0      # RSS/Atom 解析（BSD 许可）
requests>=2.28.0       # HTTP 请求（Apache 2.0）
beautifulsoup4>=4.11.0 # HTML 解析（MIT 许可）
lxml>=4.9.0            # XML/HTML 解析（BSD 许可）
python-dateutil>=2.8.2 # 日期解析（Apache 2.0）
```

**安装命令**：
```bash
pip install -r requirements.txt
```

### 系统依赖

- Python 3.10+
- SQLite 3（Python 内置）
- 网络连接（访问公开网站）

**无需**：
- ❌ 浏览器自动化
- ❌ 外部 API 密钥
- ❌ 登录凭证

---

## 🚀 运行模式

### 模式一：手动触发（推荐首次使用）

**首次运行建议使用手动模式**，检查输出是否正常。

```bash
# 生成日报
./execute_daily.sh

# 或手动请求
# "请生成今日的设计师情报日报"
```

**检查输出**：
1. 情报来源是否都是公开网站
2. 链接是否可正常访问
3. 内容是否符合预期

### 模式二：定时自动化（可选）

确认手动模式正常后，可配置定时任务：

```bash
# 配置 cron（每日早上 8 点）
crontab -e

# 添加以下行
0 8 * * * cd ~/.clawhub/skills/designer-intelligence-station && ./execute_daily.sh
```

**注意**：
- 不要立即开启自动化
- 先手动运行 1-2 次确认正常
- 监控网络活动和输出质量

---

## 📊 数据流向

### 抓取流程

```
公开网站 (RSS/API/Web)
    ↓
Python 脚本 (requests/feedparser)
    ↓
本地 JSON 缓存 (data/cache/)
    ↓
合并去重 (tools/fetch_all.py)
    ↓
SQLite 数据库 (data/intelligence_sources.db)
    ↓
Agent 筛选和格式化
    ↓
本地 Markdown 文件 (temp/)
    ↓
发送给用户（通过 ClawHub 消息通道）
```

### 数据保留

- ✅ **所有数据本地存储** - 不发送到外部服务
- ✅ **缓存可清理** - `data/cache/` 目录可随时删除
- ✅ **数据库可重建** - 从 `default_sources.json` 重新导入

---

## 🔒 安全监控

### 网络活动监控

```bash
# 监控出站连接（Linux）
sudo netstat -tnp | grep python

# 或使用更详细的工具
sudo tcpdump -i any -n port 80 or port 443
```

### 允许的域名

所有抓取的域名都在 `data/default_sources.json` 中列出，包括：
- 科技媒体：36kr.com, huxiu.com, ifanr.com 等
- 设计媒体：dezeen.com, smashingmagazine.com 等
- 社交平台：weibo.com, bilibili.com 等（需配置）

**不会访问**：
- ❌ 需要登录的网站
- ❌ 付费墙后的内容
- ❌ 私有/内部系统

---

## 🛠️ 故障排查

### 问题 1：依赖安装失败

```bash
# 检查 Python 版本
python3 --version  # 需要 3.10+

# 升级 pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt --force-reinstall
```

### 问题 2：抓取失败

```bash
# 测试单个源
python3 tools/web_fetcher_standalone.py fetch CN004

# 检查网络连接
curl -I https://www.ifanr.com/
```

### 问题 3：数据库错误

```bash
# 重新初始化
rm data/intelligence_sources.db
python3 data/import_sources.py
```

---

## 📝 版本信息

| 文件 | 版本 | 说明 |
|------|------|------|
| `SKILL.md` | 1.5.2 | 技能描述 |
| `_meta.json` | 1.5.2 | 元数据 |
| `package.json` | 1.5.2 | 包信息 |
| `requirements.txt` | 1.5.2 | Python 依赖 |

**所有文件版本已同步至 1.5.2**

---

## 📞 支持

- **文档**: `docs/` 目录
- **示例**: `EXAMPLES.md`
- **更新日志**: `CHANGELOG.md`
- **安全说明**: 本文档

---

*最后更新：2026-03-24 | 设计师情报站 v1.5.2*
