# TDD 反模式参考

> 借鉴 Superpowers 的 TDD 强制流程，列出常见的 TDD 反模式及纠正方法。

## 核心原则

**RED → GREEN → REFACTOR**

1. **RED**：先写一个失败的测试
2. **GREEN**：写最少的代码让测试通过
3. **REFACTOR**：重构代码，保持测试通过

## 反模式列表

### 1. 代码先于测试（最严重）

**症状**：
- 先写了实现代码，然后"补"测试
- 测试只是为了覆盖率，不是为了驱动设计

**危害**：
- 测试变成"确认代码正确"而非"定义代码应该做什么"
- 容易写出无法测试的代码
- 失去 TDD 的设计优势

**纠正**：
```bash
# 检测到违规
python scripts/tdd_runner.py strict --check

# 输出：
# {
#   "status": "fail",
#   "violations": [
#     {"file": "src/main.py", "reason": "新增代码无对应测试"}
#   ]
# }

# 纠正：删除代码，先写测试
rm src/main.py
# 先写 tests/test_main.py
python scripts/tdd_runner.py red tests/test_main.py  # 确认红灯
# 再写 src/main.py
python scripts/tdd_runner.py green tests/test_main.py  # 确认绿灯
```

### 2. 测试太宽泛

**症状**：
```python
def test_everything():
    # 测试了 10 个不同的功能
    assert func1() == expected1
    assert func2() == expected2
    # ...
```

**危害**：
- 一个测试失败，不知道哪个功能出问题
- 测试难以维护
- 无法精确定位回归

**纠正**：
```python
# 每个测试只验证一个行为
def test_func1_returns_expected_value():
    assert func1() == expected1

def test_func2_handles_empty_input():
    assert func2([]) == default_value
```

### 3. 测试依赖外部状态

**症状**：
```python
def test_process_data():
    # 依赖数据库中的真实数据
    data = db.query("SELECT * FROM users")
    result = process(data)
    assert result == expected
```

**危害**：
- 测试不稳定（数据库变化导致测试失败）
- 无法在 CI/CD 中运行
- 测试速度慢

**纠正**：
```python
def test_process_data():
    # 使用 mock 数据
    data = [{"id": 1, "name": "test"}]
    result = process(data)
    assert result == expected
```

### 4. 测试实现细节而非行为

**症状**：
```python
def test_internal_state():
    obj = MyClass()
    obj._internal_counter = 5  # 直接操作内部状态
    assert obj._internal_counter == 5
```

**危害**：
- 重构时测试容易失败
- 测试无法反映真实使用场景
- 鼓励暴露内部实现

**纠正**：
```python
def test_public_behavior():
    obj = MyClass()
    obj.increment()  # 通过公共接口操作
    assert obj.get_count() == 1
```

### 5. 忽略红灯

**症状**：
- 写了测试，但没有确认它失败
- 测试直接通过（可能是因为测试写错了）

**危害**：
- 无法确认测试真的在测试什么
- 可能写出"永远通过"的测试
- 失去 TDD 的反馈循环

**纠正**：
```bash
# 必须确认红灯
python scripts/tdd_runner.py red tests/test_xxx.py

# 期望输出：
# {"status": "pass", "message": "红灯 ✓ 测试按预期失败"}

# 如果测试通过了，说明测试写错了，需要修正
```

### 6. 过度重构

**症状**：
- 在 GREEN 阶段就开始重构
- 重构时改变了功能
- 重构后测试失败，但不修复

**危害**：
- 混淆了"让测试通过"和"优化代码"
- 重构引入新 bug
- 无法区分"功能变更"和"代码改进"

**纠正**：
```
RED → GREEN → (commit) → REFACTOR → (commit)

# 每个阶段独立提交
git commit -m "test: add failing test for xxx"  # RED
git commit -m "feat: implement xxx"              # GREEN
git commit -m "refactor: simplify xxx"           # REFACTOR
```

### 7. 测试覆盖率崇拜

**症状**：
- 追求 100% 覆盖率
- 为每一行代码写测试
- 测试数量远超代码数量

**危害**：
- 测试维护成本高
- 测试运行时间长
- 低价值测试（如测试 getter/setter）

**纠正**：
- 关注关键路径和边界条件
- 为行为写测试，不为实现写测试
- 接受合理的覆盖率（80-90%）

## TDD 检查清单

在每次编码前，确认：

- [ ] 我是否先写了测试？
- [ ] 测试是否失败了（红灯）？
- [ ] 我是否只写了让测试通过的最少代码？
- [ ] 测试是否通过了（绿灯）？
- [ ] 我是否在绿灯后才开始重构？
- [ ] 重构后测试是否仍然通过？

## 工具使用

```bash
# 红灯阶段
python scripts/tdd_runner.py red tests/test_xxx.py

# 绿灯阶段
python scripts/tdd_runner.py green tests/test_xxx.py

# 完整循环
python scripts/tdd_runner.py cycle tests/test_xxx.py src/xxx.py

# 强制 TDD 检查
python scripts/tdd_runner.py strict --check --src-dir src --test-dir tests
```

## 何时跳过 TDD

TDD 不是万能的，以下场景可以跳过：

1. **原型/实验代码**：快速验证想法，不需要测试
2. **简单脚本**：一次性脚本，不会复用
3. **UI 代码**：视觉验证比单元测试更重要
4. **配置变更**：纯配置修改，没有逻辑

**判断标准**：如果代码会被复用、会被其他人使用、或者包含关键业务逻辑，就应该写测试。
