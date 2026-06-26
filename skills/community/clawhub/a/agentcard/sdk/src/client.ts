/**
 * @asgcard/sdk — ASGCardClient
 *
 * Main client for the ASG Card API.
 * Handles x402 payment flow on Stellar automatically.
 */
import { Keypair, rpc as StellarRpc } from "@stellar/stellar-sdk";
import { ApiError, TimeoutError } from "./errors";
import type {
  ASGCardClientConfig,
  CardResult,
  CreateCardParams,
  FundCardParams,
  FundResult,
  HealthResponse,
  TierResponse,
  WalletAdapter,
} from "./types";
import { handleX402Payment } from "./utils/x402";

const DEFAULT_BASE_URL = "https://api.asgcard.dev";
const DEFAULT_RPC_URL = "https://mainnet.sorobanrpc.com";
const DEFAULT_TIMEOUT = 60_000;

export class ASGCardClient {
  private readonly baseUrl: string;

  private readonly timeout: number;

  private readonly rpcServer: StellarRpc.Server;

  private readonly keypair?: Keypair;

  private readonly walletAdapter?: WalletAdapter;

  constructor(config: ASGCardClientConfig) {
    if (!config.privateKey && !config.walletAdapter) {
      throw new Error("Provide either privateKey or walletAdapter");
    }

    this.baseUrl = config.baseUrl ?? DEFAULT_BASE_URL;
    this.timeout = config.timeout ?? DEFAULT_TIMEOUT;
    this.rpcServer = new StellarRpc.Server(config.rpcUrl ?? DEFAULT_RPC_URL);

    if (config.privateKey) {
      this.keypair = Keypair.fromSecret(config.privateKey);
    }

    this.walletAdapter = config.walletAdapter;
  }

  /** Stellar public key (G...) */
  get address(): string {
    if (this.keypair) {
      return this.keypair.publicKey();
    }

    return this.walletAdapter!.publicKey;
  }

  /**
   * Create a virtual card for a supported tier amount.
   * Handles 402 → x402 payment → 201 automatically.
   */
  async createCard(params: CreateCardParams): Promise<CardResult> {
    return this.requestWithX402<CardResult>(`/cards/create/tier/${params.amount}`, {
      method: "POST",
      body: JSON.stringify({
        nameOnCard: params.nameOnCard,
        email: params.email
      })
    });
  }

  /**
   * Fund an existing card by tier amount.
   * Handles 402 → x402 payment → 200 automatically.
   */
  async fundCard(params: FundCardParams): Promise<FundResult> {
    return this.requestWithX402<FundResult>(`/cards/fund/tier/${params.amount}`, {
      method: "POST",
      body: JSON.stringify({ cardId: params.cardId })
    });
  }

  /** Get available create/fund tier amounts and pricing */
  async getTiers(): Promise<TierResponse> {
    return this.request<TierResponse>("/cards/tiers", { method: "GET" });
  }

  /** Health check */
  async health(): Promise<HealthResponse> {
    return this.request<HealthResponse>("/health", { method: "GET" });
  }

  // ── x402 payment flow ────────────────────────────────

  private async requestWithX402<T>(path: string, init: RequestInit): Promise<T> {
    const first = await this.rawFetch(path, init);

    if (first.status !== 402) {
      return this.parseResponse<T>(first);
    }

    const challengePayload = await first.json();

    const paymentHeader = await handleX402Payment({
      rpcServer: this.rpcServer,
      challengePayload,
      keypair: this.keypair,
      walletAdapter: this.walletAdapter
    });

    const retry = await this.rawFetch(path, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        "X-PAYMENT": paymentHeader,
        ...(init.headers ?? {})
      }
    });

    return this.parseResponse<T>(retry);
  }

  // ── HTTP primitives ──────────────────────────────────

  private async request<T>(path: string, init: RequestInit): Promise<T> {
    const response = await this.rawFetch(path, init);
    return this.parseResponse<T>(response);
  }

  private async rawFetch(path: string, init: RequestInit): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      return await fetch(`${this.baseUrl}${path}`, {
        ...init,
        headers: {
          "Content-Type": "application/json",
          ...(init.headers ?? {})
        },
        signal: controller.signal
      });
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        throw new TimeoutError();
      }

      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private async parseResponse<T>(response: Response): Promise<T> {
    const payload = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new ApiError(response.status, payload);
    }

    return payload as T;
  }
}
