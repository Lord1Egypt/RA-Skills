import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { z } from 'zod';
import { NEUTARO_CONFIG } from './config.js';

const defaultAllowlistPath = path.join(os.homedir(), '.clawpurse', 'allowlist.json');

const DestinationSchema = z.object({
  name: z.string().optional(),
  address: z.string(),
  maxAmount: z.number().nonnegative().optional(),
  needsMemo: z.boolean().optional(),
  notes: z.string().optional(),
});

const PolicySchema = z.object({
  maxAmount: z.number().nonnegative().nullable().optional(),
  requireMemo: z.boolean().optional(),
  blockUnknown: z.boolean().optional(),
});

const AllowlistSchema = z.object({
  defaultPolicy: PolicySchema.optional(),
  destinations: DestinationSchema.array().default([]),
});

export type AllowlistConfig = z.infer<typeof AllowlistSchema>;
export type AllowlistDestination = z.infer<typeof DestinationSchema>;

export async function loadAllowlist(configPath?: string): Promise<AllowlistConfig | null> {
  const filePath = configPath || defaultAllowlistPath;
  try {
    const data = await fs.readFile(filePath, 'utf8');
    return AllowlistSchema.parse(JSON.parse(data));
  } catch (error: any) {
    if (error?.code === 'ENOENT') {
      return null;
    }
    throw new Error(`Failed to parse allowlist: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export async function saveAllowlist(config: AllowlistConfig, configPath?: string): Promise<string> {
  const filePath = configPath || defaultAllowlistPath;
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(config, null, 2), { mode: 0o600 });
  return filePath;
}

export async function allowlistExists(configPath?: string): Promise<boolean> {
  const filePath = configPath || defaultAllowlistPath;
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

function amountToMicro(amount: number): bigint {
  return BigInt(Math.round(amount * 10 ** NEUTARO_CONFIG.decimals));
}

export interface AllowlistCheckResult {
  allowed: boolean;
  requireMemo?: boolean;
  reason?: string;
  destination?: AllowlistDestination;
}

export function evaluateAllowlist(
  config: AllowlistConfig,
  toAddress: string,
  amountMicro: bigint,
  memo?: string
): AllowlistCheckResult {
  const normalizedAddress = toAddress.trim();
  const entry = config.destinations.find((d) => d.address === normalizedAddress);

  if (entry) {
    if (entry.maxAmount !== undefined) {
      const limitMicro = amountToMicro(entry.maxAmount);
      if (amountMicro > limitMicro) {
        return {
          allowed: false,
          reason: `Amount exceeds ${entry.maxAmount} ${NEUTARO_CONFIG.displayDenom} cap for ${entry.name || entry.address}`,
        };
      }
    }

    if (entry.needsMemo && !memo) {
      return {
        allowed: false,
        reason: `Destination ${entry.name || entry.address} requires a memo`,
      };
    }

    return {
      allowed: true,
      requireMemo: entry.needsMemo,
      destination: entry,
    };
  }
  
  // Not in allowlist
  const policy = config.defaultPolicy;

  if (!policy) {
    return { allowed: true };
  }

  if (policy.blockUnknown) {
    return {
      allowed: false,
      reason: 'Destination is not in allowlist (blockUnknown=true)',
    };
  }

  if (policy.maxAmount !== undefined && policy.maxAmount !== null) {
    const limitMicro = amountToMicro(policy.maxAmount);
    if (amountMicro > limitMicro) {
      return {
        allowed: false,
        reason: `Amount exceeds defaultPolicy maxAmount (${policy.maxAmount} ${NEUTARO_CONFIG.displayDenom})`,
      };
    }
  }

  if (policy.requireMemo && !memo) {
    return {
      allowed: false,
      reason: 'Default policy requires memo for unknown destinations',
    };
  }

  return { allowed: true, requireMemo: policy.requireMemo };
}

export function getAllowlistPath(): string {
  return defaultAllowlistPath;
}
