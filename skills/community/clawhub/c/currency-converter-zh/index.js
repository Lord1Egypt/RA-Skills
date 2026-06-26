// currency-converter 货币汇率换算
const https = require('https');

// 模拟汇率（实际使用时应调用API获取实时汇率）
const EXCHANGE_RATES = {
  USD: 1,
  CNY: 7.24,
  EUR: 0.92,
  JPY: 149.50,
  GBP: 0.79,
  HKD: 7.82,
  KRW: 1320.50,
  TWD: 31.50
};

const CURRENCY_NAMES = {
  USD: '美元',
  CNY: '人民币',
  EUR: '欧元',
  JPY: '日元',
  GBP: '英镑',
  HKD: '港币',
  KRW: '韩元',
  TWD: '台币'
};

// 货币代码识别
function detectCurrency(text) {
  const currencyMap = {
    '美元': 'USD', '美刀': 'USD', '刀': 'USD',
    '人民币': 'CNY', '块': 'CNY', '元': 'CNY',
    '欧元': 'EUR', '欧': 'EUR',
    '日元': 'JPY', '日币': 'JPY',
    '英镑': 'GBP', '磅': 'GBP',
    '港币': 'HKD', '港元': 'HKD',
    '韩元': 'KRW',
    '台币': 'TWD'
  };
  
  for (const [name, code] of Object.entries(currencyMap)) {
    if (text.includes(name)) {
      return code;
    }
  }
  
  // 检查3位大写代码
  const codeMatch = text.match(/\b[A-Z]{3}\b/);
  if (codeMatch && EXCHANGE_RATES[codeMatch[0]]) {
    return codeMatch[0];
  }
  
  return null;
}

// 提取数字
function extractNumber(text) {
  const match = text.match(/[\d.]+/);
  return match ? parseFloat(match[0]) : null;
}

module.exports = {
  name: 'currency-converter',
  description: '货币汇率换算工具',
  version: '1.0.0',
  author: '黄豆豆',
  
  // 激活条件
  activate(message) {
    const keywords = ['汇率', '换算', '美元', '人民币', '欧元', '日元', '英镑', '港币'];
    return keywords.some(k => message.includes(k));
  },
  
  async handle(context) {
    const message = context.message || '';
    const lowerMessage = message.toLowerCase();
    
    // 换算
    if (lowerMessage.includes('等于') || lowerMessage.includes('换算') || lowerMessage.includes('多少')) {
      return this.convert(message);
    }
    
    // 查询汇率
    if (lowerMessage.includes('汇率')) {
      return this.showRates();
    }
    
    // 显示帮助
    return this.showHelp();
  },
  
  convert(message) {
    const amount = extractNumber(message);
    const fromCurrency = detectCurrency(message.replace(/等于|换算|多少/g, ''));
    const toCurrency = detectCurrency(message);
    
    // 如果没有明确指定来源货币，默认从人民币开始
    let from = fromCurrency || 'CNY';
    let to = toCurrency || 'USD';
    
    // 如果两个货币相同，交换
    if (from === to) {
      from = 'CNY';
      to = fromCurrency || 'USD';
    }
    
    if (!amount) {
      return { message: '请输入金额\n例如：100美元等于多少人民币' };
    }
    
    if (!from || !to) {
      return { message: '无法识别货币类型\n支持的货币：美元、人民币、欧元、日元、英镑、港币' };
    }
    
    // 换算
    const fromRate = EXCHANGE_RATES[from];
    const toRate = EXCHANGE_RATES[to];
    const result = (amount / fromRate) * toRate;
    
    const fromName = CURRENCY_NAMES[from] || from;
    const toName = CURRENCY_NAMES[to] || to;
    
    return {
      message: `💱 货币换算结果\n\n`
        + `${amount} ${fromName} (${from}) = ${result.toFixed(2)} ${toName} (${to})\n\n`
        + `📊 参考汇率 (1 ${from}): ${(toRate / fromRate).toFixed(4)} ${to}\n\n`
        + `*汇率更新时间: ${new Date().toLocaleString('zh-CN')}*`
    };
  },
  
  showRates() {
    const base = 'USD';
    let msg = `💱 当前汇率 (基准: 1 USD)\n\n`;
    
    for (const [code, rate] of Object.entries(EXCHANGE_RATES)) {
      if (code !== base) {
        const name = CURRENCY_NAMES[code] || code;
        msg += `${code} ${name}: ${rate.toFixed(4)}\n`;
      }
    }
    
    msg += `\n💡 输入"100美元等于多少人民币"进行换算`;
    
    return { message: msg };
  },
  
  showHelp() {
    return {
      message: `💱 货币换算使用方法：

1. 换算金额：100美元等于多少人民币
2. 查询汇率：汇率
3. 直接输入：50欧元

支持的货币：
- 美元 (USD)
- 人民币 (CNY)
- 欧元 (EUR)
- 日元 (JPY)
- 英镑 (GBP)
- 港币 (HKD)

示例：
- 100美元等于多少人民币
- 5000日元
- 汇率查询`
    };
  }
};
