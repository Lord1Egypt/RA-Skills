# Experiment Center API Interface List

Based on ExperimentCenterNAE_Module_Design_Document.html documentation

## Interface Classification Statistics

### Integrated Interfaces (15) - Done

**Basic Operations (8):**
1. selectPopupsExperimentType - Query experiment types
2. selectExperimentFlow - Query experiment protocols
3. selectnodeexperimenter - Query experimenters
4. addExperimentFlowMain - Create experiment order
5. selectExperimentFlowMain - Query experiment list
6. selectExperimentById - Query experiment details
7. updateExperimentFlow - Save experiment data
8. updateExperimentFlowNext - Complete experiment step

**Sample Pool Management (5):**
9. selectSamplePool - Query sample pool
10. selectSamplePoolBySampleCode - Query sample by code
11. updateSamplePool - Add sample to experiment
12. deleteSamplePool - Remove sample from experiment
13. addExperimentSamplePool - Add sample to step

**Sample Mixing Operations (2):**
14. mixSample - Mix samples
15. cancelMaxSample - Cancel sample mixing

---

## Pending Integration Interfaces (68)

### 5.1.1 Experiment Type & Protocol Management (remaining 7)

16. selectPopupsExperimentTypeByRole - Query experiment types by role
17. selectPopupsExperimentTypeUserRole - Query experiment types for role management
18. addExperimentFlow - Create experiment protocol definition
19. addExperimentFlowNew - Create experiment protocol (new version)
20. selectExperimentFlowByProductId - Query protocol by product ID
21. selectExperimentFlowById - Query protocol details by ID
22. addExperimentFlowMainAndItems - Create experiment order (with details)

### 5.1.2 Experiment Order Information Query (remaining 7)

23. updateExperiment - Update experiment order basic info
24. updateExperimentById - Update experiment order by ID
25. submit - Submit experiment order
26. getExperimentInfo - Get experiment detailed info
27. selectExperimentResultInfo - Query experiment result details
28. selectNodeInfo - Query BPMN node info
29. selectOrAddExperimentFlowTemplate - Query or create step template

### 5.1.3 Step Template & Component Management (remaining 1)

30. deleteCustomTableData - Delete custom table data

### 5.1.4 Sample Pool Management (remaining 4)

31. addSampleToSamplePoolController - Add sample to pending pool (internal API)
32. addSampleToSamplePoolFegin - Feign add sample to pending pool
33. addExperimentSamplePoolBySampleApplyItems - Add sample via shipping details
34. addExperimentSamplePoolByTicket - Add sample via work ticket

### 5.1.5 Result Management (remaining 5)

35. addExperimentResult - Generate experiment result
36. selectresultTableData - Query single sample result
37. selectresultTableDatas - Query multiple sample results
38. delete - Delete detail/result table records
39. returnResult - Return experiment result

### 5.1.6 Sample Mixing & Splitting Operations (remaining 4)

40. split - Split sample
41. splitSubProduct - Split sub-product
42. splitSubProductByNumber - Split sub-product by quantity
43. splitLocus - Split locus

### 5.1.7 Product Management (remaining 3)

44. queryProductType - Query product type
45. changeProduct - Modify product type
46. selectziProduct - Query sub-product

### 5.1.8 Reagent & Instrument Management (remaining 2)

47. deleteMaterialAndInstrument - Delete reagent/instrument
48. markReagentLotConsumed - Mark reagent lot as consumed

### 5.1.9 Workflow Progression & Traceability (remaining 2)

49. selectNextFlow - Query next workflow
50. selectExperimentProcess - Query experiment workflow diagram

### 5.1.10 Advanced Sample Pool Operations (remaining 5)

51. selectAllByPoolTableId - Query all sample pool data by ID
52. delExperimentPoolById - Delete sample pool record by ID
53. selExperimentPoolBySampleCodes - Query sample pool by sample codes
54. delExperimentPoolBySampleCodes - Delete sample pool by sample codes
55. delExperimentPoolOrnextById - Delete sample pool or next flow

### 5.1.11 QC Management (remaining 6)

56. selectPopupsQualityControl - Query QC reference list
57. addQualityControl - Add QC reference
58. submitQualityControl - Submit QC result
59. selectQualityResultTableData - Query QC result (single)
60. selectQualityResultTableDatas - Query QC results (multiple)
61. selectQualitycenterExperimentTemplateItemBySampleId - Query QC check items
62. saveQualitycenterExperimentTemplateItemBySampleId - Save QC check items

### 5.1.12 Popup Queries (remaining 3)

63. selectPopupsPersonnelGroup - Query experimenter groups
64. selectUnit - Query measurement units
65. selectDictionary - Query data dictionary
66. indexQuery - Query Index list

### 5.1.13 Batch Operations (remaining 4)

67. batchWarehousing - Batch warehousing
68. batchExport - Batch export
69. batchWrite - Batch write (Excel)
70. saveTapeStationData - Save TapeStation data

### 5.1.14 Barcode Scanning Operations (remaining 2)

71. ExperimentDetailScan - Experiment detail scan (mode 1)
72. ExperimentDetailScan2 - Experiment detail scan (mode 2)

### 5.1.15 Auto-Save & Records (remaining 3)

73. autoSave - Auto-save experiment data
74. generateExperimentalRecord - Generate experiment record
75. selectExperimentQualityRecords - Query experiment quality records

### 5.1.16 Template Operations (remaining 4)

76. handleexperimentsheet - Process experiment sheet
77. editingTemplate - Edit template
78. importTemplateButton - Import template button
79. importTemplateButton/importTemplate - Execute template import

### 5.1.17 Well Plate Operations (remaining 1)

80. deleteHole - Delete well position

### 5.1.18 Other Operations (remaining 3)

81. experimentOrderChange - Change experiment order sequence
82. getExperimentsBySampleId - Query experiments by sample ID
83. getExperimentResultById - Query experiment result by ID

---

## Integration Priority Recommendations

### High Priority (Core Features)
- Result Management (5) - Generate and query experiment results
- Step Template Management (1) - Delete custom table data
- Workflow Progression (2) - Query next workflow, workflow diagram
- Product Management (3) - Query and modify products

### Medium Priority (Common Features)
- QC Management (6) - QC references and QC results
- Splitting Operations (4) - Sample and product splitting
- Batch Operations (4) - Batch warehousing, export, import
- Popup Queries (4) - Personnel groups, units, dictionary, Index

### Low Priority (Auxiliary Features)
- Advanced Sample Pool Operations (5)
- Reagent & Instrument Management (2)
- Barcode Scanning Operations (2)
- Auto-Save (3)
- Template Operations (4)
- Well Plate Operations (1)
- Other Operations (3)

---

## Recommended Integration Approach

**Option 1: Full Integration**
- Add all 83 interfaces at once
- High workload, but most complete functionality
- Estimated 2-3 hours

**Option 2: Phased Integration**
- Phase 1: High priority (11 interfaces)
- Phase 2: Medium priority (18 interfaces)
- Phase 3: Low priority (39 interfaces)
- Can be added incrementally based on actual usage needs

**Option 3: On-Demand Integration**
- You tell me which features you currently need most
- I prioritize integrating those interfaces
- Most flexible, but requires you to specify requirements

---

**Which approach would you prefer?**
