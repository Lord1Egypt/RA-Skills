#!/usr/bin/env node
/**
 * OZON 属性值动态查询模块
 * 
 * 功能：
 * 1. 优先从缓存文件加载属性值
 * 2. 缓存不存在时调用 OZON API 查询
 * 3. 自动保存查询结果到缓存
 * 
 * 缓存文件：attributes/type_{type_id}_values.json
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const ATTRIBUTES_DIR = path.join(__dirname, '../../attributes');
const CONFIG_FILE = path.join(__dirname, '../config/config.json');

/**
 * 加载 OZON 配置
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    throw new Error('配置文件不存在：' + CONFIG_FILE);
  }
  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  return config.ozon || config;  // 支持统一配置格式
}

/**
 * 发送 OZON API 请求
 */
function ozonRequest(endpoint, body) {
  return new Promise((resolve, reject) => {
    const config = loadConfig();
    const postData = JSON.stringify(body);
    
    const options = {
      hostname: 'api-seller.ozon.ru',
      port: 443,
      path: endpoint,
      method: 'POST',
      headers: {
        'Client-Id': config.client_id,
        'Api-Key': config.api_key,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.error) {
            reject(new Error(`API 错误：${result.error.message || result.error.code}`));
          } else {
            resolve(result);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 获取缓存文件路径
 * 支持两种格式：type_{typeId}_values.json 和 {categoryName}_attributes.json
 */
function getCacheFilePath(typeId, categoryName = null) {
  // 优先使用类目名称
  if (categoryName) {
    const newPath = path.join(ATTRIBUTES_DIR, `${categoryName}_attributes.json`);
    if (fs.existsSync(newPath)) {
      return newPath;
    }
  }
  // 回退到旧格式
  const oldPath = path.join(ATTRIBUTES_DIR, `type_${typeId}_values.json`);
  if (fs.existsSync(oldPath)) {
    return oldPath;
  }
  // 新格式也没有，返回默认路径
  return newPath || oldPath;
}

/**
 * 从缓存加载属性值
 */
function loadFromCache(typeId, categoryName = null) {
  const cacheFile = getCacheFilePath(typeId, categoryName);
  
  if (!fs.existsSync(cacheFile)) {
    return null;
  }
  
  try {
    const cache = JSON.parse(fs.readFileSync(cacheFile, 'utf-8'));
    
    // 检查缓存是否过期（24 小时）
    const generatedAt = new Date(cache.generated_at);
    const now = new Date();
    const hoursSinceGenerated = (now - generatedAt) / (1000 * 60 * 60);
    
    if (hoursSinceGenerated > 24) {
      console.log(`⚠️  缓存已过期 (${hoursSinceGenerated.toFixed(1)} 小时)，将重新查询`);
      return null;
    }
    
    console.log(`✅ 从缓存加载属性值：type_${typeId} (${Object.keys(cache.attributes || {}).length} 个属性)`);
    return cache;
  } catch (e) {
    console.warn(`⚠️  读取缓存失败：${e.message}`);
    return null;
  }
}

/**
 * 保存属性值到缓存
 */
function saveToCache(typeId, categoryId, attributes, categoryName = null) {
  const cacheFile = getCacheFilePath(typeId, categoryName);
  
  // 确保目录存在
  if (!fs.existsSync(ATTRIBUTES_DIR)) {
    fs.mkdirSync(ATTRIBUTES_DIR, { recursive: true });
  }
  
  const cache = {
    type_id: typeId,
    description_category_id: categoryId,
    generated_at: new Date().toISOString(),
    attributes: attributes
  };
  
  fs.writeFileSync(cacheFile, JSON.stringify(cache, null, 2));
  console.log(`✅ 属性值已保存到缓存：${cacheFile}`);
}

/**
 * 查询单个属性的有效值
 */
async function queryAttributeValue(typeId, categoryId, attributeId) {
  try {
    const result = await ozonRequest('/v1/description-category/attribute/values', {
      attribute_id: attributeId,
      description_category_id: categoryId,
      type_id: typeId,
      limit: 1000
    });
    
    // API 返回格式：{ result: [...] } 或直接是数组
    if (Array.isArray(result)) {
      return result;
    } else if (result.result && Array.isArray(result.result)) {
      return result.result;
    } else if (result.result && result.result.values && Array.isArray(result.result.values)) {
      return result.result.values;
    }
    return [];
  } catch (error) {
    console.warn(`⚠️  查询属性 ${attributeId} 失败：${error.message}`);
    return [];
  }
}

/**
 * 获取属性值（优先缓存，没有则查询 API）
 * 
 * @param {number} typeId - 类型 ID
 * @param {number} categoryId - 分类 ID
 * @param {number} attributeId - 属性 ID
 * @param {boolean} forceRefresh - 是否强制刷新缓存
 * @returns {Promise<Array>} 属性值列表
 */
async function getAttributeValues(typeId, categoryId, attributeId, forceRefresh = false) {
  // 尝试从缓存加载
  if (!forceRefresh) {
    const cache = loadFromCache(typeId);
    if (cache && cache.attributes && cache.attributes[attributeId]) {
      return cache.attributes[attributeId];
    }
  }
  
  // 查询 API
  console.log(`🌐 查询属性值：type=${typeId}, attribute=${attributeId}`);
  const values = await queryAttributeValue(typeId, categoryId, attributeId);
  
  if (values.length > 0) {
    // 保存到缓存
    const cache = loadFromCache(typeId, categoryName) || { type_id: typeId, description_category_id: categoryId, attributes: {} };
    cache.attributes[attributeId] = values;
    saveToCache(typeId, categoryId, cache.attributes, categoryName);
  }
  
  return values;
}

/**
 * 获取所有属性值（批量查询）
 * 
 * @param {number} typeId - 类型 ID
 * @param {number} categoryId - 分类 ID
 * @param {Array<number>} attributeIds - 属性 ID 列表
 * @param {boolean} forceRefresh - 是否强制刷新缓存
 * @param {string} categoryName - 类目名称（如 "toy_set"）
 * @returns {Promise<Object>} 属性值映射表 { attributeId: values }
 */
async function getAllAttributeValues(typeId, categoryId, attributeIds, forceRefresh = false, categoryName = null) {
  // 尝试从缓存加载
  if (!forceRefresh) {
    const cache = loadFromCache(typeId, categoryName);
    if (cache && cache.attributes) {
      // 检查是否所有属性都有缓存
      const allCached = attributeIds.every(id => cache.attributes[id]);
      if (allCached) {
        console.log(`✅ 从缓存加载所有属性值：${attributeIds.length} 个属性`);
        return cache.attributes;
      }
    }
  }
  
  // 批量查询
  console.log(`🌐 批量查询属性值：type=${typeId}, attributes=[${attributeIds.join(', ')}]`);
  const results = {};
  
  for (const attributeId of attributeIds) {
    const values = await queryAttributeValue(typeId, categoryId, attributeId);
    results[attributeId] = values;
    console.log(`  ✅ ${attributeId}: ${values.length} 个值`);
    
    // 避免限流，等待 100ms
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // 保存到缓存
  saveToCache(typeId, categoryId, results, categoryName);
  
  return results;
}

/**
 * 根据中文值匹配字典值 ID
 * 
 * @param {Array} values - 属性值列表
 * @param {string} chineseValue - 中文值（如"塑料"）
 * @param {string} russianValue - 俄文值（如"Пластик"）
 * @returns {Object|null} 匹配的 { id, value } 或 null
 */
function matchValueByChinese(values, chineseValue, russianValue = null) {
  if (!values || values.length === 0) return null;
  
  // 1. 精确匹配俄文值
  if (russianValue) {
    const exactMatch = values.find(v => v.value === russianValue);
    if (exactMatch) {
      return { id: exactMatch.id, value: exactMatch.value };
    }
  }
  
  // 2. 模糊匹配（包含中文关键词）
  if (chineseValue) {
    // 尝试匹配包含中文关键词的值
    const fuzzyMatch = values.find(v => 
      v.value.toLowerCase().includes(chineseValue.toLowerCase()) ||
      v.value.toLowerCase().includes(russianValue?.toLowerCase() || '')
    );
    if (fuzzyMatch) {
      return { id: fuzzyMatch.id, value: fuzzyMatch.value };
    }
  }
  
  // 3. 返回第一个值（默认）
  return { id: values[0].id, value: values[0].value };
}

/**
 * 从值列表中随机选择 N 个
 * 
 * @param {Array} values - 属性值列表
 * @param {number} count - 选择数量
 * @param {Array} excludeKeywords - 排除的关键词（如["多色", "透明"]）
 * @returns {Array} 选中的 { id, value } 列表
 */
function selectRandomValues(values, count = 1, excludeKeywords = []) {
  if (!values || values.length === 0) return [];
  
  // 过滤排除的值
  const filtered = values.filter(v => 
    !excludeKeywords.some(keyword => v.value.includes(keyword))
  );
  
  if (filtered.length === 0) {
    console.warn(`⚠️  过滤后没有可用值，使用原始列表`);
    return values.slice(0, count);
  }
  
  // 随机打乱并选择
  const shuffled = filtered.sort(() => Math.random() - 0.5);
  const selected = shuffled.slice(0, count);
  
  return selected.map(v => ({ id: v.id, value: v.value }));
}

// 导出函数
module.exports = {
  getAttributeValues,
  getAllAttributeValues,
  matchValueByChinese,
  selectRandomValues,
  loadFromCache,
  saveToCache
};
