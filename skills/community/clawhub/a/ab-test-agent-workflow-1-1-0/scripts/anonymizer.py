#!/usr/bin/env python3
"""
Anonymizer v1.0
双盲测试匿名化工具。

功能：
- 将 Contestant A/B 的输出随机化为"方案1"/"方案2"
- 支持多轮次匿名化
- 记录映射关系（仅供最终报告揭示身份）
- 检测并过滤 Contestant 输出的身份标识
"""

import random
import re
import sys
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple


@dataclass
class AnonymizedPair:
    """一轮匿名化结果"""
    round_num: int
    label_1: str        # "A" 或 "B"，方案1 对应谁
    label_2: str        # "B" 或 "A"，方案2 对应谁
    solution_1: str      # 方案1 的内容
    solution_2: str      # 方案2 的内容
    raw_a: str          # Contestant A 原始输出
    raw_b: str          # Contestant B 原始输出


@dataclass
class Anonymizer:
    """匿名化器"""
    round_num: int = 0
    pairs: List[AnonymizedPair] = field(default_factory=list)

    # 身份标识正则（Contestant 可能无意透露身份）
    IDENTITY_PATTERNS = [
        re.compile(r"(?i)(我是|我叫|I am|I'm)\s*(Contestant|A|B|参赛者)"),
        re.compile(r"(?i)Contestant\s*[AB]", re.IGNORECASE),
        re.compile(r"(?i)方案\s*[AB]"),
        re.compile(r"(?i)我是模型\s*\w+"),
        re.compile(r"(?i)(model|agent)\s*[AB]", re.IGNORECASE),
        re.compile(r"(?i)(来自|属于|由)\s*(A|B|方案)", re.IGNORECASE),
    ]

    def anonymize(
        self,
        output_a: str,
        output_b: str,
        round_num: Optional[int] = None,
    ) -> AnonymizedPair:
        """
        对一轮的双方输出进行匿名化。

        步骤：
        1. 检测并过滤身份标识
        2. 随机决定展示顺序（防顺序偏见）
        3. 记录映射关系（用于最终揭示）
        """
        rn = round_num if round_num is not None else (self.round_num + 1)
        self.round_num = rn

        # Step 1: 过滤身份标识
        clean_a = self._filter_identity(output_a)
        clean_b = self._filter_identity(output_b)

        # Step 2: 随机决定顺序
        if random.random() < 0.5:
            label_1, label_2 = "A", "B"
            sol_1, sol_2 = clean_a, clean_b
        else:
            label_1, label_2 = "B", "A"
            sol_1, sol_2 = clean_b, clean_a

        pair = AnonymizedPair(
            round_num=rn,
            label_1=label_1,
            label_2=label_2,
            solution_1=sol_1,
            solution_2=sol_2,
            raw_a=output_a,
            raw_b=output_b,
        )
        self.pairs.append(pair)
        return pair

    def _filter_identity(self, text: str) -> str:
        """过滤输出中的身份标识，防止 Contestant 泄露身份。"""
        result = text
        replaced = False
        for pattern in self.IDENTITY_PATTERNS:
            new_result = pattern.sub("[身份信息已过滤]", result)
            if new_result != result:
                result = new_result
                replaced = True
        return result

    def reveal(self, pair: AnonymizedPair) -> Dict[str, str]:
        """
        揭示匿名方案的真实来源。
        返回 {"solution_1": "Contestant X", "solution_2": "Contestant Y"}
        """
        return {
            "solution_1": f"Contestant {pair.label_1}",
            "solution_2": f"Contestant {pair.label_2}",
            "raw_a": pair.raw_a,
            "raw_b": pair.raw_b,
        }

    def get_mapping(self) -> List[Dict]:
        """获取所有轮次的匿名映射记录（用于最终报告）。"""
        return [
            {
                "round": p.round_num,
                "solution_1": f"Contestant {p.label_1}",
                "solution_2": f"Contestant {p.label_2}",
            }
            for p in self.pairs
        ]

    def check_blind(self, text: str) -> Tuple[bool, List[str]]:
        """
        检查文本是否包含泄露身份的信息。
        返回 (是否通过盲测, 违规片段列表)
        """
        violations = []
        for pattern in self.IDENTITY_PATTERNS:
            matches = pattern.findall(text)
            if matches:
                violations.extend([str(m) for m in matches])
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 3:
        print("用法: python anonymizer.py <output_A> <output_B> [--check]")
        print("示例: python anonymizer.py '我是A写的诗' '我是B的回答'")
        sys.exit(1)

    output_a = sys.argv[1]
    output_b = sys.argv[2]
    check_only = "--check" in sys.argv

    anon = Anonymizer()
    pair = anon.anonymize(output_a, output_b)

    print(f"Round {pair.round_num} 匿名化结果：")
    print(f"  方案1 = Contestant {pair.label_1}")
    print(f"  方案2 = Contestant {pair.label_2}")
    print(f"\n方案1内容：\n{pair.solution_1}")
    print(f"\n方案2内容：\n{pair.solution_2}")

    # 盲测检查
    blind_a, violations_a = anon.check_blind(output_a)
    blind_b, violations_b = anon.check_blind(output_b)

    if not blind_a:
        print(f"\n⚠️  Contestant A 输出包含身份标识: {violations_a}")
    if not blind_b:
        print(f"\n⚠️  Contestant B 输出包含身份标识: {violations_b}")

    print(f"\n✅ 匿名化完成！映射记录：")
    import json
    print(json.dumps(anon.get_mapping(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
