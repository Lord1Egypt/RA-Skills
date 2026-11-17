# p5.js 2.x 沉浸式冒险游戏设计指南（V4 新增）

> 本文是 V4 能力二「p5.js 单文件 HTML 沉浸式冒险游戏」的设计与实现手册。课件指南见 `p5js-courseware-guide.md`，系统提示见 `p5js-system-prompt.md`，本指南专注游戏化特有问题。

## ⚠️ 避坑参考（与 p5.js 互动课件一致）

本文所有 p5.js 代码必须严格遵守 `references/p5js-courseware-guide.md` 第三章「测试清单」、附录「p5 2.x 常见 API 陷阱速查」与「正确 3D 下拉拾取范式」中的全部避坑规则。任何 p5.js 课件的陷阱同样适用于游戏，特别注意：

- 已移除 API 黑名单：`screenX() / screenY() / screenZ() / modelX() / modelY() / modelZ()` 在 p5 2.x 已移除，禁止用于点击拾取（游戏中也常误用！如 3D 球点击 → 必须用「下拉列表 / selectedIndex / 原生 DOM」替代，详见课件指南附录 C）
- WEBGL 中文：默认字体在 WEBGL 下不显示中文 → 中文走 DOM HTML 信息层，WEBGL 内不画中文
- `draw()` 前置崩溃：HUD 绘制必须放在 `draw()` 末尾，否则前置崩溃导致 HUD 失效
- 状态机变量残留：所有全局变量必须在 `setup()` 顶部显式重置（防上次会话 left-over）
- 实例模式 API 前缀：所有 p5 调用必须带 `p.` 前缀（`p.createCanvas`、`p.background`）
- DOM 控件：优先用原生 HTML + `addEventListener`，p5 `createButton` 在实例模式 + 全局 `mousePressed` 共存时脆弱
- 资源与数组边界：题目 / 关卡 / 生命值数组越界需防御

> 课件指南中所有测试清单项（9 项静态自检 + 7 项验证流程）均适用于游戏开发；游戏额外检查见本文第七章「强制测试门控（游戏专项）」。

## 一、核心设计理念

- **玩中学**：把抽象 AI 概念转化为可点击、可操作、可闯关的游戏环节
- **得分/等级反映学习效果**：每答对 / 连击 / 速度奖励 / 关卡完美度 → 真实映射到学习掌握度
- **A/B/C/D 深度适配**：每个模块有专属游戏化设计（详见第三节）
- **低门槛高上限**：单 HTML 文件易打开，2D/3D 渐进式难度

## 二、得分与等级系统（核心）

### 2.1 得分公式

```text
基础分        = 答对题数 × 10
速度奖励      = max(0, 5 − 答题用时秒) × 5   // 5s 内答完 +5/题
连击加成      = 连续答对 ≥3 时，每题额外 +5
完美关卡      = 零错误通关 +50
总得分        = 基础分 + 速度奖励 + 连击加成 + 完美关卡
```

### 2.2 等级映射

| 等级 | 称号 | 分数阈值 | 视觉标识 |
|------|------|----------|----------|
| 1 | 探索者 | 0–99 | 灰色 |
| 2 | 工程师 | 100–299 | 蓝色 |
| 3 | 架构师 | 300–599 | 紫色 |
| 4 | 大师 | 600+ | 金色 |

- 等级实时联动 HUD
- 每升一级弹出祝贺 + 称号徽章

### 2.3 反馈机制
- 答对：闪光 + 音效（可选）+ 分数 +N
- 答错：震动 + 错误解析 + 减 1 颗心（3 颗心制）
- 通关：关卡完美度雷达图（5 维度）
- 结算：知识图谱回顾（学到的概念高亮）

## 三、A/B/C/D 模块深度适配

| 模块 | 游戏类型 | 核心玩法 | 典型关卡 |
|------|----------|----------|----------|
| A 认知基础 | 时间轴冒险 / 概念配对 | 2D 横版跳跃收集 AI 里程碑球，配对选择题开启新关卡 | A1：1950–2025 时间轴收集 10 个里程碑；A2：概念配对（AI / ML / DL）；A3：决策树分歧选择 |
| B 工具操作 | 操作模拟大冒险 | 按步骤完成真实操作（建项目 / 写代码 / 运行），每步配对问答题 | B1：TRAE IDE 建项目 5 步；B2：SOLO 任务派发 4 步 |
| C 方法论 | Prompt 大冒险 / 需求拆解闯关 | 输入 Prompt 击败「AI 误解怪」，正确度决定伤害 | C1：Prompt 战士（5 场 Boss）；C2：需求拆解（三层金字塔）；C3：验证闭环（4 步审查）；C4：多 Agent 协作（团队配队）；C5：飞轮（5 圈循环） |
| D 通用实练 | 数据侦探 / 编程闯关 | 数据分析 + Vibe Coding 实战 | D1：CSV 数据侦探（5 案件）；D2：Vibe Coding 编程闯关（3 项目） |

## 四、2D vs 3D 选择策略

| 场景 | 推荐 | 原因 |
|------|------|------|
| 时间轴 / 配对 / 闯关 | 2D | 节奏快、HUD 易读、跨设备流畅 |
| 星空 / 架构 / 空间探索 | 3D WEBGL | 沉浸感强、空间感 |
| 数据可视化探索 | 3D | 散点 / 网络 / 流场更直观 |

- 3D 必须用 `WEBGL` + `p.orbitControl()`（轨道控制）
- 3D 节点拾取：用「下拉列表」替代 `screenX`（防 p5 2.x 已移除 API 陷阱）

## 五、单文件 HTML 游戏模板（2D）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>V4 p5.js 游戏模板（2D）</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
  <script>
    if (typeof p5 === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
    }
  </script>
  <style>/* HUD / 弹窗样式 */</style>
</head>
<body>
  <div id="p5-container"></div>
  <script>
    const sketch = (p) => {
      // === 状态机 ===
      const STATE = { MENU: 0, PLAY: 1, LEVEL_COMPLETE: 2, GAME_OVER: 3, VICTORY: 4 };
      let state = STATE.MENU, level = 1, score = 0, combo = 0, lives = 3;
      let startTime, currentQ;

      // === 关卡数据（A/B/C/D 适配）===
      const levels = [
        { id: 'A1', q: 'AI 概念配对题…', ans: 'B', choices: ['A','B','C','D'] },
        { id: 'A2', q: '…', ans: 'A', choices: ['A','B','C','D'] }
      ];

      p.setup = () => {
        const c = p.createCanvas(p.windowWidth, p.windowHeight - 80);
        c.parent('p5-container');
        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(18);
      };

      p.draw = () => {
        p.background(20, 30, 50);
        if (state === STATE.MENU) drawMenu();
        else if (state === STATE.PLAY) drawPlay();
        else if (state === STATE.LEVEL_COMPLETE) drawLevelComplete();
        else if (state === STATE.GAME_OVER) drawGameOver();
        else if (state === STATE.VICTORY) drawVictory();
        drawHUD();  // 始终绘制 HUD（放在 draw 末尾，防前置代码崩溃失效）
      };

      function drawMenu() { /* 标题 + 开始按钮 */ }
      function drawPlay() { /* 关卡背景 + 角色 + 问答弹窗 */ }
      function drawLevelComplete() { /* 关卡结算 + 下一关按钮 */ }
      function drawGameOver() { /* 失败 + 重玩 */ }
      function drawVictory() { /* 通关 + 总分 + 等级 */ }
      function drawHUD() { /* 分数 / 等级 / 关卡 / 生命 */ }

      // === 得分逻辑 ===
      function answerCorrect() {
        const elapsed = (p.millis() - startTime) / 1000;
        const speedBonus = Math.max(0, 5 - elapsed) * 5;
        score += 10 + speedBonus;
        combo++;
        if (combo >= 3) score += 5;
      }
      function answerWrong() {
        combo = 0;
        lives--;
        if (lives <= 0) state = STATE.GAME_OVER;
      }

      // === 等级计算 ===
      function getLevel(s) {
        if (s >= 600) return { lv: 4, name: '大师', color: '#FFD700' };
        if (s >= 300) return { lv: 3, name: '架构师', color: '#9C27B0' };
        if (s >= 100) return { lv: 2, name: '工程师', color: '#2196F3' };
        return { lv: 1, name: '探索者', color: '#9E9E9E' };
      }

      p.windowResized = () => p.resizeCanvas(p.windowWidth, p.windowHeight - 80);
    };
    new p5(sketch);
  </script>
</body>
</html>
```

## 六、单文件 HTML 游戏模板（3D WEBGL）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>V4 p5.js 游戏模板（3D）</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
  <style>/* HUD / select 样式 */</style>
</head>
<body>
  <div id="p5-container"></div>
  <select id="nodeSelect"><option value="-1">选择节点…</option></select>
  <script>
    const sketch = (p) => {
      // === 状态机同 2D ===
      const STATE = { MENU: 0, PLAY: 1, LEVEL_COMPLETE: 2, GAME_OVER: 3, VICTORY: 4 };
      let state = STATE.MENU, level = 1, score = 0, combo = 0, lives = 3;
      const nodes = [];           // 3D 知识点球
      let selectedIndex = -1;     // 用 selectedIndex 代替 screenX 拾取（防 p5 2.x 陷阱）

      const levels = [
        { id: 'A1', nodes: [
          { title: '1950 图灵测试', pos: [-200, 0, 0] },
          { title: '2012 AlexNet', pos: [0, 0, 0] },
          { title: '2017 Transformer', pos: [200, 0, 0] }
        ]}
      ];

      p.setup = () => {
        const c = p.createCanvas(p.windowWidth, p.windowHeight - 80, p.WEBGL);
        c.parent('p5-container');
        // 用原生 select 替代 screenX 拾取
        const sel = document.getElementById('nodeSelect');
        levels[0].nodes.forEach((n, i) => {
          const opt = document.createElement('option');
          opt.value = i; opt.textContent = n.title;
          sel.appendChild(opt);
        });
        sel.addEventListener('change', (e) => {
          selectedIndex = parseInt(e.target.value, 10);
        });
      };

      p.draw = () => {
        p.background(10, 20, 40);
        if (state === STATE.PLAY) {
          p.orbitControl(2, 2, 0.1);  // 轨道控制（防 VCP 误用 screenX）
          p.ambientLight(150);
          p.pointLight(255, 255, 255, 0, -200, 200);
          // 绘制 3D 节点球
          levels[level - 1].nodes.forEach((n, i) => {
            p.push();
            p.translate(n.pos[0], n.pos[1], n.pos[2]);
            p.ambientMaterial(i === selectedIndex ? p.color(255, 200, 0) : p.color(100, 150, 255));
            p.sphere(40);
            p.pop();
          });
        }
        drawHUD();  // 2D HUD 覆盖在 3D 之上
      };

      function drawHUD() {
        p.resetMatrix();
        p.camera();  // 重置到 2D 坐标系
        p.fill(255);
        p.text(`分数: ${score}  等级: ${getLevel(score).name}  关卡: ${level}  ❤${lives}`, 0, -p.height / 2 + 20);
      }

      // === 得分/等级函数同 2D ===

      p.windowResized = () => p.resizeCanvas(p.windowWidth, p.windowHeight - 80);
    };
    new p5(sketch);
  </script>
</body>
</html>
```

## 七、强制测试门控（游戏专项）

课件指南第三章 + 第七章全部门控均适用。游戏额外检查：

- 状态机 5 状态全部可达（MENU / PLAY / LEVEL_COMPLETE / GAME_OVER / VICTORY）
- INITIAL_STATE 显式声明（避免上次会话值残留）
- 得分逻辑闭环：每题答对确实加分、连击正确累计、等级正确升级
- HUD 实时同步（分数 / 等级 / 关卡 / 生命）
- 2D 与 3D 坐标系不混淆（3D 必备 `p.resetMatrix()` + `p.camera()` 切回 2D HUD）
- 性能：60fps 流畅（draw 内无大对象创建）
- 不使用 p5 2.x 已移除 API（`screenX` / `screenY` / `modelX` / `modelY` 等）
- 3D 中文不在 WEBGL 内画（用 DOM HTML 信息层）
- 控件首选原生 DOM + `addEventListener`（p5 `createButton` 在实例模式 + 全局 `mousePressed` 共存时脆弱）

## 八、常见坑与解法

| 坑 | 解法 |
|----|------|
| 状态机遗漏 GAME_OVER / VICTORY | 显式声明 5 状态；状态转移表覆盖每对 |
| 初始值残留（上次会话 left-over） | setup 顶部强制重置所有全局变量 |
| draw 内创建对象致卡顿 | 提取到 setup 或对象池复用 |
| 3D HUD 坐标系错乱 | 绘制 HUD 前 `p.resetMatrix()` + `p.camera()` |
| 3D 节点点击拾取用 `screenX` | 用「下拉列表」或「selectedIndex」替代 |
| 连击 / 速度计算写死边界 | 公式封装为 `computeScore(...)` 函数可测试 |
| 等级不联动 HUD | HUD 绘制函数始终从 `score` 重新计算 level |

## 九、与 V3 课件的衔接

- 游戏中的「问答弹窗」与 V3 课件的「控制面板」风格统一
- 游戏的「关卡」与 V3 课件的「章节」对应；可互相引用
- 游戏的「知识图谱回顾」可作为 V3 课件的「教学要点总结」扩展
- 同一课程可同时输出：1 套课件（V3）+ 1 套游戏（V4）+ 1 套备课包（V4）三位一体

## 十、典型 30 分钟出活清单

1. 选 A/B/C/D 中一个模块（如 A1）
2. 列出 5–10 个核心知识点（作为关卡 / 题目）
3. 选 2D 或 3D
4. 套用第五 / 六节模板
5. 填 `levels` 数组（题目 + 答案）
6. 加 CSS 美化 HUD
7. 走强制测试门控（16 项）
8. `node --check` 语法验证
9. 浏览器实测（启动 → 通关 → 结算）
10. 交付

## 十一、跨能力避坑参考（与 p5.js 互动课件完全一致）

以下陷阱在课件与游戏中**同样致命**，开发游戏时必须与课件避坑保持一致：

| 陷阱 | 在游戏中常见误用 | 课件指南原文位置 |
|------|------------------|------------------|
| `screenX / screenY` 在 2.x 移除 | 3D 节点点击拾取 → `TypeError` | 课件指南第三章黑名单项 |
| `modelX / modelY / modelZ` 在 2.x 移除 | 模型↔屏幕坐标互转 → 崩溃 | 同上 |
| WEBGL 中文不显示 | 游戏 HUD / 弹窗显示中文 → 渲染空白 | 课件指南第九项测试清单 |
| draw 内创建对象 | 游戏对象 / 粒子数组创建 → 帧率暴跌 | 课件指南 7.1 静态自检 |
| 实例模式混用全局式 | 课件/游戏中常见 `background()` 裸写 → 静默失败 | 课件指南第三章测试清单第 4 项 |
| 状态机遗漏 `GAME_OVER / VICTORY` | 游戏只玩到一半或卡死 | 本文第七章专项检查 |
| HUD 不联动得分变化 | 玩家看不到分数实时更新 | 本文第二章 + 第七章 |

**正确范式（从课件指南附录 C 引用）**：

```javascript
// ❌ 错误范式（2.x 必崩，禁止）：
// const sx = p.screenX(n.x, n.y, n.z);  // TypeError: not a function

// ✅ 正确范式：3D 节点用「下拉列表」或「selectedIndex」驱动拾取/高亮
// （完整模板见课件指南附录 C，本指南第六节 3D 模板已应用此范式）
```

**强制要求**：
- 开发任何 p5.js 游戏前，必须先读 `references/p5js-courseware-guide.md` 第三章测试清单 + 附录 C
- 课件避坑指南更新后，本指南同步继承（无需重写本指南，下次升级时引用同步）
- 游戏测试通过门控 = 课件门控 ∪ 游戏专项门控（取并集）
