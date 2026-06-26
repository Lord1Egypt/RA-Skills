# -*- coding: utf-8 -*-
"""
{{ module_name }} 模块 Serializer 模板
自动生成时间: {{ generate_time }}
"""

from rest_framework import serializers
from .models import (
    {% for model in models %}
    {{ model.name }},
    {% endfor %}
)


{% for model in models %}
class {{ model.name }}Serializer(serializers.ModelSerializer):
    """{{ model.verbose_name|default:model.name }}序列化"""
    {% if model.related_fields %}
    {% for rf in model.related_fields %}
    {{ rf.name }}_name = serializers.CharField(source='{{ rf.name }}.{{ rf.display_field }}', read_only=True)
    {% endfor %}
    {% endif %}

    class Meta:
        model = {{ model.name }}
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        """性能优化: 预加载关联数据"""
        {% if model.related_fields %}
        queryset = queryset.select_related({% for rf in model.related_fields %}'{{ rf.name }}'{% if not forloop.last %}, {% endif %}{% endfor %})
        {% endif %}
        return queryset


class {{ model.name }}CreateSerializer(serializers.ModelSerializer):
    """{{ model.name }}创建/更新序列化"""
    class Meta:
        model = {{ model.name }}
        fields = [{% for field in model.fields %}'{{ field.name }}'{% if not forloop.last %}, {% endif %}{% endfor %}]

{% endfor %}
