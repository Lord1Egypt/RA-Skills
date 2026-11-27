# Hermes Agent 与 Linux 运行环境

适用于 Hermes 中使用本技能创建候选工作流、修改导出 JSON、离线校验和已授权的分享接口回归。不改变六阶段流程或发布门禁。

## 安装和发现

技能是标准 `SKILL.md` 目录，Python 脚本只依赖标准库，使用 Python 3.10 或更新版本。Linux 通常调用 `python3`，Windows 调用 `python`；不必额外安装 uv、pip 包、Node 或 Docker。

默认可放在 Hermes 当前 profile 的 skills 目录；先用 `hermes skills list` 和当前运行环境确认实际目录。持久化容器可能使用挂载的数据目录，不能假定 home 下的另一份 `.hermes/skills` 就是正在使用的目录。保留稳定目录名 `fastgpt-workflow-assistant`，避免多目录下存在同名副本。

使用 `scripts/package_desktop_agents.py` 生成的 `*_Hermes_folder.zip`，解压到实际 skills 根目录或已有分类目录，其结构是：

```text
fastgpt-workflow-assistant/
  SKILL.md
  references/
  scripts/
  assets/
  agents/
```

入口只有标准 `name`/`description` frontmatter；`agents/openai.yaml` 是可忽略的 Codex 元数据，不是 Hermes 依赖。安装前审查代码，更新时把旧目录备份到 skills 根目录之外，记录来源 commit 和文件哈希；不要静默覆盖本地改动。正式包从 v2.8.0 起提供 Hermes 分发目标，源码开发快照须另记 commit，不能冒充正式 Release。

SSH 非交互 shell 可能没有继承后台 Agent 的 `HERMES_HOME`；检查时须使用已核实的同一个 home/profile，不能仅凭 SSH 默认 CLI 的列表判断安装失败。不要打印整个进程环境来查路径，以免暴露密钥。

安装后运行 `hermes skills list` 检查可发现性，再运行包内冒烟测试。如果当前会话的技能目录仍是旧快照，在新会话重新加载；不必为文件同步重启整个容器。

## 命令与工作目录

从实际发现的技能目录确定 `SKILL_DIR`，把业务输出放在独立 `WORK_DIR`，不要写回技能资产。Linux 多行命令用反斜杠，不使用 PowerShell 反引号；路径始终加引号。

```bash
# 将两个占位路径替换为本次实际目录，不能直接照抄。
SKILL_DIR='/path/to/skills/fastgpt-workflow-assistant'
WORK_DIR='/path/to/workspace/fastgpt-project'
mkdir -p "$WORK_DIR"
python3 "$SKILL_DIR/scripts/smoke_test_skill.py"
python3 "$SKILL_DIR/scripts/create_workflow_from_template.py" "$WORK_DIR/candidate.json"
python3 "$SKILL_DIR/scripts/validate_fastgpt_workflow.py" "$WORK_DIR/candidate.json" --strict
python3 "$SKILL_DIR/scripts/compare_fastgpt_roundtrip.py" "$WORK_DIR/candidate.json" "$WORK_DIR/exported.json" --json
```

最后一条只在取得真实回导文件后运行。全量 `test_skill.py` 仅在源码包存在；生产包使用 `smoke_test_skill.py`，不要把缺少开发期测试文件误报为安装损坏。

## 平台访问和凭据

离线生成和校验无需平台凭据。在线测试要先确定目标实例、测试应用及用户授权范围。容器内的 `localhost` 指向 Hermes 自身，不能据此推断 FastGPT 地址；从用户提供的地址或部署记录确认，先做不携带凭据的连通性检查。

公开技能中不保存部署地址、真实 appId/shareId、密码、Cookie 或 Token。分享标识与可选授权值通过受保护环境变量传入，保留现有 `--share-id-env`、`--app-id-env`、`--authorization-env` 参数；不要读取其他客户端的登录状态来凑凭据。

```bash
# LEAPRAG_TEST_URL 与 LEAPRAG_TEST_SHARE_ID 须事先在当前环境安全配置。
# 此命令会真实发送用例，可能消耗模型额度；仅用于已授权的测试应用。
python3 "$SKILL_DIR/scripts/run_share_api_regression.py" "$WORK_DIR/cases.json" "$WORK_DIR/results.json" \
  --url "$LEAPRAG_TEST_URL" --share-only --share-id-env LEAPRAG_TEST_SHARE_ID --gap-seconds 3
```

分享回归接口只能执行已有分享应用，不能创建、修改或导入工作流。缺少分享标识或管理入口时交付候选 JSON 和待验证项，不能把接口可达当作应用配置完成，也不能虚构管理 API。

## 无浏览器与版本兼容性

先检查当前环境实际暴露的浏览器或 API 工具，不假定存在 Codex 的浏览器工具、Windows 桌面或固定 MCP 名称。没有可用浏览器和经核实的管理 API 时，可完成候选 JSON、差异分析、用例生成和离线验证；平台导入、资源重绑、保存回读、运行回归必须标记未执行。用户提供真实导出和结果后再继续评估。

内置 `fastgpt-v481-minimal.json` 不是所有新版本的已验证模板。针对更新的 FastGPT（如 4.17），应以目标实例实际导出核实节点、边、模型稳定 ID 和绑定结构；smoke test 通过不代表通过了该版本的导入或运行测试。

服务启停属于单独的运维技能。本技能不授予主机 SSH、Docker Socket、容器管理或自动启停权限，不因分享接口失败而自行重启服务。
