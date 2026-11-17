# 工作台定制参数速查手册

本文档列出生成个性化工作台时，所有需要从用户那里收集的参数，以及对应的模板修改位置。

---

## 一、必填参数（通过访谈获取）

### 1.1 身份信息

| 参数 | 变量名 | 用途 | 默认值 | 修改位置 |
|------|--------|------|--------|----------|
| 用户名 | `userName` | 首页问候、个人资料 | "麻老师" | `getEmptyData().settings.userName` |
| 职业/身份 | `occupation` | 个人资料展示 | "教师" | `getEmptyData().settings.occupation` |
| 一句话介绍 | `bio` | 个人资料副标题 | "小学教师 · 北京在编" | `getEmptyData().settings.bio` |
| 座右铭 | `userMotto` | 首页状态文字 | "今天不需要完成所有事..." | `getEmptyData().settings.userMotto` |
| 昵称 | — | 首页问候语模板 | 同 userName | `updateHomeGreeting()` 函数内 |

### 1.2 项目定义（核心）

每个项目包含以下字段：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | string | 唯一标识 | `"proj_teaching"` |
| `name` | string | 项目名称（≤6字） | `"麻老师上班啦"` |
| `icon` | string | emoji 图标 | `"📚"` |
| `colorClass` | string | CSS 颜色类名 | `"teaching"` |
| `coverImage` | string | 封面图（初始为空） | `""` |
| `subModules` | string[] | 子模块列名 | `["待办","进行中","已完成"]` |

**颜色匹配表：**

| colorClass | 深色值 | 浅色背景 | 适用 vibe |
|------------|--------|----------|-----------|
| `teaching` | `#5EE7DF` | `rgba(94,231,223,0.12)` | 教育、学习、知识 |
| `exam` | `#FFD166` | `rgba(255,209,102,0.12)` | 考试、目标、冲刺 |
| `learning` | `#7FE092` | `rgba(127,224,146,0.12)` | 成长、进步、积累 |
| `finance` | `#F871A0` | `rgba(248,113,160,0.12)` | 理财、记账、预算 |
| `side` | `#C084FC` | `rgba(192,132,252,0.12)` | 副业、兴趣、创作 |
| `ootd` | `#FF9B71` | `rgba(255,155,113,0.12)` | 穿搭、形象、风格 |
| `health` | `#60A5FA` | `rgba(96,165,250,0.12)` | 健身、健康、运动 |
| `home` | `#FBBF24` | `rgba(251,191,36,0.12)` | 家庭、生活、育儿 |

### 1.3 风格偏好

| 参数 | 选项 | 影响范围 |
|------|------|----------|
| 默认主题 | `dark` / `light` | CSS 默认变量、`getEmptyData().settings.theme` |
| 整体风格 | 科技感 / 温暖手账 / 简洁商务 | 背景渐变、卡片透明度、圆角大小 |
| 色彩偏好 | 冷色调 / 暖色调 | CSS 主色调选择 |

### 1.4 功能开关

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 是否需要课表 | `false`（非教师默认关闭） | 如果用户是教师，添加课表模块 |
| 是否需要记账 | `true` | 绝大多数用户需要 |
| 是否需要 OOTD/穿搭 | `false` | 时尚类用户需要 |
| 是否需要多端同步 | `true` | 建议默认开启，提供 CloudBase 配置说明 |
| 是否需要 AI 简报 | `true` | 已有内置规则引擎 |
| 通知默认开启 | `true` | 任务截止 + 日程提醒 |

### 1.5 手机品牌适配

| 参数 | 选项 | 影响 |
|------|------|------|
| 手机品牌 | 华为/荣耀、iPhone、小米/红米、OPPO/vivo/一加、其他 | PWA 安装指引、浏览器推荐、safe-area 确认 |
| 手机型号 | 用户自述 | 刘海屏宽度、状态栏高度确认 |
| 主用浏览器 | 华为浏览器/Chrome/Safari/MIUI浏览器/其他 | 决定是否需要引导换浏览器 |

**品牌适配速查表：**

| 品牌 | 推荐浏览器 | PWA 安装方式 | 需要额外适配 |
|------|-----------|-------------|-------------|
| 华为/荣耀 | 华为浏览器 / Chrome | 菜单→添加到桌面 | safe-area 确认刘海 |
| iPhone | **Safari**（必须） | 分享→添加到主屏幕 | iOS 通知受限，无 beforeinstallprompt |
| 小米/红米 | **Chrome** | 菜单→添加到主屏幕 | MIUI 浏览器可能不支持 PWA |
| OPPO/vivo | **Chrome** | 菜单→添加到主屏幕 | 系统浏览器 PWA 支持不完整 |
| 一加 | Chrome / OnePlus Browser | 菜单→添加到主屏幕 | 基本同标准 Android |

**模板内置的适配机制（无需手动改）：**
- `viewport-fit=cover` + `env(safe-area-inset-*)` → 处理刘海屏
- `beforeinstallprompt` 事件监听 → Android 自动弹安装横幅（iOS 不触发，自动跳过）
- `display-mode: standalone` 检测 → 判断是否已从桌面打开
- `navigator.userAgent` 检测 → 同步设备名显示
- `apple-mobile-web-app-status-bar-style: black-translucent` → iOS 状态栏透明

**需要手动适配的场景（极少）：**
- 华为 Mate 系列宽刘海 → 如有遮挡，增加 `--safe-top` 的 fallback 值
- HarmonyOS NEXT → 确保不依赖 Chrome，华为浏览器是唯一选择
- iOS 低版本（<16.4） → 通知功能静默降级，红点仍正常

---

## 二、模板替换映射

### 2.1 CSS 背景渐变生成规则

**科技感（默认）：**
```css
--bg-page-gradient: radial-gradient(ellipse at 50% -10%, rgba({PRIMARY_R}, {PRIMARY_G}, {PRIMARY_B}, 0.10) 0%, transparent 45%),
                    radial-gradient(ellipse at 100% 100%, rgba({SECONDARY_R}, {SECONDARY_G}, {SECONDARY_B}, 0.08) 0%, transparent 35%),
                    linear-gradient(180deg, {BG_COLOR} 0%, {BG_DARKER} 100%);
```

**温暖手账：**
```css
--bg-page-gradient: radial-gradient(ellipse at 50% -10%, rgba(255, 190, 140, 0.15) 0%, transparent 45%),
                    radial-gradient(ellipse at 100% 100%, rgba(255, 160, 180, 0.10) 0%, transparent 35%),
                    linear-gradient(180deg, #1A1410 0%, #0F0C08 100%);
```

**简洁商务：**
```css
--bg-page-gradient: linear-gradient(180deg, #1A1D23 0%, #101216 100%);
```

### 2.2 首页问候语模板

```javascript
// 在 updateHomeGreeting() 中：
const hour = new Date().getHours();
let timeWord;
if (hour < 7) timeWord = '凌晨好呀';
else if (hour < 12) timeWord = '早上好呀';
else if (hour < 14) timeWord = '中午好呀';
else if (hour < 18) timeWord = '下午好呀';
else timeWord = '晚上好呀';
el.textContent = `${timeWord}，${store.settings.userName}。`;
```

### 2.3 工作台名称生成规则

```
manifest.webmanifest:
  "name": "{用户名}的工作台"  或  "{用户名} Console"
  "short_name": "{首字}"    或  "{用户名首字}"

index.html:
  <title> → 同 manifest name
  <meta name="apple-mobile-web-app-title"> → 同 short_name
```

### 2.4 项目卡片动态生成

模板中的 `renderProjects()` 函数需要根据项目数量动态生成 HTML。关键逻辑：

```javascript
function renderProjects() {
  const grid = document.getElementById('projectsGrid');
  grid.innerHTML = store.projects.map((proj, i) => `
    <div class="project-card" onclick="openProject('${proj.id}')" 
         style="--card-color: var(--color-${proj.colorClass}); --card-bg: var(--color-${proj.colorClass}-bg);">
      <div class="project-card-icon">${proj.icon}</div>
      <div class="project-card-name">${proj.name}</div>
      <div class="project-card-count">${countTasks(proj.id)} 个任务</div>
    </div>
  `).join('');
}
```

### 2.5 Tab 栏自适应

如果项目数 > 6，需要考虑 tab 栏布局。当前模板固定 5 个 tab：
1. 今日待办
2. 项目（固定）
3. 日程（固定）
4. 收集箱（固定）
5. 我的（固定）

项目本身在「项目」tab 下的网格中展示，不单独占 tab。

---

## 三、输出文件清单

生成工作台后，以下文件必须全部输出：

| 文件 | 必须 | 说明 |
|------|------|------|
| `index.html` | ✅ | 主应用文件 |
| `manifest.webmanifest` | ✅ | PWA 清单 |
| `sw.js` | ✅ | Service Worker |
| `apple-touch-icon.svg` | ✅ | 应用图标 |
| `cloudbase-sdk.js` | ⚠️ | 仅当启用云同步时需要 |
| `README.md` | 推荐 | 部署说明 + CloudBase 配置指南 |

---

## 四、部署说明模板

生成工作台后，向用户提供以下部署说明：

```
## 🚀 部署你的工作台

### 方式一：一键部署到 CloudStudio（推荐）
[自动化部署链接]

### 方式二：手动部署
1. 将所有文件上传到支持 HTTPS 的静态文件服务器
2. 确保 index.html 为入口文件
3. 如需多端同步：
   a. 在腾讯云 CloudBase 控制台创建环境
   b. 开启「匿名登录」
   c. 创建数据库集合 `sync_data`
   d. 在工作台中填入环境 ID

### 添加到手机桌面
1. 用 Chrome/Safari/Edge 打开工作台网址
2. 点击浏览器菜单 → 「添加到主屏幕」
3. 以后就可以像 App 一样打开！

### 注意
- 百度浏览器、UC 浏览器不支持添加到桌面，推荐 Chrome
- 更新版本后需要完全退出再打开才能看到新功能
```
