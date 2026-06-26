# 贡献指南 (Contributing Guidelines)

感谢您对财务报表审查工具的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题 (Reporting Issues)

如果您发现了 bug 或有功能建议，请通过 [GitHub Issues](https://github.com/yourusername/financial-statement-review/issues) 提交。

提交问题时请包含：
- 问题的详细描述
- 复现步骤
- 预期行为 vs 实际行为
- 系统环境信息（Python版本、操作系统等）
- 相关的代码片段或错误日志

### 提交代码 (Submitting Code)

1. **Fork 仓库**
   ```bash
   git clone https://github.com/yourusername/financial-statement-review.git
   cd financial-statement-review
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy
   ```

4. **编写代码**
   - 遵循 PEP 8 代码规范
   - 添加适当的注释和文档字符串
   - 为新功能编写测试

5. **运行测试**
   ```bash
   pytest tests/
   ```

6. **格式化代码**
   ```bash
   black .
   flake8 .
   ```

7. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 描述更改的内容和原因
   - 关联相关的 Issue

## 代码规范

### Python 代码规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南
- 使用 4 空格缩进
- 最大行长度 100 字符
- 使用有意义的变量名

### 文档字符串规范

```python
def function_name(param1: str, param2: int) -> bool:
    """
    简短的函数描述。
    
    详细描述函数的功能、参数和返回值。
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值的描述
        
    Raises:
        ValueError: 何时抛出此异常
        
    Example:
        >>> function_name("test", 123)
        True
    """
    pass
```

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加对金蝶云星空格式的支持

- 新增 KingdeeCloudParser 类
- 支持解析云星空特有的科目编码格式
- 添加对应的测试用例

Closes #123
```

## 开发指南

### 添加新的文件解析器

1. 在 `parsers/` 目录下创建新的解析器文件
2. 继承 `BaseParser` 基类
3. 实现 `can_parse()` 和 `parse()` 方法
4. 在 `parser_manager.py` 中注册解析器

示例：
```python
from parsers.base_parser import BaseParser, ParseResult, FinancialData

class MyParser(BaseParser):
    name = "my_parser"
    description = "我的解析器"
    supported_extensions = ['.myext']
    
    def can_parse(self, file_path: str) -> bool:
        # 实现识别逻辑
        pass
    
    def parse(self, file_path: str) -> ParseResult:
        # 实现解析逻辑
        pass
```

### 添加新的审查策略

1. 在 `strategies/` 目录下创建新的策略文件
2. 继承 `BaseStrategy` 基类
3. 实现 `execute()` 方法
4. 策略会自动被 `StrategyManager` 加载

示例：
```python
from strategies.base_strategy import BaseStrategy, StrategyResult

class MyStrategy(BaseStrategy):
    name = "my_strategy"
    description = "我的审查策略"
    applicable_tax_types = ["企业所得税"]
    
    def execute(self, data: Dict) -> StrategyResult:
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        # 实现审查逻辑
        
        return result
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_parsers.py

# 运行并生成覆盖率报告
pytest --cov=parsers --cov=strategies
```

### 编写测试

测试文件放在 `tests/` 目录下：

```python
# tests/test_my_feature.py
import pytest
from parsers.my_parser import MyParser

def test_my_parser():
    parser = MyParser()
    result = parser.parse('tests/data/sample.xlsx')
    
    assert result.success
    assert result.data.balance_sheet
```

## 文档

- 更新 README.md 以反映重要的功能变更
- 为新功能添加使用示例
- 更新 API 文档（如果有）

## 行为准则

- 保持友好和尊重的交流
- 接受建设性的批评
- 关注对社区最有利的事情
- 尊重不同的观点和经验

## 问题求助

如果您在贡献过程中遇到问题：

1. 查看现有文档和 FAQ
2. 搜索已关闭的 Issues
3. 在相关 Issue 下留言询问
4. 发送邮件到维护者

## 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下发布。

---

再次感谢您对项目的贡献！🙏
