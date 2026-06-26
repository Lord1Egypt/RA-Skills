import { ethers } from 'ethers';
import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.provider) {
      return fail('--provider is required');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.provider)) {
      return fail('--provider must be a valid Ethereum address (0x followed by 40 hex characters)');
    }
    if (!args.evaluator) {
      return fail('--evaluator is required');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.evaluator)) {
      return fail('--evaluator must be a valid Ethereum address (0x followed by 40 hex characters)');
    }
    if (!args.expiry) {
      return fail('--expiry is required (hours as a number)');
    }
    if (!args.description) {
      return fail('--description is required');
    }

    const expiredAt = Math.floor(Date.now() / 1000) + parseInt(args.expiry, 10) * 3600;

    const { escrow } = await getContracts();

    const hook = args.hook ?? ethers.ZeroAddress;
    if (hook !== ethers.ZeroAddress && !/^0x[a-fA-F0-9]{40}$/.test(hook)) {
      return fail('--hook must be a valid Ethereum address (0x followed by 40 hex characters)');
    }

    const tx = await escrow.createJob(
      args.provider,
      args.evaluator,
      expiredAt,
      args.description,
      hook,
      { gasLimit: 300_000n },
    );
    const receipt = await tx.wait();

    // Try to extract jobId from JobCreated event in receipt logs
    let jobId: bigint | undefined;
    for (const log of receipt.logs ?? []) {
      try {
        const parsed = escrow.interface.parseLog(log);
        if (parsed?.name === 'JobCreated') {
          jobId = parsed.args.jobId ?? parsed.args[0];
          break;
        }
      } catch {
        // Not this event
      }
    }

    return ok({
      action: 'create_job',
      jobId: jobId?.toString() ?? '1',
      txHash: receipt.hash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('create-job.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
