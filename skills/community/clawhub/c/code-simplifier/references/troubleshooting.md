# Code Simplifier - 故障排除

## 代码质量诊断

### 1. 代码异味 (Code Smells) 识别

#### 长函数

**症状**: 函数超过 50 行

**诊断**:
```python
import ast

def check_function_length(file_path):
    """检查函数长度"""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            lines = node.end_lineno - node.lineno
            if lines > 50:
                print(f"函数 {node.name} 过长: {lines} 行")
```

**解决方案**: 提取方法

#### 重复代码

**症状**: 相同逻辑出现多次

**诊断**:
```python
# 使用工具检测
# uv add radon
# radon cc your_file.py -a

# 或使用 pycodestyle
# uv add pycodestyle
# pycodestyle --ignore=E501 your_file.py
```

**解决方案**: 提取公共函数

#### 深层嵌套

**症状**: 嵌套层级超过 3 层

**诊断**:
```python
def check_nesting_depth(file_path):
    """检查嵌套深度"""
    with open(file_path) as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        depth = (len(line) - len(line.lstrip())) // 4
        if depth > 3:
            print(f"第 {i} 行嵌套过深: {depth} 层")
```

**解决方案**: Early Return 或提取方法

### 2. 复杂度分析

**圈复杂度**:
```bash
# 安装工具
uv add radon

# 分析复杂度
radon cc your_file.py -a

# 输出示例
# your_file.py
#   F: 4:1, process_data - A (3)
#   F: 8:1, validate_data - B (6)
```

**评分标准**:
- 1-5: 简单 (好)
- 6-10: 中等 (可接受)
- 11-20: 复杂 (需要重构)
- 21+: 非常复杂 (必须重构)

## 常见问题

### 问题 1: 魔法数字散落代码中

**症状**: 代码中充满未命名的数字

```python
# ❌ 糟糕的代码
if retry_count > 3:
    if age < 18:
        if score > 75:
```

**解决方案**:
```python
# ✅ 提取常量
MAX_RETRY_COUNT = 3
ADULT_AGE = 18
PASSING_SCORE = 75

if retry_count > MAX_RETRY_COUNT:
    if age < ADULT_AGE:
        if score > PASSING_SCORE:
```

### 问题 2: 函数参数过多

**症状**: 函数有 5+ 个参数

```python
# ❌ 参数过多
def create_user(name, email, age, address, phone, country, city):
    pass
```

**解决方案**:
```python
# ✅ 使用数据类
@dataclass
class UserProfile:
    name: str
    email: str
    age: int
    address: str
    phone: str
    country: str
    city: str

def create_user(profile: UserProfile):
    pass
```

### 问题 3: God Class (上帝类)

**症状**: 一个类做了太多事情

**诊断**:
```python
# 检查类的方法数量
def check_class_size(file_path):
    with open(file_path) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            if len(methods) > 10:
                print(f"类 {node.name} 过大: {len(methods)} 个方法")
```

**解决方案**: 拆分类 (Single Responsibility Principle)

### 问题 4: 注释 vs 自文档化代码

**症状**: 需要大量注释才能理解

```python
# ❌ 糟糕: 需要注释解释
# 检查用户是否是管理员且活跃
if user.role == 'admin' and user.status == 'active':
```

**解决方案**:
```python
# ✅ 好: 自文档化
if user.is_active_admin():
```

## 自动化工具

### 1. 代码格式化

**Black** (自动格式化):
```bash
pip install black

# 格式化代码
black your_file.py

# 检查但不修改
black --check your_file.py
```

### 2. Linting

**Pylint**:
```bash
pip install pylint

# 运行 pylint
pylint your_file.py

# 输出评分
# Your code has been rated at 8.5/10
```

**Flake8**:
```bash
pip install flake8

# 运行 flake8
flake8 your_file.py
```

### 3. 类型检查

**Mypy**:
```bash
pip install mypy

# 类型检查
mypy your_file.py

# 输出示例
# your_file.py:15: error: Argument 1 has incompatible type "str"; expected "int"
```

### 4. 代码质量评分

**CodeClimate**:
```bash
# 安装
pip install codeclimate

# 分析
codeclimate analyze
```

**SonarQube**:
```bash
# 本地运行
docker run -d --name sonarqube -p 9000:9000 sonarqube

# 扫描代码
sonar-scanner
```

## 重构工作流

### 1. 安全重构步骤

```bash
# 1. 创建分支
git checkout -b refactor/user-service

# 2. 运行测试(确保绿色)
pytest tests/

# 3. 小步重构
# - 提取函数
# - 重命名变量
# - 简化逻辑

# 4. 每步后测试
pytest tests/

# 5. 提交
git commit -m "refactor: 提取用户验证逻辑"

# 6. 重复 3-5

# 7. 最终测试
pytest tests/ -v

# 8. 合并
git checkout main
git merge refactor/user-service
```

### 2. 测试覆盖率

```bash
# 安装 coverage
pip install pytest-cov

# 运行测试并生成报告
pytest --cov=your_module tests/

# HTML 报告
pytest --cov=your_module --cov-report=html tests/
open htmlcov/index.html
```

### 3. 性能基准

```python
import timeit

def benchmark():
    """性能基准测试"""
    # 旧代码
    old_time = timeit.timeit('old_code()', globals=globals(), number=1000)

    # 新代码
    new_time = timeit.timeit('new_code()', globals=globals(), number=1000)

    print(f"旧代码: {old_time:.4f}秒")
    print(f"新代码: {new_time:.4f}秒")
    print(f"提升: {(old_time - new_time) / old_time * 100:.2f}%")
```

## 团队协作

### 1. 代码审查清单

```markdown
## 代码审查要点

### 可读性
- [ ] 变量命名清晰
- [ ] 函数职责单一
- [ ] 代码逻辑易懂

### 可维护性
- [ ] 无重复代码
- [ ] 模块化良好
- [ ] 易于扩展

### 测试
- [ ] 测试覆盖率足够
- [ ] 测试用例完整
- [ ] 边界情况已考虑

### 文档
- [ ] 有必要的注释
- [ ] API 文档完整
- [ ] 变更已记录
```

### 2. Pull Request 模板

```markdown
## 变更说明
简要描述本次变更

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成

## 检查清单
- [ ] 代码符合风格指南
- [ ] 无不必要的复杂性
- [ ] 无性能退化
- [ ] 文档已更新
```

## 持续改进

### 1. 技术债务跟踪

```markdown
## 技术债务清单

### 高优先级
- [ ] 重构 UserService 类 (100 行+ 方法)
- [ ] 移除重复的数据验证逻辑

### 中优先级
- [ ] 简化错误处理流程
- [ ] 统一异常类型

### 低优先级
- [ ] 改进变量命名
- [ ] 添加类型注解
```

### 2. 定期重构

**每周/每两周**:
```python
# 重构日: 每周五下午
# 1. 选择一个模块
# 2. 识别问题代码
# 3. 小步重构
# 4. 充分测试
# 5. 总结经验
```

### 3. 知识分享

```markdown
## 重构模式分享会

### 本周主题: Early Return 模式

**问题**:
```python
def process(data):
    if data:
        if data.valid:
            # 处理逻辑
```

**解决方案**:
```python
def process(data):
    if not data:
        return
    if not data.valid:
        return
    # 处理逻辑
```

**收益**:
- 减少嵌套
- 提高可读性
- 便于维护
```

## 参考资源

- [快速开始](quickstart.md) - 基础原则
- [最佳实践](best-practices.md) - 优化建议
- [重构模式详解](refactoring_patterns.md) - 重构模式

---

**文档版本**: 1.0.0
**最后更新**: 2024-01-20
