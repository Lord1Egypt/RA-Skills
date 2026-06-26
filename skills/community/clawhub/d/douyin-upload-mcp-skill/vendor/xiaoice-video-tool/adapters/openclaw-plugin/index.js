const { createTask, getTask } = require('./lib/video-service-client');

const PLUGIN_ID = 'one-click-video';
const TOOL_NAME = 'xiaoice_video_produce';

const TOOL_PARAMETERS = {
  type: 'object',
  additionalProperties: false,
  properties: {
    action: {
      type: 'string',
      enum: ['create', 'get'],
      description: 'create to submit a task, get to query task status',
    },
    topic: {
      type: 'string',
      description: 'Topic text for create action',
    },
    taskId: {
      type: 'string',
      description: 'Task ID for get action',
    },
    sessionId: {
      type: 'string',
      description: 'Optional session ID',
    },
    traceId: {
      type: 'string',
      description: 'Optional trace ID',
    },
    vhBizId: {
      type: 'string',
      description: 'Business ID forwarded to video-task-service',
    },
    title: {
      type: 'string',
      description: 'Optional title',
    },
    content: {
      type: 'string',
      description: 'Optional content',
    },
    materialList: {
      type: 'array',
      description: 'Optional material list',
    },
    ttsConf: {
      type: 'object',
      additionalProperties: true,
      description: 'Optional tts config object',
    },
    aigcWatermark: {
      type: 'boolean',
      description: 'Optional watermark toggle',
    },
  },
  required: ['action'],
};

function toTrimmedString(value) {
  if (value == null) {
    return '';
  }
  return String(value).trim();
}

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function toPositiveInt(value) {
  if (value == null || value === '') {
    return undefined;
  }
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return undefined;
  }
  return parsed;
}

function toOpenClawResult(payload, isError) {
  let text;
  if (typeof payload === 'string') {
    text = payload;
  } else {
    try {
      text = JSON.stringify(payload, null, 2);
    } catch (error) {
      text = toTrimmedString(error?.message) || 'Failed to serialize tool response';
    }
  }

  return {
    content: [
      {
        type: 'text',
        text,
      },
    ],
    isError: Boolean(isError),
  };
}

function toErrorResult(code, message, details) {
  const errorPayload = {
    ok: false,
    error: {
      code: toTrimmedString(code) || 'tool_error',
      message: toTrimmedString(message) || 'Tool execution failed',
    },
  };

  if (isObject(details)) {
    errorPayload.error.details = details;
  }

  return toOpenClawResult(errorPayload, true);
}

function toSuccessResult(action, data) {
  return toOpenClawResult(
    {
      ok: true,
      action,
      data,
    },
    false
  );
}

function resolveRuntimeConfig(api) {
  const pluginConfig = api?.config?.plugins?.entries?.[PLUGIN_ID]?.config;
  const rawConfig = isObject(pluginConfig) ? pluginConfig : {};

  return {
    serviceBaseUrl: toTrimmedString(rawConfig.serviceBaseUrl).replace(/\/+$/, ''),
    internalToken: toTrimmedString(rawConfig.internalToken),
    requestTimeoutMs: toPositiveInt(rawConfig.requestTimeoutMs),
  };
}

function validateRuntimeConfig(config) {
  const missingFields = [];
  if (!config.serviceBaseUrl) {
    missingFields.push('serviceBaseUrl');
  }
  if (!config.internalToken) {
    missingFields.push('internalToken');
  }

  if (missingFields.length === 0) {
    return null;
  }

  return toErrorResult(
    'config_error',
    'one-click-video plugin is not fully configured',
    { missingFields }
  );
}

function normalizeOptionalString(value, fieldName) {
  if (value == null) {
    return '';
  }
  const normalized = toTrimmedString(value);
  if (!normalized) {
    throw new Error(`${fieldName} must be a non-empty string when provided`);
  }
  return normalized;
}

function validateArguments(rawArguments) {
  if (!isObject(rawArguments)) {
    throw new Error('params must be an object');
  }

  if (Object.prototype.hasOwnProperty.call(rawArguments, 'vhbizmode')) {
    throw new Error('vhbizmode is not supported; use vhBizId');
  }
  if (Object.prototype.hasOwnProperty.call(rawArguments, 'prompt')) {
    throw new Error('prompt is deprecated; use topic');
  }
  if (Object.prototype.hasOwnProperty.call(rawArguments, 'options')) {
    throw new Error('options is deprecated; use top-level create fields');
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

  const sessionId = normalizeOptionalString(rawArguments.sessionId, 'sessionId');
  const traceId = normalizeOptionalString(rawArguments.traceId, 'traceId');
  const topic = normalizeOptionalString(rawArguments.topic, 'topic');
  const vhBizId = normalizeOptionalString(rawArguments.vhBizId, 'vhBizId');
  const title = rawArguments.title == null ? undefined : normalizeOptionalString(rawArguments.title, 'title');
  const content = rawArguments.content == null ? undefined : normalizeOptionalString(rawArguments.content, 'content');

  if (action === 'create' && !topic) {
    throw new Error('topic is required for action=create');
  }
  if (action === 'create' && !vhBizId) {
    throw new Error('vhBizId is required for action=create');
  }

  let materialList;
  if (rawArguments.materialList != null) {
    if (!Array.isArray(rawArguments.materialList)) {
      throw new Error('materialList must be an array when provided');
    }
    materialList = rawArguments.materialList;
  }

  let ttsConf;
  if (rawArguments.ttsConf != null) {
    if (!isObject(rawArguments.ttsConf)) {
      throw new Error('ttsConf must be an object when provided');
    }
    ttsConf = rawArguments.ttsConf;
  }

  let aigcWatermark;
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

async function executeCreate(input, runtimeConfig) {
  const params = {
    topic: input.topic,
    vhBizId: input.vhBizId,
  };

  if (input.sessionId) {
    params.sessionId = input.sessionId;
  }
  if (input.traceId) {
    params.traceId = input.traceId;
  }
  if (input.title) {
    params.title = input.title;
  }
  if (input.content) {
    params.content = input.content;
  }
  if (input.materialList != null) {
    params.materialList = input.materialList;
  }
  if (input.ttsConf != null) {
    params.ttsConf = input.ttsConf;
  }
  if (input.aigcWatermark != null) {
    params.aigcWatermark = input.aigcWatermark;
  }

  return createTask(params, runtimeConfig);
}

async function executeGet(input, runtimeConfig) {
  return getTask(input.taskId, runtimeConfig);
}

function register(api) {
  if (!api || typeof api.registerTool !== 'function') {
    throw new Error('one-click-video plugin requires api.registerTool');
  }

  const logger = api.logger || console;

  api.registerTool({
    name: TOOL_NAME,
    description: 'Create and query XiaoIce video generation tasks via video-task-service.',
    parameters: TOOL_PARAMETERS,
    async execute(callIdOrParams, maybeParams) {
      const rawArguments = arguments.length >= 2 ? maybeParams : callIdOrParams;
      let input;
      try {
        input = validateArguments(rawArguments);
      } catch (error) {
        return toErrorResult('validation_error', error?.message);
      }

      const runtimeConfig = resolveRuntimeConfig(api);
      const configErrorResult = validateRuntimeConfig(runtimeConfig);
      if (configErrorResult) {
        return configErrorResult;
      }

      try {
        const data =
          input.action === 'create'
            ? await executeCreate(input, runtimeConfig)
            : await executeGet(input, runtimeConfig);

        return toSuccessResult(input.action, data);
      } catch (error) {
        logger.error?.(`[${PLUGIN_ID}] xiaoice_video_produce failed`, error);
        const details = isObject(error?.meta) ? error.meta : undefined;
        return toErrorResult(error?.code || 'upstream_error', error?.message, details);
      }
    },
  });

  logger.info?.(`[${PLUGIN_ID}] plugin registered`);
}

module.exports = register;
module.exports.default = register;
module.exports.PLUGIN_ID = PLUGIN_ID;
module.exports.TOOL_NAME = TOOL_NAME;
