#!/usr/bin/env node
/**
 * 获取指定类目的所有属性并生成完整映射表
 * 
 * 用法：
 * node fetch-attributes.js <description_category_id> <type_id> [category_name]
 * 
 * 示例：
 * node fetch-attributes.js 17028973 970895715 toy_set
 * 
 * 输出：
 * - mappings/{name}_mapping.json - 完整映射表（包含所有属性）
 * - mappings/{name}_mapping.md - 配置说明文档
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../config/config.json');
const MAPPINGS_DIR = path.join(__dirname, '../mappings');
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
          resolve(JSON.parse(data));
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
 * 预定义的智能映射规则
 * 根据属性名自动匹配数据来源
 */
const SMART_MAPPING_RULES = {
  // 必填属性
  '类型': { source: 'fixed', fallback: 'Набор игрушек', transform: '', note: '固定值，根据类目设置' },
  '品牌': { source: 'fixed', fallback: 'Нет бренда', transform: '', note: '无品牌商品' },
  '型号名称（针对合并为一张商品卡片）': { source: 'auto_generate', fallback: '', transform: 'oc#YYYY_MM_DD-hh_mm_ss', note: '自动生成' },
  
  // 核心字段（非属性）
  '商品标题': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_title', note: '从文案提取俄文标题' },
  '商品描述': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_description', note: '从文案提取俄文描述' },
  '售价': { source: 'ozon-pricer.price_rub', fallback: '', transform: '', note: '从价格计算模块获取' },
  '划线价': { source: 'ozon-pricer.old_price_rub', fallback: '', transform: '', note: '从价格计算模块获取' },
  '主图': { source: 'ozon-image-translator.images', fallback: '', transform: '', note: '主图列表（5 张）' },
  '富文本详情': { source: 'ozon-image-translator.images', fallback: '', transform: '', note: '详情图生成富文本（0-35 张）' },
  '标签/话题': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_hashtags', note: '从文案提取俄文标签' },
  
  // 商品属性 - 智能匹配
  '商品颜色': { source: '1688-tt.product_info.color', fallback: 'Синий', transform: 'color_smart', note: '从 1688 获取，智能转换' },
  '颜色名称': { source: '1688-tt.product_info.color', fallback: '', transform: '', note: '颜色名称（可选）' },
  '材料': { source: '1688-tt.product_info.material', fallback: 'Пластик', transform: 'material_smart', note: '从 1688 获取，智能转换' },
  '儿童年龄': { source: '1688-tt.product_info.age', fallback: '3-5 лет', transform: 'age_smart', note: '从 1688 获取' },
  '原产国': { source: 'fixed', fallback: 'Китай', transform: '', note: '固定值：中国' },
  '儿童性别': { source: 'fixed', fallback: 'Унисекс', transform: '', note: '固定值：中性' },
  '性别': { source: 'fixed', fallback: 'Унисекс', transform: '', note: '固定值：中性' },
  '简介': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_annotation', note: '从文案提取简短描述' },
  '卖家代码': { source: 'auto_generate', fallback: '', transform: 'sku_auto', note: '自动生成 SKU' },
  
  // 数量和重量
  '含包装重量，克': { source: '1688-tt.product_info.weight', fallback: '200', transform: '', note: '从 1688 获取（克）' },
  '商品重量': { source: '1688-tt.product_info.weight', fallback: '', transform: '', note: '商品净重' },
  '原厂包装数量': { source: 'fixed', fallback: '1', transform: '', note: '固定值 1' },
  '一个商品中的件数': { source: 'fixed', fallback: '1', transform: '', note: '固定值 1' },
  '散装最低数量': { source: 'fixed', fallback: '1', transform: '', note: '固定值 1' },
  '统一计量单位中的商品数量': { source: 'fixed', fallback: '1', transform: '', note: '固定值 1' },
  
  // 包装
  '包装长度': { source: '1688-tt.product_info.package_length', fallback: '10', transform: '', note: '单位：cm' },
  '包装宽度': { source: '1688-tt.product_info.package_width', fallback: '10', transform: '', note: '单位：cm' },
  '包装高度': { source: '1688-tt.product_info.package_height', fallback: '5', transform: '', note: '单位：cm' },
  
  // 玩具特定属性（有数据来源）
  '游戏原理': { source: '1688-tt.product_info.game_principle', fallback: '', transform: '', note: '从 1688 获取' },
  '拼图类型': { source: '1688-tt.product_info.puzzle_type', fallback: '', transform: '', note: '从 1688 获取' },
  '目标受众': { source: 'fixed', fallback: 'Дети', transform: '', note: '固定值：儿童' },
  '包装': { source: '1688-tt.product_info.packaging', fallback: '', transform: '', note: '从 1688 获取' },
  '拼图难度': { source: '1688-tt.product_info.puzzle_difficulty', fallback: '', transform: '', note: '从 1688 获取' },
  
  // 保修
  '保修期': { source: 'fixed', fallback: '', transform: '', note: '无保修' },
  '保质期（天）': { source: 'fixed', fallback: '', transform: '', note: '无保质期' },
  
  // 高级功能（暂无数据来源）
  '#主题标签': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_hashtags', note: '从文案提取' },
  '组合成类似的产品': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 用于商品关联' },
  'PDF 文件': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 上传 PDF 文件' },
  'PDF 文件名称': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - PDF 文件名' },
  '名称': { source: '1688-tt.copy_writing', fallback: '', transform: 'extract_title', note: '商品名称' },
  
  // 视频相关（暂无数据来源）
  '臭氧。视频：标题': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 视频标题' },
  '臭氧。视频：链接': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 视频 URL' },
  '臭氧。视频背景：链接': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 背景视频 URL' },
  '臭氧。视频：视频产品': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 视频产品信息' },
  
  // 其他
  '欧亚经济联盟的 HS 编码': { source: '', fallback: '', transform: '', note: '⚠️ 需手动配置 - 海关编码' },
  'JSON 富内容': { source: 'ozon-image-translator.images', fallback: '', transform: '', note: '详情图生成富文本 JSON' }
};

/**
 * 映射属性类型
 */
function mapAttributeType(apiType) {
  const typeMap = {
    'String': 'string',
    'Integer': 'integer',
    'Decimal': 'decimal',
    'Boolean': 'boolean',
    'Dictionary': 'string'
  };
  return typeMap[apiType] || 'string';
}

/**
 * 构建完整字段映射
 */
function buildFields(attributes) {
  const fields = {};
  
  // 1. 核心字段（非属性）
  fields.title = {
    ozon_field: 'name',
    name_ru: 'Название',
    name_cn: '商品标题',
    required: true,
    type: 'string',
    source: '1688-tt.copy_writing',
    transform: 'extract_title',
    fallback: '',
    note: '从文案提取俄文标题'
  };
  
  fields.description = {
    ozon_field: 'description',
    name_ru: 'Описание',
    name_cn: '商品描述',
    required: false,
    type: 'string',
    source: '1688-tt.copy_writing',
    transform: 'extract_description',
    fallback: '',
    note: '从文案提取俄文描述'
  };
  
  fields.price = {
    ozon_field: 'price',
    name_ru: 'Цена',
    name_cn: '售价',
    required: true,
    type: 'number',
    source: 'ozon-pricer.price_rub',
    transform: '',
    fallback: '',
    note: '卢布售价'
  };
  
  fields.old_price = {
    ozon_field: 'old_price',
    name_ru: 'Старая цена',
    name_cn: '划线价',
    required: false,
    type: 'number',
    source: 'ozon-pricer.old_price_rub',
    transform: '',
    fallback: '',
    note: '卢布划线价'
  };
  
  fields.images = {
    ozon_field: 'images',
    name_ru: 'Изображения',
    name_cn: '主图',
    required: true,
    type: 'array',
    source: 'ozon-image-translator.images',
    transform: '',
    fallback: '',
    note: '5 张主图'
  };
  
  fields.rich_content = {
    ozon_field: 'rich_content',
    name_ru: 'Rich-контент',
    name_cn: '富文本详情',
    required: false,
    type: 'object',
    source: 'ozon-image-translator.images',
    transform: '',
    fallback: '',
    note: '详情图生成富文本 JSON'
  };
  
  fields.hashtags = {
    ozon_field: 'hashtags',
    name_ru: 'Хэштеги',
    name_cn: '标签/话题',
    required: false,
    type: 'array',
    source: '1688-tt.copy_writing',
    transform: 'extract_hashtags',
    fallback: [],
    note: '从文案提取标签'
  };
  
  fields.weight = {
    ozon_field: 'weight',
    ozon_attribute_id: 0,
    name_ru: 'Вес',
    name_cn: '含包装重量',
    required: false,
    type: 'number',
    source: '1688-tt.product_info.weight',
    transform: '',
    fallback: '200',
    note: '单位：g'
  };
  
  fields.package_length = {
    ozon_field: 'length',
    ozon_attribute_id: 0,
    name_ru: 'Длина',
    name_cn: '包装长度',
    required: false,
    type: 'number',
    source: '1688-tt.product_info.package_length',
    transform: '',
    fallback: '10',
    note: '单位：cm'
  };
  
  fields.package_width = {
    ozon_field: 'width',
    ozon_attribute_id: 0,
    name_ru: 'Ширина',
    name_cn: '包装宽度',
    required: false,
    type: 'number',
    source: '1688-tt.product_info.package_width',
    transform: '',
    fallback: '10',
    note: '单位：cm'
  };
  
  fields.package_height = {
    ozon_field: 'height',
    ozon_attribute_id: 0,
    name_ru: 'Высота',
    name_cn: '包装高度',
    required: false,
    type: 'number',
    source: '1688-tt.product_info.package_height',
    transform: '',
    fallback: '5',
    note: '单位：cm'
  };
  
  fields.min_quantity = {
    ozon_field: 'min_quantity',
    ozon_attribute_id: 23518,
    name_ru: 'Минимальное количество для опта',
    name_cn: '散装最低数量',
    required: false,
    type: 'integer',
    source: 'fixed',
    transform: '',
    fallback: '1',
    note: '固定值 1'
  };
  
  fields.quantity = {
    ozon_field: 'quantity',
    ozon_attribute_id: 8962,
    name_ru: 'Количество в упаковке',
    name_cn: '一个商品中的件数',
    required: false,
    type: 'integer',
    source: 'fixed',
    transform: '',
    fallback: '1',
    note: '固定值 1'
  };
  
  fields.package_quantity = {
    ozon_field: 'package_quantity',
    ozon_attribute_id: 11650,
    name_ru: 'Количество в заводской упаковке',
    name_cn: '原厂包装数量',
    required: false,
    type: 'integer',
    source: 'fixed',
    transform: '',
    fallback: '1',
    note: '固定值 1'
  };
  
  // 2. 遍历 API 属性，为每个属性创建映射
  console.log('\n📊 构建属性映射...\n');
  
  for (const attr of attributes) {
    const attrName = attr.name;
    const rule = SMART_MAPPING_RULES[attrName];
    
    if (rule) {
      // 有预定义规则
      fields[attrName] = {
        ozon_attribute_id: attr.id,
        name_ru: attrName,
        name_cn: attrName,
        required: attr.is_required,
        type: mapAttributeType(attr.type),
        dictionary_id: attr.dictionary_id || 0,
        source: rule.source,
        transform: rule.transform || '',
        fallback: rule.fallback || '',
        note: rule.note,
        is_collection: attr.is_collection,
        is_aspect: attr.is_aspect
      };
      console.log(`  ✅ ${attrName} (ID: ${attr.id}) - ${rule.source ? '有数据源' : '⚠️ 需配置'}`);
    } else {
      // 没有预定义规则，创建空映射
      fields[attrName] = {
        ozon_attribute_id: attr.id,
        name_ru: attrName,
        name_cn: attrName,
        required: attr.is_required,
        type: mapAttributeType(attr.type),
        dictionary_id: attr.dictionary_id || 0,
        source: '',
        transform: '',
        fallback: '',
        note: `⚠️ 需手动配置 - ${attr.description ? attr.description.substring(0, 50) : '无描述'}`,
        is_collection: attr.is_collection,
        is_aspect: attr.is_aspect
      };
      const required = attr.is_required ? '【必填】' : '';
      console.log(`  ⚠️ ${attrName} (ID: ${attr.id}) ${required} - 无数据源，需手动配置`);
    }
  }
  
  return fields;
}

/**
 * 生成说明文档
 */
function generateMarkdownDoc(fields, categoryName, categoryId, typeId) {
  const requiredFields = Object.values(fields).filter(f => f.required);
  const optionalFields = Object.values(fields).filter(f => !f.required);
  const configuredFields = Object.values(fields).filter(f => f.source);
  const unconfiguredFields = Object.values(fields).filter(f => !f.source);
  
  let md = `# ${categoryName} 类目映射配置\n\n`;
  md += `## 类目信息\n\n`;
  md += `- **商品类型**: ${categoryName}\n`;
  md += `- **一级/二级类目 ID**: ${categoryId}\n`;
  md += `- **商品类型 ID**: ${typeId}\n`;
  md += `- **生成时间**: ${new Date().toISOString().replace('T', ' ').substring(0, 19)}\n`;
  md += `- **总属性数**: ${Object.keys(fields).length}\n`;
  md += `- **已配置**: ${configuredFields.length}\n`;
  md += `- **待配置**: ${unconfiguredFields.length}\n\n`;
  
  md += `---\n\n`;
  
  md += `## 必填属性（${requiredFields.length}个）\n\n`;
  md += `| 属性名 | 属性 ID | 数据来源 | 默认值 | 说明 |\n`;
  md += `|--------|--------|---------|--------|------|\n`;
  requiredFields.forEach(f => {
    const source = f.source || '❌ 未配置';
    const fallback = f.fallback || '-';
    md += `| ${f.name_cn} | ${f.ozon_attribute_id || 'N/A'} | ${source} | ${fallback} | ${f.note} |\n`;
  });
  md += `\n`;
  
  md += `## 可选属性（已配置 ${configuredFields.filter(f => !f.required && f.source).length}个）\n\n`;
  md += `| 属性名 | 属性 ID | 数据来源 | 默认值 | 说明 |\n`;
  md += `|--------|--------|---------|--------|------|\n`;
  optionalFields.filter(f => f.source).forEach(f => {
    md += `| ${f.name_cn} | ${f.ozon_attribute_id || 'N/A'} | ${f.source} | ${f.fallback || '-'} | ${f.note} |\n`;
  });
  md += `\n`;
  
  md += `## 待配置属性（${unconfiguredFields.length}个）\n\n`;
  md += `> ⚠️ 这些属性没有数据来源，需要手动配置 \`source\` 字段\n\n`;
  md += `| 属性名 | 属性 ID | 是否必填 | 说明 |\n`;
  md += `|--------|--------|---------|------|\n`;
  unconfiguredFields.forEach(f => {
    const required = f.required ? '✅ 是' : '❌ 否';
    md += `| ${f.name_cn} | ${f.ozon_attribute_id || 'N/A'} | ${required} | ${f.note} |\n`;
  });
  md += `\n`;
  
  md += `---\n\n`;
  
  md += `## 配置指南\n\n`;
  md += `### 数据来源（source）格式\n\n`;
  md += `\`\`\`\n`;
  md += `- 1688-tt.product_info.color       # 从 1688 商品数据获取\n`;
  md += `- 1688-tt.copy_writing             # 从文案获取\n`;
  md += `- ozon-pricer.price_rub            # 从价格计算模块获取\n`;
  md += `- ozon-image-translator.images     # 从图片翻译模块获取\n`;
  md += `- fixed                            # 固定值（使用 fallback）\n`;
  md += `- auto_generate                    # 自动生成（使用 transform）\n`;
  md += `- (空)                             # 无数据来源，跳过\n`;
  md += `\`\`\`\n\n`;
  
  md += `### 转换规则（transform）\n\n`;
  md += `\`\`\`\n`;
  md += `- extract_title                    # 提取俄文标题\n`;
  md += `- extract_description              # 提取俄文描述\n`;
  md += `- extract_hashtags                 # 提取俄文标签\n`;
  md += `- extract_annotation               # 提取简短描述\n`;
  md += `- color_smart                      # 智能颜色转换\n`;
  md += `- material_smart                   # 智能材质转换\n`;
  md += `- age_smart                        # 智能年龄转换\n`;
  md += `- oc#YYYY_MM_DD-hh_mm_ss          # 自动生成型号\n`;
  md += `- sku_auto                         # 自动生成 SKU\n`;
  md += `\`\`\`\n\n`;
  
  md += `## 使用示例\n\n`;
  md += `\`\`\`bash\n`;
  md += `# 测试映射\n`;
  md += `node scripts/map.js ${categoryName}\n\n`;
  md += `# 执行完整上传流程\n`;
  md += `https://detail.1688.com/offer/XXX.html op -w 200g -p 10\n`;
  md += `\`\`\`\n`;
  
  return md;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法：node fetch-attributes.js <description_category_id> <type_id> [category_name]');
    console.log('示例：node fetch-attributes.js 17028973 970895715 toy_set');
    process.exit(1);
  }
  
  const categoryId = args[0];
  const typeId = args[1];
  const categoryName = args[2] || 'category';
  
  console.log('🚀 开始获取类目属性并生成完整映射表');
  console.log(`   类目：${categoryName}`);
  console.log(`   description_category_id: ${categoryId}`);
  console.log(`   type_id: ${typeId}`);
  console.log('');
  
  const config = loadConfig();
  
  // 1. 获取属性列表
  console.log('📡 请求属性列表...');
  console.log(`   - description_category_id: ${categoryId}`);
  console.log(`   - type_id: ${typeId}`);
  console.log(`   - language: ZH_HANS`);
  
  const result = await ozonRequest('/v1/description-category/attribute', {
    description_category_id: parseInt(categoryId),
    type_id: parseInt(typeId),
    language: 'ZH_HANS'
  }, config);
  
  if (!result.result || !Array.isArray(result.result)) {
    console.error('❌ API 返回格式错误:', result);
    process.exit(1);
  }
  
  const attributes = result.result;
  console.log(`✅ 获取到 ${attributes.length} 个属性\n`);
  
  // 2. 分析属性
  console.log('📊 分析属性...\n');
  const required = attributes.filter(a => a.is_required);
  const optional = attributes.filter(a => !a.is_required);
  console.log(`   必填属性：${required.length}个`);
  console.log(`   可选属性：${optional.length}个\n`);
  
  // 3. 构建映射
  const fields = buildFields(attributes);
  
  // 4. 构建完整映射对象
  const mapping = {
    category_name: categoryName,
    description_category_id: parseInt(categoryId),
    type_id: parseInt(typeId),
    generated_at: new Date().toISOString(),
    total_attributes: attributes.length,
    fields: fields
  };
  
  // 5. 保存 JSON
  const mappingFile = path.join(MAPPINGS_DIR, `${categoryName}_mapping.json`);
  fs.writeFileSync(mappingFile, JSON.stringify(mapping, null, 2), 'utf-8');
  console.log(`\n✅ 映射表已保存：${mappingFile}`);
  
  // 6. 生成说明文档
  const mdContent = generateMarkdownDoc(fields, categoryName, categoryId, typeId);
  const mdFile = path.join(MAPPINGS_DIR, `${categoryName}_mapping.md`);
  fs.writeFileSync(mdFile, mdContent, 'utf-8');
  console.log(`✅ 说明文档已保存：${mdFile}`);
  
  // 7. 统计
  const configuredCount = Object.values(fields).filter(f => f.source).length;
  const unconfiguredCount = Object.values(fields).filter(f => !f.source).length;
  const requiredUnconfigured = required.filter(a => {
    const field = Object.values(fields).find(f => f.ozon_attribute_id === a.id);
    return field && !field.source;
  }).length;
  
  console.log('\n📊 统计:');
  console.log(`   总字段数：${Object.keys(fields).length}`);
  console.log(`   已配置：${configuredCount}`);
  console.log(`   待配置：${unconfiguredCount}`);
  
  if (requiredUnconfigured > 0) {
    console.log(`\n⚠️  警告：${requiredUnconfigured} 个必填属性未配置数据源！`);
    console.log(`   请编辑 ${mappingFile} 补充配置\n`);
  }
  
  console.log('\n✅ 完成！');
  console.log('\n下一步:');
  console.log(`1. 检查映射表：${mappingFile}`);
  console.log(`2. 阅读说明：${mdFile}`);
  console.log(`3. 补充未配置的属性（特别是必填属性）`);
  console.log(`4. 测试映射：node scripts/map.js ${categoryName}`);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
