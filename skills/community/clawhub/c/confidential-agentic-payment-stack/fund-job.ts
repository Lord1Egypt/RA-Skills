import { getContracts, parseAmount, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.jobId) {
      return fail('--jobId is required');
    }
    if (!args.amount) {
      return fail('--amount is required');
    }

    const rawAmount = parseAmount(args.amount);

    const { session, cUSDC, escrow, wallet } = await getContracts();

    const escrowAddress = await escrow.getAddress();
    const clientAddress = await wallet.getAddress();

    // Encrypt the amount for setBudget:
    // contractAddress = escrow (where FHE.fromExternal runs)
    // userAddress = client (msg.sender when calling setBudget)
    const encrypted = await session.encrypt(
      rawAmount,
      escrowAddress,
      clientAddress,
    );

    // Step 1: Set budget (ERC-8183 2-step: setBudget then fund)
    await escrow.setBudget(
      BigInt(args.jobId),
      encrypted.handles[0],
      encrypted.inputProof,
      '0x', // optParams
      { gasLimit: 2_000_000n },
    );

    // Step 2: Set operator approval for escrow (1 hour deadline)
    const expiry = Math.floor(Date.now() / 1000) + 3600;
    await cUSDC.setOperator(escrowAddress, expiry, { gasLimit: 500_000n });

    // Step 3: Fund (pulls pre-set budget)
    const tx = await escrow.fund(
      BigInt(args.jobId),
      '0x', // optParams
      { gasLimit: 2_000_000n },
    );
    const receipt = await tx.wait();

    return ok({
      action: 'fund_job',
      jobId: args.jobId,
      txHash: receipt.hash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('fund-job.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
