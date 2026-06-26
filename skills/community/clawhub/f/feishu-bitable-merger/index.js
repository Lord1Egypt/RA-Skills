#!/usr/bin/env node
const { program } = require('commander');
const { execSync } = require('child_process');

program
  .name('feishu-bitable-merger')
  .description('合并多个飞书多维表格的数据到一个目标表格');

// 调用 OpenClaw 工具函数
function callOpenClawTool(toolName, params) {
  const paramsJson = JSON.stringify(params);
  const cmd = `openclaw tool call ${toolName} '${paramsJson.replace(/'/g, "'\\''")}'`;
  try {
    const output = execSync(cmd, { encoding: 'utf8' });
    return JSON.parse(output);
  } catch (error) {
    throw new Error(`工具调用失败: ${error.message}`);
  }
}

// 解析表格 URL 获取 app_token 和 table_id
async function parseBitableUrl(url) {
  const result = await callOpenClawTool('feishu_bitable_get_meta', { url });
  return result;
}

// 获取表格字段列表
async function listFields(appToken, tableId) {
  const result = await callOpenClawTool('feishu_bitable_list_fields', { 
    app_token: appToken, 
    table_id: tableId 
  });
  return result.data.items;
}

// 获取表格记录
async function listRecords(appToken, tableId, pageSize = 500) {
  let allRecords = [];
  let pageToken = null;
  
  do {
    const params = {
      app_token: appToken,
      table_id: tableId,
      page_size: pageSize
    };
    if (pageToken) params.page_token = pageToken;
    
    const result = await callOpenClawTool('feishu_bitable_list_records', params);
    allRecords.push(...result.data.items);
    pageToken = result.data.page_token;
  } while (pageToken);
  
  return allRecords;
}

// 批量创建记录
async function createRecords(appToken, tableId, records) {
  const result = await callOpenClawTool('feishu_bitable_create_record', {
    app_token: appToken,
    table_id: tableId,
    records: records
  });
  return result;
}

program
  .command('merge')
  .description('合并多个源表格到目标表格')
  .option('--source <urls...>', '源表格URL列表')
  .option('--target <url>', '目标表格URL')
  .option('--map <mappings...>', '字段映射，格式为"旧字段:新字段"')
  .option('--deduplicate', '合并后去重')
  .action(async (options) => {
    try {
      console.log('🚀 开始合并多维表格...');
      
      // 解析目标表格信息
      const targetMeta = await parseBitableUrl(options.target);
      console.log(`✅ 目标表格解析完成: ${targetMeta.app_token}`);
      
      // 获取目标表格字段
      const targetFields = await listFields(targetMeta.app_token, targetMeta.table_id);
      const targetFieldNames = targetFields.map(f => f.field_name);
      console.log(`✅ 目标表格字段: ${targetFieldNames.join(', ')}`);
      
      // 处理字段映射
      const fieldMap = {};
      if (options.map) {
        options.map.forEach(mapping => {
          const [oldField, newField] = mapping.split(':');
          fieldMap[oldField.trim()] = newField.trim();
        });
        console.log(`✅ 字段映射配置: ${JSON.stringify(fieldMap)}`);
      }
      
      // 处理每个源表格
      let allRecords = [];
      for (const sourceUrl of options.source) {
        console.log(`\n📥 处理源表格: ${sourceUrl}`);
        const sourceMeta = await parseBitableUrl(sourceUrl);
        const sourceFields = await listFields(sourceMeta.app_token, sourceMeta.table_id);
        const sourceRecords = await listRecords(sourceMeta.app_token, sourceMeta.table_id);
        
        console.log(`   读取到 ${sourceRecords.length} 条记录`);
        
        // 转换记录字段
        const convertedRecords = sourceRecords.map(record => {
          const newFields = {};
          Object.entries(record.fields).forEach(([key, value]) => {
            const newKey = fieldMap[key] || key;
            if (targetFieldNames.includes(newKey)) {
              newFields[newKey] = value;
            }
          });
          return { fields: newFields };
        });
        
        allRecords.push(...convertedRecords);
      }
      
      // 去重处理
      if (options.deduplicate) {
        const uniqueKeys = new Set();
        const uniqueRecords = [];
        allRecords.forEach(record => {
          const key = JSON.stringify(record.fields);
          if (!uniqueKeys.has(key)) {
            uniqueKeys.add(key);
            uniqueRecords.push(record);
          }
        });
        console.log(`\n🔍 去重后剩余 ${uniqueRecords.length} 条记录`);
        allRecords = uniqueRecords;
      }
      
      // 批量写入目标表格
      console.log(`\n📤 写入 ${allRecords.length} 条记录到目标表格...`);
      for (let i = 0; i < allRecords.length; i += 500) {
        const batch = allRecords.slice(i, i + 500);
        await createRecords(targetMeta.app_token, targetMeta.table_id, batch);
        console.log(`   已写入 ${Math.min(i + 500, allRecords.length)}/${allRecords.length} 条`);
      }
      
      console.log('\n🎉 合并完成！');
      console.log(`✅ 总共合并 ${allRecords.length} 条记录`);
      
    } catch (error) {
      console.error('❌ 合并失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
