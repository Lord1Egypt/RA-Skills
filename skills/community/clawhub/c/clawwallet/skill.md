/**
 * CLAWwallet Multi-Agent Skill - Enhanced Version
 * 
 * A universal skill that works with ANY AI agent framework!
 * Supports: OpenClaw, LangChain, AutoGen, CrewAI, Custom agents, and more!
 * 
 * Documentation: https://clawwallet.pages.dev
 * 
 * Capabilities:
 * - 15+ Blockchains (Base, Ethereum, Solana, Aptos, Sui, StarkNet, Polygon zkEVM, zkSync, etc.)
 * - DeFi: Swaps, Staking, Lending, Cross-chain
 * - Multi-sig Wallets
 * - Policy Engine (Guardrails)
 * - ENS Registration
 * - Agent Identity (ERC-8004)
 * - Webhooks & WebSockets
 * 
 * @author Mr. Claw
 * @version 2.0.0
 */

import { randomUUID } from 'crypto';

// ============================================================
// Configuration
// ============================================================

const DEFAULT_CONFIG = {
  walletServiceUrl: process.env.CLAW_WALLET_URL || 'http://localhost:3000',
  apiKey: process.env.CLAW_WALLET_API_KEY,
  defaultChain: process.env.CLAW_WALLET_CHAIN || 'base-sepolia',
  autoRegister: true,
  enablePayments: true,
};

// Supported chains (from CLAWwallet docs)
const SUPPORTED_CHAINS = {
  EVM: ['ethereum', 'base', 'base-sepolia', 'arbitrum', 'optimism', 'polygon', 'avalanche', 'bsc', 'sepolia'],
  NON_EVM: ['solana', 'aptos', 'sui', 'starknet', 'polygon-zkevm', 'zksync'],
};

// ============================================================
// Skill State
// ============================================================

class MultiWalletSkill {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.wallets = new Map(); // agentName -> wallet info
    this.initialized = false;
  }

  /**
   * Initialize the skill
   */
  async initialize(context = {}) {
    console.log('🦞 CLAWwallet Multi-Agent Skill v2.0 initializing...');
    
    // Store context for later use
    this.context = context;
    
    // Test connection to wallet service
    try {
      const health = await this._request('/health');
      console.log(`✅ Wallet service healthy: ${health.status}`);
    } catch (error) {
      console.warn('⚠️ Wallet service not reachable:', error.message);
    }

    this.initialized = true;
    return {
      name: 'CLAWwallet',
      version: '2.0.0',
      description: 'Enterprise wallet infrastructure for AI agents - multi-chain, DeFi, policy guardrails',
      documentation: 'https://clawwallet.pages.dev',
      capabilities: [
        // Wallet Operations
        'create_wallet',
        'import_wallet',
        'get_balance',
        'get_token_balances',
        'send_payment',
        'send_token',
        'sweep_wallet',
        'estimate_gas',
        'get_transaction_receipt',
        
        // Multi-Chain
        'get_supported_chains',
        'switch_chain',
        
        // DeFi - Swaps
        'swap_tokens',
        'get_swap_quote',
        'get_best_quote',
        
        // DeFi - Staking
        'stake_eth',
        'unstake_eth',
        'get_staking_positions',
        'stake_lido',
        'unstake_lido',
        
        // DeFi - Lending
        'supply_to_lending',
        'borrow_from_lending',
        'repay_lending',
        'withdraw_from_lending',
        'get_lending_positions',
        
        // DeFi - Cross-chain
        'cross_chain_transfer',
        'send_via_layerzero',
        'send_via_axelar',
        
        // DeFi - Price Feeds
        'get_price',
        'token_to_usd',
        'usd_to_token',
        
        // Multi-Sig
        'create_multisig',
        'submit_multisig_transaction',
        'confirm_multisig_transaction',
        'execute_multisig_transaction',
        'get_multisig_transactions',
        
        // Policy Engine
        'set_policy',
        'get_policy',
        'apply_policy_preset',
        'check_approval_status',
        
        // ENS
        'check_ens_availability',
        'get_ens_price',
        'register_ens',
        
        // Agent Registry
        'register_agent',
        'get_agent',
        'list_agents',
        'search_agents',
        'pay_agent',
        'get_agent_balance',
        
        // Services Marketplace
        'get_services',
        'add_service',
        'get_economy_stats',
        
        // Identity
        'create_identity',
        'link_social_account',
        
        // Webhooks
        'register_webhook',
        'list_webhooks',
        'delete_webhook',
        
        // Transaction History
        'get_transaction_history',
        'get_wallet_activity',
        
        // Utilities
        'get_doctor_diagnostics',
      ],
      supportedChains: SUPPORTED_CHAINS,
    };
  }

  // ============================================================
  // Wallet Operations
  // ============================================================

  /**
   * Create a wallet for an agent
   * @param {string} agentName - Name of the agent
   * @param {string} chain - Blockchain chain (default: base-sepolia)
   */
  async createWallet(agentName, chain = this.config.defaultChain) {
    const response = await this._request('/wallet/create', {
      method: 'POST',
      body: { agentName, chain },
    });

    const wallet = response.wallet;
    
    // Store locally
    this.wallets.set(agentName, {
      address: wallet.address,
      chain: wallet.chain,
      id: wallet.id,
    });

    return {
      success: true,
      agentName,
      address: wallet.address,
      chain: wallet.chain,
      message: `Wallet created for ${agentName} on ${chain}`,
    };
  }

  /**
   * Import an existing wallet
   * @param {string} privateKey - Wallet private key
   * @param {string} agentName - Name of the agent
   * @param {string} chain - Blockchain chain
   */
  async importWallet(privateKey, agentName, chain = this.config.defaultChain) {
    const response = await this._request('/wallet/import', {
      method: 'POST',
      body: { privateKey, agentName, chain },
    });

    const wallet = response.wallet;
    
    this.wallets.set(agentName, {
      address: wallet.address,
      chain: wallet.chain,
      id: wallet.id,
    });

    return {
      success: true,
      agentName,
      address: wallet.address,
      chain: wallet.chain,
      message: `Wallet imported for ${agentName}`,
    };
  }

  /**
   * Get wallet balance (native + tokens)
   * @param {string} address - Wallet address
   * @param {string} chain - Blockchain chain
   */
  async getBalance(address, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/${address}/balance?chain=${chain}`);
    
    return {
      address,
      chain: response.balance.chain,
      eth: response.balance.eth,
      rpc: response.balance.rpc,
    };
  }

  /**
   * Get all token balances for a wallet
   * @param {string} address - Wallet address
   * @param {string} chain - Blockchain chain
   */
  async getTokenBalances(address, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/${address}/tokens?chain=${chain}`);
    return response.tokens || [];
  }

  /**
   * Send payment from wallet
   * @param {string} fromAddress - Sender wallet address
   * @param {string} toAddress - Recipient wallet address  
   * @param {string} amount - Amount in ETH
   * @param {string} chain - Blockchain chain
   */
  async sendPayment(fromAddress, toAddress, amount, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/${fromAddress}/send`, {
      method: 'POST',
      body: {
        to: toAddress,
        value: amount,
        chain,
      },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      from: fromAddress,
      to: toAddress,
      amount,
      chain,
      message: `Sent ${amount} ETH from ${fromAddress.slice(0, 8)}... to ${toAddress.slice(0, 8)}...`,
    };
  }

  /**
   * Send ERC-20 token
   * @param {string} fromAddress - Sender wallet address
   * @param {string} toAddress - Recipient address
   * @param {string} tokenAddress - ERC-20 token contract address
   * @param {string} amount - Amount to send
   * @param {string} chain - Blockchain chain
   */
  async sendToken(fromAddress, toAddress, tokenAddress, amount, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/${fromAddress}/send-token`, {
      method: 'POST',
      body: {
        to: toAddress,
        token: tokenAddress,
        amount,
        chain,
      },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      from: fromAddress,
      to: toAddress,
      token: tokenAddress,
      amount,
      chain,
    };
  }

  /**
   * Sweep all funds to another address
   * @param {string} fromAddress - Source wallet address
   * @param {string} toAddress - Destination address
   * @param {string} chain - Blockchain chain
   */
  async sweepWallet(fromAddress, toAddress, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/${fromAddress}/sweep`, {
      method: 'POST',
      body: { to: toAddress, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      from: fromAddress,
      to: toAddress,
      amount: response.swept,
      chain,
    };
  }

  /**
   * Estimate gas for a transaction
   * @param {string} from - From address
   * @param {string} to - To address
   * @param {string} value - Amount in ETH
   * @param {string} chain - Blockchain chain
   */
  async estimateGas(from, to, value = '0', chain = this.config.defaultChain) {
    const response = await this._request('/wallet/estimate-gas', {
      method: 'POST',
      body: { from, to, value, chain },
    });

    return response.estimate;
  }

  /**
   * Get transaction receipt
   * @param {string} txHash - Transaction hash
   * @param {string} chain - Blockchain chain
   */
  async getTransactionReceipt(txHash, chain = this.config.defaultChain) {
    const response = await this._request(`/wallet/tx/${txHash}?chain=${chain}`);
    return response.receipt;
  }

  /**
   * Get wallet address for an agent
   * @param {string} agentName - Name of the agent
   */
  async getWallet(agentName) {
    const wallet = this.wallets.get(agentName);
    if (wallet) return wallet;

    // Try to get from service
    const response = await this._request('/wallet');
    const wallets = response.wallets || [];
    
    for (const w of wallets) {
      if (w.agentName === agentName) {
        return {
          address: w.address,
          chain: w.chain,
          id: w.id,
        };
      }
    }

    return null;
  }

  // ============================================================
  // Multi-Chain Operations
  // ============================================================

  /**
   * Get list of supported chains
   */
  async getSupportedChains() {
    const response = await this._request('/chains');
    return response.chains || SUPPORTED_CHAINS;
  }

  /**
   * Get chain configuration
   * @param {string} chain - Chain name
   */
  async getChainConfig(chain) {
    const response = await this._request(`/chains/${chain}`);
    return response.config;
  }

  // ============================================================
  // DeFi - Swaps
  // ============================================================

  /**
   * Get swap quote from DEX
   * @param {string} fromToken - Source token address or symbol
   * @param {string} toToken - Destination token address or symbol
   * @param {string} amount - Amount to swap
   * @param {string} chain - Blockchain chain
   */
  async getSwapQuote(fromToken, toToken, amount, chain = this.config.defaultChain) {
    const response = await this._request('/defi/swap/quote', {
      method: 'POST',
      body: { fromToken, toToken, amount, chain },
    });

    return response.quote;
  }

  /**
   * Get best quote across all DEXs
   * @param {string} fromToken - Source token
   * @param {string} toToken - Destination token
   * @param {string} amount - Amount
   * @param {string} chain - Blockchain chain
   */
  async getBestQuote(fromToken, toToken, amount, chain = this.config.defaultChain) {
    const response = await this._request('/defi/swap/best-quote', {
      method: 'POST',
      body: { fromToken, toToken, amount, chain },
    });

    return response.quote;
  }

  /**
   * Execute token swap
   * @param {string} walletAddress - User wallet
   * @param {string} fromToken - Source token
   * @param {string} toToken - Destination token
   * @param {string} amount - Amount to swap
   * @param {string} chain - Blockchain chain
   */
  async swapTokens(walletAddress, fromToken, toToken, amount, chain = this.config.defaultChain) {
    const response = await this._request('/defi/swap/execute', {
      method: 'POST',
      body: { walletAddress, fromToken, toToken, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      fromToken,
      toToken,
      amount,
      chain,
    };
  }

  // ============================================================
  // DeFi - Staking
  // ============================================================

  /**
   * Stake ETH (Lido)
   * @param {string} walletAddress - User wallet
   * @param {string} amount - Amount in ETH
   * @param {string} chain - Blockchain chain (ethereum, etc.)
   */
  async stakeEth(walletAddress, amount, chain = 'ethereum') {
    const response = await this._request('/defi/stake/lido', {
      method: 'POST',
      body: { walletAddress, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      stakedAmount: response.staked,
      chain,
    };
  }

  /**
   * Unstake ETH (Lido)
   * @param {string} walletAddress - User wallet
   * @param {string} amount - Amount to unstake
   * @param {string} chain - Blockchain chain
   */
  async unstakeEth(walletAddress, amount, chain = 'ethereum') {
    const response = await this._request('/defi/stake/lido/unstake', {
      method: 'POST',
      body: { walletAddress, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      chain,
    };
  }

  /**
   * Get staking positions
   * @param {string} walletAddress - User wallet
   * @param {string} chain - Blockchain chain
   */
  async getStakingPositions(walletAddress, chain = 'ethereum') {
    const response = await this._request(`/defi/stake/positions/${walletAddress}?chain=${chain}`);
    return response.positions || [];
  }

  /**
   * Alias for stakeEth (Lido)
   */
  async stakeLido(walletAddress, amount, chain = 'ethereum') {
    return this.stakeEth(walletAddress, amount, chain);
  }

  /**
   * Alias for unstakeEth (Lido)
   */
  async unstakeLido(walletAddress, amount, chain = 'ethereum') {
    return this.unstakeEth(walletAddress, amount, chain);
  }

  // ============================================================
  // DeFi - Lending
  // ============================================================

  /**
   * Supply assets to lending protocol (Aave)
   * @param {string} walletAddress - User wallet
   * @param {string} asset - Token address
   * @param {string} amount - Amount to supply
   * @param {string} chain - Blockchain chain
   */
  async supplyToLending(walletAddress, asset, amount, chain = 'ethereum') {
    const response = await this._request('/defi/lending/supply', {
      method: 'POST',
      body: { walletAddress, asset, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      supplied: amount,
      chain,
    };
  }

  /**
   * Borrow from lending protocol (Aave)
   * @param {string} walletAddress - User wallet
   * @param {string} asset - Token to borrow
   * @param {string} amount - Amount to borrow
   * @param {string} chain - Blockchain chain
   */
  async borrowFromLending(walletAddress, asset, amount, chain = 'ethereum') {
    const response = await this._request('/defi/lending/borrow', {
      method: 'POST',
      body: { walletAddress, asset, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      borrowed: amount,
      chain,
    };
  }

  /**
   * Repay lending debt
   * @param {string} walletAddress - User wallet
   * @param {string} asset - Token to repay
   * @param {string} amount - Amount to repay
   * @param {string} chain - Blockchain chain
   */
  async repayLending(walletAddress, asset, amount, chain = 'ethereum') {
    const response = await this._request('/defi/lending/repay', {
      method: 'POST',
      body: { walletAddress, asset, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      repaid: amount,
      chain,
    };
  }

  /**
   * Withdraw from lending protocol
   * @param {string} walletAddress - User wallet
   * @param {string} asset - Token to withdraw
   * @param {string} amount - Amount to withdraw
   * @param {string} chain - Blockchain chain
   */
  async withdrawFromLending(walletAddress, asset, amount, chain = 'ethereum') {
    const response = await this._request('/defi/lending/withdraw', {
      method: 'POST',
      body: { walletAddress, asset, amount, chain },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      withdrawn: amount,
      chain,
    };
  }

  /**
   * Get lending positions
   * @param {string} walletAddress - User wallet
   * @param {string} chain - Blockchain chain
   */
  async getLendingPositions(walletAddress, chain = 'ethereum') {
    const response = await this._request(`/defi/lending/positions/${walletAddress}?chain=${chain}`);
    return response.positions || [];
  }

  // ============================================================
  // DeFi - Cross-Chain
  // ============================================================

  /**
   * Execute cross-chain transfer
   * @param {string} walletAddress - User wallet
   * @param {string} to - Destination address
   * @param {string} amount - Amount to transfer
   * @param {string} sourceChain - Source chain
   * @param {string} destChain - Destination chain
   * @param {string} protocol - Protocol (layerzero, axelar)
   */
  async crossChainTransfer(walletAddress, to, amount, sourceChain, destChain, protocol = 'layerzero') {
    const response = await this._request('/defi/crosschain/transfer', {
      method: 'POST',
      body: { walletAddress, to, amount, sourceChain, destChain, protocol },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      sourceChain,
      destChain,
      protocol,
    };
  }

  /**
   * Send via LayerZero
   */
  async sendViaLayerZero(walletAddress, to, amount, sourceChain, destChain) {
    return this.crossChainTransfer(walletAddress, to, amount, sourceChain, destChain, 'layerzero');
  }

  /**
   * Send via Axelar
   */
  async sendViaAxelar(walletAddress, to, amount, sourceChain, destChain) {
    return this.crossChainTransfer(walletAddress, to, amount, sourceChain, destChain, 'axelar');
  }

  // ============================================================
  // DeFi - Price Feeds
  // ============================================================

  /**
   * Get token price from Chainlink
   * @param {string} token - Token symbol
   * @param {string} chain - Blockchain chain
   */
  async getPrice(token, chain = 'ethereum') {
    const response = await this._request(`/defi/price/${token}?chain=${chain}`);
    return response.price;
  }

  /**
   * Convert token amount to USD
   * @param {string} token - Token symbol
   * @param {string} amount - Token amount
   * @param {string} chain - Blockchain chain
   */
  async tokenToUsd(token, amount, chain = 'ethereum') {
    const response = await this._request('/defi/price/token-to-usd', {
      method: 'POST',
      body: { token, amount, chain },
    });

    return response.usdValue;
  }

  /**
   * Convert USD amount to token
   * @param {string} token - Token symbol
   * @param {string} usdAmount - USD amount
   * @param {string} chain - Blockchain chain
   */
  async usdToToken(token, usdAmount, chain = 'ethereum') {
    const response = await this._request('/defi/price/usd-to-token', {
      method: 'POST',
      body: { token, usdAmount, chain },
    });

    return response.tokenAmount;
  }

  // ============================================================
  // Multi-Sig Wallet
  // ============================================================

  /**
   * Create a multi-sig wallet
   * @param {string[]} owners - List of owner addresses
   * @param {number} threshold - Required signatures
   * @param {string} chain - Blockchain chain
   */
  async createMultisig(owners, threshold, chain = this.config.defaultChain) {
    const response = await this._request('/multisig/create', {
      method: 'POST',
      body: { owners, threshold, chain },
    });

    return {
      success: true,
      address: response.wallet.address,
      owners,
      threshold,
      chain,
    };
  }

  /**
   * Submit transaction to multi-sig
   * @param {string} multisigAddress - Multi-sig wallet address
   * @param {string} to - Recipient address
   * @param {string} value - Amount in ETH
   * @param {string} description - Transaction description
   * @param {string} chain - Blockchain chain
   */
  async submitMultisigTransaction(multisigAddress, to, value, description = '', chain = this.config.defaultChain) {
    const response = await this._request(`/multisig/${multisigAddress}/submit`, {
      method: 'POST',
      body: { to, value, description, chain },
    });

    return {
      success: true,
      txId: response.transaction.id,
      description,
    };
  }

  /**
   * Confirm multi-sig transaction
   * @param {string} txId - Transaction ID
   * @param {string} signerAddress - Signing wallet address
   * @param {string} signature - cryptographic signature
   */
  async confirmMultisigTransaction(txId, signerAddress, signature) {
    const response = await this._request(`/multisig/tx/${txId}/confirm`, {
      method: 'POST',
      body: { signerAddress, signature },
    });

    return {
      success: true,
      confirmations: response.confirmations,
    };
  }

  /**
   * Execute multi-sig transaction
   * @param {string} txId - Transaction ID
   * @param {string} executorAddress - Executor wallet address
   */
  async executeMultisigTransaction(txId, executorAddress) {
    const response = await this._request(`/multisig/tx/${txId}/execute`, {
      method: 'POST',
      body: { executorAddress },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
    };
  }

  /**
   * Get multi-sig transactions
   * @param {string} multisigAddress - Multi-sig wallet address
   * @param {string} status - Filter by status (pending, executed, cancelled)
   */
  async getMultisigTransactions(multisigAddress, status = 'pending') {
    const response = await this._request(`/multisig/${multisigAddress}/transactions?status=${status}`);
    return response.transactions || [];
  }

  // ============================================================
  // Policy Engine (Guardrails)
  // ============================================================

  /**
   * Set policy for a wallet
   * @param {string} walletAddress - Wallet address
   * @param {object} policy - Policy rules
   */
  async setPolicy(walletAddress, policy) {
    const response = await this._request('/policy/set', {
      method: 'POST',
      body: { walletAddress, policy },
    });

    return {
      success: true,
      policy: response.policy,
    };
  }

  /**
   * Get policy for a wallet
   * @param {string} walletAddress - Wallet address
   */
  async getPolicy(walletAddress) {
    const response = await this._request(`/policy/${walletAddress}`);
    return response.policy;
  }

  /**
   * Apply a preset policy
   * @param {string} walletAddress - Wallet address
   * @param {string} presetName - Preset name (strict, moderate, relaxed)
   */
  async applyPolicyPreset(walletAddress, presetName) {
    const response = await this._request('/policy/preset', {
      method: 'POST',
      body: { walletAddress, preset: presetName },
    });

    return {
      success: true,
      policy: response.policy,
    };
  }

  /**
   * Check pending approval status
   * @param {string} approvalId - Approval ID
   */
  async checkApprovalStatus(approvalId) {
    const response = await this._request(`/policy/approval/${approvalId}`);
    return response.status;
  }

  // ============================================================
  // ENS Operations
  // ============================================================

  /**
   * Check ENS name availability
   * @param {string} name - ENS name (without .eth)
   */
  async checkEnsAvailability(name) {
    const response = await this._request(`/ens/check/${name}`);
    return {
      available: response.available,
      name: response.name,
    };
  }

  /**
   * Get ENS registration price
   * @param {string} name - ENS name
   * @param {number} durationYears - Registration duration
   */
  async getEnsPrice(name, durationYears = 1) {
    const response = await this._request('/ens/price', {
      method: 'POST',
      body: { name, duration: durationYears },
    });

    return {
      price: response.price,
      duration: durationYears,
    };
  }

  /**
   * Register ENS name
   * @param {string} walletAddress - Owner wallet
   * @param {string} name - ENS name
   * @param {number} durationYears - Registration duration
   */
  async registerEns(walletAddress, name, durationYears = 1) {
    const response = await this._request('/ens/register', {
      method: 'POST',
      body: { walletAddress, name, duration: durationYears },
    });

    return {
      success: true,
      txHash: response.transaction?.hash,
      name: `${name}.eth`,
      expires: response.expires,
    };
  }

  // ============================================================
  // Agent Registry Operations
  // ============================================================

  /**
   * Register this agent in the universal registry
   * @param {string} agentName - Name of the agent
   * @param {string} agentType - Type of agent (langchain, autogen, crewai, custom, etc.)
   * @param {string} walletAddress - Associated wallet address
   */
  async registerAgent(agentName, agentType = 'custom', walletAddress = null) {
    const response = await this._request('/agents/register', {
      method: 'POST',
      body: {
        agentName,
        agentType,
        metadata: {
          registeredAt: new Date().toISOString(),
          skill: 'CLAWwallet Multi-Agent v2.0',
          framework: this.context?.framework || 'unknown',
          version: '2.0.0',
        },
        walletAddress,
      },
    });

    return {
      success: true,
      agent: response.agent,
      message: `Agent '${agentName}' registered as '${agentType}'`,
    };
  }

  /**
   * Get agent info
   * @param {string} agentName - Name of the agent
   */
  async getAgent(agentName) {
    try {
      const response = await this._request(`/agents/${agentName}`);
      return response.agent;
    } catch (error) {
      return null;
    }
  }

  /**
   * List all registered agents
   */
  async listAgents(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    const response = await this._request(`/agents${params ? '?' + params : ''}`);
    return response.agents || [];
  }

  /**
   * Search for agents
   * @param {string} query - Search query
   */
  async searchAgents(query) {
    const response = await this._request(`/agents/search/${query}`);
    return response.agents || [];
  }

  // ============================================================
  // Agent-to-Agent Payments
  // ============================================================

  /**
   * Pay another agent
   * @param {string} toAgent - Recipient agent name or address
   * @param {string} amount - Amount in ETH
   * @param {string} description - Payment description
   */
  async payAgent(toAgent, amount, description = '') {
    const response = await this._request('/agents/pay', {
      method: 'POST',
      body: {
        toAgent,
        amount: amount.toString(),
        token: 'eth',
        type: 'service',
        description,
      },
    });

    return {
      success: true,
      payment: response.payment,
      instructions: response.instructions,
      message: `Payment of ${amount} ETH queued for ${toAgent}`,
    };
  }

  /**
   * Get agent balance
   * @param {string} agentName - Agent name
   */
  async getAgentBalance(agentName) {
    const response = await this._request(`/agents/${agentName}/balance`);
    return response.balance;
  }

  // ============================================================
  // Service Marketplace
  // ============================================================

  /**
   * List available services from agents
   */
  async getServices() {
    const response = await this._request('/agents/services');
    return response.services || [];
  }

  /**
   * Add a service offering
   * @param {string} agentName - Agent name
   * @param {object} service - Service details
   */
  async addService(agentName, service) {
    const response = await this._request(`/agents/${agentName}/services`, {
      method: 'POST',
      body: service,
    });

    return {
      success: true,
      service: response.service,
    };
  }

  // ============================================================
  // Economy Stats
  // ============================================================

  /**
   * Get economy statistics
   */
  async getEconomyStats() {
    return await this._request('/agents/economy/stats');
  }

  /**
   * Get popular agents
   */
  async getPopularAgents(limit = 10) {
    const response = await this._request(`/agents/popular?limit=${limit}`);
    return response.agents || [];
  }

  // ============================================================
  // Identity (ERC-8004)
  // ============================================================

  /**
   * Create agent identity
   * @param {string} walletAddress - Wallet address
   * @param {string} agentName - Agent name
   * @param {string} description - Agent description
   * @param {string} agentType - Type of agent
   */
  async createIdentity(walletAddress, agentName, description = '', agentType = 'assistant') {
    const response = await this._request('/identity/create', {
      method: 'POST',
      body: {
        walletAddress,
        agentName,
        description,
        agentType,
      },
    });

    return {
      success: true,
      identity: response.identity,
    };
  }

  // ============================================================
  // Social Identity
  // ============================================================

  /**
   * Link social account to agent
   * @param {string} agentId - Agent ID
   * @param {string} platform - Platform (twitter, discord, github)
   * @param {string} username - Username
   */
  async linkSocialAccount(agentId, platform, username) {
    const response = await this._request('/social/link', {
      method: 'POST',
      body: { agentId, platform, username },
    });

    return {
      success: true,
      link: response.link,
    };
  }

  // ============================================================
  // Webhooks
  // ============================================================

  /**
   * Register webhook
   * @param {string} url - Webhook URL
   * @param {string[]} events - Events to subscribe
   * @param {string} secret - Webhook secret
   */
  async registerWebhook(url, events, secret) {
    const response = await this._request('/webhooks', {
      method: 'POST',
      body: { url, events, secret },
    });

    return {
      success: true,
      webhook: response.webhook,
    };
  }

  /**
   * List webhooks
   */
  async listWebhooks() {
    const response = await this._request('/webhooks');
    return response.webhooks || [];
  }

  /**
   * Delete webhook
   * @param {string} webhookId - Webhook ID
   */
  async deleteWebhook(webhookId) {
    const response = await this._request(`/webhooks/${webhookId}`, {
      method: 'DELETE',
    });

    return {
      success: true,
    };
  }

  // ============================================================
  // Transaction History
  // ============================================================

  /**
   * Get transaction history for a wallet
   * @param {string} address - Wallet address
   * @param {number} limit - Number of transactions
   */
  async getTransactionHistory(address, limit = 50) {
    const response = await this._request(`/explorer/transactions/${address}?limit=${limit}`);
    return response.transactions || [];
  }

  /**
   * Get wallet activity
   * @param {string} agentId - Agent ID
   * @param {number} limit - Number of activities
   */
  async getWalletActivity(agentId, limit = 20) {
    const response = await this._request(`/agents/${agentId}/activity?limit=${limit}`);
    return response.activities || [];
  }

  // ============================================================
  // Doctor / Diagnostics
  // ============================================================

  /**
   * Run diagnostics
   */
  async getDoctorDiagnostics() {
    const response = await this._request('/doctor/diagnose');
    return response;
  }

  /**
   * Fix issues
   * @param {string[]} issues - List of issue IDs to fix
   */
  async fixIssues(issues) {
    const response = await this._request('/doctor/fix', {
      method: 'POST',
      body: { issues },
    });

    return {
      fixed: response.fixed,
      remaining: response.remaining,
    };
  }

  // ============================================================
  // Helper Methods
  // ============================================================

  /**
   * Make request to wallet service
   */
  async _request(path, options = {}) {
    const url = `${this.config.walletServiceUrl}${path}`;
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.config.apiKey) {
      headers['X-API-Key'] = this.config.apiKey;
    }

    const response = await fetch(url, {
      ...options,
      headers: { ...headers, ...options.headers },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Get skill status
   */
  getStatus() {
    return {
      initialized: this.initialized,
      wallets: this.wallets.size,
      version: '2.0.0',
      documentation: 'https://clawwallet.pages.dev',
      config: {
        walletServiceUrl: this.config.walletServiceUrl,
        defaultChain: this.config.defaultChain,
        autoRegister: this.config.autoRegister,
      },
    };
  }
}

// ============================================================
// Factory Function for Easy Integration
// ============================================================

/**
 * Create a CLAWwallet skill instance
 * @param {object} config - Configuration options
 */
export function createCLAWSkill(config) {
  return new MultiWalletSkill(config);
}

/**
 * Default skill instance
 */
export const defaultSkill = new MultiWalletSkill();

// ============================================================
// Agent Framework Adapters
// ============================================================

/**
 * OpenClaw Skill Adapter
 * Usage in OpenClaw:
 *   import { clawWalletSkill } from './skills/multiwallet-skill.js';
 *   agent.useSkill(clawWalletSkill);
 */
export const clawWalletSkill = {
  name: 'CLAWwallet',
  version: '2.0.0',
  
  async install(agent) {
    const skill = new MultiWalletSkill();
    await skill.initialize({ framework: 'openclaw', agent });
    
    // Register skill methods with agent - Enhanced v2.0
    // Wallet Operations
    agent.createWallet = (name, chain) => skill.createWallet(name, chain);
    agent.importWallet = (pk, name, chain) => skill.importWallet(pk, name, chain);
    agent.getBalance = (addr, chain) => skill.getBalance(addr, chain);
    agent.getTokenBalances = (addr, chain) => skill.getTokenBalances(addr, chain);
    agent.sendPayment = (from, to, amount, chain) => skill.sendPayment(from, to, amount, chain);
    agent.sendToken = (from, to, token, amount, chain) => skill.sendToken(from, to, token, amount, chain);
    agent.sweepWallet = (from, to, chain) => skill.sweepWallet(from, to, chain);
    agent.estimateGas = (from, to, value, chain) => skill.estimateGas(from, to, value, chain);
    agent.getTransactionReceipt = (hash, chain) => skill.getTransactionReceipt(hash, chain);
    
    // Multi-Chain
    agent.getSupportedChains = () => skill.getSupportedChains();
    agent.getChainConfig = (chain) => skill.getChainConfig(chain);
    
    // DeFi - Swaps
    agent.getSwapQuote = (from, to, amount, chain) => skill.getSwapQuote(from, to, amount, chain);
    agent.getBestQuote = (from, to, amount, chain) => skill.getBestQuote(from, to, amount, chain);
    agent.swapTokens = (wallet, from, to, amount, chain) => skill.swapTokens(wallet, from, to, amount, chain);
    
    // DeFi - Staking
    agent.stakeEth = (wallet, amount, chain) => skill.stakeEth(wallet, amount, chain);
    agent.unstakeEth = (wallet, amount, chain) => skill.unstakeEth(wallet, amount, chain);
    agent.getStakingPositions = (wallet, chain) => skill.getStakingPositions(wallet, chain);
    
    // DeFi - Lending
    agent.supplyToLending = (wallet, asset, amount, chain) => skill.supplyToLending(wallet, asset, amount, chain);
    agent.borrowFromLending = (wallet, asset, amount, chain) => skill.borrowFromLending(wallet, asset, amount, chain);
    agent.repayLending = (wallet, asset, amount, chain) => skill.repayLending(wallet, asset, amount, chain);
    agent.withdrawFromLending = (wallet, asset, amount, chain) => skill.withdrawFromLending(wallet, asset, amount, chain);
    agent.getLendingPositions = (wallet, chain) => skill.getLendingPositions(wallet, chain);
    
    // DeFi - Cross-chain
    agent.crossChainTransfer = (wallet, to, amount, src, dest, protocol) => skill.crossChainTransfer(wallet, to, amount, src, dest, protocol);
    agent.sendViaLayerZero = (wallet, to, amount, src, dest) => skill.sendViaLayerZero(wallet, to, amount, src, dest);
    agent.sendViaAxelar = (wallet, to, amount, src, dest) => skill.sendViaAxelar(wallet, to, amount, src, dest);
    
    // DeFi - Price
    agent.getPrice = (token, chain) => skill.getPrice(token, chain);
    agent.tokenToUsd = (token, amount, chain) => skill.tokenToUsd(token, amount, chain);
    agent.usdToToken = (token, usd, chain) => skill.usdToToken(token, usd, chain);
    
    // Multi-Sig
    agent.createMultisig = (owners, threshold, chain) => skill.createMultisig(owners, threshold, chain);
    agent.submitMultisigTransaction = (msig, to, value, desc, chain) => skill.submitMultisigTransaction(msig, to, value, desc, chain);
    agent.confirmMultisigTransaction = (txId, signer, sig) => skill.confirmMultisigTransaction(txId, signer, sig);
    agent.executeMultisigTransaction = (txId, executor) => skill.executeMultisigTransaction(txId, executor);
    agent.getMultisigTransactions = (msig, status) => skill.getMultisigTransactions(msig, status);
    
    // Policy
    agent.setPolicy = (wallet, policy) => skill.setPolicy(wallet, policy);
    agent.getPolicy = (wallet) => skill.getPolicy(wallet);
    agent.applyPolicyPreset = (wallet, preset) => skill.applyPolicyPreset(wallet, preset);
    agent.checkApprovalStatus = (id) => skill.checkApprovalStatus(id);
    
    // ENS
    agent.checkEnsAvailability = (name) => skill.checkEnsAvailability(name);
    agent.getEnsPrice = (name, years) => skill.getEnsPrice(name, years);
    agent.registerEns = (wallet, name, years) => skill.registerEns(wallet, name, years);
    
    // Agent Registry
    agent.registerAgent = (name, type, wallet) => skill.registerAgent(name, type, wallet);
    agent.getAgent = (name) => skill.getAgent(name);
    agent.listAgents = (filters) => skill.listAgents(filters);
    agent.searchAgents = (query) => skill.searchAgents(query);
    agent.payAgent = (to, amount, desc) => skill.payAgent(to, amount, desc);
    agent.getAgentBalance = (name) => skill.getAgentBalance(name);
    
    // Services & Economy
    agent.getServices = () => skill.getServices();
    agent.addService = (name, service) => skill.addService(name, service);
    agent.getEconomyStats = () => skill.getEconomyStats();
    agent.getPopularAgents = (limit) => skill.getPopularAgents(limit);
    
    // Identity
    agent.createIdentity = (wallet, name, desc, type) => skill.createIdentity(wallet, name, desc, type);
    agent.linkSocialAccount = (id, platform, username) => skill.linkSocialAccount(id, platform, username);
    
    // Webhooks
    agent.registerWebhook = (url, events, secret) => skill.registerWebhook(url, events, secret);
    agent.listWebhooks = () => skill.listWebhooks();
    agent.deleteWebhook = (id) => skill.deleteWebhook(id);
    
    // History & Diagnostics
    agent.getTransactionHistory = (addr, limit) => skill.getTransactionHistory(addr, limit);
    agent.getWalletActivity = (id, limit) => skill.getWalletActivity(id, limit);
    agent.getDoctorDiagnostics = () => skill.getDoctorDiagnostics();
    agent.fixIssues = (issues) => skill.fixIssues(issues);
    
    console.log('✅ CLAWwallet v2.0 skill installed on agent');
    return skill;
  },
};

/**
 * Standalone function for any agent
 * Just call this and use the returned methods!
 */
export default MultiWalletSkill;
