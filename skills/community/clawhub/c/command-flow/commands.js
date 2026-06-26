#!/usr/bin/env node

/**
 * Commands Data - 命令数据结构
 * 
 * 定义所有斜杠命令的元数据（来源、安全级别、执行函数）
 * 
 * @version 1.0.0
 * @author Neo（宇宙神经系统）
 */

// 命令数据来源分类
const SOURCE = {
  NATIVE: 'native',        // OpenClaw 原生
  OURS: 'ours',            // 我们开发的
  THIRD_PARTY: 'third-party' // 第三方
};

// 安全级别
const SAFETY = {
  SAFE: 'safe',      // 🟢 安全
  WARNING: 'warning', // 🟡 危险（需确认）
  HIDDEN: 'hidden'    // 🔴 隐藏（默认不显示）
};

/**
 * 命令数据结构
 */
const COMMANDS = {
  // OpenClaw 原生技能
  native: [
    {
      slug: 'skills',
      command: '/skills',
      description: '查看已安装的技能列表',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: '管理',
      executeHint: '显示技能控制台',
      execute: async () => {
        const { showDashboard } = require('../skill-dashboard/dashboard.js');
        return await showDashboard(1);
      }
    },
    {
      slug: 'search',
      command: '/search <关键词>',
      description: '搜索 ClawHub 上的技能',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: '管理',
      executeHint: '弹出搜索框',
      execute: async (query) => {
        return `正在搜索 ClawHub：${query || '请输入关键词'}\n\n（搜索功能待实现）`;
      }
    },
    {
      slug: 'install',
      command: '/install <技能名>',
      description: '安装技能',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: '管理',
      executeHint: '安装指定技能',
      execute: async (skillName) => {
        if (!skillName) {
          return '请提供技能名，例如：/install smart-router';
        }
        return `正在安装 ${skillName}...\n\n（安装功能待实现）`;
      }
    },
    {
      slug: 'update',
      command: '/update <技能名>',
      description: '更新技能（需要确认）',
      safety: SAFETY.WARNING,
      source: SOURCE.NATIVE,
      category: '管理',
      executeHint: '二次确认 → 更新',
      confirm: true,
      confirmMessage: (skillName) => `确定要更新 ${skillName || '技能'} 吗？`,
      execute: async (skillName) => {
        return `正在更新 ${skillName}...\n\n（更新功能待实现）`;
      }
    },
    {
      slug: 'uninstall',
      command: '/uninstall <技能名>',
      description: '卸载技能（不可逆，需要确认）',
      safety: SAFETY.WARNING,
      source: SOURCE.NATIVE,
      category: '管理',
      executeHint: '二次确认 → 卸载',
      confirm: true,
      confirmMessage: (skillName) => `⚠️ 卸载 ${skillName || '技能'} 不可逆，确定要继续吗？`,
      execute: async (skillName) => {
        return `正在卸载 ${skillName}...\n\n（卸载功能待实现）`;
      }
    },
    // 以下为 OpenClaw 系统命令（44 个）
    {
      slug: 'acp',
      command: '/acp',
      description: 'Agent Control Protocol 工具',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/acp\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'agent',
      command: '/agent',
      description: '运行一次 Agent 轮询',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/agent\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'agents',
      command: '/agents',
      description: '管理隔离的 Agent',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/agents\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'approvals',
      command: '/approvals',
      description: '管理执行审批',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/approvals\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'browser',
      command: '/browser',
      description: '管理 OpenClaw 专用浏览器',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/browser\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'channels',
      command: '/channels',
      description: '管理连接的聊天频道',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/channels\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'clawbot',
      command: '/clawbot',
      description: '传统 clawbot 命令别名',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/clawbot\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'completion',
      command: '/completion',
      description: '生成 Shell 自动补全脚本',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/completion\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'config',
      command: '/config',
      description: '非交互式配置助手',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/config\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'configure',
      command: '/configure',
      description: '交互式设置向导',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/configure\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'cron',
      command: '/cron',
      description: '管理定时任务',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/cron\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'daemon',
      command: '/daemon',
      description: '网关服务',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/daemon\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'dashboard',
      command: '/dashboard',
      description: '打开控制面板',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/dashboard\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'devices',
      command: '/devices',
      description: '设备配对 + Token 管理',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/devices\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'directory',
      command: '/directory',
      description: '查找联系人和群组 ID',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/directory\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'dns',
      command: '/dns',
      description: 'DNS 辅助工具',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/dns\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'docs',
      command: '/docs',
      description: '搜索 OpenClaw 在线文档',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/docs\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'doctor',
      command: '/doctor',
      description: '健康检查 + 快速修复',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/doctor\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'gateway',
      command: '/gateway',
      description: '运行、检查和查询 WebSocket 网关',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/gateway\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'health',
      command: '/health',
      description: '获取网关健康状态',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/health\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'help',
      command: '/help',
      description: '显示命令帮助',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/help\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'hooks',
      command: '/hooks',
      description: '管理内部 Agent 钩子',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/hooks\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'logs',
      command: '/logs',
      description: '查看网关日志',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/logs\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'memory',
      command: '/memory',
      description: '搜索和重建记忆文件索引',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/memory\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'message',
      command: '/message',
      description: '发送、读取和管理消息',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/message\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'models',
      command: '/models',
      description: '发现、扫描和配置模型',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/models\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'node',
      command: '/node',
      description: '运行和管理无节点主机服务',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/node\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'nodes',
      command: '/nodes',
      description: '管理网关节点配对和节点命令',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/nodes\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'onboard',
      command: '/onboard',
      description: '交互式入职向导',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/onboard\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'pairing',
      command: '/pairing',
      description: '安全 DM 配对',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/pairing\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'plugins',
      command: '/plugins',
      description: '管理 OpenClaw 插件和扩展',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/plugins\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'qr',
      command: '/qr',
      description: '生成 iOS 配对二维码',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/qr\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'reset',
      command: '/reset',
      description: '重置本地配置/状态',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/reset\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'sandbox',
      command: '/sandbox',
      description: '管理沙盒容器',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/sandbox\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'security',
      command: '/security',
      description: '安全工具和本地配置审计',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/security\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'sessions',
      command: '/sessions',
      description: '查看存储的会话列表',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/sessions\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'setup',
      command: '/setup',
      description: '初始化本地配置和工作空间',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/setup\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'status',
      command: '/status',
      description: '显示频道健康和最近会话接收者',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/status\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'system',
      command: '/system',
      description: '系统事件、心跳和状态',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/system\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'tui',
      command: '/tui',
      description: '打开终端 UI',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/tui\`\n\n（此命令为系统命令）`;
      }
    },
    {
      slug: 'webhooks',
      command: '/webhooks',
      description: 'Webhook 辅助工具和集成',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return `提示：请使用 OpenClaw 直接执行 \`/webhooks\`\n\n（此命令为系统命令）`;
      }
    }
  ],
  
  // 我们开发的技能
  ours: [
    {
      slug: 'command-flow',
      command: '//',
      description: '查看所有指令（快捷触发）',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '管理',
      executeHint: '显示斜杠命令全览（支持分页 + 一键执行）',
      execute: async () => {
        const isTelegram = process.env.TELEGRAM_PLATFORM === 'true';
        if (isTelegram) {
          const { showCommandsTelegram } = require('./telegram-inline.js');
          const result = await showCommandsTelegram(1);
          return result.text + '\n\n💡 点击任意命令按钮，自动填入输入框，只需回车即可执行！';
        } else {
          const { showCommands } = require('./dashboard.js');
          return await showCommands(false, 1);
        }
      }
    },
    {
      slug: 'compress',
      command: '/compress <文本>',
      description: '4D 向量压缩，节省 60-80% Token',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '4D 压缩',
      executeHint: '自动压缩文本',
      execute: async (text) => {
        if (!text) {
          return '请提供要压缩的文本，例如：/compress 这是一段测试文本';
        }
        return `正在压缩文本...\n\n（4D 压缩功能待实现）`;
      }
    },
    {
      slug: 'warrior',
      command: '/warrior',
      description: '多模型协同（Neo+Gemini+Grok）',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '多模型',
      executeHint: '调用战车系统',
      execute: async () => {
        return `正在调用 Warrior System...\n\n（战车系统待实现）`;
      }
    },
    {
      slug: 'token-estimator',
      command: '/token-estimator <文本>',
      description: 'Token 精确预估（精度±3.5%）',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '4D 压缩',
      executeHint: '预估 Token 数量',
      execute: async (text) => {
        if (!text) {
          return '请提供要预估的文本';
        }
        return `正在预估 Token...\n\n（Token 预估功能待实现）`;
      }
    },
    {
      slug: 'skill-dashboard',
      command: '/skill-dashboard',
      description: '技能可视化管理（分页显示）',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '管理',
      executeHint: '显示技能控制台',
      execute: async () => {
        const { showDashboard } = require('../skill-dashboard/dashboard.js');
        return await showDashboard(1);
      }
    },
    {
      slug: 'dev-dashboard',
      command: '/dev-dashboard',
      description: '开发者模式（一键巡查）',
      safety: SAFETY.SAFE,
      source: SOURCE.OURS,
      category: '开发者',
      executeHint: '显示开发者巡查报告',
      execute: async () => {
        return `正在生成开发者巡查报告...\n\n（开发者模式待实现）`;
      }
    }
  ],
  
  // 第三方技能
  thirdParty: [
    {
      slug: 'notion',
      command: '/notion',
      description: 'Notion 笔记管理',
      safety: SAFETY.SAFE,
      source: SOURCE.THIRD_PARTY,
      category: '第三方',
      executeHint: '打开 Notion 技能',
      execute: async () => {
        return `正在打开 Notion 技能...\n\n（Notion 技能待实现）`;
      }
    },
    {
      slug: 'obsidian',
      command: '/obsidian',
      description: 'Obsidian 知识库管理',
      safety: SAFETY.SAFE,
      source: SOURCE.THIRD_PARTY,
      category: '第三方',
      executeHint: '打开 Obsidian 技能',
      execute: async () => {
        return `正在打开 Obsidian 技能...\n\n（Obsidian 技能待实现）`;
      }
    }
  ],
  
  // 隐藏命令
  hidden: [
    {
      slug: 'config-delete',
      command: '/config delete',
      description: '删除配置文件（极高风险）',
      safety: SAFETY.HIDDEN,
      source: SOURCE.NATIVE,
      category: '隐藏',
      warning: '⚠️ 此操作可能导致系统崩溃，请谨慎使用',
      executeHint: '需二次确认',
      confirm: true,
      confirmMessage: '⚠️ 删除配置文件不可逆，确定要继续吗？',
      execute: async () => {
        return `正在删除配置文件...\n\n（删除配置功能待实现）`;
      }
    },
    {
      slug: 'rm-rf',
      command: '/rm -rf <路径>',
      description: '删除文件（极高风险）',
      safety: SAFETY.HIDDEN,
      source: SOURCE.NATIVE,
      category: '隐藏',
      warning: '⚠️ 可能误删重要文件，请谨慎使用',
      executeHint: '需二次确认',
      confirm: true,
      confirmMessage: '⚠️ 删除文件不可逆，确定要继续吗？',
      execute: async (path) => {
        if (!path) {
          return '请提供要删除的路径';
        }
        return `正在删除 ${path}...\n\n（删除文件功能待实现）`;
      }
    }
  ]
};

/**
 * 获取所有命令（不包括隐藏命令）
 */
function getAllCommands(includeHidden = false) {
  const all = [
    ...COMMANDS.native,
    ...COMMANDS.ours,
    ...COMMANDS.thirdParty
  ];
  
  if (includeHidden) {
    all.push(...COMMANDS.hidden);
  }
  
  return all;
}

/**
 * 根据来源筛选命令
 */
function getCommandsBySource(source) {
  switch (source) {
    case SOURCE.NATIVE:
      return COMMANDS.native;
    case SOURCE.OURS:
      return COMMANDS.ours;
    case SOURCE.THIRD_PARTY:
      return COMMANDS.thirdParty;
    default:
      return getAllCommands();
  }
}

/**
 * 根据安全级别筛选命令
 */
function getCommandsBySafety(safety) {
  const all = getAllCommands(true);
  return all.filter(cmd => cmd.safety === safety);
}

/**
 * 搜索命令（支持别名搜索）
 */
function searchCommands(query) {
  const all = getAllCommands(true);
  const lowerQuery = query.toLowerCase();
  
  return all.filter(cmd => 
    cmd.command.toLowerCase().includes(lowerQuery) ||
    cmd.description.toLowerCase().includes(lowerQuery) ||
    cmd.slug.toLowerCase().includes(lowerQuery) ||
    (cmd.aliases && cmd.aliases.includes(lowerQuery)) ||
    cmd.command === lowerQuery  // 精确匹配命令
  );
}

/**
 * 根据 slug 或别名获取命令
 */
function getCommandBySlug(slug) {
  const all = getAllCommands(true);
  return all.find(cmd => 
    cmd.slug === slug || 
    (cmd.aliases && cmd.aliases.includes(slug))
  );
}

// 导出
module.exports = {
  SOURCE,
  SAFETY,
  COMMANDS,
  getAllCommands,
  getCommandsBySource,
  getCommandsBySafety,
  searchCommands,
  getCommandBySlug
};

// 测试
if (require.main === module) {
  console.log('测试命令数据：');
  console.log('==============');
  
  console.log('\n所有命令（不包括隐藏）：');
  console.log(getAllCommands().length);
  
  console.log('\nOpenClaw 原生命令：');
  console.log(getCommandsBySource(SOURCE.NATIVE).map(c => c.command));
  
  console.log('\n我们开发的命令：');
  console.log(getCommandsBySource(SOURCE.OURS).map(c => c.command));
  
  console.log('\n搜索 "压缩"：');
  console.log(searchCommands('压缩').map(c => c.command));
}
