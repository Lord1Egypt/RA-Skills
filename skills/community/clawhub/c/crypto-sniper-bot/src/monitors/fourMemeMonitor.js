const axios = require('axios');

/**
 * Four.meme Monitor using Bitquery GraphQL API
 * Note: Four.meme is on BNB Chain (BSC), not Solana
 * Docs: https://docs.bitquery.io/docs/blockchain/BSC/four-meme-api/
 */
class FourMemeMonitor {
  constructor() {
    this.bitqueryUrl = 'https://streaming.bitquery.io/graphql';
    this.fourMemeContract = '0xF0c7616E5B2C63c3a3e7FdF5B8e5e5e5e5e5e5e5'; // Four.meme factory contract
    this.seenTokens = new Set();
    this.apiKey = process.env.BITQUERY_API_KEY || '';
  }

  /**
   * Get new tokens from four.meme
   */
  async getNewTokens() {
    try {
      if (!this.apiKey) {
        console.warn('Bitquery API key not configured for four.meme monitoring');
        return [];
      }

      return await this.getTokensFromBitquery();
    } catch (error) {
      console.error('FourMeme monitor error:', error.message);
      return [];
    }
  }

  /**
   * Get tokens using Bitquery GraphQL API for BSC
   */
  async getTokensFromBitquery() {
    const query = `
      query GetNewFourMemeTokens {
        EVM(network: bsc) {
          DEXTradeByTokens(
            where: {
              Block: {
                Time: {
                  since: "-15m"
                }
              }
              Trade: {
                Dex: {
                  ProtocolName: {
                    is: "four_meme"
                  }
                }
              }
            }
            orderBy: {descending: Block_Time}
            limit: {count: 50}
          ) {
            Trade {
              Currency {
                SmartContract
                Symbol
                Name
              }
              PriceInUSD
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

    const trades = response.data?.data?.EVM?.DEXTradeByTokens || [];
    return this.processTokens(trades);
  }

  /**
   * Process tokens from Bitquery response
   */
  processTokens(trades) {
    const newTokens = [];
    const now = Date.now();

    for (const trade of trades) {
      const token = trade.Trade?.Currency;
      if (!token || !token.SmartContract) continue;

      if (!this.seenTokens.has(token.SmartContract)) {
        this.seenTokens.add(token.SmartContract);

        newTokens.push({
          address: token.SmartContract,
          symbol: token.Symbol || 'UNKNOWN',
          name: token.Name || 'Unknown Token',
          platform: 'four.meme',
          price: trade.Trade?.PriceInUSD || 0,
          liquidity: trade.Trade?.AmountInUSD || 0,
          holders: 0, // Need separate query
          marketCap: 0, // Need calculation
          createdAt: new Date(trade.Block?.Time).getTime() || now,
          chain: 'bsc' // Important: four.meme is on BSC
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
          EVM(network: bsc) {
            DEXTradeByTokens(
              where: {
                Trade: {
                  Currency: {
                    SmartContract: {
                      is: $address
                    }
                  }
                }
              }
              limit: {count: 1}
            ) {
              Trade {
                Currency {
                  SmartContract
                  Symbol
                  Name
                }
                PriceInUSD
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

      return response.data?.data?.EVM?.DEXTradeByTokens?.[0];
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

module.exports = FourMemeMonitor;
