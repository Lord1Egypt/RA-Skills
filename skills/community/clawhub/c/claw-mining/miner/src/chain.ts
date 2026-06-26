import { ethers } from 'ethers';
import type { MinerConfig } from './config.js';
import type { ChainState, MinerChainState, Attestation } from './types.js';

const POAIW_ABI = [
  'function currentEra() view returns (uint256)',
  'function currentGlobalEpoch() view returns (uint256)',
  'function currentSeed() view returns (uint256)',
  'function seedEpoch() view returns (uint256)',
  'function eraModel(uint256) view returns (bytes32)',
  'function cooldownRemaining(address) view returns (uint256)',
  'function epochClaimCount(address,uint256) view returns (uint256)',
  'function MAX_CLAIMS_PER_EPOCH() view returns (uint256)',
  'function COOLDOWN_BLOCKS() view returns (uint256)',
  'function estimateReward(uint256) view returns (uint256)',
  'function epochCap(uint256) view returns (uint256)',
  'function epochMinted(uint256) view returns (uint256)',
  'function updateSeed()',
  'function mint(bytes32 modelHash, uint256 totalTokens, uint256 claimSeedEpoch, uint256 claimSeed, uint256 claimIndex, uint256 deadline, bytes signature)',
];

const TOKEN_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function symbol() view returns (string)',
  'function decimals() view returns (uint8)',
];

export class ChainClient {
  public readonly provider: ethers.JsonRpcProvider;
  public readonly wallet: ethers.Wallet;
  public readonly poaiwMint: ethers.Contract;

  // F-08: Accept wallet directly from config — no longer reconstructs from privateKey
  constructor(config: MinerConfig) {
    this.provider = config.wallet.provider as ethers.JsonRpcProvider;
    this.wallet = config.wallet;
    this.poaiwMint = new ethers.Contract(config.poaiwMintAddress, POAIW_ABI, this.wallet);
  }

  async getChainState(): Promise<ChainState> {
    const [currentEra, currentGlobalEpoch, currentSeed, seedEpoch, blockNumber] =
      await Promise.all([
        this.poaiwMint.currentEra() as Promise<bigint>,
        this.poaiwMint.currentGlobalEpoch() as Promise<bigint>,
        this.poaiwMint.currentSeed() as Promise<bigint>,
        this.poaiwMint.seedEpoch() as Promise<bigint>,
        this.provider.getBlockNumber(),
      ]);

    const eraModelHash: string = await this.poaiwMint.eraModel(currentEra);

    return { currentEra, currentGlobalEpoch, currentSeed, seedEpoch, eraModelHash, currentBlock: blockNumber };
  }

  async getMinerState(minerAddress: string, epoch: bigint): Promise<MinerChainState> {
    const [cooldownRemaining, epochClaimCount, maxClaimsPerEpoch, ethBalance] = await Promise.all([
      this.poaiwMint.cooldownRemaining(minerAddress) as Promise<bigint>,
      this.poaiwMint.epochClaimCount(minerAddress, epoch) as Promise<bigint>,
      this.poaiwMint.MAX_CLAIMS_PER_EPOCH() as Promise<bigint>,
      this.provider.getBalance(minerAddress),
    ]);

    return { cooldownRemaining, epochClaimCount, maxClaimsPerEpoch, ethBalance };
  }

  async getGasPrice(): Promise<bigint> {
    const feeData = await this.provider.getFeeData();
    return feeData.gasPrice ?? 0n;
  }

  async updateSeed(): Promise<ethers.TransactionReceipt> {
    const tx = await this.poaiwMint.updateSeed();
    const receipt = await tx.wait();
    if (!receipt) throw new Error('updateSeed transaction failed');
    return receipt;
  }

  async mint(attestation: Attestation): Promise<ethers.TransactionReceipt> {
    // Estimate gas first with 20% buffer
    const gasEstimate = await this.poaiwMint.mint.estimateGas(
      attestation.model_hash,
      BigInt(attestation.total_tokens),
      BigInt(attestation.seed_epoch),
      BigInt(attestation.seed),
      BigInt(attestation.claim_index),
      BigInt(attestation.deadline),
      attestation.signature,
    );

    // F-13: BigInt division truncates — add 1n to ensure buffer is never rounded to zero
    const gasLimit = (gasEstimate * 120n + 99n) / 100n;

    const tx = await this.poaiwMint.mint(
      attestation.model_hash,
      BigInt(attestation.total_tokens),
      BigInt(attestation.seed_epoch),
      BigInt(attestation.seed),
      BigInt(attestation.claim_index),
      BigInt(attestation.deadline),
      attestation.signature,
      { gasLimit },
    );

    const receipt = await tx.wait();
    if (!receipt) throw new Error('mint transaction failed');
    return receipt;
  }

  async getCooldownBlocks(): Promise<bigint> {
    return this.poaiwMint.COOLDOWN_BLOCKS() as Promise<bigint>;
  }

  async estimateReward(totalTokens: bigint): Promise<bigint> {
    return this.poaiwMint.estimateReward(totalTokens) as Promise<bigint>;
  }
}
