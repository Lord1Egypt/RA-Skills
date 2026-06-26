// 发布 LM Studio 文档系列
// 使用方法：node examples/publish-lmstudio.js

const docPublisher = require('../src/doc-publisher.js');

async function main() {
  const config = {
    rootDir: 'D:\\LMStudio',
    chaptersDir: 'chapters',
    appendixDir: 'appendix',
    outputDir: 'D:\\LMStudio\\published',
    
    publish: {
      author: 'AI 技术团队',
      prefix: '',
      addSeriesInfo: true
    }
  };
  
  console.log('📂 文档目录:', config.rootDir);
  console.log('📚 章节目录:', config.chaptersDir);
  console.log('📎 附录目录:', config.appendixDir);
  console.log('');
  
  try {
    const results = await docPublisher.publishSeries(config);
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ 发布完成！');
    console.log('='.repeat(60));
    console.log(`📊 总计：${results.length} 篇`);
    console.log('\n发布列表:');
    results.forEach((r, i) => {
      console.log(`  ${i + 1}. ${r.title}`);
      console.log(`     DraftID: ${r.draftId || r.media_id}`);
    });
    
  } catch (e) {
    console.error('\n❌ 发布失败:', e.message);
    console.error(e.stack);
    process.exit(1);
  }
}

main();
