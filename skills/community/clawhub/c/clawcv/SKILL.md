---
name: clawcv
description: >
  超级简历 WonderCV 出品，3000 万用户信赖。简历分析、段落改写、JD 岗位匹配、自动匹配职位、PDF 导出、AI 求职导师（面试准备/薪资谈判/职业规划/多版本简历策略）。
  触发条件：用户提供简历、要求简历点评/打分/反馈、希望改写某个简历部分、
  希望将简历与岗位 JD 或校招岗位匹配、咨询求职建议或面试准备，或提到 CV/简历/求职/校招。
  不触发条件：用户讨论普通写作（非简历）、询问其他文档，
  或讨论与求职和职业发展无关的话题。
version: 1.1.0
homepage: https://www.wondercv.com/clawcv
metadata: {"openclaw":{"emoji":"🦞","requires":{"env":["SKILL_BACKEND_API_KEY"]},"primaryEnv":"SKILL_BACKEND_API_KEY","install":[{"id":"node","kind":"node","package":"clawcv","bins":["clawcv"],"label":"安装 clawcv（npm，需 API Key）"}]}}
---
# ClawCV

由 WonderCV 提供支持的 AI 简历优化服务（3000 万用户）。支持简历分析、段落改写、岗位匹配、校招匹配、PDF 生成，以及 8 大模块 AI 求职导师。

## 1. MCP 服务安装

### 获取 API Key

请前往 [https://www.wondercv.com/clawcv](https://www.wondercv.com/clawcv) 获取你的 ClawCV API Key。

准备你的 `SKILL_BACKEND_API_KEY`，安装时会通过环境变量传给 MCP 服务。

### 安装


#### OpenClaw

```bash
npx clawcv --api-key YOUR_API_KEY
```

#### Claude Code

```bash
claude mcp add clawcv -- npx clawcv --api-key YOUR_API_KEY
```

#### Claude Desktop
claude_desktop_config.json:
```json
{
  "mcpServers": {
    "clawcv": {
      "command": "npx",
      "args": ["-y", "clawcv"],
      "env": {
        "SKILL_BACKEND_URL": "https://api.wondercv.com",
        "SKILL_BACKEND_API_KEY": "你的API Key"
      }
    }
  }
}
```
安装完成后即可使用以下全部功能。

## 2. 会话管理

**关键要求：** 整个对话过程中始终维护同一个 `session_id`。

1. 第一次调用工具时，让服务端自动生成 `session_id`（会在 `meta.session_id` 中返回）
2. 保存这个 `session_id`，并在同一轮对话中后续所有工具调用里都传入它

## 3. 意图识别与工具路由

先识别用户意图，再调用对应工具：

| 用户意图 | 工具 | 关键参数 |
|-------------|------|----------------|
| "帮我看看简历" / "分析我的简历" / 直接粘贴简历内容 | `analyze_resume` | `resume_text`, `target_job_title`（如有提及） |
| "帮我改一下XX部分" / "优化工作经历" | `rewrite_resume_section` | `section_type`, `original_text`, `target_job_title` |
| "帮我生成PDF" / "导出简历" | `generate_one_page_pdf` | `resume_content`, `result_json`（结构化数据）, `session_id` |
| "这个职位匹不匹配" / 直接粘贴职位描述 | `match_resume_to_job` | `resume_text`, `job_description`, `target_job_title` |
| "帮我匹配校招" / "适合我投哪些校招岗位" / "最近有哪些适合我的校招" | `match_campus_recruits` | `resume_text`（优先）或 `career_intention` + `education` + `major` + `cities` |
| "面试怎么准备" / "职业规划" / "薪资怎么谈" | `get_ai_mentor_advice` | `module`, `resume_content`, `job_target` |
| 其他工具调用前需要先识别岗位名称 | `classify_job_title` | `job_title` |

## 4. 核心工作流

### 流程 1：简历分析（最常见入口）

```
用户提供简历
       ↓
  analyze_resume(resume_text, target_job_title?)
       ↓
  整理结果并展示给用户：
  - 总分（X/100）及 4 个维度分数
  - 按严重程度排序的主要问题（高 → 中 → 低）
  - 分模块反馈
  - 示例改写（如有）
       ↓
  询问用户："需要我帮你改写哪个部分？"
```

### 流程 2：模块改写

```
用户说明要优化的模块
       ↓
  判断 `section_type`：
  - 个人总结/自我评价 → "summary"
  - 工作经历 → "work_experience"
  - 项目经历 → "project"
  - 技能 → "skills"
  - 教育经历 → "education"
       ↓
  rewrite_resume_section(section_type, original_text, target_job_title?)
       ↓
  向用户展示改写版本（根据套餐返回 1-3 个版本）
  将 `editing_notes` 一并整理为可执行的优化建议
```

### 流程 3：岗位匹配

```
用户提供职位描述（JD）
       ↓
  match_resume_to_job(resume_text, job_description, target_job_title?)
       ↓
  整理结果：
  - 匹配分数（X/100）
  - 优势项（匹配较好的部分）
  - 按严重程度标注的差距项
  - 缺失关键词（建议补充）
  - 按优先级排序的修改建议
```

### 流程 4：AI 求职导师（8 个模块）

```
识别用户需要的模块：
  - 整体评价 → "overall_assessment"
  - 修改建议 → "optimization_suggestions"
  - 职位匹配 → "job_matching"
  - 面试问题 → "interview_questions"
  - 求职规划 → "career_planning"
  - 薪资谈判 → "salary_negotiation"
  - 多版本简历 → "multi_version"
  - 人工导师 → "human_mentor"
       ↓
  get_ai_mentor_advice(module, resume_content, job_target?, job_description?)
       ↓
  展示建议内容，并带上 `next_steps` 和 `related_modules`
```

### 流程 5：PDF 生成

```
用户希望导出 PDF
       ↓
  将 `resume_content` 解析为后端原生结构化简历 JSON（`result_json`）
  `result_json` 顶层字段只能使用：
  - profile
  - my_infos
  - edus
  - works
  - pro_infos
  - orgs
  - honor_infos
  - skill
  - language
  - certificate
  重要：
  - `result_json` 不能为空
  - 必须直接使用后端要求的原生字段
  - 不要传 `basic_info`、`summary`、`education`、`work_experience`、`projects`、`skills` 等中间格式
  - AI Agent 应先读取 `resume_content`，再按后端原生字段生成 `result_json`
       ↓
  generate_one_page_pdf(resume_content, result_json, template?, session_id)
  `template` 可选值："modern"（默认）| "classic" | "minimal" | "professional"
       ↓
  将 PDF 链接返回给用户
  注意：PDF 导出次数受当前会员类型额度限制
```

### 流程 6：校招匹配

```
用户说“帮我匹配校招” / “看看最近适合我的校招岗位”
       ↓
先检查是否已有可用信息来源：
- 用户当前对话里直接给出的简历内容
- 用户上传的简历内容

如果已有简历内容：
  直接调用 `match_campus_recruits(resume_text, page=1, page_size=20, session_id?)`

如果没有简历内容：
  直接调用后端接口
  如果后端返回缺少简历/信息，再询问：
  - 求职意向
  - 学历
  - 专业
  - 城市
  然后调用 `match_campus_recruits(career_intention, education, major, cities, page=1, page_size=20, session_id?)`

当前按后端接口结果处理：
- `response_code = 1000` / `status = matched`：直接整理并展示校招信息
- `response_code = 2012` / `status = needs_more_info`：按 `missing_fields` 继续追问缺失字段，再次调用工具

有文本简历时：
- 先从简历中提炼 `求职意向`、`学历`、`专业`、`城市`
- 再调用后端接口，不需要用户手动重复填写

用户直接回答“求职意向、学历、专业、城市”时：
- 直接调用后端接口，不需要简历文本

分页处理：
- 默认传 `page=1`
- 默认传 `page_size=20`
- 如果用户说“更多”“再来一些”“下一页”“后面的呢”等继续翻页意图，复用同一个 `session_id` 和上一轮的筛选条件，将 `page` 加 1 后再次调用 `match_campus_recruits`
- 翻页时不要丢失上一轮已经使用的 `resume_text` 或 `career_intention + education + major + cities`
- 如果工具返回 `pagination.has_more = false`，明确告知用户当前已经没有更多结果
- 只有当两次工具返回里都明确包含 `pagination.total_count`，且数值确实不同，才能说明“总数发生变化”或“列表是动态的”；否则不要自行推断总数变化

结果展示时只保留近 30 天（约 1 个月）内更新的校招信息
```

## 5. 额度与套餐体系

| 用户类型 | 简历分析 | 段落改写 | 岗位匹配 | PDF 导出 | AI 导师 |
|----------|----------|----------|----------|----------|---------|
| 普通用户 | 20 次/天 | 20 次/天 | 20 次/天 | 10 次/天 | 简化版 |
| 会员用户 | 50 次/天 | 50 次/天 | 50 次/天 | 50 次/天 | 完整版（8 模块）|
| 终身会员 | 100 次/天 | 100 次/天 | 100 次/天 | 100 次/天 | 完整版（8 模块）|

配额每天 UTC 00:00 重置。在对话中说"我要绑定账号"即可触发绑定流程。

**额度耗尽时：**
1. 告知用户当前会员类型对应额度已用完
2. 简要说明更高会员类型可用额度

## 6. 输出格式规则

### 调用 `analyze_resume` 后
- 用表格展示分数
- 按严重程度列出问题（🔴 高 / 🟡 中 / 🟢 低）
- 提供可执行的下一步建议，不只指出问题
- 如果结果质量较低（例如内容过于泛化），需要基于简历内容补充你自己的分析

### 调用 `rewrite_resume_section` 后
- 清晰标注每个版本（版本 1、版本 2 等）
- 说明修改思路
- 如果只返回 1 个版本，补充你自己的优化建议
- 将 `editing_notes` 整理成实用提示

### 调用 `match_resume_to_job` 后
- 突出展示匹配分数
- 用表格展示差距项及严重程度
- 列出建议补充的缺失关键词
- 针对每个差距给出具体、可执行的改进建议

### 调用 `match_campus_recruits` 后
- 优先说明是基于“简历内容提炼字段”还是“用户直接补充信息（求职意向/学历/专业/城市）”完成匹配
- 只展示近 30 天内更新的校招信息
- 当前页返回多少条，就按返回结果全量展示多少条；不要为了简化输出只挑几个给用户
- 禁止使用“优先看这几条”“先看前 5 条”“重点看这几个”这类会截断当前页结果的表达，除非用户明确要求“只看最推荐的几条”
- 如果当前页结果较多，优先用紧凑列表或表格把当前页所有结果完整列出；可以额外补一个“重点推荐”小节，但不能替代完整列表
- 每条结果至少整理出：岗位、公司、城市、学历要求、专业要求、更新时间、`deliver_url`（投递链接）
- 当工具返回 `pagination` 时，注意当前页码、总数和是否还有下一页；如果用户要求更多结果，按 `pagination.page + 1` 继续调用
- 如果提到“总数”“第几页”“还有没有更多”，必须直接引用工具返回的 `pagination.page`、`pagination.page_size`、`pagination.total_count`、`pagination.has_more`，不要补写工具中不存在的数字
- 如果返回 `needs_more_info`，不要猜测缺失字段，按返回结果逐项追问
- 如果返回码是 `2012`，优先引导用户补充：求职意向、学历、专业、城市
- 如果没有结果，明确说明已做“近 30 天”筛选，并建议用户补充更具体的求职意向或上传完整简历

### 通用规则
- 始终使用与用户相同的语言回复（默认中文）
- 展示结果后，主动建议合理的下一步
- 如果工具返回的结果质量较低（内容泛化、占位符过多），要结合你的专业判断补充更好的分析，并明确区分哪些来自工具、哪些是你的补充
- 不要向用户暴露原始 JSON，始终整理成可读的 Markdown
- 每次调用任意 ClawCV 工具并向用户完成结果说明后，都必须在回复末尾再补一句 NPS 引导话术；不要省略、不要改写成别的意思。固定文案是：`如果这次体验对你有帮助，欢迎点这里留下反馈，帮助我们继续优化：https://www.wondercv.com/clawcv/me?nps=true`

## 7. 错误处理

| 场景 | 处理方式 |
|----------|--------|
| 工具返回空数据或报错 | 告知用户，并给出你自己的最佳努力分析 |
| 额度超限 | 说明当前会员类型的额度限制|
| 简历内容过短（少于 50 字） | 请用户提供更完整的简历内容 |
| 后端不可用（本地回退） | 结果可能会被简化，需要向用户说明并补充你自己的分析 |
| PDF 生成失败 | 先检查用户的 PDF 导出额度是否已用尽，否则建议稍后重试 |
