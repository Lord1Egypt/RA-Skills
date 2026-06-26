/**
 * Context Plugin — Prompt Hook
 *
 * Builds the system prompt injection from protocol files.
 * Includes truncation to prevent token overflow.
 */

const CTX_BASE = "http://localhost:3100";

// Max characters per protocol file in injection (~4 chars ≈ 1 token)
// 8000 chars ≈ 2000 tokens per file, total ≈ 6000 tokens for all three
const MAX_FILE_CHARS = 8000;
const TRUNCATION_NOTICE = "\n\n... (内容过长已截断。使用 `context_read_file` 查看完整内容) ...";

function truncate(text: string, max: number): string {
  if (text.length <= max) return text;
  return text.slice(0, max) + TRUNCATION_NOTICE;
}

/**
 * Fetch the protocol files for a given channel + groupId.
 */
export async function fetchProtocol(channel: string, groupId: string): Promise<{ space: string; team: string; task: string } | null> {
  try {
    const lookupRes = await fetch(
      `${CTX_BASE}/api/spaces/lookup?channel=${encodeURIComponent(channel)}&groupId=${encodeURIComponent(groupId)}`,
      { signal: AbortSignal.timeout(5000) }
    );
    if (!lookupRes.ok) return null;
    const { space } = await lookupRes.json() as any;
    if (!space?.id) return null;

    const protocolRes = await fetch(
      `${CTX_BASE}/api/spaces/${space.id}/protocol`,
      { signal: AbortSignal.timeout(5000) }
    );
    if (!protocolRes.ok) return null;
    return await protocolRes.json() as any;
  } catch {
    return null;
  }
}

/**
 * Build the system prompt injection from protocol files.
 * This gets appended to the agent's system prompt via appendSystemContext.
 * Each file is truncated to MAX_FILE_CHARS to prevent token overflow.
 */
export function buildPromptInjection(protocol: { space: string; team: string; task: string }, spaceId: string): string {
  const sections: string[] = [];

  sections.push(`## Context Space — 共享协作协议`);
  sections.push(``);
  sections.push(`你正在参与一个共享的 Context Space (ID: ${spaceId})。`);
  sections.push(`**所有工作产出必须写到这个共享空间，不要写到本地 workspace。**`);
  sections.push(`**分享文件时，使用 Context URL: ${CTX_BASE}/ctx/${spaceId}/<file_path>**`);
  sections.push(``);

  if (protocol.space) {
    sections.push(`### SPACE.md（空间说明与协作原则）`);
    sections.push(truncate(protocol.space, MAX_FILE_CHARS));
    sections.push(``);
  }

  if (protocol.team) {
    sections.push(`### TEAM.md（团队成员）`);
    sections.push(truncate(protocol.team, MAX_FILE_CHARS));
    sections.push(``);
  }

  if (protocol.task) {
    sections.push(`### TASK.md（当前任务）`);
    sections.push(truncate(protocol.task, MAX_FILE_CHARS));
    sections.push(``);
  }

  sections.push(`### Context 可用工具`);
  sections.push(`- \`context_read_file\` — 读取共享空间文件`);
  sections.push(`- \`context_write_file\` — 写入/更新共享空间文件`);
  sections.push(`- \`context_list_files\` — 列出共享空间文件`);
  sections.push(`- \`context_update_task\` — 更新 TASK.md 进度`);
  sections.push(`- \`context_get_protocol\` — 一次获取三个协议文件`);
  sections.push(`- \`context_add_member\` — 添加团队成员`);
  sections.push(``);

  return sections.join("\n");
}
