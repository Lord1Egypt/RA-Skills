import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.delegate) {
      return fail('--delegate is required (Ethereum address to grant view access)');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.delegate)) {
      return fail('--delegate must be a valid Ethereum address (0x + 40 hex chars)');
    }

    const { session, cUSDC, wallet } = await getContracts();
    const cUSDCAddress = await cUSDC.getAddress();

    // --contract overrides the default cUSDC. For amount verification, use the verifier address.
    const contractAddress = args.contract ?? cUSDCAddress;
    if (args.contract && !/^0x[a-fA-F0-9]{40}$/.test(args.contract)) {
      return fail('--contract must be a valid Ethereum address');
    }

    // Construct a native Zama SDK Token for the target contract
    const token = await session.createToken(wallet, contractAddress);

    // Expiry: --permanent for no expiry, --hours for custom (default 24h)
    let expirationDate: Date | undefined;
    let expiresIn: string;

    if (args.permanent === 'true' || args.permanent === '') {
      expirationDate = undefined; // SDK defaults to uint64.max (permanent)
      expiresIn = 'permanent (never expires)';
    } else {
      const hours = parseInt(args.hours ?? '24', 10);
      if (isNaN(hours) || hours < 1) {
        return fail('--hours must be a positive integer >= 1');
      }
      expirationDate = new Date(Date.now() + hours * 3600 * 1000);
      expiresIn = `${hours} hours`;
    }

    // Token.delegateDecryption() handles:
    // - ACL address resolution
    // - Self-delegation check (throws DelegationSelfNotAllowedError)
    // - Past-expiry check (throws ConfigurationError)
    // - On-chain TX + receipt
    const result = await token.delegateDecryption({
      delegateAddress: args.delegate,
      expirationDate,
    });

    return ok({
      action: 'grant_view',
      delegator: await wallet.getAddress(),
      delegate: args.delegate,
      contract: contractAddress,
      expiresIn,
      txHash: result.txHash,
      note: 'Delegation takes 1-2 minutes to propagate to the Zama gateway before view-as works.',
    });
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    // Map SDK-specific errors to user-friendly messages
    if (msg.includes('SelfNotAllowed') || msg.includes('self')) {
      return fail('Cannot delegate to yourself. The delegate must be a different address.');
    }
    return fail(msg);
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('grant-view.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
