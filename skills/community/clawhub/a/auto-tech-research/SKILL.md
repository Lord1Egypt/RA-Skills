---
name: auto-tech-research
description: |
  全自动化技术深度调研 Skill。通过 Chrome DevTools Protocol 操控浏览器，
  模拟真人搜索行为，在国内外主流平台检索内容，确保搜索结果与人工操作一致。
  输出 HTML 格式的结构化调研报告。

  核心原则：
  - 不使用 web_fetch，全程使用 browser（CDP 协议）
  - 搜索行为与真人一致：打开搜索引擎 → 输入关键词 → 浏览结果 → 打开链接 → 提取内容
  - 每个平台的获取状态透明输出（成功/失败/原因）

  触发词：
  - "全面调研一下 [技术]"
  - "深度研究 [技术]"
  - "技术全景分析：[技术]"

metadata:
  version: "4.0.0"
  author: "OpenClaw"
  tags: ["research", "analysis", "auto", "browser"]
  always: false
---

# 自动化技术深度调研 Skill v4.0

## 核心变更（v4.0）

**v3.0 → v4.0 最大变化：全面弃用 web_fetch，改用 browser（CDP 协议）**

| 维度 | v3.0 | v4.0 |
|------|------|------|
| **搜索工具** | web_fetch 优先，browser 降级 | **browser 唯一工具** |
| **搜索体验** | 程序式 HTTP 请求 | **模拟真人浏览器操作** |
| **JS 渲染** | 不支持 | **完整支持** |
| **登录态** | 不支持 | **支持（chrome-relay）** |
| **反爬绕过** | 经常 403 | **与真人一致，极少被拦** |
| **搜索结果** | API 返回格式 | **与人工搜索完全一致** |

## 工作流程概览

```
输入技术主题（+ 可选的用户补充链接）
    ↓
[Phase 1] 关键词扩展（中英双语）
    ↓
[Phase 2] 平台相关性评估 + 动态数量分配
    ↓
[Phase 3] 浏览器搜索（CDP 操控，模拟真人）
    ├─ 启动浏览器（独立 openclaw 实例 或 chrome-relay）
    ├─ 逐平台搜索：打开搜索页 → 输入关键词 → 获取结果列表
    ├─ 逐条打开：点击链接 → 等待加载 → snapshot 提取内容
    ├─ 记录每个平台的获取状态和原因
    └─ 用户补充链接：直接 navigate → snapshot
    ↓
[Phase 4] 内容分级整理（L1-L4）
    ↓
[Phase 5] 生成 HTML 报告
    ├─ 技术概览（200-1000字）
    ├─ 分级资源（带平台标签和可点击链接）
    ├─ 平台获取诊断面板
    └─ 平台统计明细
```

## 浏览器策略

### 浏览器选择

| 场景 | 浏览器 Profile | 说明 |
|------|----------------|------|
| **默认** | `openclaw`（省略 profile） | 独立受控浏览器，无登录态，适合公开内容 |
| **需要登录态** | `chrome-relay` | 用户已登录的 Chrome，适合知乎、B站等 |

### 启动顺序

```
1. 优先使用 openclaw 默认浏览器（独立、干净）
2. 如果平台需要登录（知乎文章、B站视频详情等），切换 chrome-relay
3. 每个平台搜索完成后，关闭标签页释放资源
```

## Phase 1: 关键词扩展

与 v3.0 一致，中英双语扩展：

```yaml
示例：Kubernetes
中文:
  核心: ["Kubernetes", "K8s", "容器编排"]
  教程: ["Kubernetes入门", "K8s教程"]
  深度: ["Kubernetes架构", "K8s原理"]
英文:
  core: ["Kubernetes", "K8s", "container orchestration"]
  tutorial: ["Kubernetes tutorial", "K8s getting started"]
  advanced: ["Kubernetes architecture", "K8s deep dive"]
```

## Phase 2: 平台相关性评估

与 v3.0 一致，根据主题动态评估每个平台的相关性和获取数量。

## Phase 3: 浏览器搜索（核心变更）

### 3.1 搜索引擎策略

| 目标平台 | 搜索方式 | URL 模板 |
|----------|----------|----------|
| **通用英文** | Google 搜索 | `https://www.google.com/search?q={关键词}` |
| **通用中文** | 百度搜索 | `https://www.baidu.com/s?wd={关键词}` |
| **知乎** | 知乎站内搜索 | `https://www.zhihu.com/search?type=content&q={关键词}` |
| **CSDN** | CSDN 搜索 | `https://so.csdn.net/so/search?q={关键词}` |
| **B站** | B站站内搜索 | `https://search.bilibili.com/all?keyword={关键词}` |
| **GitHub** | GitHub 搜索 | `https://github.com/search?q={关键词}&type=repositories` |
| **arXiv** | arXiv 搜索 | `https://arxiv.org/search/?query={关键词}` |
| **YouTube** | YouTube 搜索 | `https://www.youtube.com/results?search_query={关键词}` |
| **HackerNews** | HN 搜索 | `https://hn.algolia.com/?q={关键词}` |
| **微信公众号** | 搜狗微信搜索 | `https://weixin.sogou.com/weixin?query={关键词}` |
| **小宇宙** | 小宇宙搜索 | `https://www.xiaoyuzhoufm.com/search?q={关键词}` |

### 3.2 每个平台的搜索步骤

```
对于每个平台：
  1. browser(action="navigate", url=搜索URL)
  2. browser(action="snapshot") → 获取搜索结果列表
  3. 从 snapshot 中提取 Top N 个结果的标题和链接
  4. 对每个结果：
     a. browser(action="navigate", url=结果链接)
     b. browser(action="snapshot") → 获取文章内容
     c. 提取：标题、作者、发布时间、正文摘要
  5. 记录获取状态（成功条数、失败原因）
  6. 关闭多余标签页
```

### 3.3 关键操作示例

**Google 搜索**：
```
browser(action="navigate", url="https://www.google.com/search?q=Kubernetes+tutorial")
browser(action="snapshot")  → 获取搜索结果
# 从 snapshot 中提取链接
browser(action="navigate", url="第一个结果链接")
browser(action="snapshot")  → 获取文章内容
```

**知乎搜索**（需要 chrome-relay）：
```
browser(action="navigate", url="https://www.zhihu.com/search?type=content&q=Kubernetes",
        profile="chrome-relay")
browser(action="snapshot", profile="chrome-relay")  → 获取搜索结果
# 提取知乎文章链接（zhuanlan.zhihu.com/p/xxx）
browser(action="navigate", url="https://zhuanlan.zhihu.com/p/xxx",
        profile="chrome-relay")
browser(action="snapshot", profile="chrome-relay")  → 获取文章内容
```

**B站搜索**：
```
browser(action="navigate", url="https://search.bilibili.com/all?keyword=Kubernetes")
browser(action="snapshot")  → 获取视频列表（标题、播放量、UP主）
# 提取视频链接（bilibili.com/video/BVxxx）
```

### 3.4 内容提取策略

| 内容类型 | 提取方式 | 提取目标 |
|----------|----------|----------|
| **文章** | snapshot → 解析文本 | 标题、作者、正文前500字 |
| **视频** | snapshot → 解析元数据 | 标题、UP主、播放量、简介 |
| **论文** | snapshot → 解析摘要 | 标题、作者、Abstract |
| **仓库** | snapshot → 解析 README | 名称、Stars、描述 |
| **讨论** | snapshot → 解析帖子 | 标题、分数、评论数 |

### 3.5 获取诊断（每个平台必须输出）

```
📊 平台获取诊断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Google搜索    | 10条 | 独立浏览器，搜索结果正常
✅ 知乎          | 8条  | chrome-relay，站内搜索 + zhuanlan 直链
✅ GitHub        | 12条 | 独立浏览器，仓库搜索+API
✅ arXiv         | 5条  | 独立浏览器，搜索结果正常
✅ B站           | 6条  | 独立浏览器，视频列表正常
⚠️ CSDN          | 3条  | 独立浏览器，部分文章需VIP，跳过
❌ YouTube        | 0条  | 独立浏览器，地区限制无法加载
✅ HackerNews    | 4条  | 独立浏览器，Algolia搜索正常
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计: 48条 (7/8 平台成功)
```

### 3.6 用户补充链接处理

当用户发送额外链接时：
```
1. 识别 URL 的平台来源
2. browser(action="navigate", url=用户链接)
3. browser(action="snapshot") → 提取内容
4. 分类到对应 Level
5. 更新 HTML 报告（增量）
```

## Phase 4: 内容分级

与 v3.0 一致：L1入门 / L2实践 / L3深度 / L4前沿

## Phase 5: HTML 报告生成

与 v3.0 一致，使用 `references/report-template.html` 模板生成自包含 HTML。

## 性能优化

### 减少浏览器操作次数

1. **批量提取**：一次 snapshot 提取搜索页面的所有结果，而不是逐个点击
2. **标签复用**：在同一标签页中 navigate 不同页面，减少标签开关
3. **跳过低质量**：搜索结果中明显低质量的跳过不打开
4. **并行标签**：如果浏览器支持，可同时打开多个标签

### 超时和错误处理

```
- 页面加载超时（>15s）→ 标记失败，继续下一个
- 页面内容为空 → 尝试等待 2s 后重新 snapshot
- 弹窗/登录拦截 → 尝试关闭弹窗，或切换 chrome-relay
- 验证码 → 标记为"需人工干预"，跳过
```

## 与 v3.0 的完整对比

| 维度 | v3.0 | v4.0 |
|------|------|------|
| **搜索工具** | web_fetch 优先 | **browser（CDP）唯一** |
| **搜索体验** | HTTP 请求 | **模拟真人浏览器** |
| **JS 渲染** | ❌ | ✅ |
| **知乎** | 403 失败 | ✅ chrome-relay 搜索 |
| **B站** | 空内容 | ✅ JS 渲染后提取 |
| **CSDN** | 404 频繁 | ✅ 浏览器正常加载 |
| **YouTube** | 超时 | ⚠️ 可能地区限制 |
| **搜索结果一致性** | 低（API格式） | **高（与人工一致）** |
| **输出格式** | HTML | HTML（不变） |
| **失败诊断** | ✅ | ✅（不变） |

## 注意事项

1. **浏览器资源管理**：搜索完一个平台后关闭多余标签页，避免内存泄漏
2. **搜索频率控制**：不要短时间内对同一平台发起过多请求，间隔 2-3 秒
3. **内容提取精度**：snapshot 返回的是 accessibility tree，需要从中筛选有效内容
4. **cookie/登录态**：需要登录的平台使用 chrome-relay，公开内容用独立浏览器
5. **隐私保护**：不在独立浏览器中输入任何账号密码

---

**版本**：v4.0.0
**更新日期**：2026-03-27
**核心变更**：全面弃用 web_fetch，改用 browser CDP 协议模拟真人搜索
