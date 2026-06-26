# CodeBuddy Coding Skill

**通用 AI 编程能力扩展**

---

## 快速开始

### 1. 安装

确保已安装 CodeBuddy CLI v2.68.0+

```bash
# 检查版本
codebuddy --version
```

### 2. 基本用法

```javascript
const codebuddy = require('codebuddy-coding');

// 执行编程任务
const result = await codebuddy.execute({
  task: '创建一个用户登录页面',
  context: {
    projectPath: '/path/to/project'
  }
});

console.log('状态:', result.status);
console.log('修改文件:', result.filesModified);
```

### 3. 监听进度

```javascript
// 订阅进度事件
codebuddy.onProgress((progress) => {
  console.log(`进度: ${progress.percentage}%`);
  console.log(`当前任务: ${progress.currentTask}`);
});

// 执行任务
const result = await codebuddy.execute({
  task: '重构用户管理模块'
});
```

---

## API

### `execute(options)`

执行编程任务。

**参数:**
- `task` (string): 任务描述
- `context` (object): 任务上下文
  - `projectPath` (string): 项目路径
  - `techStack` (string): 技术栈
  - `files` (array): 相关文件
- `options` (object): 执行选项
  - `outputFormat` (string): 输出格式 ('json' | 'text')
  - `permissionMode` (string): 权限模式 ('default' | 'bypassPermissions')
  - `timeout` (number): 超时时间（秒）

**返回:**
```javascript
{
  status: 'success' | 'failed',
  filesModified: ['file1.js', 'file2.js'],
  toolCalls: [{ tool: 'write_to_file', ... }],
  reasoning: ['推理过程'],
  duration: 5.2,
  progress: { ... }
}
```

### `onProgress(callback)`

订阅进度更新事件。

### `onComplete(callback)`

订阅任务完成事件。

### `onFailed(callback)`

订阅任务失败事件。

### `getStatus()`

获取当前任务状态。

### `setDebugMode(enabled)`

启用/禁用调试模式。

---

## 示例

### 创建组件

```javascript
const codebuddy = require('codebuddy-coding');

const result = await codebuddy.execute({
  task: '创建一个用户登录组件，包含用户名、密码输入框和登录按钮',
  context: {
    projectPath: '/path/to/vue-project',
    techStack: 'Vue 3 + TypeScript'
  }
});

if (result.status === 'success') {
  console.log('组件创建成功！');
  console.log('创建的文件:', result.filesModified);
}
```

### 修复 Bug

```javascript
const result = await codebuddy.execute({
  task: '修复用户登录时的验证逻辑，密码应该至少8位且包含数字和字母',
  context: {
    projectPath: '/path/to/project',
    files: ['src/views/Login.vue']
  }
});

console.log('修复完成:', result.filesModified);
```

### 长时间任务

```javascript
codebuddy.onProgress((progress) => {
  console.log(`[${progress.percentage}%] ${progress.currentTask}`);
  console.log(`已用时: ${progress.elapsedTime}s`);
});

const result = await codebuddy.execute({
  task: '重构整个用户管理模块',
  options: {
    timeout: 600  // 10分钟
  }
});
```

---

## 集成到 Agent

### Developer Agent

```javascript
// developer/agent.js
const codebuddy = require('codebuddy-coding');

class DeveloperAgent {
  async implementFeature(task) {
    const result = await codebuddy.execute({
      task: task.description,
      context: {
        projectPath: this.projectPath
      }
    });
    return result;
  }
}
```

### Architect Agent

```javascript
// architect/agent.js
const codebuddy = require('codebuddy-coding');

class ArchitectAgent {
  async generateScaffold(requirements) {
    const result = await codebuddy.execute({
      task: `创建项目脚手架：${requirements}`,
      options: {
        permissionMode: 'bypassPermissions'
      }
    });
    return result;
  }
}
```

---

## 错误处理

```javascript
try {
  const result = await codebuddy.execute({
    task: '创建文件'
  });
} catch (error) {
  if (error.type === 'CLI_NOT_FOUND') {
    console.error('请先安装 CodeBuddy CLI');
  } else if (error.type === 'TIMEOUT') {
    console.error('任务超时');
  } else {
    console.error('执行失败:', error.message);
  }
}
```

---

## 许可证

MIT

---

**让每个 Agent 都拥有 AI 编程能力！** 🚀
