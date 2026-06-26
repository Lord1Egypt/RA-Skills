# scripts/parser/angular_parser.py
from typing import List, Dict, Any, Optional
from .base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule


class AngularParser(BaseCodeParser):
    """
    Angular 组件解析器
    支持 .component.ts 和 .component.html 文件
    """
    
    def __init__(self, file_path: str, use_cache: bool = True):
        super().__init__(file_path, use_cache)
        self.is_template = file_path.endswith('.html')
        self.decorators = {}
        self._extract_decorators()
    
    def _extract_decorators(self):
        """提取装饰器元数据"""
        try:
            if self.is_template:
                return
            
            # @Component({...})
            component_pattern = r'@Component\s*\(\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}\s*\)'
            match = self._safe_regex_search(component_pattern, self.content, context="component_decorator")
            if match:
                self.decorators['Component'] = match.group(1)
            
            # @Input(), @Output(), @ViewChild() 等
            property_patterns = [
                (r'@Input\s*(?:\(\s*["\']?([^"\']*)["\']?\s*\))?', 'Input'),
                (r'@Output\s*\(\s*\)', 'Output'),
                (r'@ViewChild\s*\([^)]+\)', 'ViewChild'),
                (r'@Inject\s*\([^)]+\)', 'Inject'),
            ]
            
            for pattern, name in property_patterns:
                matches = self._safe_regex_findall(pattern, self.content, context=f"decorator_{name}")
                if matches:
                    self.decorators[name] = matches
        
        except Exception as e:
            self.logger.warning(f"提取装饰器失败: {e}")
    
    def parse(self) -> Dict[str, Any]:
        """主解析方法"""
        try:
            if self.is_template:
                return self._parse_template()
            else:
                return self._parse_component()
        except Exception as e:
            self.logger.error(f"Angular解析失败: {e}")
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "angular",
                    "is_template": self.is_template,
                    "error": str(e)
                },
                "components": [],
                "apis": [],
                "business_rules": [],
                "complexity": {"lines_of_code": len(self.content.splitlines())}
            }
    
    def _parse_component(self) -> Dict[str, Any]:
        """解析 TypeScript 组件文件"""
        try:
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "angular",
                    "is_template": False,
                    "has_component": 'Component' in self.decorators
                },
                "structure": {
                    "lines_of_code": len(self.content.splitlines()),
                    "decorators": list(self.decorators.keys()),
                    "imports": self._extract_imports(),
                    "class_name": self._extract_class_name()
                },
                "components": [c.__dict__ for c in self.extract_components()],
                "apis": [a.__dict__ for a in self.extract_apis()],
                "business_rules": [r.__dict__ for r in self.extract_business_rules()],
                "inputs": self._extract_inputs(),
                "outputs": self._extract_outputs(),
                "injections": self._extract_injections(),
                "complexity": self.calculate_complexity()
            }
        except Exception as e:
            self.logger.warning(f"解析组件文件失败: {e}")
            return {"error": str(e)}
    
    def _parse_template(self) -> Dict[str, Any]:
        """解析 HTML 模板文件"""
        try:
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "angular",
                    "is_template": True
                },
                "structure": {
                    "template_lines": len(self.content.splitlines())
                },
                "components": [c.__dict__ for c in self.extract_components()],
                "bindings": self._extract_template_bindings(),
                "directives": self._extract_directives(),
                "pipes": self._extract_pipes(),
                "complexity": self.calculate_complexity()
            }
        except Exception as e:
            self.logger.warning(f"解析模板文件失败: {e}")
            return {"error": str(e)}
    
    def extract_components(self) -> List[ParsedComponent]:
        """提取 Angular 组件/指令"""
        components = []
        
        try:
            if self.is_template:
                # 解析 HTML 模板中的组件
                pattern = r'<([a-z]+-[a-z-]+|mat-[a-z-]+)(?:\s+([^>]*?))?/?>'
                
                for match in self._safe_regex_finditer(pattern, self.content, context="angular_components"):
                    try:
                        tag_name = match.group(1)
                        attrs_str = match.group(2) or ""
                        attrs = self._parse_attrs(attrs_str)
                        
                        comp_type, business_semantic = self._infer_angular_component(tag_name)
                        
                        component = ParsedComponent(
                            name=tag_name,
                            type=comp_type,
                            props=attrs,
                            events=self._extract_angular_events(attrs_str),
                            children=[],
                            source_range=(self._get_line_number(match.start()), 
                                        self._get_line_number(match.end())),
                            business_semantic=business_semantic
                        )
                        components.append(component)
                    except Exception:
                        continue
        except Exception as e:
            self.logger.warning(f"提取组件失败: {e}")
        
        return components
    
    def _infer_angular_component(self, tag: str) -> tuple:
        """推断 Angular 组件类型"""
        try:
            material_components = {
                'mat-form-field': ('form-field', '表单字段'),
                'mat-input': ('input', '文本输入'),
                'mat-select': ('select', '选项选择'),
                'mat-datepicker': ('date', '日期选择'),
                'mat-table': ('table', '数据列表'),
                'mat-button': ('button', '按钮'),
                'mat-card': ('card', '卡片'),
                'mat-dialog': ('dialog', '弹窗'),
                'mat-tab': ('tab', '标签页'),
                'mat-stepper': ('stepper', '步骤条'),
            }
            
            if tag in material_components:
                return material_components[tag]
            
            # 自定义组件 (app-xxx)
            if tag.startswith('app-'):
                return ('custom-component', '应用组件')
            
            return ('unknown', None)
        except Exception:
            return ('unknown', None)
    
    def extract_apis(self) -> List[ParsedAPI]:
        """提取 Angular HTTP 调用"""
        apis = []
        
        try:
            if self.is_template:
                return apis
            
            # 依赖注入的 HttpClient
            http_patterns = [
                r'this\.http\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                r'\.subscribe\s*\(',
                r'\.pipe\s*\(',
            ]
            
            for pattern in http_patterns[:1]:
                for match in self._safe_regex_finditer(pattern, self.content, context="angular_http"):
                    try:
                        method, url = match.groups()
                        apis.append(ParsedAPI(
                            method=method.upper(),
                            endpoint=url,
                            params={},
                            response_handler=None,
                            business_purpose=self._infer_api_purpose(url, method)
                        ))
                    except Exception:
                        continue
        except Exception as e:
            self.logger.warning(f"提取 API 失败: {e}")
        
        return apis
    
    def extract_business_rules(self) -> List[ParsedRule]:
        """提取业务规则"""
        rules = []
        
        try:
            if self.is_template:
                # 模板中的验证规则
                validation_pattern = r'required|minlength|maxlength|pattern|email'
                matches = self._safe_regex_findall(validation_pattern, self.content, context="template_validation")
                for match in set(matches):
                    rules.append(ParsedRule(
                        rule_type='validation',
                        expression=match,
                        source=match,
                        confidence=0.85,
                        business_meaning=f"模板验证: {match}"
                    ))
            else:
                # TypeScript 中的验证
                validators_pattern = r'Validators\.(required|minLength|maxLength|pattern|email|compose)'
                for match in self._safe_regex_finditer(validators_pattern, self.content, context="ts_validators"):
                    try:
                        validator = match.group(1)
                        rules.append(ParsedRule(
                            rule_type='validation',
                            expression=validator,
                            source=match.group(0),
                            confidence=0.90,
                            business_meaning=f"表单验证: {validator}"
                        ))
                    except Exception:
                        continue
        except Exception as e:
            self.logger.warning(f"提取业务规则失败: {e}")
        
        return rules
    
    def _extract_imports(self) -> List[Dict]:
        """提取导入"""
        try:
            imports = self._safe_regex_findall(
                r'import\s+\{?([^}]+)\}?\s+from\s+[\'"]([^\'"]+)[\'"]',
                self.content, context="imports"
            )
            return [{"name": i[0].strip(), "source": i[1]} for i in imports[:15]]
        except Exception:
            return []
    
    def _extract_class_name(self) -> Optional[str]:
        """提取类名"""
        try:
            match = self._safe_regex_search(r'export\s+class\s+(\w+)', self.content, context="class_name")
            return match.group(1) if match else None
        except Exception:
            return None
    
    def _extract_inputs(self) -> List[Dict]:
        """提取 @Input 属性"""
        try:
            pattern = r'@Input\s*(?:\(\s*["\']?([^"\']*)["\']?\s*\))?\s+(\w+)'
            matches = self._safe_regex_findall(pattern, self.content, context="inputs")
            return [{"name": m[1], "alias": m[0] or None} for m in matches]
        except Exception:
            return []
    
    def _extract_outputs(self) -> List[Dict]:
        """提取 @Output 事件"""
        try:
            pattern = r'@Output\s*\(\s*\)\s+(\w+)\s*=\s*new\s+EventEmitter'
            matches = self._safe_regex_findall(pattern, self.content, context="outputs")
            return [{"name": m} for m in matches]
        except Exception:
            return []
    
    def _extract_injections(self) -> List[Dict]:
        """提取依赖注入"""
        try:
            # constructor(private http: HttpClient)
            pattern = r'constructor\s*\(([^)]+)\)'
            match = self._safe_regex_search(pattern, self.content, context="constructor")
            if match:
                params = match.group(1)
                injections = []
                for param in params.split(','):
                    parts = param.strip().split(':')
                    if len(parts) == 2:
                        injections.append({
                            "name": parts[0].replace('private ', '').replace('public ', '').strip(),
                            "type": parts[1].strip()
                        })
                return injections
            return []
        except Exception:
            return []
    
    def _extract_template_bindings(self) -> List[Dict]:
        """提取模板绑定"""
        try:
            bindings = []
            # [(ngModel)]="property"
            ngmodel_pattern = r'\[\(ngModel\)\]\s*=\s*["\']([^"\']+)["\']'
            for match in self._safe_regex_finditer(ngmodel_pattern, self.content, context="ngmodel_bindings"):
                bindings.append({"type": "two-way", "target": match.group(1), "directive": "ngModel"})
            
            # [property]="expression"
            property_pattern = r'\[(\w+)\]\s*=\s*["\']([^"\']+)["\']'
            for match in self._safe_regex_finditer(property_pattern, self.content, context="property_bindings"):
                bindings.append({"type": "property", "name": match.group(1), "value": match.group(2)})
            
            # (event)="handler()"
            event_pattern = r'\((\w+)\)\s*=\s*["\']([^"\']+)["\']'
            for match in self._safe_regex_finditer(event_pattern, self.content, context="event_bindings"):
                bindings.append({"type": "event", "name": match.group(1), "handler": match.group(2)})
            
            return bindings
        except Exception:
            return []
    
    def _extract_directives(self) -> List[str]:
        """提取使用的指令"""
        try:
            directives = []
            structural = self._safe_regex_findall(r'\*ngIf|ngIf|ngFor|ngSwitch', self.content, context="structural_directives")
            directives.extend(structural)
            return list(set(directives))
        except Exception:
            return []
    
    def _extract_pipes(self) -> List[str]:
        """提取使用的管道"""
        try:
            pipes = self._safe_regex_findall(r'\|\s*(\w+)', self.content, context="pipes")
            return list(set(pipes))
        except Exception:
            return []
    
    def _parse_attrs(self, attrs_str: str) -> Dict[str, Any]:
        """解析 HTML 属性"""
        attrs = {}
        try:
            pattern = r'([\[\(]?)(\w+)([\]\)]?)\s*=\s*["\']([^"\']+)["\']'
            for match in self._safe_regex_finditer(pattern, attrs_str, context="angular_attrs"):
                prefix, name, suffix, value = match.groups()
                key = f"{prefix}{name}{suffix}"
                attrs[key] = value
        except Exception:
            pass
        return attrs
    
    def _extract_angular_events(self, attrs_str: str) -> List[str]:
        """提取 Angular 事件绑定"""
        try:
            return self._safe_regex_findall(r'\((\w+)\)', attrs_str, context="angular_events")
        except Exception:
            return []
    
    def _infer_api_purpose(self, url: str, method: str) -> Optional[str]:
        """推断 API 用途"""
        try:
            url_lower = url.lower()
            if 'api/' in url_lower:
                parts = url.split('/')
                return f"API调用: {parts[-1] if parts else 'unknown'}"
            return None
        except Exception:
            return None
    
    def _get_line_number(self, pos: int) -> int:
        """获取行号"""
        try:
            return self.content[:pos].count('\n') + 1
        except Exception:
            return 0
