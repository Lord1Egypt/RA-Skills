const fs = require('fs');
const path = require('path');

const { cliError } = require('./errors');
const { getRuntimeConfig } = require('./config');
const { postAqara } = require('./http');

function toBoolean(value) {
  if (typeof value === 'boolean') {
    return value;
  }
  if (typeof value === 'number') {
    return value !== 0;
  }
  if (typeof value === 'string') {
    const lowerCaseValue = value.toLowerCase();
    if (['true', '1', 'yes', 'on', 'online'].includes(lowerCaseValue)) {
      return true;
    }
    if (['false', '0', 'no', 'off', 'offline'].includes(lowerCaseValue)) {
      return false;
    }
  }
  return undefined;
}

function getDeviceName(deviceItem) {
  return deviceItem.deviceName || deviceItem.name || deviceItem.nickName || deviceItem.deviceId || 'unknown-device';
}

function getSpaceInfo(deviceItem) {
  const spaceItem = deviceItem.space && typeof deviceItem.space === 'object' ? deviceItem.space : {};
  return {
    spaceId: spaceItem.spaceId || spaceItem.id || deviceItem.spaceId || null,
    spaceName: spaceItem.name || deviceItem.spaceName || null,
  };
}

function getDeviceOnline(deviceItem) {
  const possibleOnlineValues = [
    deviceItem.online,
    deviceItem.available,
    deviceItem.reachable,
  ];

  for (const possibleOnlineValue of possibleOnlineValues) {
    const normalizedOnline = toBoolean(possibleOnlineValue);
    if (normalizedOnline !== undefined) {
      return normalizedOnline;
    }
  }
  return null;
}

function flattenTraits(deviceItem) {
  const flattenedTraits = [];
  const endpointList = Array.isArray(deviceItem.endpoints) ? deviceItem.endpoints : [];

  endpointList.forEach((endpointItem) => {
    const endpointId = Number(endpointItem.endpointId);
    const functionList = Array.isArray(endpointItem.functions)
      ? endpointItem.functions
      : Array.isArray(endpointItem.functionList)
        ? endpointItem.functionList
        : [];

    functionList.forEach((functionItem) => {
      const traitList = Array.isArray(functionItem.traits)
        ? functionItem.traits
        : Array.isArray(functionItem.properties)
          ? functionItem.properties
          : [];

      traitList.forEach((traitItem) => {
        flattenedTraits.push({
          endpointId: Number.isFinite(endpointId) ? endpointId : endpointItem.endpointId,
          functionCode: functionItem.functionCode || functionItem.code || functionItem.functionName || '',
          functionName: functionItem.functionName || '',
          traitCode: traitItem.traitCode || traitItem.code || '',
          traitName: traitItem.traitName || traitItem.name || '',
          value: traitItem.value,
          raw: traitItem,
        });
      });
    });
  });

  return flattenedTraits;
}

function normalizeDevice(deviceItem) {
  const { spaceId, spaceName } = getSpaceInfo(deviceItem);
  const flattenedTraits = flattenTraits(deviceItem);

  return {
    deviceId: deviceItem.deviceId,
    deviceName: getDeviceName(deviceItem),
    spaceId,
    spaceName,
    deviceTypesList: Array.isArray(deviceItem.deviceTypesList) ? deviceItem.deviceTypesList : [],
    online: getDeviceOnline(deviceItem),
    endpointCount: Array.isArray(deviceItem.endpoints) ? deviceItem.endpoints.length : 0,
    traitCount: flattenedTraits.length,
    traits: flattenedTraits,
    raw: deviceItem,
  };
}

async function refreshDevicesCache(options = {}) {
  const runtimeConfig = getRuntimeConfig();
  const includeEnvelope = Boolean(options.includeEnvelope);
  const aqaraResponse = await postAqara('GetAllDevicesWithSpaceRequest', null, {
    includeEnvelope,
  });

  const responsePayload = includeEnvelope ? aqaraResponse.response : aqaraResponse;
  const responseData = responsePayload?.data;

  if (!Array.isArray(responseData)) {
    throw cliError('CACHE_ERROR', 'GetAllDevicesWithSpaceRequest.data must be a JSON array', {
      actualType: Array.isArray(responseData) ? 'array' : typeof responseData,
      response: responsePayload,
    });
  }

  fs.mkdirSync(path.dirname(runtimeConfig.cachePath), { recursive: true });
  const tempCachePath = path.join(
    path.dirname(runtimeConfig.cachePath),
    `devices.${Date.now()}.tmp.json`,
  );

  try {
    fs.writeFileSync(
      tempCachePath,
      `${JSON.stringify(responseData, null, 2)}\n`,
      'utf8',
    );
    if (fs.existsSync(runtimeConfig.cachePath)) {
      fs.unlinkSync(runtimeConfig.cachePath);
    }
    fs.renameSync(tempCachePath, runtimeConfig.cachePath);
  } catch (error) {
    if (fs.existsSync(tempCachePath)) {
      fs.unlinkSync(tempCachePath);
    }
    throw cliError('CACHE_ERROR', 'failed to write device cache file', {
      path: runtimeConfig.cachePath,
      cause: error.message,
    });
  }

  return {
    deviceCount: responseData.length,
    path: runtimeConfig.cachePath,
    ...(includeEnvelope ? aqaraResponse : {}),
  };
}

async function readDevicesCache(options = {}) {
  const { refreshIfMissing = false } = options;
  const runtimeConfig = getRuntimeConfig({ allowMissing: refreshIfMissing ? false : true });

  if (!fs.existsSync(runtimeConfig.cachePath)) {
    if (refreshIfMissing) {
      await refreshDevicesCache();
    } else {
      throw cliError('CACHE_ERROR', 'device cache file does not exist', {
        path: runtimeConfig.cachePath,
        help: 'Run `aqara devices cache refresh` first.',
      });
    }
  }

  let rawCacheText = '';
  try {
    rawCacheText = fs.readFileSync(runtimeConfig.cachePath, 'utf8');
  } catch (error) {
    throw cliError('CACHE_ERROR', 'failed to read device cache', {
      path: runtimeConfig.cachePath,
      cause: error.message,
    });
  }

  let parsedCache = [];
  try {
    parsedCache = JSON.parse(rawCacheText);
  } catch (error) {
    if (refreshIfMissing) {
      await refreshDevicesCache();
      return readDevicesCache({ refreshIfMissing: false });
    }
    throw cliError('CACHE_ERROR', 'device cache is not valid JSON', {
      path: runtimeConfig.cachePath,
      cause: error.message,
    });
  }

  if (!Array.isArray(parsedCache)) {
    throw cliError('CACHE_ERROR', 'device cache root must be a JSON array', {
      path: runtimeConfig.cachePath,
      actualType: typeof parsedCache,
    });
  }

  return parsedCache.map(normalizeDevice);
}

function filterDevices(deviceList, filters = {}) {
  const {
    room,
    type,
    name,
    online,
    traitCode,
  } = filters;

  return deviceList.filter((deviceItem) => {
    if (room && String(deviceItem.spaceName || '').toLowerCase() !== String(room).toLowerCase()) {
      return false;
    }
    if (type) {
      const lowerCaseType = String(type).toLowerCase();
      const hasMatchingType = deviceItem.deviceTypesList.some(
        (deviceTypeItem) => String(deviceTypeItem).toLowerCase() === lowerCaseType,
      );
      if (!hasMatchingType) {
        return false;
      }
    }
    if (name) {
      const lowerCaseName = String(name).toLowerCase();
      const haystack = `${deviceItem.deviceId} ${deviceItem.deviceName}`.toLowerCase();
      if (!haystack.includes(lowerCaseName)) {
        return false;
      }
    }
    if (online !== undefined) {
      if (deviceItem.online !== online) {
        return false;
      }
    }
    if (traitCode) {
      const lowerCaseTraitCode = String(traitCode).toLowerCase();
      const hasMatchingTrait = deviceItem.traits.some(
        (traitItem) => String(traitItem.traitCode).toLowerCase() === lowerCaseTraitCode,
      );
      if (!hasMatchingTrait) {
        return false;
      }
    }
    return true;
  });
}

function summarizeDevice(deviceItem) {
  return {
    deviceId: deviceItem.deviceId,
    deviceName: deviceItem.deviceName,
    spaceName: deviceItem.spaceName || '',
    online: deviceItem.online,
    deviceTypes: deviceItem.deviceTypesList.join(', '),
    endpointCount: deviceItem.endpointCount,
    traitCount: deviceItem.traitCount,
  };
}

function summarizeTraitTuple(traitItem) {
  return {
    endpointId: traitItem.endpointId,
    functionCode: traitItem.functionCode,
    traitCode: traitItem.traitCode,
    value: traitItem.value,
  };
}

function resolveDevice(deviceList, selector, options = {}) {
  const { room } = options;
  const normalizedSelector = String(selector || '').trim().toLowerCase();
  if (!normalizedSelector) {
    throw cliError('INVALID_VALUE', 'device selector is required');
  }

  const scopedDeviceList = room
    ? filterDevices(deviceList, { room })
    : deviceList;

  const exactIdMatches = scopedDeviceList.filter(
    (deviceItem) => String(deviceItem.deviceId).toLowerCase() === normalizedSelector,
  );
  if (exactIdMatches.length === 1) {
    return exactIdMatches[0];
  }

  const exactNameMatches = scopedDeviceList.filter(
    (deviceItem) => String(deviceItem.deviceName).toLowerCase() === normalizedSelector,
  );
  if (exactNameMatches.length === 1) {
    return exactNameMatches[0];
  }

  const fuzzyMatches = scopedDeviceList.filter((deviceItem) => {
    const haystack = `${deviceItem.deviceId} ${deviceItem.deviceName}`.toLowerCase();
    return haystack.includes(normalizedSelector);
  });

  if (fuzzyMatches.length === 1) {
    return fuzzyMatches[0];
  }

  if (exactIdMatches.length > 1 || exactNameMatches.length > 1 || fuzzyMatches.length > 1) {
    const candidates = (exactNameMatches.length > 1 ? exactNameMatches : fuzzyMatches).map(summarizeDevice);
    throw cliError('AMBIGUOUS', `multiple devices matched selector '${selector}'`, {
      candidates,
      room: room || null,
    });
  }

  throw cliError('NOT_FOUND', `device '${selector}' was not found in cache`, {
    selector,
    room: room || null,
  });
}

function resolveDeviceTraitTuple(deviceItem, options = {}) {
  const {
    traitCode,
    functionCode,
    endpointId,
  } = options;

  const normalizedTraitCode = String(traitCode || '').trim().toLowerCase();
  if (!normalizedTraitCode) {
    throw cliError('INVALID_VALUE', 'traitCode is required for trait resolution');
  }

  const normalizedFunctionCode = functionCode
    ? String(functionCode).trim().toLowerCase()
    : null;
  const normalizedEndpointId = endpointId !== undefined && endpointId !== null
    ? Number(endpointId)
    : null;

  if (normalizedEndpointId !== null && !Number.isFinite(normalizedEndpointId)) {
    throw cliError('INVALID_VALUE', `invalid endpointId: ${endpointId}`);
  }

  const matchingTraitList = deviceItem.traits.filter((traitItem) => {
    if (String(traitItem.traitCode).toLowerCase() !== normalizedTraitCode) {
      return false;
    }
    if (normalizedFunctionCode && String(traitItem.functionCode).toLowerCase() !== normalizedFunctionCode) {
      return false;
    }
    if (normalizedEndpointId !== null && Number(traitItem.endpointId) !== normalizedEndpointId) {
      return false;
    }
    return true;
  });

  if (matchingTraitList.length === 0) {
    throw cliError('CAPABILITY_NOT_SUPPORTED', 'the requested trait tuple was not found in the device cache', {
      device: summarizeDevice(deviceItem),
      requested: {
        endpointId: normalizedEndpointId,
        functionCode: functionCode || null,
        traitCode,
      },
    });
  }

  if (matchingTraitList.length > 1) {
    throw cliError('AMBIGUOUS', 'multiple trait tuples matched the requested trait on this device', {
      device: summarizeDevice(deviceItem),
      requested: {
        endpointId: normalizedEndpointId,
        functionCode: functionCode || null,
        traitCode,
      },
      candidates: matchingTraitList.map(summarizeTraitTuple),
      help: 'Provide --function-code and/or --endpoint-id to disambiguate the target trait tuple.',
    });
  }

  return matchingTraitList[0];
}

function getCacheInfo() {
  const { cachePath } = getRuntimeConfig({ allowMissing: true });
  if (!fs.existsSync(cachePath)) {
    return {
      exists: false,
      path: cachePath,
    };
  }

  const fileStats = fs.statSync(cachePath);
  return {
    exists: true,
    path: cachePath,
    sizeBytes: fileStats.size,
    modifiedAt: fileStats.mtime.toISOString(),
  };
}

module.exports = {
  filterDevices,
  getCacheInfo,
  readDevicesCache,
  refreshDevicesCache,
  resolveDevice,
  resolveDeviceTraitTuple,
  summarizeDevice,
};
