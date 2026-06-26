# Earth2037 Map — Single-Page Spec for AI / Skills

For **OpenClaw / LLM**: one **QM** HTTP call, **tileID ↔ (x,y)**, and QM row shapes as implemented by the live game API.

---

## 1. Plain language

- **Torus** world; each cell **(x,y)**; **tileID = VillageID = CityID** (first number per QM row).
- **Main** mapId **1**: **802×802**, **x,y ∈ [-400, 401]** after wrap (**Count=802**, not 801).
- **Mini** mapId **2**: **162×162**, **x,y ∈ [-80, 81]**.

Prefer **(x,y)** for users; use **`maps_util.py`** for conversion.

---

## 2. HTTP map fetch

```http
POST {apiBase}/game/command
{"cmd": "QM", "args": "<mapId> <x>,<y>,<w>,<h>"}
```

- **Empty `args`**: API fills **7×7 around current city** (else capital).
- Example `"1 -99,224,7,7"` — rectangle on main map (anchor/size per server).

---

## 3. QM JSON rows (variable length)

Not every cell in the rectangle is listed.

- **With user**: `[tileID, FieldType, UserID, Population, TribeID]`
- **Without user**: `[tileID, FieldType, 0, TileType]`

**FieldType** = terrain class; **TileType** = surface when unowned.

**Next calls**: **FieldType 0** → **`GETNPCCITY` + tileID** (NPC **`troops`**); farmland / city → **`TILEINFO`**.

**Wilderness / “jungle” (打野)**: Search tiles with **FieldType = 0**; use **QM** over **nearby rectangles**; for each candidate **`GETNPCCITY`** to read defenders. Estimate power / attrition using a **Lanchester square-law** style view (exchange ratios scale with squared effective strength — exact numbers are server-defined). **Clearing** wild stacks usually **grants resources**. See **`SKILL.md`** and **`march_ops.py`**.

---

## 4. FieldType cheat sheet

| Value | Notes |
|-------|--------|
| -1 | Locked |
| 0 | Oasis / wild |
| 1–7 | City-eligible fields |
| 9,10,14,15 | Trading posts |
| 11–13 | Fort / tower / base |

---

## 5. Coordinates

```bash
python3 skills/earth2037/maps_util.py 142078
python3 skills/earth2037/maps_util.py --id -99 224
```

---

## 6. ASCII

```bash
python3 skills/earth2037/maps_util.py --ascii -99 224 2
```

---

## 7. Short prompt block

```text
Earth2037 torus; main map Count=802; maps_util for coords. QM variable-length rows: 5-tuple with city, 4-tuple without.
FieldType 0 oasis; 1–7 fields; 9/10/14/15 trade; 11–13 fort/tower/base.
QM empty args = current city 7×7. Wild: FieldType 0 → GETNPCCITY for troops; QM nearby. Lanchester-style attrition; clear for resources. Builds: build_ops; march_ops; chat_ops — SKILL.md.
```

---

## 8. Skill files

| File | Role |
|------|------|
| `skills/earth2037/maps_util.py` | Coords + ASCII |
| `skills/earth2037/build_ops.py` | Build / cancel queue |
| `skills/earth2037/march_ops.py` | March |
| `skills/earth2037/chat_ops.py` | World / alliance chat |
| `skills/earth2037/SKILL.md` | Full command map |

---

## 9. Minimal ASCII example

```
      x →  -1    0    1
      +------+------+------+
y=  1 |  ·   |  ·   |  ·   |
      +------+------+------+
y=  0 |  ·   |  @   |  ·   |
      +------+------+------+
```
