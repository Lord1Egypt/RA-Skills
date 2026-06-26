require('dotenv').config();
const axios = require('axios');

const BASE_URL = 'http://localhost:3001';

async function testSniperBot() {
  console.log('🧪 Testing Crypto Sniper Bot\n');

  try {
    // Test 1: Health check
    console.log('1. Testing health check...');
    const health = await axios.get(`${BASE_URL}/health`);
    console.log('✅ Health check passed:', health.data);

    // Test 2: Configure bot
    console.log('\n2. Testing configuration...');
    const configResponse = await axios.post(`${BASE_URL}/configure`, {
      buyAmount: 0.05,
      takeProfitPercent: 100,
      stopLossPercent: 50,
      maxPositions: 5,
      minLiquidity: 500
    }, {
      headers: {
        'x-skillpay-signature': 'test_signature'
      }
    });
    console.log('✅ Configuration updated:', configResponse.data);

    // Test 3: Get status
    console.log('\n3. Testing status endpoint...');
    const statusResponse = await axios.get(`${BASE_URL}/status`, {
      headers: {
        'x-skillpay-signature': 'test_signature'
      }
    });
    console.log('✅ Status retrieved:', statusResponse.data);

    // Test 4: Configure notifications
    console.log('\n4. Testing notification configuration...');
    const notifResponse = await axios.post(`${BASE_URL}/notifications`, {
      telegram: {
        enabled: true,
        botToken: process.env.TELEGRAM_BOT_TOKEN || 'test_token',
        chatId: process.env.TELEGRAM_CHAT_ID || 'test_chat_id'
      }
    }, {
      headers: {
        'x-skillpay-signature': 'test_signature'
      }
    });
    console.log('✅ Notifications configured:', notifResponse.data);

    // Test 5: Get history
    console.log('\n5. Testing history endpoint...');
    const historyResponse = await axios.get(`${BASE_URL}/history?limit=10`, {
      headers: {
        'x-skillpay-signature': 'test_signature'
      }
    });
    console.log('✅ History retrieved:', historyResponse.data);

    console.log('\n✅ All tests passed!');
    console.log('\n⚠️  Note: To start the bot, use POST /start endpoint');
    console.log('⚠️  Make sure to configure your wallet private key first!');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Run tests
testSniperBot();
