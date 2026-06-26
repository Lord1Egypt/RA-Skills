# Clawjob — UP 简历 AI Skills for Agent

> 在 AI 助手中管理简历、搜索职位、智能投递，一切尽在对话中完成。

Clawjob 是 [UP 简历](https://upcv.tech) 的 AI Skills 集合，帮助应届生和求职者更高效地找校招、找实习、找工作。在 Claude Code 中直接创建专业简历、搜索校招和社招职位、设置求职监控、辅助智能投递。通过 MCP 协议与 UP 简历无缝连接，AI 助手中的操作与网页端数据实时互通。

- **UP 简历官网**：[upcv.tech](https://upcv.tech) — 简历创建和求职搜索平台
- **Clawjob OpenClaw 版**：[clawjob.upcv.tech](https://clawjob.upcv.tech) — Skills 开放版，免费使用

## Skills 一览

| Skill | 说明 | 触发词 |
|-------|------|--------|
| [resume-create](./resume-create/) | 从零创建专业简历，身份识别→模块规划→STAR 法则 | "创建简历"、"新建简历" |
| [resume-edit](./resume-edit/) | 编辑/改写/诊断简历，JD 对照优化，导出 PDF | "编辑简历"、"优化简历"、"诊断简历" |
| [campus-search](./campus-search/) | 搜索校招项目和实习项目 | "搜索校招"、"找校招"、"实习项目" |
| [job-search](./job-search/) | 搜索岗位 JD（社招/校招/实习） | "搜索岗位"、"找工作"、"社招" |
| [job-monitor](./job-monitor/) | 每日定时监控，获取最新职位简报 | "监控校招"、"每日推荐"、"最新校招" |
| [auto-apply](./auto-apply/) | 智能投递助手，ATS 识别，表单填写指导 | "投递"、"申请岗位"、"准备投递" |

## 快速开始

### 1. 获取 API Key

前往 [clawjob.upcv.tech](https://clawjob.upcv.tech) 生成你的 API Key。

### 2. 安装 MCP Server

```bash
claude mcp add upcv -- npx @upcv/mcp-server --api-key YOUR_API_KEY
```

### 3. 开始使用

在 Claude Code 中直接说：

```
帮我创建一份简历
搜索字节跳动的校招
找上海的前端工程师岗位
帮我设置每日校招监控
根据这个 JD 优化我的简历
帮我准备投递字节跳动
```

## 典型工作流

### 从零开始求职

```
1. /resume-create  → 身份识别，模块规划，逐步创建专业简历
2. /job-search     → 搜索目标岗位，查看 JD
3. /resume-edit    → 根据岗位 JD 改写优化简历
4. /auto-apply     → 准备投递数据，辅助填写 ATS 表单
```

### 校招求职

```
1. /campus-search  → 搜索校招/实习项目
2. /job-search     → 查看具体岗位 JD
3. /resume-edit    → 针对性优化简历
4. /auto-apply     → 准备投递，导出 PDF
```

### 每日求职速览

```
1. /job-monitor    → 设置每日监控，获取最新简报
2. /job-search     → 深入了解感兴趣的岗位
3. /resume-edit    → 根据目标岗位优化简历
4. /auto-apply     → 选择目标，准备投递
```

### 简历优化

```
1. /resume-edit    → 诊断简历质量，获取改进建议
2. /job-search     → 搜索目标岗位 JD
3. /resume-edit    → JD 对照改写，STAR 法则优化经历
4. /resume-edit    → 导出 PDF
```

## 数据互通

通过 Clawjob 创建或修改的简历，会实时同步到 [UP 简历](https://upcv.tech) 网页端。你可以：

- 在 AI 助手中快速创建和编辑
- 在网页端精细调整排版和样式
- 随时在两个端之间切换，数据完全一致

## 相关链接

- [UP 简历官网](https://upcv.tech) — 简历创建和求职搜索平台
- [Clawjob OpenClaw 版](https://clawjob.upcv.tech) — Skills 开放版，免费使用
- [UPCV MCP Server](https://github.com/HireTechUpUp/upcv-mcp-server) — MCP Server npm 包（开发者）

## 支持我们

Clawjob 致力于帮助每一位应届生和求职者更高效地找到理想的校招、实习和工作机会。如果这些 Skills 对你有帮助：

1. 在 Skills Marketplace 为项目点个赞
2. 把 Clawjob 分享给正在求职的同学和朋友
3. 在 GitHub 上给我们一个 Star

你的支持能帮助更多人用上 AI 求职工具，感谢！

## License

MIT
