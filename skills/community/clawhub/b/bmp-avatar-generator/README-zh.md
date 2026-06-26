[English](README.md) · [中文](README-zh.md)

# Avatar Generator Skill

一个 skill，根据任意 seed 字符串生成确定性的像素风格 SVG 头像。底层调用 [`@bitmappunks/avatar-generator`](https://www.npmjs.com/package/@bitmappunks/avatar-generator)，版本锁定在 `0.0.5`，通过 `npx` 运行，无需全局安装。

> 同一个 seed 永远生成同一个头像。

## 概览

本 skill 适用于 Claude Code、OpenClaw、Hermes Agent 以及其他读取 `SKILL.md` 形式 skill 的 LLM agent 系统。纯文件配置，不绑定任何平台。

## 安装

**下面的安装示例以 Claude Code 为例。实际使用时，你完全可以把仓库 URL 直接交给你的 agent，让它自己处理安装——就这么简单。**

### 方式 1：直接 clone

克隆到 agent 的 skills 目录：

```bash
cd ~/.claude/skills
git clone https://github.com/bitmappunks-com/avatar-generator-skill.git avatar-generator
```

使用其他 agent 时，替换为对应的 skills 目录即可（比如 OpenClaw 是 `~/.openclaw/workspace/skills`）。

### 方式 2：ClawHub（可用时）

```bash
clawhub install bmp-avatar-generator
```

### 可选：启用 `/gen-avatar` 斜杠命令

仓库里自带一个斜杠命令 `commands/gen-avatar.md`。把它软链（或拷贝）到 agent 的 commands 目录，就能直接用 `/gen-avatar <seed> [output-path]`：

```bash
# Claude Code
ln -s ~/.claude/skills/avatar-generator/commands/gen-avatar.md ~/.claude/commands/gen-avatar.md
```

其他 agent 换成对应的 commands 目录即可。配好后 `/gen-avatar alice ./alice.svg` 一条命令直接出图，不需要再写自然语言。

skill 通过 `npx` 按需运行 `@bitmappunks/avatar-generator@0.0.5`；首次调用会把它下载进 npx 缓存，之后的调用直接复用缓存。

## 使用

安装后，当你要求根据 seed 生成头像时，agent 会自动触发这个 skill：

- "给 `alice` 生成一个头像，存到 `./alice.svg`"
- "make an avatar for `user-42` at `/tmp/u42.svg`"
- "生成头像 seed=`hello`"

agent 最终会执行：

```bash
npx -y @bitmappunks/avatar-generator@0.0.5 --out "<path>" --seed "<seed>"
```

如果没有提供 seed，agent 应默认使用当前 Unix 时间戳（秒）作为 seed，这样每次都会不一样，同时仍然能记录本次实际使用的 seed。

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `seed` | 选填 | 任意字符串。同一 seed → 同一头像。如果未提供，默认使用当前 Unix 时间戳（秒），这样每次生成都不同，但仍可复现本次结果。 |
| `output path` | 必填 | `.svg` 的绝对或相对路径。如果传目录，skill 会自动拼接 `<seed>.svg`。 |

## 输出

- 24×24 像素风 SVG。
- 如需 PNG 或调整尺寸，请另外转换（`rsvg-convert`、`sharp`、ImageMagick 等）——本 skill 不做格式转换。

## 版本锁定

本 skill 把 `@bitmappunks/avatar-generator` 锁定在 `0.0.5`。这是刻意设计：头像输出必须跨时间、跨机器保持可复现。升级底层包可能改变视觉算法，让之前生成的头像无法被重新得到。

没有和使用方沟通清楚之前，不要改动这个锁定版本。

## 依赖

- Node.js（任意近期 LTS）
- `npx`（随 npm 一起安装）

终端预览用 skill 自带的 `svg-tui.js`——不需要额外装依赖，任何支持 24 位色的终端都能直接渲染。

## 许可

MIT —— 见 [LICENSE](LICENSE)。

## 作者

BitmapPunks · [bitmappunks-com/avatar-generator-skill](https://github.com/bitmappunks-com/avatar-generator-skill)
