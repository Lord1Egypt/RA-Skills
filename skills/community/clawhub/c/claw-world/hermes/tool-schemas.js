'use strict';

function objectSchema(properties, required) {
  return {
    type: 'object',
    additionalProperties: false,
    properties: properties || {},
    required: required || []
  };
}

function stringSchema(description) {
  return { type: 'string', description };
}

function numberSchema(description) {
  return { type: 'number', description };
}

function integerSchema(description) {
  return { type: 'integer', description };
}

function booleanSchema(description) {
  return { type: 'boolean', description };
}

function buildToolSchemas() {
  return {
    env: {
      description: 'Runtime, network, and wallet check only.',
      inputSchema: objectSchema()
    },
    owned: {
      description: 'Ownership summary only.',
      inputSchema: objectSchema()
    },
    boot: {
      description: 'Full session initialization with NFA and CML context.',
      inputSchema: objectSchema({
        sessionId: stringSchema('Optional agent session id for storing the last boot snapshot.')
      })
    },
    status: {
      description: 'Read a lobster status snapshot.',
      inputSchema: objectSchema({
        tokenId: integerSchema('NFA token id.')
      }, ['tokenId'])
    },
    wallet: {
      description: 'Read wallet info from the canonical claw runtime.',
      inputSchema: objectSchema()
    },
    world: {
      description: 'Read world state from the canonical claw runtime.',
      inputSchema: objectSchema()
    },
    supply: {
      description: 'Read total minted supply.',
      inputSchema: objectSchema()
    },
    leaderboard: {
      description: 'Read leaderboard by metric.',
      inputSchema: objectSchema({
        metric: stringSchema('Optional ranking metric supported by claw leaderboard.')
      })
    },
    rank: {
      description: 'Read ranking details for an NFA.',
      inputSchema: objectSchema({
        tokenId: integerSchema('NFA token id.')
      }, ['tokenId'])
    },
    market_search: {
      description: 'Read active market listings.',
      inputSchema: objectSchema()
    },
    pk_search: {
      description: 'Read active PK matches.',
      inputSchema: objectSchema()
    },
    pk_scout: {
      description: 'Read PK opponent scout data for a match.',
      inputSchema: objectSchema({
        matchId: integerSchema('PK match id.')
      }, ['matchId'])
    },
    pk_status: {
      description: 'Read PK match status.',
      inputSchema: objectSchema({
        matchId: integerSchema('PK match id.')
      }, ['matchId'])
    },
    withdraw_status: {
      description: 'Read withdraw request status.',
      inputSchema: objectSchema({
        tokenId: integerSchema('NFA token id.')
      }, ['tokenId'])
    },
    cml_load: {
      description: 'Load CML memory for an NFA.',
      inputSchema: objectSchema({
        tokenId: integerSchema('NFA token id.'),
        full: booleanSchema('Set true to load the full cortex instead of the summary view.')
      }, ['tokenId'])
    },
    cml_save: {
      description: 'Save canonical CML memory for an NFA.',
      inputSchema: objectSchema({
        tokenId: integerSchema('NFA token id.'),
        cml: {
          type: 'object',
          description: 'Canonical CML payload to save.'
        },
        auth: stringSchema('Optional PIN/auth used for root sync.')
      }, ['tokenId', 'cml'])
    },
    session_flush: {
      description: 'Flush session hippocampus fragments back into canonical CML.',
      inputSchema: objectSchema({
        sessionId: stringSchema('Agent session id.'),
        tokenId: integerSchema('NFA token id.'),
        auth: stringSchema('Optional PIN/auth used for root sync.')
      }, ['sessionId', 'tokenId'])
    },
    task_submit: {
      description: 'Submit a completed task after explicit user confirmation through the canonical claw runtime.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        taskType: stringSchema('Task type key accepted by claw task.'),
        xp: numberSchema('XP reward amount.'),
        clw: numberSchema('CLW reward amount.'),
        score: numberSchema('Task completion score.')
      }, ['pin', 'tokenId', 'taskType', 'xp', 'clw', 'score'])
    },
    deposit: {
      description: 'Prepare a CLW deposit flow for an NFA. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        amount: stringSchema('Token amount accepted by claw deposit.')
      }, ['pin', 'tokenId', 'amount'])
    },
    fund_bnb: {
      description: 'Prepare a gas BNB funding flow for an NFA. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        amount: stringSchema('BNB amount accepted by claw fund-bnb.')
      }, ['pin', 'tokenId', 'amount'])
    },
    upkeep: {
      description: 'Run NFA upkeep after explicit user confirmation through the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.')
      }, ['pin', 'tokenId'])
    },
    transfer: {
      description: 'Prepare an ownership transfer for an NFA. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        toAddress: stringSchema('Recipient wallet address.')
      }, ['pin', 'tokenId', 'toAddress'])
    },
    market_list: {
      description: 'Prepare a fixed-price market listing. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        priceBnb: stringSchema('Listing price in BNB.')
      }, ['pin', 'tokenId', 'priceBnb'])
    },
    market_auction: {
      description: 'Prepare an auction listing. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        startPrice: stringSchema('Starting auction price in BNB.')
      }, ['pin', 'tokenId', 'startPrice'])
    },
    market_buy: {
      description: 'Prepare a fixed-price purchase request. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        listingId: integerSchema('Market listing id.'),
        priceBnb: stringSchema('Expected purchase price in BNB.')
      }, ['pin', 'listingId', 'priceBnb'])
    },
    market_bid: {
      description: 'Prepare an auction bid request. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        listingId: integerSchema('Market listing id.'),
        bidBnb: stringSchema('Bid price in BNB.')
      }, ['pin', 'listingId', 'bidBnb'])
    },
    market_cancel: {
      description: 'Cancel a market listing after explicit user confirmation through the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        listingId: integerSchema('Market listing id.')
      }, ['pin', 'listingId'])
    },
    withdraw_request: {
      description: 'Prepare a CLW withdrawal request. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        amount: stringSchema('CLW amount to withdraw.')
      }, ['pin', 'tokenId', 'amount'])
    },
    withdraw_claim: {
      description: 'Prepare a finished CLW withdrawal claim. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.')
      }, ['pin', 'tokenId'])
    },
    withdraw_cancel: {
      description: 'Cancel a pending CLW withdrawal after explicit user confirmation through the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.')
      }, ['pin', 'tokenId'])
    },
    pk_create: {
      description: 'Prepare a PK match creation flow. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        tokenId: integerSchema('NFA token id.'),
        stake: stringSchema('Stake amount accepted by claw pk-create.'),
        strategy: stringSchema('Optional strategy string for the initial commit.')
      }, ['pin', 'tokenId', 'stake'])
    },
    pk_join: {
      description: 'Prepare a PK join flow. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        matchId: integerSchema('PK match id.'),
        tokenId: integerSchema('Joining NFA token id.'),
        strategy: stringSchema('Optional strategy string for join+commit.')
      }, ['pin', 'matchId', 'tokenId'])
    },
    pk_commit: {
      description: 'Prepare a PK strategy commit. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        matchId: integerSchema('PK match id.'),
        strategy: stringSchema('Strategy string.')
      }, ['pin', 'matchId', 'strategy'])
    },
    pk_reveal: {
      description: 'Prepare a PK strategy reveal. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        matchId: integerSchema('PK match id.')
      }, ['pin', 'matchId'])
    },
    pk_settle: {
      description: 'Prepare PK settlement. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        matchId: integerSchema('PK match id.')
      }, ['pin', 'matchId'])
    },
    pk_cancel: {
      description: 'Cancel a PK match after explicit user confirmation through the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('Wallet PIN.'),
        matchId: integerSchema('PK match id.')
      }, ['pin', 'matchId'])
    },
    pk_auto_settle: {
      description: 'Prepare PK auto-settlement. Requires explicit user confirmation in the wallet.',
      inputSchema: objectSchema({
        pin: stringSchema('First wallet PIN.'),
        matchId: integerSchema('PK match id.'),
        pin2: stringSchema('Optional second wallet PIN for cross-owner matches.')
      }, ['pin', 'matchId'])
    },
    raw: {
      description: 'Developer-only claw passthrough for local debugging.',
      inputSchema: objectSchema({
        command: stringSchema('Raw claw command name.'),
        args: {
          type: 'array',
          description: 'Raw CLI arguments.',
          items: { type: 'string' }
        },
        expectJson: booleanSchema('Whether stdout should be parsed as JSON.'),
        stdin: stringSchema('Optional stdin payload passed through to claw.'),
        timeoutMs: integerSchema('Optional command timeout override in milliseconds.')
      }, ['command'])
    }
  };
}

function createToolManifest(options) {
  const settings = options || {};
  const schemas = settings.schemas || buildToolSchemas();
  const tools = settings.tools || {};
  const toolNames = Object.keys(tools).length ? Object.keys(tools) : Object.keys(schemas);

  return {
    protocol: 'openclaw-hermes-tools/v1',
    adapter: 'claw-world-hermes',
    version: settings.version || '1.1.12',
    runtime: {
      entrypoint: settings.entrypoint || 'node hermes/cli.js call <tool> [json-input]',
      manifestCommand: settings.manifestCommand || 'node hermes/cli.js manifest',
      schemaCommand: settings.schemaCommand || 'node hermes/cli.js schema <tool>'
    },
    tools: toolNames.map(function(name) {
      const schema = schemas[name] || { inputSchema: objectSchema(), description: tools[name] && tools[name].description };
      return {
        name,
        description: tools[name] && tools[name].description ? tools[name].description : schema.description || '',
        inputSchema: schema.inputSchema || objectSchema()
      };
    })
  };
}

function createOpenAiToolDescriptors(options) {
  const manifest = createToolManifest(options);
  return manifest.tools.map(function(tool) {
    return {
      type: 'function',
      function: {
        name: tool.name,
        description: tool.description,
        parameters: tool.inputSchema
      }
    };
  });
}

function createMcpToolDescriptors(options) {
  const manifest = createToolManifest(options);
  return manifest.tools.map(function(tool) {
    return {
      name: tool.name,
      description: tool.description,
      inputSchema: tool.inputSchema
    };
  });
}

module.exports = {
  buildToolSchemas,
  createToolManifest,
  createOpenAiToolDescriptors,
  createMcpToolDescriptors
};
