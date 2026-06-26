/**
 * Agent Team Plugin for OpenClaw
 *
 * Injects team member information into the system context before prompt build.
 * This ensures AI agents always have access to team information without needing
 * to explicitly invoke tools.
 */

import { readFileSync, existsSync } from "fs";
import { homedir } from "os";
import { join } from "path";

interface TeamMember {
  agent_id: string;
  name: string;
  role: string;
  is_leader: boolean;
  enabled: boolean;
  tags: string[];
  expertise: string[];
  not_good_at: string[];
  load_workflow?: boolean;
  group?: string;
}

interface TeamData {
  team: Record<string, TeamMember>;
}

interface PluginConfig {
  dataFile?: string;
  enabled?: boolean;
}

interface PluginHookAgentContext {
  agentId?: string;
  sessionKey?: string;
  sessionId?: string;
  workspaceDir?: string;
  messageProvider?: string;
  trigger?: string;
  channelId?: string;
}

interface PluginHookBeforePromptBuildEvent {
  prompt: string;
  messages: unknown[];
}

interface PluginHookBeforePromptBuildResult {
  prependContext?: string;
  systemPrompt?: string;
  prependSystemContext?: string;
  appendSystemContext?: string;
}

interface PluginApi {
  config: PluginConfig;
  on: (
    event: "before_prompt_build",
    handler: (
      event: PluginHookBeforePromptBuildEvent, 
      ctx: PluginHookAgentContext
    ) => PluginHookBeforePromptBuildResult | void,
    options?: { priority?: number }
  ) => void;
  registerCommand: (command: {
    name: string;
    description?: string;
    acceptsArgs?: boolean;
    requireAuth?: boolean;
    handler: (ctx: {
      senderId?: string;
      channel?: string;
      isAuthorizedSender?: boolean;
      args?: string;
      commandBody?: string;
      config?: unknown;
    }) => { text: string } | Promise<{ text: string }>;
  }) => void;
}

// Default data file path
const DEFAULT_DATA_FILE = join(homedir(), ".agent-team", "team.json");

/**
 * Load team data from JSON file
 */
function loadTeamData(dataFilePath: string): TeamData | null {
  try {
    if (!existsSync(dataFilePath)) {
      return null;
    }
    const content = readFileSync(dataFilePath, "utf-8");
    const data = JSON.parse(content) as TeamData;
    if (!data || typeof data !== "object" || !data.team) {
      return null;
    }
    return data;
  } catch (error) {
    console.error(`[agent-team] Error loading team data: ${error}`);
    return null;
  }
}

/**
 * Format a single team member as markdown line
 * @param member Team member to format
 * @param options Formatting options
 */
function formatMember(member: TeamMember, options: { compact?: boolean } = {}): string[] {
  const { compact = false } = options;
  const tagsStr = compact ? member.tags.join(",") : member.tags.join(", ");
  const expertiseStr = member.expertise.join(compact ? "," : ", ");
  const notGoodAtStr = member.not_good_at.join(compact ? "," : ", ");

  const lines: string[] = [];

  if (member.is_leader) {
    if (compact) {
      lines.push(`**${member.name}** ⭐ ${member.role} - ${tagsStr}`);
    } else {
      lines.push(`**${member.name}** ⭐ ${member.role} (Leader)`);
    }
  } else {
    if (compact) {
      lines.push(`**${member.name}** - ${member.role} - ${tagsStr}`);
    } else {
      lines.push(`**${member.name}** - ${member.role}`);
    }
  }

  if (compact) {
    lines.push(`- agent_id: ${member.agent_id}`);
  } else {
    lines.push(`- agent_id: \`${member.agent_id}\``);
  }

  if (tagsStr && !compact) {
    lines.push(`- tags: ${tagsStr}`);
  }

  if (expertiseStr) {
    lines.push(`- expertise: ${expertiseStr}`);
  }

  if (notGoodAtStr) {
    lines.push(`- not_good_at: ${notGoodAtStr}`);
  }

  // Show load_workflow if set
  if (member.load_workflow !== undefined) {
    lines.push(`- load_workflow: ${member.load_workflow}`);
  }

  return lines;
}

/**
 * Format team data as markdown for system context
 * @param teamData Team data from JSON file
 * @param currentAgentId The agent ID of the current session (used to determine leader role)
 */
function formatTeamContext(teamData: TeamData, currentAgentId: string): string {
  const members = Object.values(teamData.team).filter((m) => m.enabled !== false);

  if (members.length === 0) {
    return "";
  }

  const leader = members.find((m) => m.is_leader);
  const isCurrentAgentLeader = leader?.agent_id === currentAgentId;

  const lines: string[] = [
    "",
    "<agent_team>",
    "## Team Members",
    "",
  ];

  // Group members by 'group' field
  const grouped: Record<string, TeamMember[]> = {};
  for (const member of members) {
    const groupKey = member.group ?? "";
    if (!grouped[groupKey]) {
      grouped[groupKey] = [];
    }
    grouped[groupKey].push(member);
  }

  // Display grouped members (ungrouped first, then grouped)
  const ungrouped = grouped[""] || [];
  const groupedKeys = Object.keys(grouped).filter((k) => k !== "").sort();

  // Ungrouped members
  for (const member of ungrouped) {
    lines.push(...formatMember(member, { compact: true }));
    lines.push("");
  }

  // Grouped members
  for (const groupKey of groupedKeys) {
    lines.push(`### Group: ${groupKey}`);
    lines.push("");
    for (const member of grouped[groupKey]) {
      lines.push(...formatMember(member, { compact: true }));
      lines.push("");
    }
  }

  // Task Delegation Rules - always show after Team Members
  lines.push("### ⚡ Task Delegation Rules (Core Principle)");
  lines.push("");
  lines.push("**Delegation Timing:**");
  lines.push("1. First complete prep work: understand requirements, clarify goals, confirm constraints");
  lines.push("2. When entering implementation: identify the best person for execution, delegate to them");
  lines.push("3. Follow up after delegation: check output quality, ensure requirements are met");
  lines.push("");
  lines.push("**Delegation Context (what to pass):**");
  lines.push("When delegating, always provide:");
  lines.push("- Original requirements and success criteria");
  lines.push("- Relevant background and context");
  lines.push("- Your execution plan and any constraints");
  lines.push("- Expected output format");
  lines.push("");
  lines.push("**Delegation Failover:**");
  lines.push("If teammate fails to complete:");
  lines.push("1. First attempt: Send back with specific feedback for revision");
  lines.push("2. Second attempt: Reassign to another teammate with adjusted context");
  lines.push("3. Third attempt: Escalate to leader OR execute yourself");
  lines.push("");

  // Add PDCA workflow if load_workflow is true (default true for leader)
  const shouldLoadWorkflow = leader?.load_workflow ?? true;
  if (shouldLoadWorkflow) {
    lines.push("## 🔄 Task Processing Flow (Highest Priority)");
    lines.push("");
    lines.push("**Plan → Do → Check → Act**");
    lines.push("");
    lines.push("**IMPORTANT: This is a continuous improvement cycle. If task is incomplete in Act phase, loop back to Plan.**");
    lines.push("");
    lines.push("### 1. Plan — Planning Phase");
    lines.push("");
    lines.push("**Goal: Prepare thoroughly, avoid blind execution**");
    lines.push("");
    lines.push("- Understand requirements and clarify questions");
    lines.push("- Define goals and success criteria");
    lines.push("- Identify risks and determine ownership");
    lines.push("- Create execution plan");
    lines.push("");
    lines.push("### 2. Do — Execution Phase");
    lines.push("");
    lines.push("**Goal: Execute the plan while maintaining progress**");
    lines.push("");
    lines.push("- Execute or delegate based on ownership");
    lines.push("- Track progress and key decisions");
    lines.push("");
    lines.push("### 3. Check — Checking Phase");
    lines.push("");
    lines.push("**Goal: Verify results against requirements**");
    lines.push("");
    lines.push("- Verify completeness and quality");
    lines.push("- Check compliance with standards");
    lines.push("");
    lines.push("### 4. Act — Acting Phase");
    lines.push("");
    lines.push("**Goal: Summarize and decide next steps**");
    lines.push("");
    lines.push("- ✅ Task complete → End");
    lines.push("- ❌ Task incomplete → Loop back to Plan");
    lines.push("");
  }

  lines.push("</agent_team>");

  return lines.join("\n");
}

/**
 * Plugin register function
 */
export default function register(api: PluginApi): void {
  const config = api.config || {};

  // Skip if disabled
  if (config.enabled === false) {
    console.log("[agent-team] Plugin is disabled");
    return;
  }

  // Register /agent-team command
  api.registerCommand({
    name: "agent-team",
    description: "Show current team members",
    handler: (ctx) => {
      const dataFile = config.dataFile || DEFAULT_DATA_FILE;
      const teamData = loadTeamData(dataFile);

      if (!teamData) {
        return { text: `No team data found at ${dataFile}` };
      }

      // Use senderId to determine what would be injected
      const senderId = ctx.senderId || "main";
      const text = formatTeamContext(teamData, senderId);
      return { text };
    },
  });

  // Register before_prompt_build hook
  api.on(
    "before_prompt_build",
    (_event: PluginHookBeforePromptBuildEvent, ctx: PluginHookAgentContext) => {
      const dataFile = config.dataFile || DEFAULT_DATA_FILE;
      const teamData = loadTeamData(dataFile);

      if (!teamData) {
        console.log(`[agent-team] No team data found at ${dataFile}`);
        return {};
      }

      const members = Object.values(teamData.team).filter((m) => m.enabled !== false);
      if (members.length === 0) {
        console.log("[agent-team] No enabled team members");
        return {};
      }

      // Get current agent ID from context, default to "main"
      const currentAgentId = ctx.agentId || "main";
      const leader = members.find((m) => m.is_leader);
      const isCurrentAgentLeader = leader?.agent_id === currentAgentId;

      // Only inject team context for leader
      if (!isCurrentAgentLeader) {
        console.log(`[agent-team] Agent "${currentAgentId}" is not leader, skipping team context injection`);
        return {};
      }

      const context = formatTeamContext(teamData, currentAgentId);
      console.log(`[agent-team] Injecting team context for leader "${currentAgentId}" (${members.length} members)`);

      return {
        appendSystemContext: context,
      };
    },
    { priority: 10 }
  );
}
