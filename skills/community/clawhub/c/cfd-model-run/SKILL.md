# FNO Custom Dataset Training Assistant

## Description

Use this skill when the user wants to train, test, adapt, or run a Fourier Neural Operator (FNO) for CFD, PDE surrogate modeling, structured-grid prediction, or AI4S flow-field forecasting.

This is an action-first skill. When the skill is selected, the agent should bootstrap the ModelScope FNO codebase before giving a long explanation. The default model source is:

```text
OneScience/FNO_B
```

The first real use downloads the model code from ModelScope with `modelscope.snapshot_download`. Later uses may reuse the local ModelScope cache.

## Activation Policy

Select and use this skill when the user mentions any of these intents:

- FNO, Fourier Neural Operator, neural operator, operator learning
- CFD surrogate, flow-field prediction, pressure/velocity prediction
- PDE surrogate, Navier-Stokes, scientific AI, AI4S
- train on my data, fine-tune, adapt dataset, run inference
- structured grid, time-series field prediction, replacing a CFD solver
- ModelScope model `OneScience/FNO_B`

If the user asks a broad question such as "can you help me train an FNO", "run this CFD surrogate", "test the skill", or "use the FNO model", do not stop at conceptual advice. Start with the bootstrap step below, then continue with environment and data checks.

## Mandatory First Action

When this skill is activated, first check whether the ModelScope model code is already available. If it is not available, download it. Print the resolved local path.

Use this Python snippet unless the repo already contains an equivalent helper:

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    model_id="OneScience/FNO_B",
)
print(f"ModelScope FNO code path: {model_dir}")
```

If `modelscope` is missing, install it before retrying:

```bash
pip install modelscope
```

If the download fails because of authentication, rate limits, or restricted network access, tell the user to set `MODELSCOPE_API_TOKEN` or use an available mirror endpoint. Do not silently skip the download.

## Quick Smoke Test

After the code is downloaded, inspect the downloaded directory and verify that the expected training entry points exist:

- `train.py`
- `inference.py`
- `conf/fno.yaml`
- model and data pipeline files such as `model.py`, `fno_layers.py`, or `navier_stokes.py`

If these files exist, report that the FNO codebase is ready and continue to dependency verification.

If the user specifically asks to "test the skill", run only a lightweight smoke test:

1. Download or resolve `OneScience/FNO_B`.
2. Print the model directory.
3. List the main entry-point files.
4. Import the main dependencies if installed.

Do not start a long training job unless the user provided data and asked for training.

## Workflow

### Step 1. Bootstrap ModelScope Code

Run the mandatory first action above. This is the main conversion event from Clawhub skill use to real ModelScope model use.

### Step 2. Verify Runtime Environment

Required dependencies:

- Python >= 3.10
- PyTorch
- scipy
- ruamel.yaml
- tqdm
- matplotlib
- numpy
- modelscope

CUDA is optional. The code should detect `cuda:0` when available and fall back to CPU.

### Step 3. Discover User Data

Ask only for the missing data details needed to continue:

- data file path or directory
- grid dimensionality: 1D, 2D, or 3D
- physical channels, such as velocity, pressure, or temperature
- input time steps and target time steps
- train/test split size

The expected batch format is:

| Key | Shape | Description |
|---|---|---|
| `pos` | `(B, N, space_dim)` | Grid point coordinates |
| `x` | `(B, N, t_in * out_dim)` | Input time window flattened over the grid |
| `y` | `(B, N, t_out * out_dim)` | Prediction target flattened over the grid |

`N` is the total number of grid points: `H` for 1D, `H*W` for 2D, or `H*W*D` for 3D.

### Step 4. Adapt The Data Pipeline

Modify `NavierStokesDataset._init_data()` in `navier_stokes.py` to load the user's data and populate:

- `self.x`
- `self.y`
- `self.pos`
- `self.spatial_shape`

Then update `conf/fno.yaml`:

- `datapipe.source`
- `datapipe.data.ntrain`
- `datapipe.data.ntest`
- `datapipe.data.t_in`
- `datapipe.data.t_out`
- `datapipe.data.out_dim`
- `model.space_dim`

### Step 5. Extend To 1D Or 3D If Needed

If the downloaded code only ships `SpectralConv2d`, 1D and 3D datasets need extra model-layer work.

For 1D:

- implement `SpectralConv1d` in `fno_layers.py`
- use `torch.fft.rfft` and `torch.fft.irfft`
- replace `nn.Conv2d` pointwise layers with `nn.Conv1d`
- reshape features as `(B, C, L)`

For 3D:

- implement `SpectralConv3d` in `fno_layers.py`
- use `torch.fft.rfftn` and `torch.fft.irfftn`
- replace 2D pointwise layers with 3D equivalents
- reshape features as `(B, C, D, H, W)`

Update `conf/fno.yaml` so Fourier modes do not exceed half of the grid size in each dimension.

### Step 6. Train

Run `train.py` from the downloaded model directory after the dataset is configured.

The training loop should evaluate validation metrics such as `val_rel_l2` and `val_mse`, save the best checkpoint as `best_model.pt` under `training.output_dir`, and early-stop after `patience` epochs without improvement if supported by the downloaded code.

Common config fields:

| Parameter | Typical value | Description |
|---|---:|---|
| `training.num_epochs` | 500 | Max epochs |
| `training.lr` | 0.001 | AdamW learning rate |
| `training.teacher_forcing` | true | Use ground truth as next-step input |
| `model.hidden_channels` | 64 | Hidden feature channels |
| `model.num_layers` | 4 | Fourier layer depth |

### Step 7. Run Inference And Visualization

Run `inference.py` from the downloaded model directory after training or when a checkpoint is supplied.

Set `FNO_CHECKPOINT` to override the checkpoint path from the config if needed. Outputs should be saved under `training.output_dir`, commonly in `vis_results/`, with prediction tensors and comparison plots.

## Example User Prompts That Should Activate This Skill

- "Use FNO to train a CFD surrogate on my data."
- "Test whether the FNO skill works."
- "Download the OneScience FNO model from ModelScope and inspect it."
- "I have pressure and velocity fields on a structured grid. Train a neural operator."
- "Run inference with an FNO checkpoint."
- "Adapt the FNO model to my 3D flow dataset."

## Conversion Guidance

The Clawhub install event is not enough to count as real model use. Real use starts when the agent executes the ModelScope bootstrap step. Therefore, when this skill is selected, prefer a small concrete action over a long explanation:

1. Resolve or download `OneScience/FNO_B`.
2. Verify entry points.
3. Ask for the user's dataset only after the codebase is ready.

This keeps the skill honest: it increases real ModelScope usage only when the user actually invokes the FNO workflow.

## Notes

- The codebase should be treated as standalone unless the downloaded repository says otherwise.
- Single-device CPU or GPU execution is expected. Do not assume distributed training.
- ModelScope caching means repeated runs in the same environment may not increment visible download counts.
- Never fabricate a successful download. Report the real local path or the real error.
