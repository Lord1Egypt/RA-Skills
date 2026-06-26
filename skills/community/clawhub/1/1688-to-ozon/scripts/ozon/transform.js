#!/usr/bin/env node
/**
 * 智能转换函数库
 * 用于 1688 数据 → OZON 属性的智能转换
 */

const fs = require('fs');
const path = require('path');

// 加载字典（旧版：简单映射）
const COLORS_FILE = path.join(__dirname, '../attributes/colors.json');
const MATERIALS_FILE = path.join(__dirname, '../attributes/materials.json');
const AGE_RANGES_FILE = path.join(__dirname, '../attributes/age_ranges.json');

// 加载字典值（新版：OZON API 字典值 ID）
const COLOR_DICT_FILE = path.join(__dirname, '../attributes/color_dict.json');
const MATERIAL_DICT_FILE = path.join(__dirname, '../attributes/material_dict.json');
const AGE_DICT_FILE = path.join(__dirname, '../attributes/age_dict.json');

let colorsDict = null;
let materialsDict = null;
let ageRangesDict = null;

let colorDictValues = null;
let materialDictValues = null;
let ageDictValues = null;

/**
 * 懒加载字典（支持文件不存在的情况）
 */
function loadDictionaries() {
  // 加载基础字典（如果存在）
  if (!colorsDict && fs.existsSync(COLORS_FILE)) {
    colorsDict = JSON.parse(fs.readFileSync(COLORS_FILE, 'utf-8'));
  } else if (!colorsDict) {
    colorsDict = { colors: {}, common_colors: { colors: [{ ru: 'Белый' }, { ru: 'Чёрный' }, { ru: 'Красный' }] } };
  }
  
  if (!materialsDict && fs.existsSync(MATERIALS_FILE)) {
    materialsDict = JSON.parse(fs.readFileSync(MATERIALS_FILE, 'utf-8'));
  } else if (!materialsDict) {
    materialsDict = { materials: {}, default: 'Дерево' };  // 木材（儿童玩具常用）
  }
  
  if (!ageRangesDict && fs.existsSync(AGE_RANGES_FILE)) {
    ageRangesDict = JSON.parse(fs.readFileSync(AGE_RANGES_FILE, 'utf-8'));
  } else if (!ageRangesDict) {
    ageRangesDict = { age_ranges: {}, default: 'От 3 лет' };  // 从 3 岁起
  }
  
  // 加载字典值（可选）
  if (!colorDictValues && fs.existsSync(COLOR_DICT_FILE)) {
    colorDictValues = JSON.parse(fs.readFileSync(COLOR_DICT_FILE, 'utf-8'));
  }
  if (!materialDictValues && fs.existsSync(MATERIAL_DICT_FILE)) {
    materialDictValues = JSON.parse(fs.readFileSync(MATERIAL_DICT_FILE, 'utf-8'));
  }
  if (!ageDictValues && fs.existsSync(AGE_DICT_FILE)) {
    ageDictValues = JSON.parse(fs.readFileSync(AGE_DICT_FILE, 'utf-8'));
  }
}

/**
 * 颜色智能转换（返回俄文）
 * 规则：
 * 1. 有明确颜色 → 翻译为俄文
 * 2. 多色/无色/未知 → 从常见 3 色随机
 */
function smartColor(color) {
  loadDictionaries();
  
  if (!color || color === '无' || color === 'null') {
    return getRandomCommonColor();
  }
  
  // 检查是否在字典中
  const translated = colorsDict.colors[color];
  if (translated) {
    return translated;
  }
  
  // 多色/混色处理
  if (color.includes('多') || color.includes('混') || color === '彩色') {
    return getRandomCommonColor();
  }
  
  // 未知颜色，返回默认
  console.warn(`⚠️ 未知颜色 "${color}"，使用默认值`);
  return getRandomCommonColor();
}

/**
 * 颜色智能匹配（返回 3 个随机颜色的 value_id 数组）⭐ 简化版
 * 规则：
 * 1. 从 56 种颜色字典中随机选 3 个
 * 2. 排除"多色"和"透明色"
 * 3. 返回 3 个颜色的 value_id
 */
function smartColorMatch(color) {
  loadDictionaries();
  
  if (!colorDictValues || !colorDictValues.values) {
    // 字典不存在，返回空数组
    return { values: [] };
  }
  
  // 过滤掉"多色"和"透明色"
  const availableColors = colorDictValues.values.filter(v => 
    v.value !== '多色' && 
    v.value !== '透明色' &&
    v.value !== '透明' &&
    v.value !== '混色'
  );
  
  console.log(`🎨 颜色字典：${colorDictValues.values.length} 种，可用：${availableColors.length} 种（排除多色/透明色）`);
  
  // 随机选择 3 个颜色
  const shuffled = availableColors.sort(() => Math.random() - 0.5);
  const selectedColors = shuffled.slice(0, 3);
  
  console.log(`✅ 随机选择 3 个颜色：${selectedColors.map(c => `${c.value}(ID:${c.id})`).join(', ')}`);
  
  // 返回 value_id 数组格式
  return { 
    values: selectedColors.map(c => ({ value_id: c.id, value: c.value }))
  };
}

/**
 * 从常见 3 色随机选择
 */
function getRandomCommonColor() {
  const commonColors = colorsDict.common_colors.colors;
  const randomIndex = Math.floor(Math.random() * commonColors.length);
  return commonColors[randomIndex].ru;
}

/**
 * 材质智能转换（返回俄文）
 * 规则：
 * 1. 有明确材质 → 翻译为俄文
 * 2. 未知材质 → 使用默认值（塑料）
 */
function smartMaterial(material) {
  loadDictionaries();
  
  if (!material || material === '无' || material === 'null') {
    return materialsDict.default;
  }
  
  // 检查是否在字典中
  const translated = materialsDict.materials[material];
  if (translated) {
    return translated;
  }
  
  // 未知材质，返回默认
  console.warn(`⚠️ 未知材质 "${material}"，使用默认值`);
  return materialsDict.default;
}

/**
 * 材质智能匹配（返回字典值 ID）⭐ 新版
 * 规则：
 * 1. 精确匹配中文值 → 返回 ID
 * 2. 模糊匹配 → 返回最接近的 ID
 * 3. 无匹配 → 返回默认值 ID（塑料）
 */
function smartMaterialMatch(material) {
  loadDictionaries();
  
  if (!materialDictValues || !materialDictValues.values) {
    // 字典不存在，返回俄文
    return { value: smartMaterial(material) };
  }
  
  if (!material || material === '无' || material === 'null') {
    // 默认塑料
    const defaultMaterial = materialDictValues.values.find(v => v.value === '塑料' || v.value === 'ABS 塑料');
    return defaultMaterial ? { value_id: defaultMaterial.id, value: defaultMaterial.value } : { value: 'Пластик' };
  }
  
  // 精确匹配
  let matched = materialDictValues.values.find(v => v.value === material);
  if (matched) {
    console.log(`✅ 材质匹配：${material} → ID:${matched.id} (${matched.value})`);
    return { value_id: matched.id, value: matched.value };
  }
  
  // 优先匹配：单字"木" → "天然木材"
  if (material === '木') {
    const woodMaterial = materialDictValues.values.find(v => v.value === '天然木材');
    if (woodMaterial) {
      console.log(`✅ 材质特殊匹配：${material} → ID:${woodMaterial.id} (${woodMaterial.value})`);
      return { value_id: woodMaterial.id, value: woodMaterial.value };
    }
  }
  
  // 模糊匹配（包含匹配）- 优先找最相关的
  const fuzzyMatches = materialDictValues.values.filter(v => v.value.includes(material) && material.length > 0);
  if (fuzzyMatches.length > 0) {
    // 优先选择包含完整词的（如"木" → "天然木材" 而不是 "木质纤维板"）
    matched = fuzzyMatches.find(v => v.value.length - material.length <= 2) || fuzzyMatches[0];
    console.log(`✅ 材质模糊匹配：${material} → ID:${matched.id} (${matched.value})`);
    return { value_id: matched.id, value: matched.value };
  }
  
  // 关键词匹配（塑料类）
  if (material.includes('塑料') || material.includes('塑胶')) {
    const plasticMaterial = materialDictValues.values.find(v => v.value === '塑料' || v.value.includes('塑料'));
    if (plasticMaterial) {
      console.log(`✅ 塑料类匹配：${material} → ID:${plasticMaterial.id} (${plasticMaterial.value})`);
      return { value_id: plasticMaterial.id, value: plasticMaterial.value };
    }
  }
  
  // 无匹配，返回默认
  console.warn(`⚠️ 材质无匹配 "${material}"，使用默认值`);
  const defaultMaterial = materialDictValues.values.find(v => v.value === '塑料' || v.value === 'ABS 塑料');
  return defaultMaterial ? { value_id: defaultMaterial.id, value: defaultMaterial.value } : { value: 'Пластик' };
}

/**
 * 年龄智能转换
 * 规则：
 * 1. 有明确年龄 → 映射为俄文年龄段
 * 2. 未知年龄 → 使用默认值（3-10 岁）
 */
function smartAge(age) {
  loadDictionaries();
  
  if (!age || age === '无' || age === 'null') {
    return ageRangesDict.default;
  }
  
  // 精确匹配
  const translated = ageRangesDict.age_ranges[age];
  if (translated) {
    return translated;
  }
  
  // 尝试智能匹配（提取数字）
  const smartMatch = smartAgeMatch(age);
  if (smartMatch) {
    return smartMatch;
  }
  
  // 未知年龄，返回默认
  console.warn(`⚠️ 未知年龄 "${age}"，使用默认值`);
  return ageRangesDict.default;
}

/**
 * 年龄智能匹配（正则）- 旧版返回俄文
 */
function smartAgeMatch(age) {
  // 提取数字
  const numbers = age.match(/\d+/g);
  if (!numbers || numbers.length === 0) {
    return null;
  }
  
  const minAge = parseInt(numbers[0]);
  const maxAge = numbers.length > 1 ? parseInt(numbers[1]) : minAge;
  
  // 年龄段匹配
  if (maxAge <= 2) return '0-2 года';
  if (maxAge <= 5) return '3-5 лет';
  if (maxAge <= 8) return '6-8 лет';
  if (maxAge <= 12) return '9-12 лет';
  if (maxAge <= 15) return '13-15 лет';
  if (maxAge <= 18) return '16-18 лет';
  
  return 'Взрослый';
}

/**
 * 年龄智能匹配（返回字典值 ID）⭐ 新版
 */
function smartAgeMatchWithId(age) {
  loadDictionaries();
  
  if (!ageDictValues || !ageDictValues.values) {
    // 字典不存在，返回俄文
    return { value: smartAge(age) };
  }
  
  if (!age || age === '无' || age === 'null') {
    // 默认 3 岁以上
    const defaultAge = ageDictValues.values.find(v => v.value === '3 岁以上');
    return defaultAge ? { value_id: defaultAge.id, value: defaultAge.value } : { value: '3-5 лет' };
  }
  
  // 解析年龄（提取数字）
  const ageMatch = age.match(/(\d+)/);
  if (!ageMatch) {
    const defaultAge = ageDictValues.values.find(v => v.value === '3 岁以上');
    return defaultAge ? { value_id: defaultAge.id, value: defaultAge.value } : { value: '3-5 лет' };
  }
  
  const ageNum = parseInt(ageMatch[1]);
  
  // 精确匹配
  let matched = ageDictValues.values.find(v => v.value === `${ageNum}岁以上` || v.value === `${ageNum} 个月以上`);
  if (matched) {
    console.log(`✅ 年龄匹配：${age} → ID:${matched.id} (${matched.value})`);
    return { value_id: matched.id, value: matched.value };
  }
  
  // 模糊匹配（年龄段）
  if (ageNum <= 1) {
    matched = ageDictValues.values.find(v => v.value.includes('1 岁') || v.value.includes('12 个月'));
  } else if (ageNum <= 3) {
    matched = ageDictValues.values.find(v => v.value.includes('3 岁'));
  } else if (ageNum <= 5) {
    matched = ageDictValues.values.find(v => v.value.includes('5 岁'));
  } else if (ageNum <= 10) {
    matched = ageDictValues.values.find(v => v.value.includes('10 岁'));
  } else {
    matched = ageDictValues.values.find(v => v.value.includes('14 岁') || v.value.includes('18 岁'));
  }
  
  if (matched) {
    console.log(`✅ 年龄模糊匹配：${age} → ID:${matched.id} (${matched.value})`);
    return { value_id: matched.id, value: matched.value };
  }
  
  // 无匹配，返回默认
  console.warn(`⚠️ 年龄无匹配 "${age}"，使用默认值`);
  const defaultAge = ageDictValues.values.find(v => v.value === '3 岁以上');
  return defaultAge ? { value_id: defaultAge.id, value: defaultAge.value } : { value: '3-5 лет' };
}

/**
 * 品牌转换
 * 规则：固定使用"Другое"
 */
function smartBrand(brand) {
  return 'Другое';
}

/**
 * 国家智能匹配（返回字典值 ID）⭐ 新版
 */
function smartCountryMatch(country) {
  loadDictionaries();
  
  // 加载国家字典
  const countryDictFile = path.join(__dirname, '../attributes/country_dict.json');
  let countryDictValues = null;
  
  if (fs.existsSync(countryDictFile)) {
    countryDictValues = JSON.parse(fs.readFileSync(countryDictFile, 'utf-8'));
  }
  
  if (!countryDictValues || !countryDictValues.values) {
    // 字典不存在，返回俄文
    return { value: country === '中国' ? 'Китай' : country };
  }
  
  if (!country) {
    // 默认中国
    const defaultCountry = countryDictValues.values.find(v => v.value === '中国');
    return defaultCountry ? { value_id: defaultCountry.id, value: defaultCountry.value } : { value: 'Китай' };
  }
  
  // 精确匹配
  let matched = countryDictValues.values.find(v => v.value === country);
  if (matched) {
    console.log(`✅ 国家匹配：${country} → ID:${matched.id} (${matched.value})`);
    return { value_id: matched.id, value: matched.value };
  }
  
  // 无匹配，返回默认
  console.warn(`⚠️ 国家无匹配 "${country}"，使用默认值`);
  const defaultCountry = countryDictValues.values.find(v => v.value === '中国');
  return defaultCountry ? { value_id: defaultCountry.id, value: defaultCountry.value } : { value: 'Китай' };
}

/**
 * 性别智能转换
 * 规则：固定使用"Унисекс"
 */
function smartGender(gender) {
  return 'Унисекс';
}

/**
 * 生成唯一型号
 * 格式：oc#YYYY_MM_DD-hh_mm_ss
 */
function generateModelName(prefix = 'oc') {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  
  return `${prefix}#${year}_${month}_${day}-${hours}_${minutes}_${seconds}`;
}

/**
 * 通用翻译函数（如果字典中没有）
 */
async function translateUnknown(text, from = 'zh', to = 'ru') {
  // 这里可以集成翻译 API
  // 目前返回原文
  return text;
}

/**
 * 从文案中提取标题（纯俄文）
 * 只提取标题栏的俄文部分（**俄文描述:** 下面的第一行）
 */
function extractTitle(copyWriting) {
  if (!copyWriting) return '';
  
  const lines = copyWriting.split('\n');
  
  // 查找 "## 标题" 或 "### 标题" 下面的内容，然后提取俄文部分
  for (let i = 0; i < lines.length - 1; i++) {
    const line = lines[i].trim();
    if (line === '## 标题' || line.startsWith('## 标题') || 
        line === '### 标题' || line.startsWith('### 标题')) {
      // 找到下一行非空文本（格式：中文 / Развивающая игрушка-конструктор）
      for (let j = i + 1; j < lines.length; j++) {
        const nextLine = lines[j].trim();
        if (nextLine && !nextLine.startsWith('#')) {
          // 只提取俄文部分（斜杠后面的内容）
          const parts = nextLine.split('/');
          if (parts.length >= 2) {
            return parts[1].trim().substring(0, 250);
          }
          return nextLine.substring(0, 250);
        }
      }
    }
  }
  
  // 如果没有找到"## 标题"，回退到第一行非空文本
  const nonEmptyLines = lines.filter(line => line.trim());
  if (nonEmptyLines.length === 0) return '';
  
  let title = nonEmptyLines[0].trim();
  title = title.replace(/^#+\s*/, ''); // 去除 Markdown 标题标记
  title = title.replace(/^[\d+\.\s]+/, ''); // 去除序号
  
  return title.substring(0, 250); // OZON 限制 250 字符
}

/**
 * 从文案中提取俄文描述
 * 只提取 "**俄文描述**:" 下面的内容，到 "## 话题标签" 或 "**中文描述**:" 前停止
 */
function extractDescription(copyWriting) {
  if (!copyWriting) return '';
  
  const lines = copyWriting.split('\n');
  const descriptionLines = [];
  
  let inRussianDesc = false;
  let inTags = false;
  let simpleFormat = false; // 简单格式标记（## 描述）
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检测是否进入标签部分
    if (trimmed.includes('话题标签') || trimmed.includes('話題標籤') || trimmed.includes('Hashtag')) {
      inTags = true;
      inRussianDesc = false;
      simpleFormat = false;
      continue;
    }
    
    // 检测是否进入中文描述部分（停止提取俄文描述）
    if (trimmed.includes('**中文描述**')) {
      break;
    }
    
    // 检测是否进入俄文描述部分（支持带括号的格式）
    if (trimmed.includes('**俄文描述**')) {
      inRussianDesc = true;
      continue;
    }
    
    // 检测简单格式：## 描述
    if (trimmed === '## 描述' || trimmed.startsWith('## 描述')) {
      simpleFormat = true;
      inRussianDesc = true;
      continue;
    }
    
    if (inTags) {
      continue; // 跳过标签部分
    }
    
    if (!inRussianDesc && !simpleFormat) {
      continue; // 跳过俄文描述之前的内容
    }
    
    // 跳过空行
    if (!trimmed) continue;
    
    // 跳过标题行（# 开头）
    if (trimmed.startsWith('#')) continue;
    
    descriptionLines.push(trimmed);
  }
  
  const description = descriptionLines.join('\n');
  return description.substring(0, 10000); // OZON 限制 10000 字符
}

/**
 * 从文案中提取俄文 hashtags（#开头的标签）
 * OZON 后台所有文本内容只支持俄文
 */
function extractHashtags(copyWriting) {
  if (!copyWriting) return [];
  
  const lines = copyWriting.split('\n');
  let inRussianTags = false;
  let simpleFormat = false; // 简单格式标记（## 话题标签）
  const allHashtags = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检测简单格式：## 话题标签（优先级最高）
    if (trimmed === '## 话题标签' || trimmed.startsWith('## 话题标签')) {
      simpleFormat = true;
      inRussianTags = true;
      continue;
    }
    
    // 检测是否进入话题标签部分（通用匹配）
    if (trimmed.includes('话题标签') || trimmed.includes('話題標籤') || trimmed.includes('Hashtag')) {
      inRussianTags = false;
      simpleFormat = false;
      // 检查是否同一行有标签（简单格式）
      const hashtagRegex = /#[a-zA-Zа-яА-ЯёЁ0-9_]+/g;
      const matches = [...trimmed.matchAll(hashtagRegex)];
      if (matches.length > 0) {
        for (const match of matches) {
          allHashtags.push(match[0]);
        }
      }
      continue;
    }
    
    // 检测是否进入俄文标签部分（支持带括号的格式）
    if (trimmed.includes('**俄文标签**')) {
      inRussianTags = true;
      continue;
    }
    
    // 检测是否进入中文标签部分（停止提取）
    if (trimmed.includes('**中文标签**')) {
      inRussianTags = false;
      simpleFormat = false;
      continue;
    }
    
    if (!inRussianTags && !simpleFormat) continue;
    
    // 提取所有 # 开头的俄文标签（支持西里尔字母、英文、数字、下划线、连字符）
    const hashtagRegex = /#[a-zA-Zа-яА-ЯёЁ0-9_-]+/g;
    const matches = [...trimmed.matchAll(hashtagRegex)];
    for (const match of matches) {
      allHashtags.push(match[0]);
    }
  }
  
  // 去重，限制最多 10 个
  const unique = [...new Set(allHashtags)];
  return unique.slice(0, 10);
}

/**
 * 从文案中提取简短描述（简介/annotation）
 * 只提取描述部分的俄文内容，用于商品短描述
 */
function extractAnnotation(copyWriting) {
  if (!copyWriting) return '';
  
  const lines = copyWriting.split('\n');
  let inRussianDescription = false;
  const descriptionLines = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检测是否进入俄文描述部分（支持带括号的格式）
    if (trimmed.includes('**俄文描述**')) {
      inRussianDescription = true;
      continue;
    }
    
    // 检测是否进入中文描述（停止提取）
    if (trimmed.includes('**中文描述**')) {
      inRussianDescription = false;
      break;
    }
    
    if (!inRussianDescription) continue;
    
    // 跳过空行
    if (!trimmed) continue;
    
    // 提取俄文句子（以俄文字母开头）
    if (/^[А-ЯЁа-яё]/.test(trimmed)) {
      descriptionLines.push(trimmed);
    }
  }
  
  // 返回完整俄文描述（已经只有 2-3 句话）
  return descriptionLines.join(' ');
}

// 导出函数
module.exports = {
  // 旧版：返回俄文字符串
  smartColor,
  smartMaterial,
  smartAge,
  smartGender,
  smartBrand,
  generateModelName,
  getRandomCommonColor, // 用于测试
  smartAgeMatch, // 用于测试
  
  // 新版：返回字典值 ID ⭐
  smartColorMatch,
  smartMaterialMatch,
  smartAgeMatchWithId,
  smartCountryMatch,
  
  // 文案提取
  extractTitle, // v2.0 新增 - 只提取俄文标题
  extractDescription, // v2.0 新增 - 只提取俄文描述
  extractHashtags, // v2.0 新增 - 只提取俄文标签
  extractAnnotation // v3.0 新增 - 提取简短描述（简介）
};
