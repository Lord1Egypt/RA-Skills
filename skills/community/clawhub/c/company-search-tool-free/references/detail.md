# 详细参考 - company-search-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
class CompanyInfoQuery:
    """企业信息查询（免费版）"""

    def __init__(self):
        self.searcher = CompanySearcher()

    def get_basic_info(self, company_name):
        """获取企业基本信息"""
        search_result = self.searcher.fuzzy_search(company_name)
        if isinstance(search_result, dict) and "data" in search_result:
            companies = search_result["data"]
            if not companies:
                return {"error": "未找到匹配企业"}

            entid = companies[0].get("entid")
            if not entid:
                return {"error": "未获取到企业ID"}

            basic_info = self.searcher.call_tool(
                "biz_basic_info",
                {"entid": entid}
            )
            return basic_info
        return search_result

    def get_shareholders(self, company_name):
        """获取股东信息"""
        entid = self._get_entid(company_name)
        if not entid:
            return {"error": "未找到企业"}

        return self.searcher.call_tool(
            "biz_shareholders",
            {"entid": entid}
        )

    def get_key_personnel(self, company_name):
        """获取主要人员（董事/监事/高管）"""
        entid = self._get_entid(company_name)
        if not entid:
            return {"error": "未找到企业"}

        return self.searcher.call_tool(
            "biz_key_personnel",
            {"entid": entid}
        )

    def get_investments(self, company_name):
        """获取对外投资"""
        entid = self._get_entid(company_name)
        if not entid:
            return {"error": "未找到企业"}

        return self.searcher.call_tool(
            "biz_investments",
            {"entid": entid}
        )

    def get_changes(self, company_name):
        """获取工商变更记录"""
        entid = self._get_entid(company_name)
        if not entid:
            return {"error": "未找到企业"}

        return self.searcher.call_tool(
            "biz_changes",
            {"entid": entid}
        )

    def _get_entid(self, company_name):
        """获取企业entid"""
        result = self.searcher.fuzzy_search(company_name)
        if isinstance(result, dict) and "data" in result:
            companies = result["data"]
            if companies:
                return companies[0].get("entid")
        return None

query = CompanyInfoQuery()

print("=== 腾讯基本信息 ===")
info = query.get_basic_info("腾讯")
print(json.dumps(info, ensure_ascii=False, indent=2))
```

## 代码示例 (python)

```python
import subprocess
import json

class CompanySearcher:
    """企业查询器（免费版）"""

    def __init__(self, script_path="scripts/tool.mjs"):
        self.script_path = script_path
        self.runtime = self._detect_runtime()

    def _detect_runtime(self):
        """检测JS运行时"""
        for runtime in ["node"]:
            result = subprocess.run(["which", runtime], capture_output=True)
            if result.returncode == 0:
                return runtime
        return "node"

    def discover_tools(self, keyword):
        """发现可用工具"""
        cmd = [self.runtime, self.script_path, "discover", keyword]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            return result.stdout
        return f"查询失败：{result.stderr}"

    def fuzzy_search(self, company_name):
        """企业模糊搜索（获取entid）"""
        cmd = [
            self.runtime, self.script_path, "call", "biz_fuzzy_search",
            "--params", json.dumps({"key": company_name}, ensure_ascii=False)
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return result.stdout
        return {"error": result.stderr}

    def call_tool(self, tool_name, params):
        """调用指定工具"""
        cmd = [
            self.runtime, self.script_path, "call", tool_name,
            "--params", json.dumps(params, ensure_ascii=False)
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8"
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return result.stdout
        return {"error": result.stderr}

searcher = CompanySearcher()

print("=== 可用工具 ===")
print(searcher.discover_tools("企业股东信息"))

print("\n=== 模糊搜索 ===")
result = searcher.fuzzy_search("腾讯")
print(json.dumps(result, ensure_ascii=False, indent=2))
```

