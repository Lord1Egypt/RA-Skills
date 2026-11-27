# color-system-design

[![skills.sh](https://skills.sh/b/shxuk/color-system-design)](https://skills.sh/shxuk/color-system-design)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-green.svg)](./package.json)

简体中文 | [English](./README.en.md)

> **一句话定义**：`color-system-design` 是一个开源的**UI 配色系统生成器（Agent Skill + CLI）**，只需输入 1 个主视觉 Hex 色号，即可通过纯算法生成明暗双模式颜色矩阵、HTML 预览报告及 CSS/Tailwind 约束变量，无需大模型参与。
> 适合 **Web/App 开发者、Vibe Coding 用户与设计系统维护者**；不适合 **品牌 Logo 艺术创作或印刷 CMYK 配色**。

做 App、做网站，尤其是 Vibe Coding 的时候，很容易写着写着颜色就乱了，搭配起来很奇怪。

这个项目把几个出名的开源项目和标准（**GitHub Primer** 的颜色角色命名、**Adobe Leonardo** 的对比度计算、**W3C DTCG / Style Dictionary**、**APCA** 对比度参考）揉到了一起。它生成的配色**十分稳定，几乎不需要二次调整**。

**你只需要给它 1 个主视觉色号**，它就能自动帮你算出一整套搭配稳定的颜色矩阵——包括背景、文字、边框、交互态、不打架的提示色，以及自动转换好的明暗两套色系。

最后它会交给你两样东西：

1. **一个给人看的 HTML**（`dist/color-report.html`）：打开就能看到网站和 App 上的实际效果、每个颜色怎么用，点一下就能复制。
2. **一套给 AI 和代码用的约束工具**：直接可用的 CSS 变量、Tailwind 配置，外加一个检查脚本，防止后面改代码时 AI 又把颜色写乱。

---

## 30 秒上手

```bash
# 1) 作为 Agent Skill 安装（Claude Code / Cursor / Trae / Antigravity）
npx skills add shxuk/color-system-design

# 2) 或本地 CLI 运行
git clone https://github.com/shxuk/color-system-design.git && cd color-system-design
pnpm install
pnpm generate -- --seed "#007275"
```

运行完之后，直接去 `dist/` 目录看结果：

- **给人看**：用浏览器打开 `dist/color-report.html`
- **给代码用**：引入 `dist/tokens.css`（原生 CSS）或 `dist/tailwind.theme.css`（Tailwind v4 `@theme`）或 `dist/tailwind.preset.cjs`（Tailwind v3）

常用可选参数：

- `--tint subtle|pure|warm|cool`：调整背景灰的倾向（默认 `subtle`，微微带一点主视觉色调）
- `--no-semantic`：只要主色和危险红，不生成成功/警告/提示色
- `--out ./my-theme`：换个输出目录

---

## 给 AI 用的约束检查

如果你在项目里接入了这套颜色，可以跑一下检查脚本，确认亮暗模式对比度达标、没有写乱：

```bash
# 从 tokens/ 重新编译 CSS
pnpm tokens:build

# 跑对比度和角色检查（支持加上 --scan ./src 扫一下代码里有没有乱写 Hex）
pnpm tokens:check
```

---

## 它是怎么运作的

你只需要给一个主视觉 Hex 色号，脚本会按下面几步把整套颜色矩阵算出来：

1. **先钉死纸面和中性灰（OKLCH）**：取主视觉的色相，把彩度压到极低（几乎是纯灰但微微带点主色调），按目标对比度反解出亮色和暗色两套背景、卡片、分割线和正文灰。这样可以避免页面灰蒙蒙或纸色跑偏。
2. **再算主视觉的交互色（Adobe Leonardo）**：把上面钉死的亮/暗纸面作为背景，分别算出链接、按钮、Hover 态对应的色阶。暗色模式单独给高亮种子重算，不直接拿亮色反色，防止暗色下发灰看不清。
3. **自动配齐不打架的提示色（异色分离）**：按常识生成危险（红）、成功（绿）、警告（黄）、信息（蓝）四种状态色；如果你的主视觉刚好是蓝色或绿色，会自动把对应的提示色色相挪开（保持 ≥35° 距离），避免按钮和提示混在一起。
4. **套进固定角色并用双标准验一遍（Primer + WCAG/APCA）**：把算好的颜色全部填入 `fgColor` / `bgColor` / `borderColor` / `focus` 角色槽位，用 WCAG 2.1 和 APCA（`apca-w3`）同时算一遍对比度，确认字和底都看得清。
5. **打包输出**：生成给人看的 `dist/color-report.html` 预览报告，以及给代码和 AI 用的 CSS 变量、Tailwind 配置和 W3C DTCG JSON。

---

## 仓库里有什么

- `scripts/generate-color-system.mjs`：核心脚本，输入一个 Hex 色号生成全套产物
- `scripts/build-color-tokens.mjs` & `check-color-tokens.mjs`：编译与防写乱检查器
- `color-roles.md`：语义角色职责与使用禁忌参考表
- `SKILL.md`：给 AI Agent 读的技能说明书
- `llms.txt`：机器可读结构化摘要

---

## 不能做什么

`color-system-design` **明确不负责**：
- 不做品牌 LOGO 矢量设计或插画配色；
- 不做印刷 CMYK 色彩管理；
- 不生成脱离 WCAG / APCA 对比度底线的高饱和实验性混搭。

---

## 项目事实

| 项 | 值 |
|---|---|
| 版本 | `2.0.0` |
| 许可 | MIT |
| 运行时 | Node ≥ 18 |
| 核心标准 | GitHub Primer + Adobe Leonardo + OKLCH + W3C DTCG + APCA/WCAG 2.1 |
| 产物 | `color-report.html`、`tokens.css`、`tailwind.theme.css`、`tailwind.preset.cjs` |
| 不支持 | 品牌插画配色、CMYK 印刷 |

---

## 给 AI Agent 的速览

```text
名称：color-system-design
类型：Agent Skill + CLI
作用：输入 1 个主视觉 Hex 色号，生成明暗双模式颜色矩阵、HTML 报告及 CSS/Tailwind 变量
何时使用：用户说"生成配色方案/暗黑模式配色/Vibe Coding 配色/Tailwind 颜色变量/检查对比度"时
何时不用：品牌 Logo 艺术创作、印刷 CMYK 配色
入口：SKILL.md（与本段及 llms.txt 同义）
依赖：Node >= 18
安装：npx skills add shxuk/color-system-design
```

---

## License

[MIT](./LICENSE)
