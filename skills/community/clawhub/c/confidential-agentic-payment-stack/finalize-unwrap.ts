import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    // Two modes:
    // 1. --handle: use publicDecrypt to get cleartext + proof, then finalize (recommended)
    // 2. --requestId + --cleartextAmount + --proof: manual finalization (legacy/fallback)

    const { session, cUSDC } = await getContracts();

    if (args.handle) {
      // Mode 1: publicDecrypt flow (uses Zama KMS)
      if (session.isStub) {
        return fail('publicDecrypt requires live Zama SDK — not available in stub mode. Use --requestId + --cleartextAmount + --proof instead.');
      }

      const handle = args.handle;
      let clearValue: bigint;
      let proof: string;

      try {
        const decryptResult = await session.publicDecrypt([handle]);
        const rawValue = decryptResult.clearValues[handle];
        if (rawValue === undefined) {
          return fail('publicDecrypt returned no value for handle. The KMS may not have processed the request yet — wait 1-2 minutes and retry.');
        }
        clearValue = BigInt(rawValue as bigint | number | string);
        proof = decryptResult.decryptionProof;
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        return fail(
          `publicDecrypt failed: ${msg.slice(0, 200)}. ` +
          'The KMS may not have processed the request yet. Wait 1-2 minutes and retry, or use --requestId + --cleartextAmount + --proof for manual finalization.'
        );
      }

      const tx = await cUSDC.finalizeUnwrap(
        handle,
        clearValue,
        proof,
        { gasLimit: 500_000n }
      );
      const receipt = await tx.wait();

      return ok({
        action: 'unwrap_finalized',
        handle,
        cleartextAmount: clearValue.toString(),
        txHash: receipt.hash,
        method: 'publicDecrypt',
      });
    }

    // Mode 2: Manual finalization (legacy — requires all 3 params)
    if (!args.requestId) {
      return fail('Either --handle (recommended) or --requestId + --cleartextAmount + --proof is required');
    }
    if (!args.cleartextAmount) {
      return fail('--cleartextAmount is required for manual finalization');
    }
    if (!args.proof) {
      return fail('--proof is required for manual finalization');
    }

    const tx = await cUSDC.finalizeUnwrap(
      args.requestId,
      BigInt(args.cleartextAmount),
      args.proof,
      { gasLimit: 500_000n }
    );
    const receipt = await tx.wait();

    return ok({
      action: 'unwrap_finalized',
      cleartextAmount: args.cleartextAmount,
      txHash: receipt.hash,
      method: 'manual',
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('finalize-unwrap.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
