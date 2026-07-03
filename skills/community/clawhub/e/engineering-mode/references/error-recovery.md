# Error Recovery

RECOVER 阶段的错误识别与恢复流程。仅在 VERIFY 失败时加载。

## 状态锁定

进入 RECOVER 后，**状态机锁定**：
- ❌ 不创建新 checkpoint
- ❌ 不重新 DECOMPOSE
- ❌ 不切分支
- ✅ 只能：读错误 → 改代码 → 重验证

## 恢复流程

```
VERIFY 失败
    │
    ▼
1. 分析错误
   读 stdout/stderr → 识别错误类型
    │
    ▼
2. 检查改动
   git diff → 理解改了什么
    │
    ▼
3. 修复（仅一次）
   改代码 → 重 VERIFY
    │
   ┌─────┐
   │成功？│── 是 → 回到主循环
   └──┬──┘
      否
      │
      ▼
4. 回退
   切回原分支 / git reset --hard <checkpoint-hash>
   → 分析原因 → 报告用户 → 等待指示
```

## 常见错误模式

### 语法错误（L1 失败）

| 错误 | 典型信息 | 修复方法 |
|---|---|---|
| 括号不匹配 | `SyntaxError: unexpected EOF` | 检查括号配对 |
| 缩进错误 | `IndentationError` | 检查缩进一致性 |
| 未定义变量 | `NameError: name 'x' is not defined` | 检查 import / 拼写 |
| 类型错误 | `TypeError: ... is not callable` | 检查调用链 |
| 导入错误 | `ModuleNotFoundError` | 检查路径 / 包名 |

### 测试失败（L2 失败）

| 模式 | 含义 | 修复方法 |
|---|---|---|
| AssertionError | 逻辑错误，输出不符合预期 | 检查改动逻辑 |
| 新增失败 | 改动引入了 breakage | 检查对调用方的影响 |
| 超时 | 死循环或阻塞 | 检查循环条件 |

### 构建失败（L3 失败）

| 模式 | 含义 | 修复方法 |
|---|---|---|
| TypeScript 类型错误 | 类型不匹配 | 检查接口变更 |
| 链接错误 | 缺少符号 | 检查函数签名变更 |
| 循环依赖 | A→B→A | 重新设计依赖方向 |

## 回退命令

```bash
# 方案 A：回到 checkpoint（推荐）
LATEST_CHECKPOINT=$(git log --grep="^checkpoint:" -1 --format=%H)
git reset --hard $LATEST_CHECKPOINT

# 方案 B：切回原分支，丢弃临时分支
git checkout $ORIGINAL_BRANCH
git branch -D eng-mode-*
```

回退成功后报告：
```
❌ 恢复失败，已回退到 checkpoint: <hash>
失败原因：<简述>
建议：<下一步想法>
```
