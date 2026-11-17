# Provenance 渠道模型（design 前置口径）

每个本地 CLI 归属恰好一个渠道；渠道是装/卸/升级的唯一路由依据，禁止绕渠道直接操作文件。

## 渠道清单与探测

| 渠道 | 探测命令（只读查询） | 升级 | 卸载 |
|------|---------------------|------|------|
| brew | `brew list --formula` / `--cask`；`brew list --versions <name>` | `brew upgrade <name>` | `brew uninstall <name>` |
| npm -g | `npm ls -g --depth=0` | `npm update -g <pkg>` / `npm i -g <pkg>@latest` | `npm uninstall -g <pkg>` |
| pnpm -g | `pnpm ls -g --depth=0` | `pnpm update -g <pkg>` | `pnpm remove -g <pkg>` |
| pipx | `pipx list --short` | `pipx upgrade <pkg>` | `pipx uninstall <pkg>` |
| uv tool | `uv tool list` | `uv tool upgrade <pkg>` | `uv tool uninstall <pkg>` |
| cargo | `cargo install --list` | `cargo install <crate>`（重装最新） | `cargo uninstall <crate>` |
| gem | `gem list`（只报可执行 gem， binstubs 抽查） | `gem update <name>` | `gem uninstall <name>` |
| apt/dnf/pacman | 包管理器 query | 渠道对应 upgrade | 渠道对应 remove |
| manual | PATH 上二进制 ∉ 上述任何渠道输出 + journal 有记录 | 重新执行安装来源 | refchain 检查 → dry-run → 确认后删 |
| system（系统自带） | PATH ∩ 系统前缀（仅 darwin：`/usr/bin` `/bin` `/sbin` `/usr/sbin`，SIP 保护） | 无（只读盘点） | **无（不可卸载）** |

## 归属判定顺序

1. 二进制 realpath 落在渠道前缀内（如 `/opt/homebrew/Cellar`、nvm/pipx/cargo bin 目录）→ 直判。
2. realpath 落在系统前缀（仅 darwin：`/usr/bin` `/bin` `/sbin` `/usr/sbin`，SIP 保护）→ `system`；Linux 上这些路径归发行版渠道判定，不特判。
3. 渠道查询输出含该名 → 归该渠道。
4. journal 有记录 → manual。
5. 其余 → manual（未记账），标记 `untracked`。

## Journal（manual 记账）

- 路径：`~/.config/cli-butler/journal.tsv`，TSV：`name\tchannel\tinstalled_at_epoch\tsource\tnote`
- F3 install 写入；F4 uninstall 删除行；行不存在视为 untracked（卸载前 refchain 必走）。

## 已知陷阱（编码为检查规则）

- system（系统自带）CLI **永不卸载**：SIP 保护本就删不掉，卸载请求直接拒绝并说明原因。
- 渠道管理的二进制**永不直接 rm**（残骸会让渠道数据库失真，升级/卸载双双报错）。
- launchd 停用只 `launchctl bootout` 不够（只注销当前会话），必须挪走 plist 并留档。
- app 内嵌软链（OrbStack 型）：本体在 .app 内，删链不删本体；挪链备份为 `.bak`。
- npm -g 前须核对 prefix（`npm prefix -g`），防 PATH 上残留旧 prefix 劫持安装位置。
