/**
 * Context Plugin — Agent Tools
 *
 * Tools that AI agents use to interact with the shared Context space.
 */

export type ToolDef = {
  name: string;
  description: string;
  parameters: Record<string, any>;
  handler: (params: any) => Promise<string>;
};

const CTX_BASE = "http://localhost:3100";

async function ctxFetch(method: string, path: string, body?: any): Promise<any> {
  const opts: any = {
    method,
    headers: { "Content-Type": "application/json", "X-Context-Plugin": "true" },
    signal: AbortSignal.timeout(8000),
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${CTX_BASE}${path}`, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

export const tools: ToolDef[] = [
  {
    name: "context_create_space",
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
    handler: async ({ name, channel, group_id, created_by, template }) => {
      const data = await ctxFetch("POST", "/api/spaces", {
        name,
        channel,
        groupId: group_id,
        createdBy: created_by,
        template: template || "software-dev",
      });
      if (data.existed) {
        return JSON.stringify({ status: "already_exists", space: data.space });
      }
      return JSON.stringify({ status: "created", space: data.space, message: "Space created with SPACE.md, TEAM.md, and TASK.md initialized from template." });
    },
  },

  {
    name: "context_lookup_space",
    description: "Look up the Context space associated with a specific channel group. Use this to check if a group already has a shared space.",
    parameters: {
      type: "object",
      properties: {
        channel: { type: "string", description: "Channel type (discord, dmwork, telegram, slack, etc.)" },
        group_id: { type: "string", description: "Group/guild/chat ID" },
      },
      required: ["channel", "group_id"],
    },
    handler: async ({ channel, group_id }) => {
      try {
        const data = await ctxFetch("GET", `/api/spaces/lookup?channel=${encodeURIComponent(channel)}&groupId=${encodeURIComponent(group_id)}`);
        return JSON.stringify({ found: true, space: data.space });
      } catch {
        return JSON.stringify({ found: false, message: "No Context space found for this group." });
      }
    },
  },

  {
    name: "context_read_file",
    description: "Read a file from the shared Context space. Use this to access shared documents, protocol files (SPACE.md, TEAM.md, TASK.md), or any team artifacts.",
    parameters: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "Space ID" },
        path: { type: "string", description: "File path within the space (e.g., 'SPACE.md', 'docs/prd.md')" },
      },
      required: ["space_id", "path"],
    },
    handler: async ({ space_id, path }) => {
      const data = await ctxFetch("GET", `/api/spaces/${space_id}/files/${path}`);
      return JSON.stringify({ file: { path: data.file.path, content: data.file.content, version: data.file.version, updatedAt: data.file.updatedAt } });
    },
  },

  {
    name: "context_write_file",
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
    handler: async ({ space_id, path, content, modified_by }) => {
      const data = await ctxFetch("PUT", `/api/spaces/${space_id}/files/${path}`, { content, modifiedBy: modified_by });
      return JSON.stringify({
        success: true,
        file: { path: data.file.path, version: data.file.version, size: data.file.size },
        url: `${CTX_BASE}/ctx/${space_id}/${path}`,
        message: `File written. Share this URL with other agents: ${CTX_BASE}/ctx/${space_id}/${path}`,
      });
    },
  },

  {
    name: "context_list_files",
    description: "List all files in the shared Context space. Use to see what documents, artifacts, and protocol files exist.",
    parameters: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "Space ID" },
        prefix: { type: "string", description: "Optional path prefix filter (e.g., 'docs/')" },
      },
      required: ["space_id"],
    },
    handler: async ({ space_id, prefix }) => {
      const q = prefix ? `?prefix=${encodeURIComponent(prefix)}` : "";
      const data = await ctxFetch("GET", `/api/spaces/${space_id}/files${q}`);
      return JSON.stringify({ files: data.files.map((f: any) => ({ path: f.path, size: f.size, version: f.version, updatedAt: f.updatedAt })) });
    },
  },

  {
    name: "context_delete_file",
    description: "Delete a file from the shared Context space.",
    parameters: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "Space ID" },
        path: { type: "string", description: "File path to delete" },
      },
      required: ["space_id", "path"],
    },
    handler: async ({ space_id, path }) => {
      await ctxFetch("DELETE", `/api/spaces/${space_id}/files/${path}`);
      return JSON.stringify({ success: true, message: `Deleted: ${path}` });
    },
  },

  {
    name: "context_get_protocol",
    description: "Get all three protocol files (SPACE.md, TEAM.md, TASK.md) at once. Use this to quickly understand the current collaboration state.",
    parameters: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "Space ID" },
      },
      required: ["space_id"],
    },
    handler: async ({ space_id }) => {
      const data = await ctxFetch("GET", `/api/spaces/${space_id}/protocol`);
      return JSON.stringify(data);
    },
  },

  {
    name: "context_update_task",
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
    handler: async ({ space_id, content, modified_by }) => {
      const data = await ctxFetch("PUT", `/api/spaces/${space_id}/files/TASK.md`, { content, modifiedBy: modified_by });
      return JSON.stringify({ success: true, version: data.file.version, message: "TASK.md updated." });
    },
  },

  {
    name: "context_add_member",
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
    handler: async ({ space_id, name, type, role, channel_user_id, capabilities }) => {
      const data = await ctxFetch("POST", `/api/spaces/${space_id}/members`, {
        name,
        type,
        role,
        channelUserId: channel_user_id,
        capabilities,
      });
      return JSON.stringify({ success: true, member: data.member });
    },
  },

  {
    name: "context_list_members",
    description: "List all members of the Context space (both humans and agents).",
    parameters: {
      type: "object",
      properties: {
        space_id: { type: "string", description: "Space ID" },
      },
      required: ["space_id"],
    },
    handler: async ({ space_id }) => {
      const data = await ctxFetch("GET", `/api/spaces/${space_id}/members`);
      return JSON.stringify({ members: data.members });
    },
  },
];
