const axios = require('axios');

/**
 * 测试脚本
 */
async function testSkill() {
  const baseURL = 'http://localhost:3000';

  console.log('🧪 Testing Crypto Funding Monitor Skill\n');

  // 1. 健康检查
  console.log('1. Health Check...');
  try {
    const health = await axios.get(`${baseURL}/health`);
    console.log('✅ Health check passed:', health.data);
  } catch (error) {
    console.error('❌ Health check failed:', error.message);
    return;
  }

  // 2. 测试监测端点（无支付验证）
  console.log('\n2. Testing monitor endpoint...');
  try {
    const monitor = await axios.post(`${baseURL}/monitor`, {
      userId: 'test-user-123',
      transactionId: 'test-tx-456',
      channels: {
        telegram: {
          chatId: 'your-telegram-chat-id'
        }
      }
    });
    console.log('✅ Monitor test:', monitor.data);
  } catch (error) {
    console.log('⚠️  Monitor test (expected to fail without valid payment):', error.response?.data || error.message);
  }

  // 3. 测试订阅
  console.log('\n3. Testing subscription...');
  try {
    const subscribe = await axios.post(`${baseURL}/subscribe`, {
      userId: 'test-user-123',
      channels: {
        telegram: { chatId: 'your-telegram-chat-id' },
        email: { to: 'your-email@example.com' }
      },
      schedule: ['0 9 * * *', '0 18 * * *']
    });
    console.log('✅ Subscription created:', subscribe.data);
  } catch (error) {
    console.error('❌ Subscription failed:', error.response?.data || error.message);
  }

  // 4. 查询订阅状态
  console.log('\n4. Checking subscription status...');
  try {
    const status = await axios.get(`${baseURL}/subscription/test-user-123`);
    console.log('✅ Subscription status:', status.data);
  } catch (error) {
    console.error('❌ Status check failed:', error.response?.data || error.message);
  }

  // 5. 取消订阅
  console.log('\n5. Testing unsubscribe...');
  try {
    const unsubscribe = await axios.post(`${baseURL}/unsubscribe`, {
      userId: 'test-user-123'
    });
    console.log('✅ Unsubscribed:', unsubscribe.data);
  } catch (error) {
    console.error('❌ Unsubscribe failed:', error.response?.data || error.message);
  }

  console.log('\n✨ Test completed!\n');
}

// 运行测试
if (require.main === module) {
  testSkill().catch(console.error);
}

module.exports = testSkill;
