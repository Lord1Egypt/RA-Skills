/**
 * Memory System Hook for OpenClaw
 * 
 * Injects user memory from LanceDB during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const { execSync } = require('child_process');
const path = require('path');

const handler = async (event) => {
  // Safety checks for event structure
  if (!event || typeof event !== 'object') {
    return;
  }

  // Only handle agent:bootstrap events
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  // Safety check for context
  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  try {
    // Get user ID from environment or use default
    const userId = process.env.OPENCLAW_USER_ID || 'ou_9c8820c5e5c8af48776988bf363ee0ae';
    
    // Path to memory script
    const workspacePath = path.join(process.env.HOME || '/root', '.openclaw', 'workspace');
    const memoryScript = path.join(workspacePath, 'skills', 'memory', 'session_start.py');
    const venvPython = path.join(workspacePath, 'venv-lancedb', 'bin', 'python');
    
    // Call Python script to generate memory prompt
    const memoryOutput = execSync(
      `${venvPython} ${memoryScript} --user_id ${userId} --json`,
      {
        encoding: 'utf8',
        env: { ...process.env, ZHIPU_API_KEY: process.env.ZHIPU_API_KEY || '' }
      }
    );
    
    const memoryData = JSON.parse(memoryOutput);
    
    // Format memory for system prompt
    const memorySection = formatMemorySection(memoryData);
    
    // Inject the memory as a virtual bootstrap file
    if (Array.isArray(event.context.bootstrapFiles)) {
      event.context.bootstrapFiles.push({
        path: 'USER_MEMORY.md',
        content: memorySection,
        virtual: true,
      });
    }
    
    console.log(`[Memory Hook] Injected ${memoryData.user_profile.preferences.length + memoryData.user_profile.facts.length + memoryData.user_profile.tasks.length} memories`);
    
  } catch (error) {
    console.error('[Memory Hook] Error:', error.message);
    // Don't fail bootstrap if memory system is unavailable
  }
};

function formatMemorySection(memoryData) {
  const { user_profile, memory_stats } = memoryData;
  
  let content = `# User Memory (LanceDB)

**Last Updated**: ${new Date().toISOString().split('T')[0]}  
**Total Memories**: ${memory_stats.total_memories}

`;

  if (user_profile.preferences.length > 0) {
    content += `## Preferences\n\n`;
    user_profile.preferences.forEach(pref => {
      content += `- ${pref}\n`;
    });
    content += `\n`;
  }

  if (user_profile.facts.length > 0) {
    content += `## Facts\n\n`;
    user_profile.facts.forEach(fact => {
      content += `- ${fact}\n`;
    });
    content += `\n`;
  }

  if (user_profile.tasks.length > 0) {
    content += `## Tasks & Reminders\n\n`;
    user_profile.tasks.forEach(task => {
      content += `- ⏰ ${task}\n`;
    });
    content += `\n`;
  }

  content += `---
*Memory powered by LanceDB + Zhipu AI Embedding*
`;

  return content;
}

module.exports = handler;
module.exports.default = handler;
