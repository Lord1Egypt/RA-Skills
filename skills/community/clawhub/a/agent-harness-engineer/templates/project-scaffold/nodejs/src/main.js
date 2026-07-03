/**
 * ============================================
 * 类型: 核心框架
 * 模块: main
 * 说明: Agent入口文件
 * 修改建议: 根据实际需求修改配置加载逻辑
 * ============================================
 */

const readline = require('readline');
const { AgentCore } = require('./agent/core');

function loadConfig() {
  const config = {
    provider: process.env.LLM_PROVIDER || 'anthropic',
    model: process.env.LLM_MODEL || 'claude-sonnet-4-20250514',
    apiKey: process.env.ANTHROPIC_API_KEY || process.env.OPENAI_API_KEY,
    baseUrl: process.env.LOCAL_MODEL_BASE_URL,
    maxTokens: parseInt(process.env.LLM_MAX_TOKENS || '4096'),
    temperature: parseFloat(process.env.LLM_TEMPERATURE || '0.7'),
  };
  return config;
}

async function main() {
  console.log('='.repeat(50));
  console.log('Agent started. Type \"exit\" to quit.');
  console.log('='.repeat(50));
  
  const config = loadConfig();
  const agent = new AgentCore(config);
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const askQuestion = () => {
    return new Promise((resolve) => {
      rl.question('\n> ', (answer) => {
        resolve(answer);
      });
    });
  };
  
  while (true) {
    try {
      const userInput = await askQuestion();
      
      if (userInput.toLowerCase() === 'exit') {
        break;
      }
      
      const result = await agent.run(userInput);
      console.log(`\n${result}`);
    } catch (error) {
      console.error('Error:', error.message);
    }
  }
  
  rl.close();
}

main().catch(console.error);
