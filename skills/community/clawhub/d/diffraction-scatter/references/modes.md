# Mode Guide / 模式说明

| Mode / 模式 | Purpose / 用途 | Core pyFAI call |
|---|---|---|
| `radial1d` | Standard 1D radial integration / 标准 1D 径向积分 | `integrate1d_ng` |
| `azimuthal1d` | I(χ) inside a radial interval / 固定径向区间的 I(χ) | `integrate_radial` |
| `sector1d` | Sector / azimuth-window 1D profile / 扇区 1D | `integrate1d_ng(..., azimuth_range=...)` |
| `cake2d` | Full q-χ or 2θ-χ map / 完整 q-χ / 2θ-χ 图 | `integrate2d_ng` |
| `fiber2d` | GIWAXS / grazing-incidence map / GIWAXS / 纤维积分 | `FiberIntegrator.integrate2d_grazing_incidence` |

## Advanced common modes not yet scripted / 额外常见但未脚本化的高级模式

- `MultiGeometry.integrate1d()` — multi-detector fusion / 多探测器/多几何拼接
- `sigma_clip_ng()` — dynamic masking / outlier rejection / 动态 mask / 去异常值
- `pyFAI-integrate --no-gui --json` — official JSON-driven batch execution / 官方 JSON 批处理
