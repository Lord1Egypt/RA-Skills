# 无障碍HTML游戏开发规范（针对屏幕阅读器）

> 沉淀自双人蛇棋开发实践，适配国内争渡读屏、NVDA、JAWS，兼顾全盲、低视力、明眼陪伴

---

## 一、兼容性基础

### 支持的屏幕阅读器
- 桌面端：争渡读屏、NVDA、JAWS、Windows讲述人
  - 都支持标准ARIA语义，标准写法就是最好兼容
  - 争渡对标准ARIA grid支持完善，无需特殊hack
- iOS VoiceOver：如需支持请单独分版本，本规范针对桌面

### 核心原则
1. **全盲用户体验优先**，兼顾低视力和明眼陪伴
2. 所有操作必须能通过**键盘+屏幕阅读器**完成，不需要鼠标
3. 每个可交互元素必须让读屏读出**完整准确的当前信息**
4. 视觉美观辅助理解，不影响读屏操作

---

## 二、页面整体结构

### 起始页设计（推荐）
```html
<body class="start-page-active">
<div id="startPage" class="start-page" role="document" tabindex="0" 
      aria-label="[这里放完整的游戏说明]">
  <!-- 游戏标题、简介、规则、操作说明 -->
  <button id="startGameBtn">开始游戏</button>
</div>
<div id="gamePage" style="display: none;">
  <!-- 游戏主体 -->
</div>
```

**设计要点：**
1. 页面加载后起始页自动聚焦，读屏一次性朗读完整说明
2. 用户听完按**回车键直接开始游戏**，体验流畅
3. 起始页用**深色模式**，护眼适合长时间听：
   ```css
   body.start-page-active {
     background: #121212;
     color: #e0e0e0;
   }
   ```
4. 进入游戏后切换为**浅色模式**，方便看棋盘：
   ```css
   body.game-page-active {
     background: #ffffff;
     color: #333;
   }
   ```

---

## 三、ARIA语义规范

### 网格/棋盘游戏
```html
<table id="board" role="grid" aria-label="[棋盘描述：N行N列，方位说明]">
  <tr role="row">
    <td id="cell-1" role="gridcell" tabindex="0" 
          aria-label="[完整描述：编号 + 类型 + 特殊信息 + 棋子信息]">
    </td>
    ...
  </tr>
  ...
</table>
```

**必须：**
- `<table>` → `role="grid"`
- `<tr>` → `role="row"`
- `<td>` → `role="gridcell"`
- 每个格子 → `tabindex="0"` 允许键盘聚焦
- 每个格子给唯一id `id="cell-N"` 方便JS定位

### aria-label内容格式（每个可聚焦格子）
必须包含所有信息：
```
[编号] + [格子类型] + [特殊连接信息] + [动态棋子/状态信息]
```
**示例：**
```
"26号，梯子起点，会向上爬到 57 号格，有红色玩家"
```

### 模态对话框
```html
<div id="modal" role="dialog" aria-labelledby="modal-title" aria-modal="true">
  <div class="modal-content">
    <h3 id="modal-title">对话框标题</h3>
    <!-- 内容 -->
  </div>
</div>
```

**打开对话框后：** 自动聚焦第一个可交互按钮

### 选项选择设计（推荐按钮方案）
**不要**用单选按钮+确认按钮（两步容易卡）：
```html
<!-- ❌ 不推荐 -->
<input type="radio" name="mode"> 选项一
<button>确认</button>
```

**推荐**直接用两个带完整说明的按钮：
```html
<!-- ✅ 推荐 -->
<button id="opt1">选项一<br><small>说明文字</small></button>
<button id="opt2">选项二<br><small>说明文字</small></button>
```
- 点击直接执行，一步到位
- 每个按钮自带完整说明，读屏读到就知道是什么

### 状态播报区域
```html
<div id="status" role="status" aria-live="assertive"></div>
```
- 每次游戏状态变化，更新这里的文字
- 读屏会自动播报，用户即时知道结果

---

## 四、JavaScript动态更新规范

### aria-label动态更新（核心重点）
**正确做法：**
```javascript
function updateAllAria() {
  // 1. 先重置所有元素到基础状态（不带动态信息）
  for (每个格子) {
    cell.setAttribute('aria-label', getBaseLabel(cell));
  }
  // 2. 再给有动态信息的元素追加
  for (每个有棋子的格子) {
    let label = cell.getAttribute('aria-label');
    cell.setAttribute('aria-label', label + '，有红色玩家');
  }
}
```

**必须避免的错误：**
| 错误 | 后果 |
|------|------|
| 只改DOM视觉，不改aria-label | 读屏信息和视觉不一致 |
| 只改变化的格子，不改移出棋子的格子 | 信息仍然错误 |
| 动态信息放父元素，格子自己没有 | 用户聚焦格子读不到，需要额外导航 |

**配合状态播报：**
- 格子aria-label给用户浏览时看细节
- 状态区域播报本轮结果，用户不用听完细节也知道发生了什么

---

## 五、键盘快捷键规范

### 基本原则
1. 常用操作给 `accesskey="x"` → `Alt+X` 快速定位
2. 按钮文字标注快捷键：`<button accesskey="r">掷骰子(Alt+R)</button>`
3. 空格键激活主操作（当对应按钮聚焦时）
4. 全局快捷键给常用查询操作

### 示例
```html
<button id="rollDiceBtn" accesskey="r">掷骰子(Alt+R)</button>
<button id="readPositionsBtn" accesskey="p">读当前位置(Alt+P)</button>
```

```javascript
document.addEventListener('keydown', (e) => {
  // 空格键：聚焦掷骰子按钮时触发
  if (e.key === ' ' && document.activeElement === rollDiceBtn && gameStarted) {
    e.preventDefault();
    rollDice();
  }
  // Alt+P：全局朗读当前位置
  if (e.key.toLowerCase() === 'p' && e.altKey) {
    e.preventDefault();
    readPositions();
  }
});
```

---

## 六、CSS视觉适配（兼顾低视力）

### 焦点必须清晰
```css
#board td:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}
button:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}
```

### 格子类型颜色区分
```css
td.ladder { background-color: rgba(168, 230, 207, 0.7); } /* 梯子 - 浅绿色 */
td.snake { background-color: rgba(255, 139, 148, 0.7); } /* 蛇 - 浅红色 */
td.start { background-color: rgba(200, 255, 200, 0.8); } /* 起点 */
td.end { background-color: rgba(255, 200, 200, 0.8); } /* 终点 */
```

### 玩家棋子颜色
```css
.player1 { background-color: #ff4444; } /* 玩家1 - 红色 */
.player2 { background-color: #4444ff; } /* 玩家2 - 蓝色 */
```
- 颜色+文字描述双重保证，低视力+读屏都清楚

### 响应式
```css
@media (max-width: 700px) {
  #board td {
    width: 30px;
    height: 30px;
    font-size: 0.8em;
  }
}
```
- 手机上也能玩，方便低视力用户放大

---

## 七、音效方案（三选一，开发者选择）

### 方案一：Web Audio 动态生成（默认推荐，单文件）
- 适用：中小型游戏、需要单HTML文件分发
- 优点：无需额外文件，没有路径问题
- 缺点：音效简单，沉浸感一般

**基本框架：**
```javascript
let audioCtx;
function initAudio() {
  // 必须在用户第一次交互后初始化（浏览器政策）
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

function playSound(type) {
  // 根据type生成不同音效
  // - 掷骰子：轻快弹跳音调
  // - 开始游戏：阶梯爬音
  // - 梯子：一阶阶上升
  // - 遇蛇：下沉震动
  // - 胜利：华丽和弦
}
```

### 方案二：独立文件放游戏目录（推荐，好音质）
**目录结构：**
```
你的游戏/
├─ index.html
└─ audio/
   ├─ roll.mp3    掷骰子
   ├─ start.mp3   开始游戏
   ├─ ladder.mp3  爬梯子
   ├─ snake.mp3  遇蛇下滑
   └─ win.mp3     胜利
```

**用法：**
```javascript
function playSound(filename) {
  const audio = new Audio(`audio/${filename}.mp3`);
  audio.play();
}
```
- 找免费商用音效：Freesound、Mixkit、爱给网
- 需要找资源时，可以现场帮找CC0免费商用资源

### 方案三：Base64 内嵌（单文件+好音质）
- 适用：想要单文件又要好音质
- 做法：mp3转base64内嵌到HTML，播放方法同独立文件

### 方案四：腾讯技能市场生成
- 需要语音合成/专业剪辑时，用技能市场处理
- 生成后放入audio目录即可

---

## 八、视觉素材方案（三选一）

### 方案一：Canvas代码绘制（单文件）
- 适用：开发者会简单绘制，不需要很高颜值
- 优点：单文件分发，无需额外资源

### 方案二：开放版权图片放images目录
**目录结构：**
```
你的游戏/
├─ index.html
└─ images/
   ├─ 装饰素材.png
   └─ ...
```

**找素材：**
- Pixabay (https://pixabay.com/) - CC0免费商用
- Unsplash (https://unsplash.com/) - 免费商用
- 需要找可以现场帮找

**无障碍注意：**
- 装饰性图片加上 `aria-hidden="true" role="presentation"`
- 交互元素还是用HTML，图片只做装饰

---

## 九、争渡读屏兼容总结

| 特性 | 兼容性 | 做法 |
|------|--------|------|
| ARIA grid | ✅ 完美支持 | 标准写法 `role="grid/row/gridcell"` |
| 表格导航 | ✅ 完美支持 | `Ctrl+Alt+方向键` 标准操作 |
| accesskey | ✅ 完美支持 | `Alt+字母` 标准触发 |
| aria-live | ✅ 完美支持 | 动态更新播报正常 |
| dialog | ✅ 完美支持 | 标准ARIA dialog写法 |

**结论：** 标准HTML/ARIA写法就是对争渡最好兼容，不需要特殊hack

---

## 十、检查清单（开发完走一遍）

- [ ] 所有可交互元素都能Tab聚焦
- [ ] 每个可聚焦元素有完整的aria-label包含所有信息
- [ ] 状态变化后正确更新所有aria-label
- [ ] 常用操作有accesskey快捷键
- [ ] 有aria-live状态区域播报动态更新
- [ ] 焦点有清晰可见的轮廓
- [ ] 颜色区分清晰，兼顾低视力
- [ ] 模态对话框正确使用ARIA dialog属性
- [ ] 选项选择用按钮直接点击，不需要单选+确认
-  **- 如果需要iOS支持，请单独出一个iOS版本，不用ARIA grid，改用原生table + title属性**

---

## 十一、总结核心

1. **信息完整**：每个可聚焦元素读屏能读出一切需要知道的信息
2. **动态同步**：状态改变，aria-label立刻跟着改变
3. **键盘可达**：所有操作都能走键盘，不需要鼠标
4. **快捷方便**：常用操作有快捷键，减少导航次数
5. **兼顾各方**：全盲体验优先，同时照顾低视力和明眼陪伴
6. **标准写法**：对争渡/NVDA/JAWS都兼容，不需要特殊hack
