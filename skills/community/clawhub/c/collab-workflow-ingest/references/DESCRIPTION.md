# 上游流程梳理产物（workflow-structurer handoff）

## Goal
将模糊的业务需求梳理为可执行的结构化流程，并把最终产物沉淀到 ClawHub 资源中心。

## Trigger Phrases
- "帮我梳理流程并存档"
- "把这个流程入库到资源中心"
- "梳理 + 入库"

## Steps
1. 目标澄清：明确要解决什么问题，什么算走通
2. 骨架提取：列出从输入到输出的大步骤
3. 逐步骤钻取：每个步骤补齐输入/输出/职责/风险/校验/规则
4. 汇总确认：用户确认所有步骤无误
5. 产物打包：按 skill 规范组织文件夹
6. 发布入库：clawhub publish 到资源中心

## Key Rules
- 每次只处理一个步骤，不跳步
- Rules 必须在 Risks 识别之后生成
- 发布前必须 dry-run

## Key Risks
- 需求不清晰就往下走 → 产物不可用
- 目录结构不符合 skill 规范 → publish 失败
- slug 命名冲突 → 发布被拒

## Validation Summary
- `ls -R` 确认目录结构完整
- `clawhub publish --dry-run` 无报错
- `clawhub search <slug>` 能搜到条目
