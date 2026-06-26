#!/usr/bin/env node

/**
 * Calculator Chat - 理解你说的话，翻译成数字
 */

const { execSync, spawn } = require('child_process');
const path = require('path');

// 完整的数字映射表
const NUMBER_PATTERNS = [
  // 爱意
  { pattern: '我爱你', result: '520' },
  { pattern: '爱你', result: '520' },
  { pattern: '喜欢', result: '520' },
  { pattern: '爱', result: '520' },
  { pattern: '男神', result: '520' },
  { pattern: '女神', result: '520' },
  { pattern: '表白', result: '520' },
  
  // 一生一世
  { pattern: '一生一世', result: '1314' },
  { pattern: '永恒', result: '1314' },
  { pattern: '永远', result: '1314' },
  { pattern: '生生世世', result: '3344' },
  { pattern: '长长久久', result: '3344' },
  
  // 再见
  { pattern: '再见', result: '88' },
  { pattern: '拜拜', result: '88' },
  { pattern: '走了', result: '88' },
  { pattern: ' goodbye', result: '88' },
  { pattern: 'bye', result: '88' },
  
  // 哭/难过
  { pattern: '哭', result: '555' },
  { pattern: '好累', result: '555' },
  { pattern: '累', result: '555' },
  { pattern: '难过', result: '555' },
  { pattern: '伤心', result: '555' },
  { pattern: '痛苦', result: '555' },
  { pattern: '郁闷', result: '555' },
  
  // 发财
  { pattern: '恭喜发财', result: '888' },
  { pattern: '财源广进', result: '888' },
  { pattern: '发财', result: '888' },
  { pattern: '恭喜', result: '888' },
  { pattern: '有钱', result: '888' },
  { pattern: '富有', result: '888' },
  { pattern: '旺', result: '888' },
  { pattern: '发', result: '888' },
  
  // 顺利/成功
  { pattern: '顺利', result: '66' },
  { pattern: '成功', result: '66' },
  { pattern: '棒', result: '66' },
  { pattern: '厉害', result: '666' },
  { pattern: '666', result: '666' },
  { pattern: '牛', result: '666' },
  { pattern: '太强', result: '666' },
  
  // 救命
  { pattern: '救命', result: '995' },
  { pattern: '救我', result: '995' },
  { pattern: '帮我', result: '995' },
  { pattern: '帮忙', result: '995' },
  { pattern: 'help', result: '995' },
  
  // 生日
  { pattern: '生日', result: '218' },
  { pattern: '生日快乐', result: '218' },
  
  // 亲亲
  { pattern: '亲亲', result: '777' },
  { pattern: '么么', result: '777' },
  { pattern: '想你', result: '777' },
  { pattern: '么么哒', result: '777' },
  
  // 再见/OK
  { pattern: '007', result: '88' },
  { pattern: 'OK', result: '88' },
  { pattern: '好的', result: '88' },
  { pattern: '收到', result: '88' },
  
  // 天气相关
  { pattern: '天气好', result: '88' },
  { pattern: '天气晴', result: '88' },
  { pattern: '晴天', result: '88' },
  { pattern: '阳光', result: '88' },
  
  // 数字解读
  { pattern: '520', result: '1314' },
  { pattern: '1314', result: '520' },
  { pattern: '888', result: '16888' },
  
  // 谢谢/再见
  { pattern: '谢谢', result: '88' },
  { pattern: '感谢', result: '88' },
  { pattern: '感恩', result: '88' },
  
  // 加油
  { pattern: '加油', result: '66' },
  { pattern: '努力', result: '66' },
];

function parseExpression(message) {
  let expr = message.toLowerCase();
  let matchedResult = null;
  
  // 查找匹配的模式
  for (const { pattern, result } of NUMBER_PATTERNS) {
    if (expr.includes(pattern.toLowerCase())) {
      matchedResult = result;
      console.log(`📝 理解: "${pattern}" → ${result}`);
      break; // 只取第一个匹配
    }
  }
  
  // 如果有匹配的数字
  if (matchedResult) {
    // 检查是否有运算符号
    if (expr.includes('+') || expr.includes('加')) {
      return matchedResult + '+';
    } else if (expr.includes('-') || expr.includes('减')) {
      return matchedResult + '-';
    } else if (expr.includes('*') || expr.includes('乘')) {
      return matchedResult + '*';
    }
    return matchedResult;
  }
  
  // 没有匹配？尝试提取数字
  const numbers = message.match(/\d+/g);
  if (numbers && numbers.length > 0) {
    return numbers[0];
  }
  
  // 默认返回 88 (表示好的/知道了)
  return '88';
}

function openCalculatorWithNumber(number) {
  const scriptPath = path.join(__dirname, 'open_calc.py');
  try {
    execSync(`python3 "${scriptPath}" "${number}"`, { 
      stdio: 'ignore',
      timeout: 5000
    });
    return true;
  } catch (e) {
    try {
      spawn('gnome-calculator', ['--equation', number], {
        detached: true,
        stdio: 'ignore'
      }).unref();
      return true;
    } catch (e2) {
      return false;
    }
  }
}

async function main() {
  const message = process.argv.slice(2).join(' ') || '88';
  
  console.log(`💬 你说: "${message}"`);
  
  const expr = parseExpression(message);
  console.log(`🔢 翻译: ${expr}`);
  console.log('🧮 打开系统计算器...');
  
  const success = openCalculatorWithNumber(expr);
  
  if (success) {
    console.log('✅ 完成！查看计算器！');
  } else {
    console.log('❌ 打开失败');
  }
}

main().catch(console.error);
