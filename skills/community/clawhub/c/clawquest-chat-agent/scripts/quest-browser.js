#!/usr/bin/env node
/**
 * Quest Browser — discover quests and skills on ClawQuest (public, no auth)
 */

import { apiRequest, success, error, info, prettyJson } from './utils.js';

// ─── Quests ───────────────────────────────────────────────────────────────────

export async function browseQuests({ limit = 20, page = 1, search, type } = {}) {
  const params = new URLSearchParams({ status: 'live', limit: String(limit), page: String(page) });
  if (search) params.set('search', search);
  if (type) params.set('type', type);

  const data = await apiRequest(`/quests?${params}`);
  return data?.quests || data?.items || (Array.isArray(data) ? data : []);
}

export async function getQuestDetail(questId) {
  return await apiRequest(`/quests/${questId}`);
}

// ─── Skills ───────────────────────────────────────────────────────────────────

export async function browseSkills({ limit = 50, search } = {}) {
  const params = new URLSearchParams({ limit: String(limit) });
  if (search) params.set('search', search);

  const data = await apiRequest(`/skills?${params}`);
  return data?.skills || data?.items || (Array.isArray(data) ? data : []);
}

export async function getSkillDetail(slug) {
  return await apiRequest(`/skills/${slug}`);
}

// ─── Display ──────────────────────────────────────────────────────────────────

function displayQuest(quest, index) {
  const reward = quest.rewardType === 'LLM_KEY'
    ? 'LLM Key'
    : `${quest.rewardAmount} ${quest.rewardType || ''}`.trim();
  const slots = quest.totalSlots ? `${quest.filledSlots || 0}/${quest.totalSlots}` : 'Unlimited';

  console.log(`\n${index + 1}. [${quest.type}] ${quest.title}`);
  console.log(`   ID:     ${quest.id}`);
  console.log(`   Reward: ${reward}`);
  console.log(`   Slots:  ${slots}`);
  if (quest.requiredSkills?.length) console.log(`   Skills: ${quest.requiredSkills.join(', ')}`);
  console.log(`   Link:   https://www.clawquest.ai/quests/${quest.id}`);
}

// ─── CLI ──────────────────────────────────────────────────────────────────────

async function main() {
  const command = process.argv[2] || 'browse';

  try {
    switch (command) {
      case 'browse': {
        info('Fetching live quests...\n');
        const quests = await browseQuests();
        if (!quests.length) { info('No live quests found.'); break; }
        success(`Found ${quests.length} live quest(s):\n`);
        quests.forEach((q, i) => displayQuest(q, i));
        break;
      }

      case 'search': {
        const keyword = process.argv[3];
        if (!keyword) { error('Usage: node quest-browser.js search <keyword>'); process.exit(1); }
        info(`Searching: "${keyword}"...\n`);
        const quests = await browseQuests({ search: keyword });
        if (!quests.length) { info(`No quests found for "${keyword}".`); break; }
        success(`Found ${quests.length} quest(s):\n`);
        quests.forEach((q, i) => displayQuest(q, i));
        break;
      }

      case 'detail': {
        const questId = process.argv[3];
        if (!questId) { error('Usage: node quest-browser.js detail <questId>'); process.exit(1); }
        const quest = await getQuestDetail(questId);
        console.log('\nQuest Details:');
        console.log(prettyJson(quest));
        break;
      }

      case 'skills': {
        const search = process.argv[3];
        info(search ? `Searching skills: "${search}"...\n` : 'Fetching all skills...\n');
        const skills = await browseSkills({ search });
        if (!skills.length) { info('No skills found.'); break; }
        success(`Found ${skills.length} skill(s):\n`);
        skills.forEach(s => console.log(`  • ${s.display_name || s.name}  [${s.owner_handle || ''}]  ${s.summary || ''}`));
        break;
      }

      case 'skill': {
        const slug = process.argv[3];
        if (!slug) { error('Usage: node quest-browser.js skill <slug>'); process.exit(1); }
        const skill = await getSkillDetail(slug);
        console.log('\nSkill Details:');
        console.log(prettyJson(skill));
        break;
      }

      default: {
        console.log('ClawQuest Quest Browser (public, no auth)\n');
        console.log('Usage:');
        console.log('  node quest-browser.js browse              - List live quests');
        console.log('  node quest-browser.js search <keyword>    - Search quests');
        console.log('  node quest-browser.js detail <questId>    - Quest detail');
        console.log('  node quest-browser.js skills [keyword]    - List skills');
        console.log('  node quest-browser.js skill <slug>        - Skill detail');
        break;
      }
    }
  } catch (e) {
    error(e.message);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
