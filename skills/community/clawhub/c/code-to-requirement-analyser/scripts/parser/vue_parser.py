# scripts/parser/vue_parser.py
import re
import ast
from typing import List, Dict, Any, Optional, Tuple
from .base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule


class VueParser(BaseCodeParser):
    """Vue单文件组件解析器 - 带完整错误处理"""
    
    def __init__(self, file_path: str, use_cache: bool = True):
        super().__init__(file_path, use_cache)
        self.template = ""
        self.script = ""
        self.style = ""
        self._split_sections()
        
    def _split_sections(self):
        """分割SFC三个部分（带错误处理）"""
        try:
            # 提取template
            template_match = self._safe_regex_search(
                r'<template(?:\s+[^>]*)?>(.*?)</template>',
                self.content, re.DOTALL, context="template_section"
            )
            self.template = template_match.group(1) if template_match else ""
            
            # 提取script
            script_match = self._safe_regex_search(
                r'<script(?:\s+[^>]*)?>(.*?)</script>',
                self.content, re.DOTALL, context="script_section"
            )
            self.script = script_match.group(1) if script_match else ""
            
            # 提取style（可选）
            style_match = self._safe_regex_search(
                r'<style(?:\s+[^>]*)?>(.*?)</style>',
                self.content, re.DOTALL, context="style_section"
            )
            self.style = style_match.group(1) if style_match else ""
            
        except Exception as e:
            self.logger.warning(f"分割SFC部分失败: {e}")
            # 确保至少有一些默认值
            self.template = self.template or ""
            self.script = self.script or ""
            self.style = self.style or ""
        
    def parse(self) -> Dict[str, Any]:
        """主解析方法（带完整错误处理）"""
        try:
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "vue",
                    "size": len(self.content),
                    "has_scoped_style": self._has_scoped_style()
                },
                "structure": {
                    "template_lines": len(self.template.splitlines()) if self.template else 0,
                    "script_lines": len(self.script.splitlines()) if self.script else 0,
                    "style_lines": len(self.style.splitlines()) if self.style else 0,
                    "imports": self._extract_imports(),
                    "components_used": self._extract_component_usage()
                },
                "components": [c.__dict__ for c in self.extract_components()],
                "apis": [a.__dict__ for a in self.extract_apis()],
                "business_rules": [r.__dict__ for r in self.extract_business_rules()],
                "data_model": self._extract_data_model(),
                "computed_properties": self._extract_computed(),
                "watchers": self._extract_watchers(),
                "lifecycle_hooks": self._extract_lifecycle(),
                "complexity": self.calculate_complexity()
            }
        except Exception as e:
            self.logger.error(f"Vue解析失败: {e}")
            return {
                "file_info": {
                    "path": self.file_path,
                    "type": "vue",
                    "error": str(e)
                },
                "components": [],
                "apis": [],
                "business_rules": [],
                "complexity": {"lines_of_code": len(self.content.splitlines())}
            }
    
    def _has_scoped_style(self) -> bool:
        """检查是否有 scoped style"""
        try:
            style_tag = self._safe_regex_search(r'<style[^>]*>', self.content, context="style_tag")
            return 'scoped' in (style_tag.group(0) if style_tag else '')
        except Exception:
            return False
        
    def extract_components(self) -> List[ParsedComponent]:
        """提取Vue组件（带错误处理）"""
        components = []
        
        if not self.template:
            return components
        
        try:
            # 匹配组件标签（支持自闭合和双标签）
            pattern = r'<([A-Z][a-zA-Z0-9]*|[a-z]+-[a-z-]+)(?:\s+([^>]*?))?/?>'
            
            for match in self._safe_regex_finditer(pattern, self.template, context="vue_components"):
                try:
                    tag_name = match.group(1)
                    attrs_str = match.group(2) or ""
                    attrs = self._parse_attrs(attrs_str)
                    
                    # 推断组件类型和业务语义
                    comp_type, business_semantic = self._infer_component_type(tag_name, attrs)
                    
                    component = ParsedComponent(
                        name=tag_name,
                        type=comp_type,
                        props=attrs,
                        events=self._extract_events(attrs_str),
                        children=[],  # 简化处理
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
    
    def _infer_component_type(self, tag: str, attrs: Dict) -> Tuple[str, Optional[str]]:
        """推断组件类型和业务语义"""
        try:
            # 表单组件
            form_components = {
                'el-input': ('input', '文本输入'),
                'el-input-number': ('input', '数值输入'),
                'el-select': ('select', '选项选择'),
                'el-date-picker': ('date', '日期选择'),
                'el-form': ('form', '表单容器'),
                'el-form-item': ('form-item', '表单项'),
                'a-input': ('input', '文本输入'),
                'a-input-number': ('input', '数值输入'),
                'a-select': ('select', '选项选择'),
                'a-date-picker': ('date', '日期选择'),
                'van-field': ('input', '移动端输入'),
                'van-cell': ('cell', '移动端单元格'),
            }
            
            # 表格组件
            table_components = {
                'el-table': ('table', '数据列表'),
                'el-table-column': ('column', '列表字段'),
                'a-table': ('table', '数据列表'),
                'van-list': ('list', '移动端列表'),
            }
            
            # 操作组件
            action_components = {
                'el-button': ('button', self._infer_button_purpose(attrs)),
                'a-button': ('button', self._infer_button_purpose(attrs)),
                'van-button': ('button', self._infer_button_purpose(attrs)),
                'el-dropdown': ('menu', '下拉菜单'),
                'a-dropdown': ('menu', '下拉菜单'),
            }
            
            # 展示组件
            display_components = {
                'el-card': ('card', '信息卡片'),
                'el-descriptions': ('detail', '详情展示'),
                'el-tag': ('tag', '标签'),
                'a-card': ('card', '信息卡片'),
                'van-card': ('card', '卡片'),
                'van-tag': ('tag', '标签'),
            }
            
            # 导航组件
            nav_components = {
                'el-steps': ('steps', '步骤条'),
                'el-tabs': ('tabs', '标签页'),
                'el-breadcrumb': ('breadcrumb', '面包屑'),
                'a-steps': ('steps', '步骤条'),
                'a-tabs': ('tabs', '标签页'),
            }
            
            all_types = {**form_components, **table_components, 
                        **action_components, **display_components,
                        **nav_components}
            
            if tag in all_types:
                return all_types[tag]
            
            # 自定义组件：根据props推断
            props_str = str(attrs)
            if 'v-model' in props_str or 'model-value' in props_str:
                return ('custom-input', '自定义输入组件')
            if 'data-source' in props_str or ':data' in props_str:
                return ('custom-table', '自定义表格')
            if 'visible' in props_str or 'v-model' in props_str:
                return ('custom-modal', '自定义弹窗')
            
            # 大写字母开头可能是自定义组件
            if tag and tag[0].isupper():
                return ('custom-component', '自定义组件')
                
            return ('unknown', None)
        except Exception:
            return ('unknown', None)
    
    def _infer_button_purpose(self, attrs: Dict) -> Optional[str]:
        """推断按钮用途"""
        try:
            # 从 type 属性推断
            btn_type = attrs.get('type', {}).get('value', '') if isinstance(attrs.get('type'), dict) else ''
            if btn_type == 'primary':
                return '主要操作'
            if btn_type == 'danger':
                return '危险操作'
            if btn_type == 'text':
                return '文字链接'
            
            # 从文本推断
            text = attrs.get('text', '') or attrs.get('slot-default', '')
            text_lower = str(text).lower()
            
            purposes = [
                (['提交', '保存', '确认', 'submit', 'save', 'confirm'], '提交操作'),
                (['查询', '搜索', 'search', 'query'], '查询操作'),
                (['新增', '添加', 'create', 'add', 'new'], '新增操作'),
                (['删除', '移除', 'delete', 'remove'], '删除操作'),
                (['导出', '下载', 'export', 'download'], '导出操作'),
                (['导入', '上传', 'upload', 'import'], '上传操作'),
                (['编辑', '修改', 'edit', 'modify'], '编辑操作'),
                (['取消', '关闭', 'cancel', 'close'], '取消操作'),
                (['打印', 'print'], '打印操作'),
                (['重置', 'reset', 'clear'], '重置操作'),
            ]
            
            for keywords, purpose in purposes:
                if any(kw in text_lower for kw in keywords):
                    return purpose
            
            return '通用操作'
        except Exception:
            return '通用操作'
    
    def extract_apis(self) -> List[ParsedAPI]:
        """提取API调用（带错误处理）"""
        apis = []
        
        if not self.script:
            return apis
        
        try:
            # 匹配this.$http/axios/fetch调用
            patterns = [
                # this.$http.get(url, config)
                (r'this\.\$http\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"](?:,\s*([^)]+))?\)', 
                 'vue-http'),
                # axios.request(config) with method
                (r'axios\.(request|get|post|put|delete|patch)\(([^)]+)\)', 
                 'axios'),
                # axios({ method, url })
                (r'axios\s*\(\s*\{[^}]*method\s*:\s*[\'"](\w+)[\'"][^}]*url\s*:\s*[\'"]([^\'"]+)[\'"]', 
                 'axios-config'),
                # fetch(url, config)
                (r'fetch\s*\([\'"]([^\'"]+)[\'"](?:,\s*([^)]+))?\)', 
                 'fetch'),
            ]
            
            for pattern, api_type in patterns:
                for match in self._safe_regex_finditer(pattern, self.script, context=f"api_{api_type}"):
                    try:
                        if api_type == 'vue-http':
                            method, url, config = match.groups()
                            config = config or ""
                        elif api_type == 'axios':
                            method, args = match.groups()
                            url = self._extract_url_from_args(args)
                            config = args
                        elif api_type == 'axios-config':
                            method, url = match.groups()
                            config = ""
                        else:  # fetch
                            url, config = match.groups()
                            method = 'GET'
                            config = config or ""
                        
                        # 解析参数
                        params = self._extract_params_from_config(config)
                        
                        # 查找响应处理
                        response_handler = self._find_response_handler(match.end())
                        
                        api = ParsedAPI(
                            method=method.upper(),
                            endpoint=url,
                            params=params,
                            response_handler=response_handler,
                            business_purpose=self._infer_api_purpose(url, method)
                        )
                        apis.append(api)
                    except Exception as e:
                        self.logger.debug(f"解析单个API失败: {e}")
                        continue
        except Exception as e:
            self.logger.warning(f"提取API失败: {e}")
        
        return apis
    
    def _extract_url_from_args(self, args: str) -> str:
        """从axios参数提取URL"""
        try:
            # 尝试匹配url属性
            url_match = self._safe_regex_search(r'url\s*:\s*[\'"]([^\'"]+)[\'"]', args, context="axios_url")
            if url_match:
                return url_match.group(1)
            # 尝试匹配第一个字符串参数
            str_match = self._safe_regex_search(r'[\'"]([^\'"]+)[\'"]', args, context="axios_string_arg")
            return str_match.group(1) if str_match else "unknown"
        except Exception:
            return "unknown"
    
    def _infer_api_purpose(self, url: str, method: str) -> Optional[str]:
        """推断API业务用途"""
        try:
            url_lower = url.lower()
            method_upper = method.upper()
            
            # RESTful模式识别
            patterns = [
                (['create', 'add', 'new', 'insert'], ['POST'], '创建资源'),
                (['update', 'modify', 'edit', 'save'], ['PUT', 'PATCH', 'POST'], '更新资源'),
                (['delete', 'remove', 'del'], ['DELETE', 'POST'], '删除资源'),
                (['list', 'query', 'search', 'get', 'find', 'page'], ['GET', 'POST'], '查询列表'),
                (['detail', 'info', 'getbyid', 'one'], ['GET', 'POST'], '查询详情'),
                (['dict', 'enum', 'options', 'select'], ['GET'], '获取字典'),
                (['login', 'auth', 'token', 'sign'], ['POST'], '登录认证'),
                (['upload', 'import', 'file'], ['POST'], '文件上传'),
                (['download', 'export'], ['GET', 'POST'], '导出下载'),
            ]
            
            for keywords, methods, purpose in patterns:
                if any(kw in url_lower for kw in keywords) or method_upper in methods:
                    return purpose
            
            # 交易特定模式
            if any(kw in url_lower for kw in ['trade', 'order', 'transaction', 'buy', 'sell']):
                return '交易操作'
            if any(kw in url_lower for kw in ['audit', 'approve', 'check', 'review']):
                return '审核操作'
            if any(kw in url_lower for kw in ['settlement', 'clear', 'settle']):
                return '清算结算'
            if any(kw in url_lower for kw in ['fund', 'product']):
                return '产品操作'
                
            return None
        except Exception:
            return None
    
    def extract_business_rules(self) -> List[ParsedRule]:
        """提取业务规则（带错误处理）"""
        rules = []
        
        if not self.script:
            return rules
        
        try:
            # 1. 提取验证规则（表单验证）
            validation_patterns = [
                (r'rules\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', 'object'),
                (r'validator\s*:\s*([^,}\]]+)', 'function'),
                (r'required\s*:\s*true', 'required'),
                (r'pattern\s*:\s*\/([^\/]+)\/', 'regex'),
                (r'min\s*:\s*(\d+)', 'min'),
                (r'max\s*:\s*(\d+)', 'max'),
            ]
            
            # 2. 提取条件逻辑
            condition_patterns = [
                (r'if\s*\(([^)]+)\)\s*\{', 'condition'),
                (r'switch\s*\(([^)]+)\)', 'switch'),
                (r'\?([^:]+):', 'ternary'),
            ]
            
            # 3. 提取权限控制
            permission_patterns = [
                (r'v-if=["\'][^"\']*(?:permission|auth|role)[^"\']*["\']', 'permission-directive'),
                (r'checkPermission\([^)]+?\)', 'permission-check'),
                (r'hasRole\([^)]+?\)', 'role-check'),
                (r'hasPermission\([^)]+?\)', 'permission-check'),
            ]
            
            for pattern, rule_type in validation_patterns + condition_patterns + permission_patterns:
                for match in self._safe_regex_finditer(pattern, self.script, context=f"rule_{rule_type}"):
                    try:
                        source = match.group(0)
                        expression = match.group(1) if match.groups() else source
                        
                        rule = ParsedRule(
                            rule_type=self._categorize_rule(rule_type, source),
                            expression=expression[:200],
                            source=source[:100],
                            confidence=self._calculate_rule_confidence(rule_type, source),
                            business_meaning=self._interpret_rule(rule_type, expression)
                        )
                        rules.append(rule)
                    except Exception as e:
                        self.logger.debug(f"解析单个规则失败: {e}")
                        continue
        except Exception as e:
            self.logger.warning(f"提取业务规则失败: {e}")
        
        return rules
    
    def _categorize_rule(self, rule_type: str, source: str) -> str:
        """分类规则类型"""
        try:
            if rule_type in ['object', 'function', 'required', 'regex', 'min', 'max']:
                return 'validation'
            if rule_type in ['condition', 'switch', 'ternary']:
                return 'flow'
            if 'permission' in rule_type or 'role' in rule_type:
                return 'permission'
            return 'unknown'
        except Exception:
            return 'unknown'
    
    def _interpret_rule(self, rule_type: str, expression: str) -> Optional[str]:
        """解释规则的业务含义"""
        try:
            expr_lower = expression.lower()
            if 'required' in expr_lower:
                return "必填校验"
            if any(kw in expr_lower for kw in ['amount', 'money', 'price', 'sum']):
                return "金额相关规则"
            if any(kw in expr_lower for kw in ['date', 'time', 'datetime']):
                return "日期时间规则"
            if any(kw in expr_lower for kw in ['status', 'state']):
                return "状态判断规则"
            if rule_type == 'regex':
                return "格式校验"
            if rule_type in ['min', 'max']:
                return "范围校验"
            return None
        except Exception:
            return None
    
    def _calculate_rule_confidence(self, rule_type: str, source: str) -> float:
        """计算规则提取的置信度"""
        try:
            base_confidence = {
                'required': 0.95,
                'regex': 0.85,
                'condition': 0.70,
                'permission-directive': 0.90,
                'min': 0.90,
                'max': 0.90,
            }.get(rule_type, 0.60)
            
            # 根据代码清晰度调整
            if len(source) > 200:
                base_confidence -= 0.1
            if '/*' in source or '//' in source:
                base_confidence += 0.05
            
            return min(0.99, max(0.30, base_confidence))
        except Exception:
            return 0.60
    
    def _extract_data_model(self) -> Dict[str, Any]:
        """提取数据模型（带错误处理）"""
        try:
            # 匹配data() { return {...} } 或 data: () => ({...})
            pattern = r'(?:data\s*\(\)\s*\{|data\s*:\s*(?:function|\(\)\s*=>)\s*\{)\s*return\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
            match = self._safe_regex_search(pattern, self.script, context="data_model")
            
            if match:
                data_content = match.group(1)
                # 提取顶级属性
                props = self._safe_regex_findall(r'(\w+)\s*:\s*', data_content, context="data_props")
                return {"properties": props[:20], "raw_preview": data_content[:500]}
            return {}
        except Exception as e:
            self.logger.warning(f"提取数据模型失败: {e}")
            return {}
    
    def _extract_computed(self) -> List[Dict]:
        """计算属性（带错误处理）"""
        try:
            pattern = r'computed\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
            match = self._safe_regex_search(pattern, self.script, context="computed")
            if match:
                content = match.group(1)
                properties = self._safe_regex_findall(r'(\w+)\s*\(\s*\)\s*\{', content, context="computed_props")
                return [{"name": p, "type": "computed"} for p in properties[:20]]
            return []
        except Exception as e:
            self.logger.warning(f"提取计算属性失败: {e}")
            return []
    
    def _extract_watchers(self) -> List[Dict]:
        """监听器（带错误处理）"""
        try:
            pattern = r'watch\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
            match = self._safe_regex_search(pattern, self.script, context="watch")
            if match:
                content = match.group(1)
                watchers = self._safe_regex_findall(r'[\'"]?(\w+)[\'"]?\s*:', content, context="watch_targets")
                return [{"target": w, "type": "watcher"} for w in watchers[:20]]
            return []
        except Exception as e:
            self.logger.warning(f"提取监听器失败: {e}")
            return []
    
    def _extract_lifecycle(self) -> List[str]:
        """生命周期钩子（带错误处理）"""
        try:
            hooks = ['created', 'mounted', 'updated', 'destroyed', 
                    'beforeCreate', 'beforeMount', 'beforeUpdate', 'beforeDestroy',
                    'activated', 'deactivated', 'errorCaptured']
            found = []
            for hook in hooks:
                if self._safe_regex_search(rf'\b{hook}\s*\(', self.script, context=f"lifecycle_{hook}"):
                    found.append(hook)
            return found
        except Exception as e:
            self.logger.warning(f"提取生命周期失败: {e}")
            return []
    
    def _parse_attrs(self, attrs_str: str) -> Dict[str, Any]:
        """解析HTML属性（带错误处理）"""
        attrs = {}
        try:
            # 匹配 :prop="value" 或 prop="value" 或 @event="handler"
            pattern = r'([:@]?)(\w+(?:-\w+)*)\s*=\s*["\']([^"\']+)["\']'
            for match in self._safe_regex_finditer(pattern, attrs_str, context="attrs"):
                try:
                    prefix, name, value = match.groups()
                    key = f"{prefix}{name}"
                    attrs[key] = value
                except Exception:
                    continue
        except Exception as e:
            self.logger.debug(f"解析属性失败: {e}")
        return attrs
    
    def _extract_events(self, attrs_str: str) -> List[str]:
        """提取事件绑定（带错误处理）"""
        try:
            return self._safe_regex_findall(r'@(\w+)', attrs_str, context="events")
        except Exception:
            return []
    
    def _extract_imports(self) -> List[Dict]:
        """提取导入的依赖（带错误处理）"""
        try:
            imports = self._safe_regex_findall(
                r'import\s+\{?([^}]+)\}?\s+from\s+[\'"]([^\'"]+)[\'"]', 
                self.script, context="imports"
            )
            return [{"name": i[0].strip(), "source": i[1]} for i in imports[:20]]
        except Exception as e:
            self.logger.warning(f"提取导入失败: {e}")
            return []
    
    def _extract_component_usage(self) -> List[str]:
        """提取components注册（带错误处理）"""
        try:
            match = self._safe_regex_search(r'components\s*:\s*\{([^}]+)\}', self.script, context="components")
            if match:
                return [c.strip() for c in match.group(1).split(',') if c.strip()][:20]
            return []
        except Exception as e:
            self.logger.warning(f"提取组件注册失败: {e}")
            return []
    
    def _get_line_number(self, pos: int) -> int:
        """获取字符位置对应的行号"""
        try:
            return self.content[:pos].count('\n') + 1
        except Exception:
            return 0
    
    def _extract_params_from_config(self, config: str) -> Dict[str, Any]:
        """从配置字符串提取参数（带错误处理）"""
        params = {}
        try:
            matches = self._safe_regex_findall(r'(\w+)\s*:\s*([^,]+)', config, context="params")
            for key, value in matches[:5]:
                params[key] = value.strip()
        except Exception:
            pass
        return params
    
    def _find_response_handler(self, start_pos: int) -> Optional[str]:
        """查找API调用后的响应处理（带错误处理）"""
        try:
            snippet = self.script[start_pos:start_pos+500]
            
            then_match = self._safe_regex_search(r'\.then\s*\([^)]*=\s*>?\s*\{([^}]+)\}', snippet, context="then_handler")
            if then_match:
                return then_match.group(1)[:100]
            
            catch_match = self._safe_regex_search(r'\.catch\s*\([^)]*=\s*>?\s*\{([^}]+)\}', snippet, context="catch_handler")
            if catch_match:
                return f"Error: {catch_match.group(1)[:50]}"
            
            return None
        except Exception:
            return None
