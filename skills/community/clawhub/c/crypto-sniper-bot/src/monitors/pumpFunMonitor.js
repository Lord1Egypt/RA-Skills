const axios = require('axios');

/**
 * Pump.fun Monitor using Bitquery GraphQL API
 * Docs: https://docs.bitquery.io/docs/blockchain/Solana/Pumpfun/Pump-Fun-API/
 */
class PumpFunMonitor {
  constructor() {
    this.bitqueryUrl = 'https://streaming.bitquery.io/graphql';
    this.pumpPortalUrl = 'https://pumpportal.fun/api';
    this.seenTokens = new Set();
    this.apiKey = process.env.BITQUERY_API_KEY || '';
  }

  /**
   * Get new tokens from pump.fun using Bitquery
   */
  async getNewTokens() {
    try {
      // Method 1: Using Bitquery GraphQL API
      if (this.apiKey) {
        return await this.getTokensFromBitquery();
      }

      // Method 2: Using PumpPortal API (fallback)
      return await this.getTokensFromPumpPortal();
    } catch (error) {
      console.error('PumpFun monitor error:', error.message);
      return [];
    }
  }

  /**
   * Get tokens using Bitquery GraphQL API
   */
  async getTokensFromBitquery() {
    const query = `
      query GetNewPumpFunTokens {
        Solana {
          DEXTradeByTokens(
            where: {
              Trade: {
                Dex: {
                  ProgramAddress: {
                    is: "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
                  }
                }
              }
              Block: {
                Time: {
                  since: "-15m"
                }
              }
            }
            orderBy: {descending: Block_Time}
            limit: {count: 50}
          ) {
            Trade {
              Currency {
                MintAddress
                Symbol
                Name
              }
              Price
              AmountInUSD
            }
            Block {
              Time
            }
          }
        }
      }
    `;

    const response = await axios.post(
      this.bitqueryUrl,
      { query },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        timeout: 15000
      }
    );

    const trades = response.data?.data?.Solana?.DEXTradeByTokens || [];
    return this.processTokens(trades);
  }

  /**
   * Get tokens using PumpPortal API
   */
  async getTokensFromPumpPortal() {
    try {
      const response = await axios.get(`${this.pumpPortalUrl}/data`, {
        timeout: 10000
      });

      const tokens = response.data || [];
      return this.processTokensFromPumpPortal(tokens);
    } catch (error) {
      console.error('PumpPortal API error:', error.message);
      return [];
    }
  }

  /**
   * Process tokens from Bitquery response
   */
  processTokens(trades) {
    const newTokens = [];
    const now = Date.now();

    for (const trade of trades) {
      const token = trade.Trade?.Currency;
      if (!token || !token.MintAddress) continue;

      if (!this.seenTokens.has(token.MintAddress)) {
        this.seenTokens.add(token.MintAddress);

        newTokens.push({
          address: token.MintAddress,
          symbol: token.Symbol || 'UNKNOWN',
          name: token.Name || 'Unknown Token',
          platform: 'pump.fun',
          price: trade.Trade?.Price || 0,
          liquidity: trade.Trade?.AmountInUSD || 0,
          holders: 0, // Need separate query
          marketCap: 0, // Need calculation
          createdAt: new Date(trade.Block?.Time).getTime() || now
        });
      }
    }

    return newTokens;
  }

  /**
   * Process tokens from PumpPortal response
   */
  processTokensFromPumpPortal(tokens) {
    const newTokens = [];
    const now = Date.now();

    for (const token of tokens) {
      if (!token.mint) continue;

      if (!this.seenTokens.has(token.mint)) {
        this.seenTokens.add(token.mint);

        newTokens.push({
          address: token.mint,
          symbol: token.symbol || 'UNKNOWN',
          name: token.name || 'Unknown Token',
          platform: 'pump.fun',
          price: token.price || 0,
          liquidity: token.liquidity || 0,
          holders: token.holder_count || 0,
          marketCap: token.market_cap || 0,
          createdAt: token.created_timestamp ? token.created_timestamp * 1000 : now
        });
      }
    }

    return newTokens;
  }

  /**
   * Get detailed token information
   */
  async getTokenDetails(tokenAddress) {
    try {
      const query = `
        query GetTokenDetails($address: String!) {
          Solana {
            DEXTradeByTokens(
              where: {
                Trade: {
                  Currency: {
                    MintAddress: {
                      is: $address
                    }
                  }
                }
              }
              limit: {count: 1}
            ) {
              Trade {
                Currency {
                  MintAddress
                  Symbol
                  Name
                }
                Price
                AmountInUSD
              }
            }
          }
        }
      `;

      const response = await axios.post(
        this.bitqueryUrl,
        {
          query,
          variables: { address: tokenAddress }
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.apiKey}`
          },
          timeout: 10000
        }
      );

      return response.data?.data?.Solana?.DEXTradeByTokens?.[0];
    } catch (error) {
      console.error('Failed to get token details:', error.message);
      return null;
    }
  }

  /**
   * Clear old seen tokens to prevent memory issues
   */
  clearSeenTokens() {
    if (this.seenTokens.size > 1000) {
      this.seenTokens.clear();
    }
  }
}

module.exports = PumpFunMonitor;
