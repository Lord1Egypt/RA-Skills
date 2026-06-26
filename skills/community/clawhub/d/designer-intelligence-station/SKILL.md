---
name: designer-intelligence-station
description: Designer intelligence collection tool. Monitors 46 public sources (AI/hardware/mobile/design), dynamic quality-based filtering v2.1.8, generates structured daily/weekly reports. All data stored locally.
version: 2.1.8
author: 梨然 - 阿里版
license: MIT

category: research
tags:
  - design
  - intelligence
  - news
  - ai
  - hardware
  - mobile
  - structured-output
  - trend-analysis
  - open-sources-only
  - auto-dependency-check
  - dynamic-filtering
  - screening-2.1.8

models:
  recommended:
    - qwen3.5-plus

capabilities:
  - intelligence_collection
  - news_filtering
  - daily_briefing
  - weekly_report
  - dependency_autoinstall
  - behavioral_screening

languages:
  - zh

related_skills: []
---

# 设计师情报站 v2.1.8

## 📋 使用说明

**数据本地存储**：所有抓取的数据保存在本地（`data/cache/` 和 `temp/` 目录），不发送到外部服务。

### 首次运行前步骤

**请务必完成以下检查：**

1. **审查监测源** - 确认都是你信任的公开站点
   ```bash
   cat data/default_sources.json | grep '"url"'
   ```

2. **手动运行测试** - 不要立即启用自动化
   ```bash
   ./execute_daily.sh
   ```

3. **检查输出** - 确认链接都来自公开页面

**完成上述检查后，再考虑启用定时自动化。**

---

## 功能

**监控 46 个公开信息源**，覆盖 AI、智能硬件、手机、设计四大领域：

- 📰 **中文媒体**（9 个）：36 氪、机器之心、量子位、爱范儿、少数派等
- 🎨 **设计媒体**（14 个）：Dezeen、It's Nice That、Behance、Dribbble、Design Week、Core77、AIGA Eye on Design、Fast Company、UX Collective 等
- 🌐 **英文媒体**（5 个）：The Verge、TechCrunch、Wired 等
- 📡 **RSS 源**（10 个）：TechCrunch RSS、The Verge RSS、Dezeen RSS、It's Nice That RSS、Design Week RSS、Core77 RSS、AIGA Eye on Design RSS 等
- 💬 **社区平台**（4 个）：GitHub Trending、Product Hunt 等
- 📱 **社交平台**（8 个，可选配置）：微博、B 站、知乎等

**输出格式**：
- 📊 结构化日报（v1.3.3 格式，表格 + 超链接）
- 📈 深度周报（趋势分析 + 竞品动态）

---

## 安装

```bash
# 1. 安装技能
clawhub install designer-intelligence-station

# 2. 进入目录
cd ~/.clawhub/skills/designer-intelligence-station

# 3. 安装依赖
pip install -r requirements.txt

# 4. 审查监测源（重要！）
cat data/default_sources.json | grep '"url"'

# 5. 初始化数据库
python3 data/import_sources.py

# 6. 手动测试运行
./execute_daily.sh
```

---

## 依赖

**Python 3.10+**，需要以下包（都是知名开源库）：

```txt
feedparser>=6.0.0      # RSS 解析（BSD）
requests>=2.28.0       # HTTP 请求（Apache 2.0）
beautifulsoup4>=4.11.0 # HTML 解析（MIT）
lxml>=4.9.0            # XML 解析（BSD）
python-dateutil>=2.8.2 # 日期解析（Apache 2.0）
```

**无需**：
- ❌ 浏览器自动化
- ❌ 外部 API 密钥
- ❌ 登录凭证

---

## 运行模式

### 模式一：手动触发（推荐）

```bash
./execute_daily.sh
```

或在对话中请求：
```
请生成今日的设计师情报日报
```

**执行流程**：
1. 自动检查 Python 版本（需要 3.10+）
2. 自动检查 Python 依赖包
3. 如有缺失，提示并自动安装
4. 执行情报抓取和生成

### 模式二：定时自动化（可选）

**仅在手动模式测试正常后启用**：

```bash
# 配置每日早上 8 点运行
crontab -e
# 添加：0 8 * * * cd ~/.clawhub/skills/designer-intelligence-station && ./execute_daily.sh
```

### 模式三：依赖检查（独立运行）

```bash
# 仅检查依赖，不执行抓取
python3 tools/check_dependencies.py
```

---

## 数据流向

```
公开网站（RSS/API/Web）
    ↓
Python 脚本（requests/feedparser）
    ↓
本地 JSON 缓存（data/cache/）
    ↓
合并去重（tools/fetch_all.py）
    ↓
SQLite 数据库（data/intelligence_sources.db）
    ↓
Agent 筛选和格式化
    ↓
本地 Markdown 文件（temp/）
    ↓
发送给用户（ClawHub 消息通道）
```

**所有数据本地存储**，不发送到外部服务。

---

## 监测源清单

完整列表见 `data/default_sources.json`，包括：

**科技媒体**：
- 36kr.com（36 氪）
- huxiu.com（虎嗅）
- ifanr.com（爱范儿）
- sspai.com（少数派）
- theverge.com（The Verge）
- techcrunch.com（TechCrunch）

**设计媒体**：
- dezeen.com（Dezeen）
- smashingmagazine.com（Smashing Magazine）
- uxdesign.cc（UX Collective）
- fastcompany.com（Fast Company）

**社区平台**：
- github.com/trending（GitHub Trending）
- producthunt.com（Product Hunt）

**社交平台**（可选，需额外配置）：
- weibo.com（微博）
- bilibili.com（B 站）
- zhihu.com（知乎）

---

## 筛选标准（v2.0 - 基于 120+ 条行为分析）

### 6 维筛选

| 维度 | 权重 | 说明 | 采用率 |
|------|------|------|--------|
| [1] 交互/视觉创新 | ⭐⭐⭐ | 专利（有创新）/新交互/视觉技术 | 100% |
| [2] 设计工具/资源 | ⭐⭐⭐ | 提升设计师效率的工具/资源 | 85% |
| [3] 深度分析/洞察 | ⭐⭐⭐ | 趋势/方法论/行业洞察 | 85% |
| [4] 大厂 AI/设计战略 | ⭐⭐ | 苹果/谷歌/华为的 AI 或设计发布 | 60% |
| [5] 设计作品/案例 | ⭐⭐ | 创意参考/趣味性/大厂案例 | 70% |
| [6] AI+ 设计工作流 | ⭐⭐⭐ | AI 工具/工作流创新 | 80% |

### 分级（维度组合）

| 等级 | 规则 | 目标占比 |
|------|------|---------|
| **S 级** | [1]+[3] 或 [1]+[6] 或 [3]+[6] | 10-15% |
| **A 级** | [1] 或 [2] 或 [3] 或 [6] | 40-50% |
| **B 级** | [4] 或 [5]（优质） | 30-40% |
| **C 级** | 纯资讯/市场数据/营销/教程/八卦 | 排除 |

**详细筛选指南**：见 `docs/screening-guide.md`

---

## 📋 输出格式规范（v1.6.0 - 强制约束）

### 核心要求

| 要求 | 说明 | 状态 |
|------|------|------|
| **每条情报必须有详情链接** | 表格必须包含「详情」列，格式为 `[→ 详情](完整 URL)` | 🔴 强制 |
| **周刊必须深度抓取** | Moonvy/优设网周刊必须进入详情页抓取完整内容，禁止仅输出 RSS 摘要 | 🔴 强制 |
| **趋势洞察必须有相关阅读** | 每个趋势洞察底部必须添加「📎 相关阅读」链接（2-3 条） | 🔴 强制 |
| **期数自动提取** | 周刊期数必须从 RSS 标题自动提取，禁止手动输入 | 🔴 强制 |

### 详情链接规范

**所有情报表格必须包含「详情」列**：

```markdown
| 公司/机构 | 事件 | 影响 | 来源 | 详情 |
| --- | --- | --- | --- | --- |
| 谷歌 | Stitch 更新 | 形成新规范 | 优设网 | [→ 详情](https://example.com) |
```

**禁止行为**:
- ❌ 表格缺少「详情」列
- ❌ 详情链接为空或占位符
- ❌ 趋势洞察无「相关阅读」链接
- ❌ 周刊仅输出 RSS 摘要（无具体内容）

### 周刊深度抓取规范

**适用周刊**（P0 优先级）:
| 周刊名称 | URL 规则 | 期数提取 |
|----------|---------|---------|
| Moonvy 设计素材周刊 | `https://moonvy.com/blog/post/设计素材周刊/{期数}/` | "设计素材周刊 206 期" → 206 |
| 优设网体验碎周报 | `https://www.ftium4.com/ux-weekly-{期数}.html` | "体验碎周报第 273 期" → 273 |

**抓取流程**:
```
1. 检测 RSS 中的周刊条目 → 2. 提取期数 → 3. 构建 URL → 4. web_fetch 抓取 → 5. 按栏目分类输出
```

**输出格式**:
```markdown
### 📖 Moonvy 设计素材周刊 206 期（深度抓取）
### 📖 优设网体验碎周报 273 期（深度抓取）
```

**详细规范**：见 `docs/format-spec.md`

---

## 📄 文档索引

| 文档 | 说明 |
|------|------|
| `docs/format-spec.md` | **输出格式规范 v1.6.0**（详情链接、周刊抓取、表格模板） |
| `docs/screening-guide.md` | 5 维筛选标准 v2.0（6 维筛选、分级规则、排除清单） |
| `docs/execution-flow.md` | 执行流程说明（含周刊深度抓取指南） |
| `docs/auto-send-guide.md` | 自动发送指南（含详情链接规范、周刊抓取执行规范） |
| `INSTALL.md` | 详细安装指南 |
| `CHANGELOG.md` | 更新日志 |

---

## 故障排查

### 依赖安装失败

```bash
python3 --version  # 需要 3.10+
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 抓取失败

```bash
# 测试单个源
python3 tools/web_fetcher_standalone.py fetch CN004

# 检查网络
curl -I https://www.ifanr.com/
```

### 数据库错误

```bash
rm data/intelligence_sources.db
python3 data/import_sources.py
```

---

## 文档

- **INSTALL.md** - 详细安装指南
- **QUICKSTART.md** - 快速入门
- **docs/** - 详细文档（筛选指南、配置说明等）
- **CHANGELOG.md** - 更新日志

---

## 版本历史

### v2.1.6 (2026-03-27) - 安全声明简化

**优化**：
- 简化安全声明，删除冗余承诺描述
- 保留核心说明：数据本地存储

---

### v2.1.5 (2026-03-27) - 动态分布策略

**新增**：
- **动态分布筛选器** — 根据内容质量动态调整各领域占比，不强制平衡
- **质量优先原则** — 优质内容多的领域多输出，优质内容少的领域少输出
- **工具**：`tools/dynamic_filter.py` — 动态筛选脚本

**策略变化**：
- ❌ 移除：强制领域均衡配置（上限/下限）
- ✅ 新增：质量评分系统（S/A+/A/B 级，1-5 分）
- ✅ 新增：动态筛选（达到最小值后只采用 3 分以上内容）

**优势**：
- 反映真实新闻分布
- 不错过重要事件
- 避免为了平衡而降低标准

**文档**：
- 更新 `docs/screening-guide.md` — 动态分布策略 v2.1.5

---

### v2.1.4 (2026-03-27) - 领域均衡配置（已废弃）

**备注**：此版本尝试强制均衡各领域比例，但发现不合理（新闻本身不是均匀分布的），已在 v2.1.5 改为动态分布策略。

---

### v2.1.3 (2026-03-27) - 设计/审美信息源扩展

**新增监测源**（6 个设计媒体 + 4 个 RSS）：

**设计媒体**：
- ✅ It's Nice That — 平面设计/创意作品/视觉文化
- ✅ Behance — 全球设计师作品集热门榜单
- ✅ Dribbble — UI/平面/插画设计社区
- ✅ Design Week — 英国设计周（平面/产品/数字设计）
- ✅ Core77 — 工业设计权威媒体
- ✅ AIGA Eye on Design — 美国平面设计协会官方媒体

**RSS 源**：
- ✅ It's Nice That RSS
- ✅ Design Week RSS
- ✅ Core77 RSS
- ✅ AIGA Eye on Design RSS

**总计**：监测源从 40 个 → 46 个，设计类从 8 个 → 14 个

**影响**：
- 审美提升类内容覆盖率显著提升
- 新增平面设计/工业设计/视觉文化垂直领域
- Behance/Dribbble 提供实时设计趋势参考

---

### v2.1.2 (2026-03-27) - 审美提升内容权重优化

**优化**：
- **维度 [1] 扩展** - 交互/视觉创新 → 交互/视觉/**审美**创新（新增配色/排版/视觉趋势）
- **维度 [5] 升级** - 设计作品/案例 → 设计作品/**审美参考**，权重 ⭐⭐ → ⭐⭐⭐
- **采用率提升** - 维度 [5] 采用率 70% → 85%，与工具/洞察同级
- **分级规则调整** - A 级新增「[5]（知名/高讨论度）」，S 级新增「[1]+[5]（知名作品）」

**新增筛选标准**：
- ✅ 知名设计师作品（原研哉/深泽直人/Jony Ive 等）
- ✅ 高讨论度作品（Behance/Dribbble 热门榜单）
- ✅ 设计奖项作品（Red Dot/iF/IDEA 获奖）
- ✅ 审美趋势分析（年度配色/排版趋势/视觉风格）

**排除优化**：
- ❌ 普通设计师日常作品（无知名度/讨论度）
- ❌ 单一海报展示无分析（纯展示，无洞察）

**文档**：
- 更新 `docs/screening-guide.md` - 6 维筛选标准 v2.1（审美参考权重提升）

**影响**：
- 审美提升类内容占比目标：20-30%
- 设计领域板块将有更多知名作品/奖项/趋势内容

---

### v2.1.1 (2026-03-26) - 输出格式规范重大升级

**新增**：
- **详情链接强制规范** - 每条情报必须提供「详情」超链接入口
- **周刊深度抓取规范** - Moonvy/优设网周刊必须进入详情页抓取完整内容
- **趋势洞察相关阅读** - 每个趋势必须添加 2-3 条相关阅读链接
- **期数自动提取** - 从 RSS 标题自动提取周刊期数，构建详情页 URL

**文档**：
- 新增 `docs/format-spec.md` - 输出格式规范 v1.6.0（统一规范文档）
- 更新 `docs/auto-send-guide.md` - 详情链接规范 + 周刊深度抓取执行规范
- 更新 `docs/execution-flow.md` - 周刊深度抓取指南
- 更新 `docs/screening-guide.md` - 周刊深度抓取规范

**约束**：
- 🔴 强制：所有情报表格必须包含「详情」列
- 🔴 强制：禁止仅输出周刊 RSS 摘要（必须深度抓取）
- 🔴 强制：趋势洞察必须包含「📎 相关阅读」链接

**示例**：
```markdown
| 公司/机构 | 事件 | 影响 | 来源 | 详情 |
|----------|------|------|------|------|
| 谷歌 | Stitch 更新 | 形成新规范 | 优设网 | [→ 详情](链接) |
```

---

### v2.0.0 (2026-03-25) - 筛选标准重大升级
- **重构**：6 维筛选标准 v2.0（基于 120+ 条历史情报行为分析）
- **新增**：[1] 交互/视觉创新维度（专利/新交互/视觉技术）
- **新增**：[6] AI+ 设计工作流维度（AI 工具/工作流创新）
- **优化**：分级规则量化（S 级：[1]+[3] 或 [1]+[6] 或 [3]+[6]）
- **新增**：排除清单（9 类明确排除内容）
- **新增**：边界情况判断流程
- **文档**：`docs/screening-guide.md` 详细指南

### v1.6.0 (2026-03-25)
- **新增**：依赖自动检测和安装功能
- **新增**：`tools/check_dependencies.py` - 依赖检查工具
- **优化**：`execute_daily.sh` 在执行前自动检查依赖
- **优化**：缺失依赖时自动提示并安装，无需手动干预

### v1.5.3 (2026-03-24)
- 修复：安全声明前置，首次运行前必读
- 新增：监测源审查步骤
- 优化：简化描述，突出安全承诺

### v1.5.2 (2026-03-24)
- 新增：DS007 体验碎周报专栏

### v1.5.1 (2026-03-24)
- 新增：独立网页抓取器（qclaw 适配）
- 优化：全自动执行流程

---

## 许可证

MIT License - 免费使用、修改和分发。

---

*Last updated: 2026-04-03 | Designer Intelligence Station v2.1.8*
