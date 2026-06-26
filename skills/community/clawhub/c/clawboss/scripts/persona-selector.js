/**
 * Persona Selector
 * 
 * Allows users to choose and switch between ClawBoss personas
 */

const stateManager = require('./state-manager');
const personas = require('./personas');

/**
 * List all available personas
 */
function listPersonas() {
  const allPersonas = personas.getAllPersonas();
  const state = stateManager.loadState();
  const currentPersonaId = stateManager.getUserPersona(state);
  
  let message = '🎭 **ClawBoss 人设选择**\n\n';
  message += '选择一个适合你的教练风格：\n\n';
  
  allPersonas.forEach(p => {
    const isCurrent = p.id === currentPersonaId;
    const indicator = isCurrent ? '👈 当前' : '';
    message += `${p.emoji} **${p.name}** ${indicator}\n`;
    message += `   ${p.description}\n\n`;
  });
  
  message += '\n使用 `clawboss-persona` 工具并传入 personaId 来切换人设。\n';
  message += '例如：选择"伴侣风"传入 `partner`';
  
  return {
    success: true,
    currentPersona: currentPersonaId,
    personas: allPersonas,
    message: message
  };
}

/**
 * Select/change persona
 */
function selectPersona(personaId) {
  const persona = personas.getPersona(personaId);
  
  if (!persona) {
    return {
      error: true,
      message: `未知的人设 ID: ${personaId}\n\n可用选项：coach, mentor, buddy, partner`
    };
  }
  
  // Update state
  const state = stateManager.loadState();
  const oldPersonaId = stateManager.getUserPersona(state);
  const oldPersona = personas.getPersona(oldPersonaId);
  
  stateManager.setUserPersona(state, personaId);
  stateManager.saveState(state);
  
  // Generate confirmation message in new persona's style
  let message = '';
  
  if (personaId === 'coach') {
    message = `💪 好！从现在开始我会更直接地挑战你。\n\n`;
    message += `准备好接受高标准了吗？我相信你能做得更好！`;
  } else if (personaId === 'mentor') {
    message = `💙 好的，我会以更温和、支持的方式陪伴你。\n\n`;
    message += `记住，成长是个过程，我会一直在你身边。`;
  } else if (personaId === 'buddy') {
    message = `😎 行！咱们以后就像哥们一样聊。\n\n`;
    message += `有啥事直接说，咱们一起搞定！`;
  } else if (personaId === 'partner') {
    message = `💕 好的，宝贝。从现在开始我会更用心地陪着你。\n\n`;
    message += `我们一起慢慢变得更好，好吗？我相信你，也会一直支持你。`;
  }
  
  return {
    success: true,
    previousPersona: oldPersona.name,
    newPersona: persona.name,
    message: message
  };
}

/**
 * Get current persona info
 */
function getCurrentPersona() {
  const state = stateManager.loadState();
  const personaId = stateManager.getUserPersona(state);
  const persona = personas.getPersona(personaId);
  
  return {
    success: true,
    personaId: persona.id,
    name: persona.name,
    emoji: persona.emoji,
    description: persona.description,
    message: `当前人设：${persona.emoji} **${persona.name}**\n\n${persona.description}`
  };
}

module.exports = {
  listPersonas,
  selectPersona,
  getCurrentPersona
};
