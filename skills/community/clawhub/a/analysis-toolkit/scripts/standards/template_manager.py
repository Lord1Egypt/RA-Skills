"""
模板管理系统 — 行业模板 CRUD

## 数据模型

### Template（行业模板）

| 字段 | 类型 | 必需 | 说明 |
|------|------|:----:|------|
| `template_id` | str | ✅ | 唯一标识符，如 `food-testing` |
| `name` | str | ✅ | 模板名称，如 `食品检验检测标准体系` |
| `industry` | str | ✅ | 所属行业，如 `食品检测` |
| `description` | str | ✅ | 模板用途和适用范围的文字描述 |
| `standards` | list[str] | ✅ | 引用的标准 ID 列表 |
| `default_config` | dict | | 默认计算参数配置 |
| `applicable_scenarios` | list[str] | | 适用的分析场景，如 `["室内质控", "方法验证"]` |
| `notes` | str | | 补充说明 |

### 字段提取指南（供 LLM/智能体创建模板时参考）

要从用户需求或行业规范中提取信息创建模板，需定位以下内容：

1. **template_id**: 行业英文简写，如食品检测 → `food-testing`
2. **name**: 中文名称，如 `食品检验检测标准体系`
3. **industry**: 所属行业
4. **description**: 模板覆盖的业务范围和能力说明
5. **standards**: 该行业常用的标准号列表
6. **default_config**: 该行业最常用的标准编号和参数默认值
7. **applicable_scenarios**: 该行业做哪些类型的分析
"""
import os
import json
from typing import Optional

try:
    from .registry import TEMPLATES_FILE
except ImportError:
    # 当作为 __main__ 直接运行时，使用绝对路径
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from standards.registry import TEMPLATES_FILE  # type: ignore

# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════

TEMPLATE_REQUIRED = {"template_id", "name", "industry", "description", "standards"}


# ═══════════════════════════════════════════════════════
# 模板管理器
# ═══════════════════════════════════════════════════════

class TemplateManager:
    """模板管理器 — 行业模板 CRUD"""

    def __init__(self, filepath: str = TEMPLATES_FILE):
        self._filepath = filepath
        self._templates: dict[str, dict] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self._filepath):
            self._templates = {}
            return
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
            self._templates = {}
            for item in raw_list:
                tid = item.get("template_id")
                if tid:
                    self._templates[tid] = item
        except (json.JSONDecodeError, IOError):
            self._templates = {}

    def _save(self):
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(list(self._templates.values()), f, ensure_ascii=False, indent=2)

    # ── 查询接口 ──

    def list_all(self) -> list[dict]:
        """列出所有模板（摘要）"""
        return [
            {"template_id": t["template_id"], "name": t["name"],
             "industry": t.get("industry"), "standards_count": len(t.get("standards", [])),
             "applicable_scenarios": t.get("applicable_scenarios", [])}
            for t in self._templates.values()
        ]

    def get(self, template_id: str) -> Optional[dict]:
        """获取模板详情（含所有字段）"""
        return self._templates.get(template_id)

    def search(self, keyword: str) -> list[dict]:
        """按关键词搜索（名称/行业/描述）"""
        kw = keyword.lower()
        results = []
        for t in self._templates.values():
            if (kw in t.get("name", "").lower()
                    or kw in t.get("industry", "").lower()
                    or kw in t.get("description", "").lower()):
                results.append(t)
        return results

    def list_by_industry(self, industry: str) -> list[dict]:
        """按行业列出模板"""
        return [
            t for t in self._templates.values()
            if industry.lower() in t.get("industry", "").lower()
        ]

    # ── 增删改接口 ──

    def create(self, data: dict) -> dict:
        """
        创建新模板。

        LLM 调用示例：
        ```python
        tm = TemplateManager()
        result = tm.create({
            "template_id": "food-testing",
            "name": "食品检验检测标准体系",
            "industry": "食品检测",
            "description": "适用于食品理化检验的常用国家标准体系",
            "standards": ["gbt27417", "gbt5009_295"],
            "default_config": {
                "lod_loq_standard": "gbt27417",
                "recovery_standard": "gbt27417",
            },
            "applicable_scenarios": ["室内质控", "方法验证", "标准曲线"],
        })
        ```
        """
        missing = TEMPLATE_REQUIRED - set(data.keys())
        if missing:
            return {"status": "error", "message": f"缺少必需字段: {missing}"}
        tid = data["template_id"]
        if tid in self._templates:
            return {"status": "error", "message": f"模板 '{tid}' 已存在，如需更新请使用 update()"}
        self._templates[tid] = dict(data)
        self._save()
        return {"status": "ok", "message": f"模板 '{tid}' 创建成功", "template_id": tid}

    def update(self, template_id: str, data: dict) -> dict:
        """
        更新模板（增量合并，只覆盖提供的字段）。
        """
        if template_id not in self._templates:
            return {"status": "error", "message": f"模板 '{template_id}' 不存在"}
        self._templates[template_id].update(data)
        self._save()
        return {"status": "ok", "message": f"模板 '{template_id}' 已更新"}

    def delete(self, template_id: str) -> dict:
        """删除模板"""
        if template_id not in self._templates:
            return {"status": "error", "message": f"模板 '{template_id}' 不存在"}
        del self._templates[template_id]
        self._save()
        return {"status": "ok", "message": f"模板 '{template_id}' 已删除"}

    def apply(self, template_id: str) -> dict:
        """
        应用模板 — 返回模板中定义的标准配置，供计算函数使用。

        Returns
        -------
        dict — {"standards": [...], "default_config": {...}, "industry": str}
        """
        tpl = self.get(template_id)
        if not tpl:
            return {"status": "error", "message": f"模板 '{template_id}' 不存在"}
        return {
            "status": "ok",
            "template_id": template_id,
            "name": tpl.get("name"),
            "industry": tpl.get("industry"),
            "standards": tpl.get("standards", []),
            "default_config": tpl.get("default_config", {}),
            "applicable_scenarios": tpl.get("applicable_scenarios", []),
        }


# ═══════════════════════════════════════════════════════
# 单例
# ═══════════════════════════════════════════════════════

_default_manager = None


def get_manager() -> TemplateManager:
    global _default_manager
    if _default_manager is None:
        _default_manager = TemplateManager()
    return _default_manager


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    import sys
    tm = get_manager()
    if len(sys.argv) < 2:
        print("用法: python -m scripts.standards.template_manager <命令> [参数]")
        print("命令: list, get <id>, search <关键词>, list-by-industry <行业>")
        print("       create <json文件>, update <id> <json文件>, delete <id>, apply <id>")
        return

    cmd = sys.argv[1]
    if cmd == "list":
        items = tm.list_all()
        print(f"已有模板 ({len(items)} 个):")
        for t in items:
            print(f"  {t['template_id']}: {t['name']} [{t['industry']}] — {t['standards_count']} 个标准")
    elif cmd == "get" and len(sys.argv) > 2:
        tpl = tm.get(sys.argv[2])
        if tpl:
            print(json.dumps(tpl, ensure_ascii=False, indent=2))
        else:
            print(f"模板 '{sys.argv[2]}' 不存在")
    elif cmd == "search" and len(sys.argv) > 2:
        results = tm.search(sys.argv[2])
        print(f"搜索结果 ({len(results)} 个):")
        for t in results:
            print(f"  {t['template_id']}: {t['name']}")
    elif cmd == "create" and len(sys.argv) > 2:
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            data = json.load(f)
        result = tm.create(data)
        print(f"[{result['status']}] {result['message']}")
    elif cmd == "apply" and len(sys.argv) > 2:
        result = tm.apply(sys.argv[2])
        print(f"应用模板 '{sys.argv[2]}':")
        print(f"  行业: {result.get('industry')}")
        print(f"  引用标准: {', '.join(result.get('standards', []))}")
        if result.get("default_config"):
            print(f"  默认配置: {json.dumps(result['default_config'], ensure_ascii=False)}")
    else:
        print("未知命令或参数不足")


if __name__ == "__main__":
    main()
