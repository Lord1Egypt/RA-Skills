#!/usr/bin/env node
/**
 * Japan Fish & Seafood Recipe Search
 * Searches 300 Cookpad recipes by keyword (Japanese title or English tags)
 */
const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, 'recipes.json');

if (!fs.existsSync(dataFile)) {
  console.error('Error: recipes.json not found in', __dirname);
  process.exit(1);
}

const recipes = JSON.parse(fs.readFileSync(dataFile, 'utf8'));

// Search aliases for common English queries
const aliases = {
  'salmon': ['サケ', '鮭', 'サーモン', 'Salmon'],
  'tuna': ['マグロ', 'ツナ', 'Tuna'],
  'cod': ['タラ', '鱈', 'Cod'],
  'mackerel': ['サバ', '鯖', 'Mackerel'],
  'shrimp': ['エビ', '海老', 'Shrimp'],
  'squid': ['イカ', '烏賊', 'Squid'],
  'octopus': ['タコ', '蛸', 'Octopus'],
  'scallop': ['ホタテ', '帆立', 'Scallop'],
  'crab': ['カニ', '蟹', 'Crab'],
  'eel': ['ウナギ', '鰻', 'Eel'],
  'yellowtail': ['ブリ', '鰤', 'ハマチ', 'Yellowtail'],
  'sardine': ['イワシ', '鰯', 'Sardine'],
  'clam': ['アサリ', '蛤', 'Clam'],
  'oyster': ['牡蠣', 'カキ', 'Oyster'],
  'sea bream': ['タイ', '鯛', 'Sea Bream'],
  'bonito': ['カツオ', '鰹', 'Bonito'],
  'flounder': ['カレイ', 'ヒラメ', 'Flounder'],
  'saury': ['サンマ', 'Pacific Saury'],
  'pufferfish': ['フグ', 'Pufferfish'],
  'whitebait': ['シラス', 'しらす', 'Whitebait'],
  'fish cake': ['はんぺん', 'ちくわ', 'かまぼこ', 'Fish Cake', 'Fish Tube Cake'],
  'grilled': ['焼き', 'Grilled'],
  'simmered': ['煮', '煮付け', 'Simmered', 'Soy-Simmered'],
  'fried': ['揚げ', 'フライ', 'Deep-Fried', 'Fried'],
  'steamed': ['蒸し', 'Steamed'],
  'tempura': ['天ぷら', 'Tempura'],
  'sashimi': ['刺身', 'Sashimi'],
  'sushi': ['寿司', 'Sushi'],
  'teriyaki': ['照り焼き', 'Teriyaki'],
  'meuniere': ['ムニエル', 'Meunière'],
  'karaage': ['唐揚げ', 'Karaage'],
  'nanban': ['南蛮', 'Nanban'],
  'salad': ['サラダ', 'Salad'],
  'soup': ['スープ', '汁', 'Soup'],
  'hot pot': ['鍋', 'Hot Pot'],
  'bento': ['弁当', 'お弁当', 'Bento'],
  'easy': ['簡単', '手軽', 'Easy'],
  'popular': ['人気', '定番', 'Popular'],
  'miso': ['味噌', 'Miso'],
  'butter': ['バター', 'Butter'],
  'cheese': ['チーズ', 'Cheese'],
  'mayo': ['マヨ', 'マヨネーズ', 'Mayonnaise'],
  'lemon': ['レモン', 'Lemon'],
  'garlic': ['にんにく', 'ガーリック', 'Garlic'],
  'wasabi': ['わさび', 'Wasabi'],
  'sesame': ['ごま', 'Sesame'],
  'tomato': ['トマト', 'Tomato'],
  'curry': ['カレー', 'Curry'],
  'chinese': ['中華', 'Chinese'],
  'italian': ['イタリアン', 'イタリア', 'Italian'],
  'korean': ['韓国', 'コチュジャン', 'Korean'],
  'pasta': ['パスタ', 'スパゲッティ', 'Pasta'],
  'appetizer': ['おつまみ', 'Appetizer'],
};

const query = process.argv.slice(2).join(' ').trim();

if (!query) {
  console.log('🐟 Japan Fish & Seafood Recipe Search');
  console.log('=====================================');
  console.log(`Database: ${recipes.length} recipes from Cookpad Japan`);
  console.log('');
  console.log('Usage: node search.js <query>');
  console.log('');
  console.log('Examples:');
  console.log('  node search.js salmon');
  console.log('  node search.js grilled');
  console.log('  node search.js miso butter');
  console.log('  node search.js サバ');
  console.log('  node search.js easy bento');
  console.log('');
  console.log('Fish types: salmon, tuna, cod, mackerel, shrimp, squid, octopus,');
  console.log('  scallop, crab, eel, yellowtail, sardine, clam, oyster, bonito...');
  console.log('Methods: grilled, simmered, fried, steamed, tempura, sashimi, teriyaki...');
  console.log('Flavors: miso, butter, cheese, mayo, lemon, garlic, wasabi...');
  process.exit(0);
}

// Expand query terms using aliases
function expandQuery(term) {
  const lower = term.toLowerCase();
  if (aliases[lower]) return aliases[lower];
  return [term];
}

const queryTerms = query.split(/\s+/);
const expandedTerms = queryTerms.map(expandQuery);

// Search
const results = recipes.filter(r => {
  const searchText = (r.title + ' ' + (r.tags || []).join(' ')).toLowerCase();
  
  // All expanded terms must match (AND logic across query terms)
  return expandedTerms.every(expansions => {
    // At least one expansion must match (OR within each term's aliases)
    return expansions.some(exp => {
      const expLower = exp.toLowerCase();
      return searchText.includes(expLower);
    });
  });
});

if (results.length === 0) {
  console.log(`No recipes found for: "${query}"`);
  console.log('Try: salmon, tuna, mackerel, shrimp, grilled, simmered, easy, bento');
} else {
  console.log(`🐟 Found ${results.length} recipe(s) for: "${query}"`);
  console.log('');
  for (const r of results) {
    const tags = r.tags && r.tags.length > 0 ? ` [${r.tags.join(', ')}]` : '';
    console.log(`• ${r.title}${tags}`);
    console.log(`  https://cookpad.com/jp/recipes/${r.id}`);
    console.log('');
  }
}
