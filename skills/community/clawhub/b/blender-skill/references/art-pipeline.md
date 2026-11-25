# Stage 0–7 流水线与 Production Brief

> 做任何资产的主干流程。Stage 不可跳。
> 核验：2026-11-18

---

## Stage 0 — 定义（Brief 不写完不许动模型）

### Production Brief 模板（复制即用）

```markdown
## Asset Brief — <资产名>

**用途**：<玩家可交互 / 场景填充 / 过场特写 / 背景板>
**平台**：<PC 高配 / PC 主流 / 移动 / 主机 / 影视渲染>
**引擎**：<UE 5.x / Unity 6 / Godot 4 / 无（纯渲染）/ Blender 内交付>
**风格**：<写实 / 风格化 / 低模 / PSX / 卡通>（细化见 references/art-style-recipes.md）

**面数预算**：<三角数，按 standards.md §3 选表>
**贴图**：<分辨率 + 张数 + 是否共享 atlas/trim>
**纹理密度**：<px/m>
**材质数**：<上限>

**尺寸**：<宽 × 深 × 高，米>
**枢轴**：<底部中心 / 握点 / 铰链 / 地面投影>
**朝向**：<−Y 前（Blender 默认）/ 指定>

**LOD**：<需要几级 / 距离>
**碰撞**：<简单盒 / 凸包 / 逐面 / 无>
**动画**：<无 / 单一 idle / 状态机 / 骨骼数上限>

**导出**：<FBX / GLB / USD / ABC + 关键参数>
**交付目录**：<projects/<name>/out/>
**验收**：<asset_qa --tier X 全 PASS + 截图清单见 qa.md>

**已知约束**：<不能动的部分 / 必须复用的旧资产 / 授权限制>
```

### 五问定生死
1. 玩家/观众**离它多远**？→ 决定面数与贴图（10 cm 近看 vs 20 m 远景差 100 倍）
2. 会**动**吗？→ 静态可烘焙；会动要骨骼/形变，预算 ×1.5
3. 有**几个实例**？→ 大量实例必须模块化 + atlas + LOD
4. **谁**接着用？→ 交程序要干净层级与命名；交美术要可编辑拓扑
5. 什么时候**必须交**？→ 决定砍哪一档（时间不够优先砍细节层级，不砍剪影）

---

## Stage 1 — 参考

- 有参考图 → 走 `references/art-reference-match.md` 九步闭环
- 无参考图 → 至少定三件事：**剪影关键词**（3 个形容词）、**材质清单**、**色彩范围**（拿 3 个 hex）
- 建立 `COL_Reference`：人形标尺（`REF_Scale_Human`）、正/侧/顶视图平面、参考图空物体
- 参考阶段禁止建模。参考没量化就开始，Stage 5 一定返工

---

## Stage 2 — 块面（Blockout）

目标：**只解决比例与剪影**。

```
1. 建 COL_<Project> 骨架（standards.md §2）
2. 放 REF_Scale_Human（1.75 m）
3. 只用 cube/cylinder/sphere，全部 Apply Scale
4. 镜像修改器开（角色/对称物）
5. 4 个 45° 视角截图（get_screenshot_of_window_as_image）
6. 剪影过关检查：缩到 128 px 还认得出是什么？
```

判据：**128 px 缩略图能认出**。认不出 = 剪影失败，回去改比例。

禁忌：块面阶段禁止 bevel / 布尔 / 细分表面 / 材质（除临时纯色）。

---

## Stage 3 — 细化

### 细节层级（三层必须都有，且层级要拉开）
| 层 | 尺度 | 手段 | 数量 |
|---|---|---|---|
| 主形态 | > 20% 资产尺寸 | 大块切割、结构转折 | 3–7 |
| 次级 | 5–20% | 面板线、凹槽、倒角 | 10–30 |
| 微细节 | < 5% | greeble、螺栓、划痕（贴图优先） | 不限，优先贴图 |

只有主形态 = 假；全是微细节 = 噪声。

### 硬表面标准链（顺序不能乱）
```
块面 → 面板线切割 → 布尔（cutter 放 COL_Booleans，保持 live）
     → 应用 scale → 布尔后 bevel（宽度按尺寸分级）
     → Weighted Normal（keep sharp 30°）
     → 导出前才 apply modifier
```
理由：布尔后再 bevel 才能得到干净倒角；先 bevel 再布尔会产生破面与飞边。

### bevel 宽度分级
| 类型 | 宽度 | 段数 |
|---|---|---|
| 主边（视觉轮廓） | 0.005–0.02 m | 2–3 |
| 板缝 / 次级 | 0.001–0.003 m | 1–2 |
| 微细节 | 0.0005–0.001 m | 1 |

> 经验：bevel 宽度 ≈ 资产尺寸的 0.5–2%，小于 0.0005 m 在高光下等于没有。

---

## Stage 4 — 清理与 UV

```
1. merge by distance（0.0001 m）
2. 选区 → 检查非流形（Select All by Trait → Non Manifold）
3. 重算法线（Shift+N），硬边用 Weighted Normal
4. UV：Smart UV Project 起步 → 手工缝合 → pack（margin 0.002–0.01）
5. TD 校准到目标 px/m
6. 命名/层级补齐（standards.md）
7. asset_qa.py 第一次跑（几何/命名部分应已 PASS）
```

详见 `references/art-uv-texture.md`。

---

## Stage 5 — 材质 / 灯光 / lookdev

```
1. 建 master material（一个可复用图节点树，参数暴露）
2. 实例化 → 每个材质只改参数
3. 灯光：key / fill / rim 或 HDRI（见 lighting-render.md）
4. 相机：按交付用途定焦段
5. 截图比对参考，列差距 ← 这步最关键
6. 最多 3 轮收敛；3 轮还差 → 问题在几何或参考理解，不在材质
```

---

## Stage 6 — 优化

```
1. 面数审计 → 超预算先减「看不见的」：背面、内部、微 greeble
2. LOD 派生（decimate 或手工，见 optimize-export.md）
3. 碰撞体（简单盒 / 凸包）
4. 材质合并 + atlas
5. UV 二次 pack（合并后）
6. asset_qa.py --tier <tier> 全 PASS
```

---

## Stage 7 — 导出与验收

```
1. 只选 COL_Export 内的对象
2. 导出参数按 optimize-export.md 的表
3. 引擎/查看器侧复验（scale、朝向、法线、材质、动画、碰撞）
4. 截图留证（六视图 + 引擎内截图）
5. 写 QA verdict（qa.md 模板）
```

---

## 多资产组合流程

| 任务 | 流程 |
|---|---|
| 单个道具 | 0→7 直线，1 天量级 |
| 一套模块件（kit） | 先做 1 个「母版」走 0–5 → 拆成网格规格 → 其余件复用材质与 TD → 一次性 QA |
| 角色 | 0–2 剪影 → 3 高模/中模 → 重拓扑（`art-modeling.md`）→ 4 UV → 5 材质 → 绑定（`art-rig-anim.md`）→ 6 LOD → 7 导出 |
| 环境场景 | 先做尺度灰盒（Stage 2）→ 模块化拆件 → 逐件 3–7 → 组装 → 整体 QA 一次 |
| 匹配参考图镜头 | Stage 1 走九步闭环，Stage 2–5 循环比对，Stage 7 出成图 |
| 特效镜头 | `art-gn-vfx-sim.md` 先行（sim 需提前 bake），资产部分按常规 |

---

## 反模式（都会被 QA 打回）

| 反模式 | 后果 |
|---|---|
| 边做边改预算 | 前 3 天白干 |
| 场景里直接建模不建 collection | 导出选错、LOD 混乱 |
| 用 decimate 代替手工 LOD0 | 高模细节没了 |
| 材质直接改节点不建 master | 20 个材质 20 套逻辑，改不动 |
| 贴图 4k 配 100 面模型 | 浪费显存，不提升观感 |
| 忘记 apply scale 就导出 | 引擎里缩放错、物理错 |
| 靠「我记得我存了」不跑审计 | 交付日发现 40 个命名错误 |
