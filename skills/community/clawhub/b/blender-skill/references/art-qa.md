# QA：验收清单 / 缺陷分级 / Verdict

> 核验：2026-11-18

---

## 1. 缺陷分级

| 级别 | 定义 | 处置 |
|---|---|---|
| **Blocker** | 不可用：导出失败、穿模到破坏观感、命名/层级导致下游无法工作、面数超 2 倍 | 必改，不许交付 |
| **Major** | 明显可见：接缝亮线、法线翻转、材质错、scale 未应用、LOD 断链、碰撞缺失 | 必改，除非用户书面接受 |
| **Minor** | 需凑近看：小 pole、轻微 TD 偏差、个别命名不规范 | 可带 note 交付 |
| **Note** | 优化建议：可再减 5% 面、可合并一个材质 | 记录，不阻断 |

**判定原则**：宁可标 Minor 也不含糊。含糊的 QA 等于没 QA。

---

## 2. 交付前检查清单

### 2.1 场景结构
- [ ] 根 collection `COL_<Project>` 存在
- [ ] `COL_Export` 只含要交付的对象
- [ ] `COL_Reference` / `COL_Backup` / `COL_Booleans` 渲染不可见
- [ ] 无 `Collection 3` 之类默认名
- [ ] 无 `Cube.001` / `Material.002` 残留

### 2.2 几何
- [ ] 三角数在预算内（`asset_qa.py --tier` PASS）
- [ ] 无非流形边
- [ ] 无松散点/边
- [ ] 无零面积面
- [ ] 无内部冗余面（除刻意保留的厚度墙）
- [ ] 法线朝外统一
- [ ] 硬边有 bevel（LOD0）

### 2.3 变换
- [ ] 所有网格 scale = (1,1,1)
- [ ] 无负缩放
- [ ] rotation 已 apply（导出物）
- [ ] 枢轴位置符合约定（standards.md §6）

### 2.4 UV / 贴图
- [ ] 每个网格有 UV
- [ ] TD 达标且同级一致
- [ ] pack 效率 > 75%
- [ ] margin ≥ 0.002（lightmap ≥ 0.02）
- [ ] 无重叠 UV（除刻意镜像）
- [ ] 贴图命名合规
- [ ] sRGB 勾选正确

### 2.5 材质
- [ ] 材质数在预算内
- [ ] 无空材质槽
- [ ] 无 `Material.001` 残留
- [ ] 金属度非 0/1 的中间值仅出现在遮罩
- [ ] 程序化纹理已 bake

### 2.6 绑定 / 动画（如适用）
- [ ] Root 在原点，骨骼 scale = 1
- [ ] 每顶点 ≤ 4 骨骼影响
- [ ] 极端姿态无塌陷/穿插
- [ ] 动画命名 `AN_*`
- [ ] 循环动画首末帧一致

### 2.7 优化 / 导出
- [ ] LOD 链完整（LOD0..N 齐全，命名正确）
- [ ] 各 LOD 材质槽数一致
- [ ] 碰撞体命名/形状正确
- [ ] 导出参数按 optimize-export.md
- [ ] 引擎侧复验通过（导出验证矩阵）
- [ ] 交付目录含 README

---

## 3. 截图清单（验收留证）

| 必拍 | 用途 |
|---|---|
| 六视图（前/后/左/右/顶/底，正交） | 比例/剪影核对 |
| 3/4 主视角（透视，与交付用途一致） | 第一印象 |
| 细节特写 ×2（最复杂处 / 最易错处） | 证明细节 |
| 线框截图 | 拓扑证据 |
| UV 布局截图（棋盘格） | TD 证据 |
| 引擎/查看器内截图 | 导出成功证据 |
| LOD 对比图（同一视角 LOD0–3） | 优化证据 |

```python
def shot(path, cam_name=None, res=(1600, 1200)):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    if cam_name: sc.camera = bpy.data.objects[cam_name]
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
```

MCP 会话里用 `get_screenshot_of_window_as_image` 更快（非最终质量），正式留证用渲染。

---

## 4. QA Verdict 模板（复制进交付 README）

```markdown
## QA Verdict — <资产名> — <日期>

**Tier**: hero / standard / background
**审计**: asset_qa.py --tier <tier> → PASS / FAIL（附报告路径）
**统计**: <三角数> tris / <材质数> mats / <贴图总字节> / <骨骼数> bones

### 通过项
- 命名与层级：全部合规
- 面数：<x> / 预算 <y>（<z>%）
- UV：TD <x> px/m，pack 效率 <y>%
- 导出：FBX 参数按标准，引擎侧已复验（scale/朝向/法线/材质/动画/碰撞）

### 已知缺陷（附级别与是否接受）
| # | 缺陷 | 级别 | 处置 |
|---|---|---|---|
| 1 | <描述> | Minor | 接受，不影响目标视距 |

### 未覆盖/待确认
- <例如：动画未在引擎内播放验证（需程序侧配合）>

**结论**: PASS / SHIP WITH NOTES / FAIL
```

---

## 5. 常见「自我欺骗」

| 说法 | 现实 |
|---|---|
| 「看起来没问题」 | 你没在目标视距/目标光下看 |
| 「面数差不多」 | 差 30% 就是差 30%，引擎会给数字 |
| 「回头再改命名」 | 永远不会，且下游按名字写逻辑 |
| 「LOD 用 Decimate 就行」 | LOD1 用 decimate 会毁轮廓，只有 LOD2+ 可以 |
| 「引擎会自动处理缩放」 | 不会。别赌 |
| 「这个贴图应该没事」 | 打开看。9 成问题在贴图 sRGB/通道 |
| 「审计脚本报错但应该没事」 | 它报错就是有事 |
