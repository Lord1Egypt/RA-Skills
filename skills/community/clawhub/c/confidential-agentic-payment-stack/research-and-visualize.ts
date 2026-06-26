import { fail, ok, parseCliArgs } from './_wallet.js';
import { createDemoPaymentContext, paidBinaryRequest, paidJsonRequest } from './_paid-request.js';

function shortStep(payment: Awaited<ReturnType<typeof paidJsonRequest>>['payment'], step: string) {
  return {
    step,
    amountMicros: payment.amountMicros.toString(),
    txHash: payment.txHash,
    nonce: payment.nonce,
    etherscanUrl: payment.etherscanUrl,
    ...(payment.mode ? { mode: payment.mode } : {}),
  };
}

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.query) {
      return fail('--query is required');
    }

    const query = args.query;
    const searchUrl = process.env.SEARCH_SERVER_URL ?? 'http://127.0.0.1:3001';
    const llmUrl = process.env.LLM_SERVER_URL ?? 'http://127.0.0.1:3002';
    const imageUrl = process.env.IMAGE_SERVER_URL ?? 'http://127.0.0.1:3003';

    const context = await createDemoPaymentContext(100_000n);

    const search = await paidJsonRequest<{ results?: Array<{ title: string; url: string; snippet: string }> }>(
      context,
      `${searchUrl}/api/search`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ query, count: 5 }),
      },
    );

    const analysis = await paidJsonRequest<{ response?: string; usage?: Record<string, unknown> }>(
      context,
      `${llmUrl}/api/chat`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          messages: [
            { role: 'system', content: 'Summarize these search results into 3 concise insights.' },
            { role: 'user', content: JSON.stringify(search.body.results?.slice(0, 3) ?? []) },
          ],
        }),
      },
    );

    const image = await paidBinaryRequest(
      context,
      `${imageUrl}/api/generate`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          prompt: `Visual summary of: ${analysis.body.response?.slice(0, 200) ?? query}`,
          size: '512x512',
        }),
      },
    );

    const steps = [
      shortStep(search.payment, 'search'),
      shortStep(analysis.payment, 'analysis'),
      shortStep(image.payment, 'image'),
    ];

    const totalMicros = [
      search.payment.amountMicros,
      analysis.payment.amountMicros,
      image.payment.amountMicros,
    ].reduce((sum, value) => sum + value, 0n);

    return ok({
      action: 'research_and_visualize',
      query,
      steps,
      searchResults: search.body.results ?? [],
      analysis: analysis.body.response ?? '',
      image: {
        contentType: image.contentType,
        generationId: image.headers['x-generation-id'] ?? '',
        bytes: image.bytes,
      },
      totalMicros: totalMicros.toString(),
      totalUsd: (Number(totalMicros) / 1_000_000).toFixed(3),
      note: '3 encrypted x402 payments on Sepolia. Observers can see the txs, not the amounts.',
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('research-and-visualize.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
