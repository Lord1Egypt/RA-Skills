const { cliError } = require('./errors');
const { getRuntimeConfig } = require('./config');

function buildEnvelope(type, data) {
  return {
    type,
    version: 'v1',
    msgId: `aqara-cli-${Date.now()}`,
    data,
  };
}

async function postAqara(type, data, options = {}) {
  const runtimeConfig = getRuntimeConfig();
  const requestEnvelope = buildEnvelope(type, data);

  let response;
  try {
    response = await fetch(runtimeConfig.endpointUrl, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${runtimeConfig.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestEnvelope),
    });
  } catch (error) {
    throw cliError('HTTP_ERROR', `failed to call Aqara endpoint for ${type}`, {
      endpointUrl: runtimeConfig.endpointUrl,
      cause: error.message,
    });
  }

  const responseText = await response.text();
  let responsePayload;
  try {
    responsePayload = responseText ? JSON.parse(responseText) : {};
  } catch (error) {
    throw cliError('HTTP_ERROR', `Aqara endpoint returned non-JSON response for ${type}`, {
      status: response.status,
      body: responseText,
      cause: error.message,
    });
  }

  if (!response.ok) {
    throw cliError('HTTP_ERROR', `Aqara endpoint returned HTTP ${response.status} for ${type}`, {
      status: response.status,
      response: responsePayload,
    });
  }

  if (responsePayload && typeof responsePayload === 'object' && responsePayload.code !== 0) {
    throw cliError('API_ERROR', `Aqara API returned code=${responsePayload.code} for ${type}`, {
      response: responsePayload,
    });
  }

  if (options.includeEnvelope) {
    return {
      request: requestEnvelope,
      response: responsePayload,
    };
  }

  return responsePayload;
}

module.exports = {
  buildEnvelope,
  postAqara,
};
