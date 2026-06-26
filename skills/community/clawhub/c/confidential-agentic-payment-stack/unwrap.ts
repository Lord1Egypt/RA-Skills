import { getContracts, parseAmount, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.amount) {
      return fail('--amount is required');
    }

    const rawAmount = parseAmount(args.amount);
    const { session, cUSDC, wallet } = await getContracts();
    const signerAddress = await wallet.getAddress();
    const cUSDCAddress = await cUSDC.getAddress();

    // Step 1: Encrypt and send unwrap TX
    const encrypted = await session.encrypt(rawAmount, cUSDCAddress, signerAddress);

    const tx = await cUSDC.unwrap(
      signerAddress,
      signerAddress,
      encrypted.handles[0],
      encrypted.inputProof,
      { gasLimit: 2_000_000n }
    );
    const receipt = await tx.wait();

    // Parse the burn event to extract the encrypted amount handle.
    // The cUSDCMock emits ConfidentialTransfer(from, address(0), handle) for burns.
    // The Zama canonical wrapper may emit UnwrapRequested(receiver, handle).
    let burnHandle: string | null = null;
    let burnEventType: string | null = null;
    const iface = cUSDC.interface;
    for (const log of receipt.logs) {
      if (log.address.toLowerCase() !== cUSDCAddress.toLowerCase()) continue;
      try {
        const parsed = iface.parseLog({ topics: [...log.topics], data: log.data });
        if (!parsed) continue;
        // Look for ConfidentialTransfer to address(0) (burn)
        if (parsed.name === 'ConfidentialTransfer' &&
            parsed.args.to === '0x0000000000000000000000000000000000000000') {
          burnHandle = parsed.args.amount;
          burnEventType = 'ConfidentialTransfer(burn)';
          break;
        }
        // Or UnwrapRequested event (Zama canonical wrapper)
        if (parsed.name === 'UnwrapRequested') {
          burnHandle = parsed.args.amount;
          burnEventType = 'UnwrapRequested';
          break;
        }
      } catch { /* skip unparseable logs */ }
    }

    // Step 2: Try auto-finalization via publicDecrypt (SDK must be live, not stub)
    if (burnHandle && !session.isStub) {
      try {
        const decryptResult = await session.publicDecrypt([burnHandle]);
        const clearValue = decryptResult.clearValues[burnHandle];
        const proof = decryptResult.decryptionProof;

        if (clearValue !== undefined && proof) {
          const finalizeTx = await cUSDC.finalizeUnwrap(
            burnHandle,
            BigInt(clearValue as bigint | number | string),
            proof,
            { gasLimit: 500_000n }
          );
          const finalizeReceipt = await finalizeTx.wait();

          return ok({
            action: 'unwrap_complete',
            amount: args.amount,
            cleartextAmount: clearValue.toString(),
            unwrapTxHash: receipt.hash,
            finalizeTxHash: finalizeReceipt.hash,
            burnEventType,
            note: 'Auto-finalized via publicDecrypt. Underlying tokens released.',
          });
        }
      } catch (e: unknown) {
        // publicDecrypt failed — KMS may not be ready yet. Fall through to manual path.
        const msg = e instanceof Error ? e.message : String(e);
        return ok({
          action: 'unwrap_requested',
          amount: args.amount,
          txHash: receipt.hash,
          burnHandle,
          burnEventType,
          autoFinalizeError: msg.slice(0, 200),
          note: 'Step 1 complete. Auto-finalize failed — use finalize-unwrap --handle to complete manually after KMS processes the request.',
        });
      }
    }

    // No handle found or stub mode — return info for manual finalization
    return ok({
      action: 'unwrap_requested',
      amount: args.amount,
      txHash: receipt.hash,
      burnHandle: burnHandle ?? 'not found — check TX receipt for UnwrapRequested event',
      burnEventType,
      note: 'Step 1 complete. Run finalize-unwrap --handle <burnHandle> after KMS processes the decryption request (1-2 min).',
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('unwrap.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
