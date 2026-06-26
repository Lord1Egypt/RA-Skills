// Update experiment-sample-pool command to support dynamic experiment type query

const fs = require('fs');
const path = require('path');

const scriptPath = '/home/biolims/.openclaw/workspace/skills/biolims/scripts/biolims.mjs';
let content = fs.readFileSync(scriptPath, 'utf8');

// Old experiment-sample-pool function
const oldFunction = `  async 'experiment-sample-pool'(suffix, page = '1', rows = '10') {
    // suffix to type (experiment type ID) mapping
    const SUFFIX_TO_TYPE = {
      'HS':     'SYLX2024000015',  // Nucleic Acid Extraction New
      'WK':     'SYLX2024000014',  // Library Construction New
      'FJ1129': 'SYLX2024000017',  // Enrichment New
      'SJCX':   'SYLX2024000003'   // Sequencing on Machine
    };

    // Default flow parameters (fixed values)
    const DEFAULT_INDEX = 4;                          // Flow node index
    const DEFAULT_EXPERIMENT_FLOW_ID = 'NA20260018'; // Experiment flow ID
    const DEFAULT_FLOW = 'Activity_0zntuaw';         // Flow node ID

    if (!suffix) {
      return {
        error: 'Usage: biolims.mjs experiment-sample-pool <suffix> [page] [rows]\\n\\n' +
               'Parameters:\\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\\n' +
               '  page: Page number (optional, default 1)\\n' +
               '  rows: Rows per page (optional, default 10)\\n\\n' +
               'Supported experiment types:\\n' +
               '  NAE - Nucleic Acid Extraction\\n' +
               '  LP  - Library Preparation\\n' +
               '  E   - Enrichment\\n' +
               '  Se  - Sequencing\\n\\n' +
               'Examples:\\n' +
               '  biolims.mjs experiment-sample-pool NAE        # Query nucleic acid extraction sample pool\\n' +
               '  biolims.mjs experiment-sample-pool LP 1 50    # Query library construction sample pool'
      };
    }

    const type = SUFFIX_TO_TYPE[suffix];
    if (!type) {
      return {
        error: \`Unknown experiment type suffix: \${suffix}\\n\\nSupported suffixes: NAE, LP, E, Se\`
      };
    }

    const payload = {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {
          sortFiled: 'original_sample_code',
          isCustomed: false,
          sortOrder: 1
        },
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      databaseTableSuffix: suffix,
      type: type,
      index: DEFAULT_INDEX,
      experimentFlowId: DEFAULT_EXPERIMENT_FLOW_ID,
      flow: DEFAULT_FLOW
    };
    return await apiCall('POST', '/experimentalcenter/experiment/selectSamplePool', payload);
  },`;

// New experiment-sample-pool function
const newFunction = `  async 'experiment-sample-pool'(suffix, page = '1', rows = '10') {
    // Legacy suffix to type (experiment type ID) mapping (backward compatible)
    const SUFFIX_TO_TYPE = {
      'HS':     'SYLX2024000015',  // Nucleic Acid Extraction New
      'WK':     'SYLX2024000014',  // Library Construction New
      'FJ1129': 'SYLX2024000017',  // Enrichment New
      'SJCX':   'SYLX2024000003',  // Sequencing on Machine
      'NAE':    'SYLX2024000001',  // Nucleic Acid Extraction
      'LP':     'SYLX2024000007',  // Library Construction
      'E':      'SYLX2024000003',  // Enrichment
      'Se':     'SYLX2024000008'   // Sequencing
    };

    if (!suffix) {
      return {
        error: 'Usage: biolims.mjs experiment-sample-pool <suffix> [page] [rows]\\n\\n' +
               'Parameters:\\n' +
               '  suffix: Experiment type suffix (e.g. HS/WK/FJ1129/SJCX/Cell_Culture/Treatment etc.)\\n' +
               '  page: Page number (optional, default 1)\\n' +
               '  rows: Rows per page (optional, default 10)\\n\\n' +
               'Function: Query pending samples in the sample pool\\n\\n' +
               'Examples:\\n' +
               '  biolims.mjs experiment-sample-pool HS              # Query nucleic acid extraction sample pool\\n' +
               '  biolims.mjs experiment-sample-pool Cell_Culture    # Query cell culture sample pool\\n' +
               '  biolims.mjs experiment-sample-pool LP 1 50         # Query library construction sample pool'
      };
    }

    // 1. First query experiment type configuration to get type ID and flow info
    let type = SUFFIX_TO_TYPE[suffix];
    let experimentFlowId = 'NA20260018';
    let flow = 'Activity_0zntuaw';
    let index = 4;

    // Call experiment type configuration query API
    const configResult = await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, pagingSearchOne: {}, query: [] },
      sort: {}, pagingSearchOne: {}, query: [], tableData: [], page: 1, rows: 100, totalRecords: '0', isQuery: '1'
    });

    let typeInfo = null;
    if (configResult.status === 200 && configResult.data?.result) {
      typeInfo = configResult.data.result.find(item => item.databaseTableSuffix === suffix);
    }

    if (typeInfo) {
      // Use the queried experiment type ID
      type = typeInfo.id;  // e.g. SYLX2026000013

      // Query the flow info for this experiment type
      const flowResult = await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
        databaseTableSuffix: suffix,
        bioTechLeaguePagingQuery: { page: 1, rows: 50, sort: {}, query: [] }
      });

      if (flowResult.status === 200 && flowResult.data?.result?.length > 0) {
        const flowInfo = flowResult.data.result[0];
        if (flowInfo.experimentFlowId) {
          experimentFlowId = flowInfo.experimentFlowId;
        }
        
        // Parse flow node ID from templateId XML
        if (flowInfo.templateId) {
          try {
            const templateObj = typeof flowInfo.templateId === 'string' ? JSON.parse(flowInfo.templateId) : flowInfo.templateId;
            const renderConfig = templateObj.renderConfig || '';
            // Parse userTask id from XML
            const userTaskMatch = renderConfig.match(/<userTask[^>]+id="([^"]+)"/);
            if (userTaskMatch) {
              flow = userTaskMatch[1];
            }
          } catch (e) {
            // XML parsing failed, use default values
          }
        }
      }
    } else if (!type) {
      // Neither a known suffix nor found in configuration
      return {
        error: \`Unknown experiment type suffix: \${suffix}\\n\\n\` +
               \`Please first call experiment-type-config-list to query all available experiment type configurations.\\n\` +
               \`Supported suffix values: \${configResult.status === 200 ? configResult.data?.result?.map(i => i.databaseTableSuffix).join(', ') : 'unknown'}\`
      };
    }

    const payload = {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {
          sortFiled: 'original_sample_code',
          isCustomed: false,
          sortOrder: 1
        },
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      databaseTableSuffix: suffix,
      type: type,
      index: index,
      experimentFlowId: experimentFlowId,
      flow: flow
    };
    return await apiCall('POST', '/experimentalcenter/experiment/selectSamplePool', payload);
  },`;

if (content.includes(oldFunction)) {
  content = content.replace(oldFunction, newFunction);
  fs.writeFileSync(scriptPath, content, 'utf8');
  console.log('experiment-sample-pool function updated successfully');
} else {
  console.log('Failed to find matching old function, it may have been modified');
  console.log('Please manually check the biolims.mjs file');
}
