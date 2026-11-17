"""Benchmark suite for model performance testing."""
from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from .adapters.base import ChatMessage
from .router import ModelRouter


# Built-in question bank (50 questions across 6 dimensions)
QUESTION_BANK: Dict[str, List[Dict[str, Any]]] = {
    "reasoning": [
        {"id": "r1", "question": "一个水池有 3 根水管，单开甲管 4 小时注满，单开乙管 6 小时注满，单开丙管 8 小时排空。如果三管齐开，几小时能注满水池？", "answer": "24/7 小时"},
        {"id": "r2", "question": "有 12 个球，其中 11 个重量相同，1 个不同（不知轻重）。用天平最少称几次能找出？请说明步骤。", "answer": "3 次"},
        {"id": "r3", "question": "一个农夫要带一只狼、一只羊和一棵白菜过河，船每次只能载农夫和一件物品。农夫不在时，狼会吃羊，羊会吃白菜。问如何安全过河？", "answer": "农夫先带羊过河，返回，带狼过河，带羊返回，带白菜过河，返回，带羊过河"},
        {"id": "r4", "question": "有 5 个海盗分 100 枚金币，按编号顺序提方案，超半数同意则通过，否则提方案者被扔下海。假设海盗绝对理性，1 号应提什么方案？", "answer": "1 号提：97, 0, 1, 0, 2 或 97, 0, 1, 2, 0"},
        {"id": "r5", "question": "一个房间里有 3 盏灯，房间外有 3 个开关。你只能进房间一次，如何确定哪个开关对应哪盏灯？", "answer": "先开第一个开关等 5 分钟，关掉，开第二个开关，进房间。亮的是第二个，热但不亮的是第一个，冷且不亮的是第三个"},
        {"id": "r6", "question": "有 8 个球，其中 1 个较重。用天平最少称几次能找出？请说明步骤。", "answer": "2 次"},
        {"id": "r7", "question": "一个数列：1, 11, 21, 1211, 111221, 312211, ? 下一个数是什么？", "answer": "13112221"},
        {"id": "r8", "question": "小明从家到学校，如果每分钟走 60 米，迟到 5 分钟；如果每分钟走 75 米，提前 2 分钟。问家到学校距离？", "answer": "2100 米"},
        {"id": "r9", "question": "有 4 个人过桥，分别需要 1、2、5、10 分钟，桥每次最多过 2 人，手电筒必须携带。最少需要多少分钟？", "answer": "17 分钟"},
        {"id": "r10", "question": "一个整数除以 3 余 2，除以 5 余 3，除以 7 余 2，求最小正整数。", "answer": "23"},
    ],
    "code": [
        {"id": "c1", "question": "用 Python 写一个函数，判断一个字符串是否是回文。", "answer": "def is_palindrome(s): return s == s[::-1]"},
        {"id": "c2", "question": "用 Python 写一个函数，找出列表中的最大值和最小值（不使用内置 max/min）。", "answer": "def find_min_max(lst): min_val = max_val = lst[0]; for x in lst: if x < min_val: min_val = x; if x > max_val: max_val = x; return min_val, max_val"},
        {"id": "c3", "question": "用 Python 实现快速排序。", "answer": "def quicksort(arr): if len(arr) <= 1: return arr; pivot = arr[len(arr)//2]; left = [x for x in arr if x < pivot]; middle = [x for x in arr if x == pivot]; right = [x for x in arr if x > pivot]; return quicksort(left) + middle + quicksort(right)"},
        {"id": "c4", "question": "用 Python 写一个函数，计算斐波那契数列的第 n 项（递归 + 缓存）。", "answer": "from functools import lru_cache; @lru_cache(maxsize=None); def fib(n): if n < 2: return n; return fib(n-1) + fib(n-2)"},
        {"id": "c5", "question": "用 Python 实现一个简单的 LRU 缓存（容量为 capacity）。", "answer": "from collections import OrderedDict; class LRUCache: def __init__(self, capacity): self.cache = OrderedDict(); self.capacity = capacity; def get(self, key): if key not in self.cache: return -1; self.cache.move_to_end(key); return self.cache[key]; def put(self, key, value): if key in self.cache: self.cache.move_to_end(key); self.cache[key] = value; if len(self.cache) > self.capacity: self.cache.popitem(last=False)"},
        {"id": "c6", "question": "用 Python 写一个函数，判断一个数是否是质数。", "answer": "def is_prime(n): if n < 2: return False; for i in range(2, int(n**0.5)+1): if n % i == 0: return False; return True"},
        {"id": "c7", "question": "用 Python 实现二叉树的层序遍历（BFS）。", "answer": "from collections import deque; def level_order(root): if not root: return []; result = []; queue = deque([root]); while queue: level = []; for _ in range(len(queue)): node = queue.popleft(); level.append(node.val); if node.left: queue.append(node.left); if node.right: queue.append(node.right); result.append(level); return result"},
        {"id": "c8", "question": "用 Python 写一个函数，合并两个有序链表。", "answer": "def merge_two_lists(l1, l2): dummy = ListNode(0); curr = dummy; while l1 and l2: if l1.val < l2.val: curr.next = l1; l1 = l1.next; else: curr.next = l2; l2 = l2.next; curr = curr.next; curr.next = l1 or l2; return dummy.next"},
        {"id": "c9", "question": "用 Python 实现一个简单的装饰器，用于计算函数执行时间。", "answer": "import time; def timer(func): def wrapper(*args, **kwargs): start = time.time(); result = func(*args, **kwargs); print(f'{func.__name__} took {time.time()-start:.4f}s'); return result; return wrapper"},
        {"id": "c10", "question": "用 Python 写一个函数，找出数组中第 k 大的元素。", "answer": "import heapq; def find_kth_largest(nums, k): return heapq.nlargest(k, nums)[-1]"},
    ],
    "long_text": [
        {"id": "l1", "question": "阅读以下段落并总结核心观点：'人工智能的发展经历了多次浪潮。第一次浪潮以符号主义为主，专家系统广泛应用；第二次浪潮以统计学习为特征，支持向量机等算法兴起；第三次浪潮以深度学习为代表，在图像识别、自然语言处理等领域取得突破。当前，大语言模型正在引领新一轮变革。'", "answer": "AI 发展经历四次浪潮：符号主义→统计学习→深度学习→大语言模型"},
        {"id": "l2", "question": "阅读以下段落并回答问题：'量子计算利用量子比特的叠加态和纠缠态进行计算。与传统计算机不同，量子计算机在某些特定问题上具有指数级加速优势。目前主要技术路线包括超导、离子阱、光量子和拓扑量子等。' 问题：量子计算的核心优势是什么？", "answer": "在特定问题上具有指数级加速优势"},
        {"id": "l3", "question": "阅读以下段落并总结：'区块链技术通过分布式账本、共识机制和智能合约实现去中心化信任。比特币是第一个应用，以太坊引入了智能合约功能。当前区块链面临扩展性、互操作性和监管等挑战。'", "answer": "区块链通过分布式账本、共识机制、智能合约实现去中心化信任，面临扩展性、互操作性、监管挑战"},
        {"id": "l4", "question": "阅读以下段落并回答问题：'CRISPR-Cas9 是一种基因编辑技术，源自细菌的免疫系统。它通过向导 RNA 将 Cas9 蛋白引导到特定 DNA 序列进行切割。该技术被广泛应用于基因治疗、农业育种和基础研究领域。' 问题：CRISPR-Cas9 的核心机制是什么？", "answer": "通过向导 RNA 将 Cas9 蛋白引导到特定 DNA 序列进行切割"},
        {"id": "l5", "question": "阅读以下段落并总结：'碳中和是指通过植树造林、节能减排等方式抵消自身产生的二氧化碳排放量，实现二氧化碳净零排放。中国承诺在 2030 年前实现碳达峰，2060 年前实现碳中和。'", "answer": "碳中和是通过抵消实现净零排放，中国承诺 2030 碳达峰、2060 碳中和"},
        {"id": "l6", "question": "阅读以下段落并回答问题：'5G 网络具有高速率、低时延、大连接三大特点。其峰值速率可达 20Gbps，时延低至 1ms，每平方公里可连接 100 万台设备。' 问题：5G 的三大特点是什么？", "answer": "高速率、低时延、大连接"},
        {"id": "l7", "question": "阅读以下段落并总结：'元宇宙是整合多种新技术产生的虚实相融的互联网应用和社会形态。它基于扩展现实技术提供沉浸式体验，基于数字孪生技术生成现实世界的镜像，基于区块链技术搭建经济体系。'", "answer": "元宇宙是虚实相融的互联网形态，基于 XR、数字孪生、区块链构建"},
        {"id": "l8", "question": "阅读以下段落并回答问题：'边缘计算是将计算和数据存储放在靠近数据源的网络边缘节点上，以减少延迟、节省带宽。它与云计算形成互补关系。' 问题：边缘计算的核心优势是什么？", "answer": "减少延迟、节省带宽"},
        {"id": "l9", "question": "阅读以下段落并总结：'数字孪生是利用物理模型、传感器更新、运行历史等数据，集成多学科、多物理量、多尺度、多概率的仿真过程，在虚拟空间中完成映射，从而反映相对应的实体装备的全生命周期过程。'", "answer": "数字孪生是通过仿真在虚拟空间映射实体全生命周期的过程"},
        {"id": "l10", "question": "阅读以下段落并回答问题：'联邦学习是一种分布式机器学习方法，允许多个参与方在不共享原始数据的情况下协作训练模型。它通过交换模型参数而非数据来保护隐私。' 问题：联邦学习的核心特点是什么？", "answer": "不共享原始数据，通过交换模型参数协作训练，保护隐私"},
    ],
    "translation": [
        {"id": "t1", "question": "将以下中文翻译为英文：'人工智能正在改变我们的生活方式。'", "answer": "Artificial intelligence is changing our way of life."},
        {"id": "t2", "question": "将以下英文翻译为中文：'The rapid development of technology has brought both opportunities and challenges.'", "answer": "技术的快速发展既带来了机遇，也带来了挑战。"},
        {"id": "t3", "question": "将以下中文翻译为英文：'气候变化是全球面临的最严峻挑战之一。'", "answer": "Climate change is one of the most severe challenges facing the world."},
        {"id": "t4", "question": "将以下英文翻译为中文：'Machine learning algorithms can identify patterns in large datasets.'", "answer": "机器学习算法可以识别大型数据集中的模式。"},
        {"id": "t5", "question": "将以下中文翻译为英文：'教育是推动社会进步的重要力量。'", "answer": "Education is an important force driving social progress."},
        {"id": "t6", "question": "将以下英文翻译为中文：'Renewable energy sources such as solar and wind power are becoming increasingly cost-competitive.'", "answer": "太阳能和风能等可再生能源正变得日益具有成本竞争力。"},
        {"id": "t7", "question": "将以下中文翻译为英文：'健康饮食和规律运动对预防慢性病至关重要。'", "answer": "Healthy diet and regular exercise are crucial for preventing chronic diseases."},
        {"id": "t8", "question": "将以下英文翻译为中文：'The Internet of Things connects everyday devices to the internet, enabling data exchange and remote control.'", "answer": "物联网将日常设备连接到互联网，实现数据交换和远程控制。"},
        {"id": "t9", "question": "将以下中文翻译为英文：'科技创新需要持续的资金投入和人才培养。'", "answer": "Technological innovation requires continuous capital investment and talent cultivation."},
        {"id": "t10", "question": "将以下英文翻译为中文：'Sustainable development meets the needs of the present without compromising the ability of future generations to meet their own needs.'", "answer": "可持续发展满足当代人的需求，而不损害后代满足其自身需求的能力。"},
    ],
    "chinese": [
        {"id": "z1", "question": "请解释成语'刻舟求剑'的含义和寓意。", "answer": "比喻不懂事物已发展变化而仍静止地看问题"},
        {"id": "z2", "question": "《红楼梦》的作者是谁？它在中国文学史上的地位如何？", "answer": "曹雪芹，中国古典四大名著之一，巅峰之作"},
        {"id": "z3", "question": "请解释'天人合一'的哲学思想。", "answer": "强调人与自然和谐统一，人应顺应自然规律"},
        {"id": "z4", "question": "中国四大发明是什么？它们对世界文明有什么影响？", "answer": "造纸术、印刷术、火药、指南针，推动了世界文明发展进程"},
        {"id": "z5", "question": "请解释'塞翁失马，焉知非福'的寓意。", "answer": "坏事可能变成好事，祸福相依，要用发展的眼光看问题"},
        {"id": "z6", "question": "《论语》的核心思想是什么？请举出三条经典语录。", "answer": "仁、义、礼、智、信。经典语录：学而时习之、己所不欲勿施于人、三人行必有我师"},
        {"id": "z7", "question": "请解释'破釜沉舟'的典故和含义。", "answer": "项羽背水一战，比喻下定决心，不顾一切干到底"},
        {"id": "z8", "question": "中国二十四节气中，立春、立夏、立秋、立冬分别有什么含义？", "answer": "分别标志四季的开始"},
        {"id": "z9", "question": "请解释'卧薪尝胆'的故事和寓意。", "answer": "勾践忍辱负重，发愤图强，形容刻苦自励，发奋图强"},
        {"id": "z10", "question": "《道德经》的核心思想是什么？'道可道非常道'怎么理解？", "answer": "道法自然，无为而治。'道可道非常道'：可以用语言表述的道，就不是永恒不变的道"},
    ],
}


class BenchmarkSuite:
    """Model performance benchmark suite."""

    DIMENSIONS = ["reasoning", "code", "long_text", "translation", "chinese", "speed"]

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".cn-model-gateway" / "benchmark.db")
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            # Enable WAL mode for concurrent multi-process access (v1.4.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS benchmark_results (
                    id TEXT PRIMARY KEY,
                    run_id TEXT,
                    timestamp REAL,
                    provider TEXT,
                    model TEXT,
                    dimension TEXT,
                    score REAL,
                    duration_ms INTEGER,
                    prompt_tokens INTEGER DEFAULT 0,
                    completion_tokens INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS benchmark_runs (
                    run_id TEXT PRIMARY KEY,
                    timestamp REAL,
                    providers_tested TEXT,
                    dimensions_tested TEXT,
                    total_questions INTEGER
                )
            """)
            conn.commit()

    def run_benchmark(self, router: ModelRouter,
                      providers: Optional[List[str]] = None,
                      dimensions: Optional[List[str]] = None,
                      max_questions: Optional[int] = None) -> Dict[str, Any]:
        """Run benchmark for specified providers and dimensions.

        Args:
            router: ModelRouter instance
            providers: List of providers to test (default: all available)
            dimensions: List of dimensions to test (default: all)
            max_questions: Max questions per dimension (default: all)

        Returns:
            Benchmark results dict
        """
        target_providers = providers or router.list_available()
        if not target_providers:
            raise RuntimeError("没有可用的模型提供商。请先在 config.json 中配置 api_key。")

        target_dims = dimensions or self.DIMENSIONS
        run_id = str(uuid.uuid4())[:8]
        timestamp = time.time()

        print(f"📊 开始基准测试")
        print(f"   提供商: {target_providers}")
        print(f"   维度: {target_dims}")
        print(f"   ⚠️  注意：跑分将消耗 API 额度，预计约 ¥0.5-2")
        print()

        results: Dict[str, Any] = {
            "run_id": run_id,
            "timestamp": timestamp,
            "providers": {},
            "dimensions": target_dims,
        }

        for provider in target_providers:
            adapter = router.get_adapter(provider)
            if not adapter or not adapter.is_available():
                continue

            print(f"### {provider}")
            provider_results: Dict[str, Any] = {}

            for dim in target_dims:
                questions = QUESTION_BANK.get(dim, [])
                if max_questions:
                    questions = questions[:max_questions]

                if not questions:
                    continue

                print(f"  [{dim}] 测试中... ({len(questions)} 题)")
                dim_score = 0.0
                dim_duration = 0
                dim_prompt_tokens = 0
                dim_completion_tokens = 0

                for q in questions:
                    msgs = [ChatMessage(role="user", content=q["question"])]
                    try:
                        resp = router.chat(msgs, provider=provider, max_tokens=500)
                        dim_duration += resp.duration_ms
                        dim_prompt_tokens += resp.usage.get("prompt_tokens", 0)
                        dim_completion_tokens += resp.usage.get("completion_tokens", 0)
                        # Simple scoring: check if key terms from answer appear in response
                        key_terms = q["answer"].split()
                        matches = sum(1 for term in key_terms if term in resp.content)
                        score = min(1.0, matches / max(1, len(key_terms)))
                        dim_score += score
                    except Exception as e:
                        print(f"    题目 {q['id']} 失败: {e}")

                avg_score = dim_score / len(questions) if questions else 0
                provider_results[dim] = {
                    "score": round(avg_score, 3),
                    "duration_ms": dim_duration,
                    "avg_duration_ms": dim_duration // len(questions) if questions else 0,
                    "prompt_tokens": dim_prompt_tokens,
                    "completion_tokens": dim_completion_tokens,
                }

                # Save individual result
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        "INSERT INTO benchmark_results (id, run_id, timestamp, provider, model, dimension, score, duration_ms, prompt_tokens, completion_tokens) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (str(uuid.uuid4())[:8], run_id, timestamp, provider,
                         adapter.default_model, dim, avg_score, dim_duration,
                         dim_prompt_tokens, dim_completion_tokens),
                    )
                    conn.commit()

            results["providers"][provider] = provider_results

        # Save run summary
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO benchmark_runs (run_id, timestamp, providers_tested, dimensions_tested, total_questions) "
                "VALUES (?, ?, ?, ?, ?)",
                (run_id, timestamp, json.dumps(target_providers), json.dumps(target_dims), 50),
            )
            conn.commit()

        return results

    def generate_radar_chart(self, results: Dict[str, Any]) -> str:
        """Generate ASCII radar chart for comparison.

        Args:
            results: Benchmark results from run_benchmark()

        Returns:
            ASCII art radar chart string
        """
        providers = list(results["providers"].keys())
        dimensions = results.get("dimensions", self.DIMENSIONS)

        lines = ["📊 雷达图对比（文本版）\n"]
        lines.append("维度: " + " / ".join(dimensions))
        lines.append("")

        # Table header
        header = f"{'Provider':<15}" + "".join(f"{d:<12}" for d in dimensions) + "Avg"
        lines.append(header)
        lines.append("-" * len(header))

        for provider in providers:
            provider_data = results["providers"][provider]
            row = f"{provider:<15}"
            total_score = 0
            count = 0
            for dim in dimensions:
                dim_data = provider_data.get(dim, {})
                score = dim_data.get("score", 0)
                total_score += score
                count += 1
                bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
                row += f"{bar:<12}"
            avg = total_score / count if count else 0
            row += f"{avg:.1%}"
            lines.append(row)

        lines.append("")
        lines.append("图例: █ = 10% 得分率")
        return "\n".join(lines)

    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get benchmark run history.

        Args:
            limit: Maximum number of runs to return

        Returns:
            List of benchmark run records
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM benchmark_runs ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def get_run_details(self, run_id: str) -> List[Dict[str, Any]]:
        """Get detailed results for a specific run.

        Args:
            run_id: Run ID to query

        Returns:
            List of benchmark result records
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM benchmark_results WHERE run_id = ? ORDER BY provider, dimension",
                (run_id,)
            ).fetchall()
        return [dict(r) for r in rows]
