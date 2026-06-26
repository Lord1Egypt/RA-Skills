"""
AI生成服务

使用 DeepSeek API + LangChain 实现智能测试用例和脚本生成
"""

import json
import asyncio
import time
from typing import Optional, Dict, List
from datetime import datetime
import logging

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.schemas.ai import TestCaseGenerateRequest, ApiScriptGenerateRequest, UiScriptGenerateRequest

logger = logging.getLogger(__name__)


class AIGeneratorService:
    """AI生成服务类"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化AI生成服务

        Args:
            api_key: DeepSeek API密钥
        """
        self.api_key = api_key

        if not api_key:
            logger.warning("未提供DeepSeek API密钥，AI生成功能将不可用")
            self.llm = None
        else:
            try:
                self.llm = ChatOpenAI(
                    openai_api_key=api_key,
                    openai_api_base="https://api.deepseek.com",
                    model="deepseek-chat",
                    temperature=0.7,
                    max_retries=2,
                    timeout=30
                )
            except Exception as e:
                logger.error(f"初始化DeepSeek LLM失败: {str(e)}")
                self.llm = None

    def _generate_with_retry(self, chain: LLMChain, inputs: Dict) -> str:
        """带重试机制的内容生成"""
        if not self.llm:
            raise RuntimeError("AI服务未初始化，请提供有效的API密钥")

        max_retries = 2
        for attempt in range(max_retries):
            try:
                result = chain.run(**inputs)
                return result
            except Exception as e:
                logger.error(f"生成失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise RuntimeError(f"AI生成失败，已达到最大重试次数: {str(e)}")
                time.sleep(1)  # 等待1秒后重试

    def generate_test_cases(self, document_content: str, requirements: Optional[str] = None) -> str:
        """
        生成测试用例

        Args:
            document_content: 文档内容（已解析的文本）
            requirements: 额外需求说明

        Returns:
            生成的测试用例（Markdown格式）
        """
        # 如果没有提供文档内容，返回默认模板
        if not document_content:
            return self._get_default_test_case_template()

        prompt_template = """
你是一个专业的测试工程师，请根据以下需求文档生成详细的测试用例。

需求文档内容：
{document_content}

生成要求：
1. 生成至少5个功能测试用例，包括正常场景、边界场景和异常场景
2. 每个用例包含：用例编号、用例标题、前置条件、测试步骤、预期结果
3. 用例编号格式：TC-001, TC-002, ...
4. 使用Markdown格式输出
5. 重点关注业务逻辑和功能正确性

{requirements}

请生成测试用例："""

        if requirements:
            prompt_template = prompt_template.format(
                document_content=document_content,
                requirements=f"\n额外需求：{requirements}"
            )
        else:
            prompt_template = prompt_template.format(
                document_content=document_content,
                requirements=""
            )

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["document_content", "requirements"]
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = self._generate_with_retry(chain, {"document_content": document_content, "requirements": requirements or ""})

            return result

        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}")
            return self._get_default_test_case_template()

    def generate_api_script(self, document_content: str, api_info: Optional[str] = None) -> str:
        """
        生成API自动化测试脚本（Pytest + Requests）

        Args:
            document_content: 文档内容（应包含API接口信息）
            api_info: API信息（可选，覆盖文档中的API信息）

        Returns:
            生成的Python脚本
        """
        # 如果没有提供文档内容，返回默认模板
        if not document_content and not api_info:
            return self._get_default_api_script_template()

        prompt_template = """
你是一个专业的API测试工程师，请根据以下接口信息生成Pytest + Requests自动化测试脚本。

接口信息：
{document_content}
{api_info}

脚本要求：
1. 使用Pytest测试框架
2. 使用Requests库发送HTTP请求
3. 包含必要的断言（状态码、响应数据等）
4. 使用@pytest.mark.parametrize进行参数化测试
5. 包含fixture用于初始化测试环境
6. 代码要有详细的注释
7. 处理异常情况
8. 基类封装，包含常见的请求方法和断言方法

示例代码结构：
```python
import pytest
import requests

class BaseTestCase:
    """测试基类"""

    base_url = "http://localhost:8000"

    def make_request(self, method, endpoint, **kwargs):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        return response

def test_api_example():
    """测试示例"""
    # 测试代码
    pass
```

请生成完整的API测试脚本："""

        if api_info and not document_content:
            prompt_template = prompt_template.format(document_content="", api_info=api_info)
        elif api_info and document_content:
            prompt_template = prompt_template.format(document_content=document_content, api_info=api_info)
        else:
            prompt_template = prompt_template.format(document_content=document_content, api_info="")

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["document_content", "api_info"]
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = self._generate_with_retry(chain, {"document_content": document_content or "", "api_info": api_info or ""})

            return result

        except Exception as e:
            logger.error(f"生成API脚本失败: {str(e)}")
            return self._get_default_api_script_template()

    def generate_ui_script(self, document_content: str, ui_info: Optional[str] = None) -> str:
        """
        生成UI自动化测试脚本（Playwright）

        Args:
            document_content: 文档内容（应包含页面操作信息）
            ui_info: UI信息（可选，覆盖文档中的UI信息）

        Returns:
            生成的Python脚本
        """
        # 如果没有提供文档内容，返回默认模板
        if not document_content and not ui_info:
            return self._get_default_ui_script_template()

        prompt_template = """
你是一个专业的UI测试工程师，请根据以下页面操作信息生成Playwright自动化测试脚本。

页面信息：
{document_content}
{ui_info}

脚本要求：
1. 使用Playwright测试框架
2. 使用headless模式运行
3. 每个测试用例都包含截图（无论成功或失败）
4. 使用async/await语法
5. 包含fixture用于初始化浏览器和页面
6. 元素定位使用智能定位（page.locator()）
7. 包含必要的等待和超时处理
8. 代码要有详细的注释
9. 基类封装，包含常见的页面操作方法

示例代码结构：
```python
import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
class BaseUITest:
    """UI测试基类"""

    async def setup_method(self):
        """初始化浏览器和页面"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def teardown_method(self):
        """清理资源"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def navigate_to(self, url):
        """导航到指定URL"""
        await self.page.goto(url)

    async def take_screenshot(self, name):
        """截图"""
        await self.page.screenshot(path=f"screenshots/{name}.png")

async def test_example_page():
    """测试示例页面"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # 测试代码
        await browser.close()
```

请生成完整的UI测试脚本："""

        if ui_info and not document_content:
            prompt_template = prompt_template.format(document_content="", ui_info=ui_info)
        elif ui_info and document_content:
            prompt_template = prompt_template.format(document_content=document_content, ui_info=ui_info)
        else:
            prompt_template = prompt_template.format(document_content=document_content, ui_info="")

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["document_content", "ui_info"]
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = self._generate_with_retry(chain, {"document_content": document_content or "", "ui_info": ui_info or ""})

            return result

        except Exception as e:
            logger.error(f"生成UI脚本失败: {str(e)}")
            return self._get_default_ui_script_template()

    def _get_default_test_case_template(self) -> str:
        """获取默认测试用例模板"""
        return """# 测试用例

## TC-001: 登录功能测试
**前提条件**：用户已注册账号
**测试步骤**：
1. 打开登录页面
2. 输入正确的用户名和密码
3. 点击登录按钮
**预期结果**：成功登录，跳转到首页

## TC-002: 登录失败测试
**前提条件**：用户已注册账号
**测试步骤**：
1. 打开登录页面
2. 输入错误的密码
3. 点击登录按钮
**预期结果**：登录失败，显示错误提示
"""

    def _get_default_api_script_template(self) -> str:
        """获取默认API脚本模板"""
        return '''import pytest
import requests

class BaseTestCase:
    """API测试基类"""

    base_url = "http://localhost:8000"

    def make_request(self, method, endpoint, **kwargs):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        return response

@pytest.mark.asyncio
class TestAPIExample(BaseTestCase):
    """API测试示例"""

    def test_get_example(self):
        """测试GET请求"""
        response = self.make_request("GET", "/api/example")
        assert response.status_code == 200

    def test_post_example(self):
        """测试POST请求"""
        data = {"key": "value"}
        response = self.make_request("POST", "/api/example", json=data)
        assert response.status_code in [200, 201]
'''

    def _get_default_ui_script_template(self) -> str:
        """获取默认UI脚本模板"""
        return '''import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
class BaseUITest:
    """UI测试基类"""

    async def setup_method(self):
        """初始化浏览器和页面"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def teardown_method(self):
        """清理资源"""
        await self.browser.close()
        await self.playwright.stop()

    async def navigate_to(self, url):
        """导航到指定URL"""
        await self.page.goto(url)

    async def take_screenshot(self, name):
        """截图"""
        await self.page.screenshot(path=f"screenshots/{name}.png")

@pytest.mark.asyncio
class TestPageExample(BaseUITest):
    """页面测试示例"""

    async def test_page_title(self):
        """测试页面标题"""
        await self.navigate_to("http://localhost:3000")
        title = await self.page.title()
        assert title == "Expected Title"
        await self.take_screenshot("test_page_title")
'''
