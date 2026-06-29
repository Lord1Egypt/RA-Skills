/**
 * 代码知识库 - CodeKnowledge
 *
 * 功能：存储和检索代码模式片段，支持关键词搜索和语义相似度匹配
 * 设计参考：
 *   - MeaningfulMemory 三层架构（hot/warm/cold）
 *   - LessonBank 教训存储模式
 *   - memory.js 的 atomicWriteJson 原子写入
 *
 * @author Clarity
 * @version 2.0.0
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ═══════════════════════════════════════════════════════════════════════════════
// 常量配置
// ═══════════════════════════════════════════════════════════════════════════════

const DATA_DIR = path.join(__dirname, '../../../data/code-knowledge');
const SNIPPETS_FILE = path.join(DATA_DIR, 'snippets.json');
const INDEX_FILE = path.join(DATA_DIR, 'index.json');
const FAILED_PATTERNS_FILE = path.join(DATA_DIR, 'failed-patterns.json');
const TASK_ASSOCIATIONS_FILE = path.join(DATA_DIR, 'task-associations.json');

// 错误类型分类
const ERROR_TYPES = {
  SYNTAX: 'syntax_error',
  RUNTIME: 'runtime_error',
  TYPE: 'type_error',
  IMPORT: 'import_error',
  REFERENCE: 'reference_error',
  LOGIC: 'logic_error',
  DEPENDENCY: 'dependency_error',
  CONFIG: 'config_error',
  TIMEOUT: 'timeout_error',
  UNKNOWN: 'unknown_error',
};

// 三层架构配置（类似 MeaningfulMemory）
const TIER_CONFIG = {
  hot: {
    // 热门模式：usageCount > 10 或 successRate > 0.9
    minUsageCount: 10,
    minSuccessRate: 0.9,
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7天内活跃
  },
  warm: {
    // 温热模式：usageCount 3-10 或 successRate 0.7-0.9
    minUsageCount: 3,
    minSuccessRate: 0.7,
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30天内
  },
  cold: {
    // 冷门模式：usageCount < 3 或 successRate < 0.7
    minUsageCount: 0,
    minSuccessRate: 0,
    maxAge: 365 * 24 * 60 * 60 * 1000, // 一年
  },
};

// 进化配置
const EVOLUTION_CONFIG = {
  minQuality: 20,         // 质量评分低于此值淘汰
  minUsageToSurvive: 5,    // 使用次数低于此值但成功率低则淘汰
  badSuccessRate: 0.3,    // 成功率低于此值标记为低质量
  maxSnippets: 500,       // 最大片段数量
  keepTopPercent: 0.8,    // 淘汰后保留前 80%
};

// 支持的语言列表
const SUPPORTED_LANGUAGES = [
  'javascript', 'typescript', 'python', 'go', 'rust', 'java',
  'cpp', 'c', 'csharp', 'php', 'ruby', 'swift', 'kotlin',
  'shell', 'bash', 'sql', 'html', 'css', 'json', 'yaml', 'markdown'
];

// 支持的类别
const SUPPORTED_CATEGORIES = [
  'algorithm',    // 算法（排序、搜索等）
  'structure',    // 数据结构
  'network',      // 网络编程
  'io',           // 输入输出/文件操作
  'utility',      // 工具函数
  'pattern',      // 设计模式
  'database',     // 数据库
  'concurrency',  // 并发编程
  'testing',      // 测试
  'security',     // 安全相关
  'performance',  // 性能优化
  'parsing',      // 解析/序列化
];

// ═══════════════════════════════════════════════════════════════════════════════
// 模式提取配置
// ═══════════════════════════════════════════════════════════════════════════════

// 各语言的关键字和保留字（用于识别函数/类定义）
const LANGUAGE_KEYWORDS = {
  javascript: ['const', 'let', 'var', 'function', 'async', 'await', 'class', 'extends', 'import', 'export', 'return', 'if', 'else', 'for', 'while', 'try', 'catch', 'throw', 'new', 'this', 'super'],
  typescript: ['const', 'let', 'var', 'function', 'async', 'await', 'class', 'extends', 'import', 'export', 'return', 'if', 'else', 'for', 'while', 'try', 'catch', 'throw', 'new', 'this', 'super', 'interface', 'type', 'enum', 'implements', 'private', 'public', 'protected'],
  python: ['def', 'class', 'import', 'from', 'return', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'raise', 'with', 'as', 'lambda', 'yield', 'async', 'await', 'pass', 'break', 'continue', 'global', 'nonlocal'],
  go: ['func', 'package', 'import', 'type', 'struct', 'interface', 'return', 'if', 'else', 'for', 'range', 'switch', 'case', 'default', 'select', 'defer', 'go', 'chan', 'map', 'make', 'new', 'nil', 'var', 'const'],
  rust: ['fn', 'let', 'mut', 'const', 'struct', 'enum', 'impl', 'trait', 'pub', 'mod', 'use', 'import', 'return', 'if', 'else', 'match', 'for', 'while', 'loop', 'match', 'async', 'await', 'move', 'ref', 'self', 'Self'],
  java: ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'static', 'final', 'void', 'return', 'if', 'else', 'for', 'while', 'do', 'try', 'catch', 'finally', 'throw', 'throws', 'new', 'this', 'super'],
  cpp: ['int', 'void', 'class', 'struct', 'public', 'private', 'protected', 'virtual', 'override', 'template', 'typename', 'namespace', 'using', 'return', 'if', 'else', 'for', 'while', 'do', 'try', 'catch', 'throw', 'new', 'delete', 'const', 'static'],
};

// 常见框架/库的导入模式
const FRAMEWORK_PATTERNS = [
  // React/Vue/Angular
  { pattern: /from\s+['"]react['"]|import\s+.*\s+from\s+['"]react['"]/, framework: 'react', category: 'frontend' },
  { pattern: /from\s+['"]vue['"]|import\s+.*\s+from\s+['"]vue['"]/, framework: 'vue', category: 'frontend' },
  { pattern: /from\s+['"]@angular\/core['"]/, framework: 'angular', category: 'frontend' },
  // Node.js 框架
  { pattern: /from\s+['"]express['"]|require\s*\(\s*['"]express['"]/, framework: 'express', category: 'backend' },
  { pattern: /from\s+['"]fastify['"]|require\s*\(\s*['"]fastify['"]/, framework: 'fastify', category: 'backend' },
  { pattern: /from\s+['"]koa['"]|require\s*\(\s*['"]koa['"]/, framework: 'koa', category: 'backend' },
  { pattern: /from\s+['"]next['"]|require\s*\(\s*['"]next['"]/, framework: 'nextjs', category: 'framework' },
  // Python 框架
  { pattern: /from\s+(flask|fastapi|django)\b|import\s+(flask|fastapi|django)/, framework: '$1', category: 'backend' },
  { pattern: /from\s+requests|import\s+requests/, framework: 'requests', category: 'http' },
  { pattern: /from\s+selenium|import\s+selenium/, framework: 'selenium', category: 'testing' },
  // Go 框架
  { pattern: /gin-gonic\/gin|github\.com\/gin-gonic\/gin/, framework: 'gin', category: 'backend' },
  { pattern: /gorilla\/mux|github\.com\/gorilla\/mux/, framework: 'mux', category: 'backend' },
  // 数据库
  { pattern: /sequelize|prisma|typeorm/, framework: '$1', category: 'orm' },
  { pattern: /mongoose|mongodb|@mongodb/, framework: 'mongodb', category: 'database' },
  { pattern: /redis|ioredis/, framework: 'redis', category: 'cache' },
  // 工具库
  { pattern: /lodash|underscore/, framework: 'lodash', category: 'utility' },
  { pattern: /axios|node-fetch|got|http\./, framework: '$1', category: 'http' },
  { pattern: /jest|mocha|chai|vitest/, framework: '$1', category: 'testing' },
];

// 控制流关键词（用于识别算法复杂度）
const CONTROL_FLOW_KEYWORDS = ['for', 'while', 'forEach', 'map', 'filter', 'reduce', 'recursion', 'recursive', 'loop'];

// 算法复杂度关键词
const COMPLEXITY_KEYWORDS = {
  O1: ['hash', 'map', 'set', 'lookup', 'get', 'push', 'pop'],
  Ologn: ['binary', 'search', 'divide', 'conquer', 'heap', 'priority'],
  On: ['loop', 'iterate', 'scan', 'traverse', 'each', 'forEach'],
  Onlogn: ['sort', 'merge', 'quick'],
  On2: ['nested', 'double', 'matrix', 'grid', 'table'],
};

// ═══════════════════════════════════════════════════════════════════════════════
// 内置模式库 - 常用算法和数据结构
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 内置代码模式库
 * 包含常见算法和数据结构的参考实现
 */
const BUILTIN_PATTERNS = [
  // ═══════════════════════════════════════════════════════════════════════════
  // 算法 - 排序
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'algorithm',
    name: '快速排序',
    tags: ['排序', 'quickSort', '分治', '原地排序'],
    description: '快速排序实现，使用原地分区，平均时间复杂度 O(n log n)',
    code: `/**
 * 快速排序 - JavaScript 实现
 * 时间复杂度: 平均 O(n log n)，最坏 O(n²)
 * 空间复杂度: O(log n)
 */
function quickSort(arr, low = 0, high = arr.length - 1) {
  if (low < high) {
    const pivotIndex = partition(arr, low, high);
    quickSort(arr, low, pivotIndex - 1);
    quickSort(arr, pivotIndex + 1, high);
  }
  return arr;
}

function partition(arr, low, high) {
  const pivot = arr[high];
  let i = low - 1;
  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}`,
    quality: 95,
  },
  {
    language: 'javascript',
    category: 'algorithm',
    name: '归并排序',
    tags: ['排序', 'mergeSort', '分治', '稳定排序'],
    description: '归并排序实现，稳定排序，时间复杂度 O(n log n)',
    code: `/**
 * 归并排序 - JavaScript 实现
 * 时间复杂度: O(n log n)
 * 空间复杂度: O(n)
 * 特点: 稳定排序
 */
function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let i = 0, j = 0;

  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i++]);
    } else {
      result.push(right[j++]);
    }
  }

  return result.concat(left.slice(i)).concat(right.slice(j));
}`,
    quality: 90,
  },
  {
    language: 'python',
    category: 'algorithm',
    name: '堆排序',
    tags: ['排序', 'heapSort', '二叉堆', '原地排序'],
    description: '堆排序实现，使用二叉堆数据结构',
    code: `"""
堆排序 - Python 实现
时间复杂度: O(n log n)
空间复杂度: O(1)
"""
def heap_sort(arr):
    n = len(arr)

    # 构建最大堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 逐个提取元素
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)`,
    quality: 88,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 算法 - 搜索
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'algorithm',
    name: '二分查找',
    tags: ['搜索', 'binarySearch', '有序数组', '对数时间'],
    description: '二分查找算法，适用于有序数组',
    code: `/**
 * 二分查找 - JavaScript 实现
 * 时间复杂度: O(log n)
 * 前提: 数组必须已排序
 */
function binarySearch(arr, target) {
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (arr[mid] === target) {
      return mid;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1; // 未找到
}

// 递归版本
function binarySearchRecursive(arr, target, left = 0, right = arr.length - 1) {
  if (left > right) return -1;

  const mid = Math.floor((left + right) / 2);

  if (arr[mid] === target) return mid;
  if (arr[mid] < target) {
    return binarySearchRecursive(arr, target, mid + 1, right);
  }
  return binarySearchRecursive(arr, target, left, mid - 1);
}`,
    quality: 95,
  },
  {
    language: 'python',
    category: 'algorithm',
    name: '二分查找',
    tags: ['搜索', 'binarySearch', '有序数组', '对数时间'],
    description: '二分查找算法 Python 实现',
    code: `"""
二分查找 - Python 实现
时间复杂度: O(log n)
"""
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # 未找到`,
    quality: 95,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 数据结构 - 树
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'structure',
    name: '二叉树遍历',
    tags: ['树', 'binaryTree', '遍历', 'DFS', 'BFS'],
    description: '二叉树的前序、中序、后序遍历（递归和迭代）',
    code: `/**
 * 二叉树遍历
 */
class TreeNode {
  constructor(val) {
    this.val = val;
    this.left = null;
    this.right = null;
  }
}

// 前序遍历: 根-左-右
function preorderTraversal(root) {
  const result = [];
  function traverse(node) {
    if (!node) return;
    result.push(node.val);
    traverse(node.left);
    traverse(node.right);
  }
  traverse(root);
  return result;
}

// 中序遍历: 左-根-右
function inorderTraversal(root) {
  const result = [];
  function traverse(node) {
    if (!node) return;
    traverse(node.left);
    result.push(node.val);
    traverse(node.right);
  }
  traverse(root);
  return result;
}

// 后序遍历: 左-右-根
function postorderTraversal(root) {
  const result = [];
  function traverse(node) {
    if (!node) return;
    traverse(node.left);
    traverse(node.right);
    result.push(node.val);
  }
  traverse(root);
  return result;
}

// 层序遍历 (BFS)
function levelOrderTraversal(root) {
  if (!root) return [];
  const result = [];
  const queue = [root];

  while (queue.length > 0) {
    const node = queue.shift();
    result.push(node.val);
    if (node.left) queue.push(node.left);
    if (node.right) queue.push(node.right);
  }

  return result;
}`,
    quality: 90,
  },
  {
    language: 'python',
    category: 'structure',
    name: '二叉树遍历',
    tags: ['树', 'binaryTree', '遍历', 'DFS', 'BFS'],
    description: '二叉树遍历 Python 实现',
    code: `"""
二叉树遍历
"""
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_traversal(root):
    """前序遍历: 根-左-右"""
    result = []

    def traverse(node):
        if not node:
            return
        result.append(node.val)
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    return result

def level_order_traversal(root):
    """层序遍历 (BFS)"""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result`,
    quality: 88,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 数据结构 - 图
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'structure',
    name: '图的 BFS 和 DFS',
    tags: ['图', 'graph', 'BFS', 'DFS', '遍历'],
    description: '图的广度优先搜索和深度优先搜索实现',
    code: `/**
 * 图的遍历 - BFS 和 DFS
 */

// BFS (广度优先搜索) - 使用队列
function bfs(graph, start) {
  const visited = new Set();
  const result = [];
  const queue = [start];

  while (queue.length > 0) {
    const node = queue.shift();
    if (visited.has(node)) continue;

    visited.add(node);
    result.push(node);

    for (const neighbor of (graph[node] || [])) {
      if (!visited.has(neighbor)) {
        queue.push(neighbor);
      }
    }
  }

  return result;
}

// DFS (深度优先搜索) - 使用栈或递归
function dfs(graph, start) {
  const visited = new Set();
  const result = [];

  function traverse(node) {
    if (visited.has(node)) return;

    visited.add(node);
    result.push(node);

    for (const neighbor of (graph[node] || [])) {
      traverse(neighbor);
    }
  }

  traverse(start);
  return result;
}

// DFS 迭代版本
function dfsIterative(graph, start) {
  const visited = new Set();
  const result = [];
  const stack = [start];

  while (stack.length > 0) {
    const node = stack.pop();
    if (visited.has(node)) continue;

    visited.add(node);
    result.push(node);

    for (const neighbor of (graph[node] || []).reverse()) {
      if (!visited.has(neighbor)) {
        stack.push(neighbor);
      }
    }
  }

  return result;
}`,
    quality: 85,
  },
  {
    language: 'python',
    category: 'structure',
    name: '图的 BFS 和 DFS',
    tags: ['图', 'graph', 'BFS', 'DFS', '遍历'],
    description: '图的遍历 Python 实现',
    code: `"""
图的遍历 - BFS 和 DFS
"""
from collections import deque

def bfs(graph, start):
    """广度优先搜索"""
    visited = set()
    result = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node in visited:
            continue

        visited.add(node)
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append(neighbor)

    return result

def dfs(graph, start):
    """深度优先搜索（递归）"""
    visited = set()
    result = []

    def traverse(node):
        if node in visited:
            return
        visited.add(node)
        result.append(node)
        for neighbor in graph.get(node, []):
            traverse(neighbor)

    traverse(start)
    return result`,
    quality: 85,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 算法 - 动态规划
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'algorithm',
    name: '斐波那契数列',
    tags: ['动态规划', 'DP', 'fibonacci', '记忆化'],
    description: '斐波那契数列的多种实现方式对比',
    code: `/**
 * 斐波那契数列 - 多种实现对比
 */

// 暴力递归 (指数时间 - 不推荐)
function fibNaive(n) {
  if (n <= 1) return n;
  return fibNaive(n - 1) + fibNaive(n - 2);
}

// 记忆化递归 (线性时间)
function fibMemo(n, memo = {}) {
  if (n <= 1) return n;
  if (memo[n]) return memo[n];

  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n];
}

// 动态规划 (线性时间 + O(1) 空间)
function fibDP(n) {
  if (n <= 1) return n;

  let prev2 = 0, prev1 = 1;
  for (let i = 2; i <= n; i++) {
    const curr = prev1 + prev2;
    prev2 = prev1;
    prev1 = curr;
  }
  return prev1;
}

// 矩阵快速幂 (对数时间)
function fibMatrix(n) {
  if (n <= 1) return n;

  function multiply(a, b) {
    return [
      a[0][0] * b[0][0] + a[0][1] * b[1][0],
      a[0][0] * b[0][1] + a[0][1] * b[1][1],
      a[1][0] * b[0][0] + a[1][1] * b[1][0],
      a[1][0] * b[0][1] + a[1][1] * b[1][1],
    ];
  }

  function power(matrix, n) {
    if (n === 1) return matrix;
    if (n % 2 === 0) {
      const half = power(matrix, n / 2);
      return multiply(half, half);
    }
    return multiply(matrix, power(matrix, n - 1));
  }

  const result = power([1, 1, 1, 0], n - 1);
  return result[0];
}`,
    quality: 88,
  },
  {
    language: 'javascript',
    category: 'algorithm',
    name: '最长公共子序列',
    tags: ['动态规划', 'DP', 'LCS', '字符串'],
    description: '最长公共子序列的动态规划实现',
    code: `/**
 * 最长公共子序列 (LCS) - 动态规划
 * 时间复杂度: O(m * n)
 * 空间复杂度: O(m * n)
 */
function longestCommonSubsequence(s1, s2) {
  const m = s1.length;
  const n = s2.length;

  // 创建 DP 表
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  // 填充 DP 表
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (s1[i - 1] === s2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // 回溯找出 LCS
  let lcs = '';
  let i = m, j = n;
  while (i > 0 && j > 0) {
    if (s1[i - 1] === s2[j - 1]) {
      lcs = s1[i - 1] + lcs;
      i--;
      j--;
    } else if (dp[i - 1][j] > dp[i][j - 1]) {
      i--;
    } else {
      j--;
    }
  }

  return {
    length: dp[m][n],
    subsequence: lcs,
  };
}`,
    quality: 82,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 工具函数
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'utility',
    name: '防抖和节流',
    tags: ['防抖', 'debounce', '节流', 'throttle', '性能'],
    description: '防抖和节流函数的实现',
    code: `/**
 * 防抖 (debounce) - 在事件触发 n 秒后执行，n 秒内再次触发则重新计时
 * @param {Function} func - 要执行的函数
 * @param {number} delay - 延迟时间（毫秒）
 */
function debounce(func, delay = 300) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

/**
 * 节流 (throttle) - 规定时间内只执行一次
 * @param {Function} func - 要执行的函数
 * @param {number} limit - 时间限制（毫秒）
 */
function throttle(func, limit = 300) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// 带取消功能的版本
function debounceWithCancel(func, delay = 300) {
  let timeoutId;
  const debounced = function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
  debounced.cancel = () => clearTimeout(timeoutId);
  return debounced;
}`,
    quality: 92,
  },
  {
    language: 'javascript',
    category: 'utility',
    name: '深拷贝',
    tags: ['深拷贝', 'deepClone', '对象复制'],
    description: '深拷贝的多种实现方式',
    code: `/**
 * 深拷贝 - 多种实现方式
 */

// JSON 方法（简单但有局限：不支持函数、undefined、Symbol、循环引用）
function deepCloneJson(obj) {
  return JSON.parse(JSON.stringify(obj));
}

// 递归拷贝
function deepCloneRecursive(obj, visited = new WeakMap()) {
  // 处理基本类型
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  // 处理循环引用
  if (visited.has(obj)) {
    return visited.get(obj);
  }

  // 处理 Date
  if (obj instanceof Date) {
    return new Date(obj.getTime());
  }

  // 处理 RegExp
  if (obj instanceof RegExp) {
    return new RegExp(obj.source, obj.flags);
  }

  // 处理数组和普通对象
  const clone = Array.isArray(obj) ? [] : {};
  visited.set(obj, clone);

  for (const key of Object.keys(obj)) {
    clone[key] = deepCloneRecursive(obj[key], visited);
  }

  return clone;
}

// 结构化克隆（现代浏览器/Node.js）
function deepCloneStructured(obj) {
  return structuredClone(obj);
}`,
    quality: 90,
  },
  {
    language: 'python',
    category: 'utility',
    name: '深拷贝',
    tags: ['深拷贝', 'deepClone', '对象复制'],
    description: 'Python 深拷贝实现',
    code: `"""
深拷贝 - Python 实现
"""
import copy
from typing import Any

def deep_clone(obj: Any) -> Any:
    """深拷贝"""
    return copy.deepcopy(obj)

# 或者手动实现
def deep_copy_manual(obj, visited=None):
    """手动深拷贝实现"""
    if visited is None:
        visited = {}

    if id(obj) in visited:
        return visited[id(obj)]

    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj

    if isinstance(obj, (list, tuple)):
        visited[id(obj)] = result = []
        result.extend(deep_copy_manual(item, visited) for item in obj)
        return tuple(result) if isinstance(obj, tuple) else result

    if isinstance(obj, dict):
        visited[id(obj)] = result = {}
        for k, v in obj.items():
            result[deep_copy_manual(k, visited)] = deep_copy_manual(v, visited)
        return result

    # 对于其他对象，使用 copy 模块
    visited[id(obj)] = result = copy.copy(obj)
    return result`,
    quality: 88,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 网络编程
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'network',
    name: 'Promise 超时处理',
    tags: ['Promise', '超时', 'timeout', 'async'],
    description: 'Promise 超时处理的多种实现',
    code: `/**
 * Promise 超时处理
 */

/**
 * 带超时的 Promise
 * @param {Promise} promise - 原 Promise
 * @param {number} ms - 超时毫秒数
 * @param {Error} timeoutError - 超时时抛出的错误
 */
function withTimeout(promise, ms, timeoutError = new Error('Promise timeout')) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(timeoutError), ms)
    )
  ]);
}

/**
 * 带取消的 Promise
 */
function withAbort(promise) {
  let abortFn = null;
  const abortPromise = new Promise((_, reject) => {
    abortFn = () => reject(new Error('Aborted'));
  });

  const wrapped = Promise.race([promise, abortPromise]);
  wrapped.abort = abortFn;

  return wrapped;
}

/**
 * 带重试的 Promise
 * @param {Function} fn - 要执行的异步函数
 * @param {number} retries - 重试次数
 * @param {number} delay - 重试间隔（毫秒）
 */
async function withRetry(fn, retries = 3, delay = 1000) {
  let lastError;
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e;
      if (i < retries) await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
    }
  }
  throw lastError;
}`,
    quality: 88,
  },
  {
    language: 'python',
    category: 'network',
    name: '异步 HTTP 请求',
    tags: ['HTTP', 'async', 'aiohttp', '异步'],
    description: 'Python 异步 HTTP 请求实现',
    code: `"""
异步 HTTP 请求 - Python 实现
需要安装: pip install aiohttp
"""
import asyncio
import aiohttp

async def fetch(url, timeout=30):
    """异步获取 URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            return await response.text()

async def fetch_all(urls):
    """并发获取多个 URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# 使用示例
async def main():
    urls = [
        'https://api.example.com/data/1',
        'https://api.example.com/data/2',
        'https://api.example.com/data/3',
    ]
    results = await fetch_all(urls)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"URL {i} failed: {result}")
        else:
            print(f"URL {i} succeeded: {len(result)} bytes")

if __name__ == '__main__':
    asyncio.run(main())`,
    quality: 85,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 设计模式
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'pattern',
    name: '单例模式',
    tags: ['单例', 'singleton', '设计模式'],
    description: '单例模式的多种实现',
    code: `/**
 * 单例模式 - 多种实现方式
 */

// 1. 简单单例（懒加载）
const SimpleSingleton = (function() {
  let instance;
  return function() {
    if (instance) return instance;
    instance = new SingletonClass();
    return instance;
  };
})();

// 2. 闭包单例（带私有成员）
const ClosureSingleton = (function() {
  let instance;

  function SingletonClass() {
    // 私有成员
    const privateData = [];

    // 公有接口
    return {
      add: (item) => privateData.push(item),
      get: () => [...privateData],
      size: () => privateData.length,
    };
  }

  return function() {
    if (instance) return instance;
    instance = SingletonClass();
    return instance;
  };
})();

// 3. 类实现（ES6）
class Singleton {
  static #instance = null;

  constructor() {
    if (Singleton.#instance) {
      return Singleton.#instance;
    }
    Singleton.#instance = this;
    this.data = [];
  }

  static getInstance() {
    if (!Singleton.#instance) {
      Singleton.#instance = new Singleton();
    }
    return Singleton.#instance;
  }

  add(item) {
    this.data.push(item);
  }

  get() {
    return [...this.data];
  }
}`,
    quality: 88,
  },
  {
    language: 'javascript',
    category: 'pattern',
    name: '发布订阅模式',
    tags: ['发布订阅', 'pub/sub', '观察者', '设计模式'],
    description: '发布订阅模式实现',
    code: `/**
 * 发布订阅模式 (Pub/Sub)
 */
class PubSub {
  constructor() {
    this.topics = {};
    this.subUid = 0;
  }

  /**
   * 订阅主题
   * @param {string} topic - 主题名称
   * @param {Function} callback - 回调函数
   * @returns {string} 订阅 ID
   */
  subscribe(topic, callback) {
    if (!this.topics[topic]) {
      this.topics[topic] = [];
    }

    const token = 'sub_' + (++this.subUid);
    this.topics[topic].push({ token, callback });

    return token;
  }

  /**
   * 发布消息
   * @param {string} topic - 主题名称
   * @param {*} message - 消息内容
   */
  publish(topic, message) {
    if (!this.topics[topic]) {
      return false;
    }

    const subscribers = this.topics[topic];
    for (const { callback } of subscribers) {
      try {
        callback(message);
      } catch (e) {
        console.error('PubSub callback error:', e);
      }
    }

    return true;
  }

  /**
   * 取消订阅
   * @param {string} token - 订阅 ID
   */
  unsubscribe(token) {
    for (const topic in this.topics) {
      const index = this.topics[topic].findIndex(s => s.token === token);
      if (index !== -1) {
        this.topics[topic].splice(index, 1);
        return true;
      }
    }
    return false;
  }
}

// 使用示例
// pubsub.publish('user:login', { name: 'Alice' });`,
    quality: 90,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 并发编程
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'concurrency',
    name: 'Promise 并发控制',
    tags: ['Promise', '并发控制', 'concurrency', 'pool'],
    description: 'Promise 并发控制，实现工作池',
    code: `/**
 * Promise 并发控制 - 工作池
 */

/**
 * 并发限制器
 * @param {Array} tasks - 任务数组（返回 Promise 的函数）
 * @param {number} limit - 并发限制数
 */
async function concurrentLimit(tasks, limit = 5) {
  const results = [];
  const executing = new Set();

  for (const task of tasks) {
    const promise = Promise.resolve().then(() => task());
    results.push(promise);

    const cleanup = () => executing.delete(promise);
    promise.then(cleanup).catch(cleanup);
    executing.add(promise);

    if (executing.size >= limit) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}

/**
 * 工作池实现
 */
class WorkerPool {
  constructor(size = 5) {
    this.size = size;
    this.queue = [];
    this.active = 0;
  }

  async addTask(task) {
    if (this.active < this.size) {
      this.active++;
      try {
        return await task();
      } finally {
        this.active--;
        this.processNext();
      }
    } else {
      return new Promise((resolve, reject) => {
        this.queue.push({ task, resolve, reject });
      });
    }
  }

  processNext() {
    if (this.queue.length > 0) {
      const { task, resolve, reject } = this.queue.shift();
      this.addTask(task).then(resolve).catch(reject);
    }
  }
}`,
    quality: 85,
  },
  {
    language: 'go',
    category: 'concurrency',
    name: 'Go 并发模式',
    tags: ['go', 'goroutine', 'channel', '并发'],
    description: 'Go 语言的常见并发模式',
    code: `package main

import (
	"fmt"
	"sync"
)

// Worker Pool - 工作池模式
func WorkerPool(jobs <-chan int, results chan<- int, numWorkers int) {
	var wg sync.WaitGroup

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerId int) {
			defer wg.Done()
			for job := range jobs {
				// 处理工作
				result := job * 2
				results <- result
			}
		}(i)
	}

	wg.Wait()
	close(results)
}

// Pipeline - 流水线模式
func Pipeline(nums []int) <-chan int {
	out := make(chan int)

	go func() {
		for _, n := range nums {
			out <- n * 2
		}
		close(out)
	}()

	return out
}

// Fan-out/Fan-in - 分发/收集
func FanOutFanIn(input <-chan int, numWorkers int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for n := range input {
				out <- process(n)
			}
		}()
	}

	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

func process(n int) int {
	return n * n
}

func main() {
	// 示例使用
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	// 启动工作池
	go WorkerPool(jobs, results, 5)

	// 发送任务
	for i := 1; i <= 20; i++ {
		jobs <- i
	}
	close(jobs)

	// 收集结果
	for result := range results {
		fmt.Println(result)
	}
}`,
    quality: 88,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // 数据库
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'javascript',
    category: 'database',
    name: '防 SQL 注入',
    tags: ['SQL注入', 'security', '数据库安全'],
    description: '防止 SQL 注入的安全实践',
    code: `/**
 * SQL 注入防护
 * ⚠️ 这是教育示例，实际使用请使用 ORM 或成熟的数据库库
 */

/**
 * 参数化查询（防止注入）
 * @param {string} sql - SQL 语句，使用 ? 占位符
 * @param {Array} params - 参数数组
 */
function safeQuery(sql, params) {
  // 使用参数化查询，参数会被正确转义
  const query = db.prepare(sql);
  return query.all(...params);
}

// 示例
// const userId = 123;
// safeQuery('SELECT * FROM users WHERE id = ?', [userId]);

// ❌ 危险：会被注入
// unsafeQuery: 注意此处演示了危险模式

// 关键字过滤（辅助手段）
function sanitizeInput(input) {
  const dangerous = [/[\\;\\-\\-/g, /\\/g, /\\/g, /%/g, /#/g, /\\(/g, /\\)/g];
  let sanitized = String(input);
  for (const pattern of dangerous) {
    sanitized = sanitized.replace(pattern, '');
  }
  return sanitized;
}`,
    quality: 92,
  },
  {
    language: 'python',
    category: 'database',
    name: 'SQLAlchemy 防注入',
    tags: ['SQLAlchemy', 'ORM', '数据库安全'],
    description: '使用 SQLAlchemy 的安全查询',
    code: `"""
SQLAlchemy 安全查询示例
pip install sqlalchemy
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 创建引擎
engine = create_engine('sqlite:///mydb.db')
Session = sessionmaker(bind=engine)

def safe_query(user_id: int):
    """安全的参数化查询"""
    with Session() as session:
        # 使用参数绑定，避免 SQL 注入
        result = session.execute(
            text("SELECT * FROM users WHERE id = :id"),
            {"id": user_id}
        )
        return result.fetchall()

def safe_search(search_term: str):
    """安全的模糊搜索"""
    with Session() as session:
        # 参数化查询，LIKE 也安全
        result = session.execute(
            text("SELECT * FROM users WHERE name LIKE :term"),
            {"term": f"%{search_term}%"}
        )
        return result.fetchall()

# 使用示例
users = safe_query(123)
results = safe_search("John")`,
    quality: 90,
  },

  // ═══════════════════════════════════════════════════════════════════════════
  // Shell 脚本
  // ═══════════════════════════════════════════════════════════════════════════
  {
    language: 'shell',
    category: 'utility',
    name: '目录备份脚本',
    tags: ['备份', 'backup', 'shell', 'tar'],
    description: '使用 tar 进行目录备份的脚本',
code: `#!/bin/bash
#
# 目录备份脚本
# 用法: ./backup.sh <源目录> [目标目录]
#

set -euo pipefail

log() {
    echo "[$(date +%Y-%m-%d_%H:%M:%S)] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

if [ $# -lt 1 ]; then
    echo "用法: $0 <源目录> [目标目录]"
    exit 1
fi

SRC_DIR="$1"
DEST_DIR="backup"

[ -d "$SRC_DIR" ] || error "源目录不存在: $SRC_DIR"
mkdir -p "$DEST_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BASENAME=$(basename "$SRC_DIR")
BACKUP_FILE="$DEST_DIR/\${BASENAME}_\${TIMESTAMP}.tar.gz"

log "开始备份: $SRC_DIR -> $BACKUP_FILE"
tar -czf "$BACKUP_FILE" "$SRC_DIR" || error "备份失败"

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log "备份完成: $BACKUP_FILE ($SIZE)"
log "清理旧备份..."
find "$DEST_DIR" -name "\${BASENAME}_*.tar.gz" -mtime +7 -delete
log "清理完成"
`,
    quality: 85,
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// CodeKnowledge 代码知识库类
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 代码知识库
 * 三层架构（hot/warm/cold）存储代码模式片段
 * 支持关键词搜索和基于标签的语义相似度匹配
 */
class CodeKnowledge {
  /**
   * @param {Object} opts
   * @param {string} opts.rootPath - 根路径（用于数据存储）
   */
  constructor({ rootPath }) {
    this.rootPath = rootPath || path.join(__dirname, '../../../..');
    this.dataDir = path.join(this.rootPath, 'data/code-knowledge');
    this.snippetsFile = path.join(this.dataDir, 'snippets.json');
    this.indexFile = path.join(this.dataDir, 'index.json');
    this.failedPatternsFile = path.join(this.dataDir, 'failed-patterns.json');
    this.taskAssociationsFile = path.join(this.dataDir, 'task-associations.json');
    this.snippets = [];
    this.index = null;
    this.failedPatterns = [];
    this.taskAssociations = {};
    this._dirty = false;
    this._load();
  }

  // 内部工具：原子写入 JSON
  _atomicWriteJson(filePath, data) {
    const tmp = filePath + '.tmp.' + Date.now() + '.json';
    fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
    fs.renameSync(tmp, filePath);
  }

  // 加载数据
  _load() {
    fs.mkdirSync(this.dataDir, { recursive: true });
    // 逐个加载文件，单个文件失败不影响其他数据
    try {
      if (fs.existsSync(this.snippetsFile)) {
        this.snippets = JSON.parse(fs.readFileSync(this.snippetsFile, 'utf8'));
      }
    } catch (e) {
      console.warn('[CodeKnowledge] 加载 snippets 失败:', e.message);
    }
    try {
      if (fs.existsSync(this.indexFile)) {
        this.index = JSON.parse(fs.readFileSync(this.indexFile, 'utf8'));
      }
    } catch (e) {
      console.warn('[CodeKnowledge] 加载 index 失败:', e.message);
    }
    try {
      if (fs.existsSync(this.failedPatternsFile)) {
        this.failedPatterns = JSON.parse(fs.readFileSync(this.failedPatternsFile, 'utf8'));
      }
    } catch (e) {
      console.warn('[CodeKnowledge] 加载失败模式失败:', e.message);
    }
    try {
      if (fs.existsSync(this.taskAssociationsFile)) {
        this.taskAssociations = JSON.parse(fs.readFileSync(this.taskAssociationsFile, 'utf8'));
      }
    } catch (e) {
      console.warn('[CodeKnowledge] 加载任务关联失败:', e.message);
    }
  }

  // 保存数据
  _save() {
    if (!this._dirty) return;
    fs.mkdirSync(this.dataDir, { recursive: true });
    this._atomicWriteJson(this.snippetsFile, this.snippets);
    this._updateIndex();
    this._dirty = false;
  }

  // 保存失败模式库
  _saveFailedPatterns() {
    fs.mkdirSync(this.dataDir, { recursive: true });
    this._atomicWriteJson(this.failedPatternsFile, this.failedPatterns);
  }

  // 保存任务关联
  _saveTaskAssociations() {
    fs.mkdirSync(this.dataDir, { recursive: true });
    this._atomicWriteJson(this.taskAssociationsFile, this.taskAssociations);
  }

  // 更新索引
  _updateIndex() {
    this.index = {
      lastUpdated: new Date().toISOString(),
      totalCount: this.snippets.length,
    };
    try {
      this._atomicWriteJson(this.indexFile, this.index);
    } catch (e) { /* 索引写入失败不影响主流程 */ }
  }

  // 获取分类层级
  _getTier(snippet) {
    const { usageCount = 0, successRate = 0 } = snippet;
    if (usageCount > 10 || successRate > 0.9) return 'hot';
    if (usageCount >= 3 || successRate > 0.7) return 'warm';
    return 'cold';
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // 深度模式学习 - 核心功能
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * 从代码中自动提取结构化标签
   * 使用正则+语法分析（简单实现，不依赖外部parser）
   *
   * @param {string} code - 代码文本
   * @param {string} language - 编程语言
   * @returns {Object} { category, tags[], imports[], exports[], complexity, languageFeatures[] }
   */
  extractPattern(code, language) {
    if (!code || !language) {
      return { category: 'unknown', tags: [], imports: [], exports: [], complexity: 'unknown', languageFeatures: [] };
    }

    const lang = language.toLowerCase();
    const tags = [];
    const imports = [];
    const exports = [];
    const languageFeatures = [];
    let category = 'utility';

    // 1. 提取 import 语句
    const importPatterns = this._getImportPatterns(lang);
    for (const pattern of importPatterns) {
      const matches = code.matchAll(new RegExp(pattern, 'g'));
      for (const match of matches) {
        imports.push(match[1] || match[0]);
      }
    }

    // 2. 提取 export 语句
    const exportPatterns = this._getExportPatterns(lang);
    for (const pattern of exportPatterns) {
      const matches = code.matchAll(new RegExp(pattern, 'g'));
      for (const match of matches) {
        exports.push(match[1] || match[0]);
      }
    }

    // 3. 提取函数签名（识别函数定义）
    const functions = this._extractFunctions(code, lang);
    tags.push(...functions.map(f => `fn:${f.name}`));

    // 4. 提取类定义
    const classes = this._extractClasses(code, lang);
    tags.push(...classes.map(c => `class:${c}`));

    // 5. 分析控制流（识别算法复杂度）
    const controlFlowScore = this._analyzeControlFlow(code);
    if (controlFlowScore.nested > 2) {
      tags.push('nested-loop');
      category = this._inferCategoryFromTags(tags, lang) || 'algorithm';
    } else if (controlFlowScore.recursion > 0) {
      tags.push('recursion');
      category = 'algorithm';
    }

    // 6. 检测框架/库使用
    for (const fp of FRAMEWORK_PATTERNS) {
      const frameworkName = fp.framework === '$1' ? this._extractFrameworkName(code, fp.pattern) : fp.framework;
      if (frameworkName && code.match(fp.pattern)) {
        tags.push(`framework:${frameworkName}`);
        languageFeatures.push({ type: 'framework', name: frameworkName, category: fp.category });
      }
    }

    // 7. 检测语言特定特性
    const features = this._detectLanguageFeatures(code, lang);
    languageFeatures.push(...features);

    // 8. 推断类别
    category = this._inferCategoryFromTags(tags, lang) || category;
    if (category === 'utility' && imports.some(i => i.includes('test'))) {
      category = 'testing';
    }

    // 9. 计算复杂度估计
    const complexity = this._estimateComplexity(code, controlFlowScore, functions);

    return {
      category,
      tags: [...new Set(tags)],  // 去重
      imports,
      exports,
      complexity,
      languageFeatures,
      _meta: {
        functionCount: functions.length,
        classCount: classes.length,
        lineCount: code.split('\n').length,
      },
    };
  }

  /**
   * 获取语言的 import 模式
   */
  _getImportPatterns(language) {
    const patterns = {
      javascript: [
        /import\s+(?:{[^}]+}|\w+)\s+from\s+['"]([^'"]+)['"]/g,
        /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g,
      ],
      typescript: [
        /import\s+(?:{[^}]+}|\w+)\s+from\s+['"]([^'"]+)['"]/g,
        /import\s+['"]([^'"]+)['"]/g,
        /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g,
      ],
      python: [
        /^import\s+(\w+)/gm,
        /^from\s+(\w+(?:\.\w+)*)\s+import/gm,
      ],
      go: [
        /import\s+['"]([^'"]+)['"]/g,
      ],
      rust: [
        /use\s+([a-zA-Z_][a-zA-Z0-9_:]*(?:::[a-zA-Z_][a-zA-Z0-9_]*)?)/g,
      ],
      java: [
        /import\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*;/g,
      ],
      cpp: [
        /#include\s*[<"]([^>"]+)[>"]/g,
      ],
    };
    return patterns[language] || patterns.javascript;
  }

  /**
   * 获取语言的 export 模式
   */
  _getExportPatterns(language) {
    const patterns = {
      javascript: [
        /export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)/g,
        /module\.exports\s*=\s*(\w+)/g,
      ],
      typescript: [
        /export\s+(?:default\s+)?(?:const|let|var|function|class|interface|type|enum)\s+(\w+)/g,
      ],
      python: [
        /^__all__\s*=\s*\[([^\]]+)\]/gm,
      ],
    };
    return patterns[language] || patterns.javascript;
  }

  /**
   * 提取函数定义
   */
  _extractFunctions(code, language) {
    const functions = [];
    const patterns = {
      javascript: /(?:async\s+)?(?:function\s+(\w+)|([\w$]+)\s*\(|const\s+([\w$]+)\s*=\s*(?:async\s+)?\(|([\w$]+)\s*:\s*(?:async\s+)?\([^)]+\)\s*=>)/g,
      typescript: /(?:async\s+)?(?:function\s+(\w+)|([\w$]+)\s*\(|const\s+([\w$]+)\s*=\s*(?:async\s+)?\(|([\w$]+)\s*:\s*(?:async\s+)?\([^)]+\)\s*=>)/g,
      python: /def\s+(\w+)\s*\(/gm,
      go: /func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(/g,
      rust: /fn\s+(\w+)\s*[<(]/g,
      java: /(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:void|[\w<>]+)\s+(\w+)\s*\(/g,
      cpp: /(?:virtual\s+)?(?:void|[\w<>]+)\s+(\w+)\s*\(/g,
    };

    const pattern = patterns[language] || patterns.javascript;
    let match;
    const regex = new RegExp(pattern.source, pattern.flags);
    while ((match = regex.exec(code)) !== null) {
      const name = match[1] || match[2] || match[3] || match[4];
      if (name && !['if', 'else', 'for', 'while', 'switch', 'catch', 'constructor'].includes(name)) {
        functions.push({ name, match: match[0] });
      }
    }
    return functions;
  }

  /**
   * 提取类定义
   */
  _extractClasses(code, language) {
    const patterns = {
      javascript: /class\s+(\w+)(?:\s+extends\s+(\w+))?/g,
      typescript: /class\s+(\w+)(?:\s+extends\s+(\w+))?/g,
      python: /^class\s+(\w+)(?:\([^)]+\))?:/gm,
      go: /type\s+(\w+)\s+struct/g,
      rust: /(?:struct|enum)\s+(\w+)/g,
      java: /(?:public|private|protected)?\s*class\s+(\w+)(?:\s+extends\s+\w+)?/g,
    };

    const pattern = patterns[language] || patterns.javascript;
    const classes = [];
    let match;
    const regex = new RegExp(pattern.source, pattern.flags);
    while ((match = regex.exec(code)) !== null) {
      classes.push(match[1]);
    }
    return [...new Set(classes)];
  }

  /**
   * 分析控制流复杂度
   */
  _analyzeControlFlow(code) {
    const nestedPattern = /for\s*\(|while\s*\(/g;
    const recursionPattern = /\b(\w+)\s*\([^)]*\)\s*\{\s*[\s\S]*?\1\s*\(/g;

    let nested = 0;
    let maxNested = 0;
    let match;

    while ((match = nestedPattern.exec(code)) !== null) {
      nested++;
      maxNested = Math.max(maxNested, nested);
    }

    const hasRecursion = recursionPattern.test(code);
    return {
      nested: maxNested,
      recursion: hasRecursion ? 1 : 0,
      hasLoop: /for\s*\(|while\s*\(/.test(code),
      hasAsync: /async|await|Promise/.test(code),
    };
  }

  /**
   * 提取框架名称
   */
  _extractFrameworkName(code, pattern) {
    const match = code.match(pattern);
    if (match) {
      // 遍历所有捕获组，返回第一个匹配的（兼容多捕获组模式）
      for (let i = 1; i < match.length; i++) {
        if (match[i]) return match[i];
      }
      return match[0].split('/').pop().replace(/['"]/g, '');
    }
    return null;
  }

  /**
   * 检测语言特定特性
   */
  _detectLanguageFeatures(code, language) {
    const features = [];
    const lang = language.toLowerCase();

    if (lang === 'javascript' || lang === 'typescript') {
      if (/class\s+\w+/.test(code)) features.push({ type: 'class', name: 'ES6 Class' });
      if (/async\s+function|await/.test(code)) features.push({ type: 'async', name: 'Async/Await' });
      if (/=>\s*{/.test(code)) features.push({ type: 'arrow', name: 'Arrow Function' });
      if (/\?\.\s*\w+/.test(code)) features.push({ type: 'optional', name: 'Optional Chaining' });
      if (/\?\s*\w+\s*:\s*\w+/.test(code)) features.push({ type: 'ternary', name: 'Ternary Operator' });
      if (/`[^`]*\$\{[^}]+\}[^`]*`/.test(code)) features.push({ type: 'template', name: 'Template Literal' });
      if (/\.\.\.\w+/.test(code)) features.push({ type: 'spread', name: 'Spread Operator' });
      if (/<[A-Z]\w+>/.test(code)) features.push({ type: 'generic', name: 'Generics' });
      if (/interface\s+\w+/.test(code)) features.push({ type: 'interface', name: 'Interface' });
      if (/type\s+\w+\s*=/.test(code)) features.push({ type: 'type', name: 'Type Alias' });
    }

    if (lang === 'python') {
      if (/def\s+(\w+)\s*\([^)]*\*\w+/.test(code)) features.push({ type: 'varargs', name: 'Variadic Args' });
      if (/def\s+(\w+)\s*\([^)]*\*\*\w+/.test(code)) features.push({ type: 'kwargs', name: 'Keyword Args' });
      if (/@(\w+)/.test(code)) features.push({ type: 'decorator', name: 'Decorator' });
      if (/with\s+open/.test(code)) features.push({ type: 'context', name: 'Context Manager' });
      if (/yield\s+/.test(code)) features.push({ type: 'generator', name: 'Generator' });
      if (/async\s+def/.test(code)) features.push({ type: 'async', name: 'Async Function' });
      if (/dataclass/.test(code)) features.push({ type: 'dataclass', name: 'Dataclass' });
      if (/Type\[/.test(code)) features.push({ type: 'typing', name: 'Type Hints' });
    }

    if (lang === 'go') {
      if (/go\s+\w+/.test(code)) features.push({ type: 'goroutine', name: 'Goroutine' });
      if (/chan\s+\w+/.test(code)) features.push({ type: 'channel', name: 'Channel' });
      if (/defer\s+/.test(code)) features.push({ type: 'defer', name: 'Defer' });
      if (/interface\s*{/.test(code)) features.push({ type: 'interface', name: 'Interface' });
      if (/:=/.test(code)) features.push({ type: '短变量声明', name: 'Short Declaration' });
      if (/\[\]interface\{\}/.test(code)) features.push({ type: 'emptyInterface', name: 'Empty Interface' });
    }

    if (lang === 'rust') {
      if (/fn\s+\w+.*->.*\{/.test(code)) features.push({ type: 'fn', name: 'Function' });
      if (/\bmatch\s+/.test(code)) features.push({ type: 'match', name: 'Match Expression' });
      if (/impl\s+\w+/.test(code)) features.push({ type: 'impl', name: 'Implementation' });
      if (/trait\s+\w+/.test(code)) features.push({ type: 'trait', name: 'Trait' });
      if (/->/.test(code)) features.push({ type: '返回类型', name: 'Return Type Annotation' });
      if (/\.map\(|\.filter\(|\.collect\(/.test(code)) features.push({ type: 'iterator', name: 'Iterator Chain' });
      if (/\.unwrap\(\)/.test(code)) features.push({ type: 'unwrap', name: 'Result Handling' });
      if (/Option<|Result</.test(code)) features.push({ type: 'option', name: 'Option/Result' });
    }

    return features;
  }

  /**
   * 从标签推断类别
   */
  _inferCategoryFromTags(tags, language) {
    const tagStr = tags.join(' ').toLowerCase();

    // 算法类
    if (/sort|search|recursion|dp|dynamic|graph|traverse|bfs|dfs/.test(tagStr)) {
      return 'algorithm';
    }
    // 数据结构类
    if (/tree|list|stack|queue|heap|hash|map|set|graph/.test(tagStr)) {
      return 'structure';
    }
    // 网络类
    if (/http|request|fetch|api|endpoint|server|client|websocket/.test(tagStr)) {
      return 'network';
    }
    // IO类
    if (/file|read|write|stream|parse|json|yaml|xml|csv/.test(tagStr)) {
      return 'io';
    }
    // 测试类
    if (/test|jest|mocha|unittest|pytest/.test(tagStr)) {
      return 'testing';
    }
    // 安全类
    if (/auth|encrypt|secure|sanitize|validate/.test(tagStr)) {
      return 'security';
    }
    // 数据库类
    if (/sql|query|database|db|mongo|postgres|mysql/.test(tagStr)) {
      return 'database';
    }
    // 并发类
    if (/async|await|promise|concurrent|parallel|worker|pool/.test(tagStr)) {
      return 'concurrency';
    }
    // 设计模式
    if (/singleton|factory|observer|strategy|decorator|adapter/.test(tagStr)) {
      return 'pattern';
    }

    return null;
  }

  /**
   * 估计代码复杂度
   */
  _estimateComplexity(code, controlFlowScore, functions) {
    let score = 0;

    // 基础：函数数量
    score += functions.length * 2;

    // 嵌套循环
    score += controlFlowScore.nested * 10;

    // 递归
    if (controlFlowScore.recursion > 0) score += 15;

    // 异步
    if (controlFlowScore.hasAsync) score += 5;

    // 行数
    const lines = code.split('\n').length;
    score += Math.min(lines / 10, 20);

    if (score < 10) return 'low';
    if (score < 30) return 'medium';
    return 'high';
  }

  // 计算余弦相似度（基于关键词标签）
  _cosineSimilarity(tags1, tags2) {
    if (!tags1 || !tags2 || tags1.length === 0 || tags2.length === 0) return 0;
    const set = [...new Set([...tags1, ...tags2])];
    const v1 = set.map(t => (tags1.includes(t) ? 1 : 0));
    const v2 = set.map(t => (tags2.includes(t) ? 1 : 0));
    const dot = v1.reduce((s, a, i) => s + a * v2[i], 0);
    const mag = (arr) => Math.sqrt(arr.reduce((s, x) => s + x * x, 0));
    const d = mag(v1) * mag(v2);
    return d === 0 ? 0 : dot / d;
  }

  // 搜索
  search(keyword, { language, category, limit = 10 } = {}) {
    const kw = keyword.toLowerCase();
    const results = this.snippets
      .filter(s => {
        if (language && s.language !== language) return false;
        if (category && s.category !== category) return false;
        return (
          s.name.toLowerCase().includes(kw) ||
          s.description.toLowerCase().includes(kw) ||
          s.tags.some(t => t.toLowerCase().includes(kw)) ||
          s.code.toLowerCase().includes(kw)
        );
      })
      .map(s => ({
        ...s,
        relevance: this._cosineSimilarity(
          kw.split(/\s+/),
          s.tags
        ),
      }))
      .sort((a, b) => {
        if (b.relevance !== a.relevance) return b.relevance - a.relevance;
        return (b.successRate || 0) - (a.successRate || 0);
      })
      .slice(0, limit);
    return { keyword, language, category, results, count: results.length };
  }

  // 添加代码片段
  addSnippet({ language, category, name, code, description = '', tags = [] }) {
    if (!language || !name || !code) {
      return { action: 'rejected', reason: 'missing_required_fields' };
    }
    const id = `snippet-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
    const snippet = {
      id,
      language,
      category: category || 'general',
      name,
      code,
      description,
      tags: tags.map(t => String(t).toLowerCase()),
      usageCount: 0,
      successRate: 0,
      createdAt: new Date().toISOString(),
      lastUsed: null,
      quality: 0,
    };
    this.snippets.push(snippet);
    this._dirty = true;
    this._save();
    return { action: 'added', snippet };
  }

  // 获取模式列表
  // 支持两种调用方式：
  //   - getPatterns({ language, category, tier }) —— 对象过滤，返回 { patterns, count, ... }
  //   - getPatterns(nameString) —— 按名称搜索，返回匹配的模式数组
  getPatterns(filter) {
    // 字符串参数 → 按名称搜索（返回数组，兼容 code-planner 调用）
    if (typeof filter === 'string') {
      const name = filter.toLowerCase();
      // 同时在 snippets（用户添加）和 BUILTIN_PATTERNS（内置）中搜索
      const results = [
        ...this.snippets.filter(s =>
          s.name && s.name.toLowerCase().includes(name)
        ),
        ...BUILTIN_PATTERNS.filter(p =>
          p.name && p.name.toLowerCase().includes(name)
        )
      ];
      return results;
    }

    // 对象参数 → 按 language/category/tier 过滤（返回原始对象格式）
    const { language, category, tier } = filter || {};
    let list = this.snippets;
    if (language) list = list.filter(s => s.language === language);
    if (category) list = list.filter(s => s.category === category);
    if (tier) list = list.filter(s => this._getTier(s) === tier);
    return { language, category, tier, patterns: list, count: list.length };
  }

  // 从成功案例学习（扩展签名支持执行结果）
  learnFromSuccess({ name, code, language, category, description, tags, quality = 0.8, executionResult = null, taskHash = null }) {
    // 如果提供了执行结果，使用 learnFromExecution 路径
    if (executionResult !== null) {
      return this.learnFromExecution(code, language, true, { output: executionResult }, taskHash);
    }

    // 原有的学习路径
    const result = this.addSnippet({ language, category, name, code, description, tags });
    if (result.action === 'added') {
      result.snippet.successRate = quality;
      result.snippet.quality = Math.round(quality * 100);
      result.snippet.usageCount = 1;
      result.snippet.lastUsed = new Date().toISOString();
      this._dirty = true;
      this._save();
    }
    return result;
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // 从执行结果学习
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * 从执行结果中学习
   *
   * @param {string} code - 代码文本
   * @param {string} language - 编程语言
   * @param {boolean} success - 是否成功
   * @param {Object} result - 执行结果 { output?, error?, exitCode? }
   * @param {string} taskHash - 可选，任务哈希用于关联学习
   * @returns {Object} { learned: true/false, snippetId?, errorPattern? }
   */
  learnFromExecution(code, language, success, result = {}, taskHash = null) {
    // 提取代码模式
    const extracted = this.extractPattern(code, language);

    if (success) {
      // 成功：提取模式 → 调用 addSnippet
      const snippetResult = this.addSnippet({
        language,
        category: extracted.category,
        name: extracted.exports[0] || extracted.tags[0] || `generated-${Date.now()}`,
        code,
        description: `自动提取: ${extracted.tags.slice(0, 5).join(', ')}`,
        tags: extracted.tags,
      });

      if (snippetResult.action === 'added') {
        snippetResult.snippet.successRate = 1.0;
        snippetResult.snippet.quality = 100;
        snippetResult.snippet.usageCount = 1;
        snippetResult.snippet.lastUsed = new Date().toISOString();
        snippetResult.snippet.verified = true;  // 标记为已验证
        this._dirty = true;
        this._save();

        // 关联学习：同一任务的多次成功生成自动关联
        if (taskHash) {
          this._associateTask(taskHash, snippetResult.snippet.id, 'success');
        }

        return {
          learned: true,
          snippetId: snippetResult.snippet.id,
          extracted: extracted,
        };
      }

      return { learned: false, reason: 'snippet_already_exists', extracted };
    } else {
      // 失败：提取错误模式 → 记录到失败模式库
      const errorPattern = this._extractErrorPattern(code, language, result);
      this._addFailedPattern(errorPattern);

      return {
        learned: true,
        errorPattern,
        extracted,
      };
    }
  }

  /**
   * 提取错误模式
   */
  _extractErrorPattern(code, language, result) {
    const errorType = this._classifyError(result.error || '', language);
    const errorCode = this._normalizeErrorCode(code, language);

    return {
      errorCode,           // 规范化后的错误代码摘要
      code: code.substring(0, 500),  // 截取前500字符
      language,
      errorType,
      reason: this._summarizeError(result.error || ''),
      count: 1,
      firstSeen: new Date().toISOString(),
      lastSeen: new Date().toISOString(),
    };
  }

  /**
   * 分类错误类型
   */
  _classifyError(errorMsg, language) {
    const msg = (errorMsg || '').toLowerCase();

    if (/syntaxerror|syntax error/i.test(msg)) return ERROR_TYPES.SYNTAX;
    if (/referenceerror|is not defined|cannot find|nameerror/i.test(msg)) return ERROR_TYPES.REFERENCE;
    if (/typeerror|cannot read property|cannot read|not a function/i.test(msg)) return ERROR_TYPES.TYPE;
    if (/importerror|modulenotfounderror|cannot find module|npm install/i.test(msg)) return ERROR_TYPES.IMPORT;
    if (/timeout|time limit/i.test(msg)) return ERROR_TYPES.TIMEOUT;
    if (/logic|logical|incorrect|wrong/i.test(msg)) return ERROR_TYPES.LOGIC;
    if (/dependency|require|import/i.test(msg)) return ERROR_TYPES.DEPENDENCY;

    // 运行时错误检测
    if (/error|exception/i.test(msg)) return ERROR_TYPES.RUNTIME;

    return ERROR_TYPES.UNKNOWN;
  }

  /**
   * 规范化错误代码（提取关键特征）
   */
  _normalizeErrorCode(code, language) {
    // 移除注释和字符串，提取关键结构
    let normalized = code
      .replace(/\/\/.*$/gm, '')  // 移除单行注释
      .replace(/\/\*[\s\S]*?\*\//g, '')  // 移除多行注释
      .replace(/'[^']*'/g, "''")  // 替换字符串
      .replace(/"[^"]*"/g, '""')
      .replace(/`[^`]*`/g, '``')
      .replace(/\d+/g, 'N')  // 替换数字
      .replace(/[ \t]+/g, ' ')  // 规范化空白
      .trim();

    // 限制长度
    if (normalized.length > 200) {
      normalized = normalized.substring(0, 200);
    }

    return normalized;
  }

  /**
   * 总结错误信息
   */
  _summarizeError(errorMsg) {
    if (!errorMsg) return 'Unknown error';

    // 提取关键错误信息
    const match = errorMsg.match(/(?:Error|Exception):\s*(.+?)(?:\n|$)/i);
    if (match) return match[1].trim();

    // 截取前100字符
    return errorMsg.substring(0, 100).trim();
  }

  /**
   * 添加失败模式
   */
  _addFailedPattern(pattern) {
    // 检查是否已存在相同的错误模式
    const existing = this.failedPatterns.findIndex(
      p => p.errorCode === pattern.errorCode && p.language === pattern.language
    );

    if (existing >= 0) {
      // 已存在，更新计数
      this.failedPatterns[existing].count++;
      this.failedPatterns[existing].lastSeen = new Date().toISOString();
      // 更新代码示例（保留最新的）
      this.failedPatterns[existing].code = pattern.code;
    } else {
      // 新增
      this.failedPatterns.push(pattern);
    }

    this._saveFailedPatterns();
  }

  /**
   * 检查代码是否匹配已知的失败模式
   */
  isFailedPattern(code, language) {
    const errorCode = this._normalizeErrorCode(code, language);
    const pattern = this.failedPatterns.find(
      p => p.errorCode === errorCode && p.language === language
    );

    if (pattern) {
      return {
        isMatch: true,
        pattern: {
          errorType: pattern.errorType,
          count: pattern.count,
          lastSeen: pattern.lastSeen,
        },
      };
    }

    return { isMatch: false };
  }

  /**
   * 获取失败模式统计
   */
  getFailedPatternsStats() {
    const byType = {};
    for (const p of this.failedPatterns) {
      byType[p.errorType] = (byType[p.errorType] || 0) + 1;
    }

    return {
      total: this.failedPatterns.length,
      byErrorType: byType,
      topPatterns: this.failedPatterns
        .sort((a, b) => b.count - a.count)
        .slice(0, 10)
        .map(p => ({
          errorType: p.errorType,
          count: p.count,
          lastSeen: p.lastSeen,
        })),
    };
  }

  // ═══════════════════════════════════════════════════════════════════════════════
  // 关联学习
  // ═══════════════════════════════════════════════════════════════════════════════

  /**
   * 关联同一任务的多次成功生成
   *
   * @param {string} taskHash - 任务哈希
   * @param {string} snippetId - 代码片段ID
   * @param {string} outcome - 结果类型: 'success' | 'failure'
   */
  _associateTask(taskHash, snippetId, outcome) {
    if (!this.taskAssociations[taskHash]) {
      this.taskAssociations[taskHash] = {
        taskHash,
        snippetIds: [],
        successCount: 0,
        failureCount: 0,
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString(),
      };
    }

    const assoc = this.taskAssociations[taskHash];

    // 避免重复添加同一个snippet
    if (!assoc.snippetIds.includes(snippetId)) {
      assoc.snippetIds.push(snippetId);
    }

    if (outcome === 'success') {
      assoc.successCount++;
    } else {
      assoc.failureCount++;
    }

    assoc.lastUpdated = new Date().toISOString();

    this._saveTaskAssociations();
  }

  /**
   * 获取任务的关联模式
   */
  getTaskAssociations(taskHash) {
    const assoc = this.taskAssociations[taskHash];
    if (!assoc) {
      return { taskHash, snippets: [], verified: false };
    }

    // 获取关联的snippet
    const snippets = assoc.snippetIds
      .map(id => this.snippets.find(s => s.id === id))
      .filter(Boolean);

    // 已验证模式：至少有一个通过执行验证的代码
    const verified = snippets.some(s => s.verified === true);

    return {
      taskHash,
      snippets,
      successCount: assoc.successCount,
      failureCount: assoc.failureCount,
      verified,
      lastUpdated: assoc.lastUpdated,
    };
  }

  /**
   * 查找相似任务的已验证模式
   */
  findVerifiedPatterns(taskHash, minSuccessRate = 0.8) {
    // 查找所有与给定taskHash有相似前缀的关联
    const similarTasks = Object.values(this.taskAssociations)
      .filter(assoc => {
        // 使用简单的编辑距离检查相似性
        const similarity = this._calculateSimilarity(taskHash, assoc.taskHash);
        return similarity > 0.6;  // 60% 相似度阈值
      })
      .flatMap(assoc => assoc.snippetIds)
      .map(id => this.snippets.find(s => s.id === id))
      .filter(Boolean);

    // 过滤已验证且成功率高的模式
    return similarTasks
      .filter(s => s.verified === true && (s.successRate || 0) >= minSuccessRate)
      .sort((a, b) => (b.successRate || 0) - (a.successRate || 0));
  }

  /**
   * 计算字符串相似度（简单实现）
   */
  _calculateSimilarity(str1, str2) {
    if (str1 === str2) return 1;
    if (!str1 || !str2) return 0;

    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;

    if (longer.length === 0) return 1;

    // 简单的字符重叠率
    const longerChars = [...longer];
    const shorterChars = [...shorter];
    let matches = 0;

    for (const char of shorterChars) {
      const idx = longerChars.indexOf(char);
      if (idx !== -1) {
        matches++;
        longerChars.splice(idx, 1);
      }
    }

    return (matches * 2) / (str1.length + str2.length);
  }

  /**
   * 获取关联学习统计
   */
  getAssociationStats() {
    const tasks = Object.values(this.taskAssociations);
    const totalSuccess = tasks.reduce((sum, t) => sum + t.successCount, 0);
    const totalFailure = tasks.reduce((sum, t) => sum + t.failureCount, 0);

    return {
      totalTasks: tasks.length,
      totalSuccess,
      totalFailure,
      avgSuccessRate: totalSuccess + totalFailure > 0
        ? (totalSuccess / (totalSuccess + totalFailure)).toFixed(2)
        : 0,
      verifiedTasks: tasks.filter(t =>
        t.snippetIds.some(id => {
          const s = this.snippets.find(sn => sn.id === id);
          return s && s.verified === true;
        })
      ).length,
    };
  }

  // 进化：淘汰低质量模式
  evolve({ minQuality = 30, minSuccessRate = 0.3, maxAge = 90 } = {}) {
    const now = Date.now();
    const survivors = this.snippets.filter(s => {
      const ageDays = (now - new Date(s.createdAt).getTime()) / (1000 * 60 * 60 * 24);
      return (
        (s.quality || 0) >= minQuality ||
        (s.successRate || 0) >= minSuccessRate ||
        ageDays < maxAge
      );
    });
    const eliminated = this.snippets.filter(s => !survivors.includes(s));
    this.snippets = survivors;
    this._dirty = true;
    this._save();
    return {
      before: this.snippets.length + eliminated.length,
      after: this.snippets.length,
      eliminated: eliminated.length,
      survivors: survivors.length,
    };
  }

  // 统计信息
  stats() {
    const byLang = {};
    const byTier = { hot: 0, warm: 0, cold: 0 };
    for (const s of this.snippets) {
      byLang[s.language] = (byLang[s.language] || 0) + 1;
      byTier[this._getTier(s)]++;
    }
    return {
      total: this.snippets.length,
      byLanguage: byLang,
      byTier,
      builtin: BUILTIN_PATTERNS.length,
      failedPatterns: this.failedPatterns.length,
      taskAssociations: Object.keys(this.taskAssociations).length,
    };
  }

  // 统一路由分发
  dispatch(action, ...args) {
    switch (action) {
      case 'search':
        return this.search(...args);
      case 'addSnippet':
        return this.addSnippet(...args);
      case 'getPatterns':
        return this.getPatterns(...args);
      case 'learnFromSuccess':
        return this.learnFromSuccess(...args);
      case 'learnFromExecution':
        return this.learnFromExecution(...args);
      case 'evolve':
        return this.evolve(...args);
      case 'extractPattern':
        return this.extractPattern(...args);
      case 'isFailedPattern':
        return this.isFailedPattern(...args);
      case 'getFailedPatternsStats':
        return this.getFailedPatternsStats();
      case 'getTaskAssociations':
        return this.getTaskAssociations(...args);
      case 'findVerifiedPatterns':
        return this.findVerifiedPatterns(...args);
      case 'getAssociationStats':
        return this.getAssociationStats();
      default:
        return { error: `Unknown action: ${action}` };
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// 导出
// ═══════════════════════════════════════════════════════════════════════════════

module.exports = { CodeKnowledge, BUILTIN_PATTERNS };
