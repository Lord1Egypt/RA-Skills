# Design Inspiration Collector

🎨 双平台设计灵感收集技能（Dribbble + Pinterest）

**版本**：v2.1.0
**作者**：benson126

---

## 功能特点

- ✅ **双平台搜索**：Dribbble + Pinterest（已移除 Behance）
- ✅ **URL 白名单**：只取**官方搜索/标签/大搜索页**，不混入个人作品集与个人画板
- ✅ **Pinterest 大搜索优先**：使用 `/search/pins/?q=...` 构造，对应日常搜索体验（含顶部筛选标签）
- ✅ **智能去重**：当 topic 已含某关键词时不重复追加（避免 `app+app+design` 之类 URL）
- ✅ **趋势分析 + 推荐方向**：自动提取趋势摘要，给出细分推荐

---

## 触发词

`找灵感` `收集灵感` `设计参考` `UI参考` `视觉灵感` `设计趋势` `Dribbble` `Pinterest`

---

## 工作流程

1. 接收主题（如 "医疗 App"）
2. **Dribbble**：用 Tavily 搜索 → 过滤为 `/search/` 或 `/tags/` 页面（5 条）
3. **Pinterest**：直接构造 5 个不同切面的大搜索 URL（5 条）
   - `{topic} ui design`
   - `{topic} mobile ui`
   - `{topic} dashboard`
   - `{topic} concept`
   - `{topic} inspiration`
4. 输出 Markdown 报告 + JSON 数据

---

## URL 白名单

### Dribbble
- ✅ `dribbble.com/search/...`
- ✅ `dribbble.com/tags/...`
- ❌ 个人作品集 / 单个作品页

### Pinterest
- 🥇 **首选** `pinterest.com/search/pins/?q=...`（大搜索，与日常搜索体验一致）
- 🥈 备选 `pinterest.com/ideas/...`（编辑策展页）
- ❌ 个人画板 / 单个图钉详情

---

## 安装与配置

### 1. 通过 ClawHub 安装

```bash
openclaw skills install design-inspiration-collector
```

### 2. 设置环境变量

```bash
export TAVILY_API_KEY="tvly-你的key"
```

获取 Tavily API Key：https://app.tavily.com/

### 3. 安装 Python 依赖

```bash
pip3 install tavily-python
```

---

## 直接调用脚本（测试）

```bash
python3 scripts/design_collector.py "healthcare app"
```

输出位于 `~/design_inspirations/` 目录：
- `{关键词}_{时间戳}.md` — Markdown 报告
- `{关键词}_{时间戳}.json` — 结构化数据（供 LLM 后续整理）

---

## 文件结构

```
design-inspiration-collector/
├── _meta.json            # ClawHub 平台元数据
├── skill.yaml            # skill 元数据
├── SKILL.md              # 主指令（Claude 加载入口）
├── README.md             # 本文件
└── scripts/
    └── design_collector.py   # 搜索 + 过滤 + 输出脚本
```

---

## 更新日志

### v2.1.0 (2026-05-21)
- 🎯 **Pinterest 改为大搜索优先**：从 `/ideas/...` 切换到 `/search/pins/?q=...`，对应用户日常搜索体验
- 🔧 修复 URL 关键词重复问题（如 `app+app+design`）
- 📝 更新 SKILL.md 中 Pinterest URL 优先级说明

### v2.0.0 (2026-05-21)
- 🗑️ 移除 Behance（精简平台聚焦双平台）
- 🛡️ 新增 URL 白名单过滤：禁止个人作品集、画板、单个作品页
- 🔧 新增标准搜索 URL 构造作为兜底方案
- 🗑️ 移除 Playwright 截图功能（精简依赖）
- 🗑️ 移除腾讯文档输出（改为本地 Markdown）
- 🔒 修复硬编码 API Key 问题（强制从环境变量读取）
- 🔒 修复输出路径问题（`/root/...` → `~/design_inspirations`）

### v1.0.2 (初始版本)
- 包含 Behance、Dribbble、Pinterest 三平台
- 集成 Playwright 截图 + 腾讯文档上传

---

## 已知限制

1. Tavily 免费额度 1000 次/月
2. Dribbble 依赖 Tavily 搜索质量；Pinterest 是直接构造无依赖
3. 不抓取页面缩略图，只输出链接

---

## License

MIT-0
