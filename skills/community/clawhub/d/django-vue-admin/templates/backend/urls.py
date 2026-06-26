# -*- coding: utf-8 -*-
"""
{{ module_name }} 模块 URL 路由模板
自动生成时间: {{ generate_time }}
"""

from rest_framework.routers import DefaultRouter
from .views import (
    {% for model in models %}
    {{ model.name }}ViewSet,
    {% endfor %}
)

router = DefaultRouter()

{% for model in models %}
router.register(r'{{ model.name|lower }}', {{ model.name }}ViewSet, basename='{{ model.name|lower }}')
{% endfor %}

urlpatterns = router.urls
