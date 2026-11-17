#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T4 前置 · 生成 OPS-5「模块轮转课件」场景产物
============================================
目的：验证 V7.0 新增的 OPS-5 运营流能真实产出可被 harness 实测通过的产物。
选取 V6 产物尚未覆盖的轮转单元：
  · B1  → 课件（普通单元，不叠加游戏）
  · G3  → 课件 + 配套游戏（G 组，按 OPS-5 规则必须叠加游戏）
严格遵循 p5js 课件契约：实例模式 / 响应式 / CDN 降级 / 中文注释 / 全控件可实测。
"""
import os, pathlib

# 路径自适应：输出目录由脚本位置推导，可用 V7_TEST_OUT 覆盖
OUT = os.environ.get("V7_TEST_OUT") or str(pathlib.Path(__file__).resolve().parent / "out")
OUT = os.path.join(OUT, "artifacts")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  /* ---------- 基础布局：响应式，课件区 + 控制区 ---------- */
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family:"Microsoft YaHei","PingFang SC",sans-serif;
         background:#0e1030; color:#e8ecff; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:18px; }}
  header {{ padding:14px 18px; border-radius:12px; margin-bottom:14px;
            background:linear-gradient(120deg,#6C5CFF,#00E0C6); color:#0b0d24; }}
  header h1 {{ margin:0; font-size:20px; }}
  header p {{ margin:6px 0 0; font-size:13px; opacity:.85; }}
  .stage {{ display:flex; gap:16px; flex-wrap:wrap; }}
  #canvasBox {{ flex:1 1 460px; min-height:380px; background:#151a44;
                border-radius:12px; padding:8px; display:flex;
                align-items:center; justify-content:center; }}
  .panel {{ flex:0 0 300px; background:#151a44; border-radius:12px; padding:14px; }}
  .row {{ margin-bottom:12px; }}
  .row label {{ display:block; font-size:13px; margin-bottom:6px; opacity:.9; }}
  button {{ background:#6C5CFF; color:#fff; border:0; border-radius:8px;
            padding:8px 12px; margin:0 6px 6px 0; cursor:pointer; font-size:13px; }}
  button:hover {{ background:#8577ff; }}
  button.ghost {{ background:transparent; border:1px solid #6C5CFF; color:#b9b2ff; }}
  select, input[type=range] {{ width:100%; }}
  select {{ padding:6px; border-radius:6px; background:#0e1030; color:#e8ecff;
            border:1px solid #6C5CFF; }}
  .hint {{ font-size:12px; opacity:.75; line-height:1.7; margin-top:10px;
           border-top:1px dashed #3a4180; padding-top:10px; }}
  .fallback {{ color:#ffd166; font-size:13px; padding:10px; text-align:center; }}
  @media (max-width:820px) {{
    .stage {{ flex-direction:column; }}
    .panel {{ flex:1 1 auto; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </header>
  <div class="stage">
    <div id="canvasBox"><div id="fb" class="fallback" style="display:none">
      ⚠️ p5.js CDN 加载失败，已降级：核心交互控件仍可正常使用。</div></div>
    <div class="panel">
{panel}
      <div class="hint">{hint}</div>
    </div>
  </div>
</div>

<!-- p5.js：CDN 加载；失败时由脚本检测并降级，保证控件不失效 -->
<script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
<script>
{script}
</script>
</body>
</html>
"""

# ----------------------------------------------------------------- B1 课件
B1_PANEL = """      <div class="row">
        <label>第 <span id="stepNo">1</span> / 4 步：大模型是怎么「猜」下一个字的</label>
        <input type="range" id="speed" min="1" max="10" value="5" aria-label="演示速度">
      </div>
      <div class="row">
        <label>观察视角</label>
        <select id="view" aria-label="观察视角">
          <option value="token">词元流</option>
          <option value="prob">概率分布</option>
          <option value="attn">注意力权重</option>
        </select>
      </div>
      <div class="row">
        <button id="prev" type="button">上一步</button>
        <button id="next" type="button">下一步</button>
        <button id="play" type="button">自动播放</button>
        <button id="reset" class="ghost" type="button">重置</button>
      </div>
      <div class="row">
        <label><input type="checkbox" id="showLabel" aria-label="显示中文标注"> 显示中文标注</label>
      </div>"""

B1_SCRIPT = """
/* ===== B1 单元课件：大模型推理过程可视化（p5 实例模式） ===== */
(function () {
  var step = 1, playing = false, view = 'token', showLabel = true, speed = 5;
  var STEPS = 4;

  // ---- DOM 控件绑定（全部做存在性判断，缺元素也不报错） ----
  var $ = function (id) { return document.getElementById(id); };
  var stepNo = $('stepNo'), speedEl = $('speed'), viewEl = $('view'),
      labelEl = $('showLabel');

  function sync() { if (stepNo) stepNo.textContent = String(step); }

  if (speedEl) speedEl.addEventListener('input', function () {
    speed = Number(this.value) || 5;
  });
  if (viewEl) viewEl.addEventListener('change', function () { view = this.value; });
  if (labelEl) labelEl.addEventListener('change', function () { showLabel = this.checked; });

  var btnPrev = $('prev'), btnNext = $('next'), btnPlay = $('play'), btnReset = $('reset');
  if (btnPrev) btnPrev.addEventListener('click', function () {
    step = step > 1 ? step - 1 : STEPS; sync();
  });
  if (btnNext) btnNext.addEventListener('click', function () {
    step = step < STEPS ? step + 1 : 1; sync();
  });
  if (btnPlay) btnPlay.addEventListener('click', function () {
    playing = !playing; this.textContent = playing ? '暂停播放' : '自动播放';
  });
  if (btnReset) btnReset.addEventListener('click', function () {
    step = 1; playing = false; if (btnPlay) btnPlay.textContent = '自动播放'; sync();
  });
  sync();

  // ---- p5 降级检测：CDN 不可用时只显示提示，不抛错 ----
  var box = $('canvasBox'), fb = $('fb');
  if (typeof window.p5 === 'undefined') {
    if (fb) fb.style.display = 'block';
    return;
  }

  // ---- p5 实例模式草图 ----
  var sketch = function (p) {
    var tokens = ['今天', '天气', '很', '好', '我们', '去', '公园'];
    var t = 0;

    p.setup = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      var c = p.createCanvas(w, 360);
      if (c && c.parent && box) c.parent(box);
      p.textFont('sans-serif');
    };

    p.windowResized = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      p.resizeCanvas(w, 360);
    };

    p.draw = function () {
      p.background(21, 26, 68);
      if (playing) { t += speed * 0.01; if (t > 1) { t = 0; step = step < STEPS ? step + 1 : 1; sync(); } }

      var n = Math.min(tokens.length, step + 2);   // 随步骤显示更多词元
      var bw = 84, gap = 14;
      var startX = (p.width - (n * bw + (n - 1) * gap)) / 2;

      for (var i = 0; i < n; i++) {
        var x = startX + i * (bw + gap), y = 120;
        var isLast = (i === n - 1);

        if (view === 'prob') {
          // 概率分布视角：柱状高度表示候选概率
          var h = 30 + (i + 1) * 14;
          p.noStroke(); p.fill(isLast ? p.color(0, 224, 198) : p.color(108, 92, 255, 170));
          p.rect(x, y + 60 - h, bw - 10, h, 6);
        } else if (view === 'attn') {
          // 注意力视角：连线粗细表示权重
          p.stroke(0, 224, 198, 200);
          p.strokeWeight(1 + (i + 1) * 0.8);
          p.line(p.width / 2, y + 150, x + bw / 2 - 5, y + 20);
          p.noStroke();
        }

        p.fill(isLast ? p.color(0, 224, 198) : p.color(232, 236, 255));
        p.rect(x, y, bw - 10, 46, 8);
        p.fill(14, 16, 48);
        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(16);
        p.text(tokens[i], x + (bw - 10) / 2, y + 23);

        if (showLabel) {
          p.fill(185, 178, 255);
          p.textSize(11);
          p.text(i === 0 ? '输入' : (isLast ? '预测中' : '已生成'),
                 x + (bw - 10) / 2, y + 62);
        }
      }

      p.fill(185, 178, 255);
      p.textSize(13);
      p.textAlign(p.CENTER, p.CENTER);
      p.text('第 ' + step + '/' + STEPS + ' 步 · ' +
             (view === 'token' ? '词元流' : (view === 'prob' ? '概率分布' : '注意力权重')),
             p.width / 2, 300);
    };

    // 画布内交互：点击推进步骤（供 harness 烟雾测试）
    p.mousePressed = function () {
      if (p.mouseX >= 0 && p.mouseX <= p.width && p.mouseY >= 0 && p.mouseY <= p.height) {
        step = step < STEPS ? step + 1 : 1; sync();
      }
    };
    p.keyPressed = function () {
      if (p.keyCode === p.RIGHT_ARROW) { step = step < STEPS ? step + 1 : 1; sync(); }
      else if (p.keyCode === p.LEFT_ARROW) { step = step > 1 ? step - 1 : STEPS; sync(); }
      else if (String(p.key).toLowerCase() === 'r') { step = 1; sync(); }
    };
  };

  try { new window.p5(sketch); } catch (e) {
    if (fb) { fb.style.display = 'block'; fb.textContent = '⚠️ 画布初始化失败，已降级：控件可用。'; }
  }
})();
"""

# ----------------------------------------------------------------- G3 课件
G3_PANEL = """      <div class="row">
        <label>AI 治理章节 <span id="chapNo">1</span> / 3：风险分级与责任划分</label>
        <input type="range" id="risk" min="1" max="10" value="4" aria-label="风险等级">
      </div>
      <div class="row">
        <label>治理主体</label>
        <select id="actor" aria-label="治理主体">
          <option value="gov">政府监管</option>
          <option value="ent">企业自治</option>
          <option value="pub">公众监督</option>
        </select>
      </div>
      <div class="row">
        <button id="prev" type="button">上一章</button>
        <button id="next" type="button">下一章</button>
        <button id="case" type="button">切换案例</button>
        <button id="reset" class="ghost" type="button">重置</button>
      </div>
      <div class="row">
        <label><input type="checkbox" id="showDuty" aria-label="显示责任链条"> 显示责任链条</label>
      </div>"""

G3_SCRIPT = """
/* ===== G3 单元课件：AI 治理风险分级可视化（p5 实例模式） ===== */
(function () {
  var chap = 1, risk = 4, actor = 'gov', showDuty = true, caseIdx = 0;
  var CHAPS = 3;
  var CASES = ['深度伪造', '算法歧视', '数据泄露', '自动驾驶事故'];
  var ACTORS = { gov: '政府监管', ent: '企业自治', pub: '公众监督' };

  var $ = function (id) { return document.getElementById(id); };
  var chapNo = $('chapNo'), riskEl = $('risk'), actorEl = $('actor'), dutyEl = $('showDuty');

  function sync() { if (chapNo) chapNo.textContent = String(chap); }
  if (riskEl) riskEl.addEventListener('input', function () { risk = Number(this.value) || 4; });
  if (actorEl) actorEl.addEventListener('change', function () { actor = this.value; });
  if (dutyEl) dutyEl.addEventListener('change', function () { showDuty = this.checked; });

  var bPrev = $('prev'), bNext = $('next'), bCase = $('case'), bReset = $('reset');
  if (bPrev) bPrev.addEventListener('click', function () { chap = chap > 1 ? chap - 1 : CHAPS; sync(); });
  if (bNext) bNext.addEventListener('click', function () { chap = chap < CHAPS ? chap + 1 : 1; sync(); });
  if (bCase) bCase.addEventListener('click', function () { caseIdx = (caseIdx + 1) % CASES.length; });
  if (bReset) bReset.addEventListener('click', function () { chap = 1; caseIdx = 0; sync(); });
  sync();

  var box = $('canvasBox'), fb = $('fb');
  if (typeof window.p5 === 'undefined') { if (fb) fb.style.display = 'block'; return; }

  var sketch = function (p) {
    p.setup = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      var c = p.createCanvas(w, 360);
      if (c && c.parent && box) c.parent(box);
      p.textFont('sans-serif');
    };
    p.windowResized = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      p.resizeCanvas(w, 360);
    };
    p.draw = function () {
      p.background(21, 26, 68);
      // 风险分级热力条：风险越高红色越深
      var seg = 10, bw = p.width / (seg + 2);
      for (var i = 0; i < seg; i++) {
        var on = i < risk;
        var r = on ? p.map(i, 0, seg, 90, 240) : 40;
        var g = on ? p.map(i, 0, seg, 200, 70) : 44;
        p.noStroke(); p.fill(r, g, 120, on ? 230 : 90);
        p.rect(bw + i * bw, 70, bw - 6, 54, 5);
      }
      p.fill(232, 236, 255); p.textSize(13); p.textAlign(p.CENTER, p.CENTER);
      p.text('风险等级 ' + risk + ' / 10', p.width / 2, 150);

      p.fill(0, 224, 198); p.textSize(15);
      p.text('案例：' + CASES[caseIdx] + '　｜　主体：' + ACTORS[actor], p.width / 2, 190);

      if (showDuty) {
        // 责任链条：开发 → 部署 → 使用 → 监管
        var chain = ['开发方', '部署方', '使用者', ACTORS[actor]];
        var cw = p.width / (chain.length + 1);
        for (var j = 0; j < chain.length; j++) {
          var x = cw * (j + 1);
          p.fill(108, 92, 255, 200); p.rect(x - 44, 240, 88, 40, 8);
          p.fill(255); p.textSize(12); p.text(chain[j], x, 260);
          if (j > 0) { p.stroke(185, 178, 255); p.strokeWeight(2);
                       p.line(x - 44, 260, x - 44 - (cw - 88), 260); p.noStroke(); }
        }
      }
      p.fill(185, 178, 255); p.textSize(12);
      p.text('第 ' + chap + '/' + CHAPS + ' 章', p.width / 2, 320);
    };
    p.mousePressed = function () {
      if (p.mouseX >= 0 && p.mouseX <= p.width && p.mouseY >= 0 && p.mouseY <= p.height) {
        caseIdx = (caseIdx + 1) % CASES.length;
      }
    };
    p.keyPressed = function () {
      if (p.keyCode === p.RIGHT_ARROW) { chap = chap < CHAPS ? chap + 1 : 1; sync(); }
      else if (p.keyCode === p.LEFT_ARROW) { chap = chap > 1 ? chap - 1 : CHAPS; sync(); }
    };
  };

  try { new window.p5(sketch); } catch (e) {
    if (fb) { fb.style.display = 'block'; fb.textContent = '⚠️ 画布初始化失败，已降级：控件可用。'; }
  }
})();
"""

# ----------------------------------------------------------------- G3 游戏
G3_GAME_PANEL = """      <div class="row">
        <label>治理闯关：得分 <span id="score">0</span> ｜ 剩余 <span id="life">3</span></label>
        <input type="range" id="diff" min="1" max="5" value="2" aria-label="难度">
      </div>
      <div class="row">
        <label>关卡主题</label>
        <select id="theme" aria-label="关卡主题">
          <option value="privacy">隐私保护</option>
          <option value="fair">算法公平</option>
          <option value="safe">安全可靠</option>
        </select>
      </div>
      <div class="row">
        <button id="start" type="button">开始</button>
        <button id="pause" type="button">暂停</button>
        <button id="restart" class="ghost" type="button">重开</button>
      </div>
      <div class="row">
        <label><input type="checkbox" id="sound" aria-label="音效提示"> 音效提示（开关）</label>
      </div>"""

G3_GAME_SCRIPT = """
/* ===== G3 配套游戏：治理风险闯关（p5 实例模式） ===== */
(function () {
  var score = 0, life = 3, diff = 2, theme = 'privacy', sound = false;
  var running = false, paused = false;
  var targets = [], tick = 0;

  var $ = function (id) { return document.getElementById(id); };
  var scoreEl = $('score'), lifeEl = $('life');
  function sync() {
    if (scoreEl) scoreEl.textContent = String(score);
    if (lifeEl) lifeEl.textContent = String(life);
  }

  var diffEl = $('diff'), themeEl = $('theme'), soundEl = $('sound');
  if (diffEl) diffEl.addEventListener('input', function () { diff = Number(this.value) || 2; });
  if (themeEl) themeEl.addEventListener('change', function () { theme = this.value; reset(); });
  if (soundEl) soundEl.addEventListener('change', function () { sound = this.checked; });

  var TH = { privacy: '隐私保护', fair: '算法公平', safe: '安全可靠' };

  function reset() {
    targets = []; score = 0; life = 3; tick = 0;
    for (var i = 0; i < 3 + diff; i++) {
      targets.push({ x: 60 + i * 90, y: 120 + (i % 3) * 60, r: 22 + (i % 3) * 6,
                     vy: 0.4 + diff * 0.15, hit: false });
    }
    sync();
  }

  var bStart = $('start'), bPause = $('pause'), bRestart = $('restart');
  if (bStart) bStart.addEventListener('click', function () { running = true; paused = false; reset(); });
  if (bPause) bPause.addEventListener('click', function () { paused = !paused; });
  if (bRestart) bRestart.addEventListener('click', function () { reset(); running = true; paused = false; });
  reset();

  var box = $('canvasBox'), fb = $('fb');
  if (typeof window.p5 === 'undefined') { if (fb) fb.style.display = 'block'; return; }

  var sketch = function (p) {
    p.setup = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      var c = p.createCanvas(w, 360);
      if (c && c.parent && box) c.parent(box);
      p.textFont('sans-serif');
    };
    p.windowResized = function () {
      var w = box ? Math.max(320, box.clientWidth - 16) : 640;
      p.resizeCanvas(w, 360);
    };
    p.draw = function () {
      p.background(21, 26, 68);
      p.fill(185, 178, 255); p.textSize(13); p.textAlign(p.LEFT, p.CENTER);
      p.text('主题：' + TH[theme] + '　难度：' + diff + '　' +
             (running ? (paused ? '已暂停' : '进行中') : '未开始'), 16, 24);

      if (!running) {
        p.fill(0, 224, 198); p.textSize(16); p.textAlign(p.CENTER, p.CENTER);
        p.text('点击「开始」进入治理闯关', p.width / 2, p.height / 2);
        return;
      }
      if (paused) {
        p.fill(255, 209, 102); p.textSize(16); p.textAlign(p.CENTER, p.CENTER);
        p.text('已暂停', p.width / 2, p.height / 2);
        return;
      }

      tick++;
      // 风险靶标下落：点中得分，漏掉扣命
      for (var i = 0; i < targets.length; i++) {
        var t = targets[i];
        if (t.hit) continue;
        t.y += t.vy * (1 + diff * 0.1);
        if (t.y > p.height - 20) { t.hit = true; life = Math.max(0, life - 1); sync(); }
        p.noStroke();
        p.fill(t.y > p.height - 90 ? p.color(255, 120, 120) : p.color(0, 224, 198));
        p.ellipse(t.x % (p.width - 40) + 20, t.y, t.r * 2, t.r * 2);
      }
      if (targets.length && targets.every(function (t) { return t.hit; })) {
        if (life > 0) { score += 10; reset(); running = true; } else { running = false; }
        sync();
      }
      p.fill(232, 236, 255); p.textSize(13); p.textAlign(p.CENTER, p.CENTER);
      p.text('得分 ' + score + '　剩余机会 ' + life, p.width / 2, p.height - 16);
    };

    // 画布交互：点击命中靶标
    p.mousePressed = function () {
      if (!running || paused) return;
      for (var i = 0; i < targets.length; i++) {
        var t = targets[i];
        if (t.hit) continue;
        var tx = t.x % (p.width - 40) + 20;
        if (p.dist(p.mouseX, p.mouseY, tx, t.y) < t.r + 6) {
          t.hit = true; score += 5; sync();
        }
      }
    };
    p.keyPressed = function () {
      var k = String(p.key || '').toLowerCase();
      if (k === 'p') { paused = !paused; }
      else if (k === 'r') { reset(); running = true; paused = false; }
      else if (k === ' ') { running = true; paused = false; }
    };
  };

  try { new window.p5(sketch); } catch (e) {
    if (fb) { fb.style.display = 'block'; fb.textContent = '⚠️ 画布初始化失败，已降级：控件可用。'; }
  }
})();
"""

def build(fname, title, subtitle, panel, hint, script):
    html = HEAD.replace("{title}", title).replace("{subtitle}", subtitle) \
               .replace("{panel}", panel).replace("{hint}", hint) \
               .replace("{script}", script)
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {fname}  ({len(html)} 字符)")
    return path

print("生成 OPS-5 轮转场景产物：")
build("ops5-B1-courseware.html", "B1 · 大模型是怎么工作的（互动课件）",
      "OPS-5 模块轮转课件 · 单元 B1 · 词元流 / 概率分布 / 注意力三视角",
      B1_PANEL, "操作提示：拖动滑块调速度，切换视角观察推理过程；"
                "画布内点击或按 ←/→ 可切换步骤，按 R 重置。", B1_SCRIPT)

build("ops5-G3-courseware.html", "G3 · AI 治理与风险分级（互动课件）",
      "OPS-5 模块轮转课件 · 单元 G3 · 风险热力条 + 责任链条",
      G3_PANEL, "操作提示：调节风险等级观察热力变化；切换案例与治理主体；"
                "勾选显示责任链条。画布内点击切换案例。", G3_SCRIPT)

build("ops5-G3-game.html", "G3 · 治理风险闯关（配套游戏）",
      "OPS-5 配套游戏 · G 组单元按规则叠加产出",
      G3_GAME_PANEL, "玩法：点「开始」后点击下落的风险靶标得分，漏掉扣机会；"
                     "空格开始 / P 暂停 / R 重开。", G3_GAME_SCRIPT)

# ---------------------------------------------------------------- 负例产物
# 目的：验证「强制测试门控」确实能拦下坏产物，而不是一律放行。
# 设计：4 个控件中 2 个故意损坏 ——
#   ① 损坏按钮 A：回调引用未定义函数 → 触发后产生 JS 报错
#   ② 损坏按钮 B：点击后移除自身     → 触发后控件消失
#   其余 2 个正常，用于确认门控是「按控件判定」而非「一律判失败」。
# 期望 harness 结果：exit=2 且 fail>0。
NEG_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>负例 · 故意损坏的控件</title>
<style>
  body{font-family:system-ui,-apple-system,"Microsoft YaHei",sans-serif;
       background:#12121a;color:#eee;padding:24px;line-height:1.7}
  button{padding:8px 14px;margin:6px 6px 6px 0;background:#2b2b3d;color:#eee;
         border:1px solid #555;border-radius:6px;cursor:pointer}
  .row{margin:12px 0}
  code{background:#2b2b3d;padding:2px 6px;border-radius:4px}
</style>
</head>
<body>
<h1>负例产物 · 用于验证强制测试门控能拦下坏控件</h1>
<p>本文件<strong>故意</strong>包含 2 个损坏控件。期望 harness 判定：<code>exit=2 且 fail&gt;0</code>。</p>

<div class="row">
  <button id="okBtn">正常按钮（应通过）</button>
  <span id="okOut">未点击</span>
</div>

<div class="row">
  <button id="badBtn">损坏按钮 A（回调引用未定义函数 → JS 报错）</button>
</div>

<div class="row">
  <label>正常滑块（应通过）<input type="range" id="okRange" min="0" max="100" value="50"></label>
</div>

<div class="row">
  <button id="vanishBtn">损坏按钮 B（点击后移除自身 → 控件消失）</button>
</div>

<script>
document.getElementById('okBtn').addEventListener('click', function () {
  document.getElementById('okOut').textContent = '已点击：' + new Date().toLocaleTimeString();
});

// 故意：notDefinedHandler 从未定义，点击时抛 ReferenceError
document.getElementById('badBtn').addEventListener('click', function () {
  notDefinedHandler();
});

// 故意：点击后把按钮自身从 DOM 移除
document.getElementById('vanishBtn').addEventListener('click', function () {
  this.remove();
});
</script>
</body>
</html>
"""

neg_path = os.path.join(OUT, "neg-broken.html")
open(neg_path, "w", encoding="utf-8").write(NEG_HTML)
print("  ✅ 负例产物（含 2 个故意损坏控件）：" + os.path.basename(neg_path))

print(f"\n输出目录：{OUT}")
