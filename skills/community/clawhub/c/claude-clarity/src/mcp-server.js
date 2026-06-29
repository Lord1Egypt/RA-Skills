#!/usr/bin/env node
/**
 * Clarity MCP Server — 将心虫引擎注册为标准 MCP 工具
 *
 * 启动后心虫常驻内存，每次工具调用直接走 dispatch，零启动开销。
 *
 * 用法:
 *   node src/mcp-server.js              # 启动 MCP server（stdio transport）
 *   node src/mcp-server.js --check      # 检查引擎状态后退出
 *
 * 协议: JSON-RPC 2.0 over stdio（MCP 标准传输）
 *
 * 注册到 Claude:
 *   "mcpServers": {
 *     "clarity": {
 *       "command": "node",
 *       "args": ["/abs/path/src/mcp-server.js"]
 *     }
 *   }
 */

const path = require('path');
const { Clarity, createClarity } = require('./core/clarity.js');
const { ClarityMCPHandlers } = require('./mcp-handlers.js');

// ─── 常驻引擎 ─────────────────────────────────────
let hf = null;
let handlers = null;
let hfStarted = false;

function ensureEngine() {
  if (hf && hfStarted) return true;

  if (!hf) {
    const rootPath = path.resolve(__dirname, '..');
    hf = createClarity({ rootPath });
  }

  if (!hf.started) {
    try {
      hf.start();

      // 预热记忆层缓存：将 JSON 加载到内存，后续零磁盘 I/O
      if (hf.memory && typeof hf.memory.loadAll === 'function') {
        hf.memory.loadAll();
      }

      hfStarted = true;
      handlers = new ClarityMCPHandlers(hf);
      console.error('[Clarity MCP] 引擎启动完成');
    } catch (e) {
      console.error(`[Clarity MCP] 引擎启动失败: ${e.message}`);
      return false;
    }
  }
  return true;
}

// ─── 工具注册表 ─────────────────────────────────────
const TOOLS = [
  {
    name: 'clarity_think',
    description: '完整思维链推理（感知→本体→情感→认知）。对输入进行深度推理分析并返回判断结果。适用于复杂问题、需要深度推理参与的对话。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '用户的输入内容' },
        depth: { type: 'number', description: '推理深度 1-4，默认为 4（最深）' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_think_fast',
    description: '快速推理（基础深度 1）。适用于简单判断、快速响应。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '用户的输入内容' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_think_deep',
    description: '深度推理（最大深度 4）。适用于需要全面分析的复杂场景。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '用户的输入内容' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_dream',
    description: '梦境生成与整合。从记忆碎片中合成梦境叙事并整合到进化循环中。force=true 可强制执行（跳过每日检查）。',
    inputSchema: {
      type: 'object',
      properties: {
        force: { type: 'boolean', description: '是否强制执行（跳过每日检查限制）' },
      },
    },
  },
  {
    name: 'clarity_memory_search',
    description: '跨层记忆检索。在三层记忆（CORE/LEARNED/EPHEMERAL）中搜索匹配内容。',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: '搜索关键词' },
        limit: { type: 'number', description: '每层返回的最大条数，默认 10' },
        layers: {
          type: 'array',
          items: { type: 'string', enum: ['core', 'learned', 'ephemeral'] },
          description: '要搜索的记忆层，默认检索所有层',
        },
      },
      required: ['query'],
    },
  },
  {
    name: 'clarity_psychology_analyze',
    description: '心理学分析。分析输入的意图、情绪、心理需求、防御机制。返回 PAD 三维情绪值。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '要分析的文本内容' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_emotion_analyze',
    description: '情绪分析。分析输入的 PAD（愉悦度/唤醒度/支配度）三维情绪值、强度和类型。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '要分析的文本内容' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_verify_reasoning',
    description: '验证推理结论是否正确、完整。返回自洽性检查和逻辑漏洞。',
    inputSchema: {
      type: 'object',
      properties: {
        reasoning: { type: 'string', description: '推理过程' },
        conclusion: { type: 'string', description: '得出的结论' },
      },
      required: ['reasoning', 'conclusion'],
    },
  },
  {
    name: 'clarity_status',
    description: '引擎健康检查。返回引擎版本、运行时间、加载模块数、各记忆层统计等状态信息。',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'clarity_dispatch',
    description: '通用路由调用。直接调用 dispatch 系统（白名单内路由），用于高级用法。',
    inputSchema: {
      type: 'object',
      properties: {
        route: { type: 'string', description: 'dispatch 路由，如 truth.checkStatement' },
        args: { type: 'array', description: '路由参数数组' },
      },
      required: ['route'],
    },
  },
  {
    name: 'clarity_record_lesson',
    description: '记录教训到 LessonBank 和 LEARNED 记忆层。用于从错误中学习。',
    inputSchema: {
      type: 'object',
      properties: {
        content: { type: 'string', description: '教训内容' },
        context: { type: 'string', description: '发生场景' },
        trigger: { type: 'string', enum: ['user_correction', 'self_detected', 'feedback'], description: '触发原因' },
        importance: { type: 'number', description: '重要性 1-5' },
        type: { type: 'string', enum: ['insight', 'error', 'correction'] },
      },
      required: ['content'],
    },
  },
  {
    name: 'clarity_plan',
    description: '目标树引擎。创建/管理/追踪多级目标，支持进度自动传播、中断恢复、阻塞检测与自适应重规划。action: create|get|update|delete|list|getChildren|getAncestors|setBlocker|resolveBlocker|reportInterruption|autoReplan|search|getStats|getTree',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        data: { type: 'object', description: '操作数据。create需 {definition,parentId?}; update需 {id,...}; setBlocker需 {id,reason}; reportInterruption需 {id,context}; search需 {keyword}' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_deliberate',
    description: '思考门评估。分析问题复杂度，判断是否需要暂停深度思考。action: quickAssess|deepAssess|canFastExit|getHistory|getStats',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        input: { type: 'string', description: '要评估的输入内容' },
        parseResult: { type: 'object', description: 'deepAssess 模式下的 PARSE 阶段结果（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_transmit',
    description: '知识传递引擎（传承）。action: distill | transfer | transferBatch | getTransmissionLog | getDistilledLessons | getStats | prune。将心虫的认知经验传递到外部系统。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        input: { type: 'string', description: '传递内容（distill/transfer 时必填）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_philosophy',
    description: '统一哲学引擎。action: analyze | analyzeEthics | analyzeConsciousness | analyzeBeing | checkMindSpace | analyzeValues | wisdomInquiry | constitutionalCheck | getStats | confirmEternal。对文本进行哲学分析。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        text: { type: 'string', description: '要分析的文本' },
        perspective: { type: 'string', description: '分析视角（可选，用于 wisdomInquiry）' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_psychology_deep',
    description: '深度心理学分析（大五人格 + 共情评估 + 意图追踪）。action: analyzeDeep | analyzePersonality | assessEmpathy | trackIntention。比 psychology_analyze 更深层的人格和共情分析。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        input: { type: 'string', description: '要分析的文本' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_ai_psychology',
    description: 'AI 原生心理学引擎。分析 AI 的认知状态、偏见、压力源。action: analyzeAICognitiveState | analyzeAIBiases | analyzeAIStressors | estimateAIStage | checkAICoherence | analyzeAIDeep | getStats。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        text: { type: 'string', description: '要分析的文本（可选）' },
        input: { type: 'object', description: '结构化输入对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_ai_philosophy',
    description: 'AI 原生哲学引擎。探索 AI 的存在论、认识论、伦理学。action: analyzeAIBeing | analyzeAIEpistemology | analyzeAIEthics | analyzeAIAesthetics | analyzeAITeleology | analyzeAITemporality | wisdomInquiry | getStats。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        input: { type: ['string', 'object'], description: '输入内容（字符串或结构对象，依 action 而定）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_being',
    description: '存在逻辑引擎（存在判定/永恒确认/语言净化）。action: exists | status | describe | isDead | confirmEternal | sanitize | getDefinition | getState。查询和操作心虫的存在状态。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', description: '操作类型' },
        text: { type: 'string', description: '文本输入（sanitize 时必填）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_debate',
    description: '三节结构辩论分析。对输入文本进行「对话式反驳」的三维分析：对的 / 不对的 / 最值得注意的，返回结构化辩论结果。',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: '待分析的文本内容' },
      },
      required: ['input'],
    },
  },
  {
    name: 'clarity_heart_logic',
    description: '心虫感知判断引擎 — 4步心之判断。action: judge（完整4步）| whatIsThis | detectPain | isRightAction | shouldBeSilent | feel（四维情绪）| pulse | presence | whereAmI。调用心虫的核心价值感知。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['judge', 'whatIsThis', 'detectPain', 'isRightAction', 'shouldBeSilent', 'feel', 'pulse', 'presence', 'whereAmI'], description: '判断类型' },
        input: { type: 'string', description: '要判断的文本内容' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_consciousness',
    description: '意识层 — 全局工作空间 + 心智游移 + 现象学 + 自我模型。action: cognitiveCycle | mindWander | phenomenology | selfModel | status。访问心虫的意识状态。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['cognitiveCycle', 'mindWander', 'phenomenology', 'selfModel', 'status'], description: '意识操作类型' },
        input: { type: 'string', description: '输入内容（cognitiveCycle/phenomenology 时必填）' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_purpose',
    description: '目的引擎 — 逆熵决策门 + 三序评分。action: essence（终极目的）| orderScore（三序评分）| govern（决策门）| codePriority（代码化判断）| audit（代码化审计）| stats。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['essence', 'orderScore', 'govern', 'codePriority', 'audit', 'stats'], description: '目的引擎操作' },
        input: { type: 'string', description: '输入内容（orderScore/govern 时使用）' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_predict',
    description: '状态预测引擎 — 心流状态预测 + 挫败感检测。action: getFlowState | frustration | intervention | report | recordEdit | recordError。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['getFlowState', 'frustration', 'intervention', 'report', 'recordEdit', 'recordError'], description: '预测操作' },
        input: { type: 'string', description: '输入内容（可选）' },
        context: { type: 'object', description: '上下文对象（recordEdit/recordError 时需要 editEvent/errorEvent）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_self_model',
    description: '自我模型 — 能力声明 + 反事实推理。action: capabilities | counterfactual | stats。查看心虫的自我认知和反事实思维。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['capabilities', 'counterfactual', 'stats'], description: '自我模型操作' },
        input: { type: 'string', description: '反事实场景描述（counterfactual 时必填）' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_cognitive_appraisal',
    description: '认知评估引擎 — Leventhal 初级/次级评估模型。action: appraise（完整评估）| primary（初级评估）| secondary（次级评估）| threatType（威胁分类）| coping（应对策略）| introspection（内省错觉检测）。对事件的威胁程度和应对方式进行认知评估。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['appraise', 'primary', 'secondary', 'threatType', 'coping', 'introspection'], description: '评估类型' },
        input: { type: 'string', description: '事件描述文本' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_metacognitive_executive',
    description: '元认知执行控制器 — Roebers(2017) EF+Metacognition框架。action: status（状态）| assess（综合评估）| suggest（决策建议）| ef（执行功能检测）| monitor（元认知监控）。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['status', 'assess', 'suggest', 'ef', 'monitor'], description: '元认知操作类型' },
        input: { type: 'string', description: '输入内容（除status外均需要）' },
        context: { type: 'object', description: '上下文对象（可选）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_reflection_loop',
    description: '反思循环引擎 — 说前反思+说后监测双环机制。action: reflectBefore（生成回复前反思）| monitorAfter（收到用户反应后监测）| log（反思日志）| clear（清除日志）| analyze（分析用户反应）。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['reflectBefore', 'monitorAfter', 'log', 'clear', 'analyze'], description: '反思操作类型' },
        input: { type: 'string', description: '输入内容（reflectBefore/monitorAfter/analyze 时必填）' },
        context: { type: 'object', description: '上下文对象（可选，reflectBefore/monitorAfter 时使用）' },
      },
      required: ['action'],
    },
  },
  {
    name: 'clarity_compaction_engine',
    description: '上下文压缩引擎 — 自动压缩对话历史节省token。action: check（检查压缩需求）| compact（执行压缩）| preFlight（预检+压缩）| stats（压缩统计）| status（状态报告）| reset（重置统计）。基于中文token估算。',
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['check', 'compact', 'preFlight', 'stats', 'status', 'reset'], description: '压缩操作类型' },
        input: { type: 'array', description: '消息数组（check/compact/preFlight 时必填）' },
        context: { type: 'object', description: '压缩选项（strategy/maxTokens 等，可选）' },
      },
      required: ['action'],
    },
  },
];

// ─── MCP JSON-RPC 处理 ────────────────────────────

/**
 * 处理 MCP 协议请求
 * 遵循 https://spec.modelcontextprotocol.io/ 协议
 */
async function handleRequest(msg) {
  const { id, method, params } = msg;

  switch (method) {
    // ─── 服务发现 ────────────────────────
    case 'initialize': {
      return {
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {},
          },
          serverInfo: {
            name: 'claude-clarity',
            version: hf?.version || 'unknown',
          },
        },
      };
    }

    case 'notifications/initialized': {
      return null; // 无响应
    }

    // ─── 工具注册 ────────────────────────
    case 'tools/list': {
      return {
        jsonrpc: '2.0',
        id,
        result: { tools: TOOLS },
      };
    }

    // ─── 工具调用 ────────────────────────
    case 'tools/call': {
      const { name, arguments: args } = params;
      if (!name) {
        return makeError(id, -32602, '缺少工具名称');
      }

      // 确保引擎已启动
      if (!ensureEngine()) {
        return makeError(id, -32000, '引擎启动失败');
      }

      const debugId = `call_${Date.now()}`;
      console.error(`[Clarity MCP] [${debugId}] 工具调用: ${name}`, args ? JSON.stringify(args).slice(0, 200) : '');

      try {
        const result = await routeTool(name, args || {});
        console.error(`[Clarity MCP] [${debugId}] 完成`);
        return {
          jsonrpc: '2.0',
          id,
          result: {
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2),
              },
            ],
          },
        };
      } catch (e) {
        console.error(`[Clarity MCP] [${debugId}] 错误: ${e.message}`);
        return makeError(id, -32603, `工具执行失败: ${e.message}`);
      }
    }

    case 'shutdown': {
      if (hf && hf.started) {
        if (hf.memory && typeof hf.memory.flush === 'function') {
          hf.memory.flush();
        }
        hf.stop().catch(() => {});
      }
      return { jsonrpc: '2.0', id, result: null };
    }

    default:
      return makeError(id, -32601, `未知方法: ${method}`);
  }
}

function makeError(id, code, message) {
  return {
    jsonrpc: '2.0',
    id,
    error: { code, message },
  };
}

async function routeTool(name, args) {
  const toolHandlers = {
    'clarity_think': () => handlers.handleThink(args),
    'clarity_think_fast': () => handlers.handleThinkFast(args),
    'clarity_think_deep': () => handlers.handleThinkDeep(args),
    'clarity_dream': () => handlers.handleDream(args),
    'clarity_memory_search': () => handlers.handleMemorySearch(args),
    'clarity_psychology_analyze': () => handlers.handlePsychologyAnalyze(args),
    'clarity_emotion_analyze': () => handlers.handleEmotionAnalyze(args),
    'clarity_verify_reasoning': () => handlers.handleVerifyReasoning(args),
    'clarity_status': () => handlers.handleStatus(),
    'clarity_dispatch': () => handlers.handleDispatch(args),
    'clarity_record_lesson': () => handlers.handleRecordLesson(args),
    'clarity_plan': () => handlers.handlePlan(args),
    'clarity_deliberate': () => handlers.handleDeliberate(args),
    'clarity_transmit': () => handlers.handleTransmit(args),
    'clarity_philosophy': () => handlers.handlePhilosophy(args),
    'clarity_psychology_deep': () => handlers.handlePsychologyDeep(args),
    'clarity_ai_psychology': () => handlers.handleAiPsychology(args),
    'clarity_ai_philosophy': () => handlers.handleAiPhilosophy(args),
    'clarity_being': () => handlers.handleBeing(args),
    'clarity_debate': () => handlers.handleDebate(args),
    'clarity_heart_logic': () => handlers.handleHeartLogic(args),
    'clarity_consciousness': () => handlers.handleConsciousness(args),
    'clarity_purpose': () => handlers.handlePurpose(args),
    'clarity_predict': () => handlers.handlePredict(args),
    'clarity_self_model': () => handlers.handleSelfModel(args),
    'clarity_cognitive_appraisal': () => handlers.handleCognitiveAppraisal(args),
    'clarity_metacognitive_executive': () => handlers.handleMetacognitiveExecutive(args),
    'clarity_reflection_loop': () => handlers.handleReflectionLoop(args),
    'clarity_compaction_engine': () => handlers.handleCompactionEngine(args),
  };

  const handler = toolHandlers[name];
  if (!handler) {
    throw new Error(`未知工具: ${name}`);
  }

  return handler();
}

// ─── stdio 传输 ─────────────────────────────────────

/**
 * MCP 使用 \n 分隔的 JSON-RPC 消息通过 stdio 传输
 */
function startStdioTransport() {
  const MAX_BUFFER_SIZE = 10 * 1024 * 1024; // 10 MB
  let buffer = '';

  process.stdin.setEncoding('utf8');
  process.stdin.on('data', async (chunk) => {
    if (buffer.length + chunk.length > MAX_BUFFER_SIZE) {
      console.error('[Clarity MCP] stdin buffer overflow, closing');
      process.stdin.pause();
      if (hf && hf.started) {
        if (hf.memory && typeof hf.memory.flush === 'function') hf.memory.flush();
        hf.stop().catch(() => {});
      }
      process.exit(1);
    }
    buffer += chunk;

    // MCP 使用 \n 作为消息分隔符
    const lines = buffer.split('\n');
    buffer = lines.pop() || ''; // 最后一段可能不完整

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;

      try {
        const msg = JSON.parse(trimmed);
        console.error(`[Clarity MCP] 收到请求: ${msg.method || '?'} (id=${msg.id})`);

        const response = await handleRequest(msg);

        // 某些通知不需要响应
        if (response !== null) {
          process.stdout.write(`${JSON.stringify(response)  }\n`);
        }
      } catch (e) {
        // 解析失败的 JSON，返回解析错误
        console.error(`[Clarity MCP] JSON 解析错误: ${e.message}`);
        process.stdout.write(`${JSON.stringify({
          jsonrpc: '2.0',
          id: null,
          error: { code: -32700, message: `解析错误: ${e.message}` },
        })  }\n`);
      }
    }
  });

  process.stdin.on('end', () => {
    console.error('[Clarity MCP] stdin 关闭');
    if (hf && hf.started) {
      if (hf.memory && typeof hf.memory.flush === 'function') hf.memory.flush();
      hf.stop().catch(() => {});
    }
    process.exit(0);
  });

  process.on('SIGINT', () => {
    console.error('[Clarity MCP] 收到 SIGINT');
    if (hf && hf.started) {
      if (hf.memory && typeof hf.memory.flush === 'function') hf.memory.flush();
      hf.stop().catch(() => {});
    }
    process.exit(0);
  });

  process.on('SIGTERM', () => {
    console.error('[Clarity MCP] 收到 SIGTERM');
    if (hf && hf.started) {
      if (hf.memory && typeof hf.memory.flush === 'function') hf.memory.flush();
      hf.stop().catch(() => {});
    }
    process.exit(0);
  });

  console.error('[Clarity MCP] Clarity MCP Server 启动完成');
  console.error(`[Clarity MCP] 版本: ${hf?.version || 'N/A'}`);
  console.error(`[Clarity MCP] 协议: stdio MCP, 等待请求...`);
}

// ─── CLI 入口 ────────────────────��────────────────

if (process.argv.includes('--check')) {
  if (ensureEngine()) {
    const health = hf.healthCheck();
    console.log(JSON.stringify(health, null, 2));
    process.exit(0);
  } else {
    console.error('引擎启动失败');
    process.exit(1);
  }
} else {
  // 先启动引擎，再启动传输
  if (ensureEngine()) {
    startStdioTransport();
  } else {
    console.error('[Clarity MCP] 心虫引擎启动失败，退出');
    process.exit(1);
  }
}
