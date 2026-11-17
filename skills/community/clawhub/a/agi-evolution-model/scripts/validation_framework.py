
# 日志记录
import logging
logger = logging.getLogger(__name__)
"""
参数校验框架

提供统一的参数校验接口，支持多种校验规则。

版本: 1.0.0
作者: AGI Evolution Team
"""

__version__ = '1.0.0'
__author__ = 'AGI Evolution Team'

from typing import Any, Dict, List, Optional, Callable, Union
from functools import wraps
import re
from interfaces import TraceContext, create_trace_context


class ValidationError(Exception):
    """参数校验异常"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """格式化错误消息"""
        if self.field:
            return f"字段 '{self.field}' 校验失败: {self.message}"
        return f"参数校验失败: {self.message}"


class Validator:
    """参数校验器"""
    
    @staticmethod
    def required(value: Any, field_name: str = 'value') -> Any:
        """
        校验必填字段
        
        Args:
            value: 待校验的值
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果值为空
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError('不能为空', field_name, value)
        return value
    
    @staticmethod
    def type_check(value: Any, expected_type: type, field_name: str = 'value') -> Any:
        """
        校验类型
        
        Args:
            value: 待校验的值
            expected_type: 期望的类型
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果类型不匹配
        """
        if not isinstance(value, expected_type):
            raise ValidationError(
                f'期望类型 {expected_type.__name__}，实际类型 {type(value).__name__}',
                field_name,
                value
            )
        return value
    
    @staticmethod
    def min_value(value: Union[int, float], min_val: Union[int, float], field_name: str = 'value') -> Union[int, float]:
        """
        校验最小值
        
        Args:
            value: 待校验的值
            min_val: 最小值
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果值小于最小值
        """
        if value < min_val:
            raise ValidationError(f'不能小于 {min_val}', field_name, value)
        return value
    
    @staticmethod
    def max_value(value: Union[int, float], max_val: Union[int, float], field_name: str = 'value') -> Union[int, float]:
        """
        校验最大值
        
        Args:
            value: 待校验的值
            max_val: 最大值
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果值大于最大值
        """
        if value > max_val:
            raise ValidationError(f'不能大于 {max_val}', field_name, value)
        return value
    
    @staticmethod
    def range_check(
        value: Union[int, float],
        min_val: Union[int, float],
        max_val: Union[int, float],
        field_name: str = 'value'
    ) -> Union[int, float]:
        """
        校验范围
        
        Args:
            value: 待校验的值
            min_val: 最小值
            max_val: 最大值
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果值不在范围内
        """
        if value < min_val or value > max_val:
            raise ValidationError(f'必须在 {min_val} 到 {max_val} 之间', field_name, value)
        return value
    
    @staticmethod
    def min_length(value: str, min_len: int, field_name: str = 'value') -> str:
        """
        校验最小长度
        
        Args:
            value: 待校验的值
            min_len: 最小长度
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果长度小于最小值
        """
        if len(value) < min_len:
            raise ValidationError(f'长度不能小于 {min_len}', field_name, value)
        return value
    
    @staticmethod
    def max_length(value: str, max_len: int, field_name: str = 'value') -> str:
        """
        校验最大长度
        
        Args:
            value: 待校验的值
            max_len: 最大长度
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果长度大于最大值
        """
        if len(value) > max_len:
            raise ValidationError(f'长度不能大于 {max_len}', field_name, value)
        return value
    
    @staticmethod
    def pattern(value: str, pattern: str, field_name: str = 'value') -> str:
        """
        校验正则表达式
        
        Args:
            value: 待校验的值
            pattern: 正则表达式
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果不匹配正则表达式
        """
        if not re.match(pattern, value):
            raise ValidationError(f'不匹配模式 {pattern}', field_name, value)
        return value
    
    @staticmethod
    def one_of(value: Any, choices: List[Any], field_name: str = 'value') -> Any:
        """
        校验枚举值
        
        Args:
            value: 待校验的值
            choices: 可选值列表
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果值不在可选值中
        """
        if value not in choices:
            raise ValidationError(f'必须是 {choices} 中的一个', field_name, value)
        return value
    
    @staticmethod
    def custom(value: Any, validator_func: Callable[[Any], bool], message: str, field_name: str = 'value') -> Any:
        """
        自定义校验
        
        Args:
            value: 待校验的值
            validator_func: 校验函数
            message: 错误消息
            field_name: 字段名称
        
        Returns:
            校验通过的值
        
        Raises:
            ValidationError: 如果校验失败
        """
        if not validator_func(value):
            raise ValidationError(message, field_name, value)
        return value


class SchemaValidator:
    """Schema校验器"""
    
    def __init__(self, schema: Dict[str, List[Callable]]):
        """
        初始化Schema校验器
        
        Args:
            schema: 校验规则字典，格式为 {field_name: [validator1, validator2, ...]}
        """
        self.schema = schema
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        校验数据
        
        Args:
            data: 待校验的数据
        
        Returns:
            校验通过的数据
        
        Raises:
            ValidationError: 如果校验失败
        """
        validated_data = {}
        errors = []
        
        for field_name, validators in self.schema.items():
            value = data.get(field_name)
            
            try:
                for validator in validators:
                    value = validator(value, field_name)
                validated_data[field_name] = value
            except ValidationError as e:
                errors.append(str(e))
        
        if errors:
            raise ValidationError('; '.join(errors))
        
        return validated_data


def validate_params(schema: Dict[str, List[Callable]]):
    """
    装饰器：参数校验
    
    使用示例:
        @validate_params({
            'name': [Validator.required, Validator.min_length(2)],
            'age': [Validator.required, Validator.type_check(int), Validator.range_check(0, 150)]
        })
        def create_user(name: str, age: int):
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数参数
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 校验参数
            validator = SchemaValidator(schema)
            validated_data = validator.validate(bound_args.arguments)
            
            # 调用原函数
            return func(**validated_data)
        
        return wrapper
    
    return decorator


if __name__ == '__main__':
    # 测试参数校验
    validator = Validator()
    
    # 测试必填校验
    try:
        validator.required(None, 'test_field')
    except ValidationError as e:
        print(f'✓ 必填校验: {e}')
    
    # 测试类型校验
    try:
        validator.type_check('not an int', int, 'age')
    except ValidationError as e:
        print(f'✓ 类型校验: {e}')
    
    # 测试范围校验
    try:
        validator.range_check(200, 0, 150, 'age')
    except ValidationError as e:
        print(f'✓ 范围校验: {e}')
    
    # 测试Schema校验
    schema = {
        'name': [Validator.required, Validator.min_length(2)],
        'age': [Validator.required, Validator.type_check(int), Validator.range_check(0, 150)],
        'email': [Validator.required, Validator.pattern(r'^[\w\.-]+@[\w\.-]+\.\w+$')]
    }
    
    schema_validator = SchemaValidator(schema)
    
    # 测试有效数据
    valid_data = {
        'name': 'John Doe',
        'age': 30,
        'email': 'john@example.com'
    }
    
    try:
        validated = schema_validator.validate(valid_data)
        print(f'✓ 有效数据校验通过: {validated}')
    except ValidationError as e:
        print(f'✗ 有效数据校验失败: {e}')
    
    # 测试无效数据
    invalid_data = {
        'name': 'J',
        'age': 200,
        'email': 'invalid-email'
    }
    
    try:
        validated = schema_validator.validate(invalid_data)
        print(f'✗ 无效数据校验通过: {validated}')
    except ValidationError as e:
        print(f'✓ 无效数据校验失败: {e}')
    
    print('参数校验框架测试完成')
