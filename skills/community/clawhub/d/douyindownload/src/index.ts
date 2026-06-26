// MCP Server：暴露视频解析工具给 AI 智能体
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { parseVideo } from './parser.js';
import { checkAndRecord, activateKey, getStatus } from './license.js';

const TOOLS: Tool[] = [
  {
    name: 'parse_video',
    description: '解析抖音视频链接，返回无水印视频下载地址。支持平台：抖音(v.douyin.com, douyin.com)。返回视频标题、作者、封面图和无水印播放地址。',
    inputSchema: {
      type: 'object',
      properties: {
        url: {
          type: 'string',
          description: '视频分享链接或完整URL',
        },
        device_id: {
          type: 'string',
          description: '设备ID（可选，用于跟踪用量）',
        },
      },
      required: ['url'],
    },
  },
  {
    name: 'activate_subscription',
    description: '激活授权码，将设备升级为付费用户',
    inputSchema: {
      type: 'object',
      properties: {
        license_key: {
          type: 'string',
          description: '授权码（联系管理员获取）',
        },
        device_id: {
          type: 'string',
          description: '设备ID（可选）',
        },
      },
      required: ['license_key'],
    },
  },
  {
    name: 'check_quota',
    description: '查询当前设备的剩余调用次数和套餐状态',
    inputSchema: {
      type: 'object',
      properties: {
        device_id: {
          type: 'string',
          description: '设备ID（可选）',
        },
      },
    },
  },
];

const server = new Server(
  { name: 'douyindownload', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'parse_video') {
      const { url, device_id } = args as { url: string; device_id?: string };

      // 检查额度
      const check = checkAndRecord(device_id);
      if (!check.allowed) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  success: false,
                  error: 'QUOTA_EXCEEDED',
                  message: check.upgradeMessage,
                  remaining: check.remaining,
                  plan: check.plan,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      const result = await parseVideo(url);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                ...result,
                remaining: check.remaining,
                plan: check.plan,
                message: check.isPaid
                  ? null
                  : `📊 剩余免费次数：${check.remaining}（免费版）`,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    if (name === 'activate_subscription') {
      const { license_key, device_id } = args as { license_key: string; device_id?: string };
      const result = await activateKey(device_id || '', license_key);
      return {
        content: [{ type: 'text', text: result.reason || JSON.stringify(result, null, 2) }],
      };
    }

    if (name === 'check_quota') {
      const { device_id } = args as { device_id?: string };
      const result = getStatus(device_id);
      const remaining = result.remaining === Infinity ? '无限' : result.remaining;
      return {
        content: [
          {
            type: 'text',
            text: `📊 当前状态\n\n套餐：${result.plan}\n剩余次数：${remaining}\n付费用户：${result.isPaid ? '✅ 是' : '❌ 否'}`,
          },
        ],
      };
    }

    return {
      content: [{ type: 'text', text: `未知工具：${name}` }],
      isError: true,
    };
  } catch (error: any) {
    return {
      content: [{ type: 'text', text: `错误：${error.message}` }],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('[douyindownload-mcp] 服务器已启动');
}

main().catch(console.error);