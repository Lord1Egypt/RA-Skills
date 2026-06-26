# 策略库开发指南

本指南帮助开发者创建自定义审查策略，扩展财务报表审查能力。

## 快速开始

### 1. 创建新策略文件

在 `strategies/` 目录下创建新的 Python 文件，如 `my_strategy.py`：

```python
from strategies import BaseStrategy, StrategyResult


class MyStrategy(BaseStrategy):
    """我的自定义策略"""
    
    # 策略元数据
    name = "my_strategy"                    # 策略唯一标识
    description = "策略描述"                 # 策略功能描述
    version = "1.0.0"                       # 版本号
    author = "作者名"                        # 作者
    applicable_tax_types = ["增值税"]         # 适用的税种列表
    required_data_fields = ["financial_statements"]  # 必需的数据字段
    
    def execute(self, data):
        """
        执行策略核心逻辑
        
        Args:
            data: 审查数据字典
            
        Returns:
            StrategyResult: 执行结果
        """
        # 创建结果对象
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'  # 初始状态为通过
        )
        
        # 获取数据
        fs = data.get('financial_statements', {})
        
        # 执行审查逻辑...
        
        # 发现问题时添加
        result.add_finding(
            finding_type='问题类型',
            description='问题描述',
            severity='medium',  # high/medium/low
            amount=100000,      # 涉及金额（可选）
            tax_type='增值税',   # 相关税种
            regulation='法规依据'  # 法规条文
        )
        
        # 添加建议
        result.add_recommendation('改进建议内容')
        
        return result
```

### 2. 使用新策略

```python
from strategies import StrategyManager

manager = StrategyManager()

# 手动注册
from my_strategy import MyStrategy
manager.register_strategy(MyStrategy)

# 或自动加载所有策略
manager.load_all_strategies()

# 执行策略
result = manager.execute_strategy('my_strategy', data)
```

## 策略基类详解

### BaseStrategy 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | str | 策略唯一标识符，必须唯一 |
| `description` | str | 策略描述，用于展示 |
| `version` | str | 版本号，如 "1.0.0" |
| `author` | str | 作者信息 |
| `applicable_tax_types` | List[str] | 适用的税种，如 ["增值税", "企业所得税"] |
| `required_data_fields` | List[str] | 必需的数据字段，执行前会验证 |
| `priority` | int | 执行优先级，数字越小优先级越高（默认50） |
| `enabled` | bool | 是否启用（默认True） |

### StrategyResult 方法

#### add_finding() - 添加发现的问题

```python
result.add_finding(
    finding_type='增值税申报收入偏低',
    description='财务收入1000万，申报收入900万，差异10%',
    severity='high',           # high/medium/low
    amount=130000,             # 涉及金额
    tax_type='增值税',          # 税种
    regulation='增值税暂行条例第十九条'  # 法规依据
)
```

#### add_recommendation() - 添加改进建议

```python
result.add_recommendation('建议及时申报未开票收入')
```

## 数据字段规范

### financial_statements（财务报表）

```python
{
    'revenue': 100000000,              # 营业收入
    'cost': 70000000,                  # 营业成本
    'profit': 10000000,                # 利润总额
    'net_profit': 7500000,             # 净利润
    'salary': 10000000,                # 工资薪金
    'welfare': 1500000,                # 职工福利费
    'education': 800000,               # 职工教育经费
    'union_fee': 200000,               # 工会经费
    'entertainment': 500000,           # 业务招待费
    'advertising': 12000000,           # 广告费和业务宣传费
    'donation': 1000000,               # 公益性捐赠
    'inventory': 20000000,             # 存货
    'accounts_receivable': 25000000,   # 应收账款
    'fixed_assets': 30000000,          # 固定资产
    'construction_in_progress': 5000000,  # 在建工程
    'operating_cash_in': 85000000,     # 销售商品收到的现金
    'operating_cash_out': 60000000,    # 购买商品支付的现金
}
```

### tax_returns（纳税申报表）

```python
{
    # 增值税
    'vat_revenue': 95000000,           # 增值税申报收入
    'vat_output': 12350000,            # 销项税额
    'vat_input': 10000000,             # 进项税额
    'vat_paid': 2350000,               # 已缴增值税
    
    # 企业所得税
    'cit_income': 100000000,           # 所得税申报收入
    'cit_cost': 70000000,              # 申报成本
    'cit_expenses': 20000000,          # 申报费用
    'cit_taxable_income': 8000000,     # 应纳税所得额
    'cit_paid': 2000000,               # 已缴企业所得税
}
```

### company_info（企业信息）

```python
{
    'name': '某某科技有限公司',
    'tax_id': '91110000XXXXXXXXXX',
    'industry': '制造业',
    'is_small_profit': False,          # 是否小型微利企业
    'is_high_tech': True,              # 是否高新技术企业
    'established_date': '2010-01-01',
}
```

### revenue_details（收入明细）

```python
{
    'monthly_revenue': [8000000, 8500000, ...],  # 月度收入分布
    'customer_concentration': {
        'top5_revenue': 50000000,      # 前五大客户收入
        'related_party_revenue': 30000000,  # 关联方收入
    },
    'completion_data': {               # 完工百分比法数据
        'estimation_method': 'cost',   # 估计方法：cost/output
        'actual_cost': 4000000,
        'estimated_total_cost': 5000000,
        'recognized_revenue': 8000000,
        'settled_revenue': 6000000,
    }
}
```

## 策略示例

### 示例1：简单比率检查策略

```python
class GrossMarginCheckStrategy(BaseStrategy):
    """毛利率异常检查策略"""
    
    name = "gross_margin_check"
    description = "检查毛利率是否异常"
    applicable_tax_types = ["企业所得税"]
    required_data_fields = ["financial_statements"]
    
    def execute(self, data):
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        revenue = fs.get('revenue', 0)
        cost = fs.get('cost', 0)
        
        if revenue > 0:
            margin = (revenue - cost) / revenue
            
            if margin < 0:
                result.add_finding(
                    finding_type='毛利率为负',
                    description=f'毛利率为{margin*100:.1f}%，主营业务亏损',
                    severity='high',
                    tax_type='企业所得税'
                )
            elif margin > 0.5:
                result.add_finding(
                    finding_type='毛利率异常高',
                    description=f'毛利率达{margin*100:.1f}%，需核实',
                    severity='medium',
                    tax_type='企业所得税'
                )
        
        return result
```

### 示例2：带配置参数的策略

```python
class InventoryTurnoverStrategy(BaseStrategy):
    """存货周转分析策略"""
    
    name = "inventory_turnover"
    description = "分析存货周转是否正常"
    applicable_tax_types = ["企业所得税"]
    required_data_fields = ["financial_statements"]
    
    def __init__(self, config=None):
        super().__init__(config)
        # 从配置读取参数
        self.warning_days = self.config.get('warning_days', 180)
        self.critical_days = self.config.get('critical_days', 365)
    
    def execute(self, data):
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        fs = data.get('financial_statements', {})
        cost = fs.get('cost', 0)
        inventory = fs.get('inventory', 0)
        
        if cost > 0 and inventory > 0:
            turnover_days = 365 / (cost / inventory)
            
            if turnover_days > self.critical_days:
                result.add_finding(
                    finding_type='存货周转严重异常',
                    description=f'存货周转天数{turnover_days:.0f}天，超过{self.critical_days}天',
                    severity='high',
                    tax_type='企业所得税'
                )
            elif turnover_days > self.warning_days:
                result.add_finding(
                    finding_type='存货周转偏慢',
                    description=f'存货周转天数{turnover_days:.0f}天',
                    severity='medium',
                    tax_type='企业所得税'
                )
        
        return result
```

使用配置参数：

```python
config = {
    'inventory_turnover': {
        'enabled': True,
        'priority': 20,
        'warning_days': 150,   # 自定义参数
        'critical_days': 300
    }
}
manager.load_all_strategies(config_map=config)
```

## 策略管理器高级用法

### 按税种过滤执行

```python
# 只执行增值税相关策略
vat_results = manager.execute_by_tax_type(data, tax_type='增值税')

# 执行时过滤
results = manager.execute_all(data, tax_type_filter='企业所得税')
```

### 策略优先级控制

```python
# 优先级数字越小越先执行
config = {
    'tax_reconciliation': {'priority': 10},    # 先执行
    'revenue_recognition': {'priority': 20},   # 后执行
    'cost_manipulation': {'priority': 30}
}
manager.load_all_strategies(config_map=config)
```

### 禁用特定策略

```python
config = {
    'tax_reconciliation': {'enabled': True},
    'revenue_recognition': {'enabled': False}  # 禁用此策略
}
manager.load_all_strategies(config_map=config)
```

## 测试策略

创建测试文件 `test_my_strategy.py`：

```python
import unittest
from my_strategy import MyStrategy


class TestMyStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MyStrategy()
    
    def test_normal_case(self):
        """测试正常情况"""
        data = {
            'financial_statements': {
                'revenue': 10000000,
                'cost': 7000000
            }
        }
        result = self.strategy.run(data)
        self.assertEqual(result.status, 'passed')
    
    def test_abnormal_case(self):
        """测试异常情况"""
        data = {
            'financial_statements': {
                'revenue': 10000000,
                'cost': 12000000  # 成本高于收入
            }
        }
        result = self.strategy.run(data)
        self.assertEqual(result.status, 'failed')
        self.assertTrue(len(result.findings) > 0)


if __name__ == '__main__':
    unittest.main()
```

## 最佳实践

1. **单一职责**：每个策略只负责一类检查
2. **可配置性**：使用 config 参数使策略可定制
3. **详细描述**：finding 的描述要具体、可理解
4. **法规依据**：尽量引用具体法规条文
5. **风险分级**：合理使用 severity 分级
6. **金额估算**：尽可能估算涉及的税款金额
7. **添加建议**：每个 finding 都应有对应的改进建议

## 提交策略

如果你开发了通用的策略，欢迎提交：

1. 确保代码符合 Python 编码规范（PEP 8）
2. 添加完整的文档字符串
3. 包含测试用例
4. 更新策略列表文档
