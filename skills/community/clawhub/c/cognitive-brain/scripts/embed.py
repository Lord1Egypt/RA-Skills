#!/usr/bin/env python3
"""
Cognitive Brain - 本地 Embedding 生成器 v2
使用 sentence-transformers 生成本地 embedding

v2 改进：
- 静默模型加载日志
- 支持预热模式
- 支持服务模式（长期运行）
"""

import os
import sys
import json
import warnings
import logging

# ===== 在任何导入之前设置环境变量 =====
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# 完全静默 logging
logging.getLogger('sentence_transformers').setLevel(logging.CRITICAL)
logging.getLogger('transformers').setLevel(logging.CRITICAL)
logging.getLogger('torch').setLevel(logging.CRITICAL)
logging.getLogger('filelock').setLevel(logging.CRITICAL)

# 抑制所有警告
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# 重定向 stderr 到 /dev/null（仅在非服务模式）
if '--serve' not in sys.argv and '--warmup' not in sys.argv:
    import contextlib
    sys.stderr = open(os.devnull, 'w')

from sentence_transformers import SentenceTransformer

# 使用多语言小模型（支持中文，384 维）
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
model = None

def get_model():
    """获取或加载模型"""
    global model
    if model is None:
        # 再次确保静默
        import transformers
        transformers.logging.set_verbosity_error()
        
        model = SentenceTransformer(MODEL_NAME)
    return model

def embed(texts):
    """生成 embedding 向量"""
    m = get_model()
    embeddings = m.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.tolist()

def warmup():
    """预热模型 - 加载并运行一次"""
    import time
    start = time.time()
    m = get_model()
    # 运行一次编码来完全加载
    m.encode(["预热测试"], show_progress_bar=False)
    elapsed = time.time() - start
    return elapsed

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 embed.py <文本> | --batch <json> | --warmup | --serve"}))
        sys.exit(1)
    
    if sys.argv[1] == '--warmup':
        # 预热模式 - 恢复 stderr 以输出结果
        sys.stderr = sys.__stderr__
        elapsed = warmup()
        print(json.dumps({"status": "warmed_up", "elapsed_seconds": round(elapsed, 2)}))
        
    elif sys.argv[1] == '--serve':
        # 服务模式 - 从 stdin 读取请求，持续运行
        # 恢复 stderr 以输出状态
        sys.stderr = sys.__stderr__
        
        # 预热
        warmup()
        sys.stderr.write(json.dumps({"status": "ready"}) + "\n")
        sys.stderr.flush()
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                request = json.loads(line.strip())
                
                if 'text' in request:
                    # 单个文本
                    embedding = embed([request['text']])[0]
                    print(json.dumps({"embedding": embedding, "dimension": len(embedding)}))
                elif 'texts' in request:
                    # 批量
                    embeddings = embed(request['texts'])
                    print(json.dumps({"embeddings": embeddings, "dimension": len(embeddings[0])}))
                else:
                    print(json.dumps({"error": "无效请求"}))
                    
                sys.stdout.flush()
            except Exception as e:
                print(json.dumps({"error": str(e)}))
                sys.stdout.flush()
                
    elif sys.argv[1] == '--batch':
        # 批量处理
        texts = json.loads(sys.argv[2])
        embeddings = embed(texts)
        print(json.dumps({"embeddings": embeddings, "dimension": len(embeddings[0])}))
        
    else:
        # 单个文本
        text = sys.argv[1]
        embeddings = embed([text])
        print(json.dumps({
            "embedding": embeddings[0],
            "dimension": len(embeddings[0])
        }))

if __name__ == '__main__':
    main()
