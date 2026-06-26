#!/usr/bin/env node

const commands = require('../lib/commands');
const { cliError, exitCodeForError } = require('../lib/errors');

function parseArgs(argv) {
  const parsedArgs = { _: [] };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) {
      parsedArgs._.push(token);
      continue;
    }

    const withoutPrefix = token.slice(2);
    const equalsIndex = withoutPrefix.indexOf('=');

    if (equalsIndex >= 0) {
      const key = withoutPrefix.slice(0, equalsIndex);
      const value = withoutPrefix.slice(equalsIndex + 1);
      if (parsedArgs[key] === undefined) {
        parsedArgs[key] = value;
      } else if (Array.isArray(parsedArgs[key])) {
        parsedArgs[key].push(value);
      } else {
        parsedArgs[key] = [parsedArgs[key], value];
      }
      continue;
    }

    const nextToken = argv[index + 1];
    if (nextToken && !nextToken.startsWith('--')) {
      if (parsedArgs[withoutPrefix] === undefined) {
        parsedArgs[withoutPrefix] = nextToken;
      } else if (Array.isArray(parsedArgs[withoutPrefix])) {
        parsedArgs[withoutPrefix].push(nextToken);
      } else {
        parsedArgs[withoutPrefix] = [parsedArgs[withoutPrefix], nextToken];
      }
      index += 1;
      continue;
    }

    parsedArgs[withoutPrefix] = true;
  }

  if (parsedArgs['trait-code'] !== undefined) parsedArgs.traitCode = parsedArgs['trait-code'];
  if (parsedArgs['endpoint-id'] !== undefined) parsedArgs.endpointId = parsedArgs['endpoint-id'];
  if (parsedArgs['function-code'] !== undefined) parsedArgs.functionCode = parsedArgs['function-code'];
  if (parsedArgs['config-file'] !== undefined) parsedArgs.configFile = parsedArgs['config-file'];
  if (parsedArgs['config-json'] !== undefined) parsedArgs.configJson = parsedArgs['config-json'];
  if (parsedArgs['data-file'] !== undefined) parsedArgs.dataFile = parsedArgs['data-file'];
  if (parsedArgs['data-json'] !== undefined) parsedArgs.dataJson = parsedArgs['data-json'];
  if (parsedArgs['page-num'] !== undefined) parsedArgs.pageNum = parsedArgs['page-num'];
  if (parsedArgs['page-size'] !== undefined) parsedArgs.pageSize = parsedArgs['page-size'];
  if (parsedArgs['order-by'] !== undefined) parsedArgs.orderBy = parsedArgs['order-by'];
  if (parsedArgs['definition-type'] !== undefined) parsedArgs.definitionType = parsedArgs['definition-type'];
  if (parsedArgs['space-id'] !== undefined) parsedArgs.spaceId = parsedArgs['space-id'];
  if (parsedArgs['device-id'] !== undefined) parsedArgs.deviceId = parsedArgs['device-id'];
  if (parsedArgs['device-ids'] !== undefined) parsedArgs.deviceIds = parsedArgs['device-ids'];
  if (parsedArgs['parent-space-id'] !== undefined) parsedArgs.parentSpaceId = parsedArgs['parent-space-id'];
  if (parsedArgs['spatial-marking'] !== undefined) parsedArgs.spatialMarking = parsedArgs['spatial-marking'];
  if (parsedArgs['value-type'] !== undefined) parsedArgs.valueType = parsedArgs['value-type'];
  if (parsedArgs['output-file'] !== undefined) parsedArgs.outputFile = parsedArgs['output-file'];
  if (parsedArgs['on-for'] !== undefined) parsedArgs.onFor = parsedArgs['on-for'];
  if (parsedArgs['off-for'] !== undefined) parsedArgs.offFor = parsedArgs['off-for'];
  if (parsedArgs['suppress-for'] !== undefined) parsedArgs.suppressFor = parsedArgs['suppress-for'];

  return parsedArgs;
}

function printHelp() {
  console.log(`Aqara Open API CLI

Usage:
  aqara help
  aqara doctor [--ping] [--json]
  aqara config show [--json]
  aqara config set-endpoint <url> [--json]
  aqara config set-token <token> [--json]
  aqara config clear-endpoint [--json]
  aqara config clear-token [--json]

  aqara devices cache refresh [--json]
  aqara devices cache info [--json]
  aqara devices list [--room <name>] [--type <deviceType>] [--name <query>] [--online <true|false>] [--trait-code <code>] [--writable] [--readable] [--reportable] [--refresh] [--json]
  aqara devices inspect <deviceIdOrName> [--room <name>] [--refresh] [--json] [--raw]
  aqara devices traits <deviceIdOrName> [--room <name>] [--trait-code <code>] [--writable] [--readable] [--reportable] [--refresh] [--json]
  aqara devices types [--json]
  aqara devices execute <deviceIdOrName> --trait-code <code> --value <value> [--function-code <code>] [--endpoint-id <n>] [--room <name>] [--refresh] [--json] [--raw]

  aqara spaces list [--json]
  aqara spaces create --name <name> [--spatial-marking <mark>] [--parent-space-id <id>] [--json] [--raw]
  aqara spaces update --space-id <id> [--name <name>] [--spatial-marking <mark>] [--parent-space-id <id>] [--json] [--raw]
  aqara spaces associate --space-id <id> --device-id <id> [--device-id <id> ...] [--json] [--raw]

  aqara automations capabilities [--data-file <path> | --data-json <json>] [--json] [--raw]
  aqara automations list [--page-num <n>] [--page-size <n>] [--order-by <expr>] [--definition-type <type>] [--json] [--raw]
  aqara automations get <automationId> [--json] [--raw]
  aqara automations generate motion-light --room <name> [--sensor <deviceIdOrName>] [--light <deviceIdOrName> ...] [--after <HH:MM>] [--before <HH:MM>] [--on-for <duration>] [--off-for <duration>] [--suppress-for <duration>] [--output-file <path>] [--json]
  aqara automations generate manual-scene --room <name> --value <true|false> [--target <deviceIdOrName> ...] [--scene-name <name>] [--output-file <path>] [--json]
  aqara automations generate manual-scene-off --room <name> [--target <deviceIdOrName> ...] [--scene-name <name>] [--output-file <path>] [--json]
  aqara automations create-from-intent motion-light --room <name> [--sensor <deviceIdOrName>] [--light <deviceIdOrName> ...] [--after <HH:MM>] [--before <HH:MM>] [--on-for <duration>] [--off-for <duration>] [--suppress-for <duration>] [--definition-type <type>] [--json] [--raw]
  aqara automations create-from-intent manual-scene --room <name> --value <true|false> [--target <deviceIdOrName> ...] [--scene-name <name>] [--definition-type <type>] [--json] [--raw]
  aqara automations create-from-intent manual-scene-off --room <name> [--target <deviceIdOrName> ...] [--scene-name <name>] [--definition-type <type>] [--json] [--raw]
  aqara automations validate --config-file <path> | --config-json <json> [--refresh] [--json]
  aqara automations create --config-file <path> | --config-json <json> [--definition-type <type>] [--json] [--raw]
  aqara automations update <automationId> --config-file <path> | --config-json <json> [--definition-type <type>] [--json] [--raw]
  aqara automations rename <automationId> --name <name> [--definition-type <type>] [--json] [--raw]
  aqara automations enable <automationId> [moreIds...] [--json] [--raw]
  aqara automations disable <automationId> [moreIds...] [--json] [--raw]
  aqara automations delete <automationId> [moreIds...] [--json] [--raw]

  aqara traits list [--code <query>] [--name <query>] [--value-type <type>] [--writable] [--readable] [--reportable] [--json]
  aqara traits search <query> [--json]

Notes:
  - Credentials come from AQARA_ENDPOINT_URL and AQARA_OPEN_API_TOKEN first, then from the AQARA CLI config file.
  - Device cache refresh is handled inside the Node CLI and writes data/devices.json directly.
  - JSON output is recommended for automation and script integration.
`);
}

function printError(error, options) {
  const code = error?.code || 'ERROR';
  const message = error?.message || String(error);

  if (options.json) {
    const payload = {
      error: {
        code,
        message,
      },
    };
    if (error?.details !== undefined) {
      payload.error.details = error.details;
    }
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  console.error(`error[${code}]: ${message}`);
  if (error?.details?.help) {
    console.error(`help: ${error.details.help}`);
  }
  if (Array.isArray(error?.details?.candidates) && error.details.candidates.length > 0) {
    console.error('candidates:');
    error.details.candidates.forEach((candidate) => {
      const summaryText = `${candidate.deviceId || candidate.id || ''} ${candidate.deviceName || candidate.name || ''}`.trim();
      if (summaryText) {
        console.error(`  ${summaryText}`);
        return;
      }
      console.error(`  ${JSON.stringify(candidate)}`);
    });
  }
}

async function run(commandHandler, options) {
  try {
    await commandHandler();
  } catch (error) {
    printError(error, options);
    process.exit(exitCodeForError(error));
  }
}

async function main() {
  const options = parseArgs(process.argv);
  const positionals = options._;
  const [group, action, ...rest] = positionals;

  if (!group || group === 'help' || options.help) {
    printHelp();
    return;
  }

  if (group === 'doctor') {
    await run(() => commands.doctor(options), options);
    return;
  }

  if (group === 'config') {
    if (action === 'show') {
      await run(() => commands.configShow(options), options);
      return;
    }
    if (action === 'set-endpoint') {
      await run(() => commands.configSetEndpoint(rest[0], options), options);
      return;
    }
    if (action === 'set-token') {
      await run(() => commands.configSetToken(rest[0], options), options);
      return;
    }
    if (action === 'clear-endpoint') {
      await run(() => commands.configClearEndpoint(options), options);
      return;
    }
    if (action === 'clear-token') {
      await run(() => commands.configClearToken(options), options);
      return;
    }
    throw cliError('INVALID_VALUE', 'invalid config action. Use: show, set-endpoint, set-token, clear-endpoint, clear-token');
  }

  if (group === 'devices') {
    if (action === 'cache') {
      const cacheAction = rest[0];
      if (cacheAction === 'refresh') {
        await run(() => commands.devicesCacheRefresh(options), options);
        return;
      }
      if (cacheAction === 'info') {
        await run(() => commands.devicesCacheInfo(options), options);
        return;
      }
      throw cliError('INVALID_VALUE', 'invalid devices cache action. Use: refresh, info');
    }

    if (action === 'list') {
      await run(() => commands.devicesList(options), options);
      return;
    }
    if (action === 'inspect') {
      await run(() => commands.devicesInspect(rest[0], options), options);
      return;
    }
    if (action === 'traits') {
      await run(() => commands.devicesTraits(rest[0], options), options);
      return;
    }
    if (action === 'types') {
      await run(() => commands.devicesTypes(options), options);
      return;
    }
    if (action === 'execute') {
      await run(() => commands.devicesExecute(rest[0], options), options);
      return;
    }
    throw cliError('INVALID_VALUE', 'invalid devices action. Use: cache, list, inspect, traits, types, execute');
  }

  if (group === 'spaces') {
    if (action === 'list') {
      await run(() => commands.spacesList(options), options);
      return;
    }
    if (action === 'create') {
      await run(() => commands.spacesCreate(options), options);
      return;
    }
    if (action === 'update') {
      await run(() => commands.spacesUpdate(options), options);
      return;
    }
    if (action === 'associate') {
      await run(() => commands.spacesAssociate(options), options);
      return;
    }
    throw cliError('INVALID_VALUE', 'invalid spaces action. Use: list, create, update, associate');
  }

  if (group === 'automations') {
    if (action === 'capabilities') {
      await run(() => commands.automationsCapabilities(options), options);
      return;
    }
    if (action === 'list') {
      await run(() => commands.automationsList(options), options);
      return;
    }
    if (action === 'get') {
      await run(() => commands.automationsGet(rest[0], options), options);
      return;
    }
    if (action === 'generate') {
      await run(() => commands.automationsGenerate(rest[0], options), options);
      return;
    }
    if (action === 'create-from-intent') {
      await run(() => commands.automationsCreateFromIntent(rest[0], options), options);
      return;
    }
    if (action === 'validate') {
      await run(() => commands.automationsValidate(options), options);
      return;
    }
    if (action === 'create') {
      await run(() => commands.automationsCreate(options), options);
      return;
    }
    if (action === 'update') {
      await run(() => commands.automationsUpdate(rest[0], options), options);
      return;
    }
    if (action === 'rename') {
      await run(() => commands.automationsRename(rest[0], options), options);
      return;
    }
    if (action === 'enable') {
      await run(() => commands.automationsSetEnabled(rest, true, options), options);
      return;
    }
    if (action === 'disable') {
      await run(() => commands.automationsSetEnabled(rest, false, options), options);
      return;
    }
    if (action === 'delete') {
      await run(() => commands.automationsDelete(rest, options), options);
      return;
    }
    throw cliError('INVALID_VALUE', 'invalid automations action. Use: capabilities, list, get, generate, create-from-intent, validate, create, update, rename, enable, disable, delete');
  }

  if (group === 'traits') {
    if (action === 'list') {
      await run(() => commands.traitsList(options), options);
      return;
    }
    if (action === 'search') {
      await run(() => commands.traitsSearch(rest[0], options), options);
      return;
    }
    throw cliError('INVALID_VALUE', 'invalid traits action. Use: list, search');
  }

  throw cliError('INVALID_VALUE', `unknown command group: ${group}`);
}

main().catch((error) => {
  const options = parseArgs(process.argv);
  printError(error, options);
  process.exit(exitCodeForError(error));
});
