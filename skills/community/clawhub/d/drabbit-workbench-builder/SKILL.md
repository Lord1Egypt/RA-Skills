---
name: workbench-builder
author: "@Drabbit777"
license: MIT
source: "https://clawhub.ai/skills/drabbit-workbench-builder"
description: 个人工作台搭建器。通过5-7个简单问题了解用户的职业、工作需求和手机型号，自动生成个性化单页PWA工作台（含任务管理、日程、记账、项目模块等），部署到CloudStudio获得HTTPS网址，手机电脑均可添加桌面。触发词：搭建工作台、做个工作台、帮我建个工作台、个人工作台、workbench、dashboard。
---

# 个人工作台搭建器

> **作者**：@Drabbit777　**许可**：MIT　**首次发布**：2026-08-17
> 本技能包由 @Drabbit777 原创开发，基于实际教师工作台搭建经验沉淀。欢迎自由使用和修改，但发布到技能市场时请保留原作者信息。

## 概述

通过简短的访谈了解用户的工作习惯和管理需求，自动生成一个包含任务管理、日程安排、记账追踪、项目模块等功能的个性化工作台。工作台是单 HTML 文件 + PWA 配置的完整应用，部署到 CloudStudio 后获得 HTTPS 网址，支持：
- 📱 手机/电脑添加到桌面（PWA，独立图标+离线缓存）
- 🔄 多端数据同步（CloudBase 匿名登录）
- 📤 数据导出/导入（JSON）
- 🎨 深色/浅色主题切换
- 🔔 通知系统（红点+浏览器桌面弹窗）

## 前置准备

开始前，先加载 reference 文档了解完整上下文：

1. `references/customization-params.md` — **可定制参数速查手册**（所有占位符和修改位置）
2. `references/bugs-and-fixes.md` — **全部踩坑记录与修复方案**（11个已知Bug）
3. `references/template-structure.md` — **模板解剖图**（6400行代码每个区块的功能说明）

## 工作流概要

```
用户触发 → 询问工作 → 根据回答确定模块 → 定制模板 → 部署CloudStudio → 提供桌面添加指引
```

整个流程中，每完成一个步骤就汇报进展，不要默默操作。

---

## Step 1: 访谈 — 了解用户的工作

通过对话式提问了解用户需求。不要一次性把所有问题抛出来，而是像聊天一样逐个了解。

### 必问问题（5-7个，视回答调整）

**1. 怎么称呼你？你是做什么工作的？**
目标：获取姓名、职业，用于工作台标题和首页问候语。

**2. 你平常一天的工作里，哪些事情需要记录或管理？**
目标：确定需要哪些模块。引导用户说出关键词，然后匹配模块：
- 「待办/任务/今天要做什么/清单」→ 今日待办 + 收集箱
- 「日程/日历/会议/每天固定事项」→ 日历日程
- 「备课/教学/教案/准备材料」→ 备课模块
- 「记账/开销/花费/月支出」→ 记账模块
- 「穿搭/衣柜/衣服/OOTD」→ OOTD 模块
- 「其他项目/专项工作」→ 自定义项目

如果用户只说「全都要」，就默认给 4 个核心模块：待办+日程、记账、备课、OOTD。

**3. 你平常主要用手机还是电脑？**
目标：决定工作台名称和 focus 方向：
- 偏手机 → 推荐 PWA 添加到桌面，名称建议用简短好记的
- 偏电脑 → 名称可以用长一点的描述

**3.5 你用什么牌子的手机？具体型号是？**
目标：确定手机适配方案，避免 PWA 安装失败、布局错位等问题。
- 华为/荣耀 → PWA 安装需手动操作（华为浏览器/Chrome），刘海屏 safe-area 需确认
- iPhone → 必须用 Safari 添加到桌面，iOS 不支持 `beforeinstallprompt`，通知功能受限
- 小米/红米 → 推荐 Chrome，MIUI 浏览器 PWA 支持不完整
- OPPO/vivo/一加 → 推荐 Chrome
- 其他安卓 → 推荐 Chrome
- 如果用户不确定型号，问「你手机浏览器是哪个？」也能推断

**4. 喜欢什么颜色/风格？**
目标：确定主题色。选项：
- 科技蓝（默认）、暖橙色、森林绿、薰衣草紫、玫瑰粉、墨绿
- 或者用户直接说一个颜色，取对应色值

**5. 选一个图标/emoji 作为桌面图标？**
目标：PWA 添加到桌面时的图标。
- 默认：根据职业推荐（教师📚、律师⚖️、设计师🎨、医生🩺…）
- 用户可以自定义（比如「🌸」「🚀」「💼」）
- 同时确定图标背景色（默认用主题色，也可让用户另选）

**6. 有没有一句你喜欢的座右铭或格言？**
目标：显示在首页问候语下方。没有也可以跳过。

---

## Step 2: 根据回答确定模块组合

| 用户提到的需求 | 对应模块 | 数据存储字段 |
|-------------|---------|------------|
| 待办/任务 | 今日待办 + 收集箱 | `tasks[]` + `inbox[]` |
| 日程/日历 | 日历日程 | `calendar[]` |
| 备课/教学 | 备课模块 | `schedule[]`（课表）+ `lessonPlans[]`（教案） |
| 记账/开销 | 记账模块 | `finance[]` |
| 穿搭/衣柜 | OOTD 模块 | `ootdDiary[]` + `wardrobe` |
| 其他项目 | 自定义项目 | `customProjects[]` |

### 不启用模块时的处理

如果用户不需要某个模块：
1. 对应项目卡片不显示
2. 对应 `store` 数据字段仍保留（设为空数组/空对象），以免 JS 报错
3. 页面 Tab 只保留启用的项目

---

## Step 3: 定制模板

### 3.1 复制模板文件到工作目录

```
cp assets/template/index.html → {workspace}/deploy/index.html
cp assets/template/manifest.webmanifest → {workspace}/deploy/manifest.webmanifest
cp assets/template/sw.js → {workspace}/deploy/sw.js
cp assets/template/cloudbase-sdk.js → {workspace}/deploy/cloudbase-sdk.js
```

⚠️ **apple-touch-icon.svg 不要从模板复制**——必须根据用户选择的 emoji + 背景色动态生成（见 3.2.1）。

### 3.2 生成桌面图标（PWA icon）

**不要使用模板中的默认图标**，必须根据用户在第5步的选择动态生成 `apple-touch-icon.svg`。

图标规则：
- 192×192 正方形 SVG
- 圆角 40px
- 背景色 = 用户选择的图标背景色（默认主题色）
- 中央 = 用户选择的 emoji/文字，字号约 100px
- 可选：一圈半透明描边作为装饰环

生成示例（emoji🌸 + 蓝色背景）：
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192" width="192" height="192">
  <rect width="192" height="192" rx="40" fill="#1A56DB"/>
  <rect x="4" y="4" width="184" height="184" rx="38" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
  <text x="96" y="120" text-anchor="middle" font-size="90" dominant-baseline="middle">🌸</text>
</svg>
```

写入路径：`{workspace}/deploy/apple-touch-icon.svg`

### 3.3 修改参数（详见 references/customization-params.md）

**必须修改的参数：**

| 参数 | 位置 | 说明 |
|------|------|------|
| 应用名称 | `index.html` 的 title 标签 + application-name meta 标签 | 工作台名称，如「麻老师工作台」 |
| 短名称 | `manifest.webmanifest` → `"name"` + `"short_name"` | PWA 桌面图标名，≤12字 |
| 用户姓名 | `index.html` → `settings.userName` | 首页问候+「我的」页面 |
| 用户介绍 | `index.html` → `profile-bio` | 「我的」页面的一句话介绍，如「小学数学教师·北京在编」 |
| 用户职业 | `index.html` → `settings.userTitle` | 编辑资料里的默认职业 |
| 座右铭 | `index.html` → `settings.userMotto` | 首页问候语下方 |
| 主题色 | `index.html` → `:root` CSS 变量 + `settings.themeColor` | 整个应用的强调色 |
| 桌面图标 | `deploy/apple-touch-icon.svg`（动态生成） | 用户选的 emoji + 背景色 |
| 启用/停用模块 | 见下方 3.4 |

### 3.4 启用/停用模块

**停用模块需要做三件事：**
1. `init()` 函数中不调用该模块的渲染函数
2. `renderAll()` 中不渲染
3. 项目卡片列表中移除对应卡片

**更简单的方式是用 CSS 隐藏：** 在项目卡片上添加 `style="display:none"`，同时确保该模块的数据存储字段设为空不会导致渲染错误。

### 3.5 修改 manifest 和 service worker

`manifest.webmanifest`：改 `name` 和 `short_name`。
`sw.js`：改 `CACHE_NAME` 中的名称（从 `teacher-m-v?` 改成自定义名称，保持 `-v1` 起始）。

### 3.6 手机品牌适配（根据 Step 1 的 Q3.5）

不同手机品牌的浏览器对 PWA 的支持程度不同，需要根据用户手机型号做针对性适配：

**华为/荣耀（HarmonyOS / EMUI）：**
1. `manifest.webmanifest` 的 `display` 保持 `"standalone"`（华为浏览器支持）
2. 确认 `apple-touch-icon.svg` 已正确生成（华为浏览器读取 apple-touch-icon）
3. `theme-color` meta 标签需同时适配深色/浅色（华为状态栏会跟随）
4. safe-area 已有 `env(safe-area-inset-*)` 处理刘海，但需确认华为刘海宽度是否正常（Mate 系列居中刘海、P 系列开孔屏）
5. 部署后引导用户用**华为浏览器**或 **Chrome** 打开，不用百度/UC

**iPhone（iOS 14+）：**
1. `apple-mobile-web-app-status-bar-style` 已设为 `"black-translucent"`，适配刘海屏
2. iOS 不触发 `beforeinstallprompt` 事件，PWA 安装横幅代码会自动跳过（模板已处理）
3. iOS 16.4 以下不支持 PWA 桌面通知 → 通知系统的浏览器弹窗会静默失败，但红点提示仍正常
4. 确保 `viewport-fit=cover` 存在（模板已有），否则 iPhone 刘海会遮挡内容

**小米/OPPO/vivo/一加（MIUI / ColorOS / FuntouchOS）：**
1. PWA 安装提示可能不自动弹出 → 引导用户通过浏览器菜单手动添加
2. 确认 `theme-color` 已设置（影响浏览器地址栏颜色）
3. safe-area 处理同标准 Android，无需额外适配

**通用检查（所有品牌）：**
1. 模板已内置 `beforeinstallprompt` 监听 + `display-mode: standalone` 检测，会根据浏览器能力自动降级
2. `navigator.userAgent` 检测设备类型用于同步显示设备名，无需额外修改
3. 如果用户手机浏览器不支持 PWA，工作台仍可作为普通网页使用，只是没有离线缓存和桌面图标

---

## Step 4: 部署到 CloudStudio

将 `{workspace}/deploy/` 目录部署到 CloudStudio：

```
workbuddy_cloudstudio_deploy --directory {workspace}/deploy --port 3000
```

部署成功后获得 HTTPS 公开网址，记录下来。

⚠️ **重要**：CloudStudio 从同一目录重新部署会复用沙箱（URL 不变），所以后续修改只需要重新部署即可，用户数据不会丢失。

---

## Step 5: 引导用户添加到桌面

### 华为/荣耀手机（HarmonyOS / EMUI）
1. 用**华为自带浏览器**或 **Chrome** 打开 HTTPS 网址
2. 等待页面加载完成
3. 如果弹出安装横幅 → 直接点「添加到主屏幕」
4. 如果没弹出 → 点浏览器菜单（⋮ 或底部更多）→「添加到桌面」或「添加书签到主屏幕」
5. ⚠️ **不要用百度浏览器**——百度不支持 PWA
6. ⚠️ **HarmonyOS NEXT（纯血鸿蒙）** → 必须用系统自带的华为浏览器，Chrome 不可用

### iPhone/iPad（iOS）
1. 用 **Safari** 打开 HTTPS 网址（Chrome/百度等浏览器无法添加 PWA 到桌面）
2. 点底部中间「分享」按钮（方框+向上箭头）
3. 滑动找到「添加到主屏幕」
4. 确认名称后点「添加」
5. ⚠️ iOS 桌面通知受限（需 iOS 16.4+ 且从主屏幕启动的 PWA），但应用内红点提醒正常

### 小米/OPPO/vivo/一加手机
1. 用 **Chrome** 打开 HTTPS 网址（系统浏览器 PWA 支持可能不完整）
2. 等待加载完成 → 如果弹出安装横幅直接安装
3. 如果没弹出 → 菜单（⋮）→「添加到主屏幕」或「安装应用」

### 电脑（macOS Chrome/Edge）
1. 打开 HTTPS 网址
2. 浏览器地址栏右侧会出现一个「安装」图标（⊕ 或在菜单中）
3. 点击安装后，工作台会作为一个独立窗口出现在 Dock 中

---

## Step 6: 多端同步设置（可选）

如果用户希望手机和电脑数据同步：

1. 用户去 [CloudBase 控制台](https://console.cloud.tencent.com/tcb) 创建环境（免费额度够用）
2. 开启「匿名登录」
3. 创建 `sync_data` 数据库集合
4. 在工作台「我的」→ 多端同步中填入环境 ID
5. 输入配对码完成配对

详细步骤见 `references/bugs-and-fixes.md` 第 10 条。

---

## ⚠️ 常见问题速查

部署、PWA、同步相关的常见问题已全部记录在 `references/bugs-and-fixes.md`，遇到问题时优先查阅：

| 序号 | 问题 | 关键词 |
|------|------|--------|
| 1 | 修改不生效（白色页面闪现） | SW 缓存、CACHE_NAME 版本号 |
| 2 | 应用名称改不了 | manifest+SW+meta 三处同步 |
| 3 | Service Worker 更新后还是旧版 | 完全退出 PWA 再打开 |
| 4 | 百度浏览器无法添加桌面 | 换华为自带浏览器/Chrome |
| 5 | 数据丢失 | localStorage → CloudStudio URL 不变 |
| 6 | 多端同步连接失败 | CloudBase SDK、匿名登录 |
| 7 | CloudBase SDK 404 | 改用项目内打包的 cloudbase-sdk.js |
| 8 | 照片上传只能拍照 | 去掉 capture="environment" |
| 9 | 清空数据后同步状态残留 | clearAllData 清除同步配置 |
| 10 | 点击通知/主题/课表提示 Phase 2 | HTML onclick 没改，需更新 |
| 11 | CloudBase 集合不存在 | sync_data 需手动创建 |

---

## 对话风格

- **友好自然**：像帮朋友搭建一样聊天，不要板着脸列菜单
- **逐个提问**：不要一次丢出所有问题，根据回答自然追问
- **适当建议**：用户不知道选什么时，根据职业给出推荐配置
- **及时汇报**：每完成一个步骤（定制、部署）就告诉用户进展
- **部署后给指引**：部署完不等用户问，主动给出添加到桌面的操作步骤
