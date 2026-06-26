---
name: clawcompany
description: AI virtual team collaboration system with PM/Dev/Review agents for automated software development. Use when users request creating, building, or implementing features, apps, or components. Triggers on phrases like "create a...", "build a...", "implement a...", "develop a...", or when rapid prototyping and automated development workflow is needed.
---

# ClawCompany Skill

AI 虚拟团队协作系统 - 让一个人也能像拥有一支完整团队一样工作

## 描述

当用户提出开发需求时，ClawCompany 会自动组建一个 AI 虚拟团队：
- 📋 **PM Agent** - 分析需求、拆分任务、协调团队
- 💻 **Dev Agent** - 编写代码、实现功能
- 🔍 **Review Agent** - 审查代码、保证质量

## 使用场景

**何时使用：**
- 用户说："帮我创建一个..." / "实现一个..." / "开发一个..."
- 用户需要快速原型开发
- 用户想要自动化开发流程

## Agent 定义

### PM Agent

**触发：** 用户提出需求后首先调用

**System Prompt:**
```
你是 PM Agent (产品经理)。

你的职责：
1. 分析用户需求
2. 拆分成 2-4 个可执行的子任务
3. 每个任务包含：标题、描述、负责人
4. 协调团队进度

回复格式：
{
  "analysis": "需求分析...",
  "tasks": [
    {
      "id": "task-1",
      "title": "任务标题",
      "description": "任务描述",
      "assignedTo": "dev"
    }
  ],
  "message": "给团队的指示..."
}
```

**调用方式：**
```javascript
await sessions_spawn({
  runtime: 'subagent',
  task: `${systemPrompt}\n\n用户需求：${userRequest}`,
  thinking: 'high',
  mode: 'run'
})
```

---

### Dev Agent

**触发：** PM Agent 分配任务后调用

**System Prompt:**
```
你是 Dev Agent (开发者)。

你的职责：
1. 理解任务需求
2. 生成/修改代码
3. 确保代码可运行

回复格式：
{
  "files": [
    {
      "path": "src/component.tsx",
      "content": "代码内容..."
    }
  ],
  "message": "实现说明..."
}
```

**调用方式：**
```javascript
await sessions_spawn({
  runtime: 'acp',
  agentId: 'opencode',
  task: `${systemPrompt}\n\n任务：${task.description}`,
  mode: 'run'
})
```

---

### Review Agent

**触发：** Dev Agent 完成后调用

**System Prompt:**
```
你是 Review Agent (代码审查)。

审查清单：
- 代码风格
- 类型安全
- 错误处理
- 可访问性
- 性能优化
- 安全性
- 测试覆盖

回复格式：
{
  "approved": true/false,
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"],
  "message": "审查总结..."
}
```

**调用方式：**
```javascript
await sessions_spawn({
  runtime: 'subagent',
  task: `${systemPrompt}\n\n代码：${code}`,
  thinking: 'high',
  mode: 'run'
})
```

---

## 工作流程

**用户输入需求后：**

1. **启动 PM Agent**
   ```
   PM Agent 分析需求...
   ✅ 拆分为 3 个任务
   ```

2. **为每个任务启动 Dev Agent**
   ```
   Dev Agent 实现任务 1...
   ✅ 创建了 2 个文件
   
   Dev Agent 实现任务 2...
   ✅ 创建了 1 个文件
   ```

3. **启动 Review Agent**
   ```
   Review Agent 审查代码...
   ✅ 批准 / ⚠️ 需要修改
   ```

4. **返回完整结果**
   ```
   🎉 项目完成！
   - 任务：3 个
   - 文件：5 个
   - 审查：通过
   ```

---

## 实现示例

**完整流程代码：**

```javascript
// 1. PM Agent 分析需求
const pmSession = await sessions_spawn({
  runtime: 'subagent',
  task: `你是 PM Agent。

用户需求：${userRequest}

分析需求并拆分任务。返回 JSON 格式。`,
  thinking: 'high',
  mode: 'run'
})

const pmHistory = await sessions_history({ sessionKey: pmSession, limit: 1 })
const pmResult = JSON.parse(pmHistory[0].content)
const tasks = pmResult.tasks

// 2. 为每个任务启动 Dev Agent
const allFiles = []
for (const task of tasks) {
  const devSession = await sessions_spawn({
    runtime: 'acp',
    agentId: 'opencode',
    task: `实现任务：${task.title}\n描述：${task.description}`,
    mode: 'run'
  })
  
  const devHistory = await sessions_history({ sessionKey: devSession, limit: 1 })
  const devResult = JSON.parse(devHistory[0].content)
  allFiles.push(...devResult.files)
  
  // 3. Review Agent 审查
  const reviewSession = await sessions_spawn({
    runtime: 'subagent',
    task: `审查代码：\n${JSON.stringify(devResult.files)}`,
    thinking: 'high',
    mode: 'run'
  })
  
  const reviewHistory = await sessions_history({ sessionKey: reviewSession, limit: 1 })
  const reviewResult = JSON.parse(reviewHistory[0].content)
  
  if (!reviewResult.approved) {
    // 重新实现...
  }
}

// 4. 返回结果
return {
  tasks,
  files: allFiles,
  summary: `完成 ${tasks.length} 个任务，生成 ${allFiles.length} 个文件`
}
```

---

## 配置

**环境变量：**
```bash
GLM_API_KEY=your-key-here  # GLM-5 API Key
```

**Agent 配置：**
- PM Agent: thinking=high, runtime=subagent
- Dev Agent: runtime=acp, agentId=opencode
- Review Agent: thinking=high, runtime=subagent

---

## 示例对话

**用户：** "帮我创建一个登录页面"

**ClawCompany：**
```
📋 PM Agent:
我已分析需求，拆分为 3 个任务：
1. 创建登录表单组件
2. 添加表单验证
3. 实现登录 API

💻 Dev Agent:
[创建 src/components/LoginForm.tsx]
✅ 完成

💻 Dev Agent:
[创建 src/lib/validation.ts]
✅ 完成

💻 Dev Agent:
[创建 src/app/api/login/route.ts]
✅ 完成

🔍 Review Agent:
审查通过 ✅
- 代码风格：良好
- 类型安全：完整
- 安全性：通过

🎉 项目完成！
文件：3 个
任务：3 个
```

---

## 注意事项

1. **所有 Agent 使用 GLM-5**
2. **Dev Agent 使用 OpenCode**
3. **通过 sessions_spawn 调用**
4. **实时获取 sessions_history**

---

**ClawCompany - 一人企业家，无限可能！** 🦞
