---
name: "Coordinator+Worker测试场景"
description: "多Agent协作协议的测试场景和验证方法"
type: "project"
created: "2026-04-18"
updated: "2026-04-18"
---

# Coordinator+Worker协议测试场景

## 测试目标
1. 验证精确指令协议的清晰度和可执行性
2. 测试协作工作流程的完整性和效率
3. 验证并行执行策略的正确性
4. 评估错误处理和恢复机制
5. 收集用户体验和改进反馈

## 测试环境
- **Coordinator**: main Agent
- **Workers**: development Agent（用于技术任务）、product Agent（用于产品任务）
- **通信方式**: sessions_send（跨会话消息）
- **工作区**: 独立临时工作区，避免污染主工作区
- **监控**: 审计日志记录所有交互

## 测试场景

### 场景1：代码审查任务（基础测试）

#### 测试描述
用户要求检查项目中的安全漏洞，Coordinator需要将任务分解为精确指令，分配给development Agent执行。

#### 测试步骤
1. **用户需求**: "检查`/src/auth/`目录中的身份验证逻辑安全漏洞"
2. **Coordinator分析**:
   - 分析需求，确定需要检查的文件
   - 将任务分解为具体的检查点
   - 生成精确指令
3. **Worker执行**: development Agent接收指令并执行代码审查
4. **结果返回**: Worker返回审查结果
5. **Coordinator汇总**: 整合结果，生成最终报告

#### 精确指令示例
```
任务：检查`/src/auth/authentication.ts`中的身份验证逻辑安全漏洞

具体要求：
1. 检查第45-80行的`validatePassword`函数，寻找可能的SQL注入或XSS漏洞
2. 检查第120-150行的`createSession`函数，寻找会话固定或CSRF漏洞
3. 检查第200-230行的`rateLimit`函数，寻找拒绝服务攻击漏洞
4. 检查第250-280行的`resetPassword`函数，寻找逻辑漏洞

文件位置：
- 主文件：/src/auth/authentication.ts (第45-280行)
- 测试文件：/tests/auth/authentication.test.ts (第1-100行)

预期输出：
- 漏洞报告：列出发现的安全问题，每个问题包含位置、描述、风险等级（高/中/低）
- 修复建议：针对每个漏洞提供具体的修复代码示例
- 验证方法：运行现有测试确保修复不破坏现有功能

时间限制：预计2小时内完成
```

#### 预期结果
- ✅ Worker能够理解指令并执行审查
- ✅ 返回结构化的漏洞报告
- ✅ 修复建议具体可执行
- ✅ 总执行时间在预期范围内

### 场景2：产品需求分析（跨部门协作）

#### 测试描述
用户要求分析新功能需求，需要Coordinator协调product和development两个Agent协作完成。

#### 测试步骤
1. **用户需求**: "分析用户反馈，设计并评估'导出数据到Excel'功能"
2. **Coordinator分解**:
   - 将任务分解为产品分析和实现评估两个子任务
   - 分别分配给product和development Agent
   - 设置任务依赖关系（产品设计完成后进行评估）
3. **并行执行**:
   - product Agent分析用户需求，设计功能规格
   - development Agent评估技术实现难度
4. **结果整合**: Coordinator汇总两个Agent的结果，生成完整方案

#### 精确指令示例

**给product Agent的指令**:
```
任务：设计'导出数据到Excel'功能的产品规格

具体要求：
1. 分析用户反馈中关于数据导出的需求（见`/feedback/data-export-requests.md`）
2. 设计功能规格：支持的数据格式、导出选项、用户界面
3. 创建用户流程图：从触发导出到完成下载的完整流程
4. 定义成功指标：导出成功率、用户满意度提升目标

文件位置：
- 用户反馈：/feedback/data-export-requests.md (第1-50行)
- 产品规格模板：/templates/product-spec.md (第1-30行)

预期输出：
- 产品规格文档：/docs/features/data-export-spec.md
- 用户流程图：/docs/features/data-export-flow.png (或Mermaid图表)
- 成功指标定义：/docs/features/data-export-metrics.md

时间限制：预计3小时内完成
```

**给development Agent的指令**:
```
任务：评估'导出数据到Excel'功能的技术实现难度

具体要求：
1. 分析现有数据模型：`/src/models/`目录下的相关模型
2. 评估技术方案：使用现有库（如ExcelJS）还是自定义实现
3. 估算开发工作量：前端和后端的工作量估算
4. 识别技术风险：性能影响、内存使用、兼容性问题

文件位置：
- 数据模型：/src/models/data.js (第1-100行)
- 现有导出功能：/src/utils/export.js (第1-80行)

预期输出：
- 技术评估报告：/docs/tech/data-export-assessment.md
- 工作量估算：按组件分解的工作量（人日）
- 风险清单：技术风险和缓解方案

时间限制：预计2小时内完成
```

#### 预期结果
- ✅ 两个Agent能够并行执行各自任务
- ✅ 结果具有互补性，能够整合为完整方案
- ✅ 任务依赖关系正确处理（评估依赖设计）
- ✅ 跨部门协作流程顺畅

### 场景3：错误处理和恢复测试

#### 测试描述
模拟Worker执行失败的情况，测试Coordinator的错误处理机制。

#### 测试步骤
1. **正常任务分配**: Coordinator分配一个无法完成的任务给Worker
2. **Worker失败**: Worker报告无法完成任务，说明原因
3. **错误处理**: Coordinator分析失败原因，采取恢复措施
4. **任务重分配**: 调整任务或分配给其他Worker
5. **降级方案**: 如果完全无法完成，提供降级方案

#### 错误场景示例
- **场景A**: 文件不存在或权限不足
- **场景B**: 技术依赖缺失或版本不兼容
- **场景C**: 任务要求超出Agent能力范围
- **场景D**: 超时或资源限制

#### 预期结果
- ✅ Worker能够正确识别和报告失败原因
- ✅ Coordinator能够分析失败原因并制定恢复策略
- ✅ 任务能够重新分配或降级处理
- ✅ 用户能够获得合理的解释和替代方案

## 测试验证指标

### 质量指标
1. **指令清晰度**: Worker是否能够正确理解指令（通过执行结果评估）
2. **执行准确性**: 结果是否符合预期要求
3. **时间效率**: 实际执行时间 vs 预计时间
4. **资源使用**: CPU、内存、网络使用情况
5. **错误处理**: 错误识别和恢复的成功率

### 用户体验指标
1. **响应时间**: 从用户需求到首次响应的延迟
2. **结果质量**: 最终输出的完整性和可用性
3. **透明度**: 进度可视化和状态更新的及时性
4. **易用性**: 用户与多Agent系统交互的便捷性

## 测试实施计划

### 阶段1：单元测试（1天）
- 测试精确指令生成器
- 测试任务分类逻辑
- 测试并行规则验证
- 测试错误处理机制

### 阶段2：集成测试（2天）
- 测试Coordinator与单个Worker的完整流程
- 测试跨多个Worker的协作
- 测试飞书消息路由集成
- 测试审计日志记录

### 阶段3：系统测试（2天）
- 测试完整的多任务场景
- 测试高并发情况下的性能
- 测试长时间运行的稳定性
- 测试错误恢复的可靠性

### 阶段4：用户验收测试（1天）
- 真实用户任务测试
- 收集用户反馈
- 优化协议和流程
- 准备生产部署

## 测试工具和脚本

### 1. 指令验证工具
```python
# scripts/validate_instruction.py
def validate_instruction(instruction):
    """验证精确指令的完整性"""
    required_fields = ['task', 'requirements', 'file_locations', 'expected_output']
    for field in required_fields:
        if field not in instruction:
            return False, f"Missing required field: {field}"
    
    # 验证文件路径存在
    for file_info in instruction['file_locations']:
        if not os.path.exists(file_info['path']):
            return False, f"File not found: {file_info['path']}"
    
    return True, "Instruction is valid"
```

### 2. 任务执行模拟器
```python
# scripts/simulate_worker.py
class WorkerSimulator:
    def __init__(self, worker_type):
        self.worker_type = worker_type
    
    def execute_instruction(self, instruction):
        """模拟Worker执行指令"""
        # 验证指令
        is_valid, message = validate_instruction(instruction)
        if not is_valid:
            return {
                'status': 'failed',
                'reason': f"Invalid instruction: {message}"
            }
        
        # 模拟执行
        execution_time = self.estimate_execution_time(instruction)
        time.sleep(min(execution_time, 5))  # 模拟执行，最多5秒
        
        # 生成模拟结果
        result = self.generate_simulated_result(instruction)
        
        return {
            'status': 'completed',
            'result': result,
            'execution_time': execution_time
        }
```

### 3. 性能监控脚本
```python
# scripts/monitor_performance.py
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'response_time': [],
            'task_completion_time': [],
            'error_rate': [],
            'resource_usage': []
        }
    
    def record_metric(self, metric_name, value):
        """记录性能指标"""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
    
    def generate_report(self):
        """生成性能报告"""
        report = {}
        for metric_name, values in self.metrics.items():
            if values:
                report[metric_name] = {
                    'count': len(values),
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                }
        return report
```

## 测试数据准备

### 测试项目结构
```
/test-projects/
├── auth-module/
│   ├── src/
│   │   └── auth/
│   │       └── authentication.ts
│   └── tests/
│       └── auth/
│           └── authentication.test.ts
├── feedback-data/
│   └── data-export-requests.md
└── templates/
    └── product-spec.md
```

### 测试文件内容
- **authentication.ts**: 包含需要审查的代码（故意留一些安全漏洞）
- **authentication.test.ts**: 现有测试文件
- **data-export-requests.md**: 模拟用户反馈数据
- **product-spec.md**: 产品规格模板

## 成功标准

### 技术成功标准
1. **指令执行成功率**: ≥95%
2. **任务完成时间**: 90%任务在预计时间内完成
3. **错误恢复成功率**: ≥90%
4. **系统可用性**: ≥99.9%（测试期间）

### 业务成功标准
1. **用户满意度**: 用户对协作结果满意
2. **效率提升**: 相比单Agent执行，效率提升≥50%
3. **质量提升**: 输出质量提升≥30%
4. **可扩展性**: 支持扩展到更多Agent类型

## 下一步行动

### 立即行动
1. 创建测试项目结构和文件
2. 开发指令验证工具
3. 配置测试环境（独立工作区）
4. 开始单元测试

### 短期行动
1. 运行集成测试
2. 收集性能数据
3. 优化协议设计
4. 准备用户验收测试

### 长期行动
1. 扩展到更多Agent类型
2. 实现自动化测试流水线
3. 集成到生产环境
4. 持续监控和优化

---
**测试计划状态**: 草案v1.0  
**创建时间**: 2026-04-18  
**维护责任**: main Agent  
**更新频率**: 根据测试结果定期更新