import { getContracts, parseAmount, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.amount) {
      return fail('--amount is required');
    }

    const rawAmount = parseAmount(args.amount);
    const { usdc, cUSDC, wallet } = await getContracts();
    const address = await wallet.getAddress();

    await usdc.approve(await cUSDC.getAddress(), rawAmount, { gasLimit: 100_000n });

    const tx = await cUSDC.wrap(address, rawAmount, { gasLimit: 500_000n });
    const receipt = await tx.wait();

    return ok({
      action: 'wrap',
      amount: args.amount,
      txHash: receipt.hash,
      blockNumber: receipt.blockNumber,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('wrap.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
