# 优化师自我进化工作流

## 触发方式

### Cron 自动触发
- 每周日 03:00 执行一次（cron 任务：agent-optimizer-self-update）
- 执行环境：isolated session, agentTurn

### 手动触发
- 用户说"更新优化师的工程实践"

## 执行步骤

### Step 1: 收集最新工程实践

```bash
# Anthropic 最新实践
curl -s "http://localhost:3004/search?q=anthropic+claude+agent+engineering+tool+use+patterns+best+practices&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(f'- [{r.get(\"title\",\"\")}]({r.get(\"url\",\"\")})')
" 2>/dev/null

# OpenAI 最新实践
curl -s "http://localhost:3004/search?q=openai+agent+patterns+function+calling+structured+outputs+error+recovery&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:5]:
    print(f'- [{r.get(\"title\",\"\")}]({r.get(\"url\",\"\")})')
" 2>/dev/null

# 行业 Agent 架构趋势
curl -s "http://localhost:3004/search?q=llm+agent+architecture+patterns+self+healing+error+recovery+2026&format=json&engines=bing,duckduckgo" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', [])[:3]:
    print(f'- [{r.get(\"title\",\"\")}]({r.get(\"url\",\"\")})')
" 2>/dev/null
```

### Step 2: 对比与更新

读取搜索结果后，对比以下文件：

| 文件 | 检查内容 | 更新方式 |
|------|---------|---------|
| anthropic-patterns.md | 是否有新 Thinking/Tool Use 模式 | 追加新条目 |
| openai-patterns.md | 是否有新 Agent 模式 | 追加新条目 |
| error-taxonomy.md | 是否有新错误类型 | 新增分类 |
| fix-templates.md | 是否有新修复方法 | 新增模板 |

### Step 3: 清理过时内容

检查 references/ 中的内容：
- 标记已废弃的实践（用 `⚠️ 已废弃` 前缀）
- 保留历史版本供参考
- 不删除任何内容，只做标记

### Step 4: 更新版本号

在 SKILL.md 末尾的版本表中添加新记录：

```markdown
| v{x.y} | YYYY-MM-DD | 更新说明 |
```

## 更新规则

### 必须满足
- 只在确认有**新信息**时才更新
- 更新内容必须**可验证**（有来源链接）
- 更新后检查 SKILL.md 行数是否超过 400，超过则拆分

### 禁止
- 删除已有内容
- 替换经过验证有效的实践
- 添加未经验证的"最佳实践"

## 输出格式

更新完成后输出简要报告：

```
🔧 优化师自我进化完成

新增: X 条工程实践
- [条目1] - 来源
- [条目2] - 来源

更新: Y 条已有内容
- [条目1] - 变更说明

废弃: Z 条过时实践
- [条目1] - 废弃原因
```
