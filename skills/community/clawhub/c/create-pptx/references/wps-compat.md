# WPS 兼容性踩坑记录

## 结论（先看这里）

**WPS 不可靠地支持 PowerPoint 的 click-triggered 动画。**

最安全的解决方案：**用多张幻灯片替代动画**，每张幻灯片叠加一层内容，
配合淡入过渡（fade transition），视觉效果几乎等同于动画。

---

## 踩过的坑（2025-03 实测）

### 坑 1：`presetClass="entr"` 不自动隐藏形状

**PowerPoint 行为**：带入场动画（`presetClass="entr"`）的形状，在演示模式下会自动隐藏，
直到动画触发时才显示。

**WPS 行为**：WPS 忽略这个约定，所有形状在幻灯片打开时就全部可见，动画完全失效。

**尝试过的修复**：在 `<p:timing>` 里插入显式的 `style.visibility=hidden` 初始块：

```xml
<p:par>
  <p:cTn id="..." fill="hold">
    <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    <p:tnLst>
      <p:set>
        <p:cBhvr>
          <p:cTn id="..." dur="1" fill="hold"/>
          <p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>
          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
        </p:cBhvr>
        <p:to><p:strVal val="hidden"/></p:to>
      </p:set>
    </p:tnLst>
  </p:cTn>
</p:par>
```

**结果**：WPS 同样不支持 `style.visibility` 属性动画，形状依然全部可见。

### 坑 2：`delay="indefinite"` click group 结构

正确的 click-triggered 序列 XML 结构（仅在真正的 PowerPoint 中有效）：

```xml
<p:seq concurrent="1" nextAc="seek">
  <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
    <p:tnLst>
      <!-- Click group 1 -->
      <p:par>
        <p:cTn id="..." fill="hold">
          <p:stCondLst><p:cond evt="onBegin" delay="indefinite"/></p:stCondLst>
          <p:tnLst>
            <!-- staggered shape animations -->
          </p:tnLst>
        </p:cTn>
      </p:par>
      <!-- Click group 2 -->
      <p:par>...</p:par>
    </p:tnLst>
  </p:cTn>
  <p:prevCondLst><p:cond evt="onPrevClick" delay="0"/></p:prevCondLst>
  <p:nextCondLst><p:cond evt="onNextClick" delay="0"/></p:nextCondLst>
</p:seq>
```

WPS 对 `delay="indefinite"` 的处理不正确，所有 click group 会在打开时立即执行。

### 坑 3：`<p:bldLst>` 不影响实际显示

加了 `<p:bldLst>` 让 PP/WPS 知道哪些形状有动画，但这对 WPS 的可见性行为没有影响。

---

## 最终可靠方案

### 多幻灯片 + 淡入过渡

```python
from pptx_helpers import add_fade_transition

# Slide 1: 骨架
s1 = prs.slides.add_slide(layout)
draw_skeleton(s1)
add_fade_transition(s1)

# Slide 2: 骨架 + 第一组数据
s2 = prs.slides.add_slide(layout)
draw_skeleton(s2)
draw_layer_a(s2)
add_fade_transition(s2)

# Slide 3: 完整图
s3 = prs.slides.add_slide(layout)
draw_skeleton(s3)
draw_layer_a(s3)
draw_layer_b(s3)
add_fade_transition(s3)
```

**优点**：
- WPS / PowerPoint / Keynote 全部兼容
- 淡入过渡视觉效果流畅，接近动画体验
- 代码结构更清晰，易于维护

**缺点**：
- 幻灯片数量增加（通常 3-5 张）
- 静态内容（骨架）会在每张幻灯片上重复绘制（可以接受）

---

## 如果用户坚持要动画（仅限真正的 PowerPoint）

当用户明确说"用 Microsoft PowerPoint 演示，不是 WPS"时，可以尝试 XML 动画方案，
但需要注意：

1. 所有入场形状必须通过 `style.visibility=hidden` 显式隐藏（见坑 1）
2. 每个 click group 用 `delay="indefinite"` 包裹
3. 加入 `<p:bldLst>` 注册所有动画形状
4. 测试时必须用真实的演示模式（F5），编辑模式看不出效果

即便如此，不同版本的 PowerPoint 行为也可能有差异。
