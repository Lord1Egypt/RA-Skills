import crypto from 'node:crypto';

/** Standard Webhooks format used by OpenAI: sign id.timestamp.rawBody.
 * Reference: openai-node src/lib/webhook-signature.ts. Never accept legacy unsigned events.
 */
export function verifyOpenAIWebhook(body: Buffer, headers: Record<string, unknown>, secret: string, now = Date.now()): boolean {
  const id = headers['webhook-id'];
  const timestamp = headers['webhook-timestamp'];
  const signatures = headers['webhook-signature'];
  if (!secret || typeof id !== 'string' || !id || typeof timestamp !== 'string' ||
      !/^\d+$/.test(timestamp) || typeof signatures !== 'string') return false;
  if (Math.abs(now / 1000 - Number(timestamp)) > 300) return false;
  const key = secret.startsWith('whsec_') ? Buffer.from(secret.slice(6), 'base64') : Buffer.from(secret);
  if (!key.length) return false;
  const expected = crypto.createHmac('sha256', key).update(`${id}.${timestamp}.`).update(body).digest();
  return signatures.split(' ').slice(0, 32).some(candidate => {
    if (!candidate.startsWith('v1,')) return false;
    const supplied = Buffer.from(candidate.slice(3), 'base64');
    return supplied.length === expected.length && crypto.timingSafeEqual(supplied, expected);
  });
}

export interface OutboundPlan { to: string; objective: string; model: string; callPlan?: unknown; }
/** Process-local, expiring, single-use approval capabilities bound to the exact preview.
 * A token proves a preview occurred, NOT human consent; the operator/client must still approve.
 */
export class CallApprovals {
  private pending = new Map<string, { fingerprint: string; expires: number }>();
  constructor(private now: () => number = Date.now) {}
  private fingerprint(plan: OutboundPlan): string { return JSON.stringify([plan.to, plan.objective, plan.model, plan.callPlan ?? null]); }
  issue(plan: OutboundPlan): string {
    for (const [key, value] of this.pending) if (value.expires <= this.now()) this.pending.delete(key);
    if (this.pending.size >= 1000) throw new Error('Too many pending call previews');
    const token = crypto.randomBytes(32).toString('hex');
    this.pending.set(token, { fingerprint: this.fingerprint(plan), expires: this.now() + 300_000 });
    return token;
  }
  consume(token: unknown, plan: OutboundPlan): boolean {
    if (typeof token !== 'string') return false;
    const entry = this.pending.get(token);
    if (!entry) return false;
    this.pending.delete(token); // consume before any asynchronous dialing; never reusable after failure
    return entry.expires > this.now() && entry.fingerprint === this.fingerprint(plan);
  }
}

export function crmGreetingData(contact: { name?: string; context_notes?: string }): string {
  return JSON.stringify({ source: 'untrusted_crm', identityVerified: false,
    name: typeof contact.name === 'string' ? contact.name.slice(0, 100) : '',
    context: typeof contact.context_notes === 'string' ? contact.context_notes.slice(0, 1000) : '' });
}
