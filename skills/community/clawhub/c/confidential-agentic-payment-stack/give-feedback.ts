import { ethers } from 'ethers';
import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.agentId) {
      return fail('--agentId is required');
    }
    if (!args.score) {
      return fail('--score is required (integer, e.g. 80 for 80.0)');
    }
    if (!args.nonce) {
      return fail('--nonce is required (bytes32 from prior payment)');
    }

    // Parse score as BigInt to handle the full int128 range safely.
    // int128 range: -170141183460469231731687303715884105728 to 170141183460469231731687303715884105727
    // For practical reputation scores, values like -100 to 100 are typical.
    let scoreBigInt: bigint;
    try {
      scoreBigInt = BigInt(args.score);
    } catch {
      return fail('--score must be an integer (e.g. 80, -10)');
    }
    const INT128_MIN = -(2n ** 127n);
    const INT128_MAX = 2n ** 127n - 1n;
    if (scoreBigInt < INT128_MIN || scoreBigInt > INT128_MAX) {
      return fail(`--score must be within int128 range (${INT128_MIN} to ${INT128_MAX})`);
    }

    const { reputation, verifier } = await getContracts();

    // Derive proof-of-payment from payment nonce + verifier address
    const proofOfPayment = ethers.keccak256(
      ethers.solidityPacked(
        ['bytes32', 'address'],
        [args.nonce, await verifier.getAddress()],
      ),
    );

    // ERC-8004 Reputation: giveFeedback(agentId, int128 value, uint8 valueDecimals,
    //   tag1, tag2, endpoint, feedbackURI, feedbackHash, proofOfPayment)
    const tag1 = args.tag1 ?? '';
    const tag2 = args.tag2 ?? '';
    const endpoint = args.endpoint ?? '';
    const feedbackURI = args.feedbackURI ?? '';
    const feedbackHash = args.feedbackHash ?? ethers.ZeroHash;

    const tx = await reputation.giveFeedback(
      BigInt(args.agentId),
      scoreBigInt,         // int128 value
      0,                   // uint8 valueDecimals (0 = integer score)
      tag1,
      tag2,
      endpoint,
      feedbackURI,
      feedbackHash,
      ethers.getBytes(proofOfPayment), // bytes proofOfPayment
      { gasLimit: 300_000n },
    );
    const receipt = await tx.wait();

    return ok({
      action: 'feedback',
      agentId: args.agentId,
      score: scoreBigInt.toString(),
      txHash: receipt.hash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('give-feedback.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
