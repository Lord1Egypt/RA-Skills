# Experiment Center - OpenClaw Integration Documentation

## Overview

The Experiment Center module has been successfully integrated into OpenClaw, supporting management of 4 experiment types through a conversational interface:

1. **NAE** - Nucleic Acid Extraction
2. **LP** - Library Preparation
3. **E** - Enrichment
4. **Se** - Sequencing

## Available Commands

All commands are executed through the `biolims.mjs` script.

### 1. Query Experiment Types

Query all available experiment types in the system.

```bash
node biolims.mjs experiment-types
```

**Response Example:**
```json
{
  "status": 200,
  "data": {
    "result": [
      {
        "id": "SYLX2024000001",
        "code": "NA",
        "databaseTableSuffix": "NAE",
        "experimentalTypeName": "Nucleic Acid Extraction"
      },
      ...
    ]
  }
}
```

### 2. Query Experiment Protocols

Query available experiment protocols by experiment type suffix.

```bash
node biolims.mjs experiment-protocols <suffix>
```

**Parameters:**
- `suffix`: Experiment type suffix, options: `NAE` | `LP` | `E` | `Se`

**Example:**
```bash
node biolims.mjs experiment-protocols NAE
```

**Note:** Use uppercase suffixes (NAE, LP, E, Se)

### 3. Query Experimenters

Get the list of available experimenters for the current workflow node.

```bash
node biolims.mjs experiment-experimenters <experiment_id> <suffix>
```

**Parameters:**
- `experiment_id`: Experiment order ID (pass empty string `""` when creating a new experiment)
- `suffix`: Experiment type suffix

**Example:**
```bash
node biolims.mjs experiment-experimenters "" NAE
```

### 4. Create Experiment Order

Create a new experiment order.

```bash
node biolims.mjs create-experiment '<json>'
# Or read from file
node biolims.mjs create-experiment @experiment.json
```

**Required Fields:**
- `type`: Experiment type ID
- `typeName`: Experiment type name
- `databaseTableSuffix`: Experiment type suffix (NAE/LP/E/Se)
- `experimentFlowId`: Experiment protocol ID
- `experimentFlowName`: Experiment protocol name
- `templateId`: Experiment template ID

**Optional Fields:**
- `name`: Experiment order description
- `detectionItem`: Test item ID
- `detectionItemName`: Test item name

**Example JSON:**
```json
{
  "name": "Nucleic Acid Extraction Experiment-20260211",
  "type": "SYLX2024000001",
  "typeName": "Nucleic Acid Extraction",
  "databaseTableSuffix": "NAE",
  "experimentFlowId": "ETF2026000005",
  "experimentFlowName": "DNA Extraction Standard Protocol",
  "templateId": "TPL001"
}
```

### 5. Query Experiment Order List

Query experiment order list by type.

```bash
node biolims.mjs experiment-list <suffix> [page] [rows]
```

**Parameters:**
- `suffix`: Experiment type suffix (NAE/LP/E/Se)
- `page`: Page number (optional, default 1)
- `rows`: Rows per page (optional, default 10)

**Example:**
```bash
node biolims.mjs experiment-list NAE 1 10
```

### 6. Query Experiment Details

Query detailed information of a specific experiment order.

```bash
node biolims.mjs experiment-detail <experiment_id> <suffix>
```

**Parameters:**
- `experiment_id`: Experiment order ID (e.g., NA20260018)
- `suffix`: Experiment type suffix

**Example:**
```bash
node biolims.mjs experiment-detail NA20260018 NAE
```

### 7. Save Experiment Data

Save data for the current experiment step.

```bash
node biolims.mjs experiment-save '<json>'
# Or read from file
node biolims.mjs experiment-save @experiment_data.json
```

**Required Fields:**
- `databaseTableSuffix`: Experiment type suffix
- `experimentId`: Experiment order ID
- `stepDetails`: Step data object

**Optional Fields:**
- `logArr`: Operation log object

### 8. Complete Experiment Step

Complete the current step and advance to the next workflow node.

```bash
node biolims.mjs experiment-complete-step <experiment_id> <suffix> [flow_id]
```

**Parameters:**
- `experiment_id`: Experiment order ID
- `suffix`: Experiment type suffix
- `flow_id`: Current workflow node ID (optional)

**Example:**
```bash
node biolims.mjs experiment-complete-step NA20260018 NAE
```

---

## Sample Pool Management Commands

### 9. Query Sample Pool

Query the sample pool list of samples pending assignment to experiments.

```bash
node biolims.mjs experiment-sample-pool <suffix> [experiment_id] [page] [rows]
```

**Parameters:**
- `suffix`: Experiment type suffix (NAE/LP/E/Se)
- `experiment_id`: Experiment order ID (optional)
- `page`: Page number (optional, default 1)
- `rows`: Rows per page (optional, default 10)

**Example:**
```bash
node biolims.mjs experiment-sample-pool NAE "" 1 10
```

### 10. Query Sample by Code

Search for sample information in the sample pool by sample code.

```bash
node biolims.mjs experiment-sample-pool-by-code <suffix> <sample_code>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `sample_code`: Sample code

**Example:**
```bash
node biolims.mjs experiment-sample-pool-by-code NAE S001
```

### 11. Add Samples to Experiment

Select samples from the sample pool and add them to the experiment detail table.

```bash
node biolims.mjs experiment-add-samples <suffix> <experiment_id> <sample_ids>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `experiment_id`: Experiment order ID
- `sample_ids`: Sample ID list (comma-separated)

**Example:**
```bash
node biolims.mjs experiment-add-samples NAE NA20260018 "POOL001,POOL002"
```

### 12. Remove Samples from Experiment

Remove samples from the experiment detail and return them to the sample pool.

```bash
node biolims.mjs experiment-remove-samples <suffix> <experiment_id> <sample_ids>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `experiment_id`: Experiment order ID
- `sample_ids`: Sample detail ID list (comma-separated)

**Example:**
```bash
node biolims.mjs experiment-remove-samples NAE NA20260018 "ITEM001,ITEM002"
```

### 13. Add Samples to Step

Add samples from the pending pool to an experiment step template.

```bash
node biolims.mjs experiment-add-samples-to-step <suffix> <experiment_id> <template_item_id> <sample_ids>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `experiment_id`: Experiment order ID
- `template_item_id`: Template field ID
- `sample_ids`: Sample ID list (comma-separated)

**Example:**
```bash
node biolims.mjs experiment-add-samples-to-step NAE NA20260018 TI_DETAIL_001 "POOL001,POOL002"
```

---

## Sample Mixing Commands

### 14. Mix Samples

Merge multiple samples into a single mixed sample.

```bash
node biolims.mjs experiment-mix-samples <suffix> <experiment_id> <sample_ids>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `experiment_id`: Experiment order ID
- `sample_ids`: Sample ID list to mix (comma-separated)

**Example:**
```bash
node biolims.mjs experiment-mix-samples NAE NA20260018 "SAMPLE001,SAMPLE002"
```

### 15. Cancel Sample Mixing

Cancel a sample mixing operation.

```bash
node biolims.mjs experiment-cancel-mix <suffix> <experiment_id> <sample_ids>
```

**Parameters:**
- `suffix`: Experiment type suffix
- `experiment_id`: Experiment order ID
- `sample_ids`: Sample ID list to cancel mixing (comma-separated)

**Example:**
```bash
node biolims.mjs experiment-cancel-mix NAE NA20260018 "MIX001"
```

## Using in OpenClaw

Through WhatsApp or other messaging channels, you can directly converse with OpenClaw to perform these operations:

**Example Conversation:**

```
User: Query all experiment types
Claude: Executing experiment-types command...

User: Create a nucleic acid extraction experiment
Claude:
1. First query available protocols for NAE type
2. Query available experimenters
3. Create the experiment order for you

User: View details of experiment order NA20260018
Claude: Executing experiment-detail NA20260018 NAE...
```

## Experiment Type Reference Table

| Code | Suffix | Name |
|------|--------|------|
| NA | NAE | Nucleic Acid Extraction |
| LP | LP | Library Preparation |
| E | E | Enrichment |
| Se | Se | Sequencing |

## Important Notes

1. **Suffix Case**: The `suffix` parameter in all commands must use uppercase (NAE, LP, E, Se)
2. **Authentication**: All commands automatically handle token authentication and refresh
3. **Data Format**: When creating experiments, ensure JSON format is correct; reading complex data from files is recommended
4. **Workflow Steps**: Before creating an experiment, it is recommended to first query available protocols and experimenters

## Workflow

Typical experiment creation workflow:

```
1. Query experiment types (experiment-types)
   |
2. Select experiment type, query protocols for that type (experiment-protocols)
   |
3. Query available experimenters (experiment-experimenters)
   |
4. Create experiment order (create-experiment)
   |
5. View experiment list to confirm (experiment-list)
   |
6. View experiment details (experiment-detail)
   |
7. Save experiment data (experiment-save)
   |
8. Complete experiment step (experiment-complete-step)
```

## Technical Details

### API Endpoints

All Experiment Center APIs use the following base path:
```
POST http://your-server/biolims/experimentalcenter/experiment/{endpoint}
```

### Database Table Suffix Mechanism

The system distinguishes data tables for different experiment types through the `databaseTableSuffix` parameter:
- NAE -> `t_experiment_nae`, `experiment_template_nae`, etc.
- LP -> `t_experiment_lp`, `experiment_template_lp`, etc.
- E -> `t_experiment_e`, `experiment_template_e`, etc.
- Se -> `t_experiment_se`, `experiment_template_se`, etc.

## Troubleshooting

### Issue: API returns 400 error
**Solution**: Check that `databaseTableSuffix` uses the correct uppercase format (NAE, LP, E, Se)

### Issue: Token expired
**Solution**: The script automatically refreshes the token; no manual handling is needed

### Issue: Experiment creation failed
**Solution**:
1. Confirm that the experiment type ID, protocol ID, and template ID are all valid
2. Use `experiment-types` and `experiment-protocols` commands to get the correct IDs

## Changelog

### 2026-02-12
- Added sample pool management features (7 commands)
  - experiment-sample-pool - Query sample pool
  - experiment-sample-pool-by-code - Query sample by code
  - experiment-add-samples - Add samples to experiment
  - experiment-remove-samples - Remove samples from experiment
  - experiment-add-samples-to-step - Add samples to step
  - experiment-mix-samples - Sample mixing
  - experiment-cancel-mix - Cancel sample mixing
- Improved documentation, added sample pool and mixing sections

### 2026-02-11
- Added Experiment Center features to biolims.mjs
- Support for 4 experiment types
- Implemented 8 core commands
- Test verification passed

## Contact Support

For questions or suggestions, please contact the development team.
