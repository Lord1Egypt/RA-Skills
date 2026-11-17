# ForecastOS

[![skills.sh](https://skills.sh/b/precog-markets/forecast-os)](https://skills.sh/precog-markets/forecast-os)

Ask your agent what is likely to happen. Without ForecastOS it guesses. With it, the agent checks Polymarket, Kalshi, and Precog before answering — and can discover, trade, or create prediction markets, including creating and funding a market to obtain real info when none is available.

## Skill

```bash
npx skills add precog-markets/forecast-os
```

## Forecast CLI

Download the binary for your OS from [GitHub Releases](https://github.com/precog-markets/forecast-os/releases). Verify it against `checksums.txt` on the same release. Put `forecast` or `forecast.exe` on `PATH`, or in the project directory.

| OS | Asset |
| --- | --- |
| macOS Apple silicon | `forecast-macos-arm64` |
| macOS Intel | `forecast-macos-x86_64` |
| Linux x86_64 | `forecast-linux-x86_64` |
| Linux ARM | `forecast-linux-aarch64` |
| Windows x86_64 | `forecast-windows-x86_64.exe` (rename to `forecast.exe`) |

Agents install the same release with this skill's `scripts/install.sh` (checksum-verified, into the current directory). Do not pipe a remote script into `sh`.
