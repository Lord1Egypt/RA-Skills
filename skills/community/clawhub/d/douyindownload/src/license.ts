// 授权管理：免费额度、激活码验证、用量统计
import { PRICING, UPGRADE_MESSAGES, PURCHASE_URL } from './config';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import mysql from 'mysql2/promise';

// 简单的本地存储（生产环境建议用数据库）
interface UsageRecord {
  deviceId: string;
  count: number;
  lastReset: string;  // ISO date
  plan: 'free' | 'basic' | 'pro';
  keyData?: {
    key: string;
    expiresAt: string;
  };
}

interface LicenseState {
  [deviceId: string]: UsageRecord;
}

const STATE_FILE = path.join(os.homedir(), '.douyindownloadmcp', 'state.json');

function loadState(): LicenseState {
  try {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
    }
  } catch {}
  return {};
}

function saveState(state: LicenseState): void {
  try {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (error) {
    console.error('Failed to save state:', error);
  }
}

// 支付系统数据库连接配置
const PAYMENT_DB = {
  host: '49.234.177.66',
  port: 3306,
  user: 'root',
  password: 'M3JsLraQ',
  database: 'douyin_payment',
};

// 硬编码的激活码（仅作为备用，线上激活码走数据库）
const VALID_KEYS: Record<string, { plan: 'basic' | 'pro'; expiresAt: string }> = {
  'DEMO-BASIC-2026': { plan: 'basic', expiresAt: '2027-01-01' },
  'DEMO-PRO-2026': { plan: 'pro', expiresAt: '2027-01-01' },
};

export interface CheckResult {
  allowed: boolean;
  reason?: string;
  upgradeMessage?: string;
  remaining: number | '∞';
  plan: string;
  isPaid: boolean;
}

function getOrCreateRecord(deviceId: string): UsageRecord {
  const state = loadState();
  if (!state[deviceId]) {
    state[deviceId] = {
      deviceId,
      count: 0,
      lastReset: new Date().toISOString(),
      plan: 'free',
    };
    saveState(state);
  }
  return state[deviceId];
}

function resetMonthly(record: UsageRecord): void {
  const now = new Date();
  const lastReset = new Date(record.lastReset);
  if (now.getMonth() !== lastReset.getMonth() || now.getFullYear() !== lastReset.getFullYear()) {
    record.count = 0;
    record.lastReset = now.toISOString();
  }
}

// 验证激活码
export async function activateKey(deviceId: string, key: string): Promise<CheckResult> {
  const state = loadState();
  const record = getOrCreateRecord(deviceId);
  const keyStr = key.trim().toUpperCase();

  // 先尝试从支付系统数据库校验
  try {
    const db = await mysql.createConnection(PAYMENT_DB);
    try {
      const [rows] = await db.execute<any[]>(
        'SELECT plan, status, used_device FROM activation_codes WHERE code = ? LIMIT 1',
        [keyStr]
      );

      if (rows.length > 0) {
        const codeRow = rows[0];

        if (codeRow.status === 'activated') {
          return {
            allowed: true,
            reason: UPGRADE_MESSAGES.invalidKey(),
            remaining: PRICING.free.quota - record.count,
            plan: '免费版',
            isPaid: false,
          };
        }

        if (codeRow.status === 'expired') {
          return {
            allowed: true,
            reason: UPGRADE_MESSAGES.expiredKey(),
            remaining: PRICING.free.quota - record.count,
            plan: '免费版',
            isPaid: false,
          };
        }

        // 标记为已使用
        await db.execute(
          'UPDATE activation_codes SET status="activated", used_at=NOW(), used_device=? WHERE code=?',
          [deviceId, keyStr]
        );

        // 激活成功
        record.plan = codeRow.plan;
        record.keyData = { key: keyStr, expiresAt: '2099-12-31' };
        state[deviceId] = record;
        saveState(state);

        return {
          allowed: true,
          reason: UPGRADE_MESSAGES.success(Infinity, codeRow.plan === 'pro' ? 'Pro版' : '基础版'),
          remaining: Infinity,
          plan: codeRow.plan === 'pro' ? 'Pro版' : '基础版',
          isPaid: true,
        };
      }
    } finally {
      await db.end();
    }
  } catch (err) {
    console.error('[activateKey] 数据库验证失败:', (err as Error).message);
  }

  // 数据库找不到，回退到本地硬编码激活码
  const keyInfo = VALID_KEYS[keyStr];
  if (!keyInfo) {
    return {
      allowed: true,
      reason: UPGRADE_MESSAGES.invalidKey() + '\n\n👉 ' + PURCHASE_URL,
      remaining: PRICING.free.quota - record.count,
      plan: '免费版',
      isPaid: false,
    };
  }

  const expiresAt = new Date(keyInfo.expiresAt);
  if (expiresAt < new Date()) {
    return {
      allowed: true,
      reason: UPGRADE_MESSAGES.expiredKey(),
      remaining: PRICING.free.quota - record.count,
      plan: '免费版',
      isPaid: false,
    };
  }

  record.plan = keyInfo.plan;
  record.keyData = { key: keyStr, expiresAt: keyInfo.expiresAt };
  state[deviceId] = record;
  saveState(state);

  return {
    allowed: true,
    reason: UPGRADE_MESSAGES.success(Infinity, keyInfo.plan === 'pro' ? 'Pro版' : '基础版'),
    remaining: Infinity,
    plan: keyInfo.plan === 'pro' ? 'Pro版' : '基础版',
    isPaid: true,
  };
}

// 验证设备ID（简易设备指纹）
function getDeviceId(): string {
  return os.hostname() + '-' + os.platform() + '-' + os.arch();
}

// 每次调用检查
export function checkAndRecord(deviceId?: string): CheckResult {
  const did = deviceId || getDeviceId();
  const state = loadState();
  const record = getOrCreateRecord(did);

  resetMonthly(record);

  if (record.plan === 'pro') {
    return {
      allowed: true,
      remaining: Infinity,
      plan: 'Pro版',
      isPaid: true,
    };
  }

  if (record.plan === 'basic') {
    const basicLimit = PRICING.basic.quota;
    if (record.count >= basicLimit) {
      return {
        allowed: false,
        upgradeMessage: UPGRADE_MESSAGES.quotaExceeded(0, basicLimit),
        remaining: 0,
        plan: '基础版',
        isPaid: true,
      };
    }
    record.count++;
    state[did] = record;
    saveState(state);
    return {
      allowed: true,
      remaining: basicLimit - record.count,
      plan: '基础版',
      isPaid: true,
    };
  }

  // 免费版
  const freeLimit = PRICING.free.quota;
  if (record.count >= freeLimit) {
    return {
      allowed: false,
      upgradeMessage: UPGRADE_MESSAGES.quotaExceeded(freeLimit - record.count, freeLimit),
      remaining: Math.max(0, freeLimit - record.count),
      plan: '免费版',
      isPaid: false,
    };
  }

  record.count++;
  state[did] = record;
  saveState(state);

  return {
    allowed: true,
    remaining: freeLimit - record.count,
    plan: '免费版',
    isPaid: false,
  };
}

// 查询状态
export function getStatus(deviceId?: string): CheckResult {
  const did = deviceId || getDeviceId();
  const record = getOrCreateRecord(did);
  resetMonthly(record);

  let remaining: number | '∞';
  if (record.plan === 'pro') {
    remaining = Infinity;
  } else if (record.plan === 'basic') {
    remaining = Math.max(0, PRICING.basic.quota - record.count);
  } else {
    remaining = Math.max(0, PRICING.free.quota - record.count);
  }

  return {
    allowed: true,
    remaining,
    plan: record.plan === 'pro' ? 'Pro版' : record.plan === 'basic' ? '基础版' : '免费版',
    isPaid: record.plan !== 'free',
  };
}

// 重置用量（调试用）
export function resetUsage(deviceId?: string): void {
  const did = deviceId || getDeviceId();
  const state = loadState();
  if (state[did]) {
    state[did].count = 0;
    state[did].lastReset = new Date().toISOString();
    saveState(state);
  }
}