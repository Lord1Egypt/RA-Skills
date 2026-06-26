#!/usr/bin/env python3
"""
collectors/adapters/builtin/api_docs/kimi.py - Kimi API 文档适配器

支持: platform.kimi.com, api.moonshot.cn

能力:
- API 端点提取（路径/方法/描述）
- 参数列表（名称/类型/必填/描述）
- 请求/响应示例
- 代码示例（curl/Python）
- 模型列表

Task 4: 实现 Kimi API 文档识别能力
"""

import re
import sys
import json
from typing import List, Optional, Dict, Any, Tuple, Callable
from dataclasses import dataclass, field
from pathlib import Path

# 导入 Task 1 建立的基础设施
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from collectors.adapters.base import DocAdapter, register_adapter
from collectors.adapters.extraction.structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
    ApiEndpoint,
    ModelInfo,
)


@dataclass
class ApiParameter:
    """API参数"""
    name: str
    param_type: str
    required: bool
    description: str
    default: Optional[str] = None
    enum_values: Optional[List[str]] = None
    location: str = 'body'  # body, query, path, header


@dataclass
class ApiExample:
    """API示例"""
    title: str
    request: str  # JSON 格式
    response: str  # JSON 格式
    code_snippet: Optional[str] = None  # 代码片段（如 curl, Python）


@dataclass
class KimiApiEndpoint:
    """Kimi API 端点"""
    path: str
    method: str
    description: str
    endpoint_id: str  # 唯一标识
    parameters: List[ApiParameter] = field(default_factory=list)
    request_example: Optional[str] = None
    response_example: Optional[str] = None
    code_examples: List[str] = field(default_factory=list)
    rate_limit: Optional[str] = None  # 如 "60 requests/min"
    authentication: str = "Bearer Token"
    tags: List[str] = field(default_factory=list)


@dataclass
class KimiApiDoc:
    """Kimi API 文档（完整）"""
    title: str
    base_url: str = "https://api.moonshot.cn"
    version: str = "v1"
    endpoints: List[KimiApiEndpoint] = field(default_factory=list)
    models: List[ModelInfo] = field(default_factory=list)
    authentication: str = "Authorization: Bearer <api_key>"


class KimiApiAdapter(DocAdapter):
    """Kimi API 文档适配器"""
    
    # 适配器标识
    name = 'kimi_api'
    platform = 'kimi'

    # 支持的域名
    supported_domains = [
        'platform.kimi.com',
        'kimi.moonshot.cn',
        'api.moonshot.cn',
        'www.moonshot.cn',
    ]

    # Kimi API 端点 CSS 选择器
    SELECTORS = {
        # 端点卡片
        'endpoint_card': [
            '.api-endpoint',
            '.endpoint-item',
            '[class*="endpoint"]',
            '.method-path',
            '.operation-item',
            '[data-path]',
        ],
        
        # 路径
        'path': [
            '.endpoint-path',
            '.api-path',
            'code.path',
            '[class*="path"]',
            '.operation-path',
            'td.path',
        ],
        
        # 方法
        'method': [
            '.http-method',
            '.method-badge',
            '[class*="method"]',
            '.badge-get',
            '.badge-post',
            '.operation-method',
            'span.method',
        ],
        
        # 描述
        'description': [
            '.endpoint-description',
            '.api-description',
            '[class*="description"]',
            '.operation-description',
            'td.summary',
        ],
        
        # 参数表格
        'param_table': [
            '.param-table',
            '.parameters-table',
            'table.params',
            '[class*="param"] table',
            '.schema-table',
            '.arguments-table',
        ],
        
        # 示例代码
        'code_example': [
            '.code-example',
            '.example-code',
            'pre.code',
            '[class*="example"] pre',
            '.curl-example',
            '.python-example',
        ],
        
        # 模型列表
        'model_item': [
            '.model-item',
            '.model-card',
            '[class*="model"]',
            '.model-schema',
        ],
        
        # 侧边栏导航
        'sidebar_nav': [
            '.sidebar-nav',
            '.api-nav',
            '[class*="nav"]',
            '.endpoint-nav',
        ],
        
        # 请求体
        'request_body': [
            '.request-body',
            '.request-schema',
            '[class*="request-body"]',
        ],
        
        # 响应
        'response': [
            '.response',
            '.response-schema',
            '[class*="response"]',
        ],
    }

    # HTTP 方法颜色映射
    METHOD_COLORS = {
        'GET': 'green',
        'POST': 'blue',
        'PUT': 'orange',
        'DELETE': 'red',
        'PATCH': 'purple',
    }

    # 已知 Kimi API 端点模式（用于识别）
    KNOWN_PATTERNS = [
        # 聊天补全
        (r'/v1/chat/completions', 'POST', '聊天补全', ['chat']),
        # 模型
        (r'/v1/models', 'GET', '获取模型列表', ['models']),
        (r'/v1/models/([\w\-]+)', 'GET', '获取特定模型信息', ['models']),
        # 文件
        (r'/v1/files', 'POST', '上传文件', ['files']),
        (r'/v1/files/([\w\-]+)', 'GET', '获取文件信息', ['files']),
        (r'/v1/files/([\w\-]+)/content', 'GET', '获取文件内容', ['files']),
        # 消息
        (r'/v1/chat/([\w\-]+)/messages', 'GET', '获取消息列表', ['chat', 'messages']),
        # 嵌入
        (r'/v1/embeddings', 'POST', '文本嵌入', ['embeddings']),
        (r'/v1/embedding', 'POST', '文本嵌入(旧)', ['embeddings']),
    ]

    def __init__(self):
        super().__init__()
        self.platform_hosts = self.supported_domains

    @property
    def platform(self) -> str:
        return 'kimi'

    def can_handle(self, url: str) -> bool:
        """检查是否支持此URL"""
        return any(host in url for host in self.supported_domains)

    def extract(self, page, url: str) -> DocumentItem:
        """
        提取 Kimi API 文档

        Args:
            page: Playwright Page对象
            url: 文档URL

        Returns:
            DocumentItem: 结构化文档数据
        """
        # 1. 提取基本信息
        title = self._extract_title(page)

        # 2. 提取端点
        endpoints = self.extract_api_endpoints(page)

        # 3. 提取模型列表
        models = self.extract_models_list(page)

        # 4. 提取代码示例
        code_examples = self._extract_code_examples(page)

        # 5. 构建文档内容
        content = self._build_markdown(endpoints, models)

        # 6. 构建 TOC
        toc = self._build_toc(endpoints)

        return DocumentItem(
            url=url,
            title=title,
            author='Kimi (Moonshot)',
            publish_date=None,
            version='v1',
            toc=toc,
            content=content,
            code_blocks=code_examples,
            tables=[],
            images=[],
            breadcrumbs=self.extract_breadcrumbs(page),
            metadata={
                'platform': 'kimi',
                'base_url': 'https://api.moonshot.cn',
                'endpoints_count': len(endpoints),
                'models_count': len(models),
            }
        )

    def extract_api_endpoints(self, page) -> List[KimiApiEndpoint]:
        """提取 API 端点列表"""
        endpoints = []

        # 方法1：从页面结构提取
        endpoint_cards = self._find_endpoint_cards(page)

        for card in endpoint_cards:
            try:
                endpoint = self._parse_endpoint_card(card)
                if endpoint:
                    endpoints.append(endpoint)
            except Exception:
                continue

        # 方法2：从已知模式匹配（兜底）
        if not endpoints:
            endpoints = self._extract_from_known_patterns(page)

        return endpoints

    def _find_endpoint_cards(self, page) -> List:
        """查找端点卡片元素"""
        cards = []

        for selector in self.SELECTORS.get('endpoint_card', []):
            try:
                found = page.locator(selector).all()
                if found:
                    cards.extend(found)
            except Exception:
                continue

        return cards

    def _parse_endpoint_card(self, card) -> Optional[KimiApiEndpoint]:
        """解析端点卡片"""
        try:
            # 提取路径
            path = self._extract_path(card)
            if not path:
                return None

            # 提取方法
            method = self._extract_method(card)

            # 提取描述
            description = self._extract_description(card)

            # 提取端点ID
            endpoint_id = self._generate_endpoint_id(path, method)

            # 提取参数
            parameters = self._extract_parameters(card)

            # 提取示例
            request_example, response_example = self._extract_examples(card)

            # 提取代码示例
            code_examples = self._extract_code_from_card(card)

            # 提取标签
            tags = self._extract_tags(card)

            return KimiApiEndpoint(
                path=path,
                method=method,
                description=description,
                endpoint_id=endpoint_id,
                parameters=parameters,
                request_example=request_example,
                response_example=response_example,
                code_examples=code_examples,
                tags=tags,
            )
        except Exception:
            return None

    def _extract_path(self, element) -> str:
        """提取路径"""
        for selector in self.SELECTORS.get('path', []):
            try:
                el = element.locator(selector).first
                if el.count() > 0:
                    path = el.inner_text().strip()
                    if path.startswith('/'):
                        return path
            except Exception:
                continue

        # 尝试从文本中提取
        text = element.inner_text()
        path_match = re.search(r'/v\d+/[\w/{}]+', text)
        if path_match:
            return path_match.group(0)

        return ""

    def _extract_method(self, element) -> str:
        """提取HTTP方法"""
        for selector in self.SELECTORS.get('method', []):
            try:
                el = element.locator(selector).first
                if el.count() > 0:
                    method = el.inner_text().strip().upper()
                    if method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        return method
            except Exception:
                continue

        # 尝试从文本/颜色识别
        text = element.inner_text().upper()
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if method in text:
                return method

        return 'POST'  # 默认

    def _extract_description(self, element) -> str:
        """提取描述"""
        for selector in self.SELECTORS.get('description', []):
            try:
                el = element.locator(selector).first
                if el.count() > 0:
                    return el.inner_text().strip()
            except Exception:
                continue

        # 尝试从段落提取
        try:
            paragraphs = element.locator('p').all()
            for p in paragraphs:
                text = p.inner_text().strip()
                if len(text) > 20:
                    return text
        except Exception:
            pass

        return ""

    def _extract_parameters(self, element) -> List[ApiParameter]:
        """提取参数列表"""
        params = []

        for selector in self.SELECTORS.get('param_table', []):
            try:
                table = element.locator(selector).first
                if table.count() > 0:
                    rows = table.locator('tr, li').all()
                    for row in rows:
                        try:
                            cells = row.locator('td, span').all()
                            if len(cells) >= 3:
                                name = cells[0].inner_text().strip()
                                param_type = cells[1].inner_text().strip()
                                desc = cells[2].inner_text().strip()
                                required = 'required' in desc.lower() or '*' in name

                                params.append(ApiParameter(
                                    name=name.replace('*', '').strip(),
                                    param_type=param_type,
                                    required=required,
                                    description=desc,
                                ))
                        except Exception:
                            continue
            except Exception:
                continue

        return params

    def _extract_examples(self, element) -> Tuple[Optional[str], Optional[str]]:
        """提取请求和响应示例"""
        request_example = None
        response_example = None

        for selector in self.SELECTORS.get('code_example', []):
            try:
                codes = element.locator(selector).all()
                for i, code in enumerate(codes):
                    text = code.inner_text().strip()
                    if text.startswith('{'):
                        if request_example is None:
                            request_example = text
                        elif response_example is None:
                            response_example = text
            except Exception:
                continue

        return request_example, response_example

    def _extract_code_examples(self, page) -> List[CodeBlock]:
        """提取代码示例"""
        code_blocks = []

        # 查找代码块
        code_selectors = ['pre code', 'pre', '.code-block', 'code']

        for selector in code_selectors:
            try:
                elements = page.locator(selector).all()
                for el in elements:
                    code = el.inner_text().strip()
                    if code and len(code) > 10:
                        lang = self._detect_language(code)
                        code_blocks.append(CodeBlock(
                            language=lang,
                            code=code,
                            filename=None,
                        ))
            except Exception:
                continue

        return code_blocks

    def _extract_code_from_card(self, card) -> List[str]:
        """从卡片提取代码示例"""
        codes = []

        try:
            pre_elements = card.locator('pre, code').all()
            for pre in pre_elements:
                code = pre.inner_text().strip()
                if code and len(code) > 10:
                    codes.append(code)
        except Exception:
            pass

        return codes

    def _extract_from_known_patterns(self, page) -> List[KimiApiEndpoint]:
        """从已知模式提取端点（兜底）"""
        endpoints = []

        # 获取页面文本
        try:
            text = page.inner_text()
        except Exception:
            return endpoints

        # 匹配已知模式
        for pattern, method, desc, tags in self.KNOWN_PATTERNS:
            match = re.search(pattern, text)
            if match:
                path = match.group(0)
                endpoint_id = self._generate_endpoint_id(path, method)

                # 检查是否已存在
                if any(e.path == path for e in endpoints):
                    continue

                endpoints.append(KimiApiEndpoint(
                    path=path,
                    method=method,
                    description=desc,
                    endpoint_id=endpoint_id,
                    parameters=[],
                    authentication='Authorization: Bearer <api_key>',
                    tags=tags,
                ))

        return endpoints

    def extract_models_list(self, page) -> List[ModelInfo]:
        """提取模型列表"""
        models = []

        # Kimi 模型
        kimi_models = [
            ('kimi-chat', 'Kimi Chat', 'Kimi Chat', '通用对话模型', 128000),
            ('moonshot-v1-8k', 'Moonshot V1 8K', 'Moonshot', '8K上下文', 8000),
            ('moonshot-v1-32k', 'Moonshot V1 32K', 'Moonshot', '32K上下文', 32000),
            ('moonshot-v1-128k', 'Moonshot V1 128K', 'Moonshot', '128K上下文', 128000),
        ]

        for model_id, name, provider, context, context_window in kimi_models:
            models.append(ModelInfo(
                name=model_id,
                display_name=name,
                description=f'{context} - {provider}',
                context_window=context_window,
                capabilities=['chat', 'completion'],
                input_modalities=['text'],
                output_modalities=['text'],
            ))

        return models

    def extract_breadcrumbs(self, page) -> List[str]:
        """提取面包屑"""
        breadcrumbs = []

        try:
            breadcrumb_sel = '.breadcrumb, .nav-path, [class*="breadcrumb"], nav'
            items = page.locator(f'{breadcrumb_sel} span, {breadcrumb_sel} a').all()
            for item in items:
                text = item.inner_text().strip()
                if text and text not in ['>', '/', '\\', 'Home']:
                    breadcrumbs.append(text)
        except Exception:
            pass

        return breadcrumbs[:5]  # 最多5级

    def _extract_tags(self, element) -> List[str]:
        """提取标签"""
        tags = []
        try:
            tag_elements = element.locator('[class*="tag"], .tag, span.tag').all()
            for tag in tag_elements:
                text = tag.inner_text().strip()
                if text:
                    tags.append(text)
        except Exception:
            pass
        return tags

    # ========== 辅助方法 ==========

    def _extract_title(self, page) -> str:
        """提取标题"""
        try:
            title = page.locator('h1, .title, .doc-title, .api-title').first.inner_text()
            return title.strip()
        except Exception:
            return page.title() or 'Kimi API 文档'

    def _generate_endpoint_id(self, path: str, method: str) -> str:
        """生成端点ID"""
        # /v1/chat/completions -> v1-chat-completions
        clean_path = path.replace('/', '-').replace('v1-', '').strip('-')
        return f"{method.lower()}-{clean_path}"

    def _detect_language(self, code: str) -> str:
        """检测代码语言"""
        # 简单检测
        if 'curl' in code:
            return 'bash'
        if 'import requests' in code or 'httpx' in code:
            return 'python'
        if 'def ' in code or 'import ' in code:
            return 'python'
        if 'function' in code or 'const ' in code:
            return 'javascript'
        if '{' in code and '}' in code:
            return 'json'
        return 'text'

    def _build_markdown(self, endpoints: List[KimiApiEndpoint], models: List[ModelInfo]) -> str:
        """构建 Markdown 内容"""
        md = []

        # 标题
        md.append("# Kimi API 文档\n")
        md.append("> Base URL: `https://api.moonshot.cn`\n")
        md.append("---\n")

        # 认证
        md.append("## 认证\n")
        md.append("```\nAuthorization: Bearer <api_key>\n```\n")
        md.append("获取 API Key: [platform.kimi.com](https://platform.kimi.com)\n\n")

        # 模型列表
        if models:
            md.append("## 支持的模型\n\n")
            md.append("| Model ID | 名称 | 上下文窗口 |\n")
            md.append("|----------|------|----------|\n")
            for model in models:
                md.append(f"| `{model.name}` | {model.display_name} | {model.context_window} |\n")
            md.append("\n")

        # 端点列表
        if endpoints:
            md.append("## API 端点\n")
            for ep in endpoints:
                md.append(f"### {ep.method} {ep.path}\n")
                md.append(f"{ep.description}\n\n")

                # 标签
                if ep.tags:
                    md.append(f"**标签**: {' / '.join(ep.tags)}\n\n")

                # 参数
                if ep.parameters:
                    md.append("**参数**:\n\n")
                    md.append("| 名称 | 类型 | 必填 | 描述 |\n")
                    md.append("|------|------|------|------|\n")
                    for p in ep.parameters:
                        req = '是' if p.required else '否'
                        md.append(f"| `{p.name}` | {p.param_type} | {req} | {p.description} |\n")
                    md.append("\n")

                # 请求示例
                if ep.request_example:
                    md.append("**请求示例**:\n")
                    md.append("```json\n")
                    md.append(ep.request_example)
                    md.append("\n```\n\n")

                # 代码示例
                if ep.code_examples:
                    for code in ep.code_examples[:2]:  # 最多2个
                        lang = self._detect_language(code)
                        md.append(f"```{lang}\n")
                        md.append(code)
                        md.append("\n```\n\n")

        return ''.join(md)

    def _build_toc(self, endpoints: List[KimiApiEndpoint]) -> List[HeadingItem]:
        """构建目录"""
        toc = []

        for ep in endpoints:
            toc.append(HeadingItem(
                level=2,
                text=f"{ep.method} {ep.path}",
                anchor=self._generate_endpoint_id(ep.path, ep.method),
            ))

        return toc

    def to_json(self) -> str:
        """导出为 JSON 格式"""
        # 转换端点为字典
        endpoints_data = []
        for ep in self.endpoints:
            endpoints_data.append({
                'path': ep.path,
                'method': ep.method,
                'description': ep.description,
                'endpoint_id': ep.endpoint_id,
                'parameters': [
                    {
                        'name': p.name,
                        'type': p.param_type,
                        'required': p.required,
                        'description': p.description,
                    } for p in ep.parameters
                ],
                'request_example': ep.request_example,
                'response_example': ep.response_example,
                'code_examples': ep.code_examples,
            })

        return json.dumps({
            'title': self.title,
            'base_url': 'https://api.moonshot.cn',
            'version': 'v1',
            'endpoints': endpoints_data,
            'models': [
                {
                    'model_id': m.name,
                    'name': m.display_name,
                    'provider': 'Moonshot',
                    'context_window': m.context_window,
                } for m in self.models
            ],
        }, indent=2, ensure_ascii=False)


# 注册适配器
register_adapter('kimi', KimiApiAdapter())
register_adapter('platform.kimi.com', KimiApiAdapter())
register_adapter('moonshot', KimiApiAdapter())


# 向后兼容：导出到 api_docs 目录
API_DOC_ADAPTERS = {
    'kimi': KimiApiAdapter,
}

__all__ = [
    'KimiApiAdapter',
    'KimiApiEndpoint',
    'KimiApiDoc',
    'ApiParameter',
    'ApiExample',
]