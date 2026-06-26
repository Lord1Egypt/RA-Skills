const { Connection, Keypair, PublicKey, Transaction, VersionedTransaction } = require('@solana/web3.js');
const bs58 = require('bs58');
const axios = require('axios');

/**
 * Trading Engine with Jupiter Aggregator integration
 * Supports both Solana (pump.fun) and BSC (four.meme)
 */
class TradingEngine {
  constructor() {
    // Solana connection
    this.solanaConnection = new Connection(
      process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
      'confirmed'
    );
    this.wallet = null;

    // Jupiter API
    this.jupiterUrl = 'https://quote-api.jup.ag/v6';

    // BSC connection (for four.meme)
    this.bscRpcUrl = process.env.BSC_RPC_URL || 'https://bsc-dataseed.binance.org';
  }

  /**
   * Initialize wallet from private key
   */
  initializeWallet(privateKey) {
    try {
      const secretKey = bs58.decode(privateKey);
      this.wallet = Keypair.fromSecretKey(secretKey);
      console.log('Wallet initialized:', this.wallet.publicKey.toString());
      return true;
    } catch (error) {
      console.error('Failed to initialize wallet:', error.message);
      return false;
    }
  }

  /**
   * Get SOL balance
   */
  async getBalance() {
    if (!this.wallet) throw new Error('Wallet not initialized');

    const balance = await this.solanaConnection.getBalance(this.wallet.publicKey);
    return balance / 1e9; // Convert lamports to SOL
  }

  /**
   * Buy token using Jupiter Aggregator
   */
  async buyToken(tokenAddress, amountSOL, chain = 'solana') {
    if (!this.wallet) throw new Error('Wallet not initialized');

    try {
      if (chain === 'solana') {
        return await this.buyTokenSolana(tokenAddress, amountSOL);
      } else if (chain === 'bsc') {
        return await this.buyTokenBSC(tokenAddress, amountSOL);
      }

      throw new Error(`Unsupported chain: ${chain}`);
    } catch (error) {
      console.error('Buy failed:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Buy token on Solana using Jupiter
   */
  async buyTokenSolana(tokenMint, amountSOL) {
    console.log(`Buying ${amountSOL} SOL worth of ${tokenMint} on Solana`);

    // Step 1: Get quote from Jupiter
    const quote = await this.getJupiterQuote(
      'So11111111111111111111111111111111111111112', // SOL mint
      tokenMint,
      Math.floor(amountSOL * 1e9) // Convert SOL to lamports
    );

    if (!quote) {
      throw new Error('Failed to get quote from Jupiter');
    }

    // Step 2: Get swap transaction
    const swapTransaction = await this.getJupiterSwapTransaction(quote);

    if (!swapTransaction) {
      throw new Error('Failed to get swap transaction');
    }

    // Step 3: Execute transaction
    const txHash = await this.executeTransaction(swapTransaction);

    // Step 4: Get execution price
    const price = quote.outAmount / quote.inAmount;

    return {
      success: true,
      txHash,
      price,
      amount: amountSOL,
      outputAmount: quote.outAmount / 1e9
    };
  }

  /**
   * Get quote from Jupiter Aggregator
   */
  async getJupiterQuote(inputMint, outputMint, amount, slippageBps = 50) {
    try {
      const params = new URLSearchParams({
        inputMint,
        outputMint,
        amount: amount.toString(),
        slippageBps: slippageBps.toString()
      });

      const response = await axios.get(`${this.jupiterUrl}/quote?${params}`, {
        timeout: 10000
      });

      return response.data;
    } catch (error) {
      console.error('Jupiter quote error:', error.message);
      return null;
    }
  }

  /**
   * Get swap transaction from Jupiter
   */
  async getJupiterSwapTransaction(quote) {
    try {
      const response = await axios.post(
        `${this.jupiterUrl}/swap`,
        {
          quoteResponse: quote,
          userPublicKey: this.wallet.publicKey.toString(),
          wrapAndUnwrapSol: true,
          dynamicComputeUnitLimit: true,
          prioritizationFeeLamports: 'auto'
        },
        {
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000
        }
      );

      return response.data.swapTransaction;
    } catch (error) {
      console.error('Jupiter swap transaction error:', error.message);
      return null;
    }
  }

  /**
   * Execute Solana transaction
   */
  async executeTransaction(swapTransactionBase64) {
    try {
      // Deserialize transaction
      const swapTransactionBuf = Buffer.from(swapTransactionBase64, 'base64');
      const transaction = VersionedTransaction.deserialize(swapTransactionBuf);

      // Sign transaction
      transaction.sign([this.wallet]);

      // Send transaction
      const txid = await this.solanaConnection.sendRawTransaction(
        transaction.serialize(),
        {
          skipPreflight: true,
          maxRetries: 2
        }
      );

      // Confirm transaction
      await this.solanaConnection.confirmTransaction(txid, 'confirmed');

      console.log('Transaction confirmed:', txid);
      return txid;
    } catch (error) {
      console.error('Transaction execution error:', error.message);
      throw error;
    }
  }

  /**
   * Sell token using Jupiter Aggregator
   */
  async sellToken(tokenAddress, amount, chain = 'solana') {
    if (!this.wallet) throw new Error('Wallet not initialized');

    try {
      if (chain === 'solana') {
        return await this.sellTokenSolana(tokenAddress, amount);
      } else if (chain === 'bsc') {
        return await this.sellTokenBSC(tokenAddress, amount);
      }

      throw new Error(`Unsupported chain: ${chain}`);
    } catch (error) {
      console.error('Sell failed:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Sell token on Solana using Jupiter
   */
  async sellTokenSolana(tokenMint, amount) {
    console.log(`Selling ${amount} of ${tokenMint} on Solana`);

    // Get token balance first
    const balance = await this.getTokenBalance(tokenMint);
    const sellAmount = Math.floor(balance * 1e9); // Convert to smallest unit

    // Step 1: Get quote from Jupiter
    const quote = await this.getJupiterQuote(
      tokenMint,
      'So11111111111111111111111111111111111111112', // SOL mint
      sellAmount
    );

    if (!quote) {
      throw new Error('Failed to get quote from Jupiter');
    }

    // Step 2: Get swap transaction
    const swapTransaction = await this.getJupiterSwapTransaction(quote);

    if (!swapTransaction) {
      throw new Error('Failed to get swap transaction');
    }

    // Step 3: Execute transaction
    const txHash = await this.executeTransaction(swapTransaction);

    // Step 4: Get execution price
    const price = quote.outAmount / quote.inAmount;
    const amountReceived = quote.outAmount / 1e9; // Convert to SOL

    return {
      success: true,
      txHash,
      price,
      amountReceived
    };
  }

  /**
   * Get token price from Jupiter
   */
  async getTokenPrice(tokenAddress, chain = 'solana') {
    try {
      if (chain === 'solana') {
        // Get quote for 1 token to SOL
        const quote = await this.getJupiterQuote(
          tokenAddress,
          'So11111111111111111111111111111111111111112',
          1e9 // 1 token (assuming 9 decimals)
        );

        if (quote) {
          return quote.outAmount / 1e9; // Price in SOL
        }
      }

      return null;
    } catch (error) {
      console.error('Failed to get token price:', error.message);
      return null;
    }
  }

  /**
   * Get token balance
   */
  async getTokenBalance(tokenAddress) {
    if (!this.wallet) throw new Error('Wallet not initialized');

    try {
      const tokenAccounts = await this.solanaConnection.getParsedTokenAccountsByOwner(
        this.wallet.publicKey,
        { mint: new PublicKey(tokenAddress) }
      );

      if (tokenAccounts.value.length === 0) {
        return 0;
      }

      const balance = tokenAccounts.value[0].account.data.parsed.info.tokenAmount.uiAmount;
      return balance || 0;
    } catch (error) {
      console.error('Failed to get token balance:', error.message);
      return 0;
    }
  }

  /**
   * Buy token on BSC (placeholder - needs Web3.js BSC integration)
   */
  async buyTokenBSC(tokenAddress, amountBNB) {
    console.warn('BSC trading not yet implemented');
    throw new Error('BSC trading support coming soon');
  }

  /**
   * Sell token on BSC (placeholder)
   */
  async sellTokenBSC(tokenAddress, amount) {
    console.warn('BSC trading not yet implemented');
    throw new Error('BSC trading support coming soon');
  }
}

module.exports = new TradingEngine();
