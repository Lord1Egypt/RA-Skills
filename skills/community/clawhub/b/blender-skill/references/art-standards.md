# 硬规格：命名 / 层级 / 面数 / 贴图 / LOD / 单位

> 全局必读。所有数字都是**可验收阈值**，`generated/tools/asset_qa.py` 按本文件的表判定 PASS/FAIL。
> 来源：`arjun988/blender-skills` v1.3.0（MIT）的 `references/naming-conventions.md` + `polycount-budgets.md` + 各技能规格；括号内为本工作区补强（引擎实测口径、脚本化判据）。
> 最后核验：2026-11-18

---

## 1. 命名前缀（自动审计会检查）

| 类型 | 前缀 | 示例 | 审计规则 |
|---|---|---|---|
| Collection | `COL_` | `COL_Props_Hero` | 必须匹配 `^COL_[A-Za-z0-9_]+$` |
| 网格 | `SM_` | `SM_Crate_Wood_01` | `^SM_[A-Za-z0-9]+(_[A-Za-z0-9]+)+$` |
| 骨骼网格（UE 术语） | `SK_` | `SK_Hero_Body` | 角色 Armature 下网格 |
| 骨骼 | `ARM_` / `SKEL_` | `ARM_Robot_Loader` | Armature object 用 `ARM_`，UE 导出命名用 `SKEL_` |
| 材质 | `MAT_` | `MAT_Metal_Brushed` | `^MAT_[A-Za-z0-9_]+$` |
| 贴图 | `T_` | `T_Console_BC` | `^T_[A-Za-z0-9]+_(BC|N|ORM|R|M|AO|E|H)$` |
| 动画 | `AN_` | `AN_Door_Open` | Action / NLA strip 名 |
| 几何节点组 | `GN_` | `GN_Scatter_Rocks_v02` | 需要版本后缀 `_v\d{2}` |
| 相机 | `CAM_` | `CAM_Hero_Shot_01` | — |
| 灯光 | `LGT_` | `LGT_Key_Main` | — |
| 参考 | `REF_` | `REF_Scale_Human` | — |
| 碰撞 | `SM_X_COL` / `UCX_SM_X_01` | `SM_Crate_COL` | Unity 用 `_COL`，UE 用 `UCX_` 前缀 |
| 空物体 | `EMPTY_` | `EMPTY_CamTarget_Hero` | — |
| 插槽（UE） | `SOCKET_` | `SOCKET_Hand_R` | — |

**命名硬规则**
- PascalCase 词首大写 + 下划线分隔，**无空格**
- 序号必须两位：`_01` `_02`（不是 `_1`）
- 禁止默认名残留：`Cube.001` / `Material.002` / `Collection 3`（审计报 WARN，导出集合内出现按缺陷处理）
- 总长 ≤ 64 字符（引擎兼容）
- 网格名 = 材质名主体（1:1 时保持一致）

---

## 2. Collection 层级

```
COL_<Project>
├── COL_Reference       # 比例参考、正射图、人形标尺
├── COL_Blockout        # 临时块面，交付时该集合必须为空（0 对象）
├── COL_Geo
│   ├── COL_Geo_Hero
│   ├── COL_Geo_Background
│   └── COL_Geo_LOD
├── COL_Booleans        # cutter 物件（保持 live 时必须独立）
├── COL_Collision
├── COL_Lights
├── COL_Cameras
├── COL_FX
├── COL_Backup          # 破坏性操作前的副本，渲染可见性关闭
└── COL_Export          # 交付集合：只放要导出的对象
```

- **`COL_Export` 是导出的唯一入口**，不要靠「选中这些」导出。
- `COL_Backup` / `COL_Reference` / `COL_Booleans` 必须 `hide_render = True`。
- 遮挡剔除/LOD 集合按资产独立：`COL_LODs_<Asset>`。

---

## 3. 面数预算（三角面，非四边面）

### 道具
| 等级 | 三角数 | 用途 |
|---|---|---|
| Hero | 15,000–50,000 | 手持、近景可交互 |
| 标准 | 5,000–15,000 | 场景中景道具 |
| 背景 | 500–5,000 | 远景填充、杂物 |
| 极小 | 100–500 | 硬币、螺栓、碎屑 |

> 与 `references/art-modeling.md` 的道具分级（Hero 2k–8k / 标准 500–2k / 背景 100–500）**不冲突**：前者是「单件交付资产」，后者是「场景内道具」。选哪套取决于资产是否独立交付 —— **独立交付看本表，场景填充看 modeling 表**，并在 Brief 里写清用哪套。

### 角色
| 等级 | 三角数 |
|---|---|
| Hero（可玩/过场） | 50,000–100,000 |
| 标准 NPC | 20,000–40,000 |
| 群演 | 5,000–10,000 |
| 移动端 Hero | 15,000–30,000 |

### 环境
| 资产 | 三角数 |
|---|---|
| 2 m 模块墙 | 200–800 |
| 模块地砖 | 100–400 |
| 英雄建筑段 | 5,000–20,000 |
| 岩石（近景） | 1,000–5,000 |
| 树（写实） | 5,000–15,000 |
| 树（风格化/低模） | 200–2,000 |
| 草丛（每片叶） | 2–50 |

### 载具 / 武器
| 类型 | 三角数 |
|---|---|
| Hero 载具 | 80,000–200,000 |
| 可驾驶（gameplay） | 30,000–80,000 |
| 背景载具 | 5,000–15,000 |
| FPS 主武器 | 10,000–30,000 |
| TPS 武器 | 5,000–15,000 |
| 背景武器 | 500–2,000 |

### 风格修正
| 风格 | 预算调整 |
|---|---|
| Lowpoly（PS1/PS2） | −50% ~ −90% |
| PSX 恐怖 | 道具 100–800，贴图 64–256 px |
| 恐怖（稀疏） | −30% ~ −50% |
| 风格化 | 同标准，细节放贴图 |
| 写实 AAA | 取上限，LOD 强制 |

---

## 4. 贴图预算

| 资产等级 | 分辨率 |
|---|---|
| Hero | 2048–4096 |
| 标准 | 1024–2048 |
| 背景 | 512–1024 |
| 平铺面 | 1024–2048（tiling） |
| Trim sheet | 2048–4096（多资产共享） |
| 移动端 | ≤ 1024 |
| PSX 恐怖 | 64–256 |

### 纹理密度（Texel Density, px/m）

```
TD = 贴图分辨率(px) × 该 UV 岛 UV 占比 / 该岛实际世界尺寸(m)
```

| 等级 | 目标 TD |
|---|---|
| Hero | 512–1024 px/m |
| 标准 | 256–512 px/m |
| 背景 | 128–256 px/m |

同一 atlas 内所有模块**必须同 TD**。计算脚本见 `references/art-uv-texture.md`。

---

## 5. LOD

| LOD | 三角比 | 保留 | UE 屏幕尺寸（起步值） |
|---|---|---|---|
| LOD0 | 100% | 全细节 | 1.0 – 0.5 |
| LOD1 | 40–60% | 主要体块，去微 bevel / 小 greeble | 0.5 – 0.25 |
| LOD2 | 15–30% | 轮廓 | 0.25 – 0.1 |
| LOD3 | 5–10% | impostor / 卡片 / 粗糙壳 | 0.1 – 0.0 |

- 命名强制：`SM_Asset_LOD0..N`（UE 自动 LOD 靠这个名字）
- LOD0 是唯一真身；低 LOD 由它派生，不允许反向修改
- 各 LOD 材质槽数必须一致（否则引擎侧 LOD 切换会闪）
- 轮廓在目标距离上过关才算合格；blind decimate 到认不出来 = 不合格

---

## 6. 单位 / 朝向 / 枢轴

| 项 | 值 |
|---|---|
| 单位 | 1 Blender unit = 1 m（场景 Unit Scale = 1.0） |
| 导出前变换 | location 可非 0、**rotation = 0、scale = (1,1,1) 且 APPLY** |
| Blender 前向 | −Y 前 / +Z 上 |
| FBX 导出朝向 | Forward = **−Z**，Up = **Y**（默认游戏口径） |
| GLB 导出朝向 | **+Y Up** |
| UE 缩放 | 注意 UE 1 uu = 1 cm：要么模型按 1 m 建并让 FBX 单位转换处理，要么显式 ×0.01（**项目口径写死在 Brief 里，不许两边混**） |
| Unity 缩放 | 1 unit = 1 m，scale factor 1.0 |
| 枢轴 | 落地物 = 底部接触面中心；手持物 = 握点；门 = 铰链；载具 = 地面投影中心 |

### 现实尺寸对照（写实场景校验用）
| 参考物 | 尺寸 |
|---|---|
| 门高 | 2.03–2.13 m |
| 人眼高 | 1.6–1.7 m |
| 手宽 | 0.08–0.1 m |
| 砖 | 0.065 × 0.215 m |
| 汽车高 | 1.4–1.6 m |
| 天花板 | 2.4–3.5 m（机构/恐怖 2.2–2.4） |
| 走廊最小可通行 | 1.5 m（恐怖压迫 1.2–1.5） |
| 窗台高 | 0.9 m |

---

## 7. 材质数量预算

| 资产类型 | 最大材质数 |
|---|---|
| Hero 道具 | 3–5 |
| 标准道具 | 1–2 |
| 模块件 | 1（共享 atlas） |
| 角色 | 3–8（身体 / 布料 / 眼 / 发） |
| 环境模块 | 1–2 |

材质数 = draw call 数。超预算先合并材质 + 打 atlas，再谈减面。

---

## 8. 引擎专属命名

### Unreal
| 类型 | 模式 |
|---|---|
| 静态网格 | `SM_Name` |
| 骨骼网格 | `SK_Name` |
| 骨架 | `SKEL_Name` |
| LOD | `SM_Name_LOD0` … |
| 碰撞 | `UCX_SM_Name_01`（凸包，可多个）、`UBX_`（盒）、`USP_`（球）、`UCX_` 必须凸 |
| 插槽 | `SOCKET_Name` |
| 材质 | `M_Name` / 实例 `MI_Name` |

### Unity
| 类型 | 模式 |
|---|---|
| 网格 | `SM_Name` |
| 碰撞 | `SM_Name_COL` 或引擎 primitive |
| LOD Group | `SM_Name_LOD0..N` |
| 材质 | `MAT_Name` |

### Godot
- 网格 `SM_Name`；碰撞 `SM_Name_COL`；材质走 GLTF PBR 兼容（Principled）
- 层级不要冗余空节点（`EMPTY_` 只留必要的变换根）

---

## 9. 审计口径（asset_qa.py 判定）

| 检查 | 阈值 | 严重度 |
|---|---|---|
| 命名不合规 | 任一对象 | Major |
| 默认名残留（`.001` / `Cube` / `Material`） | 任一 | Major |
| Collection 缺 `COL_` 前缀 | 任一 | Minor |
| 三角数超预算 | > 预算 × 1.0 | Blocker（超 2× 直接 FAIL） |
| 三角数接近预算 | > 预算 × 0.9 | Note |
| scale ≠ 1 | 任一网格 | Major |
| 负缩放（镜像未 apply） | scale < 0 | Major |
| 无 UV | 网格有面但无 uv_layers | Blocker |
| UV 出 0–1 且无 UDIM | 任一 | Major |
| 材质槽为空 / 无材质 | 任一 | Major |
| 材质数超预算 | 见 §7 | Major |
| LOD 链断（有 LOD0 缺 LOD1） | 同名族 | Minor |
| 碰撞体缺命名 | 有 `COL_Collision` 对象但不匹配命名 | Major |
| 非流形边 | > 0 | Major |
| 松散几何（孤立点/边） | > 0 | Minor |
| 重复顶点（距离 < 1e-4） | > 0 | Minor |
| 未合并的 booleans cutter 在 Export 集合 | 任一 | Blocker |
