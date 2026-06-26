#!/usr/bin/env node
const { program } = require('commander');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

program
  .name('feishu-doc-exporter')
  .description('批量导出飞书文档为 Markdown/PDF 格式');

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

// 读取文档内容
async function readDocument(docToken) {
  const result = await callOpenClawTool('feishu_doc', {
    action: 'read',
    doc_token: docToken
  });
  return result.data;
}

// 列出文件夹内容
async function listFolder(folderToken, recursive = false) {
  const result = await callOpenClawTool('feishu_drive', {
    action: 'list',
    folder_token: folderToken
  });
  
  let items = result.data.items;
  
  if (recursive) {
    for (const item of [...items]) {
      if (item.type === 'folder') {
        const subItems = await listFolder(item.token, true);
        items = items.concat(subItems.map(subItem => ({
          ...subItem,
          path: path.join(item.name, subItem.path || subItem.name)
        })));
      }
    }
  }
  
  return items;
}

// 保存为 Markdown 文件
function saveMarkdown(content, outputPath, title) {
  const filePath = path.join(outputPath, `${title.replace(/[\/\\:*?"<>|]/g, '_')}.md`);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content);
  return filePath;
}

program
  .command('export')
  .description('导出飞书文档')
  .option('--url <url>', '文档URL')
  .option('--folder <token>', '文件夹token')
  .option('--format <format>', '导出格式: markdown/pdf', 'markdown')
  .option('--output <path>', '输出目录', './export')
  .option('--recursive', '递归导出子文件夹')
  .action(async (options) => {
    try {
      console.log('🚀 开始导出飞书文档...');
      
      // 创建输出目录
      fs.mkdirSync(options.output, { recursive: true });
      
      if (options.url) {
        // 导出单个文档
        const docToken = options.url.match(/docx\/([^\/?#]+)/)?.[1];
        if (!docToken) throw new Error('无效的文档URL');
        
        console.log(`📄 导出文档: ${docToken}`);
        const content = await readDocument(docToken);
        const title = content.title || docToken;
        const filePath = saveMarkdown(content.content, options.output, title);
        console.log(`✅ 已保存到: ${filePath}`);
        
      } else if (options.folder) {
        // 导出文件夹
        console.log(`📂 导出文件夹: ${options.folder}`);
        const items = await listFolder(options.folder, options.recursive);
        const docItems = items.filter(item => item.type === 'docx');
        
        console.log(`找到 ${docItems.length} 个文档`);
        
        for (let i = 0; i < docItems.length; i++) {
          const item = docItems[i];
          console.log(`\n📄 (${i+1}/${docItems.length}) 导出: ${item.path || item.name}`);
          
          try {
            const content = await readDocument(item.token);
            const title = content.title || item.name;
            const outputSubPath = item.path ? path.join(options.output, path.dirname(item.path)) : options.output;
            const filePath = saveMarkdown(content.content, outputSubPath, title);
            console.log(`✅ 已保存到: ${filePath}`);
          } catch (error) {
            console.log(`❌ 导出失败: ${error.message}`);
          }
        }
      } else {
        throw new Error('请指定 --url 或 --folder 参数');
      }
      
      console.log('\n🎉 导出完成！');
      
    } catch (error) {
      console.error('❌ 导出失败:', error.message);
      process.exit(1);
    }
  });

program
  .command('list')
  .description('列出文件夹中的文档')
  .option('--folder <token>', '文件夹token')
  .option('--recursive', '递归列出子文件夹')
  .action(async (options) => {
    try {
      const items = await listFolder(options.folder, options.recursive);
      
      console.log('📂 文件夹内容:');
      items.forEach(item => {
        const icon = item.type === 'folder' ? '📁' : '📄';
        const itemPath = item.path || item.name;
        console.log(`${icon} ${itemPath} (${item.token})`);
      });
      
      console.log(`\n总计: ${items.length} 个项目`);
      
    } catch (error) {
      console.error('❌ 列表获取失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
