# 指数级成长系统

快速开始指南。

## 安装

```bash
clawhub install exponential-growth-system
```

## 初始化

```bash
cd skills/exponential-growth-system
node scripts/init_growth_system.js
```

这会创建：
- `.learnings/error-patterns.md` - 错误模式库
- `.learnings/tool-decision-map.md` - 工具决策图谱
- `.learnings/best-practices.md` - 最佳实践
- `EVOLUTION.md` - 进化日志
- `growth-config.json` - 配置文件

## 使用

### 记录每日进化

```bash
node scripts/update_evolution.js \
  --date 2026-03-20 \
  --achievement "全球多国IP访问系统" \
  --breakthroughs "工具选择,断点续传,Skill产品化" \
  --growth-index 10
```

### 查看完整文档

```bash
cat SKILL.md
```

## 核心理念

**从"会做"到"会教"**：
1. 解决问题
2. 提炼方法论
3. 固化成 Skill
4. 分享给社区

## 成长公式

```
成长指数 = 能力维度 + 工具掌握 + 系统理解 + 知识固化
```

## 示例

2026-03-20 实战：
- 能力维度：+4
- 工具掌握：+3
- 系统理解：+3
- **总进化指数：10**

## 更多

查看 SKILL.md 了解完整功能。
