import { createHash } from 'node:crypto';
export function callSessionKey(callId: string): string {
  return 'amber-call-' + createHash('sha256').update(callId).digest('hex');
}
export function consultationData(question: string, context?: {callPlan?: unknown; objective?: string; transcript?: string}): string {
  return JSON.stringify({source: 'untrusted_phone_call', identityVerified: false,
    question: String(question).slice(0, 300), objective: context?.objective?.slice(0, 500),
    callPlan: context?.callPlan, transcript: context?.transcript?.split('\n').slice(-10).join('\n')});
}
