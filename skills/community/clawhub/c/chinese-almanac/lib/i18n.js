/**
 * Chinese Almanac i18n Data (三语)
 * 古典择日多语言数据
 */

const i18n = {
  // ═══════════════════════════════════════════════
  // 建除十二神 (12 Day Officers)
  // ═══════════════════════════════════════════════
  jianchu: {
    '建': { en: 'Establish', pinyin: 'Jian', emoji: '🏗️', desc_en: 'All things begin to grow', desc_zh: '万物生育', desc_ja: '万物生育' },
    '除': { en: 'Remove', pinyin: 'Chu', emoji: '🧹', desc_en: 'Remove the old, welcome the new', desc_zh: '除旧布新', desc_ja: '除旧布新' },
    '满': { en: 'Fullness', pinyin: 'Man', emoji: '🌕', desc_en: 'Abundance and fullness', desc_zh: '万物丰盈', desc_ja: '万物豊盈' },
    '平': { en: 'Balance', pinyin: 'Ping', emoji: '⚖️', desc_en: 'Stable and peaceful', desc_zh: '平稳安定', desc_ja: '平穏安定' },
    '定': { en: 'Stability', pinyin: 'Ding', emoji: '📌', desc_en: 'Stable and fixed', desc_zh: '安定稳固', desc_ja: '安定稳固' },
    '执': { en: 'Execution', pinyin: 'Zhi', emoji: '✋', desc_en: 'Execute plans, stay firm', desc_zh: '执行事务', desc_ja: '執行' },
    '破': { en: 'Destruction', pinyin: 'Po', emoji: '💥', desc_en: 'Breaking, not for new beginnings', desc_zh: '破坏冲破', desc_ja: '破壊' },
    '危': { en: 'Danger', pinyin: 'Wei', emoji: '⚠️', desc_en: 'Dangerous, proceed with caution', desc_zh: '危险之象', desc_ja: '危険' },
    '成': { en: 'Success', pinyin: 'Cheng', emoji: '✅', desc_en: 'All things come to fruition', desc_zh: '万物成就', desc_ja: '成就' },
    '收': { en: 'Harvest', pinyin: 'Shou', emoji: '🌾', desc_en: 'Harvest, collecting and storing', desc_zh: '收获之日', desc_ja: '収穫' },
    '开': { en: 'Opening', pinyin: 'Kai', emoji: '🚪', desc_en: 'Open and auspicious', desc_zh: '开放通达', desc_ja: '開放' },
    '闭': { en: 'Closing', pinyin: 'Bi', emoji: '🔒', desc_en: 'Closing and conserving', desc_zh: '关闭收敛', desc_ja: '閉鎖' },
  },

  // ═══════════════════════════════════════════════
  // 黄道黑道十二神 (Yellow/Black Road Stars)
  // ═══════════════════════════════════════════════
  huangdao: {
    yellow: [
      { zh: '青龙', en: 'Azure Dragon', emoji: '🐉', level: 'great' },
      { zh: '明堂', en: 'Bright Hall', emoji: '🏛️', level: 'great' },
      { zh: '金匮', en: 'Golden Coffer', emoji: '💰', level: 'great' },
      { zh: '天德', en: 'Heavenly Virtue', emoji: '✨', level: 'great' },
      { zh: '玉堂', en: 'Jade Hall', emoji: '🏯', level: 'great' },
      { zh: '司命', en: 'Destiny Lord', emoji: '📋', level: 'minor' },
    ],
    black: [
      { zh: '天刑', en: 'Heavenly Punishment', emoji: '⚖️', level: 'minor' },
      { zh: '朱雀', en: 'Vermilion Bird', emoji: '🔴', level: 'minor' },
      { zh: '白虎', en: 'White Tiger', emoji: '🐅', level: 'great' },
      { zh: '天牢', en: 'Heavenly Prison', emoji: '🔒', level: 'great' },
      { zh: '玄武', en: 'Black Warrior', emoji: '🐢', level: 'great' },
      { zh: '勾陈', en: 'Great Chen', emoji: '🐍', level: 'minor' },
    ],
  },

  // ═══════════════════════════════════════════════
  // 彭祖百忌 (Pengzu Taboos)
  // ═══════════════════════════════════════════════
  pengzu: {
    stems: {
      '甲': { zh: '甲不开仓财物耗散', en: 'Do not open storehouses — wealth will scatter' },
      '乙': { zh: '乙不栽植千株不长', en: 'Do not plant — seedlings won\'t grow' },
      '丙': { zh: '丙不修灶必见灾殃', en: 'Do not repair stoves — disaster will follow' },
      '丁': { zh: '丁不剃头头必生疮', en: 'Do not shave heads — sores will appear' },
      '戊': { zh: '戊不受田田主不祥', en: 'Do not accept farmland — bad omen' },
      '己': { zh: '己不破券二比并亡', en: 'Do not tear contracts — both parties lose' },
      '庚': { zh: '庚不经络织机虚张', en: 'Do not weave — the loom will be empty' },
      '辛': { zh: '辛不合酱主人不尝', en: 'Do not make sauce — the master won\'t taste it' },
      '壬': { zh: '壬不汲水更难防备', en: 'Do not draw water — hard to prevent trouble' },
      '癸': { zh: '癸不词讼理弱敌强', en: 'Do not file lawsuits — you\'ll be outmatched' },
    },
    branches: {
      '子': { zh: '子不问卜自惹祸殃', en: 'Do not divine — you\'ll invite disaster' },
      '丑': { zh: '丑不冠带主不还乡', en: 'Do not wear ceremonial hats — won\'t return home' },
      '寅': { zh: '寅不祭祀神鬼不尝', en: 'Do not worship — spirits won\'t accept offerings' },
      '卯': { zh: '卯不穿井水泉不香', en: 'Do not dig wells — water won\'t be sweet' },
      '辰': { zh: '辰不哭泣必主重丧', en: 'Do not weep — another funeral will follow' },
      '巳': { zh: '巳不远行财物伏藏', en: 'Do not travel far — wealth will be hidden' },
      '午': { zh: '午不苫盖屋主更张', en: 'Do not cover with mats — house will change owners' },
      '未': { zh: '未不服药毒气入肠', en: 'Do not take medicine — toxins will enter' },
      '申': { zh: '申不安床鬼祟入房', en: 'Do not make beds — evil spirits will enter' },
      '酉': { zh: '酉不宴客醉坐颠狂', en: 'Do not host banquets — guests will go mad' },
      '戌': { zh: '戌不吃犬作怪上床', en: 'Do not eat dog meat — monsters will haunt' },
      '亥': { zh: '亥不嫁娶不利新郎', en: 'Do not marry — bad for the groom' },
    },
  },

  // ═══════════════════════════════════════════════
  // 天干地支 (Heavenly Stems & Earthly Branches)
  // ═══════════════════════════════════════════════
  stems: ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'],
  branches: ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'],

  stemEn: {
    '甲': 'Jia (Yang Wood)', '乙': 'Yi (Yin Wood)',
    '丙': 'Bing (Yang Fire)', '丁': 'Ding (Yin Fire)',
    '戊': 'Wu (Yang Earth)', '己': 'Ji (Yin Earth)',
    '庚': 'Geng (Yang Metal)', '辛': 'Xin (Yin Metal)',
    '壬': 'Ren (Yang Water)', '癸': 'Gui (Yin Water)',
  },

  branchEn: {
    '子': 'Zi (Rat)', '丑': 'Chou (Ox)', '寅': 'Yin (Tiger)',
    '卯': 'Mao (Rabbit)', '辰': 'Chen (Dragon)', '巳': 'Si (Snake)',
    '午': 'Wu (Horse)', '未': 'Wei (Goat)', '申': 'Shen (Monkey)',
    '酉': 'You (Rooster)', '戌': 'Xu (Dog)', '亥': 'Hai (Pig)',
  },

  // ═══════════════════════════════════════════════
  // 活动类型 (Activity Types)
  // ═══════════════════════════════════════════════
  activities: {
    marriage:   { zh: '嫁娶', en: 'Marriage', ja: '結婚', emoji: '💒' },
    business:   { zh: '开业', en: 'Opening Business', ja: '開業', emoji: '🏪' },
    move:       { zh: '搬家', en: 'Moving', ja: '引越し', emoji: '🏠' },
    sign:       { zh: '签约', en: 'Signing Contracts', ja: '契約', emoji: '📝' },
    travel:     { zh: '出行', en: 'Travel', ja: '旅行', emoji: '✈️' },
    renovate:   { zh: '装修', en: 'Renovation', ja: '改装', emoji: '🔨' },
    worship:    { zh: '祭祀', en: 'Worship', ja: '祈り', emoji: '🙏' },
    wealth:     { zh: '求财', en: 'Seeking Wealth', ja: '金運', emoji: '💰' },
    start_job:  { zh: '上任', en: 'Starting New Job', ja: '就任', emoji: '👔' },
    engagement: { zh: '订婚', en: 'Engagement', ja: '約束', emoji: '💍' },
  },

  // ═══════════════════════════════════════════════
  // 标签 (Labels)
  // ═══════════════════════════════════════════════
  labels: {
    en: {
      title: 'Chinese Almanac — Date Selection',
      date: 'Date', dayGanZhi: 'Day Pillar', officer: 'Day Officer',
      huangdao: 'Yellow/Black Road', good: 'Auspicious', bad: 'Inauspicious',
      tianDe: 'Heavenly Virtue', pengzu: 'Pengzu Taboo',
      score: 'Score', yi: 'Do', ji: 'Don\'t',
      bestDays: 'Best Days', allDays: 'All Days',
      yellowRoad: 'Yellow Road (Auspicious)', blackRoad: 'Black Road (Inauspicious)',
      great: 'Great Fortune', minor: 'Minor Fortune',
      greatBad: 'Great Misfortune', minorBad: 'Minor Misfortune',
      bestDate: 'Best Date', summary: 'Summary',
    },
    zh: {
      title: '古典择日 — 黄历查询',
      date: '日期', dayGanZhi: '日柱', officer: '建除十二神',
      huangdao: '黄道黑道', good: '吉', bad: '凶',
      tianDe: '天德月德', pengzu: '彭祖百忌',
      score: '评分', yi: '宜', ji: '忌',
      bestDays: '最佳日期', allDays: '所有日期',
      yellowRoad: '黄道（吉）', blackRoad: '黑道（凶）',
      great: '大吉', minor: '小吉',
      greatBad: '大凶', minorBad: '小凶',
      bestDate: '最佳日期', summary: '总结',
    },
    ja: {
      title: '中国暦 — 日取り選定',
      date: '日付', dayGanZhi: '日柱', officer: '建除十二神',
      huangdao: '黄道黒道', good: '吉', bad: '凶',
      tianDe: '天徳月徳', pengzu: '彭祖百忌',
      score: 'スコア', yi: '宜', ji: '忌',
      bestDays: '最適な日', allDays: 'すべての日',
      yellowRoad: '黄道（吉）', blackRoad: '黒道（凶）',
      great: '大吉', minor: '小吉',
      greatBad: '大凶', minorBad: '小凶',
      bestDate: '最適な日', summary: 'まとめ',
    },
  },
};

module.exports = i18n;
