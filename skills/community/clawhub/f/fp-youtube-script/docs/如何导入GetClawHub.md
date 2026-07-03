# 如何把这个 Skill 导入 GetClawHub

即使没接触过 AI 工具也能照着做。全程约 5 分钟。

---

## 第一步：理解三个词（30秒）

- **Skill**：给 AI 提前写好的"工作说明"。导入后选中它、输入素材，AI 就按预设格式干活。
- **System Prompt**：那份"工作说明"的正文。`skill/SKILL.md` 里 `## System Prompt` 那一段就是。
- **Frontmatter**：`SKILL.md` 顶部两条 `---` 之间的部分，是配置参数（名称、模型、温度等）。

---

## 第二步：打开文件

打开 `skill/SKILL.md`。你会看到两部分：
1. 顶部 `---` 之间：配置参数
2. 中间 `## System Prompt（整段复制到 GetClawHub）`：要粘贴的核心内容

---

## 第三步：在 GetClawHub 新建 Skill

打开 GetClawHub → 左侧找到 **Skills** → 点 **「+ New Skill」**

---

## 第四步：填写字段

对照下表填（值都在 SKILL.md 顶部 frontmatter 里）：

| GetClawHub 字段 | 填什么 | 本 Skill 的值 |
|----------------|--------|--------------|
| Skill Name | name | `fp_youtube_script` |
| Display Name | display_name | YouTube 脚本生成 |
| Description | description | （复制 description 整段） |
| System Prompt | `## System Prompt` 下全部内容 | （整段粘贴，从"你是 FridayParts..."到最后） |
| Model | model | `claude-sonnet-4-6` |
| Temperature | temperature | `0.6` |
| Max Tokens | max_tokens | `2500` |

> ⚠️ System Prompt 一定要**完整粘贴**，尤其是"技术表述准确性规范"那 5 条和"参考案例"——这是 Skill 质量的核心，漏了就会退化成普通脚本生成。

---

## 第五步：保存并测试

1. 点 **Save**
2. 在测试框输入下面这段（也是 `examples/` 里用过的）：

```
主题：水泵 vs 恒温器，判断设备过热原因
关键词：water pump, thermostat, overheating, skid steer, weep hole, impeller
产品：FridayParts Water Pump（Bobcat S650）、Thermostat Kit
特殊要求：强调安全提示，所有故障判断留有余地
```

3. 点 **Run**，对照 `examples/example_water_pump_thermostat.md` 看输出是否接近。

---

## 第六步：检查输出质量

用 `reference/人工验证checklist.md` 抽查输出。重点看：
- 有没有出现"一定/肯定/绝对/always/never"等绝对化词（应该没有）
- 故障判断有没有留余地（应该有"也要排查…"）
- 检查步骤前有没有安全提示（应该有"熄火拔钥匙"）

如果这几点都过，说明 Skill 配置成功。

---

## 之后怎么用

每次要做新视频：
1. 从 Skill 09（社区痛点分析）或选题会拿到主题
2. 准备好关键词和产品信息
3. 调用这个 Skill，输入 → 拿到脚本初稿
4. 用 checklist 抽查技术细节 → 进入拍摄

---

## 拿到运营 SOP 后

SKILL.md 的 System Prompt 里留了三个占位区：
- `[资料来源]`
- `[品牌词规范]`
- `[额外验证项]`

拿到 NotebookLM SOP 后，把里面的固定资料源、品牌词规范、额外检查标准填进对应区块，重新保存 Skill 即可，不用重写。
