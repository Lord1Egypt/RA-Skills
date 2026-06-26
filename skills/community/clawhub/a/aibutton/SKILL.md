---
name: AIButton
description: 创建 Vision Node AI 按钮控件。根据客户描述生成AI控件的 aiui.json 和 index.html，并打包成 ZIP 压缩包。
---

# Vision Node AI 按钮控件生成器

## 文档来源

**fixed 规则文档**：`/Users/lippsli/Desktop/AI控件文档/AI 按钮制作文字描述模板V2.docx`

---

## AI控件结构

每个 VN AI 按钮控件包含两个核心文件：

### 1. aiui.json - 控件元数据

```json
{
  "info": {
    "name": "控件名_随机ID",
    "url": "https://www.minimaxi.com/",
    "version": "MiniMax-M2.7",
    "generator": "MiniMax",
    "time": "2026-03-26"
  },
  "description": {
    "type": "button",
    "remark": "",
    "editable": "中文描述（根据客户要求）",
    "fixed": "外观样式：例如制作一个3D效果的工业控制按钮，非激活文本是启动，激活文本是停止，非激活按钮背景是绿色，激活按钮背景是红色。尺寸要求：html和body的宽高与按钮控件的实际宽高一致（不是固定200x200），html和body的大小必须与按钮div大小一致或略大一点（不超过10px差距），禁止html/body远大于按钮导致出现大面积空白。滚动控制：无论浏览器如何放大或缩小，都不能出现滚动条，使用overflow: hidden来禁止滚动。定位要求：控件必须显示在页面的左上角，控件样式需要完整显示，不能被裁剪。布局要求：移除html和body的默认margin和padding，使用Flexbox布局确保内容从左上角开始排列，控件容器占满整个html/body空间，html和body为背景透明色，不要使用外部连接样式。控件居中显示：如果控件容器的尺寸小于html和body的尺寸，控件必须在容器中居中显示，使用Flexbox的justify-content: center实现水平居中，使用Flexbox的align-items: center实现垂直居中。边界控制：所有视觉变化均不得溢出视口，变换效果后的控件边界需在视口内，尺寸变化后的整体尺寸不得超出视口，视觉效果投影范围需在视口内，动态变化任何中间状态及最终状态均不得溢出。JS部分：1.变量初始化：cameraBtn获取页面中的按钮元素，ID初始化为null（数字类型），MPV初始化为空对象。2.空函数定义：fun空函数用于事件绑定占位。3.触摸事件绑定：为document.body添加touchstart/touchmove事件监听器，设置passive: false防止默认行为。4.父窗口消息监听：Digital类型接收ID（event.data.type等于'Digital'时，event.data.num转数字赋值给ID），Data类型接收MPV（event.data.type等于'Data'时，event.data.value赋值给MPV）。5.根据MPV更新按钮状态：遍历MPV.Input，判断SignalName第二个字符是否为'd'且数字ID匹配，如果满足则根据SignalValue设置按钮active状态。6.按下事件处理：调用e.preventDefault()阻止默认行为，添加active类，发送{id:'JND_'+ID, value:true}到父窗口。7.抬起事件处理：检查data-info属性值，data-info为false时移除active类，data-info为true时根据MPV数据决定状态，发送{id:'JND_'+ID, value:false}到父窗口。8.事件监听器绑定：mousedown/touchstart绑定按下处理，mouseup/touchend绑定抬起处理，dragstart阻止拖拽。9.通信协议：接收Digital类型获取ID，接收Data类型获取MPV，发送{id:'JND_'+ID, value:true/false}。10.按钮状态管理：手动控制模式（data-info为false）和数据驱动模式（data-info为true）。"
  }
}
```

**info 字段说明**：
| 字段 | 说明 | 当前值 |
|------|------|--------|
| url | AI大模型的对话地址 | https://www.minimaxi.com/ |
| version | 大模型版本 | MiniMax-M2.7 |
| generator | 大模型名字 | MiniMax |
| time | 创建时间 | 自动使用当前日期 |

**⚠️ 重要**：
1. 如果使用其他大模型（如 GPT、Kimi 等），需将 url、version、generator 更新为实际使用的模型信息。
2. **aiui.json 必须是纯 JSON 格式**，不能用 `JSON.stringify()`，不能把对象写成字符串。
3. **生成后必须压缩为单行格式**，使用 `json.dump(data, f, ensure_ascii=False, separators=(',', ':'))`，避免任何换行符导致解析问题。
4. **html/body 大小必须与按钮 div 大小一致或略大一点**，禁止 html/body 远大于按钮导致大面积空白（差距不超过 10px）。按钮的 html/body 尺寸应该根据实际按钮宽高设置，不是固定 200x200px。

**❌ 错误示例**（把 JSON 写成字符串，或有多余换行）：
```json
{"info":"{\"name\":\"按钮\"}","description":"{\"type\":\"button\"}"}  <!-- 错误：嵌套字符串 -->
```

**✅ 正确示例**（纯 JSON 对象，单行格式）：
```json
{"info":{"name":"按钮","url":"..."},"description":{"type":"button","editable":"..."}}
```

> ⚠️ 生成后必须用 `json.dump(..., separators=(',', ':'))` 压缩为单行，不能有换行符！

**description 字段说明**：
| 字段 | 说明 |
|------|------|
| editable | 用户描述部分（客户的中文需求） |
| fixed | 固定规则部分（**来自文档的完整技术规范，用中文**） |

### 2. index.html - 控件实现

包含 HTML 结构、CSS 样式和 JavaScript 逻辑的完整页面。

---

## aiui.json fixed 规则内容（完整中文文档）

**⚠️ 重要**：fixed 规则必须使用以下**完整版本**，不要简化！

```
去掉body的背景色；采用flex布局；设置html、body的宽高与按钮控件的实际宽高一致（不是固定200x200），html和body的大小必须与按钮div大小一致或略大一点（不超过10px差距），禁止html/body远大于按钮导致出现大面积空白。设置自定义属性data-info为false;通过class值切换激活和非激活样式；用iframe引用并且可以与父级窗口通讯；父级数据优先于事件；如果是通过父级数据改变的按钮状态则不用再将数据反馈到父级页面；如果收到父级数据event.data.type等于Digital，event.data.num储存到ID中；定义MPV={"Input":{}};如果收到父级数据event.data.type等于Data 那么MPV= event.data.value；用for (var posx in MPV.Input) 遍历json获取MPV.Input[posx].SignalName值和MPV.Input[posx].SignalValue的值， 截取MPV.Input[posx].SignalName中的数字并转成数字类型存到变量num中，并判断SignalName值的第二个字符是不是等于d如果等于d，并且num等于ID则通过获取SignalValue的值设置按钮的激活和非激活,并设置自定义属性data-info为true；鼠标按下时激活，如果data-info为false时鼠标抬起后非激活；如果data-info为true并且MPV中Input值不为"{}"时，ID设置成num变量,鼠标抬起时解析MPV数据:如果MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]]存在并且MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"] ].SignalValue值为false时设置按钮为非激活样式；如果MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]]值为true时设置按钮为激活样式；如果data-info为true并且MPV中Input值为"{}"时鼠标抬起后设置按钮为非激活样式。鼠标按下发送激活数据true到父级{id:"JND_"+ID,value:true},鼠标抬起发送非激活数据false到父级发送数据{id:"JND_"+ID,value:false},向父级发送数据时不用判断任何条件。阻止默认事件；禁止所有元素选中文本；
```

---

## 生成步骤

1. **分析需求**：
   - 如果用户**给出了描述** → 按照用户描述生成
   - 如果用户**没有给出描述** → 使用**不同的默认描述**生成**不同风格**的按钮（每次风格要有变化）
2. **生成 aiui.json**：
   - name: `控件名_时间戳MD5`
   - url/version/generator: 使用上面表格中的值
   - time: 自动使用当前日期
   - editable: 客户的中文描述（或自动生成的默认描述）
   - fixed: 上面完整的技术规范
   - ⚠️ **命名规则**：ZIP压缩包和控件名必须使用**功能名**（如：主场按钮、辅灯按钮、启动按钮、停止按钮），禁止使用通用名称如"按钮A"、"按钮B"。如果一次生成多个控件，下划线前的名字**必须不同**，禁止使用相同的名字前缀！
3. **压缩 aiui.json 为单行格式**（⚠️ 必须！）：
   ```python
   import json
   with open("aiui.json", "w") as f:
       json.dump(aiui_data, f, ensure_ascii=False, separators=(",", ":"))
   ```
4. **验证 JSON 格式**：
   ```bash
   python3 -m json.tool aiui.json > /dev/null && echo "JSON格式正确" || echo "JSON格式错误"
   ```
5. **生成 index.html**：实现完整的按钮交互逻辑
3. **压缩 aiui.json 为单行格式**（⚠️ 必须！）：
   ```python
   import json
   with open("aiui.json", "w") as f:
       json.dump(aiui_data, f, ensure_ascii=False, separators=(",", ":"))
   ```
4. **验证 JSON 格式**：
   ```bash
   python3 -m json.tool aiui.json > /dev/null && echo "JSON格式正确" || echo "JSON格式错误"
   ```
5. **生成 index.html**：实现完整的按钮交互逻辑

**⚠️ index.html 代码结构（必须严格按照此结构）**：

```javascript
// 变量初始化
var ID = 0;
var MPV = { Input: {}, SignalNameVSPos: {} };
const button = document.querySelector('.button');

// 父窗口消息监听
window.addEventListener('message', function(event) {
    if (event.data.type === 'Digital') {
        ID = event.data.num;
    } else if (event.data.type === 'Data') {
        MPV = event.data.value;
        processMPVData();
    }
});

// 激活按钮
function activateButton() {
    button.classList.add('active');
    button.textContent = '停止';
    button.setAttribute('data-info', 'true');
}

// 停用按钮
function deactivateButton() {
    button.classList.remove('active');
    button.textContent = '启动';
    button.setAttribute('data-info', 'false');
}

// 发送到父窗口
function sendToParent(value) {
    window.parent.postMessage({ id: "JND_" + ID, value: value }, '*');
}

// 处理MPV数据
function processMPVData() {
    if (MPV.Input) {
        for (var posx in MPV.Input) {
            var signalName = MPV.Input[posx].SignalName;
            var signalValue = MPV.Input[posx].SignalValue;
            var num = parseInt(signalName.match(/\d+/)[0]);
            if (signalName[1] === 'd' && num === ID) {
                if (signalValue) {
                    activateButton();
                } else {
                    deactivateButton();
                }
                button.setAttribute('data-info', 'true');
            }
        }
    }
}

// 按下事件
button.addEventListener('mousedown', function(e) {
    e.preventDefault();
    activateButton();
    sendToParent(true);
});

// 抬起事件（必须处理三种情况）
button.addEventListener('mouseup', function(e) {
    e.preventDefault();
    if (button.getAttribute('data-info') === 'false') {
        deactivateButton();
    } else if (button.getAttribute('data-info') === 'true' && Object.keys(MPV.Input).length !== 0) {
        var num = ID;
        if (MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]] &&
            MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]].SignalValue === false) {
            deactivateButton();
        } else if (MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]] &&
            MPV.Input[MPV.SignalNameVSPos.Input["[d_fb" + num + "]"]].SignalValue === true) {
            activateButton();
        }
    } else if (button.getAttribute('data-info') === 'true' && Object.keys(MPV.Input).length === 0) {
        deactivateButton();
    }
    sendToParent(false);
});

// 触摸事件（同样处理）
button.addEventListener('touchstart', function(e) {
    e.preventDefault();
    activateButton();
    sendToParent(true);
}, { passive: false });

button.addEventListener('touchend', function(e) {
    e.preventDefault();
    // 同 mouseup 逻辑
    ...
}, { passive: false });
```

5. **打包为 ZIP**：导出给 VN 系统使用

## ZIP 打包

### 命名规则

**文件名格式**：`功能名_16位MD5.zip`

控件名必须使用**功能名**（如：主场按钮、辅灯按钮），禁止使用通用名称。每次生成时，需要生成一个新的 16 位 MD5 值作为唯一标识。

### ZIP 结构（重要）

ZIP 压缩包内**必须包含一个同名文件夹**，文件夹内包含 `aiui.json` 和 `index.html`：

```
控件名_16位MD5.zip
└── 控件名_16位MD5/
    ├── aiui.json
    └── index.html
```

### JS 代码规范

**⚠️ 核心规则**：

| 文件 | 是否压缩 |
|------|----------|
| `aiui.json` | ✅ **必须压缩**为单行，用 `json.dump(..., separators=(",", ":"))` |
| `index.html` | ❌ **禁止压缩**，HTML/CSS/JS 全部保持格式化 |

**❌ index.html 中 JS 错误写法**（禁止）：
```javascript
var ID=0,MPV={Input:{}},btn=document.querySelector('.btn');
function activate(){btn.classList.add('active');btnText.textContent='停止';}
btn.addEventListener('mousedown',function(e){e.preventDefault();activate();sendToP(true)});
```

**✅ index.html 中 JS 正确写法**（必须）：
```javascript
var ID = 0;
var MPV = { Input: {}, SignalNameVSPos: {} };
var btn = document.querySelector('.btn');

function activate() {
    btn.classList.add('active');
    btnText.textContent = '停止';
    btn.setAttribute('data-info', 'true');
}

function deactivate() {
    btn.classList.remove('active');
    btnText.textContent = '启动';
    btn.setAttribute('data-info', 'false');
}

function sendToParent(value) {
    window.parent.postMessage({ id: "JND_" + ID, value: value }, '*');
}

btn.addEventListener('mousedown', function(e) {
    e.preventDefault();
    activate();
    sendToParent(true);
});
```

**格式化要求**：
- 每条语句**单独成行**
- 函数**单独成行**
- 逻辑块之间**空行分隔**
- 缩进统一 **4 空格**
- 禁止把多行代码压缩成一行

### 打包命令

**⚠️ 重要**：aiui.json 必须在打包前压缩为单行格式！

```python
# Python 压缩 aiui.json 为单行（使用 json.dump，不使用 json.dumps）
import json

aiui = {
    "info": {...},
    "description": {...}
}

with open("aiui.json", "w", encoding="utf-8") as f:
    json.dump(aiui, f, ensure_ascii=False, separators=(",", ":"))
# 结果：{"info":{...},"description":{...}}
```

```bash
# 生成唯一ID
TIMESTAMP=$(date +%s)
MD5=$(echo -n "$TIMESTAMP" | md5 -r | cut -c1-16)

# 创建临时目录和子文件夹
rm -rf /tmp/button_${MD5}
mkdir -p /tmp/button_${MD5}/控件名_${MD5}

# 复制文件到子文件夹
cp aiui.json /tmp/button_${MD5}/控件名_${MD5}/
cp index.html /tmp/button_${MD5}/控件名_${MD5}/

# 验证 aiui.json 是有效 JSON 格式
python3 -m json.tool /tmp/button_${MD5}/控件名_${MD5}/aiui.json > /dev/null && echo "✓ aiui.json 格式正确" || { echo "✗ aiui.json 格式错误"; rm -rf /tmp/button_${MD5}; exit 1; }

# 打包（包含子文件夹）
cd /tmp/button_${MD5} && zip -r ~/Desktop/VNAIButton/控件名_${MD5}.zip 控件名_${MD5}/

# 清理临时目录
rm -rf /tmp/button_${MD5}
echo "✓ 完成: ~/Desktop/VNAIButton/控件名_${MD5}.zip"
```

### 输出位置

`~/Desktop/VNAIButton/`

**不保留文件夹**，直接输出压缩包。

---

## 缩放问题修复（重要）

**问题**：按钮在 VN 系统中缩放时出现：
1. 文字变成2行
2. border 边框变粗

**解决方案**（必须在 CSS 中添加）：

```css
.button {
    /* 1. 防止边框影响尺寸 */
    box-sizing: border-box;
    
    /* 2. 防止文字换行 */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
```

**关键点**：
- `box-sizing: border-box` 让 border/padding 包含在 width/height 内，不会在缩放时撑大元素
- `white-space: nowrap` 强制文字不换行
- `overflow: hidden` 隐藏溢出内容

---

## 调试经验总结

### 1. 输出文件名规则（重要）

**每次修正后要生成新的压缩包，不要覆盖之前的文件！**

**规则**：
- 文件名格式：`名字_16位MD5.zip`
- 每次生成使用新的名字前缀（让用户容易区分）
- 每次生成使用新的 MD5 值

**错误做法**：
- ❌ 直接覆盖同名文件
- ❌ 只改 MD5 但名字不变

**正确做法**：
- ✅ 每次都生成新的名字前缀 + 新的 MD5
- ✅ 修正后给用户新的压缩包

**示例**：
| 版本 | 文件名 |
|------|--------|
| 初版 | `启动按钮_2f14bc70dcd0029d.zip` |
| 修正1 | `停止按钮_78c12d470c45b7c2.zip` |
| 修正2 | `工业按钮_cad71d5cc5d69169.zip` |

### 2. index.html 代码结构示例（完整版）

**⚠️ index.html 代码结构（必须严格按照此结构）**：

```javascript
// ========== 变量初始化 ==========
var ID = 0;
var MPV = { Input: {}, SignalNameVSPos: {} };
var btn = document.getElementById("btn");

// ========== 父窗口消息监听 ==========
window.addEventListener('message', function(event) {
    if (event.data && event.data.type) {
        if (event.data.type === 'Digital') {
            ID = parseInt(event.data.num);
        } else if (event.data.type === 'Data') {
            MPV = event.data.value;
            updateFromMPV();
        }
    }
});

// ========== 从MPV更新按钮状态 ==========
function updateFromMPV() {
    if (MPV && MPV.Input) {
        for (var posx in MPV.Input) {
            var signalName = MPV.Input[posx].SignalName;
            var signalValue = MPV.Input[posx].SignalValue;
            var num = parseInt(signalName.match(/\d+/)[0]);
            if (signalName.charAt(1) === 'd' && num === ID) {
                if (signalValue) {
                    activateButton();
                } else {
                    deactivateButton();
                }
                btn.setAttribute('data-info', 'true');
            }
        }
    }
}

// ========== 按钮状态控制 ==========
function activateButton() {
    btn.classList.add('active');
    btn.textContent = '停止';
    btn.setAttribute('data-info', 'true');
}

function deactivateButton() {
    btn.classList.remove('active');
    btn.textContent = '启动';
    btn.setAttribute('data-info', 'false');
}

// ========== 发送到父窗口 ==========
function sendToParent(value) {
    window.parent.postMessage({ id: "JND_" + ID, value: value }, '*');
}

// ========== 按下事件 ==========
function onPress(e) {
    e.preventDefault();
    activateButton();
    sendToParent(true);
}

// ========== 抬起事件 ==========
function onRelease(e) {
    e.preventDefault();
    var info = btn.getAttribute('data-info');
    if (info === 'false') {
        deactivateButton();
    } else if (info === 'true' && Object.keys(MPV.Input).length !== 0) {
        var num = ID;
        var fbKey = "[d_fb" + num + "]";
        var signalName = MPV.SignalNameVSPos && MPV.SignalNameVSPos.Input && MPV.SignalNameVSPos.Input[fbKey];
        if (signalName && MPV.Input[signalName] && MPV.Input[signalName].SignalValue === false) {
            deactivateButton();
        } else if (signalName && MPV.Input[signalName] && MPV.Input[signalName].SignalValue === true) {
            activateButton();
        }
    } else if (info === 'true' && Object.keys(MPV.Input).length === 0) {
        deactivateButton();
    }
    sendToParent(false);
}

// ========== 事件绑定 ==========
btn.addEventListener('mousedown', onPress);
btn.addEventListener('touchstart', onPress, { passive: false });
document.addEventListener('mouseup', onRelease);
document.addEventListener('touchend', onRelease);
btn.addEventListener('dragstart', function(e) { e.preventDefault(); });
```
