# 上下文优化器使用示例

## 快速开始

### 1. 分析工作空间
```bash
cd ~/.openclaw/workspace
python context_optimizer.py analyze
```

### 2. 执行优化
```bash
# 优化所有主要文件
python context_optimizer.py optimize all

# 优化指定文件
python context_optimizer.py optimize AGENTS.md
```

### 3. 提取Skill
```bash
# 提取会话启动流程为Skill
python context_optimizer.py extract-skill session-startup-manager session_startup
```

## 完整工作流程示例

### 示例1: 新项目初始化优化
```
1. 分析当前上下文状态
   python context_optimizer.py analyze

2. 查看优化建议
   [报告显示: AGENTS.md可优化85%, SOUL.md可提取协调者Skill]

3. 执行优化
   python context_optimizer.py optimize all

4. 提取高价值Skill
   python context_optimizer.py extract-skill intelligent-coordinator coordinator
   python context_optimizer.py extract-skill document-templates templates

5. 验证优化效果
   python context_optimizer.py analyze
```

### 示例2: 定期维护优化
```
每月执行一次:
1. 备份当前状态
2. 分析优化潜力
3. 执行保守优化
4. 生成优化报告
5. 更新Skill库
```

### 示例3: 针对性问题解决
```
问题: 系统响应变慢，上下文过大

解决步骤:
1. 分析token消耗
   python context_optimizer.py analyze
   [发现: MEMORY.md占60% token]

2. 针对性优化
   python context_optimizer.py optimize MEMORY.md

3. 提取重复模式为Skill
   python context_optimizer.py extract-skill report-templates templates

4. 验证性能改善
   [重新测试响应速度]
```

## 配置示例

### 配置文件位置
`~/.openclaw/workspace/context_optimizer_config.json`

### 配置示例
```json
{
  "optimization_strategy": "balanced",
  "target_reduction": 60,
  "preserve_format": true,
  "backup_original": true,
  "auto_approve": false,
  "skill_extraction": {
    "min_complexity": 3,
    "reuse_potential": "high",
    "template_library": true,
    "auto_test": true
  },
  "automation": {
    "schedule": "weekly",
    "report_delivery": true,
    "rollback_enabled": true
  }
}
```

### 策略说明
- **conservative**: 只移除明显冗余，保留所有内容
- **balanced**: 适度精简，平衡可读性和效率
- **aggressive**: 大幅精简，最大化token节省

## 集成到工作流程

### 与OpenClaw集成
```bash
# 创建cron任务定期优化
openclaw cron add --name "weekly-context-optimization" \
  --cron "0 2 * * 1" \
  --message "执行每周上下文优化: 分析工作空间，优化文件，提取新Skill" \
  --description "每周一凌晨2点自动优化上下文"
```

### 与Git集成
```bash
# 优化前提交
git add .
git commit -m "优化前状态"

# 执行优化
python context_optimizer.py optimize all

# 查看变化
git diff

# 提交优化
git add .
git commit -m "上下文优化: 减少token消耗60%"
```

### 与CI/CD集成
```yaml
# GitHub Actions示例
name: Context Optimization
on:
  schedule:
    - cron: '0 2 * * 1'  # 每周一凌晨2点
  push:
    branches: [ main ]

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Context Optimizer
        run: |
          python context_optimizer.py analyze
          python context_optimizer.py optimize all
      - name: Commit Changes
        run: |
          git config --local user.email "optimizer@example.com"
          git config --local user.name "Context Optimizer"
          git add .
          git commit -m "自动上下文优化" || echo "No changes to commit"
```

## 报告示例

### 分析报告
```
📊 上下文优化分析报告
============================================================
生成时间: 2026-03-27 14:45:00
工作空间: /home/user/.openclaw/workspace

## 总体统计
- 分析文件数: 7
- 原始token估算: 5,200
- 优化后token估算: 1,800
- 总体节省潜力: 65%

## 文件分析详情
### AGENTS.md
  - 大小: 8,500 字符
  - Token估算: 2,125
  - 优化分数: 85/100
  - Skill提取: 强烈建议提取为独立Skill

### SOUL.md
  - 大小: 2,800 字符  
  - Token估算: 700
  - 优化分数: 75/100
  - Skill提取: 建议提取智能协调者框架

## 优化建议
1. 优先优化: AGENTS.md (优化潜力: 85%)
2. 提取Skill: SOUL.md中的协调者框架
3. 定期维护: 每月执行一次优化
```

### 优化执行报告
```
优化执行结果
- AGENTS.md: 减少 88%
- SOUL.md: 减少 76%
- MEMORY.md: 减少 72%
- HEARTBEAT.md: 减少 65%
平均减少: 75.3%
```

## 故障排除

### 常见问题
1. **优化后功能异常**
   ```
   原因: 过度优化移除了重要内容
   解决: 使用备份文件恢复，调整优化策略为conservative
   ```

2. **Skill提取失败**
   ```
   原因: 源文件内容不适合提取为Skill
   解决: 手动创建Skill或调整提取参数
   ```

3. **性能无改善**
   ```
   原因: 上下文不是性能瓶颈
   解决: 检查其他性能因素，如网络、模型选择等
   ```

4. **配置不生效**
   ```
   原因: 配置文件格式错误或路径问题
   解决: 检查JSON格式，确认配置文件位置
   ```

### 调试模式
```bash
# 启用详细日志
export CONTEXT_OPTIMIZER_DEBUG=1
python context_optimizer.py analyze

# 查看备份文件
ls ~/.openclaw/workspace/backups/
```

## 最佳实践

### 优化时机
- **项目开始时**: 建立优化标准
- **重大变更后**: 系统架构调整后
- **性能下降时**: 响应变慢或内存占用高
- **定期维护**: 每月或每季度一次

### 安全措施
1. **始终备份**: 优化前自动备份
2. **版本控制**: 使用Git跟踪变化
3. **逐步实施**: 先优化一个文件测试效果
4. **用户确认**: 重大优化前获取确认

### 团队协作
1. **统一配置**: 团队使用相同优化策略
2. **共享Skill库**: 建立团队Skill共享目录
3. **文档化**: 记录优化决策和效果
4. **代码审查**: 优化变更纳入代码审查流程

## 扩展开发

### 添加新优化策略
```python
def custom_optimize(self, content: str) -> str:
    """自定义优化策略"""
    # 实现特定优化逻辑
    return optimized_content
```

### 添加新Skill类型
```python
def create_custom_skill(self, content: str, skill_name: str) -> str:
    """创建自定义类型Skill"""
    skill_template = f"""---
name: {skill_name}
description: 自定义技能模板
---
# 自定义内容
{content}
"""
    return skill_template
```

### 集成外部工具
```python
def integrate_with_external(self):
    """与外部工具集成"""
    # 例如: 与代码质量工具、性能监控工具集成
    pass
```