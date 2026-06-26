import { getContracts, ok, fail, formatUSDC, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.delegator) {
      return fail('--delegator is required (Ethereum address of the balance owner who granted you view access)');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.delegator)) {
      return fail('--delegator must be a valid Ethereum address (0x + 40 hex chars)');
    }

    const { session, cUSDC, wallet } = await getContracts();
    const delegateAddress = await wallet.getAddress();
    const cUSDCAddress = await cUSDC.getAddress();

    // Construct a ReadonlyToken for delegated decryption
    const readonlyToken = await session.createReadonlyToken(wallet, cUSDCAddress);

    // ReadonlyToken.decryptBalanceAs() handles:
    // - Reads confidentialBalanceOf(delegator) for the encrypted handle
    // - Returns 0n for zero handle (no balance, no KMS call)
    // - Pre-flight delegation check (DelegationNotFoundError, DelegationExpiredError)
    // - Credential management via DelegatedCredentialsManager
    // - KMS delegated decrypt
    // - Balance caching per (token, owner, handle)
    const balance = await readonlyToken.decryptBalanceAs({
      delegatorAddress: args.delegator,
    });

    // Get delegation expiry for metadata
    const expiry = await readonlyToken.getDelegationExpiry({
      delegatorAddress: args.delegator,
      delegateAddress,
    });

    return ok({
      action: 'view_as',
      delegator: args.delegator,
      delegate: delegateAddress,
      decryptedBalance: formatUSDC(balance),
      decryptedBalanceRaw: balance.toString(),
      delegationExpiry: expiry.toString(),
    });
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    const name = e instanceof Error ? (e as any).code ?? e.constructor?.name : '';

    // Map SDK error types to actionable messages
    if (name === 'DELEGATION_NOT_FOUND' || msg.includes('DelegationNotFound')) {
      return fail(
        `No delegation exists from ${args.delegator} to your wallet for cUSDC. ` +
        `Ask the delegator to run: grant-view --delegate <your-address>`
      );
    }
    if (name === 'DELEGATION_EXPIRED' || msg.includes('DelegationExpired')) {
      return fail(
        `Delegation from ${args.delegator} has expired. ` +
        `Ask the delegator to run grant-view again.`
      );
    }
    if (name === 'DELEGATION_NOT_PROPAGATED' || msg.includes('DelegationNotPropagated') || msg.includes('500')) {
      return fail(
        'Delegation may not have propagated to the Zama gateway yet. ' +
        'Wait 1-2 minutes after grant-view and try again.'
      );
    }
    return fail(msg);
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('view-as.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
