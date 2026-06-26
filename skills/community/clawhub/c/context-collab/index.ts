/**
 * Context Plugin — Main Entry Point v0.5
 *
 * Uses execute + jsonResult pattern (same as bundled plugins like firecrawl).
 */

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { fetchProtocol, buildPromptInjection } from "./hooks/prompt-hook.js";
import { handleContextFileRoute } from "./routes/file-access.js";

const CTX_BASE_DEFAULT = "https://context-server-mj6f.onrender.com";

// Inline jsonResult to avoid SDK import path issues with bundled SDK
function jsonResult(payload: unknown) {
  const text = typeof payload === "string" ? payload : JSON.stringify(payload, null, 2);
  return { content: [{ type: "text" as const, text }], details: payload };
}

async function ctxFetch(serverUrl: string, method: string, path: string, body?: any): Promise<any> {
  const opts: any = {
    method,
    headers: { "Content-Type": "application/json", "X-Context-Plugin": "true" },
    signal: AbortSignal.timeout(8000),
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${serverUrl}${path}`, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

// Helper: resolve channel + groupId from command context
function resolveGroupFromCommandCtx(ctx: any): { channel: string; groupId: string } | null {
  // ctx from registerCommand has: channelId, guildId (discord), groupId (dmwork), etc.
  const channelType = ctx.channel || ctx.channelType || "";
  const guildId = ctx.guildId;
  const groupId = ctx.groupId;
  const channelId = ctx.channelId;

  if (channelType === "discord" || guildId) {
    return { channel: "discord", groupId: channelId || guildId || "" };
  }
  if (channelType === "dmwork" || groupId) {
    return { channel: "dmwork", groupId: groupId || "" };
  }
  // Fallback: try session key
  const sessionKey = ctx.sessionKey || "";
  return extractChannelGroup(sessionKey, channelId || "");
}

export default definePluginEntry({
  id: "context",
  name: "context",
  description: "Multi-agent collaboration protocol engine — shared spaces with auto-injected context",

  register(api) {
    const logger = api.logger;
    const pluginConfig = (api.pluginConfig || {}) as { port?: number; serverUrl?: string; autoInject?: boolean };
    const serverUrl = pluginConfig.serverUrl || CTX_BASE_DEFAULT;
    const autoInject = pluginConfig.autoInject !== false;

    // ═══════════════════════════════════════
    // 1. PROMPT HOOK
    // ═══════════════════════════════════════

    if (autoInject) {
      api.on("before_prompt_build", async (_event, ctx) => {
        const channelId = ctx.channelId;
        if (!channelId) return;
        const sessionKey = ctx.sessionKey || "";
        logger.info(`[context] prompt-hook: sessionKey=${sessionKey}, channelId=${channelId}`);
        const cg = extractChannelGroup(sessionKey, channelId);
        if (!cg) return;

        try {
          // Look up space
          const lookupRes = await fetch(
            `${serverUrl}/api/spaces/lookup?channel=${encodeURIComponent(cg.channel)}&groupId=${encodeURIComponent(cg.groupId)}`,
            { signal: AbortSignal.timeout(3000) }
          );
          if (!lookupRes.ok) return;
          const lookupData = await lookupRes.json() as any;
          const spaceId = lookupData.space?.id;
          if (!spaceId) return;

          // Fetch protocol
          const protocolRes = await fetch(
            `${serverUrl}/api/spaces/${spaceId}/protocol`,
            { signal: AbortSignal.timeout(3000) }
          );
          if (!protocolRes.ok) return;
          const protocol = await protocolRes.json() as any;

          const injection = buildPromptInjection(protocol, spaceId);
          logger.info(`[context] prompt-hook: injecting protocol for space ${spaceId} (${injection.length} chars)`);
          return { appendSystemContext: injection };
        } catch (err: any) {
          logger.info(`[context] prompt-hook: error — ${err.message}`);
          return;
        }
      });
    }

    // ═══════════════════════════════════════
    // 2. AGENT TOOLS
    // ═══════════════════════════════════════

    api.registerTool({
      name: "context_create_space",
      label: "Create Context Space",
      description: "Create a new Context space for the current group/channel. A Context space enables multi-agent collaboration with shared files, team info, and task tracking.",
      parameters: {
        type: "object",
        properties: {
          name: { type: "string", description: "Space name" },
          channel: { type: "string", description: "Channel type (discord, dmwork, telegram, slack, etc.)" },
          group_id: { type: "string", description: "Group/guild/chat ID" },
          created_by: { type: "string", description: "Creator identifier" },
          template: { type: "string", enum: ["software-dev", "content", "research", "blank"], description: "Project template (default: software-dev)" },
        },
        required: ["name", "channel", "group_id", "created_by"],
      },
      execute: async (_id: string, params: any) => {
        const { name, channel, group_id, created_by, template } = params;
        const data = await ctxFetch(serverUrl, "POST", "/api/spaces", {
          name, channel, groupId: group_id, createdBy: created_by, template: template || "software-dev",
        });
        const spaceId = data.space?.id || data.space?.spaceId;
        const webUrl = `${serverUrl}/s/${spaceId}`;
        const ctxUrl = `${serverUrl}/ctx/${spaceId}/`;
        if (data.existed) return jsonResult({ status: "already_exists", space: data.space, webUrl, ctxUrl });
        return jsonResult({ status: "created", space: data.space, webUrl, ctxUrl, message: `Space created. Web UI: ${webUrl}` });
      },
    });

    api.registerTool({
      name: "context_delete_space",
      label: "Delete Context Space",
      description: "Delete an entire Context space and all its files. This is irreversible.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID to delete" },
        },
        required: ["space_id"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id } = params;
        const data = await ctxFetch(serverUrl, "DELETE", `/api/spaces/${space_id}`);
        return jsonResult(data);
      },
    });

    api.registerTool({
      name: "context_lookup_space",
      label: "Lookup Context Space",
      description: "Look up the Context space associated with a specific channel group. Use this to check if a group already has a shared space.",
      parameters: {
        type: "object",
        properties: {
          channel: { type: "string", description: "Channel type (discord, dmwork, telegram, slack, etc.)" },
          group_id: { type: "string", description: "Group/guild/chat ID" },
        },
        required: ["channel", "group_id"],
      },
      execute: async (_id: string, params: any) => {
        const { channel, group_id } = params;
        try {
          const data = await ctxFetch(serverUrl, "GET", `/api/spaces/lookup?channel=${encodeURIComponent(channel)}&groupId=${encodeURIComponent(group_id)}`);
          return jsonResult({ found: true, space: data.space });
        } catch {
          return jsonResult({ found: false, message: "No Context space found for this group." });
        }
      },
    });

    api.registerTool({
      name: "context_read_file",
      label: "Read Context File",
      description: "Read a file from the shared Context space. Use this to access shared documents, protocol files (SPACE.md, TEAM.md, TASK.md), or any team artifacts.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          path: { type: "string", description: "File path within the space (e.g., 'SPACE.md', 'docs/prd.md')" },
        },
        required: ["space_id", "path"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, path } = params;
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/files/${path}`);
        return jsonResult({ file: { path: data.file.path, content: data.file.content, version: data.file.version, updatedAt: data.file.updatedAt } });
      },
    });

    api.registerTool({
      name: "context_write_file",
      label: "Write Context File",
      description: "Write or update a file in the shared Context space. All your work output should be written here, NOT to local workspace. This ensures all collaborators can access your results.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          path: { type: "string", description: "File path within the space (e.g., 'docs/design.md')" },
          content: { type: "string", description: "File content" },
          modified_by: { type: "string", description: "Who is writing this file (your agent name or ID)" },
        },
        required: ["space_id", "path", "content", "modified_by"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, path, content, modified_by } = params;
        const data = await ctxFetch(serverUrl, "PUT", `/api/spaces/${space_id}/files/${path}`, { content, modifiedBy: modified_by });
        return jsonResult({
          success: true,
          file: { path: data.file.path, version: data.file.version, size: data.file.size },
          url: `${serverUrl}/ctx/${space_id}/${path}`,
        });
      },
    });

    api.registerTool({
      name: "context_list_files",
      label: "List Context Files",
      description: "List all files in the shared Context space. Use to see what documents, artifacts, and protocol files exist.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          prefix: { type: "string", description: "Optional path prefix filter (e.g., 'docs/')" },
        },
        required: ["space_id"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, prefix } = params;
        const q = prefix ? `?prefix=${encodeURIComponent(prefix)}` : "";
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/files${q}`);
        return jsonResult({ files: data.files.map((f: any) => ({ path: f.path, size: f.size, version: f.version, updatedAt: f.updatedAt })) });
      },
    });

    api.registerTool({
      name: "context_delete_file",
      label: "Delete Context File",
      description: "Delete a file from the shared Context space.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          path: { type: "string", description: "File path to delete" },
        },
        required: ["space_id", "path"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, path } = params;
        await ctxFetch(serverUrl, "DELETE", `/api/spaces/${space_id}/files/${path}`);
        return jsonResult({ success: true, message: `Deleted: ${path}` });
      },
    });

    api.registerTool({
      name: "context_get_protocol",
      label: "Get Context Protocol",
      description: "Get all three protocol files (SPACE.md, TEAM.md, TASK.md) at once. Use this to quickly understand the current collaboration state.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
        },
        required: ["space_id"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id } = params;
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/protocol`);
        return jsonResult(data);
      },
    });

    api.registerTool({
      name: "context_update_task",
      label: "Update Context Task",
      description: "Update the TASK.md file in the shared space. Call this when you start, complete, or make progress on a task.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          content: { type: "string", description: "New TASK.md content (full replacement)" },
          modified_by: { type: "string", description: "Who is updating (your name/ID)" },
        },
        required: ["space_id", "content", "modified_by"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, content, modified_by } = params;
        const data = await ctxFetch(serverUrl, "PUT", `/api/spaces/${space_id}/files/TASK.md`, { content, modifiedBy: modified_by });
        return jsonResult({ success: true, version: data.file.version });
      },
    });

    api.registerTool({
      name: "context_add_member",
      label: "Add Context Member",
      description: "Add a team member (human or agent) to the Context space. This updates the member registry.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          name: { type: "string", description: "Member display name" },
          type: { type: "string", enum: ["human", "agent"], description: "human or agent" },
          role: { type: "string", description: "Role (e.g., PM, Dev, QA, Design)" },
          channel_user_id: { type: "string", description: "Channel-specific user ID" },
          capabilities: { type: "array", items: { type: "string" }, description: "Skills/tools this member has" },
        },
        required: ["space_id", "name", "type"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, name, type, role, channel_user_id, capabilities } = params;
        const data = await ctxFetch(serverUrl, "POST", `/api/spaces/${space_id}/members`, {
          name, type, role, channelUserId: channel_user_id, capabilities,
        });
        return jsonResult({ success: true, member: data.member });
      },
    });

    api.registerTool({
      name: "context_list_members",
      label: "List Context Members",
      description: "List all members of the Context space (both humans and agents).",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
        },
        required: ["space_id"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id } = params;
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/members`);
        return jsonResult({ members: data.members });
      },
    });

    api.registerTool({
      name: "context_get_annotations",
      label: "Get Annotations",
      description: "Get annotations (human comments/feedback) on a file. Use this to see what humans want changed. Only returns 'open' annotations by default.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          file_path: { type: "string", description: "File path to get annotations for (optional, omit for all files)" },
          status: { type: "string", enum: ["open", "resolved", "all"], description: "Filter by status (default: open)" },
        },
        required: ["space_id"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, file_path, status } = params;
        let q = "?";
        if (file_path) q += `file=${encodeURIComponent(file_path)}&`;
        if (status && status !== "all") q += `status=${encodeURIComponent(status)}`;
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/annotations${q}`);
        return jsonResult({ annotations: data.annotations });
      },
    });

    api.registerTool({
      name: "context_resolve_annotation",
      label: "Resolve Annotation",
      description: "Mark an annotation as resolved after addressing the feedback. Call this after you've made the requested changes.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          annotation_id: { type: "string", description: "Annotation ID to resolve" },
          resolved_by: { type: "string", description: "Who resolved it (your name/ID)" },
        },
        required: ["space_id", "annotation_id", "resolved_by"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, annotation_id, resolved_by } = params;
        const data = await ctxFetch(serverUrl, "PUT", `/api/spaces/${space_id}/annotations/${annotation_id}/resolve`, { resolvedBy: resolved_by });
        return jsonResult({ success: true, annotation: data.annotation });
      },
    });

    api.registerTool({
      name: "context_search_files",
      label: "Search Context Files",
      description: "Search for text across all files in the shared Context space. Returns matching files and line numbers.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          query: { type: "string", description: "Search query text" },
        },
        required: ["space_id", "query"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, query } = params;
        const data = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}/search?q=${encodeURIComponent(query)}`);
        return jsonResult(data);
      },
    });

    api.registerTool({
      name: "context_notify_member",
      label: "Notify Context Member",
      description: "Send a notification message to a specific member or the whole group about a Context event (file update, task change, annotation, etc). Routes through the IM channel associated with the Space.",
      parameters: {
        type: "object",
        properties: {
          space_id: { type: "string", description: "Space ID" },
          message: { type: "string", description: "Notification message to send" },
          member_name: { type: "string", description: "Target member name (optional, omit for group-wide)" },
        },
        required: ["space_id", "message"],
      },
      execute: async (_id: string, params: any) => {
        const { space_id, message, member_name } = params;
        // Look up space to get channel info
        try {
          const spaceData = await ctxFetch(serverUrl, "GET", `/api/spaces/${space_id}`);
          const space = spaceData.space;
          if (!space) return jsonResult({ success: false, error: "Space not found" });

          const channel = space.channel; // discord, dmwork, telegram, etc.
          const groupId = space.groupId;

          // Format message
          const prefix = member_name ? `@${member_name} ` : "";
          const fullMessage = `${prefix}📢 [Context 通知]\n${message}`;

          // Use the messaging API to send to the group
          // This returns info for the agent to send via message tool
          return jsonResult({
            success: true,
            notification: {
              channel,
              target: groupId,
              message: fullMessage,
              hint: "Use the message tool with action=send to deliver this notification to the group.",
            },
          });
        } catch (err: any) {
          return jsonResult({ success: false, error: err.message });
        }
      },
    });

    // ═══════════════════════════════════════
    // 3. HTTP ROUTES
    // ═══════════════════════════════════════

    api.registerHttpRoute({
      path: "/ctx",
      match: "prefix",
      auth: "plugin",
      handler: handleContextFileRoute,
    });

    // ═══════════════════════════════════════
    // 4. SLASH COMMANDS (real implementations)
    // ═══════════════════════════════════════

    api.registerCommand({
      name: "ctx_create",
      description: "🏗️ Create a Context space for this group",
      options: [
        { name: "name", description: "Space name", type: "string", required: false },
        { name: "template", description: "Template: software-dev, content, research, blank", type: "string", required: false },
      ],
      acceptsArgs: true,
      handler: async (ctx) => {
        const cg = resolveGroupFromCommandCtx(ctx);
        if (!cg || !cg.groupId) return { text: "❌ Cannot determine group context. Use this command in a group chat." };

        const args: any = ctx.args || {};
        const name = args.name || `Space-${cg.groupId.slice(0, 8)}`;
        const template = args.template || "software-dev";

        try {
          const data = await ctxFetch(serverUrl, "POST", "/api/spaces", {
            name,
            channel: cg.channel,
            groupId: cg.groupId,
            createdBy: ctx.senderId || "unknown",
            template,
          });

          if (data.existed) {
            const space = data.space;
            return { text: `ℹ️ 本群已有 Context Space: **${space.name}**\n🆔 ID: \`${space.id}\`\n📅 创建于: ${new Date(space.createdAt).toLocaleDateString("zh-CN")}` };
          }

          const space = data.space;
          return { text: `🏗️ Context Space 创建成功！\n\n📛 名称: **${space.name}**\n🆔 ID: \`${space.id}\`\n📋 模板: ${template}\n📁 已初始化: SPACE.md + TEAM.md + TASK.md\n\n💡 AI 在本群对话时会自动获取协作上下文。` };
        } catch (err: any) {
          return { text: `❌ 创建失败: ${err.message}` };
        }
      },
    });

    api.registerCommand({
      name: "ctx_info",
      description: "📊 Show Context space info for this group",
      handler: async (ctx) => {
        const cg = resolveGroupFromCommandCtx(ctx);
        if (!cg || !cg.groupId) return { text: "❌ Cannot determine group context." };

        try {
          const data = await ctxFetch(serverUrl, "GET",
            `/api/spaces/lookup?channel=${encodeURIComponent(cg.channel)}&groupId=${encodeURIComponent(cg.groupId)}`);
          const space = data.space;

          // Get file count
          const filesData = await ctxFetch(serverUrl, "GET", `/api/spaces/${space.id}/files`);
          const membersData = await ctxFetch(serverUrl, "GET", `/api/spaces/${space.id}/members`);

          return {
            text: `📊 **${space.name}**\n\n🆔 ID: \`${space.id}\`\n📁 文件: ${filesData.files.length} 个\n👥 成员: ${membersData.members.length} 人\n📅 创建: ${new Date(space.createdAt).toLocaleDateString("zh-CN")}\n🔗 渠道: ${space.channel}`,
          };
        } catch {
          return { text: "ℹ️ 本群暂无 Context Space。使用 `/ctx_create` 创建一个。" };
        }
      },
    });

    api.registerCommand({
      name: "ctx_files",
      description: "📋 List files in this group's Context space",
      handler: async (ctx) => {
        const cg = resolveGroupFromCommandCtx(ctx);
        if (!cg || !cg.groupId) return { text: "❌ Cannot determine group context." };

        try {
          const lookupData = await ctxFetch(serverUrl, "GET",
            `/api/spaces/lookup?channel=${encodeURIComponent(cg.channel)}&groupId=${encodeURIComponent(cg.groupId)}`);
          const spaceId = lookupData.space.id;

          const filesData = await ctxFetch(serverUrl, "GET", `/api/spaces/${spaceId}/files`);
          const files = filesData.files;

          if (files.length === 0) return { text: "📋 空间中暂无文件。" };

          const list = files
            .map((f: any) => {
              const icon = f.path.endsWith(".md") ? "📝" : "📄";
              const size = f.size < 1024 ? `${f.size}B` : `${(f.size / 1024).toFixed(1)}KB`;
              return `${icon} \`${f.path}\` (${size}, v${f.version})`;
            })
            .join("\n");

          return { text: `📋 **文件列表** (${files.length} 个)\n\n${list}` };
        } catch {
          return { text: "ℹ️ 本群暂无 Context Space。使用 `/ctx_create` 创建一个。" };
        }
      },
    });

    api.registerCommand({
      name: "ctx_tasks",
      description: "📝 Show current tasks from TASK.md",
      handler: async (ctx) => {
        const cg = resolveGroupFromCommandCtx(ctx);
        if (!cg || !cg.groupId) return { text: "❌ Cannot determine group context." };

        try {
          const lookupData = await ctxFetch(serverUrl, "GET",
            `/api/spaces/lookup?channel=${encodeURIComponent(cg.channel)}&groupId=${encodeURIComponent(cg.groupId)}`);
          const spaceId = lookupData.space.id;

          const fileData = await ctxFetch(serverUrl, "GET", `/api/spaces/${spaceId}/files/TASK.md`);
          return { text: fileData.file.content };
        } catch {
          return { text: "ℹ️ 本群暂无 Context Space 或 TASK.md。" };
        }
      },
    });

    api.registerCommand({
      name: "ctx_team",
      description: "👥 Show team members from TEAM.md",
      handler: async (ctx) => {
        const cg = resolveGroupFromCommandCtx(ctx);
        if (!cg || !cg.groupId) return { text: "❌ Cannot determine group context." };

        try {
          const lookupData = await ctxFetch(serverUrl, "GET",
            `/api/spaces/lookup?channel=${encodeURIComponent(cg.channel)}&groupId=${encodeURIComponent(cg.groupId)}`);
          const spaceId = lookupData.space.id;

          const fileData = await ctxFetch(serverUrl, "GET", `/api/spaces/${spaceId}/files/TEAM.md`);
          return { text: fileData.file.content };
        } catch {
          return { text: "ℹ️ 本群暂无 Context Space 或 TEAM.md。" };
        }
      },
    });

    // ═══════════════════════════════════════
    // 5. BOOTSTRAP HOOK — Auto-inject collaboration rules
    // ═══════════════════════════════════════

    api.registerHook("agent:bootstrap", async (event) => {
      if (event.type !== "agent" || event.action !== "bootstrap") return;

      // Check if AGENTS.md already has Context rules
      const ctx = (event as any).context;
      if (!ctx || !ctx.bootstrapFiles) {
        logger.info("[context] Agent bootstrap — no bootstrap context, skipping AGENTS.md injection");
        return;
      }

      const agentsFile = ctx.bootstrapFiles.find((f: any) => f.name === "AGENTS.md");
      if (!agentsFile || !agentsFile.content) {
        logger.info("[context] Agent bootstrap — AGENTS.md not found in bootstrap files");
        return;
      }

      // Check if already has Context rules
      if (agentsFile.content.includes("Context 协作规则") || agentsFile.content.includes("context_")) {
        logger.info("[context] Agent bootstrap — AGENTS.md already has Context rules");
        return;
      }

      // Inject Context collaboration rules
      const contextRules = `

## Context 协作规则

当你在群聊中工作时，遵循以下规则：

1. **使用 Context Space** — 所有工作产出写到群关联的 Context Space，不要放本地 workspace
2. **分享用 URL** — 分享文件时发送 Context URL，不要发原文
3. **先读 TASK.md** — 开始工作前先用 \`context_get_protocol\` 了解当前任务状态
4. **及时更新** — 完成任务后用 \`context_update_task\` 更新 TASK.md
5. **自动感知** — 如果当前群没有 Space，提示用户创建或用 \`context_create_space\` 创建
`;

      agentsFile.content += contextRules;
      logger.info("[context] Agent bootstrap — injected Context rules into AGENTS.md");
    }, { name: "context-bootstrap" });

    logger.info("[context] ✅ Plugin v1.2.0 registered (15 tools, prompt hook, HTTP routes, 5 commands)");
  },
});

// ═══════════════════════════════════════
// Helpers
// ═══════════════════════════════════════

function extractChannelGroup(sessionKey: string, channelId: string): { channel: string; groupId: string } | null {
  // Discord: agent:main:discord:channel:<channelId>
  const discordChannelMatch = sessionKey.match(/discord:channel:(\d+)/);
  if (discordChannelMatch) return { channel: "discord", groupId: discordChannelMatch[1] };
  const discordGuildMatch = sessionKey.match(/discord:guild:(\d+)/);
  if (discordGuildMatch) return { channel: "discord", groupId: discordGuildMatch[1] };

  // DMWork: agent:main:dmwork:group:<uuid>
  const dmworkMatch = sessionKey.match(/dmwork:group:([a-f0-9]+)/);
  if (dmworkMatch) return { channel: "dmwork", groupId: dmworkMatch[1] };
  if (sessionKey.includes("dmwork:default:direct:")) return null;

  // Telegram
  const telegramMatch = sessionKey.match(/telegram:(-?\d+)/);
  if (telegramMatch) return { channel: "telegram", groupId: telegramMatch[1] };

  // Slack
  const slackMatch = sessionKey.match(/slack:(\w+):(\w+)/);
  if (slackMatch) return { channel: "slack", groupId: `${slackMatch[1]}:${slackMatch[2]}` };

  // Fallback
  if (channelId && channelId.includes(":")) {
    const parts = channelId.split(":");
    if (parts.length >= 2) return { channel: parts[0], groupId: parts[1] };
  }
  return null;
}
