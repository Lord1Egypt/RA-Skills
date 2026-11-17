# Source registry

Registry version: `2.0`. Select exactly one row, then read only its adapter file.

| ID | Aliases | Period | Carrier | Adapter |
|---|---|---|---|---|
| `influenza_weekly` | 流感、流感周报 | week | `html_with_pdf` | [adapters/influenza-weekly.md](adapters/influenza-weekly.md) |
| `respiratory_weekly` | 急性呼吸道、哨点监测 | week | `html` | [adapters/respiratory-weekly.md](adapters/respiratory-weekly.md) |
| `covid_monthly` | 新冠、新型冠状病毒感染疫情 | month | `html` | [adapters/covid-monthly.md](adapters/covid-monthly.md) |
| `global_infectious_risk_monthly` | 全球传染病、全球风险评估 | month | `pdf` | [adapters/global-infectious-risk-monthly.md](adapters/global-infectious-risk-monthly.md) |
| `china_public_health_risk_monthly` | 重点传染病、突发公共卫生事件、中国风险评估 | month | `pdf` | [adapters/china-public-health-risk-monthly.md](adapters/china-public-health-risk-monthly.md) |

All adapters are browser-first for list/detail page access. Ordinary HTTP is page-access fallback after a recorded browser failure. Verified PDF bytes always use `scripts/download_official_document.py`.
