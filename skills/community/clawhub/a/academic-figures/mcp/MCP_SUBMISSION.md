# SkillHub MCP 广场提报文本（备妥待提交；随 cite-holmes-mcp 结果同步动作）

> 字段结构照抄现网 schema（cite-holmes 工单核实）。署名 SorSor（uid 437178）。
> 提交通道：平台官方问卷（cite-holmes 同通道）。**提交时机：cite-holmes-mcp 收录/反馈落地后**。

- slug: `academic-figures-mcp`
- name: 学术图表 MCP（Academic Figures）
- publisher: SorSor（SkillHub 发布者，academic-figures 等技能作者）
- homepage: https://github.com/docsor1212/academic-figures/tree/main/mcp
- sourceUrl: https://github.com/docsor1212/academic-figures
- summary: 通过 MCP Server 用一条指令渲染 41 种投稿级学术图表（bar/line/KM 生存曲线含竞争风险/森林图/ROC/slope 斜率图/composite 多面板/PRISMA 2020 等），内置数据校验、渲染看门狗、像素级重叠门禁与中文诊断；本地确定性渲染（同输入同字节）、零密钥零遥测；支持 9 种期刊预设与色盲安全配色。适配论文写作、投稿出图、科研数据可视化场景。
- category: 学术科研（或"开发者工具"，按平台分类）
- 安装提示词：`安装 academic-figures-mcp：uvx --from "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp" academic-figures-mcp`

## 提交前置检查单（提交时逐项勾）

- [ ] cite-holmes-mcp 已收录或已有官方反馈（学习后再提）
- [ ] GitHub main 分支含 mcp/（v4.3.0 发布携带）+ tag mcp-v1.0.0 已推
- [ ] `uvx --from "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp" academic-figures-mcp --help` 干净环境跑通（发布后复验）
- [ ] e2e_transcript.md 为最新提交形态（tools/resources/prompts 全通过）
