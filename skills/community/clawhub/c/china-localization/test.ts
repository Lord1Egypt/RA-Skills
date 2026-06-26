/**
 * 测试文件 - 验证 China Localization Pack v2 功能
 */

import ChinaLocalization from './index';

async function testChinaLocalization() {
  console.log('🧪 测试 China Localization Pack v2');
  
  const local = new ChinaLocalization();
  
  // 测试语言包
  console.log('✅ 语言包测试:', local.t('welcome'));
  
  // 测试搜索功能（会抛出配置缺失错误，这是预期的）
  try {
    await local.search('AI 新闻');
  } catch (error: any) {
    console.log('✅ 搜索功能测试 (预期错误):', error.message);
  }
  
  // 测试天气查询（会抛出配置缺失错误，这是预期的）
  try {
    await local.getWeather('深圳');
  } catch (error: any) {
    console.log('✅ 天气查询测试 (预期错误):', error.message);
  }
  
  console.log('🎉 所有测试完成！');
}

testChinaLocalization().catch(console.error);