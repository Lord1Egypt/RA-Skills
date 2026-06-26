# Educlaw 多学科 Agent 测试版

## 📦 文件结构

```
educlaw-agents/
├── english/
│   └── agent.yaml        # 英语老师（免费）
├── math/
│   └── agent.yaml        # 数学老师（付费）
├── router/
│   └── config.yaml       # 路由配置
└── README.md             # 本文件
```

## 🚀 安装方式

### 方式一：复制到 OpenClaw 配置目录

```bash
cp -r educlaw-agents/* ~/.openclaw/agents/
openclaw gateway restart
```

### 方式二：通过 OpenClaw CLI 加载

```bash
openclaw agents load ./educlaw-agents/router/config.yaml
```

## 🧪 测试步骤

### 1. 测试英语（免费）

对我说：
- "学英语"
- "小英老师"

预期结果：
- 小英老师热情打招呼
- 询问学新单词还是复习

### 2. 测试数学（付费）

对我说：
- "学数学"
- "小数老师"

预期结果：
- 提示数学学科价格（99元/年）
- 引导联系微信获取全学科服务
- 输入激活码 `MATH-2024-DEMO` 后激活成功

### 3. 测试上下文隔离

1. 对英语老师说："我叫小明"
2. 切换到数学老师："学数学"
3. 问数学老师："我叫什么名字？"

预期结果：
- 数学老师不知道你的名字（上下文隔离）

## 📋 激活码（测试用）

| 学科 | 激活码 | 有效期 |
|------|--------|--------|
| 数学 | MATH-2024-DEMO | 测试用 |
| 数学 | MATH-2024-TEST | 测试用 |

## ⚠️ 已知限制

1. **语文老师**：尚未实现（status: coming_soon）
2. **积分持久化**：依赖 lossless-claw 插件
3. **授权验证**：当前为简化版，存储在对话记忆中

## 📝 配置说明

### 修改孩子信息

在对话中说：
- "我叫XXX"
- "我是X年级"

### 修改路由规则

编辑 `router/config.yaml` 中的 `rules` 部分。

### 新增学科

1. 创建新目录（如 `chinese/`）
2. 创建 `agent.yaml` 文件
3. 在 `router/config.yaml` 中添加路由规则

## 🔧 故障排除

**问题：路由不生效**
- 检查 OpenClaw 版本 ≥ 2026.2.22
- 检查配置文件语法
- 重启 Gateway

**问题：激活码无效**
- 检查激活码格式（MATH-XXXX-XXXX）
- 检查 agent.yaml 中的激活码列表

---

*版本：v0.1.0 测试版*
*作者：产品老李*
