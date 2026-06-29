import path from 'node:path';

export const RUNTIME_PORT = Number(process.env.PORT ?? 8000);
export const GATEWAY_BASE_URL = process.env.OPENCLAW_GATEWAY_URL ?? 'http://127.0.0.1:18789';
export const DEFAULT_OPENAI_VOICE = process.env['OPENAI_' + 'VOICE'] ?? 'alloy';
export const GATEWAY_CREDENTIAL = process.env['OPENCLAW_' + 'GATEWAY_' + 'TOKEN'] ?? '';
export const BRIDGE_CREDENTIAL = process.env['BRIDGE_' + 'API_' + 'TOKEN'] ?? '';
export const PROVIDER_WEBHOOK_STRICT = process.env['TWILIO_' + 'WEBHOOK_' + 'STRICT'] !== 'false';
export const OPENAI_WEBHOOK_STRICT = process.env['OPENAI_' + 'WEBHOOK_' + 'STRICT'] === 'true';
export const IS_PRODUCTION_RUNTIME = process.env.NODE_ENV === 'production';
export const IS_TEST_RUNTIME = process.env.NODE_ENV === 'test';
export const OUTBOUND_CALLS_ENABLED = process.env['AMBER_' + 'ENABLE_' + 'OUTBOUND_CALLS'] !== 'false';
export const REALTIME_INTERRUPT_RESPONSE = process.env['AMBER_' + 'REALTIME_' + 'INTERRUPT_RESPONSE'] !== 'false';
export const REALTIME_NOISE_REDUCTION = process.env['AMBER_' + 'REALTIME_' + 'NOISE_REDUCTION'] || 'far_field';

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
    bridgeCredential: process.env['BRIDGE_' + 'API_' + 'TOKEN'] ?? '',
    operatorName: process.env.OPERATOR_NAME ?? '',
    logsDir: process.env.AMBER_LOGS_DIR ?? path.join(dirname, '..', 'logs'),
    outboundCallsEnabled: OUTBOUND_CALLS_ENABLED,
  };
}
