# ggb-export —— 指令脚本 → .ggb 真机导出（零依赖）

把「已验证的 GeoGebra 指令脚本」导出为**可双击打开**的 .ggb 文件（技能交付方式 A，推荐；无本机环境时用 ggbgen.pages.dev，方式 B）。

原理：本地 Chrome/Edge 无头实例 + 官方 GeoGebra 引擎（deployggb.js）
→ 逐条 `evalCommand` → 逐条核验（对象创建 / 数值 / 样式）→ `getBase64()` 取 .ggb → 回读校验 → 落盘（可附带画布预览图）。

## 依赖

- Node 18+（使用全局 fetch / WebSocket，**无第三方 npm 依赖**）
- 本机 Chrome 或 Edge（自动探测常见路径；可用 `--browser` 指定）
- 首次运行需联网加载官方引擎（geogebra.org CDN）

## 用法

```bash
node export_ggb.mjs --page page.html --cmds <指令文件> --out <输出.ggb> [--png <预览.png>]
```

退出码：`0` 全过 ｜ `1` 运行失败 ｜ `2` 有指令未通过（failedList）｜ `3` 有软失败（返回成功但未创建对象）

可选参数：`--trace`（逐条追踪对象创建）、`--timeout 毫秒`、`--headful`（调试显示浏览器窗口）、`--browser <路径>`。

输出 JSON 报告：每条命令结果、脚本命令核验记录（verifiedNotes）、对象数对比、回读校验结论。

## 文件说明

| 文件 | 用途 |
|---|---|
| `page.html` | 引擎挂载页（加载官方 deployggb.js 并暴露 `window.ggbApplet`） |
| `export_ggb.mjs` | 导出器（零依赖 CDP 驱动；含脚本命令效果核验） |
| `verify_ggb.py` | .ggb 结构校验（ZIP 内容 / geogebra.xml 元素统计 / 命令调用数） |
| `example-tangent.txt` | 示例指令：导数定义（割线逼近切线），已验证真机通过 |

## 已固化的真机规则（引擎实测经验，v1.3）

1. **小写名坐标 = 向量**：`pt1 = (0, 0)` 被创建为 `vector`，`Line(pt1, pt2)` 失败；点请用大写名或 `Point(...)`。
2. **保留名被自动改名**：`sec = ...` → `sec_{1}`，之后按原名引用失败；避免与内置函数完全同名的对象名（`sec`/`tan`/`sin`/`cos`/`ln`…）。
3. **退化初值静默不创建**：`h = Slider(-1, 1, 0.01)` 初始值为 0 时 `A`、`B` 重合，`Line(A, B)` 返回“成功”却**不创建任何对象**；先 `SetValue(h, 0.5)` 设非零初值。
4. **脚本命令返回值不可信**：`SetValue` / `SetColor` / `ShowLabel` 的 `evalCommand` 恒返回 false，但效果真实生效；导出器内置 getter 核验（`getValue` / `getColor` / `getLabelVisible`）。

其中规则 1、2 已沉淀为 L1 验证器的静态提醒（v1.3）；规则 3、4 由本工具在真机执行时自动检出/核验（v1.3.1 起，规则 3 另有启发式静态预检）。预览图：检测到三维对象时自动切换 3D 视图。

## 附：3D 场景评测（v1.3.1）

已通过初步评测：`Sphere` / `Plane`（三点式）/ `IntersectPath`（平面×球面 → 交线圆）/ 3D 点 / 多元函数 `f(x,y)` 均可经导出器执行并正确写入 .ggb（元素：quadric / plane3d / conic3d / point3d / functionnvar）。3D 视图在无头环境下可正常渲染（截图确认：三维坐标系、球体、交线圆均可见）；也可导入本地 GeoGebra 复核。

## 按钮与脚本（ggb_patch.py，v1.4）

- **创建按钮**：指令中用单参形式 `btnReset = Button("重置")`（真机实测支持命名）。
- **注入脚本**：`python ggb_patch.py --ggb base.ggb --spec scripts.json --out final.ggb`
  - spec 格式：`[{"label": "btnReset", "event": "onClick", "script": "SetValue(a, 1)\nSetValue(h, 0.8)"}, …]`
  - `event` 取 `onClick`（点击）或 `onUpdate`（对象更新时）。
  - 背景：二参 `Button("标题","脚本")` 经命令注入不受支持（静默失败）；本工具产出与桌面版一致的结构（`<ggbscript val="…">`）。
- **完整样例**：`example-buttons.txt` ＋ `example-buttons.scripts.json`（割线演示 + 重置/换点按钮，已通过静态验证、真机导出与注入回读核验）。
