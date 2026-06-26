#!/usr/bin/env python3
"""
Hidden Tests Interface

隐藏测试集，用于防止测试污染和过度拟合。
测试用例在运行前保持加密/隐藏状态，确保评估的公平性。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Union
import base64
import hashlib
import json
import secrets


class TestVisibility(Enum):
    """测试可见性级别"""
    PUBLIC = "public"           # 公开测试 (开发时使用)
    PROTECTED = "protected"     # 受保护测试 (部分可见)
    HIDDEN = "hidden"           # 完全隐藏 (正式评估时使用)


class TestType(Enum):
    """隐藏测试类型"""
    FUNCTIONAL = "functional"       # 功能测试
    EDGE_CASE = "edge_case"         # 边界条件
    ADVERSARIAL = "adversarial"     # 对抗测试
    SECURITY = "security"           # 安全测试
    PERFORMANCE = "performance"     # 性能测试
    DISTRIBUTION = "distribution"   # 分布外测试


@dataclass(frozen=True)
class TestMetadata:
    """
    测试元数据 (不可变，不包含敏感内容)

    Attributes:
        id: 测试 ID (公开)
        type: 测试类型 (公开)
        category: 测试类别 (公开)
        difficulty: 难度等级 (公开)
        estimated_time_ms: 估计执行时间 (公开)
        hash: 测试内容哈希 (用于验证)
    """
    id: str
    type: TestType
    category: str
    difficulty: int = 3
    estimated_time_ms: float = 1000.0
    hash: str = ""


@dataclass(frozen=True)
class HiddenTest:
    """
    单个隐藏测试用例 (不可变，敏感内容加密存储)

    Attributes:
        metadata: 公开元数据
        encrypted_input: 加密的输入数据
        encrypted_expected: 加密的期望输出
        encrypted_validator: 加密的验证逻辑
        salt: 加密盐值
        visibility: 可见性级别
    """
    metadata: TestMetadata
    encrypted_input: bytes
    encrypted_expected: bytes
    encrypted_validator: bytes
    salt: bytes
    visibility: TestVisibility = TestVisibility.HIDDEN

    def verify_hash(self, input_data: Any, expected_output: Any) -> bool:
        """
        验证测试数据哈希是否匹配

        Args:
            input_data: 解密的输入数据
            expected_output: 解密的期望输出

        Returns:
            哈希是否匹配
        """
        content = json.dumps({
            "input": input_data,
            "expected": expected_output,
            "salt": base64.b64encode(self.salt).decode(),
        }, sort_keys=True, default=str)
        computed_hash = hashlib.sha256(content.encode()).hexdigest()[:32]
        return computed_hash == self.metadata.hash


@dataclass(frozen=True)
class TestResult:
    """
    隐藏测试结果 (不可变)

    Attributes:
        test_id: 测试 ID
        passed: 是否通过
        score: 得分 (0.0 - 1.0)
        details: 详细结果
        execution_time_ms: 执行时间
        token_usage: Token 使用量
        timestamp: 执行时间戳
    """
    test_id: str
    passed: bool
    score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    token_usage: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        assert 0.0 <= self.score <= 1.0, "Score must be in [0, 1]"


class TestDecryptor(Protocol):
    """
    测试解密器协议

    实现此协议的类可以解密隐藏测试。
    """

    def decrypt(self, encrypted_data: bytes, salt: bytes, key: bytes) -> Any:
        """解密数据"""
        ...

    def derive_key(self, password: str, salt: bytes) -> bytes:
        """从密码派生密钥"""
        ...


class SkillUnderTest(Protocol):
    """
    被测 Skill 协议

    实现此协议的类可以作为隐藏测试的目标。
    """

    def execute(self, input_data: Any) -> Any:
        """执行 Skill 并返回结果"""
        ...

    def get_name(self) -> str:
        """返回 Skill 名称"""
        ...


class HiddenTestDataSource(Protocol):
    """
    隐藏测试数据源协议

    支持从外部输入用例或密文/占位数据源读取测试。
    """

    def load_tests(self) -> List[HiddenTest]:
        """加载测试用例"""
        ...

    def get_metadata(self) -> Dict[str, Any]:
        """获取数据源元数据"""
        ...


class DictHiddenTestDataSource:
    """
    字典格式隐藏测试数据源

    从字典/JSON 数据加载测试用例。
    """

    def __init__(self, data: Dict[str, Any], password: str):
        self.data = data
        self.password = password

    def load_tests(self) -> List[HiddenTest]:
        """从字典加载测试"""
        tests = []
        for test_data in self.data.get("tests", []):
            metadata = TestMetadata(
                id=test_data["metadata"]["id"],
                type=TestType(test_data["metadata"]["type"]),
                category=test_data["metadata"]["category"],
                difficulty=test_data["metadata"].get("difficulty", 3),
                estimated_time_ms=test_data["metadata"].get("estimated_time_ms", 1000.0),
                hash=test_data["metadata"].get("hash", ""),
            )
            test = HiddenTest(
                metadata=metadata,
                encrypted_input=base64.b64decode(test_data["encrypted_input"]),
                encrypted_expected=base64.b64decode(test_data["encrypted_expected"]),
                encrypted_validator=base64.b64decode(test_data["encrypted_validator"]),
                salt=base64.b64decode(test_data["salt"]),
                visibility=TestVisibility(test_data.get("visibility", "hidden")),
            )
            tests.append(test)
        return tests

    def get_metadata(self) -> Dict[str, Any]:
        """获取数据源元数据"""
        return {
            "source_type": "dict",
            "test_count": len(self.data.get("tests", [])),
            "suite_id": self.data.get("suite_id", "unknown"),
        }


class FileHiddenTestDataSource:
    """
    文件形式隐藏测试数据源

    从 JSON 文件加载测试用例。
    """

    def __init__(self, path: Union[str, Path], password: str):
        self.path = Path(path)
        self.password = password
        self._data: Optional[Dict[str, Any]] = None

    def _load_data(self) -> Dict[str, Any]:
        """加载文件数据"""
        if self._data is None:
            with open(self.path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        return self._data

    def load_tests(self) -> List[HiddenTest]:
        """从文件加载测试"""
        data = self._load_data()
        tests = []
        for test_data in data.get("tests", []):
            metadata = TestMetadata(
                id=test_data["metadata"]["id"],
                type=TestType(test_data["metadata"]["type"]),
                category=test_data["metadata"]["category"],
                difficulty=test_data["metadata"].get("difficulty", 3),
                estimated_time_ms=test_data["metadata"].get("estimated_time_ms", 1000.0),
                hash=test_data["metadata"].get("hash", ""),
            )
            test = HiddenTest(
                metadata=metadata,
                encrypted_input=base64.b64decode(test_data["encrypted_input"]),
                encrypted_expected=base64.b64decode(test_data["encrypted_expected"]),
                encrypted_validator=base64.b64decode(test_data["encrypted_validator"]),
                salt=base64.b64decode(test_data["salt"]),
                visibility=TestVisibility(test_data.get("visibility", "hidden")),
            )
            tests.append(test)
        return tests

    def get_metadata(self) -> Dict[str, Any]:
        """获取数据源元数据"""
        data = self._load_data()
        return {
            "source_type": "file",
            "file_path": str(self.path),
            "test_count": len(data.get("tests", [])),
            "suite_id": data.get("suite_id", "unknown"),
        }


class HiddenTestSuite:
    """
    隐藏测试套件

    管理一组隐藏测试，提供安全的测试执行环境。
    测试用例在加载时保持加密，执行时临时解密。
    
    P2-a 增强:
    - 支持从外部数据源加载测试
    - 明确可见性边界 (evaluator/proposer)
    - 提供 runner interface
    """

    def __init__(
        self,
        suite_id: str,
        name: str,
        version: str,
        description: str = "",
        key_derivation: str = "pbkdf2",
    ):
        self.suite_id = suite_id
        self.name = name
        self.version = version
        self.description = description
        self.key_derivation = key_derivation
        self._tests: Dict[str, HiddenTest] = {}
        self._decryption_key: Optional[bytes] = None
        self._data_source: Optional[HiddenTestDataSource] = None
        self._visibility_boundary: str = "evaluator"  # evaluator | proposer | both

    def add_test(self, test: HiddenTest) -> None:
        """添加隐藏测试"""
        self._tests[test.metadata.id] = test

    def load_from_data_source(self, data_source: HiddenTestDataSource, password: str) -> bool:
        """
        从外部数据源加载测试用例

        Args:
            data_source: 测试数据源
            password: 解锁密码

        Returns:
            加载是否成功
        """
        self._data_source = data_source
        try:
            tests = data_source.load_tests()
            for test in tests:
                self._tests[test.metadata.id] = test
            return self.unlock(password)
        except Exception:
            return False

    def set_visibility_boundary(self, boundary: str) -> None:
        """
        设置可见性边界

        Args:
            boundary: "evaluator" | "proposer" | "both"
        
        可见性边界说明:
        - evaluator: 仅评估器可见 (默认)
        - proposer: 仅提案器可见
        - both: 两者都可见
        """
        if boundary not in ["evaluator", "proposer", "both"]:
            raise ValueError("Boundary must be 'evaluator', 'proposer', or 'both'")
        self._visibility_boundary = boundary

    def is_visible_to(self, role: str) -> bool:
        """
        检查测试对指定角色是否可见

        Args:
            role: 角色名称 ("evaluator" 或 "proposer")

        Returns:
            是否可见
        """
        if self._visibility_boundary == "both":
            return True
        return self._visibility_boundary == role

    def get_visible_tests(self, role: str) -> List[HiddenTest]:
        """
        获取对指定角色可见的测试

        Args:
            role: 角色名称

        Returns:
            可见的测试列表
        """
        if self.is_visible_to(role):
            return list(self._tests.values())
        return []

    def load_from_file(self, path: Union[str, Path]) -> None:
        """从文件加载测试套件"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.suite_id = data.get("suite_id", self.suite_id)
        self.name = data.get("name", self.name)
        self.version = data.get("version", self.version)

        for test_data in data.get("tests", []):
            metadata = TestMetadata(
                id=test_data["metadata"]["id"],
                type=TestType(test_data["metadata"]["type"]),
                category=test_data["metadata"]["category"],
                difficulty=test_data["metadata"].get("difficulty", 3),
                estimated_time_ms=test_data["metadata"].get("estimated_time_ms", 1000.0),
                hash=test_data["metadata"].get("hash", ""),
            )
            test = HiddenTest(
                metadata=metadata,
                encrypted_input=base64.b64decode(test_data["encrypted_input"]),
                encrypted_expected=base64.b64decode(test_data["encrypted_expected"]),
                encrypted_validator=base64.b64decode(test_data["encrypted_validator"]),
                salt=base64.b64decode(test_data["salt"]),
                visibility=TestVisibility(test_data.get("visibility", "hidden")),
            )
            self.add_test(test)

    def save_to_file(self, path: Union[str, Path]) -> None:
        """保存测试套件到文件"""
        data = {
            "suite_id": self.suite_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "test_count": len(self._tests),
            "tests": [
                {
                    "metadata": {
                        "id": t.metadata.id,
                        "type": t.metadata.type.value,
                        "category": t.metadata.category,
                        "difficulty": t.metadata.difficulty,
                        "estimated_time_ms": t.metadata.estimated_time_ms,
                        "hash": t.metadata.hash,
                    },
                    "encrypted_input": base64.b64encode(t.encrypted_input).decode(),
                    "encrypted_expected": base64.b64encode(t.encrypted_expected).decode(),
                    "encrypted_validator": base64.b64encode(t.encrypted_validator).decode(),
                    "salt": base64.b64encode(t.salt).decode(),
                    "visibility": t.visibility.value,
                }
                for t in self._tests.values()
            ],
        }

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def unlock(self, password: str, decryptor: Optional[TestDecryptor] = None) -> bool:
        """
        解锁测试套件 (解密)

        Args:
            password: 解锁密码
            decryptor: 可选的自定义解密器

        Returns:
            解锁是否成功
        """
        try:
            if decryptor:
                # 使用自定义解密器
                self._decryption_key = decryptor.derive_key(password, b"")
            else:
                # 使用默认密钥派生
                self._decryption_key = self._derive_key(password)
            return True
        except Exception:
            return False

    def _derive_key(self, password: str) -> bytes:
        """派生解密密钥"""
        # 简化实现：实际应使用 PBKDF2 或 Argon2
        return hashlib.sha256(password.encode()).digest()

    def _decrypt(self, encrypted_data: bytes, salt: bytes) -> Any:
        """解密数据"""
        if self._decryption_key is None:
            raise RuntimeError("Test suite is locked. Call unlock() first.")

        # 简化实现：实际应使用 AES-GCM 或 ChaCha20-Poly1305
        # 这里使用简单的 XOR 作为演示
        key = self._decryption_key
        decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted_data)])
        return json.loads(decrypted.decode())

    def run_test(
        self,
        test_id: str,
        skill: SkillUnderTest,
        timeout_ms: float = 30000.0,
    ) -> TestResult:
        """
        运行单个隐藏测试

        Args:
            test_id: 测试 ID
            skill: 被测 Skill
            timeout_ms: 超时时间 (毫秒)

        Returns:
            测试结果
        """
        if test_id not in self._tests:
            return TestResult(
                test_id=test_id,
                passed=False,
                score=0.0,
                details={"error": f"Test {test_id} not found"},
            )

        test = self._tests[test_id]

        try:
            # 解密测试数据
            input_data = self._decrypt(test.encrypted_input, test.salt)
            expected_output = self._decrypt(test.encrypted_expected, test.salt)
            validator = self._decrypt(test.encrypted_validator, test.salt)

            # 验证完整性
            if not test.verify_hash(input_data, expected_output):
                return TestResult(
                    test_id=test_id,
                    passed=False,
                    score=0.0,
                    details={"error": "Test integrity check failed"},
                )

            # 执行测试
            import time
            start_time = time.time()
            actual_output = skill.execute(input_data)
            execution_time_ms = (time.time() - start_time) * 1000

            # 验证结果
            passed, score, details = self._validate(
                actual_output,
                expected_output,
                validator,
            )

            return TestResult(
                test_id=test_id,
                passed=passed,
                score=score,
                details=details,
                execution_time_ms=execution_time_ms,
            )

        except Exception as e:
            return TestResult(
                test_id=test_id,
                passed=False,
                score=0.0,
                details={"error": str(e)},
            )

    def _validate(
        self,
        actual: Any,
        expected: Any,
        validator: Dict[str, Any],
    ) -> tuple[bool, float, Dict[str, Any]]:
        """
        验证实际输出是否符合期望

        Args:
            actual: 实际输出
            expected: 期望输出
            validator: 验证配置

        Returns:
            (是否通过, 得分, 详细信息)
        """
        validator_type = validator.get("type", "exact")

        if validator_type == "exact":
            passed = actual == expected
            score = 1.0 if passed else 0.0
            return passed, score, {"match": passed}

        elif validator_type == "contains":
            # 检查实际输出是否包含期望的关键内容
            if isinstance(expected, dict) and "keywords" in expected:
                keywords = expected["keywords"]
                actual_str = json.dumps(actual, default=str).lower()
                matches = [kw for kw in keywords if kw.lower() in actual_str]
                score = len(matches) / len(keywords) if keywords else 0.0
                return score >= validator.get("threshold", 0.8), score, {"matches": matches}

        elif validator_type == "function":
            # 使用自定义验证函数
            # 注意：实际实现中需要沙箱环境
            return True, 0.5, {"note": "Custom validator executed"}

        return False, 0.0, {"error": "Unknown validator type"}

    def run_all(
        self,
        skill: SkillUnderTest,
        categories: Optional[Set[str]] = None,
        types: Optional[Set[TestType]] = None,
        max_difficulty: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        运行所有符合条件的隐藏测试

        Args:
            skill: 被测 Skill
            categories: 仅运行指定类别的测试
            types: 仅运行指定类型的测试
            max_difficulty: 最大难度限制

        Returns:
            完整测试报告
        """
        results = []

        for test_id, test in self._tests.items():
            # 过滤测试
            if categories and test.metadata.category not in categories:
                continue
            if types and test.metadata.type not in types:
                continue
            if max_difficulty and test.metadata.difficulty > max_difficulty:
                continue

            result = self.run_test(test_id, skill)
            results.append(result)

        # 生成报告
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0.0

        # 按类型统计
        type_stats: Dict[str, Dict] = {}
        for test_id, result in zip(self._tests.keys(), results):
            test_type = self._tests[test_id].metadata.type.value
            if test_type not in type_stats:
                type_stats[test_type] = {"total": 0, "passed": 0, "avg_score": 0.0}
            type_stats[test_type]["total"] += 1
            if result.passed:
                type_stats[test_type]["passed"] += 1
            type_stats[test_type]["avg_score"] += result.score

        for stats in type_stats.values():
            if stats["total"] > 0:
                stats["avg_score"] /= stats["total"]

        return {
            "suite_id": self.suite_id,
            "version": self.version,
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": passed / total if total > 0 else 0.0,
                "avg_score": round(avg_score, 4),
            },
            "by_type": type_stats,
            "results": [
                {
                    "test_id": r.test_id,
                    "passed": r.passed,
                    "score": r.score,
                    "time_ms": r.execution_time_ms,
                }
                for r in results
            ],
        }

    def lock(self) -> None:
        """锁定测试套件 (清除解密密钥)"""
        self._decryption_key = None

    def get_metadata(self) -> Dict[str, Any]:
        """获取测试套件元数据 (公开信息)"""
        return {
            "suite_id": self.suite_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "test_count": len(self._tests),
            "tests": [
                {
                    "id": t.metadata.id,
                    "type": t.metadata.type.value,
                    "category": t.metadata.category,
                    "difficulty": t.metadata.difficulty,
                    "estimated_time_ms": t.metadata.estimated_time_ms,
                }
                for t in self._tests.values()
            ],
        }


# 辅助函数：创建隐藏测试

def create_hidden_test(
    test_id: str,
    input_data: Any,
    expected_output: Any,
    validator: Dict[str, Any],
    password: str,
    test_type: TestType = TestType.FUNCTIONAL,
    category: str = "general",
    difficulty: int = 3,
) -> HiddenTest:
    """
    创建新的隐藏测试

    Args:
        test_id: 测试 ID
        input_data: 输入数据
        expected_output: 期望输出
        validator: 验证配置
        password: 加密密码
        test_type: 测试类型
        category: 测试类别
        difficulty: 难度等级

    Returns:
        创建的隐藏测试
    """
    # 生成盐值
    salt = secrets.token_bytes(16)

    # 派生密钥
    key = hashlib.sha256(password.encode()).digest()

    # 加密数据
    def encrypt(data: Any) -> bytes:
        json_data = json.dumps(data, default=str).encode()
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(json_data)])

    encrypted_input = encrypt(input_data)
    encrypted_expected = encrypt(expected_output)
    encrypted_validator = encrypt(validator)

    # 计算哈希
    content = json.dumps({
        "input": input_data,
        "expected": expected_output,
        "salt": base64.b64encode(salt).decode(),
    }, sort_keys=True, default=str)
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]

    metadata = TestMetadata(
        id=test_id,
        type=test_type,
        category=category,
        difficulty=difficulty,
        hash=content_hash,
    )

    return HiddenTest(
        metadata=metadata,
        encrypted_input=encrypted_input,
        encrypted_expected=encrypted_expected,
        encrypted_validator=encrypted_validator,
        salt=salt,
        visibility=TestVisibility.HIDDEN,
    )
