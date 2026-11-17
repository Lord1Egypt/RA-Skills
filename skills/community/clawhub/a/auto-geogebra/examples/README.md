# 示例（全部为真实运行产物）

每个示例 = 指令源（`.txt`）+ 成品（`.ggb`，双击可打开）+ 预览图（见 `../assets/`）+ 复现说明。
生成方式：`tools/ggb-export/export_ggb.mjs` 在无头浏览器中调用官方 GeoGebra 引擎，逐条执行、核验后导出；
带按钮/脚本的示例再用 `tools/ggb-export/ggb_patch.py` 注入脚本并回读校验。

| # | 示例 | 教学主题 | 亮点 | 文件 |
|---|---|---|---|---|
| 1 | 导数定义 | 割线趋近切线 | 滑块 h 双侧逼近 0，动态文本显示割线斜率 | `demo1-derivative-definition.txt` / `.ggb` |
| 2 | 线性变换 | 矩阵作用于单位正方形 | 矩阵元素滑块 + 行列式动态文本 | `demo2-linear-transform.txt` / `.ggb` |
| 3 | 球面截交 | 平面截球面的交线圆（3D） | 3D 视图，导出时自动切换渲染 | `demo3-sphere-cross-section.txt` / `.ggb` |
| 4 | 按钮割线 | 按钮控制取点位置 | `onClick` 脚本注入（ggb_patch） | `demo4-button-secant.*` |
| 5 | 正 n 边形逼近圆 | 序列 + 面积对比 | 播放/停止/重置按钮对，n 动画 | `demo5-polygon-circle.*` |
| 6 | 泰勒近似 | 多项式逐阶逼近函数 | 阶数滑块 + 误差可视化 | `demo6-taylor.*` |
| 7 | 抛硬币频率 | 随机模拟与频率稳定 | "重新抛掷"（UpdateConstruction 重抽）+ 重置 | `demo7-coin-toss.*` |

> 其中 `*.scripts.json` 为按钮脚本注入清单（配合 `ggb_patch.py` 使用）。

## 复现

需要 Node 18+ 与本机 Chrome/Edge（首次联网加载官方引擎）：

```bash
# ① 导出（以示例 1 为例）
node ../tools/ggb-export/export_ggb.mjs --page ../tools/ggb-export/page.html \
  --cmds demo1-derivative-definition.txt --out demo1.ggb --png preview.png

# ② 带按钮的示例（demo4–demo7）：在导出结果上注入脚本
python ../tools/ggb-export/ggb_patch.py --ggb demo4-button-secant.ggb \
  --spec demo4-button-secant.scripts.json --out demo4-button-secant.ggb
```

每个 `.ggb` 交付前均通过：静态双验证（L1+L2）→ 真机逐条核验（对象/数值/样式）→ 回读结构校验。
