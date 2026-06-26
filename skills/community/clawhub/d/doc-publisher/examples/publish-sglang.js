// SGLang 系列文档发布脚本（带随机配图）
// 使用方法：node examples/publish-sglang.js

const docPublisher = require('../src/doc-publisher.js');
const imagePicker = require('../src/image-picker.js');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('='.repeat(60));
  console.log('🚀 SGLang 进阶系列 - 公众号发布（带配图）');
  console.log('='.repeat(60));
  
  const config = {
    rootDir: 'D:\\DocsAutoWrter\\SGLang',
    chaptersDir: 'chapters',
    appendixDir: 'appendix',
    outputDir: 'D:\\DocsAutoWrter\\SGLang\\published',
    
    publish: {
      author: 'SGLang 技术团队',
      addSeriesInfo: true,
      // 图片配置
      imageDir: 'D:\\DocsAutoWrter\\SGLang',  // 图片目录
      randomImage: true  // 启用随机配图
    }
  };
  
  try {
    const results = await docPublisher.publishSeries(config);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 发布完成！');
    console.log('='.repeat(60));
    console.log(`📊 总计：${results.length} 篇`);
    console.log('\n发布列表:');
    results.forEach((r, i) => {
      console.log(`  ${i + 1}. ${r.title}`);
      console.log(`     DraftID: ${r.draftId}`);
      if (r.imageUsed) {
        console.log(`     🖼️  配图：${r.imageUsed}`);
      }
    });
    
  } catch (e) {
    console.error('\n❌ 发布失败:', e.message);
    console.error(e.stack);
    process.exit(1);
  }
}

main();
