/**
 * validate_format.js
 * 
 * 验证拼音双行格式是否对齐正确。
 * 用法：node validate_format.js "拼音行" "汉字行"
 * 
 * 示例：
 *   node validate_format.js "nǐ hǎo ， xiǎo péng yǒu ！" "你 好 ， 小 朋 友 ！"
 */

const pinyinLine = (process.argv[2] ?? '').trim();
const hanziLine = (process.argv[3] ?? '').trim();

if (!pinyinLine || !hanziLine) {
  console.log('用法: node validate_format.js "拼音行" "汉字行"');
  console.log('示例: node validate_format.js "nǐ hǎo ， xiǎo péng yǒu ！" "你 好 ， 小 朋 友 ！"');
  process.exit(1);
}

console.log('=== 格式验证 / Format Validation ===\n');
console.log(`拼音行 (pinyin line):  ${pinyinLine}`);
console.log(`汉字行 (hanzi line):  ${hanziLine}`);
console.log();

const punctSet = new Set([
  '，', '。', '！', '？', '、', '；', '：',
  '"', '"', "'", "'", '（', '）', '【', '】',
  '《', '》', '…', '—', '!', '?', ',', '.', ':', ';', "'", '"', '-', '·'
]);

// pinyin: space-separated syllables; spaces between hanzi chars are visual only
const pinyinSyllables = pinyinLine.split(/\s+/).filter(s => s.length > 0);
const pinyinWordSyllables = pinyinSyllables.filter(s => !punctSet.has(s));
const pinyinPunctSyllables = pinyinSyllables.filter(s => punctSet.has(s));

// hanziLine may have spaces between characters (visual spacing); collapse them
const hanziNoSpaces = hanziLine.replace(/\s+/g, '');
const hanziChars = [...hanziNoSpaces].filter(c => /[\u4e00-\u9fa5]/.test(c));
const hanziPuncts = [...hanziNoSpaces].filter(c => punctSet.has(c));

if (pinyinWordSyllables.length === hanziChars.length) {
  console.log(`✅ 拼音音节数 = 汉字数 / Pinyin syllables = Chinese chars: ${pinyinWordSyllables.length}`);
} else {
  console.log(`❌ 拼音音节数 ≠ 汉字数 / Pinyin syllables ≠ Chinese chars:`);
  console.log(`   pinyin syllables (non-punct): ${pinyinWordSyllables.length} → ${pinyinWordSyllables.join(' ')}`);
  console.log(`   hanzi chars: ${hanziChars.length} → ${hanziChars.join(' ')}`);
}

if (pinyinPunctSyllables.length === hanziPuncts.length) {
  console.log(`✅ 标点数一致 / Punctuation match: ${pinyinPunctSyllables.length}`);
} else {
  console.log(`❌ 标点数不一致 / Punctuation mismatch: pinyin=${pinyinPunctSyllables.length} (${pinyinPunctSyllables.join(' ')}), hanzi=${hanziPuncts.length} (${hanziPuncts.join('')})`);
}

const totalPinyinSlots = pinyinSyllables.length;
const totalHanziSlots = hanziChars.length + hanziPuncts.length;
if (totalPinyinSlots === totalHanziSlots) {
  console.log(`✅ 总位置数一致 / Total position slots match: ${totalPinyinSlots}`);
} else {
  console.log(`❌ 总位置数不一致 / Total position mismatch: pinyin=${totalPinyinSlots}, hanzi=${totalHanziSlots}`);
}

// Overall result
if (pinyinWordSyllables.length === hanziChars.length && pinyinPunctSyllables.length === hanziPuncts.length) {
  console.log('\n🎉 格式验证通过 / Format validation PASSED');
  process.exit(0);
} else {
  console.log('\n⚠️  格式存在问题 / Format has issues — 请检查 / Please check');
  process.exit(1);
}
