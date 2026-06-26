# Install And Dependencies

## Repository Markers

Treat a checkout as DeepPurpose when it includes:

- `setup.py`
- `requirements.txt`
- `environment.yml`
- `DeepPurpose/`
- `DEMO/`
- `toy_data/`

## Environment Guidance

- This is an older PyTorch-era repo. The README pip example uses
  `conda create -n DeepPurpose python=3.6`.
- The bundled `environment.yml` is slightly newer and pins `python=3.7.7`,
  `pytorch=1.4.0`, `descriptastorus=2.2.0`, and notebook-era scientific stack
  packages.
- Prefer an isolated environment. If the user wants the best chance of runtime
  success on a fresh machine, the conda environment file is the safest upstream
  starting point.
- The lightweight pip path from `requirements.txt` still needs heavy packages:
  `rdkit-pypi`, `torch`, `dgllife`, `ax-platform`, `subword-nmt`, and others.
- `DeepPurpose/utils.py` also raises an explicit import error until
  `descriptastorus` and `pandas-flavor` are present.

## Practical Install Paths

README pip path:

```bash
conda create -n DeepPurpose python=3.6
conda activate DeepPurpose
conda install -c conda-forge notebook
pip install git+https://github.com/bp-kelley/descriptastorus
pip install DeepPurpose
```

Source checkout path:

```bash
conda env create -f environment.yml
conda activate DeepPurpose
jupyter notebook
```

## Validation Levels

Static checks that do not require project dependencies:

```bash
python3 setup.py --name
python3 -m compileall DeepPurpose
```

Runtime checks after the environment is ready:

```bash
python -c "from DeepPurpose import DTI, CompoundPred, DDI, PPI, ProteinPred, oneliner"
```

## Dependency Hotspots

- RDKit features drive multiple drug encodings.
- Descriptastorus is required for `rdkit_2d_normalized`.
- DGL-based encodings need `dgllife`.
- TensorBoard is imported by the DTI module.
- Notebook demos assume Jupyter is available.

## Compatibility Rules

- Do not assume current Python 3.12+ or 3.14 environments are compatible just
  because the files parse.
- If a user wants a real training or inference run, check the interpreter
  version and installed packages before promising it will work.
- If the user only wants a repo sanity check, prefer static validation over a
  full dependency install.
