const { pinyin } = require('pinyin-pro');

// 自定义词典（词组优先）
const phraseOverrides = {
  // 多音字词组
  "重庆": "chóng qìng",
  "银行": "yín háng",
  "行为": "xíng wéi",
  "快乐": "kuài lè",
  "音乐": "yīn yuè",
  "长大": "zhǎng dà",
  "校长": "xiào zhǎng",
  "长度": "cháng dù",
  "长发": "cháng fà",
  "长跑": "cháng pǎo",
  "长江": "cháng jiāng",
  "长沙": "cháng shā",
  "长城": "cháng chéng",
  "长征": "cháng zhēng",
  "长期": "cháng qī",
  "重写": "chóng xiě",
  "重新": "chóng xīn",
  "重要": "zhòng yào",
  "重点": "zhòng diǎn",
  "重量": "zhòng liàng",
  "重力": "zhòng lì",
  "电影": "diàn yǐng",
  "安排": "ān pái",
  "因为": "yīn wèi",
  "所以": "suǒ yǐ",
  "但是": "dàn shì",
  "如果": "rú guǒ",
  "已经": "yǐ jīng",
  "这里": "zhè lǐ",
  "那里": "nà lǐ",
  "哪里": "nǎ lǐ",
  "什么": "shén me",
  "怎么": "zěn me",
  "多么": "duō me",
  "唱歌": "chàng gē",
  "听了": "tīng le",
  "大了": "dà le",
  "小的": "xiǎo de",
  "好的": "hǎo de",
  "是的": "shì de",
  "有的": "yǒu de",
  "头发": "tóu fa",
  "豆腐": "dòu fu",
  "萝卜": "luó bo",
  "黄瓜": "huáng gua",
  "葡萄": "pú tao",
  "西瓜": "xī gua",
  "玉米": "yù mǐ",
  "土豆": "tǔ dòu",
  "阿姨": "ā yí",
  "叔叔": "shū shu",
  "舅舅": "jiù jiu",
  "姑姑": "gū gu",
  "伯伯": "bó bo",
  "外公": "wài gōng",
  "外婆": "wài pó",
  "爷爷": "yé ye",
  "奶奶": "nǎi nai",
  "地方": "dì fāng",
};

// 单字纠错（覆盖 pinyin-pro 不准的情况）
const charOverrides = {
  "虾": "xiā",
  "了": "le",
  "的": "de",
  "着": "zhe",
  "过": "guo",
  "得": "de",
  "地": "de",
  "啊": "a",
  "呀": "ya",
  "吗": "ma",
  "呢": "ne",
  "吧": "ba",
  "哦": "o",
  "呐": "na",
  "哩": "li",
};

// 符号直接返回
const isPunct = (c) => /[，。！？、；：""''（）【】《》…—\s]/.test(c);
const isChinese = (c) => /[\u4e00-\u9fa5]/.test(c);
const isEmoji = (c) => /[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F600}-\u{1F64F}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]/u.test(c) || (c.charCodeAt(0) >= 0xd800 && c.charCodeAt(0) <= 0xdbff);

function hasChineseOrPunct(text) {
  for (const c of text) {
    if (isChinese(c) || isPunct(c)) return true;
  }
  return false;
}

function segmentAndPinyin(text) {
  // 额外短语纠错（本地优先于 pinyin-pro）
  const extraPhraseOverrides = {
    "学习": "xué xí",
    "开始": "kāi shǐ",
    "认识": "rèn shi",
  };

  // 词组优先匹配
  const result = [];
  let i = 0;
  
  while (i < text.length) {
    // 处理emoji（2字符surrogate pair）
    let charLen = 1;
    let char = text[i];
    if (char.charCodeAt(0) >= 0xd800 && char.charCodeAt(0) <= 0xdbff) {
      charLen = 2;
      char = text.substring(i, i + 2);
    }
    
    // 标点符号直接保留
    if (isPunct(char) || /\s/.test(char)) {
      result.push({ char, pinyin: char });
      i += charLen;
      continue;
    }
    
    // 非汉字直接保留（如emoji）
    if (!isChinese(char)) {
      result.push({ char, pinyin: char });
      i += charLen;
      continue;
    }
    
    // 尝试最长词组匹配
    let matched = false;
    // 从长到短尝试
    for (let len = Math.min(4, text.length - i); len >= 1; len--) {
      const phrase = text.substring(i, i + len);
      // 优先使用 extraPhraseOverrides（本地纠错），再使用 phraseOverrides
      if (extraPhraseOverrides[phrase]) {
        const pys = extraPhraseOverrides[phrase].split(' ');
        for (let j = 0; j < phrase.length; j++) {
          const c = phrase[j];
          if (isChinese(c)) {
            result.push({ char: c, pinyin: pys[j] || pys[0] });
          }
        }
        i += phrase.length;
        matched = true;
        break;
      }
      if (phraseOverrides[phrase]) {
        const pys = phraseOverrides[phrase].split(' ');
        for (let j = 0; j < phrase.length; j++) {
          const c = phrase[j];
          if (isChinese(c)) {
            result.push({ char: c, pinyin: pys[j] || pys[0] });
          }
        }
        i += phrase.length;
        matched = true;
        break;
      }
    }
    
    if (matched) continue;
    
    // 查单字纠错
    if (charOverrides[char]) {
      result.push({ char, pinyin: charOverrides[char] });
    } else {
      // 用 pinyin-pro
      const py = pinyin(char);
      result.push({ char, pinyin: py });
    }
    i += charLen;
  }
  
  return result;
}

function toPinyinTwoLine(text) {
  // 输入验证：空内容或纯emoji
  if (!text || text.trim() === '') {
    return '【请输入需要转换拼音的中文文本】\n【Please enter Chinese text to convert to pinyin】';
  }
  
  // 检查是否有中文字符或标点
  if (!hasChineseOrPunct(text)) {
    return `【无法识别中文内容】\n${text}`;
  }
  
  const segments = segmentAndPinyin(text);
  
  // 拼音行
  const pinyinLine = segments.map(s => s.pinyin).join(' ');
  // 汉字行
  const hanziLine = segments.map(s => s.char).join(' ');
  
  return pinyinLine + '\n' + hanziLine;
}

const text = process.argv[2];
if (!text) {
  console.log('Usage: node to_pinyin.js "中文文本"');
  console.log('示例 / Example: node to_pinyin.js "你好，小朋友！"');
  process.exit(1);
}
console.log(toPinyinTwoLine(text));
