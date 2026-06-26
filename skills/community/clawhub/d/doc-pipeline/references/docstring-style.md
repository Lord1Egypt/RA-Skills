# Docstring 格式规范（Google 风格）
## 标准格式
```python
def function_name(param1: type1, param2: type2) -> return_type:
    """[简要描述函数功能]

    Args:
        param1 (type1): [参数1的详细描述]
        param2 (type2): [参数2的详细描述]

    Returns:
        return_type: [返回值的详细描述]

    Examples:
        >>> function_name(1, "test")
        [预期输出结果]

    Raises:
        [异常类型]: [触发该异常的条件]
    """
def simple_func(param: int) -> str:
    """[一句话描述功能]

    Args:
        param: [参数描述]

    Returns:
        [返回值描述]
    """