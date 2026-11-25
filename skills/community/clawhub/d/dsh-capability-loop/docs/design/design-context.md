# design-context · 能力闭环面板（Harness Web GUI）

> 用途：本次「dsh-capability-loop 面板」设计稿的**现有系统取证**。按 `references/55-design-intake.md` 要求，出稿前必须有此文件；缺项一律写「未取证 + 责任人 + 截止日」，不得用形容词代替。
> 取证时间：2026-11-18 21:50 起（约 25 分钟，Asia/Shanghai）
> 取证人：lead（本会话，非面板实现者）
> 状态：**PARTIAL**（缺「Plugins 页面运行截图」一项，见 §8；其余为源码/文档/本机截图一手证据）

## 1. 系统与环境

| 项 | 值 | 证据 |
|---|---|---|
| 产品 | DeepSeek Harness Desktop | 运行进程 `DeepSeek Harness.exe`（PID 10768） |
| DSH CLI 包 | `@deepseek-ai/dsh` `0.2.2-rc.3` | `$DSH_INSTALL_DIR/package.json` |
| Profile | `desktop`（`%USERPROFILE%\.dsh\profiles\desktop`） | `$env:DSH_PROFILE` / `$env:DSH_PROFILE_DIR` |
| Web 客户端 | React + Cordis Client 插件（slot 组合），无第三方 UI 组件库 | `@deepseek-ai/dsh-client-ui-layout` README；`dsh-client-ui-*` 包清单 |
| 主题机制 | `--dsw-*` token 样式表 + `body[data-ds-dark-theme]`；亮/暗/跟随系统 | `dsh-client-ui-theme` README §Theme presentation；`src/styles/design-platform.css` |
| 面板注册机制 | 全局面板 = `sidebar.panellist` 列表项 + 根级 `main` keyed slot；`ctx.layout.selectPanel(id)` 切换；Plugins 页即此模式 | `dsh-client-ui-sidebar` README §Global panel entries；`dsh-client-ui-plugin-manager` README §Registration；`dsh-client-ui-layout` README |

## 2. 外壳结构（不得改）

| 项 | 值 | 来源 |
|---|---|---|
| 三栏 | 左 sidebar / 中 main / 右 rightbar | ui-layout README |
| sidebar 宽 | 264–420，默认 **280**；折叠导轨 **56**（≥768） | ui-layout README |
| 断点 | <1024 自动折叠；<768 抽屉式；右侧面板首开 45%，上限 70%，保中心 ≥400 | ui-layout README |
| sidebar 行高 | 展开 **32px**，行间距 2px；折叠导轨控件 36px，间距 12px | ui-sidebar README §Global panel entries |
| sidebar 内边距 | `--dsh-sidebar-inline-padding: 8px`、`--dsh-sidebar-row-padding: 12px`、`--dsh-sidebar-label-gap: 6px`、`--dsh-sidebar-paint-inset: 3px` | ui-sidebar README |
| 页面内容宽 | **960px** 上限，居中；左右 inset `clamp(24px, 4vw, 48px)`，<768 为 20px | `PluginManagerPage.module.css` `.page` |
| 页头顶部 inset | **28px**（静止）/ 16px（滚动压缩后） | `PluginManagerPage.module.css` `.page`；ui-plugin-manager README |
| 内容块间距 | 32px；底部 48px | `PluginManagerPage.module.css` `.pageBody` |
| 顶栏/Tab | 会话页为「对话/轨迹/上下文/编排/统计」；管理页 Tab 高 34px | 运行截图；ui-plugin-manager README |

本机运行截图：`.tmp/design-evidence/desktop-window.png`（1936×1048，本会话窗口；暗色主题 + 用户壁纸）。

## 3. 主题与 token（实测值，逐条可 grep）

来源：`@deepseek-ai/dsh-client-ui-theme/src/styles/design-platform.css`（`body` = 亮色，`body[data-ds-dark-theme]` = 暗色）、`base.css`、`gradient-shadow-text.css`。

### 3.1 颜色（alias → static）

| 语义 | 亮色 | 暗色 |
|---|---|---|
| `--dsw-alias-bg-base` | `#ffffff`（neutral-bluish-00） | `rgb(21,21,23)`（950） |
| `--dsw-alias-bg-layer-1` | `#ffffff` | `rgb(35,35,36)`（875） |
| `--dsw-alias-bg-layer-2` | `#ffffff` | `rgb(44,44,46)`（850） |
| `--dsw-alias-bg-layer-3` | `#ffffff` | `rgb(53,54,56)`（800） |
| `--dsw-alias-label-primary` | `rgb(15,17,21)`（1000） | `rgb(249,250,251)`（50） |
| `--dsw-alias-label-secondary` | `rgb(97,102,107)`（700） | `rgb(207,211,214)`（300） |
| `--dsw-alias-label-tertiary` | `rgb(129,133,140)`（600） | `rgb(173,178,184)`（400） |
| `--dsw-alias-label-caption` | `rgb(173,178,184)`（400） | `rgb(129,133,140)`（600） |
| `--dsw-alias-border-l1` | `rgba(0,0,0,.04)` | `rgba(255,255,255,.06)` |
| `--dsw-alias-border-l2` | `rgba(0,0,0,.10)` | `rgba(255,255,255,.12)` |
| `--dsw-alias-border-l3` | `rgba(0,0,0,.12)` | `rgba(255,255,255,.16)` |
| `--dsw-alias-state-business-primary` | `rgb(65,118,230)`（deepseek-500） | `rgb(122,170,255)`（deepseek-400） |
| `--dsw-alias-state-success-primary` | `rgb(34,197,94)` | 同左 |
| `--dsw-alias-state-warn-primary` | `rgb(245,158,11)` | 同左 |
| `--dsw-alias-state-error-primary` | `rgb(236,19,19)` | `rgb(242,90,90)` |
| `--dsw-alias-state-done-primary` | `rgb(124,58,237)`（violet-600） | `rgb(167,139,250)`（violet-400） |
| `--dsw-alias-card-fill` | `rgb(250,250,250)` | `rgb(33,33,35)` |

### 3.2 圆角 / 阴影 / 字体

| 项 | 值 | 来源 |
|---|---|---|
| 圆角 | `--dsw-radius-xs 4 / sm 8 / md 12 / lg 16 / xl 20 / panel 28` | `base.css` |
| 阴影 | `--dsw-shadow-lv1/2/3`；浮层用 `--dsw-elevation-panel/prominent/soft`（0.5px 发丝描边 + 两层柔光） | `gradient-shadow-text.css` |
| 文本字体 | `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', …` | `base.css` |
| 正文字号 | 默认 **14px**，可设 10–22；次级 = 正文 −1/2（默认 13px）；小号固定 | `gradient-shadow-text.css`；ui-theme README |
| 焦点环 | `--dsw-focus-ring-color`（亮 `#4176E6` / 暗 `#7AAAFF`），宽 2px（密集表格可 1px） | `focus.css`；ui-theme README |

## 4. 布局骨架与页面样本

- **全局面板页的骨架**（以 Plugins 页为参照，`PluginManagerPage.module.css`）：页头（标题 + 副标题 + 右侧动作）→ 可选 Tab → 内容块（32px 间距、960px 宽度）→ 底部 48px 余量；页头随滚动压缩，Tab 落位到页头右侧。
- **列表/卡片**：官方插件页用「卡片头（图标 48px + 标题/描述）+ 行（32–40px）+ 右侧开关」；Tab 用 34px 高、选中指示 2px inset。
- **本会话实测截图**：`/` 触发菜单未在本截图出现；会话页顶栏 5 个 Tab、右侧「1 个后台任务」、底部 composer 为胶囊形。面板页**不复制会话页背景壁纸**，应使用 `--dsw-alias-bg-base` 纯色（Plugins 页同款）。

## 5. 状态清单（现有页面已覆盖的态）

| 态 | 现有做法 | 来源 |
|---|---|---|
| loading | 骨架卡（3 行 + 4 卡），透明度脉冲，`prefers-reduced-motion` 时静止 | ui-plugin-manager README |
| empty | 居中短句 + 一个主行动按钮 | ui-plugin-market README（无索引源） |
| error | 就地短句 + `Retry`，不弹 toast（首屏） | ui-plugin-market README |
| stale/refresh | 保留旧内容 + 失败 toast；手动刷新有 spinner 最短 400ms | ui-plugin-manager README |
| disabled | `disabled` 控件 + tooltip 说明原因 | ui-plugin-manager README |
| hover | 仅 `@media (hover: hover)` 生效，避免触屏粘滞 | `PluginManagerPage.module.css` 头注释 |

## 6. 差异清单（本设计不用现有方案的地方）

| # | 差异 | 为什么 | 影响面 |
|---|---|---|---|
| D1 | 新增「阶段轨道（stepper）」组件 | 现有 DSH 无阶段进度组件；本面板核心是 7 阶段状态 | 仅本页；用现有 token 与 32px 行高，不引入组件库 |
| D2 | 新增 4 个「指标块」 | 现有管理页无 KPI 块；指标是闭环可度量的入口 | 仅本页；数字用 `--dsw-font-markdown-*` 或 20px/600，不新增字号档 |
| D3 | 页头常驻「接管档位」分段控件 | 接管必须是用户可控的开关，不能藏进二级页 | 复用现有 segmented 控件形态（如 Appearance 三项） |
| D4 | 状态色新增「影子」态 | 影子=记录不阻断，语义介于 idle 与 warn；**不新增色值**，用 `state-warn-secondary` + 虚线边框表达 | 仅本页 |
| D5 | 新增「能力地图」12 卡网格 | 全量能力需要总览入口；现有管理页无此密度 | 仅本页；卡片规格沿用 `card-fill` + `radius-md` |
| D6 | 新增「运行中心」（进度/输出尾部/取消） | 面板要「一步到位跑门禁」；现有页无运行队列 | 仅本页；输出用 `--ds-font-family-code` 11px，进度条用 `state-business-primary` |
| D7 | 页宽 1000px（现有 960） | 7 个 Tab + 运行历史需要更宽；只改本页内容宽，不动外壳 | 仅本页；>1440 时仍居中，左右至少 40px |
| D8 | Tab 数 7（现有 2–3） | 全量能力分组；不是新组件，沿用 34px Tab 规格 | 960px 下 7×4 字可容纳；更窄横向滚动 |

## 7. 复用与禁止

- **复用**：`--dsw-alias-*` 全部颜色；半径/阴影/焦点环/字体栈；sidebar 行高与内边距；28px 页头 inset；34px Tab；骨架/空态/错误态模式；运行输出用现有代码字体。**页宽 1000px 是本设计的差异项（现为 960），见 §6 D7。**
- **禁止**：`--dsw-*` 之外自造颜色；新字号档；新圆角档；`filter: invert()` 做暗色；iframe 承载面板（不继承主题/locale，见 dsh-doc `practices.md`）；读取其他插件 DOM 估位。

## 8. 未取证清单（D-ID）

| ID | 缺什么 | 原因 | 责任人 | 截止 |
|---|---|---|---|---|
| D-01 | Plugins 页面**运行截图**（亮/暗各一张，1440 宽） | Web GUI 需 `dsh web` 打印的鉴权 URL；桌面壳未开远程调试端口，headless Chrome 被 401 拒绝（证据：`.tmp/design-evidence/gui-1440.png`） | lead | 面板 P1 实现时用真实插件页补 |
| D-02 | 面板在 375/768/1024/1440/1920 的真实渲染（7 Tab + 运行中心） | 尚未实现 | 实现者 | P2 验收前 |
| D-03 | 暗色下 `state-warn-secondary` 虚线边框的实际对比度 | 设计稿用样值，未实测 | 实现者 | P2 验收前 |
| D-04 | 侧边栏「能力闭环」图标在 56px 导轨下的可辨识度 | 尚无图标 | 设计者 | P1 出图标时 |

> 本文件与设计稿 `2026-11-18-capability-loop-panel.md` 同目录；两者不一致时以设计稿的「差异清单」为准并回写本文件。
