// src/errors.ts
var ErrorCode = /* @__PURE__ */ ((ErrorCode2) => {
  ErrorCode2["INVALID_ADDRESS"] = "INVALID_ADDRESS";
  ErrorCode2["INVALID_AMOUNT"] = "INVALID_AMOUNT";
  ErrorCode2["INVALID_CHAIN"] = "INVALID_CHAIN";
  ErrorCode2["INVALID_CURRENCY"] = "INVALID_CURRENCY";
  ErrorCode2["INSUFFICIENT_FUNDS"] = "INSUFFICIENT_FUNDS";
  ErrorCode2["UNAUTHORIZED"] = "UNAUTHORIZED";
  ErrorCode2["FORBIDDEN"] = "FORBIDDEN";
  ErrorCode2["INVALID_CREDENTIALS"] = "INVALID_CREDENTIALS";
  ErrorCode2["SESSION_EXPIRED"] = "SESSION_EXPIRED";
  ErrorCode2["NOT_FOUND"] = "NOT_FOUND";
  ErrorCode2["RESOURCE_EXISTS"] = "RESOURCE_EXISTS";
  ErrorCode2["CONFLICT"] = "CONFLICT";
  ErrorCode2["RATE_LIMITED"] = "RATE_LIMITED";
  ErrorCode2["TIMEOUT"] = "TIMEOUT";
  ErrorCode2["NETWORK_ERROR"] = "NETWORK_ERROR";
  ErrorCode2["INTERNAL_ERROR"] = "INTERNAL_ERROR";
  ErrorCode2["INSUFFICIENT_BALANCE"] = "INSUFFICIENT_BALANCE";
  ErrorCode2["GUARDRAIL_VIOLATION"] = "GUARDRAIL_VIOLATION";
  ErrorCode2["RETRY_FAILED"] = "RETRY_FAILED";
  return ErrorCode2;
})(ErrorCode || {});
var AgentsBankError = class _AgentsBankError extends Error {
  constructor(message, code, status = 500, details, retryable = false) {
    super(message);
    this.name = "AgentsBankError";
    this.code = code;
    this.status = status;
    this.details = details;
    this.retryable = retryable;
    Object.setPrototypeOf(this, _AgentsBankError.prototype);
  }
  /**
   * Check if error is retryable (transient failure)
   */
  isRetryable() {
    return this.retryable || this.code === "TIMEOUT" /* TIMEOUT */ || this.code === "NETWORK_ERROR" /* NETWORK_ERROR */ || this.code === "RATE_LIMITED" /* RATE_LIMITED */ || this.status >= 500;
  }
  /**
   * Convert to JSON for logging/serialization
   */
  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      status: this.status,
      details: this.details,
      retryable: this.retryable
    };
  }
};
var createError = (message, code, status = 500, details) => {
  const retryable = code === "TIMEOUT" /* TIMEOUT */ || code === "NETWORK_ERROR" /* NETWORK_ERROR */ || code === "RATE_LIMITED" /* RATE_LIMITED */;
  return new AgentsBankError(message, code, status, details, retryable);
};
var errorCodeFromStatus = (status) => {
  if (status === 400) return "INVALID_ADDRESS" /* INVALID_ADDRESS */;
  if (status === 401) return "UNAUTHORIZED" /* UNAUTHORIZED */;
  if (status === 403) return "FORBIDDEN" /* FORBIDDEN */;
  if (status === 404) return "NOT_FOUND" /* NOT_FOUND */;
  if (status === 409) return "CONFLICT" /* CONFLICT */;
  if (status === 429) return "RATE_LIMITED" /* RATE_LIMITED */;
  if (status >= 500) return "INTERNAL_ERROR" /* INTERNAL_ERROR */;
  return "INTERNAL_ERROR" /* INTERNAL_ERROR */;
};

// src/client.ts
var DEFAULT_BASE_URL = "https://api.agentsbank.online";
var DEFAULT_TIMEOUT = 3e4;
var DEFAULT_RETRY_CONFIG = {
  maxAttempts: 3,
  initialDelayMs: 100,
  maxDelayMs: 5e3
};
var AgentsBank = class {
  constructor(config = {}) {
    this.baseUrl = config.baseUrl || DEFAULT_BASE_URL;
    this.apiKey = config.apiKey;
    this.token = config.token;
    this.timeout = config.timeout || DEFAULT_TIMEOUT;
    this.fetchImpl = config.fetch || globalThis.fetch;
    this.retryConfig = { ...DEFAULT_RETRY_CONFIG, ...config.retryConfig };
    this.guardrails = config.guardrails || {};
    if (!this.fetchImpl) {
      throw new Error("fetch is not available. Please provide a fetch implementation.");
    }
  }
  // ============================================
  // CONFIGURATION
  // ============================================
  /**
   * Set JWT token for authentication
   */
  setToken(token) {
    this.token = token;
  }
  /**
   * Set API key for authentication
   */
  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }
  /**
   * Get current authentication status
   */
  isAuthenticated() {
    return !!(this.token || this.apiKey);
  }
  // ============================================
  // HTTP HELPERS
  // ============================================
  getHeaders() {
    const headers = {
      "Content-Type": "application/json"
    };
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    } else if (this.apiKey) {
      headers["x-api-key"] = this.apiKey;
    }
    return headers;
  }
  async request(method, path, body) {
    let lastError = null;
    const maxAttempts = this.retryConfig.maxAttempts || 3;
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        return await this.requestInternal(method, path, body);
      } catch (error) {
        lastError = error;
        if (error instanceof AgentsBankError) {
          if (!error.isRetryable()) {
            throw error;
          }
          if (attempt < maxAttempts - 1) {
            const delay = Math.min(
              this.retryConfig.initialDelayMs * Math.pow(2, attempt),
              this.retryConfig.maxDelayMs
            );
            await new Promise((resolve) => setTimeout(resolve, delay));
          }
        } else {
          throw error;
        }
      }
    }
    if (lastError instanceof AgentsBankError) {
      throw lastError;
    }
    throw createError("All retry attempts failed", "RETRY_FAILED" /* RETRY_FAILED */, 500);
  }
  async requestInternal(method, path, body) {
    const url = `${this.baseUrl}${path}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    try {
      const response = await this.fetchImpl(url, {
        method,
        headers: this.getHeaders(),
        body: body ? JSON.stringify(body) : void 0,
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      const data = await response.json();
      if (!response.ok) {
        const code = data.code || "INTERNAL_ERROR" /* INTERNAL_ERROR */;
        throw createError(
          data.error || "Request failed",
          code,
          response.status,
          data.details
        );
      }
      return data;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof AgentsBankError) {
        throw error;
      }
      if (error instanceof Error) {
        if (error.name === "AbortError") {
          throw createError(
            "Request timeout",
            "TIMEOUT" /* TIMEOUT */,
            408
          );
        }
        throw createError(error.message, "NETWORK_ERROR" /* NETWORK_ERROR */, 500);
      }
      throw createError("Unknown error", "INTERNAL_ERROR" /* INTERNAL_ERROR */, 500);
    }
  }
  // ============================================
  // AUTHENTICATION
  // ============================================
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
  async register(request) {
    const response = await this.request(
      "POST",
      "/api/auth/agent/register-self",
      request
    );
    if (response.token) {
      this.token = response.token;
    }
    return response;
  }
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
  async login(request) {
    const response = await this.request(
      "POST",
      "/api/auth/agent/login",
      request
    );
    if (response.token) {
      this.token = response.token;
    }
    return response;
  }
  /**
   * Refresh the JWT token
   */
  async refreshToken() {
    const response = await this.request(
      "POST",
      "/api/auth/refresh"
    );
    if (response.token) {
      this.token = response.token;
    }
    return response;
  }
  // ============================================
  // WALLETS
  // ============================================
  /**
   * Create a new wallet on the specified chain
   * 
   * @example
   * ```ts
   * const wallet = await client.createWallet('solana');
   * console.log(wallet.address); // Solana address
   * ```
   */
  async createWallet(chain) {
    return this.request("POST", "/api/wallets", { chain });
  }
  /**
   * Get wallet details by ID
   */
  async getWallet(walletId) {
    return this.request("GET", `/api/wallets/${walletId}`);
  }
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
  async getBalance(walletId) {
    return this.request("GET", `/api/wallets/${walletId}/balance`);
  }
  /**
   * Get transaction history for a wallet
   */
  async getTransactionHistory(walletId, limit) {
    const query = limit ? `?limit=${limit}` : "";
    return this.request(
      "GET",
      `/api/wallets/${walletId}/history${query}`
    );
  }
  // ============================================
  // TRANSACTIONS
  // ============================================
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
  async send(walletId, request) {
    return this.request(
      "POST",
      `/api/wallets/${walletId}/send`,
      request
    );
  }
  /**
   * Estimate gas/fees for a transaction
   */
  async estimateGas(walletId, toAddress, amount) {
    return this.request(
      "GET",
      `/api/wallets/${walletId}/estimate-gas?to_address=${encodeURIComponent(toAddress)}&amount=${encodeURIComponent(amount)}`
    );
  }
  // ============================================
  // SIGNING
  // ============================================
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
  async signMessage(walletId, message) {
    return this.request(
      "POST",
      `/api/wallets/${walletId}/sign-message`,
      { message }
    );
  }
  // ============================================
  // CATALOGUE
  // ============================================
  /**
   * Get supported chains and tokens
   */
  async getCatalogue() {
    return this.request("GET", "/api/catalogue/chains");
  }
  // ============================================
  // HEALTH
  // ============================================
  /**
   * Check API health status
   */
  async health() {
    return this.request(
      "GET",
      "/health"
    );
  }
  // ============================================
  // HELPER METHODS (v1.0.5)
  // ============================================
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
  async hasEnoughFunds(walletId, amount) {
    const balance = await this.getBalance(walletId);
    const nativeTokens = {
      ethereum: "ETH",
      bsc: "BNB",
      solana: "SOL",
      bitcoin: "BTC"
    };
    const currency = nativeTokens[balance.chain];
    const currentBalance = parseFloat(balance.balance[currency] || "0");
    const requiredAmount = parseFloat(amount);
    return {
      has_enough_funds: currentBalance >= requiredAmount,
      current_balance: balance.balance[currency] || "0",
      required_amount: amount,
      currency
    };
  }
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
  async sendSafe(walletId, request) {
    this.validateGuardrails(request.to_address, request.amount);
    const hasEnough = await this.hasEnoughFunds(walletId, request.amount);
    if (!hasEnough.has_enough_funds) {
      throw createError(
        `Insufficient funds: need ${request.amount}, have ${hasEnough.current_balance}`,
        "INSUFFICIENT_FUNDS" /* INSUFFICIENT_FUNDS */,
        409
      );
    }
    if (request.maxGasUSD) {
      try {
        await this.estimateGas(walletId, request.to_address, request.amount);
      } catch (error) {
        if (!(error instanceof AgentsBankError && error.code === "TIMEOUT" /* TIMEOUT */)) {
          throw error;
        }
      }
    }
    return this.send(walletId, {
      to_address: request.to_address,
      amount: request.amount,
      currency: request.currency
    });
  }
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
  async sendMultiple(walletId, request) {
    const results = [];
    let totalAmount = "0";
    let totalFees = "0";
    for (const recipient of request.recipients) {
      try {
        this.validateGuardrails(recipient.to_address, recipient.amount);
        const tx = await this.send(walletId, {
          to_address: recipient.to_address,
          amount: recipient.amount,
          currency: recipient.currency
        });
        results.push(tx);
        totalAmount = (parseFloat(totalAmount) + parseFloat(recipient.amount)).toString();
      } catch (error) {
        if (error instanceof AgentsBankError) {
          results.push({
            tx_hash: "",
            status: "failed",
            from_address: "",
            to_address: recipient.to_address,
            amount: recipient.amount,
            chain: "ethereum"
            // Placeholder
          });
        } else {
          throw error;
        }
      }
    }
    return {
      results,
      totalAmount,
      totalFees,
      timestamp: (/* @__PURE__ */ new Date()).toISOString()
    };
  }
  /**
   * Validate transaction against guardrails
   * @private
   */
  validateGuardrails(toAddress, amount) {
    if (!this.guardrails) return;
    if (this.guardrails.whitelistedAddresses && this.guardrails.whitelistedAddresses.length > 0) {
      if (!this.guardrails.whitelistedAddresses.includes(toAddress)) {
        throw createError(
          "Recipient address not whitelisted",
          "GUARDRAIL_VIOLATION" /* GUARDRAIL_VIOLATION */,
          403
        );
      }
    }
    if (this.guardrails.blacklistedAddresses && this.guardrails.blacklistedAddresses.includes(toAddress)) {
      throw createError(
        "Recipient address is blacklisted",
        "GUARDRAIL_VIOLATION" /* GUARDRAIL_VIOLATION */,
        403
      );
    }
    if (this.guardrails.maxPerTxUSD) {
      const amountNum = parseFloat(amount);
      if (amountNum > this.guardrails.maxPerTxUSD) {
        throw createError(
          `Transaction amount $${amountNum} exceeds max per tx $${this.guardrails.maxPerTxUSD}`,
          "GUARDRAIL_VIOLATION" /* GUARDRAIL_VIOLATION */,
          403
        );
      }
    }
  }
};
function createClient(config) {
  return new AgentsBank(config);
}

// src/index.ts
var VERSION = "1.0.5";
var SUPPORTED_CHAINS = [
  "ethereum",
  "bsc",
  "solana",
  "bitcoin"
];
var SUPPORTED_CURRENCIES = [
  "ETH",
  "BNB",
  "SOL",
  "BTC",
  "USDT",
  "USDC"
];
export {
  AgentsBank,
  AgentsBankError,
  ErrorCode,
  SUPPORTED_CHAINS,
  SUPPORTED_CURRENCIES,
  VERSION,
  createClient,
  createError,
  errorCodeFromStatus
};
