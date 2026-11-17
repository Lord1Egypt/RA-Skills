// COC 7e 内置数据表 & KP 辅助
// 数据源：coc7空白人物卡CY23.2Plus.xlsx（丛雨，2023/04）+ 7e 守秘人规则书
// 所有数据内置，断网可用

import { rollDice, makeRng } from './dice.mjs';

// ---------- 疯狂发作表（即时症状，10 条） ----------

export const MADNESS_INSTANT = [
  '失忆：调查员只记得最后身处的安全地点，却没有来到这里的记忆。持续 1D10 轮。',
  '假性残疾：陷入心理性失明、失聪及躯体缺失感，持续 1D10 轮。',
  '暴力倾向：六亲不认的暴力行为，对周围敌人与友方无差别攻击，持续 1D10 轮。',
  '偏执：严重偏执妄想，有人窥视、同伴背叛、无人可信任，持续 1D10 轮。',
  '人际依赖：将他人误认为重要之人并努力维持关系，持续 1D10 轮。',
  '昏厥：当场昏倒，需 1D10 轮才能苏醒。',
  '逃避行为：用任何手段试图逃离当前位置，持续 1D10 轮。',
  '竭嘶底里：大笑、哭泣、嘶吼、害怕等极端情绪，持续 1D10 轮。',
  '恐惧：从恐惧症状表选择一个恐惧源，持续 1D10 轮。',
  '躁狂：从躁狂症状表选择一个躁狂诱因，持续 1D10 轮。',
];

// ---------- 疯狂发作表（总结症状，10 条） ----------

export const MADNESS_SUMMARY = [
  '失忆：回过神来身处陌生地方，忘记自己是谁。记忆会随时间恢复。',
  '被窃：1D10 小时后恢复，发觉被盗。携宝贵之物需做幸运检定。',
  '遍体鳞伤：1D10 小时后恢复，HP 减半（不造成重伤），未被窃。',
  '暴力倾向：陷入强烈暴力与破坏欲，可能毫无印象。',
  '极端信念：采取极端手段展示思想信念之一。',
  '重要之人：1D10 小时或更久，不顾一切接近重要之人。',
  '被收容：在精神病院或警察局回过神来。',
  '逃避行为：恢复清醒时发现自己在很远的地方。',
  '恐惧：患上新恐惧症。1D10 小时后恢复，开始避开恐惧源。',
  '狂躁：患上新狂躁症。1D10 小时后恢复，完全沉浸于新症状。',
];

// ---------- 恐惧症表（精选 20 条，可扩展） ----------

export const PHOBIAS = [
  '幽闭恐惧症（密闭空间）',
  '高空恐惧症（高处）',
  '黑暗恐惧症（黑暗）',
  '深海恐惧症（深海/海洋）',
  '蜘蛛恐惧症（蜘蛛）',
  '蛇类恐惧症（蛇）',
  '社交恐惧症（社交场合）',
  '不洁恐惧症（污秽/细菌）',
  '死亡恐惧症（死亡/尸体）',
  '血恐惧症（血液）',
  '火恐惧症（火焰）',
  '雷电恐惧症（雷暴）',
  '陌生恐惧症（陌生人）',
  '独处恐惧症（独自一人）',
  '镜子恐惧症（镜子）',
  '面具恐惧症（面具）',
  '人偶恐惧症（人偶/雕像）',
  '迷路恐惧症（迷失方向）',
  '尸体恐惧症（尸体）',
  '精神病恐惧症（精神疾病）',
];

// ---------- 躁狂症表（精选 20 条，可扩展） ----------

export const MANIAS = [
  '强迫清洁症（不停清洗）',
  '囤积癖（无法丢弃物品）',
  '偷窃癖（无法控制偷窃冲动）',
  '纵火癖（对火焰的迷恋）',
  '嗜睡症（不可控的睡眠）',
  '自残癖（自我伤害）',
  '多语症（无法停止说话）',
  '夸大妄想（坚信自己非凡）',
  '宗教狂热（极端宗教行为）',
  '收集癖（特定物品的强迫收集）',
  '计数癖（强迫性计数）',
  '对称癖（强迫性的对称需求）',
  '疑病症（坚信自己患病）',
  '色情狂（不可控的性冲动）',
  '裸露癖（暴露身体冲动）',
  '虚构症（编造虚假记忆）',
  '模仿症（模仿他人言行）',
  '书写癖（强迫性书写）',
  '流浪癖（不可控的游荡）',
  '嗜血癖（对血液的迷恋）',
];

// ---------- 1920s 人名表 ----------

export const NAMES_1920S = {
  // 中文男名
  male_zh: [
    '约翰', '罗伯特', '詹姆斯', '查尔斯', '乔治', '爱德华', '阿尔伯特',
    '托马斯', '亨利', '亚瑟', '弗雷德里克', '哈里', '沃尔特', '弗兰克',
  ],
  // 英文男名
  male_en: [
    'Joseph', 'William', 'Robert', 'James', 'Charles', 'George', 'Edward', 'Albert',
    'Thomas', 'Henry', 'Arthur', 'Frederick', 'Harry', 'Walter', 'Frank',
  ],
  // 中文女名
  female_zh: [
    '玛丽', '海伦', '玛格丽特', '安娜', '露丝', '多萝西', '伊丽莎白', '弗朗西斯',
    '爱丽丝', '艾琳', '艾玛', '克拉拉', '艾达', '艾拉', '格蕾丝', '弗洛伦斯',
  ],
  // 英文女名
  female_en: [
    'Mary', 'Helen', 'Margaret', 'Anna', 'Ruth', 'Dorothy', 'Elizabeth', 'Frances',
    'Alice', 'Irene', 'Emma', 'Clara', 'Ada', 'Ella', 'Grace', 'Florence',
  ],
  // 中文姓氏
  surnames_zh: [
    '史密斯', '约翰逊', '威廉姆斯', '布朗', '琼斯', '戴维斯', '米勒', '威尔逊',
    '泰勒', '安德森', '托马斯', '杰克逊', '怀特', '哈里斯', '马丁', '汤普森',
  ],
  // 英文姓氏
  surnames_en: [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Davis', 'Miller', 'Wilson',
    'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson',
  ],
};

// ---------- 1920s 职业（精选 30 个，完整数据可扩展） ----------

export const OCCUPATIONS_1920S = [
  { id: 2, name: '会计师', creditRating: [30, 70], attribute: '教育×4', skills: ['会计', '法律', '图书馆', '聆听', '说服', '侦查'], contacts: '生意伙伴，法律界，金融业界' },
  { id: 4, name: '演员-戏剧演员', creditRating: [9, 40], attribute: '教育×2+外貌×2', skills: ['技艺（表演）', '乔装', '格斗', '历史', '心理学'], contacts: '戏剧产业，报刊艺术批评家，演员公会' },
  { id: 5, name: '演员-电影演员', creditRating: [20, 90], attribute: '教育×2+外貌×2', skills: ['技艺（表演）', '乔装', '汽车驾驶', '心理学'], contacts: '电影工作室，媒体评论员，作家' },
  { id: 7, name: '精神病医生', creditRating: [10, 60], attribute: '教育×4', skills: ['法律', '聆听', '医学', '外语', '精神分析', '心理学', '科学'], contacts: '其他精神疾病研究者，医生' },
  { id: 8, name: '动物训练师', creditRating: [10, 40], attribute: '教育×2+外貌或意志×2', skills: ['跳跃', '聆听', '自然', '心理学', '科学（动物学）', '潜行', '追踪'], contacts: '动物园，马戏团，赞助人' },
  { id: 9, name: '文物学家', creditRating: [30, 70], attribute: '教育×4', skills: ['估价', '技艺', '历史', '图书馆', '外语', '侦查'], contacts: '书商，古董收藏者，历史研究学会' },
  { id: 10, name: '古董商', creditRating: [30, 50], attribute: '教育×4', skills: ['会计', '估价', '汽车驾驶', '历史', '图书馆', '导航'], contacts: '本地历史学家，其他古董商' },
  { id: 11, name: '考古学家', creditRating: [10, 40], attribute: '教育×4', skills: ['估价', '考古', '历史', '外语', '图书馆', '侦查', '机械维修', '导航'], contacts: '赞助人，博物馆，大学' },
  { id: 12, name: '建筑师', creditRating: [30, 70], attribute: '教育×4', skills: ['会计', '技艺（技术制图）', '法律', '母语', '计算机或图书馆', '说服', '心理学', '科学（数学）'], contacts: '本地建设和城市规划部门，建筑公司' },
  { id: 13, name: '艺术家', creditRating: [9, 50], attribute: '教育×2+敏捷或意志×2', skills: ['技艺', '历史或自然', '外语', '心理学', '侦查'], contacts: '美术馆，美术批评家，富有的赞助人' },
  { id: 16, name: '作家', creditRating: [9, 30], attribute: '教育×4', skills: ['技艺（文学）', '历史', '图书馆', '自然或神秘学', '外语', '母语', '心理学'], contacts: '出版社，文学评论家，历史学家' },
  { id: 17, name: '酒保', creditRating: [8, 25], attribute: '教育×2+外貌×2', skills: ['会计', '格斗（斗殴）', '聆听', '心理学', '侦查'], contacts: '常客，可能有犯罪组织' },
  { id: 18, name: '猎人', creditRating: [20, 50], attribute: '教育×2+力量或敏捷×2', skills: ['射击', '聆听或侦查', '自然', '导航', '科学（生物学）', '潜行', '追踪'], contacts: '外国政府官员，狩猎监管，前客户' },
  { id: 19, name: '书商', creditRating: [20, 40], attribute: '教育×4', skills: ['会计', '估价', '汽车驾驶', '历史', '图书馆', '母语', '外语'], contacts: '目录学家、其他书商、图书馆和大学' },
  { id: 20, name: '赏金猎人', creditRating: [9, 30], attribute: '教育×2+力量或敏捷×2', skills: ['汽车驾驶', '电子学或电气维修', '格斗或射击', '法律', '心理学', '追踪', '潜行'], contacts: '保释业者，本地警察，线人' },
  { id: 30, name: '侦探（私家）', creditRating: [9, 30], attribute: '教育×2+力量或敏捷×2', skills: ['艺术与手艺（摄影）', '法律', '图书馆', '聆听', '心理学', '侦查', '潜行'], contacts: '警察局，犯罪组织，记者' },
  { id: 35, name: '医生', creditRating: [30, 80], attribute: '教育×4', skills: ['急救', '医学', '心理学', '科学（生物学）', '科学（化学）', '聆听', '精神分析'], contacts: '医院，医学院，其他医生' },
  { id: 40, name: '记者', creditRating: [9, 30], attribute: '教育×4', skills: ['艺术与手艺（摄影）', '图书馆', '母语', '外语', '心理学', '侦查', '潜行'], contacts: '报纸编辑，警察局，地下组织' },
  { id: 50, name: '律师', creditRating: [30, 80], attribute: '教育×4', skills: ['会计', '法律', '图书馆', '母语', '说服', '心理学'], contacts: '法官，警察，政客，犯罪组织' },
  { id: 55, name: '图书馆员', creditRating: [9, 35], attribute: '教育×4', skills: ['会计', '图书馆', '母语', '外语', '历史', '心理学'], contacts: '学者，作家，学生' },
  { id: 60, name: '机械师', creditRating: [9, 40], attribute: '教育×2+敏捷×2', skills: ['机械维修', '电气维修', '汽车驾驶', '科学（物理）', '技工'], contacts: '工厂，车厂，运输公司' },
  { id: 65, name: '军人/军官', creditRating: [9, 30], attribute: '教育×2+力量或敏捷×2', skills: ['格斗', '射击', '潜行', '追踪', '急救', '导航'], contacts: '退伍军人组织，军方，政府' },
  { id: 70, name: '传教士/神职人员', creditRating: [9, 60], attribute: '教育×4', skills: ['历史', '图书馆', '母语', '外语', '心理学', '说服', '聆听'], contacts: '教会，慈善组织，社区' },
  { id: 75, name: '音乐家', creditRating: [9, 50], attribute: '教育×2+敏捷或外貌×2', skills: ['技艺（乐器）', '聆听', '心理学', '母语'], contacts: '剧院，电台，唱片公司' },
  { id: 80, name: '护士', creditRating: [9, 30], attribute: '教育×4', skills: ['急救', '医学', '心理学', '聆听', '潜行', '科学（生物学）'], contacts: '医院，医生，患者' },
  { id: 85, name: '警官/巡警', creditRating: [20, 60], attribute: '教育×2+力量或敏捷×2', skills: ['格斗（斗殴）', '射击', '法律', '聆听', '心理学', '侦查', '潜行'], contacts: '警察局，线人，记者' },
  { id: 90, name: '飞行员', creditRating: [20, 70], attribute: '教育×2+敏捷×2', skills: ['机械维修', '电气维修', '导航', '科学（物理）', '侦查'], contacts: '航空公司，军方，富有的客户' },
  { id: 95, name: '教授', creditRating: [20, 70], attribute: '教育×4', skills: ['图书馆', '母语', '外语', '心理学', '科学', '历史'], contacts: '大学，学者，学生' },
  { id: 100, name: '海员/船长', creditRating: [9, 50], attribute: '教育×2+敏捷或意志×2', skills: ['机械维修', '导航', '技工', '游泳', '格斗', '侦查'], contacts: '港口，码头工会，走私者' },
  { id: 105, name: '出租车司机', creditRating: [5, 20], attribute: '教育×2+敏捷×2', skills: ['汽车驾驶', '机械维修', '聆听', '侦查', '心理学'], contacts: '运输公司，黑社会，常客' },
];

// ---------- 武器表（精选常用武器） ----------

export const WEAPONS = [
  { name: '弓箭', skill: '弓术', damage: '1D6+半DB', range: '30码', penetrate: false, attacks: 1, magazine: 1, malfunction: 97, eras: ['1920s', '现代'], price: { '1920s': 7, '现代': 75 } },
  { name: '黄铜指虎', skill: '斗殴', damage: '1D3+1+DB', range: '接触', penetrate: false, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 1, '现代': 10 } },
  { name: '长鞭', skill: '鞭子', damage: '1D3+半DB', range: '10英尺', penetrate: false, attacks: 1, magazine: null, malfunction: null, eras: ['1920s'], price: { '1920s': 5, '现代': 50 } },
  { name: '电锯', skill: '电锯', damage: '2D8', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: 95, eras: ['现代'], price: { '1920s': null, '现代': 300 } },
  { name: '大型棍状物（棒球棍）', skill: '斗殴', damage: '1D8+DB', range: '接触', penetrate: false, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 3, '现代': 35 } },
  { name: '手斧/镰刀', skill: '斧', damage: '1D6+1+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 3, '现代': 9 } },
  { name: '大型刀具（甘蔗刀）', skill: '斗殴', damage: '1D8+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 4, '现代': 50 } },
  { name: '中型刀具（菜刀）', skill: '斗殴', damage: '1D4+2+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 2, '现代': 15 } },
  { name: '小型刀具（弹簧刀）', skill: '斗殴', damage: '1D4+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 2, '现代': 6 } },
  { name: '大型剑（马刀）', skill: '剑', damage: '1D8+1+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 30, '现代': 75 } },
  { name: '中型剑（佩剑）', skill: '剑', damage: '1D6+1+DB', range: '接触', penetrate: true, attacks: 1, magazine: null, malfunction: null, eras: ['1920s', '现代'], price: { '1920s': 15, '现代': 100 } },
  { name: '.22 小型自动手枪', skill: '手枪', damage: '1D6', range: '15码', penetrate: true, attacks: '1(3)', magazine: 6, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 25, '现代': 190 } },
  { name: '.32 左轮手枪', skill: '手枪', damage: '1D8', range: '15码', penetrate: true, attacks: '1(3)', magazine: 6, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 15, '现代': 200 } },
  { name: '.38 左轮手枪', skill: '手枪', damage: '1D10', range: '15码', penetrate: true, attacks: '1(3)', magazine: 6, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 25, '现代': 200 } },
  { name: '.38 自动手枪', skill: '手枪', damage: '1D10', range: '15码', penetrate: true, attacks: '1(3)', magazine: 8, malfunction: 99, eras: ['1920s', '现代'], price: { '1920s': 30, '现代': 375 } },
  { name: '.45 左轮手枪', skill: '手枪', damage: '1D10+2', range: '15码', penetrate: true, attacks: '1(3)', magazine: 6, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 30, '现代': 300 } },
  { name: '.45 自动手枪', skill: '手枪', damage: '1D10+2', range: '15码', penetrate: true, attacks: '1(3)', magazine: 7, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 40, '现代': 375 } },
  { name: '9mm 格洛克 17', skill: '手枪', damage: '1D10', range: '15码', penetrate: true, attacks: '1(3)', magazine: 17, malfunction: 98, eras: ['现代'], price: { '1920s': null, '现代': 500 } },
  { name: '.22 栓式步枪', skill: '步枪/霰弹枪', damage: '1D6+1', range: '30码', penetrate: true, attacks: 1, magazine: 6, malfunction: 99, eras: ['1920s', '现代'], price: { '1920s': 13, '现代': 70 } },
  { name: '.30 杠杆式步枪', skill: '步枪/霰弹枪', damage: '2D6', range: '50码', penetrate: true, attacks: 1, magazine: 6, malfunction: 98, eras: ['1920s', '现代'], price: { '1920s': 19, '现代': 150 } },
  { name: '12号双管霰弹枪', skill: '步枪/霰弹枪', damage: '2D6+2/4D6', range: '10码', penetrate: false, attacks: 1, magazine: 2, malfunction: 100, eras: ['1920s', '现代'], price: { '1920s': 25, '现代': 250 } },
  { name: '12号泵动式霰弹枪', skill: '步枪/霰弹枪', damage: '2D6+2/4D6', range: '10码', penetrate: false, attacks: '1/2', magazine: 5, malfunction: 99, eras: ['1920s', '现代'], price: { '1920s': 35, '现代': 250 } },
  { name: '汤普森冲锋枪', skill: '步枪/霰弹枪', damage: '1D10+2', range: '50码', penetrate: true, attacks: '1(5)', magazine: 50, malfunction: 95, eras: ['1920s', '现代'], price: { '1920s': 200, '现代': 1500 } },
];

// ---------- 抽签辅助 ----------

function pickFromList(list, rng = makeRng()) {
  return list[rng(0, list.length - 1)];
}

function rollTable(table, rng = makeRng()) {
  // 表是 1-indexed
  const roll = rng(1, table.length);
  return { roll, index: roll - 1, value: table[roll - 1] };
}

// ---------- 公共 API ----------

/**
 * 随机生成姓名。
 * @param {string} gender  'male' | 'female' | 'any'
 * @param {string} lang    'zh' | 'en' | 'any'（默认 'en'，符合 1920s 美国背景）
 * @param {object} rng
 */
export function randomName(gender = 'any', lang = 'en', rng = makeRng()) {
  let g = gender;
  if (g === 'any') g = rng(0, 1) === 0 ? 'male' : 'female';
  let l = lang;
  if (l === 'any') l = rng(0, 1) === 0 ? 'zh' : 'en';
  const firstKey = `${g}_${l}`;
  const lastKey = `surnames_${l}`;
  const first = pickFromList(NAMES_1920S[firstKey], rng);
  const last = pickFromList(NAMES_1920S[lastKey], rng);
  const full = l === 'zh' ? `${first}${last}` : `${first} ${last}`;
  return { first, last, full, gender: g, lang: l };
}

/**
 * 随机生成 NPC。
 * @param {string} lang  'zh' | 'en' | 'any'
 * @param {object} rng
 */
export function randomNpc(lang = 'en', rng = makeRng()) {
  const name = randomName('any', lang, rng);
  const occ = pickFromList(OCCUPATIONS_1920S, rng);
  return {
    name: name.full,
    gender: name.gender,
    lang: name.lang,
    occupation: occ.name,
    creditRating: `${occ.creditRating[0]}-${occ.creditRating[1]}`,
    skills: occ.skills,
    contacts: occ.contacts,
  };
}

export function randomPhobia(rng = makeRng()) {
  return rollTable(PHOBIAS, rng);
}

export function randomMania(rng = makeRng()) {
  return rollTable(MANIAS, rng);
}

export function randomMadnessInstant(rng = makeRng()) {
  return rollTable(MADNESS_INSTANT, rng);
}

export function randomMadnessSummary(rng = makeRng()) {
  return rollTable(MADNESS_SUMMARY, rng);
}

export function listOccupations() {
  return OCCUPATIONS_1920S;
}

export function findWeapon(name) {
  const lower = name.toLowerCase();
  return WEAPONS.find((w) => w.name.toLowerCase().includes(lower));
}

export function listWeapons() {
  return WEAPONS;
}

// ---------- 先攻列表 ----------

/**
 * 战斗先攻（按 DEX 降序）。
 * @param {Array<{name, dex, ...}>} combatants
 */
export function combatInitiative(combatants) {
  return [...combatants].sort((a, b) => b.dex - a.dex).map((c, i) => ({
    name: c.name,
    dex: c.dex,
    initiative: i + 1,
  }));
}

/**
 * 追逐战先攻（按 MOV 降序）。
 * @param {Array<{name, mov, ...}>} combatants
 */
export function chaseInitiative(combatants) {
  return [...combatants].sort((a, b) => b.mov - a.mov).map((c, i) => ({
    name: c.name,
    mov: c.mov,
    initiative: i + 1,
  }));
}

// ---------- 剧情/钩子生成器 ----------

const HOOK_SUBJECTS = ['一位失踪的学者', '一封奇怪的信件', '一座废弃的庄园', '一本古老的书', '一个奇怪的梦', '一位濒死的陌生人', '一段失落的记忆', '一艘归来的船', '一件古怪的文物', '一段诡异的歌声'];
const HOOK_THREATS = ['一只潜伏的怪物', '一个邪教组织', '一种古老的诅咒', '一个疯狂的科学实验', '一个时空裂缝', '一位不死的存在', '一种蔓延的瘟疫', '一个古老的预言', '一个异形的栖息地', '一个集体的疯狂'];
const HOOK_LOCATIONS = ['一座偏远的村庄', '一座荒废的修道院', '一艘远洋的轮船', '一座大雪封山的小屋', '一座城市的地下水道', '一座倒塌的灯塔', '一座被遗弃的精神病院', '一片迷雾弥漫的沼泽', '一座古老的图书馆', '一个地下的祭坛'];

export function generateHook(rng = makeRng()) {
  return {
    subject: pickFromList(HOOK_SUBJECTS, rng),
    threat: pickFromList(HOOK_THREATS, rng),
    location: pickFromList(HOOK_LOCATIONS, rng),
    toString() {
      return `调查员们被卷入【${this.subject}】的谜团，遭遇【${this.threat}】，地点在【${this.location}】。`;
    },
  };
}
