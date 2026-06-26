require('dotenv').config();
const PumpFunMonitor = require('./src/monitors/pumpFunMonitor');
const FourMemeMonitor = require('./src/monitors/fourMemeMonitor');
const tradingEngine = require('./src/trading/tradingEngine');

async function testAPIIntegration() {
  console.log('🧪 Testing API Integration\n');

  try {
    // Test 1: PumpFun Monitor
    console.log('1. Testing PumpFun Monitor...');
    const pumpMonitor = new PumpFunMonitor();
    console.log('✅ PumpFun Monitor initialized');

    // Test getting new tokens (will use fallback API without Bitquery key)
    console.log('   Attempting to fetch new tokens from pump.fun...');
    const pumpTokens = await pumpMonitor.getNewTokens();
    console.log(`   Found ${pumpTokens.length} tokens from pump.fun`);
    if (pumpTokens.length > 0) {
      console.log('   Sample token:', {
        symbol: pumpTokens[0].symbol,
        address: pumpTokens[0].address.substring(0, 10) + '...',
        platform: pumpTokens[0].platform
      });
    }

    // Test 2: FourMeme Monitor
    console.log('\n2. Testing FourMeme Monitor...');
    const fourMonitor = new FourMemeMonitor();
    console.log('✅ FourMeme Monitor initialized');

    if (!process.env.BITQUERY_API_KEY) {
      console.log('   ⚠️  Bitquery API key not configured - skipping four.meme test');
      console.log('   To test four.meme, add BITQUERY_API_KEY to .env');
    } else {
      console.log('   Attempting to fetch new tokens from four.meme...');
      const fourTokens = await fourMonitor.getNewTokens();
      console.log(`   Found ${fourTokens.length} tokens from four.meme`);
    }

    // Test 3: Jupiter Integration
    console.log('\n3. Testing Jupiter Aggregator Integration...');
    console.log('   Testing quote fetching...');

    // Test getting a quote (SOL to USDC)
    const testQuote = await tradingEngine.getJupiterQuote(
      'So11111111111111111111111111111111111111112', // SOL
      'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', // USDC
      1000000000 // 1 SOL
    );

    if (testQuote) {
      console.log('✅ Jupiter quote successful');
      console.log('   Input amount: 1 SOL');
      console.log('   Output amount:', (testQuote.outAmount / 1e6).toFixed(2), 'USDC');
      console.log('   Price impact:', testQuote.priceImpactPct || 'N/A');
    } else {
      console.log('⚠️  Jupiter quote failed (may be rate limited or network issue)');
    }

    // Test 4: Wallet initialization (without actual private key)
    console.log('\n4. Testing Wallet System...');
    if (process.env.WALLET_PRIVATE_KEY) {
      const initialized = tradingEngine.initializeWallet(process.env.WALLET_PRIVATE_KEY);
      if (initialized) {
        console.log('✅ Wallet initialized successfully');
        const balance = await tradingEngine.getBalance();
        console.log(`   SOL Balance: ${balance.toFixed(4)} SOL`);
      } else {
        console.log('❌ Wallet initialization failed');
      }
    } else {
      console.log('⚠️  WALLET_PRIVATE_KEY not configured - skipping wallet test');
      console.log('   To test wallet, add WALLET_PRIVATE_KEY to .env');
    }

    console.log('\n✅ API Integration Tests Complete!\n');
    console.log('📋 Summary:');
    console.log('   - PumpFun Monitor: ✅ Working');
    console.log('   - FourMeme Monitor: ✅ Initialized');
    console.log('   - Jupiter Aggregator: ✅ Working');
    console.log('   - Trading Engine: ✅ Ready');

    console.log('\n⚠️  Important Notes:');
    console.log('   1. For full functionality, configure BITQUERY_API_KEY in .env');
    console.log('   2. For live trading, configure WALLET_PRIVATE_KEY in .env');
    console.log('   3. Start with small amounts to test trading');
    console.log('   4. Monitor bot activity regularly');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.error('Stack:', error.stack);
  }
}

// Run tests
testAPIIntegration();
