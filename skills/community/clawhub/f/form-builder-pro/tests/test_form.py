"""
Form Builder Pro - 单元测试
"""

import pytest
import json
import yaml
import tempfile
import os
from scripts.form_engine import FormBuilder, Field, Form


class TestField:
    """测试Field类"""
    
    def test_field_creation(self):
        """测试字段创建"""
        field = Field(
            name="test_field",
            type="text",
            label="测试字段",
            required=True,
            default="default_value"
        )
        
        assert field.name == "test_field"
        assert field.type == "text"
        assert field.label == "测试字段"
        assert field.required is True
        assert field.default == "default_value"
    
    def test_field_to_dict(self):
        """测试字段序列化"""
        field = Field(name="email", type="email", label="邮箱")
        d = field.to_dict()
        
        assert d["name"] == "email"
        assert d["type"] == "email"
        assert d["label"] == "邮箱"


class TestForm:
    """测试Form类"""
    
    @pytest.fixture
    def sample_form(self):
        """创建示例表单"""
        form = Form(name="test_form", description="测试表单")
        form.add_field(Field(name="username", type="text", label="用户名", required=True))
        form.add_field(Field(name="age", type="number", label="年龄", required=False))
        return form
    
    def test_form_creation(self):
        """测试表单创建"""
        form = Form(name="my_form", description="我的表单")
        assert form.name == "my_form"
        assert form.description == "我的表单"
    
    def test_add_field(self, sample_form):
        """测试添加字段"""
        assert len(sample_form.fields) == 2
        assert sample_form.get_field("username") is not None
        assert sample_form.get_field("age") is not None
    
    def test_remove_field(self, sample_form):
        """测试移除字段"""
        sample_form.remove_field("age")
        assert len(sample_form.fields) == 1
        assert sample_form.get_field("age") is None
    
    def test_to_json_schema(self, sample_form):
        """测试JSON Schema生成"""
        schema = sample_form.to_json_schema()
        
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "username" in schema["properties"]
        assert "age" in schema["properties"]
        assert "required" in schema
        assert "username" in schema["required"]
        assert "age" not in schema["required"]
    
    def test_validate_success(self, sample_form):
        """测试验证成功"""
        data = {"username": "testuser", "age": 25}
        result = sample_form.validate(data)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_missing_required(self, sample_form):
        """测试缺少必填字段"""
        data = {"age": 25}  # 缺少username
        result = sample_form.validate(data)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    def test_validate_type_error(self, sample_form):
        """测试类型错误"""
        data = {"username": "test", "age": "not_a_number"}
        result = sample_form.validate(data)
        
        assert result["valid"] is False
    
    def test_conditional_field(self):
        """测试条件字段"""
        form = Form()
        form.add_field(Field(
            name="has_promo",
            type="checkbox",
            label="有优惠码"
        ))
        form.add_field(Field(
            name="promo_code",
            type="text",
            label="优惠码",
            conditional={
                "field": "has_promo",
                "operator": "equals",
                "value": True
            }
        ))
        
        # 条件满足时
        result1 = form.validate({"has_promo": True, "promo_code": "SAVE20"})
        assert result1["valid"] is True
        
        # 条件不满足时，promo_code不参与验证
        result2 = form.validate({"has_promo": False})
        assert result2["valid"] is True
    
    def test_custom_validator(self, sample_form):
        """测试自定义验证器"""
        def validate_username(value, data):
            if len(value) < 3:
                return "用户名至少需要3个字符"
            return True
        
        sample_form.add_validator("username", validate_username)
        
        # 验证通过
        result1 = sample_form.validate({"username": "abc"})
        assert result1["valid"] is True
        
        # 验证失败
        result2 = sample_form.validate({"username": "ab"})
        assert result2["valid"] is False
        assert any("3个字符" in e for e in result2["errors"])
    
    def test_render_default_template(self, sample_form):
        """测试默认模板渲染"""
        html = sample_form.render()
        
        assert "<form" in html
        assert "username" in html
        assert "age" in html
        assert "<button" in html
    
    def test_render_custom_template(self, sample_form):
        """测试自定义模板渲染"""
        template = "<div>{{ name }}: {% for f in fields %}{{ f.name }} {% endfor %}</div>"
        html = sample_form.render(template)
        
        assert "test_form" in html
        assert "username" in html
        assert "age" in html


class TestFormBuilder:
    """测试FormBuilder类"""
    
    def test_builder_creation(self):
        """测试构建器创建"""
        builder = FormBuilder()
        assert isinstance(builder.form, Form)
    
    def test_set_metadata(self):
        """测试设置元数据"""
        builder = FormBuilder()
        builder.set_metadata(name="my_form", description="描述")
        
        assert builder.form.name == "my_form"
        assert builder.form.description == "描述"
    
    def test_add_field_chaining(self):
        """测试链式调用"""
        builder = FormBuilder()
        result = builder.add_text_field("name", "姓名")
        
        assert result is builder  # 返回self支持链式
        assert len(builder.form.fields) == 1
    
    def test_add_fields(self):
        """测试添加快捷字段方法"""
        builder = FormBuilder()
        form = builder \
            .add_text_field("name", "姓名") \
            .add_email_field("email", "邮箱") \
            .add_number_field("age", "年龄") \
            .add_select_field("gender", "性别", [
                {"value": "male", "label": "男"},
                {"value": "female", "label": "女"}
            ]) \
            .build()
        
        assert len(form.fields) == 4
        assert form.get_field("name").type == "text"
        assert form.get_field("email").type == "email"
        assert form.get_field("age").type == "number"
        assert form.get_field("gender").type == "select"
    
    def test_load_from_json(self):
        """测试从JSON加载"""
        config = {
            "name": "json_form",
            "description": "JSON表单",
            "fields": [
                {"name": "field1", "type": "text", "label": "字段1", "required": True},
                {"name": "field2", "type": "email", "label": "字段2"}
            ]
        }
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            builder = FormBuilder()
            form = builder.load_from_json(temp_path)
            
            assert form.name == "json_form"
            assert len(form.fields) == 2
            assert form.get_field("field1").required is True
        finally:
            os.unlink(temp_path)
    
    def test_load_from_yaml(self):
        """测试从YAML加载"""
        config = {
            "name": "yaml_form",
            "description": "YAML表单",
            "fields": [
                {"name": "title", "type": "text", "label": "标题"}
            ]
        }
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)
            temp_path = f.name
        
        try:
            builder = FormBuilder()
            form = builder.load_from_yaml(temp_path)
            
            assert form.name == "yaml_form"
            assert len(form.fields) == 1
        finally:
            os.unlink(temp_path)
    
    def test_build(self):
        """测试build方法"""
        builder = FormBuilder()
        form = builder.add_text_field("name", "姓名").build()
        
        assert isinstance(form, Form)
        assert len(form.fields) == 1


class TestEdgeCases:
    """测试边界情况"""
    
    def test_empty_form_validation(self):
        """测试空表单验证"""
        form = Form()
        result = form.validate({})
        assert result["valid"] is True
    
    def test_field_order(self):
        """测试字段排序"""
        form = Form()
        form.add_field(Field(name="c", label="C", order=3))
        form.add_field(Field(name="a", label="A", order=1))
        form.add_field(Field(name="b", label="B", order=2))
        
        field_names = [f.name for f in form.fields]
        assert field_names == ["a", "b", "c"]
    
    def test_complex_conditional(self):
        """测试复杂条件逻辑"""
        form = Form()
        form.add_field(Field(name="status", type="select", label="状态"))
        form.add_field(Field(
            name="reason",
            type="textarea",
            label="原因",
            conditional={
                "field": "status",
                "operator": "in",
                "value": ["rejected", "cancelled"]
            }
        ))
        
        # 需要reason
        result1 = form.validate({"status": "rejected", "reason": "不符合要求"})
        assert result1["valid"] is True
        
        # 不需要reason
        result2 = form.validate({"status": "approved"})
        assert result2["valid"] is True
        
        # 缺少reason
        result3 = form.validate({"status": "cancelled"})
        assert result3["valid"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
