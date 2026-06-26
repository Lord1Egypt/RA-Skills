const api = require('../src/wechat-api.js');

async function test() {
  // 测试 1: 最简单的 HTML
  const html1 = '<h1>测试标题</h1><p>测试内容</p>';
  console.log('测试 1 - 简单 HTML:', html1.length, '字符');
  try {
    const r1 = await api.addDraft({ title: '格式测试 1', author: '测试', digest: '测试', content: html1 });
    console.log('✅ 测试 1 成功，DraftID:', r1.media_id);
  } catch (e) {
    console.log('❌ 测试 1 失败:', e.message);
  }
  
  // 测试 2: 带 section 标签
  const html2 = '<section><h1>测试</h1><p>内容</p></section>';
  console.log('\n测试 2 - Section 标签:', html2.length, '字符');
  try {
    const r2 = await api.addDraft({ title: '格式测试 2', author: '测试', digest: '测试', content: html2 });
    console.log('✅ 测试 2 成功，DraftID:', r2.media_id);
  } catch (e) {
    console.log('❌ 测试 2 失败:', e.message);
  }
  
  // 测试 3: 带代码块
  const html3 = '<section><h1>代码测试</h1><section style="margin:20px 0;padding:15px;background:#f8f9fa;"><pre><code>print(123)</code></pre></section></section>';
  console.log('\n测试 3 - 代码块:', html3.length, '字符');
  try {
    const r3 = await api.addDraft({ title: '格式测试 3', author: '测试', digest: '测试', content: html3 });
    console.log('✅ 测试 3 成功，DraftID:', r3.media_id);
  } catch (e) {
    console.log('❌ 测试 3 失败:', e.message);
  }
  
  // 测试 4: 带列表
  const html4 = '<section><h1>列表测试</h1><p>【1】项目一</p><p>【2】项目二</p></section>';
  console.log('\n测试 4 - 列表:', html4.length, '字符');
  try {
    const r4 = await api.addDraft({ title: '格式测试 4', author: '测试', digest: '测试', content: html4 });
    console.log('✅ 测试 4 成功，DraftID:', r4.media_id);
  } catch (e) {
    console.log('❌ 测试 4 失败:', e.message);
  }
}

test().catch(e => console.error('Error:', e));
