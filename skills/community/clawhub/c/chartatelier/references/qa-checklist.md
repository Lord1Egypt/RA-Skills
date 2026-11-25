# 验收清单

> 五项自检 + 交付前总检查。每一条都有可执行的判据，不写“看起来是否协调”这类无法验收的表述。

## 一、五项自检

| # | 检查项 | 判据 | 不通过时 |
|---|---|---|---|
| 1 | 留白 | 内容覆盖率 ≥95% 宽、≥93% 高；四边留白 1–3% | 收紧 viewBox，收掉页面默认内边距 |
| 2 | 连线交叉 | 正交折线两两相交 = 0 | 改走行间空隙，或一侧改虚线绕行 |
| 3 | 文字溢出 | 每个 `<text>` 外接框在所属矩形内 ±2px | 缩短文案 → 加高框体 → 折行，禁止缩字号 |
| 4 | 对比度 | 正文/标注 ≥4.5∶1，大字标题 ≥3∶1 | 标题色同色系加深一档，不改填充 |
| 5 | 导出尺寸 | 像素宽 = 逻辑宽 × 倍数（±2px），且 ≥3000px | 重设窗口尺寸或缩放倍数 |

检查顺序固定：几何 → 排版 → 色彩 → 导出。前一项没过不要改后一项，否则改完颜色还要重测几何。

## 二、几何探针（浏览器控制台）

在打开图表的页面执行，返回 JSON。要点：排除 `defs`（标记、图案）与铺满画布的底图，否则外接框恒等于整张画布。

```js
(() => {
  const svg = document.querySelector('svg');
  if (!svg) return 'no svg';
  const vb = svg.viewBox.baseVal;
  const els = [...svg.querySelectorAll('rect,text,line,path')].filter(el => {
    if (el.closest('defs')) return false;
    const b = el.getBBox();
    return !(b.width >= vb.width * 0.95 && b.height >= vb.height * 0.95);
  });
  let minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
  els.forEach(el => {
    const b = el.getBBox();
    if (!b.width && !b.height) return;
    minX = Math.min(minX, b.x); minY = Math.min(minY, b.y);
    maxX = Math.max(maxX, b.x + b.width); maxY = Math.max(maxY, b.y + b.height);
  });
  const rects = els.filter(e => e.tagName === 'rect');
  let overlaps = 0;
  for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
    const a = rects[i].getBBox(), b = rects[j].getBBox();
    const ox = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
    const oy = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
    if (ox > 3 && oy > 3) overlaps++;
  }
  const overflow = [...svg.querySelectorAll('text')].filter(t => {
    const tb = t.getBBox();
    let p = t.parentElement;
    while (p && p !== svg) {
      if (p.tagName === 'rect') {
        const pb = p.getBBox();
        return tb.x < pb.x - 2 || tb.y < pb.y - 2 ||
               tb.x + tb.width > pb.x + pb.width + 2 ||
               tb.y + tb.height > pb.y + pb.height + 2;
      }
      p = p.parentElement;
    }
    return false;
  }).length;
  const clipped = els.filter(el => {
    const b = el.getBBox();
    if (!b.width && !b.height) return false;
    return b.x < vb.x - 0.5 || b.y < vb.y - 0.5 ||
           b.x + b.width > vb.x + vb.width + 0.5 ||
           b.y + b.height > vb.y + vb.height + 0.5;
  }).length;
  return JSON.stringify({
    viewBox: [vb.x, vb.y, vb.width, vb.height],
    contentBox: { minX: Math.round(minX), minY: Math.round(minY),
                  maxX: Math.round(maxX), maxY: Math.round(maxY),
                  w: Math.round(maxX - minX), h: Math.round(maxY - minY) },
    margins: { left: Math.round(minX - vb.x), top: Math.round(minY - vb.y),
               right: Math.round(vb.x + vb.width - maxX),
               bottom: Math.round(vb.y + vb.height - maxY) },
    suggestedViewBox: `${Math.round(minX - 16)} ${Math.round(minY - 16)} ${Math.round(maxX - minX + 32)} ${Math.round(maxY - minY + 32)}`,
    overlaps, overflow, clipped
  }, null, 1);
})()
```

判读：`overlaps` 里若出现“容器边界框 × 其子节点”的配对，属预期，不计入缺陷；兄弟节点之间的重叠才是缺陷。`overflow` 与 `clipped` 必须为 0。

## 三、覆盖率校验（读回 PNG）

```python
from PIL import Image
im = Image.open(path).convert('RGB')
w, h = im.size
px = im.load()
xs, ys = [], []
for y in range(0, h, 8):
    for x in range(0, w, 8):
        r, g, b = px[x, y]
        if max(r, g, b) - min(r, g, b) > 30:   # 饱和度判据，不用亮度分桶
            xs.append(x); ys.append(y)
print(w, h, 'cover',
      round((max(xs) - min(xs)) / w * 100, 1),
      round((max(ys) - min(ys)) / h * 100, 1))
```

判据：宽 ≥95%、高 ≥93%。用亮度分桶会把浅色填充误判为空白，导致覆盖率虚低而误改版式。

## 四、qa-report.json 字段

| 字段 | 含义 | 通过值 |
|---|---|---|
| `logical` | 逻辑画布 `[w, h]` | 1520 × 856 等 |
| `expected_px` | 逻辑 × 倍数 | 3040 × 1712 |
| `actual_px` | 实际 PNG 尺寸 | 与 `expected_px` 相差 ≤2px |
| `cover_w` / `cover_h` | 内容覆盖率（百分比） | ≥95 / ≥93 |
| `margins` | 四边留白（像素） | 各为画布宽的 1–3% |
| `overflow` | 文字溢出数 | 0 |
| `sibling_overlap` | 兄弟节点重叠数 | 0 |
| `clipped` | 越出 viewBox 的元素数 | 0 |
| `contrast_min` | 采样文字的最低对比度 | ≥4.5 |
| `ok` | 综合结论 | true |

## 五、交付前总检查

- [ ] 五项自检全绿，`qa-report.json` 的 `ok` 为 true。
- [ ] PNG 在 25% 缩放看层级清楚，在 100% 缩放看文字不糊、箭头不断。
- [ ] SVG 在矢量软件中能改字，且改完不跑版（证明文本未转曲）。
- [ ] HTML 双击可开，控制台无报错。
- [ ] 文件名全小写、连字符分隔、带版本号，不含客户名与项目代号。
- [ ] 图例、编号、单位、页脚版本与正文一致（重点查“共 X 页 / 第 Y 页”这类自相矛盾）。
- [ ] 交付说明含图种判定、配色口径、字号阶梯、复现命令四项。
- [ ] 临时文件已清理，交付目录里只有交付物。

## 六、记录与复盘

每次交付把 `qa-report.json` 与最终 PNG 放在同一目录。返工时先看上一版报告里的 `cover_w`、`overflow`、`contrast_min` 三个数，判断是版式问题还是导出问题，避免盲改。

同一批交付（如一套汇报的 5 张图）必须交叉比对：语义色含义是否一致、字号阶梯是否统一、图例样式是否同款。三处任一不一致，按“同一份交付”处理，重做而不是逐张修补。
