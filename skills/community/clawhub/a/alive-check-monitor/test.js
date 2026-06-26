const axios = require('axios');

async function testAliveCheck() {
  const baseURL = 'http://localhost:3000';

  console.log('🧪 测试还活着么监测服务\n');

  // 1. 健康检查
  console.log('1. 健康检查...');
  try {
    const health = await axios.get(`${baseURL}/health`);
    console.log('✅ 健康检查通过:', health.data);
  } catch (error) {
    console.error('❌ 健康检查失败:', error.message);
    return;
  }

  // 2. 注册用户
  console.log('\n2. 注册用户...');
  try {
    const register = await axios.post(`${baseURL}/register`, {
      userId: 'test001',
      name: '张三',
      phone: '13800138000',
      emergencyContacts: [
        {
          name: '李四',
          relation: '朋友',
          phone: '13900139000',
          telegram: '123456789',
          priority: 1
        }
      ]
    });
    console.log('✅ 注册成功:', register.data.message);
  } catch (error) {
    console.log('⚠️  注册测试:', error.response?.data || error.message);
  }

  // 3. 用户签到
  console.log('\n3. 用户签到...');
  try {
    const checkin = await axios.post(`${baseURL}/checkin`, {
      userId: 'test001',
      message: '今天状态不错！',
      mood: '😊',
      location: '在家'
    });
    console.log('✅ 签到成功:', checkin.data.message);
    console.log('   连续签到:', checkin.data.data.user.consecutiveDays, '天');
  } catch (error) {
    console.error('❌ 签到失败:', error.response?.data || error.message);
  }

  // 4. 查询状态
  console.log('\n4. 查询用户状态...');
  try {
    const status = await axios.get(`${baseURL}/status/test001`);
    console.log('✅ 状态查询成功:');
    console.log('   用户:', status.data.data.name);
    console.log('   状态:', status.data.data.status);
    console.log('   上次签到:', status.data.data.lastCheckin);
  } catch (error) {
    console.error('❌ 状态查询失败:', error.response?.data || error.message);
  }

  // 5. 查看签到历史
  console.log('\n5. 查看签到历史...');
  try {
    const history = await axios.get(`${baseURL}/history/test001?days=7`);
    console.log(`✅ 历史记录: ${history.data.count} 条`);
  } catch (error) {
    console.error('❌ 历史查询失败:', error.response?.data || error.message);
  }

  console.log('\n✨ 测试完成!\n');
}

if (require.main === module) {
  testAliveCheck().catch(console.error);
}

module.exports = testAliveCheck;
