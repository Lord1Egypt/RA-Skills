# 绊线（检测线）交互工作流

**导航：** 返回 [SKILL.md](./SKILL.md) | 类型定义 [types-guide.md](./types-guide.md)

> 当用户需要为穿越检测定义绊线时，遵循此交互工作流。

## 核心概念

- **p1→p2** 主检测线（用户定义，2 个点）
- **p3→p4** A-B 区域标记（系统自动生成或用户定义）
- **方向** Forward/Backward/TwoWay（要检测的方向）

**自动生成过程**：用户只需指定 p1 和 p2 点。系统会自动生成垂直于主线的 p3 和 p4 点用于预览和确认。

矢量穿越检测算法详情，见 [types-guide.md#tripwire](./types-guide.md#tripwire)

## 工作流步骤

### 第 1 步：生成网格参考

```bash
node scripts/show-grid.mjs <image> <output-grid.png>
```

### 第 2 步：用户指定绊线

"查看网格，检测线应该在哪里？例如，从 B2 到 G2？"

### 第 3 步：预览绊线位置

系统基于用户的 2 个点（p1、p2）生成完整的 4 点结构，然后调用 `visualize.mjs` 生成预览：

```bash
# 自动计算 4 个点后
node scripts/visualize.mjs <image> '[]' preview.png \
  --overlays '[{
    "kind":"TripWire",
    "name":"tripwire preview",
    "direction":"Forward",
    "points":[p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,p4_x,p4_y]
  }]'
```

预览显示：
- 主线（p1→p2）虚线 - 橙色
- A/B 标记（p3→p4）虚线 - 橙色，带标签
- 方向箭头 - Forward=绿色在 p4，Backward=红色在 p3

### 第 4 步：确认 A/B 区域

"查看预览图像：
- A 区在这一侧（例如线的上方）
- B 区在那一侧（例如线的下方）
- 绿色箭头显示 Forward 是 A→B

这是否正确？"

### 第 5 步：选择方向模式

用户看到预览后，提问：
- Forward（相同方向）
- Backward（相反方向）
- TwoWay（检测两个方向）

### 第 6 步：最终确认

生成最终预览，用户确认，然后调用技能：

```bash
echo '{"input0":{"image":"photo.jpg","tripwire":{"id":"1","name":"line","kind":"TripWire","points":[p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,p4_x,p4_y],"direction":"Forward"}}}' | \
  node scripts/invoke.mjs ep-xxxx-yyyy
```

---

## 常见错误

❌ 不要在显示预览前解释 A/B
✅ 用户必须看到带 A/B 标记标签的预览

❌ 不要仅使用 2 个点
✅ 始终提供 4 个点（主线 + A/B 标记）

❌ 不要跳过预览验证
✅ 始终显示预览以确认

---

## 完整对话示例

**用户**："我需要检测进入门的人员"

**你**：
1. 生成网格：
```bash
node scripts/show-grid.mjs door-camera.jpg door-grid.png
```

2. 问："查看网格，检测线应该在哪里？例如 B2 到 G2？"

3. 用户："是的，从 B2 到 G2 的线"

4. 生成显示绊线位置和 A/B 标记的预览：
```bash
node scripts/visualize.mjs door-camera.jpg '[]' preview1.png \
  --overlays '[{"kind":"TripWire","name":"door","direction":"Forward","points":[B2_x,B2_y,G2_x,G2_y,B1_x,B1_y,G3_x,G3_y]}]'
```

5. 解释："这是绊线预览：
   - 区域 'A' 在线上方（外侧）
   - 区域 'B' 在线下方（内侧）
   - 绿色箭头显示 Forward 检测 A→B（从外侧进入）

   你对这个设置满意吗？"

6. 用户："是的，我想检测进入（Forward）"

7. 生成最终预览以确认

8. 调用技能进行检测

---

## 数据结构

详见 [types-guide.md#tripwire](./types-guide.md#tripwire) 了解完整的定义、矢量算法和示例。
