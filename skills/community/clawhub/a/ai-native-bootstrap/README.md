# ai-native-bootstrap v1.0

一次安装，多项目复用的 AI-Native SDLC 初始化 Skill。Python 3.9+、仅标准库、无需网络。**不会自动操作生产环境。**

## 1. 安装（任选一个 Agent）

在解压后的 `ai-native-bootstrap/` 目录运行：

```bash
python3 scripts/install.py --agent codex --scope user              # 预览，不写入
python3 scripts/install.py --agent codex --scope user --apply      # 安装到 ~/.agents/skills/
```

也可以使用 `--agent claude` 或 `--agent opencode`。项目级安装加 `--scope project --project /path/to/repo`。遇到旧版本请先审查，使用 `--upgrade --apply` 会保留旧版备份；已有本地修改则拒绝升级。

## 2. 接入一个项目

```bash
python3 scripts/bootstrap.py audit --project /path/to/repo
python3 scripts/bootstrap.py plan --project /path/to/repo
# 先在干净的独立分支操作，然后明确授权写入：
python3 scripts/bootstrap.py init --project /path/to/repo --adapter codex --apply
python3 scripts/bootstrap.py verify --project /path/to/repo
```

新空目录无需先初始化 Git，但强烈建议先 `git init`，并在独立分支工作。正常业务项目的修改应在独立工作分支完成；`main/master/trunk` 默认拒绝接入。没有 `--apply` 时，不会写入任何文件。

## 3. 接入后必须做的事情

1. 审核接入后生成的只读审计报告（项目内 ai-sdlc 文档目录的 audit 文件）中的真实项目事实、风险和 UNKNOWN 标记。
2. 查阅接入后生成的候选命令清单（默认全部 disabled），确认它们不会触碰生产资源，再将需要执行的 `enabled` 改为 `true`。
3. 运行接入后生成的本地检查入口 `check.py`；未启用真实检查时会返回退出码 **2**（BLOCKED），不是伪造 PASS。
4. 选取真实历史 Bug 或已验收任务，填写接入后生成的 Evals 案例文件（默认空集），再运行评估入口 `eval.py`（没有案例会退出 2，绝不伪造通过）。
5. 在已有 CI 和外部部署平台上单独确认权限/审批，完成 D05–D08 验收。

## 4. 自检

```bash
python3 scripts/validate_bundle.py
python3 -m unittest discover -s tests -v
```

## 5. 安全限制

本工具只读审计 manifest、技术栈和 Git 状态；不会读取 `.env` 值、令牌、私钥，不执行 `npm install`，不推送、合并、上线，也不创建自以为有效的生产门禁。目录存在、脚本可执行和测试框架存在，都**不等于**生产项目完成质量验收。

完整实施标准见 `references/implementation-standard.md`，平台差异见 `references/adapters-and-safety.md`。安装后，可在 Agent 中说“使用 ai-native-bootstrap 初始化当前项目”。

## 6. 接入产物的能力边界

- `audit` / `plan` 无写入；`init --apply` 只生成工程规范和本地验证入口。
- 未发现可信的项目测试命令时，检查入口为 `BLOCKED`，不是 PASS。
- Evals 默认空集，不制造“历史真实案例”。
- 不自动配置 CI、生产授权或运行模型 API；这些需要在实际项目内经审查接入。
- 跨 Agent 适配提供官方技能安装路径与项目规则桥接，不保证某个工具已自动加载；须新开 Agent 会话验证。

## 7. 验收与可复现打包

- `ACCEPTANCE.md`：已运行的离线测试范围、证据和未验证项。
- `python3 scripts/package.py /path/to/ai-native-bootstrap-v1.0.zip`：仅打包审查过的文件，不包括缓存、凭证或无关资料。
- 已有接入仓库如需增量升级：先将上次接入变更提交到干净的功能分支，再执行 `bootstrap.py init --project <REPO> --adapter all --upgrade --apply`。旧规则发生漂移时会拒绝自动升级，需人工审查。
