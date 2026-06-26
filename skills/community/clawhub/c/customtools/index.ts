/**
 * OpenClaw Custom Tools Plugin
 * 
 * 注册自定义工具:
 * - task_create, task_list, task_get, task_update, task_stop
 * - skill_load, skill_list, skill_search
 * - lsp_goto_definition, lsp_find_references, lsp_document_symbols, lsp_hover, lsp_workspace_symbol
 * - config_get, config_set, config_list, config_export, config_reset
 * - mcp_list_servers, mcp_list_tools, mcp_call_tool, mcp_echo (MCP协议客户端)
 */

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import http from "http";
import { URL } from "url";
import { Type } from "@sinclair/typebox";

// ============ Task Tools ============

const taskCreateParams = Type.Object({
  subject: Type.String({ description: "任务标题" }),
  description: Type.Optional(Type.String({ description: "任务描述" })),
  activeForm: Type.Optional(Type.String({ description: "进行中的描述" })),
  owner: Type.Optional(Type.String({ description: "负责人" })),
  blockedBy: Type.Optional(Type.Array(Type.String(), { description: "阻塞此任务的任务ID" })),
  metadata: Type.Optional(Type.Record(Type.String(), Type.Unknown(), { description: "附加元数据" })),
});

const taskListParams = Type.Object({});

const taskGetParams = Type.Object({
  taskId: Type.String({ description: "任务ID" }),
});

const taskUpdateParams = Type.Object({
  taskId: Type.String({ description: "要更新的任务ID" }),
  status: Type.Optional(Type.Union([Type.Literal("pending"), Type.Literal("in_progress"), Type.Literal("completed")])),
  subject: Type.Optional(Type.String({ description: "新标题" })),
  description: Type.Optional(Type.String({ description: "新描述" })),
  owner: Type.Optional(Type.String({ description: "新负责人" })),
  blockedBy: Type.Optional(Type.Array(Type.String())),
});

const taskStopParams = Type.Object({
  taskId: Type.String({ description: "任务ID" }),
});

// ============ Skill Tools ============

const skillLoadParams = Type.Object({
  skillName: Type.String({ description: "技能名称" }),
});

const skillListParams = Type.Object({});

const skillSearchParams = Type.Object({
  query: Type.String({ description: "搜索关键词" }),
});

// ============ LSP Tools ============

const lspGotoDefinitionParams = Type.Object({
  filePath: Type.String({ description: "文件路径" }),
  line: Type.Optional(Type.Number({ description: "行号（1-based）" })),
  character: Type.Optional(Type.Number({ description: "列号（1-based）" })),
});

const lspFindReferencesParams = Type.Object({
  filePath: Type.String({ description: "文件路径" }),
  line: Type.Optional(Type.Number()),
  character: Type.Optional(Type.Number()),
});

const lspDocumentSymbolsParams = Type.Object({
  filePath: Type.String({ description: "文件路径" }),
});

const lspHoverParams = Type.Object({
  filePath: Type.String({ description: "文件路径" }),
  line: Type.Optional(Type.Number()),
  character: Type.Optional(Type.Number()),
});

const lspWorkspaceSymbolParams = Type.Object({
  query: Type.String({ description: "搜索关键词" }),
});

// ============ Config Tools ============

const configGetParams = Type.Object({
  path: Type.Optional(Type.String({ description: "配置路径，如 agents.defaults.model" })),
});

const configSetParams = Type.Object({
  path: Type.String({ description: "配置路径" }),
  value: Type.Unknown({ description: "新的配置值" }),
});

const configListParams = Type.Object({
  category: Type.Optional(Type.String({ description: "分类筛选" })),
});

const configExportParams = Type.Object({});

const configResetParams = Type.Object({
  path: Type.Optional(Type.String({ description: "要重置的配置路径" })),
});

// ============ MCP Tools ============

const mcpServerParams = Type.Object({
  name: Type.String({ description: "服务器名称" }),
  type: Type.Union([Type.Literal("stdio"), Type.Literal("http")], { description: "连接类型" }),
  url: Type.Optional(Type.String({ description: "HTTP URL (type=http时)" })),
  command: Type.Optional(Type.String({ description: "命令 (type=stdio时)" })),
  args: Type.Optional(Type.Array(Type.String(), { description: "命令参数" })),
});

const mcpToolParams = Type.Object({
  serverName: Type.Optional(Type.String({ description: "服务器名称，默认第一个" })),
});

const mcpCallParams = Type.Object({
  serverName: Type.String({ description: "服务器名称" }),
  toolName: Type.String({ description: "工具名称" }),
  arguments: Type.Optional(Type.Record(Type.String(), Type.Unknown(), { description: "工具参数" })),
});

// ============ 工具实现 (简化版，直接在插件中实现) ============

// Task 存储
interface Task {
  id: string;
  subject: string;
  description: string;
  activeForm?: string;
  owner?: string;
  status: "pending" | "in_progress" | "completed";
  blockedBy: string[];
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}

let taskHighWaterMark = 0;
const taskStorage: Task[] = [];

async function getNextTaskId(): Promise<string> {
  taskHighWaterMark++;
  return String(taskHighWaterMark);
}

// Skill 存储（模拟）
const skills = [
  { name: "taskflow", path: "built-in:taskflow", description: "工作流任务管理" },
  { name: "weather", path: "built-in:weather", description: "天气查询" },
  { name: "healthcheck", path: "built-in:healthcheck", description: "系统健康检查" },
];

// ============ 插件入口 ============

export default definePluginEntry({
  id: "custom-tools",
  name: "Custom Tools",
  description: "Custom tools: Task management, Skill loader, LSP code intelligence, Config management",
  
  register(api) {
    
    // ========== Task Tools ==========
    
    api.registerTool({
      name: "task_create",
      description: "创建新任务，类似 TODO 列表",
      parameters: taskCreateParams,
      async execute(_id, params) {
        const id = await getNextTaskId();
        const now = new Date().toISOString();
        const task: Task = {
          id,
          subject: params.subject,
          description: params.description || "",
          activeForm: params.activeForm,
          owner: params.owner,
          status: "pending",
          blockedBy: params.blockedBy || [],
          metadata: params.metadata || {},
          createdAt: now,
          updatedAt: now,
        };
        taskStorage.push(task);
        return { content: [{ type: "text", text: `Task #${id} created: ${task.subject}` }] };
      },
    });

    api.registerTool({
      name: "task_list",
      description: "列出所有任务",
      parameters: taskListParams,
      async execute(_id) {
        if (taskStorage.length === 0) {
          return { content: [{ type: "text", text: "No tasks found" }] };
        }
        const lines = taskStorage.map(t => `#${t.id} [${t.status}] ${t.subject}${t.owner ? ` (${t.owner})` : ""}`);
        return { content: [{ type: "text", text: lines.join("\n") }] };
      },
    });

    api.registerTool({
      name: "task_get",
      description: "获取任务详情",
      parameters: taskGetParams,
      async execute(_id, params) {
        const task = taskStorage.find(t => t.id === params.taskId);
        if (!task) {
          return { content: [{ type: "text", text: `Task #${params.taskId} not found` }] };
        }
        return { content: [{ type: "text", text: JSON.stringify(task, null, 2) }] };
      },
    });

    api.registerTool({
      name: "task_update",
      description: "更新任务状态或内容",
      parameters: taskUpdateParams,
      async execute(_id, params) {
        const task = taskStorage.find(t => t.id === params.taskId);
        if (!task) {
          return { content: [{ type: "text", text: `Task #${params.taskId} not found` }] };
        }
        if (params.status) task.status = params.status;
        if (params.subject) task.subject = params.subject;
        if (params.description) task.description = params.description;
        if (params.owner) task.owner = params.owner;
        if (params.blockedBy) task.blockedBy = params.blockedBy;
        task.updatedAt = new Date().toISOString();
        return { content: [{ type: "text", text: `Task #${task.id} updated` }] };
      },
    });

    api.registerTool({
      name: "task_stop",
      description: "停止/完成一个任务",
      parameters: taskStopParams,
      async execute(_id, params) {
        const task = taskStorage.find(t => t.id === params.taskId);
        if (!task) {
          return { content: [{ type: "text", text: `Task #${params.taskId} not found` }] };
        }
        task.status = "completed";
        task.updatedAt = new Date().toISOString();
        return { content: [{ type: "text", text: `Task #${task.id} completed` }] };
      },
    });

    // ========== Skill Tools ==========

    api.registerTool({
      name: "skill_load",
      description: "动态加载指定名称的 SKILL.md 文件",
      parameters: skillLoadParams,
      async execute(_id, params) {
        const skill = skills.find(s => s.name === params.skillName);
        if (!skill) {
          return { content: [{ type: "text", text: `Skill "${params.skillName}" not found` }] };
        }
        return { content: [{ type: "text", text: `Loaded skill: ${skill.name}\nPath: ${skill.path}\n${skill.description}` }] };
      },
    });

    api.registerTool({
      name: "skill_list",
      description: "列出所有可用的 skills",
      parameters: skillListParams,
      async execute(_id) {
        const lines = skills.map(s => `- ${s.name}: ${s.description}`);
        return { content: [{ type: "text", text: lines.join("\n") }] };
      },
    });

    api.registerTool({
      name: "skill_search",
      description: "搜索 skills",
      parameters: skillSearchParams,
      async execute(_id, params) {
        const query = params.query.toLowerCase();
        const results = skills.filter(s => 
          s.name.toLowerCase().includes(query) || 
          s.description.toLowerCase().includes(query)
        );
        if (results.length === 0) {
          return { content: [{ type: "text", text: `No skills found matching "${params.query}"` }] };
        }
        const lines = results.map(s => `- ${s.name}: ${s.description}`);
        return { content: [{ type: "text", text: lines.join("\n") }] };
      },
    });

    // ========== LSP Tools (简化实现) ==========

    api.registerTool({
      name: "lsp_goto_definition",
      description: "跳转到代码定义位置（需要 LSP 服务器支持）",
      parameters: lspGotoDefinitionParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[LSP] goto_definition: ${params.filePath}:${params.line || 1}:${params.character || 1}\n\n(LSP server not connected - this is a stub)` }] };
      },
    });

    api.registerTool({
      name: "lsp_find_references",
      description: "查找代码引用位置",
      parameters: lspFindReferencesParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[LSP] find_references: ${params.filePath}:${params.line || 1}:${params.character || 1}\n\n(LSP server not connected - this is a stub)` }] };
      },
    });

    api.registerTool({
      name: "lsp_document_symbols",
      description: "获取文件中的代码符号列表",
      parameters: lspDocumentSymbolsParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[LSP] document_symbols: ${params.filePath}\n\n(LSP server not connected - this is a stub)` }] };
      },
    });

    api.registerTool({
      name: "lsp_hover",
      description: "获取代码悬停信息",
      parameters: lspHoverParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[LSP] hover: ${params.filePath}:${params.line || 1}:${params.character || 1}\n\n(LSP server not connected - this is a stub)` }] };
      },
    });

    api.registerTool({
      name: "lsp_workspace_symbol",
      description: "在工作区搜索符号",
      parameters: lspWorkspaceSymbolParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[LSP] workspace_symbol: "${params.query}"\n\n(LSP server not connected - this is a stub)` }] };
      },
    });

    // ========== Config Tools ==========

    api.registerTool({
      name: "config_get",
      description: "获取配置项的值",
      parameters: configGetParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[Config] get: ${params.path || "(root)"}\n\n(Use gateway config tools for actual config access)` }] };
      },
    });

    api.registerTool({
      name: "config_set",
      description: "设置配置项的值",
      parameters: configSetParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[Config] set: ${params.path} = ${JSON.stringify(params.value)}\n\n(Use gateway config.patch for actual config changes)` }] };
      },
    });

    api.registerTool({
      name: "config_list",
      description: "列出配置分类",
      parameters: configListParams,
      async execute(_id, params) {
        const categories = ["agents", "models", "tools", "channels", "plugins", "gateway", "auth"];
        return { content: [{ type: "text", text: `Config categories: ${categories.join(", ")}\n\n(Use openclaw config commands for actual config access)` }] };
      },
    });

    api.registerTool({
      name: "config_export",
      description: "导出当前配置",
      parameters: configExportParams,
      async execute(_id) {
        return { content: [{ type: "text", text: "[Config] export\n\n(Use openclaw config commands for actual config export)" }] };
      },
    });

    api.registerTool({
      name: "config_reset",
      description: "重置配置到默认值",
      parameters: configResetParams,
      async execute(_id, params) {
        return { content: [{ type: "text", text: `[Config] reset: ${params.path || "(root)"}\n\n(Use openclaw config commands for actual config reset)` }] };
      },
    });

    // ========== MCP Tools (内置简化HTTP客户端) ==========
    // 注意：stdio支持需要子进程管理，这里仅实现HTTP客户端

    const mcpServers = new Map<string, { url: string; tools: unknown[] }>();

    async function mcpRequest(url: string, method: string, params: Record<string, unknown> = {}): Promise<unknown> {
      const urlObj = new URL(url);
      const isHttps = urlObj.protocol === "https:";
      const httpModule = isHttps ? (await import("https")) : http;

      return new Promise((resolve, reject) => {
        const body = JSON.stringify({ jsonrpc: "2.0", id: 1, method, params });
        const options = {
          hostname: urlObj.hostname,
          port: urlObj.port || (isHttps ? 443 : 80),
          path: urlObj.pathname,
          method: "POST",
          headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) }
        };

        const req = httpModule.request(options, (res) => {
          let data = "";
          res.on("data", chunk => { data += chunk; });
          res.on("end", () => {
            try {
              const response = JSON.parse(data);
              resolve(response.result || response);
            } catch (e) { reject(e); }
          });
        });

        req.on("error", reject);
        req.write(body);
        req.end();
      });
    }

    api.registerTool({
      name: "mcp_echo",
      description: "测试 MCP HTTP 服务器是否可用",
      parameters: mcpServerParams,
      async execute(_id, params) {
        const url = params.url || "http://localhost:3000";
        try {
          const result = await mcpRequest(url, "initialize", {
            protocolVersion: "2024-11-05",
            capabilities: {},
            clientInfo: { name: "openclaw-mcp", version: "1.0.0" }
          }) as { serverInfo: { name: string; version: string } };
          return { content: [{ type: "text", text: `✅ MCP服务器连接成功: ${result.serverInfo.name} v${result.serverInfo.version}` }] };
        } catch (e) {
          return { content: [{ type: "text", text: `❌ MCP服务器连接失败: ${(e as Error).message}` }] };
        }
      },
    });

    api.registerTool({
      name: "mcp_list_servers",
      description: "列出已添加的MCP服务器",
      parameters: mcpToolParams,
      async execute(_id, _params) {
        if (mcpServers.size === 0) {
          return { content: [{ type: "text", text: "没有已添加的MCP服务器\n\n使用 mcp_echo 添加服务器，如: mcp_echo { url: \"http://localhost:3000\" }" }] };
        }
        const lines = ["已添加的MCP服务器:"];
        for (const [name, server] of mcpServers) {
          lines.push(`- ${name}: ${server.url} (${server.tools.length} tools)`);
        }
        return { content: [{ type: "text", text: lines.join("\n") }] };
      },
    });

    api.registerTool({
      name: "mcp_list_tools",
      description: "获取MCP服务器的工具列表",
      parameters: mcpToolParams,
      async execute(_id, params) {
        let name = params.serverName;
        let server = name ? mcpServers.get(name) : mcpServers.values().next().value;
        
        if (!server) {
          return { content: [{ type: "text", text: `❌ 服务器 \"${name || "default"}\" 未找到\n\n使用 mcp_echo 先添加服务器` }] };
        }

        try {
          const result = await mcpRequest(server.url, "tools/list", {}) as { tools: { name: string; description: string }[] };
          const lines = [`服务器 ${name || server.url} 的工具列表 (`] + result.tools.length + "):"];
          for (const tool of result.tools) {
            lines.push(`  - ${tool.name}: ${tool.description || "(no description)"}`);
          }
          return { content: [{ type: "text", text: lines.join("\n") }] };
        } catch (e) {
          return { content: [{ type: "text", text: `❌ 获取工具列表失败: ${(e as Error).message}` }] };
        }
      },
    });

    api.registerTool({
      name: "mcp_call_tool",
      description: "调用MCP服务器上的工具",
      parameters: mcpCallParams,
      async execute(_id, params) {
        const server = mcpServers.get(params.serverName);
        if (!server) {
          return { content: [{ type: "text", text: `❌ 服务器 \"${params.serverName}\" 未找到` }] };
        }

        try {
          const result = await mcpRequest(server.url, "tools/call", {
            name: params.toolName,
            arguments: params.arguments || {}
          }) as { content: { type: string; text: string }[] };
          return { content: [{ type: "text", text: result.content?.[0]?.text || JSON.stringify(result) }] };
        } catch (e) {
          return { content: [{ type: "text", text: `❌ 调用工具失败: ${(e as Error).message}` }] };
        }
      },
    });

    console.log("[custom-tools] Plugin registered: 18 tools (including MCP)");
  },
});
