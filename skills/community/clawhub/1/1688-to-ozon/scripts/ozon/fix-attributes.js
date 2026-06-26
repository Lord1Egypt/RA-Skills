#!/usr/bin/env node
/**
 * 修复 OZON 商品重复属性问题
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../config/config.json');

function loadConfig() {
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
}

function ozonRequest(endpoint, body, config) {
  return new Promise((resolve, reject) => {
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
          resolve(result);
        } catch (e) {
          reject(new Error('解析响应失败：' + data));
        }
      });
    });

    req.on('error', (err) => {
      reject(new Error('网络错误：' + err.message));
    });

    req.write(postData);
    req.end();
  });
}

async function fixProductAttributes() {
  const config = loadConfig();
  
  // 已导入的商品信息
  const productId = 3916060327;
  const offerId = 'ozon_1774621377347_dc8a0146';
  
  console.log('🔧 开始修复商品属性...\n');
  console.log(`product_id: ${productId}`);
  console.log(`offer_id: ${offerId}\n`);
  
  // 读取映射结果文件，获取完整的商品数据
  const mappingFile = path.join(__dirname, '../data/mappings/ozon_1774621377347_dc8a0146.json');
  
  if (!fs.existsSync(mappingFile)) {
    console.log('⚠️  映射文件不存在，尝试从 upload-request.json 读取');
    
    const WORKSPACE_DIR = process.cwd();
    const uploadRequestFile = path.join(WORKSPACE_DIR, 'projects/ozon-publisher/input/upload-request.json');
    if (!fs.existsSync(uploadRequestFile)) {
      console.error('❌ upload-request.json 也不存在');
      return;
    }
    
    const uploadRequest = JSON.parse(fs.readFileSync(uploadRequestFile, 'utf-8'));
    const product = uploadRequest.items[0];
    
    console.log('📋 从 upload-request.json 读取商品数据');
    console.log(`   offer_id: ${product.offer_id}`);
    console.log(`   属性数量：${product.attributes?.length || 0}`);
    
    // 重新提交商品（覆盖）
    const updateBody = {
      items: [product]
    };
    
    console.log('\n🔄 重新提交商品（覆盖模式）...');
    
    try {
      const result = await ozonRequest('/v3/product/import', updateBody, config);
      console.log('\n✅ 商品重新导入结果:', JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('\n❌ 重新导入失败:', error.message);
    }
    
  } else {
    console.log('⚠️  需要使用映射文件重新生成商品数据');
  }
}

// 修复路径问题
async function fixProductAttributesV2() {
  const config = loadConfig();
  
  const WORKSPACE_DIR = process.cwd();
  const uploadRequestFile = path.join(WORKSPACE_DIR, 'projects/ozon-publisher/input/upload-request.json');
  
  if (!fs.existsSync(uploadRequestFile)) {
    console.error('❌ upload-request.json 不存在:', uploadRequestFile);
    return;
  }
  
  const uploadRequest = JSON.parse(fs.readFileSync(uploadRequestFile, 'utf-8'));
  const product = uploadRequest.items[0];
  
  console.log('📋 读取商品数据');
  console.log(`   offer_id: ${product.offer_id}`);
  console.log(`   属性数量：${product.attributes?.length || 0}`);
  
  // 检查重复属性
  const attrCount = {};
  product.attributes?.forEach(attr => {
    attrCount[attr.id] = (attrCount[attr.id] || 0) + 1;
  });
  
  console.log('\n🔍 属性统计:');
  Object.entries(attrCount).forEach(([id, count]) => {
    if (count > 1) {
      console.log(`   ❌ 属性 ${id}: 重复 ${count} 次`);
    }
  });
  
  // 重新提交商品（覆盖）
  console.log('\n🔄 重新提交商品（覆盖模式）...');
  
  const updateBody = {
    items: [product]
  };
  
  try {
    const result = await ozonRequest('/v3/product/import', updateBody, config);
    console.log('\n✅ 商品重新导入结果:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('\n❌ 重新导入失败:', error.message);
  }
}

fixProductAttributesV2();

fixProductAttributes();
