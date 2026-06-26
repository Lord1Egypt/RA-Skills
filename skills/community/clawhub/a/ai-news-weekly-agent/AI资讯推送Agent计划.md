# AI 资讯周报 Agent（开源项目说明）

这个项目用于每周自动汇总 AI 圈的高价值信息，输出一份中文可读、结构化、可追溯的 Markdown 周报，并支持以 OpenClaw Skill 形式运行。

---

## 项目目标

解决三个实际问题：

- 信息太散：官方新闻、行业媒体、论文、开源动态分布在不同平台
- 信息太杂：同质内容多、噪声高、难以持续跟踪
- 输出不稳定：很多工具能抓取，但难产出长期可读的周报

因此本项目聚焦“稳定产出周报”，而不是做重型资讯平台。

---

## 当前功能（v1）

- 周报时间窗默认 7 天（`168h`）
- 自动聚合：官方发布、行业资讯、开源动态、论文研究、OpenClaw 热榜
- 论文占比控制（默认上限 20%）
- 每条保留来源链接与发布日期
- OpenClaw 热榜输出 Top 3（排名、发布者、用途、链接）
- 使用 LLM 生成中文长文解读（尽量 200 字以上）
- 产出路径：`daily_docs/ai_weekly_YYYYMMDD.md`

---

## 产出策略

- 新闻优先：优先保留官方和行业新闻
- 论文限流：默认论文不超过 20%
- 官方补位：官方新闻不足时使用更宽窗口补齐
- 可追溯：正文与链接区都保留发布日期
- 异常可见：抓取失败会记录到“抓取异常”章节

---

## OpenClaw Skill 形式
推荐触发方式：

- `生成AI周报`
- `生成本周周报`
- `刷新OpenClaw热榜`

推荐执行命令：

```bash
python3 run_daily_digest.py --use-llm --window-hours 168 --max-paper-ratio 0.2 --min-official-items 3
```

输出文件：

- `daily_docs/ai_weekly_YYYYMMDD.md`

---

## 环境变量与密钥安全

本项目支持两种配置方式：

1. 用户本地 `.env`
2. OpenClaw 运行环境注入变量

必填变量：

- `ARK_API_KEY`
- `ARK_ENDPOINT_ID`（推荐）

可选变量：

- `ARK_MODEL`
- `DIGEST_WEBHOOK_URL`

开源安全约定：

- 仓库不提交真实 `.env`
- 仓库只提交 `.env.example`
- `.gitignore` 默认忽略 `.env` 与生成文件

`.env.example` 示例：

```env
ARK_API_KEY=your_ark_api_key_here
ARK_ENDPOINT_ID=ep-your-endpoint-id
ARK_MODEL=model_name
DIGEST_WEBHOOK_URL=
```

> 说明：真实 key 只应存在于运行环境，不应进入仓库、日志、截图或 issue。

---

## 仓库结构建议

```text
ai-weekly-agent/
  run_daily_digest.py
  sources.json
  SKILL.md
  README.md
  LICENSE
  .env.example
  .gitignore
  daily_docs/
```

---

## 快速开始

```bash
python3 run_daily_digest.py --use-llm
```

常用参数：

- `--window-hours 168`：周报时间窗（默认）
- `--max-paper-ratio 0.2`：论文占比上限
- `--min-official-items 3`：官方新闻最小目标条数
- `--focus-skill "tavily"`：追踪某个 OpenClaw skill 排名


### 信源：

1. **官方发布类**：OpenAI、Anthropic、Google AI、Meta AI、Microsoft AI 等官方 Blog
2. **研究论文类**：arXiv（cs.AI/cs.CL/cs.CV）、Papers with Code、Semantic Scholar 热门
3. **代码与开源类**：GitHub Trending、Hugging Face Trending、Awesome 系列仓库
4. **行业媒体类**：TechCrunch AI、The Verge AI、VentureBeat AI、MIT Tech Review AI
5. **社区讨论类**：Reddit（r/MachineLearning 等）、Hacker News、X（Twitter）列表
6. **中文资讯类**：机器之心、量子位、新智元、36Kr AI 相关栏目
7. **国内官方模型类**：国内大模型厂商官网、开发者平台、官方公众号

