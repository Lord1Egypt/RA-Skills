/**
 * BountySwarm OpenClaw Skill Handler
 *
 * Bridges OpenClaw agent commands to the BountySwarm backend API.
 */

interface SkillContext {
  config: { backendUrl: string };
  log: (msg: string) => void;
}

interface CommandResult {
  success: boolean;
  data?: any;
  error?: string;
}

async function apiCall(
  ctx: SkillContext,
  method: string,
  path: string,
  body?: any
): Promise<any> {
  const url = `${ctx.config.backendUrl}${path}`;
  ctx.log(`→ ${method} ${url}`);

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });

  const json = await res.json();
  if (!res.ok) {
    throw new Error(json.error ?? `HTTP ${res.status}`);
  }
  return json;
}

// ─── Command Handlers ───────────────────────────────────────────────

export async function bountyCreate(
  ctx: SkillContext,
  params: {
    reward: number;
    deadline: number;
    description: string;
    metadataURI: string;
    maxSubmissions?: number;
  }
): Promise<CommandResult> {
  try {
    const data = await apiCall(ctx, "POST", "/api/bounty", params);
    ctx.log(`✅ Bounty #${data.bountyId} created (tx: ${data.txHash})`);
    return { success: true, data };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

export async function bountyList(ctx: SkillContext): Promise<CommandResult> {
  try {
    const data = await apiCall(ctx, "GET", "/api/bounties");
    ctx.log(`📋 Found ${data.total} open bounties`);
    return { success: true, data };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

export async function bountySubmit(
  ctx: SkillContext,
  params: {
    bountyId: number;
    resultHash: string;
    resultURI: string;
  }
): Promise<CommandResult> {
  try {
    const data = await apiCall(ctx, "POST", "/api/submit", params);
    ctx.log(`✅ Solution submitted to bounty #${params.bountyId} (tx: ${data.txHash})`);
    return { success: true, data };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

export async function bountyPick(
  ctx: SkillContext,
  params: {
    bountyId: number;
    winner: string;
  }
): Promise<CommandResult> {
  try {
    const data = await apiCall(ctx, "POST", "/api/pick-winner", params);
    ctx.log(`🏆 Winner selected for bounty #${params.bountyId}: ${params.winner} (tx: ${data.txHash})`);
    return { success: true, data };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

export async function bountySubcontract(
  ctx: SkillContext,
  params: {
    bountyId: number;
    subAgent: string;
    feePercent: number;
    subtaskURI: string;
  }
): Promise<CommandResult> {
  try {
    const data = await apiCall(ctx, "POST", "/api/subcontract", params);
    ctx.log(
      `🤝 Delegation #${data.delegationId} created → ${params.subAgent} (${params.feePercent / 100}% fee, tx: ${data.txHash})`
    );
    return { success: true, data };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

// ─── Router ─────────────────────────────────────────────────────────

export async function handleCommand(
  ctx: SkillContext,
  command: string,
  params: any
): Promise<CommandResult> {
  switch (command) {
    case "bounty:create":
      return bountyCreate(ctx, params);
    case "bounty:list":
      return bountyList(ctx);
    case "bounty:submit":
      return bountySubmit(ctx, params);
    case "bounty:pick":
      return bountyPick(ctx, params);
    case "bounty:subcontract":
      return bountySubcontract(ctx, params);
    default:
      return { success: false, error: `Unknown command: ${command}` };
  }
}
