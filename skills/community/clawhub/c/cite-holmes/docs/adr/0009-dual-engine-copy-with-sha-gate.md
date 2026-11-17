# ADR-0009: 引擎双副本（mcp 嵌入式）与 sha 门禁

日期: 2026-10-29 · 状态: Accepted

## 决策

引擎 scripts/verify_refs.py 在 mcp/verify_refs.py 保持一份**逐字节一致**的
嵌入式副本（sync_engine.sh 同步+sha 校验），GitHub 仓库 tests/ 内有逐字节
相等测试锁（tests/ 不随 skill 包分发——包体最小化设计，仓库是测试真源），
发布链哨兵再兜底一道。不做单副本+动态 import 的"精简"。

## 背景

MCP 以 uvx/git 子目录独立分发（mcp/ 可单独安装），PyPI/uvx 环境无法保证
父目录布局；嵌入式副本让 mcp/ 自包含。外部结构反馈曾建议精简双副本，
但副本并非冗余：它是分发单元的一部分。

## 后果

- 任何引擎改动必须跑 `bash mcp/sync_engine.sh`（sha 门禁）；tests/ 的
  逐字节相等测试锁在提交层拦截；发布链内置两道机械闸兜底——第 ⓪ 步
  MCP sha 只读门（同步漂移即中止发布）与第 ①b 步打包后洁净复验
  （包内文件与 trunk 逐字节比对）——漂移不会带病上线
- 对用户的可见语义：mcp/ 与 scripts/ 的判定能力永远一致
- 成本：每次引擎变更多一次同步动作（sync_engine.sh 自带 sha 自检，
  测试锁与发布哨兵双闸兜底，非人工记忆依赖）
