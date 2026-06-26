class ServiceRequestError extends Error {
  constructor(code, message, meta = null) {
    super(message);
    this.name = 'ServiceRequestError';
    this.code = code;
    this.meta = meta;
  }
}

function toTrimmedString(value) {
  if (value == null) {
    return '';
  }
  return String(value).trim();
}

function normalizeBaseUrl(baseUrl) {
  return toTrimmedString(baseUrl).replace(/\/+$/, '');
}

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function truncateText(value, maxLength = 600) {
  const text = toTrimmedString(value);
  if (!text) {
    return '';
  }
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength)}...`;
}

function resolveClientConfig(userConfig = {}) {
  const serviceBaseUrl = normalizeBaseUrl(
    userConfig.serviceBaseUrl || process.env.XIAOICE_VIDEO_SERVICE_BASE_URL
  );
  const internalToken = toTrimmedString(
    userConfig.internalToken || process.env.VIDEO_SERVICE_INTERNAL_TOKEN
  );
  const fetchFn = typeof userConfig.fetch === 'function' ? userConfig.fetch : global.fetch;

  return {
    serviceBaseUrl,
    internalToken,
    fetchFn,
  };
}

function validateClientConfig(config) {
  const errors = [];
  if (!config.serviceBaseUrl) {
    errors.push('XIAOICE_VIDEO_SERVICE_BASE_URL is required');
  }
  if (!config.internalToken) {
    errors.push('VIDEO_SERVICE_INTERNAL_TOKEN is required');
  }
  if (typeof config.fetchFn !== 'function') {
    errors.push('fetch API is not available in the current runtime');
  }
  return errors;
}

async function parseResponseBody(response, path) {
  let rawText = '';
  try {
    rawText = await response.text();
  } catch (error) {
    throw new ServiceRequestError(
      'service_response_read_error',
      'Failed to read video service response body',
      {
        path,
        status: response.status,
        reason: toTrimmedString(error.message),
      }
    );
  }

  if (!rawText) {
    return {
      rawText: '',
      json: null,
    };
  }

  try {
    return {
      rawText,
      json: JSON.parse(rawText),
    };
  } catch (error) {
    return {
      rawText,
      json: null,
    };
  }
}

async function requestVideoService(config, { method, path, body }) {
  const url = `${config.serviceBaseUrl}${path}`;
  let response;

  try {
    response = await config.fetchFn(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-Internal-Token': config.internalToken,
      },
      body: body == null ? undefined : JSON.stringify(body),
    });
  } catch (error) {
    throw new ServiceRequestError(
      'service_unreachable',
      'Failed to connect to video service',
      {
        path,
        method,
        reason: toTrimmedString(error.message),
      }
    );
  }

  const payload = await parseResponseBody(response, path);
  const responseJson = payload.json;

  if (!response.ok) {
    const serviceError = isObject(responseJson?.error)
      ? {
          code: toTrimmedString(responseJson.error.code),
          message: toTrimmedString(responseJson.error.message),
        }
      : null;

    const details = {
      path,
      method,
      status: response.status,
      statusText: toTrimmedString(response.statusText),
    };

    if (serviceError && (serviceError.code || serviceError.message)) {
      details.serviceError = serviceError;
    } else if (isObject(responseJson)) {
      details.response = responseJson;
    } else if (payload.rawText) {
      details.responseText = truncateText(payload.rawText);
    }

    throw new ServiceRequestError(
      'service_http_error',
      `Video service request failed with HTTP ${response.status}`,
      details
    );
  }

  if (!isObject(responseJson) || !isObject(responseJson.data)) {
    throw new ServiceRequestError(
      'service_invalid_response',
      'Video service response must be JSON with a data object',
      {
        path,
        method,
        status: response.status,
        responseText: truncateText(payload.rawText),
      }
    );
  }

  return responseJson.data;
}

function createVideoServiceClient(userConfig = {}) {
  const config = resolveClientConfig(userConfig);

  return {
    config,
    validateConfig() {
      return validateClientConfig(config);
    },
    async createTask(body) {
      return requestVideoService(config, {
        method: 'POST',
        path: '/v1/tasks',
        body,
      });
    },
    async getTask(taskId) {
      return requestVideoService(config, {
        method: 'GET',
        path: `/v1/tasks/${encodeURIComponent(toTrimmedString(taskId))}`,
      });
    },
  };
}

async function createTask(params, userConfig = {}) {
  return createVideoServiceClient(userConfig).createTask(params);
}

async function getTask(taskId, userConfig = {}) {
  return createVideoServiceClient(userConfig).getTask(taskId);
}

module.exports = {
  ServiceRequestError,
  createVideoServiceClient,
  createTask,
  getTask,
  requestVideoService,
};
