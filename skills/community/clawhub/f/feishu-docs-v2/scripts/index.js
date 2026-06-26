#!/usr/bin/env node

const lark = require('@larksuiteoapi/node-sdk');
const { Command } = require('commander');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const program = new Command();

// Token 缓存
let tenantTokenCache = null;
let tokenExpireTime = 0;

// 创建认证客户端
function createAuthClient() {
  return new lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
    appType: lark.AppType.SelfBuild,
    domain: process.env.FEISHU_DOMAIN || 'https://open.feishu.cn',
    disableTokenCache: true,
  });
}

// 创建 API 客户端
function createApiClient() {
  return new lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
    appType: lark.AppType.SelfBuild,
    domain: process.env.FEISHU_DOMAIN || 'https://open.feishu.cn',
    disableTokenCache: true,
  });
}

// 获取 Tenant Access Token
async function getTenantToken() {
  // 检查缓存是否有效（提前 5 分钟过期）
  const now = Date.now();
  if (tenantTokenCache && tokenExpireTime > now + 5 * 60 * 1000) {
    return tenantTokenCache;
  }

  try {
    const authClient = createAuthClient();
    const response = await authClient.auth.v3.tenantAccessToken.internal({
      data: {
        app_id: process.env.FEISHU_APP_ID,
        app_secret: process.env.FEISHU_APP_SECRET,
      },
    }, lark.withTenantToken(''));  // 获取 token 时传递空字符串

    if (response.code !== 0) {
      throw new Error(`获取 token 失败: ${response.msg}`);
    }

    tenantTokenCache = response.tenant_access_token;
    // token 有效期一般为 2 小时，单位是秒
    tokenExpireTime = now + response.expire * 1000;

    return tenantTokenCache;
  } catch (error) {
    throw new Error(`获取 Tenant Token 失败: ${error.message}`);
  }
}

// 创建带 token 的请求选项
async function withToken() {
  const token = await getTenantToken();
  return lark.withTenantToken(token);
}

// 错误处理函数
function handleError(error, message) {
  console.error(`❌ ${message}:`, error.message);
  if (process.env.DEBUG) {
    console.error(error);
  }
  process.exit(1);
}

// 验证环境变量
function validateEnv() {
  const required = ['FEISHU_APP_ID', 'FEISHU_APP_SECRET'];
  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    console.error('❌ 缺少必要的环境变量:', missing.join(', '));
    console.log('\n请创建 .env 文件并配置以下变量:');
    console.log('FEISHU_APP_ID=你的应用ID');
    console.log('FEISHU_APP_SECRET=你的应用密钥');
    process.exit(1);
  }
}

program
  .name('feishu-docs')
  .description('飞书文档管理命令行工具')
  .version('1.0.0');

// 读取文档命令
program
  .command('get')
  .description('读取飞书文档内容')
  .requiredOption('-d, --doc-token <token>', '文档 token (docToken)')
  .option('-o, --output <file>', '输出到文件')
  .option('--format <format>', '输出格式: json, markdown, text', 'json')
  .action(async (options) => {
    validateEnv();
    try {
      console.log(`📖 正在读取文档: ${options.docToken}`);

      const client = createApiClient();
      const tokenOption = await withToken();

      // 获取文档元数据
      const docResponse = await client.docx.document.get({
        path: { document_id: options.docToken },
      }, tokenOption);

      // 获取文档内容 (纯文本)
      const contentResponse = await client.docx.document.rawContent.get({
        path: { document_id: options.docToken },
      }, tokenOption);

      const result = {
        meta: docResponse.data,
        content: contentResponse.data,
      };

      // 格式化输出
      let output = '';
      if (options.format === 'json') {
        output = JSON.stringify(result, null, 2);
      } else if (options.format === 'markdown') {
        output = `# ${result.meta?.document?.title || '无标题'}\n\n`;
        output += result.content?.content || '';
      } else {
        output = `标题: ${result.meta?.document?.title || '无标题'}\n`;
        output += `Token: ${result.meta?.document?.document_token}\n`;
        output += `创建时间: ${result.meta?.document?.create_time}\n`;
        output += `更新时间: ${result.meta?.document?.update_time}\n`;
        output += `\n内容:\n${result.content?.content || '无内容'}`;
      }

      if (options.output) {
        fs.writeFileSync(options.output, output);
        console.log(`✅ 文档已保存到: ${options.output}`);
      } else {
        console.log('\n--- 文档内容 ---');
        console.log(output);
      }
    } catch (error) {
      handleError(error, '读取文档失败');
    }
  });

// 获取文档块内容
program
  .command('get-blocks')
  .description('获取文档块内容（结构化数据）')
  .requiredOption('-d, --doc-token <token>', '文档 token (docToken)')
  .option('-o, --output <file>', '输出到文件')
  .action(async (options) => {
    validateEnv();
    try {
      console.log(`📖 正在获取文档块: ${options.docToken}`);

      const client = createApiClient();
      const tokenOption = await withToken();

      const response = await client.docx.document.block.list({
        path: { document_id: options.docToken },
      }, tokenOption);

      const output = JSON.stringify(response.data, null, 2);

      if (options.output) {
        fs.writeFileSync(options.output, output);
        console.log(`✅ 文档块已保存到: ${options.output}`);
      } else {
        console.log('\n--- 文档块内容 ---');
        console.log(output);
      }
    } catch (error) {
      handleError(error, '获取文档块失败');
    }
  });

// 创建文档命令
program
  .command('create')
  .description('创建新的飞书文档')
  .requiredOption('-f, --folder-token <token>', '父文件夹 token')
  .option('-t, --title <title>', '文档标题', '新建文档')
  .option('--content <content>', '文档内容 (纯文本)')
  .option('--file <file>', '从本地文件读取内容')
  .action(async (options) => {
    validateEnv();
    try {
      console.log(`📝 正在创建文档: ${options.title}`);

      let content = options.content || '';

      // 从文件读取内容
      if (options.file) {
        if (!fs.existsSync(options.file)) {
          console.error(`❌ 文件不存在: ${options.file}`);
          process.exit(1);
        }
        content = fs.readFileSync(options.file, 'utf-8');
        console.log(`📄 已读取文件: ${options.file}`);
      }

      const client = createApiClient();
      const tokenOption = await withToken();

      // 创建文档
      const createResponse = await client.docx.document.create({
        data: {
          folder_token: options.folderToken,
          title: options.title,
        },
      }, tokenOption);

      const documentId = createResponse.data?.document?.document_id;
      console.log(`✅ 文档创建成功!`);
      console.log(`   文档 ID: ${documentId}`);
      console.log(`   标题: ${createResponse.data?.document?.title}`);
      console.log(`   URL: ${createResponse.data?.document?.url}`);

      // 如果有内容，添加到文档
      if (content) {
        console.log('📝 正在转换并添加内容...');

        // 1. 将 Markdown 内容转换为 docx 块
        const isMarkdown = options.file?.endsWith('.md') || content.includes('#') || content.includes('- ');
        const convertResponse = await client.docx.document.convert({
          data: {
            content_type: isMarkdown ? 'markdown' : 'html',
            content: content,
          },
        }, tokenOption);

        const blocks = convertResponse.data?.blocks || [];
        if (blocks.length === 0) {
          console.log('⚠️  没有可添加的内容块');
        } else {
          console.log(`🔄 内容已转换为 ${blocks.length} 个块`);

          // 2. 使用 documentBlockDescendant.create 创建块
          const batchSize = 100;
          for (let i = 0; i < blocks.length; i += batchSize) {
            const batch = blocks.slice(i, i + batchSize);
            await client.docx.documentBlockDescendant.create({
              path: {
                document_id: documentId,
                block_id: documentId,
              },
              data: {
                children_id: batch.map((_, idx) => `${documentId}_child_${i + idx}`),
                index: i,
                descendants: batch,
              },
            }, tokenOption);
            console.log(`📝 已添加块 ${i + 1} - ${Math.min(i + batchSize, blocks.length)} / ${blocks.length}`);
          }

          console.log('✅ 内容添加完成');
        }
      }

      // 输出文档信息到文件
      const infoFile = `doc-${documentId}.json`;
      fs.writeFileSync(infoFile, JSON.stringify(createResponse.data, null, 2));
      console.log(`📄 文档信息已保存到: ${infoFile}`);
    } catch (error) {
      handleError(error, '创建文档失败');
    }
  });

async function upload(client, tokenOption,options) {
  try {
    if (!fs.existsSync(options.file)) {
      console.error(`❌ 文件不存在: ${options.file}`);
      process.exit(1);
    }

    const fileName = options.name || path.basename(options.file);
    const fileContent = fs.readFileSync(options.file);
    const fileSize = fileContent.length;

    console.log(`📤 正在上传文件: ${fileName}`);
    console.log(`   大小: ${(fileSize / 1024).toFixed(2)} KB`);
    console.log(`   目标文件夹: ${options.folderToken}`);

    const response = await client.drive.v1.file.uploadAll({
      data: {
        file_name: fileName,
        parent_type: 'explorer',
        parent_node: options.folderToken,
        size: fileSize,
        file: fileContent,
      },
    }, tokenOption);

    if (process.env.DEBUG) {
      console.log('API Response:', JSON.stringify(response, null, 2));
    }

    // 处理不同的响应结构
    const resFileToken = response.data?.file_token || response.file_token;
    const resFileName = response.data?.name || response.name || fileName;


    console.log(`✅ 文件上传成功!`);
    console.log(`   文件 Token: ${resFileToken}`);
    console.log(`   名称: ${resFileName}`);

    return resFileToken;
  } catch (error) {
    handleError(error, '上传文件失败');
    return "";
  }
}

async function importDoc(client, tokenOption, fileToken, options) {
  try {
    console.log(`📥 正在创建导入任务...`);
    console.log(`   源文件 Token: ${fileToken}`);
    console.log(`   目标类型: ${options.type}`);
    console.log(`   文件扩展名: ${options.ext}`);

    const response = await client.drive.v1.importTask.create({
      data: {
        file_extension: options.ext,
        file_token: fileToken,
        type: options.type,
        point: {
          mount_type: 1,
          mount_key: options.folderToken,
        },
      },
    }, tokenOption);

    console.log(`✅ 导入任务创建成功!`);
    console.log(`   任务 ID: ${response.data?.ticket}`);

    return response.data?.ticket;
  } catch (error) {
    handleError(error, '创建导入任务失败');
    return "";
  }
}

// 导入文件为飞书文档
program
  .command('import-file')
  .description('将本地文件导入为飞书文档')
  .requiredOption('-f, --file <path>', '本地文件路径')
  .requiredOption('--folder-token <token>', '父文件夹 token')
  .option('--type <type>', '导入目标类型: docx (文档), sheet (表格), bitable (多维表格)', 'docx')
  .option('--ext <extension>', '源文件扩展名: txt, docx, xlsx, csv, md 等', 'md')
  .action(async (options) => {
    validateEnv();

    const client = createApiClient();
    const tokenOption = await withToken();
    const fileToken = await upload(client,tokenOption,options);
    const taskId = await importDoc(client,tokenOption,fileToken, options);

    let code = -1;
    let response = undefined;
    do{
      console.log(`正在查询任务状态...`);
      response = await client.drive.v1.importTask.get({
            path: {
              ticket:taskId,
            },
          },
          tokenOption
      );
      code = Number(response.data?.result?.job_status);
      await new Promise(resolve => setTimeout(resolve, 1000));
    } while (code === 1 || code === 2);

    console.log(`✅ 查询任务状态成功!`);
    console.log(`   任务状态码: ${response.data?.result?.job_status}`);
    console.log(`   任务描述: ${response.data?.result?.job_error_msg}`);
    console.log(`   云文档地址: ${response.data?.result?.url}`);
  });

// 列出文件夹内容
program
  .command('list')
  .description('列出文件夹内容')
  .option('--folder-token <token>', '文件夹 token (默认根目录)')
  .action(async (options) => {
    validateEnv();
    try {
      console.log(`📂 正在列出文件夹内容...`);

      const client = createApiClient();
      const tokenOption = await withToken();

      // 使用云文档 API 列出文件
      const response = await client.drive.v1.file.list({
        params: {
          folder_token: options.folderToken || '0',
        },
      }, tokenOption);

      const items = response.data?.files || [];

      if (items.length === 0) {
        console.log('📭 文件夹为空');
        return;
      }

      console.log(`\n📂 文件夹内容 (${items.length} 项):\n`);
      console.log('类型\t\t名称\t\t\tToken');
      console.log('-'.repeat(80));

      for (const item of items) {
        const type = item.type === 'docx' ? '📄 文档' :
                     item.type === 'folder' ? '📁 文件夹' : `📦 ${item.type}`;
        const name = (item.name || '').padEnd(20, ' ');
        console.log(`${type}\t${name}\t${item.token}`);
      }
    } catch (error) {
      handleError(error, '列出文件夹失败');
    }
  });

// 删除文档
program
  .command('delete')
  .description('删除飞书文档')
  .requiredOption('-d, --doc-token <token>', '文档 token')
  .option('--force', '强制删除，不提示确认', false)
  .action(async (options) => {
    validateEnv();
    try {
      if (!options.force) {
        console.log(`⚠️  即将删除文档: ${options.docToken}`);
        console.log('请使用 --force 参数确认删除');
        process.exit(1);
      }

      console.log(`🗑️  正在删除文档: ${options.docToken}`);

      const client = createApiClient();
      const tokenOption = await withToken();

      await client.drive.v1.file.delete({
        path: { file_token: options.docToken },
      }, tokenOption);

      console.log('✅ 文档删除成功');
    } catch (error) {
      handleError(error, '删除文档失败');
    }
  });

// 更新文档内容
program
  .command('update')
  .description('更新文档内容')
  .requiredOption('-d, --doc-token <token>', '文档 token')
  .option('--content <content>', '新内容')
  .option('--file <file>', '从本地文件读取内容')
  .option('--append', '追加模式 (默认覆盖)', false)
  .action(async (options) => {
    validateEnv();
    try {
      console.log(`📝 正在更新文档: ${options.docToken}`);

      let content = options.content || '';

      if (options.file) {
        if (!fs.existsSync(options.file)) {
          console.error(`❌ 文件不存在: ${options.file}`);
          process.exit(1);
        }
        content = fs.readFileSync(options.file, 'utf-8');
        console.log(`📄 已读取文件: ${options.file}`);
      }

      if (!content) {
        console.error('❌ 请提供内容或使用 --file 指定文件');
        process.exit(1);
      }

      const client = createApiClient();
      const tokenOption = await withToken();

      const documentId = options.docToken;

      if (!options.append) {
        // 获取当前文档块
        const blocksResponse = await client.docx.document.block.list({
          path: { document_id: documentId },
        }, tokenOption);

        const blocks = blocksResponse.data?.items || [];

        // 删除现有块 (除了文档块本身)
        for (const block of blocks) {
          if (block.block_id !== documentId && block.parent_block_id === documentId) {
            try {
              await client.docx.document.block.delete({
                path: {
                  document_id: documentId,
                  block_id: block.block_id,
                },
              }, tokenOption);
            } catch (e) {
              // 忽略删除错误
            }
          }
        }
      }

      // 添加新内容
      await client.docx.document.block.children.create({
        path: {
          document_id: documentId,
          block_id: documentId,
        },
        data: {
          children: [
            {
              block_type: 2,
              text: {
                elements: [
                  {
                    text_run: {
                      content: content,
                    },
                  },
                ],
              },
            },
          ],
        },
      }, tokenOption);

      console.log('✅ 文档更新成功');
    } catch (error) {
      handleError(error, '更新文档失败');
    }
  });

// 计算 Adler-32 校验和
function calculateAdler32(buffer) {
  const MOD_ADLER = 65521;
  let a = 1;
  let b = 0;

  for (let i = 0; i < buffer.length; i++) {
    a = (a + buffer[i]) % MOD_ADLER;
    b = (b + a) % MOD_ADLER;
  }

  return ((b << 16) | a).toString();
}

// 显示帮助信息
program.on('--help', () => {
  console.log('');
  console.log('使用示例:');
  console.log('');
  console.log('  $ node scripts/index.js get -d doccxxxxxxxxxxxxxx');
  console.log('  $ node scripts/index.js get -d doccxxxxxxxxxxxxxx -o output.md --format markdown');
  console.log('  $ node scripts/index.js create -f foldxxxxxxxxxxxxxx -t "我的文档"');
  console.log('  $ node scripts/index.js create -f foldxxxxxxxxxxxxxx -t "我的文档" --file content.txt');
  console.log('  $ node scripts/index.js import-file -f ./document.pdf --folder-token foldxxxxxxxxxxxxxx --type docx --ext txt');
  console.log('  $ node scripts/index.js list --folder-token foldxxxxxxxxxxxxxx');
  console.log('  $ node scripts/index.js delete -d doccxxxxxxxxxxxxxx --force');
  console.log('  $ node scripts/index.js update -d doccxxxxxxxxxxxxxx --file new-content.md');
  console.log('');
  console.log('环境变量配置 (.env 文件):');
  console.log('  FEISHU_APP_ID=cli_xxxxxxxxxx');
  console.log('  FEISHU_APP_SECRET=xxxxxxxxxx');
  console.log('');
  console.log('获取应用凭证:');
  console.log('  1. 访问 https://open.feishu.cn/app');
  console.log('  2. 创建企业自建应用');
  console.log('  3. 在"凭证与基础信息"中获取 App ID 和 App Secret');
  console.log('  4. 在"权限管理"中添加以下权限:');
  console.log('     - docx:document (查看、编辑、创建文档)');
  console.log('     - drive:drive (查看、删除云空间文件)');
  console.log('     - drive:file (上传文件)');
  console.log('     - drive:importTask (导入文件为文档)');
  console.log('     - auth:tenant (获取租户访问凭证)');
  console.log('');
});

program.parse();
