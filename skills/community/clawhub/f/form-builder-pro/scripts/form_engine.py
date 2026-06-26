"""
Form Engine - 表单引擎
支持JSON Schema验证、动态渲染、条件逻辑的表单处理引擎
"""

import json
import re
import yaml
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from jsonschema import validate, ValidationError as JSONSchemaError
from jinja2 import Template


@dataclass
class Field:
    """
    表单字段定义
    """
    name: str
    type: str = "text"  # text, email, number, select, checkbox, etc.
    label: str = ""
    required: bool = False
    default: Any = None
    options: List[Dict] = field(default_factory=list)
    validation: Dict = field(default_factory=dict)
    conditional: Optional[Dict] = None  # 条件显示规则
    help_text: str = ""
    placeholder: str = ""
    order: int = 0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "label": self.label,
            "required": self.required,
            "default": self.default,
            "options": self.options,
            "validation": self.validation,
            "conditional": self.conditional,
            "help_text": self.help_text,
            "placeholder": self.placeholder,
            "order": self.order
        }


class Form:
    """
    表单类 - 包含字段定义和验证逻辑
    """
    
    def __init__(self, name: str = "", description: str = ""):
        self.name = name
        self.description = description
        self.fields: List[Field] = []
        self._field_map: Dict[str, Field] = {}
        self.custom_validators: Dict[str, Callable] = {}
        self.json_schema: Optional[Dict] = None
    
    def add_field(self, field: Field) -> "Form":
        """添加字段"""
        self.fields.append(field)
        self._field_map[field.name] = field
        # 按order排序
        self.fields.sort(key=lambda f: f.order)
        return self
    
    def remove_field(self, name: str) -> "Form":
        """移除字段"""
        if name in self._field_map:
            self.fields = [f for f in self.fields if f.name != name]
            del self._field_map[name]
        return self
    
    def get_field(self, name: str) -> Optional[Field]:
        """获取字段定义"""
        return self._field_map.get(name)
    
    def to_json_schema(self) -> Dict:
        """转换为JSON Schema格式"""
        properties = {}
        required_fields = []
        
        for field in self.fields:
            prop = self._field_to_schema_property(field)
            properties[field.name] = prop
            
            if field.required:
                required_fields.append(field.name)
        
        schema = {
            "type": "object",
            "properties": properties,
            "title": self.name,
            "description": self.description
        }
        
        if required_fields:
            schema["required"] = required_fields
        
        self.json_schema = schema
        return schema
    
    def _field_to_schema_property(self, field: Field) -> Dict:
        """将字段转换为JSON Schema属性"""
        prop = {
            "type": self._map_type_to_schema(field.type),
            "title": field.label or field.name
        }
        
        if field.help_text:
            prop["description"] = field.help_text
        
        if field.default is not None:
            prop["default"] = field.default
        
        # 添加验证规则
        if "pattern" in field.validation:
            prop["pattern"] = field.validation["pattern"]
        
        if "minLength" in field.validation:
            prop["minLength"] = field.validation["minLength"]
        
        if "maxLength" in field.validation:
            prop["maxLength"] = field.validation["maxLength"]
        
        if "minimum" in field.validation:
            prop["minimum"] = field.validation["minimum"]
        
        if "maximum" in field.validation:
            prop["maximum"] = field.validation["maximum"]
        
        if field.type == "select" and field.options:
            prop["enum"] = [opt.get("value") for opt in field.options]
        
        return prop
    
    def _map_type_to_schema(self, field_type: str) -> str:
        """映射字段类型到JSON Schema类型"""
        type_mapping = {
            "text": "string",
            "email": "string",
            "password": "string",
            "textarea": "string",
            "number": "number",
            "integer": "integer",
            "boolean": "boolean",
            "date": "string",
            "datetime": "string",
            "select": "string",
            "multiselect": "array",
            "checkbox": "boolean",
            "checkboxes": "array",
            "radio": "string",
            "file": "string",
            "array": "array",
            "object": "object"
        }
        return type_mapping.get(field_type, "string")
    
    def validate(self, data: Dict) -> Dict[str, Any]:
        """
        验证表单数据
        
        Returns:
            {
                "valid": bool,
                "errors": List[str],
                "data": Dict (清洗后的数据)
            }
        """
        schema = self.to_json_schema()
        errors = []
        
        # 检查条件字段
        visible_fields = self._get_visible_fields(data)
        
        # 过滤不可见字段
        data_to_validate = {
            k: v for k, v in data.items() 
            if k in visible_fields
        }
        
        # JSON Schema验证
        try:
            validate(instance=data_to_validate, schema=schema)
        except JSONSchemaError as e:
            errors.append(f"{e.path[0]}: {e.message}" if e.path else e.message)
        
        # 自定义验证
        for field_name, validator in self.custom_validators.items():
            if field_name in data:
                try:
                    result = validator(data[field_name], data)
                    if result is not True:
                        errors.append(f"{field_name}: {result}")
                except Exception as e:
                    errors.append(f"{field_name}: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "data": data_to_validate
        }
    
    def _get_visible_fields(self, data: Dict) -> set:
        """获取在给定数据下可见的字段"""
        visible = set()
        
        for field in self.fields:
            if field.conditional is None:
                visible.add(field.name)
            else:
                # 评估条件
                if self._evaluate_condition(field.conditional, data):
                    visible.add(field.name)
        
        return visible
    
    def _evaluate_condition(self, condition: Dict, data: Dict) -> bool:
        """评估条件规则"""
        operator = condition.get("operator", "equals")
        field = condition.get("field")
        value = condition.get("value")
        
        if field not in data:
            return False
        
        field_value = data[field]
        
        if operator == "equals":
            return field_value == value
        elif operator == "not_equals":
            return field_value != value
        elif operator == "contains":
            return value in field_value if isinstance(field_value, (str, list)) else False
        elif operator == "in":
            return field_value in value if isinstance(value, list) else False
        elif operator == "gt":
            return field_value > value
        elif operator == "gte":
            return field_value >= value
        elif operator == "lt":
            return field_value < value
        elif operator == "lte":
            return field_value <= value
        
        return False
    
    def add_validator(self, field_name: str, validator: Callable) -> "Form":
        """添加自定义验证器"""
        self.custom_validators[field_name] = validator
        return self
    
    def render(self, template_str: Optional[str] = None) -> str:
        """使用Jinja2模板渲染表单"""
        if template_str is None:
            template_str = self._default_template()
        
        template = Template(template_str)
        return template.render(
            form=self,
            fields=self.fields,
            name=self.name,
            description=self.description
        )
    
    def _default_template(self) -> str:
        """默认HTML模板"""
        return """
<form id="{{ name }}" class="form-builder-form">
    {% if description %}<p class="form-description">{{ description }}</p>{% endif %}
    
    {% for field in fields %}
    <div class="form-field" data-field="{{ field.name }}">
        <label for="{{ field.name }}">
            {{ field.label }}
            {% if field.required %}<span class="required">*</span>{% endif %}
        </label>
        
        {% if field.type == 'textarea' %}
            <textarea name="{{ field.name }}" id="{{ field.name }}"
                {% if field.required %}required{% endif %}
                {% if field.placeholder %}placeholder="{{ field.placeholder }}"{% endif %}
            >{{ field.default or '' }}</textarea>
        {% elif field.type == 'select' %}
            <select name="{{ field.name }}" id="{{ field.name }}"
                {% if field.required %}required{% endif %}>
                {% for opt in field.options %}
                <option value="{{ opt.value }}" {% if field.default == opt.value %}selected{% endif %}>
                    {{ opt.label }}
                </option>
                {% endfor %}
            </select>
        {% else %}
            <input type="{{ field.type }}" name="{{ field.name }}" id="{{ field.name }}"
                {% if field.required %}required{% endif %}
                {% if field.placeholder %}placeholder="{{ field.placeholder }}"{% endif %}
                {% if field.default %}value="{{ field.default }}"{% endif %}
            />
        {% endif %}
        
        {% if field.help_text %}
        <small class="help-text">{{ field.help_text }}</small>
        {% endif %}
    </div>
    {% endfor %}
    
    <button type="submit" class="form-submit">提交</button>
</form>
        """
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "fields": [f.to_dict() for f in self.fields],
            "schema": self.to_json_schema()
        }
    
    def to_json(self) -> str:
        """序列化为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class FormBuilder:
    """
    表单构建器 - 用于创建和管理表单
    """
    
    def __init__(self):
        self.form = Form()
    
    def set_metadata(self, name: str = "", description: str = "") -> "FormBuilder":
        """设置表单元数据"""
        self.form.name = name
        self.form.description = description
        return self
    
    def add_field(self, field: Field) -> "FormBuilder":
        """添加字段"""
        self.form.add_field(field)
        return self
    
    def remove_field(self, name: str) -> "FormBuilder":
        """移除字段"""
        self.form.remove_field(name)
        return self
    
    def add_text_field(self, name: str, label: str, **kwargs) -> "FormBuilder":
        """快捷添加文本字段"""
        return self.add_field(Field(name=name, type="text", label=label, **kwargs))
    
    def add_email_field(self, name: str, label: str, **kwargs) -> "FormBuilder":
        """快捷添加邮箱字段"""
        defaults = {"validation": {"pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"}}
        defaults.update(kwargs)
        return self.add_field(Field(name=name, type="email", label=label, **defaults))
    
    def add_number_field(self, name: str, label: str, **kwargs) -> "FormBuilder":
        """快捷添加数字字段"""
        return self.add_field(Field(name=name, type="number", label=label, **kwargs))
    
    def add_select_field(self, name: str, label: str, options: List[Dict], **kwargs) -> "FormBuilder":
        """快捷添加选择字段"""
        return self.add_field(Field(name=name, type="select", label=label, options=options, **kwargs))
    
    def load_from_yaml(self, file_path: str) -> "Form":
        """从YAML文件加载表单定义"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self._load_from_config(config)
        return self.form
    
    def load_from_json(self, file_path: str) -> "Form":
        """从JSON文件加载表单定义"""
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self._load_from_config(config)
        return self.form
    
    def _load_from_config(self, config: Dict):
        """从配置字典加载表单"""
        self.form.name = config.get("name", "")
        self.form.description = config.get("description", "")
        
        for field_config in config.get("fields", []):
            field = Field(**field_config)
            self.form.add_field(field)
    
    def build(self) -> Form:
        """构建并返回表单实例"""
        return self.form
