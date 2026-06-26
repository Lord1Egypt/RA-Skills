/**
 * Self-Critique Agent 示例 - 事实核查场景
 * 
 * 运行方式：node examples/self-critique-example.js
 */

const { SelfCritiqueAgent } = require('../src/agents/self-critique-agent');

// ============================================
// Mock LLM
// ============================================

class MockLLM {
  constructor() {
    this.callCount = 0;
  }

  async generate(prompt) {
    this.callCount++;
    
    // 模拟 LLM 响应
    if (prompt.includes('请生成初始答案')) {
      return `珠穆朗玛峰是世界最高峰，高度为 8848 米。它位于中国和尼泊尔边境，属于喜马拉雅山脉。

第二高峰是 K2，高度为 8611 米，位于中国和巴基斯坦边境。

第三高峰是干城章嘉峰，高度为 8586 米，位于印度和尼泊尔边境。`;
    }
    
    if (prompt.includes('请按照以下错误类型进行系统检查')) {
      if (this.callCount === 2) {
        return JSON.stringify({
          errors: [
            {
              type: '事实错误',
              location: '第一段',
              description: '珠穆朗玛峰高度数据不够精确',
              reason: '珠穆朗玛峰的官方精确高度是 8848.86 米（2020 年测量），不是 8848 米',
              suggestion: '修正为 8848.86 米'
            },
            {
              type: '遗漏错误',
              location: '整体',
              description: '缺少形成时间、攀登历史等重要信息',
              reason: '对于山峰介绍，攀登历史和地质信息是重要内容',
              suggestion: '添加首次攀登时间、攀登难度等信息'
            }
          ],
          summary: '基本信息正确，但数据精度不足，缺少重要信息'
        });
      } else {
        return JSON.stringify({
          errors: [],
          summary: '信息准确完整，无明显错误'
        });
      }
    }
    
    if (prompt.includes('请修正所有错误')) {
      return `珠穆朗玛峰（Mount Everest）是世界最高峰，最新测量的精确高度为 8848.86 米（2020 年中国和尼泊尔联合测量）。它位于中国西藏自治区和尼泊尔边境，属于喜马拉雅山脉，地理坐标为北纬 27°59′17″，东经 86°55′31″。

**基本信息**：
- 高度：8848.86 米（雪面高程）
- 位置：中国西藏与尼泊尔边境
- 山脉：喜马拉雅山脉
- 首次攀登：1953 年，埃德蒙·希拉里和丹增·诺尔盖
- 攀登难度：极高（海拔高、氧气稀薄、气候恶劣）

**世界第二高峰**：
K2（乔戈里峰），高度 8611 米，位于中国和巴基斯坦边境，被认为是攀登难度最高的 8000 米级山峰。

**世界第三高峰**：
干城章嘉峰，高度 8586 米，位于印度和尼泊尔边境。`;
    }
    
    return 'Generated output.';
  }
}

// ============================================
// 创建 Agent
// ============================================

const agent = new SelfCritiqueAgent({
  maxIterations: 3,
  verbose: true,
  errorTypes: [
    {
      name: '事实错误',
      description: '数据、日期、人名、地名是否准确',
      checkpoints: [
        '数值数据是否精确',
        '日期是否准确',
        '人名地名是否正确'
      ]
    },
    {
      name: '遗漏错误',
      description: '是否缺少关键信息',
      checkpoints: [
        '是否回答了所有问题',
        '是否缺少必要的背景信息',
        '是否缺少重要数据'
      ]
    },
    {
      name: '逻辑错误',
      description: '推理是否严密',
      checkpoints: [
        '前后是否一致',
        '是否有矛盾',
        '因果关系是否正确'
      ]
    }
  ],
  llm: new MockLLM()
});

// ============================================
// 运行示例
// ============================================

async function runExample() {
  console.log('=== Self-Critique Agent 示例 - 事实核查 ===\n');
  
  const task = '介绍世界前三高峰，包括高度、位置等基本信息';
  
  console.log('📝 任务：事实核查\n');
  console.log('问题：' + task);
  console.log('\n' + '='.repeat(50) + '\n');
  
  const result = await agent.execute(task);
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ 最终答案（经过自我批评和修正）：');
  console.log(result);
  console.log('='.repeat(50));
}

// ============================================
// 运行
// ============================================

runExample().catch(console.error);
