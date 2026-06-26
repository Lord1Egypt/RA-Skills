import { ethers } from 'ethers';
import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    if (!args.uri || args.uri.trim() === '') {
      return fail('--uri is required and must be a non-empty string');
    }

    const { identity, wallet } = await getContracts();
    const signerAddress = await wallet.getAddress();

    // ERC-8004: register(string agentURI) — disambiguate overload for ethers v6
    const tx = await identity.getFunction('register(string)')(args.uri, { gasLimit: 500_000n });
    const receipt = await tx.wait();

    // Extract agentId from Registered event (ERC-8004 event name)
    let agentId: bigint = 0n;
    if (receipt?.logs) {
      for (const log of receipt.logs) {
        try {
          const iface = new ethers.Interface([
            'event Registered(uint256 indexed agentId, string agentURI, address indexed owner)',
          ]);
          const parsed = iface.parseLog(log);
          if (parsed && parsed.name === 'Registered') {
            agentId = BigInt(parsed.args.agentId);
            break;
          }
        } catch {
          // Log didn't match — continue
        }
      }
    }

    // ERC-8004: setAgentWallet requires EIP-712 signature from the wallet being linked.
    // Since the agent owner IS the wallet, we self-sign.
    const deadline = Math.floor(Date.now() / 1000) + 3600; // 1 hour
    const domain = {
      name: 'AgentIdentityRegistry',
      version: '1',
      chainId: (await wallet.getProvider().getNetwork()).chainId,
      verifyingContract: await identity.getAddress(),
    };
    const types = {
      SetAgentWallet: [
        { name: 'agentId', type: 'uint256' },
        { name: 'newWallet', type: 'address' },
        { name: 'deadline', type: 'uint256' },
      ],
    };
    const value = { agentId, newWallet: signerAddress, deadline };
    const signature = await wallet.signTypedData(domain, types, value);

    const setTx = await identity.setAgentWallet(
      agentId, signerAddress, deadline, signature,
      { gasLimit: 300_000n },
    );
    await setTx.wait();

    return ok({
      action: 'register',
      agentId: agentId.toString(),
      txHash: receipt.hash,
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('register-agent.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
