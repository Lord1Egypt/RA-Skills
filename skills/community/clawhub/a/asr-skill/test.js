/**
 * 测试脚本
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:3000';

async function testHealth() {
  console.log('🧪 测试健康检查接口...');
  try {
    const response = await axios.get(`${BASE_URL}/health`);
    console.log('✅ 健康检查通过:', response.data);
    return true;
  } catch (error) {
    console.error('❌ 健康检查失败:', error.message);
    return false;
  }
}

async function testInfo() {
  console.log('\n🧪 测试信息接口...');
  try {
    const response = await axios.get(`${BASE_URL}/info`);
    console.log('✅ 信息接口通过:');
    console.log('  Skill名称:', response.data.data.name);
    console.log('  支持语言数:', response.data.data.supportedLanguages.length);
    console.log('  支持方言数:', response.data.data.supportedDialects.length);
    return true;
  } catch (error) {
    console.error('❌ 信息接口失败:', error.message);
    return false;
  }
}

async function testDialectMapping() {
  console.log('\n🧪 测试方言映射功能...');
  
  const testCases = [
    { input: '四川话', expected: 'Sichuan' },
    { input: '粤语', expected: 'Cantonese' },
    { input: '广东话', expected: 'Cantonese' },
    { input: '东北话', expected: 'Dongbei' },
    { input: '闽南语', expected: 'Minnan' },
    { input: '上海话', expected: 'Wu' },
    { input: '普通话', expected: 'Chinese' },
    { input: 'zh-CN', expected: 'Chinese' },
    { input: 'zh-HK', expected: 'Cantonese' },
    { input: 'english', expected: 'English' },
  ];
  
  const dialectMap = require('./dialect-map');
  let allPassed = true;
  
  for (const testCase of testCases) {
    const result = dialectMap.normalize(testCase.input);
    const passed = result === testCase.expected;
    console.log(`  ${passed ? '✅' : '❌'} ${testCase.input} → ${result} (预期: ${testCase.expected})`);
    if (!passed) allPassed = false;
  }
  
  if (allPassed) {
    console.log('✅ 方言映射测试全部通过');
  } else {
    console.error('❌ 部分方言映射测试失败');
  }
  
  return allPassed;
}

async function testTranscribe() {
  console.log('\n🧪 测试转录接口...');
  console.log('ℹ️  请确保服务已启动，此测试需要实际音频文件');
  
  // 检查是否有测试音频文件
  const testAudioPath = path.join(__dirname, 'test.wav');
  if (!fs.existsSync(testAudioPath)) {
    console.log('ℹ️  未找到test.wav测试音频文件，跳过转录测试');
    console.log('💡 你可以手动测试:');
    console.log('  curl -X POST -F "audio=@test.wav" -F "language=四川话" http://localhost:3000/transcribe');
    return true;
  }
  
  try {
    const formData = new FormData();
    formData.append('audio', fs.createReadStream(testAudioPath));
    formData.append('language', '四川话');
    
    const response = await axios.post(`${BASE_URL}/transcribe`, formData, {
      headers: formData.getHeaders(),
      timeout: 60000, // 首次加载模型可能需要较长时间
    });
    
    if (response.data.success) {
      console.log('✅ 转录成功:');
      console.log('  识别文本:', response.data.data.text);
      console.log('  检测语言:', response.data.data.language);
      console.log('  处理时长:', response.data.data.duration.toFixed(2) + 's');
      return true;
    } else {
      console.error('❌ 转录失败:', response.data.error);
      return false;
    }
  } catch (error) {
    console.error('❌ 转录请求失败:', error.message);
    if (error.response) {
      console.error('  错误详情:', error.response.data);
    }
    return false;
  }
}

async function runAllTests() {
  console.log('🚀 开始运行所有测试...\n');
  
  const results = [];
  
  results.push(await testHealth());
  results.push(await testInfo());
  results.push(await testDialectMapping());
  results.push(await testTranscribe());
  
  console.log('\n📊 测试结果汇总:');
  const passed = results.filter(r => r).length;
  const total = results.length;
  
  console.log(`  通过: ${passed}/${total}`);
  
  if (passed === total) {
    console.log('\n🎉 所有测试通过！');
  } else {
    console.log(`\n⚠️  有 ${total - passed} 项测试失败`);
    process.exit(1);
  }
}

// 如果直接运行此脚本，则执行测试
if (require.main === module) {
  runAllTests().catch(console.error);
}

module.exports = {
  testHealth,
  testInfo,
  testDialectMapping,
  testTranscribe,
  runAllTests,
};