#!/usr/bin/env node
/**
 * Buddy Pet Generator
 * 生成随机宠物属性
 */

// ============ 数据表 ============
const SPECIES = [
  'duck', 'goose', 'blob', 'cat', 'dragon', 'octopus', 'owl', 'penguin',
  'turtle', 'snail', 'ghost', 'axolotl', 'capybara', 'cactus', 'robot',
  'rabbit', 'mushroom', 'chonk'
];

const NAMES = [
  'Flicker', 'Nano', 'Pico', 'Glimmer', 'Spark', 'Cuddles', 'Blitz',
  'Crinkle', 'Wobble', 'Pixel', 'Dizzy', 'Glitch', 'Miso', 'Tofu',
  'Biscuit', 'Mochi', 'Pudding', 'Marmalade'
];

const EYES = ['·', '✦', '×', '◉', '@', '°'];
const STAT_NAMES = ['DEBUGGING', 'PATIENCE', 'CHAOS', 'WISDOM', 'SNARK'];

const RARITY_FLOOR = {
  legendary: 50,
  epic: 35,
  rare: 25,
  uncommon: 15,
  common: 5,
};

const RARITY_STARS = {
  legendary: '★★★★★',
  epic: '★★★★☆',
  rare: '★★★☆☆',
  uncommon: '★★☆☆☆',
  common: '★☆☆☆☆',
};

// ============ ASCII Frames ============
const BODIES = {
  turtle: [
    ['   _,--._   ', '  ( ·  · )  ', ' /[______]\\ ', '  ``    ``  '],
    ['   _,--._   ', '  ( ·  · )  ', ' /[______]\\ ', '   ``  ``   '],
    ['   _,--._   ', '  ( ·  · )  ', ' /[======]\\ ', '  ``    ``  '],
  ],
  duck: [
    ['    __      ', '  <({E} )___  ', '   (  ._>   ', '    `--´    '],
    ['    __      ', '  <({E} )___  ', '   (  ._>   ', '    `--´~   '],
    ['    __      ', '  <({E} )___  ', '   (  .__>  ', '    `--´    '],
  ],
  cat: [
    ['   /\\_/\\    ', '  ( ·   ·)  ', '  (  ω  )   ', '  (")_(")   '],
    ['   /\\_/\\    ', '  ( ·   ·)  ', '  (  ω  )   ', '  (")_(")~  '],
    ['   /\\-/\\    ', '  ( ·   ·)  ', '  (  ω  )   ', '  (")_(")   '],
  ],
  blob: [
    ['   .----.   ', '  ( ·  · )  ', '  (      )  ', '   `----´   '],
    ['  .------.  ', ' (  ·  ·  ) ', ' (        ) ', '  `------´  '],
    ['    .--.    ', '   (·  ·)   ', '   (    )   ', '    `--´    '],
  ],
  ghost: [
    ['    ____    ', '   /    \\   ', '  (  · ·  ) ', '  (  ____  ) ', '   \\____/   '],
    ['    ____    ', '   /    \\   ', '  (  · ·  ) ', '  (  ----  ) ', '   /____\\   '],
    ['    ____    ', '   /    \\   ', '  (  · ·  ) ', '  (   __   ) ', '   `----`   '],
  ],
  dragon: [
    ['  /^\\  /^\\  ', ' <  ·  ·  > ', ' (   ~~   ) ', '  `-vvvv-´  '],
    ['  /^\\  /^\\  ', ' <  ·  ·  > ', ' (        ) ', '  `-vvvv-´  '],
    ['   ~    ~   ', '  /^\\  /^\\  ', ' <  ·  ·  > ', ' (   ~~   ) ', '  `-vvvv-´  '],
  ],
  owl: [
    ['   /\\  /\\   ', '  ((·)(·))  ', '  (  ><  )  ', '   `----´   '],
    ['   /\\  /\\   ', '  ((·)(·))  ', '  (  ><  )  ', '   .----.   '],
    ['   /\\  /\\   ', '  ((·)(-))  ', '  (  ><  )  ', '   `----´   '],
  ],
  penguin: [
    ['  .---.     ', '  (·>·)     ', ' /(   )\\    ', '  `---´     '],
    ['  .---.     ', '  (·>·)     ', ' |(   )|    ', '  `---´     '],
    ['  .---.     ', '  (·>·)     ', ' /(   )\\    ', '  `---´     '],
  ],
  octopus: [
    ['   .----.   ', '  ( ·  · ) ', '  (______)  ', '  /\\/\\/\\/\\  '],
    ['   .----.   ', '  ( ·  · ) ', '  (______)  ', '  \\/\\/\\/\\/  '],
    ['     o      ', '   .----.   ', '  ( ·  · ) ', '  (______)  ', '  /\\/\\/\\/\\  '],
  ],
  robot: [
    ['  [_____]   ', '  | · · |   ', '  |     |   ', '  [_____]   '],
    ['  [_____]   ', '  | · · |   ', '  |  U  |   ', '  [_____]   '],
    ['  [_____]   ', '  | ^ ^ |   ', '  |  o  |   ', '  [_____]   '],
  ],
  rabbit: [
    ['  /\\  /\\   ', ' (  ·  · ) ', '  (  ω  )   ', '  /|   |\\  ', ' (_|   |_) '],
    ['  /\\  /\\   ', ' (  ·  · ) ', '  (  ω  )   ', '  /|   |\\  ', '   (_ _)   '],
    ['  /\\  /\\   ', ' (  ·  · ) ', '  (  >w< )  ', '  /|   |\\  ', ' (_|   |_) '],
  ],
  snail: [
    [' {E}    .--.  ', '  \\  ( @ )  ', '   \\_`--´   ', '  ~~~~~~~   '],
    ['  {E}   .--.  ', '  |  ( @ )  ', '   \\_`--´   ', '  ~~~~~~~   '],
    [' {E}    .--.  ', '   \\  ( @ )  ', '   |`--´    ', '  ~~~~~~~~~  '],
  ],
  cactus: [
    ['    _  _    ', '   | || |   ', '   | || |   ', '  _| || |_  ', ' (________) '],
    ['    _  _    ', '   | || |   ', '   | || |   ', '  _| || |_  ', ' |________| '],
    ['   \\ \\/ /   ', '    \\  /    ', '    |  |    ', '   _|  |_   ', '  (______)  '],
  ],
  axolotl: [
    ['  ~    ~   ', '  < ·  · >  ', '   ( ― )   ', '  /|   |\\  ', '  / \\   / \\  '],
    ['    ~    ~  ', '   < ·  · >  ', '    ( ― )   ', '   /|   |\\  ', '   / \\   / \\  '],
    ['  ~    ~   ', '  < ·  · >  ', '   ( ı )   ', '  /|   |\\  ', '  / \\   / \\  '],
  ],
  capybara: [
    ['    ____    ', '   /    \\   ', '  (  ·  · ) ', '   (  ―  )   ', '   /|  |\\   '],
    ['    ____    ', '   /    \\   ', '  (  ·  · ) ', '   (  ―  )   ', '    ||    '],
    ['    ____    ', '   /    \\   ', '  (  ·  · ) ', '   \\  ―  /   ', '    ||    '],
  ],
  goose: [
    ['     ({E}>    ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
    ['    ({E}>     ', '     ||     ', '   _(__)_   ', '    ^^^^    '],
    ['     ({E}>>   ', '     ||     ', '   _(__)_   ', '    ~~~~    '],
  ],
  mushroom: [
    ['  .---.    ', ' (  ·  · )  ', '  `---´    ', '    | |    ', '   /   \\   '],
    ['  .---.    ', ' (  ·  · )  ', '  `---´    ', '    | |    ', '   ~~~~~   '],
    ['  .---.    ', ' (  ~~~ )  ', '  `---´    ', '    | |    ', '   /   \\   '],
  ],
  chonk: [
    ['  ______   ', ' /      \\  ', '|  ·  ·  | ', '|   __   | ', ' \\______/  '],
    ['  ______   ', ' /  __  \\  ', '|  ·  ·  | ', '|  |__|  | ', ' \\______/  '],
    ['  ______   ', ' /      \\  ', '|  ~~~~  | ', '|   __   | ', ' \\______/  '],
  ],
};

// ============ 工具函数 ============
function rng(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ============ 属性生成 ============
function generateStats() {
  return {
    DEBUGGING: rng(1, 20),
    PATIENCE: rng(1, 20),
    CHAOS: rng(1, 20),
    WISDOM: rng(1, 20),
    SNARK: rng(1, 20),
  };
}

function calcTotal(stats) {
  return Object.values(stats).reduce((a, b) => a + b, 0);
}

function getRarity(total) {
  if (total >= 50) return 'legendary';
  if (total >= 35) return 'epic';
  if (total >= 25) return 'rare';
  if (total >= 15) return 'uncommon';
  return 'common';
}

function getPersonality(stats) {
  const snark = stats.SNARK;
  const chaos = stats.CHAOS;
  const wisdom = stats.WISDOM;

  let tone = '';
  if (snark <= 20) tone = 'friendly and mild';
  else if (snark <= 40) tone = 'lightly teasing';
  else if (snark <= 60) tone = 'decidedly snarky';
  else if (snark <= 80) tone = 'acidic and biting';
  else tone = 'a master of passive aggression';

  let style = '';
  if (chaos >= 15) style = 'unpredictable';
  if (wisdom >= 15) style = (style ? style + ', yet surprisingly deep' : 'surprisingly insightful');

  return `Always ${tone}${style ? ', ' + style : ''}. Thinks most code could be shorter. Keeps you humble.`;
}

// ============ ASCII 渲染 ============
function renderASCII(species, frame = 0, eye = '·') {
  const frames = BODIES[species] || BODIES.blob;
  const frameData = frames[frame % frames.length];
  return frameData.map(line => line.replace(/\{E\}/g, eye)).join('\n');
}

// ============ 主生成函数 ============
function generatePet() {
  const species = pick(SPECIES);
  const name = pick(NAMES);
  const stats = generateStats();
  const total = calcTotal(stats);
  const rarity = getRarity(total);
  const personality = getPersonality(stats);
  const eye = pick(EYES);
  const frame = rng(0, 2);

  return {
    name,
    species,
    stats,
    total,
    rarity,
    personality,
    eye,
    frame,
    createdAt: new Date().toISOString().split('T')[0],
  };
}

// ============ 输出 ============
const pet = generatePet();

console.log(JSON.stringify(pet, null, 2));

// 如果直接运行脚本，额外输出 ASCII
console.log('\n--- ASCII Preview ---\n');
console.log(renderASCII(pet.species, pet.frame, pet.eye));
console.log(`\n🐢 ${pet.name} (${capitalize(pet.species)})`);
console.log(`Rarity: ${RARITY_STARS[pet.rarity]} ${pet.rarity}`);
console.log(`Personality: ${pet.personality}`);
