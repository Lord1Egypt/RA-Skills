# 绑定 / 骨骼 / 动画 / 毛发 / 布料

> 核验：2026-11-18

---

## 1. 骨骼层级（UE/Unity 兼容）

```
Root
└ pelvis
  ├ spine_01 → spine_02 → spine_03 → neck → head
  │                                ├ clavicle_l → upperarm_l → lowerarm_l → hand_l → fingers
  │                                └ clavicle_r → …
  ├ thigh_l → calf_l → foot_l → ball_l
  └ thigh_r → …
```

| 规则 | 说明 |
|---|---|
| Root 骨骼必须在原点 | 引擎的 root motion 依赖它 |
| 命名 | UE 用 `pelvis/spine_01/thigh_l`；Unity Humanoid 用 `Hips/Spine/LeftUpLeg`（按目标引擎；Humanoid 必须严格对名） |
| 骨骼数 | 角色 40–120（含手指）；移动端 ≤ 60 |
| 每顶点影响 | **≤ 4**（引擎硬限制；UE 默认 4，最多 8 需开设置） |
| 缩放 | 所有骨骼 scale = 1，不允许继承缩放 |
| 骨骼朝向 | 主骨骼 X 轴指向子骨骼（UE 习惯），导前统一 |

---

## 2. IK / FK 选择

| 部位 | 用 | 理由 |
|---|---|---|
| 手臂（手工动画） | FK | 控制细腻 |
| 手臂（交互/道具对齐） | IK | 手固定位置 |
| 腿（走路/跑） | IK | 脚必须贴地 |
| 脊柱 | FK | 需要柔顺弧线 |
| 尾巴/鞭 | 骨骼链 + FK | 甩动 |
| 面部 | FK + 形态键 | — |

IK 链必须设 `Chain Length` 与 pole target；腿部 IK 关掉 `Use IK Stretch` 除非需要。

```python
def add_ik(arm_obj, bone_name, target, pole=None, chain=2):
    pb = arm_obj.pose.bones[bone_name]
    c = pb.constraints.new('IK')
    c.target = target
    c.chain_count = chain
    if pole: c.pole_target = pole
    return c
```

---

## 3. 权重（Skinning）

| 手法 | 场景 |
|---|---|
| Automatic Weights（bone heat） | 起步，80% 情况够用 |
| Envelope | 硬表面/机械 |
| 手工刷 | 关节、面部 |
| 数据传输 | 同拓扑的多件衣服 |

### 手刷纪律
- 关节处权重**渐变**，不允许硬切（除机械）
- 膝盖内侧要有「压缩补偿」——内弯时不能塌
- 肩部三角肌区域权重向外扩一圈
- 手指每节独立，指根不带到手掌过多
- 硬表面附件（护甲）用单骨 100% 权重，不混

### 检查
```python
def check_influences(obj, limit=4):
    bad = []
    for v in obj.data.vertices:
        n = sum(1 for g in v.groups if g.weight > 1e-4)
        if n > limit: bad.append((v.index, n))
    return bad
```

---

## 4. 形态键 / 面部

- 形态键用于：表情、肌肉隆起、服装贴合、可调体型
- 命名 `Basis` / `Smile_L` / `Brow_Raise` / `Blink` …（UE 的 Morph Target 直接用这些名）
- 数量 ≤ 60（超过要合并或用骨骼）
- 形态键与骨骼可叠加，注意导出时的 shape key 选项

---

## 5. 动画

| 类型 | 帧数（30fps） |
|---|---|
| Idle 循环 | 60–120（2–4 s） |
| Walk 循环 | 24–32（0.8–1.07 s） |
| Run 循环 | 16–24（0.53–0.8 s） |
| Jump | 30–45 |
| Attack（轻） | 15–25 |
| Attack（重） | 30–50 |
| 死亡 | 45–90 |

规则：
- 帧率统一 **30 fps**（游戏动画惯例；影视 24）
- 循环动画**首末帧必须相同**（或差 1 帧由引擎 wrap）
- 关键帧插值：四肢 Bezier，机械/道具 Linear
- Root motion 与 in-place 二选一，写进 Brief
- 动作命名 `AN_<Char>_<Action>_<Variant>`，如 `AN_Hero_Walk_Fwd`

### NLA
- 每个动作一个 Action + 一个 NLA strip
- strip 命名与 Action 一致
- 导出 FBX 时选 `NLA Strips` 或 `All Actions`（UE 用后者批量导入）

---

## 6. 毛发

| 方式 | 用途 | 面数成本 |
|---|---|---|
| 卡片（hair cards） | 游戏实时 | 低（每束 8–30 面） |
| 粒子毛发（hair particles） | 渲染/影视 | 高 |
| 曲线（5.x curves） | 影视 + 新管线 | 中 |
| 几何节点毛发 | 程序化 | 中 |

游戏毛发规范：
- 卡片数：Hero 头 40–120 束；NPC 10–30
- 卡片走向跟随发流，不要平行排布
- alpha clip + 双面
- 发根深、发梢浅（顶点色或 alpha 渐变）
- 至少 2 层（底层打底，顶层破形）

---

## 7. 布料

| 方式 | 场景 |
|---|---|
| 布料模拟（Cloth modifier） | 影视、静帧 |
| 骨骼 + 权重 | 游戏实时（裙子/披风 3–6 骨） |
| 骨骼 + 弹簧（jiggle） | 简化动态 |
| 形态键 | 定死的褶皱 |

游戏布料规则：
- 骨骼数 ≤ 8（裙/披风）
- 顶点影响 ≤ 4（同身体）
- 穿模检查：跑一遍极端姿态
- 双层衣物要给内层留余量（0.005 m+）

---

## 8. 绑定验收清单

- [ ] Root 在原点，骨骼 scale = 1
- [ ] 每顶点影响 ≤ 4
- [ ] 关节弯 90°/120° 无塌陷无穿插
- [ ] IK 有 pole target，无翻转
- [ ] 手/脚有 IK 控制器与自定义形状
- [ ] 面部形态键命名规范
- [ ] 极端姿态跑过一遍（深蹲/举臂/扭头）
- [ ] 骨骼命名与目标引擎一致
- [ ] 导出 FBX 时 `Add Leaf Bones` 关、`Primary Bone Axis` 按引擎设
