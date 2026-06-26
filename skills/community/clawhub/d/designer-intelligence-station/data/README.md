# 设计师情报站 · 数据文件说明

本目录包含信息源数据库和相关工具，用于情报抓取和管理。

---

## 📁 文件清单

### 核心数据

| 文件 | 说明 | 大小 | 必需 |
|------|------|------|------|
| `intelligence_sources.db` | SQLite 数据库（主数据库） | ~32KB | ✅ |
| `default_sources.json` | ClawHub 分发版配置（精简） | ~9KB | ✅ |
| `sources_export.json` | 完整导出（含所有字段） | ~10KB | ⚠️ 可选 |

### 工具脚本

| 文件 | 说明 | 用途 |
|------|------|------|
| `import_sources.py` | 信息源导入工具 | 从 ClawHub 下载后初始化数据库 |
| `sources_manager.py` | 信息源管理工具 | 增删改查、导出导入 |
| `rss_fetcher.py` | RSS 抓取器 | 抓取 RSS 源 |
| `api_fetcher.py` | API 抓取器 | 抓取 GitHub/Product Hunt 等 |
| `web_fetcher.py` | Web 抓取器 | 抓取网页内容 |
| `fetch_all.py` | 统一抓取入口 | 合并所有来源 |

### 缓存

| 目录 | 说明 |
|------|------|
| `cache/` | 临时缓存目录（RSS/API 抓取结果） |

---

## 🚀 快速开始

### 从 ClawHub 下载后初始化

```bash
# 1. 进入技能目录
cd skills/designer-intelligence-station

# 2. 导入信息源数据库
python data/import_sources.py

# 3. 验证导入
python tools/sources_manager.py list
```

### 查看信息源

```bash
# 列出所有信息源
python tools/sources_manager.py list

# 按抓取方式筛选
python tools/sources_manager.py list web    # Web 抓取
python tools/sources_manager.py list rss    # RSS
python tools/sources_manager.py list api    # API

# 按领域筛选
python tools/sources_manager.py list 设计    # 设计领域
```

### 添加新信息源

```bash
# 手动添加
python tools/sources_manager.py add <id> <name> <url> <type> <domain>

# 示例：添加设计博客
python tools/sources_manager.py add DS007 "Design Blog" "https://example.com" "设计媒体" "设计"
```

### 禁用/启用信息源

```bash
# 禁用
python tools/sources_manager.py disable CN001

# 启用
python tools/sources_manager.py enable CN001
```

### 导出/备份

```bash
# 导出为 JSON
python tools/sources_manager.py export > backup.json

# 从备份导入
python data/import_sources.py backup.json
```

---

## 📊 数据库结构

### sources 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | TEXT | 唯一标识（如 `DS001`） |
| `name` | TEXT | 名称 |
| `url` | TEXT | 网址/RSS/API 链接 |
| `type` | TEXT | 类型（兼容字段） |
| `domain` | TEXT | 领域（AI/手机/硬件/设计） |
| `priority` | TEXT | 优先级（高/中/低） |
| `status` | TEXT | 状态（enabled/disabled） |
| `update_frequency` | TEXT | 更新频率 |
| `notes` | TEXT | 备注 |
| `fetch_method` | TEXT | **抓取方式（web/rss/api）** |
| `category` | TEXT | **分类（中文媒体/设计媒体等）** |
| `created_at` | TEXT | 创建时间 |
| `updated_at` | TEXT | 更新时间 |

---

## 🔧 维护建议

### 定期检查

1. **每月检查失效源**
   ```bash
   # 查看错误日志
   cat temp/dis_daily/*.log 2>/dev/null | grep "错误\|失败"
   ```

2. **更新域名变更**
   ```bash
   # 修改网址
   python tools/sources_manager.py update CN007 --url "https://new-domain.com"
   ```

3. **备份数据库**
   ```bash
   # 导出备份
   python tools/sources_manager.py export > data/backup_$(date +%Y%m%d).json
   ```

### 版本控制

- ✅ `default_sources.json` - 应提交到 Git（ClawHub 分发）
- ✅ `sources_export.json` - 应提交到 Git（完整备份）
- ❌ `intelligence_sources.db` - 二进制文件，不提交（可从 JSON 重建）
- ❌ `cache/` - 临时缓存，不提交

---

## 📝 信息源分类

### 抓取方式

| 方式 | 数量 | 说明 |
|------|------|------|
| `web` | 21 | 网页抓取（需要解析 HTML） |
| `rss` | 6 | RSS 订阅源 |
| `api` | 4 | API 接口（GitHub/Product Hunt 等） |

### 领域分布

| 领域 | 数量 | 典型源 |
|------|------|--------|
| 设计 | 13 | Dezeen, UX Collective, Sidebar |
| AI | 15 | 机器之心，TechCrunch, GitHub |
| 手机 | 10 | 9to5Mac, IT 之家，爱范儿 |
| 硬件 | 8 | 大疆，影石，Product Hunt |

---

## 🆘 故障排查

### 问题：导入失败

```bash
# 检查数据库文件权限
ls -la data/intelligence_sources.db

# 删除重建
rm data/intelligence_sources.db
python data/import_sources.py
```

### 问题：抓取失败

```bash
# 检查信息源状态
python tools/sources_manager.py list | grep "❌"

# 手动测试单个源
curl -I "https://example.com"
```

### 问题：数据丢失

```bash
# 从备份恢复
python data/import_sources.py data/sources_export.json
```

---

## 📞 支持

- 技能作者：梨然 - 阿里版
- 版本：v1.4.1
- 最后更新：2026-03-24
