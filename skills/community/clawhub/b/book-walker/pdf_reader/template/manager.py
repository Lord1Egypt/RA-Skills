"""模板管理 - 用户定义块级加工模板，供 LLM 按句子级处理整段"""
import json
from pathlib import Path
from typing import Optional, Dict, List

# skill/pdf_reader/template/manager.py -> skill/storage
_STORAGE = Path(__file__).resolve().parent.parent.parent / "storage"

DEFAULT_TEMPLATE = "请直接输出原文。"
DEFAULT_PROMPT = """请对以下 PDF 段落按句处理，每句依次输出：
1. 原文（英文保持原样）
2. 翻译（简体中文）
3. 解读（1-2 句总结要点）

只输出处理结果，不要额外解释。"""


class TemplateManager:
    """模板管理器 - 存储/加载用户定义的 LLM 加工模板"""

    def __init__(self, storage_dir: Path = None):
        self._storage = Path(storage_dir) if storage_dir else _STORAGE
        self._file = self._storage / "templates.json"
        self._data: Dict = {}

    def _load(self) -> Dict:
        """加载模板数据"""
        if self._data:
            return self._data
        self._storage.mkdir(parents=True, exist_ok=True)
        if self._file.exists():
            try:
                with open(self._file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {
                "current": "默认",
                "templates": {
                    "默认": DEFAULT_TEMPLATE,
                    "原文翻译解读": DEFAULT_PROMPT,
                },
            }
            self._save()
        return self._data

    def _save(self):
        """保存到文件"""
        self._storage.mkdir(parents=True, exist_ok=True)
        with open(self._file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def list_templates(self) -> List[str]:
        """返回所有模板名称"""
        d = self._load()
        return list(d.get("templates", {}).keys())

    def get_current_name(self) -> str:
        """当前使用的模板名"""
        d = self._load()
        return d.get("current", "默认")

    def get_current_prompt(self) -> str:
        """当前模板的 prompt 文本"""
        d = self._load()
        name = d.get("current", "默认")
        return d.get("templates", {}).get(name, DEFAULT_TEMPLATE)

    def define(self, name: str, prompt: str) -> str:
        """定义/覆盖模板"""
        self._load()
        if "templates" not in self._data:
            self._data["templates"] = {}
        self._data["templates"][name] = prompt
        self._save()
        return f"✅ 已定义模板「{name}」"

    def use(self, name: str) -> str:
        """切换当前模板"""
        self._load()
        if name not in self._data.get("templates", {}):
            return f"❌ 模板「{name}」不存在，请先用「模板 定义 {name} <内容>」创建"
        self._data["current"] = name
        self._save()
        return f"✅ 已切换为模板「{name}」"
