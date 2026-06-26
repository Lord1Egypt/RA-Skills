import { ethers } from 'ethers';
import { getContracts, parseAmount, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.to) {
      return fail('--to is required');
    }
    if (!/^0x[a-fA-F0-9]{40}$/.test(args.to)) {
      return fail('--to must be a valid Ethereum address (0x followed by 40 hex characters)');
    }
    if (!args.amount) {
      return fail('--amount is required');
    }

    const to = args.to;
    const rawAmount = parseAmount(args.amount);
    const { session, cUSDC, verifier, wallet } = await getContracts();
    const signerAddress = await wallet.getAddress();

    const nonce = ethers.hexlify(ethers.randomBytes(32));

    const { handles, inputProof } = await session.encrypt(
      rawAmount,
      await cUSDC.getAddress(),
      signerAddress,
    );

    const data = ethers.AbiCoder.defaultAbiCoder().encode(
      ['address', 'bytes32', 'uint64'],
      [to, nonce, rawAmount],
    );

    const tx = await cUSDC.confidentialTransferAndCall(
      await verifier.getAddress(),
      handles[0],
      inputProof,
      data,
      { gasLimit: 2_000_000n },
    );
    const receipt = await tx.wait();

    return ok({
      action: 'pay',
      to,
      amount: args.amount,
      txHash: receipt.hash,
      nonce,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('pay.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
