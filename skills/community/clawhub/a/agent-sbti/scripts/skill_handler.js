/**
 * Agent-SBTI: Skill 对话处理器
 */

const fs = require('fs');
const path = require('path');

const testModule = require('./test.js');
const configModule = require('./agent_config.js');
const applyModule = require('./apply.js');

const STATE_FILE = path.join(__dirname, '..', 'state.json');

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function loadState() {
  if (fs.existsSync(STATE_FILE)) {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  }
  return null;
}

function clearState() {
  if (fs.existsSync(STATE_FILE)) {
    fs.unlinkSync(STATE_FILE);
  }
}

class AgentSBTI {
  constructor() {
    this.state = loadState();
  }

  startTest() {
    this.state = {
      step: 'testing',
      currentQuestion: 0,
      answers: [],
      dimensions: null,
      personality: null,
      selectedType: null
    };
    saveState(this.state);
    return this.showQuestion(0);
  }

  showQuestion(index) {
    const q = testModule.questions[index];
    if (!q) return this.finishTest();
    
    let response = '\n📌 **第 ' + (index + 1) + '/20 题**\n\n' + q.q + '\n\n';
    q.o.forEach((opt, i) => {
      response += (i + 1) + '. ' + opt.t + '\n';
    });
    response += '\n请回复数字 1-4 选择答案';
    return response;
  }

  handleAnswer(answer) {
    const num = parseInt(answer);
    if (isNaN(num) || num < 1 || num > 4) {
      return '请输入 1-4 之间的数字';
    }
    
    this.state.answers.push(num - 1);
    this.state.currentQuestion++;
    saveState(this.state);
    
    if (this.state.currentQuestion < 20) {
      return this.showQuestion(this.state.currentQuestion);
    } else {
      return this.finishTest();
    }
  }

  finishTest() {
    this.state.dimensions = testModule.calcDimensionScore(this.state.answers);
    this.state.personality = testModule.detectPersonality(this.state.dimensions);
    this.state.step = 'selecting';
    saveState(this.state);
    
    const desc = testModule.getPersonalityDesc(this.state.personality);
    
    let response = '\n🎉 **测试完成！**\n\n';
    response += '你的 SBTI 人格类型: ' + desc.n + ' (' + this.state.personality + ')\n';
    response += '📝 "' + desc.slogan + '"\n\n';
    response += '**详细描述:**\n';
    desc.desc.forEach((d, i) => {
      response += (i + 1) + '. ' + d + '\n';
    });
    response += '\n📊 **维度得分:**\n';
    Object.entries(this.state.dimensions)
      .sort((a, b) => b[1] - a[1])
      .forEach(([dim, score]) => {
        const normalized = Math.min(5, Math.max(1, score)); const bars = '█'.repeat(normalized) + '░'.repeat(6 - normalized);
        response += dim + ': ' + bars + ' (' + score + ')\n';
      });
    
    response += '\n---\n';
    response += '\n🎭 **现在选择 Agent 性格类型:**\n\n';
    response += '1. 🔄 **互补型** - 补足你的弱点\n';
    response += '2. 📋 **同频型** - 复制你的风格\n';
    response += '3. ⚖️ **微调型** - 80%相似 + 20%强化弱点\n';
    response += '4. 🎛️ **自定义** - 自己选择人格类型\n\n';
    response += '请回复数字 1-4 选择，或说"自定义"查看所有人格类型';
    
    return response;
  }

  handleTypeSelect(selection) {
    const num = parseInt(selection);
    
    if (isNaN(num) || num < 1 || num > 4) {
      if (selection.includes('自定义') || selection.includes('看看')) {
        return this.showAllPersonalityTypes();
      }
      return '请输入 1-4 之间的数字';
    }
    
    const types = ['complement', 'same', 'mixed', 'custom'];
    const type = types[num - 1];
    
    if (type === 'custom') {
      return this.showAllPersonalityTypes();
    }
    
    return this.generateConfig(type);
  }

  showAllPersonalityTypes() {
    const configs = configModule.listPersonalityConfigs();
    
    let response = '\n🎛️ **自定义人格类型**\n\n';
    response += '你说都不喜欢？那自己选一个吧：\n\n';
    
    configs.forEach((c, i) => {
      response += (i + 1) + '. ' + c.emoji + ' **' + c.id + '** - ' + c.name + '\n';
      response += '   ' + c.style + '\n\n';
    });
    
    response += '请回复数字 1-5 选择人格类型';
    this.state.step = 'custom_selecting';
    saveState(this.state);
    
    return response;
  }

  handleCustomSelect(selection) {
    const num = parseInt(selection);
    const configs = configModule.listPersonalityConfigs();
    
    if (isNaN(num) || num < 1 || num > configs.length) {
      return '请输入 1-5 之间的数字';
    }
    
    const selected = configs[num - 1];
    return this.generateConfig('custom', selected.id);
  }

  generateConfig(type, personality) {
    const dims = this.state.dimensions;
    let result;
    
    if (type === 'custom' && personality) {
      result = configModule.generateAgentConfig(dims, 'custom', personality);
    } else {
      result = configModule.generateAgentConfig(dims, type);
    }
    
    this.state.step = 'confirming';
    this.state.selectedType = type;
    this.state.selectedPersonality = result.personality;
    this.state.config = result.config;
    this.state.soulConfig = result.soul;
    saveState(this.state);
    
    const typeNames = {
      'complement': '🔄 互补型',
      'same': '📋 同频型',
      'mixed': '⚖️ 微调型',
      'custom': '🎛️ ' + result.personality
    };
    
    let response = '\n📋 **Agent 性格配置预览**\n\n';
    response += '类型: ' + (typeNames[type] || type) + '\n\n';
    response += '**沟通风格:**\n';
    Object.entries(result.config.communication).forEach(([k, v]) => {
      response += '- ' + k + ': ' + v + '\n';
    });
    response += '\n**性格特征:**\n';
    Object.entries(result.config.personality).forEach(([k, v]) => {
      response += '- ' + k + ': ' + v + '\n';
    });
    
    response += '\n---\n';
    response += '\n🤖 **确认修改吗？**\n\n';
    response += '在修改前，我会帮你备份原配置到:\n';
    response += '`~/.openclaw/workspace/backup/agent-sbti/`\n\n';
    response += '请回复「是」确认修改，或「取消」退出';
    
    return response;
  }

  handleConfirm(confirm) {
    if (confirm.includes('取消') || confirm.includes('算了')) {
      clearState();
      return '已取消配置。随时可以说「SBTI 测试」重新开始。';
    }
    
    if (!confirm.includes('是') && !confirm.includes('确认') && !confirm.includes('好')) {
      return '请回复「是」确认修改，或「取消」退出';
    }
    
    const result = applyModule.applyConfig(this.state.soulConfig);
    
    if (!result.success) {
      return '❌ 应用失败: ' + result.error;
    }
    
    let response = '\n✅ **配置已更新！**\n\n';
    response += '📁 备份位置: ' + result.backupPath + '\n\n';
    response += '**本次修改内容:**\n';
    response += applyModule.formatChanges(result.changes) + '\n\n';
    response += '---\n\n';
    response += '如果想恢复原配置，请说「恢复原配置」。\n';
    response += '如需重新测试，请说「SBTI 测试」。';
    
    clearState();
    return response;
  }

  handleRollback() {
    const result = applyModule.rollback(0);
    
    if (!result.success) {
      return '❌ 回滚失败: ' + result.error;
    }
    
    return '✅ 已恢复到上一版本\n备份位置: ' + result.restoredFrom;
  }

  process(input) {
    if (!this.state) {
      if (input.includes('测试') || input.includes('SBTI')) {
        return this.startTest();
      }
      return null;
    }
    
    switch (this.state.step) {
      case 'testing':
        return this.handleAnswer(input);
      case 'selecting':
        return this.handleTypeSelect(input);
      case 'custom_selecting':
        return this.handleCustomSelect(input);
      case 'confirming':
        return this.handleConfirm(input);
      default:
        return null;
    }
  }

  shouldHandle(input) {
    if (!this.state) {
      return input.includes('测试') || input.includes('SBTI');
    }
    return true;
  }
}

module.exports = AgentSBTI;
