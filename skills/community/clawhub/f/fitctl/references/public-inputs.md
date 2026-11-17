# Public examples and licensing

The skill instructions and Python helper scripts are distributed under MIT-0
(see `LICENSE`). The fitctl CLI, core, Python bindings, and their upstream
example data are separate projects with their own licenses. Installing or
calling them does not change their licenses.

## Source of the example data

The example scripts download inputs from the public fitctl v0.8.0 revision
`1ec8777d69525b6037fa2654d084cddcf61e3c62`:

- [Survey fixture corpus](https://github.com/tznurmin/fitctl/tree/v0.8.0/fixtures/host_survey)
- [State fixture corpus](https://github.com/tznurmin/fitctl/tree/v0.8.0/fixtures/host_state)
- [Policy](https://github.com/tznurmin/fitctl/blob/v0.8.0/configs/policy/general_compute_default.v1.json)
- [Service profiles](https://github.com/tznurmin/fitctl/tree/v0.8.0/configs/service_profiles)
- [Upstream Apache-2.0 license](https://github.com/tznurmin/fitctl/blob/v0.8.0/LICENSE)

Those upstream files are not distributed in this skill. Downloaded copies
retain their upstream licensing; do not include the cache in a skill upload
or describe its contents as MIT-0.

The three task scripts (`scripts/observe.py`, `examples/run_fixtures.py`, and
`examples/run_advanced_python.py`) are skill utilities that call the installed
Python API. They are not part of either native package. The small
`examples/_public_inputs.py` helper downloads and verifies the input files.
The thermal-provider JSON under `examples/inputs/` is a configuration
example written for this skill, not a copied upstream file; its provider
kinds and commands mirror the provider behavior fitctl documents (and the
core's built-in local provider definitions expose the same `sensors -j`
and `nvidia-smi --query-gpu=...` shapes). Treat it as an example to adapt
per host, not as a canonical upstream artifact.

## Run the examples

Run from a workspace where reports and a cache may be written:

```bash
<fitctl-py> <skill-dir>/examples/run_fixtures.py --out reports/fixtures
<fitctl-py> <skill-dir>/examples/run_advanced_python.py --out reports/advanced
```

The first run downloads eleven files over HTTPS from
`raw.githubusercontent.com`. Each request has a 20-second timeout and a
1 MiB size limit. Files are checked against the SHA-256 values in
`examples/_public_inputs.py`, then cached under
`.cache/fitctl-skill/<revision>/` relative to the working directory. This is
a selected input set for these examples; the upstream corpus manifests also
name other fixtures, which these scripts do not request.

Use `--cache-dir /path/to/cache` to choose another location. The scripts
reject a cache inside the skill directory. A populated, valid cache works
offline. A missing file requires a download; a download, permissions, or
integrity error exits unsuccessfully as an operational error. It never
becomes a fit/unfit verdict. A cache mismatch requires inspecting the
affected file before deliberately removing it and fetching a fresh copy.

Do not execute downloaded input files: they are JSON data. Live survey,
state, and monitoring workflows do not use this input download path.

## Related public Python examples

The published Python repository documents the same APIs:

- [Recorded decisions, redaction, and semantic identity](https://github.com/tznurmin/fitctl-python/blob/v0.1.1/docs/recorded.md)
- [Batch comparison](https://github.com/tznurmin/fitctl-python/blob/v0.1.1/docs/batch.md)
- [Collection and replay](https://github.com/tznurmin/fitctl-python/blob/v0.1.1/docs/collection.md)

These are reference documentation, not alternate download locations for the
skill's helper scripts.
