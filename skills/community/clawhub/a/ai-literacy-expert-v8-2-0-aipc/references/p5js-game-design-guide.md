> **V7 兼容性说明**：本文件在 V6 基础上进行 V7 原生增强。V7 新增：PAUSE 暂停状态机、难度分级系统（简单/普通/困难）、键盘 + 触屏双模操控、三级 CDN 兜底、单文件 ≤ 200KB 体积硬限。V6 全部能力继续有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 增强版本：V7 · 增强日期：2026-08-15

# p5.js 2.x 沉浸式冒险游戏设计指南（V4 新增）

> 本文是 V4 能力二「p5.js 单文件 HTML 沉浸式冒险游戏」的设计与实现手册。课件指南见 `references/p5js-courseware-guide.md`，系统提示见 `references/p5js-system-prompt.md`，本指南专注游戏化特有问题。

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V7 p5.js 游戏模板（2D）</title>
  <!-- 三级 CDN 兜底：cdnjs → jsdelivr → 本地 vendor -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
  <script>
    if (typeof p5 === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
    }
    if (typeof p5 === 'undefined') {
      document.write('<script src="./vendor/p5.min.js"><\/script>');  // 本地兜底
    }
  </script>
  <style>
    /* HUD / 弹窗样式 */
    body { margin: 0; overflow: hidden; font-family: 'Noto Sans SC', sans-serif; }
    #p5-container { width: 100vw; height: 100vh; }
    /* 触屏虚拟按键 */
    .touch-btn { position: fixed; width: 56px; height: 56px; border-radius: 50%; background: rgba(255,255,255,0.3); border: 2px solid rgba(255,255,255,0.5); display: flex; align-items: center; justify-content: center; font-size: 24px; color: #fff; user-select: none; -webkit-user-select: none; touch-action: none; z-index: 100; }
    .touch-btn:active { background: rgba(255,255,255,0.5); }
    #dpad-up    { bottom: 130px; left: 50%; transform: translateX(-50%); }
    #dpad-down  { bottom: 10px;  left: 50%; transform: translateX(-50%); }
    #dpad-left  { bottom: 70px;  left: 20px; }
    #dpad-right { bottom: 70px;  right: 20px; }
    #btn-action { bottom: 70px;  right: 20px; width: 64px; height: 64px; font-size: 14px; }
    #btn-pause  { top: 10px; right: 10px; width: 44px; height: 44px; font-size: 18px; }
    /* 仅触屏设备显示虚拟按键 */
    @media (hover: hover) and (pointer: fine) { .touch-btn { display: none; } }
  </style>
</head>
<body>
  <div id="p5-container"></div>

  <!-- 触屏虚拟 D-pad 与操作按钮（仅触屏设备可见） -->
  <div id="dpad-up"    class="touch-btn" aria-label="向上移动">▲</div>
  <div id="dpad-down"  class="touch-btn" aria-label="向下移动">▼</div>
  <div id="dpad-left"  class="touch-btn" aria-label="向左移动">◀</div>
  <div id="dpad-right" class="touch-btn" aria-label="向右移动">▶</div>
  <div id="btn-action" class="touch-btn" aria-label="确认操作">确认</div>
  <div id="btn-pause"  class="touch-btn" aria-label="暂停游戏">⏸</div>

  <script>
    const sketch = (p) => {
      // === 状态机（V7 新增 PAUSE 状态）===
      const STATE = { MENU: 0, PLAY: 1, PAUSE: 2, LEVEL_COMPLETE: 3, GAME_OVER: 4, VICTORY: 5 };
      let state = STATE.MENU, level = 1, score = 0, combo = 0, lives = 3;
      let startTime, currentQ;

      // === 难度分级（V7 新增）===
      const DIFFICULTY = { EASY: 0, NORMAL: 1, HARD: 2 };
      let difficulty = DIFFICULTY.NORMAL;
      const difficultyConfig = {
        [DIFFICULTY.EASY]:   { label: '简单', speedMul: 0.7, lives: 5, hints: true,  color: '#4CAF50' },
        [DIFFICULTY.NORMAL]: { label: '普通', speedMul: 1.0, lives: 3, hints: false, color: '#FF9800' },
        [DIFFICULTY.HARD]:   { label: '困难', speedMul: 1.5, lives: 1, hints: false, color: '#F44336' }
      };

      // === 键盘状态（V7 新增）===
      const keys = { up: false, down: false, left: false, right: false, action: false };

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
        // 键盘事件绑定（V7 新增）
        p.keyPressed = handleKeyPressed;
        p.keyReleased = handleKeyReleased;
        // 触屏事件绑定（V7 新增）
        p.touchStarted = handleTouchStarted;
        setupTouchControls();
      };

      p.draw = () => {
        p.background(20, 30, 50);
        if (state === STATE.MENU) drawMenu();
        else if (state === STATE.PLAY) drawPlay();
        else if (state === STATE.PAUSE) drawPause();          // V7 新增
        else if (state === STATE.LEVEL_COMPLETE) drawLevelComplete();
        else if (state === STATE.GAME_OVER) drawGameOver();
        else if (state === STATE.VICTORY) drawVictory();
        drawHUD();  // 始终绘制 HUD（放在 draw 末尾，防前置代码崩溃失效）
      };

      // === 菜单（含难度选择，V7 新增）===
      function drawMenu() {
        /* 标题 + 难度选择（简单/普通/困难）+ 开始按钮 */
        /* 键盘：方向键选难度，Enter 开始 */
        /* 触屏：点击难度按钮，点击开始 */
      }
      function drawPlay() { /* 关卡背景 + 角色 + 问答弹窗 */ }
      // === 暂停画面（V7 新增）===
      function drawPause() {
        /* 半透明遮罩 + "暂停" 文字 + "继续"按钮 + "退出"按钮 */
        /* 键盘：Escape/P 继续，Enter 确认 */
        /* 触屏：点击继续/退出按钮 */
      }
      function drawLevelComplete() { /* 关卡结算 + 下一关按钮 */ }
      function drawGameOver() { /* 失败 + 重玩 */ }
      function drawVictory() { /* 通关 + 总分 + 等级 */ }
      function drawHUD() { /* 分数 / 等级 / 关卡 / 生命 / 难度 */ }

      // === 键盘处理（V7 新增）===
      function handleKeyPressed() {
        if (p.keyCode === p.UP_ARROW || p.key === 'w')    keys.up = true;
        if (p.keyCode === p.DOWN_ARROW || p.key === 's')   keys.down = true;
        if (p.keyCode === p.LEFT_ARROW || p.key === 'a')   keys.left = true;
        if (p.keyCode === p.RIGHT_ARROW || p.key === 'd')  keys.right = true;
        if (p.key === ' ') keys.action = true;

        // 状态切换按键
        if ((p.key === 'Escape' || p.key === 'p' || p.key === 'P') && state === STATE.PLAY) {
          state = STATE.PAUSE;
        } else if ((p.key === 'Escape' || p.key === 'p' || p.key === 'P') && state === STATE.PAUSE) {
          state = STATE.PLAY;
        }
        if (p.key === 'Enter' && state === STATE.MENU) {
          applyDifficulty(); state = STATE.PLAY;
        }
      }
      function handleKeyReleased() {
        if (p.keyCode === p.UP_ARROW || p.key === 'w')    keys.up = false;
        if (p.keyCode === p.DOWN_ARROW || p.key === 's')   keys.down = false;
        if (p.keyCode === p.LEFT_ARROW || p.key === 'a')   keys.left = false;
        if (p.keyCode === p.RIGHT_ARROW || p.key === 'd')  keys.right = false;
        if (p.key === ' ') keys.action = false;
      }

      // === 触屏控制（V7 新增）===
      function setupTouchControls() {
        const bindTouch = (id, keyName) => {
          const el = document.getElementById(id);
          if (!el) return;
          el.addEventListener('touchstart', (e) => { e.preventDefault(); keys[keyName] = true; });
          el.addEventListener('touchend',   (e) => { e.preventDefault(); keys[keyName] = false; });
        };
        bindTouch('dpad-up', 'up');
        bindTouch('dpad-down', 'down');
        bindTouch('dpad-left', 'left');
        bindTouch('dpad-right', 'right');
        bindTouch('btn-action', 'action');
        // 暂停按钮
        const pauseBtn = document.getElementById('btn-pause');
        if (pauseBtn) {
          pauseBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            if (state === STATE.PLAY) state = STATE.PAUSE;
            else if (state === STATE.PAUSE) state = STATE.PLAY;
          });
        }
      }
      function handleTouchStarted() {
        // p5 touch 回调可用于 Canvas 内交互
      }

      // === 难度应用（V7 新增）===
      function applyDifficulty() {
        const cfg = difficultyConfig[difficulty];
        lives = cfg.lives;
        // speedMul 可在 drawPlay 中用于调节游戏速度
      }

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V7 p5.js 游戏模板（3D）</title>
  <!-- 三级 CDN 兜底：cdnjs → jsdelivr → 本地 vendor -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
  <script>
    if (typeof p5 === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
    }
    if (typeof p5 === 'undefined') {
      document.write('<script src="./vendor/p5.min.js"><\/script>');  // 本地兜底
    }
  </script>
  <style>/* HUD / select 样式 */</style>
</head>
<body>
  <div id="p5-container"></div>
  <select id="nodeSelect"><option value="-1">选择节点…</option></select>
  <script>
    const sketch = (p) => {
      // === 状态机（V7 新增 PAUSE 状态）===
      const STATE = { MENU: 0, PLAY: 1, PAUSE: 2, LEVEL_COMPLETE: 3, GAME_OVER: 4, VICTORY: 5 };
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
        else if (state === STATE.PAUSE) {
          // 暂停时不更新 3D 场景，仅绘制暂停遮罩
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

- 状态机 6 状态全部可达（MENU / PLAY / PAUSE / LEVEL_COMPLETE / GAME_OVER / VICTORY）
- **PAUSE 暂停状态**：Escape / P 键可触发暂停，暂停时游戏循环停止、显示"暂停"遮罩、提供"继续"和"退出"按钮；PLAY ↔ PAUSE 双向切换正常；PAUSE → MENU 退出正常
- **键盘操控**：方向键 / WASD 移动、Space 动作、Escape 暂停、Enter 确认，所有按键响应无延迟
- **触屏操控**：虚拟 D-pad 和动作按钮在触屏设备上可见且可用；touchstart/touchend 事件正确绑定
- **难度分级**：MENU 状态可选简单/普通/困难三档；不同难度影响速度、生命、提示等参数
- **文件体积**：单 HTML 文件 ≤ 200KB（备课 HTML ≤ 500KB）
- **CDN 兜底**：三级 CDN 兜底（cdnjs → jsdelivr → 本地 vendor）已配置
- INITIAL_STATE 显式声明（避免上次会话值残留）
- 得分逻辑闭环：每题答对确实加分、连击正确累计、等级正确升级
- HUD 实时同步（分数 / 等级 / 关卡 / 生命 / 难度）
- 2D 与 3D 坐标系不混淆（3D 必备 `p.resetMatrix()` + `p.camera()` 切回 2D HUD）
- 性能：60fps 流畅（draw 内无大对象创建）
- 不使用 p5 2.x 已移除 API（`screenX` / `screenY` / `modelX` / `modelY` 等）
- 3D 中文不在 WEBGL 内画（用 DOM HTML 信息层）
- 控件首选原生 DOM + `addEventListener`（p5 `createButton` 在实例模式 + 全局 `mousePressed` 共存时脆弱）

---

## 七·一、PAUSE 暂停状态机规范（V7 新增）

> 所有游戏必须实现 PAUSE 状态，确保玩家可随时暂停和恢复游戏。

### 状态转移图

```text
MENU ──Enter/点击开始──▶ PLAY
PLAY ──Escape / P / 暂停按钮──▶ PAUSE
PAUSE ──Escape / P / 继续按钮──▶ PLAY
PAUSE ──退出按钮──▶ MENU
PLAY ──lives ≤ 0──▶ GAME_OVER
PLAY ──通关──▶ LEVEL_COMPLETE ──下一关──▶ PLAY
LEVEL_COMPLETE ──全部通关──▶ VICTORY
GAME_OVER / VICTORY ──重玩──▶ MENU
```

### PAUSE 状态实现要点

1. **触发方式**：`Escape` 键、`P` 键、或画面上的暂停按钮（⏸ 图标）
2. **暂停时行为**：
   - `draw()` 中不执行游戏逻辑更新（角色不移动、计时器暂停）
   - 绘制半透明遮罩（如 `p.fill(0, 0, 0, 150); p.rect(0, 0, p.width, p.height);`）
   - 显示"暂停"大字
   - 提供"继续"按钮（恢复 PLAY）和"退出"按钮（返回 MENU）
3. **状态切换**：PLAY ↔ PAUSE 为双向切换（同一按键/按钮在两个状态下作用相反）
4. **音频**：暂停时静音背景音乐（如有）

---

## 七·二、难度分级系统（V7 新增）

> 所有游戏必须提供三档难度选择，让玩家根据自身水平调整挑战。

### 难度参数表

| 参数 | 简单 | 普通 | 困难 |
|------|------|------|------|
| 游戏速度倍率 | 0.7× | 1.0× | 1.5× |
| 初始生命数 | 5 | 3 | 1 |
| 提示功能 | ✅ 可用 | ❌ 不可用 | ❌ 不可用 |
| 答题时限 | 放宽 1.5× | 标准 | 缩短 0.7× |
| 得分倍率 | 0.8× | 1.0× | 1.5× |
| 标识颜色 | 绿色 (#4CAF50) | 橙色 (#FF9800) | 红色 (#F44336) |

### 难度选择界面

- 在 MENU 状态显示三个难度按钮（横向排列），默认选中"普通"
- 键盘操作：`←` / `→` 方向键切换难度，当前选中项高亮
- 触屏操作：直接点击难度按钮
- 选中后按 `Enter` 或点击"开始游戏"按钮进入游戏

### 难度配置代码范式

```javascript
// 难度配置（在 sketch 顶部定义）
const DIFFICULTY = { EASY: 0, NORMAL: 1, HARD: 2 };
let difficulty = DIFFICULTY.NORMAL;
const difficultyConfig = {
  [DIFFICULTY.EASY]:   { label: '简单', speedMul: 0.7, lives: 5, hints: true,  timeMul: 1.5, scoreMul: 0.8, color: '#4CAF50' },
  [DIFFICULTY.NORMAL]: { label: '普通', speedMul: 1.0, lives: 3, hints: false, timeMul: 1.0, scoreMul: 1.0, color: '#FF9800' },
  [DIFFICULTY.HARD]:   { label: '困难', speedMul: 1.5, lives: 1, hints: false, timeMul: 0.7, scoreMul: 1.5, color: '#F44336' }
};

// 开始游戏时应用难度
function applyDifficulty() {
  const cfg = difficultyConfig[difficulty];
  lives = cfg.lives;
  // 在 draw 中使用 cfg.speedMul 调节速度、cfg.timeMul 调节时限、cfg.scoreMul 调节得分
}
```

---

## 七·三、键盘与触屏操控实现指南（V7 新增）

> 所有游戏必须同时支持键盘和触屏操控，确保 PC / 平板 / 手机均可流畅游玩。

### 键盘操控规范

| 按键 | 游戏功能 |
|------|----------|
| `↑` / `W` | 向上移动 |
| `↓` / `S` | 向下移动 |
| `←` / `A` | 向左移动 |
| `→` / `D` | 向右移动 |
| `Space` | 动作 / 攻击 / 确认 |
| `Escape` / `P` | 暂停 / 继续 |
| `Enter` | 菜单确认 / 对话推进 |

### 触屏虚拟按键实现

触屏设备（手机/平板）需显示虚拟 D-pad 和操作按钮。实现方式：

1. **HTML 层**：在 `<body>` 中添加虚拟按键 DOM 元素（方向键 + 动作键 + 暂停键）
2. **CSS 层**：使用 `@media (hover: hover) and (pointer: fine)` 媒体查询，仅在触屏设备上显示虚拟按键
3. **JS 层**：为虚拟按键绑定 `touchstart` / `touchend` 事件，映射到与键盘相同的逻辑状态

```javascript
// 触屏虚拟按键绑定示例
function setupTouchControls() {
  const bindTouch = (elementId, keyName) => {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.addEventListener('touchstart', (e) => {
      e.preventDefault();  // 阻止触屏滚动干扰
      keys[keyName] = true;
    });
    el.addEventListener('touchend', (e) => {
      e.preventDefault();
      keys[keyName] = false;
    });
  };
  bindTouch('dpad-up', 'up');
  bindTouch('dpad-down', 'down');
  bindTouch('dpad-left', 'left');
  bindTouch('dpad-right', 'right');
  bindTouch('btn-action', 'action');
}
```

### ARIA 无障碍

- 所有虚拟按键需添加 `aria-label`（如 `aria-label="向上移动"`）
- 暂停按钮添加 `aria-label="暂停游戏"`
- Canvas 容器添加 `role="application"` 和描述性 `aria-label`

---

## 七·四、游戏文件体积限制（V7 新增）

> 与课件指南一致，游戏文件也必须严格控制体积。

### 体积上限

| 文件类型 | 体积上限 |
|----------|----------|
| 学生游戏（单 HTML） | **≤ 200KB** |
| 教师备课包游戏 HTML | **≤ 500KB** |

### 体积优化策略

1. **代码压缩**：移除多余空格和注释
2. **图片优化**：优先使用 CSS 绘制图形（渐变、形状）代替位图；必须用图时使用 SVG
3. **避免内嵌大资源**：音频使用 Web Audio API 程序化生成音效，不内嵌音频文件
4. **精简关卡数据**：关卡数据用紧凑格式存储，避免冗余字段
5. **CDN 加载依赖**：p5.js 通过 CDN 加载，不计入文件体积

---

## 七·五、按钮功能完整性测试（V8-AIPC 新增 · 强制门控 · 游戏专项）

> **V8-AIPC 红线**：游戏内**每一个按钮都必须经过实际点击验证，确保功能正常**——菜单按钮、难度按钮、暂停按钮、继续/退出按钮、答案按钮、技能按钮，无一例外。
> 本章是 `p5js-courseware-guide.md` 第三章·一"按钮功能完整性"在游戏场景的**专项扩展**，要求完全相同 + 额外覆盖游戏特有按钮（PAUSE 切换、难度选择、关卡跳跃）。

### 7-5.1 游戏按钮清单必须覆盖的最小集

```text
✅ 菜单按钮    ：btn-start / btn-help / btn-quit
✅ 难度按钮    ：btn-easy / btn-normal / btn-hard
✅ 暂停/继续   ：btn-pause / btn-resume
✅ 退出/重玩   ：btn-exit / btn-replay
✅ 答案/选项   ：btn-opt-0 / btn-opt-1 / btn-opt-2 / btn-opt-3  (4 选项)
✅ 下一关/结算 ：btn-next / btn-restart
```

任何游戏未在 HTML 注释块 `[BUTTON_REGISTRY]` 中声明以上 6 类按钮，**不得交付**。

### 7-5.2 7 项强制检查（同课件指南，但适配游戏）

| # | 检查项 | 游戏适配要点 |
|---|--------|--------------|
| B1 | 存在性 | MENU 状态隐藏的按钮（如 btn-resume 仅在 PAUSE 显示）须在切换后立即可被 `getElementById` 找到 |
| B2 | 可点击 | PAUSE 状态：MENU/PLAY 按钮应处于 `disabled=true` |
| B3 | 回调绑定 | 难度按钮 callback 必须调用 `applyDifficulty()`，否则后续 lives/speed 不生效 |
| B4 | 触发后状态变化 | 状态机 6 状态必须严格可迁移（MENU→PLAY→PAUSE→PLAY→GAME_OVER→MENU 等） |
| B5 | 重复点击稳定性 | 暂停按钮连点 3 次：PLAY→PAUSE→PLAY→PAUSE 不应崩溃 |
| B6 | 键盘等价性 | 每个按钮都有 `keydown` 桥接（Enter / Space / 方向键+Enter） |
| B7 | 触屏等价性 | D-pad 与动作按钮都需 `touchstart` 监听 |

### 7-5.3 游戏专项 B8 / B9 补充

| # | 检查项 | 通过标准 |
|---|--------|----------|
| B8 | **难度生效链** | 选 EASY → `lives=5, speedMul=0.7`；选 HARD → `lives=1, speedMul=1.5` |
| B9 | **状态机闭环** | 任意状态 → 任意状态（通过合法路径）必须可达成；PAUSE 不可直达 VICTORY |

### 7-5.4 测试与交付

- 自动化测试：`tests/test_p5js_buttons.py` 同时覆盖课件与游戏（按 `[BUTTON_REGISTRY]` 内 `type: courseware | game` 字段分支）
- 强制门控结果块（课件指南 7.5 + 本章 7-5.5）必须包含"游戏按钮 6 类最小集"勾选
- 任一 B1–B9 不通过 = **不得交付**

### 7-5.5 V8.1-AIPC 扩展：所有互动控件完整性门控（强制）

> **V8.1-AIPC 在 V8-AIPC button-only 基础上扩展到全控件**——游戏内除 button 外，
> 还需通过 slider / select / input / canvas / key / touch / drag 7 类扩展门控。

#### 7-5.5.1 游戏 12 类最小集（V8.1-AIPC 强制）

```text
✅ 按钮控件    ：btn-start / btn-help / btn-quit / btn-pause / btn-resume / btn-exit / btn-replay / btn-opt-0~3 / btn-next / btn-restart
✅ 滑块控件    ：sld-volume / sld-difficulty（必选）
✅ 下拉菜单    ：sel-character / sel-level（可选）
✅ 文本输入    ：inp-player-name（可选）
✅ Canvas 鼠标 ：cvs-play + mousedown/mousemove/mouseup
✅ 全局键盘    ：key-up / key-down / key-left / key-right / key-space / key-esc（至少 2 个）
✅ 触屏桥      ：tch-dpad / tch-pause（必选）
✅ 拖拽控件    ：dnd-paddle / dnd-knob（至少 1 个）
```

#### 7-5.5.2 12+ 项检查项

| 类别 | 检查 | 通过标准 |
|------|------|----------|
| button | B1-B5 + B6-B9 | V8-AIPC 9 项 |
| slider | S1 存在 / S2 范围 / S3 input 监听 / S4 重复 3 次无错 | 4 项 |
| select | Se1 存在 / Se2 选项非空 / Se3 change 监听 | 3 项 |
| input | I1 存在 / I2 input 监听 / I3 重复无错 | 3 项 |
| canvas | C1 存在 / C2 mousedown / C3 触发无错 / C4 拖拽链路 | 4 项 |
| key | K1 全局 keydown / K2 至少响应 1 键 | 2 项 |
| touch | T1 全局 touchstart | 1 项（课件软要求） |
| drag | D1 mousedown→mousemove→mouseup 链路 | 1 项 |

合计：**9（B）+ 4（S）+ 3（Se）+ 3（I）+ 4（C）+ 2（K）+ 1（T）+ 1（D）= 27 项**

#### 7-5.5.3 自动化测试

- `tests/test_p5js_interactive.py`（V8.1-AIPC 新增）36 项测试，全部独立通过
- `tests/test_p5js_buttons.py`（V8-AIPC）29 项保持不变，向后兼容

#### 7-5.5.4 迁移要点

| 旧 V8-AIPC 写法 | V8.1-AIPC 写法 |
|------------------|------------------|
| `[BUTTON_REGISTRY]` 仅声明 button | `[INTERACTIVE_REGISTRY]` 声明 button + slider + select + input + canvas + key + touch + drag |
| 仅 button 6 类最小集 | button 6 类 + 控件 12 类（共 18 类） |
| 9 项 B1-B9 门控 | 9 项 B1-B9 + 18 项扩展门控 = 27 项 |

#### 7-5.5.5 交付物门控结果块

```
[互动控件完整性 V8.1-AIPC]
- 声明控件数:  X
- 通过控件数:  X (B1-B5 + S1-S4 + Se1-Se3 + I1-I3 + C1-C4 + K1-K2 + T1 + D1)
- 失败控件:    [ctrl-id] → ? 不通过 (原因)
- 自动化测试:  tests/test_p5js_interactive.py 退出码 0 (36/36)
- 浏览器实测:  ✅ / ⏳ (请用户实测)
```

---

## 八、常见坑与解法

| 坑 | 解法 |
|----|------|
| 状态机遗漏 GAME_OVER / VICTORY / PAUSE | 显式声明 6 状态（含 PAUSE）；状态转移表覆盖每对 |
| 初始值残留（上次会话 left-over） | setup 顶部强制重置所有全局变量 |
| draw 内创建对象致卡顿 | 提取到 setup 或对象池复用 |
| 3D HUD 坐标系错乱 | 绘制 HUD 前 `p.resetMatrix()` + `p.camera()` |
| 3D 节点点击拾取用 `screenX` | 用「下拉列表」或「selectedIndex」替代 |
| 连击 / 速度计算写死边界 | 公式封装为 `computeScore(...)` 函数可测试 |
| 等级不联动 HUD | HUD 绘制函数始终从 `score` 重新计算 level |
| 暂停后游戏逻辑仍在运行 | PAUSE 状态下 draw 中跳过游戏逻辑更新，仅绘制遮罩 |
| 触屏虚拟按键不显示 | 检查 CSS 媒体查询是否正确匹配触屏设备；确认 z-index 高于 Canvas |
| 难度切换未生效 | applyDifficulty() 必须在状态切换到 PLAY 前调用 |
| 文件体积超标 | 用压缩工具检查；移除冗余注释/空格；图片转 SVG 或 CSS 绘制 |

## 九、与 V3 课件的衔接

- 游戏中的「问答弹窗」与 V3 课件的「控制面板」风格统一
- 游戏的「关卡」与 V3 课件的「章节」对应；可互相引用
- 游戏的「知识图谱回顾」可作为 V3 课件的「教学要点总结」扩展
- 同一课程可同时输出：1 套课件（V3）+ 1 套游戏（V4）+ 1 套备课包（V4）三位一体

## 十、典型 30 分钟出活清单

1. 选 A/B/C/D 中一个模块（如 A1）
2. 列出 5–10 个核心知识点（作为关卡 / 题目）
3. 选 2D 或 3D
4. 套用第五 / 六节模板（含三级 CDN 兜底）
5. 填 `levels` 数组（题目 + 答案）
6. 配置难度分级（简单/普通/困难参数）
7. 实现 PAUSE 暂停状态 + 键盘/触屏操控
8. 加 CSS 美化 HUD
9. 检查文件体积 ≤ 200KB
10. 走强制测试门控（含 V7 新增项）
11. `node --check` 语法验证
12. 浏览器实测（启动 → 选难度 → 通关 → 暂停/继续 → 结算）
13. 触屏设备实测（虚拟 D-pad 操控）
14. 交付

## 十一、跨能力避坑参考（与 p5.js 互动课件完全一致）

以下陷阱在课件与游戏中**同样致命**，开发游戏时必须与课件避坑保持一致：

| 陷阱 | 在游戏中常见误用 | 课件指南原文位置 |
|------|------------------|------------------|
| `screenX / screenY` 在 2.x 移除 | 3D 节点点击拾取 → `TypeError` | 课件指南第三章黑名单项 |
| `modelX / modelY / modelZ` 在 2.x 移除 | 模型↔屏幕坐标互转 → 崩溃 | 同上 |
| WEBGL 中文不显示 | 游戏 HUD / 弹窗显示中文 → 渲染空白 | 课件指南第九项测试清单 |
| draw 内创建对象 | 游戏对象 / 粒子数组创建 → 帧率暴跌 | 课件指南 7.1 静态自检 |
| 实例模式混用全局式 | 课件/游戏中常见 `background()` 裸写 → 静默失败 | 课件指南第三章测试清单第 4 项 |
| 状态机遗漏 `GAME_OVER / VICTORY / PAUSE` | 游戏只玩到一半或卡死、无法暂停 | 本文第七章专项检查 |
| HUD 不联动得分变化 | 玩家看不到分数实时更新 | 本文第二章 + 第七章 |
| CDN 单点故障 | 仅配一个 CDN 源，不可达时白屏 | 课件指南代码引入标准（三级兜底） |
| 文件体积超标 | 内嵌大量图片/音频致 HTML 超 200KB | 课件指南六·二 + 本文七·四 |
| 缺少键盘/触屏支持 | 仅支持鼠标操作，手机/平板无法玩 | 课件指南六·一 + 本文七·三 |

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
