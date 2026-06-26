# 医药电话会议纪要 Skill（中文增强版）

这是一个适用于 ClawHub / OpenClaw 风格 skill 的完整文件包。

## 文件结构
- `SKILL.md`：主 skill 文件，包含 frontmatter 和完整规则
- `examples/input.md`：示例输入
- `examples/output.md`：示例输出
- `templates/call_notes_template.md`：标准纪要模板
- `templates/invocation_prompt.md`：调用提示模板

## 适用任务
- 电话会议转纪要
- 策略会 / 专家会纪要整理
- 医药、医疗服务、器械、CXO 等行业交流纪要标准化
- 录音转写后整理为内部投研纪要

## 本版新增特性
- 中文投研风格表达
- 低置信度内容必须尽量标注音频时间点
- 更强调“完整性优先于压缩”
- 更适合医药行业专有名词纠错

## 建议搭配输入
建议在调用时附带：
- 公司名 / 主题
- 时间
- 参会人
- 行业术语表
- 产品名 / 药名 / 公司名列表
- 原始带时间戳转写

如果转写没有时间戳，skill 会要求在不确定位置写明“无可用时间戳”。
