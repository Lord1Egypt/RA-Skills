# Token 高效 SVG 写法（关键！）

内联 SVG 出图应优先用 **CSS 类 + `<defs>`/`<use>` 复用**，而非逐元素重复内联 `style`。同等视觉效果下，生成 token 可减少 **40%–63%**（实测 6 节点片段 -42.7%；30 节点/40 连线量级约 -63%）。规则：

- **样式集中到 `<style>`**：把 `fill`/`stroke`/`font` 等抽成类（如 `.node`、`.edge`、`.label`、`.bg`），元素用 `class="..."` 引用，杜绝每个 `<rect>`/`<text>` 重复写 `style="..."`。
- **形状用 `<defs><g id="node">` 定义一次，`<use href="#node" x= y=>` 多次实例化**：同尺寸节点只定义一次。
- **白底衬底也用类**：防压字的 `fill="#ffffff"` 矩形统一用 `.bg{fill:#fff}`，避免逐条重复。
- **坐标精简**：同列节点用统一 `x`、文本用 `text-anchor` 居中，减少坐标拼写。

## 最小可套用模板

```svg
<svg viewBox="0 0 680 320" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .node{fill:#f5f3eb;stroke:#d4d1c7;stroke-width:1;rx:10}
      .node-t{font:500 14px sans-serif;fill:#1a1a18;text-anchor:middle}
      .edge{stroke:#5f5e5a;stroke-width:1.5;fill:none}
      .label{font:400 12px sans-serif;fill:#6b6961}
      .bg{fill:#fff}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <g id="box">
      <rect class="node" width="140" height="48" rx="10"/>
    </g>
  </defs>

  <!-- 白底衬底（防压字） -->
  <rect class="bg" x="150" y="60" width="120" height="22"/>

  <!-- 节点实例 -->
  <use href="#box" x="40" y="40"/>
  <text class="node-t" x="110" y="68">网关</text>

  <use href="#box" x="260" y="40"/>
  <text class="node-t" x="330" y="68">订单服务</text>

  <!-- 连线 -->
  <path class="edge" d="M180 64 L260 64" marker-end="url(#arrow)"/>
  <text class="label" x="200" y="56">调用</text>
</svg>
```

## 对比要点

| 写法 | 6 节点 token | 30 节点/40 连线 token |
|------|-------------|----------------------|
| 逐元素内联 style | 基准 | 基准 |
| CSS 类 + defs/use | **-42.7%** | **-63%** |

视觉渲染完全等价，仅省生成成本。
