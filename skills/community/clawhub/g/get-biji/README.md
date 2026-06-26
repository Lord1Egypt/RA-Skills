# Get 笔记自动同步

24/7 录音卡 → [Get 笔记](https://biji.com) AI 转录 → 本地 Markdown 归档。

## 功能

- 自动同步 Get 笔记到本地 Markdown 文件
- 智能分类（客户、会议、灵感、待办、复盘、选题）
- 章节标题自动注入原文转录
- 长录音原文自动分离为独立文件
- 增量同步，跳过已同步的笔记
- 静默刷新认证，约 90 天无需手动登录

## 快速开始

```bash
# 安装依赖
npm install

# 首次运行（会弹出浏览器登录 biji.com）
OUTPUT_DIR="/你的输出目录" node scripts/sync.js

# 测试模式（只同步 2 条）
OUTPUT_DIR="/你的输出目录" TEST_LIMIT=2 node scripts/sync.js
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OUTPUT_DIR` | 输出目录 | `./notes` |
| `SINCE_DATE` | 起始日期过滤 | `2026-01-01` |
| `TEST_LIMIT` | 测试模式，限制同步条数 | `0`（全部） |

## 输出结构

```
Get笔记/
  2026-03/
    2026-03-01_客户_AI搜索优化业务合作洽谈.md          ← 摘要（短录音原文内嵌）
    2026-03-01_客户_AI搜索优化业务合作洽谈_原文.md      ← 原文转录（长录音自动分离）
  2026-02/
    2026-02-28_会议_团队周会纪要.md
    ...
```

**分类规则：** `classifyNote()` 根据录音类型、时长、关键词自动判断：

| 分类 | 触发条件 |
|------|----------|
| 客户 | 含"客户""报价""需求""合作"等关键词 |
| 会议 | 录音>10分钟，或含"会议""讨论""培训" |
| 灵感 | 短录音(<3分钟)的默认分类 |
| 待办 | 含"待办""记得""要做""明天" |
| 复盘 | 含"复盘""反思""总结" |
| 选题 | 含"选题""文章""内容""课程" |

## 认证机制

三级认证链，优先使用缓存，尽量避免弹浏览器：

1. **JWT 缓存**（30分钟有效）→ 直接使用
2. **refresh_token 静默刷新**（~90天有效）→ 后台自动刷新
3. **Playwright 浏览器登录**（最后手段）→ 弹出浏览器手动登录

首次运行需要登录一次，之后约 90 天内全自动。

## 文件说明

### 脚本

| 文件 | 说明 |
|------|------|
| `scripts/sync.js` | 主同步脚本（调度器） |
| `scripts/api.js` | 认证 + API 请求 |
| `scripts/format.js` | 格式化 + 分类 + 章节注入 |
| `scripts/rebuild-state.js` | 从 API 重建同步状态（丢失状态文件时用） |
| `scripts/dedupe.js` | 去重工具 |

### 状态文件（自动生成，已在 .gitignore 中）

| 文件 | 说明 |
|------|------|
| `.sync-state.json` | 已同步的 note_id 列表 |
| `.token-cache.json` | JWT + refresh_token 缓存 |
| `.auth-state.json` | Playwright 浏览器登录状态 |

## 架构

```
sync.js (调度器)
  ├── api.js (认证 + 数据获取)
  │   ├── JWT 缓存管理
  │   ├── refresh_token 静默刷新
  │   └── Playwright 浏览器登录（兜底）
  └── format.js (内容处理)
      ├── classifyNote() — 智能分类
      ├── parseChapters() — 解析章节时间戳
      ├── buildTranscript() — 构建带章节标题的原文
      └── buildSummaryMarkdown() — 生成摘要 Markdown
```
