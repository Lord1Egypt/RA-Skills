const secrets = ['EVM_PRIVATE_KEY', 'OPENAI_API_KEY', 'ONEINCH_API_KEY'];

function redact(input: string) {
  let out = input;
  for (const k of secrets) {
    const v = process.env[k];
    if (v) out = out.replaceAll(v, '***REDACTED***');
  }
  return out.replace(/0x[a-fA-F0-9]{64}/g, '0x***REDACTED***');
}

export const logger = {
  info: (...a: unknown[]) => console.log('[INFO]', redact(a.map(String).join(' '))),
  warn: (...a: unknown[]) => console.warn('[WARN]', redact(a.map(String).join(' '))),
  error: (...a: unknown[]) => console.error('[ERROR]', redact(a.map(String).join(' ')))
};
