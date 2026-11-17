# 授权机制设计（真实数据不进 skill 包，仍可验证流程）

> 对应需求：用真实数据验证 skill 流程完整性，但每位用户花不同 → 真实数据不能嵌入 skill；
> 且需一套授权流程，让不同用户能基于各自数据**合法授权访问**。

## 核心矛盾

- skill 是**公开发布**的共享件 → 绝不能含任何用户的真实植物数据（隐私泄露 + 跨用户串味）。
- 但需**用真实数据验证** skill 全流程（建档→查今日该浇→浇水→更新 next_water→校验→备份/回滚）是否真的闭环。
- 且**每位用户的花不同**，验证数据必须来自用户本人、随用随授权。

## 三层数据分离（治本方案）

| 层 | 位置 | 内容 | 随 skill 发布？ |
|----|------|------|----------------|
| ① 代码/规则层 | `~/.workbuddy/skills/blooming-elf-v4/` | SKILL.md、scripts、references、`tests/`（仅含**合成假数据** demo 夹具） | ✅ 发布 |
| ② 用户数据层 | `~/.workbuddy/blooming-elf/` | `plants.json`（真实植物）+ `.auth`（授权记录） | ❌ **绝不发布**（在 skill 目录之外，`package_skill` 天然排除） |
| ③ 验证执行层 | `tests/e2e_check.py` 在**临时副本**上跑 | 只读②的副本，源数据零修改 | ✅ 发布（仅代码） |

> 关键：② 在 skill 目录**之外**，打包永远带不走它。skill 只持有"指向②路径的指针"，而指针（`.auth`）本身也在②里，不含任何数据本体。

## 授权流程（每位用户合法授权自己的数据）

1. **建数据**：用户（或 skill 引导）在 `~/.workbuddy/blooming-elf/plants.json` 写入本人真实植物（多实例用 `instances[]`）。
2. **显式授权**：用户说"授权我的花数据" → skill 校验路径存在 + `validate_state.py` 通过 → 写 `plants.json.auth`（与数据同目录、同名前缀）：
   ```json
   {
     "authorized_at": "2026-07-29",
     "owner": "十一一",
     "data_path": "~/.workbuddy/blooming-elf/plants.json",
     "schema_version": 4,
     "granted_by": "explicit-user-consent",
     "note": "授权 blooming-elf 读取本人真实植物数据用于流程验证"
   }
   ```
   这条 `plants.json.auth` = **用户明示同意的凭证**，是读取真实数据的唯一门票。
3. **读取**：skill / `e2e_check.py` 仅在 `.auth` 存在且 `data_path` 有效时读取真实数据；无 `.auth` → 拒绝，仅用 demo 夹具。
4. **防越权**：`e2e_check.py` 拒绝 `data_path` 落在 skill 目录内（防止误把真实数据塞进包）；路径须位于用户家目录或显式授权目录。
5. **撤销**：用户说"撤销授权" → 删 `plants.json.auth` → skill 立即失去读取资格；真实数据仍在磁盘，只是不再被读。

## 用真实数据验证流程完整性（不嵌入）

`tests/e2e_check.py` 机制：
- **默认（无参）**：用 `tests/fixtures/demo.json`（**合成假数据**，可随包发布），跑完整闭环，供发布前冒烟测试。
- **`--data <真实plants.json>`**：要求同目录有 `plants.json.auth` → 复制到**临时文件** → 在副本上模拟「今日该浇→浇水→更新 next_water→commit_state→备份/回滚」→ 断言结果 → **源文件零改动**。
- **失败用例内置**：故意构造 `next<last` → 断言 `commit_state.py` 回滚 + 退出码 1。

→ 真实数据"被用"但"不被留"：验证完即删临时副本，磁盘上真实数据始终只在②层。

## 打包安全（发布前必查）

- `package_skill.py` 只打包 skill 目录；`~/.workbuddy/blooming-elf/` 在其外 → 自动排除。
- `tests/fixtures/demo.json` 是假数据，可安全随包。
- 发布前 `pre-publish` 自检（见 CHANGELOG / P2-10）会 grep 确认包内**无** `plants.json.auth`、无真实 `plants.json`、无用户绝对路径。

## 用户侧一句话说明

> 你的花数据只存在你自己机器上的 `~/.workbuddy/blooming-elf/`，skill 发布包里没有任何你的信息；
> 只有你显式"授权"后，验证脚本才会读一份临时副本跑流程，用完即删，源数据不动。
