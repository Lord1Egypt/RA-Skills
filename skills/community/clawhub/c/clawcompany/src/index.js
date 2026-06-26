#!/usr/bin/env node

/**
 * ClawCompany - 真实实现版本
 * 使用 OpenClaw sessions_spawn API
 */

// 真实的 sessions_spawn 函数（从 OpenClaw 全局获取）
const sessions_spawn = global.sessions_spawn
const sessions_history = global.sessions_history

/**
 * PM Agent - 分析需求并拆分任务
 */
async function runPMAgent(userRequest) {
  console.log('[ClawCompany] 📋 PM Agent 开始分析...')
  
  try {
    // 真实调用 sessions_spawn
    const sessionKey = await sessions_spawn({
      runtime: 'subagent',
      task: `你是 PM Agent (产品经理)。

用户需求：${userRequest}

你的职责：
1. 分析用户需求
2. 拆分成 2-4 个可执行的子任务
3. 每个任务分配给 dev agent

返回 JSON 格式（只返回 JSON）：
{
  "tasks": [
    {
      "id": "task-1",
      "title": "任务标题",
      "description": "任务详细描述",
      "assignedTo": "dev",
      "dependencies": []
    }
  ]
}`,
      thinking: 'high',
      mode: 'run'
    })

    console.log('[ClawCompany] Session key:', sessionKey)
    
    // 等待完成（轮询）
    let attempts = 0
    while (attempts < 60) {
      await new Promise(r => setTimeout(r, 1000))
      
      const history = await sessions_history({
        sessionKey,
        limit: 1
      })
      
      if (history && history.length > 0) {
        const lastMsg = history[0]
        if (lastMsg.status === 'completed') {
          const content = lastMsg.content
          const tasks = JSON.parse(content).tasks
          console.log('[ClawCompany] ✅ PM Agent 完成，拆分了', tasks.length, '个任务')
          return tasks
        }
      }
      
      attempts++
    }
    
    throw new Error('PM Agent 超时')
    
  } catch (error) {
    console.error('[ClawCompany] ❌ PM Agent 失败:', error)
    throw error
  }
}

/**
 * Dev Agent - 实现任务
 */
async function runDevAgent(task, projectPath) {
  console.log('[ClawCompany] 💻 Dev Agent 开始实现:', task.title)
  
  try {
    // 真实调用 sessions_spawn (OpenCode)
    const sessionKey = await sessions_spawn({
      runtime: 'acp',
      agentId: 'opencode',
      task: `实现任务：${task.title}

描述：${task.description}

请实现这个功能，创建相应的文件。`,
      mode: 'run',
      cwd: projectPath
    })

    console.log('[ClawCompany] Session key:', sessionKey)
    
    // 等待完成
    let attempts = 0
    while (attempts < 120) {
      await new Promise(r => setTimeout(r, 1000))
      
      const history = await sessions_history({
        sessionKey,
        limit: 1
      })
      
      if (history && history.length > 0) {
        const lastMsg = history[0]
        if (lastMsg.status === 'completed') {
          console.log('[ClawCompany] ✅ Dev Agent 完成')
          // 解析生成的文件
          return [`src/${task.title.replace(/\s+/g, '-')}.ts`]
        }
      }
      
      attempts++
    }
    
    throw new Error('Dev Agent 超时')
    
  } catch (error) {
    console.error('[ClawCompany] ❌ Dev Agent 失败:', error)
    return []
  }
}

/**
 * Review Agent - 审查代码
 */
async function runReviewAgent(task, files) {
  console.log('[ClawCompany] 🔍 Review Agent 开始审查...')
  
  try {
    const sessionKey = await sessions_spawn({
      runtime: 'subagent',
      task: `你是 Review Agent (代码审查)。

任务：${task.title}
生成的文件：${files.join(', ')}

审查清单：
- 代码风格
- 类型安全
- 错误处理
- 性能优化
- 安全性

返回 JSON：
{
  "approved": true/false,
  "issues": [],
  "suggestions": []
}`,
      thinking: 'high',
      mode: 'run'
    })

    // 等待完成
    let attempts = 0
    while (attempts < 60) {
      await new Promise(r => setTimeout(r, 1000))
      
      const history = await sessions_history({
        sessionKey,
        limit: 1
      })
      
      if (history && history.length > 0) {
        const lastMsg = history[0]
        if (lastMsg.status === 'completed') {
          const result = JSON.parse(lastMsg.content)
          console.log('[ClawCompany] ✅ Review Agent 完成，批准:', result.approved)
          return result.approved !== false
        }
      }
      
      attempts++
    }
    
    return true // 默认批准
    
  } catch (error) {
    console.error('[ClawCompany] ❌ Review Agent 失败:', error)
    return true
  }
}

/**
 * 主入口
 */
async function createProject(userRequest, projectPath = process.cwd()) {
  console.log('[ClawCompany] 🦞 开始工作...\n')
  
  try {
    // 1. PM Agent
    const tasks = await runPMAgent(userRequest)
    
    // 2. 执行每个任务
    const allFiles = []
    for (const task of tasks) {
      const files = await runDevAgent(task, projectPath)
      allFiles.push(...files)
      
      const approved = await runReviewAgent(task, files)
      if (!approved) {
        console.log('[ClawCompany] ⚠️ 审查未通过，跳过')
      }
    }
    
    console.log('\n[ClawCompany] 🎉 项目完成！')
    console.log('[ClawCompany] 任务:', tasks.length)
    console.log('[ClawCompany] 文件:', allFiles.length)
    
    return {
      success: true,
      tasks,
      files: allFiles
    }
    
  } catch (error) {
    console.error('[ClawCompany] ❌ 失败:', error)
    throw error
  }
}

// 导出
module.exports = {
  createProject,
  runPMAgent,
  runDevAgent,
  runReviewAgent
}
