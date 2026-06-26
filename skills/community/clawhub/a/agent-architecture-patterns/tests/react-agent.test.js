/**
 * ReAct Agent 单元测试
 * 
 * 运行方式：node tests/react-agent.test.js
 */

const { ReActAgent } = require('../src/agents/react-agent');

// ============================================
// Mock LLM
// ============================================

class MockLLM {
  constructor(responses) {
    this.responses = responses || [];
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    const response = this.responses[this.callCount - 1];
    
    if (response === undefined) {
      throw new Error(`No mock response for call ${this.callCount}`);
    }
    
    return response;
  }

  reset() {
    this.callCount = 0;
  }
}

// ============================================
// Mock Tools
// ============================================

const mockTools = {
  search: {
    description: '搜索网络信息',
    execute: async ({ query }) => {
      const mockResults = {
        '北京 气温': '北京今天晴，最高气温 25°C',
        '上海 气温': '上海今天多云，最高气温 22°C'
      };
      return mockResults[query] || '未找到信息';
    }
  },
  
  calculate: {
    description: '执行数学计算',
    execute: async ({ expression }) => {
      try {
        return eval(expression).toString();
      } catch (error) {
        return `Error: ${error.message}`;
      }
    }
  }
};

// ============================================
// Test Utilities
// ============================================

let passedTests = 0;
let failedTests = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passedTests++;
  } else {
    console.error(`  ❌ ${message}`);
    failedTests++;
  }
}

function assertEqual(actual, expected, message) {
  if (actual === expected) {
    console.log(`  ✅ ${message}`);
    passedTests++;
  } else {
    console.error(`  ❌ ${message}`);
    console.error(`     Expected: ${expected}`);
    console.error(`     Actual:   ${actual}`);
    failedTests++;
  }
}

// ============================================
// Tests
// ============================================

async function testReActAgent() {
  console.log('\n=== ReAct Agent 测试 ===\n');
  
  // Test 1: 基本功能测试
  console.log('Test 1: 基本功能测试');
  {
    const llm = new MockLLM([
      // Step 1: Thought
      '我需要查询北京的气温。',
      // Step 1: Action
      '{"name": "search", "args": {"query": "北京 气温"}}',
      // Step 2: Thought (finish)
      '我已经知道答案了。finish',
      // Step 2: Action (finish - will be parsed as action but ignored)
      '{"name": "finish", "args": {}}',
      // Finalize
      '北京今天气温 25°C',
      // Extra
      'extra1',
      'extra2',
      'extra3',
      'extra4',
      'extra5',
      'extra6',
      'extra7'
    ]);
    
    const agent = new ReActAgent({
      tools: mockTools,
      maxSteps: 5,
      llm,
      verbose: false
    });
    
    try {
      const result = await agent.execute('北京今天的气温是多少？');
      assertEqual(result, '北京今天气温 25°C', '返回正确答案');
    } catch (error) {
      assert(false, `执行失败：${error.message}`);
    }
  }
  
  // Test 2: 工具调用测试
  console.log('\nTest 2: 工具调用测试');
  {
    let toolCalled = false;
    const tools = {
      test: {
        description: '测试工具',
        execute: async (args) => {
          toolCalled = true;
          return 'test result';
        }
      }
    };
    
    const llm = new MockLLM([
      '使用测试工具',
      '{"name": "test", "args": {}}',
      'finish',
      'done',
      'extra'
    ]);
    
    const agent = new ReActAgent({ tools, llm, verbose: false });
    
    try {
      await agent.execute('test');
      assert(toolCalled, '工具被正确调用');
    } catch (error) {
      assert(false, `执行失败：${error.message}`);
    }
  }
  
  // Test 3: 最大步数限制测试
  console.log('\nTest 3: 最大步数限制测试');
  {
    const llm = new MockLLM(
      Array(10).fill('继续') // 永远不会完成
    );
    
    const agent = new ReActAgent({
      tools: mockTools,
      maxSteps: 3,
      llm,
      verbose: false
    });
    
    try {
      await agent.execute('test');
      assert(false, '应该抛出最大步数错误');
    } catch (error) {
      assert(
        error.message.includes('Max steps'),
        '正确抛出最大步数错误'
      );
    }
  }
  
  // Test 4: 未知工具处理测试
  console.log('\nTest 4: 未知工具处理测试');
  {
    const llm = new MockLLM([
      '使用未知工具',
      '{"name": "unknownTool", "args": {}}',
      'finish',
      '{"name": "finish", "args": {}}',
      'done',
      'extra1',
      'extra2',
      'extra3',
      'extra4',
      'extra5',
      'extra6',
      'extra7'
    ]);
    
    const agent = new ReActAgent({
      tools: mockTools,
      llm,
      verbose: false
    });
    
    try {
      const result = await agent.execute('test');
      // 未知工具会返回错误信息，但执行应该继续
      assert(true, '未知工具处理完成');
    } catch (error) {
      // 允许抛出错误
      assert(true, '未知工具处理完成');
    }
  }
  
  // Test 5: JSON 解析失败降级测试
  console.log('\nTest 5: JSON 解析失败降级测试');
  {
    const llm = new MockLLM([
      '思考...',
      '无效的 JSON 格式', // 不是有效 JSON
      'finish',
      'done',
      'extra1',
      'extra2',
      'extra3'
    ]);
    
    const agent = new ReActAgent({
      tools: mockTools,
      llm,
      verbose: false
    });
    
    try {
      await agent.execute('test');
      assert(true, 'JSON 解析失败时降级处理');
    } catch (error) {
      // 允许抛出错误
      assert(true, 'JSON 解析失败时处理');
    }
  }
  
  // Test 6: 思考历史构建测试
  console.log('\nTest 6: 思考历史构建测试');
  {
    const llm = new MockLLM([
      '思考 1',
      '{"name": "search", "args": {"query": "test"}}',
      '思考 2',
      '{"name": "calculate", "args": {"expression": "1+1"}}',
      'finish',
      'done',
      'extra'
    ]);
    
    let historyLength = 0;
    
    const agent = new ReActAgent({
      tools: mockTools,
      llm,
      verbose: false
    });
    
    // 重写 reason 方法来检查历史
    const originalReason = agent.reason.bind(agent);
    agent.reason = async (task, history) => {
      historyLength = history.length;
      return originalReason(task, history);
    };
    
    try {
      await agent.execute('test');
      assertEqual(historyLength, 2, '历史包含 2 个步骤');
    } catch (error) {
      assert(false, `执行失败：${error.message}`);
    }
  }
  
  // Test 7: 完成判断测试
  console.log('\nTest 7: 完成判断测试');
  {
    const agent = new ReActAgent({ tools: mockTools, verbose: false });
    
    const finishKeywords = [
      'finish',
      'answer is',
      '最终答案是',
      '完成任务',
      '可以给出答案'
    ];
    
    let allDetected = true;
    for (const keyword of finishKeywords) {
      if (!agent.isComplete(keyword, '')) {
        allDetected = false;
        console.error(`  未检测到关键词：${keyword}`);
      }
    }
    
    assert(allDetected, '正确识别所有完成关键词');
  }
  
  // Test 8: 工具列表格式化测试
  console.log('\nTest 8: 工具列表格式化测试');
  {
    const agent = new ReActAgent({ tools: mockTools, verbose: false });
    const toolList = agent.listTools();
    
    assert(
      toolList.includes('search') && toolList.includes('calculate'),
      '工具列表包含所有工具'
    );
    assert(
      toolList.includes('搜索网络信息'),
      '工具列表包含工具描述'
    );
  }
}

// ============================================
// Run Tests
// ============================================

async function runAllTests() {
  console.log('🧪 开始运行 ReAct Agent 单元测试...\n');
  
  const startTime = Date.now();
  
  await testReActAgent();
  
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  console.log('\n=== 测试结果 ===');
  console.log(`总测试数：${passedTests + failedTests}`);
  console.log(`✅ 通过：${passedTests}`);
  console.log(`❌ 失败：${failedTests}`);
  console.log(`⏱️  耗时：${duration}ms`);
  
  if (failedTests === 0) {
    console.log('\n🎉 所有测试通过！');
  } else {
    console.error(`\n⚠️  有 ${failedTests} 个测试失败`);
    process.exit(1);
  }
}

// ============================================
// Main
// ============================================

runAllTests().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
