/**
 * 安全的随机数工具
 * 使用 crypto 模块替代 Math.random
 */

const crypto = require('crypto');

/**
 * 生成安全的随机整数 [min, max)
 */
function randomInt(min, max) {
  return crypto.randomInt(min, max);
}

/**
 * 生成安全的随机浮点数 [0, 1)
 */
function randomFloat() {
  return crypto.randomInt(0, 1000000) / 1000000;
}

/**
 * 打乱数组（Fisher-Yates 算法）
 */
function shuffleArray(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = randomInt(0, i + 1);
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * 从数组中随机选择一项
 */
function randomChoice(array) {
  if (array.length === 0) return undefined;
  return array[randomInt(0, array.length)];
}

/**
 * 生成范围内的随机浮点数
 */
function randomRange(min, max) {
  return min + randomFloat() * (max - min);
}

module.exports = {
  randomInt,
  randomFloat,
  shuffleArray,
  randomChoice,
  randomRange
};
