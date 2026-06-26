/**
 * ReAct Agent 示例 - 单 Agent 架构模式
 * 
 * 运行方式：node examples/react-example.js
 */

const { ReActAgent } = require('../src/agents/react-agent');

// ============================================
// 1. 定义工具
// ============================================

const tools = {
  // 工具 1: 网络搜索
  search: {
    description: '搜索网络信息。适用于查询事实、新闻、数据等。',
    execute: async ({ query }) => {
      console.log(`  [Tool: search] Query: ${query}`);
      
      // 模拟搜索结果（实际实现调用搜索 API）
      const mockResults = {
        '北京 气温': '北京今天晴，最高气温 25°C，最低气温 15°C',
        '上海 气温': '上海今天多云，最高气温 22°C，最低气温 18°C',
        '珠穆朗玛峰 高度': '8848.86 米',
        'K2 高度': '8611 米',
        'JavaScript 创始人': 'Brendan Eich',
        'Python 创始人': 'Guido van Rossum'
      };
      
      return mockResults[query] || `未找到"${query}"的相关信息`;
    }
  },
  
  // 工具 2: 数学计算
  calculate: {
    description: '执行数学计算。适用于加减乘除、幂运算等。',
    execute: async ({ expression }) => {
      console.log(`  [Tool: calculate] Expression: ${expression}`);
      
      try {
        // 安全计算（实际实现应该用更安全的表达式解析器）
        const result = eval(expression);
        return result.toString();
      } catch (error) {
        return `计算错误：${error.message}`;
      }
    }
  },
  
  // 工具 3: 文件读取
  readFile: {
    description: '读取文件内容。适用于读取本地文件。',
    execute: async ({ path }) => {
      console.log(`  [Tool: readFile] Path: ${path}`);
      
      // 模拟文件读取（实际实现调用 fs.readFile）
      const mockFiles = {
        'config.json': '{"name": "my-app", "version": "1.0.0"}',
        'package.json': '{"name": "example", "dependencies": {"express": "^4.18.0"}}'
      };
      
      return mockFiles[path] || `文件不存在：${path}`;
    }
  }
};

// ============================================
// 2. 创建 Agent
// ============================================

const agent = new ReActAgent({
  tools,
  maxSteps: 10,
  verbose: true  // 启用详细日志
});

// ============================================
// 3. 运行示例
// ============================================

async function runExamples() {
  console.log('=== ReAct Agent 示例 ===\n');
  
  // 示例 1: 简单查询
  console.log('📝 示例 1: 简单查询');
  console.log('任务：北京今天的气温是多少？\n');
  
  const answer1 = await agent.execute('北京今天的气温是多少？');
  console.log(`\n答案：${answer1}\n`);
  console.log('---\n');
  
  // 示例 2: 比较查询
  console.log('📝 示例 2: 比较查询');
  console.log('任务：北京今天的气温比上海高还是低？\n');
  
  const answer2 = await agent.execute('北京今天的气温比上海高还是低？');
  console.log(`\n答案：${answer2}\n`);
  console.log('---\n');
  
  // 示例 3: 计算任务
  console.log('📝 示例 3: 计算任务');
  console.log('任务：珠穆朗玛峰比 K2 高多少米？\n');
  
  const answer3 = await agent.execute('珠穆朗玛峰比 K2 高多少米？');
  console.log(`\n答案：${answer3}\n`);
  console.log('---\n');
  
  // 示例 4: 多步骤任务
  console.log('📝 示例 4: 多步骤任务');
  console.log('任务：JavaScript 和 Python 的创始人是谁？他们分别是哪国人？\n');
  
  const answer4 = await agent.execute('JavaScript 和 Python 的创始人是谁？他们分别是哪国人？');
  console.log(`\n答案：${answer4}\n`);
  console.log('---\n');
  
  console.log('=== 示例完成 ===');
}

// ============================================
// 4. 运行
// ============================================

runExamples().catch(console.error);
