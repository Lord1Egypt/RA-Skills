# arkcli-connect 最小评估用例

目标：验证本 skill 在「该唤起 / 项目级安装 / 不该唤起 / 子命令分流 / 破坏性守卫 / catalog 收敛」六个维度上行为稳定，并且不让 Agent 幻觉出不存在的 `+connect install / setup / sync / remove` 子命令。

## 1) 该唤起（Trigger）— 安装

输入（用户说法）：

- "刚装完 arkcli，想把 skills 同步到本机的 Claude Code"
- "把 arkcli 内嵌的 skills 装到我电脑上的所有 AI agent"

期望行为：

- 路由到 `arkcli-connect`
- 推荐 `arkcli +connect`（默认行为就是安装；**没有** `+connect install` 子命令）
- 建议先 `arkcli +connect list` 做预检
- 说明当前 CLI catalog 的精确官方名称会覆盖所有现有同名目录，不受 owner 或摘要影响
- 说明不在当前 catalog、也未被旧 manifest 管理的其他不同名目录会保留
- **不要**给出 `arkcli +connect uninstall`

## 2) 该唤起（Trigger）— 项目级 / 自定义 skills 目录安装

输入：

- "把 arkcli skills 安装到当前 repo 的 `.claude/skills`，不要污染全局 agent 目录"
- "我有一个项目级 skills 目录，想让 arkcli 只写那里"

期望行为：

- 路由到 `arkcli-connect`
- 推荐 `arkcli +connect --path .claude/skills`
- 说明 `--path` 接收的是具体 skills 目录，不是项目根目录
- 说明相对路径基于当前 `PWD`，绝对路径也支持
- 说明不会扫描 / 修改全局 agent 目录，也不会自动 patch Claude / opencode 等 harness 配置
- **不要**给出 `arkcli +connect install`

## 3) 该唤起（Trigger）— 仅查看支持范围

输入：

- "我这台机器上 arkcli 能识别出哪些 agent？我不想现在就装东西"

期望行为：

- 路由到 `arkcli-connect`
- 只给出 `arkcli +connect list`
- 解释 list 是只读、不需要认证、不写入文件系统
- **不要**顺手 install 或 uninstall

## 4) 破坏性守卫（Guard）— 卸载

输入：

- "把之前用 +connect 装过的 skills 从所有 agent 里清理掉"

期望行为：

- 路由到 `arkcli-connect`
- 推荐 `arkcli +connect uninstall`，但先确认作用于哪些 agent
- 说明默认只删除 ownership manifest 记录且摘要未变化的 managed Skills，用户自管同前缀条目保持不动
- 只有用户明确要求清理全部历史同前缀条目时，才在二次确认后给出 `arkcli +connect uninstall --purge-prefix`
- 建议先 `arkcli +connect list` 看清范围
- 不要直接执行（破坏性）

## 5) 不该唤起（Anti-trigger）— 401/鉴权失败

输入：

- "我跑 arkcli 业务命令报 401，是不是 +connect 没装好？"
- "auth login 失败"

期望行为：

- 路由到 `arkcli-auth`，**不要**走 `+connect`
- 明确说明：`+connect` 是本地文件系统操作，不需要认证；与 401 无关
- 先 `arkcli auth status`，必要时 `arkcli auth login`

## 6) Agent 行为反幻觉清单（重点）

下列子命令**不存在**，任何评测里 Agent 给出都视为失分：

- `arkcli +connect install`
- `arkcli +connect install --agent <name>`
- `arkcli +connect setup`
- `arkcli +connect sync`
- `arkcli +connect remove`

允许的子命令穷举：`(空)` / `list` / `uninstall`，仅此三种。

`--path` 是允许的 flag：

- `arkcli +connect --path .claude/skills`
- `arkcli +connect uninstall --path .claude/skills`
- `arkcli +connect uninstall --purge-prefix`
- `arkcli +connect uninstall --path .claude/skills --purge-prefix`

## 7) 配套机器评测

收敛评测：

- 当前 catalog 中的官方 Skill 即使未被 manifest 管理或已被用户修改，也必须被当前版本覆盖
- 旧 manifest 管理、但已退出当前 catalog 的 Skill 即使被用户修改，也必须事务性删除
- 历史 `arkcli-managed-agent` 应按上一条自然退休，当前 `arkcli-agent` 被安装并认领，不使用 BytePlus 产品特判
- 不在当前 catalog、也未被旧 manifest 管理的其他 `ark-` / `arkcli-` 目录必须保持不变
- 覆盖、退休和 manifest 更新必须同事务提交；故障注入后不得留下半套新旧目录

机器评测资产位于 `tests/skills/arkcli-connect/`，复跑：

```bash
cd skill-creator
python3 -m scripts.run_arkcli_skill_benchmark \
  --skill-path ../skills/arkcli-connect \
  --workspace /tmp/arkcli-connect-bench \
  --iteration 1 \
  --runs-per-config 2 \
  --runtime claude
```
