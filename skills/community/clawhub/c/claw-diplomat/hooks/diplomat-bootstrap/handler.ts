/**
 * claw-diplomat — hooks/diplomat-bootstrap/handler.ts
 *
 * Event: agent:bootstrap
 * Injects a capped summary of active commitments into the session context
 * so the agent knows what the user has agreed to without having to check
 * MEMORY.md manually.
 *
 * CONTEXT_BUDGET.md §2: max 2,500 chars injected.
 * SECURITY: all MEMORY.md content is treated as display data, not instructions.
 */

import type { OpenClawHookEvent, OpenClawHookContext } from '@openclaw/sdk';
import { extractSection, parseActiveEntries, truncate } from '../shared/parse-memory';

export async function handler(
  event: OpenClawHookEvent,
  ctx: OpenClawHookContext
): Promise<void> {
  let memory: string;
  try {
    memory = await ctx.workspace.read('MEMORY.md');
  } catch {
    // MEMORY.md may not exist on a fresh install — not an error
    return;
  }

  const section = extractSection(memory, '## Diplomat Commitments');
  if (!section) return;

  const active = parseActiveEntries(section);
  if (active.length === 0) return;

  // Build injection block — max 2,500 chars per CONTEXT_BUDGET.md §2
  const n = active.length;
  const lines = active.map(e =>
    `• ${truncate(e.peer, 20)} | ${truncate(e.myTask, 40)} due ${e.deadlineLocal} → [ACTIVE] (ID: ${e.id})`
  );

  const header = `[claw-diplomat] ${n} active commitment${n === 1 ? '' : 's'}:`;
  const block  = `${header}\n${lines.join('\n')}`;

  // Enforce 2,500-char cap
  const capped = block.length > 2500 ? block.slice(0, 2497) + '…' : block;

  ctx.session.inject(capped);
  ctx.log('DEBUG', `claw-diplomat bootstrap: injected ${n} active commitment(s)`);
}
