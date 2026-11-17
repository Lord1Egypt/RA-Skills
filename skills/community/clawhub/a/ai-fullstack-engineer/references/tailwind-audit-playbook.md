# Tailwind CSS 审计深度 Playbook

> 本文件是 `tailwind-audit` 子技能的**深层参考**，按需读取。聚焦 Tailwind 项目的诊断与体检，不重复 `css-master` 的布局写法，也不重复 `web-performance` 的通用性能指标。

## 0. 前置：确认版本与安装方式

审计结论高度依赖 Tailwind 主版本，落地前先核对：

```bash
# 看项目实际安装的版本
cat package.json | grep -A2 -B2 tailwindcss
npx tailwindcss --help        # 确认本地 CLI 可用及其子命令
```

- **v3**：配置在 `tailwind.config.js`，扫描靠 `content` 数组，指令 `@tailwind base/components/utilities`，`@apply` 支持任意变体（含响应式/状态）
- **v4**：CSS-first 配置（`@theme` / `@import "tailwindcss"`），扫描靠 `@source` / 自动探测，构建走 `@tailwindcss/postcss` 或 CLI；**`@apply` 仅支持简单工具类，不支持响应式/状态变体**（这是迁移期最常踩的坑）

---

## 1. 决策树：先定审计类别

```
这次体检最关心什么？
├─ 生产 CSS 体积偏大 / 怀疑没用到的类很多？
│   └─ 走 §2 体积与 purge 审计
├─ 刚把 v3 升到 v4 / 准备升？
│   └─ 走 §3 v3→v4 迁移审计
├─ 配置里定义了一堆主题，不确定有没有人用？
│   └─ 走 §4 配置漂移审计
├─ 同一元素上写了多个互斥/重复的类？
│   └─ 走 §5 类名冲突与去重
└─ 大量 @apply / 动态拼接类名？
    └─ 走 §6 @apply 与动态类名审计
```

> 一次审计可覆盖多类，但**先定主目标**能避免清单发散。

---

## 2. 体积与 purge 审计（最常被问）

**核心问题**：`content` 路径配错 → 本该被 tree-shake 的类没生成，或反过来生成了一堆根本没用的类。

```bash
# 2.1 直接看构建产物体积（先看数字）
npx tailwindcss -i ./src/input.css -o ./dist/out.css --minify
ls -lh dist/out.css

# 2.2 抽查某个「应该存在」的类是否真的生成了
grep -c "bg-blue-500" dist/out.css

# 2.3 抽查某个「只在注释/字符串里出现」的类是否被误生成（误生成=content 路径过宽）
grep -c "hover:scale-110" dist/out.css
```

**判读**：
- 产物里**缺失**实际用到的类 → `content` 路径漏了目录（如漏了 `./src/components/**`），样式会「偶尔丢类」，最难查
- 产物里**存在**只出现在字符串/注释里的类 → `content` 匹配过宽或误把 `.md`/`.test.tsx` 扫进来了，体积虚胖

**常见漏配清单**：
- `content` 用了绝对路径或写死了 `./src` 却实际在 `./app`
- 动态拼接类名的文件没进 `content`（见 §6）
- 忘了把 `node_modules` 里某组件库的模板加进 `content`（如 `content: [{ path: './node_modules/@acme/ui/**/*.{js,tsx}' }]`）

---

## 3. v3 → v4 迁移审计（漏改清单）

按官方迁移路径逐项核对（v4 行为变化大，逐项过比整体搜更稳）：

| 检查项 | v3 写法 | v4 现状 | 漏改后果 |
|--------|---------|---------|----------|
| 入口指令 | `@tailwind base/components/utilities` | `@import "tailwindcss"` | 构建报错或样式全丢 |
| 配置文件 | `tailwind.config.js`（JS） | CSS-first：`@theme { }` | 主题扩展不生效 |
| 暗色模式 | `darkMode: 'class'` + `dark:` | 默认 `prefers-color-scheme`；用 `@custom-variant dark (&:where(.dark, .dark *))` 恢复 class 策略 | 暗色突然跟随系统 |
| 容器 | `container` 类 + `theme.container` | 默认移除，需 `@container` 或插件 | `container` 类无效 |
| 不透明度修饰 | `bg-red-500/50` 自动支持 | 需配合新版色板 | 透明度失效 |
| `divide` / `outline` 色 | 旧默认色 | 调整 | 边框/轮廓色异常 |
| `@apply` 变体 | 支持 `hover:`,`md:` | **不支持变体**（仅简单工具类） | 构建失败 |
| 插件 API | JS 插件 `plugin()` | CSS `@plugin` | 旧插件不加载 |

```bash
# 扫一遍典型的 v3 残留写法
grep -rn "@tailwind" src/ && echo "⚠ 仍有 v3 指令残留"
grep -rn "darkMode" tailwind.config.* && echo "⚠ 仍有 v3 配置残留"
grep -rn "@apply.*hover:\|@apply.*md:\|@apply.*focus:" src/ && echo "⚠ @apply 含变体（v4 不支持）"
```

---

## 4. 配置漂移审计（定义了 vs 用了）

**目标**：找出「`theme.extend` 里定义却从没用过」的主题键（死配置），以及「用了却没在 config 里定义」的类（靠默认或魔法）。

```bash
# 4.1 取 config 里扩展的自定义色/间距键
grep -oE "(colors|spacing|fontSize)\s*:\s*\{" tailwind.config.* 

# 4.2 在源码里抽查某个自定义键是否被引用
grep -rn "brand-" src/ | head
```

**判读**：自定义键在源码里 `grep` 不到 → 多半是死配置，可删；反之源码里出现 `bg-unknown` 却不在 config → 说明依赖了默认/魔法值，应显式定义以便审计。

---

## 5. 类名冲突与去重审计

**问题**：同一元素写了互斥类（如 `px-2 px-4`、先后 `text-red-500 text-blue-500`），后者覆盖前者，前者是噪音；或团队没统一顺序，diff 噪音大。

```bash
# 5.1 粗扫同一 JSX 行出现多个 padding/颜色工具类的情况（需人工确认是否真冲突）
grep -rnoE "class(Name)?=[\"\{][^\"}]*" src/ | head -50

# 5.2 用官方/社区 lint 强制类顺序与非法组合
npx eslint . --plugin tailwindcss \
  --rule '{"tailwindcss/no-contradicting-classname": "error"}' \
  --rule '{"tailwindcss/classnames-order": "warn"}'
```

> 若项目是 **Tailwind v4**，官方提供了 `@tailwindcss/lint`（在能安装的前提下）做同类检查；命令以目标环境实际可用为准，先 `npx @tailwindcss/lint --help` 确认。运行时去重可用 `tailwind-merge`：`twMerge("px-2 px-4")` → `"px-4"`。

---

## 6. @apply 与动态类名审计

**6.1 @apply 滥用**
- v3 里 `@apply hover:px-4` 能跑；**v4 直接报错**——迁移期第一波雷。
- `@apply` 把工具类「烘焙」进组件 CSS，过度使用会**膨胀每个组件的样式块**，且失去 Tailwind 的跨文件去重。
- 体检：统计单个文件 `@apply` 数量，>10 条的基本可以还原成原生 className。

```bash
grep -rc "@apply" src/ | awk -F: '$2>10'
```

**6.2 动态拼接类名断 purge（最隐蔽）**
Tailwind 的 purge 是**静态扫描文本**的，以下写法会让类「看不见」而被摇掉：

```jsx
// ❌ 会被摇掉：bg-red-500 这个完整字符串从不出现在源码
<div className={`bg-${color}-500`} />

// ✅ 安全：完整字面量出现，purge 能识别
const map = { red: 'bg-red-500', blue: 'bg-blue-500' }
<div className={map[color]} />

// ✅ 或用 safelist（v3）明确声明动态类
// tailwind.config.js: safelist: [{ pattern: /bg-(red|blue|green)-500/ }]
```

体检：扫 `className={` 与字符串模板插值，标记所有「类被拆成变量拼接」的位置，逐个确认是否进了 `content` 或 `safelist`。

---

## 7. 审计产出清单（交付前自核对）

- [ ] 已确认目标 Tailwind 版本（v3 / v4）并据此选择命令
- [ ] 体积审计：产物体积数字 + 至少 2 个「应存在/不应存在」类的 `grep` 实证
- [ ] 若处于迁移期：§3 表格逐行核对，列出漏改文件与行号
- [ ] 配置漂移：列出死配置键（定义了没用）与未定义却使用的类
- [ ] 冲突/重复类名：用 lint 或 `tailwind-merge` 给出去重建议
- [ ] @apply 滥用：标出 >10 条 `@apply` 的文件；动态类名：标出所有模板插值处并确认 purge 安全
- [ ] 重大整改（删配置、改 `@apply`、动 `safelist`）**先出报告**，不擅自拍板改动生产样式

---

## 8. 高频踩坑速查

| 现象 | 根因 | 修法 |
|------|------|------|
| 某些页面样式「偶尔丢」 | `content` 漏了动态路由/组件目录 | 补全 `content` glob，重构建验证 |
| 生产 CSS 几百 KB 但页面很简单 | `content` 扫了 `.md`/测试文件或漏配 safelist 反向 | 收窄 `content`；把真正动态的列进 `safelist` |
| v4 升级后 `@apply hover:px-4` 构建失败 | v4 `@apply` 不支持变体 | 改为在 className 上写 `hover:px-4`，或拆出组件类 |
| 暗色模式突然跟随系统 | v4 默认 `prefers-color-scheme` | 用 `@custom-variant dark` 恢复 class 策略 |
| 同元素两种颜色都写了却只生效一个 | 后写的覆盖前一个（噪音） | 删冗余，用 lint/`twMerge` 去重 |
| `bg-${c}-500` 不生效 | 静态 purge 看不见拼接字符串 | 用字面量映射或 `safelist` |
| `container` 类升级后失效 | v4 默认移除 container | 改用 `@container` 或装 `@tailwindcss/container-queries` |

---

## 相关参考

- 前端通用范式（含 Tailwind 集成）：[references/frontend-playbook.md](frontend-playbook.md)
- 布局写法（非审计视角）：[skills/css-master](../skills/css-master/SKILL.md)
- 通用性能指标：[skills/web-performance](../skills/web-performance/SKILL.md)
- 本 playbook 归属子技能：[skills/tailwind-audit](../skills/tailwind-audit/SKILL.md)
