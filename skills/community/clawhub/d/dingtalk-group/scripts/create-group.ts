// 创建钉钉内部群会话
// 用法: ts-node scripts/create-group.ts --name "群名称" --owner <ownerUserId> --members <userId1,userId2,...> [options]
// 需要设置环境变量 DINGTALK_APP_KEY 和 DINGTALK_APP_SECRET
export {};

const https = require('https');
const { default: dingtalkOauth2_1_0, GetAccessTokenRequest } = require('@alicloud/dingtalk/oauth2_1_0');
const { Config } = require('@alicloud/openapi-client');

interface CreateGroupResult {
  success: boolean;
  chatid?: string;
  openConversationId?: string;
  conversationTag?: number;
  error?: {
    code: string;
    message: string;
  };
}

/**
 * 创建钉钉客户端配置
 */
function createConfig(): any {
  const config = new Config({});
  config.protocol = "https";
  config.regionId = "central";
  return config;
}

/**
 * 获取 Access Token
 */
async function getAccessToken(appKey: string, appSecret: string): Promise<string> {
  const config = createConfig();
  const client = new dingtalkOauth2_1_0(config);

  const request = new GetAccessTokenRequest({
    appKey: appKey,
    appSecret: appSecret,
  });

  try {
    const response = await client.getAccessToken(request);
    const accessToken = response.body?.accessToken;

    if (!accessToken) {
      throw new Error('获取 access_token 失败：响应中未包含 token');
    }

    return accessToken;
  } catch (err: any) {
    throw new Error(`获取 access_token 失败: ${err.message || err}`);
  }
}

/**
 * 通用钉钉旧版 API 调用函数
 */
async function dingtalkRequest(accessToken: string, method: string, path: string, body?: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'oapi.dingtalk.com',
      path: `${path}?access_token=${accessToken}`,
      method,
      headers: {
        'Content-Type': 'application/json',
      } as Record<string, string>,
    };
    const req = https.request(options, (res: any) => {
      let data = '';
      res.on('data', (chunk: string) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.errcode !== undefined && parsed.errcode !== 0) {
            reject({ code: parsed.errcode, message: parsed.errmsg });
          } else if (res.statusCode && res.statusCode >= 400) {
            reject(parsed);
          } else {
            resolve(parsed);
          }
        } catch {
          reject(new Error(`Invalid JSON response: ${data}`));
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * 解析命令行参数
 */
function parseArgs(args: string[]): Record<string, string> {
  const parsed: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && i + 1 < args.length && !args[i + 1].startsWith('--')) {
      parsed[args[i].slice(2)] = args[i + 1];
      i++;
    } else if (args[i] === '--debug') {
      parsed['debug'] = 'true';
    }
  }
  return parsed;
}

/**
 * 创建内部群会话
 */
async function createGroup(
  accessToken: string,
  params: {
    name: string;
    owner: string;
    useridlist: string[];
    showHistoryType?: number;
    searchable?: number;
    validationType?: number;
    mentionAllAuthority?: number;
    managementType?: number;
    chatBannedType?: number;
  },
  debug: boolean = false,
): Promise<void> {
  try {
    const body: any = {
      name: params.name,
      owner: params.owner,
      useridlist: params.useridlist,
    };

    if (params.showHistoryType !== undefined) body.showHistoryType = params.showHistoryType;
    if (params.searchable !== undefined) body.searchable = params.searchable;
    if (params.validationType !== undefined) body.validationType = params.validationType;
    if (params.mentionAllAuthority !== undefined) body.mentionAllAuthority = params.mentionAllAuthority;
    if (params.managementType !== undefined) body.managementType = params.managementType;
    if (params.chatBannedType !== undefined) body.chatBannedType = params.chatBannedType;

    if (debug) {
      console.error('\n=== 调试信息 ===');
      console.error('请求参数:', JSON.stringify(body, null, 2));
      console.error('==============\n');
    }

    const response = await dingtalkRequest(accessToken, 'POST', '/chat/create', body);

    if (debug) {
      console.error('\n=== 调试信息 ===');
      console.error('完整响应:', JSON.stringify(response, null, 2));
      console.error('==============\n');
    }

    const result: CreateGroupResult = {
      success: true,
      chatid: response.chatid,
      openConversationId: response.openConversationId,
      conversationTag: response.conversationTag,
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (err: any) {
    const result: CreateGroupResult = {
      success: false,
      error: {
        code: String(err.code || 'UNKNOWN_ERROR'),
        message: err.message || err.msg || JSON.stringify(err),
      },
    };
    console.error(JSON.stringify(result, null, 2));
    process.exit(1);
  }
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const parsed = parseArgs(args);
  const debug = parsed['debug'] === 'true';

  const appKey = process.env.DINGTALK_APP_KEY;
  const appSecret = process.env.DINGTALK_APP_SECRET;

  if (!appKey || !appSecret) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'MISSING_CREDENTIALS',
        message: '缺少钉钉应用凭证，请设置环境变量 DINGTALK_APP_KEY 和 DINGTALK_APP_SECRET',
        usage: 'export DINGTALK_APP_KEY=your-app-key && export DINGTALK_APP_SECRET=your-app-secret && ts-node scripts/create-group.ts --name "群名" --owner <userId> --members <userId1,userId2>',
      },
    }, null, 2));
    process.exit(1);
  }

  if (!parsed['name']) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'INVALID_ARGUMENTS',
        message: '缺少必填参数 --name（群名称，1~20 个字符）',
        usage: 'ts-node scripts/create-group.ts --name "群名" --owner <userId> --members <userId1,userId2> [--showHistoryType 1] [--searchable 0] [--validationType 0] [--mentionAllAuthority 0] [--managementType 0] [--chatBannedType 0] [--debug]',
      },
    }, null, 2));
    process.exit(1);
  }

  if (!parsed['owner']) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'INVALID_ARGUMENTS',
        message: '缺少必填参数 --owner（群主 userId，必须在 members 中）',
      },
    }, null, 2));
    process.exit(1);
  }

  if (!parsed['members']) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'INVALID_ARGUMENTS',
        message: '缺少必填参数 --members（群成员 userId，逗号分隔，每次最多 40 人）',
      },
    }, null, 2));
    process.exit(1);
  }

  const useridlist = parsed['members'].split(',').map(s => s.trim()).filter(Boolean);

  if (!useridlist.includes(parsed['owner'])) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'INVALID_ARGUMENTS',
        message: `群主 ${parsed['owner']} 必须在 members 列表中`,
      },
    }, null, 2));
    process.exit(1);
  }

  const params: any = {
    name: parsed['name'],
    owner: parsed['owner'],
    useridlist,
  };

  if (parsed['showHistoryType']) params.showHistoryType = parseInt(parsed['showHistoryType'], 10);
  if (parsed['searchable']) params.searchable = parseInt(parsed['searchable'], 10);
  if (parsed['validationType']) params.validationType = parseInt(parsed['validationType'], 10);
  if (parsed['mentionAllAuthority']) params.mentionAllAuthority = parseInt(parsed['mentionAllAuthority'], 10);
  if (parsed['managementType']) params.managementType = parseInt(parsed['managementType'], 10);
  if (parsed['chatBannedType']) params.chatBannedType = parseInt(parsed['chatBannedType'], 10);

  try {
    console.error('正在获取 access_token...');
    const accessToken = await getAccessToken(appKey, appSecret);
    console.error('access_token 获取成功，正在创建群...');

    await createGroup(accessToken, params, debug);
  } catch (err: any) {
    console.error(JSON.stringify({
      success: false,
      error: {
        code: 'AUTH_FAILED',
        message: err.message || '认证失败',
      },
    }, null, 2));
    process.exit(1);
  }
}

main();
