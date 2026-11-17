# 验收标准

## 总门槛

只有以下关键门槛全部 PASS，Agent Slim 的某次瘦身才可以交付：

| 门槛 | PASS 定义 | FAIL 处理 |
|---|---|---|
| G0 结构 | 项目骨架完整，JSON、Markdown、frontmatter 可解析 | 修复或阻断 |
| G1 收益口径 | Hot/Warm/Cold 分开，Token 与磁盘收益不混算，估算与实测有标签 | 修正报告后重验 |
| G2 能力保持 | 触发词、引用、frontmatter、常用任务回归通过 | 回滚 |
| G3 隐私 | 发布候选无私人路径、公司资料、密钥或会话正文 | 阻断发布 |
| G4 可逆性 | dry-run 差异稳定；apply 可回滚且哈希一致 | 阻断交付 |
| G5 可用性 | 新用户按 README 可在 5 分钟内理解输入、步骤和输出 | 重写 README |
| G6 职责边界 | Ponytail、Skill Architect、Memory Orchestrator 和用量事实源无重复实现 | 修正边界后重验 |

## 能力保留证据

### 1. 触发回归

准备正向触发词和易混触发词。正向必须命中预期入口；易混词不能误触发无关高危动作。结果按 `命中/未命中` 记录，不能用主观描述代替。

### 2. 引用完整性

扫描 Skill 中声明的 index、reference、template、script 和 fixture。引用目标必须存在、可读，且不越界到未声明目录。

### 3. frontmatter 可解析

至少验证：

- frontmatter 在本技能声明的受限 YAML 子集内可解析；
- `name`、`description` 存在；
- 值类型正确；
- 不允许出现无法解析的标签或重复关键字段。

完整 YAML 解析器不在 s3 范围内；缺少完整解析证据时只能记为能力边界，不能写成“完整 YAML 已验证”。

### 4. 常用任务回归

每次瘦身必须绑定一组代表性常用任务。每个任务至少记录输入、预期交付、关键字段和 PASS/FAIL。不能只跑“Skill 能加载”就宣称能力未回退。

### 5. 失败可恢复

在临时副本执行真实 apply，再触发回滚。回滚后所有目标文件哈希必须与事务前一致；无法比较哈希的对象必须提供内容等价证据。

## 发布专项验收（s5）

| 项目 | 验证方式 | 当前状态 |
|---|---|---|
| Ponytail 审查 | 每个脚本、文档、命令都有保留/删除/合并结论；核心审计、计划、隔离恢复、验证和调度能力保留 | PASS（见项目内 s5 发布报告） |
| Skill Architect | 审查 `SKILL.md` 大块章节；外移低频内容并保留路由，skill-architect 校验通过 | PASS |
| 发布元数据 | `SKILL.md`、`manifest.json`、README、CHANGELOG、LICENSE、NOTICE、`agents/openai.yaml`、双尺寸图标齐全且版本一致 | PASS |
| 跨平台 | Python 3.9+ 标准库；无私人绝对路径；无无扩展名脚本；Windows 盘符/UNC 路径被拒绝；Windows 使用 `.py` 入口 | PASS（静态测试） |
| 三平台包 | GitHub 完整包、SkillHub 轻量包、ClawHub 合规包均可解压，共享文件逐字节一致 | PASS |
| 全套测试 | `py_compile`、`unittest`、项目结构校验全部通过 | PASS |
| 隐私与内容 | skill-publisher 发布检查的隐私、涉政、身份伪装命中为 0；引用缺失为 0 | PASS |
| 包完整性 | 三个 zip 的 SHA-256 与 `SHA256SUMS.txt` 一致 | PASS |

## 布局接入验收（0.3.0）

| 项目 | 验证方式 | 结果 |
|---|---|---|
| 默认路径无回归 | 不传 `--layout` 审计 Codex Home | PASS，`host=codex`、hot 67 / warm 335 / cold 5 类，与 0.2.0 一致 |
| 布局生效 | 传 `--layout` 审计第二个 Agent | PASS，Hot 23→28 条、2,985→5,497 tok，常驻记忆与身份文件被计入 |
| 误报告警消除 | 同上 | PASS，3 条厂商专属告警降为 0，缺失改用 `HOT_FILE_MISSING` |
| 路径逃逸拒绝 | `../` 与绝对路径 | PASS，报 `LAYOUT_PATH_REJECTED`，退出码 64 |
| 下游兼容 | 用布局审计结果跑 `plan` | PASS，动作正常生成 |
| 注入测量闸门 | `measure_prompt.py --gate 57344` | `UNMEASURED`——出包环境无 `codex` 命令，按规矩不得写成 PASS |

## 当前证据

- 开发期分阶段验收记录（s1–s4）归档在项目内阶段验收文件，不随发布包分发。
- s5 的审查结论、文件清单、体积、测试命令、包哈希和回滚路径见项目内发布报告。
- 真实宿主 test-prompts 仍未提供：触发/路由回归只能记 `PARTIAL`，不得写成真实宿主 PASS。
- 未执行的目标不能写 PASS；任何失败记录必须保留，不得通过删除证据美化结果。

## 交付判定

- **PASS**：所有关键门槛 PASS，且证据可复现。
- **FAIL**：任一关键门槛失败，已修复前不得推进。
- **待确认**：证据不足，不计入 PASS，也不得用于发布声明。
