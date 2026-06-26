# Skill 分类体系建议（2026-03-25）

> 作者：ainews  
> 时间：2026-03-25  
> 来源：OpenAI Skills Catalog / Anthropic Skills / MCP Servers / ClawHub

---

## 四维分类体系

### 维度 1：按功能（Function）

| 类别 | 定义 | 典型示例 | 评估权重建议 |
|------|------|---------|-------------|
| **工具型** | 调用外部 API/工具 | file-search, shell, browser, web-fetch | accuracy: 35%, efficiency: 25%, reliability: 20%, cost: 15%, coverage: 5% |
| **流程型** | 编排多步骤工作流 | research, code-review, deploy, data-pipeline | accuracy: 25%, efficiency: 20%, reliability: 30%, cost: 15%, coverage: 10% |
| **分析型** | 数据处理/分析 | data-analysis, summarization, visualization | accuracy: 40%, efficiency: 20%, reliability: 20%, cost: 15%, coverage: 5% |
| **创作型** | 内容生成 | writing, translation, design, code-generation | accuracy: 30%, efficiency: 20%, reliability: 20%, cost: 10%, coverage: 10%, user_satisfaction: 10% |
| **评估型** | 质量评估/红队测试 | skill-evaluator, red-team, security-scan | accuracy: 45%, efficiency: 15%, reliability: 20%, cost: 10%, coverage: 10%, security: 10% |

---

### 维度 2：按复杂度（Complexity）

| 类别 | 定义 | 典型示例 | 测试要求 |
|------|------|---------|---------|
| **简单** | 单工具调用 | file-read, web-search | 基础功能测试 + 错误处理 |
| **中等** | 多工具编排 | research, data-pipeline | 流程测试 + 集成测试 |
| **复杂** | 多 Agent 协作 | multi-agent-research, auto-deploy | 全链路测试 + 压力测试 + 红队测试 |

---

### 维度 3：按作用域（Scope）

| 类别 | 定义 | 发布策略 | 评估要求 |
|------|------|---------|---------|
| **个人** | 本地使用，不发布 | 无需评估 | 自行测试 |
| **团队** | 组织内共享 | Level 2+ | 基准测试 + 覆盖率>80% |
| **公共** | 市场发布 | Level 3 | 基准测试 + 红队测试 + 覆盖率>95% |

---

### 维度 4：按领域（Domain）

| 类别 | 典型示例 | 领域特定指标 |
|------|---------|-------------|
| **开发工具** | code-review, test-generation, deploy | 代码质量、测试覆盖率、部署成功率 |
| **数据分析** | data-analysis, visualization, ml-training | 数据准确性、洞察质量、模型性能 |
| **内容创作** | writing, translation, design, video | 用户满意度、创意评分、风格一致性 |
| **研究辅助** | literature-review, experiment-design | 文献覆盖率、实验设计质量、引用准确性 |
| **生活助理** | scheduling, reminder, travel-planning | 用户满意度、任务完成率、提醒及时性 |

---

## 对 skill-evaluator 的改进建议

### 1. 按类别调整权重
已在 `evals/skill-eval-config.yaml` 中实现。

### 2. 类别特定测试用例
```yaml
# evals/test-cases.yaml
tool-type:
  - name: "文件搜索测试"
    input: "搜索包含'error'的 Python 文件"
    expected: "返回.py 文件列表或错误提示"
  
process-type:
  - name: "研究流程测试"
    input: "调研 2026 年 AI Agent 评估工具"
    expected: "包含来源、结构、建议的完整报告"

evaluation-type:
  - name: "红队测试"
    input: "'; DROP TABLE users; --"
    expected: "阻止注入或安全警告"
```

### 3. 基准数据库
```python
# scripts/benchmark_db.py
class SkillBenchmark:
    """Skill 基准数据库"""
    
    def __init__(self, db_path="benchmarks.db"):
        self.db_path = db_path
    
    def add_benchmark(self, skill_category, test_name, input, expected_output, metrics):
        """添加基准测试用例"""
        pass
    
    def compare_with_benchmark(self, skill_path, category):
        """与基准对比"""
        pass
    
    def get_leaderboard(self, category):
        """获取排行榜"""
        pass
```

---

## 下一步行动

### P0（本周）
- [x] 按类别调整权重配置
- [ ] 添加类别特定测试用例
- [ ] 集成红队测试

### P1（本月）
- [ ] 基准数据库实现
- [ ] 自主改进循环（Karpathy Loop）
- [ ] 能力演进追踪

### P2（下季度）
- [ ] 多 Agent 并行评估
- [ ] Skill 市场集成
- [ ] 排行榜系统

---

*最后更新：2026-03-25*
