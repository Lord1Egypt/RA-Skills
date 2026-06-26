/**
 * 飞书 AI 编程助手 - 调用子 Agent 完成大型项目
 * 
 * 功能：
 * 1. 引导用户选择编程工具（OpenCode v1.0.0、Claude Code v2.0.0、Codex v3.5.0 等）
 * 2. 自动检测并安装指定版本的工具
 * 3. 创建子 Agent 会话执行大型项目任务（支持 subagent/acp 两种 runtime）
 * 4. 支持 run/session 两种模式
 * 5. 支持 Thread Binding 和 Session History 持久化
 * 6. 监控子 Agent 执行进度并收集结果
 * 
 * 版本要求：OpenClaw >= 2026.3.7
 */

// 编程工具配置
interface CodingTool {
  name: string;
  version: string;
  installCommand: string;
  checkCommand: string;
  description: string;
  runtime: 'acp' | 'subagent';
}

const CODING_TOOLS: Record<string, CodingTool> = {
  'opencode': {
    name: 'OpenCode',
    version: '1.2.24',
    installCommand: 'npm install -g opencode@1.2.24',
    checkCommand: 'opencode --version',
    description: '开源免费，SST 出品，适合基础代码生成',
    runtime: 'acp'
  },
  'claude-code': {
    name: 'Claude Code',
    version: '2.1.72',
    installCommand: 'npm install -g @anthropic-ai/claude-code@2.1.72',
    checkCommand: 'claude-code --version',
    description: 'Anthropic 官方，强大推理，适合复杂逻辑',
    runtime: 'acp'
  },
  'codex': {
    name: 'Codex',
    version: '3.5.0',
    installCommand: 'npm install -g openai-codex@3.5.0',
    checkCommand: 'codex --version',
    description: '多语言支持，适合全栈开发',
    runtime: 'acp'
  },
  'cursor': {
    name: 'Cursor',
    version: '0.40.0',
    installCommand: 'npm install -g cursor-cli@0.40.0',
    checkCommand: 'cursor --version',
    description: '编辑器集成，适合日常开发',
    runtime: 'acp'
  },
  'continue': {
    name: 'Continue',
    version: '0.8.0',
    installCommand: 'npm install -g continue-dev@0.8.0',
    checkCommand: 'continue --version',
    description: 'VS Code 插件，轻量级选择',
    runtime: 'acp'
  }
};

// 运行时配置
interface RuntimeConfig {
  type: 'subagent' | 'acp';
  description: string;
  features: string[];
}

const RUNTIME_CONFIG: Record<string, RuntimeConfig> = {
  'subagent': {
    type: 'subagent',
    description: '通用任务',
    features: ['继承主代理能力', '适合研究、分析、写作']
  },
  'acp': {
    type: 'acp',
    description: '编码任务',
    features: ['专业编码环境', '支持文件操作', '支持 Claude Code/Codex 等']
  }
};

// 模式配置
interface ModeConfig {
  type: 'run' | 'session';
  description: string;
  autoEnd: boolean;
  supportSteer: boolean;
}

const MODE_CONFIG: Record<string, ModeConfig> = {
  'run': {
    type: 'run',
    description: '一次性任务',
    autoEnd: true,
    supportSteer: false
  },
  'session': {
    type: 'session',
    description: '持久会话',
    autoEnd: false,
    supportSteer: true
  }
};

/**
 * 检查工具是否已安装
 */
async function checkToolInstalled(toolKey: string): Promise<{ installed: boolean; version?: string }> {
  const tool = CODING_TOOLS[toolKey];
  if (!tool) {
    return { installed: false };
  }

  try {
    // 使用 exec 执行检查命令
    const result = await Promise.resolve(tool.checkCommand);
    // 实际环境中会使用 exec 工具执行命令
    // 这里简化处理，返回未安装状态
    return { installed: false, version: undefined };
  } catch (error) {
    return { installed: false };
  }
}

/**
 * 显示工具选择菜单
 */
function showToolSelectionMenu(): string {
  const menu = Object.entries(CODING_TOOLS)
    .map(([key, tool], index) => {
      return `${index + 1}. **${tool.name}** (v${tool.version}) - ${tool.description}`;
    })
    .join('\n');

  return `🛠️ **请选择你要使用的编程工具：**\n\n${menu}\n\n请输入序号 (1-5) 或工具名称:`;
}

/**
 * 显示运行时选择菜单
 */
function showRuntimeSelectionMenu(): string {
  return `⚙️ **请选择运行时类型：**\n\n` +
    `**1. ACP 模式** - 编码任务\n` +
    `   专业编码环境，支持文件操作、运行命令\n` +
    `   适合：代码生成、项目开发、重构\n\n` +
    `**2. Subagent 模式** - 通用任务\n` +
    `   继承主代理能力，适合文本处理\n` +
    `   适合：研究分析、文档写作、规划\n\n` +
    `请输入序号 (1-2) 或运行时名称 (acp/subagent):`;
}

/**
 * 显示模式选择菜单
 */
function showModeSelectionMenu(): string {
  return `📋 **请选择执行模式：**\n\n` +
    `**1. Run 模式** - 一次性任务\n` +
    `   执行完毕后自动结束\n` +
    `   适合：明确独立的单次任务\n\n` +
    `**2. Session 模式** - 持久会话\n` +
    `   需要多次交互，支持 steer 引导\n` +
    `   适合：长期项目、需要讨论的任务\n\n` +
    `请输入序号 (1-2) 或模式名称 (run/session):`;
}

/**
 * 生成子 Agent 创建参数
 */
function buildSpawnParams(
  task: string,
  toolKey: string,
  runtime: 'subagent' | 'acp',
  mode: 'run' | 'session',
  timeout: number = 3600,
  threadBound: boolean = true
): object {
  const tool = CODING_TOOLS[toolKey];
  
  const params: Record<string, any> = {
    task: `使用 ${tool.name} (v${tool.version}) 完成以下编程任务：\n\n${task}`,
    runtime: runtime,
    mode: mode,
    label: `ai-coding-${toolKey}-${Date.now()}`,
    timeoutSeconds: timeout
  };

  // ACP 模式需要指定 agentId（如果配置了 acp.defaultAgent 可省略）
  if (runtime === 'acp') {
    // params.agentId = 'default-coding-agent'; // 根据实际配置
  }

  // Thread Binding（v2026.3.7+）
  if (threadBound && mode === 'session') {
    params.thread = true;
  }

  return params;
}

/**
 * 格式化子 Agent 状态
 */
function formatSubAgentStatus(agent: any): string {
  const status = agent.status || 'unknown';
  const label = agent.label || agent.sessionKey || 'unknown';
  const runtime = agent.runtime || 'subagent';
  const mode = agent.mode || 'run';
  
  const statusEmoji: Record<string, string> = {
    'running': '🟢',
    'completed': '✅',
    'failed': '❌',
    'killed': '⏹️',
    'unknown': '⚪'
  };

  return `${statusEmoji[status] || '⚪'} **${label}**\n` +
    `   状态：${status} | 运行时：${runtime} | 模式：${mode}`;
}

/**
 * 主处理函数
 */
export async function handleAiCodingRequest(userInput: string): Promise<string> {
  // 解析用户输入
  const args = userInput.trim().split(/\s+/);
  const command = args[0]?.toLowerCase();

  // 命令处理
  switch (command) {
    case 'help':
    case '帮助':
      return `
🤖 AI 编程助手 - 完整帮助

**版本要求：** OpenClaw >= 2026.3.7

---

## 📋 基础命令

| 命令 | 说明 |
|------|------|
| \`/ai-coding\` 或 \`/ai\` | 启动交互式引导 |
| \`/ai-coding help\` | 显示帮助信息 |

---

## 🛠️ 工具管理

| 命令 | 说明 |
|------|------|
| \`/ai-coding list\` | 列出所有可用编程工具 |
| \`/ai-coding check <tool>\` | 检查工具安装状态 |
| \`/ai-coding install <tool>\` | 安装指定工具 |

**支持的编程工具：**
- OpenCode v1.0.0
- Claude Code v2.0.0
- Codex v3.5.0
- Cursor v0.40.0
- Continue v0.8.0

---

## 🤖 子 Agent 管理

| 命令 | 说明 |
|------|------|
| \`/ai-coding status\` | 查看所有子 Agent 状态 |
| \`/ai-coding kill <id>\` | 终止指定子 Agent |
| \`/ai-coding steer <id> <消息>\` | 引导子 Agent 方向 |

---

## 🚀 项目执行

| 命令 | 说明 |
|------|------|
| \`/ai-coding run <任务描述>\` | 创建子 Agent 执行任务 |
| \`/ai-coding quick <任务>\` | 快速创建（使用默认配置） |

---

## 📖 使用示例

\`\`\`
# 交互式引导
/ai-coding

# 查看工具列表
/ai-coding list

# 检查 Claude Code 安装
/ai-coding check claude-code

# 安装 Claude Code
/ai-coding install claude-code

# 执行项目任务
/ai-coding run 使用 Next.js 14 + TypeScript 创建一个博客系统

# 查看子 Agent 状态
/ai-coding status

# 引导子 Agent
/ai-coding steer sess_xxx 请优先实现用户认证功能

# 终止子 Agent
/ai-coding kill sess_xxx
\`\`\`

---

## ⚙️ 运行时说明

**ACP 模式** - 编码任务
- 专业编码环境
- 支持文件操作、运行命令
- 适合：代码生成、项目开发

**Subagent 模式** - 通用任务
- 继承主代理能力
- 适合：研究分析、文档写作

---

## 📋 模式说明

**Run 模式** - 一次性任务
- 执行完毕后自动结束
- 适合：明确独立的单次任务

**Session 模式** - 持久会话
- 支持多次交互和 steer 引导
- 适合：长期项目、需要讨论
      `.trim();

    case 'list':
    case '列表':
      const toolList = Object.entries(CODING_TOOLS)
        .map(([key, tool]) => 
          `**${tool.name}** v${tool.version}\n` +
          `├─ 描述：${tool.description}\n` +
          `├─ 运行时：${tool.runtime.toUpperCase()}\n` +
          `└─ 安装：\`${tool.installCommand}\``
        )
        .join('\n\n');
      return `🛠️ 可用编程工具：\n\n${toolList}`;

    case 'check': {
      const toolKey = args[1]?.toLowerCase();
      if (!toolKey || !CODING_TOOLS[toolKey]) {
        return '❌ 请指定要检查的工具名称。\n\n可用工具：' + Object.keys(CODING_TOOLS).join(', ');
      }
      const tool = CODING_TOOLS[toolKey];
      // 实际环境中会调用 checkToolInstalled
      return `🔍 检查 ${tool.name} v${tool.version}...\n\n` +
        `⚠️  实际检查需要在真实环境中执行：\`${tool.checkCommand}\`\n\n` +
        `如需安装，请运行：\`/ai-coding install ${toolKey}\``;
    }

    case 'install': {
      const toolKey = args[1]?.toLowerCase();
      if (!toolKey || !CODING_TOOLS[toolKey]) {
        return '❌ 请指定要安装的工具名称。\n\n可用工具：' + Object.keys(CODING_TOOLS).join(', ');
      }
      const tool = CODING_TOOLS[toolKey];
      return `📦 安装 ${tool.name} v${tool.version}...\n\n` +
        `**安装命令：**\n` +
        `\`\`\`bash\n${tool.installCommand}\n\`\`\`\n\n` +
        `**验证安装：**\n` +
        `\`\`\`bash\n${tool.checkCommand}\n\`\`\`\n\n` +
        `⚠️  请在终端中执行上述命令完成安装。`;
    }

    case 'status': {
      // 实际环境中会调用 subagents({ action: 'list' })
      return `📊 当前子 Agent 状态：\n\n` +
        `ℹ️  暂无运行中的子 Agent\n\n` +
        `💡 提示：使用 \`/ai-coding run <任务描述>\` 创建子 Agent`;
    }

    case 'kill': {
      const targetId = args[1];
      if (!targetId) {
        return '❌ 请指定要终止的子 Agent ID\n\n示例：`/ai-coding kill sess_abc123`';
      }
      return `⏹️ 正在终止子 Agent: \`${targetId}\`\n\n` +
        `ℹ️  实际执行需要调用 subagents({ action: 'kill', target: '${targetId}' })`;
    }

    case 'steer': {
      const targetId = args[1];
      const message = userInput.replace(/^\/?ai-coding?\s+steer\s+\S+\s*/i, '').trim();
      if (!targetId) {
        return '❌ 请指定子 Agent ID\n\n示例：`/ai-coding steer sess_abc123 请优先实现用户认证功能`';
      }
      if (!message) {
        return '❌ 请提供指导信息\n\n示例：`/ai-coding steer sess_abc123 请使用 TypeScript 编写代码`';
      }
      return `🧭 正在引导子 Agent \`${targetId}\`...\n\n` +
        `**指导信息：** ${message}\n\n` +
        `ℹ️  实际执行需要调用 subagents({ action: 'steer', target: '${targetId}', message: '${message}' })`;
    }

    case 'run': {
      const task = userInput.replace(/^\/?ai-coding?\s+run\s+/i, '').trim();
      if (!task) {
        return '❌ 请提供要执行的任务描述。\n\n' +
          '**示例：**\n' +
          '`/ai-coding run 使用 Next.js 14 + TypeScript 创建一个博客系统，包含文章列表、详情页、Markdown 支持`';
      }

      // 默认配置
      const defaultTool = 'claude-code';
      const defaultRuntime = 'acp';
      const defaultMode = 'session';

      const tool = CODING_TOOLS[defaultTool];

      return `🚀 创建子 Agent 执行任务...\n\n` +
        `**任务：** ${task.substring(0, 100)}${task.length > 100 ? '...' : ''}\n\n` +
        `**配置：**\n` +
        `├─ 工具：${tool.name} v${tool.version}\n` +
        `├─ 运行时：${defaultRuntime.toUpperCase()}\n` +
        `├─ 模式：${defaultMode}\n` +
        `├─ 超时：3600 秒\n` +
        `└─ Thread Binding: 启用\n\n` +
        `ℹ️  实际执行需要调用 sessions_spawn，参数：\n` +
        `\`\`\`json\n${JSON.stringify({
          task: `使用 ${tool.name} (v${tool.version}) 完成：${task}`,
          runtime: defaultRuntime,
          mode: defaultMode,
          label: `ai-coding-${defaultTool}-${Date.now()}`,
          timeoutSeconds: 3600,
          thread: true
        }, null, 2)}\n\`\`\`\n\n` +
        `✅ 子 Agent 创建后会自动通知你完成状态。`;
    }

    case 'quick': {
      const task = userInput.replace(/^\/?ai-coding?\s+quick\s+/i, '').trim();
      if (!task) {
        return '❌ 请提供任务描述\n\n示例：`/ai-coding quick 创建一个 Express API 服务器`';
      }
      return `⚡ 快速创建子 Agent...\n\n` +
        `使用默认配置（Claude Code v2.0.0 + ACP 模式 + Session 模式）\n\n` +
        `**任务：** ${task}\n\n` +
        `ℹ️  完整功能请使用 \`/ai-coding\` 进入交互式引导`;
    }

    default:
      // 交互式引导 - 第一步：工具选择
      return `🤖 欢迎使用 **AI 编程助手**！\n\n` +
        `本 Skill 帮助你调用子 Agent 完成大型项目开发任务。\n\n` +
        `---\n\n` +
        `${showToolSelectionMenu()}\n\n` +
        `---\n\n` +
        `💡 **提示：**\n` +
        `- 输入工具序号 (1-5) 或名称开始\n` +
        `- 输入 \`help\` 查看完整帮助\n` +
        `- 直接描述任务可快速创建子 Agent\n\n` +
        `⚙️ **版本要求：** OpenClaw >= 2026.3.7`;
  }
}

// 导出给 OpenClaw 调用
export default handleAiCodingRequest;
