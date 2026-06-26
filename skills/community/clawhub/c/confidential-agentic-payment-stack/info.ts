import { getContracts, ok, fail, parseCliArgs } from './_wallet.js';

export async function run(args: Record<string, string>): Promise<string> {
  try {
    const { wallet, provider, cUSDC, verifier, identity, reputation, escrow } =
      await getContracts();

    const address = await wallet.getAddress();
    const ethBalance = await provider.getBalance(address);

    const network = await provider.getNetwork();
    const networkName =
      network.chainId === 1n ? 'Ethereum Mainnet' :
      network.chainId === 11155111n ? 'Ethereum Sepolia' :
      `Chain ${network.chainId}`;

    return ok({
      action: 'info',
      network: networkName,
      chainId: Number(network.chainId),
      walletType: wallet.type,
      walletAddress: address,
      ethBalance: ethBalance.toString(),
      contracts: {
        cUSDC: await cUSDC.getAddress(),
        verifier: await verifier.getAddress(),
        identity: await identity.getAddress(),
        reputation: await reputation.getAddress(),
        escrow: await escrow.getAddress(),
      },
      scheme: 'fhe-confidential-v1',
    });
  } catch (e: unknown) {
    return fail(e instanceof Error ? e.message : String(e));
  }
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('info.ts')) {
  const args = parseCliArgs(process.argv.slice(2));
  run(args).then(console.log);
}
