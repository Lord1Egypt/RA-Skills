"""
配置加载器 — 读取 config.yaml，解析环境变量占位符
"""
import os
import re
import yaml


def load_config(config_path: str = "config.yaml") -> dict:
    """加载配置文件，解析 ${VAR} 环境变量占位符"""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # 替换 ${VAR} → 环境变量值
    def _replace_env(match):
        var_name = match.group(1)
        return os.environ.get(var_name, "")

    resolved = re.sub(r'\$\{(\w+)\}', _replace_env, raw)
    return yaml.safe_load(resolved)


# 全局配置实例
config = None


def get_config(config_path: str = "config.yaml") -> dict:
    global config
    if config is None:
        config = load_config(config_path)
    return config


def reload_config(config_path: str = "config.yaml") -> dict:
    global config
    config = load_config(config_path)
    return config
