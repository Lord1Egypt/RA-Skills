#!/usr/bin/env python3
"""
Agent Ready Scanner - 检查网站是否为 AI Agent 做好准备
参考: https://isitagentready.com
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse, urljoin

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    print("Error: requests library required. Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)


@dataclass
class CheckResult:
    name: str
    category: str
    status: str  # "pass", "fail", "warning", "skip"
    message: str
    details: dict = field(default_factory=dict)
    fix_suggestion: str = ""


@dataclass
class ScanReport:
    url: str
    timestamp: str
    total_score: int
    max_score: int
    categories: dict
    checks: list
    summary: str


class AgentReadyScanner:
    """扫描网站是否为 AI Agent 做好准备"""
    
    def __init__(self, url: str, timeout: int = 10):
        self.base_url = url.rstrip('/')
        self.parsed = urlparse(self.base_url)
        self.domain = self.parsed.netloc
        self.timeout = timeout
        self.checks: list[CheckResult] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AgentReadyScanner/1.0 (+https://github.com/qclaw/agent-ready-scanner)'
        })
    
    def safe_get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """安全的 HTTP GET 请求"""
        try:
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True, **kwargs)
            return resp
        except RequestException:
            return None
    
    def safe_head(self, url: str) -> Optional[requests.Response]:
        """安全的 HTTP HEAD 请求"""
        try:
            resp = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            return resp
        except RequestException:
            return None
    
    # ========== DISCOVERABILITY ==========
    
    def check_robots_txt(self) -> CheckResult:
        """检查 robots.txt 是否存在且有效"""
        url = f"{self.base_url}/robots.txt"
        resp = self.safe_get(url)
        
        if resp is None or resp.status_code != 200:
            return CheckResult(
                name="robots.txt",
                category="Discoverability",
                status="fail",
                message="robots.txt 不存在或无法访问",
                fix_suggestion=f"在网站根目录创建 robots.txt 文件。示例:\n\nUser-agent: *\nAllow: /\n\nSitemap: {self.base_url}/sitemap.xml"
            )
        
        content = resp.text
        
        # 检查是否有 AI bot 规则
        ai_bots = ['GPTBot', 'ChatGPT-User', 'Claude-Web', 'Anthropic-AI', 'Google-Extended', 'CCBot', 'Omgili']
        has_ai_rules = any(bot in content for bot in ai_bots)
        
        # 检查是否有 sitemap 指令
        has_sitemap = 'sitemap' in content.lower()
        
        details = {
            "url": url,
            "has_ai_rules": has_ai_rules,
            "has_sitemap": has_sitemap,
            "size": len(content)
        }
        
        if has_ai_rules and has_sitemap:
            return CheckResult(
                name="robots.txt",
                category="Discoverability",
                status="pass",
                message="robots.txt 存在，包含 AI bot 规则和 sitemap 指令",
                details=details
            )
        elif has_ai_rules:
            return CheckResult(
                name="robots.txt",
                category="Discoverability",
                status="warning",
                message="robots.txt 存在，包含 AI bot 规则，但缺少 sitemap 指令",
                details=details,
                fix_suggestion=f"在 robots.txt 中添加 sitemap 指令:\n\nSitemap: {self.base_url}/sitemap.xml"
            )
        elif has_sitemap:
            return CheckResult(
                name="robots.txt",
                category="Discoverability",
                status="warning",
                message="robots.txt 存在，包含 sitemap 指令，但缺少 AI bot 规则",
                details=details,
                fix_suggestion="添加 AI 爬虫规则。示例:\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: Claude-Web\nAllow: /"
            )
        else:
            return CheckResult(
                name="robots.txt",
                category="Discoverability",
                status="warning",
                message="robots.txt 存在，但缺少 AI bot 规则和 sitemap 指令",
                details=details,
                fix_suggestion=f"添加 AI bot 规则和 sitemap 指令:\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: Claude-Web\nAllow: /\n\nSitemap: {self.base_url}/sitemap.xml"
            )
    
    def check_sitemap(self) -> CheckResult:
        """检查 sitemap.xml 是否存在"""
        # 先尝试从 robots.txt 获取 sitemap URL
        robots_resp = self.safe_get(f"{self.base_url}/robots.txt")
        sitemap_urls = []
        
        if robots_resp and robots_resp.status_code == 200:
            for line in robots_resp.text.splitlines():
                if line.lower().startswith('sitemap:'):
                    sitemap_urls.append(line.split(':', 1)[1].strip())
        
        if not sitemap_urls:
            sitemap_urls = [f"{self.base_url}/sitemap.xml"]
        
        for url in sitemap_urls:
            resp = self.safe_get(url)
            if resp and resp.status_code == 200 and '<?xml' in resp.text:
                # 简单验证 XML 格式
                url_count = resp.text.count('<url>')
                return CheckResult(
                    name="Sitemap",
                    category="Discoverability",
                    status="pass",
                    message=f"Sitemap 存在且有效，包含 {url_count} 个 URL",
                    details={"url": url, "url_count": url_count}
                )
        
        return CheckResult(
            name="Sitemap",
            category="Discoverability",
            status="fail",
            message="Sitemap 不存在或无效",
            fix_suggestion=f"创建 sitemap.xml 文件，列出网站所有重要页面。可使用在线工具或插件自动生成:\n\n{self.base_url}/sitemap.xml"
        )
    
    def check_link_headers(self) -> CheckResult:
        """检查 Link 响应头"""
        resp = self.safe_head(self.base_url)
        
        if resp is None:
            return CheckResult(
                name="Link Headers",
                category="Discoverability",
                status="fail",
                message="无法访问网站首页"
            )
        
        link_header = resp.headers.get('Link', '')
        
        if not link_header:
            # 尝试 GET 请求
            resp = self.safe_get(self.base_url)
            if resp:
                link_header = resp.headers.get('Link', '')
        
        details = {"link_header": link_header[:200] if link_header else None}
        
        if link_header:
            # 检查是否包含有用的链接类型
            has_alternate = 'rel="alternate"' in link_header or "rel=alternate" in link_header
            has_mcp = 'mcp' in link_header.lower()
            
            if has_mcp:
                return CheckResult(
                    name="Link Headers",
                    category="Discoverability",
                    status="pass",
                    message="Link 头包含 MCP 发现信息",
                    details=details
                )
            elif has_alternate:
                return CheckResult(
                    name="Link Headers",
                    category="Discoverability",
                    status="warning",
                    message="Link 头存在，包含 alternate 链接",
                    details=details,
                    fix_suggestion="考虑在 Link 头中添加 MCP 或其他 agent 发现信息"
                )
        
        return CheckResult(
            name="Link Headers",
            category="Discoverability",
            status="warning",
            message="Link 响应头未设置",
            details=details,
            fix_suggestion="在响应头中添加 Link 头，用于发现 MCP、API 等资源:\n\nLink: <./.well-known/mcp>; rel=\"mcp\""
        )
    
    # ========== CONTENT ACCESSIBILITY ==========
    
    def check_markdown_negotiation(self) -> CheckResult:
        """检查 Markdown 内容协商支持"""
        # 尝试 Accept: text/markdown
        try:
            resp = self.session.get(
                self.base_url,
                headers={'Accept': 'text/markdown, text/html;q=0.9'},
                timeout=self.timeout
            )
            
            content_type = resp.headers.get('Content-Type', '')
            details = {"content_type": content_type}
            
            if 'markdown' in content_type.lower():
                return CheckResult(
                    name="Markdown Negotiation",
                    category="Content Accessibility",
                    status="pass",
                    message="支持 Markdown 内容协商",
                    details=details
                )
            
            # 检查是否有 llms.txt
            llms_resp = self.safe_get(f"{self.base_url}/llms.txt")
            if llms_resp and llms_resp.status_code == 200:
                return CheckResult(
                    name="Markdown Negotiation",
                    category="Content Accessibility",
                    status="pass",
                    message="存在 llms.txt 文件（Markdown 格式的网站说明）",
                    details={"llms_txt": f"{self.base_url}/llms.txt"}
                )
            
            return CheckResult(
                name="Markdown Negotiation",
                category="Content Accessibility",
                status="warning",
                message="不支持 Markdown 内容协商",
                details=details,
                fix_suggestion="两种方式可选:\n\n1. 配置服务器支持 Markdown 内容协商（当 Accept: text/markdown 时返回 Markdown 格式）\n\n2. 创建 llms.txt 文件，提供网站内容的 Markdown 摘要，供 AI agents 使用"
            )
        except RequestException:
            return CheckResult(
                name="Markdown Negotiation",
                category="Content Accessibility",
                status="fail",
                message="请求失败"
            )
    
    def check_llms_txt(self) -> CheckResult:
        """检查 llms.txt 文件"""
        url = f"{self.base_url}/llms.txt"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            content = resp.text
            # 检查是否是有效的 Markdown
            has_title = content.strip().startswith('#')
            size = len(content)
            
            details = {"url": url, "size": size, "has_title": has_title}
            
            if has_title and size > 100:
                return CheckResult(
                    name="llms.txt",
                    category="Content Accessibility",
                    status="pass",
                    message=f"llms.txt 存在且内容丰富（{size} 字节）",
                    details=details
                )
            else:
                return CheckResult(
                    name="llms.txt",
                    category="Content Accessibility",
                    status="warning",
                    message="llms.txt 存在但内容可能不完整",
                    details=details,
                    fix_suggestion="完善 llms.txt 内容，添加网站概述、API 文档、重要链接等信息"
                )
        
        return CheckResult(
            name="llms.txt",
            category="Content Accessibility",
            status="fail",
            message="llms.txt 不存在",
            fix_suggestion=f"创建 llms.txt 文件，提供网站内容的 Markdown 摘要:\n\n# {self.domain}\n\n> 网站简介\n\n## 主要内容\n\n- 链接1: 描述\n- 链接2: 描述\n\n## API\n\n如有 API，在此说明"
        )
    
    # ========== BOT ACCESS CONTROL ==========
    
    def check_ai_bot_rules(self) -> CheckResult:
        """检查 AI bot 访问规则"""
        url = f"{self.base_url}/robots.txt"
        resp = self.safe_get(url)
        
        if resp is None or resp.status_code != 200:
            return CheckResult(
                name="AI Bot Rules",
                category="Bot Access Control",
                status="fail",
                message="无法读取 robots.txt",
                fix_suggestion="创建 robots.txt 并添加 AI bot 规则"
            )
        
        content = resp.text
        
        # 常见 AI bots
        ai_bots = {
            'GPTBot': 'OpenAI GPT 爬虫',
            'ChatGPT-User': 'ChatGPT 用户代理',
            'Claude-Web': 'Anthropic Claude 爬虫',
            'Anthropic-AI': 'Anthropic AI',
            'Google-Extended': 'Google AI 训练',
            'CCBot': 'Common Crawl',
            'Omgili': 'Omgili',
            'Bytespider': '字节跳动',
            'PerplexityBot': 'Perplexity'
        }
        
        found_bots = {}
        for bot, desc in ai_bots.items():
            if bot in content:
                # 查找对应的 Allow/Disallow
                pattern = rf'User-agent:\s*{bot}\s*\n(?:.*\n)*?\s*(Allow|Disallow):\s*(\S+)'
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    found_bots[bot] = {"desc": desc, "rule": f"{match.group(1)}: {match.group(2)}"}
                else:
                    found_bots[bot] = {"desc": desc, "rule": "未明确规则"}
        
        details = {"found_bots": found_bots}
        
        if len(found_bots) >= 3:
            return CheckResult(
                name="AI Bot Rules",
                category="Bot Access Control",
                status="pass",
                message=f"已配置 {len(found_bots)} 个 AI bot 规则",
                details=details
            )
        elif found_bots:
            return CheckResult(
                name="AI Bot Rules",
                category="Bot Access Control",
                status="warning",
                message=f"仅配置了 {len(found_bots)} 个 AI bot 规则",
                details=details,
                fix_suggestion="添加更多 AI bot 规则:\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: Claude-Web\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /"
            )
        else:
            return CheckResult(
                name="AI Bot Rules",
                category="Bot Access Control",
                status="fail",
                message="未配置任何 AI bot 规则",
                fix_suggestion="在 robots.txt 中添加 AI bot 规则:\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: Claude-Web\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /"
            )
    
    def check_content_signals(self) -> CheckResult:
        """检查 Content Signals 支持"""
        resp = self.safe_get(self.base_url)
        
        if resp is None:
            return CheckResult(
                name="Content Signals",
                category="Bot Access Control",
                status="fail",
                message="无法访问网站"
            )
        
        # 检查 Content-Signal 头
        content_signal = resp.headers.get('Content-Signal', '')
        
        # 检查 meta 标签
        has_meta_signal = False
        if 'text/html' in resp.headers.get('Content-Type', ''):
            has_meta_signal = 'content-signal' in resp.text.lower() or 'content_signal' in resp.text.lower()
        
        details = {"header": content_signal[:100] if content_signal else None, "meta": has_meta_signal}
        
        if content_signal or has_meta_signal:
            return CheckResult(
                name="Content Signals",
                category="Bot Access Control",
                status="pass",
                message="支持 Content Signals",
                details=details
            )
        
        return CheckResult(
            name="Content Signals",
            category="Bot Access Control",
            status="warning",
            message="未检测到 Content Signals",
            details=details,
            fix_suggestion="Content Signals 是 Cloudflare 提供的内容标记机制，用于帮助 AI 理解内容类型和权限。如使用 Cloudflare，可启用 Content Signals 功能。"
        )
    
    # ========== PROTOCOL DISCOVERY ==========
    
    def check_mcp_server_card(self) -> CheckResult:
        """检查 MCP Server Card"""
        # 检查 /.well-known/mcp.json
        url = f"{self.base_url}/.well-known/mcp.json"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                details = {"url": url, "has_name": "name" in data, "has_tools": "tools" in data}
                
                if "name" in data:
                    return CheckResult(
                        name="MCP Server Card",
                        category="Protocol Discovery",
                        status="pass",
                        message=f"MCP Server Card 存在: {data.get('name', 'Unknown')}",
                        details=details
                    )
            except json.JSONDecodeError:
                pass
        
        # 检查 Link 头中的 MCP
        resp = self.safe_head(self.base_url)
        if resp:
            link = resp.headers.get('Link', '')
            if 'mcp' in link.lower():
                return CheckResult(
                    name="MCP Server Card",
                    category="Protocol Discovery",
                    status="warning",
                    message="Link 头中引用了 MCP，但 /.well-known/mcp.json 不存在",
                    fix_suggestion="创建 /.well-known/mcp.json 文件，定义 MCP server 信息"
                )
        
        return CheckResult(
            name="MCP Server Card",
            category="Protocol Discovery",
            status="fail",
            message="MCP Server Card 不存在",
            fix_suggestion=f"创建 /.well-known/mcp.json 文件:\n\n{{\n  \"name\": \"{self.domain}\",\n  \"description\": \"网站描述\",\n  \"tools\": []\n}}"
        )
    
    def check_agent_skills(self) -> CheckResult:
        """检查 Agent Skills"""
        # 检查 /.well-known/agent-skills.json 或 /agent-skills.json
        urls = [
            f"{self.base_url}/.well-known/agent-skills.json",
            f"{self.base_url}/agent-skills.json"
        ]
        
        for url in urls:
            resp = self.safe_get(url)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    skill_count = len(data.get('skills', []))
                    details = {"url": url, "skill_count": skill_count}
                    
                    if skill_count > 0:
                        return CheckResult(
                            name="Agent Skills",
                            category="Protocol Discovery",
                            status="pass",
                            message=f"Agent Skills 存在，定义了 {skill_count} 个技能",
                            details=details
                        )
                    else:
                        return CheckResult(
                            name="Agent Skills",
                            category="Protocol Discovery",
                            status="warning",
                            message="Agent Skills 文件存在，但未定义任何技能",
                            details=details,
                            fix_suggestion="在 agent-skills.json 中添加技能定义"
                        )
                except json.JSONDecodeError:
                    continue
        
        return CheckResult(
            name="Agent Skills",
            category="Protocol Discovery",
            status="fail",
            message="Agent Skills 不存在",
            fix_suggestion=f"创建 /.well-known/agent-skills.json 文件:\n\n{{\n  \"skills\": [\n    {{\n      \"name\": \"skill-name\",\n      \"description\": \"技能描述\",\n      \"endpoint\": \"/api/skill\"\n    }}\n  ]\n}}"
        )
    
    def check_webmcp(self) -> CheckResult:
        """检查 WebMCP 支持"""
        url = f"{self.base_url}/.well-known/webmcp.json"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                return CheckResult(
                    name="WebMCP",
                    category="Protocol Discovery",
                    status="pass",
                    message="支持 WebMCP",
                    details={"url": url}
                )
            except json.JSONDecodeError:
                pass
        
        return CheckResult(
            name="WebMCP",
            category="Protocol Discovery",
            status="warning",
            message="不支持 WebMCP",
            fix_suggestion="WebMCP 是通过 HTTP 暴露 MCP 的标准。如需支持，创建 /.well-known/webmcp.json"
        )
    
    def check_api_catalog(self) -> CheckResult:
        """检查 API Catalog"""
        # 检查 OpenAPI/Swagger
        urls = [
            f"{self.base_url}/openapi.json",
            f"{self.base_url}/.well-known/openapi.json",
            f"{self.base_url}/swagger.json",
            f"{self.base_url}/api-docs"
        ]
        
        for url in urls:
            resp = self.safe_get(url)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    if 'openapi' in data or 'swagger' in data:
                        return CheckResult(
                            name="API Catalog",
                            category="Protocol Discovery",
                            status="pass",
                            message="OpenAPI/Swagger 文档存在",
                            details={"url": url, "version": data.get('openapi') or data.get('swagger')}
                        )
                except json.JSONDecodeError:
                    continue
        
        return CheckResult(
            name="API Catalog",
            category="Protocol Discovery",
            status="warning",
            message="未发现 OpenAPI/Swagger 文档",
            fix_suggestion="提供 OpenAPI 规范文档，帮助 AI agents 发现和理解 API:\n\n/openapi.json 或 /.well-known/openapi.json"
        )
    
    def check_oauth_discovery(self) -> CheckResult:
        """检查 OAuth 发现"""
        url = f"{self.base_url}/.well-known/openid-configuration"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                return CheckResult(
                    name="OAuth Discovery",
                    category="Protocol Discovery",
                    status="pass",
                    message="支持 OAuth/OpenID Connect 发现",
                    details={"url": url}
                )
            except json.JSONDecodeError:
                pass
        
        # 检查 OAuth Protected Resource (RFC 9728)
        url2 = f"{self.base_url}/.well-known/oauth-protected-resource"
        resp2 = self.safe_get(url2)
        
        if resp2 and resp2.status_code == 200:
            return CheckResult(
                name="OAuth Discovery",
                category="Protocol Discovery",
                status="pass",
                message="支持 OAuth Protected Resource 发现 (RFC 9728)",
                details={"url": url2}
            )
        
        return CheckResult(
            name="OAuth Discovery",
            category="Protocol Discovery",
            status="warning",
            message="未配置 OAuth 发现",
            fix_suggestion="如网站使用 OAuth，配置 /.well-known/openid-configuration 或 /.well-known/oauth-protected-resource"
        )
    
    def check_a2a_agent_card(self) -> CheckResult:
        """检查 A2A Agent Card"""
        url = f"{self.base_url}/.well-known/agent.json"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                return CheckResult(
                    name="A2A Agent Card",
                    category="Protocol Discovery",
                    status="pass",
                    message="A2A Agent Card 存在",
                    details={"url": url, "name": data.get('name')}
                )
            except json.JSONDecodeError:
                pass
        
        return CheckResult(
            name="A2A Agent Card",
            category="Protocol Discovery",
            status="warning",
            message="A2A Agent Card 不存在",
            fix_suggestion="A2A (Agent-to-Agent) 是 Google 提出的 agent 互操作标准。创建 /.well-known/agent.json 定义 agent 信息"
        )
    
    # ========== COMMERCE ==========
    
    def check_x402(self) -> CheckResult:
        """检查 x402 支付协议"""
        # x402 使用 402 状态码
        resp = self.safe_get(self.base_url)
        
        if resp and resp.status_code == 402:
            return CheckResult(
                name="x402",
                category="Commerce",
                status="pass",
                message="支持 x402 支付协议 (HTTP 402)",
                details={"status_code": 402}
            )
        
        # 检查 /.well-known/x402.json
        url = f"{self.base_url}/.well-known/x402.json"
        resp2 = self.safe_get(url)
        
        if resp2 and resp2.status_code == 200:
            return CheckResult(
                name="x402",
                category="Commerce",
                status="pass",
                message="x402 配置存在",
                details={"url": url}
            )
        
        return CheckResult(
            name="x402",
            category="Commerce",
            status="warning",
            message="不支持 x402 支付协议",
            fix_suggestion="x402 是基于 HTTP 402 的 agentic 支付协议。如需支持 AI agent 自动支付，可配置 x402"
        )
    
    def check_ucp(self) -> CheckResult:
        """检查 UCP (Universal Commerce Protocol)"""
        url = f"{self.base_url}/.well-known/ucp.json"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            return CheckResult(
                name="UCP",
                category="Commerce",
                status="pass",
                message="支持 UCP (Universal Commerce Protocol)",
                details={"url": url}
            )
        
        return CheckResult(
            name="UCP",
            category="Commerce",
            status="warning",
            message="不支持 UCP",
            fix_suggestion="UCP 是通用商业协议。如需支持 agentic commerce，可配置 UCP"
        )
    
    def check_acp(self) -> CheckResult:
        """检查 ACP (Agentic Commerce Protocol)"""
        url = f"{self.base_url}/.well-known/acp.json"
        resp = self.safe_get(url)
        
        if resp and resp.status_code == 200:
            return CheckResult(
                name="ACP",
                category="Commerce",
                status="pass",
                message="支持 ACP (Agentic Commerce Protocol)",
                details={"url": url}
            )
        
        return CheckResult(
            name="ACP",
            category="Commerce",
            status="warning",
            message="不支持 ACP",
            fix_suggestion="ACP 是 Agentic Commerce Protocol。如需支持 AI agent 自动交易，可配置 ACP"
        )
    
    # ========== 执行扫描 ==========
    
    def run_all_checks(self) -> list[CheckResult]:
        """执行所有检查"""
        self.checks = []
        
        # Discoverability
        self.checks.append(self.check_robots_txt())
        self.checks.append(self.check_sitemap())
        self.checks.append(self.check_link_headers())
        
        # Content Accessibility
        self.checks.append(self.check_llms_txt())
        self.checks.append(self.check_markdown_negotiation())
        
        # Bot Access Control
        self.checks.append(self.check_ai_bot_rules())
        self.checks.append(self.check_content_signals())
        
        # Protocol Discovery
        self.checks.append(self.check_mcp_server_card())
        self.checks.append(self.check_agent_skills())
        self.checks.append(self.check_webmcp())
        self.checks.append(self.check_api_catalog())
        self.checks.append(self.check_oauth_discovery())
        self.checks.append(self.check_a2a_agent_card())
        
        # Commerce
        self.checks.append(self.check_x402())
        self.checks.append(self.check_ucp())
        self.checks.append(self.check_acp())
        
        return self.checks
    
    def calculate_score(self) -> tuple[int, int]:
        """计算总分"""
        score_map = {"pass": 2, "warning": 1, "fail": 0, "skip": 0}
        total = sum(score_map.get(c.status, 0) for c in self.checks)
        max_score = len(self.checks) * 2
        return total, max_score
    
    def generate_report(self) -> ScanReport:
        """生成报告"""
        total, max_score = self.calculate_score()
        
        # 按类别分组
        categories = {}
        for check in self.checks:
            cat = check.category
            if cat not in categories:
                categories[cat] = {"checks": [], "score": 0, "max_score": 0}
            categories[cat]["checks"].append(asdict(check))
            score_map = {"pass": 2, "warning": 1, "fail": 0, "skip": 0}
            categories[cat]["score"] += score_map.get(check.status, 0)
            categories[cat]["max_score"] += 2
        
        # 生成摘要
        pass_count = sum(1 for c in self.checks if c.status == "pass")
        warning_count = sum(1 for c in self.checks if c.status == "warning")
        fail_count = sum(1 for c in self.checks if c.status == "fail")
        
        percentage = int((total / max_score) * 100) if max_score > 0 else 0
        
        if percentage >= 80:
            summary = f"🎉 网站已为 AI Agent 做好准备！得分 {percentage}%，{pass_count} 项通过"
        elif percentage >= 50:
            summary = f"⚠️ 网站部分准备就绪，得分 {percentage}%，{pass_count} 项通过，{warning_count} 项需改进"
        else:
            summary = f"❌ 网站尚未准备好，得分 {percentage}%，{fail_count} 项未通过"
        
        return ScanReport(
            url=self.base_url,
            timestamp=datetime.now().isoformat(),
            total_score=total,
            max_score=max_score,
            categories=categories,
            checks=[asdict(c) for c in self.checks],
            summary=summary
        )


def main():
    parser = argparse.ArgumentParser(description="Agent Ready Scanner - 检查网站是否为 AI Agent 做好准备")
    parser.add_argument("url", help="要扫描的网站 URL")
    parser.add_argument("--timeout", type=int, default=10, help="请求超时时间（秒）")
    parser.add_argument("--output", "-o", help="输出文件路径（JSON 格式）")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    # 确保 URL 有协议
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"🔍 扫描 {url} ...", file=sys.stderr)
    
    scanner = AgentReadyScanner(url, timeout=args.timeout)
    scanner.run_all_checks()
    report = scanner.generate_report()
    
    if args.format == "json":
        output = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    else:
        # 文本格式
        lines = [
            f"Agent Ready Report for {report.url}",
            f"=" * 50,
            f"Score: {report.total_score}/{report.max_score} ({int(report.total_score/report.max_score*100)}%)",
            f"",
            report.summary,
            f"",
        ]
        
        for cat, data in report.categories.items():
            lines.append(f"\n## {cat}")
            lines.append(f"Score: {data['score']}/{data['max_score']}")
            for check in data['checks']:
                status_icon = {"pass": "✅", "warning": "⚠️", "fail": "❌"}.get(check['status'], "❓")
                lines.append(f"  {status_icon} {check['name']}: {check['message']}")
        
        output = "\n".join(lines)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 报告已保存到 {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
