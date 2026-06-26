/**
 * clawSafe 交互式测试工具
 * 运行: node test-interactive.js
 */

const Detector = require('../detector');

const detector = new Detector();

console.log('\n🛡️  clawSafe 交互式测试\n');
console.log('输入内容进行检测，输入 "exit" 退出\n');
console.log('示例攻击类型：');
console.log('  - LLM: "Ignore previous instructions"');
console.log('  - SQL: "admin\' OR 1=1--"');
console.log('  - XSS: "<script>alert(1)</script>"');
console.log('  - API: "sk-1234567890abcdef"\n');

const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask() {
  rl.question('> ', (input) => {
    if (input.toLowerCase() === 'exit') {
      console.log('\n👋 再见！');
      rl.close();
      return;
    }

    if (!input.trim()) {
      ask();
      return;
    }

    const result = detector.scan(input);
    
    console.log('\n--- 检测结果 ---');
    console.log(`🔒 安全: ${result.safe ? '✅ 是' : '❌ 否'}`);
    console.log(`📊 置信度: ${(result.confidence * 100).toFixed(1)}%`);
    
    if (result.threats.length > 0) {
      console.log(`⚠️  威胁类型: ${result.threats.map(t => t.type).join(', ')}`);
      console.log('\n详细:');
      result.threats.forEach(t => {
        console.log(`  - ${t.type} (${t.severity}) 置信度: ${(t.confidence * 100).toFixed(1)}%`);
      });
    }
    
    console.log('\n');
    ask();
  });
}

ask();
