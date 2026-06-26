# ALAPI Skill

ALAPI 官方 skill，用于帮助 AI 或开发者更高效地完成 ALAPI 接口搜索、文档理解、参数提取、代码生成和按需真实调用。

这个 skill 主要解决这些问题：

- 搜索 ALAPI 接口
- 读取 ALAPI OpenAPI 和文档页
- 提取参数、返回结构和调用约定
- 生成可直接使用的对接代码
- 在用户明确允许且 token 可用时执行真实调用

适合的典型场景包括：

- 想快速找到某个能力对应的 ALAPI 接口
- 已有文档链接，想直接生成接入代码
- 需要区分已确认参数和文档未明确说明的字段
- 需要在不泄露 token 的前提下测试真实接口

## 仓库地址

- GitHub: `https://github.com/ALAPI-SDK/skill`

## 安装方式

可以直接通过 `npx skills add` 安装：

```bash
npx skills add https://github.com/ALAPI-SDK/skill
```

安装完成后，可按你的 skills 管理方式启用或保留这个 skill。
## 文件结构

- `SKILL.md`: skill 主说明，面向 AI 的执行规则
- `agents/openai.yaml`: UI 元数据
- `scripts/alapi.py`: 零依赖 CLI，负责搜索、读文档、读 OpenAPI、真实调用
- `references/code-examples.md`: 多语言接入模板
- `tests/test_alapi.py`: 最小回归测试
- `evals/evals.json`: 评测集

## 这个 Skill 解决什么问题

ALAPI 接入请求经常会重复几件事：

- 找接口
- 看参数
- 确认返回结构
- 写接入代码
- 必要时做一次真实调用

这个 skill 的作用，就是把这些步骤收敛成一套更稳定、可复用的流程，避免 AI 每次都从零猜测。

## 行为约定

这是一个 **ALAPI 专用 skill**，不是通用 API skill。

默认优先执行只读操作：

- `search`
- `explore`
- `detail`
- `openapi`

只有在下面两个条件同时满足时，才执行真实 `call`：

1. 用户明确要求真实调用或测试接口
2. 已提供可用 token

token 优先级：

- 显式 `--token` 最高优先级
- 否则读取环境变量 `ALAPI_TOKEN`

最终回复中不应回显用户的真实 token。

## CLI 用法

不要假设当前工作目录就是仓库根目录。应先基于 skill 目录定位脚本：

```bash
SKILL_DIR=/absolute/path/to/alapi
SCRIPT="$SKILL_DIR/scripts/alapi.py"
python3 "$SCRIPT" --help
```

示例：

```bash
python3 "$SCRIPT" --json search "IP查询"
python3 "$SCRIPT" --json openapi 27
python3 "$SCRIPT" --json call ip --token "$ALAPI_TOKEN" --param ip=8.8.8.8
ALAPI_TOKEN=your_token python3 "$SCRIPT" --json call ip --param ip=8.8.8.8
```

## 真实使用示例

- `帮我查一下 IP: 8.8.8.8`
- `帮我生成视频解析的代码`
- `这个关键词搜不到，帮我换几个更合理的 ALAPI 搜索词`
- `如果视频解析有多个候选接口，先别直接写代码，先帮我确认选哪个`

## 机器可读输出

当输出会被另一个 agent 消费，或需要串联下一步时，优先使用 `--json`。

支持的命令：

- `search <keyword>`
- `explore`
- `detail <id>`
- `openapi <id>`
- `call <path> --token <token> [--param key=value] [--method GET|POST]`

## 验证

运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 /Users/anhao/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## 说明

- 当前 README 默认以 skill 仓库根目录为基准说明命令和文件结构
- 如果你把它移动到别的仓库或 skill 目录，内部相对结构最好保持不变
- 不要在自动化流程里写死旧的仓库相对路径
