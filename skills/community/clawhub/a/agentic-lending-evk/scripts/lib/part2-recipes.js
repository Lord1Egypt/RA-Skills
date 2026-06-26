const EVK_RECIPE_CATALOG = {
  'btc-major-stable-borrow-v1': {
    recipeId: 'btc-major-stable-borrow-v1',
    protocol: 'evk',
    riskPreset: 'btc-major',
    hookProfile: 'none',
    ownershipProfile: 'deployer-owned',
    governanceProfile: 'deployer-governed',
    allowedOracleModes: ['direct-chainlink-compatible', 'composite-chainlink-compatible', 'custom-api3-fallback'],
    supportedCollateralSymbols: ['BTC', 'CBBTC', 'TBTC', 'WBTC'],
    supportedBorrowSymbols: ['USD', 'USDC', 'USDT'],
    ltvBps: 8000,
    liquidationThresholdBps: 8500,
  },
  'eth-major-stable-borrow-v1': {
    recipeId: 'eth-major-stable-borrow-v1',
    protocol: 'evk',
    riskPreset: 'eth-major',
    hookProfile: 'none',
    ownershipProfile: 'deployer-owned',
    governanceProfile: 'deployer-governed',
    allowedOracleModes: ['direct-chainlink-compatible', 'composite-chainlink-compatible', 'custom-api3-fallback'],
    supportedCollateralSymbols: ['ETH', 'WETH', 'WEETH', 'WSTETH'],
    supportedBorrowSymbols: ['USD', 'USDC', 'USDT'],
    ltvBps: 8250,
    liquidationThresholdBps: 8750,
  },
};

function getEvkRecipe(recipeId) {
  return EVK_RECIPE_CATALOG[recipeId] || null;
}

function listEvkRecipes() {
  return Object.values(EVK_RECIPE_CATALOG);
}

module.exports = {
  EVK_RECIPE_CATALOG,
  getEvkRecipe,
  listEvkRecipes,
};
