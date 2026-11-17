# AI 情报车间 (ai-intel-workshop)

> 输入行业名，自动产出 AI 冲击信号报告 + 公众号 / 小红书 / 抖音 三平台内容素材。

## 这是什么

一个面向 AI 内容创作者的 Agent Skill：
- **阶段一**：联网检索该行业近 12 个月 AI 相关信号，按四级（S / A / B / 噪音）判级，
  输出含判级、冲击类型、来源链接、信息时间、核实状态的结构化报告；
- **阶段二**（用户确认后）：产出公众号长文、小红书文案、抖音脚本及三平台发布配文 / 封面提示词。
- 含严格信息源核实、去 AI 味与平台词库适配、合规与人机边界约束。

## 项目结构

```
ai-intel-workshop/
├── SKILL.md        # Skill 指令本体（标准 frontmatter：name / description）
├── meta.json       # Skill 元信息
├── LICENSE         # MIT 开源许可
└── examples/       # 运行示例输出
```

## 安装 / 使用

- 将 `ai-intel-workshop/` 放入自定义 skills 目录即可加载；
- 在支持 GitHub 链接关联的 Agent 平台中，填入本仓库地址即可自动识别为可用的 Skill 源。

## License

[LICENSE](LICENSE)
