# content-deai-engine

去 AI 味内容引擎 —— 为小红书、X、知乎等平台生成"有人味、可传播、可追溯"的内容。

## 触发场景

- 用户要求"去 AI 味""重写成更像人写的""太像 AI 了"
- 需要把草稿改写为平台适配版本
- 需要发布前质量门禁检查

## 核心能力

1. **AI 味诊断**：识别三段式模板、机械连接词、空泛大词
2. **四步重写**：去模板 → 加细节 → 立观点 → 给动作
3. **平台适配**：小红书/X/知乎结构化模板
4. **发布前门禁**：8 项检查清单，不满足先修稿

## 文件结构

```
content-deai-engine/
├── SKILL.md                          # 主技能文件
├── references/
│   ├── anti-ai-patterns.md           # AI 味模式识别与替换建议
│   ├── platform-templates.md         # 小红书/X/知乎模板
│   └── preflight-checklist.md        # 发布前检查清单
```

## 使用示例

当用户说"把这段去 AI 味"：
1. 先用 `anti-ai-patterns.md` 诊断
2. 按"四步重写法"改写
3. 用 `platform-templates.md` 适配目标平台
4. 用 `preflight-checklist.md` 做发布前检查

## 安装

```bash
clawhub install content-deai-engine
```

## 许可证

MIT