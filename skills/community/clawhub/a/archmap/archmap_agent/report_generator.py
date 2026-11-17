from pathlib import Path
from typing import Any
from datetime import datetime


class ReportGenerator:
    def __init__(self, template_dir: str | Path):
        self.template_dir = Path(template_dir)

    # ---- 通用工具方法 ----

    STORAGE_TYPES = {"Table", "MQ", "Redis", "VectorCollection", "MinIO", "LanceDB"}

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _modules_to_dict(self, modules: list[dict] | dict[str, dict]) -> dict[str, dict]:
        """兼容 modules 为数组或对象两种历史格式。"""
        if isinstance(modules, dict):
            return modules
        return {m["module_id"]: m for m in modules}

    def _escape_md_cell(self, text: str) -> str:
        return str(text).replace("|", "\\|").replace("\n", " ")

    def _clean_route(self, route: str) -> str:
        """清洗API路由：移除不可见字符、首尾空格，保留合法路径字符。"""
        cleaned = "".join(c for c in str(route) if c.isprintable())
        return cleaned.strip()

    def _is_valid_api_route(self, route: str) -> bool:
        """校验是否为合法API路由：必须含斜杠，长度合理，不含乱码与非法字符。"""
        r = self._clean_route(route)
        if not r or "/" not in r or len(r) > 120:
            return False
        # 过滤关键字碎片
        fragments = {"state:", "query:", "db:", "query", "db,", "hash(tenant", "e.target.value", "urlPattern,", "t1"}
        if r.lower() in {f.lower() for f in fragments} or r in fragments:
            return False
        # 拒绝含 | ' " \ 空格 或控制字符的路由
        if any(c in r for c in "|'\"\\ "):
            return False
        # 必须仅由合法路径字符组成
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.{}:()<>/?=&%*,~@+")
        if not all(c in allowed for c in r):
            return False
        return True

    def _derive_api_purpose(self, route: str) -> str:
        """基于路由语义生成真实业务用途描述。"""
        r = self._clean_route(route)
        if not r:
            return "业务接口"
        lower = r.lower()
        # 全局语义识别
        if "health" in lower:
            return "健康检查"
        if "login" in lower or "/user" in lower or "/users" in lower:
            return "用户认证与管理"
        if "proxy" in lower:
            if "db" in lower:
                return "数据库代理转发"
            if "prom" in lower:
                return "Prometheus 代理转发"
            return "代理转发"
        if "sse/subscribe" in lower:
            return "SSE 订阅"
        if "pdf" in lower and "raw" in lower:
            return "PDF 原始数据读取"
        if "pdf" in lower:
            return "PDF 数据集操作"
        if any(k in lower for k in ("minio", "s3")):
            return "MinIO 对象存储操作"
        if "vector" in lower:
            return "向量数据操作"
        if "graphql" in lower:
            return "GraphQL 查询"
        if "tongue" in lower or "tonguedb" in lower:
            return "舌诊数据服务"
        if "appium" in lower:
            return "Appium 测试服务"
        if "playwright" in lower:
            return "Playwright 测试服务"
        if "self-heal" in lower:
            return "自愈监控服务"
        if "retro" in lower:
            return "复盘触发服务"
        if "pm-process-step" in lower:
            return "PM 流程步骤处理"

        # 按最后有效段推断动作
        action_map = {
            "list": "查询/列举", "list-recent": "查询最近记录", "overview-stat": "统计概览",
            "stats": "统计", "summary": "摘要", "status": "状态查询",
            "create-template": "创建模板", "save": "保存", "import": "导入", "batch": "批量导入",
            "upload": "上传", "generate": "生成", "preview": "预览", "regenerate": "重新生成",
            "start": "启动", "stop": "终止", "terminate": "终止",
            "restore": "恢复", "restore-full": "完整恢复", "rollback-node": "回滚节点",
            "verify": "校验", "pack": "打包", "cleanup": "清理", "batch-clean": "批量清理",
            "manual-snap": "手动快照",
        }
        segments = [s for s in r.replace("{", "").replace("}", "").replace("<", "").replace(">", "").replace("**", "").split("/") if s]
        for seg in reversed(segments):
            if "{" in seg or seg == "path:path":
                continue
            key = seg.strip(":").split("=")[0]
            if key in action_map:
                return f"{action_map[key]} {r}"
            if any(c.isalpha() for c in key):
                # B04-E09：推断不出真实语义时不输出模板废话，降级为待标注
                return "-（语义待标注）"
        return "-（语义待标注）"

    INVALID_STORAGE_NAMES = {
        "immutable", "writable", "on", "any", "default", "throw", "true", "false", "return",
        "function", "const", "let", "var", "null", "undefined", "table", "mysql", "redis",
        "value of", "ng-table", "jquery-sortable", "fixed-data-table", "x-editable",
        "antd-tools run sort-api-table", "#/rabbitmq",
    }

    def _is_valid_storage_name(self, name: str) -> bool:
        """校验存储名称合法性，过滤版本号、npm包、代码关键字、CSS、UI组件等脏数据。"""
        n = str(name).strip()
        if not n or len(n) > 64:
            return False
        lower = n.lower()
        if lower in self.INVALID_STORAGE_NAMES:
            return False
        # 过滤版本号/表达式/npm包/CSS
        invalid_patterns = ("^", "~", ">=", "<=", ">", "<", "@", "display:", "display ")
        if any(p in n for p in invalid_patterns):
            return False
        # 过滤纯代码片段或单个英文单词
        if " " in n and not any(c.isalnum() for c in n.replace(" ", "")):
            return False
        # 过滤无意义单字/短词
        if len(n) <= 2:
            return False
        # 过滤明显前端组件名
        if any(k in lower for k in ("editable", "sortable", "jquery", "leaflet", "ng-table")):
            return False
        # 必须包含可识别字符
        if not any(c.isalnum() or c in "_.-" for c in n):
            return False
        return True

    def _module_layer(self, module_id: str) -> int:
        """按模块名推断架构层级：0=存储/基础设施，1=后端/核心，2=前端/展示，3=部署/文档/测试。"""
        lower = module_id.lower()
        if any(k in lower for k in ("data", "lance", "storage", "db", "archive", "checkpoint", "cache", "pdf", "review", "memory", "vector")):
            return 0
        if any(k in lower for k in ("frontend", "ui", "web", "client", "appium-frontend", "app.frontend")):
            return 2
        if any(k in lower for k in ("deploy", "docker", "docs", "test", "spec", "output", "log")):
            return 3
        return 1

    def _classify_storage(self, name: str) -> str:
        n = name.lower()
        if "redis" in n:
            return "Redis"
        if any(k in n for k in ("rabbit", "kafka", "mq", "queue")):
            return "MQ"
        if "minio" in n or "s3" in n:
            return "MinIO"
        if "lance" in n:
            return "LanceDB"
        if any(k in n for k in ("vector", "vec", "embedding")):
            return "VectorCollection"
        if any(k in n for k in ("mysql", "sqlite", "postgres", "table", "db")):
            return "Table"
        return "Table"

    def _source_file_stems(self, m: dict) -> list[str]:
        p = Path(m.get("abs_path", ""))
        if not p.is_dir():
            return []
        stems = []
        for f in sorted(p.iterdir()):
            if f.is_file() and f.suffix in (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rs"):
                if f.stem in ("__init__", "__main__"):
                    continue
                stems.append(f.stem)
        return stems

    def _derive_responsibility(self, m: dict) -> str:
        """基于模块API、存储、源码文件名或目录名推断核心业务职责。"""
        apis = [self._clean_route(a.get("route", "")) for a in m.get("apis", []) if self._is_valid_api_route(a.get("route", ""))]
        storages = [s.get("name", "") for s in m.get("storages", []) if self._is_valid_storage_name(s.get("name", ""))]
        path = Path(m.get("module_path", "")).name or m.get("module_id", "")
        if apis and storages:
            return f"提供 {apis[0]} 等接口服务，读写 {storages[0]} 等存储"
        if apis:
            return f"提供 {apis[0]} 等接口服务"
        if storages:
            return f"管理 {storages[0]} 等数据存储"
        name_hints = {
            "backend": "后端主服务",
            "frontend": "前端应用",
            "data": "数据存储层",
            "deploy": "部署配置",
            "etl": "ETL 数据处理",
            "appium_engine": "Appium 测试执行引擎（设备连接、脚本运行、报告生成）",
            "appium-frontend": "Appium 前端代理服务",
            "appium_reports": "Appium 测试报告存储",
            "archive": "上下文归档资料",
            "archive_system": "审计归档系统",
            "config": "项目配置管理",
            "docs": "文档资料与 PDF 原始数据接口",
            "scripts": "流程脚本与 PM 步骤处理端点",
            "deliverables": "交付物管理接口",
            "experience_lib": "经验库加载与管理（通用违规、流程经验沉淀）",
            "harness_agent": "Harness 平台 Agent（步骤同步、项目/实例管理）",
            "knowledge_base": "知识库数据与检索规则管理",
            "mempalace": "MemPalace 本地记忆服务（向量索引、嵌入、压缩、存储）",
            "playwright-skill": "Playwright 技能服务（页面截图、静态资源代理）",
            "prompt_store": "提示词仓库（核心加载器、约束规则、少样例案例）",
            "projects": "项目资产与模板管理",
            "retrieval": "检索引擎（通用/PDF 检索、角色过滤、路由）",
            "tongue_diagnosis": "中医舌诊数据库（ETL、知识库迁移、数据回填）",
        }
        if path in name_hints:
            return name_hints[path]
        stems = self._source_file_stems(m)
        if stems:
            return f"负责 {', '.join(stems[:3])} 等核心实现"
        return f"{path} 模块"

    def _is_business_module_id(self, mid: str) -> bool:
        """校验模块ID是否为顶层业务模块（不含子路径、隐藏目录）。"""
        if not mid:
            return False
        if mid.startswith(".") or mid.startswith("_"):
            return False
        if "/" in str(mid) or "\\" in str(mid):
            return False
        return True

    def _filter_business_deps(self, deps: list[str], valid_ids: set[str]) -> list[str]:
        """过滤依赖列表，仅保留顶层业务模块ID。"""
        return sorted(d for d in deps if self._is_business_module_id(d) and d in valid_ids and d != "")

    @staticmethod
    def _import_deps(m: dict) -> list:
        """循环依赖判定仅认 import 边；旧基线条目无该字段时回退 dependencies。"""
        return m.get("import_dependencies") if "import_dependencies" in m else m.get("dependencies", [])

    def _detect_cycles(self, modules: dict[str, dict]) -> set[tuple[str, str]]:
        """检测模块间双向循环依赖（仅基于 import 代码级依赖，URL 字符串引用不构成循环）。"""
        cycles = set()
        for mid, m in modules.items():
            for dep in self._import_deps(m):
                if dep in modules and mid in self._import_deps(modules[dep]):
                    cycles.add(tuple(sorted([mid, dep])))
        return cycles

    def _mermaid_file(self, title: str, description: str, mermaid_text: str) -> str:
        return f"# {title}\n\n{description}\n\n```mermaid\n{mermaid_text}\n```\n"

    # ---- 各报告渲染方法 ----

    def _render_01_summary(self, aggregated: dict, violations: list[dict], config: dict) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        shared_apis = aggregated.get("shared_apis", [])
        shared_storages = aggregated.get("shared_storages", [])
        project_name = config.get("project_name", "unknown")
        mode = config.get("mode", "全量基线构建")

        # 统计
        total_modules = len(modules)
        violation_modules = {mid for mid, m in modules.items() if m.get("violations")}

        # 循环依赖检测（仅 import 边）
        cycle_pairs = []
        seen = set()
        for mid, m in modules.items():
            for dep in self._import_deps(m):
                if dep in modules and mid in self._import_deps(modules[dep]):
                    pair = tuple(sorted([mid, dep]))
                    if pair not in seen:
                        seen.add(pair)
                        cycle_pairs.append(pair)

        # 共享资源使用统计（基于清洗后的存储清单，禁止直接读取原始脏数据）
        api_usage: dict[str, int] = {}
        for m in modules.values():
            for api in m.get("apis", []):
                if api.get("shared"):
                    route = api.get("route", "")
                    api_usage[route] = api_usage.get(route, 0) + 1

        storage_records = self._collect_storage_records({"modules": aggregated.get("modules", {})})
        shared_storage_records = {
            name: rec for name, rec in storage_records.items()
            if rec["shared"] or len(rec["modules"]) > 1
        }

        lines = [f"# 执行摘要", ""]
        lines.append(f"- 项目标识：{project_name}")
        lines.append(f"- 测绘类型：{mode}")
        lines.append(f"- 测绘时间：{self._now()}")
        lines.append("")
        lines.append("## 统计概况")
        lines.append(f"- 业务模块：{total_modules} 个")
        lines.append(f"- 共享API：{len(shared_apis)} 个")
        lines.append(f"- 共享数据表/存储：{len(shared_storage_records)} 个")
        lines.append(f"- 粒度异常模块：{len(violation_modules)} 个")
        lines.append(f"- 循环依赖对：{len(cycle_pairs)} 对")
        lines.append("")

        lines.append("## 风险提示")
        if cycle_pairs:
            lines.append("1. 以下模块对存在双向循环依赖：")
            for a, b in cycle_pairs[:10]:
                lines.append(f"   - `{a}` ↔ `{b}`")
            if len(cycle_pairs) > 10:
                lines.append(f"   - ... 共 {len(cycle_pairs)} 对，详见 08_依赖矩阵.md")
            # A04-E13：风险区必须可行动——严重度分级 + 处置建议
            involved = {x for pair in cycle_pairs for x in pair}
            severity = "高" if len(cycle_pairs) >= 3 or len(involved) >= 3 else "中"
            lines.append(f"   - 严重度：{severity}（{len(cycle_pairs)} 对、涉及 {len(involved)} 个模块成网）")
            lines.append("   - 处置建议：提取双向引用中的共享契约（接口/模型/常量）为独立模块，或对其中一方做依赖倒置（事件/回调/注册表）；优先拆解被依赖最多的模块（见 05 清单「被哪些模块依赖」列）。")
        else:
            lines.append("1. 未发现模块间循环依赖。")

        multi_api = [(r, c) for r, c in api_usage.items() if c > 1]
        if multi_api:
            lines.append(f"2. 以下共享 API 被多个模块使用，修改需关注兼容性：")
            for r, c in sorted(multi_api, key=lambda x: -x[1])[:5]:
                lines.append(f"   - `{r}`：{c} 个模块")
        else:
            lines.append("2. 未发现跨模块共享 API。")

        if shared_storage_records:
            lines.append(f"3. 以下共享存储被多个模块使用，修改需关注兼容性：")
            for name, rec in sorted(shared_storage_records.items(), key=lambda x: -len(x[1]["modules"]))[:5]:
                lines.append(f"   - `{name}`：{len(rec['modules'])} 个模块")
        else:
            lines.append("3. 未发现跨模块共享存储。")

        if violation_modules:
            lines.append(f"4. 粒度异常模块：{len(violation_modules)} 个，详见 09_粒度校验报告.md")
        else:
            lines.append("4. 未发现粒度异常模块。")

        # B04-E09：疑似副本/镜像模块检测——API 集合高度重合的模块对会让共享 API 统计掺入噪声
        api_sets: dict[str, set] = {}
        for mid, m in modules.items():
            if not self._is_business_module_id(mid):
                continue
            routes = {self._clean_route(a.get("route", "")) for a in m.get("apis", []) if self._is_valid_api_route(a.get("route", ""))}
            if len(routes) >= 5:
                api_sets[mid] = routes
        dup_hints = []
        ids = sorted(api_sets)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a_set, b_set = api_sets[ids[i]], api_sets[ids[j]]
                inter = len(a_set & b_set)
                if inter >= 5 and inter / min(len(a_set), len(b_set)) >= 0.8:
                    dup_hints.append((ids[i], ids[j], inter))
        if dup_hints:
            lines.append("5. 疑似副本/镜像模块（API 集合重合度 ≥80%，共享 API 统计含噪声，建议确认是否部署副本/代理转发）：")
            for a, b, inter in dup_hints[:5]:
                lines.append(f"   - `{a}` ≈ `{b}`：{inter} 个重合 API")

        lines.append("")
        lines.append("## 查阅指引")
        lines.append("- 模块明细 → 05_模块资产清单.md")
        lines.append("- API 明细 → 06_API资产清单.md")
        lines.append("- 存储明细 → 07_存储资产清单.md")
        lines.append("- 依赖详情 → 08_依赖矩阵.md")
        lines.append("- 架构依赖视图 → 02_架构图.md")
        lines.append("- 数据流转视图 → 03_数据链路图.md")
        lines.append("- 时序视图 → 04_时序图.md")
        lines.append("- 解析异常明细 → 09_粒度校验报告.md")
        lines.append("")
        return "\n".join(lines)

    def _render_02_architecture(self, mermaid: dict) -> str:
        return self._mermaid_file(
            "模块全局依赖架构图",
            "下图展示所有业务模块调用依赖关系，仅体现模块层级关联，接口、存储明细查看对应资产清单。",
            mermaid.get("architecture", "graph TD\n    root[root]"),
        )

    def _render_03_data_flow(self, mermaid: dict) -> str:
        return self._mermaid_file(
            "数据链路图",
            "下图展示模块与共享存储/消息队列之间的读写流向，实线表示存在读写关联。\n\n> 覆盖声明（A04-E09）：仅统计源码静态特征可识别的存储资产；SQLite 文件库、LanceDB 实例、Redis、MinIO、文件系统快照等运行时创建的存储可能未被覆盖，实际存储面请以部署配置与运行时盘点为准。",
            mermaid.get("data_flow", "graph LR\n    Module[Module]"),
        )

    def _render_04_sequence(self, mermaid: dict) -> str:
        return self._mermaid_file(
            "核心业务流程时序图",
            "下图基于模块依赖关系生成**示意性**核心调用链路（B06-E15：非真实调用追踪，不含分支/异常/并发路径）。真实业务时序请结合 06_API资产清单.md 的入口路由及其调用方代码确认。",
            mermaid.get("sequence", "sequenceDiagram\n    actor User\n    User->>Module: 请求"),
        )

    def _render_05_modules(self, aggregated: dict) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        valid_ids = {mid for mid in modules.keys() if self._is_business_module_id(mid)}
        cycles = self._detect_cycles(modules)
        lines = ["# 模块资产清单", ""]
        lines.append("| 模块ID | 模块名称 | 核心业务职责 | 源码目录路径 | 依赖外部模块 | 被哪些模块依赖 |")
        lines.append("|---|---|---|---|---|---|")
        for mid in sorted(valid_ids):
            m = modules[mid]
            name = self._escape_md_cell(Path(m.get("module_path", "").strip("/")).name or mid)
            path = self._escape_md_cell(m.get("module_path", ""))
            responsibility = self._escape_md_cell(self._derive_responsibility(m))
            deps = self._filter_business_deps(m.get("dependencies", []), valid_ids)
            dps = self._filter_business_deps(m.get("dependents", []), valid_ids)
            dep_text = ", ".join(f"`{d}`" for d in deps) or "-"
            dp_text = ", ".join(f"`{d}`" for d in dps) or "-"
            # 标记循环依赖风险
            has_cycle = any(mid in pair for pair in cycles)
            if has_cycle:
                dep_text = (dep_text + " 【循环依赖风险】") if dep_text != "-" else "【循环依赖风险】"
            lines.append(
                f"| `{mid}` | {name} | {responsibility} | {path} | {dep_text} | {dp_text} |"
            )
        lines.append("")
        return "\n".join(lines)

    def _render_06_apis(self, aggregated: dict) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        valid_ids = {mid for mid in modules.keys() if self._is_business_module_id(mid)}
        route_records: dict[str, dict] = {}
        for mid in sorted(valid_ids):
            for api in modules[mid].get("apis", []):
                route = self._clean_route(api.get("route", ""))
                if not self._is_valid_api_route(route):
                    continue
                rec = route_records.setdefault(route, {"owners": set(), "shared": False})
                rec["owners"].add(mid)
                if api.get("shared"):
                    rec["shared"] = True

        rows: list[str] = []
        for route in sorted(route_records.keys()):
            rec = route_records[route]
            owners = sorted(rec["owners"])
            owner_text = ", ".join(f"`{m}`" for m in owners)
            purpose = self._escape_md_cell(self._derive_api_purpose(route))
            shared = "true" if (rec["shared"] or len(owners) > 1) else "false"
            rows.append(f"| `{route}` | {owner_text} | {purpose} | {shared} |")

        lines = ["# API资产清单", ""]
        lines.append("| API标识(路由) | 归属模块 | 业务用途 | reuse_flag |")
        lines.append("|---|---|---|---|")
        lines.extend(rows or ["| - | - | - | - |"])
        lines.append("")
        return "\n".join(lines)

    def _collect_storage_records(self, aggregated: dict) -> dict[str, dict]:
        """按清洗后的存储名称聚合，返回 {name: {"modules": set[str], "shared": bool}}。"""
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        valid_ids = {mid for mid in modules.keys() if self._is_business_module_id(mid)}
        records: dict[str, dict] = {}
        for mid in valid_ids:
            for storage in modules[mid].get("storages", []):
                name = storage.get("name", "")
                if not self._is_valid_storage_name(name):
                    continue
                records.setdefault(name, {"modules": set(), "shared": False})
                records[name]["modules"].add(mid)
                if storage.get("shared"):
                    records[name]["shared"] = True
        return records

    def _render_07_storages(self, aggregated: dict) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        valid_ids = {mid for mid in modules.keys() if self._is_business_module_id(mid)}
        storage_records = self._collect_storage_records(aggregated)
        exclusive_rows: list[str] = []
        shared_rows: list[str] = []
        for name in sorted(storage_records.keys()):
            record = storage_records[name]
            candidates = [m for m in record["modules"] if self._is_business_module_id(m)]
            owner = min(candidates, key=lambda mid: (self._module_layer(mid), mid))
            kind = self._classify_storage(name)
            shared = record["shared"] or len(record["modules"]) > 1
            row = f"| {kind} | `{name}` | `{owner}` | {'true' if shared else 'false'} |"
            if shared:
                shared_rows.append(row)
            else:
                exclusive_rows.append(row)

        lines = ["# 存储资产清单", ""]
        lines.append("## 独占资源")
        lines.append("")
        lines.append("| 资源类型 | 资源名称 | 归属模块 | 是否共享 |")
        lines.append("|---|---|---|---|")
        lines.extend(exclusive_rows or ["| - | - | - | - |"])
        lines.append("")
        lines.append("## 共享资源")
        lines.append("")
        lines.append("| 资源类型 | 资源名称 | 归属模块 | 是否共享 |")
        lines.append("|---|---|---|---|")
        lines.extend(shared_rows or ["| - | - | - | - |"])
        lines.append("")
        return "\n".join(lines)

    def _render_08_dependency_matrix(self, aggregated: dict) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        valid_ids = {mid for mid in modules.keys() if self._is_business_module_id(mid)}
        active_ids = sorted(
            mid for mid in valid_ids
            if modules[mid].get("dependencies") or modules[mid].get("dependents")
        )
        lines = ["# 依赖矩阵", ""]
        if not active_ids:
            lines.append("当前未识别到模块间依赖。")
            lines.append("")
            return "\n".join(lines)

        lines.append("横向：被依赖模块；纵向：当前模块。`✅` 表示存在依赖（含 API 消费/存储共享），`🔁` 表示 import 级双向循环依赖。")
        lines.append("")
        header = "| 模块 | " + " | ".join(f"`{mid}`" for mid in active_ids) + " |"
        sep = "|---|---|" + "|".join("---" for _ in active_ids) + "|"
        lines.append(header)
        lines.append(sep)
        for row_id in active_ids:
            row_deps = set(self._filter_business_deps(modules[row_id].get("dependencies", []), valid_ids))
            cells = []
            for col_id in active_ids:
                if col_id in row_deps:
                    cells.append("🔁" if row_id in self._import_deps(modules[col_id]) and col_id in self._import_deps(modules[row_id]) else "✅")
                else:
                    cells.append("")
            lines.append(f"| `{row_id}` | " + " | ".join(cells) + " |")
        lines.append("")
        return "\n".join(lines)

    def _render_09_granularity(self, aggregated: dict, violations: list[dict]) -> str:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        lines = ["# 粒度校验报告", ""]

        module_violations = []
        for mid, m in modules.items():
            for v in m.get("violations", []):
                module_violations.append({
                    "module_id": mid,
                    "type": v.get("type", "粒度异常"),
                    "detail": v.get("detail", str(v)),
                })

        all_violations = module_violations + violations
        lines.append(f"- 异常模块数量：{len({v['module_id'] for v in all_violations})}")
        lines.append(f"- 违规记录总数：{len(all_violations)}")
        lines.append("")

        if not all_violations:
            lines.append("本次测绘未发现粒度违规或解析异常。")
            lines.append("")

        # B06-E13：产物交叉一致性自检——报告群自身的口径对齐与欠覆盖告警
        lines.append("## 产物交叉一致性自检")
        storage_records = self._collect_storage_records({"modules": aggregated.get("modules", {})})
        shared_cnt = sum(1 for r in storage_records.values() if r["shared"] or len(r["modules"]) > 1)
        exclusive_cnt = len(storage_records) - shared_cnt
        unique_routes = set()
        for m in modules.values():
            for a in m.get("apis", []):
                r = self._clean_route(a.get("route", ""))
                if self._is_valid_api_route(r):
                    unique_routes.add(r)
        lines.append(f"- 唯一 API 路由数（06 口径）：{len(unique_routes)}")
        lines.append(f"- 存储资产数（07 口径）：{len(storage_records)}（共享 {shared_cnt} / 独占 {exclusive_cnt}）")
        if len(unique_routes) >= 50 and len(storage_records) <= max(1, len(unique_routes) // 50):
            lines.append(f"- ⚠️ 欠覆盖告警：API/存储比例 {len(unique_routes)}:{len(storage_records)} 严重失衡，存储静态识别大概率欠覆盖（参见 03 图头覆盖声明），01 的「共享存储」计数请勿当作系统真实存储面。")
        else:
            lines.append("- API/存储比例处于常规区间。")
        lines.append("- 口径说明：01 摘要、03 数据链路图、07 存储清单共用同一清洗聚合管线，三者存储计数一致；不一致即引擎缺陷，请上报。")
        lines.append("")

        if not all_violations:
            return "\n".join(lines)

        lines.append("| 模块ID | 违规类型 | 违规详情描述 |")
        lines.append("|---|---|---|")
        for v in all_violations:
            mid = self._escape_md_cell(v.get("module_id", ""))
            vtype = self._escape_md_cell(v.get("type", ""))
            detail = self._escape_md_cell(v.get("detail", ""))
            lines.append(f"| `{mid}` | {vtype} | {detail} |")
        lines.append("")
        lines.append("## 建议处理方案")
        lines.append("1. 对超粒度模块进一步拆分，确保单个模块职责单一。")
        lines.append("2. 对单文件模块补充目录上下文，避免孤立解析。")
        lines.append("3. API 描述中移除入参/出参细节，保持高层语义。")
        lines.append("4. 存储描述中移除字段/索引细节，聚焦资源类型与用途。")
        lines.append("")
        return "\n".join(lines)

    # ---- 入口 ----

    def generate_full(self, aggregated: dict, mermaid: dict[str, str], violations: list[dict], config: dict) -> dict[str, str]:
        dispatch = {
            "01_执行摘要.md": lambda: self._render_01_summary(aggregated, violations, config),
            "02_架构图.md": lambda: self._render_02_architecture(mermaid),
            "03_数据链路图.md": lambda: self._render_03_data_flow(mermaid),
            "04_时序图.md": lambda: self._render_04_sequence(mermaid),
            "05_模块资产清单.md": lambda: self._render_05_modules(aggregated),
            "06_API资产清单.md": lambda: self._render_06_apis(aggregated),
            "07_存储资产清单.md": lambda: self._render_07_storages(aggregated),
            "08_依赖矩阵.md": lambda: self._render_08_dependency_matrix(aggregated),
            "09_粒度校验报告.md": lambda: self._render_09_granularity(aggregated, violations),
        }
        files = {}
        # B06-E01：02~09 统一注入基线元信息头（01 自带时间戳不重复注入）
        meta_header = f"> 基线元信息：生成时间 {self._now()} ｜ 测绘模式 {config.get('mode', '全量基线构建')} ｜ 引擎 archmap_agent\n"
        for tpl in config.get("report_templates", []):
            content = dispatch.get(tpl, lambda: f"# {tpl}\n\n（未定义渲染器）")()
            if tpl != "01_执行摘要.md":
                head, _, rest = content.partition("\n")
                content = head + "\n\n" + meta_header + rest
            files[tpl] = content
        return files
