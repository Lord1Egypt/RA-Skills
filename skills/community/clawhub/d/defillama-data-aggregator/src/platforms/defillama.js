/**
 * DefiLlama API Client
 * https://docs.llama.fi/
 */

const ApiClient = require('../utils/api-client');

class DefiLlamaClient {
  constructor(config) {
    this.config = config;
    this.client = new ApiClient({
      ...config.settings,
      baseUrl: config.defillama.baseUrl
    });
  }

  /**
   * Get total DeFi TVL (sum of all chains)
   */
  async getTotalTvl() {
    const chains = await this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/chains`,
      cacheDuration: 3600 // Cache for 1 hour
    });
    
    // Calculate total TVL from all chains
    const totalTvl = chains.reduce((sum, chain) => sum + (chain.tvl || 0), 0);
    
    return {
      totalTvl: totalTvl,
      chains: chains,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get protocol TVL
   */
  async getProtocolTvl(protocolName) {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/protocol/${protocolName}`,
      cacheDuration: 300 // Cache for 5 minutes
    });
  }

  /**
   * Get all protocols
   */
  async getProtocols(filters = {}) {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/protocols`,
      params: filters,
      cacheDuration: 600 // Cache for 10 minutes
    });
  }

  /**
   * Get chain TVL by name
   */
  async getChainTvl(chainName) {
    const chains = await this.getChains();
    
    // Find the chain by name (case-insensitive)
    const chain = chains.find(c => 
      c.name.toLowerCase() === chainName.toLowerCase() ||
      c.gecko_id === chainName.toLowerCase() ||
      c.tokenSymbol?.toLowerCase() === chainName.toLowerCase()
    );
    
    if (!chain) {
      throw new Error(`Chain "${chainName}" not found. Available chains: ${chains.slice(0, 10).map(c => c.name).join(', ')}...`);
    }
    
    return {
      name: chain.name,
      gecko_id: chain.gecko_id,
      tokenSymbol: chain.tokenSymbol,
      tvl: chain.tvl,
      chainId: chain.chainId,
      cmcId: chain.cmcId
    };
  }

  /**
   * Get all chains
   */
  async getChains() {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/chains`,
      cacheDuration: 3600 // Cache for 1 hour
    });
  }

  /**
   * Get protocol details
   */
  async getProtocolDetails(name) {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/protocol/${name}`,
      cacheDuration: 600 // Cache for 10 minutes
    });
  }

  /**
   * Get TVL historical data
   */
  async getTvlHistory(protocol, timeframe = '24h') {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/protocol/${protocol}`,
      cacheDuration: 300 // Cache for 5 minutes
    });
  }

  /**
   * Get yields by pool
   * Uses https://yields.llama.fi/pools endpoint
   */
  async getPoolYields(filters = {}) {
    const response = await this.client.request({
      url: `https://yields.llama.fi/pools`,
      cacheDuration: 300 // Cache for 5 minutes
    });

    // Extract pools from response (API returns {status, data} structure)
    let poolsList = [];
    if (response && response.data && Array.isArray(response.data)) {
      poolsList = response.data;
    } else if (Array.isArray(response)) {
      poolsList = response;
    }

    // Filter the pools based on the provided filters
    let filteredPools = poolsList;

    if (filters.minApy !== undefined && filters.minApy > 0) {
      filteredPools = filteredPools.filter(pool => pool.apy >= filters.minApy);
    }

    if (filters.minTvl !== undefined && filters.minTvl > 0) {
      filteredPools = filteredPools.filter(pool => pool.tvlUsd >= filters.minTvl);
    }

    if (filters.chain) {
      filteredPools = filteredPools.filter(pool => 
        pool.chain && pool.chain.toLowerCase() === filters.chain.toLowerCase()
      );
    }

    if (filters.stablecoin) {
      filteredPools = filteredPools.filter(pool => pool.stablecoin === true);
    }

    if (filters.query) {
      const queryLower = filters.query.toLowerCase();
      filteredPools = filteredPools.filter(pool => 
        (pool.project && pool.project.toLowerCase().includes(queryLower)) ||
        (pool.symbol && pool.symbol.toLowerCase().includes(queryLower))
      );
    }

    // Sort by APY descending (only if APY is a valid number)
    filteredPools.sort((a, b) => {
      const apyA = typeof a.apy === 'number' ? a.apy : 0;
      const apyB = typeof b.apy === 'number' ? b.apy : 0;
      return apyB - apyA;
    });

    return filteredPools;
  }

  /**
   * Get bridge volumes
   */
  async getBridgeVolumes() {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/bridges/volumes`,
      cacheDuration: 3600 // Cache for 1 hour
    });
  }

  /**
   * Get stablecoin pegs
   */
  async getStablecoinPegs() {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/stablecoins`,
      cacheDuration: 600 // Cache for 10 minutes
    });
  }

  /**
   * Get oracle prices
   */
  async getOraclePrices() {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/prices`,
      cacheDuration: 60 // Cache for 1 minute
    });
  }

  /**
   * Get token price
   */
  async getTokenPrice(token) {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/prices/current/${token}`,
      cacheDuration: 60 // Cache for 1 minute
    });
  }

  /**
   * Get protocol categories
   */
  async getProtocolCategories() {
    return this.client.request({
      url: `${this.config.defillama.baseUrl}/v2/protocol/categories`,
      cacheDuration: 86400 // Cache for 24 hours
    });
  }
}

module.exports = DefiLlamaClient;
