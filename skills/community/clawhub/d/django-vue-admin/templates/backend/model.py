# -*- coding: utf-8 -*-
"""
{{ module_name }} 模块 Model 模板
自动生成时间: {{ generate_time }}
"""

from django.db import models
from utils.model import CommonBModel


{% for model in models %}
class {{ model.name }}(CommonBModel):
    """{{ model.verbose_name|default:model.name }}"""
    {% for field in model.fields %}
    {{ field.name }} = models.{{ field.type }}(
        {% if field.verbose_name %}
        '{{ field.verbose_name }}',
        {% endif %}
        {% if field.max_length %}
        max_length={{ field.max_length }},
        {% endif %}
        {% if field.max_digits %}
        max_digits={{ field.max_digits }},
        {% endif %}
        {% if field.decimal_places %}
        decimal_places={{ field.decimal_places }},
        {% endif %}
        {% if field.default is not none %}
        default={{ field.default }},
        {% endif %}
        {% if field.null %}
        null=True,
        {% endif %}
        {% if field.blank %}
        blank=True,
        {% endif %}
        {% if field.unique %}
        unique=True,
        {% endif %}
        {% if field.related_name %}
        related_name='{{ field.related_name }}',
        {% endif %}
        {% if field.on_delete %}
        on_delete=models.{{ field.on_delete }},
        {% endif %}
    )
    {% endfor %}

    class Meta:
        verbose_name = '{{ model.verbose_name|default:model.name }}'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.name

{% endfor %}
