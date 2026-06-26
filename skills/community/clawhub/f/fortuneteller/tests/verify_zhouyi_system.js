#!/usr/bin/env node
const assert = require("node:assert/strict");
const zhouyi = require("../data/zhouyi-benjing.js");

const trigrams = {
  "111": "乾",
  "110": "兑",
  "101": "离",
  "100": "震",
  "011": "巽",
  "010": "坎",
  "001": "艮",
  "000": "坤"
};

const lookup = {
  "乾|乾": 1, "乾|兑": 43, "乾|离": 14, "乾|震": 34, "乾|巽": 9, "乾|坎": 5, "乾|艮": 26, "乾|坤": 11,
  "兑|乾": 10, "兑|兑": 58, "兑|离": 38, "兑|震": 54, "兑|巽": 61, "兑|坎": 60, "兑|艮": 41, "兑|坤": 19,
  "离|乾": 13, "离|兑": 49, "离|离": 30, "离|震": 55, "离|巽": 37, "离|坎": 63, "离|艮": 22, "离|坤": 36,
  "震|乾": 25, "震|兑": 17, "震|离": 21, "震|震": 51, "震|巽": 42, "震|坎": 3, "震|艮": 27, "震|坤": 24,
  "巽|乾": 44, "巽|兑": 28, "巽|离": 50, "巽|震": 32, "巽|巽": 57, "巽|坎": 48, "巽|艮": 18, "巽|坤": 46,
  "坎|乾": 6, "坎|兑": 47, "坎|离": 64, "坎|震": 40, "坎|巽": 59, "坎|坎": 29, "坎|艮": 4, "坎|坤": 7,
  "艮|乾": 33, "艮|兑": 31, "艮|离": 56, "艮|震": 62, "艮|巽": 53, "艮|坎": 39, "艮|艮": 52, "艮|坤": 15,
  "坤|乾": 12, "坤|兑": 45, "坤|离": 35, "坤|震": 16, "坤|巽": 20, "坤|坎": 8, "坤|艮": 23, "坤|坤": 2
};

function resolve(bits) {
  const lower = trigrams[bits.slice(0, 3)];
  const upper = trigrams[bits.slice(3, 6)];
  return zhouyi[lookup[`${lower}|${upper}`] - 1];
}

assert.equal(zhouyi.length, 64);
for (const hex of zhouyi) {
  assert.equal(hex.lines.length, 6, `${hex.number} ${hex.name} should have 6 lines`);
  assert.ok(hex.judgment, `${hex.number} ${hex.name} should have judgment`);
}

assert.equal(zhouyi[0].name, "乾");
assert.equal(zhouyi[0].extras[0].label, "用九");
assert.equal(zhouyi[1].name, "坤");
assert.equal(zhouyi[1].extras[0].label, "用六");
assert.equal(zhouyi[2].lines[1].text, "屯如邅如，乘馬班如。匪寇婚媾，女子貞不字，十年乃字。");

assert.equal(resolve("111111").name, "乾");
assert.equal(resolve("000000").name, "坤");
assert.equal(resolve("111000").name, "泰");
assert.equal(resolve("000111").name, "否");
assert.equal(resolve("101010").name, "既濟");
assert.equal(resolve("010101").name, "未濟");
assert.equal(resolve("011101").name, "鼎");
assert.equal(resolve("001101").name, "旅");

const sourceRules = [
  "六爻不变：本卦卦辞",
  "一爻变：该动爻爻辞",
  "二爻变：两条动爻爻辞，以上爻为主",
  "三爻变：本卦卦辞与变卦卦辞",
  "四爻变：两条静爻爻辞，以下爻为主",
  "五爻变：变卦中唯一静爻所对应的爻辞",
  "六爻皆变：乾用用九，坤用用六，其他用变卦卦辞"
];
assert.equal(sourceRules.length, 7);

console.log("zhouyi system verification passed");
