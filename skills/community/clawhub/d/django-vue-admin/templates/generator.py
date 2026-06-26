#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Django-Vue-Admin 代码生成器
自动分析 Model 生成完整 CRUD 代码
"""

import os
import re
import sys
from datetime import datetime

# 配置
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_model_fields(models_content):
    """解析 models.py 文件，提取字段信息"""
    models = []
    
    # 提取所有 Model 类
    class_pattern = r'class\s+(\w+)\(([^)]+)\):'
    field_pattern = r'(\w+)\s*=\s*models\.(\w+)\(([^)]*)\)'
    
    classes = re.finditer(class_pattern, models_content)
    
    for cls in classes:
        model_name = cls.group(1)
        base_class = cls.group(2)
        
        # 找到类的起始位置
        start_pos = cls.end()
        
        # 找到类的结束位置（下一个 class 或文件结束）
        next_class = models_content.find('class ', start_pos)
        if next_class == -1:
            class_content = models_content[start_pos:]
        else:
            class_content = models_content[start_pos:next_class]
        
        # 提取字段
        fields = []
        for field_match in re.finditer(field_pattern, class_content):
            field_name = field_match.group(1)
            field_type = field_match.group(2)
            field_args = field_match.group(3)
            
            # 提取 verbose_name
            verbose_name = field_name
            if "verbose_name='" in field_args:
                match = re.search(r"verbose_name='([^']+)'", field_args)
                if match:
                    verbose_name = match.group(1)
            elif 'verbose_name="' in field_args:
                match = re.search(r'verbose_name="([^"]+)"', field_args)
                if match:
                    verbose_name = match.group(1)
            
            # 判断是否为外键
            related_model = None
            if 'ForeignKey' in field_type or 'OneToOneField' in field_type:
                if "'self'" in field_args:
                    related_model = 'self'
                else:
                    match = re.search(r"['\"](\w+)['\"].*on_delete", field_args)
                    if match:
                        related_model = match.group(1)
            
            # 判断是否为 ManyToMany
            if 'ManyToManyField' in field_type:
                match = re.search(r"['\"](\w+)['\"]", field_args)
                if match:
                    related_model = match.group(1)
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'verbose_name': verbose_name,
                'related_model': related_model,
                'args': field_args
            })
        
        if fields:
            models.append({
                'name': model_name,
                'base_class': base_class,
                'fields': fields
            })
    
    return models


def generate_serializer(models):
    """生成 serializers.py"""
    lines = [
        "# -*- coding: utf-8 -*-",
        f"# 自动生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "from rest_framework import serializers",
        "from .models import " + ", ".join([m['name'] for m in models]),
        "",
    ]
    
    for model in models:
        model_name = model['name']
        
        # 获取关联字段
        related_fields = []
        for f in model['fields']:
            if f['related_model']:
                related_fields.append({
                    'name': f['name'],
                    'model': f['related_model'],
                    'display': 'name' if f['related_model'] != 'self' else 'name'
                })
        
        # List Serializer
        lines.append(f"class {model_name}Serializer(serializers.ModelSerializer):")
        for rf in related_fields:
            if rf['model'] != 'self':
                lines.append(f"    {rf['name']}_name = serializers.CharField(source='{rf['name']}.name', read_only=True)")
        
        lines.append('    class Meta:')
        lines.append(f"        model = {model_name}")
        lines.append("        fields = '__all__'")
        lines.append("")
        lines.append("    @staticmethod")
        lines.append("    def setup_eager_loading(queryset):")
        if related_fields:
            selects = [f"'{rf['name']}'" for rf in related_fields if rf['model'] != 'self']
            if selects:
                lines.append(f"        return queryset.select_related({', '.join(selects)})")
            else:
                lines.append("        return queryset")
        else:
            lines.append("        return queryset")
        lines.append("")
        
        # Create Serializer
        create_fields = [f['name'] for f in model['fields'] 
                       if f['name'] not in ['id', 'create_time', 'update_time', 'is_deleted', 'create_by', 'update_by', 'belong_dept']]
        
        lines.append(f"class {model_name}CreateSerializer(serializers.ModelSerializer):")
        lines.append('    class Meta:')
        lines.append(f"        model = {model_name}")
        lines.append(f"        fields = {create_fields}")
        lines.append("")
    
    return "\n".join(lines)


def generate_viewset(models, module_name):
    """生成 views.py"""
    lines = [
        "# -*- coding: utf-8 -*-",
        f"# 自动生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "from rest_framework.viewsets import ModelViewSet",
        "from rest_framework.permissions import IsAuthenticated",
        "from django_filters.rest_framework import DjangoFilterBackend",
        "from rest_framework.filters import SearchFilter, OrderingFilter",
        "from rest_framework.decorators import action",
        "from rest_framework.response import Response",
        "",
        f"from .models import " + ", ".join([m['name'] for m in models]),
        "from .serializers import " + ", ".join([f"{m['name']}Serializer, {m['name']}CreateSerializer" for m in models]),
        "from utils.permission import RbacPermission",
        "",
    ]
    
    for model in models:
        model_name = model['name']
        lower_name = model_name.lower()
        
        lines.append(f"class {model_name}ViewSet(ModelViewSet):")
        lines.append(f'    """{model_name}管理"""')
        lines.append("    perms_map = {")
        lines.append("        'get': '*',")
        lines.append(f"        'post': '{module_name}_{lower_name}_create',")
        lines.append(f"        'put': '{module_name}_{lower_name}_update',")
        lines.append(f"        'delete': '{module_name}_{lower_name}_delete',")
        lines.append("    }")
        lines.append("    permission_classes = [IsAuthenticated, RbacPermission]")
        lines.append(f"    queryset = {model_name}.objects.all()")
        lines.append("")
        lines.append("    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]")
        
        # 推断搜索和过滤字段
        search_fields = []
        filter_fields = []
        for f in model['fields']:
            if f['type'] in ['CharField', 'TextField']:
                search_fields.append(f"'{f['name']}'")
            if f['type'] in ['ForeignKey', 'BooleanField', 'IntegerField']:
                if f['name'] not in ['id', 'create_time', 'update_time']:
                    filter_fields.append(f"'{f['name']}'")
        
        if search_fields:
            lines.append(f"    search_fields = [{', '.join(search_fields)}]")
        if filter_fields:
            lines.append(f"    filterset_fields = [{', '.join(filter_fields)}]")
        
        lines.append("    ordering = ['-create_time']")
        lines.append("")
        lines.append("    def get_serializer_class(self):")
        lines.append("        if self.action in ['list', 'retrieve']:")
        lines.append(f"            return {model_name}Serializer")
        lines.append(f"        return {model_name}CreateSerializer")
        lines.append("")
        lines.append("    def get_queryset(self):")
        lines.append("        from utils.queryset import get_data_scope")
        lines.append("        return get_data_scope(self.request.user, super().get_queryset())")
        lines.append("")
    
    return "\n".join(lines)


def generate_urls(models):
    """生成 urls.py"""
    lines = [
        "# -*- coding: utf-8 -*-",
        f"# 自动生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "from rest_framework.routers import DefaultRouter",
        "from .views import " + ", ".join([f"{m['name']}ViewSet" for m in models]),
        "",
        "router = DefaultRouter()",
    ]
    
    for model in models:
        lower_name = model['name'].lower()
        lines.append(f"router.register(r'{lower_name}', {model['name']}ViewSet, basename='{lower_name}')")
    
    lines.append("")
    lines.append("urlpatterns = router.urls")
    
    return "\n".join(lines)


def generate_api_js(models, module_name):
    """生成前端 API"""
    lines = [
        f"// {module_name} 模块 API",
        f"// 自动生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "import request from '@/utils/request'",
    ]
    
    for model in models:
        model_name = model['name']
        lower_name = model_name.lower()
        
        lines.append(f"")
        lines.append(f"// {model_name} API")
        lines.append(f"export function get{model_name}List(params) {{")
        lines.append(f"  return request({{ url: '/{module_name}/{lower_name}/', method: 'get', params }})")
        lines.append(f"}}")
        lines.append(f"export function get{model_name}(id) {{")
        lines.append(f"  return request({{ url: `/${{'{module_name}/{lower_name}'}}/${{id}}/`, method: 'get' }})")
        lines.append(f"}}")
        lines.append(f"export function create{model_name}(data) {{")
        lines.append(f"  return request({{ url: '/{module_name}/{lower_name}/', method: 'post', data }})")
        lines.append(f"}}")
        lines.append(f"export function update{model_name}(id, data) {{")
        lines.append(f"  return request({{ url: `/${{'{module_name}/{lower_name}'}}/${{id}}/`, method: 'put', data }})")
        lines.append(f"}}")
        lines.append(f"export function delete{model_name}(id) {{")
        lines.append(f"  return request({{ url: `/${{'{module_name}/{lower_name}'}}/${{id}}/`, method: 'delete' }})")
        lines.append(f"}}")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python generator.py <models.py路径> [模块名]")
        print("示例: python generator.py apps/system/models.py system")
        sys.exit(1)
    
    models_path = sys.argv[1]
    module_name = sys.argv[2] if len(sys.argv) > 2 else "myapp"
    
    # 读取 models.py
    with open(models_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析模型
    models = parse_model_fields(content)
    
    if not models:
        print("未找到任何 Model")
        sys.exit(1)
    
    print(f"找到 {len(models)} 个模型: {', '.join([m['name'] for m in models])}")
    
    # 生成代码
    output_dir = os.path.dirname(models_path)
    
    # Serializer
    serializer_content = generate_serializer(models)
    serializer_path = os.path.join(output_dir, 'serializers.py')
    with open(serializer_path, 'w', encoding='utf-8') as f:
        f.write(serializer_content)
    print(f"生成: {serializer_path}")
    
    # ViewSet
    viewset_content = generate_viewset(models, module_name)
    viewset_path = os.path.join(output_dir, 'views.py')
    with open(viewset_path, 'w', encoding='utf-8') as f:
        f.write(viewset_content)
    print(f"生成: {viewset_path}")
    
    # URLs
    urls_content = generate_urls(models)
    urls_path = os.path.join(output_dir, 'urls.py')
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print(f"生成: {urls_path}")
    
    # 前端 API
    client_dir = os.path.dirname(os.path.dirname(os.path.dirname(models_path)))
    api_path = os.path.join(client_dir, 'src', 'api', f'{module_name}.js')
    if not os.path.exists(os.path.dirname(api_path)):
        os.makedirs(os.path.dirname(api_path))
    api_content = generate_api_js(models, module_name)
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(api_content)
    print(f"生成: {api_path}")
    
    print("\n代码生成完成!")


if __name__ == '__main__':
    main()
