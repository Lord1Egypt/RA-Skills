# 🔄 Claude Code Team 模型分配说明

**版本：** v2.0.0  
**状态：** ✅ 多平台自动识别

---

## ❓ 你的问题

### 问题 1：技能名字要不要改？

**答案：** 不需要改"百炼版本"，就叫 `claude-code-team`

**原因：** 现在**自动识别平台**，不需要你指定

---

### 问题 2：我不提百炼版本，会自动分配最优模型吗？

**答案：** ✅ **会自动分配！**

**工作原理：**
```
1. 检测你当前使用的模型平台
   ↓
2. 自动选择对应平台的模型映射
   ↓
3. 为每个角色分配该平台最优模型
```

---

### 问题 3：如果用火山，不用配置也会自动分配火山最优模型吗？

**答案：** ✅ **是的！自动分配！**

**平台检测逻辑：**
```javascript
function detectPlatform() {
    const currentModel = getCurrentModel(); // 获取当前使用的模型
    
    if (currentModel.includes('bailian')) {
        return 'bailian'; // 百炼平台
    } else if (currentModel.includes('volcengine') || currentModel.includes('doubao')) {
        return 'volcengine'; // 火山引擎
    } else if (currentModel.includes('gpt') || currentModel.includes('openai')) {
        return 'openai'; // OpenAI
    } else {
        return 'bailian'; // 默认百炼
    }
}

function getModelForRole(role) {
    const platform = detectPlatform();
    return modelMapping[platform][role]; // 自动返回对应平台的最优模型
}
```

---

## 📊 多平台模型映射

### 百炼平台（阿里云）

| 角色 | 模型 |
|------|------|
| 产品经理 | `bailian/qwen-max` |
| 设计师 | `bailian/qwen-plus` |
| 程序员 | `bailian/glm-5` |
| 架构师 | `bailian/qwen-max` |

### 火山引擎（字节）

| 角色 | 模型 |
|------|------|
| 产品经理 | `volcengine/doubao-pro-32k` |
| 设计师 | `volcengine/doubao-pro-32k` |
| 程序员 | `volcengine/doubao-lite-32k` |
| 架构师 | `volcengine/doubao-pro-32k` |

### OpenAI

| 角色 | 模型 |
|------|------|
| 产品经理 | `gpt-4o` |
| 设计师 | `gpt-4o` |
| 程序员 | `gpt-4o-mini` |
| 架构师 | `gpt-4o` |

---

## 🎯 使用方式

### 场景 1：百炼平台

```
你：软件开发团队，优化这个项目
    ↓
我自动检测：当前用百炼模型
    ↓
自动分配：
- 产品经理 → bailian/qwen-max
- 设计师 → bailian/qwen-plus
- 程序员 → bailian/glm-5
```

### 场景 2：火山平台

```
你：软件开发团队，优化这个项目
    ↓
我自动检测：当前用火山模型
    ↓
自动分配：
- 产品经理 → volcengine/doubao-pro-32k
- 设计师 → volcengine/doubao-pro-32k
- 程序员 → volcengine/doubao-lite-32k
```

### 场景 3：OpenAI 平台

```
你：软件开发团队，优化这个项目
    ↓
我自动检测：当前用 OpenAI 模型
    ↓
自动分配：
- 产品经理 → gpt-4o
- 设计师 → gpt-4o
- 程序员 → gpt-4o-mini
```

---

## ✅ 总结

| 问题 | 答案 |
|------|------|
| 技能名字要改吗？ | ❌ 不需要，就叫 `claude-code-team` |
| 不提平台会自动分配吗？ | ✅ 会自动识别并分配 |
| 用火山会自动分配火山模型吗？ | ✅ 会自动分配火山最优模型 |
| 需要配置吗？ | ❌ 不需要，自动检测 |

---

## 🚀 现在可以测试

**你不需要说"百炼版本"，直接说：**

1. "软件开发团队，优化 I Ching 项目"
2. "技术中台团队，解决 Gateway 问题"

**我会自动：**
- ✅ 检测当前平台
- ✅ 分配对应平台最优模型
- ✅ 启动团队

---

*版本：2.0.0*  
*状态：✅ 多平台自动识别*