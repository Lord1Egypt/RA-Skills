# APK 仪表盘 App 内部架构

本 App 是 Capacitor 项目，核心为单文件 `dist/index.html`（~1100 行）。Android 层只提供一个 WebView 壳子，所有 UI 和业务逻辑在 HTML 内。

## 文件结构（dist 目录）

```
dist/
└── index.html          # 唯一源码，内嵌 CSS + JS + ECharts
android/
└── app/
    └── build.gradle    # versionCode + versionName + 签名配置
```

## 字段索引映射（FI）

Feishu base v3 API 使用 `offset` 翻页时，记录以**位置数组**返回。`FI` 对象定义字段位置：

```javascript
var FI = {text: 0, month: 1, amount: 2, category: 3, type: 4};
```

| 索引 | 字段名 | Feishu 类型 | JS 访问方式 | 示例值 |
|------|--------|-------------|------------|--------|
| 0 | 文本 | 文本 | `r[FI.text]` | `"2026-05-21 12:30 午饭"` |
| 1 | 月份 | 文本 | `r[FI.month]` | `"2026-05"` |
| 2 | 金额 | 数字 | `r[FI.amount]` | `23.50` |
| 3 | 分类 | 单选 | `r[FI.category]` | `["餐饮"]` |
| 4 | 类型 | 单选 | `r[FI.type]` | `["支出"]` |

注意：单选/多选字段在数组中的值是 **数组**（`["餐饮"]`），取第一个用 `arr[0]`。

**FI 顺序由 setup_bitable.py 中 create_field 的调用顺序决定**，不能随意调整。

## 业务逻辑流程

### 数据生命周期

1. **登录** → 输入 App ID / Secret / Base Token / Table ID → 存 localStorage
2. **init()** → getToken() → fetchAll() → 拉取全部明细记录 → showApp() + render()
3. **刷新** → doRefresh() → 重新 fetchAll → 渲染
4. **月份切换** → 改变 curMonth → re-render（不复拉数据）
5. **全部模式** → isTotalMode=true → render(month=null) → 聚合所有月份

### 渲染链

```
render()
├── getMonthSummary(month)      → 遍历 detailRecords，按 type 字段区分收支
├── renderSummary(inc, exp)     → 三张卡片 + 自适应字号（canvas measureText）
├── renderPie(cats)             → 支出饼图（ECharts 环形图）
├── renderIncPie(incCats)       → 收入饼图（仅在 showIncomePie=true 时）
├── renderHBar(cats)            → 分类金额水平条形图
├── renderBar()                 → 月度对比柱状图（从 detailRecords 按月份聚合）
├── renderLine(month)           → 日支出趋势折线图
└── renderDetails(month)        → 消费明细列表 + 分页
```

### 样式架构

- 主题通过 `data-theme` 属性切换（dark / light）
- 所有颜色通过 CSS 变量引用（`var(--bg)`, `var(--card)` 等）
- ECharts 颜色通过 `CUR_THEME` 对象传递
- 按钮反馈统一使用 `transform:scale`
- 页面入场：`fadeUp` 动画

## UI 约定速查

| 组件 | CSS 类 | 按压反馈 | 禁用态 |
|------|--------|----------|--------|
| 导航按钮 | `.mbtn` | `scale(.88)` | `opacity:.35, cursor:not-allowed` |
| 主操作按钮 | `.lbtn` | `scale(.97)` | (无禁用态) |
| 弹窗按钮 | `.dbtn` | `scale(.95)` | (内联控制) |
| 功能按钮按下态 | `.pressed` | 背景色变 accent，颜色变白 | — |
| header 齿轮 | `.mbtn.sett:active` | `rotate(45deg)` | — |
| header 刷新 | `.mbtn.refresh:active` | `rotate(180deg)` | — |

## 弹窗系统

所有弹窗使用同一套模式：

1. 点击触发 → `lock-scroll` → 移除 overlay 的 `hidden` → 显示 `dialogIn` 动画
2. 关闭 → `closeOverlay(id)` → 加 `.closing` 类触发 `dialogOut` 动画（150ms）→ 加 `.hidden` → 移除 `lock-scroll`
3. 背景关闭 → 绑定 `click` 事件检查 `e.target === this`

| 弹窗 | overlay ID | 关闭方式 |
|------|-----------|----------|
| 设置 | `sett-overlay` | 点击 ✕ / 背景 |
| 分类设置 | `cat-overlay` | 点击 ✕ / 背景 |
| 检查更新 | `upd-overlay` | 点击按钮 / 背景 |
| 关于 | `abt-overlay` | 点击 ✕ / 背景 |
| 刷新确认 | `refresh-overlay` | 点击按钮 / 背景 |
| 通用错误 | `.dialog` | 点击按钮 |

## 主题系统

```javascript
var THEMES = {
  dark:  { tooltipBg: '#1a1a2e', tooltipBorder: '#2a2a4a', ... },
  light: { tooltipBg: '#ffffff', tooltipBorder: '#ddd6cc', ... }
};
```

`applyTheme(theme)` 会：
1. 设置 `data-theme` 属性 + `localStorage` 持久化
2. 更新按钮图标（☀ / 🌙）
3. 全部 dispose 已有 ECharts 实例
4. 调用 `render()` 重绘
5. 给每个图表容器加 `.chart-fade` 淡入类（300ms 后移除）

## 版本号三处同步

| 文件 | 变量 | 示例 |
|------|------|------|
| `dist/index.html` (JS) | `APP_VERSION` | `'1.3.0'` |
| `android/app/build.gradle` | `versionCode`, `versionName` | `14`, `"1.3.0"` |
| 仓库 `SKILL.md` | `version:` | `1.3.0` |

versionCode 计算：主×10000 + 次×100 + 修订，每次 release +1。

## 构建与发布

```bash
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
cd /path/to/feishu-dashboard-app
bash sync.sh
# APK 输出到 android/app/build/outputs/apk/release/app-release.apk
```

发布流程：构建 → 用户测试 → git add + commit → git tag → GitHub Release（手动）
