"""
Pipeline 流水线系统

三步走：
    1. 定义一个 Pipeline（列步骤）
    2. 执行它（传数据）
    3. 存成模板（下次复用）

内置模板在 templates/default/，用户自定义在 templates/user/。
"""
from .engine import Pipeline, Step, pipeline, step
from .registry import list_templates, load_template, save_template, delete_template
