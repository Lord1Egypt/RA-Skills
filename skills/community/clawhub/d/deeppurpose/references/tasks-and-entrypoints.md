# Tasks And Entrypoints

## Module Map

- `DeepPurpose/DTI.py`
  - Drug-target interaction prediction
  - Entrypoints: `model_initialize`, `model_pretrained`, `repurpose`,
    `virtual_screening`
- `DeepPurpose/CompoundPred.py`
  - Compound property prediction
  - Entrypoints: `model_initialize`, `model_pretrained`, `repurpose`
- `DeepPurpose/DDI.py`
  - Drug-drug interaction prediction
  - Entrypoints: `model_initialize`, `model_pretrained`
- `DeepPurpose/PPI.py`
  - Protein-protein interaction prediction
  - Entrypoints: `model_initialize`, `model_pretrained`
- `DeepPurpose/ProteinPred.py`
  - Protein function prediction
  - Entrypoints: `model_initialize`, `model_pretrained`
- `DeepPurpose/oneliner.py`
  - Opinionated wrappers for repurposing and virtual screening using pretrained
    or fine-tuned model bundles

## Common Pipeline

1. Load or read data.
2. Choose `drug_encoding` and, when relevant, `target_encoding`.
3. Call `data_process(...)` from `DeepPurpose.utils`.
4. Build a config with `generate_config(...)`.
5. Initialize with `model_initialize(**config)` or load with
   `model_pretrained(...)`.
6. Train with `.train(train, val, test)`, or predict with task-specific helper
   functions.

## Split Methods

From `DeepPurpose/utils.py`:

- DTI supports `random`, `cold_drug`, `cold_protein`, `HTS`,
  `repurposing_VS`, and `no_split`.
- Compound property supports `random`, `repurposing_VS`, and `no_split`.
- DDI, PPI, and protein function support `random` and `no_split`.
- `repurposing_VS` is a special no-label compatibility path used for ranking or
  screening helpers.

## Encoding Choices

Drug encodings from `README.md` and `utils.py`:

- `Morgan`
- `Pubchem`
- `Daylight`
- `rdkit_2d_normalized`
- `ESPF`
- `ErG`
- `CNN`
- `CNN_RNN`
- `Transformer`
- `MPNN`
- `DGL_GCN`
- `DGL_NeuralFP`
- `DGL_GIN_AttrMasking`
- `DGL_GIN_ContextPred`
- `DGL_AttentiveFP`

Target encodings:

- `AAC`
- `PseudoAAC`
- `Conjoint_triad`
- `Quasi-seq`
- `ESPF`
- `CNN`
- `CNN_RNN`
- `Transformer`

## Task Selection Rules

- If the user has SMILES plus protein sequences, use DTI.
- If the user only has SMILES and labels, use `CompoundPred`.
- If the user has drug pairs, use DDI.
- If the user has protein pairs, use PPI.
- If the user has protein sequences plus labels, use `ProteinPred`.
- If the user wants a fast ranking workflow over candidate drugs for a target,
  inspect `oneliner.py` and the repurposing demos first.

## Important Runtime Behaviors

- `generate_config(...)` creates `result_folder` eagerly if it does not exist.
- DTI and compound repurposing helpers write ranking tables such as
  `repurposing.txt`.
- `oneliner.py` will download pretrained model bundles or model-config bundles
  unless the caller provides `pretrained_dir`.
- `convert_y` matters for DTI regression outputs because several pretrained
  models are stored on the log scale.

## Example Starting Points

- general DTI tutorial: `Tutorial_1_DTI_Prediction.ipynb`
- compound property tutorial:
  `Tutorial_2_Drug_Property_Pred_Assay_Data.ipynb`
- dataset reading tutorial: `DEMO/load_data_tutorial.ipynb`
- one-line repurposing: `DEMO/case-study-I-Drug-Repurposing-for-3CLPro.ipynb`
- one-line custom-data repurposing:
  `DEMO/case-study-III-Drug-Repurposing-with-Customized-Data.ipynb`
- virtual screening:
  `DEMO/case-study-II-Virtual-Screening-for-BindingDB-IC50.ipynb`
