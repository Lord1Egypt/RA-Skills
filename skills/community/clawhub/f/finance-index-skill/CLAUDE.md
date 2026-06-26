# Project Memory: 汇添富基金 · 添富市场风向标 Qclaw Skill

## User Profile

- **Name**: PZ
- **Role**: 汇添富基金公司成员，负责理财通代销平台的机构店铺运营
- **Email**: <chenpeizhuan@hotmail.com>

## Project Overview

为汇添富基金在腾讯理财通代销平台的机构店铺设计一款 Qclaw Skill——"指数通"，帮助用户获取金融市场资讯解读和指数板块推荐。

## Key Decisions (已确认)

- **Skill命名**: "指数通"
- **板块展示**: 对话页展示3个板块
- **跳转页设计**: 仅展示指数信息，不列具体基金产品（最保守合规方案）
- **去品牌化策略**: Skill日常输出中不提及汇添富基金，避免用户觉得是广告；
- **合规红线**:
  - 不分析用户个人持仓
  - 不推荐具体基金产品
  - 可推荐关注指数板块（如中证红利000922等）
  - 每条AI回复末尾附合规声明

## **1. Think Before Coding**

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## **2. Simplicity First**

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## **3. Surgical Changes**

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## **4. Goal-Driven Execution**

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.


## Architecture: Phase 1 vs Phase 2

### Phase 1 — 零开发轻量上线

- **技术架构**: 纯 SKILL.md + references/ 静态知识文件
- **数据来源**: AI模型自身知识 + references/中的预置指数信息
- **无需开发**: 不依赖MCP、API、后端服务
- **迭代方式**: 每周根据用户反馈更新SKILL.md和references文件
- **references文件规划**:
  - 指数名单（\~1000条）应按主题拆分为多个小文件（每个<15KB）
  - 建议建立轻量索引文件 index\_catalog.json（仅含代码+名称+分类）
  - 分类文件如 index\_broad\_market.json、index\_tech.json、index\_dividend.json 等
  - ⚠️ 注意：OpenClaw bootstrapMaxChars 默认20,000字符，超大文件会被截断

### Phase 2 — 添富MCP实时数据

- **技术架构**: SKILL.md + 自研"添富MCP Server"
- **数据来源**: 聚源数据、同花顺iFinD、阿尔法派资讯等（通过添富MCP统一封装）
- **用户无需配置第三方MCP/API**: 添富MCP统一提供付费资讯和数据
- **⚠️ Qclaw MCP现状**: Qclaw的MCP功能"暂未开放"，需等待腾讯开放后才能实施
- **⚠️ Plugin Bundle**: Qclaw目前不支持Plugin Bundle，用户可能需要手动配置MCP
- **数据风险与应对**:
  - API密钥泄露 → 服务端代理，不暴露给客户端
  - 数据源不稳定 → 多源备份 + 降级策略
  - 版权风险 → 二次加工解读，不原文转载
  - 用户成本 → 免费增值模式
  - 安全漏洞 → 输入校验 + 权限最小化

## Core Value Proposition

"资讯→机会→指数"三段式解读引擎：把一条财经资讯，变成一个可行动的投资视角。这是ClawHub金融类Skill的市场空白。

## Skill Five Core Features

1. **热点解读**: 政策出台、板块异动，AI帮你30秒看懂背后逻辑
2. **每日风向**: 每天早上推一份市场关键词，结合宏观与行业动态（微信主动推送）
3. **指数雷达**: 追踪用户关心的主题指数走势，可跳转理财通指数详情页
4. **主题探索问答**: 用户自由提问宏观/板块问题，AI给出有观点的回答
5. **指数图谱科普**: 沪深300/中证500区别等知识问答，长效留存钩子

## Competitive Landscape (as of March 2026)

- **ClawHub**: 13,000+ Skills, 金融投资类311+个(9.5%)
- **SkillHub**: 腾讯中国版，2026.3.12上线，精选Top50+安全审计
- **主要竞品**:
  - 妙想Skills（专业投研，六大场景，机构级数据，门槛高）
  - 36氪官方Skill（资讯聚合，热点追踪，缺二次解读）
  - tushare-finance（数据接入，220+接口，技术门槛高）
  - Stock Watcher（行情监控，同花顺数据，功能浅）
- **汇添富差异化**: 持牌机构背书 + 投研团队视角 + "资讯→指数"解读链路

## Platform Context

### Qclaw vs OpenClaw 关键区别

- **Qclaw**: 腾讯电脑管家团队出品的产品化封装，微信直联+低门槛部署
- **OpenClaw**: 开源AI Agent框架，本地执行，完整生态
- **兼容性**: Qclaw兼容OpenClaw的SKILL.md格式，可使用ClawHub上5000+技能
- **MCP限制**: ⚠️ Qclaw的MCP servers功能**暂未开放**（截至2026年3月）
- **Plugin Bundle**: ⚠️ Qclaw目前**不支持**Plugin Bundle
- **Skill更新**: 用户安装后，Skill更新机制取决于来源（ClawHub/SkillHub可推送更新）

### 理财通店铺

- 类似汇添富真实店铺页(蓝底+CUAM logo+标签栏)
- 参考数据源: 财新网caixin.com、中证指数官网、国证指数官网、汇添富99fund.com

## SKILL.md 技术规范

- **格式**: YAML frontmatter（name, description, version, metadata）+ Markdown body
- **关键字段**: user-invocable: true, metadata.openclaw\.compatibility: ">=0.8"
- **Body内容**: 角色定义、工作流场景、输出格式、合规约束、数据源说明、输入输出示例
- **references/文件夹**: 静态知识文件，按需加载
- **Context限制**: \~200K tokens上限，bootstrapMaxChars默认20,000字符

## User Journey

发现(店铺页) → 安装(三步引导) → 体验(微信对话) → 转化(点击指数→跳转理财通) → 留存(每日推送)

## Page Design (三屏)

1. **理财通店铺页**: 蓝色品牌头部 + Skill深蓝卡片 + 场景横滑卡片 + 三步安装引导 + 信任背书
2. **Qclaw ClawBot对话页**: 技能身份卡 + 行情数据卡 + 3色板块卡(红/蓝/金) + 追问按钮 + 合规声明
3. **指数详情页**: 指数信息(走势/PE/股息率) + 风向标观点卡 + 相关指数 + "搜索相关产品"按钮

## Deliverables

- `htf_skill_prototype_v2.html` — 三屏手机端原型图
- `htf_skill_project_doc.docx` — 项目文档（竞品分析+功能设计+页面方案+技术架构）
- `market-compass-skill/SKILL.md` — Skill示例文件（一期版本）
- `.claude/CLAUDE.md` — 本记忆文件

## Next Steps

- [ ] Skill命名最终确认（备选：A股行情解读、财经资讯解读、指数板块雷达等）
- [ ] 编写正式SKILL.md及references知识库
- [ ] 与汇添富研究团队对接投研框架
- [ ] 合规部门审核页面文案和Skill输出模板
- [ ] 一期Skill上线ClawHub/SkillHub
- [ ] 跟进Qclaw MCP开放进度（影响二期时间线）
- [ ] 二期：开发添富MCP Server
- [ ] 用户活动设计（复盘报告、成长计划、模拟组合等）

