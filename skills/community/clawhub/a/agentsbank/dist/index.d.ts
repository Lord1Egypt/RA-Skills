/**
 * AgentsBank SDK Types
 * TypeScript definitions for the AgentsBank API
 */
interface RetryConfig {
    /** Maximum retry attempts for transient failures */
    maxAttempts?: number;
    /** Initial delay in milliseconds */
    initialDelayMs?: number;
    /** Maximum delay in milliseconds */
    maxDelayMs?: number;
}
interface CacheConfig {
    /** Enable response caching */
    enabled?: boolean;
    /** Use Redis for caching (default: fallback to in-memory) */
    useRedis?: boolean;
}
interface GuardrailsConfig {
    /** Daily spending limit in USD */
    dailyLimitUSD?: number;
    /** Maximum per-transaction limit in USD */
    maxPerTxUSD?: number;
    /** List of whitelisted recipient addresses */
    whitelistedAddresses?: string[];
    /** List of blacklisted recipient addresses */
    blacklistedAddresses?: string[];
    /** Max transactions per hour */
    maxTxPerHour?: number;
    /** Max unique recipients per day */
    maxRecipientsPerDay?: number;
}
interface WebhookConfig {
    /** Webhook URL for event notifications */
    url?: string;
    /** Secret for HMAC-SHA256 signing */
    secret?: string;
    /** Events to subscribe to */
    events?: WebhookEvent[];
}
type WebhookEvent = 'transaction.sent' | 'transaction.received' | 'transaction.confirmed' | 'wallet.created' | 'balance.changed' | 'error.occurred' | 'agent.login';
interface AgentsBankConfig {
    /** Base URL of the AgentsBank API */
    baseUrl?: string;
    /** API key for authentication (alternative to JWT) */
    apiKey?: string;
    /** JWT token for authentication */
    token?: string;
    /** Request timeout in milliseconds */
    timeout?: number;
    /** Custom fetch implementation */
    fetch?: typeof fetch;
    /** Retry configuration for transient failures */
    retryConfig?: RetryConfig;
    /** Cache configuration */
    cacheConfig?: CacheConfig;
    /** Guardrails for spending limits and restrictions */
    guardrails?: GuardrailsConfig;
    /** Webhook configuration for events */
    webhooks?: WebhookConfig;
}
interface RegisterAgentRequest {
    /** Human's username */
    human_username: string;
    /** Human's email */
    human_email: string;
    /** Agent owner's first name */
    first_name: string;
    /** Agent owner's last name */
    last_name: string;
    /** Password for agent (min 8 chars, uppercase, number, special char) */
    agent_password: string;
    /** Optional agent capabilities */
    capabilities?: string[];
    /** Optional agent description */
    description?: string;
}
interface RegisterAgentResponse {
    agent_id: string;
    agent_username: string;
    api_key: string;
    did: string;
    token: string;
    recovery_words: string[];
    wallets: WalletInfo[];
    message: string;
}
interface LoginRequest {
    agent_username: string;
    agent_password: string;
}
interface LoginResponse {
    agent_id: string;
    token: string;
}
type Chain = 'ethereum' | 'bsc' | 'solana' | 'bitcoin';
type Currency = 'ETH' | 'BNB' | 'SOL' | 'BTC' | 'USDT' | 'USDC';
interface WalletInfo {
    wallet_id: string;
    agent_id: string;
    chain: Chain;
    address: string;
    type: 'custodial';
    balance?: WalletBalance;
    created_at: string;
}
interface WalletBalance {
    [currency: string]: string;
}
interface CreateWalletRequest {
    chain: Chain;
}
interface CreateWalletResponse extends WalletInfo {
}
interface GetBalanceResponse {
    wallet_id: string;
    chain: Chain;
    address: string;
    balance: WalletBalance;
}
interface SendTransactionRequest {
    /** Recipient address */
    to_address: string;
    /** Amount to send (as string for precision) */
    amount: string;
    /** Optional: currency (defaults to native token) */
    currency?: Currency;
}
interface SendTransactionResponse {
    tx_hash: string;
    status: TransactionStatus;
    from_address: string;
    to_address: string;
    amount: string;
    chain: Chain;
}
type TransactionStatus = 'pending' | 'confirmed' | 'failed';
interface Transaction {
    tx_id: string;
    wallet_id: string;
    chain: Chain;
    type: TransactionType;
    from_address: string;
    to_address: string;
    amount: string;
    currency: Currency;
    tx_hash: string;
    status: TransactionStatus;
    chain_fee?: string;
    chain_fee_usd?: string;
    bank_fee?: string;
    bank_fee_usd?: string;
    total_fee?: string;
    total_fee_usd?: string;
    timestamp: string;
}
type TransactionType = 'deposit' | 'transfer' | 'swap' | 'stake' | 'unstake' | 'withdraw';
interface TransactionHistoryResponse {
    wallet_id: string;
    transactions: Transaction[];
}
interface SignMessageRequest {
    message: string;
}
interface SignMessageResponse {
    wallet_id: string;
    address: string;
    message: string;
    signature: string;
}
interface EstimateGasRequest {
    to_address: string;
    amount: string;
}
interface EstimateGasResponse {
    chain: Chain;
    to_address: string;
    amount: string;
    estimated_gas: string;
}
interface SendSafeRequest extends SendTransactionRequest {
    /** Optional: max acceptable gas fee in USD */
    maxGasUSD?: number;
}
interface SendMultipleRequest {
    /** Array of recipients and amounts */
    recipients: Array<{
        to_address: string;
        amount: string;
        currency?: Currency;
    }>;
}
interface SendMultipleResponse {
    results: SendTransactionResponse[];
    totalAmount: string;
    totalFees: string;
    timestamp: string;
}
interface BalanceCheckResponse {
    has_enough_funds: boolean;
    current_balance: string;
    required_amount: string;
    currency?: Currency;
}
interface ChainInfo {
    id: Chain;
    name: string;
    symbol: string;
    nativeToken: Currency;
    decimals: number;
    tokens: Currency[];
    chainId: number | null;
    explorer: string;
}
interface CatalogueResponse {
    chains: ChainInfo[];
}
interface ApiError {
    error: string;
    code?: string;
    details?: Record<string, unknown>;
}
interface FeeEstimate {
    chain_fee: string;
    chain_fee_usd: string;
    bank_fee: string;
    bank_fee_usd: string;
    total_fee: string;
    total_fee_usd: string;
}
interface FeeInfo {
    base_percentage: number;
    min_fee_usd: number;
    max_fee_usd: number;
    chain_multipliers: Record<Chain, number>;
}

/**
 * AgentsBank SDK Client
 * Main API client for interacting with AgentsBank services
 */

declare class AgentsBank {
    private baseUrl;
    private apiKey?;
    private token?;
    private timeout;
    private fetchImpl;
    private retryConfig;
    private guardrails;
    constructor(config?: AgentsBankConfig);
    /**
     * Set JWT token for authentication
     */
    setToken(token: string): void;
    /**
     * Set API key for authentication
     */
    setApiKey(apiKey: string): void;
    /**
     * Get current authentication status
     */
    isAuthenticated(): boolean;
    private getHeaders;
    private request;
    private requestInternal;
    /**
     * Register a new agent (self-registration)
     * Creates both human and agent accounts
     *
     * @example
     * ```ts
     * const result = await client.register({
     *   human_username: 'myuser',
     *   human_email: 'user@example.com',
     *   first_name: 'John',
     *   last_name: 'Doe',
     *   agent_password: 'SecurePass123!'
     * });
     *
     * // Save the token for future requests
     * client.setToken(result.token);
     *
     * // IMPORTANT: Save recovery words securely!
     * console.log(result.recovery_words);
     * ```
     */
    register(request: RegisterAgentRequest): Promise<RegisterAgentResponse>;
    /**
     * Login with agent credentials
     *
     * @example
     * ```ts
     * const result = await client.login({
     *   agent_username: 'agent_123456_abc',
     *   agent_password: 'SecurePass123!'
     * });
     *
     * client.setToken(result.token);
     * ```
     */
    login(request: LoginRequest): Promise<LoginResponse>;
    /**
     * Refresh the JWT token
     */
    refreshToken(): Promise<{
        token: string;
    }>;
    /**
     * Create a new wallet on the specified chain
     *
     * @example
     * ```ts
     * const wallet = await client.createWallet('solana');
     * console.log(wallet.address); // Solana address
     * ```
     */
    createWallet(chain: Chain): Promise<CreateWalletResponse>;
    /**
     * Get wallet details by ID
     */
    getWallet(walletId: string): Promise<WalletInfo>;
    /**
     * Get wallet balance (fetches from blockchain)
     *
     * @example
     * ```ts
     * const { balance } = await client.getBalance(walletId);
     * console.log(`SOL: ${balance.SOL}`);
     * console.log(`USDC: ${balance.USDC}`);
     * ```
     */
    getBalance(walletId: string): Promise<GetBalanceResponse>;
    /**
     * Get transaction history for a wallet
     */
    getTransactionHistory(walletId: string, limit?: number): Promise<TransactionHistoryResponse>;
    /**
     * Send a transaction from a wallet
     *
     * @example
     * ```ts
     * // Send native token (SOL, ETH, BNB, BTC)
     * const tx = await client.send(walletId, {
     *   to_address: 'recipient_address',
     *   amount: '0.1'
     * });
     *
     * // Send token (USDC, USDT)
     * const tx = await client.send(walletId, {
     *   to_address: 'recipient_address',
     *   amount: '100',
     *   currency: 'USDC'
     * });
     * ```
     */
    send(walletId: string, request: SendTransactionRequest): Promise<SendTransactionResponse>;
    /**
     * Estimate gas/fees for a transaction
     */
    estimateGas(walletId: string, toAddress: string, amount: string): Promise<EstimateGasResponse>;
    /**
     * Sign a message with wallet's private key
     * Useful for authentication with external services
     *
     * @example
     * ```ts
     * const { signature } = await client.signMessage(walletId, 'Hello, World!');
     * // Use signature to prove ownership of the address
     * ```
     */
    signMessage(walletId: string, message: string): Promise<SignMessageResponse>;
    /**
     * Get supported chains and tokens
     */
    getCatalogue(): Promise<CatalogueResponse>;
    /**
     * Check API health status
     */
    health(): Promise<{
        status: string;
        timestamp: string;
        version: string;
    }>;
    /**
     * Check if wallet has enough funds for a transaction
     * Includes guardrail validation
     *
     * @example
     * ```ts
     * const hasEnough = await client.hasEnoughFunds(walletId, '1.0');
     * if (!hasEnough.has_enough_funds) {
     *   console.log('Insufficient balance:', hasEnough.current_balance);
     * }
     * ```
     */
    hasEnoughFunds(walletId: string, amount: string): Promise<BalanceCheckResponse>;
    /**
     * Send transaction with pre-flight checks (recommended for production)
     * Includes auto-retry, balance validation, guardrail checks
     *
     * @example
     * ```ts
     * const tx = await client.sendSafe(walletId, {
     *   to_address: 'recipient',
     *   amount: '1.0',
     *   maxGasUSD: 100
     * });
     * ```
     */
    sendSafe(walletId: string, request: SendSafeRequest): Promise<SendTransactionResponse>;
    /**
     * Send transactions to multiple recipients
     * Batch operation for efficiency
     *
     * @example
     * ```ts
     * const results = await client.sendMultiple(walletId, {
     *   recipients: [
     *     { to_address: '0x111...', amount: '1.0' },
     *     { to_address: '0x222...', amount: '2.0' }
     *   ]
     * });
     * ```
     */
    sendMultiple(walletId: string, request: SendMultipleRequest): Promise<SendMultipleResponse>;
    /**
     * Validate transaction against guardrails
     * @private
     */
    private validateGuardrails;
}
/**
 * Create a new AgentsBank client instance
 *
 * @example
 * ```ts
 * import { createClient } from '@agentsbank/sdk';
 *
 * const client = createClient({
 *   apiKey: 'your-api-key'
 * });
 *
 * // Or with token
 * const client = createClient({
 *   token: 'your-jwt-token'
 * });
 * ```
 */
declare function createClient(config?: AgentsBankConfig): AgentsBank;

/**
 * AgentsBank SDK Typed Errors
 * 19 specific error codes for precise error handling
 */
declare enum ErrorCode {
    INVALID_ADDRESS = "INVALID_ADDRESS",
    INVALID_AMOUNT = "INVALID_AMOUNT",
    INVALID_CHAIN = "INVALID_CHAIN",
    INVALID_CURRENCY = "INVALID_CURRENCY",
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS",
    UNAUTHORIZED = "UNAUTHORIZED",
    FORBIDDEN = "FORBIDDEN",
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS",
    SESSION_EXPIRED = "SESSION_EXPIRED",
    NOT_FOUND = "NOT_FOUND",
    RESOURCE_EXISTS = "RESOURCE_EXISTS",
    CONFLICT = "CONFLICT",
    RATE_LIMITED = "RATE_LIMITED",
    TIMEOUT = "TIMEOUT",
    NETWORK_ERROR = "NETWORK_ERROR",
    INTERNAL_ERROR = "INTERNAL_ERROR",
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE",
    GUARDRAIL_VIOLATION = "GUARDRAIL_VIOLATION",
    RETRY_FAILED = "RETRY_FAILED"
}
/**
 * Extended AgentsBank error with typed codes
 */
declare class AgentsBankError extends Error {
    readonly code: ErrorCode;
    readonly status: number;
    readonly details?: Record<string, unknown>;
    readonly retryable: boolean;
    constructor(message: string, code: ErrorCode, status?: number, details?: Record<string, unknown>, retryable?: boolean);
    /**
     * Check if error is retryable (transient failure)
     */
    isRetryable(): boolean;
    /**
     * Convert to JSON for logging/serialization
     */
    toJSON(): {
        name: string;
        message: string;
        code: ErrorCode;
        status: number;
        details: Record<string, unknown> | undefined;
        retryable: boolean;
    };
}
/**
 * Error factory for creating typed errors
 */
declare const createError: (message: string, code: ErrorCode, status?: number, details?: Record<string, unknown>) => AgentsBankError;
/**
 * Helper to detect error code from HTTP status
 */
declare const errorCodeFromStatus: (status: number) => ErrorCode;

/**
 * AgentsBank SDK
 * Official TypeScript/JavaScript SDK for AgentsBank.ai
 *
 * @packageDocumentation
 */

declare const VERSION = "1.0.5";
declare const SUPPORTED_CHAINS: readonly string[];
declare const SUPPORTED_CURRENCIES: readonly string[];

export { AgentsBank, type AgentsBankConfig, AgentsBankError, type ApiError, type BalanceCheckResponse, type CacheConfig, type CatalogueResponse, type Chain, type ChainInfo, type CreateWalletRequest, type CreateWalletResponse, type Currency, ErrorCode, type EstimateGasRequest, type EstimateGasResponse, type FeeEstimate, type FeeInfo, type GetBalanceResponse, type GuardrailsConfig, type LoginRequest, type LoginResponse, type RegisterAgentRequest, type RegisterAgentResponse, type RetryConfig, SUPPORTED_CHAINS, SUPPORTED_CURRENCIES, type SendMultipleRequest, type SendMultipleResponse, type SendSafeRequest, type SendTransactionRequest, type SendTransactionResponse, type SignMessageRequest, type SignMessageResponse, type Transaction, type TransactionHistoryResponse, type TransactionStatus, type TransactionType, VERSION, type WalletBalance, type WalletInfo, type WebhookConfig, type WebhookEvent, createClient, createError, errorCodeFromStatus };
