# 代码审查流程示例

## 场景1：PR自动审查

### 触发条件
当有新PR提交时自动触发

### 审查流程

```
开发者提交PR → AI审查 → 生成报告 → GitHub评论
```

### 示例输出

```markdown
## 🤖 AI代码审查报告

### 📊 变更概览
- 文件变更：5个
- 新增代码：+156行
- 删除代码：-42行
- 测试覆盖：87%

### ✅ 检查通过
- [x] 代码风格检查
- [x] 安全漏洞扫描
- [x] 单元测试
- [x] 依赖检查

### ⚠️ 改进建议

#### 1. 性能优化
**文件：** `auth/service.py:45`

**问题：** 数据库查询在循环中执行，可能导致N+1问题

**当前代码：**
```python
for user_id in user_ids:
    user = db.query(User).get(user_id)
    users.append(user)
```

**建议优化：**
```python
users = db.query(User).filter(User.id.in_(user_ids)).all()
```

**预期收益：** 减少数据库查询次数，提升10倍性能

#### 2. 错误处理
**文件：** `auth/service.py:78`

**问题：** 异常处理过于宽泛

**建议：** 细化异常类型，提供更准确的错误信息

### 🎯 总体评价
**等级：** B+（良好）

**建议：** 修复性能问题后可合并

---
*由AI代码审查助手生成*
```

---

## 场景2：代码质量分析

### 用户指令
```
分析这个项目的代码质量
```

### AI响应

```markdown
## 📊 代码质量分析报告

### 项目概览
- 项目：User Service
- 代码行数：12,456行
- 文件数：89个
- 测试覆盖率：78%

### 📈 质量指标

| 指标 | 当前值 | 目标值 | 状态 |
|------|--------|--------|------|
| 代码覆盖率 | 78% | 80% | 🟡 |
| 复杂度 | 12.5 | <15 | 🟢 |
| 重复代码 | 2.3% | <5% | 🟢 |
| 文档覆盖率 | 45% | 60% | 🔴 |
| 技术债务 | 15天 | <20天 | 🟢 |

### 🔍 问题分布

#### 🔴 高优先级（3个）
1. **核心模块缺乏单元测试**
   - 文件：`payment/service.py`
   - 覆盖率：12%
   - 风险：高

2. **硬编码配置**
   - 文件：`config/settings.py`
   - 问题：API密钥硬编码
   - 风险：极高

3. **SQL注入风险**
   - 文件：`legacy/query.py`
   - 问题：字符串拼接SQL
   - 风险：高

#### 🟡 中优先级（8个）
- 命名不规范（3个）
- 缺少错误处理（2个）
- 代码重复（3个）

#### 🟢 低优先级（12个）
- 文档缺失
- 格式问题
- 未使用导入

### 💡 改进建议

1. **立即处理**
   - 修复SQL注入漏洞
   - 移除硬编码密钥
   - 为核心模块补充测试

2. **本周完成**
   - 统一命名规范
   - 增加错误处理

3. **本月完成**
   - 提升文档覆盖率至60%
   - 重构重复代码

### 📅 技术债务趋势

```
1月：███████░░░ 18天
2月：██████░░░░ 15天
3月：█████░░░░░ 12天
```

趋势：良好，技术债务在减少

---

需要我生成具体的修复代码吗？
```

---

## 场景3：重构建议

### 用户指令
```
帮我重构这个函数
```

### AI响应

```markdown
## 🔧 重构建议

### 原始代码
```python
def process_orders(orders):
    result = []
    for order in orders:
        if order.status == "pending":
            if order.amount > 100:
                discount = order.amount * 0.1
            else:
                discount = 0
            total = order.amount - discount
            if total > 0:
                result.append({
                    "id": order.id,
                    "total": total,
                    "discount": discount
                })
    return result
```

### 问题分析

1. **嵌套过深**：4层嵌套，可读性差
2. **魔法数字**：100和0.1没有语义
3. **单一职责**：函数做了太多事情
4. **缺少类型提示**：不利于维护

### 重构后代码

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Order:
    id: str
    status: str
    amount: float

class OrderProcessor:
    DISCOUNT_THRESHOLD = 100
    DISCOUNT_RATE = 0.1
    
    def process_orders(self, orders: List[Order]) -> List[Dict]:
        """处理订单并计算折扣。"""
        pending_orders = self._filter_pending(orders)
        return [self._process_order(order) for order in pending_orders 
                if self._is_valid(order)]
    
    def _filter_pending(self, orders: List[Order]) -> List[Order]:
        """筛选待处理订单。"""
        return [o for o in orders if o.status == "pending"]
    
    def _process_order(self, order: Order) -> Dict:
        """处理单个订单。"""
        discount = self._calculate_discount(order.amount)
        return {
            "id": order.id,
            "total": order.amount - discount,
            "discount": discount
        }
    
    def _calculate_discount(self, amount: float) -> float:
        """计算折扣金额。"""
        if amount > self.DISCOUNT_THRESHOLD:
            return amount * self.DISCOUNT_RATE
        return 0
    
    def _is_valid(self, order: Order) -> bool:
        """检查订单是否有效。"""
        return order.amount > 0
```

### 改进点

1. **单一职责**：每个函数只做一件事
2. **类型安全**：添加类型提示
3. **可配置**：折扣参数提取为常量
4. **可测试**：每个小函数可独立测试
5. **可读性**：通过函数名自解释

### 测试代码

```python
def test_order_processor():
    processor = OrderProcessor()
    orders = [
        Order("1", "pending", 150),  # 有折扣
        Order("2", "pending", 50),   # 无折扣
        Order("3", "completed", 200), # 非pending
    ]
    
    result = processor.process_orders(orders)
    
    assert len(result) == 2
    assert result[0]["discount"] == 15  # 150 * 0.1
    assert result[1]["discount"] == 0
```

---

需要我应用这个重构吗？
```
