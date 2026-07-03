"""
模板注册表 — 保存/加载/管理分析流水线模板。

模板存储为 JSON 文件：
    templates/default/  — 内置场景模板，只读
    templates/user/     — 用户自定义模板，可读写

每条流水线可标记 tags，方便分类检索。
"""
import json
import os
from typing import Dict, List, Optional
from .engine import Pipeline, Step

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_DIR = os.path.join(_SKILL_DIR, "pipeline", "templates", "default")
_REPORT_DIR = os.path.join(_SKILL_DIR, "pipeline", "templates", "reports")   # v2: 报告模板
_USER_DIR = os.path.join(_SKILL_DIR, "pipeline", "templates", "user")
os.makedirs(_USER_DIR, exist_ok=True)


def _all_templates(directory: str) -> List[dict]:
    """扫描目录下所有 .json 模板文件"""
    results = []
    if not os.path.isdir(directory):
        return results
    for fname in sorted(os.listdir(directory)):
        if fname.endswith(".json"):
            path = os.path.join(directory, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["_file"] = path
                data["_type"] = "内置" if "default" in directory else "自定义"
                results.append(data)
            except (json.JSONDecodeError, IOError):
                pass
    return results


def list_templates(tag: Optional[str] = None, template_type: str = "all") -> List[dict]:
    """
    列出所有可用模板。

    Parameters
    ----------
    tag : str, optional — 按标签过滤
    template_type : str — "all" | "scenario" | "report" — 按类型筛选

    Returns
    -------
    list[dict]
        每个模板包含 name, description, tags, steps/sections, type
    """
    dirs = []
    if template_type in ("all", "scenario"):
        dirs.extend([_DEFAULT_DIR, _USER_DIR])
    if template_type in ("all", "report"):
        dirs.append(_REPORT_DIR)

    templates = []
    for d in dirs:
        templates.extend(_all_templates(d))

    if tag:
        templates = [t for t in templates if tag in t.get("tags", [])]

    # 精简返回
    return [
        {
            "name": t["name"],
            "description": t.get("description", ""),
            "tags": t.get("tags", []),
            "steps": len(t.get("steps", [])),
            "has_report": bool(t.get("default_report") or t.get("report")),
            "type": t.get("_type", "自定义"),
            "template_type": t.get("type", "scenario"),
        }
        for t in templates
    ]


def load_template(name: str) -> Pipeline:
    """
    按名称加载模板。

    查找顺序（按类型）：
      场景: user/ → default/
      报告: reports/

    Parameters
    ----------
    name : str — 模板名称（不含 .json）

    Returns
    -------
    Pipeline
    """
    # 先查 user 目录
    user_path = os.path.join(_USER_DIR, f"{name}.json")
    if os.path.exists(user_path):
        with open(user_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Pipeline.from_dict(data)

    # 再查 default 目录（场景模板）
    default_path = os.path.join(_DEFAULT_DIR, f"{name}.json")
    if os.path.exists(default_path):
        with open(default_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Pipeline.from_dict(data)

    # 再查 reports 目录（报告模板）
    report_path = os.path.join(_REPORT_DIR, f"{name}.json")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Pipeline.from_dict(data)

    # 模糊匹配
    all_t = (_all_templates(_DEFAULT_DIR)
             + _all_templates(_USER_DIR)
             + _all_templates(_REPORT_DIR))
    for t in all_t:
        if name.lower() in t["name"].lower():
            return Pipeline.from_dict(t)

    raise FileNotFoundError(f"未找到模板: {name}")


def save_template(pipeline: Pipeline, overwrite=False) -> str:
    """
    保存流水线为用户模板。

    Parameters
    ----------
    pipeline : Pipeline
    overwrite : bool
        是否覆盖已有同名模板

    Returns
    -------
    str — 保存路径
    """
    path = os.path.join(_USER_DIR, f"{pipeline.name}.json")

    if os.path.exists(path) and not overwrite:
        raise FileExistsError(f"模板 '{pipeline.name}' 已存在。使用 overwrite=True 覆盖。")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(pipeline.to_dict(), f, ensure_ascii=False, indent=2)

    return path


def delete_template(name: str) -> bool:
    """
    删除用户自定义模板。

    Parameters
    ----------
    name : str

    Returns
    -------
    bool — 是否删除成功
    """
    path = os.path.join(_USER_DIR, f"{name}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
