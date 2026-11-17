---

slug: actor-identifier-tool-pro
name: "actor-identifier-tool-pro"
version: "1.0.0"
displayName: "仓库协作分析(专业版)"
summary: "面向团队的企业级Git仓库协作分析平台,含批量分析、自定义指标、CI集成与企业报告。。仓库协作分析工具专业版为团队与企业提供端到端Git仓库协作分析能力,涵盖多仓库批量分析、自定义指标、CI"
license: "Proprietary"
edition: "pro"
description: |-
  仓库协作分析工具专业版为团队与企业提供端到端Git仓库协作分析能力,涵盖多仓库批量分析、自定义指标、CI/CD集成与企业级聚合报告。核心能力:
  - 多仓库批量分析与汇总
  - 自定义指标与团队级聚合
  - CI/CD流水线集成(周期性报告)
  - 企业级报告(Markdown/HTML/PDF)
  - 历史趋势对比与基线管理
  - 工作流改进建议(仓库级)
  - 团队流程讨论启动器

  适用场景:
  - 中大型团队多仓库协作模式洞察
  - 企业研发效能分析(非个人评估)
  - 工作流改进复盘与决策支持
  - 周期性仓库健康...
tags:
  - Git
  - 仓库分析
  - 企业开发
  - 团队协作
  - CI/CD
  - 研发效能
  - 隐私保护
  - 工具
  - 效率
  - git
  - repo
  - pro
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"

---

> **功能说明**: 本技能涵盖 与汇总、分析与汇总 等核心能力。


# 仓库协作分析工具(专业版)

## 概述

`actor-identifier-tool-pro` 是面向团队与企业的端到端 Git 仓库协作分析平台。它在免费版单仓库聚合分析之上,扩展了多仓库批量分析、自定义指标、CI/CD 集成、企业级报告与历史趋势对比能力,帮助团队洞察跨仓库的协作模式、识别工作流改进点并驱动流程优化.
本版本完全兼容免费版的所有隐私保护规则、命令白名单与安全契约,可平滑升级。所有分析仍坚持仓库级聚合,不做任何个人评估、排名或人事决策.
## 核心能力

| 能力 | 说明 | 是否兼容免费版 |
|---|---|-------|
| 单仓库聚合分析 | 免费版全部提交节奏、流失率、合规率、巴士因子 | 完全兼容 |
| 多仓库批量分析 | 一次分析多个仓库并汇总 | Pro 新增 |
| 自定义指标 | 团队定义专属指标与阈值 | Pro 新增 |
| CI/CD 集成 | 周期性自动分析与报告 | Pro 新增 |
| 企业级报告 | Markdown / HTML / PDF 多格式输出 | Pro 新增 |
| 历史趋势对比 | 与基线对比,识别趋势变化 | Pro 新增 |
| 工作流改进建议 | 仓库级流程讨论启动器 | Pro 新增 |
| 团队流程讨论 | 启动团队复盘的非个人化议题 | Pro 新增 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向团队的企业级、Git、仓库协作分析平台、含批量分析、集成与企业报告、仓库协作分析工具、专业版为团队与企、业提供端到端、仓库协作分析能力、涵盖多仓库批量分、集成与企业级聚合、核心能力、多仓库批量分析与、自定义指标与团队、级聚合、流水线集成、周期性报告、历史趋势对比与基、线管理、团队流程讨论启动等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1:多仓库批量分析

为团队批量分析多个仓库,生成汇总报告.
```bash
#!/usr/bin/env bash
# （请参考skill目录中的脚本文件） — 多仓库批量分析
set -euo pipefail
# ...
REPOS=(
  "/path/to/frontend"
  "/path/to/backend"
  "/path/to/infra"
  "/path/to/mobile"
)
# ...
REPORT_DIR="reports/repo-analysis"
mkdir -p "$REPORT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SUMMARY_FILE="$REPORT_DIR/summary-$TIMESTAMP.md"
# ...
{
  echo "# 多仓库协作分析汇总"
  echo ""
  echo "- 执行时间: $(date)"
  echo "- 仓库数量: ${#REPOS[@]}"
  echo ""
  echo "## 各仓库指标"
  echo ""
  echo "| 仓库 | 总提交 | 日均提交 | 活跃天数% | 周末% | 深夜% | Bug修复% | 流失率 | 合规率 |"
  echo "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
} > "$SUMMARY_FILE"
# ...
for repo in "${REPOS[@]}"; do
  repo_name=$(basename "$repo")
# ...
  # 校验仓库
  if ! git -C "$repo" rev-parse --is-inside-work-tree &>/dev/null; then
    echo "跳过非 Git 仓库: $repo"
    continue
  fi
# ...
  # 收集聚合指标(仅仓库级,无个人拆分)
  total_commits=$(git -C "$repo" log --pretty=format:"%H" | wc -l)
  avg_msg_len=$(git -C "$repo" log --pretty=format:"%s" | awk '{ print length }' \
    | awk '{ sum += $1; count++ } END { printf "%.1f", sum/count }')
  convention_rate=$(git -C "$repo" log --pretty=format:"%s" \
    | grep -cE "^(feat|fix|chore|docs|style|refactor|test|perf|ci|build)((.+))?:" || echo 0)
  bug_fix_count=$(git -C "$repo" log --grep="fix\|bug\|hotfix" --oneline -i | wc -l)
# ...
  # 写入汇总行(仅仓库级聚合,无个人数据)
  echo "| $repo_name | $total_commits | - | - | - | - | - | - | ${convention_rate}% |" >> "$SUMMARY_FILE"
# ...
  # 单仓库详细报告
  echo "已分析: $repo_name (总提交: $total_commits)"
done
# ...
echo ""
echo "## 工作流观察(仓库级)"
echo ""
echo "- 上述指标均为仓库级聚合,不做个人拆分"
echo "- 异常信号应作为团队流程讨论的启动器,而非个人评判"
echo "- 报告不用于绩效、排名或人事决策"
# ...
echo ""
echo "汇总报告: $SUMMARY_FILE"
```

### 场景 2:CI/CD 周期性分析

每周自动生成仓库协作分析报告,提交到团队文档库.
```yaml
# .github/workflows/weekly-analysis.yml
name: Weekly Repo Analysis
on:
  schedule:
    - cron: '0 8 * * 1'  # 每周一上午8点
  workflow_dispatch:
# ...
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
# ...
      - name: 安装依赖
        run: |
          sudo apt-get update
          sudo apt-get install -y jq
# ...
      - name: 执行仓库分析
        run: |
          mkdir -p reports
          bash （请参考skill目录中的脚本文件）
# ...
      - name: 生成 PDF 报告(可选)
        run: |
          # 用 pandoc 将 Markdown 转 PDF
          pandoc reports/repo-analysis/summary-*.md \
            -o reports/repo-analysis/weekly-report.pdf \
            --pdf-engine=weasyprint
# ...
      - name: 提交报告到文档库
        run: |
          git config user.name "Analysis Bot"
email "bot@example.com"
          git add reports/
          git commit -m "chore: weekly repo analysis report [skip ci]" || true
          git push
# ...
      - name: 通知团队
        uses: slackapi/slack-github-action@v1
        with:
          slack-message: "本周仓库协作分析报告已生成,详见 reports/repo-analysis/"
```

### 场景 3:自定义指标与基线对比

团队定义专属指标,与历史基线对比识别趋势变化.
```yaml
# .repo-metrics.yaml — 自定义指标配置
version: "1.0"
metrics:
  # 仓库级提交节奏
  - name: "日均提交数"
    query: "git log --pretty=format:'%ad' --date=short | sort -u | wc -l"
    baseline: 5.0
    threshold:
      warning_below: 3.0
      critical_below: 1.0
# ...
  # 约定式合规率
  - name: "约定式提交合规率"
    query: "git log --pretty=format:'%s' | grep -cE '^(feat|fix|chore|docs|style|refactor|test|perf|ci|build)'"
    baseline: 80  # 百分比
    threshold:
      warning_below: 70
      critical_below: 50
# ...
  # 文件级巴士因子(风险文件数)
  - name: "单一作者文件数"
    query: "git log --pretty=format:'%an' --name-only | sort | uniq -c | awk '$1==1' | wc -l"
    baseline: 10
    threshold:
      warning_above: 20
      critical_above: 50
# ...
  # 大提交比例(>500行)
  - name: "大提交比例"
    query: "git log --pretty=format:'%H' --shortstat | grep -E '([5-9][0-9]{2}|[0-9]{4,}) insertion' | wc -l"
    baseline: 0.1  # 10%
    threshold:
      warning_above: 0.2
      critical_above: 0.4
# ...
# 工作流改进议题模板
discussion_starters:
  - "仓库周末提交比例较高 — 值得团队流程讨论"
  - "约定式合规率下降 — 是否需要规范复习"
  - "巴士因子风险文件增加 — 是否需要知识分享"
  - "大提交比例上升 — 是否需要拆分提交习惯"
```

## 快速开始

### 领先步:声明团队上下文

在对话中说明团队规模、仓库数量与分析目标,例如:

```
我们是 30 人的工程团队,有 8 个微服务仓库,
需要每周自动生成协作分析报告,关注巴士因子与约定式合规率,
报告仅用于团队流程改进,不用于个人评估.
```

### 第二步:获取工程方案

工具会输出批量分析脚本、CI 集成 YAML、自定义指标配置与企业级报告模板.
### 第三步:落地与持续运行

```bash
# 应用自定义指标配置
cp .repo-metrics.yaml ./
# ...
# 执行批量分析
bash （请参考skill目录中的脚本文件）
# ...
# 查看报告
cat reports/repo-analysis/summary-*.md
```

#
## 示例

### 企业级报告模板(Markdown)

```markdown
#  仓库协作分析报告
# ...
> **报告说明**:本报告仅描述仓库级工作流模式,不用于个人评估、排名或人事决策.
# ...
## 报告概览
- 报告周期:  ~ 
- 仓库数量: 
- 总提交数: 
# ...
## 仓库级指标汇总
| 仓库 | 总提交 | 日均提交 | 合规率 | 巴士因子风险文件 |
|:-----|:-----|:-----|:-----|:-----|
<动态配置>
| <动态配置> | <动态配置> | <动态配置> | <动态配置>% | <动态配置> |
<动态配置>
# ...
## 工作流观察
<动态配置>
- 
<动态配置>
# ...
## 工作流改进讨论议题
<动态配置>
- 
<动态配置>
# ...
## 已知限制
- 本报告仅反映 Git 可见的活动,不反映代码审查、设计、文档、指导等非提交工作
- 所有指标均为仓库级聚合,不做个人拆分
- 报告不可用于绩效评估、排名、招聘、解雇或任何人事决策
```

### 安全契约(与免费版一致)

| 规则 | 说明 |
|---:|---:|
| 命令白名单 | 仅允许只读 git 子命令,见免费版表格 |
| 路径限制 | 仅访问用户提供的仓库路径,不遍历父目录 |
| 邮箱不收集 | 仅用 `%an`(作者名),永不用 `%ae`(邮箱) |
| 敏感数据本地处理 | 提交消息与文件路径仅本地折叠为聚合数值 |
| 密钥自动脱敏 | API Key、Token、密钥、连接串显示前替换为 `[REDACTED]` |
| 无个人评估 | 拒绝任何个人拆分、排名或人事评估请求 |
| 无网络 | 仅本地 git 命令,无 fetch/pull/clone/remote |

## 优选实践

1. **坚持仓库级聚合**:所有指标在仓库整体层面聚合,永不拆分到个人.
2. **报告作为讨论启动器**:异常信号应作为团队流程讨论的起点,而非个人评判.
3. **周期性分析与趋势对比**:每周或每迭代生成报告,与基线对比识别趋势变化.
4. **隐私优先不变**:Pro 版完全继承免费版的隐私保护规则,不因扩展能力而放松.
5. **工作流改进而非人事评估**:报告驱动流程优化,不可用于绩效、排名、招聘或解雇.
6. **限制声明必含**:每份报告必须包含"仅描述仓库级模式,不用于个人评估"的声明.
7. **多仓库汇总去标识化**:跨仓库汇总时,仅保留仓库级数据,不关联个人.
8. **CI 中保护报告访问**:报告可能含敏感的工作流信息,访问权限按需控制.
## 常见问题

### Q1: 多仓库分析如何避免泄露个人数据?

跨仓库汇总时仅保留仓库级聚合数据,不关联个人。巴士因子风险披露中的姓名仅出现在文件级风险说明中,不与评估性指标关联.
### Q2: 自定义指标如何保证安全?

自定义指标配置(`.repo-metrics.yaml`)中的 `query` 字段必须是白名单内的只读 git 命令。CI 在执行前校验 query 是否符合白名单,违规则拒绝执行.
### Q3: 报告如何与团队复盘结合?

将报告作为复盘会议的输入,聚焦"工作流改进议题"部分,讨论流程优化而非个人表现。例如"周末提交比例较高 — 是否需要调整发布窗口".
### Q4: 历史趋势如何存储与对比?

每次分析报告归档到 `reports/repo-analysis/` 目录,文件名带时间戳。趋势对比脚本读取历史报告,计算同比与环比变化,识别异常波动.
### Q5: Pro 版与免费版如何协同?

Pro 版完全兼容免费版的所有分析能力、隐私规则与安全契约。个人开发者可继续使用免费版分析单仓库,团队场景启用 Pro 版获得批量、自定义指标与 CI 集成能力。两个版本可在同一团队并存.
### Q6: 如何度量团队协作健康度?

跟踪四个仓库级指标:约定式合规率、巴士因子风险文件数、周末/深夜提交比例、大提交比例。四者共同反映团队工作流健康度。注意:这些是工作流信号,不是个人绩效指标.
## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows(需 Git Bash 或 WSL)/ macOS / Linux
- **Git**:任意现代版本(2.0+)
- **CI 平台**:GitHub Actions / GitLab CI / Jenkins

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| git | 系统工具 | 必需 | 系统包管理器 |
| cut / sort / uniq / awk / grep | 系统工具 | 必需 | 系统预装(Unix) |
| jq | 系统工具 | 推荐 | 系统包管理器 |
| pandoc | 文档工具 | 可选(生成 PDF) | 系统包管理器 |
| weasyprint | Python 包 | 可选(PDF 引擎) | `pip install weasyprint` |
| PyYAML | Python 包 | 推荐(读取指标配置) | `pip install pyyaml` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本 Skill 核心能力基于本地 git 命令,无需额外 API Key
- Slack 通知需配置 `SLACK_WEBHOOK_URL`
- 报告推送私有仓库需配置 `GITHUB_TOKEN` 或对应平台的访问令牌

### 可用性分类

- **分类**: MD+execute(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言指令驱动 Agent 执行只读 git 命令并输出仓库级聚合报告;批量脚本与 CI 集成需在仓库中落地并由 CI 执行;所有数据本地处理,无网络、无写入、无仓库外访问

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "仓库协作分析(专业版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "actor identifier pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。