# -*- coding: utf-8 -*-
"""
{{ module_name }} 模块 ViewSet 模板
自动生成时间: {{ generate_time }}
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    {% for model in models %}
    {{ model.name }},
    {% endfor %}
)
from .serializers import (
    {% for model in models %}
    {{ model.name }}Serializer, {{ model.name }}CreateSerializer,
    {% endfor %}
)
from utils.permission import RbacPermission


{% for model in models %}
class {{ model.name }}ViewSet(ModelViewSet):
    """{{ model.verbose_name|default:model.name }}管理"""
    perms_map = {
        'get': '*',
        'post': '{{ module_name }}_{{ model.name|lower }}_create',
        'put': '{{ module_name }}_{{ model.name|lower }}_update',
        'delete': '{{ module_name }}_{{ model.name|lower }}_delete',
    }
    permission_classes = [IsAuthenticated, RbacPermission]
    queryset = {{ model.name }}.objects.all()
    
    # 搜索、过滤、排序
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [{% for field in model.search_fields %}'{{ field }}'{% if not forloop.last %}, {% endif %}{% endfor %}]
    filterset_fields = [{% for field in model.filter_fields %}'{{ field }}'{% if not forloop.last %}, {% endif %}{% endfor %}]
    ordering_fields = [{% for field in model.ordering_fields %}'{{ field }}'{% if not forloop.last %}, {% endif %}{% endfor %}]
    ordering = ['-create_time']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return {{ model.name }}Serializer
        return {{ model.name }}CreateSerializer
    
    def get_queryset(self):
        """数据权限过滤"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # 超级管理员看全部
        if user.is_superuser:
            return queryset
        
        # 根据角色数据权限过滤
        {% if model.data_scope == 'department' %}
        from utils.queryset import get_data_scope
        return get_data_scope(user, queryset)
        {% else %}
        return queryset
        {% endif %}

{% endfor %}
