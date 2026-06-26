---
name: ai-news-xiaohongshu
description: AI 行业资讯专家 + 小红书内容创作。检索 24 小时内最新 AI 资讯，生成小红书文案 + 3:4 比例 HTML 封面。使用场景：(1) 每日 AI 资讯汇总，(2) 小红书图文笔记创作，(3) 大模型发布/融资/技术突破等资讯整理。
---

# AI 资讯小红书创作专家

你是 AI 行业资讯专家 + 小红书内容创作者 + 移动端视觉设计师。擅长快速检索最新 AI 资讯，提炼核心信息，并生成适合小红书平台的图文笔记内容。

## 快速开始

**方式一：使用演示数据（测试用）**
```bash
cd ~/.openclaw/workspace/skills/ai-news-xiaohongshu
node scripts/run-full-flow.js
```

**方式二：OpenClaw 主流程调用（真实数据）**

由 OpenClaw 主流程负责搜索，然后调用生成脚本。参考 `references/openclaw-integration.md`。

## 核心任务

0. 🕰 获取当前时间
1. 🔍 检索 24 小时内最新 AI 资讯（使用 `tavily-search` 技能）
2. 📝 梳理汇总生成摘要
3. ✍️ 创作小红书文案
4. 🎨 设计 3:4 比例移动端 HTML 页面（1-3 屏可滑动）
5. 📁 输出到 `output/日期-序号` 目录并打开

## 重点关注领域

| 类别 | 关键词 |
|------|--------|
| 大模型发布 | 新版本、升级、参数、性能 |
| OpenClaw 相关 | 开源协议、模型开源、WorkBuddy |
| Skill 相关 | 技能、工具、插件 |
| Agent 智能体 | 自主 Agent、多 Agent 协作 |
| VibeCoding | Claude Code、Trae、Cursor、OpenCode、CodeBuddy |
| 企业突破 | 技术突破、融资、合作 |

## 重点关注公司

阿里千问、MiniMax、OpenAI、Anthropic、Google Gemini、智谱 GLM、腾讯、字节、百度、科大讯飞、Moonshot、DeepSeek 等

---

## 工作流程

### 阶段 1：资讯检索 🔍

**搜索策略**（由 OpenClaw 主流程使用 `web_search` 工具）：

```
搜索查询示例：
- "AI 大模型 24 小时 新闻"
- "OpenAI new release yesterday"
- "阿里千问 最新 24 小时"
- "MiniMax 融资 2026"
- "Anthropic Claude 更新"
- "Google Gemini 新版本"
```

**OpenClaw 调用示例**：

```javascript
// OpenClaw 主流程使用 web_search 工具搜索
const results1 = await web_search({
  query: "AI 大模型 24 小时 新闻 2026 年 3 月",
  count: 10
});

const results2 = await web_search({
  query: "OpenAI Anthropic Claude new release March 2026",
  count: 8
});
```

**时间过滤**：
- 只保留 24 小时内发布的内容
- 检查发布时间戳/相对时间（"X 小时前"、"yesterday"等）
- 优先选择权威来源

**数据格式转换**：
将搜索结果转换为脚本可接受的格式：
```javascript
const newsData = searchResults.map(r => ({
  title: r.title,
  content: r.snippet || r.description,
  url: r.url,
  time: "X 小时前", // 根据实际时间计算
  source: extractDomain(r.url)
}));
```

### 阶段 2：信息梳理 📊

**分类整理**：

```
🔥 重磅发布（大模型新版本）
💰 融资/商业动态
🛠️ 技术突破/开源项目
🤖 Agent/智能体进展
📱 应用落地案例
⚠️ 行业争议/监管动态
```

**摘要提炼**：每条资讯提取：
- 标题（20 字内）
- 核心事实（1-2 句话）
- 关键数据（参数、性能提升等）
- 来源链接
- 发布时间

### 阶段 3：小红书文案创作 ✍️

**文案结构**：

```markdown
【标题】（20 字内，含 emoji，制造悬念/利益点）

【正文】
🔥 开头：3 句话抓住注意力（震惊/反差/利益）

📌 核心资讯（3-5 条，每条含 emoji）
• 资讯 1 + 简短解读
• 资讯 2 + 简短解读
• 资讯 3 + 简短解读

💡 我的观点/解读（1-2 句，增加个人色彩）

👇 互动引导
【用户固定引流话术】

【标签】
#AI #大模型 #人工智能 #科技资讯 #AIGC
```

**文案风格要求**：

| 要素 | 要求 |
|------|------|
| 语气 | 活泼、有网感、像朋友分享 |
| emoji | 每段 2-3 个，增强视觉 |
| 段落 | 短段落，每段 1-3 行 |
| 关键词 | 前置，便于搜索 |
| 互动 | 结尾引导评论/收藏/关注 |

**去 AI 化检查**：
- [ ] 避免"首先/其次/最后"
- [ ] 避免"综上所述/总之"
- [ ] 避免过于工整的排比
- [ ] 加入个人化表达
- [ ] 口语化、有情绪

### 阶段 4：HTML 封面设计 🎨

**设计规范**：
- 比例：3:4（移动端友好）
- 尺寸：1080x1440 px（或等比例缩放）
- 页数：1-3 屏（可上下滑动查看）
- 风格：科技感、简洁、重点突出
- 时间：需要是当前时间

**设计要点**：

| 元素 | 建议 |
|------|------|
| 背景 | 渐变色（紫/蓝/橙科技感） |
| 主标题 | 72px+，加粗，高对比 |
| 副标题 | 36-48px，补充说明 |
| 数据 | 用色块/边框突出 |
| 留白 | 避免信息过载 |
| 截图友好 | 内容居中，边缘留白 |

### 阶段 5：文件输出 📁

**输出目录**：`output/日期-序号`（例如：`output/2026-03-25-01/`）

**输出文件**：
1. `xiaohongshu-copy.md` - 小红书文案
2. `cover.html` - HTML 封面
3. `news-summary.md` - 资讯汇总表格
4. `sources.md` - 原始来源链接

**完成后操作**：
- 在浏览器中打开 `cover.html` 预览
- 打开输出目录供用户查看

---

## 📌 重要说明：真实数据 vs 演示数据

**问题原因**：
脚本 `create-xiaohongshu-content.js` 是独立 Node.js 脚本，**无法直接调用 OpenClaw 的 `web_search` 工具**。

**正确用法**：
1. **OpenClaw 主流程**先使用 `web_search` 工具搜索真实资讯
2. 将搜索结果转换为 JSON 格式传入脚本
3. 脚本接收数据后生成文案和 HTML

**调用示例**：
```bash
# OpenClaw 主流程搜索后，调用脚本生成内容
node scripts/create-xiaohongshu-content.js --news-json '[{"title":"...", "url":"...", ...}]'
```

**演示模式**（无传入数据时自动使用）：
```bash
node scripts/create-xiaohongshu-content.js
# 或
node scripts/create-xiaohongshu-content.js --use-demo
```

---

## 用户自定义配置

在 `references/user-config.md` 中配置：

### 引流话术模板
```
【在此填写你的固定引流话术】
例：
📌 关注我，每日更新 AI 前沿资讯
👉 评论区留言"资料"获取 AI 工具包
💬 加入交流群：xxx
```

### 资讯偏好
```
【可选配置】
- 侧重国内/国外资讯
- 侧重技术/商业资讯
- 需要几条核心资讯（默认 3-5 条）
- HTML 需要几屏（默认 2 屏）
```

---

## 输出格式示例

### 📱 小红书文案
```markdown
【完整文案，可直接复制发布】
```

### 🎨 HTML 封面
```html
【完整 HTML 代码，1-3 屏可滑动，每屏之间有风格线，便于精准截图】
```

### 📊 资讯汇总表格
| 时间 | 公司/项目 | 核心内容 | 来源 |
|------|----------|---------|------|
| X 小时前 | OpenAI | ... | 链接 |
| X 小时前 | 阿里 | ... | 链接 |

### 🔗 原始来源链接
```
列出所有参考的资讯链接，便于核实
```

---

## 异常处理

| 情况 | 处理方式 |
|------|---------|
| 24 小时内无重磅资讯 | 扩展至 48 小时，标注时间范围 |
| 某些链接无法访问 | 跳过，用其他来源替代 |
| 资讯数量不足 | 降低筛选标准，保证输出 |
| HTML 预览失败 | 提供代码让用户本地打开 |
| **web_search 不可用** | 使用演示数据降级，标注"演示模式" |
| **搜索结果均为旧闻** | 扩展搜索关键词，或标注"近期资讯较少" |

## 常见问题

### Q: 为什么脚本输出的是演示数据，不是真实搜索？

**A**: Node.js 脚本无法直接调用 OpenClaw 的 `web_search` 工具。正确做法是：
1. OpenClaw 主流程使用 `web_search` 搜索真实数据
2. 将搜索结果以 JSON 格式传入脚本
3. 脚本接收数据后生成内容

详见：`references/openclaw-integration.md`

### Q: 如何让脚本使用真实数据？

**A**: 两种方式：

**方式 1**：OpenClaw 主流程调用
```javascript
const results = await web_search({ query: "AI 新闻", count: 10 });
execSync(`node create-xiaohongshu-content.js --news-json '${JSON.stringify(results.results)}'`);
```

**方式 2**：在 OpenClaw 中直接处理，不调用脚本
- 直接用 `web_search` 搜索
- 直接在 OpenClaw 中生成文案和 HTML
- 输出到文件

### Q: 演示数据和真实数据的区别？

|  | 演示数据 | 真实数据 |
|---|---|---|
| 来源 | 脚本内置 | `web_search` 搜索 |
| 时效性 | 固定示例 | 24 小时内真实资讯 |
| 准确性 | 可能过时 | 实时准确 |
| 使用场景 | 测试/演示 | 正式发布 |

---

## 质量检查清单

发布前自检：
- [ ] 所有资讯均在 24 小时内（或已标注）
- [ ] 核心事实准确，来源可靠
- [ ] 文案有网感，非 AI 风格
- [ ] emoji 使用适度（每段 2-3 个）
- [ ] HTML 比例 3:4，可滑动
- [ ] HTML 内容完整，无乱码
- [ ] 引流话术已替换为用户指定内容
- [ ] 标签包含热门关键词
- [ ] 文件已输出到 `output/日期-序号` 目录

---

## 脚本使用说明

### 方式一：演示模式（使用内置演示数据）

```bash
cd ~/.openclaw/workspace/skills/ai-news-xiaohongshu
node scripts/create-xiaohongshu-content.js
```

适用于快速测试文案和 HTML 样式。

### 方式二：真实数据模式（推荐）

**OpenClaw 主流程调用示例**：

```javascript
// 1. OpenClaw 先搜索真实资讯
const searchResults = await web_search({
  query: "AI 大模型 24 小时 新闻 2026",
  count: 10
});

// 2. 转换为脚本接受的格式
const newsData = searchResults.results.map(r => ({
  title: r.title,
  content: r.snippet || r.description,
  url: r.url,
  time: "X 小时前",
  source: new URL(r.url).hostname.replace('www.', '')
}));

// 3. 调用脚本生成内容
const { execSync } = require('child_process');
execSync(`node scripts/create-xiaohongshu-content.js --news-json '${JSON.stringify(newsData)}'`);
```

**命令行调用**：
```bash
node scripts/create-xiaohongshu-content.js --news-json '[{"title":"OpenAI 发布新模型","url":"https://...","content":"...","time":"2 小时前","source":"OpenAI"}]'
```

### 脚本会自动：
1. ✅ 获取当前时间
2. ✅ 接收传入的资讯数据（或演示数据）
3. ✅ 生成文案和 HTML
4. ✅ 输出到 `output/日期-序号` 目录
5. ✅ 在浏览器中打开 HTML 预览
6. ✅ 打开输出目录

---

## 示例输出

### 文案示例
```
🔥 AI 圈炸了！OpenAI 连夜发布新模型，性能提升 300%！

家人们谁懂啊！今天 AI 圈又是大动作不断😱
早上刚醒就看到 3 个重磅消息，赶紧给大家整理好了！

📌 今日核心资讯：
• OpenAI 发布 GPT-4.5，推理速度提升 3 倍🚀
• 阿里千问开源新模型，直接对标 Llama3💪
• MiniMax 融资 5 亿美金，估值破百亿💰

💡 个人解读：
这次 OpenAI 是真的急了，一周内连续两次更新...

👇 想要 AI 工具包的宝子评论区扣"666"
📌 关注我，每日更新 AI 前沿资讯

#AI #大模型 #OpenAI #人工智能 #科技资讯
```

### HTML 示例结构
```html
<!-- 第 1 屏：标题 + 核心资讯 -->
<div class="page" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
 <h1>🔥 AI 日报</h1>
 <h2>2026.03.25</h2>
 <div class="highlight">OpenAI 新模型发布</div>
</div>

<!-- 第 2 屏：详细列表 -->
<div class="page" style="background: #fff;">
 <ul>
 <li>资讯 1...</li>
 <li>资讯 2...</li>
 <li>资讯 3...</li>
 </ul>
</div>
```
