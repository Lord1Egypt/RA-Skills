# Earth2037 地图 — 给 AI / Skill 的单页说明

本文档面向 **OpenClaw / LLM**：一次 HTTP 拉 **QM**，以及 **tileID ↔ (x,y)**、**QM 返回数组** 的约定（与线上游戏服一致）。

---

## 1. 地图是什么（人话）

- **环面**：走出一边从对边折回。
- 每格 **(x,y)** 整数坐标；**tileID = VillageID = CityID**（QM 每行第一个数）。
- **主图** mapId **1**：每轴 **802** 格（**802×802**），**x、y ∈ [-400, 401]**（环绕后）。行宽常记 **Count=802**（不要用 801）。
- **小图** mapId **2**：**162×162**，**x、y ∈ [-80, 81]**。

对玩家以 **(x,y)** 为主；**maps_util.py** 做 ID 换算。

---

## 2. 单次 HTTP 拉地图块

```http
POST {apiBase}/game/command
Authorization: Bearer <token>
Content-Type: application/json

{"cmd": "QM", "args": "<mapId> <x>,<y>,<w>,<h>"}
```

- **`args` 为空**：游戏 API 会补成 **当前城为中心、主图 7×7**（无「当前城」则用主城）。
- 带参示例：`"1 -99,224,7,7"` 为主图一片矩形（左上角 / 宽高以游戏服解析为准）。

返回 `data` 中含 `/svr qm …` 及地块 JSON 数组。

---

## 3. QM 返回中的地块数组（不定长）

矩形内**不是**每格都有一行；仅满足**游戏过滤规则**的格会输出。

- **有用户**：`[tileID, FieldType, UserID, Population, TribeID]`（5 个数）
- **无用户**：`[tileID, FieldType, 0, TileType]`（4 个数）

常见情况：**FieldType 1～7** 且无城、且地表为某种「空草地」时，整格可能**不返回**（省流量）；**有城的格**仍会返回。

**FieldType**：绿洲/田型/贸易站等；**TileType** 在无城行里表示**地表样式**。

**看单格下一步**：**FieldType=0**（绿洲/野地）→ **`GETNPCCITY` + tileID**（看 **NPC 兵力**）；**田型 / 玩家城** → **`TILEINFO` + tileID**。

**打野**：在 **FieldType=0** 的 tile 上搜索；用 **QM** 扫**邻近地图**，对每个候选格 **`GETNPCCITY`** 查兵；战力与战损可按 **兰开斯特平方律** 粗估；歼敌后通常**获得资源**。详见 **`SKILL.md`** 与 **`march_ops.py`**。

---

## 4. FieldType 语义摘要

命名如 **F6W5C3I4**：**F** 雷岩、**W** 净水、**C** 油田、**I** 矿山（建城后资源格分布，细节以游戏为准）。

| 值 | 说明 |
|----|------|
| -1 | 锁定 |
| 0 | **绿洲** / 野地 |
| 1～7 | 可建城田型（多种 6/9/12/18 田） |
| 9,10,14,15 | 贸易站 |
| 11 | 要塞 |
| 12 | 塔 |
| 13 | 基地 |

---

## 5. 坐标换算

```bash
python3 skills/earth2037-game/maps_util.py 142078
python3 skills/earth2037-game/maps_util.py --id -99 224
```

---

## 6. ASCII 线框

```bash
python3 skills/earth2037-game/maps_util.py --ascii -99 224 2
python3 skills/earth2037-game/maps_util.py --ascii-tile 142078 3
```

**与服端 QM 一致的地块图**（需 `EARTH2037_TOKEN` 或 `config.json` 的 token；先 `2037.py bootstrap` 更佳）：

```bash
python3 skills/earth2037-game/maps_util.py qm                    # args 空 = 当前城 7×7
python3 skills/earth2037-game/maps_util.py qm -a "1 -99,224,9,9"   # 主图矩形
```

`--help` 走 argparse，不会再把 `--help` 当成 tileID。

行 = **y**（上行 y 更大），列 = **x** 右增。

---

## 7. 短指令（system prompt）

```text
地球2037环面图；主图 Count=802，maps_util 换坐标。QM 不定长。FieldType 0=野地：打野先筛 0 再 GETNPCCITY 看兵力，QM 扫邻近；战损可兰开斯特平方律粗估，歼敌有资源。建造 GETBUILDCOST+ADDBUILDQUEUE（build_ops）；出征 march_ops；聊天 chat_ops。详见 SKILL.md。
```

---

## 8. 相关文件（Skill 侧）

| 文件 | 作用 |
|------|------|
| `skills/earth2037-game/maps_util.py` | 坐标 + ASCII；`maps_util.py qm` 拉 QM 并按 FieldType 画格 |
| `skills/earth2037-game/build_ops.py` | 升级 / 取消队列 |
| `skills/earth2037-game/march_ops.py` | 出征 |
| `skills/earth2037-game/chat_ops.py` | 世界/联盟聊天 |
| `skills/earth2037-game/SKILL.md` | 完整命令与 HTTP 约定 |

---

## 9. 示意

```
      x →  -1    0    1
      +------+------+------+
y=  1 |  ·   |  ·   |  ·   |
      +------+------+------+
y=  0 |  ·   |  @   |  ·   |   @ = 中心 (x,y)
      +------+------+------+
```
