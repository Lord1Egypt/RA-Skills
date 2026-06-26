import { ethers } from 'ethers';
import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.jobId) {
      return fail('--jobId is required');
    }
    if (!args.action) {
      return fail('--action is required (must be "approve" or "reject")');
    }
    if (args.action !== 'approve' && args.action !== 'reject') {
      return fail('--action must be "approve" or "reject"');
    }

    const { escrow } = await getContracts();
    const reason = args.reason
      ? ethers.encodeBytes32String(args.reason.slice(0, 31))
      : ethers.ZeroHash;

    let tx;
    if (args.action === 'approve') {
      // ERC-8183: complete(jobId, reason, optParams)
      tx = await escrow.complete(BigInt(args.jobId), reason, '0x', { gasLimit: 2_000_000n });
    } else {
      // ERC-8183: reject(jobId, reason, optParams)
      tx = await escrow.reject(BigInt(args.jobId), reason, '0x', { gasLimit: 1_500_000n });
    }

    const receipt = await tx.wait();

    return ok({
      action: args.action,
      jobId: args.jobId,
      txHash: receipt.hash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('complete-job.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
