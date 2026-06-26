import { getContracts, ok, fail, formatUSDC, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    const { usdc, cUSDC, session, wallet } = await getContracts();
    const ownAddress = await wallet.getAddress();

    // --of: read another agent's balance via delegation
    const targetAddress = args.of ?? ownAddress;
    const isDelegated = !!args.of && args.of.toLowerCase() !== ownAddress.toLowerCase();

    if (isDelegated && !/^0x[a-fA-F0-9]{40}$/.test(args.of)) {
      return fail('--of must be a valid Ethereum address (0x + 40 hex chars)');
    }

    // Public USDC balance (always readable — ERC-20)
    const publicBalance: bigint = await usdc.balanceOf(targetAddress);

    // Encrypted cUSDC balance handle
    const zeroBits = '0x' + '00'.repeat(32);
    let encryptedHandle: string;
    if (isDelegated) {
      // For delegated reads: let errors propagate — a network error is not "zero balance"
      encryptedHandle = await cUSDC.confidentialBalanceOf(targetAddress);
    } else {
      // For own balance: graceful fallback (existing behavior)
      try {
        encryptedHandle = await cUSDC.confidentialBalanceOf(targetAddress);
      } catch {
        encryptedHandle = zeroBits;
      }
    }
    const hasEncryptedBalance = encryptedHandle !== zeroBits;

    // Decrypt own balance if --decrypt flag is set
    let decryptedBalance: string | null = null;
    let decryptedBalanceRaw: string | null = null;
    let delegationError: string | null = null;

    const wantDecrypt = args.decrypt === 'true' || args.decrypt === '';

    if (!isDelegated && wantDecrypt && hasEncryptedBalance) {
      try {
        const cUSDCAddress = await cUSDC.getAddress();
        const balance = await session.decryptBalance(
          encryptedHandle,
          cUSDCAddress,
          ownAddress,
          wallet,
        );
        decryptedBalance = formatUSDC(balance);
        decryptedBalanceRaw = balance.toString();
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        if (msg.includes('stub mode') || msg.includes('Cannot create')) {
          delegationError = 'Decrypt requires @zama-fhe/sdk (not available in stub mode)';
        } else {
          throw e;
        }
      }
    }

    // If delegated and has balance, attempt decryption via ReadonlyToken
    if (isDelegated && hasEncryptedBalance) {
      try {
        const cUSDCAddress = await cUSDC.getAddress();
        const readonlyToken = await session.createReadonlyToken(wallet, cUSDCAddress);
        const balance = await readonlyToken.decryptBalanceAs({
          delegatorAddress: targetAddress,
        });
        decryptedBalance = formatUSDC(balance);
        decryptedBalanceRaw = balance.toString();
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        const code = (e as any)?.code ?? '';

        // Only delegation-state errors are non-fatal (user can fix by running grant-view)
        // Infrastructure errors (SDK missing, network down, etc.) should propagate as fail()
        // Match by error code (stable), constructor name, AND message substring (defense in depth
        // against SDK version changes renaming error classes)
        const name = (e as any)?.constructor?.name ?? '';
        const isDelegationError =
          code === 'DELEGATION_NOT_FOUND' || name === 'DelegationNotFoundError' || msg.includes('DelegationNotFound') ||
          code === 'DELEGATION_EXPIRED' || name === 'DelegationExpiredError' || msg.includes('DelegationExpired') ||
          code === 'DELEGATION_NOT_PROPAGATED' || name === 'DelegationNotPropagatedError' || msg.includes('DelegationNotPropagated') ||
          code === 'DELEGATION_COOLDOWN' || name === 'DelegationCooldownError' || msg.includes('DelegationCooldown');

        if (code === 'DELEGATION_NOT_FOUND' || name === 'DelegationNotFoundError' || msg.includes('DelegationNotFound')) {
          delegationError = 'No delegation — ask the owner to run grant-view --delegate ' + ownAddress;
        } else if (code === 'DELEGATION_EXPIRED' || name === 'DelegationExpiredError' || msg.includes('DelegationExpired')) {
          delegationError = 'Delegation expired — ask the owner to run grant-view again';
        } else if (code === 'DELEGATION_NOT_PROPAGATED' || name === 'DelegationNotPropagatedError' || msg.includes('DelegationNotPropagated')) {
          delegationError = 'Delegation not yet propagated — wait 1-2 minutes after grant-view';
        } else if (code === 'DELEGATION_COOLDOWN' || name === 'DelegationCooldownError' || msg.includes('DelegationCooldown')) {
          delegationError = 'Delegation cooldown — wait a few minutes before delegating again';
        } else {
          // Infrastructure error — not a delegation-state problem. Fail hard.
          throw e;
        }
      }
    }

    return ok({
      action: 'balance',
      walletAddress: targetAddress,
      ...(isDelegated ? { viewingAs: ownAddress } : {}),
      publicBalance: publicBalance.toString(),
      publicBalanceUSDC: formatUSDC(publicBalance),
      hasEncryptedBalance,
      encryptedBalanceHandle: encryptedHandle,
      ...(decryptedBalance !== null ? { decryptedBalance, decryptedBalanceRaw } : {}),
      ...(delegationError !== null ? { delegationError } : {}),
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('balance.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
