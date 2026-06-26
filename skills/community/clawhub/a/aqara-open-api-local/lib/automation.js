const { cliError } = require('./errors');
const {
  readDevicesCache,
  resolveDevice,
  resolveDeviceTraitTuple,
  summarizeDevice,
} = require('./cache');

const comparatorKeyList = [
  'is',
  'isNot',
  'greaterThan',
  'greaterThanOrEqual',
  'greaterThanOrEqualTo',
  'lessThan',
  'lessThanOrEqual',
  'lessThanOrEqualTo',
  'in',
];

function ensurePlainObject(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw cliError('INVALID_VALUE', `${label} must be an object`);
  }
  return value;
}

function ensureNonEmptyString(value, label) {
  if (!value || !String(value).trim()) {
    throw cliError('INVALID_VALUE', `${label} must be a non-empty string`);
  }
  return String(value).trim();
}

function ensureInteger(value, label) {
  if (!Number.isInteger(value)) {
    throw cliError('INVALID_VALUE', `${label} must be an integer`);
  }
  return value;
}

function ensureArray(value, label) {
  if (!Array.isArray(value)) {
    throw cliError('INVALID_VALUE', `${label} must be an array`);
  }
  return value;
}

function assertNoForbiddenFields(value, pathLabel = 'config') {
  if (!value || typeof value !== 'object') {
    return;
  }

  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      assertNoForbiddenFields(item, `${pathLabel}[${index}]`);
    });
    return;
  }

  Object.entries(value).forEach(([key, nestedValue]) => {
    if (key === 'operator' || key === 'fieldCode') {
      throw cliError('INVALID_VALUE', `forbidden field '${key}' found at ${pathLabel}`);
    }
    assertNoForbiddenFields(nestedValue, `${pathLabel}.${key}`);
  });
}

function assertComparatorPresent(nodeObject, pathLabel) {
  const hasComparator = comparatorKeyList.some((key) => Object.prototype.hasOwnProperty.call(nodeObject, key));
  if (!hasComparator) {
    throw cliError('INVALID_VALUE', `${pathLabel} must include at least one comparator field`);
  }
}

function buildDeviceMap(deviceList) {
  return new Map(deviceList.map((deviceItem) => [deviceItem.deviceId, deviceItem]));
}

function resolveExistingDevice(deviceMap, deviceId, pathLabel) {
  const matchingDevice = deviceMap.get(deviceId);
  if (!matchingDevice) {
    throw cliError('NOT_FOUND', `device '${deviceId}' referenced by ${pathLabel} was not found in cache`, {
      deviceId,
      path: pathLabel,
    });
  }
  return matchingDevice;
}

function validateDevicePropertySource(sourceObject, pathLabel, deviceMap) {
  ensurePlainObject(sourceObject, pathLabel);
  if (sourceObject.type !== 'device.property') {
    throw cliError('INVALID_VALUE', `${pathLabel}.type must be "device.property"`);
  }

  const deviceId = ensureNonEmptyString(sourceObject.deviceId, `${pathLabel}.deviceId`);
  const endpointId = ensureInteger(sourceObject.endpointId, `${pathLabel}.endpointId`);
  const functionCode = ensureNonEmptyString(sourceObject.functionCode, `${pathLabel}.functionCode`);
  const traitCode = ensureNonEmptyString(sourceObject.traitCode, `${pathLabel}.traitCode`);

  const deviceItem = resolveExistingDevice(deviceMap, deviceId, pathLabel);
  resolveDeviceTraitTuple(deviceItem, {
    endpointId,
    functionCode,
    traitCode,
  });
}

function validateDataRefSource(sourceObject, pathLabel, scopeNameSet) {
  ensurePlainObject(sourceObject, pathLabel);
  if (sourceObject.type !== 'data.ref') {
    throw cliError('INVALID_VALUE', `${pathLabel}.type must be "data.ref"`);
  }
  if (sourceObject.targets !== undefined) {
    throw cliError('INVALID_VALUE', `${pathLabel}.targets is forbidden`);
  }
  if (sourceObject.from !== '/metadata/scope') {
    throw cliError('INVALID_VALUE', `${pathLabel}.from must be "/metadata/scope"`);
  }
  ensurePlainObject(sourceObject.select, `${pathLabel}.select`);
  if (sourceObject.select.by !== 'name') {
    throw cliError('INVALID_VALUE', `${pathLabel}.select.by must be "name"`);
  }
  const selectedScopeName = ensureNonEmptyString(sourceObject.select.value, `${pathLabel}.select.value`);
  if (!scopeNameSet.has(selectedScopeName)) {
    throw cliError('NOT_FOUND', `${pathLabel}.select.value '${selectedScopeName}' was not found in metadata.scope`, {
      scopeName: selectedScopeName,
      path: pathLabel,
    });
  }
}

function validateSource(sourceObject, pathLabel, validationContext, allowedSourceTypes) {
  if (!allowedSourceTypes.includes(sourceObject?.type)) {
    throw cliError('INVALID_VALUE', `${pathLabel}.type must be one of: ${allowedSourceTypes.join(', ')}`);
  }

  if (sourceObject.type === 'device.property') {
    validateDevicePropertySource(sourceObject, pathLabel, validationContext.deviceMap);
    return;
  }

  if (sourceObject.type === 'data.ref') {
    validateDataRefSource(sourceObject, pathLabel, validationContext.scopeNameSet);
    return;
  }
}

function validateScopeItem(scopeItem, scopeIndex, validationContext) {
  const pathLabel = `metadata.scope[${scopeIndex}]`;
  ensurePlainObject(scopeItem, pathLabel);
  ensureNonEmptyString(scopeItem.name, `${pathLabel}.name`);
  if (validationContext.scopeNameSet.has(scopeItem.name)) {
    throw cliError('INVALID_VALUE', `duplicate scope name '${scopeItem.name}' in metadata.scope`);
  }
  validationContext.scopeNameSet.add(scopeItem.name);
  validateDevicePropertySource(scopeItem, pathLabel, validationContext.deviceMap);
}

function validateStarter(starterObject, starterIndex, automationIndex, validationContext) {
  const pathLabel = `automations[${automationIndex}].starters[${starterIndex}]`;
  ensurePlainObject(starterObject, pathLabel);

  if (starterObject.type === 'manual') {
    ensureNonEmptyString(starterObject.name, `${pathLabel}.name`);
    return;
  }

  if (starterObject.type === 'property.event') {
    validateSource(starterObject.source, `${pathLabel}.source`, validationContext, ['device.property', 'data.ref']);
    assertComparatorPresent(starterObject, pathLabel);
    if (starterObject.for !== undefined) {
      ensureNonEmptyString(starterObject.for, `${pathLabel}.for`);
    }
    if (starterObject.suppressFor !== undefined) {
      ensureNonEmptyString(starterObject.suppressFor, `${pathLabel}.suppressFor`);
    }
    return;
  }

  if (starterObject.type === 'time.schedule') {
    ensureNonEmptyString(starterObject.at, `${pathLabel}.at`);
    return;
  }

  throw cliError('INVALID_VALUE', `${pathLabel}.type '${starterObject.type}' is not supported in the default schema-first path`);
}

function validateCondition(conditionObject, pathLabel, validationContext) {
  ensurePlainObject(conditionObject, pathLabel);

  if (conditionObject.type === 'property.state') {
    if (conditionObject.source?.targets !== undefined) {
      throw cliError('INVALID_VALUE', `${pathLabel}.source.targets is forbidden`);
    }
    validateSource(conditionObject.source, `${pathLabel}.source`, validationContext, ['device.property', 'data.ref']);
    assertComparatorPresent(conditionObject, pathLabel);
    return;
  }

  if (conditionObject.type === 'and') {
    const nestedConditionList = ensureArray(conditionObject.conditions, `${pathLabel}.conditions`);
    if (nestedConditionList.length === 0) {
      throw cliError('INVALID_VALUE', `${pathLabel}.conditions must not be empty`);
    }
    nestedConditionList.forEach((nestedCondition, nestedIndex) => {
      validateCondition(nestedCondition, `${pathLabel}.conditions[${nestedIndex}]`, validationContext);
    });
    return;
  }

  if (conditionObject.type === 'time.between') {
    ensureNonEmptyString(conditionObject.after, `${pathLabel}.after`);
    ensureNonEmptyString(conditionObject.before, `${pathLabel}.before`);
    return;
  }

  throw cliError('INVALID_VALUE', `${pathLabel}.type '${conditionObject.type}' is not supported in the default schema-first path`);
}

function validateAction(actionObject, actionIndex, automationIndex, validationContext) {
  const pathLabel = `automations[${automationIndex}].actions[${actionIndex}]`;
  ensurePlainObject(actionObject, pathLabel);

  if (actionObject.type === 'delay') {
    ensureNonEmptyString(actionObject.for, `${pathLabel}.for`);
    return;
  }

  if (actionObject.type !== 'device.trait.write') {
    throw cliError('INVALID_VALUE', `${pathLabel}.type '${actionObject.type}' is not supported in the default schema-first path`);
  }

  const functionCode = ensureNonEmptyString(actionObject.functionCode, `${pathLabel}.functionCode`);
  const traitCode = ensureNonEmptyString(actionObject.traitCode, `${pathLabel}.traitCode`);
  const targetList = ensureArray(actionObject.targets, `${pathLabel}.targets`);

  if (targetList.length === 0) {
    throw cliError('INVALID_VALUE', `${pathLabel}.targets must not be empty`);
  }

  targetList.forEach((targetObject, targetIndex) => {
    const targetPathLabel = `${pathLabel}.targets[${targetIndex}]`;
    ensurePlainObject(targetObject, targetPathLabel);
    const deviceId = ensureNonEmptyString(targetObject.deviceId, `${targetPathLabel}.deviceId`);
    const endpointIdList = ensureArray(targetObject.endpointIds, `${targetPathLabel}.endpointIds`);
    if (endpointIdList.length === 0) {
      throw cliError('INVALID_VALUE', `${targetPathLabel}.endpointIds must not be empty`);
    }
    const deviceItem = resolveExistingDevice(validationContext.deviceMap, deviceId, targetPathLabel);
    endpointIdList.forEach((endpointId, endpointIndex) => {
      ensureInteger(endpointId, `${targetPathLabel}.endpointIds[${endpointIndex}]`);
      resolveDeviceTraitTuple(deviceItem, {
        endpointId,
        functionCode,
        traitCode,
      });
    });
  });
}

function validateAutomationBranch(automationObject, automationIndex, validationContext) {
  const pathLabel = `automations[${automationIndex}]`;
  ensurePlainObject(automationObject, pathLabel);
  ensureNonEmptyString(automationObject.name, `${pathLabel}.name`);

  const starterList = ensureArray(automationObject.starters, `${pathLabel}.starters`);
  const actionList = ensureArray(automationObject.actions, `${pathLabel}.actions`);
  if (starterList.length === 0) {
    throw cliError('INVALID_VALUE', `${pathLabel}.starters must not be empty`);
  }
  if (actionList.length === 0) {
    throw cliError('INVALID_VALUE', `${pathLabel}.actions must not be empty`);
  }

  starterList.forEach((starterObject, starterIndex) => {
    validateStarter(starterObject, starterIndex, automationIndex, validationContext);
  });

  if (automationObject.condition !== undefined) {
    validateCondition(automationObject.condition, `${pathLabel}.condition`, validationContext);
  }

  actionList.forEach((actionObject, actionIndex) => {
    validateAction(actionObject, actionIndex, automationIndex, validationContext);
  });
}

async function validateAutomationConfig(configObject, options = {}) {
  assertNoForbiddenFields(configObject);

  const validatedConfigObject = ensurePlainObject(configObject, 'config');
  const metadataObject = ensurePlainObject(validatedConfigObject.metadata, 'metadata');
  ensureNonEmptyString(metadataObject.name, 'metadata.name');

  const scopeList = ensureArray(metadataObject.scope || [], 'metadata.scope');
  const automationList = ensureArray(validatedConfigObject.automations, 'automations');
  if (automationList.length === 0) {
    throw cliError('INVALID_VALUE', 'automations must not be empty');
  }

  const deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });
  const validationContext = {
    deviceMap: buildDeviceMap(deviceList),
    scopeNameSet: new Set(),
  };

  scopeList.forEach((scopeItem, scopeIndex) => {
    validateScopeItem(scopeItem, scopeIndex, validationContext);
  });

  automationList.forEach((automationObject, automationIndex) => {
    validateAutomationBranch(automationObject, automationIndex, validationContext);
  });

  return {
    valid: true,
    metadataName: metadataObject.name,
    scopeCount: scopeList.length,
    automationCount: automationList.length,
    deviceCount: deviceList.length,
  };
}

function normalizeText(value) {
  return String(value || '').trim().toLowerCase();
}

function buildSafeScopeName(roomName) {
  return String(roomName || 'room')
    .trim()
    .replace(/[^a-zA-Z0-9]+/gu, ' ')
    .split(' ')
    .filter(Boolean)
    .map((part, index) => {
      const lowerCasePart = part.toLowerCase();
      if (index === 0) {
        return lowerCasePart;
      }
      return lowerCasePart.charAt(0).toUpperCase() + lowerCasePart.slice(1);
    })
    .join('') || 'room';
}

function filterDevicesByRoom(deviceList, roomName) {
  const normalizedRoomName = normalizeText(roomName);
  return deviceList.filter((deviceItem) => normalizeText(deviceItem.spaceName) === normalizedRoomName);
}

function listAvailableRoomNameList(deviceList) {
  return [...new Set(
    deviceList
      .map((deviceItem) => String(deviceItem.spaceName || '').trim())
      .filter(Boolean),
  )].sort((leftRoomName, rightRoomName) => leftRoomName.localeCompare(rightRoomName));
}

function normalizeStringList(value) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value
    .map((item) => String(item || '').trim())
    .filter(Boolean);
}

function parseBooleanLikeValue(value, label) {
  if (typeof value === 'boolean') {
    return value;
  }

  const normalizedValue = String(value || '').trim().toLowerCase();
  if (['true', '1', 'yes', 'on', 'enabled'].includes(normalizedValue)) {
    return true;
  }
  if (['false', '0', 'no', 'off', 'disabled'].includes(normalizedValue)) {
    return false;
  }

  throw cliError('INVALID_VALUE', `${label} must be a boolean-like value`, {
    value,
    help: `Use true/false for ${label}.`,
  });
}

function resolveRoomEvidence(deviceList, options) {
  const roomName = ensureNonEmptyString(options.room, 'room');
  const roomDeviceList = filterDevicesByRoom(deviceList, roomName);
  const availableRoomNameList = listAvailableRoomNameList(deviceList);
  const retrievedSpaceNameList = normalizeStringList(options.retrievedSpaceNameList || options.spaceNameList);
  const roomExistsInRetrievedSpaceEvidence = retrievedSpaceNameList
    .some((retrievedSpaceName) => normalizeText(retrievedSpaceName) === normalizeText(roomName));

  if (roomDeviceList.length > 0) {
    return {
      roomName,
      roomDeviceList,
      availableRoomNameList,
      roomExistsInRetrievedSpaceEvidence,
    };
  }

  if (roomExistsInRetrievedSpaceEvidence) {
    throw cliError('NOT_FOUND', `room '${roomName}' exists in retrieved space evidence but has no devices in retrieved device evidence`, {
      room: roomName,
      availableRooms: availableRoomNameList,
      help: 'Stop and clarify with the user, or refresh the retrieved device evidence. Do not fall back to a different room automatically.',
    });
  }

  throw cliError('NOT_FOUND', `room '${roomName}' was not found in retrieved device evidence`, {
    room: roomName,
    availableRooms: availableRoomNameList,
    help: 'Use a room that already exists in the retrieved evidence, or refresh evidence first. Do not fall back to a different room automatically.',
  });
}

function hasTraitTuple(deviceItem, traitCode, functionCode) {
  try {
    resolveDeviceTraitTuple(deviceItem, {
      traitCode,
      functionCode,
    });
    return true;
  } catch (error) {
    return false;
  }
}

function resolveMotionSensorDevice(deviceList, options) {
  const roomEvidence = resolveRoomEvidence(deviceList, options);
  const { roomName, roomDeviceList, availableRoomNameList } = roomEvidence;

  if (options.sensor) {
    const selectedSensorDevice = resolveDevice(deviceList, options.sensor, { room: roomName });
    resolveDeviceTraitTuple(selectedSensorDevice, {
      traitCode: 'Occupancy',
      functionCode: 'OccupancySensing',
    });
    return selectedSensorDevice;
  }

  const candidateSensorList = roomDeviceList.filter((deviceItem) => hasTraitTuple(deviceItem, 'Occupancy', 'OccupancySensing'));
  if (candidateSensorList.length === 0) {
    throw cliError('NOT_FOUND', `no occupancy sensor was found in room '${roomName}'`, {
      room: roomName,
      availableRooms: availableRoomNameList,
      roomDeviceCount: roomDeviceList.length,
      help: 'Choose a room that already contains an occupancy sensor in the retrieved evidence, or specify --sensor explicitly.',
    });
  }
  if (candidateSensorList.length > 1) {
    throw cliError('AMBIGUOUS', `multiple occupancy sensors were found in room '${roomName}'`, {
      room: roomName,
      candidates: candidateSensorList.map(summarizeDevice),
      help: 'Provide --sensor <deviceIdOrName> to choose the motion source device.',
    });
  }
  return candidateSensorList[0];
}

function buildOnOffTargetSpec(deviceItem) {
  const matchingTupleList = deviceItem.traits.filter((traitItem) => {
    return normalizeText(traitItem.functionCode) === 'output'
      && normalizeText(traitItem.traitCode) === 'onoff';
  });

  if (matchingTupleList.length === 0) {
    throw cliError('CAPABILITY_NOT_SUPPORTED', `device '${deviceItem.deviceName}' does not expose Output/OnOff in cache`, {
      device: summarizeDevice(deviceItem),
    });
  }

  const endpointIdList = [...new Set(matchingTupleList.map((traitItem) => traitItem.endpointId))];
  endpointIdList.forEach((endpointId, endpointIndex) => {
    ensureInteger(endpointId, `target.endpointIds[${endpointIndex}]`);
  });

  return {
    deviceId: deviceItem.deviceId,
    endpointIds: endpointIdList,
  };
}

function resolveTargetDeviceList(deviceList, options) {
  const roomEvidence = resolveRoomEvidence(deviceList, options);
  const { roomName, roomDeviceList, availableRoomNameList } = roomEvidence;

  const targetSelectorList = Array.isArray(options.targetSelectorList) ? options.targetSelectorList : [];
  if (targetSelectorList.length > 0) {
    return targetSelectorList.map((targetSelector) => {
      const targetDevice = resolveDevice(deviceList, targetSelector, { room: roomName });
      buildOnOffTargetSpec(targetDevice);
      return targetDevice;
    });
  }

  const lightTargetList = roomDeviceList.filter((deviceItem) => {
    const hasOnOff = hasTraitTuple(deviceItem, 'OnOff', 'Output');
    const normalizedTypeList = (deviceItem.deviceTypesList || []).map((deviceType) => normalizeText(deviceType));
    return hasOnOff && normalizedTypeList.includes('light');
  });

  if (lightTargetList.length > 0) {
    return lightTargetList;
  }

  const fallbackTargetList = roomDeviceList.filter((deviceItem) => hasTraitTuple(deviceItem, 'OnOff', 'Output'));
  if (fallbackTargetList.length > 0) {
    return fallbackTargetList;
  }

  throw cliError('NOT_FOUND', `no controllable OnOff targets were found in room '${roomName}'`, {
    room: roomName,
    availableRooms: availableRoomNameList,
    roomDeviceCount: roomDeviceList.length,
    help: 'Stop and clarify with the user. Do not move the automation to a different room automatically.',
  });
}

function resolveManualSceneTargetDeviceList(deviceList, options) {
  const roomEvidence = resolveRoomEvidence(deviceList, options);
  const { roomName, roomDeviceList, availableRoomNameList } = roomEvidence;
  const targetSelectorList = Array.isArray(options.targetSelectorList) ? options.targetSelectorList : [];

  if (targetSelectorList.length > 0) {
    return targetSelectorList.map((targetSelector) => {
      const targetDevice = resolveDevice(deviceList, targetSelector, { room: roomName });
      buildOnOffTargetSpec(targetDevice);
      return targetDevice;
    });
  }

  const candidateTargetList = roomDeviceList.filter((deviceItem) => hasTraitTuple(deviceItem, 'OnOff', 'Output'));
  if (candidateTargetList.length > 0) {
    return candidateTargetList;
  }

  throw cliError('NOT_FOUND', `no controllable OnOff targets were found in room '${roomName}'`, {
    room: roomName,
    availableRooms: availableRoomNameList,
    roomDeviceCount: roomDeviceList.length,
    help: 'Stop and clarify with the user. Do not move the automation to a different room automatically.',
  });
}

function buildStateCondition(targetSpec, value, options = {}) {
  const stateConditionObject = {
    type: 'property.state',
    source: {
      type: 'device.property',
      deviceId: targetSpec.deviceId,
      endpointId: targetSpec.endpointIds[0],
      functionCode: 'Output',
      traitCode: 'OnOff',
    },
    is: value,
  };

  if (!options.after && !options.before) {
    return stateConditionObject;
  }

  if (!options.after || !options.before) {
    throw cliError('INVALID_VALUE', 'both --after and --before are required when using a time window');
  }

  return {
    type: 'and',
    conditions: [
      {
        type: 'time.between',
        after: options.after,
        before: options.before,
      },
      stateConditionObject,
    ],
  };
}

function buildTimeCondition(options = {}) {
  if (!options.after && !options.before) {
    return undefined;
  }
  if (!options.after || !options.before) {
    throw cliError('INVALID_VALUE', 'both --after and --before are required when using a time window');
  }
  return {
    type: 'time.between',
    after: options.after,
    before: options.before,
  };
}

function buildMotionLightConfig(sensorDevice, targetDeviceList, options) {
  const motionTraitTuple = resolveDeviceTraitTuple(sensorDevice, {
    traitCode: 'Occupancy',
    functionCode: 'OccupancySensing',
  });
  const targetSpecList = targetDeviceList.map(buildOnOffTargetSpec);
  const safeRoomName = ensureNonEmptyString(options.room, 'room');
  const scopeName = `${buildSafeScopeName(safeRoomName)}Motion`;
  const metadataName = options.name || `${safeRoomName} motion light automation`;
  const metadataDescription = options.description
    || `${safeRoomName}: occupied turns lights on, unoccupied turns lights off.`;
  const onForDuration = options.onFor || '5sec';
  const offForDuration = options.offFor || '5min';
  const suppressForDuration = options.suppressFor || '30sec';

  const singleTargetSpec = targetSpecList.length === 1 && targetSpecList[0].endpointIds.length === 1
    ? targetSpecList[0]
    : null;

  const onBranchCondition = singleTargetSpec
    ? buildStateCondition(singleTargetSpec, false, options)
    : buildTimeCondition(options);
  const offBranchCondition = singleTargetSpec
    ? buildStateCondition(singleTargetSpec, true)
    : undefined;

  return {
    metadata: {
      name: metadataName,
      description: metadataDescription,
      scope: [
        {
          name: scopeName,
          type: 'device.property',
          deviceId: sensorDevice.deviceId,
          endpointId: motionTraitTuple.endpointId,
          functionCode: motionTraitTuple.functionCode,
          traitCode: motionTraitTuple.traitCode,
        },
      ],
    },
    automations: [
      {
        name: `${safeRoomName} occupied lights on`,
        starters: [
          {
            type: 'property.event',
            source: {
              type: 'data.ref',
              from: '/metadata/scope',
              select: {
                by: 'name',
                value: scopeName,
              },
            },
            is: true,
            for: onForDuration,
            suppressFor: suppressForDuration,
          },
        ],
        ...(onBranchCondition ? { condition: onBranchCondition } : {}),
        actions: [
          {
            type: 'device.trait.write',
            functionCode: 'Output',
            traitCode: 'OnOff',
            targets: targetSpecList,
            value: true,
          },
        ],
      },
      {
        name: `${safeRoomName} unoccupied lights off`,
        starters: [
          {
            type: 'property.event',
            source: {
              type: 'data.ref',
              from: '/metadata/scope',
              select: {
                by: 'name',
                value: scopeName,
              },
            },
            is: false,
            for: offForDuration,
            suppressFor: suppressForDuration,
          },
        ],
        ...(offBranchCondition ? { condition: offBranchCondition } : {}),
        actions: [
          {
            type: 'device.trait.write',
            functionCode: 'Output',
            traitCode: 'OnOff',
            targets: targetSpecList,
            value: false,
          },
        ],
      },
    ],
  };
}

function buildManualSceneConfig(targetDeviceList, options) {
  const roomName = ensureNonEmptyString(options.room, 'room');
  const targetSpecList = targetDeviceList.map(buildOnOffTargetSpec);
  const sceneName = options.sceneName || options['scene-name'] || `${roomName} Scene`;
  const targetValue = options.value === undefined
    ? false
    : parseBooleanLikeValue(options.value, '--value');
  const normalizedActionLabel = targetValue ? 'on' : 'off';

  return {
    metadata: {
      name: options.name || `${roomName} manual scene`,
      description: options.description || `${roomName}: manually turn ${normalizedActionLabel} controllable OnOff devices.`,
    },
    automations: [
      {
        name: options.automationName || `${roomName} all ${normalizedActionLabel}`,
        starters: [
          {
            type: 'manual',
            name: sceneName,
          },
        ],
        actions: [
          {
            type: 'device.trait.write',
            functionCode: 'Output',
            traitCode: 'OnOff',
            targets: targetSpecList,
            value: targetValue,
          },
        ],
      },
    ],
  };
}

async function generateAutomationConfigFromIntent(templateType, options = {}) {
  const normalizedTemplateType = ensureNonEmptyString(templateType, 'templateType').toLowerCase();
  const deviceList = await readDevicesCache({ refreshIfMissing: Boolean(options.refresh) });

  if (!['motion-light', 'manual-scene', 'manual-scene-off'].includes(normalizedTemplateType)) {
    throw cliError('INVALID_VALUE', `unsupported automation template '${templateType}'`, {
      supportedTemplates: ['motion-light', 'manual-scene', 'manual-scene-off'],
    });
  }

  const roomEvidence = resolveRoomEvidence(deviceList, options);
  if (normalizedTemplateType === 'manual-scene' || normalizedTemplateType === 'manual-scene-off') {
    const targetDeviceList = resolveManualSceneTargetDeviceList(deviceList, options);
    const configObject = buildManualSceneConfig(targetDeviceList, {
      ...options,
      ...(normalizedTemplateType === 'manual-scene-off' ? { value: false } : {}),
      ...(normalizedTemplateType === 'manual-scene-off' && options.sceneName === undefined && options['scene-name'] === undefined
        ? { sceneName: `${options.room} Off` }
        : {}),
      ...(normalizedTemplateType === 'manual-scene-off' && options.name === undefined
        ? { name: `${options.room} off scene` }
        : {}),
      ...(normalizedTemplateType === 'manual-scene-off' && options.automationName === undefined
        ? { automationName: `${options.room} all off` }
        : {}),
    });

    return {
      templateType: normalizedTemplateType,
      room: options.room,
      availableRooms: roomEvidence.availableRoomNameList,
      roomDeviceCount: roomEvidence.roomDeviceList.length,
      targetDevices: targetDeviceList.map(summarizeDevice),
      config: configObject,
    };
  }

  const sensorDevice = resolveMotionSensorDevice(deviceList, options);
  const targetDeviceList = resolveTargetDeviceList(deviceList, options);
  const configObject = buildMotionLightConfig(sensorDevice, targetDeviceList, options);

  return {
    templateType: normalizedTemplateType,
    room: options.room,
    availableRooms: roomEvidence.availableRoomNameList,
    roomDeviceCount: roomEvidence.roomDeviceList.length,
    sensorDevice: summarizeDevice(sensorDevice),
    targetDevices: targetDeviceList.map(summarizeDevice),
    config: configObject,
  };
}

module.exports = {
  generateAutomationConfigFromIntent,
  validateAutomationConfig,
};
