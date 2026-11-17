# 交互增强模式库（按钮 / 动画 / 模拟）

> 把「经典展示型演示」升级为「交互演示」的可复用模式。
> 素材来源：作者手工案例库（教学创新赛·抛硬币/几何概率系列、直方图等·Probabilities balls、实变函数·CantorSet 等，共 219+ 案全库联学）+ 本技能真机实测。自 v1.4 起启用。

## 0. 引擎事实（真机实测，编写按钮/脚本前必读）

- **按钮创建**：`Button()`、`Button("标题")` 均可经指令创建，支持命名（`btnReset = Button("重置")`）。
- **带脚本的二参形式 `Button("标题","脚本")` 经命令注入不受支持**（真机实测：静默失败，按钮不会被创建）。
  正确姿势：先用 `Button("标题")` 创建 → `export_ggb.mjs` 真机导出 → `ggb_patch.py` 注入脚本。
- **脚本语言（GGBScript）要点**：
  - 多语句用**换行**分隔（`;` 不是分隔符——真机实测只执行第一句）；
  - 方括号经典写法与圆括号均可（`SetValue[a,1]` ＝ `SetValue(a,1)`）；
  - 脚本命令（SetValue / StartAnimation 等）经 API 执行时返回 false 属正常现象，**看效果不看返回值**。
- **脚本存储位置**：.ggb 内 `geogebra.xml` 中 `<ggbscript val="…"/>`（点击）/ `<ggbscript onUpdate="…"/>`（对象更新时）。

## 1. 重置按钮（最常用）

```json
{"label": "btnReset", "event": "onClick", "script": "SetValue(a, 1)\nSetValue(h, 0.8)"}
```

- 列表类清空：`results = {}` 或 `SetValue[plist, {}]`（作者案例：Coin Toss 的 Restart、几何概率的 clear）。
- 约定：打开的初始状态 ＝ 重置后的状态（孩子按一下就知道回到了起点）。

## 2. 重抽 / 换一批（随机模拟）

```json
{"label": "btnRand", "event": "onClick", "script": "SetValue(a, RandomUniform(-2, 2))"}
```

- 重排列表：`BlueRandomList = Shuffle[BlueList]`（作者案例：Probabilities balls）。
- 单次抽样并累积：`event = Random(0,1)` + `SetValue(results, Append(results, event))`（作者案例：Coin Toss）。

## 3. 开始/停止对 + 自动运行（进阶，作者体系）

作者案例（几何概率系列）的"动画驱动模拟"三件套：

1. 一个滑块（如 `kk`）设为动画（`playing=true`），且动画速度指向变量 `speed`（`<animation speed="speed">`）；
2. 该滑块挂 `onUpdate` 脚本：每动画步执行一次模拟，并 `If[sum==n, SetValue[speed,0]]` 自动停止；
3. 两个按钮 + **条件显隐**：「开始」按钮 `SetValue[speed,3]`（同时重置计数），显示条件 `speed ≟ 0`；
   「停止」按钮 `speed=0`，显示条件 `speed > 0`。

> 本技能现状：上述 .ggb 结构可生成（onUpdate 经 `ggb_patch.py` 注入）；完整自动运行的视觉行为建议导出后在本机 GeoGebra 实跑确认。

## 4. 累积/迭代按钮

`SetValue(results, Append(results, event))` —— 每次点击往列表追加一个元素；
配合 `CountIf` / `TableText` 即时做统计表（作者案例风格）。

## 5. 输入框参数（Textfield）

`txtN = Textfield(n)` —— 让教师/学生直接改参数（作者库 28 案使用）。
真机导出后可用 `getValue` / `setValue` 核验初值。

## 6. 生成与验证流程（本技能）

1. 指令文件中用**单参**创建按钮：`btnReset = Button("重置")`；
2. 静态双验证（L1/L2）→ `export_ggb.mjs` 真机导出（按钮对象随文件保存）；
3. `python ggb_patch.py --ggb base.ggb --spec scripts.json --out final.ggb` 注入脚本；
4. 回读验证：脚本数量（geogebra.xml 中 ggbscript）、对象清单、脚本语句可执行性。

> 完整样例：`tools/ggb-export/example-buttons.txt` ＋ `example-buttons.scripts.json`（割线演示 + 重置/换点按钮）。

## 7. 按钮定位

按钮默认会堆叠在同一位置（互相遮挡）。用 `SetCoords(btnReset, x, y)` 设置像素位置（以画布左上角为原点）。该脚本命令返回值照例不可信（false），但效果真实生效——导出器已内置 `labelOffset` 核验：

```
SetCoords(btnReset, 40, 80)
SetCoords(btnRand, 40, 140)
```
