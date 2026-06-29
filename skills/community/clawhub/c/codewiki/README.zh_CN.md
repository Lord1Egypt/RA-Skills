# jiangsier-skill-codewiki

> 一个对 AI Agent 友好的 Bash 工作流脚本，用于克隆 Git 仓库并通过 `codewiki`
> CLI 从中生成结构化的 Wiki。

`scripts/codewiki.sh` 是一个轻量、依赖极少的 Bash 脚本，既可以由人类直接在终端调用，
也可以被外部 AI Agent 程序化触发（参见 `SKILL.md`）。给定一个仓库地址（可选输
出目录和生成指令），它会：

1. 克隆仓库（若已存在则拉取最新代码）。
2. 在仓库目录内运行 `codewiki generate`，将生成的 Wiki 输出到
   `<output>/<repo>/wiki`。
3. *（可选）* 通过同目录下的 `scripts/render_docs.sh`，将上述 Wiki 渲染为
   **MkDocs** 和/或 **VitePress** 静态站点；并可选择性启动 HTTP 预览服务。

## 特性

- **对 Agent 友好。** 标志位可预测、`--help` 结构清晰、退出码稳定，并附带
  `SKILL.md`，便于 AI Agent 解析、确认并触发调用，无需猜测。
- **双格式仓库解析。** 既接受简写形式 `group/repo`（自动展开为
  `https://github.com/group/repo.git`），也接受完整的 `https://` 或 `git@`
  克隆地址。
- **动态指令处理。** 可选的 `-i/--instructions` 文本会原样（含空格、引号、
  Shell 元字符）转发给 `codewiki generate`，引号处理正确无误。
- **可选的渲染流水线。** `--render <mkdocs|vitepress|both>` 将生成的 Markdown
  渲染为静态站点，输出到 `<output>/<repo>/mkdocs` 和/或
  `<output>/<repo>/vitepress`；`--serve [PORT]` 可一键启动 HTTP 预览。
- **可重复执行。** 若目标目录已包含克隆，脚本会执行 `git pull --ff-only`
  而非重新克隆，保证幂等性。
- **严格的依赖检查。** 若缺失 `git` 或 `codewiki`，立即以清晰提示失败退出
  （仅在请求对应渲染栈时才检查 `python3` / `node`）。
- **默认浅克隆。** 使用 `git clone --depth 1`，克隆更快、占用更小；在仅需工
  作区代码时已足够。

## 安装与前置条件

| 依赖              | 用途                                                  | 安装方式                                                                          |
|-------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------|
| Bash ≥ 4          | 脚本运行环境（数组、`[[ ]]`）                         | macOS / Linux 系统默认                                                            |
| Git               | 克隆 / 拉取仓库                                       | https://git-scm.com/                                                              |
| `codewiki`        | 脚本调用的 Wiki 生成器                                | [FSoft-AI4Code/CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki) — 参照其 README 安装 |
| `python3` ≥ 3.9   | MkDocs 渲染器（仅在 `--render` 使用 mkdocs 或 both 时）| https://www.python.org/downloads/                                                 |
| `node` ≥18 + `npm`| VitePress 渲染器（仅在 `--render` 使用 vitepress 或 both 时）| https://nodejs.org/                                                       |

为脚本添加可执行权限：

```bash
chmod +x scripts/codewiki.sh scripts/render_docs.sh
```

（可选）将 `scripts/` 目录加入 `PATH`，即可在任意位置以 `codewiki.sh` 调用。

## 用法

### 直接在命令行调用

```bash
# 简写形式，使用默认输出目录（.）：
./scripts/codewiki.sh -r anthropics/claude-code

# 完整 HTTPS 地址 + 自定义输出目录：
./scripts/codewiki.sh -r https://github.com/foo/bar.git -o ./work/bar

# SSH 地址 + 生成指令：
./scripts/codewiki.sh -r git@github.com:foo/bar.git \
              -o ./out \
              -i "聚焦于 auth 模块；跳过 vendored 代码。"

# 生成 + 渲染两种栈，并在端口 3000 启动预览：
./scripts/codewiki.sh -r foo/bar --render both --serve 3000

# 仅渲染 MkDocs（不启动预览服务）：
./scripts/codewiki.sh -r foo/bar --render mkdocs

# 查看帮助：
./scripts/codewiki.sh -h
```

### 作为 AI Agent 技能使用

将 `SKILL.md`（以及脚本本体）拷贝到你的 Agent 技能目录中（例如
`~/.claude/skills/codewiki/`）。此后 Agent 即可响应 `/codewiki <用户输入>`：
先解析用户请求，展示结构化确认概览，**仅在用户确认后**才调用脚本。

## 配置与参数说明

| 标志 / 选项                  | 是否必填 | 说明                                                                  | 默认值 |
|------------------------------|----------|-----------------------------------------------------------------------|--------|
| `-r, --repository <repo>`    | 是       | 仓库简写 `group/repo` 或完整的 `https://` / `git@` 克隆地址。         | —      |
| `-o, --output <dir>`         | 否       | 目标目录；不存在时自动 `mkdir -p` 创建。                              | `.`    |
| `-i, --instructions <text>`  | 否       | 自由文本指令，原样传递给 `codewiki generate --instructions`。         | (无)   |
| `--render <stack>`           | 否       | 生成后调用 `render_docs.sh` 渲染静态站点；`<stack>` ∈ `mkdocs`、`vitepress`、`both`。 | (跳过) |
| `--serve [PORT]`             | 否       | 渲染完成后在本地启动 HTTP 预览。需要先指定 `--render`。默认端口 `8000`；当 `--render both` 时，MkDocs 使用 `PORT`、VitePress 使用 `PORT+1`。 | (无)   |
| `-h, --help`                 | —        | 打印帮助并退出。                                                      | —      |

## 输出目录结构

```
<output>/
└── <repo>/
    ├── (.git)              # 源仓库的浅克隆
    ├── wiki/               # codewiki 输出 —— Markdown + 元数据
    ├── mkdocs/site/        # MkDocs 静态站点（仅在 --render mkdocs|both 时生成）
    └── vitepress/site/     # VitePress 静态站点（仅在 --render vitepress|both 时生成）
```

## 退出码

| 退出码 | 含义              |
|--------|-------------------|
| 0      | 成功              |
| 1      | 用法错误          |
| 2      | 缺少依赖          |
| 3      | 克隆 / 拉取失败   |
| 4      | codewiki 执行失败 |
| 5      | 渲染失败          |

## 许可证

详见 [LICENSE](LICENSE)。
