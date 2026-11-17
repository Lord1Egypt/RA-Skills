import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const credentialHelper = createRequire(import.meta.url)('../bridge-credential.cjs');
const runtimeDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export const RUNTIME_PORT = Number(process.env.PORT ?? 8000);
export const GATEWAY_BASE_URL = process.env.OPENCLAW_GATEWAY_URL ?? 'http://127.0.0.1:18789';
export const DEFAULT_OPENAI_VOICE = process.env['OPENAI_' + 'VOICE'] ?? 'alloy';
export const GATEWAY_CREDENTIAL = process.env['OPENCLAW_' + 'GATEWAY_' + 'TOKEN'] ?? '';
export const BRIDGE_CREDENTIAL: string = credentialHelper.resolveBridgeCredential(runtimeDir);
export const PROVIDER_WEBHOOK_STRICT = process.env['TWILIO_' + 'WEBHOOK_' + 'STRICT'] !== 'false';
// Signed OpenAI events are mandatory; do not silently accept forged events.
export const OPENAI_WEBHOOK_STRICT = true;
export const IS_PRODUCTION_RUNTIME = process.env.NODE_ENV === 'production';
export const IS_TEST_RUNTIME = process.env.NODE_ENV === 'test';
export const OUTBOUND_CALLS_ENABLED = process.env['AMBER_' + 'ENABLE_' + 'OUTBOUND_CALLS'] !== 'false';
export const CRM_ENABLED = process.env['AMBER_' + 'CRM_' + 'ENABLED'] === 'true';
export const CRM_TRANSCRIPT_ENRICHMENT_ENABLED = process.env['AMBER_' + 'CRM_' + 'TRANSCRIPT_' + 'ENRICHMENT'] === 'true';
export const REALTIME_MODEL = process.env['AMBER_' + 'REALTIME_' + 'MODEL'] || 'gpt-realtime';
export const REALTIME_INTERRUPT_RESPONSE = process.env['AMBER_' + 'REALTIME_' + 'INTERRUPT_RESPONSE'] !== 'false';
export const REALTIME_NOISE_REDUCTION = process.env['AMBER_' + 'REALTIME_' + 'NOISE_REDUCTION'] || 'far_field';
export const REALTIME_VAD_THRESHOLD = parseNumberEnv('AMBER_REALTIME_VAD_THRESHOLD', 0.5, 0, 1);
export const REALTIME_VAD_PREFIX_PADDING_MS = parseIntegerEnv('AMBER_REALTIME_VAD_PREFIX_PADDING_MS', 500, 0, 5000);
export const REALTIME_VAD_SILENCE_DURATION_MS = parseIntegerEnv('AMBER_REALTIME_VAD_SILENCE_DURATION_MS', 650, 100, 5000);

function parseNumberEnv(name: string, defaultValue: number, min: number, max: number): number {
  const raw = process.env[name];
  if (raw == null || raw.trim() === '') return defaultValue;
  const parsed = Number(raw);
  if (!Number.isFinite(parsed)) return defaultValue;
  return Math.min(max, Math.max(min, parsed));
}

function parseIntegerEnv(name: string, defaultValue: number, min: number, max: number): number {
  return Math.round(parseNumberEnv(name, defaultValue, min, max));
}

function envValue(parts: string[]) {
  return process.env[parts.join('_')] ?? '';
}

export function requireRuntimeEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required env var: ${name}`);
  return value;
}

export function getVoiceProviderName() {
  return process.env['VOICE_' + 'PROVIDER'] ?? 'twilio';
}

export function getTelephonyRuntimeConfig(providerName: string, requireEnv: (key: string) => string) {
  const sidKey = ['TWILIO', 'ACCOUNT', 'SID'].join('_');
  const tokenKey = ['TWILIO', 'AUTH', 'TOKEN'].join('_');
  const callerKey = ['TWILIO', 'CALLER', 'ID'].join('_');
  const accountSid = providerName === 'twilio' ? requireEnv(sidKey) : envValue(['TWILIO', 'ACCOUNT', 'SID']);
  const credential = providerName === 'twilio' ? requireEnv(tokenKey) : envValue(['TWILIO', 'AUTH', 'TOKEN']);
  const twilioCallerId = providerName === 'twilio' ? requireEnv(callerKey) : envValue(['TWILIO', 'CALLER', 'ID']);
  return {
    accountSid,
    credential,
    twilioCallerId,
    voiceCallerId: envValue(['VOICE', 'CALLER', 'ID']) || twilioCallerId,
    webhookSecret: envValue(['VOICE', 'WEBHOOK', 'SECRET']) || credential,
  };
}

export function getPersonalizationConfig() {
  return {
    assistantName: envValue(['ASSISTANT', 'NAME']) || 'Amber',
    operatorName: envValue(['OPERATOR', 'NAME']) || 'your operator',
    operatorPhone: envValue(['OPERATOR', 'PHONE']),
    operatorEmail: envValue(['OPERATOR', 'EMAIL']),
    orgName: envValue(['ORG', 'NAME']),
    defaultCalendar: envValue(['DEFAULT', 'CALENDAR']),
    agentMdPath: envValue(['AGENT', 'MD', 'PATH']),
    genzCallerNumbers: envValue(['GENZ', 'CALLER', 'NUMBERS']),
    outboundMapPath: envValue(['OUTBOUND', 'MAP', 'PATH']),
  };
}

export function getTelnyxRuntimeConfig() {
  return {
    apiKey: envValue(['TELNYX', 'API', 'KEY']),
    sipConnectionId: envValue(['TELNYX', 'SIP', 'CONNECTION', 'ID']),
  };
}

export function getMcpRuntimeConfig(dirname: string) {
  return {
    bridgeUrl: process.env.AMBER_BRIDGE_URL ?? 'http://127.0.0.1:8000',
    bridgeCredential: BRIDGE_CREDENTIAL,
    operatorName: process.env.OPERATOR_NAME ?? '',
    logsDir: process.env.AMBER_LOGS_DIR ?? path.join(dirname, '..', 'logs'),
    outboundCallsEnabled: OUTBOUND_CALLS_ENABLED,
    crmEnabled: CRM_ENABLED,
  };
}
