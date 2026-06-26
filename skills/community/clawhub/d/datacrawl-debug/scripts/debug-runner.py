#!/usr/bin/env python3
"""DebugRunner — 代码错误诊断与修复建议"""

import argparse
import json
import re
import sys


# 常见数据处理错误模式库
ERROR_PATTERNS = {
    "connection": {
        "patterns": [
            r"ConnectionError|MaxRetryError|NewConnectionError",
            r"requests\.exceptions\.ConnectionError",
            r"urllib3\.exceptions",
            r"ERR_CONNECTION_REFUSED|ERR_CONNECTION_TIMED_OUT",
        ],
        "diagnosis": "网络连接失败",
        "causes": ["目标网站不可达", "DNS解析失败", "网络不稳定"],
        "fixes": [
            "检查URL是否正确，浏览器能否正常打开",
            "添加重试机制: requests.Session() + HTTPAdapter(max_retries=3)",
            "检查网络连接状态",
            "增加超时时间: timeout=30",
        ],
    },
    "http_error": {
        "patterns": [
            r"HTTP (\d{3})",
            r"status_code.*?(\d{3})",
            r"403 Forbidden|401 Unauthorized|429 Too Many|503 Service",
        ],
        "diagnosis": "HTTP状态码异常",
        "subtypes": {
            "403": {"cause": "访问被拒绝或权限不足", "fix": "检查请求头设置 / 降低请求频率 / 确认访问权限"},
            "401": {"cause": "需要认证", "fix": "检查认证信息是否正确"},
            "429": {"cause": "请求过于频繁", "fix": "增大请求间隔(3-5秒) / 降低并发数"},
            "503": {"cause": "服务暂时不可用", "fix": "稍后重试(30-60秒) / 检查服务状态"},
            "404": {"cause": "页面不存在或URL错误", "fix": "检查URL有效性 / 页面可能已下架"},
        },
        "fixes": ["根据具体状态码对症处理", "添加状态码检查: resp.raise_for_status()", "实现重试逻辑"],
    },
    "timeout": {
        "patterns": [
            r"Timeout|timed?[\s-]?out",
            r"ReadTimeout|ConnectTimeout",
            r"requests\.exceptions\.Timeout",
        ],
        "diagnosis": "请求超时",
        "causes": ["目标服务器响应慢", "网络不稳定", "页面过大/动态内容加载慢"],
        "fixes": [
            "增加超时: timeout=(5, 30)  # 连接5秒+读取30秒",
            "Playwright: page.goto(url, timeout=60000)",
            "对大页面使用流式读取: resp.iter_content(chunk_size=8192)",
        ],
    },
    "selector_error": {
        "patterns": [
            r"AttributeError.*?NoneType|NoneType.*?has no attribute",
            r"NoSuchElementException",
            r"find.*?returned None|select_one.*?returned None",
            r"IndexError.*?out of range|list index out of range",
        ],
        "diagnosis": "选择器匹配失败，元素未找到",
        "causes": ["页面结构变化", "动态加载未完成", "选择器写错"],
        "fixes": [
            "先用浏览器开发者工具验证选择器",
            "添加等待: time.sleep() 或 WebDriverWait",
            "使用更宽泛的选择器: class*='partial' 而非精确匹配",
            "添加None判断: if element: text = element.get_text()",
            "Playwright: page.wait_for_selector('.target', timeout=10000)",
        ],
    },
    "encoding": {
        "patterns": [
            r"UnicodeDecodeError|UnicodeEncodeError",
            r"codec can't decode|codec can't encode",
            r"gbk|gb2312|latin",
        ],
        "diagnosis": "编码问题",
        "causes": ["网页非UTF-8编码", "编码自动检测失败", "乱码数据"],
        "fixes": [
            "指定编码: resp.encoding = resp.apparent_encoding",
            "手动指定: resp.encoding = 'utf-8' 或 'gbk'",
            "原始字节解码: content = resp.content.decode('utf-8', errors='ignore')",
        ],
    },
    "json_parse": {
        "patterns": [
            r"json\.decoder\.JSONDecodeError",
            r"Expecting value|Expecting property",
            r"Unexpected.*?character",
        ],
        "diagnosis": "JSON解析失败",
        "causes": ["返回的不是JSON(可能是HTML错误页)", "JSON格式不规范", "返回为空"],
        "fixes": [
            "先检查resp.text确认返回内容类型",
            "添加: if resp.headers.get('content-type','').startswith('application/json')",
            "容错解析: json.loads(text, strict=False)",
            "检查是否被重定向到登录页",
        ],
    },
    "selenium_playwright": {
        "patterns": [
            r"selenium\.common\.exceptions",
            r"playwright\._impl\._errors",
            r"SessionNotCreatedException|WebDriverException",
            r"Browser closed unexpectedly",
        ],
        "diagnosis": "浏览器自动化错误",
        "causes": ["浏览器版本不匹配", "Driver未安装", "内存不足", "无头模式渲染失败"],
        "fixes": [
            "Playwright: playwright install chromium",
            "Selenium: 检查ChromeDriver版本与Chrome版本匹配",
            "添加参数: --no-sandbox --disable-dev-shm-usage --disable-gpu",
            "内存不足: --max-old-space-size=4096 或减少并发",
        ],
    },
    "rate_limit": {
        "patterns": [
            r"rate.?limit|too many requests|slow down",
            r"captcha|CAPTCHA|验证码|slider|滑块",
            r"blocked|banned|access denied",
        ],
        "diagnosis": "反爬/限流触发",
        "causes": ["请求频率过高", "IP被封", "触发验证码", "行为模式被识别"],
        "fixes": [
            "降低频率: 每次请求间隔3-5秒+随机抖动",
            "添加随机User-Agent: from fake_useragent import UserAgent",
            "使用代理IP池轮换",
            "遇到验证码: 暂停30分钟+切换IP+降低频率",
            "模拟人类行为: 随机鼠标移动+页面滚动",
        ],
    },
}


def diagnose(error_message: str, code_snippet: str = "") -> dict:
    """诊断错误并给出修复建议"""
    findings = []
    for category, info in ERROR_PATTERNS.items():
        for pattern in info["patterns"]:
            if re.search(pattern, error_message, re.IGNORECASE):
                finding = {
                    "category": category,
                    "diagnosis": info["diagnosis"],
                    "matched_pattern": pattern,
                    "causes": info.get("causes", []),
                    "fixes": info.get("fixes", []),
                }
                # HTTP状态码子类型
                if category == "http_error" and "subtypes" in info:
                    status_match = re.search(r"(\d{3})", error_message)
                    if status_match:
                        code = status_match.group(1)
                        if code in info["subtypes"]:
                            sub = info["subtypes"][code]
                            finding["specific_diagnosis"] = sub["cause"]
                            finding["specific_fix"] = sub["fix"]
                findings.append(finding)
                break

    if not findings:
        findings.append({
            "category": "unknown",
            "diagnosis": "未识别的错误类型",
            "causes": ["错误信息不在已知模式库中"],
            "fixes": [
                "1. 搜索错误信息的完整文本",
                "2. 检查错误堆栈中的文件名和行号",
                "3. 确认依赖版本是否兼容",
                "4. 在目标URL上手动测试请求",
            ],
        })

    # 代码片段分析
    code_hints = []
    if code_snippet:
        if "time.sleep" not in code_snippet:
            code_hints.append("建议添加请求间延迟: time.sleep(random.uniform(1, 3))")
        if "try" not in code_snippet and "except" not in code_snippet:
            code_hints.append("建议添加异常处理: try/except 包裹请求逻辑")
        if "timeout" not in code_snippet.lower():
            code_hints.append("建议设置超时: requests.get(url, timeout=15)")
        if "User-Agent" not in code_snippet:
            code_hints.append("建议添加User-Agent头部")

    return {
        "error_message": error_message[:500],
        "findings": findings,
        "code_hints": code_hints,
        "severity": "critical" if any(f["category"] in ("connection", "rate_limit") for f in findings) else "warning",
    }


def main():
    parser = argparse.ArgumentParser(description="DebugRunner - 代码错误诊断与修复建议")
    parser.add_argument("--error", type=str, required=True, help="错误信息")
    parser.add_argument("--code", type=str, default="", help="相关代码片段")

    args = parser.parse_args()
    result = diagnose(args.error, args.code)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
