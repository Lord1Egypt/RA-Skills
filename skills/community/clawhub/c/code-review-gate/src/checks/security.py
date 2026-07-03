"""安全检查器 — 检测安全漏洞。

覆盖:
- SQL 注入
- XSS / 命令注入
- 硬编码敏感信息
- 输入验证缺失
- 权限控制缺失
"""

from __future__ import annotations

import re

from src.checks.base import BaseChecker
from src.models import CheckResult, Severity, Status


class SecurityChecker(BaseChecker):
    category = "security"
    label = "安全性 (Security)"
    severity = "critical"

    # SQL 关键字（用于注入检测）
    _SQL_KEYWORDS = r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|MERGE|REPLACE)\b"

    # SQL 注入危险模式
    # 设计思路：SQL 关键字可以出现在拼接符之前或之后，所以每个模式需覆盖双向
    SQL_INJECTION_PATTERNS = [
        # --- f-string: f"...SELECT...{var}" 或 f"...{var}...SELECT..." ---
        (
            r"f[\"'].*" + _SQL_KEYWORDS + r".*\{.*\}",
            "f-string 构建 SQL 查询 (SQL注入风险)",
            "使用参数化查询代替 f-string 拼接，如 cursor.execute(sql, params)",
        ),
        # --- 字符串拼接: "...SQL..." + var ---
        (
            r"[\"'].*" + _SQL_KEYWORDS + r".*[\"']\s*\+\s*\w+",
            'SQL 字符串通过 "+" 拼接变量 (SQL注入风险)',
            "使用参数化查询，将用户数据作为 execute() 的第二个参数传入",
        ),
        # --- 字符串拼接: var + "...SQL..." ---
        (
            r"\w+\s*\+\s*[\"'].*" + _SQL_KEYWORDS,
            'SQL 字符串通过 "+" 拼接变量 (SQL注入风险)',
            "使用参数化查询，将用户数据作为 execute() 的第二个参数传入",
        ),
        # --- .format(): "...SELECT...{var}".format(...) ---
        (
            r"[\"'].*" + _SQL_KEYWORDS + r".*[\"']\s*\.format\(",
            ".format() 构建 SQL 查询 (SQL注入风险)",
            "使用参数化查询代替 .format() 拼接",
        ),
        # --- % 格式化: "...SELECT...%s" % var ---
        (
            r"[\"'].*" + _SQL_KEYWORDS + r".*[\"']\s*%\s*\w+",
            "% 格式化构建 SQL 查询 (SQL注入风险)",
            "使用参数化查询代替 % 格式化",
        ),
        # --- execute() 参数拼接（防御纵深）---
        (
            r"execute\w*\(\s*\w+\s*\+\s*",
            "execute() 参数使用字符串拼接 (SQL注入风险)",
            "使用参数化查询，如 cursor.execute(sql, (param,))",
        ),
    ]

    # 命令注入
    COMMAND_INJECTION_PATTERNS = [
        (r"os\.system\(.*\+", "os.system 使用字符串拼接 (命令注入风险)", "使用 subprocess.run([...]) 带参数列表"),
        (r"os\.system\(.*format", "os.system 使用 .format() (命令注入风险)", "使用 subprocess.run([...]) 带参数列表"),
        (r"subprocess\.call\(.*shell\s*=\s*True", "subprocess 启用 shell=True (命令注入风险)", "移除 shell=True，使用参数列表"),
        (r"eval\(.*\+", "eval 使用动态字符串 (代码注入风险)", "避免使用 eval()"),
        (r"exec\(.*\+", "exec 使用动态字符串 (代码注入风险)", "避免使用 exec()"),
    ]

    # 硬编码敏感信息
    SECRET_PATTERNS = [
        (r"(api_?key|apikey)\s*=\s*[\"'][\w\-]{8,}", "API Key 硬编码", "使用环境变量或 Secret Manager"),
        (r"(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']", "密码硬编码", "使用环境变量或 Secret Manager"),
        (r"(secret|token)\s*=\s*[\"'][\w\-]{8,}", "Secret/Token 硬编码", "使用环境变量或 Secret Manager"),
        (r"(private_?key|privkey)\s*=\s*[\"']", "私钥硬编码", "使用文件引用或环境变量"),
    ]

    # 输入验证缺失
    INPUT_VALIDATION_PATTERNS = [
        (r"request\.(args|form|json|data)\[", "未使用 .get() 获取请求参数 (KeyError 风险)", "使用 request.args.get() 带默认值"),
        (r"int\(request\.", "未验证的 int() 类型转换", "使用 try/except 或参数验证"),
    ]

    def run(self) -> list[CheckResult]:
        ext = self._get_file_extensions()

        # 仅对代码文件执行安全检查
        code_exts = {".py", ".js", ".ts", ".java", ".go", ".rb", ".php", ".sql"}
        if not ext & code_exts and ext:
            self._finding("sec-skip", "安全检查", "critical", "skipped",
                          detail="非代码文件，跳过安全扫描")
            return [self._result(self.label)]

        self._check_sql_injection()
        self._check_command_injection()
        self._check_secrets()
        self._check_input_validation()
        self._check_xss()
        self._check_auth()

        return [self._result(self.label)]

    def _search(
        self,
        patterns: list[tuple[str, str, str]],
        check_id: str,
        extra_flags: int = 0,
    ) -> None:
        """通用模式搜索。

        Args:
            patterns: (regex, detail, fix) 三元组列表
            check_id: 归属的检查项 ID
            extra_flags: 额外的 re 标志位（如 re.DOTALL 用于跨行匹配）
        """
        flags = re.IGNORECASE | extra_flags
        for pattern, detail, fix in patterns:
            for match in re.finditer(pattern, self.diff, flags):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id=check_id,
                    question="是否存在安全漏洞？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="可能导致数据泄露、系统入侵或代码执行",
                    fix=fix,
                )

    def _check_sql_injection(self) -> None:
        # SQL 注入检测不使用 DOTALL：SQL 语句和拼接符通常在同一行
        # 跨行 SQL 拼接（如三引号字符串）按行拆分后单独检测
        self._search(self.SQL_INJECTION_PATTERNS, "sec-sql")

    def _check_command_injection(self) -> None:
        self._search(self.COMMAND_INJECTION_PATTERNS, "sec-cmd")

    def _check_secrets(self) -> None:
        for pattern, detail, fix in self.SECRET_PATTERNS:
            for match in re.finditer(pattern, self.diff, re.IGNORECASE):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="sec-secret",
                    question="是否有敏感信息硬编码？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="敏感信息暴露在代码仓库中",
                    fix=fix,
                )

    def _check_input_validation(self) -> None:
        for pattern, detail, fix in self.INPUT_VALIDATION_PATTERNS:
            for match in re.finditer(pattern, self.diff, re.IGNORECASE):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="sec-input",
                    question="输入验证是否充分？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="未验证的输入可能导致异常或安全漏洞",
                    fix=fix,
                )

    def _check_xss(self) -> None:
        # 检测 HTML/JS 中未转义的输出
        xss_patterns = [
            (r"innerHTML\s*=", "直接设置 innerHTML (XSS 风险)", "使用 textContent 或 DOMPurify"),
            (r"dangerouslySetInnerHTML", "React dangerouslySetInnerHTML (XSS 风险)", "使用 DOMPurify 清理内容"),
            (r"document\.write\(", "document.write 调用 (XSS 风险)", "使用安全 DOM API"),
            (r"\.html\(.*\+", "jQuery .html() 字符串拼接 (XSS 风险)", "使用 .text() 或转义"),
        ]
        for pattern, detail, fix in xss_patterns:
            for match in re.finditer(pattern, self.diff, re.IGNORECASE):
                line = self.diff[:match.start()].count("\n") + 1
                self._finding(
                    check_id="sec-xss",
                    question="是否存在 XSS 漏洞？",
                    severity="critical",
                    status="fail",
                    file_ref=f"line ~{line}",
                    detail=detail,
                    risk="可能导致跨站脚本攻击",
                    fix=fix,
                )

    def _check_auth(self) -> None:
        # 检测公开 API 端点是否缺少认证装饰器
        api_no_auth = []
        for match in re.finditer(
            r"def\s+(\w+)\s*\([^)]*\)\s*:\s*\n(?:\s*\"\"\"[^\"]*\"\"\"\s*\n)?(\s+)(?!.*@)", self.diff
        ):
            func_name = match.group(1)
            if any(word in func_name.lower() for word in ["admin", "delete", "manage", "config"]):
                api_no_auth.append(func_name)

        # 简化：检测路由装饰器后缺少认证装饰器
        auth_pattern = re.compile(
            r"@(?:app|router|bp|blueprint)\.(?:route|get|post|put|delete|patch)\([^)]+\)\s*\n(?!\s*@)",
        )
        for match in auth_pattern.finditer(self.diff):
            line = self.diff[:match.start()].count("\n") + 1
            self._finding(
                check_id="sec-auth",
                question="权限控制是否正确实现？",
                severity="critical",
                status="fail",
                file_ref=f"line ~{line}",
                detail="API 端点可能缺少认证中间件",
                risk="未认证访问可能导致数据泄露",
                fix="添加 @require_auth 或等效认证装饰器",
            )
