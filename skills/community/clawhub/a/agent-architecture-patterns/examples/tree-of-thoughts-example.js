/**
 * Tree of Thoughts Agent 示例 - 创意设计场景
 * 
 * 运行方式：node examples/tree-of-thoughts-example.js
 */

const { TreeOfThoughtsAgent } = require('../src/agents/tree-of-thoughts-agent');

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
    if (prompt.includes('请生成') && prompt.includes('个不同的思考方向')) {
      const depth = (prompt.match(/Depth: (\d+)/) || [])[1] || 0;
      
      if (depth === 0) {
        // 初始思考
        return JSON.stringify([
          { thought: '开发一个 AI 健康助手应用，通过对话提供健康建议' },
          { thought: '创建智能健身教练，使用摄像头纠正运动姿势' },
          { thought: '设计心理健康陪伴机器人，提供情感支持和冥想指导' }
        ]);
      } else if (depth === 1) {
        // 第二轮思考
        return JSON.stringify([
          { thought: 'AI 健康助手 + 饮食追踪功能' },
          { thought: 'AI 健康助手 + 运动计划定制' },
          { thought: '智能健身教练 + 实时语音指导' },
          { thought: '心理健康机器人 + 睡眠监测' }
        ]);
      } else {
        // 第三轮思考
        return JSON.stringify([
          { thought: 'AI 健康助手 + 饮食 + 运动 + 睡眠综合管理' },
          { thought: '智能健身教练 + AR 眼镜实时指导' }
        ]);
      }
    }
    
    if (prompt.includes('请评估这个思考的质量')) {
      // 模拟评分
      const scores = [7.5, 8.2, 6.8, 8.5, 7.9, 9.2, 8.8];
      const score = scores[this.callCount % scores.length];
      return score.toString();
    }
    
    if (prompt.includes('请基于这个思考路径，生成最终的解决方案')) {
      return `## FitAI - 智能健身解决方案

### 产品定位
AI 驱动的个性化健身教练，通过计算机视觉和语音指导帮助用户正确锻炼。

### 核心功能

1. **动作识别与纠正**
   - 使用摄像头实时捕捉用户动作
   - AI 对比标准动作，提供实时纠正
   - 语音反馈："膝盖再弯曲一点"、"背部保持挺直"

2. **个性化训练计划**
   - 根据用户目标（减脂/增肌/塑形）定制计划
   - 动态调整难度
   - 进度追踪和成就系统

3. **智能饮食建议**
   - 拍照识别食物
   - 卡路里计算
   - 营养搭配建议

4. **社区与竞争**
   - 健身挑战
   - 好友排行榜
   - 成就分享

### 技术栈
- 计算机视觉：MediaPipe / OpenPose
- AI 引擎：自定义训练的动作识别模型
- 前端：React Native（跨平台）
- 后端：Node.js + Python

### 商业模式
- 免费基础版（有限功能）
- 高级版：$14.99/月（完整功能）
- 企业版：健身房合作

### 竞争优势
- 实时动作纠正（差异化）
- 个性化程度高
- 价格亲民

### MVP 计划
1. 核心功能：动作识别 + 基础训练（4 周）
2. 添加：个性化计划（2 周）
3. 添加：饮食功能（2 周）
4. 测试与发布（2 周）

总计：10 周完成 MVP`;
    }
    
    return 'Generated thought.';
  }
}

// ============================================
// 创建 Agent
// ============================================

const agent = new TreeOfThoughtsAgent({
  maxDepth: 3,
  branchFactor: 3,
  beamWidth: 2,
  verbose: true,
  llm: new MockLLM()
});

// ============================================
// 运行示例
// ============================================

async function runExample() {
  console.log('=== Tree of Thoughts Agent 示例 - 创意设计 ===\n');
  
  const task = '设计一个创新的 AI 健身应用，要有差异化竞争优势';
  
  console.log('📝 任务：创意设计\n');
  console.log('需求：' + task);
  console.log('\n' + '='.repeat(50) + '\n');
  
  const result = await agent.execute(task);
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ 最终方案（经过多路径探索）：');
  console.log(result);
  console.log('='.repeat(50));
}

// ============================================
// 运行
// ============================================

runExample().catch(console.error);
