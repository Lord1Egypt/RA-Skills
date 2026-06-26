"""
Form Builder Pro - 使用示例
演示表单引擎的各种功能
"""

from scripts.form_engine import FormBuilder, Field


def example_basic_form():
    """
    基础表单创建示例
    """
    print("=" * 60)
    print("示例1: 基础表单创建")
    print("=" * 60)
    
    # 使用构建器创建表单
    builder = FormBuilder()
    form = builder \
        .set_metadata(name="contact_form", description="联系表单") \
        .add_text_field("name", "姓名", required=True, placeholder="请输入姓名") \
        .add_email_field("email", "电子邮箱", required=True) \
        .add_text_field("phone", "联系电话", required=False) \
        .add_field(Field(
            name="message",
            type="textarea",
            label="留言内容",
            required=True,
            help_text="请详细描述您的需求"
        )) \
        .build()
    
    # 验证数据
    test_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "phone": "13800138000",
        "message": "这是一个测试留言"
    }
    
    result = form.validate(test_data)
    print(f"验证结果: {result}")
    
    # 测试错误数据
    bad_data = {
        "email": "invalid-email",
        "message": ""
    }
    
    result = form.validate(bad_data)
    print(f"错误数据验证: {result}")


def example_advanced_form():
    """
    高级表单示例 - 包含条件逻辑
    """
    print("\n" + "=" * 60)
    print("示例2: 高级表单 - 条件显示")
    print("=" * 60)
    
    builder = FormBuilder()
    form = builder \
        .set_metadata(name="job_application", description="职位申请表") \
        .add_text_field("full_name", "姓名", required=True) \
        .add_select_field(
            "education",
            "学历",
            options=[
                {"value": "high_school", "label": "高中"},
                {"value": "bachelor", "label": "本科"},
                {"value": "master", "label": "硕士"},
                {"value": "phd", "label": "博士"}
            ],
            required=True
        ) \
        .add_field(Field(
            name="school_name",
            type="text",
            label="毕业院校",
            conditional={
                "field": "education",
                "operator": "not_equals",
                "value": "high_school"
            }
        )) \
        .add_select_field(
            "has_experience",
            "是否有工作经验",
            options=[
                {"value": "yes", "label": "是"},
                {"value": "no", "label": "否"}
            ],
            required=True
        ) \
        .add_number_field(
            "years_experience",
            "工作年限",
            conditional={
                "field": "has_experience",
                "operator": "equals",
                "value": "yes"
            },
            validation={"minimum": 0, "maximum": 50}
        ) \
        .build()
    
    # 测试1: 高中学历（不显示学校字段）
    data1 = {
        "full_name": "李四",
        "education": "high_school",
        "has_experience": "no"
    }
    result1 = form.validate(data1)
    print(f"高中学历验证: valid={result1['valid']}")
    
    # 测试2: 本科学历（显示学校字段）
    data2 = {
        "full_name": "王五",
        "education": "bachelor",
        "school_name": "北京大学",
        "has_experience": "yes",
        "years_experience": 5
    }
    result2 = form.validate(data2)
    print(f"本科有工作经验验证: valid={result2['valid']}")


def example_json_schema():
    """
    JSON Schema生成示例
    """
    print("\n" + "=" * 60)
    print("示例3: JSON Schema生成")
    print("=" * 60)
    
    builder = FormBuilder()
    form = builder \
        .set_metadata(name="user_registration", description="用户注册") \
        .add_text_field(
            "username",
            "用户名",
            required=True,
            validation={"minLength": 3, "maxLength": 20, "pattern": "^[a-zA-Z0-9_]+$"}
        ) \
        .add_email_field("email", "邮箱", required=True) \
        .add_field(Field(
            name="password",
            type="password",
            label="密码",
            required=True,
            validation={"minLength": 8}
        )) \
        .add_number_field(
            "age",
            "年龄",
            required=False,
            validation={"minimum": 18, "maximum": 120}
        ) \
        .build()
    
    schema = form.to_json_schema()
    print("生成的JSON Schema:")
    import json
    print(json.dumps(schema, indent=2, ensure_ascii=False))


def example_yaml_config():
    """
    YAML配置加载示例
    """
    print("\n" + "=" * 60)
    print("示例4: YAML配置加载")
    print("=" * 60)
    
    yaml_content = """
name: survey_form
description: 满意度调查表
fields:
  - name: satisfaction
    type: select
    label: 满意度评分
    required: true
    options:
      - value: "1"
        label: 非常不满意
      - value: "2"
        label: 不满意
      - value: "3"
        label: 一般
      - value: "4"
        label: 满意
      - value: "5"
        label: 非常满意
  - name: feedback
    type: textarea
    label: 具体意见
    required: false
    help_text: 请告诉我们您的具体建议
    conditional:
      field: satisfaction
      operator: "in"
      value: ["1", "2"]
"""
    
    # 保存YAML文件
    with open("/tmp/survey_form.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content)
    
    # 从YAML加载
    builder = FormBuilder()
    form = builder.load_from_yaml("/tmp/survey_form.yaml")
    
    print(f"从YAML加载表单: {form.name}")
    print(f"字段数量: {len(form.fields)}")
    
    # 验证数据
    data = {"satisfaction": "5"}
    result = form.validate(data)
    print(f"验证结果: {result}")


def example_custom_validation():
    """
    自定义验证示例
    """
    print("\n" + "=" * 60)
    print("示例5: 自定义验证规则")
    print("=" * 60)
    
    builder = FormBuilder()
    form = builder \
        .set_metadata(name="password_form") \
        .add_field(Field(
            name="password",
            type="password",
            label="密码",
            required=True
        )) \
        .add_field(Field(
            name="confirm_password",
            type="password",
            label="确认密码",
            required=True
        )) \
        .build()
    
    # 添加自定义验证器 - 确认密码匹配
    def validate_password_match(value, all_data):
        if all_data.get("password") != value:
            return "密码不匹配"
        return True
    
    form.add_validator("confirm_password", validate_password_match)
    
    # 测试验证
    data1 = {
        "password": "Secret123",
        "confirm_password": "Secret123"
    }
    result1 = form.validate(data1)
    print(f"密码匹配验证: {result1}")
    
    data2 = {
        "password": "Secret123",
        "confirm_password": "Wrong123"
    }
    result2 = form.validate(data2)
    print(f"密码不匹配验证: {result2}")


def example_template_rendering():
    """
    模板渲染示例
    """
    print("\n" + "=" * 60)
    print("示例6: 模板渲染")
    print("=" * 60)
    
    builder = FormBuilder()
    form = builder \
        .set_metadata(name="login_form", description="用户登录") \
        .add_field(Field(
            name="username",
            type="text",
            label="用户名",
            required=True,
            placeholder="请输入用户名"
        )) \
        .add_field(Field(
            name="password",
            type="password",
            label="密码",
            required=True,
            placeholder="请输入密码"
        )) \
        .add_field(Field(
            name="remember",
            type="checkbox",
            label="记住我",
            default=False
        )) \
        .build()
    
    # 使用默认模板渲染
    html = form.render()
    print("渲染的HTML表单 (前500字符):")
    print(html[:500] + "...")
    
    # 自定义模板
    custom_template = """
<form class="custom-form">
    <h2>{{ name }}</h2>
    {% for field in fields %}
    <div class="field-wrapper">
        <input name="{{ field.name }}" placeholder="{{ field.label }}" />
    </div>
    {% endfor %}
    <button>提交</button>
</form>
"""
    custom_html = form.render(custom_template)
    print("\n自定义模板渲染 (前300字符):")
    print(custom_html[:300] + "...")


if __name__ == "__main__":
    print("表单构建器专业版 - 使用示例\n")
    
    example_basic_form()
    example_advanced_form()
    example_json_schema()
    example_yaml_config()
    example_custom_validation()
    example_template_rendering()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)
