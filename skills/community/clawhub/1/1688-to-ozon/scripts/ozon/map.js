#!/usr/bin/env node
/**
 * 通用映射引擎 v2.0 (v1.0.51+ 新架构)
 * 根据类目映射规则，将 1688 数据转换为 OZON 完整商品格式
 * 
 * 数据读取规则（v1.0.51+）：
 * - 从 1688-to-ozon/ 主目录读取各步骤输出
 * - 1688-tt/：Step 1 商品抓取
 * - ozon-image-translator/：Step 2 图片翻译
 * - ozon-pricer/：Step 3 价格计算
 * 
 * 输出：
 * - mapping_result.json：映射结果
 * - upload-request.json：OZON 上传请求
 * 
 * v2.0 更新：
 * - ✅ 构建完整 ozon_product（name, description, price, images, hashtags 等）
 * - ✅ 支持 attributes + 核心字段
 * - ✅ 自动生成 offer_id
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {
  smartColor,
  smartMaterial,
  smartAge,
  smartGender,
  smartBrand,
  generateModelName,
  smartColorMatch,
  smartMaterialMatch,
  smartAgeMatchWithId,
  smartCountryMatch,
  extractTitle,
  extractDescription,
  extractHashtags,
  extractAnnotation
} = require('./transform');
const attributeValues = require('./attribute-values');

const MAPPINGS_DIR = path.join(__dirname, '../mappings');
// 动态获取当前 workspace（支持多 agent）
const ROOT_DIR = path.join(__dirname, '../../..'); // ~/.openclaw/
const WORKSPACE_DIR = process.env.WORKSPACE_DIR || process.cwd(); // 支持 WORKSPACE_DIR 环境变量
// 1688-to-ozon 主目录（各步骤输出在此目录下）
const MAIN_DIR = path.join(WORKSPACE_DIR, '1688-to-ozon');

// 各步骤输出目录
const DIR_1688 = path.join(MAIN_DIR, '1688-tt');
const DIR_TRANSLATOR = path.join(MAIN_DIR, 'ozon-image-translator');
const DIR_PRICER = path.join(MAIN_DIR, 'ozon-pricer');
const DIR_OUTPUT = MAIN_DIR; // mapping_result.json 直接输出到主目录

// 兼容旧路径（如果新路径不存在则使用）
const INPUT_DIR = path.join(WORKSPACE_DIR, 'ozon-publisher/input');
const INPUT_DIR_ALT = path.join(WORKSPACE_DIR, 'projects/ozon-publisher/input');

// 全局缓存：type_id -> 属性值映射表
let cachedAttributeValues = null;

/**
 * 加载类目映射规则
 */
function loadCategoryMapping(category) {
  const mappingFile = path.join(MAPPINGS_DIR, `${category}_mapping.json`);
  
  if (!fs.existsSync(mappingFile)) {
    throw new Error(`类目映射文件不存在：${mappingFile}`);
  }
  
  return JSON.parse(fs.readFileSync(mappingFile, 'utf-8'));
}

/**
 * 从 input 目录加载数据
 * 
 * 目录结构：
 * input/
 * ├── 1688-tt/
 * │   ├── product_info.md
 * │   ├── copy_writing.md
 * │   └── images/
 * ├── ozon-image-translator/
 * │   └── images/
 * └── ozon-pricer/
 *     └── result.json
 */
function loadInputData() {
  const data = {};
  
  // 确定输入目录（新架构：直接读取各步骤输出目录）
  let inputDir = MAIN_DIR;
  if (!fs.existsSync(MAIN_DIR)) {
    // 兼容旧架构：尝试使用旧路径
    if (fs.existsSync(INPUT_DIR)) {
      inputDir = INPUT_DIR;
    } else if (fs.existsSync(INPUT_DIR_ALT)) {
      inputDir = INPUT_DIR_ALT;
    }
  }
  console.log('📂 使用输入目录:', inputDir);
  
  // 1. 加载 1688-tt 数据
  const tt1688Dir = fs.existsSync(DIR_1688) ? DIR_1688 : path.join(inputDir, '1688-tt');
  if (fs.existsSync(tt1688Dir)) {
    data['1688-tt'] = {};
    
    // 读取 product_info.md
    const productInfoFile = path.join(tt1688Dir, 'product_info.md');
    if (fs.existsSync(productInfoFile)) {
      data['1688-tt'].product_info = parseProductInfo(productInfoFile);
    }
    
    // 读取 copy_writing（只读 JSON，MD 是给用户看的）
    const copyWritingJson = path.join(tt1688Dir, 'copy_writing.json');

    if (fs.existsSync(copyWritingJson)) {
      const jsonData = JSON.parse(fs.readFileSync(copyWritingJson, 'utf-8'));
      data['1688-tt'].copy_writing_json = jsonData;
      console.log('   ✅ 从 copy_writing.json 读取结构化数据');
    } else {
      throw new Error(`copy_writing.json 不存在：${copyWritingJson}`);
    }
    
    // 读取图片列表
    const imagesDir = path.join(tt1688Dir, 'images');
    if (fs.existsSync(imagesDir)) {
      data['1688-tt'].images = fs.readdirSync(imagesDir)
        .filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
    }
  }
  
  // 2. 加载 ozon-pricer 数据（必须有）
  const pricerDir = fs.existsSync(DIR_PRICER) ? DIR_PRICER : path.join(inputDir, 'ozon-pricer');
  if (!fs.existsSync(pricerDir)) {
    throw new Error('❌ ozon-pricer 目录不存在，请先运行ozon-pricer获取价格数据');
  }
  
  // 优先读取 result.json，如果没有则解析 pricing.md
  const resultFile = path.join(pricerDir, 'result.json');
  const pricingFile = path.join(pricerDir, 'pricing.md');
  
  if (fs.existsSync(resultFile)) {
    data['ozon-pricer'] = JSON.parse(fs.readFileSync(resultFile, 'utf-8'));
    console.log('   ✅ 从 result.json 读取价格数据');
  } else if (fs.existsSync(pricingFile)) {
    // 解析 pricing.md - 读取人民币价格
    const pricingContent = fs.readFileSync(pricingFile, 'utf-8');
    
    // 匹配价格（支持两种格式）
    // 格式1: 折后售价：¥127.24 (划线价 ¥254.48，50折)
    // 格式2: 折后售价：¥127.24 (划线价 ¥254.48，折前价 ¥254.48)
    const priceLineMatch = pricingContent.match(/折后售价：¥([\d.]+) [(]划线价 ¥([\d.]+)/);
    
    if (priceLineMatch) {
      const discountedPrice = parseFloat(priceLineMatch[1]);
      const beforeDiscountPrice = parseFloat(priceLineMatch[2]);
      
      data['ozon-pricer'] = {
        price_cny: discountedPrice, // 折后售价（上传售价）
        old_price_cny: beforeDiscountPrice // 划线价
      };
      console.log(`✅ 从 pricing.md 解析价格：折前¥${beforeDiscountPrice.toFixed(2)} CNY（折后¥${discountedPrice}）`);
    } else {
      throw new Error('❌ 无法从 pricing.md 解析价格数据');
    }
  } else {
    throw new Error(`❌ ozon-pricer/result.json 和 ozon-pricer/pricing.md 都不存在`);
  }
  
  // 3. 加载 ozon-image-translator 数据
  const translatorDir = fs.existsSync(DIR_TRANSLATOR) ? DIR_TRANSLATOR : path.join(inputDir, 'ozon-image-translator');
  if (fs.existsSync(translatorDir)) {
    data['ozon-image-translator'] = {};
    
    // 读取 images.json（包含 URL）
    const imagesJsonFile = path.join(translatorDir, 'images.json');
    if (fs.existsSync(imagesJsonFile)) {
      data['ozon-image-translator'].images_json = JSON.parse(fs.readFileSync(imagesJsonFile, 'utf-8'));
    }
    
    // 读取图片文件名列表
    const imagesDir = path.join(translatorDir, 'images');
    if (fs.existsSync(imagesDir)) {
      data['ozon-image-translator'].images = fs.readdirSync(imagesDir)
        .filter(f => f.endsWith('.jpg') || f.endsWith('.png'));
    }
  }
  
  return data;
}

/**
 * 解析 product_info.md
 * 
 * 文件格式：
 * ## 商品信息
 * - 品牌：其他
 * - 颜色：彩色
 * - 材质：塑胶
 * - 年龄：0-2 岁
 * - 性别：男女孩
 * - 包装尺寸：10x10x5 cm
 * 
 * ## 附加信息（用户提供）
 * - **商品重量**: 200g
 * - **采购价格**: ¥10 元
 */
function parseProductInfo(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const result = {};
  
  const lines = content.split('\n');
  for (const line of lines) {
    // 尝试匹配 Markdown 表格格式：| **属性** | 值 |
    const tableMatch = line.match(/^\|\s*\*?\*?(.+?)\*?\*?\s*\|\s*(.+?)\s*\|$/);
    // 尝试匹配列表格式：- **属性**: 值
    const listMatch = line.match(/^-?\s*\*?\*?(.+?)\*?\*?\s*[:：]\s*(.+?)\s*$/);
    
    const match = tableMatch || listMatch;
    if (match) {
      const key = match[1].trim().toLowerCase();
      const value = match[2].trim();
      
      // 映射到标准字段名
      if (key.includes('品牌')) result.brand = value;
      else if (key.includes('颜色')) result.color = value;
      else if (key.includes('材质')) result.material = value;
      else if (key.includes('年龄')) result.age = value;
      else if (key.includes('性别')) result.gender = value;
      else if (key.includes('包装尺寸')) {
        // 解析 10x10x5 cm
        const dims = value.match(/(\d+)x(\d+)x(\d+)/);
        if (dims) {
          result.package_length = parseInt(dims[1]);
          result.package_width = parseInt(dims[2]);
          result.package_height = parseInt(dims[3]);
        }
      }
      else if (key.includes('商品重量') || key.includes('重量')) {
        // 解析 200g 或 200
        const weightMatch = value.match(/(\d+)/);
        if (weightMatch) {
          result.weight = parseInt(weightMatch[1]);
        }
      }
      else if (key.includes('采购价格') || key.includes('价格')) {
        // 解析 ¥10 元 或 10
        const priceMatch = value.match(/(\d+)/);
        if (priceMatch) {
          result.purchase_price = parseInt(priceMatch[1]);
        }
      }
    }
  }
  
  return result;
}

/**
 * 生成 offer_id（基于时间戳 + 随机数）
 */
function generateOfferId() {
  const timestamp = Date.now();
  const random = crypto.randomBytes(4).toString('hex');
  return `ozon_${timestamp}_${random}`;
}

/**
 * 根据 source 路径获取数据
 * 
 * source 格式：
 * - 1688-tt.product_info.brand → 从 data['1688-tt'].product_info.brand 获取
 * - fixed → 固定值（使用 fallback）
 * - auto_generate → 自动生成（在 transform 中处理）
 */
function getSourceValue(source, data) {
  if (!source) return null;
  
  // 特殊处理：fixed 和 auto_generate
  if (source === 'fixed' || source === 'auto_generate') {
    return null; // 返回 null，让 fallback 或 transform 处理
  }
  
  // 解析 source 路径
  const parts = source.split('.');
  if (parts.length < 2) {
    console.warn(`⚠️ 无效的 source 路径：${source}`);
    return null;
  }
  
  // 第一部分：技能名（1688-tt, ozon-pricer, ozon-image-translator）
  const skillName = parts[0];
  
  // 后续部分：数据路径
  const fieldPath = parts.slice(1).join('.');
  
  // 从对应技能数据中获取
  const skillData = data[skillName];
  if (!skillData) {
    console.warn(`⚠️ 未找到技能数据：${skillName}`);
    return null;
  }
  
  return getNestedValue(skillData, fieldPath);
}

/**
 * 获取嵌套对象值
 */
function getNestedValue(obj, fieldPath) {
  if (!obj) return null;
  
  const fields = fieldPath.split('.');
  let value = obj;
  
  for (const field of fields) {
    if (value === null || value === undefined) return null;
    value = value[field];
  }
  
  return value;
}

/**
 * 应用转换规则
 */
function applyTransform(value, transform, field, data) {
  if (!transform) {
    return value;
  }
  
  // 型号生成
  if (transform === 'oc#YYYY_MM_DD-hh_mm_ss') {
    return generateModelName();
  }
  
  // 标题提取（只读取 JSON）
  if (transform === 'extract_title') {
    const copyWritingJson = data?.['1688-tt']?.copy_writing_json;
    
    if (copyWritingJson?.title?.ru) {
      return copyWritingJson.title.ru.substring(0, 250);
    }
    return '';
  }
  
  // 描述提取（转换为 HTML 格式）
  if (transform === 'extract_description') {
    const copyWritingJson = data?.['1688-tt']?.copy_writing_json;
    
    if (copyWritingJson?.description?.ru) {
      let text = copyWritingJson.description.ru.substring(0, 10000);
      // 转换为 HTML 格式
      text = text
        // 换行符转换为 <br>
        .replace(/\n/g, '<br>')
        // 加粗标题：**text** 或 ✨emoji → <strong>text</strong>
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/✨([^\n<]+)/g, '<strong>$1</strong>')
        .replace(/📏([^\n<]+)/g, '<strong>$1</strong>')
        .replace(/🎵([^\n<]+)/g, '<strong>$1</strong>')
        // 项目符号 • 转换为 <li>
        .replace(/<br>• /g, '<br><li>')
        .replace(/^• /g, '<li>');
      
      // 如果有 <li>，包裹在 <ul> 中
      if (text.includes('<li>')) {
        text = text.replace(/(<li>)/g, '<ul>$1').replace(/<\/li>(?!.*<li>)/, '</li></ul>');
      }
      
      return text;
    }
    return '';
  }
  
  // 标签提取（转换为逗号分隔的字符串）
  if (transform === 'extract_hashtags') {
    const copyWritingJson = data?.['1688-tt']?.copy_writing_json;
    
    if (copyWritingJson?.hashtags?.ru && Array.isArray(copyWritingJson.hashtags.ru)) {
      // OZON API 要求字符串格式，标签之间用空格分隔
      // LLM 生成时已使用下划线连接（如 #детские_игрушки）
      const tags = copyWritingJson.hashtags.ru.slice(0, 25); // OZON 限制最多 25 个
      return tags.join(' ');
    }
    return '';
  }
  
  // 简介提取（营销亮点，只读取 JSON）
  if (transform === 'extract_annotation') {
    const copyWritingJson = data?.['1688-tt']?.copy_writing_json;
    
    if (copyWritingJson?.annotation?.ru) {
      return copyWritingJson.annotation.ru;
    }
    // Fallback：如果 LLM 没生成 annotation，则用 description 前 200 字符
    if (copyWritingJson?.description?.ru) {
      return copyWritingJson.description.ru.substring(0, 200);
    }
    return '';
  }
  
  // 智能转换
  switch (transform) {
    case 'color_smart':
      return smartColor(value);
    
    case 'material_smart':
      return smartMaterial(value);
    
    case 'age_smart':
      return smartAge(value);
    
    case 'gender_smart':
      return smartGender(value);
    
    case 'brand_smart':
      return smartBrand(value);
    
    case 'price_multiply_1.2':
      // 划线价 = 售价 * 1.2
      const num = parseFloat(value);
      if (isNaN(num)) return value;
      return (num * 1.2).toFixed(2);
    
    default:
      console.warn(`⚠️ 未知转换规则：${transform}`);
      return value;
  }
}

/**
 * 构建 OZON attributes 格式（支持动态属性值查询）
 */
async function buildAttributesAsync(data, mapping) {
  const attributes = [];
  
  // 加载属性值缓存（type_id -> 属性值映射表）
  const typeId = mapping.type_id;
  const categoryId = mapping.description_category_id;
  const categoryName = mapping.category_name;  // 类目名称，如 "toy_set"
  
  // 获取所有需要查询的属性 ID
  const attributeIdsToQuery = [];
  for (const [key, field] of Object.entries(mapping.fields)) {
    if (field._disabled || !field.ozon_attribute_id || field.ozon_attribute_id === 0) continue;
    if (field.dictionary_id && field.dictionary_id > 0) {
      attributeIdsToQuery.push(field.ozon_attribute_id);
    }
  }
  
  // 批量查询属性值（优先缓存）
  if (attributeIdsToQuery.length > 0) {
    try {
      cachedAttributeValues = await attributeValues.getAllAttributeValues(
        typeId, categoryId, attributeIdsToQuery, false, categoryName
      );
    } catch (error) {
      console.warn(`⚠️  查询属性值失败：${error.message}，将使用静态字典`);
      cachedAttributeValues = {};
    }
  }
  
  for (const [key, field] of Object.entries(mapping.fields)) {
    // 跳过被禁用的字段
    if (field._disabled) {
      console.log(`⏭️ 跳过已禁用字段：${field.name_cn} (${key})`);
      continue;
    }
    
    // 跳过没有 ozon_attribute_id 的字段
    if (!field.ozon_attribute_id) {
      console.log(`⏭️ 跳过非属性字段：${field.name_cn} (${key})`);
      continue;
    }
    
    // 跳过 ozon_attribute_id 为 0 的字段
    if (field.ozon_attribute_id === 0) {
      continue;
    }
    
    // 获取源数据
    let value = getSourceValue(field.source, data);
    
    // 应用转换
    const finalValue = applyTransform(value, field.transform, field, data);
    
    // 对于有字典的智能匹配，使用原始值而不是转换后的值
    // 因为 smart*Match 函数期望接收原始中文值并返回 value_id
    const useValueForMatch = (field.dictionary_id && field.dictionary_id > 0 && 
      (field.transform === 'color_smart' || field.transform === 'material_smart' || 
       field.transform === 'age_smart' || field.transform === 'country_smart')) 
      ? (value || field.fallback) 
      : (finalValue || field.fallback);
    
    // 使用 fallback
    const useValue = finalValue || field.fallback;
    
    // 跳过空值属性（OZON API 要求：空值属性不要发送）
    if (!useValue || useValue === '' || (Array.isArray(useValue) && useValue.length === 0)) {
      if (field.name_cn === '简介') {
        console.log(`🔍 简介调试：finalValue="${finalValue ? finalValue.substring(0, 50) : 'null'}", fallback="${field.fallback}"`);
      }
      console.log(`⏭️ 跳过空值属性：${field.name_cn}`);
      continue;
    }
    
    // 检查是否有 dictionary_id（字典值属性）
    let valueObject;
    if (field.dictionary_id && field.dictionary_id > 0) {
      // 有字典，优先使用动态查询结果
      let matchResult;
      
      if (field.transform === 'color_smart') {
        // 颜色：从动态查询结果中随机选 3 个
        const colorValues = cachedAttributeValues?.[field.ozon_attribute_id] || [];
        if (colorValues.length > 0) {
          // 排除多色/透明色
          const excludeKeywords = ['多色', '透明', '混色'];
          const filtered = colorValues.filter(v => 
            !excludeKeywords.some(k => v.value.includes(k))
          );
          const selected = filtered.sort(() => Math.random() - 0.5).slice(0, 3);
          matchResult = { 
            values: selected.map(v => ({ value_id: v.id, value: v.value }))
          };
          console.log(`✅ ${field.name_cn}: ${selected.length} 个颜色 [${selected.map(v => `ID:${v.id}(${v.value})`).join(', ')}] [动态查询]`);
        } else {
          matchResult = smartColorMatch(useValueForMatch);
        }
      } else if (field.transform === 'material_smart') {
        // 材料：从动态查询结果中匹配
        const materialValues = cachedAttributeValues?.[field.ozon_attribute_id] || [];
        if (materialValues.length > 0) {
          // 尝试匹配"塑料"
          const matched = materialValues.find(v => v.value === 'Пластик' || v.value.includes('пластик'));
          if (matched) {
            matchResult = { value_id: matched.id, value: matched.value };
            console.log(`✅ ${field.name_cn}: ID:${matched.id} (${matched.value}) [动态查询]`);
          } else {
            matchResult = { value_id: materialValues[0].id, value: materialValues[0].value };
            console.log(`✅ ${field.name_cn}: ID:${materialValues[0].id} (${materialValues[0].value}) [默认]`);
          }
        } else {
          matchResult = smartMaterialMatch(useValueForMatch);
        }
      } else if (field.transform === 'age_smart') {
        // 年龄：从动态查询结果中匹配
        const ageValues = cachedAttributeValues?.[field.ozon_attribute_id] || [];
        if (ageValues.length > 0) {
          // 尝试匹配"3 岁以上"
          const matched = ageValues.find(v => v.value.includes('3 岁') || v.value.includes('3 года'));
          if (matched) {
            matchResult = { value_id: matched.id, value: matched.value };
            console.log(`✅ ${field.name_cn}: ID:${matched.id} (${matched.value}) [动态查询]`);
          } else {
            matchResult = { value_id: ageValues[0].id, value: ageValues[0].value };
            console.log(`✅ ${field.name_cn}: ID:${ageValues[0].id} (${ageValues[0].value}) [默认]`);
          }
        } else {
          matchResult = smartAgeMatchWithId(useValueForMatch);
        }
      } else if (field.transform === 'country_smart') {
        matchResult = smartCountryMatch(useValueForMatch);
      } else if (field.source === 'fixed' && field.fallback) {
        // fixed 类型，使用 fallback 值匹配字典
        if (field.ozon_attribute_id === 4389) {
          // 原产国：从动态查询结果中匹配
          const countryValues = cachedAttributeValues?.[4389] || [];
          if (countryValues.length > 0) {
            const matched = countryValues.find(v => v.value === 'Китай' || v.value === '中国');
            if (matched) {
              matchResult = { value_id: matched.id, value: matched.value };
              console.log(`✅ ${field.name_cn}: ID:${matched.id} (${matched.value}) [动态查询]`);
            } else {
              matchResult = { value_id: 90296, value: 'Китай' }; // 默认中国
              console.log(`✅ ${field.name_cn}: ID:90296 (Китай) [默认值]`);
            }
          } else {
            matchResult = smartCountryMatch(field.fallback);
          }
        } else if (field.ozon_attribute_id === 13216) {
          // 儿童性别：从动态查询结果中匹配
          const genderValues = cachedAttributeValues?.[13216] || [];
          if (genderValues.length > 0) {
            const matched = genderValues.find(v => v.value === 'Унисекс');
            if (matched) {
              matchResult = { value_id: matched.id, value: matched.value };
              console.log(`✅ ${field.name_cn}: ID:${matched.id} (${matched.value}) [动态查询]`);
            } else {
              matchResult = { value_id: genderValues[0].id, value: genderValues[0].value };
              console.log(`✅ ${field.name_cn}: ID:${genderValues[0].id} (${genderValues[0].value}) [默认]`);
            }
          } else {
            matchResult = { value: field.fallback };
          }
        } else if (field.ozon_attribute_id === 8229) {
          // 类型：从动态查询结果中匹配
          const typeValues = cachedAttributeValues?.[8229] || [];
          if (typeValues.length > 0) {
            const matched = typeValues.find(v => v.value === 'Набор игрушек');
            if (matched) {
              matchResult = { value_id: matched.id, value: matched.value };
              console.log(`✅ ${field.name_cn}: ID:${matched.id} (${matched.value}) [动态查询]`);
            } else {
              matchResult = { value_id: typeValues[0].id, value: typeValues[0].value };
              console.log(`✅ ${field.name_cn}: ID:${typeValues[0].id} (${typeValues[0].value}) [默认]`);
            }
          } else {
            matchResult = { value: field.fallback };
          }
        } else {
          // 其他 fixed 类型：使用 value_id（如果配置了）
          if (field.value_id) {
            matchResult = { value_id: field.value_id, value: field.fallback };
            console.log(`✅ ${field.name_cn}: ID:${field.value_id} (${field.fallback}) [配置值]`);
          } else {
            matchResult = { value: field.fallback };
          }
        }
      } else {
        // 其他属性，直接使用值
        matchResult = { value: useValue };
      }
      
      // 处理返回值
      if (field.transform === 'rich_content_json' && Array.isArray(useValue)) {
        // 富文本：从 images_json 对象数组中提取详情图 URL，转换为 JSON 字符串
        const detailImageUrls = useValue
          .filter(img => img.isDetail === true || img.isDetail === 'true' || (img.filename && img.filename.startsWith('detail_')))
          .map(img => img.url);
        
        const richContent = {
          content: [
            {
              widgetName: 'raShowcase',
              type: 'roll',
              blocks: detailImageUrls.map(url => ({
                imgLink: '',
                img: {
                  src: url,
                  srcMobile: url,
                  alt: '',
                  position: 'width_full',
                  positionMobile: 'width_full',
                  widthMobile: 800,
                  heightMobile: 800
                }
              }))
            }
          ],
          version: 0.3
        };
        valueObject = { value: JSON.stringify(richContent) };
        console.log(`✅ ${field.name_cn}: JSON 字符串 (${detailImageUrls.length} 张详情图)`);
      } else if (field.transform === 'color_smart' && matchResult.values && Array.isArray(matchResult.values)) {
        // 颜色：返回 3 个随机颜色（OZON API 要求：dictionary_value_id + value）
        valueObject = matchResult.values.map(v => ({ dictionary_value_id: v.value_id, value: v.value }));
        console.log(`✅ ${field.name_cn}: ${matchResult.values.length} 个颜色 [${matchResult.values.map(v => `ID:${v.value_id}`).join(', ')}]`);
      } else if (matchResult.value_id) {
        // 字典类型属性：使用 dictionary_value_id + value（OZON API 标准格式）
        valueObject = { dictionary_value_id: matchResult.value_id, value: matchResult.value };
        console.log(`✅ ${field.name_cn}: ID:${matchResult.value_id} (${matchResult.value})`);
      } else {
        // 没有 value_id，尝试使用预设的默认字典 ID
        let defaultId = null;
        let defaultValue = matchResult.value;
        
        // 原产国：中国 (90296)
        if (field.ozon_attribute_id === 4389) {
          defaultId = 90296;
          defaultValue = 'Китай';
          console.log(`✅ ${field.name_cn}: ID:${defaultId} (${defaultValue}) [默认]`);
          valueObject = { dictionary_value_id: defaultId, value: defaultValue };
        } else {
          valueObject = { value: defaultValue };
          console.log(`⚠️  ${field.name_cn}: ${defaultValue} (无字典 ID)`);
        }
      }
    } else {
      // 无字典，直接使用值
      // 特殊处理 1: hashtags 数组需要转换为字符串（用空格连接）
      // 特殊处理 2: 数值类型（decimal/number）需要转换为字符串
      // 特殊处理 3: rich_content_json 转换为 JSON 字符串
      let finalUseValue = useValue;
      
      if (field.transform === 'rich_content_json' && Array.isArray(useValue)) {
        // 富文本：从 images_json 对象数组中提取详情图 URL，转换为 JSON 字符串
        // 支持两种模式：
        // 1. attribute_id: 11254 - 作为 attributes 数组中的属性（推荐）
        // 2. 顶层字段 - 旧模式（兼容）
        const detailImageUrls = useValue
          .filter(img => img.isDetail === true || img.isDetail === 'true' || (img.filename && img.filename.startsWith('detail_')))
          .map(img => img.url);
        
        const richContent = {
          content: [
            {
              widgetName: 'raShowcase',
              type: 'roll',
              blocks: detailImageUrls.map(url => ({
                imgLink: '',
                img: {
                  src: url,
                  srcMobile: url,
                  alt: '',
                  position: 'width_full',
                  positionMobile: 'width_full',
                  widthMobile: 800,
                  heightMobile: 800
                }
              }))
            }
          ],
          version: 0.3
        };
        finalUseValue = JSON.stringify(richContent);
        
        // 如果是 attribute_id 11254，直接作为 attribute 的 value
        if (field.ozon_attribute_id === 11254) {
          console.log(`✅ ${field.name_cn} (ID:11254): JSON 字符串 (${detailImageUrls.length} 张详情图)`);
        } else {
          console.log(`✅ ${field.name_cn}: JSON 字符串 (${detailImageUrls.length} 张详情图)`);
        }
      } else if (field.ozon_attribute_id === 23171 && Array.isArray(useValue)) {
        finalUseValue = useValue.join(' ');
        console.log(`✅ ${field.name_cn}: ${finalUseValue.substring(0, 50)}... (数组转字符串)`);
      } else if (field.type === 'decimal' || field.type === 'number') {
        // 数值类型转字符串（OZON API 要求所有 value 都是字符串）
        finalUseValue = String(useValue);
        console.log(`✅ ${field.name_cn}: ${finalUseValue} (数值转字符串)`);
      } else {
        console.log(`✅ ${field.name_cn}: ${useValue}`);
      }
      
      valueObject = { value: finalUseValue };
    }
    
    // 添加到 attributes
    // 颜色属性 valueObject 已经是数组，不需要再包一层
    // OZON API 要求：添加 complex_id: 0
    attributes.push({
      complex_id: 0,
      id: field.ozon_attribute_id,
      values: Array.isArray(valueObject) ? valueObject : [valueObject]
    });
  }
  
  return attributes;
}

/**
 * 构建完整商品数据 v3.0（异步版本，支持动态属性值查询）
 */
async function buildProductAsync(data, mapping) {
  console.log('\n🔧 构建完整商品数据（异步）...\n');
  
  // 提取 copy_writing_json（避免重复访问）
  const copyWritingJson = data['1688-tt']?.copy_writing_json;
  
  // 1. 核心字段
  const productData = {};
  
  // 1.1 title → name（从 JSON 读取）
  const titleField = mapping.fields.title;
  if (titleField && copyWritingJson?.title?.ru) {
    productData.name = copyWritingJson.title.ru.substring(0, 250);
    console.log(`✅ 商品标题：${productData.name.substring(0, 50)}...`);
  }
  
  // 1.2 description（从 JSON 读取）
  const descField = mapping.fields.description;
  if (descField && copyWritingJson?.description?.ru) {
    productData.description = copyWritingJson.description.ru.substring(0, 10000);
    console.log(`✅ 商品描述：${productData.description.substring(0, 50)}...`);
  }
  
  // 1.3 price (OZON API 要求字符串类型，单位 CNY)
  const priceField = mapping.fields.price;
  const pricerData = data['ozon-pricer'];
  const finalPrice = pricerData?.finalPriceCNY || pricerData?.price_cny;
  if (priceField && finalPrice) {
    productData.price = String(finalPrice);
    console.log(`✅ 售价：¥${productData.price} CNY`);
  }
  
  // 1.4 old_price (OZON API 要求字符串类型，单位 CNY)
  const oldPriceField = mapping.fields.old_price;
  const oldPrice = pricerData?.oldPriceCNY || pricerData?.old_price_cny || pricerData?.beforeDiscountPriceCNY;
  if (oldPriceField && oldPrice) {
    productData.old_price = String(oldPrice);
    console.log(`✅ 划线价：¥${productData.old_price} CNY`);
  }
  
  // 1.5 hashtags（从 JSON 读取）
  const hashtagField = mapping.fields.hashtags;
  // copyWritingJson 已在函数开头声明（第 682 行），此处直接使用
  if (hashtagField && copyWritingJson?.hashtags?.ru) {
    productData.hashtags = copyWritingJson.hashtags.ru.slice(0, 25);
    console.log(`✅ 标签：${productData.hashtags.length} 个`);
  }
  
  // 1.6 images（从 ozon-image-translator 获取）
  const imagesField = mapping.fields.images;
  if (imagesField && data['ozon-image-translator']?.images) {
    // 分离主图和详情图
    const allImages = data['ozon-image-translator'].images;
    const mainImages = allImages.filter(f => f.startsWith('main_') || f.startsWith('main-'));
    const detailImages = allImages.filter(f => f.startsWith('detail_') || f.startsWith('detail-'));
    
    // 注意：这里只保存文件名，upload.js 会负责上传到图床获取 URL
    productData._imageFiles = {
      main: mainImages,
      detail: detailImages
    };
    console.log(`✅ 图片：${mainImages.length} 张主图，${detailImages.length} 张详情图`);
  }
  
  // 1.6.1 images（顶层字段，upload.js 会替换为 URL）
  productData.images = [];
  console.log(`✅ 产品图片：待上传（upload.js 填充 URL）`);
  
  // 1.6.2 rich_content（顶层字段，详情图，upload.js 会填充）
  productData.rich_content = null;
  console.log(`✅ 富文本详情：待生成（upload.js 填充）`);
  
  // 1.7 description_category_id 和 type_id
  productData.description_category_id = mapping.description_category_id;
  productData.type_id = mapping.type_id;
  console.log(`✅ 分类 ID：${mapping.description_category_id}`);
  console.log(`✅ 类型 ID：${mapping.type_id}`);
  
  // 1.8 offer_id（自动生成）
  productData.offer_id = generateOfferId();
  console.log(`✅ Offer ID: ${productData.offer_id}`);
  
  // 2. attributes（品牌、颜色、材质等）
  console.log('\n📋 构建属性列表...');
  // 注意：buildAttributesAsync 是异步函数，需要在 buildProductAsync 中调用
  // 这里先留空，由 buildProductAsync 填充
  productData.attributes = [];
  
  // 3. 包装信息
  console.log('\n📦 构建包装信息...');
  
  // 3.1 weight（必填，无默认值）
  const weightField = mapping.fields.weight;
  if (weightField) {
    let weight = null;
    // 优先从 args 读取
    if (data.args && data.args.weight) {
      const weightStr = String(data.args.weight);
      if (weightStr.includes('kg')) {
        weight = parseFloat(weightStr.replace('kg', '')) * 1000;
      } else if (weightStr.includes('g')) {
        weight = parseFloat(weightStr.replace('g', ''));
      } else {
        weight = parseFloat(weightStr);
      }
    }
    // 如果 args 没有，尝试从 result.json 读取
    if (!weight && data['ozon-pricer'] && data['ozon-pricer'].weightKg) {
      weight = data['ozon-pricer'].weightKg * 1000;
    }
    // 没有重量直接报错
    if (!weight) {
      throw new Error('❌ 重量 weight 是必填参数，请通过 -w 参数传递（如 -w 1.25kg 或 -w 1250g）');
    }
    productData.weight = parseInt(weight);
    productData.weight_unit = 'g';
    console.log(`✅ 重量：${productData.weight} g`);
  }
  
  // 3.2 package dimensions（优先 args，其次 fallback）
  const dimensionFields = {
    length: mapping.fields.length,
    width: mapping.fields.width,
    height: mapping.fields.height,
    depth: mapping.fields.depth
  };
  
  for (const [ozonField, field] of Object.entries(dimensionFields)) {
    if (field) {
      let value = null;
      // 尝试从 args 读取
      if (data.args && data.args[ozonField]) {
        value = data.args[ozonField];
      }
      // 如果 args 没有，使用 fallback
      if (!value) {
        value = field.fallback;
      }
      if (value) {
        productData[ozonField] = parseInt(value);
        console.log(`✅ ${ozonField}: ${productData[ozonField]} cm`);
      }
    }
  }
  
  // 3.3 dimension_unit
  productData.dimension_unit = 'cm';
  
  // 4. 默认值
  productData.vat = '0'; // 跨境商品税率 0
  productData.currency = 'CNY'; // OZON 中国卖家使用 CNY 计价
  
  // 5. 数量设置
  productData.min_quantity = 1; // 散装最低数量，固定 1
  productData.quantity = 1; // 原厂包装数量，固定 1
  console.log(`✅ 最低数量：${productData.min_quantity}`);
  console.log(`✅ 包装数量：${productData.quantity}`);
  
  // 2. attributes（异步构建）
  console.log('\n📋 构建属性列表（动态查询）...');
  productData.attributes = await buildAttributesAsync(data, mapping);
  
  return productData;
}

/**
 * 构建完整商品数据 v2.0（同步版本，兼容旧代码）
 */
function buildProduct(data, mapping) {
  console.log('\n🔧 构建完整商品数据（同步）...\n');
  
  // 1. 核心字段
  const productData = {};
  
  // 1.1 title → name
  const titleField = mapping.fields.title;
  if (titleField && data['1688-tt']?.copy_writing) {
    productData.name = extractTitle(data['1688-tt'].copy_writing);
    console.log(`✅ 商品标题：${productData.name}`);
  }
  
  // 1.2 description
  const descField = mapping.fields.description;
  if (descField && data['1688-tt']?.copy_writing) {
    productData.description = extractDescription(data['1688-tt'].copy_writing);
    console.log(`✅ 商品描述：${productData.description.substring(0, 50)}...`);
  }
  
  // 1.3 price
  const priceField = mapping.fields.price;
  if (priceField && data['ozon-pricer']?.price_cny) {
    productData.price = String(data['ozon-pricer'].price_cny);
    console.log(`✅ 售价：¥${productData.price} CNY`);
  }
  
  // 1.4 old_price
  const oldPriceField = mapping.fields.old_price;
  if (oldPriceField && data['ozon-pricer']?.old_price_cny) {
    productData.old_price = String(data['ozon-pricer'].old_price_cny);
    console.log(`✅ 划线价：¥${productData.old_price} CNY`);
  }
  
  // 1.5 hashtags
  const hashtagField = mapping.fields.hashtags;
  if (hashtagField && data['1688-tt']?.copy_writing) {
    productData.hashtags = extractHashtags(data['1688-tt'].copy_writing);
    console.log(`✅ 标签：${productData.hashtags.join(' ')}`);
  }
  
  // 1.6 images
  const imagesField = mapping.fields.images;
  if (imagesField && data['ozon-image-translator']?.images) {
    const allImages = data['ozon-image-translator'].images;
    const mainImages = allImages.filter(f => f.startsWith('main_') || f.startsWith('main-'));
    const detailImages = allImages.filter(f => f.startsWith('detail_') || f.startsWith('detail-'));
    productData._imageFiles = { main: mainImages, detail: detailImages };
    console.log(`✅ 图片：${mainImages.length} 张主图，${detailImages.length} 张详情图`);
  }
  
  productData.images = [];
  productData.rich_content = null;
  productData.description_category_id = mapping.description_category_id;
  productData.type_id = mapping.type_id;
  productData.offer_id = generateOfferId();
  
  // 2. attributes（同步版本，使用静态字典）
  console.log('\n📋 构建属性列表（静态字典）...');
  productData.attributes = buildAttributes(data, mapping);
  
  // 3. 包装信息
  console.log('\n📦 构建包装信息...');
  const weightField = mapping.fields.weight;
  if (weightField) {
    const weight = getSourceValue(weightField.source, data);
    if (weight) {
      productData.weight = parseInt(weight);
      productData.weight_unit = 'g';
      console.log(`✅ 重量：${productData.weight} g`);
    }
  }
  
  const packageFields = { package_length: 'length', package_width: 'width', package_height: 'height' };
  for (const [fieldName, ozonField] of Object.entries(packageFields)) {
    const field = mapping.fields[fieldName];
    if (field) {
      const value = getSourceValue(field.source, data) || field.fallback;
      productData[ozonField] = parseInt(value);
      console.log(`✅ ${ozonField}: ${productData[ozonField]} cm`);
    }
  }
  
  productData.vat = '0';
  productData.currency = 'CNY';
  productData.min_quantity = 1;
  productData.quantity = 1;
  
  return productData;
}

/**
 * 主函数：执行映射（异步版本）
 */
async function mapAsync(category = 'toy', args = {}) {
  console.log(`🗺️  开始映射 - 类目：${category} (异步)`);
  
  // 1. 从 input 目录加载数据
  console.log('📂 从 input 目录加载数据...');
  const data = loadInputData();
  
  // 添加命令行参数到 data
  if (Object.keys(args).length > 0) {
    data.args = args;
    console.log(`📥 命令行参数：${JSON.stringify(args)}`);
  }
  
  // 2. 加载映射规则
  const mapping = loadCategoryMapping(category);
  console.log(`📋 加载映射规则：${mapping.category_name_cn} (${mapping.description_category_id})`);
  
  // 3. 构建商品数据（异步）
  const productData = await buildProductAsync(data, mapping);
  
  console.log('✅ 映射完成（动态查询）');
  
  return {
    mapping: mapping,
    product: productData,
    rawData: data
  };
}

/**
 * 主函数：执行映射（同步版本，兼容旧代码）
 */
function map(category = 'toy') {
  console.log(`🗺️  开始映射 - 类目：${category}`);
  
  // 1. 从 input 目录加载数据
  console.log('📂 从 input 目录加载数据...');
  const data = loadInputData();
  
  // 2. 加载映射规则
  const mapping = loadCategoryMapping(category);
  console.log(`📋 加载映射规则：${mapping.category_name_cn} (${mapping.description_category_id})`);
  
  // 3. 构建商品数据
  const productData = buildProduct(data, mapping);
  
  console.log('✅ 映射完成');
  
  return {
    mapping: mapping,
    product: productData,
    rawData: data
  };
}

// CLI 支持
// CLI 入口（异步版本）
if (require.main === module) {
  (async () => {
    try {
      // 解析命令行参数
      const args = {};
      let category = 'toy_set';
      
      for (let i = 2; i < process.argv.length; i++) {
        if (process.argv[i] === '--category' && process.argv[i + 1]) {
          category = process.argv[i + 1];
          i++;
        } else if (process.argv[i] === '--weight' && process.argv[i + 1]) {
          args.weight = process.argv[i + 1];
          i++;
        } else if (process.argv[i] === '--length' && process.argv[i + 1]) {
          args.length = process.argv[i + 1];
          i++;
        } else if (process.argv[i] === '--width' && process.argv[i + 1]) {
          args.width = process.argv[i + 1];
          i++;
        } else if (process.argv[i] === '--height' && process.argv[i + 1]) {
          args.height = process.argv[i + 1];
          i++;
        }
      }
      
      console.log(`📥 命令行参数：${JSON.stringify(args)}`);
      
      const result = await mapAsync(category, args);
      
      // 保存映射结果到主目录（新架构）
      const outputFile = path.join(DIR_OUTPUT, 'mapping_result.json');
      fs.writeFileSync(outputFile, JSON.stringify(result.product, null, 2));
      console.log(`\n✅ 映射结果已保存：${outputFile}`);
      
      // 生成 upload-request.json（OZON 上传请求格式）
      const uploadRequestFile = path.join(DIR_OUTPUT, 'upload-request.json');
      fs.writeFileSync(uploadRequestFile, JSON.stringify({ items: [result.product] }, null, 2));
      console.log(`✅ 上传请求已保存：${uploadRequestFile}`);
      
      console.log('\n📦 最终结果:');
      console.log(JSON.stringify(result.product, null, 2));
    } catch (error) {
      console.error('❌ 映射失败:', error.message);
      console.error('\n💡 提示：请确保 input 目录有数据');
      console.error('   运行 full-workflow.js 会自动复制数据到 input 目录');
      process.exit(1);
    }
  })();
}

// 导出
module.exports = {
  map,
  mapAsync,
  loadInputData,
  loadCategoryMapping,
  buildAttributesAsync,
  buildProduct,
  buildProductAsync,
  parseProductInfo,
  getSourceValue
};
