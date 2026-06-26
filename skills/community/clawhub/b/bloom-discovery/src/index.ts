/**
 * Bloom Identity Card Generator - CLI Entry Point
 *
 * OpenClaw skill wrapper for bloom-identity-skill-v2
 */

import 'dotenv/config';
import { Command } from 'commander';
import { BloomIdentitySkillV2, ExecutionMode } from './bloom-identity-skill-v2';

const program = new Command();

program
  .name('bloom-identity')
  .description('Generate Bloom Identity Card from Twitter/X and on-chain data')
  .version('4.0.0')
  .requiredOption('--user-id <userId>', 'OpenClaw user ID')
  .option('--mode <mode>', 'Execution mode: auto, manual, or hybrid', 'auto')
  .option('--skip-share', 'Skip Twitter share link generation', false)
  .parse(process.argv);

const options = program.opts();

async function main() {
  try {
    console.log('🌸 Bloom Identity Card Generator');
    console.log('================================\n');

    const skill = new BloomIdentitySkillV2();

    const result = await skill.execute(options.userId, {
      mode: options.mode as ExecutionMode,
      skipShare: options.skipShare,
    });

    if (!result.success) {
      if (result.needsManualInput) {
        console.error('\n❌ Insufficient data. Manual Q&A required.');
        console.error('Questions:', result.manualQuestions);
        process.exit(1);
      }

      console.error(`\n❌ Failed: ${result.error}`);
      process.exit(1);
    }

    // Format and output the result
    formatResult(result);

  } catch (error) {
    console.error('\n❌ Error:', error instanceof Error ? error.message : 'Unknown error');
    process.exit(1);
  }
}

function formatResult(result: any): void {
  const { identityData, recommendations, discoveries, dashboardUrl } = result;

  console.log('');
  console.log(`${getPersonalityEmoji(identityData.personalityType)} You're ${identityData.personalityType}`);
  console.log(`"${identityData.customTagline}"`);
  console.log(`Categories: ${identityData.mainCategories.join(' \u2022 ')}`);
  if (identityData.hiddenInsight) {
    console.log(`🔍 ${identityData.hiddenInsight.brief}`);
  }
  console.log('');

  if (recommendations?.length > 0 && dashboardUrl) {
    console.log(`\u2728 Your Identity Card is ready`);
    console.log(`\u2192 See your card & recommendations: ${dashboardUrl}`);
  } else if (dashboardUrl) {
    console.log(`\u2728 Your Identity Card is ready`);
    console.log(`\u2192 See your card: ${dashboardUrl}`);
  }

  // Show "New for You" discoveries on re-runs
  if (discoveries?.length > 0) {
    console.log('');
    console.log('\uD83C\uDD95 New for You:');
    for (const d of discoveries.slice(0, 5)) {
      const score = d.matchScore != null ? `${d.matchScore}%` : '';
      const source = d.source || 'Unknown';
      console.log(`   ${d.name}${score ? ` (${score} match)` : ''} \u00B7 ${source}`);
      if (d.url) console.log(`   \u2192 ${d.url}`);
    }
  }

  console.log('');
}

function getPersonalityEmoji(type: string): string {
  const emojiMap: Record<string, string> = {
    'The Visionary': '💜',
    'The Explorer': '💚',
    'The Cultivator': '🩷',
    'The Optimizer': '🧡',
    'The Innovator': '💙',
  };
  return emojiMap[type] || '🌸';
}

// Run the CLI
main();
