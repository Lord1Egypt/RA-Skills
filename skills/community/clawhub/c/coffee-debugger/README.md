# Coffee Debugger

开发者咖啡决策引擎 -- 一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) Skill。

根据你的工作场景（写代码、Debug、开会、写文档）、疲劳程度和当前时间，精准推荐最适合的咖啡。

## 安装

```bash
claude install github:maximum2974/coffee-debugger
```

或在 [ClawHub](https://clawhub.com/maximum2974/coffee-debugger) 上查看。

## 使用

安装后，在 Claude Code 中直接调用：

```
/coffee-debugger Debug 非常疲惫
```

也可以自然语言触发：

- "我在 debug 一个内存泄漏，好累，喝什么咖啡？"
- "下午三点了犯困，推荐个咖啡"
- "开会前需要提神"

Skill 会自动采集你的工作场景、疲劳程度和当前时间，给出一份个性化的"咖啡处方"。

## 示例输出

```
### 你的咖啡处方

**诊断：** 下午 Debug 内存泄漏，非常疲惫，需要紧急恢复战斗力
**处方：** Doppio 双份浓缩 + 少量糖
**剂量：** 标准杯，立刻饮用
**理由：** Debug 需要极致的模式识别能力，双份浓缩提供速效咖啡因冲击。
加糖补充血糖，帮助疲惫大脑更快进入状态。

> **开发者贴士：** 内存泄漏就像拿铁里的糖浆——你不知道它什么时候加进去的，但它一直在那里悄悄堆积。
```

## 支持的场景

| 场景 | 咖啡方向 |
|------|----------|
| 写代码 | 平稳释放，维持心流 |
| Debug | 强劲速效，思维清晰 |
| 开会 | 温和舒适，暖系饮品 |
| 写文档 | 轻柔提神，降低焦虑 |
| Code Review | 干净利落，消除脑雾 |
| 救火 | 最大火力 |
| 学习 | 轻盈探索型 |
| 摸鱼 | 有趣新奇，打破死循环 |

## License

MIT
