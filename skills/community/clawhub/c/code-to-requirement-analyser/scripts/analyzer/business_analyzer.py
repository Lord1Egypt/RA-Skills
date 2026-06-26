# scripts/analyzer/business_analyzer.py
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class TradeDimension:
    lifecycle: List[str]  # 创建/审核/执行/清算/结算/归档
    trade_type: List[str]  # 买入/卖出/申购/赎回/兑换
    product_type: List[str]  # 基金/股票/债券/存款
    channel: List[str]  # APP/网银/柜面/第三方
    parties: List[str]  # 买方/卖方/担保方/监管方

@dataclass
class FunctionalRequirement:
    id: str
    name: str
    description: str
    priority: str  # P0/P1/P2
    scenario: str
    ui_elements: List[str]
    acceptance_criteria: List[str]

@dataclass
class BusinessRule:
    id: str
    name: str
    rule_type: str  # validation/permission/calculation/constraint
    description: str
    expression: Optional[str]
    severity: str  # error/warning/info
    related_fields: List[str]

class TradeBusinessAnalyzer:
    """交易业务分析器"""
    
    def __init__(self, taxonomy_path: str = None):
        self.taxonomy = self._load_taxonomy(taxonomy_path)
        self.component_library = self._load_component_library()
        
    def _load_taxonomy(self, path: Optional[str]) -> Dict:
        """加载交易分类体系"""
        default_taxonomy = {
            "lifecycle": {
                "创建": ["录入", "选择", "确认", "提交"],
                "审核": ["初审", "复审", "终审", "驳回"],
                "执行": ["冻结", "扣款", "成交", "确认"],
                "清算": ["对账", "计算", "核对"],
                "结算": ["划拨", "到账", "凭证"],
                "归档": ["存储", "查询", "审计"]
            },
            "trade_types": {
                "买入": ["认购", "申购", "定投"],
                "卖出": ["赎回", "变现", "到期"],
                "兑换": ["转换", "调仓", "换汇"],
                "其他": ["分红", "质押", "解冻"]
            },
            "products": ["基金", "股票", "债券", "存款", "理财", "保险", "信托"],
            "channels": ["手机银行", "网银", "柜面", "自助终端", "API"],
        }
        
        if path and Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                return {**default_taxonomy, **json.load(f)}
        return default_taxonomy
    
    def _load_component_library(self) -> Dict[str, Dict]:
        """加载组件语义库"""
        return {
            "el-input-number": {
                "semantic": "数值输入",
                "common_fields": ["amount", "quantity", "price", "rate"],
                "business_type": "金额/数量"
            },
            "el-select": {
                "semantic": "选项选择",
                "common_fields": ["type", "status", "category", "productId"],
                "business_type": "分类/状态"
            },
            "el-date-picker": {
                "semantic": "日期选择",
                "common_fields": ["startDate", "endDate", "tradeDate", "maturityDate"],
                "business_type": "时间要素"
            },
            "el-table": {
                "semantic": "数据列表",
                "common_patterns": ["query_result", "position_list", "history_record"],
                "business_type": "信息展示"
            }
        }
    
    def analyze(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """主分析方法"""
        
        # 1. 识别交易维度
        dimension = self._identify_dimension(parsed_data)
        
        # 2. 推导功能需求
        requirements = self._derive_requirements(parsed_data, dimension)
        
        # 3. 标准化业务规则
        rules = self._standardize_rules(parsed_data.get("business_rules", []))
        
        # 4. 构建数据字典
        data_dict = self._build_data_dictionary(parsed_data)
        
        # 5. 识别业务流程
        process = self._identify_process(parsed_data, dimension)
        
        # 6. 计算置信度
        confidence = self._calculate_overall_confidence(parsed_data, dimension)
        
        return {
            "trade_dimension": dimension.__dict__,
            "functional_requirements": [r.__dict__ for r in requirements],
            "business_rules": [r.__dict__ for r in rules],
            "data_dictionary": data_dict,
            "business_process": process,
            "analysis_confidence": confidence,
            "suggestions": self._generate_suggestions(parsed_data, dimension)
        }
    
    def _identify_dimension(self, data: Dict) -> TradeDimension:
        """识别交易维度"""
        text = json.dumps(data, ensure_ascii=False).lower()
        
        # 生命周期识别
        lifecycle_scores = {}
        for phase, indicators in self.taxonomy["lifecycle"].items():
            score = sum(1 for ind in indicators if ind in text)
            if score > 0:
                lifecycle_scores[phase] = score
        lifecycle = sorted(lifecycle_scores, key=lifecycle_scores.get, reverse=True)[:2]
        
        # 交易类型识别
        trade_types = []
        for ttype, variants in self.taxonomy["trade_types"].items():
            if any(v in text for v in [ttype] + variants):
                trade_types.append(ttype)
        
        # 产品类型识别
        products = [p for p in self.taxonomy["products"] if p in text]
        
        # 渠道识别
        channels = [c for c in self.taxonomy["channels"] if c in text]
        
        # 参与方推断（基于API和字段名）
        parties = []
        if any(kw in text for kw in ["buyer", "买方", "申购方"]):
            parties.append("买方")
        if any(kw in text for kw in ["seller", "卖方", "发行方"]):
            parties.append("卖方")
        
        return TradeDimension(
            lifecycle=lifecycle or ["未识别"],
            trade_type=trade_types or ["未识别"],
            product_type=products or ["通用"],
            channel=channels or ["未指定"],
            parties=parties or ["客户"]
        )
    
    def _derive_requirements(self, data: Dict, dimension: TradeDimension) -> List[FunctionalRequirement]:
        """推导功能需求"""
        requirements = []
        components = data.get("components", [])
        apis = data.get("apis", [])
        
        # 按组件类型分组分析
        forms = [c for c in components if c.get("type") == "form"]
        tables = [c for c in components if c.get("type") == "table"]
        actions = [c for c in components if c.get("type") == "button"]
        
        # 表单录入需求
        if forms:
            req = FunctionalRequirement(
                id="FR-001",
                name=f"{dimension.trade_type[0]}信息录入" if dimension.trade_type else "交易信息录入",
                description=f"用户通过表单录入{dimension.product_type[0] if dimension.product_type else '产品'}交易所需信息",
                priority="P0",
                scenario=f"客户需要{dimension.trade_type[0] if dimension.trade_type else '办理'}业务时",
                ui_elements=[f["name"] for f in forms[:3]],
                acceptance_criteria=[
                    "支持所有必填字段输入",
                    "实时校验数据合法性",
                    "提供默认值和自动计算"
                ]
            )
            requirements.append(req)
        
        # 数据查询需求（基于表格组件）
        if tables:
            req = FunctionalRequirement(
                id="FR-002",
                name="交易记录查询",
                description="用户查询历史交易记录和当前状态",
                priority="P1",
                scenario="客户需要查看交易进度或历史记录",
                ui_elements=[t["name"] for t in tables[:2]],
                acceptance_criteria=[
                    "支持多维度筛选",
                    "分页展示大数据量",
                    "支持导出功能"
                ]
            )
            requirements.append(req)
        
        # 操作功能需求（基于按钮）
        for i, action in enumerate(actions[:3], 3):
            semantic = action.get("business_semantic", "操作")
            req = FunctionalRequirement(
                id=f"FR-{i:03d}",
                name=f"{semantic}功能",
                description=f"用户执行{semantic}操作",
                priority="P0" if any(kw in semantic for kw in ["提交", "确认", "保存"]) else "P1",
                scenario=f"用户需要{semantic}时",
                ui_elements=[action["name"]],
                acceptance_criteria=["操作前确认", "操作后反馈结果", "支持撤销（如适用）"]
            )
            requirements.append(req)
        
        # API驱动的隐含需求
        for api in apis:
            purpose = api.get("business_purpose")
            if purpose and not any(purpose in r.description for r in requirements):
                req = FunctionalRequirement(
                    id=f"FR-{len(requirements)+1:03d}",
                    name=f"{purpose}接口",
                    description=f"系统通过API实现{purpose}",
                    priority="P1",
                    scenario="系统内部数据处理",
                    ui_elements=[],
                    acceptance_criteria=[f"成功调用{api['endpoint']}", "正确处理响应"]
                )
                requirements.append(req)
        
        return requirements
    
    def _standardize_rules(self, raw_rules: List[Dict]) -> List[BusinessRule]:
        """标准化业务规则"""
        standardized = []
        
        for i, rule in enumerate(raw_rules, 1):
            rule_type = rule.get("rule_type", "unknown")
            expression = rule.get("expression", "")
            
            # 规则分类和命名
            if rule_type == "validation":
                name = self._infer_validation_name(expression)
                severity = "error"
            elif rule_type == "permission":
                name = "权限控制"
                severity = "error"
            elif rule_type == "flow":
                name = "流程控制"
                severity = "warning"
            else:
                name = "业务规则"
                severity = "info"
            
            # 提取相关字段
            fields = self._extract_fields_from_expression(expression)
            
            br = BusinessRule(
                id=f"BR-{i:03d}",
                name=name,
                rule_type=rule_type,
                description=rule.get("business_meaning") or expression[:100],
                expression=expression[:200] if len(expression) > 50 else expression,
                severity=severity,
                related_fields=fields
            )
            standardized.append(br)
        
        return standardized
    
    def _infer_validation_name(self, expression: str) -> str:
        """推断验证规则名称"""
        if "required" in expression:
            return "必填校验"
        if any(kw in expression for kw in ["min", "max", "length"]):
            return "长度/范围校验"
        if "pattern" in expression or "/" in expression:
            return "格式校验"
        if any(kw in expression for kw in ["email", "phone", "idcard"]):
            return "格式校验"
        return "数据校验"
    
    def _extract_fields_from_expression(self, expression: str) -> List[str]:
        """从表达式中提取字段名"""
        # 匹配常见的字段访问模式
        patterns = [
            r'this\.(\w+)',
            r'form\.(\w+)',
            r'row\.(\w+)',
            r'item\.(\w+)',
            r'(\w+)\.value',
            r'["\'](\w+)["\']',
        ]
        fields = set()
        for pattern in patterns:
            matches = re.findall(pattern, expression)
            fields.update(m for m in matches if not m.isdigit() and len(m) > 1)
        return list(fields)[:5]
    
    def _build_data_dictionary(self, data: Dict) -> List[Dict]:
        """构建数据字典"""
        dictionary = []
        
        # 从data模型提取
        data_model = data.get("data_model", {})
        for prop in data_model.get("properties", []):
            entry = {
                "field_name": prop,
                "field_type": "unknown",
                "required": False,
                "description": self._infer_field_meaning(prop),
                "source": "data_model"
            }
            dictionary.append(entry)
        
        # 从组件props推断
        for comp in data.get("components", []):
            for prop_name, prop_value in comp.get("props", {}).items():
                if "v-model" in prop_name and isinstance(prop_value, str):
                    field = prop_value.replace("this.", "").replace("form.", "")
                    if not any(d["field_name"] == field for d in dictionary):
                        dictionary.append({
                            "field_name": field,
                            "field_type": "input",
                            "required": "required" in str(comp.get("props", {})),
                            "description": comp.get("business_semantic", ""),
                            "source": "ui_binding"
                        })
        
        return dictionary
    
    def _infer_field_meaning(self, field_name: str) -> str:
        """推断字段业务含义"""
        # 常见字段名映射
        mappings = {
            "amount": "金额",
            "quantity": "数量",
            "price": "价格",
            "rate": "费率/利率",
            "type": "类型",
            "status": "状态",
            "date": "日期",
            "userId": "用户标识",
            "productId": "产品标识",
            "orderId": "订单标识",
        }
        return mappings.get(field_name, f"字段：{field_name}")
    
    def _identify_process(self, data: Dict, dimension: TradeDimension) -> Dict[str, Any]:
        """识别业务流程"""
        # 基于生命周期和组件流程推断
        lifecycle = dimension.lifecycle
        
        process_steps = []
        for phase in lifecycle:
            indicators = self.taxonomy["lifecycle"].get(phase, [])
            step = {
                "phase": phase,
                "activities": indicators[:3],
                "ui_indicators": self._find_ui_for_phase(data, phase),
                "api_indicators": self._find_api_for_phase(data, phase)
            }
            process_steps.append(step)
        
        return {
            "main_flow": process_steps,
            "alternative_flows": [],  # 简化处理
            "exception_flows": self._identify_exception_flows(data)
        }
    
    def _find_ui_for_phase(self, data: Dict, phase: str) -> List[str]:
        """查找阶段相关的UI组件"""
        phase_keywords = {
            "创建": ["form", "input", "select", "button"],
            "审核": ["audit", "approve", "reject", "detail"],
            "执行": ["confirm", "progress", "loading"],
            "清算": ["calculate", "report", "table"],
            "结算": ["result", "success", "voucher"],
        }
        keywords = phase_keywords.get(phase, [])
        components = data.get("components", [])
        return [c["name"] for c in components if any(kw in c["name"].lower() for kw in keywords)]
    
    def _find_api_for_phase(self, data: Dict, phase: str) -> List[str]:
        """查找阶段相关的API"""
        phase_patterns = {
            "创建": ["create", "add", "submit", "save"],
            "审核": ["audit", "approve", "check", "review"],
            "执行": ["execute", "process", "confirm"],
            "清算": ["clear", "settle", "calculate"],
            "结算": ["transfer", "pay", "settlement"],
        }
        patterns = phase_patterns.get(phase, [])
        apis = data.get("apis", [])
        return [a["endpoint"] for a in apis if any(p in a["endpoint"].lower() for p in patterns)]
    
    def _identify_exception_flows(self, data: Dict) -> List[Dict]:
        """识别异常流程"""
        exceptions = []
        
        # 从错误处理代码识别
        for rule in data.get("business_rules", []):
            if "catch" in rule.get("source", "") or "error" in rule.get("expression", "").lower():
                exceptions.append({
                    "trigger": rule.get("expression", "")[:50],
                    "handling": "捕获异常",
                    "ui_feedback": "错误提示"
                })
        
        # 从API响应处理识别
        for api in data.get("apis", []):
            if api.get("response_handler") and "error" in api["response_handler"].lower():
                exceptions.append({
                    "trigger": f"{api['method']} {api['endpoint']} 失败",
                    "handling": api["response_handler"][:50],
                    "ui_feedback": "操作失败提示"
                })
        
        return exceptions
    
    def _calculate_overall_confidence(self, data: Dict, dimension: TradeDimension) -> Dict[str, float]:
        """计算整体置信度"""
        scores = {
            "dimension_confidence": 0.9 if dimension.trade_type[0] != "未识别" else 0.5,
            "component_confidence": min(1.0, len(data.get("components", [])) * 0.1),
            "api_confidence": min(1.0, len(data.get("apis", [])) * 0.15),
            "rule_confidence": sum(r.get("confidence", 0.5) for r in data.get("business_rules", [])) / 
                             max(1, len(data.get("business_rules", [])))
        }
        scores["overall"] = sum(scores.values()) / len(scores)
        return scores
    
    def _generate_suggestions(self, data: Dict, dimension: TradeDimension) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 基于识别结果的建议
        if dimension.trade_type[0] == "未识别":
            suggestions.append("建议：补充交易类型标识（如文件名、常量定义）以提高识别准确度")
        
        if len(data.get("apis", [])) == 0:
            suggestions.append("警告：未识别到API调用，可能为纯展示页面或静态数据")
        
        # 基于代码质量的建议
        complexity = data.get("complexity", {})
        if complexity.get("cyclomatic_complexity", 0) > 20:
            suggestions.append("建议：页面逻辑较复杂，建议拆分为多个子组件")
        
        # 基于业务规则的建议
        rules = data.get("business_rules", [])
        validations = [r for r in rules if r.get("rule_type") == "validation"]
        if len(validations) > 10:
            suggestions.append("提示：验证规则较多，建议统一封装验证逻辑")
        
        return suggestions