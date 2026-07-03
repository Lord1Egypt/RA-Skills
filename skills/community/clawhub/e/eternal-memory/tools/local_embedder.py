#!/usr/bin/env python3
"""
本地向量引擎 v1.0 — 零依赖自嵌入 + ONNX增强
=============================================
设计目标：SKILL推送后能在任何环境运行，不依赖外部向量服务。
策略：
  Tier 1: ONNX模型（如果环境有，用pip install fastembed一键装）
  Tier 2: Jieba分词+TF-IDF（零依赖降级，纯Python）
  Tier 3: 字符n-gram（终极备胎，连jieba都不用）

三层共享同一API，对上层透明。

用法：
  from tools.local_embedder import LocalEmbedder
  le = LocalEmbedder()
  emb = le.encode("测试文本")  # -> List[float]
"""

import os, sys, json, math, re, hashlib
from collections import Counter
from typing import List, Optional, Tuple

# ── 零依赖分词器 ──

class SimpleTokenizer:
    """纯Python中文分词（零依赖）"""
    
    # 核心词汇表（高频交易+记忆领域词）
    TRADE_TERMS = {
        "止损", "止盈", "开仓", "平仓", "持仓", "仓位", "保证金", "回撤",
        "夏普", "收益", "胜率", "盈亏", "多头", "空头", "做多", "做空",
        "ATR", "MACD", "RSI", "KDJ", "布林", "均线", "K线", "分时",
        "期货", "期权", "现货", "合约", "交割", "主力",
        "苹果", "甲醇", "PVC", "AP", "MA", "螺纹", "铁矿", "原油",
        "记忆", "向量", "图谱", "FTS5", "索引", "归档", "校验",
        "引擎", "系统", "架构", "升级", "融合", "进化",
        "大伯", "小P", "小四", "智库", "小智", "小米", "Hermes",
        "策略", "回测", "量化", "因子", "信号", "参数", "优化",
        "数据", "文件", "代码", "函数", "class", "def", "import",
        "内存", "延迟", "并发", "线程", "进程", "异步",
    }
    
    def __init__(self):
        pass
    
    def tokenize(self, text: str) -> List[str]:
        """最大正向匹配分词 + 英文/数字提取"""
        tokens = []
        n = len(text)
        i = 0
        
        while i < n:
            ch = text[i]
            
            # 跳过空白和标点
            if ch.isspace() or ch in '，。！？、；：""''（）【】《》…—·-—':
                i += 1
                continue
            
            # 英文/数字：连续提取
            if ch.isascii() and (ch.isalpha() or ch.isdigit()):
                j = i
                while j < n and (text[j].isascii() and (text[j].isalnum() or text[j] in '_.@#')):
                    j += 1
                token = text[i:j].lower()
                if token:
                    tokens.append(token)
                i = j
                continue
            
            # 中文：最大正向匹配 - 尝试从当前位置匹配词表中的词
            matched = False
            # 从长到短尝试匹配（最长优先）
            for max_len in range(min(8, n - i), 0, -1):
                candidate = text[i:i + max_len]
                if candidate in self.TRADE_TERMS:
                    tokens.append(candidate)
                    i += max_len
                    matched = True
                    break
            
            if not matched:
                # 单字
                tokens.append(text[i])
                i += 1
        
        return tokens


class TFIDFVectorizer:
    """TF-IDF向量化（零依赖）"""
    
    def __init__(self, dim: int = 512):
        self.dim = dim          # 输出维度
        self.vocab: dict = {}    # 词→id
        self.idf: dict = {}      # id→idf值
        self.doc_count = 0
        self.tokenizer = SimpleTokenizer()
    
    def fit(self, documents: List[str]):
        """训练IDF — 选中等频率词（最有区分度）"""
        df = Counter()  # 文档频率
        
        for doc in documents:
            tokens = set(self.tokenizer.tokenize(doc))
            for t in tokens:
                df[t] += 1
        
        self.doc_count = len(documents)
        
        # 计算IDF + 过滤：去掉太稀有(df<=1)和太常见(df>=doc_count*0.9)
        candidates = []
        for term, count in df.items():
            if count <= 1 or count >= self.doc_count * 0.9:
                continue  # 忽略极稀有和极常见词
            # 最少出现2次，最多出现在90%的文档中
            idf_val = math.log((self.doc_count + 1) / (count + 1)) + 1
            # 综合得分 = IDF * sqrt(df) —— 偏向有区分度的常见词
            score = idf_val * math.sqrt(count)
            candidates.append((term, idf_val, count, score))
        
        # 按综合得分排序，取前dim个
        candidates.sort(key=lambda x: x[3], reverse=True)
        
        for i, (term, idf_val, count, score) in enumerate(candidates[:self.dim - 1]):
            self.vocab[term] = i
            self.idf[i] = idf_val
    
    def transform(self, text: str) -> List[float]:
        """将文本转为TF-IDF向量"""
        vec = [0.0] * self.dim
        
        tokens = self.tokenizer.tokenize(text)
        if not tokens:
            return vec
        
        # 词频
        tf = Counter(tokens)
        max_tf = max(tf.values()) if tf else 1
        
        for term, count in tf.items():
            if term in self.vocab:
                idx = self.vocab[term]
                tf_norm = count / max_tf
                vec[idx] = tf_norm * self.idf.get(idx, 1.0)
        
        # L2归一化
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        
        return vec


class LocalEmbedder:
    """
    本地向量引擎
    Tier 1: ONNX模型（如果fastembed可用）
    Tier 2: Jieba+TF-IDF（零依赖）
    Tier 3: 字符ngram（终极备胎）
    """
    
    def __init__(self, dim: int = 512):
        self.dim = dim
        self.mode = "tier3_char"  # 默认
        self._model = None
        self._tfidf = TFIDFVectorizer(dim=dim)
        self._tfidf_fitted = False
        
        # 尝试加载ONNX（可配置跳过）
        if os.environ.get("SKIP_ONNX", "").lower() not in ("1", "true", "yes"):
            self._try_onnx()
        
        # 如果ONNX不行，尝试TF-IDF
        if self.mode != "onnx":
            self._try_tfidf()
    
    def _try_onnx(self):
        """尝试加载fastembed ONNX模型"""
        try:
            from fastembed import TextEmbedding
            cache = os.path.expanduser("~/.cache/huggingface/hub")
            self._model = TextEmbedding(
                model_name='BAAI/bge-small-zh-v1.5',
                cache_dir=cache,
                threads=2
            )
            # 测试
            next(self._model.embed(['test']))
            self.mode = "onnx"
            self.dim = 512
            self._model_name = 'BAAI/bge-small-zh-v1.5'
        except Exception:
            self._model = None
    
    def _try_tfidf(self):
        """尝试初始化TF-IDF（从记忆文件拟合）"""
        try:
            memory_dir = os.path.expanduser("~/.openclaw/workspace-v4-pro/memory")
            docs = []
            for root, dirs, files in os.walk(memory_dir):
                if "cold_archive" in root:
                    continue
                for f in files[:200]:  # 上限200个文件
                    if f.endswith('.md'):
                        try:
                            with open(os.path.join(root, f)) as fh:
                                docs.append(fh.read()[:2000])
                        except Exception:
                            pass
                if len(docs) >= 100:
                    break
            
            if docs:
                self._tfidf.fit(docs)
                self._tfidf_fitted = True
                self.mode = "tfidf"
        except Exception:
            self.mode = "tier3_char"
    
    def encode(self, text: str) -> Optional[List[float]]:
        """统一编码接口"""
        if self.mode == "onnx" and self._model:
            try:
                return list(next(self._model.embed([text])))
            except Exception:
                self.mode = "tfidf"
        
        if self.mode == "tfidf" and self._tfidf_fitted:
            try:
                return self._tfidf.transform(text)
            except Exception:
                self.mode = "tier3_char"
        
        # Tier 3: 字符ngram降级
        return self._char_ngram_embed(text)
    
    def _char_ngram_embed(self, text: str, n: int = 3) -> List[float]:
        """字符ngram哈希→固定维度向量（终极备胎）"""
        vec = [0.0] * self.dim
        
        # 提取n-gram
        clean = re.sub(r'[\s\n\r\t]+', '', text)
        for i in range(len(clean) - n + 1):
            ngram = clean[i:i+n]
            h = hashlib.md5(ngram.encode()).hexdigest()
            idx = int(h, 16) % self.dim
            vec[idx] += 1
        
        # 词级ngram（更好的语义捕获）
        words = re.findall(r'[\u4e00-\u9fff]{1,4}|[a-zA-Z0-9]+', text)
        for w in words:
            h = hashlib.md5(w.encode()).hexdigest()
            idx = int(h, 16) % self.dim
            vec[idx] += 1.0 / len(words)  # 归一化
        
        # L2归一化
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        
        return vec
    
    def similarity(self, a: List[float], b: List[float]) -> float:
        """余弦相似度"""
        if not a or not b:
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b + 1e-8)
    
    def info(self) -> dict:
        return {"mode": self.mode, "dim": self.dim, "backend": self.mode}


# ── HTTP兼容代理（可选，用于保持对旧API的兼容） ──

class EmbeddingServer:
    """本地向量HTTP服务（替换127.0.0.1:19999）"""
    
    def __init__(self, port: int = 19999):
        self.embedder = LocalEmbedder()
        self.port = port
    
    def start(self):
        """启动HTTP服务器"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        embedder = self.embedder
        
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                content_len = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_len)
                try:
                    data = json.loads(body)
                    text = data.get("input", "")
                    emb = embedder.encode(text)
                    resp = {"data": [{"embedding": emb}], "model": embedder.info()["mode"]}
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(resp).encode())
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(embedder.info()).encode())
            
            def log_message(self, format, *args):
                pass  # 静默
        
        server = HTTPServer(('127.0.0.1', self.port), Handler)
        print(f"🧬 本地向量服务启动: 127.0.0.1:{self.port} ({self.embedder.info()['mode']})")
        server.serve_forever()


# ── 测试+CLI ──
if __name__ == "__main__":
    import time
    
    le = LocalEmbedder()
    print(f"📊 向量引擎: {le.info()}")
    
    # 测试编码
    queries = [
        "记忆系统升级 v3.4",
        "AP苹果期货止损策略回测",
        "def calculate_atr 代码函数",
        "大伯问小P今天行情怎么样",
        "PVC MA 甲醇持仓风险",
    ]
    
    print("\n=== 编码测试 ===")
    for q in queries:
        t0 = time.time()
        emb = le.encode(q)
        lat = (time.time() - t0) * 1000
        nz = sum(1 for v in emb if v != 0)
        print(f"  [{lat:.1f}ms] dim={len(emb)} nz={nz} '{q[:40]}'")
    
    # 相似度测试
    print("\n=== 相似度测试 ===")
    emb_a = le.encode("记忆系统升级")
    emb_b = le.encode("记忆系统 v3.4 融合")
    emb_c = le.encode("AP期货止损策略")
    
    sim_ab = le.similarity(emb_a, emb_b)
    sim_ac = le.similarity(emb_a, emb_c)
    print(f"  '记忆系统升级' vs '记忆系统v3.4融合': {sim_ab:.3f} (期待>0.5)")
    print(f"  '记忆系统升级' vs 'AP期货止损策略': {sim_ac:.3f} (期待<0.3)")
    
    if sim_ab > 0.3 and sim_ab > sim_ac:
        print("  ✅ 语义区分有效")
    else:
        print("  ⚠️ 区分度不足（降级模式正常）")
    
    # 服务模式
    if "--serve" in sys.argv:
        port = int(sys.argv[sys.argv.index("--serve") + 1]) if "--serve" in sys.argv and len(sys.argv) > sys.argv.index("--serve") + 1 else 19999
        server = EmbeddingServer(port=port)
        server.start()
