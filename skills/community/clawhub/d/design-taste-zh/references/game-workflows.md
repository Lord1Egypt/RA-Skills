# 游戏工作流 —— 评审、报告、修改、生成

## 1. 评审一张游戏图（分步）

1. **分类**：资产类型（`game-screenshot | key-art | capsule | icon | game-ui | concept | sprite`）和品类（`python3 scripts/review_image.py --list-genres`）。询问或推断目标平台（Steam、App Store、Google Play、主机、游戏内）。
2. **跑指标**
   ```bash
   python3 scripts/review_image.py shot.png --type game-screenshot --genre moba --out review-shot
   ```
   输出 `metrics.json`、`report.md`（本中文版默认中文骨架；`--lang en` 为英文）、`palette.png`、`thirds-overlay.png`、`grayscale.png`、`thumbnail.png`。
3. **看图**：先看原图，再看 `grayscale.png`（灰度｜三值色调分离｜Otsu 图底蒙版）和 `thumbnail.png`（商店尺寸，彩色 + 灰度，Steam 深蓝底）。
4. **做五项测试**并写下证据：
   | 测试 | 方法 | 通过标准 |
   |---|---|---|
   | 灰度测试 | `grayscale.png` 第 1 格 | 玩家、敌人、可交互物、logo 仍可分离 |
   | 三值测试 | 第 2 格 | 焦点区域独占一个明度组；背景被压缩 |
   | 剪影测试 | 第 3 格 / 脑中把主体涂黑 | 从轮廓即可认出角色身份；群体不粘连 |
   | 缩略图测试 | `thumbnail.png` 的 184×69 / 120×45 / 128 / 64 | 标题可读、品类可猜、只有一个主体 |
   | 玩法 2 秒测试 | 看 2 秒，移开视线 | 能回答“我在哪、什么在威胁我、我能和什么交互” |
5. **按品类解读指标**（目标值见 `game-aesthetics.md §3/§6`）：
   - `contrast_rms` / `figure_ground_gap` 偏低 → 可读性风险；对射击、MOBA、大逃杀、平台跳跃最关键；恐怖/水墨只要有焦点强调可容忍。
   - `value_bands` 某一档 > 85% → 单调；恐怖和夜景可以偏暗，但需要一条被照亮的焦点路径。
   - `shape_edge_retention` < 0.30 且 `edge_density` 高 → 微细节噪声、大形弱（AI 图和过度刻画的概念图常见）。
   - `hud_edge_coverage_est` 对照品类上限：SLG/MMO/放置/卡牌可容忍 40–45%；射击/开放世界 ≤ 15%。`hud_center_clutter_est` > 0.15 = UI 侵占游玩区域。（启发式——建筑和网格会抬高数值。）
   - 色数：风格化/休闲希望色箱少；像素画 `unique_colors_exact` ≤ 256 且 `pixel_run_mode` = 一致的整数倍。
   - 胶囊图/图标/主视觉的缩略图 `contrast_rms` < 35 或保留率 < 0.75 → P0。
6. **打分**：11 个维度按类型权重（`game-aesthetics.md §2`）；总分 = 0.4 指标 + 0.6 视觉；有 P0 则上限 59。
7. **写报告**（模板见下）并给出具体修法；可选做一个修改样稿（调整明度后的裁切、胶囊图重绘稿），重跑脚本展示指标变化。

## 2. 报告模板

```markdown
# 游戏美术评审：<文件名>｜<类型>｜<品类>

**一句话结论：** <能不能用、最大问题、最该先改什么>

## 评分
| 部分 | 分数 |
|---|---|
| 指标分（脚本 40%） | xx/100 |
| 视觉分（Agent 60%） | xx/100 |
| **总分**（有 P0 则 ≤59） | xx/100 |

| 维度 | 权重 | 分 | 证据 |
|---|---|---|---|
| G1 可读性/剪影 | | | 灰度图中敌人与地面明度差… |
| G2 明度与色彩层级 | | | |
| G3 玩法优先清晰度 | | | |
| G4 美术方向统一 | | | |
| G5 UI/HUD | | | HUD 边缘覆盖 xx% |
| G6 特效克制 | | | |
| G7 光影氛围 | | | |
| G8 角色/场景设计 | | | |
| G9 品牌/主视觉吸引力 | | | |
| G10 技术完成度 | | | |
| G11 AI 痕迹/原创 | | | |

## 问题清单
### P0（阻断玩法或上架）
1. **问题** — 证据（位置/指标）— 修改方法（具体数值/做法）
### P1（明显降低质量）
### P2（打磨）

## 改进方案（按优先级）
1. …（例：背景明度压到 30–45%，敌人加 2px 暖色描边）
## 测试结论
- 灰度测试：通过/不通过 · 剪影测试 · 缩略图测试（184×69 / 120×45）· 2 秒测试
附件：grayscale.png、thumbnail.png、palette.png、thirds-overlay.png
```

## 3. 按品类的改进配方

| 品类 | 典型修改配方 |
|---|---|
| 射击 / 大逃杀 | 环境去饱和并压缩明度范围（如 25–60%），敌人加轮廓光/描边，准星区 ≤ 1 个亮元素，HUD 移到四角 |
| MOBA | 地面纹理对比 −20%，单位脚下加队伍色光圈，特效强度分档（普攻 30% / 控制 60% / 大招 100% 亮度），皮肤保留基础剪影 |
| ARPG / Roguelike | 敌方弹幕用一个暖色高饱和色相并置于最上渲染层；玩家特效偏冷且半透明；地面明度带收窄；掉落光柱按稀有度区分 |
| 平台跳跃 / 银河城 | 平台：明度 +1 档并加描边；背景对比 −40%、加雾；危险物用红色/尖刺形状族 |
| 开放世界 | 按生态/时段写色彩脚本；天际线上的地标剪影；用雾表现纵深；HUD 自动隐藏 |
| JRPG / 二次元抽卡 | 角色色彩关键色（每个英雄一个色相）；脸部明度最高；UI 角标上限（红点 ≤ 3）；线宽规范 |
| SLG / MMO / 放置 / 卡牌 | 字号 ≤ 4 档、等宽数字、图标形状编码、面板层级（主/次/三级背景）、留白间距 8/16 px |
| 休闲 / 三消 | 棋子：色相 + 形状 + 明度三重编码；棋盘底板；背景模糊；按钮 ≥ 44 pt 且有立体/按下态 |
| 恐怖 | 黑位提到约 8–15% 亮度；路径/关键物上有光池；单一强调色相；用雾片表现纵深 |
| 竞速 / 体育 | 赛道/场地中性；队服明度对比；运动模糊只在周边；转播式 HUD |
| 像素风 | 选定一个尺度（如 16/32 px 图块），16–32 色调色板配色相偏移色阶，最近邻整数倍放大，选择性描边 |
| 武侠/仙侠 | 配色取自石青/石绿/朱砂/赭石/月白；云雾分层；粒子光效减半；书法字只用于 logo |
| 水墨 | 5 级墨色 + 1 枚红印；留白 ≥ 30%；剪影边缘用枯笔；不要均匀的数码纹理 |
| 胶囊图 / 图标 | Logo ≥ 小胶囊图宽度的 60%，粗字重，加描边/投影保证对比；一个角色或符号；在 `#1b2838` 上测试 120×45；必要时为小胶囊图单独出图 |

## 4. 提示词模板（不带 AI slop 的游戏美术）

规则：写明**品类、镜头、玩法功能、明度规划、配色数量、形状语言**，以及要避免的东西。不要让模型在图中生成文字（logo 之后再加）。先生成剪影/缩略图，再加细节。图像模型对英文提示词更稳定，以下模板保留英文。

**Key art**
```
Key art for a <genre> game, <one-sentence hook>. Single hero <character> in a <pose verb> pose, strong readable silhouette against a <simple/darker/lighter> background, 3-value structure (dark frame, mid environment, brightest on face and <prop>). Palette: <dominant hue> dominant, <accent hue> accent only on <element>, max 4 hues. <rendering style: painterly / cel-shaded / ink wash>. Clear empty area at <top/bottom third> for the logo. No text, no watermark, no extra characters, no lens flares, no glowing particles everywhere, anatomically correct hands holding the <weapon>.
```
**In-game screenshot mock / environment**
```
<genre> gameplay scene, <camera: isometric / third-person over-shoulder / side-view 2D>, player character clearly separated from background by value and rim light, enemies use <warm red> accents, walkable path lit, background desaturated with atmospheric haze, HUD-free (UI added later), consistent <style> materials, low-frequency detail in background, no random props, no text.
```
**Character concept**
```
Character concept sheet, <role> for a <genre> game, shape language: <triangles=aggressive / circles=friendly / squares=sturdy>, readable as a black silhouette, detail clustered at <chest/head>, rest areas on <legs/arms>, front and 3/4 view consistent, neutral gray background, palette <3 colors + 1 accent>, no text, no extra limbs, symmetric gear consistent left/right.
```
**Pixel art**
```
<N>x<N> pixel art sprite, <subject>, exact 1-pixel grid, <16>-color limited palette with hue-shifted ramps, selective dark outline, no anti-aliasing, no gradients, no blur, transparent background, side view, idle pose.
```
(Then verify with `--type sprite --genre pixel`: unique colors ≤ palette, run mode = scale; redraw if fake.)

**水墨 / 仙侠**
```
Chinese ink wash (水墨) game scene, <subject>, five ink tones from deep black to pale wash, 40% empty rice-paper space, single cinnabar red accent on <seal/sun/cloak>, dry-brush edges on rocks, mist layers for depth, no neon glow, no gold particles, no text or fake calligraphy.
```
**Capsule (art only, logo added in a design tool)**
```
Wide 462x174 composition, one bold subject on the <left/right> third, large flat area on the other side for a heavy title logo, high value contrast against dark navy, readable when shrunk to 120x45, no small details, no text.
```
