#!/usr/bin/env python3
"""
LLM Eval Runner — AI应用评估测试运行脚本

用法:
  python eval_runner.py --test-file tests.jsonl --prompt-file prompts/system.txt
  python eval_runner.py --test-file tests.jsonl --api-url http://localhost:8000/chat

配置文件 eval_config.yaml:
  model: gpt-4o-mini
  api_key: ${OPENAI_API_KEY}
  metrics: [accuracy, latency, cost]
"""
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class TestCase:
    """评估测试用例"""
    id: str
    query: str
    expected_keywords: List[str]  # 期望回复中包含的关键词
    category: str = "general"
    max_latency_ms: int = 10000   # 最大允许延迟
    min_length: int = 10          # 最小回复长度


@dataclass
class EvalResult:
    """单条评估结果"""
    case_id: str
    passed: bool
    actual_response: str
    latency_ms: float
    token_count: int = 0
    cost_usd: float = 0.0
    fail_reason: str = ""


@dataclass
class EvalReport:
    """评估报告"""
    total: int = 0
    passed: int = 0
    results: List[EvalResult] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0

    @property
    def avg_latency_ms(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.latency_ms for r in self.results) / len(self.results)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "accuracy": f"{self.accuracy:.1%}",
            "avg_latency_ms": f"{self.avg_latency_ms:.0f}",
            "failed_cases": [
                {"id": r.case_id, "reason": r.fail_reason, "response": r.actual_response[:200]}
                for r in self.results if not r.passed
            ],
        }


def load_test_cases(filepath: str) -> List[TestCase]:
    """从 JSONL 文件加载测试用例"""
    cases = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            data = json.loads(line)
            cases.append(TestCase(**data))
    return cases


def evaluate_case(case: TestCase, llm_func) -> EvalResult:
    """评估单个测试用例"""
    start = time.time()
    try:
        response = llm_func(case.query)
    except Exception as e:
        return EvalResult(
            case_id=case.id,
            passed=False,
            actual_response="",
            latency_ms=(time.time() - start) * 1000,
            fail_reason=f"调用失败: {e}",
        )

    latency_ms = (time.time() - start) * 1000

    # 检查关键词匹配
    passed = all(
        kw.lower() in response.lower()
        for kw in case.expected_keywords
    )
    fail_reason = ""
    if not passed:
        missing = [kw for kw in case.expected_keywords if kw.lower() not in response.lower()]
        fail_reason = f"缺少关键词: {missing}"

    # 检查延迟
    if latency_ms > case.max_latency_ms:
        passed = False
        fail_reason += f"; 超时 {latency_ms:.0f}ms > {case.max_latency_ms}ms"

    return EvalResult(
        case_id=case.id,
        passed=passed,
        actual_response=response,
        latency_ms=latency_ms,
        fail_reason=fail_reason,
    )


def run_eval(test_file: str, llm_func, verbose: bool = False) -> EvalReport:
    """运行完整评估"""
    cases = load_test_cases(test_file)
    report = EvalReport(total=len(cases))

    print(f"\n{'='*60}")
    print(f"🧪 LLM Eval Runner")
    print(f"   测试用例: {len(cases)} 条")
    print(f"{'='*60}\n")

    for case in cases:
        result = evaluate_case(case, llm_func)
        report.results.append(result)

        status = "✅" if result.passed else "❌"
        print(f"{status} [{case.id}] {case.query[:40]}... ({result.latency_ms:.0f}ms)")
        if not result.passed and verbose:
            print(f"   失败原因: {result.fail_reason}")

    report.passed = sum(1 for r in report.results if r.passed)

    print(f"\n{'='*60}")
    print(f"📊 评估报告")
    print(f"   准确率: {report.accuracy:.1%} ({report.passed}/{report.total})")
    print(f"   平均延迟: {report.avg_latency_ms:.0f}ms")
    print(f"{'='*60}\n")

    return report


def create_mock_llm(responses: Dict[str, str] = None):
    """创建模拟 LLM (用于测试评估流程)"""
    responses = responses or {}
    def mock(query: str) -> str:
        for key, value in responses.items():
            if key in query:
                return value
        return f"Mock response for: {query}"
    return mock


def create_openai_llm(api_key: str, model: str, system_prompt: str = ""):
    """创建 OpenAI LLM 调用函数"""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    def call(query: str) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})
        resp = client.chat.completions.create(model=model, messages=messages)
        return resp.choices[0].message.content
    return call


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Eval Runner")
    parser.add_argument("--test-file", required=True, help="测试用例 JSONL 文件")
    parser.add_argument("--mock", action="store_true", help="使用 Mock LLM (快速测试)")
    parser.add_argument("--api-key", default="", help="OpenAI API Key")
    parser.add_argument("--model", default="gpt-4o-mini", help="模型名称")
    parser.add_argument("--prompt-file", default="", help="System Prompt 文件")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--output", "-o", default="", help="输出报告 JSON 文件路径")

    args = parser.parse_args()

    # 构建 LLM 调用函数
    if args.mock:
        llm_func = create_mock_llm()
        print("⚠️  使用 Mock LLM 模式")
    else:
        api_key = args.api_key or "sk-placeholder"
        system_prompt = ""
        if args.prompt_file:
            system_prompt = Path(args.prompt_file).read_text(encoding="utf-8")
        llm_func = create_openai_llm(api_key, args.model, system_prompt)
        print(f"🤖 模型: {args.model}")

    # 运行评估
    report = run_eval(args.test_file, llm_func, verbose=args.verbose)

    # 输出报告
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"📄 报告已保存: {args.output}")
