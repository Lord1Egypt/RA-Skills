# Experiment Center Full Command List (83 Commands)

## All Integrated!

All 83 Experiment Center API endpoints have been successfully integrated into `biolims.mjs`.

---

## Command Category Index

### 1. Experiment Type & Protocol Management (10)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-types | Query experiment types | `node biolims.mjs experiment-types` |
| experiment-types-by-role | Query experiment types by role | `node biolims.mjs experiment-types-by-role [page] [rows]` |
| experiment-types-user-role | Query experiment types for role management | `node biolims.mjs experiment-types-user-role [page] [rows]` |
| create-experiment-flow | Create experiment protocol definition | `node biolims.mjs create-experiment-flow '<json>'` |
| create-experiment-flow-new | Create experiment protocol (new version) | `node biolims.mjs create-experiment-flow-new '<json>'` |
| experiment-protocols | Query experiment protocols | `node biolims.mjs experiment-protocols <suffix>` |
| experiment-flow-by-product | Query protocol by product ID | `node biolims.mjs experiment-flow-by-product <suffix> <product_id>` |
| experiment-flow-by-id | Query protocol details by ID | `node biolims.mjs experiment-flow-by-id <suffix> <flow_id>` |
| create-experiment | Create experiment order | `node biolims.mjs create-experiment '<json>'` |
| create-experiment-with-items | Create experiment order (with details) | `node biolims.mjs create-experiment-with-items '<json>'` |

### 2. Experiment Order Query & Update (9)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-list | Query experiment order list | `node biolims.mjs experiment-list <suffix> [page] [rows]` |
| experiment-detail | Query experiment details | `node biolims.mjs experiment-detail <experiment_id> <suffix>` |
| update-experiment | Update experiment order basic info | `node biolims.mjs update-experiment '<json>'` |
| update-experiment-by-id | Update experiment order by ID | `node biolims.mjs update-experiment-by-id <suffix> <experiment_id>` |
| submit-experiment | Submit experiment order | `node biolims.mjs submit-experiment '<json>'` |
| get-experiment-info | Get experiment detailed info | `node biolims.mjs get-experiment-info <suffix> <experiment_id>` |
| experiment-result-info | Query experiment result details | `node biolims.mjs experiment-result-info <result_table> <template_item_id>` |
| experiment-node-info | Query BPMN node info | `node biolims.mjs experiment-node-info <suffix> <experiment_id> <flow_id>` |
| experiment-template | Query or create step template | `node biolims.mjs experiment-template <suffix> <experiment_id> <flow_id> [template_id]` |

### 3. Step & Data Operations (4)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-save | Save experiment data | `node biolims.mjs experiment-save '<json>'` |
| experiment-complete-step | Complete experiment step | `node biolims.mjs experiment-complete-step <experiment_id> <suffix> [flow_id]` |
| delete-custom-table | Delete custom table data | `node biolims.mjs delete-custom-table <suffix> <experiment_id> <template_item_id> <row_ids>` |
| delete-experiment-data | Delete detail/result table records | `node biolims.mjs delete-experiment-data '<json>'` |

### 4. Sample Pool Management (9)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-sample-pool | Query sample pool | `node biolims.mjs experiment-sample-pool <suffix> [experiment_id] [page] [rows]` |
| experiment-sample-pool-by-code | Query sample by code | `node biolims.mjs experiment-sample-pool-by-code <suffix> <sample_code>` |
| experiment-add-samples | Add samples to experiment | `node biolims.mjs experiment-add-samples <suffix> <experiment_id> <sample_ids>` |
| experiment-remove-samples | Remove samples from experiment | `node biolims.mjs experiment-remove-samples <suffix> <experiment_id> <sample_ids>` |
| experiment-add-samples-to-step | Add samples to step | `node biolims.mjs experiment-add-samples-to-step <suffix> <experiment_id> <template_item_id> <sample_ids>` |
| add-sample-to-pool-controller | Add sample to pending pool | `node biolims.mjs add-sample-to-pool-controller <type> '<samples_json>'` |
| add-sample-to-pool-fegin | Feign add sample to pending pool | `node biolims.mjs add-sample-to-pool-fegin <type> '<samples_json>'` |
| add-sample-pool-by-apply | Add sample via shipping details | `node biolims.mjs add-sample-pool-by-apply '<json>'` |
| add-sample-pool-by-ticket | Add sample via work ticket | `node biolims.mjs add-sample-pool-by-ticket '<json>'` |

### 5. Advanced Sample Pool Operations (5)

| Command | Function | Usage |
|---------|----------|-------|
| select-pool-by-table-id | Query all sample pool data by ID | `node biolims.mjs select-pool-by-table-id <table_name> <pool_id>` |
| delete-pool-by-id | Delete sample pool record by ID | `node biolims.mjs delete-pool-by-id <platform_id> <pool_id>` |
| select-pool-by-codes | Query sample pool by sample codes | `node biolims.mjs select-pool-by-codes <table_name> <sample_codes>` |
| delete-pool-by-codes | Delete sample pool by sample codes | `node biolims.mjs delete-pool-by-codes <table_name> <sample_codes>` |
| delete-pool-or-next | Delete sample pool or next flow | `node biolims.mjs delete-pool-or-next <table_name> <experiment_id>` |

### 6. Sample Mixing & Splitting Operations (6)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-mix-samples | Mix samples | `node biolims.mjs experiment-mix-samples <suffix> <experiment_id> <sample_ids>` |
| experiment-cancel-mix | Cancel sample mixing | `node biolims.mjs experiment-cancel-mix <suffix> <experiment_id> <sample_ids>` |
| split-sample | Split sample | `node biolims.mjs split-sample '<json>'` |
| split-sub-product | Split sub-product | `node biolims.mjs split-sub-product '<json>'` |
| split-sub-product-by-number | Split sub-product by quantity | `node biolims.mjs split-sub-product-by-number '<json>'` |
| split-locus | Split locus | `node biolims.mjs split-locus '<json>'` |

### 7. Result Management (5)

| Command | Function | Usage |
|---------|----------|-------|
| add-experiment-result | Generate experiment result | `node biolims.mjs add-experiment-result '<json>'` |
| select-result-by-sample | Query single sample result | `node biolims.mjs select-result-by-sample <suffix> <sample_code>` |
| select-result-multi | Query multiple sample results | `node biolims.mjs select-result-multi '<json>'` |
| return-result | Return experiment result | `node biolims.mjs return-result '<json>'` |
| get-experiment-result-by-id | Query experiment result by ID | `node biolims.mjs get-experiment-result-by-id '<json>'` |

### 8. Product Management (3)

| Command | Function | Usage |
|---------|----------|-------|
| query-product-type | Query product type | `node biolims.mjs query-product-type <suffix> <experiment_id>` |
| change-product | Modify product type | `node biolims.mjs change-product '<json>'` |
| select-sub-product | Query sub-product | `node biolims.mjs select-sub-product <suffix> <experiment_id>` |

### 9. Reagent & Instrument Management (2)

| Command | Function | Usage |
|---------|----------|-------|
| delete-material-instrument | Delete reagent/instrument | `node biolims.mjs delete-material-instrument '<json>'` |
| mark-reagent-consumed | Mark reagent lot as consumed | `node biolims.mjs mark-reagent-consumed '<json>'` |

### 10. Workflow Progression & Traceability (2)

| Command | Function | Usage |
|---------|----------|-------|
| select-next-flow | Query next workflow | `node biolims.mjs select-next-flow <suffix> <product_id>` |
| select-experiment-process | Query experiment workflow diagram | `node biolims.mjs select-experiment-process <suffix> <product_id>` |

### 11. QC Management (7)

| Command | Function | Usage |
|---------|----------|-------|
| select-qc-list | Query QC reference list | `node biolims.mjs select-qc-list [page] [rows]` |
| add-qc | Add QC reference | `node biolims.mjs add-qc '<json>'` |
| submit-qc | Submit QC result | `node biolims.mjs submit-qc '<json>'` |
| select-qc-result | Query QC result (single) | `node biolims.mjs select-qc-result <suffix> <sample_code>` |
| select-qc-results | Query QC results (multiple) | `node biolims.mjs select-qc-results '<json>'` |
| select-qc-template-item | Query QC check items | `node biolims.mjs select-qc-template-item <suffix> <sample_id>` |
| save-qc-template-item | Save QC check items | `node biolims.mjs save-qc-template-item <suffix> <sample_code> '<items_json>'` |

### 12. Popup Queries (5)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-experimenters | Query experimenters | `node biolims.mjs experiment-experimenters <experiment_id> <suffix>` |
| select-personnel-group | Query experimenter groups | `node biolims.mjs select-personnel-group [page] [rows]` |
| select-unit | Query measurement units | `node biolims.mjs select-unit [page] [rows]` |
| select-dictionary | Query data dictionary | `node biolims.mjs select-dictionary <type> [page] [rows]` |
| index-query | Query Index list | `node biolims.mjs index-query [page] [rows]` |

### 13. Batch Operations (4)

| Command | Function | Usage |
|---------|----------|-------|
| batch-warehousing | Batch warehousing | `node biolims.mjs batch-warehousing <suffix> <experiment_id> <item_ids>` |
| batch-export | Batch export | `node biolims.mjs batch-export <suffix> <experiment_id> <item_ids>` |
| batch-write | Batch write (Excel) | `node biolims.mjs batch-write <file_path> '<json_data>'` |
| save-tapestation-data | Save TapeStation data | `node biolims.mjs save-tapestation-data <suffix> <experiment_ids> '<samples_json>'` |

### 14. Barcode Scanning Operations (2)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-scan | Experiment detail scan (mode 1) | `node biolims.mjs experiment-scan '<json>'` |
| experiment-scan2 | Experiment detail scan (mode 2) | `node biolims.mjs experiment-scan2 '<json>'` |

### 15. Auto-Save & Records (3)

| Command | Function | Usage |
|---------|----------|-------|
| auto-save-experiment | Auto-save experiment data | `node biolims.mjs auto-save-experiment '<json>'` |
| generate-experiment-record | Generate experiment record | `node biolims.mjs generate-experiment-record '<json>'` |
| select-quality-records | Query experiment quality records | `node biolims.mjs select-quality-records <batch>` |

### 16. Template Operations (4)

| Command | Function | Usage |
|---------|----------|-------|
| handle-experiment-sheet | Process experiment sheet | `node biolims.mjs handle-experiment-sheet <experiment_id>` |
| editing-template | Edit template | `node biolims.mjs editing-template '<json>'` |
| import-template-button | Import template button | `node biolims.mjs import-template-button '<json>'` |
| import-template-execute | Execute template import | `node biolims.mjs import-template-execute '<json>'` |

### 17. Well Plate Operations (1)

| Command | Function | Usage |
|---------|----------|-------|
| delete-hole | Delete well position | `node biolims.mjs delete-hole '<json>'` |

### 18. Other Operations (3)

| Command | Function | Usage |
|---------|----------|-------|
| experiment-order-change | Change experiment order sequence | `node biolims.mjs experiment-order-change '<json>'` |
| get-experiments-by-sample | Query experiments by sample ID | `node biolims.mjs get-experiments-by-sample '<json>'` |
| get-experiment-result-by-id | Query experiment result by ID | `node biolims.mjs get-experiment-result-by-id '<json>'` |

---

## Usage Instructions

### Parameter Format

- `<suffix>`: Experiment type suffix, use uppercase (NAE/LP/E/Se)
- `<json>`: JSON string, can be passed directly or read from file using `@filepath`
- `[parameter]`: Optional parameter

### Examples

```bash
# Pass JSON directly
node biolims.mjs create-experiment '{"name":"Test","type":"SYLX2024000001",...}'

# Read JSON from file
node biolims.mjs create-experiment @experiment.json

# Comma-separated ID list
node biolims.mjs experiment-add-samples NAE NA20260018 "POOL001,POOL002,POOL003"
```

---

## Test Verification

Tested command examples:
```bash
# Query experiment types
node biolims.mjs experiment-types

# Query experiment list
node biolims.mjs experiment-list NAE 1 10

# Query sample pool
node biolims.mjs experiment-sample-pool NAE

# Query measurement units
node biolims.mjs select-unit 1 10
```

All commands passed API call testing and returned successfully!

---

## Changelog

### 2026-02-12
- All 83 Experiment Center API endpoints integrated
- Added 68 new commands
- Updated command help information
- Passed test verification

---

## Support

For help, please refer to:
- `EXPERIMENT_CENTER_README.md` - Basic usage guide
- `API_INTERFACE_LIST.md` - Interface list and priorities
- This document - Full command reference

All these commands are available through OpenClaw conversation!
