# Data And Pretrained Models

## Built-In Dataset Helpers

From `DeepPurpose/dataset.py` and `README.md`:

- Binding benchmark datasets:
  - `download_BindingDB()` plus `process_BindingDB()`
  - `load_process_DAVIS()`
  - `load_process_KIBA()`
- Repurposing datasets:
  - `load_antiviral_drugs()`
  - `load_broad_repurposing_hub()`
- COVID-era examples:
  - `load_AID1706_SARS_CoV_3CL()`
  - `load_SARS_CoV_Protease_3CL()`
  - `load_SARS_CoV2_Protease_3CL()`
  - `load_SARS_CoV2_RNA_polymerase()`
  - `load_SARS_CoV2_Helicase()`
  - `load_SARS_CoV2_3to5_exonuclease()`
  - `load_SARS_CoV2_endoRNAse()`

## Custom Text Formats

Use the helpers in `DeepPurpose/dataset.py` instead of hand-rolling parsers.

- Drug-target training pairs:
  `read_file_training_dataset_drug_target_pairs(path)`
  - line format: `SMILES TargetSeq Label`
- Bioassay training data:
  `read_file_training_dataset_bioassay(path)`
  - first line is the target sequence, remaining lines are `SMILES Label`
- Compound property:
  `read_file_compound_property(path)`
  - line format: `DrugName SMILES`
- Protein function:
  `read_file_protein_function(path)`
  - line format: `TargetName TargetSeq`
- Drug-drug pairs:
  `read_file_training_dataset_drug_drug_pairs(path)`
  - line format: `SMILES1 SMILES2 Label`
- Protein-protein pairs:
  `read_file_training_dataset_protein_protein_pairs(path)`
  - line format: `TargetSeq1 TargetSeq2 Label`
- Repurposing library:
  `read_file_repurposing_library(path)`
  - line format: `DrugName SMILES`
- Target sequence file:
  `read_file_target_sequence(path)`
  - line format: `TargetName TargetSeq`
- Virtual screening pairs:
  `read_file_virtual_screening_drug_target_pairs(path)`
  - line format: `SMILES TargetSeq`

## Pretrained Model Rules

- Generic pretrained loading:

```python
net = models.model_pretrained(model="MPNN_CNN_DAVIS")
```

- A local directory path also works:

```python
net = models.model_pretrained(FILE_PATH)
```

- `DeepPurpose/utils.py` downloads pretrained assets from Harvard Dataverse.
- `download_pretrained_model("pretrained_models")` and
  `download_pretrained_model("models_configs")` are bundle downloads used by
  `oneliner.py`.
- Repeated calls reuse the extracted local directory if it already exists.

## Output And Ranking Behavior

- Repurposing helpers write `repurposing.txt` plus serialized ranking outputs in
  the chosen result folder.
- `oneliner.py` creates subdirectories under `save_dir`, including downloaded
  data, per-model result folders, and aggregated results.
- Keep writable paths explicit, especially when adapting notebook examples to a
  script or agent workflow.

## Important Pitfalls

- `process_BindingDB(..., convert_to_log=True)` changes the label scale.
- For DTI pretrained models trained on DAVIS or BindingDB, tell the user when
  `convert_y` should convert between `p` and `nM`.
- `download_BindingDB()` tries to discover the current BindingDB file and falls
  back to a hard-coded `BindingDB_All_202406.tsv` URL if discovery fails.
- `oneliner.repurpose(...)` and `oneliner.virtual_screening(...)` will download
  assets automatically unless `pretrained_dir` and local inputs are provided.
- Toy files under `toy_data/` are useful for explaining formats, but they are
  not a substitute for a full dependency-ready runtime environment.
