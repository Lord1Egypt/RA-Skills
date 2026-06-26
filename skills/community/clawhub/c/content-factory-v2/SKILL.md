---
name: content-factory
description: Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with user, writing professional content through self-iteration, and outputting both Markdown and HTML formats.
---

# Content Factory

## 高质量内容创作标准（2026-02-20 更新）

### 爆款文章核心公式

**标题 + 开头 = 80%的阅读量**

### 核心原则

**文章必须给用户带来真正价值：**
1. **学到具体的方法论** - 不是泛泛而谈，有可操作的方法
2. **能实操的指南** - 照着做就能成，给提示词、给代码、给步骤
3. **开拓视野提升认知** - 看到以前没想过的东西，认知升级

### 标题写法

- 争议/对比词：「手撕Sora，脚踢Veo」「黑奴」「智商税」
- 数字吸睛：「13个行业实战案例」
- 疑问句引发好奇：「真的值吗？」
- 颠覆认知：挑战传统观点

### 开头写法

**Hook 是必须的：开头必须有一个 Hook，不能直接进入正文。**

Hook 的结构：**承认一个普遍痛点 + 今天这期的独特发现**

Jeff 给的示范：
「大家使用 OpenClaw，其实并没有特别好的找到商业应用场景。今天通过地图 API 的结合，让我们看到了更多商业落地应用的可能性。」

其他 Hook 示例：
- 「很多人装了 OpenClaw，但不知道它还能这样用……」
- 「你以为 OpenClaw 只能聊天？实际上它能干这个……」
- 「大多数人用 AI 工具只用到了一成功能……」

**一句话总结：开头先承认用户的困惑或局限，再抛出今天的发现，让读者觉得『这正是我需要的』。**

### 正文结构

**2-3个具体案例，层层递进：**

每个案例包含：
- 具体场景（扔给AI什么任务）
- 真实过程（提示词、报错、改Bug）
- 结果展示（截图、链接、数据）
- 优缺点分析（不藏着掖着）

### 干货要求

- 给可直接抄作业的提示词
- 完整代码示例
- 真实项目名和案例
- 工作流拆解

### 真诚原则

- 报错经历也分享
- 槽点大方承认
- 效果对比（Before/After）
- 提供测试链接和在线Demo

### 结尾升华

- 方法论总结
- 未来趋势展望
- Agent自动化想象空间

### 三篇文章对照学习

| 维度 | Qwen3.5篇 | MiniMax M2.5篇 | Seedance 2.0篇 |
|------|-----------|-----------------|-----------------|
| **标题** | 争议词+结论 | 疑问句+颠覆 | 对比+数字 |
| **开头** | 问题切入 | 观察洞察 | 回应期待 |
| **结构** | 2.0→3.0升级 | 基础→附加→终极 | 行业分类 |
| **干货** | 代码配置 | 提示词实测 | 完整工作流 |
| **真诚** | 报错经历 | 槽点承认 | 不足之处 |
| **结尾** | 心里话升华 | 测试入口 | Agent未来 |

---

## Overview


### 八、高阅读量文章共同点（来自饼干哥哥、藏师傅分析）

**1. 选题精准**
- 蹭热点 + 独特视角
- 解决具体问题
- 目标人群明确

**2. 结构清晰**
- 层层递进
- 案例丰富
- 重点突出

**3. 语言生动**
- 有情绪（有态度）
- 有细节（不说正确的废话）
- 有对话感（像在跟朋友聊天）

**4. 利他思维**
- 读者能得到什么？
- 看完能做什么？
- 为什么转发？

**5. 平台友好**
- 关键词布局
- 开头有关键词
- 结尾引导互动

Generate complete WeChat Official Account "viral-style" articles using YouTube research, user confirmation, and professional writing with self-iteration.
Use this skill when given a topic/title and asked to research, create, and write a complete WeChat article with both MD and HTML outputs.

## CRITICAL: Tool Dependency Check (MUST DO FIRST)

**Before starting any research, MANDATORY tool check:**

### Step 1: Check yt-dlp Installation
```bash
yt-dlp --version
```

**If not installed or command fails:**
- STOP immediately
- Inform user: "yt-dlp tool is required for YouTube content extraction"
- Provide installation command: `pip install yt-dlp`
- Wait for user to install before proceeding
- DO NOT skip to alternative methods without checking tools first

### Step 2: Verify Script Files
```bash
ls scripts/yt_dlp_search.py
ls scripts/yt_dlp_captions.py
```

**If scripts missing:**
- Check skill base directory: `~/.claude/skills\content-factory\scripts\`
- Inform user if files are missing
- DO NOT proceed without verifying script availability

### Step 3: Verify Web Search Tools
```bash
# Test Tavily (primary) - check credentials first
python3 -c "import json; print(json.load(open('/root/.openclaw/credentials/tavily.json'))['api_key'])" && echo "Tavily: OK"

# Test Brave (fallback) - check credentials
python3 -c "import json; print(json.load(open('/root/.openclaw/credentials/brave.json'))['api_key'])" && echo "Brave: OK"

# Test smart_search script
python3 /root/.openclaw/workspace/scripts/smart_search.py "test" --max-results 1 2>&1 | head -5
```

**If Tavily/Brave credentials exist:**
- ✅ "Web search tools verified: Tavily API ✓, Brave API ✓"
- Proceed with web research using smart_search.py (Tavily primary, Brave fallback)

**If credentials missing:**
- ⚠️ "Web search credentials not found in credentials/ — check Tavily/Brave setup"
- Fall back to: YouTube search results + X/Nitter + official pages (still viable)

### Step 4: Tool Status Communication
Always inform user of tool status:
- ✅ "yt-dlp installed (version X.X.X), proceeding with YouTube content extraction"
- ✅ "Web search: Tavily ✓, Brave ✓"
- ❌ "yt-dlp not found, please install with: pip install yt-dlp"
- ⚠️ "Scripts found but yt-dlp missing, installation required"
- ⚠️ "Web search unavailable — using YouTube search + X/Nitter + official pages"

**IMPORTANT PRINCIPLE:**
- Tool checking is a PREREQUISITE, not optional
- "Optionally run scripts" means "use if available", NOT "skip if inconvenient"
- Local scripts are PRIMARY method, WebFetch is FALLBACK
- Never assume tools are unavailable without checking first
- **Web Search: Always use smart_search.py via exec FIRST (Tavily → Brave fallback)**
  - Test: `python3 /root/.openclaw/workspace/scripts/smart_search.py "test" --max-results 1`
  - Do NOT use OpenClaw built-in `web_search` tool as primary (it has separate Brave key config)

## Workflow

### 1) Intake and clarify

- Require: user-provided title/topic.
- Ask for missing essentials: target audience, industry/region, tone (serious vs. punchy), desired length, and recency constraints.
- Confirm language preference; default to Chinese output unless user requests otherwise.

### 2) Web Research (Multi-source)

**IMPORTANT: Research from diverse web sources - YouTube is a KEY source but not the ONLY source.**

**Primary Research Sources (in priority order):**

1. **YouTube Videos** (Key source for case studies and expert insights)

   **CRITICAL: YouTube Content Extraction Priority Order**

   **PRIMARY METHOD (Try First):**
   - Run `scripts/yt_dlp_search.py` to search and collect video metadata
     ```bash
     python scripts/yt_dlp_search.py "your search query" --max-results 10
     ```
   - Use `scripts/yt_dlp_captions.py` to download subtitles/transcripts
     ```bash
     python scripts/yt_dlp_captions.py VIDEO_URL --whisper-if-missing
     ```
   - These scripts provide: title, channel, view count, upload date, duration, URL, full transcripts

   **FALLBACK METHOD (If scripts fail):**
   - Try WebFetch on YouTube video pages
   - If WebFetch blocked, request user to provide video URLs manually
   - Use smart_search.py via exec to find YouTube video links, then extract metadata

   **LAST RESORT (If all YouTube access fails):**
   - Proceed with other sources (articles, reports, blogs)
   - Clearly document in article that YouTube content was unavailable
   - Compensate with more industry reports and expert blogs

   **Content Extraction Guidelines:**
   - Load `references/youtube_research_checklist.md` for detailed extraction steps
   - Select 2-4 high-view, highly relevant videos (preferably top 20% by view count)
   - Extract verifiable data from: transcripts, descriptions, video chapters
   - Capture: title, channel, view count, upload date, duration, URL, transcript excerpts, relevance notes

2. **Official Documentation & Announcements**
   - Company blogs (e.g., anthropic.com/news, openai.com/blog)
   - Official product documentation
   - Press releases and official statements
   - GitHub repositories (README, release notes)

3. **Industry Analysis & Reports**
   - Gartner, Forrester, McKinsey reports
   - TechCrunch, VentureBeat, The Verge news articles
   - Industry-specific publications
   - Research papers and whitepapers

4. **Expert Blogs & Technical Content**
   - Medium, Dev.to, Hacker News discussions
   - Personal blogs of industry experts
   - LinkedIn articles from thought leaders
   - Technical tutorials and case studies

5. **Community Discussions & Reviews**
   - Reddit threads (r/MachineLearning, r/artificial, etc.)
   - Stack Overflow technical discussions
   - Product Hunt reviews
   - Twitter/X threads from verified experts

**Research Strategy:**

- **Build 5-10 diverse search queries** covering:
  - Core topic keywords (e.g., "Claude Cowork enterprise deployment")
  - Use case scenarios (e.g., "AI agent workflow automation case study")
  - Problem/solution pairs (e.g., "reduce report generation time AI")
  - Industry trends (e.g., "AI agent adoption 2026 forecast")
  - Comparison queries (e.g., "Claude Cowork vs Copilot")

- **Use WebSearch and WebFetch tools** to gather content from multiple sources
- **Diversify source types**: Mix videos, articles, reports, and discussions
- **Prioritize recent content**: Focus on material from the last 3-6 months unless topic requires historical context

**Content Extraction Guidelines:**

- **Summarize only from verifiable sources** - Extract actual content, not speculation
- **Explicitly label source type and URL** for each data point:
  - "根据Anthropic官方博客 (anthropic.com/news/...)"
  - "YouTube视频《...》中提到 (youtube.com/watch?v=...)"
  - "Gartner 2026年报告指出 (...)"
  - "TechCrunch报道称 (techcrunch.com/...)"
- **Cross-verify key statistics** from multiple sources when possible
- **Capture publication dates** to ensure data freshness
- **Note credibility indicators**: author credentials, publication reputation, data sources cited

**When web access is unavailable:**
- Ask for user-provided URLs or content excerpts
- Request permission to enable web search tools
- Use available references and documentation

### 3) Synthesize angles

- Extract 3-7 **cross-source insights**: recurring pain points, surprising data, repeated mistakes, or actionable tactics found across multiple sources (videos, articles, reports, discussions)
- Identify **consensus patterns**: What do multiple credible sources agree on?
- Spot **unique insights**: What does only one highly credible source reveal?
- Note **conflicting viewpoints**: Where do sources disagree? (can become article angles)
- Translate insights into shareable WeChat angles:
  - Beginner-friendly guides
  - Myth-busting content
  - Actionable checklists
  - Trend analysis + predictions
  - Real case studies with verified data

### 4) Produce topic ideas and confirm with user

- Load `references/wechat_viral_frameworks.md` to diversify angles and hooks.
- Generate 3-5 potential article topics based on **multi-source web research** (YouTube, blogs, reports, discussions).

### 4.5) Write Research to Shared Memory (MANDATORY)

**CRITICAL: Before presenting options to user, write full research context to shared memory.**

This is required because: the cron job runs in an isolated session. After presenting options via Feishu, the session ends. When the user responds with "选X" in the main session, Chief Agent must be able to retrieve the research context.

**Write to this file:**
```
/root/.openclaw/workspace/memory/daily/research-YYYY-MM-DD.md
```

**File must include:**
- All candidate topics with titles, target readers, core promises
- **Every YouTube/video URL** (this is the most commonly missing field)
- Full outlines for each topic
- Source URLs for all references
- Which topic is recommended as Option 1 and why

**Format:**
```markdown
# Research - YYYY-MM-DD

## Candidate 1 (Recommended)
**Title:** ...
**Target:** ...
**Source URLs:** https://youtube.com/... (CRITICAL - include all)
**Outline:** ...

## Candidate 2
...
```

**After writing memory, THEN present options to user (Step 5).**
<<<<<<< HEAD
=======

**🚨 CRITICAL: Topic Direction - Application-Focused (2026-03-17 更新)**

**⚠️ 禁止生成纯技术类选题！以下方向禁止出现：**
- ❌ 模型对比（如：DeepSeek vs GPT-4）
- ❌ API 更新（如：OpenAI 新 API 发布）
- ❌ 纯技术解读（如：MoE 架构解析）
- ❌ 论文解读（如：最新 AI 论文分析）

**✅ 必须生成应用导向选题！方向优先级：**

1. **Skills - Agent Skills 使用技巧**
   - 如何用 AI Agent 提升工作效率
   - 特定技能的使用秘笈和最佳实践
   - 自动化工作流的搭建经验

2. **应用场景 - AI Agent 实际案例**
   - AI 在具体工作中的落地案例
   - 行业场景的 AI 解决方案
   - 真实用户的使用体验分享

3. **商业模式分析 - AI 创业与盈利**
   - AI 产品/服务如何赚钱
   - 成功的 AI 商业案例分析
   - AI 创业机会和赛道分析

4. **工具评测 - 真实体验对比**
   - 多款 AI 工具的实际使用对比
   - 优缺点分析和使用建议
   - 适合不同场景的工具推荐

5. **案例分享 - AI 落地实录**
   - 企业/个人 AI 部署的真实案例
   - 部署成本、效果和经验教训
   - 可复制的 AI 实施方法论

6. **OpenClaw 专题 - Agent 编排实战**
   - **OpenClaw 技巧教程**
     - OpenClaw 实际使用技巧
     - 多个 Chat App 如何配置
     - Agent 编排最佳实践
   - **OpenClaw 应用场景**
     - 用 OpenClaw 做自动化工作流
     - OpenClaw + 飞书/微信/Telegram 集成
     - 自定义 Agent 开发
   - **OpenClaw 商业模式**
     - 基于 OpenClaw 的 SaaS 服务
     - OpenClaw 企业部署案例

**选题评估标准：**
- 是否对读者有实际帮助？
- 读者能否立即应用到工作中？
- 是否有具体的案例和数据支撑？

**🚨 CRITICAL: Topic Freshness Requirement (2026-03-09)**
- **MUST only select topics from past 24-48 hours**
- **For AI/Tech topics: Must verify the news date, no outdated热点**
- Use search with time filter: `after:2026-03-08` or similar
- If researching DeepSeek, OpenAI, Anthropic etc - check the LATEST developments
- **Reject any topic where the news is older than 48 hours**

>>>>>>> 8d2abf78b8490403831aae82052e8e107054b856
- For each topic, provide:
  - Title (Chinese by default)
  - Target reader
  - Core promise/value
  - Outline with 3-5 sections (short section headers + 1-2 key points each)
  - Opening hook (1-2 sentences)

### 5) User confirmation - MANDATORY

**CRITICAL: Before proceeding to write the full article, MUST confirm with user:**
- Present the proposed topic and outline clearly
- Use AskUserQuestion tool to ask: "Which topic would you like me to develop into a full article?" or "Is this outline approved for full article writing?"
- Wait for explicit user approval before proceeding
- Allow user to request modifications to the outline

### 6) Write complete article with self-iteration

Once the topic and outline are confirmed:

**Phase 1: Initial Draft**
- Write complete article following the approved outline
- Target length: 2000-4000 Chinese characters
- **MANDATORY: Include real cases and practical implementation**:
  - **At least 2-3 real enterprise cases** with specific company names, metrics, and outcomes
  - **Step-by-step implementation guide** for readers to follow
  - **Actionable checklists** or frameworks that can be immediately applied
  - **Concrete examples** with numbers, timeframes, and results
- **CRITICAL: NO FAKE NUMBERS - Data Integrity Requirements**:
  - ❌ **NEVER fabricate or invent specific metrics, percentages, or statistics**
  - ❌ **DO NOT make up company names, dates, or case study details**
  - ✅ **Use verifiable data from YouTube research** (transcripts, descriptions, published reports)
  - ✅ **When exact numbers unavailable, use professional qualifying language**:
    - "预计可达..." (expected to reach...)
    - "通常情况下可提升..." (typically improves by...)
    - "根据行业经验，一般..." (based on industry experience, generally...)
    - "类似案例显示约..." (similar cases show approximately...)
    - "预期节省..." (projected to save...)
  - ✅ **Cite data sources when using specific numbers**: "根据Gartner报告...", "McKinsey研究显示..."
  - ✅ **Use ranges instead of precise fake numbers**: "提升30-50%" not "提升47.3%"
  - ✅ **Focus on qualitative improvements when quantitative data unavailable**: "显著提升效率" rather than inventing "93%效率提升"
  - **Example of WRONG approach**: "我见证了北京某公司效率提升93%"（如果这个93%是编造的）
  - **Example of RIGHT approach**: "类似部署预计可提升30-50%的效率，具体取决于现有流程复杂度"
- **IMPORTANT: NO EMOJIS in professional versions** - Do not use any emoji characters in the full MD/HTML article content (emojis are only allowed in Xiaohongshu version)
- **IMPORTANT: First-person narrative** - Use "我" (I/me) perspective throughout the article:
  - Write as if sharing personal insights and experiences
  - Use phrases like: "我发现...", "我观察到...", "让我分享...", "我建议..."
  - Create connection with reader through: "你可能会问...", "这让我想起..."
  - Professional yet warm tone - not overly casual, but approachable and authentic
  - **禁止废话表达**: 避免"我认为"、"我觉得"、"我相信"等无信息量表达，直接陈述观点
- **IMPORTANT: 精炼写作原则**:
  - 每句话必须包含新信息，不重复已说过的内容
  - 删除所有冗余修饰词和过渡句
  - 如果删掉某句话不影响理解，就必须删掉
  - 用数据和事实说话，不用主观判断词
- Follow the professional tone and style from `references/reference.html`:
  - Use structured headings (h1, h2, h3, h4)
  - Include blockquotes for emphasis
  - Professional yet engaging narrative style
  - Clear section separation with proper spacing

**Phase 2: Self-Iteration**
- Review the draft for:
  - **Tone consistency**: Professional, confident, not arrogant; avoid complex jargon
  - **First-person voice**: Ensure consistent use of "我" perspective, warm and authentic
  - **Structure flow**: Logical progression from problem → insight → solution
  - **Hook strength**: Opening must grab attention within 3 seconds
  - **Key points**: Each section delivers clear value
  - **Call-to-action**: Natural and compelling conclusion
  - **Case quality**: Verify all cases have specific metrics and are credible
  - **Implementation practicality**: Ensure action steps are clear and executable
  - **精炼检查** ⚠️ MANDATORY:
    - 删除所有"我认为"、"我觉得"、"我相信"等废话表达
    - 检查是否有重复表达相同意思的句子，合并或删除
    - 确保每个段落都有新信息，不是前文的重复
    - 删除所有不影响理解的冗余句子
  - **Data integrity verification** ⚠️ CRITICAL:
    - Check every number, percentage, and metric in the article
    - Verify each can be traced back to YouTube research or cited source
    - Replace any invented numbers with qualifying language ("预计...", "通常...", "约...")
    - Ensure company names and case details are verifiable or appropriately qualified
    - Remove overly precise fake statistics (e.g., "47.3%" → "约45-50%" or "显著提升")
    - **禁止杜撰案例**: 所有案例必须来自研究阶段的真实来源
- Make 2-3 rounds of self-improvement focusing on clarity and impact
- Ensure transitions between sections are smooth

**Phase 3: Quality Review & Scoring (MANDATORY)**

After completing the MD draft, perform a structured quality review and scoring:

**Scoring Criteria (100 points total):**

| Category | Points | Criteria |
|----------|--------|----------|
| **精炼度** | 20 | 无重复表达、无废话("我认为/我觉得")、每句有新信息 |
| **数据真实性** | 20 | 所有案例和数据可追溯到研究来源、无杜撰 |
| **结构清晰度** | 15 | 逻辑流畅、层次分明、移动端友好 |
| **标题吸引力** | 15 | 开头3秒抓住注意力、价值主张明确 |
| **可执行性** | 15 | 行动建议具体可操作、读者能立即应用 |
| **语言质量** | 15 | 专业自信、第一人称一致、无语法错误 |

**Scoring Process:**
1. Complete the MD article draft
2. Perform self-review against each criterion
3. Calculate total score (0-100)
4. Output score report in this format:

```
📊 文章质量评分报告
━━━━━━━━━━━━━━━━━━━━━
精炼度:      XX/20  [具体问题说明]
数据真实性:  XX/20  [具体问题说明]
结构清晰度:  XX/15  [具体问题说明]
标题吸引力:  XX/15  [具体问题说明]
可执行性:    XX/15  [具体问题说明]
语言质量:    XX/15  [具体问题说明]
━━━━━━━━━━━━━━━━━━━━━
总分: XX/100
```

**Decision Logic:**
- **Score < 85**: 自动进行修改，修复扣分项，重新评分，循环直到≥85
- **Score ≥ 85**: 进入"飞书文档确认"流程

**Auto-fix priorities for score < 85:**
1. 删除所有"我认为/我觉得/我相信"
2. 合并或删除重复表达
3. 核实并修正可疑数据
4. 加强开头吸引力
5. 补充具体可执行建议

### ⏸️ 飞书文档确认流程 (CRITICAL - 2026-03-20 新增)

**在生成4种格式之前，必须先写入飞书云文档等待确认！**

**Step 1: 创建飞书云文档**
- 使用 feishu_doc 工具创建新文档
- 文档标题格式：`[待确认] {文章标题}`
- 内容为 Markdown 格式
- 写入后用 read 验证内容

**Step 2: 通知用户确认**
- 发送消息给用户，包含：
  - 文档链接
  - "请确认内容是否OK，回复确认后生成4种格式"
- 等待用户明确确认（用户回复"确认"、"OK"、"可以"等）

**Step 3: 用户确认后**
- 用户确认 → 进入 Phase 4 生成4种格式
- 用户有修改意见 → 根据意见修改后重新写入飞书，循环确认流程

**⚠️ 重要：禁止跳过此步骤直接生成4种格式！**

---

**Phase 4: Final Polish**
- Check all examples and data points are accurate
- Verify Chinese grammar and punctuation
- Ensure visual hierarchy is clear for mobile reading
- Add emphasis with **bold** for key insights
- **Remove all emoji characters** - Article must be emoji-free for professional publication
- **Add business conversion ending** - Replace "参考来源" with engagement and consultation call-to-action (see below)
- **No horizontal rules in HTML** - Do NOT use `<hr/>` tags between paragraphs in HTML output (markdown `---` is acceptable)
- **⚠️ VERIFY XIAOHONGSHU CHARACTER COUNT** - Before finalizing Format 3, count characters (excluding hashtags) and ensure 800-1000. If under 800, add more detail; if over 1000, aggressively cut while keeping core message.

**Phase 5: Generate Infographics for Key Data (HTML Only)**

**CRITICAL: If article contains core data visualizations, generate infographics using NotebookLM**

**When to generate infographics:**
- Article has 2+ key statistics or data comparisons
- Market growth trends with specific numbers
- Before/after comparisons with metrics
- Multi-point data that benefits from visual representation

**Infographic generation workflow:**

1. **Identify data visualization opportunities** in the article:
   - Market size/growth data (e.g., "$315B → $1.1T")
   - Percentage trends (e.g., "36.3% of companies")
   - Before/after comparisons (e.g., "Traditional: $25k/mo vs Solo: $500/mo")
   - Multi-metric comparisons (e.g., "3 key factors")

2. **Use notebooklm-api skill to generate infographics:**
   ```bash
   # For each key data point, generate an infographic
   notebooklm generate infographic "Create a professional infographic showing [data description].
   Use blue color scheme (#1a5490, #2980b9, #3498db) to match article theme.
   Modern, clean design with clear data visualization. Include: [specific metrics]"
   ```

3. **Color scheme requirements** (MUST match HTML theme):
   - Primary blue: #1a5490
   - Accent blue: #2980b9
   - Light blue: #3498db
   - Background: #ebf5fb (light blue)
   - Text: #2c3e50 (dark gray)
   - Use blue gradients and professional business style

4. **Wait for generation and download:**
   ```bash
   # Wait for infographic completion
   notebooklm artifact wait <artifact_id> --timeout 900

   # Download to output directory
   notebooklm download infographic "YYYY-MM-DD-[slug]-[data-name].png"
   ```

5. **CRITICAL: Compress image for WeChat upload:**
   ```bash
   # NotebookLM generates large PNG files (5-10MB) that timeout during WeChat upload
   # ALWAYS compress to JPEG before publishing
   python scripts/compress_image.py "YYYY-MM-DD-[slug]-[data-name].png"

   # This creates: YYYY-MM-DD-[slug]-[data-name]-compressed.jpg (typically < 1MB)
   # Compression: PNG 5.93MB → JPEG 0.68MB (88% reduction, quality=85)
   ```

6. **Insert into HTML output:**
   - Use the COMPRESSED image filename (not the original PNG)
   - Replace CSS-based visualizations with actual infographic images
   - Use proper `<figure>` structure with caption and source
   - Example:
   ```html
   <figure style="margin: 40px 0;">
     <img src="2026-01-18-article-slug-market-growth-compressed.jpg"
          alt="Market Growth Visualization"
          class="article-image">
     <figcaption class="image-caption">
       SaaS市场增长趋势 (2025-2032)
     </figcaption>
     <p class="image-source">
       数据来源：<a href="[source_url]" target="_blank">[Source Name]</a>
     </p>
   </figure>
   ```

7. **Typical infographics to generate** (2-4 per article):
   - Market growth chart (if article discusses market trends)
   - Comparison infographic (traditional vs new approach)
   - Statistics visualization (key percentages/numbers)
   - Process/workflow diagram (if explaining steps)

**Example prompts for common data types:**

- **Market Growth:**
  ```
  "Create a professional infographic showing SaaS market growth from $315B (2025) to $1.13T (2032).
  Use ascending bar chart or line graph. Blue color scheme (#1a5490, #2980b9, #3498db).
  Highlight 20%+ CAGR. Modern business style."
  ```

- **Percentage Trend:**
  ```
  "Create a professional infographic showing 36.3% of new companies are solo-founded in 2026,
  compared to <10% in 2025. Show dramatic 3x+ growth. Blue color scheme matching corporate theme.
  Use pie chart or comparison bars."
  ```

- **Cost Comparison:**
  ```
  "Create a professional side-by-side comparison infographic: Traditional (5-person team, $25k/month,
  $50k+ MRR to break even) vs Solo+AI ($500/month, $5k MRR profitable). Blue color scheme.
  Clear visual contrast."
  ```

**Important notes:**
- Generate infographics AFTER writing full article content
- Only generate for Format 2 (HTML) - not needed for MD/Xiaohongshu/Tweet
- Infographics should enhance, not replace, written content
- Always include proper attribution and source links
- File naming: `YYYY-MM-DD-[article-slug]-[data-description].png`

### 7) Output format - Quad Format Required

**⚠️ 仅在用户确认飞书文档后生成！**

**MANDATORY: Always generate ALL FOUR formats**

**Format 1: Markdown (.md) - 完整专业版**
- Save to `/root/.openclaw/workspace/output/YYYY-MM-DD-[article-title-slug].md`
- Clean markdown with proper heading hierarchy
- **DO NOT include metadata/frontmatter** - Start directly with `# Article Title`
- No YAML header, no version info, no date header

**Format 2: HTML (.html) - 完整专业版**
- Save to `/root/.openclaw/workspace/output/YYYY-MM-DD-[article-title-slug].html`
- **⚠️ INFOGRAPHIC GENERATION REQUIRED**: If article contains core data (market trends, statistics, comparisons), use Phase 4 workflow to generate infographics via notebooklm-api skill BEFORE finalizing HTML
- Use the enhanced HTML structure and styling:
  - **Color scheme**: 墨绿主题 + 砖红点缀双色体系
  - 墨绿（主色）：文字 #556b2f，竖线 #556b2f，背景 #f6fff6
  - 砖红（强调色）：文字 #b74134，背景 #fff8e7，奶黄阴影
  - **Font family**: -apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", "Microsoft YaHei"
  - **Line height**: 1.75 (reduced from 1.9 for tighter spacing)
  - **Max width**: 860px, centered
  - **Headings**: 墨绿配色 (h2: #556b2f 加粗，左侧墨绿竖线)
  - **Blockquote**: 墨绿主题 (#f6fff6 background, #556b2f border, box-shadow)
  - **Enhanced text styles**:
    - `.highlight` - Blue highlight background (linear-gradient)
    - `.highlight-green` - Blue text with blue highlight background
    - `.highlight-green` - DEPRECATED: Use `.highlight-green` instead (unified blue theme)
    - `.highlight-orange` - DEPRECATED: Use `.highlight-green` instead (unified blue theme)
    - `.underline-dotted` - Dotted underline for emphasis (2px dotted #3498db)
    - `.data-box` - Data highlight box with shadow
    - `.key-number` - Key numbers in blue, bold, larger font
  - **Image styles**:
    - `.article-image` - Responsive images with shadow and border-radius
    - `.image-caption` - Centered, italic caption text
    - `.image-source` - Source attribution with clickable links
  - Responsive design with proper viewport meta
- Include complete HTML structure (DOCTYPE, head, body)
- Apply consistent spacing and typography
- **IMPORTANT: Do NOT use `<hr/>` tags between paragraphs** - Use spacing and headings for visual separation instead
- **DO NOT include metadata** - No date, version info, or author metadata in HTML output

### 🚨 微信公众号排版规范 (CRITICAL - 必须遵守)

**⚠️ 权威规范文件：`references/wechat-format-rules.md`（以此为准，不得与该文件冲突）**

**🚨 2026-04-09 重大更新（经验教训）：**

**核心问题**：微信安全过滤会强制覆盖 `<h1>/<h2>/<h3>/<p>/<strong>` 等HTML默认标签的样式（变蓝色），所有CSS class和 `<style>` 块都会被剥离。

**唯一安全方案：所有样式必须用 `<div>` 和 `<span>` 标签的 style="" 内联属性，禁止使用任何被微信强制覆盖的标签。**

排版规范核心要点（完整内容见 `references/wechat-format-rules.md`）：

#### 文章标题（H1 - 用于脚本提取）
```html
<!-- 供 wechat_publish.py 提取标题，必须保留且 display:none -->
<h1 style="display:none;">从张雪峰.skill到金谷园饺子馆.skill，给我们带来的思考</h1>
```

#### 二级标题（Section Title）
```html
<!-- 禁止用 <h2>，微信会强制覆盖为蓝色！必须用 div 内联 -->
<div style="font-size:17px;color:#556b2f;font-weight:bold;margin:28px 15px 14px;padding-left:12px;border-left:4px solid #556b2f;">一、章节标题</div>
```
- 字体：17px，墨绿色 #556b2f，加粗
- 左侧墨绿竖线：4px solid #556b2f
- 左侧留白：padding-left:12px
- 上下间距：margin:28px 15px 14px

#### 正文段落（Body Paragraph）
```html
<!-- 禁止用 <p>，微信会覆盖样式！必须用 div 内联 -->
<div style="margin:0 0 12px;padding:0 15px;line-height:1.8;">正文内容</div>
```
- 段间距：margin:0 0 12px（下一段前留12px）
- 左右留白：padding:0 15px
- 行高：line-height:1.8

#### 重点字词（Highlighted Key Terms）
```html
<!-- 砖红字体 + 奶黄背景，不是红色！ -->
<span style="background:#fff8e7;padding:2px 6px;border-radius:3px;color:#b74134;font-weight:600;">重点字词</span>
```

#### 重点句（Important Sentences - 点下划线）
```html
<!-- 墨绿色点状下划线，不是红色！ -->
<span style="border-bottom:2px dotted #556b2f;padding-bottom:2px;color:#556b2f;">重点句子</span>
```

#### 数字强调（Key Numbers）
```html
<span style="color:#556b2f;font-weight:bold;">12天</span>
```

#### Hook区域（开篇摘要框）
```html
<div style="background:#f6fff6;border-left:5px solid #556b2f;box-shadow:3px 3px 10px rgba(85,107,47,0.12);padding:18px 20px;border-radius:0 10px 10px 0;margin:0 0 24px 0;font-size:15px;line-height:1.9;">
    <span style="color:#556b2f;font-weight:bold;">2026年4月</span>，短短两天内...
</div>
```

#### CTA结尾（必须添加）
```html
<div style="background:#556b2f;padding:16px;border-radius:10px;text-align:center;color:#fff;margin:24px 0 0;">
    <div style="margin:0;color:#fff;font-size:15px;line-height:1.8;">如果你觉得文章对你有所帮助，请关注就行</div>
</div>
```

#### 完整HTML结构规则

| 元素 | ❌ 禁止 | ✅ 正确 |
|------|--------|--------|
| 文章标题 | `<h1>`（会变蓝） | `<h1 style="display:none;">` + 视觉标题用div |
| 二级标题 | `<h2>/<p>`（会变蓝） | `<div style="border-left:4px solid #556b2f;color:#556b2f;">` |
| 正文段落 | `<p>`（会变蓝） | `<div style="margin:0 0 12px;padding:0 15px;">` |
| 加粗强调 | `<strong>`（会变蓝） | `<span style="color:#556b2f;font-weight:bold;">` |
| 重点字词 | class样式（被剥离） | `<span style="background:#fff8e7;padding:2px 6px;border-radius:3px;color:#b74134;">` |
| 重点句下划线 | class样式（被剥离） | `<span style="border-bottom:2px dotted #556b2f;padding-bottom:2px;color:#556b2f;">` |
| CTA区域 | `<p>`（会变蓝） | `<div style="background:#556b2f;...;">` |
| 列表 | `<ul>/<ol>/<li>`（圆点不可控） | `<div style="margin:0 0 6px 20px;">• 内容</div>` |

#### 颜色系统（Jeff品牌色）

| 用途 | 颜色值 | 示例 |
|------|--------|------|
| 二级标题 | #556b2f（墨绿） | `color:#556b2f;font-weight:bold;` |
| 左侧竖线 | #556b2f（墨绿） | `border-left:4px solid #556b2f;` |
| 重点句点下划线 | #556b2f（墨绿） | `border-bottom:2px dotted #556b2f;` |
| 重点字词背景 | #fff8e7（奶黄） | `background:#fff8e7;` |
| 重点字词字体 | #b74134（砖红） | `color:#b74134;` |
| CTA背景 | #556b2f（墨绿） | `background:#556b2f;` |

#### 发布命令（必须使用 -X utf8）
```bash
cd /root/.openclaw/workspace/skills/content-factory && python3 -X utf8 scripts/wechat_publish.py --html "/root/.openclaw/workspace/output/YYYY-MM-DD-article-slug.html" --cover "/root/.openclaw/workspace/output/YYYY-MM-DD-article-slug-cover.png"
```

- **必须加 `-X utf8`**：否则中文会变成 `\uXXXX` 转义序列
- **必须加 `--cover`**：否则封面图使用默认图片
- **禁止元信息**：禁止日期、版本号、版权声明

- **Content structure optimization**:
  - REDUCE bullet points - convert to flowing narrative paragraphs
  - INCREASE first-person narrative ("我发现...", "我观察到...", "在我看来...")
  - Use bullet points ONLY for tool lists or step-by-step instructions
  - Transform data lists into prose with inline highlights
- **WeChat list formatting (CRITICAL for publishing)**:
  - Remove ALL blank lines between `<li>` elements to prevent WeChat from adding extra bullets
  - Format lists compactly: `<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>` (no newlines between items)
  - Apply to both `<ul>` and `<ol>` lists
  - WeChat's parser treats blank lines as new list items, causing visual clutter
  - This is handled automatically by wechat_publish.py script during upload
- **Visual data presentation**:
  - **PREFER NotebookLM-generated infographics** for key data (see Phase 4)
  - Use CSS-based visualizations only as fallback if infographic generation fails
  - Add inline data visualizations using CSS gradients and flexbox
  - Create visual comparison cards for before/after scenarios
  - Use colored boxes with statistics for key data points
  - Include source attribution links for all data visualizations
  - Example: Create gradient boxes showing market growth trends
  - Example: Use side-by-side comparison cards for cost structures
  - Example: Design stat cards with large numbers and context
- **Information source images**:
  - Search for charts/graphs from original sources (Fortune Business Insights, Scalable.news, etc.)
  - If images unavailable, create CSS-based data visualizations
  - Always include `<figure>` with `<figcaption>` and source links
  - Use `<p class="image-source">` with clickable attribution links

**Format 3: Markdown (.md) - 小红书版 (Xiaohongshu Style)**
- Save to `/root/.openclaw/workspace/output/YYYY-MM-DD-[article-title-slug]-小红书.md`
- **🚨 STRICT CHARACTER COUNT (CRITICAL)**:
  - Target: **800-1000 characters** (Chinese chars + English words)
  - **MUST use Python script to verify before sending to user**
  - Verification command: 
    ```bash
    python3 -c "import re; c=re.sub(r'#+\s*|---+|^-\s+|#+\s*$|\n\n+','',open('file.md').read()); print(len(re.findall(r'[\u4e00-\u9fa5]',c))+len(re.findall(r'[a-zA-Z]+',c)))"
    ```
  - If count < 800: Add more content/expansion
  - If count > 1000: Aggressively cut while keeping core message
  - **DO NOT rely on `wc -c`** - it counts bytes not displayable characters
- **Casual, engaging style WITH emojis** (opposite of professional versions)
- **STRICT CHARACTER LIMIT: 800-1000 Chinese characters** (excluding hashtags)
  - ⚠️ **CRITICAL**: Count characters BEFORE finalizing - must be ≥800 AND ≤1000
  - Use Python to verify: `800 <= len(content_without_hashtags) <= 1000`
  - If under 800, add more detail to case study or tips
  - If over 1000, aggressively cut content while keeping core message
  - Priority: Keep case study + key data + actionable tips
- **MUST include at least 1 complete case study** with specific metrics
- **Content structure**:
  - Eye-catching opening with emojis (2-3 sentences)
  - 1-2 key insights or problems
  - 1 complete real case with specific numbers/results
  - 3-5 actionable tips or takeaways (bullet points with emojis)
  - Engaging conclusion with call-to-action
  - **Hashtags at the end** (5-10 relevant hashtags)
- **Tone**: Conversational, exciting, relatable - like sharing a discovery with friends
- **Emoji usage**: Use emojis strategically for emphasis and visual appeal (✨💡🚀📊💪 etc.)
- **Hashtag format examples**:
  ```markdown
  #ClaudeCowork #AI工具 #企业效率 #人工智能 #职场提升 #AI代理 #效率翻倍 #科技趋势
  ```
- **DO NOT include business conversion section** - Keep it short and focused for Xiaohongshu platform
- **Character count verification** (MANDATORY):
  ```python
  # After writing, verify character count
  content = """[your xiaohongshu content]"""
  lines = content.split('\n')
  hashtag_line = [l for l in lines if l.startswith('#')]
  if hashtag_line:
      content_without_hashtags = content.replace(hashtag_line[0], '').strip()
  else:
      content_without_hashtags = content.strip()

  char_count = len(content_without_hashtags)
  assert 800 <= char_count <= 1000, f"Character count {char_count} must be between 800-1000!"
  ```

**Format 4: Text (.txt) - X/Twitter 英文长推文版 (X Pro)**
- Save to `/root/.openclaw/workspace/output/YYYY-MM-DD-[article-title-slug]-tweet.txt`
- **English language only** - Professional, data-driven long-form tweet
- **Maximum length: 1000 characters** (optimized for readability and engagement)
- **MUST include 2-3 complete cases with specific metrics** from the article
- **Content structure**:
  - Strong hook (2-3 sentences defining the core shift/insight)
  - Case 1: Problem → Solution → Results (3-5 bullet points with specific numbers)
  - Case 2: Problem → Solution → Results (3-5 bullet points with specific numbers)
  - Optional Case 3 or security/challenge lesson (if space permits)
  - Paradigm shift summary (3-5 transformation points using →)
  - Industry prediction or trend (Gartner data, market forecast)
  - Brief actionable framework or next steps (optional, 2-3 points)
  - Compelling call-to-action (question or statement)
  - 5-8 relevant hashtags at the end
- **Tone**: Professional yet engaging, authoritative but accessible, Twitter-style brevity
- **Visual structure**: Use separators (━━━), bullet points (•), arrows (→) for clarity
- **Emoji usage**: Minimal - only if it enhances readability (max 2-3 total)
- **Data density**: Include 6-9 specific metrics (percentages, time reductions, ROI)
- **Hashtag format**: 5-8 tags covering technology, industry, and application
  ```
  #AI #ClaudeCowork #EnterpriseAI #Automation #AIAgents #DigitalTransformation #Productivity #FutureOfWork
  ```
- **Focus**: Extract 2-3 most compelling cases with concrete results, maintain Twitter's scannable format while providing depth

**File Naming Convention:**
- Use ISO date format: `YYYY-MM-DD` (e.g., 2026-01-14)
- Followed by article title slug in lowercase with hyphens
- Xiaohongshu version adds `-小红书` suffix before extension
- Tweet version adds `-tweet` suffix before extension
- Examples:
  - `2026-01-14-claude-cowork-enterprise-guide.md` (Professional MD)
  - `2026-01-14-claude-cowork-enterprise-guide.html` (Professional HTML)
  - `2026-01-14-claude-cowork-enterprise-guide-小红书.md` (Xiaohongshu MD)
  - `2026-01-14-claude-cowork-enterprise-guide-tweet.txt` (Twitter/X English)

**Output Directory Structure:**
```

├── 2026-01-14-[article-title-slug].md
├── 2026-01-14-[article-title-slug].html
├── 2026-01-14-[article-title-slug]-小红书.md
└── 2026-01-14-[article-title-slug]-tweet.txt
```

Create the output directory if it doesn't exist.

### 8) WeChat Cover Photo Generation (GLM-Image API)

**IMPORTANT: Before publishing, generate a professional WeChat cover photo using GLM-Image API.**

**WeChat Cover Specifications:**
- **Size**: `900x386` pixels (WeChat Official Account standard)
- **Aspect Ratio**: 21:9 (ultra-wide landscape)
- **Style**: Professional magazine style with minimalist flat vector graphics
- **Format**: PNG or JPEG (compress if > 1MB)

**Cover Photo Generation Workflow:**

1. **Extract article title** from the finalized content
2. **Generate cover photo using GLM-Image API**:
   ```bash
   # Generate cover photo using GLM-Image API
   python scripts/generate_cover_photo.py \
     --title "[article title]" \
     --theme "[article theme]" \
     --output "/root/.openclaw/workspace/output/YYYY-MM-DD-[article-slug]-cover.png"
   ```

3. **Image will be automatically generated at 21:9 ratio (900x386 pixels)**

4. **Compress if needed:**
   ```bash
   # Check file size
   ls -lh "YYYY-MM-DD-[article-slug]-cover.png"

   # If > 1MB, compress to JPEG
   python scripts/compress_image.py "YYYY-MM-DD-[article-slug]-cover.png"
   # Creates: YYYY-MM-DD-[article-slug]-cover-compressed.jpg
   ```

5. **Include cover photo reference** in publishing workflow

**Prompt Engineering Guidelines for Cover Photos:**

**Core Principles:**
- **Title-focused**: Graphics should complement, not compete with the title
- **Minimalist**: Less is more - avoid cluttered designs
- **Professional**: Magazine-quality aesthetics
- **White background**: Pure white (#ffffff) - MANDATORY for all covers
- **Dark blue primary**: Navy blue (藏青色 #1a3a52 or #1a5490) for text and main graphics
- **Accent colors**: Light blue (#3498db), gray (#7f8c8d) for subtle elements only
- **21:9 Ultra-wide**: Design for 21:9 aspect ratio (900x386 pixels)

**Example Prompts by Article Type:**

1. **Tech/AI Articles:**
   ```
   Create a professional WeChat cover image (900x386 pixels, 21:9 ultra-wide landscape).

   Title: [AI/Tech article title]

   Style: Professional magazine cover with minimalist flat vector graphics.
   - Pure white background (#ffffff)
   - Title centered in dark blue (藏青色 #1a3a52)
   - Subtle geometric shapes: circuits, nodes, or abstract tech patterns in dark blue
   - Optional accent: light blue (#3498db) for highlights
   - Clean, modern typography
   - High contrast for mobile readability
   - 21:9 ultra-wide composition
   ```

2. **Business/Enterprise Articles:**
   ```
   Create a professional WeChat cover image (900x386 pixels, 21:9 ultra-wide landscape).

   Title: [Business article title]

   Style: Professional magazine cover with minimalist design.
   - Pure white background (#ffffff)
   - Title centered in navy blue (藏青色 #1a5490)
   - Subtle business graphics: charts, graphs, or geometric patterns in dark blue
   - Optional accent: gray (#7f8c8d) for subtle elements
   - Professional, trustworthy aesthetic
   - Balanced composition
   ```

3. **Tutorial/Guide Articles:**
   ```
   Create a professional WeChat cover image (900x386 pixels, 21:9 ultra-wide landscape).

   Title: [Tutorial/Guide title]

   Style: Professional magazine cover with clear hierarchy.
   - Pure white background (#ffffff)
   - Title centered in dark blue (藏青色 #1a3a52)
   - Minimalist icons or step indicators in dark blue
   - Optional accent: light blue (#3498db) for visual interest
   - Clean, educational aesthetic
   - Easy to scan on mobile
   ```

4. **General Template (Recommended):**
   ```
   Create a professional WeChat Official Account cover image (900x386 pixels, 21:9 ultra-wide landscape).

   Title: [article title - use actual title text]

   Design requirements:
   - Professional magazine style
   - Minimalist flat vector graphics based ONLY on the title keywords
   - Pure white background (#ffffff) - MANDATORY
   - Title text centered, large, and prominent in dark blue (藏青色 #1a3a52 or #1a5490)
   - Graphics and shapes in dark blue/navy (藏青色)
   - Optional accent colors: light blue (#3498db), gray (#7f8c8d) for subtle elements only
   - Clean geometric shapes that relate to title content
   - High contrast for mobile readability
   - Professional typography (sans-serif, bold for title)
   - **21:9 ultra-wide composition** - use horizontal space effectively
   - Suitable for business/professional audience

   Layout:
   - Title occupies center 60% of image
   - Background graphics subtle and non-distracting
   - Adequate white space around title
   - Professional, magazine-quality finish
   ```

**Color Palette (Consistent with Article Theme):**
- **Background**: Pure white (#ffffff) - MANDATORY for all covers
- **Primary**: Dark blue/Navy (藏青色) #1a3a52 or #1a5490 - for title text and main graphics
- **Accent 1**: Light blue #3498db or #2980b9 - for highlights and visual interest
- **Accent 2**: Gray #7f8c8d - for subtle elements
- **Text**: Dark blue for title, dark gray #2c3e50 for subtitles

**Quality Checklist:**
- [ ] Pure white background (#ffffff)
- [ ] Title and graphics in dark blue (藏青色)
- [ ] Title is clearly readable on mobile devices
- [ ] Background graphics don't compete with title
- [ ] Color scheme matches article theme (dark blue primary)
- [ ] Image dimensions are 900x386 pixels (21:9)
- [ ] File size < 1MB (compress if needed)
- [ ] Professional, magazine-quality aesthetic
- [ ] Suitable for business/professional audience

**Integration with Publishing Workflow:**
- Generate cover photo AFTER finalizing article content
- Compress to < 1MB if needed (use `scripts/compress_image.py`)
- Include cover photo path in WeChat publishing API call
- Verify cover photo meets WeChat specifications (size, format, content)

**Error Handling:**
- If GLM generation fails, retry with simplified prompt
- If generation takes too long, check API quota
- If file size > 1MB, compress to JPEG with quality=85
- Notify user if cover generation is skipped

### 9) WeChat Official Account Auto-Publishing

**IMPORTANT: After generating Format 2 (HTML) and cover photo, automatically publish to WeChat Official Account for preview.**

**WeChat Official Account Credentials:**
- Credentials are stored in `.env` file (see Configuration section below)
- **AppID**: Set `WECHAT_APP_ID` in `.env`
- **AppSecret**: Set `WECHAT_APP_SECRET` in `.env`
- Get credentials from: https://mp.weixin.qq.com/ → 设置与开发 → 基本配置

**Publishing Workflow:**

1. **Generate all 4 formats** (MD, HTML, Xiaohongshu, Tweet)
2. **Generate WeChat cover photo** using GLM-Image API (see section 8)
3. **Compress cover photo and infographics** if > 1MB
4. **Extract content from HTML file** for WeChat API
5. **Call publishing script with UTF-8 mode** (CRITICAL on Windows)
6. **Verify encoding and images** in WeChat draft preview
7. **Return preview URL** to user

**Publishing Script Usage (CRITICAL - Windows UTF-8 Mode):**
```bash
# ALWAYS use -X utf8 flag on Windows to prevent encoding errors
python -X utf8 scripts/wechat_publish.py --html "/root/.openclaw/workspace/output/YYYY-MM-DD-[article-title-slug].html"

# WITHOUT -X utf8, Chinese characters will show as \uXXXX escape sequences
# This is a Windows-specific issue due to GBK default encoding
```

**Expected Output:**
```
✓ Access token obtained
✓ Content image uploaded: [filename] -> http://mmbiz.qpic.cn/...
✓ Draft article created
✓ Media ID: WOr7ZIAYNpv...
```

**Verification Checklist:**
- [ ] Check logs for "Content image uploaded" (confirms image upload success)
- [ ] Verify Chinese characters display correctly (not `\uXXXX` sequences)
- [ ] Open WeChat draft preview to confirm images display
- [ ] Document Media ID for reference

**API Endpoints Used:**
- Token: `https://api.weixin.qq.com/cgi-bin/token`
- Draft: `https://api.weixin.qq.com/cgi-bin/draft/add`
- Preview: `https://api.weixin.qq.com/cgi-bin/freepublish/submit`

**Error Handling:**
- If API call fails, save HTML locally and notify user
- Log error details to `publish_errors.log`
- Provide manual publishing instructions

**Security Notes:**
- AppSecret is sensitive - consider moving to environment variable in production
- Access tokens expire after 2 hours - script handles refresh automatically
- Preview links are valid for 24 hours

**Article Ending - Business Conversion (MANDATORY for Format 1 & 2):**

Instead of listing "参考来源" or "References", ALWAYS end Format 1 (MD) and Format 2 (HTML) professional articles with a business conversion section that guides readers to follow and engage for AI consulting services.

**NOTE: Do NOT include this section in Format 3 (Xiaohongshu) - that format should end with hashtags only.**

**Markdown Format (for Format 1):**
```markdown
---

如果觉得这篇文章对您帮助，欢迎关注公众号。
```

**HTML Format (for Format 2, add before `</body>`):**
```html
<p>如果觉得这篇文章对您帮助，欢迎关注公众号。</p>
```

**Important Notes:**
- Do NOT include "参考来源" or "References" sections in any articles
- The business conversion section is MANDATORY for every article
- Customize the contact information placeholder based on user needs
- Keep the tone consistent with first-person narrative: professional, helpful, and approachable
- This section serves as the commercial funnel to convert readers into consulting clients
- **Do NOT use `<hr/>` before the business conversion section** - The h2 heading provides sufficient visual separation

## Quality bar and safety

- Avoid unverifiable claims about video content; summarize only what is available in transcripts or descriptions.
- Keep summaries concise and clearly attributed to sources.
- Avoid direct copying of long transcript passages.
- **Article Writing Standards**:
  - Maintain professional, confident tone without arrogance
  - Use concrete examples and data points
  - Ensure logical flow and clear value proposition
  - Mobile-first readability (short paragraphs, clear hierarchy)
  - Include proper attributions for any referenced content
- **Writing Quality Rules (MANDATORY)**:
  - **精炼表达**: 不要重复相同意思的话语，每句话必须有新信息
  - **禁止废话**: 不要使用"我认为"、"我觉得"、"我相信"等无意义表达，直接陈述观点
  - **禁止杜撰**: 所有案例和数据必须来自研究阶段收集的真实来源，不得编造
  - **直接有力**: 用"是"而不是"我认为是"，用"数据显示"而不是"我觉得数据可能显示"
  - **删除冗余**: 如果删掉某句话不影响理解，就删掉它

## Common Mistakes and Lessons Learned

### ❌ MISTAKE 1: Skipping Tool Dependency Check
**What happened:**
- Assumed yt-dlp was unavailable without checking
- Jumped directly to WebFetch/WebSearch fallback methods
- Missed opportunity to extract rich YouTube content

**Why it's wrong:**
- Tool checking is MANDATORY, not optional
- "Optionally run scripts" means "use if available", NOT "skip if inconvenient"
- Local scripts are PRIMARY method, WebFetch is FALLBACK

**Correct approach:**
```bash
# ALWAYS check first
yt-dlp --version
ls scripts/yt_dlp_search.py
ls scripts/yt_dlp_captions.py

# Then decide execution path based on results
```

### ❌ MISTAKE 2: Misunderstanding "Optional" in Documentation
**What happened:**
- Saw "Optionally run scripts" and interpreted as "can skip"
- Didn't realize local scripts are the PRIMARY YouTube extraction method

**Why it's wrong:**
- "Optional" means "if conditions are met, should use"
- It's about tool availability, not execution priority
- WebFetch is the fallback, not the primary method

**Correct interpretation:**
- IF yt-dlp installed → MUST use scripts (primary method)
- IF yt-dlp missing → inform user, request installation
- ONLY IF user declines → use fallback methods

### ❌ MISTAKE 3: Not Reading Reference Documentation
**What happened:**
- Didn't load `references/youtube_research_checklist.md`
- Missed detailed instructions on YouTube content extraction

**Why it's wrong:**
- Reference docs contain critical workflow details
- They provide step-by-step guidance for complex tasks
- Skipping them leads to incomplete execution

**Correct approach:**
```bash
# ALWAYS load reference docs when mentioned
Read("references/youtube_research_checklist.md")
```

### ❌ MISTAKE 4: Premature Fallback to Alternative Sources
**What happened:**
- WebFetch failed → immediately switched to WebSearch for articles
- Didn't exhaust all YouTube extraction methods first

**Why it's wrong:**
- YouTube content provides unique value (case studies, personal stories, demos)
- Articles/reports can't fully replace video content richness
- Should try ALL methods before giving up on primary source

**Correct decision tree:**
```
YouTube needed?
    ↓
Check yt-dlp installed?
    ↓ YES                           ↓ NO
Try scripts                    → Inform user + install
    ↓ SUCCESS    ↓ FAIL              ↓
Continue      → Try WebFetch    → Retry scripts
                    ↓ FAIL              ↓ FAIL
              Request user URLs   → Use fallback sources
                    ↓ FAIL         (document limitation)
              Use fallback sources
              (document limitation)
```

### ❌ MISTAKE 5: WeChat Publishing Encoding Errors (Windows)
**What happened:**
- Published article to WeChat showed Unicode escape sequences instead of Chinese characters
- Example: `\u6211\u752872\u5c0f\u65f6` instead of "我用72小时"
- Draft created successfully but content was unreadable

**Why it's wrong:**
- Windows default encoding is GBK, not UTF-8
- BeautifulSoup HTML parsing inherits system encoding
- JSON serialization with `ensure_ascii=False` alone is insufficient
- The issue affects the entire Python process, not just file I/O

**Root cause:**
- Windows console uses GBK encoding by default
- Python's default encoding follows system locale
- HTML parsing and string operations use default encoding
- WeChat API receives incorrectly encoded content

**Correct approach:**
```bash
# ALWAYS use Python UTF-8 mode on Windows for WeChat publishing
python -X utf8 scripts/wechat_publish.py --html "/root/.openclaw/workspace/output/article.html"

# NOT just PYTHONIOENCODING (insufficient):
# PYTHONIOENCODING=utf-8 python scripts/wechat_publish.py  # ❌ Only fixes I/O

# The -X utf8 flag forces UTF-8 for:
# - File I/O operations
# - String encoding/decoding
# - HTML parsing (BeautifulSoup)
# - JSON serialization
# - HTTP request bodies
```

**Verification:**
- Check WeChat draft preview immediately after publishing
- Look for Chinese characters rendering correctly
- If you see `\uXXXX` sequences, encoding failed
- Re-run with `-X utf8` flag

**Prevention checklist:**
- [ ] Always use `python -X utf8` for WeChat publishing on Windows
- [ ] Test with a short article first to verify encoding
- [ ] Check draft preview before announcing success
- [ ] Document the Media ID for reference

### ❌ MISTAKE 6: NotebookLM Infographic Too Large for WeChat Upload
**What happened:**
- Generated 6.0MB PNG infographic using NotebookLM API
- WeChat image upload timed out: `TimeoutError('The write operation timed out')`
- Article published successfully but without the infographic
- User reported: "图片没有加载进去" (images not loaded)

**Why it's wrong:**
- NotebookLM generates high-resolution PNG files (often 5-10MB)
- WeChat API has 10MB limit but large files timeout frequently
- Network upload timeout occurs before reaching size limit
- PNG format is uncompressed and inefficient for web delivery

**Root cause:**
- NotebookLM prioritizes quality over file size
- PNG format preserves all pixel data without compression
- WeChat's upload endpoint has strict timeout limits (60 seconds)
- Large files fail silently - draft created but image missing

**Correct approach:**
```bash
# Step 1: Generate infographic with NotebookLM (as usual)
notebooklm generate infographic "prompt..." --json
notebooklm artifact wait <artifact_id> --timeout 600
notebooklm download infographic ./output.png

# Step 2: ALWAYS compress before WeChat upload
python -c "
from PIL import Image
import os

# Convert PNG to JPEG with quality optimization
img = Image.open('output.png').convert('RGB')
img.save('output-compressed.jpg', 'JPEG', quality=85, optimize=True)

# Verify size reduction
original_mb = os.path.getsize('output.png') / 1024 / 1024
compressed_mb = os.path.getsize('output-compressed.jpg') / 1024 / 1024
print(f'Original: {original_mb:.2f}MB → Compressed: {compressed_mb:.2f}MB')
"

# Step 3: Update HTML to reference compressed image
# Replace: <img src="output.png" ...>
# With:    <img src="output-compressed.jpg" ...>

# Step 4: Publish with compressed image
python -X utf8 scripts/wechat_publish.py --html "/root/.openclaw/workspace/output/article.html"
```

**Compression results:**
- Original PNG: 5.93MB → Compressed JPEG: 0.68MB (88% reduction)
- Upload time: Timeout → 21 seconds (successful)
- Visual quality: Minimal degradation at 85% JPEG quality

**Prevention checklist:**
- [ ] Always compress NotebookLM infographics before WeChat upload
- [ ] Target file size: < 1MB for reliable upload
- [ ] Use JPEG format with quality=85 for good balance
- [ ] Verify image uploaded successfully in logs: "Content image uploaded: ... -> http://mmbiz.qpic.cn/..."
- [ ] Check WeChat draft preview to confirm image displays
- [ ] If upload fails, reduce JPEG quality to 75 or resize dimensions

**Image compression script (reusable):**
```python
# Save as scripts/compress_image.py
from PIL import Image
import sys
import os

def compress_for_wechat(input_path, output_path=None, quality=85):
    """Compress image for WeChat upload (target < 1MB)"""
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}-compressed.jpg"

    img = Image.open(input_path)
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')

    img.save(output_path, 'JPEG', quality=quality, optimize=True)

    original_mb = os.path.getsize(input_path) / 1024 / 1024
    compressed_mb = os.path.getsize(output_path) / 1024 / 1024

    print(f"Original: {original_mb:.2f}MB")
    print(f"Compressed: {compressed_mb:.2f}MB ({100*(1-compressed_mb/original_mb):.1f}% reduction)")
    print(f"Output: {output_path}")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compress_image.py <input_image> [output_image] [quality]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85

    compress_for_wechat(input_path, output_path, quality)
```

**Usage:**
```bash
# Compress with default settings (quality=85)
python scripts/compress_image.py infographic.png

# Compress with custom quality
python scripts/compress_image.py infographic.png output.jpg 75

# Compress and specify output path
python scripts/compress_image.py infographic.png compressed.jpg
```

### ✅ BEST PRACTICES

1. **Always Check Tools First**
   - Run dependency checks before starting research
   - Inform user of tool status
   - Don't assume unavailability

2. **Follow Priority Order Strictly**
   - Primary method → Fallback method → Last resort
   - Don't skip steps in the decision tree
   - Document why each method failed

3. **Be Transparent with User**
   - Tell user which tools are available
   - Explain which methods you're using
   - Inform if content quality is degraded due to tool limitations

4. **Read All Reference Documentation**
   - Load checklist files when mentioned
   - Follow detailed workflows in reference docs
   - Don't improvise when guidance exists

5. **Systematic Troubleshooting**
   - If A fails, check why before trying B
   - Don't jump from A to D without trying B and C
   - Record failure reasons for future improvement

6. **WeChat Publishing on Windows (CRITICAL)**
   - ALWAYS use `python -X utf8` flag for WeChat publishing
   - Verify encoding in draft preview immediately
   - Check for `\uXXXX` sequences indicating encoding failure
   - Re-run with UTF-8 mode if Chinese characters don't display

7. **NotebookLM Infographic Workflow**
   - Generate infographic with NotebookLM as usual
   - ALWAYS compress PNG to JPEG before WeChat upload
   - Target file size: < 1MB for reliable upload
   - Use `scripts/compress_image.py` for consistent compression
   - Update HTML to reference compressed image filename
   - Verify image upload success in logs before announcing completion

8. **Image Compression for WeChat**
   - Convert PNG to JPEG with quality=85
   - Check compressed file size (should be < 1MB)
   - If still too large, reduce quality to 75 or resize dimensions
   - Verify image displays correctly in WeChat draft preview
   - Keep original PNG for archival purposes

## Configuration

### Environment Setup

All API keys and credentials are stored in `.env` file for security and easy management.

**Setup Steps:**

1. **Copy the example file**:
   ```bash
   cd ~/.claude/skills\content-factory
   copy .env.example .env
   ```

2. **Edit .env and add your credentials**:
   ```env
   # WeChat Official Account (Required for auto-publishing)
   WECHAT_APP_ID=your-wechat-app-id
   WECHAT_APP_SECRET=your-wechat-app-secret
   ```

3. **Get your credentials**:
   - **WeChat Credentials**: https://mp.weixin.qq.com/ → 设置与开发 → 基本配置
   - **NotebookLM**: Authenticate with `notebooklm login` (for cover photo generation)

4. **Verify configuration**:
   ```bash
   python scripts/check_env.py
   ```

**Important**:
- Never commit `.env` file to Git (it's in `.gitignore`)
- Keep `.env.example` as a template (safe to commit)
- See `API_KEY_SETUP.md` for detailed setup instructions
- See `CONFIGURATION.md` for configuration management details

## Resources

**Research Tools:**
- `scripts/yt_dlp_captions.py` - Download YouTube captions/transcripts
- `scripts/yt_dlp_search.py` - Search and collect YouTube metadata
- `scripts/compress_image.py` - Compress images for WeChat upload
- `scripts/wechat_publish.py` - Auto-publish to WeChat Official Account
- `notebooklm-api` skill - Generate infographics and cover photos
- WebSearch tool - Search across all web sources
- WebFetch tool - Fetch and extract content from URLs

**Reference Guides:**
- `references/youtube_research_checklist.md` - YouTube-specific research workflow
- `references/web_research_guide.md` - Multi-source web research best practices
- `references/wechat_viral_frameworks.md` - Article frameworks and hooks
- `references/wechat_publishing_guide.md` - WeChat publishing documentation
- `references/reference.html` - **HTML template and styling reference for output**

**Templates:**
- `assets/wechat_outline_template.md` - Outline template (optional)

**Output Directory:**
- `/root/.openclaw/workspace/output/` - Target directory for generated MD, HTML, Xiaohongshu, Tweet files, and cover photos

---

如果觉得这篇文章对您帮助，欢迎关注公众号。
```

