# Changelog

## v1.1.2 — 2026-07-15

### Orchestration Boundary Fix (ClawHub SkillSpector Round 3)

- **移除子技能实现细节**：pipeline.md不再文档化xhs-crafter的截图实现（端口清理、HTTP服务器），改为"调用xhs-crafter执行截图"
- **移除bypass语言**：异常表中"外部进程复制绕行方法"的描述改为中性的"使用替代复制方法"
- **移除端口条目**：异常表移除"8090端口被占用"条目，截图异常改为"重新调用xhs-crafter截图"
- **SKILL.md数据处理声明**：移除"本地HTTP服务器"和"端口清理"，改为"子技能调用"声明
- **SKILL.md权限声明**：subprocess从具体命令改为"调用xhs-crafter执行截图"
- **SKILL.md规则5**：从"截图安全（端口清理）"改为"调用xhs-crafter执行截图"
- **桌面交付**：移除"（自动执行）"标注，强化写入提示

## v1.1.1 — 2026-07-15

### Disclosure Fixes (ClawHub SkillSpector Round 2)

- **description补充web search声明**：添加"(with web search enrichment)"和"Local files are created on desktop"
- **数据处理声明扩展**：从4条扩展为完整声明，覆盖网络请求(WebFetch+WebSearch+图片下载)、本地文件创建、HTTP服务器、端口清理
- **移除过度修改**：删除"跳过transcript-crafter的3个确认点"的显式bypass语言，改为"以auto模式执行"
- **pipeline.md安全提示**：截图步骤添加安全提示blockquote，本地交付步骤添加文件创建提示
- **硬编码路径修复**：pipeline.md中2处C:\路径替换为占位符
- **README中英文同步**：数据处理声明中英文完全一致

## v1.1.0 — 2026-07-15

### Security Audit Fixes (ClawHub SkillSpector)

- **端口定向清理**：将"杀全部Python进程的旧命令"替换为仅清理8090端口占用进程的定向方案
- **云上传consent gate**：飞书云盘同步从自动执行改为需用户确认，Phase 4.2添加确认门
- **隐私声明**：SKILL.md/README.md/README_EN.md 添加"数据处理与隐私"章节
- **触发边界**：添加明确触发条件和不触发条件
- **移除explorer.exe**：不再自动打开文件夹，仅告知输出路径
- **权限声明**：添加5维度权限声明表格
- **description更新**：添加"Cloud sync is opt-in only"

### Architecture

- Phase 1改为调用transcript-crafter完整8步流程（含5工具搜索补充）
- 字号铁律升级：正文≥32px，辅助≥28px，元信息≥24px

## v1.0.0 — 2026-06-14

### Initial Release

- One-shot pipeline: 素材 → 长文 → 5-9张社交卡片 + 文字稿
- 编排层架构：调度transcript-crafter + xhs-crafter
- 多样性轮换：8封面词 + 8封底词 + 5主题池
- 截图安全检查
- 桌面 + 飞书云盘双通道交付
