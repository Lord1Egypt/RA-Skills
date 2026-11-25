import { createHash } from 'node:crypto';
export function callSessionKey(callId: string): string {
  return 'amber-call-' + createHash('sha256').update(callId).digest('hex');
}
export function consultationData(question: string, context?: {callPlan?: unknown; objective?: string; transcript?: string}): string {
  return JSON.stringify({source: 'untrusted_phone_call', identityVerified: false,
    question: String(question).slice(0, 300), objective: context?.objective?.slice(0, 500),
    callPlan: context?.callPlan, transcript: context?.transcript?.split('\n').slice(-10).join('\n')});
}

/** Keep the event type and numeric usage fields the dashboard reads. */
export function realtimeEventForLog(event: any): Record<string, unknown> {
  const type = typeof event?.type === 'string' && /^[a-z_.]{1,80}$/.test(event.type)
    ? event.type : 'unknown';
  const usage = type === 'response.done' ? event?.response?.usage
    : type === 'conversation.item.input_audio_transcription.completed' ? event?.usage
    : undefined;
  if (!usage || typeof usage !== 'object') return { type };

  const numericFields = (source: any, fields: string[]) => Object.fromEntries(
    fields.filter((key) => Number.isFinite(source?.[key]) && source[key] >= 0)
      .map((key) => [key, source[key]])
  );
  const counters = {
    ...numericFields(usage, ['total_tokens', 'input_tokens', 'output_tokens']),
    input_token_details: numericFields(usage.input_token_details, ['text_tokens', 'audio_tokens', 'cached_tokens']),
    output_token_details: numericFields(usage.output_token_details, ['text_tokens', 'audio_tokens']),
  };
  return type === 'response.done' ? { type, response: { usage: counters } } : { type, usage: counters };
}
