# scripts/parser/react_parser.py
import re
import json
from typing import List, Dict, Any, Optional, Tuple
from .base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule


class ReactParser(BaseCodeParser):
    """
    React 组件解析器
    支持 JSX/TSX、函数组件、类组件、Hooks
    """
    
    def __init__(self, file_path: str, use_cache: bool = True):
        super().__init__(file_path, use_cache)
        self.is_typescript = file_path.endswith('.tsx') or file_path.endswith('.ts')
        self.imports = {}
        self.hooks_usage = {}
        self._extract_imports()
        self._extract_hooks()
    
    def _extract_imports(self):
        """提取导入语句"""
        try:
            # ES6 import: import { Component } from 'library'
            es6_pattern = r'import\s+\{?\s*([^}]+?)\s*\}?\s+from\s+[\'"]([^\'"]+)[\'"]'
            for match in self._safe_regex_finditer(es6_pattern, self.content, context="imports"):
                names, source = match.groups()
                for name in names.split(','):
                    self.imports[name.strip()] = source
            
            # Default import: import React from 'react'
            default_pattern = r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
            for match in self._safe_regex_finditer(default_pattern, self.content, context="imports"):
                name, source = match.groups()
                self.imports[name] = source
        except Exception as e:
            self.logger.warning(f"提取导入失败: {e}")
    
    def _extract_hooks(self):
        """提取 React Hooks 使用"""
        try:
            hooks = [
                'useState', 'useEffect', 'useContext', 'useReducer',
                'useCallback', 'useMemo', 'useRef', 'useLayoutEffect',
                'useQuery', 'useMutation', 'useInfiniteQuery'  # React Query
            ]
            
            for hook in hooks:
                pattern = rf'\b{hook}\s*\('
                count = len(self._safe_regex_findall(pattern, self.content, context=f"hook_{hook}"))
                if count > 0:
                    self.hooks_usage[hook] = count
        except Exception as e:
            self.logger.warning(f"提取 Hooks 失败: {e}")
    
    def parse(self) -> Dict[str, Any]:
        """主解析方法"""
        try:
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "react",
                    "is_typescript": self.is_typescript,
                    "size": len(self.content)
                },
                "structure": {
                    "lines_of_code": len(self.content.splitlines()),
                    "imports": self.imports,
                    "hooks_usage": self.hooks_usage,
                    "component_type": self._detect_component_type()
                },
                "components": [c.__dict__ for c in self.extract_components()],
                "apis": [a.__dict__ for a in self.extract_apis()],
                "business_rules": [r.__dict__ for r in self.extract_business_rules()],
                "state_management": self._extract_state_management(),
                "props_interface": self._extract_props_interface(),
                "complexity": self.calculate_complexity()
            }
        except Exception as e:
            self.logger.error(f"解析失败: {e}")
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "react",
                    "error": str(e)
                },
                "components": [],
                "apis": [],
                "business_rules": [],
                "complexity": {"lines_of_code": len(self.content.splitlines())}
            }
    
    def _detect_component_type(self) -> str:
        """检测组件类型"""
        try:
            # 函数组件
            if re.search(r'function\s+\w+\s*\([^)]*\)\s*\{[^}]*return\s*\(?\s*<', self.content):
                return "function_component"
            # 箭头函数组件
            if re.search(r'const\s+\w+\s*=\s*(?:\([^)]*\)|[^=]+)\s*=>\s*\{[^}]*return\s*\(?\s*<', self.content):
                return "arrow_function_component"
            # 类组件
            if re.search(r'class\s+\w+\s+extends\s+(?:React\.)?Component', self.content):
                return "class_component"
            return "unknown"
        except Exception:
            return "unknown"
    
    def extract_components(self) -> List[ParsedComponent]:
        """提取 JSX 组件"""
        components = []
        
        try:
            # 匹配 JSX 标签（包括自闭合和双标签）
            # 支持：组件名大写字母开头，或带点的组件（如 AntD.Table）
            pattern = r'<([A-Z][a-zA-Z0-9]*(?:\.[A-Z][a-zA-Z0-9]*)*)((?:\s+[^>]*)?)(/?>)'
            
            for match in self._safe_regex_finditer(pattern, self.content, context="jsx_components"):
                try:
                    tag_name = match.group(1)
                    attrs_str = match.group(2) or ""
                    is_self_closing = match.group(3) == '/>'
                    
                    attrs = self._parse_jsx_attrs(attrs_str)
                    comp_type, business_semantic = self._infer_component_type(tag_name, attrs)
                    
                    component = ParsedComponent(
                        name=tag_name,
                        type=comp_type,
                        props=attrs,
                        events=self._extract_events(attrs_str),
                        children=[],
                        source_range=(self._get_line_number(match.start()), 
                                    self._get_line_number(match.end())),
                        business_semantic=business_semantic
                    )
                    components.append(component)
                except Exception as e:
                    self.logger.debug(f"解析单个组件失败: {e}")
                    continue
        
        except Exception as e:
            self.logger.warning(f"提取组件失败: {e}")
        
        return components
    
    def _parse_jsx_attrs(self, attrs_str: str) -> Dict[str, Any]:
        """解析 JSX 属性"""
        attrs = {}
        try:
            # 支持：prop={value}、prop="value"、{...spread}
            patterns = [
                # 表达式：prop={expression}
                (r'(\w+)\s*=\s*\{([^}]+)\}', 'expression'),
                # 字符串：prop="value" 或 prop='value'
                (r'(\w+)\s*=\s*["\']([^"\']+)["\']', 'string'),
                # 布尔简写：disabled、required
                (r'\s(\w+)(?=\s|$|>)', 'boolean'),
            ]
            
            for pattern, attr_type in patterns:
                for match in self._safe_regex_finditer(pattern, attrs_str, context="jsx_attrs"):
                    try:
                        if attr_type == 'expression':
                            key, value = match.groups()
                            attrs[key] = {"type": "expression", "value": value.strip()}
                        elif attr_type == 'string':
                            key, value = match.groups()
                            attrs[key] = {"type": "string", "value": value}
                        elif attr_type == 'boolean':
                            key = match.group(1)
                            if key not in attrs:
                                attrs[key] = {"type": "boolean", "value": True}
                    except Exception:
                        continue
        except Exception as e:
            self.logger.debug(f"解析属性失败: {e}")
        
        return attrs
    
    def _extract_events(self, attrs_str: str) -> List[str]:
        """提取事件处理器"""
        try:
            # onClick={handler}、onSubmit={handleSubmit}
            return self._safe_regex_findall(r'on(\w+)\s*=\s*\{', attrs_str, context="events")
        except Exception:
            return []
    
    def _infer_component_type(self, tag: str, attrs: Dict) -> Tuple[str, Optional[str]]:
        """推断组件类型和业务语义"""
        try:
            # Ant Design 组件映射
            antd_components = {
                'Input': ('input', '文本输入'),
                'InputNumber': ('input', '数值输入'),
                'Select': ('select', '选项选择'),
                'DatePicker': ('date', '日期选择'),
                'Form': ('form', '表单容器'),
                'Table': ('table', '数据列表'),
                'Button': ('button', self._infer_button_purpose(attrs)),
                'Card': ('card', '信息卡片'),
                'Modal': ('modal', '弹窗确认'),
                'Drawer': ('drawer', '侧边面板'),
                'Tabs': ('tabs', '标签切换'),
                'Steps': ('steps', '步骤流程'),
                'Upload': ('upload', '文件上传'),
                'Radio': ('radio', '单选'),
                'Checkbox': ('checkbox', '多选'),
                'Switch': ('switch', '开关'),
            }
            
            # Material-UI 组件映射
            mui_components = {
                'TextField': ('input', '文本输入'),
                'Select': ('select', '选项选择'),
                'Button': ('button', self._infer_button_purpose(attrs)),
                'Table': ('table', '数据列表'),
                'Dialog': ('modal', '弹窗确认'),
                'Drawer': ('drawer', '侧边面板'),
            }
            
            # 处理带点的组件名（如 Form.Item）
            base_name = tag.split('.')[-1]
            
            all_mappings = {**antd_components, **mui_components}
            
            if base_name in all_mappings:
                return all_mappings[base_name]
            
            # 根据 props 推断
            if 'value' in attrs or 'defaultValue' in attrs:
                return ('custom-input', '自定义输入')
            if 'dataSource' in attrs or 'data' in attrs:
                return ('custom-table', '自定义表格')
            if 'open' in attrs or 'visible' in attrs:
                return ('custom-modal', '自定义弹窗')
            
            return ('unknown', None)
        except Exception:
            return ('unknown', None)
    
    def _infer_button_purpose(self, attrs: Dict) -> Optional[str]:
        """推断按钮用途"""
        try:
            # 从 children 或 text 推断
            type_attr = attrs.get('type', {}).get('value', '')
            if type_attr == 'primary':
                return '主要操作'
            if type_attr == 'danger':
                return '危险操作'
            
            # 尝试从代码上下文推断
            for key in ['onClick', 'htmlType']:
                if key in str(attrs):
                    handler = str(attrs.get(key, ''))
                    if any(kw in handler for kw in ['submit', 'save', 'create']):
                        return '提交操作'
                    if any(kw in handler for kw in ['delete', 'remove']):
                        return '删除操作'
                    if any(kw in handler for kw in ['search', 'query', 'filter']):
                        return '查询操作'
            
            return '通用操作'
        except Exception:
            return '通用操作'
    
    def extract_apis(self) -> List[ParsedAPI]:
        """提取 API 调用"""
        apis = []
        
        try:
            # 1. 标准 fetch
            fetch_pattern = r'fetch\s*\(\s*["\']([^"\']+)["\'](?:\s*,\s*(\{[^}]*\}))?\s*\)'
            for match in self._safe_regex_finditer(fetch_pattern, self.content, context="fetch"):
                try:
                    url, config = match.groups()
                    apis.append(ParsedAPI(
                        method="FETCH",
                        endpoint=url,
                        params=self._parse_fetch_config(config or ""),
                        response_handler=self._find_response_handler(match.end()),
                        business_purpose=self._infer_api_purpose(url, "GET")
                    ))
                except Exception:
                    continue
            
            # 2. axios
            axios_patterns = [
                (r'axios\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', 'method_first'),
                (r'axios\s*\(\s*\{[^}]*method\s*:\s*["\'](\w+)["\'][^}]*url\s*:\s*["\']([^"\']+)["\']', 'config'),
                (r'axios\s*\(\s*\{[^}]*url\s*:\s*["\']([^"\']+)["\'][^}]*method\s*:\s*["\'](\w+)["\']', 'config_reverse'),
            ]
            
            for pattern, pattern_type in axios_patterns:
                for match in self._safe_regex_finditer(pattern, self.content, context="axios"):
                    try:
                        if pattern_type == 'method_first':
                            method, url = match.groups()
                        elif pattern_type == 'config':
                            method, url = match.groups()
                        else:  # config_reverse
                            url, method = match.groups()
                        
                        apis.append(ParsedAPI(
                            method=method.upper(),
                            endpoint=url,
                            params={},
                            response_handler=self._find_response_handler(match.end()),
                            business_purpose=self._infer_api_purpose(url, method)
                        ))
                    except Exception:
                        continue
            
            # 3. React Query / TanStack Query
            rq_patterns = [
                r'useQuery\s*\(\s*(?:\[["\']?([^"\]]+)["\']?\]|\{[^}]*queryKey\s*:\s*\[["\']?([^"\]]*)["\']?\])',
                r'useMutation\s*\(\s*\{[^}]*mutationFn\s*:\s*(?:\([^)]*\)\s*=>\s*)?(\w+)',
            ]
            
            for pattern in rq_patterns:
                for match in self._safe_regex_finditer(pattern, self.content, context="react_query"):
                    try:
                        query_key = match.group(1) or match.group(2) or "unknown"
                        apis.append(ParsedAPI(
                            method="QUERY",
                            endpoint=f"react-query://{query_key}",
                            params={"queryKey": query_key},
                            response_handler=None,
                            business_purpose="数据查询"
                        ))
                    except Exception:
                        continue
        
        except Exception as e:
            self.logger.warning(f"提取 API 失败: {e}")
        
        return apis
    
    def _parse_fetch_config(self, config: str) -> Dict[str, Any]:
        """解析 fetch 配置"""
        params = {}
        try:
            method_match = self._safe_regex_search(r'method\s*:\s*["\'](\w+)["\']', config, context="fetch_method")
            if method_match:
                params['method'] = method_match.group(1)
            
            body_match = self._safe_regex_search(r'body\s*:\s*(\w+|\{[^}]*\})', config, context="fetch_body")
            if body_match:
                params['body'] = body_match.group(1)
        except Exception:
            pass
        return params
    
    def _find_response_handler(self, start_pos: int) -> Optional[str]:
        """查找 API 调用后的响应处理"""
        try:
            snippet = self.content[start_pos:start_pos+800]
            
            # .then().catch() 模式
            then_match = self._safe_regex_search(r'\.then\s*\(\s*(?:\w+|\([^)]*\)\s*=>)\s*\{([^}]+)\}', snippet, context="response_handler")
            if then_match:
                return then_match.group(1)[:150]
            
            # async/await 模式
            await_match = self._safe_regex_search(r'(?:const|let|var)\s+(\w+)\s*=\s*await', snippet, context="await_handler")
            if await_match:
                return f"await result -> {await_match.group(1)}"
            
            return None
        except Exception:
            return None
    
    def _infer_api_purpose(self, url: str, method: str) -> Optional[str]:
        """推断 API 业务用途"""
        try:
            url_lower = url.lower()
            
            # RESTful 模式
            patterns = {
                '创建资源': (['create', 'add', 'new', 'post'], ['POST']),
                '更新资源': (['update', 'modify', 'edit', 'put'], ['PUT', 'PATCH']),
                '删除资源': (['delete', 'remove', 'del'], ['DELETE']),
                '查询列表': (['list', 'query', 'search', 'get', 'fetch'], ['GET']),
                '查询详情': (['detail', 'info', 'getbyid', 'find'], ['GET']),
                '登录认证': (['login', 'auth', 'token', 'signin'], ['POST']),
                '文件上传': (['upload', 'import'], ['POST']),
                '导出下载': (['export', 'download'], ['GET']),
            }
            
            for purpose, (keywords, methods) in patterns.items():
                if any(kw in url_lower for kw in keywords) or method.upper() in methods:
                    return purpose
            
            return None
        except Exception:
            return None
    
    def extract_business_rules(self) -> List[ParsedRule]:
        """提取业务规则"""
        rules = []
        
        try:
            # 1. 表单验证（Form rules）
            validation_patterns = [
                (r'rules\s*:\s*\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\]', 'array_rules'),
                (r'required\s*:\s*(?:true|\{[^}]*\})', 'required'),
                (r'validator\s*:\s*(?:async\s+)?(?:\([^)]*\)\s*=>|\w+\s*=>)', 'custom_validator'),
                (r'pattern\s*:\s*/([^/]+)/', 'regex'),
                (r'min\s*:\s*(\d+)', 'min'),
                (r'max\s*:\s*(\d+)', 'max'),
            ]
            
            for pattern, rule_type in validation_patterns:
                for match in self._safe_regex_finditer(pattern, self.content, context=f"validation_{rule_type}"):
                    try:
                        source = match.group(0)
                        expression = match.group(1) if match.groups() else source
                        
                        rule = ParsedRule(
                            rule_type='validation',
                            expression=expression[:200],
                            source=source[:100],
                            confidence=self._calculate_rule_confidence(rule_type, source),
                            business_meaning=self._interpret_rule(rule_type, expression)
                        )
                        rules.append(rule)
                    except Exception:
                        continue
            
            # 2. 条件逻辑
            condition_patterns = [
                (r'if\s*\([^)]+\)\s*\{[^}]*\}', 'if_statement'),
                (r'ternary\s*\?[^:]+:[^;]+', 'ternary'),
                (r'(?:\w+)\s*\?\s*[^:]+\s*:\s*[^;,\n]+', 'inline_ternary'),
            ]
            
            for pattern, cond_type in condition_patterns:
                for match in self._safe_regex_finditer(pattern, self.content, context=f"condition_{cond_type}"):
                    try:
                        source = match.group(0)
                        rule = ParsedRule(
                            rule_type='flow',
                            expression=source[:200],
                            source=source[:100],
                            confidence=0.7,
                            business_meaning="流程控制"
                        )
                        rules.append(rule)
                    except Exception:
                        continue
            
            # 3. 权限检查
            permission_patterns = [
                (r'hasPermission\s*\([^)]+\)', 'hasPermission'),
                (r'checkPermission\s*\([^)]+\)', 'checkPermission'),
                (r'roles?\.includes?\s*\([^)]+\)', 'role_check'),
                (r'isAdmin|isSuperAdmin', 'admin_check'),
            ]
            
            for pattern, perm_type in permission_patterns:
                for match in self._safe_regex_finditer(pattern, self.content, context=f"permission_{perm_type}"):
                    try:
                        source = match.group(0)
                        rule = ParsedRule(
                            rule_type='permission',
                            expression=source[:200],
                            source=source[:100],
                            confidence=0.9,
                            business_meaning="权限控制"
                        )
                        rules.append(rule)
                    except Exception:
                        continue
        
        except Exception as e:
            self.logger.warning(f"提取业务规则失败: {e}")
        
        return rules
    
    def _calculate_rule_confidence(self, rule_type: str, source: str) -> float:
        """计算规则置信度"""
        base_confidence = {
            'required': 0.95,
            'regex': 0.85,
            'custom_validator': 0.80,
            'min': 0.90,
            'max': 0.90,
        }.get(rule_type, 0.70)
        
        # 根据代码质量调整
        if len(source) > 300:
            base_confidence -= 0.1
        if '//' in source or '/*' in source:
            base_confidence += 0.05
        
        return min(0.99, max(0.30, base_confidence))
    
    def _interpret_rule(self, rule_type: str, expression: str) -> Optional[str]:
        """解释规则业务含义"""
        try:
            if rule_type == 'required':
                return "必填校验"
            if rule_type == 'regex':
                return "格式校验"
            if rule_type in ['min', 'max']:
                return "范围校验"
            if rule_type == 'custom_validator':
                return "自定义校验"
            if any(kw in expression for kw in ['amount', 'money', 'price']):
                return "金额校验"
            if any(kw in expression for kw in ['date', 'time']):
                return "日期校验"
            return None
        except Exception:
            return None
    
    def _extract_state_management(self) -> Dict[str, Any]:
        """提取状态管理"""
        try:
            states = []
            
            # useState hooks
            usestate_pattern = r'const\s*\[([^,]+),\s*set(\w+)\]\s*=\s*useState\s*\(([^)]*)\)'
            for match in self._safe_regex_finditer(usestate_pattern, self.content, context="useState"):
                try:
                    state_name, setter_name, default_value = match.groups()
                    states.append({
                        "name": state_name.strip(),
                        "setter": f"set{setter_name}",
                        "default": default_value.strip() if default_value else undefined,
                        "type": "useState"
                    })
                except Exception:
                    continue
            
            # Redux / Zustand / Context
            redux_pattern = r'useSelector\s*\(\s*(?:state\s*=>|[^)]+)\s*=>\s*state\.([^.\s]+)'
            redux_slices = self._safe_regex_findall(redux_pattern, self.content, context="redux")
            
            return {
                "local_state": states,
                "redux_slices": redux_slices,
                "hooks_used": list(self.hooks_usage.keys())
            }
        except Exception as e:
            self.logger.warning(f"提取状态管理失败: {e}")
            return {"local_state": [], "redux_slices": [], "hooks_used": []}
    
    def _extract_props_interface(self) -> Optional[Dict]:
        """提取 Props 接口定义"""
        try:
            # TypeScript interface
            interface_pattern = r'interface\s+(\w+Props)\s*\{([^}]+)\}'
            match = self._safe_regex_search(interface_pattern, self.content, context="props_interface")
            if match:
                interface_name = match.group(1)
                content = match.group(2)
                # 提取字段
                fields = []
                for field_match in self._safe_regex_finditer(r'(\w+)(\?)?:\s*([^;\n]+)', content, context="interface_fields"):
                    try:
                        name, optional, type_str = field_match.groups()
                        fields.append({
                            "name": name,
                            "type": type_str.strip(),
                            "optional": bool(optional)
                        })
                    except Exception:
                        continue
                return {"name": interface_name, "fields": fields}
            
            # PropTypes
            proptypes_pattern = r'(\w+)\.propTypes\s*=\s*\{([^}]+)\}'
            pt_match = self._safe_regex_search(proptypes_pattern, self.content, context="propTypes")
            if pt_match:
                return {"type": "PropTypes", "component": pt_match.group(1)}
            
            return None
        except Exception as e:
            self.logger.warning(f"提取 Props 接口失败: {e}")
            return None
    
    def _get_line_number(self, pos: int) -> int:
        """获取字符位置对应的行号"""
        try:
            return self.content[:pos].count('\n') + 1
        except Exception:
            return 0
