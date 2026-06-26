// 测试脚本 - Family Memory Timeline
import { handleFamilyMemoryTimeline } from '../handler.mjs';

async function runTest() {
  console.log('=== Family Memory Timeline 自测 ===\n');
  
  // 测试用例
  const testRequest = {
    media: [
      '/photos/vacation_2023.jpg',
      { path: '/photos/birthday.png', description: '春节家庭聚会温馨时刻', timestamp: '2023-01-22T18:00:00' }
    ],
    conversations: [
      { speaker: '妈妈', content: '今天宝宝第一次走路了，太激动了！', timestamp: '2023-05-15T10:30:00' },
      { speaker: '爸爸', content: '要记录下来这珍贵的时刻', timestamp: '2023-05-15T10:31:00' },
      { speaker: '奶奶', content: '宝宝真棒！', timestamp: '2023-05-15T10:32:00' }
    ],
    config: {
      style: { narrative: 'warm' },
      output: { formats: ['json', 'markdown'] }
    },
    projectName: '2023家庭回忆'
  };
  
  console.log('测试输入:');
  console.log('- 媒体文件: 2个');
  console.log('- 对话记录: 3条');
  console.log('- 故事风格: warm (温馨)');
  console.log('');
  
  try {
    const result = await handleFamilyMemoryTimeline(testRequest);
    
    if (result.success) {
      console.log('✅ 处理成功!\n');
      console.log('输出摘要:');
      console.log('- story.id:', result.story.id);
      console.log('- story.title:', result.story.title);
      console.log('- timeline.events count:', result.story.timeline.events.length);
      console.log('- chapters count:', result.story.chapters.length);
      console.log('- totalEvents:', result.story.summary.totalEvents);
      console.log('- processingTime:', result.story.metadata.processingTime, 'ms');
      console.log('');
      
      console.log('情感分布:');
      for (const [emotion, count] of Object.entries(result.story.timeline.statistics.emotionDistribution)) {
        console.log('  -', emotion, ':', count);
      }
      console.log('');
      
      console.log('关键时刻:');
      for (const m of result.story.summary.keyMoments.slice(0, 3)) {
        console.log('  -', m.title, '(重要性:', m.significance + '/10)');
      }
      console.log('');
      
      console.log('Markdown输出预览 (前500字符):');
      console.log(result.outputContent.substring(0, 500));
      console.log('...\n');
      
      console.log('=== 自测通过 ===');
    } else {
      console.log('❌ 处理失败:', result.error);
    }
  } catch (error) {
    console.log('❌ 测试异常:', error.message);
  }
}

runTest();
