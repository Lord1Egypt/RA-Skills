# 追平契约与恢复协议

本文件是契约生命周期、机械状态和恢复规则的单一事实来源。

## 目录

- [生命周期](#生命周期)
- [Frontmatter schema](#frontmatter-schema)
- [命令](#命令)
- [写前协议](#写前协议)
- [恢复来源](#恢复来源)
- [敏感信息](#敏感信息)
- [继续、阻塞与恢复](#继续阻塞与恢复)
- [正常关闭](#正常关闭)

## 生命周期

每个权威根同时只允许一份 `RECONCILIATION.md`：

```text
评估（无文件）
  → 用户确认
  → executing
  → paused ↔ executing（同一轮次分段推进）
  → blocked ↔ executing
  → restoring → restored → 复验恢复证据 → ready_to_close
  → 或 executing → 复验完成证据 → ready_to_close
  → close 重新核验并删除契约
```

文件存在表示轮次未结束；不存在表示没有活动轮次。不得归档已完成契约，也不得保留 `completed` 状态。

## Frontmatter schema

固定字段：

| 字段 | 含义 |
|---|---|
| `schema_version` | 契约结构版本，当前为整数 `1`；新增关闭字段向后兼容读取和恢复 |
| `round_id` | 本轮唯一标识 |
| `status` | `executing`、`paused`、`blocked`、`restoring`、`restored`、`ready_to_close` |
| `authority_root` | 权威根绝对路径 |
| `target_stage` | 本次执行上限：`requirements`、`design`、`tasks`、`implementation`、`validation` |
| `completion_stage` | 整轮闭环终点，不浅于执行上限；缺失或 `null` 时允许读取和恢复，但禁止正常关闭 |
| `created_at` | 契约创建时间 |
| `confirmed_at` | 用户执行确认时间 |
| `version_control` | `git` 或 `none` |
| `baseline_ref` | `init` 时解析并冻结的不可变 Git commit SHA；无 Git 时为 `null` |

正文必须保留模板中的全部章节。机器日志位于固定标记之间，人工编辑不得改变标记、JSON 结构或日志项。

## 命令

从已安装 Skill 的目录运行：

```bash
python3 scripts/contract.py init <authority-root> \
  --target-stage <stage> \
  --completion-stage <stage> \
  --version-control <git|none> \
  [--baseline-ref <ref>] \
  --writable-root <root>

python3 scripts/contract.py prepare <contract> --path <file> \
  [--recovery-mode <embed|git>] \
  [--allow-sensitive] [--allow-large]

python3 scripts/contract.py applied <contract> --path <file>
python3 scripts/contract.py status <contract> [--set <executing|paused|blocked|restoring>]
python3 scripts/contract.py scope <contract> --target-stage <stage> \
  [--completion-stage <stage>] [--writable-root <root>] --confirmation <用户确认原文或定位>
python3 scripts/contract.py restore <contract>
python3 scripts/contract.py verify <contract>
python3 scripts/contract.py verify <contract> --mark-ready --evidence <closing-evidence.json>
python3 scripts/contract.py close <contract>
```

`--allow-sensitive`、`--allow-large` 和 `recovery-mode=git` 只能反映契约中已经记录的用户选择，命令行开关本身不构成授权。

`scope` 只记录已有确认，不产生授权。它保留 `round_id`、基线和全部恢复日志；暂停的契约还需显式恢复 `executing`。闭环终点不能降低；新可写根重新确认后用可重复的 `--writable-root` 追加，不能移除有恢复日志的原根。

## 写前协议

对每次文件修改、创建或删除执行：

1. `prepare` 校验路径位于已确认可写根内。
2. `prepare` 检测符号链接、敏感候选和载荷大小。
3. `prepare` 先把原始哈希、模式和恢复来源写入契约。
4. 修改目标文件。
5. `applied` 重新检测修改后内容，再记录新哈希、模式和反向差异。
6. `verify` 检查当前文件与日志链一致。

同一文件可多次变更，每次生成独立日志项。恢复前必须先校验全部日志结构，并将每个目标重新解析到已确认可写根内；任一路径非法时，不得开始文件恢复。恢复时按日志逆序执行，任何外部漂移都会把契约置为 `blocked`。

恢复是可重试的：若进程已把某个文件恢复到精确前态、但尚未来得及持久化该日志项的 `restored` 状态，下一次 `restore` 将把该文件识别为已恢复并继续，而不是误报外部漂移。

脚本只处理常规文件，不跟随符号链接，不递归快照目录。目录结构调整必须拆成可逆的文件创建与删除，并在删除清单中明确列出。

## 恢复来源

默认 `embed`：把原始字节 gzip 压缩后 Base64 编码存入契约，能够在无 Git 时精确恢复。Base64 不是加密。

选择 `git` 时，`init` 先把用户提供的引用解析为不可变 commit SHA；日志只保存仓库、该 SHA 和相对路径。`prepare` 还会证明当前字节与冻结基线完全一致。工作树内容与基线不一致时必须使用 `embed`，不能用 Git 对象覆盖真实前态。即使 `HEAD`、分支或标签随后移动，恢复来源也不会改变。

估算后的嵌入载荷超过 10 MiB 时暂停，让用户选择：

- 明确确认后使用 `--allow-large` 嵌入。
- 在内容与 Git 引用一致时改用 `--recovery-mode git`。
- 缩小本轮范围。

## 敏感信息

契约权限始终为 `0600`。脚本只输出敏感信号名称和路径，不输出命中值；敏感日志的可读差异被省略，但精确恢复载荷仍可能含秘密。

检测到敏感候选时默认停止。用户逐文件确认本地载荷风险后，才可使用 `--allow-sensitive`。若敏感信号首次出现在修改后内容中，`applied` 会省略差异、保存哈希并把契约置为 `blocked`，等待用户确认。用户拒绝时，将该文件移出可写范围并由用户处理或恢复本次修改。

`init` 会核对声明的 `version_control` 与权威根实际状态。有 Git 时，`verify` 检测契约是否进入索引；被跟踪或暂存即阻塞。Skill 不自动修改 `.gitignore`、`.git/info/exclude`、索引或提交历史。

## 继续、阻塞与恢复

继续未完成轮次前运行 `status` 和 `verify`，阅读契约中的变更断言、进度和阻塞。只有解决阻塞或重新确认边界后，才把状态从 `blocked` 改回 `executing`。

阶段性暂停、交接或等待下一次授权时，将状态设为 `paused`，记录完成水位、剩余工作和下次所需授权。保留契约，不运行恢复，不创建替代轮次。

只有用户明确要求撤销本轮修改时：

1. 运行 `restore`，让脚本逆序恢复。
2. 运行 `verify`，确认日志链与前态一致。
3. 重新运行基线验证，检查活跃引用没有停在中间状态。
4. 确认契约没有尚未恢复的独有要求。
5. 提供 `outcome=restored` 的关闭证据，运行 `verify --mark-ready --evidence` 和 `close`。

`restore` 完成后状态为 `restored`，仅代表文件已恢复；它不能证明验证基线和引用已经复验。

漂移、缺失 Git 对象、损坏载荷或基线验证失败都保持阻塞，不得通过删除契约绕过。

## 正常关闭

`verify` 的 `valid` 仅表示 schema、日志链、文件哈希、权限和 Git 状态一致。正常关闭要求执行上限已达到闭环终点、状态为 `executing`、独立关闭证据属于同一轮次且没有剩余工作。`blocked` 必须先解决阻塞；`paused` 不能关闭。Skill 逐项证明：

- 断言已吸收。
- 闭环终点及全部上游阶段门槛通过，必要检查没有 NotRun 或未解释失败。
- 零未解释残留。
- 水位已更新。
- 契约未被 Git 跟踪。
- 契约没有独有有效要求。

按 [closure-evidence.md](closure-evidence.md) 提供证据后运行 `verify --mark-ready --evidence`。脚本登记契约指纹和证据哈希；`close` 重新检查当前文件、契约和证据后才删除契约。两个命令分开执行，任一失败都保留契约，不用 `rm`、`unlink` 或补丁绕过。状态查询不是关闭许可。

旧契约缺少 `completion_stage` 时，依据原始确认用 `scope` 补齐，不猜测、更不删除重建。旧版 `ready_to_close` 没有证据登记时不能关闭：尚未恢复的轮次先转回 `executing`，补齐终点和证据；需要恢复的轮次转为 `restoring` 后继续 `restore`。保留旧恢复日志。

脚本检查结构、证据存在性和漂移，不能证明自然语言结论真实，也不能阻止绕过脚本直接删除文件。Agent 仍须阅读逐项证据，完成整个闭环复核。
