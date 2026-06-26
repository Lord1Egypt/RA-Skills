# 事实核查钩子（Fact-Check Hook）

## 概述

自动检测AI输出中的可疑内容，触发验证流程。

## 钩子类型

### 1. 日期时间钩子

```python
# 触发条件
date_patterns = [
    r'\d{4}-\d{2}-\d{2}',  # 2024-01-01
    r'\d{4}年\d{1,2}月\d{1,2}日',  # 2024年1月1日
    r'今天|昨天|明天|上周|下周|本月',  # 相对日期
]

# 验证动作
def verify_date(date_str):
    # 1. 获取系统时钟
    import datetime
    now = datetime.datetime.now()
    
    # 2. 比对日期
    # 3. 返回验证结果
    return {
        "verified": True/False,
        "actual_date": now.strftime("%Y-%m-%d"),
        "confidence": "确定/不确定"
    }
```

### 2. 数字统计钩子

```python
# 触发条件
number_patterns = [
    r'\d+%',  # 百分比
    r'\d+\.\d+',  # 小数
    r'总计|平均|统计|数量|金额',  # 统计词汇
]

# 验证动作
def verify_number(number, context):
    # 1. 从源文件读取
    # 2. 用脚本计算
    # 3. 交叉验证
    return {
        "verified": True/False,
        "source": "文件名/命令输出",
        "confidence": "确定/推断/不确定"
    }
```

### 3. 代码API钩子

```python
# 触发条件
code_patterns = [
    r'import\s+\w+',  # import语句
    r'\w+\.\w+\(',  # 方法调用
    r'function\s+\w+',  # 函数定义
]

# 验证动作
def verify_code(code_snippet):
    # 1. grep搜索确认存在
    # 2. websearch搜索官方文档
    # 3. 跑一下验证能用
    return {
        "verified": True/False,
        "source": "文件路径/官方文档URL",
        "confidence": "确定/不确定"
    }
```

### 4. 文件路径钩子

```python
# 触发条件
path_patterns = [
    r'[A-Za-z]:\\',  # Windows路径
    r'/',  # Unix路径
    r'\.\./',  # 相对路径
]

# 验证动作
def verify_path(path):
    # 1. ls或Test-Path验证存在
    # 2. 返回验证结果
    return {
        "verified": True/False,
        "actual_path": "实际路径",
        "confidence": "确定/不确定"
    }
```

### 5. 引用来源钩子

```python
# 触发条件
reference_patterns = [
    r'https?://',  # URL
    r'论文|文献|研究报告',  # 学术引用
    r'标准|规范|法规',  # 法规引用
]

# 验证动作
def verify_reference(reference):
    # 1. 搜索确认存在
    # 2. 访问URL验证可访问
    # 3. 返回验证结果
    return {
        "verified": True/False,
        "accessible": True/False,
        "confidence": "确定/不确定"
    }
```

## 钩子执行流程

```
1. 检测输出内容
2. 匹配触发模式
3. 执行验证动作
4. 返回验证结果
5. 根据结果处理：
   - 验证通过 → 继续
   - 验证失败 → 标注 [需验证]
   - 无法验证 → 标注 [不确定]
```

## 钩子配置

```yaml
hooks:
  fact-check:
    enabled: true
    auto_trigger: true
    confidence_threshold: 0.8
    actions:
      on_verified: "continue"
      on_failed: "annotate"
      on_uncertain: "ask_user"
```
