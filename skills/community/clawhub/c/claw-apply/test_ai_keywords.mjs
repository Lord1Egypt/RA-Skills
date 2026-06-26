/**
 * test_ai_keywords.mjs — Test AI-generated search terms with full context
 */
import { readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { generateKeywords } from './lib/keywords.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));
const profile = JSON.parse(readFileSync(resolve(__dir, 'config/profile.json'), 'utf8'));
const searchConfig = JSON.parse(readFileSync(resolve(__dir, 'config/search_config.json'), 'utf8'));
const apiKey = process.env.ANTHROPIC_API_KEY;

async function main() {
  console.log('🤖 AI keyword generation — full context test\n');

  for (const search of searchConfig.searches) {
    console.log(`\n━━ ${search.name} ━━`);
    console.log('Static keywords:', search.keywords.join(', '));
    console.log('\nGenerating AI keywords...');

    const keywords = await generateKeywords(search, profile, apiKey);
    console.log(`\nAI generated (${keywords.length}):`);
    keywords.forEach((k, i) => console.log(`  ${i+1}. "${k}"`));

    const merged = [...new Set([...search.keywords, ...keywords])];
    console.log(`\nMerged total: ${merged.length} unique queries`);
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
