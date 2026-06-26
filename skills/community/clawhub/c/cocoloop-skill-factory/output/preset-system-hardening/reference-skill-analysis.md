# Preset System Hardening - 参考分析

## 分析对象

- `codex-prd/skill-domain-landscape.md`
- `cocoloop-skill-factory/SKILL.md`
- `cocoloop-skill-factory/ref/research.md`
- `cocoloop-skill-factory/ref/design.md`
- `cocoloop-skill-factory/ref/construction.md`
- `cocoloop-skill-factory/sub-skills/brainstorm/SKILL.md`
- `cocoloop-skill-factory/sub-skills/skill-creator/SKILL.md`
- `cocoloop-skill-factory/utils/template/spec-template.yaml`

## 1. 当前主流程

### 值得保留的部分

- research、design、construction 三段式骨架已经稳定
- 分步询问规则已经明确
- 浏览器自动化等复杂方向已经有单独路线比较
- `spec.yaml` 已经进入正式协议层

### 需要补强的部分

- 还没有“任务域优先”的入口层
- 搜索仍然偏通用，没有按域搜索
- 预设资产还不存在

## 2. 当前协议层

### 值得保留的部分

- `primary_domain`、`peer_domains`、`domain_supplements`
- `coverage_status`、`open_gaps`
- `adapters`

### 需要补强的部分

- 字段责任矩阵
- 研究和设计的阻塞条件
- `output/` 契约

## 3. 当前子 Skill

### 值得保留的部分

- `brainstorm` 已经适合做按域问题包的载体
- `skill-creator` 已经强调按域组织 references

### 需要补强的部分

- `brainstorm` 需要先判任务域，再问通用问题
- `skill-creator` 需要知道预设包和任务域输出

## 汇总结论

这一轮更新不需要推翻主流程。
更合理的做法是在现有骨架上补一层前置路由和一层固定预设资产。
