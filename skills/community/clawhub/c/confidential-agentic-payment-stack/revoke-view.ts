import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.delegate) {
      return fail('--delegate is required (Ethereum address to revoke view access from)');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.delegate)) {
      return fail('--delegate must be a valid Ethereum address (0x + 40 hex chars)');
    }

    const { session, cUSDC, wallet } = await getContracts();
    const delegatorAddress = await wallet.getAddress();
    const cUSDCAddress = await cUSDC.getAddress();

    // Pre-check: use ReadonlyToken.isDelegated() to verify delegation exists
    const readonlyToken = await session.createReadonlyToken(wallet, cUSDCAddress);
    const isDelegated = await readonlyToken.isDelegated({
      delegatorAddress,
      delegateAddress: args.delegate,
    });

    if (!isDelegated) {
      return fail(
        `No active delegation exists from ${delegatorAddress} to ${args.delegate} for cUSDC.`
      );
    }

    // Token.revokeDelegation() handles ACL address resolution + on-chain TX
    const token = await session.createToken(wallet, cUSDCAddress);
    const result = await token.revokeDelegation({
      delegateAddress: args.delegate,
    });

    return ok({
      action: 'revoke_view',
      delegator: delegatorAddress,
      delegate: args.delegate,
      contract: cUSDCAddress,
      txHash: result.txHash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('revoke-view.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
