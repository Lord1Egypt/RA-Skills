# Generic Material Parameter Template

This package does not ship with a preconfigured material system. Fill this file or a copied project-specific material database with the installing user's own measured or literature-supported parameters.

## Optical Constants

| Material | Wavelength Range | n Source | k Source | Notes |
| --- | --- | --- | --- | --- |
| `<MATERIAL_1>` | `<UNCONFIGURED>` | `<MEASURED / LITERATURE / FIT>` | `<MEASURED / LITERATURE / FIT>` | `<UNCONFIGURED>` |
| `<MATERIAL_2>` | `<UNCONFIGURED>` | `<MEASURED / LITERATURE / FIT>` | `<MEASURED / LITERATURE / FIT>` | `<UNCONFIGURED>` |

Required for optical simulations:

- wavelength grid and units
- refractive index `n(λ)`
- extinction coefficient `k(λ)` or absorption coefficient
- interpolation method
- data source and confidence level

## Semiconductor Or Transport Parameters

| Material | Eg | Electron Affinity / Work Function | Doping | Mobility | Lifetime | Relative Permittivity | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<MATERIAL_1>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` |
| `<MATERIAL_2>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` |

Required for semiconductor simulations:

- band gap or relevant energy levels
- carrier statistics model
- mobility model
- recombination model
- doping or carrier concentration
- boundary/contact assumptions
- temperature dependence when relevant

## Interface Parameters

| Interface | Parameter | Value | Source / Validation |
| --- | --- | --- | --- |
| `<INTERFACE_1>` | `<OFFSET / BARRIER / RECOMBINATION / CONTACT RESISTANCE>` | `<UNCONFIGURED>` | `<UNCONFIGURED>` |

Do not assume interface offsets or contact behavior from material names. Use measured, calculated, or literature-supported values and record the source.

## Calibration Checklist

- Compare simulated dark and illuminated curves against measured data when available.
- Report which parameters were fitted and which were fixed.
- Run sensitivity checks for uncertain parameters.
- Keep raw parameter sources with the simulation output.
