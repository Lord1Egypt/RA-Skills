# 工作台搭建 — 全部踩坑记录与修复方案

本文档记录从零搭建 Teacher M console 过程中遇到的所有 bug、冲突、性能问题和修复方案。生成任何新工作台时，务必逐条检查以下问题。

---

## 一、PWA 相关坑

### 1.1 华为手机浏览器不支持 PWA
- **现象**：用户用百度浏览器打开，找不到「添加到主屏幕」选项
- **根因**：百度浏览器（和部分国产浏览器）不支持 PWA 的 `beforeinstallprompt` 事件
- **修复**：
  - 建议用户使用华为自带浏览器或 Chrome
  - 添加 `beforeinstallprompt` 监听 + 顶部横幅提示（`installBanner`），在支持的浏览器上主动引导
  - 横幅 7 天内不再显示（`localStorage.setItem('tm_install_banner_dismissed', ...)`）
- **预防**：生成工作台后，明确告知用户推荐使用 Chrome/Edge/Safari 添加到桌面

### 1.2 Service Worker 缓存不更新
- **现象**：修改 index.html 后部署，手机端仍然是旧版本
- **根因**：SW 缓存策略为 cache-first，旧版 HTML 被缓存在 Service Worker 中
- **修复**：
  - 每次部署前手动递增 SW 版本号（`CACHE_NAME = 'workbench-v{N}'`）
  - SW 的 `activate` 事件中清理旧缓存：`caches.keys().filter(k => k !== CACHE_NAME).map(k => caches.delete(k))`
  - 告知用户：完全退出 PWA 再重新打开才能加载新版本（不是刷新，是退出重开）
- **预防**：
  - 每次修改模板后，递增 CACHE_NAME 版本号
  - 在 SKILL.md 工作流中明确标注：部署前必须改 SW 版本号

### 1.3 manifest 配置不当
- **现象**：添加到桌面后标题显示为「Teacher M console」而不是简短名称
- **修复**：manifest.webmanifest 中 `short_name` 设为简短名称（如「M」），`name` 设为完整名称
- **关键配置项**：
  ```json
  {
    "display": "standalone",       // 必须，否则会显示浏览器 chrome
    "orientation": "portrait",     // 竖屏锁定
    "theme_color": "#0F1720",      // 状态栏颜色
    "background_color": "#0F1720"  // 启动页背景色
  }
  ```

---

## 二、多端同步（CloudBase）相关坑

### 2.1 SDK CDN 链接失效
- **现象**：手机端报 `tcb is not defined`
- **根因**：旧版 SDK CDN `https://web.sdk.qcloud.com/tcb-js-sdk/1.11.0/tcb.js` 已 404
- **修复**：
  - 用 npm 安装 `@cloudbase/js-sdk@2` + esbuild 打包成 IIFE 格式 `cloudbase-sdk.js`（约 1MB）
  - 从 HTML 中引用本地 SDK 文件，不依赖外部 CDN
  - 打包命令：
    ```bash
    npm install @cloudbase/js-sdk@2
    npx esbuild --bundle --format=iife --global-name=cloudbase \
      --outfile=cloudbase-sdk.js node_modules/@cloudbase/js-sdk/dist/commonjs/index.js
    ```
- **预防**：模板中直接包含 `cloudbase-sdk.js` 本地文件，永远不依赖外部 CDN

### 2.2 SDK API 迁移（v1 → v2）
- **现象**：初始化失败，`auth.anonymousAuthProvider is not a function`
- **根因**：v2 SDK API 接口发生变化
- **修复对照表**：
  | 旧版 API | 新版 API |
  |----------|----------|
  | `tcb.init({env})` | `cloudbase.init({env})` |
  | `auth.anonymousAuthProvider().signIn()` | `auth.signInAnonymously()` |
  | `db.collection('x').doc(id).get()` | `db.collection('x').doc(id).get()` (不变) |
- **预防**：确认 SDK 版本后再写代码，不要混用新旧 API

### 2.3 匿名登录未开启
- **现象**：手机端输入配对码后报「连接失败」
- **根因**：CloudBase 控制台默认关闭匿名登录
- **修复**：在 CloudBase 控制台 → 环境设置 → 登录授权 → 开启「匿名登录」
- **预防**：生成工作台后，在部署文档中明确告知用户必须开启匿名登录

### 2.4 数据库集合未创建
- **现象**：`syncPull()` 返回空，报错
- **根因**：CloudBase 数据库需要手动创建集合 `sync_data`
- **修复**：在 CloudBase 控制台 → 数据库 → 新建集合 `sync_data`
- **预防**：部署文档中明确列出所有需要创建的集合

### 2.5 同步冲突：清空数据不清理同步配置
- **现象**：用户点击「清空所有数据」后，界面仍显示「已同步」，配对码残留
- **根因**：`clearAllData()` 只清空 `store` 业务数据，没有清空 `syncConfig`
- **修复**：
  ```javascript
  function clearAllData() {
    store = getEmptyData();
    saveStore();
    syncConfig = null;           // 清除同步配置
    saveSyncConfig();            // 持久化空配置
    if (syncTimer) { clearInterval(syncTimer); syncTimer = null; }
    if (cloudbaseApp) { cloudbaseApp = null; }
    renderAll();
    renderSyncPanel();           // 刷新同步面板
  }
  ```
- **预防**：任何「重置」操作都要检查是否清除了所有非业务数据的配置

### 2.6 同步时机：创建配对后没立即 push
- **现象**：「创建配对」生成配对码后，另一台设备加入时显示「连接失败」
- **根因**：`showSyncPair()` 生成配对码后没有立即 push 数据到云端
- **修复**：在生成配对码后调用 `saveStore()`（触发 `syncPush()`）
- **预防**：任何创建配对/修改数据后，要确保数据已推送到云端

### 2.7 图片数据撑爆文档大小
- **现象**：CloudBase 单文档限制 1MB，包含 OOTD 照片数据的文档超限
- **根因**：Base64 编码的照片数据体积巨大
- **修复**：在 `syncPush()` 中用 `stripPhotosForSync()` 剔除所有图片数据，只同步文本数据。照片保留在各设备本地
- **预防**：多端同步时，大体积二进制数据（图片、文件）不进入云端，只保留在本地

---

## 三、功能实现相关坑

### 3.1 contentEditable 课表编辑不保存
- **现象**：编辑完课表后刷新页面，修改丢失
- **根因**：`contentEditable` 只修改 DOM，需要手动保存到 store
- **修复**：`saveScheduleEdit()` 遍历所有 `.sg-cell[contenteditable]` 单元格，提取 `textContent`，构建 `store.classSchedule` 数组，然后 `saveStore()`
- **关键代码**：
  ```javascript
  const rows = document.querySelectorAll('.sg-cell[contenteditable="true"]');
  // 5天 × 6节课 = 30个单元格，按 day × slot 索引提取
  for (let day = 0; day < 5; day++) {
    for (let slot = 0; slot < 6; slot++) {
      const idx = slot * 5 + day;
      periods[slot] = rows[idx].textContent.trim() || '—';
    }
  }
  ```

### 3.2 照片上传只能拍照不能选相册
- **现象**：用户反馈只能拍照，无法从相册选择已有照片
- **根因**：`<input type="file">` 上设置了 `capture="environment"` 属性，强制调用相机
- **修复**：去掉 `capture` 属性，保留 `accept="image/*"`
- **预防**：照片上传功能默认应支持相册选择，相机作为可选项

### 3.3 通知弹窗权限
- **现象**：Notification API 在非 HTTPS 环境下不可用
- **根因**：浏览器安全策略要求 Notification API 必须在 HTTPS 或 localhost 下使用
- **修复**：部署到 CloudStudio（HTTPS）后通知正常工作
- **预防**：部署环境必须支持 HTTPS，本地开发用 localhost

### 3.4 Canvas 饼图中文字体问题
- **现象**：Canvas 绘制文字颜色不正确
- **根因**：`ctx.fillStyle = 'var(--text-primary)'` 在 Canvas 中不生效，CSS 变量不是 Canvas 的有效颜色值
- **修复**：Canvas 中直接使用硬编码颜色值，不用 CSS 变量

### 3.5 头像图片撑爆页面
- **现象**：用户上传大图片作为「我的」页面头像后，整张图片溢出并铺满整个页面背景，文字完全看不清
- **根因**：「我的」页面的 `.profile-avatar` 容器只有 `width:80px; height:80px; border-radius:50%`，**没有** `overflow: hidden`，且没有为内部的 `img` 设置尺寸限制。`<img>` 标签按原始尺寸渲染，撑爆 flex 容器（`.profile-header`），最终覆盖整个屏幕
- **错误对照**：首页的 `.avatar-img` 是正确的（有 `overflow: hidden` 和 `img { width:100%; height:100%; object-fit:cover; }`）
- **修复**：
  ```css
  .profile-avatar {
    width: 80px;
    height: 80px;
    border-radius: var(--radius-full);
    overflow: hidden;
    flex-shrink: 0;     /* 防止 flex 布局中被拉伸 */
  }
  .profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  ```
- **预防**：
  - 任何**接收用户上传图片的圆形/方形容器**，必须同时设置 `overflow: hidden` 和子元素 `img { width:100%; height:100%; object-fit:cover; }`
  - flex 容器中上传图片组件，必须加 `flex-shrink: 0`
  - 给用户的应急方案：上传异常后可在「我的」→「编辑个人资料」清空头像字段，或直接「清空所有数据」
- **预防**：Canvas 绘制时使用实际颜色值（如 `#FFFFFF`、`#F871A0`），不要依赖 CSS 变量

---

## 四、CSS/UI 相关坑

### 4.1 深色主题的 CSS 变量覆盖不完整
- **现象**：切换到浅色主题后，部分 UI 元素仍然是深色
- **根因**：只设置了 `[data-theme="light"]` 的 `:root` 变量，但没有覆盖特定组件的背景色
- **修复**：为所有使用 `rgba(255,255,255,x)` 背景的元素添加 `[data-theme="light"]` 覆盖规则
- **必须覆盖的元素**：
  - `.profile-menu-item` 背景
  - `.profile-menu-badge` 背景和文字色
  - `.sync-btn-sm` 背景
  - 所有 `.bg-card-alt` 和 `.bg-glass` 类
- **预防**：切换主题后必测：个人资料页、同步面板、FAB 菜单、模态框

### 4.2 iOS Safari 安全区适配
- **现象**：iPhone 底部 tab bar 被 Home Indicator 遮挡
- **修复**：
  - `<meta name="viewport" content="... viewport-fit=cover">`
  - `.tab-bar { padding-bottom: env(safe-area-inset-bottom); }`
  - `.fab-btn { bottom: calc(24px + env(safe-area-inset-bottom)); }`
- **预防**：所有底部固定元素都要加 `env(safe-area-inset-bottom)`

### 4.3 移动端 100vh 问题
- **现象**：移动端浏览器地址栏收缩导致 100vh 变化，页面跳动
- **修复**：使用 `position: fixed` + `top:0; bottom:0` 替代 `height: 100vh`
- **预防**：移动端布局避免使用 `100vh`，用 fixed 定位代替

### 4.4 华为手机 PWA 安装横幅不弹出
- **现象**：华为浏览器打开工作台后，`beforeinstallprompt` 事件不触发，没有安装提示
- **根因**：华为浏览器（特别是 EMUI 版）对 PWA 的 `beforeinstallprompt` 支持不完整，和标准 Chrome 行为不一致
- **修复**：模板已处理——安装横幅事件如果 5 秒内未触发，会显示手动安装引导按钮。用户也可通过菜单→「添加到桌面」手动安装
- **预防**：部署后必须用华为浏览器实机测试 PWA 安装流程，不要假设横幅会自动弹出

### 4.5 HarmonyOS NEXT 不支持 Chrome
- **现象**：纯血鸿蒙系统上 Chrome 不可用，用户无法按常规指引安装
- **根因**：HarmonyOS NEXT 移除 Android 兼容层，Chrome 无法安装
- **修复**：引导用户使用**华为浏览器**（系统自带）打开工作台网址
- **PWA 安装方式**：华为浏览器菜单→「添加到桌面」
- **预防**：询问用户手机系统时，区分 HarmonyOS（兼容 Android）和 HarmonyOS NEXT（纯血鸿蒙），纯血系统只能用华为浏览器

### 4.6 iPhone iOS 通知功能受限
- **现象**：iPhone 从桌面打开 PWA 后，浏览器桌面通知不弹出
- **根因**：iOS 16.4 以下完全不支持 PWA 通知。iOS 16.4+ 支持但需要用户从主屏幕启动 PWA 且网站配置了 Push API
- **影响范围**：仅限浏览器桌面弹窗（Notification API），**应用内红点提醒不受影响**
- **修复**：无需额外修改，模板的通知系统会检测 `Notification.permission`，不支持时静默降级为仅红点提醒
- **预防**：给 iPhone 用户的预期管理——「通知红点会正常显示，但浏览器弹窗可能不支持」

---

## 五、部署相关坑

### 5.1 CloudStudio 重新部署不换 URL
- **现象**：从同一目录重新部署，URL 不变（沙箱复用）
- **这是特性不是 bug**：数据不会因重新部署丢失
- **预防**：部署文档中说明 URL 稳定性，避免用户担心「更新后会丢数据」

### 5.2 SW 缓存导致 CloudStudio 部署不生效
- **现象**：CloudStudio 部署成功后，浏览器访问仍然是旧版
- **根因**：SW 的 navigate 请求使用了 network-first 策略，但如果 SW 自身没更新，旧的 SW 继续服务
- **修复**：确保每次部署前递增 CACHE_NAME，SW 文件本身的内容变化会触发浏览器检查更新
- **预防**：部署前先改 SW 版本号

---

## 六、数据模型相关坑

### 6.1 localStorage 容量限制
- **现象**：数据量大时（尤其是 Base64 图片）localStorage 写入可能失败
- **根因**：localStorage 通常限制 5-10MB
- **预防**：
  - 图片数据限制 500KB 以内
  - 大量历史数据建议提供导出功能
  - 可选云同步减轻本地存储压力

### 6.2 数据版本兼容
- **现象**：新增字段后，旧数据的 localStorage 中没有该字段，导致 `undefined` 错误
- **修复**：在 `loadStore()` 中做数据迁移/默认值填充
- **预防**：每次新增数据字段时，检查 `loadStore()` 是否需要兼容旧数据格式

---

## 七、ClawHub 上架相关坑

### 7.1 ClawHub CLI 默认连接内网地址
- **现象**：`clawhub login` 报 `getaddrinfo ENOTFOUND copilot.tencent.com`
- **根因**：CLI 默认 registry 指向腾讯内网 `copilot.tencent.com`，公网不可达
- **修复**：必须显式设置环境变量 `CLAWHUB_SITE=https://clawhub.ai CLAWHUB_REGISTRY=https://clawhub.ai`
- **预防**：所有 clawhub 命令前都加这两个环境变量

### 7.2 设备授权流程在内置浏览器中失败
- **现象**：WorkBuddy 内置浏览器打开 ClawHub 设备授权页，GitHub 登录后页面无限刷新
- **根因**：内置浏览器（WebView）不支持 GitHub OAuth 的 Cookie/跳转机制
- **修复**：改用系统浏览器（Safari/Chrome）打开授权链接
- **预防**：涉及 OAuth 登录的场景一律引导用户使用系统浏览器

### 7.3 设备码后台进程被杀导致 token 未保存
- **现象**：用户在浏览器完成授权，但 `clawhub whoami` 仍显示未登录
- **根因**：`clawhub login --device` 在后台运行时，Bash 工具调用结束后进程被终止，轮询中断，token 未保存
- **修复**：改用 `--token` 方式直接写入 API Token，跳过设备授权流程
- **获取 Token 步骤**：clawhub.ai → 登录 → Settings → API Tokens → 创建 → 复制
- **预防**：优先使用 `clawhub login --token <token>` 方式，不依赖设备授权

### 7.4 GitHub 账号未满 14 天无法发布技能
- **现象**：`clawhub skill publish` 报 `GitHub account must be at least 14 days old to publish skills`
- **根因**：ClawHub 反垃圾注册机制，新 GitHub 账号需满 14 天才能发布技能
- **限制**：CLI 和网页端均受此限制，无法绕过
- **应对方案**：
  1. 等待 GitHub 账号满 14 天后重新发布
  2. 使用已有 14 天以上的 GitHub 账号
  3. 期间通过 zip 包直接分享给其他用户手动安装
- **预防**：SKILL.md 中标注此限制，提醒用户提前准备符合条件的 GitHub 账号

---

## 八、生成工作台时的必检清单

每生成一个新工作台，必须检查：

- [ ] `index.html` 中所有 CSS 变量名和值与定制参数一致
- [ ] 项目数量与用户指定的项目数量一致，tab bar 导航正确
- [ ] `getEmptyData()` 中的默认数据与用户需求匹配
- [ ] `manifest.webmanifest` 的 `short_name` 和 `name` 正确
- [ ] SW 的 `CACHE_NAME` 已设置初始版本（如 `workbench-v1`）
- [ ] 所有底部固定元素有 `env(safe-area-inset-bottom)` 适配
- [ ] 手机端 viewport meta 包含 `viewport-fit=cover`
- [ ] 如启用云同步，CloudBase SDK 文件已包含
- [ ] 如启用云同步，部署文档包含匿名登录和集合创建说明
- [ ] 深色/浅色主题切换覆盖了所有关键 UI 元素
- [ ] 通知权限请求逻辑正确（HTTPS 环境必须）
- [ ] 所有接收用户上传图片的容器都有 `overflow: hidden` + `img { width:100%; height:100%; object-fit:cover; }`（见 3.5）
- [ ] flex 容器中的图片组件都有 `flex-shrink: 0`
- [ ] 已根据用户手机品牌给出正确的 PWA 安装指引（见 SKILL.md Step 5）
- [ ] 华为手机用户：确认引导用华为浏览器/Chrome，不用百度/UC
- [ ] iPhone 用户：确认引导用 Safari 添加到桌面，且说明通知可能受限
- [ ] HarmonyOS NEXT 用户：确认引导用华为浏览器（Chrome 不可用）
