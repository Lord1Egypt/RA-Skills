#!/usr/bin/env node
/**
 * 获取属性的所有预设值（字典值）
 * 
 * 用法：
 * node fetch-attribute-values.js <attribute_id> <category_id> <type_id> [attr_name]
 * 
 * 示例：
 * node fetch-attribute-values.js 4975 17028973 970895715 material
 * node fetch-attribute-values.js 10096 17028973 970895715 color
 * node fetch-attribute-values.js 4978 17028973 970895715 age
 * 
 * 输出：
 * - attributes/{name}_dict.json - 字典值列表
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../config/config.json');
const ATTRIBUTES_DIR = path.join(__dirname, '../attributes');

const OZON_API_HOST = 'api-seller.ozon.ru';

/**
 * 加载配置
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('配置文件不存在，请先创建 config/config.json');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
}

/**
 * 发送 OZON API 请求
 */
function ozonRequest(endpoint, body, config) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(body);
    const options = {
      hostname: OZON_API_HOST,
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
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          reject(new Error(`API 响应解析失败：${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 获取属性所有值（支持分页）
 */
async function fetchAllValues(attributeId, categoryId, typeId, config) {
  const allValues = [];
  let lastValueId = 0;
  let hasMore = true;
  let page = 1;
  
  console.log(`📡 开始获取属性值...`);
  console.log(`   attribute_id: ${attributeId}`);
  console.log(`   category_id: ${categoryId}`);
  console.log(`   type_id: ${typeId}`);
  console.log('');
  
  while (hasMore) {
    console.log(`📄 第 ${page} 页...`);
    
    const result = await ozonRequest('/v1/description-category/attribute/values', {
      attribute_id: attributeId,
      description_category_id: categoryId,
      type_id: typeId,
      language: 'ZH_HANS', // 中文，方便匹配
      limit: 1000,
      last_value_id: lastValueId
    }, config);
    
    if (!result.result || !Array.isArray(result.result)) {
      console.error('❌ API 返回格式错误:', result);
      break;
    }
    
    const values = result.result;
    console.log(`   ✅ 获取到 ${values.length} 个值`);
    
    allValues.push(...values);
    
    hasMore = result.has_next;
    if (hasMore && values.length > 0) {
      lastValueId = values[values.length - 1].id;
      page++;
      
      // 延迟一下，避免 API 限流
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }
  
  return allValues;
}

/**
 * 保存字典文件
 */
function saveDictionary(name, values, attributeId, categoryId, typeId) {
  const dict = {
    attribute_id: attributeId,
    description_category_id: categoryId,
    type_id: typeId,
    generated_at: new Date().toISOString(),
    total_values: values.length,
    values: values.map(v => ({
      id: v.id,
      value: v.value,
      info: v.info || '',
      picture: v.picture || ''
    }))
  };
  
  const dictFile = path.join(ATTRIBUTES_DIR, `${name}_dict.json`);
  fs.writeFileSync(dictFile, JSON.stringify(dict, null, 2), 'utf-8');
  console.log(`\n✅ 字典已保存：${dictFile}`);
  console.log(`   总记录数：${values.length}`);
  
  // 打印前 10 条示例
  console.log('\n📋 前 10 条示例:');
  values.slice(0, 10).forEach((v, i) => {
    console.log(`   ${i + 1}. ${v.value} (${v.info}) [ID: ${v.id}]`);
  });
  
  return dictFile;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 3) {
    console.log('用法：node fetch-attribute-values.js <attribute_id> <category_id> <type_id> [attr_name]');
    console.log('示例：node fetch-attribute-values.js 4975 17028973 970895715 material');
    process.exit(1);
  }
  
  const attributeId = parseInt(args[0]);
  const categoryId = parseInt(args[1]);
  const typeId = parseInt(args[2]);
  const attrName = args[3] || `attr_${attributeId}`;
  
  console.log('🚀 开始获取属性字典值');
  console.log(`   属性：${attrName}`);
  console.log(`   attribute_id: ${attributeId}`);
  console.log('');
  
  const config = loadConfig();
  
  // 获取所有值
  const values = await fetchAllValues(attributeId, categoryId, typeId, config);
  
  if (values.length === 0) {
    console.log('\n⚠️  该属性没有预设值（可能是自由文本属性）');
    process.exit(0);
  }
  
  // 保存字典
  saveDictionary(attrName, values, attributeId, categoryId, typeId);
  
  console.log('\n✅ 完成！');
  console.log('\n下一步:');
  console.log(`1. 检查字典文件：attributes/${attrName}_dict.json`);
  console.log(`2. 在映射表中使用字典值 ID`);
  console.log(`3. 创建中文→俄文的映射关系`);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
