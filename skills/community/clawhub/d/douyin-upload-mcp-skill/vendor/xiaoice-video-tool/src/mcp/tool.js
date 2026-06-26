const { createVideoServiceClient, ServiceRequestError } = require('../shared/video-service-client');

const TOOL_NAME = 'xiaoice_video_produce';

const TOOL_DEFINITION = {
  name: TOOL_NAME,
  description: 'Create or query XiaoIce video generation tasks via local video-task-service.',
  inputSchema: {
    type: 'object',
    additionalProperties: false,
    properties: {
      action: {
        type: 'string',
        enum: ['create', 'get'],
      },
      topic: {
        type: 'string',
      },
      taskId: {
        type: 'string',
      },
      sessionId: {
        type: 'string',
      },
      traceId: {
        type: 'string',
      },
      vhBizId: {
        type: 'string',
      },
      title: {
        type: 'string',
      },
      content: {
        type: 'string',
      },
      materialList: {
        type: 'array',
      },
      ttsConf: {
        type: 'object',
        additionalProperties: true,
      },
      aigcWatermark: {
        type: 'boolean',
      },
    },
    required: ['action'],
  },
};

function toTrimmedString(value) {
  if (value == null) {
    return '';
  }
  return String(value).trim();
}

function inferAction(rawArguments) {
  if (!rawArguments || typeof rawArguments !== 'object' || Array.isArray(rawArguments)) {
    return 'unknown';
  }
  const action = toTrimmedString(rawArguments.action);
  return action || 'unknown';
}

function hasOwn(object, key) {
  return Object.prototype.hasOwnProperty.call(object, key);
}

function buildToolError(action, code, message, details = null) {
  const error = {
    code: toTrimmedString(code) || 'tool_error',
    message: toTrimmedString(message) || 'Tool execution failed',
  };

  if (details && typeof details === 'object' && !Array.isArray(details)) {
    error.details = details;
  }

  return {
    ok: false,
    action: action || 'unknown',
    error,
  };
}

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function validateToolArguments(rawArguments) {
  if (!isObject(rawArguments)) {
    throw new Error('tool arguments must be an object');
  }

  const action = toTrimmedString(rawArguments.action);
  if (!action) {
    throw new Error('action is required');
  }
  if (action !== 'create' && action !== 'get') {
    throw new Error('action must be one of: create, get');
  }

  const taskId = toTrimmedString(rawArguments.taskId);
  if (action === 'get' && !taskId) {
    throw new Error('taskId is required for action=get');
  }

  if (hasOwn(rawArguments, 'vhbizmode')) {
    throw new Error('vhbizmode is no longer supported; use vhBizId');
  }
  if (hasOwn(rawArguments, 'prompt')) {
    throw new Error('prompt is deprecated; use topic');
  }
  if (hasOwn(rawArguments, 'options')) {
    throw new Error('options is deprecated; use top-level create fields');
  }

  const sessionId = rawArguments.sessionId == null ? '' : toTrimmedString(rawArguments.sessionId);
  const traceId = rawArguments.traceId == null ? '' : toTrimmedString(rawArguments.traceId);
  const vhBizId = rawArguments.vhBizId == null ? '' : toTrimmedString(rawArguments.vhBizId);
  const topic = rawArguments.topic == null ? '' : toTrimmedString(rawArguments.topic);
  const title = rawArguments.title == null ? undefined : toTrimmedString(rawArguments.title);
  const content = rawArguments.content == null ? undefined : toTrimmedString(rawArguments.content);

  if (rawArguments.sessionId != null && !sessionId) {
    throw new Error('sessionId must be a non-empty string when provided');
  }
  if (rawArguments.traceId != null && !traceId) {
    throw new Error('traceId must be a non-empty string when provided');
  }
  if (rawArguments.topic != null && !topic) {
    throw new Error('topic must be a non-empty string when provided');
  }
  if (rawArguments.vhBizId != null && !vhBizId) {
    throw new Error('vhBizId must be a non-empty string when provided');
  }
  if (rawArguments.title != null && !title) {
    throw new Error('title must be a non-empty string when provided');
  }
  if (rawArguments.content != null && !content) {
    throw new Error('content must be a non-empty string when provided');
  }

  if (action === 'create' && !topic) {
    throw new Error('topic is required for action=create');
  }
  if (action === 'create' && !vhBizId) {
    throw new Error('vhBizId is required for action=create');
  }

  let materialList = undefined;
  if (rawArguments.materialList != null) {
    if (!Array.isArray(rawArguments.materialList)) {
      throw new Error('materialList must be an array when provided');
    }
    materialList = rawArguments.materialList;
  }

  let ttsConf = undefined;
  if (rawArguments.ttsConf != null) {
    if (!isObject(rawArguments.ttsConf)) {
      throw new Error('ttsConf must be an object when provided');
    }
    ttsConf = rawArguments.ttsConf;
  }

  let aigcWatermark = undefined;
  if (rawArguments.aigcWatermark != null) {
    if (typeof rawArguments.aigcWatermark !== 'boolean') {
      throw new Error('aigcWatermark must be a boolean when provided');
    }
    aigcWatermark = rawArguments.aigcWatermark;
  }

  return {
    action,
    topic,
    taskId,
    sessionId,
    traceId,
    vhBizId,
    title,
    content,
    materialList,
    ttsConf,
    aigcWatermark,
  };
}

function toNullableNumber(value) {
  if (value == null || value === '') {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function normalizeTaskRecord(record) {
  return {
    taskId: toTrimmedString(record.taskId),
    providerTaskId: toTrimmedString(record.providerTaskId),
    status: toTrimmedString(record.status),
    videoUrl: toTrimmedString(record.videoUrl),
    errorMessage: toTrimmedString(record.errorMessage),
    traceId: toTrimmedString(record.traceId),
    sessionId: toTrimmedString(record.sessionId),
    createdAt: toNullableNumber(record.createdAt),
    updatedAt: toNullableNumber(record.updatedAt),
    finishedAt: toNullableNumber(record.finishedAt),
  };
}

async function executeCreate(serviceClient, input) {
  const requestBody = {
    topic: input.topic,
    vhBizId: input.vhBizId,
  };

  if (input.sessionId) {
    requestBody.sessionId = input.sessionId;
  }
  if (input.traceId) {
    requestBody.traceId = input.traceId;
  }
  if (input.title) {
    requestBody.title = input.title;
  }
  if (input.content) {
    requestBody.content = input.content;
  }
  if (input.materialList != null) {
    requestBody.materialList = input.materialList;
  }
  if (input.ttsConf != null) {
    requestBody.ttsConf = input.ttsConf;
  }
  if (input.aigcWatermark != null) {
    requestBody.aigcWatermark = input.aigcWatermark;
  }

  const data = await serviceClient.createTask(requestBody);

  const task = normalizeTaskRecord({
    taskId: data.taskId,
    status: data.status || 'submitted',
    providerTaskId: data.providerTaskId || '',
    videoUrl: data.videoUrl || '',
    errorMessage: data.errorMessage || '',
    sessionId: data.sessionId || input.sessionId || '',
    traceId: data.traceId || input.traceId || '',
    createdAt: data.createdAt ?? null,
    updatedAt: data.updatedAt ?? null,
    finishedAt: data.finishedAt ?? null,
  });

  if (!task.taskId) {
    throw new ServiceRequestError(
      'service_invalid_response',
      'Video service create response is missing taskId',
      {
        path: '/v1/tasks',
        method: 'POST',
      }
    );
  }

  return {
    ok: true,
    action: 'create',
    task,
  };
}

async function executeGet(serviceClient, input) {
  const encodedTaskId = encodeURIComponent(input.taskId);
  const data = await serviceClient.getTask(input.taskId);

  const task = normalizeTaskRecord({
    ...data,
    taskId: data.taskId || input.taskId,
  });

  if (!task.taskId) {
    throw new ServiceRequestError(
      'service_invalid_response',
      'Video service get response is missing taskId',
      {
        path: `/v1/tasks/${encodedTaskId}`,
        method: 'GET',
      }
    );
  }

  return {
    ok: true,
    action: 'get',
    task,
  };
}

function createToolHandler(userConfig = {}) {
  const serviceClient = createVideoServiceClient(userConfig);

  return {
    definition: TOOL_DEFINITION,
    async execute(rawArguments) {
      const inferredAction = inferAction(rawArguments);
      let input;

      try {
        input = validateToolArguments(rawArguments);
      } catch (error) {
        return buildToolError(
          inferredAction,
          'validation_error',
          toTrimmedString(error.message) || 'Invalid tool arguments'
        );
      }

      const configErrors = serviceClient.validateConfig();

      if (configErrors.length > 0) {
        return buildToolError(input.action, 'config_error', 'MCP server is not fully configured', {
          fields: configErrors,
        });
      }

      try {
        if (input.action === 'create') {
          return await executeCreate(serviceClient, input);
        }
        return await executeGet(serviceClient, input);
      } catch (error) {
        if (error instanceof ServiceRequestError) {
          return buildToolError(input.action, error.code, error.message, error.meta || undefined);
        }

        return buildToolError(
          input.action,
          'internal_error',
          toTrimmedString(error?.message) || 'Unexpected MCP tool error'
        );
      }
    },
  };
}

function normalizeMcpResultPayload(payload) {
  if (isObject(payload)) {
    return payload;
  }
  return buildToolError('unknown', 'internal_error', 'Tool execution returned an invalid payload');
}

function toMcpToolResult(payload) {
  const normalized = normalizeMcpResultPayload(payload);
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(normalized, null, 2),
      },
    ],
    isError: normalized.ok === false,
    structuredContent: normalized,
  };
}

async function executeXiaoiceVideoProduce(rawArguments, runtimeConfig = {}) {
  const handler = createToolHandler(runtimeConfig);
  const payload = await handler.execute(rawArguments);
  return toMcpToolResult(payload);
}

function createXiaoiceVideoProduceTool(runtimeConfig = {}) {
  const handler = createToolHandler(runtimeConfig);
  return {
    name: TOOL_NAME,
    description: TOOL_DEFINITION.description,
    inputSchema: TOOL_DEFINITION.inputSchema,
    async execute(callIdOrArguments, maybeArguments) {
      const rawArguments = arguments.length >= 2 ? maybeArguments : callIdOrArguments;
      const payload = await handler.execute(rawArguments);
      return toMcpToolResult(payload);
    },
  };
}

module.exports = {
  TOOL_NAME,
  TOOL_DEFINITION,
  createToolHandler,
  createXiaoiceVideoProduceTool,
  executeXiaoiceVideoProduce,
  toMcpToolResult,
};
