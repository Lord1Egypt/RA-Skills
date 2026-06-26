---
name: execute-verify-report
description: Execute-Verify-Report 三步法工具 — 强制AI遵循"执行→验证→报告"流程，杜绝"说做了其实没做"、"完成了但不验证"等问题。基于STANDING-ORDERS核心原则设计。
---

# Execute-Verify-Report (EVR) - 三步法工具 ✅

> 执行不是确认，验证不是可选，报告不是敷衍

## 问题背景

AI Agent常见错误：
- ❌ "我会做的" ≠ 做了
- ❌ "完成了"但没有验证
- ❌ 无限重试同一失败操作
- ❌ 静默失败不报告

**Execute-Verify-Report 三步法从根源解决。**

## 核心原则

| 步骤 | 含义 | 反例 | 正例 |
|------|------|------|------|
| **Execute** | 实际执行 | "我会去做的" | "已执行：`date` 输出 13:17:23" |
| **Verify** | 验证结果 | "应该成功了" | "验证：文件存在，大小2.3KB" |
| **Report** | 完整汇报 | "搞定了" | "执行→验证→结果→下一步" |

## 使用方法

### 方式1：汇报模板（强制）

```markdown
**任务**: [任务描述]

🔧 **Execute**
```bash
[实际执行的命令]
```
输出: [粘贴实际输出]

✅ **Verify**
- 验证方法: [如何验证]
- 验证结果: ✅通过 / ❌失败
- 失败原因: [如果失败]

📋 **Report**
- 结果: [一句话总结]
- 数据: [具体数字/状态]
- 下一步: [下一步行动]
```

### 方式2：脚本辅助

```bash
# 开始任务
evr start "修复安全漏洞"

# 执行步骤
evr step "修改配置文件权限"
# 自动提示: 请运行验证命令

# 验证步骤
evr verify "chmod 600 ~/.openclaw/openclaw.json"
# 自动检查: 文件权限是否为600？

# 结束任务
evr done
# 生成完整EVR报告
```

## 失败处理

### 重试规则

```javascript
// 最多重试3次
for (let attempt = 1; attempt <= 3; attempt++) {
  const result = execute(command);
  
  if (verify(result)) {
    report("✅ 成功", result);
    break;
  }
  
  if (attempt === 3) {
    report("❌ 连续3次失败，停止重试", result);
    escalate("需要人工干预");
  }
}
```

### 静默失败检测

```bash
# 错误示例（静默失败）
rm important-file.txt  # 如果文件不存在，命令返回0但无事发生

# EVR正确做法
if [ -f important-file.txt ]; then
  rm important-file.txt
  # 验证: 文件是否确实被删除
  if [ ! -f important-file.txt ]; then
    echo "✅ 验证通过: 文件已删除"
  else
    echo "❌ 验证失败: 文件仍存在"
  fi
else
  echo "⚠️ 文件不存在，无需删除"
fi
```

## 案例分析

### 案例1：文件删除

**❌ 错误方式**:
```
用户: 删除文件
AI: 好的，我会删除的。 [然后没做]
```

**✅ EVR正确方式**:
```
🔧 Execute
$ rm /path/to/file.txt
[无输出，命令成功]

✅ Verify
$ ls -la /path/to/file.txt
ls: cannot access '/path/to/file.txt': No such file or directory
验证结果: ✅ 文件确实已删除

📋 Report
- 结果: 文件删除成功
- 数据: 删除了1个文件
- 验证: 文件不存在确认
- 下一步: 进行下一个任务
```

### 案例2：Git提交

**❌ 错误方式**:
```
用户: 提交更改
AI: 好的，已提交。 [实际有未提交文件]
```

**✅ EVR正确方式**:
```
🔧 Execute
$ git add -A
$ git commit -m "fix: 修复安全问题"
[master a1b2c3d] fix: 修复安全问题
 2 files changed, 15 insertions(+)

✅ Verify
$ git status
On branch master
nothing to commit, working tree clean
$ git log --oneline -1
a1b2c3d fix: 修复安全问题
验证结果: ✅ 提交成功，工作区干净

📋 Report
- 结果: Git提交成功
- 数据: 2个文件，15行改动
- 提交: a1b2c3d
- 验证: working tree clean
- 下一步: 推送到远程
```

## 集成到AGENTS.md

```markdown
## Execute-Verify-Report (EVR) 铁律

**所有任务必须遵循：**

1. **Execute** — 实际执行，不只是确认
   - 必须看到命令输出
   - 必须等待命令完成
   - 必须捕获返回码

2. **Verify** — 验证结果正确
   - 文件操作: 检查文件存在/内容/权限
   - 网络操作: 检查响应状态码
   - 系统操作: 检查进程/服务状态
   - 数据操作: 检查数据准确性

3. **Report** — 汇报做了什么和验证结果
   - 不要只说"完成了"
   - 要说"完成了什么，如何验证的"
   - 包含具体数据

**禁止：**
- ❌ "我会做的" ≠ 做了
- ❌ "完成了"但没有验证
- ❌ 最多重试3次，之后必须停止
- ❌ 静默失败

**违反EVR = 严重错误，立即纠正**
```

## 最佳实践

### 验证方法速查

| 操作类型 | 验证命令 | 通过标准 |
|---------|---------|---------|
| 文件创建 | `ls -la file` | 文件存在 |
| 文件删除 | `ls file 2>&1` | 文件不存在 |
| 文件修改 | `cat file` / `md5sum` | 内容/哈希匹配 |
| 权限修改 | `stat -c "%a" file` | 权限值正确 |
| Git提交 | `git status` / `git log` | 干净/提交存在 |
| 网络请求 | `curl -I url` | HTTP 200 |
| 服务启动 | `systemctl status svc` | active (running) |
| 进程运行 | `pgrep process` | 返回PID |

### 报告模板

```markdown
✅ [任务名] 完成

**执行**: [命令]
**验证**: [方法] → [结果]
**数据**: [具体数字]
**下一步**: [行动]
```

## License

MIT

---

*Created by 小白* 🤍  
*基于 STANDING-ORDERS 核心原则*  
*"执行不是确认，验证不是可选，报告不是敷衍"*
