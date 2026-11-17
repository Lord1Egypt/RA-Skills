---
doc-type: DEV-STANDARDS
layer: project
doc-class: to-be
status: draft           # draft | accepted | deprecated
owner:
---

# DEV-STANDARDS：〈项目名〉开发规范与仓库导航

> **产出者**：技术负责人/架构师——规范的签发者；例外与豁免（第 5 节）的唯一登记处
> **受众**：全部开发者/新成员 + AI 编程智能体（按第 4 节速查命令直接执行安装/启动/测试）
> **归档**：`docs/project/dev-standards.md`；本文件是导航与工作流约定，不是规范正文——正文在各规范文件，一处维护
> **真值源**：目录结构以实际仓库为准；编码规范正文以 references/standards/* 为准；CI 门禁以流水线配置文件为准；本文件只链接与导航，不复制规范正文
> **质量门禁**：① 第 4 节命令逐条可复制执行 ② monorepo 判定规则有可操作判据 ③ 每条例外含 ADR 链接与有效期 ④ 目录树与实际仓库一致

## 1. 仓库拓扑

〈填写指引：声明单仓 or monorepo 及理由；判定规则必须可操作——写出明确条件而非原则话，AI 编程智能体按规则决定新代码落位；目录树与实际仓库逐目录一致，每目录职责一句话。〉

- 拓扑：〈单仓 / monorepo——理由一句话，如"3 个应用共享领域包，monorepo 降低同步成本"〉

| 新代码落位 | 判据 | 动作 |
|---|---|---|
| 示例：packages/ | 〈被 ≥2 个应用复用且接口稳定〉 | 〈先立 ADR（`./adr/`），再创建包〉 |
| 示例：apps/<app>/ | 〈仅本应用使用〉 | 〈直接落位，无需 ADR〉 |

```
〈目录树 + 每目录职责一句话〉
apps/
  order-api/     # 〈订单服务，可独立部署〉
  admin-web/     # 〈管理后台前端〉
packages/
  db-client/     # 〈共享 DB 访问包（被 ≥2 应用复用，ADR-0005）〉
references/
  standards/     # 〈编码规范正文，不参与构建〉
```

## 2. 开发工作流

〈填写指引：写"怎么做"，不写"为什么"——选型理由链 ADR；所有约定与代码仓库/CI 实际配置一致，写了但没配置的约定等于没写。〉

- 分支模型：〈trunk-based（主干直推 + 短生命周期分支 ≤2 天合并）/ 短分支 feature flow〉
- 提交规范：〈如 Conventional Commits：`feat|fix|docs|refactor|test|chore(scope): subject`〉
- 合并纪律：〈如 squash 合并、主干禁 force-push、变更至少 1 人审查〉
- CI 门禁：〈lint + test + build 全绿才可合并〉——门禁以流水线配置文件（〈.ci/pipeline.yaml〉）为准，本节与配置不一致时修本节
- 环境约定：〈本地/预发/生产配置来源（.env / 配置中心）；密钥不入库，.env.example 仅含键名与样例值〉

## 3. 编码规范索引（按栈）

〈填写指引：本文件只链接与导航，不复制规范正文（同一信息只维护一处）；强制项摘要 ≤3 条/行，写"漏了会怎样"级别的红线项；新增技术栈先补规范文件再登记此表。〉

| 层 | 规范文件 | 强制项摘要（≤3 条） |
|---|---|---|
| 示例：后端 | 〈references/standards/backend-style.md〉 | 〈禁 any；错误统一走错误码表；service 层禁直接访问 req/res〉 |
| 示例：前端 | 〈references/standards/frontend-style.md〉 | 〈组件 ≤200 行；状态须显式声明来源；禁内联魔法数样式〉 |
| 示例：API | 〈`./api-contract.md` + references/standards/api-design.md〉 | 〈改接口先改契约后改实现；错误结构以契约全局约定为基线〉 |
| 示例：数据库 | 〈references/standards/database.md〉 | 〈迁移文件只增不改；破坏性迁移须双写过渡；索引变更附查询计划〉 |

## 4. 本地开发速查

〈填写指引：一屏可复制执行：环境要求/安装/启动/测试；命令必须真实可跑——AI 编程智能体会字面执行，错误命令比缺失更危险；环境变量给样例文件（.env.example）；执行环境差异（Node 版本管理器/系统依赖）单独注明。〉

```bash
# 环境：〈Node.js 20 LTS / pnpm 9〉
pnpm install                  # 安装全部依赖（workspace 递归）
cp .env.example .env.local    # 配置本地环境变量（必填项见 .env.example）
pnpm dev                      # 本地启动（默认 http://localhost:3000）
pnpm test                     # 全量测试
pnpm --filter order-api test  # 单包测试
pnpm build                    # 全量构建（与 CI 门禁一致）
```

〈执行环境差异：〈如 Windows 需启用符号链接支持、Node 版本切换用 nvm/fnm〉——逐条写明，不写"参考官方文档"。〉

## 5. 例外与豁免

〈填写指引：登记所有偏离规范的例外——理由 + ADR 链接 + 有效期；到期未续自动失效；无记录的偏离按违规处理，评审与 CI 按规范执行，不认口头豁免。〉

| 例外 | 理由 | ADR | 有效期 |
|---|---|---|---|
| 示例：〈legacy-auth 包暂不启用新错误码结构〉 | 〈对接遗留网关，改造排期中〉 | 〈ADR-0012〉 | 〈至 2026-06-30〉 |

〈豁免失效处理：到期未续自动失效——续期须更新有效期并重估影响；不续期则整改代码至合规后删行，并在对应 ADR 补退出记录。〉

## 红线自查（一票否决，提交前逐条勾选）

- [ ] 第 4 节命令逐条实际执行通过（在干净环境验证过）
- [ ] 目录树与实际仓库当前状态一致，无新增未登记目录
- [ ] 每条例外含 ADR 链接与有效期；过期例外已清理
- [ ] 规范正文未复制进本文件（只有链接与强制项摘要）
- [ ] monorepo 判定规则可操作（有明确判据而非原则话）
- [ ] CI 门禁描述与流水线配置文件一致

## 追踪链

| 方向 | 对象 | 说明 |
|---|---|---|
| 上游（本文消费） | 〈`./design.md` 第 5 节构建块 / ADR-NNNN / references/standards/*〉 | 拓扑与规范的输入依据 |
| 下游（消费本文） | 〈`./api-contract.md` 第 5 节全局约定（只记差异） / CI 流水线 / 全体开发者与新成员上手〉 | 被执行的规范与命令 |
