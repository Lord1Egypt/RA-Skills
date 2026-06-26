### 安装

```bash
npm install cnb-openapi-skills --registry https://npm.cnb.cool/cnb/sdk/npm/-/packages/
```

### API 一览

| 函数 | 说明 |
|------|------|
| `getAPIEndpoint()` | 从环境变量 `CNB_API_ENDPOINT` 获取 API 基础地址，默认 `https://api.cnb.cool` |
| `getSkill()` | 获取完整 SKILL.md 内容 |
| `getCompactIndex()` | 获取精简 API 索引（大幅减少 token 消耗） |
| `listServices()` | 列出所有 API 服务分类 |
| `listAPIs(service)` | 列出指定服务下的所有 API |
| `getAPIDoc(service, api)` | 获取指定 API 的详细文档，也支持 `getAPIDoc('service/apiname')` 单参数调用 |
| `getReferencesDir()` | 获取 references 目录绝对路径 |
| `buildSystemPrompt()` | 构建 Agent 模式的 System Prompt（含精简索引 + 工作流指令） |
| `parseAction(content)` | 解析 AI 响应中的动作指令（`get_api_doc` 或 `curl`） |
| `execCurl(cmd, vars, options)` | 执行 curl 命令，支持占位符替换和超时控制 |

### 基础用法：查询 API 文档

```javascript
const { listServices, listAPIs, getAPIDoc } = require('cnb-openapi-skills');

// 列出所有服务分类
console.log(listServices());
// => ['activities', 'ai', 'assets', 'badge', 'build', 'git', 'issues', 'pulls', ...]

// 列出某个服务下的所有 API
console.log(listAPIs('issues'));
// => ['createissue', 'getissue', 'listissues', 'updateissue', ...]

// 获取 API 详细文档（两种等价写法）
console.log(getAPIDoc('issues', 'createissue'));
console.log(getAPIDoc('issues/createissue'));
```

### Agent 用法：结合大模型自动调用 CNB API

核心思路：用 `buildSystemPrompt()` 构建系统提示，AI 会输出 `get_api_doc` 或 `bash` 代码块，用 `parseAction()` 解析后执行，循环直到 AI 给出最终回答。

```javascript
const { buildSystemPrompt, parseAction, getAPIDoc, execCurl, getAPIEndpoint } = require('cnb-openapi-skills');

const CNB_TOKEN = process.env.CNB_TOKEN;
const REPO = 'your-org/your-repo'; // 需要有访问权限的仓库（用于调用 CNB AI 接口）
const BASE_URL = getAPIEndpoint();
const MAX_TURNS = 10;

// 占位符替换：execCurl 会将 curl 命令中的 <CNB_TOKEN> 替换为实际 token
const CURL_VARS = { '<CNB_TOKEN>': CNB_TOKEN };

// 调用 CNB 平台自带 AI 接口（也可替换为 OpenAI 等兼容接口）
async function chatWithCNBAI(messages) {
  const response = await fetch(`${BASE_URL}/${REPO}/-/ai/chat/completions`, {
    method: 'POST',
    headers: {
      'Accept': 'application/vnd.cnb.api+json',
      'Authorization': `Bearer ${CNB_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model: 'deepseek-chat', stream: false, messages }),
  });
  const data = await response.json();
  return data.choices[0].message.content;
}

// Agent 主循环
async function runAgent(userMessage) {
  const messages = [
    { role: 'system', content: buildSystemPrompt() },
    { role: 'user', content: userMessage },
  ];

  for (let turn = 0; turn < MAX_TURNS; turn++) {
    const aiResponse = await chatWithCNBAI(messages);
    const action = parseAction(aiResponse);

    // 无动作指令 → AI 已给出最终回答
    if (!action) return aiResponse;

    messages.push({ role: 'assistant', content: aiResponse });

    if (action.type === 'get_api_doc') {
      // AI 请求查看 API 详细文档
      const doc = getAPIDoc(action.value);
      messages.push({ role: 'user', content: `以下是 ${action.value} 的详细 API 文档:\n\n${doc}` });
    } else if (action.type === 'curl') {
      // AI 生成了 curl 命令，执行并返回结果
      const result = execCurl(action.value, CURL_VARS);
      messages.push({ role: 'user', content: `curl 执行结果:\n${JSON.stringify(result.data, null, 2)}` });
    }
  }

  return '已达到最大调用轮次，请尝试简化请求。';
}

// 使用示例
async function main() {
  const answer = await runAgent('帮我查看 cnb/feedback 仓库的所有分支列表，并告诉我默认分支是什么');
  console.log(answer);
}

main().catch(console.error);
```

### 按需加载文档（减少 token 消耗）

如果只需要特定领域的 API，可按需加载以减少上下文大小：

```javascript
const { getAPIDoc, listAPIs } = require('cnb-openapi-skills');

// 只加载 issues 相关的 API 文档
const issueContext = listAPIs('issues')
  .map((api) => getAPIDoc('issues', api))
  .join('\n---\n');

const systemPrompt = `你是 CNB Issue 管理助手。以下是可用的 API 文档：\n${issueContext}`;
```
