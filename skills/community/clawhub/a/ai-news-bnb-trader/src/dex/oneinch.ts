import { Wallet, JsonRpcProvider } from 'ethers';
import { logger } from '../utils/logger.js';

export type Quote = { toTokenAmount: bigint; estimatedGas: bigint; srcUsd?: number; dstUsd?: number; slippageBps: number };

export class OneInchDex {
  constructor(
    private provider: JsonRpcProvider,
    private wallet: Wallet,
    private base: string,
    private apiKey: string,
    private dryRun: boolean
  ) {}

  private headers() {
    const h: Record<string, string> = { 'accept': 'application/json' };
    if (this.apiKey) h['Authorization'] = `Bearer ${this.apiKey}`;
    return h;
  }

  async quote(from: string, to: string, amount: bigint): Promise<Quote> {
    const url = `${this.base}/quote?src=${from}&dst=${to}&amount=${amount.toString()}`;
    const r = await fetch(url, { headers: this.headers() });
    if (!r.ok) throw new Error(`quote failed ${r.status}`);
    const j = await r.json();
    return {
      toTokenAmount: BigInt(j.dstAmount),
      estimatedGas: BigInt(j.gas ?? 0),
      slippageBps: 30
    };
  }

  async swap(from: string, to: string, amount: bigint, slippageBps: number): Promise<{ txHash?: string }> {
    if (this.dryRun) {
      logger.info('[DRY-RUN] swap', from, to, amount.toString(), `slippage=${slippageBps}`);
      return {};
    }
    const url = `${this.base}/swap?src=${from}&dst=${to}&amount=${amount.toString()}&from=${this.wallet.address}&slippage=${(slippageBps/100).toFixed(2)}&disableEstimate=true`;
    const r = await fetch(url, { headers: this.headers() });
    if (!r.ok) throw new Error(`swap build failed ${r.status}`);
    const j = await r.json();

    const tx = await this.wallet.sendTransaction({
      to: j.tx.to,
      data: j.tx.data,
      value: BigInt(j.tx.value ?? '0'),
      gasLimit: BigInt(j.tx.gas ?? '500000')
    });
    const rcpt = await tx.wait();
    return { txHash: rcpt?.hash };
  }
}
