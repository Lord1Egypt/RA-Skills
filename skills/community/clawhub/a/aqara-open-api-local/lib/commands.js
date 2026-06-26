const fs = require('fs');
const path = require('path');

const { cliError } = require('./errors');
const {
  getRuntimeConfig,
  maskToken,
  readCliConfig,
  updateCliConfig,
} = require('./config');
const { postAqara } = require('./http');
const {
  filterDevices,
  getCacheInfo,
  readDevicesCache,
  refreshDevicesCache,
  resolveDevice,
  resolveDeviceTraitTuple,
  summarizeDevice,
} = require('./cache');
const {
  generateAutomationConfigFromIntent,
  validateAutomationConfig,
} = require('./automation');
const { enrichTraitItem, filterTraitCatalog, parseTraitCatalog } = require('./traits');
const { printJson, printKeyValues, printTable } = require('./output');

function outputPayload(payload, options, printer) {
  if (options.json) {
    printJson(payload);
    return;
  }
  if (typeof printer === 'function') {
    printer(payload);
    return;
  }
  console.log(payload);
}

function requireString(value, message) {
  if (!value || !String(value).trim()) {
    throw cliError('INVALID_VALUE', message);
  }
  return String(value).trim();
}

function parseBooleanInput(value, fieldName) {
  if (typeof value === 'boolean') {
    return value;
  }
  const normalizedValue = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'on', 'enabled'].includes(normalizedValue)) {
    return true;
  }
  if (['false', '0', 'no', 'off', 'disabled'].includes(normalizedValue)) {
    return false;
  }
  throw cliError('INVALID_VALUE', `invalid boolean for ${fieldName}: ${value}`);
}

function parseNumberInput(value, fieldName) {
  const parsedNumber = Number(value);
  if (!Number.isFinite(parsedNumber)) {
    throw cliError('INVALID_VALUE', `invalid number for ${fieldName}: ${value}`);
  }
  return parsedNumber;
}

function parseLiteralValue(rawValue) {
  if (rawValue === undefined) {
    return undefined;
  }

  const stringValue = String(rawValue).trim();
  if (stringValue === '') {
    return '';
  }

  try {
    return JSON.parse(stringValue);
  } catch (_) {
    // ignore and keep parsing
  }

  const lowerCaseValue = stringValue.toLowerCase();
  if (['true', 'false'].includes(lowerCaseValue)) {
    return lowerCaseValue === 'true';
  }

  const numericValue = Number(stringValue);
  if (Number.isFinite(numericValue) && /^-?\d+(\.\d+)?$/u.test(stringValue)) {
    return numericValue;
  }

  return stringValue;
}

function readJsonFile(filePath) {
  const absolutePath = path.isAbsolute(filePath)
    ? filePath
    : path.join(getRuntimeConfig({ allowMissing: true }).packageRootPath, filePath);

  let rawJsonText = '';
  try {
    rawJsonText = fs.readFileSync(absolutePath, 'utf8');
  } catch (error) {
    throw cliError('INVALID_VALUE', `failed to read JSON file: ${absolutePath}`, {
      cause: error.message,
    });
  }

  try {
    return JSON.parse(rawJsonText);
  } catch (error) {
    throw cliError('INVALID_VALUE', `failed to parse JSON file: ${absolutePath}`, {
      cause: error.message,
    });
  }
}

function getJsonInput(options, fileFlagName, jsonFlagName, defaultValue) {
  if (options[fileFlagName]) {
    return readJsonFile(options[fileFlagName]);
  }
  if (options[jsonFlagName]) {
    try {
      return JSON.parse(options[jsonFlagName]);
    } catch (error) {
      throw cliError('INVALID_VALUE', `failed to parse ${jsonFlagName}`, {
        cause: error.message,
      });
    }
  }
  if (defaultValue !== undefined) {
    return defaultValue;
  }
  throw cliError('INVALID_VALUE', `one of --${fileFlagName} or --${jsonFlagName} is required`);
}

function getArrayOption(options, ...flagNames) {
  const values = [];
  flagNames.forEach((flagName) => {
    const rawValue = options[flagName];
    if (rawValue === undefined) {
      return;
    }
    if (Array.isArray(rawValue)) {
      rawValue.forEach((item) => {
        String(item).split(',').forEach((splitItem) => {
          if (splitItem.trim()) {
            values.push(splitItem.trim());
          }
        });
      });
      return;
    }
    String(rawValue).split(',').forEach((splitItem) => {
      if (splitItem.trim()) {
        values.push(splitItem.trim());
      }
    });
  });
  return values;
}

function writeJsonOutputFile(filePath, payload) {
  const absolutePath = path.isAbsolute(filePath)
    ? filePath
    : path.join(getRuntimeConfig({ allowMissing: true }).packageRootPath, filePath);

  fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
  fs.writeFileSync(absolutePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  return absolutePath;
}

function getTraitCatalogMap() {
  const traitCatalog = parseTraitCatalog();
  return new Map(traitCatalog.map((traitItem) => [traitItem.traitCode, traitItem]));
}

function enrichDeviceTraits(deviceItem, traitCatalogMap) {
  return deviceItem.traits.map((traitItem) => enrichTraitItem(traitCatalogMap, traitItem));
}

function filterDeviceListByTraitCatalog(deviceList, options) {
  if (!options.writable && !options.readable && !options.reportable) {
    return deviceList;
  }

  const traitCatalogMap = getTraitCatalogMap();
  return deviceList.filter((deviceItem) => {
    const enrichedTraits = enrichDeviceTraits(deviceItem, traitCatalogMap);
    return enrichedTraits.some((traitItem) => {
      if (options.writable && !traitItem.writable) {
        return false;
      }
      if (options.readable && !traitItem.readable) {
        return false;
      }
      if (options.reportable && !traitItem.reportable) {
        return false;
      }
      return true;
    });
  });
}

async function doctor(options) {
  const runtimeConfig = getRuntimeConfig({ allowMissing: true });
  const cacheInfo = getCacheInfo();

  const resultPayload = {
    nodeVersion: process.version,
    packageRootPath: runtimeConfig.packageRootPath,
    endpointConfigured: Boolean(runtimeConfig.endpointUrl),
    tokenConfigured: Boolean(runtimeConfig.token),
    endpointSource: runtimeConfig.endpointSource,
    tokenSource: runtimeConfig.tokenSource,
    configPath: runtimeConfig.configPath,
    cacheInfo,
    runtime: {
      fetchAvailable: typeof fetch === 'function',
      cacheRefreshMode: 'node_cli',
    },
  };

  if (options.ping) {
    if (!runtimeConfig.endpointUrl || !runtimeConfig.token) {
      throw cliError('NO_TOKEN', 'doctor --ping requires configured Aqara credentials');
    }
    const pingResult = await postAqara('GetSpacesRequest', null, {
      includeEnvelope: options.raw,
    });
    resultPayload.ping = pingResult;
  }

  outputPayload(resultPayload, options, (payload) => {
    printKeyValues({
      nodeVersion: payload.nodeVersion,
      packageRootPath: payload.packageRootPath,
      endpointConfigured: payload.endpointConfigured,
      tokenConfigured: payload.tokenConfigured,
      endpointSource: payload.endpointSource,
      tokenSource: payload.tokenSource,
      configPath: payload.configPath,
      cacheExists: payload.cacheInfo.exists,
      cachePath: payload.cacheInfo.path,
      fetchAvailable: payload.runtime.fetchAvailable,
      cacheRefreshMode: payload.runtime.cacheRefreshMode,
    });
  });
}

async function devicesCacheRefresh(options) {
  const refreshResult = await refreshDevicesCache({ includeEnvelope: options.raw });
  outputPayload(refreshResult, options, (payload) => {
    console.log(`OK: wrote ${payload.deviceCount} devices to ${payload.path}`);
  });
}

async function devicesCacheInfo(options) {
  const cacheInfo = getCacheInfo();
  outputPayload(cacheInfo, options, (payload) => {
    printKeyValues(payload);
  });
}

async function devicesList(options) {
  let deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });
  deviceList = filterDevices(deviceList, {
    room: options.room,
    type: options.type,
    name: options.name,
    online: options.online !== undefined ? parseBooleanInput(options.online, 'online') : undefined,
    traitCode: options.traitCode,
  });
  deviceList = filterDeviceListByTraitCatalog(deviceList, options);

  const payload = deviceList.map((deviceItem) => {
    const summary = summarizeDevice(deviceItem);
    if (options.raw) {
      summary.raw = deviceItem.raw;
    }
    return summary;
  });

  outputPayload(payload, options, (items) => {
    printTable(items, [
      { key: 'deviceId', label: 'deviceId', maxWidth: 24 },
      { key: 'deviceName', label: 'deviceName', maxWidth: 28 },
      { key: 'spaceName', label: 'space', maxWidth: 20 },
      { key: 'deviceTypes', label: 'types', maxWidth: 28 },
      { key: 'online', label: 'online', maxWidth: 8 },
      { key: 'traitCount', label: 'traits', maxWidth: 8 },
    ]);
  });
}

async function devicesInspect(selector, options) {
  const deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });
  const deviceItem = resolveDevice(deviceList, selector, { room: options.room });
  const traitCatalogMap = getTraitCatalogMap();
  const payload = {
    deviceId: deviceItem.deviceId,
    deviceName: deviceItem.deviceName,
    spaceId: deviceItem.spaceId,
    spaceName: deviceItem.spaceName,
    online: deviceItem.online,
    deviceTypesList: deviceItem.deviceTypesList,
    traits: enrichDeviceTraits(deviceItem, traitCatalogMap),
  };
  if (options.raw) {
    payload.raw = deviceItem.raw;
  }

  outputPayload(payload, options, (item) => {
    printKeyValues({
      deviceId: item.deviceId,
      deviceName: item.deviceName,
      spaceName: item.spaceName,
      online: item.online,
      deviceTypesList: item.deviceTypesList.join(', '),
      traitCount: item.traits.length,
    });
  });
}

async function devicesTraits(selector, options) {
  const deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });
  const deviceItem = resolveDevice(deviceList, selector, { room: options.room });
  const traitCatalogMap = getTraitCatalogMap();

  let traitList = enrichDeviceTraits(deviceItem, traitCatalogMap);
  if (options.traitCode) {
    const lowerCaseTraitCode = String(options.traitCode).toLowerCase();
    traitList = traitList.filter((traitItem) => String(traitItem.traitCode).toLowerCase() === lowerCaseTraitCode);
  }
  if (options.writable) {
    traitList = traitList.filter((traitItem) => traitItem.writable);
  }
  if (options.readable) {
    traitList = traitList.filter((traitItem) => traitItem.readable);
  }
  if (options.reportable) {
    traitList = traitList.filter((traitItem) => traitItem.reportable);
  }

  outputPayload(traitList, options, (items) => {
    printTable(items, [
      { key: 'endpointId', label: 'endpoint', maxWidth: 10 },
      { key: 'functionCode', label: 'functionCode', maxWidth: 24 },
      { key: 'traitCode', label: 'traitCode', maxWidth: 22 },
      { key: 'traitNameChinese', label: 'traitName', maxWidth: 20 },
      { key: 'value', label: 'value', maxWidth: 18 },
      { key: 'writable', label: 'writable', maxWidth: 9 },
    ]);
  });
}

async function devicesTypes(options) {
  const responsePayload = await postAqara('GetDeviceTypeInfosRequest', null, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    const responseData = payload.data || payload.response?.data || [];
    printTable(responseData, [
      { key: 'deviceType', label: 'deviceType', maxWidth: 24 },
      { key: 'name', label: 'name', maxWidth: 20 },
    ]);
  });
}

async function devicesExecute(selector, options) {
  requireString(options.traitCode, '--trait-code is required');
  if (options.value === undefined) {
    throw cliError('INVALID_VALUE', '--value is required');
  }

  const deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });
  const deviceItem = resolveDevice(deviceList, selector, { room: options.room });
  const resolvedTraitTuple = resolveDeviceTraitTuple(deviceItem, {
    endpointId: options.endpointId !== undefined ? parseNumberInput(options.endpointId, 'endpointId') : undefined,
    functionCode: options.functionCode,
    traitCode: options.traitCode,
  });

  const requestItem = {
    deviceId: deviceItem.deviceId,
    endpointId: resolvedTraitTuple.endpointId,
    functionCode: resolvedTraitTuple.functionCode,
    traitCode: resolvedTraitTuple.traitCode,
    value: parseLiteralValue(options.value),
  };

  const responsePayload = await postAqara('ExecuteTraitRequest', [requestItem], {
    includeEnvelope: options.raw,
  });

  outputPayload(responsePayload, options, (payload) => {
    printKeyValues({
      deviceId: deviceItem.deviceId,
      deviceName: deviceItem.deviceName,
      endpointId: requestItem.endpointId,
      functionCode: requestItem.functionCode,
      traitCode: requestItem.traitCode,
      value: requestItem.value,
      resultCode: payload.code ?? payload.response?.code,
    });
  });
}

async function spacesList(options) {
  const responsePayload = await postAqara('GetSpacesRequest', null, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    const responseData = payload.data || payload.response?.data || [];
    printJson(responseData);
  });
}

async function spacesCreate(options) {
  const requestData = {
    name: requireString(options.name, '--name is required'),
  };
  if (options.spatialMarking) {
    requestData.spatialMarking = options.spatialMarking;
  }
  if (options.parentSpaceId) {
    requestData.parentSpaceId = options.parentSpaceId;
  }

  const responsePayload = await postAqara('CreateSpaceRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function spacesUpdate(options) {
  const requestData = {
    spaceId: requireString(options.spaceId, '--space-id is required'),
  };
  if (options.name) {
    requestData.name = options.name;
  }
  if (options.spatialMarking) {
    requestData.spatialMarking = options.spatialMarking;
  }
  if (options.parentSpaceId) {
    requestData.parentSpaceId = options.parentSpaceId;
  }
  if (Object.keys(requestData).length === 1) {
    throw cliError('INVALID_VALUE', 'spaces update requires at least one change such as --name or --spatial-marking');
  }

  const responsePayload = await postAqara('UpdateSpaceRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function spacesAssociate(options) {
  const deviceIds = getArrayOption(options, 'deviceId', 'deviceIds');
  if (deviceIds.length === 0) {
    throw cliError('INVALID_VALUE', 'spaces associate requires one or more --device-id values');
  }

  const requestData = {
    spaceId: requireString(options.spaceId, '--space-id is required'),
    deviceIds,
  };

  const responsePayload = await postAqara('AssociateDevicesToSpaceRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsCapabilities(options) {
  const requestData = getJsonInput(options, 'dataFile', 'dataJson', {});
  const responsePayload = await postAqara('QueryAutomationCapabilitiesRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsList(options) {
  const requestData = {
    pageNum: options.pageNum ? parseNumberInput(options.pageNum, 'pageNum') : 1,
    pageSize: options.pageSize ? parseNumberInput(options.pageSize, 'pageSize') : 50,
  };

  const definitionTypes = getArrayOption(options, 'definitionType', 'definitionTypes');
  if (definitionTypes.length > 0) {
    requestData.definitionTypes = definitionTypes;
  }
  if (options.orderBy) {
    requestData.orderBy = options.orderBy;
  }

  const responsePayload = await postAqara('GetAutomationListRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsGet(automationId, options) {
  const responsePayload = await postAqara(
    'GetAutomationDetailsRequest',
    requireString(automationId, 'automationId is required'),
    { includeEnvelope: options.raw },
  );
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsCreate(options) {
  const configJson = getJsonInput(options, 'configFile', 'configJson');
  const validationSummary = await validateAutomationConfig(configJson, options);
  const requestData = {
    definitionType: options.definitionType || 'SCRIPT_JSON',
    config: configJson,
  };
  const responsePayload = await postAqara('CreateAutomationRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    console.log(`validated automation config: ${validationSummary.metadataName}`);
    printJson(payload);
  });
}

async function automationsUpdate(automationId, options) {
  const configJson = getJsonInput(options, 'configFile', 'configJson');
  const validationSummary = await validateAutomationConfig(configJson, options);
  const requestData = {
    automationId: requireString(automationId, 'automationId is required'),
    definitionType: options.definitionType || 'SCRIPT_JSON',
    config: configJson,
    updateMask: ['config'],
  };

  const responsePayload = await postAqara('UpdateAutomationRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    console.log(`validated automation config: ${validationSummary.metadataName}`);
    printJson(payload);
  });
}

async function automationsValidate(options) {
  const configJson = getJsonInput(options, 'configFile', 'configJson');
  const validationSummary = await validateAutomationConfig(configJson, options);
  outputPayload(validationSummary, options, (payload) => {
    printKeyValues(payload);
  });
}

async function automationsGenerate(templateType, options) {
  const targetSelectorList = getArrayOption(options, 'light', 'lights', 'target', 'targets');
  const generatedAutomation = await generateAutomationConfigFromIntent(templateType, {
    ...options,
    targetSelectorList,
  });

  let outputPath = null;
  if (options.outputFile) {
    outputPath = writeJsonOutputFile(options.outputFile, generatedAutomation.config);
  }

  outputPayload({
    ...generatedAutomation,
    ...(outputPath ? { outputPath } : {}),
  }, options, (payload) => {
    if (payload.outputPath) {
      console.log(`wrote generated config to ${payload.outputPath}`);
    }
    printJson(payload.config);
  });
}

async function automationsCreateFromIntent(templateType, options) {
  const targetSelectorList = getArrayOption(options, 'light', 'lights', 'target', 'targets');
  const generatedAutomation = await generateAutomationConfigFromIntent(templateType, {
    ...options,
    targetSelectorList,
  });
  const validationSummary = await validateAutomationConfig(generatedAutomation.config, options);
  const requestData = {
    definitionType: options.definitionType || 'SCRIPT_JSON',
    config: generatedAutomation.config,
  };
  const responsePayload = await postAqara('CreateAutomationRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    console.log(`generated and validated automation config: ${validationSummary.metadataName}`);
    printJson(payload);
  });
}

async function automationsRename(automationId, options) {
  const requestData = {
    automationId: requireString(automationId, 'automationId is required'),
    definitionType: options.definitionType || 'SCRIPT_JSON',
    name: requireString(options.name, '--name is required'),
    updateMask: ['name'],
  };

  const responsePayload = await postAqara('UpdateAutomationRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsSetEnabled(automationIds, enabled, options) {
  if (!automationIds || automationIds.length === 0) {
    throw cliError('INVALID_VALUE', 'at least one automation id is required');
  }

  const requestData = {
    automationIds,
    enabled,
  };
  const responsePayload = await postAqara('UpdateAutomationStatusRequest', requestData, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function automationsDelete(automationIds, options) {
  if (!automationIds || automationIds.length === 0) {
    throw cliError('INVALID_VALUE', 'at least one automation id is required');
  }

  const responsePayload = await postAqara('DeleteAutomationRequest', automationIds, {
    includeEnvelope: options.raw,
  });
  outputPayload(responsePayload, options, (payload) => {
    printJson(payload);
  });
}

async function traitsList(options) {
  const traitCatalog = parseTraitCatalog();
  const filteredTraits = filterTraitCatalog(traitCatalog, {
    query: options.query || options.code || options.name,
    writable: options.writable ? true : undefined,
    readable: options.readable ? true : undefined,
    reportable: options.reportable ? true : undefined,
    valueType: options.valueType,
  });

  outputPayload(filteredTraits, options, (items) => {
    printTable(items, [
      { key: 'traitCode', label: 'traitCode', maxWidth: 24 },
      { key: 'traitNameChinese', label: 'traitName', maxWidth: 18 },
      { key: 'traitNameEnglish', label: 'traitNameEnglish', maxWidth: 26 },
      { key: 'valueType', label: 'valueType', maxWidth: 12 },
      { key: 'writable', label: 'writable', maxWidth: 9 },
      { key: 'reportable', label: 'reportable', maxWidth: 10 },
    ]);
  });
}

async function traitsSearch(query, options) {
  requireString(query, 'search query is required');
  return traitsList({
    ...options,
    query,
  });
}

async function configShow(options) {
  const { configPath, config } = readCliConfig();
  const runtimeConfig = getRuntimeConfig({ allowMissing: true });
  const payload = {
    configPath,
    endpointUrl: config.endpointUrl || config.AQARA_ENDPOINT_URL || '',
    tokenMasked: maskToken(config.token || config.AQARA_OPEN_API_TOKEN || ''),
    endpointConfigured: Boolean(runtimeConfig.endpointUrl),
    tokenConfigured: Boolean(runtimeConfig.token),
    endpointSource: runtimeConfig.endpointSource,
    tokenSource: runtimeConfig.tokenSource,
  };

  outputPayload(payload, options, (item) => {
    printKeyValues(item);
  });
}

async function configSetEndpoint(endpointUrl, options) {
  const normalizedEndpointUrl = requireString(endpointUrl, 'endpointUrl is required');
  const { configPath } = updateCliConfig((currentConfig) => ({
    ...currentConfig,
    endpointUrl: normalizedEndpointUrl,
  }));

  outputPayload({
    success: true,
    configPath,
    endpointUrl: normalizedEndpointUrl,
  }, options, (payload) => {
    printKeyValues(payload);
  });
}

async function configSetToken(token, options) {
  const normalizedToken = requireString(token, 'token is required');
  const { configPath } = updateCliConfig((currentConfig) => ({
    ...currentConfig,
    token: normalizedToken,
  }));

  outputPayload({
    success: true,
    configPath,
    tokenMasked: maskToken(normalizedToken),
  }, options, (payload) => {
    printKeyValues(payload);
  });
}

async function configClearEndpoint(options) {
  const { configPath, config } = updateCliConfig((currentConfig) => {
    const nextConfig = { ...currentConfig };
    delete nextConfig.endpointUrl;
    delete nextConfig.AQARA_ENDPOINT_URL;
    return nextConfig;
  });

  outputPayload({
    success: true,
    configPath,
    endpointStillPresent: Boolean(config.endpointUrl || config.AQARA_ENDPOINT_URL),
  }, options, (payload) => {
    printKeyValues(payload);
  });
}

async function configClearToken(options) {
  const { configPath, config } = updateCliConfig((currentConfig) => {
    const nextConfig = { ...currentConfig };
    delete nextConfig.token;
    delete nextConfig.AQARA_OPEN_API_TOKEN;
    return nextConfig;
  });

  outputPayload({
    success: true,
    configPath,
    tokenStillPresent: Boolean(config.token || config.AQARA_OPEN_API_TOKEN),
  }, options, (payload) => {
    printKeyValues(payload);
  });
}

module.exports = {
  automationsCapabilities,
  automationsCreate,
  automationsDelete,
  automationsGenerate,
  automationsGet,
  automationsList,
  automationsRename,
  automationsSetEnabled,
  automationsCreateFromIntent,
  automationsUpdate,
  automationsValidate,
  devicesCacheInfo,
  devicesCacheRefresh,
  devicesExecute,
  devicesInspect,
  devicesList,
  devicesTraits,
  devicesTypes,
  configClearEndpoint,
  configClearToken,
  configSetEndpoint,
  configSetToken,
  configShow,
  doctor,
  spacesAssociate,
  spacesCreate,
  spacesList,
  spacesUpdate,
  traitsList,
  traitsSearch,
};
