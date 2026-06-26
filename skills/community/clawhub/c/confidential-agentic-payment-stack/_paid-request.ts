import { FhePayingClient, type FheWallet, type ZamaFheSession } from '../../core/src/index.js';
import { getContracts } from './_wallet.js';

export interface DemoPaymentMetadata {
  amountMicros: bigint;
  txHash: string;
  nonce: string;
  payee: string;
  resourceUrl: string;
  etherscanUrl: string;
  mode?: 'live' | 'mock';
}

export interface DemoPaymentContext {
  wallet: FheWallet;
  session: ZamaFheSession;
  client: FhePayingClient;
  payerAddress: string;
}

interface PaymentChallenge {
  scheme?: string;
  price: string;
  tokenAddress: string;
  verifierAddress: string;
  recipientAddress: string;
  chainId: number;
}

export interface PaidJsonRequestResult<T = any> {
  body: T;
  payment: DemoPaymentMetadata;
}

export interface PaidBinaryRequestResult {
  contentType: string;
  bytes: number;
  headers: Record<string, string>;
  payment: DemoPaymentMetadata;
}

export async function createDemoPaymentContext(maxPayment: bigint = 100_000n): Promise<DemoPaymentContext> {
  const { wallet, session } = await getContracts();
  const payerAddress = await wallet.getAddress();

  const maxUsd = Number(maxPayment) / 1_000_000;
  const client = new FhePayingClient(wallet, session, {
    maxTotalUsd: maxUsd,
    maxPerRequestUsd: maxUsd,
    warnThresholdUsd: maxUsd * 0.8,
  });

  return { wallet, session, client, payerAddress };
}

function buildEtherscanUrl(chainId: number, txHash: string): string {
  const base = chainId === 1
    ? 'https://etherscan.io/tx/'
    : 'https://sepolia.etherscan.io/tx/';
  return `${base}${txHash}`;
}

function cloneHeaders(headers?: HeadersInit): Headers {
  return new Headers(headers);
}

function headersToObject(headers: Headers): Record<string, string> {
  return Object.fromEntries(headers.entries());
}

function latestReceipt(context: DemoPaymentContext, chainId: number, resourceUrl: string): DemoPaymentMetadata {
  const receipt = context.client.getReceipts().at(-1);
  if (!receipt) {
    throw new Error('Payment created but no receipt was recorded');
  }

  return {
    amountMicros: receipt.amountMicros,
    txHash: receipt.txHash,
    nonce: receipt.nonce,
    payee: receipt.payee,
    resourceUrl: receipt.resourceUrl ?? resourceUrl,
    etherscanUrl: buildEtherscanUrl(chainId, receipt.txHash),
  };
}

async function createMockMetadata(url: string): Promise<DemoPaymentMetadata> {
  return {
    amountMicros: 0n,
    txHash: 'mock-unpaid',
    nonce: 'mock-unpaid',
    payee: url,
    resourceUrl: url,
    etherscanUrl: '',
    mode: 'mock',
  };
}

function parseChallenge(response: Response): PaymentChallenge {
  const header = response.headers.get('x-payment-required');
  if (!header) {
    throw new Error('402 without X-Payment-Required header');
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(header);
  } catch {
    throw new Error('Malformed X-Payment-Required header');
  }

  const challenge = parsed as Partial<PaymentChallenge>;
  if (
    !challenge.price ||
    !challenge.tokenAddress ||
    !challenge.verifierAddress ||
    !challenge.recipientAddress ||
    challenge.chainId === undefined
  ) {
    throw new Error('Incomplete X-Payment-Required header');
  }

  return challenge as PaymentChallenge;
}

async function executePaidRequest(
  context: DemoPaymentContext,
  url: string,
  init: RequestInit,
  options?: {
    fetchFn?: typeof fetch;
    allowUnpaidSuccess?: boolean;
  },
): Promise<{ response: Response; payment: DemoPaymentMetadata }> {
  const fetchFn = options?.fetchFn ?? globalThis.fetch;
  const allowUnpaidSuccess = options?.allowUnpaidSuccess ?? (process.env.MOCK_PAYWALL === 'true');

  const initial = await fetchFn(url, init);

  if (initial.status !== 402) {
    if (initial.ok && allowUnpaidSuccess) {
      return {
        response: initial,
        payment: await createMockMetadata(url),
      };
    }
    throw new Error(`Expected HTTP 402 challenge from ${url}, got ${initial.status}`);
  }

  const challenge = parseChallenge(initial);
  const proof = await context.client.createPayment({
    price: BigInt(challenge.price),
    payTo: challenge.recipientAddress,
    verifierAddress: challenge.verifierAddress,
    tokenAddress: challenge.tokenAddress,
    chainId: challenge.chainId,
    resourceUrl: url,
  });

  const retryHeaders = cloneHeaders(init.headers);
  retryHeaders.set('x-payment', JSON.stringify(proof));

  const retried = await fetchFn(url, {
    ...init,
    headers: retryHeaders,
  });

  if (!retried.ok) {
    throw new Error(`Paid retry failed for ${url}: ${retried.status}`);
  }

  return {
    response: retried,
    payment: latestReceipt(context, challenge.chainId, url),
  };
}

export async function paidJsonRequest<T = any>(
  context: DemoPaymentContext,
  url: string,
  init: RequestInit,
  options?: {
    fetchFn?: typeof fetch;
    allowUnpaidSuccess?: boolean;
  },
): Promise<PaidJsonRequestResult<T>> {
  const { response, payment } = await executePaidRequest(context, url, init, options);

  let body: T;
  try {
    body = await response.json() as T;
  } catch {
    throw new Error(`Expected JSON response from ${url}`);
  }

  return { body, payment };
}

export async function paidBinaryRequest(
  context: DemoPaymentContext,
  url: string,
  init: RequestInit,
  options?: {
    fetchFn?: typeof fetch;
    allowUnpaidSuccess?: boolean;
  },
): Promise<PaidBinaryRequestResult> {
  const { response, payment } = await executePaidRequest(context, url, init, options);
  const bytes = (await response.arrayBuffer()).byteLength;

  return {
    contentType: response.headers.get('content-type') ?? '',
    bytes,
    headers: headersToObject(response.headers),
    payment,
  };
}
