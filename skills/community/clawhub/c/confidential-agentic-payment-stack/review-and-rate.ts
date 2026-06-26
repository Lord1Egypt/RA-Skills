import { fail, ok, parseCliArgs } from './_wallet.js';
import { paidJsonRequest, createDemoPaymentContext } from './_paid-request.js';
import { run as runGiveFeedback } from './give-feedback.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.code) {
      return fail('--code is required');
    }

    const language = args.language ?? 'typescript';
    const score = args.score ?? '80';

    // Validate score before spending money on the paid review
    try { BigInt(score); } catch {
      return fail('--score must be an integer (e.g. 80, -10)');
    }

    const codeReviewUrl = process.env.CODE_REVIEW_URL ?? 'http://127.0.0.1:3004';
    const agentId = process.env.CODE_REVIEW_AGENT_ID;

    const context = await createDemoPaymentContext(100_000n);

    const review = await paidJsonRequest<{
      issues?: Array<Record<string, unknown>>;
      summary?: string;
    }>(
      context,
      `${codeReviewUrl}/api/review`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          code: args.code,
          language,
        }),
      },
    );

    let feedback:
      | {
          submitted: boolean;
          agentId?: string;
          txHash?: string;
        }
      | {
          submitted: false;
          skipped: true;
          reason: string;
        };

    if (!agentId) {
      feedback = {
        submitted: false,
        skipped: true,
        reason: 'CODE_REVIEW_AGENT_ID is not configured',
      };
    } else {
      const raw = await runGiveFeedback({
        agentId,
        score,
        nonce: review.payment.nonce,
        tag1: 'demo',
        tag2: 'code-review',
      });
      const parsed = JSON.parse(raw);
      if (!parsed.ok) {
        return fail(`Feedback failed after successful paid review: ${parsed.error}`);
      }
      feedback = {
        submitted: true,
        agentId,
        txHash: parsed.txHash,
      };
    }

    return ok({
      action: 'review_and_rate',
      payment: {
        amountMicros: review.payment.amountMicros.toString(),
        txHash: review.payment.txHash,
        nonce: review.payment.nonce,
        etherscanUrl: review.payment.etherscanUrl,
        ...(review.payment.mode ? { mode: review.payment.mode } : {}),
      },
      review: {
        issues: review.body.issues ?? [],
        summary: review.body.summary ?? '',
      },
      feedback,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('review-and-rate.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
