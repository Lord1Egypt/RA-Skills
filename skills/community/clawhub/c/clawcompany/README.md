# ClawCompany Skill

> 🦞 AI 虚拟团队协作系统 - 一人企业家，无限可能

## 简介

ClawCompany 是一个 OpenClaw Skill，通过智能调度 PM/Dev/Review 三个 AI Agent，自动完成从需求分析到代码实现再到质量审查的完整开发流程。

**核心价值：** 一个人 = 一支团队

## 安装

```bash
# 从 ClawHub 安装
openclaw skill install clawcompany

# 或从源码安装
git clone https://github.com/felix-miao/ClawCompany.git
cd ClawCompany/skill
npm install
npm run build
npm link
```

## 快速开始

### 1. 配置 GLM API Key

```bash
export GLM_API_KEY=your-api-key-here
```

### 2. 使用

**在 OpenClaw 中：**

```
用户：帮我创建一个登录页面
OpenClaw：（自动调用 ClawCompany）
  📋 PM Agent 分析需求...
  💻 Dev Agent 生成代码...
  🔍 Review Agent 审查质量...
  ✅ 项目完成！
```

**通过 CLI：**

```bash
clawcompany "创建一个计算器应用"
```

## 使用示例

### 示例 1：创建 Web 组件

```bash
clawcompany "创建一个 Todo List 组件"
```

**输出：**
```
🦞 ClawCompany 开始工作...

[1/3] PM Agent 分析需求...
✅ PM Agent 拆分了 3 个任务

[2/3] Dev Agent 实现 "创建 TodoItem 组件"...
✅ 创建了 1 个文件

[3/3] Review Agent 审查...
✅ 审查通过

🎉 项目完成！完成 3 个任务，生成 3 个文件
```

### 示例 2：创建完整应用

```bash
clawcompany "创建一个用户认证系统，包含注册、登录、密码重置" --path ~/my-project
```

### 示例 3：模拟运行

```bash
clawcompany "创建登录页面" --dry-run --verbose
```

## CLI 选项

```
用法：
  clawcompany <需求描述> [选项]

选项：
  --path <目录>      项目路径（默认：当前目录）
  --verbose          详细日志
  --dry-run          模拟运行（不实际执行）
  --help             显示帮助信息

环境变量：
  GLM_API_KEY        GLM API Key（必需）
  PROJECT_ROOT       默认项目路径
  VERBOSE            详细模式
  DRY_RUN            模拟运行
```

## 工作原理

### Agent 协作流程

```
用户需求
    ↓
[1] PM Agent (subagent)
    - 分析需求
    - 拆分 2-4 个任务
    - 分配给 Dev Agent
    ↓
[2] Dev Agent (OpenCode)
    - 理解任务
    - 生成代码
    - 保存文件
    ↓
[3] Review Agent (subagent)
    - 检查代码质量
    - 安全审查
    - 批准/修改
    ↓
✅ 完成项目
```

### 技术架构

| Agent | Runtime | 实现 |
|-------|---------|------|
| PM Agent | subagent | GLM-5 (thinking: high) |
| Dev Agent | acp | OpenCode (真实编码) |
| Review Agent | subagent | GLM-5 (thinking: high) |

## 配置

### 必需配置

```bash
# GLM API Key（必需）
export GLM_API_KEY=your-key-here
```

获取 GLM API Key：https://open.bigmodel.cn/

### 可选配置

```bash
# GLM 模型（默认：glm-5）
export GLM_MODEL=glm-5

# 项目根目录
export PROJECT_ROOT=~/Projects

# 详细模式
export VERBOSE=true

# 模拟运行
export DRY_RUN=true
```

## API

### createProject()

```typescript
import { createProject } from 'clawcompany'

const result = await createProject(
  '创建一个登录页面',
  '/path/to/project',
  { verbose: true }
)

console.log(result.summary)
// 🎉 项目完成！完成 3 个任务，生成 3 个文件
```

### 返回值

```typescript
interface ProjectResult {
  success: boolean
  tasks: Task[]
  files: string[]
  summary: string
}
```

## 示例项目

查看 `examples/` 目录获取更多示例：

- `simple-component.md` - 创建简单组件
- `web-app.md` - 创建 Web 应用
- `api-endpoint.md` - 创建 API 端点

## 性能

| 指标 | 数值 |
|------|------|
| PM Agent 分析时间 | 5-10 秒 |
| Dev Agent 实现时间 | 30-60 秒/任务 |
| Review Agent 审查时间 | 5-10 秒 |
| 完整流程时间 | 1-2 分钟 |
| 成功率 | >95% |

## 故障排除

### GLM API 调用失败

```bash
# 检查 API Key
echo $GLM_API_KEY

# 测试 API
curl -X POST https://api.z.ai/api/coding/paas/v4/chat/completions \
  -H "Authorization: Bearer $GLM_API_KEY" \
  -d '{"model":"glm-5","messages":[{"role":"user","content":"test"}]}'
```

### Dev Agent 无法启动

```bash
# 检查 OpenCode
which opencode

# OpenClaw 会自动选择可用的编码代理
```

## 开发

### 构建

```bash
npm run build
```

### 测试

```bash
npm test
```

### 发布到 ClawHub

```bash
openclaw skill publish
```

## 相关链接

- **GitHub**: https://github.com/felix-miao/ClawCompany
- **ClawHub**: https://clawhub.com/skills/clawcompany
- **OpenClaw**: https://openclaw.ai

## License

MIT

## 作者

**Felix Miao**
- 比赛: OpenClaw 龙虾大赛 2026
- 赛道: 生产力龙虾

---

**ClawCompany - 一人企业家，无限可能！** 🦞
